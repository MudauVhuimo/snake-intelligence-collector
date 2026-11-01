#!/usr/bin/env python3
"""Wits Snake26 respectful, restart-safe metadata/replay collector.

Python 3.11+ standard library only. This project uses only public GET endpoints.
The reported API schema has not been independently verified from this environment.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path
import random
import re
import sqlite3
import tempfile
import time
from typing import Any
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://lamp.ms.wits.ac.za/snake26/api/"
USER_AGENT = "WitsSnakeResearchCollector/0.1 (+educational research; polite requests)"
NAME_RX = re.compile(r"^[A-Za-z0-9_.-]+$")
DIRECTIONS = {(1, 0): "RIGHT", (-1, 0): "LEFT", (0, 1): "DOWN", (0, -1): "UP"}
SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS seasons (
    name TEXT PRIMARY KEY, created TEXT, entrants INTEGER, rounds INTEGER,
    config_hash TEXT, recorded_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS teams (
    slug TEXT PRIMARY KEY, language TEXT, file_name TEXT,
    latest_sha256 TEXT, last_seen_season TEXT
);
CREATE TABLE IF NOT EXISTS team_versions (
    season_name TEXT NOT NULL REFERENCES seasons(name),
    team_slug TEXT NOT NULL REFERENCES teams(slug),
    sha256 TEXT NOT NULL, language TEXT,
    PRIMARY KEY (season_name, team_slug)
);
CREATE TABLE IF NOT EXISTS standings (
    season_name TEXT NOT NULL REFERENCES seasons(name),
    team_slug TEXT NOT NULL REFERENCES teams(slug),
    division INTEGER, division_rank INTEGER, rating REAL,
    points REAL, career_games INTEGER, career_wins INTEGER,
    PRIMARY KEY(season_name, team_slug)
);
CREATE TABLE IF NOT EXISTS matches (
    season_name TEXT NOT NULL REFERENCES seasons(name),
    replay_name TEXT NOT NULL, round_num INTEGER,
    division INTEGER, seed INTEGER, map_id TEXT, turns INTEGER,
    winner TEXT, kept INTEGER NOT NULL DEFAULT 1,
    kind TEXT NOT NULL DEFAULT 'league', label TEXT,
    replay_sha256 TEXT, replay_bytes INTEGER, downloaded_at TEXT,
    PRIMARY KEY(season_name, replay_name)
);
CREATE TABLE IF NOT EXISTS participants (
    season_name TEXT NOT NULL,
    replay_name TEXT NOT NULL,
    team_slug TEXT NOT NULL REFERENCES teams(slug),
    slot INTEGER, placement INTEGER, final_length INTEGER,
    max_length INTEGER, food_eaten INTEGER, kills INTEGER,
    deaths INTEGER, turns_survived INTEGER,
    PRIMARY KEY(season_name, replay_name, team_slug),
    FOREIGN KEY(season_name, replay_name) REFERENCES matches(season_name, replay_name)
);
CREATE TABLE IF NOT EXISTS events (
    season_name TEXT NOT NULL, replay_name TEXT NOT NULL,
    turn INTEGER NOT NULL, event_idx INTEGER NOT NULL,
    kind TEXT, snake_slot INTEGER, cause TEXT, killer_slot INTEGER,
    PRIMARY KEY(season_name, replay_name, turn, event_idx),
    FOREIGN KEY(season_name, replay_name) REFERENCES matches(season_name, replay_name)
);
CREATE TABLE IF NOT EXISTS behavior (
    season_name TEXT NOT NULL, replay_name TEXT NOT NULL,
    team_slug TEXT NOT NULL REFERENCES teams(slug),
    observed_moves INTEGER NOT NULL, straight_moves INTEGER NOT NULL,
    left_turns INTEGER NOT NULL, right_turns INTEGER NOT NULL,
    food_events INTEGER NOT NULL, deaths INTEGER NOT NULL,
    self_collisions INTEGER NOT NULL, body_collisions INTEGER NOT NULL,
    head_to_head_deaths INTEGER NOT NULL,
    avg_latency_ms REAL,
    PRIMARY KEY(season_name, replay_name, team_slug),
    FOREIGN KEY(season_name, replay_name) REFERENCES matches(season_name, replay_name)
);
CREATE INDEX IF NOT EXISTS idx_matches_division ON matches(division);
CREATE INDEX IF NOT EXISTS idx_participants_team ON participants(team_slug);
CREATE INDEX IF NOT EXISTS idx_standings_team ON standings(team_slug);
"""


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def safe_name(value: str) -> str:
    if not isinstance(value, str) or not NAME_RX.fullmatch(value) or value in (".", ".."):
        raise ValueError(f"Unsafe or invalid API identifier: {value!r}")
    return value


