#!/usr/bin/env python3
"""Install the book's SDLC principles into a project's agent-instructions file.

    python3 adopt-principles.py /path/to/project           # merge into AGENTS.md
    python3 adopt-principles.py . --file CLAUDE.md         # any other target
    python3 adopt-principles.py . --pointer CLAUDE.md      # + a stub redirecting there
    python3 adopt-principles.py . --dry-run                # show what would change
    python3 adopt-principles.py . --print                  # just print the block

Writes **AGENTS.md** by default — the open, tool-neutral convention (<https://agents.md/>)
that Claude Code, Cursor, Copilot, Codex, Gemini CLI, Aider and others read. Nothing here
is specific to one vendor: the principles are the book's, and the output is Markdown.

For a tool that only reads its own filename, either target it directly with `--file`, or
keep AGENTS.md as the single source and add a one-line stub with `--pointer` so the two
can never drift apart.

Works on a brand-new empty directory and on a mature codebase. The generated text is
tailored to whatever stack is detected — test command, lint tooling, and a hedged note on
practices the scan did not find.

**Never clobbers.** The block is delimited by HTML comment markers; re-running replaces
only what is between them and leaves the rest of the file untouched. Anything you write
outside the markers is yours and survives every regeneration.
"""

from __future__ import annotations

import argparse
import importlib.util
import pathlib
import re
import sys
import textwrap
from string import Template

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE_PATH = HERE / "principles-template.md"
BEGIN = "<!-- BEGIN swebook-principles"
END = "<!-- END swebook-principles"

# language -> (test command, lint note)
STACK = {
    "Python": ("`pytest`",
               "For Python: `ruff` (lint + format) and `mypy` for types."),
    "TypeScript": ("`npm test`",
                   "For TypeScript: ESLint, Prettier, and `tsc --noEmit` in CI — "
                   "`strict` on in `tsconfig.json`."),
    "JavaScript": ("`npm test`",
                   "For JavaScript: ESLint and Prettier; consider adding types via "
                   "JSDoc or TypeScript."),
    "Go": ("`go test ./...`",
           "For Go: `go vet` and `golangci-lint`; `gofmt` is not optional."),
    "Ruby": ("`bundle exec rspec`",
             "For Ruby: RuboCop for style and Brakeman for Rails security analysis."),
    "Java": ("`mvn test`",
             "For Java: Checkstyle or Spotless, plus SpotBugs/ErrorProne."),
    "Kotlin": ("`./gradlew test`", "For Kotlin: ktlint and detekt."),
    "Rust": ("`cargo test`",
             "For Rust: `cargo clippy -- -D warnings` and `cargo fmt --check`."),
    "C#": ("`dotnet test`",
           "For C#: `dotnet format` and the built-in Roslyn analyzers."),
    "PHP": ("`composer test`",
            "For PHP: PHP_CodeSniffer or PHP-CS-Fixer, plus PHPStan or Psalm."),
}
DEFAULT_STACK = ("your test runner", "")


def load_census():
    """Reuse repo-census.py's detection so both modes agree on the facts."""
    spec = importlib.util.spec_from_file_location("repo_census", HERE / "repo-census.py")
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    # Don't leave a __pycache__ inside the skill directory — it would land in
    # whichever repo the skill was copied into.
    prev, sys.dont_write_bytecode = sys.dont_write_bytecode, True
    try:
        spec.loader.exec_module(mod)
        return mod
    except Exception:  # detection is a nicety; never block adoption on it
        return None
    finally:
        sys.dont_write_bytecode = prev


def describe(project: pathlib.Path) -> tuple[str, str, str]:
    """-> (project_context, test_cmd, lint_note)"""
    census = load_census()
    if census is None:
        return ("**This project.** Stack not detected — fill in the test and lint "
                "commands below.", *DEFAULT_STACK)

    try:
        c = census.census(project)
    except Exception:
        return ("**This project.** Stack not detected — fill in the test and lint "
                "commands below.", *DEFAULT_STACK)

    langs = c.get("languages") or []
    primary = langs[0][0] if langs else None
    test_cmd, lint_note = STACK.get(primary, DEFAULT_STACK)

    is_new = c.get("source_files", 0) < 3 and not c.get("git", {}).get("is_repo")
    if is_new:
        return (
            "**This project.** A new or nearly empty repository. Set up version control, "
            "a test runner, and continuous integration *before* the first feature — every "
            "practice below assumes all three exist. Getting them in place on day one "
            "costs an hour; retrofitting them costs a sprint.",
            test_cmd, lint_note)

    bits = []
    if langs:
        bits.append(", ".join(f"{n} ({k} files)" for n, k in langs[:3]))
    if c.get("test_files"):
        bits.append(f"{c['test_files']} test files")
    else:
        bits.append("**no tests detected**")
    bits.append(f"CI: {', '.join(c['ci'])}" if c.get("ci") else "**no CI detected**")

    # Possible gaps — NEVER asserted as fact. A signal means "the lookup tables
    # matched nothing", not "the practice is absent": tools are commonly invoked
    # from CI steps, Makefiles, or pre-commit hooks that no file-name scan sees.
    # Stating an unverified absence here would be the hallucinated-absence failure
    # the skill exists to prevent, arriving through the tool instead of the model.
    sig = c.get("signals", {})
    ci_tools = c.get("ci_tools", {})
    unmatched = []
    if not sig.get("static_checking") and not ci_tools.get("static_checking"):
        unmatched.append("linter/formatter")
    if not sig.get("security") and not ci_tools.get("security"):
        unmatched.append("dependency or security scanning")
    if not sig.get("design", {}).get("ADRs"):
        unmatched.append("architecture decision records")
    if not c.get("lockfiles") and c.get("dep_managers"):
        unmatched.append("a dependency lockfile")

    ctx = "**This project.** " + " · ".join(bits) + "."
    if unmatched:
        ctx += ("\nNot detected by the setup scan: " + ", ".join(unmatched) +
                ". This scan reads file names and CI definitions only — **confirm before "
                "treating any of these as a gap**, since tools invoked from a Makefile, a "
                "pre-commit hook, or a script will not show up here. Whatever is genuinely "
                "missing becomes a backlog item; the practices below apply either way.")
    return ctx, test_cmd, lint_note


