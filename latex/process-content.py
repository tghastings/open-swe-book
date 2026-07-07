#!/usr/bin/env python3
"""Turn the book-content-extract workflow output into build artifacts:
  latex/captions.json      {readme_path: [captions in document order]}
  latex/bibliography.tex   numbered, alphabetized reference list
  latex/glossary-defs.tex  \\newglossaryentry definitions (glossaries package)
  latex/gloss-map.json     {readme_path: [[term, key], ...]} for \\glsadd tagging
Usage: process-content.py <workflow-output.json>
"""
import sys, json, re

data = json.load(open(sys.argv[1]))["result"]

def esc(s):
    s = (s or "")
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("#", r"\#"),
                 ("_", r"\_"), ("$", r"\$"), ("~", r"\textasciitilde{}"),
                 ("^", r"\textasciicircum{}"), ("{", r"\{"), ("}", r"\}")]:
        s = s.replace(a, b)
    return s
def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())
def sortkey(a, t):
    return re.sub(r"[^a-z0-9 ]", "", (a or t or "").lower()).strip()

# --- captions.json ---
captions = {f"{c['dir']}/README.md": c["captions"] for c in data}
json.dump(captions, open("latex/captions.json", "w"), indent=1)

# --- bibliography.tex: numbered, alphabetized reference list ---
seen_title, refs = set(), []
for c in data:
    for b in c["bib"]:
        nt = norm(b.get("title"))
        if not nt or nt in seen_title:
            continue
        seen_title.add(nt)
        parts = []
        if b.get("author"):
            parts.append(esc(b["author"].strip().rstrip(",")))
        if b.get("year"):
            parts.append(f"({esc(b['year'])})")
        head = " ".join(parts)
        ref = (head + ". " if head else "") + r"\textit{" + esc(b.get("title", "")) + "}."
        if b.get("publisher"):
            ref += " " + esc(b["publisher"]) + "."
        if b.get("url"):
            ref += r" \url{" + b["url"].replace("%", r"\%").replace("#", r"\#") + "}"
        refs.append((sortkey(b.get("author"), b.get("title")), ref))
refs.sort(key=lambda r: r[0])
with open("latex/bibliography.tex", "w") as f:
    f.write("\\chapter{Bibliography}\n\\begingroup\\raggedright\n"
            "\\setlength{\\parindent}{0pt}\\setlength{\\parskip}{0pt}\n")
    for i, (_, ref) in enumerate(refs, 1):
        f.write(f"\\par\\hangindent=2.2em\\hangafter=1 \\makebox[1.9em][l]{{{i}.}}{ref}"
                "\\par\\addvspace{0.4em}\n")
    f.write("\\endgroup\n")

# --- glossary: \newglossaryentry defs + per-chapter term->key map ---
gloss, gmap, usedkeys = {}, {}, set()   # gloss: norm_term -> (term, definition, key)
for c in data:
    readme = f"{c['dir']}/README.md"
    for g in c["glossary"]:
        term = g["term"].strip()
        n = norm(term)
        if not n or n in gloss:
            continue
        key = re.sub(r"[^a-z0-9]", "", term.lower()) or f"g{len(gloss)}"
        while key in usedkeys:
            key += "x"
        usedkeys.add(key)
        gloss[n] = (term, g["definition"].strip(), key)
        gmap.setdefault(readme, []).append([term, key])
json.dump(gmap, open("latex/gloss-map.json", "w"), indent=1)
with open("latex/glossary-defs.tex", "w") as f:
    for n in sorted(gloss, key=lambda k: gloss[k][0].lower()):
        term, d, key = gloss[n]
        if not d.endswith("."):
            d += "."
        d = re.sub(r'(^|\s)”', r'\1“', d)   # ”done” -> “done”
        d2 = re.sub(r'\^(\w+)', lambda m: '@@SUP' + m.group(1) + '@@', d)  # Size^b
        d_tex = esc(d2).replace('@@SUP', r'\textsuperscript{').replace('@@', '}')
        f.write(f"\\newglossaryentry{{{key}}}{{name={{{esc(term)}}},"
                f"description={{{d_tex}}}}}\n")

print(f"captions: {sum(len(v) for v in captions.values())} in {len(captions)} files")
print(f"bib: {len(refs)} numbered entries")
print(f"glossary: {len(gloss)} entries, mapped across {len(gmap)} chapters")
