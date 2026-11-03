---
name: ghost-crawler
version: 1.1.0
type: ai-skill
architecture: package
description: >-
  Legend-tier organ (Tier A — The Silent Infiltrators) built from the Adrian
  Lamo lineage — enter-without-knocking infrastructure hunting. Drives Phase 1
  from PASSIVE public indexes first (CT logs, search-engine dork grammar,
  public archives, DNS records), hunting the forgotten side doors — abandoned
  subdomains, exposed panels, open directories, backup archives, misconfigured
  storage, accidentally-public internal services — while the guarded main
  application stays untouched. ESince v1.1.0 the organ carries the executable
  method layer (A16) — a mechanical critique of the Lamo-era form's floors
  (entries as anecdotes with the noticing left in the man, indexes read
  without coverage records, side-door classes implicit per story, archive
  freshness unstamped, the no-trace discipline carried by prose ethics instead
  of accounting) shipped as protocol M1–M5: the index protocol with a coverage
  table and named gaps, the census schema with a completeness gate, the as-of
  freshness rule that prices follow-up, the exposure differential with
  persistence checks, and the trace ledger that closes every session with
  counted touches. Use when scope is tight and information minimal, when the
  target's WAF is scanner-hostile, when the operator wants misconfigurations
  and forgotten assets instead of app-layer bugs, or when recon must raise
  zero alarms ("masuk tanpa mengetuk", "siluman", "cari misconfiguration",
  "google dorking", "forgotten assets", "side door", "avoid the WAF").
category: security/legend-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: Adrian Lamo (1981-2018 — the "homeless hacker"; Yahoo/Microsoft/WorldCom/NYT entries via infrastructure misconfiguration, public proxy discipline)
  tier: A — The Silent Infiltrators
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; program rules that permit passive public-index queries
---

# ghost-crawler v1.1.0 — Enter Without Knocking

## 0. What This Skill Is — and Is Not

* **Is**: the posture organ for tight scope, thin information, and
  WAFs that punish scanners. It hunts the FORGOTTEN perimeter —
  assets the operator's target forgot it owns — using passive
  public indexes first, and it routes every discovery into the
  existing recon organs rather than duplicating them.
* **Is not**: an exploitation organ, and explicitly not an
  emulation of Lamo's unauthorized entries — his targets were
  entered without permission; this organ's entries are authorized
  program scope, and the proof of a side door is a single bounded
  request, not a residence. The doctrine distilled is WHERE he
  looked and the attribution discipline, translated to authorized
  hunting.

## 1. Inherited Contracts

Plugs into **Phase 1** (recon & mapping) of the mythos-bug-hunter
spine, driving the existing organs: subdomain-hunter (enumeration,
takeover pairs), content-discovery (calibrated walks, backup triage),
cloud-config-auditor (anonymous storage, CORS, takeovers),
surface-cartographer (the dossier). Inherits R0 (the side door must
be IN scope — a forgotten asset outside program scope is reported
as intel, never probed), R5 (index output is a hypothesis until the
verification probe), and the effort budgets (R7). Craft layer:
pipeline-smith shapes the passive stages; scan-economist prices
each sweep.

## 2. The Lineage (attribution, with the honest caveat)

**Adrián Alfonso Lamo Atwood (1981–2018)** — "the homeless hacker" —
entered the networks of Yahoo, Microsoft, WorldCom, and the New York
Times (2001–2002) not by breaking application logic but by finding
infrastructure nobody was watching: misconfigured proxies, exposed
internal services, forgotten credentials in plain sight. He crawled
through public web proxies for attribution hygiene, worked from
libraries and internet cafés, and famously reported what he found —
the 2003 DOJ complaint (United States v. Lamo) and his 2004
conviction document the method's shape. He died in March 2018; this
distillation treats the historical record with respect and uses it
only as methodology reference. The operator's brief frames the
doctrine as "enter without knocking — attack the unguarded side
instead of the guarded main app, via public search engines
passively". The verification record is `references/sources.md`.

## 3. Doctrine — How Lamo-Thinking Runs

1. **The front door is a decoy.** The guarded main application is
   the most-watched, best-tested, WAF-protected surface on the
   estate. It is the LAST thing this organ touches.
2. **Forgotten beats fortified.** Abandoned subdomains, old
   branding, staging hosts left public, backup archives, storage
   buckets created for a launch and never locked: these are owned
   by nobody and watched by nobody.
3. **Passive indexes are the map.** Certificate transparency,
   search-engine dorks, public archives (job posts, press releases,
   code-hosting orgs), DNS records — the target is never touched
   while the map is drawn.
