<!--
  Print-edition front matter for the GENERIC (pseudocode) hardcover, 7x10.
  This is print-only: no links, no download/citation/repository sections, no
  "read online" or language-tab references. It replaces the web landing page
  (README) at the front of the print PDF.

  NOTE: book-build.sh extracts ONLY the introduction section below (the Preface).
  The title page and the copyright page are typeset separately from
  latex/title.tex, so they intentionally do NOT live here — keeping a second
  copy here only risks drift and a duplicate copyright page. Keep this Preface
  in sync with the book's content, written for a reader holding the book, not a
  browser.
-->

<!-- ========================== INTRODUCTION =========================== -->
<section class="introduction">

# Preface

Most software that matters is built by teams, under requirements that keep changing, with
defects that are inevitable, at a scale no single person can hold in their head. A first
programming course teaches you to make one function work. This book is about the harder
thing that comes next: building and evolving a whole system, alongside other people, over
years. That discipline is **software engineering**, and it rewards durable principles far
more than fluency in any one programming language.

Four facts about software shape everything in these pages:

1. **Software is complex**, so we manage that complexity with deliberate design and
   architecture.
2. **Requirements change**, so we work in short, iterative cycles that let us adapt instead
   of guessing everything up front.
3. **Defects are inevitable**, so we catch them early with reviews, static checking, and
   testing.
4. **Teams need coordination**, so we adopt processes that balance structure with the
   freedom to respond.

These four pressures recur in every chapter. Watch for them, and much of the field stops
looking like a grab-bag of tools and starts looking like a small set of responses to the
same handful of forces.

## How this book is organized

The chapters move through the life of a software project, in arcs. The first two set the
stage: what software engineering is, and what process a team uses to do it. The next three
turn a vague need into something you can build — eliciting, analyzing, and specifying
requirements as user stories and use cases. Two chapters on design and architecture show
how to structure a system so that likely changes stay cheap. Two on quality show how to
check and test that the system actually works. A chapter on security asks how a system
holds up under attack, from its own code to the open-source supply chain it depends on. A
chapter on metrics shows how to measure quality and progress honestly. A chapter on the
role of AI separates what genuinely changes when machines can draft code from what
stubbornly does not. A final chapter on delivery follows a change from a finished commit to
running safely in front of real users, and then into the long life of code as it becomes
legacy. An appendix carries a real team project alongside the concepts, so the ideas have
somewhere to land.

Each chapter builds on the ones before it, and each explains not only *what* to do but
*why* — because the "why" is what survives when the tools change.

## How to read it

Concepts come first in this book, and code comes second. Where an idea is clearest as a
running example, you will find it written as **pseudocode**: a plain, language-agnostic
sketch of the logic, free of any particular language's syntax. The intent is that the
example reads the same whether your daily language is Python, Java, Go, or something not yet
invented.

The pseudocode follows a small, consistent style. A routine opens with `function` and
returns a value with `return`. Decisions use `if ... then`, `else`, and `end if`; repetition
uses `for each ... in ...` or `while ... do`. An arrow pair, `<-`, means assignment: read
`total <- price * quantity` as "let *total* become *price* times *quantity*." Comparisons
use the ordinary symbols `=`, `<`, `>`, `<=`, `>=`. Anything after `//` on a line is a
comment. Names come from the problem — *patient*, *catalog*, *invoice* — not from any
implementation.

You can read the book straight through, or use the table of contents to jump to a specific
concern. Either way, the aim is the same: to leave you able to build software that other
people can trust, and that you can keep changing for longer than anyone expects.

## How this book was made

This book was written in collaboration with an AI assistant (Anthropic's Claude) under the
author's direction. The author set the scope, chapter progression, and course alignment;
supplied source material and corrections; fact-checked claims against the primary sources
cited throughout the book; and edited the prose. The author has reviewed, and stands behind,
every chapter.

Chapter 13 teaches that professional AI use means disclosing the assistance, verifying the
output, and owning the result. This note applies that standard to the book itself.

</section>
