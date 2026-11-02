# Snake26: does occupied-space geometry explain underdog apples?

Generated UTC: 2026-11-02T00:43:28+00:00

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
| Student shortest | 210 | 229 | 47.8% |
| Benchmark shortest or tied | 174 | 2567 | 6.3% |

Observed difference in student capture share: **41.5 percentage points**.
Exploratory 95% **match-cluster bootstrap** interval for the difference:
**35.4 to 47.9 percentage points**
(4000 valid bootstrap draws, resampling 46 complete replay matches).
This interval reflects match-level resampling variability in this selected archive;
it does not adjust for bot version, different opponent skill or hidden strategy choices.

## Check whether the pattern is unique to one benchmark

| Initially closest benchmark | Reversal: student captures / all | Not reversed: student captures / all |
|---|---:|---:|
| ~benchmark | 66/125 (52.8%) | 26/840 (3.1%) |
| ~gauntlet_1 | 27/57 (47.4%) | 11/271 (4.1%) |
| ~hungry | 18/35 (51.4%) | 9/275 (3.3%) |
| ~hunter | 25/53 (47.2%) | 7/299 (2.3%) |
| ~survivor | 57/123 (46.3%) | 40/680 (5.9%) |
| ~wander | 17/46 (37.0%) | 81/376 (21.5%) |

## What this does and DOES NOT establish

- This is **predictive association in recorded states**, not causal proof.
- The more distant student may also differ in length, steering policy or risk tolerance.
- The static route freezes every snake body; real tails vacate and opponents move.
- A food capture is not necessarily a deliberate race by all possible opponents.
- All apple events within one replay are correlated and should be clustered.
- To claim a strategy advantage, validate these conditional patterns on held-out
  replays and later compare actual executable snakes under controlled seeds.
- No competition snake has been modified.
