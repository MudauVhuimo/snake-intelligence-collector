# Snake26: historical league versus trial specialization

Generated UTC: 2026-11-03T15:24:19+00:00

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

Current season: **2026-11-03-145900-season**.
Eligible historical Division 1 standings snapshots: **11**.
Positive league/trial rank correlation: **11** snapshots.
Median Division 1 correlation: **+0.344**.

Hourly seasons, repeated seeds, and unchanged bot versions are strongly
correlated. The history is a trajectory of recorded competition snapshots,
**not** a set of independent randomized experiments.

## 1. How does correlation evolve across seasons?

![Historical rank alignment](charts/historical_rank_alignment.svg)

| Season | Division 1 students | Spearman rho: league rank vs trial growth rank |
|---|---:|---:|
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
| 421538-tshifhiwa-bvumbi | 28 | 4.0 | +0.77 | 5 | 0 |
| 402334-angile-saho | 23 | 1.0 | +0.71 | 5 | 0 |
| 403339-david-ndambo | 22 | 7.0 | +0.48 | 6 | 0 |
| 423158-risima-mashele | 32 | 17.5 | +0.47 | 4 | 0 |
| 388060-tshepang-tshabalala | 13 | 2.0 | +0.35 | 6 | 0 |
| 403501-mashau-mudzanani | 27 | 19.0 | +0.26 | 5 | 1 |
| 427039-sameeha-miabala | 17 | 10.0 | +0.23 | 5 | 0 |

| League specialists (Division 1) | League rank | Trial rank within Division 1 | Gap | League games | League full replays |
|---|---:|---:|---:|---:|---:|
| 404721-khensani-maluleke | 8 | 29.5 | -0.69 | 6 | 1 |
| 428786-marvellous-sambo | 7 | 26.0 | -0.61 | 5 | 0 |
| 426895-mpho-ramasakona | 10 | 27.5 | -0.56 | 6 | 0 |
| 421462-alexander-palmer | 1 | 13.0 | -0.39 | 3 | 3 |
| 423258-muhammed-dar | 21 | 32.0 | -0.35 | 4 | 1 |
| 419342-ayeshan-puckree | 6 | 16.0 | -0.32 | 4 | 1 |
| 424820-elisha-mundalamo | 3 | 11.0 | -0.26 | 5 | 0 |

## 3. Repeated snapshots and bot changes

The next table lists select current Division 1 extremes. SHA counts are
distinct *season-snapshot* version hashes, not confirmed per-match hashes.
Repeated identical snapshots can produce apparent consistency without
new independent evidence.

| Student | Eligible Division 1 snapshots | Distinct snapshot hashes | Median rank gap |
|---|---:|---:|---:|
| 421538-tshifhiwa-bvumbi | 6 | 1 | +0.60 |
| 402334-angile-saho | 11 | 2 | +0.42 |
| 403339-david-ndambo | 11 | 1 | +0.00 |
| 423158-risima-mashele | 1 | 1 | +0.47 |
| 404721-khensani-maluleke | 11 | 1 | -0.56 |
| 428786-marvellous-sambo | 11 | 1 | -0.58 |
| 426895-mpho-ramasakona | 11 | 1 | -0.31 |
| 421462-alexander-palmer | 11 | 1 | -0.35 |

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
