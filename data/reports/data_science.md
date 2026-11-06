# Snake26 — Data Science Dashboard: Phase I

Generated UTC: 2026-11-06T11:03:52+00:00

## Data coverage and quality

- Cataloged seasons: **153**; match records: **78,048**.
- Replay records marked downloaded in SQLite: **260**.
- Files on disk: **260**; sampled: **250**.
- Unique replay payloads (SHA-256): **181**; duplicate payloads skipped: **69**; unreadable: **0**.
- Latest season: **2026-11-06-102324-season**; published gauntlet_1 trial results: **168**.

> Thousands of catalog records are not thousands of independent replay observations.
> Adjacent turns are correlated. Same bot, version, opponent setup or seed can recur.
> These plots describe outcomes; they do not prove why any bot wins.

## 1. Comparable gauntlet_1 trial outcomes

![Final body lengths](charts/gauntlet_rankings.svg)

A single shared-seed on-arrival match per student is not evidence of consistent performance.
Our recorded trial: **215 final length**, **42 apples**, placement **1**.

## 2. Food acquired versus retained growth

![Apples and retained length](charts/apples_vs_length.svg)

The no-reset relation **L = 5 + 5 × apples** holds exactly in **61/168** reported trials.
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
| 5-24 | 186,800 | 53 | 0.284 | 308,489 | 1,351 |
| 25-49 | 194,050 | 79 | 0.407 | 103,525 | 441 |
| 50-99 | 306,855 | 164 | 0.534 | 48,255 | 137 |
| 100-149 | 191,450 | 112 | 0.585 | 3,522 | 10 |
| 150+ | 86,506 | 36 | 0.416 | 0 | 0 |

Exposure: one alive snake at the start of an observed turn. A death is attributed
to its previous alive state, not the dead/respawned frame's length. A zero-exposure
bin is **unknown**, not safe. Rates are descriptive and not independent probabilities.
These pooled figures DO NOT establish differences between the two game environments.

## 6. Corrected: student death risk separated by mode

![Student death rates by match kind](charts/death_rates_by_mode.svg)

| Length | League alive turns | League deaths | League rate / 1000 | Trial alive turns | Trial deaths | Trial rate / 1000 |
|---|---:|---:|---:|---:|---:|---:|
| 5-24 | 172,577 | 53 | 0.307 | 14,223 | 0 | 0.000 |
| 25-49 | 175,764 | 78 | 0.444 | 18,286 | 1 | 0.055 |
| 50-99 | 271,144 | 161 | 0.594 | 35,711 | 3 | 0.084 |
| 100-149 | 152,560 | 112 | 0.734 | 38,890 | 0 | 0.000 |
| 150+ | 35,698 | 22 | 0.616 | 50,808 | 14 | 0.276 |

Unique full replay payloads sampled: league 102, trials 79.
A missing bar denotes NO exposure, not zero risk. Different opponents,
seeds and bot versions make these observational, non-causal comparisons.

## 7. Research roadmap — no competition-snake changes yet

1. Detailed pre-death event studies and matched successful escapes.
2. Food-contest timelines: distance to food at spawn, arrival times, and head pressure.
3. Territory and opponent danger, including tail vacancy and time-dependent occupied space.
4. Code-version cohorts and match-level/bootstrap uncertainty intervals.
5. Separate league battles from fixed on-arrival trials before any causal claims.

We cannot replay private competitors as live executables using fixed recorded moves.
