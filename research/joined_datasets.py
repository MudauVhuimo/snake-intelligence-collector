"""Canonical, audited Snake26 league/trial dataset join.

Source of truth: published match catalogs in data/snake.db.
Join key: (season_name, team_slug); season-level SHA is attached as a
snapshot marker, NOT proof that every game used that version.
No replay-derived claims are imputed from catalog results.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
import argparse
import csv
import json
import sqlite3
import random

from .league_core import spearman, current_season

SUITES = ("910000", "911000", "912000")
METRICS = (
    ("mean_food", "mean_food", "Apples per game"),
    ("mean_length", "mean_length", "Final body length"),
    ("mean_kills", "mean_kills", "Kills per game"),
    ("mean_retention", "mean_retention", "Retained growth / expected no-reset growth"),
)

def average(values):
    vals = [v for v in values if v is not None]
    return mean(vals) if vals else None

def retained(length,food):
    if length is None or food is None or food < 0:
        return None
    expected = 5 + 5*food
    return length/expected if expected > 0 else None

def get_rows(db):
    values = db.execute(
        """SELECT m.season_name,p.team_slug,m.replay_name,m.kind,m.division,
                  m.replay_sha256,p.placement,p.final_length,p.food_eaten,
                  p.kills,p.deaths,b.observed_moves,b.deaths
           FROM matches m JOIN participants p
             ON p.season_name=m.season_name AND p.replay_name=m.replay_name
           LEFT JOIN behavior b
             ON b.season_name=p.season_name AND b.replay_name=p.replay_name
                AND b.team_slug=p.team_slug
           WHERE m.kept=1 AND m.kind IN ('league','trial')
             AND p.team_slug NOT LIKE '~%'
           ORDER BY m.season_name,m.replay_name,p.team_slug"""
    ).fetchall()
    # One row = one identifiable student in one official match. Do not multiply
    # rows by joining full behavior or event tables of multiple events.
    humans=Counter((r[0],r[2]) for r in values)
    results=[]
    for season,team,replay,kind,div,sha,place,length,food,kills,deaths,moves,observed_deaths in values:
        if kind=="league" and humans[season,replay] < 2:
            # League match with one student and three built-in fillers is
            # not evidence of student-vs-student competitive skill.
            continue
        suite=next((s for s in SUITES if replay.endswith("/trial-"+s+".rep")),None)
        if kind=="trial" and suite is None:
            continue
        results.append(dict(season=season,team=team,replay=replay,kind=kind,
                            division=div,students=humans[season,replay],
                            suite=suite,has_replay=bool(sha),sha=sha,
                            placement=place,final_length=length,food=food,
                            kills=kills,deaths=observed_deaths if sha else None,
                            observed_moves=moves if sha else None,
                            retention=retained(length,food)))
    return results

def summarize(rows,kind):
    groups=defaultdict(list)
    for row in rows:
        if row["kind"]==kind:
            groups[(row["season"],row["team"])].append(row)
    result={}
    for key,obs in groups.items():
        # Three controlled on-arrival suites = three separate experimental
        # conditions, not three independent copies of the same treatment.
        suites={r["suite"]:r for r in obs if kind=="trial"}
        if kind=="trial" and len(suites)!=len(obs):
            raise ValueError(f"Duplicate on-arrival suite for {key}")
        kept = list(suites.values()) if kind=="trial" else obs
        result[key]=dict(
            season=key[0], team=key[1], games=len(kept),
            suites=len(suites) if kind=="trial" else None,
            complete=bool(kind=="trial" and len(suites)==3
                          and all(suites[s]["placement"] is not None and
                                  suites[s]["final_length"] is not None for s in SUITES)),
            mean_place=average([r["placement"] for r in kept]),
            win_rate=average([int(r["placement"]==1) for r in kept if r["placement"] is not None]),
            mean_food=average([r["food"] for r in kept]),
            mean_final_length=average([r["final_length"] for r in kept]),
            mean_kills=average([r["kills"] for r in kept]),
            mean_retention=average([r["retention"] for r in kept]),
            replays=sum(r["has_replay"] for r in kept),
            observed_deaths=sum(r["deaths"] or 0 for r in kept if r["has_replay"]),
            observed_moves=sum(r["observed_moves"] or 0 for r in kept if r["has_replay"]),
            observed_death_games=sum(r["deaths"] is not None for r in kept),
            pure_games=sum(r["students"]==4 for r in kept) if kind=="league" else None,
            mixed_games=sum(r["students"]<4 for r in kept) if kind=="league" else None,
            gauntlet_length=suites.get("912000",{}).get("final_length") if kind=="trial" else None,
            gauntlet_food=suites.get("912000",{}).get("food") if kind=="trial" else None,
        )
    return result

def write_csv(path,rows,fields):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def snapshot(db):
    rows=get_rows(db)
    league=summarize(rows,"league")
    trial=summarize(rows,"trial")
    standings={(season,team):dict(division=div,rank=rank,points=points,rating=rating)
               for season,team,div,rank,points,rating in db.execute(
               "SELECT season_name,team_slug,division,division_rank,points,rating FROM standings")}
    versions={(season,team):sha for season,team,sha in db.execute(
        "SELECT season_name,team_slug,sha256 FROM team_versions")}
    latest=current_season(db)
    joined=[]
    for key in sorted(set(league)|set(trial)):
        lm=league.get(key,{})
        tm=trial.get(key,{})
        st=standings.get(key,{})
        version=versions.get(key)
        result=dict(season=key[0],team=key[1],version_sha256=version,
                    version_evidence="season-end snapshot only" if version else "unknown",
                    official_division=st.get("division"),official_rank=st.get("rank"),
                    official_points=st.get("points"),official_rating=st.get("rating"),
                    league_games=lm.get("games",0),league_replays=lm.get("replays",0),
                    league_pure_games=lm.get("pure_games",0),league_mixed_games=lm.get("mixed_games",0),
                    league_mean_place=lm.get("mean_place"),league_win_rate=lm.get("win_rate"),
                    league_mean_food=lm.get("mean_food"),
                    league_mean_length=lm.get("mean_final_length"),
                    league_mean_kills=lm.get("mean_kills"),
                    league_mean_retention=lm.get("mean_retention"),
                    league_observed_deaths=lm.get("observed_deaths"),
                    league_observed_moves=lm.get("observed_moves"),
                    trial_games=tm.get("games",0),trial_suites=tm.get("suites",0),
                    trial_complete=bool(tm.get("complete")),
                    trial_replays=tm.get("replays",0),trial_mean_place=tm.get("mean_place"),
                    trial_win_rate=tm.get("win_rate"),
                    trial_mean_food=tm.get("mean_food"),
                    trial_mean_length=tm.get("mean_final_length"),
                    trial_mean_kills=tm.get("mean_kills"),
                    trial_mean_retention=tm.get("mean_retention"),
                    trial_gauntlet_length=tm.get("gauntlet_length"),
                    trial_gauntlet_food=tm.get("gauntlet_food"),
                    trial_observed_deaths=tm.get("observed_deaths"),
                    trial_observed_moves=tm.get("observed_moves"))
        result["paired"] = bool(result["league_games"]>=2 and result["trial_complete"])
        joined.append(result)
    return dict(latest=latest,rows=rows,league=league,trial=trial,
                joined=joined,standings=standings)

def paired_bootstrap_rho(values_x,values_y,draws=2000,seed=2026):
    """Percentile interval resampling STUDENTS (the actual paired units).

    This represents sampling variation within the current division only.
    It does not correct opponent selection, repeated seasons or version drift.
    """
    n=len(values_x)
    if n<8 or n!=len(values_y):
        return None
    rng=random.Random(seed)
    vals=[]
    for _ in range(draws):
        indexes=[rng.randrange(n) for _ in range(n)]
        rho=spearman([values_x[i] for i in indexes],
                     [values_y[i] for i in indexes])
        if rho is not None:
            vals.append(rho)
    if len(vals)<max(40,draws//2):
        return None
    vals.sort()
    return dict(low=vals[int(.025*(len(vals)-1))],
                high=vals[int(.975*(len(vals)-1))],
                draws=len(vals))

def correlations(joined,season,division=1,min_league=3):
    people=[r for r in joined if r["season"]==season
            and r["official_division"]==division
            and r["trial_complete"] and r["league_games"]>=min_league]
    results=[]
    for index,(league_field,trial_field,label) in enumerate(METRICS):
        valid=[r for r in people if r["league_"+league_field] is not None
               and r["trial_"+trial_field] is not None]
        lx=[r["league_"+league_field] for r in valid]
        tx=[r["trial_"+trial_field] for r in valid]
        value=spearman(lx,tx)
        interval=paired_bootstrap_rho(lx,tx,seed=2026+index) if value is not None else None
        results.append(dict(metric=label,n=len(valid),rho=value,
                            ci_low=interval["low"] if interval else None,
                            ci_high=interval["high"] if interval else None,
                            ci_draws=interval["draws"] if interval else 0))
    return people,results

def audit(db,rows):
    mode=Counter()
    observed=Counter()
    unique=defaultdict(set)
    for kind,n,downloaded,distinct in db.execute(
        """SELECT kind,COUNT(*),
           SUM(CASE WHEN replay_sha256 IS NOT NULL THEN 1 ELSE 0 END),
           COUNT(DISTINCT replay_sha256)
           FROM matches WHERE kind IN ('league','trial') AND kept=1 GROUP BY kind"""
    ):
        mode[kind]=n
        observed[kind]=downloaded or 0
    for mode_name,sha in db.execute(
        "SELECT kind,replay_sha256 FROM matches WHERE replay_sha256 IS NOT NULL"):
        if sha:
            unique[mode_name].add(sha)
    return dict(catalog=dict(mode),replays=dict(observed),
                unique={k:len(unique[k]) for k in ("league","trial")},
                game_rows=len(rows),bad_retention=sum(r["retention"] is not None
                     and r["retention"]>1.001 for r in rows))

def build(data_dir):
    with sqlite3.connect(data_dir/"snake.db") as db:
        snap=snapshot(db)
        qa=audit(db,snap["rows"])
    derived=data_dir/"derived"
    derived.mkdir(parents=True,exist_ok=True)
    league_rows=list(snap["league"].values())
    trial_rows=list(snap["trial"].values())
    joined=snap["joined"]
    # Preserve stable field order so downstream plots/notebooks can reuse files.
    write_csv(derived/"league_team_seasons.csv",league_rows,list(league_rows[0]) if league_rows else ["season","team"])
    write_csv(derived/"trial_team_seasons.csv",trial_rows,list(trial_rows[0]) if trial_rows else ["season","team"])
    write_csv(derived/"joined_team_seasons.csv",joined,list(joined[0]) if joined else ["season","team"])
    people,metrics=correlations(joined,snap["latest"],division=1)
    paired=sum(r["paired"] for r in joined if r["season"]==snap["latest"])
    qa.update(current_season=snap["latest"],league_team_seasons=len(league_rows),
              trial_team_seasons=len(trial_rows),joined_rows=len(joined),
              latest_div1_matched=len(people),latest_season_paired=paired,
              correlations=metrics)
    (derived/"quality.json").write_text(json.dumps(qa,indent=2)+"\n",encoding="utf-8")
    return snap,qa

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    args=p.parse_args()
    _,qa=build(args.data_dir)
    print(json.dumps(qa,indent=2))

if __name__=="__main__":
    main()
