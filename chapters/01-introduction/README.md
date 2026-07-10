# Chapter 1 — Introduction

> **Where we are.** This opening chapter introduces the ideas that thread through the book.
These include the definition of software engineering, the challenges associated with requirements,
the inherent complexity of software, the inevitability of defects, and the trade-offs among project
scope, cost, and time. Additionally, the chapter addresses the importance of social responsibility
for software professionals. Subsequent chapters each address one or more of these foundational challenges.

Writing a program that works once, on your machine, for input you chose yourself, is
programming. **Software engineering** is what you need when *other people* depend on
that program — when it must keep working next year, after five other developers have
changed it, on inputs no one anticipated, at a scale no single person can hold in their
head. Understanding the gap between those two activities is the subject of this book.

## 1.1 What Is Software Engineering?

### 1.1.1 A Working Definition

> **Definition.** *Software engineering* is the disciplined application of principles,
> methods, and tools to build and evolve software systems that are useful, correct
> enough, and economical to change — usually by a **team**, usually under **changing
> requirements**, usually at a **scale** that defeats ad-hoc effort.

Three words in that definition carry a lot of weight:

- **Team.** Most real software — and nearly all software at commercial scale — is built
  by groups. Coordination, communication, and shared understanding become first-class
  engineering concerns, not afterthoughts.
  This is why Chapter 2 is about *process* and why an entire team project runs alongside
  the concepts (Appendix A).
- **Changing.** Requirements are discovered, not handed down. They shift as users learn
  what they actually want. Methods that assume a frozen specification tend to fail; this
  is why the industry moved toward *iterative, agile* methods (Chapters 2–4).
- **Scale.** Beyond a few tens of thousands of lines, hardly anyone understands the whole
  system in detail. We manage that with **design and architecture** (Chapters 6–7):
  dividing the system so each part can be understood, changed, and tested in relative
  isolation.

What separates software engineering from mere coding is the focus on the **why**
behind the **how**. Any competent developer can be told "use dependency injection here."
An engineer understands *what problem it solves* (coupling), *when it helps*, and *when
it is overkill* along with the trade-offs — and can make the call on a design they have never
seen before.

### 1.1.2 A Tale of Two Companies

Consider two startups building the same product — a scheduling app for clinics.

