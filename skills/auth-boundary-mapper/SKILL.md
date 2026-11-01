---
name: auth-boundary-mapper
version: 1.0.0
type: ai-skill
architecture: package
description: Phase-2/3 access-control organ — builds the role-by-resource authorization matrix from evidence, then runs systematic IDOR/BOLA differentials (baseline own-object, treatment cross-object, control nonexistent-object) with two operator-provided test accounts. Use when the operator asks to test IDOR or BOLA, map who can access what, probe horizontal/vertical privilege boundaries, or audit access control on an API ("tes IDOR", "BOLA", "akses kontrol", "privilege boundary", "role matrix", "broken access control").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; two operator-owned test accounts
---

# auth-boundary-mapper v1.0.0 — The Matrix Before The Hunt

## 0. What This Skill Is — and Is Not

* **Is**: the organ that replaces "let me try some IDs" with a matrix: every
  (role × resource × action) cell probed by a differential whose baseline,
  treatment, and control are three separate ledgered requests.
* **Is not**: a credential abuse tool. It runs on operator-provided test
  accounts, on self-owned data, inside scope — or it does not run.

## 1. Inherited Contracts

Plugs into **Phase 2** (matrix as hypothesis source) and **Phase 3**
(differential experiments) of the mythos-bug-hunter spine. Inherits the
full experiment contract (§6: baseline/treatment/control/n_runs/delta),
closure vocabulary (§7), and the canary doctrine (§8: cross-object tests
use SELF-OWNED objects — account B reading account A's object where both
belong to the operator).

## 2. Preconditions (hard)

1. AUTH record present; target in scope.
2. Two operator-owned test accounts: A (low privilege) and B (different
   role/tenant — the more different, the sharper the matrix).
3. Each account owns at least one object of every resource type under test
   (created by the operator, before any probe).
4. Sessions/tokens for both accounts are recorded as FACT records (kind,
   transport: cookie/header/both) — session semantics ARE the boundary
   under study.

## 3. Procedure — Numbered Actions

1. Build the matrix skeleton from the api-surface-mapper inventory:
   rows = resource types × object instances (A-owned, B-owned), columns =
   actions (read/update/delete/list), cells = (role, expected-verdict).
   The matrix template and verdict grammar are in `references/matrix.md`.
2. **Baseline round** — each account touches its OWN objects. Expected
   verdicts become the "world as it is" records.
3. **Treatment round** — account B requests A-owned objects (parameter
   swap: id, uuid, path segment, tenant header). One request per cell.
4. **Control round** — same request shape against a nonexistent object id
   (same effort, wrong knob): separates "access granted" from "error
   handling that never checks".
5. Delta analysis per cell: granted-to-B-reading-A is a boundary violation
   candidate ONLY when the baseline says A's own access works and the
   control says the id-space check exists (or its absence is itself
   recorded). Close per the spine's three-state vocabulary.
6. Vertical slice: repeat the treatment round with B hitting
   admin-marked endpoints (admin-console surfaces from the dossier).
7. Record the matrix verdict table in the engagement; CONFIRMED cells feed
   Phase 4 impact synthesis with the canary ladder (bounded: read ONE
   self-owned cross-tenant object, stop).
8. Exit gate: matrix coverage numbers (cells probed, per round), closures
   by state, and every verdict citing its three records.

## 4. Hard Rules (mechanically enforced)

1. **Three records per cell** (baseline, treatment, control) before any
   closure — the auditor counts them per hypothesis.
2. **Self-owned objects only.** Cross-tenant tests use operator-owned
   accounts; real-user objects are never touched (R0 canary doctrine).
3. **No privilege escalation attempts against production roles** the
   operator does not own (no admin-account guessing — the matrix maps,
   the operator decides).
4. **Matrix before hunt.** The first IDOR-shaped hypothesis cites the
   matrix cell; drive-by parameter churn without a matrix is R1 slop.

## 5. Tool Routing

| When | Tool |
| --- | --- |
| Probing cells (with session headers) | `http_probe` |
| Recording matrix rounds | `ledger_append` (EXPERIMENT/CONTROL tags) |
| Endpoint inventory source | `api_introspect` + `js_analyze` outputs |
| Registering boundary surfaces | `dossier_add` (surface-cartographer) |

## 6. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Building the matrix / verdict grammar | `references/matrix.md` |
