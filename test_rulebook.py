"""Registry ensures one named hypothesis cannot become a rule by rhetoric."""
import json
import tempfile
import unittest
from pathlib import Path

from research.rulebook import build,read_registry

RULE={
 "id":"SAFETY-01","title":"Check mechanics","stage":0,
 "domain":"mechanics","mode":"both","if_state":"Dangerous step",
 "then_hypothesis":"Exclude verified fatal moves",
 "evidence":[],"counterexample":"Moving tail",
 "next_experiment":"Validate official mechanics",
 "falsification":"Incorrect transition prediction"
}

class RulebookTests(unittest.TestCase):
    def test_existing_registry_is_valid_and_not_prematurely_promoted(self):
        r=read_registry(Path(__file__).parent/"research"/"rule_candidates.json")
        self.assertGreaterEqual(len(r),7)
        self.assertTrue(all(x["stage"]<=1 for x in r))
        self.assertEqual(len({x["id"] for x in r}),len(r))
        self.assertTrue(all(x["counterexample"] and x["falsification"] for x in r))

    def test_error_if_claimed_promotion_without_controlled_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            file=Path(tmp)/"rules.json"
            for stage in (2,3,4):
                rule=dict(RULE,stage=stage,evidence=["data/reports/threat_windows.md"])
                file.write_text(json.dumps(dict(version=1,rules=[rule])))
                with self.assertRaises(ValueError):
                    read_registry(file)

    def test_render_with_custom_registry_and_plain_markdown(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)
            reg=path/"hypotheses.json"
            reg.write_text(json.dumps(dict(version=1,rules=[RULE])))
            result=build(path,registry=reg)
            self.assertEqual(result["rules"],1)
            output=(path/"reports"/"algorithm_rulebook.md").read_text()
            self.assertIn("No stage automatically advances",output)
            self.assertIn("SAFETY-01",output)
            self.assertIn("Moving tail",output)
            self.assertIn("full research protocol".lower(),output.lower())

    def test_reject_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/"bad.json"
            path.write_text(json.dumps(dict(version=1,rules=[RULE,RULE])))
            with self.assertRaises(ValueError):
                read_registry(path)

if __name__=="__main__":
    unittest.main()
