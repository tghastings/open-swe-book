# Chapter 9 — Exercises

Exercises are graded by depth: **[warm‑up]** checks understanding, **[analysis]** asks
you to reason. Several exercises require *actual work* — drawing a graph,
deriving values, or constructing a test set — not just prose. Show the work, not only the
answer.

## Concepts

1. **[warm‑up]** In one sentence each, state the *selection*, *adequacy*, and *oracle*
   problems from §9.1.1, then give a concrete example of a function for which the oracle
   problem is genuinely hard (you can produce inputs but cannot easily say what the right
   output is).

2. **[warm‑up]** Explain why "we ran the app and it looked fine" fails as a stopping rule,
   and rewrite it as a proper test-adequacy criterion for a function that validates email
   addresses.

3. **[warm‑up]** For the `apply_discount` function in §9.2.1, classify each of these as an
   *exact-value*, *property*, or *cross-check* oracle: (a) `assert apply_discount(100, 50)
   == 50`; (b) `assert apply_discount(p, 0) == p for all p >= 0`; (c) comparing the result
   against last year's pricing engine. Which is strongest, and why?

4. **[warm‑up]** Give one defect that a *unit* test cannot catch but an *integration* test
   can, and one that an *integration* test cannot catch but a *system* test can. Explain
   the difference in scope that makes each blind spot exist.

## Analysis

5. **[analysis]** A teammate proudly reports "95% statement coverage." Describe two
   distinct ways the code could still contain a serious, easily-triggered defect despite
   that number. For each, name the coverage criterion (from §9.3 or §9.5) that would have
   forced a test to catch it.

6. **[analysis]** Explain, with a two-test example of your own construction, why 100%
   *condition* coverage does not imply 100% *decision* coverage. Then give a different
   two-test example showing the reverse (100% decision, less than 100% condition). (See
   §9.5.1 — but use a decision *other* than `A || B`.)

7. **[analysis]** A team has inverted the testing pyramid into an "ice-cream cone": 200
   slow end-to-end tests and 30 unit tests. Describe three concrete symptoms they will
   experience and the refactoring of their test strategy you would recommend, with
   justification tied to the cost-of-defect argument in §9.2.4.

8. **[analysis]** Combinatorial (pairwise) testing "reduces 27 runs to 9" in §9.6. Under
   what circumstance does a pairwise suite *provably* miss a defect? Construct a small
   three-parameter example where the bug appears only under a specific three-way
   combination, and state what coverage strength you would need to guarantee catching it.

## Do the work

9. **[analysis]** *Draw a CFG and give branch-coverage tests.* Consider:

   ```generic
   function fizzbuzz(n)
     if n % 15 = 0 then
       return "FizzBuzz"
     else if n % 3 = 0 then
       return "Fizz"
     else if n % 5 = 0 then
       return "Buzz"
     else
       return n as text
     end if
   end function
   ```

   ```go
   func fizzbuzz(n int) string {
   	if n%15 == 0 {
   		return "FizzBuzz"
   	} else if n%3 == 0 {
   		return "Fizz"
   	} else if n%5 == 0 {
   		return "Buzz"
   	} else {
   		return strconv.Itoa(n)
   	}
   }
   ```

   ```java
   static String fizzbuzz(int n) {
     if (n % 15 == 0) {
       return "FizzBuzz";
     } else if (n % 3 == 0) {
       return "Fizz";
     } else if (n % 5 == 0) {
       return "Buzz";
     } else {
       return String.valueOf(n);
     }
   }
   ```

   ```javascript
   function fizzbuzz(n) {
     if (n % 15 === 0) {
       return "FizzBuzz";
     } else if (n % 3 === 0) {
       return "Fizz";
     } else if (n % 5 === 0) {
       return "Buzz";
     } else {
       return String(n);
     }
   }
   ```

   ```python
   def fizzbuzz(n):
     if n % 15 == 0:
       return "FizzBuzz"
     elif n % 3 == 0:
       return "Fizz"
     elif n % 5 == 0:
       return "Buzz"
     else:
       return str(n)
   ```

   ```ruby
   def fizzbuzz(n)
     if n % 15 == 0
       "FizzBuzz"
     elsif n % 3 == 0
       "Fizz"
     elsif n % 5 == 0
       "Buzz"
     else
       n.to_s
     end
   end
   ```

   ```typescript
   function fizzbuzz(n: number): string {
     if (n % 15 === 0) {
       return "FizzBuzz";
     } else if (n % 3 === 0) {
       return "Fizz";
     } else if (n % 5 === 0) {
       return "Buzz";
     } else {
       return String(n);
     }
   }
   ```

   (a) Draw the control-flow graph (Mermaid or by hand), labeling each decision node and
   each edge. (b) Give the minimum number of test inputs that achieves 100% **branch
   coverage**, list the input and expected output for each, and (c) state which branch
   edges each test covers. (d) Does your suite also achieve 100% statement coverage? Argue
   why, referencing the subsumption relationship from §9.3.2.

10. **[analysis]** *Derive boundary values.* A spec states: *`assign_grade(score)` accepts
    an integer `0..100`; it returns `"A"` for `90..100`, `"B"` for `80..89`, `"C"` for
    `70..79`, and `"F"` for `0..69`; any score outside `0..100` is rejected with an
    error.* (a)
    List the equivalence classes (valid and invalid). (b) For every boundary in the spec,
    give the below/at/above triple of values and the expected result for each. (c) Then
    write a buggy one-line guard or comparison (e.g., `>=` vs `>`) and identify exactly
    which of your boundary tests would catch it.

11. **[analysis]** *Construct an MC/DC test set.* Consider the decision
    `D = A && (B || C)` (note: different from the worked example). (a) Build the full 8-row
    truth table with a `D` column. (b) Find an independence pair for each of A, B, and C
    (two rows differing only in that condition, with `D` flipping). (c) Take the union to
    give a minimal MC/DC suite and confirm it has N + 1 = 4 tests (or explain why this
    decision needs a different count). (d) State, for each test in your final set, which
    condition(s) it helps prove independent.

12. **[analysis]** *Path counting.* For the classify-and-sum function in §9.3.1, you
    argued full path coverage is impossible. Now take a *loop-free* function with three
    independent `if` statements in sequence (write one — e.g., applying three optional
    surcharges). (a) How many distinct paths does it have? (b) How many tests for branch
    coverage? (c) Explain the exponential-vs-linear gap and what it implies about when path
    coverage is worth attempting.
