# Chapter 7 — Architectural Patterns

> **Where we are.** Chapter 6 argued that the way to tame a large system is to decompose
> it into modules with high cohesion and low coupling. That advice is true but abstract:
> it tells you *what good structure looks like* without telling you *which structure to
> reach for* when you sit down to design a real system. This chapter closes that gap. An
> **architectural pattern** is a reusable, named arrangement of modules and connectors
> that has repeatedly solved a recurring design problem.[^1] [^2] Learning the catalog means you
> rarely start from a blank page — and, better still, that you can *reason about the
> trade-offs* of a structure before you commit code to it.

A pattern is not a library you install or a framework you inherit. It is a *shape* — a
recurring answer to a recurring question about how responsibilities and dependencies
should be arranged. When someone says "we'll put a message broker in the middle" or
"the UI is just a view over the model," they are naming a pattern, and everyone who
knows the vocabulary immediately shares a picture of the structure, its participants,
and the compromises it implies. That shared picture is the real payoff. Patterns give a
team a *design language* precise enough to argue in.

One honest caveat before the catalog: the patterns in this chapter do not all live at
the same altitude, even though tradition files them under one name.[^3] Layering, shared
data, and client-server shape *entire systems*; MVC organizes a *subsystem*; the
observer is an object-level *design pattern* that architectures merely lean on; REST is
a *convention for interfaces* between systems; and product lines are a *strategy across
a family* of systems. Keep the altitude in mind as you read — "should we use observer
or a product line?" is not a choice anyone faces, and knowing which level a pattern
addresses tells you which decisions it can and cannot make for you.

Every pattern in this chapter is presented the same way, so you can compare them fairly:
the **problem** it solves, its **structure** (with a diagram), the **participants** and
their responsibilities, the **trade-offs** you accept by adopting it, and a concrete
**example** from systems you have probably used. Read for the trade-offs above all. The
mark of an engineer, as Chapter 1 put it, is knowing *when a pattern earns its cost and
when it is overkill*, not merely that it exists.

> **Principle.** A pattern is a *contract with consequences*. Adopting it buys you some
> qualities (flexibility, testability, scalability) and charges you others (indirection,
> latency, more moving parts). If you cannot name what you are buying and what you are
> paying, you are cargo-culting, not designing.

## 7.1 Software Layering

### 7.1.1 The Layered Pattern

Almost every substantial system you will build is organized, at the coarsest level, into
**layers**. The **layered pattern** stacks the system into horizontal tiers, where each
layer offers services to the layer directly above it and consumes services from the
layer directly below.[^1] A layer is a group of modules that operate at the same level of
abstraction: the top speaks the language of the user's problem, the bottom speaks the
language of the machine, and the middle layers translate progressively between them.

**Problem it solves.** A system spans a huge range of abstraction. At the top, you care
about "confirm the appointment"; at the bottom, you care about "write these bytes to a
socket." If every part of the code were free to talk to every other part, a change to
the database driver could ripple into the appointment-booking logic, and you could not
reason about either in isolation. Layering imposes order on that range of abstraction by
insisting that dependencies point *downward only*. High-level policy depends on
low-level mechanism through a stable interface, never the reverse.

**Structure.** A classic business application uses three or four layers. The
**presentation** layer renders the interface and interprets user input. The
**application** (or service) layer coordinates use cases and enforces workflow. The
**domain** layer holds the core business rules and entities. The **infrastructure** (or
persistence) layer talks to databases, message queues, and the outside world.

```mermaid
flowchart TD
    P["Presentation layer<br/>(screens, controllers, API endpoints)"]
    A["Application / service layer<br/>(use-case coordination, transactions)"]
    D["Domain layer<br/>(business rules, entities)"]
    I["Infrastructure layer<br/>(database, messaging, external APIs)"]
    P -->|calls, depends on| A
    A -->|calls, depends on| D
    D -->|calls, depends on| I
    classDef layer fill:#eef,stroke:#66a,color:#000;
    class P,A,D,I layer;
```

**Participants.** Each layer is a participant with one responsibility: to provide a
coherent set of services at its level of abstraction and to hide the layer beneath it.
The *interface* of a layer — the set of operations it exposes upward — is itself a
participant, because it is the contract that lets the upper layer stay ignorant of the
lower layer's internals.

A design decision you must make explicitly is whether layers are **strict** (a layer may
call *only* the layer immediately below it) or **relaxed** (a layer may call any layer
below it). Strict layering maximizes isolation — you could replace the domain layer's
notion of persistence without the presentation layer noticing — but it costs you
"pass-through" code, where a layer exposes an operation for no reason but to forward it
down. Relaxed layering removes that boilerplate but weakens the guarantee, because now
the presentation layer might reach past the application layer straight into
infrastructure, coupling the top of the stack to the bottom.

**A real example.** The seven-layer OSI model of network protocols is the textbook case:
your application code hands a message down the stack without knowing whether it
travels over copper, fiber, or radio, because each layer presents a clean service to the
one above.[^4] Closer to daily work, the standard three-tier web application — browser,
application server, database — is layering you already rely on, and any framework
organized as "controllers → services → repositories" is layering by another name.

### 7.1.2 Design Trade-offs

Layering is popular because its benefits are real and general. It gives you
**substitutability**: because a layer depends only on the *interface* below it, you can
swap one implementation for another — an in-memory store for a real database in tests, a
new payment provider for an old one — without touching the layers above. It gives you
**separation of concerns**, so a developer can work on presentation without understanding
persistence. And it gives you a **shared mental model**: new engineers can find their way
because "where does this code go?" usually has an obvious layered answer.

But the pattern is not free, and pretending otherwise is a common source of pain.

> **Pitfall.** *The pass-through tax.* In strict layering, a field the user enters at the
> top must often be threaded through every layer to reach the database — a change to add
> one field touches presentation, application, domain, and infrastructure. When most of
> your layers merely forward data without transforming it, the layering is buying you
> little and costing you edits in four files per change.

There is also a **performance** cost. Each layer boundary is a call, sometimes a
serialization, occasionally a network hop. For most applications this is negligible; for
a latency-critical inner loop it is not, and you may deliberately collapse layers in the
hot path. And layering says nothing about horizontal scaling — a beautifully layered
monolith is still one deployable unit.

The deeper trade-off is between **isolation and directness**. Strict layers isolate
change but add indirection; relaxed layers are direct but let coupling leak. The right
call depends on which changes you expect. If you expect to swap infrastructure often,
pay for strictness. If your layers are thin and stable, relax them. Notice that this is
the Chapter 1 principle in action: *make likely changes cheap*, and accept a
small standing cost to do it.

## 7.2 Three Building Blocks

Before the larger architectures, you need three smaller building blocks that appear *inside*
almost all of them. They are the mortar between the bricks: how modules share state
without becoming tangled (shared data), how they react to each other's changes without
tight coupling (the observer), and — implicit in both — how a stable interface lets
independent parts evolve. Master these and the big patterns become recombinations of
ideas you already understand.

### 7.2.1 The Shared-Data Pattern

**Problem it solves.** Many components need to read and write a common body of data:
several tools operate on the same document, several services on the same customer record.
If each component kept its own copy, you would face the treacherous job of keeping the
copies consistent. The **shared-data** (or **repository**) pattern gives the components a
single, central data store that they all access through a defined interface, making the
store the authoritative source of truth.[^2]

**Structure.** A central **data store** sits at the hub. Around it, independent
**accessor** components read and write, but they do not talk to each other directly —
they communicate *through* the shared data. The store owns concerns that would otherwise
be duplicated: consistency, concurrency control, integrity constraints, and durability.

```mermaid
flowchart TD
    subgraph accessors [Independent accessors]
        C1[Component A]
        C2[Component B]
        C3[Component C]
    end
    DS[("Shared data store<br/>(single source of truth)")]
    C1 <--> DS
    C2 <--> DS
    C3 <--> DS
    classDef c fill:#efe,stroke:#6a6,color:#000;
    class C1,C2,C3 c;
```

