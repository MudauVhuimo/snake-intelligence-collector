import tempfile
from pathlib import Path
import unittest

from collector import connect, ingest_games, ingest_latest_season
from trial_leaderboard import make_report

class TrialRankingTests(unittest.TestCase):
    def test_three_suite_comparison_from_catalog_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            db=connect(Path(tmp)/"test.db")
            season="2026-11-01-200000-season"
            ingest_latest_season(db,{
                "name":season,"meta":{"created":"2026-11-01T20:00:00","entrants":1,
                                     "rounds":6,"config_hash":"abc"},
                "entrants":[{"id":"student-a","name":"student-a","sha256":"a"}],
                "tables":[],"standings":[{"name":"student-a","division":1,
                                          "rating":1500,"points":10,"games":3,"wins":2}]
            })
            games=[]
            for i,seed in enumerate([910000,911000,912000]):
                games.append({"kind":"trial","replay":f"trials/student-a/trial-{seed}.rep",
                    "seed":seed,"kept":True,"round":None,"division":None,
                    "snakes":[{"name":"student-a","placement":1 if i==2 else 2,
                               "length":100+i*10,"food":20,"kills":0,"turns":2000},
                              {"name":"~benchmark","placement":3,
                               "length":5,"food":0,"kills":0,"turns":2000}]})
            ingest_games(db,season,{"season":season,"games":games})
            report=make_report(db)
            db.close()
            self.assertIn("Complete three-trial sets: **1**",report)
            self.assertIn("gauntlet_1",report)
            self.assertIn("student-a",report)
            self.assertIn("110",report)

if __name__=="__main__":
    unittest.main()
