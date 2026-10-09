from __future__ import annotations

import json
import shutil
import struct
import subprocess
import tempfile
import unittest
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "effective-web" / "scripts" / "visual-change-boxes.mjs"
NODE = shutil.which("node")

WHITE = (255, 255, 255, 255)
WIDTH = 64


def chunk(kind: bytes, body: bytes) -> bytes:
    checksum = zlib.crc32(kind + body) & 0xFFFFFFFF
    return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", checksum)


def paeth(left: int, up: int, upper_left: int) -> int:
    estimate = left + up - upper_left
    distances = (abs(estimate - left), abs(estimate - up), abs(estimate - upper_left))
    if distances[0] <= distances[1] and distances[0] <= distances[2]:
        return left
    return up if distances[1] <= distances[2] else upper_left


def filtered(row: bytes, previous: bytes, kind: int, step: int) -> bytes:
    """Applies one PNG filter so the decoder's unfiltering is exercised."""
    output = bytearray()
    for index, value in enumerate(row):
        left = row[index - step] if index >= step else 0
        up = previous[index]
        upper_left = previous[index - step] if index >= step else 0
        predictor = (0, left, up, (left + up) // 2, paeth(left, up, upper_left))[kind]
        output.append((value - predictor) & 0xFF)
    return bytes(output)


def write_png(path: Path, rows: list[list[tuple[int, int, int, int]]], rgb: bool = False) -> None:
    channels = 3 if rgb else 4
    raw = bytearray()
    previous = bytes(len(rows[0]) * channels)
    for index, pixels in enumerate(rows):
        row = bytes(value for pixel in pixels for value in pixel[:channels])
        kind = index % 5
        raw.append(kind)
        raw += filtered(row, previous, kind, channels)
        previous = row
    header = struct.pack(">IIBBBBB", len(rows[0]), len(rows), 8, 2 if rgb else 6, 0, 0, 0)
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(bytes(raw)))
        + chunk(b"IEND", b"")
    )


def blank() -> list[tuple[int, int, int, int]]:
    return [WHITE] * WIDTH


def text_line(seed: int, start: int = 4, length: int = 40) -> list[tuple[int, int, int, int]]:
    """A row of distinct dark 'glyph' pixels, unique per seed."""
    row = blank()
    for x in range(start, start + length):
        shade = (seed * 37 + x * 11) % 120
        row[x] = (shade, shade // 2, 90, 255)
    return row


def page(lines: list[int | None]) -> list[list[tuple[int, int, int, int]]]:
    """Each entry becomes a three-row text line, or three blank rows for None."""
    rows: list[list[tuple[int, int, int, int]]] = []
    for seed in lines:
        for offset in range(3):
            rows.append(blank() if seed is None else text_line(seed * 10 + offset))
    return rows


@unittest.skipIf(NODE is None, "node is not installed")
class VisualChangeBoxesTest(unittest.TestCase):
    def run_script(self, before, after, *arguments: str, rgb: bool = False):
        with tempfile.TemporaryDirectory() as directory:
            before_path = Path(directory) / "before.png"
            after_path = Path(directory) / "after.png"
            write_png(before_path, before, rgb)
            write_png(after_path, after, rgb)
            result = subprocess.run(
                [NODE, str(SCRIPT), str(before_path), str(after_path), *arguments],
                capture_output=True,
                text=True,
                check=True,
            )
        return json.loads(result.stdout)

    def changes(self, before, after, **options):
        report = self.run_script(before, after, **options)
        return [
            (change["kind"], change["y"], change["height"], change["x"], change["width"])
            for change in report["changes"]
        ]

    def test_identical_screenshots_have_no_changes(self) -> None:
        base = page([1, None, 2, None, 3])
        self.assertEqual(self.changes(base, base), [])

    def test_inserted_content_is_new_and_moved_content_is_not_reported(self) -> None:
        before = page([1, None, 2, None, 3])
        after = page([1, None, 9, None, 2, None, 3])
        self.assertEqual(self.changes(before, after), [("added", 6, 3, 4, 40)])

    def test_removed_content_is_a_line_where_it_used_to_be(self) -> None:
        before = page([1, None, 2, None, 3, None, 4])
        after = page([1, None, 2, None, 4])
        [(kind, y, height, _, _)] = self.changes(before, after)
        self.assertEqual((kind, height), ("removed", 0))
        self.assertIn(y, range(9, 13))

    def test_changed_content_is_framed_to_its_columns(self) -> None:
        before = page([1, None, 2, None, 3])
        after = [list(row) for row in before]
        after[7][20] = (200, 0, 0, 255)
        self.assertEqual(self.changes(before, after), [("changed", 7, 1, 20, 1)])

    def test_moved_content_tolerates_anti_aliasing_but_not_new_content(self) -> None:
        before = page([1, None, 2, None, 3])
        # Row 19 is the second row of line 3, which moved down with line 2 between it and the insertion.
        softened = page([1, None, 9, None, 2, None, 3])
        softened[19] = [(min(255, r + 6), g, b, a) for r, g, b, a in softened[19]]
        self.assertEqual(self.changes(before, softened), [("added", 6, 3, 4, 40)])
        replaced = page([1, None, 9, None, 2, None, 3])
        replaced[18:21] = [text_line(80 + offset, start=30, length=20) for offset in range(3)]
        # The replaced line lies within the merge gap of the insertion, so both read as one change.
        self.assertEqual(self.changes(before, replaced), [("changed", 6, 15, 4, 46)])

    def test_annotations_use_css_pixels_and_number_the_changes(self) -> None:
        before = page([1, None, 2, None, 3])
        after = page([1, None, 9, None, 2, None, 3])
        report = self.run_script(before, after, "--scale", "2", rgb=True)
        self.assertEqual(report["legend"], "NEW 1")
        self.assertEqual(
            report["annotations"],
            [{"kind": "added", "label": "NEW 1", "color": "#15803d", "x": 2, "y": 3, "width": 20, "height": 2}],
        )
        self.assertIn("visualChangeOverlay", report["overlayScript"])

    def test_rejects_wrong_usage_and_non_png_input(self) -> None:
        usage = subprocess.run([NODE, str(SCRIPT), "only-one.png"], capture_output=True, text=True)
        self.assertEqual(usage.returncode, 2)
        with tempfile.NamedTemporaryFile(suffix=".png") as fake:
            fake.write(b"not a png")
            fake.flush()
            failure = subprocess.run([NODE, str(SCRIPT), fake.name, fake.name], capture_output=True, text=True)
        self.assertEqual(failure.returncode, 1)
        self.assertIn("Not a PNG", failure.stderr)


if __name__ == "__main__":
    unittest.main()
