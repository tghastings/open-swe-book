---
name: repo-scorecard
description: Apply the SDLC practices from "Software Engineering: Standing on the Shoulders of Giants" to a codebase — either ADOPT them (write TDD, BDD, security, CI and stewardship rules into the project's CLAUDE.md, for a new or existing project) or SCORE the repo against them (letter grade per area with triple-verified, actionable findings). Use when asked to score, grade, audit, or review a repo's engineering practices, or to set up / bootstrap a project with the book's principles.
---

# Repository scorecard

Two modes. Most projects want both, in this order.

| Mode | When | Section |
|---|---|---|
| **Adopt** | Starting a project, or bringing an existing one under the book's practices. Writes the principles into `CLAUDE.md` so every future session follows them. | [Mode A](#mode-a--adopt-the-principles) |
| **Score** | Auditing what a repo actually does. Letter grade per SDLC area with verified findings. | [Mode B](#mode-b--score-the-repository) |

Adopt sets the standard; score measures against it. Running adopt first and score a sprint
later gives the owner a before/after they can point at.

---

## Mode A — Adopt the principles

Install the book's SDLC practices into a project's agent-instructions file, so the rules
are in context for every future session rather than living in a book nobody re-reads.

```bash
python3 <skill-dir>/adopt-principles.py /path/to/project     # merge into CLAUDE.md
python3 <skill-dir>/adopt-principles.py . --agents           # AGENTS.md instead
python3 <skill-dir>/adopt-principles.py . --dry-run          # report, write nothing
python3 <skill-dir>/adopt-principles.py . --print            # stdout only
```

**What it writes.** A tailored block covering every part of the lifecycle: requirements and
acceptance criteria, BDD scenarios, TDD (red-green-refactor, *never trust a test you have
never seen fail*, oracle choice, failure paths), design and ADRs, commit and review
practice, static checking, security, delivery and DORA, metrics without gaming,
maintenance and stewardship, working with AI assistance, and a definition of done. Each
rule cites the chapter that explains it.

**It is tailored, not boilerplate.** The script reuses `repo-census.py`'s detection to fill
in the real test and lint commands for the stack, and to name the practices *not yet in
place* so the block reads as a backlog rather than a fiction. A new empty directory gets
different opening advice than a mature codebase.

**It never clobbers.** The block sits between `<!-- BEGIN swebook-principles -->` markers.
Re-running replaces only what is between them; anything the owner writes outside survives.
An existing `CLAUDE.md` with no markers gets the block appended, never overwritten.

**After running it**, tell the owner three things: which file changed, that their own
content was preserved, and that re-running refreshes the block as the project matures.
Offer to tailor further — a project with no CI yet may want the delivery rules trimmed to
what it can actually honor this month, since rules a team cannot follow teach them to
ignore the file.

---

## Mode B — Score the repository

Grade a repo against the nine SDLC areas the book teaches, and hand back a report the
owner can act on this week: a letter grade per area, an overall grade, and findings that
each name a concrete change and cite the chapter that teaches it.

The audience is students running a course team project and practitioners auditing their
own work. Both deserve the same thing: **specific, verified, teachable feedback** — not a
generic DevOps maturity checklist.

Read [`rubric.md`](rubric.md) for the per-area criteria, weights, grade bands, and
anti-inflation rules. Read it before grading, not after.

## Two failure modes to design against

An agent turned loose on a repo fails in two predictable directions. Both produce a
report the owner stops trusting after the first wrong line.

1. **Hallucinated absence.** "No tests found" when the tests live in `spec/`. "No CI" when
   there is a `.gitlab-ci.yml`. Never claim something is missing without running a search
   that would have found it, and showing that search.
2. **Checklist deflation.** Grading a two-sprint student project against a FAANG
   production system — dinging it for no SBOM, no service mesh, no chaos testing. Grade
   against the **profile's** expectations (see `rubric.md`), not an imagined ideal.

The triple-check in Step 3 exists to catch both. It is the skill, not overhead.

## The nine areas

One per SDLC-covering part of the book, so every grade points at something to go read.

| # | Area | Book part | Chapters |
|---|---|---|---|
| 1 | Process & Teamwork | Getting Started · Practice | 1–2, App. A |
| 2 | Requirements | What to Build | 3–5 |
| 3 | Design & Architecture | Design and Architecture | 6–7 |
| 4 | Version Control | Version Control | 8 |
| 5 | Software Quality | Software Quality | 9–10 |
| 6 | Security | Security | 11 |
| 7 | Metrics | Metrics | 12 |
| 8 | AI-Assisted Practice | The AI Shift | 13 |
| 9 | Delivery & Evolution | Delivery and Evolution | 14–15 |

## Workflow

### Step 0 — Pick the profile and set the goal

Ask which profile applies if it is not obvious from context (a course repo with a team
and sprints → `student`; anything else → `practitioner`). The profile sets the weights
and the expectation bar in `rubric.md`.

Then run `/goal` so the standard survives all three verification passes. If `/goal` is
unavailable, paste the same text as the first line of your notes.

> **Goal.** Score <repo> against the book's nine SDLC areas using the <profile> profile.
> Every finding must cite a real path or command output I have actually run, name one
> concrete change, and reference the book section that teaches it. Verify absence by
> searching before claiming it. Grade against the <profile> bar, not an ideal system.
> Drop any finding that fails refutation. Read-only: change nothing in the repo.

### Step 1 — Census

```bash
python3 <skill-dir>/repo-census.py /path/to/repo      # --json for machine-readable
```

`<skill-dir>` is the directory this file lives in — `.claude/skills/repo-scorecard/`
under whichever project installed the skill. Stdlib only, offline, read-only.

It reports languages, tracked-file counts, test files, CI, dependency managers and
lockfiles, per-area tooling signals, high-confidence secret hits, and commit-history
statistics (conventional-commit rate, author spread, how much of the history landed on
its busiest day).

It reads file names, CI definitions, and git history. Three rules for reading its output:

- It prefers `git ls-files`, so build output never inflates the counts. A non-git
  directory falls back to a filtered walk — and "not a git repository" is itself the
  single largest finding you will write that day.
- **"nothing matched" is a prompt to go look, never a finding.** It means the lookup
  tables matched nothing, not that the practice is absent. Tools get invoked from
  Makefiles, `package.json` scripts, pre-commit hooks, and shell scripts that this scan
  does not open. Confirm by reading before you grade — the census reports facts about its
  own search, and turning that into a claim about the repo is the hallucinated-absence
  failure this skill exists to prevent.
- **`— CI steps that cannot fail the build —` is high-value.** A scanner or test suite
  behind `continue-on-error: true`, `|| true`, or `fail: false` is configured but
  advisory. That is a genuinely different state from both "present" and "absent", and it
  is usually invisible to the owner — the badge is green. Grade it as *configured but not
  gating* (see `rubric.md`), and quote the file and line.

### Step 2 — Read the repo

The census tells you what exists; only reading tells you whether it is any good. At
minimum, before grading:

- `README.md` — can a new contributor run this? That answers half of area 9.
- The CI config, end to end — what actually gates a merge, versus what merely runs.
- Two or three real test files — are these assertions, or `assert True` with a coverage
  number attached? Ch. 10's "never trust a test you have never seen fail" is the standard.
- `git log --oneline -30` and one real diff — commit hygiene and change size.
- The largest source file, and the dependency manifest.

For team repos, also skim open/closed issues and a merged PR if the host CLI is available
(`gh pr list`, `gh issue list`). Skip silently if it is not; never fabricate that history.

### Step 3 — Triple-check every finding (mandatory)

A finding ships only if it survives all three passes.

**Pass 1 — Locate.** Every claim is backed by output you have actually seen.
- Claiming something *exists*: cite `path:line` or the command output.
- Claiming something is *missing*: run the search that would have found it and show it.
  `rg --files | rg -i 'test|spec'`, `git ls-files | rg -i 'ci|workflow'`,
  `rg -i 'lint|format' package.json Makefile`. No search, no finding.

**Pass 2 — Refute.** Argue against your own finding; default to dropping it. Drop if:
- the practice exists somewhere else, under another name, or via a framework default
  (Rails/Django/Spring conventions, `go test` needing no config, `cargo fmt` built in);
- it is out of scope for this repo's kind (a CLI needs no k8s manifests; a solo script
  needs no CODEOWNERS);
- it exceeds the profile bar in `rubric.md`;
- the "fix" is cargo-culting a tool rather than solving a problem the repo actually has.

**Pass 3 — Actionability.** Name the edit and the teacher. "Testing is weak" fails.
"`auth.py` has no test for the expired-token path — add a case asserting 401, and see
§10.2 on choosing oracles" passes. Every finding cites a book section; if you cannot find
one, the finding probably belongs to a different area, or does not belong in the book's
frame at all.

Keep the casualties in a **Considered and dropped** list with one-line reasons. It shows
the owner their repo was read, not pattern-matched, and it stops the same false positive
resurfacing on the next run.

### Step 4 — Grade

Score each area per `rubric.md`, using **surviving findings only** — a claim killed in
Pass 2 must not depress a grade. Mark genuinely inapplicable areas `N/A` and redistribute
their weight proportionally. Compute the weighted total, map to a letter, then run the
anti-inflation and anti-deflation checks in `rubric.md`.

Assign every finding to **exactly one** area — see *No double jeopardy* in `rubric.md`
for the tie-break order. Other areas may cite it ("see F1") without deducting.

### Step 5 — Write the scorecard

Produce **both** artifacts, **outside the graded repo** unless the owner asks otherwise —
a review artifact should never show up in their `git status`. Default to
`../<repo-name>-scorecard.{json,html,md}`.

**5a. Findings JSON** — the source of truth, written first. The HTML renders from it, and
re-running later lets you diff two reviews.

```jsonc
{
  "repo": "simpli-re",
  "path": "/abs/path",
  "profile": "practitioner",
  "reviewed": "2026-07-26",
  "commit": "2304a3c",
  "branch": "main",
  "overall": { "score": 78, "grade": "C+" },
  // optional: what the score becomes once the top finding is fixed
  "counterfactual": { "score": 84, "grade": "B", "note": "with F1 remediated" },
  "areas": [
    { "n": 1, "name": "Process & Teamwork", "chapters": "1–2, App. A",
      "weight": 5, "grade": "B+", "points": 88, "justification": "one line" }
  ],
  "strengths": ["specific, with a path"],
  "findings": [
    { "id": "F1", "severity": "Critical", "area": "Security",
      "title": "one line, no period",
      "evidence": "markdown: `path:line`, command output",
      "why": "why a reader/owner is underserved",
      "do": "the concrete change",
      "book": "Ch. 11 (secrets), §14.6",
      "effort": "M" }
  ],
  "dropped": [{ "claim": "No ADRs", "reason": "docs/decisions/ holds four" }],
  "verification": { "pass1": "…", "pass2": "…", "pass3": "…", "shipped": 7 }
}
```

`severity` ∈ `Critical | Major | Minor | Nit`. `effort` ∈ `S | M | L`. `points` is the
letter's fixed value from `rubric.md` — the renderer recomputes the weighted total from
`weight` × `points` and **warns if it disagrees with `overall.score`**, which catches
arithmetic slips before the owner sees them.

**5b. Interactive HTML report** — generate, never hand-write:

```bash
python3 <skill-dir>/render-scorecard.py findings.json -o ../<repo>-scorecard.html
```

Self-contained (no network, inline CSS/JS), light/dark aware, print-friendly. Gives the
owner severity/area filters, live search, expand-all, and per-finding **done** checkboxes
that persist in `localStorage` — so the report doubles as the remediation worklist.

**5c. Markdown scorecard** *(optional)* — same content for terminal or PR-comment reading.
Generate with `--markdown` rather than writing it twice.

````markdown
# Scorecard — <repo>
Profile: <student|practitioner> · Reviewed: <date> · Commit: <short sha>
**Overall: <letter> (<score>/100)**

| # | Area | Weight | Grade | One-line justification |
|---|---|---|---|---|
| 1 | Process & Teamwork | 15 | B | … |
| … | | | | |

## Top 3 next actions
1. **<finding id>** — <one line>. (~<effort>)
2. …
3. …

## What's working
Two or three specifics, with paths. Real credit, not padding — an owner who sees their
genuine strengths named will trust the criticism.

## Findings

### F1 · [Major] Software Quality — CI runs tests but does not gate the merge
**Evidence:** `.github/workflows/ci.yml:22` runs `pytest`; no branch protection, and
`continue-on-error: true` on line 24.
**Why it matters:** A red test that cannot block a merge is a notification, not a gate —
the failure reaches main anyway.
**Do this:** Remove `continue-on-error`, then require the check in branch protection.
**Book:** §14.3 (deployment pipeline), §10.1 (what a test is for)
**Effort:** S

## Considered and dropped
- *No ADRs* — `docs/decisions/` holds four; missed on the first pass.
- *No linter* — `ruff` is configured in `pyproject.toml:41`.

## Verification
Pass 1: N claims checked against command output, K dropped as unverifiable.
Pass 2: J dropped on refutation. Pass 3: M reworded for actionability.
<N> findings ship.
````

## Rules

- **Read-only.** Never modify, stage, commit, or push in the graded repo. If the owner
  wants fixes applied, that is a separate request after they have read the scorecard.
- **Never run untrusted code** from the repo to "check if it works" — no `npm install`,
  no `make`, no test suites. Grade by reading. Static tools already installed are fine.
- **Secrets:** if the census flags a live-looking credential, verify it is real and not a
  test fixture or placeholder, then lead the report with it and tell the owner to rotate
  first and scrub history second. Never paste the secret value into the scorecard.
- **Cite, don't assert.** Every grade traces to findings; every finding traces to
  evidence and a book section.
- **Grade the repo, not the person.** "The test suite has no failure-path cases," never
  "the team was careless."
