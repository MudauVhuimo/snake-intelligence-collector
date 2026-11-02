"""Death autopsies versus matched observed escapes, from actual Wits replays.

The important outcome is NOT predicted/hypothetical: death events occur in
the NEXT ten real frames after a danger-state snapshot. Retrospectively match
cases to observed survivors on baseline features and report the genuine
first-step changes, with early deaths/selection made explicit.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from datetime import datetime,timezone
from html import escape
from pathlib import Path
from statistics import mean,median
import argparse
import csv
import json
import random

from .escape_autopsy_core import load_autopsies,match_cases,paired_deltas
from .league_comparison import chart

TRACKED=("421462-alexander-palmer","403754-vhuimo-mudau",
         "388060-tshepang-tshabalala","428786-marvellous-sambo",
         "409997-utayan-naidoo")
MEASURES=(("exits_gain","Change in local free neighbors"),
          ("head_gain","Change in nearest-head distance"),
          ("stable_food_progress","Progress toward same visible apple"))

def fmt(value,digits=2):
    return "n/a" if value is None else f"{value:+.{digits}f}"

def write_csv(path,records,columns):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=columns,extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

def summarized_matches(matches):
    results=Counter()
    for pair in matches:
        mode=pair["case"]["mode"]
        results[mode+"_pairs"]+=1
        if pair["same_replay"]:results[mode+"_same_replay"]+=1
        if pair["same_student"]:results[mode+"_same_student"]+=1
        if pair["level"]=="phase_relaxed":results[mode+"_phase_relaxed"]+=1
    return results

def bootstrap_difference(differences,draws=1000,seed=2026):
    """Resample complete *death-case replay* clusters, not independent turns.

    The controls are chosen without replacement. Cross-replay controls still
    couple some clusters, and CIs do NOT correct for winner/strategy selection.
    """
    by_sha=defaultdict(list)
    for row in differences:
        by_sha[row["case_sha"]].append(row["control_minus_case"])
    keys=sorted(by_sha)
    if len(keys)<8:
        return None
    rng=random.Random(seed)
    samples=[]
    for _ in range(draws):
        values=[]
        for key in rng.choices(keys,k=len(keys)):
            values.extend(by_sha[key])
        if values:
            samples.append(mean(values))
    samples.sort()
    return dict(low=samples[int(.025*(len(samples)-1))],
                high=samples[int(.975*(len(samples)-1))],
                clusters=len(keys),draws=draws)

def extract_rows(matches):
    columns=("mode","case_student","control_student","case_replay",
             "control_replay","case_sha","control_sha","case_turn",
             "control_turn","match_quality","same_match","same_student",
             "baseline_length_case","baseline_length_control","length_band",
             "baseline_nearest_case","baseline_nearest_control",
             "baseline_exits_case","baseline_exits_control",
             "head_pressure","death_turn","death_cause",
             "case_observed_1","control_observed_1",
             "case_exits_gain_1","control_exits_gain_1",
             "case_head_gain_1","control_head_gain_1",
             "case_food_progress_1","control_food_progress_1",
             "case_observed_3","control_observed_3",
             "case_exits_gain_3","control_exits_gain_3",
             "case_head_gain_3","control_head_gain_3",
             "control_death_next_10")
    rows=[]
    for pair in matches:
        a,b=pair["case"],pair["control"]
        d=dict(mode=a["mode"],case_student=a["student"],
            control_student=b["student"],case_replay=a["replay"],
            control_replay=b["replay"],case_sha=a["sha"],control_sha=b["sha"],
            case_turn=a["start_turn"],control_turn=b["start_turn"],
            match_quality=pair["level"],same_match=pair["same_replay"],
            same_student=pair["same_student"],baseline_length_case=a["length"],
            baseline_length_control=b["length"],length_band=a["length_bin"],
            baseline_nearest_case=a["nearest_head"],
            baseline_nearest_control=b["nearest_head"],
            baseline_exits_case=a["neighbor_exits"],
            baseline_exits_control=b["neighbor_exits"],
            head_pressure=a["head_pressure"],
            death_turn=a["death_turn"],death_cause=a["death_cause"],
            control_death_next_10=b["death_next_10"])
        for step in (1,3):
            aa=a["trajectory"].get(step)
            bb=b["trajectory"].get(step)
            d["case_observed_"+str(step)]=bool(aa)
            d["control_observed_"+str(step)]=bool(bb)
            for dest,src in (("exits_gain","exits_gain"),
                             ("head_gain","head_gain")):
                d[f"case_{dest}_{step}"]=aa[src] if aa else None
                d[f"control_{dest}_{step}"]=bb[src] if bb else None
        aa=a["trajectory"].get(1)
        bb=b["trajectory"].get(1)
        d["case_food_progress_1"]=aa.get("stable_food_progress") if aa else None
        d["control_food_progress_1"]=bb.get("stable_food_progress") if bb else None
        rows.append(d)
    return rows,columns

def comparison_plot(path,pairs):
    """Plot actual observed first-turn changes, not policy recommendations."""
    mode_values={}
    for mode in ("league","trial"):
        for feature,title in MEASURES[:2]:
            data=paired_deltas(pairs,mode,1,feature)
            mode_values[mode,feature]=dict(
                cases=mean(x["case_value"] for x in data) if data else None,
                controls=mean(x["control_value"] for x in data) if data else None,
                n=len(data))
    maxabs=max([abs(x) for d in mode_values.values()
                for x in (d["cases"],d["controls"]) if x is not None]+[.1])
    high=max(1,maxabs*1.2)
    origin=535
    scale=230/high
    body=['<line x1="535" y1="83" x2="535" y2="350" stroke="#94a3b8"/>',
          '<rect x="766" y="54" width="12" height="12" fill="#60a5fa"/>',
          '<text x="783" y="65">Death cases (if still alive)</text>',
          '<rect x="766" y="72" width="12" height="12" fill="#34d399"/>',
          '<text x="783" y="83">Matched 10-turn survivors</text>']
    titles={
        "exits_gain":"Free adjacent cells at next turn − starting count",
        "head_gain":"Nearest head distance at next turn − starting distance"}
    for i,(mode,measure) in enumerate(
         (("league","exits_gain"),("league","head_gain"),
          ("trial","exits_gain"),("trial","head_gain"))):
        y=110+i*69
        data=mode_values[mode,measure]
        body.append(f'<text x="22" y="{y+9}">{escape(mode.title())}: '
                    f'{escape(measure.replace("_"," "))} (n={data["n"]})</text>')
        for j,(kind,col) in enumerate((("cases","#60a5fa"),("controls","#34d399"))):
            value=data[kind]
            if value is None:
                continue
            width=abs(value)*scale
            x=origin if value>=0 else origin-width
            yy=y-5+j*23
            body.append(f'<rect x="{x:.1f}" y="{yy}" width="{width:.1f}" '
                        f'height="18" rx="2" fill="{col}"/>')
            tx=origin+value*scale+(8 if value>=0 else -8)
            side="start" if value>=0 else "end"
            body.append(f'<text x="{tx:.1f}" y="{yy+13}" text-anchor="{side}">'
                        f'{value:+.2f}</text>')
    body+=['<text x="535" y="410" text-anchor="middle">'
           'Baseline-matched comparisons; first-turn alive/observed pairs ONLY</text>',
           '<text x="535" y="432" text-anchor="middle">'
           'Missing first turns after death are NOT scored as zero movement</text>']
    chart(path,"First-turn movements: death cases vs matched observed escapes",body,460)

def sample_trajectory_svg(path,matches):
    """An actual pair's recorded dynamics; zero invented moves."""
    pairs=[m for m in matches if m["case"]["mode"]=="league"
           and m["case"]["trajectory"].get(1)
           and m["control"]["trajectory"].get(1)]
    if not pairs:
        return chart(path,"Recorded death vs escape","<text x='40' y='100'>No qualifying paired trace</text>",200)
    pairs.sort(key=lambda p:(
        not p["same_replay"],
        not bool(p["case"]["trajectory"].get(3)),
        abs(p["case"]["neighbor_exits"]-p["control"]["neighbor_exits"]),
        p["case"]["sha"],p["case"]["start_turn"]))
    pair=pairs[0]
    content=[
        '<text x="30" y="73">Exact observed snapshot at step 0 and subsequent surviving steps</text>',
        '<rect x="30" y="99" width="12" height="12" fill="#60a5fa"/>',
        '<text x="48" y="110">Death case</text>',
        '<rect x="185" y="99" width="12" height="12" fill="#34d399"/>',
        '<text x="204" y="110">Survival control</text>'
    ]
    fields=(("neighbor_exits","Free neighboring cells",0,4,155),
            ("nearest_head","Nearest opponent head distance",0,30,335))
    for key,title,minimum,maximum,y in fields:
        content.append(f'<text x="35" y="{y-18}">{escape(title)}</text>')
        left,right=y+120,y+120  # labeled below, no invisible geometry
        for value in (0,1,3,10):
            xx=190+(value/10)*700
            content.append(f'<text x="{xx:.1f}" y="{y+118}" text-anchor="middle">'
                           f'{value}</text>')
        for item,color,side in ((pair["case"],"#60a5fa","death"),
                                (pair["control"],"#34d399","escape")):
            vals=[(0,item[key])]
            vals.extend((t,detail[key]) for t in (1,3,10)
                        if (detail:=item["trajectory"].get(t)) is not None)
            for (t1,a),(t2,b) in zip(vals,vals[1:]):
                # 30-turn state is not drawn on a ten-turn axis.
                xx=190+(t1/10)*700
                yy=y+90-(a-minimum)/(maximum-minimum)*85
                x2=190+(t2/10)*700
                y2=y+90-(b-minimum)/(maximum-minimum)*85
                content.append(f'<line x1="{xx:.1f}" y1="{yy:.1f}" '
                               f'x2="{x2:.1f}" y2="{y2:.1f}" '
                               f'stroke="{color}" stroke-width="3"/>')
            for t,value in vals:
                xx=190+(t/10)*700
                yy=y+90-(value-minimum)/(maximum-minimum)*85
                content.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" '
                               f'r="4.3" fill="{color}"/>')
            if side=="death":
                content.append(f'<text x="190" y="{y+138}" fill="{color}">'
                               f'Case death at +{item["death_turn"]-item["start_turn"]} turns</text>')
    content += [
        '<text x="35" y="523">Observed pair: death case '+escape(pair["case"]["student"])+
        ' vs '+escape(pair["control"]["student"])+'</text>',
        '<text x="35" y="545">Same real replay: '+str(pair["same_replay"]).lower()+
        '; selected matched baseline, NOT a counterfactual action comparison.</text>'
    ]
    chart(path,"One genuine danger-state death and escape trace",content,580)

