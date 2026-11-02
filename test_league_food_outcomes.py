"""Tie-break study tests: no future action leakage and whole-match resampling."""
import csv
import tempfile
import unittest
from pathlib import Path
from research.league_food_outcomes import score, summarize, build


def episode(sha="game", gap=0, lengths=(10, 20), winner="tied_second",
            status="confirmed", steps=("farther", "closer")):
    return dict(sha=sha, gap=str(gap), nearest_length=str(lengths[0]),
                second_length=str(lengths[1]), status=status,
                winner_class=winner, nearest_step=steps[0],
                second_step=steps[1])


class LeagueFoodOutcomesTests(unittest.TestCase):
    def test_length_tiebreak_rewards_longer_on_equal_distance(self):
        short = episode()
        self.assertEqual(score(short), (0.5, 1.0))
        long = episode(lengths=(40, 5), winner="tied_first")
        self.assertEqual(score(long), (0.5, 1.0))
        equal = episode(lengths=(10, 10), winner="tied_first")
        self.assertEqual(score(equal), (0.5, 0.5))

    def test_distance_priority_ignores_length_if_not_tied(self):
        r = episode(gap=1, lengths=(5, 100), winner="nearest")
        self.assertEqual(score(r), (1.0, 1.0))
        r["winner_class"] = "second"
        self.assertEqual(score(r), (0.0, 0.0))

    def test_third_party_winner_scores_zero_for_both(self):
        self.assertEqual(score(episode(winner="other")), (0.0, 0.0))

    def test_no_data_leakage_from_post_action_movement(self):
        a = episode(steps=("closer", "farther"))
        b = episode(steps=("farther", "closer"))
        self.assertEqual(score(a), score(b))

    def test_unconfirmed_outcome_not_scored(self):
        with self.assertRaises(ValueError):
            score(episode(status="censored_40"))

    def test_bootstrap_uses_games_and_is_repeatable(self):
        r = [episode("A"), episode("A"), episode("B", lengths=(10,20),
             winner="tied_first"), episode("B", gap=1, winner="nearest"),
             episode("C", status="censored_40")]
        first = summarize(r, draws=200, seed=42)
        second = summarize(r, draws=200, seed=42)
        self.assertEqual(first["confirmed"], 4)
        self.assertEqual(first["unique_replays"], 2)
        self.assertEqual(first["ci_low"], second["ci_low"])
        self.assertEqual(first["ci_high"], second["ci_high"])

    def test_csv_report(self):
        rows = [episode("A"), episode("B", gap=1, winner="nearest"),
                episode("C", status="censored_40")]
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            csvpath=root/"derived"/"league_food_contests.csv"
            csvpath.parent.mkdir(parents=True)
            with csvpath.open("w",newline="") as f:
                writer=csv.DictWriter(f,fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            result=build(root,draws=50)
            self.assertEqual(result["confirmed"],2)
            self.assertIn("pre-action prediction check",
                          (root/"reports"/"league_food_prediction.md").read_text())


if __name__=="__main__":
    unittest.main()
