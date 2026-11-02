# Snake26: historical league versus trial specialization

Generated UTC: 2026-11-02T06:36:50+00:00

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

Current season: **2026-11-02-045859-season**.
Eligible historical Division 1 standings snapshots: **5**.
Positive league/trial rank correlation: **5** snapshots.
Median Division 1 correlation: **+0.401**.

Hourly seasons, repeated seeds, and unchanged bot versions are strongly
correlated. The history is a trajectory of recorded competition snapshots,
**not** a set of independent randomized experiments.

## 1. How does correlation evolve across seasons?

![Historical rank alignment](charts/historical_rank_alignment.svg)

| Season | Division 1 students | Spearman rho: league rank vs trial growth rank |
|---|---:|---:|
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
| 388060-tshepang-tshabalala | 25 | 1.0 | +0.77 | 6 | 2 |
| 419636-jason-chen | 24 | 3.0 | +0.68 | 5 | 0 |
| 408008-bradley-buys | 29 | 15.0 | +0.45 | 6 | 1 |
| 413538-lelethuthando-nikelo | 14 | 2.0 | +0.39 | 6 | 2 |
| 421349-phathutshedzo-mudzanani | 16 | 5.0 | +0.35 | 6 | 0 |
| 422777-thandile-mamiana | 26 | 20.0 | +0.19 | 5 | 1 |
| 425488-zinhle-zitha | 30 | 24.0 | +0.19 | 5 | 0 |

| League specialists (Division 1) | League rank | Trial rank within Division 1 | Gap | League games | League full replays |
|---|---:|---:|---:|---:|---:|
| 428786-marvellous-sambo | 5 | 26.0 | -0.68 | 5 | 1 |
| 408070-collen-mthombeni | 11 | 31.5 | -0.66 | 5 | 0 |
| 389160-lwandle-ramanugu | 17 | 29.5 | -0.40 | 6 | 1 |
| 428954-njabulo-ndlozi | 8 | 19.0 | -0.35 | 6 | 1 |
| 421462-alexander-palmer | 1 | 11.0 | -0.32 | 6 | 6 |
| 404721-khensani-maluleke | 21 | 29.5 | -0.27 | 5 | 0 |
| 423135-mpho-muremi | 13 | 21.0 | -0.26 | 5 | 0 |

## 3. Repeated snapshots and bot changes

The next table lists select current Division 1 extremes. SHA counts are
distinct *season-snapshot* version hashes, not confirmed per-match hashes.
Repeated identical snapshots can produce apparent consistency without
new independent evidence.

| Student | Eligible Division 1 snapshots | Distinct snapshot hashes | Median rank gap |
|---|---:|---:|---:|
| 388060-tshepang-tshabalala | 4 | 1 | +0.61 |
| 419636-jason-chen | 3 | 1 | +0.68 |
| 408008-bradley-buys | 3 | 1 | +0.42 |
| 413538-lelethuthando-nikelo | 5 | 1 | +0.29 |
| 428786-marvellous-sambo | 5 | 1 | -0.65 |
| 408070-collen-mthombeni | 5 | 1 | -0.47 |
| 389160-lwandle-ramanugu | 5 | 1 | -0.40 |
| 428954-njabulo-ndlozi | 5 | 1 | -0.27 |

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
