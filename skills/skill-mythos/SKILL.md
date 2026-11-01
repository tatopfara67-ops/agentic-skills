---
name: skill-mythos
version: 1.0.0
type: ai-skill
architecture: package
description: Master activation module for the Skill Mythos bundle — the extreme-expertise organ stack for pentest, bug bounty, and security research. Carries the twelve charter articles (identity, research-grounded synthesis, legitimate methodology assimilation, stability-first autonomy, quality over bounty), the tiered bundle map, the autonomy protocol for self-selecting organs by phase and event, and the triage-grade quality gates: zero false positives via the differential triad, fully reproducible steps, CVSS 3.1 vectors with recomputed scores, Bugcrowd VRT P-ratings with the HackerOne crosswalk. Use at session start, when the operator says activate Skill Mythos, when choosing organs for the current state, or when classifying and rating any finding ("aktifkan Skill Mythos", "which organ fits this", "rate this finding", "CVSS and VRT mapping", "report gates").
category: security/governance
license: MIT
metadata:
  author: tatopfara67-ops
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# skill-mythos v1.0.0 — The Master Charter

## 0. What This Skill Is — and Is Not

* **Is**: the activation module for the bundle. When Skill Mythos is
  installed and the agent is turned loose on authorized work, THIS file is
  the first routing layer: it states what the bundle is, how organs are
  selected and combined autonomously, and the quality standard every
  finding must clear before it ships. One call — `mythos_charter()` —
  returns the distilled version.
* **Is not**: a hunting technique. It performs zero probes. The organs do
  the work; the charter defines the frame they work inside.

## 1. The Charter — Twelve Articles

1. **Identity.** Skill Mythos is an extreme-expertise bundle for
   pentest, bug bounty, and security research — not general-purpose
   skills wearing a security costume.
2. **Research-grounded.** Methods are synthesized from complete public
   sources — books, papers, advisories, post-mortems — read in full
   context, never snippet-mined. Claims still live or die by the
   evidence ledger; no pedigree excuses an uncited claim.
3. **Legitimate assimilation.** The methodology and mindset of named
   public researchers are studied, attributed, and re-implemented as
   decision logic — reading, understanding, implementing. No
   proprietary code, no IP theft, no unattributed borrowing
   (references/assimilation-doctrine.md).
4. **Stability, sustainability, consistency.** Deterministic and
   auditable behavior over cleverness. The same input produces the
   same record; the same vector produces the same score.
5. **Autonomy with accountability.** Once activated, the agent
   self-selects, filters, and combines organs to fit the state,
   situation, environment, and target architecture — autonomously, but
   bounded by R0 scope and the append-only ledger, and auditable after
   the fact.
6. **Selection by phase and event, not curiosity.** Organs are routed
   by engagement phase; the Binary Brain is event-triggered.
7. **Quality over bounty.** The end goal is superior report quality;
   reward-chasing is how reproducibility dies. Profitability follows
   reproducibility.
8. **Zero false positives.** A claim ships only after the differential
   triad — baseline / treatment / control — all ledgered.
   Single-channel observations stay leads.
9. **Full reproducibility.** Any third party can replay every step
   from the report alone; n_runs (or attempts + success_rate) is a
   mandatory field, not a courtesy.
10. **Measured severity.** Every CONFIRMED finding carries a CVSS 3.1
    vector with a recomputed base score (`cvss3_score`) and a Bugcrowd
    VRT mapping with P-rating and HackerOne crosswalk (`vrt_classify`).
11. **Triage viability.** Reports are written for the triage desk:
    precise, hedging-free, evidence-cited, impact-chained,
    classification-complete.
12. **Philosophy per organ.** Each organ carries its methodology's
    essence and documents its lineage; the charter is the convergence
    point, not a replacement for any organ.

## 2. The Bundle at a Glance

