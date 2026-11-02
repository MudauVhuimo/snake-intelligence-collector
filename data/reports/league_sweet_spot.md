# Snake26: League aggression vs growth-retention hypothesis

Generated UTC: 2026-11-02T06:08:32+00:00

## Data design

Latest official season: 2026-11-02-045859-season. Division 1 group: 32 students.
Included students with at least 3 recorded league matches and usable food/length: 32.

A length-retention proxy is final length divided by 5 plus 5 times ALL apples eaten.
This can detect lost growth from resets but cannot reconstruct exact death timing.
Each student faces a different schedule; raw averages do not control for opponent strength.

## The apparent risk-versus-food tradeoff

![Actual food collection against retained final growth](charts/league_food_retention.svg)

The upper-right area represents students who collect more apples and retain more
resulting length in these match samples. It is not a proven optimum.

## Which league outcomes align with official Division 1 ranking?

| Metric | Bots with matches | Spearman agreement with official league rank |
|---|---:|---:|
| Mean apples per league match | 32 | 0.364 |
| Mean retained growth ratio | 32 | 0.551 |
| Mean kills per league match | 32 | 0.527 |
| Mean final body length | 32 | 0.797 |
| League first-place frequency | 32 | 0.848 |

Positive means higher performance on that metric tends to align with better
official standing. League win rate and rank are related game outcomes; their
correlation is NOT independent evidence for a specific movement strategy.

## Specific students worth comparing in full replays

| Student | Division 1 rank | League matches | League win % | Mean apples | Mean length | Mean retained growth | Gauntlet final length |
|---|---:|---:|---:|---:|---:|---:|---:|
| 421462-alexander-palmer | 1 | 6 | 83.3 | 38.2 | 147.5 | 0.74 | 215 |
| 409997-utayan-naidoo | 12 | 3 | 33.3 | 41.3 | 80.0 | 0.40 | 255 |
| 427064-khodani-netili | 2 | 5 | 60.0 | 30.2 | 126.0 | 0.84 | 240 |
| 427039-sameeha-miabala | 3 | 6 | 66.7 | 26.3 | 114.2 | 0.84 | 200 |
| 424820-elisha-mundalamo | 4 | 4 | 50.0 | 30.0 | 123.8 | 0.77 | 180 |
| 428786-marvellous-sambo | 5 | 5 | 60.0 | 30.8 | 115.0 | 0.71 | 20 |
| 403339-david-ndambo | 6 | 5 | 40.0 | 31.6 | 108.0 | 0.71 | 205 |
| 419926-mphile-nchabeleng | 7 | 5 | 40.0 | 31.6 | 66.0 | 0.44 | 180 |
| 428954-njabulo-ndlozi | 8 | 6 | 33.3 | 27.7 | 59.2 | 0.42 | 145 |
| 388828-ngcebo-methula | 9 | 5 | 60.0 | 36.8 | 81.0 | 0.39 | 200 |
| 402334-angile-saho | 10 | 6 | 33.3 | 29.3 | 99.2 | 0.63 | 235 |

## Why we cannot yet declare a sweet spot

- Only a handful of current-season games per student are currently cataloged.
- Different opponents, starts, seats, maps and versions can change outcomes.
- A mean retained ratio is a reset proxy, not proof of risk-aversion or aggression.
- Final-length evidence cannot tell whether the snake deliberately avoided fights.
- Needed: elite league replays with apple choices, head threats, deaths and escape routes.
- Test per-match and per-bot-version uncertainty before proposing a movement rule.

The same research cycle must continue collecting and analyzing benchmark trials.
No new competition agent code is implemented in this analysis.
