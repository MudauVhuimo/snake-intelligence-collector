"""Mode-separated observed replay behavior; join on the same student-season.

Catalog measurements (all games) and observed movement measurements (downloaded
full replays only) are never mixed or silently substituted.
"""
from __future__ import annotations
from collections import defaultdict, Counter
from statistics import mean
from pathlib import Path
from html import escape
import argparse
import csv
import json
import sqlite3
from datetime import datetime, timezone

from .league_core import spearman, current_season
from .league_comparison import chart

def load(db):
    # Latest seasons first: if an exact replay payload recurs in an older
    # historical season, count it once for behavior and surface the limitation.
    records=db.execute(
        """SELECT m.season_name,m.replay_name,m.kind,m.replay_sha256,
                  p.team_slug,b.observed_moves,b.food_events,b.deaths,
                  b.self_collisions,b.body_collisions,b.head_to_head_deaths,
                  b.straight_moves,b.left_turns,b.right_turns
           FROM matches m JOIN participants p
              ON m.season_name=p.season_name AND m.replay_name=p.replay_name
           JOIN behavior b ON b.season_name=p.season_name
              AND b.replay_name=p.replay_name AND b.team_slug=p.team_slug
           WHERE m.kept=1 AND m.kind IN ('league','trial')
              AND m.replay_sha256 IS NOT NULL AND p.team_slug NOT LIKE '~%'
           ORDER BY m.season_name DESC,m.replay_name,p.team_slug"""
    ).fetchall()
    # League games with only one student aren't comparable to actual peers.
    human_counts={k:n for k,n in db.execute(
        """SELECT p.season_name || char(31) || p.replay_name,COUNT(*)
           FROM participants p JOIN matches m ON m.season_name=p.season_name
             AND m.replay_name=p.replay_name
           WHERE m.kind='league' AND m.kept=1 AND p.team_slug NOT LIKE '~%'
           GROUP BY p.season_name,p.replay_name"""
    )}
    groups=defaultdict(list)
    seen=set()
    quality=Counter()
    for season,replay,kind,sha,team,moves,food,deaths,self_deaths,body_deaths,head_deaths,straight,left,right in records:
        if kind=="league" and human_counts.get(season+"\x1f"+replay,0)<2:
            quality["one_student_league_excluded"]+=1
            continue
        duplicate=(sha,team)
        if duplicate in seen:
            quality["duplicate_team_replay_excluded"]+=1
            continue
        seen.add(duplicate)
        groups[season,team,kind].append(dict(season=season,team=team,mode=kind,
            replay=replay,sha=sha,moves=int(moves or 0),
            food=int(food or 0),deaths=int(deaths or 0),
            self_collisions=int(self_deaths or 0),body_collisions=int(body_deaths or 0),
            head_to_head=int(head_deaths or 0),straight=int(straight or 0),
            left=int(left or 0),right=int(right or 0)))
        quality[kind+"_replay_student_exposures"]+=1
    rows=[]
    for (season,team,kind),obs in sorted(groups.items()):
        total=lambda key:sum(r[key] for r in obs)
        moves=total("moves")
        rows.append(dict(season=season,team=team,mode=kind,matches=len(obs),
            observed_moves=moves,observed_food_events=total("food"),
            observed_deaths=total("deaths"),
            food_per_1000_moves=1000*total("food")/moves if moves else None,
            deaths_per_1000_moves=1000*total("deaths")/moves if moves else None,
            self_deaths_per_1000_moves=1000*total("self_collisions")/moves if moves else None,
            straight_fraction=total("straight")/moves if moves else None))
    return rows,quality

def paired(rows,season):
    by=defaultdict(dict)
    for r in rows:
        if r["season"]==season:
            by[r["team"]][r["mode"]]=r
    return [(n,v["league"],v["trial"]) for n,v in sorted(by.items())
            if "league" in v and "trial" in v and
            v["league"]["observed_moves"]>0 and v["trial"]["observed_moves"]>0]

def rate_chart(path,title,all_rows,field):
    modes=("league","trial")
    total={}
    for kind in modes:
        items=[r for r in all_rows if r["mode"]==kind]
        exposure=sum(x["observed_moves"] for x in items)
        numerator=sum(x["observed_food_events" if field=="food" else "observed_deaths"] for x in items)
        total[kind]=1000*numerator/exposure if exposure else None
    valid=[v for v in total.values() if v is not None]
    maximum=max(valid,default=1)
    high=max(1,maximum*1.2)
    body=['<text x="100" y="78">Selected unique replay student observations (not a random league sample)</text>',
          '<line x1="100" y1="380" x2="900" y2="380" stroke="#64748b"/>']
    for i,(mode,color) in enumerate((("league","#60a5fa"),("trial","#fbbf24"))):
        value=total[mode]
        x=275+i*380
        height=270*(value or 0)/high
        body.extend([
            f'<rect x="{x}" y="{380-height:.1f}" width="135" height="{height:.1f}" rx="5" fill="{color}"/>',
            f'<text x="{x+68}" y="{370-height:.1f}" text-anchor="middle" fill="#f8fafc">'
            f'{value:.3f}</text>' if value is not None else
            f'<text x="{x+68}" y="160" text-anchor="middle">No observations</text>',
            f'<text x="{x+68}" y="408" text-anchor="middle">{mode.title()}</text>'])
    chart(path,title,body,445)
    return total

