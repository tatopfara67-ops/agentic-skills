---
name: subdomain-hunter
version: 1.0.0
type: ai-skill
architecture: package
description: Phase-1 subdomain enumeration organ — passive-first ladder (certificate transparency, passive CLI routing), resolution and CDN/wildcard detection, permutation round, and CNAME-dangling takeover checks, all evidence-cited. Use when the operator asks to enumerate subdomains, expand a domain's asset inventory, check wildcard DNS, or investigate subdomain takeover ("cari subdomain", "enum subdomain", "subdomain takeover", "permutasi domain", "asset discovery").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# subdomain-hunter v1.0.0 — Passive First, Always

## 0. What This Skill Is — and Is Not

* **Is**: the Phase-1 organ that answers "what exists under this domain?"
  with a deduplicated, resolved, classified list — and then answers the
  follow-up nobody should skip: "is any of it dangling?"
* **Is not**: a brute-force firehose. Active enumeration is the LAST rung of
  the ladder, and it is rate-courteous when it runs.

## 1. Inherited Contracts

Plugs into **Phase 1** of the mythos-bug-hunter spine. Inherits the Canon
(especially R0 scope gate, R1 plan-before-action, R5 tools-are-not-verdicts),
the ledger record format, and backlog mechanics. Does not restate them.

## 2. The Ladder — Cheapest Signal First

1. **Certificate transparency** — `ct_subdomains(program, domain)`. Reads a
   public database; the target is never touched. Offline egress returns
   `ok=False` gracefully — record it and move down the ladder, never pretend.
2. **Passive CLI routing** — if the environment has `subfinder` or
   `amass -passive`, `arsenal_route(program, "subfinder", domain, "-silent")`
   harvests aggregated passive sources. Scanner output is a hypothesis about
   existence, not a finding (R5): each discovered name still needs resolution
   evidence before it becomes a SURFACE record.
3. **Resolution round** — `dns_resolve(program, name)` for every candidate.
   Only resolving names are surfaces. Record wildcard behavior FIRST:
   resolve two random non-existent names; if they resolve, every "live"
   claim downstream must say "live-or-wildcard" until proven otherwise.
4. **Permutation round** — only when the asset space is thin: generate
   permuted candidates (dev/staging/uat/internal prefixes, `-word` and
   `word2` joins — the generator table is in `references/sources.md`) and
   resolve them. This is DNS-side only, still not an HTTP flood.
5. **HTTP liveness** — `http_probe` each resolved name once. Status, server
   header, and redirect target become the reachability verdict for the
   dossier.

## 3. Takeover Discipline (the follow-up that matters)

A resolving name with a CNAME pointing at a deprovisioned third party is a
takeover candidate. The check sequence and the provider signature table
(Heroku/GitHub Pages/Shopify/Azure/CloudFront and friends) live in
`references/takeover-signatures.md`. The discipline that makes it evidence:

* The CNAME chain is a FACT record (from `dns_resolve`).
* The provider's "not found" marker on the dangling target is a second FACT
  record (from `http_probe` of the service host).
* Only the two records together justify a Phase-2 hypothesis; neither alone
  is a finding.

## 4. Procedure — Numbered Actions

1. Entry: AUTH record present; domain is in scope (`scope_check`).
2. Run ladder rungs 1–2; merge candidate names; dedupe; count them.
3. Wildcard probe (two random names) — record the verdict.
4. Resolve all candidates; drop non-resolving ones with a FACT record each
   (a negative is still an observation).
5. `http_probe` the survivors; classify (surface-cartographer taxonomy) and
   `dossier_add` each with evidence citations.
6. For names whose CNAME leaves the parent domain: run the takeover
   sequence from `references/takeover-signatures.md`.
7. Exit gate: numbers stated — candidates found, resolving, live, wildcard
   verdict, takeover candidates. Anything unresolved is parked with a
   reason, not dropped.

## 5. Hard Rules (mechanically enforced)

1. **Passive before active.** The permutation round and HTTP liveness run
   only after CT and passive routing produced their records — the ledger's
   record order proves it (auditor checks: first subdomain-related record
   is a passive-source one).
2. **Wildcard is a verdict, not a vibe.** Two random-name resolutions,
   recorded, before any "live host" claim.
3. **Takeover claims need both records** (CNAME chain + provider marker).
4. **No invented names in the dossier.** Every name cites a discovery record
   (CT output, CLI output, or permutation record).

## 6. Tool Routing

| When | Tool |
| --- | --- |
| CT enumeration | `ct_subdomains` |
| Passive CLI harvest | `arsenal_route` (subfinder / amass -passive) |
| Resolution, CNAME chains, wildcard probe | `dns_resolve` |
| HTTP liveness + provider markers | `http_probe` |
| Registering surfaces | `dossier_add` (surface-cartographer) |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Building the candidate ladder or permutation set | `references/sources.md` |
| Any CNAME leaves the parent domain | `references/takeover-signatures.md` |
