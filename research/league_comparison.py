"""Publish an auditable league-versus-trial comparison from the game catalog."""
from collections import Counter,defaultdict
from datetime import datetime,timezone
from html import escape
from pathlib import Path
import argparse
import json
import sqlite3
from .league_core import build_data

def fmt(value,places=1):
    return "—" if value is None else f"{value:.{places}f}"

def chart(path,title,body,h=480):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {h}">'
                    f'<rect width="1000" height="{h}" fill="#111a2b" rx="15"/>'
                    f'<text x="30" y="38" fill="#f8fafc" font-family="sans-serif" font-size="22">'
                    f'{escape(title)}</text><g fill="#cbd5e1" font-family="sans-serif" '
                    f'font-size="12">{"".join(body)}</g></svg>',encoding="utf-8")

def rank_chart(path,data):
    standings,trials=data["standings"],data["trials"]
    names=[n for n in data["div1"] if n in trials]
    if not names:
        return chart(path,"League rank and trial performance",
                     ['<text x="40" y="110">No shared data yet</text>'],200)
    x_low=min(trials[n]["mean_length"] for n in names)-8
    x_high=max(trials[n]["mean_length"] for n in names)+8
    last=max(standings[n]["rank"] for n in names)
    X=lambda length:110+755*(length-x_low)/max(1,x_high-x_low)
    Y=lambda rank:78+331*(rank-1)/max(1,last-1)
    body=['<line x1="110" y1="410" x2="865" y2="410" stroke="#64748b"/>',
          '<line x1="110" y1="78" x2="110" y2="410" stroke="#64748b"/>',
          '<text x="465" y="454" text-anchor="middle">Mean length in three on-arrival trials</text>',
          '<text x="24" y="244" text-anchor="middle" transform="rotate(-90 24 244)">Official Division 1 rank (1 is best)</text>']
    for rank in range(1,last+1,5):
        yy=Y(rank)
        body.extend([f'<line x1="110" y1="{yy:.1f}" x2="865" y2="{yy:.1f}" stroke="#29364b"/>',
                     f'<text x="94" y="{yy+4:.1f}" text-anchor="end">{rank}</text>'])
    for n in names:
        xx,yy=X(trials[n]["mean_length"]),Y(standings[n]["rank"])
        leader=n==data["div1"][0]
        standout=n=="409997-utayan-naidoo"
        col="#fbbf24" if leader else "#34d399" if standout else "#60a5fa"
        body.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="{7 if leader or standout else 4}" '
                    f'fill="{col}"><title>{escape(n)}; league {standings[n]["rank"]}; '
                    f'trial {trials[n]["trial_rank"]}; mean length {trials[n]["mean_length"]:.1f}</title></circle>')
        if leader or standout:
            body.append(f'<text x="{xx+9:.1f}" y="{yy-12:.1f}" fill="{col}">'
                        f'{escape(n.split("-",1)[-1])}</text>')
    chart(path,"Actual Division 1 vs controlled trial growth",body)

def coverage_chart(path,cataloged,downloaded):
    maximum=max(1,max(cataloged.values(),default=1))
    body=['<text x="80" y="75">Across all historically indexed seasons</text>']
    for i,kind in enumerate(("league","trial")):
        y=120+120*i
        total=cataloged[kind]
        saved=downloaded[kind]
        width=655*total/maximum
        used=655*saved/maximum
        body.extend([f'<text x="80" y="{y+20}" fill="#f8fafc">{kind.title()}</text>',
                     f'<rect x="165" y="{y}" width="{width:.1f}" height="30" rx="3" fill="#324057"/>',
                     f'<rect x="165" y="{y}" width="{used:.1f}" height="30" rx="3" fill="#60a5fa"/>',
                     f'<text x="843" y="{y+19}">{saved} / {total}</text>'])
    body.extend(['<rect x="165" y="383" width="12" height="12" fill="#60a5fa"/>',
                 '<text x="183" y="394">Downloaded replay</text>',
                 '<rect x="366" y="383" width="12" height="12" fill="#324057"/>',
                 '<text x="384" y="394">Cataloged; replay not downloaded</text>'])
    chart(path,"What are we actually studying?",body,435)

