"""Across-the-field Snake26 league cohort comparisons, never a two-snake audit.

Group each student's REPLAY EXPO​SURE by the official ranking from the SAME
season (Division 1 only). Strong (top quartile), middle half, and struggling
(bottom quartile) are observation cohorts, not bot-code labels.
Avoid mixing trials with real peer league matches; report both separately.
Only compare recorded future death/escape outcomes and action proxies.
One repeated SHA replay counts once via upstream long_horizon_survival.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
import sqlite3
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path
from statistics import mean
import random

from .league_comparison import chart

COHORTS=("top_quartile","middle_half","bottom_quartile")
BANDS=("5-24","25-49","50-99","100+")
THREATS=("head_close","confined_only")

def ranks(db):
    """Cohort assignment ALWAYS refers to that season's own official standings."""
    grouped=defaultdict(list)
    for season,team,division,rank in db.execute(
        "SELECT season_name,team_slug,division,division_rank FROM standings "
        "WHERE division=1 AND division_rank IS NOT NULL AND "
        "team_slug NOT LIKE '~%'"):
        if isinstance(rank,int) and rank>0:
            grouped[season].append((team,rank))
    result={}
    for season,items in grouped.items():
        if len(items)<12:
            continue
        n=len(items)
        sorted_names=sorted(items,key=lambda x:(x[1],x[0]))
        top=math.ceil(n/4)
        bottom=math.floor(3*n/4)
        for i,(team,rank) in enumerate(sorted_names):
            # Use official rank rather than position in lexical order.
            cohort=("top_quartile" if rank<=top else
                    "bottom_quartile" if rank>bottom else "middle_half")
            result[season,team]=dict(cohort=cohort,rank=rank,division_size=n)
    return result

def read_windows(path):
    if not path.exists():return []
    with path.open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def classify(rows,ranked):
    result=[]
    qc=Counter()
    seen=set()
    for r in rows:
        key=(r.get("replay_sha"),r.get("student"),r.get("turn"))
        if not all(key):
            qc["bad_identity"]+=1
            continue
        if key in seen:
            qc["duplicate_exposures"]+=1
            continue
        seen.add(key)
        mode=r.get("mode")
        if mode not in ("league","trial"):
            qc["invalid_mode"]+=1
            continue
        meta=ranked.get((r.get("season"),r.get("student")))
        if not meta:
            qc[mode+"_unmatched_rank"]+=1
            continue
        try:
            length=int(r["length"])
            nearest=int(r["nearest_head"])
            exits=int(r["free_exits"])
            turn=int(r["turn"])
            if not 0<=exits<=4 or nearest<0 or length<5 or turn<0:
                raise ValueError("Bad window")
        except (ValueError,TypeError,KeyError):
            qc["bad_window"]+=1
            continue
        if r.get("outcome10") not in ("alive","dead","censored") or (
            r.get("outcome30") not in ("alive","dead","censored")):
            qc["invalid_outcome"]+=1
            continue
        # Ignore unobserved future windows explicitly, rather than labeling safe.
        gain=None
        if r.get("exit_gain3") not in (None,""):
            try:gain=int(r["exit_gain3"])
            except ValueError:qc["bad_3_turn_delta"]+=1
        first_move=r.get("first_move_style")
        if first_move not in ("straight","turn","reverse","unknown_heading"):
            first_move=None
        food_progress=None
        if r.get("food_progress_same_apple1") not in (None,""):
            try:food_progress=int(r["food_progress_same_apple1"])
            except (ValueError,TypeError):qc["bad_food_progress"]+=1
        result.append(dict(
            season=r["season"],replay_sha=r["replay_sha"],
            student=r["student"],mode=mode,cohort=meta["cohort"],
            rank=meta["rank"],division_size=meta["division_size"],
            turn=turn,phase=turn//500,length=length,
            length_band=r["length_band"],nearest_head=nearest,
            free_exits=exits,head_close=nearest<=3,
            confined=exits<=1,exit_gain3=gain,
            first_move=first_move,food_progress1=food_progress,
            status10=r["outcome10"],status30=r["outcome30"]))
        qc[mode+"_ranked_windows"]+=1
    return result,qc

