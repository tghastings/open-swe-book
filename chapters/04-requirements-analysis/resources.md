# Chapter 4 — Open Resources

Curated, freely available materials for going deeper on requirements analysis: estimation,
consensus techniques, prioritization, satisfaction modeling, and algorithmic cost models.
Legend: 📘 reading/article · 🎓 course/courseware · 📄 paper/standard · 🎥 video. Each entry
notes access terms; "free to read" means available at no cost, though not always under an
open license. Prefer these over paywalled textbooks.

---

## Relative estimation, story points, and velocity

- 📘 **Mike Cohn — "What Are Story Points?" and related estimation articles** (Mountain
  Goat Software blog). The most widely cited practitioner writing on story points,
  velocity, and relative sizing.
  <https://www.mountaingoatsoftware.com/blog/what-are-story-points>
  *Free to read; © Mountain Goat Software. Concepts are freely reusable; do not copy text.*

- 📘 **Mike Cohn — main blog** (agile planning, splitting stories, release forecasting).
  <https://www.mountaingoatsoftware.com/blog>
  *Free to read.*

- 📘 **Mike Cohn — *Agile Estimating and Planning* (Prentice Hall, 2005).** The standard
  book-length treatment of story points, relative sizing, velocity, and release planning.
  <https://www.mountaingoatsoftware.com/books/agile-estimating-and-planning>
  *Commercial book; official page free to read. Check your library for the full text.*

- 🎓 **Atlassian Agile Coach — "Estimation" and "Sprints/Velocity" guides.** Clear,
  vendor-neutral tutorials with worked examples of forecasting from velocity.
  <https://www.atlassian.com/agile/project-management/estimation>
  *Free to read; © Atlassian.*

## Consensus estimation: Planning Poker and Delphi

- 📘 **Planning Poker — overview.** The canonical description of the technique and its rules.
  <https://www.mountaingoatsoftware.com/agile/planning-poker>
  *Free to read; © Mountain Goat Software.*

- 📄 **James Grenning — "Planning Poker or How to Avoid Analysis Paralysis While Release
  Planning" (2002).** The original paper introducing Planning Poker, hosted by its author.
  <https://wingman-sw.com/papers/PlanningPoker-v1.1.pdf>
  *Free to download; © James Grenning.*

- 📘 **RAND Corporation — "Delphi Method" topic page.** RAND's own overview of the method's
  origin (1950s, Olaf Helmer and Norman Dalkey, forecasting technology's effect on warfare).
  <https://www.rand.org/topics/delphi-method.html>
  *Free to read; © RAND.*

- 📄 **Barry Boehm — Wideband Delphi** (described in *Software Engineering Economics*, 1981,
  and summarized in many open lecture notes). For an openly accessible summary, see the
  Wikipedia article, which cites primary sources:
  <https://en.wikipedia.org/wiki/Wideband_delphi>
  *Wikipedia text is CC BY-SA 4.0.*

- 📄 **Dalkey & Helmer — "An Experimental Application of the Delphi Method"** (RAND, 1963).
  The foundational report on the original Delphi method. RAND makes many historical reports
  freely downloadable.
  <https://www.rand.org/pubs/research_memoranda/RM727z1.html>
  *Free to download from RAND.*

## Prioritization

- 📘 **DSDM / Agile Business Consortium — MoSCoW Prioritisation.** The source framework that
  defines Must/Should/Could/Won't and the effort-balancing guidance (e.g., capping Musts
  at roughly 60% of effort).
  <https://www.agilebusiness.org/dsdm-project-framework/moscow-prioritisation.html>
  *Free to read; © Agile Business Consortium.*

- 📘 **Scaled Agile — "WSJF (Weighted Shortest Job First)."** The cost-of-delay ÷ job-size
  prioritization scheme, adapted from Donald G. Reinertsen, *The Principles of Product
  Development Flow* (Celeritas, 2009).
  <https://framework.scaledagile.com/wsjf>
  *Free to read; © Scaled Agile, Inc. Reinertsen's book is commercial.*

- 📘 **Roman Pichler — "Product Prioritization" articles** (value vs. cost vs. risk, and
  when to sequence risky work early). Practical, well-illustrated.
  <https://www.romanpichler.com/blog/>
  *Free to read; © Roman Pichler.*

## Customer satisfaction: the Kano model

- 📘 **Kano model — overview and how-to** (Folding Burritos / Daniel Zacarias,
  "Complete Guide to the Kano Model"). A thorough, well-diagrammed practitioner explanation
  of the categories, the two-question survey, and category decay.
  <https://foldingburritos.com/blog/kano-model/>
  *Free to read.*

