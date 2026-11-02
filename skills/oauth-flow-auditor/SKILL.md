---
name: oauth-flow-auditor
version: 2.2.0
type: ai-skill
architecture: package
description: Phase-2/3 OAuth/OIDC flow organ, upgraded (v2) with the Aaron Parecki lineage — a check catalog (redirect_uri exact-match matrix at BOTH endpoints, state presence/validation/binding, PKCE downgrade, code reuse, token audience, implicit flow) where every check is a pre-registered hypothesis with its own falsifier, run as differentials against operator-owned IdP testSince v2.2.0 the organ carries the executable method layer (A16) — a mechanical critique of the published checklist craft's floors (presence rules without differential tests, endpoints audited singly while the classes live in sequences, state presence conflated with validation, spec layers blurred in prose, token lifecycle as unmeasured afterthought) shipped as protocol M1–M5: the flow pin with spec-layer evidence, the redirect byte-class exactness differential, the forged/replayed/absent state test, the PKCE downgrade probe with the wrong-verifier control, and the lifecycle ceiling measured on operator-owned grants. Use when the operator asks to audit an OAuth flow, test redirect_uri validation, check state/PKCE handling, probe code or token reuse, or review an OIDC client configuration ("tes oauth", "redirect_uri", "PKCE", "state missing", "code reuse", "token audience", "OIDC audit", "oauth 2.1", "mix-up").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: v2 — Aaron Parecki (author of OAuth 2.0 Simplified, maintainer of oauth.net, co-editor of the OAuth 2.1 draft; the redirect_uri-exactness / state / PKCE craft)
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; operator-owned OAuth test app pair
---

# oauth-flow-auditor v2.2.0 — Flows Are State Machines; Test The Transitions

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

## 3.5 First Principles — the WWH registers (A14)

* **WHAT** — delegation-protocol defects: OAuth 2.0 grants
  (authorization code, implicit's ghosts, client credentials,
  device flows), OIDC layers (ID-token claims, nonce, session), and
  the implementation's checks (redirect-URI validation, state,
  PKCE, token storage and audience).
* **WHY** — the protocol DISTRIBUTES trust across parties: the
  authorization server, the client, the resource owner, and every
  value passed between them (codes, tokens, redirects, claims). Each
  grant type chooses where secrets live; each implementation chooses
  which spec options to enforce — the spec's flexibility is exactly
  where implementations diverge, and a skipped check (state, exact
  redirect match, audience binding) becomes a trust that crosses a
  party that never earned it. That is the root cause of every check
  in the catalog.
* **HOW** — flows are state machines: enumerate the states (browsers,
  user, AS, client) and the transitions (redirects, token posts,
  redemptions), then test each TRANSITION against its spec check —
  every check carries its falsifier: the probe that would FAIL it. An
  audit where no check can fail is theater (the organ's own law).

War note (A15): the cheng sweep is the 12-check catalog against the
observed flows; the ch'i is the transition the implementation added
that the spec never named (custom parameters crossing redirect
boundaries). W4 pairs them; W6 governs the report — the triage desk
reads state machines, not essays.

## 3.5 The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published OAuth craft where it was mechanically weak —
"validate redirect_uri exactly" as a rule instead of a byte-class
differential, endpoints audited alone while code-interception and
downgrade live in the SEQUENCE, "state present" treated as "state
validated", 2.0/2.1/OIDC layers mixed unpinned, scope deltas and
rotation never measured — and ships the executable replacement:
**M1** the flow pin (provider, spec layer with behavioral evidence,
endpoint set, operator-registered client), **M2** the exactness
differential (exact/case/path-append/suffix/param variant classes,
n ≥ 3; acceptance class AND code-landing observed; all-rejected =
guard CONFIRMED as data), **M3** the state test (legitimate vs forged
vs replayed, n ≥ 5; forged-accepted = never-validated, replay-only =
single-use broken), **M4** the PKCE downgrade probe (S256/plain/absent
× wrong-verifier control; downgrade graded from the grant PAIR),
**M5** the lifecycle ceiling (granted-vs-requested scope delta read
from the operator's own token; claims capped at operator-owned
evidence).

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
| Grading the published craft, pinning the flow, running exactness and state differentials | `references/method-upgrade.md` |
