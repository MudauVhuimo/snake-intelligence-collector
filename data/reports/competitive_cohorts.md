# Snake26: Strong, middle, and struggling league competitors — comparison

Generated UTC: 2026-11-03T15:23:21+00:00

## Scientific question

Across the competition, what danger-response patterns distinguish
consistently strong versus weaker *official league* snakes in
comparable situations? This is a population-level exploration,
NOT a study of our submitted agent or a named rival. ALL student bots
are eligible. Palmer is one top-division example, not the baseline.

## Cohort design and selection caveats

- Use official Division 1 standings from the **SAME replay season**
  as each sampled student, never transplant today's rank into older
  bot versions. Division 2 ranks are not mixed into Division 1.
- Top cohort: official division rank in best 25%; bottom: worst 25%;
  middle: remaining 50%. Only standings with at least 12 members qualify.
- A frame is sampled every 25 turns only when a student is near
  another live head (within 3 toroidal cells) OR has <=1 unoccupied
  neighbor. Same raw replay payload counted once, not once per season.
- Outcomes: real death event in the following 10 or 30 turns,
  with incomplete followup CENSORED and respawn still a death.
- We focus on actual league matches; controlled trials are shown
  SEPARATELY, grouped by the student's same-season league standing.
- Historical archived replays are deliberately sampled, not a random
  draw from all official matches. Rankings include game results;
  ranking groups are outcome-selected, not randomized policies.

Baseline windows available across BOTH environments: **4,049**.
Same-season Division 1 ranked league windows: **2,548**.
Same-season Division 1 ranked trial windows: **341**.
League windows without qualifying same-season rank: **841**.
Trial windows without qualifying same-season rank: **319**.
Duplicate rows excluded: **0**.

## 1. Observed danger exposure and outcomes by performance cohort

![Strong vs weak student danger windows](charts/cohort_danger_outcomes.svg)

| Match mode | Division 1 cohort | Students | Unique replays | Danger windows | Nearby heads | Confinement | Death by +10 (events/windows) | Death by +30 (events/windows) | Gained exit by +3 (among +10 survivors) | First move straight | Moved toward a persistent apple |
|---|---|---:|---:|---:|---|---|---|---|---|---|---|
| league | top_quartile | 15 | 60 | 838 | 64.32% | 42.36% | 12/838 (1.43%) | 20/824 (2.43%) | 826 sampled, 39.83% | 838 moves, 55.73% | 796 moves, 55.15% |
| league | middle_half | 37 | 64 | 1230 | 63.41% | 41.71% | 45/1230 (3.66%) | 75/1213 (6.18%) | 1185 sampled, 37.97% | 1225 moves, 57.88% | 1166 moves, 56.26% |
| league | bottom_quartile | 25 | 43 | 480 | 66.25% | 38.12% | 19/480 (3.96%) | 29/475 (6.11%) | 461 sampled, 35.79% | 479 moves, 63.47% | 452 moves, 53.76% |
| trial | top_quartile | 10 | 18 | 139 | 73.38% | 30.94% | 1/139 (0.72%) | 2/138 (1.45%) | 138 sampled, 31.88% | 139 moves, 67.63% | 129 moves, 65.89% |
| trial | middle_half | 11 | 15 | 149 | 67.11% | 41.61% | 0/149 (0.00%) | 0/148 (0.00%) | 149 sampled, 39.60% | 149 moves, 67.11% | 137 moves, 56.93% |
| trial | bottom_quartile | 5 | 6 | 53 | 83.02% | 20.75% | 1/53 (1.89%) | 1/53 (1.89%) | 52 sampled, 26.92% | 53 moves, 64.15% | 48 moves, 64.58% |

First-move straight/turn is reconstructed from two consecutive REAL frames.
Food progress means closing distance to the SAME apple still visible
one frame later; this does not prove the snake targeted that apple.
These rows DESCRIBE the encounters each cohort experienced; they do
not establish that stronger snakes made different decisions inequivalent states. A difference may reflect opponents and selection.

