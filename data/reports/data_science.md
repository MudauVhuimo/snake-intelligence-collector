# Snake26 — Data Science Dashboard: Phase I

Generated UTC: 2026-11-01T23:45:46+00:00

## Data coverage and quality

- Cataloged seasons: **47**; match records: **20,406**.
- Replay records marked downloaded in SQLite: **150**.
- Files on disk: **150**; sampled: **150**.
- Unique replay payloads (SHA-256): **87**; duplicate payloads skipped: **63**; unreadable: **0**.
- Latest season: **2026-11-01-225859-season**; published gauntlet_1 trial results: **146**.

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

## 4. Deaths by recorded cause (all match modes pooled)

![Observed death events](charts/death_causes.svg)

Raw counts mix opponent groups and survival exposure; they are not comparable risk rates.

## 5. Death-event rate by body length (all match modes pooled)

![Deaths normalized by observed alive turns](charts/death_rates.svg)

| Length range | Student alive turns | Student deaths | Deaths / 1,000 alive turns | Benchmark alive turns | Benchmark deaths |
|---|---:|---:|---:|---:|---:|
| 5-24 | 85,812 | 29 | 0.338 | 165,206 | 733 |
| 25-49 | 89,156 | 39 | 0.437 | 55,814 | 241 |
| 50-99 | 139,573 | 77 | 0.552 | 24,119 | 74 |
| 100-149 | 84,246 | 43 | 0.510 | 1,343 | 4 |
| 150+ | 42,152 | 15 | 0.356 | 0 | 0 |

Exposure: one alive snake at the start of an observed turn. A death is attributed
to its previous alive state, not the dead/respawned frame's length. A zero-exposure
bin is **unknown**, not safe. Rates are descriptive and not independent probabilities.
These pooled figures DO NOT establish differences between the two game environments.

## 6. Corrected: student death risk separated by mode

![Student death rates by match kind](charts/death_rates_by_mode.svg)

| Length | League alive turns | League deaths | League rate / 1000 | Trial alive turns | Trial deaths | Trial rate / 1000 |
|---|---:|---:|---:|---:|---:|---:|
| 5-24 | 78,372 | 29 | 0.370 | 7,440 | 0 | 0.000 |
| 25-49 | 79,633 | 38 | 0.477 | 9,523 | 1 | 0.105 |
| 50-99 | 121,854 | 75 | 0.615 | 17,719 | 2 | 0.113 |
| 100-149 | 64,184 | 43 | 0.670 | 20,062 | 0 | 0.000 |
| 150+ | 12,946 | 8 | 0.618 | 29,206 | 7 | 0.240 |

Unique full replay payloads sampled: league 45, trials 42.
A missing bar denotes NO exposure, not zero risk. Different opponents,
seeds and bot versions make these observational, non-causal comparisons.

## 7. Research roadmap — no competition-snake changes yet

1. Detailed pre-death event studies and matched successful escapes.
2. Food-contest timelines: distance to food at spawn, arrival times, and head pressure.
3. Territory and opponent danger, including tail vacancy and time-dependent occupied space.
4. Code-version cohorts and match-level/bootstrap uncertainty intervals.
5. Separate league battles from fixed on-arrival trials before any causal claims.

We cannot replay private competitors as live executables using fixed recorded moves.
