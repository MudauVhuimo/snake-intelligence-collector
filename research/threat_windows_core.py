"""Actual head pressure, local exits and subsequent death in Snake26 replays.

Observational design:
- An exposure is one *living STUDENT* sampled every 25 consecutive game turns.
- At the exposure frame: record distance to the nearest living opponent's head,
  body length and 0..4 immediately unoccupied toroidal neighboring cells.
- Outcome: does this same snake have a recorded 'died' event within the NEXT
  10 contiguous turns? Do not count a death on the exposure turn.
- Separate student-versus-student league from on-arrival benchmark matches.
- Deduplicate exact replay bytes with SHA-256, and report match counts.

No opponent intentions, hypothetical actions or private bot code are inferred.
"""
from collections import Counter,defaultdict
from pathlib import Path
import gzip
import hashlib
import json

STRIDE=25
HORIZON=10
LENGTH_BINS=("5-24","25-49","50-99","100+")

def length_band(n):
    if n<5:return None
    if n<25:return "5-24"
    if n<50:return "25-49"
    if n<100:return "50-99"
    return "100+"

def coord(p):
    if not isinstance(p,dict) or "x" not in p or "y" not in p:
        return None
    try:return int(p["x"]),int(p["y"])
    except (ValueError,TypeError):return None

def heads(frame):
    """id -> (name, head, body length); living and well-formed only."""
    found={}
    for snake in frame.get("snakes",[]):
        body=snake.get("body") or []
        if not snake.get("alive") or not body:
            continue
        sid, name=snake.get("id"),snake.get("name")
        pos=coord(body[0])
        if sid is None or not isinstance(name,str) or pos is None:
            continue
        found[sid]=(name,pos,len(body))
    return found

def distance(a,b,w,h):
    dx=abs(a[0]-b[0])
    dy=abs(a[1]-b[1])
    return min(dx,w-dx)+min(dy,h-dy)

def board_shape(replay):
    board=(replay.get("header") or {}).get("board") or [35,35]
    if not isinstance(board,(tuple,list)) or len(board)!=2:
        raise ValueError("Invalid board")
    w,h=int(board[0]),int(board[1])
    if not (3<=w<=1000 and 3<=h<=1000):
        raise ValueError("Invalid dimensions")
    return w,h

def unoccupied_neighbors(frame,pos,w,h):
    """Occupied NOW. Moving tails make this a conservative mobility proxy."""
    occupied=set()
    for s in frame.get("snakes",[]):
        if s.get("alive"):
            occupied.update(p for b in (s.get("body") or []) if (p:=coord(b)) is not None)
    occupied.update(p for b in (frame.get("obstacles") or []) if (p:=coord(b)) is not None)
    x,y=pos
    return sum(p not in occupied for p in
               (((x+1)%w,y),((x-1)%w,y),(x,(y+1)%h),(x,(y-1)%h)))

def category(nearest):
    if nearest<=3:return "near_0_3"
    if nearest<=7:return "middle_4_7"
    return "far_8_plus"