def safe_replay_name(value: str) -> str:
    """Allow structured trial replay paths, never traversal or arbitrary paths."""
    if not isinstance(value, str) or len(value) > 180:
        raise ValueError("Invalid replay identifier")
    parts = value.split("/")
    if not 1 <= len(parts) <= 4 or any(
        not NAME_RX.fullmatch(part) or part in (".", "..") for part in parts
    ):
        raise ValueError(f"Unsafe replay identifier: {value!r}")
    if not parts[-1].endswith(".rep"):
        raise ValueError("Expected .rep replay")
    return value


def checked_json(raw: bytes) -> dict[str, Any]:
    result = json.loads(raw)
    if not isinstance(result, dict):
        raise ValueError("Expected a JSON object")
    return result


class Client:
    def __init__(self, delay: float = 1.0, retries: int = 3):
        self.delay, self.retries = delay, retries
        self.last_request = 0.0

    def fetch(self, endpoint: str, params: dict[str, str] | None = None, timeout: int = 40) -> bytes:
        url = API_BASE + endpoint
        if params:
            url += "?" + urllib.parse.urlencode(params)
        for attempt in range(self.retries):
            elapsed = time.monotonic() - self.last_request
            if self.last_request and elapsed < self.delay:
                time.sleep(self.delay - elapsed)
            self.last_request = time.monotonic()
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    if resp.status != 200:
                        raise RuntimeError(f"HTTP {resp.status} from {endpoint}")
                    return resp.read()
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as exc:
                if isinstance(exc, urllib.error.HTTPError) and exc.code in (400, 401, 403, 404):
                    raise
                if attempt + 1 == self.retries:
                    raise
                wait = min(2 ** attempt * 2, 12) + random.uniform(0, 0.5)
                print(f"Retrying {endpoint} after {type(exc).__name__} ({wait:.1f}s)")
                time.sleep(wait)
        raise AssertionError("unreachable")

    def get_json(self, endpoint: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        return checked_json(self.fetch(endpoint, params))

    def get_replay(self, replay_name: str) -> bytes:
        return self.fetch("replay", {"name": safe_replay_name(replay_name)}, timeout=60)


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.execute("PRAGMA journal_mode=DELETE")  # safe when committing db file to git
    db.executescript(SCHEMA)
    # In-place migration of existing database and repair of incomplete old catalogs.
    columns = {row[1] for row in db.execute("PRAGMA table_info(matches)")}
    if "kind" not in columns:
        db.execute("ALTER TABLE matches ADD COLUMN kind TEXT NOT NULL DEFAULT 'league'")
    if "label" not in columns:
        db.execute("ALTER TABLE matches ADD COLUMN label TEXT")
    seasons_columns = {row[1] for row in db.execute("PRAGMA table_info(seasons)")}
    if "catalog_version" not in seasons_columns:
        db.execute("ALTER TABLE seasons ADD COLUMN catalog_version INTEGER NOT NULL DEFAULT 0")
    db.commit()
    return db


def ensure_team(db: sqlite3.Connection, slug: str) -> None:
    db.execute("INSERT OR IGNORE INTO teams(slug) VALUES (?)", (slug,))


def ensure_season(db: sqlite3.Connection, name: str) -> None:
    db.execute("INSERT OR IGNORE INTO seasons(name, recorded_at) VALUES (?, ?)", (name, utcnow()))


def ingest_latest_season(db: sqlite3.Connection, season: dict[str, Any]) -> None:
    name = safe_name(season["name"])
    meta = season.get("meta") or {}
    ensure_season(db, name)
    db.execute("""UPDATE seasons SET created=?, entrants=?, rounds=?, config_hash=? WHERE name=?""",
               (meta.get("created"), meta.get("entrants"), meta.get("rounds"), meta.get("config_hash"), name))
    for entry in season.get("entrants", []):
        slug = entry.get("id") or entry.get("name")
        if not slug:
            continue
        ensure_team(db, slug)
        db.execute("""UPDATE teams SET language=?, file_name=?, latest_sha256=?, last_seen_season=? WHERE slug=?""",
                   (entry.get("language"), entry.get("file"), entry.get("sha256"), name, slug))
        if entry.get("sha256"):
            db.execute("""INSERT INTO team_versions(season_name,team_slug,sha256,language)
                VALUES (?,?,?,?) ON CONFLICT(season_name,team_slug) DO UPDATE SET
                sha256=excluded.sha256, language=excluded.language""",
                       (name, slug, entry["sha256"], entry.get("language")))
    ranks = {}
    for table in season.get("tables", []):
        for member in table.get("table", []):
            ranks[member.get("name")] = (table.get("division"), member.get("position"))
    for item in season.get("standings", []):
        slug = item.get("name")
        if not slug:
            continue
        ensure_team(db, slug)
        division, rank = ranks.get(slug, (item.get("division"), None))
        db.execute("""INSERT INTO standings(season_name,team_slug,division,division_rank,rating,points,career_games,career_wins)
            VALUES (?,?,?,?,?,?,?,?) ON CONFLICT(season_name,team_slug) DO UPDATE SET
            division=excluded.division,division_rank=excluded.division_rank,
            rating=excluded.rating,points=excluded.points,career_games=excluded.career_games,
            career_wins=excluded.career_wins""",
                   (name, slug, division, rank, item.get("rating"), item.get("points"),
                    item.get("games"), item.get("wins")))
    db.commit()


def ingest_games(db: sqlite3.Connection, name: str, catalog: dict[str, Any]) -> int:
    ensure_season(db, name)
    count = 0
    for match in catalog.get("games", []):
        replay = match.get("replay")
        if not replay:
            continue
        try:
            replay = safe_replay_name(replay)
        except ValueError:
            continue
        db.execute("""INSERT INTO matches(season_name,replay_name,round_num,division,seed,map_id,turns,winner,kept,kind,label)
            VALUES (?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(season_name,replay_name) DO UPDATE SET
            round_num=excluded.round_num,division=excluded.division,seed=excluded.seed,
            map_id=excluded.map_id,turns=excluded.turns,winner=excluded.winner,
            kept=excluded.kept,kind=excluded.kind,label=excluded.label""",
                   (name, replay, match.get("round"), match.get("division"), match.get("seed"),
                    match.get("map_id"), match.get("turns"), match.get("winner"),
                    int(match.get("kept") is not False), match.get("kind") or "unknown",
                    match.get("label")))
        for person in match.get("snakes", []):
            slug = person.get("name")
            if not slug:
                continue
            ensure_team(db, slug)
            # The catalog has no verified snake-slot ID; preserve NULL until replay parsing.
            db.execute("""INSERT INTO participants(season_name,replay_name,team_slug,slot,placement,final_length,food_eaten,kills,turns_survived)
                VALUES (?,?,?,?,?,?,?,?,?) ON CONFLICT(season_name,replay_name,team_slug) DO UPDATE SET
                placement=excluded.placement,final_length=excluded.final_length,
                food_eaten=excluded.food_eaten,kills=excluded.kills,turns_survived=excluded.turns_survived""",
                       (name, replay, slug, None, person.get("placement"), person.get("length"),
                        person.get("food"), person.get("kills"), person.get("turns")))
        count += 1
    db.execute("UPDATE seasons SET catalog_version=2 WHERE name=?", (name,))
    db.commit()
    return count


def direction(old: dict, new: dict, width: int, height: int) -> str | None:
    if width < 3 or height < 3:
        return None
    dx = (new["x"] - old["x"]) % width
    dy = (new["y"] - old["y"]) % height
    if dx == width - 1:
        dx = -1
    if dy == height - 1:
        dy = -1
    return DIRECTIONS.get((dx, dy))


def relative_turn(before: str, after: str) -> str:
    clockwise = ["UP", "RIGHT", "DOWN", "LEFT"]
    delta = (clockwise.index(after) - clockwise.index(before)) % 4
    return {0: "straight", 1: "right", 2: "reverse", 3: "left"}[delta]


def analyze_replay(replay: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], list[tuple]]:
    frames = replay.get("frames", [])
    if not isinstance(frames, list) or not frames:
        raise ValueError("Replay has no frames")
    header = replay.get("header") or {}
    board = header.get("board") or [35, 35]
    width, height = int(board[0]), int(board[1])
    observations = defaultdict(lambda: Counter())
    latency = defaultdict(list)
    slot_names: dict[int, str] = {}
    events = []
    for frame in frames:
        for snake in frame.get("snakes", []):
            slot = snake.get("id")
            name = snake.get("name")
            if slot is not None and name:
                slot_names[int(slot)] = name
            if name and snake.get("latency_ms") is not None:
                latency[name].append(float(snake["latency_ms"]))
        for ix, event in enumerate(frame.get("events", [])):
            turn = event.get("turn", frame.get("turn", 0))
            cause = event.get("cause") or {}
            if not isinstance(cause, dict):
                cause = {}
            kind = event.get("kind")
            slot = event.get("snake")
            events.append((turn, ix, kind, slot, cause.get("kind"), cause.get("by")))
            name = slot_names.get(slot)
            if name and kind == "ate":
                observations[name]["food_events"] += 1
            if name and kind == "died":
                observations[name]["deaths"] += 1
                cause_name = cause.get("kind")
                if cause_name == "self_collision":
                    observations[name]["self_collisions"] += 1
                elif cause_name == "head_to_head":
                    observations[name]["head_to_head_deaths"] += 1
                elif cause_name == "collision":
                    observations[name]["body_collisions"] += 1
    for before, after in zip(frames, frames[1:]):
        if after.get("turn", -10) != before.get("turn", -10) + 1:
            continue
        former = {s.get("id"): s for s in before.get("snakes", [])}
        for snake in after.get("snakes", []):
            previous = former.get(snake.get("id"))
            if not previous or not snake.get("alive") or not previous.get("alive"):
                continue
            prev_body, body = previous.get("body") or [], snake.get("body") or []
            if len(prev_body) < 2 or not body:
                continue
            old_heading = direction(prev_body[1], prev_body[0], width, height)
            move = direction(prev_body[0], body[0], width, height)
            if not old_heading or not move:
                continue
            result = relative_turn(old_heading, move)
            if result == "reverse":  # usually invalid or a discontinuity; not a reliable choice
                continue
            name = snake.get("name") or previous.get("name")
            if name:
                observations[name]["observed_moves"] += 1
                observations[name][{"straight": "straight_moves", "left": "left_turns", "right": "right_turns"}[result]] += 1
    result = {}
    for name in set(observations) | set(latency) | set(slot_names.values()):
        obs = observations[name]
        result[name] = {k: obs[k] for k in (
            "observed_moves", "straight_moves", "left_turns", "right_turns",
            "food_events", "deaths", "self_collisions", "body_collisions", "head_to_head_deaths")}
        result[name]["avg_latency_ms"] = (sum(latency[name]) / len(latency[name])) if latency[name] else None
    return result, events


