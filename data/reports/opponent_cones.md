# Snake26: Opponent next-head reachability across league and trials

Generated UTC: 2026-11-03T19:59:20+00:00

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

Source replay payloads: **178**.
Danger positions: **4310**, league **3610**, trials **700**.
Unique opponent normal next-head transitions checked: **9779**.
Within predicted cone: **9779**; outside: **0**.
Dead/absent/respawned opponents excluded, not marked predicted: **23**.
League recorded head-to-head VICTIM events (all replay turns): **76**; trials **654**.
Victim events are not distinct collisions, and may lack an
identifiable opposing player. Compare last-frame lengths only:

| Last-known victim length relative to named peer | Events |
|---|---:|
| victim_shorter | 688 |
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
| league | top_quartile | 15 | 64 | 913 | 166/906 (18.3%) | 5/906 (0.6%) | 882 | 74/882 (8.4%) | 0/882 (0.0%) | 12/913 |
| league | middle_half | 37 | 68 | 1284 | 271/1266 (21.4%) | 8/1266 (0.6%) | 1205 | 82/1205 (6.8%) | 1/1205 (0.1%) | 48/1284 |
| league | bottom_quartile | 25 | 45 | 496 | 100/493 (20.3%) | 2/493 (0.4%) | 471 | 23/471 (4.9%) | 1/471 (0.2%) | 20/496 |
| league | unranked | 58 | 27 | 917 | 156/907 (17.2%) | 6/907 (0.7%) | 873 | 52/873 (6.0%) | 1/873 (0.1%) | 35/917 |
| trial | top_quartile | 10 | 18 | 139 | 34/139 (24.5%) | 2/139 (1.4%) | 139 | 15/139 (10.8%) | 0/139 (0.0%) | 1/139 |
| trial | middle_half | 12 | 17 | 169 | 25/167 (15.0%) | 1/167 (0.6%) | 161 | 16/161 (9.9%) | 0/161 (0.0%) | 1/169 |
| trial | bottom_quartile | 5 | 7 | 64 | 22/64 (34.4%) | 0/64 (0.0%) | 64 | 13/64 (20.3%) | 0/64 (0.0%) | 1/64 |
| trial | unranked | 19 | 39 | 328 | 90/327 (27.5%) | 5/327 (1.5%) | 325 | 42/325 (12.9%) | 0/325 (0.0%) | 3/328 |

### A critical sensitivity check: does a shorter-opponent opportunity exist?

The unconditional rates above MIX states where a weaker opponent
can enter a candidate destination with states having NO such option.
Define a shorter-opponent opportunity as at least one modeled
candidate cell reached by a shorter opponent's cone, but by
NO equal-or-longer opponent cone. The resulting denominator is
observed first moves WITH an actual such opportunity.

| Mode | Cohort | Mean body length (observed) | First moves with shorter-only opportunity | Chose shorter-only contest | Conditional % |
|---|---|---:|---:|---:|---:|
| league | top_quartile | 94.9 | 111 | 74 | 66.7% |
| league | middle_half | 69.8 | 123 | 81 | 65.9% |
| league | bottom_quartile | 55.2 | 30 | 22 | 73.3% |
| league | unranked | 68.8 | 73 | 51 | 69.9% |
| trial | top_quartile | 118.7 | 30 | 15 | 50.0% |
| trial | middle_half | 118.7 | 21 | 16 | 76.2% |
| trial | bottom_quartile | 105.2 | 21 | 13 | 61.9% |
| trial | unranked | 108.6 | 84 | 42 | 50.0% |

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
| 25-49 | middle_half | 14 | 13 | 92.9% |
| 25-49 | bottom_quartile | 3 | 2 | 66.7% |
| 50-99 | top_quartile | 36 | 23 | 63.9% |
| 50-99 | middle_half | 53 | 33 | 62.3% |
| 50-99 | bottom_quartile | 18 | 14 | 77.8% |
| 100+ | top_quartile | 70 | 49 | 70.0% |
| 100+ | middle_half | 51 | 32 | 62.7% |
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
| league | Current free neighboring cells | 1055 | 33 | 0.736 |
| league | Best 8-step moving-own-tail reach | 1055 | 33 | 0.857 |
| league | Modeled first steps outside all opponent cones | 1055 | 33 | 0.770 |
| league | Best tail reach outside all head cones | 1055 | 33 | 0.867 |
| league | First steps avoiding equal/longer head cones | 1055 | 33 | 0.787 |
| league | Best tail reach outside equal/longer head cones | 1055 | 33 | 0.864 |
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
| Avoid any possible head vs plain tail reach | 0.010 | [-0.004, +0.028] | 28 |
| Avoid equal/longer heads vs plain tail reach | 0.007 | [-0.000, +0.016] | 28 |
| Avoid any possible head vs free neighbors | 0.131 | [+0.070, +0.214] | 28 |

## 4. Same-game comparisons, NOT selected opponent anecdotes

Compare previous non-reused top-vs-bottom student pairs from the
SAME league replay and matched baseline length/pressure/phase.
Paired game situations with opponent cone data: **96**.
Differences below are bottom minus top. Matched situations can
still have different food, opponents or exact positions.

| State/observed behavior | Both measurable pairs | Games | Bottom minus top | 95% game interval |
|---|---:|---:|---:|---|
| Surviving first move entered possible head contest | 90 | 30 | -0.044 | [-0.131, +0.023] |
| Surviving move entered equal/longer head cone | 90 | 30 | 0.000 | [+0.000, +0.000] |
| ALL projected next cells possibly head-contested | 96 | 30 | 0.000 | [+0.000, +0.000] |

## 5. Same student/season: do league and trial styles agree?

Join by student AND season, only when each environment has at
least THREE real observed first moves from that student.
Paired student-season samples: **32**.
Spearman correlation of observed head-contest rates: **0.115** (n/a if insufficient/constant).
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
