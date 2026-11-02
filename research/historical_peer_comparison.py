"""Historical peer-game performance vs fixed-trial growth, WITHOUT official standings.

Unlike the official-rank comparison, this can inspect older seasons whose
standings were never captured. Match-derived placements are a DIFFERENT
outcome and must never be labeled an official division ranking.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
from datetime import datetime,timezone
from html import escape
from pathlib import Path
from statistics import mean,median
import csv
import json
import sqlite3
from .joined_datasets import snapshot
from .league_core import spearman
from .league_comparison import chart

def analyze(db,minimum_students=10,minimum_games=3):
    snap=snapshot(db)
    student_counts=defaultdict(set)
    matches=defaultdict(list)
    rows=db.execute(
        """SELECT m.season_name,m.replay_name,m.division,
                  p.team_slug,p.placement,p.final_length,p.food_eaten
           FROM matches m JOIN participants p
             ON p.season_name=m.season_name AND p.replay_name=m.replay_name
           WHERE m.kind='league' AND m.kept=1 AND m.division IS NOT NULL
             AND p.team_slug NOT LIKE '~%'
           ORDER BY m.season_name,m.replay_name"""
    )
    for season,replay,division,team,place,length,food in rows:
        student_counts[season,replay].add(team)
        matches[season,team].append(dict(season=season,replay=replay,
            division=division,team=team,place=place,length=length,food=food))
    grouped=defaultdict(list)
    coverage=Counter()
    for (season,team),games in matches.items():
        trials=snap["trial"].get((season,team))
        if not trials or not trials["complete"]:
            coverage["trial_incomplete"]+=1
            continue
        eligible=[g for g in games if len(student_counts[g["season"],g["replay"]])>=2
                  and g["place"] is not None]
        divisions={g["division"] for g in eligible}
        if len(eligible)<minimum_games:
            coverage["insufficient_peer_games"]+=1
            continue
        if len(divisions)!=1:
            coverage["ambiguous_division"]+=1
            continue
        division=next(iter(divisions))
        if trials["mean_final_length"] is None:
            coverage["missing_trial_length"]+=1
            continue
        grouped[season,division].append(dict(season=season,team=team,
            division=division,league_games=len(eligible),
            league_mean_place=mean(x["place"] for x in eligible),
            league_mean_length=mean(x["length"] for x in eligible
                                    if x["length"] is not None)
                                if any(x["length"] is not None for x in eligible) else None,
            trial_mean_length=trials["mean_final_length"],
            official_rank=snap["standings"].get((season,team),{}).get("rank"),
            snapshot_sha=snap["joined"][0].get("version_sha256") if False else
               next((r["version_sha256"] for r in snap["joined"] if
                     r["season"]==season and r["team"]==team),None)))
    time_series=[]
    student_rows=[]
    for (season,division),people in sorted(grouped.items()):
        if len(people)<minimum_students:
            coverage["small_cohort"]+=1
            continue
        rho=spearman([p["league_mean_place"] for p in people],
                     [-p["trial_mean_length"] for p in people])
        time_series.append(dict(season=season,division=division,
                                n=len(people),rho=rho,
                                mean_peer_games=round(mean(p["league_games"] for p in people),1),
                                official_rank_available=sum(p["official_rank"] is not None for p in people)))
        student_rows.extend(people)
    return time_series,student_rows,coverage

def plot(path,results):
    obs=sorted((r for r in results if r["division"]==1 and r["rho"] is not None),
               key=lambda r:r["season"])[-30:]
    if not obs:
        return chart(path,"Historical peer performance versus fixed trials",
                     ['<text x="40" y="100">No qualifying historical peer comparisons yet</text>'],220)
    X=lambda index:110+790*index/max(1,len(obs)-1)
    Y=lambda rho:350-255*(rho+1)/2
    parts=['<line x1="110" y1="350" x2="900" y2="350" stroke="#64748b"/>',
           '<line x1="110" y1="95" x2="110" y2="350" stroke="#64748b"/>']
    for rho in (-1,-.5,0,.5,1):
        yy=Y(rho)
        parts+= [f'<line x1="110" y1="{yy:.1f}" x2="900" y2="{yy:.1f}" stroke="#29364b"/>',
                 f'<text x="95" y="{yy+4:.1f}" text-anchor="end">{rho:+.1f}</text>']
    for i in range(len(obs)-1):
        a,b=obs[i:i+2]
        parts.append(f'<line x1="{X(i):.1f}" y1="{Y(a["rho"]):.1f}" '
                     f'x2="{X(i+1):.1f}" y2="{Y(b["rho"]):.1f}" '
                     f'stroke="#60a5fa" stroke-width="2.2"/>')
    for i,r in enumerate(obs):
        parts.append(f'<circle cx="{X(i):.1f}" cy="{Y(r["rho"]):.1f}" r="3.8" '
                     f'fill="#34d399"><title>{escape(r["season"])} '
                     f'cohort={r["n"]} rho={r["rho"]:+.3f}</title></circle>')
    parts+= [f'<text x="110" y="382">{escape(obs[0]["season"][:16])}</text>',
             f'<text x="900" y="382" text-anchor="end">{escape(obs[-1]["season"][:16])}</text>',
             '<text x="500" y="410" text-anchor="middle">'
             'Historical match CATALOG snapshots; NOT independent experimental repetitions</text>']
    chart(path,"Actual peer-game placement versus trial growth",parts,440)

def export(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        fields=list(rows[0]) if rows else ["season","division","n","rho"]
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def build(data_dir):
    with sqlite3.connect(data_dir/"snake.db") as db:
        correlations,student_rows,coverage=analyze(db)
    div1=sorted((r for r in correlations if r["division"]==1),
                key=lambda r:r["season"])
    all_seasons={r["season"] for r in correlations}
    chart_path=data_dir/"reports"/"charts"/"historical_peer_vs_trial.svg"
    plot(chart_path,correlations)
    derived=data_dir/"derived"
    export(derived/"historical_peer_trial_correlations.csv",correlations)
    export(derived/"historical_peer_trial_students.csv",student_rows)
    lines=[
        "# Snake26 historical league outcomes versus fixed trials","",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
        "## Why this analysis exists","",
        "We have many historical league match CATALOGS but relatively few saved",
        "official standings for old seasons. To use those actual student-vs-student",
        "games, we compute each student's average recorded league **placement**",
        "among at least three peer matches in one season and one match division.",
        "We compare it to that student's mean final length in all three on-arrival",
        "trial suites. Division is taken from the recorded league MATCH, not inferred",
        "from a missing official standings table.",
        "",
        "This is **not official rank** and must never be reported as official rank.",
        "Different league schedules and opponents affect placement. Many hourly",
        "snapshots reuse bots, seeds and exact match results, so the history is",
        "NOT a series of independent replications.","",
        "## Coverage","",
        f"- Season/division cohorts with at least 10 eligible students: **{len(correlations)}**.",
        f"- Distinct seasons represented: **{len(all_seasons)}**.",
        f"- Division 1 snapshots: **{len(div1)}**.",
        f"- Eligible student/season/division records: **{len(student_rows)}**.",
        f"- Excluded student-seasons with fewer than 3 peer league games: **{coverage['insufficient_peer_games']}**.",
        f"- Excluded student-seasons with conflicting match divisions: **{coverage['ambiguous_division']}**.",
        f"- Excluded student-seasons without all three trial suites: **{coverage['trial_incomplete']}**.",
        "",
        "## Student-vs-student placement correlation with benchmark growth","",
        "![Historical peer placement and trial growth](charts/historical_peer_vs_trial.svg)","",
        "A positive Spearman correlation means a student with better average",
        "league placement (smaller numerical place) tends to grow longer in trials",
        "(larger numerical length) *within the same season and match division*.",
        "It does NOT establish that benchmark growth causes league success.","",
        "| Indexed season | Division 1 students | Spearman rho | Avg peer matches/student | Official ranks saved? |",
        "|---|---:|---:|---:|---:|"]
    for r in div1[-24:][::-1]:
        lines.append(f"| {r['season']} | {r['n']} | "
                     f"{r['rho']:+.3f}" if r["rho"] is not None else
                     f"| {r['season']} | {r['n']} | insufficient")
        # Final two cells are appended without altering the original table cells.
        lines[-1]+=f" | {r['mean_peer_games']} | {r['official_rank_available']}/{r['n']} |"
    if not div1:
        lines.append("| No eligible Division 1 historical comparison yet | — | — | — | — |")
    lines+=["",
        "## Interpretation and responsible next actions","",
        "If league/trial ranking gaps persist across historical snapshots with",
        "the same recorded SHA, they are *hypotheses* about robustness, not proof",
        "of unchanged executable code. Select mismatched performers for full replay",
        "case studies; pair growth, actual deaths, threat exposure and length",
        "retention, controlling for opponents and game phase.",
        "",
        "## Downloadable derived inputs","",
        "- [Season-by-division peer-game correlations](../derived/historical_peer_trial_correlations.csv)",
        "- [Student-level source rows](../derived/historical_peer_trial_students.csv)",
        "No competition snake has been altered.",""]
    path=data_dir/"reports"/"historical_peer_comparison.md"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text("\n".join(lines),encoding="utf-8")
    return dict(seasons=len(all_seasons),div1_snapshots=len(div1),
                student_rows=len(student_rows),report=str(path),
                latest_div1_rho=div1[-1]["rho"] if div1 else None)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--data-dir",type=Path,default=Path("data"))
    args=parser.parse_args()
    print(json.dumps(build(args.data_dir),indent=2))

if __name__=="__main__":
    main()
