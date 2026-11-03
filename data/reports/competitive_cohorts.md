# Snake26: Strong, middle, and struggling league competitors — comparison

Generated UTC: 2026-11-03T07:00:48+00:00

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

Baseline windows available across BOTH environments: **3,531**.
Same-season Division 1 ranked league windows: **2,222**.
Same-season Division 1 ranked trial windows: **284**.
League windows without qualifying same-season rank: **721**.
Trial windows without qualifying same-season rank: **304**.
Duplicate rows excluded: **0**.

## 1. Observed danger exposure and outcomes by performance cohort

![Strong vs weak student danger windows](charts/cohort_danger_outcomes.svg)

| Match mode | Division 1 cohort | Students | Unique replays | Danger windows | Nearby heads | Confinement | Death by +10 (events/windows) | Death by +30 (events/windows) | Gained exit by +3 (among +10 survivors) | First move straight | Moved toward a persistent apple |
|---|---|---:|---:|---:|---|---|---|---|---|---|---|
| league | top_quartile | 15 | 52 | 690 | 65.07% | 41.88% | 10/690 (1.45%) | 16/679 (2.36%) | 680 sampled, 39.71% | 690 moves, 55.51% | 655 moves, 55.88% |
| league | middle_half | 35 | 56 | 1074 | 62.29% | 42.09% | 39/1074 (3.63%) | 66/1059 (6.23%) | 1035 sampled, 38.65% | 1069 moves, 57.81% | 1016 moves, 56.30% |
| league | bottom_quartile | 23 | 40 | 458 | 66.59% | 37.99% | 18/458 (3.93%) | 27/453 (5.96%) | 440 sampled, 35.68% | 457 moves, 63.46% | 430 moves, 54.42% |
| trial | top_quartile | 10 | 17 | 128 | 75.00% | 29.69% | 1/128 (0.78%) | 2/127 (1.57%) | 127 sampled, 29.92% | 128 moves, 67.19% | 119 moves, 67.23% |
| trial | middle_half | 8 | 12 | 121 | 65.29% | 42.98% | 0/121 (0.00%) | 0/120 (0.00%) | 121 sampled, 40.50% | 121 moves, 66.12% | 110 moves, 52.73% |
| trial | bottom_quartile | 4 | 4 | 35 | 85.71% | 17.14% | 0/35 (0.00%) | 0/35 (0.00%) | 35 sampled, 31.43% | 35 moves, 65.71% | 32 moves, 65.62% |

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

- Common strata across both modes: **46**.
- League replays with ranked student exposures: **61**.
- Those containing BOTH extreme cohorts: **35**.
- Distinct top/bottom students in overlapping games: **34**.

| Mode | Cohort within overlap | Windows | Distinct replays | +10 death frequency | +3 exit gain frequency | First-move straight | Same-apple progress |
|---|---|---:|---:|---|---|---|---|
| league | top_quartile | 687 | 52 | 1.46% | 39.59% | 55.60% | 56.13% |
| league | bottom_quartile | 451 | 40 | 3.77% | 35.48% | 63.78% | 54.14% |
| trial | top_quartile | 114 | 17 | 0.00% | 26.32% | 71.05% | 68.57% |
| trial | bottom_quartile | 29 | 4 | 0.00% | 27.59% | 65.52% | 60.71% |

## 3. Strong versus struggling snakes in the SAME real match

Each pair uses one top-quartile and one bottom-quartile student
from the SAME actual replay, SAME body-length band, near-head
condition, confined/unconfined condition, and 500-turn game phase.
Pairing uses only BASELINE variables, and no observed window is reused.
This is a harder comparison than grouping results across unrelated
games, but pairs may still differ in exact body location, apples,
opponent responses and how much time passes between snapshots.

Matched dangerous-position pairs: **88**.
Distinct league replays with strict matched pairs: **27**.

| Measured outcome (bottom minus top) | Both decisions observable | Replay clusters | Difference (percentage points) | Replay-resampled 95% interval |
|---|---:|---:|---:|---|
| Died in next 10 turns | 88 | 27 | +4.55 | [+1.02, +9.21] |
| First step was a turn/reversal rather than straight | 88 | 27 | -9.09 | [-23.38, +2.59] |
| Moved toward same still-visible apple | 82 | 27 | -4.88 | [-20.78, +11.36] |
| Gained 1+ neighboring cell by turn 3, among +10 survivors | 82 | 26 | -7.32 | [-18.64, +2.38] |

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
