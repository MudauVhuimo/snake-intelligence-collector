# Snake26: JOINED league + trials study

Generated UTC: 2026-11-03T15:24:21+00:00

**Latest official season:** 2026-11-03-145900-season. This report treats competitive league
matches and controlled on-arrival trials as **two separate datasets**
and joins them at the **same season + same student**. The published
end-of-season code SHA, when known, is attached for auditing, but is
**not proof that every match in that season used that exact code version**.

## 1. Data provenance and cleaning

**Source of truth:** official public Wits catalog records in the SQLite archive.

| Separate data source | Cataloged matches | Full replays | Unique replay hashes |
|---|---:|---:|---:|
| League | 8,371 | 149 | 91 |
| Trial | 54,978 | 91 | 78 |

**Historical student-season rows:** league 6,610,
trials 18,326, union 18,351.
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
| Apples per game | 32 | 0.453 | [+0.130, +0.683] |
| Final body length | 32 | 0.332 | [-0.045, +0.624] |
| Kills per game | 32 | 0.141 | [-0.289, +0.533] |
| Retained growth / expected no-reset growth | 32 | 0.471 | [+0.152, +0.715] |

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
| 1 | 421462-alexander-palmer | 3 | 66.7 | 34.0 | 0.70 | 1.00 | 48.0 | 0.79 | 15.33 | 3/0 |
| 2 | 427064-khodani-netili | 4 | 50.0 | 26.0 | 0.76 | 0.75 | 42.0 | 1.00 | 11.33 | 2/1 |
| 3 | 424820-elisha-mundalamo | 5 | 40.0 | 33.4 | 0.50 | 1.00 | 40.3 | 0.95 | 13.33 | 0/0 |
| 4 | 388828-ngcebo-methula | 5 | 60.0 | 30.4 | 0.59 | 1.00 | 40.0 | 1.00 | 14.67 | 0/0 |
| 5 | 413538-lelethuthando-nikelo | 5 | 40.0 | 29.4 | 0.76 | 1.20 | 43.3 | 1.00 | 22.33 | 1/0 |
| 6 | 419342-ayeshan-puckree | 4 | 50.0 | 30.5 | 0.89 | 1.25 | 32.0 | 1.00 | 12.33 | 1/0 |
| 7 | 428786-marvellous-sambo | 5 | 20.0 | 29.0 | 0.46 | 0.40 | 34.7 | 0.70 | 16.00 | 0/0 |
| 8 | 404721-khensani-maluleke | 6 | 50.0 | 33.3 | 0.58 | 1.17 | 45.0 | 0.43 | 13.00 | 1/0 |
| 9 | 419926-mphile-nchabeleng | 5 | 60.0 | 29.2 | 0.73 | 1.20 | 35.0 | 1.00 | 14.00 | 0/0 |
| 10 | 426895-mpho-ramasakona | 6 | 33.3 | 26.5 | 0.30 | 1.33 | 40.7 | 0.54 | 15.67 | 0/0 |
| 11 | 426650-babongile-mafantiri | 6 | 33.3 | 29.8 | 0.31 | 0.83 | 32.7 | 1.00 | 20.33 | 0/0 |
| 12 | 421349-phathutshedzo-mudzanani | 4 | 25.0 | 28.8 | 0.34 | 1.25 | 43.7 | 0.95 | 10.33 | 0/0 |
| 13 | 388060-tshepang-tshabalala | 6 | 33.3 | 31.5 | 0.25 | 0.33 | 44.7 | 1.00 | 15.00 | 0/0 |
| 14 | 423239-zeeshaan-bham | 6 | 16.7 | 35.7 | 0.49 | 1.17 | 41.0 | 1.00 | 13.33 | 2/0 |
| 15 | 410193-vhugala-makhwathane | 6 | 33.3 | 26.3 | 0.66 | 3.67 | 27.0 | 1.00 | 8.67 | 0/0 |
| 16 | 409997-utayan-naidoo | 5 | 60.0 | 31.4 | 0.54 | 1.20 | 48.7 | 0.77 | 10.67 | 0/0 |
| 17 | 427039-sameeha-miabala | 5 | 0.0 | 26.4 | 0.69 | 1.00 | 38.7 | 1.00 | 14.33 | 0/0 |
| 18 | 408501-asher-urison | 5 | 0.0 | 28.0 | 0.38 | 1.00 | 38.3 | 0.70 | 8.00 | 1/0 |
| 19 | 429782-maseeha-seedat | 6 | 16.7 | 29.2 | 0.32 | 2.83 | 37.3 | 0.79 | 12.33 | 0/0 |
| 20 | 423436-ntobeko-zondi | 4 | 25.0 | 29.0 | 0.47 | 0.75 | 31.7 | 1.00 | 10.00 | 2/0 |
| 21 | 423258-muhammed-dar | 4 | 25.0 | 31.2 | 0.61 | 1.00 | 48.3 | 0.22 | 11.33 | 1/1 |
| 22 | 403339-david-ndambo | 6 | 33.3 | 29.2 | 0.70 | 1.33 | 41.3 | 1.00 | 12.67 | 0/0 |
| 23 | 402334-angile-saho | 5 | 40.0 | 29.4 | 0.59 | 2.40 | 46.3 | 1.00 | 23.33 | 0/0 |
| 24 | 406000-mulimisi-rammela | 4 | 0.0 | 21.8 | 0.82 | 1.25 | 25.0 | 1.00 | 12.00 | 0/0 |
| 25 | 428954-njabulo-ndlozi | 6 | 16.7 | 26.0 | 0.24 | 3.17 | 37.3 | 0.75 | 17.00 | 0/0 |
| 26 | 389160-lwandle-ramanugu | 4 | 0.0 | 22.0 | 0.29 | 0.25 | 38.0 | 0.54 | 17.33 | 0/0 |
| 27 | 403501-mashau-mudzanani | 5 | 0.0 | 34.2 | 0.16 | 0.20 | 41.3 | 0.75 | 8.33 | 1/1 |
| 28 | 421538-tshifhiwa-bvumbi | 5 | 0.0 | 29.6 | 0.26 | 0.00 | 42.3 | 1.00 | 15.67 | 0/0 |
| 29 | 419222-asisipho-ngaba | 6 | 0.0 | 27.3 | 0.23 | 0.83 | 41.3 | 0.64 | 11.67 | 0/0 |
| 30 | 408070-collen-mthombeni | 5 | 0.0 | 29.2 | 0.38 | 0.00 | 42.3 | 0.50 | 4.67 | 1/0 |
| 31 | 424907-sibongakonke-ntsele | 5 | 0.0 | 25.6 | 0.17 | 0.40 | 36.7 | 0.62 | 8.00 | 0/0 |
| 32 | 423158-risima-mashele | 4 | 25.0 | 24.2 | 0.36 | 0.50 | 41.7 | 0.78 | 11.33 | 0/0 |

