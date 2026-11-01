"""Generate a measurement-first study of apparently disadvantaged apple captures."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import argparse
import csv
import json
import statistics

from .underdog_core import scan
from .food_race_core import lag_band, LAGS
from .eda_charts import grouped

def mean_or_none(values):
    return round(statistics.mean(values),2) if values else None

def median_or_none(values):
    return round(statistics.median(values),2) if values else None

def summarize(rows):
    groups=defaultdict(list)
    for row in rows:
        groups[(row["study"],row["winner"])].append(row)
    summary={}
    for label in ("benchmark_closer","near_tie","student_closer"):
        for winner in ("Student","Benchmark"):
            batch=groups[(label,winner)]
            p5s=[x["student_p5"] for x in batch if x["student_p5"] is not None]
            p5b=[x["bench_p5"] for x in batch if x["bench_p5"] is not None]
            paired=[x for x in batch if x["student_p5"] is not None and x["bench_p5"] is not None]
            summary[(label,winner)]=dict(
                count=len(batch),
                lag_median=median_or_none([x["lag"] for x in batch]),
                nearest_benchmark_died=sum(x["bench_death"] for x in batch),
                student_died=sum(x["student_death"] for x in batch),
                paired5=len(paired),
                student_progress_mean=mean_or_none([x["student_p5"] for x in paired]),
                bench_progress_mean=mean_or_none([x["bench_p5"] for x in paired]),
                student_approach_share=round(100*sum(x["student_p5"]>0 for x in paired)/len(paired),1) if paired else None,
                bench_approach_share=round(100*sum(x["bench_p5"]>0 for x in paired)/len(paired),1) if paired else None)
    return summary

def svg_for_progress(rows, target):
    by_type=defaultdict(list)
    for row in rows:
        if row["study"]!="benchmark_closer":
            continue
        if row["student_p5"] is not None and row["bench_p5"] is not None:
            by_type[row["winner"]].append(row)
    values=defaultdict(Counter)
    for winner in ("Student","Benchmark"):
        group=by_type[winner]
        if not group:
            continue
        values["Student"][winner]=100*sum(x["student_p5"]>0 for x in group)/len(group)
        values["Benchmark"][winner]=100*sum(x["bench_p5"]>0 for x in group)/len(group)
    grouped(target,"Moved closer in first 5 turns, by eventual capture",
            ["Student","Benchmark"],values,
            {"Student":"Student wins","Benchmark":"Benchmark wins"})
    return {winner:len(by_type[winner]) for winner in ("Student","Benchmark")}

def write_csv(rows,path):
    path.parent.mkdir(parents=True,exist_ok=True)
    names=("path","start_turn","pos_x","pos_y","lag","winner","winner_name",
           "student_name","bench_name","student_start","bench_start","advantage",
           "study","student_p5","bench_p5","student_p10","bench_p10",
           "student_death","bench_death","student_length","bench_length")
    with path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=names)
        writer.writeheader()
        for r in rows:
            x={k:r.get(k) for k in names}
            x["pos_x"],x["pos_y"]=r["pos"]
            writer.writerow(x)

def build(data_dir: Path,max_files=250):
    rows,q=scan(data_dir,max_files)
    results=summarize(rows)
    folder=data_dir/"reports"
    charts=folder/"charts"
    charts.mkdir(parents=True,exist_ok=True)
    by_start=defaultdict(Counter)
    by_lag=defaultdict(Counter)
    for row in rows:
        by_start[row["winner"]][row["study"]]+=1
        if row["study"]=="benchmark_closer":
            by_lag[row["winner"]][lag_band(row["lag"])]+=1
    grouped(charts/"underdog_outcomes.svg","Food captures vs initially closer group",
            ["benchmark_closer","near_tie","student_closer"],by_start,
            {"benchmark_closer":"Bench +3", "near_tie":"Difference 0-2",
             "student_closer":"Student +3"})
    grouped(charts/"underdog_lag.svg","Apple lifetime when benchmark starts 3+ closer",
            list(LAGS),by_lag,{})
    paired_sizes=svg_for_progress(rows,charts/"underdog_progress.svg")
    # Export ALL episodes for auditing; also save a small hand-picked example trace
    write_csv(rows,folder/"underdog_episodes.csv")
    useful=sorted((r for r in rows if r["study"]=="benchmark_closer" and
                   r["winner"]=="Student" and r["lag"]>=8 and not r["bench_death"]
                   and not r["student_death"] and r["student_p5"] is not None
                   and r["bench_p5"] is not None),
                  key=lambda x:(-x["advantage"], x["lag"], x["path"], x["start_turn"]))
    top=useful[:15]
    examples=[]
    for r in top:
        examples.append(dict(path=r["path"],start_turn=r["start_turn"],food=list(r["pos"]),
                             student=r["student_name"],nearest_benchmark=r["bench_name"],
                             initial_student_distance=r["student_start"],
                             initial_benchmark_distance=r["bench_start"],
                             winner=r["winner_name"],duration=r["lag"],trace=r["trace"]))
    (folder/"underdog_examples.json").write_text(json.dumps(examples,indent=2)+"\n",encoding="utf-8")
    our=results[("benchmark_closer","Student")]
    their=results[("benchmark_closer","Benchmark")]
    lines=[
      "# Snake26 — How did the farther snake win?","",
      "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
      "## Evidence quality","",
      f"- Scanned **{q['scanned']}** replay files; unique on-arrival trial replays: **{q['unique_trial_replays']}**.",
      f"- Duplicate archived trial files skipped: **{q['duplicates']}**; unreadable: **{q['invalid']}**.",
      f"- Comparable first-visible student-vs-benchmark apple opportunities: **{q['eligible_episodes']}**.",
      f"- Captures matched to real next-frame head + eat event: **{q['matched']}**.",
      f"- Disappearances without verified consumer: **{q['unmatched']}**.",
      "Only on-arrival trials with EXACTLY one active student and at least one living built-in benchmark are included.",
      "All distance comparisons use toroidal Manhattan geometry, not hypothetical safe paths.","",
      "## Initial distance disadvantage versus actual winner","",
      "![Outcome by initial distance advantage](charts/underdog_outcomes.svg)","",
      "| Who started at least 3 cells closer? | Student captured | Benchmark captured | Student share |",
      "|---|---:|---:|---:|"
    ]
    for group,label in (("benchmark_closer","Benchmark"),("near_tie","Neither (within 2)"),
                        ("student_closer","Student")):
        a=results[(group,"Student")]["count"]
        b=results[(group,"Benchmark")]["count"]
        lines.append(f"| {label} | {a:,} | {b:,} | {100*a/(a+b):.1f}% |" if a+b else f"| {label} | 0 | 0 | n/a |")
    lines += [
      "", "The student share above describes captured apples only. One student faces three",
      "benchmarks and their starting abilities and survival vary; it is NOT a fair head-to-head win rate.","",
      "## Focus: student captured while a benchmark started 3+ closer","",
      f"- Verified captures: **{our['count']}**; benchmark wins while initially closer: **{their['count']}**.",
      f"- In student wins, initially nearest benchmark died before capture: **{our['nearest_benchmark_died']}**.",
      f"- In student wins, student died before capture: **{our['student_died']}**.",
      f"- Median apple lifetime, student wins: **{our['lag_median']} turns**; benchmark wins: **{their['lag_median']} turns**.","",
      "![Food capture times](charts/underdog_lag.svg)","",
      "## First five turns: movement toward apple","",
      "![Fraction moving closer](charts/underdog_progress.svg)","",
      f"- Complete comparable five-turn, death-free trajectories: **{paired_sizes['Student']}** student-win",
      f"  and **{paired_sizes['Benchmark']}** benchmark-win apple episodes.",
      f"- Student-win: student progress **{our['student_progress_mean']}** cells on average; nearest",
      f"  benchmark progress **{our['bench_progress_mean']}** cells (distance decrease positive).",
      f"- Benchmark-win: student progress **{their['student_progress_mean']}** cells; nearest",
      f"  benchmark progress **{their['bench_progress_mean']}** cells.",
      "We exclude episodes with a death or respawn of either focal snake anywhere before capture",
      "from this particular five-turn comparison. The selection is intentional but may bias results.",
      "The apple must remain visible for 5 turns; fast captures are also excluded.","",
      "## Individual cases for inspection","",
      "See **underdog_examples.json** for up to 15 recorded distance traces of student wins",
      "where a benchmark started at least 3 cells closer, both focal snakes remained alive,",
      "and the apple remained present at least 8 turns.",
      "See **underdog_episodes.csv** for all matched on-arrival events with distances, capture",
      "time, death flags, and early-distance progress.","",
      "| Replay | First visible turn | Student initial distance | Nearest benchmark | Benchmark distance | Captured after |",
      "|---|---:|---:|---|---:|---:|"
    ]
    for r in top[:10]:
        lines.append(f"| {r['path']} | {r['start_turn']} | {r['student_start']} | {r['bench_name']} | {r['bench_start']} | {r['lag']} |")
    lines.extend(["","## Interpretation and next work","",
      "Farther-but-faster does not automatically imply pathfinding superiority.",
      "A closer snake could have chosen a different apple, waited for safety, or been",
      "unable to reach the apple along a safe path. Other opponents can affect both.",
      "Next: calculate **actual route efficiency and obstacle-aware distance at first sight**;",
      "compare traced examples, then produce spatial board/path visualizations.",
      "No competition bot has been modified.",""])
    dest=folder/"underdog_study.md"
    dest.write_text("\n".join(lines),encoding="utf-8")
    return dict(unique=q["unique_trial_replays"],eligible=q["eligible_episodes"],
                confirmed=q["matched"],underdog_student_wins=our["count"],
                closest_benchmark_died=our["nearest_benchmark_died"],
                examples=len(examples),report=str(dest))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    p.add_argument("--max-files",type=int,default=250)
    args=p.parse_args()
    if args.max_files<0:p.error("max-files must be nonnegative")
    print(json.dumps(build(args.data_dir,args.max_files),indent=2))

if __name__=="__main__":
    main()
