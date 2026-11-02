"""Death autopsy: only real observed actions, matched starting risk, no leakage."""
import csv
import gzip
import json
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree

from research.escape_autopsy_core import (
    review_replay, load_autopsies, match_cases, paired_deltas,
    stable_target_food, strata,
)
from research.escape_autopsies import build, bootstrap_difference

S="2026-11-02-045859-season"

def snake(sid,name,t,alive=True):
    if not alive:
        return dict(id=sid,name=name,alive=False,body=[])
    x=(3+t)%35
    y=1 if sid==0 else 4
    body=[dict(x=(x-i)%35,y=y) for i in range(5)]
    return dict(id=sid,name=name,alive=True,body=body)

def game(mode="league",death_at=5):
    frames=[]
    for t in range(70):
        dead=death_at<=t<=death_at+5 if death_at is not None else False
        frames.append(dict(
            turn=t,
            snakes=[snake(0,"student-a",t,not dead),
                    snake(1,"~benchmark" if mode=="trial" else "student-b",t)],
            food=[dict(x=20,y=20)],
            events=([dict(kind="died",snake=0,
                         cause=dict(kind="head_to_head"))] if t==death_at else [])))
    return dict(header=dict(board=[35,35]),frames=frames)

class EscapeAutopsyTests(unittest.TestCase):
    def test_retrospective_death_and_actual_control(self):
        observations,quality=review_replay(
            game(),"season","game-1.rep","league","sha-league")
        self.assertEqual(quality["death_event_disagreement"],0)
        deaths=[x for x in observations if x["outcome"]=="death"]
        self.assertEqual(len(deaths),1)
        case=deaths[0]
        self.assertEqual(case["start_turn"],0)
        self.assertEqual(case["death_turn"],5)
        self.assertEqual(case["death_cause"],"head_to_head")
        self.assertIn(1,case["trajectory"])
        self.assertIn(3,case["trajectory"])
        self.assertNotIn(10,case["trajectory"])
        self.assertEqual(case["trajectory"][1]["displacement"],1)
        self.assertEqual(case["trajectory"][1]["stable_food_progress"],1)
        controls=[x for x in observations if x["outcome"]=="escape_10"]
        self.assertTrue(controls)
        pairs,unmatched=match_cases(observations)
        self.assertEqual(len(pairs),1)
        self.assertTrue(pairs[0]["same_replay"])
        self.assertEqual(pairs[0]["case"]["length_bin"],
                         pairs[0]["control"]["length_bin"])
        self.assertEqual(pairs[0]["case"]["head_pressure"],
                         pairs[0]["control"]["head_pressure"])
        self.assertEqual(pairs[0]["case"]["limited_exits"],
                         pairs[0]["control"]["limited_exits"])
        self.assertEqual(len(paired_deltas(pairs,"league",1,"exits_gain")),1)
        self.assertEqual(len(paired_deltas(pairs,"league",10,"exits_gain")),0)

    def test_death_next_turn_not_fabricated_as_no_motion(self):
        observations,_=review_replay(
            game(death_at=1),"season","game-1.rep","league","sha")
        pairs,_=match_cases(observations)
        self.assertEqual(len(pairs),1)
        self.assertNotIn(1,pairs[0]["case"]["trajectory"])
        self.assertEqual(paired_deltas(pairs,"league",1,"head_gain"),[])

    def test_mode_separation_and_missing_food_target(self):
        league,_=review_replay(game("league"),"s","a","league","sha-a")
        trial,_=review_replay(game("trial"),"s","b","trial","sha-b")
        pairs,_=match_cases(league+trial)
        self.assertEqual(len(pairs),2)
        self.assertEqual({pair["case"]["mode"] for pair in pairs},
                         {"league","trial"})
        self.assertTrue(all(pair["case"]["mode"]==pair["control"]["mode"]
                            for pair in pairs))
        before=dict(food=[dict(x=1,y=1)])
        after=dict(food=[dict(x=10,y=10)])
        self.assertIsNone(stable_target_food(before,after,(0,1),(1,1),35,35))

    def test_real_gz_dedup_csv_svg_reports(self):
        with tempfile.TemporaryDirectory() as t:
            base=Path(t)
            root=base/"replays"/S
            root.mkdir(parents=True)
            for name,value in (("game-101.rep.gz",game("league")),
                               ("game-102.rep.gz",game("league")),
                               ("trials/student-a/trial-910000.rep.gz",game("trial"))):
                path=root/name
                path.parent.mkdir(parents=True,exist_ok=True)
                with gzip.open(path,"wt",encoding="utf-8") as f:
                    json.dump(value,f)
            rows,quality=load_autopsies(base)
            self.assertEqual(quality["unique_replays"],2)
            self.assertEqual(quality["duplicate_replays"],1)
            report=build(base)
            self.assertEqual(report["matched_league"],1)
            self.assertEqual(report["matched_trial"],1)
            for name in ("escape_case_control.svg","escape_example_trace.svg"):
                ElementTree.parse(base/"reports"/"charts"/name)
            with (base/"derived"/"escape_matched_pairs.csv").open(newline="") as f:
                pairs=list(csv.DictReader(f))
            self.assertEqual(len(pairs),2)
            self.assertIn("RETROSPECTIVE",(
                base/"reports"/"escape_autopsies.md").read_text())

    def test_bootstrap_does_not_pretend_one_case_is_many_matches(self):
        pairs=[dict(case_sha="one-game",control_minus_case=1) for _ in range(200)]
        self.assertIsNone(bootstrap_difference(pairs))

if __name__=="__main__":
    unittest.main()
