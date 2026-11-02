"""Full-field Snake26 opponent next-head cones: actual league and trials separately.

All per-move model scores come from the current state. Next-frame positions
are used ONLY for retrospective move validation or outcome labels.
"""
from __future__ import annotations
from collections import defaultdict
from datetime import datetime,timezone
from pathlib import Path
from statistics import mean
import argparse,csv,json,math,random

from .league_comparison import chart
from .route_space import auc,holdout,pair_source_decisions,pair_contrast

COHORTS=("top_quartile","middle_half","bottom_quartile","unranked")
LENGTH_BANDS=("5-24","25-49","50-99","100+")
FEATURES=(
    ("free_exits","Current free neighboring cells"),
    ("best_tail","Best 8-step moving-own-tail reach"),
    ("uncontested_count","Modeled first steps outside all opponent cones"),
    ("best_uncontested_tail","Best tail reach outside all head cones"),
    ("nonweaker_free_count","First steps avoiding equal/longer head cones"),
    ("best_nonweaker_free_tail","Best tail reach outside equal/longer head cones"),
)

def parse_bool(s):
    if s is True or s in ("True","true","1"):return True
    if s is False or s in ("False","false","0"):return False
    return None

def read_rows(data_dir):
    source=Path(data_dir)/"derived"/"route_choice_windows.csv"
    if not source.exists():return []
    with source.open(newline="",encoding="utf-8") as stream:
        rows=list(csv.DictReader(stream))
    for r in rows:
        for name in ("turn","length","free_exits","candidate_count",
                     "opponent_heads","threatened_count","nonweaker_threatened_count",
                     "uncontested_count","nonweaker_free_count",
                     "best_tail","best_uncontested_tail","best_nonweaker_free_tail"):
            v=r.get(name)
            r[name]=int(v) if v not in ("",None) else None
        for name in ("all_cone","all_nonweaker_cone",
                     "chosen_cone","chosen_nonweaker_cone","chosen_longer_cone"):
            r[name]=parse_bool(r.get(name))
    return rows

def percent(n,d):
    return 100*n/d if d else None

def fmt(x,digits=3):
    return "insufficient" if x is None else f"{x:.{digits}f}"

def counts(rows):
    choices=[r for r in rows if r["chosen_cone"] is not None]
    candidates=[r for r in rows if r["candidate_count"]]
    known=[r for r in rows if r["death10"] in ("alive","dead")]
    n= len(candidates)
    k= len(choices)
    return dict(
        windows=len(rows),games=len({r["replay_sha"] for r in rows}),
        students=len({r["student"] for r in rows}),
        candidate_frames=n,observed_moves=k,
        any_cone=sum(r["threatened_count"]>0 for r in candidates),
        all_cone=sum(r["all_cone"] is True for r in candidates),
        chosen_cone=sum(r["chosen_cone"] is True for r in choices),
        chosen_nonweaker=sum(r["chosen_nonweaker_cone"] is True for r in choices),
        first_step_h2h=sum(r["first_step_death_cause"]=="head_to_head" for r in rows),
        death10=sum(r["death10"]=="dead" for r in known),known10=len(known),
        pct_any=percent(sum(r["threatened_count"]>0 for r in candidates),n),
        pct_all=percent(sum(r["all_cone"] is True for r in candidates),n),
        pct_chosen=percent(sum(r["chosen_cone"] is True for r in choices),k),
        pct_nonweaker=percent(
            sum(r["chosen_nonweaker_cone"] is True for r in choices),k))

def risk_auc(rows,feature):
    records=[dict(risk=-r[feature],death10=r["death10"])
             for r in rows if r[feature] is not None]
    return auc(records,"risk")

def bootstrap_auc(rows,left,right,draws=700,seed=2026):
    """Whole-replay resampling on identical held-out observations."""
    bygame=defaultdict(list)
    for r in rows:bygame[r["replay_sha"]].append(r)
    games=sorted(bygame)
    a,b=risk_auc(rows,left),risk_auc(rows,right)
    result=dict(games=len(games),low=None,high=None,draws=0,
                difference=a-b if a is not None and b is not None else None)
    if len(games)<8:return result
    rng=random.Random(seed)
    vals=[]
    for _ in range(draws):
        part=[r for sha in rng.choices(games,k=len(games)) for r in bygame[sha]]
        a,b=risk_auc(part,left),risk_auc(part,right)
        if a is not None and b is not None:vals.append(a-b)
    vals.sort()
    if len(vals)>=draws//2:
        result.update(low=vals[int(.025*(len(vals)-1))],
                      high=vals[int(.975*(len(vals)-1))],
                      draws=len(vals))
    return result

