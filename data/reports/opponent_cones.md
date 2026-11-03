# Snake26: Opponent next-head reachability across league and trials

Generated UTC: 2026-11-03T15:24:17+00:00

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

Source replay payloads: **168**.
Danger positions: **4049**, league **3389**, trials **660**.
Unique opponent normal next-head transitions checked: **9181**.
Within predicted cone: **9181**; outside: **0**.
Dead/absent/respawned opponents excluded, not marked predicted: **23**.
League recorded head-to-head VICTIM events (all replay turns): **73**; trials **629**.
Victim events are not distinct collisions, and may lack an
identifiable opposing player. Compare last-frame lengths only:

| Last-known victim length relative to named peer | Events |
|---|---:|
| victim_shorter | 660 |
| equal | 42 |
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
| league | top_quartile | 15 | 60 | 838 | 151/831 (18.2%) | 5/831 (0.6%) | 809 | 66/809 (8.2%) | 0/809 (0.0%) | 12/838 |
| league | middle_half | 37 | 64 | 1230 | 256/1212 (21.1%) | 8/1212 (0.7%) | 1156 | 79/1156 (6.8%) | 1/1156 (0.1%) | 45/1230 |
| league | bottom_quartile | 25 | 43 | 480 | 97/477 (20.3%) | 2/477 (0.4%) | 455 | 22/455 (4.8%) | 1/455 (0.2%) | 19/480 |
| league | unranked | 56 | 25 | 841 | 135/832 (16.2%) | 5/832 (0.6%) | 805 | 46/805 (5.7%) | 1/805 (0.1%) | 32/841 |
| trial | top_quartile | 10 | 18 | 139 | 34/139 (24.5%) | 2/139 (1.4%) | 139 | 15/139 (10.8%) | 0/139 (0.0%) | 1/139 |
| trial | middle_half | 11 | 15 | 149 | 23/148 (15.5%) | 1/148 (0.7%) | 142 | 15/142 (10.6%) | 0/142 (0.0%) | 0/149 |
| trial | bottom_quartile | 5 | 6 | 53 | 20/53 (37.7%) | 0/53 (0.0%) | 53 | 12/53 (22.6%) | 0/53 (0.0%) | 1/53 |
| trial | unranked | 18 | 38 | 319 | 89/318 (28.0%) | 5/318 (1.6%) | 316 | 42/316 (13.3%) | 0/316 (0.0%) | 3/319 |

### A critical sensitivity check: does a shorter-opponent opportunity exist?

The unconditional rates above MIX states where a weaker opponent
can enter a candidate destination with states having NO such option.
Define a shorter-opponent opportunity as at least one modeled
candidate cell reached by a shorter opponent's cone, but by
NO equal-or-longer opponent cone. The resulting denominator is
observed first moves WITH an actual such opportunity.

| Mode | Cohort | Mean body length (observed) | First moves with shorter-only opportunity | Chose shorter-only contest | Conditional % |
|---|---|---:|---:|---:|---:|
| league | top_quartile | 96.9 | 102 | 66 | 64.7% |
| league | middle_half | 69.9 | 118 | 78 | 66.1% |
| league | bottom_quartile | 54.7 | 29 | 21 | 72.4% |
| league | unranked | 68.5 | 64 | 45 | 70.3% |
| trial | top_quartile | 118.7 | 30 | 15 | 50.0% |
| trial | middle_half | 119.5 | 20 | 15 | 75.0% |
| trial | bottom_quartile | 108.7 | 20 | 12 | 60.0% |
| trial | unranked | 109.9 | 83 | 42 | 50.6% |

The top group may encounter MORE weaker opponents because its snakes
are already longer. Conditional rates can erase or reverse the
apparent top/middle/bottom trend. An observed shorter-only contest
is not necessarily deliberate aggression or an advantageous action.
Still excludes immediate deaths because their attempted destinations
are not present in next-frame surviving heads.

