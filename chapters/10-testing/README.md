# Chapter 10 — Testing

> **Where we are.** Chapter 9 attacked defects *before* the program runs, with static
> checking, types, and review. This chapter attacks them by *running* the program on
> chosen inputs and comparing what it does against what it should do. Testing cannot
> prove a program correct, but it is the single most practical net for catching the
> defects that reviews miss — and the ones a future change will introduce. The central
> skill is deciding *which* tests to write and knowing when you have written *enough*.

You have already met testing in miniature: run the code, look at the output, decide if
it is right. The trouble is that a real program has more possible inputs than there are
atoms in the universe, so "run it and look" does not scale and does not tell you when to
stop. This chapter turns testing from an art into an engineering activity with
**criteria**: systematic ways to select inputs, to measure how thoroughly you have
exercised the code and its specification, and to justify — to yourself, your team, and
sometimes a regulator — the claim that the software has been tested well enough to ship.

## 10.1 Overview of Testing

At its simplest, a **test** records three things: an *input* or setup, an *expected
property or result*, and the *actual behavior* observed when you run it. The test
**passes** when the observed behavior matches what was expected and **fails** otherwise. A
**test suite** is a collection of tests run together. This sounds trivial, and for one test
it is; the engineering lives in the four
questions the rest of this section raises.

> **Principle.** Testing can reveal the *presence* of defects but never their *absence*.[^1]
> A passing suite means "no defect was triggered by these inputs," not "no defect
> exists." Everything in this chapter is about making that first statement as strong as
> it can practically be.

### 10.1.1 Issues during Testing

Four hard problems recur every time you test anything. Name them now, because the rest of
the chapter is a set of answers to them.

- **Selection.** The input space is astronomically large. Which handful of inputs should
  you actually run? (§10.1.2, and all of §§10.3–10.6.) And once a suite exists: which of
  *its* tests does this change need to run? (§10.1.6.)
- **Adequacy.** Having run some tests, how do you know whether you have run *enough*? What
  is the stopping rule? (§10.1.3.)
- **Oracle.** For each input, how do you decide whether the observed output is *correct*?
  Sometimes that is harder than producing the output. (§10.1.4.)
- **Automation and repeatability.** A test you cannot re-run cheaply is nearly worthless,
  because its main long-term value is catching *regressions* — old defects reintroduced by
  new changes. Manual "click around and see" testing fails this test.

Keep these four in view. A criticism like "your tests are weak" almost always resolves
into one of them: you picked the wrong inputs, you stopped too early, your oracle was too
lax, or your tests do not run automatically.

### 10.1.2 Test Selection

Because you cannot try every input, you must *sample* the input space — and a random or
lazy sample usually misses the inputs most likely to break. Good selection is
**criterion-driven**: you choose a rule that partitions the space of possibilities and
then pick inputs to satisfy the rule. Two great families of criteria run through this
chapter, and they look at the program from opposite sides:

- **Black-box (specification-based)** selection reads the *spec* and ignores the code.
  You pick inputs that represent distinct required behaviors — valid and invalid classes,
  boundaries, combinations (§10.4, §10.6). Its virtue: it finds *missing* code and survives
  a rewrite.
- **White-box (structure-based)** selection reads the *code* and picks inputs that
  exercise its statements, branches, and paths (§10.3, §10.5). Its virtue: it finds code
  the spec-based tests never reached, and it *measures* thoroughness precisely.

Neither subsumes the other. A black-box suite can achieve 100% of every code-coverage
metric and still miss a feature that was never implemented (there is no code to cover). A
white-box suite can cover every branch of the code that *exists* and never notice the
branch that *should* exist. Mature teams use both and measure with both.

### 10.1.3 Test Adequacy: Deciding When to Stop

"We tested it" is not a stopping rule; "we covered every branch, every equivalence class,
and every boundary, and all tests pass" is. A **test-adequacy criterion** (also called a
**coverage criterion**) is a checkable condition that tells you whether a suite is done
*with respect to that criterion*. It converts the vague question "have we tested enough?"
into a countable one.

Most criteria have the shape: *there is a set of things to cover, and the suite is
adequate when it covers all of them.* The "things" might be statements, branches, paths,
equivalence classes, boundaries, or condition-outcome pairs. Coverage is then the
fraction covered:

$$\text{coverage} = \frac{\text{items exercised by the suite}}{\text{total items required by the criterion}}$$

Coverage is a *floor, not a ceiling*: 100% branch coverage means every branch ran, not
that every branch is correct. But low coverage is a genuine alarm — code that never ran
under any test is code you know nothing about empirically.

> **Pitfall.** Do not manage to a coverage number for its own sake. A team told "hit 90%"
> can write assertion-free tests that *execute* code without *checking* it, gaming the
> metric while learning nothing. Coverage is a diagnostic, not a goal; pair it always with
> meaningful oracles (§10.1.4).

### 10.1.4 Test Oracles: Evaluating the Response to a Test

An **oracle** is whatever decides, for a given input, whether the actual output is
correct. In a textbook example the oracle is obvious — you write `assert add(2, 3) == 5`,
and `5` is the oracle. In real systems it is often the hardest part of testing, a
difficulty known as the **oracle problem**.[^2] If you are testing a function that renders a
map, or ranks search results, or predicts weather, what exactly should you compare
against?

Several oracle strategies, from strongest to weakest:

- **Exact expected value.** You know the right answer and hard-code it: `assert
  reverse("abc") == "cba"`. Strongest, but only available when you can compute the answer
  independently.
- **Property / invariant oracle.** You cannot name the exact answer but you know a
  property it must satisfy. For a sort: the output is a permutation of the input and is
  non-decreasing. For encryption: `decrypt(encrypt(x)) == x` (a *round-trip* oracle). These
  power **property-based testing**, where a tool generates many random inputs and checks
  the property on each.
- **Cross-check / differential oracle.** Compare against an independent implementation —
  a slow reference version, a previous release, or a competitor. If they disagree, at
  least one is wrong.
- **Human judgment.** A person inspects the output. Necessary for look-and-feel, but slow,
  non-repeatable, and the enemy of automation — use it sparingly.

Consider a function `median(xs)`. An exact oracle requires you to know the median of each
test list. A cheaper property oracle: after sorting, the result equals the middle element;
and `median(xs) == median(reversed(xs))` (order independence). Property oracles let you
throw thousands of generated inputs at the function without hand-computing each answer —
often the difference between a suite that finds real defects and one that only confirms
the three cases you already thought of.

With a property-based testing tool — every ecosystem has one — both properties become one
test run against hundreds of generated lists:

```generic
// property-based test: a tool generates many non-empty lists xs
function median(xs)
  ys <- sort xs ascending
  return ys[length of ys / 2]   // middle element (upper median)
end function

for each generated non-empty list xs do
  m <- median(xs)
  assert m = median(reverse of xs)   // order independence
  assert xs contains m               // the median is one of the inputs
end for
```

```go
// rapid generates the inputs: go get pgregory.net/rapid
func median(xs []int) int {
	ys := slices.Clone(xs)
	slices.Sort(ys)
	return ys[len(ys)/2] // middle element (upper median)
}

func TestMedianProperties(t *testing.T) {
	rapid.Check(t, func(t *rapid.T) {
		xs := rapid.SliceOfN(rapid.Int(), 1, -1).Draw(t, "xs")
		m := median(xs)
		rev := slices.Clone(xs)
		slices.Reverse(rev)
		if m != median(rev) { // order independence
			t.Errorf("median depends on order: %v", xs)
		}
		if !slices.Contains(xs, m) { // the median is one of the inputs
			t.Errorf("median %d not in %v", m, xs)
		}
	})
}
```

```java
// jqwik generates the inputs: add the net.jqwik:jqwik dependency
import java.util.*;
import net.jqwik.api.*;
import net.jqwik.api.constraints.NotEmpty;

class MedianProperties {
  static int median(List<Integer> xs) {
    var ys = new ArrayList<>(xs);
    Collections.sort(ys);
    return ys.get(ys.size() / 2);                // middle element (upper median)
  }

  @Property
  boolean medianProperties(@ForAll @NotEmpty List<Integer> xs) {
    var rev = new ArrayList<>(xs);
    Collections.reverse(rev);
    return median(xs) == median(rev)             // order independence
        && xs.contains(median(xs));              // the median is one of the inputs
  }
}
```

```javascript
// fast-check generates the inputs: npm install fast-check
const fc = require("fast-check");

function median(xs) {
  const ys = xs.toSorted((a, b) => a - b);
  return ys[Math.floor(xs.length / 2)];   // middle element (upper median)
}

fc.assert(
  fc.property(fc.array(fc.integer(), { minLength: 1 }), (xs) => {
    const m = median(xs);
    return m === median(xs.toReversed())  // order independence
      && xs.includes(m);                  // the median is one of the inputs
  })
);
```

```python
# Hypothesis generates the inputs: pip install hypothesis
from hypothesis import given, strategies as st

def median(xs):
  return sorted(xs)[len(xs) // 2]          # middle element (upper median)

@given(st.lists(st.integers(), min_size=1))
def test_median_properties(xs):
  m = median(xs)
  assert m == median(list(reversed(xs)))   # order independence
  assert m in xs                           # the median is one of the inputs
```

```ruby
# PropCheck generates the inputs: gem install prop_check
require "prop_check"
G = PropCheck::Generators

def median(xs)
  xs.sort[xs.length / 2]                     # middle element (upper median)
end

PropCheck.forall(G.array(G.integer, empty: false)) do |xs|
  m = median(xs)
  raise "order dependence" unless m == median(xs.reverse)  # order independence
  raise "median not in xs" unless xs.include?(m)   # the median is one of the inputs
end
```

