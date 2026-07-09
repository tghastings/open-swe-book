# Chapter 10 — Open Resources

Free, open-licensed, or freely accessible materials that reinforce this chapter. Types: 📘 open
text · 🎓 course · 📄 primary source / standard · 🎥 video. Each entry notes its license or access terms; when in doubt, check the linked page.

## Foundations: what to test and how

- 🎓 **MIT 6.031 — Software Construction, "Testing" reading** —
  [web.mit.edu/6.031](https://web.mit.edu/6.031/www/sp22/classes/03-testing/). Excellent
  treatment of partitioning the input space, choosing test cases, and coverage. *License:
  the 6.031 materials are offered for reuse under Creative Commons (BY-SA); check the page
  footer.*
- 🎓 **UC Berkeley — Engineering Software as a Service (ESaaS), ch. 8 "Testing"** —
  [saasbook.info](https://www.saasbook.info/). Test-driven development, mocks/stubs, and
  the testing pyramid in a full-stack context. *License: book is free to read online;
  see the site for terms.*
- 📘 **Software Engineering at Google — testing chapters** (Ch. 12 "Testing Overview",
  Ch. 13 "Unit Testing", Ch. 10 "Test Doubles", Ch. 14 "Larger Testing") —
  [abseil.io/resources/swe-book](https://abseil.io/resources/swe-book). Industrial
  perspective on test size, flakiness, hermeticity, and scaling a suite. *License: CC
  BY-NC-ND 4.0 (free to read; no derivatives).*
- 📄 **Dijkstra — "Notes on Structured Programming" (EWD249, 1970)** —
  [cs.utexas.edu](https://www.cs.utexas.edu/~EWD/ewd02xx/EWD249.PDF). Source of the
  chapter's opening principle: "Program testing can be used to show the presence of bugs,
  but never to show their absence!" *Access: free in the UT Austin EWD archive.*
- 📄 **Boehm — "Verifying and Validating Software Requirements and Design
  Specifications"**, IEEE Software 1(1), 1984 —
  [doi.org](https://doi.org/10.1109/MS.1984.233702). Origin of the "building the product
  right" (verification) vs. "building the right product" (validation) distinction.
  *Access: abstract free; full text via IEEE Xplore (paywalled).*
- 📄 **Boehm & Basili — "Software Defect Reduction Top 10 List"**, IEEE Computer 34(1),
  2001 — [cs.umd.edu](https://www.cs.umd.edu/projects/SoftEng/ESEG/papers/82.78.pdf). The
  classic evidence that defects cost far more to fix the later they are found. *Access:
  free author copy at the University of Maryland.*
- 📄 **Barr, Harman, McMinn, Shahbaz & Yoo — "The Oracle Problem in Software Testing: A
  Survey"**, IEEE TSE 41(5), 2015 — [doi.org](https://doi.org/10.1109/TSE.2014.2372785).
  The definitive survey behind §10.1.4's oracle strategies. *Access: abstract free; full
  text via IEEE Xplore (paywalled); author preprints circulate freely.*
- 📄 **DeMillo, Lipton & Sayward — "Hints on Test Data Selection: Help for the Practicing
  Programmer"**, IEEE Computer 11(4), 1978 —
  [doi.org](https://doi.org/10.1109/C-M.1978.218136). The paper that launched mutation
  testing (§10.1.5) and the coupling effect. *Access: abstract free; full text via IEEE
  Xplore (paywalled).*
- 📘 **Myers — "The Art of Software Testing"** (Wiley, 1979; 3rd ed. 2011) —
  [wiley.com](https://www.wiley.com/en-us/The+Art+of+Software+Testing%2C+3rd+Edition-p-9781119202486).
  The classic source for equivalence partitioning, boundary-value analysis, and
  multiple-condition coverage (§10.4, §10.5). *Access: commercial book; often in university
  libraries.*
- 📘 **Kaner, Bach & Pettichord — "Lessons Learned in Software Testing"** (Wiley, 2002) —
  [wiley.com](https://www.wiley.com/en-us/Lessons+Learned+in+Software+Testing:+A+Context+Driven+Approach-p-9780471081128).
  Context-driven testing wisdom, including the hardware origin of the "smoke test" name
  (§10.2.3). *Access: commercial book.*

## Coverage criteria, white-box, and MC/DC

- 📘 **Ammann & Offutt — "Introduction to Software Testing" companion site** —
  [cs.gmu.edu/~offutt/softwaretest](https://cs.gmu.edu/~offutt/softwaretest/). Slides,
  examples, and tools for graph coverage, logic coverage (including MC/DC), and
  input-space partitioning — the academic backbone of §§10.3–10.6. *Access: teaching
  materials free on the author's site.*
- 📄 **NASA/DOT-FAA — "A Practical Tutorial on Modified Condition/Decision Coverage"**
  (Hayhurst, Veerhusen, Chilenski, Rierson), NASA/TM-2001-210876 —
  [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/20010057789). The definitive, worked
  explanation of MC/DC, independence pairs, and the N + 1 minimum test count. *License:
  U.S. government work, public domain.*
- 📄 **RTCA DO-178C** (software considerations in airborne systems) —
  [rtca.org](https://www.rtca.org/). The standard whose Table A-7 *mandates* MC/DC at the
  most critical software level (Level A). The standard itself is sold by RTCA, but many
  university course pages summarize its coverage objectives for free.
- 📄 **McCabe — "A Complexity Measure"**, IEEE TSE SE-2(4), 1976 —
  [doi.org](https://doi.org/10.1109/TSE.1976.233837). The original cyclomatic-complexity
  paper behind §10.3.1. *Access: abstract free; full text via IEEE Xplore (paywalled).*
- 📄 **NIST SP 500-235 — "Structured Testing: A Testing Methodology Using the Cyclomatic
  Complexity Metric"** (Watson & McCabe, 1996) —
  [nvlpubs.nist.gov](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication500-235.pdf).
  Basis-path testing and the evidence for treating complexity 10 as a working limit.
  *License: U.S. government work, public domain.*
- 📄 **SEI — "C4 Software Technology Reference Guide" (CMU/SEI-97-HB-001, 1997)** —
  [sei.cmu.edu](https://www.sei.cmu.edu/documents/1625/1997_002_001_16523.pdf). Source of
  the conventional cyclomatic-complexity risk bands (1–10, 11–20, 21–50, >50) quoted in
  §10.3.1. *Access: free PDF from the SEI.*

## Black-box and combinatorial testing

- 📄 **NIST — Automated Combinatorial Testing for Software (ACTS) project** —
  [csrc.nist.gov/projects/automated-combinatorial-testing-for-software](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software).
  The empirical fault-strength data behind §10.6, plus the free **ACTS** covering-array
  generator and NIST Special Publication 800-142. *License: U.S. government work, public
  domain; ACTS tool free for download.*
- 📄 **Microsoft PICT — Pairwise Independent Combinatorial Testing tool** —
  [github.com/microsoft/pict](https://github.com/microsoft/pict). A small, scriptable
  covering-array generator for building pairwise test suites. *License: MIT.*
- 📄 **Kuhn, Wallace & Gallo — "Software Fault Interactions and Implications for Software
  Testing"**, IEEE TSE 30(6), 2004 —
  [csrc.nist.gov](https://csrc.nist.gov/pubs/journal/2004/06/software-fault-interactions-and-implications-for-s/final).
  The fault-database study behind §10.6's claim that most interaction failures involve
  only two or three parameters. *Access: NIST page links a free preprint.*
- 📄 **Kuhn, Kacker & Lei — NIST SP 800-142, "Practical Combinatorial Testing"** (2010) —
  [csrc.nist.gov](https://csrc.nist.gov/pubs/sp/800/142/final). The full how-to for
  pairwise and higher-strength testing, with the empirical interaction-rule data.
  *License: U.S. government work, public domain.*
- 📄 **Miller, Fredriksen & So — "An Empirical Study of the Reliability of UNIX
  Utilities"**, CACM 33(12), 1990 — [doi.org](https://doi.org/10.1145/96267.96279). The
  study that coined "fuzz" testing (§10.4.2) by crashing a quarter of UNIX utilities with
  random input. *Access: abstract free; free copies via the UW–Madison fuzzing project.*

## Tools and practice

- 📘 **pytest documentation** — [docs.pytest.org](https://docs.pytest.org/). Fixtures,
  parametrization, and the `raises` idiom used in this chapter's examples. *License:
  docs under MIT.*
- 📄 **Hypothesis — property-based testing for Python** —
  [hypothesis.readthedocs.io](https://hypothesis.readthedocs.io/). Puts the property/
  invariant oracles of §10.1.4 into practice by generating inputs for you. *License:
  MPL-2.0.*
- 📘 **Python `unittest.mock` — official documentation** —
  [docs.python.org/3/library/unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html).
  `Mock`, `patch`, and `side_effect` — the standard-library way to build the stubs and
  mocks of §10.2.1. *License: Python docs, PSF license (free to read and reuse).*
- 📘 **behave — BDD for Python, documentation** —
  [behave.readthedocs.io](https://behave.readthedocs.io/). Executable Gherkin as in the
  §10.2.3 callout: a `features/` directory of `.feature` scenarios plus a `steps/`
  directory whose `@given`/`@when`/`@then` functions bind each step to code. *License:
  BSD-2-Clause.*
- 📄 **mutmut — mutation testing for Python** —
  [mutmut.readthedocs.io](https://mutmut.readthedocs.io/). Generates and runs the mutants
  of §10.1.5 against a pytest suite and reports the survivors. *License: open source; see
  the project page.*
- 📄 **Google OSS-Fuzz — continuous fuzzing documentation** —
  [google.github.io/oss-fuzz](https://google.github.io/oss-fuzz/). How industrial-scale
  fuzz testing (§10.4) is run continuously against hundreds of open-source projects, with
  guides for adding your own. *License: Apache-2.0.*
- 🎥 **"TDD, Where Did It All Go Wrong" — Ian Cooper** (conference talk, freely on
  YouTube). A widely-cited critique of testing implementation details instead of behavior;
  a good companion to the pyramid and oracle discussions. *Access: free to view.*
- 📄 **McConnell — "Daily Build and Smoke Test"**, IEEE Software 13(4), 1996 —
  [stevemcconnell.com](https://stevemcconnell.com/ieeesoftware/bp04.htm). The classic
  best-practices column on gating every build with a smoke test (§10.2.3). *Access: free
  on the author's site.*
- 📄 **Fowler — "TestPyramid"** (martinfowler.com bliki) —
  [martinfowler.com/bliki/TestPyramid.html](https://martinfowler.com/bliki/TestPyramid.html).
  A short, free summary of the testing pyramid, crediting Mike Cohn's *Succeeding with
  Agile* (2009), where the model appeared (§10.2.4). *Access: free to read.*
- 📄 **Ottinger & Schuchert — "F.I.R.S.T." (Agile in a Flash, 2009)** —
  [agileinaflash.blogspot.com](https://agileinaflash.blogspot.com/2009/02/first.html). The
  originators' write-up of the FIRST properties of §10.2.1, popularized in Robert C.
  Martin's *Clean Code* (2008), ch. 9. *Access: free blog post.*
- 📄 **Luo, Hariri, Eloussi & Marinov — "An Empirical Analysis of Flaky Tests"**, FSE
  2014 — [doi.org](https://doi.org/10.1145/2635868.2635920). The empirical taxonomy of
  flaky-test root causes (async waits, concurrency, order dependence) behind §10.2.4.
  *Access: free author copy on the authors' Illinois pages; ACM DL paywalled.*

## License note

Linked resources remain under their own licenses (noted above where known); this page is
licensed **CC BY-SA 4.0**.
