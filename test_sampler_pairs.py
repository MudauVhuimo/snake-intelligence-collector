"""Replay sampler explicitly creates comparable student-season league+trial pairs."""
import tempfile
import unittest
from pathlib import Path

from collector import connect,ingest_latest_season,ingest_games,queued_matches,prioritize_paired_trials

S="2026-11-02-085859-season"

class PairedSamplerTests(unittest.TestCase):
    def test_pair_priority_covers_different_students_and_rotates_suites(self):
        students=["student-a","student-b","student-c","student-d"]
        unpaired=["trial-specialist"]
        candidates=[]
        owners={}
        for suite in ("912000","910000","911000"):
            for student in students+unpaired:
                pair=(S,f"trials/{student}/trial-{suite}.rep")
                candidates.append(pair)
                owners[pair]=student
        ordered=prioritize_paired_trials(
            candidates,owners,{(S,n) for n in students},set(),set())
        first_four=ordered[:4]
        self.assertEqual({owners[p] for p in first_four},set(students))
        self.assertGreaterEqual(len({p[1][-10:-4] for p in first_four}),2)
        self.assertNotIn("trial-specialist",{owners[p] for p in ordered[:12]})

    def test_archived_league_pair_beats_unrelated_and_existing_trial(self):
        candidates=[
            (S,"trials/unrelated/trial-910000.rep"),
            (S,"trials/covered/trial-910000.rep"),
            (S,"trials/uncoupled/trial-910000.rep"),
            (S,"trials/newly-paired/trial-910000.rep")]
        owners={p:p[1].split("/")[1] for p in candidates}
        order=prioritize_paired_trials(
            candidates,owners,{(S,"newly-paired")},
            {(S,"covered")},set())
        self.assertEqual(owners[order[0]],"newly-paired")
        self.assertEqual(owners[order[1]],"covered")

    def test_actual_queued_games_include_paired_trial_evidence(self):
        with tempfile.TemporaryDirectory() as root:
            data=Path(root)
            db=connect(data/"snake.db")
            names=["student-a","student-b","student-c","student-d"]
            ingest_latest_season(db,dict(name=S,meta={"created":"2026-11-02T08:00:00"},
                entrants=[dict(name=n,id=n,sha256=n) for n in names],
                standings=[dict(name=n,division=1,points=5,games=2,wins=1) for n in names],
                tables=[dict(division=1,table=[dict(name=n,position=i+1) for i,n in enumerate(names)])]))
            games=[]
            for i in range(6):
                games.append(dict(replay=f"game-7{i:04d}.rep",kind="league",
                    division=1,seed=70000+i,kept=True,
                    snakes=[dict(name=n,placement=k+1,length=45,food=8,kills=0)
                            for k,n in enumerate(names)]))
            for student in names+["unrelated-x","unrelated-y"]:
                for suite in ("910000","911000","912000"):
                    games.append(dict(replay=f"trials/{student}/trial-{suite}.rep",
                        kind="trial",kept=True,seed=int(suite),
                        snakes=[dict(name=student,placement=1,length=95,food=18,kills=0),
                                dict(name="~benchmark",placement=2,length=5,food=0,kills=0)]))
            ingest_games(db,S,{"season":S,"games":games})
            selection=queued_matches(db,data,[S],set(names),10)
            self.assertEqual(sum(p[1].startswith("game-") for p in selection),6)
            trial_students={p[1].split("/")[1] for p in selection if "/trial-" in p[1]}
            self.assertEqual(trial_students,set(names))
            db.close()

if __name__=="__main__":
    unittest.main()
