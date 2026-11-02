# Snake26: League aggression vs growth-retention hypothesis

Generated UTC: 2026-11-02T16:15:29+00:00

## Data design

Latest official season: 2026-11-02-145901-season. Division 1 group: 32 students.
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
| Mean apples per league match | 32 | 0.365 |
| Mean retained growth ratio | 32 | 0.369 |
| Mean kills per league match | 32 | 0.190 |
| Mean final body length | 32 | 0.462 |
| League first-place frequency | 32 | 0.525 |

Positive means higher performance on that metric tends to align with better
official standing. League win rate and rank are related game outcomes; their
correlation is NOT independent evidence for a specific movement strategy.

## Specific students worth comparing in full replays

| Student | Division 1 rank | League matches | League win % | Mean apples | Mean length | Mean retained growth | Gauntlet final length |
|---|---:|---:|---:|---:|---:|---:|---:|
| 424820-elisha-mundalamo | 1 | 5 | 80.0 | 33.0 | 170.0 | 1.00 | 180 |
| 409997-utayan-naidoo | 8 | 4 | 50.0 | 31.5 | 40.0 | 0.33 | 255 |
| 402334-angile-saho | 2 | 4 | 50.0 | 35.2 | 106.2 | 0.60 | 235 |
| 421462-alexander-palmer | 3 | 4 | 50.0 | 35.2 | 118.8 | 0.66 | 215 |
| 427064-khodani-netili | 4 | 5 | 40.0 | 29.4 | 107.0 | 0.70 | 240 |
| 428954-njabulo-ndlozi | 5 | 6 | 16.7 | 36.0 | 32.5 | 0.16 | 145 |
| 404721-khensani-maluleke | 6 | 6 | 50.0 | 30.3 | 43.3 | 0.27 | 30 |
| 427039-sameeha-miabala | 7 | 5 | 20.0 | 23.2 | 103.0 | 0.88 | 200 |
| 408070-collen-mthombeni | 9 | 4 | 25.0 | 24.2 | 47.5 | 0.37 | 165 |
| 421349-phathutshedzo-mudzanani | 10 | 6 | 16.7 | 31.2 | 99.2 | 0.61 | 240 |

## Why we cannot yet declare a sweet spot

- Only a handful of current-season games per student are currently cataloged.
- Different opponents, starts, seats, maps and versions can change outcomes.
- A mean retained ratio is a reset proxy, not proof of risk-aversion or aggression.
- Final-length evidence cannot tell whether the snake deliberately avoided fights.
- Needed: elite league replays with apple choices, head threats, deaths and escape routes.
- Test per-match and per-bot-version uncertainty before proposing a movement rule.

The same research cycle must continue collecting and analyzing benchmark trials.
No new competition agent code is implemented in this analysis.
