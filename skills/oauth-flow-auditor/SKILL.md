---
name: oauth-flow-auditor
version: 1.0.0
type: ai-skill
architecture: package
description: Phase-2/3 OAuth/OIDC flow organ — a check catalog (redirect_uri exact-match, state presence, PKCE, code reuse, token audience, implicit flow) where every check is a pre-registered hypothesis with its own falsifier, run as differentials against operator-owned IdP test apps. Use when the operator asks to audit an OAuth flow, test redirect_uri validation, check state/PKCE handling, probe code or token reuse, or review an OIDC client configuration ("tes oauth", "redirect_uri", "PKCE", "state missing", "code reuse", "token audience", "OIDC audit").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; operator-owned OAuth test app pair
---

# oauth-flow-auditor v1.0.0 — Flows Are State Machines; Test The Transitions

## 0. What This Skill Is — and Is Not

* **Is**: the organ that walks an OAuth/OIDC flow as a state machine and
  attacks each TRANSITION with a catalog check: every check has a grammar,
  a falsifier, and a differential — before it has a verdict.
* **Is not**: a token-fiddling playground. Tokens are operator-owned test
  artifacts; no third-party account is ever involved.

## 1. Inherited Contracts

Plugs into **Phase 2** (check catalog → hypotheses) and **Phase 3**
(differential experiments) of the mythos-bug-hunter spine. Inherits the
hypothesis grammar (§5), experiment contract (§6), closure vocabulary (§7),
and canary doctrine (§8: only self-injected markers cross boundaries).

## 2. Preconditions (hard)

1. AUTH record present; authorization server AND client callback host both
   in scope (the gate checks both — an out-of-scope callback host is a
   REFUSED record, and that refusal is itself reported).
2. An operator-owned test app registration (client_id under test) and a
   second one for cross-app confusion checks.
3. The flow transcript: each step of ONE happy-path run, ledgered as FACT
   records, BEFORE any check runs — the baseline state machine.

## 3. Procedure — Numbered Actions

1. Record the happy path: authorize request → redirect → callback → token
   exchange → resource access. One request per step, all FACT records.
2. Load the check catalog (`references/checks.md`) and map each check to
   the transition it attacks.
3. Pre-register one hypothesis per check, in the spine grammar, with the
   falsifier stated BEFORE the crafted request (retrodisction is discarded,
   spine §5).
4. Run each check as a differential: baseline (happy-path record from
   step 1) vs treatment (the check's crafted variant) vs control (same
   effort, unrelated knob — e.g. a garbage state value when testing
   redirect_uri).
5. Close each hypothesis in the three-state vocabulary; CONFIRMED checks
   get impact synthesis with the canary ladder.
6. Exit gate: catalog coverage numbers — checks applicable, run, closed by
   state — with every closure citing its records.

## 4. Hard Rules (mechanically enforced)

1. **Falsifier before payload.** The hypothesis record precedes the
   treatment request in the ledger — order is auditable.
2. **Both hosts in scope.** Authorization server and callback host; the
   gate refusal otherwise is a finding about the ENGAGEMENT, not the target.
3. **Operator-owned apps only.** Cross-app checks use the operator's second
   app registration, never a third party's client_id.
4. **No token replay against real user resources.** Token reuse checks
   redeem the code/token against the operator's own resource server.

## 5. Tool Routing

| When | Tool |
| --- | --- |
| Happy-path + check requests | `http_probe` (headers carry the session) |
| Recording hypotheses/closures | `ledger_append` (EXPERIMENT/CONTROL tags) |
| Client metadata discovery | `api_introspect` on the IdP's well-known endpoints |
| Registering flow surfaces | `dossier_add` (surface-cartographer) |

## 6. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Selecting and running checks | `references/checks.md` |