## 2. Restrict to comparable pre-decision danger situations

Common-support strata require BOTH top and bottom students in the
SAME environment, body length band, near-head yes/no, restricted
neighbor count yes/no, and 500-turn phase. Each group must contain
actual observations; we do not extrapolate outside overlap.

- Common strata across both modes: **50**.
- League replays with ranked student exposures: **69**.
- Those containing BOTH extreme cohorts: **38**.
- Distinct top/bottom students in overlapping games: **36**.

| Mode | Cohort within overlap | Windows | Distinct replays | +10 death frequency | +3 exit gain frequency | First-move straight | Same-apple progress |
|---|---|---:|---:|---|---|---|---|
| league | top_quartile | 837 | 60 | 1.43% | 39.88% | 55.68% | 55.22% |
| league | bottom_quartile | 473 | 43 | 3.81% | 35.60% | 63.77% | 53.48% |
| trial | top_quartile | 131 | 18 | 0.76% | 30.77% | 69.47% | 66.12% |
| trial | bottom_quartile | 45 | 6 | 2.22% | 22.73% | 64.44% | 59.52% |

## 3. Strong versus struggling snakes in the SAME real match

Each pair uses one top-quartile and one bottom-quartile student
from the SAME actual replay, SAME body-length band, near-head
condition, confined/unconfined condition, and 500-turn game phase.
Pairing uses only BASELINE variables, and no observed window is reused.
This is a harder comparison than grouping results across unrelated
games, but pairs may still differ in exact body location, apples,
opponent responses and how much time passes between snapshots.

Matched dangerous-position pairs: **90**.
Distinct league replays with strict matched pairs: **28**.

| Measured outcome (bottom minus top) | Both decisions observable | Replay clusters | Difference (percentage points) | Replay-resampled 95% interval |
|---|---:|---:|---:|---|
| Died in next 10 turns | 90 | 28 | +5.56 | [+1.75, +10.78] |
| First step was a turn/reversal rather than straight | 90 | 28 | -8.89 | [-21.59, +3.41] |
| Moved toward same still-visible apple | 84 | 28 | -2.38 | [-17.98, +14.63] |
| Gained 1+ neighboring cell by turn 3, among +10 survivors | 83 | 27 | -7.23 | [-18.92, +3.26] |

Positive values mean the bottom cohort exhibited the behavior or
death more frequently; negative values mean the top did.
Match-level bootstrap uncertainty addresses repeated episodes in
one replay, NOT repeated student versions across snapshots.
Even equal baseline categories are NOT identical legal choices;
none of these contrasts alone tells us which action caused survival.
[Auditable non-reused matched pairs](../derived/competitive_matched_decisions.csv).

These are COMMON-STRATUM comparisons but they are NOT reweighted
to identical distributions within the overlap. Even same-game cohorts
may occupy different locations and face unequal threats. No p-value
or effect-size certainty is claimed from individual windows.

## 4. What would make a useful algorithm rule?

Test the hypothesis that top league competitors select routes with
better safe future mobility after controlling for starting length,
head geometry and food opportunity. Our 0–4 free-neighbor count is
an INSTANTANEOUS proxy, not a legal-move count or full route quality.
We must next measure per-ACTION future reachable areas and opponent
reach cones, then reproduce any predictive advantage on HELD-OUT
entire matches and unseen bot versions.
A cohort difference at this stage is evidence for a feature to
test, NEVER evidence that copying a champion's move is optimal.

## Auditable outputs

- [Cohort sample sizes, outcomes, mobility](../derived/competitive_cohort_danger.csv).
- [Underlying complete danger-window observations](../derived/long_horizon_danger_windows.csv).
- [Research protocol and rule-promotion tests](../../docs/ALGORITHM_RESEARCH_PROTOCOL.md).

**No existing submitted snake code was modified.**
