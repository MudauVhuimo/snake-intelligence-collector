"""Publish the canonical joined research hub and environment-specific graphics.

Data sources are separate aggregated league and controlled-trial tables;
the ONLY comparison join key is (season, student). Bot SHA is attached when
available, but not claimed to identify every game played in that season.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path
import argparse
import json

from .joined_datasets import build as prepare, correlations
from .behavior_by_mode import build as behavior_report
from .threat_windows import build as threat_report
from .escape_autopsies import build as autopsy_report
from .long_horizon_survival import build as long_horizon_report
from .competitive_cohorts import build as competitive_cohorts_report
from .route_space import build as route_space_report
from .rulebook import build as render_rulebook
from .seasonal_disagreement import build as seasonal_report
from .historical_peer_comparison import build as historical_peer_report
from .league_comparison import chart

PAIRS=(
    ("mean_food","Mean apples per game","apples"),
    ("mean_length","Mean final body length","length"),
    ("mean_kills","Mean kills per game","kills"),
    ("mean_retention","Mean growth retention","retention"),
)
COLORS=("#60a5fa","#34d399","#fbbf24","#f472b6")

def printable(value,places=2):
    if value is None:
        return "—"
    return f"{value:.{places}f}"

def points_chart(path,people,key,title,champion):
    xkey="trial_"+key
    ykey="league_"+key
    matched=[r for r in people if r.get(xkey) is not None and r.get(ykey) is not None]
    if not matched:
        return chart(path,title,["<text x='55' y='110'>No eligible joined observations</text>"],220)
    xmin=min(r[xkey] for r in matched)
    xmax=max(r[xkey] for r in matched)
    ymin=min(r[ykey] for r in matched)
    ymax=max(r[ykey] for r in matched)
    if xmax<=xmin:xmax=xmin+1
    if ymax<=ymin:ymax=ymin+1
    dx=(xmax-xmin)*.08
    dy=(ymax-ymin)*.08
    xmin,xmax=xmin-dx,xmax+dx
    ymin,ymax=ymin-dy,ymax+dy
    X=lambda x:112+735*(x-xmin)/(xmax-xmin)
    Y=lambda y:412-325*(y-ymin)/(ymax-ymin)
    body=['<line x1="112" y1="412" x2="847" y2="412" stroke="#64748b"/>',
          '<line x1="112" y1="87" x2="112" y2="412" stroke="#64748b"/>',
          '<text x="490" y="464" text-anchor="middle">Controlled trial metric</text>',
          '<text x="23" y="250" text-anchor="middle" transform="rotate(-90 23 250)">League metric (vs students)</text>',
          f'<text x="875" y="99">Paired students: {len(matched)}</text>']
    for i in range(5):
        yy=412-325*i/4
        xx=112+735*i/4
        body.extend([f'<line x1="112" y1="{yy:.1f}" x2="847" y2="{yy:.1f}" stroke="#29364b"/>',
                     f'<text x="101" y="{yy+4:.1f}" text-anchor="end">{ymin+(ymax-ymin)*i/4:.2f}</text>',
                     f'<line x1="{xx:.1f}" y1="87" x2="{xx:.1f}" y2="412" stroke="#29364b"/>',
                     f'<text x="{xx:.1f}" y="435" text-anchor="middle">{xmin+(xmax-xmin)*i/4:.2f}</text>'])
    for r in matched:
        own=r["team"]==champion
        c="#fbbf24" if own else "#60a5fa"
        xx,yy=X(r[xkey]),Y(r[ykey])
        body.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="{8 if own else 4.5}" '
                    f'fill="{c}" opacity=".9"><title>{escape(r["team"])}: '
                    f'trial={r[xkey]:.2f}, league={r[ykey]:.2f}, '
                    f'league games={r["league_games"]}</title></circle>')
        if own:
            body.append(f'<text x="{xx+11:.1f}" y="{yy-11:.1f}" fill="#fbbf24">'
                        f'{escape(r["team"].split("-",1)[-1])}</text>')
    chart(path,title,body,490)

def rho_chart(path,results):
    # Spearman may be negative. Bars run outward from zero in either direction.
    w,h=1000,380
    center=490
    max_width=330
    body=['<line x1="490" y1="76" x2="490" y2="326" stroke="#64748b"/>',
          '<text x="490" y="355" text-anchor="middle">Spearman correlation (trial metric vs league metric)</text>']
    for i,item in enumerate(results):
        yy=100+i*62
        rho=item["rho"]
        body.append(f'<text x="18" y="{yy+17}" fill="#cbd5e1">'
                    f'{escape(item["metric"][:31])} (n={item["n"]})</text>')
        if rho is None:continue
        width=abs(rho)*max_width
        x=center if rho>=0 else center-width
        body.append(f'<rect x="{x:.1f}" y="{yy}" width="{width:.1f}" height="23" rx="3" '
                    f'fill="{ "#34d399" if rho>=0 else "#f472b6"}"/>')
        tx=(center+width+9 if rho>=0 else center-width-9)
        align="start" if rho>=0 else "end"
        body.append(f'<text x="{tx:.1f}" y="{yy+17}" text-anchor="{align}" '
                    f'fill="#f8fafc">{rho:+.3f}</text>')
    chart(path,"How similarly do students perform in the two environments?",body,h)

def build(data_dir):
    data,quality=prepare(data_dir)
    latest=quality["current_season"]
    if not latest:
        raise RuntimeError("No official season to compare")
    movement=behavior_report(data_dir)  # Replay evidence stays separate from catalog outcomes.
    threat=threat_report(data_dir)  # Forward-looking head danger, matched mode definitions.
    autopsies=autopsy_report(data_dir)  # Baseline-matched recorded death/escape trajectories.
    long_horizon=long_horizon_report(data_dir)  # Censor-aware +10/+20/+30 followups.
    cohorts=competitive_cohorts_report(data_dir)  # Same-season Division 1 top/middle/bottom cohort study.
    routes=route_space_report(data_dir)  # Pre-action frozen-body vs moving-own-tail route prediction.
    candidate_rules=render_rulebook(data_dir)  # Evidence-gated hypotheses for a NEW agent.
    history=seasonal_report(data_dir)  # Longitudinal matched ranking differences, not independent trials.
    peer_history=historical_peer_report(data_dir)  # Older peer-game catalogs without official standings.
    paired,results=correlations(data["joined"],latest,division=1,min_league=3)
    champion=next((r["team"] for r in sorted(paired,key=lambda r:
                    r["official_rank"] if r["official_rank"] is not None else 99999)),None)
    charts=data_dir/"reports"/"charts"
    charts.mkdir(parents=True,exist_ok=True)
    for key,label,short in PAIRS:
        points_chart(charts/("joint_"+short+".svg"),paired,key,
                     "Same student: "+label+" in two environments",champion)
    rho_chart(charts/"joint_correlations.svg",results)
    modes=("league","trial")
    official=[r for r in data["joined"] if r["season"]==latest
              and r["official_division"]==1]
    official.sort(key=lambda r:r["official_rank"] if r["official_rank"] is not None else 999)
    qa=quality
    output=data_dir/"reports"
    lines=[
        "# Snake26: JOINED league + trials study","",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
        f"**Latest official season:** {latest}. This report treats competitive league",
        "matches and controlled on-arrival trials as **two separate datasets**",
        "and joins them at the **same season + same student**. The published",
        "end-of-season code SHA, when known, is attached for auditing, but is",
        "**not proof that every match in that season used that exact code version**.",
        "",
        "## 1. Data provenance and cleaning","",
        "**Source of truth:** official public Wits catalog records in the SQLite archive.","",
        "| Separate data source | Cataloged matches | Full replays | Unique replay hashes |",
        "|---|---:|---:|---:|"]
    for kind in modes:
        lines.append(f"| {kind.title()} | {qa['catalog'].get(kind,0):,} | "
                     f"{qa['replays'].get(kind,0):,} | {qa['unique'].get(kind,0):,} |")
    lines += [
        "",f"**Historical student-season rows:** league {qa['league_team_seasons']:,},",
        f"trials {qa['trial_team_seasons']:,}, union {qa['joined_rows']:,}.",
        f"**Current season paired students (at least 2 student-opponent league games",
        f"plus all 3 trials): {qa['latest_season_paired']}**.",
        f"**Division 1 study sample (at least 3 league games + all trials): {len(paired)}**.",
        "",
        "Important: a cataloged game is not automatically a recorded full replay.",
        "We do not estimate actions, decisions, deaths or attack policy from aggregate",
        "placements. Identical SHA replay payloads are counted separately in catalog",
        "coverage but not as independent unique recordings.",
        f"**Possible mechanics/data inconsistencies** (final length larger than",
        f"5 + 5 times apples) among student-game observations: {qa['bad_retention']}.",
        "Investigate any nonzero cases before interpreting reset behavior.",
        "",
        "## 2. Correlations between SAME students in both environments","",
        "![Joined correlations](charts/joint_correlations.svg)","",
        "| Paired measurement | Division 1 students | Spearman rho | Exploratory 95% paired-student bootstrap interval |",
        "|---|---:|---:|---:|"]
    for row in results:
        interval=(f"[{row['ci_low']:+.3f}, {row['ci_high']:+.3f}]"
                  if row.get("ci_low") is not None and row.get("ci_high") is not None
                  else "insufficient")
        lines.append(f"| {row['metric']} | {row['n']} | {printable(row['rho'],3)} | {interval} |")
    lines+=["",
        "Correlations are calculated only among students from **the same division",
        "and season**, to avoid comparing ranks of different divisions. These are",
        "within-student comparisons across distinct conditions—not claims that",
        "one environment causes performance in the other.",
        "The exploratory 95% percentile intervals resample complete paired STUDENTS",
        "(2,000 draws per metric), not frames or individual games. They do NOT",
        "adjust for league schedule differences, opponent difficulty, code changes",
        "or selection bias. This is one time-specific Division 1 cohort.",
        "",
        "## 3. Compare actual outcomes side by side","",
        "![Same students: food acquisition](charts/joint_apples.svg)","",
        "![Same students: length retained](charts/joint_length.svg)","",
        "![Same students: kills](charts/joint_kills.svg)","",
        "![Same students: retention ratio](charts/joint_retention.svg)","",
        "Every dot represents one matched student-season. The x-axis is the",
        "three-trial average; y-axis is the actual league average against",
        "at least two student opponents. Trial seeds are fixed, while league",
        "match opponents, seats and seeds vary by schedule.",
        "",
        "## 4. Current Division 1: actual joined rows","",
        "| Rank | Student | League games | League wins % | League apples | League retained | League kills | Trial apples | Trial retained | Trial kills | Replay coverage L/T |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in official:
        win=(100*r["league_win_rate"] if r["league_win_rate"] is not None else None)
        lines.append(
            f"| {r['official_rank']} | {r['team']} | {r['league_games']} | "
            f"{printable(win,1)} | {printable(r['league_mean_food'],1)} | "
            f"{printable(r['league_mean_retention'],2)} | {printable(r['league_mean_kills'],2)} | "
            f"{printable(r['trial_mean_food'],1)} | {printable(r['trial_mean_retention'],2)} | "
            f"{printable(r['trial_mean_kills'],2)} | {r['league_replays']}/{r['trial_replays']} |")
    lines += [
        "",
        "## 5. The same students: *actual replay-derived* behavior","",
        f"Current-season students with BOTH league and trial full replay behavior: "
        f"**{movement['paired_student_replays']}**.",
        "Catalog counts cannot fill in missing replay decisions; only identical,",
        "verifiable frame-derived definitions can be compared across modes.",
        "[See the mode-separated behavioral report](behavior_by_mode.md) for",
        "observed food-event/death rates and their conditional correlations.",
        "![Student food events per observed move in each mode](charts/observed_food_by_mode.svg)",
        "![Student deaths per observed move in each mode](charts/observed_deaths_by_mode.svg)",
        "### Forward-looking head pressure and escape space",
        f"Unique replays with complete frame-based pressure analysis: **{threat['replays']}**",
        f"(league **{threat['league_replays']}**, trial **{threat['trial_replays']}**).",
        "Measure danger BEFORE the outcome: each living student's nearest",
        "opponent head, free adjacent cells, then death events in the NEXT",
        "ten turns. See [head-pressure and escape study](threat_windows.md)",
        "for length-stratified results, per-replay counts and uncertainty.",
        "![10-turn death frequencies by head proximity](charts/head_pressure_vs_death.svg)",
        "### Matched death autopsies versus observed 10-turn escapes",
        f"League death cases paired to real survivors: **{autopsies['matched_league']}**.",
        f"On-arrival trial death cases paired separately: **{autopsies['matched_trial']}**.",
        "[Explore actual first-turn escape movement](escape_autopsies.md),",
        "matching on initial length, head proximity, and available neighboring",
        "cells. Later-turn comparisons exclude early deaths and are subject",
        "to survivorship selection, not a proof of causal protection.",
        "![Matched death versus escape movements](charts/escape_case_control.svg)",
        "### Research-to-algorithm decision registry",
        "Our [falsifiable rulebook](algorithm_rulebook.md) tracks",
        f"**{candidate_rules['rules']} proposed state-to-action hypotheses** with",
        "supporting studies, counterexamples and required validation.",
        "NO observational rule is automatically promoted into the new agent.",
        "### All competitors: strong, middle, and struggling league cohorts",
        "[Compare all three performance cohorts](competitive_cohorts.md)",
        "using official standings from the SAME replay season, with body-length",
        "and danger-state common-support checks. Palmer and the submitted",
        "snake are ordinary members of their cohorts, not a head-to-head.",
        f"Same-season ranked league danger windows: **{cohorts['ranked_league_windows']:,}**.",
        "![League and trial cohorts by danger response](charts/cohort_danger_outcomes.svg)",
        "### Which actual first moves preserve usable future space?",
        "The [route-space investigation](route_space.md) contrasts frozen",
        "flood-fill with an 8-step simulated moving-own-tail continuation for",
        "EACH alternative first move, then measures the actual chosen action.",
        "The model freezes opponents and assumes no growth; its routes are",
        "NOT engine-verified safe paths or counterfactual outcomes.",
        f"Replay-sampled danger positions with route features: **{routes['modeled_windows']}**.",
        "![Recorded high-route-space first moves by cohort](charts/route_choice_cohorts.svg)",
        "### Does the snake remain safe after its first escape?",
        "[Palmer's audited danger-response casebook](palmer_casebook.md) gives",
        "one earliest dangerous position per unique league replay and",
        "the actual head movements, local exits, opponent distances and apples.",
        "The [10/20/30-turn survival analysis](long_horizon_survival.md) checks",
        "recorded deaths after danger, treats respawns as failures, and",
        "censors missing future frames. It also compares Palmer with actual",
        "students in his archived league games, not benchmark opponents.",
        "![Death-free +10 and conditional +30 outcomes](charts/danger_survival_30.svg)",
        "![Early recovered free cells versus late deaths](charts/escape_recovery_late_death.svg)",
        "",
        "## 6. Longitudinal disagreement: league specialists vs trial specialists","",
        f"Historical Division 1 snapshots with matched outcome comparisons: "
        f"**{history['division1_snapshots']}**.",
        "We rank the same eligible students within each official division and",
        "season, then compare league versus trial percentiles. Repeated hourly",
        "snapshots are correlated and do not form independent experiments.",
        "[Open the historical disagreement study](seasonal_disagreement.md).",
        "![Historical rank agreement](charts/historical_rank_alignment.svg)",
        "![Students specializing in league or trials](charts/league_trial_outliers.svg)",
        "",
        "## 7. Older seasons with actual peer games but no saved standings","",
        f"Historical seasons comparable by match-derived Division 1 outcomes: "
        f"**{peer_history['div1_snapshots']}** snapshots.",
        "This study uses cataloged student-versus-student placements when old",
        "OFFICIAL rankings were not archived. These are explicitly labeled",
        "match-derived outcomes, never represented as official league rank.",
        "[Open historical peer-game versus trial results](historical_peer_comparison.md).",
        "![Old league match outcomes and trial growth](charts/historical_peer_vs_trial.svg)",
        "",
        "## 8. Reproducible joined data exports","",
        "- [League team-season summaries](../derived/league_team_seasons.csv) —",
        "  the real competition outcomes, including human-opponent counts.",
        "- [Trial team-season summaries](../derived/trial_team_seasons.csv) —",
        "  three controlled benchmark setups, kept separate.",
        "- [Joined student-season dataset](../derived/joined_team_seasons.csv) —",
        "  one row per student and season; missing sides are **missing**, not zero.",
        "- [Historical game-based peer performance comparisons](../derived/historical_peer_trial_correlations.csv) —",
        "  actual archived matches; does NOT imply missing official rank.",
        "- [Historical league–trial student rank gaps](../derived/seasonal_rank_gaps.csv) —",
        "  comparable within-division student-season ranks; snapshots not independent.",
        "- [Danger follow-ups (10/20/30 turns)](../derived/long_horizon_danger_windows.csv) —",
        "  death-event validated, with right-censoring and actual +3 actions.",
        "- [Matched death/survival replay observations](../derived/escape_matched_pairs.csv) —",
        "  baseline-matched cases and real early turn trajectories.",
        "- [Head-pressure and local-exit exposures](../derived/threat_window_student_seasons.csv) —",
        "  sampled from actual replay frames, with next-10-turn outcomes.",
        "- [Replay-backed behavior, separated by mode](../derived/replay_behavior_by_mode.csv) —",
        "  only downloaded full match observations.",
        "- [Data validation summary](../derived/quality.json) —",
        "  replay coverage, SHA deduplication and sample sizes.",
        "",
        "## 9. What needs further evidence","",
        "1. Obtain full league replays of top Division 1 students, including both",
        "   winners and losers, and map their exact turns/deaths/food contests.",
        "2. Run the **same replay-derived definitions** separately on league and",
        "   on-arrival data: food pursuit, death risk, contest pressure and mobility.",
        "3. Compare like-for-like length, turn phase, opponent skill and version.",
        "4. Group uncertainty by complete match/season, not thousands of turns.",
        "5. Interpret only held-out, version-aware patterns before changing our snake.",
        "",
        "This joined report establishes observational associations, not an optimal",
        "aggression/safety formula. No competition snake code has been modified.",""
    ]
    dest=output/"joint_analysis.md"
    dest.write_text("\n".join(lines),encoding="utf-8")
    home=[
        "# Snake26 Research — Start here","",
        "The **canonical research entry point** is [Joined League + Trials](joint_analysis.md).",
        "Read this before interpreting the older single-environment reports.",
        "",
        "## Source-of-truth datasets","",
        "- [League outcomes](../derived/league_team_seasons.csv)",
        "- [Trial outcomes](../derived/trial_team_seasons.csv)",
        "- [Joined per student-season outcomes](../derived/joined_team_seasons.csv)",
        "- [Coverage, completeness and quality checks](../derived/quality.json)","",
        "## Supporting studies — with explicitly limited scopes","",
        "- [Official league versus fixed-seed rankings](league_vs_trials.md):",
        "  standings/outcomes, not a replay-derived behavioral model.",
        "- [Historical actual peer-match outcomes vs trials](historical_peer_comparison.md):",
        "  works without older official standings; **game-derived proxy** only.",
        "- [League/trial specialists across historical snapshots](seasonal_disagreement.md):",
        "  matched division ranks, tracked across recorded seasons and bot hashes.",
        "- [Evidence-gated algorithm rulebook](algorithm_rulebook.md):",
        "  falsifiable state-to-action hypotheses for a NEW agent, not code fixes.",
        "- [Actual student decisions versus future route space](route_space.md):",
        "  frozen-body vs own-moving-tail route-proxy audit by performance cohort.",
        "- [All competitors: strong/middle/struggling cohorts](competitive_cohorts.md):",
        "  same-season rank-matched danger outcomes, separated league vs trials.",
        "- [Palmer league danger decision sequences](palmer_casebook.md):",
        "  one deterministic audited real episode per unique league replay.",
        "- [Danger escapes: do they stay safe for 20–30 turns?](long_horizon_survival.md):",
        "  censored follow-ups and same-game Palmer comparison.",
        "- [Matched death autopsies versus escapes](escape_autopsies.md):",
        "  actual ten-turn outcomes with observable early actions; not a policy test.",
        "- [Head pressure, local exits, and future deaths](threat_windows.md):",
        "  actual replay frames; mode- and length-stratified, not a proven policy.",
        "- [Observed league/trial behavior matched by student](behavior_by_mode.md):",
        "  replay-derived food and death measures; report sample coverage first.",
        "- [League food versus growth retained](league_sweet_spot.md):",
        "  correlation, not proven aggression or optimal policy.",
        "- [On-arrival food contests](food_races.md):",
        "  primarily student-versus-built-in benchmark observations.",
        "- [On-arrival underdog apple case studies](underdog_study.md):",
        "  benchmark-specific, NOT evidence about peers in league matches.",
        "- [Historical replay behavioral proxies](strategy_lab.md):",
        "  cross-mode exploratory snapshots; treat aggregates as preliminary.",
        "- [Replay growth/death exploratory plots](data_science.md):",
        "  mixed-mode student exposure; see mode separation warnings.",
        "",
        "## Operating rules","",
        "Research reports are generated from the repository's SQLite catalogs",
        "and archived replay frames by one scheduled GitHub Actions collector.",
        "Research code changes alone do not trigger data downloads. A separate",
        "read-only validation workflow tests new analysis code.",
        "All files are private repository research artifacts; no private bot",
        "executables or source code are extracted. No Java snake changes yet.",""
    ]
    (output/"README.md").write_text("\n".join(home),encoding="utf-8")
    return dict(season=latest,route_space_windows=routes["modeled_windows"],candidate_rules=candidate_rules["rules"],competitive_cohort_ranked_league_windows=cohorts["ranked_league_windows"],long_horizon_windows=long_horizon["league"]["baseline"]+long_horizon["trial"]["baseline"],matched_autopsies_league=autopsies["matched_league"],matched_autopsies_trial=autopsies["matched_trial"],head_pressure_windows=threat["windows"],peer_history_div1_snapshots=peer_history["div1_snapshots"],historical_div1_snapshots=history["division1_snapshots"],replay_paired=movement["paired_student_replays"],paired_division1=len(paired),
                comparison={r["metric"]:r["rho"] for r in results},
                reports=[str(dest),str(output/"README.md")])

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    args=p.parse_args()
    print(json.dumps(build(args.data_dir),indent=2))

if __name__=="__main__":
    main()
