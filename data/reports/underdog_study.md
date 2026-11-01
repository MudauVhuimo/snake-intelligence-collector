# Snake26 — How did the farther snake win?

Generated UTC: 2026-11-01T23:18:52+00:00

## Evidence quality

- Scanned **126** replay files; unique on-arrival trial replays: **33**.
- Duplicate archived trial files skipped: **13**; unreadable: **0**.
- Comparable first-visible student-vs-benchmark apple opportunities: **4156**.
- Captures matched to real next-frame head + eat event: **4121**.
- Disappearances without verified consumer: **2**.
Only on-arrival trials with EXACTLY one active student and at least one living built-in benchmark are included.
All distance comparisons use toroidal Manhattan geometry, not hypothetical safe paths.

## Initial distance disadvantage versus actual winner

![Outcome by initial distance advantage](charts/underdog_outcomes.svg)

| Who started at least 3 cells closer? | Student captured | Benchmark captured | Student share |
|---|---:|---:|---:|
| Benchmark | 338 | 2,185 | 13.4% |
| Neither (within 2) | 435 | 383 | 53.2% |
| Student | 673 | 107 | 86.3% |

The student share above describes captured apples only. One student faces three
benchmarks and their starting abilities and survival vary; it is NOT a fair head-to-head win rate.

## Focus: student captured while a benchmark started 3+ closer

- Verified captures: **338**; benchmark wins while initially closer: **2185**.
- In student wins, initially nearest benchmark died before capture: **61**.
- In student wins, student died before capture: **2**.
- In student wins, nearest benchmark consumed another apple before this capture: **0**.
- In student wins, benchmark had NO static path at first sight (all occupied bodies frozen): **57**.
- In student wins, student had no static path under the same approximation: **26**.
- In student wins, both static paths existed: **278**.
- Of those, the student's static path was SHORTER despite longer Manhattan distance: **157**.
- Median apple lifetime, student wins: **22.0 turns**; benchmark wins: **12 turns**.

![Food capture times](charts/underdog_lag.svg)

## First five turns: movement toward apple

![Fraction moving closer](charts/underdog_progress.svg)

- Complete comparable five-turn, death-free trajectories: **275** student-win
  and **1899** benchmark-win apple episodes.
- Student-win: student progress **3.16** cells on average; nearest
  benchmark progress **0.59** cells (distance decrease positive).
- Benchmark-win: student progress **1.15** cells; nearest
  benchmark progress **3.15** cells.
We exclude episodes with a death or respawn of either focal snake anywhere before capture
from this particular five-turn comparison. The selection is intentional but may bias results.
The apple must remain visible for 5 turns; fast captures are also excluded.

## Individual cases for inspection

See **underdog_examples.json** for up to 15 recorded distance traces of student wins
where a benchmark started at least 3 cells closer, both focal snakes remained alive,
and the apple remained present at least 8 turns.
See **underdog_episodes.csv** for all matched on-arrival events with distances, capture
time, death flags, and early-distance progress.

| Replay | First visible turn | Student initial distance | Nearest benchmark | Benchmark distance | Captured after |
|---|---:|---:|---|---:|---:|
| 2026-11-01-225859-season/trials/413538-lelethuthando-nikelo/trial-911000.rep | 663 | 24 | ~hunter | 4 | 24 |
| 2026-10-14-123340-season/trials/409997-utayan-naidoo/trial-910000.rep | 516 | 31 | ~survivor | 11 | 34 |
| 2026-10-14-123340-season/trials/409987-sbongakonke-shange/trial-910000.rep | 1452 | 28 | ~survivor | 8 | 89 |
| 2026-10-14-123340-season/trials/402334-angile-saho/trial-910000.rep | 1435 | 27 | ~hungry | 8 | 27 |
| 2026-10-14-123340-season/trials/408070-collen-mthombeni/trial-911000.rep | 1403 | 25 | ~wander | 6 | 31 |
| 2026-10-14-123340-season/trials/409997-utayan-naidoo/trial-911000.rep | 1885 | 23 | ~benchmark | 5 | 23 |
| 2026-11-01-215859-season/trials/409598-langelihle-funeka/trial-911000.rep | 1002 | 21 | ~wander | 3 | 24 |
| 2026-11-01-205859-season/trials/402334-angile-saho/trial-912000.rep | 1782 | 28 | ~survivor | 10 | 28 |
| 2026-11-01-215859-season/trials/409598-langelihle-funeka/trial-912000.rep | 1256 | 29 | ~gauntlet_1 | 11 | 34 |
| 2026-10-23-145906-season/trials/388060-tshepang-tshabalala/trial-911000.rep | 867 | 31 | ~wander | 13 | 47 |

## Interpretation and next work

Farther-but-faster does not automatically imply pathfinding superiority.
A closer snake could have chosen a different apple, waited for safety, or been
unable to reach the apple along a safe path. Other opponents can affect both.
Next: calculate **actual route efficiency and obstacle-aware distance at first sight**;
compare traced examples, then produce spatial board/path visualizations.
Static path is a conservative snapshot BFS with all snake bodies frozen in place;
tails can vacate, so an unreachable static path does NOT mean a truly impossible route.
A benchmark eating another apple is observed diversion, not proof of its objective.
No competition bot has been modified.

## Observed spatial paths and distance histories

![Recorded underdog race 1](charts/underdog_case_1.svg)

![Recorded underdog race 2](charts/underdog_case_2.svg)

Paths follow actual recorded heads; wraparound edges are not drawn as teleports.
