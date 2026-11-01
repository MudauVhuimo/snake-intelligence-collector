# Snake26: JOINED league + trials study

Generated UTC: 2026-11-01T23:46:10+00:00

**Latest official season:** 2026-11-01-225859-season. This report treats competitive league
matches and controlled on-arrival trials as **two separate datasets**
and joins them at the **same season + same student**. The published
end-of-season code SHA, when known, is attached for auditing, but is
**not proof that every match in that season used that exact code version**.

## 1. Data provenance and cleaning

**Source of truth:** official public Wits catalog records in the SQLite archive.

| Separate data source | Cataloged matches | Full replays | Unique replay hashes |
|---|---:|---:|---:|
| League | 2,093 | 95 | 45 |
| Trial | 17,958 | 55 | 42 |

**Historical student-season rows:** league 1,548,
trials 5,986, union 6,005.
**Current season paired students (at least 2 student-opponent league games
plus all 3 trials): 146**.
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

| Paired measurement | Division 1 students | Spearman rho |
|---|---:|---:|
| Apples per game | 32 | 0.491 |
| Final body length | 32 | 0.475 |
| Kills per game | 32 | 0.438 |
| Retained growth / expected no-reset growth | 32 | 0.499 |

Correlations are calculated only among students from **the same division
and season**, to avoid comparing ranks of different divisions. These are
within-student comparisons across distinct conditions—not claims that
one environment causes performance in the other.

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
| 1 | 421462-alexander-palmer | 3 | 66.7 | 28.7 | 0.70 | 0.67 | 48.0 | 0.79 | 15.33 | 3/0 |
| 2 | 428786-marvellous-sambo | 5 | 60.0 | 32.0 | 0.74 | 1.00 | 34.7 | 0.70 | 16.00 | 1/0 |
| 3 | 388828-ngcebo-methula | 6 | 66.7 | 32.7 | 0.47 | 0.83 | 40.0 | 1.00 | 14.67 | 3/0 |
| 4 | 403339-david-ndambo | 5 | 80.0 | 30.2 | 0.84 | 1.40 | 41.3 | 1.00 | 12.67 | 1/0 |
| 5 | 427039-sameeha-miabala | 4 | 50.0 | 25.8 | 1.00 | 0.75 | 38.7 | 1.00 | 14.33 | 1/0 |
| 6 | 413538-lelethuthando-nikelo | 5 | 20.0 | 33.6 | 0.64 | 1.80 | 43.3 | 1.00 | 22.33 | 2/3 |
| 7 | 421349-phathutshedzo-mudzanani | 4 | 25.0 | 29.8 | 0.56 | 0.50 | 43.7 | 0.95 | 10.33 | 0/3 |
| 8 | 427064-khodani-netili | 5 | 40.0 | 31.4 | 0.40 | 1.80 | 42.0 | 1.00 | 11.33 | 1/0 |
| 9 | 419926-mphile-nchabeleng | 6 | 33.3 | 29.3 | 0.61 | 0.67 | 35.0 | 1.00 | 14.00 | 3/3 |
| 10 | 424820-elisha-mundalamo | 5 | 20.0 | 31.4 | 0.78 | 1.20 | 40.3 | 0.95 | 13.33 | 4/0 |
| 11 | 428954-njabulo-ndlozi | 4 | 25.0 | 30.2 | 0.25 | 0.50 | 37.3 | 0.75 | 17.00 | 2/0 |
| 12 | 426895-mpho-ramasakona | 5 | 20.0 | 26.2 | 0.27 | 0.60 | 40.7 | 0.54 | 15.67 | 1/0 |
| 13 | 406000-mulimisi-rammela | 5 | 40.0 | 23.0 | 0.82 | 1.00 | 25.0 | 1.00 | 12.00 | 0/0 |
| 14 | 423258-muhammed-dar | 5 | 40.0 | 32.0 | 0.47 | 0.80 | 44.0 | 0.74 | 13.00 | 1/0 |
| 15 | 388060-tshepang-tshabalala | 5 | 20.0 | 25.4 | 0.65 | 0.80 | 44.7 | 1.00 | 15.00 | 4/0 |
| 16 | 389160-lwandle-ramanugu | 6 | 33.3 | 25.7 | 0.45 | 1.17 | 38.0 | 0.54 | 17.33 | 1/0 |
| 17 | 423436-ntobeko-zondi | 6 | 33.3 | 27.2 | 0.57 | 0.33 | 33.3 | 1.00 | 12.00 | 1/0 |
| 18 | 423135-mpho-muremi | 5 | 0.0 | 21.4 | 0.91 | 0.80 | 26.0 | 1.00 | 21.33 | 2/0 |
| 19 | 408070-collen-mthombeni | 6 | 16.7 | 30.3 | 0.24 | 0.33 | 42.3 | 0.50 | 4.67 | 2/0 |
| 20 | 426650-babongile-mafantiri | 5 | 40.0 | 26.6 | 0.16 | 0.40 | 32.7 | 1.00 | 20.33 | 0/0 |
| 21 | 402334-angile-saho | 6 | 16.7 | 30.8 | 0.52 | 1.17 | 52.7 | 0.78 | 19.33 | 1/0 |
| 22 | 404721-khensani-maluleke | 4 | 0.0 | 34.2 | 0.31 | 0.00 | 45.0 | 0.43 | 13.00 | 1/0 |
| 23 | 419342-ayeshan-puckree | 5 | 20.0 | 27.4 | 0.43 | 0.60 | 32.0 | 1.00 | 12.33 | 0/0 |
| 24 | 422777-thandile-mamiana | 6 | 0.0 | 18.5 | 0.70 | 0.50 | 35.0 | 0.81 | 8.33 | 2/0 |
| 25 | 427417-phophi-shavhani | 5 | 20.0 | 27.8 | 0.41 | 1.00 | 44.0 | 0.40 | 10.00 | 1/0 |
| 26 | 409997-utayan-naidoo | 6 | 16.7 | 28.7 | 0.21 | 0.17 | 48.7 | 0.77 | 10.67 | 2/1 |
| 27 | 410193-vhugala-makhwathane | 6 | 0.0 | 24.5 | 0.66 | 0.17 | 27.0 | 1.00 | 8.67 | 2/0 |
| 28 | 424907-sibongakonke-ntsele | 5 | 20.0 | 22.8 | 0.50 | 0.40 | 36.7 | 0.62 | 8.00 | 1/0 |
| 29 | 408008-bradley-buys | 5 | 0.0 | 25.8 | 0.30 | 0.40 | 42.0 | 0.76 | 16.67 | 1/0 |
| 30 | 428798-oratile-molefe | 6 | 0.0 | 26.2 | 0.30 | 0.33 | 31.3 | 0.54 | 8.33 | 1/0 |
| 31 | 428464-madalitso-mnqanqeni | 5 | 0.0 | 28.2 | 0.11 | 0.20 | 41.7 | 0.50 | 9.33 | 1/0 |
| 32 | 423239-zeeshaan-bham | 5 | 20.0 | 34.4 | 0.34 | 0.40 | 41.0 | 1.00 | 13.33 | 2/0 |

