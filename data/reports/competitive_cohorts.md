# Snake26: Strong, middle, and struggling league competitors — comparison

Generated UTC: 2026-11-02T16:19:43+00:00

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

Baseline windows available across BOTH environments: **2,836**.
Same-season Division 1 ranked league windows: **1,765**.
Same-season Division 1 ranked trial windows: **190**.
League windows without qualifying same-season rank: **603**.
Trial windows without qualifying same-season rank: **278**.
Duplicate rows excluded: **0**.

## 1. Observed danger exposure and outcomes by performance cohort

![Strong vs weak student danger windows](charts/cohort_danger_outcomes.svg)

| Match mode | Division 1 cohort | Students | Unique replays | Danger windows | Nearby heads | Confinement | Death by +10 (events/windows) | Death by +30 (events/windows) | Gained exit by +3 (among +10 survivors) | First move straight | Moved toward a persistent apple |
|---|---|---:|---:|---:|---|---|---|---|---|---|---|
| league | top_quartile | 14 | 40 | 533 | 67.17% | 39.40% | 7/533 (1.31%) | 12/524 (2.29%) | 526 sampled, 38.59% | 533 moves, 53.66% | 506 moves, 57.11% |
| league | middle_half | 30 | 46 | 862 | 62.65% | 41.76% | 23/862 (2.67%) | 46/849 (5.42%) | 839 sampled, 37.54% | 858 moves, 57.93% | 823 moves, 56.62% |
| league | bottom_quartile | 20 | 32 | 370 | 64.59% | 39.73% | 14/370 (3.78%) | 22/368 (5.98%) | 356 sampled, 36.24% | 369 moves, 63.14% | 347 moves, 53.60% |
| trial | top_quartile | 7 | 14 | 93 | 72.04% | 33.33% | 1/93 (1.08%) | 2/93 (2.15%) | 92 sampled, 30.43% | 93 moves, 67.74% | 86 moves, 66.28% |
| trial | middle_half | 4 | 8 | 78 | 67.95% | 43.59% | 0/78 (0.00%) | 0/77 (0.00%) | 78 sampled, 34.62% | 78 moves, 65.38% | 71 moves, 50.70% |
| trial | bottom_quartile | 2 | 2 | 19 | 78.95% | 21.05% | 0/19 (0.00%) | 0/19 (0.00%) | 19 sampled, 36.84% | 19 moves, 57.89% | 19 moves, 52.63% |

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

- Common strata across both modes: **42**.
- League replays with ranked student exposures: **49**.
- Those containing BOTH extreme cohorts: **27**.
- Distinct top/bottom students in overlapping games: **31**.

| Mode | Cohort within overlap | Windows | Distinct replays | +10 death frequency | +3 exit gain frequency | First-move straight | Same-apple progress |
|---|---|---:|---:|---|---|---|---|
| league | top_quartile | 520 | 40 | 1.15% | 37.55% | 54.23% | 56.88% |
| league | bottom_quartile | 364 | 32 | 3.57% | 35.90% | 63.64% | 53.37% |
| trial | top_quartile | 66 | 14 | 0.00% | 27.27% | 72.73% | 61.67% |
| trial | bottom_quartile | 18 | 2 | 0.00% | 33.33% | 55.56% | 50.00% |

## 3. Strong versus struggling snakes in the SAME real match

Each pair uses one top-quartile and one bottom-quartile student
from the SAME actual replay, SAME body-length band, near-head
condition, confined/unconfined condition, and 500-turn game phase.
Pairing uses only BASELINE variables, and no observed window is reused.
This is a harder comparison than grouping results across unrelated
games, but pairs may still differ in exact body location, apples,
opponent responses and how much time passes between snapshots.

Matched dangerous-position pairs: **66**.
Distinct league replays with strict matched pairs: **20**.

| Measured outcome (bottom minus top) | Both decisions observable | Replay clusters | Difference (percentage points) | Replay-resampled 95% interval |
|---|---:|---:|---:|---|
| Died in next 10 turns | 66 | 20 | +4.55 | [+0.00, +9.68] |
| First step was a turn/reversal rather than straight | 66 | 20 | -10.61 | [-27.78, +5.33] |
| Moved toward same still-visible apple | 61 | 20 | -6.56 | [-26.79, +11.59] |
| Gained 1+ neighboring cell by turn 3, among +10 survivors | 63 | 20 | -7.94 | [-20.63, +4.00] |

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
