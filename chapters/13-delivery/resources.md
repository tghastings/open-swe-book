# Chapter 13 — Open Resources

Free, open‑licensed, or freely accessible materials that reinforce this chapter. Types: 📘 open
text · 🎓 course · 📄 primary source / standard · 🎥 video · 🛠 tool. Licenses vary and are noted
where known. Each entry notes its license or access terms; when in doubt, check the linked page.

## Primary sources for the case studies

- 📄 **SEC Release No. 34-70694 — In the Matter of Knight Capital Americas LLC** (October
  2013) — [sec.gov](https://www.sec.gov/litigation/admin/2013/34-70694.pdf). The
  enforcement order behind §13.3.5's first case study: the reused flag, the eighth server,
  the 97 unheeded alerts, and the rollback that made things worse are all findings in this
  document. Read it — it is short, plainly written, and the definitive corrective to the
  folklore versions. *License: U.S. government work, public domain.*
- 📄 **CrowdStrike — External Technical Root Cause Analysis, Channel File 291** (August
  2024) — [crowdstrike.com](https://www.crowdstrike.com/wp-content/uploads/2024/08/Channel-File-291-Incident-Root-Cause-Analysis-08.06.2024.pdf).
  The vendor's own account of the 21-versus-20 field mismatch, the validator bug, and the
  committed remediations (staged rings, customer-controlled cadence, bounds checking).
  A model of what a public post-incident analysis should contain. *Access: free on the
  vendor's site.*
- 📄 **CrowdStrike — Preliminary Post Incident Review, and Remediation and Guidance Hub**
  (July 2024) —
  [crowdstrike.com](https://www.crowdstrike.com/en-us/blog/falcon-content-update-preliminary-post-incident-report/).
  The first public account, with the deployment timeline (content released 04:09 UTC,
  reverted 05:27 UTC on July 19); the companion
  [Remediation Hub](https://www.crowdstrike.com/falcon-content-update-remediation-and-guidance-hub/)
  documents the manual safe-mode recovery steps. *Access: free on the vendor's site.*
- 📄 **Microsoft — "Helping our customers through the CrowdStrike outage"** (July 20,
  2024) —
  [blogs.microsoft.com](https://blogs.microsoft.com/blog/2024/07/20/helping-our-customers-through-the-crowdstrike-outage/).
  The source of the widely cited ~8.5 million affected-devices estimate ("less than one
  percent of all Windows machines"). *Access: free to read.*
- 📄 **Delta Air Lines — Form 8-K** (October 2024) —
  [sec.gov](https://www.sec.gov/Archives/edgar/data/27904/000168316824005369/delta_8k.htm).
  Delta's own filing on the outage: approximately 7,000 flight cancellations over five
  days and at least $500 million in claimed damages. *Access: SEC filing, public record.*
- 📄 **Parametrix — "CrowdStrike to cost Fortune 500 $5.4 billion"** (July 2024) —
  [parametrixinsurance.com](https://www.parametrixinsurance.com/in-the-news/crowdstrike-to-cost-fortune-500-5-4-billion-insured-loss-range-of-540-million-to-1-08-billion).
  The loss-estimate source: $5.4 billion in direct losses for the US Fortune 500
  (excluding Microsoft), with only 10–20 percent likely covered by cyber insurance.
  *Access: free to read.*
- 📄 **CNNMoney — "Knight Capital in $400 million rescue agreement"** (August 6, 2012) —
  [money.cnn.com](https://web.archive.org/web/2013/https://money.cnn.com/2012/08/06/investing/knight-capital-agreement/index.htm).
  Contemporary account of the emergency financing that kept Knight alive after August 1;
  the SEC order above records the July 2013 merger into KCG Holdings. *Access: free to
  read.*

## The cloud and distributed systems

- 📄 **Kubernetes documentation** — [kubernetes.io/docs](https://kubernetes.io/docs/).
  The official concepts, tutorials, and reference for §13.1.5: containers, pods, services,
  ingress, and cluster architecture, with a browser-based interactive tutorial that needs
  no installation. *License: docs are CC BY 4.0.*
- 📘 **37signals — "We have left the cloud"** —
  [world.hey.com/dhh](https://world.hey.com/dhh/we-have-left-the-cloud-251760fb). The
  first-person record of §13.1.4's repatriation case study; the announcement post
  **"Why we're leaving the cloud"** (October 2022) —
  [world.hey.com/dhh](https://world.hey.com/dhh/why-we-re-leaving-the-cloud-654b47e0) —
  lays out the reasoning and the cost arithmetic for leaving the cloud on steady,
  predictable workloads. *Access: free to read.*
- 📘 **InfoQ — "Prime Video Switched from Serverless to EC2 and ECS to Save Costs"** (May
  2023) —
  [infoq.com](https://www.infoq.com/news/2023/05/prime-ec2-ecs-saves-costs/). A concise
  writeup of the Prime Video team's account of cutting one monitoring service's cost by
  roughly 90 percent by consolidating a distributed serverless design into a
  monolith-style process (§13.1.4). The original Prime Video Tech post (Marcin Kolny,
  March 2023) is offline; an archived copy survives at
  [web.archive.org](https://web.archive.org/web/20230504060528/https://www.primevideotech.com/video-streaming/scaling-up-the-prime-video-audio-video-monitoring-service-and-reducing-costs-by-90).
  *Access: free to read.*
- 📄 **Gilbert & Lynch — "Brewer's Conjecture and the Feasibility of Consistent,
  Available, Partition-Tolerant Web Services"** (ACM SIGACT News, 2002) —
  [doi.org/10.1145/564585.564601](https://doi.org/10.1145/564585.564601). The paper that
  turned Brewer's conjecture into §13.1.6's CAP theorem by proving it; author copies
  circulate freely. Pair it with Brewer's own retrospective, **"CAP Twelve Years Later:
  How the 'Rules' Have Changed"** (IEEE Computer, 2012), free to read at
  [infoq.com/articles/cap-twelve-years-later](https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/),
  which corrects the folklore "pick two of three" reading. *Access: both freely readable.*
- 📄 **Eric Brewer — "Towards Robust Distributed Systems"** (PODC 2000 keynote slides) —
  [people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~brewer/cs262b-2004/PODC-keynote.pdf).
  The keynote in which Brewer stated CAP as a conjecture, two years before the Gilbert &
  Lynch proof above. *Access: free on the author's site.*
- 📄 **AWS — Shared Responsibility Model, and "What's the Difference Between Containers
  and Virtual Machines?"** —
  [aws.amazon.com](https://aws.amazon.com/compliance/shared-responsibility-model/) and
  [aws.amazon.com/compare](https://aws.amazon.com/compare/the-difference-between-containers-and-virtual-machines/).
  Vendor statements of §13.1.4's security-responsibility split ("security *of* the cloud"
  versus "security *in* the cloud") and §13.1.5's container/VM distinction. *Access: free
  to read.*
- 📄 **Synergy Research Group — cloud market share updates** —
  [srgresearch.com](https://www.srgresearch.com/articles/cloud-market-share-trends-big-three-together-hold-63-while-oracle-and-the-neoclouds-inch-higher).
  Quarterly market data behind §13.1.4's "big three" claim: Amazon, Microsoft, and Google
  together held 63 percent of enterprise cloud-infrastructure spending in late 2025.
  *Access: press releases free to read.*
- 📄 **CNCF Annual Survey 2023** —
  [cncf.io](https://www.cncf.io/reports/cncf-annual-survey-2023/). Adoption data behind
  §13.1.5's "de-facto standard" description of Kubernetes: 84 percent of respondents were
  using or evaluating it. *Access: free to read.*

## CI/CD and deployment practice

- 📘 **Martin Fowler — "Continuous Integration"** —
  [martinfowler.com/articles/continuousIntegration.html](https://martinfowler.com/articles/continuousIntegration.html).
  The canonical long-form article behind §13.2: mainline commits, self-testing builds,
  broken-build discipline, and the ten-minute build. *Access: free to read; ©
  martinfowler.com.*
- 📘 **Pete Hodgson — "Feature Toggles (aka Feature Flags)"** —
  [martinfowler.com/articles/feature-toggles.html](https://martinfowler.com/articles/feature-toggles.html).
  The definitive long-form treatment behind §13.3.3: toggle categories (release, ops,
  experiment, permission), lifespans, implementation patterns, and toggle-debt hygiene.
  *Access: free to read; © martinfowler.com.*
- 📘 **Martin Fowler — "DeploymentPipeline", "BlueGreenDeployment", and "CanaryRelease"**
  — [martinfowler.com/bliki](https://martinfowler.com/bliki/). Short, precise entries on
  the deployment strategies of §13.3.2. *Access: free to read.*
- 📄 **Ross Harmes (Flickr) — "Flipping Out"** (2009) —
  [code.flickr.net](https://code.flickr.net/2009/12/02/flipping-out/). The post that
  popularized the *feature flipper*: trunk-only development, flags, and multiple deploys
  a day, years before the tooling industry existed (§13.3.3). *Access: free to read.*
- 📄 **Chuck Rossi (Facebook Engineering) — "Rapid release at massive scale"** (2017) —
  [engineering.fb.com](https://engineering.fb.com/2017/08/31/web/rapid-release-at-massive-scale/).
  How Facebook's quasi-continuous release uses the Gatekeeper flag system to roll out
  code and features independently (§13.3.3). *Access: free to read.*
- 🛠 **OpenFeature** — [openfeature.dev](https://openfeature.dev/). The CNCF-incubating,
  vendor-neutral feature-flag API (§13.3.3); pairs with open-source flag backends such as
  [Unleash](https://docs.getunleash.io/guides/feature-flag-best-practices) and GitHub's
  [Flipper](https://github.com/flippercloud/flipper) for Ruby. *License: Apache-2.0
  (OpenFeature); vendor docs free to read.*
- 📄 **Minimum CD** — [minimumcd.org](https://minimumcd.org/). A community-maintained,
  vendor-neutral statement of the *minimum* practices that constitute continuous delivery
  — a useful checklist for auditing your own pipeline against §§13.2–13.3. *License: CC
  BY-SA 4.0.*
- 📘 **Bryan Finster — "5-Minute DevOps" series** — free to read on
  [bdfinst.medium.com](https://bdfinst.medium.com/) and [bryanfinster.com](https://bryanfinster.com/). Short, blunt essays from a
  practitioner on trunk-based development, small batches, pipeline discipline, and why
  "we're too regulated for CD" is usually wrong. Several installments pair directly with
  this chapter's sections. *Access: free to read.*
- 📘 **Google — Site Reliability Engineering (the SRE book and workbook)** —
  [sre.google/books](https://sre.google/books/). Free online editions covering release
  engineering, canarying, error budgets, and postmortem culture — the operations side of
  §13.3 and §13.7 at planetary scale. *License: CC BY-NC-ND 4.0 (free to read).*

## Deployment mechanics: containers, DNS, and TLS

- 🛠 **Docker — official documentation** — [docs.docker.com](https://docs.docker.com/).
  The Dockerfile reference, image-building guide, and *Get Started* tutorial behind
  §13.4.1. *Access: free to read; Docker Engine is Apache-2.0.*
- 🛠 **Docker Compose documentation** —
  [docs.docker.com/compose](https://docs.docker.com/compose/). The Compose file reference
  and multi-service examples used in §13.4.2. *Access: free to read.*
- 🛠 **Docker Official Images — Postgres and Redis** —
  [hub.docker.com/_/postgres](https://hub.docker.com/_/postgres) ·
  [hub.docker.com/_/redis](https://hub.docker.com/_/redis). Maintained, security-patched
  base images, with usage notes on volumes and environment configuration (§13.4.3).
  *Access: free; images under their projects' licenses.*
- 📘 **The Twelve-Factor App** — [12factor.net](https://12factor.net/). The widely cited
  methodology for cloud-native services; factor III (config) is the
  externalized-configuration rule of §13.4.4. *Access: free to read.*
- 📄 **Cloudflare Learning Center — DNS and reverse proxies** —
  [what is DNS?](https://www.cloudflare.com/learning/dns/what-is-dns/) ·
  [what is a reverse proxy?](https://www.cloudflare.com/learning/cdn/glossary/reverse-proxy/).
  Readable explainers for the DNS resolution chain (§13.5.1) and the edge-proxy model
  (§13.5.3). *Access: free to read.*
- 📄 **Let's Encrypt — How It Works, and ACME (RFC 8555)** —
  [letsencrypt.org/how-it-works](https://letsencrypt.org/how-it-works/) ·
  [rfc-editor.org/rfc/rfc8555](https://www.rfc-editor.org/rfc/rfc8555). The free, automated
  certificate authority and the protocol behind automatic HTTPS (§13.5.2). *Access: free;
  RFC is an IETF standard.*
- 🛠 **Caddy — automatic-HTTPS reverse proxy** —
  [caddyserver.com](https://caddyserver.com/). A web server that obtains and renews Let's
  Encrypt certificates with no configuration, the simplest way to put TLS in front of a
  container (§13.5.2). *License: Apache-2.0.*
- 📄 **Google — HTTPS encryption on the web (Transparency Report)** —
  [transparencyreport.google.com/https](https://transparencyreport.google.com/https/overview).
  Ongoing measurement of the share of web traffic served over HTTPS (§13.5.2). *Access:
  free to read.*

## DORA and delivery research

- 📄 **DORA — research program, four-keys definitions, and annual State of DevOps
  reports** — [dora.dev](https://dora.dev/). The research base for §13.7: metric
  definitions, performance-band data, capability catalog, and a quick check for assessing
  your own team. *Access: site content free; reports free to download.*
- 📘 **Forsgren, Humble, Kim — *Accelerate*** (IT Revolution Press, 2018). The book-length
  treatment of the research methodology and the speed-and-stability finding. *Not* openly
  licensed — listed here as the standard citation; the dora.dev material above covers the
  findings freely.

## Continuous security and the supply chain

- 📄 **OWASP — scanner-family references** —
  [Source Code Analysis Tools (SAST)](https://owasp.org/www-community/Source_Code_Analysis_Tools) ·
  [Vulnerability Scanning Tools (DAST)](https://owasp.org/www-community/Vulnerability_Scanning_Tools) ·
  [Component Analysis (SCA)](https://owasp.org/www-community/Component_Analysis). The
  community definitions behind §13.6.1's three scanner families, with maintained tool
  lists. *Free to read; OWASP content is CC BY-SA.*
- 📄 **CISA — Software Bill of Materials (SBOM)** — [cisa.gov/sbom](https://www.cisa.gov/sbom).
  The U.S. government's SBOM resource hub referenced in §13.6.2. *License: U.S.
  government work, public domain.*
- 📄 **GitHub Docs — Dependabot** —
  [docs.github.com/en/code-security/dependabot](https://docs.github.com/en/code-security/dependabot).
  Reference for the update-bot workflow of §13.6.2. *License: GitHub docs are CC BY 4.0.*
- 🛠 **OWASP Dependency-Check and Dependency-Track** —
  [owasp.org/www-project-dependency-check](https://owasp.org/www-project-dependency-check/)
  and [dependencytrack.org](https://dependencytrack.org/). Open-source SCA: the first
  scans a build for known-vulnerable components; the second tracks SBOMs across an
  organization. *License: Apache-2.0.*
- 📄 **SLSA — Supply-chain Levels for Software Artifacts** — [slsa.dev](https://slsa.dev/).
  A leveled framework for build-pipeline integrity and artifact provenance — the
  structured answer to the SolarWinds-style attacks of §13.6.2. *License: spec on GitHub
  under Community Specification License; site content CC BY 4.0.*
- 📄 **CISA — Alert AA20-352A** (December 2020) —
  [cisa.gov](https://www.cisa.gov/news-events/cybersecurity-advisories/aa20-352a). The US
  government advisory on the SolarWinds compromise behind §13.6.2: malicious code inserted
  during the software build and signed with the vendor's legitimate code-signing
  certificate. *License: U.S. government work, public domain.*
- 📄 **npm — "kik, left-pad, and npm"** (March 2016) —
  [blog.npmjs.org](https://blog.npmjs.org/post/141577284765/kik-left-pad-and-npm). The
  registry's own account of §13.6.2's left-pad unpublication and the breakage that
  followed; The Register's contemporaneous report prints the eleven-line package in
  full — [theregister.com](https://www.theregister.com/2016/03/23/npm_left_pad_chaos/).
  *Access: both free to read.*

## Legacy code, refactoring, and technical debt

- 📘 **Martin Fowler — "StranglerFigApplication"** —
  [martinfowler.com/bliki/StranglerFigApplication.html](https://martinfowler.com/bliki/StranglerFigApplication.html).
  The original naming of §13.8.5's incremental-replacement pattern, with the fig-tree
  metaphor from its source. *Access: free to read.*
- 📘 **Refactoring catalog** — [refactoring.com/catalog](https://refactoring.com/catalog/)
  (Fowler's official catalog of named moves and mechanics) and
  [refactoring.guru](https://refactoring.guru/refactoring) (a free-to-read tutorial
  treatment with examples). The named, small, behavior-preserving steps of §13.8.3.
  *Access: both free to read online; the full Refactoring book is commercial.*
- 📄 **Ward Cunningham — "The WyCash Portfolio Management System"** (OOPSLA 1992
  experience report) — widely mirrored, e.g. via
  [c2.com](http://c2.com/doc/oopsla92.html). The four-paragraph origin of the
  technical-debt metaphor (§13.8.4), worth reading to see how much the original meaning —
  debt as *deliberate*, to be repaid with refactoring — matches this chapter's framing.
  *Access: free on the author's site.*
- 📄 **Robert L. Glass — "Frequently Forgotten Fundamental Facts about Software
  Engineering"** (IEEE Software, 2001) —
  [doi.org](https://doi.org/10.1109/MS.2001.922739). Source for §13.8's maintenance-cost
  figure: maintenance typically consumes 40 to 80 percent (60 percent average) of software
  costs. *Access: paywalled at IEEE; widely assigned in courses, and author copies
  circulate.*
- 📘 **Michael Feathers — *Working Effectively with Legacy Code*** (Prentice Hall, 2004) —
  [informit.com](https://www.informit.com/store/working-effectively-with-legacy-code-9780131177055).
  The source of §13.8.1's tests-first definition of legacy code and the
  edit-and-pray/cover-and-modify distinction. *Not* openly licensed — listed here as the
  standard citation.

## License note

Linked resources remain under their own licenses (noted above where known); this page is
licensed **CC BY‑SA 4.0**.
