#!/usr/bin/env python3
"""Preprocess a Markdown file for the LaTeX book build.

Usage: preprocess.py <in.md> <fig-dir> <out.md> [fig-prefix=fig] [demote=0]

  fig-prefix  unique per source file so figures don't collide across chapters
  demote      raise every heading by N levels (merge exercises/resources into a
              chapter as sections instead of new chapters)

Transforms: drop web-only code-system paragraphs and chapter-end web nav; strip
the "Chapter N —" prefix and manual section numbers (LaTeX auto-numbers); keep
only the generic code fence; mermaid -> grayscale figure include; unwrap links to
text; fix the non-breaking hyphen absent from Endure.
"""
import sys, re

import json
inp, figdir, out = sys.argv[1:4]
inp = re.sub(r'/+', '/', inp)   # normalize (ls -d adds a trailing slash -> chapters/x//README.md)
prefix = sys.argv[4] if len(sys.argv) > 4 else "fig"
demote = int(sys.argv[5]) if len(sys.argv) > 5 else 0
md = open(inp, encoding="utf-8").read()
try:
    caps = json.load(open("latex/captions.json")).get(inp, [])
except Exception:
    caps = []
def texesc(s):
    for a, b in [("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_")]:
        s = s.replace(a, b)
    return s
def outside_fences(text, fn):
    """Apply fn only to text outside ``` fenced code blocks (and mermaid)."""
    parts = re.split(r'(?ms)(^[ \t]*```.*?^[ \t]*```[ \t]*$)', text)
    return ''.join(p if i % 2 else fn(p) for i, p in enumerate(parts))

# --- print cleanup: drop web-only paragraphs (six languages / tabs / ?lang) ---
md = re.sub(r'\n\n((?:[^\n]|\n(?!\n))*?'
            r'(?:appears in six languages|behind a row of tabs|\?lang=|'
            r'The others are worth your attention)'
            r'(?:[^\n]|\n(?!\n))*)', '', md)
# chapter-end nav/takeaway bullets (exercises/resources follow directly in print)
md = re.sub(r'(?m)^[-*] .*(?:Continue to the (?:\[)?Exercises|'
            r'Go deeper with the (?:\[)?Open Resources|'
            r'\*\*Key takeaways\*\* are summarized).*\n?', '', md)
# the divider that bracketed those bullets is now orphaned at the file end
md = re.sub(r'(?m)\n+---[ \t]*\n\s*$', '\n', md)

# --- headings: let LaTeX number them ---
md = re.sub(r'(?m)^(# )Chapter\s+\d+\s*[—:–-]\s*', r'\1', md)
md = re.sub(r'(?m)^(# )Appendix\s+[A-Z]\s*[—:–-]\s*', r'\1', md)
md = re.sub(r'(?m)^(#{2,6} )(?:[A-Z]\.)?\d+(?:\.\d+)*\.?\s+', r'\1', md)
# templates: drop fill-in placeholders (and any dangling em-dash) from headings
md = re.sub(r'(?m)^(#{1,6} .*)$',
            lambda m: re.sub(r'\s*[—–-]?\s*<[^>]*>', '', m.group(1)).rstrip(' —–-'), md)
if demote:
    md = re.sub(r'(?m)^(#{1,5}) ', lambda m: '#' * (len(m.group(1)) + demote) + ' ', md)