def build(data_dir):
    with sqlite3.connect(data_dir/"snake.db") as db:
        data=build_data(db)
        if not data["season"]:
            raise RuntimeError("No season with official standings")
        unique=defaultdict(set)
        for kind,sha in db.execute("SELECT kind,replay_sha256 FROM matches WHERE replay_sha256 IS NOT NULL"):
            if sha:unique[kind].add(sha)
    out=data_dir/"reports"
    fig=out/"charts"
    rank_chart(fig/"league_vs_trials.svg",data)
    cataloged=Counter()
    downloaded=Counter()
    for season,kind,n,dl,unique_n in data["coverage"]:
        cataloged[kind]+=n
        downloaded[kind]+=dl or 0
    coverage_chart(fig/"league_replay_coverage.svg",cataloged,downloaded)
    standings,trials,league=data["standings"],data["trials"],data["league"]
    champion=data["div1"][0] if data["div1"] else None
    trial_winner=min(trials,key=lambda x:trials[x]["trial_rank"]) if trials else None
    gauntlet_winner=max(trials,key=lambda x:trials[x]["gauntlet_length"]) if trials else None
    lines=[
        "# Snake26: League versus on-arrival trials","",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "Latest season with official standings: "+data["season"],"",
        "## 1. Are league and benchmark results consistent?","",
        "![Division 1 rank versus trial strength](charts/league_vs_trials.svg)","",
        "| Division | Students with all trials | Official rank vs mean trial length (Spearman) | Official rank vs gauntlet length (Spearman) |",
        "|---|---:|---:|---:|"
    ]
    for division in sorted(data["comparisons"]):
        row=data["comparisons"][division]
        lines.append(f"| {division} | {row['n']} | {fmt(row['official_vs_trial_len'],3)} | {fmt(row['official_vs_gauntlet_len'],3)} |")
    lines.extend(["",
        "Positive correlation means better official ranking tends to align with better trial lengths.",
        "Never compare division-specific rank numbers across divisions: Division 2 rank 1 is not Division 1 rank 1.",
        "Official standings can reflect accumulated scoring; these are cross-sectional associations.",
        "",
        "## 2. Which snakes demonstrate the gap?","",
        "| Group | Student | Division/rank | Combined trial rank | Mean trial final length | Gauntlet final length |",
        "|---|---|---|---:|---:|---:|"])
    for label,name in (("League champion",champion),("Best combined trials",trial_winner),
                       ("Best gauntlet_1",gauntlet_winner)):
        if name:
            s=standings.get(name,{})
            t=trials[name]
            lines.append(f"| {label} | {name} | {s.get('division','—')}/{s.get('rank','—')} | "
                         f"{t['trial_rank']} | {fmt(t['mean_length'])} | {t['gauntlet_length']} |")
    lines += ["",
        "## 3. What do REAL league match results reveal?","",
        "Some official league games also have built-in filler opponents. We distinguish",
        "student-only matches from mixed matches and compare only catalog games",
        "with at least two actual students.",
        "",
        "| Latest league format | Games cataloged | Full replays saved |",
        "|---|---:|---:|"]
    for label,count in sorted(data["latest_kind"].items()):
        lines.append(f"| {label} | {count} | {data['latest_downloaded'][label]} |")
    lines += ["",
        "League metrics below use official match catalog outcomes, not any assumed",
        "strategy inferred from replay. Win rate and mean placement are per-game observations.",
        "Retained ratio means final length divided by (5 + 5 times total apples); it can",
        "indicate growth lost to resets but cannot identify the number or timing of deaths.",
        "",
        "| Div 1 rank | Student | League matches | Win % | Mean place | Mean apples | Mean kills | Mean length | Retained ratio | League replays | Trial rank |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for name in data["div1"]:
        info=league.get(name,{})
        t=trials.get(name,{})
        win=100*info["win_rate"] if info.get("win_rate") is not None else None
        lines.append(f"| {standings[name]['rank']} | {name} | {info.get('league_games',0)} | "
                     f"{fmt(win)} | {fmt(info.get('avg_place'))} | {fmt(info.get('avg_food'))} | "
                     f"{fmt(info.get('avg_kills'))} | {fmt(info.get('avg_length'))} | "
                     f"{fmt(info.get('avg_retained'),2)} | {info.get('replay_games',0)} | "
                     f"{t.get('trial_rank','—')} |")
    lines += ["",
        "## 4. How biased is our replay collection?","",
        "![League and trial replay coverage](charts/league_replay_coverage.svg)","",
        "| Mode | Catalog records | Downloaded replays | Unique byte-identical replay payloads | Coverage |",
        "|---|---:|---:|---:|---:|"]
    for kind in ("league","trial"):
        count=cataloged[kind]
        dl=downloaded[kind]
        lines.append(f"| {kind} | {count:,} | {dl:,} | {len(unique[kind]):,} | {100*dl/count if count else 0:.2f}% |")
    lines += ["",
        "The total number of historical catalogs is NOT the count of independent bot matches;",
        "replays, opponents, seeds and bot versions may repeat across seasons.",
        "If league replay coverage is small, detailed claims about league navigation",
        "or aggression are premature.",
        "",
        "## 5. Testing the proposed aggression/safety sweet spot","",
        "Our hypothesis is that competitive leaders optimize both growth and survival.",
        "That is plausible but unproven. Compare for each bot and game type:",
        "- Food acquisition: apples per alive turn, contested captures, route progress.",
        "- Risk management: deaths per 1,000 alive turns, body collision causes, safe-space preservation.",
        "- Aggression: kills per game, head-on approach rates, pressures around contested apples.",
        "- Retention: final body length versus all accumulated apples, accounting for resets.",
        "- Adaptation: changes to the same team's behavior in trials versus real league matches.",
        "Match code versions and opponent composition; bootstrap uncertainty by entire match.",
        "",
        "## Next steps",
        "Rebalance replay downloads toward League Division 1 and genuine student-versus-student",
        "situations while maintaining substantial coverage of on-arrival benchmark trials.",
        "Do not implement another competition snake until those comparisons are tested.",""]
    path=out/"league_vs_trials.md"
    path.write_text("\n".join(lines),encoding="utf-8")
    return dict(season=data["season"],division1=len(data["div1"]),
                champion=champion,best_combined_trial=trial_winner,
                best_gauntlet=gauntlet_winner,
                league_catalogs=cataloged["league"],
                league_replays=downloaded["league"],
                unique_league_replays=len(unique["league"]),
                div1_spearman=data["comparisons"].get(1),
                report=str(path))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    args=p.parse_args()
    print(json.dumps(build(args.data_dir),indent=2))

if __name__=="__main__":
    main()
