# Chapter 15 — Maintenance and Evolution

> **Where we are.** Chapter 14 carried a verified change the last mile into production and
> taught you to keep it flowing — pipelines, progressive deployment, containers, names,
> certificates, and the DORA evidence that delivery performance matters. This chapter is
> about everything after the celebration: the years a successful system spends being
> fixed, adapted, extended, and refactored, usually by people who did not write it.

Deployment begins the longest phase of a successful system's life. Most professional
effort goes into **evolving** systems that have been in production for years, not into
building new ones — and this chapter is about the code you will inherit.

The industry has names for that work. **Corrective maintenance** fixes defects.
**Adaptive maintenance** responds to a changing environment — a new OS version, a
deprecated API, a new regulation — where the code did nothing wrong but the world moved.
**Perfective maintenance** adds the features and improvements users keep asking a living
system for. And **preventative maintenance** — refactoring, debt paydown — improves
structure now so that all the other kinds stay affordable later. A widely cited
historical rule of thumb places maintenance, taken together, at roughly 60 percent of a
system's lifetime cost — the share varies substantially by system, by organization, and
by what gets classified as maintenance, but the direction is not in
doubt.[^1] Read that number again: the phase this book spent fourteen chapters
preparing you for is the *minority* of the money, which is reason enough to treat evolving
code as the main event of an engineering career rather than the cleanup after it.

## 15.1 What Makes Code Legacy

Colloquially, "legacy" means old. The working definition that matters is different:
**legacy code is code without tests** — or, in its more visceral form, *code you are
afraid to change*. Age is incidental. A module written last month with no tests, no
documentation, and one departed author is legacy; a fifteen-year-old module with a
thorough suite is not, because the suite makes change safe. The defining property is that
*the system's actual behavior is not pinned down anywhere except in the code itself* —
so any change might break something, you cannot know what, and you cannot know cheaply.
Fear sets in, fear breeds avoidance, avoidance means changes are bolted on in the least
invasive (and least clean) way possible, and the code gets worse precisely because
everyone is being careful. Breaking that spiral is a skill, and it starts with an
inversion of the testing you learned in Chapter 10.

The tests-first definition comes from Michael Feathers, whose *Working Effectively with
Legacy Code* also names the only two ways there are to change legacy code.[^2] **Edit and
pray**: study the code, make the change, look around manually for anything you broke,
deploy, and hope. **Cover and modify**: first build tests that cover the code you must
touch, then make the change and let the tests detect any behavior you altered without
meaning to. This book has been teaching the second way all along; here it finally gets its
name. Cover-and-modify starts with a search, not an edit: locate your **change points** —
the specific places in the code where your change must actually land — because those are
the places the test coverage has to grip before you touch anything. The next two
sections are cover-and-modify in practice.

## 15.2 Characterization Tests

