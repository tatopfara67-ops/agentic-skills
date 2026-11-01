---
name: auth-boundary-mapper
version: 2.0.0
type: ai-skill
architecture: package
description: Phase-2/3 access-control organ, upgraded (v2) with the Frans Rosen lineage — builds the role-by-resource authorization matrix from evidence, then runs systematic IDOR/BOLA differentials (baseline own-object, treatment cross-object, control nonexistent-object) with two operator-provided test accounts; v2 adds the IDOR field-guide layer — identifier-construction analysis before any swap, swap testing across ALL parameter positions, 2nd-order IDOR sweeps, full response-body diffing, cloud multi-tenant boundary emphasis, and non-obvious verb coverage (PATCH, bulk, export tokens). Use when the operator asks to test IDOR or BOLA, map who can access what, probe horizontal/vertical privilege boundaries, audit access control on an API, or audit cloud multi-tenant isolation ("tes IDOR", "BOLA", "akses kontrol", "privilege boundary", "role matrix", "broken access control", "2nd-order IDOR", "tenant isolation").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: v2 — Frans Rosen (Detectify co-founder; IDOR-through-methodology lineage: identifier construction, 2nd-order IDOR, response-diff rigor)
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; two operator-owned test accounts
---

# auth-boundary-mapper v2.0.0 — The Matrix Before The Hunt

## 0. What This Skill Is — and Is Not

* **Is**: the organ that replaces "let me try some IDs" with a matrix: every
  (role × resource × action) cell probed by a differential whose baseline,
  treatment, and control are three separate ledgered requests. Since v2 it
  carries the **Frans Rosen lineage** as its field-guide layer — the craft
  that made IDOR a repeatable discipline rather than parameter luck.
* **Is not**: a credential abuse tool. It runs on operator-provided test
  accounts, on self-owned data, inside scope — or it does not run.

## 1. Inherited Contracts

Plugs into **Phase 2** (matrix as hypothesis source) and **Phase 3**
(differential experiments) of the mythos-bug-hunter spine. Inherits the
full experiment contract (§6: baseline/treatment/control/n_runs/delta),
closure vocabulary (§7), and the canary doctrine (§8: cross-object tests
use SELF-OWNED objects — account B reading account A's object where both
belong to the operator). Inter-system trust edges belong to
trust-graph-hunter (v2 boundary clarification); role×resource INSIDE one
system stays here.

## 2. The Lineage Layer (v2 — the Frans Rosen doctrine)

**Frans Rosen** — Detectify co-founder, consistently top-ranked bug bounty
hunter — is the public archetype of IDOR as a *methodology*: attack modern
web technologies by studying how object references are CONSTRUCTED and
CONSUMED, not by spraying identifier values ("Attacking Modern Web
Technologies"; the 2nd-order IDOR keynote material; his IDOR writeup
series). v2 folds the lineage in as five field rules, applied inside the
matrix procedure (§4) and detailed in `references/idor-field-guide.md`:

1. **Analyze the identifier BEFORE swapping it.** How the id is built
   (sequential int, UUID, GUID-with-embedded-timestamp, username/email,
   org-prefixed composite) decides the swap strategy and the blast-radius
   argument.
2. **Swap in every parameter position.** Access checks are frequently
   per-position: the same object reachable via path, query, body, and
   header — checked in some, decorative in others.
3. **Hunt 2nd-order IDOR.** References created/validated in one request
   and consumed in a LATER feature (invites, exports, email-linked
   actions) leak across tenants where the direct swap is clean.
4. **Diff the full response.** Status codes lie; bodies do not — 200-with-
   different-body-shape is the signature of partial authorization.
5. **Cloud tenant = object boundary.** In multi-tenant SaaS, the tenant
   context (org_id, region, sub) is a dimension of the matrix, not
   ambient background.

The attribution record (with the operator-brief spelling correction) is
in `references/idor-field-guide.md` §5.

## 3. Preconditions (hard)