**Participants.** The **data store** is responsible for holding state and enforcing its
invariants. The **accessors** are responsible for the actual computation; they are
decoupled from each other because their only shared knowledge is the store's schema and
interface. Often one accessor's writes become another's inputs — a compiler's symbol
table, written by the parser and read by the type checker, is a shared-data design.

**Trade-offs.** The great advantage is that accessors are mutually independent: you can
add a new one without touching the others, because they coordinate only through the
store. The great danger is that the store becomes a **coupling magnet** and a
**bottleneck**. Because everyone depends on the schema, a schema change can break every
accessor at once — the store's interface is now a system-wide contract. And because
every access funnels through one place, the store can become the scalability limit and a
single point of failure. Relational databases, blackboard systems in AI, and the Redux
"single store" in front-end apps are all shared-data designs, and all of them live with
this same tension between convenient centralization and dangerous centralization.[^1] [^5]

### 7.2.2 Observers and Subscribers — the Observer Pattern

**Problem it solves.** One object holds state that others care about, and those others
must react when it changes — a spreadsheet cell changes and every chart derived from it
must redraw. The naive solution has the state-holder call each interested party directly,
but that means the state-holder must *know about* every interested party, hard-coding a
dependency on things that logically depend on *it*. The **observer** pattern inverts that
dependency: interested parties **subscribe**, and the state-holder notifies its
subscribers without knowing who or what they are.[^6]

**Structure.** A **subject** maintains a list of **observers** and offers `subscribe` and
`unsubscribe` operations. When the subject's state changes, it iterates its list and
calls a uniform `notify`/`update` operation on each observer. The subject knows only that
observers implement that operation; it knows nothing else about them.

```mermaid
flowchart LR
    Subj["Subject<br/>observers: List&lt;Observer&gt;<br/>subscribe() / notify()"]
    O1["Observer 1<br/>update()"]
    O2["Observer 2<br/>update()"]
    O3["Observer 3<br/>update()"]
    O1 -.->|subscribe| Subj
    O2 -.->|subscribe| Subj
    O3 -.->|subscribe| Subj
    Subj -->|"notify() on change"| O1
    Subj -->|"notify()"| O2
    Subj -->|"notify()"| O3
    classDef s fill:#fee,stroke:#a66,color:#000;
    class O1,O2,O3 s;
```

In the clinic scheduler, the waiting-room display must redraw when an appointment's
status changes:

```generic
type Appointment
  status
  observers   // list of notification callbacks

function subscribe(appointment, observer)
  append observer to appointment.observers

function set_status(appointment, new_status)
  appointment.status <- new_status
  for each notify in appointment.observers do   // any subscriber will do
    notify(appointment)
  end for

appt <- new Appointment with status "booked"
subscribe(appt, function(a) print "display: appointment is now " + a.status)
set_status(appt, "arrived")   // prints: display: appointment is now arrived
```

```go
type Observer func(*Appointment)

type Appointment struct {
	Status    string
	observers []Observer
}

func (a *Appointment) Subscribe(observer Observer) {
	a.observers = append(a.observers, observer)
}

func (a *Appointment) SetStatus(newStatus string) {
	a.Status = newStatus
	for _, notify := range a.observers { // any Observer func will do
		notify(a)
	}
}

func main() {
	appt := &Appointment{Status: "booked"}
	appt.Subscribe(func(a *Appointment) {
		fmt.Println("display: appointment is now " + a.Status)
	})
	appt.SetStatus("arrived") // prints: display: appointment is now arrived
}
```

```java
interface Observer { void update(Appointment appointment); }

class Appointment {
  String status = "booked";
  private final List<Observer> observers = new ArrayList<>();

  void subscribe(Observer observer) { observers.add(observer); }

  void setStatus(String newStatus) {
    status = newStatus;
    for (Observer obs : observers) obs.update(this);   // any Observer will do
  }
}

class WaitingRoomDisplay implements Observer {
  public void update(Appointment appointment) {
    IO.println("display: appointment is now " + appointment.status);
  }
}

void main() {
  Appointment appt = new Appointment();
  appt.subscribe(new WaitingRoomDisplay());
  appt.setStatus("arrived");             // prints: display: appointment is now arrived
}
```

```javascript
class Appointment {
  constructor(status = "booked") {
    this.status = status;
    this.observers = [];
  }

  subscribe(callback) {
    this.observers.push(callback);
  }

  setStatus(newStatus) {
    this.status = newStatus;
    for (const notify of this.observers) notify(this);  // any callback will do
  }
}

const waitingRoomDisplay = (appointment) =>
  console.log(`display: appointment is now ${appointment.status}`);

const appt = new Appointment();
appt.subscribe(waitingRoomDisplay);
appt.setStatus("arrived");               // prints: display: appointment is now arrived
```

```python
class Appointment:
  def __init__(self, status="booked"):
    self.status = status
    self._observers = []

  def subscribe(self, observer):
    self._observers.append(observer)

  def set_status(self, new_status):
    self.status = new_status
    for obs in self._observers:      # any object with update() will do
      obs.update(self)

class WaitingRoomDisplay:
  def update(self, appointment):
    print(f"display: appointment is now {appointment.status}")

appt = Appointment()
appt.subscribe(WaitingRoomDisplay())
appt.set_status("arrived")               # prints: display: appointment is now arrived
```

```ruby
class Appointment
  attr_reader :status

  def initialize(status = "booked")
    @status = status
    @observers = []
  end

  def subscribe(&block)
    @observers << block
  end

  def set_status(new_status)
    @status = new_status
    @observers.each { |notify| notify.call(self) }  # any block will do
  end
end

appt = Appointment.new
appt.subscribe { |a| puts "display: appointment is now #{a.status}" }
appt.set_status("arrived")               # prints: display: appointment is now arrived
```

```typescript
type Observer = (appointment: Appointment) => void;

class Appointment {
  status: string;
  private observers: Observer[] = [];

  constructor(status: string = "booked") {
    this.status = status;
  }

  subscribe(callback: Observer): void {
    this.observers.push(callback);
  }

  setStatus(newStatus: string): void {
    this.status = newStatus;
    for (const notify of this.observers) notify(this);  // any callback will do
  }
}

const waitingRoomDisplay: Observer = (appointment) =>
  console.log(`display: appointment is now ${appointment.status}`);

const appt = new Appointment();
appt.subscribe(waitingRoomDisplay);
appt.setStatus("arrived");               // prints: display: appointment is now arrived
```

Nowhere does `Appointment` name a concrete observer type — it iterates whatever
subscribed and invokes each one's notification callback.

**Participants.** The **subject** (or *observable*) owns the state and the subscriber
list. The **observer** (or *subscriber*) implements the callback that runs on change. The
crucial property is the direction of the dependency: observers depend on the subject's
*notification interface*, and the subject depends on the observers' *update interface* —
neither depends on the other's concrete type. This is why you can add a new observer
without recompiling the subject.

At larger scale the same idea becomes **publish-subscribe**: publishers emit *events* to
named channels or topics, and subscribers register interest in topics rather than in a
specific subject.[^7] A message broker (§7.5.3) sits in the middle so that publishers and
subscribers need not even know the other exists or be running at the same time. Observer
is publish-subscribe in miniature, in one process; pub/sub is observer scaled across a
network.

**Trade-offs.** You gain **loose coupling** and **extensibility**: the subject is closed
to modification but open to new observers, which is precisely the flexibility a GUI
toolkit or an event system needs. You pay in **traceability** and **surprise**. Control
flow becomes implicit — reading the subject's code, you cannot see what happens when it
fires an event, because the reactions live elsewhere and are wired up at runtime. Bugs
hide in the ordering of notifications, in observers that trigger further changes (cascade
and cycles), and in **lapsed listeners** that forget to unsubscribe and leak memory. Use
the observer when the set of reactions is open-ended and you want the source to stay
ignorant of them; avoid it when a plain direct call would be clearer and the reactions
are fixed.

