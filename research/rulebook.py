"""Render falsifiable Snake26 algorithm-rule candidates, never auto-promote.

No Java code is generated. Each hypothesis requires transparent evidence and
holdout testing before it may become an implementation decision.
"""
from __future__ import annotations
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
import argparse,json,re

REQUIRED=("id","title","stage","domain","mode","if_state","then_hypothesis",
          "evidence","counterexample","next_experiment","falsification")
STAGES={0:"Open question",1:"Observed association",2:"Replicated predictor",
        3:"Controlled candidate",4:"Promoted rule"}

def read_registry(path):
    source=json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(source,dict) or source.get("version")!=1:
        raise ValueError("Only version 1 research registries are supported")
    records=source.get("rules")
    if not isinstance(records,list):
        raise ValueError("rules must be a list")
    seen=set()
    for rule in records:
        if not isinstance(rule,dict) or any(k not in rule for k in REQUIRED):
            raise ValueError("Missing required hypothesis fields")
        if not isinstance(rule["stage"],int) or rule["stage"] not in STAGES:
            raise ValueError("Invalid evidence stage")
        if not isinstance(rule["id"],str) or not re.fullmatch(r"[A-Z]+-\d+",rule["id"]):
            raise ValueError("Invalid rule identifier")
        if rule["id"] in seen:raise ValueError("Duplicate rule identifiers")
        seen.add(rule["id"])
        if rule["mode"] not in ("league","trial","both"):
            raise ValueError("Invalid research mode")
        if not isinstance(rule["evidence"],list) or any(
                not isinstance(x,str) or not x.startswith("data/reports/")
                or not x.endswith(".md") for x in rule["evidence"]):
            raise ValueError("Evidence paths must refer to internal reports")
        if rule["stage"]>=1 and not rule["evidence"]:
            raise ValueError("Observed associations require an evidence source")
        if rule["stage"]>=2 and not rule.get("holdout_validation"):
            raise ValueError("Stage 2+ requires explicit held-out validation record")
        if rule["stage"]>=3 and not rule.get("controlled_ablation"):
            raise ValueError("Stage 3+ requires controlled agent test record")
        if rule["stage"]==4 and not rule.get("fresh_paired_seed_validation"):
            raise ValueError("Stage 4 requires fresh paired-seed league-like result")
        for key in ("title","if_state","then_hypothesis","counterexample",
                    "next_experiment","falsification"):
            if not isinstance(rule[key],str) or not rule[key].strip():
                raise ValueError("Missing substantive hypothesis description")
    return records

def md(s):
    return str(s).replace("|",r"\|").replace("\n"," ").strip()

def build(data_dir,registry=None):
    data_dir=Path(data_dir)
    path=Path(registry) if registry else Path(__file__).with_name("rule_candidates.json")
    records=read_registry(path)
    counts=Counter(r["stage"] for r in records)
    lines=[
        "# Snake26 — Evidence-gated algorithm rulebook","",
        "Generated UTC: "+datetime.now(timezone.utc).isoformat(timespec="seconds"),"",
        "**Purpose:** build a NEW snake from cross-competitor research, NOT",
        "fix the existing submission or clone a particular league leader.",
        "Strong snakes (including Palmer), mid-field snakes, struggling",
        "snakes and benchmark specialists are all evidence sources.",
        "",
        f"Registered questions: **{len(records)}**. Open: **{counts[0]}**. "
        f"Observed association: **{counts[1]}**. "
        f"Controlled / promoted: **{counts[3]+counts[4]}**.","",
        "## Candidate decisions and evidence stages","",
        "| ID | Decision | Applicable evidence | Stage | Why still provisional |",
        "|---|---|---|---|---|"]
    for item in records:
        lines.append(f"| {item['id']} | {md(item['title'])} | {item['mode']} | "
                     f"{STAGES[item['stage']]} | "
                     f"{md(item['next_experiment'])} |")
    lines+=["",
        "## State-to-action hypotheses, counterexamples and falsification tests",""]
    for item in records:
        lines.extend([
            f"### {item['id']} — {item['title']}","",
            f"**Evidence stage:** {item['stage']} — {STAGES[item['stage']]}. "
            f"**Domain:** {item['domain']}. **Scope:** {item['mode']}.","",
            f"**When:** {item['if_state']}","",
            f"**Then, HYPOTHESIS only:** {item['then_hypothesis']}","",
            f"**Known counterexample / limitation:** {item['counterexample']}","",
            f"**Next needed measurement:** {item['next_experiment']}","",
            f"**Falsify if:** {item['falsification']}","",
            "**Supporting reports:** "+
            (", ".join(f"[{Path(x).stem}]({Path(x).name})" for x in item["evidence"])
             if item["evidence"] else "none yet — mechanics or behavioral research needed"),
            "",
        ])
    lines += [
        "## Promotion gates","",
        "0. **Open:** question and measurable variables established.",
        "1. **Observed:** source-linked analysis with denominators, caveats",
        "   and failure cases, kept league and trials separate.",
        "2. **Replicated:** whole unseen games / seasons / opponents; guard",
        "   bot-version leakage and confounding.",
        "3. **Controlled:** new independent Java candidate improves league-like",
        "   competitive scores in a reproducible ablation.",
        "4. **Promoted:** repeated fresh paired-seed evaluation, no major",
        "   regression in survival, retained growth, or runtime.",
        "",
        "No stage automatically advances when a dashboard is rebuilt.",
        "Raw replay correlation does not prove a different move would work.",
        "",
        "[Full research protocol](../../docs/ALGORITHM_RESEARCH_PROTOCOL.md).",
        "[All-student cohort comparison](competitive_cohorts.md).",
        "[Controlled league/trial comparison](league_vs_trials.md).",
        "",
        "**No Java competitor code is modified by this report.**",""]
    target=data_dir/"reports"/"algorithm_rulebook.md"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text("\n".join(lines),encoding="utf-8")
    return dict(rules=len(records),stages=dict(counts),report=str(target))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    p.add_argument("--registry",type=Path)
    args=p.parse_args()
    print(json.dumps(build(args.data_dir,args.registry),indent=2))

if __name__=="__main__":
    main()
