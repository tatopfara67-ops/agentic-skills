---
name: desync-hunter
version: 1.4.0
type: ai-skill
architecture: package
description: >-
  Legend-tier organ (Tier S — the Logic Architects) built from the James
  Kettle / PortSwigger lineage — protocol & specification asymmetry analysis.
  Treats every protocol specification as a hypothesis, inventories the parsing
  chain (CDN/WAF/HTTP2-terminator/backend), and hunts the disagreements
  between front-end and back-end parsers via manually-crafted ambiguous
  requests (CL/TE conflicts, header-name oddities, absolute-form, obs-fold),
  confirmed by time-based and response-class differentials with raw bytes as
  artifacts. Since v1.3.0 the organ carries the executable method layer (A16):
  a mechanical critique of the published art's floors (Burp-centric delivery,
  probe-first map-later, timing-oracle habit, single-shot narrative, borrowed
  victims) and their fixes as protocol M1–M4 — the CHAINMAP record schema with
  per-hop version evidence, the parser-pair × ambiguity-class selection
  matrix, the interleaved differential confirmation rule (n ≥ 5,
  response-class buckets, control with one restoring byte), and the escalation
  ladder with canary-marked operator-owned victims and a mandatory ceiling
  statement. Use when testing without a scanner against proxy chains, when
  hunting request smuggling or desync, when documentation says the system
  works one way and you need to force input the other way, or when classifying
  parser asymmetries ("request smuggling", "CL.TE", "desync", "protocol
  asymmetry", "parser differential", "manipulasi HTTP header", "smuggling").
category: security/legend-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: James Kettle (albinowax, PortSwigger Web Security Research — HTTP request smuggling, browser-powered desync, HTTP/2)
  tier: S — The Logic Architect & Reverse Engineers
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; targets whose scope explicitly covers the infrastructure/proxy layer
---

# desync-hunter v1.4.0 — The Spec Is A Hypothesis

## 0. What This Skill Is — and Is Not

* **Is**: the organ for the gap between what the documentation
  promises and what the parsers actually do. Its unit of work is the
  SEAM: any place two components both parse the same bytes (frontend
  vs backend, HTTP/2 terminator vs HTTP/1.1 origin, browser vs cache)
  — where a crafted ambiguity makes them disagree.
* **Is not**: a raw-socket spray tool. Ambiguities are designed from
  the parsing-chain map, sent in ones, and confirmed by differential
  evidence. It does not borrow Kettle's Burp-only tooling; the
  doctrine is the method, executable with one-request-at-a-time
  discipline.

## 1. Inherited Contracts

Plugs into **Phase 2** (parsing-chain hypotheses) and **Phase 3**
(experiments) of the mythos-bug-hunter spine. Inherits the experiment
contract (§6 — response-class AND timing evidence, n_runs floors),
the canary doctrine (§8 — victim sessions in poisoning proofs are
operator-owned accounts), and effort budgets (R7). Adjacent organs:
signal-smith supplies encoding-level craft for ambiguous headers;
chain-architect composes desync primitives into chains; packet-orchestrator
governs any raw-socket automation (manual trace first).

## 2. The Lineage (attribution)

**James Kettle** (PortSwigger Web Security Research lead, publishing
as albinowax) built the modern discipline this organ distills: "HTTP
Desync Attacks" / request smuggling research (Black Hat USA 2019 and
the PortSwigger research series), browser-powered desync, HTTP/2
desync ("The Sequel Is Always Worse", Black Hat USA 2021), and web
cache deception. The core of the lineage is the posture: RE-READ the
specification, assume implementations disagree, and design the exact
input where they do. Distilled as decision logic only — no
PortSwigger or Burp content is embedded. The verification record is
`references/sources.md`.

## 2.5 First Principles — the WWH registers (A14)

* **WHAT** — a parsing-chain disagreement: two components (frontend
  vs backend, HTTP/2 terminator vs HTTP/1.1 origin, browser vs cache)
  both parse the same bytes and reach different conclusions about
  where the message ends and the next one begins. The unit is the
  SEAM — the boundary between adjacent parsers — and the bug class
  is CL/TE and its siblings: any byte sequence whose framing verdict
  differs across the chain.
