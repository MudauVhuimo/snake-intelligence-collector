# Snake26: real league apple contests

Generated UTC: 2026-11-03T12:27:22+00:00

## Opportunity definition

One observation is a newly visible apple with two living STUDENT heads within
10 toroidal Manhattan steps, separated by at most 2 steps in distance to that apple.
First-frame food is flagged in the CSV. Replays with only one student are excluded.
Distance is NOT a safe-path estimate; this is selected, observational replay data.

Unique replay payloads: **85**; exact duplicates: **58**.
Close-peer opportunities: **853**.
Captures verified within 40 turns: **808/853 (94.7%)**.
Unverified disappearances: **0**; horizon/end censored: **45**; frame gaps: **0**.

## Actual capturer among verified outcomes

| Position at first visibility | Captures | Share of confirmed |
|---|---:|---:|
| Strictly closest | 470 | 58.2% |
| Strictly second-closest | 106 | 13.1% |
| Tied first (ID-order tie break) | 86 | 10.6% |
| Tied second (ID-order tie break) | 87 | 10.8% |
| Other participant | 59 | 7.3% |

These shares are conditional on confirmed captures, NOT an intervention or
the chance that chasing an apple will win it.

## Actual first movements, including missing/dead observations

| Starting distance rank | Closer | Sideways | Farther | Died at +1 | Unobserved normal step |
|---|---:|---:|---:|---:|---:|
| nearest | 624 | 0 | 229 | 0 | 0 |
| second | 517 | 0 | 336 | 0 | 0 |
- Nearest first moves into possible opponent head cones: **18/853 (2.1%)**; equal/longer cones: **0/853 (0.0%)**.
- Second first moves into possible opponent head cones: **28/853 (3.3%)**; equal/longer cones: **2/853 (0.2%)**.

A geometric cone includes collision-impossible opponent moves; it is NOT
a calibrated likelihood. Dead/unobserved first moves never become assumed safe
movements. Movement observations are survivor-selected.

## Palmer: distinct reference subset

Eligible apple appearances involving Palmer: **127**.
Palmer captured **61**; another participant captured **61**; censored/unverified **5**.
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
