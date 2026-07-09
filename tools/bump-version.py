#!/usr/bin/env python3
"""Set the book version everywhere it is HARDCODED (not derived from the git tag).

    tools/bump-version.py 1.0b2                  # all hardcoded spots (local / release)
    tools/bump-version.py 1.0b2 --repo           # repo-facing surfaces on main
                                                 #   (CITATION.cff + README.md) — version-sync CI
    tools/bump-version.py 1.0b2 --citation-only  # just CITATION.cff (legacy alias)

Then rebuild the interior PDF, commit, and tag:

    bash latex/book-build.sh
    git add -A && git commit -m "Release 1.0b2"
    git tag v1.0b2 && git push --tags

Tag-driven surfaces (deployed web sidebar, EPUB metadata, EPUB covers) pick up the
version from the tag automatically, so they are NOT touched here. The KDP print
cover wrap ("1st Beta Edition" / "1β") is intentionally left alone.
"""
import re, sys, pathlib, datetime

citation_only = "--citation-only" in sys.argv[1:]
repo_only = "--repo" in sys.argv[1:]
args = [a for a in sys.argv[1:] if a not in ("--citation-only", "--repo")]
if len(args) != 1:
    sys.exit(__doc__)
V = args[0].lstrip("v")                           # accept "v1.0b2" or "1.0b2"
if not re.fullmatch(r"\d+\.\d+(b\d+)?", V):
    sys.exit(f"error: {V!r} is not a version like 1.0b2 or 1.0")
ROOT = pathlib.Path(__file__).resolve().parent.parent
TODAY = datetime.date.today().isoformat()

# (file, pattern, replacement, expected_count)
EDITS = [
    ("CITATION.cff",   r'(?m)^version: "[^"]*"',                    f'version: "{V}"',                 1),
    ("CITATION.cff",   r'(?m)^date-released: "[^"]*"',              f'date-released: "{TODAY}"',       1),
    ("CITATION.cff",   r'edition: "First Edition, [^"]*"',          f'edition: "First Edition, {V}"',  1),
    ("README.md",      r'\*First Edition, [^*\n]*\*',               f'*First Edition, {V}.*',          1),
    ("latex/title.tex",r'First Edition, [^\\]*\\par',              f'First Edition, {V}\\par',         1),
    ("latex/title.tex",r'First Edition \([^)]*\), 2026',           f'First Edition ({V}), 2026',       1),
    ("version.js",     r'const VERSION = "[^"]*"',                  f'const VERSION = "{V}"',           1),
]
if repo_only:                                     # version-sync CI: repo-facing files on main
    EDITS = [e for e in EDITS if e[0] in ("CITATION.cff", "README.md")]
elif citation_only:                               # legacy: CITATION.cff only
    EDITS = [e for e in EDITS if e[0] == "CITATION.cff"]

changed = []
for rel, pat, repl, want in EDITS:
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")
    s2, n = re.subn(pat, lambda _m, r=repl: r, s)   # literal repl (no \-escape processing)
    if n != want:
        sys.exit(f"error: {rel}: pattern /{pat}/ matched {n}x, expected {want}x "
                 "(the file may have drifted — update bump-version.py)")
    if s2 != s:
        p.write_text(s2, encoding="utf-8")
        changed.append(rel)

print(f"version set to {V} (date-released {TODAY}).")
print("updated:", ", ".join(sorted(set(changed))) or "(already current)")
print("next: rebuild the PDF (bash latex/book-build.sh), then commit and tag:")
print(f"      git add -A && git commit -m 'Release {V}' && git tag v{V} && git push --tags")
