# Snake26: does occupied-space geometry explain underdog apples?

Generated UTC: 2026-11-02T23:41:36+00:00

## Critical definition

All included food episodes start with a built-in benchmark head at least THREE
toroidal Manhattan cells closer to the apple than the student head.
For this snapshot, temporarily treat ALL occupied snake body cells and
obstacles as permanently blocked, and run a toroidal breadth-first search
from each head to the food. This is an approximation: bodies and tails move.
Exclude episodes with no static path for either head, which can bias results.

## Main association

![Frozen-body route order and real apple recipient](charts/static_path_reversal.svg)

| Frozen-body path ordering | Student captures | Benchmark captures | Student capture share |
|---|---:|---:|---:|
| Student shortest | 293 | 312 | 48.4% |
| Benchmark shortest or tied | 220 | 3361 | 6.1% |

Observed difference in student capture share: **42.3 percentage points**.
Exploratory 95% **match-cluster bootstrap** interval for the difference:
**37.3 to 47.2 percentage points**
(4000 valid bootstrap draws, resampling 62 complete replay matches).
This interval reflects match-level resampling variability in this selected archive;
it does not adjust for bot version, different opponent skill or hidden strategy choices.

## Check whether the pattern is unique to one benchmark

| Initially closest benchmark | Reversal: student captures / all | Not reversed: student captures / all |
|---|---:|---:|
| ~benchmark | 83/166 (50.0%) | 33/1081 (3.1%) |
| ~gauntlet_1 | 40/83 (48.2%) | 17/376 (4.5%) |
| ~hungry | 29/54 (53.7%) | 11/381 (2.9%) |
| ~hunter | 36/71 (50.7%) | 8/367 (2.2%) |
| ~survivor | 82/178 (46.1%) | 49/912 (5.4%) |
| ~wander | 23/53 (43.4%) | 102/464 (22.0%) |

## What this does and DOES NOT establish

- This is **predictive association in recorded states**, not causal proof.
- The more distant student may also differ in length, steering policy or risk tolerance.
- The static route freezes every snake body; real tails vacate and opponents move.
- A food capture is not necessarily a deliberate race by all possible opponents.
- All apple events within one replay are correlated and should be clustered.
- To claim a strategy advantage, validate these conditional patterns on held-out
  replays and later compare actual executable snakes under controlled seeds.
- No competition snake has been modified.