def tied_ranks(values):
    indexed=sorted(range(len(values)),key=lambda i:values[i])
    result=[0.0]*len(values)
    start=0
    while start<len(indexed):
        stop=start+1
        while stop<len(indexed) and values[indexed[stop]]==values[indexed[start]]:
            stop+=1
        for i in indexed[start:stop]:result[i]=(start+1+stop)/2
        start=stop
    return result

def spearman(pairs):
    if len(pairs)<4:return None
    a,b=zip(*pairs)
    a,b=tied_ranks(a),tied_ranks(b)
    ma,mb=mean(a),mean(b)
    numerator=sum((x-ma)*(y-mb) for x,y in zip(a,b))
    da=sum((x-ma)**2 for x in a)
    db=sum((y-mb)**2 for y in b)
    return numerator/math.sqrt(da*db) if da and db else None

def paired_student_modes(rows,min_choices=3):
    groups=defaultdict(list)
    for r in rows:
        if r["chosen_cone"] is not None:
            groups[r["season"],r["student"],r["mode"]].append(r)
    pairs=[]
    for season,student in sorted({(s,n) for s,n,m in groups}):
        league=groups.get((season,student,"league"),[])
        trial=groups.get((season,student,"trial"),[])
        if min(len(league),len(trial))<min_choices:continue
        pairs.append(dict(season=season,student=student,
            league_choices=len(league),trial_choices=len(trial),
            league_contested=mean(r["chosen_cone"] for r in league),
            trial_contested=mean(r["chosen_cone"] for r in trial),
            league_nonweaker=mean(r["chosen_nonweaker_cone"] for r in league),
            trial_nonweaker=mean(r["chosen_nonweaker_cone"] for r in trial)))
    rho=spearman([(x["league_contested"],x["trial_contested"]) for x in pairs])
    return pairs,rho

def write_csv(path,rows,columns):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

def plot(path,summary):
    groups={(r["mode"],r["cohort"]):r for r in summary}
    body=[
        '<line x1="105" y1="367" x2="918" y2="367" stroke="#64748b"/>',
        '<text x="106" y="82">Actual first moves into a possible opponent-head cell</text>',
        '<text x="106" y="101">Only next-frame survivors; NOT a measured risk of death</text>']
    for i,c in enumerate(COHORTS[:3]):
        centre=240+i*273
        body.append(f'<text x="{centre}" y="407" text-anchor="middle">'
                    f'{("Top 25%","Middle 50%","Bottom 25%")[i]}</text>')
        for j,(mode,color) in enumerate((("league","#60a5fa"),("trial","#fbbf24"))):
            val=groups[mode,c]["pct_chosen"]
            x=centre-57+j*69
            if val is None:
                body.append(f'<text x="{x+26}" y="350">n/a</text>')
                continue
            h=val*2.5
            body.append(f'<rect x="{x}" y="{367-h:.1f}" height="{h:.1f}" '
                        f'width="52" rx="4" fill="{color}"/>')
            body.append(f'<text x="{x+26}" y="{353-h:.1f}" text-anchor="middle">'
                        f'{val:.1f}%</text>')
    body.extend(['<rect x="748" y="53" width="13" height="13" fill="#60a5fa"/>',
                 '<text x="766" y="65">League</text>',
                 '<rect x="848" y="53" width="13" height="13" fill="#fbbf24"/>',
                 '<text x="866" y="65">Trials</text>'])
    chart(path,"Opponent reach-cone exposure in observed student moves",body,447)

