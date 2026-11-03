# Snake26: real league apple contests

Generated UTC: 2026-11-03T15:20:01+00:00

## Opportunity definition

One observation is a newly visible apple with two living STUDENT heads within
10 toroidal Manhattan steps, separated by at most 2 steps in distance to that apple.
First-frame food is flagged in the CSV. Replays with only one student are excluded.
Distance is NOT a safe-path estimate; this is selected, observational replay data.

Unique replay payloads: **91**; exact duplicates: **58**.
Close-peer opportunities: **912**.
Captures verified within 40 turns: **863/912 (94.6%)**.
Unverified disappearances: **0**; horizon/end censored: **49**; frame gaps: **0**.

## Actual capturer among verified outcomes

| Position at first visibility | Captures | Share of confirmed |
|---|---:|---:|
| Strictly closest | 504 | 58.4% |
| Strictly second-closest | 110 | 12.7% |
| Tied first (ID-order tie break) | 92 | 10.7% |
| Tied second (ID-order tie break) | 94 | 10.9% |
| Other participant | 63 | 7.3% |

These shares are conditional on confirmed captures, NOT an intervention or
the chance that chasing an apple will win it.

## Actual first movements, including missing/dead observations

| Starting distance rank | Closer | Sideways | Farther | Died at +1 | Unobserved normal step |
|---|---:|---:|---:|---:|---:|
| nearest | 663 | 0 | 249 | 0 | 0 |
| second | 548 | 0 | 363 | 1 | 0 |
- Nearest first moves into possible opponent head cones: **20/912 (2.2%)**; equal/longer cones: **0/912 (0.0%)**.
- Second first moves into possible opponent head cones: **30/911 (3.3%)**; equal/longer cones: **2/911 (0.2%)**.

A geometric cone includes collision-impossible opponent moves; it is NOT
a calibrated likelihood. Dead/unobserved first moves never become assumed safe
movements. Movement observations are survivor-selected.

## Palmer: distinct reference subset

Eligible apple appearances involving Palmer: **145**.
Palmer captured **74**; another participant captured **66**; censored/unverified **5**.
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
