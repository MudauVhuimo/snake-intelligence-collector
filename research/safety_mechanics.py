"""2026 Snake league mechanics: observed-transition audit.

Measure what actual official replay frames DO, not unchosen moves.
The authoritative compiled engine is NOT reimplemented here.
In particular, an apparently blocked cell can become free as a tail moves.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from .threat_windows_core import board_shape, coord, heads, distance

CAUSES = ("self", "body", "head_to_head", "obstacle", "forfeit", "other")


def _snake_info(frame):
    result = {}
    for snake in frame.get("snakes", ()):
        sid = snake.get("id")
        if sid is None or not snake.get("alive") or not snake.get("body"):
            continue
        body = tuple(p for x in snake["body"] if (p := coord(x)) is not None)
        if body:
            result[sid] = dict(name=snake.get("name", ""), body=body,
                               length=len(body), head=body[0], tail=body[-1])
    return result


def audit_replay(replay):
    w,h = board_shape(replay)
    frames = replay.get("frames", ())
    if not isinstance(frames, list) or len(frames) < 2:
        raise ValueError("Need consecutive replay frames")
    data = defaultdict(Counter)
    for before,after in zip(frames,frames[1:]):
        old_t = before.get("turn")
        if not isinstance(old_t, int) or after.get("turn") != old_t+1:
            data["all"]["nonconsecutive"] += 1
            continue
        old = _snake_info(before)
        new = _snake_info(after)
        events = after.get("events", ())
        if not isinstance(events, list):
            events = []
        died = {e.get("snake"): e.get("cause") or {}
                for e in events if e.get("kind") == "died"}
        ate = {e.get("snake") for e in events if e.get("kind") == "ate"}
        food = {p for x in before.get("food", ()) if (p := coord(x)) is not None}
        for sid,person in old.items():
            mode = "trial" if str(person["name"]).startswith("~") else "student"
            # Keep all students and built-ins distinct, but combine for normal-move parity.
            bucket = data["all"]
            bucket["prior_alive_snake_turns"] += 1
            if sid in died:
                bucket["recorded_deaths"] += 1
                cause = died[sid].get("kind") or "unknown"
                bucket["death_" + str(cause)] += 1
                if cause == "head_to_head":
                    other = old.get(died[sid].get("by"))
                    if other is None:
                        bucket["head_on_peer_not_found"] += 1
                    else:
                        own_len = person["length"]
                        rival_len = other["length"]
                        relation = ("shorter" if own_len < rival_len else
                                    "longer" if own_len > rival_len else "equal")
                        bucket["head_on_victim_" + relation] += 1
                continue
            next_person = new.get(sid)
            if next_person is None:
                bucket["unexplained_absences"] += 1
                continue
            oldhead,newhead=person["head"],next_person["head"]
            if distance(oldhead,newhead,w,h)!=1:
                bucket["invalid_one_step_head"] += 1
                continue
            bucket["normal_one_step_heads"] += 1
            if abs(newhead[0]-oldhead[0])==w-1 or abs(newhead[1]-oldhead[1])==h-1:
                bucket["wrapped_steps"] += 1
            if newhead == person["tail"]:
                bucket["entered_old_own_tail"] += 1
                if newhead in next_person["body"][1:]:
                    bucket["old_tail_still_occupied_after_move"] += 1
            foreign_old_tails = [s for enemy,s in old.items()
                                 if enemy!=sid and newhead==s["tail"]]
            if foreign_old_tails:
                bucket["entered_old_opponent_tail"] += 1
                if any(newhead in other["body"] for enemy,other in new.items()
                       if enemy!=sid):
                    bucket["opponent_tail_still_occupied_after_move"] += 1
            if sid in ate:
                bucket["recorded_eating_survivors"] += 1
                if newhead not in food:
                    bucket["ate_event_without_previous_food_cell"] += 1
                increment = next_person["length"]-person["length"]
                bucket["eating_length_delta_" + str(increment)] += 1
            if next_person["length"]<person["length"]:
                bucket["unexplained_length_decrease"] += 1
        for sid in ate:
            if sid not in old:
                data["all"]["eat_without_prior_living_id"] += 1
    return data["all"]


def scan(data_dir, max_files=250):
    root=data_dir/"replays"
    paths=sorted(root.rglob("*.rep.gz"), reverse=True)
    picked=paths[:max_files] if max_files else paths
    totals=defaultdict(Counter)
    seen=set()
    quality=Counter(available_files=len(paths),selected_files=len(picked))
    for path in picked:
        try:
            with gzip.open(path,"rb") as file: raw=file.read()
            sha=hashlib.sha256(raw).hexdigest()
            if sha in seen:
                quality["duplicate_payloads"] += 1
                continue
            replay=json.loads(raw)
            counts=audit_replay(replay)
        except (ValueError,TypeError,KeyError,OSError):
            quality["unreadable"] += 1
            continue
        seen.add(sha)
        mode="trial" if "trials" in path.relative_to(root).parts else "league"
        totals[mode].update(counts)
        quality[mode+"_unique_replays"] += 1
    return totals,quality


def build(data_dir,max_files=250):
    totals,quality=scan(data_dir,max_files)
    labels=[
        ("prior_alive_snake_turns","Previously living snake-turns"),
        ("normal_one_step_heads","Normal surviving one-cell head moves"),
        ("invalid_one_step_head","Invalid observed head motion"),
        ("wrapped_steps","Observed toroidal wrap moves"),
        ("entered_old_own_tail","Surviving move into OWN old tail coordinate"),
        ("entered_old_opponent_tail","Surviving move into OPPONENT old tail coordinate"),
        ("recorded_eating_survivors","Survivors with recorded eat event"),
        ("ate_event_without_previous_food_cell","Eat without previous-frame apple"),
        ("recorded_deaths","Explicit recorded death events"),
        ("death_self","Self death events"),
        ("death_body","Body death events"),
        ("death_head_to_head","Head-to-head victim events"),
        ("head_on_victim_shorter","Head-on victim shorter than attributed rival"),
        ("head_on_victim_equal","Head-on victim equal to attributed rival"),
        ("head_on_victim_longer","Head-on victim longer than attributed rival"),
        ("head_on_peer_not_found","Head-on attribution peer unavailable"),
        ("unexplained_absences","Unexplained missing living head next frame"),
    ]
    lines=[
        "# Snake26: observed collision and movement mechanics audit","",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
        "## Evidence and limits", "",
        "Source: deduplicated REAL 2026 league/trial replay payloads, consecutive",
        "frames and explicit death/eat events. Outcomes use actual participants.",
        "This audit does **NOT** simulate hypothetical alternatives; it cannot",
        "establish that any unchosen action would be safe or certainly fatal.",
        "A replay victim event is not a complete head-on collision record.",
        "The authoritative engine's simultaneous action resolution is still the",
        "source of truth. Verify game-specific collision order against that",
        "engine before declaring a Java next-move filter 'provably safe'.", "",
        f"Unique league replays: **{quality['league_unique_replays']}**;",
        f"unique trials: **{quality['trial_unique_replays']}**;",
        f"duplicate payloads removed: **{quality['duplicate_payloads']}**;",
        f"unreadable replays: **{quality['unreadable']}**.", "",
        "## Verified observed outcomes by environment", "",
        "| Audit | Peer league | On-arrival trials |",
        "|---|---:|---:|",
    ]
    for key,label in labels:
        lines.append(f"| {label} | {totals['league'][key]} | {totals['trial'][key]} |")
    lines+=["", "## Eating growth length changes among observed survivors", "",
            "| Next-frame body segment count minus previous | League | Trials |",
            "|---|---:|---:|"]
    deltas=sorted({int(k.removeprefix("eating_length_delta_"))
                   for v in totals.values() for k in v
                   if k.startswith("eating_length_delta_")})
    for delta in deltas:
        lines.append(f"| {delta:+d} | {totals['league']['eating_length_delta_'+str(delta)]} | {totals['trial']['eating_length_delta_'+str(delta)]} |")
    lines += ["", "## Interpretation for SAFETY-01", "",
        "- Wrap movements are observable one-step transitions on a torus.",
        "- A surviving old-tail entry falsifies any simplistic permanent",
        "  rule that bans every currently occupied tail cell.",
        "- Head-on victim length comparisons are OBSERVATIONAL support for",
        "  length priority, not a complete formal proof of tie/collision order.",
        "- Opponent tails may advance simultaneously; do not assume a tail",
        "  vacates if food growth or a collision changes the same turn.",
        "- An explicit cause labels a recorded death, not the unavailable",
        "  attempted destination of the dead snake.",
        "- Before gameplay implementation, run targeted move-pair tests",
        "  against the exact downloaded 2026 native engine or documented",
        "  official mechanics to validate guaranteed vs merely possible danger.",
        "", "**This closes the missing descriptive evidence gap only; no action",
        "has been certified safe in all game states.**", ""]
    target=data_dir/"reports"/"safety_mechanics.md"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text("\n".join(lines),encoding="utf-8")
    return dict(quality=dict(quality),league=dict(totals["league"]),
                trial=dict(totals["trial"]),report=str(target))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir",type=Path,default=Path("data"))
    parser.add_argument("--max-files",type=int,default=250)
    args=parser.parse_args()
    if args.max_files<0:parser.error("max-files must be >=0")
    output=build(args.data_dir,args.max_files)
    print(json.dumps(dict(quality=output["quality"],report=output["report"],
                          league_head_events=output["league"].get("death_head_to_head",0)),
                     indent=2))


if __name__=="__main__":
    main()