## 5. The same students: *actual replay-derived* behavior

Current-season students with BOTH league and trial full replay behavior: **3**.
Catalog counts cannot fill in missing replay decisions; only identical,
verifiable frame-derived definitions can be compared across modes.
[See the mode-separated behavioral report](behavior_by_mode.md) for
observed food-event/death rates and their conditional correlations.
![Student food events per observed move in each mode](charts/observed_food_by_mode.svg)
![Student deaths per observed move in each mode](charts/observed_deaths_by_mode.svg)

## 6. Reproducible joined data exports

- [League team-season summaries](../derived/league_team_seasons.csv) —
  the real competition outcomes, including human-opponent counts.
- [Trial team-season summaries](../derived/trial_team_seasons.csv) —
  three controlled benchmark setups, kept separate.
- [Joined student-season dataset](../derived/joined_team_seasons.csv) —
  one row per student and season; missing sides are **missing**, not zero.
- [Replay-backed behavior, separated by mode](../derived/replay_behavior_by_mode.csv) —
  only downloaded full match observations.
- [Data validation summary](../derived/quality.json) —
  replay coverage, SHA deduplication and sample sizes.

## 7. What needs further evidence

1. Obtain full league replays of top Division 1 students, including both
   winners and losers, and map their exact turns/deaths/food contests.
2. Run the **same replay-derived definitions** separately on league and
   on-arrival data: food pursuit, death risk, contest pressure and mobility.
3. Compare like-for-like length, turn phase, opponent skill and version.
4. Group uncertainty by complete match/season, not thousands of turns.
5. Interpret only held-out, version-aware patterns before changing our snake.

This joined report establishes observational associations, not an optimal
aggression/safety formula. No competition snake code has been modified.
