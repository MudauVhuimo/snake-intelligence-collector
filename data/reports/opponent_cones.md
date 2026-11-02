# Snake26: Opponent next-head reachability across league and trials

Generated UTC: 2026-11-02T08:40:29+00:00

## What was tested

For every actual dangerous student position, derive all opponent
one-step head destinations from current head and neck on the
toroidal board. With a known heading, exclude immediate reversal;
otherwise include all four cardinal neighbors. No occupancy filter
is applied to opponents, so these sets are geometric UPPER BOUNDS,
not legal moves, probabilistic predictions or certain deaths.
Equal/longer CURRENT opponent length is a separate descriptive flag.
We have not imported collision rules from earlier Wits Snake games.

League is the competitive target. Trial benchmark observations are
shown in separate rows. Rankings come from the corresponding
official student league season; all students are included.
New candidates are NOT built or modified by this investigation.

## 1. Transition verification and actual head-on death records

Source replay payloads: **112**.
Danger positions: **2637**, league **2196**, trials **441**.
Unique opponent normal next-head transitions checked: **6006**.
Within predicted cone: **6006**; outside: **0**.
Dead/absent/respawned opponents excluded, not marked predicted: **15**.
League recorded head-to-head VICTIM events (all replay turns): **45**; trials **427**.
Victim events are not distinct collisions, and may lack an
identifiable opposing player. Compare last-frame lengths only:

| Last-known victim length relative to named peer | Events |
|---|---:|
| victim_shorter | 444 |
| equal | 28 |
| victim_longer | 0 |
| missing_participant | 0 |
| missing_prior_frame | 0 |

Do NOT infer official 2026 head-on resolution solely from these
events; cause attribution, concurrent deaths, growth and missing
peer IDs can complicate interpretation.

## 2. How do strong, average and struggling snakes encounter cones?

![Observed student first moves into possible opponent head cells](charts/opponent_contests.svg)

| Mode | League performance group | Students | Games | Danger windows | Frames with ≥1 contested alternative | ALL alternatives contested | Observed first moves | Observed move into cone | Into equal/longer cone | Death by +10 |
|---|---|---:|---:|---:|---|---|---:|---|---|---|
| league | top_quartile | 13 | 37 | 486 | 92/481 (19.1%) | 4/481 (0.8%) | 465 | 45/465 (9.7%) | 0/465 (0.0%) | 5/486 |
| league | middle_half | 29 | 42 | 807 | 174/794 (21.9%) | 4/794 (0.5%) | 763 | 50/763 (6.6%) | 0/763 (0.0%) | 22/807 |
| league | bottom_quartile | 20 | 32 | 370 | 72/369 (19.5%) | 1/369 (0.3%) | 352 | 15/352 (4.3%) | 1/352 (0.3%) | 14/370 |
| league | unranked | 48 | 16 | 533 | 89/529 (16.8%) | 3/529 (0.6%) | 518 | 28/518 (5.4%) | 1/518 (0.2%) | 22/533 |
| trial | top_quartile | 5 | 12 | 81 | 18/81 (22.2%) | 2/81 (2.5%) | 81 | 7/81 (8.6%) | 0/81 (0.0%) | 1/81 |
| trial | middle_half | 4 | 8 | 78 | 12/78 (15.4%) | 0/78 (0.0%) | 74 | 7/74 (9.5%) | 0/74 (0.0%) | 0/78 |
| trial | bottom_quartile | 1 | 1 | 8 | 2/8 (25.0%) | 0/8 (0.0%) | 8 | 2/8 (25.0%) | 0/8 (0.0%) | 0/8 |
| trial | unranked | 13 | 32 | 274 | 80/273 (29.3%) | 5/273 (1.8%) | 271 | 39/271 (14.4%) | 0/271 (0.0%) | 3/274 |

SELECTION WARNING: observed first moves require a live head at t+1.
Snakes killed on their first step have NO recorded destination;
observed contested-move shares thus CANNOT estimate how dangerous
contested choices are. Pre-action cone exposure includes those deaths.

## 3. Predictive value on held-out actual league games

