---
name: module-smith
version: 1.1.0
type: ai-skill
architecture: package
description: Craft-lineage organ distilled from HD Moore — founder of the Metasploit Framework (2003) and of internet-scale exposure measurement (Project Sonar, 2013). Exploitation as composition: the door-opener (exploit), the cargo (payload), the delivery (stager/handler) are separate, rankable, reusable concerns — every hypothesis in this pipeline is a module with reliability metadata (rank, references, disclosure date), every impact proof is a payload kept separate from the access proof, and every claim of exposureSince v1.1.0 the organ carries the executable method layer (A16) — a mechanical critique of the HD Moore art's floors (rank metadata asserted instead of measured, stagers tuned for one target class, composition proven by single-shot demo, internet-scale measurement without a written protocol, payload compatibility as prose folklore) shipped as protocol M1–M5: the module record with measured reliability, the stager differential across delivery classes, the composition joint-gate with cleanup accounting, the measurement protocol with harm gates, and the compat matrix with rank arithmetic. Use when designing or structuring exploit/verification work, when reusing prior findings on new surfaces, when measuring exposure prevalence, or when composing probe chains ("reuse the earlier finding", "how reliable is this vector", "is this exposure systemic", "package this as a reusable check").
category: security/craft-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: HD Moore — Metasploit Framework (2003, Ruby, acquired by Rapid7 2009), Project Sonar (2013, internet-wide UDP scans, open data)
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# module-smith v1.1.0 — The HD Moore Lineage

## 0. What This Skill Is — and Is Not

* **Is**: the organ that structures offensive work as *composed,
  reusable, ranked modules* instead of one-off scripts — and that
  treats "how exposed is this, really?" as a measurable question with
  a recorded baseline.
* **Is not**: an exploit framework, and never a launcher. The arsenal
  runs bounded probes with canaries; this organ governs how those
  probes are *shaped, ranked, reused, and measured*.

## 1. The Lineage (attribution)

HD Moore published the Metasploit Framework in October 2003 (Perl,
rewritten in Ruby in 2004), grew it into the industry's standard
exploit platform, and later ran Project Sonar (announced 2013):
weekly internet-wide scans of UDP services, published as open data.
Sources: references/sources.md — the verification record

## 2. The Four Laws of Module Craft

1. **Separation of concerns.** The exploit opens the channel; the
   payload decides what travels it; the stager stages; the handler
   listens. In arsenal terms: the *access proof* (the differential
   that shows the door opens) is a different artifact from the *impact
   proof* (the canary that shows what walks through). Never fuse them
   — a finding whose access proof is its impact proof is unauditable.
2. **Reliability is metadata.** Metasploit modules carry rank
   (manual/great/normal/average/low), references (CVE, advisory URLs),
   disclosure dates. Modern form: every H-record states its prior,
   the records it stands on, and how often it reproduced (n_runs);
   a hypothesis without a rank is a guess wearing an ID.
3. **Frameworks compound, scripts evaporate.** A module written for
   one target this morning is reusable against the next target with
   the same class tomorrow — if it was written as a module: declared
   inputs, declared observable, declared falsifier. Reuse is a design
   decision made at write-time.
4. **Exposure is a measurement, not a vibe.** Sonar scanned the same
   services weekly and published the data; "most should never be
   exposed to the internet" became a checkable sentence. Modern form:
   prevalence claims ("this endpoint pattern is systemic") cite a
   CONTROL baseline — N surfaces probed with the same effort, the
   hit-rate recorded — never a feeling.

## 2.5 The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published module art where it was mechanically weak —
`Rank: Excellent` as an author's label rather than a measurement, stagers
inheriting the demo's egress conditions, exploit+stager+payload proven by
one run, Sonar-class measurement left to goodwill, compat notes as folklore
— and ships the executable replacement: **M1** the module record
(reliability n/k per target-class; labels without n refused), **M2** the
stager differential (n ≥ 5 per delivery class; FIELD-READY at ≥ 4/5
established and surviving), **M3** the composition proof (joint n ≥ 5,
clean-state per run, confidence = min(links) × joint factor, floor link
named), **M4** the measurement protocol (scope, rate, dedup, harm-gates,
aggregate disclosure — all fields filled before the run), **M5** the
compat matrix + rank arithmetic (EMPTY cells never claim; rank =
reliability × field-readiness × joint, factors visible).

## 3. Procedure — Numbered Actions

1. Frame each hypothesis as a module card: **inputs** (target,
   preconditions), **observable** (the exact response delta that
   would count), **falsifier** (the neighbor that must NOT move),
   **rank** (prior %, from where), **references** (R-NNN, advisories).
2. Prove access first: the differential triad (baseline / treatment /
   control) establishes the door opens — nothing else.
3. Prove impact second, as a separate payload: one bounded canary
   (the spine's canary ladder), recorded as its own CANARY record
   citing its own records.
4. Rank from reproduction: n_runs updates the module's rank; unstable
   modules drop to leads, no exceptions.
5. Index for reuse: modules keyed by surface class + VRT class; when
   a new surface of a known class appears, re-run the module card,
   do not re-derive it from scratch.
6. Measure exposure claims: prevalence = hits/attempted over the
   recorded probe set; state the denominator or drop the claim.

## 4. Tool Routing

| When | Tool |
| --- | --- |
| Writing module cards | `ledger_append` (EXPERIMENT pre-registrations) |
| Access proofs (the triad) | `http_probe` × {baseline, treatment, control} |
| Impact proofs (payloads) | canary ladder — spine Phase 4 + CANARY records |
| Reuse lookup | `ledger_summary`, dossier class filters |
| Exposure measurement | probe sets over surfaces + CONTROL records |
| CLI oracles (sqlmap class) | `arsenal_route` (`--batch` mandatory, oracle only) |

## 5. Hard Rules

1. Access proof and impact proof are separate records — a fused
   "proof" fails the report gate.
2. No module ships without rank + references; no rank without runs.
3. Reuse goes through the card (inputs/observable/falsifier), never
   by copy-pasting a past conclusion onto a new target.
4. Prevalence claims carry their denominator, always.
5. The framework serves the ledger, not the reverse: a module that
   cannot be expressed as records does not exist here.

## 6. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Structuring hypotheses as modules; ranking | references/mindset.md |
| Running module proofs and exposure counts | references/playbook.md |
| Checking lineage claims and reading list | references/sources.md |
| Grading the published method, measuring module reliability, computing rank | references/method-upgrade.md |
