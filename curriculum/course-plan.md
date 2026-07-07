# Course Plans

Two ready‑to‑use schedules for a junior/senior software‑engineering course built on this
book — **Variant A**, a 15‑week milestone track, and **Variant B**, a 16‑week semester run
on two‑week sprints. Both run **two parallel tracks** (as the ACM/IEEE guidelines
recommend[^1]):

- **Concepts track** — the thirteen chapters, one theme at a time.
- **Project track** — a real team project (Appendix A), started early and iterated.

The two tracks are **tightly coupled at the start** (weeks 1–4, while teams form and
scope their projects) and **loosely coupled afterward**, so each can move at its own
pace.

## Variant A: 15-week milestone track

| Week | Concepts (chapter) | Project milestone | Key open resources |
|------|--------------------|-------------------|--------------------|
| 1 | Ch. 1 — Introduction | Form teams; brainstorm ideas | ACM Code of Ethics; Therac‑25 |
| 2 | Ch. 2 — Processes (Scrum/XP); Ch. 8 — Version Control (Git) | Pick a process; set up repo & board with a protected `main` | Scrum Guide; Pro Git |
| 3 | Ch. 3 — User Requirements | **Project Proposal** (App. A.2) | ESaaS ch.7; Volere; INVEST |
| 4 | Ch. 4 — Requirements Analysis | Backlog + estimates (Planning Poker) | Planning Poker; MoSCoW; Kano |
| 5 | Ch. 5 — Use Cases | Use cases / stories for iteration 1 | Cockburn use cases |
| 6 | Ch. 6 — Design & Architecture | Architecture sketch; class diagram | MIT 6.031; 4+1 views |
| 7 | Ch. 7 — Architectural Patterns | **Status Report 1** (skeletal system) | Fowler PoEAA; MS patterns |
| 8 | *Midterm / catch‑up* | Sprint review + retrospective | — |
| 9 | Ch. 9 — Static Checking; CI pipelines (§14.2) | Set up CI, linters, code review | Google eng‑practices; Fagan |
| 10 | Ch. 10 — Testing (coverage) | Test plan; coverage targets | MIT 6.031 testing; Ammann/Offutt |
| 11 | Ch. 10 — Testing (MC/DC, combinatorial) | **Status Report 2** (viable system) | NIST combinatorial |
| 12 | Ch. 11 — Software Security (OWASP Top 10, SAST/DAST/SCA, supply chain) | Threat‑model the project; add dependency scanning | OWASP Top 10; PortSwigger; OpenSSF Scorecard |
| 13 | Ch. 12 — Metrics (quality, defects, statistics); DORA (§14.7) | Defect tracking; measure & analyze project data | OpenIntro Stats; DORA |
| 14 | Ch. 13 — SE in the Age of AI; Ch. 14 — CD, evolution + review | **Comprehensive Final Report** (A.5) | METR study; o16g manifesto; SEC 34‑70694 |
| 15 | Final presentations / demos | Ship & retrospective | — |

> **Flexibility on Chapter 11 (Software Security).** Week 12 gives security its own
> session, but the material also pairs naturally with the CI and static-analysis week
> (week 9) — teach it wherever your emphasis lies. Either way, the project's "static
> analysis + supply-chain security" sprint (Appendix A) is where students apply the OWASP
> Top 10 and the dependency-vetting controls to their own code. If you are pressed for
> time, Chapter 12's statistics half (§12.6–§12.9) is the readiest thing to move to
> optional reading, following its own "two paths" note.

## Variant B: 16-week semester on two-week sprints

For courses that run the project on a two-week sprint cadence with the **dual-hat
cross-team customer model** — each team pitches an idea that *another* team builds, and
serves as customer for its own pitch (see
[Running the Project on Two-Week Sprints](../chapters/appendix-a-team-project/two-week-sprints.md)).
Concepts and project interleave: four onboarding deliverables (Sprint 0‑0 … 0‑3), then four
two-week build sprints, each ending in a **Demo Day** and a team/customer review, with a
progressive engineering-hardening arc (CI → CD → lint/dependency scans → debt paydown).