* **WHY** — HTTP has no single parser: the spec is prose read by
  many implementers, each resolving ambiguity with its own state
  machine (and its own legacy of lenient clients it must keep
  serving). Two correct-enough parsers can disagree about edge
  inputs precisely BECAUSE both are tolerating something. That is
  the root cause — ambiguity tolerated twice, differently — and it
  is why the class renews with every protocol generation (HTTP/2,
  HTTP/3): new framing, same division of interpretive labor.
* **HOW** — map the parsers (with versions) BEFORE any payload;
  design each request to isolate ONE ambiguity; send it once; read
  the delta as response-class AND timing, where timing is only a
  lead that graduates to a response-class differential; ship the
  exact bytes as the artifact. Poisoning demonstrations run on
  operator-owned accounts only.

War note (A15): the cheng sweep is the known seam catalog (CL+TE,
duplicate CL, obs-fold, absolute-form) against the mapped chain; the
ch'i is the seam PAIR only this stack joins — the version combination
whose disagreement nobody has submitted. W1 binds before anything:
the chain map with versions is the spies' report, written before the
first crafted byte. W2 in its purest form: the smuggled request that
lands in the backend queue and is READ from it is the proof — the
victimless differential — never the poisoned production response.

## 3. Doctrine — How Kettle-Thinking Runs

1. **The spec is a hypothesis.** If the documentation says the system
   behaves way A, the experiment is: force input shaped for way B and
   observe. Disagreement is not an error to report to the vendor —
   it is the finding class.
2. **Map the parsers before the payloads.** Which boxes touch the
   bytes: browser, CDN, WAF, HTTP/2 terminator, load balancer, cache,
   origin? Every pair of adjacent parsers is a candidate seam; the
   chain map (with versions, from response headers) is a FACT record.
3. **One ambiguity, one request.** Each crafted request isolates ONE
   disagreement (CL+TE, duplicate CL, odd header name, obs-fold,
   absolute-form, non-standard method, content-type mismatch). Batch
   sprays destroy attribution of which ambiguity moved the delta.
4. **Timing is an oracle, not a proof.** A stalled/desynced response
   time indicates the backend held the connection open — a LEAD that
   must graduate to a response-class differential before CONFIRMED.
5. **Bytes are the evidence.** A desync claim ships with the exact
   request bytes (artifact) and the exact divergent responses
   (artifacts); "it hung a bit" is not a finding.
6. **The victim is always you.** Any poisoning demonstration
   (request capture, cache poisoning affecting a victim fetch) runs
   with operator-owned accounts and operator-controlled fetches.

## 3.5 The Method Layer — Critique, Upgrade, M1–M4 (A16)

A lineage named is not expertise delivered. The published art is
told through Burp verbs and one-shot narratives — documented floors,
not heresy. `references/method-upgrade.md` grades each floor (W1–W5)
and ships the executable replacement:

* **M1 CHAINMAP** — one FACT record per hop with product VERSION and
  its evidence (ordered headers, ALPN negotiation, absolute-form
  acceptance, error-page ownership). "nginx" is not
  "nginx/1.24.0"; the matrix keys on the pair of versions.
* **M2 selection matrix** — parser pair × ambiguity class, with
  preconditions and the FIRST probe by corpus ID. A class without a
  matching pair row is a refused request, not a shot.
* **M3 differential protocol** — baseline / treatment / control,
  n ≥ 5 each, INTERLEAVED; response-class buckets; the three-part
  confirm rule; timing as escalation only, thresholds pre-registered
  (median deltas vs 3 × baseline IQR), single shots never reported.
* **M4 escalation ladder** — error-echo → response-class → short
  timing → long timing → poisoning demo with canary-marked
  operator-owned victim; each step entered only on the previous
  one's recorded inconclusive. The report carries a mandatory
  ceiling statement: which level was actually reached.

Probes come byte-exact from `references/corpus.json` — never
hand-typed, never from memory. Doctrine (§3) states the posture;
M1–M4 make it executable.

## 3.6 The Operator Layer (A17) — the James Kettle runtime

`references/operator-os.md` ships the figure's documented psychology
as the agent's RUNTIME, in four parts: the thinking framework (numbered
if-then decision rules, each citing the documented behavior it
distills), the behavioral protocol (situation → move → agent action →
refusal, with pacing and failure-reaction rules — how the agent acts
and behaves while hunting), the scripting arsenal (the organ's core
techniques as exact, tool-agnostic commands and micro-scripts, each
with its read-out and decision gate), and the rigid run-order binding
rules, behavior, and scripts onto the M-protocol above. Load it when
the hunt runs: the doctrine states the posture, the M-protocol states
the procedure — the operator OS is how the agent BEHAVES while
executing, characteristic of James Kettle.

