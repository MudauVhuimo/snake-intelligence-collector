# Snake26: historical league versus trial specialization

Generated UTC: 2026-11-06T11:09:00+00:00

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

Current season: **2026-11-06-102324-season**.
Eligible historical Division 1 standings snapshots: **13**.
Positive league/trial rank correlation: **13** snapshots.
Median Division 1 correlation: **+0.332**.

Hourly seasons, repeated seeds, and unchanged bot versions are strongly
correlated. The history is a trajectory of recorded competition snapshots,
**not** a set of independent randomized experiments.

## 1. How does correlation evolve across seasons?

![Historical rank alignment](charts/historical_rank_alignment.svg)

| Season | Division 1 students | Spearman rho: league rank vs trial growth rank |
|---|---:|---:|
| 2026-11-06-102324-season | 32 | +0.120 |
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
| 422453-mauricetshepo-frost | 30 | 1.0 | +0.94 | 6 | 0 |
| 409987-sbongakonke-shange | 28 | 8.5 | +0.63 | 5 | 0 |
| 421349-phathutshedzo-mudzanani | 19 | 4.0 | +0.48 | 4 | 0 |
| 426650-babongile-mafantiri | 32 | 18.5 | +0.44 | 6 | 0 |
| 402334-angile-saho | 27 | 14.0 | +0.42 | 6 | 1 |
| 429653-elohim-mahungele | 31 | 18.5 | +0.40 | 6 | 3 |
| 423239-zeeshaan-bham | 18 | 6.0 | +0.39 | 5 | 1 |

| League specialists (Division 1) | League rank | Trial rank within Division 1 | Gap | League games | League full replays |
|---|---:|---:|---:|---:|---:|
| 404721-khensani-maluleke | 8 | 29.5 | -0.69 | 6 | 0 |
| 408070-collen-mthombeni | 10 | 31.0 | -0.68 | 6 | 0 |
| 410193-vhugala-makhwathane | 9 | 29.5 | -0.66 | 6 | 0 |
| 408501-asher-urison | 6 | 24.0 | -0.58 | 5 | 0 |
| 421462-alexander-palmer | 1 | 15.0 | -0.45 | 4 | 4 |
| 420790-damian-nel | 2 | 13.0 | -0.35 | 6 | 1 |
| 426895-mpho-ramasakona | 17 | 27.0 | -0.32 | 6 | 1 |

## 3. Repeated snapshots and bot changes

The next table lists select current Division 1 extremes. SHA counts are
distinct *season-snapshot* version hashes, not confirmed per-match hashes.
Repeated identical snapshots can produce apparent consistency without
new independent evidence.

| Student | Eligible Division 1 snapshots | Distinct snapshot hashes | Median rank gap |
|---|---:|---:|---:|
| 422453-mauricetshepo-frost | 2 | 1 | +0.84 |
| 409987-sbongakonke-shange | 1 | 1 | +0.63 |
| 421349-phathutshedzo-mudzanani | 13 | 1 | +0.19 |
| 426650-babongile-mafantiri | 7 | 1 | +0.19 |
| 404721-khensani-maluleke | 12 | 1 | -0.60 |
| 408070-collen-mthombeni | 13 | 1 | -0.47 |
| 410193-vhugala-makhwathane | 10 | 2 | -0.23 |
| 408501-asher-urison | 11 | 1 | -0.03 |

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
