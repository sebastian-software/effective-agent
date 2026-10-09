from __future__ import annotations

import base64
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/effective-image/scripts/retouch_batch.py"
SPEC = importlib.util.spec_from_file_location("retouch_batch", SCRIPT)
retouch = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = retouch
SPEC.loader.exec_module(retouch)


class RetouchBatchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.client = mock.Mock()
        buffer = io.BytesIO()
        Image.new("RGB", (32, 48), "green").save(buffer, format="PNG")
        self.result_bytes = buffer.getvalue()
        self.client.images.edit.return_value = SimpleNamespace(data=[SimpleNamespace(
            b64_json=base64.b64encode(self.result_bytes).decode()
        )])
        self.factory = mock.Mock(return_value=self.client)

    def image(self, name: str) -> Path:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (32, 48), "red").save(path)
        return path

    def run_batch(self, argv: list[str]) -> int:
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "local-test-placeholder"}), \
                mock.patch.dict(sys.modules, {"openai": SimpleNamespace(OpenAI=self.factory)}), \
                contextlib.redirect_stdout(io.StringIO()):
            return retouch.main(argv)

    def assert_rejected(self, argv: list[str], message: str) -> None:
        before = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        with self.assertRaisesRegex(SystemExit, message):
            self.run_batch(argv)
        self.factory.assert_not_called()
        self.client.images.edit.assert_not_called()
        after = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(after, before, "preflight must leave every input and output untouched")

    def test_duplicate_stems_across_folders_abort_the_whole_batch(self) -> None:
        first = self.image("shoot-a/portrait.jpg")
        second = self.image("shoot-b/portrait.jpg")
        unique = self.image("shoot-a/other.jpg")
        self.assert_rejected([str(unique), str(first), str(second)], "Output collision")

    def test_duplicate_stems_across_formats_are_rejected_even_in_dry_run(self) -> None:
        self.image("shoot/portrait.jpg")
        self.image("shoot/portrait.png")
        self.assert_rejected([str(self.root / "shoot"), "--dry-run"], "Output collision")

    def test_force_never_overwrites_an_original(self) -> None:
        source = self.image("portrait.png")
        self.assert_rejected([
            str(source), "--out-dir", str(self.root), "--suffix", "", "--force"
        ], "would overwrite input")

    def test_output_cannot_overwrite_another_source_in_the_batch(self) -> None:
        source = self.image("portrait.jpg")
        other = self.image("portrait-retouched.png")
        self.assert_rejected([
            str(source), str(other), "--out-dir", str(self.root), "--force"
        ], "would overwrite input")

    def test_output_cannot_overwrite_a_color_reference(self) -> None:
        source = self.image("portrait.jpg")
        reference = self.image("portrait-retouched.png")
        self.assert_rejected([
            str(source), "--reference", str(reference), "--out-dir", str(self.root), "--force"
        ], "would overwrite input")

    def test_symlink_and_hardlink_outputs_cannot_overwrite_originals(self) -> None:
        for link_type in ("symlink", "hardlink"):
            with self.subTest(link_type=link_type):
                source = self.image(f"{link_type}/portrait.png")
                output = source.with_name("portrait-retouched.png")
                if link_type == "symlink":
                    output.symlink_to(source)
                else:
                    os.link(source, output)
                self.assert_rejected([
                    str(source), "--out-dir", str(source.parent), "--force"
                ], "would overwrite input")

    def test_symlinked_output_folder_cannot_hide_an_original_collision(self) -> None:
        source = self.image("shoot/portrait.png")
        alias = self.root / "alias"
        alias.symlink_to(source.parent, target_is_directory=True)
        self.assert_rejected([
            str(source), "--out-dir", str(alias), "--suffix", "", "--force"
        ], "would overwrite input")

    def test_prompt_record_cannot_overwrite_notes(self) -> None:
        source = self.image("portrait.jpg")
        notes = self.root / "portrait-retouched.prompt.json"
        notes.write_text('{"portrait": "Keep the quiet expression."}')
        self.assert_rejected([
            str(source), "--notes", str(notes), "--out-dir", str(self.root), "--force"
        ], "would overwrite input")

    def test_distinct_output_names_keep_both_results_and_originals(self) -> None:
        first = self.image("shoot/first.jpg")
        second = self.image("shoot/second.jpg")
        originals = {path: path.read_bytes() for path in (first, second)}
        self.assertEqual(self.run_batch([str(first.parent)]), 0)
        self.assertEqual(self.client.images.edit.call_count, 2)
        for source in (first, second):
            self.assertEqual(source.read_bytes(), originals[source])
            output = source.parent / "retouched" / f"{source.stem}-retouched.png"
            self.assertEqual(output.read_bytes(), self.result_bytes)
            self.assertTrue(output.with_suffix(".prompt.json").is_file())

    def test_existing_output_is_skipped_and_force_can_replace_it(self) -> None:
        source = self.image("portrait.jpg")
        output = self.image("retouched/portrait-retouched.png")
        previous = output.read_bytes()
        self.assertEqual(self.run_batch([str(source)]), 0)
        self.factory.assert_not_called()
        self.assertEqual(output.read_bytes(), previous)
        self.assertEqual(self.run_batch([str(source), "--force"]), 0)
        self.client.images.edit.assert_called_once()
        self.assertEqual(output.read_bytes(), self.result_bytes)


if __name__ == "__main__":
    unittest.main()
