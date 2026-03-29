"""
Create a 40x32 copy of each PNG in ../icons named {base}-Small.png.
Skips sources already named *-Small.png. Originals are unchanged.
"""
import os
import sys

from PIL import Image

try:
    Resampling = Image.Resampling
except AttributeError:
    Resampling = Image

CANVAS_W, CANVAS_H = 40, 32


def paste_contain(src: Image.Image, canvas_w: int, canvas_h: int) -> Image.Image:
    w, h = src.size
    if w < 1 or h < 1:
        return Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    scale = min(canvas_w / w, canvas_h / h)
    nw = max(1, int(round(w * scale)))
    nh = max(1, int(round(h * scale)))
    resized = src.resize((nw, nh), Resampling.NEAREST)
    out = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    x = (canvas_w - nw) // 2
    y = (canvas_h - nh) // 2
    if resized.mode != "RGBA":
        resized = resized.convert("RGBA")
    out.paste(resized, (x, y), resized)
    return out


def main():
    root = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "icons"))
    if not os.path.isdir(root):
        print("icons folder not found:", root, file=sys.stderr)
        sys.exit(1)
    n = 0
    for name in sorted(os.listdir(root)):
        if not name.lower().endswith(".png"):
            continue
        base, _ = os.path.splitext(name)
        if base.endswith("-Small"):
            continue
        out_name = base + "-Small.png"
        out_path = os.path.join(root, out_name)
        in_path = os.path.join(root, name)
        im = Image.open(in_path)
        if im.mode != "RGBA":
            im = im.convert("RGBA")
        canvas = paste_contain(im, CANVAS_W, CANVAS_H)
        canvas.save(out_path, optimize=True)
        n += 1
    print("Wrote", n, "files (*-Small.png) at", CANVAS_W, "x", CANVAS_H, "in", root)


if __name__ == "__main__":
    main()
