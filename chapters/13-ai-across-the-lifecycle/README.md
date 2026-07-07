# Chapter 13 — Software Engineering in the Age of AI

> **Where we are.** Every previous chapter described a durable engineering discipline —
> process, requirements, design, checking, testing, metrics, teamwork. This chapter asks
> what happens to those disciplines when generative AI and **coding agents** can draft
> code, tests, requirements, and designs in seconds. We separate what genuinely changes
> from what stubbornly does not, walk the whole lifecycle stage by stage, look honestly at
> the *evidence* (which is more mixed than the marketing), and close with the **o16g
> "Outcome Engineering" manifesto** — a recent, provocative attempt to redefine the
> profession for the agentic era.

The headline claim of the moment is that AI writes the code now. The more useful claim is
this: **AI changes where the hard part lives.** For decades the bottleneck was *producing*
correct code fast enough. As producing gets cheap, the bottleneck moves to *deciding what
to build* and *proving it works* — which are the very activities this book has been
teaching. The engineer who internalized Chapters 1–12 is the person best positioned to
*direct* the agents.

## 13.1 What AI Changes — and What It Doesn't

### 13.1.1 Essential vs. Accidental Complexity, Revisited

Recall from Chapter 1 the split between **essential** complexity (inherent in the problem)
and **accidental** complexity (from our tools and toil). Generative AI is a spectacular
weapon against *accidental* complexity: boilerplate, glue code, format conversions, first
drafts of tests, "how do I call this API" friction. It is far weaker against *essential*
complexity: deciding what the system should actually do, resolving conflicting goals,
choosing an architecture whose likely changes are cheap. That boundary is the single most
important idea in this chapter. **Delegate the toil; own the essence.**

### 13.1.2 The Four Pressures Still Hold

The book's four cross-cutting pressures do not go away — AI just shifts them:

- **Software is complex.** Agents can *generate* complexity faster than ever, including
  accidental complexity you did not ask for. Architecture (Chapters 6–7) matters *more*.
- **Requirements change.** AI lowers the cost of *responding* to change, which raises the
  premium on knowing *which* change is worth making (Chapters 3–4).
- **Defects are inevitable.** AI produces plausible-looking defects at scale. Reviews,
  static checking, and tests (Chapters 9–10) become the load-bearing walls.
- **Teams need coordination.** "Teams" now include non-human members. Coordinating a
  *swarm* of agents is a new and unsolved organizational problem (see §13.4).

### 13.1.3 A Ladder of Assistance: From Autocomplete to Agents

"AI coding" is not one thing. It helps to name the rungs, because the engineering
questions differ at each:

```mermaid
flowchart BT
    A["Autocomplete<br/>(line/block suggestions)"] --> B["Chat assistant<br/>(ask, explain, refactor)"]
    B --> C["In-IDE agent<br/>(multi-file edits, runs tools)"]
    C --> D["Autonomous agent<br/>(takes an issue →<br/>opens a PR)"]
    D --> E["Multi-agent swarm<br/>(planner + workers + critics)"]
    classDef rung fill:#eef,stroke:#66a,color:#000;
    class A,B,C,D,E rung;
```

As you climb the ladder, the human's job moves from *typing* toward *specifying,
supervising, and verifying* — and the cost of a confident-but-wrong output rises, because
more happens between your instruction and your review.

### 13.1.4 The Productivity Paradox

Does AI make developers faster? The honest answer is *it depends, and the evidence is
mixed enough to demand humility.*

- **Perceived gains are large.** In field studies, a majority of developers report feeling
  more productive with tools like GitHub Copilot, and vendors cite eye-catching
  numbers.[^1]<!-- -->[^2]
- **Measured gains are smaller and sometimes negative.** In a 2025 randomized controlled
  trial, METR had experienced open-source developers do real tasks in repositories they
  knew well. Developers *predicted* AI would make them ~24% faster; in fact they were about
  **19% slower** with AI — and still *believed* they'd been faster afterward.[^3] The slowdown
  came largely from the overhead of **reviewing and integrating** generated output. Scope
  the finding as carefully as the researchers did: it describes *that specific setting* —
  experienced developers, mature and familiar repositories, high quality standards,
  early-2025 tools — not AI-assisted work in general, and tools have moved since.

