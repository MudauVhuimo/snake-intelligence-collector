# Snake26: Head pressure, escape options, and subsequent deaths

Generated UTC: 2026-11-03T12:29:08+00:00

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

- Archived files scanned: **230** of 230 candidate files.
- Unique replay payloads: **159**
(league **85**, trials **74**).
- Exact byte-identical duplicates skipped: **71**.
- Unreadable / invalid: **0**.
- Single-student league games excluded: **0**.
- Nonstandard trial rosters excluded: **0**.
- Student windows with complete follow-up: **32,806**.
- Distinct student/replay summaries: **414**.
- Latest sampled season: **2026-11-03-115900-season**.
- Latest sampled student-season with BOTH replay modes: **3**.

## 1. Head pressure and observed future death

![Pressure and 10-turn death events](charts/head_pressure_vs_death.svg)

| Environment | Nearest opponent head | Windows | Death in next 10 turns | Observed frequency | Unique replays |
|---|---|---:|---:|---:|---:|
| league | Opponent head ≤3 | 2,029 | 48 | 2.37% | 85 |
| league | Head 4–7 | 5,143 | 38 | 0.74% | 85 |
| league | Head ≥8 | 19,717 | 59 | 0.30% | 85 |
| trial | Opponent head ≤3 | 480 | 3 | 0.62% | 73 |
| trial | Head 4–7 | 1,179 | 0 | 0.00% | 74 |
| trial | Head ≥8 | 4,258 | 3 | 0.07% | 74 |

A close opponent head does NOT imply an aggressive attack or a collision.
This is a selected replay sample. Risk differences are not causal effects
and are not comparisons between equally skilled opponent populations.

## 2. Pressure vs distance alone: match-level uncertainty

- **league:** close-minus-far risk = **+2.07 percentage points**; exploratory 95% match-resampled interval **[+1.44, +2.72]**, 85 distinct replay clusters.
- **trial:** close-minus-far risk = **+0.55 percentage points**; exploratory 95% match-resampled interval **[-0.07, +1.28]**, 74 distinct replay clusters.

Resampling entire REPLAYS reduces pseudo-replication from repeated turns.
It does not adjust confounding from body length, opponent type, code
versions, player ability or game phase.

## 3. Compare danger within body-length categories

| Mode | Length | Head ≤3: death/windows | Head ≥8: death/windows | Close - far frequency |
|---|---|---:|---:|---:|
| league | 5-24 | 5/375 | 7/4342 | 1.17 pp |
| league | 25-49 | 15/383 | 10/4309 | 3.68 pp |
| league | 50-99 | 16/745 | 22/6558 | 1.81 pp |
| league | 100+ | 12/526 | 20/4508 | 1.84 pp |
| trial | 5-24 | 0/43 | 0/405 | 0.00 pp |
| trial | 25-49 | 1/79 | 0/455 | 1.27 pp |
| trial | 50-99 | 1/120 | 1/926 | 0.73 pp |
| trial | 100+ | 1/238 | 2/2472 | 0.34 pp |

## 4. Immediate escape space at the same head pressure

| Mode | Head proximity | Free neighboring cells | Death events/windows | Observed frequency |
|---|---|---|---:|---:|
| league | Opponent head ≤3 | 0-1 free sides | 17/169 | 10.06% |
| league | Opponent head ≤3 | 2-4 free sides | 31/1860 | 1.67% |
| league | Head ≥8 | 0-1 free sides | 36/858 | 4.20% |
| league | Head ≥8 | 2-4 free sides | 23/18859 | 0.12% |
| trial | Opponent head ≤3 | 0-1 free sides | 3/37 | 8.11% |
| trial | Opponent head ≤3 | 2-4 free sides | 0/443 | 0.00% |
| trial | Head ≥8 | 0-1 free sides | 1/115 | 0.87% |
| trial | Head ≥8 | 2-4 free sides | 2/4143 | 0.05% |

This helps distinguish crowded **local geometry** from opponent-head
pressure, but is still a snapshot association, not an actual 10-turn
pathfinding or safety proof.

## 5. Palmer and other known students — descriptive exposure only

| Student | Mode | Replay matches | Sampled windows | Head ≤3 share | 0–1 free-side share | Death in next 10-turn window |
|---|---|---:|---:|---:|---:|---:|
| 421462-alexander-palmer | league | 27 | 2159 | 8.4% | 4.4% | 3/2159 |
| 421462-alexander-palmer | trial | 3 | 240 | 7.5% | 2.5% | 0/240 |
| 388060-tshepang-tshabalala | league | 12 | 957 | 7.8% | 5.0% | 3/957 |
| 388060-tshepang-tshabalala | trial | 3 | 240 | 7.5% | 2.5% | 0/240 |
| 428786-marvellous-sambo | league | 9 | 719 | 7.8% | 4.6% | 5/719 |
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
