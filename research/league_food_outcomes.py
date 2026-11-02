"""Replay-cluster audit of two PRE-ACTION apple capturer predictors.

Uses only eligible observed league apple appearances saved by
league_food_contests. Both rules are FIXED in advance, not trained/tuned:
  A: Pick geometrically closer snake (0.5 expected tie credit).
  B: Pick geometrically closer snake; on equal distance, prefer longer body
     (0.5 expected credit if both bodies also equal).
Outcomes are verified captures, including 0 credit when a third snake wins.
These are PREDICTIVE accuracy scores; NOT causal policy success rates.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

BOOTSTRAPS = 2000
SEED = 20261102
TOP2 = {"nearest", "second", "tied_first", "tied_second"}
FIRST = {"nearest", "tied_first"}


def score(row):
    """Return expected 0/1 credits for each fixed prediction.

    The half-credit at exact ties avoids arbitrary snake-id tie advantage.
    A third-party capture earns zero for both policies. Caller only passes
    confirmed episodes; no subsequent movement is consulted for prediction.
    """
    if row["status"] != "confirmed":
        raise ValueError("Cannot evaluate unverified apple episode")
    gap = int(row["gap"])
    near_len = int(row["nearest_length"])
    second_len = int(row["second_length"])
    outcome = row["winner_class"]
    if outcome not in TOP2 and outcome != "other":
        raise ValueError("Invalid confirmed winner class")
    if outcome == "other":
        return 0.0, 0.0
    near_won = outcome in FIRST
    nearest = (0.5 if gap == 0 else float(near_won))
    if gap > 0:
        length_tiebreak = float(near_won)
    elif near_len == second_len:
        length_tiebreak = 0.5
    else:
        length_tiebreak = float(near_won == (near_len > second_len))
    return nearest, length_tiebreak


def summarize(rows, draws=BOOTSTRAPS, seed=SEED):
    verified = [r for r in rows if r["status"] == "confirmed"]
    grouped = defaultdict(lambda: [0, 0.0, 0.0])
    by_gap = defaultdict(lambda: [0, 0.0, 0.0])
    tied_length = Counter()
    steps = Counter()
    for r in verified:
        base, altered = score(r)
        sha = r["sha"]
        group = grouped[sha]
        group[0] += 1
        group[1] += base
        group[2] += altered
        group = by_gap[int(r["gap"])]
        group[0] += 1
        group[1] += base
        group[2] += altered
        if int(r["gap"]) == 0 and r["winner_class"] in TOP2:
            nl, sl = int(r["nearest_length"]), int(r["second_length"])
            relation = "near_longer" if nl > sl else "near_shorter" if nl < sl else "equal"
            tied_length[(relation, "first_wins" if r["winner_class"] in FIRST else "second_wins")] += 1
        if r["winner_class"] in TOP2:
            steps[(r["nearest_step"], r["second_step"],
                   "first_wins" if r["winner_class"] in FIRST else "second_wins")] += 1

    n = len(verified)
    total_base = sum(x[1] for x in grouped.values())
    total_altered = sum(x[2] for x in grouped.values())
    differences = []
    clusters = list(grouped.values())
    if clusters and draws > 0:
        rng = random.Random(seed)
        for _ in range(draws):
            sampled = rng.choices(clusters, k=len(clusters))
            denominator = sum(x[0] for x in sampled)
            if denominator:
                differences.append(
                    100.0 * sum(x[2]-x[1] for x in sampled)/denominator)
    differences.sort()
    def percentage(numerator, denominator):
        return 100.0 * numerator / denominator if denominator else None

    return dict(
        episodes=len(rows), confirmed=n, unique_replays=len(grouped),
        nearest_accuracy=percentage(total_base, n),
        tiebreak_accuracy=percentage(total_altered, n),
        improvement_pp=percentage(total_altered-total_base, n),
        ci_low=differences[int(0.025*len(differences))] if differences else None,
        ci_high=differences[min(len(differences)-1, int(0.975*len(differences)))] if differences else None,
        gaps={k:dict(n=v[0],nearest=percentage(v[1],v[0]),
                      tiebreak=percentage(v[2],v[0]))
              for k,v in sorted(by_gap.items())},
        tied_length=dict(tied_length),
        steps=dict(steps),
        top2_confirmed=sum(r["winner_class"] in TOP2 for r in verified),
        other_captures=sum(r["winner_class"] == "other" for r in verified))


def read_episodes(path):
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def build(data_dir, draws=BOOTSTRAPS):
    rows = read_episodes(data_dir/"derived"/"league_food_contests.csv")
    result = summarize(rows, draws=draws)
    def fmt(value):
        return f"{value:.1f}%" if value is not None else "insufficient"
    def pp(value):
        return f"{value:+.2f} pp" if value is not None else "insufficient"

    lines = [
        "# Snake26: apple contest pre-action prediction check", "",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"), "",
        "## Frozen predictors and population", "",
        "Compare two explicitly FIXED predictions on verified league captures:",
        "A) predict the nearer of the two closest student heads; when distances tie,",
        "assign half-credit rather than arbitrarily favoring a student ID.",
        "B) the same, but when distances tie, predict the LONGER of those two snakes;",
        "equal lengths also receive half-credit. A win by any other snake scores",
        "zero for both. This is expected classification credit, not an agent outcome.",
        "No future movement is an input to either predictor.", "",
        f"Eligible apple episodes: **{result['episodes']}**.",
        f"Verified captures: **{result['confirmed']}**; unverified/censored excluded: "
        f"**{result['episodes']-result['confirmed']}**.",
        f"Confirmed captures by one of two competitors: **{result['top2_confirmed']}**;",
        f"by a different student: **{result['other_captures']}**.",
        f"Distinct replay SHA clusters in verified set: **{result['unique_replays']}**.", "",
        "## Predicted capturer accuracy (verified episodes only)", "",
        "| Fixed rule | Expected accuracy |",
        "|---|---:|",
        f"| Geometric nearest, 50/50 at ties | {fmt(result['nearest_accuracy'])} |",
        f"| Nearest, break exact distance ties by longer body | {fmt(result['tiebreak_accuracy'])} |",
        f"| Difference | {pp(result['improvement_pp'])} |",
        "",
        f"Exploratory 95% cluster-bootstrap interval for accuracy difference: "
        f"**[{pp(result['ci_low'])}, {pp(result['ci_high'])}]**.",
        f"Resampled whole unique replay files ({draws} seeded draws), not turns or apple events.",
        "This interval does not adjust for repeated students, bot versions,",
        "similar seeds, match schedule or prior exploration of the same data.", "",
        "## Break down by initial distance gap", "",
        "| Initial distance gap | Confirmed apples | Nearest baseline | Length tie-break |",
        "|---|---:|---:|---:|"]
    for gap, value in result["gaps"].items():
        lines.append(f"| {gap} cells | {value['n']} | {fmt(value['nearest'])} | {fmt(value['tiebreak'])} |")
    lines += ["",
        "Distance tie is the ONLY stratum where the predictors differ.",
        "For distance gaps of 1 or 2 cells, both predict the nearer head;",
        "this does not claim that nearer is a safe or optimal movement policy.", "",
        "## At exact distance ties, what did recorded body length predict?", "",
        "| Initial body lengths | First head captured | Second head captured |",
        "|---|---:|---:|"]
    for code, label in [("near_longer", "First is longer"),
                        ("equal", "Equal length"),
                        ("near_shorter", "Second is longer")]:
        lines.append(f"| {label} | {result['tied_length'].get((code,'first_wins'),0)} | "
                     f"{result['tied_length'].get((code,'second_wins'),0)} |")
    lines += ["",
        "## Actual first moves (retrospective description ONLY)", "",
        "This section uses observed next-frame moves and is NOT available to",
        "either pre-action predictor. A snake moving closer is not evidence",
        "of deliberate pursuit or that imitating its move would cause success.", "",
        "| First head step | Second head step | First head captured | Second head captured |",
        "|---|---|---:|---:|"]
    for a in ("closer", "farther", "sideways", "missing", "died"):
        for b in ("closer", "farther", "sideways", "missing", "died"):
            x = result["steps"].get((a,b,"first_wins"),0)
            y = result["steps"].get((a,b,"second_wins"),0)
            if x+y:
                lines.append(f"| {a} | {b} | {x} | {y} |")
    lines += ["",
        "## What this does NOT establish", "",
        "- More length at equal distance is predictive, not proof that choosing",
        "  an apple race based on length increases score or survival.",
        "- Distance ignores occupied-path geometry, future turns, and opponent choices.",
        "- Current results are selected archived games and may overlap competitor versions.",
        "- A real agent's utility must include death/reset risk, retained growth, and",
        "  league placement, evaluated on unseen games and diverse opponents.",
        "- Palmer remains in the main evidence, with its separately audited",
        "  [casebook](palmer_casebook.md) and [apple episodes](league_food_contests.md).",
        "", "[Raw episode CSV](../derived/league_food_contests.csv).",
        "**No competition Snake AI was modified.**", ""
    ]
    out = data_dir/"reports"/"league_food_prediction.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    return dict(report=str(out), **{k:result[k] for k in
                                  ("episodes","confirmed","unique_replays","improvement_pp",
                                   "ci_low","ci_high")})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--bootstrap", type=int, default=BOOTSTRAPS)
    args = parser.parse_args()
    if args.bootstrap < 0:
        parser.error("bootstrap draws must be >=0")
    print(json.dumps(build(args.data_dir, draws=args.bootstrap), indent=2))


if __name__ == "__main__":
    main()
