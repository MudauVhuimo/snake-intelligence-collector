# Snake26: does occupied-space geometry explain underdog apples?

Generated UTC: 2026-11-02T16:17:03+00:00

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
| Student shortest | 277 | 304 | 47.7% |
| Benchmark shortest or tied | 212 | 3178 | 6.3% |

Observed difference in student capture share: **41.4 percentage points**.
Exploratory 95% **match-cluster bootstrap** interval for the difference:
**36.5 to 46.4 percentage points**
(4000 valid bootstrap draws, resampling 58 complete replay matches).
This interval reflects match-level resampling variability in this selected archive;
it does not adjust for bot version, different opponent skill or hidden strategy choices.

## Check whether the pattern is unique to one benchmark

| Initially closest benchmark | Reversal: student captures / all | Not reversed: student captures / all |
|---|---:|---:|
| ~benchmark | 81/161 (50.3%) | 30/1022 (2.9%) |
| ~gauntlet_1 | 35/77 (45.5%) | 16/347 (4.6%) |
| ~hungry | 29/53 (54.7%) | 11/364 (3.0%) |
| ~hunter | 35/70 (50.0%) | 8/348 (2.3%) |
| ~survivor | 75/168 (44.6%) | 49/866 (5.7%) |
| ~wander | 22/52 (42.3%) | 98/443 (22.1%) |

## What this does and DOES NOT establish

- This is **predictive association in recorded states**, not causal proof.
- The more distant student may also differ in length, steering policy or risk tolerance.
- The static route freezes every snake body; real tails vacate and opponents move.
- A food capture is not necessarily a deliberate race by all possible opponents.
- All apple events within one replay are correlated and should be clustered.
- To claim a strategy advantage, validate these conditional patterns on held-out
  replays and later compare actual executable snakes under controlled seeds.
- No competition snake has been modified.
