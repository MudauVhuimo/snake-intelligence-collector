# Snake26: League aggression vs growth-retention hypothesis

Generated UTC: 2026-11-03T15:17:35+00:00

## Data design

Latest official season: 2026-11-03-145900-season. Division 1 group: 32 students.
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
| Mean apples per league match | 32 | 0.400 |
| Mean retained growth ratio | 32 | 0.532 |
| Mean kills per league match | 32 | 0.258 |
| Mean final body length | 32 | 0.628 |
| League first-place frequency | 32 | 0.751 |

Positive means higher performance on that metric tends to align with better
official standing. League win rate and rank are related game outcomes; their
correlation is NOT independent evidence for a specific movement strategy.

## Specific students worth comparing in full replays

| Student | Division 1 rank | League matches | League win % | Mean apples | Mean length | Mean retained growth | Gauntlet final length |
|---|---:|---:|---:|---:|---:|---:|---:|
| 421462-alexander-palmer | 1 | 3 | 66.7 | 34.0 | 115.0 | 0.70 | 215 |
| 409997-utayan-naidoo | 16 | 5 | 60.0 | 31.4 | 88.0 | 0.54 | 255 |
| 427064-khodani-netili | 2 | 4 | 50.0 | 26.0 | 103.8 | 0.76 | 240 |
| 424820-elisha-mundalamo | 3 | 5 | 40.0 | 33.4 | 89.0 | 0.50 | 180 |
| 388828-ngcebo-methula | 4 | 5 | 60.0 | 30.4 | 90.0 | 0.59 | 200 |
| 413538-lelethuthando-nikelo | 5 | 5 | 40.0 | 29.4 | 110.0 | 0.76 | 190 |
| 419342-ayeshan-puckree | 6 | 4 | 50.0 | 30.5 | 140.0 | 0.89 | 180 |
| 428786-marvellous-sambo | 7 | 5 | 20.0 | 29.0 | 60.0 | 0.46 | 20 |
| 404721-khensani-maluleke | 8 | 6 | 50.0 | 33.3 | 100.0 | 0.58 | 30 |
| 419926-mphile-nchabeleng | 9 | 5 | 60.0 | 29.2 | 104.0 | 0.73 | 180 |
| 426895-mpho-ramasakona | 10 | 6 | 33.3 | 26.5 | 43.3 | 0.30 | 225 |

## Why we cannot yet declare a sweet spot

- Only a handful of current-season games per student are currently cataloged.
- Different opponents, starts, seats, maps and versions can change outcomes.
- A mean retained ratio is a reset proxy, not proof of risk-aversion or aggression.
- Final-length evidence cannot tell whether the snake deliberately avoided fights.
- Needed: elite league replays with apple choices, head threats, deaths and escape routes.
- Test per-match and per-bot-version uncertainty before proposing a movement rule.

The same research cycle must continue collecting and analyzing benchmark trials.
No new competition agent code is implemented in this analysis.
