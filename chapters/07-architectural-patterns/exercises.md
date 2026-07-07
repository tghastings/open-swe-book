# Chapter 7 — Exercises

Exercises are graded by depth: **[warm-up]** checks understanding, **[analysis]** asks you
to reason about a design and its trade-offs. For every pattern you choose, the grading rubric is
the same one an engineer applies in practice: *name what the pattern buys you and what it
costs you.*

## Concepts

1. **[warm-up]** In one sentence each, state the *problem* solved by the layered pattern,
   the observer pattern, and the client-server pattern. Then name the single quality each
   one is primarily trying to protect (for example, substitutability, or shared truth).

2. **[warm-up]** Explain the difference between *strict* and *relaxed* layering. Give one
   concrete situation where you would accept the pass-through cost of strict layering, and
   one where relaxed layering is the better call, and say why.

3. **[warm-up]** The observer pattern "inverts a dependency." Which object would depend on
   which in the naive (non-observer) design, and which way does the dependency point after
   you apply the observer? Draw the two arrows.

4. **[warm-up]** MVC insists that "the model does not depend on the view." Give one
   concrete benefit you lose the moment a business rule leaks into a view, and connect it
   to the humble-view principle from §7.3.3.

## Analysis

5. **[analysis]** A colleague proposes storing all shared application state in one central
   store that every component reads and writes (the shared-data pattern). List two specific
   ways this will help the team as the app grows, and two specific ways it will hurt.
   Propose one design change that keeps most of the benefit while reducing the biggest risk.

6. **[analysis]** You are asked to add "email the customer whenever an order ships" to a
   system, and you expect more such notifications (SMS, push, webhook) to be requested
   soon. Compare two designs: (a) a direct call from the shipping code to the email code,
   and (b) an observer/publish-subscribe design where shipping emits an event. Argue which
   you would choose *today* and how your answer changes if only the email notification will
   ever exist.

7. **[analysis]** Take the Unix pipeline

   ```bash
   cat log | grep ERROR | sort | uniq -c
   ```

   Identify the filters and the pipes. Then describe one transformation that the
   pipes-and-filters structure makes *easy* (give the new pipeline) and one requirement
   that this structure makes *awkward*, explaining why the awkwardness is inherent to the
   pattern rather than to Unix. A fifteen-line sample log to experiment on lives at
   [`code/ch07/data/access.log`](../../code/ch07/data/access.log) — its interesting lines
   say `404` rather than `ERROR`, so adjust the `grep`.

8. **[analysis]** A batch report currently runs every night over a file of the day's
   transactions. Product now wants results "within ten seconds of each transaction."
   Explain, using §7.4.3, three specific design problems that switching from a bounded file
   to an unbounded stream forces you to confront that the nightly batch could ignore.

9. **[analysis]** Your mobile app talks to a payment provider's server over a documented
   HTTP protocol. Explain how the client-server structure lets you test the app's behavior
   for a *declined card* and a *server timeout* without ever touching the real provider.
   Then state one class of bug this test-server approach *cannot* catch, and what kind of
   test (Chapter 10) you would add to cover it.

10. **[analysis]** A team is splitting a monolith into many services and debating whether to
    let services call each other directly or route all calls through a broker. Give the two
    strongest arguments for the broker and the two strongest against. Under what growth
    conditions does the broker become worth its cost?

## Choosing a pattern

For each scenario, choose the *most appropriate* pattern (or small combination) from this
chapter, sketch its structure in two or three sentences, and — this is the graded part —
justify the choice by naming what you buy and what you pay. There is often more than one
defensible answer; the justification is what matters.

11. **[analysis]** A data-science team must process 40 terabytes of clickstream logs
    overnight to compute per-user visit counts. The job is embarrassingly parallel per
    record, then aggregated by user. Pick a pattern, and explain what the framework does for
    you and where your main cost will be.

12. **[analysis]** A desktop drawing program shows the same shapes in a canvas, a
    layers-list sidebar, and a properties panel; editing any one must instantly update the
    others. Pick a pattern (or combination), show the wiring, and explain how it keeps the
    three displays consistent without any of them knowing about the others.
