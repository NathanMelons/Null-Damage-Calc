#!/usr/bin/env python3
"""
Write docs/icons/{Name}-small.png for each docs/icons/{Name}.png (skips *-small.png / *-Small.png sources).
Each output is a 40×30 canvas; the sprite is scaled to fit inside (aspect preserved), centered on transparency.
Run from repo root: python scripts/generate-small-icons.py
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow required: pip install Pillow", file=sys.stderr)
    sys.exit(1)

W, H = 40, 30


def fit_contain_center(im: Image.Image, cw: int, ch: int) -> Image.Image:
    im = im.convert("RGBA")
    sw, sh = im.size
    if sw < 1 or sh < 1:
        return Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    scale = min(cw / sw, ch / sh)
    nw = max(1, int(round(sw * scale)))
    nh = max(1, int(round(sh * scale)))
    scaled = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    x = (cw - nw) // 2
    y = (ch - nh) // 2
    canvas.paste(scaled, (x, y), scaled)
    return canvas


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    icons = root / "docs" / "icons"
    if not icons.is_dir():
        print(f"Missing {icons}", file=sys.stderr)
        sys.exit(1)

    n = 0
    err = 0
    for p in sorted(icons.glob("*.png")):
        stem = p.stem
        if stem.lower().endswith("-small"):
            continue
        out = icons / f"{stem}-small.png"
        try:
            im = Image.open(p)
            fit_contain_center(im, W, H).save(out, "PNG")
            n += 1
            if n % 500 == 0:
                print(n, "...", flush=True)
        except OSError as e:
            err += 1
            print("FAIL", p.name, e, file=sys.stderr)
    print(f"Wrote {n} *-small.png, {err} errors")


if __name__ == "__main__":
    main()
