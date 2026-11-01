"""Tests: league and trials must never be conflated."""
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree
from collector import connect,ingest_latest_season,ingest_games
from research.league_core import build_data,spearman
from research.league_comparison import build

S="2026-11-01-205859-season"
LEADER="league-champion"
TRIAL="trial-champion"
A="third-student"
B="fourth-student"

def games():
    rows=[]
    for name,length in ((LEADER,80),(TRIAL,220),(A,160),(B,125)):
        for suite in ("910000","911000","912000"):
            rows.append(dict(replay="trials/"+name+"/trial-"+suite+".rep",kind="trial",
                seed=int(suite),kept=True,snakes=[
                    dict(name=name,placement=1,length=length,food=(length-5)//5,kills=3),
                    dict(name="~benchmark",placement=2,length=10,food=2,kills=0)]))
    rows.append(dict(replay="game-71000.rep",kind="league",division=1,seed=71000,
        kept=True,snakes=[
            dict(name=LEADER,placement=1,length=60,food=11,kills=1),
            dict(name=A,placement=2,length=40,food=7,kills=0),
            dict(name=B,placement=3,length=15,food=2,kills=0),
            dict(name="~benchmark",placement=4,length=5,food=0,kills=0)]))
    rows.append(dict(replay="game-72000.rep",kind="league",division=1,seed=72000,
        kept=True,snakes=[
            dict(name=A,placement=1,length=95,food=18,kills=1),
            dict(name=LEADER,placement=2,length=45,food=9,kills=0),
            dict(name=B,placement=3,length=30,food=5,kills=0),
            dict(name="~benchmark",placement=4,length=5,food=0,kills=0)]))
    rows.append(dict(replay="game-73000.rep",kind="league",division=2,seed=73000,
        kept=True,snakes=[
            dict(name=TRIAL,placement=1,length=90,food=17,kills=0),
            dict(name="~benchmark",placement=2,length=10,food=1,kills=0)]))
    return {"season":S,"games":rows}

def latest():
    names=[LEADER,A,B,TRIAL]
    return dict(name=S,meta={"created":"2026-11-01T20:00:00"},
        entrants=[{"name":n,"id":n,"sha256":"sha-"+n} for n in names],
        tables=[{"division":1,"table":[{"name":LEADER,"position":1},
                                       {"name":A,"position":2},{"name":B,"position":3}]},
                {"division":2,"table":[{"name":TRIAL,"position":13}]}],
        standings=[dict(name=n,division=1 if n!=TRIAL else 2,
                        games=6,wins=1,rating=1000,points=15) for n in names])

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.data=Path(self.tmp.name)
        db=connect(self.data/"snake.db")
        ingest_latest_season(db,latest())
        ingest_games(db,S,games())
        db.execute("UPDATE matches SET replay_sha256='sample' WHERE replay_name='game-71000.rep'")
        db.commit()
        db.close()

    def test_rank_mismatch_is_kept_explicit(self):
        db=connect(self.data/"snake.db")
        try:
            data=build_data(db)
            self.assertEqual(data["div1"][0],LEADER)
            self.assertEqual(data["trials"][TRIAL]["trial_rank"],1)
            self.assertEqual(data["trials"][LEADER]["trial_rank"],4)
            self.assertEqual(data["league"][LEADER]["league_games"],2)
            self.assertEqual(data["league"][LEADER]["league_wins"],1)
            self.assertEqual(data["league"][LEADER]["replay_games"],1)
            self.assertEqual(data["league"][A]["league_games"],2)
            self.assertTrue(any("mixed" in x for x in data["latest_kind"]))
            # Excludes the one-student league match for trial leader comparisons.
            self.assertNotIn(TRIAL,data["league"])
        finally:
            db.close()

    def test_comparison_figures_and_report(self):
        summary=build(self.data)
        self.assertEqual(summary["champion"],LEADER)
        self.assertEqual(summary["best_combined_trial"],TRIAL)
        self.assertEqual(summary["league_catalogs"],3)
        self.assertEqual(summary["league_replays"],1)
        for f in ("league_vs_trials.svg","league_replay_coverage.svg"):
            ElementTree.parse(self.data/"reports"/"charts"/f)
        doc=(self.data/"reports"/"league_vs_trials.md").read_text()
        self.assertIn("League champion",doc)
        self.assertIn("trial-champion",doc)
        self.assertIn("built-in filler",doc)

    def test_spearman_handles_ties(self):
        self.assertEqual(spearman([1,2,3,4],[1,2,3,4]),1)
        self.assertEqual(spearman([1,2,3,4],[4,3,2,1]),-1)
        self.assertIsNone(spearman([1,1,1,1],[1,2,3,4]))

if __name__=="__main__":
    unittest.main()
