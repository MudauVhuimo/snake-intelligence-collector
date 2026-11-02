# Snake26 — Research program for designing a competitive decision algorithm

**Research mission:** discover *generalizable state → action decision rules* that maximize performance in **real student-versus-student league play**. The goal is **not** to reproduce, reverse-engineer, or outperform any particular student's observed policy in a head-to-head case study. A single competitor's replay can be a counterexample or diagnostic, never a source of universally accepted rules.

**Research mode:** no competition agent implementation until hypotheses have passed the evidence gates below. Distinguish observations, plausible causal mechanisms, and tested rules.

## The precise question

> Given a Snake26 game state, what information is sufficient to rank the available actions so that the resulting policy increases expected competitive performance across many different opponents, starting positions, board densities, and stages of a match?

We seek a **state-dependent decision system**, not one global rule such as “always chase the nearest apple” or “always maximize immediately empty neighbors.”

### The decisions the future agent will have to make

| Decision | General research question | Features to test, not assume | Required comparison |
|---|---|---|---|
| **A. Legal/safe action filter** | When is a move *certainly fatal* versus merely risky? | Formal engine collision order, moving tails, head-to-head rules, body position | Verify against official platform rules and replay transitions; no inferred legality from a frozen board |
| **B. Short-horizon survival** | When should immediate survival override food or aggression? | Opponent-head reachability, relative lengths, contested cells, local exits, time-to-collision | Death within 1/3/10 turns, conditioned on body length and opponent context, grouped by match |
| **C. Long-term mobility** | Which safe move avoids future enclosure? | Tail-aware reachable area, articulation points, dead ends, body release time, region connectivity | Survival and route availability at 10/30/100 turns versus static-neighbor baselines |
| **D. Food choice** | When is an apple worth pursuing, and when should it be abandoned? | Toroidal distance, safe shortest path, opponent arrival time, pursuit detour, post-eating escape space | Verified captures and subsequent death/growth, separately league vs trials |
| **E. Competitive confrontation** | When should a snake press, yield, block, or attack? | Head-on rules, size advantage, relative heading, opponent projected moves, kill opportunity, escape after attack | Actual student-opponent encounters, kills/deaths/placement, not benchmark-only aggression |
| **F. Growth versus risk** | When does collecting one more apple lower expected final performance? | Current retained length, food reward, estimated death loss, phase, number of safe exits | Food gained **and retained** versus deaths, first-place rate, final length and opponent context |
| **G. Adaptive strategy** | Should priorities change with size, density, opponent behavior or remaining turns? | Length, free-space fraction, dangerous-head density, score context, game phase | Stratified estimates and held-out ablations; avoid fixed thresholds until measured |
| **H. Robustness** | Does a rule work across many students, seeds, maps and bot versions? | League/trial environment, opponent archetypes, version snapshot, map, seed, season | Entire held-out **games/versions**; re-run paired-seed league-like benchmarks |
| **I. Computation budget** | How deep must lookahead be, and when is computation worth spending? | Branching factor, horizon, density, board occupancy, distance-to-threat | Search-depth ablations, correctness and time/memory limits under platform interface |

For every decision, we aim to produce: **an observable feature definition, an estimated risk/reward tradeoff, a candidate decision rule, a counterexample, and a test that could falsify it.**

## Evidence and generalization rules

1. **League is the primary outcome target.** Use official league results and student-versus-student full replays to learn competitive behaviors. On-arrival trials are a *separate controlled test environment*, not the optimization target. Join the same student and season to study transfer only when both have actual data.
2. **Keep match catalogs and replay evidence separate.** Catalogs support wins, final length, food and placement. Only frames and genuine events support observed movements, deaths, route choices, and exposure measures.
3. **Do not study only winners.** Sample successes, failures, near misses, ordinary snakes and different opponent strategies. Match or stratify on body length, density, phase, relative heading, seed/map, player, and version where available.
4. **Use the actual mechanics.** Verify the platform's collision order, walls/toroidal behavior, head-to-head outcomes, food growth and death resets against official rules and replay transitions *before* writing a safety invariant. Current frozen-body BFS and free-neighbor measures are descriptive approximations, not legal move engines.
5. **No counterfactual claims from replays.** One observed action cannot reveal what would have happened under a different action because opponents and future board states react. A “survivor used X” statement does not prove “X prevents death.”
6. **Measure exposure, not only deaths.** Compare risk per alive snake-turn, conditional on geometry and opponent proximity. Account for game-ending censoring, death followed by respawn, and the fact that multiple sampled turns from one game are correlated.
7. **Avoid leakage and pseudo-replication.** Build predictors only from information available at decision time; reserve outcomes for labels. Bootstrap full replay matches (or student/version clusters when appropriate), not turns. Hourly snapshots with reused seeds/codes are not independent trials.
8. **Use holdouts before promotion.** Partition by entire replay/game, preferably by opponent group, version or later season. Compare improvements to a locked baseline with the same seeds and opponents. Do not promote based on a single seed, one strong snake, or trial growth alone.

## Evidence gates: how observations become rules

