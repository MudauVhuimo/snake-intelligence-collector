"""Read Snake26 trials and unique replay traces for exploratory analysis."""
from collections import Counter, defaultdict
from pathlib import Path
import gzip
import hashlib
import json
import sqlite3

BINS = [(5, 24, "5-24"), (25, 49, "25-49"), (50, 99, "50-99"),
        (100, 149, "100-149"), (150, 100000, "150+")]
CAUSES = ("self_collision", "collision", "head_to_head", "other")

def length_bin(length):
    for lo, hi, label in BINS:
        if lo <= length <= hi:
            return label
    return None

def trial_catalog(db):
    row = db.execute("SELECT name FROM seasons WHERE created IS NOT NULL ORDER BY name DESC LIMIT 1").fetchone()
    if not row:
        return None, []
    season = row[0]
    rows = db.execute(
        """SELECT p.team_slug, p.final_length, p.food_eaten, p.placement
           FROM matches m JOIN participants p
             ON m.season_name=p.season_name AND m.replay_name=p.replay_name
           WHERE m.season_name=? AND m.kind='trial'
             AND m.replay_name LIKE '%/trial-912000.rep'
             AND p.team_slug NOT LIKE '~%'
             AND p.final_length IS NOT NULL AND p.food_eaten IS NOT NULL""",
        (season,)).fetchall()
    return season, [dict(name=n, length=int(l), food=int(f), place=p)
                    for n,l,f,p in rows]

def replay_summary(data_dir, season, max_files=250):
    """Avoid counting byte-identical historical replays as independent matches."""
    candidates = sorted((data_dir/"replays").rglob("*.rep.gz"),reverse=True)
    chosen = candidates[:max_files] if max_files else candidates
    summary = dict(files=len(candidates), scanned=len(chosen), unique=0,
                   duplicate=0, bad=0, curves={}, deaths=defaultdict(Counter),
                   exposures=defaultdict(Counter),
                   mode_deaths=defaultdict(Counter),
                   mode_exposures=defaultdict(Counter),
                   unique_modes=Counter())
    hashes = set()
    for path in chosen:
        try:
            with gzip.open(path, "rb") as source:
                raw = source.read()
            digest = hashlib.sha256(raw).hexdigest()
            if digest in hashes:
                summary["duplicate"] += 1
                continue
            replay = json.loads(raw)
            frames = replay["frames"]
            if not isinstance(frames, list) or len(frames)<2:
                raise ValueError("invalid replay")
            hashes.add(digest)
        except (ValueError, KeyError, OSError, TypeError):
            summary["bad"] += 1
            continue
        summary["unique"] += 1
        relative = path.relative_to(data_dir/"replays")
        mode = "trial" if "trials" in relative.parts else "league"
        summary["unique_modes"][mode] += 1
        if relative.parts[0] == season and path.name == "trial-912000.rep.gz":
            students = [s.get("name") for s in frames[0].get("snakes",[])
                        if isinstance(s.get("name"),str) and not s["name"].startswith("~")]
            if len(students)==1:
                name = students[0]
                values = []
                for frame in frames:
                    turn = frame.get("turn")
                    if not isinstance(turn,int) or (turn%100 and frame is not frames[-1]):
                        continue
                    snake = next((s for s in frame.get("snakes",[])
                                  if s.get("name")==name), None)
                    if snake:
                        values.append((turn, int(snake.get("length") or len(snake.get("body") or []))))
                summary["curves"][name] = values
        for before, after in zip(frames, frames[1:]):
            if after.get("turn") != before.get("turn",-999)+1:
                continue
            alive = {}
            for snake in before.get("snakes",[]):
                if not snake.get("alive") or not snake.get("body"):
                    continue
                sid, name = snake.get("id"),snake.get("name")
                if sid is None or not isinstance(name,str):
                    continue
                group = "Benchmark" if name.startswith("~") else "Student"
                cat = length_bin(int(snake.get("length") or len(snake["body"])))
                if cat:
                    alive[sid]=(group,cat)
                    summary["exposures"][group][cat]+=1
                    if group=="Student":
                        summary["mode_exposures"][mode][cat]+=1
            for event in after.get("events",[]):
                if event.get("kind") != "died" or event.get("snake") not in alive:
                    continue
                group,cat=alive[event["snake"]]
                cause=(event.get("cause") or {}).get("kind")
                cause=cause if cause in CAUSES else "other"
                summary["deaths"][group][cause]+=1
                summary["deaths"][group]["bin:"+cat]+=1
                if group=="Student":
                    summary["mode_deaths"][mode]["bin:"+cat]+=1
                    summary["mode_deaths"][mode][cause]+=1
    return summary
