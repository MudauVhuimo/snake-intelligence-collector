"""Turn-by-turn observation of food races where a built-in bot starts closer.

Definitions:
- One published on-arrival trial has a student and built-in benchmark bots.
- Start distances are toroidal Manhattan distances, not collision-free routes.
- Capture requires a real eat event AND next-frame head at the disappeared food.
- No claims of why an opponent chose a move or what it would do counterfactually.
"""
from collections import Counter, defaultdict
from pathlib import Path
import gzip
import hashlib
import json

from .food_race_core import dist, heads, points, group, lag_band

def alive_snake(frame, sid):
    return next((s for s in frame.get("snakes", [])
                 if s.get("id") == sid and s.get("alive") and s.get("body")), None)

def head_pos(snake):
    p = snake["body"][0]
    return (int(p["x"]), int(p["y"]))

def static_path_length(frame, sid, target, w, h):
    """Shortest toroidal path if every currently occupied body cell stays blocked.

    This is a snapshot obstruction proxy, NOT an actual time-dependent safe route.
    Tail cells may vacate, and opposing heads move simultaneously.
    """
    from collections import deque
    who = alive_snake(frame, sid)
    if not who:
        return None
    start = head_pos(who)
    if start == target:
        return 0
    occupied = set()
    for snake in frame.get("snakes", []):
        if snake.get("alive"):
            for p in snake.get("body") or []:
                occupied.add((int(p["x"]), int(p["y"])))
    for p in frame.get("obstacles") or []:
        occupied.add((int(p["x"]), int(p["y"])))
    if target in occupied:
        return None
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        (x,y),steps = queue.popleft()
        for neighbour in (((x+1)%w,y),((x-1)%w,y),
                          (x,(y+1)%h),(x,(y-1)%h)):
            if neighbour == target:
                return steps + 1
            if neighbour in occupied or neighbour in visited:
                continue
            visited.add(neighbour)
            queue.append((neighbour,steps+1))
    return None


def start_case(frame, pos, w, h, replay_name):
    candidates = heads(frame)
    students = sorted((dist(p, pos, w, h), sid, name) for sid, (name, p) in candidates.items()
                      if group(name) == "Student")
    benches = sorted((dist(p, pos, w, h), sid, name) for sid, (name, p) in candidates.items()
                     if group(name) == "Benchmark")
    if len(students) != 1 or not benches:
        return None
    sd, student_id, student_name = students[0]
    bd, bench_id, bench_name = benches[0]
    return dict(start_turn=frame["turn"], pos=pos, path=replay_name,
                student_id=student_id, student_name=student_name,
                bench_id=bench_id, bench_name=bench_name,
                student_start=sd, bench_start=bd,
                student_length=len(alive_snake(frame, student_id)["body"]),
                bench_length=len(alive_snake(frame, bench_id)["body"]),
                trace=[], student_death=False, bench_death=False,
                student_respawn=False, bench_respawn=False,
                bench_other_ate=0, student_other_ate=0,
                student_static=None, bench_static=None)

def sample(case, frame, w, h):
    t = frame.get("turn")
    if not isinstance(t, int):
        return
    if case["trace"] and case["trace"][-1]["t"] == t:
        return
    a = alive_snake(frame, case["student_id"])
    b = alive_snake(frame, case["bench_id"])
    case["trace"].append(dict(t=t,
        sd=dist(head_pos(a), case["pos"], w, h) if a else None,
        bd=dist(head_pos(b), case["pos"], w, h) if b else None,
        spos=head_pos(a) if a else None, bpos=head_pos(b) if b else None))

def death_or_respawn(case, frame):
    for event in frame.get("events", []):
        kind, sid = event.get("kind"), event.get("snake")
        if kind == "died":
            if sid == case["student_id"]: case["student_death"] = True
            if sid == case["bench_id"]: case["bench_death"] = True
        elif kind == "ate":
            current = heads(frame).get(sid)
            if current and current[1] != case["pos"]:
                if sid == case["student_id"]: case["student_other_ate"] += 1
                if sid == case["bench_id"]: case["bench_other_ate"] += 1
        elif kind == "respawned":
            if sid == case["student_id"]: case["student_respawn"] = True
            if sid == case["bench_id"]: case["bench_respawn"] = True

