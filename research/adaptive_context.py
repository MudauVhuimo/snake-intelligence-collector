"""State-stratified observational survival and food evidence for ADAPT-07.

NOT an optimal adaptive policy estimator. Uses PRE-outcome length, arena
occupancy, head pressure and game phase. The next 10 turns have to be
contiguous; food counts stop at first recorded death.
"""
from __future__ import annotations
import argparse
import csv
import gzip
import hashlib
import json
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path

from .threat_windows_core import board_shape, coord, heads, scan_replay

def density_band(value):
    if value < .15:return "low_<15%"
    if value < .30:return "mid_15-30%"
    return "high_>=30%"

def phase_band(turn):
    if turn < 500:return "early_0-499"
    if turn < 1500:return "middle_500-1499"
    return "late_1500+"

def occupied_fraction(frame,width,height):
    occupied=set()
    for snake in frame.get("snakes",()):
        if snake.get("alive"):
            occupied.update(p for x in snake.get("body",()) if (p:=coord(x)) is not None)
    occupied.update(p for x in frame.get("obstacles",()) if (p:=coord(x)) is not None)
    return len(occupied)/(width*height)

def observed_replay(replay, mode, season, path, sha):
    w,h=board_shape(replay)
    samples, qc=scan_replay(replay,season,path,mode,sha)
    tmap={frame["turn"]:frame for frame in replay["frames"]
          if isinstance(frame.get("turn"),int)}
    rows=[]
    for sample in samples:
        t=sample["start_turn"]
        frame=tmap.get(t)
        if frame is None:continue
        ids=[sid for sid,(name,head,length) in heads(frame).items()
             if name==sample["student"]]
        if len(ids)!=1:
            qc["ambiguous_student_id"]+=1
            continue
        sid=ids[0]
        foods=0
        # Food retained before any death (not after a 5-turn respawn).
        for step in range(1,11):
            after=tmap[t+step]
            events=after.get("events",())
            if any(e.get("kind")=="died" and e.get("snake")==sid for e in events):
                break
            foods+=sum(e.get("kind")=="ate" and e.get("snake")==sid for e in events)
        fraction=occupied_fraction(frame,w,h)
        rows.append(dict(sha=sha,mode=mode,season=season,student=sample["student"],
                         turn=t,length=sample["length"],
                         length_bin=sample["length_bin"],
                         density=fraction,density_bin=density_band(fraction),
                         phase=phase_band(t),head_pressure=sample["head_pressure"],
                         free_exits=sample["neighbor_exits"],
                         death_10=sample["death_next_10"],food_10=foods,
                         is_palmer="palmer" in sample["student"].lower()))
    return rows,qc

def scan(data_dir,max_files=250):
    root=data_dir/"replays"
    paths=sorted(root.rglob("*.rep.gz"),reverse=True)
    chosen=paths[:max_files] if max_files else paths
    seen=set()
    quality=Counter(available_files=len(paths),selected_files=len(chosen))
    output=[]
    for path in chosen:
        rel=path.relative_to(root)
        mode="trial" if "trials" in rel.parts else "league"
        try:
            with gzip.open(path,"rb") as file:raw=file.read()
            sha=hashlib.sha256(raw).hexdigest()
            if sha in seen:
                quality["duplicate_payloads"]+=1
                continue
            rows,qc=observed_replay(json.loads(raw),mode,rel.parts[0],str(rel),sha)
        except (ValueError,OSError,TypeError,KeyError):
            quality["invalid_replays"]+=1
            continue
        seen.add(sha)
        quality[mode+"_replays"]+=1
        quality.update(qc)
        output.extend(rows)
    return output,quality

def summary(rows,fields):
    by=defaultdict(lambda:[0,0,0,set()])
    for row in rows:
        key=tuple(row[x] for x in fields)
        group=by[key]
        group[0]+=1
        group[1]+=int(row["death_10"])
        group[2]+=int(row["food_10"])
        group[3].add(row["sha"])
    return sorted((key,dict(n=n,deaths=d,food=f,games=len(games),
                            death_pct=100*d/n,food_per_100=100*f/n))
                  for key,(n,d,f,games) in by.items())

