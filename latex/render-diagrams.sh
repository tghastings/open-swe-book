#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
DIR="$1"; MJS="$PWD/latex/mermaid.min.js"
# resolve tools without letting a miss abort the script under `set -e` — they are
# only needed to render an UNcached diagram (the loop skips ones already rendered)
CHROME="${CHROME_BIN:-$(command -v google-chrome-stable || command -v google-chrome || command -v chromium || true)}"
MAGICK="$(command -v magick || command -v convert || true)"
shopt -s nullglob
mmds=("$DIR"/*.mmd)
echo "rendering ${#mmds[@]} diagrams..."
for m in "${mmds[@]}"; do
  n=$(basename "$m" .mmd)
  [ -f "$DIR/$n.png" ] && continue
  # gantt charts are wide horizontal timelines; give them a wide canvas + tuned config
  if grep -qE '^\s*gantt\b' "$m"; then kind=gantt; win="1800,1100"; dsf=2;
  elif grep -qE '^\s*(%%\{init[^\n]*\}%%\s*)?xychart' "$m" || grep -q 'xychart' "$m"; then kind=xychart; win="1250,2400"; dsf=3;
  else kind=flow; win="1400,2400"; dsf=3; fi
  python3 - "$m" "$DIR/$n.html" "$MJS" "$kind" <<'PY'
import html, sys
src, kind = open(sys.argv[1]).read(), sys.argv[4]
if kind == "xychart":
    body = "margin:0;background:#fff;width:1050px;padding:10px 10px 26px 10px"
    cfg = ""
elif kind == "gantt":
    body = "margin:0;background:#fff;width:1150px;padding:14px"
    cfg = ('gantt:{useMaxWidth:true,leftPadding:150,barHeight:24,barGap:8,'
           'fontSize:13,sectionFontSize:15,topPadding:50}')
else:
    body, cfg = "margin:0;background:#fff;display:inline-block;padding:6px", ""
open(sys.argv[2], "w").write(f'''<!doctype html><html><head><meta charset="utf-8">
<script src="file://{sys.argv[3]}"></script>
<style>body{{{body}}} svg{{overflow:visible !important}}</style></head>
<body><pre class="mermaid">{html.escape(src)}</pre>
<script>mermaid.initialize({{startOnLoad:true,theme:"neutral",securityLevel:"loose"{',' + cfg if cfg else ''}}});</script></body></html>''')
PY
  "$CHROME" --headless=new --disable-gpu ${CHROME_FLAGS:-} --force-device-scale-factor=$dsf \
    --hide-scrollbars --window-size=$win --screenshot="$DIR/$n.raw.png" \
    --virtual-time-budget=12000 "file://$PWD/$DIR/$n.html" 2>/dev/null
  "$MAGICK" "$DIR/$n.raw.png" -trim +repage -colorspace Gray -bordercolor white -border 10 "$DIR/$n.png" 2>/dev/null
done
rm -f "$DIR"/*.raw.png "$DIR"/*.html
echo "diagrams done"
