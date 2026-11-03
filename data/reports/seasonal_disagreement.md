# Snake26: historical league versus trial specialization

Generated UTC: 2026-11-03T19:59:21+00:00

## Design and guardrails

League ranks are official division-specific rankings; we rerank students
inside the SAME eligible division cohort by their average final length
across the three fixed on-arrival trials. Official positions are separately
reranked within this eligible cohort before computing percentile gaps.
We require at least three cataloged peer league
games, all three on-arrival trials, and at least 10 students per division.
A normalized rank difference of +1 means excellent trials relative to
league, and -1 means excellent league performance relative to trials.
These are ranks, NOT inferred policy scores or match-level causal effects.

Current season: **2026-11-03-185906-season**.
Eligible historical Division 1 standings snapshots: **12**.
Positive league/trial rank correlation: **12** snapshots.
Median Division 1 correlation: **+0.338**.

Hourly seasons, repeated seeds, and unchanged bot versions are strongly
correlated. The history is a trajectory of recorded competition snapshots,
**not** a set of independent randomized experiments.

## 1. How does correlation evolve across seasons?

![Historical rank alignment](charts/historical_rank_alignment.svg)

| Season | Division 1 students | Spearman rho: league rank vs trial growth rank |
|---|---:|---:|
| 2026-11-03-185906-season | 32 | +0.332 |
| 2026-11-03-145900-season | 32 | +0.344 |
| 2026-11-03-115900-season | 32 | +0.263 |
| 2026-11-03-055900-season | 32 | +0.275 |
| 2026-11-03-025900-season | 32 | +0.277 |
| 2026-11-02-225901-season | 32 | +0.488 |
| 2026-11-02-145901-season | 32 | +0.354 |
| 2026-11-02-045859-season | 32 | +0.417 |
| 2026-11-01-235859-season | 32 | +0.401 |
| 2026-11-01-225859-season | 32 | +0.442 |
| 2026-11-01-215859-season | 32 | +0.069 |
| 2026-11-01-205859-season | 32 | +0.140 |

## 2. Who specializes in a DIFFERENT environment?

![Within-Division rank gaps](charts/league_trial_outliers.svg)

**Positive difference:** relatively stronger three-trial growth;
**negative:** relatively stronger competitive league rank.

| Trial specialists (Division 1) | League rank | Trial rank within Division 1 | Gap | League games | League full replays |
|---|---:|---:|---:|---:|---:|
| 422453-mauricetshepo-frost | 24 | 1.0 | +0.74 | 4 | 0 |
| 419636-jason-chen | 26 | 5.0 | +0.68 | 5 | 0 |
| 388060-tshepang-tshabalala | 22 | 3.0 | +0.61 | 6 | 1 |
| 403754-vhuimo-mudau | 27 | 16.0 | +0.35 | 4 | 0 |
| 408008-bradley-buys | 28 | 17.0 | +0.35 | 5 | 1 |
| 429782-maseeha-seedat | 29 | 19.0 | +0.32 | 4 | 1 |
| 421538-tshifhiwa-bvumbi | 14 | 6.0 | +0.26 | 6 | 0 |

| League specialists (Division 1) | League rank | Trial rank within Division 1 | Gap | League games | League full replays |
|---|---:|---:|---:|---:|---:|
| 408070-collen-mthombeni | 9 | 30.0 | -0.68 | 4 | 1 |
| 423258-muhammed-dar | 13 | 32.0 | -0.61 | 5 | 0 |
| 428786-marvellous-sambo | 7 | 25.0 | -0.58 | 3 | 0 |
| 421462-alexander-palmer | 1 | 15.0 | -0.45 | 3 | 3 |
| 389160-lwandle-ramanugu | 16 | 29.0 | -0.42 | 4 | 2 |
| 426895-mpho-ramasakona | 17 | 26.5 | -0.31 | 5 | 1 |
| 424820-elisha-mundalamo | 4 | 13.0 | -0.29 | 5 | 2 |

## 3. Repeated snapshots and bot changes

The next table lists select current Division 1 extremes. SHA counts are
distinct *season-snapshot* version hashes, not confirmed per-match hashes.
Repeated identical snapshots can produce apparent consistency without
new independent evidence.

| Student | Eligible Division 1 snapshots | Distinct snapshot hashes | Median rank gap |
|---|---:|---:|---:|
| 422453-mauricetshepo-frost | 1 | 1 | +0.74 |
| 419636-jason-chen | 7 | 1 | +0.61 |
| 388060-tshepang-tshabalala | 9 | 1 | +0.45 |
| 403754-vhuimo-mudau | 6 | 1 | +0.18 |
| 408070-collen-mthombeni | 12 | 1 | -0.46 |
| 423258-muhammed-dar | 9 | 2 | -0.13 |
| 428786-marvellous-sambo | 12 | 1 | -0.58 |
| 421462-alexander-palmer | 12 | 1 | -0.35 |

## 4. What this changes in our replay investigation

Target BOTH ends of the disagreement distribution: trial specialists
who underperform in league, and league specialists who struggle in trials.
For each, obtain actual full games from both environments and compare:
survival/respawn, contested-food decisions, opponent proximity, risk versus
growth and match outcomes under comparable conditions.
Use historical snapshots to select interesting students, NOT as
evidence of stable strategy unless versions and game conditions match.

## Export

[All historical matched student-season rank gaps](../derived/seasonal_rank_gaps.csv)

This is observational research; no competition snake has been modified.
