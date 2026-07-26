# AGENTS.md

Instructions for AI coding agents working with this repository. Written to the
[AGENTS.md](https://agents.md/) convention, which Claude Code, Cursor, Copilot, and others
read — the same tool-neutral practice Chapter 13 recommends.

This repository is **"Software Engineering: Standing on the Shoulders of Giants"** — an
open textbook (CC BY-SA 4.0 prose, MIT code) built with [mdBook](https://rust-lang.github.io/mdBook/)
and published at [swebook.org](https://www.swebook.org). Prose lives in `chapters/`, one
directory per chapter holding `README.md`, `exercises.md`, and `resources.md`.

There are two reasons an agent touches this repo. Jump to the one that applies.

---

## 1 · Grading a repository against the book

The repo ships a skill that scores **your own project** against the nine SDLC areas the
book teaches, with a letter grade per area and findings that cite the chapter teaching the
fix. It is for students running a course team project and for practitioners auditing
working code.

**Skill:** `.claude/skills/repo-scorecard/`

### Install it

The skill needs to live where your agent looks for skills — which is your project, not
this one. Copy it into whichever scope you want:

```bash
# just this project
mkdir -p /path/to/your-project/.claude/skills
cp -r .claude/skills/repo-scorecard /path/to/your-project/.claude/skills/

# or every project on this machine
mkdir -p ~/.claude/skills
cp -r .claude/skills/repo-scorecard ~/.claude/skills/
```

Then, from your project, ask your agent to *"score this repo"* / *"grade my repo against
the book"* and it will pick the skill up. Everything is stdlib Python 3 and offline — no
install step, no network, no API key.

### Run it directly

The two scripts also work standalone, without an agent:

```bash
# what the repo has — languages, tests, CI, linters, scanners, commit hygiene
python3 .claude/skills/repo-scorecard/repo-census.py /path/to/your-project

# findings JSON -> interactive HTML report (also --markdown, --fragment)
python3 .claude/skills/repo-scorecard/render-scorecard.py findings.json -o report.html
```

`repo-census.py` reports facts and grades nothing; the judgment is the agent's. The HTML
report is one self-contained file with severity and area filters, search, and per-finding
checkboxes that persist locally, so it doubles as the remediation worklist.

### Rules the skill must be run under

- **Read-only.** Never modify, stage, commit, or push in the repository being graded.
  Applying fixes is a separate request, after the owner has read the scorecard.
- **Never execute the graded project's code** to "see if it works" — no `npm install`, no
  `make`, no running its test suite. Grade by reading.
- **Write the report outside the graded repo** unless its owner asks otherwise. A review
  artifact should never turn up in their `git status`.
- **Verify absence before claiming it.** "No tests" without a search that would have found
  them is the failure mode that makes a scorecard worthless. `rubric.md` and the skill's
  Step 3 spell out the triple-check.
- **If a live credential turns up, lead with it** and tell the owner to rotate first and
  scrub history second. Never paste the secret value into the report.

`SKILL.md` holds the workflow; `rubric.md` holds the per-area criteria, weights, grade
bands, the no-double-jeopardy rule, and the anti-inflation/anti-deflation guards. Read
both before grading — they exist because ungrounded grading is worse than none.

---

## 2 · Contributing to the book itself

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) first for house style. It governs; this section
adds the mechanical rules an agent will otherwise get wrong.

### Build and preview

```bash
# live-reload preview on :3000
docker run -d --name se-book -p 3000:3000 -v "$PWD:/book" se-book-mdbook

# one-shot verification build — ALWAYS to .verify (gitignored), never an ad-hoc dir
docker run --rm -v "$PWD:/book" se-book-mdbook mdbook build -d /book/.verify
docker run --rm -v "$PWD:/book" se-book-mdbook rm -rf /book/.verify
```

The image is mdBook 0.4.40 + mdbook-mermaid. **mdBook alone silently leaves Mermaid blocks
unrendered** — if diagrams vanish, that is why. A one-shot build run while the serve
container is watching will race it; build to `.verify` instead.

### Rules that will bite you

- **Never link to a `README.md`.** mdBook rewrites those to a nonexistent `README.html`.
  Link chapters in directory form — `../08-version-control-git/` or `../02-…/#anchor`.
  `SUMMARY.md` is the one file that keeps real `.md` paths.
- **No `#anchors` in `SUMMARY.md`** — mdBook fails with "Chapter file not found." Sidebar
  sub-navigation is injected at runtime by `subsections.js`.
- **Footnotes are per-page** and numbered by first use, with no gaps. Adding or moving
  cited prose breaks this silently. Validate, and let `--fix` renumber:
  ```bash
  python3 tools/check-footnotes.py            # exit 0 = clean
  python3 tools/check-footnotes.py --fix      # renumber mechanical issues
  ```
  It runs in CI on pushes to `main` and on tags.
- **Chapter exercise tags are `[warm‑up]` and `[analysis]` only** — and the warm-up tag
  uses a **non-breaking hyphen (U+2011)**, not ASCII `-`. Grepping `[warm-up]` returns
  zero hits across the whole book; match `[warm.up]` or the literal `‑`. Appendix A is the
  exception: its project checkpoints use `[team]` / `[project]` / `[analysis]`, documented
  in its own intro.
- **Example values are deliberate.** Names, numbers, and figures in worked examples were
  chosen on purpose. Do not normalize, round, or swap them for "more realistic" ones while
  editing nearby prose.
- **`latex/references.tex` is generated** by `latex/make-references.py` from the chapter
  footnotes — never hand-edit it. Same for `latex/citation-map.json`.
- **The print interior is black-and-white grayscale.** Never propose color figures, and
  check that any new diagram survives losing its hue.
- **Claims stay confident but falsifiable.** The house voice is direct and memorable, but
  a textbook must model contextual reasoning — scope absolute formulations ("always",
  "never", "every team") with a qualifier that keeps the voice: "As a default team
  policy…", "In most conventional web deployments…", "For beginner teams…".

### Style, in one paragraph

Second person, explain the *why* before the *how*, US spelling, prose wrapped at 90–100
columns. Bold a term at first use. Diagrams are Mermaid fenced blocks — labels beginning
`1. ` parse as a Markdown list and break the render, so write `"1 · Planning"`. Callouts
are blockquotes with a bold lead-in: `> **Principle.**`, `> **Pitfall.**`,
`> **Case study.**`. Every chapter closes with three bullets: Key takeaways, a link to
Exercises, and a link to Open Resources.
