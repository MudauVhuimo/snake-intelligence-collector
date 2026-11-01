"""Test whether high league performance aligns with food AND growth retention.

Descriptive analysis; no inferred causal strategy or opponent source code.
"""
from datetime import datetime,timezone
from html import escape
from pathlib import Path
from .league_core import build_data,spearman
from .league_comparison import chart,fmt
import argparse
import json
import sqlite3

METRICS=(
    ("avg_food","Mean apples per league match"),
    ("avg_retained","Mean retained growth ratio"),
    ("avg_kills","Mean kills per league match"),
    ("avg_length","Mean final body length"),
    ("win_rate","League first-place frequency"),
)

def scatter(path,data,selected):
    leagues=data["league"]
    names=selected
    if not names:
        return chart(path,"Division 1 food and retention",["<text x='40' y='100'>No league results</text>"],210)
    x_values=[leagues[n]["avg_food"] for n in names]
    y_values=[leagues[n]["avg_retained"] for n in names]
    xmin=max(0,min(x_values)-3)
    xmax=max(x_values)+4
    ymin=0
    ymax=max(1.02,max(y_values)+.03)
    X=lambda x:108+750*(x-xmin)/max(1,xmax-xmin)
    Y=lambda y:410-315*(y-ymin)/max(.01,ymax-ymin)
    content=['<line x1="108" y1="410" x2="858" y2="410" stroke="#64748b"/>',
             '<line x1="108" y1="95" x2="108" y2="410" stroke="#64748b"/>',
             '<text x="460" y="466" text-anchor="middle">Mean apples eaten per league match</text>',
             '<text x="21" y="250" transform="rotate(-90 21 250)" text-anchor="middle">Mean retained growth ratio</text>']
    for value in (0,.2,.4,.6,.8,1):
        yy=Y(value)
        content.extend([f'<line x1="108" y1="{yy:.1f}" x2="858" y2="{yy:.1f}" stroke="#2d3b52"/>',
                        f'<text x="92" y="{yy+4:.1f}" text-anchor="end">{value:.1f}</text>'])
    for n in names:
        stats=leagues[n]
        rank=data["standings"][n]["rank"]
        champion=rank==1
        gauntlet=n=="409997-utayan-naidoo"
        color="#fbbf24" if champion else "#34d399" if gauntlet else "#60a5fa"
        xx,yy=X(stats["avg_food"]),Y(stats["avg_retained"])
        radius=8 if champion or gauntlet else 4
        content.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="{radius}" '
                       f'fill="{color}" opacity=".9"><title>'
                       f'{escape(n)}; official league rank {rank}; apples {stats["avg_food"]:.1f}; '
                       f'retained {stats["avg_retained"]:.2f}; games {stats["league_games"]}'
                       '</title></circle>')
        if champion or gauntlet:
            content.append(f'<text x="{xx+9:.1f}" y="{yy-11:.1f}" fill="{color}">'
                           f'{escape(n.split("-",1)[-1])}</text>')
    content.extend(['<circle cx="865" cy="104" r="6" fill="#fbbf24"/>',
                    '<text x="879" y="107">League leader</text>',
                    '<circle cx="865" cy="123" r="6" fill="#34d399"/>',
                    '<text x="879" y="126">Gauntlet leader</text>'])
    chart(path,"Division 1: food acquired vs growth retained",content,495)

def build(data_dir:Path,min_matches=3):
    with sqlite3.connect(data_dir/"snake.db") as db:
        data=build_data(db)
    if not data["season"]:
        raise RuntimeError("Missing official league standings")
    participants=[n for n in data["div1"] if n in data["league"]
                  and data["league"][n]["league_games"]>=min_matches
                  and data["league"][n]["avg_food"] is not None
                  and data["league"][n]["avg_retained"] is not None]
    folder=data_dir/"reports"
    scatter(folder/"charts"/"league_food_retention.svg",data,participants)
    leader=data["div1"][0]
    gauntlet="409997-utayan-naidoo"
    lines=[
        "# Snake26: League aggression vs growth-retention hypothesis","",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
        "## Data design","",
        f"Latest official season: {data['season']}. Division 1 group: {len(data['div1'])} students.",
        f"Included students with at least {min_matches} recorded league matches and usable food/length: {len(participants)}.","",
        "A length-retention proxy is final length divided by 5 plus 5 times ALL apples eaten.",
        "This can detect lost growth from resets but cannot reconstruct exact death timing.",
        "Each student faces a different schedule; raw averages do not control for opponent strength.","",
        "## The apparent risk-versus-food tradeoff","",
        "![Actual food collection against retained final growth](charts/league_food_retention.svg)","",
        "The upper-right area represents students who collect more apples and retain more",
        "resulting length in these match samples. It is not a proven optimum.",
        "",
        "## Which league outcomes align with official Division 1 ranking?","",
        "| Metric | Bots with matches | Spearman agreement with official league rank |",
        "|---|---:|---:|"
    ]
    correlations={}
    for key,description in METRICS:
        names=[n for n in participants if data["league"][n][key] is not None]
        rho=spearman([data["standings"][n]["rank"] for n in names],
                     [-data["league"][n][key] for n in names])
        correlations[key]=rho
        lines.append(f"| {description} | {len(names)} | {fmt(rho,3)} |")
    lines+=["",
        "Positive means higher performance on that metric tends to align with better",
        "official standing. League win rate and rank are related game outcomes; their",
        "correlation is NOT independent evidence for a specific movement strategy.",
        "",
        "## Specific students worth comparing in full replays","",
        "| Student | Division 1 rank | League matches | League win % | Mean apples | Mean length | Mean retained growth | Gauntlet final length |",
        "|---|---:|---:|---:|---:|---:|---:|---:|"]
    names=[leader,gauntlet]+[n for n in data["div1"][:10] if n not in (leader,gauntlet)]
    for n in names:
        r=data["standings"].get(n,{})
        t=data["trials"].get(n,{})
        p=data["league"].get(n,{})
        lines.append(f"| {n} | {r.get('rank','—')} | {p.get('league_games','—')} | "
                     f"{fmt(p.get('win_rate')*100 if p.get('win_rate') is not None else None)} | "
                     f"{fmt(p.get('avg_food'))} | {fmt(p.get('avg_length'))} | "
                     f"{fmt(p.get('avg_retained'),2)} | {t.get('gauntlet_length','—')} |")
    lines+=["",
        "## Why we cannot yet declare a sweet spot","",
        "- Only a handful of current-season games per student are currently cataloged.",
        "- Different opponents, starts, seats, maps and versions can change outcomes.",
        "- A mean retained ratio is a reset proxy, not proof of risk-aversion or aggression.",
        "- Final-length evidence cannot tell whether the snake deliberately avoided fights.",
        "- Needed: elite league replays with apple choices, head threats, deaths and escape routes.",
        "- Test per-match and per-bot-version uncertainty before proposing a movement rule.",
        "",
        "The same research cycle must continue collecting and analyzing benchmark trials.",
        "No new competition agent code is implemented in this analysis.",""]
    output=folder/"league_sweet_spot.md"
    output.write_text("\n".join(lines),encoding="utf-8")
    return dict(season=data["season"],students=len(participants),
                correlations=correlations,leader=leader,report=str(output))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    args=p.parse_args()
    print(json.dumps(build(args.data_dir),indent=2))

if __name__=="__main__":
    main()
