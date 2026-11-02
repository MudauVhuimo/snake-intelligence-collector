# Snake26 historical league outcomes versus fixed trials

Generated UTC: 2026-11-02T07:53:49+00:00

## Why this analysis exists

We have many historical league match CATALOGS but relatively few saved
official standings for old seasons. To use those actual student-vs-student
games, we compute each student's average recorded league **placement**
among at least three peer matches in one season and one match division.
We compare it to that student's mean final length in all three on-arrival
trial suites. Division is taken from the recorded league MATCH, not inferred
from a missing official standings table.

This is **not official rank** and must never be reported as official rank.
Different league schedules and opponents affect placement. Many hourly
snapshots reuse bots, seeds and exact match results, so the history is
NOT a series of independent replications.

## Coverage

- Season/division cohorts with at least 10 eligible students: **97**.
- Distinct seasons represented: **58**.
- Division 1 snapshots: **58**.
- Eligible student/season/division records: **2475**.
- Excluded student-seasons with fewer than 3 peer league games: **19**.
- Excluded student-seasons with conflicting match divisions: **0**.
- Excluded student-seasons without all three trial suites: **21**.

## Student-vs-student placement correlation with benchmark growth

![Historical peer placement and trial growth](charts/historical_peer_vs_trial.svg)

A positive Spearman correlation means a student with better average
league placement (smaller numerical place) tends to grow longer in trials
(larger numerical length) *within the same season and match division*.
It does NOT establish that benchmark growth causes league success.

| Indexed season | Division 1 students | Spearman rho | Avg peer matches/student | Official ranks saved? |
|---|---:|---:|---:|---:|
| 2026-11-02-045859-season | 32 | +0.381 | 5.4 | 32/32 |
| 2026-11-02-035859-season | 31 | +0.194 | 5.0 | 0/31 |
| 2026-11-01-235859-season | 32 | +0.328 | 4.6 | 32/32 |
| 2026-11-01-225859-season | 32 | +0.498 | 5.1 | 32/32 |
| 2026-11-01-215859-season | 32 | +0.062 | 5.6 | 32/32 |
| 2026-11-01-205859-season | 32 | +0.113 | 4.5 | 32/32 |
| 2026-11-01-195859-season | 32 | +0.377 | 4.5 | 0/32 |
| 2026-10-28-115857-season | 32 | +0.231 | 5 | 0/32 |
| 2026-10-28-075857-season | 32 | +0.281 | 4.6 | 0/32 |
| 2026-10-28-065857-season | 32 | -0.050 | 4.5 | 0/32 |
| 2026-10-28-055857-season | 32 | +0.263 | 4.4 | 0/32 |
| 2026-10-23-185857-season | 32 | +0.509 | 4.5 | 0/32 |
| 2026-10-23-155859-season | 32 | +0.446 | 4.6 | 0/32 |
| 2026-10-23-145906-season | 32 | +0.400 | 4.9 | 0/32 |
| 2026-10-19-015858-season | 32 | +0.549 | 4.8 | 0/32 |
| 2026-10-19-005858-season | 32 | +0.447 | 4.9 | 0/32 |
| 2026-10-18-235859-season | 31 | +0.442 | 4.8 | 0/31 |
| 2026-10-16-095859-season | 26 | +0.525 | 6 | 0/26 |
| 2026-10-16-085900-season | 25 | +0.573 | 5.8 | 0/25 |
| 2026-10-16-075858-season | 24 | +0.505 | 6 | 0/24 |
| 2026-10-16-065857-season | 24 | +0.509 | 6 | 0/24 |
| 2026-10-16-055857-season | 24 | +0.463 | 6 | 0/24 |
| 2026-10-16-045857-season | 24 | +0.428 | 6 | 0/24 |
| 2026-10-16-035857-season | 24 | +0.594 | 6 | 0/24 |

## Interpretation and responsible next actions

If league/trial ranking gaps persist across historical snapshots with
the same recorded SHA, they are *hypotheses* about robustness, not proof
of unchanged executable code. Select mismatched performers for full replay
case studies; pair growth, actual deaths, threat exposure and length
retention, controlling for opponents and game phase.

## Downloadable derived inputs

- [Season-by-division peer-game correlations](../derived/historical_peer_trial_correlations.csv)
- [Student-level source rows](../derived/historical_peer_trial_students.csv)
No competition snake has been altered.
