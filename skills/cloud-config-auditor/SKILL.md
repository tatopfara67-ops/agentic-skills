---
name: cloud-config-auditor
version: 2.1.0
type: ai-skill
architecture: package
description: Phase-1/3 cloud-and-config organ, upgraded (v2) with the Toni de la Fuente (Prowler) lineage — CORS origin-differential matrix, anonymous-access checks on object storage (bounded to one listing page), dangling-DNS takeover verification, and header/hygiene facts, plus checks-as-code discipline: stable check IDs with versions, CIS benchmark citation for severity words, drift re-verification in the engagement window, and posture families over magic scores. Use when the operator asks to audit CORS, check S3/GCS bucket anonymous access, verify a subdomain takeover candidate, or review security headers and TLS hygiene ("tes CORS", "bucket anonymous", "S3 misconfig", "takeover check", "security headers", "origin differential", "CIS", "posture", "check version").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: v2 — Toni de la Fuente (Prowler author/steward; the checks-as-code, benchmark-mapping, and open-posture tradition)
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# cloud-config-auditor v2.1.0 — Misconfiguration Is A Differential Too

## 0. What This Skill Is — and Is Not

* **Is**: the organ for the misconfiguration family: CORS, anonymous
  object-store access, dangling DNS, and hygiene headers — each checked as
  a differential against a control origin/request, never as a screenshot.
* **Is not**: a cloud account auditor. No credentials, no console, no
  infrastructure APIs — only what the target's public HTTP surface answers.
  Since v2 it carries the **Toni de la Fuente lineage** as its field-guide
  layer — checks as versioned code with benchmark citations, not scanner
  opinions.

## 1. Inherited Contracts

Plugs into **Phase 1** (hygiene facts) and **Phase 3** (differentials) of
the mythos-bug-hunter spine. Inherits the Canon, ledger discipline,
closure vocabulary, and the bounded-scope proof rule (one listing page,
then stop — spine §8.2).

## 2. The Lineage Layer (v2 — the de la Fuente doctrine)

**Toni de la Fuente** — Prowler's author and steward; the open-source
cloud-posture tradition where every check is a versioned rule with a
severity, a rationale, and a remediation. v2 folds the lineage in as
five field rules, applied inside the procedure (§3) and detailed in
`references/checks-as-code.md`:

1. **Every check carries a stable ID + version + benchmark paragraph**
   (CCA-CORS-01 style) — the rule text lives in the reference, not in
   the operator's memory.
2. **Severity words cite the mapped paragraph** (CIS families), never a
   mood; where CIS and the target's hardening guide disagree, BOTH are
   recorded.
3. **Verdicts carry timestamps.** Load-bearing verdicts re-verify inside
   the engagement window before the report ships; flips are
   report-worthy observations.
4. **Name the posture shape, then the provider instance** — the families
   are shared across clouds; the fingerprints are local and date-pinned.
5. **Matrix tables over magic scores.** An aggregated grade that cannot
   be unpacked back into its records is exactly the hallucination-shaped
   output this repo exists to prevent.

## 2.5 First Principles — the WWH registers (A14)

* **WHAT** — a posture class: CORS allow-shapes, anonymous object
  storage, dangling DNS delegations, absent security headers, cookie
  attribute shapes. Unified not by exploit syntax but by locus: the
  CONFIGURATION is the attack surface — nothing is injected, the
  shipped state itself is the bug. The families are shared across
  providers; the fingerprints (exact header shapes, provider markers)
  are local and date-pinned.
* **WHY** — every misconfiguration is a frozen decision meeting a
  changed world: the CORS allow written for one origin after the
  surface grew five; the bucket ACL set public before the data became
  sensitive; the DNS record pointing at a service that was later
  deleted. The root cause is that configuration is decided once, at
  setup, with the adversary model of that day — and nothing in the
  cloud re-derives it as topology drifts. That is why this class
  compounds with company age and why re-verification inside the
  engagement window (v2 rule 3) is not paranoia.
