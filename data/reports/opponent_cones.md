# Snake26: Opponent next-head reachability across league and trials

Generated UTC: 2026-11-02T16:20:25+00:00

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

Source replay payloads: **122**.
Danger positions: **2836**, league **2368**, trials **468**.
Unique opponent normal next-head transitions checked: **6474**.
Within predicted cone: **6474**; outside: **0**.
Dead/absent/respawned opponents excluded, not marked predicted: **17**.
League recorded head-to-head VICTIM events (all replay turns): **53**; trials **459**.
Victim events are not distinct collisions, and may lack an
identifiable opposing player. Compare last-frame lengths only:

| Last-known victim length relative to named peer | Events |
|---|---:|
| victim_shorter | 482 |
| equal | 30 |
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
| league | top_quartile | 14 | 40 | 533 | 102/528 (19.3%) | 4/528 (0.8%) | 511 | 47/511 (9.2%) | 0/511 (0.0%) | 7/533 |
| league | middle_half | 30 | 46 | 862 | 186/847 (22.0%) | 4/847 (0.5%) | 814 | 57/814 (7.0%) | 0/814 (0.0%) | 23/862 |
| league | bottom_quartile | 20 | 32 | 370 | 72/369 (19.5%) | 1/369 (0.3%) | 352 | 15/352 (4.3%) | 1/352 (0.3%) | 14/370 |
| league | unranked | 51 | 19 | 603 | 104/599 (17.4%) | 5/599 (0.8%) | 582 | 35/582 (6.0%) | 1/582 (0.2%) | 24/603 |
| trial | top_quartile | 7 | 14 | 93 | 20/93 (21.5%) | 2/93 (2.2%) | 93 | 8/93 (8.6%) | 0/93 (0.0%) | 1/93 |
| trial | middle_half | 4 | 8 | 78 | 12/78 (15.4%) | 0/78 (0.0%) | 74 | 7/74 (9.5%) | 0/74 (0.0%) | 0/78 |
| trial | bottom_quartile | 2 | 2 | 19 | 7/19 (36.8%) | 0/19 (0.0%) | 19 | 4/19 (21.1%) | 0/19 (0.0%) | 0/19 |
| trial | unranked | 14 | 33 | 278 | 81/277 (29.2%) | 5/277 (1.8%) | 275 | 39/275 (14.2%) | 0/275 (0.0%) | 3/278 |

### A critical sensitivity check: does a shorter-opponent opportunity exist?

The unconditional rates above MIX states where a weaker opponent
can enter a candidate destination with states having NO such option.
Define a shorter-opponent opportunity as at least one modeled
candidate cell reached by a shorter opponent's cone, but by
NO equal-or-longer opponent cone. The resulting denominator is
observed first moves WITH an actual such opportunity.

| Mode | Cohort | Mean body length (observed) | First moves with shorter-only opportunity | Chose shorter-only contest | Conditional % |
|---|---|---:|---:|---:|---:|
| league | top_quartile | 95.7 | 71 | 47 | 66.2% |
| league | middle_half | 71.3 | 88 | 57 | 64.8% |
| league | bottom_quartile | 54.5 | 19 | 14 | 73.7% |
| league | unranked | 63.3 | 48 | 34 | 70.8% |
| trial | top_quartile | 121.6 | 17 | 8 | 47.1% |
| trial | middle_half | 130.1 | 11 | 7 | 63.6% |
| trial | bottom_quartile | 158.9 | 7 | 4 | 57.1% |
| trial | unranked | 109.4 | 76 | 39 | 51.3% |

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
| 25-49 | top_quartile | 2 | 2 | 100.0% |
| 25-49 | middle_half | 7 | 7 | 100.0% |
| 25-49 | bottom_quartile | 3 | 2 | 66.7% |
| 50-99 | top_quartile | 20 | 14 | 70.0% |
| 50-99 | middle_half | 40 | 25 | 62.5% |
| 50-99 | bottom_quartile | 10 | 8 | 80.0% |
| 100+ | top_quartile | 48 | 31 | 64.6% |
| 100+ | middle_half | 36 | 22 | 61.1% |
| 100+ | bottom_quartile | 5 | 3 | 60.0% |

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
| league | Current free neighboring cells | 855 | 26 | 0.737 |
| league | Best 8-step moving-own-tail reach | 855 | 26 | 0.857 |
| league | Modeled first steps outside all opponent cones | 855 | 26 | 0.781 |
| league | Best tail reach outside all head cones | 855 | 26 | 0.870 |
| league | First steps avoiding equal/longer head cones | 855 | 26 | 0.797 |
| league | Best tail reach outside equal/longer head cones | 855 | 26 | 0.866 |
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
| Avoid any possible head vs plain tail reach | 0.013 | [-0.005, +0.038] | 22 |
| Avoid equal/longer heads vs plain tail reach | 0.009 | [-0.000, +0.019] | 22 |
| Avoid any possible head vs free neighbors | 0.133 | [+0.059, +0.223] | 22 |

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
Paired student-season samples: **14**.
Spearman correlation of observed head-contest rates: **0.232** (n/a if insufficient/constant).
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
