---
name: cloud-config-auditor
version: 1.0.0
type: ai-skill
architecture: package
description: Phase-1/3 cloud-and-config organ — CORS origin-differential matrix, anonymous-access checks on object storage (bounded to one listing page), dangling-DNS takeover verification, and header/hygiene facts, all evidence-cited. Use when the operator asks to audit CORS, check S3/GCS bucket anonymous access, verify a subdomain takeover candidate, or review security headers and TLS hygiene ("tes CORS", "bucket anonymous", "S3 misconfig", "takeover check", "security headers", "origin differential").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# cloud-config-auditor v1.0.0 — Misconfiguration Is A Differential Too

## 0. What This Skill Is — and Is Not

* **Is**: the organ for the misconfiguration family: CORS, anonymous
  object-store access, dangling DNS, and hygiene headers — each checked as
  a differential against a control origin/request, never as a screenshot.
* **Is not**: a cloud account auditor. No credentials, no console, no
  infrastructure APIs — only what the target's public HTTP surface answers.

## 1. Inherited Contracts

Plugs into **Phase 1** (hygiene facts) and **Phase 3** (differentials) of
the mythos-bug-hunter spine. Inherits the Canon, ledger discipline,
closure vocabulary, and the bounded-scope proof rule (one listing page,
then stop — spine §8.2).

## 2. Procedure — Numbered Actions

1. Entry: AUTH record present; target in scope.
2. **CORS matrix** per `references/cors-matrix.md`: the origin differential
   is three requests — no Origin header (baseline), an evil origin
   (treatment), a subdomain-of-target origin (control that separates
   reflected-allow from wildcard-allow). Read ACAO/ACAC verdicts from the
   records, not from memory.
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

## 3. Hard Rules (mechanically enforced)

1. **Every CORS verdict cites three records** (baseline/treatment/control
   origins). Single-origin screenshots close nothing.
2. **One listing page.** Storage enumeration proofs are bounded; "could
   list everything" is a claim about the mechanism, not an invitation.
3. **No resource registration.** Takeover claimability is reported as an
   evidence pair; registering the dangling resource is an explicit
   operator action outside this organ.
4. **Hygiene is facts, not severity.** Missing headers alone never carry
   severity words in the report without a paired reachable-sink record.

## 4. Tool Routing

| When | Tool |
| --- | --- |
| Origin differentials, storage probes, hygiene fetches | `http_probe` (EXPERIMENT/CONTROL) |
| CNAME chains for takeover candidates | `dns_resolve` (subdomain-hunter organ) |
| Recording verdicts | `ledger_append` (SURFACE/EXPERIMENT/CONTROL) |
| Registering surfaces | `dossier_add` (surface-cartographer) |

## 5. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Running the CORS matrix / reading verdicts | `references/cors-matrix.md` |
| Verifying a takeover candidate | `references/takeover-checks.md` |
