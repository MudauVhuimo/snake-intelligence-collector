"""Rank-gap studies compare the SAME eligible cohort and do not imply causation."""
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree
from research.seasonal_disagreement import study,svg_history,svg_extremes,save_csv

def cohort(season,omit=False):
    rows=[]
    for i in range(12):
        name=f"student-{i:02d}"
        if omit and i==8:
            continue
        rows.append(dict(
            season=season,team=name,official_division=1,official_rank=i+1,
            league_games=4,trial_complete=True,trial_mean_length=50+(i*13)%130,
            league_replays=1,trial_replays=1,
            league_mean_length=80-i*3,league_mean_food=30-i,
            league_mean_retention=.9-i*.02,trial_mean_retention=.4+i*.03,
            version_sha256=f"sha-{i//2}",
        ))
    return rows

class RankGapTests(unittest.TestCase):
    def test_same_group_ranks_and_no_fake_independence(self):
        rows=cohort("2026-11-01-100000-season")+cohort("2026-11-02-100000-season",True)
        groups,episodes=study(rows,minimum=10)
        self.assertEqual(len(groups),2)
        self.assertEqual(len(episodes),23)
        for e in episodes:
            self.assertLessEqual(abs(e["trial_minus_league"]),1)
            self.assertGreaterEqual(e["official_percentile"],0)
            self.assertLessEqual(e["official_percentile"],1)
        self.assertNotEqual(episodes[1]["official_rank"],episodes[1]["trial_rank"])

    def test_exclude_missing_or_non_peer_cohorts(self):
        rows=cohort("2026-11-01-100000-season")
        rows[2]["trial_complete"]=False
        rows[3]["league_games"]=1
        rows[4]["official_division"]=None
        groups,episodes=study(rows,minimum=10)
        self.assertEqual(groups,{})
        self.assertEqual(episodes,[])

    def test_render_historical_and_divergence_svg(self):
        groups,episodes=study(cohort("2026-11-01-100000-season"),minimum=10)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            svg_history(root/"trend.svg",list(groups.values()),"2026-11-01-100000-season")
            svg_extremes(root/"outliers.svg",episodes)
            save_csv(root/"student_season.csv",episodes)
            ElementTree.parse(root/"trend.svg")
            ElementTree.parse(root/"outliers.svg")
            self.assertEqual(len((root/"student_season.csv").read_text().splitlines()),13)

if __name__=="__main__":
    unittest.main()