## 5. The same students: *actual replay-derived* behavior

Current-season students with BOTH league and trial full replay behavior: **3**.
Catalog counts cannot fill in missing replay decisions; only identical,
verifiable frame-derived definitions can be compared across modes.
[See the mode-separated behavioral report](behavior_by_mode.md) for
observed food-event/death rates and their conditional correlations.
![Student food events per observed move in each mode](charts/observed_food_by_mode.svg)
![Student deaths per observed move in each mode](charts/observed_deaths_by_mode.svg)
### Forward-looking head pressure and escape space
Unique replays with complete frame-based pressure analysis: **169**
(league **91**, trial **78**).
Measure danger BEFORE the outcome: each living student's nearest
opponent head, free adjacent cells, then death events in the NEXT
ten turns. See [head-pressure and escape study](threat_windows.md)
for length-stratified results, per-replay counts and uncertainty.
![10-turn death frequencies by head proximity](charts/head_pressure_vs_death.svg)
### Matched death autopsies versus observed 10-turn escapes
League death cases paired to real survivors: **108**.
On-arrival trial death cases paired separately: **5**.
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
Same-season ranked league danger windows: **2,548**.
![League and trial cohorts by danger response](charts/cohort_danger_outcomes.svg)
### Which actual first moves preserve usable future space?
The [route-space investigation](route_space.md) contrasts frozen
flood-fill with an 8-step simulated moving-own-tail continuation for
EACH alternative first move, then measures the actual chosen action.
The model freezes opponents and assumes no growth; its routes are
NOT engine-verified safe paths or counterfactual outcomes.
Replay-sampled danger positions with route features: **4049**.
![Recorded high-route-space first moves by cohort](charts/route_choice_cohorts.svg)
### Which first steps could become opponent head contests?
The [whole-field head-cone analysis](opponent_cones.md) models all
opponents' next-head REACHABLE cells from current geometry, compares
them with each alternative route and audits real next-frame
moves and head-to-head victim events. Separate league and trial
outcomes remain visible; these are NOT verified engine-legal moves.
Actual league danger positions with cone features: **3389**.
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

Historical Division 1 snapshots with matched outcome comparisons: **11**.
We rank the same eligible students within each official division and
season, then compare league versus trial percentiles. Repeated hourly
snapshots are correlated and do not form independent experiments.
[Open the historical disagreement study](seasonal_disagreement.md).
![Historical rank agreement](charts/historical_rank_alignment.svg)
![Students specializing in league or trials](charts/league_trial_outliers.svg)

## 7. Older seasons with actual peer games but no saved standings

Historical seasons comparable by match-derived Division 1 outcomes: **123** snapshots.
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
