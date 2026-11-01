"""End-to-end regression checks for our canonical JOINED research tables."""
from pathlib import Path
from xml.etree import ElementTree
import csv
import json
import tempfile
import unittest

from collector import connect,ingest_latest_season,ingest_games
from research.joined_datasets import snapshot,correlations,retained
from research.integrated_dashboard import build

SEASON="2026-11-02-010000-season"
OLD="2026-10-21-010000-season"
NAMES=("top-league","top-trial","middle","lower","trial-only")

class JoinedResearchTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data=Path(self.temp.name)
        db=connect(self.data/"snake.db")
        season=dict(name=SEASON,meta={"created":"2026-11-02T01:00:00"},
                    entrants=[dict(name=n,id=n,sha256=f"sha-{n}") for n in NAMES],
                    standings=[dict(name=n,division=1 if n!="trial-only" else 2,
                                    points=30-i,rating=1000-i,games=3,wins=1)
                               for i,n in enumerate(NAMES)],
                    tables=[dict(division=1,table=[dict(name=n,position=i+1)
                                   for i,n in enumerate(NAMES[:4])]),
                            dict(division=2,table=[dict(name="trial-only",position=1)])])
        ingest_latest_season(db,season)
        games=[]
        # One genuine four-student league match per round and three fixed trials.
        for round_no in range(3):
            snakes=[]
            for i,n in enumerate(NAMES[:4]):
                snakes.append(dict(name=n,placement=i+1,
                    length=50+(3-i)*8+round_no*5,
                    food=10+(3-i)*2+round_no,kills=3-i,
                    turns=2000))
            games.append(dict(replay=f"game-7{round_no}000.rep",kind="league",
                              division=1,seed=70000+round_no,kept=True,
                              snakes=snakes))
        # Single-human league game must NOT enter our peer league dataset.
        games.append(dict(replay="game-filler.rep",kind="league",division=2,
                          seed=10,kept=True,snakes=[
            dict(name="trial-only",placement=1,length=150,food=29,kills=3),
            dict(name="~benchmark",placement=2,length=5,food=0,kills=0)]))
        for i,n in enumerate(NAMES):
            for suite in ("910000","911000","912000"):
                games.append(dict(replay=f"trials/{n}/trial-{suite}.rep",
                                  kind="trial",seed=int(suite),kept=True,
                                  snakes=[
                                      dict(name=n,placement=1,length=50+i*25,food=10+i*6,kills=i),
                                      dict(name="~benchmark",placement=2,length=5,food=0,kills=0)]))
        ingest_games(db,SEASON,dict(season=SEASON,games=games))
        # Historical data must remain an independent season, not join current.
        ingest_games(db,OLD,{"season":OLD,"games":[
            dict(replay="game-123.rep",kind="league",seed=123,kept=True,
                 snakes=[dict(name="top-league",placement=1,length=5,food=0,kills=0),
                         dict(name="middle",placement=2,length=5,food=0,kills=0)])]})
        db.execute("UPDATE matches SET replay_sha256='real-sha' "
                   "WHERE season_name=? AND replay_name='game-70000.rep'",(SEASON,))
        db.commit()
        db.close()

    def test_separate_sources_and_join_identity(self):
        db=connect(self.data/"snake.db")
        try:
            data=snapshot(db)
        finally:
            db.close()
        self.assertEqual(data["latest"],SEASON)
        self.assertEqual(len([x for x in data["joined"] if x["season"]==SEASON]),5)
        cohort=[r for r in data["joined"] if r["season"]==SEASON]
        lead=next(r for r in cohort if r["team"]=="top-league")
        trial_only=next(r for r in cohort if r["team"]=="trial-only")
        self.assertEqual(lead["league_games"],3)
        self.assertEqual(lead["trial_games"],3)
        self.assertEqual(lead["league_replays"],1)
        self.assertTrue(lead["trial_complete"])
        self.assertEqual(lead["official_rank"],1)
        self.assertEqual(lead["version_sha256"],"sha-top-league")
        self.assertEqual(lead["version_evidence"],"season-end snapshot only")
        self.assertEqual(trial_only["league_games"],0)
        self.assertFalse(trial_only["paired"])
        historical=next(r for r in data["joined"] if r["season"]==OLD and r["team"]=="top-league")
        self.assertEqual(historical["version_evidence"],"unknown")
        self.assertFalse(historical["paired"])
        paired,metrics=correlations(data["joined"],SEASON,division=1)
        self.assertEqual(len(paired),4)
        self.assertEqual(len(metrics),4)
        self.assertTrue(all(m["rho"] is not None for m in metrics))

    def test_final_length_ratio_is_not_death_count(self):
        self.assertEqual(retained(55,10),1)
        self.assertAlmostEqual(retained(5,10),5/55)
        self.assertIsNone(retained(None,10))
        self.assertIsNone(retained(10,None))

    def test_canonical_figures_report_and_csvs(self):
        result=build(self.data)
        self.assertEqual(result["paired_division1"],4)
        path=self.data/"reports"/"joint_analysis.md"
        report=path.read_text(encoding="utf-8")
        self.assertIn("same season + same student",report)
        self.assertIn("League replays",report)
        self.assertIn("Source",report)
        self.assertIn("top-league",report)
        for metric in ("apples","length","kills","retention","correlations"):
            ElementTree.parse(self.data/"reports"/"charts"/("joint_"+metric+".svg"))
        with (self.data/"derived"/"joined_team_seasons.csv").open(newline="") as f:
            joined=list(csv.DictReader(f))
        self.assertEqual(len(joined),7)  # five current + two historical
        self.assertEqual(len({(r["season"],r["team"]) for r in joined}),len(joined))
        quality=json.loads((self.data/"derived"/"quality.json").read_text())
        self.assertEqual(quality["latest_season_paired"],4)
        self.assertEqual(quality["replays"]["league"],1)
        self.assertIn("canonical research entry", (self.data/"reports"/"README.md").read_text())

if __name__=="__main__":
    unittest.main()
