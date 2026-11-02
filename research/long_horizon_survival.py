"""Real 10/20/30-turn snake survival after danger, without counting respawns as safety."""
from __future__ import annotations
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path
from statistics import mean
import argparse,csv,json,random

from .league_comparison import chart
from .long_horizon_core import load,survival_counts,by_recovery,recovery_label,PALMER

def percent(n,d):
    return 100*n/d if d else None

def fmt(value):
    return "n/a" if value is None else f"{value:.2f}"

def write_csv(path,records):
    path.parent.mkdir(parents=True,exist_ok=True)
    columns=list(records[0]) if records else ["season","mode","student"]
    with path.open("w",newline="",encoding="utf-8") as file:
        writer=csv.DictWriter(file,fieldnames=columns)
        writer.writeheader()
        writer.writerows(records)

def cluster_bootstrap(rows,mode,draws=1000,seed=2026):
    """Bootstrap full replay units for late death association, no turn pseudo-replication."""
    games=defaultdict(lambda:defaultdict(lambda:[0,0]))
    for r in rows:
        if r["mode"]!=mode or r["status10"]!="alive" or r["status30"]=="censored":
            continue
        group=recovery_label(r,3)
        if group is None:continue
        games[r["sha"]][group][0]+=int(r["status30"]=="dead")
        games[r["sha"]][group][1]+=1
    keys=sorted(games)
    if len(keys)<8:return None
    rng=random.Random(seed)
    outcomes=[]
    for _ in range(draws):
        sums=defaultdict(lambda:[0,0])
        for sha in rng.choices(keys,k=len(keys)):
            for group,(dead,total) in games[sha].items():
                sums[group][0]+=dead
                sums[group][1]+=total
        if sums["gained_exit"][1] and sums["did_not_gain"][1]:
            a=sums["gained_exit"]
            b=sums["did_not_gain"]
            outcomes.append(100*(a[0]/a[1]-b[0]/b[1]))
    if len(outcomes)<draws//2:return None
    outcomes.sort()
    return dict(low=outcomes[int(.025*(len(outcomes)-1))],
                high=outcomes[int(.975*(len(outcomes)-1))],
                clusters=len(keys),draws=len(outcomes))

def plot_survival(path,rates):
    body=['<line x1="110" y1="369" x2="919" y2="369" stroke="#64748b"/>',
          '<text x="113" y="81">Two different denominators; not a matched intervention</text>',
          '<rect x="752" y="49" width="13" height="13" fill="#60a5fa"/>',
          '<text x="770" y="61">League</text>',
          '<rect x="844" y="49" width="13" height="13" fill="#fbbf24"/>',
          '<text x="863" y="61">Trials</text>']
    for i,(metric,label) in enumerate((
        ("first10","No death, first 10 turns"),
        ("last30","No death by turn 30, given +10 survival"))):
        center=295+i*415
        body.append(f'<text x="{center}" y="407" text-anchor="middle">{label}</text>')
        for j,(mode,color) in enumerate((("league","#60a5fa"),("trial","#fbbf24"))):
            value=rates[mode][metric]
            if value is None:
                body.append(f'<text x="{center-40+j*80}" y="347">n/a</text>')
                continue
            height=value*2.5
            x=center-55+j*70
            body.append(f'<rect x="{x}" y="{369-height:.1f}" width="57" '
                        f'height="{height:.1f}" fill="{color}" rx="4"/>')
            body.append(f'<text x="{x+28:.1f}" y="{357-height:.1f}" '
                        f'text-anchor="middle" fill="{color}">{value:.1f}%</text>')
    chart(path,"Danger survival: first ten vs next twenty turns",body,445)

