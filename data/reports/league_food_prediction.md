# Snake26: apple contest pre-action prediction check

Generated UTC: 2026-11-02T16:17:16+00:00

## Frozen predictors and population

Compare two explicitly FIXED predictions on verified league captures:
A) predict the nearer of the two closest student heads; when distances tie,
assign half-credit rather than arbitrarily favoring a student ID.
B) the same, but when distances tie, predict the LONGER of those two snakes;
equal lengths also receive half-credit. A win by any other snake scores
zero for both. This is expected classification credit, not an agent outcome.
No future movement is an input to either predictor.

Eligible apple episodes: **642**.
Verified captures: **607**; unverified/censored excluded: **35**.
Confirmed captures by one of two competitors: **557**;
by a different student: **50**.
Distinct replay SHA clusters in verified set: **65**.

## Predicted capturer accuracy (verified episodes only)

| Fixed rule | Expected accuracy |
|---|---:|
| Geometric nearest, 50/50 at ties | 68.0% |
| Nearest, break exact distance ties by longer body | 71.3% |
| Difference | +3.38 pp |

Exploratory 95% cluster-bootstrap interval for accuracy difference: **[+1.89 pp, +4.99 pp]**.
Resampled whole unique replay files (2000 seeded draws), not turns or apple events.
This interval does not adjust for repeated students, bot versions,
similar seeds, match schedule or prior exploration of the same data.

## Break down by initial distance gap

| Initial distance gap | Confirmed apples | Nearest baseline | Length tie-break |
|---|---:|---:|---:|
| 0 cells | 141 | 44.3% | 58.9% |
| 1 cells | 260 | 70.8% | 70.8% |
| 2 cells | 206 | 80.6% | 80.6% |

Distance tie is the ONLY stratum where the predictors differ.
For distance gaps of 1 or 2 cells, both predict the nearer head;
this does not claim that nearer is a safe or optimal movement policy.

## At exact distance ties, what did recorded body length predict?

| Initial body lengths | First head captured | Second head captured |
|---|---:|---:|
| First is longer | 33 | 14 |
| Equal length | 6 | 8 |
| Second is longer | 21 | 43 |

## Actual first moves (retrospective description ONLY)

This section uses observed next-frame moves and is NOT available to
either pre-action predictor. A snake moving closer is not evidence
of deliberate pursuit or that imitating its move would cause success.

| First head step | Second head step | First head captured | Second head captured |
|---|---|---:|---:|
| closer | closer | 228 | 50 |
| closer | farther | 155 | 8 |
| farther | closer | 7 | 72 |
| farther | farther | 20 | 17 |

## What this does NOT establish

- More length at equal distance is predictive, not proof that choosing
  an apple race based on length increases score or survival.
- Distance ignores occupied-path geometry, future turns, and opponent choices.
- Current results are selected archived games and may overlap competitor versions.
- A real agent's utility must include death/reset risk, retained growth, and
  league placement, evaluated on unseen games and diverse opponents.
- Palmer remains in the main evidence, with its separately audited
  [casebook](palmer_casebook.md) and [apple episodes](league_food_contests.md).

[Raw episode CSV](../derived/league_food_contests.csv).
**No competition Snake AI was modified.**
