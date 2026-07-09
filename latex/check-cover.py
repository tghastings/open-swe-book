#!/usr/bin/env python3
"""Validate the generated KDP case-laminate cover wrap.

Checks the built cover PDF against the geometry KDP specifies for the
7x10, 400pp case-laminate template (CASE_LAMINATE_7.000x10.000_400_BW_WHITE):

  * overall MediaBox size and spine placement (read straight from the PDF)
  * spine content (1B, title/author, dot) stays inside the trim-safe zone,
    with 1B near the top and the pink dot near the bottom
  * the back-cover bio text clears the lower-right barcode zone
  * nothing bleeds into the spine hinge folds

Run it after latex/make-cover.sh:

    python3 latex/check-cover.py latex/swebook-generic-cover-wrap.pdf

Exits non-zero (and prints every failure) if any check fails, so CI can gate
on it. The pixel checks need Pillow + a PDF rasterizer (pdftoppm, from
poppler-utils); if neither is available the script still runs the MediaBox
checks and skips the rest with a clear note.
"""
import re
import subprocess
import sys
import shutil
import tempfile
import os

# ---- Geometry, in inches, from the KDP template + our cover-wrap.html layout ----
OVERALL_W, OVERALL_H = 16.6667, 11.4167   # template MediaBox (1200 x 822 pt)
DIM_TOL = 0.02                            # ~1.4pt slack on overall size

TRIM_TOP, TRIM_BOTTOM = 0.7085, 10.7085   # trim = 10in tall, centered in the 11.417 wrap
SPINE_L, SPINE_R = 7.7875, 8.8775         # spine folds; width 1.090
SAFE = 0.10                               # keep live content this far inside trim / folds

# barcode zone reserved in the back cover's lower-right (KDP prints the barcode here)
BAR_L, BAR_R = 5.05, 7.10
BAR_TOP, BAR_BOTTOM = 9.00, 10.22

DPI = 150
failures = []
def check(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        failures.append(msg)


def read_mediabox(pdf):
    data = open(pdf, "rb").read()
    m = re.search(rb"/MediaBox\s*\[([^\]]+)\]", data)
    if not m:
        raise SystemExit(f"no /MediaBox in {pdf}")
    v = [float(x) for x in m.group(1).split()]
    return (v[2] - v[0]) / 72.0, (v[3] - v[1]) / 72.0


def rasterize(pdf):
    """Return a Pillow image of the cover at DPI, or None if tools are missing."""
    try:
        from PIL import Image
    except ImportError:
        print("note: Pillow not installed; skipping pixel checks")
        return None
    if not shutil.which("pdftoppm"):
        print("note: pdftoppm (poppler-utils) not found; skipping pixel checks")
        return None
    with tempfile.TemporaryDirectory() as d:
        pre = os.path.join(d, "page")
        subprocess.run(["pdftoppm", "-png", "-r", str(DPI), pdf, pre],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        png = pre + "-1.png"
        if not os.path.exists(png):
            return None
        return Image.open(png).convert("RGB").copy()


def is_light(p):   # bright title/author/label ink on the dark cover
    r, g, b = p
    return r > 150 and g > 150 and b > 150 and not (r > 248 and g > 248 and b > 248)

def is_pink(p):    # the 1B badge and the accent dot (#ff2d78-ish)
    r, g, b = p
    return r > 180 and 20 < g < 130 and 80 < b < 180


def content_rows(px, W, H, x0, x1, pred):
    """First/last y (inches) in the x-band [x0,x1] where pred(pixel) holds."""
    a = b = None
    xa, xb = int(x0 * DPI), int(x1 * DPI)
    for y in range(H):
        for x in range(xa, min(xb, W)):
            if pred(px[x, y]):
                if a is None:
                    a = y
                b = y
                break
    return (a / DPI if a is not None else None, b / DPI if b is not None else None)


def main():
    pdf = sys.argv[1] if len(sys.argv) > 1 else "latex/swebook-generic-cover-wrap.pdf"
    if not os.path.exists(pdf):
        raise SystemExit(f"cover not found: {pdf} (run latex/make-cover.sh first)")
    print(f"checking {pdf}")

    print("dimensions:")
    w, h = read_mediabox(pdf)
    check(abs(w - OVERALL_W) <= DIM_TOL, f"overall width {w:.4f}in == {OVERALL_W}in (KDP template)")
    check(abs(h - OVERALL_H) <= DIM_TOL, f"overall height {h:.4f}in == {OVERALL_H}in (KDP template)")

    img = rasterize(pdf)
    if img is not None:
        W, H = img.size
        px = img.load()
        # sanity: the raster matches the MediaBox at DPI
        check(abs(W / DPI - w) <= DIM_TOL and abs(H / DPI - h) <= DIM_TOL,
              f"raster {W}x{H}px matches {w:.3f}x{h:.3f}in at {DPI}dpi")

        print("spine content inside the trim-safe zone:")
        st, sb = content_rows(px, W, H, SPINE_L + SAFE, SPINE_R - SAFE, lambda p: is_light(p) or is_pink(p))
        check(st is not None, "spine has visible content")
        if st is not None:
            check(st >= TRIM_TOP + SAFE, f"spine top {st:.2f}in >= {TRIM_TOP + SAFE:.2f}in (not above trim-safe)")
            check(sb <= TRIM_BOTTOM - SAFE, f"spine bottom {sb:.2f}in <= {TRIM_BOTTOM - SAFE:.2f}in (not below trim-safe)")
            # 1B pinned to the top third, the dot to the bottom third of the safe span
            pt, _ = content_rows(px, W, H, SPINE_L + SAFE, SPINE_R - SAFE, is_pink)
            _, pb = content_rows(px, W, H, SPINE_L + SAFE, SPINE_R - SAFE, is_pink)
            span = TRIM_BOTTOM - TRIM_TOP
            check(pt is not None and pt <= TRIM_TOP + span / 3,
                  f"1B badge near spine top (pink top {pt:.2f}in <= {TRIM_TOP + span/3:.2f}in)")
            check(pb is not None and pb >= TRIM_BOTTOM - span / 3,
                  f"accent dot near spine bottom (pink bottom {pb:.2f}in >= {TRIM_BOTTOM - span/3:.2f}in)")

        print("spine content clears the hinge folds:")
        # scan the full spine height for any bright ink outside the safe horizontal band
        bleed = 0
        for y in range(int(TRIM_TOP * DPI), int(TRIM_BOTTOM * DPI)):
            for x in list(range(int(SPINE_L * DPI), int((SPINE_L + SAFE) * DPI))) + \
                     list(range(int((SPINE_R - SAFE) * DPI), int(SPINE_R * DPI))):
                if x < W and (is_light(px[x, y]) or is_pink(px[x, y])):
                    bleed += 1
        check(bleed < 40, f"no spine ink within {SAFE}in of the folds (stray px={bleed})")

        print("back-cover text clears the barcode zone:")
        intruders = 0
        for y in range(int(BAR_TOP * DPI), int(min(BAR_BOTTOM, TRIM_BOTTOM) * DPI)):
            for x in range(int(BAR_L * DPI), int(BAR_R * DPI)):
                if x < W and is_light(px[x, y]):
                    intruders += 1
        check(intruders < 40, f"barcode zone free of bio text (stray px={intruders})")

    print()
    if failures:
        print(f"FAILED {len(failures)} check(s):")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("all cover checks passed")


if __name__ == "__main__":
    main()