def rates(rows):
    """Return counts, not statistical claims. Exclude right-censored outcomes."""
    known10=[r for r in rows if r["status10"]!="censored"]
    known30=[r for r in rows if r["status30"]!="censored"]
    valid_gain=[r for r in rows if r["exit_gain3"] is not None
                and r["status10"]=="alive"]
    observed_moves=[r for r in rows if r["first_move"] in ("straight","turn","reverse")]
    food_moves=[r for r in rows if r["food_progress1"] is not None]
    d10=sum(r["status10"]=="dead" for r in known10)
    d30=sum(r["status30"]=="dead" for r in known30)
    return dict(n=len(rows),n10=len(known10),deaths10=d10,
                n30=len(known30),deaths30=d30,
                death10_pct=100*d10/len(known10) if known10 else None,
                death30_pct=100*d30/len(known30) if known30 else None,
                close_pct=100*sum(r["head_close"] for r in rows)/len(rows) if rows else None,
                confined_pct=100*sum(r["confined"] for r in rows)/len(rows) if rows else None,
                gain3_pct=100*sum(r["exit_gain3"]>0 for r in valid_gain)/len(valid_gain)
                if valid_gain else None,
                n_gain3=len(valid_gain),
                first_move_n=len(observed_moves),
                straight_pct=100*sum(r["first_move"]=="straight" for r in observed_moves)/
                len(observed_moves) if observed_moves else None,
                food_move_n=len(food_moves),
                toward_apple_pct=100*sum(r["food_progress1"]>0 for r in food_moves)/
                len(food_moves) if food_moves else None,
                replays=len({r["replay_sha"] for r in rows}),
                students=len({r["student"] for r in rows}),
                seasons=len({r["season"] for r in rows}))

def grouped_rates(rows):
    return {(mode,c):rates([r for r in rows if r["mode"]==mode and
            r["cohort"]==c]) for mode in ("league","trial") for c in COHORTS}

def matching_stratum(row):
    """Strict pre-outcome matching; no future action/outcome used in strata."""
    return (row["mode"],row["length_band"],row["head_close"],
            row["confined"],row["phase"])

def common_support(rows):
    """Restrict comparison to state strata visited by both extreme cohorts."""
    by_stratum=defaultdict(lambda:defaultdict(list))
    for r in rows:
        if r["cohort"] in (COHORTS[0],COHORTS[-1]):
            by_stratum[matching_stratum(r)][r["cohort"]].append(r)
    supported=[]
    info=Counter()
    for key,groups in by_stratum.items():
        if all(groups.get(c) for c in (COHORTS[0],COHORTS[-1])):
            info["common_strata"]+=1
            for c in (COHORTS[0],COHORTS[-1]):
                supported.extend(groups[c])
                info[c+"_windows"]+=len(groups[c])
        else:info["single_cohort_strata"]+=1
    return supported,info

def same_game_support(rows):
    """How often do strong and struggling students share an actual replay?"""
    by_replay=defaultdict(lambda:defaultdict(list))
    for r in rows:
        if r["mode"]=="league":
            by_replay[r["replay_sha"]][r["cohort"]].append(r)
    games=[groups for groups in by_replay.values()
           if groups.get("top_quartile") and groups.get("bottom_quartile")]
    return dict(unique_league_replays=len(by_replay),both_extremes=len(games),
                matched_students=len({r["student"] for g in games
                    for cohort in ("top_quartile","bottom_quartile") for r in g[cohort]}))

