# Snake26: Head pressure, escape options, and subsequent deaths

Generated UTC: 2026-11-03T07:00:07+00:00

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

- Archived files scanned: **220** of 220 candidate files.
- Unique replay payloads: **150**
(league **80**, trials **70**).
- Exact byte-identical duplicates skipped: **70**.
- Unreadable / invalid: **0**.
- Single-student league games excluded: **0**.
- Nonstandard trial rosters excluded: **0**.
- Student windows with complete follow-up: **30,966**.
- Distinct student/replay summaries: **390**.
- Latest sampled season: **2026-11-03-055900-season**.
- Latest sampled student-season with BOTH replay modes: **3**.

## 1. Head pressure and observed future death

![Pressure and 10-turn death events](charts/head_pressure_vs_death.svg)

| Environment | Nearest opponent head | Windows | Death in next 10 turns | Observed frequency | Unique replays |
|---|---|---:|---:|---:|---:|
| league | Opponent head ≤3 | 1,895 | 44 | 2.32% | 80 |
| league | Head 4–7 | 4,884 | 35 | 0.72% | 80 |
| league | Head ≥8 | 18,590 | 58 | 0.31% | 80 |
| trial | Opponent head ≤3 | 449 | 3 | 0.67% | 69 |
| trial | Head 4–7 | 1,109 | 0 | 0.00% | 70 |
| trial | Head ≥8 | 4,039 | 3 | 0.07% | 70 |

A close opponent head does NOT imply an aggressive attack or a collision.
This is a selected replay sample. Risk differences are not causal effects
and are not comparisons between equally skilled opponent populations.

## 2. Pressure vs distance alone: match-level uncertainty

- **league:** close-minus-far risk = **+2.01 percentage points**; exploratory 95% match-resampled interval **[+1.34, +2.68]**, 80 distinct replay clusters.
- **trial:** close-minus-far risk = **+0.59 percentage points**; exploratory 95% match-resampled interval **[-0.07, +1.39]**, 70 distinct replay clusters.

Resampling entire REPLAYS reduces pseudo-replication from repeated turns.
It does not adjust confounding from body length, opponent type, code
versions, player ability or game phase.

## 3. Compare danger within body-length categories

| Mode | Length | Head ≤3: death/windows | Head ≥8: death/windows | Close - far frequency |
|---|---|---:|---:|---:|
| league | 5-24 | 5/353 | 7/4104 | 1.25 pp |
| league | 25-49 | 15/365 | 10/4089 | 3.87 pp |
| league | 50-99 | 14/691 | 21/6165 | 1.69 pp |
| league | 100+ | 10/486 | 20/4232 | 1.59 pp |
| trial | 5-24 | 0/42 | 0/382 | 0.00 pp |
| trial | 25-49 | 1/73 | 0/433 | 1.37 pp |
| trial | 50-99 | 1/113 | 1/851 | 0.77 pp |
| trial | 100+ | 1/221 | 2/2373 | 0.37 pp |

## 4. Immediate escape space at the same head pressure

| Mode | Head proximity | Free neighboring cells | Death events/windows | Observed frequency |
|---|---|---|---:|---:|
| league | Opponent head ≤3 | 0-1 free sides | 16/151 | 10.60% |
| league | Opponent head ≤3 | 2-4 free sides | 28/1744 | 1.61% |
| league | Head ≥8 | 0-1 free sides | 36/807 | 4.46% |
| league | Head ≥8 | 2-4 free sides | 22/17783 | 0.12% |
| trial | Opponent head ≤3 | 0-1 free sides | 3/33 | 9.09% |
| trial | Opponent head ≤3 | 2-4 free sides | 0/416 | 0.00% |
| trial | Head ≥8 | 0-1 free sides | 1/108 | 0.93% |
| trial | Head ≥8 | 2-4 free sides | 2/3931 | 0.05% |

This helps distinguish crowded **local geometry** from opponent-head
pressure, but is still a snapshot association, not an actual 10-turn
pathfinding or safety proof.

## 5. Palmer and other known students — descriptive exposure only

| Student | Mode | Replay matches | Sampled windows | Head ≤3 share | 0–1 free-side share | Death in next 10-turn window |
|---|---|---:|---:|---:|---:|---:|
| 421462-alexander-palmer | league | 23 | 1839 | 8.2% | 4.2% | 3/1839 |
| 421462-alexander-palmer | trial | 3 | 240 | 7.5% | 2.5% | 0/240 |
| 388060-tshepang-tshabalala | league | 12 | 957 | 7.8% | 5.0% | 3/957 |
| 388060-tshepang-tshabalala | trial | 3 | 240 | 7.5% | 2.5% | 0/240 |
| 428786-marvellous-sambo | league | 8 | 639 | 7.2% | 4.4% | 4/639 |
| 428786-marvellous-sambo | trial | 1 | 80 | 12.5% | 1.2% | 0/80 |
| 409997-utayan-naidoo | league | 9 | 717 | 7.5% | 4.5% | 7/717 |
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