def plot_recovery(path,rates):
    body=['<line x1="110" y1="369" x2="920" y2="369" stroke="#64748b"/>',
          '<text x="110" y="78">Risk of death in turns 11–30 among first-ten survivors</text>',
          '<text x="110" y="98">Exit gain: at least one extra free neighbor at turn +3</text>']
    for i,mode in enumerate(("league","trial")):
        center=290+i*420
        body.append(f'<text x="{center}" y="410" text-anchor="middle">'
                    f'{mode.title()} (observational, not causal)</text>')
        for j,(group,color) in enumerate((("gained_exit","#34d399"),("did_not_gain","#60a5fa"))):
            g=rates[mode][group]
            value=percent(g["died11to30"],g["known30"])
            x=center-64+j*72
            if value is None:
                body.append(f'<text x="{x+25}" y="346">n/a</text>')
                continue
            height=value*2.6
            body.append(f'<rect x="{x}" y="{369-height:.1f}" width="60" '
                        f'height="{height:.1f}" fill="{color}" rx="4"/>')
            body.append(f'<text x="{x+30}" y="{355-height:.1f}" text-anchor="middle">'
                        f'{value:.1f}%</text>')
            body.append(f'<text x="{x+30}" y="387" text-anchor="middle">'
                        f'{"Gain" if j==0 else "No gain"}</text>')
    chart(path,"Recovery of local exits vs later death",body,445)

def export_rows(rows):
    for r in rows:
        action=r.get("first_action") or {}
        step=r["measurements"].get(3) or {}
        after10=r["measurements"].get(10) or {}
        after30=r["measurements"].get(30) or {}
        yield dict(season=r["season"],mode=r["mode"],replay_sha=r["sha"],
            replay=r["replay"],student=r["student"],turn=r["turn"],
            length=r["length"],length_band=r["length_bin"],
            nearest_head=r["nearest_head"],free_exits=r["free_exits"],
            pressure=r["head_pressure"],confined=r["confined"],
            outcome10=r["status10"],outcome20=r["status20"],outcome30=r["status30"],
            contiguous_followup=r["continuous_followup"],
            first_move_axis=action.get("movement"),
            first_move_style=action.get("turn_type"),
            food_progress_same_apple1=r.get("stable_food_progress1"),
            exit_gain3=step.get("exit_change"),
            head_distance_gain3=step.get("head_distance_change"),
            apples10=after10.get("apples"),apples30=after30.get("apples"),
            free_exits30=after30.get("free_exits"))

def palmer_comparison(rows):
    league=[r for r in rows if r["mode"]=="league"]
    shas={r["sha"] for r in league if r["student"]==PALMER}
    selected=[r for r in league if r["sha"] in shas]
    results={}
    for group,sub in (
        ("Palmer",[r for r in selected if r["student"]==PALMER]),
        ("Other students in Palmer games",[r for r in selected if r["student"]!=PALMER])):
        counts=survival_counts(sub,"league")
        observed=[r["measurements"][3]["exit_change"]
                  for r in sub if r["status10"]=="alive" and 3 in r["measurements"]]
        results[group]=dict(**counts,mean_exit_gain3=mean(observed) if observed else None,
                             observed3=len(observed))
    return results,len(shas)