md = md.replace('‑', '-')                      # U+2011 not in Endure
md = re.sub(r'\^\\\*', r'^{\\ast}', md)   # MathJax z^\* -> LaTeX z^{\ast}
# join words the source wrapped right after a hyphen or slash ("vendor-\nneutral")
md = outside_fences(md, lambda t: re.sub(r'(\w[-/])\n[ \t]{0,3}(?=\w)', r'\1', t))
md = outside_fences(md, lambda t: re.sub(r'(\w[-/])\n> ?(?=\w)', r'\1', t))
# a line-leading "(1972)", "(b)", or "2019)" is prose (usually a wrapped
# parenthetical inside a bullet), not a fancy-list item — escape it, at any indent
md = outside_fences(md, lambda t: re.sub(r'(?m)^([ \t]*)\((\w{1,4})\)', r'\1\\(\2)', t))
md = outside_fences(md, lambda t: re.sub(r'(?m)^([ \t]*)(\d{1,4})\)', r'\1\2\\)', t))
# keep "(October 2013)"-style dates on one line
md = outside_fences(md, lambda t: re.sub(
    r'\((January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})\)',
    r'(\1\\ \2)', t))


# --- numbered citations: footnote markers become superscript [n] pointing at the
# --- References chapter (numbers assigned by latex/make-references.py)
try:
    _cites = json.load(open("latex/citation-map.json")).get(inp, {})
except Exception:
    _cites = {}
if _cites:
    for lbl in _cites:                        # drop the footnote definitions
        md = re.sub(r'(?m)^\[\^' + re.escape(lbl) + r'\]:[^\n]*(?:\n(?!\[\^|#|\s*$)[^\n]*)*\n?',
                    '', md)
    md = re.sub(r'\[\^([^\]]+)\](?!:)',       # markers -> tokens
                lambda m: f'@@C{_cites[m.group(1)]}@@' if m.group(1) in _cites else m.group(0), md)
    md = re.sub(r'(?:@@C\d+@@)+',             # collapse adjacent, render superscript
                lambda m: '`\\textsuperscript{[' + ', '.join(re.findall(r'@@C(\d+)@@', m.group(0)))
                          + ']}`{=latex}', md)

# make remaining footnote labels unique per file — chapters reuse [^1],[^2],... which
# collide when concatenated, so pandoc resolves references to the wrong definition
md = outside_fences(md, lambda t: re.sub(r'\[\^(\w+)\]', lambda m: f'[^{prefix}fn{m.group(1)}]', t))
# print: drop the emoji type-legend sentence (icons become text labels; the
# legend would otherwise read "Course course · Video video")
md = re.sub(r'(?:Types|Legend):\s*[📘📄🎓]{1}[^.]*\.', '', md)
# emoji absent from Endure: map the resource-type icons to text labels, strip the rest
for _e, _t in {'📘': 'Book ', '🎓': 'Course ', '📄': 'Source ', '🎥': 'Video ', '🛠': 'Tool '}.items():
    md = md.replace(_e, _t)
md = re.sub(r'[\U0001F000-\U0001FAFF\U00002600-\U000026FF\U00002700-\U00002712\U00002714-\U00002716\U00002718-\U000027BF️]', '', md)
# render fill-in placeholders literally (pandoc otherwise drops <Team Name> as an HTML tag)
md = outside_fences(md, lambda t: re.sub(
    r'<(?!https?://|mailto:|/|br[ />])([A-Za-z0-9#][^<>\n]{0,58})>', r'\\<\1\\>', t))
# a list inside a blockquote needs a blank quote line before it, or it runs in
md = outside_fences(md, lambda t: re.sub(
    r'(?m)^(> [^\-\d\n][^\n]*)\n(?=> (?:- |\d+\. ))', '\\1\n>\n', t))
# a blockquote must be preceded by a blank line, or pandoc leaks the ">" as text
md = outside_fences(md, lambda t: re.sub(r'(?m)^([^>\n].*)\n(>)', r'\1\n\n\2', t))

# --- drop per-chapter Sources heading (footnotes stay; consolidated bib at back) ---
md = re.sub(r'(?m)^#{2,4}\s+Sources\s*$\n?', '', md)
# drop the divider that separated the body from the Sources block (now an empty
# double-rule box, since the footnotes render at the page bottom, not inline)
md = re.sub(r'(?m)^---[ \t]*\n\s*\n(?=\[\^)', '', md)
# --- drop per-chapter License note (one overarching license on the copyright page) ---
md = re.sub(r'(?ms)^##\s+License note\b.*', '', md)

