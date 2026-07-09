# Chapter 13 — Open Resources

Free, open-licensed, or freely accessible primary sources behind this chapter. Types: 📘 open
text · 🎓 course · 📄 primary source/paper · 🎥 video. Licenses vary and are noted where known.
AI moves fast — prefer primary studies over vendor blogs, and check dates.

## The o16g manifesto (used in §13.4)

- 📄 **o16g — the Outcome Engineering manifesto**, Cory Ondrejka —
  [o16g.com/manifesto](https://o16g.com/manifesto/). The 16 principles and the "it was
  never about the code" thesis. Read it in full and form your own view.
- 📄 Onebrief, **"Onebrief Hires Cory Ondrejka as Chief Technology Officer"** (2026) —
  [businesswire.com](https://www.businesswire.com/news/home/20260203520166/en/Onebrief-Hires-Cory-Ondrejka-as-Chief-Technology-Officer-to-Drive-Next-Gen-Command-Operating-System).
  Background on the manifesto's author.

## Productivity evidence (used in §13.1.4, §13.3)

- 📄 METR, **"Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer
  Productivity"** (2025) — [metr.org study](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
  · [arXiv 2507.09089](https://arxiv.org/abs/2507.09089). The randomized trial that found a
  ~19% slowdown and a large perception gap.
- 📄 **"The Impact of LLM-Assistants on Software Developer Productivity: A Systematic
  Review"** (2025) — [arXiv 2507.03156](https://arxiv.org/html/2507.03156v2).
- 📄 GitHub, **"Research: Quantifying GitHub Copilot's Impact on Developer Productivity
  and Happiness"** (2022) — [github.blog](https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/).
  The perceived-productivity survey.
- 📄 Peng et al., **"The Impact of AI on Developer Productivity: Evidence from GitHub
  Copilot"** (2023) — [arXiv 2302.06590](https://arxiv.org/abs/2302.06590). The vendor
  experiment behind the eye-catching "55.8% faster" number.
- 📄 Sundar Pichai's Alphabet Q3 2024 earnings-call remark that more than a quarter of new
  code at Google is AI-generated, then reviewed by engineers — reported by
  [Fortune](https://fortune.com/2024/10/30/googles-code-ai-sundar-pichai/).
- 📄 **DORA / State of DevOps** reports on AI's effect on delivery —
  [dora.dev](https://dora.dev/).

## Code quality & security (used in §13.3)

- 📄 GitClear, **"AI Copilot Code Quality: 2025 Research"** (rising code clones, falling
  refactoring) — [gitclear.com research](https://www.gitclear.com/ai_assistant_code_quality_2025_research).
- 📄 Perry et al., **"Do Users Write More Insecure Code with AI Assistants?"** (Stanford) —
  [arXiv 2211.03622](https://arxiv.org/abs/2211.03622). The "false sense of security" study.
- 📄 Pearce et al., **"Asleep at the Keyboard? Assessing the Security of GitHub Copilot's
  Code Contributions"** — [arXiv 2108.09293](https://arxiv.org/abs/2108.09293).
- 📄 Google Research, **"Resolving Code Review Comments with Machine Learning"** (2023) —
  [research.google](https://research.google/blog/resolving-code-review-comments-with-ml/).
  ML-suggested fixes for review comments at Google scale.

## AI in requirements, design, testing (used in §13.2)

- 📄 **"Generative AI for Requirements Engineering: A Systematic Literature Review"** —
  [arXiv 2409.06741](https://arxiv.org/pdf/2409.06741).
- 📄 **"Leveraging LLMs for User Stories in AI Systems (UStAI)"** (FSE 2025) —
  [arXiv 2504.00513](https://arxiv.org/pdf/2504.00513).
- 📄 Krishna et al., **"Using LLMs in Software Requirements Specifications: An Empirical
  Evaluation"** (2024) — [arXiv 2404.17842](https://arxiv.org/abs/2404.17842). LLM-drafted
  SRS quality vs. entry-level engineers, plus time/cost savings.
- 📄 Hong et al., **"MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework"**
  (2023) — [arXiv 2308.00352](https://arxiv.org/abs/2308.00352). Role specialization to
  reduce errors in multi-agent software generation.
- 📄 Li et al., **"Bridging Requirements and Architecture: Multi-Agent Orchestration with
  External Knowledge and Hierarchical Memory"** (2026) —
  [arXiv 2606.01385](https://arxiv.org/abs/2606.01385). Specialized agents that turn
  requirements into candidate architectures.
- 📄 Schäfer et al., **"An Empirical Evaluation of Using Large Language Models for
  Automated Unit Test Generation"** (2023) —
  [arXiv 2302.06527](https://arxiv.org/abs/2302.06527).
- 📄 **"Context Matters: Evaluating Context Strategies for Automated ADR Generation Using
  LLMs"** (architecture decisions) — [arXiv 2604.03826](https://arxiv.org/pdf/2604.03826).
- 📄 **SWE-bench** (resolve real GitHub issues) — [swebench.com](https://www.swebench.com/)
  · [arXiv 2310.06770](https://arxiv.org/abs/2310.06770); and **SWT-bench** (generate
  bug-reproducing tests) — [arXiv 2406.12952](https://arxiv.org/pdf/2406.12952).
- 📄 Aleithan et al., **"SWE-Bench+: Enhanced Coding Benchmark for LLMs"** (2024) —
  [arXiv 2410.06992](https://arxiv.org/abs/2410.06992). Solution leakage and weak test
  suites can inflate reported benchmark resolution rates.

## Agentic development in practice (used in §§13.5–13.7)

- 📄 GitHub, **Spec Kit** — an open toolkit for spec-driven development —
  [github.com/github/spec-kit](https://github.com/github/spec-kit); intro on the
  [GitHub Blog](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/).
  The constitution → specify → plan → tasks → implement pipeline.
- 📄 **`AGENTS.md`** — the open standard for agent instruction files —
  [agents.md](https://agents.md/). "A README for agents"; donated to the Linux Foundation's
  Agentic AI Foundation in December 2025.
- 📄 Anthropic, **"Manage Claude's memory"** (Claude Code docs) —
  [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory). How `CLAUDE.md`
  is loaded and what makes an instructions file effective.
- 📄 Addy Osmani, **"Loop Engineering"** (2026) —
  [addyo.substack.com](https://addyo.substack.com/p/loop-engineering); overview at
  [O'Reilly Radar](https://www.oreilly.com/radar/loop-engineering/). The four-layer stack,
  the five moves, the anti-patterns, and the four silent costs.
- 📄 Anthropic, **"Harness design for long-running application development"** (2026) —
  [anthropic.com/engineering](https://www.anthropic.com/engineering/harness-design-long-running-apps).
  The GAN-inspired planner / generator / evaluator architecture and why agents overrate
  their own output.
- 🎥 Steve Kaliski, **"How Stripe built 'minions'"** (*How I AI*, 2026) —
  [lennysnewsletter.com](https://www.lennysnewsletter.com/p/how-stripe-built-minionsai-coding);
  coverage at [InfoQ](https://www.infoq.com/news/2026/03/stripe-autonomous-coding-agents/).
  ~1,300 PRs/week from deterministic gates around a *Goose* fork.
- 📄 **`bdfinst/agentic-dev-team`** — Claude Code plugins for a spec-to-shipping workflow —
  [github.com/bdfinst/agentic-dev-team](https://github.com/bdfinst/agentic-dev-team). A
  working `/specs → /plan → /build → /pr` template with critic agents and TDD gates.

### Per-tool instruction guides (used in §13.6)

Each agent ships its own guide for how to phrase instructions — the *facts* port via
`AGENTS.md`, the *tone* does not. Read the guide for the tool you actually use.

- 📄 Anthropic, **"Best practices for Claude Code"** —
  [code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices)
  and **"Manage Claude's memory"** — [.../memory](https://code.claude.com/docs/en/memory).
  Source of the `IMPORTANT`/`YOU MUST` emphasis lever and the "prune ruthlessly" rule.
- 📄 OpenAI, **"Codex — Prompting"** —
  [developers.openai.com/codex/prompting](https://developers.openai.com/codex/prompting) —
  and **"Best practices"** — [.../learn/best-practices](https://developers.openai.com/codex/learn/best-practices).
  Verifiable, decomposed instructions; no capitalization advice.
- 📄 Cursor, **"Rules"** — [cursor.com/docs/rules](https://cursor.com/docs/rules).
  Glob-scoped `.mdc` rule files (and native `AGENTS.md` support).
- 📄 Google, **"Provide context with `GEMINI.md` files"** (Gemini CLI) —
  [geminicli.com/docs/cli/gemini-md](https://geminicli.com/docs/cli/gemini-md/).
- 📄 GitHub, **"Adding repository custom instructions for Copilot"** —
  [docs.github.com](https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot).
  The `.github/copilot-instructions.md` convention.

## Foundations & agentic engineering

- 📄 **Manifesto for Agile Software Development** — [agilemanifesto.org](https://agilemanifesto.org/)
  (the historical counterpoint the o16g manifesto positions itself against).
- 📄 **"Toward Agentic Software Engineering Beyond Code: Vision, Values, and Vocabulary"** —
  [arXiv 2510.19692](https://arxiv.org/pdf/2510.19692).
- 🎥 Talks and courses on AI-assisted development appear frequently; prefer
  university/primary sources and always check the publication date.

## License note

Linked resources remain under their own licenses; this page is CC BY-SA 4.0. The o16g
manifesto is quoted briefly for commentary and attributed to its author.
