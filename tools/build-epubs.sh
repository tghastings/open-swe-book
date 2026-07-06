#!/usr/bin/env bash
# Build per-language EPUB + PDF editions: identical prose, one language of code.
#   tools/build-epubs.sh                 -> the five single-language editions
#   tools/build-epubs.sh go              -> just the Go edition
#   tools/build-epubs.sh all             -> one edition with every language stacked
# Output: $EPUB_OUT (default ./epubs) as swebook-<lang>.epub.
# Requires: mdbook+mdbook-mermaid (PATH or se-book-mdbook docker image),
#           Chrome/Chromium headless, pandoc (PATH or pandoc/core docker image).
set -euo pipefail
cd "$(dirname "$0")/.."
BOOK_DIR="$PWD"
OUT="${EPUB_OUT:-$PWD/epubs}"
BUILD=".epub-build"
mkdir -p "$OUT"
VERSION="${SWEBOOK_VERSION:-$(git describe --tags --always 2>/dev/null || echo dev)}"
export SWEBOOK_VERSION="$VERSION"

CHROME="${CHROME_BIN:-$(command -v google-chrome-stable || command -v google-chrome \
  || command -v chromium-browser || command -v chromium)}"
export CHROME_BIN="$CHROME"
export RASTER_DIR="$OUT/.raster"   # diagram PNG cache shared across editions

run_pandoc() {  # run_pandoc <in-html> <out-epub> <edition-description> <title> <cover>
  local args=(-f html+tex_math_dollars --mathml
    --metadata title="$4" --metadata identifier="org.swebook.$2.$VERSION"
    --metadata lang=en
    --metadata rights="CC BY-SA 4.0 (prose); MIT (code)"
    --metadata description="$3" --toc --toc-depth=2 --split-level=1)
  if command -v pandoc >/dev/null; then
    pandoc "$OUT/$1" -o "$OUT/$2" "${args[@]}" \
      --resource-path "$OUT" \
      --epub-metadata tools/epub-metadata.xml \
      --css tools/epub.css --highlight-style tools/onelight.theme \
      --epub-cover-image "$5" \
      --epub-embed-font fonts/Inconsolata-latin.woff2
  else
    docker run --rm --user "$(id -u):$(id -g)" -v "$OUT:/data" -v "$BOOK_DIR:/book" pandoc/core \
      "/data/$1" -o "/data/$2" "${args[@]}" \
      --resource-path /data \
      --epub-metadata /book/tools/epub-metadata.xml \
      --css /book/tools/epub.css --highlight-style /book/tools/onelight.theme \
      --epub-cover-image "/book/$5" \
      --epub-embed-font /book/fonts/Inconsolata-latin.woff2
  fi
}

# 1. Build the site and render print.html with JS (mermaid -> SVG).
if command -v mdbook >/dev/null; then
  mdbook build -d "$BOOK_DIR/$BUILD"
else
  docker run --rm -v "$BOOK_DIR:/book" se-book-mdbook mdbook build -d "/book/$BUILD"
fi
# Force the LIGHT theme for the render: headless Chrome reports dark-mode
# preference, which would bake dark-theme colors into every diagram SVG.
# (.epub-build may be root-owned from the docker build, so the wrapper lives
# in $OUT with a <base> pointing back at the build dir.)
python3 - "$BOOK_DIR/$BUILD" "$OUT" <<'PY'
import sys
d, out = sys.argv[1], sys.argv[2]
t = open(f"{d}/print.html", encoding="utf-8").read()
t = t.replace("<head>",
              f'<head><base href="file://{d}/">'
              '<script>try{localStorage.setItem("mdbook-theme","light")}'
              "catch(e){}</script>", 1)
