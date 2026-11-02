"""Strong/middle/weak competitive cohort research: no team singled out."""
import csv
import sqlite3
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree

from research.competitive_cohorts import (
    COHORTS, ranks, classify, matching_stratum, common_support,
    same_game_support, rates, build
)

SEASON="2026-11-02-045859-season"
PREVIOUS="2026-10-31-045859-season"

def fixture_database(db):
    db.execute("CREATE TABLE standings (season_name TEXT, team_slug TEXT, "
               "division INTEGER,division_rank INTEGER)")
    rows=[]
    for season in (SEASON,PREVIOUS):
        for i in range(1,17):
            rows.append((season,f"student-{i:02d}",1,
                         i if season==SEASON else 17-i))
    rows.append((SEASON,"division2-top",2,1))
    db.executemany("INSERT INTO standings VALUES (?,?,?,?)",rows)
    db.commit()

def window(season=SEASON,student="student-01",mode="league",sha="r1",
           turn="0",status="alive",confined=False):
    return dict(season=season,student=student,mode=mode,replay_sha=sha,
        replay=f"{season}/game-0001.rep.gz",turn=turn,
        length="30",length_band="25-49",nearest_head="2",
        first_move_style="turn",first_move_axis="+x",
        food_progress_same_apple1="1",
        free_exits="1" if confined else "3",outcome10=status,
        outcome20=status,outcome30=status,exit_gain3="1",apples10="1",
        apples30="2",head_distance_gain3="2")

class CohortTests(unittest.TestCase):
    def test_season_rank_never_carried_across_versions(self):
        with sqlite3.connect(":memory:") as db:
            fixture_database(db)
            ranked=ranks(db)
        self.assertEqual(ranked[SEASON,"student-01"]["cohort"],"top_quartile")
        self.assertEqual(ranked[PREVIOUS,"student-01"]["cohort"],"bottom_quartile")
        self.assertNotIn((SEASON,"division2-top"),ranked)

    def test_respect_mode_deduplicate_sha_and_censor(self):
        with sqlite3.connect(":memory:") as db:
            fixture_database(db)
            ranked=ranks(db)
        source=[
            window(sha="match1",student="student-01",status="dead"),
            window(sha="match1",student="student-01",status="dead"),
            window(sha="match1",student="student-16",status="alive"),
            window(sha="trial1",student="student-16",mode="trial"),
            window(sha="match2",student="division2-top"),
            window(sha="missing",student="student-03",status="censored")
        ]
        observed,qc=classify(source,ranked)
        self.assertEqual(len(observed),4)
        self.assertEqual(qc["duplicate_exposures"],1)
        self.assertEqual(qc["league_unmatched_rank"],1)
        self.assertEqual(rates(observed[:1])["deaths10"],1)
        self.assertEqual(rates(observed[-1:])["n10"],0)

    def test_common_strata_require_both_cohorts_same_mode(self):
        with sqlite3.connect(":memory:") as db:
            fixture_database(db)
            rank=ranks(db)
        source=[window(sha="A",student="student-01"),
                window(sha="A",student="student-16"),
                window(sha="B",student="student-16",mode="trial"),
                window(sha="C",student="student-15",confined=True)]
        data,_=classify(source,rank)
        common,qc=common_support(data)
        self.assertEqual(len(common),2)
        self.assertEqual(qc["common_strata"],1)
        shared=same_game_support(data)
        self.assertEqual(shared["both_extremes"],1)

    def test_report_and_svg_use_only_same_season_qualifiers(self):
        with tempfile.TemporaryDirectory() as path:
            data=Path(path)
            (data/"derived").mkdir()
            with sqlite3.connect(data/"snake.db") as db:
                fixture_database(db)
            source=[
                window(sha="match-a",student="student-01",status="dead"),
                window(sha="match-a",student="student-16",status="alive"),
                window(sha="trial-a",student="student-08",mode="trial"),
                window(PREVIOUS,student="student-01",sha="old-match"),
                window(sha="match-b",student="student-08"),
            ]
            with (data/"derived"/"long_horizon_danger_windows.csv").open(
                 "w",newline="",encoding="utf-8") as stream:
                writer=csv.DictWriter(stream,fieldnames=list(source[0]))
                writer.writeheader()
                writer.writerows(source)
            summary=build(data)
            self.assertEqual(summary["ranked_league_windows"],4)
            self.assertEqual(summary["ranked_trial_windows"],1)
            self.assertEqual(summary["same_match_extremes"],1)
            report=(data/"reports"/"competitive_cohorts.md").read_text()
            self.assertIn("NOT a study",report)
            self.assertIn("SAME replay season",report)
            ElementTree.parse(data/"reports"/"charts"/"cohort_danger_outcomes.svg")
            with (data/"derived"/"competitive_cohort_danger.csv").open(
                 newline="",encoding="utf-8") as stream:
                self.assertEqual(len(list(csv.DictReader(stream))),6)

if __name__=="__main__":
    unittest.main()
