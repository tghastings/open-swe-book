#!/usr/bin/env python3
"""Build the numbered References section from the chapters' citation footnotes.

Scans every source file in book order, collects footnote definitions, dedupes
repeat citations of the same work (by italic title + year), and numbers entries
in order of first in-text citation — so the number a reader sees in the text is
the number in the References list, by construction.

Writes:
  latex/references.tex    \\chapter{References} with numbered entries
  latex/citation-map.json {file: {label: refnum}} consumed by preprocess.py
"""
import re, json, os, glob

def ordered_files():
    files = []
    for ch in sorted(glob.glob('chapters/[01]*/')):
        for base in ('README.md', 'exercises.md', 'resources.md'):
            p = ch + base
            if os.path.exists(p):
                files.append(p)
    A = 'chapters/appendix-a-team-project/'
    for base in ('README.md', 'two-week-sprints.md', 'exercises.md', 'resources.md'):
        if os.path.exists(A + base):
            files.append(A + base)
    for t in ('idea-pitch', 'project-proposal', 'sprint-report', 'status-report',
              'team-review', 'final-report', 'individual-writeup'):
        p = f'templates/{t}.md'
        if os.path.exists(p):
            files.append(p)
    files += ['curriculum/open-resources-map.md', 'curriculum/course-plan.md']
    return files

DEF_RE = re.compile(r'(?m)^\[\^([^\]]+)\]:[^\n]*(?:\n(?!\[\^|#|\s*$)[^\n]*)*')
REF_RE = re.compile(r'\[\^([^\]]+)\](?!:)')

def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

_variants = {}    # (author, year) -> list of (title_norm, key)
_by_url = {}      # normalized URL -> key       (same URL = same work)
_by_title = {}    # long title norm + year -> key (same long title+year = same work)

def _normurl(u):
    u = re.sub(r'^https?://(www\.)?', '', u.lower()).rstrip('/')
    return u

def dedup_key(text):
    """Same work cited twice (maybe different chapters/pages/author formats) ->
    one entry. Merges by (a) identical URL, (b) identical long title + year,
    (c) title-prefix variants under the same author and year."""
    u = re.search(r'\]\(([^)]+)\)', text)
    if u and _normurl(u.group(1)) in _by_url:
        return _by_url[_normurl(u.group(1))]
    t = re.search(r'\*([^*]+)\*', text)
    y = re.search(r'\b((?:19|20)\d{2})\b', text)
    year = y.group(1) if y else ''
    if not t:
        key = norm(re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text))[:120]
    else:
        parts = re.split(r'[:\u2014]', t.group(1), 1)
        main = t.group(1) if (len(parts) > 1 and re.match(r'\s*\d', parts[1])) else parts[0]
        title = norm(main)
        title = re.sub(r'^the', '', title)                 # "The Mythical..." == "Mythical..."
        author = norm(text.split('*', 1)[0])[:40]
        key = None
        if len(title) >= 12 and (title + year) in _by_title:
            key = _by_title[title + year]                   # distinctive title, same year
        if key is None:
            for t2, k2 in _variants.get((author, year), []):
                if len(title) >= 6 and (t2.startswith(title) or title.startswith(t2)):
                    key = k2; break
        if key is None:
            key = title + year
            _variants.setdefault((author, year), []).append((title, key))
        if len(title) >= 12:
            _by_title.setdefault(title + year, key)
    if u:
        _by_url.setdefault(_normurl(u.group(1)), key)
    return key

def canonical(text):
    """Reference-list form: drop citation-specific chapter/section pointers."""
    t = ' '.join(text.split())
    t = re.sub(r',?\s+chs?\.\s+(?:\d+\s*)?(?:[“"][^”"]*[”"])?[^,()]*', ' ', t)
    t = ' '.join(t.split())
    return t.replace(' ,', ',').replace(' .', '.').replace(' (', ' (')

def to_tex(s):
    links = []
    def keep(m):
        links.append(m.group(2))
        return f'@@L{len(links)-1}@@'
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', keep, s)
    for a, b in [('&', r'\&'), ('%', r'\%'), ('#', r'\#'), ('$', r'\$'), ('_', r'\_'),
                 ('~', r'\textasciitilde{}'), ('^', r'\textasciicircum{}')]:
        s = s.replace(a, b)
    s = re.sub(r'\*\*([^*]+)\*\*', r'\\textbf{\1}', s)
    s = re.sub(r'\*([^*]+)\*', r'\\textit{\1}', s)
    s = re.sub(r'`([^`]+)`', r'\\texttt{\1}', s)
    s = s.replace('‑', '-')
    # Straight double quotes reach XeLaTeX as raw LaTeX (pandoc's smart-quotes never
    # sees references.tex), so they render as a closing curly on BOTH sides. Make them
    # directional: opening after start/space/open-bracket/dash, closing otherwise.
    s = re.sub(r'(^|[\s(\[{—–-])"', '\\1“', s)
    s = s.replace('"', '”')
    for i, u in enumerate(links):
        s = s.replace(f'@@L{i}@@', r'\url{' + u.replace('%', r'\%').replace('#', r'\#') + '}')
    return s

entries = []          # canonical text, in first-citation order
key2num = {}
cmap = {}             # file -> {label: num}
uncited = 0

for f in ordered_files():
    src = open(f, encoding='utf-8').read()
    defs = {m.group(1): m.group(0).split(':', 1)[1].strip() for m in DEF_RE.finditer(src)}
    fmap = {}
    for m in REF_RE.finditer(src):
        lbl = m.group(1)
        if lbl in fmap or lbl not in defs:
            continue
        key = dedup_key(defs[lbl])
        if key not in key2num:
            entries.append(canonical(defs[lbl]))
            key2num[key] = len(entries)
        fmap[lbl] = key2num[key]
    uncited += sum(1 for d in defs if d not in fmap)
    if fmap:
        cmap[f] = fmap

json.dump(cmap, open('latex/citation-map.json', 'w'), indent=1)
with open('latex/references.tex', 'w') as out:
    out.write('\\chapter{References}\n\\begingroup\\raggedright'
              '\\setlength{\\parindent}{0pt}\\setlength{\\parskip}{0pt}\\small\n')
    for i, e in enumerate(entries, 1):
        out.write(f'\\par\\hangindent=2.6em\\hangafter=1 '
                  f'\\makebox[2.6em][l]{{[{i}]}}{to_tex(e)}\\par\\addvspace{{0.35em}}\n')
    out.write('\\endgroup\n')

n_cites = sum(len(v) for v in cmap.values())
print(f'references: {len(entries)} entries | citation labels mapped: {n_cites} '
      f'| files: {len(cmap)} | defs never cited: {uncited}')
