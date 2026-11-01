"""Observed food episodes in public Snake26 replay frames.

Only matches a consumed apple if an 'ate' event and the next head both
identify its previous board coordinate. No hypothetical actions are simulated.
"""
from collections import Counter, defaultdict
from pathlib import Path
import gzip
import hashlib
import json

BANDS=("Student 3+ closer","Student 1-2 closer","Equal",
       "Benchmark 1-2 closer","Benchmark 3+ closer")
LAGS=("1-5","6-10","11-20","21-40","41-100","101+")

def points(items):
    return {(p["x"],p["y"]) for p in items or []
            if isinstance(p,dict) and isinstance(p.get("x"),int)
            and isinstance(p.get("y"),int)}

def dist(a,b,w,h):
    dx,dy=abs(a[0]-b[0]),abs(a[1]-b[1])
    return min(dx,w-dx)+min(dy,h-dy)

def group(name):
    return "Benchmark" if name.startswith("~") else "Student"

def heads(frame):
    result={}
    for snake in frame.get("snakes",[]):
        body=snake.get("body") or []
        if snake.get("alive") and body and snake.get("id") is not None and snake.get("name"):
            first=body[0]
            if "x" in first and "y" in first:
                result[snake["id"]]=(str(snake["name"]),(int(first["x"]),int(first["y"])))
    return result

def first_seen(frame,pos,w,h):
    distances=sorted((dist(head,pos,w,h),name,sid,group(name))
                     for sid,(name,head) in heads(frame).items())
    student=next((d for d,n,s,g in distances if g=="Student"),None)
    bench=next((d for d,n,s,g in distances if g=="Benchmark"),None)
    return dict(turn=frame.get("turn"),distances=distances,
                student_d=student,benchmark_d=bench)

def advantage_band(adv):
    if adv<=-3:return BANDS[0]
    if adv<0:return BANDS[1]
    if adv==0:return BANDS[2]
    if adv<=2:return BANDS[3]
    return BANDS[4]

def lag_band(lag):
    if lag<=5:return LAGS[0]
    if lag<=10:return LAGS[1]
    if lag<=20:return LAGS[2]
    if lag<=40:return LAGS[3]
    if lag<=100:return LAGS[4]
    return LAGS[5]

def replay_food_events(replay):
    frames=replay.get("frames",[])
    board=(replay.get("header") or {}).get("board") or [35,35]
    w,h=map(int,board)
    if w<3 or h<3 or not isinstance(frames,list) or len(frames)<2:
        raise ValueError("Invalid replay geometry or frames")
    active={}
    qc=Counter()
    rows=[]
    for before,after in zip(frames,frames[1:]):
        t=before.get("turn")
        if not isinstance(t,int) or after.get("turn")!=t+1:
            qc["discontinuities"]+=1
            active={}
            continue
        pre=points(before.get("food"))
        post=points(after.get("food"))
        for pos in pre:
            if pos not in active:
                active[pos]=first_seen(before,pos,w,h)
                qc["first_visible"]+=1
        removed=pre-post
        next_heads=heads(after)
        eat_ids={e.get("snake") for e in after.get("events",[])
                 if e.get("kind")=="ate"}
        for pos in removed:
            qc["disappeared"]+=1
            matches=[(name,sid) for sid,(name,head) in next_heads.items()
                     if sid in eat_ids and head==pos]
            if len(matches)!=1:
                qc["unmatched"]+=1
                continue
            name,sid=matches[0]
            observed=active.get(pos)
            if not observed or not isinstance(observed["turn"],int):
                qc["missing_start"]+=1
                continue
            lag=after["turn"]-observed["turn"]
            if lag<1:
                qc["invalid_lag"]+=1
                continue
            sd,bd=observed["student_d"],observed["benchmark_d"]
            row=dict(group=group(name),winner=name,lag=lag,
                     student_d=sd,benchmark_d=bd,advantage=None,band=None,
                     contested=False,starting_winner_dist=None)
            row["starting_winner_dist"]=next(
                (d for d,n,i,g in observed["distances"] if i==sid),None)
            if sd is not None and bd is not None:
                adv=sd-bd
                row["advantage"]=adv
                row["band"]=advantage_band(adv)
                row["contested"]=abs(adv)<=2 and min(sd,bd)<=10
            rows.append(row)
            qc["matched"]+=1
        for pos in removed:
            active.pop(pos,None)
        active={pos:v for pos,v in active.items() if pos in post}
    return rows,qc

def scan(data_dir,max_files=250):
    files=sorted((data_dir/"replays").rglob("*.rep.gz"),reverse=True)
    selected=files[:max_files] if max_files else files
    seen=set()
    quality=Counter(files=len(files),scanned=len(selected))
    modes=defaultdict(list)
    for path in selected:
        rel=path.relative_to(data_dir/"replays")
        mode="On-arrival" if "trials" in rel.parts else "League"
        try:
            with gzip.open(path,"rb") as f:
                raw=f.read()
            digest=hashlib.sha256(raw).hexdigest()
            if digest in seen:
                quality["duplicates"]+=1
                continue
            replay=json.loads(raw)
            rows,counters=replay_food_events(replay)
            seen.add(digest)
        except (OSError,ValueError,KeyError,TypeError):
            quality["invalid"]+=1
            continue
        quality["unique"]+=1
        quality.update(counters)
        modes[mode].extend(rows)
    return quality,modes
