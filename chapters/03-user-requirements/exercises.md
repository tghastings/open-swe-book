# Chapter 3 — Exercises

Exercises are graded by depth: **[warm‑up]** checks understanding, **[analysis]** asks
you to reason.

## Concepts

1. **[warm‑up]** In your own words, distinguish a *functional requirement* from a *quality
   (non-functional) requirement*. Write one of each for a photo-sharing app, and give the
   quality requirement a *measurable fit criterion*.
2. **[warm‑up]** Name the four stages of the requirements cycle and, in one sentence each,
   say what goes wrong if a team skips that stage.
3. **[warm‑up]** Classify each of the following as a *stated*, *implied*, or *latent* need
   for a food-delivery app, and justify the label: (a) "let me track the driver on a map,"
   (b) "don't show me restaurants that are closed," (c) "reorder my usual meal in one tap
   before I even open the menu."
4. **[warm‑up]** Rewrite this vague requirement into a testable one: "The search should be
   fast." State what extra information you had to invent, and why each piece matters.

## Analysis

5. **[analysis]** Take a real need you have with some app you use and write it as a
   Connextra user story (*as a…I want…so that*). Then check it against all six INVEST
   letters, and for any letter it fails, describe the specific fix (split it, add acceptance
   criteria, schedule a spike, etc.).
6. **[analysis]** A teammate says "agile means we don't need to write requirements." Using
   §3.2, write a two-paragraph rebuttal that explains what agile teams actually do with
   requirements and *why* deferring detail to "the last responsible moment" is a feature,
   not laziness.
7. **[analysis]** Interviews and observation reach different kinds of needs. Describe a
   concrete situation where an interview would *mislead* you but observing the real task
   would reveal the truth, and explain the human reason for the gap.
8. **[analysis]** Pick a feature you consider a *delighter* in a product you love. Argue how
   it will eventually decay into a *must-be* expectation, and what that implies for a team
   that stops eliciting needs after version 1.
9. **[analysis]** Take the medical check-in scenario in §3.5.2 and write one *new* exception
   branch that the chapter did not cover. Then list the specific requirement(s) — including
   at least one quality requirement — that your exception uncovers.
10. **[analysis]** Sketch a small goal hierarchy (root goal, two sub-goals, three or four
    leaf features) for a bike-share app. Then identify one pair of *conflicting* goals and
    one pair of *contributing* goals, and write the one-sentence trade-off decision a
    stakeholder would need to record for the conflict.
11. **[analysis]** Build a three-level attack tree for the goal "post a message as another
    user" on a social app. Use at least three STRIDE categories to find branches, then turn
    two leaves into concrete security requirements, naming the attack each one defeats.
12. **[analysis]** A team's backlog holds three *Must* stories (`ST-4` flag interpreter,
    `ST-9` cancel appointment, `ST-11` print day schedule). Their repo has feature files
    for `ST-4` and `ST-11`, a passing scenario for a story `ST-2` that no longer exists,
    and recent commit messages `"fix cancel flow"` and `"ST-11 print header"`. Using
    §3.4.4, list every traceability gap you can find (forward and backward), and state
    the one-line repair for each.
