# Snake26: real league apple contests

Generated UTC: 2026-11-06T11:05:01+00:00

## Opportunity definition

One observation is a newly visible apple with two living STUDENT heads within
10 toroidal Manhattan steps, separated by at most 2 steps in distance to that apple.
First-frame food is flagged in the CSV. Replays with only one student are excluded.
Distance is NOT a safe-path estimate; this is selected, observational replay data.

Unique replay payloads: **102**; exact duplicates: **59**.
Close-peer opportunities: **1017**.
Captures verified within 40 turns: **963/1017 (94.7%)**.
Unverified disappearances: **0**; horizon/end censored: **54**; frame gaps: **0**.

## Actual capturer among verified outcomes

| Position at first visibility | Captures | Share of confirmed |
|---|---:|---:|
| Strictly closest | 565 | 58.7% |
| Strictly second-closest | 117 | 12.1% |
| Tied first (ID-order tie break) | 103 | 10.7% |
| Tied second (ID-order tie break) | 106 | 11.0% |
| Other participant | 72 | 7.5% |

These shares are conditional on confirmed captures, NOT an intervention or
the chance that chasing an apple will win it.

## Actual first movements, including missing/dead observations

| Starting distance rank | Closer | Sideways | Farther | Died at +1 | Unobserved normal step |
|---|---:|---:|---:|---:|---:|
| nearest | 744 | 0 | 273 | 0 | 0 |
| second | 610 | 0 | 406 | 1 | 0 |
- Nearest first moves into possible opponent head cones: **21/1017 (2.1%)**; equal/longer cones: **0/1017 (0.0%)**.
- Second first moves into possible opponent head cones: **35/1016 (3.4%)**; equal/longer cones: **2/1016 (0.2%)**.

A geometric cone includes collision-impossible opponent moves; it is NOT
a calibrated likelihood. Dead/unobserved first moves never become assumed safe
movements. Movement observations are survivor-selected.

## Palmer: distinct reference subset

Eligible apple appearances involving Palmer: **181**.
Palmer captured **96**; another participant captured **80**; censored/unverified **5**.
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
