---
name: js-recon
version: 1.0.0
type: ai-skill
architecture: package
description: Phase-1/2 JS recon organ — fetch JS bundles, extract endpoints and commented-out routes locally, flag secret-shaped strings (masked, report-only), and unpack sourcemap references. Use when the operator asks to analyze a target's JavaScript, find hidden API endpoints in bundles, hunt for exposed keys in JS, or diff old bundle versions ("analisa JS", "endpoint extraction", "cari endpoint di javascript", "source map", "secret di JS").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# js-recon v1.0.0 — The Bundle Is a Map

## 0. What This Skill Is — and Is Not

* **Is**: the organ that treats client-side JavaScript as what it is — a
  server API inventory the target accidentally published. One request fetches
  the bundle; all analysis happens locally against the artifact.
* **Is not**: a secret-extraction service. Secret-shaped strings are
  reported masked, for the operator. The pipeline never uses them (hard
  rule, mechanically enforced: the tool masks values in context and never
  transmits them anywhere).

## 1. Inherited Contracts

Plugs into **Phase 1** (bundle inventory) and **Phase 2** (endpoint
hypothesis sources) of the mythos-bug-hunter spine. Inherits the Canon,
ledger discipline, R5 (bundle output is a hypothesis about server behavior —
each endpoint needs its own probe record before it is a surface).

## 2. Procedure — Numbered Actions

1. Entry: AUTH record present; asset URL in scope.
2. Collect bundle URLs: `http_probe` the HTML entry points; parse
   `<script src>` and inline module references (the extraction catalog,
   including SPA chunk-graph walking, is in `references/extraction.md`).
3. `js_analyze(program, url)` per bundle. The tool saves the raw bundle as
   an artifact and returns: endpoints, commented-out routes, masked secret
   hints, sourcemap references — each with ledger records.
4. Probe every extracted endpoint ONCE (`http_probe`): existence and auth
   posture become SURFACE records. An endpoint in JS that 404s server-side
   is itself an observation (client/server drift — record it).
5. Commented-out routes are gold: they are `deprecated-endpoint` candidates
   the server may still mount. Probe them explicitly.
6. Sourcemap references (`sourceMappingURL=`) pointing at a `.map` that
   resolves: record as a `config-exposure` candidate — original sources on
   a production host. Fetch bounded (one map), save artifact, inventory file
   names only.
7. Secret hints follow `references/secrets-policy.md` verbatim: masked in
   context, report-only, never used, never pasted into requests.
8. `dossier_add` each live endpoint with evidence citations (the probe
   record, not the extraction record alone — extraction is a hypothesis).
9. Exit gate: numbers stated — bundles analyzed, endpoints extracted,
   endpoints live, commented routes, sourcemaps, secret hints (masked).

## 3. Hard Rules (mechanically enforced)

1. **One fetch per bundle.** Analysis is local. Re-fetching a bundle mid-
   engagement needs a reason in the ledger note.
2. **Secrets are report-only.** Masking happens inside the tool; the
   returned context physically cannot contain the full value.
3. **Extraction ≠ surface.** Only probe records justify dossier entries.
4. **Bodies stay out of context.** The tool returns counts and paths; raw
   bundle bytes live in artifacts (spine §3).

## 4. Tool Routing

| When | Tool |
| --- | --- |
| Fetch + local analysis of a bundle | `js_analyze` |
| Endpoint existence/auth posture probes | `http_probe` |
| Sourcemap bounded fetch | `http_probe` (the .map is a normal artifact) |
| Registering live endpoints | `dossier_add` (surface-cartographer) |

## 5. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Building the bundle list / walking a chunk graph | `references/extraction.md` |
| Any secret hint appears | `references/secrets-policy.md` |
