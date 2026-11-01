"""Study *association* between snapshot route reversal and observed apple capture.

Input: underdog_episodes.csv generated from public, deduplicated on-arrival
replays. Never use these descriptive statistics as a counterfactual win rate.
"""
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime, timezone
import argparse
import csv
import json
import random

from .eda_charts import grouped

def read_cases(path):
    cases=[]
    with path.open(encoding="utf-8",newline="") as source:
        for r in csv.DictReader(source):
            if r.get("study")!="benchmark_closer":
                continue
            if r.get("winner") not in ("Student","Benchmark"):
                continue
            if r.get("student_static") in ("","None",None):
                continue
            if r.get("bench_static") in ("","None",None):
                continue
            try:
                a=int(r["student_static"])
                b=int(r["bench_static"])
            except ValueError:
                continue
            cases.append(dict(path=r["path"],winner=r["winner"],
                              opponent=r["bench_name"],reversed=a<b,
                              a=a,b=b,margin=b-a))
    return cases

def bin_counts(cases):
    return Counter((r["reversed"],r["winner"]) for r in cases)

def capture_share(counts,rev):
    wins=counts[rev,"Student"]
    lost=counts[rev,"Benchmark"]
    return wins/(wins+lost) if wins+lost else None

def bootstrap(cases,iterations=4000,seed=2026):
    by_match=defaultdict(list)
    for case in cases:
        by_match[case["path"]].append(case)
    paths=list(by_match)
    if not paths:
        return None
    rng=random.Random(seed)
    differences=[]
    for _ in range(iterations):
        sample=Counter()
        for key in rng.choices(paths,k=len(paths)):
            sample.update(bin_counts(by_match[key]))
        p1=capture_share(sample,True)
        p0=capture_share(sample,False)
        if p1 is not None and p0 is not None:
            differences.append(p1-p0)
    if len(differences)<20:
        return None
    differences.sort()
    return dict(low=differences[int(.025*(len(differences)-1))],
                high=differences[int(.975*(len(differences)-1))],
                median=differences[len(differences)//2],
                draws=len(differences),clusters=len(paths))

def build(data_dir: Path):
    input_file=data_dir/"reports"/"underdog_episodes.csv"
    cases=read_cases(input_file)
    c=bin_counts(cases)
    p_reverse=capture_share(c,True)
    p_normal=capture_share(c,False)
    ci=bootstrap(cases)
    output=data_dir/"reports"
    fig=output/"charts"
    fig.mkdir(parents=True,exist_ok=True)
    values=defaultdict(Counter)
    for rev,label in ((True,"Reversed"),(False,"Not reversed")):
        p=capture_share(c,rev)
        if p is not None:
            values["Student"][label]=100*p
            values["Benchmark"][label]=100*(1-p)
    grouped(fig/"static_path_reversal.svg",
            "Capture shares, conditional on initially closer benchmark",
            ["Reversed","Not reversed"],values,
            {"Reversed":"Student static shorter","Not reversed":"Not shorter"})
    lines=[
        "# Snake26: does occupied-space geometry explain underdog apples?","",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
        "## Critical definition","",
        "All included food episodes start with a built-in benchmark head at least THREE",
        "toroidal Manhattan cells closer to the apple than the student head.",
        "For this snapshot, temporarily treat ALL occupied snake body cells and",
        "obstacles as permanently blocked, and run a toroidal breadth-first search",
        "from each head to the food. This is an approximation: bodies and tails move.",
        "Exclude episodes with no static path for either head, which can bias results.",
        "",
        "## Main association","",
        "![Frozen-body route order and real apple recipient](charts/static_path_reversal.svg)","",
        "| Frozen-body path ordering | Student captures | Benchmark captures | Student capture share |",
        "|---|---:|---:|---:|"
    ]
    for rev,label in ((True,"Student shortest"),(False,"Benchmark shortest or tied")):
        a,b=c[rev,"Student"],c[rev,"Benchmark"]
        share=100*a/(a+b) if a+b else 0
        lines.append(f"| {label} | {a} | {b} | {share:.1f}% |")
    if p_reverse is not None and p_normal is not None:
        lines.extend(["",f"Observed difference in student capture share: **{100*(p_reverse-p_normal):.1f} percentage points**."])
    if ci:
        lines.extend([
            f"Exploratory 95% **match-cluster bootstrap** interval for the difference:",
            f"**{100*ci['low']:.1f} to {100*ci['high']:.1f} percentage points**",
            f"({ci['draws']} valid bootstrap draws, resampling {ci['clusters']} complete replay matches).",
            "This interval reflects match-level resampling variability in this selected archive;",
            "it does not adjust for bot version, different opponent skill or hidden strategy choices."])
    lines.extend(["","## Check whether the pattern is unique to one benchmark","",
                  "| Initially closest benchmark | Reversal: student captures / all | Not reversed: student captures / all |",
                  "|---|---:|---:|"])
    opponents=sorted({r["opponent"] for r in cases})
    for opponent in opponents:
        batch=bin_counts([r for r in cases if r["opponent"]==opponent])
        cells=[]
        for rev in (True,False):
            a,b=batch[rev,"Student"],batch[rev,"Benchmark"]
            cells.append(f"{a}/{a+b} ({100*a/(a+b):.1f}%)" if a+b else "n/a")
        lines.append(f"| {opponent} | {cells[0]} | {cells[1]} |")
    lines.extend(["",
        "## What this does and DOES NOT establish","",
        "- This is **predictive association in recorded states**, not causal proof.",
        "- The more distant student may also differ in length, steering policy or risk tolerance.",
        "- The static route freezes every snake body; real tails vacate and opponents move.",
        "- A food capture is not necessarily a deliberate race by all possible opponents.",
        "- All apple events within one replay are correlated and should be clustered.",
        "- To claim a strategy advantage, validate these conditional patterns on held-out",
        "  replays and later compare actual executable snakes under controlled seeds.",
        "- No competition snake has been modified.",""])
    report=output/"path_geometry.md"
    report.write_text("\n".join(lines),encoding="utf-8")
    return dict(cases=len(cases),matches=len({r["path"] for r in cases}),
                reversed_student=c[True,"Student"],
                reversed_benchmark=c[True,"Benchmark"],
                normal_student=c[False,"Student"],
                normal_benchmark=c[False,"Benchmark"],
                bootstrap=ci,report=str(report))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    args=p.parse_args()
    print(json.dumps(build(args.data_dir),indent=2))

if __name__=="__main__":
    main()
