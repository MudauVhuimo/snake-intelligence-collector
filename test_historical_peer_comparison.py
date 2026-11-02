"""Historical peer-match comparison works even when official standings are absent."""
import csv
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree

from collector import connect,ingest_games
from research.historical_peer_comparison import analyze,build

SEASON="2026-10-16-020000-season"

class HistoricalPeerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.db=connect(self.root/"snake.db")
        self.addCleanup(self.db.close)
        games=[]
        for round_no in range(3):
            for group in range(3):
                snakes=[]
                for seat in range(4):
                    i=group*4+seat
                    snakes.append(dict(name=f"student-{i:02d}",
                        placement=seat+1,length=5+5*(20-seat*3),
                        food=20-seat*3,kills=3-seat))
                games.append(dict(replay=f"game-7{round_no}{group:02d}.rep",
                                  kind="league",division=1,seed=70000+round_no*100+group,
                                  kept=True,snakes=snakes))
        for i in range(12):
            for suite in ("910000","911000","912000"):
                games.append(dict(replay=f"trials/student-{i:02d}/trial-{suite}.rep",
                    kind="trial",seed=int(suite),kept=True,
                    snakes=[dict(name=f"student-{i:02d}",placement=1,
                                 length=215-(i%4)*35,food=40-(i%4)*7,kills=2),
                            dict(name="~benchmark",placement=2,length=5,food=0,kills=0)]))
        ingest_games(self.db,SEASON,{"season":SEASON,"games":games})
        self.db.commit()

    def test_old_missing_standings_can_still_be_analyzed(self):
        results,students,quality=analyze(self.db)
        self.assertEqual(len(results),1)
        self.assertEqual(results[0]["n"],12)
        self.assertEqual(results[0]["official_rank_available"],0)
        self.assertEqual(len(students),12)
        self.assertEqual(results[0]["rho"],1)

    def test_full_report_and_csv(self):
        result=build(self.root)
        self.assertEqual(result["seasons"],1)
        self.assertEqual(result["div1_snapshots"],1)
        ElementTree.parse(self.root/"reports"/"charts"/"historical_peer_vs_trial.svg")
        with (self.root/"derived"/"historical_peer_trial_students.csv").open(newline="") as f:
            self.assertEqual(len(list(csv.DictReader(f))),12)
        doc=(self.root/"reports"/"historical_peer_comparison.md").read_text()
        self.assertIn("not official rank",doc.lower())
        self.assertIn("12 | +1.000",doc)

if __name__=="__main__":
    unittest.main()
