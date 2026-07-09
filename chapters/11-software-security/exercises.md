# Chapter 11 — Exercises

Exercises are graded by depth: **[warm‑up]** checks understanding, **[analysis]** asks
you to reason. Several exercises require *actual work* — running a scanner, reading a primary
source, scoring a real package — not just prose. Show the work, not only the answer.

## Concepts

1. **[warm‑up]** Define *threat*, *vulnerability*, and *exploit* in one sentence each, then
   classify these three items as one of the three: a missing authorization check on an admin
   endpoint; a competitor who wants your customer list; a script that dumps that list by calling
   the unprotected endpoint (§11.1).

2. **[warm‑up]** Name the OWASP Top 10:2025 category that best fits each of these, and justify in
   one clause: (a) a URL parameter `?userId=1043` that any logged-in user can change to read another
   patient's record; (b) a search box that runs `SELECT … WHERE name = '` + input + `'`; (c) a
   password-reset flow that emails a token but never expires it (§11.2).

3. **[warm‑up]** In one sentence each, distinguish **SAST**, **DAST**, and **SCA**, and say which of
   the three would have had the best chance of flagging the Log4Shell dependency *before* it was
   exploited (§11.3, §11.4).

4. **[warm‑up]** Explain "shift left" to a teammate who thinks security is the penetration test the
   week before launch. Give one concrete practice from an *earlier* phase that catches a class of
   defect the pen test would miss (§11.1).

## Analysis

5. **[analysis]** Take the injection example from §11.2 and, in your project's language, write both
   versions: the string-concatenated query and the parameterized query. Then write one input that
   returns every row from the vulnerable version, and confirm the same input is harmless against the
   parameterized one. Submit the two queries, the malicious input, and one sentence on *why* the
   parameterized version is safe.

6. **[analysis]** Run **OpenSSF Scorecard** (or read its published report) against one open-source
   dependency your project actually uses. Report its aggregate score and the two lowest-scoring
   checks. Then argue, in a paragraph, whether that score alone would tell you the package is safe to
   adopt — and what the six-control framework of §11.4 would add that the score does not (§11.4).

7. **[analysis]** Read Andres Freund's original oss-security disclosure of the xz-utils backdoor
   (linked in Open Resources). In your own words, identify the *human* weak link the attack exploited
   and name which of the dissertation's six controls (C1–C6), if any, would plausibly have caught it
   — and which would not, and why. This is the point of the case study: some attacks are social, not
   technical (§11.4).

8. **[analysis]** Pick one package your project depends on and walk it through the Day 0 controls
   (C1–C4) from §11.4: does it have known CVEs; who maintains it and how recently; is it signed;
   does it have branch protection? Assign it Low / Medium / High risk and state the Time-to-Repair
   band that implies. You do not need every answer to be perfect — the exercise is learning to *ask*
   the four questions before you type `install` (§11.4).

9. **[analysis]** AI pentest tools such as Strix validate findings by building a working
   proof-of-concept. Explain why that validation step matters more for an *autonomous* tool than for
   a human tester, and describe one situation in which running such a tool would be unethical or
   illegal even though it is technically easy (§11.3). Ground your answer in the authorization
   principle, not vibes.

10. **[analysis]** Choose one OWASP Top 10:2025 category and write a single **quality-attribute
    scenario** (§6.1.4) for it: the stimulus (an attacker's action), the environment, the response
    your system should make, and a measurable response criterion. This is how a vague "be secure"
    becomes something you can design toward and test (§11.1, §6.1.4).