def matched_same_game_episodes(rows):
    """Greedy 1:1 unique pairs in SAME league game and SAME baseline stratum.

    Match pre-outcome length band, nearest head <=3, free exits <=1, phase.
    Prefer closest EXACT starting length, head distance, free exits and turn.
    This is observational matching, not randomization or causal inference.
    """
    indexed=defaultdict(lambda:defaultdict(list))
    for row in rows:
        if row["mode"]!="league" or row["cohort"] not in ("top_quartile","bottom_quartile"):
            continue
        key=(row["replay_sha"],matching_stratum(row))
        indexed[key][row["cohort"]].append(row)
    matched=[]
    for key,groups in sorted(indexed.items(),key=lambda kv:str(kv[0])):
        tops=sorted(groups.get("top_quartile",[]),key=lambda r:(
            r["turn"],r["student"]))
        bottoms=list(groups.get("bottom_quartile",[]))
        for top in tops:
            if not bottoms:
                break
            best=min(range(len(bottoms)),key=lambda i:(
                abs(bottoms[i]["length"]-top["length"]),
                abs(bottoms[i]["nearest_head"]-top["nearest_head"]),
                abs(bottoms[i]["free_exits"]-top["free_exits"]),
                abs(bottoms[i]["turn"]-top["turn"]),
                bottoms[i]["student"]))
            bottom=bottoms.pop(best)
            matched.append((top,bottom))
    return matched

def pair_value(row,metric):
    if metric=="death10":
        if row["status10"]=="censored":return None
        return int(row["status10"]=="dead")
    if metric=="turn":
        return (int(row["first_move"]!="straight")
                if row["first_move"] in ("straight","turn","reverse") else None)
    if metric=="apple_progress":
        return (int(row["food_progress1"]>0)
                if row["food_progress1"] is not None else None)
    if metric=="exit_gain":
        if row["status10"]!="alive" or row["exit_gain3"] is None:return None
        return int(row["exit_gain3"]>0)
    raise ValueError("Unknown measured feature")

def paired_contrast(pairs,metric,draws=1000,seed=2026):
    """Bottom minus top, event-level; confidence by entire REPLAY cluster.

    Resampling replay clusters handles correlated episodes within game.
    Historical repeated opponents/bot versions can still create dependence.
    """
    observations=[(a["replay_sha"],pair_value(a,metric),pair_value(b,metric))
                  for a,b in pairs]
    observed=[(sha,100*(v-u)) for sha,u,v in observations
              if u is not None and v is not None]
    result=dict(n=len(observed),
                replay_clusters=len({sha for sha,_ in observed}),
                bottom_minus_top_pp=(mean(diff for _,diff in observed)
                                     if observed else None),
                ci_low=None,ci_high=None)
    grouped=defaultdict(list)
    for sha,value in observed:grouped[sha].append(value)
    games=sorted(grouped)
    if len(games)<8:return result
    rng=random.Random(seed)
    bs=[]
    for _ in range(draws):
        diff=[]
        for sha in rng.choices(games,k=len(games)):
            diff.extend(grouped[sha])
        if diff:bs.append(mean(diff))
    bs.sort()
    if bs:
        result["ci_low"]=bs[int(.025*(len(bs)-1))]
        result["ci_high"]=bs[int(.975*(len(bs)-1))]
    return result

def write_matched_csv(path,pairs):
    rows=[]
    for top,bottom in pairs:
        row=dict(season=top["season"],replay_sha=top["replay_sha"],
                 top_student=top["student"],bottom_student=bottom["student"],
                 top_turn=top["turn"],bottom_turn=bottom["turn"],
                 top_length=top["length"],bottom_length=bottom["length"],
                 top_head_dist=top["nearest_head"],bottom_head_dist=bottom["nearest_head"],
                 top_free_exits=top["free_exits"],bottom_free_exits=bottom["free_exits"],
                 top_first_move=top["first_move"],bottom_first_move=bottom["first_move"],
                 top_apple_progress1=top["food_progress1"],
                 bottom_apple_progress1=bottom["food_progress1"],
                 top_exit_gain3=top["exit_gain3"],bottom_exit_gain3=bottom["exit_gain3"],
                 top_outcome10=top["status10"],bottom_outcome10=bottom["status10"])
        rows.append(row)
    write_csv(path,rows)
    return rows

def fmt(v):
    return "insufficient" if v is None else f"{v:.2f}%"

