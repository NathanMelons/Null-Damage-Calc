"""One-off / batch: double each PNG's pixel dimensions in ../icons (nearest-neighbor)."""
import os
import sys

from PIL import Image

try:
    Resampling = Image.Resampling
except AttributeError:
    Resampling = Image  # Pillow < 9

def main():
    root = os.path.join(os.path.dirname(__file__), "..", "icons")
    root = os.path.normpath(root)
    if not os.path.isdir(root):
        print("icons folder not found:", root, file=sys.stderr)
        sys.exit(1)
    n = 0
    for name in os.listdir(root):
        if not name.lower().endswith(".png"):
            continue
        path = os.path.join(root, name)
        im = Image.open(path)
        w, h = im.size
        out = im.resize((w * 2, h * 2), Resampling.NEAREST)
        out.save(path, optimize=True)
        n += 1
    print("Scaled", n, "PNG files in", root)

if __name__ == "__main__":
    main()
