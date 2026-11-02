"""Adaptive study tests: fixed strata, explicit death and no post-respawn food."""
import gzip
import json
import tempfile
import unittest
from pathlib import Path
from research.adaptive_context import (density_band,phase_band,occupied_fraction,
                                       observed_replay,build,summary)


def snake(sid,name,x,y,alive=True):
    return dict(id=sid,name=name,alive=alive,
                body=[dict(x=x,y=y)]*5 if alive else [])


def fixture():
    frames=[]
    for turn in range(12):
        dead=turn>=8
        events=[]
        if turn==3:events=[dict(kind="ate",snake=1)]
        if turn==8:events=[dict(kind="died",snake=1,cause=dict(kind="self"))]
        if turn==10:events=[dict(kind="ate",snake=1)]  # should NOT count
        frames.append(dict(turn=turn,snakes=[
            snake(1,"421462-alexander-palmer",1,1,alive=not dead),
            snake(2,"peer",8,8)],events=events,food=[]))
    return dict(header=dict(board=[35,35]),frames=frames)


class AdaptiveEvidenceTests(unittest.TestCase):
    def test_precommitted_bands(self):
        self.assertEqual(density_band(.149),"low_<15%")
        self.assertEqual(density_band(.15),"mid_15-30%")
        self.assertEqual(density_band(.30),"high_>=30%")
        self.assertEqual(phase_band(499),"early_0-499")
        self.assertEqual(phase_band(500),"middle_500-1499")
        self.assertEqual(phase_band(1500),"late_1500+")

    def test_occupied_deduplicates_body_cells(self):
        f=fixture()["frames"][0]
        self.assertEqual(occupied_fraction(f,35,35),2/(35*35))

    def test_10_turn_death_not_alive_after_respawn(self):
        r=fixture()
        rows,checks=observed_replay(r,"league","s","g","sha")
        self.assertEqual(len(rows),2)
        palmer=next(row for row in rows if row["is_palmer"])
        self.assertEqual(palmer["death_10"],1)
        self.assertEqual(palmer["food_10"],1)
        peer=next(row for row in rows if not row["is_palmer"])
        self.assertEqual(peer["death_10"],0)
        self.assertEqual(peer["food_10"],0)

    def test_no_incomplete_future_counted(self):
        r=fixture()
        # Keep >=11 payload frames, but remove a required intermediate turn.
        r["frames"]=[f for f in r["frames"] if f["turn"]!=5]
        rows,checks=observed_replay(r,"league","s","g","sha")
        self.assertEqual(rows,[])

    def test_summary_rates_and_games(self):
        r=fixture()
        rows,_=observed_replay(r,"league","s","g","sha")
        by=summary(rows,("mode",))
        self.assertEqual(by[0][1]["n"],2)
        self.assertEqual(by[0][1]["deaths"],1)
        self.assertEqual(by[0][1]["food"],1)
        self.assertEqual(by[0][1]["games"],1)

    def test_export_and_replay_hash_dedup(self):
        data=json.dumps(fixture()).encode()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for season in ("x","y"):
                path=root/"replays"/season/"game.rep.gz"
                path.parent.mkdir(parents=True,exist_ok=True)
                with gzip.open(path,"wb") as file:file.write(data)
            result=build(root)
            self.assertEqual(result["windows"],2)
            self.assertEqual(result["quality"]["duplicate_payloads"],1)
            self.assertIn("Palmer as reference subset",
                          (root/"reports"/"adaptive_context.md").read_text())

if __name__=="__main__":unittest.main()
