#!/usr/bin/env python3
"""Audit changed skill guidance with a local coding harness before a push.

The deterministic validators check that links and named sections resolve. This
audit asks `claude` or `codex` whether changed guidance still points at content
that exists and agrees with the rest of its skill. It reviews only the commits
being pushed, caches results per change, and fails when a finding is
high-confidence. A missing harness or a harness error never blocks a push.

The prompt lives in docs/reference-audit.md; see docs/contributor-checks.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "docs" / "reference-audit.md"
CACHE = ROOT / ".reference-audit-cache"
SCOPE = ("skills/", "instructions/")
HARNESSES = ("claude", "codex")
TIMEOUT_SECONDS = 900
LINK = re.compile(r"\]\(([^)\s#]+\.md)(?:#[^)]*)?\)")

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["findings"],
    "properties": {
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "file",
                    "line",
                    "quote",
                    "kind",
                    "confidence",
                    "related",
                    "explanation",
                    "suggestion",
                ],
                "properties": {
                    "file": {"type": "string"},
                    "line": {"type": "integer"},
                    "quote": {"type": "string"},
                    "kind": {
                        "type": "string",
                        "enum": ["stale-pointer", "contradiction", "relative-phrasing"],
                    },
                    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                    "related": {"type": "string"},
                    "explanation": {"type": "string"},
                    "suggestion": {"type": "string"},
                },
            },
        }
    },
}


class HarnessError(Exception):
    pass


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


def default_base() -> str:
    """Return the upstream branch, else the merge base with the default branch."""
    for args in (
        ("rev-parse", "--verify", "--quiet", "@{upstream}"),
        ("merge-base", "HEAD", "origin/HEAD"),
        ("merge-base", "HEAD", "origin/main"),
        ("merge-base", "HEAD", "main"),
    ):
        try:
            base = git(*args).strip()
        except subprocess.CalledProcessError:
            continue
        if base:
            return base
    raise SystemExit("reference-audit: no upstream or main branch to compare with; pass --base")


def in_scope(path: str) -> bool:
    return path.endswith(".md") and path.startswith(SCOPE)


def changed_files(base: str) -> list[str]:
    output = git("diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD")
    return sorted(path for path in output.splitlines() if in_scope(path))


def linked_paths(markdown: Path) -> set[str]:
    found: set[str] = set()
    for target in LINK.findall(markdown.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://")):
            continue
        destination = (markdown.parent / target).resolve()
        if destination.is_file() and destination.is_relative_to(ROOT):
            found.add(destination.relative_to(ROOT).as_posix())
    return found


def related_files(changed: list[str]) -> list[str]:
    """Return the router, link targets, and linking files of each changed file."""
    related: set[str] = set()
    changed_set = set(changed)
    for path in changed:
        markdown = ROOT / path
        if not markdown.is_file():
            continue
        related |= linked_paths(markdown)
        parts = Path(path).parts
        if parts[0] == "skills" and len(parts) > 2:
            skill = ROOT / parts[0] / parts[1]
            if (skill / "SKILL.md").is_file():
                related.add(f"{parts[0]}/{parts[1]}/SKILL.md")
            for candidate in sorted(skill.rglob("*.md")):
                if path in linked_paths(candidate):
                    related.add(candidate.relative_to(ROOT).as_posix())
    return sorted(path for path in related - changed_set if in_scope(path))


def fenced(text: str, language: str = "") -> str:
    longest = max((len(run) for run in re.findall(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}{language}\n{text.rstrip()}\n{fence}"


def build_prompt(base: str, changed: list[str], related: list[str], diff: str) -> str:
    listing = lambda paths: "\n".join(f"- {path}" for path in paths) or "- (none)"
    return (
        f"{PROMPT.read_text(encoding='utf-8').rstrip()}\n\n"
        "## Change under review\n\n"
        f"Compared with `{base}`.\n\n"
        f"Changed files:\n\n{listing(changed)}\n\n"
        f"Related files (router, link targets, and files linking here):\n\n{listing(related)}\n\n"
        f"Diff:\n\n{fenced(diff, 'diff')}\n"
    )


def pick_harness(requested: str) -> str | None:
    if requested != "auto":
        return requested if shutil.which(requested) else None
    return next((name for name in HARNESSES if shutil.which(name)), None)


def harness_command(name: str, model: str | None, schema_path: Path, output_path: Path) -> list[str]:
    if name == "claude":
        command = [
            "claude", "-p",
            "--output-format", "json",
            "--json-schema", json.dumps(SCHEMA),
            "--tools", "Read,Grep,Glob",
            "--allowedTools", "Read,Grep,Glob",
            "--strict-mcp-config",
            "--no-session-persistence",
        ]
        return command + (["--model", model] if model else [])
    command = [
        "codex", "exec",
        "--sandbox", "read-only",
        "--ephemeral",
        "--cd", str(ROOT),
        "--output-schema", str(schema_path),
        "--output-last-message", str(output_path),
    ]
    return command + (["--model", model] if model else []) + ["-"]


def parse_output(name: str, stdout: str, output_path: Path) -> dict:
    try:
        if name == "claude":
            envelope = json.loads(stdout)
            if envelope.get("is_error"):
                raise HarnessError(str(envelope.get("result") or "claude reported an error"))
            result = envelope.get("structured_output")
            return result if isinstance(result, dict) else json.loads(envelope["result"])
        return json.loads(output_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, KeyError, OSError) as error:
        raise HarnessError(f"unreadable {name} output: {error}") from error


def run_harness(name: str, model: str | None, prompt: str) -> list[dict]:
    with tempfile.TemporaryDirectory() as directory:
        schema_path = Path(directory) / "schema.json"
        output_path = Path(directory) / "result.json"
        schema_path.write_text(json.dumps(SCHEMA), encoding="utf-8")
        try:
            completed = subprocess.run(
                harness_command(name, model, schema_path, output_path),
                cwd=ROOT,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired as error:
            raise HarnessError(f"{name} did not finish within {TIMEOUT_SECONDS} s") from error
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout).strip().splitlines()[-1:] or [""]
            raise HarnessError(f"{name} exited with {completed.returncode}: {detail[0]}")
        result = parse_output(name, completed.stdout, output_path)
    findings = result.get("findings") if isinstance(result, dict) else None
    if not isinstance(findings, list) or not all(isinstance(item, dict) for item in findings):
        raise HarnessError(f"{name} returned no findings list")
    return findings


def report(findings: list[dict]) -> int:
    """Print findings, most confident first, and return the number of blocking ones."""
    order = {"high": 0, "medium": 1, "low": 2}
    for finding in sorted(findings, key=lambda item: order.get(item.get("confidence"), 3)):
        print(
            f"{str(finding.get('confidence', '?')).upper():6} {finding.get('kind', '?')} "
            f"{finding.get('file', '?')}:{finding.get('line', '?')}"
        )
        if finding.get("quote"):
            print(f"       \"{finding['quote']}\"")
        for label in ("related", "explanation", "suggestion"):
            if finding.get(label):
                print(f"       {label}: {finding[label]}")
    return sum(1 for finding in findings if finding.get("confidence") == "high")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", help="commit to compare with (default: upstream, else main)")
    parser.add_argument(
        "--harness",
        choices=("auto", *HARNESSES),
        default=os.environ.get("REFERENCE_AUDIT_HARNESS", "auto"),
    )
    parser.add_argument("--model", default=os.environ.get("REFERENCE_AUDIT_MODEL") or None)
    parser.add_argument("--no-cache", action="store_true", help="ignore a cached result")
    parser.add_argument("--print-prompt", action="store_true", help="print the prompt and exit")
    args = parser.parse_args(argv)

    base = args.base or default_base()
    changed = changed_files(base)
    if not changed:
        print("reference-audit: no skill or instruction-pack Markdown changed")
        return 0

    diff = git("diff", f"{base}...HEAD", "--", *changed)
    prompt = build_prompt(base, changed, related_files(changed), diff)
    if args.print_prompt:
        print(prompt)
        return 0

    harness = pick_harness(args.harness)
    if harness is None:
        print("reference-audit: no claude or codex CLI found; skipping the audit")
        return 0

    key = hashlib.sha256(
        "\0".join((harness, args.model or "", prompt)).encode("utf-8")
    ).hexdigest()
    cache_file = CACHE / f"{key}.json"
    if cache_file.is_file() and not args.no_cache:
        findings = json.loads(cache_file.read_text(encoding="utf-8"))
        print(f"reference-audit: cached {harness} result for {len(changed)} changed file(s)")
    else:
        print(f"reference-audit: auditing {len(changed)} changed file(s) with {harness}…", flush=True)
        try:
            findings = run_harness(harness, args.model, prompt)
        except HarnessError as error:
            print(f"reference-audit: {error}; not blocking the push", file=sys.stderr)
            return 0
        CACHE.mkdir(exist_ok=True)
        cache_file.write_text(json.dumps(findings, indent=2), encoding="utf-8")

    if not findings:
        print("reference-audit: no findings")
        return 0
    blocking = report(findings)
    if blocking:
        print(
            f"reference-audit: {blocking} high-confidence finding(s). Fix them, or push "
            "with --no-verify when a finding is wrong."
        )
        return 1
    print("reference-audit: findings above are advisory")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
