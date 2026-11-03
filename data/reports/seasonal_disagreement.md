# Snake26: historical league versus trial specialization

Generated UTC: 2026-11-03T07:01:19+00:00

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

Current season: **2026-11-03-055900-season**.
Eligible historical Division 1 standings snapshots: **9**.
Positive league/trial rank correlation: **9** snapshots.
Median Division 1 correlation: **+0.354**.

Hourly seasons, repeated seeds, and unchanged bot versions are strongly
correlated. The history is a trajectory of recorded competition snapshots,
**not** a set of independent randomized experiments.

## 1. How does correlation evolve across seasons?

![Historical rank alignment](charts/historical_rank_alignment.svg)

| Season | Division 1 students | Spearman rho: league rank vs trial growth rank |
|---|---:|---:|
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
| 421538-tshifhiwa-bvumbi | 24 | 4.0 | +0.65 | 5 | 2 |
| 402334-angile-saho | 20 | 1.0 | +0.61 | 4 | 0 |
| 419636-jason-chen | 22 | 3.0 | +0.61 | 5 | 0 |
| 403754-vhuimo-mudau | 32 | 14.0 | +0.58 | 5 | 1 |
| 409997-utayan-naidoo | 30 | 12.0 | +0.58 | 4 | 0 |
| 427039-sameeha-miabala | 23 | 10.0 | +0.42 | 5 | 0 |
| 423436-ntobeko-zondi | 29 | 18.0 | +0.35 | 5 | 1 |

| League specialists (Division 1) | League rank | Trial rank within Division 1 | Gap | League games | League full replays |
|---|---:|---:|---:|---:|---:|
| 428786-marvellous-sambo | 4 | 25.0 | -0.68 | 3 | 1 |
| 404721-khensani-maluleke | 11 | 28.5 | -0.56 | 6 | 0 |
| 410193-vhugala-makhwathane | 7 | 21.5 | -0.47 | 6 | 0 |
| 419222-asisipho-ngaba | 10 | 23.5 | -0.44 | 4 | 1 |
| 428464-madalitso-mnqanqeni | 17 | 27.0 | -0.32 | 6 | 0 |
| 428954-njabulo-ndlozi | 12 | 21.5 | -0.31 | 6 | 0 |
| 408070-collen-mthombeni | 21 | 30.0 | -0.29 | 4 | 1 |

## 3. Repeated snapshots and bot changes

The next table lists select current Division 1 extremes. SHA counts are
distinct *season-snapshot* version hashes, not confirmed per-match hashes.
Repeated identical snapshots can produce apparent consistency without
new independent evidence.

| Student | Eligible Division 1 snapshots | Distinct snapshot hashes | Median rank gap |
|---|---:|---:|---:|
| 421538-tshifhiwa-bvumbi | 4 | 1 | +0.52 |
| 402334-angile-saho | 9 | 2 | +0.42 |
| 419636-jason-chen | 5 | 1 | +0.61 |
| 403754-vhuimo-mudau | 4 | 1 | +0.23 |
| 428786-marvellous-sambo | 9 | 1 | -0.58 |
| 404721-khensani-maluleke | 9 | 1 | -0.55 |
| 410193-vhugala-makhwathane | 6 | 1 | -0.13 |
| 419222-asisipho-ngaba | 5 | 1 | -0.18 |

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
