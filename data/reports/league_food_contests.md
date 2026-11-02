# Snake26: real league apple contests

Generated UTC: 2026-11-02T23:41:51+00:00

## Opportunity definition

One observation is a newly visible apple with two living STUDENT heads within
10 toroidal Manhattan steps, separated by at most 2 steps in distance to that apple.
First-frame food is flagged in the CSV. Replays with only one student are excluded.
Distance is NOT a safe-path estimate; this is selected, observational replay data.

Unique replay payloads: **71**; exact duplicates: **54**.
Close-peer opportunities: **708**.
Captures verified within 40 turns: **670/708 (94.6%)**.
Unverified disappearances: **0**; horizon/end censored: **38**; frame gaps: **0**.

## Actual capturer among verified outcomes

| Position at first visibility | Captures | Share of confirmed |
|---|---:|---:|
| Strictly closest | 385 | 57.5% |
| Strictly second-closest | 90 | 13.4% |
| Tied first (ID-order tie break) | 70 | 10.4% |
| Tied second (ID-order tie break) | 71 | 10.6% |
| Other participant | 54 | 8.1% |

These shares are conditional on confirmed captures, NOT an intervention or
the chance that chasing an apple will win it.

## Actual first movements, including missing/dead observations

| Starting distance rank | Closer | Sideways | Farther | Died at +1 | Unobserved normal step |
|---|---:|---:|---:|---:|---:|
| nearest | 523 | 0 | 185 | 0 | 0 |
| second | 428 | 0 | 280 | 0 | 0 |
- Nearest first moves into possible opponent head cones: **15/708 (2.1%)**; equal/longer cones: **0/708 (0.0%)**.
- Second first moves into possible opponent head cones: **22/708 (3.1%)**; equal/longer cones: **1/708 (0.1%)**.

A geometric cone includes collision-impossible opponent moves; it is NOT
a calibrated likelihood. Dead/unobserved first moves never become assumed safe
movements. Movement observations are survivor-selected.

## Palmer: distinct reference subset

Eligible apple appearances involving Palmer: **86**.
Palmer captured **42**; another participant captured **41**; censored/unverified **3**.
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
