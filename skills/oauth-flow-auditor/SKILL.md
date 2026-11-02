---
name: oauth-flow-auditor
version: 2.0.0
type: ai-skill
architecture: package
description: Phase-2/3 OAuth/OIDC flow organ, upgraded (v2) with the Aaron Parecki lineage — a check catalog (redirect_uri exact-match matrix at BOTH endpoints, state presence/validation/binding, PKCE downgrade, code reuse, token audience, implicit flow) where every check is a pre-registered hypothesis with its own falsifier, run as differentials against operator-owned IdP test apps, with severity vocabulary mapped to the RFC 9700 BCP. Use when the operator asks to audit an OAuth flow, test redirect_uri validation, check state/PKCE handling, probe code or token reuse, or review an OIDC client configuration ("tes oauth", "redirect_uri", "PKCE", "state missing", "code reuse", "token audience", "OIDC audit", "oauth 2.1", "mix-up").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: v2 — Aaron Parecki (author of OAuth 2.0 Simplified, maintainer of oauth.net, co-editor of the OAuth 2.1 draft; the redirect_uri-exactness / state / PKCE craft)
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; operator-owned OAuth test app pair
---

# oauth-flow-auditor v2.0.0 — Flows Are State Machines; Test The Transitions

## 0. What This Skill Is — and Is Not

* **Is**: the organ that walks an OAuth/OIDC flow as a state machine and
  attacks each TRANSITION with a catalog check: every check has a grammar,
  a falsifier, and a differential — before it has a verdict.
* **Is not**: a token-fiddling playground. Tokens are operator-owned test
  artifacts; no third-party account is ever involved. Since v2 it carries
  the **Aaron Parecki lineage** as its field-guide layer — the craft that
  treats redirect_uri as the load-bearing wall, state as three separate
  checks, and the BCP as the severity vocabulary.

## 1. Inherited Contracts

Plugs into **Phase 2** (check catalog → hypotheses) and **Phase 3**
(differential experiments) of the mythos-bug-hunter spine. Inherits the
hypothesis grammar (§5), experiment contract (§6), closure vocabulary (§7),
and canary doctrine (§8: only self-injected markers cross boundaries).

## 2. The Lineage Layer (v2 — the Parecki doctrine)

**Aaron Parecki** — author of "OAuth 2.0 Simplified" (oauth.com),
maintainer of oauth.net, co-editor of the in-progress OAuth 2.1 draft.
v2 folds the lineage in as five field rules, applied inside the check
catalog (§4) and detailed in `references/flow-craft.md`:

1. **redirect_uri is a matrix at both ends.** Exact match per RFC 6749
   §3.1.2.3 — case, trailing slash, traversal, userinfo, encoding,
   scheme — tested at the authorization endpoint AND the token endpoint
   separately; their disagreement is itself a finding.
2. **state is three checks, never one.** Presence, validation, binding/
   single-use — each closes on its own differential.
3. **PKCE is checked where it wasn't invited.** Downgrade and plain-vs-
   S256 apply to confidential clients too.
4. **Severity vocabulary maps to the BCP (RFC 9700):** issuer
   identification, exact redirect matching, no implicit, sender-
   constrained tokens — cite the control, not the mood.
5. **Error paths are instruments.** Differential bodies/latency across
   client_id/redirect knowledge maps the enumeration surface; echoed
   redirect_uri in error output is chain input, recorded verbatim.

## 3. Preconditions (hard)

1. AUTH record present; authorization server AND client callback host both
   in scope (the gate checks both — an out-of-scope callback host is a
   REFUSED record, and that refusal is itself reported).
2. An operator-owned test app registration (client_id under test) and a
   second one for cross-app confusion checks.
3. The flow transcript: each step of ONE happy-path run, ledgered as FACT
   records, BEFORE any check runs — the baseline state machine.

## 4. Procedure — Numbered Actions

1. Record the happy path: authorize request → redirect → callback → token
   exchange → resource access. One request per step, all FACT records.
2. Load the check catalog (`references/checks.md`) and map each check to
   the transition it attacks; v2 checks select their variants from the
   lineage matrix in `references/flow-craft.md` (redirect_uri both ends,
   state triple, PKCE downgrade, BCP vocabulary).
3. Pre-register one hypothesis per check, in the spine grammar, with the
   falsifier stated BEFORE the crafted request (retrodisction is discarded,
   spine §5).
4. Run each check as a differential: baseline (happy-path record from
   step 1) vs treatment (the check's crafted variant) vs control (same
   effort, unrelated knob — e.g. a garbage state value when testing
   redirect_uri).
5. Close each hypothesis in the three-state vocabulary; CONFIRMED checks
   get impact synthesis with the canary ladder, severity words citing
   the mapped BCP control (v2).
6. Exit gate: catalog coverage numbers — checks applicable, run, closed by
   state — with every closure citing its records.

## 5. Hard Rules (mechanically enforced)

1. **Falsifier before payload.** The hypothesis record precedes the
   treatment request in the ledger — order is auditable.
2. **Both hosts in scope.** Authorization server and callback host; the
   gate refusal otherwise is a finding about the ENGAGEMENT, not the target.
3. **Operator-owned apps only.** Cross-app checks use the operator's second
   app registration, never a third party's client_id.
4. **No token replay against real user resources.** Token reuse checks
   redeem the code/token against the operator's own resource server.
5. **redirect_uri verdicts name their endpoint** (v2): a matrix row closed
   without saying WHICH end accepted it is an incomplete record.

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Happy-path + check requests | `http_probe` (headers carry the session) |
| Recording hypotheses/closures | `ledger_append` (EXPERIMENT/CONTROL tags) |
| Client metadata discovery | `api_introspect` on the IdP's well-known endpoints |
| Registering flow surfaces | `dossier_add` (surface-cartographer) |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Selecting and running checks | `references/checks.md` |
| redirect_uri matrix, state triple, PKCE downgrade, BCP vocabulary, error-path instruments | `references/flow-craft.md` |
| Citing the lineage artifacts behind the v2 layer | `references/sources.md` |