> **Principle.** Perceived productivity is not measured productivity. On familiar,
> high-standards code, the time you save typing can be swamped by the time you spend
> verifying what the agent produced. *Verification is the new bottleneck* — a theme this
> whole chapter returns to.

The lesson is not "AI is useless" — gains are real for boilerplate, unfamiliar APIs,
greenfield prototypes, and well-specified narrow tasks. The lesson is that **leverage
scales with the operator's judgment**, and that you must *measure* impact rather than trust
the feeling of speed (a direct application of Chapter 12).

## 13.2 AI Across the Lifecycle

Here we walk the lifecycle, mapping AI's role onto each chapter's discipline. For each
stage: *what AI does well now*, *where it fails*, and *what fundamental the human still
owns.*

```mermaid
flowchart TD
    P[Process &amp; Teamwork<br/>Ch.2] --> R[Requirements<br/>Ch.3-4]
    R --> U[Use Cases<br/>Ch.5]
    U --> D[Design &amp; Architecture<br/>Ch.6-7]
    D --> C[Code + Static Checking<br/>Ch.8]
    C --> T[Testing<br/>Ch.9]
    T --> S[Software Security<br/>Ch.10]
    S --> M[Quality Metrics<br/>Ch.11]
    M -.feedback.-> R
    classDef ai fill:#eef,stroke:#66a,color:#000;
    class P,R,U,D,C,T,S,M ai;
```

### 13.2.1 Process and Teamwork (Chapter 2)

AI compresses many process activities: drafting sprint plans, summarizing standups,
writing retro notes, triaging issues, generating first-pass estimates. Agents can now take
a ticket and open a pull request unattended, which strains the assumptions of Scrum and XP
— what is a "sprint" when a swarm can attempt fifty backlog items overnight?

- **Fails at:** judgment about *value* and *sequencing*; reading the human dynamics of a
  team; owning accountability for what ships.
- **Human owns:** the definition of done, the choice of what to build next, and
  responsibility. The agile principle "working software is the primary measure of progress"
  gets *sharper*, not softer — see the manifesto's "verified reality" in §13.4.[^4]

### 13.2.2 Requirements (Chapter 3)

Large language models are genuinely useful for **elicitation and drafting**: turning
interview notes, tickets, and support logs into candidate user stories, acceptance
criteria (Given/When/Then), and edge-case lists. Studies report LLM-drafted requirements
that reviewers rate as complete, consistent first drafts — comparable to an entry-level
engineer's — produced far faster and cheaper.[^5]<!-- -->[^6]

- **Fails at:** knowing what users actually *need* versus what is *plausible*; an LLM will
  cheerfully invent requirements that sound reasonable and are wrong (**hallucinated
  requirements**), and its fluency can manufacture false consensus.[^7]
- **Human owns:** talking to real stakeholders, resolving conflicting goals (Chapter 3's
  goal hierarchies), and *validating* that a story reflects a real need. Use AI to widen
  the net of candidate requirements; use humans to decide which are true.

### 13.2.3 Estimation and Analysis (Chapter 4)

AI can suggest story-point estimates from historical data and surface comparable past
work. But recall *why* we estimate in Chapter 4: story points model **human uncertainty**
and drive **prioritization**, not stopwatch time. When agents do the building, the
estimation question shifts from "how many engineer-hours?" toward "how much **compute/
budget**, and is the outcome worth it?" — precisely the manifesto's *cost, not time*
reframing (§13.4). MoSCoW, value/cost/risk, and Kano analysis remain the right tools; the
"cost" axis just gets a new currency.

### 13.2.4 Use Cases (Chapter 5)

Given a goal and a happy path, models are good at enumerating **alternative flows** and
exception cases — exactly the tedious part of use-case writing that people skip. That
coverage is valuable. But an agent cannot tell you which actor *goals* matter, and it will
pad use cases with flows no user will ever take.

- **Human owns:** the actor–goal list (what the system is *for*) and pruning generated
  flows down to the ones that carry real risk or value.

### 13.2.5 Design and Architecture (Chapters 6–7)

This is where the human-owned layer is thickest. AI can propose class structures, generate
**Architecture Decision Records (ADRs)**, suggest applicable patterns from Chapter 7, and
even prototype competing designs to compare. Research on multi-agent systems that go from
requirements to candidate architectures is active but early, and leans on role
specialization to fight hallucination.[^8]<!-- -->[^9]

