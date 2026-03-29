"""Batch: halve each PNG's pixel dimensions in docs/icons (or ../icons) (nearest-neighbor)."""
import os
import sys

from PIL import Image

try:
    Resampling = Image.Resampling
except AttributeError:
    Resampling = Image  # Pillow < 9


def main():
    base = os.path.join(os.path.dirname(__file__), "..")
    root = os.path.normpath(os.path.join(base, "docs", "icons"))
    if not os.path.isdir(root):
        root = os.path.normpath(os.path.join(base, "icons"))
    if not os.path.isdir(root):
        print("icons folder not found (expected docs/icons or icons):", root, file=sys.stderr)
        sys.exit(1)
    n = 0
    for name in os.listdir(root):
        if not name.lower().endswith(".png"):
            continue
        path = os.path.join(root, name)
        im = Image.open(path)
        w, h = im.size
        nw = max(1, w // 2)
        nh = max(1, h // 2)
        out = im.resize((nw, nh), Resampling.NEAREST)
        out.save(path, optimize=True)
        n += 1
    print("Halved", n, "PNG files in", root)


if __name__ == "__main__":
    main()
