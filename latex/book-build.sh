#!/usr/bin/env bash
# Build the FULL book interior via LaTeX (scrbook + xelatex, one pandoc pass).
set -euo pipefail
cd "$(dirname "$0")/.."
B=latex/bookbuild; mkdir -p "$B/figs"

# Toolchain: local dev runs pandoc/xelatex inside the se-latex Docker image;
# CI sets LATEX_NATIVE=1 to use tools installed directly on the runner. Both
# resolve paths under $R and run the same commands via tex()/texsh().
if [ "${LATEX_NATIVE:-0}" = 1 ]; then
  R="$PWD"
  tex()   { "$@"; }
  texsh() { sh -c "$1"; }
else
  R="/book"
  tex()   { docker run --rm -v "$PWD:/book" se-latex "$@"; }
  texsh() { docker run --rm -v "$PWD:/book" se-latex sh -c "$1"; }
fi
python3 latex/make-references.py
find "$B" -maxdepth 1 -type f -delete 2>/dev/null   # clear top-level files, keep rendered figs/
: > "$B/body.md"; : > "$B/appendix.md"; : > "$B/instructor.md"
idx=0
emit() {  # <src> <target> <demote>
  idx=$((idx+1))
  python3 latex/preprocess.py "$1" "$B/figs" "$B/e.md" "d${idx}f" "${3:-0}" >/dev/null
  cat "$B/e.md" >> "$2"; printf '\n\n' >> "$2"
}
# Introduction (print front matter) -> intro.md, then preprocess
python3 - > "$B/intro-raw.md" <<'PY'
import re
t = open("latex/front-matter.md", encoding="utf-8").read()
m = re.search(r'<section class="introduction">(.*?)</section>', t, re.S)
open("/dev/stdout", "w").write(m.group(1).strip())
PY
emit "$B/intro-raw.md" "$B/intro.md" 0

# Chapters 1-13: README (chapter) + exercises + resources (sections)
for ch in $(ls -d chapters/[01]*/ | sort); do
  emit "$ch/README.md" "$B/body.md" 0
  [ -f "$ch/exercises.md" ] && emit "$ch/exercises.md" "$B/body.md" 1
  [ -f "$ch/resources.md" ] && emit "$ch/resources.md" "$B/body.md" 1
done
# Appendix A + templates
A=chapters/appendix-a-team-project
emit "$A/README.md" "$B/appendix.md" 0
emit "$A/two-week-sprints.md" "$B/appendix.md" 1
emit "$A/exercises.md" "$B/appendix.md" 1
emit "$A/resources.md" "$B/appendix.md" 1
printf '\n# Project Templates\n\n' >> "$B/appendix.md"
for t in idea-pitch project-proposal sprint-report status-report team-review final-report individual-writeup; do
  emit "templates/$t.md" "$B/appendix.md" 1
done
# Instructor resources
printf '\n# Instructor Resources\n\n' >> "$B/instructor.md"
emit "curriculum/open-resources-map.md" "$B/instructor.md" 1
emit "curriculum/course-plan.md" "$B/instructor.md" 1

# --- assemble one markdown with raw-LaTeX front/main/appendix/back matter ---
{
  printf '```{=latex}\n\\frontmatter\n```\n'
  printf '```{=latex}\n'; cat latex/title.tex; printf '\n```\n\n'
  cat "$B/intro.md"
  printf '\n```{=latex}\n\\cleardoublepage\n\\tableofcontents\n\\mainmatter\n```\n\n'
  cat "$B/body.md"
  printf '\n```{=latex}\n\\appendix\n```\n\n'
  cat "$B/appendix.md"
  cat "$B/instructor.md"
  printf '\n```{=latex}\n\\backmatter\n\\printglossary[title={Glossary},toctitle={Glossary}]\n```\n\n'
  printf '```{=latex}\n'; cat latex/references.tex; printf '\n```\n'
} > "$B/combined.md"
cp latex/glossary-defs.tex "$B/glossary-defs.tex"

echo "=== rendering diagrams ==="
bash latex/render-diagrams.sh "$B/figs"

echo "=== pandoc -> standalone LaTeX ==="
tex pandoc "$R/$B/combined.md" -f markdown-implicit_header_references -o "$R/$B/book.tex" -s \
  --top-level-division=chapter --number-sections \
  --syntax-definition="$R/tools/generic.xml" --highlight-style=tango \
  --include-in-header="$R/latex/preamble.tex" --lua-filter="$R/latex/footnotes.lua" --lua-filter="$R/latex/callouts.lua" \
  -V documentclass=scrbook -V classoption=11pt,twoside,openright 2>&1 | grep -iE 'error' || true

echo "=== xelatex + makeglossaries + xelatex x2 ==="
read -r -d '' COMPILE <<EOF || true
cd "$R/$B"
python3 "$R/latex/fix-tex.py" book.tex
xelatex -interaction=nonstopmode -halt-on-error book.tex >p1.log 2>&1 || { echo "PASS1 FAIL"; grep -iE "^\\!" p1.log | head; exit 1; }
makeglossaries book >mg.log 2>&1 || echo "(makeglossaries issues)"
xelatex -interaction=nonstopmode book.tex >p2.log 2>&1
xelatex -interaction=nonstopmode book.tex >p3.log 2>&1
rm -f "$R/latex/swebook-interior.pdf"; cp book.pdf "$R/latex/swebook-interior.pdf"
echo "compile done"
EOF
texsh "$COMPILE"

if [ -f latex/swebook-interior.pdf ]; then echo "built: latex/swebook-interior.pdf"; else echo "BUILD FAILED"; exit 1; fi
