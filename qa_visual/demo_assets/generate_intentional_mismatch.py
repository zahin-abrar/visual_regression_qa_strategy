"""Regenerate the deliberately incorrect reference for the intentional-failure demo.

This is NOT an approved golden. It is derived deterministically from the approved
``baselines/android/pixel10-api37/breaking_news.png`` by swapping the red and blue
channels (the red banner becomes blue; white text and alpha are unchanged). The
approved golden is only read, never written.

Usage (from qa_visual/):
    .venv\\Scripts\\python.exe demo_assets\\generate_intentional_mismatch.py
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "baselines/android/pixel10-api37/breaking_news.png"
TARGET = ROOT / "demo_assets/intentional_mismatch_breaking_news.png"
SOURCE_SHA256 = "E552AD4D89CC3684062E803B49550DFCDB868AEA0575BF890DA85D958438BE7F"


def main() -> int:
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest().upper()
    if digest != SOURCE_SHA256:
        raise SystemExit(f"Approved breaking_news golden changed unexpectedly: {digest}")
    with Image.open(SOURCE) as source:
        r, g, b, a = source.convert("RGBA").split()
        mismatch = Image.merge("RGBA", (b, g, r, a))
    # Fixed save parameters and no metadata keep the output byte-stable.
    mismatch.save(TARGET, format="PNG", optimize=False, compress_level=9)
    print(f"{TARGET.name} {mismatch.size[0]}x{mismatch.size[1]} "
          f"SHA-256 {hashlib.sha256(TARGET.read_bytes()).hexdigest().upper()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
