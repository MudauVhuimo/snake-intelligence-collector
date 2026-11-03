# Snake26: League aggression vs growth-retention hypothesis

Generated UTC: 2026-11-03T04:06:52+00:00

## Data design

Latest official season: 2026-11-03-025900-season. Division 1 group: 32 students.
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
| Mean apples per league match | 32 | 0.497 |
| Mean retained growth ratio | 32 | 0.740 |
| Mean kills per league match | 32 | 0.621 |
| Mean final body length | 32 | 0.800 |
| League first-place frequency | 32 | 0.878 |

Positive means higher performance on that metric tends to align with better
official standing. League win rate and rank are related game outcomes; their
correlation is NOT independent evidence for a specific movement strategy.

## Specific students worth comparing in full replays

| Student | Division 1 rank | League matches | League win % | Mean apples | Mean length | Mean retained growth | Gauntlet final length |
|---|---:|---:|---:|---:|---:|---:|---:|
| 421462-alexander-palmer | 1 | 6 | 83.3 | 34.5 | 145.8 | 0.85 | 215 |
| 409997-utayan-naidoo | 2 | 4 | 50.0 | 33.0 | 47.5 | 0.36 | 255 |
| 424820-elisha-mundalamo | 2 | 4 | 50.0 | 31.5 | 162.5 | 1.00 | 180 |
| 404721-khensani-maluleke | 3 | 5 | 80.0 | 35.4 | 134.0 | 0.72 | 30 |
| 413538-lelethuthando-nikelo | 4 | 5 | 40.0 | 28.2 | 122.0 | 0.85 | 190 |
| 403339-david-ndambo | 5 | 5 | 60.0 | 31.6 | 96.0 | 0.61 | 205 |
| 419342-ayeshan-puckree | 6 | 5 | 60.0 | 29.0 | 96.0 | 0.65 | 180 |
| 427064-khodani-netili | 7 | 5 | 60.0 | 29.4 | 132.0 | 0.84 | 240 |
| 428786-marvellous-sambo | 8 | 4 | 25.0 | 30.5 | 51.2 | 0.35 | 20 |
| 427039-sameeha-miabala | 9 | 4 | 25.0 | 28.8 | 100.0 | 0.70 | 200 |
| 429782-maseeha-seedat | 10 | 5 | 40.0 | 29.4 | 76.0 | 0.54 | 185 |

## Why we cannot yet declare a sweet spot

- Only a handful of current-season games per student are currently cataloged.
- Different opponents, starts, seats, maps and versions can change outcomes.
- A mean retained ratio is a reset proxy, not proof of risk-aversion or aggression.
- Final-length evidence cannot tell whether the snake deliberately avoided fights.
- Needed: elite league replays with apple choices, head threats, deaths and escape routes.
- Test per-match and per-bot-version uncertainty before proposing a movement rule.

The same research cycle must continue collecting and analyzing benchmark trials.
No new competition agent code is implemented in this analysis.
