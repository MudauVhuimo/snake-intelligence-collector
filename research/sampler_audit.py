"""Offline preview of the league/trial replay sampler against the archived catalog."""
from collections import Counter
from pathlib import Path
import argparse
import json
import sqlite3
from collector import queued_matches, promising_trial_slugs

def preview(data_dir:Path,limit:int=10,lookback:int=12):
    with sqlite3.connect(data_dir/"snake.db") as db:
        row=db.execute("""SELECT season_name FROM standings
                          GROUP BY season_name ORDER BY season_name DESC LIMIT 1""").fetchone()
        if not row:
            raise ValueError("No indexed season standings")
        current=row[0]
        others=[r[0] for r in db.execute(
            """SELECT season_name FROM matches WHERE season_name!=?
               GROUP BY season_name ORDER BY season_name DESC LIMIT ?""",
            (current,lookback-1))]
        seasons=[current]+others
        tops={r[0] for r in db.execute(
            "SELECT team_slug FROM standings WHERE season_name=? "
            "AND division=1 AND division_rank<=10",(current,))}
        priority=tops|promising_trial_slugs(db,current)
        picked=queued_matches(db,data_dir,seasons,priority,limit)
        details=[]
        for season,name in picked:
            kind,division=db.execute(
                "SELECT kind,division FROM matches WHERE season_name=? AND replay_name=?",
                (season,name)).fetchone()
            humans=db.execute(
                "SELECT COUNT(*) FROM participants WHERE season_name=? AND replay_name=? "
                "AND team_slug NOT LIKE '~%'",
                (season,name)).fetchone()[0]
            details.append(dict(season=season,name=name,
                                kind="trial" if kind=="trial" else "league",
                                division=division,students=humans))
        counts=Counter(r["kind"] for r in details)
        suites=Counter(next((x for x in ("910000","911000","912000") if x in r["name"]),"other")
                       for r in details if r["kind"]=="trial")
    return dict(current=current,counts=dict(counts),trial_suites=dict(suites),
                historical=sum(r["season"]!=current for r in details),choices=details)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    p.add_argument("--limit",type=int,default=10)
    args=p.parse_args()
    print(json.dumps(preview(args.data_dir,args.limit),indent=2))

if __name__=="__main__":
    main()
