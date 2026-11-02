# Reference — Changelog And Crosswalk

> Part of **mythos-bug-hunter v4.5.0** (package architecture).
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
| §34 researcher conduct / §35 phase playbook | — (methodology: behavior + execution sequence) | — | — | applies to all categories |
| §13 self-repair / §31 mistake-learning | — (methodology) | — | — | — |
| §32 ruthless-mind hypothesis generation | feeds A01/A03/A05 discovery | feeds API1/API5 discovery | feeds LLM01 chains | — |

---

## E. Changelog

```
v4.5.0 (2026-11)
  - New section §34.8 The Long Game (references/researcher-conduct.md):
    mission horizon & the surrender reflex — the conduct answer to the
    most common long-horizon agent failure, quitting while the mission
    is unmet and packaging it as a summary. Mission contract (operator
    goal parsed at Phase 0 into a MISSION state block: objective, done
    criteria as CONFIRMED-closure counts, stop rights, budget); the
    three legal stops (quota met · exhaustion proof · operator release)
    with context exhaustion demoted to a pause — one mission, N
    sessions, resumed via continue_pending; the dead-end redirect rule
    (every FALSIFIED/Park is followed same-session by a queue pull);
    the reframe ban (no silent goal downgrading, no severity
    inflation — report the gap in the same breath); the stamina floor
    (fatigue is not evidence; barren requires closed hypotheses).
  - New conduct card S13 (quota unmet, stopping feels reasonable) and
    failure gallery entry #9 "The quitter" (tell: session close with
    quota unmet and P0/P1 TODOs unresolved, packaged as summary +
    recommendations).
  - engagement-architecture.md: §17.3 gains the mission-quota clause
    (quota unmet + remaining backlog forces TODO regeneration — the
    queue cannot be drained by never filling it; stopping on an unmet
    quota requires the written exhaustion proof); §18.1 state gains the
    `mission` field.
  - SKILL.md: Phase 0 writes the MISSION block when the order names a
    goal; routing and quick-reference card updated. doctrine_forge
    (skill-mythos 1.2.0): the forged bug_quota order now carries the
    mission-horizon clause — quota as continuation mandate — with a
    paired unittest. Version bump 4.4.0 → 4.5.0 (minor: new reference
    content, non-breaking).
v4.4.0 (2026-11)
  - New section §32.10 The Trained Eye (references/ruthless-mind.md): instinct
    as a measurable asset — the 14-cue catalog (sequential-id vs UUID drift,
    status-body asymmetry, dual id positions, v1/v2 twins, verbose oracles,
    bimodal timing, per-role header drift, dead-but-alive verbs, stale build
    hashes, decorative claims, orphan methods, tenant-slice acceptance,
    GraphQL/REST twins, per-edge rate asymmetry), each with its smell, why it
    smells, historical yield, and first cheap probe; the notice protocol
    (log-on-fire, same-session H-record or named park, cue tag on the record);
    the calibration loop (per-cue yield tally at engagement close, promote
    ≥ 20%, demote < 5% twice, two-engagement floor before retirement).
  - SKILL.md: H-record grammar gains the `cue:` line (required when the
    trigger was noticing, not a scanner); operator set gains Noticing;
    routing table updated. Version bump 4.3.0 → 4.4.0 (minor: new reference
    content, non-breaking grammar addition).
v4.3.0 (2026-11)
  - New module §34 (references/researcher-conduct.md): the behavioral layer —
    how the agent acts as a security researcher while doing anything else in
    this package. Identity contrast table (scanner wrapper vs researcher,
    each row ledger-auditable); the 4-step moment loop (record → classify →
    explain → queue, ≤60 s per observation) with the expectation-line rule
    (no stated expectation = the request was noise, not an experiment) and
    the chase rule (curiosity never hijacks the queue); 12 numbered conduct
    situation cards S1–S12 (anomaly, 403/401, archived 404, 405, 500/stack
    trace, scanner hit, certainty, stuck, operator pressure, "is it secure",
    out-of-scope discovery, unknown tech); the communication contract (5
    message shapes only, blocking-question format, refusal format, the
    honest-unknown format); the researcher's clock (time allocation
    5/25/10/40/10/10 with no idle time); 7 mechanical habits (whole-response
    reading, foreign-ID following, hot disproven list, sibling checks,
    hypothesis-before-payload, 10-minute resume ritual, same-day anomaly
    closure); the 8-entry behavioral failure gallery (wrapper, moth,
    gambler, novelist, people-pleaser, goldfish, one-shot wonder,
    control-skiper) with ledger tells and countermeasures.
  - New module §35 (references/phase-playbook.md): the execution manual —
    the phase framework from recon to report, action by action. Six fixed
    parts per phase (objective / entry / actions / decisions / exit gate /
    failure modes); §16.1 machine mapped onto the SKILL.md §4 phase numbers.
    Phase 0: 6 numbered actions incl. the six-probe fact-table baseline and
    the shell capability-inventory loop. Phase 1: 9 cost-ordered recon
    stages (passive-first) with commands and ledger landings. Phase 2: the
    5-source hypothesis drill — surface-class × attack-class matrix over
    all 21 inventory categories, the 7 assumption families (role, ownership,
    state, ordering, uniqueness, idempotency, price integrity), anomaly
    abduction, scanner conversion, sibling seeds. Phase 3: the 10-step
    experiment loop with the outcome routing table (reproduced / not
    reproduced / no delta / partial). Phase 4: canary round-trip design,
    bounded reach, weakest-verified-link impact chains. Phase 5: gate →
    ledger draft → auditor → ship → mistake ledger → calibration audit →
    close ritual. §35.7: compact two-day illustrative engagement timeline.
  - SKILL.md: v4.3.0; description extended (conduct contract + phase
    playbook); package layout 17 → 19 modules with the operational-spine
    note; §4 gains the contract/execution/behavior routing paragraph; §17
    index gains the two module rows; §18 quick card gains the two routing
    lines (how to act → §34; what to run → §35).
  - All reference module headers bumped to v4.3.0.

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