def build(data_dir,max_files=250):
    data_dir=Path(data_dir)
    observations,quality=load_autopsies(data_dir,max_files)
    matches,unmatched=match_cases(observations)
    match_stats=summarized_matches(matches)
    reports=data_dir/"reports"
    figures=reports/"charts"
    figures.mkdir(parents=True,exist_ok=True)
    comparison_plot(figures/"escape_case_control.svg",matches)
    sample_trajectory_svg(figures/"escape_example_trace.svg",matches)
    csv_rows,cols=extract_rows(matches)
    write_csv(data_dir/"derived"/"escape_matched_pairs.csv",csv_rows,cols)
    cases=Counter(row["mode"] for row in observations if row["outcome"]=="death")
    survivors=Counter(row["mode"] for row in observations if row["outcome"]=="escape_10")
    table=[]
    confidence={}
    for mode in ("league","trial"):
        for step,measure in ((1,"exits_gain"),(1,"head_gain"),
                             (1,"stable_food_progress"),(3,"exits_gain"),
                             (3,"head_gain")):
            pairs=paired_deltas(matches,mode,step,measure)
            interval=bootstrap_difference(pairs)
            record=dict(mode=mode,step=step,measure=measure,n=len(pairs),
                cases=mean(x["case_value"] for x in pairs) if pairs else None,
                controls=mean(x["control_value"] for x in pairs) if pairs else None,
                difference=mean(x["control_minus_case"] for x in pairs) if pairs else None,
                bootstrap=interval)
            table.append(record)
            confidence[mode,step,measure]=record
    lines=[
        "# Snake26: Death autopsies versus successful real escapes","",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
        "## Research question","",
        "Among student snakes starting in *similarly dangerous real positions*,",
        "what did snakes that survived the NEXT ten turns visibly do, compared",
        "with snakes that actually died? This is a RETROSPECTIVE case–control",
        "observation, not a randomized experiment or a policy recommendation.","",
        "## Methods and data quality","",
        "1. Sample each living student every 25 turns in unique full replay files.",
        "   Include positions with an opponent head within three toroidal cells,",
        "   or zero/one currently unoccupied neighboring cells.",
        "2. Require ten contiguous future frames. A 'death' case must have",
        "   a genuine **died** event in turns +1 to +10. A control has no died",
        "   event in those ten turns. Mere 'survived at turn 2,000' is insufficient.",
        "3. Match cases to controls **within the SAME match mode**, body-length",
        "   band, baseline head-pressure band, and limited-exits band. Also match",
        "   500-turn game phase where available; if not, the phase is relaxed",
        "   and disclosed. Prefer an actual control from the SAME replay.",
        "4. Compare actual free-neighbor changes, head-distance changes and",
        "   pursuit of the SAME still-visible apple after turns +1 and +3.",
        "   If a snake dies before an observation, that step is **missing**—",
        "   NEVER zero, and NEVER a hypothetical move.",
        "5. Separately resample full case-replay clusters for exploratory CIs.",
        "   Multiple cases from the same game remain dependent; cross-replay",
        "   control matching creates further dependency.",
        "",
        f"Files scanned: **{quality['scanned']}** of {quality['files']}.",
        f"Unique replay payloads: **{quality['unique_replays']}**",
        f"(league {quality['league_unique_replays']}, trial {quality['trial_unique_replays']}).",
        f"Duplicate replays skipped: **{quality['duplicate_replays']}**.",
        f"Unreadable: **{quality['invalid']}**.",
        f"Valid dangerous baseline positions: **{len(observations):,}**.",
        "",
        "## 1. Baseline-matched death cases and observed survivor controls","",
        "| Match mode | Death cases | Survivor control candidates | Matched pairs | Same replay | Phase relaxed | Unmatched deaths |",
        "|---|---:|---:|---:|---:|---:|---:|"]
    for mode in ("league","trial"):
        lines.append(f"| {mode} | {cases[mode]} | {survivors[mode]} | "
                     f"{match_stats[mode+'_pairs']} | {match_stats[mode+'_same_replay']} | "
                     f"{match_stats[mode+'_phase_relaxed']} | {unmatched[mode]} |")
    lines += ["",
        "Matching minimizes observable baseline differences. It does NOT balance",
        "unobserved bot policy, opponent skill, map future, or specific matchup.",
        "Some controls come from other real games; report same-match counts.",
        "",
        "## 2. First observed escape movements (post-baseline)","",
        "![First-turn case-control movement comparison](charts/escape_case_control.svg)","",
        "| Mode | Step | Real measured change | Alive and measured matched pairs | Death cases mean | Survivor controls mean | Survivor − case | Exploratory match-bootstrap interval |",
        "|---|---:|---|---:|---:|---:|---:|---|"]
    for r in table:
        interval=r["bootstrap"]
        ci=(f"[{fmt(interval['low'])}, {fmt(interval['high'])}], "
            f"{interval['clusters']} case-replay clusters" if interval else
            "insufficient distinct case-replay clusters")
        lines.append(f"| {r['mode']} | +{r['step']} | {r['measure']} | {r['n']} | "
                     f"{fmt(r['cases'])} | {fmt(r['controls'])} | "
                     f"{fmt(r['difference'])} | {ci} |")
    lines+=["",
        "## 2a. Sensitivity checks: what if comparisons are stricter?","",
        "| League comparison subset | Baseline matched pairs | Both alive/observed at +1 | Mean +1 free-exit gain difference (survivor − case) |",
        "|---|---:|---:|---:|"]
    league_pairs=[p for p in matches if p["case"]["mode"]=="league"]
    subsets=[
        ("All baseline-matched league pairs",league_pairs),
        ("Same replay ONLY",[p for p in league_pairs if p["same_replay"]]),
        ("Same 500-turn phase",[p for p in league_pairs if p["level"]=="exact"]),
        ("Exact starting free-exit count",[p for p in league_pairs
             if p["case"]["neighbor_exits"]==p["control"]["neighbor_exits"]]),
        ("Exact free exits AND head distance",[p for p in league_pairs
             if p["case"]["neighbor_exits"]==p["control"]["neighbor_exits"]
             and p["case"]["nearest_head"]==p["control"]["nearest_head"]]),
        ("Opponent head <=3 cells",[p for p in league_pairs
             if p["case"]["nearest_head"]<=3]),
        ("At most one free neighboring cell",[p for p in league_pairs
             if p["case"]["neighbor_exits"]<=1]),
    ]
    for title,subset in subsets:
        d=paired_deltas(subset,"league",1,"exits_gain")
        delta=mean(x["control_minus_case"] for x in d) if d else None
        lines.append(f"| {title} | {len(subset)} | {len(d)} | {fmt(delta)} |")
    lines+=["",
        "These are nested exploratory subsets, NOT independent confirmations.",
        "If a strict subset has few pairs, its mean is especially unstable.",
        "The original matching is retrospective. A shared 500-turn phase is",
        "not proof of identical maps, opponents or goals.",
        "",
        "## 2b. Check baseline balance rather than assuming matching is perfect","",
        "| League baseline comparison | Death case average | Survivor control average |",
        "|---|---:|---:|"]
    for key,label in (("neighbor_exits","Free adjacent cells"),
                      ("nearest_head","Opponent head distance"),
                      ("length","Body length"),
                      ("start_turn","Game turn")):
        a=mean(p["case"][key] for p in league_pairs) if league_pairs else None
        b=mean(p["control"][key] for p in league_pairs) if league_pairs else None
        lines.append(f"| {label} | {fmt(a)} | {fmt(b)} |")
    lines+=["",
        "Our matching enforces body LENGTH BAND, head PRESSURE BAND and",
        "limited-exit BAND, but individual numerical values can still differ.",
        "Baseline imbalance is a remaining confounding source.",""]

    lines+=["",
        "The +1 and +3 means include only pairs for which BOTH actual states",
        "were observable and the death case was still alive at that step.",
        "Therefore later steps suffer **survivorship selection**: do not",
        "interpret differences as prevention effects.",
        "",
        "## 3. An actual case and an actual matched escape","",
        "![Observed death versus escape trajectory](charts/escape_example_trace.svg)","",
        "The chosen example shares baseline danger descriptors and prefers the",
        "same replay. It does **not** imply the snakes had interchangeable legal",
        "moves, objectives, or opponent reactions.",
        "",
        "## 4. What we can safely conclude","",
        "This analysis can show early movement patterns associated with survival",
        "after danger, as well as how often each pattern is actually observable.",
        "It CANNOT prove that a specific move saved a snake, that another move",
        "would have killed a competitor, or that Palmer's policy was reproduced.",
        "We must control for opponent skill, starting length, body geometry,",
        "head positions, food availability and season/version before building",
        "a new movement rule. The strongest future evidence will come from",
        "repeated paired observations and controlled held-out Java experiments.",
        "",
        "## Reproducible data","",
        "- [Baseline-matched dead/survivor observations](../derived/escape_matched_pairs.csv).",
        "- [Mode-separated head-pressure risk](threat_windows.md).",
        "- [Canonical joined student league/trial research](joint_analysis.md).",
        "",
        "**No competition snake was modified.**",""]
    report=reports/"escape_autopsies.md"
    report.write_text("\n".join(lines),encoding="utf-8")
    return dict(replays=quality["unique_replays"],
                league_deaths=cases["league"],trial_deaths=cases["trial"],
                matched_league=match_stats["league_pairs"],
                matched_trial=match_stats["trial_pairs"],
                same_replay_league=match_stats["league_same_replay"],
                same_replay_trial=match_stats["trial_same_replay"],
                measures=[{k:v for k,v in x.items() if k!="bootstrap"}
                          for x in table],
                report=str(report))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    p.add_argument("--max-files",type=int,default=250)
    args=p.parse_args()
    print(json.dumps(build(Path(args.data_dir),args.max_files),indent=2))

if __name__=="__main__":
    main()
