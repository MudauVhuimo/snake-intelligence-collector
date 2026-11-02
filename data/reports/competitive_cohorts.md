# Snake26: Strong, middle, and struggling league competitors — comparison

Generated UTC: 2026-11-02T23:44:28+00:00

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

Baseline windows available across BOTH environments: **3,093**.
Same-season Division 1 ranked league windows: **1,893**.
Same-season Division 1 ranked trial windows: **219**.
League windows without qualifying same-season rank: **691**.
Trial windows without qualifying same-season rank: **290**.
Duplicate rows excluded: **0**.

## 1. Observed danger exposure and outcomes by performance cohort

![Strong vs weak student danger windows](charts/cohort_danger_outcomes.svg)

| Match mode | Division 1 cohort | Students | Unique replays | Danger windows | Nearby heads | Confinement | Death by +10 (events/windows) | Death by +30 (events/windows) | Gained exit by +3 (among +10 survivors) | First move straight | Moved toward a persistent apple |
|---|---|---:|---:|---:|---|---|---|---|---|---|---|
| league | top_quartile | 15 | 44 | 560 | 65.71% | 40.54% | 8/560 (1.43%) | 13/550 (2.36%) | 552 sampled, 39.49% | 560 moves, 53.57% | 531 moves, 56.31% |
| league | middle_half | 33 | 50 | 934 | 62.21% | 42.08% | 28/934 (3.00%) | 52/921 (5.65%) | 906 sampled, 38.41% | 930 moves, 57.63% | 892 moves, 55.94% |
| league | bottom_quartile | 21 | 36 | 399 | 64.91% | 39.60% | 16/399 (4.01%) | 25/396 (6.31%) | 383 sampled, 36.03% | 398 moves, 62.56% | 375 moves, 53.60% |
| trial | top_quartile | 7 | 14 | 93 | 72.04% | 33.33% | 1/93 (1.08%) | 2/93 (2.15%) | 92 sampled, 30.43% | 93 moves, 67.74% | 86 moves, 66.28% |
| trial | middle_half | 6 | 10 | 99 | 65.66% | 43.43% | 0/99 (0.00%) | 0/98 (0.00%) | 99 sampled, 37.37% | 99 moves, 66.67% | 92 moves, 51.09% |
| trial | bottom_quartile | 3 | 3 | 27 | 81.48% | 18.52% | 0/27 (0.00%) | 0/27 (0.00%) | 27 sampled, 33.33% | 27 moves, 66.67% | 26 moves, 61.54% |

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

- Common strata across both modes: **44**.
- League replays with ranked student exposures: **53**.
- Those containing BOTH extreme cohorts: **31**.
- Distinct top/bottom students in overlapping games: **33**.

| Mode | Cohort within overlap | Windows | Distinct replays | +10 death frequency | +3 exit gain frequency | First-move straight | Same-apple progress |
|---|---|---:|---:|---|---|---|---|
| league | top_quartile | 547 | 44 | 1.28% | 38.52% | 54.11% | 56.07% |
| league | bottom_quartile | 393 | 36 | 3.82% | 35.71% | 63.01% | 53.39% |
| trial | top_quartile | 80 | 14 | 0.00% | 26.25% | 71.25% | 67.12% |
| trial | bottom_quartile | 26 | 3 | 0.00% | 30.77% | 65.38% | 60.00% |

## 3. Strong versus struggling snakes in the SAME real match

Each pair uses one top-quartile and one bottom-quartile student
from the SAME actual replay, SAME body-length band, near-head
condition, confined/unconfined condition, and 500-turn game phase.
Pairing uses only BASELINE variables, and no observed window is reused.
This is a harder comparison than grouping results across unrelated
games, but pairs may still differ in exact body location, apples,
opponent responses and how much time passes between snapshots.

Matched dangerous-position pairs: **70**.
Distinct league replays with strict matched pairs: **23**.

| Measured outcome (bottom minus top) | Both decisions observable | Replay clusters | Difference (percentage points) | Replay-resampled 95% interval |
|---|---:|---:|---:|---|
| Died in next 10 turns | 70 | 23 | +4.29 | [+0.00, +8.86] |
| First step was a turn/reversal rather than straight | 70 | 23 | -11.43 | [-28.33, +2.78] |
| Moved toward same still-visible apple | 65 | 23 | -4.62 | [-23.53, +12.86] |
| Gained 1+ neighboring cell by turn 3, among +10 survivors | 67 | 23 | -10.45 | [-22.06, +1.82] |

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
