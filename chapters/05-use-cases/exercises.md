# Chapter 5 — Exercises

Exercises are graded by depth: **[warm‑up]** checks understanding, **[analysis]** asks
you to reason.

## Concepts

1. **[warm‑up]** Define *actor*, *primary actor*, and *supporting actor* in your own
   words. For the ATM example, name one of each and say what distinguishes the primary
   from the supporting one.
2. **[warm‑up]** Explain the difference between a *goal* and a *step*. Rewrite each of
   these as a proper goal (a result in the world, not a UI action): "click the Submit
   button," "scroll to the bottom of the terms," "log in."
3. **[warm‑up]** What is the *basic flow* (main success scenario), and why do you write it
   before any alternative flow? Give the one-sentence reason in terms of what the
   alternatives depend on.
4. **[warm‑up]** Match each condition to the right structure — *specific alternative*,
   *bounded alternative*, or *extension point*: (a) the user cancels at any screen; (b) the
   entered coupon code is expired; (c) an optional gift-wrap step offered only in December.

## Analysis

5. **[analysis]** Take the ATM step *"The Cardholder enters a PIN; the system validates it
   with the Bank Authorization System."* Rewrite it once *too abstractly* and once *too
   concretely* (leaking design), then explain in a sentence what each version costs you.
6. **[analysis]** A teammate's use case has a success postcondition but no failure
   postcondition. Using the ATM's "no money out without a matching debit" guarantee as a
   model, explain why the missing failure postcondition is a real defect, and write a
   failure postcondition for a use case *Transfer Funds Between Accounts*.
7. **[analysis]** You are told to model a shared *login* step used by five different use
   cases, and an optional *apply loyalty discount* step that only applies to members
   during a sale. Decide whether each should be an `«include»` or an `«extend»`, and
   justify each choice by naming which use case depends on which.
8. **[analysis]** Critique this use-case diagram decision: a colleague has drawn arrows
   between ovals to show that "Withdraw Cash" happens *before* "Print Receipt," with a
   labeled condition on the arrow. Explain what is wrong, and state where that ordering
   and condition information actually belongs.
9. **[analysis]** Convert this user story into a full use case using the template from
   §5.3.1: *"As a patron, I want to renew a borrowed library book online so that I can
   keep it longer without visiting the branch."* Include a primary actor, at least one
   supporting actor, preconditions, a numbered basic flow, at least two alternative flows
   (one specific, one bounded), and both success and failure postconditions.
10. **[analysis]** Write a use case from scratch for **"Book a Clinic Appointment"** by an
    online patient. Produce the actor–goal list first (Pass 1), then the basic flow
    (Pass 2), then at least three deviations from the happy path (Pass 3), labeling each
    as a specific alternative, a bounded alternative, or behavior attached at an
    extension point. Note explicitly which step each deviation branches from.
11. **[analysis]** Take your answer to Exercise 10 and identify one stretch of behavior it
    shares with a second plausible use case for the same clinic system (e.g., *Reschedule
    Appointment*). Factor that shared behavior into an `«include»`d use case, and show the
    single line that now replaces the shared steps in each includer.
