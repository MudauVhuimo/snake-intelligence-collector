# Snake26: apple contest pre-action prediction check

Generated UTC: 2026-11-02T23:41:51+00:00

## Frozen predictors and population

Compare two explicitly FIXED predictions on verified league captures:
A) predict the nearer of the two closest student heads; when distances tie,
assign half-credit rather than arbitrarily favoring a student ID.
B) the same, but when distances tie, predict the LONGER of those two snakes;
equal lengths also receive half-credit. A win by any other snake scores
zero for both. This is expected classification credit, not an agent outcome.
No future movement is an input to either predictor.

Eligible apple episodes: **708**.
Verified captures: **670**; unverified/censored excluded: **38**.
Confirmed captures by one of two competitors: **616**;
by a different student: **54**.
Distinct replay SHA clusters in verified set: **71**.

## Predicted capturer accuracy (verified episodes only)

| Fixed rule | Expected accuracy |
|---|---:|
| Geometric nearest, 50/50 at ties | 68.0% |
| Nearest, break exact distance ties by longer body | 71.8% |
| Difference | +3.81 pp |

Exploratory 95% cluster-bootstrap interval for accuracy difference: **[+2.22 pp, +5.32 pp]**.
Resampled whole unique replay files (2000 seeded draws), not turns or apple events.
This interval does not adjust for repeated students, bot versions,
similar seeds, match schedule or prior exploration of the same data.

## Break down by initial distance gap

| Initial distance gap | Confirmed apples | Nearest baseline | Length tie-break |
|---|---:|---:|---:|
| 0 cells | 158 | 44.6% | 60.8% |
| 1 cells | 285 | 71.2% | 71.2% |
| 2 cells | 227 | 80.2% | 80.2% |

Distance tie is the ONLY stratum where the predictors differ.
For distance gaps of 1 or 2 cells, both predict the nearer head;
this does not claim that nearer is a safe or optimal movement policy.

## At exact distance ties, what did recorded body length predict?

| Initial body lengths | First head captured | Second head captured |
|---|---:|---:|
| First is longer | 42 | 16 |
| Equal length | 6 | 8 |
| Second is longer | 22 | 47 |

## Actual first moves (retrospective description ONLY)

This section uses observed next-frame moves and is NOT available to
either pre-action predictor. A snake moving closer is not evidence
of deliberate pursuit or that imitating its move would cause success.

| First head step | Second head step | First head captured | Second head captured |
|---|---|---:|---:|
| closer | closer | 250 | 56 |
| closer | farther | 173 | 10 |
| farther | closer | 9 | 77 |
| farther | farther | 23 | 18 |

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
