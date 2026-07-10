# Chapter 15 — Exercises

Exercises are graded by depth: **[warm‑up]** checks understanding, **[analysis]** asks
you to reason. Several require *actual work* — a real characterization suite, a real
refactoring, a real repository — not just prose. Show the work, not only the answer.

## Concepts

1. **[warm‑up]** Classify each of these as *deliberate* or *inadvertent* technical debt
   (§15.5), and justify: (a) hard-coding a single currency to make a demo deadline, with
   a backlog ticket to internationalize; (b) a data model that made sense before the
   requirements pivoted; (c) copy-pasting a function at 2 a.m. during crunch to avoid
   touching a shared module.

## Analysis

2. **[analysis]** *Write a characterization test.* You inherit this undocumented,
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

    (a) Following §15.2, write a suite of characterization tests, in your language's
    test framework, that pins the current behavior for at least six input classes,
    including a missing value (`None`, `null`, or `nil`, whichever your tab uses),
    empty string, whitespace-only, over-length, hyphenated, and a non-alphanumeric input
    under both `strict` values. (b) Identify one behavior your probing reveals that looks
    like a bug, and explain — citing §15.2 — why you should pin it rather than fix it
    in the same change. (c) State which single line you would be most afraid to "clean
    up" without this suite, and why.

3. **[analysis]** *Refactor under green.* With the characterization suite from exercise 2
    in place, refactor your language's `norm_code` in small, named, behavior-preserving
    moves (§15.3): at minimum, extract the normalization steps (trim/uppercase/strip
    hyphens) into their own function, and remove the duplicated strict/empty handling so
    the "what counts as invalid" decision lives in exactly one place. Rules: one move at
    a time, suite green after every move, no behavior change (the suite is the referee —
    including any pinned bug). Report each move by its catalog name, and state after
    which move you would commit, and why there rather than at the end.

4. **[analysis]** *Build a technical-debt register.* The clinic-app team's codebase
    carries these known liabilities: (a) the authorization check is copy-pasted into
    three request handlers; (b) the ORM is two major versions behind and the old version
    stops receiving security patches next year; (c) a hand-rolled date parser has a known
    daylight-saving bug that two downstream call sites silently work around; (d) the
    billing module has no tests at all; (e) a feature flag from a promotion that ended
    last year still guards dead code in the checkout path. Build a **debt register**
    (§15.5): for each item, classify it (deliberate or inadvertent), name the *interest*
    it charges (what it costs the team per sprint, concretely) and the *principal* (what
    paying it off would take). Then order the five for paydown, justify the order — and
    identify the one item you would argue is *not* worth paying down this term, and why.

5. **[analysis]** Your organization proposes a two-year big-bang rewrite of a
    ten-year-old billing system. Using §15.6 and the browser-rewrite case of §2.6.3,
    write a one-page counter-proposal for a strangler-fig migration: what the interception
    layer would be, which capability you would peel off first (and why *that* one), how
    each slice gets validated, and what the organization can do at month six under your
    plan that it cannot do under the rewrite.

6. **[analysis]** *Maintain, strangle, or rewrite?* A regional insurer runs a 12-year-old
    policy-administration system: the domain rules change perhaps twice a year (regulatory
    updates), the last production incident was fourteen months ago, two of the original
    developers still maintain it, and test coverage is thin everywhere except the premium
    calculator — but one subsystem, the customer-facing quote portal, needs features the
    old architecture makes painful. Management is being pitched a full rewrite. Write a
    one-page recommendation that honestly weighs all *three* options — continued
    maintenance, a strangler migration (§15.6), and the rewrite — against criteria you
    state explicitly (rate of change, incident history, knowledge retention, test
    coverage, where the pain actually is). Note that in this scenario the cheapest option
    may be the right one for most of the system; your recommendation may differ by
    subsystem, and should say so.

7. **[analysis]** *Find the change points and seams in a real codebase.* Pick a codebase
    you did not write — your team project's oldest module, or an open-source project you
    use — and invent one plausible change request for it. Before touching anything,
    report: (a) the **change points** — the specific files and functions where the change
    must land (§15.1); (b) the **seam** you would use to get tests in place — the spot
    where you can alter or intercept behavior without editing the code you are about to
    change (a constructor parameter, an interface boundary, an environment hook); (c) the
    first characterization test you would write there (§15.2), with its actual input; and
    (d) one place you would refuse to modify until it had more coverage, and what that
    refusal would cost.

8. **[analysis]** *Repository stewardship.* Choose one pull request from your team project
    or another repository. Identify one small improvement you made — or could safely make —
    beyond the requested behavior: a clearer name, a stronger test, a corrected document, a
    simplified branch, removed duplication, or an improved build check. Explain why the
    improvement is *relevant* to the change (not an unrelated detour), how you verified it
    preserved behavior (§15.2, §15.3), and name one *larger* cleanup you deliberately left
    for a separate issue because including it would have made the change harder to review or
    reverse (§15.4, §15.5).
