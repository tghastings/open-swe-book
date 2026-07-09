#!/usr/bin/env bash
# Render the KDP case-laminate wrap cover (16.667 x 11.417 in @ 300dpi, spine 1.090 in).
# Output: latex/swebook-generic-cover-wrap.pdf
set -euo pipefail
cd "$(dirname "$0")/.."
CHROME="${CHROME_BIN:-$(command -v google-chrome-stable || command -v chromium)}"
MAGICK="$(command -v magick || command -v convert)"   # ImageMagick 7 'magick' or 6 'convert'
"$CHROME" --headless=new --disable-gpu ${CHROME_FLAGS:-} --force-device-scale-factor=3.125 \
  --window-size=1600,1096 --hide-scrollbars \
  --screenshot=latex/cover-wrap.png --virtual-time-budget=4000 \
  "file://$PWD/latex/cover-wrap.html" 2>/dev/null
"$MAGICK" latex/cover-wrap.png -units PixelsPerInch -density 300 latex/swebook-generic-cover-wrap.pdf
rm -f latex/cover-wrap.png
python3 -c "import re; v=[float(x) for x in re.findall(rb'/MediaBox\s*\[([^\]]+)\]', open('latex/swebook-generic-cover-wrap.pdf','rb').read())[0].split()]; print(f'cover: {v[2]/72:.3f} x {v[3]/72:.3f} in (KDP wants 16.667 x 11.417)')"