def scan_replay(replay,season,replay_path,mode,sha):
    w,h=board_shape(replay)
    frames=replay.get("frames")
    if not isinstance(frames,list) or len(frames)<HORIZON+1:
        raise ValueError("Insufficient frames")
    # Confirm historical 'league' games actually involve at least two students.
    roster={s.get("name") for f in frames[:1] for s in f.get("snakes",[])
            if isinstance(s.get("name"),str) and not s["name"].startswith("~")}
    if mode=="league" and len(roster)<2:
        return [],Counter(excluded_single_student_league=1)
    if mode=="trial" and len(roster)!=1:
        return [],Counter(excluded_nonstandard_trial=1)
    tmap={}
    for i,frame in enumerate(frames):
        t=frame.get("turn")
        if isinstance(t,int):
            tmap[t]=i
    # One recorded death event per snake/time. Never infer it from a low final length.
    death_times=defaultdict(set)
    for frame in frames:
        t=frame.get("turn")
        if not isinstance(t,int):continue
        for event in frame.get("events",[]):
            if event.get("kind")=="died" and event.get("snake") is not None:
                death_times[event["snake"]].add(t)
    output=[]
    qc=Counter()
    for before in frames:
        t=before.get("turn")
        if not isinstance(t,int) or t%STRIDE:
            continue
        # Explicitly require the next ten frames to have consecutive turn IDs.
        if any((t+k not in tmap or frames[tmap[t+k]].get("turn")!=t+k)
               for k in range(1,HORIZON+1)):
            qc["incomplete_followup"]+=1
            continue
        living=heads(before)
        if not living:
            continue
        # All alive body coordinates must be evaluated at this same instant.
        occupied=set()
        for s in before.get("snakes",[]):
            if s.get("alive"):
                occupied.update(p for b in (s.get("body") or []) if (p:=coord(b)) is not None)
        occupied.update(p for b in (before.get("obstacles") or []) if (p:=coord(b)) is not None)
        for sid,(name,head,bodylength) in living.items():
            if name.startswith("~"):continue
            other=[(distance(head,pos,w,h),id2,othername,olength)
                   for id2,(othername,pos,olength) in living.items() if sid!=id2]
            if not other:
                qc["no_live_opponent"]+=1
                continue
            nearest,opponent_id,other_name,other_length=min(other,key=lambda x:x[0])
            length=length_band(bodylength)
            if length is None:continue
            x,y=head
            exits=sum(p not in occupied for p in
                      (((x+1)%w,y),((x-1)%w,y),(x,(y+1)%h),(x,(y-1)%h)))
            upcoming=death_times.get(sid,set())
            died=any(t<event_t<=t+HORIZON for event_t in upcoming)
            output.append(dict(
                season=season,replay=replay_path,sha=sha,mode=mode,student=name,
                start_turn=t,length=bodylength,length_bin=length,
                nearest_head=nearest,nearest_type="benchmark" if other_name.startswith("~") else "student",
                nearest_opponent=other_name,neighbor_exits=exits,
                head_pressure=category(nearest),death_next_10=int(died),
                died_event_count=len(upcoming)))
            qc["observed_windows"]+=1
            qc["future_death_windows"]+=int(died)
    return output,qc

def load(data_dir,max_files=250):
    paths=sorted((data_dir/"replays").rglob("*.rep.gz"),reverse=True)
    selected=paths[:max_files] if max_files else paths
    seen=set()
    qc=Counter(files=len(paths),files_scanned=len(selected))
    rows=[]
    for path in selected:
        rel=path.relative_to(data_dir/"replays")
        season=rel.parts[0] if rel.parts else "unknown"
        mode="trial" if "trials" in rel.parts else "league"
        try:
            with gzip.open(path,"rb") as f:raw=f.read()
            sha=hashlib.sha256(raw).hexdigest()
            if sha in seen:
                qc["duplicate_replays"]+=1
                continue
            replay=json.loads(raw)
            observations,q=scan_replay(replay,season,str(rel),mode,sha)
            seen.add(sha)
        except (OSError,TypeError,KeyError,ValueError):
            qc["unreadable"]+=1
            continue
        qc["unique_replays"]+=1
        qc[mode+"_unique_replays"]+=1
        qc.update(q)
        rows.extend(observations)
    return rows,qc

def summarize(rows):
    grouped=defaultdict(list)
    for row in rows:
        grouped[(row["mode"],row["head_pressure"])].append(row)
    result={}
    for mode in ("league","trial"):
        for bucket in ("near_0_3","middle_4_7","far_8_plus"):
            records=grouped[mode,bucket]
            died=sum(x["death_next_10"] for x in records)
            result[mode,bucket]=dict(n=len(records),died=died,
                                    risk=100*died/len(records) if records else None,
                                    matches=len({x["sha"] for x in records}),
                                    students=len({x["student"] for x in records}))
    return result

def per_student(rows):
    grouped=defaultdict(list)
    for row in rows:
        grouped[(row["season"],row["student"],row["mode"])].append(row)
    output=[]
    for (season,student,mode),group in sorted(grouped.items()):
        n=len(group)
        near=sum(x["head_pressure"]=="near_0_3" for x in group)
        confined=sum(x["neighbor_exits"]<=1 for x in group)
        deaths=sum(x["death_next_10"] for x in group)
        output.append(dict(season=season,student=student,mode=mode,
            sampled_windows=n,replays=len({x["sha"] for x in group}),
            close_head_windows=near,close_head_fraction=near/n,
            limited_exits_windows=confined,limited_exits_fraction=confined/n,
            death_within_10_windows=deaths,death_within_10_fraction=deaths/n))
    return output