# --- tag terms with \index for the back-of-book index (page refs, no definitions) ---
def _norm(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())
def _cands(term):
    out = [term]
    nop = re.sub(r'\s*\([^)]*\)', '', term).strip()          # drop parenthetical
    if nop and nop != term:
        out.append(nop)
    p = re.search(r'\(([^)]+)\)', term)                      # the abbreviation itself
    if p:
        out.append(p.group(1).strip())
    for suf in ('pattern', 'model', 'culture', 'testing', 'manifesto', 'diagram'):
        if nop.lower().endswith(' ' + suf):
            out.append(nop[:-(len(suf) + 1)].strip())
    if nop:                                                 # plural / singular of last word
        parts = nop.split()
        last = parts[-1]
        pl = last[:-1] + 'ies' if last.endswith('y') else last + 'es' if last.endswith(('s', 'x', 'ch')) else last + 's'
        out.append(' '.join(parts[:-1] + [pl]))
        if last.endswith('s'):
            out.append(' '.join(parts[:-1] + [last[:-1]]))
    return [c for c in dict.fromkeys(out) if c]
def _plain(md, needle):
    for m in re.finditer(r'(?i)\b' + needle + r'\b', md):
        ls = md.rfind('\n', 0, m.start()) + 1
        if md[ls] == '#' or md[:m.start()].count('`') % 2:
            continue
        return m.end()
    return None
def _find(md, term):
    cands = _cands(term)
    for m in re.finditer(r'\*\*([^*]+)\*\*', md):            # 1) bold use
        cn = _norm(m.group(1))
        for c in cands:
            tn = _norm(c)
            if tn and (cn == tn or tn in cn or cn in tn):
                return m.end()
    for c in cands:                                          # 2) plain candidate
        h = _plain(md, re.escape(c))
        if h is not None:
            return h
    words = re.findall(r'[A-Za-z0-9][\w-]{2,}', re.sub(r'\([^)]*\)', '', term))
    if len(words) >= 2:                                      # 3) interrupted phrase
        h = _plain(md, re.escape(words[0]) + r'[\s\S]{0,40}?' + re.escape(words[-1]))
        if h is not None:
            return h
    return None
def _idxterm(term):                       # clean display/sort term for \index
    t = re.sub(r'\s*\([^)]*\)', '', term).strip() or term
    for a, b in [('\\', r'\textbackslash '), ('#', r'\#'), ('&', r'\&'),
                 ('_', r'\_'), ('$', r'\$'), ('%', r'\%'), ('{', r'\{'),
                 ('}', r'\}'), ('^', r'\textasciicircum{}'), ('~', r'\textasciitilde{}')]:
        t = t.replace(a, b)
    for c in ('"', '!', '@', '|'):        # makeindex control chars -> escape with " ('"' first)
        t = t.replace(c, '"' + c)
    return t
try:
    _gm_all = json.load(open("latex/gloss-map.json"))
    _gm_here = _gm_all.get(inp, [])
    _all_terms = list({t for pairs in _gm_all.values() for t, _ in pairs})
except Exception:
    _gm_here, _all_terms = [], []
idx_pts = []
for term, _ in _gm_here:                  # 1) primary occurrence — guarantees every term is indexed
    h = _find(md, term)
    if h is not None:
        idx_pts.append((h, term))
_cn = {t: {_norm(c) for c in _cands(t) if _norm(c)} for t in _all_terms}
for m in re.finditer(r'\*\*([^*]+)\*\*', md):   # 2) every boldface use of a known term -> extra page refs
    cn = _norm(m.group(1))
    if cn:
        for t in _all_terms:
            if cn in _cn[t]:
                idx_pts.append((m.end(), t)); break