open(f"{out}/light-print.html", "w", encoding="utf-8").write(t)
PY
render_dump() {  # render_dump <budget-ms>
  "$CHROME" --headless --disable-gpu ${CHROME_FLAGS:-} --dump-dom \
    --virtual-time-budget="$1" \
    "file://$OUT/light-print.html" > "$OUT/rendered.html" 2> "$OUT/chrome.log"
}
expected_diagrams=$(grep -rh -c '^```mermaid' chapters/*/*.md templates/*.md curriculum/*.md 2>/dev/null | awk '{n+=$1} END {print n+0}')
render_dump 30000
rendered=$(grep -c 'data-processed="true"' "$OUT/rendered.html" || true)
if [ "$rendered" -lt "$expected_diagrams" ]; then
  echo "mermaid rendered $rendered/$expected_diagrams — retrying with a larger budget" >&2
  render_dump 90000
  rendered=$(grep -c 'data-processed="true"' "$OUT/rendered.html" || true)
fi
if [ "$rendered" -lt "$expected_diagrams" ]; then
  echo "FATAL: only $rendered of $expected_diagrams diagrams rendered; chrome log:" >&2
  cat "$OUT/chrome.log" >&2
  exit 1
fi
echo "diagrams rendered: $rendered/$expected_diagrams"
rm -f "$OUT/light-print.html" "$OUT/chrome.log"

# 2. Covers (regenerated every run: they carry the version).
LANGS="${1:-python java javascript go ruby typescript}"
for lang in $LANGS; do
  [ "$lang" = all ] || bash tools/make-covers.sh covers "$lang"
done

# 3. Per-language filter + pandoc.
TITLE="Software Engineering: Standing on the Shoulders of Giants"
declare -A PRETTY=([python]=Python [java]=Java [javascript]=JavaScript [go]=Go [ruby]=Ruby [typescript]=TypeScript)
for lang in $LANGS; do
  python3 tools/epub-lang-filter.py "$OUT/rendered.html" "$lang" "$VERSION" > "$OUT/filtered-$lang.html"
  if [ "$lang" = all ]; then
    name="swebook.epub"; edition="First Edition, all languages"
    title="$TITLE"; cover="tools/covers/cover-python.png"
  else
    name="swebook-$lang.epub"; edition="First Edition, ${PRETTY[$lang]} code examples ($VERSION)"
    title="$TITLE (${PRETTY[$lang]} Edition)"; cover="tools/covers/cover-$lang.png"
  fi
  run_pandoc "filtered-$lang.html" "$name" "$edition" "$title" "$cover"
  python3 - "$OUT/$name" <<'PY'
import sys, zipfile
# Apple Books: honor publisher fonts/styles by default (legacy but respected).
with zipfile.ZipFile(sys.argv[1], "a") as z:
    if "META-INF/com.apple.ibooks.display-options.xml" not in z.namelist():
        z.writestr("META-INF/com.apple.ibooks.display-options.xml",
                   '<?xml version="1.0" encoding="UTF-8"?>\n'
                   '<display_options><platform name="*">'
                   '<option name="specified-fonts">true</option>'
                   "</platform></display_options>")
PY
  if [ "$lang" != all ]; then
    python3 - "$OUT/$name" "$lang" <<'PY'
import sys, zipfile, re
path, lang = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(path)
x = "".join(z.read(n).decode("utf-8", "ignore")
            for n in z.namelist() if n.endswith(".xhtml"))
langs = set(re.findall(r'class="sourceCode (\w+)"', x))
extra = langs - {lang, "bash", "gherkin", "bibtex", "text"}
if extra:
    sys.exit(f"PURITY FAILURE in {path}: found {sorted(extra)}")
media = [n for n in z.namelist() if "/media/" in n]
pngs = sum(1 for n in media if n.endswith(".png"))
svgs = sum(1 for n in media if n.endswith(".svg"))
if pngs < 40 or svgs:
    sys.exit(f"DIAGRAM FAILURE in {path}: {pngs} png / {svgs} svg in media "
             "(expected ~47 png, 0 svg)")
if "language-mermaid" in x or 'class="mermaid"' in x:
    sys.exit(f"DIAGRAM FAILURE in {path}: unrendered mermaid source shipped")
PY
  fi
  echo "built: $name (purity ok)"

  # PDF twin: same filtered HTML through pandoc standalone HTML (same One
  # Light highlighting + MathML), cover page injected, printed by Chrome.
  html="$OUT/pdf-$lang.html"
  if command -v pandoc >/dev/null; then
    pandoc "$OUT/filtered-$lang.html" -o "$html" -s -f html+tex_math_dollars --mathml \
      --resource-path "$OUT" \
      --metadata title="$title" --toc --toc-depth=2 \
      --highlight-style tools/onelight.theme \
      --css "file://$BOOK_DIR/tools/epub.css" --css "file://$BOOK_DIR/tools/pdf.css"
  else
    docker run --rm --user "$(id -u):$(id -g)" -v "$OUT:/data" -v "$BOOK_DIR:/book" pandoc/core \
      "/data/filtered-$lang.html" -o "/data/pdf-$lang.html" -s \
      -f html+tex_math_dollars --mathml \
      --metadata title="$title" --toc --toc-depth=2 \
      --highlight-style /book/tools/onelight.theme \
      --css "file://$BOOK_DIR/tools/epub.css" --css "file://$BOOK_DIR/tools/pdf.css"
  fi
  python3 - "$html" "$BOOK_DIR/$cover" "$BOOK_DIR" <<'PY'
import sys, re
p, cover, book = sys.argv[1], sys.argv[2], sys.argv[3]
t = open(p, encoding="utf-8").read()
t = re.sub(r"(<body[^>]*>)",
           r'\1<div class="pdf-cover"><img src="file://' + cover + '"/></div>',
           t, count=1)
font = ('<style>@font-face{font-family:"Inconsolata";font-weight:200 900;'
        'src:url("file://' + book + '/fonts/Inconsolata-latin.woff2")'
        ' format("woff2")}</style>')
t = t.replace("</head>", font + "</head>", 1)
open(p, "w", encoding="utf-8").write(t)
PY
  "$CHROME" --headless --disable-gpu ${CHROME_FLAGS:-} \
    --print-to-pdf="$OUT/${name%.epub}.pdf" --no-pdf-header-footer \
    --virtual-time-budget=20000 "file://$html" 2>/dev/null
  rm -f "$html"
  echo "built: ${name%.epub}.pdf"
done
rm -rf "$OUT"/rendered.html "$OUT"/filtered-*.html "$OUT"/.raster
