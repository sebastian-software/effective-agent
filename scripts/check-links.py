#!/usr/bin/env python3
"""Run lychee, checking our own site and main-branch file URLs in this checkout.

This validates new page and repository file links before deployment or merge.
All other URLs retain lychee's normal network checks and the caller's strict
or CI-specific settings.
"""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check-links.py LYCHEE [options]", file=sys.stderr)
        return 2
    site_remap = rf"^https://skills\.sebastian-software\.com/(.*)$ {(ROOT / 'site').as_uri()}/$1"
    repository_remap = (
        r"^https://github\.com/sebastian-software/skills\.sebastian-software\.com/blob/main/(.*)$ "
        f"{ROOT.as_uri()}/$1"
    )
    return subprocess.call([
        sys.argv[1], "--remap", site_remap, "--remap", repository_remap,
        "--index-files", "index.html",
        *sys.argv[2:],
    ], cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
