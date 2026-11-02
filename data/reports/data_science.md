# Snake26 — Data Science Dashboard: Phase I

Generated UTC: 2026-11-02T06:14:38+00:00

## Data coverage and quality

- Cataloged seasons: **66**; match records: **30,246**.
- Replay records marked downloaded in SQLite: **180**.
- Files on disk: **180**; sampled: **180**.
- Unique replay payloads (SHA-256): **113**; duplicate payloads skipped: **67**; unreadable: **0**.
- Latest season: **2026-11-02-045859-season**; published gauntlet_1 trial results: **146**.

> Thousands of catalog records are not thousands of independent replay observations.
> Adjacent turns are correlated. Same bot, version, opponent setup or seed can recur.
> These plots describe outcomes; they do not prove why any bot wins.

## 1. Comparable gauntlet_1 trial outcomes

![Final body lengths](charts/gauntlet_rankings.svg)

A single shared-seed on-arrival match per student is not evidence of consistent performance.
Our recorded trial: **175 final length**, **34 apples**, placement **1**.

## 2. Food acquired versus retained growth

![Apples and retained length](charts/apples_vs_length.svg)

The no-reset relation **L = 5 + 5 × apples** holds exactly in **52/146** reported trials.
**0** result(s) exceed this reference: inspect game mechanics if nonzero.
Below-reference points may reflect growth lost to deaths, but only full replay events establish their cause.

## 3. Observed growth trajectories

![Growth across game turns](charts/gauntlet_growth.svg)

Current-season gauntlet_1 trial replays with trajectories: **2**.
Actual recorded body lengths, sampled every 100 turns; missing curves are not interpolated.

## 4. Deaths by recorded cause (all match modes pooled)

![Observed death events](charts/death_causes.svg)

Raw counts mix opponent groups and survival exposure; they are not comparable risk rates.

## 5. Death-event rate by body length (all match modes pooled)

![Deaths normalized by observed alive turns](charts/death_rates.svg)

| Length range | Student alive turns | Student deaths | Deaths / 1,000 alive turns | Benchmark alive turns | Benchmark deaths |
|---|---:|---:|---:|---:|---:|
| 5-24 | 112,577 | 35 | 0.311 | 214,158 | 955 |
| 25-49 | 115,027 | 52 | 0.452 | 71,148 | 317 |
| 50-99 | 179,675 | 99 | 0.551 | 30,079 | 94 |
| 100-149 | 109,711 | 56 | 0.510 | 1,412 | 4 |
| 150+ | 57,664 | 20 | 0.347 | 0 | 0 |

Exposure: one alive snake at the start of an observed turn. A death is attributed
to its previous alive state, not the dead/respawned frame's length. A zero-exposure
bin is **unknown**, not safe. Rates are descriptive and not independent probabilities.
These pooled figures DO NOT establish differences between the two game environments.

## 6. Corrected: student death risk separated by mode

![Student death rates by match kind](charts/death_rates_by_mode.svg)

| Length | League alive turns | League deaths | League rate / 1000 | Trial alive turns | Trial deaths | Trial rate / 1000 |
|---|---:|---:|---:|---:|---:|---:|
| 5-24 | 103,002 | 35 | 0.340 | 9,575 | 0 | 0.000 |
| 25-49 | 103,110 | 51 | 0.495 | 11,917 | 1 | 0.084 |
| 50-99 | 156,680 | 97 | 0.619 | 22,995 | 2 | 0.087 |
| 100-149 | 84,582 | 56 | 0.662 | 25,129 | 0 | 0.000 |
| 150+ | 19,340 | 11 | 0.569 | 38,324 | 9 | 0.235 |

Unique full replay payloads sampled: league 59, trials 54.
A missing bar denotes NO exposure, not zero risk. Different opponents,
seeds and bot versions make these observational, non-causal comparisons.

## 7. Research roadmap — no competition-snake changes yet

1. Detailed pre-death event studies and matched successful escapes.
2. Food-contest timelines: distance to food at spawn, arrival times, and head pressure.
3. Territory and opponent danger, including tail vacancy and time-dependent occupied space.
4. Code-version cohorts and match-level/bootstrap uncertainty intervals.
5. Separate league battles from fixed on-arrival trials before any causal claims.

We cannot replay private competitors as live executables using fixed recorded moves.
