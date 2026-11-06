# Snake26: Opponent next-head reachability across league and trials

Generated UTC: 2026-11-06T11:08:58+00:00

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

Source replay payloads: **180**.
Danger positions: **4451**, league **3789**, trials **662**.
Unique opponent normal next-head transitions checked: **10065**.
Within predicted cone: **10065**; outside: **0**.
Dead/absent/respawned opponents excluded, not marked predicted: **21**.
League recorded head-to-head VICTIM events (all replay turns): **77**; trials **646**.
Victim events are not distinct collisions, and may lack an
identifiable opposing player. Compare last-frame lengths only:

| Last-known victim length relative to named peer | Events |
|---|---:|
| victim_shorter | 685 |
| equal | 38 |
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
| league | top_quartile | 17 | 68 | 979 | 175/971 (18.0%) | 6/971 (0.6%) | 943 | 76/943 (8.1%) | 0/943 (0.0%) | 14/979 |
| league | middle_half | 39 | 72 | 1333 | 280/1314 (21.3%) | 8/1314 (0.6%) | 1251 | 89/1251 (7.1%) | 1/1251 (0.1%) | 49/1333 |
| league | bottom_quartile | 27 | 48 | 533 | 107/530 (20.2%) | 2/530 (0.4%) | 504 | 25/504 (5.0%) | 1/504 (0.2%) | 22/533 |
| league | unranked | 58 | 28 | 944 | 160/934 (17.1%) | 6/934 (0.6%) | 900 | 52/900 (5.8%) | 1/900 (0.1%) | 35/944 |
| trial | top_quartile | 12 | 21 | 158 | 38/158 (24.1%) | 2/158 (1.3%) | 158 | 17/158 (10.8%) | 0/158 (0.0%) | 1/158 |
| trial | middle_half | 12 | 17 | 169 | 25/167 (15.0%) | 1/167 (0.6%) | 161 | 16/161 (9.9%) | 0/161 (0.0%) | 1/169 |
| trial | bottom_quartile | 5 | 7 | 64 | 22/64 (34.4%) | 0/64 (0.0%) | 64 | 13/64 (20.3%) | 0/64 (0.0%) | 1/64 |
| trial | unranked | 19 | 33 | 271 | 78/271 (28.8%) | 5/271 (1.8%) | 271 | 36/271 (13.3%) | 0/271 (0.0%) | 1/271 |

### A critical sensitivity check: does a shorter-opponent opportunity exist?

The unconditional rates above MIX states where a weaker opponent
can enter a candidate destination with states having NO such option.
Define a shorter-opponent opportunity as at least one modeled
candidate cell reached by a shorter opponent's cone, but by
NO equal-or-longer opponent cone. The resulting denominator is
observed first moves WITH an actual such opportunity.

| Mode | Cohort | Mean body length (observed) | First moves with shorter-only opportunity | Chose shorter-only contest | Conditional % |
|---|---|---:|---:|---:|---:|
| league | top_quartile | 94.8 | 114 | 76 | 66.7% |
| league | middle_half | 69.9 | 130 | 88 | 67.7% |
| league | bottom_quartile | 55.5 | 33 | 24 | 72.7% |
| league | unranked | 68.7 | 75 | 51 | 68.0% |
| trial | top_quartile | 121.5 | 34 | 17 | 50.0% |
| trial | middle_half | 118.7 | 21 | 16 | 76.2% |
| trial | bottom_quartile | 105.2 | 21 | 13 | 61.9% |
| trial | unranked | 106.5 | 73 | 36 | 49.3% |

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
| 25-49 | top_quartile | 5 | 2 | 40.0% |
| 25-49 | middle_half | 14 | 13 | 92.9% |
| 25-49 | bottom_quartile | 3 | 2 | 66.7% |
| 50-99 | top_quartile | 36 | 23 | 63.9% |
| 50-99 | middle_half | 58 | 38 | 65.5% |
| 50-99 | bottom_quartile | 20 | 16 | 80.0% |
| 100+ | top_quartile | 72 | 51 | 70.8% |
| 100+ | middle_half | 53 | 34 | 64.2% |
| 100+ | bottom_quartile | 9 | 5 | 55.6% |

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
| league | Current free neighboring cells | 1101 | 35 | 0.742 |
| league | Best 8-step moving-own-tail reach | 1101 | 35 | 0.864 |
| league | Modeled first steps outside all opponent cones | 1101 | 35 | 0.772 |
| league | Best tail reach outside all head cones | 1101 | 35 | 0.873 |
| league | First steps avoiding equal/longer head cones | 1101 | 35 | 0.791 |
| league | Best tail reach outside equal/longer head cones | 1101 | 35 | 0.870 |
| trial | Current free neighboring cells | 131 | 0 | insufficient |
| trial | Best 8-step moving-own-tail reach | 131 | 0 | insufficient |
| trial | Modeled first steps outside all opponent cones | 131 | 0 | insufficient |
| trial | Best tail reach outside all head cones | 131 | 0 | insufficient |
| trial | First steps avoiding equal/longer head cones | 131 | 0 | insufficient |
| trial | Best tail reach outside equal/longer head cones | 131 | 0 | insufficient |

### Match-cluster uncertainty for league predictor differences

Bootstrap complete REPLAYS, never independently resample hundreds
of overlapping turns. These exploratory intervals also inherit
possible bot-version/season dependence and selection from the
previous research archive. If an interval spans 0, no superiority
is established.

| Same held-out league observations | AUC difference | Exploratory 95% replay interval | Matches |
|---|---:|---|---:|
| Avoid any possible head vs plain tail reach | 0.009 | [-0.004, +0.028] | 29 |
| Avoid equal/longer heads vs plain tail reach | 0.006 | [-0.000, +0.015] | 29 |
| Avoid any possible head vs free neighbors | 0.131 | [+0.076, +0.201] | 29 |

## 4. Same-game comparisons, NOT selected opponent anecdotes

Compare previous non-reused top-vs-bottom student pairs from the
SAME league replay and matched baseline length/pressure/phase.
Paired game situations with opponent cone data: **109**.
Differences below are bottom minus top. Matched situations can
still have different food, opponents or exact positions.

| State/observed behavior | Both measurable pairs | Games | Bottom minus top | 95% game interval |
|---|---:|---:|---:|---|
| Surviving first move entered possible head contest | 101 | 33 | -0.030 | [-0.112, +0.033] |
| Surviving move entered equal/longer head cone | 101 | 33 | 0.000 | [+0.000, +0.000] |
| ALL projected next cells possibly head-contested | 109 | 33 | 0.000 | [+0.000, +0.000] |

## 5. Same student/season: do league and trial styles agree?

Join by student AND season, only when each environment has at
least THREE real observed first moves from that student.
Paired student-season samples: **35**.
Spearman correlation of observed head-contest rates: **0.171** (n/a if insufficient/constant).
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
