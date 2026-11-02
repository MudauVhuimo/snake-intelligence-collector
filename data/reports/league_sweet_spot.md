# Snake26: League aggression vs growth-retention hypothesis

Generated UTC: 2026-11-02T00:42:14+00:00

## Data design

Latest official season: 2026-11-01-235859-season. Division 1 group: 32 students.
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
| Mean apples per league match | 32 | 0.298 |
| Mean retained growth ratio | 32 | 0.583 |
| Mean kills per league match | 32 | 0.419 |
| Mean final body length | 32 | 0.667 |
| League first-place frequency | 32 | 0.808 |

Positive means higher performance on that metric tends to align with better
official standing. League win rate and rank are related game outcomes; their
correlation is NOT independent evidence for a specific movement strategy.

## Specific students worth comparing in full replays

| Student | Division 1 rank | League matches | League win % | Mean apples | Mean length | Mean retained growth | Gauntlet final length |
|---|---:|---:|---:|---:|---:|---:|---:|
| 421462-alexander-palmer | 1 | 6 | 66.7 | 36.8 | 143.3 | 0.77 | 215 |
| 409997-utayan-naidoo | 29 | 5 | 0.0 | 32.0 | 20.0 | 0.11 | 255 |
| 403339-david-ndambo | 2 | 5 | 60.0 | 31.6 | 51.0 | 0.30 | 205 |
| 427064-khodani-netili | 3 | 4 | 50.0 | 27.5 | 127.5 | 0.89 | 240 |
| 426895-mpho-ramasakona | 4 | 4 | 50.0 | 28.8 | 116.2 | 0.76 | 225 |
| 423436-ntobeko-zondi | 5 | 4 | 50.0 | 26.5 | 106.2 | 0.78 | 185 |
| 388828-ngcebo-methula | 6 | 4 | 25.0 | 27.2 | 120.0 | 0.82 | 200 |
| 424820-elisha-mundalamo | 7 | 5 | 40.0 | 29.2 | 111.0 | 0.71 | 180 |
| 428786-marvellous-sambo | 8 | 5 | 40.0 | 31.2 | 25.0 | 0.17 | 20 |
| 388060-tshepang-tshabalala | 9 | 4 | 50.0 | 29.8 | 115.0 | 0.81 | 210 |
| 427039-sameeha-miabala | 10 | 5 | 60.0 | 31.4 | 110.0 | 0.70 | 200 |

## Why we cannot yet declare a sweet spot

- Only a handful of current-season games per student are currently cataloged.
- Different opponents, starts, seats, maps and versions can change outcomes.
- A mean retained ratio is a reset proxy, not proof of risk-aversion or aggression.
- Final-length evidence cannot tell whether the snake deliberately avoided fights.
- Needed: elite league replays with apple choices, head threats, deaths and escape routes.
- Test per-match and per-bot-version uncertainty before proposing a movement rule.

The same research cycle must continue collecting and analyzing benchmark trials.
No new competition agent code is implemented in this analysis.
