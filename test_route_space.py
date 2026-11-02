"""Route-space methods: wraparound, own-tail dynamics and no future leakage."""
from __future__ import annotations
import csv,gzip,hashlib,json,sqlite3,tempfile,unittest
from pathlib import Path
from xml.etree import ElementTree

from research.route_space_core import (
    Scene,adjacent,step_body,candidate_moves,frozen_area,
    scene_metrics,tail_reachable,rank_choice,validate_plain_transition,
    scene_from_frame
)
from research.route_space import (
    extract,build,auc,eval_records,holdout,cohort_metrics,pair_contrast
)

SEASON="2026-11-02-045859-season"

def body(sid,t,student=True):
    x=(3+t)%7
    y=1 if student else 4
    return [dict(x=(x-i)%7,y=y) for i in range(4)]

def game(kind="league"):
    frames=[]
    for t in range(40):
        frames.append(dict(turn=t,food=[dict(x=6,y=6)],obstacles=[],
            snakes=[dict(id=0,name="student-01",alive=True,body=body(0,t)),
                    dict(id=1,name="~benchmark" if kind=="trial" else "student-16",
                         alive=True,body=body(1,t,False))],
            events=[]))
    return dict(header=dict(board=[7,7]),frames=frames)

def make_data(data,kind="league"):
    (data/"derived").mkdir(parents=True,exist_ok=True)
    (data/"replays"/SEASON).mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(data/"snake.db") as db:
        db.execute("CREATE TABLE standings(season_name TEXT,team_slug TEXT,"
                   "division INTEGER,division_rank INTEGER)")
        db.executemany("INSERT INTO standings VALUES (?,?,?,?)",
                       [(SEASON,f"student-{i:02d}",1,i) for i in range(1,17)])
        db.commit()
    g=game(kind)
    raw=json.dumps(g,sort_keys=True).encode()
    sha=hashlib.sha256(raw).hexdigest()
    name=f"{SEASON}/game-001.rep.gz"
    path=data/"replays"/name
    with gzip.open(path,"wb") as file:file.write(raw)
    rows=[dict(season=SEASON,mode=kind,replay_sha=sha,
       replay=name,student="student-01",turn=0,length=4,
       length_band="5-24",nearest_head=3,free_exits=2,
       outcome10="alive",outcome20="alive",outcome30="alive")]
    with (data/"derived"/"long_horizon_danger_windows.csv").open(
        "w",newline="",encoding="utf-8") as file:
        writer=csv.DictWriter(file,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return g

class RouteTests(unittest.TestCase):
    def test_wraparound_neighbors_and_own_tail(self):
        self.assertEqual(adjacent((0,0),7,7),((1,0),(6,0),(0,1),(0,6)))
        start=((0,0),(0,1),(1,1),(1,0))
        self.assertIsNone(step_body(start,(0,1),frozenset()))
        moved=step_body(start,(1,0),frozenset())
        self.assertEqual(moved,((1,0),(0,0),(0,1),(1,1)))
        self.assertEqual(len(moved),4)

    def test_frozen_region_is_different_from_own_tail_continuation(self):
        body=((1,1),(1,2),(2,2),(2,1))
        area={x for x in range(7) for y in range(7)
              if (x,y) not in {(1,1),(1,2),(2,2),(2,1),(0,1)}}
        scene=Scene(7,7,body,frozenset(area),frozenset())
        options=scene_metrics(scene,horizon=8,beam=24)
        self.assertIn((2,1),[x["next_head"] for x in options])
        self.assertNotIn((1,2),[x["next_head"] for x in options])
        self.assertTrue(all(x["tail"]>=1 for x in options))
        self.assertTrue(all(x["frozen"]>=1 for x in options))
        # A current food sitting at a vacating tail changes growth
        # possibilities; do not pretend the no-growth tail entry is legal.
        food_scene=Scene(7,7,body,frozenset(area),frozenset({(2,1)}))
        self.assertNotIn((2,1),[x["next_head"] for x in scene_metrics(food_scene)])

    def test_legitimate_repeated_tail_coordinates_are_not_dropped(self):
        g=game()
        original=g["frames"][0]["snakes"][0]["body"]
        # During +5 food growth, tail stays in place across several frames.
        original.append(dict(original[-1]))
        original.append(dict(original[-1]))
        scene=scene_from_frame(g,g["frames"][0],0)
        self.assertIsNotNone(scene)
        self.assertEqual(len(scene.own),6)
        # The repeated tail is still blocked after a single pop.
        self.assertIsNone(step_body(scene.own,scene.own[-1],scene.others))
        # Duplicating an internal body point is NOT a normal growth suffix.
        original.insert(1,dict(original[1]))
        self.assertIsNone(scene_from_frame(g,g["frames"][0],0))

    def test_midrank_on_tied_options_and_missing_actual_head(self):
        paths=[dict(next_head=(0,0),frozen=5,tail=10),
               dict(next_head=(1,0),frozen=5,tail=6),
               dict(next_head=(2,0),frozen=1,tail=6)]
        r=rank_choice(paths,(1,0),"frozen")
        self.assertAlmostEqual(r["rank"],2/3)
        self.assertTrue(r["top"])
        self.assertIsNone(rank_choice(paths,(9,9),"tail"))
        self.assertFalse(rank_choice(paths,(1,0),"tail")["top"])

    def test_plain_shift_and_replay_future_not_read_for_scene(self):
        g=game()
        frame=g["frames"][0]
        scene=scene_from_frame(g,frame,0)
        opts=scene_metrics(scene)
        g["frames"][1]["snakes"][0]["body"][0]["x"]=6
        self.assertEqual(opts,scene_metrics(scene))
        b=((3,1),(2,1),(1,1),(0,1))
        self.assertTrue(validate_plain_transition(b,((4,1),)+b[:-1],False))
        self.assertFalse(validate_plain_transition(b,((4,1),)+b[:-2]+((6,1),),False))
        self.assertIsNone(validate_plain_transition(b,b,True))

    def test_replay_pipeline_and_svg(self):
        with tempfile.TemporaryDirectory() as tmp:
            data=Path(tmp)
            make_data(data)
            rows,qc=extract(data)
            self.assertEqual(len(rows),1)
            self.assertEqual(qc["plain_shift_checked"],1)
            self.assertEqual(qc["plain_shift_valid"],1)
            self.assertEqual(rows[0]["cohort"],"top_quartile")
            self.assertTrue(rows[0]["actual_move_observed"])
            self.assertGreater(rows[0]["best_frozen"],0)
            self.assertGreater(rows[0]["best_tail"],0)
            result=build(data)
            self.assertEqual(result["replays"],1)
            self.assertEqual(result["modeled_windows"],1)
            self.assertTrue((data/"reports"/"route_space.md").is_file())
            ElementTree.parse(data/"reports"/"charts"/"route_choice_cohorts.svg")
            with (data/"derived"/"route_choice_windows.csv").open() as f:
                self.assertEqual(len(list(csv.DictReader(f))),1)

    def test_auc_and_same_replay_bootstrap_guard(self):
        sample=[dict(death10="dead",free_exits=1,best_frozen=1,best_tail=1),
                dict(death10="alive",free_exits=3,best_frozen=10,best_tail=8)]
        r=eval_records(sample)
        self.assertEqual(r["free_exits"],1)
        self.assertEqual(r["best_frozen"],1)
        a=dict(replay_sha="shasame",chosen_tail_rank=0.8)
        b=dict(replay_sha="shasame",chosen_tail_rank=0.1)
        pair=pair_contrast([(a,b)],"chosen_tail_rank")
        self.assertEqual(pair["pairs"],1)
        self.assertIsNone(pair["low"])

if __name__=="__main__":
    unittest.main()
