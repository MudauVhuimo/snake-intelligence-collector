"""Regression checks: raw replay behavior must not be substituted by catalog stats."""
from pathlib import Path
from xml.etree import ElementTree
import csv
import tempfile
import unittest

from collector import connect,ingest_games,ingest_latest_season
from research.behavior_by_mode import build,load,paired

S="2026-11-02-000000-season"
A,B="strong","steady"

class ReplayBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data=Path(self.temp.name)
        db=connect(self.data/"snake.db")
        ingest_latest_season(db,dict(name=S,
            meta={"created":"2026-11-02T00:00:00"},
            entrants=[dict(name=n,id=n,sha256="sha-"+n) for n in (A,B)],
            standings=[dict(name=n,division=1,points=1,games=1,wins=0) for n in (A,B)],
            tables=[dict(division=1,table=[dict(name=A,position=1),dict(name=B,position=2)])]))
        league="game-777.rep"
        trial="trials/strong/trial-912000.rep"
        ingest_games(db,S,dict(season=S,games=[
            dict(replay=league,kind="league",division=1,kept=True,seed=777,
                 snakes=[dict(name=A,placement=1,length=25,food=4,kills=1),
                         dict(name=B,placement=2,length=10,food=1,kills=0)]),
            dict(replay=trial,kind="trial",kept=True,seed=912000,
                 snakes=[dict(name=A,placement=1,length=20,food=3,kills=1),
                         dict(name="~survivor",placement=2,length=5,food=0,kills=0)]),
        ]))
        for path,hash_value,kind in ((league,"league-hash","league"),(trial,"trial-hash","trial")):
            db.execute("UPDATE matches SET replay_sha256=? WHERE season_name=? AND replay_name=?",
                       (hash_value,S,path))
        for path,team,moves,food,deaths in (
            (league,A,900,4,1),(league,B,800,2,3),(trial,A,1800,9,0)):
            db.execute("""INSERT INTO behavior(season_name,replay_name,team_slug,
               observed_moves,straight_moves,left_turns,right_turns,food_events,
               deaths,self_collisions,body_collisions,head_to_head_deaths,avg_latency_ms)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
               (S,path,team,moves,moves//2,moves//4,moves-moves//2-moves//4,
                food,deaths,0,0,0,0))
        db.commit()
        db.close()

    def test_mode_separation_and_uncertainty(self):
        db=connect(self.data/"snake.db")
        try:
            rows,quality=load(db)
        finally:
            db.close()
        self.assertEqual(len(rows),3)
        both=paired(rows,S)
        self.assertEqual(len(both),1)
        self.assertEqual(both[0][0],A)
        self.assertEqual(both[0][1]["observed_deaths"],1)
        self.assertEqual(both[0][2]["observed_deaths"],0)
        self.assertEqual(quality["league_replay_student_exposures"],2)
        self.assertEqual(quality["trial_replay_student_exposures"],1)

    def test_report_and_svg(self):
        result=build(self.data)
        self.assertEqual(result["paired_student_replays"],1)
        self.assertTrue(all(c["rho"] is None for c in result["correlations"]))
        for p in ("observed_deaths_by_mode.svg","observed_food_by_mode.svg"):
            ElementTree.parse(self.data/"reports"/"charts"/p)
        with (self.data/"derived"/"replay_behavior_by_mode.csv").open() as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),3)
        self.assertIn("insufficient",(self.data/"reports"/"behavior_by_mode.md").read_text())

if __name__=="__main__":
    unittest.main()
