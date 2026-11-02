"""Alternative first-move route-space PROXIES, derived from observed Snake26 frames.

The two estimators intentionally differ:
* frozen_area: connected free cells after ONE hypothetical no-growth move,
  keeping ALL snake bodies stationary and treating obstacles as fixed.
* tail_reach8: number of distinct head positions encountered by a bounded
  8-step self-body continuation, with the OWN body/tail moving and all OTHER
  snakes frozen. Food consumption/growth, head contests, and future opponent
  moves are NOT simulated. This is not an engine-verified legal path.

Beam search is deterministic (64 states/depth, at most two per endpoint),
optimistic/approximate, and does not establish a feasible long-term policy.
It is a feature study, NEVER a counterfactual win-rate experiment.
"""
from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass

from .threat_windows_core import board_shape,coord

DIRECTIONS=((1,0),(-1,0),(0,1),(0,-1))
HORIZON=8
BEAM=64
ENDPOINT_CAP=2

@dataclass(frozen=True)
class Scene:
    width:int
    height:int
    own:tuple
    others:frozenset
    food:frozenset

def adjacent(pos,w,h):
    x,y=pos
    return (((x+1)%w,y),((x-1)%w,y),(x,(y+1)%h),(x,(y-1)%h))

def scene_from_frame(replay,frame,sid):
    w,h=board_shape(replay)
    own=[s for s in frame.get("snakes",()) if s.get("id")==sid
         and s.get("alive") and s.get("body")]
    if len(own)!=1:
        return None
    body=tuple(coord(p) for p in own[0]["body"])
    if len(body)<2 or any(x is None for x in body) or len(set(body))!=len(body):
        return None
    occupied=set()
    for s in frame.get("snakes",()):
        if s.get("id")==sid or not s.get("alive"):continue
        occupied.update(x for p in s.get("body",()) if (x:=coord(p)) is not None)
    occupied.update(x for p in frame.get("obstacles",()) if (x:=coord(p)) is not None)
    food=frozenset(x for p in frame.get("food",()) if (x:=coord(p)) is not None)
    return Scene(w,h,body,frozenset(occupied),food)

def step_body(body,new_head,foreign):
    """Own-tail vacating in a NO-GROWTH projection; no official legality claim."""
    if new_head in foreign or new_head in body[:-1]:
        return None
    return (new_head,)+body[:-1]

def candidate_moves(scene):
    """Movement possibilities under *our* no-growth, frozen-others model.

    Exclude stepping into the old tail if the destination is an apple:
    actual food would cause growth; model does not simulate +5 body growth.
    """
    return [(p,new) for p in adjacent(scene.own[0],scene.width,scene.height)
            if (new:=step_body(scene.own,p,scene.others)) is not None
            and not (p in scene.food and p==scene.own[-1])]

def frozen_area(scene,post_body):
    """Flood-fill from next head, with all postmove body cells frozen."""
    start=post_body[0]
    blocked=scene.others|frozenset(post_body[1:])
    if start in blocked:return 0
    seen={start}
    queue=deque([start])
    while queue:
        p=queue.popleft()
        for nxt in adjacent(p,scene.width,scene.height):
            if nxt not in blocked and nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return len(seen)

def projected_free_dirs(scene,body):
    return sum(p not in scene.others and p not in body[:-1]
               for p in adjacent(body[0],scene.width,scene.height))

def tail_reachable(scene,first_body,horizon=HORIZON,beam=BEAM):
    """Bounded own-body self-avoiding continuation, frozen opponents, no growth.

    Report union of reachable head positions at offsets 1..H, plus whether a
    full H-step continuation was retained in the beam. This is a lower bound
    on simulated-beam state exploration, not on true game safe space.
    """
    if horizon<1 or beam<1:raise ValueError("Horizon and beam must be positive")
    frontier=[first_body]
    visited={first_body[0]}
    full_depth=1
    for depth in range(2,horizon+1):
        next_states=[]
        dedup=set()
        for state in frontier:
            for p in adjacent(state[0],scene.width,scene.height):
                new=step_body(state,p,scene.others)
                if new is None or new in dedup:
                    continue
                dedup.add(new)
                next_states.append(new)
        if not next_states:break
        # Diverse next heads first, then another representative per head.
        next_states.sort(key=lambda b:(-projected_free_dirs(scene,b),
                                       b[0],b[-1],b))
        chosen=[]
        used=Counter()
        for state in next_states:
            head=state[0]
            if used[head]>=ENDPOINT_CAP:continue
            chosen.append(state)
            used[head]+=1
            if len(chosen)>=beam:break
        frontier=chosen
        visited.update(s[0] for s in frontier)
        full_depth=depth
    return dict(area=len(visited),full_horizon=(full_depth==horizon),
                max_depth=full_depth)

def scene_metrics(scene,horizon=HORIZON,beam=BEAM):
    rows=[]
    for p,new_body in candidate_moves(scene):
        tail=tail_reachable(scene,new_body,horizon,beam)
        rows.append(dict(next_head=p,frozen=frozen_area(scene,new_body),
                         tail=tail["area"],full_horizon=tail["full_horizon"],
                         max_depth=tail["max_depth"],
                         adjacent_free=projected_free_dirs(scene,new_body)))
    return rows

def rank_choice(rows,selected,metric):
    """Compare ACTUAL observed first head against model's alternatives.

    Rank 0..1 = midrank percentile; 1 means strictly better than all other
    actions, .5 means every candidate ties; this is NOT predicted outcomes.
    """
    if not rows or selected is None:return None
    found=next((x for x in rows if x["next_head"]==selected),None)
    if found is None:return None
    values=[x[metric] for x in rows]
    here=found[metric]
    n=len(values)
    return dict(value=here,
                best=max(values),
                regret=max(values)-here,
                rank=(sum(v<here for v in values)+.5*sum(v==here for v in values))/n,
                discriminative=max(values)>min(values),
                top=here==max(values))

def validate_plain_transition(body,following,was_eating):
    """Only check invariant when no growth/event and same body length.

    This verifies the model's OWN-body shift on actual observed normal moves;
    never treats the simulated OTHER snake positions as validated.
    """
    if was_eating or not following or len(body)!=len(following):
        return None
    return (following[0],)+body[:-1]==following
