# Snake26: Strong, middle, and struggling league competitors — comparison

Generated UTC: 2026-11-06T11:08:10+00:00

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

Baseline windows available across BOTH environments: **4,451**.
Same-season Division 1 ranked league windows: **2,845**.
Same-season Division 1 ranked trial windows: **391**.
League windows without qualifying same-season rank: **944**.
Trial windows without qualifying same-season rank: **271**.
Duplicate rows excluded: **0**.

## 1. Observed danger exposure and outcomes by performance cohort

![Strong vs weak student danger windows](charts/cohort_danger_outcomes.svg)

| Match mode | Division 1 cohort | Students | Unique replays | Danger windows | Nearby heads | Confinement | Death by +10 (events/windows) | Death by +30 (events/windows) | Gained exit by +3 (among +10 survivors) | First move straight | Moved toward a persistent apple |
|---|---|---:|---:|---:|---|---|---|---|---|---|---|
| league | top_quartile | 17 | 68 | 979 | 63.84% | 42.80% | 14/979 (1.43%) | 24/964 (2.49%) | 965 sampled, 39.90% | 978 moves, 55.83% | 931 moves, 55.42% |
| league | middle_half | 39 | 72 | 1333 | 63.09% | 42.01% | 49/1333 (3.68%) | 79/1316 (6.00%) | 1284 sampled, 38.55% | 1328 moves, 59.11% | 1262 moves, 56.26% |
| league | bottom_quartile | 27 | 48 | 533 | 65.85% | 38.65% | 22/533 (4.13%) | 32/528 (6.06%) | 511 sampled, 36.20% | 532 moves, 62.22% | 502 moves, 53.59% |
| trial | top_quartile | 12 | 21 | 158 | 71.52% | 32.91% | 1/158 (0.63%) | 2/156 (1.28%) | 157 sampled, 33.76% | 158 moves, 65.82% | 147 moves, 65.99% |
| trial | middle_half | 12 | 17 | 169 | 65.68% | 43.79% | 1/169 (0.59%) | 1/168 (0.60%) | 168 sampled, 39.88% | 168 moves, 67.26% | 154 moves, 57.79% |
| trial | bottom_quartile | 5 | 7 | 64 | 81.25% | 21.88% | 1/64 (1.56%) | 2/64 (3.12%) | 63 sampled, 23.81% | 64 moves, 64.06% | 56 moves, 66.07% |

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

- Common strata across both modes: **52**.
- League replays with ranked student exposures: **77**.
- Those containing BOTH extreme cohorts: **43**.
- Distinct top/bottom students in overlapping games: **40**.

| Mode | Cohort within overlap | Windows | Distinct replays | +10 death frequency | +3 exit gain frequency | First-move straight | Same-apple progress |
|---|---|---:|---:|---|---|---|---|
| league | top_quartile | 976 | 68 | 1.43% | 39.92% | 55.69% | 55.60% |
| league | bottom_quartile | 527 | 48 | 3.98% | 35.97% | 62.36% | 53.23% |
| trial | top_quartile | 150 | 21 | 0.67% | 32.89% | 67.33% | 65.47% |
| trial | bottom_quartile | 55 | 7 | 1.82% | 20.37% | 63.64% | 63.27% |

## 3. Strong versus struggling snakes in the SAME real match

Each pair uses one top-quartile and one bottom-quartile student
from the SAME actual replay, SAME body-length band, near-head
condition, confined/unconfined condition, and 500-turn game phase.
Pairing uses only BASELINE variables, and no observed window is reused.
This is a harder comparison than grouping results across unrelated
games, but pairs may still differ in exact body location, apples,
opponent responses and how much time passes between snapshots.

Matched dangerous-position pairs: **109**.
Distinct league replays with strict matched pairs: **33**.

| Measured outcome (bottom minus top) | Both decisions observable | Replay clusters | Difference (percentage points) | Replay-resampled 95% interval |
|---|---:|---:|---:|---|
| Died in next 10 turns | 109 | 33 | +5.50 | [+1.82, +10.20] |
| First step was a turn/reversal rather than straight | 109 | 33 | -6.42 | [-17.92, +3.85] |
| Moved toward same still-visible apple | 101 | 33 | -3.96 | [-17.24, +10.08] |
| Gained 1+ neighboring cell by turn 3, among +10 survivors | 101 | 32 | -8.91 | [-19.17, +0.84] |

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
