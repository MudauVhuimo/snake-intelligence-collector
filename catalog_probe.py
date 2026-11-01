#!/usr/bin/env python3
"""Inspect published match kinds without downloading any additional replays."""
from collections import Counter
from pathlib import Path

from collector import Client, safe_name, utcnow

def main():
    client = Client(delay=1.0)
    site = client.get_json("site")
    season_names = list(dict.fromkeys([site["season"]["name"]] + site.get("seasons", [])))[:12]
    lines = [
        "# Match catalog discovery", "",
        f"Generated UTC: {utcnow()}", "",
        "Metadata only; no private snake source code or new replay downloads.", "",
        "| Season | Cataloged | Kinds | Benchmark/arrival-style matches |",
        "|---|---:|---|---:|",
    ]
    samples = []
    total = Counter()
    for season in season_names:
        season = safe_name(season)
        try:
            data = client.get_json("games", {"season": season})
        except Exception as exc:
            lines.append(f"| `{season}` | ERROR | {type(exc).__name__} | — |")
            continue
        games = data.get("games", [])
        kinds = Counter(str(g.get("kind", "missing")) for g in games)
        total.update(kinds)
        related = []
        for game in games:
            roster = [str(s.get("name", "")) for s in game.get("snakes", [])]
            signature = " ".join([str(game.get("kind", "")), str(game.get("label", "")), *roster]).lower()
            if any(w in signature for w in ["arrival", "on-arrival", "benchmark", "survivor", "hungry", "hunter", "wander", "gauntlet"]):
                related.append(game)
        lines.append(f"| `{season}` | {len(games)} | {', '.join(f'{k}: {v}' for k,v in sorted(kinds.items()))} | {len(related)} |")
        for g in related[:4]:
            samples.append((season, g))
        if len(samples) < 3 and games:
            samples.append((season, games[0]))
    lines += ["", "## Catalog kinds (all scanned seasons)", "",
              ", ".join(f"`{k}`: {v}" for k, v in sorted(total.items())) or "None", "",
              "## Representative matching games", ""]
    for season, g in samples[:18]:
        names = ", ".join(str(s.get("name", "")) for s in g.get("snakes", []))
        lines += [
            f"- **{season} / {g.get('replay', 'no replay')}**",
            f"  - Kind: `{g.get('kind')}`; label: `{g.get('label')}`; kept: `{g.get('kept')}`; division: `{g.get('division')}`",
            f"  - Participants: {names or '(none listed)'}",
        ]
    lines += ["", "## Important limitation", "",
              "The catalog shows match *metadata* only. These are not executable opponents. We can compare outcomes against shared benchmark bots, but cannot accurately simulate our new snake against a historical opponent by replaying fixed opponent actions after changing the board.", ""]
    output = Path("data/reports/catalog.md")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Catalog scan complete, kinds: {dict(total)}; report: {output}")

if __name__ == "__main__":
    main()
