# Snake26: League aggression vs growth-retention hypothesis

Generated UTC: 2026-11-02T23:39:54+00:00

## Data design

Latest official season: 2026-11-02-225901-season. Division 1 group: 32 students.
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
| Mean apples per league match | 32 | 0.235 |
| Mean retained growth ratio | 32 | 0.515 |
| Mean kills per league match | 32 | 0.292 |
| Mean final body length | 32 | 0.633 |
| League first-place frequency | 32 | 0.822 |

Positive means higher performance on that metric tends to align with better
official standing. League win rate and rank are related game outcomes; their
correlation is NOT independent evidence for a specific movement strategy.

## Specific students worth comparing in full replays

| Student | Division 1 rank | League matches | League win % | Mean apples | Mean length | Mean retained growth | Gauntlet final length |
|---|---:|---:|---:|---:|---:|---:|---:|
| 421349-phathutshedzo-mudzanani | 1 | 4 | 75.0 | 32.8 | 91.2 | 0.55 | 240 |
| 409997-utayan-naidoo | 23 | 5 | 20.0 | 32.0 | 39.0 | 0.24 | 255 |
| 424820-elisha-mundalamo | 2 | 6 | 50.0 | 29.7 | 82.5 | 0.58 | 180 |
| 421462-alexander-palmer | 3 | 4 | 50.0 | 33.0 | 141.2 | 0.85 | 215 |
| 427039-sameeha-miabala | 4 | 6 | 50.0 | 32.3 | 66.7 | 0.43 | 200 |
| 388828-ngcebo-methula | 5 | 6 | 66.7 | 30.2 | 97.5 | 0.63 | 200 |
| 413538-lelethuthando-nikelo | 6 | 4 | 25.0 | 33.8 | 88.8 | 0.48 | 190 |
| 403339-david-ndambo | 7 | 6 | 50.0 | 28.2 | 88.3 | 0.63 | 205 |
| 419926-mphile-nchabeleng | 8 | 3 | 33.3 | 29.0 | 100.0 | 0.63 | 180 |
| 423239-zeeshaan-bham | 9 | 6 | 33.3 | 31.7 | 92.5 | 0.51 | 170 |
| 408501-asher-urison | 10 | 5 | 20.0 | 24.8 | 77.0 | 0.62 | 20 |

## Why we cannot yet declare a sweet spot

- Only a handful of current-season games per student are currently cataloged.
- Different opponents, starts, seats, maps and versions can change outcomes.
- A mean retained ratio is a reset proxy, not proof of risk-aversion or aggression.
- Final-length evidence cannot tell whether the snake deliberately avoided fights.
- Needed: elite league replays with apple choices, head threats, deaths and escape routes.
- Test per-match and per-bot-version uncertainty before proposing a movement rule.

The same research cycle must continue collecting and analyzing benchmark trials.
No new competition agent code is implemented in this analysis.
