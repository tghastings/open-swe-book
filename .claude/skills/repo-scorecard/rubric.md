# Rubric — repository scorecard

Nine areas, one per SDLC-covering part of the book. Every criterion traces to something
the book actually teaches, so a grade always points somewhere to go read.

## Weights

| # | Area | student | practitioner |
|---|---|---:|---:|
| 1 | Process & Teamwork | 15 | 5 |
| 2 | Requirements | 15 | 10 |
| 3 | Design & Architecture | 10 | 15 |
| 4 | Version Control | 15 | 10 |
| 5 | Software Quality | 15 | 20 |
| 6 | Security | 10 | 15 |
| 7 | Metrics | 5 | 5 |
| 8 | AI-Assisted Practice | 5 | 5 |
| 9 | Delivery & Evolution | 10 | 15 |
| | **Total** | **100** | **100** |

**student** — a course team project: process, requirements discipline, and commit hygiene
are the learning objectives, so they carry the weight.
**practitioner** — a working codebase: quality, security, and delivery carry it.

## Letter → points

Assign a letter per area, then convert for the weighted total. Fixed values, so two runs
of the same repo agree.

| A | A− | B+ | B | B− | C+ | C | C− | D | F |
|---|---|---|---|---|---|---|---|---|---|
| 95 | 91 | 88 | 85 | 81 | 78 | 75 | 71 | 65 | 50 |

Weighted total → overall grade:

| Score | 93+ | 90–92 | 87–89 | 83–86 | 80–82 | 77–79 | 73–76 | 70–72 | 60–69 | <60 |
|---|---|---|---|---|---|---|---|---|---|---|
| Grade | A | A− | B+ | B | B− | C+ | C | C− | D | F |

## Generic grade anchors

Specialize per area below, but the shape is constant. The distinction that matters is
**configured** versus **enforced and used** — a linter nobody runs is not static checking.

- **A** — practice present, enforced automatically, and visibly used in day-to-day history.
- **B** — present and genuinely used, with one real gap. *This is a good repo.*
- **C** — partially present, or configured but not enforced, or applied inconsistently.
- **D** — token presence: the file exists, the practice does not.
- **F** — absent, and the consequences are visible in the repo.

## No double jeopardy

**One defect, one area. Always.** Many defects legitimately match the criteria of two or
three areas — committed credentials satisfy the F condition for both Security and Version
Control; a god-file matches both Design and Maintenance. Scoring the same defect twice
punishes the repo twice for one mistake and quietly makes the weighted total meaningless.

Assign each finding to exactly one area using the first rule that applies:

1. **Consequence over mechanism.** Grade where the *damage* lands, not where the mistake
   was made. Committed credentials → **Security** (the exposure is the harm), not Version
   Control (which is merely how they got there).
2. **Most specific area wins.** If one area names the defect explicitly in its criteria and
   another only implies it, the explicit one takes it. A missing SBOM is Security, not
   Delivery, even though it ships in the pipeline.
3. **Where the fix lives.** If still tied, assign it to the area whose practice the owner
   must change. A flaky test that blocks deploys is Software Quality — that is where the
   repair happens.
4. **Highest weight breaks the final tie** — so the score reflects the defect at its true
   cost under the active profile.

The other areas get **no deduction** for that defect, but **may reference it** in their
justification line ("see F1") so the report still reads coherently. Note the call in
*Considered and dropped* when it was genuinely close — it shows the choice was made rather
than missed.

## Severity ladder

- **Critical** — live credential committed; no version control; a vulnerability reachable
  from untrusted input; the build cannot be reproduced from a clean clone.
- **Major** — an area's core practice is missing or unenforced.
- **Minor** — a gap or inconsistency inside a practice that otherwise works.
- **Nit** — polish. Cap at two per scorecard; more than that buries the real findings.

---

## 1 · Process & Teamwork — Ch. 1–2, Appendix A

**Expects:** work is visible and sliced, iterations have a cadence, and the team has
written agreements. The book uses Scrum's 2020 vocabulary — **accountabilities**, not
"roles" — and treats process as a means, not a ritual.

**Look for:** an issue tracker in real use (not three stale cards); work broken into
sprint-sized slices; a definition of done; a team charter or working agreements; evidence
of iteration (tags, milestones, sprint branches, retro notes); commit history spread
across the term rather than compressed into the last two days.

- **A** — cadence is visible in the history; work is tracked and sliced; a written
  definition of done exists and the merged work meets it.
- **B** — tracked and iterative, but the definition of done is implicit or the cadence is
  uneven.
- **C** — some tracking, little slicing; iteration is asserted but not visible in history.
- **D** — a tracker exists with token use; history shows one or two big drops.
- **F** — no visible process; the whole project lands in a single sitting.

> Practitioner profile: a solo repo needs no charter. Grade cadence, issue hygiene, and
> whether the work is sliced. Mark `N/A` if there is genuinely no team and no tracker
> expectation.

## 2 · Requirements — Ch. 3–5