# 3) curated extra entries (latex/index-extra.json) — people, case studies, tools,
#    standards, subentries, and see-references. Each item is [pattern, raw_entry]:
#    `pattern` locates the page (searched like a term; "" = end of this file), and
#    `raw_entry` is inserted VERBATIM as \index{...}, so makeindex syntax works:
#    "coverage!branch" (subentry), "MTTR|see{DORA delivery metrics}" (alias).
#    The special key "_aliases" is a list of raw entries emitted once, with ch01.
try:
    _extra = json.load(open("latex/index-extra.json"))
except Exception:
    _extra = {}
def _find_literal(text, pat):             # exact, case-sensitive; skip code + headings + footnote defs
    for m in re.finditer(re.escape(pat), text):
        ls = text.rfind('\n', 0, m.start()) + 1
        if text[ls] in '#' or text[ls:ls + 2] == '[^' or text[:m.start()].count('`') % 2:
            continue
        return m.end()
    return None
raw_pts = []
for pat, entry in _extra.get(inp, []):
    if pat:
        h = _find_literal(md, pat)
        if h is not None:
            raw_pts.append((h, entry))
        else:
            sys.stderr.write(f"index-extra: pattern not found in {inp}: {pat!r}\n")
    else:
        raw_pts.append((len(md), entry))
if inp == "chapters/01-introduction/README.md":
    for entry in _extra.get("_aliases", []):
        raw_pts.append((len(md), entry))

ins = [(pos, _idxterm(term)) for pos, term in idx_pts] + raw_pts
_seen = set()
for pos, ent in sorted(ins, key=lambda x: x[0], reverse=True):   # insert from the end
    if (pos, ent) in _seen:
        continue
    _seen.add((pos, ent))
    md = md[:pos] + '\\index{' + ent + '}' + md[pos:]

# --- code fences: keep only generic ---
md = re.sub(r'(?ms)^[ \t]*```(?:go|java|javascript|python|ruby|typescript)[ \t]*\n.*?^[ \t]*```[ \t]*$\n?', '', md)

# --- mermaid -> grayscale figure include (write .mmd for rendering) ---
import datetime
def _fix_gantt(src):
    """A `gantt` with `dateFormat X` reads week numbers as unix seconds, so every
    task lands at the epoch and the chart collapses. Convert to real dates."""
    if not re.match(r'\s*gantt\b', src) or not re.search(r'dateFormat\s+X\b', src):
        return src
    base = datetime.date(2026, 1, 5)
    def repl(m):
        pre, start, dur = m.group(1), int(m.group(2)), int(m.group(3))
        d = (base + datetime.timedelta(weeks=start)).isoformat()
        return f"{pre}{d}, {dur}w" if dur > 0 else f"{pre}{d}, 0d"
    src = re.sub(r'(?m)(:.*?)(\d+)\s*,\s*(\d+)\s*$', repl, src)
    src = re.sub(r'dateFormat\s+X', 'dateFormat YYYY-MM-DD', src)
    src = re.sub(r'axisFormat\s+\S+', 'axisFormat %b %d', src)
    src = re.sub(r'(?m)^(\s*title .*)$', r'\1\n    todayMarker off', src, count=1)
    return src
XY_INIT = ('%%{init: {"xyChart": {"width": 1000, "height": 600, "titleFontSize": 18, '
           '"titlePadding": 10, "xAxis": {"labelFontSize": 13, "labelPadding": 6}, '
           '"yAxis": {"labelFontSize": 13, "labelPadding": 6, "titleFontSize": 15, "titlePadding": 14}}, '
           '"themeVariables": {"xyChart": {"plotColorPalette": "#8a8a8a"}}}}%%')
def _fix_xychart(src):
    """xychart-beta: reserve gutter for the y-axis title (else it overprints the
    tick numbers), darken the bars for B&W print, and fix the canvas size."""
    if re.match(r'\s*xychart', src) and '%%{init' not in src:
        return XY_INIT + '\n' + src
    return src

