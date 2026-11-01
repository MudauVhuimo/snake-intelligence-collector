# Snake26 Research Protocol

**Status:** Exploratory, observational research. Do not modify the competition Java agent until the user explicitly requests that phase.

## Evidence tiers

- **Tier A — Raw replay frames:** actual observed positions, food, movement, deaths, and timestamps. Validate event state alignment and duplicate SHA-256 payloads.
- **Tier B — Match catalog:** published participants, score, placement, food, kills, seed, kind, and replay path. Does not directly establish death timing or route choice.
- **Tier C — Behavioral proxies:** greedy-food choices, free-space estimates, trap risk, opponent pressure, and putative strategies inferred from visible states. These are model-dependent interpretations.
- **Tier D — Counterfactuals:** what would have happened had a different action been taken. A replay alone CANNOT answer this; require a live simulator and responsive opponents.

## Core research questions

1. **Growth versus survival:** distinguish apples collected, retained length, maximum length, and deaths. Plot time-resolved length with actual death/respawn markers.
2. **Food competition:** for each food appearance, identify candidate snakes, toroidal distance, competing arrival times, and actual winner. Compare equal body-length and threat strata.
3. **Death autopsies:** inspect 50 turns before each death, opponent approach, available safe cells, trapped area, and whether the tail was reachable. Match controls at similar length and turn.
4. **Spatial risk:** density of occupied cells, dynamic tail-vacancy risk, reachable future space, adversarial head move cones, and room to maneuver.
5. **Strategy fingerprints:** relative turns, target pursuit, time to apples, looping behavior, low-space avoidance, and response to larger opponents.
6. **Bot evolution:** correlate changed submission SHA-256 with matched changes in on-arrival trials and league results; do not attribute differences solely to code.
7. **Efficiency:** measure objective-relevant retention and apples per alive turn, latency distribution, and timeout/rejected moves.

## Sampling and inference

- **Avoid replay duplication:** identical SHA-256 payloads are one exact observation, not independent evidence; distinguish this from same seed/output summaries.
- **Avoid bot-version contamination:** keep code hashes and match-season combinations explicit. A named team can change strategy across seasons.
- **Avoid within-match pseudo-replication:** 2,000 adjacent turns are correlated; statistical uncertainty should be clustered by match, then stratified by season/opponent.
- **Avoid unearned conclusions:** simple occupancy flood fill treats moving tails as blocked and can tie many moves at the scoring cap. A 99% roomiest-choice rate alone is not evidence of a particular planner.
- **Separate game modes:** on-arrival trials against common built-in opponents are not league matches against other students; compare like with like.
- **Normalize observed risk:** divide actual death events by alive-turn exposure for the relevant state-length bin. Report denominator and number of unique matches.
- **Use matched controls:** compare danger situations at similar turn, length, occupancy, opponent geometry and engine version.
- **Do not infer code from replay:** observed actions are evidence of behavior, not source-code access.

## Phase I — Descriptive dashboard

Created by `python -m research.dashboard`. Includes catalog coverage, shared gauntlet_1 final length ranking, apples versus retained final length, recorded growth curves, death causes, and length-specific death-event exposure rates. Figures are SVGs embedded in `data/reports/data_science.md`.

## Phase II — Event studies

For each real death, record a pre-event window (e.g. 50 preceding turns), with time-aligned mobility, free-cell count, tail distance, opponent threats, and food-target opportunity. Select control windows that did not end in death from the same season/opponent setup and similar starting conditions. Plot trajectories plus effect-size confidence intervals clustered by match.

## Phase III — Food races

At each spawn, calculate per-snake toroidal Manhattan distance, potential head collisions, and occupancy-aware path length; track which snake consumes the apple and how long it takes. Analyze near-tie contests separately from unopposed apples. Avoid treating food acquired by another bot as a failure of pursuit without accounting for relative positions.

## Phase IV — Strategies for later validation

Convert stable empirical patterns into pre-registered hypotheses for an independent Java candidate, but do not implement it during the research-only phase. On replay state/action prediction, hold out entire matches and code versions. A valid policy prediction is **not** proof of improved competitive performance; only controlled live benchmarking can establish that.

**Data ethics and operations:** publicly accessible read-only API; respectful request pacing, no private credentials/source extraction, no server load spikes; retain work in the private repository and monitor storage growth.
