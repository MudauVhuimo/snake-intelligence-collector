# Snake26: Opponent next-head reachability across league and trials

Generated UTC: 2026-11-03T04:11:32+00:00

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

Source replay payloads: **140**.
Danger positions: **3301**, league **2745**, trials **556**.
Unique opponent normal next-head transitions checked: **7534**.
Within predicted cone: **7534**; outside: **0**.
Dead/absent/respawned opponents excluded, not marked predicted: **18**.
League recorded head-to-head VICTIM events (all replay turns): **60**; trials **529**.
Victim events are not distinct collisions, and may lack an
identifiable opposing player. Compare last-frame lengths only:

| Last-known victim length relative to named peer | Events |
|---|---:|
| victim_shorter | 557 |
| equal | 32 |
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
| league | top_quartile | 15 | 48 | 632 | 120/625 (19.2%) | 5/625 (0.8%) | 608 | 55/608 (9.0%) | 0/608 (0.0%) | 9/632 |
| league | middle_half | 35 | 53 | 1012 | 211/996 (21.2%) | 5/996 (0.5%) | 950 | 63/950 (6.6%) | 0/950 (0.0%) | 33/1012 |
| league | bottom_quartile | 21 | 37 | 410 | 86/408 (21.1%) | 2/408 (0.5%) | 390 | 20/390 (5.1%) | 1/390 (0.3%) | 17/410 |
| league | unranked | 53 | 21 | 691 | 110/686 (16.0%) | 5/686 (0.7%) | 666 | 37/666 (5.6%) | 1/666 (0.2%) | 26/691 |
| trial | top_quartile | 9 | 16 | 118 | 27/118 (22.9%) | 2/118 (1.7%) | 118 | 12/118 (10.2%) | 0/118 (0.0%) | 1/118 |
| trial | middle_half | 7 | 11 | 110 | 16/110 (14.5%) | 0/110 (0.0%) | 105 | 10/105 (9.5%) | 0/105 (0.0%) | 0/110 |
| trial | bottom_quartile | 3 | 3 | 27 | 11/27 (40.7%) | 0/27 (0.0%) | 27 | 8/27 (29.6%) | 0/27 (0.0%) | 0/27 |
| trial | unranked | 15 | 35 | 301 | 84/300 (28.0%) | 5/300 (1.7%) | 298 | 42/298 (14.1%) | 0/298 (0.0%) | 3/301 |

### A critical sensitivity check: does a shorter-opponent opportunity exist?

The unconditional rates above MIX states where a weaker opponent
can enter a candidate destination with states having NO such option.
Define a shorter-opponent opportunity as at least one modeled
candidate cell reached by a shorter opponent's cone, but by
NO equal-or-longer opponent cone. The resulting denominator is
observed first moves WITH an actual such opportunity.

| Mode | Cohort | Mean body length (observed) | First moves with shorter-only opportunity | Chose shorter-only contest | Conditional % |
|---|---|---:|---:|---:|---:|
| league | top_quartile | 95.9 | 85 | 55 | 64.7% |
| league | middle_half | 71.0 | 96 | 63 | 65.6% |
| league | bottom_quartile | 54.2 | 24 | 19 | 79.2% |
| league | unranked | 66.5 | 51 | 36 | 70.6% |
| trial | top_quartile | 117.7 | 23 | 12 | 52.2% |
| trial | middle_half | 120.5 | 14 | 10 | 71.4% |
| trial | bottom_quartile | 143.0 | 11 | 8 | 72.7% |
| trial | unranked | 109.9 | 79 | 42 | 53.2% |

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
| 25-49 | top_quartile | 3 | 2 | 66.7% |
| 25-49 | middle_half | 8 | 8 | 100.0% |
| 25-49 | bottom_quartile | 3 | 2 | 66.7% |
| 50-99 | top_quartile | 25 | 17 | 68.0% |
| 50-99 | middle_half | 42 | 26 | 61.9% |
| 50-99 | bottom_quartile | 13 | 11 | 84.6% |
| 100+ | top_quartile | 56 | 36 | 64.3% |
| 100+ | middle_half | 41 | 26 | 63.4% |
| 100+ | bottom_quartile | 7 | 5 | 71.4% |

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
| league | Current free neighboring cells | 958 | 32 | 0.746 |
| league | Best 8-step moving-own-tail reach | 958 | 32 | 0.873 |
| league | Modeled first steps outside all opponent cones | 958 | 32 | 0.782 |
| league | Best tail reach outside all head cones | 958 | 32 | 0.883 |
| league | First steps avoiding equal/longer head cones | 958 | 32 | 0.799 |
| league | Best tail reach outside equal/longer head cones | 958 | 32 | 0.880 |
| trial | Current free neighboring cells | 117 | 0 | insufficient |
| trial | Best 8-step moving-own-tail reach | 117 | 0 | insufficient |
| trial | Modeled first steps outside all opponent cones | 117 | 0 | insufficient |
| trial | Best tail reach outside all head cones | 117 | 0 | insufficient |
| trial | First steps avoiding equal/longer head cones | 117 | 0 | insufficient |
| trial | Best tail reach outside equal/longer head cones | 117 | 0 | insufficient |

### Match-cluster uncertainty for league predictor differences

Bootstrap complete REPLAYS, never independently resample hundreds
of overlapping turns. These exploratory intervals also inherit
possible bot-version/season dependence and selection from the
previous research archive. If an interval spans 0, no superiority
is established.

| Same held-out league observations | AUC difference | Exploratory 95% replay interval | Matches |
|---|---:|---|---:|
| Avoid any possible head vs plain tail reach | 0.010 | [-0.004, +0.033] | 25 |
| Avoid equal/longer heads vs plain tail reach | 0.007 | [-0.000, +0.017] | 25 |
| Avoid any possible head vs free neighbors | 0.137 | [+0.069, +0.208] | 25 |

## 4. Same-game comparisons, NOT selected opponent anecdotes

Compare previous non-reused top-vs-bottom student pairs from the
SAME league replay and matched baseline length/pressure/phase.
Paired game situations with opponent cone data: **71**.
Differences below are bottom minus top. Matched situations can
still have different food, opponents or exact positions.

| State/observed behavior | Both measurable pairs | Games | Bottom minus top | 95% game interval |
|---|---:|---:|---:|---|
| Surviving first move entered possible head contest | 67 | 24 | -0.075 | [-0.152, -0.015] |
| Surviving move entered equal/longer head cone | 67 | 24 | 0.000 | [+0.000, +0.000] |
| ALL projected next cells possibly head-contested | 71 | 24 | 0.000 | [+0.000, +0.000] |

## 5. Same student/season: do league and trial styles agree?

Join by student AND season, only when each environment has at
least THREE real observed first moves from that student.
Paired student-season samples: **20**.
Spearman correlation of observed head-contest rates: **0.180** (n/a if insufficient/constant).
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