* **HOW** — each check is a stable-ID rule run as a differential, not
  a verdict from memory: the CORS origin triad (no-origin baseline,
  evil-origin treatment, subdomain control), the anonymous/garbage-
  token storage pair, the CNAME-chain + provider-marker double fact.
  Severity words cite benchmark paragraphs; verdicts carry timestamps
  and re-verify before the report; matrices ship, aggregates do not.

War note (A15): this organ IS W3 — misconfiguration is neglect made
visible, so the queue ranks by neglect signals (age, drift, forgotten
edges) over surface fame. The cheng sweep is the check catalog
(CCA-*, CIS families) against the inventoried surfaces; the ch'i is
the dangling edge — the takeover pair or takeover-shaped DNS relic
left behind by an infrastructure migration nobody re-audited. W2:
the bounded proof reads ONE page of keys and stops; a full bucket
dump is looting, not evidence.

## 3. Procedure — Numbered Actions

1. Entry: AUTH record present; target in scope.
2. **CORS matrix** per `references/cors-matrix.md`: the origin differential
   is three requests — no Origin header (baseline), an evil origin
   (treatment), a subdomain-of-target origin (control that separates
   reflected-allow from wildcard-allow). Read ACAO/ACAC verdicts from the
   records, not from memory; the check row carries its CCA-CORS-* ID (v2).
3. **Object storage anonymous access** for storage-shaped surfaces
   (file-storage class from the dossier): the bucket URL probed once
   anonymous (list attempt), once with a garbage token (control). A 200
   ListBucket-style XML body on the anonymous attempt is the SURFACE
   record; the bounded proof reads ONE page of keys and stops.
4. **Dangling-DNS verification** for takeover candidates surfaced by
   subdomain-hunter: the CNAME-chain FACT plus the provider-marker FACT
   (procedure in `references/takeover-checks.md`); CONFIRMED claims about
   claimability stay operator-side — this organ records evidence, it does
   not register resources.
5. **Hygiene facts** on the main surfaces: security headers present/absent
   (CSP, HSTS, XFO, XCTO, referrer-policy), cookie attribute shapes
   (Secure/HttpOnly/SameSite) — recorded as FACTs; absent protections are
   facts, not findings; they feed hypotheses only when combined with a
   reachable sink.
6. Exit gate: matrix tables complete with verdicts citing their request
   records; storage verdicts with bounded-listing attestations; takeover
   candidates with their record pairs; hygiene fact counts.

## 4. Hard Rules (mechanically enforced)

1. **Every CORS verdict cites three records** (baseline/treatment/control
   origins). Single-origin screenshots close nothing.
2. **One listing page.** Storage enumeration proofs are bounded; "could
   list everything" is a claim about the mechanism, not an invitation.
3. **No resource registration.** Takeover claimability is reported as an
   evidence pair; registering the dangling resource is an explicit
   operator action outside this organ.
4. **Hygiene is facts, not severity.** Missing headers alone never carry
   severity words in the report without a paired reachable-sink record.
5. **Check rows carry ID + version + benchmark citation** (v2) — a
   verdict whose rule text cannot be found is an incomplete record.

## 5. Tool Routing

| When | Tool |
| --- | --- |
| Origin differentials, storage probes, hygiene fetches | `http_probe` (EXPERIMENT/CONTROL) |
| CNAME chains for takeover candidates | `dns_resolve` (subdomain-hunter organ) |
| Recording verdicts | `ledger_append` (SURFACE/EXPERIMENT/CONTROL) |
| Registering surfaces | `dossier_add` (surface-cartographer) |

## 6. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Running the CORS matrix / reading verdicts | `references/cors-matrix.md` |
| Verifying a takeover candidate | `references/takeover-checks.md` |
| Check IDs, benchmark mapping, drift re-verification, posture families | `references/checks-as-code.md` |
| Citing the lineage artifacts behind the v2 layer | `references/sources.md` |
