# Chapter 7 — Open Resources

Free, openly-licensed or freely-readable materials that reinforce this chapter. Types:
📘 open text/report · 🎓 course · 📄 primary source/catalog · 🎥 video. Each entry notes
how freely it can be reused; unless stated, a resource is *free to read* but remains under
its author's copyright.

## Pattern catalogs (use across the whole chapter)

- 📄 **Martin Fowler — *Patterns of Enterprise Application Architecture*, online catalog**
  — [martinfowler.com/eaaCatalog](https://martinfowler.com/eaaCatalog/). Concise
  entries for layering, repository/shared-data, MVC and its relatives, and the
  service/domain split. *Free to read online; text is © the author.*
- 📄 **Martin Fowler — "GUI Architectures"** —
  [martinfowler.com/eaaDev/uiArchs.html](https://martinfowler.com/eaaDev/uiArchs.html).
  The clearest free treatment of MVC, MVP, MVVM, the observer wiring behind them, and the
  humble-view idea used in §7.3.3. *Free to read; © the author.*
- 📄 **Martin Fowler — "Humble Object"** —
  [martinfowler.com/bliki/HumbleObject.html](https://martinfowler.com/bliki/HumbleObject.html).
  The humble-view discipline of §7.3.3 in pattern form, crediting Michael Feathers'
  "Humble Dialog Box" and Gerard Meszaros' *xUnit Test Patterns*. *Free to read; © the author.*
- 📄 **E. Gamma, R. Helm, R. Johnson & J. Vlissides — *Design Patterns* (1994), publisher's
  page** —
  [informit.com](https://www.informit.com/store/design-patterns-elements-of-reusable-object-oriented-9780201633610).
  The original catalog entry for the observer pattern of §7.2.2. *Catalog page free to read;
  the book itself is a paid text.*
- 📄 **F. Buschmann, R. Meunier, H. Rohnert, P. Sommerlad & M. Stal — *Pattern-Oriented
  Software Architecture, Vol. 1: A System of Patterns* (1996), publisher's page** —
  [wiley.com](https://www.wiley.com/en-us/Pattern-Oriented+Software+Architecture,+Volume+1,+A+System+of+Patterns-p-9780471958697).
  The catalog that documents layers, broker, and blackboard as named patterns. *Catalog page
  free to read; the book itself is a paid text.*
- 📄 **MVC in real frameworks** — Django's own account of its MTV naming
  ([Django FAQ](https://docs.djangoproject.com/en/stable/faq/general/)), Rails' MVC code
  organization ([Rails Guides](https://guides.rubyonrails.org/getting_started.html)), and
  Redux's single-store, one-way data flow
  ([Three Principles](https://redux.js.org/understanding/thinking-in-redux/three-principles)),
  as used in §7.3.3's "MVC in the wild." *Free official documentation.*
- 📄 **Patterns at production scale** — engineering write-ups from Instagram on Django
  (["Static Analysis at Scale"](https://instagram-engineering.com/static-analysis-at-scale-an-instagram-story-8f498ab71a0c)),
  Shopify on Rails
  (["Deconstructing the Monolith"](https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity)),
  and Airbnb on React
  (["Rearchitecting Airbnb's Frontend"](https://medium.com/airbnb-engineering/rearchitecting-airbnbs-frontend-5e213efc24d2))
  — the systems named in §7.3.3. *Free to read; © the companies.*
- 📘 **Mark Richards — *Software Architecture Patterns*** (O'Reilly report) — a short,
  free report covering layered, event-driven, microkernel/plug-in, and other styles;
  register for the free download at O'Reilly. Excellent companion to §7.1 and §7.6.
  *Free with registration; © O'Reilly.*
- 📄 **Microsoft — Cloud Design Patterns** —
  [learn.microsoft.com/azure/architecture/patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/).
  Practical, vendor-documented patterns for client-server, broker/gateway, pub-sub, and
  streaming problems, each with problem/solution/considerations. *Free to read; © Microsoft,
  many samples under permissive licenses.*

## Dataflow, streams, and big data (§7.4)

- 📄 **The Reactive Manifesto** — [reactivemanifesto.org](https://www.reactivemanifesto.org/).
  A short, free statement of the principles behind responsive, message-driven, back-pressured
  systems — directly relevant to dataflow networks and unbounded streams. *Free to read.*
- 📄 **J. Dean & S. Ghemawat, "MapReduce: Simplified Data Processing on Large Clusters"**
  (OSDI 2004) — the original paper behind §7.4.4, free from Google Research:
  [research.google](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/).
  *Free to read; © the authors/publisher.*
- 📄 **M. Zaharia et al., "Resilient Distributed Datasets" (NSDI 2012)** —
  [usenix.org](https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia).
  The Spark paper: how later engines generalized MapReduce into arbitrary dataflow graphs
  (§7.4.4). *Open access via USENIX.*
- 🎥 **Tyler Akidau — "The World Beyond Batch: Streaming"** (talk/companion articles) —
  a free, accessible introduction to windows, event time, and late data that underpins
  §7.4.3. O'Reilly Radar:
  [Streaming 101](https://www.oreilly.com/radar/the-world-beyond-batch-streaming-101/).
  *Free to read.*

## Client-server, broker, and distributed structure (§7.5)

- 📘 **MIT 6.031 Software Construction — readings on interfaces, concurrency, and
  client/server** — [web.mit.edu/6.031](http://web.mit.edu/6.031/). Develops the
  "depend on an interface, swap the implementation" idea that powers test servers (§7.5.2).
  *Free courseware, Creative Commons licensed.*
- 📄 **Microsoft — Publisher-Subscriber, Gateway Aggregation, and Ambassador patterns**
  (within the Cloud Design Patterns catalog above; direct link:
  [Publisher-Subscriber](https://learn.microsoft.com/en-us/azure/architecture/patterns/publisher-subscriber))
  — concrete, documented instances of the
  broker pattern in modern systems. *Free to read; © Microsoft.*
- 📄 **James Lewis & Martin Fowler — "Microservices"** —
  [martinfowler.com/articles/microservices.html](https://martinfowler.com/articles/microservices.html).
  The essay that defined the microservice style named at the end of §7.5.4. *Free to read;
  © the authors.*

## Product lines (§7.6)

- 📄 **Carnegie Mellon Software Engineering Institute — Software Product Lines** —
  [sei.cmu.edu](https://www.sei.cmu.edu/library/software-product-lines-collection/).
  Definitions of
  commonality/variability, the domain- vs. application-engineering split, and product-line
  economics used in §7.6. *Free to read; © CMU/SEI.*
- 📄 **K. Kang, S. Cohen, J. Hess, W. Novak & A. S. Peterson — "Feature-Oriented Domain
  Analysis (FODA) Feasibility Study" (CMU/SEI-90-TR-021, 1990)** —
  [sei.cmu.edu](https://www.sei.cmu.edu/library/feature-oriented-domain-analysis-foda-feasibility-study/).
  The report that introduced feature models (§7.6.1). *Free to read; © CMU/SEI.*
- 📄 **K. Pohl, G. Böckle & F. van der Linden — *Software Product Line Engineering*
  (Springer, 2005), publisher's page** —
  [link.springer.com](https://link.springer.com/book/10.1007/3-540-28901-1). The standard
  text behind the domain- vs. application-engineering split of §7.6.2. *Catalog page free
  to read; the book itself is a paid text.*
- 📄 **SEI — "A Framework for Software Product Line Practice"** — a free online catalog of
  the practice areas an organization needs to run a product line; a good map of §7.6 at
  organizational scale. *Free to read; © CMU/SEI.*

## RESTful APIs (§7.5.4)

- 📄 **Roy Fielding — "Architectural Styles and the Design of Network-based Software
  Architectures," ch. 5** — the doctoral dissertation that defined REST.
  [ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm).
  *Free to read; © Roy Fielding.*
- 📘 **MDN Web Docs — HTTP methods and status codes** —
  [developer.mozilla.org/docs/Web/HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP).
  The practical reference for the verb grammar REST builds on. *CC BY-SA.*
- 📄 **IETF — RFC 9110, *HTTP Semantics*** —
  [rfc-editor.org/rfc/rfc9110](https://www.rfc-editor.org/rfc/rfc9110.html). The definitive
  specification of the HTTP methods in §7.5.4, including which are safe. *Freely available;
  © IETF Trust.*

## Foundational background

- 📄 **M. Shaw & D. Garlan — architectural styles** — the academic origin of thinking about
  systems as pattern/style choices (pipes-and-filters, layered, repository, client-server).
  Overview papers and lecture notes are freely available via university course pages; the
  book record for *Software Architecture: Perspectives on an Emerging Discipline* (1996) is
  at [dl.acm.org](https://dl.acm.org/doi/book/10.5555/231003).
  *Free to read; © the authors.*
- 📄 **Trygve Reenskaug — "MVC: Xerox PARC 1978–79"** —
  [folk.uio.no](https://folk.uio.no/trygver/themes/mvc/mvc-index.html).
  The inventor's own notes on the origin of Model-View-Controller (§7.3.2). *Free to read;
  © the author.*
- 📄 **ISO/IEC 7498-1:1994 — the OSI Basic Reference Model** —
  [iso.org](https://www.iso.org/standard/20269.html). The seven-layer model used as the
  textbook case of layering in §7.1.1. *Catalog page free to read; the standard text is
  paywalled.*
- 📘 **Wikipedia — "Architectural pattern"** and linked style articles —
  [en.wikipedia.org/wiki/Architectural_pattern](https://en.wikipedia.org/wiki/Architectural_pattern).
  A reliable, openly-licensed starting map with references. *Text under CC BY-SA.*


## License note

Linked resources remain under their own licenses; check each before reuse. This page and
all original prose in this chapter are licensed **CC BY-SA 4.0**.