| Tier | Skill | Role |
| --- | --- | --- |
| Spine | mythos-bug-hunter (v4.3.0, separate bundle) | discipline layer: R0–R7 canon, ledger, hypothesis grammar, closure gates |
| 0 master | skill-mythos (this bundle) | activation: charter, autonomy protocol, quality gates |
| 1 recon & mapping | surface-cartographer | the organized dossier — asset graph, 21-class taxonomy, priority queue |
| 1 | subdomain-hunter | passive-first enumeration, wildcard verdicts, takeover pairs |
| 1 | content-discovery | calibrated walks, backup/config triage |
| 1 | js-recon | bundle analysis, commented routes, masked secret hints |
| 1 | api-surface-mapper | spec parsing, version diffs, undocumented endpoints |
| 2 access & logic | auth-boundary-mapper | role×resource matrix, IDOR/BOLA differentials |
| 2 | oauth-flow-auditor | 12-check OAuth/OIDC catalog with falsifiers |
| 2 | business-logic-hunter | workflow abuse, races with rate floors |
| 3 deep technical | injection-lab | differential oracles; sqlmap as oracle only |
| 3 | ssrf-playbook | canary-callback channel proofs, bounded egress |
| 3 | xss-playbook | sink contexts, marker proofs, CSP as fact |
| 3 | cloud-config-auditor | CORS matrix, anonymous storage (bounded), takeovers |
| 4 incident | adversary-tracker | the Shimomura Binary Brain — event-triggered hunts on assets you defend |

Execution hand: the **arsenal** MCP server (25 scope-gated tools),
the **auditor** report gate, two self-owned **labs**, and audited
**examples**. Full map with load-when triggers lives in
references/bundle-map.md — the atlas.

## 3. Autonomy Protocol (short form)

1. **Assess state** — phase, authorization posture (`auth_status`),
   environment (what is reachable), target architecture dynamics
   (monolith/API/AI surface), effort budget.
2. **Select organs** by the routing table — never by curiosity.
3. **Combine** deliberately: one organ drives, at most two support;
   say which and why in the plan note.
4. **Re-assess** at every phase boundary and on every incident
   trigger; park the remainder with a resume note (R1).
5. **Interrupt** for the Binary Brain when a sensor or the operator
   reports adversary activity on assets you are authorized to defend.

The full decision procedure, including the state variables and the
combination rules, is in references/autonomy-protocol.md — the
routing contract.

## 4. Quality Gates — the Mythos Standard

Before any report ships (`auditor/audit_report.py`, exit 0 or it does
not ship), every CONFIRMED finding block carries:

* the differential triad — baseline / treatment / control records;
* n_runs ≥ 2 with stable deltas (or attempts + success_rate);
* **cvss:** a CVSS 3.1 base vector + its computed score — the auditor
  recomputes it and a mismatch fails the report;
* **vrt:** the Bugcrowd VRT dotted category + P-rating — validated
  against the shipped official taxonomy
  (references/vrt-taxonomy.json);
* **reproduction:** steps or an E-NNN card a third party can replay;
* impact-chain: and canary attestation lines.

Severity is a three-layer discipline: technical (CVSS), taxonomy
baseline (VRT P-rating + HackerOne crosswalk), and the program-context
call — all three stated, divergences argued, none silently merged.
Details and the report-block template live in
references/quality-gates.md, references/cvss-guide.md, and
references/vrt-mapping.md — in that order of depth.

## 5. Activation Sequence

1. `mythos_charter()` — articles, bundle map with install status,
   quality gates (this file, distilled).
2. `list_skills()` — metadata only; progressive disclosure is the cost
   model.
3. Load the spine (mythos-bug-hunter) and its conduct module.
4. Pick organs by phase via the autonomy protocol.
5. At report time: `cvss3_score` → `vrt_classify` → write the block →
   audit until exit 0.

Wiring, selftest, validation, and the first-session bootstrap are in
references/activation.md — the install runbook.

## 6. Attribution and Licenses

* Bugcrowd Vulnerability Rating Taxonomy data
  (references/vrt-taxonomy.json) is shipped under Apache-2.0 with
  attribution — see NOTICE.md.
* The CVSS 3.1 arithmetic follows the public FIRST specification;
  no FIRST content is redistributed here.
* Methodology lineages (e.g., the Shimomura 1994–95 hunt behind
  adversary-tracker) are documented per organ with public sources.

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Mapping the full bundle, organ load-when triggers | references/bundle-map.md |
| Selecting/combining organs autonomously | references/autonomy-protocol.md |
| Writing or auditing a finding block | references/quality-gates.md |
| Classifying against Bugcrowd VRT / HackerOne | references/vrt-mapping.md |
| Constructing or scoring a CVSS 3.1 vector | references/cvss-guide.md |
| Studying or extending an assimilated lineage | references/assimilation-doctrine.md |
| Installing, wiring, bootstrapping the first session | references/activation.md |
