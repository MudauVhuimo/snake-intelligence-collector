"""Long-horizon outcomes after genuinely dangerous Wits Snake26 positions.

Sampling:
  * Reuse exactly the deduplicated baseline danger windows from escape_autopsy_core:
    one living student every 25 turns, near a head (<=3) OR <=1 free neighbor.
  * Survival means NO recorded 'died' event before the horizon. Being alive
    at the horizon AFTER a respawn is not survival.
  * For every horizon require ALL turns t+1..t+h to exist, unless a 'died'
    event already occurred in contiguous observed frames. Missing future
    frames -> censored (never automatically survived).
  * Classify behavior at +3 before looking at late deaths (turns 11..30).
  * League games (student peers) and benchmark trials are always separate.
  * Every repeat replay is deduplicated by SHA-256 before sampling.

The inferential unit for intervals is the entire unique REPLAY, not a frame.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import gzip
import hashlib
import json

from .escape_autopsy_core import review_replay, first_death_by_id, snapshots_at
from .threat_windows_core import board_shape, coord, distance, heads, unoccupied_neighbors

HORIZONS=(10,20,30)
STEPS=(1,3,10,20,30)
PALMER="421462-alexander-palmer"

def continuous_turns(frames, t, limit=30):
    """Highest verified turn-offset consecutively present after t."""
    count=0
    for offset in range(1,limit+1):
        if t+offset not in frames:
            break
        count=offset
    return count

def outcome_status(t, sid, death_by_id, contiguous, horizon):
    """dead, alive, or censored at horizon; death AFTER a gap is unknown."""
    first=min((d for d,cause in death_by_id.get(sid,()) if t<d<=t+min(contiguous,horizon)),
              default=None)
    if first is not None:
        return "dead"
    return "alive" if contiguous>=horizon else "censored"

def axial_step(start,finish,w,h):
    """Recorded toroidal one-cell move, never a hypothetical legal option."""
    dx=(finish[0]-start[0])%w
    dy=(finish[1]-start[1])%h
    if (dx,dy)==(1,0):return (1,0)
    if (dx,dy)==(w-1,0):return (-1,0)
    if (dx,dy)==(0,1):return (0,1)
    if (dx,dy)==(0,h-1):return (0,-1)
    return None

def observed_first_action(frame0,frame1,sid,w,h):
    """Determine the actual first movement and straight/turn class."""
    snakes0=[s for s in frame0.get("snakes",())
             if s.get("id")==sid and s.get("alive")]
    snakes1=[s for s in frame1.get("snakes",())
             if s.get("id")==sid and s.get("alive")]
    if len(snakes0)!=1 or len(snakes1)!=1:
        return None
    old=snakes0[0].get("body") or []
    new=snakes1[0].get("body") or []
    if len(old)<2 or not new:
        return None
    head,neck,after=coord(old[0]),coord(old[1]),coord(new[0])
    if head is None or neck is None or after is None:
        return None
    previous=axial_step(neck,head,w,h)
    move=axial_step(head,after,w,h)
    if move is None:
        return None
    movement={(1,0):"+x",(-1,0):"-x",(0,1):"+y",(0,-1):"-y"}[move]
    if previous is None:
        style="unknown_heading"
    elif move==previous:
        style="straight"
    elif move==(-previous[0],-previous[1]):
        style="reverse"
    else:
        style="turn"
    return dict(movement=movement,turn_type=style)


def observed_followup(replay, season, replay_name, mode, sha):
    """One real danger state with explicitly censored future outcomes."""
    w,h=board_shape(replay)
    frames=snapshots_at(replay)
    deaths=first_death_by_id(replay)
    baseline,qc=review_replay(replay,season,replay_name,mode,sha)
    result=[]
    for row in baseline:
        t,sid=row["start_turn"],row["sid"]
        contiguous=continuous_turns(frames,t,HORIZONS[-1])
        if contiguous<10:
            qc["unexpected_incomplete_10"]+=1
            continue
        # A snake missing from a complete frame with NO earlier recorded death
        # is not safely surviving. Censor it rather than guessing its cause.
        for dt in range(1,contiguous+1):
            prior_death=any(t<death_turn<=t+dt for death_turn,cause in deaths.get(sid,()))
            if prior_death:
                break  # Once death is known, all later horizons are failed.
            if sid not in heads(frames[t+dt]):
                contiguous=dt-1
                qc["unexplained_disappearance_censored"]+=1
                break
        status={h:outcome_status(t,sid,deaths,contiguous,h) for h in HORIZONS}
        if (status[10]=="dead") != bool(row["death_next_10"]):
            qc["death_flag_disagreement"]+=1
            continue
        # Already-dead case stays dead at longer horizons; no respawn can erase it.
        if status[10]=="dead":
            assert all(status[h]=="dead" for h in HORIZONS)
        start=frames[t]
        measurements={}
        actual_first_action=(observed_first_action(start,frames[t+1],sid,w,h)
            if status[10]=="alive" or outcome_status(t,sid,deaths,contiguous,1)=="alive"
            else None)
        start_count=row["neighbor_exits"]
        start_nearest=row["nearest_head"]
        for step in STEPS:
            if step>contiguous:
                continue
            # Nonobserved because snake DIED in the interim, even if respawned.
            if outcome_status(t,sid,deaths,contiguous,step)!="alive":
                continue
            future=frames[t+step]
            self_now=heads(future).get(sid)
            if not self_now:
                qc["alive_without_head"]+=1
                continue
            pos=self_now[1]
            opponents=[v for otherid,v in heads(future).items() if otherid!=sid]
            near=min((distance(pos,item[1],w,h) for item in opponents),default=None)
            exits=unoccupied_neighbors(future,pos,w,h)
            apples=0
            for dt in range(1,step+1):
                for event in frames[t+dt].get("events",()):
                    if event.get("kind")=="ate" and event.get("snake")==sid:
                        apples+=1
            measurements[step]=dict(
                free_exits=exits,exit_change=exits-start_count,
                nearest_head=near,head_distance_change=near-start_nearest
                if near is not None else None,apples=apples,
                length=self_now[2])
        # Recording actual future labels does not imply those were known to a
        # player at baseline. No future measure enters matching/stratification.
        result.append(dict(
            season=season,replay=replay_name,sha=sha,mode=mode,
            student=row["student"],sid=sid,turn=t,
            length=row["length"],length_bin=row["length_bin"],
            head_pressure=row["head_pressure"],
            nearest_head=row["nearest_head"],
            free_exits=row["neighbor_exits"],
            confined=(row["neighbor_exits"]<=1),
            death_next_10=row["death_next_10"],
            continuous_followup=contiguous,
            status10=status[10],status20=status[20],status30=status[30],
            measurements=measurements,
            first_action=actual_first_action,
            all_death_events=deaths.get(sid,())))
        qc["long_horizon_baselines"]+=1
        qc["censored_30"]+=status[30]=="censored"
        qc["survived_10"]+=status[10]=="alive"
        qc["survived_30"]+=status[30]=="alive"
    return result,qc

def load(data_dir,max_files=250):
    candidates=sorted((data_dir/"replays").rglob("*.rep.gz"),reverse=True)
    selected=candidates[:max_files] if max_files else candidates
    qc=Counter(files=len(candidates),scanned=len(selected))
    seen=set()
    rows=[]
    for path in selected:
        rel=path.relative_to(data_dir/"replays")
        mode="trial" if "trials" in rel.parts else "league"
        season=rel.parts[0]
        try:
            with gzip.open(path,"rb") as f:raw=f.read()
            sha=hashlib.sha256(raw).hexdigest()
            if sha in seen:
                qc["replay_duplicates"]+=1
                continue
            game=json.loads(raw)
            obs,report=observed_followup(game,season,str(rel),mode,sha)
            seen.add(sha)
            qc.update(report)
            qc[mode+"_unique_replays"]+=1
            rows.extend(obs)
        except (OSError,ValueError,TypeError,KeyError):
            qc["unreadable_replays"]+=1
            continue
    qc["unique_replays"]=len(seen)
    return rows,qc

def survival_counts(rows,mode,subgroup=None):
    selected=[x for x in rows if x["mode"]==mode and
              (subgroup is None or subgroup(x))]
    s10=[r for r in selected if r["status10"]=="alive"]
    known30=[r for r in s10 if r["status30"]!="censored"]
    known20=[r for r in s10 if r["status20"]!="censored"]
    return dict(
        baseline=len(selected),death10=sum(r["status10"]=="dead" for r in selected),
        survived10=len(s10),known20=len(known20),
        alive20=sum(r["status20"]=="alive" for r in known20),
        late_death20=sum(r["status20"]=="dead" for r in known20),
        censored20=len(s10)-len(known20),known30=len(known30),
        alive30=sum(r["status30"]=="alive" for r in known30),
        late_death30=sum(r["status30"]=="dead" for r in known30),
        censored30=len(s10)-len(known30),
        replays=len({r["sha"] for r in selected}),
        students=len({r["student"] for r in selected}),
    )

def recovery_label(r,step=3):
    data=r["measurements"].get(step)
    if data is None:
        return None
    return "gained_exit" if data["exit_change"]>=1 else "did_not_gain"

def by_recovery(rows,mode,step=3):
    """Study AFTER the first 10 survived turns. Recovery is measured at +3.

    This prevents late outcome attribution to a snake already dead by +3.
    Right-censored 30-turn followups are reported, not assumed alive.
    """
    out={}
    for state in ("gained_exit","did_not_gain"):
        subset=[r for r in rows if r["mode"]==mode and
                r["status10"]=="alive" and recovery_label(r,step)==state]
        known=[r for r in subset if r["status30"]!="censored"]
        out[state]=dict(
            total10=len(subset),known30=len(known),
            died11to30=sum(r["status30"]=="dead" for r in known),
            alive30=sum(r["status30"]=="alive" for r in known),
            censored30=len(subset)-len(known),
            unique_replays=len({r["sha"] for r in subset}),
        )
    return out
