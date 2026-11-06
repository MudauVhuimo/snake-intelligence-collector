# Snake26: Head pressure, escape options, and subsequent deaths

Generated UTC: 2026-11-06T11:07:05+00:00

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

- Archived files scanned: **250** of 260 candidate files.
- Unique replay payloads: **181**
(league **102**, trials **79**).
- Exact byte-identical duplicates skipped: **69**.
- Unreadable / invalid: **0**.
- Single-student league games excluded: **0**.
- Nonstandard trial rosters excluded: **0**.
- Student windows with complete follow-up: **38,636**.
- Distinct student/replay summaries: **487**.
- Latest sampled season: **2026-11-06-102324-season**.
- Latest sampled student-season with BOTH replay modes: **3**.

## 1. Head pressure and observed future death

![Pressure and 10-turn death events](charts/head_pressure_vs_death.svg)

| Environment | Nearest opponent head | Windows | Death in next 10 turns | Observed frequency | Unique replays |
|---|---|---:|---:|---:|---:|
| league | Opponent head ≤3 | 2,435 | 58 | 2.38% | 102 |
| league | Head 4–7 | 6,219 | 48 | 0.77% | 102 |
| league | Head ≥8 | 23,663 | 73 | 0.31% | 102 |
| trial | Opponent head ≤3 | 491 | 2 | 0.41% | 78 |
| trial | Head 4–7 | 1,262 | 1 | 0.08% | 79 |
| trial | Head ≥8 | 4,566 | 3 | 0.07% | 79 |

A close opponent head does NOT imply an aggressive attack or a collision.
This is a selected replay sample. Risk differences are not causal effects
and are not comparisons between equally skilled opponent populations.

## 2. Pressure vs distance alone: match-level uncertainty

- **league:** close-minus-far risk = **+2.07 percentage points**; exploratory 95% match-resampled interval **[+1.43, +2.66]**, 102 distinct replay clusters.
- **trial:** close-minus-far risk = **+0.34 percentage points**; exploratory 95% match-resampled interval **[-0.09, +0.96]**, 79 distinct replay clusters.

Resampling entire REPLAYS reduces pseudo-replication from repeated turns.
It does not adjust confounding from body length, opponent type, code
versions, player ability or game phase.

## 3. Compare danger within body-length categories

| Mode | Length | Head ≤3: death/windows | Head ≥8: death/windows | Close - far frequency |
|---|---|---:|---:|---:|
| league | 5-24 | 7/439 | 8/5170 | 1.44 pp |
| league | 25-49 | 16/478 | 11/5171 | 3.13 pp |
| league | 50-99 | 19/894 | 24/7879 | 1.82 pp |
| league | 100+ | 16/624 | 30/5443 | 2.01 pp |
| trial | 5-24 | 0/50 | 0/437 | 0.00 pp |
| trial | 25-49 | 1/79 | 0/495 | 1.27 pp |
| trial | 50-99 | 0/123 | 1/996 | -0.10 pp |
| trial | 100+ | 1/239 | 2/2638 | 0.34 pp |

## 4. Immediate escape space at the same head pressure

| Mode | Head proximity | Free neighboring cells | Death events/windows | Observed frequency |
|---|---|---|---:|---:|
| league | Opponent head ≤3 | 0-1 free sides | 18/207 | 8.70% |
| league | Opponent head ≤3 | 2-4 free sides | 40/2228 | 1.80% |
| league | Head ≥8 | 0-1 free sides | 44/1045 | 4.21% |
| league | Head ≥8 | 2-4 free sides | 29/22618 | 0.13% |
| trial | Opponent head ≤3 | 0-1 free sides | 2/36 | 5.56% |
| trial | Opponent head ≤3 | 2-4 free sides | 0/455 | 0.00% |
| trial | Head ≥8 | 0-1 free sides | 1/133 | 0.75% |
| trial | Head ≥8 | 2-4 free sides | 2/4433 | 0.05% |

This helps distinguish crowded **local geometry** from opponent-head
pressure, but is still a snapshot association, not an actual 10-turn
pathfinding or safety proof.

## 5. Palmer and other known students — descriptive exposure only

| Student | Mode | Replay matches | Sampled windows | Head ≤3 share | 0–1 free-side share | Death in next 10-turn window |
|---|---|---:|---:|---:|---:|---:|
| 421462-alexander-palmer | league | 40 | 3198 | 8.1% | 4.5% | 6/3198 |
| 421462-alexander-palmer | trial | 3 | 240 | 7.5% | 2.5% | 0/240 |
| 388060-tshepang-tshabalala | league | 13 | 1037 | 7.7% | 4.6% | 3/1037 |
| 388060-tshepang-tshabalala | trial | 2 | 160 | 8.1% | 3.1% | 0/160 |
| 428786-marvellous-sambo | league | 11 | 878 | 8.2% | 4.4% | 8/878 |
| 428786-marvellous-sambo | trial | 1 | 80 | 12.5% | 1.2% | 0/80 |
| 409997-utayan-naidoo | league | 10 | 797 | 7.2% | 4.6% | 7/797 |
| 409997-utayan-naidoo | trial | 3 | 240 | 7.1% | 2.5% | 0/240 |
| 403754-vhuimo-mudau | league | 5 | 397 | 3.8% | 6.5% | 0/397 |

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