def build(data_dir,max_files=250):
    rows,quality=scan(data_dir,max_files)
    report_dir=data_dir/"reports"
    derived_dir=data_dir/"derived"
    report_dir.mkdir(parents=True,exist_ok=True)
    derived_dir.mkdir(parents=True,exist_ok=True)
    fields=("mode","length_bin","density_bin","phase","head_pressure",
            "turn","density","death_10","food_10","sha","student","is_palmer")
    export=derived_dir/"adaptive_state_windows.csv"
    with export.open("w",newline="",encoding="utf-8") as file:
        writer=csv.DictWriter(file,fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k:row[k] for k in fields})
    def rate(n,d):
        return f"{100*d/n:.2f}%" if n else "insufficient"
    lines=[
        "# Snake26: are risk and food opportunities state-dependent?", "",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"), "",
        "## Study design and missingness", "",
        "For each living STUDENT at turns divisible by 25, use only features",
        "visible at that turn: body length, full occupied-cell fraction (including",
        "obstacles), nearest opponent head distance and turn phase. Require 10",
        "consecutive future frames and classify actual death events (not being",
        "alive at the final frame after respawn). Count actual apple events only",
        "UNTIL first death. Cohorts below are DESCRIPTIVE; they do not measure",
        "what a changed decision would do. Student peer league and fixed trials",
        "are never pooled for inferential comparisons.", "",
        "Density bands fixed BEFORE viewing results: <15%, 15-<30%, >=30%.",
        "Phases: turns 0-499, 500-1499, 1500+; length bands: 5-24, 25-49, 50-99, 100+.",
        "All density is instantaneous arena occupancy, not a measured",
        "probability of a path becoming blocked.", "",
        f"Unique peer league replays: **{quality['league_replays']}**; trial replays: **{quality['trial_replays']}**.",
        f"Observed complete 10-turn windows: **{len(rows)}**;",
        f"league **{sum(r['mode']=='league' for r in rows)}**,",
        f"trials **{sum(r['mode']=='trial' for r in rows)}**.",
        f"Duplicate replay payloads removed: **{quality['duplicate_payloads']}**.",
        "",
        "## Stratified actual outcomes", "",
        "Death percentage is DIED within next 10 turns / eligible windows;",
        "food rate is confirmed eats before any death / 100 eligible windows.",
        "Nearby repeated windows and the same students make the raw fractions",
        "correlated. **No cross-row causal effect claim**.", "",
    ]
    for name,fields in [
        ("Body length",("mode","length_bin")),
        ("Arena occupancy",("mode","density_bin")),
        ("Game phase",("mode","phase")),
        ("Length × occupancy",("mode","length_bin","density_bin")),
        ("Length × phase",("mode","length_bin","phase")),
        ("Head proximity × occupancy",("mode","head_pressure","density_bin")),
    ]:
        groups=summary(rows,fields)
        lines.extend(["### "+name,"",
                      "| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |",
                      "|---|---|---:|---:|---:|---:|---:|"])
        for key,g in groups:
            mode,*bands=key
            if len(fields)>2 and (g["n"]<30 or g["games"]<3):
                continue
            label=" / ".join(bands)
            lines.append(f"| {mode} | {label} | {g['n']} | {g['games']} | "
                         f"{g['deaths']} | {g['death_pct']:.2f}% | {g['food_per_100']:.2f} |")
        lines.append("")
    for mode in ("league","trial"):
        mode_rows=[r for r in rows if r["mode"]==mode]
        palmer=[r for r in mode_rows if r["is_palmer"]]
        if mode=="league":
            lines.extend(["## Palmer as reference subset, not population replacement","",
                          f"Palmer league windows: **{len(palmer)}** / **{len(mode_rows)}** league windows;",
                          f"death events in next 10: **{sum(r['death_10'] for r in palmer)}**;",
                          f"observed apple events before death: **{sum(r['food_10'] for r in palmer)}**.",
                          "Selected games/versions are not a matched estimate of Palmer's",
                          "causal strategy or an appropriate single-opponent benchmark.",""])
    lines+=["## What this can and cannot conclude","",
            "- State/length/density/phase interactions are measurable; raw group",
            "  differences justify TESTING an adaptive score, not choosing weights.",
            "- A crowded phase may correlate with long bodies and better peers;",
            "  the rate differences do NOT isolate density itself.",
            "- Small cells, rare deaths and repeated snapshots can yield unstable",
            "  risks. Censoring at match end is handled by requiring full followup.",
            "- To advance beyond observation, fit/validate pre-action interaction",
            "  predictors on whole held-out seasons/games, then compare adaptive",
            "  versus fixed-weight Java agents on fresh paired seeds.",
            "", "[Auditable window-level export](../derived/adaptive_state_windows.csv).",
            "**No new game-playing policy has been proved by these observations.**", ""]
    target=report_dir/"adaptive_context.md"
    target.write_text("\n".join(lines),encoding="utf-8")
    return dict(windows=len(rows),quality=dict(quality),report=str(target),
                league_deaths=sum(r["death_10"] for r in rows if r["mode"]=="league"))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir",type=Path,default=Path("data"))
    parser.add_argument("--max-files",type=int,default=250)
    args=parser.parse_args()
    if args.max_files<0:parser.error("max-files must be >=0")
    print(json.dumps(build(args.data_dir,args.max_files),indent=2))

if __name__=="__main__":
    main()