def palmer_casebook(rows,data_dir):
    """One deterministically selected real danger episode per unique Palmer game.

    We select the EARLIEST sampled dangerous position, without selecting for
    future outcome. A peer comparator is shown only when starting length band,
    head-pressure category and constrained/unconstrained exits match within
    the SAME game. Those categories do not perfectly equalize geometry.
    """
    candidate={}
    for r in rows:
        if r["mode"]=="league" and r["student"]==PALMER:
            existing=candidate.get(r["sha"])
            if existing is None or r["turn"]<existing["turn"]:
                candidate[r["sha"]]=r
    out=[]
    for sha,p in sorted(candidate.items(),key=lambda item:
                        (item[1]["season"],item[1]["replay"]),reverse=True):
        peers=[r for r in rows if r["mode"]=="league" and r["sha"]==sha
               and r["student"]!=PALMER and r["length_bin"]==p["length_bin"]
               and r["head_pressure"]==p["head_pressure"]
               and r["confined"]==p["confined"]]
        peers.sort(key=lambda r:(abs(r["turn"]-p["turn"]),
                   abs(r["length"]-p["length"]),r["student"]))
        peer=peers[0] if peers else None
        act=p.get("first_action") or {}
        record=dict(
            season=p["season"],replay=p["replay"],sha=sha,
            danger_turn=p["turn"],body_length=p["length"],
            initial_head_distance=p["nearest_head"],initial_free_exits=p["free_exits"],
            first_actual_move=act.get("movement"),first_move_style=act.get("turn_type"),
            outcome10=p["status10"],outcome20=p["status20"],outcome30=p["status30"],
            matched_peer=peer["student"] if peer else None,
            peer_danger_turn=peer["turn"] if peer else None,
            peer_outcome30=peer["status30"] if peer else None)
        for t in (1,3,10,20,30):
            m=p["measurements"].get(t) or {}
            record[f"free_exits_{t}"]=m.get("free_exits")
            record[f"opponent_distance_{t}"]=m.get("nearest_head")
            record[f"apples_{t}"]=m.get("apples")
        out.append(record)
    write_csv(data_dir/"derived"/"palmer_league_casebook.csv",out)
    report=[
        "# Palmer's real league danger decisions — replay casebook","",
        "One selected example from EACH unique archived league game containing",
        "a sampled dangerous Palmer position. For reproducibility, selection",
        "uses the **earliest dangerous snapshot** in that game, NOT a winning",
        "or particularly impressive escape. No hypothetical moves are drawn.",
        "A danger snapshot means head distance <=3 cells or <=1 free neighbor.",
        "All observed x/y motions are on the real toroidal board. The first",
        "move style reports straight/turn/reverse relative to actual body",
        "orientation; unknown means we cannot determine orientation.",
        "A recorded death before +30 remains a death after respawn.",
        "If no frame or an unexplained absence is observed, +30 is censored.","",
        "| Archived league replay | Turn | Length | Start head distance | Free exits 0 to +3 | Actual first move | Death-free +30? | Comparable peer in same game |",
        "|---|---:|---:|---:|---|---|---|---|"]
    for r in out:
        f0=r["initial_free_exits"]
        f3=r["free_exits_3"]
        escape=f"{f0} → {f3 if f3 is not None else 'not observed'}"
        move=(r["first_actual_move"] or "unknown")+" / "+(r["first_move_style"] or "unknown")
        peer=r["matched_peer"] or "no matching baseline peer"
        report.append(
            f"| [{r['replay'].split('/')[-1]}](../replays/{r['replay']}) | "
            f"{r['danger_turn']} | {r['body_length']} | {r['initial_head_distance']} | "
            f"{escape} | {move} | {r['outcome30']} | {peer} |")
    report += ["",
        "## How to compare a genuine decision sequence","",
        "Use the [per-game CSV](../derived/palmer_league_casebook.csv), which",
        "contains each real replay's measured head distance, unoccupied",
        "neighbor count and apple captures at turns 0, 1, 3, 10, 20, 30.",
        "Cells may be empty after a death or when followup is censored.",
        "The optional matched peer shares the same replay, length band,",
        "head-proximity band and confined/unconfined category. Their starting",
        "turn, exact body, apples, and opponent positions may still differ.",
        "These are descriptive case studies, not a learned or proven policy.",
        "No competition snake code has been altered.",""]
    path=data_dir/"reports"/"palmer_casebook.md"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text("\n".join(report),encoding="utf-8")
    return dict(games=len(out),matched_peer_games=sum(bool(x["matched_peer"]) for x in out),
                report=str(path))

