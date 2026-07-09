# Chapter 6 — Open Resources

Free, open-licensed, or freely accessible materials that reinforce this chapter. Types: 📘 open
text · 🎓 course · 📄 primary source · 🎥 video. Licenses vary and are noted where known; when a
resource is free to read but not openly relicensable, it is marked *free to read*.

## Modularity, abstraction, and interfaces

- 🎓 **MIT 6.031 — Software Construction (specs, ADTs, abstraction functions)** —
  [web.mit.edu/6.031](http://web.mit.edu/6.031/). The readings on *specifications*,
  *abstract data types*, and *abstraction functions & rep invariants* are the best free
  treatment of information hiding and interface design anywhere. *License:* course
  materials under **CC BY-SA** (see the site footer).
- 📘 **Software Engineering at Google** — [abseil.io/resources/swe-book](https://abseil.io/resources/swe-book).
  Especially the chapters on *dependencies*, *large-scale change*, and *deprecation*, which
  show coupling, modularity, and "design for change" at industrial scale. *License:* free to
  read online; individual figures **CC BY 4.0** (see the book's front matter).
- 📄 **D. L. Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules"**
  (1972) — the paper that introduced information hiding. Official abstract page:
  [dl.acm.org/doi/10.1145/361598.361623](https://dl.acm.org/doi/10.1145/361598.361623);
  also widely available as a PDF via university course pages. *License:* ACM copyright,
  *free to read* via many .edu mirrors.
- 📄 **F. P. Brooks, Jr., *The Mythical Man-Month: Essays on Software Engineering***
  (1975; anniversary ed. 1995) — the source of *conceptual integrity* (§6.1.3). Publisher
  page: [informit.com](https://www.informit.com/store/mythical-man-month-essays-on-software-engineering-anniversary-9780201835953).
  *License:* commercial book; catalog page *free to read*.

## Coupling, cohesion, and design principles

- 📘 **Refactoring.Guru — Design Principles & SOLID** —
  [refactoring.guru/design-patterns](https://refactoring.guru/design-patterns)
  and [refactoring.guru/refactoring/smells/couplers](https://refactoring.guru/refactoring/smells/couplers).
  Clear, illustrated explanations of coupling smells and the principles behind low
  coupling / high cohesion. *License:* free to read; content is the site's own (not openly
  relicensable).
- 📘 **MIT 6.005/6.031 "Reading: Designing specifications / Abstraction"** —
  [web.mit.edu/6.031](http://web.mit.edu/6.031/) (see the *Specifications* and
  *Abstraction Functions & Rep Invariants* readings). Covers cohesion and coupling
  implicitly through spec strength and representation independence. *License:* **CC BY-SA**.
- 📄 **W. P. Stevens, G. J. Myers, and L. L. Constantine, "Structured Design"**, *IBM
  Systems Journal* 13(2), 1974 — the paper that introduced coupling and cohesion (§6.2.2).
  Official page: [dl.acm.org/doi/10.1147/sj.132.0115](https://dl.acm.org/doi/10.1147/sj.132.0115).
  *License:* IBM and ACM copyright, *free to read* via .edu mirrors.
- 📄 **E. Yourdon and L. L. Constantine, *Structured Design: Fundamentals of a Discipline
  of Computer Program and Systems Design*** (1979) — the book-length treatment of the
  coupling and cohesion ladders used in §6.2.2. Borrowable scan:
  [archive.org](https://archive.org/details/Structured_Design_Edward_Yourdon_Larry_Constantine).
  *License:* commercial book; *free to borrow* via the Internet Archive.
- 📄 **R. C. Martin, "Design Principles and Design Patterns"** (2000) — the paper that
  collected the five principles later known as SOLID (§6.2.3).
  [Archived PDF](https://web.archive.org/web/20030416004136/http://www.objectmentor.com/resources/articles/Principles_and_Patterns.PDF)
  via the Wayback Machine. *License:* © Robert C. Martin, *free to read*.
- 📄 **B. Meyer, *Object-Oriented Software Construction*** (1988; 2nd ed. 1997) — origin of
  the open-closed principle's "open for extension, closed for modification." Author's page:
  [bertrandmeyer.com/OOSC2](https://bertrandmeyer.com/OOSC2/). *License:* commercial book;
  the author's page is *free to read*.
- 📄 **B. H. Liskov and J. M. Wing, "A Behavioral Notion of Subtyping"**, *ACM TOPLAS*
  16(6), 1994 — the formal statement behind the Liskov substitution principle. Official
  page: [dl.acm.org/doi/10.1145/197320.197383](https://dl.acm.org/doi/10.1145/197320.197383).
  *License:* ACM copyright, *free to read* via .edu mirrors.
- 📘 **A. Hunt and D. Thomas, *The Pragmatic Programmer*** (1999; 20th-anniversary ed.
  2019) — origin of DRY, "every piece of knowledge must have a single, unambiguous,
  authoritative representation." Publisher page:
  [pragprog.com](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/).
  *License:* commercial book; extracts on the publisher page are *free to read*.

## Class diagrams and UML notation

- 📘 **UML-diagrams.org — Class Diagrams** —
  [uml-diagrams.org/class-diagrams-overview.html](https://www.uml-diagrams.org/class-diagrams-overview.html).
  A precise, example-rich reference for association, aggregation, composition,
  generalization, dependency, and multiplicity notation. *License:* free to read
  (site's own content).
- 📄 **OMG, *OMG Unified Modeling Language (OMG UML)*, version 2.5.1** (2017) — the
  normative specification for the class-diagram notation in §6.3 (visibility markers,
  association, aggregation, composition, generalization, dependency, multiplicity).
  [omg.org/spec/UML/2.5.1](https://www.omg.org/spec/UML/2.5.1/). *License:* specification
  is *free to download* from the OMG.
- 📘 **Mermaid — Class Diagram syntax** —
  [mermaid.js.org/syntax/classDiagram.html](https://mermaid.js.org/syntax/classDiagram.html).
  The notation used for the diagrams in this chapter, so you can reproduce and extend them.
  *License:* **MIT** (Mermaid is open source).

## Architectural views (used in §6.4)

- 📄 **P. Kruchten, "Architectural Blueprints — The 4+1 View Model of Software
  Architecture"**, *IEEE Software*, 1995 —
  [PDF](https://www.cs.ubc.ca/~gregor/teaching/papers/4+1view-architecture.pdf). The primary
  source for §6.4; short and very readable. *License:* IEEE copyright, *free to read* via a
  university course page.
- 📄 **ISO/IEC/IEEE 42010 — Architecture description** — the standard behind "views,"
  "viewpoints," and "concerns." Overview and definitions at
  [archived overview site](https://web.archive.org/web/2023/http://www.iso-architecture.org/42010/) (original site now offline); official catalog
  page: [iso.org/standard/74393.html](https://www.iso.org/standard/74393.html). *License:*
  standard is paid; the overview page is *free to read*.
- 📘 **Software Architecture in Practice / SEI resources** — L. Bass, P. Clements, and
  R. Kazman's book (4th ed. 2021,
  [insights.sei.cmu.edu](https://insights.sei.cmu.edu/library/software-architecture-in-practice-fourth-edition/))
  defines architecture as the set of structures needed to reason about a system and names
  the module / component-and-connector / allocation structure families (§6.1.1, §6.4.2);
  the Software Engineering Institute also publishes free technical reports on *views and
  beyond* and *architecture documentation* at
  [resources.sei.cmu.edu](https://resources.sei.cmu.edu/library/). *License:* book is
  commercial; SEI reports are free to download (U.S. government–funded FFRDC reports).
- 📘 **"Shape Up," Ryan Singer (Basecamp), chs. "Principles of Shaping" and "Find the
  Elements"** — shaped work as rough / solved / bounded, breadboarding
  (places/affordances/connections), fat-marker sketches, and designing at the right
  fidelity (used in §6.1.2). <https://basecamp.com/shapeup/1.1-chapter-02> ·
  <https://basecamp.com/shapeup/1.3-chapter-04> · *Free to read online; © Basecamp.*

## Quality-attribute scenarios

- 📘 **"Software Architecture in Practice" (4th ed.), Bass, Clements & Kazman** — the
  standard treatment of quality-attribute scenarios (§6.1.4) and architecture evaluation.
  <https://www.informit.com/store/software-architecture-in-practice-9780136886099>.
  *License:* commercial book; the sample chapters and companion material on the publisher
  and SEI sites are *free to read*.

## License note

Linked resources remain under their own licenses; where a resource is only *free to read*
rather than openly licensed, treat its text as read-only and cite it rather than copying it.
This page itself is licensed **CC BY-SA 4.0**.