def plot(path,groups):
    eligible=[groups[m,c]["death10_pct"] for m in ("league","trial")
              for c in COHORTS if groups[m,c]["death10_pct"] is not None]
    high=max(2.0,max(eligible,default=0)*1.2)
    body=['<line x1="107" y1="372" x2="919" y2="372" stroke="#64748b"/>',
          f'<text x="900" y="118" text-anchor="end">Vertical scale: 0 to {high:.1f}%</text>',
          '<text x="105" y="81">Observed deaths in next 10 turns, measured per danger window</text>',
          '<text x="105" y="99">Ranked by same-season official Division 1 standings</text>']
    for i,c in enumerate(COHORTS):
        centre=245+i*267
        body.append(f'<text x="{centre}" y="407" text-anchor="middle">'
                    f'{("Top 25%","Middle 50%","Bottom 25%")[i]}</text>')
        for j,(mode,color) in enumerate((("league","#60a5fa"),("trial","#fbbf24"))):
            r=groups[mode,c]
            val=r["death10_pct"]
            x=centre-55+j*63
            if val is None:
                body.append(f'<text x="{x+27}" y="348">n/a</text>')
                continue
            height=255*min(high,val)/high
            # chart uses a 0..100 scale, not an exaggerated percent axis
            body.append(f'<rect x="{x}" y="{372-height:.1f}" width="54" '
                        f'height="{height:.1f}" rx="3" fill="{color}"/>')
            body.append(f'<text x="{x+27}" y="{359-height:.1f}" '
                        f'text-anchor="middle">{val:.2f}%</text>')
    body.extend(['<rect x="720" y="54" width="12" height="12" fill="#60a5fa"/>',
                 '<text x="737" y="65">League</text>',
                 '<rect x="832" y="54" width="12" height="12" fill="#fbbf24"/>',
                 '<text x="849" y="65">Trials</text>'])
    chart(path,"Division 1 cohort danger outcomes (descriptive)",body,445)

def write_csv(path,items):
    path.parent.mkdir(parents=True,exist_ok=True)
    keys=list(items[0]) if items else ["mode","cohort","n","replays"]
    with path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=keys)
        writer.writeheader()
        writer.writerows(items)