## 7.3 User Interfaces: Model-View-Controller

### 7.3.1 Design Decisions

Interactive applications share a hard problem: the same underlying information must be
*displayed* in one or more ways, *edited* through user gestures, and *stored* somewhere
durable — and each of those concerns changes on a different schedule and for different
reasons. Visual design changes when a designer redoes the look. Interaction changes when
you add a keyboard shortcut. Business rules change when the domain changes. If all three
concerns live in one tangled blob — the "smart widget" that draws itself, handles clicks,
*and* enforces business rules — every change risks breaking the others, and none of it
can be tested without a running screen.

The governing design decision, then, is a **separation of concerns**: keep the *data and
rules* apart from the *presentation* apart from the *input handling*. A second decision
follows: because one piece of data may drive several displays, the data should not depend
on any particular display — displays should depend on the data. That is the observer
relationship of §7.2.2, and it is the engine inside every UI architecture in
this family.

### 7.3.2 The Basic Model-View-Controller Pattern

**Problem it solves.** How do you build an interactive application so that its appearance,
its input handling, and its core logic can each change independently and be tested
independently? **Model-View-Controller (MVC)** answers by splitting the application into
three roles.

**Structure and participants.**

- The **model** holds the application's data and business rules. It knows nothing about
  the screen. It is a plain, testable object that could run in a batch job with no UI at
  all. When its state changes, it announces the change to whoever is listening.
- The **view** renders the model for the user. It reads from the model and draws; it
  holds no business rules of its own. Several views may show the same model differently —
  a table and a chart of the same numbers.
- The **controller** interprets user input (clicks, keystrokes, gestures) and translates
  it into operations on the model. It contains the *interaction* logic that connects
  gestures to intentions.

The wiring is what makes MVC more than three boxes. The view **observes** the model: when
the model changes, it notifies its views, and each view re-reads the model and redraws.
This is why editing data in one place updates every view of it automatically.

```mermaid
flowchart TD
    U((User))
    V["View<br/>renders model"]
    C["Controller<br/>interprets input"]
    M["Model<br/>data + business rules"]
    U ~~~ V
    V -->|"reads state"| M
    V -->|"shows"| U
    U -->|"gestures<br/>(clicks, keys)"| C
    C -->|"updates state"| M
    M -.->|"notify change (observer)"| V
    classDef mvc fill:#eef,stroke:#66a,color:#000;
    class C,M,V mvc;
```

**A real example.** The pattern was born in desktop UI toolkits and now underlies most
web frameworks.[^8] In a server-side web app, an incoming request is dispatched to a
*controller* action, which manipulates *model* objects (and their database records) and
then selects a *view* (a template) to render the response. The exact division of labor
varies — UI frameworks have spawned close cousins called **MVP**
(Model-View-Presenter) and **MVVM** (Model-View-ViewModel), which differ mainly in how
much logic sits between the view and the model and in which direction the wiring points.[^9]
What they share, and what you should carry away, is the core commitment: *the model does
not depend on the view*.

**Trade-offs.** MVC buys you **independent evolution and testability**. Because the model
has no UI dependencies, you can unit-test all your business rules without simulating a
screen — often the single biggest testability win available in an interactive app. You
can restyle the view or add a second view without touching the model. The cost is
**structure for its own sake in small cases**: a trivial screen split into three
collaborating objects is more indirection than a beginner expects, and the boundary
between "controller logic" and "model logic" is a perennial source of debate that spawns
those competing variants. As with layering, the pattern pays off in proportion to how
often, and how independently, the three concerns actually change.

### 7.3.3 Keep Views Simple

The single most valuable discipline within MVC is to keep views **thin** — sometimes
called the *humble view*.[^10] A view should contain as little logic as you can manage:
ideally it only reads values from the model (or a view-model prepared for it) and maps
them onto widgets. It should contain no business rules, no decisions that matter, and no
state that cannot be trivially reconstructed from the model.

Why so insistent? Because the view is the *one part you cannot easily test*. Automated
tests can exercise a model directly, but exercising a rendered screen usually means slow,
brittle UI automation. Every branch, calculation, or rule you allow to creep into the
view is a branch that escapes your fast, reliable tests and hides where only a human
clicking around will find its bugs. Pushing that logic down into the model — or into a
dedicated **presenter/view-model** whose job is to pre-compute exactly what the view
should show — moves it back under test.

In the clinic app's invoice list, a fat view buries the overdue rule where no unit test
reaches it:

```generic
function render(invoice, today)
  text <- invoice.patient_name
  if not invoice.paid and days_between(invoice.sent_on, today) > 30 then
    text <- text + " — OVERDUE"   // a business rule, trapped on screen
  end if
  return text
```

```go
type InvoiceWidget struct{}

func (w InvoiceWidget) Render(invoice Invoice, today time.Time) string {
	text := invoice.PatientName
	if !invoice.Paid && today.Sub(invoice.SentOn).Hours() > 30*24 {
		text += " — OVERDUE" // a business rule, trapped on screen
	}
	return text
}
```

```java
class InvoiceWidget {
  String render(Invoice invoice, LocalDate today) {
    String text = invoice.patientName();
    if (!invoice.paid() && ChronoUnit.DAYS.between(invoice.sentOn(), today) > 30) {
      text += " — OVERDUE";              // a business rule, trapped on screen
    }
    return text;
  }
}
```

```javascript
const MS_PER_DAY = 86_400_000;

class InvoiceWidget {
  render(invoice, today) {
    let text = invoice.patientName;
    if (!invoice.paid && (today - invoice.sentOn) / MS_PER_DAY > 30) {
      text += " — OVERDUE";              // a business rule, trapped on screen
    }
    return text;
  }
}
```

```python
class InvoiceWidget:
  def render(self, invoice, today):
    text = invoice.patient_name
    if not invoice.paid and (today - invoice.sent_on).days > 30:
      text += " — OVERDUE"         # a business rule, trapped on screen
    return text
```

```ruby
class InvoiceWidget
  def render(invoice, today)
    text = invoice.patient_name
    if !invoice.paid && (today - invoice.sent_on) > 30
      text += " — OVERDUE"             # a business rule, trapped on screen
    end
    text
  end
end
```

```typescript
const MS_PER_DAY = 86_400_000;

interface Invoice {
  patientName: string;
  sentOn: Date;
  paid: boolean;
}

class InvoiceWidget {
  render(invoice: Invoice, today: Date): string {
    let text = invoice.patientName;
    if (!invoice.paid && (+today - +invoice.sentOn) / MS_PER_DAY > 30) {
      text += " — OVERDUE";              // a business rule, trapped on screen
    }
    return text;
  }
}
```

The humble version moves the rule into a view-model and leaves the view nothing to decide:

```generic
// the rule, extracted where tests reach it
function is_overdue(invoice, today)
  return not invoice.paid and days_between(invoice.sent_on, today) > 30

function invoice_view_model(invoice, today)
  if is_overdue(invoice, today) then badge <- " — OVERDUE" else badge <- ""
  return view model with text = invoice.patient_name + badge

// the view maps a precomputed field to a widget
function render(vm)
  return vm.text
```

```go
// the rule, extracted where tests reach it
func isOverdue(invoice Invoice, today time.Time) bool {
	return !invoice.Paid && today.Sub(invoice.SentOn).Hours() > 30*24
}

type InvoiceViewModel struct{ Text string }

func invoiceViewModel(invoice Invoice, today time.Time) InvoiceViewModel {
	badge := ""
	if isOverdue(invoice, today) {
		badge = " — OVERDUE"
	}
	return InvoiceViewModel{Text: invoice.PatientName + badge}
}

// the view maps a precomputed field to a widget
func (w InvoiceWidget) Render(vm InvoiceViewModel) string { return vm.Text }
```

