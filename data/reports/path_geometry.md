# Snake26: does occupied-space geometry explain underdog apples?

Generated UTC: 2026-11-03T19:55:51+00:00

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
| Student shortest | 380 | 419 | 47.6% |
| Benchmark shortest or tied | 284 | 4481 | 6.0% |

Observed difference in student capture share: **41.6 percentage points**.
Exploratory 95% **match-cluster bootstrap** interval for the difference:
**37.6 to 45.7 percentage points**
(4000 valid bootstrap draws, resampling 82 complete replay matches).
This interval reflects match-level resampling variability in this selected archive;
it does not adjust for bot version, different opponent skill or hidden strategy choices.

## Check whether the pattern is unique to one benchmark

| Initially closest benchmark | Reversal: student captures / all | Not reversed: student captures / all |
|---|---:|---:|
| ~benchmark | 116/238 (48.7%) | 43/1426 (3.0%) |
| ~gauntlet_1 | 54/112 (48.2%) | 24/535 (4.5%) |
| ~hungry | 38/70 (54.3%) | 13/523 (2.5%) |
| ~hunter | 38/75 (50.7%) | 12/433 (2.8%) |
| ~survivor | 107/241 (44.4%) | 75/1299 (5.8%) |
| ~wander | 27/63 (42.9%) | 117/549 (21.3%) |

## What this does and DOES NOT establish

- This is **predictive association in recorded states**, not causal proof.
- The more distant student may also differ in length, steering policy or risk tolerance.
- The static route freezes every snake body; real tails vacate and opponents move.
- A food capture is not necessarily a deliberate race by all possible opponents.
- All apple events within one replay are correlated and should be clustered.
- To claim a strategy advantage, validate these conditional patterns on held-out
  replays and later compare actual executable snakes under controlled seeds.
- No competition snake has been modified.
