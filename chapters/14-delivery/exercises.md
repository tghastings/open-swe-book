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

5. **[warm‑up]** Classify each of these as *deliberate* or *inadvertent* technical debt
   (§14.8.4), and justify: (a) hard-coding a single currency to make a demo deadline, with
   a backlog ticket to internationalize; (b) a data model that made sense before the
   requirements pivoted; (c) copy-pasting a function at 2 a.m. during crunch to avoid
   touching a shared module.

6. **[warm‑up]** A teammate's `docker-compose.yml` writes the database password directly
   into the `environment:` block as a literal string, and the file is committed to the
   repository. Using §14.4.4, name two distinct things that go wrong with this, and
   rewrite the relevant lines so the password comes from an untracked source instead.
   Then, using §14.4.3, explain why the `db` (Postgres) service needs a `volumes:` entry
   but the `cache` (Redis) service can safely omit one.

## Analysis

7. **[analysis]** *Compute the four keys.* A student team's combined git and deploy log
   for two weeks is below. A deploy is "failed" if it required a revert or hotfix;
   recovery time is from deploy to restored service.

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

   Compute (a) deployment frequency (deploys per week), (b) median lead time for changes,
   (c) change failure rate, and (d) mean failed-deployment recovery time. Then (e) using
   §14.7.3's elite benchmarks, identify which key is furthest from elite and propose the
   single pipeline change most likely to improve it.

8. **[analysis]** *Design a canary rollout.* Your team is shipping a rewritten
   session-handling module to a service with 200,000 daily users. Design a staged rollout
   plan (§14.3.2): define at least three rings with their traffic percentages, the health
   metrics that gate each promotion (name at least three, and give a numeric threshold for
   one), the soak time per ring, and the automatic action on regression. State explicitly
   what your plan's worst-case blast radius is, and compare it to a blue-green switch of
   100% of traffic.

9. **[analysis]** *Knight versus CrowdStrike.* Using only the facts in §14.3.5, write a
   structured comparison of the two incidents: for each, identify (a) the latent defect
   and how long it lay dormant, (b) the deployment-process failure that activated or
   spread it, (c) the missing safeguard that would have bounded the damage, and (d) the
   time from trigger to full impact. Then answer the pairing question directly: why does
   Knight argue *for* deployment automation while CrowdStrike shows automation is not
   sufficient — and what one practice, common to both post-mortems, addresses each?

10. **[analysis]** The CrowdStrike case says "config and content are code." A teammate
   objects: "running our full test suite on every config change would be absurd — it's
   just data." Steelman the teammate's position, then rebut it: what *proportionate*
   pipeline (validation, testing, staged rollout) would you design for pure-content
   changes, and which properties of code changes must it preserve?

11. **[analysis]** Goodhart's Law (§12.1.2) says any single metric target gets gamed. For
    each of the four DORA keys taken *alone*, describe a way a cynical team could improve
    the number while making delivery worse — then show which *other* key would expose each
    cheat (§14.7.2). One key is hardest to pair with a built-in counter; identify it and
    propose an external counter-metric.

