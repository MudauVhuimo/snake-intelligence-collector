#!/usr/bin/env python3
"""Compare on-arrival trial results with the SAME built-in opponents and seeds.

Uses complete public match catalog metadata; no replay download is needed.
Placements are game outcomes, not estimated from length.
"""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import sqlite3
from statistics import mean

from collector import utcnow

SUITES = {
    "910000": "hungry + survivor + benchmark",
    "911000": "hunter + benchmark + wander",
    "912000": "gauntlet_1 + survivor + benchmark",
}

def make_report(db: sqlite3.Connection) -> str:
    row = db.execute("SELECT name FROM seasons WHERE created IS NOT NULL ORDER BY name DESC LIMIT 1").fetchone()
    if not row:
        return "# On-arrival trial comparison\n\nNo current-season catalog yet.\n"
    season = row[0]
    rows=db.execute(
        """SELECT m.replay_name, p.team_slug, p.placement, p.final_length,
                  p.food_eaten, p.kills, m.seed
           FROM matches m JOIN participants p
             ON p.season_name=m.season_name AND p.replay_name=m.replay_name
           WHERE m.season_name=? AND m.kind='trial'
             AND p.team_slug NOT LIKE '~%'""", (season,)).fetchall()
    league = {n:(div,rank) for n,div,rank in db.execute(
        "SELECT team_slug,division,division_rank FROM standings WHERE season_name=?",(season,))}
    trials=defaultdict(dict)
    for replay,name,placement,length,food,kills,seed in rows:
        match_type = replay.rsplit("/",1)[-1]
        key=next((key for key in SUITES if f"trial-{key}.rep"==match_type),None)
        if not key:
            continue
        trials[name][key] = {"place":placement,"length":length,
            "food":food,"kills":kills,"replay":replay}
    complete={name:r for name,r in trials.items() if len(r)==3 and all(
        r[key]["place"] is not None for key in SUITES)}
    lines=["# Snake26 on-arrival trial comparison","",
           f"Generated UTC: {utcnow()}",
           f"Latest season: `{season}`",
           f"Student trial sets found: **{len(trials)}**",
           f"Complete three-trial sets: **{len(complete)}**","",
           "## Common benchmark setups","",
           "| Trial | Built-in opponents |",
           "|---|---|"]
    for k,opps in SUITES.items():
        lines.append(f"| `trial-{k}` | {opps} |")
    lines+=["","Each student runs these fixed baseline opponent groups. **Compare their official placements and recorded final lengths**; the replay is still needed to understand the decisions. Results from separate archived seasons may repeat identical submissions, so this report uses the latest season only.","",
            "## Combined ranking across all three trials","",
            "Sorted by mean placement (lower is better), then mean final length as a tiebreaker. This is a research ranking, **not the official league leaderboard**.","",
            "| # | Student bot | 910000 place | 911000 place | 912000 place | Mean place | Mean final length | Current division/rank |",
            "|---:|---|---:|---:|---:|---:|---:|---|"]
    ranked=sorted(complete.items(),key=lambda item:(
        mean(v["place"] for v in item[1].values()),
        -mean(v["length"] or 0 for v in item[1].values()),
        item[0]))
    for i,(name,obs) in enumerate(ranked[:35],1):
        places=[obs[k]["place"] for k in SUITES]
        lens=[obs[k]["length"] or 0 for k in SUITES]
        div,rank=league.get(name,(None,None))
        lines.append(f"| {i} | `{name}` | {places[0]} | {places[1]} | {places[2]} | {mean(places):.2f} | {mean(lens):.1f} | {f'{div}/{rank}' if div is not None else '—'} |")
    lines+=["","## Best performers specifically against gauntlet_1","",
            "Official placement and final length from the trial that also includes survivor and benchmark.","",
            "| # | Student bot | Placement | Final length | Food | Kills | Archived replay path |",
            "|---:|---|---:|---:|---:|---:|---|"]
    gauntlet=sorted(((name,v["912000"]) for name,v in trials.items()
                     if "912000" in v and v["912000"]["place"] is not None),
                    key=lambda x:(x[1]["place"],-(x[1]["length"] or 0),x[0]))
    for i,(name,obs) in enumerate(gauntlet[:35],1):
        lines.append(f"| {i} | `{name}` | {obs['place']} | {obs['length']} | {obs['food']} | {obs['kills']} | `{obs['replay']}` |")
    lines+=["","## Research next steps (no competition-bot implementation yet)","",
            "1. Compare the same student and season in the actual league and on-arrival conditions using the canonical [joined analysis](joint_analysis.md).",
            "2. For both settings, measure food, kills, growth retained and replay-derived death rates with matched definitions.",
            "3. Prioritize full league replays of Division 1 students and diverse on-arrival suites; deduplicate identical replay payloads.",
            "4. Treat large trial final lengths as controlled observations, not evidence of league dominance.",
            "",
            "Different bot versions, seeds, map changes, or seat orders make direct numerical comparisons misleading. These trial comparisons provide a common reference, not a controlled head-to-head against private competitor code.",""]
    return "\n".join(lines)

def main():
    data=Path("data")
    db=sqlite3.connect(data/"snake.db")
    try:
        report=make_report(db)
    finally:
        db.close()
    dst=data/"reports"/"trial_leaderboard.md"
    dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_text(report,encoding="utf-8")
    print("Wrote",dst)

if __name__=="__main__":
    main()
