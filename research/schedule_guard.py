"""Polite schedule guard: avoid redundant Wits fetches on a backup cron slot.

Both primary and backup GitHub Actions schedules may run late or be skipped.
The on-disk last successful archive timestamp decides whether to collect.
Concurrency is separately enforced by the GitHub workflow.
"""
from datetime import datetime,timezone
from pathlib import Path
import argparse
import os
import re

TIMESTAMP=re.compile(r"^Generated \(UTC\): ([^\r\n]+)",re.MULTILINE)

def parse_generated(text):
    match=TIMESTAMP.search(text or "")
    if not match:
        return None
    try:
        value=datetime.fromisoformat(match.group(1).strip())
        if value.tzinfo is None:
            return None
        return value.astimezone(timezone.utc)
    except (ValueError,TypeError):
        return None

def should_collect(last,now=None,minimum_age_minutes=50,force=False):
    """Only a new ARCHIVE publication counts, not a code-only commit."""
    if force or last is None:
        return True
    now=(now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    seconds=(now-last.astimezone(timezone.utc)).total_seconds()
    if seconds< -300:
        # Timestamp from the future due to corrupt clocks is suspect.
        return True
    return seconds>=minimum_age_minutes*60

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report",type=Path,default=Path("data/reports/latest.md"))
    parser.add_argument("--min-age",type=int,default=50)
    args=parser.parse_args()
    if args.min_age<1:
        parser.error("min-age must be positive")
    try:
        last=parse_generated(args.report.read_text(encoding="utf-8"))
    except OSError:
        last=None
    force=os.environ.get("GITHUB_EVENT_NAME")=="workflow_dispatch"
    collect=should_collect(last,minimum_age_minutes=args.min_age,force=force)
    print("Latest archived publication:",last.isoformat() if last else "unknown")
    print("Forced manually:",force)
    print("Collector needed:",collect)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"],"a",encoding="utf-8") as f:
            f.write("collect="+("true" if collect else "false")+"\n")
    else:
        print("collect="+("true" if collect else "false"))

if __name__=="__main__":
    main()
