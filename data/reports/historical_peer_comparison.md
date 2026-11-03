# Snake26 historical league outcomes versus fixed trials

Generated UTC: 2026-11-03T15:24:21+00:00

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

- Season/division cohorts with at least 10 eligible students: **233**.
- Distinct seasons represented: **123**.
- Division 1 snapshots: **123**.
- Eligible student/season/division records: **6415**.
- Excluded student-seasons with fewer than 3 peer league games: **86**.
- Excluded student-seasons with conflicting match divisions: **0**.
- Excluded student-seasons without all three trial suites: **26**.

## Student-vs-student placement correlation with benchmark growth

![Historical peer placement and trial growth](charts/historical_peer_vs_trial.svg)

A positive Spearman correlation means a student with better average
league placement (smaller numerical place) tends to grow longer in trials
(larger numerical length) *within the same season and match division*.
It does NOT establish that benchmark growth causes league success.

| Indexed season | Division 1 students | Spearman rho | Avg peer matches/student | Official ranks saved? |
|---|---:|---:|---:|---:|
| 2026-11-03-145900-season | 32 | +0.350 | 5 | 32/32 |
| 2026-11-03-135900-season | 32 | +0.171 | 5.1 | 0/32 |
| 2026-11-03-115900-season | 32 | +0.251 | 4.9 | 32/32 |
| 2026-11-03-105900-season | 32 | +0.187 | 4.5 | 0/32 |
| 2026-11-03-055900-season | 32 | +0.321 | 5 | 32/32 |
| 2026-11-03-045900-season | 31 | -0.093 | 4.6 | 0/31 |
| 2026-11-03-025900-season | 32 | +0.231 | 4.6 | 32/32 |
| 2026-11-03-015900-season | 32 | +0.094 | 4.8 | 0/32 |
| 2026-11-02-225901-season | 32 | +0.546 | 5 | 32/32 |
| 2026-11-02-215901-season | 32 | +0.009 | 4.6 | 0/32 |
| 2026-11-02-145901-season | 32 | +0.182 | 4.9 | 32/32 |
| 2026-11-02-135859-season | 32 | +0.086 | 5 | 0/32 |
| 2026-11-02-045859-season | 32 | +0.381 | 5.4 | 32/32 |
| 2026-11-02-035859-season | 31 | +0.194 | 5.0 | 0/31 |
| 2026-11-01-235859-season | 32 | +0.328 | 4.6 | 32/32 |
| 2026-11-01-225859-season | 32 | +0.498 | 5.1 | 32/32 |
| 2026-11-01-215859-season | 32 | +0.062 | 5.6 | 32/32 |
| 2026-11-01-205859-season | 32 | +0.113 | 4.5 | 32/32 |
| 2026-11-01-195859-season | 32 | +0.377 | 4.5 | 0/32 |
| 2026-10-29-125858-season | 32 | +0.496 | 5 | 0/32 |
| 2026-10-29-105900-season | 32 | +0.382 | 4.9 | 0/32 |
| 2026-10-29-055859-season | 29 | +0.278 | 4.4 | 0/29 |
| 2026-10-29-035858-season | 32 | +0.235 | 4.5 | 0/32 |
| 2026-10-29-005901-season | 32 | +0.287 | 4.9 | 0/32 |

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