def wrap(text: str, width: int = 92) -> str:
    """Wrap each paragraph, matching the book's 90–100 column prose style."""
    return "\n".join(
        textwrap.fill(p, width=width, break_long_words=False, break_on_hyphens=False)
        for p in text.split("\n") if p.strip() != "" or True)


def build_block(project: pathlib.Path) -> str:
    ctx, test_cmd, lint_note = describe(project)
    tpl = Template(TEMPLATE_PATH.read_text(encoding="utf-8"))
    # Own line so the injected note never overflows the bullet it hangs off.
    note = ("\n  " + lint_note) if lint_note else ""
    return tpl.safe_substitute(project_context=wrap(ctx), test_cmd=test_cmd,
                               lint_note=note).rstrip() + "\n"


def merge(existing: str | None, block: str, project_name: str) -> tuple[str, str]:
    """-> (new_text, action). Replaces a managed block, else appends. Never clobbers."""
    if existing is None:
        header = (f"# {project_name}\n\n"
                  "Project instructions for AI coding agents.\n\n")
        return header + block, "created"

    if BEGIN in existing and END in existing:
        pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END) + r"[^\n>]*-->",
                             re.S)
        new, n = pattern.subn(block.rstrip(), existing, count=1)
        if n:
            return new, "updated in place"
        # markers present but malformed — fall through to append rather than guess

    sep = "" if existing.endswith("\n\n") else ("\n" if existing.endswith("\n") else "\n\n")
    return existing + sep + "\n" + block, "appended"


def write_pointer(path: pathlib.Path, target_name: str) -> None:
    """One line redirecting a tool-specific file at the real instructions.

    Keeps a single source of truth: two full copies drift, a pointer cannot."""
    line = (f"See [{target_name}]({target_name}) — this project keeps its agent "
            f"instructions there, in the tool-neutral AGENTS.md convention.\n")
    if path.exists():
        text = path.read_text(encoding="utf-8")
        if target_name in text:
            print(f"pointer already present: {path}")
            return
        path.write_text(text.rstrip() + "\n\n" + line, encoding="utf-8")
        print(f"pointer appended: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(line, encoding="utf-8")
    print(f"pointer written: {path}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=".", help="project root (default: cwd)")
    ap.add_argument("--file", default="AGENTS.md",
                    help="target filename (default: AGENTS.md — the tool-neutral "
                         "convention). Use e.g. CLAUDE.md, GEMINI.md, .cursorrules, "
                         "or .github/copilot-instructions.md for a specific tool.")
    ap.add_argument("--pointer", metavar="FILE",
                    help="also write a one-line stub at FILE redirecting to the target, "
                         "for tools that only read their own filename")
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    ap.add_argument("--print", dest="print_only", action="store_true",
                    help="print the block to stdout and exit")
    args = ap.parse_args()

    project = pathlib.Path(args.path).resolve()
    if not project.is_dir():
        print(f"not a directory: {project}", file=sys.stderr)
        return 1
    if not TEMPLATE_PATH.exists():
        print(f"missing template: {TEMPLATE_PATH}", file=sys.stderr)
        return 1

    block = build_block(project)
    if args.print_only:
        sys.stdout.write(block)
        return 0

    target = project / args.file
    existing = target.read_text(encoding="utf-8") if target.exists() else None
    new_text, action = merge(existing, block, project.name)

    if args.dry_run:
        print(f"would be {action}: {target}")
        if action == "appended":
            print("  (existing content is preserved; the block is added at the end)")
        print(f"  block: {len(block.splitlines())} lines")
        if args.pointer:
            print(f"  would also write pointer: {project / args.pointer}")
        return 0

    if existing == new_text:
        print(f"{target} already current — no change")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(new_text, encoding="utf-8")
        print(f"{action}: {target}")
        if action == "appended":
            print("  existing content preserved above the block")
        print("  re-run any time to refresh; edits outside the markers are kept")

    if args.pointer:
        write_pointer(project / args.pointer, args.file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
