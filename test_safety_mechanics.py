"""Synthetic regression tests for observed 2026 movement and collision audit."""
import gzip
import json
import tempfile
import unittest
from pathlib import Path
from research.safety_mechanics import audit_replay, build


def snake(sid, name, cells, alive=True):
    return dict(id=sid,name=name,alive=alive,
                body=[dict(x=x,y=y) for x,y in cells] if alive else [])


def replay(before,after,events=(),food=()):
    return dict(header=dict(board=[35,35]),frames=[
        dict(turn=0,snakes=before,food=[dict(x=x,y=y) for x,y in food],
             events=[]),
        dict(turn=1,snakes=after,food=[],events=list(events))])


class MechanicsAuditTests(unittest.TestCase):
    def test_head_wrap_one_step(self):
        r=replay([snake(1,"student",[(34,1),(33,1),(32,1)])],
                 [snake(1,"student",[(0,1),(34,1),(33,1)])])
        stats=audit_replay(r)
        self.assertEqual(stats["normal_one_step_heads"],1)
        self.assertEqual(stats["wrapped_steps"],1)

    def test_old_tail_entry_can_be_observed_surviving(self):
        before=[snake(1,"student",[(2,2),(2,3),(3,3),(3,2)])]
        after=[snake(1,"student",[(3,2),(2,2),(2,3),(3,3)])]
        counts=audit_replay(replay(before,after))
        self.assertEqual(counts["entered_old_own_tail"],1)
        self.assertEqual(counts["old_tail_still_occupied_after_move"],0)

    def test_recorded_head_to_head_victim_length(self):
        old=[snake(1,"student",[(2,2),(2,3),(2,4)]),
             snake(2,"peer",[(4,2),(4,3),(4,4),(4,5)])]
        new=[snake(1,"student",[],False),
             snake(2,"peer",[(3,2),(4,2),(4,3),(4,4)])]
        counts=audit_replay(replay(old,new,
            [dict(kind="died",snake=1,cause=dict(kind="head_to_head",by=2))]))
        self.assertEqual(counts["head_on_victim_shorter"],1)
        self.assertEqual(counts["recorded_deaths"],1)

    def test_eat_event_position_and_growth_delta(self):
        before=[snake(1,"student",[(2,2),(2,3)])]
        after=[snake(1,"student",[(3,2),(2,2),(2,3),(2,3)])]
        counts=audit_replay(replay(before,after,
                            [dict(kind="ate",snake=1)],[(3,2)]))
        self.assertEqual(counts["recorded_eating_survivors"],1)
        self.assertEqual(counts["ate_event_without_previous_food_cell"],0)
        self.assertEqual(counts["eating_length_delta_2"],1)

    def test_dedup_export(self):
        a=snake(1,"student",[(34,1),(33,1),(32,1)])
        b=snake(1,"student",[(0,1),(34,1),(33,1)])
        payload=json.dumps(replay([a],[b])).encode()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for season in ("a","b"):
                f=root/"replays"/season/"league-1.rep.gz"
                f.parent.mkdir(parents=True,exist_ok=True)
                with gzip.open(f,"wb") as z:z.write(payload)
            outcome=build(root)
            self.assertEqual(outcome["quality"]["league_unique_replays"],1)
            self.assertEqual(outcome["quality"]["duplicate_payloads"],1)
            self.assertIn("Surviving move into OWN old tail",
                          (root/"reports"/"safety_mechanics.md").read_text())

if __name__=="__main__":unittest.main()
