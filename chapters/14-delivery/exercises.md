# Chapter 14 — Exercises

Exercises are graded by depth: **[warm‑up]** checks understanding, **[analysis]** asks
you to reason. Several exercises require *actual work* — computing metrics
from a log, designing a rollout, writing a real test — not just prose. Show the work, not
only the answer.

## Concepts

1. **[warm‑up]** In one sentence each, distinguish *continuous integration*, *continuous
   delivery*, and *continuous deployment* (§14.2.1, §14.3.1). Then state which of the three
   a team practices if every green build produces a deployable artifact but a product
   manager clicks "release" once a week — and what single change would move them to the
   next level.

2. **[warm‑up]** Explain why horizontal scaling (§14.1.2) depends on the statelessness
   convention from §7.5.4. Give one concrete example of per-client state that would break
   "any server can answer any request," and one standard place to move it.

3. **[warm‑up]** A teammate says "we don't need rollback — we'll just fix forward, our
   pipeline is fast." Using §14.3.4, give one situation where roll-forward is genuinely the
   only option and one where an untested reliance on it would be dangerous.

4. **[warm‑up]** For each scanner family in §14.6 — SAST, DAST, SCA, secrets scanning —
   name the *earliest* pipeline stage at which it can give a correct answer, and say why it
   cannot run earlier.

5. **[warm‑up]** A teammate's `docker-compose.yml` writes the database password directly
   into the `environment:` block as a literal string, and the file is committed to the
   repository. Using §14.4.4, name two distinct things that go wrong with this, and
   rewrite the relevant lines so the password comes from an untracked source instead.
   Then, using §14.4.3, explain why the `db` (Postgres) service needs a `volumes:` entry
   but the `cache` (Redis) service can safely omit one.

## Analysis

6. **[analysis]** *Compute the DORA metrics.* A student team's combined git and deploy log
   for two weeks is below. A deploy is "failed" if it required a revert or hotfix;
   recovery time is from deploy to restored service. Note that the revert and the hotfix
   are themselves deployments — unplanned ones, shipped because production broke.

   | Change | Commit time | Deployed | Outcome |
   |--------|-------------|----------|---------|
   | C1 | Mon 09:00 | Mon 15:00 | ok |
   | C2 | Mon 11:00 | Tue 10:00 | ok |
   | C3 | Tue 14:00 | Thu 09:00 | failed — reverted Thu 10:30 |
   | C4 | Thu 11:00 | Thu 16:00 | ok |
   | C5 | Fri 10:00 | Mon 10:00 (wk 2) | ok |
   | C6 | Mon 13:00 (wk 2) | Wed 09:00 (wk 2) | failed — hotfixed Wed 15:00 |
   | C7 | Wed 10:00 (wk 2) | Wed 17:00 (wk 2) | ok |
   | C8 | Thu 09:00 (wk 2) | Fri 11:00 (wk 2) | ok |

   Compute (a) deployment frequency (deploys per week), (b) median change lead time,
   (c) change fail rate, (d) mean failed-deployment recovery time, and (e) deployment
   rework rate — counting the revert and the hotfix as deployments, what share of *all*
   deployments were unplanned (§14.7.1)? Then (f) using the 2019 elite bands quoted in
   §14.7.3, identify which metric is furthest from elite and propose the single pipeline
   change most likely to improve it.

7. **[analysis]** *Design a canary rollout.* Your team is shipping a rewritten
   session-handling module to a service with 200,000 daily users. Design a staged rollout
   plan (§14.3.2): define at least three rings with their traffic percentages, the health
   metrics that gate each promotion (name at least three, and give a numeric threshold for
   one), the soak time per ring, and the automatic action on regression. State explicitly
   what your plan's worst-case blast radius is, and compare it to a blue-green switch of
   100% of traffic.

8. **[analysis]** *Knight versus CrowdStrike.* Using only the facts in §14.3.5, write a
   structured comparison of the two incidents: for each, identify (a) the latent defect
   and how long it lay dormant, (b) the deployment-process failure that activated or
   spread it, (c) the missing safeguard that would have bounded the damage, and (d) the
   time from trigger to full impact. Then answer the pairing question directly: why does
   Knight argue *for* deployment automation while CrowdStrike shows automation is not
   sufficient — and what one practice, common to both post-mortems, addresses each?

9. **[analysis]** The CrowdStrike case says "config and content are code." A teammate
   objects: "running our full test suite on every config change would be absurd — it's
   just data." Steelman the teammate's position, then rebut it: what *proportionate*
   pipeline (validation, testing, staged rollout) would you design for pure-content
   changes, and which properties of code changes must it preserve?

10. **[analysis]** Goodhart's Law (§12.1.2) says any single metric target gets gamed. For
    each of the four classic DORA keys taken *alone*, describe a way a cynical team could
    improve the number while making delivery worse — then show which *other* metric would
    expose each cheat (§14.7.2). Finally: DORA's 2024 addition of **deployment rework
    rate** closed exactly one such gap — which of your cheats does it catch that the
    original four keys missed, and why did that cheat survive the original pairing?

11. **[analysis]** You are putting a small service online at `app.example.com`, running as
    a Compose stack (app + Postgres + Redis) on a single rented virtual machine. Using
    §14.5, write the deployment as an ordered checklist: (a) the DNS record(s) you create
    and what each points to; (b) how the service obtains a valid HTTPS certificate; (c)
    what placing the domain behind Cloudflare would add, and one risk it introduces; and
    (d) one thing that could still be broken for users after all of the above is correct,
    and how you would detect it — connecting your answer to the DORA signals of §14.7.
