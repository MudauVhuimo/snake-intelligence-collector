"""Deterministic audit of peer-league apple contests and censoring."""
import gzip
import json
import tempfile
import unittest
from pathlib import Path

from research.league_food_contests import analyze_replay, build, scan


def snake(sid, name, x, y, alive=True):
    return dict(id=sid, name=name, alive=alive,
                body=[dict(x=x, y=y)]*5 if alive else [])


def example(ate=True, died=False, one_student=False, far=False):
    palmer = "421462-alexander-palmer"
    peer = "~benchmark" if one_student else "peer"
    before = dict(turn=0, snakes=[
        snake(1, palmer, 1, 1),
        snake(2, peer, 20 if far else 3, 20 if far else 1)],
        food=[dict(x=2, y=1)], events=[])
    after = dict(turn=1, snakes=[
        snake(1, palmer, 2, 1, alive=not died), snake(2, peer, 3, 2)],
        food=[], events=([dict(kind="died", snake=1)] if died else
                         [dict(kind="ate", snake=1)] if ate else []))
    return dict(header=dict(board=[35, 35]), frames=[before, after])


class LeagueFoodContestsTests(unittest.TestCase):
    def test_palmer_capture_requires_two_signals(self):
        rows, counts = analyze_replay(example(), "s", "s/game.rep.gz", "sha")
        self.assertEqual(len(rows), 1)
        self.assertEqual(counts["confirmed"], 1)
        self.assertEqual(rows[0]["winner_class"], "tied_first")
        self.assertEqual(rows[0]["nearest_step"], "closer")
        self.assertEqual(rows[0]["winner"], "421462-alexander-palmer")
        self.assertEqual(rows[0]["palmer_result"], "captured")

    def test_missing_ate_event_does_not_assign_capture(self):
        rows, _ = analyze_replay(example(ate=False), "s", "g", "sha")
        self.assertEqual(rows[0]["status"], "unverified_disappearance")
        self.assertEqual(rows[0]["winner"], "")
        self.assertEqual(rows[0]["palmer_result"], "unresolved")

    def test_first_turn_death_remains_in_denominator(self):
        rows, _ = analyze_replay(example(died=True), "s", "g", "sha")
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0]["nearest_first_death"])
        self.assertEqual(rows[0]["nearest_step"], "died")

    def test_benchmark_only_second_participant_excluded(self):
        rows, quality = analyze_replay(example(one_student=True), "s", "g", "sha")
        self.assertEqual(rows, [])
        self.assertEqual(quality["excluded_not_peer_league"], 1)

    def test_distant_peer_not_a_close_contest(self):
        rows, _ = analyze_replay(example(far=True), "s", "g", "sha")
        self.assertEqual(rows, [])

    def test_unchanged_apple_after_40_turns_censors(self):
        replay = example()
        replay["frames"] = replay["frames"][:1]
        for t in range(1, 42):
            f = dict(turn=t, snakes=[snake(1, "421462-alexander-palmer", 1, 1),
                                      snake(2, "peer", 3, 1)],
                     food=[dict(x=2, y=1)], events=[])
            replay["frames"].append(f)
        rows, _ = analyze_replay(replay, "s", "g", "sha")
        self.assertEqual(rows[0]["status"], "censored_40")
        self.assertEqual(rows[0]["palmer_result"], "unresolved")

    def test_dedup_and_export(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            payload = json.dumps(example()).encode()
            for season in ("old", "new"):
                path = root / "replays" / season / "game.rep.gz"
                path.parent.mkdir(parents=True, exist_ok=True)
                with gzip.open(path, "wb") as f:
                    f.write(payload)
            events, quality = scan(root)
            self.assertEqual(len(events), 1)
            self.assertEqual(quality["unique_replays"], 1)
            self.assertEqual(quality["duplicate_replays"], 1)
            result = build(root)
            self.assertEqual(result["episodes"], 1)
            self.assertIn("Palmer captured **1**",
                          (root / "reports" / "league_food_contests.md").read_text())


if __name__ == "__main__":
    unittest.main()