12. **[analysis]** *Write a characterization test.* You inherit this undocumented,
    untested function, which production code calls from several places:

    ```generic
    function norm_code(s, strict)              // strict defaults to false
      if s is missing then
        if strict then return nothing else return "" end if
      end if
      s <- remove all "-" from uppercase(trim(s))
      if length(s) > 8 then
        s <- first 8 characters of s
      end if
      // alphanumeric check is false for the empty string
      if strict and not (s is nonempty and every character of s is alphanumeric) then
        raise error with value s
      end if
      if s is empty then
        if strict then return nothing else return "" end if
      end if
      return s
    end function
    ```

    ```go
    func normCode(s *string, strict bool) (*string, error) { // nil = missing input
    	if s == nil {
    		if strict {
    			return nil, nil
    		}
    		return new(string), nil // ""
    	}
    	t := strings.ReplaceAll(strings.ToUpper(strings.TrimSpace(*s)), "-", "")
    	if len(t) > 8 {
    		t = t[:8]
    	}
    	if strict && !isAlnum(t) {
    		return nil, fmt.Errorf("invalid code: %q", t)
    	}
    	return &t, nil
    }

    func isAlnum(s string) bool { // alnum check: nonempty, all letters/digits
    	for _, r := range s {
    		if !unicode.IsLetter(r) && !unicode.IsDigit(r) {
    			return false
    		}
    	}
    	return s != ""
    }
    ```

    ```java
    static String normCode(String s, boolean strict) {
      if (s == null) return strict ? null : "";
      s = s.strip().toUpperCase().replace("-", "");
      if (s.length() > 8) s = s.substring(0, 8);
      boolean alnum = !s.isEmpty() && s.chars().allMatch(Character::isLetterOrDigit);
      if (strict && !alnum) throw new IllegalArgumentException(s);
      return s.isEmpty() ? (strict ? null : "") : s;
    }
    ```

    ```javascript
    function normCode(s, strict = false) {
      if (s === null) return strict ? null : "";
      s = s.trim().toUpperCase().replaceAll("-", "");
      if (s.length > 8) s = s.slice(0, 8);
      if (strict && !/^[\p{L}\p{N}]+$/u.test(s)) throw new RangeError(s);
      return s || (strict ? null : "");
    }
    ```

    ```python
    def norm_code(s, strict=False):
      if s is None:
        return "" if not strict else None
      s = s.strip().upper().replace("-", "")
      if len(s) > 8:
        s = s[:8]
      if strict and not s.isalnum():
        raise ValueError(s)
      return s or ("" if not strict else None)
    ```

    ```ruby
    def norm_code(s, strict: false)
      return strict ? nil : "" if s.nil?
      s = s.strip.upcase.delete("-")
      s = s[0, 8] if s.length > 8
      raise ArgumentError, s if strict && s !~ /\A[[:alnum:]]+\z/
      s.empty? ? (strict ? nil : "") : s
    end
    ```

    ```typescript
    function normCode(s: string | null, strict: boolean = false): string | null {
      if (s === null) return strict ? null : "";
      s = s.trim().toUpperCase().replaceAll("-", "");
      if (s.length > 8) s = s.slice(0, 8);
      if (strict && !/^[\p{L}\p{N}]+$/u.test(s)) throw new RangeError(s);
      return s || (strict ? null : "");
    }
    ```

    (a) Following §14.8.2, write a suite of characterization tests, in your language's
    test framework, that pins the current behavior for at least six input classes,
    including a missing value (`None`, `null`, or `nil`, whichever your tab uses),
    empty string, whitespace-only, over-length, hyphenated, and a non-alphanumeric input
    under both `strict` values. (b) Identify one behavior your probing reveals that looks
    like a bug, and explain — citing §14.8.2 — why you should pin it rather than fix it
    in the same change. (c) State which single line you would be most afraid to "clean
    up" without this suite, and why.

13. **[analysis]** Your organization proposes a two-year big-bang rewrite of a
    ten-year-old billing system. Using §14.8.5 and the browser-rewrite case of §2.6.3,
    write a one-page counter-proposal for a strangler-fig migration: what the interception
    layer would be, which capability you would peel off first (and why *that* one), how
    each slice gets validated, and what the organization can do at month six under your
    plan that it cannot do under the rewrite.

14. **[analysis]** You are putting a small service online at `app.example.com`, running as
    a Compose stack (app + Postgres + Redis) on a single rented virtual machine. Using
    §14.5, write the deployment as an ordered checklist: (a) the DNS record(s) you create
    and what each points to; (b) how the service obtains a valid HTTPS certificate; (c)
    what placing the domain behind Cloudflare would add, and one risk it introduces; and
    (d) one thing that could still be broken for users after all of the above is correct,
    and how you would detect it — connecting your answer to the DORA signals of §14.7.
