# Chapter 13 — Exercises

Tags: **[warm‑up]** checks understanding · **[analysis]** asks you to reason.

## Concepts

1. **[warm‑up]** In your own words, restate the distinction between *essential* and
   *accidental* complexity (Chapter 1) and give one software task at each end that AI
   handles well or poorly. Why does the boundary predict where AI helps?
2. **[warm‑up]** Name the five rungs of the "ladder of assistance" (§13.1.3). For each,
   state one thing the *human* must still do.
3. **[warm‑up]** What is the **oracle problem**, and why does it limit AI-generated tests
   even when coverage numbers look high?

## Analysis

4. **[analysis]** The 2025 METR trial found experienced developers were ~19% *slower* with
   AI while believing they were faster. Give two plausible mechanisms for the gap, and
   describe an experiment (using Chapter 12 methods) you could run on your own team to
   measure *your* real speedup instead of trusting the feeling.
5. **[analysis]** Pick any three lifecycle stages from §13.2. For each, write one sentence
   on what AI does well and one on the specific fundamental a human still owns. Cite the
   chapter each maps to.
6. **[analysis]** §13.2.6 says AI "inverts" the code-review problem. Explain the inversion,
   and propose two concrete team policies that keep reviewer trust (Chapter 9) from eroding
   when most code under review is machine-generated.
7. **[analysis]** The security evidence (§13.3) shows users of AI assistants writing *less*
   secure code while feeling *more* secure. Which cognitive bias from Chapter 4 does this
   resemble, and what process safeguard would you add?

## The o16g manifesto

8. **[analysis]** Map any **five** of the sixteen o16g principles to specific chapters of
   this book, and for each say whether it *restates* an existing discipline or proposes
   something genuinely new.
9. **[analysis]** The manifesto declares "The Backlog is Dead — manage to cost, not
   capacity." Argue *for* and *against* this claim using Chapter 4's prioritization tools.
   Under what conditions does it hold?
10. **[analysis]** Principle 16 ("Audit the Outcomes") depends on human expertise, yet heavy
    reliance on agents may erode that expertise (the *deskilling* risk). Explain the tension
    and propose how a team could stay able to audit what its agents produce.
11. **[analysis]** "Certainty, not vibes" is the manifesto's verification slogan. Give one
    kind of outcome that is cheap to verify automatically and one that is expensive or
    impossible, and connect the second to the oracle problem.

## Agentic practice

12. **[warm‑up]** State the "inversion" at the heart of spec-driven development (§13.5) in
    one sentence. Which two chapters supply the skills the *Specify* phase depends on?
13. **[warm‑up]** Name the five moves a loop makes each turn (§13.7.1). For each, name the
    anti-pattern that appears when it is skipped.
14. **[analysis]** Write a first-draft `AGENTS.md` (about 10–15 lines) for your team project
    (Appendix A). Then justify each line against the §13.6 tests: does it materially change a
    decision, or could the agent infer it by reading the code? Delete anything that fails.
15. **[analysis]** §13.7.2 argues the agent that wrote the code is the worst judge of it, and
    the fix is a *separate* evaluator that defaults to "no." Explain why this is the same
    problem as the oracle problem (§13.2.7), and why swapping in a different model or agent
    helps where "asking the author to be more critical" does not.
16. **[analysis]** Pick two of the four silent costs of a running loop (§13.7.3) —
    verification debt, comprehension rot, cognitive surrender, token blowout. For each,
    describe a concrete symptom you would expect to see first, and the specific discipline
    (from this book) that guards against it.
17. **[analysis]** Stripe's "Minions" ship ~1,300 PRs a week on a fork of a mid-tier
    open-source harness, not a frontier model (§13.7.3). Explain, using the five moves, where
    that pipeline's reliability actually comes from — and why "use a bigger model" would not
    have produced it.
18. **[analysis]** §13.6 argues that an `AGENTS.md` ports *facts* between tools but not *tone*
    — Anthropic documents `IMPORTANT`/`YOU MUST` emphasis as a lever, while OpenAI's Codex
    guide stresses verifiable, decomposed instructions instead. Take one rule from your team's
    `AGENTS.md` and rewrite it two ways: once emphasis-first, once rationale-first ("do X
    *because* Y"). Which version would you expect to survive being read by a *different* agent
    than the one you wrote it for, and why?
