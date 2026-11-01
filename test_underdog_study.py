"""Offline checks for observed underdog apple captures."""
from pathlib import Path
import gzip
import json
import tempfile
import unittest
from xml.etree import ElementTree
from research.underdog_core import extract, static_path_length
from research.underdog_study import build
from research.underdog_case_chart import chart_case

def game(student_win=True, death=False):
    frames=[]
    for t in range(7):
        student=min(t,5) if student_win else 0
        bench=(4-t)%35 if student_win else min(4+t,5)
        gone=t>=(5 if student_win else 1)
        events=[]
        if t==(5 if student_win else 1):
            events.append(dict(kind="ate",snake=0 if student_win else 1))
        if death and t==2:
            events.append(dict(kind="died",snake=1))
        frames.append(dict(
            turn=t,events=events,food=[] if gone else [dict(x=5,y=0)],
            snakes=[
                dict(id=0,name="student",alive=True,body=[dict(x=student,y=0)]),
                dict(id=1,name="~benchmark",alive=True,body=[dict(x=bench,y=0)])
            ]))
    return {"header":{"board":[35,35]},"frames":frames}

class Tests(unittest.TestCase):
    def test_farther_student_wins(self):
        rows,q=extract(game(),"trial")
        self.assertEqual(q["matched"],1)
        r=rows[0]
        self.assertEqual((r["winner"],r["advantage"],r["student_p5"],r["bench_p5"]),
                         ("Student",4,5,-5))
    def test_closer_benchmark_wins(self):
        r=extract(game(False),"trial")[0][0]
        self.assertEqual((r["winner"],r["lag"]),("Benchmark",1))
        self.assertIsNone(r["student_p5"])
    def test_death_excludes_progress(self):
        r=extract(game(True,True),"trial")[0][0]
        self.assertTrue(r["bench_death"])
        self.assertIsNone(r["bench_p5"])
    def test_static_paths_and_diverted_eating(self):
        replay=game()
        replay["frames"][2]["events"].append(dict(kind="ate",snake=1))
        row=extract(replay,"trial")[0][0]
        self.assertEqual(row["bench_other_ate"],1)
        self.assertGreaterEqual(row["student_static"],row["student_start"])
        self.assertGreaterEqual(row["bench_static"],row["bench_start"])

    def test_map_visualization(self):
        row=extract(game(),"trial")[0][0]
        case={"trace":row["trace"],"student":row["student_name"],
              "nearest_benchmark":row["bench_name"],"food":list(row["pos"]),
              "initial_student_distance":row["student_start"],
              "initial_benchmark_distance":row["bench_start"],"duration":row["lag"]}
        with tempfile.TemporaryDirectory() as t:
            path=Path(t)/"case.svg"
            chart_case(case,path)
            ElementTree.parse(path)

    def test_outputs(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            for i,wins in enumerate((True,False)):
                p=root/"replays"/"s"/"trials"/str(i)/"trial-912000.rep.gz"
                p.parent.mkdir(parents=True,exist_ok=True)
                with gzip.open(p,"wt") as f:
                    json.dump(game(wins),f)
            result=build(root)
            self.assertEqual(result["confirmed"],2)
            self.assertEqual(result["underdog_student_wins"],1)
            for name in ("underdog_outcomes.svg","underdog_lag.svg","underdog_progress.svg"):
                ElementTree.parse(root/"reports"/"charts"/name)
            self.assertEqual(len((root/"reports"/"underdog_episodes.csv").read_text().splitlines()),3)

if __name__=="__main__":
    unittest.main()
