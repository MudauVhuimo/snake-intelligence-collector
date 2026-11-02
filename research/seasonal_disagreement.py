"""Historical league/trial disagreements, same student and same season.

Avoid treating correlated hourly seasons or unchanged bot versions as independent
experimental replicates. Official ranks are compared ONLY within one division;
trial scores are reranked within that same division for transparency.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from statistics import median
import csv
import json
import sqlite3

from .joined_datasets import snapshot
from .league_core import midranks, spearman
from .league_comparison import chart

def study(rows,minimum=10):
    groups=defaultdict(list)
    for r in rows:
        if (r["official_division"] is not None
                and r["official_rank"] is not None
                and r["trial_complete"] and r["league_games"]>=3
                and r["trial_mean_length"] is not None):
            groups[r["season"],r["official_division"]].append(r)
    by_season={}
    episodes=[]
    for (season,division),batch in sorted(groups.items()):
        if len(batch)<minimum:
            continue
        # Ranks in league use official rank; trial ranks use a three-suite
        # average, reranked among students in the SAME official division.
        trial_rank=midranks([-r["trial_mean_length"] for r in batch])
        n=len(batch)
        official=[r["official_rank"] for r in batch]
        official_cohort_rank=midranks(official)
        rho=spearman(official,trial_rank)
        by_season[season,division]=dict(season=season,division=division,
                    n=n,rho=rho,latest=season==max(x[0] for x in groups),
                    paired_student_seasons=n)
        for r,rank,cohort_rank in zip(batch,trial_rank,official_cohort_rank):
            # Both percentiles refer to the SAME eligible student cohort.
            # Raw official position remains separately available in the export.
            official_pct=(cohort_rank-1)/max(1,n-1)
            trial_pct=(rank-1)/max(1,n-1)
            episodes.append(dict(
                season=season,division=division,student=r["team"],
                official_rank=r["official_rank"],trial_rank=rank,
                official_percentile=round(official_pct,4),
                trial_percentile=round(trial_pct,4),
                trial_minus_league=round(official_pct-trial_pct,4),
                league_games=r["league_games"],
                league_replays=r["league_replays"],
                trial_replays=r["trial_replays"],
                trial_mean_length=r["trial_mean_length"],
                league_mean_length=r["league_mean_length"],
                league_mean_food=r["league_mean_food"],
                league_mean_retention=r["league_mean_retention"],
                trial_mean_retention=r["trial_mean_retention"],
                version_snapshot=r["version_sha256"],
            ))
    return by_season,episodes

def svg_history(path,series,latest):
    obs=[r for r in series if r["division"]==1 and r["rho"] is not None]
    obs.sort(key=lambda x:x["season"])
    obs=obs[-24:]
    if not obs:
        return chart(path,"Division 1 trial/league agreement over time",
            ['<text x="45" y="100">No comparable snapshots yet</text>'],220)
    xleft,xright=115,900
    X=lambda i:xleft+(xright-xleft)*i/max(1,len(obs)-1)
    Y=lambda rho:342-250*(rho+1)/2
    marks=['<line x1="115" y1="342" x2="900" y2="342" stroke="#64748b"/>',
           '<line x1="115" y1="92" x2="115" y2="342" stroke="#64748b"/>']
    for value in (-1,-.5,0,.5,1):
        y=Y(value)
        marks += [f'<line x1="115" y1="{y:.1f}" x2="900" y2="{y:.1f}" stroke="#29364b"/>',
                  f'<text x="100" y="{y+4:.1f}" text-anchor="end">{value:+.1f}</text>']
    for i,(a,b) in enumerate(zip(obs,obs[1:])):
        marks.append(f'<line x1="{X(i):.1f}" y1="{Y(a["rho"]):.1f}" '
                     f'x2="{X(i+1):.1f}" y2="{Y(b["rho"]):.1f}" stroke="#60a5fa" stroke-width="2.8"/>')
    for i,r in enumerate(obs):
        marks.append(f'<circle cx="{X(i):.1f}" cy="{Y(r["rho"]):.1f}" '
                     f'r="4.2" fill="#34d399"><title>{escape(r["season"])} '
                     f'students={r["n"]} rho={r["rho"]:+.3f}</title></circle>')
    marks += [f'<text x="115" y="371">{escape(obs[0]["season"][:16])}</text>',
              f'<text x="900" y="371" text-anchor="end">{escape(obs[-1]["season"][:16])}</text>',
              '<text x="480" y="401" text-anchor="middle">'
              'Last 24 indexed snapshots, NOT independent repetitions</text>']
    chart(path,"Division 1: trial growth vs league rank over time",marks,430)

def svg_extremes(path,entries):
    ordered=sorted(entries,key=lambda r:abs(r["trial_minus_league"]),reverse=True)[:12]
    if not ordered:
        return chart(path,"Which students differ most between environments?",
                     ['<text x="40" y="100">No paired cohort</text>'],220)
    body=['<line x1="495" y1="70" x2="495" y2="690" stroke="#94a3b8"/>',
          '<text x="495" y="62" text-anchor="middle">Equal within-division percentile</text>']
    for i,r in enumerate(ordered):
        y=98+i*48
        delta=r["trial_minus_league"]
        magnitude=abs(delta)*320
        start=495 if delta>=0 else 495-magnitude
        col="#fbbf24" if delta>=0 else "#60a5fa"
        body.append(f'<rect x="{start:.1f}" y="{y}" width="{magnitude:.1f}" height="24" '
                    f'fill="{col}" rx="3"><title>{escape(r["student"])}; '
                    f'official rank {r["official_rank"]}, trial-within-division '
                    f'rank {r["trial_rank"]:.1f}</title></rect>')
        body.append(f'<text x="25" y="{y+17}" fill="#e2e8f0">'
                    f'{escape(r["student"].split("-",1)[-1][:25])}</text>')
        body.append(f'<text x="{start+magnitude+8:.1f}" y="{y+17}" fill="{col}">'
                    f'{delta:+.2f}</text>')
    body += ['<text x="170" y="712" fill="#60a5fa">Left: stronger in league</text>',
             '<text x="600" y="712" fill="#fbbf24">Right: stronger in trials</text>']
    chart(path,"Students whose league and trial ranks diverge",body,750)

def save_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    columns=list(rows[0]) if rows else ["season","division","student"]
    with path.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

def build(data_dir):
    with sqlite3.connect(data_dir/"snake.db") as db:
        snap=snapshot(db)
    seasons,rows=study(snap["joined"])
    latest=snap["latest"]
    current=[r for r in rows if r["season"]==latest and r["division"]==1]
    old=[r for r in seasons.values() if r["division"]==1 and r["rho"] is not None]
    old.sort(key=lambda r:r["season"])
    outcome=Counter()
    for row in old:
        outcome["eligible"]+=1
        if row["rho"]>0:outcome["positive"]+=1
    chart_dir=data_dir/"reports"/"charts"
    chart_dir.mkdir(parents=True,exist_ok=True)
    svg_history(chart_dir/"historical_rank_alignment.svg",list(seasons.values()),latest)
    svg_extremes(chart_dir/"league_trial_outliers.svg",current)
    dest=data_dir/"derived"/"seasonal_rank_gaps.csv"
    save_csv(dest,rows)
    sets=defaultdict(set)
    series=defaultdict(list)
    for r in rows:
        if r["division"]==1:
            series[r["student"]].append(r)
            if r["version_snapshot"]:
                sets[r["student"]].add(r["version_snapshot"])
    extreme_trials=sorted(current,key=lambda x:x["trial_minus_league"],reverse=True)
    extreme_league=sorted(current,key=lambda x:x["trial_minus_league"])
    lines=[
      "# Snake26: historical league versus trial specialization","",
      "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
      "## Design and guardrails","",
      "League ranks are official division-specific rankings; we rerank students",
      "inside the SAME eligible division cohort by their average final length",
      "across the three fixed on-arrival trials. Official positions are separately",
      "reranked within this eligible cohort before computing percentile gaps.",
      "We require at least three cataloged peer league",
      "games, all three on-arrival trials, and at least 10 students per division.",
      "A normalized rank difference of +1 means excellent trials relative to",
      "league, and -1 means excellent league performance relative to trials.",
      "These are ranks, NOT inferred policy scores or match-level causal effects.",
      "",
      f"Current season: **{latest}**.",
      f"Eligible historical Division 1 standings snapshots: **{outcome['eligible']}**.",
      f"Positive league/trial rank correlation: **{outcome['positive']}** snapshots.",
      f"Median Division 1 correlation: **{median(r['rho'] for r in old):+.3f}**." if old else
        "No historical Division 1 correlation data.",
      "",
      "Hourly seasons, repeated seeds, and unchanged bot versions are strongly",
      "correlated. The history is a trajectory of recorded competition snapshots,",
      "**not** a set of independent randomized experiments.","",
      "## 1. How does correlation evolve across seasons?","",
      "![Historical rank alignment](charts/historical_rank_alignment.svg)","",
      "| Season | Division 1 students | Spearman rho: league rank vs trial growth rank |",
      "|---|---:|---:|"]
    for r in old[-15:][::-1]:
        lines.append(f"| {r['season']} | {r['n']} | {r['rho']:+.3f} |")
    lines+=["",
      "## 2. Who specializes in a DIFFERENT environment?","",
      "![Within-Division rank gaps](charts/league_trial_outliers.svg)","",
      "**Positive difference:** relatively stronger three-trial growth;",
      "**negative:** relatively stronger competitive league rank.","",
      "| Trial specialists (Division 1) | League rank | Trial rank within Division 1 | Gap | League games | League full replays |",
      "|---|---:|---:|---:|---:|---:|"]
    for r in extreme_trials[:7]:
        lines.append(f"| {r['student']} | {r['official_rank']} | {r['trial_rank']:.1f} | "
                     f"{r['trial_minus_league']:+.2f} | {r['league_games']} | {r['league_replays']} |")
    lines+=["",
      "| League specialists (Division 1) | League rank | Trial rank within Division 1 | Gap | League games | League full replays |",
      "|---|---:|---:|---:|---:|---:|"]
    for r in extreme_league[:7]:
        lines.append(f"| {r['student']} | {r['official_rank']} | {r['trial_rank']:.1f} | "
                     f"{r['trial_minus_league']:+.2f} | {r['league_games']} | {r['league_replays']} |")
    lines+=["",
      "## 3. Repeated snapshots and bot changes","",
      "The next table lists select current Division 1 extremes. SHA counts are",
      "distinct *season-snapshot* version hashes, not confirmed per-match hashes.",
      "Repeated identical snapshots can produce apparent consistency without",
      "new independent evidence.",
      "",
      "| Student | Eligible Division 1 snapshots | Distinct snapshot hashes | Median rank gap |",
      "|---|---:|---:|---:|"]
    selected=list(dict.fromkeys([r["student"] for r in extreme_trials[:4]+extreme_league[:4]]))
    for name in selected:
        hist=series[name]
        if not hist:continue
        lines.append(f"| {name} | {len(hist)} | {len(sets[name])} | "
                     f"{median(x['trial_minus_league'] for x in hist):+.2f} |")
    lines+=["",
      "## 4. What this changes in our replay investigation","",
      "Target BOTH ends of the disagreement distribution: trial specialists",
      "who underperform in league, and league specialists who struggle in trials.",
      "For each, obtain actual full games from both environments and compare:",
      "survival/respawn, contested-food decisions, opponent proximity, risk versus",
      "growth and match outcomes under comparable conditions.",
      "Use historical snapshots to select interesting students, NOT as",
      "evidence of stable strategy unless versions and game conditions match.",
      "",
      "## Export","",
      "[All historical matched student-season rank gaps](../derived/seasonal_rank_gaps.csv)","",
      "This is observational research; no competition snake has been modified.",""]
    target=data_dir/"reports"/"seasonal_disagreement.md"
    target.write_text("\n".join(lines),encoding="utf-8")
    return dict(latest=latest,division1_snapshots=len(old),
                latest_students=len(current),recent_rho=old[-1]["rho"] if old else None,
                trial_specialists=[r["student"] for r in extreme_trials[:5]],
                league_specialists=[r["student"] for r in extreme_league[:5]],
                report=str(target))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    args=p.parse_args()
    print(json.dumps(build(args.data_dir),indent=2))

if __name__=="__main__":
    main()
