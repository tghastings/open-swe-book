#!/usr/bin/env python3
"""Validate footnote numbering in the book's Markdown sources.

    tools/check-footnotes.py            # check every chapter + templates, report issues
    tools/check-footnotes.py --fix      # additionally renumber to first-use order (1..n)
    tools/check-footnotes.py <file>...  # check only the given files

Checks, per file (footnotes are per-page in mdBook, so files are independent):
  * every inline reference [^N] has exactly one definition [^N]:
  * every definition is referenced at least once
  * no duplicate definitions of the same number
  * numbers follow FIRST-USE order: the first marker to appear in the prose is [^1],
    the second new one [^2], and so on, with no gaps
  * the definitions block lists definitions in ascending order

Inline code spans and fenced code blocks are ignored (regexes like [^0-9] in a code
listing are not footnotes). --fix rewrites both markers and definitions to first-use
order and re-sorts the definitions block; it refuses to fix files with undefined or
duplicate footnotes (fix those by hand first — they are semantic, not mechanical).

Exit status: 0 clean, 1 issues found (so CI can gate on it).
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REF = re.compile(r"\[\^(\d+)\](?!:)")
DEF = re.compile(r"^\[\^(\d+)\]:")


def mask_code(text):
    """Blank out fenced code blocks and inline code spans, preserving offsets."""
    out = []
    in_fence = False
    for line in text.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append(" " * len(line))
            continue
        if in_fence:
            out.append(" " * len(line))
            continue
        # blank inline `code` spans
        out.append(re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line))
    return "\n".join(out)


def analyze(path):
    text = path.read_text(encoding="utf-8")
    masked = mask_code(text)
    lines = masked.split("\n")

    defs, def_order = {}, []            # number -> [line numbers]; numbers in file order
    for i, line in enumerate(lines, 1):
        m = DEF.match(line)
        if m:
            n = int(m.group(1))
            defs.setdefault(n, []).append(i)
            def_order.append(n)

    refs, use_order = {}, []            # number -> [line numbers]; first-use order
    for i, line in enumerate(lines, 1):
        if DEF.match(line):
            continue                    # a definition line is not a use
        for m in REF.finditer(line):
            n = int(m.group(1))
            refs.setdefault(n, []).append(i)
            if n not in use_order:
                use_order.append(n)

    issues = []
    for n in sorted(set(refs) - set(defs)):
        issues.append(f"UNDEFINED  [^{n}] used at line {refs[n][0]} but never defined")
    for n in sorted(set(defs) - set(refs)):
        issues.append(f"UNUSED     [^{n}]: defined at line {defs[n][0]} but never referenced")
    for n in sorted(k for k, v in defs.items() if len(v) > 1):
        issues.append(f"DUPLICATE  [^{n}]: defined at lines {', '.join(map(str, defs[n]))}")
    if use_order and use_order != list(range(1, len(use_order) + 1)):
        expect = list(range(1, len(use_order) + 1))
        issues.append(f"ORDER      first-use sequence is {use_order}, expected {expect}")
    referenced_defs = [n for n in def_order if n in refs]
    if referenced_defs != sorted(referenced_defs):
        issues.append(f"DEF-SORT   definitions appear as {def_order}, not ascending")
    return text, use_order, issues


def renumber(path, text, use_order):
    """Rewrite markers and definitions so first-use order is 1..n; sort the defs block."""
    mapping = {old: new for new, old in enumerate(use_order, 1)}
    masked = mask_code(text)
    src, out = text.split("\n"), []
    for raw, m in zip(src, masked.split("\n")):
        # rebuild the line, replacing only footnote tokens found in the MASKED copy
        newline, last = [], 0
        for match in re.finditer(r"\[\^(\d+)\](:?)", m):
            n = int(match.group(1))
            if n in mapping:
                newline.append(raw[last:match.start()])
                newline.append(f"[^{mapping[n]}]{match.group(2)}")
                last = match.end()
        newline.append(raw[last:])
        out.append("".join(newline))
    # sort the definitions block: collect each definition with its continuation lines
    masked2 = mask_code("\n".join(out))
    mlines = masked2.split("\n")
    blocks, i = [], 0                    # (start, end_exclusive, number)
    while i < len(mlines):
        m = DEF.match(mlines[i])
        if m:
            j = i + 1
            while j < len(mlines) and not DEF.match(mlines[j]) and (
                mlines[j].startswith((" ", "\t")) or mlines[j].strip() == ""
            ):
                j += 1
            blocks.append((i, j, int(m.group(1))))
            i = j
        else:
            i += 1
    if blocks:
        first, last = blocks[0][0], blocks[-1][1]
        contiguous = all(b[0] >= first and b[1] <= last for b in blocks)
        if contiguous:
            chunks = []
            for (s, e, n) in blocks:
                chunk = out[s:e]
                while chunk and chunk[-1].strip() == "":
                    chunk = chunk[:-1]
                chunks.append((n, chunk))
            chunks.sort(key=lambda c: c[0])
            flat = []
            for _, chunk in chunks:
                flat.extend(chunk + [""])
            if flat and flat[-1] == "" and last < len(out) and out[last].strip() == "":
                flat = flat[:-1]
            out = out[:first] + flat + out[last:]
    path.write_text("\n".join(out), encoding="utf-8")


def main():
    fix = "--fix" in sys.argv[1:]
    args = [a for a in sys.argv[1:] if a != "--fix"]
    if args:
        files = [pathlib.Path(a).resolve() for a in args]
    else:
        files = sorted(ROOT.glob("chapters/*/*.md")) + sorted(ROOT.glob("templates/*.md"))
    total = 0
    for path in files:
        if not path.exists():
            print(f"{path}: not found")
            total += 1
            continue
        text, use_order, issues = analyze(path)
        if not issues:
            continue
        rel = path.relative_to(ROOT) if str(path).startswith(str(ROOT)) else path
        print(f"\n{rel}:")
        for msg in issues:
            print(f"  {msg}")
        blocking = [m for m in issues if m.startswith(("UNDEFINED", "DUPLICATE"))]
        mechanical = [m for m in issues if m.startswith(("ORDER", "DEF-SORT"))]
        if fix and mechanical and not blocking:
            renumber(path, text, use_order)
            _, _, after = analyze(path)
            print(f"  FIXED -> renumbered to first-use order"
                  + (f"; remaining: {after}" if after else "; now clean"))
            total += len(after)
        else:
            if fix and blocking:
                print("  (not auto-fixed: undefined/duplicate footnotes need a human)")
            total += len(issues)
    if total == 0:
        print("all footnotes clean")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
