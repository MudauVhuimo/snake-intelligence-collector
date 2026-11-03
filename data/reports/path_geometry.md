# Snake26: does occupied-space geometry explain underdog apples?

Generated UTC: 2026-11-03T06:58:36+00:00

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
| Student shortest | 327 | 346 | 48.6% |
| Benchmark shortest or tied | 246 | 3843 | 6.0% |

Observed difference in student capture share: **42.6 percentage points**.
Exploratory 95% **match-cluster bootstrap** interval for the difference:
**38.1 to 47.1 percentage points**
(4000 valid bootstrap draws, resampling 70 complete replay matches).
This interval reflects match-level resampling variability in this selected archive;
it does not adjust for bot version, different opponent skill or hidden strategy choices.

## Check whether the pattern is unique to one benchmark

| Initially closest benchmark | Reversal: student captures / all | Not reversed: student captures / all |
|---|---:|---:|
| ~benchmark | 95/186 (51.1%) | 38/1231 (3.1%) |
| ~gauntlet_1 | 49/100 (49.0%) | 20/451 (4.4%) |
| ~hungry | 32/62 (51.6%) | 12/448 (2.7%) |
| ~hunter | 36/71 (50.7%) | 10/392 (2.6%) |
| ~survivor | 91/199 (45.7%) | 59/1079 (5.5%) |
| ~wander | 24/55 (43.6%) | 107/488 (21.9%) |

## What this does and DOES NOT establish

- This is **predictive association in recorded states**, not causal proof.
- The more distant student may also differ in length, steering policy or risk tolerance.
- The static route freezes every snake body; real tails vacate and opponents move.
- A food capture is not necessarily a deliberate race by all possible opponents.
- All apple events within one replay are correlated and should be clustered.
- To claim a strategy advantage, validate these conditional patterns on held-out
  replays and later compare actual executable snakes under controlled seeds.
- No competition snake has been modified.