1. AUTH record present; target in scope.
2. Two operator-owned test accounts: A (low privilege) and B (different
   role/tenant — the more different, the sharper the matrix).
3. Each account owns at least one object of every resource type under test
   (created by the operator, before any probe).
4. Sessions/tokens for both accounts are recorded as FACT records (kind,
   transport: cookie/header/both) — session semantics ARE the boundary
   under study.

## 4. Procedure — Numbered Actions

1. Build the matrix skeleton from the api-surface-mapper inventory:
   rows = resource types × object instances (A-owned, B-owned), columns =
   actions (read/update/delete/list), cells = (role, expected-verdict).
   The matrix template and verdict grammar are in `references/matrix.md`.
2. **Identifier-construction pass (v2)** — for every resource id in the
   matrix, record its construction class and swap strategy per
   `references/idor-field-guide.md` §1-2 BEFORE any swap runs.
3. **Baseline round** — each account touches its OWN objects. Expected
   verdicts become the "world as it is" records.
4. **Treatment round** — account B requests A-owned objects (parameter
   swap: id, uuid, path segment, tenant header). One request per cell;
   v2: the swap runs in EVERY parameter position the surface exposes
   (path/query/body/header) — each position is its own cell.
5. **Control round** — same request shape against a nonexistent object id
   (same effort, wrong knob): separates "access granted" from "error
   handling that never checks".
6. **Response-body diff (v2 rigor)** — every granted treatment diffs the
   FULL response body (hash + shape) against the A-owned baseline
   artifact; 200-with-swapped-label is recorded as a false-positive
   near-miss, not a finding.
7. Delta analysis per cell: granted-to-B-reading-A is a boundary violation
   candidate ONLY when the baseline says A's own access works and the
   control says the id-space check exists (or its absence is itself
   recorded). Close per the spine's three-state vocabulary.
8. Vertical slice: repeat the treatment round with B hitting
   admin-marked endpoints (admin-console surfaces from the dossier).
9. **2nd-order sweep (v2)** — for invite/export/share/report-generation
   flows, re-run the reference through the SECOND feature that consumes
   it (the guide's §3): the differential pair is (create-then-consume
   cross-tenant) vs (create-then-consume own-tenant).
10. **Cloud tenant slice (v2)** — in multi-tenant targets, add the tenant
   context dimension (org_id/region/sub header) to the treatment round;
   cross-tenant verdicts follow the same triad discipline.
11. Record the matrix verdict table in the engagement; CONFIRMED cells feed
   Phase 4 impact synthesis with the canary ladder (bounded: read ONE
   self-owned cross-tenant object, stop).
12. Exit gate: matrix coverage numbers (cells probed, per round, per
   parameter position), identifier classes mapped, 2nd-order flows swept,
   closures by state, and every verdict citing its three records.

## 5. Hard Rules (mechanically enforced)

1. **Three records per cell** (baseline, treatment, control) before any
   closure — the auditor counts them per hypothesis.
2. **Self-owned objects only.** Cross-tenant tests use operator-owned
   accounts; real-user objects are never touched (R0 canary doctrine).
3. **No privilege escalation attempts against production roles** the
   operator does not own (no admin-account guessing — the matrix maps,
   the operator decides).
4. **Matrix before hunt.** The first IDOR-shaped hypothesis cites the
   matrix cell; drive-by parameter churn without a matrix is R1 slop.
5. **Full-body diff on every granted cell (v2).** A granted verdict
   without the body-hash comparison against baseline is a LEAD.

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Probing cells (with session headers) | `http_probe` |
| Recording matrix rounds | `ledger_append` (EXPERIMENT/CONTROL tags) |
| Endpoint inventory source | `api_introspect` + `js_analyze` outputs |
| Registering boundary surfaces | `dossier_add` (surface-cartographer) |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Building the matrix / verdict grammar | `references/matrix.md` |
| Identifier classes / swap positions / 2nd-order flows / tenant slices (the Rosen field guide) | `references/idor-field-guide.md` |
