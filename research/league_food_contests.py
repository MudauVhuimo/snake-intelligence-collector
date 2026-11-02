"""Observed apple contests among student peers in the 2026 Snake league.

Descriptive replay evidence only: no inferred intent, alternative-world moves,
or experimental agent. One row is one first-visible apple opportunity.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from .opponent_cone_core import opponent_cones
from .threat_windows_core import board_shape, coord, distance, heads

HORIZON = 40
MAX_DISTANCE = 10
MAX_GAP = 2


def food_cells(frame):
    return {p for item in frame.get("food", ())
            if (p := coord(item)) is not None}


def contestants(frame, apple, width, height):
    options = sorted(
        ((distance(pos, apple, width, height), name, str(sid), sid, length, pos)
         for sid, (name, pos, length) in heads(frame).items()
         if not name.startswith("~")), key=lambda x: x[:3])
    if (len(options) < 2 or options[1][0] > MAX_DISTANCE or
            options[1][0] - options[0][0] > MAX_GAP):
        return None
    return [dict(sid=sid, name=name, length=length, head=pos, distance=d)
            for d, name, _tie, sid, length, pos in options[:2]]


def first_step(frame, following, person, apple, width, height):
    sid = person["sid"]
    result = dict(step="missing", cone=None, nonweaker_cone=None, first_death=False)
    if following is None or following.get("turn") != frame.get("turn") + 1:
        return result
    result["first_death"] = any(e.get("kind") == "died" and e.get("snake") == sid
                                for e in following.get("events", ()))
    if result["first_death"]:
        result["step"] = "died"
        return result
    next_head = heads(following).get(sid)
    if next_head is None or distance(person["head"], next_head[1], width, height) != 1:
        return result
    after_dist = distance(next_head[1], apple, width, height)
    before_dist = person["distance"]
    result["step"] = ("closer" if after_dist < before_dist else
                      "farther" if after_dist > before_dist else "sideways")
    cones = opponent_cones(frame, sid, width, height)
    threatened = [v for v in cones.values() if next_head[1] in v["reaches"]]
    result["cone"] = bool(threatened)
    result["nonweaker_cone"] = any(v["length"] >= person["length"] for v in threatened)
    return result


def capture_status(following, apple):
    """Require both explicit eat event and actual new head on prior apple cell."""
    alive = heads(following)
    ate = {e.get("snake") for e in following.get("events", ()) if e.get("kind") == "ate"}
    hits = [sid for sid, (_name, pt, _length) in alive.items() if sid in ate and pt == apple]
    return hits[0] if len(hits) == 1 else None


def analyze_replay(replay, season, replay_path, sha):
    width, height = board_shape(replay)
    frames = replay.get("frames")
    if not isinstance(frames, list) or not frames:
        raise ValueError("Missing replay frames")
    roster = {s.get("name") for s in frames[0].get("snakes", ())
              if isinstance(s.get("name"), str) and not s["name"].startswith("~")}
    if len(roster) < 2:
        return [], Counter(excluded_not_peer_league=1)

    rows, qc = [], Counter()
    for i, frame in enumerate(frames):
        turn = frame.get("turn")
        if not isinstance(turn, int):
            qc["missing_turn"] += 1
            continue
        previous = frames[i-1] if i else None
        if previous is not None and previous.get("turn") != turn - 1:
            qc["frame_gaps"] += 1
            continue
        appeared = food_cells(frame) - (food_cells(previous) if previous else set())
        for apple in sorted(appeared):
            qc["visible_food_appearances"] += 1
            pair = contestants(frame, apple, width, height)
            if pair is None:
                continue
            qc["eligible_close_peer_contests"] += 1
            following = frames[i+1] if i+1 < len(frames) else None
            steps = [first_step(frame, following, person, apple, width, height)
                     for person in pair]
            winner_id, status, elapsed = None, "censored_40", None
            last_turn = turn
            for later in frames[i+1:i+HORIZON+1]:
                if later.get("turn") != last_turn + 1:
                    status = "censored_gap"
                    break
                last_turn += 1
                if apple not in food_cells(later):
                    winner_id = capture_status(later, apple)
                    status = ("confirmed" if winner_id is not None else
                              "unverified_disappearance")
                    elapsed = last_turn - turn
                    break
            else:
                if len(frames)-i-1 < HORIZON:
                    status = "censored_end"

            ids = {person["sid"] for person in pair}
            if winner_id is None:
                winner_class = "unresolved"
            elif winner_id not in ids:
                winner_class = "other"
            else:
                winner_class = "nearest" if winner_id == pair[0]["sid"] else "second"
                if pair[0]["distance"] == pair[1]["distance"]:
                    winner_class = "tied_first" if winner_class == "nearest" else "tied_second"
            palmer = next((p for p in pair if "palmer" in p["name"].lower()), None)
            palmer_result = ("not_present" if palmer is None else
                             "unresolved" if winner_id is None else
                             "captured" if winner_id == palmer["sid"] else "other_captured")
            winner_name = ""
            if elapsed is not None and winner_id is not None:
                winner_name = heads(frames[i+elapsed]).get(winner_id, ("",None,None))[0]
            rows.append(dict(
                season=season, replay=replay_path, sha=sha,
                start_turn=turn, food_x=apple[0], food_y=apple[1],
                first_frame=i == 0,
                nearest=pair[0]["name"], second=pair[1]["name"],
                nearest_distance=pair[0]["distance"], second_distance=pair[1]["distance"],
                gap=pair[1]["distance"] - pair[0]["distance"],
                nearest_length=pair[0]["length"], second_length=pair[1]["length"],
                nearest_step=steps[0]["step"], second_step=steps[1]["step"],
                nearest_cone=steps[0]["cone"], second_cone=steps[1]["cone"],
                nearest_nonweaker_cone=steps[0]["nonweaker_cone"],
                second_nonweaker_cone=steps[1]["nonweaker_cone"],
                nearest_first_death=steps[0]["first_death"],
                second_first_death=steps[1]["first_death"],
                status=status, elapsed=elapsed, winner_class=winner_class,
                winner=winner_name, palmer_result=palmer_result))
            qc[status] += 1
    return rows, qc


def scan(data_dir, max_files=250):
    available = [p for p in sorted((data_dir / "replays").rglob("*.rep.gz"), reverse=True)
                 if "trials" not in p.relative_to(data_dir / "replays").parts]
    selected = available[:max_files] if max_files else available
    rows, seen, qc = [], set(), Counter(league_files=len(available), files_scanned=len(selected))
    for path in selected:
        rel = path.relative_to(data_dir / "replays")
        try:
            with gzip.open(path, "rb") as f:
                raw = f.read()
            sha = hashlib.sha256(raw).hexdigest()
            if sha in seen:
                qc["duplicate_replays"] += 1
                continue
            seen.add(sha)
            found, quality = analyze_replay(json.loads(raw), rel.parts[0], str(rel), sha)
        except (ValueError, TypeError, OSError, KeyError):
            qc["invalid_replays"] += 1
            continue
        qc["unique_replays"] += 1
        qc.update(quality)
        rows.extend(found)
    return rows, qc


def build(data_dir, max_files=250):
    rows, qc = scan(data_dir, max_files)
    reports, derived = data_dir / "reports", data_dir / "derived"
    reports.mkdir(parents=True, exist_ok=True)
    derived.mkdir(parents=True, exist_ok=True)
    csv_path = derived / "league_food_contests.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]) if rows
                                else ["season", "replay", "start_turn", "status"])
        writer.writeheader()
        writer.writerows(rows)

    status = Counter(r["status"] for r in rows)
    outcomes = Counter(r["winner_class"] for r in rows if r["status"] == "confirmed")
    palmer = Counter(r["palmer_result"] for r in rows if r["palmer_result"] != "not_present")
    def pct(n, denominator):
        return f"{100*n/denominator:.1f}%" if denominator else "insufficient"

    lines = [
        "# Snake26: real league apple contests", "",
        "Generated UTC: " + datetime.now(timezone.utc).isoformat(timespec="seconds"), "",
        "## Opportunity definition", "",
        "One observation is a newly visible apple with two living STUDENT heads within",
        "10 toroidal Manhattan steps, separated by at most 2 steps in distance to that apple.",
        "First-frame food is flagged in the CSV. Replays with only one student are excluded.",
        "Distance is NOT a safe-path estimate; this is selected, observational replay data.", "",
        f"Unique replay payloads: **{qc['unique_replays']}**; exact duplicates: **{qc['duplicate_replays']}**.",
        f"Close-peer opportunities: **{len(rows)}**.",
        f"Captures verified within {HORIZON} turns: **{status['confirmed']}/{len(rows)} ({pct(status['confirmed'], len(rows))})**.",
        f"Unverified disappearances: **{status['unverified_disappearance']}**; horizon/end censored: **{status['censored_40']+status['censored_end']}**; frame gaps: **{status['censored_gap']}**.", "",
        "## Actual capturer among verified outcomes", "",
        "| Position at first visibility | Captures | Share of confirmed |",
        "|---|---:|---:|",
    ]
    for label, key in (("Strictly closest", "nearest"), ("Strictly second-closest", "second"),
                       ("Tied first (ID-order tie break)", "tied_first"),
                       ("Tied second (ID-order tie break)", "tied_second"),
                       ("Other participant", "other")):
        lines.append(f"| {label} | {outcomes[key]} | {pct(outcomes[key], status['confirmed'])} |")
    lines += [
        "", "These shares are conditional on confirmed captures, NOT an intervention or",
        "the chance that chasing an apple will win it.", "",
        "## Actual first movements, including missing/dead observations", "",
        "| Starting distance rank | Closer | Sideways | Farther | Died at +1 | Unobserved normal step |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for role in ("nearest", "second"):
        moves = Counter(r[f"{role}_step"] for r in rows)
        lines.append(f"| {role} | {moves['closer']} | {moves['sideways']} | {moves['farther']} | {moves['died']} | {moves['missing']} |")
    for role in ("nearest", "second"):
        observed = [r for r in rows if r[f"{role}_cone"] is not None]
        cone = sum(r[f"{role}_cone"] is True for r in observed)
        nonweaker = sum(r[f"{role}_nonweaker_cone"] is True for r in observed)
        lines.append(f"- {role.title()} first moves into possible opponent head cones: **{cone}/{len(observed)} ({pct(cone,len(observed))})**; equal/longer cones: **{nonweaker}/{len(observed)} ({pct(nonweaker,len(observed))})**.")
    lines += [
        "", "A geometric cone includes collision-impossible opponent moves; it is NOT",
        "a calibrated likelihood. Dead/unobserved first moves never become assumed safe",
        "movements. Movement observations are survivor-selected.", "",
        "## Palmer: distinct reference subset", "",
        f"Eligible apple appearances involving Palmer: **{sum(palmer.values())}**.",
        f"Palmer captured **{palmer['captured']}**; another participant captured **{palmer['other_captured']}**; censored/unverified **{palmer['unresolved']}**.",
        "These are not opponent-matched skill ratings.", "",
        "## Research limitations", "",
        "- Different games and bot versions are not independent or necessarily comparable.",
        "- Repeated apple episodes in one replay require match-cluster uncertainty analysis.",
        "- A closer first move does not establish intent; apple position and bodies evolve.",
        "- Censored and unverified apples are not counted as losses.",
        "- To advance FOOD-04, test body-aware arrival predictors on whole-game holdouts",
        "  and finally in controlled ablations against diverse peers (including Palmer).",
        "", "[Episode-level CSV](../derived/league_food_contests.csv).", "",
        "**No Java competitor agent is changed.**", "",
    ]
    report = reports / "league_food_contests.md"
    report.write_text("\n".join(lines), encoding="utf-8")
    return dict(episodes=len(rows), confirmed=status["confirmed"],
                palmer_episodes=sum(palmer.values()), report=str(report), csv=str(csv_path))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--max-files", type=int, default=250)
    args = parser.parse_args()
    if args.max_files < 0:
        parser.error("max-files must be nonnegative")
    print(json.dumps(build(args.data_dir, args.max_files), indent=2))


if __name__ == "__main__":
    main()
