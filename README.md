# Wits Snake26 Intelligence Collector 🐍

A **conservative, restart-safe** public-API research collector for the Wits Snake AI 2026 competition. It tracks seasonal standings and code hashes, catalogs matches, downloads a limited number of replays, derives reliable movement statistics, and generates `data/reports/latest.md`.

**Status:** Implementation tested with local synthetic API/replay fixtures. Network access to the live platform was unavailable in the build environment. API endpoint structures are taken from the Gemini investigation dated November 2026 and must be validated in the first live run. No GitHub repository or automation has been created by this package alone.

## Quick start

Requires Python 3.11 or newer. No third-party packages.

```bash
python -m unittest discover -s tests -v
python collector.py --max-replays 2
```

The first run creates `data/snake.db`, `data/replays/<season>/<game>.rep.gz`, and `data/reports/latest.md`. `--max-replays 0` collects metadata without downloading replays.

## Cloud deployment — GitHub Actions

1. Create a **private** GitHub repository and upload the entire contents of this project, including `.github/workflows/collect.yml`.
2. Enable Actions for the repository and allow workflow `GITHUB_TOKEN` **Read and write permissions** if your repository/account settings require it. The workflow also requests `contents: write`.
3. From **Actions → Collect Snake26 intelligence → Run workflow**, run it once manually and inspect logs and `data/reports/latest.md`.
4. If successful, the workflow is scheduled hourly at `HH:15 UTC`; schedules may be delayed or missed by GitHub and are not real-time guarantees.
5. Your computer can be switched off. Data is committed to the **private repository** after each successful run.

For manual catch-up, use **Run workflow** and temporarily increase `max_replays` up to 30. Be respectful of the platform's server load. The default is **six replays per run**, not the entire season. Initial historical metadata is limited to two latest seasons; change `--lookback-seasons` (up to 12) if needed. Only replays of catalogued matches marked `kept=true` are considered.

### How selection works

The latest season is preferred, with Division 1 matches and matches featuring the latest Division 1 top ten prioritized. When older seasons are available, about one-third of replay slots go toward historical games to ensure backfilling progresses. Older seasons are picked up as space allows. Each game is only downloaded once. If the previous run downloaded a file but failed before committing its DB entry, the next run re-parses the local compressed file instead of requesting it again. Failed downloads remain eligible for later retries.

The `api/season` schema has only been reported for the latest season. Therefore, the collector archives historical **game catalogs**, not unverified historical standings.

## Database and replay analysis

- `seasons`: known seasons and current-season metadata
- `teams`: entrant identifiers and current metadata
- `team_versions`: `(season, team)` ↔ submitted code hash, so old hashes are not lost
- `standings`: seasonal ratings and division rank
- `matches`: metadata and replay digest, unique by `(season, replay name)`
- `participants`: individual results, **unknown snake slot stays NULL until replay parsed**
- `events`: per-turn death, food, and other events
- `behavior`: counts of valid relative moves (straight/left/right), deaths and death causes, food events, latency

The replay format reportedly contains complete states but *not* explicit move strings. Moves are **inferred** from consecutive alive frames on the toroidal grid. Frames with missing moves, respawns, jumps or ambiguous reversals are intentionally omitted. This **does not** recover an unsuccessful decision, a rejected move, or the bot's reasoning. Analysis counts are descriptive, not claims about superiority.

## Security, volume, and reliability

- Uses public unauthenticated GET requests only. No login/session scraping, passwords or tokens.
- Keeps requests sequential with ≥0.75 seconds spacing and retries transient failures with backoff.
- Validates safe replay identifiers to prevent writing outside `data/replays/`.
- Replays are gzip-compressed; the current workflow tracks the database and compressed raw replays in Git. **Git repository history grows over time**, particularly with an updated SQLite file every hour. This is intended as a short-term, modest-volume solution for the November 8 deadline, not limitless archive storage.
- SQLite uses rollback-journal mode rather than WAL for safer commit-to-Git workflows. No concurrent writers.
- The site may block scraping or have unpublished usage restrictions; follow the institution's instructions and stop if requested. Don't increase concurrency aggressively.
- Hosted runners and scheduled jobs are not guaranteed exact execution times. For high-volume, long-term storage, migrate replays to object storage and keep Git to code and summaries.

## Limitations

This code has **not** been live-tested against Wits from this environment. If Gemini's sample JSON differs from the real API, adjust the parser after examining a redacted response. The last-run report contains only metrics from downloaded replays; it should not be interpreted as a leaderboard. No predictive model or new competition bot is included yet.
