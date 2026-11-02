"""Replay-only death autopsies versus observed 10-turn escapes.

Constructs a retrospective CASE–CONTROL comparison from real frame states:
* sample every 25 turns, analyze only heads <=3 cells away OR <=1 free side;
* require contiguous future 10-turn replay frames;
* outcomes are real 'died' events, not score/length heuristics;
* match observed death cases to survivors in the SAME mode, starting length
  band, head-distance band, free-side band and (when possible) time phase;
* report both sides' *actual* first-three-turn movement and attrition.

No counterfactual replay, optimal policy claim, or Java snake edits.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from pathlib import Path
import gzip
import hashlib
import json
from statistics import mean

from .threat_windows_core import (
    board_shape, coord, distance, heads, length_band, load as unused_load,
    scan_replay, unoccupied_neighbors,
)

HORIZON=10
TRACE_STEPS=(1,3,10,30)
MATCHING_PHASE=500

def same_distance(a,b,w,h):
    return distance(a,b,w,h)

def snapshots_at(replay):
    return {f["turn"]:f for f in replay.get("frames",[])
            if isinstance(f.get("turn"),int)}

def first_death_by_id(replay):
    events=defaultdict(list)
    for f in replay["frames"]:
        t=f.get("turn")
        if not isinstance(t,int):continue
        for e in f.get("events",[]):
            if e.get("kind")=="died" and e.get("snake") is not None:
                events[e["snake"]].append((t,(e.get("cause") or {}).get("kind","unknown")))
    return events

def stable_target_food(before,after,head_a,head_b,w,h):
    """Only follow the *same* visible apple; never replace with a new target."""
    food_a={p for x in before.get("food",[]) if (p:=coord(x)) is not None}
    food_b={p for x in after.get("food",[]) if (p:=coord(x)) is not None}
    same=food_a & food_b
    if not same:return None
    target=min(same,key=lambda p:(distance(head_a,p,w,h),p))
    return distance(head_a,target,w,h)-distance(head_b,target,w,h)

def trajectory_at(frame_before,frame_after,sid,baseline,w,h,all_deaths,offset):
    t=frame_before["turn"]
    if frame_after is None or frame_after.get("turn")!=t+offset:
        return None
    if any(t<at<=t+offset for at,cause in all_deaths.get(sid,())):
        return None
    living=heads(frame_after)
    if sid not in living:
        return None
    name,point,_=living[sid]
    opponents=[(oid,v) for oid,v in living.items() if oid!=sid]
    if not opponents:
        return None
    nearest=min(distance(point,other[1],w,h) for oid,other in opponents)
    exits=unoccupied_neighbors(frame_after,point,w,h)
    origin=baseline["head"]
    jump=distance(point,origin,w,h)
    result=dict(
        nearest_head=nearest,neighbor_exits=exits,
        head_gain=nearest-baseline["nearest_head"],
        exits_gain=exits-baseline["neighbor_exits"],
        position=point,displacement=jump)
    if offset==1:
        if jump!=1:
            return None  # Inconsistent movement or unseen respawn/teleport.
        result["stable_food_progress"]=stable_target_food(
            frame_before,frame_after,origin,point,w,h)
    return result

def review_replay(replay,season,path,mode,sha):
    """Return danger-window observations, plus a QC counter."""
    w,h=board_shape(replay)
    frames=snapshots_at(replay)
    deaths=first_death_by_id(replay)
    base,qc=scan_replay(replay,season,path,mode,sha)
    out=[]
    seen_starts=set()
    for row in base:
        if not (row["nearest_head"]<=3 or row["neighbor_exits"]<=1):
            continue
        t=row["start_turn"]
        start=frames.get(t)
        if start is None:
            continue
        live=heads(start)
        candidates=[(sid,pt) for sid,pt in live.items() if pt[0]==row["student"]]
        if len(candidates)!=1:
            qc["ambiguous_student_names"]+=1
            continue
        sid,(_,pos,_)=candidates[0]
        key=(t,sid)
        if key in seen_starts:
            qc["duplicate_start"]+=1
            continue
        seen_starts.add(key)
        before=dict(row,head=pos,sid=sid)
        # All outcomes use real 'died' events already validated by scan_replay.
        event=next(((at,cause) for at,cause in deaths.get(sid,())
                    if t<at<=t+HORIZON),None)
        if bool(event)!=bool(row["death_next_10"]):
            qc["death_event_disagreement"]+=1
            continue
        trajectory={}
        for step in TRACE_STEPS:
            if any(t+k not in frames for k in range(1,step+1)):
                qc["missing_step_"+str(step)]+=1
                continue
            sample=trajectory_at(start,frames.get(t+step),sid,before,w,h,deaths,step)
            if sample:
                trajectory[step]=sample
        phase=t//MATCHING_PHASE
        before.update(
            outcome="death" if event else "escape_10",
            death_turn=event[0] if event else None,
            death_cause=event[1] if event else None,
            phase=phase,limited_exits=row["neighbor_exits"]<=1,
            trajectory=trajectory,
        )
        out.append(before)
        qc["danger_positions"]+=1
        qc["death_cases"]+=int(bool(event))
    return out,qc

def load_autopsies(data_dir,max_files=250):
    paths=sorted((data_dir/"replays").rglob("*.rep.gz"),reverse=True)
    choices=paths[:max_files] if max_files else paths
    quality=Counter(files=len(paths),scanned=len(choices))
    seen=set()
    all_rows=[]
    for path in choices:
        rel=path.relative_to(data_dir/"replays")
        mode="trial" if "trials" in rel.parts else "league"
        season=rel.parts[0]
        try:
            with gzip.open(path,"rb") as file:raw=file.read()
            sha=hashlib.sha256(raw).hexdigest()
            if sha in seen:
                quality["duplicate_replays"]+=1
                continue
            replay=json.loads(raw)
            rows,qc=review_replay(replay,season,str(rel),mode,sha)
            seen.add(sha)
        except (ValueError,KeyError,TypeError,OSError):
            quality["invalid"]+=1
            continue
        quality[mode+"_unique_replays"]+=1
        quality["unique_replays"]+=1
        quality.update(qc)
        all_rows.extend(rows)
    return all_rows,quality

def strata(row,phase=True):
    key=(row["mode"],row["length_bin"],row["head_pressure"],row["limited_exits"])
    return key+(row["phase"],) if phase else key

def match_cases(rows):
    """Match on PRE-outcome variables only, one un-reused control per case.

    Exact match: mode,length band,head-pressure band,limited exits,500-turn
    phase; fallback removes only phase, clearly flagged in report.
    Within stratum prefer the same replay (opponents/environment controlled),
    then same student, then nearest initial length / head distance / exits.
    This is NOT randomized or a policy efficacy estimate.
    """
    cases=[r for r in rows if r["outcome"]=="death"]
    controls=[r for r in rows if r["outcome"]=="escape_10"]
    by_exact=defaultdict(list)
    by_relaxed=defaultdict(list)
    for r in controls:
        by_exact[strata(r)].append(r)
        by_relaxed[strata(r,False)].append(r)
    used=set()
    matches=[]
    unmatched=Counter()
    for case in sorted(cases,key=lambda r:(
            r["mode"],r["sha"],r["start_turn"],r["student"])):
        level="exact"
        choices=[r for r in by_exact[strata(case)] if
                 (r["sha"],r["student"],r["start_turn"]) not in used]
        if not choices:
            level="phase_relaxed"
            choices=[r for r in by_relaxed[strata(case,False)] if
                     (r["sha"],r["student"],r["start_turn"]) not in used]
        if not choices:
            unmatched[case["mode"]]+=1
            continue
        choices.sort(key=lambda r:(
            r["sha"]!=case["sha"],r["student"]!=case["student"],
            abs(r["length"]-case["length"]),
            abs(r["nearest_head"]-case["nearest_head"]),
            abs(r["neighbor_exits"]-case["neighbor_exits"]),
            abs(r["start_turn"]-case["start_turn"]),r["sha"],r["student"]))
        control=choices[0]
        used.add((control["sha"],control["student"],control["start_turn"]))
        matches.append(dict(case=case,control=control,level=level,
                            same_replay=(case["sha"]==control["sha"]),
                            same_student=(case["student"]==control["student"])))
    return matches,unmatched

def paired_deltas(matches,mode,step,measure):
    """Both subjects must still be alive and observed at the step.

    IMPORTANT: conditional 'survived until step' is selected, especially
    among death cases. Report both-sides-available and missing counts.
    """
    result=[]
    for pair in matches:
        if pair["case"]["mode"]!=mode:
            continue
        a=pair["case"]["trajectory"].get(step)
        b=pair["control"]["trajectory"].get(step)
        if not a or not b:
            continue
        if a.get(measure) is None or b.get(measure) is None:
            continue
        result.append(dict(
            case_sha=pair["case"]["sha"],control_sha=pair["control"]["sha"],
            case_value=a[measure],control_value=b[measure],
            control_minus_case=b[measure]-a[measure],
            same_replay=pair["same_replay"]))
    return result