def build(data_dir):
    data_dir=Path(data_dir)
    with sqlite3.connect(data_dir/"snake.db") as db:
        ranked=ranks(db)
    original=read_windows(data_dir/"derived"/"long_horizon_danger_windows.csv")
    observations,qc=classify(original,ranked)
    groups=grouped_rates(observations)
    supported,matching=common_support(observations)
    within=grouped_rates(supported)
    shared=same_game_support(observations)
    same_match_pairs=matched_same_game_episodes(observations)
    pair_stats={k:paired_contrast(same_match_pairs,k) for k in
                ("death10","turn","apple_progress","exit_gain")}
    write_matched_csv(data_dir/"derived"/"competitive_matched_decisions.csv",
                      same_match_pairs)
    chart_path=data_dir/"reports"/"charts"/"cohort_danger_outcomes.svg"
    plot(chart_path,groups)
    by_group=[]
    for mode in ("league","trial"):
        for cohort in COHORTS:
            by_group.append(dict(mode=mode,cohort=cohort,
                                 **groups[mode,cohort]))
    write_csv(data_dir/"derived"/"competitive_cohort_danger.csv",by_group)
    lines=[
        "# Snake26: Strong, middle, and struggling league competitors — comparison","",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
        "## Scientific question","",
        "Across the competition, what danger-response patterns distinguish",
        "consistently strong versus weaker *official league* snakes in",
        "comparable situations? This is a population-level exploration,",
        "NOT a study of our submitted agent or a named rival. ALL student bots",
        "are eligible. Palmer is one top-division example, not the baseline.","",
        "## Cohort design and selection caveats","",
        "- Use official Division 1 standings from the **SAME replay season**",
        "  as each sampled student, never transplant today's rank into older",
        "  bot versions. Division 2 ranks are not mixed into Division 1.",
        "- Top cohort: official division rank in best 25%; bottom: worst 25%;",
        "  middle: remaining 50%. Only standings with at least 12 members qualify.",
        "- A frame is sampled every 25 turns only when a student is near",
        "  another live head (within 3 toroidal cells) OR has <=1 unoccupied",
        "  neighbor. Same raw replay payload counted once, not once per season.",
        "- Outcomes: real death event in the following 10 or 30 turns,",
        "  with incomplete followup CENSORED and respawn still a death.",
        "- We focus on actual league matches; controlled trials are shown",
        "  SEPARATELY, grouped by the student's same-season league standing.",
        "- Historical archived replays are deliberately sampled, not a random",
        "  draw from all official matches. Rankings include game results;",
        "  ranking groups are outcome-selected, not randomized policies.","",
        f"Baseline windows available across BOTH environments: **{len(original):,}**.",
        f"Same-season Division 1 ranked league windows: **{qc['league_ranked_windows']:,}**.",
        f"Same-season Division 1 ranked trial windows: **{qc['trial_ranked_windows']:,}**.",
        f"League windows without qualifying same-season rank: **{qc['league_unmatched_rank']:,}**.",
        f"Trial windows without qualifying same-season rank: **{qc['trial_unmatched_rank']:,}**.",
        f"Duplicate rows excluded: **{qc['duplicate_exposures']}**.",
        "",
        "## 1. Observed danger exposure and outcomes by performance cohort","",
        "![Strong vs weak student danger windows](charts/cohort_danger_outcomes.svg)","",
        "| Match mode | Division 1 cohort | Students | Unique replays | Danger windows | Nearby heads | Confinement | Death by +10 (events/windows) | Death by +30 (events/windows) | Gained exit by +3 (among +10 survivors) | First move straight | Moved toward a persistent apple |",
        "|---|---|---:|---:|---:|---|---|---|---|---|---|---|"]
    for x in by_group:
        lines.append(f"| {x['mode']} | {x['cohort']} | {x['students']} | "
                     f"{x['replays']} | {x['n']} | {fmt(x['close_pct'])} | "
                     f"{fmt(x['confined_pct'])} | {x['deaths10']}/{x['n10']} "
                     f"({fmt(x['death10_pct'])}) | {x['deaths30']}/{x['n30']} "
                     f"({fmt(x['death30_pct'])}) | {x['n_gain3']} sampled, "
                     f"{fmt(x['gain3_pct'])} | {x['first_move_n']} moves, "
                     f"{fmt(x['straight_pct'])} | {x['food_move_n']} moves, "
                     f"{fmt(x['toward_apple_pct'])} |")
    lines+=["",
        "First-move straight/turn is reconstructed from two consecutive REAL frames.",
        "Food progress means closing distance to the SAME apple still visible",
        "one frame later; this does not prove the snake targeted that apple.",
        "These rows DESCRIBE the encounters each cohort experienced; they do",
        "not establish that stronger snakes made different decisions in"
        "equivalent states. A difference may reflect opponents and selection.","",
        "## 2. Restrict to comparable pre-decision danger situations","",
        "Common-support strata require BOTH top and bottom students in the",
        "SAME environment, body length band, near-head yes/no, restricted",
        "neighbor count yes/no, and 500-turn phase. Each group must contain",
        "actual observations; we do not extrapolate outside overlap.","",
        f"- Common strata across both modes: **{matching['common_strata']}**.",
        f"- League replays with ranked student exposures: **{shared['unique_league_replays']}**.",
        f"- Those containing BOTH extreme cohorts: **{shared['both_extremes']}**.",
        f"- Distinct top/bottom students in overlapping games: **{shared['matched_students']}**.",
        "",
        "| Mode | Cohort within overlap | Windows | Distinct replays | +10 death frequency | +3 exit gain frequency | First-move straight | Same-apple progress |",
        "|---|---|---:|---:|---|---|---|---|"]
    for mode in ("league","trial"):
        for cohort in ("top_quartile","bottom_quartile"):
            v=within[mode,cohort]
            lines.append(f"| {mode} | {cohort} | {v['n']} | {v['replays']} | "
                         f"{fmt(v['death10_pct'])} | {fmt(v['gain3_pct'])} | "
                         f"{fmt(v['straight_pct'])} | {fmt(v['toward_apple_pct'])} |")
    lines += ["",
        "## 3. Strong versus struggling snakes in the SAME real match","",
        "Each pair uses one top-quartile and one bottom-quartile student",
        "from the SAME actual replay, SAME body-length band, near-head",
        "condition, confined/unconfined condition, and 500-turn game phase.",
        "Pairing uses only BASELINE variables, and no observed window is reused.",
        "This is a harder comparison than grouping results across unrelated",
        "games, but pairs may still differ in exact body location, apples,",
        "opponent responses and how much time passes between snapshots.","",
        f"Matched dangerous-position pairs: **{len(same_match_pairs)}**.",
        f"Distinct league replays with strict matched pairs: "
        f"**{len({a['replay_sha'] for a,b in same_match_pairs})}**.",
        "",
        "| Measured outcome (bottom minus top) | Both decisions observable | Replay clusters | Difference (percentage points) | Replay-resampled 95% interval |",
        "|---|---:|---:|---:|---|"]
    for metric,label in (
        ("death10","Died in next 10 turns"),
        ("turn","First step was a turn/reversal rather than straight"),
        ("apple_progress","Moved toward same still-visible apple"),
        ("exit_gain","Gained 1+ neighboring cell by turn 3, among +10 survivors")
    ):
        r=pair_stats[metric]
        ci=(f"[{r['ci_low']:+.2f}, {r['ci_high']:+.2f}]"
            if r["ci_low"] is not None else "insufficient distinct games")
        d=f"{r['bottom_minus_top_pp']:+.2f}" if r["bottom_minus_top_pp"] is not None else "n/a"
        lines.append(f"| {label} | {r['n']} | {r['replay_clusters']} | {d} | {ci} |")
    lines += ["",
        "Positive values mean the bottom cohort exhibited the behavior or",
        "death more frequently; negative values mean the top did.",
        "Match-level bootstrap uncertainty addresses repeated episodes in",
        "one replay, NOT repeated student versions across snapshots.",
        "Even equal baseline categories are NOT identical legal choices;",
        "none of these contrasts alone tells us which action caused survival.",
        "[Auditable non-reused matched pairs](../derived/competitive_matched_decisions.csv).",
        "",
        "These are COMMON-STRATUM comparisons but they are NOT reweighted",
        "to identical distributions within the overlap. Even same-game cohorts",
        "may occupy different locations and face unequal threats. No p-value",
        "or effect-size certainty is claimed from individual windows.",
        "",
        "## 4. What would make a useful algorithm rule?","",
        "Test the hypothesis that top league competitors select routes with",
        "better safe future mobility after controlling for starting length,",
        "head geometry and food opportunity. Our 0–4 free-neighbor count is",
        "an INSTANTANEOUS proxy, not a legal-move count or full route quality.",
        "We must next measure per-ACTION future reachable areas and opponent",
        "reach cones, then reproduce any predictive advantage on HELD-OUT",
        "entire matches and unseen bot versions.",
        "A cohort difference at this stage is evidence for a feature to",
        "test, NEVER evidence that copying a champion's move is optimal.",
        "",
        "## Auditable outputs","",
        "- [Cohort sample sizes, outcomes, mobility](../derived/competitive_cohort_danger.csv).",
        "- [Underlying complete danger-window observations](../derived/long_horizon_danger_windows.csv).",
        "- [Research protocol and rule-promotion tests](../../docs/ALGORITHM_RESEARCH_PROTOCOL.md).",
        "",
        "**No existing submitted snake code was modified.**",""]
    dst=data_dir/"reports"/"competitive_cohorts.md"
    dst.write_text("\n".join(lines),encoding="utf-8")
    return dict(ranked_league_windows=qc["league_ranked_windows"],
                ranked_trial_windows=qc["trial_ranked_windows"],
                common_strata=matching["common_strata"],
                same_match_extremes=shared["both_extremes"],
                strictly_matched_pairs=len(same_match_pairs),
                pair_statistics=pair_stats,
                cohorts=by_group,report=str(dst))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir",type=Path,default=Path("data"))
    a=parser.parse_args()
    print(json.dumps(build(a.data_dir),indent=2))

if __name__=="__main__":
    main()
