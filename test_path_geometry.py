"""Research regression tests for route reversal and match-level uncertainty."""
import csv
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree

from research.path_geometry import read_cases,bin_counts,capture_share,bootstrap,build

COLUMNS=("path","study","winner","bench_name","student_static","bench_static")

class GeometryStudyTests(unittest.TestCase):
    def test_frozen_route_reversal_is_not_manhattan_reversal(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            report=root/"reports"
            report.mkdir()
            input=report/"underdog_episodes.csv"
            with input.open("w",newline="",encoding="utf-8") as f:
                w=csv.DictWriter(f,fieldnames=COLUMNS)
                w.writeheader()
                for path in ("season-a/game","season-b/game"):
                    w.writerow(dict(path=path,study="benchmark_closer",winner="Student",
                                    bench_name="~survivor",student_static=7,bench_static=30))
                    w.writerow(dict(path=path,study="benchmark_closer",winner="Benchmark",
                                    bench_name="~survivor",student_static=30,bench_static=7))
                w.writerow(dict(path="s/game",study="benchmark_closer",winner="Student",
                                bench_name="~benchmark",student_static="",bench_static=9))
                w.writerow(dict(path="s/game",study="near_tie",winner="Student",
                                bench_name="~benchmark",student_static=8,bench_static=9))
            records=read_cases(input)
            self.assertEqual(len(records),4)
            counts=bin_counts(records)
            self.assertEqual(capture_share(counts,True),1)
            self.assertEqual(capture_share(counts,False),0)
            ci=bootstrap(records,100,2026)
            self.assertEqual(ci["clusters"],2)
            self.assertEqual(ci["median"],1)
            result=build(root)
            self.assertEqual(result["cases"],4)
            self.assertEqual(result["matches"],2)
            ElementTree.parse(report/"charts"/"static_path_reversal.svg")
            self.assertIn("match-cluster bootstrap",(report/"path_geometry.md").read_text())

if __name__=="__main__":
    unittest.main()
