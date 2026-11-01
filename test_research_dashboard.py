"""Offline checks for the research dashboard (no Wits network calls)."""
import gzip
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from xml.etree import ElementTree

from research.eda_core import length_bin, replay_summary
from research.dashboard import build

class ResearchDashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.season="2026-11-01-205859-season"
        self.name="403754-vhuimo-mudau"
        db=sqlite3.connect(self.root/"snake.db")
        db.executescript("""CREATE TABLE seasons(name TEXT PRIMARY KEY,created TEXT);
            CREATE TABLE matches(season_name TEXT,replay_name TEXT,kind TEXT,replay_sha256 TEXT);
            CREATE TABLE participants(season_name TEXT,replay_name TEXT,team_slug TEXT,
                final_length INTEGER,food_eaten INTEGER,placement INTEGER);""")
        db.execute("INSERT INTO seasons VALUES (?,?)",(self.season,"2026-11-01"))
        for slug,length,food in [(self.name,175,34),("top-snake",255,50)]:
            db.execute("INSERT INTO matches VALUES (?,?,?,?)",
                       (self.season,f"trials/{slug}/trial-912000.rep","trial","dummy"))
            db.execute("INSERT INTO participants VALUES (?,?,?,?,?,?)",
                       (self.season,f"trials/{slug}/trial-912000.rep",slug,length,food,1))
        db.commit()
        db.close()
        states=[]
        for t in range(4):
            alive=t<3
            states.append({"turn":t,
                "snakes":[{"id":0,"name":self.name,"alive":alive,
                           "length":25 if alive else 0,
                           "body":[{"x":t,"y":0}] if alive else []},
                          {"id":1,"name":"~benchmark","alive":True,
                           "length":5,"body":[{"x":0,"y":t}]}],
                "events":[{"kind":"died","snake":0,
                           "cause":{"kind":"self_collision"}}] if t==3 else []})
        path=self.root/"replays"/self.season/"trials"/self.name/"trial-912000.rep.gz"
        path.parent.mkdir(parents=True)
        with gzip.open(path,"wt",encoding="utf-8") as f:
            json.dump({"header":{"board":[35,35]},"frames":states},f)

    def test_length_bins(self):
        self.assertEqual(length_bin(5),"5-24")
        self.assertEqual(length_bin(149),"100-149")
        self.assertIsNone(length_bin(0))

    def test_death_attribution(self):
        stats=replay_summary(self.root,self.season,250)
        self.assertEqual(stats["unique"],1)
        self.assertEqual(stats["exposures"]["Student"]["25-49"],3)
        self.assertEqual(stats["deaths"]["Student"]["self_collision"],1)
        self.assertEqual(stats["deaths"]["Student"]["bin:25-49"],1)

    def test_match_modes_are_not_pooled_in_replay_risk(self):
        stats=replay_summary(self.root,self.season,250)
        self.assertEqual(stats["unique_modes"]["trial"],1)
        self.assertEqual(stats["unique_modes"]["league"],0)
        self.assertEqual(stats["mode_exposures"]["trial"]["25-49"],3)
        self.assertEqual(stats["mode_deaths"]["trial"]["bin:25-49"],1)
        self.assertEqual(stats["mode_exposures"]["league"]["25-49"],0)

    def test_dashboard_charts(self):
        result=build(self.root)
        self.assertEqual(result["trials"],2)
        self.assertEqual(result["curves"],1)
        for file in ["gauntlet_rankings.svg","apples_vs_length.svg",
                     "gauntlet_growth.svg","death_causes.svg","death_rates.svg",
                     "death_rates_by_mode.svg"]:
            ElementTree.parse(self.root/"reports"/"charts"/file)
        report=(self.root/"reports"/"data_science.md").read_text()
        self.assertIn("175",report)
        self.assertIn("2/2",report)
        self.assertIn("Corrected: student death risk separated by mode",report)

if __name__=="__main__":
    unittest.main()
