# Snake26: does occupied-space geometry explain underdog apples?

Generated UTC: 2026-11-02T06:09:55+00:00

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
| Student shortest | 254 | 270 | 48.5% |
| Benchmark shortest or tied | 197 | 2992 | 6.2% |

Observed difference in student capture share: **42.3 percentage points**.
Exploratory 95% **match-cluster bootstrap** interval for the difference:
**37.0 to 47.6 percentage points**
(4000 valid bootstrap draws, resampling 54 complete replay matches).
This interval reflects match-level resampling variability in this selected archive;
it does not adjust for bot version, different opponent skill or hidden strategy choices.

## Check whether the pattern is unique to one benchmark

| Initially closest benchmark | Reversal: student captures / all | Not reversed: student captures / all |
|---|---:|---:|
| ~benchmark | 75/144 (52.1%) | 28/958 (2.9%) |
| ~gauntlet_1 | 31/68 (45.6%) | 13/318 (4.1%) |
| ~hungry | 27/47 (57.4%) | 11/340 (3.2%) |
| ~hunter | 33/64 (51.6%) | 7/336 (2.1%) |
| ~survivor | 69/153 (45.1%) | 48/815 (5.9%) |
| ~wander | 19/48 (39.6%) | 90/422 (21.3%) |

## What this does and DOES NOT establish

- This is **predictive association in recorded states**, not causal proof.
- The more distant student may also differ in length, steering policy or risk tolerance.
- The static route freezes every snake body; real tails vacate and opponents move.
- A food capture is not necessarily a deliberate race by all possible opponents.
- All apple events within one replay are correlated and should be clustered.
- To claim a strategy advantage, validate these conditional patterns on held-out
  replays and later compare actual executable snakes under controlled seeds.
- No competition snake has been modified.
