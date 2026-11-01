"""Food competition report and SVG charts from confirmed observed food events."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json

from .food_race_core import scan, BANDS, LAGS, lag_band
from .eda_charts import grouped

def build(data_dir: Path,max_files=250):
    quality,modes=scan(data_dir,max_files)
    output=data_dir/"reports"
    output.mkdir(parents=True,exist_ok=True)
    chart_dir=output/"charts"
    chart_dir.mkdir(parents=True,exist_ok=True)
    trials=modes.get("On-arrival",[])
    by_distance=defaultdict(Counter)
    by_lag=defaultdict(Counter)
    contests=Counter()
    for row in trials:
        if row["band"]:
            by_distance[row["group"]][row["band"]]+=1
        by_lag[row["group"]][lag_band(row["lag"])]+=1
        if row["contested"]:
            contests[row["group"]]+=1
    label={
        BANDS[0]:"Student +3", BANDS[1]:"Student +1-2",
        BANDS[2]:"Tied", BANDS[3]:"Benchmark +1-2",
        BANDS[4]:"Benchmark +3",
    }
    grouped(chart_dir/"food_start_advantage.svg",
            "Who collects apples by first-visible distance advantage",
            list(BANDS),by_distance,label)
    grouped(chart_dir/"food_capture_lag.svg",
            "Observed apple lifetime before confirmed consumption",
            list(LAGS),by_lag,{})
    q=quality
    coverage=100*q["matched"]/q["disappeared"] if q["disappeared"] else 0
    lines=[
        "# Snake26 Food Races: Observational Study", "",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
        "## Data validity FIRST", "",
        f"- Replay files scanned: **{q['scanned']}** of {q['files']}; unique content: **{q['unique']}**.",
        f"- Exact duplicates skipped: **{q['duplicates']}**; unreadable replays: **{q['invalid']}**.",
        f"- First-visible apple episodes: **{q['first_visible']}**.",
        f"- Apples disappearing between adjacent states: **{q['disappeared']}**.",
        f"- Captures matched to next-head position AND explicit eat event: **{q['matched']}**.",
        f"- Unmatched disappearances: **{q['unmatched']}**.",
        f"- Confirmation rate among disappeared apples: **{coverage:.1f}%**.",
        f"- On-arrival matched apple events: **{len(trials)}**; league matched events: **{len(modes.get('League',[]))}**.","",
        "> The measurement is conservative. A disappearing apple without BOTH",
        "> a matching eat event and next-frame head is not assigned a winner.",
        "> A low confirmation rate could indicate timing/schema mismatch.",
        "> A first-visible apple may already have existed before a replay started.","",
        "## 1. Apples won by starting-distance advantage","",
        "![Observed apple outcomes by initial food distance](charts/food_start_advantage.svg)","",
        "At each first-visible apple location, we measure the toroidal Manhattan",
        "distance from the nearest living student head and nearest built-in benchmark head.",
        "Student +3 means the student head was at least three cells closer.",
        "We then identify which type ACTUALLY consumed the apple, using recorded events.",
        "Bars show observed counts only, **not normalized win probabilities**.","",
        "## 2. How long did those apples remain available?","",
        "![Observed food lifetimes](charts/food_capture_lag.svg)","",
        "Duration is turns from first visible board coordinate to confirmed capture.",
        "It does NOT mean the winner deliberately pursued that apple the entire time.",
        "Unconsumed/censored opportunities are not included in the lifetime histogram.","",
        "## 3. Close competitive opportunities","",
        "We call an apple initially contested when the student versus benchmark",
        "nearest-head distances differ by at most two cells, and at least one head",
        "is at toroidal Manhattan distance ten or less at first appearance.",
        f"Observed matched contested captures: **{sum(contests.values())}**.",
        f"- Student captured: **{contests['Student']}**.",
        f"- Built-in benchmark captured: **{contests['Benchmark']}**.","",
        "That is an operational distance-based definition, not proof of",
        "the actual safe paths, intentions or likelihood of winning.","",
        "## 4. Environment coverage","",
        "| Mode | Matched apple captures | Student captures | Benchmark captures |",
        "|---|---:|---:|---:|"
    ]
    for mode in ("On-arrival","League"):
        rows=modes.get(mode,[])
        by=Counter(r["group"] for r in rows)
        lines.append(f"| {mode} | {len(rows)} | {by['Student']} | {by['Benchmark']} |")
    lines.extend(["",
        "## Next research questions","",
        "1. For each new apple, inspect time-to-first-target movement and the route actually taken.",
        "2. Compare occupied-path distance rather than toroidal Manhattan distance alone.",
        "3. Stratify by student identity, bot code hash, turn, length, and opponent group.",
        "4. Quantify head-on collision threats during near-tie contests.",
        "5. Analyze missing/disappearing-event coverage before making strong claims.","",
        "### Interpretation rules","",
        "- Archived actions do not tell us why a bot chose a route.",
        "- Food disappearing without a matching event is missing evidence, not a loss.",
        "- Recorded opponents would react differently to hypothetical player moves.",
        "- Multiple captures per match are correlated. Avoid naive independent confidence intervals.",
        "- Do not implement a new Snake AI during this research-only phase.",""
    ])
    target=output/"food_races.md"
    target.write_text("\n".join(lines),encoding="utf-8")
    return {"replays":q["unique"],"confirmed":q["matched"],
            "missing":q["unmatched"],"contested":sum(contests.values()),
            "report":str(target)}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    p.add_argument("--max-files",type=int,default=250)
    args=p.parse_args()
    if args.max_files<0:p.error("max-files must not be negative")
    print(json.dumps(build(args.data_dir,args.max_files),indent=2))

if __name__=="__main__":
    main()
