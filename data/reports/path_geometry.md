# Snake26: does occupied-space geometry explain underdog apples?

Generated UTC: 2026-11-03T15:19:42+00:00

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
| Student shortest | 363 | 387 | 48.4% |
| Benchmark shortest or tied | 269 | 4281 | 5.9% |

Observed difference in student capture share: **42.5 percentage points**.
Exploratory 95% **match-cluster bootstrap** interval for the difference:
**38.4 to 46.5 percentage points**
(4000 valid bootstrap draws, resampling 78 complete replay matches).
This interval reflects match-level resampling variability in this selected archive;
it does not adjust for bot version, different opponent skill or hidden strategy choices.

## Check whether the pattern is unique to one benchmark

| Initially closest benchmark | Reversal: student captures / all | Not reversed: student captures / all |
|---|---:|---:|
| ~benchmark | 109/218 (50.0%) | 41/1362 (3.0%) |
| ~gauntlet_1 | 53/108 (49.1%) | 22/500 (4.4%) |
| ~hungry | 38/68 (55.9%) | 13/503 (2.6%) |
| ~hunter | 36/72 (50.0%) | 12/423 (2.8%) |
| ~survivor | 102/226 (45.1%) | 67/1227 (5.5%) |
| ~wander | 25/58 (43.1%) | 114/535 (21.3%) |

## What this does and DOES NOT establish

- This is **predictive association in recorded states**, not causal proof.
- The more distant student may also differ in length, steering policy or risk tolerance.
- The static route freezes every snake body; real tails vacate and opponents move.
- A food capture is not necessarily a deliberate race by all possible opponents.
- All apple events within one replay are correlated and should be clustered.
- To claim a strategy advantage, validate these conditional patterns on held-out
  replays and later compare actual executable snakes under controlled seeds.
- No competition snake has been modified.