- 📄 **Kano et al. (1984) — "Attractive Quality and Must-Be Quality."** The original paper
  introducing the model (*Journal of the Japanese Society for Quality Control* 14(2)).
  Free to read on J-STAGE: <https://doi.org/10.20684/quality.14.2_147>
  *Copyrighted (in Japanese); the Wikipedia article (CC BY-SA) is a fair open starting point:*
  <https://en.wikipedia.org/wiki/Kano_model>

- 📄 **Kano (2001) — "Life Cycle and Creation of Attractive Quality"** (4th International
  QMOD Conference). Kano's follow-up showing categories decay over time — delighters age
  into must-bes.
  <https://www.semanticscholar.org/paper/Life-Cycle-and-Creation-of-Attractive-Quality-Kano/488788f1b49e92ee9ffb3bae6164c24374e1b2e4>
  *Copyrighted; abstract and citation record free via Semantic Scholar.*

## Plan-driven / algorithmic estimation: COCOMO

- 📄 **Barry W. Boehm — *Software Engineering Economics* (Prentice-Hall, 1981).** The book
  that introduced COCOMO (and Wideband Delphi); the source of the Basic COCOMO a/b
  coefficients and schedule equations.
  <https://dl.acm.org/doi/10.5555/539425>
  *Commercial book; ACM catalog page free. Check your library for the full text.*

- 📄 **Boehm et al. — "Cost Models for Future Software Life Cycle Processes: COCOMO 2.0"**
  (USC-CSE technical report, 1995). The primary open specification of COCOMO II, including
  the power-law form and scale/effort factors. The USC CSSE site is offline; archived copy:
  <https://web.archive.org/web/20160910062006/http://csse.usc.edu/TECHRPTS/1995/usccse95-500/usccse95-500.pdf>
  *Free to download (Internet Archive).*

- 📄 **Boehm et al. — *COCOMO II Model Definition Manual*, v2.1 (USC CSE, 2000).** The full
  COCOMO II specification: function-point sizing, five scale factors, seventeen effort
  multipliers. Widely mirrored by universities, e.g.:
  <https://www.rose-hulman.edu/class/csse/csse372/201410/Homework/CII_modelman2000.pdf>
  *Free to download; © USC.*

- 🎓 **USC Center for Systems and Software Engineering — COCOMO II tool page** (archived;
  the live site is offline).
  <https://web.archive.org/web/20220319202437/https://csse.usc.edu/tools/COCOMOII>
  *Free to use; © USC CSSE.*

- 📘 **Frederick P. Brooks, Jr. — *The Mythical Man-Month* (Addison-Wesley, 1975).** Source
  of the n(n−1)/2 intercommunication formula behind the diseconomy-of-scale discussion in
  §4.6.1.
  <https://www.informit.com/store/mythical-man-month-essays-on-software-engineering-anniversary-9780201835953>
  *Commercial book; publisher page free. Check your library for the full text.*

## Estimation, judgment, and its limits (background)

- 📘 **Steve McConnell — *Software Estimation: Demystifying the Black Art* companion materials / articles**
  (Construx resources). Practical guidance on estimate-vs-target, ranges, and re-estimation.
  <https://www.construx.com/resources/>
  *Free to read; © Construx.*

- 📄 **Tversky & Kahneman (1974) — "Judgment under Uncertainty: Heuristics and Biases,"**
  *Science*. The primary source on anchoring — essential background for §4.2.1. Widely
  available as a free PDF via university course pages.
  <https://www.science.org/doi/10.1126/science.185.4157.1124>
  *Copyrighted; free preprints commonly hosted by universities.*

- 📄 **Strack & Mussweiler (1997) — "Explaining the Enigmatic Anchoring Effect,"** *Journal
  of Personality and Social Psychology* 73(3). The Gandhi age-9/age-140 anchoring
  demonstration cited in §4.2.1.
  <https://doi.org/10.1037/0022-3514.73.3.437>
  *Copyrighted (APA); abstract free at the DOI.*

- 📘 **Atul Gawande — *The Checklist Manifesto* (Metropolitan Books, 2009).** How surgery
  and aviation turned hard-won experience into checklists — background for §4.1.
  <https://atulgawande.com/book/the-checklist-manifesto/>
  *Commercial book; author's page free. Check your library for the full text.*

## Appetite: fixed time, variable scope

- 📘 **Ryan Singer — *Shape Up: Stop Running in Circles and Ship Work that Matters*
  (Basecamp, 2019).** The free online book behind §4.2.4: *appetite* vs. estimate,
  fixed-time/variable-scope, the circuit breaker, scope hammering, and judging against the
  baseline. See especially the Introduction and "Bets, Not Backlogs."
  <https://basecamp.com/shapeup>
  *Free to read online; © Basecamp.*

## License note

Linked resources remain under their own licenses; this page is CC BY-SA 4.0.
