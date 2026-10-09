from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
LYCHEE = os.environ.get("LYCHEE_BIN") or shutil.which("lychee")


@unittest.skipUnless(LYCHEE, "lychee is required for link-check integration tests")
class CheckoutLinkTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        (self.root / "scripts").mkdir()
        shutil.copy2(ROOT / "scripts/check-links.py", self.root / "scripts/check-links.py")
        skill = self.root / "skills/new-skill"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("# New Skill\n\n## Route by Intent\n", encoding="utf-8")
        page = self.root / "site/skills/new-skill"
        page.mkdir(parents=True)
        (page / "index.html").write_text('<h1 id="install">Install</h1>', encoding="utf-8")
        (self.root / "lychee.toml").write_text('include_fragments = "anchor-only"\n', encoding="utf-8")

    def tearDown(self) -> None:
        self.directory.cleanup()

    def check(self, links: str) -> subprocess.CompletedProcess[str]:
        document = self.root / "links.md"
        document.write_text(links, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(self.root / "scripts/check-links.py"), LYCHEE,
             "--offline", "--config", str(self.root / "lychee.toml"), str(document)],
            cwd=self.root, capture_output=True, text=True, timeout=15,
        )

    def test_new_site_and_main_branch_files_are_checked_before_publication(self) -> None:
        result = self.check(
            "[Page](https://effective-agent.dev/skills/new-skill/#install)\n"
            "[Source](https://github.com/sebastian-software/effective-agent/blob/main/skills/new-skill/SKILL.md#route-by-intent)\n"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_main_branch_file_still_fails(self) -> None:
        result = self.check(
            "[Missing](https://github.com/sebastian-software/effective-agent/blob/main/skills/absent/SKILL.md)\n"
        )
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_main_branch_anchor_still_fails(self) -> None:
        result = self.check(
            "[Missing anchor](https://github.com/sebastian-software/effective-agent/blob/main/skills/new-skill/SKILL.md#absent)\n"
        )
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