```java
// the rule, extracted where tests reach it
boolean isOverdue(Invoice invoice, LocalDate today) {
  return !invoice.paid() && ChronoUnit.DAYS.between(invoice.sentOn(), today) > 30;
}

record InvoiceViewModel(String text) {}

InvoiceViewModel invoiceViewModel(Invoice invoice, LocalDate today) {
  String badge = isOverdue(invoice, today) ? " — OVERDUE" : "";
  return new InvoiceViewModel(invoice.patientName() + badge);
}

class InvoiceWidget {
  String render(InvoiceViewModel vm) {   // maps a precomputed field to a widget
    return vm.text();
  }
}
```

```javascript
function isOverdue(invoice, today) {     // the rule, extracted where tests reach it
  return !invoice.paid && (today - invoice.sentOn) / MS_PER_DAY > 30;
}

function invoiceViewModel(invoice, today) {
  const badge = isOverdue(invoice, today) ? " — OVERDUE" : "";
  return { text: invoice.patientName + badge };
}

class InvoiceWidget {
  render(vm) {                           // maps a precomputed field to a widget
    return vm.text;
  }
}
```

```python
def is_overdue(invoice, today):          # the rule, extracted where tests reach it
  return not invoice.paid and (today - invoice.sent_on).days > 30

def invoice_view_model(invoice, today):
  badge = " — OVERDUE" if is_overdue(invoice, today) else ""
  return {"text": invoice.patient_name + badge}

class InvoiceWidget:
  def render(self, vm):                # maps a precomputed field to a widget
    return vm["text"]
```

```ruby
def overdue?(invoice, today)             # the rule, extracted where tests reach it
  !invoice.paid && (today - invoice.sent_on) > 30
end

def invoice_view_model(invoice, today)
  badge = overdue?(invoice, today) ? " — OVERDUE" : ""
  { text: invoice.patient_name + badge }
end

class InvoiceWidget
  def render(vm)                         # maps a precomputed field to a widget
    vm[:text]
  end
end
```

```typescript
interface InvoiceViewModel {
  text: string;
}

// the rule, extracted where tests reach it
function isOverdue(invoice: Invoice, today: Date): boolean {
  return !invoice.paid && (+today - +invoice.sentOn) / MS_PER_DAY > 30;
}

function invoiceViewModel(invoice: Invoice, today: Date): InvoiceViewModel {
  const badge = isOverdue(invoice, today) ? " — OVERDUE" : "";
  return { text: invoice.patientName + badge };
}

class InvoiceWidget {
  render(vm: InvoiceViewModel): string {   // maps a precomputed field to a widget
    return vm.text;
  }
}
```

The extracted rule now tests in a few short lines, with no widget in sight:

```generic
function test_unpaid_31_days_is_overdue()
  adilyn <- Invoice with name "Adilyn", sent_on 2026-06-01, paid false
  assert is_overdue(adilyn, 2026-07-02)   // unpaid, sent 31 days ago
```

```go
func TestUnpaid31DaysIsOverdue(t *testing.T) {
	adilyn := Invoice{"Adilyn", time.Date(2026, 6, 1, 0, 0, 0, 0, time.UTC), false}
	if !isOverdue(adilyn, time.Date(2026, 7, 2, 0, 0, 0, 0, time.UTC)) {
		t.Error("unpaid invoice sent 31 days ago should be overdue")
	}
}
```

```java
void testUnpaid31DaysIsOverdue() {
  assert isOverdue(new Invoice("Adilyn", LocalDate.of(2026, 6, 1), false),
      LocalDate.of(2026, 7, 2));
}
```

```javascript
function testUnpaid31DaysIsOverdue() {
  const adilyn = { patientName: "Adilyn", sentOn: new Date("2026-06-01"), paid: false };
  assert(isOverdue(adilyn, new Date("2026-07-02")));
}
```

```python
def test_unpaid_31_days_is_overdue():   # the whole test: two lines
  assert is_overdue(Invoice("Adilyn", sent_on=date(2026, 6, 1), paid=False), date(2026, 7, 2))
```

```ruby
def test_unpaid_31_days_is_overdue
  adilyn = Invoice.new("Adilyn", Date.new(2026, 6, 1), false)
  raise unless overdue?(adilyn, Date.new(2026, 7, 2))
end
```

```typescript
function testUnpaid31DaysIsOverdue(): void {
  const adilyn: Invoice =
    { patientName: "Adilyn", sentOn: new Date("2026-06-01"), paid: false };
  assert(isOverdue(adilyn, new Date("2026-07-02")));
}
```

> **Principle.** *Put logic where it can be tested.* The humble-view rule is a
> testability strategy, not a matter of aesthetics. Treat the boundary of your test coverage as a
> design constraint, and keep the untestable layer as thin as physically possible.

> **MVC in the wild.** Real frameworks realize the pattern under shuffled names. Django
> calls its variant **MTV (Model-Template-View)**: Django's "view" plays the controller
> role and its "template" is the view — the same triad, relabeled.[^11] Rails is classic
> server-side MVC.[^12] **Single-page applications (SPAs)** built with React or Angular move
> the triad into the browser, often replacing two-way observer wiring with a
> **unidirectional data-flow** store (Flux/Redux): the view fires actions, the store
> updates, the view re-renders — the same separation with a stricter update discipline.[^5]
> Very large products run on each (Instagram on Django, Shopify on Rails, Airbnb on
> React), which is the point: the pattern, not the framework, is the transferable
> knowledge.[^13] [^14]<!-- -->[^15]

## 7.4 Dataflow Architectures

The patterns so far organize systems around *objects that call each other*. A different
family organizes systems around the *flow of data through transformations*. In a
**dataflow architecture**, you think first about the data — where it enters, how it is
transformed step by step, and where it exits — and the components fall out as the stages
that do the transforming. This inversion is powerful whenever the essence of a system is
"take this stream of stuff and progressively turn it into that stream of stuff."

### 7.4.1 Dataflow Pipelines — Pipes and Filters

**Problem it solves.** You must perform a *sequence* of independent transformations on a
body of data, and you want each transformation to be a self-contained unit you can build,
test, reuse, and reorder without knowing about its neighbors. The **pipes-and-filters**
pattern arranges the computation as a linear chain: each **filter** reads from an input
**pipe**, transforms what it reads, and writes to an output pipe that feeds the next
filter.[^1] [^2]

**Structure and participants.** A **filter** is a stateless-by-default component with one
job: consume input, produce output. A **pipe** is the connector that carries data from
one filter's output to the next filter's input — it is a buffer and a decoupler. Because
filters communicate *only* through pipes and share no other state, a filter knows nothing
about what comes before or after it; it only knows the shape of the data on its pipes.

```mermaid
flowchart TD
    subgraph R1 [" "]
        direction LR
        Src[(Source)] -->|pipe| F1["Filter: split"] -->|pipe| F2["Filter: transform"]
    end
    subgraph R2 [" "]
        direction LR
        F3["Filter: aggregate"] -->|pipe| Sink[(Sink)]
    end
    R1 -->|pipe| R2
    classDef f fill:#efe,stroke:#6a6,color:#000;
    class F1,F2,F3 f;
    style R1 fill:none,stroke:none
    style R2 fill:none,stroke:none
```

**A real example.** The Unix shell pipeline is the canonical case: six independent
filters chain into a "most frequent sources of 404 errors" report, and each command was
written by someone who never imagined this particular pipeline.

```bash
cat access.log  |   # read
  grep 404      |   # select
  cut -d' ' -f1 |   # project
  sort          |   # order
  uniq -c       |   # count
  sort -rn          # rank
```

Compilers are built the same way — lexer, parser, optimizer, code generator — and so is
any image or audio processing chain.

**Trade-offs.** The wins are **reuse and composability** (filters recombine into new
pipelines like Lego), **understandability** (each stage is simple in isolation), and
easy **parallelism** (adjacent filters can run concurrently, each working on data as it
arrives). The costs: pipes impose a **lowest-common-denominator data format** — often
plain text or byte streams — so filters spend effort parsing and re-serializing at every
boundary, and rich structure is awkward to pass through. A purely linear pipeline also
handles **errors** poorly: there is no natural place for a filter deep in the chain to
report a problem back upstream. And interactive, back-and-forth workloads simply do not
fit the one-directional flow.

