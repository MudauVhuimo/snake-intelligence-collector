# Snake26: JOINED league + trials study

Generated UTC: 2026-11-02T23:45:16+00:00

**Latest official season:** 2026-11-02-225901-season. This report treats competitive league
matches and controlled on-arrival trials as **two separate datasets**
and joins them at the **same season + same student**. The published
end-of-season code SHA, when known, is attached for auditing, but is
**not proof that every match in that season used that exact code version**.

## 1. Data provenance and cleaning

**Source of truth:** official public Wits catalog records in the SQLite archive.

| Separate data source | Cataloged matches | Full replays | Unique replay hashes |
|---|---:|---:|---:|
| League | 4,995 | 125 | 71 |
| Trial | 36,015 | 75 | 62 |

**Historical student-season rows:** league 3,846,
trials 12,005, union 12,026.
**Current season paired students (at least 2 student-opponent league games
plus all 3 trials): 147**.
**Division 1 study sample (at least 3 league games + all trials): 32**.

Important: a cataloged game is not automatically a recorded full replay.
We do not estimate actions, decisions, deaths or attack policy from aggregate
placements. Identical SHA replay payloads are counted separately in catalog
coverage but not as independent unique recordings.
**Possible mechanics/data inconsistencies** (final length larger than
5 + 5 times apples) among student-game observations: 0.
Investigate any nonzero cases before interpreting reset behavior.

## 2. Correlations between SAME students in both environments

![Joined correlations](charts/joint_correlations.svg)

| Paired measurement | Division 1 students | Spearman rho | Exploratory 95% paired-student bootstrap interval |
|---|---:|---:|---:|
| Apples per game | 32 | 0.441 | [+0.088, +0.716] |
| Final body length | 32 | 0.273 | [-0.068, +0.546] |
| Kills per game | 32 | 0.340 | [-0.046, +0.673] |
| Retained growth / expected no-reset growth | 32 | 0.214 | [-0.098, +0.522] |

Correlations are calculated only among students from **the same division
and season**, to avoid comparing ranks of different divisions. These are
within-student comparisons across distinct conditions—not claims that
one environment causes performance in the other.
The exploratory 95% percentile intervals resample complete paired STUDENTS
(2,000 draws per metric), not frames or individual games. They do NOT
adjust for league schedule differences, opponent difficulty, code changes
or selection bias. This is one time-specific Division 1 cohort.

## 3. Compare actual outcomes side by side

![Same students: food acquisition](charts/joint_apples.svg)

![Same students: length retained](charts/joint_length.svg)

![Same students: kills](charts/joint_kills.svg)

![Same students: retention ratio](charts/joint_retention.svg)

Every dot represents one matched student-season. The x-axis is the
three-trial average; y-axis is the actual league average against
at least two student opponents. Trial seeds are fixed, while league
match opponents, seats and seeds vary by schedule.

## 4. Current Division 1: actual joined rows

