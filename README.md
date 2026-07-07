# Software Engineering: Standing on the Shoulders of Giants

*First Edition, July 2026.*

📖 **Read the book online at [www.swebook.org](https://www.swebook.org).**

This book is freely available and openly licensed, providing instruction in the principles and best practices of
modern software engineering: how software is built in industry using
agile methods, how to discover and analyze requirements, how to design and architect
modular systems, how to check and test code, and how to measure quality with metrics.

The book is structured into fourteen chapters and a team project appendix, following the topic
progression of the ACM/IEEE software‑engineering curriculum guidelines (SE2014/SEEK).[^1]
Each chapter contains original explanatory prose rather than material copied from other textbooks
and is accompanied by a curated map of free or openly accessible resources — MOOCs, university
courseware, primary specifications, and papers — with licenses noted where known. The material is designed to support a complete
software‑engineering course.

> **An independent open educational resource.** This is a complete, standalone book.
> Except for clearly attributed quotations and linked external resources, its explanatory
> prose, examples, diagrams, and exercises are original, and the book is released under
> Creative Commons. See [`curriculum/open-resources-map.md`](curriculum/open-resources-map.md)
> for the mapping from each chapter to complementary open materials. The prose was
> drafted with AI assistance under the author's direction, review, and fact-checking —
> see [How this book was made](#how-this-book-was-made-ai-assistance) below.

---

## Why this book exists

Most significant software is developed by teams, under evolving requirements, and with
inevitable defects, at a scale that exceeds the capacity of any individual to fully comprehend. A typical programming course teaches students to write individual
functions, whereas a software engineering course instructs students in building and evolving
complete systems collaboratively. The discipline
emphasizes enduring principles over proficiency in any single programming language:

1. **Software is complex** → we manage complexity with design and architecture.
2. **Requirements change** → we use iterative, agile methods to adapt.
3. **Defects are inevitable** → we use reviews, static checking, and testing to catch them.
4. **Teams need coordination** → we use processes, and a healthy balance of structure and flexibility.

These four foundational concepts are integrated throughout every chapter.

## How the book is organized

The chapters are organized into thematic arcs:

| Arc | Chapters | Question it answers |
|-----|----------|---------------------|
| **Getting started** | 1–2 | What is software engineering, and what process do we use? |
| **What to build** | 3–5 | How do we discover, analyze, and specify requirements? |
| **Design & architecture** | 6–7 | How do we structure a system to tame complexity? |
| **Version control** | 8 | How do teams manage, review, and collaborate on a shared codebase? |
| **Software quality** | 9–10 | How do we check and test that the system works? |
| **Security** | 11 | How do we build software that resists attack, from the code to the supply chain? |
| **Metrics** | 12 | How do we measure quality and track progress? |
| **The AI shift** | 13 | How is AI reshaping every stage — and what stays the same? |
| **Delivery** | 14 | How does code get from a merged branch to running safely in production? |
| **Practice** | Appendix A | How do we run a real team project alongside the concepts? |

## Suggested paths through the book

- **One-semester course (14–16 weeks).** Read all fourteen chapters in order, one to two
  weeks each, with the Appendix A team project running in parallel from week 2. Two
  ready-made week-by-week plans (a milestone track and a two-week-sprint track) are in
  [`curriculum/course-plan.md`](curriculum/course-plan.md).
- **One-quarter course (~10 weeks).** Keep the spine and compress: Chapters 1–2
  (week 1), 3–4 (weeks 2–3, folding Chapter 5's use-case notation into the requirements
  work), 6–8 (weeks 4–5, design, patterns, and version control), 9–10 (weeks 6–7, checking
  and testing), 11–12 (week 8, security and metrics), and 14 (week 9, delivery), with
  Chapter 13 (AI) read alongside each topic through its per-stage sections (§13.2). Run a
  scoped-down project: proposal, two sprints, final demo.
- For self-study, chapters should be read sequentially. Each chapter concludes with key takeaways, exercises, and
  free resources for further study. Alternatively, readers may use the arc table above to focus on a specific
  goal, such as Chapters 9–10 for checking and testing or Chapter 14 for CI/CD. Chapters cross-reference the
  earlier ideas they depend on.

## Code examples in six languages

Every code example in the book is provided in **Python, Java, JavaScript, Go, Ruby,
and TypeScript**, plus a language-agnostic **Generic** tab written in pseudocode, behind
language tabs — pick your language once and the whole site follows
(or open any page with [`?lang=go`](?lang=go) to pre-select one). Each snippet also lives in
[`code/`](code/) as a runnable file with a test, executed by continuous integration on
every change.

The book is also available as an **EPUB and a PDF**, one edition per language plus a
**Generic (pseudocode)** edition — identical prose, published with each tagged release:

EPUB:
[Generic](https://github.com/tghastings/open-swe-book/releases/latest/download/swebook-generic.epub) ·
[Python](https://github.com/tghastings/open-swe-book/releases/latest/download/swebook-python.epub) ·
[Java](https://github.com/tghastings/open-swe-book/releases/latest/download/swebook-java.epub) ·
[JavaScript](https://github.com/tghastings/open-swe-book/releases/latest/download/swebook-javascript.epub) ·
[Go](https://github.com/tghastings/open-swe-book/releases/latest/download/swebook-go.epub) ·
[Ruby](https://github.com/tghastings/open-swe-book/releases/latest/download/swebook-ruby.epub) ·
[TypeScript](https://github.com/tghastings/open-swe-book/releases/latest/download/swebook-typescript.epub)
&nbsp;&nbsp;PDF:
[Generic](https://github.com/tghastings/open-swe-book/releases/latest/download/swebook-generic.pdf) ·
[Python](https://github.com/tghastings/open-swe-book/releases/latest/download/swebook-python.pdf) ·
[Java](https://github.com/tghastings/open-swe-book/releases/latest/download/swebook-java.pdf) ·
[JavaScript](https://github.com/tghastings/open-swe-book/releases/latest/download/swebook-javascript.pdf) ·
[Go](https://github.com/tghastings/open-swe-book/releases/latest/download/swebook-go.pdf) ·
[Ruby](https://github.com/tghastings/open-swe-book/releases/latest/download/swebook-ruby.pdf) ·
[TypeScript](https://github.com/tghastings/open-swe-book/releases/latest/download/swebook-typescript.pdf)

All editions, including past versions, are on the
[releases page](https://github.com/tghastings/open-swe-book/releases).

## Table of contents

The sidebar provides a complete, linked table of contents, including chapters and sections. Alternatively, readers may begin with any chapter of interest:

1. [Introduction](chapters/01-introduction/) — what SE is, the requirements challenge, complexity, defects, the iron triangle, professional ethics.
2. [Software Development Processes](chapters/02-software-development-processes/) — plan vs. grow, Scrum, XP, waterfall/V, spiral & risk.
3. [User Requirements](chapters/03-user-requirements/) — eliciting needs, user stories, features, scenarios, goals, security attack trees.
4. [Requirements Analysis](chapters/04-requirements-analysis/) — estimation, planning poker, MoSCoW, Kano, value/cost/risk, COCOMO.
5. [Use Cases](chapters/05-use-cases/) — actors & goals, basic and alternative flows, use‑case diagrams and relationships.
6. [Design and Architecture](chapters/06-design-and-architecture/) — modularity, coupling & cohesion, UML class diagrams, 4+1 views.
7. [Architectural Patterns](chapters/07-architectural-patterns/) — layering, shared‑data, observer, pub‑sub, MVC, dataflow, client‑server, broker, REST, product lines.
8. [Version Control with Git](chapters/08-version-control-git/) — the commit graph, branching/merging/rebase, remotes and pull requests, merge conflicts, team workflows, and Markdown for READMEs and documentation.
9. [Static Checking](chapters/09-static-checking/) — architecture reviews, inspections, code reviews, automated static analysis.
10. [Testing](chapters/10-testing/) — levels of testing, control‑flow & MC/DC coverage, black‑box coverage, combinatorial testing.
11. [Software Security](chapters/11-software-security/) — the CIA triad and defense in depth, the OWASP Top 10:2025, SAST/DAST/SCA and AI‑assisted security testing, the open‑source supply chain (Log4Shell, xz‑utils, and continuous verification of components), and building security in.
12. [Quality Metrics](chapters/12-quality-metrics/) — meaningful metrics, defect measures, boxplots/histograms, statistics, confidence intervals, regression.
13. [Software Engineering in the Age of AI](chapters/13-ai-across-the-lifecycle/) — how AI reshapes every lifecycle stage, the productivity/quality/security evidence, and the o16g Outcome Engineering manifesto.
14. [Delivery: CI/CD, DevOps, and Evolution](chapters/14-delivery/) — SaaS and the cloud, CI pipelines, continuous deployment (the Knight Capital and CrowdStrike case studies), security pipelines, DORA metrics, legacy code and technical debt.

- [Appendix A: The Team Project](chapters/appendix-a-team-project/) — proposal, sprint and status reports, team reviews, and final-report templates.

## How to use this repository

- Learners are advised to read the chapters sequentially. Each chapter concludes with Key Takeaways, Exercises,
  and *Open resources* pointing to free courses and readings for deeper study.
- Instructors will find that the chapters align with a 14–16 week semester. Two ready-made plans
  (a milestone track and a two-week-sprint track) live in
  [`curriculum/course-plan.md`](curriculum/course-plan.md). Run the team project from
  Appendix A on a parallel track. Reusable document templates (idea pitch, proposal,
  sprint and status reports, team review, final report, individual write-up) are linked
  from [Appendix A](chapters/appendix-a-team-project/).
- Contributors should consult [`CONTRIBUTING.md`](CONTRIBUTING.md). This resource is intended to be a
  living, community‑improved resource.

## Building the book

The chapters are plain Markdown and render on GitHub as‑is. To build a browsable
website with [`mdBook`](https://rust-lang.github.io/mdBook/) (for a PDF, print the
site's built-in print page from your browser):

```bash
cargo install mdbook mdbook-mermaid   # one-time
mdbook serve                          # live preview at http://localhost:3000
mdbook build                          # outputs static site to ./book-output
```

`SUMMARY.md` is the mdBook table of contents; `book.toml` holds configuration.

## How this book was made (AI assistance)

This book was written in collaboration with an AI assistant (Anthropic's Claude) under
the author's direction. The author set the scope, chapter progression, and course
alignment; supplied source material and corrections; fact-checked claims against the
primary sources cited in each chapter's *Open Resources* page; and edited the prose
throughout. The author has reviewed, and stands behind, every chapter. If you find an
error, please [open an issue](https://github.com/tghastings/open-swe-book/issues),
regardless of how it was introduced.

Chapter 13 teaches that professional AI use means disclosing the assistance, verifying
the output, and owning the result. This note applies that standard to the book itself.

## About the author

**Thomas Hastings** teaches software engineering at the University of Colorado Colorado
Springs. This book started as part of his combined undergraduate and graduate course,
CS 4300/5300. He also serves as an assistant professor (reservist) at the United States
Air Force Academy, where he teaches in the Department of Computer and Cyber Sciences.
He earned his Ph.D. in Engineering and M.Eng. in Software Engineering from UCCS, and
his B.S. from Colorado Christian University. His research focuses on open-source
software security and software supply chains, including the continuous verification of
components.

The focus on testing, delivery, and running code in this book comes from real-world
experience. Thomas has worked as a software engineer for over twenty years and is
currently at Amazon Web Services. He keeps this book as an open, ongoing project. The
views in this book are his own and do not reflect those of his employers.

Links: [Google Scholar](https://scholar.google.com/citations?user=8iQ6Jt0AAAAJ) ·
[tom.hastings.dev](https://tom.hastings.dev) ·
[GitHub](https://github.com/tghastings)

## If this book helped you

This book is free, and it stays free. If it helped you learn a topic, teach a course, or
build something, the most useful thing you can do in return is
**[star the repository on GitHub](https://github.com/tghastings/open-swe-book)** — it
takes a second, and a star is how I get to see who the book is reaching: students,
instructors, teams, and self‑learners. Knowing where it lands is what tells me the work is
worth continuing, and it shapes what I write and fix next. If you have a moment for more
than a click, I would genuinely love to hear how you are using it — a quick note in an
[issue](https://github.com/tghastings/open-swe-book/issues) naming your course, team, or
project makes my week.

## Citing this book

If you use this book in a course or reference it in your writing, please cite it.
GitHub's **"Cite this repository"** button (from [`CITATION.cff`](CITATION.cff)) gives
APA and BibTeX directly, or copy the BibTeX below.

Whole book:

```bibtex
@book{hastings2026swe,
  author    = {Hastings, Thomas},
  title     = {Software Engineering: Standing on the Shoulders of Giants},
  year      = {2026},
  publisher = {Self-published},
  url       = {https://www.swebook.org/},
  note      = {Open textbook, licensed CC BY-SA 4.0. Source:
               \url{https://github.com/tghastings/open-swe-book}}
}
```

A single chapter (adjust `title`, `chapter`, and `url`):

```bibtex
@inbook{hastings2026swe-ch14,
  author    = {Hastings, Thomas},
  title     = {Delivery: CI/CD, DevOps, and Evolution},
  booktitle = {Software Engineering: Standing on the Shoulders of Giants},
  chapter   = {14},
  year      = {2026},
  publisher = {Self-published},
  url       = {https://www.swebook.org/chapters/14-delivery/}
}
```

The `\url` in `note` needs `\usepackage{url}` (or `hyperref`) in your LaTeX preamble;
with `biblatex` you can move it to a `urldate`/`addendum` field instead. If you use a
classic BibTeX style (`plain`, `plainnat`), swap `@inbook` for `@incollection` — those
styles ignore `booktitle` inside `@inbook`.

## Copyright and license

**Copyright © 2026 Thomas Hastings.** Unless otherwise noted, the text and figures are
licensed **[CC BY‑SA 4.0](LICENSE)**; code examples are licensed **MIT**. You are free to
share and adapt with attribution. All trademarks, product names, and company names are the
property of their respective owners and are used for identification and educational
purposes only. See also the [`LICENSE`](LICENSE) file.

[^1]: ACM/IEEE‑CS Joint Task Force on Computing Curricula, *Software Engineering 2014:
Curriculum Guidelines for Undergraduate Degree Programs in Software Engineering*
(SE2014), which defines the SEEK body of knowledge.
[acm.org/education/curricula-recommendations](https://www.acm.org/education/curricula-recommendations).