**Expects:** stated needs, in the user's terms, with testable acceptance criteria — user
stories (Connextra), INVEST, scenarios, use cases. The book's throughline is that
requirements are traceable to something you can check.

**Look for:** stories or requirements written down anywhere (issues, `docs/`, a backlog);
acceptance criteria attached to them; `.feature` files or scenario-style test names;
traceability from a requirement to the code and test that satisfy it; a README that says
what the software is *for* and who uses it.

- **A** — requirements are written, testable, and traceable into tests or issues.
- **B** — stories with acceptance criteria exist; traceability is partial.
- **C** — requirements exist as prose or a title-only backlog; not testable as written.
- **D** — only a README feature list; no acceptance criteria anywhere.
- **F** — nothing states what the system is supposed to do.

## 3 · Design & Architecture — Ch. 6–7

**Expects:** deliberate structure — modularity, low coupling, high cohesion — and
decisions recorded rather than remembered. Ch. 7 catalogs the patterns; §7.5.4 covers REST.

**Look for:** a directory structure that reveals the architecture; modules with clear
responsibilities; ADRs (`docs/adr/`, `docs/decisions/`); an architecture doc or diagram;
consistent application of whatever pattern is in play; absence of god-files. Read the
largest source file — its size and mixed responsibilities are the fastest architecture
signal in any repo.

- **A** — structure is legible, boundaries hold, and significant decisions are recorded
  with their trade-offs.
- **B** — clean structure, decisions undocumented.
- **C** — structure is inconsistent; boundaries leak; one or two files carry too much.
- **D** — organization is incidental; a god-file dominates.
- **F** — no discernible structure.

## 4 · Version Control — Ch. 8

**Expects:** small, well-described commits; a branching model the team actually follows;
review before merge; nothing in history that should not be there.

**Look for:** commit-message quality (the census reports conventional-commit rate and
very-short-message rate); commit size; a branching model (Gitflow or GitHub Flow) visible
in branch and merge structure; merged PRs with review; a `.gitignore` that keeps build
output and secrets out; no committed `.env`, keys, or vendored `node_modules`.

- **A** — small focused commits, descriptive messages, review before merge, clean history.
- **B** — good hygiene with a soft spot — terse messages, or occasional oversized commits.
- **C** — messages are mostly uninformative ("fix", "update"), or commits bundle unrelated
  changes; review is inconsistent.
- **D** — a handful of huge commits; no branching; no review.
- **F** — not a git repository, or history is unusable (bulk binaries, no meaningful commits).

> Committed credentials score under **Security**, not here. What belongs to this area is
> the separable practice gap — e.g. a `.gitignore` rule added without the follow-up
> `git rm --cached` — and that is a Minor, not an F.

> The census's `busiest_day_pct` is the tell for student repos: a history where most
> commits land on one day did not practice incremental integration, whatever the total says.

## 5 · Software Quality — Ch. 9–10

**Expects:** both halves. **Static** (Ch. 9): type checking, linting, formatting, human
review. **Dynamic** (Ch. 10): tests at more than one level, chosen oracles, honest
coverage. The standard the book sets is *never trust a test you have never seen fail*.

**Look for:** linter/formatter/type-checker configs *and* CI steps that run them; tests
that exist, run in CI, and gate the merge; more than one test level; assertions that could
actually fail (read two or three); failure-path and edge-case coverage, not just happy
path; coverage measured but not worshipped; no `continue-on-error` or `|| true` quietly
neutering the gate.

- **A** — static checks and tests both run in CI and block merges; tests cover failure
  paths; assertions are meaningful.
- **B** — solid tests and checks, with a real gap: one level missing, or checks run
  without gating.
- **C** — tests exist but are shallow or happy-path only; linting configured but not
  enforced.
- **D** — a handful of token tests; no static analysis.
- **F** — no tests, or tests that cannot fail.

> Read the assertions. A suite of `assert response is not None` with 80% coverage is a
> C, not an A — coverage measures execution, not verification.

## 6 · Security — Ch. 11

