---
name: api-surface-mapper
version: 1.0.0
type: ai-skill
architecture: package
description: Phase-1/2 API discovery organ — bounded sweeps for openapi/swagger/graphql documentation, spec parsing into a method-by-method endpoint inventory, version-diffing (v1 vs v2), and undocumented-endpoint detection by spec-vs-JS cross-reference. Use when the operator asks to map an API, find the API docs, inventory endpoints and parameters, check GraphQL introspection, or diff API versions ("cari API", "endpoint inventory", "openapi", "graphql introspection", "api versioning", "undocumented endpoint").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# api-surface-mapper v1.0.0 — The Spec Is Half the Map

## 0. What This Skill Is — and Is Not

* **Is**: the organ that turns "there is an API somewhere" into a
  parameter-level inventory: every documented method, every version, every
  undocumented endpoint the JS reveals but the spec omits.
* **Is not**: an API fuzzer. It discovers and inventories; testing belongs
  to Phase 3 organs (injection-lab, auth-boundary-mapper).

## 1. Inherited Contracts

Plugs into **Phase 1** (inventory) and **Phase 2** (hypothesis sources) of
the mythos-bug-hunter spine. Inherits the Canon, ledger discipline, R5
(spec output is a map, not a verdict — endpoints still need probe records).

## 2. Procedure — Numbered Actions

1. Entry: AUTH record present; base URL in scope.
2. `api_introspect(program, base)` — the bounded documentation sweep
   (openapi/swagger/api-docs/graphql endpoints + one read-only GraphQL
   introspection POST). Spec bodies land as artifacts; paths are extracted
   and returned compactly.
3. Parse the inventory per endpoint: method, path, parameters (name, type,
   required), auth marking. The schema of the inventory table and the
   parameter taxonomy are in `references/discovery-endpoints.md`.
4. **Version diff.** Probe sibling versions seen in evidence (`/api/v1`,
   `/v2`, `/v0`): endpoints present in an old version but absent from the
   current spec are `deprecated-endpoint` candidates — the highest-yield
   variant-analysis shape in API work.
5. **Spec-vs-JS cross-reference.** Endpoints the js-recon organ extracted
   that NO spec documents are undocumented surfaces: `api-rest` class,
   priority +10, note "undocumented: absent from spec, present in client".
6. GraphQL specifics (introspection grammar, depth-limited queries, type
   inventory) follow `references/graphql.md`. Introspection-disabled does
   not end the organ: schema hints from JS (query strings, persisted query
   ids) still feed the inventory as hypotheses.
7. `dossier_add` every endpoint-method pair with evidence citations (spec
   artifact record + probe record).
8. Exit gate: numbers stated — specs found, endpoints documented,
   versions probed, deprecated candidates, undocumented endpoints,
   introspection verdict.

## 3. Hard Rules (mechanically enforced)

1. **Read-only discovery.** GET/OPTIONS plus the single introspection
   POST; nothing mutates during inventory.
2. **Bounded sweep.** The doc-endpoint list is fixed and short; no
   speculative path churn in this organ.
3. **Spec entries still need probe records** for reachability before they
   become dossier surfaces (R5).
4. **Parameter inventory cites the artifact** (the saved spec), not memory.

## 4. Tool Routing

| When | Tool |
| --- | --- |
| Documentation sweep + spec parsing | `api_introspect` |
| Endpoint/version liveness probes | `http_probe` |
| Cross-reference source | `js_analyze` (js-recon organ) |
| Registering endpoint surfaces | `dossier_add` (surface-cartographer) |

## 5. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Building the endpoint inventory table | `references/discovery-endpoints.md` |
| A GraphQL endpoint appears | `references/graphql.md` |
