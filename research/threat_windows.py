"""League vs controlled-trial head-pressure and near-death research report.

Inputs: raw gzip replays, deduplicated by SHA; fixed 25-turn sampling and
10-turn future death-event window. All estimates are *observational*.
"""
from collections import Counter,defaultdict
from datetime import datetime,timezone
from html import escape
from pathlib import Path
import argparse
import csv
import json
import random

from .threat_windows_core import load,summarize,per_student,LENGTH_BINS

BUCKETS=("near_0_3","middle_4_7","far_8_plus")
NAMES={"near_0_3":"Opponent head ≤3","middle_4_7":"Head 4–7",
       "far_8_plus":"Head ≥8"}
TRACKED=("421462-alexander-palmer","388060-tshepang-tshabalala",
         "428786-marvellous-sambo","409997-utayan-naidoo",
         "403754-vhuimo-mudau")

def percentage(n,d):
    return 100*n/d if d else None

def f(value,precision=2):
    return "n/a" if value is None else f"{value:.{precision}f}"

def write_csv(path,records,columns=None):
    path.parent.mkdir(parents=True,exist_ok=True)
    cols=columns or (list(records[0]) if records else ["season","student","mode"])
    with path.open("w",newline="",encoding="utf-8") as stream:
        writer=csv.DictWriter(stream,fieldnames=cols,extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

def risk_plot(path,rates,title):
    """Avoid rendering missing exposures as an apparent zero-risk bar."""
    high=max([x["risk"] for x in rates.values() if x["risk"] is not None]+[.1])*1.18
    body=['<line x1="96" y1="379" x2="927" y2="379" stroke="#64748b"/>',
          '<rect x="685" y="51" width="12" height="12" fill="#60a5fa"/>',
          '<text x="704" y="63">Actual student league</text>',
          '<rect x="855" y="51" width="12" height="12" fill="#fbbf24"/>',
          '<text x="874" y="63">Controlled trials</text>']
    for i,b in enumerate(BUCKETS):
        center=118+(i+.5)*775/3
        body.append(f'<text x="{center:.1f}" y="411" text-anchor="middle">'
                    f'{escape(NAMES[b])}</text>')
        for j,mode in enumerate(("league","trial")):
            item=rates[mode,b]
            risk=item["risk"]
            if risk is None:
                body.append(f'<text x="{center+(-40 if j==0 else 40):.1f}" y="350" '
                            'text-anchor="middle">n/a</text>')
                continue
            height=265*risk/high
            color="#60a5fa" if mode=="league" else "#fbbf24"
            x=center-43+j*46
            body.append(f'<rect x="{x:.1f}" y="{379-height:.1f}" width="43" '
                        f'height="{height:.1f}" rx="4" fill="{color}">'
                        f'<title>{mode}: {risk:.2f}% of {item["n"]} sampled windows '
                        f'led to a death event within 10 turns</title></rect>')
            body.append(f'<text x="{x+21:.1f}" y="{367-height:.1f}" '
                        f'text-anchor="middle" fill="{color}">{risk:.1f}%</text>')
    from .league_comparison import chart
    chart(path,title,body,455)

def cluster_interval(rows,mode,iterations=800,seed=2026):
    """Resample complete unique replay files, NOT correlated turn exposures."""
    games=defaultdict(lambda:{"near":[0,0],"far":[0,0]})
    for x in rows:
        if x["mode"]!=mode:
            continue
        b=x["head_pressure"]
        if b not in ("near_0_3","far_8_plus"):continue
        k="near" if b=="near_0_3" else "far"
        games[x["sha"]][k][0]+=int(x["death_next_10"])
        games[x["sha"]][k][1]+=1
    keys=list(games)
    if len(keys)<8:
        return None
    rng=random.Random(seed)
    diffs=[]
    for _ in range(iterations):
        a=b=c=d=0
        for key in rng.choices(keys,k=len(keys)):
            record=games[key]
            a+=record["near"][0];b+=record["near"][1]
            c+=record["far"][0];d+=record["far"][1]
        if b and d:
            diffs.append(100*(a/b-c/d))
    if len(diffs)<iterations//2:
        return None
    diffs.sort()
    return dict(low=round(diffs[int(.025*(len(diffs)-1))],2),
                high=round(diffs[int(.975*(len(diffs)-1))],2),
                draws=len(diffs),clusters=len(keys))

def build(data_dir,max_files=250):
    rows,qc=load(data_dir,max_files)
    rates=summarize(rows)
    indiv=per_student(rows)
    base=data_dir/"reports"
    charts=base/"charts"
    derived=data_dir/"derived"
    base.mkdir(parents=True,exist_ok=True)
    risk_plot(charts/"head_pressure_vs_death.svg",rates,
              "Recorded death within 10 turns vs nearest opponent head")
    stratified=defaultdict(Counter)
    by_exits=defaultdict(Counter)
    for r in rows:
        key=(r["mode"],r["length_bin"],r["head_pressure"])
        stratified[key]["n"]+=1
        stratified[key]["deaths"]+=r["death_next_10"]
        free="0-1 free sides" if r["neighbor_exits"]<=1 else "2-4 free sides"
        by_exits[(r["mode"],r["head_pressure"],free)]["n"]+=1
        by_exits[(r["mode"],r["head_pressure"],free)]["deaths"]+=r["death_next_10"]
    # CSV one unique replay / mode / student: cluster-aware audit.
    by_replay=defaultdict(list)
    for r in rows:
        by_replay[(r["sha"],r["mode"],r["season"],r["student"])].append(r)
    observations=[]
    for (sha,mode,season,student),items in sorted(by_replay.items()):
        observations.append(dict(sha=sha,mode=mode,season=season,
            student=student,replay=items[0]["replay"],windows=len(items),
            close=sum(x["head_pressure"]=="near_0_3" for x in items),
            confined=sum(x["neighbor_exits"]<=1 for x in items),
            future_death=sum(x["death_next_10"] for x in items)))
    write_csv(derived/"threat_window_replay_summary.csv",observations)
    write_csv(derived/"threat_window_student_seasons.csv",indiv)

    latest=max((r["season"] for r in rows),default=None)
    paired=defaultdict(dict)
    for entry in indiv:
        if entry["season"]==latest:
            paired[entry["student"]][entry["mode"]]=entry
    matched=[(name,groups["league"],groups["trial"]) for name,groups in paired.items()
             if "league" in groups and "trial" in groups]
    interval={mode:cluster_interval(rows,mode) for mode in ("league","trial")}
    lines=[
        "# Snake26: Head pressure, escape options, and subsequent deaths","",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
        "## Study design — actual replay frames, not a simulator","",
        "At every **25th turn**, for each living STUDENT, measure the toroidal",
        "Manhattan distance to the nearest **living opponent head** and number",
        "of immediately unoccupied neighboring cells (0–4, all current snake",
        "bodies and obstacles treated as blocked). Check whether that same snake",
        "has a recorded **death event in the NEXT 10 contiguous turns**.",
        "A sampled window can include a death but we do not infer causes or intent.",
        "The immediate-neighbor metric is a conservative **snapshot proxy**,",
        "NOT a legal-action count or guaranteed future escape: tails and heads move.",
        "Windows are spaced 25 turns apart to avoid overlapping 10-turn outcomes.",
        "They are STILL correlated within snake and replay match.",
        "",
        "## Coverage and quality first","",
        f"- Archived files scanned: **{qc['files_scanned']}** of {qc['files']} candidate files.",
        f"- Unique replay payloads: **{qc['unique_replays']}**",
        f"(league **{qc['league_unique_replays']}**, trials **{qc['trial_unique_replays']}**).",
        f"- Exact byte-identical duplicates skipped: **{qc['duplicate_replays']}**.",
        f"- Unreadable / invalid: **{qc['unreadable']}**.",
        f"- Single-student league games excluded: **{qc['excluded_single_student_league']}**.",
        f"- Nonstandard trial rosters excluded: **{qc['excluded_nonstandard_trial']}**.",
        f"- Student windows with complete follow-up: **{len(rows):,}**.",
        f"- Distinct student/replay summaries: **{len(observations)}**.",
        f"- Latest sampled season: **{latest or 'not available'}**.",
        f"- Latest sampled student-season with BOTH replay modes: **{len(matched)}**.",
        "",
        "## 1. Head pressure and observed future death","",
        "![Pressure and 10-turn death events](charts/head_pressure_vs_death.svg)","",
        "| Environment | Nearest opponent head | Windows | Death in next 10 turns | Observed frequency | Unique replays |",
        "|---|---|---:|---:|---:|---:|"
    ]
    for mode in ("league","trial"):
        for b in BUCKETS:
            r=rates[mode,b]
            lines.append(f"| {mode} | {NAMES[b]} | {r['n']:,} | {r['died']:,} | "
                         f"{f(r['risk'])}% | {r['matches']} |")
    lines+=["",
        "A close opponent head does NOT imply an aggressive attack or a collision.",
        "This is a selected replay sample. Risk differences are not causal effects",
        "and are not comparisons between equally skilled opponent populations.","",
        "## 2. Pressure vs distance alone: match-level uncertainty",""]
    for mode in ("league","trial"):
        n=rates[mode,"near_0_3"]["risk"]
        d=rates[mode,"far_8_plus"]["risk"]
        ci=interval[mode]
        if n is None or d is None:
            lines.append(f"- **{mode}:** insufficient near/far exposures.")
        elif ci:
            lines.append(f"- **{mode}:** close-minus-far risk = **{n-d:+.2f} percentage points**; "
                         f"exploratory 95% match-resampled interval **[{ci['low']:+.2f}, {ci['high']:+.2f}]**, "
                         f"{ci['clusters']} distinct replay clusters.")
        else:
            lines.append(f"- **{mode}:** close-minus-far frequency = **{n-d:+.2f} percentage points**; "
                         "too few replay clusters for this interval.")
    lines+=["",
        "Resampling entire REPLAYS reduces pseudo-replication from repeated turns.",
        "It does not adjust confounding from body length, opponent type, code",
        "versions, player ability or game phase.",
        "",
        "## 3. Compare danger within body-length categories","",
        "| Mode | Length | Head ≤3: death/windows | Head ≥8: death/windows | Close - far frequency |",
        "|---|---|---:|---:|---:|"]
    for mode in ("league","trial"):
        for cat in LENGTH_BINS:
            a=stratified[mode,cat,"near_0_3"]
            b=stratified[mode,cat,"far_8_plus"]
            ra=percentage(a["deaths"],a["n"])
            rb=percentage(b["deaths"],b["n"])
            lines.append(f"| {mode} | {cat} | {a['deaths']}/{a['n']} | {b['deaths']}/{b['n']} | "
                         f"{f(ra-rb) if ra is not None and rb is not None else 'n/a'} pp |")
    lines+=["",
        "## 4. Immediate escape space at the same head pressure","",
        "| Mode | Head proximity | Free neighboring cells | Death events/windows | Observed frequency |",
        "|---|---|---|---:|---:|"]
    for mode in ("league","trial"):
        for proximity in ("near_0_3","far_8_plus"):
            for sides in ("0-1 free sides","2-4 free sides"):
                obs=by_exits[mode,proximity,sides]
                lines.append(f"| {mode} | {NAMES[proximity]} | {sides} | "
                             f"{obs['deaths']}/{obs['n']} | {f(percentage(obs['deaths'],obs['n']))}% |")
    lines+=["",
        "This helps distinguish crowded **local geometry** from opponent-head",
        "pressure, but is still a snapshot association, not an actual 10-turn",
        "pathfinding or safety proof.",
        "",
        "## 5. Palmer and other known students — descriptive exposure only","",
        "| Student | Mode | Replay matches | Sampled windows | Head ≤3 share | 0–1 free-side share | Death in next 10-turn window |",
        "|---|---|---:|---:|---:|---:|---:|"]
    for team in TRACKED:
        for mode in ("league","trial"):
            arr=[r for r in indiv if r["student"]==team and r["mode"]==mode]
            denom=sum(x["sampled_windows"] for x in arr)
            if not denom:continue
            nr=sum(x["close_head_windows"] for x in arr)
            confined=sum(x["limited_exits_windows"] for x in arr)
            death=sum(x["death_within_10_windows"] for x in arr)
            replay_count=sum(x["replays"] for x in arr)
            lines.append(f"| {team} | {mode} | {replay_count} | {denom} | "
                         f"{100*nr/denom:.1f}% | {100*confined/denom:.1f}% | {death}/{denom} |")
    lines+=["",
        "These students have very different recorded sample sizes. Rows include",
        "multiple seasons and possibly changed bot submissions. Do NOT rank their",
        "intrinsic skill using these unadjusted exposure percentages.",
        "",
        "## 6. Same student and season: can head-pressure behavior transfer?","",
        f"Latest sampled paired-student cohort: **{len(matched)}**.",
        "At least four paired students with reliable coverage are needed even",
        "to explore a rank correlation; sample size, opponent type and replay",
        "selection must be shown before stronger conclusions.",
        "",
        "## Reproducible exports","",
        "- [Student-season mode-separated threat exposure](../derived/threat_window_student_seasons.csv)",
        "- [Per replay student exposure and outcome totals](../derived/threat_window_replay_summary.csv)",
        "",
        "**Next hypothesis:** a strong competitor preserves local exits BEFORE",
        "near-head encounters, rather than maximizing distance from everyone.",
        "This study cannot yet establish that policy. Validate across new league",
        "replays and matched controls before trying it in the Java agent.",""]
    target=base/"threat_windows.md"
    target.write_text("\n".join(lines),encoding="utf-8")
    return dict(replays=qc["unique_replays"],league_replays=qc["league_unique_replays"],
                trial_replays=qc["trial_unique_replays"],windows=len(rows),
                latest_paired=len(matched),intervals=interval,
                risks={mode:{b:rates[mode,b]["risk"] for b in BUCKETS}
                       for mode in ("league","trial")},
                report=str(target))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    p.add_argument("--max-files",type=int,default=250)
    args=p.parse_args()
    if args.max_files<0:
        p.error("max-files must be >=0")
    print(json.dumps(build(args.data_dir,args.max_files),indent=2))

if __name__=="__main__":
    main()
