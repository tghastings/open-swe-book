#!/usr/bin/env python3
"""Mechanical census of a code repository — feeds the `repo-scorecard` skill.

Detects what a repo *has* (CI, tests, linters, scanners, containers, docs, ADRs,
commit hygiene) so the grading agent argues about meaning instead of guessing at
facts. Read-only, offline, no dependencies beyond the stdlib and `git`.

This scores NOTHING and grades NOTHING. Absence of a signal is not a defect —
a repo may hold its tests somewhere this tool does not look. Every finding built
on this output must still be confirmed by reading the repo.

Usage:
    python3 repo-census.py                 # census the current directory
    python3 repo-census.py /path/to/repo
    python3 repo-census.py --json
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import subprocess
import sys

SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", ".venv", "venv", "env", "__pycache__",
    "dist", "build", "target", "out", ".next", ".nuxt", "vendor", ".tox",
    ".mypy_cache", ".pytest_cache", ".ruff_cache", "coverage", "htmlcov",
    ".gradle", "obj", ".idea", ".vscode", "Pods", ".terraform", ".cache",
    "site-packages", ".bundle", ".dart_tool", "Carthage",
}

LANGUAGES = {
    ".py": "Python", ".js": "JavaScript", ".jsx": "JavaScript", ".ts": "TypeScript",
    ".tsx": "TypeScript", ".go": "Go", ".java": "Java", ".kt": "Kotlin",
    ".rb": "Ruby", ".rs": "Rust", ".cs": "C#", ".php": "PHP", ".swift": "Swift",
    ".c": "C", ".h": "C", ".cpp": "C++", ".hpp": "C++", ".cc": "C++",
    ".scala": "Scala", ".ex": "Elixir", ".exs": "Elixir", ".dart": "Dart",
    ".sh": "Shell", ".sql": "SQL", ".html": "HTML", ".css": "CSS", ".scss": "CSS",
}

# signal name -> exact paths / suffixes / directory names to look for.
# Grouped by the rubric area each one informs.
SIGNALS: dict[str, dict[str, list[str]]] = {
    "process": {
        "issue templates": [".github/ISSUE_TEMPLATE"],
        "PR template": [".github/pull_request_template.md", ".github/PULL_REQUEST_TEMPLATE.md"],
        "CODEOWNERS": ["CODEOWNERS", ".github/CODEOWNERS", "docs/CODEOWNERS"],
        "contributing guide": ["CONTRIBUTING.md", "docs/CONTRIBUTING.md"],
    },
    "requirements": {
        "requirements/specs dir": ["docs/requirements", "requirements", "specs", "docs/specs"],
        "user stories / backlog": ["BACKLOG.md", "docs/backlog.md", "STORIES.md"],
        "BDD features": [".feature"],
    },
    "design": {
        "ADRs": ["docs/adr", "doc/adr", "docs/decisions", "architecture/decisions",
                 "docs/architecture/decisions", "adr"],
        "architecture doc": ["ARCHITECTURE.md", "docs/architecture.md", "docs/ARCHITECTURE.md",
                             "docs/design.md", "DESIGN.md"],
        "diagrams": ["docs/diagrams", "assets/diagrams", ".puml", ".drawio", ".mmd"],
    },
    "version_control": {
        ".gitignore": [".gitignore"],
        "gitattributes": [".gitattributes"],
        "commit hooks": [".pre-commit-config.yaml", ".husky", "lefthook.yml", ".commitlintrc",
                         "commitlint.config.js", ".gitmessage"],
    },
    "static_checking": {
        "linter config": [".eslintrc", ".eslintrc.js", ".eslintrc.json", "eslint.config.js",
                          ".flake8", ".pylintrc", "pylintrc", ".rubocop.yml",
                          ".golangci.yml", ".golangci.yaml", "clippy.toml",
                          "checkstyle.xml", ".swiftlint.yml", "biome.json"],
        "formatter config": [".prettierrc", ".prettierrc.json", ".prettierrc.js",
                             ".editorconfig", "rustfmt.toml", ".clang-format"],
        "type checking": ["mypy.ini", ".mypy.ini", "tsconfig.json", "pyrightconfig.json"],
        "ruff/black (pyproject)": ["pyproject.toml"],
    },
    "testing": {
        "test config": ["pytest.ini", "tox.ini", "jest.config.js", "jest.config.ts",
                        "vitest.config.ts", "vitest.config.js", "karma.conf.js",
                        "phpunit.xml", ".rspec", "nose.cfg"],
        "coverage config": [".coveragerc", "codecov.yml", ".codecov.yml", "coverage.xml"],
    },
    "security": {
        "dependabot": [".github/dependabot.yml", ".github/dependabot.yaml"],
        "renovate": ["renovate.json", ".renovaterc", ".github/renovate.json"],
        "SECURITY.md": ["SECURITY.md", ".github/SECURITY.md"],
        "secret scanning": [".gitleaks.toml", ".secrets.baseline", ".talismanrc"],
        "SBOM": ["sbom.json", "sbom.xml", "bom.json", "cyclonedx.json"],
        "scanner config": [".snyk", "trivy.yaml", ".semgrep.yml", ".semgrepignore"],
    },
    "delivery": {
        "Dockerfile": ["Dockerfile", "Containerfile"],
        "compose": ["docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"],
        "k8s manifests": ["k8s", "kubernetes", "charts", "helm"],
        "IaC": ["terraform", ".tf", "main.tf", "cloudformation", "pulumi"],
        "env template": [".env.example", ".env.sample", ".env.template"],
        "release automation": [".releaserc", "release-please-config.json", "goreleaser.yml",
                               ".goreleaser.yaml"],
    },
    "maintenance": {
        "README": ["README.md", "README.rst", "README.txt", "readme.md"],
        "LICENSE": ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"],
        "CHANGELOG": ["CHANGELOG.md", "CHANGES.md", "HISTORY.md"],
        "docs dir": ["docs", "doc"],
    },
    "ai_practice": {
        "agent instructions": ["AGENTS.md", "CLAUDE.md", "GEMINI.md", ".cursorrules",
                               ".github/copilot-instructions.md", ".windsurfrules"],
        "agent config dir": [".claude", ".cursor"],
    },
}

CI_FILES = {
    "GitHub Actions": [".github/workflows"],
    "GitLab CI": [".gitlab-ci.yml"],
    "CircleCI": [".circleci/config.yml"],
    "Jenkins": ["Jenkinsfile"],
    "Azure Pipelines": ["azure-pipelines.yml"],
    "Travis": [".travis.yml"],
    "Drone": [".drone.yml"],
    "Buildkite": [".buildkite"],
}

# Tools are usually *invoked* in CI rather than configured by a dotfile — a repo can
# run Brakeman and npm audit on every push with no security config file anywhere. Read
# the workflow bodies, or the file-based SIGNALS table reports a gap that isn't there.
CI_TOOL_PATTERNS = {
    "security": [
        "brakeman", "bundler-audit", "bundle audit", "npm audit", "yarn audit",
        "pnpm audit", "pip-audit", "safety check", "trivy", "snyk", "semgrep",
        "gitleaks", "trufflehog", "codeql", "dependency-check", "govulncheck",
        "cargo audit", "osv-scanner", "importmap audit", "grype", "syft",
        "dotnet list package --vulnerable", "composer audit",
    ],
    "static_checking": [
        "rubocop", "eslint", "ruff", "flake8", "pylint", "mypy", "pyright",
        "tsc ", "golangci-lint", "go vet", "gofmt", "clippy", "checkstyle",
        "spotbugs", "ktlint", "detekt", "phpstan", "psalm", "black ", "prettier",
        "dotnet format", "swiftlint", "biome",
    ],
    "testing": [
        "pytest", "rspec", "jest", "vitest", "go test", "cargo test", "mvn test",
        "gradle test", "dotnet test", "rails test", "minitest", "cucumber",
        "phpunit", "npm test", "yarn test", "karma", "playwright", "cypress",
    ],
}

# A step that cannot fail the build is a notification, not a gate (Ch. 14).
ADVISORY_PATTERNS = [
    (re.compile(r"continue-on-error:\s*true"), "continue-on-error: true"),
    (re.compile(r"\|\|\s*true\b"), "|| true"),
    (re.compile(r"\|\|\s*exit\s+0\b"), "|| exit 0"),
    (re.compile(r"^\s*fail:\s*false", re.M), "fail: false"),
    (re.compile(r"--exit-zero\b"), "--exit-zero"),
]

CI_FILE_HINTS = (".github/workflows/", ".gitlab-ci.yml", "jenkinsfile",
                 ".circleci/", "azure-pipelines.yml", ".travis.yml",
                 ".drone.yml", ".buildkite/")

DEP_MANIFESTS = {
    "requirements.txt": "pip", "pyproject.toml": "python", "Pipfile": "pipenv",
    "package.json": "npm", "go.mod": "go", "Cargo.toml": "cargo",
    "pom.xml": "maven", "build.gradle": "gradle", "build.gradle.kts": "gradle",
    "Gemfile": "bundler", "composer.json": "composer", "*.csproj": "nuget",
}
LOCKFILES = ["package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock",
             "Pipfile.lock", "go.sum", "Cargo.lock", "Gemfile.lock", "composer.lock",
             "requirements.lock", "uv.lock"]

TEST_PATTERNS = [
    re.compile(r"(^|/)tests?/"), re.compile(r"(^|/)__tests__/"), re.compile(r"(^|/)spec/"),
    re.compile(r"(^|/)test_[^/]+\.py$"), re.compile(r"_test\.py$"),
    re.compile(r"\.(test|spec)\.[jt]sx?$"), re.compile(r"_test\.go$"),
    re.compile(r"Test[s]?\.java$"), re.compile(r"_spec\.rb$"),
    re.compile(r"Tests?\.cs$"), re.compile(r"_test\.rs$"), re.compile(r"\.feature$"),
]

# High-confidence only. A noisy secret scanner trains people to ignore it.
SECRET_PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
    (re.compile(r"-----BEGIN (RSA |OPENSSH |EC |DSA |PGP )?PRIVATE KEY-----"), "private key"),
    (re.compile(r"ghp_[A-Za-z0-9]{36}"), "GitHub personal access token"),
    (re.compile(r"sk-[A-Za-z0-9]{32,}"), "API secret key"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
]
SECRET_SCAN_MAX_BYTES = 400_000


def run_git(repo: pathlib.Path, *args: str) -> str | None:
    try:
        r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                           text=True, timeout=25)
        return r.stdout.strip() if r.returncode == 0 else None
    except (subprocess.SubprocessError, OSError):
        return None


def git_stats(repo: pathlib.Path) -> dict:
    if run_git(repo, "rev-parse", "--is-inside-work-tree") != "true":
        return {"is_repo": False}

    out = {"is_repo": True}
    out["branch"] = run_git(repo, "rev-parse", "--abbrev-ref", "HEAD") or "?"
    total = run_git(repo, "rev-list", "--count", "HEAD")
    out["commits"] = int(total) if total and total.isdigit() else 0

    log = run_git(repo, "log", "--no-merges", "--format=%an%x00%ad%x00%s",
                  "--date=short", "-n", "2000") or ""
    subjects, authors, dates = [], collections.Counter(), collections.Counter()
    for line in log.split("\n"):
        if line.count("\x00") != 2:
            continue
        author, date, subject = line.split("\x00")
        authors[author] += 1
        dates[date] += 1
        subjects.append(subject)

    out["authors"] = len(authors)
    out["top_authors"] = authors.most_common(5)
    out["active_days"] = len(dates)
    out["sampled"] = len(subjects)

    if subjects:
        conv = re.compile(
            r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
            r"(\([^)]+\))?!?: .+")
        out["conventional_pct"] = round(
            100 * sum(1 for s in subjects if conv.match(s)) / len(subjects))
        out["short_msg_pct"] = round(
            100 * sum(1 for s in subjects if len(s) < 15) / len(subjects))
        # A repo whose history lands in one or two sittings did not practice
        # incremental integration, whatever the commit count says.
        busiest = dates.most_common(1)[0][1] if dates else 0
        out["busiest_day_pct"] = round(100 * busiest / len(subjects))
    if dates:
        out["first_commit"], out["last_commit"] = min(dates), max(dates)

    merges = run_git(repo, "rev-list", "--count", "--merges", "HEAD")
    out["merge_commits"] = int(merges) if merges and merges.isdigit() else 0
    branches = run_git(repo, "branch", "-a", "--format=%(refname:short)") or ""
    out["branches"] = len([b for b in branches.split("\n") if b.strip()])
    tags = run_git(repo, "tag") or ""
    out["tags"] = len([t for t in tags.split("\n") if t.strip()])
    return out


def tracked_files(repo: pathlib.Path) -> list[pathlib.Path] | None:
    """Prefer git's index: it respects .gitignore for free, so build output
    (dist/, book-output/, coverage HTML) never inflates the counts. A repo is
    graded on what it commits, not on what it happens to have built locally."""
    out = run_git(repo, "ls-files", "-z")
    if out is None:
        return None
    paths = [repo / p for p in out.split("\0") if p]
    return [p for p in paths
            if p.is_file() and not any(part in SKIP_DIRS for part in p.parts)]


def walk(repo: pathlib.Path) -> list[pathlib.Path]:
    git_files = tracked_files(repo)
    if git_files is not None:
        return git_files
    files, stack, budget = [], [repo], 60_000
    while stack and len(files) < budget:
        d = stack.pop()
        try:
            for entry in d.iterdir():
                if entry.is_symlink():
                    continue
                if entry.is_dir():
                    if entry.name not in SKIP_DIRS:
                        stack.append(entry)
                else:
                    files.append(entry)
        except (PermissionError, OSError):
            continue
    return files


def match_signal(rel_lower: set[str], targets: list[str]) -> list[str]:
    """Match a target as an exact path, a path component (file or directory at
    any depth), or — for bare extensions like '.feature' — a filename suffix."""
    hits = []
    for t in targets:
        tl = t.lower()
        is_ext = tl.startswith(".") and "/" not in tl and "." not in tl[1:]
        for r in rel_lower:
            padded = "/" + r
            if (r == tl
                    or r.startswith(tl + "/")
                    or padded.endswith("/" + tl)
                    or ("/" + tl + "/") in padded
                    or (is_ext and r.endswith(tl))):
                hits.append(t)
                break
    return hits


def scan_secrets(files: list[pathlib.Path], repo: pathlib.Path) -> list[dict]:
    found = []
    for f in files:
        rel = str(f.relative_to(repo))
        low = rel.lower()
        name = f.name.lower()
        if name.startswith(".env") and not any(
                name.endswith(s) for s in (".example", ".sample", ".template")):
            found.append({"file": rel, "issue": "committed .env file"})
        if name.endswith((".pem", ".p12", ".pfx")) or name in ("id_rsa", "id_dsa", "id_ed25519"):
            found.append({"file": rel, "issue": "committed key material"})
        if low.endswith((".png", ".jpg", ".gif", ".pdf", ".zip", ".ico", ".woff",
                         ".woff2", ".mp4", ".svg", ".lock")):
            continue
        try:
            if f.stat().st_size > SECRET_SCAN_MAX_BYTES:
                continue
            text = f.read_text(encoding="utf-8", errors="ignore")
        except (OSError, ValueError):
            continue
        for pat, label in SECRET_PATTERNS:
            m = pat.search(text)
            if m:
                line = text.count("\n", 0, m.start()) + 1
                found.append({"file": f"{rel}:{line}", "issue": label})
                break
    return found


def scan_ci_bodies(files: list[pathlib.Path], repo: pathlib.Path) -> tuple[dict, list]:
    """Read CI definitions for invoked tools and for steps that cannot fail.

    Returns ({area: [tools]}, [advisory steps]). This is a text scan, so it finds
    what is named — it cannot know whether the step actually runs."""
    tools: dict[str, set[str]] = {k: set() for k in CI_TOOL_PATTERNS}
    advisory: list[dict] = []

    for f in files:
        rel = f.relative_to(repo).as_posix()
        low = rel.lower()
        if not any(h in low for h in CI_FILE_HINTS):
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lowered = text.lower()
        for area, names in CI_TOOL_PATTERNS.items():
            for name in names:
                if name in lowered:
                    tools[area].add(name.strip())
        for i, line in enumerate(text.split("\n"), 1):
            if line.lstrip().startswith("#"):
                continue
            for rx, label in ADVISORY_PATTERNS:
                if rx.search(line):
                    advisory.append({"file": f"{rel}:{i}", "pattern": label})
                    break

    return {k: sorted(v) for k, v in tools.items() if v}, advisory


def census(repo: pathlib.Path) -> dict:
    files = walk(repo)
    rels = {str(f.relative_to(repo)) for f in files}
    rel_lower = {r.lower() for r in rels}

    langs = collections.Counter()
    loc = collections.Counter()
    for f in files:
        lang = LANGUAGES.get(f.suffix.lower())
        if not lang:
            continue
        langs[lang] += 1
        try:
            if f.stat().st_size < 2_000_000:
                loc[lang] += sum(1 for _ in f.open("rb"))
        except OSError:
            pass

    test_files = sorted(r for r in rels
                        if any(p.search(r.replace("\\", "/")) for p in TEST_PATTERNS))
    src_count = sum(langs.values())

    found: dict[str, dict[str, list[str]]] = {}
    for area, sigs in SIGNALS.items():
        found[area] = {}
        for label, targets in sigs.items():
            hits = match_signal(rel_lower, targets)
            if hits:
                found[area][label] = hits

    ci = {name: match_signal(rel_lower, paths)
          for name, paths in CI_FILES.items()}
    ci = {k: v for k, v in ci.items() if v}
    workflows = sorted(r for r in rels if r.startswith(".github/workflows/")
                       and r.endswith((".yml", ".yaml")))

    manifests = sorted({v for k, v in DEP_MANIFESTS.items()
                        if k.lower() in rel_lower
                        or (k.startswith("*") and any(r.endswith(k[1:].lower())
                                                      for r in rel_lower))})
    locks = sorted(l for l in LOCKFILES if l.lower() in rel_lower)

    ci_tools, advisory = scan_ci_bodies(files, repo)

    return {
        "repo": str(repo.resolve()),
        "ci_tools": ci_tools,
        "advisory_steps": advisory,
        "files": len(files),
        "languages": langs.most_common(8),
        "loc": loc.most_common(8),
        "source_files": src_count,
        "test_files": len(test_files),
        "test_examples": test_files[:8],
        "test_ratio": round(len(test_files) / src_count, 2) if src_count else 0.0,
        "ci": ci,
        "workflows": workflows,
        "dep_managers": manifests,
        "lockfiles": locks,
        "signals": found,
        "secrets": scan_secrets(files, repo),
        "git": git_stats(repo),
    }


def report(c: dict) -> None:
    print(f"repo: {c['repo']}")
    print(f"files: {c['files']} · source files: {c['source_files']} · "
          f"test files: {c['test_files']} (ratio {c['test_ratio']})")
    if c["languages"]:
        print("languages: " + ", ".join(f"{n} ({k})" for n, k in c["languages"]))

    g = c["git"]
    print("\n— version control —")
    if not g.get("is_repo"):
        print("  NOT a git repository")
    else:
        print(f"  commits: {g['commits']} · authors: {g['authors']} · "
              f"branches: {g['branches']} · tags: {g['tags']} · merges: {g['merge_commits']}")
        if g.get("first_commit"):
            print(f"  span: {g['first_commit']} → {g['last_commit']} "
                  f"over {g['active_days']} active day(s)")
        if "conventional_pct" in g:
            print(f"  conventional commits: {g['conventional_pct']}% · "
                  f"very short messages: {g['short_msg_pct']}% · "
                  f"busiest single day: {g['busiest_day_pct']}% of sampled commits")
        if g.get("top_authors"):
            print("  top authors: " + ", ".join(f"{a} ({n})" for a, n in g["top_authors"]))

    print("\n— automation —")
    print(f"  CI: {', '.join(c['ci']) if c['ci'] else 'NONE DETECTED'}")
    for w in c["workflows"]:
        print(f"    - {w}")
    print(f"  dependency managers: {', '.join(c['dep_managers']) or 'none detected'}")
    print(f"  lockfiles: {', '.join(c['lockfiles']) or 'NONE DETECTED'}")

    print("\n— signals by rubric area —")
    for area, sigs in c["signals"].items():
        label = area.replace("_", " ")
        parts = list(sigs)
        if area == "testing" and c["test_files"]:
            parts.insert(0, f"{c['test_files']} test file(s)")
        for tool in c.get("ci_tools", {}).get(area, []):
            parts.append(f"{tool} (in CI)")
        print(f"  {label}: " + (", ".join(parts) if parts else "nothing matched"))

    if c.get("advisory_steps"):
        print("\n— CI steps that cannot fail the build —")
        for a in c["advisory_steps"][:12]:
            print(f"  ! {a['file']} — {a['pattern']}")
        print("  A check that cannot fail is a notification, not a gate.")

    if c["secrets"]:
        print("\n— possible secrets in the working tree (VERIFY BEFORE REPORTING) —")
        for s in c["secrets"][:15]:
            print(f"  ! {s['file']} — {s['issue']}")

    print("\n\"nothing matched\" means this tool's lookup tables found nothing — NOT that")
    print("the practice is absent. Tools get invoked in Makefiles, pre-commit hooks, and")
    print("scripts this scan never opens. Confirm by reading before claiming a gap.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=".", help="repo root (default: cwd)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    repo = pathlib.Path(args.path)
    if not repo.is_dir():
        print(f"not a directory: {repo}", file=sys.stderr)
        return 1

    c = census(repo)
    if args.json:
        print(json.dumps(c, indent=2))
    else:
        report(c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