```typescript
// fast-check generates the inputs: npm install fast-check
import fc from "fast-check";

function median(xs: number[]): number {
  const ys = xs.slice().sort((a, b) => a - b);
  return ys[Math.floor(xs.length / 2)];   // middle element (upper median)
}

fc.assert(
  fc.property(fc.array(fc.integer(), { minLength: 1 }), (xs: number[]): boolean => {
    const m = median(xs);
    return m === median(xs.slice().reverse())  // order independence
      && xs.includes(m);                       // the median is one of the inputs
  })
);
```

### 10.1.5 Mutation Testing: Grading Your Suite

Coverage tells you what your tests *ran*; it cannot tell you what they would *catch*. The
pitfall in §10.1.3 — assertion-free tests that execute everything and check nothing —
scores 100% on any coverage criterion while detecting no defects at all. **Mutation
testing** closes that gap by testing the tests.[^3] A mutation tool takes your working code
and plants small, deliberate defects called **mutants**: flip a `<` to `<=`, change a
constant by one, negate a condition, delete a statement. Each mutant is a plausible bug —
exactly the kind a tired programmer writes. The tool then reruns your suite against each
mutant in turn:

- If at least one test **fails**, the suite noticed the defect: the mutant is **killed**.
- If every test still **passes**, the mutant is a **survivor** — your suite executed the
  broken line and did not notice.

The **mutation score** — mutants killed divided by mutants generated — grades your
suite's defect-detecting strength in a way coverage never can. Better, nearly every survivor is
*actionable*: it points at a specific line where an assertion is weak or missing.

Watch it work on the discount function, the worked example you will meet in §10.2.1. Suppose
the tool mutates the guard
`price < 0` into `price <= 0`, so a price of exactly zero is now (wrongly) rejected.
Rerun the suite: no test ever passes a zero price, so every test still passes and the
mutant **survives**. The survivor names the missing test precisely:

```generic
// kills the `price <= 0` mutant: exercises a price of exactly zero
function test_free_item_allowed()
  assert apply_discount(0.0, 50) = 0.0
end function
```

```go
func TestFreeItemAllowed(t *testing.T) { // kills the `price <= 0` mutant
	if got, err := ApplyDiscount(0.0, 50); err != nil || got != 0.0 {
		t.Errorf("got %v, %v; want 0.0", got, err)
	}
}
```

```java
@Test void freeItemAllowed() {
  assertEquals(0.0, applyDiscount(0.0, 50));   // kills the `price <= 0` mutant
}
```

```javascript
test("free item allowed", () => {
  assert.equal(applyDiscount(0.0, 50), 0.0);   // kills the `price <= 0` mutant
});
```

```python
def test_free_item_allowed():
  assert apply_discount(0.0, 50) == 0.0    # kills the `price <= 0` mutant
```

```ruby
def test_free_item_allowed
  assert_equal(0.0, apply_discount(0.0, 50))   # kills the `price <= 0` mutant
end
```

```typescript
test("free item allowed", () => {
  assert.equal(applyDiscount(0.0, 50), 0.0);   // kills the `price <= 0` mutant
});
```

Add it, rerun, and the mutant dies — and, not coincidentally, you have just written the
boundary-value test (§10.4.2) your suite was missing. Mature tools exist in every
ecosystem: **go-mutesting** for Go, **PIT** for Java, **Stryker** for JavaScript and
TypeScript, **mutmut** for Python, **mutant** for Ruby.

> **Pitfall — mutation testing is expensive.** Each mutant means rerunning the suite, and
> a modest module can generate hundreds of mutants, so a full run can take hours. Do not
> put it on every commit. Use it selectively — on critical modules, on changed code, or
> in a periodic job — and treat the survivors it reports as a curated to-do list for your
> suite, not a number to chase.

### 10.1.6 Selecting from the Suite: Regression Selection and Prioritization

Everything so far selects *inputs* — it builds the suite. A second selection problem
appears once the suite exists and keeps growing: on every change, *which of the tests you
already have should run, and in what order?* Early in a project the answer is "all of
them, every time," and you should keep that answer for as long as you can. But suites
grow with their codebase, and eventually the full run no longer fits the feedback loop it
exists to power — one industrial team reported a suite that took seven weeks to run in
full.[^4] The moment there is a budget, three techniques share the work, and the
vocabulary is worth knowing:

- **Minimization** permanently deletes tests that no longer earn their runtime: redundant
  (everything they exercise, another test also exercises) or obsolete (the behavior they
  check no longer exists).
- **Selection** picks, per change, the subset of tests relevant to what changed. A CSS
  change does not need the payroll calculation suite — *if* you can establish which tests
  a change can possibly affect.
- **Prioritization** keeps every test but orders the run so likely failures come first.
  Feedback arrives when the first test *fails*, not when the last one passes; researchers
  score an ordering by its rate of fault detection (APFD).[^4]

