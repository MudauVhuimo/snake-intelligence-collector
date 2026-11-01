import gzip
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from collector import (connect, ingest_latest_season, ingest_games, install_replay,
                       analyze_replay, direction, collect, replay_location, safe_name, safe_replay_name, queued_matches)

S = "2026-11-01-195859-season"
A, B = "top-snake", "other-snake"


def latest():
    return {
        "name": S,
        "meta": {"created": "2026-11-01T20:08:24", "entrants": 2,
                 "rounds": 6, "config_hash": "abc"},
        "entrants": [
            {"name": A, "id": A, "language": "Java", "file": "Snake.java", "sha256": "hash-v1"},
            {"name": B, "id": B, "language": "Python", "file": "snake.py", "sha256": "hash-b"},
        ],
        "standings": [{"name": A, "division": 1, "rating": 1000,
                       "games": 10, "wins": 4, "points": 20}],
        "tables": [{"division": 1, "table": [{"name": A, "position": 1}]}],
    }


def games():
    return {"season": S, "games": [
        {"replay": "game-123.rep", "round": 1, "division": 1, "seed": 123,
         "map_id": "arena", "turns": 2000, "winner": A, "kept": True,
         "snakes": [{"name": A, "placement": 1, "length": 10, "food": 1,
                     "kills": 0, "turns": 2000},
                    {"name": B, "placement": 2, "length": 5, "food": 0,
                     "kills": 0, "turns": 2000}]}
    ]}


def mk_snake(slot, name, body, alive=True):
    return {"id": slot, "name": name, "body": [{"x": x, "y": y} for x, y in body],
            "alive": alive, "latency_ms": 1.2}


def replay():
    # wraps x=4 -> x=0 on 5x5 board (heading RIGHT)
    # then turns DOWN to x=0,y=1 and eats food; B dies and respawns
    return {"header": {"board": [5, 5], "roster": [A, B]}, "total_frames": 4,
            "frames": [
                {"turn": 0, "snakes": [mk_snake(0, A, [(4, 0), (3, 0)]),
                                          mk_snake(1, B, [(1, 1), (2, 1)])], "events": []},
                {"turn": 1, "snakes": [mk_snake(0, A, [(0, 0), (4, 0)]),
                                          mk_snake(1, B, [], False)],
                 "events": [{"turn": 1, "kind": "died", "snake": 1,
                             "cause": {"kind": "self_collision"}}]},
                {"turn": 2, "snakes": [mk_snake(0, A, [(0, 1), (0, 0)]),
                                          mk_snake(1, B, [(2, 4), (1, 4)])],
                 "events": [{"turn": 2, "kind": "ate", "snake": 0},
                            {"turn": 2, "kind": "respawned", "snake": 1}]},
                {"turn": 3, "snakes": [mk_snake(0, A, [(0, 2), (0, 1)]),
                                          mk_snake(1, B, [(3, 4), (2, 4)])], "events": []},
            ]}


class FakeClient:
    def __init__(self):
        self.requests = []
        self.replay_calls = 0
    def get_json(self, endpoint, params=None):
        self.requests.append((endpoint, params))
        if endpoint == "site":
            return {"season": {"name": S}, "seasons": [S]}
        if endpoint == "season":
            return latest()
        if endpoint == "games":
            return games()
        raise AssertionError(endpoint)
    def get_replay(self, name):
        self.replay_calls += 1
        self.requests.append(("replay", name))
        return json.dumps(replay()).encode()


