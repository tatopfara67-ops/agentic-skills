---
name: ssrf-playbook
version: 1.4.0
type: ai-skill
architecture: package
description: >-
  Phase-3 SSRF organ — canary-callback channel-existence proofs on an
  operator-owned interaction host, egress mapping by scheme, redirect-chain
  tracing, and metadata-endpoint checks only inside explicitly authorized
  cloud scope, all as differentials. Since v1.3.0 the organ carries the
  executable method layer (A16) — a mechanical critique of the
  callback-everywhere habit's floors (canary before hypotheses, channel
  conflation, parser disagreement re-discovered per bug, metadata URLs from
  memory, impact claimed without read-back) shipped as protocol M1–M5: the
  channel hypothesis table, the four-rung channel-proof ladder, the
  parser-differential map, the cloud-metadata decision table with mandatory
  headers, and the impact ceiling that refuses gossip. Since v1.4.0 the
  payload corpus deepens (A19): the loopback name family (literal
  localhost, zero-forms, in-127/8, the own-domain-resolves row) and the
  IPv6 bracket family enter the versioned corpus (corpus.json 1.1.0) —
  the scheme matrix's named rows now resolve to byte-exact entries
  instead of prose descriptions. Use when the operator
  asks to test SSRF, check a URL-fetch parameter, map egress from a target,
  trace redirect-based SSRF, or probe cloud metadata reachability ("tes SSRF",
  "url fetch", "internal request", "egress mapping", "metadata endpoint",
  "redirect to internal").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; operator-owned interaction/callback host
---

# ssrf-playbook v1.4.0 — Prove The Channel, Not The Gossip

## 0. What This Skill Is — and Is Not

* **Is**: the organ that proves a server-side request channel with a
  self-owned canary callback, then maps what that channel can reach —
  in bounded, recorded steps.
* **Is not**: an internal-network scanner. Egress mapping is a handful of
  differential probes; port sweeps through the channel are operator
  decisions with their own scope conversations, not default behavior.

## 1. Inherited Contracts

Plugs into **Phase 3** of the mythos-bug-hunter spine. Inherits hypothesis
grammar, experiment contract, closure vocabulary, and the canary doctrine
(§8): the channel-existence proof uses ONLY a marker we own —
`MYTHOS-CANARY-<uuid>` — on an interaction host the operator controls.
No third-party URL is ever the test payload.

## 1.5 First Principles — the WWH registers (A14)

* **WHAT** — the server is made to fetch attacker-chosen resources:
  full SSRF (response visible), blind SSRF (only side effects),
  semi-blind (status/timing hints), plus the egress classes (cloud
  metadata, internal services, file:// and gopher:// style schemes
  where the fetcher honors them).
* **WHY** — the server's network position is the asset: perimeter
  firewalls trust the server's own requests, internal services grew
  up unauthenticated behind them, and the URL parser/redirect chain
  differs at every hop — a fetch the FRONTEND validates can be
  re-aimed by the backend parser after a redirect, a DNS rebinding,
  or a parser's odd scheme. Trust in position plus disagreement
  between parsers is the root cause.
* **HOW** — the channel is the proof: a canary callback to a
  self-owned interaction host, one hit, then stop. Response-body
  claims are leads until the channel (or a bounded, self-owned
  retrieval) confirms; egress is mapped by canary, never by
  collateral fetching of real internal services.

War note (A15): the cheng sweep is the scheme/parameter catalog
against known fetch surfaces; the ch'i is the redirect/rebind path
the target's own parser chain permits that nobody documented. W2
rides the channel law: one canary hit then stop — the internal
network is mapped by inference from one hit, never by storming it.

## 1.6 The Method Layer — Critique, Upgrade, M1–M5 (A16)