**Expects:** proportional practice — secrets kept out of the repo, dependencies watched,
the OWASP Top 10 respected at the boundaries, and supply-chain awareness (Log4Shell,
xz-utils are the book's cautionary cases).

**Look for:** no committed secrets (census flags high-confidence hits); a `.env.example`
alongside real config loaded from the environment; pinned dependencies with a lockfile;
Dependabot/Renovate; SCA or SAST in CI; input validation and parameterized queries at the
boundaries; `SECURITY.md` for anything public; SBOM or signing for anything distributed.

- **A** — secrets externalized, dependencies pinned and monitored, scanning in CI **that
  gates the merge**, and boundary handling is correct where you read it.
- **B** — good hygiene; automated scanning missing, or present but advisory only
  (`|| true`, `continue-on-error`) so a finding never blocks anything.
- **C** — no committed secrets, but dependencies unpinned or unmonitored, no scanning.
- **D** — weak boundary handling, or dependencies badly stale.
- **F** — a live credential in the repo, or an obvious injection path from untrusted input.

> Committed credentials belong **here**, not in Version Control — consequence over
> mechanism (see *No double jeopardy*). Area 4 may cite the finding without deducting.

> A committed live credential is **Critical** and leads the report: rotate first, scrub
> history second. Verify it is not a placeholder or fixture before you say a word about it.

## 7 · Metrics — Ch. 12

**Expects:** measurement tied to a question (GQM, per Basili), not a dashboard for its own
sake — and awareness that a metric adopted as a target stops measuring anything.

**Look for:** anything measured on purpose — coverage tracked over time, defect or bug
labels used consistently, CI duration watched, complexity or code-health checks, DORA
figures if delivery is automated. For student repos, evidence of measurement in reports
or retros counts.

- **A** — a small number of metrics tied to explicit questions, tracked over time, and
  visibly acted on.
- **B** — metrics collected and referenced, without a stated question.
- **C** — one incidental metric (a coverage badge) with no evident use.
- **D** — metrics gamed or vanity-only.
- **F** — nothing measured.

> Low weight everywhere (5). Small repos legitimately measure little — do not manufacture
> a Major finding here to fill the section.

## 8 · AI-Assisted Practice — Ch. 13

**Expects:** if AI tooling is used, it is used deliberately — durable project context
(`CLAUDE.md`, `AGENTS.md`), human review of generated code, and awareness that generation
shifts effort to verification rather than removing it.

**Look for:** agent instruction files and whether they are current; whether AI-assisted
changes went through the same review and tests as everything else; oversized unreviewed
commits that read as bulk generation; any attribution policy the course or org requires.

- **A** — durable context files, maintained; generated code reviewed and tested like any
  other; the verification burden is visibly owned.
- **B** — AI used with review, no durable context captured.
- **C** — signs of generated code merged with light review.
- **D** — large unreviewed generated drops.
- **F** — generated code merged unreviewed and untested, with defects visible.

> Mark `N/A` if there is no evidence of AI assistance. Absence of AI tooling is **not** a
> deduction — the book does not require its use.

## 9 · Delivery & Evolution — Ch. 14–15

**Expects:** a repeatable path from commit to running software (Ch. 14), and deliberate
care of the codebase over time (Ch. 15) — technical debt tracked, refactoring ongoing,
**repository stewardship**: leave it better than you found it.

**Look for:** CI that builds and tests on every push; automated or documented deployment;
config and secrets from the environment (twelve-factor); a `Dockerfile`/`compose.yml` or
equivalent reproducible setup; a README that gets a newcomer running; dependencies
maintained rather than frozen in 2021; refactoring commits in the history; debt tracked
somewhere; docs that match the current code. DORA's **five** metrics are the frame for
delivery health — throughput plus instability.

- **A** — one command (or one documented sequence) from clone to running; CI/CD automated;
  config externalized; history shows continuous care.
- **B** — CI solid, deployment manual but documented; some drift between docs and code.
- **C** — CI builds only; setup requires tribal knowledge; visible neglect (stale deps,
  dead code, outdated README).
- **D** — no CI; setup is guesswork.
- **F** — the project cannot be built or run from a clean clone.

> The single best test of this area: could *you*, from the README alone, get it running?
> Say so in the scorecard either way — it is the most actionable line in the report.

---

## Anti-inflation

1. **Start every area at B (85).** Move up only with evidence the practice is *enforced
   and used*; move down only with a Pass-1-verified finding.
2. **No A in an area with a surviving Major finding.** No overall A with any surviving
   Critical.
3. **Configuration is not practice.** A linter config with no CI step, a test suite that
   never gates, a `CLAUDE.md` last touched at commit two — each caps its area at C.
4. **Distribution check.** If six or more areas land A−/A, you are grading the presence of
   files. Re-run Pass 2 harder before publishing.

## Anti-deflation

1. **Absence requires a shown search.** No search output in Pass 1, no finding — and
   therefore no deduction. A census line reading "nothing matched" is not a search
   result about the repo; it is a statement about the census's own lookup tables. Tools
   invoked from CI steps, Makefiles, or hooks are routinely missed. Go look.
2. **Grade against the profile bar.** A student project is not a production service. Never
   deduct for enterprise ceremony the profile does not ask for (SBOM, CODEOWNERS, service
   mesh, chaos testing).
3. **Small and well-made is an A.** A 400-line CLI with real tests, clean commits, and a
   working README earns it. Size is not maturity.
4. **Floor check.** If every area lands C or below, verify the profile is right and the
   census read the correct directory before publishing.

## N/A areas

Mark an area `N/A` only when it is genuinely inapplicable — no AI assistance (area 8), a
solo repo with no team process (area 1). Redistribute its weight proportionally across the
rest. **At most two `N/A` areas**; needing a third means the wrong profile, or that this
repo is not what the tool is for. Never use `N/A` to avoid a hard call.