def build(data_dir):
    data_dir=Path(data_dir)
    rows=read_rows(data_dir)
    source=data_dir/"derived"/"route_cone_quality.json"
    qc=json.loads(source.read_text(encoding="utf-8")) if source.exists() else {}
    groups=[dict(mode=m,cohort=c,**counts([r for r in rows
                   if r["mode"]==m and r["cohort"]==c]))
            for m in ("league","trial") for c in COHORTS]
    league=[r for r in rows if r["mode"]=="league"]
    trial=[r for r in rows if r["mode"]=="trial"]
    samples={m:holdout(rows) for m,rows in (("league",league),("trial",trial))}
    aucs={m:{key:risk_auc(samples[m],key) for key,label in FEATURES}
          for m in ("league","trial")}
    contrasts={name:bootstrap_auc(samples["league"],left,right)
               for name,left,right in (
                   ("uncontested_minus_tail","best_uncontested_tail","best_tail"),
                   ("nonweaker_minus_tail","best_nonweaker_free_tail","best_tail"),
                   ("uncontested_minus_neighbors","best_uncontested_tail","free_exits"))}
    pairs=pair_source_decisions(data_dir,rows)
    paired={key:pair_contrast(pairs,key) for key in (
        "chosen_cone","chosen_nonweaker_cone","all_cone")}
    same_students,rho=paired_student_modes(rows)
    write_csv(data_dir/"derived"/"opponent_cone_cohorts.csv",groups,
              list(groups[0]) if groups else ["mode","cohort","windows"])
    write_csv(data_dir/"derived"/"opponent_cone_paired_students.csv",
              same_students,list(same_students[0]) if same_students else
              ["season","student","league_choices","trial_choices",
               "league_contested","trial_contested",
               "league_nonweaker","trial_nonweaker"])
    chart_path=data_dir/"reports"/"charts"/"opponent_contests.svg"
    chart_path.parent.mkdir(parents=True,exist_ok=True)
    plot(chart_path,groups)
    lines=[
        "# Snake26: Opponent next-head reachability across league and trials","",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
        "## What was tested","",
        "For every actual dangerous student position, derive all opponent",
        "one-step head destinations from current head and neck on the",
        "toroidal board. With a known heading, exclude immediate reversal;",
        "otherwise include all four cardinal neighbors. No occupancy filter",
        "is applied to opponents, so these sets are geometric UPPER BOUNDS,",
        "not legal moves, probabilistic predictions or certain deaths.",
        "Equal/longer CURRENT opponent length is a separate descriptive flag.",
        "We have not imported collision rules from earlier Wits Snake games.",
        "",
        "League is the competitive target. Trial benchmark observations are",
        "shown in separate rows. Rankings come from the corresponding",
        "official student league season; all students are included.",
        "New candidates are NOT built or modified by this investigation.",
        "",
        "## 1. Transition verification and actual head-on death records","",
        f"Source replay payloads: **{qc.get('unique_replays',0)}**.",
        f"Danger positions: **{len(rows)}**, league **{len(league)}**, "
        f"trials **{len(trial)}**.",
        f"Unique opponent normal next-head transitions checked: "
        f"**{qc.get('opponent_next_checked',0)}**.",
        f"Within predicted cone: **{qc.get('opponent_next_within_cone',0)}**; "
        f"outside: **{qc.get('opponent_next_outside_cone',0)}**.",
        f"Dead/absent/respawned opponents excluded, not marked predicted: "
        f"**{qc.get('opponent_dead',0)+qc.get('opponent_absent',0)}**.",
        f"League recorded head-to-head VICTIM events (all replay turns): "
        f"**{qc.get('league_h2h_victim_events',0)}**; trials "
        f"**{qc.get('trial_h2h_victim_events',0)}**.",
        "Victim events are not distinct collisions, and may lack an",
        "identifiable opposing player. Compare last-frame lengths only:",
        "",
        "| Last-known victim length relative to named peer | Events |",
        "|---|---:|"]
    for key in ("victim_shorter","equal","victim_longer",
                "missing_participant","missing_prior_frame"):
        lines.append(f"| {key} | {qc.get('head_on_'+key,0)} |")
    lines+=["",
        "Do NOT infer official 2026 head-on resolution solely from these",
        "events; cause attribution, concurrent deaths, growth and missing",
        "peer IDs can complicate interpretation.",
        "",
        "## 2. How do strong, average and struggling snakes encounter cones?","",
        "![Observed student first moves into possible opponent head cells](charts/opponent_contests.svg)","",
        "| Mode | League performance group | Students | Games | Danger windows | Frames with ≥1 contested alternative | ALL alternatives contested | Observed first moves | Observed move into cone | Into equal/longer cone | Death by +10 |",
        "|---|---|---:|---:|---:|---|---|---:|---|---|---|"]
    for r in groups:
        lines.append(f"| {r['mode']} | {r['cohort']} | {r['students']} | "
                     f"{r['games']} | {r['windows']} | "
                     f"{r['any_cone']}/{r['candidate_frames']} "
                     f"({fmt(r['pct_any'],1)}%) | "
                     f"{r['all_cone']}/{r['candidate_frames']} "
                     f"({fmt(r['pct_all'],1)}%) | {r['observed_moves']} | "
                     f"{r['chosen_cone']}/{r['observed_moves']} "
                     f"({fmt(r['pct_chosen'],1)}%) | "
                     f"{r['chosen_nonweaker']}/{r['observed_moves']} "
                     f"({fmt(r['pct_nonweaker'],1)}%) | "
                     f"{r['death10']}/{r['known10']} |")
    lines+=["",
        "SELECTION WARNING: observed first moves require a live head at t+1.",
        "Snakes killed on their first step have NO recorded destination;",
        "observed contested-move shares thus CANNOT estimate how dangerous",
        "contested choices are. Pre-action cone exposure includes those deaths.",
        "",
        "## 3. Predictive value on held-out actual league games","",
        "For each PRE-action feature, higher values mean more modeled safe",
        "options and are negated to rank actual recorded death within 10 turns.",
        "Use the SAME SHA-based entire-replay holdout as our route-space study.",
        "ROC AUC = 0.5 chance ranking; 1.0 perfect separation. AUC is not",
        "a calibrated risk or evidence of a better agent.",
        "",
        "| Match mode | Pre-action feature | Holdout windows | Death events | AUC |",
        "|---|---|---:|---:|---:|"]
    for mode in ("league","trial"):
        for key,label in FEATURES:
            part=samples[mode]
            lines.append(f"| {mode} | {label} | {len(part)} | "
                         f"{sum(r['death10']=='dead' for r in part)} | "
                         f"{fmt(aucs[mode][key])} |")
    lines+=["",
        "### Match-cluster uncertainty for league predictor differences","",
        "Bootstrap complete REPLAYS, never independently resample hundreds",
        "of overlapping turns. These exploratory intervals also inherit",
        "possible bot-version/season dependence and selection from the",
        "previous research archive. If an interval spans 0, no superiority",
        "is established.",
        "",
        "| Same held-out league observations | AUC difference | Exploratory 95% replay interval | Matches |",
        "|---|---:|---|---:|"]
    for key,label in (
        ("uncontested_minus_tail","Avoid any possible head vs plain tail reach"),
        ("nonweaker_minus_tail","Avoid equal/longer heads vs plain tail reach"),
        ("uncontested_minus_neighbors","Avoid any possible head vs free neighbors")
    ):
        v=contrasts[key]
        ci=(f"[{v['low']:+.3f}, {v['high']:+.3f}]"
            if v["low"] is not None else "insufficient event/game support")
        lines.append(f"| {label} | {fmt(v['difference'])} | {ci} | {v['games']} |")
    lines+=["",
        "## 4. Same-game comparisons, NOT selected opponent anecdotes","",
        "Compare previous non-reused top-vs-bottom student pairs from the",
        "SAME league replay and matched baseline length/pressure/phase.",
        f"Paired game situations with opponent cone data: **{len(pairs)}**.",
        "Differences below are bottom minus top. Matched situations can",
        "still have different food, opponents or exact positions.",
        "",
        "| State/observed behavior | Both measurable pairs | Games | Bottom minus top | 95% game interval |",
        "|---|---:|---:|---:|---|"]
    for key,label in (
        ("chosen_cone","Surviving first move entered possible head contest"),
        ("chosen_nonweaker_cone","Surviving move entered equal/longer head cone"),
        ("all_cone","ALL projected next cells possibly head-contested")
    ):
        v=paired[key]
        ci=(f"[{v['low']:+.3f}, {v['high']:+.3f}]"
            if v["low"] is not None else "insufficient clusters")
        lines.append(f"| {label} | {v['pairs']} | {v['matches']} | "
                     f"{fmt(v['difference'])} | {ci} |")
    lines+=["",
        "## 5. Same student/season: do league and trial styles agree?","",
        "Join by student AND season, only when each environment has at",
        "least THREE real observed first moves from that student.",
        f"Paired student-season samples: **{len(same_students)}**.",
        f"Spearman correlation of observed head-contest rates: "
        f"**{fmt(rho)}** (n/a if insufficient/constant).",
        "With so few and sometimes repeated submitted versions, this is",
        "not evidence of causal cross-environment transfer.",
        "[Underlying paired-student rows](../derived/opponent_cone_paired_students.csv).",
        "",
        "## 6. Hypothesis for the NEW algorithm, awaiting falsification","",
        "A route may be spacious yet exposed to several possible opponent",
        "next-head locations. A candidate future policy could trade off",
        "accessible area against prospective head conflicts, but no",
        "specific weights, cutoffs or opponent probabilities are approved.",
        "Next we need current 2026 head-to-head mechanics from engine source",
        "or unambiguous events, and a test that uses moving opponents and",
        "actual apple-contest behavior. Held-out diverse-opponent ablations",
        "must precede promotion of any rule.",
        "",
        "## Auditable data","",
        "- [Source frame-based first moves and pre-action cone features](../derived/route_choice_windows.csv).",
        "- [Cohort rates](../derived/opponent_cone_cohorts.csv).",
        "- [Head-event and transition audit counts](../derived/route_cone_quality.json).",
        "- [Paired student/season comparisons](../derived/opponent_cone_paired_students.csv).",
        "- [Underlying dynamic-space report](route_space.md).",
        "",
        "**No Java competition snake code was touched.**",""]
    report=data_dir/"reports"/"opponent_cones.md"
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text("\n".join(lines),encoding="utf-8")
    return dict(league_windows=len(league),trial_windows=len(trial),
                holdout_auc=aucs,bootstrap=contrasts,
                matched_pairs=len(pairs),paired_students=len(same_students),
                quality=qc,report=str(report))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    args=p.parse_args()
    print(json.dumps(build(args.data_dir),indent=2))

if __name__=="__main__":
    main()
