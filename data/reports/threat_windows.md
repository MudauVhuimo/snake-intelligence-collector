# Snake26: Head pressure, escape options, and subsequent deaths

Generated UTC: 2026-11-02T07:47:38+00:00

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

- Archived files scanned: **180** of 180 candidate files.
- Unique replay payloads: **113**
(league **59**, trials **54**).
- Exact byte-identical duplicates skipped: **67**.
- Unreadable / invalid: **0**.
- Single-student league games excluded: **0**.
- Nonstandard trial rosters excluded: **0**.
- Student windows with complete follow-up: **22,984**.
- Distinct student/replay summaries: **290**.
- Latest sampled season: **2026-11-02-045859-season**.
- Latest sampled student-season with BOTH replay modes: **0**.

## 1. Head pressure and observed future death

![Pressure and 10-turn death events](charts/head_pressure_vs_death.svg)

| Environment | Nearest opponent head | Windows | Death in next 10 turns | Observed frequency | Unique replays |
|---|---|---:|---:|---:|---:|
| league | Opponent head ≤3 | 1,446 | 31 | 2.14% | 59 |
| league | Head 4–7 | 3,694 | 25 | 0.68% | 59 |
| league | Head ≥8 | 13,527 | 39 | 0.29% | 59 |
| trial | Opponent head ≤3 | 338 | 3 | 0.89% | 53 |
| trial | Head 4–7 | 858 | 0 | 0.00% | 54 |
| trial | Head ≥8 | 3,121 | 2 | 0.06% | 54 |

A close opponent head does NOT imply an aggressive attack or a collision.
This is a selected replay sample. Risk differences are not causal effects
and are not comparisons between equally skilled opponent populations.

## 2. Pressure vs distance alone: match-level uncertainty

- **league:** close-minus-far risk = **+1.86 percentage points**; exploratory 95% match-resampled interval **[+1.16, +2.60]**, 59 distinct replay clusters.
- **trial:** close-minus-far risk = **+0.82 percentage points**; exploratory 95% match-resampled interval **[-0.06, +1.92]**, 54 distinct replay clusters.

Resampling entire REPLAYS reduces pseudo-replication from repeated turns.
It does not adjust confounding from body length, opponent type, code
versions, player ability or game phase.

## 3. Compare danger within body-length categories

| Mode | Length | Head ≤3: death/windows | Head ≥8: death/windows | Close - far frequency |
|---|---|---:|---:|---:|
| league | 5-24 | 5/286 | 5/2989 | 1.58 pp |
| league | 25-49 | 9/267 | 6/3018 | 3.17 pp |
| league | 50-99 | 10/530 | 14/4562 | 1.58 pp |
| league | 100+ | 7/363 | 14/2958 | 1.46 pp |
| trial | 5-24 | 0/32 | 0/291 | 0.00 pp |
| trial | 25-49 | 1/56 | 0/326 | 1.79 pp |
| trial | 50-99 | 1/80 | 0/637 | 1.25 pp |
| trial | 100+ | 1/170 | 2/1867 | 0.48 pp |

## 4. Immediate escape space at the same head pressure

| Mode | Head proximity | Free neighboring cells | Death events/windows | Observed frequency |
|---|---|---|---:|---:|
| league | Opponent head ≤3 | 0-1 free sides | 11/104 | 10.58% |
| league | Opponent head ≤3 | 2-4 free sides | 20/1342 | 1.49% |
| league | Head ≥8 | 0-1 free sides | 23/571 | 4.03% |
| league | Head ≥8 | 2-4 free sides | 16/12956 | 0.12% |
| trial | Opponent head ≤3 | 0-1 free sides | 3/30 | 10.00% |
| trial | Opponent head ≤3 | 2-4 free sides | 0/308 | 0.00% |
| trial | Head ≥8 | 0-1 free sides | 1/84 | 1.19% |
| trial | Head ≥8 | 2-4 free sides | 1/3037 | 0.03% |

This helps distinguish crowded **local geometry** from opponent-head
pressure, but is still a snapshot association, not an actual 10-turn
pathfinding or safety proof.

## 5. Palmer and other known students — descriptive exposure only

| Student | Mode | Replay matches | Sampled windows | Head ≤3 share | 0–1 free-side share | Death in next 10-turn window |
|---|---|---:|---:|---:|---:|---:|
| 421462-alexander-palmer | league | 17 | 1359 | 8.4% | 4.3% | 2/1359 |
| 421462-alexander-palmer | trial | 3 | 240 | 7.5% | 2.5% | 0/240 |
| 388060-tshepang-tshabalala | league | 8 | 638 | 7.4% | 4.1% | 2/638 |
| 388060-tshepang-tshabalala | trial | 3 | 240 | 7.5% | 2.5% | 0/240 |
| 428786-marvellous-sambo | league | 4 | 320 | 6.2% | 3.8% | 1/320 |
| 409997-utayan-naidoo | league | 6 | 477 | 8.6% | 3.8% | 2/477 |
| 409997-utayan-naidoo | trial | 3 | 240 | 7.1% | 2.5% | 0/240 |
| 403754-vhuimo-mudau | league | 4 | 318 | 3.1% | 6.3% | 0/318 |

These students have very different recorded sample sizes. Rows include
multiple seasons and possibly changed bot submissions. Do NOT rank their
intrinsic skill using these unadjusted exposure percentages.

## 6. Same student and season: can head-pressure behavior transfer?

Latest sampled paired-student cohort: **0**.
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