4. **One knock, one answer.** Each candidate side door receives
   exactly ONE bounded verification probe; confirmation moves it to
   the dossier; the probe count is the organ's honesty metric.
5. **Stay a ghost.** Rate floors, no pattern-spray, no retry
   escalation; attribution hygiene per program rules (operator-
   approved egress only where allowed). If a WAF notices, that is
   an engagement fact to report, never a volume war.

## 3.5 The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published passive-hunt form where it was mechanically weak —
every entry a story (the method stays in the man), "the indexes" consulted
ad hoc with no coverage accounting, side-door classes implicit in each
anecdote, cached snapshots treated as findings without as-of dates,
"I didn't disturb anything" as an unauditable claim — and ships the
executable replacement: **M1** the index protocol (ordered pass, one
EXPERIMENT per index, query grammar recorded verbatim, coverage table with
named gaps), **M2** the census schema (every catalog class produces
candidates or a recorded no-yield proof — refused closure otherwise),
**M3** the freshness rule (≤ 30 d present / 30–180 d flagged / > 180 d
MEMORY, priced accordingly), **M4** the exposure differential (index-derived
candidate vs declared surface; persistence ≥ 2 checks across ≥ 24 h),
**M5** the trace ledger (passive reads counted; active touches 0 or each
justified on record).

## 4. Procedure — Numbered Actions

1. Posture check: `auth_status` + the program's passive-source
   rules; declare the rate floor and the one-probe-per-candidate
   rule in the plan note.
2. Passive sweep, in order (each stage a pipeline-smith-shaped,
   scan-economist-priced stage; all outputs are FACT/lead records):
   a. CT logs + DNS history via `ct_subdomains` / `dns_resolve` —
      the hostname superset, flagging dangling/delegated-but-forgotten
      names (route to subdomain-hunter for takeover pairs).
   b. Dork grammar pass over public search engines — one query per
      misconfig class from `references/side-door-catalog.md`
      (exposed panels, open directories, backup archives, verbose
      error indexes, staging hostnames).
   c. Archive/branding sweep — old codenames, previous products,
      acquired companies, abandoned code-hosting orgs (public
      information only).
   d. Anonymous-storage sweep per cloud-config-auditor's bounded
      checks, where program scope covers the storage namespace.
3. Candidate triage: every passive hit becomes a dossier BACKLOG
   entry with its index source cited; nothing is probed yet.
4. One-probe verification, priority-ordered: exactly one
   `http_probe` per candidate (existence + class of exposure);
   the response (not the index snippet) decides CONFIRMED-exposure
   vs dead lead (R5).
5. Exposure classification: found side doors are REPORTED as
   exposures (open bucket, exposed panel, takeover-ready delegation)
   — exploitation beyond the one proof is an operator decision,
   not an agent action (takeover canary: one operator-controlled
   token, then release — subdomain-hunter's rule).
6. Report posture: numbers stated — candidates from indexes, probes
   spent, exposures confirmed per class, takeover pairs, and the
   main-app request count (which should read ZERO or near-zero).
7. Exit gate: passive stages run with record counts, candidates
   triaged, probes spent = candidates probed, exposures classified
   with citations, remainder parked with resume notes.

## 5. Hard Rules (mechanically enforced)

1. **Passive before any probe.** A candidate with no passive-index
   citation is not probed — this organ never guess-walks hosts.
2. **One probe per candidate.** A second request at a candidate
   needs a new hypothesis and a ledgered reason; retries after a
   WAF reset are forbidden (refusal-is-final, spine R0 corollary).
3. **Scope owns the side door.** Forgotten assets outside program
   scope are reported to the operator as intel — never probed.
4. **Exposure ≠ exploit.** Discovered panels/buckets are proven
   exposed (one bounded request), not looted; default-credential
   attempts against a discovered panel require an explicit operator
   instruction recorded in the ledger.
5. **The main app stays untouched** while unexplored side doors
   remain — that inversion is the organ's identity.

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Hostname superset, delegations | `ct_subdomains`, `dns_resolve` (subdomain-hunter) |
| Calibrated content/backup walks on confirmed hosts | `content_discover` (content-discovery) |
| Storage/CORS bounded checks | cloud-config-auditor organ |
| The one verification probe | `http_probe` |
| Triage + dossier backlog | `dossier_add` (surface-cartographer, backlog=True) |
| Passive stage shaping + pricing | pipeline-smith + scan-economist organs |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Building the dork grammar / misconfig classes | `references/side-door-catalog.md` |
| Verifying the Lamo lineage (and its caveat) | `references/sources.md` |
| Grading the published form, running the index pass, closing the census gate | `references/method-upgrade.md` |