Chapter 10's tests were built from a *specification*: the oracle
([§10.1.4](../10-testing/#1014-test-oracles-evaluating-the-response-to-a-test)) told you
what the right answer *should* be. Legacy code has no trustworthy spec — the comments
lie, the documentation describes version 2, and the original requirements are three
pivots old. So you flip the direction of inference. A **characterization test** documents
what the code *actually does now*: you call the function with an input, observe the
output, and write that observation down as the expected value. The running system itself
becomes the oracle.

This feels like cheating — you are asserting the code does whatever it does, bugs
included. But the test's job is to **pin down current behavior**, not to verify
correctness, so that your upcoming changes cannot alter it *unknowingly*. Users, and other
code, may well depend on the current behavior, strange corners and all. The practical
loop: write a test with a deliberately wrong expected value, run it, read the actual
value from the failure message, and promote that actual value into the assertion. Probe
the edges — empty inputs, nulls, boundary values — until you have a net of pinned
behavior around everything your change might disturb. When a characterization test
exposes something that is plainly a bug, resist fixing it in the same breath: record it,
finish building the net, and change behavior as its own deliberate, separately reviewed
step. One commit should refactor *or* fix, never ambiguously both.

Applied to a fee-code lookup inherited with the clinic scheduler, the loop leaves this
trail:

```generic
function legacy_fee_code(visit_type)   // inherited: no docs, no tests
  codes <- { "exam": "E10", "lab": "L20", "vaccine": "V30" }
  if visit_type is a key in codes then
    return codes[visit_type]
  end if
  return "E10"                          // default when the type is unknown
end function

test probe_unknown_type
  assert legacy_fee_code("phone") = "XXX"    // deliberately wrong
// FAILED: legacy_fee_code("phone") = "E10", not "XXX"

test unknown_type_bills_as_exam              // observed value, promoted
  assert legacy_fee_code("phone") = "E10"

test empty_type_bills_as_exam                // edge probe: pinned, bug or not
  assert legacy_fee_code("") = "E10"
```

```go
func legacyFeeCode(visitType string) string { // inherited: no docs, no tests
	codes := map[string]string{"exam": "E10", "lab": "L20", "vaccine": "V30"}
	return cmp.Or(codes[visitType], "E10")
}

func TestProbeUnknownType(t *testing.T) {
	if got := legacyFeeCode("phone"); got != "XXX" { // deliberately wrong
		t.Errorf(`legacyFeeCode("phone") = %q, want "XXX"`, got)
	}
}
// FAILED: legacyFeeCode("phone") = "E10", want "XXX"

func TestUnknownTypeBillsAsExam(t *testing.T) { // observed value, promoted
	if got := legacyFeeCode("phone"); got != "E10" {
		t.Errorf("got %q", got)
	}
}

func TestEmptyTypeBillsAsExam(t *testing.T) { // edge probe: pinned, bug or not
	if got := legacyFeeCode(""); got != "E10" {
		t.Errorf("got %q", got)
	}
}
```

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;
import java.util.Map;

class FeeCodeCharacterization {
  static String legacyFeeCode(String visitType) {   // inherited: no docs, no tests
    return Map.of("exam", "E10", "lab", "L20", "vaccine", "V30")
        .getOrDefault(visitType, "E10");
  }

  @Test void probeUnknownType() {
    assertEquals("XXX", legacyFeeCode("phone"));    // deliberately wrong
  }
  // FAILED: org.opentest4j.AssertionFailedError: expected: <XXX> but was: <E10>

  @Test void unknownTypeBillsAsExam() {             // observed value, promoted
    assertEquals("E10", legacyFeeCode("phone"));
  }

  @Test void emptyTypeBillsAsExam() {               // edge probe: pinned, bug or not
    assertEquals("E10", legacyFeeCode(""));
  }
}
```

```javascript
const test = require("node:test");
const assert = require("node:assert/strict");

function legacyFeeCode(visitType) {                 // inherited: no docs, no tests
  return { exam: "E10", lab: "L20", vaccine: "V30" }[visitType] ?? "E10";
}

test("probe unknown type", () => {
  assert.equal(legacyFeeCode("phone"), "XXX");      // deliberately wrong
});
// FAILED: AssertionError [ERR_ASSERTION]: Expected values to be strictly equal:
// 'E10' !== 'XXX'

test("unknown type bills as exam", () => {          // observed value, promoted
  assert.equal(legacyFeeCode("phone"), "E10");
});

test("empty type bills as exam", () => {            // edge probe: pinned, bug or not
  assert.equal(legacyFeeCode(""), "E10");
});
```

```python
def legacy_fee_code(visit_type):                    # inherited: no docs, no tests
  return {"exam": "E10", "lab": "L20", "vaccine": "V30"}.get(visit_type, "E10")

def test_probe_unknown_type():
  assert legacy_fee_code("phone") == "XXX"        # deliberately wrong
# FAILED: AssertionError: assert 'E10' == 'XXX'

def test_unknown_type_bills_as_exam():              # observed value, promoted
  assert legacy_fee_code("phone") == "E10"

def test_empty_type_bills_as_exam():                # edge probe: pinned, bug or not
  assert legacy_fee_code("") == "E10"
```

```ruby
require "minitest/autorun"

def legacy_fee_code(visit_type)                     # inherited: no docs, no tests
  { "exam" => "E10", "lab" => "L20", "vaccine" => "V30" }.fetch(visit_type, "E10")
end

class TestFeeCode < Minitest::Test
  def test_probe_unknown_type
    assert_equal "XXX", legacy_fee_code("phone")    # deliberately wrong
  end
  # FAILED: Expected: "XXX"  Actual: "E10"

  def test_unknown_type_bills_as_exam               # observed value, promoted
    assert_equal "E10", legacy_fee_code("phone")
  end

  def test_empty_type_bills_as_exam                 # edge probe: pinned, bug or not
    assert_equal "E10", legacy_fee_code("")
  end
end
```

```typescript
import test from "node:test";
import assert from "node:assert/strict";

function legacyFeeCode(visitType: string): string {  // inherited: no docs, no tests
  const codes: Record<string, string> =
    { exam: "E10", lab: "L20", vaccine: "V30" };
  return codes[visitType] ?? "E10";
}

test("probe unknown type", () => {
  assert.equal(legacyFeeCode("phone"), "XXX");       // deliberately wrong
});
// FAILED: AssertionError [ERR_ASSERTION]: Expected values to be strictly equal:
// 'E10' !== 'XXX'

test("unknown type bills as exam", () => {           // observed value, promoted
  assert.equal(legacyFeeCode("phone"), "E10");
});

test("empty type bills as exam", () => {             // edge probe: pinned, bug or not
  assert.equal(legacyFeeCode(""), "E10");
});
```

Characterizing assumes you can find your way around, and with an inherited codebase that
takes a deliberate workflow. Read what the previous team left behind first — the tests
above all: a passing test is executable documentation that stays synchronized with the
behavior it actually checks, though what it checks may be incomplete or no longer what
anyone intends. Then read any design
documents. On documentation, note the distinction: an architecture description
([§6.5](../06-design-and-architecture/#65-describing-system-architecture)) is the *formal*
design artifact, but tests, commit history, and mockups are living *informal*
documentation, and agile teams weight the informal kind heavily because it stays closer
to the code. Next, generate a class or dependency diagram — most languages have
tools that extract one — to see the shape of the system before you dive into any single
file. Then get the application and its test suite running *locally*, against a cloned or
fixture copy of the database, before touching anything: a system you cannot run is a
system you cannot characterize. Only then write characterization tests at your intended
change points, and begin.

Modern tooling has also shifted the *comprehension* half of legacy work. Understanding
what a gnarly function actually does — the prerequisite for characterizing it — has always
been the slowest, loneliest part of the job. AI assistants
([§13.2](../13-ai-across-the-lifecycle/#132-ai-across-the-lifecycle)) are genuinely strong
here: summarizing an unfamiliar module, proposing what a function's edge cases might be,
drafting candidate characterization tests for you to verify against the running code. The
verification discipline of Chapter 13 still governs — an AI's *account* of legacy behavior
is a hypothesis, and the running system remains the only oracle — but as a hypothesis
generator for code no living person understands, it removes a real bottleneck.

## 15.3 Refactoring Under Green Tests

With behavior pinned, you can refactor. Chapter 2 introduced **refactoring** inside the
red–green–refactor loop
([§2.3.2](../02-software-development-processes/#232-testing-make-it-central-to-development)):
improving the design of existing code without changing its behavior, protected by green
tests. In legacy work, the loop is the same but the entry point differs — you had to
*build* the green net first — and the discipline must be stricter, because the code fights
back. The craft is to move in steps so small that each one is obviously
behavior-preserving — rename, extract a function, inline a variable, move a method —
running the suite after every step. If the bar goes red, the *last* step is the culprit;
undo it and take a smaller one. Named, cataloged refactoring moves (Fowler's catalog is
the standard reference) matter because each has known mechanics and known traps; a
sequence of safe moves composes into a transformation you would never dare attempt as one
leap.[^3]

Where should you aim the moves? **Code smells** are surface symptoms that *suggest* — not
prove — a deeper design problem: a long method, a large class that does too many things, a
stretch of duplicated code, **magic numbers** (unexplained literals like `65` scattered
through the logic), deeply nested conditionals, a long parameter list. A smell is a prompt
to look closer, not a verdict; sometimes the long method really is the clearest way to
write that logic. For functions in particular, a compact health checklist is **SOFA**:
keep each function **S**hort, doing **O**ne thing, taking **F**ew arguments, and written
at a single level of **A**bstraction. Some smells can even be measured: cyclomatic
complexity counts the independent decision paths through a function — built on the
control-flow analysis of [Chapter 10](../10-testing/#1031-control-flow-graphs) — turning
"this method feels tangled"
into a number a pipeline can watch.

The named moves map onto the smells. Beyond rename, extract, inline, and move: **replace
magic number with named constant** (`speed > SPEED_LIMIT` explains itself; `speed > 65`
does not); **introduce guard clauses** — early returns for the exceptional cases — to
flatten deeply nested conditionals; **remove duplication**, applying Chapter 6's DRY
principle, while staying alert for code that merely *looks* similar but serves different
purposes; **decompose large class**, splitting along clusters of fields and methods that
change together; **replace temp with query**, turning a scattered computed variable into
one well-named method; and **introduce parameter object**, bundling arguments that always
travel together into a single type that can then attract the behavior that uses it.

The clinic scheduler's booking check shows two of those smells at once:

```generic
function can_book(patient, slot, booked_today)
  if patient is present then
    if slot.open then
      if booked_today < 8 then      // magic number: daily booking cap
        return true
      else
        return false
      end if
    else
      return false
    end if
  else
    return false
  end if
end function
```

```go
func canBook(patient *Patient, slot Slot, bookedToday int) bool {
	if patient != nil {
		if slot.Open {
			if bookedToday < 8 {
				return true
			} else {
				return false
			}
		} else {
			return false
		}
	} else {
		return false
	}
}
```

```java
static boolean canBook(Patient patient, Slot slot, int bookedToday) {
  if (patient != null) {
    if (slot.open()) {
      if (bookedToday < 8) {
        return true;
      } else {
        return false;
      }
    } else {
      return false;
    }
  } else {
    return false;
  }
}
```

```javascript
function canBook(patient, slot, bookedToday) {
  if (patient !== null) {
    if (slot.open) {
      if (bookedToday < 8) {
        return true;
      } else {
        return false;
      }
    } else {
      return false;
    }
  } else {
    return false;
  }
}
```

```python
def can_book(patient, slot, booked_today):
  if patient is not None:
    if slot.open:
      if booked_today < 8:
        return True
      else:
        return False
    else:
      return False
  else:
    return False
```

```ruby
def can_book(patient, slot, booked_today)
  if !patient.nil?
    if slot.open
      if booked_today < 8
        true
      else
        false
      end
    else
      false
    end
  else
    false
  end
end
```

```typescript
interface Slot {
  open: boolean;
}

function canBook(patient: string | null, slot: Slot, bookedToday: number): boolean {
  if (patient !== null) {
    if (slot.open) {
      if (bookedToday < 8) {
        return true;
      } else {
        return false;
      }
    } else {
      return false;
    }
  } else {
    return false;
  }
}
```

Replace the magic `8` with a named constant, run the suite, flatten the nesting with
guard clauses, run it again — the tests stay green after each move:

```generic
MAX_DAILY_BOOKINGS <- 8

function can_book(patient, slot, booked_today)
  if patient is absent then return false
  if not slot.open then return false
  return booked_today < MAX_DAILY_BOOKINGS
end function
```

```go
const maxDailyBookings = 8

func canBook(patient *Patient, slot Slot, bookedToday int) bool {
	if patient == nil {
		return false
	}
	if !slot.Open {
		return false
	}
	return bookedToday < maxDailyBookings
}
```

```java
static final int MAX_DAILY_BOOKINGS = 8;

static boolean canBook(Patient patient, Slot slot, int bookedToday) {
  if (patient == null) return false;
  if (!slot.open()) return false;
  return bookedToday < MAX_DAILY_BOOKINGS;
}
```

```javascript
const MAX_DAILY_BOOKINGS = 8;

function canBook(patient, slot, bookedToday) {
  if (patient === null) return false;
  if (!slot.open) return false;
  return bookedToday < MAX_DAILY_BOOKINGS;
}
```

```python
MAX_DAILY_BOOKINGS = 8

def can_book(patient, slot, booked_today):
  if patient is None:
    return False
  if not slot.open:
    return False
  return booked_today < MAX_DAILY_BOOKINGS
```

```ruby
MAX_DAILY_BOOKINGS = 8

def can_book(patient, slot, booked_today)
  return false if patient.nil?
  return false unless slot.open
  booked_today < MAX_DAILY_BOOKINGS
end
```

```typescript
const MAX_DAILY_BOOKINGS = 8;

function canBook(patient: string | null, slot: Slot, bookedToday: number): boolean {
  if (patient === null) return false;
  if (!slot.open) return false;
  return bookedToday < MAX_DAILY_BOOKINGS;
}
```

Legacy code adds a chicken-and-egg problem the catalog alone cannot solve: the worst code
cannot be tested without refactoring (dependencies are hard-wired, everything talks to the
database) and cannot be safely refactored without tests. The escape is a minimal set of
low-risk *enabling* changes — introduce a parameter, extract an interface for a hard-wired
dependency so a test double (Chapter 10) can stand in — done with extreme care, exactly to
the point where a test can grip, and no further.

## 15.4 Technical Debt

The economics underneath all of this has a name. **Technical debt** is the metaphor for
the future cost incurred when you take a shortcut today: like financial debt, it lets you
move faster *now* in exchange for **interest** — and the interest is that *every future
change to that code costs more* than it would have.[^4] The metaphor's precision is its
virtue. Debt is a *deal*, not simply "bad code" — and sometimes the deal is a good one.
**Deliberate debt** is a conscious trade — "we hard-code the tax rule to make the pilot;
we log a ticket to generalize it" — the engineering equivalent of a startup loan, rational
whenever learning fast matters more than building clean, *provided you track it and
service it*. **Inadvertent debt** is the interest you pay on shortcuts you never knew you
took — from inexperience, from requirements that shifted under a once-correct design, or
from Chapter 1's crunch pitfall, where scope silently absorbed through overtime gets paid
for later in weakened structure. Nobody chose it, so nobody tracks it, so it compounds.

Unmanaged, debt's interest payments consume a team's entire capacity: each feature takes
longer, which raises pressure, which invites new shortcuts, which raises interest again.
The management is not "never borrow" — it is to borrow knowingly, keep the debts visible
(a debt register in the backlog, reviewed like any other work), and pay down principal
where you actually pay interest: the high-churn code you touch weekly, not the ugly module
nobody has opened in years. Refactoring (§15.3) is the repayment mechanism, and the
pipeline ([§14.2](../14-delivery/#142-continuous-integration-pipelines)) is what makes
repayment safe enough to do continuously.

## 15.5 Strangler Fig versus Big-Bang Rewrite

What about a system so far gone that the team wants to start over? Chapter 2's troubled
browser rewrite
([§2.6.3](../02-software-development-processes/#263-a-troubled-project)) showed how a
**big-bang rewrite** concentrates risk: you discard the accumulated knowledge embedded in
code that handles a thousand edge cases, you run two systems (one frozen, one imaginary)
for the duration, and the new system's first real validation comes at the end, all at
once. The delivery-era alternative is the **strangler fig** pattern, named for the fig
that grows around a host tree, roots itself, and gradually replaces the host it envelops.[^5]
You place an interception layer — a routing facade — in front of the legacy system, then
peel off one capability at a time: build the new implementation, route that slice of
traffic to it, verify it in production (a canary, [§14.3.2](../14-delivery/#1432-deployment-strategies), at the granularity of a
feature), and retire the old code path. At every moment, you have one *working* system —
part old, part new — and every increment of the rewrite is validated by real use within
weeks of being written. The rewrite becomes a sequence of small, reversible deployments
instead of one giant irreversible bet: the whole argument of Chapter 14, applied to the
biggest change a team ever makes.

## 15.6 Conclusion

Evolution is where Chapter 6's "design for change" either pays its dividend or collects
its debt: systems built with seams, interfaces, and tests bend under years of change;
systems without them become the legacy code someone else must characterize, strangle, and
replace. The working sequence of this chapter is the discipline in miniature: pin current
behavior with characterization tests, refactor only under green, repay debt deliberately
rather than by accident, and when replacement is truly justified, strangle rather than
rewrite. Chapter 14's compression was a rule about *making* change — keep it small, keep
its path to users automatic;
this chapter adds the long-run corollary: **keep the code changeable** — because the one
certainty about a successful system is that it will have to change for longer than anyone
who built it expects.

---

### Sources

[^1]: Robert L. Glass, *Frequently Forgotten Fundamental Facts about Software Engineering* (IEEE Software, 2001). [doi.org](https://doi.org/10.1109/MS.2001.922739).

[^2]: Michael Feathers, *Working Effectively with Legacy Code* (Prentice Hall, 2004). [informit.com](https://www.informit.com/store/working-effectively-with-legacy-code-9780131177055).

[^3]: Martin Fowler, *Catalog of Refactorings*. [refactoring.com](https://refactoring.com/catalog/).

[^4]: Ward Cunningham, *The WyCash Portfolio Management System* (OOPSLA experience report, 1992). [c2.com](http://c2.com/doc/oopsla92.html).

[^5]: Martin Fowler, *StranglerFigApplication* (2004). [martinfowler.com](https://martinfowler.com/bliki/StranglerFigApplication.html).

---

- **Key takeaways** are summarized above in §15.6.
- Continue to the [Exercises](exercises.md).
- Go deeper with the [Open Resources](resources.md) for this chapter.
