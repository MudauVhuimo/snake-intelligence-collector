"""One-step opponent-head REACHABILITY CONES for Snake26 replay research.

These are geometric overapproximations, NOT engine-verified legal moves,
probabilities, or necessarily fatal head-to-head contacts:
* Heading is inferred only from a valid toroidal head/neck step.
* Exclude immediate reversal into the neck if heading is known.
* Otherwise include all four cardinal destinations (uncertain).
* Do NOT freeze opponents' possible tail cells or assume body collision order.
* Compare current observed body length without asserting 2026 head-on rule.

Use solely baseline frames for prediction; inspect next frame only to AUDIT
the proposed reach sets, never to alter predicted candidate risk scores.
"""
from __future__ import annotations
from collections import Counter

from .long_horizon_core import axial_step
from .route_space_core import adjacent
from .threat_windows_core import coord

def opponent_cones(frame, focal_id, width, height):
    """id -> head, length, three or four candidate next-head positions."""
    cones={}
    for s in frame.get("snakes",()):
        sid=s.get("id")
        if sid==focal_id or sid is None or not s.get("alive"):
            continue
        body=s.get("body") or ()
        if not body:
            continue
        head=coord(body[0])
        if head is None:
            continue
        neck=coord(body[1]) if len(body)>=2 else None
        heading=axial_step(neck,head,width,height) if neck is not None else None
        reaches=set(adjacent(head,width,height))
        if heading is not None:
            # Against the previous movement, equivalent to stepping back into neck.
            backward=((head[0]-heading[0])%width,
                      (head[1]-heading[1])%height)
            reaches.discard(backward)
        cones[sid]=dict(name=s.get("name","?"),length=len(body),head=head,
                        known_heading=heading is not None,
                        reaches=frozenset(reaches))
    return cones

def summarize_candidates(alternatives,cones,own_length):
    """Augment route alternatives without looking at future opponent actions."""
    decorated=[]
    for move in alternatives:
        target=move["next_head"]
        reaching=[sid for sid,p in cones.items() if target in p["reaches"]]
        nonweaker=[sid for sid in reaching if cones[sid]["length"]>=own_length]
        longer=[sid for sid in reaching if cones[sid]["length"]>own_length]
        decorated.append({
            **move,
            "head_cone":bool(reaching),
            "nonweaker_cone":bool(nonweaker),
            "longer_cone":bool(longer),
            "potential_opponents":len(reaching),
        })
    return decorated

def candidate_profile(options):
    """One pre-action state risk feature set, distinct from an observed choice."""
    n=len(options)
    cone=[x for x in options if x["head_cone"]]
    nonweaker=[x for x in options if x["nonweaker_cone"]]
    uncontested=[x for x in options if not x["head_cone"]]
    nonweaker_free=[x for x in options if not x["nonweaker_cone"]]
    def biggest(rows):
        return max((x["tail"] for x in rows),default=0)
    return dict(
        candidate_count=n,
        threatened_count=len(cone),
        nonweaker_threatened_count=len(nonweaker),
        uncontested_count=len(uncontested),
        nonweaker_free_count=len(nonweaker_free),
        all_cone=bool(n and len(cone)==n),
        all_nonweaker_cone=bool(n and len(nonweaker)==n),
        best_uncontested_tail=biggest(uncontested),
        best_nonweaker_free_tail=biggest(nonweaker_free),
        best_any_tail=biggest(options),
        top_tail_has_uncontested=bool(options) and any(
            x["tail"]==biggest(options) and not x["head_cone"] for x in options),
        tail_best_requires_cone=bool(options) and not any(
            x["tail"]==biggest(options) and not x["head_cone"] for x in options),
    )

def actual_choice_risk(options,observed_next_head):
    """Observed choice only if next frame contains an actual living snake head."""
    if observed_next_head is None:return dict(observed=False)
    chosen=next((x for x in options if x["next_head"]==observed_next_head),None)
    if chosen is None:return dict(observed=False)
    return dict(observed=True,chosen_cone=chosen["head_cone"],
                chosen_nonweaker_cone=chosen["nonweaker_cone"],
                chosen_longer_cone=chosen["longer_cone"],
                chosen_tail=chosen["tail"],
                chosen_avoided_risk=not chosen["head_cone"])

def check_opponent_next_heads(cones,following,excluded_ids):
    """Audit observed surviving opponents against PREVIOUS-frame cones.

    Exclude both deaths AND new respawns. A teleport is not a normal move.
    This validates geometry, not that all enumerated moves are legal.
    """
    counters=Counter()
    if following is None:
        counters["missing_frame"]+=1
        return counters
    now={}
    for s in following.get("snakes",()):
        if s.get("id") is None or not s.get("alive") or not s.get("body"):
            continue
        pos=coord(s["body"][0])
        if pos is not None:now[s["id"]]=pos
    for sid,cone in cones.items():
        if sid in excluded_ids:
            counters["opponent_dead"]+=1
            continue
        if sid not in now:
            counters["opponent_absent"]+=1
            continue
        counters["opponent_next_checked"]+=1
        if now[sid] in cone["reaches"]:
            counters["opponent_next_within_cone"]+=1
        else:
            counters["opponent_next_outside_cone"]+=1
            if cone["known_heading"]:
                counters["known_heading_disagreement"]+=1
    return counters

def head_to_head_lengths(before,death_event):
    """Lengths at LAST observed frame for a recorded head_to_head death.

    This is a victim EVENT, not unique collision or an inferred attacker move.
    'by' may be missing/unknown; do not fabricate which player won.
    """
    cause=death_event.get("cause") or {}
    if death_event.get("kind")!="died" or cause.get("kind")!="head_to_head":
        return None
    sid=death_event.get("snake")
    by=cause.get("by")
    if before is None:
        return dict(relation="missing_prior_frame",victim_length=None,
                    peer_length=None)
    living={}
    for s in before.get("snakes",()):
        if s.get("alive") and s.get("body") and s.get("id") is not None:
            living[s["id"]]=len(s["body"])
    if sid not in living or by not in living:
        return dict(relation="missing_participant",victim_length=living.get(sid),
                    peer_length=living.get(by))
    a,b=living[sid],living[by]
    relation="victim_shorter" if a<b else "victim_longer" if a>b else "equal"
    return dict(relation=relation,victim_length=a,peer_length=b)


def audit_next_head_death(following,focal_id):
    """Observed next-frame death event cause. A cause is not a predicted move."""
    if following is None:return "censored"
    matched=[e for e in following.get("events",())
             if e.get("kind")=="died" and e.get("snake")==focal_id]
    if not matched:return "no_recorded_death"
    if len(matched)>1:return "ambiguous_death"
    return str((matched[0].get("cause") or {}).get("kind") or "other")
