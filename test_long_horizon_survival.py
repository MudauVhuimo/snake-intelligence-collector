"""Regression tests for 30-turn death, respawn, censoring and same-league-game comparison."""
import csv
import gzip
import json
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree

from research.long_horizon_core import (
    observed_followup,continuous_turns,outcome_status,load,
    survival_counts,by_recovery,recovery_label,PALMER)
from research.long_horizon_survival import build,cluster_bootstrap,palmer_comparison

SEASON="2026-11-02-045859-season"

def snake(sid,name,t,alive=True):
    if not alive:
        return dict(id=sid,name=name,alive=False,body=[])
    x=(3+t)%35
    body=[dict(x=(x-i)%35,y=1 if sid==0 else 4) for i in range(5)]
    return dict(id=sid,name=name,alive=True,body=body)

def game(kind="league",death_at=None,missing_after=None,
         silent_absence=None,turn_count=80):
    frames=[]
    for t in range(turn_count):
        if missing_after is not None and t>missing_after:
            break
        missing=silent_absence is not None and silent_absence<=t<=silent_absence+5
        respawn_delay=(death_at is not None and death_at<=t<=death_at+5)
        frames.append(dict(turn=t,
           snakes=[snake(0,PALMER,t,not (missing or respawn_delay)),
                   snake(1,"~benchmark" if kind=="trial" else "student-rival",t)],
           food=[dict(x=20,y=15)],
           events=[dict(kind="died",snake=0,cause=dict(kind="collision"))]
                   if death_at==t else []))
    return dict(header=dict(board=[35,35]),frames=frames)

def palmer0(replay,mode):
    rows,qc=observed_followup(replay,SEASON,"game.rep",mode,"hash-"+mode)
    return next(r for r in rows if r["student"]==PALMER and r["turn"]==0)

class LongHorizonTests(unittest.TestCase):
    def test_respawn_does_not_count_as_survival(self):
        row=palmer0(game(death_at=5),"league")
        self.assertEqual((row["status10"],row["status20"],row["status30"]),
                         ("dead","dead","dead"))
        self.assertNotIn(10,row["measurements"])
        self.assertNotIn(30,row["measurements"])
        self.assertEqual(row["death_next_10"],1)

    def test_death_after_first_ten_fails_later_horizons(self):
        row=palmer0(game(death_at=15),"league")
        self.assertEqual((row["status10"],row["status20"],row["status30"]),
                         ("alive","dead","dead"))
        self.assertEqual(row["measurements"][3]["exit_change"],
                         row["measurements"][3]["free_exits"]-row["free_exits"])
        self.assertIn(10,row["measurements"])
        self.assertNotIn(20,row["measurements"])

    def test_end_of_game_is_censored_not_safe(self):
        row=palmer0(game(turn_count=16),"league")
        self.assertEqual((row["status10"],row["status20"],row["status30"]),
                         ("alive","censored","censored"))
        self.assertEqual(row["continuous_followup"],15)

    def test_unexplained_absence_is_censored(self):
        row=palmer0(game(silent_absence=15),"league")
        self.assertEqual(row["status10"],"alive")
        self.assertEqual(row["status20"],"censored")
        self.assertEqual(row["status30"],"censored")
        self.assertEqual(row["continuous_followup"],14)

    def test_full_survival_requires_no_death_and_complete_frames(self):
        row=palmer0(game(),"league")
        self.assertEqual((row["status10"],row["status20"],row["status30"]),
                         ("alive","alive","alive"))
        self.assertIn(30,row["measurements"])
        self.assertEqual(row["first_action"]["movement"],"+x")
        self.assertEqual(row["first_action"]["turn_type"],"straight")
        c=survival_counts([row],"league")
        self.assertEqual(c["known30"],1)
        self.assertEqual(c["alive30"],1)
        self.assertEqual(c["censored30"],0)

    def test_survivors_by_exit_gain_never_include_dead_before_ten(self):
        death=palmer0(game(death_at=5),"league")
        alive=palmer0(game(),"league")
        classes=by_recovery([death,alive],"league")
        self.assertEqual(sum(v["total10"] for v in classes.values()),1)
        self.assertIsNone(recovery_label(death,3)) if 3 not in death["measurements"] else None

    def test_files_duplicate_and_modes_separate(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)
            root=base/"replays"/SEASON
            root.mkdir(parents=True)
            for name,r in (
                ("game-11.rep.gz",game()),
                ("game-12.rep.gz",game()),
                ("trials/a/trial-912000.rep.gz",game("trial",death_at=15))):
                path=root/name
                path.parent.mkdir(parents=True,exist_ok=True)
                with gzip.open(path,"wt",encoding="utf-8") as stream:
                    json.dump(r,stream)
            rows,qc=load(base)
            self.assertEqual(qc["unique_replays"],2)
            self.assertEqual(qc["replay_duplicates"],1)
            self.assertEqual(qc["league_unique_replays"],1)
            self.assertEqual(qc["trial_unique_replays"],1)
            summary=build(base)
            self.assertEqual(summary["replays"],2)
            self.assertEqual(summary["palmer_games"],1)
            self.assertEqual(summary["palmer_casebook"]["games"],1)
            self.assertTrue((base/"reports"/"palmer_casebook.md").is_file())
            with (base/"derived"/"palmer_league_casebook.csv").open(newline="") as f:
                casebook=list(csv.DictReader(f))
            self.assertEqual(casebook[0]["first_actual_move"],"+x")
            self.assertEqual(casebook[0]["first_move_style"],"straight")
            self.assertGreater(summary["league"]["survived10"],0)
            for filename in ("danger_survival_30.svg","escape_recovery_late_death.svg"):
                ElementTree.parse(base/"reports"/"charts"/filename)
            with (base/"derived"/"long_horizon_danger_windows.csv").open(newline="") as f:
                self.assertGreater(len(list(csv.DictReader(f))),0)
            self.assertIn("CENSORED",(base/"reports"/"long_horizon_survival.md").read_text())

    def test_replay_cluster_bootstrap_requires_independent_matches(self):
        r=palmer0(game(),"league")
        self.assertIsNone(cluster_bootstrap([r],"league"))
        self.assertEqual(outcome_status(0,0,{0:[(5,"collision")]},30,30),"dead")

if __name__=="__main__":
    unittest.main()
