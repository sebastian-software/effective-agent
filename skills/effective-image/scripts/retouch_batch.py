#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.100", "pillow>=11"]
# ///
"""Apply the business portrait retouch to photos through the OpenAI Images API.

The prompt is read from references/route-business-retouch.md, so the route
stays the single source of the brief. Each output is saved next to a record
of the exact prompt, model, size, and reference role used.
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps

ROUTE = Path(__file__).resolve().parent.parent / "references" / "route-business-retouch.md"
SOURCE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
MIME_TYPES = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}

# Size limits documented for gpt-image-2 and assumed for newer models: edges
# are multiples of 16, the long edge is at most 3840 px, and the total is
# between 655,360 and 8,294,400 pixels.
SIZE_STEP = 16
MAX_EDGE = 3840
MAX_PIXELS = 8_294_400
MIN_PIXELS = 655_360
MAX_RATIO = 3

ROLE_SENTENCES = {
    "color": "Image 2 is only a color treatment reference. Image 1 is the original edit target.",
    "identity": "Image 2 is an identity/anatomy reference only. Preserve Image 1's approved grade.",
}


@dataclass(frozen=True)
class Job:
    source: Path
    reference: Path | None
    output: Path
    size: str
    prompt: str


def load_template(route: Path = ROUTE) -> str:
    text = route.read_text(encoding="utf-8")
    section = text.split("## Reusable Imagegen Prompt", 1)
    match = re.search(r"~~~text\n(.*?)\n~~~", section[1], re.DOTALL) if len(section) == 2 else None
    if match is None:
        raise SystemExit(f"No reusable prompt found in {route}")
    return match.group(1).strip()


def build_prompt(template: str, role: str | None, notes: str | None) -> str:
    lines = template.splitlines()
    if role is None:
        # The route omits the Image 2 sentence when no second reference is supplied.
        lines = [line for line in lines if not line.startswith("Input role of Image 2")]
    parts = [ROLE_SENTENCES[role]] if role else []
    parts.append("\n".join(lines))
    if notes:
        parts.append(f"Photo-specific instruction: {notes.strip()}")
    return "\n\n".join(parts)


def largest_size(width: int, height: int) -> str:
    """Returns the largest supported output size matching the source's aspect ratio."""
    ratio = max(width, height) / min(width, height)
    if ratio > MAX_RATIO:
        raise ValueError(f"Aspect ratio {ratio:.2f}:1 exceeds {MAX_RATIO}:1")
    for long_edge in range(MAX_EDGE, 0, -SIZE_STEP):
        short_edge = max(SIZE_STEP, round(long_edge / ratio / SIZE_STEP) * SIZE_STEP)
        if long_edge * short_edge <= MAX_PIXELS:
            break
    if long_edge * short_edge < MIN_PIXELS:
        raise ValueError("Source is too small for a supported output size")
    return f"{long_edge}x{short_edge}" if width >= height else f"{short_edge}x{long_edge}"


def oriented_upload(path: Path) -> tuple[tuple[str, bytes, str], tuple[int, int]]:
    """Returns the upload payload and displayed dimensions, applying EXIF rotation."""
    data = path.read_bytes()
    with Image.open(io.BytesIO(data)) as image:
        orientation = image.getexif().get(0x0112, 1)
        if orientation == 1:
            return (path.name, data, MIME_TYPES[path.suffix.lower()]), image.size
        upright = ImageOps.exif_transpose(image)
        buffer = io.BytesIO()
        upright.save(buffer, format="PNG")
        return (f"{path.stem}.png", buffer.getvalue(), "image/png"), upright.size


def collect_sources(inputs: list[Path]) -> list[Path]:
    sources: list[Path] = []
    for item in inputs:
        if item.is_dir():
            sources.extend(sorted(p for p in item.iterdir() if p.suffix.lower() in SOURCE_SUFFIXES))
        elif item.suffix.lower() in SOURCE_SUFFIXES:
            sources.append(item)
        else:
            raise SystemExit(f"Unsupported input: {item}")
    if not sources:
        raise SystemExit("No source images found")
    return sources


