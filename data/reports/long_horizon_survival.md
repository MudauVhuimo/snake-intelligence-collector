# Snake26: Do escapes stay safe for the next 20–30 turns?

Generated UTC: 2026-11-03T04:10:54+00:00

## Study design
Actual student replay frames are sampled every 25 turns when the nearest
opponent head is within three toroidal cells OR the snake has at most one
unoccupied neighboring square. We distinguish league peers from fixed
benchmark trials and deduplicate replay payloads by SHA-256.
A recorded death event is FAILURE even if the snake later respawns.
A missing frame or unexplained disappearance is CENSORED, never safe.
Outcomes are death-free through +10, +20 or +30 turns. Since +30
covers longer than the 25-turn sampling stride, windows from the same
snake and match can overlap; resample entire replay clusters.

## Data quality
Files scanned: **210** / 210.
Unique replay payloads: **141** (league 75, trials 66).
Duplicate payloads: **69**.
Unreadable files: **0**.
Dangerous starting positions: **3,301**.
Silent snake disappearances censored: **0**.

## 1. Actual death-free followup
![Death-free survival by horizon](charts/danger_survival_30.svg)

| Mode | Baseline danger windows | Dead by +10 | Survived +10 | Alive at +20 after +10 (known only) | Alive at +30 after +10 (known only) | Censored before +30 |
|---|---:|---:|---:|---|---|---:|
| league | 2745 | 85 | 2660 | 2625/2660 (98.68%) | 2561/2624 (97.60%) | 36 |
| trial | 556 | 4 | 552 | 548/552 (99.28%) | 542/548 (98.91%) | 4 |

The +20 and +30 percentages condition on first-ten survival AND having
a known future outcome. Never confuse them with unconditional survival.

## 2. Does recovering an extra exit at +3 predict death in turns 11–30?
![Exit recovery versus later death](charts/escape_recovery_late_death.svg)

Analyze only snakes surviving to +10. Exits are an immediate geometry
proxy, not guaranteed legal directions or long-horizon path safety.
| Mode | +3 escape-space change | Survived first 10 | Known outcome at +30 | Dead in +11..+30 | Conditional death % | Censored |
|---|---|---:|---:|---:|---:|---:|
| league | Gained at least one exit | 1026 | 1005 | 15 | 1.49% | 21 |
| league | No new exit | 1634 | 1619 | 48 | 2.96% | 15 |
| trial | Gained at least one exit | 175 | 173 | 2 | 1.16% | 2 |
| trial | No new exit | 377 | 375 | 4 | 1.07% | 2 |

## 3. Match-cluster bootstrap for late death difference
Difference is exit-GAINERS minus NON-gainers, in percentage points.
Negative would favor gainers, positive would favor non-gainers.
This is observational and subject to selection and opponent confounding.

| Mode | Observed difference (percentage points) | Exploratory 95% replay-bootstrap CI | Replay clusters |
|---|---:|---:|---:|
| league | -1.47 | [-2.49, -0.43] | 75 |
| trial | 0.09 | [-1.66, 2.45] | 65 |

## 4. Palmer compared with actual students in the same league games
Unique league replays with Palmer danger windows: **22**.
These are real same-game opponent observations, but not exactly
matched head positions, lengths, or player skill.

| Role | Danger windows | Survived +10 | Known +30 after +10 | Survived +30 | Mean +3 free-exit change |
|---|---:|---:|---:|---:|---:|
| Palmer | 206 | 206 | 204 | 203 | 0.31 (n=206) |
| Other students in Palmer games | 642 | 616 | 611 | 597 | 0.36 (n=616) |

## 5. Palmer's actual decision sequences in individual league replays
Audited games in the [Palmer casebook](palmer_casebook.md): **22**.
Games with a comparable starting-danger peer in the SAME replay: **21**.
The casebook exposes actual movement direction and straight-versus-turn
choice plus neighboring-space, head-distance and food observations
through turns +1, +3, +10, +20 and +30 where recorded.
We select the earliest qualifying danger in each replay, never
cherry-pick a successful later move.
[Open Palmer's complete observed casebook](palmer_casebook.md).

## 6. Interpretation and next experiment
A successful first escape does not guarantee another twenty safe turns.
Early mobility recovery and late survival can be associated without
the move CAUSING survival. Conditioning on +10 survival selects a
nonrandom subset of snakes; initial body geometry, head trajectories,
apples, opponent strength and season/version remain confounders.
Next, investigate close-call turns with head direction, legal move
options and contested food in the SAME games. Only then consider
testing candidate policy changes on held-out seeds.

## Auditable observations
[Censor-aware 10/20/30-turn danger windows](../derived/long_horizon_danger_windows.csv).
[Matched real escape/autopsy report](escape_autopsies.md).
[Canonical joined league/trial dashboard](joint_analysis.md).

**No Java competition snake code was changed.**
