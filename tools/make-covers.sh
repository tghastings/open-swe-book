#!/usr/bin/env bash
# Render EPUB cover PNGs (1600x2560) with headless Chrome.
#   tools/make-covers.sh <outdir> [lang ...]     (default: all five languages)
set -euo pipefail
cd "$(dirname "$0")"
OUTDIR="${1:-covers}"; shift || true
LANGS=("${@:-python java javascript go ruby typescript generic}")
[ $# -eq 0 ] && LANGS=(python java javascript go ruby typescript generic)
mkdir -p "$OUTDIR"
CHROME="${CHROME_BIN:-$(command -v google-chrome-stable || command -v google-chrome \
  || command -v chromium-browser || command -v chromium)}"

declare -A NAME=([python]=Python [java]=Java [javascript]=JavaScript [go]=Go [ruby]=Ruby [typescript]=TypeScript [generic]=Generic)
declare -A ACCENT=([python]="#4b8bbe" [java]="#f89820" [javascript]="#f0db4f" \
  [go]="#00add8" [ruby]="#cc342d" [typescript]="#3178c6" [generic]="#ff2d78")

for lang in "${LANGS[@]}"; do
  html="$(mktemp --suffix=.html)"
  sed -e "s/{{LANG}}/${NAME[$lang]}/g" -e "s/{{ACCENT}}/${ACCENT[$lang]}/g" \
    -e "s/{{VERSION}}/${SWEBOOK_VERSION:-1.0b1}/g" \
    cover-template.html > "$html"
  # The generic (pseudocode) cover carries no language-edition badge.
  # The generic (retail/KDP) cover carries no language badge, and its footer is
  # stamped "First Edition" rather than a build version number.
  if [ "$lang" = generic ]; then
    sed -i '/class="badge"/d' "$html"
    sed -i 's#<div class="edition">.*</div>#<div class="edition">First Edition</div>#' "$html"
  fi
  "$CHROME" --headless --disable-gpu ${CHROME_FLAGS:-} \
    --screenshot="$OUTDIR/cover-$lang.png" --window-size=1600,2560 \
    --virtual-time-budget=2000 "file://$html" 2>/dev/null
  rm -f "$html"
  echo "cover: $OUTDIR/cover-$lang.png"
done