### Further stratification by length in REAL league matches

| Length at danger position | Cohort | Observed first moves with shorter-only option | Chose it | Rate |
|---|---|---:|---:|---:|
| 5-24 | top_quartile | 1 | 0 | 0.0% |
| 5-24 | middle_half | 5 | 3 | 60.0% |
| 5-24 | bottom_quartile | 1 | 1 | 100.0% |
| 25-49 | top_quartile | 4 | 2 | 50.0% |
| 25-49 | middle_half | 12 | 11 | 91.7% |
| 25-49 | bottom_quartile | 3 | 2 | 66.7% |
| 50-99 | top_quartile | 32 | 20 | 62.5% |
| 50-99 | middle_half | 51 | 33 | 64.7% |
| 50-99 | bottom_quartile | 17 | 13 | 76.5% |
| 100+ | top_quartile | 65 | 44 | 67.7% |
| 100+ | middle_half | 50 | 31 | 62.0% |
| 100+ | bottom_quartile | 8 | 5 | 62.5% |

These strata are small and not exact-matched relative-length or
opponent-heading contexts; do NOT extrapolate a universal
size-based offensive rule.

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
| league | Current free neighboring cells | 1024 | 32 | 0.743 |
| league | Best 8-step moving-own-tail reach | 1024 | 32 | 0.872 |
| league | Modeled first steps outside all opponent cones | 1024 | 32 | 0.781 |
| league | Best tail reach outside all head cones | 1024 | 32 | 0.882 |
| league | First steps avoiding equal/longer head cones | 1024 | 32 | 0.797 |
| league | Best tail reach outside equal/longer head cones | 1024 | 32 | 0.879 |
| trial | Current free neighboring cells | 127 | 0 | insufficient |
| trial | Best 8-step moving-own-tail reach | 127 | 0 | insufficient |
| trial | Modeled first steps outside all opponent cones | 127 | 0 | insufficient |
| trial | Best tail reach outside all head cones | 127 | 0 | insufficient |
| trial | First steps avoiding equal/longer head cones | 127 | 0 | insufficient |
| trial | Best tail reach outside equal/longer head cones | 127 | 0 | insufficient |

### Match-cluster uncertainty for league predictor differences

Bootstrap complete REPLAYS, never independently resample hundreds
of overlapping turns. These exploratory intervals also inherit
possible bot-version/season dependence and selection from the
previous research archive. If an interval spans 0, no superiority
is established.

| Same held-out league observations | AUC difference | Exploratory 95% replay interval | Matches |
|---|---:|---|---:|
| Avoid any possible head vs plain tail reach | 0.010 | [-0.004, +0.030] | 27 |
| Avoid equal/longer heads vs plain tail reach | 0.007 | [-0.000, +0.015] | 27 |
| Avoid any possible head vs free neighbors | 0.139 | [+0.077, +0.213] | 27 |

## 4. Same-game comparisons, NOT selected opponent anecdotes

Compare previous non-reused top-vs-bottom student pairs from the
SAME league replay and matched baseline length/pressure/phase.
Paired game situations with opponent cone data: **90**.
Differences below are bottom minus top. Matched situations can
still have different food, opponents or exact positions.

| State/observed behavior | Both measurable pairs | Games | Bottom minus top | 95% game interval |
|---|---:|---:|---:|---|
| Surviving first move entered possible head contest | 84 | 28 | -0.048 | [-0.135, +0.025] |
| Surviving move entered equal/longer head cone | 84 | 28 | 0.000 | [+0.000, +0.000] |
| ALL projected next cells possibly head-contested | 90 | 28 | 0.000 | [+0.000, +0.000] |

## 5. Same student/season: do league and trial styles agree?

Join by student AND season, only when each environment has at
least THREE real observed first moves from that student.
Paired student-season samples: **29**.
Spearman correlation of observed head-contest rates: **0.201** (n/a if insufficient/constant).
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