| Week | Concepts (chapter) | Project / sprint deliverable |
|------|--------------------|------------------------------|
| 1 | Ch. 1 — Introduction; SaaS & the cloud (§14.1) | Think about project ideas |
| 2 | Ch. 3 — User Requirements; Shape Up (§2.8, §4.2.4) | — |
| 3 | Ch. 2 — Processes & types of agile; Ch. 8 — Version Control (Git) | Teams form; **Sprint 0‑0**: idea pitches; set up repo with protected `main` |
| 4 | Ch. 6 — Design principles | **Sprint 0‑1**: pitch swap + proposal with customer |
| 5 | Ch. 7 — Architectures + REST (§7.5.4); idea presentations | **Sprint 0‑2**: user stories + lo‑fi UI/storyboards (§§3.4–3.5) |
| 6 | Ch. 10 — Testing; CI pipelines (§14.2); DORA (§14.7) | **Sprint 0‑3**: initial view, deployed |
| 7 | Demo Day; sprints & iterations (§2.2) | **Sprint 1** begins; team review #0 |
| 8 | *Test 1* | — |
| 9 | Continuous deployment (§14.3: Knight Capital, CrowdStrike) | Sprint 1 due → Demo Day; **Sprint 2**; review #1 |
| 10 | *Spring break* | — |
| 11 | Ch. 9 — Static checking; risk | Sprint 2 continues |
| 12 | Ch. 11 — Software Security (OWASP Top 10, SAST/DAST/SCA, supply chain); security pipelines (§14.6) | Sprint 2 due → Demo Day; **Sprint 3**; review #2 |
| 13 | Legacy code & refactoring (§14.8); Ch. 13 AI readings | Sprint 3 continues |
| 14 | Work days; Ch. 12 metrics in practice | Sprint 3 due → Demo Day; **Sprint 4**; review #3 |
| 15 | *Test 2* | Sprint 4 due |
| 16 | Final presentations | Individual write‑ups; review #4 |

Chapters 4–5 (estimation, use cases) are woven into the sprint work as read‑before
material (see the sprint table in the appendix page) rather than given lecture weeks.
Assessment shifts accordingly: sprint reports and team reviews replace the two status
reports, and two in‑term tests replace the midterm/final split.

## Assessment (suggested weights)

| Component | Weight |
|-----------|-------:|
| Team project (proposal, 2 status reports, final report, demo) | 45% |
| Individual exercises / problem sets (chapter `exercises.md`) | 20% |
| Midterm (concepts, weeks 1–7) | 15% |
| Final exam (concepts, whole book) | 20% |

## Learning outcomes

By the end, a student can:

1. Choose and run an appropriate **process** (Scrum/XP/hybrid) for a team project.
2. **Elicit, write, prioritize, and estimate** requirements as user stories/use cases.
3. **Design a modular architecture** and describe it with UML and 4+1 views.
4. Apply the right **architectural patterns** to a problem.
5. **Review and statically check** code and architecture for defects.
6. Design a **test suite** that meets defined coverage criteria.
7. Identify common **vulnerabilities** (the OWASP Top 10) and vet open‑source
   dependencies for **software‑supply‑chain** risk.
8. Define and interpret **quality metrics** using sound statistics.
9. Work effectively on a **software team** and communicate progress.

## Adapting the plan

- **10‑week quarter:** merge weeks 4↔5, fold Chapter 11 (security) into week 9's
  CI/static‑analysis session, and teach Chapter 12 on its minimum path (§12.1–§12.5);
  move MC/DC to optional reading. (See the one‑quarter path on the front page.)
- **Bootcamp / self‑study:** follow the four anchor courses in
  [`open-resources-map.md`](open-resources-map.md) alongside the chapters; do the
  project solo or in a pair.
- **No team project:** keep the concepts track; use the checkpoints in
  [Appendix A's project exercises](../chapters/appendix-a-team-project/exercises.md) as
  larger individual assignments.

[^1]: ACM/IEEE‑CS Joint Task Force on Computing Curricula, *Software Engineering 2014:
Curriculum Guidelines for Undergraduate Degree Programs in Software Engineering*
(SE2014), which recommends a substantial team project alongside the concepts.
[acm.org/education/curricula-recommendations](https://www.acm.org/education/curricula-recommendations).
