# Snake26 Intelligence — League + Trial Data Science 🐍📊

**Research first. No new competition Snake AI is implemented in this repository.**

This private repository collects publicly accessible Wits Snake26 match catalogs, official league standings, submitted-bot version hashes where available, and selected full replays. Our purpose is to learn what predicts performance **against other students**, while preserving on-arrival benchmark trials as controlled, *different* evidence.

## Start here

1. **[Research dashboard and report index](data/reports/README.md)** — the entry point for all studies
2. **[Canonical joint league–trial report](data/reports/joint_analysis.md)** — same student, same season, cross-environment correlations
3. **[Competition-wide decisions: strong/middle/struggling snakes](data/reports/competitive_cohorts.md)** — same-season league rank, actual recorded choices, matched same-game comparisons
   - **[2026 collision/movement evidence](data/reports/safety_mechanics.md)** — observed wrap, tail, head-on deaths, and apple growth; formal move legality still requires engine verification
   - **[Adaptive survival/food contexts](data/reports/adaptive_context.md)** — league/trial death and apple rates by body length, occupancy, game phase and head proximity
   - **[Future route-space investigation](data/reports/route_space.md)** — frozen flood-fill versus moving own-tail prediction, with replay-holdout ROC AUC and cluster-bootstrap uncertainty
   - **[Opponent head-reach investigation](data/reports/opponent_cones.md)** — one-turn geometric threat sets, actual head-on event audit, league-vs-trial comparisons, and a critical shorter-opponent opportunity adjustment
   - **[Evidence-gated algorithm rulebook](data/reports/algorithm_rulebook.md)** — state-to-action hypotheses, counterexamples, tests for a completely NEW agent
4. **[Full replay behavior separated by environment](data/reports/behavior_by_mode.md)** — real observed decisions, not inferred from match scores
   - **[Opponent head pressure and escape-space study](data/reports/threat_windows.md)**
   - **[Matched death autopsies versus observed escapes](data/reports/escape_autopsies.md)** — same-mode, same-starting-risk comparisons across real league and trial replays
   - **[30-turn danger survival](data/reports/long_horizon_survival.md)** — after the first successful escape, does the snake remain alive?
   - **[Real student-vs-student apple contests](data/reports/league_food_contests.md)** — verified apple captures with Palmer subset and explicit censoring
   - **[Apple prediction tie-break audit](data/reports/league_food_prediction.md)** — replay-cluster comparison of closer-head versus length-at-distance-tie predictors
   - **[Palmer's actual league danger decisions](data/reports/palmer_casebook.md)** — one strong competitor's real movement casebook, supporting (not replacing) population-wide comparisons
5. **[Historical peer-game versus trial study](data/reports/historical_peer_comparison.md)** — actual archived student league placements where official old standings are missing
6. **[Historical league/trial specialists](data/reports/seasonal_disagreement.md)** — comparable division rank gaps with explicit snapshot/version caveats
7. **[Joined data exports](data/derived/joined_team_seasons.csv)** and **[quality audit](data/derived/quality.json)** — reproducible inputs and coverage

The old [strategy laboratory](data/reports/strategy_lab.md) is a **legacy pooled diagnostic**, not evidence about league strategy. On-arrival food-race/underdog studies remain useful supporting studies but **do not substitute for student-versus-student replay observations**.

## The correct research design

| Environment | Opponents | Data used | What we can claim |
|---|---|---|---|
| League | Other submitted student snakes; occasional built-in filler | Official match results, standings and full replays | Actual competitive outcomes and observed behavior when downloaded |
| On-arrival trials | Three fixed built-in benchmark groups | Three common trial scores and full replays | Controlled performance with common opponent configurations |
| Joint cohort | **Same student + same season**, separate source columns | Joined tables and mode-separated replay features | Observational cross-environment correlations, not causation |

**Important:** A student's recorded SHA-256 is the season snapshot. It does not prove that *every match* within the season used that exact submitted version. Historical standings may be missing; never compare Division 2 rank 1 to Division 1 rank 1 as equivalent. Match catalog data cannot tell us how a snake chose to move; only replay frames can provide movement observations. Identical full replays are deduplicated by content SHA-256 for behavioral analysis.

Archived matches without official historical standings can still be compared using **observed peer-game placements**, which are NOT official league ranks. Recent joined Spearman correlations include exploratory **paired-student bootstrap** intervals; repeated hourly snapshots and schedules are not independent experiments.

The paired outcomes dataset includes both complete trial sets and student-opponent league games. The matched **replay-behavior** cohort is smaller and must report its sample size explicitly; it cannot be filled in using aggregate food or length values.

## GitHub Actions — just two workflows

- **[Collect Snake26 intelligence](.github/workflows/collect.yml)** — the **sole data writer**, offered a primary scheduled slot at minute 17 UTC and backup at minute 47 UTC. A tested 50-minute archive-freshness guard skips redundant runs; the workflow is also available via manual Run workflow. Downloads a small number of replays sequentially with ≥0.75 seconds between requests, safely updates the SQLite archive, rebuilds reports and publishes data. Replay sampling targets **60% league / 40% trials**, prioritizing Division 1 student-versus-student matches, **same-student/same-season replay pairing**, all three trial suites, and historical coverage; actual quotas depend on available unique games.
- **[Validate Snake26 research](.github/workflows/research_ci.yml)** — read-only tests and analysis on code changes. **Never downloads from Wits or writes to the Git repository.** Produces a downloadable artifact with current paired reports and graphs.

Research code changes **do not trigger costly collection runs**. Only one GitHub Actions job can publish the database/replays at a time. GitHub can delay hourly jobs; this is not guaranteed real-time monitoring.

## Run locally (Python 3.11+, standard library only)

```bash
python -m unittest discover -s . -p 'test*.py' -v
python -m research.integrated_dashboard --data-dir data
python -m research.league_comparison --data-dir data
python -m research.dashboard --data-dir data
# Optional: collect limited new public replay data:
python collector.py --max-replays 2 --lookback-seasons 2
```

The repository holds `data/snake.db`, `data/replays/<season>/**/*.rep.gz` (gzipped JSON), reports under `data/reports/`, and derived tables under `data/derived/`. GitHub does not preview compressed replay JSON as a video. The analysis scripts intentionally do not require private competitors' source code or accounts.

## Quality, safety and storage

Public GET requests only; no credential collection or aggressive scraping. Respect Wits server limits and any campus restrictions. Full replays may contain the positions, events and timings needed for analysis, but they **cannot act as responsive opponent executables in hypothetical matches**. Retain match-level controls, differentiate versions and avoid interpreting correlated turns as independent trials.

The SQLite file is tracked in Git as a pragmatic short-term archive. **Frequent database and replay commits will increase repository history size**; longer-term work should migrate raw storage to object storage rather than treating Git as an unlimited time-series database. Avoid deleting raw evidence as part of report cleanup.

**Research stage:** audit and quantify student league play and controlled trials together; investigate hypotheses next; implement a new Snake AI only after the evidence justifies it.
