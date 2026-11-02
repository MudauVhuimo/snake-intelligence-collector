# Snake26 Research — Start here

The **canonical research entry point** is [Joined League + Trials](joint_analysis.md).
Read this before interpreting the older single-environment reports.

## Source-of-truth datasets

- [League outcomes](../derived/league_team_seasons.csv)
- [Trial outcomes](../derived/trial_team_seasons.csv)
- [Joined per student-season outcomes](../derived/joined_team_seasons.csv)
- [Coverage, completeness and quality checks](../derived/quality.json)

## Supporting studies — with explicitly limited scopes

- [Official league versus fixed-seed rankings](league_vs_trials.md):
  standings/outcomes, not a replay-derived behavioral model.
- [Historical actual peer-match outcomes vs trials](historical_peer_comparison.md):
  works without older official standings; **game-derived proxy** only.
- [League/trial specialists across historical snapshots](seasonal_disagreement.md):
  matched division ranks, tracked across recorded seasons and bot hashes.
- [Head pressure, local exits, and future deaths](threat_windows.md):
  actual replay frames; mode- and length-stratified, not a proven policy.
- [Observed league/trial behavior matched by student](behavior_by_mode.md):
  replay-derived food and death measures; report sample coverage first.
- [League food versus growth retained](league_sweet_spot.md):
  correlation, not proven aggression or optimal policy.
- [On-arrival food contests](food_races.md):
  primarily student-versus-built-in benchmark observations.
- [On-arrival underdog apple case studies](underdog_study.md):
  benchmark-specific, NOT evidence about peers in league matches.
- [Historical replay behavioral proxies](strategy_lab.md):
  cross-mode exploratory snapshots; treat aggregates as preliminary.
- [Replay growth/death exploratory plots](data_science.md):
  mixed-mode student exposure; see mode separation warnings.

## Operating rules

Research reports are generated from the repository's SQLite catalogs
and archived replay frames by one scheduled GitHub Actions collector.
Research code changes alone do not trigger data downloads. A separate
read-only validation workflow tests new analysis code.
All files are private repository research artifacts; no private bot
executables or source code are extracted. No Java snake changes yet.
