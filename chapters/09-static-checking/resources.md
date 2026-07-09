# Chapter 9 — Open Resources

Free, open-licensed, or freely accessible materials that reinforce this chapter. Types: 📘 open
text · 🎓 course · 📄 primary source · 🎥 video. Licenses vary and are noted where known.

## Code review (used in §9.3)

- 📘 **Google Engineering Practices — "How to do a code review"** —
  [google.github.io/eng-practices/review](https://google.github.io/eng-practices/review/).
  Google's public guide for both reviewers and authors: what to look for, how fast to review,
  how to handle disagreement, and why "will this improve the codebase's health over time?" is
  the central question. *Licensed CC BY 3.0 — freely reusable with attribution.*
- 📘 **MIT 6.031 *Software Construction* — "Code Review" reading** —
  [web.mit.edu/6.031](https://web.mit.edu/6.031/www/sp22/classes/04-code-review/). A concrete,
  example-driven reading on reviewing for correctness and clarity, with a catalog of common
  smells. *Course materials offered openly by MIT OpenCourseWare (CC BY-NC-SA).*
- 📘 **"Software Engineering at Google," Ch. 9 "Code Review"** —
  [abseil.io/resources/swe-book](https://abseil.io/resources/swe-book/html/ch09.html). Why
  Google reviews nearly every change, the roles of reviewers, the value of small changes, and
  review latency. *Free to read online; book text CC BY-NC-ND.*
- 📄 **A. Bacchelli & C. Bird, "Expectations, Outcomes, and Challenges of Modern Code
  Review," *ICSE*, 2013** —
  [microsoft.com/research](https://www.microsoft.com/en-us/research/publication/expectations-outcomes-and-challenges-of-modern-code-review/).
  The Microsoft study behind §9.3: finding defects is the top *stated* motivation for review,
  but the realized value leans toward knowledge transfer, team awareness, and better
  solutions. *PDF freely available from Microsoft Research.*
- 📘 **SmartBear, "Best Practices for Peer Code Review"** —
  [smartbear.com](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/).
  Findings from a SmartBear study of a Cisco Systems team: review no more than 200–400 lines
  at a time, at under ~500 lines per hour — the data behind this chapter's small-change and
  review-rate advice. *Freely accessible vendor guide.*

## Inspection (used in §9.2)

- 📄 **M. E. Fagan, "Design and Code Inspections to Reduce Errors in Program Development,"
  *IBM Systems Journal* 15(3), 1976** —
  [dl.acm.org](https://dl.acm.org/doi/10.1147/sj.153.0182). The founding paper on formal
  inspection, defining the phases, roles, and the discipline of measuring the process.
  *Official record paywalled; PDF widely available from IBM and university course pages —
  search "Fagan Design and Code Inspections 1976 PDF."*
- 📄 **M. E. Fagan, "Advances in Software Inspections," *IEEE Transactions on Software
  Engineering* SE-12(7), 1986** —
  [research.ibm.com](https://research.ibm.com/publications/advances-in-software-inspections).
  Fagan's follow-up a decade later: the six-operation process (planning, overview,
  preparation, inspection, rework, follow-up) and reported quality results. *Abstract page
  free; full text via IEEE or course-page PDFs.*
- 📄 **B. Boehm & V. R. Basili, "Software Defect Reduction Top 10 List," *IEEE Computer*
  34(1), 2001** —
  [cs.umd.edu](https://www.cs.umd.edu/projects/SoftEng/ESEG/papers/82.78.pdf). A compact
  survey of defect-reduction evidence, including the finding that peer reviews catch about
  60% of defects — the basis for §9.2's "more than half." *Free author-hosted PDF.*
- 📄 **L. G. Votta, "Does Every Inspection Need a Meeting?," *ACM SIGSOFT FSE*, 1993** —
  [dl.acm.org](https://dl.acm.org/doi/10.1145/167049.167070). The empirical study showing
  that individual preparation, not the meeting, finds most inspection defects — the source
  for §9.2.1's claim about the preparation phase. *Abstract free; full text paywalled.*
- 📄 **NASA Software Formal Inspections Standard (NASA-STD-8739.9)** —
  [standards.nasa.gov](https://standards.nasa.gov/standard/NASA/NASA-STD-87399). A public,
  practical standard for running inspections, including participant roles, entry/exit
  criteria, and data collection. *U.S. government work — public domain.*

## Automated static analysis (used in §9.4)

- 📘 **SonarQube / SonarSource documentation** —
  [docs.sonarsource.com](https://docs.sonarsource.com/). Docs for a widely used static-analysis
  platform: rule categories (bugs, vulnerabilities, code smells), quality gates, and how
  findings are surfaced in CI. *Docs free to read; the tool has open-source and commercial
  editions.*
- 📄 **"Lessons from Building Static Analysis Tools at Google," *CACM* 61(4), 2018** —
  [cacm.acm.org](https://cacm.acm.org/research/lessons-from-building-static-analysis-tools-at-google/).
  The primary source behind §9.4.2's argument that *false-positive rate*, not raw recall,
  decides whether developers act on a tool. Explains their target of keeping false positives
  low enough that warnings get fixed.
- 📘 **Clang Static Analyzer — user documentation** —
  [clang-analyzer.llvm.org](https://clang-analyzer.llvm.org/). Openly documented data-flow /
  bug-pattern analyzer for C/C++/Objective-C, useful for seeing what path-sensitive analysis
  actually reports. *Open source (Apache-2.0 with LLVM exceptions).*

## Learning from failure (used in §9.1)

- 📄 **N. G. Leveson & C. S. Turner, "An Investigation of the Therac-25 Accidents," *IEEE
  Computer* 26(7), 1993** —
  [ieeexplore.ieee.org](https://ieeexplore.ieee.org/document/274940). The definitive
  investigation of the Therac-25 overdoses, including the manufacturer's unexamined
  assumptions about software reliability — the source behind §9.1.2's retrospective-review
  point. *Official record paywalled; an updated version is freely available from the author
  at [sunnyday.mit.edu](http://sunnyday.mit.edu/papers/therac.pdf).*

## License note

Linked resources remain under their own licenses (noted above where known); this page is
CC BY-SA 4.0.
