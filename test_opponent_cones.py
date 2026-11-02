"""Opponents' possible next-head positions: mechanics and observational guardrails."""
import csv
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree

from research.opponent_cone_core import (
    opponent_cones,summarize_candidates,candidate_profile,
    actual_choice_risk,check_opponent_next_heads,
    audit_next_head_death,head_to_head_lengths
)
from research.opponent_cones import (
    read_rows,counts,risk_auc,spearman,paired_student_modes,bootstrap_auc,build
)
from research.route_space import build as build_routes,extract as extract_routes
from test_route_space import make_data

def snake(sid,name,head,neck,more=()):
    body=[dict(x=x,y=y) for x,y in (head,neck,*more)]
    return dict(id=sid,name=name,alive=True,body=body)

class OpponentConesTests(unittest.TestCase):
    def test_wraparound_heading_and_no_reverse(self):
        frame=dict(snakes=[
            snake(0,"focal",(10,10),(9,10)),
            snake(1,"opponent",(0,0),(34,0))
        ])
        cones=opponent_cones(frame,0,35,35)
        self.assertEqual(cones[1]["reaches"],
                         frozenset({(1,0),(0,1),(0,34)}))
        self.assertNotIn((34,0),cones[1]["reaches"])
        self.assertTrue(cones[1]["known_heading"])

    def test_unknown_heading_marks_four_not_three(self):
        frame=dict(snakes=[
            snake(0,"focal",(7,7),(6,7)),
            dict(id=2,name="opponent",alive=True,body=[dict(x=0,y=0)])
        ])
        c=opponent_cones(frame,0,35,35)
        self.assertFalse(c[2]["known_heading"])
        self.assertEqual(len(c[2]["reaches"]),4)

    def test_contact_flag_is_not_a_head_on_death_claim(self):
        frame=dict(snakes=[
            snake(0,"focal",(10,10),(9,10),[(8,10)]),
            snake(1,"long rival",(12,10),(13,10),
                  [(14,10),(15,10),(16,10)]),
            snake(2,"short rival",(10,12),(10,13))
        ])
        cones=opponent_cones(frame,0,35,35)
        choices=[
            dict(next_head=(11,10),tail=20,frozen=80),
            dict(next_head=(10,11),tail=15,frozen=70),
            dict(next_head=(9,10),tail=5,frozen=50),
        ]
        results=summarize_candidates(choices,cones,3)
        self.assertTrue(results[0]["head_cone"])
        self.assertTrue(results[0]["nonweaker_cone"])
        self.assertFalse(results[1]["nonweaker_cone"])
        self.assertTrue(results[1]["head_cone"])
        self.assertFalse(results[2]["head_cone"])
        p=candidate_profile(results)
        self.assertEqual(p["threatened_count"],2)
        self.assertEqual(p["uncontested_count"],1)
        self.assertEqual(p["best_uncontested_tail"],5)
        self.assertTrue(p["tail_best_requires_cone"])
        self.assertEqual(actual_choice_risk(results,(11,10))["chosen_cone"],True)
        self.assertFalse(actual_choice_risk(results,None)["observed"])
        self.assertFalse(actual_choice_risk(results,(20,20))["observed"])

    def test_prediction_validation_excludes_death_respawn(self):
        frame=dict(snakes=[
            snake(0,"focal",(10,10),(9,10)),
            snake(1,"rival",(0,0),(34,0))
        ])
        cone=opponent_cones(frame,0,35,35)
        forward=dict(snakes=[snake(1,"rival",(1,0),(0,0))])
        ok=check_opponent_next_heads(cone,forward,set())
        self.assertEqual(ok["opponent_next_within_cone"],1)
        reverse=dict(snakes=[snake(1,"rival",(34,0),(0,0))])
        wrong=check_opponent_next_heads(cone,reverse,set())
        self.assertEqual(wrong["opponent_next_outside_cone"],1)
        excluded=check_opponent_next_heads(cone,reverse,{1})
        self.assertEqual(excluded["opponent_next_checked"],0)
        self.assertEqual(excluded["opponent_dead"],1)
        self.assertEqual(audit_next_head_death(dict(events=[
            dict(kind="died",snake=0,cause=dict(kind="head_to_head",by=1))
        ]),0),"head_to_head")
        self.assertEqual(audit_next_head_death(None,0),"censored")

    def test_head_to_head_length_is_observation_not_resolution(self):
        before=dict(snakes=[
            snake(0,"victim",(1,1),(0,1)),
            snake(1,"rival",(3,1),(4,1),[(5,1),(6,1)])
        ])
        event=dict(kind="died",snake=0,cause=dict(kind="head_to_head",by=1))
        self.assertEqual(head_to_head_lengths(before,event)["relation"],
                         "victim_shorter")
        event["cause"]["by"]=40
        self.assertEqual(head_to_head_lengths(before,event)["relation"],
                         "missing_participant")
        self.assertIsNone(head_to_head_lengths(before,dict(
            kind="died",snake=0,cause=dict(kind="collision",by=1))))

    def test_end_to_end_separates_modes_and_missing_replay_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            data=Path(tmp)
            make_data(data)
            route=build_routes(data)
            self.assertEqual(route["modeled_windows"],1)
            self.assertTrue((data/"derived"/"route_cone_quality.json").exists())
            rows=read_rows(data)
            self.assertEqual(len(rows),1)
            self.assertEqual(rows[0]["mode"],"league")
            self.assertEqual(rows[0]["opponent_heads"],1)
            results=build(data)
            self.assertEqual(results["league_windows"],1)
            self.assertEqual(results["trial_windows"],0)
            self.assertTrue((data/"reports"/"opponent_cones.md").is_file())
            ElementTree.parse(data/"reports"/"charts"/"opponent_contests.svg")
            with (data/"derived"/"opponent_cone_cohorts.csv").open() as f:
                self.assertEqual(len(list(csv.DictReader(f))),8)
        with tempfile.TemporaryDirectory() as tmp:
            report=build(Path(tmp))
            self.assertEqual(report["league_windows"],0)
            self.assertIn("insufficient",(Path(tmp)/"reports"/"opponent_cones.md").read_text())

    def test_conditional_shorter_opportunity_rate_prevents_overinterpretation(self):
        base=dict(replay_sha="one",student="student-1",
                  candidate_count=2,death10="alive",
                  first_step_death_cause="no_recorded_death",
                  length=100,all_cone=False,
                  chosen_cone=False,chosen_nonweaker_cone=False)
        options=[
            dict(base,student="student-a",threatened_count=1,
                 nonweaker_threatened_count=0,
                 chosen_cone=True,chosen_nonweaker_cone=False),
            dict(base,student="student-b",threatened_count=1,
                 nonweaker_threatened_count=1,
                 chosen_cone=False,chosen_nonweaker_cone=False),
        ]
        result=counts(options)
        self.assertEqual(result["shorter_opportunity_choices"],1)
        self.assertEqual(result["shorter_only_selected"],1)
        self.assertEqual(result["pct_shorter_selected"],100.0)
        self.assertEqual(result["observed_moves"],2)

    def test_holdout_uncertainty_requires_multiple_games(self):
        rows=[
            dict(death10="dead",free_exits=1,best_tail=2,
                 best_uncontested_tail=0,replay_sha="sample"),
            dict(death10="alive",free_exits=3,best_tail=10,
                 best_uncontested_tail=9,replay_sha="sample")
        ]
        self.assertEqual(risk_auc(rows,"free_exits"),1)
        self.assertIsNone(bootstrap_auc(rows,"best_tail","free_exits")["low"])
        self.assertIsNone(spearman([(1,1),(2,2)]))
        self.assertIsNone(spearman([(1,1),(1,2),(1,3),(1,4)]))

if __name__=="__main__":
    unittest.main()