| Rank | Student | League games | League wins % | League apples | League retained | League kills | Trial apples | Trial retained | Trial kills | Replay coverage L/T |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 421349-phathutshedzo-mudzanani | 4 | 75.0 | 32.8 | 0.55 | 0.25 | 43.7 | 0.95 | 10.33 | 4/0 |
| 2 | 424820-elisha-mundalamo | 6 | 50.0 | 29.7 | 0.58 | 1.50 | 40.3 | 0.95 | 13.33 | 0/0 |
| 3 | 421462-alexander-palmer | 4 | 50.0 | 33.0 | 0.85 | 0.50 | 48.0 | 0.79 | 15.33 | 0/0 |
| 4 | 427039-sameeha-miabala | 6 | 50.0 | 32.3 | 0.43 | 0.83 | 38.7 | 1.00 | 14.33 | 0/0 |
| 5 | 388828-ngcebo-methula | 6 | 66.7 | 30.2 | 0.63 | 0.50 | 40.0 | 1.00 | 14.67 | 0/0 |
| 6 | 413538-lelethuthando-nikelo | 4 | 25.0 | 33.8 | 0.48 | 1.75 | 43.3 | 1.00 | 22.33 | 0/0 |
| 7 | 403339-david-ndambo | 6 | 50.0 | 28.2 | 0.63 | 0.50 | 41.3 | 1.00 | 12.67 | 0/0 |
| 8 | 419926-mphile-nchabeleng | 3 | 33.3 | 29.0 | 0.63 | 0.00 | 35.0 | 1.00 | 14.00 | 0/0 |
| 9 | 423239-zeeshaan-bham | 6 | 33.3 | 31.7 | 0.51 | 0.83 | 41.0 | 1.00 | 13.33 | 2/1 |
| 10 | 408501-asher-urison | 5 | 20.0 | 24.8 | 0.62 | 0.20 | 38.3 | 0.70 | 8.00 | 0/0 |
| 11 | 404721-khensani-maluleke | 6 | 16.7 | 32.7 | 0.52 | 0.33 | 45.0 | 0.43 | 13.00 | 0/0 |
| 12 | 410193-vhugala-makhwathane | 6 | 16.7 | 26.2 | 0.64 | 3.67 | 27.0 | 1.00 | 8.67 | 0/0 |
| 13 | 388060-tshepang-tshabalala | 5 | 40.0 | 28.6 | 0.33 | 0.40 | 44.7 | 1.00 | 15.00 | 1/0 |
| 14 | 427064-khodani-netili | 5 | 40.0 | 27.4 | 0.89 | 1.60 | 42.0 | 1.00 | 11.33 | 0/0 |
| 15 | 408070-collen-mthombeni | 5 | 40.0 | 26.8 | 0.69 | 0.60 | 42.3 | 0.50 | 4.67 | 0/0 |
| 16 | 421538-tshifhiwa-bvumbi | 4 | 50.0 | 31.8 | 0.64 | 0.75 | 42.3 | 1.00 | 15.67 | 0/0 |
| 17 | 428786-marvellous-sambo | 4 | 25.0 | 28.8 | 0.64 | 0.75 | 34.7 | 0.70 | 16.00 | 1/0 |
| 18 | 426895-mpho-ramasakona | 5 | 0.0 | 28.4 | 0.30 | 0.40 | 40.7 | 0.54 | 15.67 | 0/0 |
| 19 | 419222-asisipho-ngaba | 4 | 25.0 | 24.2 | 0.35 | 1.25 | 41.3 | 0.64 | 11.67 | 1/0 |
| 20 | 402334-angile-saho | 6 | 16.7 | 27.5 | 0.51 | 4.17 | 46.3 | 1.00 | 23.33 | 0/0 |
| 21 | 406000-mulimisi-rammela | 5 | 20.0 | 20.0 | 1.00 | 0.60 | 25.0 | 1.00 | 12.00 | 1/1 |
| 22 | 427417-phophi-shavhani | 5 | 0.0 | 28.4 | 0.41 | 2.20 | 44.0 | 0.40 | 10.00 | 2/0 |
| 23 | 409997-utayan-naidoo | 5 | 20.0 | 32.0 | 0.24 | 0.40 | 48.7 | 0.77 | 10.67 | 0/0 |
| 24 | 426650-babongile-mafantiri | 4 | 25.0 | 25.2 | 0.33 | 1.25 | 32.7 | 1.00 | 20.33 | 0/0 |
| 25 | 408008-bradley-buys | 6 | 16.7 | 23.7 | 0.51 | 1.00 | 42.0 | 0.76 | 16.67 | 2/1 |
| 26 | 420285-kgotlelelo-aphane | 6 | 16.7 | 31.3 | 0.15 | 0.33 | 42.7 | 0.85 | 7.00 | 0/0 |
| 27 | 428954-njabulo-ndlozi | 5 | 0.0 | 34.8 | 0.21 | 0.20 | 37.3 | 0.75 | 17.00 | 0/0 |
| 28 | 407318-deo-kabunda | 6 | 0.0 | 27.8 | 0.27 | 0.00 | 35.7 | 1.00 | 7.33 | 0/0 |
| 29 | 423436-ntobeko-zondi | 5 | 0.0 | 27.4 | 0.58 | 0.20 | 31.7 | 1.00 | 10.00 | 0/0 |
| 30 | 423258-muhammed-dar | 5 | 0.0 | 34.8 | 0.45 | 0.40 | 48.3 | 0.22 | 11.33 | 1/0 |
| 31 | 419342-ayeshan-puckree | 4 | 0.0 | 33.0 | 0.37 | 0.00 | 32.0 | 1.00 | 12.33 | 1/0 |
| 32 | 428798-oratile-molefe | 4 | 0.0 | 23.0 | 0.22 | 0.00 | 31.3 | 0.54 | 8.33 | 0/0 |

## 5. The same students: *actual replay-derived* behavior

