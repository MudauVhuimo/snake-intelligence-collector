# Snake26: Head pressure, escape options, and subsequent deaths

Generated UTC: 2026-11-02T23:43:33+00:00

## Study design — actual replay frames, not a simulator

At every **25th turn**, for each living STUDENT, measure the toroidal
Manhattan distance to the nearest **living opponent head** and number
of immediately unoccupied neighboring cells (0–4, all current snake
bodies and obstacles treated as blocked). Check whether that same snake
has a recorded **death event in the NEXT 10 contiguous turns**.
A sampled window can include a death but we do not infer causes or intent.
The immediate-neighbor metric is a conservative **snapshot proxy**,
NOT a legal-action count or guaranteed future escape: tails and heads move.
Windows are spaced 25 turns apart to avoid overlapping 10-turn outcomes.
They are STILL correlated within snake and replay match.

## Coverage and quality first

- Archived files scanned: **200** of 200 candidate files.
- Unique replay payloads: **133**
(league **71**, trials **62**).
- Exact byte-identical duplicates skipped: **67**.
- Unreadable / invalid: **0**.
- Single-student league games excluded: **0**.
- Nonstandard trial rosters excluded: **0**.
- Student windows with complete follow-up: **27,456**.
- Distinct student/replay summaries: **346**.
- Latest sampled season: **2026-11-02-225901-season**.
- Latest sampled student-season with BOTH replay modes: **3**.

## 1. Head pressure and observed future death

![Pressure and 10-turn death events](charts/head_pressure_vs_death.svg)

| Environment | Nearest opponent head | Windows | Death in next 10 turns | Observed frequency | Unique replays |
|---|---|---:|---:|---:|---:|
| league | Opponent head ≤3 | 1,666 | 37 | 2.22% | 71 |
| league | Head 4–7 | 4,329 | 30 | 0.69% | 71 |
| league | Head ≥8 | 16,504 | 52 | 0.32% | 71 |
| trial | Opponent head ≤3 | 389 | 3 | 0.77% | 61 |
| trial | Head 4–7 | 980 | 0 | 0.00% | 62 |
| trial | Head ≥8 | 3,588 | 2 | 0.06% | 62 |

A close opponent head does NOT imply an aggressive attack or a collision.
This is a selected replay sample. Risk differences are not causal effects
and are not comparisons between equally skilled opponent populations.

## 2. Pressure vs distance alone: match-level uncertainty

- **league:** close-minus-far risk = **+1.91 percentage points**; exploratory 95% match-resampled interval **[+1.23, +2.65]**, 71 distinct replay clusters.
- **trial:** close-minus-far risk = **+0.72 percentage points**; exploratory 95% match-resampled interval **[-0.06, +1.71]**, 62 distinct replay clusters.

Resampling entire REPLAYS reduces pseudo-replication from repeated turns.
It does not adjust confounding from body length, opponent type, code
versions, player ability or game phase.

## 3. Compare danger within body-length categories

| Mode | Length | Head ≤3: death/windows | Head ≥8: death/windows | Close - far frequency |
|---|---|---:|---:|---:|
| league | 5-24 | 5/323 | 6/3624 | 1.38 pp |
| league | 25-49 | 11/309 | 9/3587 | 3.31 pp |
| league | 50-99 | 13/609 | 18/5545 | 1.81 pp |
| league | 100+ | 8/425 | 19/3748 | 1.38 pp |
| trial | 5-24 | 0/37 | 0/328 | 0.00 pp |
| trial | 25-49 | 1/66 | 0/373 | 1.52 pp |
| trial | 50-99 | 1/90 | 0/739 | 1.11 pp |
| trial | 100+ | 1/196 | 2/2148 | 0.42 pp |

## 4. Immediate escape space at the same head pressure

| Mode | Head proximity | Free neighboring cells | Death events/windows | Observed frequency |
|---|---|---|---:|---:|
| league | Opponent head ≤3 | 0-1 free sides | 14/127 | 11.02% |
| league | Opponent head ≤3 | 2-4 free sides | 23/1539 | 1.49% |
| league | Head ≥8 | 0-1 free sides | 30/708 | 4.24% |
| league | Head ≥8 | 2-4 free sides | 22/15796 | 0.14% |
| trial | Opponent head ≤3 | 0-1 free sides | 3/30 | 10.00% |
| trial | Opponent head ≤3 | 2-4 free sides | 0/359 | 0.00% |
| trial | Head ≥8 | 0-1 free sides | 1/94 | 1.06% |
| trial | Head ≥8 | 2-4 free sides | 1/3494 | 0.03% |

This helps distinguish crowded **local geometry** from opponent-head
pressure, but is still a snapshot association, not an actual 10-turn
pathfinding or safety proof.

## 5. Palmer and other known students — descriptive exposure only

| Student | Mode | Replay matches | Sampled windows | Head ≤3 share | 0–1 free-side share | Death in next 10-turn window |
|---|---|---:|---:|---:|---:|---:|
| 421462-alexander-palmer | league | 18 | 1439 | 8.3% | 4.2% | 2/1439 |
| 421462-alexander-palmer | trial | 3 | 240 | 7.5% | 2.5% | 0/240 |
| 388060-tshepang-tshabalala | league | 11 | 878 | 7.4% | 4.6% | 3/878 |
| 388060-tshepang-tshabalala | trial | 3 | 240 | 7.5% | 2.5% | 0/240 |
| 428786-marvellous-sambo | league | 6 | 480 | 6.9% | 4.2% | 3/480 |
| 409997-utayan-naidoo | league | 9 | 717 | 7.5% | 4.5% | 7/717 |
| 409997-utayan-naidoo | trial | 3 | 240 | 7.1% | 2.5% | 0/240 |
| 403754-vhuimo-mudau | league | 4 | 318 | 3.1% | 6.3% | 0/318 |

These students have very different recorded sample sizes. Rows include
multiple seasons and possibly changed bot submissions. Do NOT rank their
intrinsic skill using these unadjusted exposure percentages.

## 6. Same student and season: can head-pressure behavior transfer?

Latest sampled paired-student cohort: **3**.
At least four paired students with reliable coverage are needed even
to explore a rank correlation; sample size, opponent type and replay
selection must be shown before stronger conclusions.

## Reproducible exports

- [Student-season mode-separated threat exposure](../derived/threat_window_student_seasons.csv)
- [Per replay student exposure and outcome totals](../derived/threat_window_replay_summary.csv)

**Next hypothesis:** a strong competitor preserves local exits BEFORE
near-head encounters, rather than maximizing distance from everyone.
This study cannot yet establish that policy. Validate across new league
replays and matched controls before trying it in the Java agent.
