#!/usr/bin/env python3
"""Renumber chapters 8..13 -> 9..14 (to insert a new Chapter 8: Version Control
with Git). Shifts internal cross-references only; protects citations to external
books (Clean Code, Shape Up, ESaaS, Software Engineering at Google).

Run from the book root. Pass --apply to write; default is a dry-run report.
"""
import re, sys, glob, os

APPLY = '--apply' in sys.argv
RENAMED = {  # dir basename -> (old chapter number, new)
    '08-static-checking': (8, 9),
    '09-testing': (9, 10),
    '10-software-security': (10, 11),
    '11-quality-metrics': (11, 12),
    '12-ai-across-the-lifecycle': (12, 13),
    '13-delivery': (13, 14),
}
EXT_BOOKS = ('Clean Code', 'Shape Up', 'ESaaS', 'Software Engineering at Google',
             'Engineering Software as a Service')

def shift(n):
    n = int(n)
    return n + 1 if 8 <= n <= 13 else n

def _shift_dotted(tok):            # "13.2" -> "14.2" ; "9" -> "10" ; "2.4" -> "2.4"
    parts = tok.split('.')
    parts[0] = str(shift(parts[0]))
    return '.'.join(parts)

def shift_sections(text):          # §13.2 , §§11.6–11.9 , §2.4–2.5
    def repl(m):
        body = re.sub(r'\d+(?:\.\d+)*', lambda t: _shift_dotted(t.group(0)), m.group(2))
        return m.group(1) + body
    return re.sub(r'(§§?)\s*(\d+(?:\.\d+)*(?:\s*[–—-]\s*\d+(?:\.\d+)*)*)', repl, text)

def shift_links(text):             # ../13-delivery/#132-slug -> ../14-delivery/#142-slug
    def repl(m):
        nn, name, anchor = m.group(1), m.group(2), m.group(3) or ''
        oldc = int(nn); newc = shift(oldc)
        if newc == oldc:
            return m.group(0)
        new_nn = f'{newc:02d}'
        am = re.match(r'#(\d+)(.*)', anchor)
        if am and am.group(1).startswith(str(oldc)):
            anchor = '#' + str(newc) + am.group(1)[len(str(oldc)):] + am.group(2)
        return f'../{new_nn}{name}{anchor}'
    return re.sub(r'\.\./(\d{2})(-[a-z0-9-]+/)(#[\w-]+)?', repl, text)

def shift_chapter_words(line):     # "Chapter 8", "Chapters 8–11", "Ch. 8", "Ch. 8–9"
    if any(b in line for b in EXT_BOOKS):
        return line                # whole line cites an external book -> leave it
    def repl(m):
        # protect refs immediately followed by a quoted title (external, multi-line cites)
        after = line[m.end():m.end() + 4]
        if re.match(r'\s*,?\s*["“]', after):
            return m.group(0)
        pre, n1, rng = m.group(1), m.group(2), m.group(3)
        out = pre + str(shift(n1))
        if rng:
            sep = re.match(r'\s*[–—-]\s*', rng).group(0)
            out += sep + str(shift(re.search(r'\d+', rng).group(0)))
        return out
    return re.sub(r'\b(Chapters?\s+|[Cc]h\.\s+)(\d{1,2})(\s*[–—-]\s*\d{1,2})?', repl, line)

def process(text):
    text = shift_sections(text)
    text = shift_links(text)
    text = '\n'.join(shift_chapter_words(ln) for ln in text.split('\n'))
    return text

files = (glob.glob('chapters/*/*.md') + glob.glob('templates/*.md') +
         glob.glob('curriculum/*.md'))
changed = 0
for f in files:
    s = open(f, encoding='utf-8').read()
    out = process(s)
    if out != s:
        changed += 1
        if APPLY:
            open(f, 'w', encoding='utf-8').write(out)

# section-number headings inside the 6 renamed chapter READMEs (## 8.1 -> ## 9.1)
head_changed = 0
for d, (old, new) in RENAMED.items():
    p = f'chapters/{d}/README.md'
    if not os.path.exists(p):
        continue
    s = open(p, encoding='utf-8').read()
    out = re.sub(rf'(?m)^(#{{1,6}}\s+){old}(\.\d)', rf'\g<1>{new}\2', s)
    if out != s:
        head_changed += 1
        if APPLY:
            open(p, 'w', encoding='utf-8').write(out)

print(('APPLIED' if APPLY else 'DRY-RUN') +
      f': {changed} files with ref shifts, {head_changed} READMEs with heading shifts')