### 7.4.2 Dataflow Networks

A strict pipeline is linear, but real transformations often **branch and merge**. A
**dataflow network** generalizes the pipeline into a directed graph: a filter may have
several inputs and several outputs, data may fan out to parallel branches and fan back
in, and the topology can express joins, splits, and conditional routing.

```mermaid
flowchart LR
    S[(Source)] --> A[Filter A]
    A --> B[Filter B]
    A --> C[Filter C]
    B --> D[Filter D: merge]
    C --> D
    D --> T[(Sink)]
    classDef f fill:#efe,stroke:#6a6,color:#000;
    class A,B,C,D f;
```

**Problem it solves and trade-offs.** Networks handle transformations whose natural shape
is a graph, not a line — enriching a record from two sources and combining the results,
or routing different record types down different processing paths. You keep the filters'
independence and composability, but you pay in **complexity of coordination**: a node
that merges two inputs must decide how to synchronize streams that arrive at different
rates, and the graph can deadlock if a cycle of full buffers waits on itself. Stream
processing frameworks, build systems (whose dependency graph *is* a dataflow network),
and spreadsheet recalculation engines are all dataflow networks. This is the structure
underneath modern **reactive** programming, where you declare how outputs are computed
from inputs and the runtime propagates changes through the graph for you.

### 7.4.3 Unbounded Streams

The pipelines above quietly assumed the data *ends* — a file has a last line, a document
a last page. Many important systems process data that never ends: sensor readings, user
clickstreams, financial ticks, log lines flowing in forever. An **unbounded stream**
changes the rules, because a filter can no longer "read all the input, then produce all
the output." It must produce results *incrementally*, from data it has seen so far,
without ever waiting for an end that will not come.

**Problem it solves and consequences.** Stream processing lets you compute continuously
and react in near-real-time instead of in nightly batches. But unboundedness forces
design decisions the batch world could ignore. You must reason in **windows** — "the
count of events in the last five minutes" — because "the total count" is never final.[^16] You
must handle **out-of-order and late data**, because events generated at one time may
arrive later, and you must decide how long to wait. You must bound memory, because you
cannot buffer an infinite stream, which means most computations must be *incremental* and
approximate. And **backpressure** becomes essential: when a downstream filter cannot keep
up, it must signal upstream to slow down — or the design must shed load deliberately — or
buffers overflow and the system falls over.[^17]

> **Case study.** A fraud-detection system watches a never-ending stream of card
> transactions and must flag a suspicious one within seconds. It cannot wait for a "batch"
> to close; it maintains a sliding window of recent activity per account, updates running
> statistics as each event arrives, and applies backpressure to the ingestion feed when
> the scoring stage saturates. Every hard part of this design is a direct consequence of
> the stream being *unbounded*.

### 7.4.4 Big Dataflows — MapReduce-Style

When the data is not just endless but *enormous* — too large for one machine — dataflow
becomes a strategy for **distributing** computation across a cluster. The
**MapReduce** style captures a pattern that recurs across huge batch jobs: express the
computation as a **map** step that transforms each record independently, followed by a
**reduce** step that aggregates the mapped results by key.[^18] Because the map step treats
records independently, the framework can shard the data across hundreds of machines and
run the maps in parallel; because the reduce step aggregates by key, the framework can
route all records with the same key to the same reducer.

```mermaid
flowchart LR
    In[(Huge input,<br/>sharded)] --> M1[map] --> Sh{{shuffle<br/>by key}}
    In --> M2[map] --> Sh
    In --> M3[map] --> Sh
    Sh --> R1[reduce] --> Out[(Result)]
    Sh --> R2[reduce] --> Out
    classDef f fill:#efe,stroke:#6a6,color:#000;
    class M1,M2,M3,R1,R2 f;
```

**Problem it solves and trade-offs.** The pattern's genius is that *you* write two small,
sequential functions — map and reduce — and the *framework* handles the hard distributed
concerns: partitioning the data, scheduling work, moving map outputs to the right
reducers (the **shuffle**), and re-running tasks that fail on a flaky machine. You get
massive parallelism and fault tolerance almost for free, provided your problem fits the
map-then-reduce shape. The costs are real: the rigid two-phase structure forces awkward
encodings for computations that are naturally iterative (many machine-learning
algorithms) or that need many stages, and the shuffle — moving data across the network
between phases — is often the dominant expense.[^18] Later engines generalize the idea into
arbitrary dataflow graphs of transformations to reduce that cost, but the core insight is
the same: *describe the dataflow, let the platform distribute it.*[^19]

## 7.5 Connecting Clients with Servers

The previous patterns mostly organize a single program. The next family organizes systems
that span **multiple machines**, where the fundamental questions become who initiates
contact, who holds the shared state, and how parties find one another across a network.

### 7.5.1 The Client-Server Pattern

**Problem it solves.** Many users, on many machines, need shared access to common data or
computation — a shared calendar, a bank ledger, a search index. You cannot put a copy on
every device and hope they agree. The **client-server** pattern designates one role, the
**server**, as the keeper of the shared resource, and another role, the **client**, as
the many requesters that ask the server to do work on their behalf.[^2] Clients initiate;
the server responds.

**Structure and participants.** The **server** owns the authoritative resource and waits
for requests, handling each according to a published **protocol** (the request/response
contract). The **client** knows the protocol and the server's address, sends requests,
and consumes responses; clients generally do not talk to each other. The protocol is the
interface that lets the two sides evolve independently, just as a layer's interface
does in §7.1.

```mermaid
flowchart TD
    C1[Client A]
    C2[Client B]
    C3[Client C]
    S["Server<br/>owns shared resource<br/>serves requests via protocol"]
    C1 -->|request| S
    C2 -->|request| S
    C3 -->|request| S
    S -->|response| C1
    S -->|response| C2
    S -->|response| C3
    classDef c fill:#eef,stroke:#66a,color:#000;
    class C1,C2,C3 c;
```

**A real example.** The web is client-server at planet scale: your browser (client) sends
HTTP requests to web servers that own the pages and data. A database server serving many
application instances, an email server, a game server — all follow the same shape.
**Trade-offs:** you gain a single authoritative source of truth and centralized control
of security and consistency, but the server is a **bottleneck and single point of
failure**, which is why real systems replicate and load-balance servers. The pattern also
raises the question of *how thick* the client should be — a thin client (just a display)
keeps logic central and easy to update but demands constant connectivity; a thick client
works offline and offloads the server but is harder to keep consistent and to upgrade.

### 7.5.2 Deploying Test Servers

A practical consequence of client-server structure is that you can *substitute the
server*. Because the client depends only on the **protocol**, not on any particular
server implementation, you can point the client at a stand-in server during development
and testing — a **test server** (often called a *mock*, *stub*, or *fake*).

**Why this matters.** Testing a client against the real production server is slow,
flaky, and dangerous: the real server may be unavailable, may hold irreplaceable data you
do not want to mutate, or may be a paid third-party API. A test server implements just
enough of the protocol to exercise the client's behavior — you can program it to return
specific responses, simulate errors and timeouts, and record what the client sent. This
lets you test client behavior that is nearly impossible to trigger against the real
thing, such as "what does the UI do when the server returns a 500?" A short stub built
from nothing but the standard library answers that question for the clinic client:

```generic
// a stub server programmed to always fail
function always_fail(request)
  respond with status 500 and body "boom"

function fetch_appointments(base_url)
  response <- http_get(base_url + "/appointments")
  if response failed or response.status >= 400 then
    return empty list   // fallback: empty schedule, not a crash
  end if
  return response.body

stub <- start server serving always_fail on a free port
if fetch_appointments(stub.url) != empty list then
  fail "client should fall back to an empty schedule on 500"
end if
stop stub
```

