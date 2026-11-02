# Snake26: Do escapes stay safe for the next 20–30 turns?

Generated UTC: 2026-11-02T23:44:28+00:00

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
Files scanned: **200** / 200.
Unique replay payloads: **133** (league 71, trials 62).
Duplicate payloads: **67**.
Unreadable files: **0**.
Dangerous starting positions: **3,093**.
Silent snake disappearances censored: **0**.

## 1. Actual death-free followup
![Death-free survival by horizon](charts/danger_survival_30.svg)

| Mode | Baseline danger windows | Dead by +10 | Survived +10 | Alive at +20 after +10 (known only) | Alive at +30 after +10 (known only) | Censored before +30 |
|---|---:|---:|---:|---|---|---:|
| league | 2584 | 78 | 2506 | 2473/2506 (98.68%) | 2409/2470 (97.53%) | 36 |
| trial | 509 | 4 | 505 | 502/505 (99.41%) | 496/501 (99.00%) | 4 |

The +20 and +30 percentages condition on first-ten survival AND having
a known future outcome. Never confuse them with unconditional survival.

## 2. Does recovering an extra exit at +3 predict death in turns 11–30?
![Exit recovery versus later death](charts/escape_recovery_late_death.svg)

Analyze only snakes surviving to +10. Exits are an immediate geometry
proxy, not guaranteed legal directions or long-horizon path safety.
| Mode | +3 escape-space change | Survived first 10 | Known outcome at +30 | Dead in +11..+30 | Conditional death % | Censored |
|---|---|---:|---:|---:|---:|---:|
| league | Gained at least one exit | 960 | 939 | 15 | 1.60% | 21 |
| league | No new exit | 1546 | 1531 | 46 | 3.00% | 15 |
| trial | Gained at least one exit | 158 | 156 | 2 | 1.28% | 2 |
| trial | No new exit | 347 | 345 | 3 | 0.87% | 2 |

## 3. Match-cluster bootstrap for late death difference
Difference is exit-GAINERS minus NON-gainers, in percentage points.
Negative would favor gainers, positive would favor non-gainers.
This is observational and subject to selection and opponent confounding.

| Mode | Observed difference (percentage points) | Exploratory 95% replay-bootstrap CI | Replay clusters |
|---|---:|---:|---:|
| league | -1.41 | [-2.50, -0.36] | 71 |
| trial | 0.41 | [-1.47, 2.77] | 61 |

## 4. Palmer compared with actual students in the same league games
Unique league replays with Palmer danger windows: **18**.
These are real same-game opponent observations, but not exactly
matched head positions, lengths, or player skill.

| Role | Danger windows | Survived +10 | Known +30 after +10 | Survived +30 | Mean +3 free-exit change |
|---|---:|---:|---:|---:|---:|
| Palmer | 170 | 170 | 168 | 167 | 0.26 (n=170) |
| Other students in Palmer games | 517 | 498 | 493 | 481 | 0.35 (n=498) |

## 5. Palmer's actual decision sequences in individual league replays
Audited games in the [Palmer casebook](palmer_casebook.md): **18**.
Games with a comparable starting-danger peer in the SAME replay: **17**.
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