For each PRE-action feature, higher values mean more modeled safe
options and are negated to rank actual recorded death within 10 turns.
Use the SAME SHA-based entire-replay holdout as our route-space study.
ROC AUC = 0.5 chance ranking; 1.0 perfect separation. AUC is not
a calibrated risk or evidence of a better agent.

| Match mode | Pre-action feature | Holdout windows | Death events | AUC |
|---|---|---:|---:|---:|
| league | Current free neighboring cells | 760 | 23 | 0.734 |
| league | Best 8-step moving-own-tail reach | 760 | 23 | 0.864 |
| league | Modeled first steps outside all opponent cones | 760 | 23 | 0.785 |
| league | Best tail reach outside all head cones | 760 | 23 | 0.879 |
| league | First steps avoiding equal/longer head cones | 760 | 23 | 0.799 |
| league | Best tail reach outside equal/longer head cones | 760 | 23 | 0.874 |
| trial | Current free neighboring cells | 106 | 0 | insufficient |
| trial | Best 8-step moving-own-tail reach | 106 | 0 | insufficient |
| trial | Modeled first steps outside all opponent cones | 106 | 0 | insufficient |
| trial | Best tail reach outside all head cones | 106 | 0 | insufficient |
| trial | First steps avoiding equal/longer head cones | 106 | 0 | insufficient |
| trial | Best tail reach outside equal/longer head cones | 106 | 0 | insufficient |

### Match-cluster uncertainty for league predictor differences

Bootstrap complete REPLAYS, never independently resample hundreds
of overlapping turns. These exploratory intervals also inherit
possible bot-version/season dependence and selection from the
previous research archive. If an interval spans 0, no superiority
is established.

| Same held-out league observations | AUC difference | Exploratory 95% replay interval | Matches |
|---|---:|---|---:|
| Avoid any possible head vs plain tail reach | 0.015 | [-0.004, +0.040] | 19 |
| Avoid equal/longer heads vs plain tail reach | 0.010 | [-0.000, +0.021] | 19 |
| Avoid any possible head vs free neighbors | 0.146 | [+0.061, +0.233] | 19 |

## 4. Same-game comparisons, NOT selected opponent anecdotes

Compare previous non-reused top-vs-bottom student pairs from the
SAME league replay and matched baseline length/pressure/phase.
Paired game situations with opponent cone data: **66**.
Differences below are bottom minus top. Matched situations can
still have different food, opponents or exact positions.

| State/observed behavior | Both measurable pairs | Games | Bottom minus top | 95% game interval |
|---|---:|---:|---:|---|
| Surviving first move entered possible head contest | 62 | 20 | -0.081 | [-0.161, -0.017] |
| Surviving move entered equal/longer head cone | 62 | 20 | 0.000 | [+0.000, +0.000] |
| ALL projected next cells possibly head-contested | 66 | 20 | 0.000 | [+0.000, +0.000] |

## 5. Same student/season: do league and trial styles agree?

Join by student AND season, only when each environment has at
least THREE real observed first moves from that student.
Paired student-season samples: **12**.
Spearman correlation of observed head-contest rates: **0.457** (n/a if insufficient/constant).
With so few and sometimes repeated submitted versions, this is
not evidence of causal cross-environment transfer.
[Underlying paired-student rows](../derived/opponent_cone_paired_students.csv).

## 6. Hypothesis for the NEW algorithm, awaiting falsification

A route may be spacious yet exposed to several possible opponent
next-head locations. A candidate future policy could trade off
accessible area against prospective head conflicts, but no
specific weights, cutoffs or opponent probabilities are approved.
Next we need current 2026 head-to-head mechanics from engine source
or unambiguous events, and a test that uses moving opponents and
actual apple-contest behavior. Held-out diverse-opponent ablations
must precede promotion of any rule.

## Auditable data

- [Source frame-based first moves and pre-action cone features](../derived/route_choice_windows.csv).
- [Cohort rates](../derived/opponent_cone_cohorts.csv).
- [Head-event and transition audit counts](../derived/route_cone_quality.json).
- [Paired student/season comparisons](../derived/opponent_cone_paired_students.csv).
- [Underlying dynamic-space report](route_space.md).

**No Java competition snake code was touched.**