def find_reference(reference: Path | None, stem: str) -> Path | None:
    """Uses a single reference file for every source, or the file in a folder named after the source."""
    if reference is None or reference.is_file():
        return reference
    matches = sorted(
        p
        for p in reference.iterdir()
        if p.suffix.lower() in SOURCE_SUFFIXES and (p.stem == stem or p.stem.startswith(f"{stem}-"))
    )
    if len(matches) > 1:
        raise SystemExit(f"Ambiguous references for {stem}: {', '.join(p.name for p in matches)}")
    return matches[0] if matches else None


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("inputs", nargs="+", type=Path, help="Source images or folders")
    parser.add_argument("--out-dir", type=Path, help="Output folder (default: <first input>/retouched)")
    parser.add_argument("--suffix", default="-retouched", help="Appended to each output's file stem")
    parser.add_argument("--notes", type=Path, help="JSON object mapping source stems to photo-specific instructions")
    parser.add_argument("--reference", type=Path, help="Image 2: one file, or a folder matched by source stem")
    parser.add_argument("--reference-role", choices=sorted(ROLE_SENTENCES), default="color")
    parser.add_argument("--model", default="gpt-image-2.5-sunburst")
    parser.add_argument("--quality", choices=["low", "medium", "high", "auto"], default="high")
    parser.add_argument("--size", default="max", help="'max' (largest supported at the source ratio), 'auto', or WxH")
    parser.add_argument("--force", action="store_true", help="Overwrite existing outputs")
    parser.add_argument("--dry-run", action="store_true", help="Print the plan without calling the API")
    return parser.parse_args(argv)


def plan(args: argparse.Namespace) -> list[Job]:
    template = load_template()
    notes = json.loads(args.notes.read_text(encoding="utf-8")) if args.notes else {}
    sources = collect_sources(args.inputs)
    first = args.inputs[0]
    out_dir = args.out_dir or (first if first.is_dir() else first.parent) / "retouched"
    jobs: list[Job] = []
    for source in sources:
        reference = find_reference(args.reference, source.stem)
        _, (width, height) = oriented_upload(source)
        size = largest_size(width, height) if args.size == "max" else args.size
        prompt = build_prompt(template, args.reference_role if reference else None, notes.get(source.stem))
        output = out_dir / f"{source.stem}{args.suffix}.png"
        jobs.append(Job(source=source, reference=reference, output=output, size=size, prompt=prompt))
    return jobs


def run(job: Job, args: argparse.Namespace, client: object) -> str:
    image, _ = oriented_upload(job.source)
    images = [image]
    if job.reference is not None:
        images.append(oriented_upload(job.reference)[0])
    result = client.images.edit(  # type: ignore[attr-defined]
        model=args.model,
        image=images if len(images) > 1 else images[0],
        prompt=job.prompt,
        size=job.size,
        quality=args.quality,
        output_format="png",
    )
    job.output.parent.mkdir(parents=True, exist_ok=True)
    job.output.write_bytes(base64.b64decode(result.data[0].b64_json))
    record = {
        "source": job.source.name,
        "reference": job.reference.name if job.reference else None,
        "reference_role": args.reference_role if job.reference else None,
        "model": args.model,
        "quality": args.quality,
        "size": job.size,
        "prompt": job.prompt,
    }
    job.output.with_suffix(".prompt.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    with Image.open(job.output) as output:
        return f"{output.width}x{output.height}"


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    jobs = plan(args)
    pending = [job for job in jobs if args.force or not job.output.exists()]
    for job in jobs:
        state = "todo" if job in pending else "skip (exists)"
        reference = f" + {job.reference.name}" if job.reference else ""
        print(f"{state:14} {job.source.name}{reference} -> {job.output.name} @ {job.size}")
    if args.dry_run:
        if pending:
            print(f"\nPrompt for {pending[0].source.name}:\n\n{pending[0].prompt}")
        return 0
    if not pending:
        return 0
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set", file=sys.stderr)
        return 2

    from openai import OpenAI

    client = OpenAI(timeout=900)
    failures = 0
    for index, job in enumerate(pending, 1):
        print(f"[{index}/{len(pending)}] {job.source.name} ...", flush=True)
        try:
            print(f"    saved {job.output} ({run(job, args, client)})", flush=True)
        except Exception as error:  # noqa: BLE001 - report and continue with the next photo
            failures += 1
            print(f"    failed: {error}", file=sys.stderr, flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