```go
package main

import (
	"io"
	"net/http"
	"net/http/httptest"
)

func alwaysFail(w http.ResponseWriter, _ *http.Request) { http.Error(w, "boom", 500) }
func fetchAppointments(baseURL string) []byte {
	resp, err := http.Get(baseURL + "/appointments")
	if err != nil || resp.StatusCode >= 400 {
		return nil // fallback: empty schedule, not a crash
	}
	body, _ := io.ReadAll(resp.Body)
	return body
}

func main() {
	stub := httptest.NewServer(http.HandlerFunc(alwaysFail))
	defer stub.Close()
	if len(fetchAppointments(stub.URL)) != 0 {
		panic("client should fall back to an empty schedule on 500")
	}
}
```

```java
import com.sun.net.httpserver.HttpServer;

byte[] fetchAppointments(String baseUrl) {
  try (var in = URI.create(baseUrl + "/appointments").toURL().openStream()) {
    return in.readAllBytes();
  } catch (IOException e) {
    return new byte[0];                  // fallback: empty schedule, not a crash
  }
}

void main() throws Exception {
  var stub = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
  stub.createContext("/", exchange -> exchange.sendResponseHeaders(500, -1));
  stub.start();                          // serves requests on a background thread

  var base = "http://127.0.0.1:" + stub.getAddress().getPort();
  assert fetchAppointments(base).length == 0;
  stub.stop(0);
}
```

```javascript
const assert = require("node:assert");
const http = require("node:http");

async function fetchAppointments(baseUrl) {
  const resp = await fetch(baseUrl + "/appointments");
  if (!resp.ok) return [];               // fallback: empty schedule, not a crash
  return Buffer.from(await resp.arrayBuffer());
}

const stub = http.createServer((req, res) => res.writeHead(500).end());
stub.listen(0, "127.0.0.1", async () => {
  const base = `http://127.0.0.1:${stub.address().port}`;
  assert.deepStrictEqual(await fetchAppointments(base), []);
  stub.close();
});
```

```python
import http.server, threading, urllib.error, urllib.request
# stub server, client, and failing-path check: about twenty lines of stdlib