- **Fails at:** the *significant, expensive-to-change decisions* that define architecture
  (Chapter 6); it has no stake in your five-year maintenance cost and cannot feel the pain
  of high coupling.
- **Human owns:** modularity, coupling/cohesion trade-offs, and choosing which likely
  changes to make cheap. Let AI *draft and compare* designs; keep the *decision* and its
  rationale human and written down.

### 13.2.6 Static Checking and Code Review (Chapter 9)

AI both helps and harms here, sharply. AI reviewers and smarter static analyzers
catch real bugs, explain them, and suggest fixes.[^10] But **a growing share
of code under review is now itself AI-generated** — by late 2024 Google reported more than
a quarter of its new code was — which inverts the problem from
Chapter 9: the scarce resource, *reviewer trust and attention*, is now spent on machine
output produced faster than humans can vet it.[^11]

> **Pitfall.** A 2023 controlled study found developers with an AI assistant wrote
> *less secure* code while being *more confident* it was secure — a false sense of
> safety.[^12]
> In the AI era, static analysis and human review are the brakes that make the speed
> usable.

- **Human owns:** deciding *intent and trust* (does this change do what we meant?), and
  keeping review standards from eroding under volume. Precision/recall trade-offs for
  analyzers (Chapter 9) matter more as more code flows through them.

### 13.2.7 Testing (Chapter 10)

