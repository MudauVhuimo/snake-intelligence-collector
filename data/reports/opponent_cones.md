# Snake26: Opponent next-head reachability across league and trials

Generated UTC: 2026-11-03T07:01:18+00:00

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

Source replay payloads: **149**.
Danger positions: **3531**, league **2943**, trials **588**.
Unique opponent normal next-head transitions checked: **8035**.
Within predicted cone: **8035**; outside: **0**.
Dead/absent/respawned opponents excluded, not marked predicted: **21**.
League recorded head-to-head VICTIM events (all replay turns): **63**; trials **568**.
Victim events are not distinct collisions, and may lack an
identifiable opposing player. Compare last-frame lengths only:

| Last-known victim length relative to named peer | Events |
|---|---:|
| victim_shorter | 595 |
| equal | 36 |
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
| league | top_quartile | 15 | 52 | 690 | 126/683 (18.4%) | 5/683 (0.7%) | 665 | 57/665 (8.6%) | 0/665 (0.0%) | 10/690 |
| league | middle_half | 35 | 56 | 1074 | 226/1057 (21.4%) | 6/1057 (0.6%) | 1011 | 69/1011 (6.8%) | 1/1011 (0.1%) | 39/1074 |
| league | bottom_quartile | 23 | 40 | 458 | 91/455 (20.0%) | 2/455 (0.4%) | 436 | 22/436 (5.0%) | 1/436 (0.2%) | 18/458 |
| league | unranked | 54 | 22 | 721 | 113/715 (15.8%) | 5/715 (0.7%) | 694 | 39/694 (5.6%) | 1/694 (0.1%) | 26/721 |
| trial | top_quartile | 10 | 17 | 128 | 31/128 (24.2%) | 2/128 (1.6%) | 128 | 14/128 (10.9%) | 0/128 (0.0%) | 1/128 |
| trial | middle_half | 8 | 12 | 121 | 18/121 (14.9%) | 0/121 (0.0%) | 116 | 12/116 (10.3%) | 0/116 (0.0%) | 0/121 |
| trial | bottom_quartile | 4 | 4 | 35 | 11/35 (31.4%) | 0/35 (0.0%) | 35 | 8/35 (22.9%) | 0/35 (0.0%) | 0/35 |
| trial | unranked | 16 | 36 | 304 | 84/303 (27.7%) | 5/303 (1.7%) | 301 | 42/301 (14.0%) | 0/301 (0.0%) | 3/304 |

### A critical sensitivity check: does a shorter-opponent opportunity exist?

The unconditional rates above MIX states where a weaker opponent
can enter a candidate destination with states having NO such option.
Define a shorter-opponent opportunity as at least one modeled
candidate cell reached by a shorter opponent's cone, but by
NO equal-or-longer opponent cone. The resulting denominator is
observed first moves WITH an actual such opportunity.

| Mode | Cohort | Mean body length (observed) | First moves with shorter-only opportunity | Chose shorter-only contest | Conditional % |
|---|---|---:|---:|---:|---:|
| league | top_quartile | 95.8 | 87 | 57 | 65.5% |
| league | middle_half | 70.8 | 104 | 68 | 65.4% |
| league | bottom_quartile | 55.2 | 27 | 21 | 77.8% |
| league | unranked | 67.3 | 53 | 38 | 71.7% |
| trial | top_quartile | 118.0 | 27 | 14 | 51.9% |
| trial | middle_half | 120.8 | 16 | 12 | 75.0% |
| trial | bottom_quartile | 122.1 | 11 | 8 | 72.7% |
| trial | unranked | 109.8 | 79 | 42 | 53.2% |

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
| 25-49 | middle_half | 10 | 9 | 90.0% |
| 25-49 | bottom_quartile | 3 | 2 | 66.7% |
| 50-99 | top_quartile | 27 | 19 | 70.4% |
| 50-99 | middle_half | 44 | 28 | 63.6% |
| 50-99 | bottom_quartile | 16 | 13 | 81.2% |
| 100+ | top_quartile | 56 | 36 | 64.3% |
| 100+ | middle_half | 45 | 28 | 62.2% |
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
| league | Current free neighboring cells | 990 | 32 | 0.746 |
| league | Best 8-step moving-own-tail reach | 990 | 32 | 0.873 |
| league | Modeled first steps outside all opponent cones | 990 | 32 | 0.783 |
| league | Best tail reach outside all head cones | 990 | 32 | 0.883 |
| league | First steps avoiding equal/longer head cones | 990 | 32 | 0.800 |
| league | Best tail reach outside equal/longer head cones | 990 | 32 | 0.880 |
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
| Avoid any possible head vs plain tail reach | 0.010 | [-0.004, +0.029] | 26 |
| Avoid equal/longer heads vs plain tail reach | 0.007 | [-0.000, +0.015] | 26 |
| Avoid any possible head vs free neighbors | 0.137 | [+0.074, +0.206] | 26 |

## 4. Same-game comparisons, NOT selected opponent anecdotes

Compare previous non-reused top-vs-bottom student pairs from the
SAME league replay and matched baseline length/pressure/phase.
Paired game situations with opponent cone data: **88**.
Differences below are bottom minus top. Matched situations can
still have different food, opponents or exact positions.

| State/observed behavior | Both measurable pairs | Games | Bottom minus top | 95% game interval |
|---|---:|---:|---:|---|
| Surviving first move entered possible head contest | 83 | 27 | -0.048 | [-0.141, +0.030] |
| Surviving move entered equal/longer head cone | 83 | 27 | 0.000 | [+0.000, +0.000] |
| ALL projected next cells possibly head-contested | 88 | 27 | 0.000 | [+0.000, +0.000] |

## 5. Same student/season: do league and trial styles agree?

Join by student AND season, only when each environment has at
least THREE real observed first moves from that student.
Paired student-season samples: **23**.
Spearman correlation of observed head-contest rates: **0.214** (n/a if insufficient/constant).
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