figs = []
def mm(m):
    src = m.group(1).replace('&nbsp;', ' ')
    src = re.sub(r'(?m)^\s*classDef .*$', '', src)
    src = re.sub(r':::[A-Za-z0-9_]+', '', src)
    src = _fix_gantt(src)
    src = _fix_xychart(src)
    figs.append(src); n = len(figs)
    # path RELATIVE to the xelatex working dir (latex/bookbuild), not an absolute
    # /book/... which only exists when the repo is Docker-mounted there. figdir is
    # "<bookbuild>/figs"; xelatex runs from "<bookbuild>", so "figs/..." resolves in
    # Docker and native CI alike.
    fn = f'{figdir.rstrip("/").rsplit("/", 1)[-1]}/{prefix}{n}.png'
    cap = r'\caption{' + texesc(caps[n - 1]) + '}' if n - 1 < len(caps) else ''
    # rasters are 3x device scale (gantt: 2x); scale to TRUE size, cap at text width —
    # a three-node diagram should not be stretched to a full page
    scale = '0.375' if re.match(r'\s*gantt', src) else '0.25'
    return (r'\begin{figure}[htbp]\centering\includegraphics[scale=' + scale +
            r',max width=\linewidth,max totalheight=0.72\textheight]{' + fn + '}'
            + cap + r'\end{figure}')
md = re.sub(r'(?ms)^```mermaid[ \t]*\n(.*?)^```[ \t]*$', mm, md)

# --- links (print has none): bare-domain text gets the FULL target URL (a print
# --- reader cannot follow "doi.org."); prose link text stays as plain text
def _unlink(m):
    txt, url = m.group(1), m.group(2)
    if re.fullmatch(r'[a-z0-9.\-]+', txt) and url.startswith('http'):
        bare = re.sub(r'^https?://(www\.)?', '', url).rstrip('/')
        if bare.lower() != txt.lower().rstrip('/'):
            return '`\\url{' + url + '}`{=latex}'
    return txt
md = outside_fences(md, lambda t: re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]*)\)', _unlink, t))
# wrap bare prose URLs in \url{} so xurl can break them (they overflow otherwise).
# Protect inline code spans and <autolinks> first: wrapping a fragment INSIDE them
# corrupts the URL (https://www./url%7B...%7D in print). Autolinks become \url too.
_URL = re.compile(
    r'(?<![\w@/<\[(.\-~])('
    r'https?://[^\s)<>\]]+'
    r'|(?:[a-z0-9-]+\.)+[a-z]{2,}/[^\s)<>\]]+'
    r'|(?:[a-z0-9-]+\.)+(?:com|org|net|edu|gov|io|dev|co|uk|ca|de|info|no|ai|app|xyz|google|blog)\b'
    r')')
def _wrapurl(m):
    u, trail = m.group(1), ''
    while u and u[-1] in '.,;:)':
        trail = u[-1] + trail; u = u[:-1]
    return r'\url{' + u + '}' + trail
_prot = []
def _keep(tex):
    _prot.append(tex)
    return f'@@P{len(_prot)-1}@@'
def _protect_and_wrap(t):
    t = re.sub(r'`[^`\n]+`', lambda m: _keep(m.group(0)), t)
    t = re.sub(r'<(https?://[^>\s]+)>',
               lambda m: _keep('`\\url{' + m.group(1) + '}`{=latex}'), t)
    return _URL.sub(_wrapurl, t)
md = outside_fences(md, _protect_and_wrap)
md = re.sub(r'@@P(\d+)@@', lambda m: _prot[int(m.group(1))], md)

for i, s in enumerate(figs, 1):
    open(f'{figdir}/{prefix}{i}.mmd', 'w', encoding='utf-8').write(s)
open(out, 'w', encoding='utf-8').write(md)
print(f'{prefix}: {len(figs)} figures')
