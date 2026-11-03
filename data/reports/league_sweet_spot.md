# Snake26: League aggression vs growth-retention hypothesis

Generated UTC: 2026-11-03T06:57:20+00:00

## Data design

Latest official season: 2026-11-03-055900-season. Division 1 group: 32 students.
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
| Mean apples per league match | 32 | 0.509 |
| Mean retained growth ratio | 32 | 0.502 |
| Mean kills per league match | 32 | 0.413 |
| Mean final body length | 32 | 0.648 |
| League first-place frequency | 32 | 0.759 |

Positive means higher performance on that metric tends to align with better
official standing. League win rate and rank are related game outcomes; their
correlation is NOT independent evidence for a specific movement strategy.

## Specific students worth comparing in full replays

| Student | Division 1 rank | League matches | League win % | Mean apples | Mean length | Mean retained growth | Gauntlet final length |
|---|---:|---:|---:|---:|---:|---:|---:|
| 427064-khodani-netili | 1 | 5 | 60.0 | 32.2 | 111.0 | 0.67 | 240 |
| 409997-utayan-naidoo | 30 | 4 | 25.0 | 28.5 | 66.2 | 0.43 | 255 |
| 424820-elisha-mundalamo | 2 | 4 | 50.0 | 34.2 | 158.8 | 0.91 | 180 |
| 403339-david-ndambo | 3 | 5 | 60.0 | 30.2 | 140.0 | 0.89 | 205 |
| 428786-marvellous-sambo | 4 | 3 | 33.3 | 32.0 | 60.0 | 0.37 | 20 |
| 421462-alexander-palmer | 5 | 5 | 60.0 | 30.2 | 156.0 | 1.00 | 215 |
| 388828-ngcebo-methula | 6 | 5 | 40.0 | 27.4 | 119.0 | 0.86 | 200 |
| 410193-vhugala-makhwathane | 7 | 6 | 33.3 | 25.0 | 106.7 | 0.84 | 175 |
| 413538-lelethuthando-nikelo | 8 | 5 | 40.0 | 28.2 | 106.0 | 0.69 | 190 |
| 421349-phathutshedzo-mudzanani | 9 | 6 | 16.7 | 32.0 | 78.3 | 0.50 | 240 |
| 419222-asisipho-ngaba | 10 | 4 | 25.0 | 29.5 | 72.5 | 0.39 | 180 |

## Why we cannot yet declare a sweet spot

- Only a handful of current-season games per student are currently cataloged.
- Different opponents, starts, seats, maps and versions can change outcomes.
- A mean retained ratio is a reset proxy, not proof of risk-aversion or aggression.
- Final-length evidence cannot tell whether the snake deliberately avoided fights.
- Needed: elite league replays with apple choices, head threats, deaths and escape routes.
- Test per-match and per-bot-version uncertainty before proposing a movement rule.

The same research cycle must continue collecting and analyzing benchmark trials.
No new competition agent code is implemented in this analysis.