class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.db = connect(self.root / "snake.db")
    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def test_nested_trial_replay_paths_and_catalog(self):
        trial="trials/top-snake/trial-912000.rep"
        self.assertEqual(safe_replay_name(trial),trial)
        for bad in ("../escape.rep","trials/../evil.rep","/trials/x.rep",
                    "trials//x.rep","trials/secret\\x.rep","trials/x.json"):
            with self.assertRaises(ValueError):
                safe_replay_name(bad)
        self.assertEqual(replay_location(self.root,S,trial),
                         self.root/"replays"/S/"trials"/"top-snake"/"trial-912000.rep.gz")
        catalog={"season":S,"games":[{
            "replay":trial,"kind":"trial","label":"top-snake on arrival",
            "round":None,"division":None,"seed":912000,"kept":True,
            "snakes":[{"name":A,"placement":1,"length":25,"food":4,"kills":0,"turns":2000},
                      {"name":"~gauntlet_1","placement":2,"length":5,"food":0,"kills":0,"turns":2000}]}]}
        ingest_games(self.db,S,catalog)
        data=self.db.execute("SELECT kind,label FROM matches WHERE replay_name=?",(trial,)).fetchone()
        self.assertEqual(data,("trial","top-snake on arrival"))
        chosen=queued_matches(self.db,self.root,[S],{A},3)
        self.assertEqual(chosen,[(S,trial)])
        self.assertEqual(self.db.execute("SELECT catalog_version FROM seasons WHERE name=?",(S,)).fetchone()[0],2)

    def test_validation_and_torus(self):
        for name in ("../secret", "foo/bar", "..", "x?z"):
            with self.assertRaises(ValueError):
                safe_name(name)
        self.assertEqual(direction({"x": 4, "y": 0}, {"x": 0, "y": 0}, 5, 5), "RIGHT")
        self.assertEqual(direction({"x": 0, "y": 0}, {"x": 0, "y": 4}, 5, 5), "UP")

    def test_actions_and_respawn_exclusion(self):
        metrics, events = analyze_replay(replay())
        self.assertEqual(metrics[A]["observed_moves"], 3)
        self.assertEqual(metrics[A]["straight_moves"], 2)
        self.assertEqual(metrics[A]["right_turns"], 1)
        self.assertEqual(metrics[A]["food_events"], 1)
        self.assertEqual(metrics[B]["deaths"], 1)
        self.assertEqual(metrics[B]["self_collisions"], 1)
        self.assertEqual(metrics[B]["observed_moves"], 1)  # excludes teleport from death to respawn
        self.assertEqual(len(events), 3)

    def test_ingest_and_bot_hash_changes(self):
        ingest_latest_season(self.db, latest())
        ingest_games(self.db, S, games())
        slot = self.db.execute("SELECT slot FROM participants WHERE team_slug=?", (A,)).fetchone()[0]
        self.assertIsNone(slot)
        v2 = latest()
        v2["entrants"][0]["sha256"] = "hash-v2"
        ingest_latest_season(self.db, v2)
        self.assertEqual(self.db.execute("SELECT sha256 FROM team_versions WHERE team_slug=?", (A,)).fetchone()[0], "hash-v2")
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM teams").fetchone()[0], 2)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM matches").fetchone()[0], 1)

    def test_replay_and_repeat_runs(self):
        cli = FakeClient()
        first = collect(cli, self.db, self.root, max_replays=6, lookback=1)
        self.assertEqual(first["downloaded"], 1)
        target = replay_location(self.root, S, "game-123.rep")
        self.assertTrue(target.exists())
        with gzip.open(target, "rb") as f:
            self.assertEqual(json.load(f)["header"]["board"], [5, 5])
        self.assertEqual(self.db.execute("SELECT slot FROM participants WHERE team_slug=?", (A,)).fetchone()[0], 0)
        self.assertEqual(self.db.execute("SELECT deaths FROM participants WHERE team_slug=?", (B,)).fetchone()[0], 1)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM behavior").fetchone()[0], 2)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM events").fetchone()[0], 3)
        # Catalog is checked again, but replay isn't re-downloaded.
        second = collect(cli, self.db, self.root, max_replays=6, lookback=1)
        self.assertEqual(second["downloaded"], 0)
        self.assertEqual(cli.replay_calls, 1)
        self.assertIn("Downloaded replays", (self.root / "reports/latest.md").read_text())

    def test_recover_after_db_write_interrupted(self):
        cli = FakeClient()
        collect(cli, self.db, self.root, max_replays=6, lookback=1)
        self.db.execute("UPDATE matches SET replay_sha256=NULL WHERE season_name=?", (S,))
        self.db.commit()
        again = collect(cli, self.db, self.root, max_replays=6, lookback=1)
        self.assertEqual(again["downloaded"], 1)
        self.assertEqual(cli.replay_calls, 1)  # loaded disk archive, no new network request

    def test_history_gets_part_of_download_budget(self):
        ingest_latest_season(self.db, latest())
        ingest_games(self.db, S, games())
        old = "2026-10-31-195859-season"
        old_games = {"season": old, "games": []}
        for i in range(4):
            row = games()["games"][0].copy()
            row["replay"] = f"old-{i}.rep"
            old_games["games"].append(row)
        ingest_games(self.db, old, old_games)
        recent_games = {"season": S, "games": []}
        for i in range(6):
            row = games()["games"][0].copy()
            row["replay"] = f"new-{i}.rep"
            recent_games["games"].append(row)
        ingest_games(self.db, S, recent_games)
        picked = queued_matches(self.db, self.root, [S, old], {A}, 6)
        self.assertEqual(sum(1 for season, _ in picked if season == old), 2)
        self.assertEqual(sum(1 for season, _ in picked if season == S), 4)

    def test_failed_replay_is_retryable(self):
        cli = FakeClient()
        def bad(name):
            cli.replay_calls += 1
            return b'not json'
        cli.get_replay = bad
        res = collect(cli, self.db, self.root, max_replays=6, lookback=1)
        self.assertEqual(res["downloaded"], 0)
        self.assertIsNone(self.db.execute("SELECT replay_sha256 FROM matches").fetchone()[0])
        self.assertFalse(replay_location(self.root, S, "game-123.rep").exists())


if __name__ == "__main__":
    unittest.main()
