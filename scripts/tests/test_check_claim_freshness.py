from __future__ import annotations

from datetime import date
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "check_claim_freshness", ROOT / "scripts/check-claim-freshness.py"
)
freshness = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = freshness
SPEC.loader.exec_module(freshness)


class MarkerDateTests(unittest.TestCase):
    def test_reads_month_period_and_year_markers(self) -> None:
        self.assertEqual(freshness.marker_dates("Chromium-only as of October 2026."),
                         [date(2026, 10, 1)])
        self.assertEqual(freshness.marker_dates("as of early 2026"), [date(2026, 2, 1)])
        self.assertEqual(freshness.marker_dates("as of 2025"), [date(2025, 7, 1)])

    def test_reads_iso_markers(self) -> None:
        self.assertEqual(freshness.marker_dates("Snapshot date: **2026-07-16**."),
                         [date(2026, 7, 16)])
        self.assertEqual(freshness.marker_dates("At last review (2026-07-22), LinkedIn"),
                         [date(2026, 7, 22)])
        self.assertEqual(freshness.marker_dates("met this when checked in October 2026"),
                         [date(2026, 10, 1)])

    def test_ignores_lines_without_markers(self) -> None:
        self.assertEqual(freshness.marker_dates("Baseline 2023 feature, Chrome 111+."), [])


class ScanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)

    def tearDown(self) -> None:
        self.directory.cleanup()

    def write(self, name: str, text: str) -> Path:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_reports_only_claims_older_than_the_limit(self) -> None:
        self.write("a.md", "Old: Chromium-only as of January 2026.\n"
                           "New: Chromium-only as of October 2026.\n")
        code = freshness.main([str(self.root), "--today", "2026-10-14",
                               "--max-age-days", "180", "--strict"])
        self.assertEqual(code, 1)
        code = freshness.main([str(self.root), "--today", "2026-10-14",
                               "--max-age-days", "365", "--strict"])
        self.assertEqual(code, 0)

    def test_lists_undated_support_claims_outside_snapshot_files(self) -> None:
        self.write("undated.md", "`initial-letter` is Limited availability (Chrome 110+).\n"
                                  "| Limited availability | Do not depend on it |\n")
        self.write("radar.md", "Snapshot date: **2026-10-14**.\n\n- `x` is Limited availability in Safari.\n")
        dated, undated = freshness.scan(freshness.markdown_files([self.root]))
        self.assertEqual([(claim.path.name, claim.line) for claim in undated], [("undated.md", 1)])
        self.assertEqual([claim.path.name for claim in dated], ["radar.md"])

    def test_skips_eval_fixtures(self) -> None:
        self.write("skill/evals/cases.md", "Chromium-only as of January 2020.\n")
        self.assertEqual(freshness.markdown_files([self.root]), [])


if __name__ == "__main__":
    unittest.main()
