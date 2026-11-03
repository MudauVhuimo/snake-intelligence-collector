# Snake26 — Data Science Dashboard: Phase I

Generated UTC: 2026-11-03T19:55:07+00:00

## Data coverage and quality

- Cataloged seasons: **142**; match records: **71,298**.
- Replay records marked downloaded in SQLite: **250**.
- Files on disk: **250**; sampled: **250**.
- Unique replay payloads (SHA-256): **179**; duplicate payloads skipped: **71**; unreadable: **0**.
- Latest season: **2026-11-03-185906-season**; published gauntlet_1 trial results: **152**.

> Thousands of catalog records are not thousands of independent replay observations.
> Adjacent turns are correlated. Same bot, version, opponent setup or seed can recur.
> These plots describe outcomes; they do not prove why any bot wins.

## 1. Comparable gauntlet_1 trial outcomes

![Final body lengths](charts/gauntlet_rankings.svg)

A single shared-seed on-arrival match per student is not evidence of consistent performance.
Our recorded trial: **175 final length**, **34 apples**, placement **1**.

## 2. Food acquired versus retained growth

![Apples and retained length](charts/apples_vs_length.svg)

The no-reset relation **L = 5 + 5 × apples** holds exactly in **56/152** reported trials.
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
| 5-24 | 179,665 | 52 | 0.289 | 321,307 | 1,399 |
| 25-49 | 187,625 | 78 | 0.416 | 107,263 | 465 |
| 50-99 | 294,123 | 161 | 0.547 | 49,302 | 140 |
| 100-149 | 184,306 | 103 | 0.559 | 3,522 | 10 |
| 150+ | 86,017 | 38 | 0.442 | 0 | 0 |

Exposure: one alive snake at the start of an observed turn. A death is attributed
to its previous alive state, not the dead/respawned frame's length. A zero-exposure
bin is **unknown**, not safe. Rates are descriptive and not independent probabilities.
These pooled figures DO NOT establish differences between the two game environments.

## 6. Corrected: student death risk separated by mode

![Student death rates by match kind](charts/death_rates_by_mode.svg)

| Length | League alive turns | League deaths | League rate / 1000 | Trial alive turns | Trial deaths | Trial rate / 1000 |
|---|---:|---:|---:|---:|---:|---:|
| 5-24 | 164,553 | 52 | 0.316 | 15,112 | 0 | 0.000 |
| 25-49 | 168,703 | 77 | 0.456 | 18,922 | 1 | 0.053 |
| 50-99 | 256,839 | 157 | 0.611 | 37,284 | 4 | 0.107 |
| 100-149 | 144,306 | 103 | 0.714 | 40,000 | 0 | 0.000 |
| 150+ | 33,437 | 21 | 0.628 | 52,580 | 17 | 0.323 |

Unique full replay payloads sampled: league 97, trials 82.
A missing bar denotes NO exposure, not zero risk. Different opponents,
seeds and bot versions make these observational, non-causal comparisons.

## 7. Research roadmap — no competition-snake changes yet

1. Detailed pre-death event studies and matched successful escapes.
2. Food-contest timelines: distance to food at spawn, arrival times, and head pressure.
3. Territory and opponent danger, including tail vacancy and time-dependent occupied space.
4. Code-version cohorts and match-level/bootstrap uncertainty intervals.
5. Separate league battles from fixed on-arrival trials before any causal claims.

We cannot replay private competitors as live executables using fixed recorded moves.
