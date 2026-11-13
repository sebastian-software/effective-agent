from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "effective-delivery" / "scripts" / "worktree_cleanup.py"
GIT_ENV = dict(
    os.environ,
    GIT_AUTHOR_NAME="Test",
    GIT_AUTHOR_EMAIL="test@example.com",
    GIT_COMMITTER_NAME="Test",
    GIT_COMMITTER_EMAIL="test@example.com",
    GIT_CONFIG_GLOBAL=os.devnull,
    GIT_CONFIG_SYSTEM=os.devnull,
)
CAN_SEE_PROCESSES = bool(shutil.which("lsof")) or os.path.isdir("/proc/self")


class WorktreeCleanupTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        base = Path(self.directory.name).resolve()
        self.workspace = base / "workspace"
        self.repo = self.workspace / "group" / "my repo"
        self.repo.mkdir(parents=True)
        self.report = base / "report.json"
        self.git("init", "-q", "-b", "main")
        (self.repo / "a.txt").write_text("a\n", encoding="utf-8")
        (self.repo / ".gitignore").write_text(".env.local\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-q", "-m", "init")

    def git(self, *args: str, cwd: Path | None = None) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd or self.repo,
            env=GIT_ENV,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def add_worktree(self, name: str) -> Path:
        path = self.repo / ".claude" / "worktrees" / name
        self.git("worktree", "add", "-q", "-b", "b-" + name, str(path))
        return path

    def commit_in(self, path: Path, filename: str, message: str) -> None:
        (path / filename).write_text(message + "\n", encoding="utf-8")
        self.git("add", ".", cwd=path)
        self.git("commit", "-q", "-m", message, cwd=path)

    def run_script(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=cwd,
            env=GIT_ENV,
            capture_output=True,
            text=True,
        )

    def scan(self) -> dict[str, dict]:
        result = self.run_script(
            "scan", "--root", str(self.workspace), "--out", str(self.report),
            "--no-fetch", "--no-gh", "--no-sizes",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(self.report.read_text(encoding="utf-8"))
        self.assertEqual(len(report["repos"]), 1)
        return {wt["name"]: wt for wt in report["repos"][0]["worktrees"]}

    def remove(self, *args: str) -> subprocess.CompletedProcess[str]:
        return self.run_script("remove", "--report", str(self.report), "--no-gh", *args)

    def branches(self) -> set[str]:
        return set(self.git("for-each-ref", "--format=%(refname:short)", "refs/heads").split())

    def test_scan_classifies_each_state(self) -> None:
        self.add_worktree("ancestor")
        squash = self.add_worktree("squash")
        self.commit_in(squash, "s1.txt", "first")
        self.commit_in(squash, "s2.txt", "second")
        self.git("merge", "-q", "--squash", "b-squash")
        self.git("commit", "-q", "-m", "squashed")
        unmerged = self.add_worktree("unmerged")
        self.commit_in(unmerged, "u.txt", "open work")
        dirty = self.add_worktree("dirty")
        (dirty / "new.txt").write_text("wip\n", encoding="utf-8")
        noise = self.add_worktree("noise")
        (noise / "node_modules").mkdir()
        (noise / "node_modules" / "x.js").write_text("x\n", encoding="utf-8")
        stale = self.add_worktree("stale")
        finished = subprocess.Popen([sys.executable, "-c", "pass"])
        finished.wait()
        self.git("worktree", "lock", "--reason", f"agent (pid {finished.pid})", str(stale))
        manual = self.add_worktree("manual")
        self.git("worktree", "lock", "--reason", "keep for the demo", str(manual))
        gone = self.add_worktree("gone")
        shutil.rmtree(gone)

        found = self.scan()

        self.assertEqual(
            {name: wt["class"] for name, wt in found.items()},
            {
                "ancestor": "done", "squash": "done", "unmerged": "unmerged",
                "dirty": "dirty", "noise": "done", "stale": "done",
                "manual": "busy", "gone": "missing",
            },
        )
        self.assertEqual(found["squash"]["merged_via"], "content already in main")
        self.assertEqual(found["noise"]["untracked_noise"], ["node_modules"])
        self.assertEqual(found["stale"]["lock"]["kind"], "stale")
        self.assertEqual(found["unmerged"]["ahead"], 1)

    def test_remove_done_deletes_branch_and_records_how_to_restore_it(self) -> None:
        done = self.add_worktree("done")
        noise = self.add_worktree("noise")
        (noise / "node_modules").mkdir()
        tip = self.scan()["done"]["tip"]

        result = self.remove("--classes", "done,missing")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(done.exists())
        self.assertFalse(noise.exists())
        self.assertEqual(self.branches(), {"main"})
        self.assertIn(f"branch 'b-done' {tip}", result.stdout)
        record = json.loads(self.report.with_suffix(".removed.json").read_text(encoding="utf-8"))
        self.assertEqual({entry["branch"] for entry in record["removed"]}, {"b-done", "b-noise"})
        self.assertTrue(all(entry["branch_deleted"] for entry in record["removed"]))

    def test_dirty_worktree_stays_even_when_named(self) -> None:
        dirty = self.add_worktree("dirty")
        (dirty / "new.txt").write_text("wip\n", encoding="utf-8")
        self.scan()

        result = self.remove("--classes", "done", "--include", str(dirty))

        self.assertIn("class dirty is never removed", result.stdout)
        self.assertTrue((dirty / "new.txt").exists())
        self.assertIn("b-dirty", self.branches())

    def test_worktree_changed_since_the_scan_is_skipped(self) -> None:
        done = self.add_worktree("done")
        self.scan()
        (done / "late.txt").write_text("late\n", encoding="utf-8")

        result = self.remove("--classes", "done")

        self.assertIn("changed since the scan (done -> dirty", result.stdout)
        self.assertTrue((done / "late.txt").exists())

    def test_unmerged_needs_include_and_keeps_its_branch(self) -> None:
        unmerged = self.add_worktree("unmerged")
        self.commit_in(unmerged, "u.txt", "open work")
        self.scan()

        self.remove("--classes", "done")
        self.assertTrue(unmerged.exists())

        result = self.remove("--include", str(unmerged))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(unmerged.exists())
        self.assertIn("b-unmerged", self.branches())

    def test_unique_ignored_file_blocks_removal_until_named(self) -> None:
        done = self.add_worktree("done")
        (done / ".env.local").write_text("SECRET=1\n", encoding="utf-8")
        found = self.scan()
        self.assertEqual(found["done"]["class"], "done")
        self.assertEqual(found["done"]["notable_ignored"], [".env.local"])

        result = self.remove("--classes", "done")
        self.assertIn("ignored files that exist only here", result.stdout)
        self.assertTrue(done.exists())

        self.remove("--include", str(done))
        self.assertFalse(done.exists())

    def test_classes_rejects_everything_but_done_and_missing(self) -> None:
        self.add_worktree("done")
        self.scan()

        result = self.remove("--classes", "unmerged")

        self.assertEqual(result.returncode, 2)
        self.assertIn("--classes accepts done and missing only", result.stderr)

    def test_dry_run_removes_nothing(self) -> None:
        done = self.add_worktree("done")
        self.scan()

        result = self.remove("--classes", "done", "--dry-run")

        self.assertIn("would remove", result.stdout)
        self.assertTrue(done.exists())
        self.assertIn("b-done", self.branches())

    def test_worktree_the_helper_is_started_from_is_protected(self) -> None:
        own = self.add_worktree("own")

        result = self.run_script(
            "scan", "--root", str(self.workspace), "--out", str(self.report),
            "--no-fetch", "--no-gh", "--no-sizes",
            cwd=own,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(self.report.read_text(encoding="utf-8"))
        found = report["repos"][0]["worktrees"][0]
        self.assertEqual(found["class"], "busy")
        self.assertIn(f"protected: {own}", found["reasons"])

    @unittest.skipUnless(CAN_SEE_PROCESSES, "needs lsof or /proc")
    def test_worktree_with_a_process_inside_is_busy(self) -> None:
        busy = self.add_worktree("busy")
        process = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"], cwd=busy)
        self.addCleanup(process.wait)
        self.addCleanup(process.kill)

        found = self.scan()
        result = self.remove("--classes", "done", "--include", str(busy))

        self.assertEqual(found["busy"]["class"], "busy")
        self.assertIn("in use by", found["busy"]["reasons"][0])
        self.assertTrue(busy.exists())
        self.assertIn("class busy is never removed", result.stdout)


if __name__ == "__main__":
    unittest.main()
