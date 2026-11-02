"""Synthetic tests: head proximity occurs BEFORE the recorded death outcome."""
import gzip
import json
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree

from research.threat_windows_core import (
    board_shape, category, distance, length_band, unoccupied_neighbors,
    scan_replay, load, summarize, per_student)
from research.threat_windows import build, cluster_interval

SEASON="2026-11-02-045859-season"
STUDENT="421462-alexander-palmer"

def snake(sid,name,x,y,alive=True):
    body=[dict(x=(x-i)%35,y=y%35) for i in range(5)] if alive else []
    return dict(id=sid,name=name,alive=alive,body=body)

def replay(mode="league",with_death=True):
    frames=[]
    for turn in range(41):
        # t=0 near; t=25 far. The event appears in frame 5,
        # within t=0's forward 10-turn window ONLY.
        far=turn>=20
        student_alive=not (with_death and 5<=turn<=10)
        frames.append(dict(
            turn=turn,
            snakes=[
                snake(0,STUDENT,1,1,student_alive),
                snake(1,"~benchmark" if mode=="trial" else "student-opponent",
                      20 if far else 3, 20 if far else 1)
            ],
            food=[dict(x=15,y=15)],
            events=[dict(kind="died",snake=0,cause=dict(kind="collision"))]
                   if with_death and turn==5 else []))
    return dict(header=dict(board=[35,35]),frames=frames)

class ThreatWindowsTests(unittest.TestCase):
    def test_wraparound_proximity_and_length(self):
        self.assertEqual(distance((34,0),(0,0),35,35),1)
        self.assertEqual(category(3),"near_0_3")
        self.assertEqual(category(8),"far_8_plus")
        self.assertEqual(length_band(49),"25-49")
        self.assertEqual(length_band(100),"100+")
        self.assertEqual(board_shape(replay()),(35,35))
        self.assertGreaterEqual(unoccupied_neighbors(replay()["frames"][0],(1,1),35,35),0)

    def test_death_cannot_leak_back_or_be_guessed(self):
        samples,quality=scan_replay(replay(),"s","game-1.rep","league","sha1")
        self.assertEqual(len(samples),4)  # 2 students at t=0 and t=25
        our=[r for r in samples if r["student"]==STUDENT]
        self.assertEqual(len(our),2)
        self.assertEqual(our[0]["start_turn"],0)
        self.assertEqual(our[0]["head_pressure"],"near_0_3")
        self.assertEqual(our[0]["death_next_10"],1)
        self.assertEqual(our[1]["start_turn"],25)
        self.assertEqual(our[1]["head_pressure"],"far_8_plus")
        self.assertEqual(our[1]["death_next_10"],0)
        self.assertEqual(quality["future_death_windows"],1)
        without,_=scan_replay(replay(with_death=False),"s","game-1.rep","league","sha1")
        self.assertEqual(sum(x["death_next_10"] for x in without),0)

    def test_trial_and_unmatched_league_rosters(self):
        trial,_=scan_replay(replay("trial"),SEASON,"trials/stu/trial-912000.rep","trial","x")
        self.assertEqual(len(trial),2)
        self.assertTrue(all(x["mode"]=="trial" for x in trial))
        rejected,qc=scan_replay(replay("trial"),SEASON,"game-1.rep","league","x")
        self.assertEqual(rejected,[])
        self.assertEqual(qc["excluded_single_student_league"],1)

    def test_true_dedup_plus_full_csv_and_svg(self):
        with tempfile.TemporaryDirectory() as root:
            data=Path(root)
            folder=data/"replays"/SEASON
            folder.mkdir(parents=True)
            for name,game in (("game-1.rep.gz",replay("league")),
                              ("game-2.rep.gz",replay("league")),
                              ("trials/stu/trial-912000.rep.gz",replay("trial"))):
                dest=folder/name
                dest.parent.mkdir(parents=True,exist_ok=True)
                with gzip.open(dest,"wt") as f:
                    json.dump(game,f)
            rows,quality=load(data)
            self.assertEqual(quality["unique_replays"],2)
            self.assertEqual(quality["duplicate_replays"],1)
            self.assertEqual(quality["league_unique_replays"],1)
            self.assertEqual(quality["trial_unique_replays"],1)
            report=build(data)
            self.assertEqual(report["latest_paired"],1)
            self.assertEqual(report["league_replays"],1)
            self.assertEqual(report["trial_replays"],1)
            ElementTree.parse(data/"reports"/"charts"/"head_pressure_vs_death.svg")
            self.assertTrue((data/"derived"/"threat_window_student_seasons.csv").is_file())
            self.assertTrue((data/"derived"/"threat_window_replay_summary.csv").is_file())
            self.assertIn("NEXT 10", (data/"reports"/"threat_windows.md").read_text())

    def test_match_cluster_bootstrap_needs_several_games(self):
        samples,_=scan_replay(replay(),SEASON,"game-1.rep","league","sha")
        self.assertIsNone(cluster_interval(samples,"league"))

if __name__=="__main__":
    unittest.main()