def progress_at(case, name, offset=5):
    key = "sd" if name == "student" else "bd"
    if case[name + "_death"] or case[name + "_respawn"]:
        return None
    t0 = case["start_turn"]
    start = next((point[key] for point in case["trace"] if point["t"] == t0), None)
    end = next((point[key] for point in case["trace"] if point["t"] == t0 + offset), None)
    return start - end if start is not None and end is not None else None

def extract(replay, replay_name):
    frames = replay.get("frames", [])
    board = (replay.get("header") or {}).get("board") or [35, 35]
    w, h = map(int, board)
    if w < 3 or h < 3 or not isinstance(frames, list) or len(frames) < 2:
        raise ValueError("Invalid replay")
    active, rows, qc = {}, [], Counter()
    frame_lookup = {f.get("turn"):f for f in frames if isinstance(f.get("turn"),int)}
    for before, after in zip(frames, frames[1:]):
        turn = before.get("turn")
        if not isinstance(turn, int) or after.get("turn") != turn + 1:
            active.clear()
            qc["discontinuities"] += 1
            continue
        pre, post = points(before.get("food")), points(after.get("food"))
        for pos in pre:
            if pos not in active:
                new = start_case(before, pos, w, h, replay_name)
                if new is not None:
                    active[pos] = new
                    qc["eligible_episodes"] += 1
        for case in active.values():
            sample(case, before, w, h)
            death_or_respawn(case, after)
        next_heads = heads(after)
        ate = {e.get("snake") for e in after.get("events", []) if e.get("kind") == "ate"}
        for pos in pre - post:
            case = active.get(pos)
            if not case:
                continue
            candidates = [(sid, n) for sid, (n, p) in next_heads.items()
                          if sid in ate and p == pos]
            if len(candidates) != 1:
                qc["unmatched"] += 1
                continue
            sid, name = candidates[0]
            sample(case, after, w, h)
            case["winner"] = group(name)
            case["winner_name"] = name
            case["lag"] = after["turn"] - case["start_turn"]
            case["advantage"] = case["student_start"] - case["bench_start"]
            case["student_p5"] = progress_at(case, "student")
            case["bench_p5"] = progress_at(case, "bench")
            case["student_p10"] = progress_at(case, "student", 10)
            case["bench_p10"] = progress_at(case, "bench", 10)
            if case["advantage"] >= 3:
                start_frame = frame_lookup.get(case["start_turn"])
                if start_frame is not None:
                    case["student_static"] = static_path_length(
                        start_frame,case["student_id"],pos,w,h)
                    case["bench_static"] = static_path_length(
                        start_frame,case["bench_id"],pos,w,h)
            case["study"] = ("benchmark_closer" if case["advantage"] >= 3
                             else "student_closer" if case["advantage"] <= -3
                             else "near_tie")
            rows.append(case)
            qc["matched"] += 1
        for pos in pre - post:
            active.pop(pos, None)
        active = {pos: case for pos, case in active.items() if pos in post}
    return rows, qc

def scan(data_dir: Path, limit=250):
    files = sorted((data_dir / "replays").rglob("*.rep.gz"), reverse=True)
    selected = files[:limit] if limit else files
    seen, quality, records = set(), Counter(files=len(files), scanned=len(selected)), []
    for file in selected:
        rel = file.relative_to(data_dir / "replays")
        if "trials" not in rel.parts:
            continue
        try:
            with gzip.open(file, "rb") as f:
                raw = f.read()
            sha = hashlib.sha256(raw).hexdigest()
            if sha in seen:
                quality["duplicates"] += 1
                continue
            replay = json.loads(raw)
            rows, checks = extract(replay, str(rel)[:-3])
            seen.add(sha)
        except (OSError, ValueError, KeyError, TypeError):
            quality["invalid"] += 1
            continue
        quality["unique_trial_replays"] += 1
        quality.update(checks)
        records.extend(rows)
    return records, quality
