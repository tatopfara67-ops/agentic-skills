---
name: deep-teardown
version: 1.0.0
type: ai-skill
architecture: package
description: Legend-tier organ (Tier S — the Logic Architects) built from the George Hotz (geohot) lineage — dismantle-to-primitives reverse engineering. Acquires the client artifact once (JS bundle, mobile APK/IPA, desktop binary, firmware image within scope), then dissects it LOCALLY down its teardown ladder (deobfuscation, sourcemaps, dex-to-source, strings/symbols) to reconstruct business logic and map how the app handles tokens, keys, and PII on-device BEFORE anything is sent to the server; every server-relevant discovery becomes a bounded hypothesis, never a blind guess. Use when the operator wants the app taken apart rather than probed, when hunting hidden feature flags, admin-gated code shipped in clients, hardcoded internal endpoints, or client-side secret storage ("bongkar aplikasi", "decompile APK", "reverse engineer the client", "teardown", "analisa biner", "read the minified JS logic").
category: security/legend-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: George Hotz (geohot — first iPhone SIM unlock 2007, PS3 reverse engineering, blackra1n)
  tier: S — The Logic Architect & Reverse Engineers
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; artifacts acquired within program scope (store-published app, public bundle, in-scope download)
---

# deep-teardown v1.0.0 — Dismantle To Primitives

## 0. What This Skill Is — and Is Not

* **Is**: the organ that treats the shipped client as the most honest
  documentation the target ever published — then proves it wrong. One
  acquisition fetch; everything after that is LOCAL dissection of the
  artifact down the teardown ladder, mapping logic and local data
  handling (tokens, keys, PII) before a single byte reaches the
  server.
* **Is not**: dynamic instrumentation of a live target, and not a
  secret-extraction service (secrets policy inherited verbatim:
  masked, report-only, never used). Client-side findings are
  HYPOTHESES until a server-side differential confirms them (R5).

## 1. Inherited Contracts

Plugs into **Phase 1/2** (artifact acquisition + logic maps feeding
hypotheses) and **Phase 3** (bounded verification probes) of the
mythos-bug-hunter spine. Inherits R5 (artifact output is a
hypothesis, each endpoint needs its own probe record), the secrets
policy (masked in context, full values only in on-disk artifacts),
and effort budgets (R7 — the ladder descends only as far as the
hypothesis requires). Adjacent organs: js-recon inventories web
bundles (this organ goes DEEPER on logic); chain-architect consumes
discovered internal endpoints as primitives.

## 2. The Lineage (attribution)

**George Hotz** (geohot) is the public archetype of teardown-first
thinking: at 17, the first reported iPhone SIM unlock (August 2007) —
accomplished by dismantling the device's software stack to its
primitives rather than waiting for someone else's tool; the
PlayStation 3 reverse-engineering era (and the Sony lawsuit that
followed); blackra1n (2009); later comma.ai and tinygrad. The
posture distilled: read the actual code/bytes instead of the docs,
understand how the system really manages its data at the lowest
level you can reach, and let the primitives tell you where the
design bends. No exploit, code, or method specific to his targets is
embedded — only the posture, applied to authorized client artifacts.
The verification record is `references/sources.md`.

## 3. Doctrine — How Hotz-Thinking Runs

1. **The artifact is the spec.** Marketing pages lie, API docs rot,
   the shipped binary tells the truth: what endpoints exist, what
   checks the client performs, what it stores, what it trusts.
2. **One acquisition, then silence.** Download the artifact once
   (store page, public URL, in-scope download); all work happens
   against the local copy. Re-downloading needs a ledgered reason.
3. **Descend the ladder only as needed.** Each layer of the teardown
   ladder answers specific hypothesis classes; going deeper costs
   budget — stop when the question is answered.
4. **Local data flow before network flow.** Map where tokens/keys/PII
   live on-device (storage, prefs, keychain, plaintext, memory) and
   what transforms precede transmission — the client's handling IS
   a trust-boundary statement by the vendor.
5. **Client logic is a hypothesis about server logic.** A disabled
   check, an admin flag, a debug stub in the client says the server
   MIGHT also trust it — the finding is only CONFIRMED by the
   server's own differential response.

## 4. Procedure — Numbered Actions

1. Acquire the artifact inside scope: public store APK (in-scope
   mobile program), the already-fetched JS bundles of Phase 1, an
   in-scope desktop installer. One FACT record with the artifact
   hash and acquisition source.
2. Inventory the artifact at layer 0: file tree, formats, signature,
   permissions requested — the map that decides which ladder to
   climb (`references/teardown-ladder.md`).
3. Climb the ladder per hypothesis class:
   * JS: deobfuscate/unminify, reconstruct module graph, read the
     business logic and the feature-flag branch conditions.
   * APK/IPA: unpack, dex→source (jadx-class tooling), read
     manifest, services, and the network layer's real endpoint list.
   * Binaries/firmware: strings, symbols, packed sections, config
     extraction.
4. Extract the four inventories, each as artifact-backed FACT
   records: (a) full endpoint list incl. internal/debug hosts;
   (b) client-side checks and flags (admin gates, feature flags,
   debug stubs); (c) local storage map of tokens/keys/PII with
   encryption status; (d) hardcoded values classified by the secrets
   policy (masked in context).
5. Convert each inventory entry into hypotheses: internal endpoint →
   reachability probe (ONLY if the endpoint's host is in scope);
   admin flag → differential probe of the gated route with/without
   the flag; plaintext local storage → report-grade finding with the
   storage path, no exfiltration.
6. Bounded verification: one `http_probe` per hypothesis, each with
   its baseline/control; client-side-only findings (local storage
   Plaintext) are reported as client findings with reproduction
   steps, no server differential needed.
7. Exit gate: artifact count + hashes, ladder depth reached, four
   inventories with counts, hypotheses generated, probes run,
   findings closed by state — numbers stated (R6).

## 5. Hard Rules (mechanically enforced)

1. **One acquisition per artifact.** Re-download needs a reason in
   the ledger note; analysis is local.
2. **Secrets stay masked.** Full values exist only in on-disk
   artifacts for the operator; never transmitted, never pasted into
   requests (inherited policy, verbatim).
3. **Client bypass ≠ server bug.** A client-disabled check is a
   hypothesis; only the server's differential response CONFIRMs
   (R5).
4. **Internal hosts are leads, not licenses.** Endpoints discovered
   in the artifact are probed only when their host is in scope —
   otherwise they are reported as exposure intel for the operator.
5. **Ladder depth is budgeted.** Going one layer deeper needs the
   hypothesis class that requires it, stated in the plan note (R7).

## 6. Tool Routing

| When | Tool |
| --- | --- |
| JS bundle inventory (shallow) | `js_analyze` (js-recon) |
| Deeper JS logic / APK / binary dissection | local tooling per `references/teardown-ladder.md`, outputs as artifacts |
| Verification probes of discovered endpoints | `http_probe` |
| Registering discovered surfaces | `dossier_add` (surface-cartographer) |
| Records | `ledger_append` (FACT/EXPERIMENT/CONTROL) |
| Endpoint primitives for chains | chain-architect |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Choosing the teardown path per artifact type | `references/teardown-ladder.md` |
| Verifying the Hotz lineage and sources | `references/sources.md` |
