# Reference — Changelog And Crosswalk

> Part of **mythos-bug-hunter v4.2.0** (package architecture).
> **Load when:** Provenance: methodology crosswalk and changelog.
> Authoritative rules, Canon, and pipeline contracts live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts with the
> SKILL.md Canon or contracts, **SKILL.md wins**. Section numbering below is
> inherited from the v4.0 monolith and is intentionally non-sequential.

---

## D. Methodology Crosswalk

| This skill | OWASP Top 10:2025 | API Top 10:2023 | LLM 2025 / Agentic 2026 | WSTG |
|---|---|---|---|---|
| §20 Authorization matrix | A01 | API1 BOLA, API5 BFLA | ASI03, LLM06 | ATHZ-* |
| §21 Status playbook | A05, A10 | API7 | — | INFO-* |
| §22 AuthN/session/JWT | A07 | API2, API3 | — | ATHN-*, SESS-* |
| §23.1-23.2 smuggling/cache | A05, A08 | API4 (unrestricted resource consumption, where applicable) | — | — |
| §23.3 races | A04, A08 | API4 | — | BUSL-* |
| §23.4 SSRF | A05 (injection family) | API8 SSRF | LLM01 chains | — |
| §23.5 framework bypass | A01, A05 | API5 | — | — |
| §23.6 OAuth | A07 | API2 | — | OATH-* |
| §24 AI surface | A05 (prompt injection family), A01 | API1/5 via agent tools | LLM01-LLM10, ASI01-ASI10 | — |
| §25 supply chain | A03, A08 | — | LLM03, ASI04 | — |
| §19/§28 reporting discipline | A09 | API7 | — | REP-* |
| §9-§10 reasoning core (logic, suspicion engine) | — (methodology) | — | — | applies to all categories |
| §13 self-repair / §31 mistake-learning | — (methodology) | — | — | — |
| §32 ruthless-mind hypothesis generation | feeds A01/A03/A05 discovery | feeds API1/API5 discovery | feeds LLM01 chains | — |

---

## E. Changelog

```
v4.2.0 (2026-10)
  - New module §29 (references/recon-toolchain.md): recon toolchain routing
    (17 jobs, order + rationale + ledger landing per row), target triage
    score (8 countable signals ordering the R1 backlog), duplicate
    suppression (fingerprint-tuple dedup key; one finding for N hosts),
    time-boxes as Park triggers (5/20/45-min clocks extending R7), probing
    ladder for blind vectors (error → differential-content → time → OOB,
    ordered by cost and jitter-immunity), sibling sweep (CONFIRMED →
    20-minute bounded variant hunt via naming/version/controller seams),
    operator-pressure protocol (quota is not evidence; bounded negatives).
  - SKILL.md: R7 enforcement extended with time-box triggers; §4.2 and §17
    route to the new module; reference library 16 → 17 modules.
  - Housekeeping: frontmatter license/author fields; placeholder-marker
    fix in the §17 routing table.

v4.1.0 (2026-10)
  - Package architecture: monolith split into SKILL.md core + 16
    load-on-demand reference modules + scripts + example fixtures;
    progressive disclosure per module headers.

v4.0.0 (2026-10)
  - Reasoning core: Formal Logic Core (modus ponens/tollens exploit and
    falsification chains, fallacy-to-false-positive mapping,
    necessity/sufficiency proof, Laplace induction discipline, abductive
    anomaly triage); Bayesian Suspicion Engine (priors with provenance,
    likelihood-ratio table, hard decision bands, EV/minute prioritization,
    silence compounding, calibration audit).
  - Operational core: Self-Repair Protocol (F1-F5 failure taxonomy, triage
    ladder, one-change-per-retry, retry budget, positive-control ledger);
    Mistake-Learning System (error journal schema, post-mortem triggers,
    bias checklist, regret table, mid-session self-awareness probes,
    session-close ritual).
  - Engineering doctrine: Minimal Code Doctrine (lazy-senior rules,
    robustness floor, mth-* micro-scripts, lifecycle, anti-patterns).
  - Mindset: The Ruthless Mind — nine principles of extreme reasoning
    strictly inside the authorization gate (laziness mapping, assumption
    destruction, cross-domain transplant, dark-lab protocol,
    extreme-input grammar).
  - Integration: candidate records carry p_prior/p_post/evidence_log; TODO
    priority gains EV ranking; prime directives 3.9 and 3.10; Part VI
    renamed Governance and Mindset; sections 28 -> 34; methodology
    crosswalk extended.

v3.0.0 (2026-10)
  - Reasoning core rebuilt as explicit machines: validation loop gates
    (G0-G7), verdict transition machine + calibration ladder, hypothesis
    grammar with falsifiability rules, differential matrix extended with
    tier (H) and concurrency (I) axes.
  - Machine-usable artifacts: JSON schemas for candidate records, TODOs,
    and engagement state; tightened report templates.
  - New Part IV playbooks: modern attack classes (HTTP/2 smuggling, cache
    poisoning/deception, single-packet races, SSRF at the AI edge, Next.js
    middleware bypass CVE-2025-29927, OAuth 2.1-era pitfalls); AI/LLM/agent
    attack surface (OWASP LLM Top 10 2025 + Agentic Top 10 2026 mapping,
    prompt-injection test chains, MCP tool poisoning/rug pulls/shadowing,
    non-deterministic validation discipline); supply-chain integrity
    verification with php2shell (2026), php.net (2021), xz-utils (2024)
    case studies.
  - Part V execution toolkit: curl-first recipes (differential trio,
    fingerprinting, method/path sweeps, header probes, timing, HTTP/2,
    concurrency pattern), safe canary payload library, tool map.
  - Governance: TRENDFRESH research protocol, pre-disclosure/0-day
    etiquette, updated source ladder.
  - Structure cleanup: 6 parts / 28 sections / 5 appendices; each concept
    has exactly one home (v2's duplicated fabrication, status-code, and
    priority content merged); framework references updated to OWASP
    Top 10:2025 editions; authorization matrix extended A-L → A-P;
    ASCII-only prose; no reliance on any specific vendor stack.

v2.0.0 (2026-08)
  - Complete rewrite: pivot from binary/kernel exploitation to web/API
    bug bounty. Validation engine, verdict system, evidence chain,
    pinpoint TODOs, attack surface inventory, Actor-Resource-Action
    authorization testing, status code handling, differential testing,
    calculation precision, stop conditions, reportability gate, state
    management, priority engine, context-window discipline.

v1.0.0 (2026-05)
  - Initial release (binary/kernel exploitation focus).
```

---

*This module is provided for authorized security research and educational
purposes only. Unauthorized use against any system is illegal and
unethical. Always obtain explicit authorization before testing any target.
The accuracy discipline in this module exists precisely because false
positives waste everyone's time and false claims damage trust in security
research.*
