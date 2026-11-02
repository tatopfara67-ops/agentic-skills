---
name: xss-playbook
version: 2.0.0
type: ai-skill
architecture: package
description: Phase-3 XSS organ, upgraded (v2) with the Mario Heiderich (Cure53) lineage — sink-context analysis first (HTML body, attribute, JS string, URL, with CSP factored), context-aware payload grammar, execution proofs by self-owned canary marker instead of alert() theater, and the mXSS layer: re-derive context after DOM mutations, the mXSS class catalog (re-serialization, namespace confusion, parsing-context switch), DOM clobbering as a pseudo-source, and sanitizer version-pinning as a ledgered fact. Use when the operator asks to test reflected or stored XSS, analyze a sink context, draft context-safe payloads, check CSP impact, or trace DOM source-to-sink flows ("tes XSS", "reflected", "stored", "DOM XSS", "sink context", "CSP bypass check", "payload untuk konteks ini", "mXSS", "mutation XSS", "sanitizer bypass", "DOM clobbering").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: v2 — Mario Heiderich (Cure53; the mXSS research line — mutation between sanitization and re-parse is the vulnerability)
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# xss-playbook v2.0.0 — Context First, Marker Always, Mutation Counts

## 0. What This Skill Is — and Is Not

* **Is**: the organ that classifies the sink context BEFORE choosing a
  payload grammar, proves execution with a canary marker the operator owns,
  and treats CSP as a measured fact, not a vibe.
* **Is not**: a payload dictionary. Payloads without a classified context
  are recombination noise; the context decides the grammar (and usually
  the shortest proof). Since v2 it carries the **Mario Heiderich
  lineage** as its field-guide layer — the mutation class of bugs that
  live BETWEEN sanitization and re-parse, where context analysis alone
  goes blind.

## 1. Inherited Contracts

Plugs into **Phase 3** of the mythos-bug-hunter spine. Inherits hypothesis
grammar (a payload exists only after the mechanism hypothesis cites the
sink-context record), experiment contract, closure vocabulary, and the
canary doctrine: execution proof = the page performing an observable
action with OUR marker (`MYTHOS-CANARY-<uuid>`), never `alert()` theater,
never third-party resources, never other users' sessions.

## 2. The Lineage Layer (v2 — the Heiderich doctrine)

**Mario Heiderich** — Cure53 founder, the mXSS research line ("mXSS
attacks", ACM WPES 2013; "Attacking well-secured Web-Applications by
using innerHTML"; the 2024 mXSS revival talks). v2 folds the lineage in
as five field rules, applied inside the procedure (§3) and detailed in
`references/mxss-and-clobber.md`:

1. **Context is not stable.** After ANY DOM mutation of attacker-
   relevant data, re-derive the sink context before refining the payload
   — the mutation, not the payload, is the vulnerability.
2. **One minimal differential per mutation class** (re-serialization,
   namespace confusion, parsing-context switch); the mutated bytes are
   the artifact.
3. **Clobber keys are harvested, not sprayed.** id/name collisions with
   `window.*`/`document.*` are their own hypothesis class and chain
   input.
4. **Sanitizer name+version is a ledgered FACT.** Sanitizers regress;
   a stale version is itself a reportable hygiene fact.
5. **The marker proof still decides.** mXSS earns severity through the
   chain it enables (spine §8; chain-architect input), not drama.

## 3. Procedure — Numbered Actions

1. Entry: reflection/storage hypothesis pre-registered, citing the
   parameter record and the observed reflection record.
2. **Classify the sink context** per `references/contexts.md`: element
   text, attribute (which attribute: value/href/style/event), JS string
   literal, JS code position, URL context, comment context, or DOM sink
   (innerHTML/document.write/eval family — the sink list lives in the
   reference). Record the classification with its evidence. When the sink
   is a mutation-capable host (innerHTML round-trip, template rendering,
   foreignObject), the v2 mutation pass applies BEFORE grammar refinement
   (`references/mxss-and-clobber.md`).
3. **CSP as a FACT:** record the CSP header (or its absence) on the
   response carrying the sink. The policy's script-src shape determines
   which proof channels exist; a strict-CSP context may cap the impact
   story at HTML injection unless a bypass hypothesis exists.
4. **Grammar selection** from the reference: the minimal payload family
   for the classified context, marker-carrying (e.g. the marker as an
   id/name attribute value plus the execution primitive for that context).
5. **Differential:** baseline (benign value of the same length/charset),
   treatment (payload), control (same payload shape with the grammar's
   active characters neutralized). Delta = marker-action observed in the
   rendered DOM only under treatment — observed how? A self-owned
   execution proof: the marker element landing in the DOM with the
   attribute the grammar targets, or `console`-side marker assignment,
   captured by the operator's browser session. The observation record
   cites the artifact (screenshot/DOM snippet saved by the operator).
6. **Stored XSS:** same grammar; the storage round-trip and the rendering
   surface are separate records; self-owned profile storage only.
7. **DOM XSS:** trace source-to-sink from the js-recon artifacts (source
   list: location properties, postMessage, name; sink list in the
   reference); the hypothesis cites BOTH endpoints of the flow with
   line-level evidence from the bundle artifact. DOM-clobber candidates
   (id/name harvesting, §2 rule 3) are checked as their own hypothesis
   family.
8. Impact synthesis: execution primitive + CSP verdict + reach (self page
   only vs stored-everywhere) — with the canary attestation and bounded
   scope statement.
9. Exit gate: every closure cites context classification, CSP fact,
   baseline/treatment/control records, and the marker observation; mXSS-
   class closures additionally cite the mutated-bytes artifact and the
   sanitizer version fact.

## 4. Hard Rules (mechanically enforced)

1. **No context, no payload.** The first XSS-shaped treatment request must
   follow a sink-context record — ledger order is auditable.
2. **Marker proofs only.** `alert(1)` closes nothing here; the canary
   marker in the observed outcome is the closure evidence.
3. **Self-owned storage and sessions.** Stored-XSS rendering is checked in
   the operator's own session; no other user is involved in a proof.
4. **CSP verdicts cite the header record**, including the no-CSP case
   (recorded as an observed absence).
5. **Mutation-class closures cite the mutated bytes** (v2) — a mutation
   claim without the round-trip artifact closes nothing.

## 5. Tool Routing

| When | Tool |
| --- | --- |
| Baseline/treatment/control requests | `http_probe` (EXPERIMENT/CONTROL) |
| Bundle source-to-sink tracing | `js_analyze` artifacts (js-recon organ) |
| Recording marker observations | `ledger_append` (CANARY, citing operator-captured artifact) |
| Registering sink surfaces | `dossier_add` (surface-cartographer) |

## 6. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Classifying a sink / choosing the grammar | `references/contexts.md` |
| Mutation-capable sink, sanitizer output executing, framework "safe" API | `references/mxss-and-clobber.md` |
| Citing the lineage artifacts behind the v2 layer | `references/sources.md` |
