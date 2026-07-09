# Chapter 11 — Open Resources

Free, open-licensed, or freely accessible materials that reinforce this chapter. Types: 📘 open
text · 🎓 course · 📄 primary source / standard · 🎥 video · 🛠 tool. Licenses vary and are noted
where known. Each entry notes its license or access terms; when in doubt, check the linked page.

## The OWASP Top 10 and hands-on practice

- 📄 **OWASP Top 10:2025** — [owasp.org/Top10](https://owasp.org/Top10/). The current edition of
  the industry's shared vulnerability vocabulary, with a page per category (root causes, examples,
  prevention, and mapped CWEs). Start here, then read the two or three categories most relevant to
  your project. *License: CC BY-SA 4.0.*
- 🛠 **OWASP Juice Shop** — [owasp.org/www-project-juice-shop](https://owasp.org/www-project-juice-shop/).
  A deliberately insecure single-page web app with 100+ challenges spanning the Top 10 and beyond;
  run it locally and try to break it. *License: MIT.*
- 🛠 **OWASP WebGoat** — [owasp.org/www-project-webgoat](https://owasp.org/www-project-webgoat/).
  A deliberately insecure Java app with *guided* lessons — a gentler on-ramp than Juice Shop for a
  first encounter with SQL injection and friends. *License: open source.*
- 🎓 **PortSwigger Web Security Academy** — [portswigger.net/web-security](https://portswigger.net/web-security).
  Free, hands-on labs and readings from the team behind Burp Suite; the closest thing to a canonical
  free web-security course. *Access: free; account only tracks progress.*
- 📄 **OWASP Cheat Sheet Series** — [cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/).
  ~150 concise, high-value guidance pages (authentication, cryptography, cloud, AI security). The
  reference you reach for while writing a control, not while studying. *License: CC BY-SA 4.0.*
- 📄 **OWASP Application Security Verification Standard (ASVS 5.0)** —
  [owasp.org/www-project-application-security-verification-standard](https://owasp.org/www-project-application-security-verification-standard/).
  A checklist-style standard for *testing* web-application security controls at three rigor levels.
  *License: CC BY-SA 4.0.*

## AI in security

- 🛠 **Strix — open-source autonomous AI pentest agents** —
  [github.com/usestrix/strix](https://github.com/usestrix/strix). Agents that run a target
  dynamically, find vulnerabilities, and validate them with proofs-of-concept; CLI + Docker,
  model-agnostic, with CI/pull-request integration. **Authorized testing only.** *License:
  Apache-2.0.*
- 📄 **Google Project Zero — "From Naptime to Big Sleep"** —
  [projectzero.google/2024/10/from-naptime-to-big-sleep.html](https://projectzero.google/2024/10/from-naptime-to-big-sleep.html).
  The primary write-up of the first real-world vulnerability found by an AI agent (in SQLite).
  *Access: free.*
- 📄 **GitHub — Copilot Autofix general availability** —
  [github.blog changelog](https://github.blog/changelog/2024-08-14-copilot-autofix-for-codeql-code-scanning-alerts-is-now-generally-available/).
  The announcement with the CodeQL-plus-LLM remediation numbers cited in §11.3. *Access: free.*

## The software supply chain

- 📄 **Andres Freund — "backdoor in upstream xz/liblzma"** (oss-security, 29 Mar 2024) —
  [openwall.com/lists/oss-security/2024/03/29/4](https://www.openwall.com/lists/oss-security/2024/03/29/4).
  The original disclosure of the xz-utils backdoor. Read the primary source before any blog summary.
  *Access: public mailing-list archive.*
- 📄 **Russ Cox — "Timeline of the xz open source attack"** —
  [research.swtch.com/xz-timeline](https://research.swtch.com/xz-timeline). A meticulously sourced
  timeline of the multi-year social-engineering campaign behind CVE-2024-3094. *Access: free.*
- 📄 **NVD — CVE-2021-44228 (Log4Shell)** —
  [nvd.nist.gov/vuln/detail/CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228) — and
  **CVE-2024-3094 (xz)** —
  [nvd.nist.gov/vuln/detail/CVE-2024-3094](https://nvd.nist.gov/vuln/detail/CVE-2024-3094). The
  authoritative records for the two case studies. *Access: U.S. government work, public domain.*
- 🛠 **OpenSSF Scorecard** — [scorecard.dev](https://scorecard.dev/). Automated checks (code review,
  branch protection, pinned dependencies, signed releases, and more) that score an open-source
  project's security posture — the tool the chapter's Day 0 controls build on. *License: Apache-2.0.*
- 🛠 **OWASP Dependency-Check** —
  [owasp.org/www-project-dependency-check](https://owasp.org/www-project-dependency-check/) — and
  **Dependency-Track** —
  [owasp.org/www-project-dependency-track](https://owasp.org/www-project-dependency-track/).
  Software-composition analysis: the first scans a build for known-vulnerable dependencies, the
  second continuously monitors an SBOM across a whole portfolio. *License: Apache-2.0.*
- 📄 **SLSA — Supply-chain Levels for Software Artifacts** — [slsa.dev](https://slsa.dev/). The
  framework of build/source integrity levels (L0–L3) referenced in §11.4. *License: open.*
- 🛠 **Sigstore** — [docs.sigstore.dev](https://docs.sigstore.dev/). Keyless, identity-based signing
  of artifacts with a public transparency log — the modern answer to "who built this, and can I
  verify it?" *License: Apache-2.0.*
- 📄 **CycloneDX** — [cyclonedx.org](https://cyclonedx.org/) — and **SPDX** —
  [spdx.dev](https://spdx.dev/). The two mainstream SBOM standards (ECMA-424 and ISO/IEC 5962
  respectively). *License / standard: open.*
- 🎭 **MALUS** (satire) — [malus.sh](https://malus.sh/). A deadpan parody of an AI "clean-room"
  service that claims to launder away open-source license and attribution obligations. The joke
  makes the §11.4.2 point vivid: the open-source supply chain runs on reciprocity, and eroding
  it is its own slow supply-chain risk. *Read it, then read a real license.*

## Standards, frameworks, and courses

- 📄 **NIST SP 800-218 — Secure Software Development Framework (SSDF) v1.1** —
  [csrc.nist.gov/pubs/sp/800/218/final](https://csrc.nist.gov/pubs/sp/800/218/final). The common
  vocabulary of secure-development practices referenced in §11.5. *Access: U.S. government work,
  public domain.*
- 🎓 **OpenSSF — "Developing Secure Software" (LFD121)** —
  [openssf.org/training/courses](https://openssf.org/training/courses/). A free, self-paced online
  course (~14–18 hours) with a free certificate; also on edX. The single best free starting point
  for a student who wants breadth. *Access: free, including the certificate.*
- 📄 **Google Cloud — Software supply chain security docs** —
  [cloud.google.com/software-supply-chain-security/docs/attack-vectors](https://cloud.google.com/software-supply-chain-security/docs/attack-vectors).
  Maps source, build, dependency, and deployment threats onto the SLSA framework. *License:
  CC BY 4.0.*
- 📄 **Hastings & Walcott, "Continuous Verification of Open Source Components in a World of Weak
  Links," ISSREW 2022** — [doi.org/10.1109/ISSREW55968.2022.00068](https://doi.org/10.1109/ISSREW55968.2022.00068).
  The published paper behind §11.4's six-control framework. *Access: IEEE (publisher page; author
  preprints are widely indexed).*

## License note

Linked resources remain under their own licenses; this page is CC BY-SA 4.0.