**Company A** hires strong programmers and tells them to "just ship." They skip written
requirements ("we all know what a calendar does"), skip tests ("we'll test by using
it"), and let the architecture emerge by accretion. For three months they look *faster*
than anyone: demos appear weekly. Then the trouble starts. A change to time-zone
handling breaks appointment reminders in a way no one notices for two weeks. Onboarding
a fourth engineer takes a month because only one person understands the booking logic.
Every new feature has a chance of resurrecting an old bug. Velocity collapses under the
weight of the system's own complexity.

**Company B** spends the first two weeks talking to clinic staff, writing a handful of
user stories, sketching a modular architecture, and setting up automated tests and code
review. Their first demo comes a week later than Company A's. But by the third month
the two teams look nothing alike: new engineers are productive in days, changes are
localized, and a failing test usually catches a regression before it reaches a user.

Neither team is smarter. The difference is **engineering discipline**: Company B paid a
small, early, *predictable* cost to avoid a large, late, *unpredictable* one. The rest
of this book is, in effect, a catalog of the disciplines that make a team behave like
Company B — and an honest account of when each is worth its cost.

### 1.1.3 Where the Discipline Came From

The phrase "software engineering" owes its early currency to practitioners, not to a
standards committee. In the 1960s, **Margaret Hamilton** led the team at the MIT
Instrumentation Laboratory that wrote the flight software for the **Apollo Guidance
Computer** — the code that flew astronauts to the Moon.[^1] At the time, programming was
widely seen as a clerical afterthought to the "real" engineering of hardware. Hamilton
pushed the term **software engineering** into use deliberately, to insist that building
flight software deserved — and required — the same rigor and respect as the aerospace
engineering around it.[^2]

Her team's discipline paid off in the most public way imaginable. Minutes before the
Apollo 11 lunar landing, the guidance computer was flooded with unexpected input and
began running out of capacity, throwing alarms. Because the software had been engineered
with **priority scheduling** — the ability to shed low-priority work and keep the tasks
that mattered most for landing — it recovered instead of crashing, and the landing
proceeded.[^3] A design decision made long before launch, against a failure no one could
fully predict, saved the mission. It remains one of the clearest early demonstrations of
what disciplined software design can do for a project.

The rest of the industry was learning similar lessons. Through the 1960s,
hardware performance improved on the exponential curves we now describe with Moore's
Law,[^4] while large software projects ran chronically late, blew their budgets, and failed
outright in mission-critical settings — defense, aerospace, banking. Software, not
hardware, had become the bottleneck. In 1968, a NATO-sponsored conference in Garmisch,
Germany gave the problem a name — the **software crisis** — and proposed a remedy in its
very title: the *NATO Software Engineering* conference argued that software should be
developed like an engineering discipline, with deliberate methods, rather than by ad-hoc
programming and heroics.[^5]

What ultimately answered the crisis, though, was not a fixed body of rules like a
building code. Software turned out to be too changeable for that. The discipline's
mature answer is **empiricism**: work like an experimental scientist. Iterate in small
steps, seek fast **feedback**, prefer **incremental** progress you can evaluate, run
**experiments** when you are unsure, and let measured evidence — not opinion or
authority — settle the argument. Modern writers such as Dave Farley frame the effective
software engineer as this kind of scientist.[^6] Keep that framing in mind
in Chapter 2: every process you will learn about there — Scrum's sprints, XP's tests, the
spiral's risk-driven loops — is an institutionalized version of the same iterate,
measure, and adjust cycle.

## 1.2 The Requirements Challenge

The hardest part of many projects is not building the system right, but figuring out
**which system to build**. Fred Brooks, the author of *The Mythical Man-Month*,
famously argued that the hardest single part of software work is deciding precisely
what to build, because it is the one part whose mistakes most cripple the result and
are hardest to fix later.[^7]

### 1.2.1 Identifying Users and Requirements

A **requirement** is a statement of something the software must do or a quality it must
have. The catch is that the people who *have* the need are usually not the people who
*build* the software, and they rarely state the need precisely. Users describe
solutions ("add a dropdown here") when what they have is a *problem* ("I can't tell
which appointments are unconfirmed"). Part of the engineer's job is to dig past the
requested solution to the underlying problem.

Requirements also come from more than the obvious end user. A clinic scheduling app has:

- **End users** (front-desk staff) who book appointments,
- **Secondary users** (clinicians) who view schedules,
- **Sponsors** who pay and care about cost and compliance,
- **Regulators** whose rules (privacy, accessibility) are non-negotiable constraints.

Chapter 3 gives concrete techniques — user stories, features, scenarios, and goal
hierarchies — for eliciting and recording what all of these stakeholders actually need.

### 1.2.2 Dealing with Requirements Changes

Requirements *change*, and this is normal, not a failure. Users learn from early
versions; markets move; regulations update. The engineering question is not "how do we
prevent change?" but "how do we build so that change is cheap?"

Two broad answers appear throughout the book:

1. **Process-level:** work in short iterations so that less new work accumulates before
   feedback arrives, limiting the likelihood and extent of rework and keeping the team
   aligned with its *latest* understanding rather than a stale specification (Chapter 2).
2. **Design-level:** structure the system so that a likely change touches one module,
   not twenty (Chapter 6).

> **Principle.** The cost of a change should be proportional to the *size* of the
> change, not to the *size* of the system. Achieving that is the central goal of good
> process and good architecture alike.

## 1.3 Software Is Intrinsically Complex

### 1.3.1 Sources of Complexity

Some complexity is **essential** — it is inherent in the problem. A tax-preparation
program is complicated because tax law is complicated; no cleverness removes that.
Other complexity is **accidental** — it comes from our tools, our choices, and our
mistakes: tangled dependencies, unclear names, duplicated logic, leaky abstractions.[^7]

Good engineering cannot eliminate essential complexity, but it relentlessly attacks
accidental complexity. Much of this book is about that: clear requirements and
specifications (Chapters 3–5), design and patterns that package proven solutions
(Chapters 6–7), reviews that catch needless complication (Chapter 9).

Software is also unusually complex among engineered artifacts for structural reasons:

- It is **invisible** — you cannot see its shape, so you rely on models and diagrams.[^7]
- It is **discrete** — a one-character change can flip behavior completely; there is no
  "small error → small effect" safety net that continuous physical systems enjoy.
- It is **changed constantly** — a bridge is designed once; software is redesigned every
  sprint.

### 1.3.2 Architecture: Dealing with Program Complexity

The primary weapon against complexity is **decomposition**: split the system into parts
small enough to understand, with **well-defined interfaces** between them, so that you
can reason about one part without holding the others in your head. When the parts and
their connections are chosen deliberately, we call the result the system's
**architecture** (Chapters 6–7).

```mermaid
flowchart TD
    A[Complex system] -->|decompose| B[Module 1]
    A --> C[Module 2]
    A --> D[Module 3]
    B <-->|narrow, explicit interface| C
    C <-->|narrow, explicit interface| D
    classDef m fill:#eef,stroke:#66a,color:#000;
    class B,C,D m;
```

A good decomposition has **high cohesion** (each module does one thing well) and **low
coupling** (modules depend on each other as little as possible, and only through their
interfaces). These two ideas — introduced here, developed in Chapter 6 — are perhaps the
most important in all of software design.

## 1.4 Defects Are Inevitable

Humans make mistakes; therefore software has defects. The engineering response is to
accept this and build **multiple, overlapping** nets that catch defects early,
when they are cheap to fix.

### 1.4.1 Fix Faults to Avoid Failures

It helps to separate three ideas that everyday speech blurs into "bug":

- A **mistake** (or *error*) is a human action that produces an incorrect result — a
  developer misreads a spec.
- A **fault** (the "defect" in the code) is the resulting flaw in the software — an
  off-by-one in a loop.
- A **failure** is the observable event when the running system deviates from correct
  behavior — the report prints the wrong total.

A fault is *latent* until some execution triggers it into a failure. This chain —
mistake → fault → failure — explains why we attack defects at every stage: better
requirements and reviews reduce **mistakes**; static checking and inspection find
**faults** before they run; testing provokes **failures** in a safe setting before users
do. No single technique suffices, which is why Chapters 9 and 10 are complementary.

### 1.4.2 Introduction to Testing

**Testing** runs the software on chosen inputs and checks the outputs against what we
expect. It cannot prove the absence of defects — as Dijkstra, a pioneer in computing
and mathematics, observed, testing shows the *presence* of bugs, never their absence[^8] —
but a well-designed test suite makes it *unlikely* that a serious fault survives, and
it makes change safe by catching regressions. Testing is important enough that Chapter 10
is devoted to it, including how to decide when you have tested *enough* (coverage).

### 1.4.3 Black-Box and White-Box Testing

Two complementary viewpoints run through all of testing:

- **Black-box (specification-based)** testing chooses inputs from the *specification*,
  ignoring the code. You test *what the system should do*: valid and invalid inputs,
  boundaries, and equivalence classes of behavior. Its strength is that it finds *missing*
  logic and stays valid when the code is rewritten.
- **White-box (structure-based)** testing chooses inputs by looking at the *code*,
  aiming to exercise its statements, branches, and paths. Its strength is finding code
  that the specification-based tests never reach.

Neither subsumes the other, and Chapter 10 shows how to combine them and how to *measure*
their thoroughness with coverage criteria.

## 1.5 Balancing Constraints: The Iron Triangle

Every project runs under three linked constraints:

- **Scope** — how much it does (features, quality).
- **Cost** — how much effort/money it consumes.
- **Time** — when it must ship.

```mermaid
flowchart TD
    S[Scope] --- C[Cost]
    C --- T[Time]
    T --- S
```

### 1.5.1 Scope. Cost. Time. Pick Any Two!

These constraints are coupled: you cannot freely fix all three. Want more **scope** at
the same **time**? Pay more **cost** (people, tools). Want to ship sooner without more
cost? Cut **scope**. The classic quip — *"good, fast, cheap: pick two"* — captures the
reality that **quality is not free**, and that a manager who demands more scope, sooner,
for less is mistaking innumeracy for ambition.

Agile methods make a deliberate choice here: they **fix time and cost** (a fixed-length
iteration with a fixed team) and let **scope flex** — the aim is to ship *something* valuable
on the date, even if not everything. Plan-driven methods more often fix scope and flex
time. Chapters 2 and 4 return to this trade-off with concrete estimation and
prioritization techniques (story points, MoSCoW, value/cost/risk). And modern software
increasingly ships as a **continuously updated service** rather than a boxed product —
Chapter 14 examines how that reshapes the triangle, when releasing becomes a routine
decision instead of a once-a-year event.

> **Pitfall.** Silently absorbing a scope increase by working nights ("crunch") hides
> the trade-off instead of resolving it. It borrows against future quality — the debt is
> repaid, with interest, as defects and burnout.

## 1.6 Social Responsibility

Software runs medical devices, cars, elections, and financial systems. Engineering
decisions are therefore **ethical** decisions, and "I was just implementing the spec" is
not a defense. This section grounds that claim in three cases.

### 1.6.1 Case Study: The Volkswagen Emissions Scandal

In 2015, regulators discovered that Volkswagen diesel vehicles contained a **defeat
device**: software that detected when the car was being emissions-tested (from steering,
speed, and time patterns) and switched to a cleaner, lower-performance mode *only during
the test*. On the road, the cars emitted many times the legal limit of nitrogen oxides.[^9]

The software worked *exactly as designed* — and that is the problem. This was no mere testing failure — it was a *requirement* that should never have
been implemented. Engineers wrote that code. The lesson: **correctness is not the same
as rightness.** A professional must sometimes refuse to build what they are asked to
build.

### 1.6.2 The ACM Code

The profession has written norms. The **ACM Code of Ethics and Professional Conduct**
and the joint **ACM/IEEE-CS Software Engineering Code of Ethics** state, among other
principles, that software engineers shall act in the **public interest**, produce work of
**high quality**, be **honest** about their work and its limitations, and maintain
**competence**.[^10] [^11] These are not decoration: they give an engineer a shared, citable basis
for saying *no*, and for raising concerns without it being merely personal opinion.

### 1.6.3 Case Study: The Therac-25 Accidents

Between 1985 and 1987, a radiation-therapy machine, the **Therac-25**, delivered
massive radiation overdoses to at least six patients, several fatally.[^12] The causes were
a textbook of engineering failures: a **race condition** in concurrent control software
that surfaced only when an operator typed quickly; **removal of the hardware interlocks**
that earlier models used as a safety backstop, leaving software as the sole safeguard;
**reused code** never designed for this configuration; misleading error messages; and a
development culture that assumed the software was correct and dismissed early field
reports.[^12]

The Therac-25 is the canonical warning that in safety-critical systems, software defects
kill, and that **process, testing, and honest incident response are matters of life and
death** — not bureaucratic overhead.

### 1.6.4 Lessons for Software Projects

Across these cases, recurring lessons:

1. **Build the right thing, not just the thing right** — question requirements that harm
   users or the public.
2. **Don't rely on a single safeguard** — defense in depth (interlocks *and* software
   checks; reviews *and* tests).
3. **Take field reports seriously** — a dismissed anomaly is a failure waiting to recur.
4. **Concurrency and reuse are risk multipliers** — treat them with extra rigor.
5. **You are accountable for what you ship**, regardless of who asked for it.

## 1.7 Conclusion

Software engineering exists because software is built by teams, for changing needs, at a
scale and complexity that defeat improvisation, with defects that are inevitable and
sometimes dangerous. The rest of this book is organized as a set of responses to exactly
those pressures:

- **Process** (Ch. 2) coordinates the team and embraces change.
- **Requirements** (Ch. 3–5) discover and pin down *what to build*.
- **Design and architecture** (Ch. 6–7) tame complexity so change stays cheap.
- **Version control** (Ch. 8) gives every change a name, a history, and an owner — the
  substrate every later discipline builds on.
- **Static checking and testing** (Ch. 9–10) catch the inevitable defects early.
- **Security** (Ch. 11) makes the software resist attack, from the code to the supply chain it is built from.
- **Metrics** (Ch. 12) tell us, with evidence rather than opinion, how we are doing.
- **AI across the lifecycle** (Ch. 13) re-examines every one of those disciplines as
  coding agents take over more of the typing.
- **Delivery** (Ch. 14) carries a verified change the last mile, into production, safely.
- **Maintenance and evolution** (Ch. 15) keep the system alive and changeable through the
  years after launch — where most engineering effort actually goes.
- **A team project** (Appendix A) puts it all into practice.

A word about the code you will meet along the way. Concepts come first in this book and
code second, but from Chapter 2 onward nearly every code-shaped idea is also shown as a
short, runnable example — and each example appears in six languages — **Python, Java,
JavaScript, Go, Ruby, and TypeScript** — plus a language-agnostic **Generic** tab written
in pseudocode, for when you want the idea without any one language's syntax. They sit
behind a row of tabs. Pick your language once and every
example on every page follows; you can also open any page with [`?lang=go`](?lang=go)
(or [`java`](?lang=java), [`javascript`](?lang=javascript), [`python`](?lang=python),
[`ruby`](?lang=ruby), [`typescript`](?lang=typescript), [`generic`](?lang=generic)) to pre-select one.
The tabs run alphabetically, so **Generic** leads the row; the **Ruby** tab is selected by
default until you pick another — and the examples are written to read cleanly even in a
language you have never used.

The others are worth your attention even so, because some lessons only appear in the
contrast: information hiding looks different as a Java interface, a Go implicit
interface, Ruby duck typing, and a TypeScript `interface`; the same unit tests read
differently in pytest, JUnit, `node:test`, `go test`, and Minitest — and each difference says something about
the language's design. Every snippet is a real program, kept as a runnable file with a
test in the book's repository and exercised by continuous integration, so the examples
cannot silently rot. And when an example is *supposed* to fail — a type fault the
compiler rejects in Chapter 9 — the error message printed beside it is the compiler's
actual output, not a paraphrase.

Keep the four cross-cutting principles in view as you read: *software is complex;
requirements change; defects are inevitable; teams need coordination.* Nearly every
technique in this book earns its place by answering one of them.

---

### Sources

[^1]: NASA, *Margaret Hamilton* (NASA Science biography, n.d.). [science.nasa.gov](https://science.nasa.gov/people/margaret-hamilton/).

[^2]: IEEE Computer Society, *Margaret Hamilton: First Software Engineer* (2018). [computer.org](https://www.computer.org/publications/tech-news/events/what-to-know-about-the-scientist-who-invented-the-term-software-engineering).

[^3]: Don Eyles, *Tales from the Lunar Module Guidance Computer*, AAS paper 04-064, 27th AAS Guidance and Control Conference (2004). [doneyles.com](https://www.doneyles.com/LM/Tales.html).

[^4]: Gordon E. Moore, *Cramming More Components onto Integrated Circuits*, Electronics 38(8), 1965; reprinted in IEEE Solid-State Circuits Society Newsletter (2006). [doi.org](https://doi.org/10.1109/N-SSC.2006.4785860).

[^5]: Peter Naur & Brian Randell (eds.), *Software Engineering: Report on a Conference Sponsored by the NATO Science Committee, Garmisch, Germany, 7–11 Oct. 1968* (1969). [cs.ncl.ac.uk](http://homepages.cs.ncl.ac.uk/brian.randell/NATO/nato1968.PDF).

[^6]: David Farley, *Modern Software Engineering: Doing What Works to Build Better Software Faster* (Addison-Wesley, 2022). [informit.com](https://www.informit.com/store/modern-software-engineering-doing-what-works-to-build-9780137314911).

[^7]: Frederick P. Brooks, Jr., *No Silver Bullet: Essence and Accidents of Software Engineering*, Computer 20(4), pp. 10–19 (1987). [doi.org](https://doi.org/10.1109/MC.1987.1663532).

[^8]: Edsger W. Dijkstra, *Notes on Structured Programming*, EWD249, p. 7 (1970). [cs.utexas.edu](https://www.cs.utexas.edu/users/EWD/ewd02xx/EWD249.PDF).

[^9]: U.S. Environmental Protection Agency, *Notice of Violation to Volkswagen AG* (Sept. 18, 2015). [epa.gov](https://www.epa.gov/vw).

[^10]: ACM, *ACM Code of Ethics and Professional Conduct* (2018). [acm.org](https://www.acm.org/code-of-ethics).

[^11]: ACM/IEEE-CS Joint Task Force, *Software Engineering Code of Ethics and Professional Practice, v5.2* (1999). [computer.org](https://www.computer.org/education/code-of-ethics).

[^12]: Nancy G. Leveson & Clark S. Turner, *An Investigation of the Therac-25 Accidents*, Computer 26(7), pp. 18–41 (1993). [doi.org](https://doi.org/10.1109/MC.1993.274940).

---

- **Key takeaways** are summarized above in §1.7.
- Continue to the [Exercises](exercises.md).
- Go deeper with the [Open Resources](resources.md) for this chapter.
