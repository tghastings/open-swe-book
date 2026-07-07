#!/usr/bin/env bash
# Build ONE chapter to PDF via LaTeX. Usage: build-chapter.sh chapters/06-design-and-architecture
set -euo pipefail
cd "$(dirname "$0")/.."
CH="$1"; BUILD=latex/build; rm -rf "$BUILD"; mkdir -p "$BUILD"
num=$(basename "$CH" | grep -oE '^[0-9]+'); prev=$((10#$num - 1))
python3 latex/preprocess.py "$CH/README.md" "$BUILD" "$BUILD/chapter.md"
printf '```{=latex}\n\\setcounter{chapter}{%d}\n```\n\n' "$prev" | cat - "$BUILD/chapter.md" > "$BUILD/c.md" && mv "$BUILD/c.md" "$BUILD/chapter.md"

# Render each mermaid diagram -> tight high-DPI grayscale PNG (Chrome renders the
# label text correctly, including spaces; rsvg does not).
for m in "$BUILD"/*.mmd; do
  [ -e "$m" ] || continue; n=$(basename "$m" .mmd)
  python3 - "$m" "$BUILD/$n.html" "$PWD/latex/mermaid.min.js" <<'PY'
import html, sys
src = open(sys.argv[1]).read()
doc = f'''<!doctype html><html><head><meta charset="utf-8">
<script src="file://{sys.argv[3]}"></script>
<style>body{{margin:0;background:#fff;display:inline-block;padding:6px}}</style></head>
<body><pre class="mermaid">{html.escape(src)}</pre>
<script>mermaid.initialize({{startOnLoad:true, theme:"neutral", securityLevel:"loose"}});</script>
</body></html>'''
open(sys.argv[2], "w").write(doc)
PY
  google-chrome-stable --headless=new --disable-gpu --force-device-scale-factor=3 \
    --hide-scrollbars --window-size=1400,2200 --screenshot="$BUILD/$n.raw.png" \
    --virtual-time-budget=12000 "file://$PWD/$BUILD/$n.html" 2>/dev/null
  magick "$BUILD/$n.raw.png" -trim +repage -colorspace Gray \
    -bordercolor white -border 10 "$BUILD/$n.png" 2>/dev/null
  echo "  [$n] $(identify -format '%wx%h' "$BUILD/$n.png" 2>/dev/null)"
done

docker run --rm -v "$PWD:/book" se-latex pandoc "/book/$BUILD/chapter.md" \
  -o "/book/$BUILD/chapter.pdf" --pdf-engine=xelatex \
  --top-level-division=chapter --number-sections \
  --syntax-definition=/book/tools/generic.xml --highlight-style=tango \
  --include-in-header=/book/latex/preamble.tex --lua-filter=/book/latex/callouts.lua \
  -V documentclass=scrbook -V classoption=11pt,twoside -V colorlinks=false 2>&1 | tail -6
echo "built: $BUILD/chapter.pdf"