class AlwaysFail(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_error(500)
  def log_message(self, *_):           # keep test output clean
    pass

def fetch_appointments(base_url):
  try:
    with urllib.request.urlopen(base_url + "/appointments") as resp:
      return resp.read()
  except urllib.error.HTTPError:
    return []                        # fallback: empty schedule, not a crash

stub = http.server.HTTPServer(("127.0.0.1", 0), AlwaysFail)
threading.Thread(target=stub.serve_forever, daemon=True).start()

assert fetch_appointments(f"http://127.0.0.1:{stub.server_port}") == []
stub.shutdown()
```

```ruby
require "net/http"
require "socket"

stub = TCPServer.new("127.0.0.1", 0)
Thread.new do
  loop do
    client = stub.accept                 # a stub programmed to always fail
    client.gets("\r\n\r\n")              # consume the request head
    client.write "HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n"
    client.close
  end
end

def fetch_appointments(base_url)
  resp = Net::HTTP.get_response(URI(base_url + "/appointments"))
  resp.is_a?(Net::HTTPSuccess) ? resp.body : []  # fallback: empty schedule
end

port = stub.addr[1]
raise unless fetch_appointments("http://127.0.0.1:#{port}") == []
stub.close
```

```typescript
import assert from "node:assert";
import http from "node:http";
import type { AddressInfo } from "node:net";

async function fetchAppointments(baseUrl: string): Promise<Buffer | never[]> {
  const resp = await fetch(baseUrl + "/appointments");
  if (!resp.ok) return [];               // fallback: empty schedule, not a crash
  return Buffer.from(await resp.arrayBuffer());
}

const stub = http.createServer((req, res) => res.writeHead(500).end());
stub.listen(0, "127.0.0.1", async () => {
  const { port } = stub.address() as AddressInfo;
  const base = `http://127.0.0.1:${port}`;
  assert.deepStrictEqual(await fetchAppointments(base), []);
  stub.close();
});
```

The substitution is the network-tier echo of the layering benefit in §7.1.2: *depend on
an interface, and you can swap the implementation.* The trade-off is that a test server
is only as faithful as you make it — tests can pass against a fake that behaves
differently from reality, so a smaller number of full **integration tests** against a
real server remain essential (Chapter 10). The same substitution idea, scaled to
production, powers the blue-green and canary deployment strategies of Chapter 14.

### 7.5.3 The Broker Pattern

Plain client-server assumes the client knows *which* server to call and *where* it lives.
That assumption breaks down when there are many servers, when they come and go, or when
you want clients and servers to be ignorant of each other's location and identity. The
**broker** pattern inserts an intermediary — a **broker** — between clients and servers to
decouple them.[^1]

**Problem it solves.** As a system grows into many services, hard-wiring every caller to
every callee's address creates a brittle web of point-to-point dependencies: move or
rename a service and every caller breaks. A broker centralizes the connective tissue.
Clients send requests to the broker, which is responsible for *locating* an appropriate
server, *routing* the request to it, and *returning* the result — so clients address the
broker, not the server, and servers can be added, moved, or replaced without any client
knowing.

```mermaid
flowchart TD
    C1[Client A]
    C2[Client B]
    B{"Broker<br/>locates, routes,<br/>load-balances"}
    S1[Server X]
    S2[Server Y]
    S3[Server Z]
    C1 -->|request| B
    C2 -->|request| B
    B -->|route| S1
    B -->|route| S2
    B -->|route| S3
    classDef c fill:#eef,stroke:#66a,color:#000;
    classDef s fill:#efe,stroke:#6a6,color:#000;
    class C1,C2 c;
    class S1,S2,S3 s;
```

**Participants and examples.** The **broker** registers available servers, resolves each
request to a capable server, and may add load-balancing, retries, and monitoring. The
**client** and **server** are relieved of finding each other. Message brokers (the engine
behind publish-subscribe at scale, §7.2.2), API gateways, service meshes, and the classic
CORBA object request broker are all instances.[^1] **Trade-offs:** you gain **location
transparency**, dynamic membership, and a natural home for cross-cutting concerns like
load-balancing and observability. You pay in **latency** (an extra hop), in **complexity**
(the broker itself must be built, deployed, and scaled), and in **risk concentration** —
the broker can become the very single point of failure it was meant to help you avoid, so
in practice it too must be made redundant.

### 7.5.4 RESTful APIs

Client-server tells you *who talks to whom*; it does not tell you what the conversation
looks like. The dominant answer on today's web is **REST** (Representational State
Transfer) — less a new pattern than a set of conventions that make the client-server
pattern scale across the internet.[^20] An API that follows them is called **RESTful**.

**Problem it solves.** If every server invents its own vocabulary of operations
(`getPatient`, `fetch_appt`, `makeBookingV2`…), every client must learn every server's
private language, and generic infrastructure — caches, proxies, browsers, load balancers —
can help with none of it. REST standardizes the conversation so that *any* client can talk
to *any* server using the same small grammar.

**Structure.** Four conventions do the work:

- **Resources, named by URIs.** Everything interesting is a **resource** with a stable
  name: `/patients/143`, `/patients/143/appointments`, `/appointments/987`. Nouns, not
  verbs — the URI names a *thing*, not an *action*.
- **A fixed set of verbs.** Instead of unlimited custom operations, HTTP's methods act on
  resources. By common convention **GET** reads (safely, with no side effects), **POST** often
  creates, **PUT/PATCH** update, and **DELETE** removes.[^21] The clinic app's "mark patient
  arrived" becomes
  `PATCH /appointments/987` with body `{"status": "arrived"}` — no bespoke
  `markArrived` endpoint to document or learn.
- **Representations.** The client never touches the server's internal objects; it
  exchanges **representations** of them — today almost always JSON. The server's database
  schema can change freely as long as the representation stays stable (an interface, in
  Chapter 6's sense, at network scale).
- **Statelessness.** Each request carries everything the server needs (identity,
  parameters); the server keeps **no per-client session state** between requests.[^20] That is
  what lets any of the broker's servers (§7.5.3) answer any request — the foundation of
  horizontal scaling.

**Example.** A slice of the clinic scheduler's API:

| Request | Meaning |
|---------|---------|
| `GET /patients/143/appointments` | List patient 143's appointments |
| `POST /patients/143/appointments` | Book a new appointment for patient 143 |
| `GET /appointments/987` | Fetch one appointment's representation |
| `PATCH /appointments/987` | Update it (e.g., `{"status": "arrived"}`) |
| `DELETE /appointments/987` | Cancel it |

**POST, PUT, or PATCH?** The three writing verbs are the ones students confuse, and the choice
turns on two questions. First, *who names the new resource?* Reach for **POST** when the
*server* assigns the URL: `POST /patients/143/appointments` creates a fresh `/appointments/987`,
and posting again makes a *second* appointment — POST is not **idempotent**. Reach for **PUT**
when the *client* already knows the URL and wants to create or wholly *replace* what lives
there, sending the complete representation; repeating the same `PUT /appointments/987` leaves
the resource in the same state, so PUT *is* idempotent. Second, *full replacement or a partial
change?* Reach for **PATCH** to alter part of an existing resource, sending only the fields
that change — `PATCH /appointments/987` with `{"status": "arrived"}` touches nothing else. The
one-line version: **POST** creates under a server-chosen name, **PUT** replaces in full, and
**PATCH** changes in part.

> **Pitfall.** Idempotency is not a nicety — the network will retry. If a client times out and
> resends, an idempotent `PUT` or `DELETE` is harmless, but a resent `POST` can double-book the
> appointment. Design writes so that the safely-repeatable verb is used wherever you can, and
> protect the ones that cannot be (e.g., with an idempotency key) rather than assuming each
> request arrives exactly once.

**Trade-offs.** You gain **uniformity** (one grammar for every service; tooling, caching,
and testing all get cheaper), **evolvability** (representations decouple clients from
server internals), and effortless fit with the web's infrastructure. You pay when the
domain is not noun-shaped — long-running operations, batch actions, and "verbs with no
natural resource" (send reminder? merge records?) force modeling contortions — and
statelessness pushes real state you *do* need (sessions, carts) into tokens or the shared
data layer (§7.2.1). When a client needs many resources at once, REST's one-resource-per-request
grain can also mean chatty interfaces.

> **Principle.** REST is the interface discipline of Chapter 6 applied across a network:
> stable names, a small uniform contract, and hidden internals. Every real API still needs
> documentation — schemas, authorization rules, error formats — but if every endpoint
> requires its own bespoke interaction model that consistent resource-and-HTTP semantics
> cannot explain, the API is gaining little from REST's uniform interface.

One more pair of names to recognize: **service-oriented architecture (SOA)** and its
modern descendant, **microservices**, describe systems built as fleets of small services
calling one another — the services-calling-services lineage that client-server, broker,
and REST together make workable at scale.[^22]

## 7.6 Families and Product Lines

Everything so far treats architecture as the design of *one* system. But organizations
rarely build one system in isolation; they build a *family* of related systems — the same
product for different platforms, tiers, or customers. A phone maker ships dozens of
handset models running variations of one software base. A car company runs related but
distinct control software across an entire fleet. Treating each as a from-scratch project
wastes the enormous overlap between them. **Software product-line engineering** means
building a family of related products from a shared set of assets in a
planned way, and it changes what "architecture" is for.[^23]

### 7.6.1 Commonalities and Variabilities

The core analytical move is to separate what all family members share from what
distinguishes them. A **commonality** is a feature, behavior, or component present in
*every* product of the family — every handset has a dialer, every edition of the app
authenticates users. A **variability** is a point where products *differ* — one edition
has video calling and another does not; one region requires a different tax calculation.

**Why the distinction matters.** Commonalities are built *once* and reused
without change across the family, so effort spent making them solid is amortized over
every product. Variabilities are the points you must design to *vary*, so each one needs
an explicit mechanism — a configuration flag, a plug-in slot, a swappable module, a
compile-time option — that lets a given product select its variant without modifying
shared code. The design work of a product line is largely the work of **enumerating the
variabilities and choosing a variation mechanism for each**. A **feature model** is the
common tool for recording this: it captures which features are mandatory, which are
optional, and which are mutually exclusive, so that each valid product is a permitted
selection of features.[^24]

> **Pitfall.** Guessing wrong about which axis will vary is expensive. If you hard-code
> something that later must differ across products, retrofitting variability into shared
> code is painful; if you build elaborate variation machinery for an axis that never
> varies, you paid for flexibility you never use. Product-line design lives or dies on
> predicting the right variabilities — which is why it rewards domains you understand
> deeply.

### 7.6.2 Software Architecture and Product Lines

A product line needs a special kind of architecture: a **reference architecture** (or
*platform*) that is shared by every product in the family and that makes the planned
variabilities easy to exercise. This raises the stakes on the patterns earlier in the
chapter. Every variation point is, in the end, an *interface behind which alternatives
plug in* — and the patterns you have learned are the machinery for building such
interfaces:

- **Layering** lets you vary one layer (say, the platform-specific infrastructure) across
  products while the layers above stay identical.
- The **observer** and **broker** patterns let a product add or swap behavior by
  registering different components, without editing the shared core.
- **Plug-in** structures — a stable core that discovers and loads optional modules — are
  the workhorse variation mechanism, and they are just the open/closed discipline of the
  observer pattern applied at the scale of whole features.

```mermaid
flowchart LR
    Core["Shared platform /<br/>reference architecture<br/>(all commonalities)"]
    VP1{{"Variation point:<br/>payment"}}
    VP2{{"Variation point:<br/>region rules"}}
    VP3{{"Variation point:<br/>video calling"}}
    Core --- VP1
    Core --- VP2
    Core --- VP3
    VP1 --> A1[Card plug-in]
    VP1 --> A2[Wallet plug-in]
    VP2 --> B1[US rules]
    VP2 --> B2[EU rules]
    VP3 --> C1[Enabled]
    VP3 --> C2[Omitted]
    classDef core fill:#eef,stroke:#66a,color:#000;
    class Core core;
```

The organizational consequence is a split between two activities: **domain engineering**
builds the reusable platform and its variation points, and **application engineering**
assembles a specific product by selecting variants and adding only what is unique to it.[^25]
Getting this split right is what turns "we copy-pasted last year's product and hacked on
it" into a genuine, maintainable family.

### 7.6.3 Economics of Product-Line Engineering

Product lines are an *economic* bet, and you should be honest about the
arithmetic. Building a reusable platform with well-designed variation points costs
**more up front** than building a single product — you are engineering for change that
has not happened yet.[^25] That investment pays back only when you build *enough* products
from the platform that the per-product savings exceed the extra platform cost.

```mermaid
flowchart LR
    subgraph few [Few products]
      direction TB
      a["Platform cost is<br/>never recovered →<br/>product line loses"]
    end
    subgraph many [Many products]
      direction TB
      b["Per-product savings<br/>exceed platform cost →<br/>product line wins"]
    end
```

Until you build enough products from the platform to reach break-even, you would have
been better off building each system directly. The savings, when they come, are not only in initial construction but in
**maintenance and quality**: fix a bug in a commonality once and every product inherits
the fix; a feature hardened in one product is available to all. The risks mirror the
rewards — an over-engineered platform, a mis-predicted variability (§7.6.1), or a domain
too unstable to have durable commonalities can leave you paying the up-front cost without
collecting the return. The engineering judgment is therefore the same one that governs
every pattern in this chapter: *invest in flexibility exactly where change is likely, and
not one place more.*

## 7.7 Conclusion

Architectural patterns are the vocabulary of large-scale design. Each is a named answer
to a recurring structural question, and each answer is a trade-off — you adopt it to buy
a quality you need and you pay for it in some other coin. The through-line of the whole
chapter is the Chapter 1 principle restated at every scale: *structure the system so that
the changes you expect are cheap, and do not pay for flexibility you will not use.*
Layering makes it cheap to swap an implementation behind an interface. The observer makes
it cheap to add a new reaction to a change. MVC makes it cheap to evolve appearance,
interaction, and rules on separate schedules. Dataflow makes it cheap to reorder and
parallelize transformations. Client-server, broker, and product lines push those same
ideas across machines and across whole families of products.

The table below is your quick-reference map. Use it the way an engineer uses any catalog:
not to pick the fanciest option, but to reach quickly for the *smallest* pattern that
solves the problem in front of you and to state out loud what it will cost.

| Pattern | Problem it solves | Key trade-off |
| --- | --- | --- |
| **Layering** | Span a wide range of abstraction without tangling high- and low-level code | Isolation vs. pass-through indirection and per-boundary cost |
| **Shared data** | Many components must operate on one authoritative body of data | Convenient central truth vs. coupling magnet and bottleneck |
| **Observer / pub-sub** | Parties must react to a change without the source knowing them | Loose coupling vs. hidden, hard-to-trace control flow |
| **Model-View-Controller** | Appearance, input, and rules must evolve and test independently | Testable separation vs. extra structure and boundary debates |
| **Pipes and filters** | Apply a sequence of reusable, recombinable transformations | Composability vs. lowest-common-denominator data format |
| **Dataflow network** | Transformations whose natural shape branches and merges | Expressive graph vs. coordination and deadlock complexity |
| **Unbounded streams** | Process never-ending data with near-real-time results | Continuous, incremental results vs. windowing, late data, backpressure |
| **MapReduce-style** | Batch-process data too large for one machine | Free parallelism/fault tolerance vs. rigid two-phase shape and shuffle cost |
| **Client-server** | Many users need shared access to one authoritative resource | Central control vs. bottleneck and single point of failure |
| **Broker** | Many services must find each other without hard-wired locations | Location transparency vs. extra hop, complexity, and risk concentration |
| **RESTful API** | Every server invents its own vocabulary, defeating generic clients and tooling | Uniform grammar and evolvability vs. contortions for non-resource-shaped operations |
| **Product line** | Build a family of related products from shared assets | Reuse and consistency vs. up-front platform cost and misprediction risk |

No system of any size uses just one pattern. A real application layers presentation over domain over
infrastructure (layering), renders through MVC (which runs on the observer), talks to a
database (shared data) across the network (client-server over a REST API, perhaps via a
broker), ingests
events as a stream (dataflow), and — if the company is lucky enough to sell many editions
— does all of this on a shared platform (product line). Learning the patterns individually
is how you learn to *combine* them, and combining them well is what architecture is.

---

### Sources

[^1]: Frank Buschmann, Regine Meunier, Hans Rohnert, Peter Sommerlad & Michael Stal, *Pattern-Oriented Software Architecture, Volume 1: A System of Patterns* (1996). [wiley.com](https://www.wiley.com/en-us/Pattern-Oriented+Software+Architecture,+Volume+1,+A+System+of+Patterns-p-9780471958697).

[^2]: Mary Shaw & David Garlan, *Software Architecture: Perspectives on an Emerging Discipline* (1996). [dl.acm.org](https://dl.acm.org/doi/book/10.5555/231003).

[^3]: Frank Buschmann, Regine Meunier, Hans Rohnert, Peter Sommerlad, and Michael Stal, *Pattern-Oriented Software Architecture, Volume 1: A System of Patterns* (Wiley, 1996) — which files recurring structures into three levels: architectural patterns, design patterns, and idioms. [wiley.com](https://www.wiley.com/en-us/Pattern+Oriented+Software+Architecture,+Volume+1,+A+System+of+Patterns-p-9780471958697).

[^4]: ISO/IEC, *ISO/IEC 7498-1:1994 — Open Systems Interconnection — Basic Reference Model* (1994). [iso.org](https://www.iso.org/standard/20269.html).

[^5]: Redux project, *Three Principles*, Redux documentation (accessed 2026). [redux.js.org](https://redux.js.org/understanding/thinking-in-redux/three-principles).

[^6]: Erich Gamma, Richard Helm, Ralph Johnson & John Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software* (1994). [informit.com](https://www.informit.com/store/design-patterns-elements-of-reusable-object-oriented-9780201633610).

[^7]: Microsoft, *Publisher-Subscriber Pattern*, Azure Architecture Center (accessed 2026). [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/architecture/patterns/publisher-subscriber).

[^8]: Trygve Reenskaug, *MVC: Xerox PARC 1978–79* (1979; the inventor's notes). [folk.uio.no](https://folk.uio.no/trygver/themes/mvc/mvc-index.html).

[^9]: Martin Fowler, *GUI Architectures* (2006). [martinfowler.com](https://martinfowler.com/eaaDev/uiArchs.html).

[^10]: Martin Fowler, *Humble Object* (2020; after Michael Feathers' "Humble Dialog Box" and Gerard Meszaros' *xUnit Test Patterns*). [martinfowler.com](https://martinfowler.com/bliki/HumbleObject.html).

[^11]: Django Software Foundation, *FAQ: General*, Django documentation (accessed 2026). [docs.djangoproject.com](https://docs.djangoproject.com/en/stable/faq/general/).

[^12]: Rails team, *Getting Started with Rails*, Rails Guides (accessed 2026). [guides.rubyonrails.org](https://guides.rubyonrails.org/getting_started.html).

[^13]: Instagram Engineering, *Static Analysis at Scale: An Instagram Story* (2019). [instagram-engineering.com](https://instagram-engineering.com/static-analysis-at-scale-an-instagram-story-8f498ab71a0c).

[^14]: Shopify Engineering, *Deconstructing the Monolith* (2019). [shopify.engineering](https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity).

[^15]: Airbnb Engineering, *Rearchitecting Airbnb's Frontend* (2018). [medium.com/airbnb-engineering](https://medium.com/airbnb-engineering/rearchitecting-airbnbs-frontend-5e213efc24d2).

[^16]: Tyler Akidau, *Streaming 101: The World Beyond Batch* (2015). [oreilly.com](https://www.oreilly.com/radar/the-world-beyond-batch-streaming-101/).

[^17]: Jonas Bonér, Dave Farley, Roland Kuhn & Martin Thompson, *The Reactive Manifesto* (2014). [reactivemanifesto.org](https://www.reactivemanifesto.org/).

[^18]: Jeffrey Dean & Sanjay Ghemawat, *MapReduce: Simplified Data Processing on Large Clusters*, OSDI (2004). [research.google](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/).

[^19]: Matei Zaharia et al., *Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing*, NSDI (2012). [usenix.org](https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia).

[^20]: Roy T. Fielding, *Architectural Styles and the Design of Network-based Software Architectures*, ch. 5 (2000). [ics.uci.edu](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm).

[^21]: R. Fielding, M. Nottingham & J. Reschke (eds.), *RFC 9110: HTTP Semantics*, IETF (2022). [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc9110.html).

[^22]: James Lewis & Martin Fowler, *Microservices* (2014). [martinfowler.com](https://martinfowler.com/articles/microservices.html).

[^23]: Carnegie Mellon Software Engineering Institute, *Software Product Lines Collection* (accessed 2026). [sei.cmu.edu](https://www.sei.cmu.edu/library/software-product-lines-collection/).

[^24]: Kyo C. Kang, Sholom G. Cohen, James A. Hess, William E. Novak & A. Spencer Peterson, *Feature-Oriented Domain Analysis (FODA) Feasibility Study*, CMU/SEI-90-TR-021 (1990). [sei.cmu.edu](https://www.sei.cmu.edu/library/feature-oriented-domain-analysis-foda-feasibility-study/).

[^25]: Klaus Pohl, Günter Böckle & Frank van der Linden, *Software Product Line Engineering: Foundations, Principles and Techniques* (2005). [link.springer.com](https://link.springer.com/book/10.1007/3-540-28901-1).

---

- **Key takeaways** are summarized above in §7.7.
- Continue to the [Exercises](exercises.md).
- Go deeper with the [Open Resources](resources.md) for this chapter.
