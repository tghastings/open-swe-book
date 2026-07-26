# Appendix A — Project Exercises

Unlike the chapter exercises, these are **checkpoints** for a real team project. Work
them with your team, in order, across the term. Each maps to a deliverable in the
[course plans](../../curriculum/course-plan.md). Checkpoints are tagged **[team]**
(working agreements and people), **[project]** (deliverable artifacts), or
**[analysis]** (reflection).

## Weeks 1–2 — Team and idea

1. **[team]** Write a one-paragraph *team charter*: how you will communicate, how often
   you will meet, how you will make decisions, and how you will handle a member who
   falls behind. Commit it to your repository's README.
2. **[team]** Brainstorm five project ideas. For each, note the primary user and the one
   problem it solves. Pick one and write two sentences on why it is *feasible in a term*
   and *worth doing*.

## Weeks 3–4 — Proposal

3. **[project]** Fill in the [project proposal template](../../templates/project-proposal.md).
   Your backlog must use MoSCoW (Chapter 4) and contain at least one *Won't-have-this-time*
   item to prove you have scoped realistically.
4. **[analysis]** Identify your project's single riskiest assumption (technical, user, or
   team). Describe the cheapest experiment that would tell you within one week whether it
   holds.

## Weeks 5–7 — Skeletal system (Status Report 1)

5. **[project]** Build a *walking skeleton*: a thin slice that runs end-to-end through
   every architectural layer (Chapters 6–7) even if each part is trivial. Submit
   [Status Report 1](../../templates/status-report.md).
6. **[analysis]** Draw your system's architecture as it actually is now (not as planned),
   using a class or component diagram from Chapter 6. Note one place where reality already
   diverged from the proposal, and why.

## Weeks 8–11 — Viable system (Status Report 2)

7. **[project]** Reach a minimum viable product: the *Must-haves* work for a real user.
   Submit [Status Report 2](../../templates/status-report.md) with a test-coverage number
   (Chapter 10) and your current defect count (Chapter 12).
8. **[team]** Run one retrospective (Chapter 2). Record two things to keep doing and one
   concrete change. At the next checkpoint, report whether the change stuck.

## Weeks 12–15 — Final report and demo

9. **[project]** Complete the [final report](../../templates/final-report.md), including a
   quality-metrics section (Chapter 12): defect-removal efficiency, at least one chart of
   your project data, and a short *limitations* paragraph naming the threats to validity
   in your numbers — a semester project yields few, unevenly measured, non-independent
   observations, and saying so is part of the analysis. Descriptive statistics, trends,
   and honest raw counts are the expected level of rigor; add a confidence interval only
   if your data give you enough independent observations to justify one (§12.8), and say
   explicitly when they do not. A stated limitation earns more credit than pseudo-precision.
   If your pipeline history supports it, also report your five DORA delivery metrics
   (§14.7.4) from your deploy log — with the same limitations discipline.
10. **[analysis]** Write an honest *individual contribution* statement for each member,
    then a team retrospective: what would you do differently if you started over knowing
    what you know now? Tie at least three lessons back to specific chapters.
11. **[project]** Prepare a 5–8 minute demo that shows the system doing real work for its
    primary user — not a slideshow *about* the system, but the system itself.
12. **[analysis]** Score your repository with the repository scorecard from §A.6 at the
    start of this phase and again before the demo. Include both scorecards in your
    final report with a short account of what changed: which findings you fixed, which you
    decided not to fix and why, and which you refuted with evidence the tool could not see.
    A defended disagreement counts as much here as a fix.
