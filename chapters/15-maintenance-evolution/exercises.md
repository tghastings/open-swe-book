# Chapter 15 — Exercises

Exercises are graded by depth: **[warm‑up]** checks understanding, **[analysis]** asks
you to reason. Two of the three require *actual work* — writing a real characterization
suite, designing a migration — not just prose. Show the work, not only the answer.

## Concepts

1. **[warm‑up]** Classify each of these as *deliberate* or *inadvertent* technical debt
   (§15.4), and justify: (a) hard-coding a single currency to make a demo deadline, with
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

3. **[analysis]** Your organization proposes a two-year big-bang rewrite of a
    ten-year-old billing system. Using §15.5 and the browser-rewrite case of §2.6.3,
    write a one-page counter-proposal for a strangler-fig migration: what the interception
    layer would be, which capability you would peel off first (and why *that* one), how
    each slice gets validated, and what the organization can do at month six under your
    plan that it cannot do under the rewrite.