The subtle point is that a time budget changes what "best" means. Suppose your merge gate
has a ten-minute budget ([§14.2.4](../14-delivery/#1424-keeping-pipelines-fast)), and
history gives you a value estimate for each test — say, the distinct regressions each one
has caught over the past year:

| Test | Regressions caught | Runtime |
|------|-------------------:|--------:|
| `T1` | 9                  | 9 min   |
| `T2` | 4                  | 3 min   |
| `T3` | 4                  | 4 min   |
| `T4` | 3                  | 3 min   |

The obvious greedy rule — most valuable test first — spends nine of the ten minutes on
`T1`, for nine regressions' worth of protection. Selecting *against the budget* runs
`T2`, `T3`, and `T4` instead: eleven regressions' worth in the same ten minutes. This is
the **0/1 knapsack problem** — each test an item with a weight (its runtime) and a value;
maximize value within the budget — which is NP-complete, and the real problem is harder
still, because test values *overlap*: two tests that exercise the same code catch the
same defects, so a selection's value is less than the sum of its parts. Practical
approaches therefore lean on heuristics and search — knapsack approximations and genetic
algorithms have both been studied[^5] — and large CI systems apply the same idea as
**predictive test selection**, weighting each test by its failure history and its
relevance to the changed files.

> **Principle.** A test budget is a constraint to design against, not permission to skip
> testing quietly. Decide explicitly what runs at the merge gate and what runs
> continuously behind it (§14.2.4), and never let "the suite is slow" drift into "we
> don't run the suite."

## 10.2 Levels of Testing

Testing happens at several *levels*, distinguished by how much of the system is under
test at once. Each level answers a different question and catches a different class of
defect, and the levels are complementary, not redundant.

### 10.2.1 Unit Testing

A **unit test** exercises the smallest independently testable piece — typically one
function, method, or class — *in isolation* from the rest of the system. Its dependencies
are replaced by **test doubles**: a **stub** returns canned answers, a **mock**
additionally records how it was called and lets you assert on those calls, and a **fake**
is a lightweight working implementation (an in-memory database standing in for the real
one).

Each double below stands in for the `discounts` dependency of `PriceService` (§10.2.2) —
the stub feeds the unit a canned percent and nothing more:

```generic
// a stub returns canned answers, nothing more
function stub_catalog.price_of(item)
  return 12.0        // every item costs 12.0
end function

function stub_discounts.percent_for(item)
  return 25          // canned answer, whatever the item
end function

svc <- new PriceService(stub_catalog, stub_discounts)
assert svc.quote("mug") = 9.0   // 12.0 * (1 - 0.25)
```

```go
type StubCatalog struct{}

func (StubCatalog) PriceOf(item string) float64 { return 12.0 } // every item costs 12.0

type StubDiscounts struct{}

func (StubDiscounts) PercentFor(item string) float64 { return 25 } // canned answer

func TestStubFeedsCannedPercent(t *testing.T) {
	svc := NewPriceService(StubCatalog{}, StubDiscounts{})
	if got, err := svc.Quote("mug"); err != nil || got != 9.0 {
		t.Errorf("got %v, %v; want 9.0", got, err) // 12.0 * (1 - 0.25)
	}
}
```

```java
class StubCatalog implements Catalog {
  public double priceOf(String item) { return 12.0; }  // every item costs 12.0
}

class StubDiscounts implements Discounts {
  public int percentFor(String item) { return 25; }    // canned answer, whatever the item
}

var svc = new PriceService(new StubCatalog(), new StubDiscounts());
assert svc.quote("mug") == 9.0;                  // 12.0 * (1 - 0.25)
```

```javascript
class StubCatalog {
  priceOf(item) { return 12.0; }        // every item costs 12.0
}

class StubDiscounts {
  percentFor(item) { return 25; }       // canned answer, whatever the item
}

const svc = new PriceService(new StubCatalog(), new StubDiscounts());
assert.equal(svc.quote("mug"), 9.0);             // 12.0 * (1 - 0.25)
```

```python
class StubCatalog:
  def price_of(self, item): return 12.0        # every item costs 12.0

class StubDiscounts:
  def percent_for(self, item): return 25       # canned answer, whatever the item

svc = PriceService(StubCatalog(), StubDiscounts())
assert svc.quote("mug") == 9.0                   # 12.0 * (1 - 0.25)
```

```ruby
class StubCatalog
  def price_of(item) = 12.0        # every item costs 12.0
end

class StubDiscounts
  def percent_for(item) = 25       # canned answer, whatever the item
end

svc = PriceService.new(StubCatalog.new, StubDiscounts.new)
raise unless svc.quote("mug") == 9.0             # 12.0 * (1 - 0.25)
```

```typescript
class StubCatalog implements Catalog {
  priceOf(item: string): number { return 12.0; }   // every item costs 12.0
}

class StubDiscounts implements Discounts {
  percentFor(item: string): number { return 25; }  // canned answer, any item
}

const svc = new PriceService(new StubCatalog(), new StubDiscounts());
assert.equal(svc.quote("mug"), 9.0);             // 12.0 * (1 - 0.25)
```

The mock also records the interaction, so the test can assert on *how* the unit used it:

```generic
// a mock also records how it was called
mock_discounts.calls <- empty list

function mock_discounts.percent_for(item)
  append item to mock_discounts.calls
  return 25
end function

new PriceService(stub_catalog, mock_discounts).quote("mug")
assert mock_discounts.calls = ["mug"]   // called exactly once, with "mug"
```

```go
type MockDiscounts struct{ calls []string }

func (m *MockDiscounts) PercentFor(item string) float64 {
	m.calls = append(m.calls, item)
	return 25
}

func TestMockRecordsInteraction(t *testing.T) {
	mock := &MockDiscounts{}
	NewPriceService(StubCatalog{}, mock).Quote("mug")
	if !slices.Equal(mock.calls, []string{"mug"}) { // called exactly once, with "mug"
		t.Errorf("calls = %v; want [mug]", mock.calls)
	}
}
```

```java
class MockDiscounts implements Discounts {
  final List<String> calls = new ArrayList<>();
  public int percentFor(String item) {
    calls.add(item);
    return 25;
  }
}

var mock = new MockDiscounts();
new PriceService(new StubCatalog(), mock).quote("mug");
assert mock.calls.equals(List.of("mug"));        // called exactly once, with "mug"
```

```javascript
class MockDiscounts {
  calls = [];
  percentFor(item) {
    this.calls.push(item);
    return 25;
  }
}

const mock = new MockDiscounts();
new PriceService(new StubCatalog(), mock).quote("mug");
assert.deepEqual(mock.calls, ["mug"]);           // called exactly once, with "mug"
```

```python
class MockDiscounts:
  def __init__(self): self.calls = []
  def percent_for(self, item):
    self.calls.append(item)
    return 25

mock = MockDiscounts()
PriceService(StubCatalog(), mock).quote("mug")
assert mock.calls == ["mug"]                     # called exactly once, with "mug"
```

```ruby
class MockDiscounts
  attr_reader :calls
  def initialize = @calls = []
  def percent_for(item)
    @calls << item
    25
  end
end

mock = MockDiscounts.new
PriceService.new(StubCatalog.new, mock).quote("mug")
raise unless mock.calls == ["mug"]               # called exactly once, with "mug"
```

```typescript
class MockDiscounts implements Discounts {
  calls: string[] = [];
  percentFor(item: string): number {
    this.calls.push(item);
    return 25;
  }
}

const mock = new MockDiscounts();
new PriceService(new StubCatalog(), mock).quote("mug");
assert.deepEqual(mock.calls, ["mug"]);           // called exactly once, with "mug"
```

And the fake actually works — an in-memory table stands in for the discount database, so
any lookup behaves the way the real component would:

```generic
// a fake is a working stand-in: an in-memory table of discounts
function fake_discounts.percent_for(item)
  if item in table then
    return table[item]
  else
    return 0          // a missing item means no discount
  end if
end function

svc <- new PriceService(stub_catalog, fake_discounts with table {"mug": 25})
assert svc.quote("mug") = 9.0
assert svc.quote("bowl") = 12.0   // unknown item: no discount
```

```go
// FakeDiscounts reads an in-memory table; a missing item means no discount (0).
type FakeDiscounts struct{ table map[string]float64 }

func (f FakeDiscounts) PercentFor(item string) float64 { return f.table[item] }

func TestFakeBehavesLikeRealTable(t *testing.T) {
	svc := NewPriceService(StubCatalog{}, FakeDiscounts{map[string]float64{"mug": 25}})
	if got, _ := svc.Quote("mug"); got != 9.0 {
		t.Errorf("mug: got %v; want 9.0", got)
	}
	if got, _ := svc.Quote("bowl"); got != 12.0 { // unknown item: no discount
		t.Errorf("bowl: got %v; want 12.0", got)
	}
}
```

```java
class FakeDiscounts implements Discounts {
  final Map<String, Integer> table;              // in-memory stand-in
  FakeDiscounts(Map<String, Integer> table) { this.table = new HashMap<>(table); }
  public int percentFor(String item) { return table.getOrDefault(item, 0); }
}

var svc = new PriceService(new StubCatalog(), new FakeDiscounts(Map.of("mug", 25)));
assert svc.quote("mug") == 9.0;
assert svc.quote("bowl") == 12.0;                // unknown item: no discount
```

```javascript
class FakeDiscounts {
  constructor(table) { this.table = { ...table }; }   // in-memory stand-in
  percentFor(item) { return this.table[item] ?? 0; }
}

const svc = new PriceService(new StubCatalog(), new FakeDiscounts({ mug: 25 }));
assert.equal(svc.quote("mug"), 9.0);
assert.equal(svc.quote("bowl"), 12.0);           // unknown item: no discount
```

```python
class FakeDiscounts:
  def __init__(self, table): self.table = dict(table)      # in-memory stand-in
  def percent_for(self, item): return self.table.get(item, 0)

svc = PriceService(StubCatalog(), FakeDiscounts({"mug": 25}))
assert svc.quote("mug") == 9.0
assert svc.quote("bowl") == 12.0                 # unknown item: no discount
```

```ruby
class FakeDiscounts
  def initialize(table) = @table = table.dup     # in-memory stand-in
  def percent_for(item) = @table.fetch(item, 0)
end

svc = PriceService.new(StubCatalog.new, FakeDiscounts.new("mug" => 25))
raise unless svc.quote("mug") == 9.0
raise unless svc.quote("bowl") == 12.0           # unknown item: no discount
```

```typescript
class FakeDiscounts implements Discounts {
  private table: Record<string, number>;
  constructor(table: Record<string, number>) { this.table = { ...table }; }  // stand-in
  percentFor(item: string): number { return this.table[item] ?? 0; }
}

const svc = new PriceService(new StubCatalog(), new FakeDiscounts({ mug: 25 }));
assert.equal(svc.quote("mug"), 9.0);
assert.equal(svc.quote("bowl"), 12.0);           // unknown item: no discount
```

Unit tests are the workhorses of a suite because they are *fast*, *precise*, and *stable*:
fast because they touch no network or disk, precise because a failure points at one unit,
and stable because they do not break when an unrelated part of the system changes. Here is
a unit under test and a small suite:

```generic
// reduce price by percent (0..100); reject bad input
function apply_discount(price, percent)
  if price < 0 then
    error "price must be non-negative"
  end if
  if percent < 0 or percent > 100 then
    error "percent must be in 0..100"
  end if
  return round(price * (1 - percent / 100) to 2 decimals)
end function
```

```go
// ApplyDiscount reduces price by percent (0..100). Returns an error on bad input.
func ApplyDiscount(price, percent float64) (float64, error) {
	if price < 0 {
		return 0, errors.New("price must be non-negative")
	}
	if percent < 0 || percent > 100 {
		return 0, errors.New("percent must be in 0..100")
	}
	return math.Round(price*(1-percent/100)*100) / 100, nil
}
```

```java
/** Reduce price by percent (0..100). Throws IllegalArgumentException on bad input. */
static double applyDiscount(double price, double percent) {
  if (price < 0) throw new IllegalArgumentException("price must be non-negative");
  if (percent < 0 || percent > 100)
    throw new IllegalArgumentException("percent must be in 0..100");
  return Math.round(price * (1 - percent / 100) * 100) / 100.0;
}
```

```javascript
// Reduce price by percent (0..100). Throws RangeError on bad input.
function applyDiscount(price, percent) {
  if (price < 0) throw new RangeError("price must be non-negative");
  if (percent < 0 || percent > 100) throw new RangeError("percent must be in 0..100");
  return Math.round(price * (1 - percent / 100) * 100) / 100;
}
```

```python
def apply_discount(price, percent):
  """Reduce price by percent (0..100). Raises ValueError on bad input."""
  if price < 0:
    raise ValueError("price must be non-negative")
  if percent < 0 or percent > 100:
    raise ValueError("percent must be in 0..100")
  return round(price * (1 - percent / 100), 2)
```

```ruby
# Reduce price by percent (0..100). Raises ArgumentError on bad input.
def apply_discount(price, percent)
  raise ArgumentError, "price must be non-negative" if price < 0
  raise ArgumentError, "percent must be in 0..100" unless (0..100).cover?(percent)
  (price * (1 - percent / 100.0)).round(2)
end
```

```typescript
// Reduce price by percent (0..100). Throws RangeError on bad input.
function applyDiscount(price: number, percent: number): number {
  if (price < 0) throw new RangeError("price must be non-negative");
  if (percent < 0 || percent > 100) throw new RangeError("percent must be in 0..100");
  return Math.round(price * (1 - percent / 100) * 100) / 100;
}
```

```generic
// each case names a distinct behavior and carries its own oracle
cases <- [
  ("no discount",     100.0,   0, 100.0),
  ("half off",        143.0,  50,  71.5),
  ("rounds to cents",   9.99,  10,   8.99),
  ("full discount",    40.0, 100,   0.0),
]
for each (name, price, percent, want) in cases do
  assert apply_discount(price, percent) = want
end for

// invalid class: percent above 100 is rejected
assert apply_discount(100.0, 150) raises an error
```

```go
func TestApplyDiscount(t *testing.T) {
	cases := []struct {
		name                 string
		price, percent, want float64
	}{
		{"no discount", 100.0, 0, 100.0},
		{"half off", 143.0, 50, 71.5},
		{"rounds to cents", 9.99, 10, 8.99},
		{"full discount", 40.0, 100, 0.0},
	}
	for _, c := range cases {
		t.Run(c.name, func(t *testing.T) {
			if got, err := ApplyDiscount(c.price, c.percent); err != nil || got != c.want {
				t.Errorf("got %v, %v; want %v", got, err, c.want)
			}
		})
	}
}

func TestRejectsBadPercent(t *testing.T) {
	if _, err := ApplyDiscount(100.0, 150); err == nil {
		t.Error("want error for percent 150, got nil")
	}
}
```

```java
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class ApplyDiscountTest {
  @Test void noDiscount()    { assertEquals(100.0, applyDiscount(100.0, 0)); }
  @Test void halfOff()       { assertEquals(71.5, applyDiscount(143.0, 50)); }
  @Test void roundsToCents() { assertEquals(8.99, applyDiscount(9.99, 10)); }
  @Test void fullDiscount()  { assertEquals(0.0, applyDiscount(40.0, 100)); }
  @Test void rejectsBadPercent() {
    assertThrows(IllegalArgumentException.class, () -> applyDiscount(100.0, 150));
  }
}
```

```javascript
const test = require("node:test");
const assert = require("node:assert/strict");

test("no discount", () => assert.equal(applyDiscount(100.0, 0), 100.0));
test("half off", () => assert.equal(applyDiscount(143.0, 50), 71.5));
test("rounds to cents", () => assert.equal(applyDiscount(9.99, 10), 8.99));
test("full discount", () => assert.equal(applyDiscount(40.0, 100), 0.0));
test("rejects bad percent", () => {
  assert.throws(() => applyDiscount(100.0, 150), RangeError);
});
```

```python
def test_no_discount():        assert apply_discount(100.0, 0)   == 100.0
def test_half_off():           assert apply_discount(143.0, 50)  == 71.5
def test_rounds_to_cents():    assert apply_discount(9.99, 10)   == 8.99
def test_full_discount():      assert apply_discount(40.0, 100)  == 0.0
def test_rejects_bad_percent():
  import pytest
  with pytest.raises(ValueError):
    apply_discount(100.0, 150)
```

```ruby
require "minitest/autorun"

class TestApplyDiscount < Minitest::Test
  def test_no_discount     = assert_equal(100.0, apply_discount(100.0, 0))
  def test_half_off        = assert_equal(71.5, apply_discount(143.0, 50))
  def test_rounds_to_cents = assert_equal(8.99, apply_discount(9.99, 10))
  def test_full_discount   = assert_equal(0.0, apply_discount(40.0, 100))

  def test_rejects_bad_percent
    assert_raises(ArgumentError) { apply_discount(100.0, 150) }
  end
end
```

```typescript
import test from "node:test";
import assert from "node:assert/strict";

test("no discount", () => assert.equal(applyDiscount(100.0, 0), 100.0));
test("half off", () => assert.equal(applyDiscount(143.0, 50), 71.5));
test("rounds to cents", () => assert.equal(applyDiscount(9.99, 10), 8.99));
test("full discount", () => assert.equal(applyDiscount(40.0, 100), 0.0));
test("rejects bad percent", () => {
  assert.throws(() => applyDiscount(100.0, 150), RangeError);
});
```

Each test names a distinct behavior and carries its own oracle (the expected value or the
expected exception). Notice we are already thinking about selection: 0 and 100 are the
*boundaries* of the valid percent range (§10.4.2), and 150 is an invalid class.

What makes a unit test *good*? The **FIRST** mnemonic names five properties worth
enforcing on every test you write:[^6]

- **F**ast — milliseconds, so the whole suite runs on every save;
- **I**ndependent — no shared state and no required order, so any subset runs alone and
  a failure implicates exactly one test;
- **R**epeatable — the same result on every run and every machine, with no dependence on
  network, clock, or leftover environment;
- **S**elf-validating — the test asserts its own pass or fail, carrying its oracle
  (§10.1.4) instead of printing output for a human to eyeball;
- **T**imely — written with (or before —
  [§2.3.2](../02-software-development-processes/#232-testing-make-it-central-to-development))
  the code it tests, while the design can still respond to what testing reveals.

### 10.2.2 Integration Testing

Units that each pass in isolation can still fail *together* — one returns meters where the
other expects feet, one returns a null value where the other never checks. **Integration
testing** exercises the *interfaces and interactions* between units, growing the scope from
a pair of collaborators up toward whole subsystems. This is where mismatched assumptions,
wrong data formats, and protocol errors surface.

```generic
// PriceService wires two collaborators together
// catalog: name -> base price;  discounts: name -> percent off
function PriceService.quote(item)
  base <- catalog.price_of(item)      // unit A
  pct <- discounts.percent_for(item)  // unit B
  return apply_discount(base, pct)
end function
```

```go
type Catalog interface{ PriceOf(item string) float64 }
type Discounts interface{ PercentFor(item string) float64 }

type PriceService struct {
	catalog   Catalog   // unit A: name -> base price
	discounts Discounts // unit B: name -> percent off
}

func (s PriceService) Quote(item string) (float64, error) {
	base := s.catalog.PriceOf(item)
	pct := s.discounts.PercentFor(item)
	return ApplyDiscount(base, pct)
}
```

```java
class PriceService {
  private final Catalog catalog;      // unit A: name -> base price
  private final Discounts discounts;  // unit B: name -> percent off

  PriceService(Catalog catalog, Discounts discounts) {
    this.catalog = catalog;
    this.discounts = discounts;
  }

  double quote(String item) {
    double base = catalog.priceOf(item);
    double pct = discounts.percentFor(item);
    return applyDiscount(base, pct);
  }
}
```

```javascript
class PriceService {
  constructor(catalog, discounts) {
    this.catalog = catalog;        // unit A: name -> base price
    this.discounts = discounts;    // unit B: name -> percent off
  }

  quote(item) {
    const base = this.catalog.priceOf(item);
    const pct = this.discounts.percentFor(item);
    return applyDiscount(base, pct);
  }
}
```

```python
class PriceService:
  def __init__(self, catalog, discounts):
    self.catalog = catalog          # unit A: name -> base price
    self.discounts = discounts      # unit B: name -> percent off

  def quote(self, item):
    base = self.catalog.price_of(item)
    pct = self.discounts.percent_for(item)
    return apply_discount(base, pct)
```

```ruby
class PriceService
  def initialize(catalog, discounts)
    @catalog = catalog        # unit A: name -> base price
    @discounts = discounts    # unit B: name -> percent off
  end

  def quote(item)
    base = @catalog.price_of(item)
    pct = @discounts.percent_for(item)
    apply_discount(base, pct)
  end
end
```

```typescript
interface Catalog { priceOf(item: string): number; }
interface Discounts { percentFor(item: string): number; }

class PriceService {
  catalog: Catalog;      // unit A: name -> base price
  discounts: Discounts;  // unit B: name -> percent off
  constructor(catalog: Catalog, discounts: Discounts) {
    this.catalog = catalog;
    this.discounts = discounts;
  }

  quote(item: string): number {
    const base = this.catalog.priceOf(item);
    const pct = this.discounts.percentFor(item);
    return applyDiscount(base, pct);
  }
}
```

A unit test of `PriceService`'s quote method would *mock* `catalog` and `discounts`. An
**integration test** instead wires the real (or fake) catalog and discount components
together and checks that their contract holds end to end:

```generic
// integration test: wire the real catalog and discounts together
function test_quote_integrates_catalog_and_discounts()
  catalog <- new Catalog with table {"mug": 12.0}
  discounts <- new Discounts with table {"mug": 25}
  svc <- new PriceService(catalog, discounts)
  assert svc.quote("mug") = 9.0   // 12.0 * (1 - 0.25)
end function
```

```go
func TestQuoteIntegratesCatalogAndDiscounts(t *testing.T) {
	catalog := MapCatalog{"mug": 12.0}
	discounts := MapDiscounts{"mug": 25}
	svc := PriceService{catalog, discounts}
	got, err := svc.Quote("mug")
	if err != nil || got != 9.0 { // 12.0 * (1 - 0.25)
		t.Errorf("got %v, %v; want 9.0", got, err)
	}
}
```

```java
import static org.junit.jupiter.api.Assertions.*;
import java.util.Map;
import org.junit.jupiter.api.Test;

class PriceServiceIntegrationTest {
  @Test void quoteIntegratesCatalogAndDiscounts() {
    Catalog catalog = new Catalog(Map.of("mug", 12.0));
    Discounts discounts = new Discounts(Map.of("mug", 25.0));
    PriceService svc = new PriceService(catalog, discounts);
    assertEquals(9.0, svc.quote("mug"));  // 12.0 * (1 - 0.25)
  }
}
```

```javascript
const test = require("node:test");
const assert = require("node:assert/strict");

test("quote integrates catalog and discounts", () => {
  const catalog = new Catalog({ mug: 12.0 });
  const discounts = new Discounts({ mug: 25 });
  const svc = new PriceService(catalog, discounts);
  assert.equal(svc.quote("mug"), 9.0);  // 12.0 * (1 - 0.25)
});
```

```python
def test_quote_integrates_catalog_and_discounts():
  catalog = Catalog({"mug": 12.0})
  discounts = Discounts({"mug": 25})
  svc = PriceService(catalog, discounts)
  assert svc.quote("mug") == 9.0     # 12.0 * (1 - 0.25)
```

```ruby
require "minitest/autorun"

class TestPriceServiceIntegration < Minitest::Test
  def test_quote_integrates_catalog_and_discounts
    catalog = Catalog.new({ "mug" => 12.0 })
    discounts = Discounts.new({ "mug" => 25 })
    svc = PriceService.new(catalog, discounts)
    assert_equal(9.0, svc.quote("mug"))  # 12.0 * (1 - 0.25)
  end
end
```

```typescript
import test from "node:test";
import assert from "node:assert/strict";

test("quote integrates catalog and discounts", () => {
  const catalog = new Catalog({ mug: 12.0 });
  const discounts = new Discounts({ mug: 25 });
  const svc = new PriceService(catalog, discounts);
  assert.equal(svc.quote("mug"), 9.0);  // 12.0 * (1 - 0.25)
});
```

If `Discounts` returned a *fraction* (0.25) while the discount function expects a *percentage*
(25), every unit test could pass while this integration test correctly fails. That
interface mismatch is the defect class unit tests are blind to.

### 10.2.3 Functional, System, and Acceptance Testing

Higher levels test the assembled product against ever-broader notions of "correct":

- **Functional testing** checks that a complete feature behaves per its specification,
  treating the system as a black box: *given a shopping cart with these items and this
  coupon, the checkout total is X.* It spans many units but is scoped to one function of
  the product.
- **System testing** exercises the *entire, integrated* system in a production-like
  environment, including **non-functional** requirements — performance, security,
  reliability, usability. "The page loads in under 500 ms at 1,000 concurrent users" is a
  system-level test.
- **Acceptance testing** answers the customer's question, "will I sign for this?" It is
  run against the customer's own criteria, often *by* or *with* the customer.
  **User acceptance testing (UAT)** uses real users and realistic tasks; **alpha/beta**
  releases are acceptance testing in the wild.

A useful way to remember the difference: functional and system testing ask *"did we build
the product right?"* (verification), while acceptance testing asks *"did we build the
right product?"* (validation).[^7] Both matter, and passing one is no guarantee of the
other.

> **From acceptance criteria to acceptance tests.** The **Given / When / Then** scenarios
> you wrote as a story's acceptance criteria ([§3.4.1](../03-user-requirements/#341-guidelines-for-effective-user-stories))
> *are* your acceptance tests. In **Behavior-Driven Development (BDD)**, those **Gherkin**
> `.feature` scenarios are made executable by tools like **Cucumber**, **behave**, or
> **SpecFlow/Reqnroll**: each `Given`/`When`/`Then` step binds to code, so the customer-readable
> specification runs on every build. This is functional/acceptance testing whose oracle
> (§10.1.4) is the agreed scenario itself.

One more system-level suite gets its own name because you will run it constantly. A
**smoke test** is a fast, shallow pass that answers a single question: *is the build
fundamentally alive?* The app starts, the homepage loads, a user can log in — nothing
deeper. The name comes from hardware bring-up: power the board on and see whether smoke
comes out before bothering with finer measurements.[^8] Smoke tests run immediately after a
build or a deployment, as a *gate*: if they fail, the build is dead on arrival, no deeper
(and more expensive) testing is worth starting, and a deploy must not proceed.[^9] Chapter 14
gives them a formal home as a stage of the delivery pipeline, run right after each deploy
([§14.2.2](../14-delivery/#1422-the-stages-of-a-pipeline)).

### 10.2.4 Case Study: Test Early and Often — the Testing Pyramid

The levels are not equally cheap. A good unit test runs in milliseconds and almost never
flakes; a
full end-to-end (E2E) test may spin up a browser, a database, and three services, take
minutes, and fail intermittently for reasons that have nothing to do with your code.
This cost gradient motivates the **testing pyramid**: have *many* fast unit tests, *fewer*
integration tests, and *only a handful* of slow end-to-end tests.[^10]

```mermaid
flowchart TD
    E["End-to-End / UI tests<br/>few · slow · brittle · high confidence per test"]
    I["Integration / service tests<br/>some · medium speed"]
    U["Unit tests<br/>many · fast · precise · cheap"]
    E --- I --- U
    classDef top fill:#fdd,stroke:#c66,color:#000;
    classDef mid fill:#ffd,stroke:#cc6,color:#000;
    classDef bot fill:#dfd,stroke:#6c6,color:#000;
    class E top; class I mid; class U bot;
```

The pyramid is an economic argument. Suppose a defect in the discount logic could be
caught at any level. Caught by a unit test, the feedback arrives in seconds, on the exact
line, before you even commit. Caught by an E2E test in CI, it arrives twenty minutes
later as "checkout total was wrong," and you must *debug down* to the line. Caught in
production, it arrives as a customer complaint and a refund. The cost of a defect
typically rises substantially with each stage it survives — the exact multiplier varies
by domain, tooling, and release process (§2.4.2) — so you push detection as far *down*
and *early* as it will go.[^11]

> **Pitfall — the ice-cream cone.** Teams that skip unit tests and lean on a big pile of
> slow, flaky E2E tests invert the pyramid into an "ice-cream cone." Their CI is slow,
> failures are hard to localize, and developers learn to ignore red builds ("probably just
> flaky"). An ignored test suite protects nothing. Prefer the pyramid deliberately.

Because flakiness is what poisons trust, know its causes. A **flaky test** — one that
passes and fails across runs with no code change — most often traces to one of four
roots: **race conditions and async timing** (the assertion runs before the work
finishes); **shared mutable state** between tests (one test's leftovers change another's
result); **test-order dependence** (the suite passes in one order and fails in another);
or **unstable external dependencies** (real networks, real clocks, third-party services).[^12]
The fixes mirror the causes: isolate state so each test builds and tears down its own
world; make tests order-independent (and let the runner randomize order to prove it);
await asynchronous work properly with sane timeouts instead of sleeping and hoping; and
replace or fake unstable dependencies. For the incorrigible case, **quarantine** the test
out of the gating suite — then fix it or delete it, because a test allowed to stay
red-then-green trains the team to ignore the suite.

"Test early and often" also means testing *continuously*: run the fast tests on every
save, the full suite on every push, and treat a broken build as a stop-the-line event.
This is the testing half of **continuous integration** (Chapter 2) — the discipline that
keeps the "make change cheap" promise from Chapter 1 honest. Chapter 14 assembles these
tests, with the static checks of Chapter 9, into the full delivery pipeline.

## 10.3 Code Coverage I: White-Box Testing

White-box testing selects inputs by looking at the code's *structure*. To talk about
structure precisely, we model a function as a graph.

### 10.3.1 Control-Flow Graphs

A **control-flow graph (CFG)** represents a function as a directed graph: **nodes** are
basic blocks (maximal straight-line sequences of statements), and **edges** are the
possible transfers of control between them. A branch (an `if`, a loop condition) is a node
with two outgoing edges; a merge is a node with two incoming edges. The CFG makes
"statements," "branches," and "paths" into things you can *count*.

Consider a function that classifies a number and, for positive numbers, sums 1..n:

```generic
function classify_and_sum(n)      // node 1  (entry)
  if n < 0 then                   // node 2  (decision)
    return "negative"             // node 3
  end if
  total <- 0                       // node 4
  i <- 1                           // node 4
  while i <= n do                 // node 5  (decision)
    total <- total + i             // node 6
    i <- i + 1                     // node 6
  end while
  return "sum=" + total           // node 7  (exit)
end function
```

```go
func ClassifyAndSum(n int) string { // node 1  (entry)
	if n < 0 { // node 2  (decision)
		return "negative" // node 3
	}
	total := 0   // node 4
	i := 1       // node 4
	for i <= n { // node 5  (decision)
		total += i // node 6
		i++        // node 6
	}
	return fmt.Sprintf("sum=%d", total) // node 7  (exit)
}
```

```java
static String classifyAndSum(int n) {  // node 1  (entry)
  if (n < 0) {                         // node 2  (decision)
    return "negative";                 // node 3
  }
  int total = 0;                       // node 4
  int i = 1;                           // node 4
  while (i <= n) {                     // node 5  (decision)
    total += i;                        // node 6
    i += 1;                            // node 6
  }
  return "sum=" + total;               // node 7  (exit)
}
```

```javascript
function classifyAndSum(n) {  // node 1  (entry)
  if (n < 0) {                // node 2  (decision)
    return "negative";        // node 3
  }
  let total = 0;              // node 4
  let i = 1;                  // node 4
  while (i <= n) {            // node 5  (decision)
    total += i;               // node 6
    i += 1;                   // node 6
  }
  return `sum=${total}`;      // node 7  (exit)
}
```

```python
def classify_and_sum(n):        # node 1  (entry)
  if n < 0:                   # node 2  (decision)
    return "negative"       # node 3
  total = 0                   # node 4
  i = 1                       # node 4
  while i <= n:               # node 5  (decision)
    total += i              # node 6
    i += 1                  # node 6
  return f"sum={total}"       # node 7  (exit)
```

```ruby
def classify_and_sum(n)  # node 1  (entry)
  if n < 0               # node 2  (decision)
    return "negative"    # node 3
  end
  total = 0              # node 4
  i = 1                  # node 4
  while i <= n           # node 5  (decision)
    total += i           # node 6
    i += 1               # node 6
  end
  "sum=#{total}"         # node 7  (exit)
end
```

```typescript
function classifyAndSum(n: number): string {  // node 1  (entry)
  if (n < 0) {                // node 2  (decision)
    return "negative";        // node 3
  }
  let total = 0;              // node 4
  let i = 1;                  // node 4
  while (i <= n) {            // node 5  (decision)
    total += i;               // node 6
    i += 1;                   // node 6
  }
  return `sum=${total}`;      // node 7  (exit)
}
```

Its control-flow graph:

```mermaid
flowchart TD
    N1(("1: enter")) --> N2{"2: n &lt; 0 ?"}
    N2 -- "true" --> N3["3: return 'negative'"]
    N2 -- "false" --> N4["4: total=0; i=1"]
    N4 --> N5{"5: i &lt;= n ?"}
    N5 -- "true" --> N6["6: total+=i; i+=1"]
    N6 --> N5
    N5 -- "false" --> N7["7: return sum"]
    N3 --> EX(("exit"))
    N7 --> EX
```

Two structural features matter for what follows. First, node 2 and node 5 are
**decisions**, each with a true edge and a false edge. Second, node 5's true edge loops
back — a **cycle** — which is why the number of *paths* through this function is unbounded
(you can go around the loop 0, 1, 2, … times), while the number of *edges* is finite.
That gap is the whole reason path coverage is usually impractical and weaker criteria
exist.

The CFG also gives you a number worth knowing. **Cyclomatic complexity** is the count of
a function's decision points plus one — equivalently, for a graph with $E$ edges and $N$
nodes, $E - N + 2$.[^13] It measures how many independent paths thread the function, and so
roughly how many tests branch coverage will demand. For the function above: two decisions
(nodes 2 and 5), so complexity $2 + 1 = 3$; or count the graph above, $E = 9$, $N = 8$,
$9 - 8 + 2 = 3$. Conventional bands for reading the number: **1–10** is simple, readily
testable code; **11–20** is moderately complex; **21–50** is risky; above **50** is
extremely difficult to test comprehensively — and a strong sign the function should be
decomposed.[^14] The metric earns its keep as a *predictor*: high-complexity
functions are where defects cluster and where the hard-to-cover branches live, which
makes it a map of where to spend testing effort — and refactoring (Chapter 15,
[§15.3](../15-maintenance-evolution/#153-refactoring-under-green-tests)) is the
treatment for the hot spots it finds.[^15]

### 10.3.2 Control-Flow Coverage Criteria

Three classic criteria form a hierarchy of increasing strength. We work each one on the
classify-and-sum function from §10.3.1.

**Statement coverage** requires every node (statement) to be executed by at least one
test. What set of inputs runs every node? Node 3 needs `n < 0`; nodes 4–7 need `n >= 0`;
node 6 (the loop body) needs `n >= 1`. So:

| Test | Input `n` | Nodes executed | New nodes |
|------|-----------|----------------|-----------|
| T1   | `-5`      | 1, 2, 3        | 1,2,3     |
| T2   | `3`       | 1,2,4,5,6,5,6,5,6,5,7 | 4,5,6,7 |

**Two tests** (`n=-5`, `n=3`) achieve 100% statement coverage — every node has run.

**Branch (decision) coverage** requires every *edge out of a decision* to be taken — both
the true and false outcome of each decision. List the four decision edges: node 2 true,
node 2 false, node 5 true, node 5 false. Check the tests above:

- `n=-5` takes node 2 **true**. (node 5 never reached.)
- `n=3` takes node 2 **false**, node 5 **true** (loop body runs), and node 5 **false**
  (loop exits).

Between them, all four edges are covered, so the *same* two tests also give 100% branch
coverage here. That is a coincidence of this function's shape; branch coverage is strictly
stronger than statement coverage in general. To see why, change the function so the loop
can be skipped entirely and a statement after it depends on the loop having run — a test
that covers every statement can still fail to take the "loop body never executes" edge.

> **Note — branch coverage subsumes statement coverage.** If every branch is taken, every
> node between branches must have run, so 100% branch ⇒ 100% statement. The converse
> fails: a single `if` with no `else` can reach 100% statement coverage with one test
> (condition true) while never taking the false edge. Whenever a team says "coverage,"
> ask *which* coverage — the gap between these two is where real defects hide.

**Path coverage** requires every *distinct path* from entry to exit to be executed. Count
the paths in the classify-and-sum function:

- The `n < 0` path (through node 3): **1** path.
- The `n >= 0` paths differ by how many times the loop runs: 0 iterations, 1 iteration, 2
  iterations, … — one path per possible value of `n >= 0`, i.e. **unbounded**.

So full path coverage is *impossible* here — a decisive illustration of why we settle for
branch coverage plus judgment about loops (commonly: test the loop 0 times, once, and
"many" times). Even in loop-free code, path count grows as roughly $2^d$ for $d$
independent decisions, so path coverage is exponential and reserved for tiny, critical
routines.

The hierarchy, then: **path ⇒ branch ⇒ statement** (each implies the ones to its right).[^16]
Strength costs test cases; the engineering choice is how far up the hierarchy a given
piece of code justifies climbing. A checkout total merits branch coverage; an autopilot
demands more (§10.5).

> **Case study — measuring coverage isn't free.** Coverage tools work by *instrumenting*
> the program: a probe at every statement or branch records what ran. The probes cost
> real time and memory — overheads of 10–30% in time, with instrumented binaries 60–90%
> larger, have been reported — unnoticeable for a unit suite on a laptop, prohibitive on
> a memory-constrained phone. One line of research sidesteps instrumentation entirely:
> modern CPUs already record where they branch, and *sampling* those hardware monitors
> during a test run recovered up to ~90% of branch coverage with less overhead and no
> code growth — enough to measure coverage on the device a mobile app actually ships
> to.[^5]

## 10.4 Input Coverage I: Black-Box Testing

Black-box testing turns the *specification* into a set of items to cover, without looking
at the code. The two most valuable criteria partition the input space and then probe its
edges.

### 10.4.1 Equivalence-Class Coverage

The insight is that inputs are not all different: a program usually treats whole *classes*
of inputs identically, so one representative of a class is (almost) as good as any other.
An **equivalence class (equivalence partition)** is a set of inputs the specification
implies should be handled the same way.[^17] You partition the input space into classes —
covering both *valid* and *invalid* classes — and pick one representative from each. This
slashes the number of tests from "every input" to "one per class" while keeping strong
coverage of *behaviors*.

Take a spec: *`set_volume(level)` accepts an integer `level` from 1 to 100 inclusive and
sets the volume; any other value is rejected.* The classes are:

| Class                     | Example representative | Expected behavior |
|---------------------------|------------------------|-------------------|
| C1: below range (`< 1`)   | `-3`                   | rejected          |
| C2: in range (`1..100`)   | `55`                   | accepted          |
| C3: above range (`> 100`) | `250`                  | rejected          |
| C4: non-integer type      | `"loud"`, `3.5`        | rejected          |

Four tests, one per class, cover every distinct *specified* behavior. Compare this to
testing 1, 2, 3, …, 100 (100 tests that all exercise the same behavior C2) — equivalence
partitioning gives you the same behavioral coverage for a fraction of the cost, and it
forces you to remember the *invalid* classes that ad-hoc testing skips.

### 10.4.2 Boundary-Value Coverage

Defects cluster at the *edges* of equivalence classes, because that is where programmers
write the fragile comparisons: `<` versus `<=`, an off-by-one in a loop bound, `>` versus
`>=`. **Boundary-value analysis** targets exactly those edges: for each boundary, test the
value just below it, at it, and just above it.[^17]

For `set_volume`, valid range 1..100, the two boundaries are 1 (lower) and 100 (upper).
The boundary values to test:

| Boundary | Values to test | Expected |
|----------|----------------|----------|
| lower = 1   | `0`   | rejected (just below) |
|             | `1`   | accepted (at)         |
|             | `2`   | accepted (just above) |
| upper = 100 | `99`  | accepted (just below) |
|             | `100` | accepted (at)         |
|             | `101` | rejected (just above) |

Six boundary tests. Watch them do their job. Suppose a developer wrote the guard as:

```generic
function set_volume(level)
  // a statically typed language requires level to be an integer here
  if level is not an integer or level < 1 or level >= 100 then  // BUG: >= should be >
    error "level must be 1..100"
  end if
  apply(level)
end function
```

```go
func SetVolume(level int) error {
	if level < 1 || level >= 100 { // BUG: >= should be >
		return errors.New("level must be 1..100")
	}
	apply(level)
	return nil
}
```

```java
static void setVolume(int level) {
  if (level < 1 || level >= 100)  // BUG: >= should be >
    throw new IllegalArgumentException("level must be 1..100");
  apply(level);
}
```

```javascript
function setVolume(level) {
  if (!Number.isInteger(level) || level < 1 || level >= 100) {  // BUG: >= should be >
    throw new RangeError("level must be 1..100");
  }
  apply(level);
}
```

```python
def set_volume(level):
  if not isinstance(level, int) or level < 1 or level >= 100:   # BUG: >= should be >
    raise ValueError("level must be 1..100")
  _apply(level)
```

```ruby
def set_volume(level)
  if !level.is_a?(Integer) || level < 1 || level >= 100   # BUG: >= should be >
    raise ArgumentError, "level must be 1..100"
  end
  apply(level)
end
```

```typescript
function setVolume(level: unknown): void {
  if (typeof level !== "number" || !Number.isInteger(level)
      || level < 1 || level >= 100) {          // BUG: >= should be >
    throw new RangeError("level must be 1..100");
  }
  apply(level);
}
```

The equivalence-class test with representative `55` passes (it is happily accepted), and
so would `250` (rejected) and `-3` (rejected). The defect hides at the top edge. But the
boundary test at level `100` **fails** — the code rejects a value the spec says is
valid — pinpointing the `>=`/`>` mistake. This is the payoff: boundary values find one of
the most common categories of numeric defect, and they cost only a few extra tests on top
of equivalence classes.

> **Note.** Combine the two criteria: equivalence partitioning tells you *which regions*
> exist; boundary analysis tells you *where within and between regions* to probe. In
> practice you write one "interior" representative per class **plus** the below/at/above
> triples at each boundary. For `set_volume` that is roughly 4 + 6 = a handful of tests
> that together cover behavior far better than dozens of random ones.

One black-box technique abandons careful selection altogether. **Fuzz testing (fuzzing)**
throws huge volumes of malformed, random, or mutated inputs at a program and watches for
crashes, hangs, and memory errors — no specification, no partitions, just the implicit
oracle (§10.1.4) that the program *must not fall over*.[^18] It is a cousin of property-based
testing but adversarial in spirit: instead of checking a property on well-formed inputs,
it hunts for the ill-formed input nobody thought to reject. That makes fuzzing a
mainstay of security testing — buffer overflows, injection flaws, and denial-of-service
defects are the bugs that surface when a parser meets input its author never imagined.
Because an effective fuzzing campaign runs for hours or days, it belongs in a
non-blocking pipeline stage (Chapter 14), not on the every-commit path.

## 10.5 Code Coverage II: MC/DC

Branch coverage checks that each *decision* comes out true and false at least once. But a
decision can be a **compound** boolean expression — `(A && B) || C` — and branch coverage
says nothing about the individual **conditions** inside it. A suite can flip the whole
decision true/false while some condition never actually influenced the outcome. For the
highest-criticality software (in avionics, DO-178C requires it at the most critical
design-assurance level), we need a stronger criterion:
**Modified Condition/Decision Coverage (MC/DC)**.[^19]

### 10.5.1 Condition and Decision Coverage Are Independent

First untangle two finer criteria:

- **Condition coverage** requires each individual condition (`A`, `B`, `C`) to be both
  true and false at least once — but says nothing about the decision's outcome.
- **Decision coverage** (= branch coverage) requires the whole decision to be both true
  and false — but says nothing about individual conditions.

Neither implies the other. Consider the decision `A || B` with just two tests:
`(A=true, B=false)` and `(A=false, B=true)`.

| Test | A | B | `A \|\| B` |
|------|---|---|-----------|
| t1   | T | F | T         |
| t2   | F | T | T         |

Every condition takes both values (A is T then F; B is F then T), so **condition coverage
is 100%**. Yet the decision is `true` in *both* tests — it never came out false — so
**decision coverage is only 50%**. Conversely, testing `(A=true, B=false)` and
`(A=false, B=false)` gives full decision coverage (T then F) while `B` never takes the
value true — so **condition coverage is not met**. Because each criterion can be
satisfied while the other is not, they are genuinely independent — and *neither alone*
guarantees that every condition can actually change the result.

### 10.5.2 MC/DC Pairs of Tests

**MC/DC** demands the strongest practical property: **every condition must be shown to
independently affect the decision's outcome.**[^20] Concretely, for each condition you must
exhibit a **pair** of tests in which *only that condition changes*, everything else is
held fixed, *and the decision's result flips*. That pair proves the condition is not dead
weight — it really controls the outcome on its own.

MC/DC bundles four requirements: every decision takes both outcomes (decision coverage);
every condition takes both values (condition coverage); and each condition independently
flips the decision. Remarkably, for a decision with **N conditions** this can usually be
achieved with just **N + 1** tests — a linear number, versus $2^N$ for exhaustive testing
of the truth table.[^20] That exhaustive criterion has its own name — **multiple-condition
coverage**, which requires every combination of condition truth values — and MC/DC is
best understood as its practical approximation.[^17]
That is why MC/DC is the sweet spot for critical code: strong evidence that each condition
independently affects the outcome, at a linear rather than exponential test cost.

Let us fully work the decision from the section opener:

$$D = (A \land B) \lor C$$

It has N = 3 conditions, so we expect 4 tests. Start from the complete truth table (row
numbers will let us cite tests precisely):

| # | A | B | C | `A && B` | `D = (A&&B) \|\| C` |
|---|---|---|---|----------|---------------------|
| 1 | T | T | T | T        | **T** |
| 2 | T | T | F | T        | **T** |
| 3 | T | F | T | F        | **T** |
| 4 | T | F | F | F        | **F** |
| 5 | F | T | T | F        | **T** |
| 6 | F | T | F | F        | **F** |
| 7 | F | F | T | F        | **T** |
| 8 | F | F | F | F        | **F** |

Now find an **independence pair** for each condition — two rows differing *only* in that
condition, with different results for `D`.

**Condition A.** Hold B and C fixed, vary A, require `D` to flip. Compare rows 2 and 6:

| # | A | B | C | D |
|---|---|---|---|---|
| 2 | **T** | T | F | T |
| 6 | **F** | T | F | F |

Only A changed (T→F), B=T and C=F are held, and `D` flipped T→F. So **{2, 6}** is A's
independence pair. (Intuitively: with C false, the result is decided by `A && B`; holding
B true, A alone controls it.)

**Condition B.** Hold A and C fixed, vary B. Compare rows 2 and 4:

| # | A | B | C | D |
|---|---|---|---|---|
| 2 | T | **T** | F | T |
| 4 | T | **F** | F | F |

Only B changed (T→F), A=T and C=F held, `D` flipped T→F. So **{2, 4}** is B's pair.

**Condition C.** Hold A and B fixed, vary C. We need `A && B` to be *false* (otherwise the
`|| C` is short-circuited and C cannot matter). Compare rows 3 and 4:

| # | A | B | C | D |
|---|---|---|---|---|
| 3 | T | F | **T** | T |
| 4 | T | F | **F** | F |

Only C changed (T→F), A=T and B=F held, `D` flipped T→F. So **{3, 4}** is C's pair.

Now assemble the minimal suite by taking the **union** of the rows used:

$$\{2, 6\} \cup \{2, 4\} \cup \{3, 4\} = \{2, 3, 4, 6\}$$

Just **four tests** — exactly N + 1 = 3 + 1:

| Test | A | B | C | D | Proves independence of |
|------|---|---|---|---|------------------------|
| row 2 | T | T | F | T | A (with 6), B (with 4) |
| row 3 | T | F | T | T | C (with 4)             |
| row 4 | T | F | F | F | B (with 2), C (with 3) |
| row 6 | F | T | F | F | A (with 2)             |

Verify the bundle: A's pair {2,6} ✓, B's pair {2,4} ✓, C's pair {3,4} ✓ are all present.
Every condition is shown to independently drive the decision, the decision is both T (rows
2, 3) and F (rows 4, 6), and each condition takes both values across the suite. This
4-test set satisfies MC/DC for `(A && B) || C`, versus 8 tests for the full truth table —
the linear-vs-exponential saving that makes MC/DC affordable at scale.

> **Note — why "modified."** The name comes from the *modification* idea: for each
> condition, you *modify only it* and observe the decision change. The reused test (row 2
> here, which serves both A and B; row 4, which serves both B and C) is why the count lands
> at N + 1 rather than 2N — pairs share tests. When short-circuit operators or coupled
> conditions prevent sharing, you may need slightly more than N + 1, though still usually
> far fewer than the full $2^N$.

> **Pitfall.** MC/DC is defined per *condition*, not per *decision*. If you rewrite
> `if (a > 0 && b > 0)` as two nested `if`s, tools may report "100% branch coverage" and
> lull you into thinking you are done — but you have not shown each condition's independent
> effect. When correctness is critical, measure MC/DC explicitly with a tool that
> understands compound conditions.

## 10.6 Input Coverage II: Combinatorial Testing

Many systems are configured by several parameters at once, and defects often lurk in
*combinations* rather than single values. Suppose a checkout page is parameterized by
browser, operating system, and locale, each with three options:

- **Browser** ∈ {Chrome, Firefox, Safari}
- **OS** ∈ {Windows, macOS, Linux}
- **Locale** ∈ {EN, FR, JP}

Testing *every* combination is **exhaustive** and costs $3 \times 3 \times 3 = 27$ runs —
and with more parameters it explodes multiplicatively (ten binary flags is already 1,024
combinations). That is infeasible, yet single-value testing ("try each browser once")
misses interaction bugs like "date format breaks *only* on Safari *with* the JP locale."

**Combinatorial testing** exploits an empirical regularity: the large majority of
interaction defects are triggered by the interaction of just **two** parameters, and
almost all of the rest by three.[^21] NIST studied fault databases across many domains and
found that testing all *pairs* of parameter values catches the bulk of interaction faults.[^22]
So instead of covering all *combinations*, we cover all *pairs* — **pairwise** (a.k.a.
**all-pairs**, or 2-way) testing.

The goal: choose a small set of test configurations such that for **every pair of
parameters, every pair of their values appears together in at least one test.** For our
three 3-valued parameters, all pairs can be covered in just **9** tests (not 27):

| Test | Browser | OS      | Locale |
|------|---------|---------|--------|
| 1 | Chrome  | Windows | EN |
| 2 | Chrome  | macOS   | FR |
| 3 | Chrome  | Linux   | JP |
| 4 | Firefox | Windows | FR |
| 5 | Firefox | macOS   | JP |
| 6 | Firefox | Linux   | EN |
| 7 | Safari  | Windows | JP |
| 8 | Safari  | macOS   | EN |
| 9 | Safari  | Linux   | FR |

Check the claim for one parameter pair, Browser × Locale. The (Browser, Locale)
combinations appearing are: (Chrome,EN), (Chrome,FR), (Chrome,JP), (Firefox,FR),
(Firefox,JP), (Firefox,EN), (Safari,JP), (Safari,EN), (Safari,FR) — all 9 possible pairs,
each at least once. The same holds for Browser × OS and OS × Locale (verify OS × Locale as
an exercise). So every 2-way interaction is exercised, and the "Safari + JP" bug from above
*cannot* slip through: test 7 pairs them. We reduced 27 runs to 9 — a 3× saving here, and
the saving grows dramatically with more parameters (pairwise coverage of ten 3-valued
parameters needs fewer than twenty tests, not 59,049).

> **Note.** You rarely build these tables by hand. Tools — Microsoft's PICT, the NIST
> **ACTS** tool, or libraries in most languages — generate a minimal (or near-minimal)
> covering array for you, and can extend from pairwise to 3-way or higher when the risk
> justifies it. What you must supply is the *model*: the parameters, their meaningful
> values (use equivalence classes and boundaries from §10.4 to choose them), and any
> constraints ("Safari implies macOS"). Combinatorial testing composes with black-box
> input analysis; it does not replace it.

> **Pitfall.** Pairwise is a heuristic, not a guarantee. If a defect requires a *three-way*
> interaction (fails only on Firefox + Linux + JP together), a 2-way suite may miss it. Use
> higher-strength (3-way, 4-way) coverage for the most critical or most interaction-prone
> subsystems, and let the empirical fault-strength data — not habit — set the level.

## 10.7 Conclusion

Testing is how you earn the right to say "this software works," and this chapter turned
that claim from a hope into an engineering argument. The through-line is **criteria**:
every hard question about testing becomes tractable once you name a set of items to cover
and measure the fraction you have.

- The four issues — **selection, adequacy, oracles, automation** (§10.1) — are the
  questions every testing decision answers, explicitly or by accident. Answer them on
  purpose.
- Testing happens at **levels** — unit, integration, functional, system, acceptance
  (§10.2) — and the **pyramid** tells you to invest most where feedback is fastest and
  cheapest, catching defects early where they cost the least.
- **White-box** criteria (§10.3, §10.5) measure how thoroughly you exercised the code:
  statement ⇐ branch ⇐ path in strength, with **MC/DC** as the linear-cost criterion that
  isolates each condition's independent effect in critical compound decisions.
- **Black-box** criteria (§10.4, §10.6) measure how thoroughly you exercised the
  *specified behavior*: equivalence classes, boundary values, and pairwise combinations.

No single criterion is enough, and no amount of testing proves correctness. But a suite
built from these criteria — black-box *and* white-box, at the right level, with honest
oracles, run automatically on every change — is the most reliable, most economical net we
have for catching the defects Chapter 1 promised are inevitable. The next chapter turns testing's
adversarial instinct — probing the inputs and error paths where a program misbehaves —
toward an attacker who is *trying* to make it misbehave. Then Chapter 12 turns to measuring
quality across a whole project, where the coverage numbers you learned to compute here are
among the first metrics you will report.

---

### Sources

[^1]: Edsger W. Dijkstra, *Notes on Structured Programming*, EWD249 (1970), §3 ("Program
    testing can be used to show the presence of bugs, but never to show their absence!");
    the aphorism also appears in the 1969 NATO *Software Engineering Techniques* report.
    [cs.utexas.edu](https://www.cs.utexas.edu/users/EWD/ewd02xx/EWD249.PDF).

[^2]: Earl T. Barr, Mark Harman, Phil McMinn, Muzammil Shahbaz, and Shin Yoo, *The Oracle
    Problem in Software Testing: A Survey*, IEEE Transactions on Software Engineering 41(5)
    (2015). [doi.org](https://doi.org/10.1109/TSE.2014.2372785).

[^3]: Richard A. DeMillo, Richard J. Lipton, and Frederick G. Sayward, *Hints on Test Data
    Selection: Help for the Practicing Programmer*, IEEE Computer 11(4) (1978).
    [doi.org](https://doi.org/10.1109/C-M.1978.218136).

[^4]: Gregg Rothermel, Roland H. Untch, Chengyun Chu, and Mary Jean Harrold,
    *Prioritizing Test Cases for Regression Testing*, IEEE Transactions on Software
    Engineering 27(10) (2001) — the paper that introduced APFD; the seven-week suite is
    its industrial case study. [doi.org](https://doi.org/10.1109/32.962562).

[^5]: Kristen R. Walcott-Justice, *Testing in Resource-Constrained Environments*, Ph.D.
    dissertation, University of Virginia (2012). Develops budget-guaranteed, time-aware
    test selection (knapsack solvers, then an overlap-aware genetic algorithm) and THeME,
    which recovers up to ~90% of branch coverage by sampling CPU hardware monitors
    instead of instrumenting the code.
    [faculty.uccs.edu](https://faculty.uccs.edu/kwalcott/wp-content/uploads/sites/49/2024/01/dissertation_with_sigs.pdf).

[^6]: Tim Ottinger and Brett Schuchert, *F.I.R.S.T.* (Agile in a Flash, 2009); popularized
    in Robert C. Martin, *Clean Code*, ch. 9 (2008).
    [agileinaflash.blogspot.com](https://agileinaflash.blogspot.com/2009/02/first.html).

[^7]: Barry W. Boehm, *Verifying and Validating Software Requirements and Design
    Specifications*, IEEE Software 1(1) (1984). [doi.org](https://doi.org/10.1109/MS.1984.233702).

[^8]: Cem Kaner, James Bach, and Bret Pettichord, *Lessons Learned in Software Testing: A
    Context-Driven Approach* (Wiley, 2002).
    [wiley.com](https://www.wiley.com/en-us/Lessons+Learned+in+Software+Testing:+A+Context+Driven+Approach-p-9780471081128).

[^9]: Steve McConnell, *Daily Build and Smoke Test*, IEEE Software 13(4) (1996).
    [stevemcconnell.com](https://stevemcconnell.com/ieeesoftware/bp04.htm).

[^10]: Mike Cohn, *Succeeding with Agile: Software Development Using Scrum* (Addison-Wesley,
    2009); summarized in Martin Fowler, *TestPyramid* (2012).
    [martinfowler.com](https://martinfowler.com/bliki/TestPyramid.html).

[^11]: Barry Boehm and Victor R. Basili, *Software Defect Reduction Top 10 List*, IEEE
    Computer 34(1) (2001). [cs.umd.edu](https://www.cs.umd.edu/projects/SoftEng/ESEG/papers/82.78.pdf).

[^12]: Qingzhou Luo, Farah Hariri, Lamyaa Eloussi, and Darko Marinov, *An Empirical
    Analysis of Flaky Tests*, Proc. FSE 2014. [doi.org](https://doi.org/10.1145/2635868.2635920).

[^13]: Thomas J. McCabe, *A Complexity Measure*, IEEE Transactions on Software Engineering
    SE-2(4) (1976). [doi.org](https://doi.org/10.1109/TSE.1976.233837).

[^14]: Software Engineering Institute, *C4 Software Technology Reference Guide — A
    Prototype*, CMU/SEI-97-HB-001 (1997), "Cyclomatic Complexity" section.
    [sei.cmu.edu](https://www.sei.cmu.edu/documents/1625/1997_002_001_16523.pdf).

[^15]: Arthur H. Watson and Thomas J. McCabe, *Structured Testing: A Testing Methodology
    Using the Cyclomatic Complexity Metric*, NIST Special Publication 500-235 (1996).
    [nvlpubs.nist.gov](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication500-235.pdf).

[^16]: Paul Ammann and Jeff Offutt, *Introduction to Software Testing*, 2nd ed. (2016).
    [cs.gmu.edu](https://cs.gmu.edu/~offutt/softwaretest/).

[^17]: Glenford J. Myers, *The Art of Software Testing* (Wiley, 1979; 3rd ed. 2011).
    [wiley.com](https://www.wiley.com/en-us/The+Art+of+Software+Testing%2C+3rd+Edition-p-9781119202486).

[^18]: Barton P. Miller, Lars Fredriksen, and Bryan So, *An Empirical Study of the
    Reliability of UNIX Utilities*, Communications of the ACM 33(12) (1990).
    [doi.org](https://doi.org/10.1145/96267.96279).

[^19]: RTCA, *DO-178C: Software Considerations in Airborne Systems and Equipment
    Certification* (2011), Table A-7 — MC/DC is an objective only at Level A.
    [rtca.org](https://www.rtca.org/).

[^20]: Kelly J. Hayhurst, Dan S. Veerhusen, John J. Chilenski, and Leanna K. Rierson, *A
    Practical Tutorial on Modified Condition/Decision Coverage*, NASA/TM-2001-210876 (2001).
    [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/20010057789).

[^21]: D. Richard Kuhn, Dolores R. Wallace, and Albert M. Gallo, *Software Fault
    Interactions and Implications for Software Testing*, IEEE Transactions on Software
    Engineering 30(6) (2004).
    [csrc.nist.gov](https://csrc.nist.gov/pubs/journal/2004/06/software-fault-interactions-and-implications-for-s/final).

[^22]: D. Richard Kuhn, Raghu N. Kacker, and Yu Lei, *Practical Combinatorial Testing*,
    NIST Special Publication 800-142 (2010). [csrc.nist.gov](https://csrc.nist.gov/pubs/sp/800/142/final).

---

- **Key takeaways** are summarized above in §10.7.
- Continue to the [Exercises](exercises.md).
- Go deeper with the [Open Resources](resources.md) for this chapter.
