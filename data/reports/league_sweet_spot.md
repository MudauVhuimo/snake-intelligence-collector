# Snake26: League aggression vs growth-retention hypothesis

Generated UTC: 2026-11-06T11:02:46+00:00

## Data design

Latest official season: 2026-11-06-102324-season. Division 1 group: 32 students.
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
| Mean apples per league match | 32 | 0.217 |
| Mean retained growth ratio | 32 | 0.532 |
| Mean kills per league match | 32 | 0.176 |
| Mean final body length | 32 | 0.558 |
| League first-place frequency | 32 | 0.803 |

Positive means higher performance on that metric tends to align with better
official standing. League win rate and rank are related game outcomes; their
correlation is NOT independent evidence for a specific movement strategy.

## Specific students worth comparing in full replays

| Student | Division 1 rank | League matches | League win % | Mean apples | Mean length | Mean retained growth | Gauntlet final length |
|---|---:|---:|---:|---:|---:|---:|---:|
| 421462-alexander-palmer | 1 | 4 | 75.0 | 36.0 | 151.2 | 0.80 | 215 |
| 409997-utayan-naidoo | 7 | 6 | 50.0 | 32.2 | 80.8 | 0.47 | 255 |
| 420790-damian-nel | 2 | 6 | 66.7 | 30.8 | 120.0 | 0.77 | 225 |
| 427039-sameeha-miabala | 3 | 5 | 60.0 | 31.6 | 79.0 | 0.50 | 200 |
| 424283-mmathabo-riba | 4 | 5 | 60.0 | 31.0 | 79.0 | 0.51 | 210 |
| 424820-elisha-mundalamo | 5 | 5 | 40.0 | 31.2 | 144.0 | 0.89 | 170 |
| 408501-asher-urison | 6 | 5 | 20.0 | 26.0 | 64.0 | 0.51 | 20 |
| 413538-lelethuthando-nikelo | 7 | 6 | 50.0 | 29.5 | 93.3 | 0.62 | 190 |
| 404721-khensani-maluleke | 8 | 6 | 50.0 | 33.2 | 70.0 | 0.42 | 30 |
| 410193-vhugala-makhwathane | 9 | 6 | 33.3 | 26.7 | 49.2 | 0.43 | 10 |
| 408070-collen-mthombeni | 10 | 6 | 16.7 | 28.2 | 70.8 | 0.49 | 165 |

## Why we cannot yet declare a sweet spot

- Only a handful of current-season games per student are currently cataloged.
- Different opponents, starts, seats, maps and versions can change outcomes.
- A mean retained ratio is a reset proxy, not proof of risk-aversion or aggression.
- Final-length evidence cannot tell whether the snake deliberately avoided fights.
- Needed: elite league replays with apple choices, head threats, deaths and escape routes.
- Test per-match and per-bot-version uncertainty before proposing a movement rule.

The same research cycle must continue collecting and analyzing benchmark trials.
No new competition agent code is implemented in this analysis.