Current-season students with BOTH league and trial full replay behavior: **3**.
Catalog counts cannot fill in missing replay decisions; only identical,
verifiable frame-derived definitions can be compared across modes.
[See the mode-separated behavioral report](behavior_by_mode.md) for
observed food-event/death rates and their conditional correlations.
![Student food events per observed move in each mode](charts/observed_food_by_mode.svg)
![Student deaths per observed move in each mode](charts/observed_deaths_by_mode.svg)
### Forward-looking head pressure and escape space
Unique replays with complete frame-based pressure analysis: **133**
(league **71**, trial **62**).
Measure danger BEFORE the outcome: each living student's nearest
opponent head, free adjacent cells, then death events in the NEXT
ten turns. See [head-pressure and escape study](threat_windows.md)
for length-stratified results, per-replay counts and uncertainty.
![10-turn death frequencies by head proximity](charts/head_pressure_vs_death.svg)
### Matched death autopsies versus observed 10-turn escapes
League death cases paired to real survivors: **78**.
On-arrival trial death cases paired separately: **3**.
[Explore actual first-turn escape movement](escape_autopsies.md),
matching on initial length, head proximity, and available neighboring
cells. Later-turn comparisons exclude early deaths and are subject
to survivorship selection, not a proof of causal protection.
![Matched death versus escape movements](charts/escape_case_control.svg)
### Research-to-algorithm decision registry
Our [falsifiable rulebook](algorithm_rulebook.md) tracks
**8 proposed state-to-action hypotheses** with
supporting studies, counterexamples and required validation.
NO observational rule is automatically promoted into the new agent.
### All competitors: strong, middle, and struggling league cohorts
[Compare all three performance cohorts](competitive_cohorts.md)
using official standings from the SAME replay season, with body-length
and danger-state common-support checks. Palmer and the submitted
snake are ordinary members of their cohorts, not a head-to-head.
Same-season ranked league danger windows: **1,893**.
![League and trial cohorts by danger response](charts/cohort_danger_outcomes.svg)
### Which actual first moves preserve usable future space?
The [route-space investigation](route_space.md) contrasts frozen
flood-fill with an 8-step simulated moving-own-tail continuation for
EACH alternative first move, then measures the actual chosen action.
The model freezes opponents and assumes no growth; its routes are
NOT engine-verified safe paths or counterfactual outcomes.
Replay-sampled danger positions with route features: **3093**.
![Recorded high-route-space first moves by cohort](charts/route_choice_cohorts.svg)
### Which first steps could become opponent head contests?
The [whole-field head-cone analysis](opponent_cones.md) models all
opponents' next-head REACHABLE cells from current geometry, compares
them with each alternative route and audits real next-frame
moves and head-to-head victim events. Separate league and trial
outcomes remain visible; these are NOT verified engine-legal moves.
Actual league danger positions with cone features: **2584**.
![Observed head-contest choices by group](charts/opponent_contests.svg)
### Does the snake remain safe after its first escape?
[Palmer's audited danger-response casebook](palmer_casebook.md) gives
one earliest dangerous position per unique league replay and
the actual head movements, local exits, opponent distances and apples.
The [10/20/30-turn survival analysis](long_horizon_survival.md) checks
recorded deaths after danger, treats respawns as failures, and
censors missing future frames. It also compares Palmer with actual
students in his archived league games, not benchmark opponents.
![Death-free +10 and conditional +30 outcomes](charts/danger_survival_30.svg)
![Early recovered free cells versus late deaths](charts/escape_recovery_late_death.svg)

## 6. Longitudinal disagreement: league specialists vs trial specialists

Historical Division 1 snapshots with matched outcome comparisons: **7**.
We rank the same eligible students within each official division and
season, then compare league versus trial percentiles. Repeated hourly
snapshots are correlated and do not form independent experiments.
[Open the historical disagreement study](seasonal_disagreement.md).
![Historical rank agreement](charts/historical_rank_alignment.svg)
![Students specializing in league or trials](charts/league_trial_outliers.svg)

## 7. Older seasons with actual peer games but no saved standings

Historical seasons comparable by match-derived Division 1 outcomes: **80** snapshots.
This study uses cataloged student-versus-student placements when old
OFFICIAL rankings were not archived. These are explicitly labeled
match-derived outcomes, never represented as official league rank.
[Open historical peer-game versus trial results](historical_peer_comparison.md).
![Old league match outcomes and trial growth](charts/historical_peer_vs_trial.svg)

## 8. Reproducible joined data exports

- [League team-season summaries](../derived/league_team_seasons.csv) —
  the real competition outcomes, including human-opponent counts.
- [Trial team-season summaries](../derived/trial_team_seasons.csv) —
  three controlled benchmark setups, kept separate.
- [Joined student-season dataset](../derived/joined_team_seasons.csv) —
  one row per student and season; missing sides are **missing**, not zero.
- [Historical game-based peer performance comparisons](../derived/historical_peer_trial_correlations.csv) —
  actual archived matches; does NOT imply missing official rank.
- [Historical league–trial student rank gaps](../derived/seasonal_rank_gaps.csv) —
  comparable within-division student-season ranks; snapshots not independent.
- [Danger follow-ups (10/20/30 turns)](../derived/long_horizon_danger_windows.csv) —
  death-event validated, with right-censoring and actual +3 actions.
- [Matched death/survival replay observations](../derived/escape_matched_pairs.csv) —
  baseline-matched cases and real early turn trajectories.
- [Head-pressure and local-exit exposures](../derived/threat_window_student_seasons.csv) —
  sampled from actual replay frames, with next-10-turn outcomes.
- [Replay-backed behavior, separated by mode](../derived/replay_behavior_by_mode.csv) —
  only downloaded full match observations.
- [Data validation summary](../derived/quality.json) —
  replay coverage, SHA deduplication and sample sizes.

## 9. What needs further evidence

1. Obtain full league replays of top Division 1 students, including both
   winners and losers, and map their exact turns/deaths/food contests.
2. Run the **same replay-derived definitions** separately on league and
   on-arrival data: food pursuit, death risk, contest pressure and mobility.
3. Compare like-for-like length, turn phase, opponent skill and version.
4. Group uncertainty by complete match/season, not thousands of turns.
5. Interpret only held-out, version-aware patterns before changing our snake.

This joined report establishes observational associations, not an optimal
aggression/safety formula. No competition snake code has been modified.
