"""Synthetic, deterministic tests for food matching and censoring rules."""
import gzip
import json
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from research.food_race_core import (
    dist, replay_food_events, scan, advantage_band, lag_band,
)
from research.food_races import build

def snake(ident,name,x,y):
    return {"id":ident,"name":name,"alive":True,
            "body":[{"x":x,"y":y}]}

def fixture(with_eat=True):
    return {"header":{"board":[35,35]},"frames":[
        {"turn":0,"snakes":[snake(0,"student",1,0),snake(1,"~benchmark",4,0)],
         "food":[{"x":2,"y":0}],"events":[]},
        {"turn":1,"snakes":[snake(0,"student",2,0),snake(1,"~benchmark",3,0)],
         "food":[],"events":[{"kind":"ate","snake":0}] if with_eat else []},
        {"turn":2,"snakes":[snake(0,"student",3,0),snake(1,"~benchmark",3,1)],
         "food":[],"events":[]}
    ]}

class FoodRacesTests(unittest.TestCase):
    def test_wrap_dist(self):
        self.assertEqual(dist((34,0),(0,0),35,35),1)
        self.assertEqual(dist((0,34),(0,0),35,35),1)

    def test_capture_requires_both_ate_and_head(self):
        rows,qc=replay_food_events(fixture())
        self.assertEqual(qc["matched"],1)
        self.assertEqual(qc["disappeared"],1)
        self.assertEqual(rows[0]["winner"],"student")
        self.assertEqual(rows[0]["advantage"],-1)
        self.assertTrue(rows[0]["contested"])
        self.assertEqual(rows[0]["lag"],1)
        missing,stats=replay_food_events(fixture(False))
        self.assertEqual(missing,[])
        self.assertEqual(stats["unmatched"],1)

    def test_unmatched_position_is_not_guessed(self):
        replay=fixture()
        replay["frames"][1]["snakes"][0]["body"][0]["x"]=6
        rows,checks=replay_food_events(replay)
        self.assertEqual(rows,[])
        self.assertEqual(checks["unmatched"],1)

    def test_lag_categories(self):
        self.assertEqual(lag_band(4),"1-5")
        self.assertEqual(lag_band(101),"101+")
        self.assertEqual(advantage_band(4),"Benchmark 3+ closer")

    def test_exact_duplicate_files(self):
        with tempfile.TemporaryDirectory() as rootdir:
            root=Path(rootdir)
            for season in ("a","b"):
                p=root/"replays"/season/"trials"/"student"/"trial-912000.rep.gz"
                p.parent.mkdir(parents=True,exist_ok=True)
                with gzip.open(p,"wb") as f:
                    f.write(json.dumps(fixture()).encode())
            quality,modes=scan(root)
            self.assertEqual(quality["unique"],1)
            self.assertEqual(quality["duplicates"],1)
            self.assertEqual(len(modes["On-arrival"]),1)
            result=build(root)
            self.assertEqual(result["confirmed"],1)
            for name in ("food_start_advantage.svg","food_capture_lag.svg"):
                ET.parse(root/"reports"/"charts"/name)
            self.assertIn("100.0%",(root/"reports"/"food_races.md").read_text())

if __name__=="__main__":
    unittest.main()
