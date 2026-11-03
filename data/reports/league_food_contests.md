# Snake26: real league apple contests

Generated UTC: 2026-11-03T19:56:05+00:00

## Opportunity definition

One observation is a newly visible apple with two living STUDENT heads within
10 toroidal Manhattan steps, separated by at most 2 steps in distance to that apple.
First-frame food is flagged in the CSV. Replays with only one student are excluded.
Distance is NOT a safe-path estimate; this is selected, observational replay data.

Unique replay payloads: **97**; exact duplicates: **58**.
Close-peer opportunities: **968**.
Captures verified within 40 turns: **917/968 (94.7%)**.
Unverified disappearances: **0**; horizon/end censored: **51**; frame gaps: **0**.

## Actual capturer among verified outcomes

| Position at first visibility | Captures | Share of confirmed |
|---|---:|---:|
| Strictly closest | 532 | 58.0% |
| Strictly second-closest | 114 | 12.4% |
| Tied first (ID-order tie break) | 98 | 10.7% |
| Tied second (ID-order tie break) | 103 | 11.2% |
| Other participant | 70 | 7.6% |

These shares are conditional on confirmed captures, NOT an intervention or
the chance that chasing an apple will win it.

## Actual first movements, including missing/dead observations

| Starting distance rank | Closer | Sideways | Farther | Died at +1 | Unobserved normal step |
|---|---:|---:|---:|---:|---:|
| nearest | 703 | 0 | 265 | 0 | 0 |
| second | 579 | 0 | 388 | 1 | 0 |
- Nearest first moves into possible opponent head cones: **21/968 (2.2%)**; equal/longer cones: **0/968 (0.0%)**.
- Second first moves into possible opponent head cones: **34/967 (3.5%)**; equal/longer cones: **2/967 (0.2%)**.

A geometric cone includes collision-impossible opponent moves; it is NOT
a calibrated likelihood. Dead/unobserved first moves never become assumed safe
movements. Movement observations are survivor-selected.

## Palmer: distinct reference subset

Eligible apple appearances involving Palmer: **157**.
Palmer captured **81**; another participant captured **71**; censored/unverified **5**.
These are not opponent-matched skill ratings.

## Research limitations

- Different games and bot versions are not independent or necessarily comparable.
- Repeated apple episodes in one replay require match-cluster uncertainty analysis.
- A closer first move does not establish intent; apple position and bodies evolve.
- Censored and unverified apples are not counted as losses.
- To advance FOOD-04, test body-aware arrival predictors on whole-game holdouts
  and finally in controlled ablations against diverse peers (including Palmer).

[Episode-level CSV](../derived/league_food_contests.csv).

**No Java competitor agent is changed.**
