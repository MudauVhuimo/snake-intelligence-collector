# Snake26: JOINED league + trials study

Generated UTC: 2026-11-06T11:09:02+00:00

**Latest official season:** 2026-11-06-102324-season. This report treats competitive league
matches and controlled on-arrival trials as **two separate datasets**
and joins them at the **same season + same student**. The published
end-of-season code SHA, when known, is attached for auditing, but is
**not proof that every match in that season used that exact code version**.

## 1. Data provenance and cleaning

**Source of truth:** official public Wits catalog records in the SQLite archive.

| Separate data source | Cataloged matches | Full replays | Unique replay hashes |
|---|---:|---:|---:|
| League | 10,155 | 161 | 102 |
| Trial | 65,538 | 99 | 86 |

**Historical student-season rows:** league 8,126,
trials 21,846, union 21,874.
**Current season paired students (at least 2 student-opponent league games
plus all 3 trials): 168**.
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
| Apples per game | 32 | 0.605 | [+0.296, +0.812] |
| Final body length | 32 | 0.207 | [-0.177, +0.543] |
| Kills per game | 32 | 0.240 | [-0.124, +0.563] |
| Retained growth / expected no-reset growth | 32 | 0.233 | [-0.111, +0.533] |

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
| 1 | 421462-alexander-palmer | 4 | 75.0 | 36.0 | 0.80 | 1.50 | 48.0 | 0.79 | 15.33 | 4/0 |
| 2 | 420790-damian-nel | 6 | 66.7 | 30.8 | 0.77 | 2.00 | 37.7 | 1.00 | 19.00 | 1/1 |
| 3 | 427039-sameeha-miabala | 5 | 60.0 | 31.6 | 0.50 | 1.60 | 38.7 | 1.00 | 14.33 | 1/1 |
| 4 | 424283-mmathabo-riba | 5 | 60.0 | 31.0 | 0.51 | 0.40 | 39.0 | 1.00 | 9.33 | 1/1 |
| 5 | 424820-elisha-mundalamo | 5 | 40.0 | 31.2 | 0.89 | 0.60 | 38.3 | 1.00 | 10.67 | 0/0 |
| 6 | 408501-asher-urison | 5 | 20.0 | 26.0 | 0.51 | 0.40 | 38.3 | 0.70 | 8.00 | 0/0 |
| 7 | 413538-lelethuthando-nikelo | 6 | 50.0 | 29.5 | 0.62 | 5.00 | 43.3 | 1.00 | 22.33 | 0/0 |
| 8 | 404721-khensani-maluleke | 6 | 50.0 | 33.2 | 0.42 | 0.17 | 45.0 | 0.43 | 13.00 | 0/0 |
| 9 | 410193-vhugala-makhwathane | 6 | 33.3 | 26.7 | 0.43 | 1.00 | 47.3 | 0.41 | 10.33 | 0/0 |
| 10 | 408070-collen-mthombeni | 6 | 16.7 | 28.2 | 0.49 | 2.33 | 42.3 | 0.50 | 4.67 | 0/0 |
| 11 | 423436-ntobeko-zondi | 5 | 20.0 | 22.6 | 0.71 | 1.00 | 36.3 | 1.00 | 23.33 | 0/0 |
| 12 | 408797-linathi-nomazele | 5 | 20.0 | 25.2 | 0.49 | 0.40 | 39.7 | 1.00 | 10.67 | 0/0 |
| 13 | 427064-khodani-netili | 6 | 33.3 | 29.8 | 0.66 | 0.50 | 42.0 | 1.00 | 11.33 | 1/0 |
| 14 | 403339-david-ndambo | 5 | 40.0 | 28.4 | 0.61 | 0.20 | 41.3 | 1.00 | 12.67 | 0/0 |
| 15 | 388828-ngcebo-methula | 5 | 40.0 | 28.8 | 0.59 | 0.20 | 40.0 | 1.00 | 14.67 | 0/0 |
| 16 | 419926-mphile-nchabeleng | 6 | 16.7 | 27.5 | 0.51 | 0.50 | 35.0 | 1.00 | 14.00 | 0/0 |
| 17 | 426895-mpho-ramasakona | 6 | 16.7 | 28.7 | 0.52 | 0.67 | 40.7 | 0.54 | 15.67 | 1/0 |
| 18 | 423239-zeeshaan-bham | 5 | 40.0 | 25.2 | 0.34 | 0.20 | 41.0 | 1.00 | 13.33 | 1/0 |
| 19 | 421349-phathutshedzo-mudzanani | 4 | 50.0 | 31.2 | 0.68 | 0.50 | 43.7 | 0.95 | 10.33 | 0/0 |
| 20 | 406000-mulimisi-rammela | 5 | 20.0 | 22.6 | 0.70 | 3.00 | 25.0 | 1.00 | 12.00 | 0/0 |
| 21 | 403501-mashau-mudzanani | 5 | 0.0 | 36.8 | 0.16 | 0.40 | 41.3 | 0.75 | 8.33 | 0/0 |
| 22 | 388060-tshepang-tshabalala | 5 | 0.0 | 25.6 | 0.91 | 0.40 | 41.7 | 0.71 | 13.00 | 0/0 |
| 23 | 423258-muhammed-dar | 6 | 0.0 | 31.2 | 0.27 | 0.83 | 48.3 | 0.22 | 11.33 | 0/0 |
| 24 | 424251-thandolwethu-zondi | 5 | 0.0 | 33.6 | 0.31 | 0.40 | 50.7 | 0.44 | 9.33 | 2/0 |
| 25 | 419342-ayeshan-puckree | 5 | 20.0 | 25.0 | 0.37 | 0.20 | 32.0 | 1.00 | 12.33 | 0/0 |
| 26 | 428786-marvellous-sambo | 5 | 0.0 | 31.4 | 0.49 | 0.60 | 34.7 | 0.70 | 16.00 | 0/0 |
| 27 | 402334-angile-saho | 6 | 0.0 | 32.2 | 0.16 | 1.33 | 48.0 | 0.79 | 19.33 | 1/0 |
| 28 | 409987-sbongakonke-shange | 5 | 0.0 | 22.6 | 0.42 | 0.00 | 39.7 | 1.00 | 12.67 | 0/0 |
| 29 | 429782-maseeha-seedat | 6 | 0.0 | 26.8 | 0.54 | 2.50 | 37.3 | 0.79 | 12.33 | 0/0 |
| 30 | 422453-mauricetshepo-frost | 6 | 16.7 | 34.8 | 0.09 | 1.33 | 48.7 | 1.00 | 26.00 | 0/0 |
| 31 | 429653-elohim-mahungele | 6 | 16.7 | 23.7 | 0.30 | 0.33 | 32.7 | 1.00 | 18.00 | 3/0 |
| 32 | 426650-babongile-mafantiri | 6 | 0.0 | 24.5 | 0.44 | 0.67 | 32.7 | 1.00 | 20.33 | 0/0 |

