"""Deterministic PNG comparison; deliberately never creates/updates goldens.

PNG comparison is a test runner concern, independent of Appium or operating system.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from PIL import Image, ImageChops


@dataclass(frozen=True)
class Comparison:
    size_match: bool
    baseline_size: tuple[int, int]
    actual_size: tuple[int, int]
    changed_pixels: int
    total_pixels: int
    changed_ratio: float
    max_changed_ratio: float
    channel_tolerance: int
    passed: bool


def compare_png(
    baseline: Path,
    actual: Path,
    diff_path: Path,
    *,
    channel_tolerance: int = 12,
    max_changed_ratio: float = 0.002,
) -> Comparison:
    """Compare actual vs approved reference and write visible red diff overlay.

    A pixel changes if *any* RGB channel differs more than channel_tolerance.
    The allowed changed-pixel ratio defaults to 0.2%, not 20%.
    Different image dimensions are always a failure.
    """
    if not 0 <= channel_tolerance <= 255:
        raise ValueError("channel_tolerance must be in [0, 255]")
    if not 0 <= max_changed_ratio <= 1:
        raise ValueError("max_changed_ratio must be in [0, 1]")

    diff_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(baseline) as original_baseline, Image.open(actual) as original_actual:
        b = original_baseline.convert("RGB")
        a = original_actual.convert("RGB")
        size_match = b.size == a.size
        total = a.width * a.height
        if not size_match:
            # A mismatched crop/device config cannot safely be pixel-compared.
            # Preserve both images side by side as diagnostic evidence.
            side_by_side = Image.new("RGB", (b.width + a.width, max(b.height, a.height)), (255, 255, 255))
            side_by_side.paste(b, (0, 0))
            side_by_side.paste(a, (b.width, 0))
            side_by_side.save(diff_path)
            return Comparison(False, b.size, a.size, total, total, 1.0, max_changed_ratio, channel_tolerance, False)

        channels = ImageChops.difference(b, a).split()
        flags = [ch.point(lambda px: 255 if px > channel_tolerance else 0) for ch in channels]
        mask = ImageChops.lighter(ImageChops.lighter(flags[0], flags[1]), flags[2])
        changed = mask.histogram()[255]
        changed_ratio = changed / total if total else 0.0
        overlay = Image.composite(Image.new("RGB", a.size, (255, 0, 80)), a, mask)
        overlay.save(diff_path)
        return Comparison(True, b.size, a.size, changed, total, changed_ratio, max_changed_ratio, channel_tolerance, changed_ratio <= max_changed_ratio)


def write_result(result: Comparison, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(result), indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two real PNG files without changing goldens")
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--actual", required=True, type=Path)
    parser.add_argument("--diff", required=True, type=Path)
    parser.add_argument("--result-json", type=Path)
    parser.add_argument("--channel-tolerance", type=int, default=12)
    parser.add_argument("--max-changed-ratio", type=float, default=0.002)
    args = parser.parse_args()
    if not args.baseline.is_file() or not args.actual.is_file():
        parser.error("Both --baseline and --actual must be existing PNG files")
    result = compare_png(
        args.baseline, args.actual, args.diff,
        channel_tolerance=args.channel_tolerance, max_changed_ratio=args.max_changed_ratio,
    )
    if args.result_json:
        write_result(result, args.result_json)
    print(json.dumps(asdict(result), indent=2))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