def replay_location(root: Path, season: str, replay: str) -> Path:
    parts = safe_replay_name(replay).split("/")
    return root / "replays" / safe_name(season) / Path(*parts[:-1]) / (parts[-1] + ".gz")


def install_replay(db: sqlite3.Connection, root: Path, season: str, name: str, raw: bytes) -> None:
    payload = checked_json(raw)
    stats, events = analyze_replay(payload)  # validate BEFORE committing file or DB state
    target = replay_location(root, season, name)
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix=".replay-", suffix=".gz", dir=target.parent, delete=False) as fh:
        tmp = Path(fh.name)
        try:
            with gzip.GzipFile(fileobj=fh, mode="wb", compresslevel=6, mtime=0) as gz:
                gz.write(raw)
        except BaseException:
            tmp.unlink(missing_ok=True)
            raise
    tmp.replace(target)
    digest = hashlib.sha256(raw).hexdigest()
    header = payload.get("header") or {}
    roster = header.get("roster", [])
    slot_by_name: dict[str, int] = {}
    for i, slug in enumerate(roster):
        if isinstance(slug, str):
            slot_by_name[slug] = i
    if payload.get("frames"):
        for snake in payload["frames"][0].get("snakes", []):
            if snake.get("name") and snake.get("id") is not None:
                slot_by_name[snake["name"]] = int(snake["id"])
    with db:
        db.execute("DELETE FROM events WHERE season_name=? AND replay_name=?", (season, name))
        db.execute("DELETE FROM behavior WHERE season_name=? AND replay_name=?", (season, name))
        for turn, ix, kind, slot, cause, killer in events:
            db.execute("""INSERT INTO events(season_name,replay_name,turn,event_idx,kind,snake_slot,cause,killer_slot)
                        VALUES (?,?,?,?,?,?,?,?)""", (season, name, turn, ix, kind, slot, cause, killer))
        for slug, metrics in stats.items():
            ensure_team(db, slug)
            db.execute("""INSERT INTO behavior(season_name,replay_name,team_slug,
                observed_moves,straight_moves,left_turns,right_turns,food_events,deaths,self_collisions,
                body_collisions,head_to_head_deaths,avg_latency_ms) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (season, name, slug, *(metrics[k] for k in (
                    "observed_moves", "straight_moves", "left_turns", "right_turns",
                    "food_events", "deaths", "self_collisions", "body_collisions", "head_to_head_deaths",
                    "avg_latency_ms"))))
            db.execute("""UPDATE participants SET slot=?, deaths=? WHERE season_name=? AND replay_name=? AND team_slug=?""",
                       (slot_by_name.get(slug), metrics["deaths"], season, name, slug))
        db.execute("""UPDATE matches SET replay_sha256=?, replay_bytes=?, downloaded_at=?
                     WHERE season_name=? AND replay_name=?""", (digest, len(raw), utcnow(), season, name))


def top_slugs(season: dict[str, Any], limit: int = 10) -> set[str]:
    ranked = []
    for table in season.get("tables", []):
        if table.get("division") == 1:
            ranked.extend((m.get("position", 999), m.get("name")) for m in table.get("table", []) if m.get("name"))
    return {slug for _, slug in sorted(ranked)[:limit]}


def promising_trial_slugs(db: sqlite3.Connection, season: str, limit: int = 15) -> set[str]:
    """Prioritize top gauntlet-1 trial performers even outside league Division 1."""
    rows = db.execute("""SELECT p.team_slug
        FROM matches m JOIN participants p
          ON m.season_name=p.season_name AND m.replay_name=p.replay_name
        WHERE m.season_name=? AND m.kind='trial'
          AND m.replay_name LIKE '%/trial-912000.rep'
          AND p.team_slug NOT LIKE '~%'
        ORDER BY p.placement ASC, p.final_length DESC
        LIMIT ?""", (season,limit)).fetchall()
    return {row[0] for row in rows}


def likely_replay_signatures(db: sqlite3.Connection) -> tuple[dict[tuple[str,str], tuple], set[tuple]]:
    """Heuristic signatures for prioritization only. Not proof of identical frames."""
    matches = db.execute("""SELECT season_name,replay_name,kind,seed,replay_sha256
        FROM matches""").fetchall()
    players: dict[tuple[str,str],list[tuple]] = defaultdict(list)
    for row in db.execute("""SELECT season_name,replay_name,team_slug,placement,
                            final_length,food_eaten,kills
                            FROM participants"""):
        players[(row[0],row[1])].append(tuple(row[2:]))
    signatures = {}
    downloaded = set()
    for season,name,kind,seed,sha in matches:
        signature = (kind,seed,tuple(sorted(players.get((season,name),[]))))
        signatures[(season,name)] = signature
        if sha:
            downloaded.add(signature)
    return signatures,downloaded


def queued_matches(db: sqlite3.Connection, root: Path, known_seasons: list[str],
                   priority: set[str], limit: int) -> list[tuple[str, str]]:
    """Research sampler: 60% student league, 40% controlled trials when available.

    League matches with several student opponents and Division 1 are preferred.
    Preserve recent and historical representation inside BOTH tracks.
    Do not count identical catalog signatures as new observations if alternatives
    exist. Exact SHA-256 deduplication still happens after replay download.
    """
    if limit <= 0 or not known_seasons:
        return []
    signatures, downloaded = likely_replay_signatures(db)
    champion_row = db.execute(
        "SELECT team_slug FROM standings WHERE season_name=? "
        "AND division=1 AND division_rank=1 LIMIT 1", (known_seasons[0],)
    ).fetchone()
    champion = champion_row[0] if champion_row else None
    # Represent a historical season once, even if a caller supplies duplicates.
    seasons = list(dict.fromkeys(known_seasons))
    pools: dict[str, list[list[tuple[str, str]]]] = {
        "league": [[], []], "trial": [[], []]
    }
    for index, season in enumerate(seasons):
        rows = db.execute("""SELECT m.replay_name, m.division, m.kind
                            FROM matches m WHERE m.season_name=?
                              AND m.kept=1 AND m.replay_sha256 IS NULL""",
                          (season,)).fetchall()
        entries: dict[str, list[tuple[tuple, str]]] = {"league": [], "trial": []}
        for name, division, kind in rows:
            names = {p[0] for p in db.execute(
                "SELECT team_slug FROM participants WHERE season_name=? AND replay_name=?",
                (season, name))}
            human_count = sum(not n.startswith("~") for n in names)
            priority_flag = 0 if (priority & names) else 1
            signature = signatures.get((season, name))
            already = signature in downloaded
            if kind == "trial":
                # Keep all three fixed on-arrival setups, not only gauntlet_1.
                suite_order = (0 if "/trial-912" in name else
                               1 if "/trial-910" in name else 2)
                score = (already, priority_flag, suite_order, name)
                entries["trial"].append((score, name))
            else:
                # Includes old catalogs whose kind was not explicitly classified.
                # Most actual league games have four students, but some include
                # filler benchmarks. Both are cataloged and reported separately.
                score = (already, division != 1,
                         0 if champion is not None and champion in names else 1,
                         -human_count, priority_flag, name)
                entries["league"].append((score, name))
        for kind in ("league", "trial"):
            entries[kind].sort(key=lambda x: x[0])
            if kind == "trial":
                # Round-robin all three controlled trial suites: each cycle
                # still captures gauntlet_1, hungry and hunter setups.
                groups = [[], [], []]
                for score, filename in entries[kind]:
                    suite = (0 if "/trial-912" in filename else
                             1 if "/trial-910" in filename else 2)
                    groups[suite].append((score, filename))
                entries[kind] = [
                    item for offset in range(max(map(len, groups), default=0))
                    for group_items in groups if offset < len(group_items)
                    for item in (group_items[offset],)
                ]
            dest = 0 if index == 0 else 1
            # Historical entries are interleaved across seasons below.
            if dest == 0:
                pools[kind][0] = [(season, name) for _, name in entries[kind]]
            else:
                existing = pools[kind][1]
                batch = [(season, name) for _, name in entries[kind]]
                # Round-robin across older seasons: avoid fully mining one
                # old season before sampling other archived periods.
                if index == 1:
                    pools[kind][1] = [batch]
                else:
                    pools[kind][1].append(batch)

    historical: dict[str, list[tuple[str, str]]] = {}
    for kind in ("league", "trial"):
        batches = pools[kind][1]
        # Older history may be absent; no API calls are made here.
        if batches and isinstance(batches[0],tuple):
            historical[kind] = list(batches)
        else:
            historical[kind] = [
                item for offset in range(max((len(x) for x in batches),default=0))
                for batch in batches if offset < len(batch)
                for item in (batch[offset],)
            ]

    league_target = (limit * 3 + 4) // 5  # ceil(60% of total)
    targets = {"league": league_target, "trial": limit - league_target}
    history_target = min(limit - 1, limit // 3) if len(seasons) > 1 else 0
    history_goals = {
        "league": min(targets["league"], (history_target * 3 + 4) // 5),
        "trial": max(0, history_target - min(targets["league"], (history_target * 3 + 4) // 5))
    }
    selected: list[tuple[str, str]] = []
    chosen: set[tuple[str, str]] = set()
    seen = set(downloaded)

    def add(pool: list[tuple[str, str]], cap: int, novel: bool) -> None:
        for pair in pool:
            if len(selected) >= cap:
                break
            if pair in chosen:
                continue
            sig = signatures.get(pair)
            if novel and sig in seen:
                continue
            selected.append(pair)
            chosen.add(pair)
            if sig is not None:
                seen.add(sig)

    # Explicit quotas for each environment, not an accidental side effect of
    # sorting trial suites before league games.
    for kind in ("league", "trial"):
        start = len(selected)
        hist_goal = start + history_goals[kind]
        goal = start + targets[kind]
        add(historical[kind], hist_goal, True)
        add(historical[kind], hist_goal, False)
        add(pools[kind][0], goal, True)
        add(historical[kind], goal, True)
        add(pools[kind][0], goal, False)
        add(historical[kind], goal, False)
    # If one environment has fewer new games, use the rest of the budget
    # in the other rather than leave available evidence on the table.
    if len(selected) < limit:
        for novel in (True, False):
            for kind in ("league", "trial"):
                add(pools[kind][0] + historical[kind], limit, novel)
    return selected



def report(db: sqlite3.Connection, root: Path, season: str) -> None:
    rows = db.execute("""SELECT p.team_slug, COUNT(*) samples,
        SUM(CASE WHEN p.placement=1 THEN 1 ELSE 0 END) wins,
        ROUND(AVG(p.final_length),1) avg_length,
        SUM(COALESCE(b.observed_moves,0)) moves,
        SUM(COALESCE(b.deaths,0)) deaths,
        SUM(COALESCE(b.self_collisions,0)) self_deaths,
        SUM(COALESCE(b.food_events,0)) food_events
        FROM participants p JOIN matches m ON p.season_name=m.season_name AND p.replay_name=m.replay_name
        LEFT JOIN behavior b ON p.season_name=b.season_name AND p.replay_name=b.replay_name AND p.team_slug=b.team_slug
        WHERE p.season_name=? AND m.replay_sha256 IS NOT NULL
        GROUP BY p.team_slug ORDER BY samples DESC, wins DESC LIMIT 20""", (season,)).fetchall()
    seasons, catalogs, downloaded = db.execute("SELECT COUNT(*), (SELECT COUNT(*) FROM matches), (SELECT COUNT(*) FROM matches WHERE replay_sha256 IS NOT NULL) FROM seasons").fetchone()
    lines = ["# Snake intelligence — collection status", "", f"Generated (UTC): {utcnow()}",
             f"Latest season: `{season}`", f"Cataloged seasons: {seasons}",
             f"Cataloged matches: {catalogs}", f"Downloaded replays (all seasons): {downloaded}", "",
             "## Most-observed snakes in downloaded current-season replays", "",
             "| Team | Matches | Wins | Avg final length | Observed moves | Deaths | Self-deaths | Food events |",
             "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for slug, n, wins, length, moves, deaths, self_deaths, ate in rows:
        lines.append(f"| `{slug}` | {n} | {wins} | {length} | {moves} | {deaths} | {self_deaths} | {ate} |")
    lines.extend(["", "Counts reflect downloaded replays only, not the whole league. Actions are inferred from adjacent alive frames, excluding discontinuities.",
                  "No strategy or win-rate advantage is assumed from these descriptive numbers.", ""])
    path = root / "reports" / "latest.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def select_seasons(site: dict[str, Any], db: sqlite3.Connection, limit: int) -> list[str]:
    """Sample recent and old seasons; gradually index missing history."""
    current = safe_name(site["season"]["name"])
    older = []
    for item in site.get("seasons", []):
        try:
            name = safe_name(item)
        except (TypeError, ValueError):
            continue
        if name != current and name not in older:
            older.append(name)
    chosen = [current]
    if not older:
        return chosen
    for index in [0, len(older)-1, len(older)//2, len(older)//4, 3*len(older)//4]:
        if len(chosen) >= limit:
            break
        if older[index] not in chosen:
            chosen.append(older[index])
    missing = [name for name in reversed(older) if not db.execute(
        "SELECT 1 FROM matches WHERE season_name=? LIMIT 1", (name,)).fetchone()]
    for item in missing + older:
        if len(chosen) >= limit:
            break
        if item not in chosen:
            chosen.append(item)
    return chosen[:limit]


def collect(client: Client, db: sqlite3.Connection, root: Path, max_replays: int,
            lookback: int = 2) -> dict[str, Any]:
    # During a platform season rollover, these two independent endpoints can
    # briefly disagree. Retry without assuming either response is authoritative.
    for rollover_attempt in range(3):
        site = client.get_json("site")
        current = safe_name(site["season"]["name"])
        season_data = client.get_json("season")
        if season_data.get("name") == current:
            break
        print(f"Season rollover in progress (attempt {rollover_attempt+1}/3); "
              "retrying consistent site/season snapshot", flush=True)
        time.sleep(2 + 2 * rollover_attempt)
    else:
        print("SKIPPED: /api/site and /api/season disagree during rollover; "
              "preserving existing data for the next scheduled run", flush=True)
        return {"season": current, "season_count": 0, "downloaded": 0,
                "attempted": 0, "skipped": "season_rollover"}
    seasons = select_seasons(site, db, lookback)
    ingest_latest_season(db, season_data)
    for name in seasons:
        version = db.execute("SELECT catalog_version FROM seasons WHERE name=?", (name,)).fetchone()
        if name != current and version and version[0] >= 2:
            continue
        try:
            catalog = client.get_json("games", {"season": name})
            if catalog.get("season") not in (None, name):
                raise ValueError(f"Catalog season mismatch: {name}")
            n = ingest_games(db, name, catalog)
            print(f"Cataloged {n} matches from {name}")
        except (OSError, ValueError, urllib.error.URLError, urllib.error.HTTPError) as exc:
            if name == current:
                raise
            print(f"Unable to index historical season {name}: {type(exc).__name__}: {exc}")
    priority = top_slugs(season_data) | promising_trial_slugs(db, current)
    chosen = queued_matches(db, root, seasons, priority, max_replays)
    completed = 0
    for name, replay in chosen:
        try:
            target = replay_location(root, name, replay)
            if target.exists():
                # Recover after a previous crash between file write and DB update.
                with gzip.open(target, "rb") as fh:
                    raw = fh.read()
            else:
                raw = client.get_replay(replay)
            install_replay(db, root, name, replay, raw)
            completed += 1
            print(f"Saved replay {name}/{replay}")
        except (OSError, ValueError, KeyError, TypeError, urllib.error.URLError) as exc:
            print(f"Skipped {name}/{replay}: {type(exc).__name__}: {exc}")
            # Leave absent/unmarked so future hourly cycles retry.
    report(db, root, current)
    return {"season": current, "season_count": len(seasons), "downloaded": completed,
            "attempted": len(chosen)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--max-replays", type=int, default=6)
    parser.add_argument("--lookback-seasons", type=int, default=2)
    parser.add_argument("--delay-seconds", type=float, default=1.0)
    args = parser.parse_args()
    if not (0 <= args.max_replays <= 30) or not (1 <= args.lookback_seasons <= 12) or args.delay_seconds < 0.75:
        parser.error("Use 0–30 replays, 1–12 seasons, and a delay of at least 0.75 seconds")
    db = connect(args.data_dir / "snake.db")
    try:
        outcome = collect(Client(delay=args.delay_seconds), db, args.data_dir,
                          args.max_replays, args.lookback_seasons)
        print(json.dumps(outcome, indent=2))
    finally:
        db.close()


if __name__ == "__main__":
    main()
