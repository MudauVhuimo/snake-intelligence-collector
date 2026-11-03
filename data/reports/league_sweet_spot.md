# Snake26: League aggression vs growth-retention hypothesis

Generated UTC: 2026-11-03T12:25:24+00:00

## Data design

Latest official season: 2026-11-03-115900-season. Division 1 group: 32 students.
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
| Mean apples per league match | 32 | 0.336 |
| Mean retained growth ratio | 32 | 0.584 |
| Mean kills per league match | 32 | 0.404 |
| Mean final body length | 32 | 0.677 |
| League first-place frequency | 32 | 0.769 |

Positive means higher performance on that metric tends to align with better
official standing. League win rate and rank are related game outcomes; their
correlation is NOT independent evidence for a specific movement strategy.

## Specific students worth comparing in full replays

| Student | Division 1 rank | League matches | League win % | Mean apples | Mean length | Mean retained growth | Gauntlet final length |
|---|---:|---:|---:|---:|---:|---:|---:|
| 421462-alexander-palmer | 1 | 4 | 75.0 | 31.0 | 160.0 | 1.00 | 215 |
| 409997-utayan-naidoo | 4 | 5 | 40.0 | 36.6 | 119.0 | 0.65 | 255 |
| 413538-lelethuthando-nikelo | 2 | 5 | 60.0 | 29.0 | 150.0 | 1.00 | 190 |
| 424820-elisha-mundalamo | 3 | 5 | 60.0 | 33.2 | 88.0 | 0.53 | 180 |
| 408501-asher-urison | 4 | 6 | 33.3 | 28.2 | 122.5 | 0.85 | 20 |
| 427064-khodani-netili | 5 | 6 | 33.3 | 28.0 | 86.7 | 0.61 | 240 |
| 388828-ngcebo-methula | 6 | 5 | 40.0 | 31.0 | 71.0 | 0.49 | 200 |
| 419342-ayeshan-puckree | 7 | 5 | 40.0 | 27.6 | 76.0 | 0.48 | 180 |
| 423239-zeeshaan-bham | 8 | 5 | 20.0 | 35.4 | 56.0 | 0.32 | 170 |
| 423436-ntobeko-zondi | 9 | 4 | 25.0 | 20.2 | 57.5 | 0.62 | 145 |
| 404721-khensani-maluleke | 10 | 4 | 25.0 | 37.8 | 92.5 | 0.49 | 30 |

## Why we cannot yet declare a sweet spot

- Only a handful of current-season games per student are currently cataloged.
- Different opponents, starts, seats, maps and versions can change outcomes.
- A mean retained ratio is a reset proxy, not proof of risk-aversion or aggression.
- Final-length evidence cannot tell whether the snake deliberately avoided fights.
- Needed: elite league replays with apple choices, head threats, deaths and escape routes.
- Test per-match and per-bot-version uncertainty before proposing a movement rule.

The same research cycle must continue collecting and analyzing benchmark trials.
No new competition agent code is implemented in this analysis.
