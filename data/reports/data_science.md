# Snake26 — Data Science Dashboard: Phase I

Generated UTC: 2026-11-01T22:35:22+00:00

## Data coverage and quality

- Cataloged seasons: **24**; match records: **8,994**.
- Replay records marked downloaded in SQLite: **78**.
- Files on disk: **78**; sampled: **78**.
- Unique replay payloads (SHA-256): **37**; duplicate payloads skipped: **41**; unreadable: **0**.
- Latest season: **2026-11-01-205859-season**; published gauntlet_1 trial results: **146**.

> Thousands of catalog records are not thousands of independent replay observations.
> Adjacent turns are correlated. Same bot, version, opponent setup or seed can recur.
> These plots describe outcomes; they do not prove why any bot wins.

## 1. Comparable gauntlet_1 trial outcomes

![Final body lengths](charts/gauntlet_rankings.svg)

A single shared-seed on-arrival match per student is not evidence of consistent performance.
Our recorded trial: **175 final length**, **34 apples**, placement **1**.

## 2. Food acquired versus retained growth

![Apples and retained length](charts/apples_vs_length.svg)

The no-reset relation **L = 5 + 5 × apples** holds exactly in **53/146** reported trials.
**0** result(s) exceed this reference: inspect game mechanics if nonzero.
Below-reference points may reflect growth lost to deaths, but only full replay events establish their cause.

## 3. Observed growth trajectories

![Growth across game turns](charts/gauntlet_growth.svg)

Current-season gauntlet_1 trial replays with trajectories: **4**.
Actual recorded body lengths, sampled every 100 turns; missing curves are not interpolated.

## 4. Deaths by recorded cause

![Observed death events](charts/death_causes.svg)

Raw counts mix opponent groups and survival exposure; they are not comparable risk rates.

## 5. Death-event rate by body length

![Deaths normalized by observed alive turns](charts/death_rates.svg)

| Length range | Student alive turns | Student deaths | Deaths / 1,000 alive turns | Benchmark alive turns | Benchmark deaths |
|---|---:|---:|---:|---:|---:|
| 5-24 | 39,836 | 11 | 0.276 | 60,616 | 281 |
| 25-49 | 44,450 | 21 | 0.472 | 19,551 | 89 |
| 50-99 | 66,015 | 44 | 0.667 | 7,157 | 26 |
| 100-149 | 38,617 | 21 | 0.544 | 608 | 2 |
| 150+ | 16,557 | 2 | 0.121 | 0 | 0 |

Exposure: one alive snake at the start of an observed turn. A death is attributed
to its previous alive state, not the dead/respawned frame's length. A zero-exposure
bin is **unknown**, not safe. Rates are descriptive and not independent probabilities.

## Research roadmap — no competition-snake changes yet

1. Detailed pre-death event studies and matched successful escapes.
2. Food-contest timelines: distance to food at spawn, arrival times, and head pressure.
3. Territory and opponent danger, including tail vacancy and time-dependent occupied space.
4. Code-version cohorts and match-level/bootstrap uncertainty intervals.
5. Separate league battles from fixed on-arrival trials before any causal claims.

We cannot replay private competitors as live executables using fixed recorded moves.
