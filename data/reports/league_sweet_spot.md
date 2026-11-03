# Snake26: League aggression vs growth-retention hypothesis

Generated UTC: 2026-11-03T19:54:15+00:00

## Data design

Latest official season: 2026-11-03-185906-season. Division 1 group: 32 students.
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
| Mean apples per league match | 32 | 0.838 |
| Mean retained growth ratio | 32 | 0.524 |
| Mean kills per league match | 32 | 0.289 |
| Mean final body length | 32 | 0.698 |
| League first-place frequency | 32 | 0.818 |

Positive means higher performance on that metric tends to align with better
official standing. League win rate and rank are related game outcomes; their
correlation is NOT independent evidence for a specific movement strategy.

## Specific students worth comparing in full replays

| Student | Division 1 rank | League matches | League win % | Mean apples | Mean length | Mean retained growth | Gauntlet final length |
|---|---:|---:|---:|---:|---:|---:|---:|
| 421462-alexander-palmer | 1 | 3 | 100.0 | 36.7 | 95.0 | 0.55 | 215 |
| 409997-utayan-naidoo | 15 | 4 | 50.0 | 29.2 | 126.2 | 0.83 | 255 |
| 427064-khodani-netili | 2 | 6 | 66.7 | 30.2 | 155.8 | 1.00 | 240 |
| 402334-angile-saho | 3 | 6 | 66.7 | 33.2 | 102.5 | 0.60 | 240 |
| 424820-elisha-mundalamo | 4 | 5 | 60.0 | 31.4 | 120.0 | 0.72 | 180 |
| 388828-ngcebo-methula | 5 | 4 | 25.0 | 30.8 | 93.8 | 0.58 | 200 |
| 413538-lelethuthando-nikelo | 6 | 5 | 60.0 | 32.2 | 138.0 | 0.82 | 190 |
| 428786-marvellous-sambo | 7 | 3 | 33.3 | 29.7 | 105.0 | 0.72 | 20 |
| 403339-david-ndambo | 8 | 6 | 33.3 | 32.5 | 109.2 | 0.65 | 205 |
| 408070-collen-mthombeni | 9 | 4 | 25.0 | 32.0 | 65.0 | 0.37 | 165 |
| 423239-zeeshaan-bham | 10 | 6 | 33.3 | 34.8 | 84.2 | 0.50 | 170 |

## Why we cannot yet declare a sweet spot

- Only a handful of current-season games per student are currently cataloged.
- Different opponents, starts, seats, maps and versions can change outcomes.
- A mean retained ratio is a reset proxy, not proof of risk-aversion or aggression.
- Final-length evidence cannot tell whether the snake deliberately avoided fights.
- Needed: elite league replays with apple choices, head threats, deaths and escape routes.
- Test per-match and per-bot-version uncertainty before proposing a movement rule.

The same research cycle must continue collecting and analyzing benchmark trials.
No new competition agent code is implemented in this analysis.