| Stage | Label | Required proof | What may be claimed |
|---|---|---|---|
| **0** | Open question | Well-defined state/action/outcome and known data gaps | A hypothesis to investigate |
| **1** | Observed association | Source-linked analysis, denominators, mode separation, uncertainty, counterexamples | A *possible* feature or mechanism; **not** a policy |
| **2** | Replicated predictor | Holds in held-out whole games and several opponent contexts, adjusted/stratified for obvious confounders | Worth testing as a rule |
| **3** | Controlled candidate | A controlled, reproducible agent ablation on common seeds and diverse opponents improves league-like competitive objectives without a serious failure tradeoff | A testable policy component |
| **4** | Promoted rule | Repeated fresh/held-out paired-seed evaluation; sufficient gain in competitive outcomes and acceptable survival/computation across contexts | May enter the final algorithm |

**Important:** No current observational study has promoted a behavioral policy to stages 3 or 4. Stage 4 cannot be conferred by an appealing correlation or by comparing two named students.

### Initial synthesis: what the existing archive *actually* supports

| Observation (source) | Interpretation allowed | What is **not** established |
|---|---|---|
| In league replays, head distance ≤3 correlated with death within 10 turns more than distance ≥8: 2.14% vs 0.29% ([head-pressure](../data/reports/threat_windows.md)) | Proximity belongs in risk features | “Always flee from heads”; opponent position/length and current geometry are confounders |
| When league head distance ≤3, 0–1 currently unoccupied neighbors correlated with 10.58% death vs 1.49% with 2–4 ([head-pressure](../data/reports/threat_windows.md)) | Escape-space scarcity deserves strong attention | That maximizing *current* empty cells is optimal; tails move and the future matters |
| In league, gaining an extra free neighbor within 3 turns was associated with less death in turns 11–30 after surviving the first 10: 1.55% vs 3.09% ([30-turn follow-up](../data/reports/long_horizon_survival.md)) | Mobility recovery may matter as a multi-turn feature | Causality, universal thresholds, or transfer to controlled trials (trial result differs) |
| League final length aligned more strongly with official division rank than apples per game: Spearman 0.797 vs 0.364 ([food/retention](../data/reports/league_sweet_spot.md)) | Rewards must account for growth *retained* and competitive outcome | That apples are unimportant, or that an observed snake deliberately avoided risk |
| In **trials**, static occupied-path ordering predicted many food-race outcomes better than head-distance order ([path geometry](../data/reports/path_geometry.md)) | Safe, obstacle-aware travel time deserves testing | That static BFS is a legal future route, or that the effect extends to student league competition |
| Fixed trial performance and competitive league placement show only partial agreement ([league vs trials](../data/reports/league_vs_trials.md)) | Optimize real competitive outcomes and test transfer | A universal “aggression/safety sweet spot” or a competitor-specific blueprint |

These are **provisional findings, not algorithmic instructions**. Some are based on selected replays and may change as collection improves. Keep contradictory and negative evidence in the record.

## Research work products, in priority order

**Priority 1 — Verify mechanics and build action-level features.** Inspect platform rules, confirm tail-vacating legality and head collision mechanics. From each replay state reconstruct each snake's real move, current occupancy, possible next head cells, opponent reach sets, opponent size, nearest *safe* food path, and a short dynamic reachable-space estimate. Audit each feature against replay transitions. Never confuse hypothetical legal moves with observed decisions.

**Priority 2 — Explain survival-versus-growth in real league games.** Estimate future death risk and retained growth conditional on length, head pressure, confinement, game phase, and verified food opportunities. Build same-game risk strata; include every performance quartile, not just elite snakes. Find conditions where an apple pursuit improves expected outcome versus getting trapped.

**Priority 3 — Test contested food and opponent head interactions.** For each newly visible apple, enumerate all students that can plausibly reach it; assess safe travel time and next-3-turn head hazards. Observe actual consumption, winner, death and remaining mobility. Distinguish deliberate chase from accidental trajectory correlation. Repeat with league students and trials separately.

**Priority 4 — Risk-aware route planning.** Compare first-neighbor count with static flood fill, tail-aware reachable area, temporal connectivity and narrow corridor detection. Ask which predictors forecast death and reduced growth on held-out league games. Negative results matter as much as positive.

**Priority 5 — Synthesize a state→action policy only after gates 2–3.** Start from engine-verified legality, estimate survival probability and future mobility for each permitted action, estimate safe food and competitive opportunities, then rank actions using *measured* costs and rewards. Test alternate orderings/weights and fallback rules under paired seeds. There are NO defensible numerical coefficients yet.

## Proposed policy *shape*, not an implementation

```text
Given observable state s:
    A <- moves verified legal under official game mechanics
    for a in A:
        risk[a]       <- estimate short-horizon collision/death probability
        mobility[a]   <- estimate tail-aware future reachable/escape region
        food[a]       <- estimate contest-adjusted safe reward and arrival time
        contest[a]    <- estimate opponent/head-control benefit and exposure
    apply state-dependent safety/reward tradeoff, to be learned/tested
    select action with strongest experimentally validated competitive value
    if evidence or budget is insufficient: use tested conservative fallback
```

The *existence* of these modules is a design hypothesis. Their definitions, cutoffs, weights, lookahead depth, and ordering all remain open until checked.

## How to use the research registry

The companion [candidate-rule registry](../research/rule_candidates.json) is the machine-readable backlog. The scheduled dashboard renders [algorithm rulebook](../data/reports/algorithm_rulebook.md) from that registry. Each record identifies the question, status, evidence scope, proposed rule, falsification/validation work and its next measurable result. Update it whenever a study answers a question, contradicts a rule, or exposes a gap.

Individual-player casebooks are **diagnostic appendices only**. They cannot replace population-level inference or advance the status of a rule. **The goal is to discover general principles—not reproduce any student's snake.**
