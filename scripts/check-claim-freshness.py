#!/usr/bin/env python3
"""Report dated claims in skill guidance that are due for re-verification.

Volatile guidance (browser support short of Baseline Widely available, vendor
behavior, platform limits, tool pins) carries a date such as "as of October
2026", a "Snapshot date: **YYYY-MM-DD**" header, or a "Last verified" field.
This script finds those dates and reports every one older than the allowed
age. With --undated it also lists support-status claims that name a browser
engine or version but carry no date at all.

The check reads files only; it never fetches sources or edits guidance.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
import os
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATHS = ("skills", "instructions")
DEFAULT_MAX_AGE_DAYS = 180

MONTHS = {
    name: number
    for number, name in enumerate(
        ("january", "february", "march", "april", "may", "june", "july",
         "august", "september", "october", "november", "december"),
        start=1,
    )
}
MONTH = "(" + "|".join(MONTHS) + ")"
PERIOD = {"early": 2, "mid": 6, "late": 10}

ISO_MARKERS = (
    re.compile(r"snapshot date:\s*\**\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE),
    re.compile(
        r"(?:last verified|verified|last reviewed|at last review|checked)\D{0,20}?"
        r"(\d{4}-\d{2}-\d{2})",
        re.IGNORECASE,
    ),
)
AS_OF = re.compile(
    r"\bas of\s+(?:(early|mid|late)\s+)?(?:" + MONTH + r"\s+)?(\d{4})\b",
    re.IGNORECASE,
)
CHECKED_IN = re.compile(
    r"\b(?:verified|checked|reviewed)\s+in\s+" + MONTH + r"\s+(\d{4})\b",
    re.IGNORECASE,
)
SUPPORT_STATUS = re.compile(
    r"limited availability|chromium-only|safari only|single-engine|"
    r"behind a flag|not yet (?:supported|widely)|"
    r"\b(?:no|not) (?:firefox|safari|chrome|chromium)\b",
    re.IGNORECASE,
)
ENGINE = re.compile(r"\b(?:chrome|chromium|safari|firefox|edge|webkit|gecko)\b|\b\d{2,3}\+",
                    re.IGNORECASE)


@dataclass(frozen=True)
class Claim:
    path: Path
    line: int
    dated: date | None
    text: str


def marker_dates(line: str) -> list[date]:
    """Return every verification date written on one line."""
    found: list[date] = []
    for pattern in ISO_MARKERS:
        for match in pattern.finditer(line):
            try:
                found.append(date.fromisoformat(match.group(1)))
            except ValueError:
                continue
    for match in AS_OF.finditer(line):
        period, month, year = match.groups()
        if month:
            found.append(date(int(year), MONTHS[month.lower()], 1))
        elif period:
            found.append(date(int(year), PERIOD[period.lower()], 1))
        else:
            found.append(date(int(year), 7, 1))
    for match in CHECKED_IN.finditer(line):
        month, year = match.groups()
        found.append(date(int(year), MONTHS[month.lower()], 1))
    return found


def markdown_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix == ".md":
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(p for p in path.rglob("*.md") if "evals" not in p.parts))
    return files


def scan(files: list[Path]) -> tuple[list[Claim], list[Claim]]:
    """Collect dated claims and, separately, undated support-status claims."""
    dated: list[Claim] = []
    undated: list[Claim] = []
    for path in files:
        lines = path.read_text(encoding="utf-8").splitlines()
        has_snapshot = any(ISO_MARKERS[0].search(line) for line in lines)
        for number, line in enumerate(lines, start=1):
            dates = marker_dates(line)
            if dates:
                dated.append(Claim(path, number, min(dates), line.strip()))
            elif not has_snapshot and SUPPORT_STATUS.search(line) and ENGINE.search(line):
                undated.append(Claim(path, number, None, line.strip()))
    return dated, undated


def relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def excerpt(text: str, limit: int = 140) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", type=Path,
                        help="files or directories to scan (default: skills, instructions)")
    parser.add_argument("--max-age-days", type=int, default=DEFAULT_MAX_AGE_DAYS)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today(),
                        help="reference date as YYYY-MM-DD (default: today)")
    parser.add_argument("--undated", action="store_true",
                        help="also list support-status claims without a date")
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 when any claim is due for re-verification")
    args = parser.parse_args(argv)

    paths = args.paths or [ROOT / name for name in DEFAULT_PATHS]
    dated, undated = scan(markdown_files(paths))
    stale = [c for c in dated if c.dated and (args.today - c.dated).days > args.max_age_days]
    annotate = os.environ.get("GITHUB_ACTIONS") == "true"

    for claim in stale:
        age = (args.today - claim.dated).days
        message = (f"verified {claim.dated.isoformat()} ({age} days ago); re-check the claim "
                   f"against its primary source and update the date: {excerpt(claim.text)}")
        if annotate:
            print(f"::warning file={relative(claim.path)},line={claim.line}::{message}")
        else:
            print(f"{relative(claim.path)}:{claim.line}: {message}")
    if args.undated:
        for claim in undated:
            message = f"support-status claim without a date: {excerpt(claim.text)}"
            if annotate:
                print(f"::notice file={relative(claim.path)},line={claim.line}::{message}")
            else:
                print(f"{relative(claim.path)}:{claim.line}: {message}")

    summary = (f"{len(dated)} dated claims, {len(stale)} older than {args.max_age_days} days"
               + (f", {len(undated)} undated support-status claims" if args.undated else ""))
    print(summary)
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as handle:
            handle.write(f"### Claim freshness\n\n{summary}.\n")
    return 1 if args.strict and stale else 0


if __name__ == "__main__":
    sys.exit(main())
