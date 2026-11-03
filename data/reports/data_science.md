# Snake26 — Data Science Dashboard: Phase I

Generated UTC: 2026-11-03T12:26:20+00:00

## Data coverage and quality

- Cataloged seasons: **120**; match records: **59,229**.
- Replay records marked downloaded in SQLite: **230**.
- Files on disk: **230**; sampled: **230**.
- Unique replay payloads (SHA-256): **159**; duplicate payloads skipped: **71**; unreadable: **0**.
- Latest season: **2026-11-03-115900-season**; published gauntlet_1 trial results: **147**.

> Thousands of catalog records are not thousands of independent replay observations.
> Adjacent turns are correlated. Same bot, version, opponent setup or seed can recur.
> These plots describe outcomes; they do not prove why any bot wins.

## 1. Comparable gauntlet_1 trial outcomes

![Final body lengths](charts/gauntlet_rankings.svg)

A single shared-seed on-arrival match per student is not evidence of consistent performance.
Our recorded trial: **175 final length**, **34 apples**, placement **1**.

## 2. Food acquired versus retained growth

![Apples and retained length](charts/apples_vs_length.svg)

The no-reset relation **L = 5 + 5 × apples** holds exactly in **54/147** reported trials.
**0** result(s) exceed this reference: inspect game mechanics if nonzero.
Below-reference points may reflect growth lost to deaths, but only full replay events establish their cause.

## 3. Observed growth trajectories

![Growth across game turns](charts/gauntlet_growth.svg)

Current-season gauntlet_1 trial replays with trajectories: **1**.
Actual recorded body lengths, sampled every 100 turns; missing curves are not interpolated.

## 4. Deaths by recorded cause (all match modes pooled)

![Observed death events](charts/death_causes.svg)

Raw counts mix opponent groups and survival exposure; they are not comparable risk rates.

## 5. Death-event rate by body length (all match modes pooled)

![Deaths normalized by observed alive turns](charts/death_rates.svg)

| Length range | Student alive turns | Student deaths | Deaths / 1,000 alive turns | Benchmark alive turns | Benchmark deaths |
|---|---:|---:|---:|---:|---:|
| 5-24 | 158,466 | 47 | 0.297 | 292,070 | 1,285 |
| 25-49 | 163,204 | 71 | 0.435 | 95,497 | 418 |
| 50-99 | 257,822 | 142 | 0.551 | 44,298 | 127 |
| 100-149 | 161,725 | 87 | 0.538 | 2,469 | 7 |
| 150+ | 78,831 | 30 | 0.381 | 0 | 0 |

Exposure: one alive snake at the start of an observed turn. A death is attributed
to its previous alive state, not the dead/respawned frame's length. A zero-exposure
bin is **unknown**, not safe. Rates are descriptive and not independent probabilities.
These pooled figures DO NOT establish differences between the two game environments.

## 6. Corrected: student death risk separated by mode

![Student death rates by match kind](charts/death_rates_by_mode.svg)

| Length | League alive turns | League deaths | League rate / 1000 | Trial alive turns | Trial deaths | Trial rate / 1000 |
|---|---:|---:|---:|---:|---:|---:|
| 5-24 | 145,362 | 47 | 0.323 | 13,104 | 0 | 0.000 |
| 25-49 | 146,284 | 70 | 0.479 | 16,920 | 1 | 0.059 |
| 50-99 | 224,306 | 138 | 0.615 | 33,516 | 4 | 0.119 |
| 100-149 | 125,963 | 87 | 0.691 | 35,762 | 0 | 0.000 |
| 150+ | 30,208 | 19 | 0.629 | 48,623 | 11 | 0.226 |

Unique full replay payloads sampled: league 85, trials 74.
A missing bar denotes NO exposure, not zero risk. Different opponents,
seeds and bot versions make these observational, non-causal comparisons.

## 7. Research roadmap — no competition-snake changes yet

1. Detailed pre-death event studies and matched successful escapes.
2. Food-contest timelines: distance to food at spawn, arrival times, and head pressure.
3. Territory and opponent danger, including tail vacancy and time-dependent occupied space.
4. Code-version cohorts and match-level/bootstrap uncertainty intervals.
5. Separate league battles from fixed on-arrival trials before any causal claims.

We cannot replay private competitors as live executables using fixed recorded moves.
