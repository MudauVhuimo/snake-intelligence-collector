#!/usr/bin/env python3
"""Read downloaded Snake26 replay frames and propose TESTABLE policy experiments.

No ML training or speculative 'win' claims. Static candidate-space calculations
are approximate because opponent turns, tail movement and food changes are unknown.
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque
import gzip
import json
from pathlib import Path
import sqlite3

from collector import direction, relative_turn, utcnow

STEP = {"UP": (0, -1), "RIGHT": (1, 0), "DOWN": (0, 1), "LEFT": (-1, 0)}
ORDER = list(STEP)

def wrap_dist(a: tuple[int, int], b: tuple[int, int], w: int, h: int) -> int:
    dx, dy = abs(a[0]-b[0]), abs(a[1]-b[1])
    return min(dx, w-dx) + min(dy, h-dy)

def at(p: tuple[int, int], d: str, w: int, h: int) -> tuple[int, int]:
    dx, dy = STEP[d]
    return ((p[0]+dx)%w, (p[1]+dy)%h)

def body_points(snake: dict) -> list[tuple[int,int]]:
    return [(int(p["x"]), int(p["y"])) for p in (snake.get("body") or [])]

def bounded_space(start: tuple[int,int], blocked: set[tuple[int,int]],
                  w: int, h: int, cap: int) -> int:
    if start in blocked:
        return 0
    visited = {start}
    todo = deque([start])
    while todo and len(visited) < cap:
        current = todo.popleft()
        for d in ORDER:
            nxt = at(current, d, w, h)
            if nxt not in blocked and nxt not in visited:
                visited.add(nxt)
                todo.append(nxt)
                if len(visited) >= cap:
                    break
    return len(visited)

def decision_features(before: dict, after: dict, snake: dict, nxt: dict,
                      w: int, h: int) -> dict | None:
    """One observed move at t->t+1; compute candidate proxies from state at t."""
    if not snake.get("alive") or not nxt.get("alive"):
        return None
    body = body_points(snake)
    next_body = body_points(nxt)
    if len(body) < 2 or not next_body:
        return None
    head = body[0]
    previous = body[1]
    heading = direction({"x": previous[0],"y":previous[1]},
                        {"x":head[0],"y":head[1]}, w, h)
    move = direction({"x":head[0],"y":head[1]},
                     {"x":next_body[0][0],"y":next_body[0][1]}, w, h)
    if not heading or not move or relative_turn(heading, move) == "reverse":
        return None
    occupied = set()
    opp_heads = []
    for other in before.get("snakes",[]):
        if not other.get("alive"):
            continue
        b = body_points(other)
        occupied.update(b)
        if other.get("id") != snake.get("id") and b:
            opp_heads.append(b[0])
    occupied.update((int(p["x"]),int(p["y"])) for p in before.get("obstacles",[]))
    food = [(int(p["x"]),int(p["y"])) for p in before.get("food",[])]
    # We deliberately treat occupied tails as blocked: conservative snapshot proxy.
    candidates = {}
    for d in ORDER:
        if relative_turn(heading,d) == "reverse":
            continue
        pos = at(head,d,w,h)
        if pos in occupied:
            continue
        dist = min((wrap_dist(pos,p,w,h) for p in food),default=None)
        cap = min(w*h, max(80,len(body)+20))
        candidates[d] = {"space":bounded_space(pos,occupied,w,h,cap),
                         "food_dist":dist,
                         "pos":pos}
    if move not in candidates:
        # Could have moved into a vacating tail. Cannot assess safely.
        return None
    result = {"valid":1,"choice":move,"len":len(body),"n_safe":len(candidates),
              "near_opponent":int(bool(opp_heads) and min(wrap_dist(head,p,w,h) for p in opp_heads)<=3),
              "greedy_applicable":0,"greedy":0,
              "space_applicable":int(len(candidates)>=2),"roomiest":0,
              "tradeoff":0,"space_over_food":0,
              "selected_food":candidates[move]["food_dist"],
              "selected_space":candidates[move]["space"],
              "best_space":max(c["space"] for c in candidates.values()),
              "options":candidates}
    if len(candidates)>=2:
        result["roomiest"]=int(candidates[move]["space"] == result["best_space"])
        if food:
            best_d=min(c["food_dist"] for c in candidates.values())
            result["greedy_applicable"]=1
            result["greedy"]=int(candidates[move]["food_dist"]==best_d)
            closest=[d for d,c in candidates.items() if c["food_dist"]==best_d]
            closest_space=max(candidates[d]["space"] for d in closest)
            if result["best_space"]>=closest_space+10:
                result["tradeoff"]=1
                result["space_over_food"]=int(result["roomiest"] and not result["greedy"])
    return result

def extract(replay: dict, every: int=25) -> tuple[dict[str, Counter], list[dict]]:
    frames=replay.get("frames",[])
    board=(replay.get("header") or {}).get("board") or [35,35]
    w,h=int(board[0]),int(board[1])
    agg=defaultdict(Counter)
    examples=[]
    for before,after in zip(frames,frames[1:]):
        turn=int(before.get("turn",-1))
        if turn<0 or turn%every!=0 or after.get("turn")!=turn+1:
            continue
        next_by_id={s.get("id"):s for s in after.get("snakes",[])}
        for snake in before.get("snakes",[]):
            other=next_by_id.get(snake.get("id"))
            if not other:
                continue
            features=decision_features(before,after,snake,other,w,h)
            if not features:
                continue
            name=snake.get("name")
            if not name:
                continue
            c=agg[name]
            for k in ("valid","near_opponent","greedy_applicable","greedy","space_applicable","roomiest","tradeoff","space_over_food"):
                c[k]+=features[k]
            if features["tradeoff"] and len(examples)<30:
                examples.append({"team":name,"turn":turn,"length":features["len"],
                    "move":features["choice"],"selected_space":features["selected_space"],
                    "best_space":features["best_space"],"selected_food":features["selected_food"],
                    "options":features["options"],"space_over_food":features["space_over_food"]})
    return dict(agg),examples

def percent(a: int,b: int) -> str:
    return f"{100*a/b:.1f}%" if b else "—"

def analyze(root: Path, top: set[str] | None=None, every: int=25, limit: int=0) -> dict:
    db=sqlite3.connect(root/"snake.db")
    if top is None:
        latest=db.execute("SELECT name FROM seasons WHERE created IS NOT NULL ORDER BY name DESC LIMIT 1").fetchone()
        top={x[0] for x in db.execute(
            "SELECT team_slug FROM standings WHERE season_name=? AND division=1 AND division_rank<=10",
            (latest[0],))} if latest else set()
    files=sorted((root/"replays").rglob("*.rep.gz"),reverse=True)
    hashes={(s,n):sha for s,n,sha in db.execute(
        "SELECT season_name,replay_name,replay_sha256 FROM matches WHERE replay_sha256 IS NOT NULL")}
    if limit:
        files=files[:limit]
    teams=defaultdict(Counter)
    group=defaultdict(Counter)
    matches=Counter()
    cases=[]
    processed=0
    failed=0
    duplicates=0
    seen_hashes=set()
    processed_keys=[]
    for path in files:
        rel=path.relative_to(root/"replays")
        season=rel.parts[0]
        replay_name="/".join(rel.parts[1:])[:-3]
        sha=hashes.get((season,replay_name))
        if sha and sha in seen_hashes:
            duplicates+=1
            continue
        try:
            with gzip.open(path,"rt",encoding="utf-8") as fh:
                replay=json.load(fh)
            summary, examples=extract(replay,every=every)
        except (OSError,ValueError,KeyError,TypeError) as err:
            failed+=1
            print(f"Skipping {path}: {type(err).__name__}: {err}")
            continue
        processed+=1
        processed_keys.append((season,replay_name))
        if sha:
            seen_hashes.add(sha)
        for name,obs in summary.items():
            teams[name].update(obs)
            matches[name]+=1
            label = ("Built-in benchmarks" if name.startswith("~") else
                     "Current top-10" if name in top else "Other student bots")
            group[label].update(obs)
        for e in examples:
            if len(cases)>=100:
                break
            e["season"]=season
            e["replay"]=replay_name
            cases.append(e)
    death_causes=defaultdict(Counter)
    for season,replay in processed_keys:
        for slug,cause,count in db.execute(
            """SELECT p.team_slug, COALESCE(e.cause,'unspecified'), COUNT(*)
               FROM events e JOIN participants p
                 ON p.season_name=e.season_name AND p.replay_name=e.replay_name
                 AND p.slot=e.snake_slot
               WHERE e.kind='died' AND e.season_name=? AND e.replay_name=?
               GROUP BY p.team_slug, COALESCE(e.cause,'unspecified')""",
            (season,replay)).fetchall():
            death_causes[slug][cause]+=count
    db.close()
    return {"teams":teams,"groups":group,"matches":matches,"cases":cases,
            "processed":processed,"failed":failed,"duplicates":duplicates,
            "top":top,"stride":every,
            "death_causes":death_causes}

def markdown(results: dict) -> str:
    teams=results["teams"]; groups=results["groups"]; matches=results["matches"]
    lines=["# Snake26 strategy laboratory — LEGACY POOLED EXPLORATION","",
           "**Important:** This legacy diagnostic pools on-arrival trials and actual league",
           "replays. It is NOT valid evidence that a strategy works in the league.",
           "Use [Joined Research](joint_analysis.md) and",
           "[Mode-Separated Replay Behavior](behavior_by_mode.md) instead.",
           "The static reachable-space search is capped: many genuinely different",
           "moves tie at the cap. Thus a very high 'widest-space choice' percentage",
           "does NOT establish that a snake uses a space-maximizing algorithm.","",
           f"Updated UTC: {utcnow()}",
           f"Unique replays analyzed: **{results['processed']}** (duplicate hashes skipped: {results['duplicates']}; unreadable: {results['failed']})",
           f"Sampling: every **{results['stride']}th** turn per match, not independent observations.","",
           "## What the data can and cannot tell us","",
           "This is **behavioral observation**, not a live match simulator. Candidate moves use a conservative **static occupancy** approximation: snake tails may vacate, opponents move simultaneously, and outcomes could change. Therefore percentages are descriptive proxies, not guaranteed-safe decisions or win probabilities.","",
           "A prerecorded opponent does **not** respond to changes made by our bot; fixed historical moves cannot provide a valid full counterfactual match. To benchmark wins, we need to run live executables against locally available opponents or compare equivalent seed/opponent setups.","",
           "## Mixed trial/league samples: diagnostic only","",
           "| Group | Sampled moves | Food-nearest choices | Widest-space choices | Clear food/space tradeoffs | Space favored in tradeoffs |",
           "|---|---:|---:|---:|---:|---:|"]
    for k in ("Current top-10","Other student bots","Built-in benchmarks"):
        x=groups.get(k,Counter())
        lines.append(f"| {k} | {x['valid']} | {percent(x['greedy'],x['greedy_applicable'])} | {percent(x['roomiest'],x['space_applicable'])} | {x['tradeoff']} | {percent(x['space_over_food'],x['tradeoff'])} |")
    lines+=["","**Interpretation guardrail:** Built-in `~` bots are reported separately. Top-ten means the *latest* Division 1 top-ten ranking, not necessarily the same code version in old seasons. Groups have unequal and possibly biased opponents. Do not infer causation or an optimal policy from this table.","",
            "## Individual behavior fingerprints","",
            "| Team | Replays | Sampled moves | Food-nearest | Widest-space | Food/space conflicts | Space chosen in conflicts |",
            "|---|---:|---:|---:|---:|---:|---:|"]
    ranked=sorted(teams, key=lambda n:(n.startswith("~"),n not in results["top"],-matches[n],-teams[n]["valid"]))
    for n in ranked[:30]:
        x=teams[n]
        lines.append(f"| `{n}` | {matches[n]} | {x['valid']} | {percent(x['greedy'],x['greedy_applicable'])} | {percent(x['roomiest'],x['space_applicable'])} | {x['tradeoff']} | {percent(x['space_over_food'],x['tradeoff'])} |")
    lines+=["","## Observed deaths by cause","",
            "Counts are actual `died` replay events, unlike static-space estimates.","",
            "| Group | Self-collision | Body collision | Head-to-head | Other |",
            "|---|---:|---:|---:|---:|"]
    for label in ("Current top-10","Other student bots","Built-in benchmarks"):
        combined=Counter()
        for slug,causes in results["death_causes"].items():
            group_name = ("Built-in benchmarks" if slug.startswith("~") else
                          "Current top-10" if slug in results["top"] else "Other student bots")
            if group_name == label:
                combined.update(causes)
        major=sum(combined.get(k,0) for k in ("self_collision","collision","head_to_head"))
        lines.append(f"| {label} | {combined['self_collision']} | {combined['collision']} | {combined['head_to_head']} | {sum(combined.values())-major} |")
    lines+=["","Use the death causes to decide whether to first test tail-reachability, body-avoidance, or head-to-head threat rules. Compare on equivalent unseen matches, not raw unadjusted death totals.","",
            "## Replay-backed tactical situations","",
            "A tradeoff means the most food-directed static-free move had a reachable-space estimate at least 10 tiles smaller than another static-free option. Space scores are **bounded probes**, not exact guarantees.","",
            "| Replay | Turn | Snake | Body length | Actual move | Food distance after move | Space score (chosen/best) | Favored space? |",
            "|---|---:|---|---:|---|---:|---:|---|"]
    ranked_cases=sorted(results["cases"], key=lambda e:(not e["space_over_food"],-e["length"]))
    for e in ranked_cases[:24]:
        link=f"../replays/{e['season']}/{e['replay']}.gz"
        lines.append(f"| [`{e['replay']}`]({link}) | {e['turn']} | `{e['team']}` | {e['length']} | {e['move']} | {e['selected_food']} | {e['selected_space']}/{e['best_space']} | {'yes' if e['space_over_food'] else 'no'} |")
    if not ranked_cases:
        lines.append("| No clear space/food conflicts sampled yet | | | | | | | |")
    lines+=["","## Historical hypotheses for later investigation (NO implementation yet)","",
            "1. **Food-versus-space planner:** Assign each candidate move a weighted score for distance to food and bounded flood-fill space. Compare against current Java bot, using the same fresh seeds.",
            "2. **Danger override:** When a candidate leads to constrained reachable space, temporarily prioritize escape over food; test ablation with/without the override.",
            "3. **Opponent-pressure rule:** Test threat-aware movement when an opponent head is within three toroidal tiles. The current report counts proximity but does not yet recover opponent intent.",
            "4. **Policy imitation experiment:** Use replay states as labeled observations for relative actions, holding out entire matches and seasons for validation. High next-move accuracy alone is *not* proof of better game performance.",
            "",
            "Only promote a strategy if it improves **held-out match outcomes** and survival with equivalent opponent setups. Collect more samples before trusting patterns from individual snakes.",""]
    return "\n".join(lines)

def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    p.add_argument("--stride",type=int,default=25)
    p.add_argument("--max-files",type=int,default=0)
    a=p.parse_args()
    if a.stride<1: p.error("stride must be >=1")
    r=analyze(a.data_dir,every=a.stride,limit=a.max_files)
    output=a.data_dir/"reports"/"strategy_lab.md"
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(markdown(r),encoding="utf-8")
    print(f"Strategy report built from {r['processed']} replay(s): {output}")

if __name__ == "__main__":
    main()