def build(data_dir,max_files=250):
    data_dir=Path(data_dir)
    rows,qc=load(data_dir,max_files)
    counts={mode:survival_counts(rows,mode) for mode in ("league","trial")}
    recovery={mode:by_recovery(rows,mode) for mode in ("league","trial")}
    bootstrap={mode:cluster_bootstrap(rows,mode) for mode in ("league","trial")}
    palmer,palmer_games=palmer_comparison(rows)
    casebook=palmer_casebook(rows,data_dir)
    figures=data_dir/"reports"/"charts"
    figures.mkdir(parents=True,exist_ok=True)
    plot_survival(figures/"danger_survival_30.svg",{
        m:dict(first10=percent(c["survived10"],c["baseline"]),
               last30=percent(c["alive30"],c["known30"]))
        for m,c in counts.items()})
    plot_recovery(figures/"escape_recovery_late_death.svg",recovery)
    write_csv(data_dir/"derived"/"long_horizon_danger_windows.csv",list(export_rows(rows)))
    lines=[
        "# Snake26: Do escapes stay safe for the next 20–30 turns?","",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
        "## Study design",
        "Actual student replay frames are sampled every 25 turns when the nearest",
        "opponent head is within three toroidal cells OR the snake has at most one",
        "unoccupied neighboring square. We distinguish league peers from fixed",
        "benchmark trials and deduplicate replay payloads by SHA-256.",
        "A recorded death event is FAILURE even if the snake later respawns.",
        "A missing frame or unexplained disappearance is CENSORED, never safe.",
        "Outcomes are death-free through +10, +20 or +30 turns. Since +30",
        "covers longer than the 25-turn sampling stride, windows from the same",
        "snake and match can overlap; resample entire replay clusters.",
        "",
        "## Data quality",
        f"Files scanned: **{qc['scanned']}** / {qc['files']}.",
        f"Unique replay payloads: **{qc['unique_replays']}** "
        f"(league {qc['league_unique_replays']}, trials {qc['trial_unique_replays']}).",
        f"Duplicate payloads: **{qc['replay_duplicates']}**.",
        f"Unreadable files: **{qc['unreadable_replays']}**.",
        f"Dangerous starting positions: **{len(rows):,}**.",
        f"Silent snake disappearances censored: **{qc['unexplained_disappearance_censored']}**.","",
        "## 1. Actual death-free followup",
        "![Death-free survival by horizon](charts/danger_survival_30.svg)","",
        "| Mode | Baseline danger windows | Dead by +10 | Survived +10 | Alive at +20 after +10 (known only) | Alive at +30 after +10 (known only) | Censored before +30 |",
        "|---|---:|---:|---:|---|---|---:|"]
    for mode,c in counts.items():
        lines.append(f"| {mode} | {c['baseline']} | {c['death10']} | {c['survived10']} | "
                     f"{c['alive20']}/{c['known20']} ({fmt(percent(c['alive20'],c['known20']))}%) | "
                     f"{c['alive30']}/{c['known30']} ({fmt(percent(c['alive30'],c['known30']))}%) | "
                     f"{c['censored30']} |")
    lines += ["",
        "The +20 and +30 percentages condition on first-ten survival AND having",
        "a known future outcome. Never confuse them with unconditional survival.",
        "",
        "## 2. Does recovering an extra exit at +3 predict death in turns 11–30?",
        "![Exit recovery versus later death](charts/escape_recovery_late_death.svg)","",
        "Analyze only snakes surviving to +10. Exits are an immediate geometry",
        "proxy, not guaranteed legal directions or long-horizon path safety.",
        "| Mode | +3 escape-space change | Survived first 10 | Known outcome at +30 | Dead in +11..+30 | Conditional death % | Censored |",
        "|---|---|---:|---:|---:|---:|---:|"]
    for mode in ("league","trial"):
        for label,key in (("Gained at least one exit","gained_exit"),
                          ("No new exit","did_not_gain")):
            r=recovery[mode][key]
            lines.append(f"| {mode} | {label} | {r['total10']} | {r['known30']} | "
                         f"{r['died11to30']} | "
                         f"{fmt(percent(r['died11to30'],r['known30']))}% | "
                         f"{r['censored30']} |")
    lines += ["",
        "## 3. Match-cluster bootstrap for late death difference",
        "Difference is exit-GAINERS minus NON-gainers, in percentage points.",
        "Negative would favor gainers, positive would favor non-gainers.",
        "This is observational and subject to selection and opponent confounding.","",
        "| Mode | Observed difference (percentage points) | Exploratory 95% replay-bootstrap CI | Replay clusters |",
        "|---|---:|---:|---:|"]
    for mode in ("league","trial"):
        a,b=recovery[mode]["gained_exit"],recovery[mode]["did_not_gain"]
        ra=percent(a["died11to30"],a["known30"])
        rb=percent(b["died11to30"],b["known30"])
        delta=ra-rb if ra is not None and rb is not None else None
        ci=bootstrap[mode]
        lines.append(f"| {mode} | {fmt(delta)} | "
                     f"{'['+fmt(ci['low'])+', '+fmt(ci['high'])+']' if ci else 'insufficient'} | "
                     f"{ci['clusters'] if ci else '—'} |")
    lines+=["",
        "## 4. Palmer compared with actual students in the same league games",
        f"Unique league replays with Palmer danger windows: **{palmer_games}**.",
        "These are real same-game opponent observations, but not exactly",
        "matched head positions, lengths, or player skill.","",
        "| Role | Danger windows | Survived +10 | Known +30 after +10 | Survived +30 | Mean +3 free-exit change |",
        "|---|---:|---:|---:|---:|---:|"]
    for name,rec in palmer.items():
        lines.append(f"| {name} | {rec['baseline']} | {rec['survived10']} | "
                     f"{rec['known30']} | {rec['alive30']} | "
                     f"{fmt(rec['mean_exit_gain3'])} (n={rec['observed3']}) |")
    lines += ["",
        "## 5. Palmer's actual decision sequences in individual league replays",
        f"Audited games in the [Palmer casebook](palmer_casebook.md): "
        f"**{casebook['games']}**.",
        f"Games with a comparable starting-danger peer in the SAME replay: "
        f"**{casebook['matched_peer_games']}**.",
        "The casebook exposes actual movement direction and straight-versus-turn",
        "choice plus neighboring-space, head-distance and food observations",
        "through turns +1, +3, +10, +20 and +30 where recorded.",
        "We select the earliest qualifying danger in each replay, never",
        "cherry-pick a successful later move.",
        "[Open Palmer's complete observed casebook](palmer_casebook.md).",
        "",
        "## 6. Interpretation and next experiment",
        "A successful first escape does not guarantee another twenty safe turns.",
        "Early mobility recovery and late survival can be associated without",
        "the move CAUSING survival. Conditioning on +10 survival selects a",
        "nonrandom subset of snakes; initial body geometry, head trajectories,",
        "apples, opponent strength and season/version remain confounders.",
        "Next, investigate close-call turns with head direction, legal move",
        "options and contested food in the SAME games. Only then consider",
        "testing candidate policy changes on held-out seeds.",
        "",
        "## Auditable observations",
        "[Censor-aware 10/20/30-turn danger windows](../derived/long_horizon_danger_windows.csv).",
        "[Matched real escape/autopsy report](escape_autopsies.md).",
        "[Canonical joined league/trial dashboard](joint_analysis.md).",
        "",
        "**No Java competition snake code was changed.**",""]
    report=data_dir/"reports"/"long_horizon_survival.md"
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text("\n".join(lines),encoding="utf-8")
    return dict(replays=qc["unique_replays"],league=counts["league"],trial=counts["trial"],
                recovery=recovery,bootstrap=bootstrap,palmer=palmer,
                palmer_games=palmer_games,palmer_casebook=casebook,
                report=str(report))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    p.add_argument("--max-files",type=int,default=250)
    args=p.parse_args()
    print(json.dumps(build(args.data_dir,args.max_files),indent=2))
if __name__=="__main__":
    main()
