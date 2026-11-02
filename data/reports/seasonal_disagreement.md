# Snake26: historical league versus trial specialization

Generated UTC: 2026-11-02T23:45:14+00:00

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

Current season: **2026-11-02-225901-season**.
Eligible historical Division 1 standings snapshots: **7**.
Positive league/trial rank correlation: **7** snapshots.
Median Division 1 correlation: **+0.401**.

Hourly seasons, repeated seeds, and unchanged bot versions are strongly
correlated. The history is a trajectory of recorded competition snapshots,
**not** a set of independent randomized experiments.

## 1. How does correlation evolve across seasons?

![Historical rank alignment](charts/historical_rank_alignment.svg)

| Season | Division 1 students | Spearman rho: league rank vs trial growth rank |
|---|---:|---:|
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
| 402334-angile-saho | 20 | 1.0 | +0.61 | 6 | 0 |
| 407318-deo-kabunda | 28 | 14.0 | +0.45 | 6 | 0 |
| 419342-ayeshan-puckree | 31 | 19.0 | +0.39 | 4 | 1 |
| 421538-tshifhiwa-bvumbi | 16 | 4.0 | +0.39 | 4 | 0 |
| 388060-tshepang-tshabalala | 13 | 2.0 | +0.35 | 5 | 1 |
| 409997-utayan-naidoo | 23 | 12.0 | +0.35 | 5 | 0 |
| 420285-kgotlelelo-aphane | 26 | 15.5 | +0.34 | 6 | 0 |

| League specialists (Division 1) | League rank | Trial rank within Division 1 | Gap | League games | League full replays |
|---|---:|---:|---:|---:|---:|
| 404721-khensani-maluleke | 11 | 28.0 | -0.55 | 6 | 0 |
| 408070-collen-mthombeni | 15 | 29.0 | -0.45 | 5 | 0 |
| 408501-asher-urison | 10 | 21.0 | -0.35 | 5 | 0 |
| 410193-vhugala-makhwathane | 12 | 22.5 | -0.34 | 6 | 0 |
| 421462-alexander-palmer | 3 | 13.0 | -0.32 | 4 | 0 |
| 424820-elisha-mundalamo | 2 | 11.0 | -0.29 | 6 | 0 |
| 426895-mpho-ramasakona | 18 | 27.0 | -0.29 | 5 | 0 |

## 3. Repeated snapshots and bot changes

The next table lists select current Division 1 extremes. SHA counts are
distinct *season-snapshot* version hashes, not confirmed per-match hashes.
Repeated identical snapshots can produce apparent consistency without
new independent evidence.

| Student | Eligible Division 1 snapshots | Distinct snapshot hashes | Median rank gap |
|---|---:|---:|---:|
| 402334-angile-saho | 7 | 2 | +0.39 |
| 407318-deo-kabunda | 1 | 1 | +0.45 |
| 419342-ayeshan-puckree | 7 | 1 | +0.19 |
| 421538-tshifhiwa-bvumbi | 3 | 1 | +0.39 |
| 404721-khensani-maluleke | 7 | 1 | -0.53 |
| 408070-collen-mthombeni | 7 | 1 | -0.47 |
| 408501-asher-urison | 5 | 1 | +0.03 |
| 410193-vhugala-makhwathane | 4 | 1 | -0.03 |

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