## 4. Procedure — Numbered Actions

1. Map the parsing chain: one `http_probe` per infrastructure
   identifier (Server, Via, X-Powered-By, cache headers) — the chain
   map with versions is a FACT record set; the seam inventory
   follows from it.
2. Baseline the chain's NORMAL behavior: three canonical requests
   (GET /, HEAD /, POST with body) — response classes and timing
   baselines recorded.
3. Design one ambiguity per hypothesis (pre-registered EXPERIMENT):
   predicted frontend interpretation vs predicted backend
   interpretation, and the observable that would distinguish them.
   The ambiguity catalog and grammar is
   `references/asymmetry-catalog.md`.
4. Send the ambiguous request via `http_probe` with exact raw
   headers; capture response class, timing, and body hash as
   artifacts. Rate floor: one ambiguity per 10 seconds — WAF-hostile
   targets get the ghost-crawler posture, not volume.
5. Confirm via the differential triad: baseline (canonical request),
   treatment (ambiguous request), control (the same ambiguity minus
   ONE byte that restores agreement — proves the ambiguity itself,
   not the connection, caused the delta). n_runs ≥ 2 with stable
   deltas; timing-only observations stay LEADs.
6. Classify the seam: CL.TE, TE.CL, TE.TE, duplicate-CL, H2.CL,
   H2.TE, header-name normalization, absolute-form/authority
   confusion, cache-key vs body divergence. State which parser
   versions disagreed (from the chain map).
7. Impact, bounded: demonstrate ONE of — smuggled canary request
   reaching the origin (self-marked distinctive path), poisoning a
   cache entry fetched next by an operator-owned session, or
   capturing a request from an operator-owned "victim" session.
   Then stop.
8. Exit gate: seams inventoried, ambiguities tested (by class),
   differentials confirmed with byte artifacts, impact proof type
   stated, every claim citing records; unexplored ambiguity classes
   parked with a resume note.

## 5. Hard Rules (mechanically enforced)

1. **No real-user traffic as victim.** Poisoning proofs use
   operator-owned sessions and fetches only; a report line about
   other users' requests requires it be the LEAD of an operator
   decision, never an agent action.
2. **Bytes or it did not happen.** Every desync finding cites
   artifacts containing the exact request bytes and both responses.
3. **One ambiguity per request.** Composite ambiguities are separate
   hypotheses, not one clever payload.
4. **Timing alone never CONFIRMs.** A timing delta is a LEAD that
   must graduate to a response-class differential.
5. **Scope covers the seam.** The infrastructure layer (CDN/WAF/LB)
   must be inside program scope before ambiguity probes — a
   web-app-only scope does not authorize parser probing of the
   tenant's shared edge (R0 applies to the SEAM's owner, not just
   the app's domain).

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Chain map + baselines + ambiguous requests | `http_probe` (exact raw headers) |
| Timing oracles | `http_probe` note field + artifacts (wall-clock stated) |
| Raw sockets / HTTP/2 specific framing | spine micro-script doctrine + packet-orchestrator (manual trace first) |
| Encoding-level header craft | signal-smith organ (its encoding-grammar module) |
| Records | `ledger_append` (EXPERIMENT/CONTROL/CANARY) |
| Classification at report time | `cvss3_score` + `vrt_classify` |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Choosing/designing an ambiguity | `references/asymmetry-catalog.md` |
| Grading the published method, building the CHAINMAP, running the selection matrix and differential protocol | `references/method-upgrade.md` |
| Running the hunt — the James Kettle runtime: thinking rules, situation-to-action behavior, scripting, rigid run-order | references/operator-os.md |
| Exact probe bytes (CL.TE/TE.CL differential + timeout probes, TE.TE obfuscations, H2.CL), per-technique failure modes, primary sources | `references/corpus.json` (versioned payload corpus) |
| Verifying the Kettle lineage and sources | `references/sources.md` |

The corpus is versioned (`corpus_version`) and every entry carries its
primary source and its **failure modes** — read them before closing any
hypothesis as negative: a probe that failed for a documented reason
(intermediary re-framing, per-request connections, refusal posture)
leaves the seam untested, not disproven.