Testing is where agentic AI has advanced most measurably. Benchmarks like **SWE-bench**
(fix a real GitHub issue) and **SWT-bench** (generate a bug-reproducing test) have driven
rapid progress in automated **test generation** and **program repair**; as of 2025, agents
resolve a substantial fraction of such benchmark issues end to end.[^13]<!-- -->[^14] Treat those numbers with
care, though: passing a benchmark's tests is *evidence*, not proof, of a correct fix —
studies of SWE-bench-style evaluation have found patches that pass the benchmark suite
while failing developer-written tests or behaving differently from the true fix, so weak
or incomplete test suites can inflate reported resolution rates (the **oracle problem**
again, wearing a benchmark's clothes).[^15] Models are also strong at
generating unit tests, property-based tests, and boundary cases (Chapter 10's black-box
techniques).[^16]

But the deepest problem in testing survives untouched: the **oracle problem**. A generated
test encodes *what the model thinks correct behavior is* — which may simply mirror a
misunderstanding also baked into the generated code. Coverage numbers can look great while
the tests assert the wrong thing.

Chapter 10's discount example makes the failure concrete: suppose the billing spec says
half-cent prices round *up*, while the generated code trips a language-specific rounding
or representation trap — named in each variant's leading comment — and the generated test
asserts whatever the code already returns.

```generic
function apply_discount(price, percent)
  // AI-generated: rounds the last cent half-to-even (banker's rounding)
  return round_to_2_decimals(price * (1 - percent / 100))

function test_half_off()
  // AI-generated: asserts the code's own behavior
  if apply_discount(10.25, 50) != "5.12" then
    fail "testHalfOff failed"
  end if

test_half_off()                  // passes — and every line of the unit is covered
print apply_discount(10.25, 50)  // 5.12; the billing spec says 5.13 (half up)
```

```go
package main

import "fmt"

func applyDiscount(price, percent float64) string { // AI-generated: %.2f rounds ties
	return fmt.Sprintf("%.2f", price*(1-percent/100)) // to even — banker's rounding
}

func testHalfOff() { // AI-generated: asserts the code's own behavior
	if applyDiscount(10.25, 50) != "5.12" {
		panic("testHalfOff failed")
	}
}

func main() {
	testHalfOff()                         // passes — and every line of the unit is covered
	fmt.Println(applyDiscount(10.25, 50)) // 5.12; the billing spec says 5.13 (half up)
}
```

```java
import java.math.BigDecimal;
import java.math.RoundingMode;

public class OracleProblem {
  static double applyDiscount(double price, double percent) {
    return BigDecimal.valueOf(price * (1 - percent / 100))  // AI-generated: HALF_EVEN
        .setScale(2, RoundingMode.HALF_EVEN).doubleValue(); // = banker's rounding
  }

  static void testHalfOff() {  // AI-generated: asserts the code's own behavior
    if (applyDiscount(10.25, 50) != 5.12) throw new AssertionError();
  }

  public static void main(String[] args) {
    testHalfOff();  // passes — and every line of the unit is covered
    System.out.println(applyDiscount(10.25, 50)); // 5.12; the billing spec says 5.13
  }
}
```

```javascript
const assert = require("node:assert");

function applyDiscount(price, percent) {  // AI-generated: toFixed(2) rounds the stored
  return Number((price * (1 - percent / 100)).toFixed(2)); // double: 8.575 is 8.5749…
}

function testHalfOff() {                  // AI-generated: asserts the code's own behavior
  assert.strictEqual(applyDiscount(17.15, 50), 8.57);
}

testHalfOff();                           // passes — and every line of the unit is covered
console.log(applyDiscount(17.15, 50));   // 8.57; the billing spec says 8.58 (half up)
```

```python
def apply_discount(price, percent):     # AI-generated: Python round() = banker's rounding
  return round(price * (1 - percent / 100), 2)

def test_half_off():                    # AI-generated: asserts the code's own behavior
  assert apply_discount(10.25, 50) == 5.12

test_half_off()                         # passes — and every line of the unit is covered
print(apply_discount(10.25, 50))        # 5.12; the billing spec says 5.13 (half up)
```

```ruby
def apply_discount(price, percent)      # AI-generated: format %.2f rounds ties to
  format("%.2f", price * (1 - percent / 100.0))  # even — banker's rounding
end

def test_half_off                       # AI-generated: asserts the code's own behavior
  raise "test failed" unless apply_discount(10.25, 50) == "5.12"
end

test_half_off                           # passes — and every line of the unit is covered
puts apply_discount(10.25, 50)          # 5.12; the billing spec says 5.13 (half up)
```

```typescript
import assert from "node:assert";

function applyDiscount(price: number, percent: number): number { // AI-generated:
  return Number((price * (1 - percent / 100)).toFixed(2)); // toFixed(2) rounds the double
}

function testHalfOff(): void {            // AI-generated: asserts the code's own behavior
  assert.strictEqual(applyDiscount(17.15, 50), 8.57);
}

testHalfOff();                           // passes — and every line of the unit is covered
console.log(applyDiscount(17.15, 50));   // 8.57; the billing spec says 8.58 (half up)
```

Coverage looked great; the oracle was wrong. The suite agrees with the code because both
encode the same mistake, and only a reviewer who knows the billing spec can see that the
last cent rounded the wrong way — each variant's final print line shows the value the
spec required.

- **Human owns:** the **oracle** — the specification of correct behavior — and the coverage
  *criteria* that decide when testing is enough (statement/branch/MC/DC, §§10.3–10.5).
  Generated tests are a starting point to be reviewed, not ground truth.

**Security (Chapter 11)** is changed on both sides: AI writes vulnerabilities as fluently
as it writes features, and AI-driven tools now hunt for them — autonomous
pentest agents that validate findings with working exploits ([§11.3](../11-software-security/#113-finding-vulnerabilities-from-manual-to-autonomous)).
The human still owns the authorization to test, the judgment that a finding is real, and
the secure-by-design decisions no scanner makes for you.

### 13.2.8 Quality and Metrics (Chapter 12)

AI forces a reckoning with **what we measure**. Lines of code and commit counts were always
weak proxies; when a machine emits thousands of lines on request, they become actively
misleading. One industry analysis reports that as AI assistance spread (2021→2024), the
share of **duplicated/cloned** code rose while **refactoring** fell — a maintainability
warning sign that raw output volume hides, though it awaits independent academic
replication.[^17]

- **Human owns:** choosing metrics that resist gaming (Chapter 12's Goodhart's-Law
  discipline) and that measure **outcomes** — defect-removal efficiency, customer-found
  defects, DORA delivery metrics (Chapter 14), verified value delivered — rather than agent *activity*.
  This is the empirical backbone of Outcome Engineering (§13.4).

### 13.2.9 The Team Project (Appendix A)

In your own project, treat agents as fast, tireless, over-confident junior teammates. Let
them scaffold, draft tests, and explain unfamiliar code — but require the same evidence you
would from a human: a green test suite, a passing review, and a metric that moved. Record
*where* you used AI and *how you verified it*; that provenance is part of honest
engineering (and of your final report).

## 13.3 The Evidence: Productivity, Quality, Security

A balanced reading of the current research:

| Dimension | What the evidence suggests | Caveat |
|-----------|---------------------------|--------|
| **Productivity** | Real gains on boilerplate, unfamiliar APIs, greenfield, narrow well-specified tasks. | On familiar, high-standards code, a 2025 RCT found a ~19% *slowdown*; perception overstates gains.[^3] |
| **Quality** | Faster first drafts; good at tests and explanations. | Rising code duplication and falling refactoring in one industry analysis point to maintainability debt.[^17] |
| **Security** | Analyzers + AI review can catch known bug patterns. | ~40% of AI-generated programs in one study contained vulnerabilities; users felt *more* secure while being *less* so.[^18]<!-- -->[^12] |

The through-line: **AI is a power tool, and a power tool amplifies the operator.** In
skilled hands with strong verification (specs, tests, reviews, metrics), it is a real
multiplier. Without those disciplines, it multiplies *output* while quietly degrading
*quality* — and the operator won't feel it happening.

> **Principle.** In the AI era, the fundamentals in this book are not obsolete — they are
> your *verification layer*. Specs say what "correct" means; tests and reviews check it;
> metrics prove it in production. That layer is what turns fast generation into trustworthy
> software.

## 13.4 Outcome Engineering: The o16g Manifesto

In 2026, Cory Ondrejka (co-creator of Second Life; former engineering leader at Google and
Meta; CTO of Onebrief) published the **o16g manifesto** — *Outcome Engineering* — arguing
that agentic development demands a new frame.[^19]<!-- -->[^20] Its thesis: **"It was never about the
code."** Code is "the incantation transforming computation into magic," a *mechanism* for
delivering an idea. Once agents remove the constraint of human typing bandwidth, the
manifesto argues, creation is limited by the *cost of compute*, not human capacity — and the
profession should move "beyond software engineering" toward engineering **outcomes**.[^19]

Treat this as an emerging framing, not a settled body of practice: at this writing the
manifesto is months old, its vocabulary is still contested, and no independent evidence
yet shows teams shipping better outcomes by adopting it. Read it the way you would read
the Agile Manifesto in 2001 — a position paper whose worth the next decade will decide.

It is organized around four shifts and **16 principles** in two parts.[^19] Whatever you make of
its rhetoric, its principles map with surprising directness onto the disciplines in this
book — which is itself an argument that the fundamentals endure.

**The four shifts:** *Creation not code. Cost not time. Capacity not backlog. Certainty
not vibes.*[^19]

### Part I — The Goals ("superpowered creation")

1. **The Voyage — Human Intent.** Agents explore paths; humans choose the destination.
   Don't abdicate vision to the machine. *(This book: requirements and goals, Ch. 3.)*
2. **The Truth — Verified Reality is the Only Truth.** Code is a vanity metric; grade agents
   on the verified rate of positive change delivered, not lines written. *(Testing &
   metrics, Ch. 10, 11.)*
3. **The Teamwork — No More Single Player Mode.** Outcome engineering is a team sport;
   define explicit protocols for debate, decision, and delivery. *(Process, Ch. 2.)*
4. **The Liberation — The Backlog is Dead.** Never reject an idea for lack of *time*, only
   lack of *budget*; manage to cost, not capacity. *(Prioritization reframed, Ch. 4.)*
5. **The Joy — Unleash the Builders.** Write code only when it brings joy; delegate
   the toil. *(Essential vs. accidental complexity, Ch. 1.)*
6. **The Map — No Wandering in the Dark.** Never dispatch an agent without context; map the
   territory before building. *(Architecture description, Ch. 6.)*
7. **The Tech Island — Build It All.** When code is the cheapest resource, build to answer
   questions and test hypotheses. *(Prototyping to reduce risk, Ch. 2.)*
8. **The Artifacts — Failures are Artifacts.** Don't just roll back; dissect the failure and
   debug the *decision*, not only the code. *(Retrospectives & post-mortems, Ch. 2, 8.)*

### Part II — The Building ("the iron price")

9. **The Orchestration — Agentic Coordination is a New Org.** Scaling agents mirrors scaling
   people, "faster, weirder, and harder"; design the org chart for the swarm. *(Team
   structure, Ch. 2 / Appendix A.)*
10. **The Law — Code the Constitution.** Encode mission, vision, and rules into the
    environment so agents can parse intent; ambiguity is the enemy of alignment.
    *(Specifications & acceptance criteria, Ch. 3, 5.)*
11. **The Graph — All the Context, Everywhere.** Embed context into the infrastructure (a
    knowledge graph), not just the prompt. *(Architectural views & documentation, Ch. 6.)*
12. **The Order — Priorities Drive Compute.** Compute is still a cost; always know the next
    most important task. *(Value/cost/risk prioritization, Ch. 4.)*
13. **The Documentation — Show Your Work.** Code is the *what*; reasoning is the *why* —
    require agents to record discoveries and rejected paths. *(ADRs & rationale, Ch. 6.)*
14. **The Immune System — Continuous Improvement.** Repeating a mistake is a system failure;
    spend compute on the post-mortem and inoculate against recurrence. *(Process
    improvement & metrics, Ch. 2, 11.)*
15. **The Gate — Risk Stops the Line.** Make risk a *blocking* function; if risk is unknown
    or unmitigated, the line stops. *(Static checking as a quality gate, Ch. 9.)*
16. **The Validation — Audit the Outcomes.** Trust is a vulnerability; models drift, so
    continuously audit agents against the domain. *(Test adequacy & monitoring, Ch. 10–11.)*

### A reading: what's strong, what's open

**What's compelling.** The manifesto's center of gravity — *verified reality over vanity
metrics*, *outcomes over activity*, *encode intent explicitly*, *make risk a blocking
gate*, *audit continuously* — is essentially this book's quality philosophy, restated for a
world where a machine writes the first draft. Principles 2, 10, 14, 15, and 16 are almost a
summary of Chapters 9–12. That convergence is the point: **when generation is cheap,
specification and verification become the whole game.**

**What's open to challenge.** Treat it as a provocation, not gospel:

- *"The backlog is dead / cost not capacity"* assumes compute is cheap and value is easy to
  price. Prioritization under scarcity (Chapter 4) does not vanish; its currency changes.
- *"Certainty, not vibes"* is a high bar. The oracle problem (§13.2.7) means some outcomes
  remain expensive or impossible to verify automatically; "verified reality" has real
  limits.
- The **productivity paradox** (§13.1.4) cautions against assuming agents are a pure
  accelerator; the verification bottleneck can dominate.
- **Deskilling risk:** if engineers stop writing and reviewing code closely, who retains the
  judgment to *audit the outcomes*? The manifesto's own Principle 16 depends on expertise it
  could erode.

Held critically, Outcome Engineering is a useful lens: it names the shift from *producing*
software to *directing and verifying* its production — which is exactly the shift this
chapter has been describing.

## 13.5 Principles for the AI-Augmented Engineer

Synthesizing the evidence and the manifesto into working advice:

1. **Own intent and verification.** Choose the destination and define "correct"; let agents
   explore paths. You are accountable for what ships (Chapter 1's ethics do not delegate).
2. **Keep the fundamentals.** You cannot safely accept what you cannot evaluate. Understand
   the design, the tests, and the metrics well enough to catch a confident wrong answer.
3. **Shift your effort up the stack.** Spend the time AI frees on *specifying* (clear
   requirements, acceptance criteria, ADRs) and *checking* (reviews, coverage, metrics) —
   not on generating more code.
4. **Manage the new risks.** Security defects, license/provenance of generated code,
   hallucination, over-trust, and skill atrophy are now first-class engineering concerns.
5. **Measure outcomes, not activity.** Judge yourself and your agents by verified value
   delivered and defects escaped — never by lines or PR counts.

## 13.6 Conclusion

AI does not repeal the four pressures of software engineering; it *relocates* their weight.
Producing code gets cheaper, so **deciding what to build and proving it works** — the
subject of every chapter in this book — becomes the differentiator. The disciplines you
learned are promoted, not made quaint. Requirements become the prompt.
Specifications become the constitution. Tests and reviews become the trust layer over a
firehose of generated code. Metrics become the proof that an *outcome*, not just an output,
was delivered.

The o16g manifesto pushes this to its edge — *it was never about the code* — and whether or
not you accept its every claim, it points where the profession is heading: engineers who
direct fleets of agents toward well-specified, rigorously verified outcomes. That job is not
less engineering. It is *more* of the hardest, most human parts of it.

---

### Sources

[^1]: GitHub (Eirini Kalliamvakou), *Research: Quantifying GitHub Copilot's Impact on Developer Productivity and Happiness* (2022). [github.blog](https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/).
[^2]: Sida Peng, Eirini Kalliamvakou, Peter Cihon, and Mert Demirer, *The Impact of AI on Developer Productivity: Evidence from GitHub Copilot* (2023). [arXiv 2302.06590](https://arxiv.org/abs/2302.06590).
[^3]: METR (Joel Becker, Nate Rush, Elizabeth Barnes, and David Rein), *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity* (2025). [metr.org](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) · [arXiv 2507.09089](https://arxiv.org/abs/2507.09089).
[^4]: Kent Beck et al., *Principles behind the Agile Manifesto* (2001). [agilemanifesto.org](https://agilemanifesto.org/principles.html).
[^5]: Madhava Krishna, Bhagesh Gaur, Arsh Verma, and Pankaj Jalote, *Using LLMs in Software Requirements Specifications: An Empirical Evaluation* (2024). [arXiv 2404.17842](https://arxiv.org/abs/2404.17842).
[^6]: Asma Yamani, Malak Baslyman, and Moataz Ahmed, *Leveraging LLMs for User Stories in AI Systems: UStAI Dataset* (2025). [arXiv 2504.00513](https://arxiv.org/abs/2504.00513).
[^7]: Haowei Cheng et al., *Generative AI for Requirements Engineering: A Systematic Literature Review* (2024). [arXiv 2409.06741](https://arxiv.org/abs/2409.06741).
[^8]: Sirui Hong et al., *MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework* (2023). [arXiv 2308.00352](https://arxiv.org/abs/2308.00352).
[^9]: Ruiyin Li et al., *Bridging Requirements and Architecture: Multi-Agent Orchestration with External Knowledge and Hierarchical Memory* (2026). [arXiv 2606.01385](https://arxiv.org/abs/2606.01385).
[^10]: Google Research, *Resolving Code Review Comments with Machine Learning* (2023). [research.google](https://research.google/blog/resolving-code-review-comments-with-ml/).
[^11]: Sundar Pichai, Alphabet Q3 2024 earnings-call remarks — more than a quarter of new code at Google is AI-generated, then reviewed by engineers — as reported by Fortune (2024). [fortune.com](https://fortune.com/2024/10/30/googles-code-ai-sundar-pichai/).
[^12]: Neil Perry, Megha Srivastava, Deepak Kumar, and Dan Boneh, *Do Users Write More Insecure Code with AI Assistants?* (CCS 2023). [arXiv 2211.03622](https://arxiv.org/abs/2211.03622).
[^13]: Carlos E. Jimenez et al., *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* (2023). [arXiv 2310.06770](https://arxiv.org/abs/2310.06770) · leaderboard at [swebench.com](https://www.swebench.com/).
[^14]: Niels Mündler, Mark Niklas Müller, Jingxuan He, and Martin Vechev, *SWT-Bench: Testing and Validating Real-World Bug-Fixes with Code Agents* (2024). [arXiv 2406.12952](https://arxiv.org/abs/2406.12952).
[^15]: Reem Aleithan et al., *SWE-Bench+: Enhanced Coding Benchmark for LLMs* (2024). [arXiv 2410.06992](https://arxiv.org/abs/2410.06992).
[^16]: Max Schäfer, Sarah Nadi, Aryaz Eghbali, and Frank Tip, *An Empirical Evaluation of Using Large Language Models for Automated Unit Test Generation* (2023). [arXiv 2302.06527](https://arxiv.org/abs/2302.06527).
[^17]: GitClear (William Harding et al.), *AI Copilot Code Quality: 2025 Research* (2025). [gitclear.com](https://www.gitclear.com/ai_assistant_code_quality_2025_research).
[^18]: Hammond Pearce et al., *Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions* (2021). [arXiv 2108.09293](https://arxiv.org/abs/2108.09293).
[^19]: Cory Ondrejka, *Outcome Engineering — The o16g Manifesto* (2026). [o16g.com](https://o16g.com/manifesto/).
[^20]: Onebrief, *Onebrief Hires Cory Ondrejka as Chief Technology Officer* (2026). [businesswire.com](https://www.businesswire.com/news/home/20260203520166/en/Onebrief-Hires-Cory-Ondrejka-as-Chief-Technology-Officer-to-Drive-Next-Gen-Command-Operating-System).

---

- **Key takeaways** are summarized above in §13.6.
- Continue to the [Exercises](exercises.md).
- Go deeper with the [Open Resources](resources.md) for this chapter.