A lineage named is not expertise delivered — and neither is a habit.
`references/method-upgrade.md` grades the callback-everywhere default
this organ was forged against — a canary pasted into every parameter
before anything is known, DNS pings reported as compromise, parser
disagreement re-discovered per bug, metadata URLs typed from memory
(false negatives that read as "secured"), impact escalated on gossip
— and ships the executable replacement: **M1** the channel hypothesis
table (URL-shaped parameters registered BEFORE any canary fires),
**M2** the channel-proof ladder (DNS → HTTP fetch → read-back →
metadata; rung 2 is the minimum "confirmed", rung 1 alone is a LEAD),
**M3** the parser-differential map (case/encoding and redirect-follow
pairs per hop boundary, n ≥ 3, interleaved — which hop normalizes is
a FACT), **M4** the cloud-metadata decision table (IMDSv2 two-step,
GCP/Azure mandatory headers — a 403 is "guarded under THIS probe",
never "secured"), **M5** the impact ceiling (claims capped by rung;
credentials/RCE handed to chain-architect as candidates, not asserted).

## 2. Procedure — Numbered Actions

1. Entry: hypothesis pre-registered (URL-shaped parameter + suspected
   fetch sink, from the api-surface-mapper parameter taxonomy).
2. **Canary round-trip** (channel existence): treatment = parameter set to
   the operator interaction-host URL carrying the canary marker; control =
   same request with a garbage scheme/invalid URL of identical length.
   Delta = the callback arriving WITH the marker, per the operator's
   interaction-host log, recorded as a CANARY ledger record.
3. **Scheme matrix** (egress): the canary URL re-issued per scheme and
   shape — `http`, `https`, scheme-less, userinfo tricks (`http://user@host`),
   and redirect-chain variants (canary URL that 30x's to a second canary
   path). Probe bytes come from `references/corpus.json`: the loopback
   name family (SSRF-012), the IPv6 bracket family (SSRF-011), odd IP
   notations (SSRF-003), userinfo/parser confusion (SSRF-009) — scheme-less
   stays a labeled derivation row until a sourced entry exists. One
   request each; every callback is a CANARY record.
4. **Redirect tracing:** whether the fetch follows redirects determines
   whether an attacker-controlled redirector reaches internal space; the
   probe is the operator's redirector, never a third party's.
5. **Metadata checks only under explicit cloud scope:** the engagement's
   scope row must name the platform AND permit internal-address probing
   before any metadata-path request runs; otherwise this step is parked
   with a note (the gate is policy, the parking is honesty).
6. **Bounded internal reach:** at most a small set of named, hypothesized
   internal services (from evidence: error messages, config artifacts,
   response headers) — one request each, markers where possible. No sweeps.
7. Impact synthesis: channel existence + egress summary + (if authorized)
   one metadata canary read, bounded; severity follows the spine's ladder.
8. Exit gate: canary round-trip verdict, scheme matrix table, redirect
   verdict, scope-status of the internal step, closures citing records.

## 3. Hard Rules (mechanically enforced)

1. **Canary markers only** for channel proofs — third-party URLs as test
   payloads are refused by this organ's procedure; the ledger's CANARY
   tag is the audit trail.
2. **No internal sweeps.** Named, evidence-derived addresses only.
3. **Metadata requires named scope.** The scope row text is quoted in the
   ledger note before the first metadata request.
4. **One request per cell.** Repeat requests only when closing a timing-
   dependent hypothesis, with floors per the spine.

## 4. Tool Routing

| When | Tool |
| --- | --- |
| Treatment/control requests | `http_probe` (EXPERIMENT/CONTROL/CANARY tags) |
| Operator interaction-host setup | operator-owned; full procedure in `references/canary-callback.md` |
| Recording callbacks (from operator log) | `ledger_append` (CANARY) |
| Registering URL-fetch surfaces | `dossier_add` (surface-cartographer) |

## 5. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Setting up the callback host / interpreting callbacks | `references/canary-callback.md` |
| Exact bypass payloads (scheme handlers, IP notations, IPv6 and loopback name families, redirect/rebinding, cloud metadata endpoints, parser confusion), per-technique failure modes, primary sources | `references/corpus.json` (versioned payload corpus) |
| Grading the callback habit, running the ladder and map, capping impact | `references/method-upgrade.md` |

The corpus is versioned (`corpus_version`) and every entry carries its
primary source and its **failure modes** — read them before closing any
hypothesis as negative: a bypass that failed for a documented reason
(resolve-then-validate normalization, per-hop checks, IMDSv2 tokens)
leaves the filter untested, not effective. The canary entry (SSRF-010)
routes every channel proof through the operator's declared collector
(`http_probe` canary mode).
