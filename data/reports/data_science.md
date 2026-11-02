# Snake26 — Data Science Dashboard: Phase I

Generated UTC: 2026-11-02T16:16:21+00:00

## Data coverage and quality

- Cataloged seasons: **77**; match records: **36,114**.
- Replay records marked downloaded in SQLite: **190**.
- Files on disk: **190**; sampled: **190**.
- Unique replay payloads (SHA-256): **123**; duplicate payloads skipped: **67**; unreadable: **0**.
- Latest season: **2026-11-02-145901-season**; published gauntlet_1 trial results: **148**.

> Thousands of catalog records are not thousands of independent replay observations.
> Adjacent turns are correlated. Same bot, version, opponent setup or seed can recur.
> These plots describe outcomes; they do not prove why any bot wins.

## 1. Comparable gauntlet_1 trial outcomes

![Final body lengths](charts/gauntlet_rankings.svg)

A single shared-seed on-arrival match per student is not evidence of consistent performance.
Our recorded trial: **175 final length**, **34 apples**, placement **1**.

## 2. Food acquired versus retained growth

![Apples and retained length](charts/apples_vs_length.svg)

The no-reset relation **L = 5 + 5 × apples** holds exactly in **52/148** reported trials.
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
| 5-24 | 123,390 | 38 | 0.308 | 229,635 | 1,024 |
| 25-49 | 125,820 | 56 | 0.445 | 76,567 | 338 |
| 50-99 | 196,259 | 114 | 0.581 | 32,656 | 102 |
| 100-149 | 122,735 | 63 | 0.513 | 1,412 | 4 |
| 150+ | 62,282 | 21 | 0.337 | 0 | 0 |

Exposure: one alive snake at the start of an observed turn. A death is attributed
to its previous alive state, not the dead/respawned frame's length. A zero-exposure
bin is **unknown**, not safe. Rates are descriptive and not independent probabilities.
These pooled figures DO NOT establish differences between the two game environments.

## 6. Corrected: student death risk separated by mode

![Student death rates by match kind](charts/death_rates_by_mode.svg)

| Length | League alive turns | League deaths | League rate / 1000 | Trial alive turns | Trial deaths | Trial rate / 1000 |
|---|---:|---:|---:|---:|---:|---:|
| 5-24 | 113,321 | 38 | 0.335 | 10,069 | 0 | 0.000 |
| 25-49 | 113,097 | 55 | 0.486 | 12,723 | 1 | 0.079 |
| 50-99 | 171,384 | 112 | 0.654 | 24,875 | 2 | 0.080 |
| 100-149 | 95,082 | 63 | 0.663 | 27,653 | 0 | 0.000 |
| 150+ | 21,662 | 12 | 0.554 | 40,620 | 9 | 0.222 |

Unique full replay payloads sampled: league 65, trials 58.
A missing bar denotes NO exposure, not zero risk. Different opponents,
seeds and bot versions make these observational, non-causal comparisons.

## 7. Research roadmap — no competition-snake changes yet

1. Detailed pre-death event studies and matched successful escapes.
2. Food-contest timelines: distance to food at spawn, arrival times, and head pressure.
3. Territory and opponent danger, including tail vacancy and time-dependent occupied space.
4. Code-version cohorts and match-level/bootstrap uncertainty intervals.
5. Separate league battles from fixed on-arrival trials before any causal claims.

We cannot replay private competitors as live executables using fixed recorded moves.
