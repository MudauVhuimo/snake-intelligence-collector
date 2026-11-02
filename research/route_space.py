"""Real-action route-space comparison for ALL Snake26 student competitors.

Input: the previously audited 10/20/30-turn danger-window CSV.
We re-open EXACT archived replay frames and compute competing FIRST-MOVE
features using only PRE-decision geometry:
- currently empty neighbors, frozen-body postmove flood-fill,
- 8-step no-growth OWN-moving-body beam reach; other snakes frozen.
The latter is NOT legal-engine simulation, future opponent prediction,
or a counterfactual benefit of an unchosen move.
Source games are SHA-deduplicated; league and trials stay separate.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from datetime import datetime,timezone
from pathlib import Path
from statistics import mean
from html import escape
import argparse,csv,gzip,hashlib,json,random,sqlite3

from .competitive_cohorts import ranks
from .league_comparison import chart
from .route_space_core import (
    scene_from_frame,scene_metrics,rank_choice,validate_plain_transition)
from .threat_windows_core import coord
from .opponent_cone_core import (
    opponent_cones,summarize_candidates,candidate_profile,
    actual_choice_risk,check_opponent_next_heads,audit_next_head_death,
    head_to_head_lengths)

FEATURES=(("static","Frozen-body flood-fill"),("tail","Own-tail 8-step beam reach"))
MEASURES=(("free_exits","Current unoccupied neighbors"),
          ("best_frozen","Best frozen-body flood-fill"),
          ("best_tail","Best no-growth moving-tail beam reach"))

def read_csv(path):
    if not path.exists():return []
    with path.open(newline="",encoding="utf-8") as file:
        return list(csv.DictReader(file))

def write_csv(path,rows,fields=None):
    path.parent.mkdir(parents=True,exist_ok=True)
    cols=fields or (list(rows[0]) if rows else ["mode","student","replay_sha","turn"])
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

def observed_by_name(frame,student):
    hits=[s for s in frame.get("snakes",()) if s.get("name")==student
          and s.get("id") is not None and s.get("alive") and s.get("body")]
    return hits[0] if len(hits)==1 else None

def get_next_head(frame,sid):
    if frame is None:return None
    hits=[s for s in frame.get("snakes",()) if s.get("id")==sid
          and s.get("alive") and s.get("body")]
    return (hits[0] if len(hits)==1 else None)

def one_window(replay,frames,window,cohort,quality,audited_opponents=None):
    t=int(window["turn"])
    frame=frames.get(t)
    if frame is None:
        quality["missing_frame"]+=1
        return None
    current=observed_by_name(frame,window["student"])
    if not current:
        quality["missing_student"]+=1
        return None
    sid=current["id"]
    scene=scene_from_frame(replay,frame,sid)
    if scene is None:
        quality["invalid_scene"]+=1
        return None
    if len(set(scene.own))!=len(scene.own):
        quality["repeated_tail_accepted"]+=1
    alternatives=scene_metrics(scene)
    # Opponent reach sets use ONLY present-frame head/neck and length.
    cones=opponent_cones(frame,sid,scene.width,scene.height)
    options=summarize_candidates(alternatives,cones,len(scene.own))
    profile=candidate_profile(options)
    following=frames.get(t+1)
    after=get_next_head(following,sid)
    observed_head=coord(after["body"][0]) if after else None
    selected_risk=actual_choice_risk(options,observed_head)
    first_death=audit_next_head_death(following,sid)
    quality["first_step_"+first_death]+=1
    if audited_opponents is not None:
        fresh={opp_id:c for opp_id,c in cones.items()
               if (t,opp_id) not in audited_opponents}
        audited_opponents.update((t,opp_id) for opp_id in fresh)
        excluded={e.get("snake") for e in (following or {}).get("events",())
                  if e.get("kind") in ("died","respawned")}
        quality.update(check_opponent_next_heads(fresh,following,excluded))
    quality["candidate_threatened"]+=sum(x["head_cone"] for x in options)
    quality["candidate_total"]+=len(options)
    quality["unknown_heading_opponents"]+=sum(not x["known_heading"] for x in cones.values())
    observed=(rank_choice(alternatives,observed_head,"frozen"),
              rank_choice(alternatives,observed_head,"tail"))
    if observed_head is not None and any(x is None for x in observed):
        quality["observed_outside_projection"]+=1
    if observed_head is None:quality["observed_next_head_missing"]+=1
    if following and after:
        ate=any(e.get("snake")==sid and e.get("kind")=="ate"
                for e in following.get("events",()))
        next_body=tuple(coord(x) for x in after["body"])
        verdict=validate_plain_transition(scene.own,next_body,ate)
        if verdict is not None:
            quality["plain_shift_checked"]+=1
            quality["plain_shift_valid"]+=int(verdict)
            quality["plain_shift_invalid"]+=int(not verdict)
    mode=window["mode"]
    death10=window["outcome10"]
    death30=window["outcome30"]
    if death10 not in ("alive","dead","censored"):
        quality["invalid_label"]+=1
        return None
    modelable=len(alternatives)
    frozen=[x["frozen"] for x in alternatives]
    moving=[x["tail"] for x in alternatives]
    ostatic,otail=observed
    quality[mode+"_windows"]+=1
    quality[mode+"_first_moves_measured"]+=int(otail is not None)
    quality[mode+"_no_candidate"]+=int(modelable==0)
    quality[mode+"_choice_discriminative"]+=int(
        otail is not None and otail["discriminative"])
    return dict(
        season=window["season"],mode=mode,replay_sha=window["replay_sha"],
        replay=window["replay"],student=window["student"],turn=t,
        cohort=cohort or "unranked",length=int(window["length"]),
        length_band=window["length_band"],
        near_head=int(window["nearest_head"])<=3,
        free_exits=int(window["free_exits"]),
        phase=t//500,death10=death10,death30=death30,
        candidate_count=modelable,
        opponent_heads=len(cones),
        unknown_opponent_headings=sum(not c["known_heading"] for c in cones.values()),
        threatened_count=profile["threatened_count"],
        nonweaker_threatened_count=profile["nonweaker_threatened_count"],
        uncontested_count=profile["uncontested_count"],
        nonweaker_free_count=profile["nonweaker_free_count"],
        all_cone=profile["all_cone"],
        all_nonweaker_cone=profile["all_nonweaker_cone"],
        best_uncontested_tail=profile["best_uncontested_tail"],
        best_nonweaker_free_tail=profile["best_nonweaker_free_tail"],
        tail_best_requires_cone=profile["tail_best_requires_cone"],
        top_tail_has_uncontested=profile["top_tail_has_uncontested"],
        first_step_death_cause=first_death,
        chosen_cone=(selected_risk.get("chosen_cone") if selected_risk["observed"] else None),
        chosen_nonweaker_cone=(selected_risk.get("chosen_nonweaker_cone")
                              if selected_risk["observed"] else None),
        chosen_longer_cone=(selected_risk.get("chosen_longer_cone")
                           if selected_risk["observed"] else None),
        best_frozen=max(frozen,default=0),
        best_tail=max(moving,default=0),
        frozen_spread=max(frozen,default=0)-min(frozen,default=0),
        tail_spread=max(moving,default=0)-min(moving,default=0),
        actual_move_observed=otail is not None,
        chosen_frozen=ostatic["value"] if ostatic else None,
        chosen_tail=otail["value"] if otail else None,
        chosen_frozen_rank=ostatic["rank"] if ostatic else None,
        chosen_tail_rank=otail["rank"] if otail else None,
        chosen_frozen_regret=ostatic["regret"] if ostatic else None,
        chosen_tail_regret=otail["regret"] if otail else None,
        chosen_top_frozen=(ostatic["top"] if ostatic and ostatic["discriminative"] else None),
        chosen_top_tail=(otail["top"] if otail and otail["discriminative"] else None),
        chosen_frozen_discriminative=bool(ostatic and ostatic["discriminative"]),
        chosen_tail_discriminative=bool(otail and otail["discriminative"]),
        candidate_food_count=sum(x["next_head"] in scene.food for x in alternatives),
        candidate_tail_entry=sum(x["next_head"]==scene.own[-1] for x in alternatives))

def extract(data_dir,max_files=250):
    """Reuse existing audited deduplicated danger windows, no re-sampling."""
    raw=read_csv(data_dir/"derived"/"long_horizon_danger_windows.csv")
    if not raw:
        # Some integration fixtures contain catalogs but no full replay files.
        # Publish explicitly empty/insufficient results rather than fabricate.
        return [],Counter(source_danger_windows=0,modeled_rows=0,unique_replays=0)
    from .competitive_cohorts import ranks
    with sqlite3.connect(data_dir/"snake.db") as db:
        official=ranks(db)
    selected_replays=sorted({r["replay"] for r in raw})[:max_files] if max_files else sorted(
        {r["replay"] for r in raw})
    allowed=set(selected_replays)
    rows=defaultdict(list)
    for row in raw:
        if row["replay"] in allowed:
            rows[row["replay"]].append(row)
    results=[]
    quality=Counter(source_danger_windows=len(raw),chosen_replay_paths=len(rows))
    seen_sha=set()
    for rel,windows in sorted(rows.items()):
        file=data_dir/"replays"/rel
        try:
            with gzip.open(file,"rb") as f:content=f.read()
            digest=hashlib.sha256(content).hexdigest()
            if any(window["replay_sha"]!=digest for window in windows):
                quality["sha_mismatch"]+=1
                continue
            if digest in seen_sha:
                quality["duplicate_replays"]+=1
                continue
            replay=json.loads(content)
            frames={f["turn"]:f for f in replay.get("frames",[])
                    if isinstance(f.get("turn"),int)}
            if not frames:raise ValueError("No turn frames")
        except (OSError,ValueError,KeyError,TypeError):
            quality["invalid_replays"]+=1
            continue
        seen_sha.add(digest)
        mode=windows[0]["mode"]
        quality[mode+"_unique_replays"]+=1
        # Every recorded head-on victim event is counted once per unique replay.
        for after_frame in replay.get("frames",()):
            turn=after_frame.get("turn")
            prev=frames.get(turn-1) if isinstance(turn,int) else None
            for event in after_frame.get("events",()):
                outcome=head_to_head_lengths(prev,event)
                if outcome is not None:
                    quality[mode+"_h2h_victim_events"]+=1
                    quality["head_on_"+outcome["relation"]]+=1
        audited_opponents=set()
        for win in windows:
            try:
                rank=official.get((win["season"],win["student"]))
                row=one_window(replay,frames,win,rank["cohort"] if rank else None,
                               quality,audited_opponents)
                if row:
                    results.append(row)
            except (KeyError,ValueError,TypeError):
                quality["invalid_window"]+=1
    quality["unique_replays"]=len(seen_sha)
    quality["modeled_rows"]=len(results)
    return results,quality

def auc(records,feature):
    """Exact tie-corrected Mann–Whitney ROC AUC: higher => more death risk.

    Sorting avoids quadratic death x survival comparisons in a match bootstrap.
    """
    ordered=sorted((r[feature],int(r["death10"]=="dead"))
                   for r in records if r["death10"] in ("alive","dead")
                   and r[feature] is not None)
    npos=sum(label for value,label in ordered)
    nneg=len(ordered)-npos
    if not npos or not nneg:return None
    rank_sum=0.0
    i=0
    while i<len(ordered):
        j=i+1
        while j<len(ordered) and ordered[j][0]==ordered[i][0]:
            j+=1
        positive=sum(label for value,label in ordered[i:j])
        rank_sum+=positive*(i+1+j)/2
        i=j
    return (rank_sum-npos*(npos+1)/2)/(npos*nneg)

def replay_bootstrap_auc_difference(rows,first,second,draws=1000,seed=2026):
    """Bootstrap WHOLE replay clusters for paired univariate AUC difference.

    Comparisons are on identical observed windows; scores fixed before outcomes.
    Intervals do NOT adjust repeated bot versions or hypothesis selection.
    """
    grouped=defaultdict(list)
    for r in rows:grouped[r["replay_sha"]].append(r)
    shas=sorted(grouped)
    result=dict(replay_clusters=len(shas),draws=0,low=None,high=None,
                observed=None)
    risk=lambda records,key:[{**r,"risk":-r[key]} for r in records]
    a=auc(risk(rows,first),"risk")
    b=auc(risk(rows,second),"risk")
    result["observed"]=a-b if a is not None and b is not None else None
    if len(shas)<8:return result
    rng=random.Random(seed)
    samples=[]
    for _ in range(draws):
        rs=[r for sha in rng.choices(shas,k=len(shas)) for r in grouped[sha]]
        a=auc(risk(rs,first),"risk")
        b=auc(risk(rs,second),"risk")
        if a is not None and b is not None:samples.append(a-b)
    samples.sort()
    if len(samples)>=draws//2:
        result["draws"]=len(samples)
        result["low"]=samples[int(.025*(len(samples)-1))]
        result["high"]=samples[int(.975*(len(samples)-1))]
    return result

def eval_records(rows):
    """Negative sign converts bigger mobility to lower predicted risk."""
    transformed=[{**r,**{"risk_"+key:-r[key] for key,_ in MEASURES}} for r in rows]
    return {key:auc(transformed,"risk_"+key) for key,_ in MEASURES}

def holdout(rows):
    """Fixed hash-split at REPLAY level, independent of observed outcome."""
    return [r for r in rows if int(r["replay_sha"][:8],16)%5==0]

def cohort_metrics(rows):
    by=defaultdict(list)
    for r in rows:by[r["mode"],r["cohort"]].append(r)
    output=[]
    for mode in ("league","trial"):
        for cohort in ("top_quartile","middle_half","bottom_quartile","unranked"):
            part=by[mode,cohort]
            actual=[r for r in part if r["actual_move_observed"]]
            informative=[r for r in actual if r["chosen_tail_discriminative"]]
            frozen_info=[r for r in actual if r["chosen_frozen_discriminative"]]
            def frac(items,key):
                return 100*sum(bool(x[key]) for x in items)/len(items) if items else None
            output.append(dict(
                mode=mode,cohort=cohort,windows=len(part),
                distinct_replays=len({r["replay_sha"] for r in part}),
                distinct_students=len({r["student"] for r in part}),
                moves=len(actual),informative_tail=len(informative),
                informative_frozen=len(frozen_info),
                chose_best_tail_pct=frac(informative,"chosen_top_tail"),
                chose_best_frozen_pct=frac(frozen_info,"chosen_top_frozen"),
                mean_tail_rank=mean(x["chosen_tail_rank"] for x in actual)
                if actual else None,
                mean_frozen_rank=mean(x["chosen_frozen_rank"] for x in actual)
                if actual else None,
                death10=sum(r["death10"]=="dead" for r in part)))
    return output

def pair_source_decisions(data_dir,rows):
    """Cross-reference prior SAME-MATCH baseline pairs; only exact student-turn keys."""
    source=read_csv(data_dir/"derived"/"competitive_matched_decisions.csv")
    index={(r["replay_sha"],r["student"],str(r["turn"])):r for r in rows}
    matched=[]
    for case in source:
        sha=case["replay_sha"]
        top=index.get((sha,case["top_student"],case["top_turn"]))
        bottom=index.get((sha,case["bottom_student"],case["bottom_turn"]))
        if top is None or bottom is None:
            continue
        matched.append((top,bottom))
    return matched

def pair_contrast(pairs,key,seed=2026,draws=1000):
    """Observed bottom minus top in SAME GAME, bootstrap complete game units."""
    bygame=defaultdict(list)
    for top,bottom in pairs:
        a,b=top.get(key),bottom.get(key)
        if a is None or b is None:continue
        bygame[top["replay_sha"]].append(float(b)-float(a))
    games=sorted(bygame)
    observed=[v for vals in bygame.values() for v in vals]
    result=dict(pairs=len(observed),matches=len(games),
                difference=mean(observed) if observed else None,low=None,high=None)
    if len(games)<8:return result
    rng=random.Random(seed)
    means=[]
    for _ in range(draws):
        sample=[v for game in rng.choices(games,k=len(games)) for v in bygame[game]]
        means.append(mean(sample))
    means.sort()
    result["low"]=means[int(.025*(len(means)-1))]
    result["high"]=means[int(.975*(len(means)-1))]
    return result

def fmt(v,suffix="",precision=2):
    return "insufficient" if v is None else f"{v:.{precision}f}{suffix}"

def draw_chart(path,cohorts):
    data={(r["mode"],r["cohort"]):r for r in cohorts}
    labels=("top_quartile","middle_half","bottom_quartile")
    body=['<line x1="99" y1="380" x2="924" y2="380" stroke="#64748b"/>',
          '<text x="90" y="76">Share choosing highest modeled 8-step reach, only discriminative choices</text>',
          '<text x="90" y="96">Frozen opponents, no food growth; NOT a verified legal-move policy</text>']
    for i,cohort in enumerate(labels):
        x=215+i*275
        body.append(f'<text x="{x+32}" y="414" text-anchor="middle">'
                    f'{("Top 25%","Middle 50%","Bottom 25%")[i]}</text>')
        for j,(mode,color) in enumerate((("league","#60a5fa"),("trial","#fbbf24"))):
            r=data[mode,cohort]
            val=r["chose_best_tail_pct"]
            xj=x+j*70
            if val is None:
                body.append(f'<text x="{xj+25}" y="361">n/a</text>')
                continue
            h=val*2.5
            body.append(f'<rect x="{xj}" y="{380-h:.1f}" width="51" '
                        f'height="{h:.1f}" rx="3" fill="{color}"/>')
            body.append(f'<text x="{xj+25}" y="{367-h:.1f}" text-anchor="middle">'
                        f'{val:.1f}%</text>')
    body+=['<rect x="708" y="53" width="12" height="12" fill="#60a5fa"/>',
           '<text x="725" y="64">League</text>',
           '<rect x="811" y="53" width="12" height="12" fill="#fbbf24"/>',
           '<text x="828" y="64">Trials</text>']
    chart(path,"Observed choices of modeled route-space options",body,450)

def build(data_dir,max_files=250):
    data_dir=Path(data_dir)
    rows,qc=extract(data_dir,max_files)
    cohorts=cohort_metrics(rows)
    all_league=[r for r in rows if r["mode"]=="league"]
    all_trial=[r for r in rows if r["mode"]=="trial"]
    whole={mode:eval_records(part) for mode,part in
           (("league",all_league),("trial",all_trial))}
    unseen={mode:eval_records(holdout(part)) for mode,part in
            (("league",all_league),("trial",all_trial))}
    holdouts={mode:holdout(part) for mode,part in
              (("league",all_league),("trial",all_trial))}
    bootstrap={label:replay_bootstrap_auc_difference(holdouts["league"],left,right)
               for label,left,right in (
                   ("tail_minus_frozen","best_tail","best_frozen"),
                   ("tail_minus_neighbors","best_tail","free_exits"),
                   ("frozen_minus_neighbors","best_frozen","free_exits"))}
    matches=pair_source_decisions(data_dir,rows)
    paired={key:pair_contrast(matches,key) for key in
            ("chosen_tail_rank","chosen_frozen_rank",
             "chosen_top_tail","chosen_top_frozen")}
    output=data_dir/"derived"
    write_csv(output/"route_choice_windows.csv",rows)
    write_csv(output/"route_choice_cohorts.csv",cohorts)
    report=data_dir/"reports"
    draw_chart(report/"charts"/"route_choice_cohorts.svg",cohorts)
    lines=[
        "# Snake26: Do strong snakes choose routes with more future space?","",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
        "## Research question","",
        "Across ALL student snakes, does the ACTUAL first move after a",
        "dangerous position preserve a larger possible future escape region?",
        "Does modeled future space predict recorded deaths more usefully than",
        "simply counting today's unoccupied neighboring cells?",
        "",
        "## What the model DOES and DOES NOT simulate","",
        "For each sampled alive snake: enumerate possible next head positions",
        "under a simplified no-growth, stationary-opponent projection.",
        "Freeze OTHER snake bodies/obstacles. Compare:",
        "1. **Frozen-body flood fill:** after each candidate first step,",
        "   count connected currently-unoccupied cells (all bodies frozen).",
        "2. **Tail-aware 8-step beam:** shift the OWN body one cell after",
        "   every projected step, allowing tail cells to vacate (including",
        "   legitimate repeated terminal coordinates during prior growth).",
        "   Keep at most"
        "   64 distinct body states per depth with at most two states per head.",
        "   Count distinct projected head positions reached over eight steps.",
        "   Deterministic beam pruning means the count is approximate.",
        "**Neither metric predicts opponent actions or food consumption/growth.**",
        "Both are diagnostic geometry proxies, NOT engine-verified legal",
        "routes, safe next moves, or alternative realities. The 8-step beam",
        "counts positions across hypothetical paths, not a single escape route.",
        "An actual apple could prevent the modeled tail from vacating.",
        "The rank of the ACTUAL recorded first move is measured ONLY when",
        "that snake has a valid recorded head on the NEXT frame. Missing",
        "or dead-next-turn moves are excluded from choice comparisons.",
        "Real death outcomes (next 10 turns) remain separate recorded labels.",
        "",
        "## Coverage and validation of ordinary body shifts","",
        f"Source danger-window observations: **{qc['source_danger_windows']:,}**.",
        f"Unique replay payloads WITH danger observations: **{qc['unique_replays']}**",
        f"(league {qc['league_unique_replays']}, trials {qc['trial_unique_replays']}).",
        f"Audited dangerous windows: **{qc['modeled_rows']:,}**",
        f"(league {qc['league_windows']}, trial {qc['trial_windows']}).",
        f"Observed first movements in model alternatives: league "
        f"**{qc['league_first_moves_measured']}**, trials "
        f"**{qc['trial_first_moves_measured']}**.",
        f"First moves missing because of death/absence: "
        f"**{qc['observed_next_head_missing']}**.",
        f"Observed valid heads outside the simplified model: "
        f"**{qc['observed_outside_projection']}** (NOT silently made legal).",
        f"Recognized duplicated terminal tail cells during growth: "
        f"**{qc['repeated_tail_accepted']}**.",
        f"Invalid scene/body shape: **{qc['invalid_scene']}**.",
        f"Missing frame/student: **{qc['missing_frame']+qc['missing_student']}**.",
        f"Invalid source windows: **{qc['invalid_window']}**.",
        f"SHA mismatch / unreadable replay: **{qc['sha_mismatch']+qc['invalid_replays']}**.",
        "Any skipped rows remain excluded rather than silently designated safe.",
        f"Plain no-food-growth actual body transitions consistent with shift: "
        f"**{qc['plain_shift_valid']}/{qc['plain_shift_checked']}**.",
        f"Modeled windows with no next candidates: **{qc['league_no_candidate']+qc['trial_no_candidate']}**.",
        "",
        "## 1. Choices of high predicted future space by actual league/trial bots","",
        "![Share of first moves choosing best modeled tail reach](charts/route_choice_cohorts.svg)","",
        "| Mode | Official Division 1 cohort | Students | Replays | Dangerous frames | Actual moves | Informative route comparisons | Choose max tail-reach | Choose max frozen flood-fill |",
        "|---|---|---:|---:|---:|---:|---:|---|---|"]
    for r in cohorts:
        lines.append(f"| {r['mode']} | {r['cohort']} | {r['distinct_students']} | "
                     f"{r['distinct_replays']} | {r['windows']} | {r['moves']} | "
                     f"{r['informative_tail']} | {fmt(r['chose_best_tail_pct'],'%')} | "
                     f"{fmt(r['chose_best_frozen_pct'],'%')} |")
    lines+=["",
        "A candidate is **informative** only if alternative first moves have",
        "different modeled scores; all-tie cases cannot demonstrate a",
        "policy preference. Choosing the maximal modeled option is NOT proof",
        "that that action was strategically optimal.",
        "",
        "## 2. Can baseline route features predict actual +10 death?","",
        "ROC AUC measures how often a dangerous observation is ranked above a",
        "non-death by its negative mobility score. 0.5 is chance, 1 perfect.",
        "These are FIXED univariate features (no fit on this archive),",
        "shown both overall and in a deterministic whole-replay hash holdout",
        "(SHA prefix modulo 5 = 0). Because feature ideas were devised using",
        "earlier archive results, this holdout is only a preliminary audit.",
        "",
        "| Environment | Predictor (lower mobility => more risk) | All archive AUC | Fixed replay-holdout AUC | Holdout windows | Holdout death events |",
        "|---|---|---:|---:|---:|---:|"]
    for mode in ("league","trial"):
        test=holdouts[mode]
        for key,label in MEASURES:
            lines.append(f"| {mode} | {label} | "
                         f"{fmt(whole[mode][key])} | {fmt(unseen[mode][key])} | "
                         f"{len(test)} | {sum(r['death10']=='dead' for r in test)} |")
    lines+=["",
        "## 2a. Whole-game bootstrap: how reliable is the holdout difference?","",
        "Use exactly the SAME held-out dangerous league frames for both",
        "predictors. Repeatedly sample entire replay games, preserving",
        "within-match correlation instead of resampling individual turns.",
        "Intervals are exploratory and do not control for repeated bot versions",
        "or feature engineering influenced by this historical archive.",
        "",
        "| Holdout league contrast | Observed AUC advantage | Replay-bootstrap 95% interval | Games |",
        "|---|---:|---|---:|"]
    for label,title in (
        ("tail_minus_frozen","Moving-tail reach minus frozen flood-fill"),
        ("tail_minus_neighbors","Moving-tail reach minus free neighbors"),
        ("frozen_minus_neighbors","Frozen flood-fill minus free neighbors")
    ):
        b=bootstrap[label]
        ci=(f"[{b['low']:+.3f}, {b['high']:+.3f}]"
            if b["low"] is not None else "insufficient replay clusters")
        lines.append(f"| {title} | {fmt(b['observed'],precision=3)} | "
                     f"{ci} | {b['replay_clusters']} |")
    lines += ["",
        "A confidence interval crossing ZERO means the data do not establish",
        "that a more complicated feature is actually superior.",
        "",
        "## 2b. Sensitivity to current body length","",
        "Length can change the meaning of 'room to move'; report all bins",
        "rather than assuming one universally useful mobility estimator.","",
        "| League body length | Observed danger windows | 10-turn deaths | Free neighbors AUC | Frozen flood-fill AUC | Moving-tail reach AUC |",
        "|---|---:|---:|---:|---:|---:|"]
    for length in ("5-24","25-49","50-99","100+"):
        part=[r for r in all_league if r["length_band"]==length]
        values=eval_records(part)
        lines.append(f"| {length} | {len(part)} | "
                     f"{sum(r['death10']=='dead' for r in part)} | "
                     f"{fmt(values['free_exits'])} | "
                     f"{fmt(values['best_frozen'])} | {fmt(values['best_tail'])} |")
    lines+=["",
        "Small snakes and long snakes can differ; individual bins have few",
        "death events, so these figures are NOT verified optimal thresholds.",
        "",
        "Univariate AUC is NOT a calibrated hazard model. Match/body length",
        "food density, opponent strength and available routes affect every",
        "candidate feature. A test with no deaths cannot produce an AUC.",
        "",
        "## 3. Same real game and baseline-matched strong/struggling choices","",
        "Use prior non-reused top-versus-bottom matched decisions, selected by",
        "same replay, length band, head closeness, confinement and game phase.",
        f"Matched SAME-GAME pairs with route profiles: **{len(matches)}**.",
        "Differences below are **bottom minus top**, where higher choice",
        "rank means a modeled option preserved more projected future space.",
        "Resampling full replay clusters gives exploratory intervals.",
        "",
        "| Recorded decision measure | Both sides observed | Unique replay clusters | Bottom minus top | Replay bootstrap 95% interval |",
        "|---|---:|---:|---:|---:|"]
    for key,label,unit in (
        ("chosen_tail_rank","Tail-aware modeled choice percentile",""),
        ("chosen_frozen_rank","Frozen flood-fill choice percentile",""),
        ("chosen_top_tail","Chose highest modeled tail space",""),
        ("chosen_top_frozen","Chose highest frozen area","")):
        p=paired[key]
        ci=(f"[{p['low']:+.3f}, {p['high']:+.3f}]"
            if p["low"] is not None else "insufficient independent matches")
        lines.append(f"| {label} | {p['pairs']} | {p['matches']} | "
                     f"{fmt(p['difference'],precision=3)} | {ci} |")
    lines+=["",
        "Pairs remain nonidentical board states, even inside one game;",
        "differences are descriptive only. In particular, moving opponents,",
        "contest mechanics, and growth can reverse the apparent route order.",
        "",
        "## 4. Candidate algorithm-design implication","",
        "A future route evaluator should examine *dynamic space and tail timing*,",
        "not just the instantaneous four-neighbor count, IF these features",
        "demonstrate useful out-of-match predictive value and controlled",
        "league-like policy gains. These metrics remain observational and",
        "simplified, so no weight or threshold has been justified.",
        "Next: incorporate modelled opponent one-step reachable head cells",
        "and verified engine growth/collision order, then compare more",
        "accurate route risks on fresh league replay and controlled agent tests.",
        "",
        "## Source data and reproducibility","",
        "- [Danger positions with actual observed route choices](../derived/route_choice_windows.csv).",
        "- [All-student league/trial cohort summaries](../derived/route_choice_cohorts.csv).",
        "- [Field-wide strong-vs-weak matched cohorts](competitive_cohorts.md).",
        "- [Evidence-gated new algorithm rulebook](algorithm_rulebook.md).",
        "",
        "**No submitted or new competition snake implemented.**",""]
    path=report/"route_space.md"
    path.write_text("\n".join(lines),encoding="utf-8")
    return dict(replays=qc["unique_replays"],modeled_windows=qc["modeled_rows"],
                observed_moves=qc["league_first_moves_measured"]+
                               qc["trial_first_moves_measured"],
                same_game_pairs=len(matches),cohorts=cohorts,auc=whole,
                holdout_auc=unseen,bootstrap_auc=bootstrap,
                quality=dict(qc),report=str(path))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir",type=Path,default=Path("data"))
    parser.add_argument("--max-files",type=int,default=250)
    args=parser.parse_args()
    print(json.dumps(build(args.data_dir,args.max_files),indent=2))

if __name__=="__main__":
    main()
