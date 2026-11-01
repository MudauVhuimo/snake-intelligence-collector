"""Build the Snake26 Phase I data-science report from archived public data.

Usage: python -m research.dashboard
No game bots, external requests, or third-party dependencies.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import sqlite3

from .eda_core import BINS, CAUSES, replay_summary, trial_catalog
from .eda_charts import apples, growth, grouped, rankings

OUR_SLUG = "403754-vhuimo-mudau"

def build(data_dir: Path, our_slug: str = OUR_SLUG, max_files: int = 250):
    db = sqlite3.connect(data_dir/"snake.db")
    try:
        season, rows = trial_catalog(db)
        seasons = db.execute("SELECT COUNT(*) FROM seasons").fetchone()[0]
        matches = db.execute("SELECT COUNT(*) FROM matches").fetchone()[0]
        saved = db.execute("SELECT COUNT(*) FROM matches WHERE replay_sha256 IS NOT NULL").fetchone()[0]
    finally:
        db.close()
    stats = replay_summary(data_dir,season,max_files)
    output=data_dir/"reports"
    figures=output/"charts"
    figures.mkdir(parents=True,exist_ok=True)
    rankings(figures/"gauntlet_rankings.svg",rows,our_slug)
    apples(figures/"apples_vs_length.svg",rows,our_slug)
    growth(figures/"gauntlet_growth.svg",stats["curves"],rows,our_slug)
    grouped(figures/"death_causes.svg","Observed death causes",list(CAUSES),
            stats["deaths"],{"self_collision":"Self","collision":"Body",
                             "head_to_head":"Head-to-head","other":"Other"})
    bins=[b[2] for b in BINS]
    rates=defaultdict(Counter)
    for group in ("Student","Benchmark"):
        for category in bins:
            denominator=stats["exposures"][group][category]
            numerator=stats["deaths"][group]["bin:"+category]
            rates[group][category]=(1000*numerator/denominator if denominator else 0)
    grouped(figures/"death_rates.svg","Deaths per 1,000 alive snake-turns",
            bins,rates,{})
    me=next((x for x in rows if x["name"]==our_slug),None)
    exact=sum(x["length"]==5+5*x["food"] for x in rows)
    impossible=sum(x["length"]>5+5*x["food"] for x in rows)
    lines=[
        "# Snake26 — Data Science Dashboard: Phase I","",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
        "## Data coverage and quality","",
        f"- Cataloged seasons: **{seasons:,}**; match records: **{matches:,}**.",
        f"- Replay records marked downloaded in SQLite: **{saved:,}**.",
        f"- Files on disk: **{stats['files']:,}**; sampled: **{stats['scanned']:,}**.",
        f"- Unique replay payloads (SHA-256): **{stats['unique']:,}**; duplicate payloads skipped: **{stats['duplicate']:,}**; unreadable: **{stats['bad']:,}**.",
        f"- Latest season: **{season or 'unavailable'}**; published gauntlet_1 trial results: **{len(rows):,}**.","",
        "> Thousands of catalog records are not thousands of independent replay observations.",
        "> Adjacent turns are correlated. Same bot, version, opponent setup or seed can recur.",
        "> These plots describe outcomes; they do not prove why any bot wins.","",
        "## 1. Comparable gauntlet_1 trial outcomes","",
        "![Final body lengths](charts/gauntlet_rankings.svg)","",
        "A single shared-seed on-arrival match per student is not evidence of consistent performance.",
        (f"Our recorded trial: **{me['length']} final length**, **{me['food']} apples**, placement **{me['place']}**."
         if me else "The configured student slug is absent from the latest trial catalog."),"",
        "## 2. Food acquired versus retained growth","",
        "![Apples and retained length](charts/apples_vs_length.svg)","",
        f"The no-reset relation **L = 5 + 5 × apples** holds exactly in **{exact}/{len(rows)}** reported trials.",
        f"**{impossible}** result(s) exceed this reference: inspect game mechanics if nonzero.",
        "Below-reference points may reflect growth lost to deaths, but only full replay events establish their cause.","",
        "## 3. Observed growth trajectories","",
        "![Growth across game turns](charts/gauntlet_growth.svg)","",
        f"Current-season gauntlet_1 trial replays with trajectories: **{len(stats['curves'])}**.",
        "Actual recorded body lengths, sampled every 100 turns; missing curves are not interpolated.","",
        "## 4. Deaths by recorded cause","",
        "![Observed death events](charts/death_causes.svg)","",
        "Raw counts mix opponent groups and survival exposure; they are not comparable risk rates.","",
        "## 5. Death-event rate by body length","",
        "![Deaths normalized by observed alive turns](charts/death_rates.svg)","",
        "| Length range | Student alive turns | Student deaths | Deaths / 1,000 alive turns | Benchmark alive turns | Benchmark deaths |",
        "|---|---:|---:|---:|---:|---:|"
    ]
    for b in bins:
        a=stats["exposures"]["Student"][b]
        d=stats["deaths"]["Student"]["bin:"+b]
        c=stats["exposures"]["Benchmark"][b]
        e=stats["deaths"]["Benchmark"]["bin:"+b]
        lines.append(f"| {b} | {a:,} | {d:,} | {1000*d/a if a else 0:.3f} | {c:,} | {e:,} |")
    lines.extend([
        "",
        "Exposure: one alive snake at the start of an observed turn. A death is attributed",
        "to its previous alive state, not the dead/respawned frame's length. A zero-exposure",
        "bin is **unknown**, not safe. Rates are descriptive and not independent probabilities.","",
        "## Research roadmap — no competition-snake changes yet","",
        "1. Detailed pre-death event studies and matched successful escapes.",
        "2. Food-contest timelines: distance to food at spawn, arrival times, and head pressure.",
        "3. Territory and opponent danger, including tail vacancy and time-dependent occupied space.",
        "4. Code-version cohorts and match-level/bootstrap uncertainty intervals.",
        "5. Separate league battles from fixed on-arrival trials before any causal claims.","",
        "We cannot replay private competitors as live executables using fixed recorded moves.",""
    ])
    target=output/"data_science.md"
    target.write_text("\n".join(lines),encoding="utf-8")
    return dict(seasons=seasons,catalogs=matches,files=stats["files"],
                unique=stats["unique"],duplicates=stats["duplicate"],
                trials=len(rows),curves=len(stats["curves"]),report=str(target))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir",type=Path,default=Path("data"))
    parser.add_argument("--our-slug",default=OUR_SLUG)
    parser.add_argument("--max-files",type=int,default=250)
    args=parser.parse_args()
    if args.max_files<0:
        parser.error("max-files must be nonnegative")
    print(json.dumps(build(args.data_dir,args.our_slug,args.max_files),indent=2))

if __name__=="__main__":
    main()