def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    fields=list(rows[0]) if rows else ["season","team","mode","matches"]
    with path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def build(data_dir):
    with sqlite3.connect(data_dir/"snake.db") as db:
        latest=current_season(db)
        rows,quality=load(db)
    if not latest:
        raise RuntimeError("No current official season")
    all_pairs=paired(rows,latest)
    fields=(
        ("food_per_1000_moves","Food events per 1,000 observed moves"),
        ("deaths_per_1000_moves","Death events per 1,000 observed moves"),
        ("straight_fraction","Straight-move fraction")
    )
    associations=[]
    for key,label in fields:
        values=[(a[key],b[key]) for name,a,b in all_pairs if
                a.get(key) is not None and b.get(key) is not None]
        associations.append(dict(metric=label,n=len(values),
            rho=spearman([x for x,y in values],[y for x,y in values]) if len(values)>=4 else None))
    derived=data_dir/"derived"
    write_csv(derived/"replay_behavior_by_mode.csv",rows)
    figures=data_dir/"reports"/"charts"
    food_rates=rate_chart(figures/"observed_food_by_mode.svg",
                          "Observed food events per 1,000 moves",rows,"food")
    death_rates=rate_chart(figures/"observed_deaths_by_mode.svg",
                           "Observed deaths per 1,000 moves",rows,"deaths")
    format_rho=lambda value: f"{value:.3f}" if value is not None else "insufficient"
    lines=[
        "# Snake26: Replay behavior by environment, then joined by student","",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
        "**Source:** full replay-derived behavior table, NOT catalog outcome proxies.",
        "Every student/match is grouped by explicit match kind. A SHA-identical",
        "replay reused in another season is counted once per student here.",
        "Student-only versus mixed league game composition is retained by",
        "excluding one-student matches. Full opponent strength is not controlled.",
        "",
        "## 1. How many students have observations in BOTH environments?","",
        f"- Current official season: **{latest}**.",
        f"- Current season unique students with at least one replay in EACH mode: **{len(all_pairs)}**.",
        f"- Duplicate student/replay SHA observations excluded: **{quality['duplicate_team_replay_excluded']}**.",
        f"- One-student league observations excluded: **{quality['one_student_league_excluded']}**.",
        f"- Student-replay exposures from league: **{quality['league_replay_student_exposures']}**.",
        f"- Student-replay exposures from trials: **{quality['trial_replay_student_exposures']}**.","",
        "## 2. Two different game environments","",
        "![Food events per move by mode](charts/observed_food_by_mode.svg)","",
        "![Death events per move by mode](charts/observed_deaths_by_mode.svg)","",
        "These rates use confirmed replay observation counts and measured moves",
        "as exposure. They are NOT apples/deaths per game, nor lifetime survival probabilities.",
        "They combine different opponents and selected matches: do not interpret",
        "the group gap as a treatment or optimal aggression setting.",
        "",
        "## 3. Join the SAME student-season across both replay sources","",
        "| Replay-derived metric | Students with BOTH modes | Spearman rho league vs trial |",
        "|---|---:|---:|"
    ]
    for a in associations:
        lines.append(f"| {a['metric']} | {a['n']} | {format_rho(a['rho'])} |")
    lines += ["",
        "If too few students have replay evidence on both sides, correlation is",
        "reported as insufficient—not extrapolated from catalog placements.",
        "",
        "## 4. Export and next controls","",
        "- [One row per observed student/season/mode](../derived/replay_behavior_by_mode.csv).",
        "- [Main catalog-based joined study](joint_analysis.md).",
        "- Need matched opponent strength, turn/length stratification and more",
        "  Division 1 student-versus-student replays for mechanism claims.",
        "- Multiple moves within one match are correlated; do not use naive turn-level",
        "  confidence intervals or mistake sample selection for a fair experiment.",
        "- Bot SHA tracked at season snapshot only; mid-season changes may exist.",""]
    target=data_dir/"reports"/"behavior_by_mode.md"
    target.write_text("\n".join(lines),encoding="utf-8")
    return dict(season=latest,paired_student_replays=len(all_pairs),
                observations=len(rows),correlations=associations,
                mode_rates=dict(food=food_rates,deaths=death_rates),
                report=str(target))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    args=p.parse_args()
    print(json.dumps(build(args.data_dir),indent=2))

if __name__=="__main__":
    main()
