from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts" / "reference-audit.py"
SPEC = importlib.util.spec_from_file_location("reference_audit", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)

HIGH = {
    "file": "skills/example/references/a.md",
    "line": 3,
    "quote": "See [b](b.md) for tables.",
    "kind": "stale-pointer",
    "confidence": "high",
    "related": "skills/example/references/b.md:1",
    "explanation": "b.md has no tables.",
    "suggestion": "Link to c.md.",
}


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


class ReferenceAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name).resolve()
        references = self.root / "skills" / "example" / "references"
        references.mkdir(parents=True)
        (self.root / "docs").mkdir()
        (self.root / "docs" / "reference-audit.md").write_text("# Audit\n", encoding="utf-8")
        (self.root / "skills" / "example" / "SKILL.md").write_text(
            "# Example\n\n[a](references/a.md)\n", encoding="utf-8"
        )
        (references / "a.md").write_text("# A\n\nSee [b](b.md).\n", encoding="utf-8")
        (references / "b.md").write_text("# B\n", encoding="utf-8")
        (references / "c.md").write_text("# C\n\nBack to [a](a.md).\n", encoding="utf-8")
        (references / "d.md").write_text("# D\n", encoding="utf-8")
        git(self.root, "init", "-q", "-b", "main")
        git(self.root, "-c", "user.name=t", "-c", "user.email=t@example.com",
            "commit", "-q", "--allow-empty", "-m", "base")
        git(self.root, "add", "-A")
        git(self.root, "-c", "user.name=t", "-c", "user.email=t@example.com",
            "commit", "-q", "-m", "change")

        self.patches = [
            mock.patch.object(AUDIT, "ROOT", self.root),
            mock.patch.object(AUDIT, "PROMPT", self.root / "docs" / "reference-audit.md"),
            mock.patch.object(AUDIT, "CACHE", self.root / ".reference-audit-cache"),
        ]
        for patch in self.patches:
            patch.start()

    def tearDown(self) -> None:
        for patch in self.patches:
            patch.stop()
        self.temporary_directory.cleanup()

    def run_main(self, *args: str) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code = AUDIT.main(["--base", "HEAD~1", *args])
        return code, output.getvalue()

    def test_scopes_the_audit_to_changed_skill_markdown(self) -> None:
        self.assertEqual(
            AUDIT.changed_files("HEAD~1"),
            [
                "skills/example/SKILL.md",
                "skills/example/references/a.md",
                "skills/example/references/b.md",
                "skills/example/references/c.md",
                "skills/example/references/d.md",
            ],
        )

    def test_collects_the_router_link_targets_and_linking_files(self) -> None:
        self.assertEqual(
            AUDIT.related_files(["skills/example/references/a.md"]),
            [
                "skills/example/SKILL.md",
                "skills/example/references/b.md",
                "skills/example/references/c.md",
            ],
        )

    def test_fences_a_diff_that_contains_backticks(self) -> None:
        self.assertEqual(AUDIT.fenced("a ```` b", "diff"), "`````diff\na ```` b\n`````")

    def test_blocks_on_a_high_confidence_finding_and_caches_it(self) -> None:
        with mock.patch.object(AUDIT, "pick_harness", return_value="claude"), \
             mock.patch.object(AUDIT, "run_harness", return_value=[HIGH]) as run:
            first, output = self.run_main()
            second, cached = self.run_main()

        self.assertEqual((first, second), (1, 1))
        self.assertEqual(run.call_count, 1)
        self.assertIn("HIGH   stale-pointer skills/example/references/a.md:3", output)
        self.assertIn("cached claude result", cached)

    def test_medium_findings_are_advisory(self) -> None:
        finding = dict(HIGH, confidence="medium")
        with mock.patch.object(AUDIT, "pick_harness", return_value="codex"), \
             mock.patch.object(AUDIT, "run_harness", return_value=[finding]):
            code, output = self.run_main()

        self.assertEqual(code, 0)
        self.assertIn("advisory", output)

    def test_a_missing_harness_skips_without_blocking(self) -> None:
        with mock.patch.object(AUDIT, "pick_harness", return_value=None):
            code, output = self.run_main()

        self.assertEqual(code, 0)
        self.assertIn("skipping", output)

    def test_a_harness_error_does_not_block(self) -> None:
        with mock.patch.object(AUDIT, "pick_harness", return_value="claude"), \
             mock.patch.object(AUDIT, "run_harness", side_effect=AUDIT.HarnessError("boom")):
            code, output = self.run_main()

        self.assertEqual(code, 0)
        self.assertIn("boom; not blocking", output)
        self.assertFalse((self.root / ".reference-audit-cache").exists())

    def test_reads_claude_structured_output(self) -> None:
        envelope = json.dumps({"is_error": False, "structured_output": {"findings": [HIGH]}})
        self.assertEqual(
            AUDIT.parse_output("claude", envelope, self.root / "unused"),
            {"findings": [HIGH]},
        )

    def test_reports_a_claude_error_envelope(self) -> None:
        envelope = json.dumps({"is_error": True, "result": "not logged in"})
        with self.assertRaisesRegex(AUDIT.HarnessError, "not logged in"):
            AUDIT.parse_output("claude", envelope, self.root / "unused")

    def test_reads_the_codex_last_message_file(self) -> None:
        output = self.root / "last.json"
        output.write_text(json.dumps({"findings": []}), encoding="utf-8")
        self.assertEqual(AUDIT.parse_output("codex", "", output), {"findings": []})


if __name__ == "__main__":
    unittest.main()