## 5. The same students: *actual replay-derived* behavior

Current-season students with BOTH league and trial full replay behavior: **3**.
Catalog counts cannot fill in missing replay decisions; only identical,
verifiable frame-derived definitions can be compared across modes.
[See the mode-separated behavioral report](behavior_by_mode.md) for
observed food-event/death rates and their conditional correlations.
![Student food events per observed move in each mode](charts/observed_food_by_mode.svg)
![Student deaths per observed move in each mode](charts/observed_deaths_by_mode.svg)
### Forward-looking head pressure and escape space
Unique replays with complete frame-based pressure analysis: **181**
(league **102**, trial **79**).
Measure danger BEFORE the outcome: each living student's nearest
opponent head, free adjacent cells, then death events in the NEXT
ten turns. See [head-pressure and escape study](threat_windows.md)
for length-stratified results, per-replay counts and uncertainty.
![10-turn death frequencies by head proximity](charts/head_pressure_vs_death.svg)
### Matched death autopsies versus observed 10-turn escapes
League death cases paired to real survivors: **120**.
On-arrival trial death cases paired separately: **4**.
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
Same-season ranked league danger windows: **2,845**.
![League and trial cohorts by danger response](charts/cohort_danger_outcomes.svg)
### Which actual first moves preserve usable future space?
The [route-space investigation](route_space.md) contrasts frozen
flood-fill with an 8-step simulated moving-own-tail continuation for
EACH alternative first move, then measures the actual chosen action.
The model freezes opponents and assumes no growth; its routes are
NOT engine-verified safe paths or counterfactual outcomes.
Replay-sampled danger positions with route features: **4451**.
![Recorded high-route-space first moves by cohort](charts/route_choice_cohorts.svg)
### Which first steps could become opponent head contests?
The [whole-field head-cone analysis](opponent_cones.md) models all
opponents' next-head REACHABLE cells from current geometry, compares
them with each alternative route and audits real next-frame
moves and head-to-head victim events. Separate league and trial
outcomes remain visible; these are NOT verified engine-legal moves.
Actual league danger positions with cone features: **3789**.
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

Historical Division 1 snapshots with matched outcome comparisons: **13**.
We rank the same eligible students within each official division and
season, then compare league versus trial percentiles. Repeated hourly
snapshots are correlated and do not form independent experiments.
[Open the historical disagreement study](seasonal_disagreement.md).
![Historical rank agreement](charts/historical_rank_alignment.svg)
![Students specializing in league or trials](charts/league_trial_outliers.svg)

## 7. Older seasons with actual peer games but no saved standings

Historical seasons comparable by match-derived Division 1 outcomes: **145** snapshots.
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
