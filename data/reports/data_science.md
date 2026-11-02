# Snake26 — Data Science Dashboard: Phase I

Generated UTC: 2026-11-02T23:40:52+00:00

## Data coverage and quality

- Cataloged seasons: **88**; match records: **41,979**.
- Replay records marked downloaded in SQLite: **200**.
- Files on disk: **200**; sampled: **200**.
- Unique replay payloads (SHA-256): **133**; duplicate payloads skipped: **67**; unreadable: **0**.
- Latest season: **2026-11-02-225901-season**; published gauntlet_1 trial results: **147**.

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
| 5-24 | 133,463 | 40 | 0.300 | 245,681 | 1,112 |
| 25-49 | 135,863 | 60 | 0.442 | 80,239 | 355 |
| 50-99 | 215,270 | 121 | 0.562 | 36,343 | 107 |
| 100-149 | 134,667 | 72 | 0.535 | 1,412 | 4 |
| 150+ | 67,103 | 24 | 0.358 | 0 | 0 |

Exposure: one alive snake at the start of an observed turn. A death is attributed
to its previous alive state, not the dead/respawned frame's length. A zero-exposure
bin is **unknown**, not safe. Rates are descriptive and not independent probabilities.
These pooled figures DO NOT establish differences between the two game environments.

## 6. Corrected: student death risk separated by mode

![Student death rates by match kind](charts/death_rates_by_mode.svg)

| Length | League alive turns | League deaths | League rate / 1000 | Trial alive turns | Trial deaths | Trial rate / 1000 |
|---|---:|---:|---:|---:|---:|---:|
| 5-24 | 122,780 | 40 | 0.326 | 10,683 | 0 | 0.000 |
| 25-49 | 122,071 | 59 | 0.483 | 13,792 | 1 | 0.073 |
| 50-99 | 188,665 | 119 | 0.631 | 26,605 | 2 | 0.075 |
| 100-149 | 105,084 | 72 | 0.685 | 29,583 | 0 | 0.000 |
| 150+ | 23,826 | 14 | 0.588 | 43,277 | 10 | 0.231 |

Unique full replay payloads sampled: league 71, trials 62.
A missing bar denotes NO exposure, not zero risk. Different opponents,
seeds and bot versions make these observational, non-causal comparisons.

## 7. Research roadmap — no competition-snake changes yet

1. Detailed pre-death event studies and matched successful escapes.
2. Food-contest timelines: distance to food at spawn, arrival times, and head pressure.
3. Territory and opponent danger, including tail vacancy and time-dependent occupied space.
4. Code-version cohorts and match-level/bootstrap uncertainty intervals.
5. Separate league battles from fixed on-arrival trials before any causal claims.

We cannot replay private competitors as live executables using fixed recorded moves.
