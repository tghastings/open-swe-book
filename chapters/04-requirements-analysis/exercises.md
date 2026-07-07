# Chapter 4 — Exercises

These exercises build the judgment behind requirements analysis: sizing work, forecasting
from data, and ranking by value, cost, and risk. Tags indicate the kind of effort:
**[warm-up]** checks understanding, **[analysis]** asks you to reason or compute. Several
exercises require real arithmetic — do the math, and show your work.

Throughout, we reuse the **clinic scheduling app** from Chapters 1 and 3.

## Concepts

1. **[warm-up]** For each vague requirement below, rewrite it so it passes the §4.1
   checklist — in particular, give it a concrete **acceptance test** and name at least one
   dependency.

   - "The app should be fast."
   - "Patients should get reminders."
   - "Reports should look professional."

   Then explain, in one sentence each, why the original wording could not be estimated.

2. **[warm-up]** A teammate says, "Let's just call one story point one day of work, so
   5 points = 5 days." Explain two concrete problems this creates, referring to
   *anchoring* (§4.2.1) and to the reason points are deliberately *relative* (§4.2.2).

3. **[warm-up]** Read this exchange:

   > **Lead:** "The export feature is trivial — maybe half a day?"
   > **Junior dev:** "Yeah, that sounds about right, half a day."

   Identify the cognitive bias at work, explain how Planning Poker's *private,
   simultaneous* voting (§4.3.1) would have prevented it, and describe what the junior dev
   *should* have done differently.

## Estimation and forecasting

4. **[analysis]** *Forecast from velocity.* Your team's completed points for the last four
   sprints were:

   > Sprint 1: **19** Sprint 2: **24** Sprint 3: **21** Sprint 4: **28**

   The remaining backlog totals **156 points**. Sprints are **two weeks** long.

   a. Compute the average velocity.
   b. Forecast the number of sprints remaining (round up) and the calendar weeks.
   c. Give an *optimistic* and a *pessimistic* forecast using the fastest and slowest of
      the four sprints, and state the completion range you would tell a sponsor.
   d. Mid-Sprint-5, the sponsor adds 30 points of new "must-have" work. Redo the
      most-likely forecast. In one sentence, explain what this shows about fixed-scope
      promises.

5. **[analysis]** At sprint's end, a 13-point story is "almost finished — just needs
   testing." Your teammate argues it should count as, say, 11 points toward velocity since
   it is nearly done. Explain why agile counts 90%-done as **0**, and how counting partial
   credit would corrupt the forecast in Exercise 4.

6. **[analysis]** *Run a Planning Poker round.* Below are the Round-1 cards four
   estimators played for the story *"Let patients reschedule their own appointment
   online."* The scale is 1, 2, 3, 5, 8, 13.

   > Cards: **3, 5, 5, 13**

   a. Which two estimators must explain their reasoning first, and why those two?
   b. Invent a *plausible* reason the 13-player saw that the others missed, and a
      *plausible* reason the 3-player was too low. (Hint: think about consent, conflicts,
      notifications.)
   c. Write a believable Round-2 result and the final consensus, in the style of the
      walkthrough in §4.3.1. Explain why the *conversation*, not the number, was the real
      output.

## Prioritization

7. **[analysis]** You have a fixed release date and can clearly not finish everything.
   Sort these into **Must / Should / Could / Won't-this-time**, and justify each placement
   in a sentence.

   - Book and cancel appointments
   - Detect scheduling conflicts
   - Dark-mode theme
   - HIPAA-compliant audit log of who viewed a record
   - Waitlist with automatic promotion when a slot opens
   - Multi-language interface

   Then explain why keeping *Musts* to roughly 60% of the effort (§4.4.1) protects your
   release date — what specifically goes wrong if 95% of the work is "Must"?

8. **[analysis]** Rank these features by **value ÷ cost** and give the build order. Show
   the ratio for each.

   | Feature              | Value (1–10) | Cost (pts) |
   |----------------------|-------------:|-----------:|
   | Waitlist auto-promote|            7 |          8 |
   | Conflict detection   |            9 |          4 |
   | Dark mode            |            3 |          2 |
   | Insurance-card scan  |            8 |         13 |

   Which feature has a high *raw* value (8) yet ranks **last**, and what does
   that teach about "build the flashiest thing first"?

9. **[analysis]** Take the same four features from Exercise 8 and add a **risk** rating
   (10 = most dangerous). The insurance-card scan needs an unfamiliar OCR service; the
   waitlist needs new notification plumbing.

   | Feature              | Value | Risk | Cost |
   |----------------------|------:|-----:|-----:|
   | Waitlist auto-promote|     7 |    6 |    8 |
   | Conflict detection   |     9 |    2 |    4 |
   | Dark mode            |     3 |    1 |    2 |
   | Insurance-card scan  |     8 |    9 |   13 |

   a. Compute the **weighted priority = (value + risk) ÷ cost** for each and give the new
      order.
   b. Which feature does the added risk term reward most, and why does the formula
      deliberately favor tackling risky work early (§4.4.3)?
   c. Argue for or against overriding the formula to build conflict detection first
      anyway.

10. **[analysis]** For each feature, decide its Kano category (**Must-be / Performance /
    Attractive / Indifferent**) and justify it using the functional/dysfunctional question
    pair (§4.5.1).

    - The displayed appointment time is correct.
    - Search returns results faster.
    - A one-tap "add to my phone's calendar" button.
    - The app's loading spinner is a custom animation.

    Then pick one **Attractive** feature you named and argue how it might *decay* into a
    Performance or Must-be feature over five years (§4.5.3).

## Effort models

11. **[analysis]** *COCOMO effort estimate.* Your team estimates the clinic app at
    **35 KLOC**. Using **Basic COCOMO**, compute the effort in person-months for:

    a. an **organic** project (a = 2.4, b = 1.05), and
    b. an **embedded** project (a = 3.6, b = 1.20).

    Show the arithmetic (you may use Effort = a × KLOC^b directly). Then:

    c. Explain the *ratio* between the two answers in terms of both *a* and *b*.
    d. The project actually grows to **70 KLOC**. Recompute the *organic* estimate and
       show that doubling the size raised effort by a factor of about **2.07**, not 2.0.
       Name the property of software this demonstrates (§4.6.1).

12. **[analysis]** *Triangulate three estimates.* For one real feature, you now have three
    independent estimates: Planning Poker says **8 points** (which, at your velocity of
    ~4 points/person-week, implies ~2 person-weeks); COCOMO, from a KLOC guess, says
    **3 person-weeks**; a senior developer's gut says **1 person-week**. They disagree
    by 3×.

    a. Rather than averaging them, what should you *do* with the disagreement (§4.6.2
       pitfall)?
    b. For each method, name one assumption that, if wrong, would explain its being an
       outlier.
    c. Which single method would you trust *most* once the team has run six sprints, and
       why?
