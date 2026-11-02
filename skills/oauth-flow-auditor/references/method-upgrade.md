# The method upgrade — critiquing Parecki, shipping the executable flow audit

The charter's A16 charge: **a lineage named is not expertise delivered.**
Aaron Parecki's art is real — OAuth 2.0 Simplified, oauth.net
stewardship, the 2.1 draft — but the published craft ships as
blog-checklist: redirect_uri exactness, state, PKCE as rules of
thumb, each told singly, none with a differential. This module
extracts what is protocol-shaped and ships the replacement: a flow
pin with the version matrix, the exactness differential, the
state three-condition test, the PKCE downgrade probe, and a token
lifecycle ceiling measured on operator-owned grants. An agent that
has never read the RFCs must run this at its precision.

## 1. The critique — five mechanical weaknesses of the published craft

| # | What the craft shows (documented) | Why it is weak as a shipped method |
| - | ---------------------------------- | --------------------------------- |
| W1 | Checklist epistemology — "validate redirect_uri exactly", "always use state", "use PKCE" stated as rules | Presence rules without differential tests: a flow can pass every checklist line and still accept a byte-variant redirect or an unvalidated state — the checklists grade configuration, not behavior |
| W2 | Flows tested singly — each endpoint (authorize, token, callback) audited alone | The vulnerability classes live in the SEQUENCE (code interception needs the whole redirect walk; downgrade needs the pair of grant attempts); single-endpoint audits cannot see them |
| W3 | Presence conflated with correctness — "state is present" treated as "state is validated" | The two are independent: unvalidated state is a silent as its absence; only the forged/replayed/absent three-condition test separates them |
| W4 | Version layers blurred — 2.0 vs 2.1 vs OIDC vs provider extensions mixed in prose guidance | A finding's meaning depends on which spec layer the provider actually implements; unpinned advice produces both false positives (demanding 2.1 behavior from a 2.0 flow) and missed classes |
| W5 | Token lifecycle as afterthought — expiry, rotation, scope creep mentioned, never measured | The granted-scope vs requested-scope delta, the refresh-rotation behavior, and the expiry class are the impact carriers; folklore treats them as deployment trivia |

## 2. The upgrades — and where they land

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | The flow pinned: provider, spec layer, endpoints as FACTs | **M1** — the flow pin |
| U2 | Redirect exactness as a byte-class differential | **M2** — the exactness differential |
| U3 | State as a three-condition test | **M3** — the state test |
| U4 | PKCE as a downgrade probe | **M4** — the PKCE probe |
| U5 | The lifecycle measured on operator-owned grants | **M5** — the lifecycle ceiling |

## 3. The executable protocol — M1 through M5

### M1 — the flow pin

```
FLOW-PIN: provider=<observed, from operator-owned app> spec-layer=
  <2.0|2.1-behavior|OIDC|provider-ext, evidence cited> endpoints=
  {authorize,token,callback,introspection-if-reachable} client=
  <operator-registered test app> grant-classes=<observed>
```

Every later claim cites the pin (W4). Spec-layer evidence = the
provider's own behavior on distinguishing probes (e.g. does the
authorize endpoint require PKCE when the client sends it), never
the provider's documentation alone.

### M2 — the exactness differential (redirect_uri as behavior)

One EXPERIMENT per byte-variant class, n ≥ 3, operator-owned app:

| Variant class | Probe | Acceptance means |
| ------------- | ----- | ---------------- |
| exact | registered URI verbatim | baseline — the working pair |
| case | scheme/host case-flipped | loose compare — finding class: redirect weakness |
| path-append | registered + `/x` | prefix match — worse class |
| suffix-confusion | `evil.com#` / `@` / dot-segment tricks per corpus | structural confusion — route to injection-lab grammar if novel |
| param-inject | added params (`?x=1`) | param-tolerant — combined with state test |

Rules: the probe uses the operator's own client id and observes the
AUTHORIZE side (does the error page fire?) AND, on success, where
the CODE lands — the differential is acceptance-class per variant,
recorded; a provider that rejects all variants is recorded as
exact-compare-CONFIRMED (a working guard is data, not
disappointment).

### M3 — the state test (presence ≠ correctness)

Three conditions on the callback, n ≥ 5, interleaved:

1. **legitimate-state** — the app's own round-trip (baseline);
2. **forged-state** — the operator test client sends a DIFFERENT
   state value than it issued (treatment);
3. **replayed-state** — a captured operator state re-used (the
   replay class).

**Confirm rule**: forged-state and replayed-state must BOTH be
rejected (error class ≥ 4/5) for the state validation to be graded
WORKING; acceptance of either (≥ 4/5) is the finding, graded by
which condition failed — forged-accepted = never-validated
(severe), replayed-accepted-only = single-use broken (session
fixation class). Present-but-unvalidated is exactly what this
separates (W3).

### M4 — the PKCE downgrade probe

1. The operator client runs the flow three ways, n ≥ 3 each:
   with-PKCE (S256), with-plain-challenge, without-PKCE.
2. **Observation**: which variants the provider's authorize+token
   pair ACCEPTS, and whether the token endpoint verifies the
   verifier (a transformed-verifier probe — wrong verifier, correct
   code — closes the verification question).
3. **Downgrade finding**: without-PKCE accepted on a public-class
   client = downgrade class, graded with the interception context
   (W2's sequence discipline: the pair of grant attempts is the
   evidence, not one endpoint).

### M5 — the lifecycle ceiling (measured on operator grants)

```
LIFECYCLE: requested-scope=<operator app's ask> granted-scope=
  <introspection/decode observation, VERBATIM> delta=<classes
  beyond request — the creep finding> expiry=<class> rotation=
  <refresh behavior, n=2 observed> ceiling: claims capped at
  OPERATOR-OWNED grant evidence
```

The scope delta is read from the operator's own token (introspection
endpoint or JWT decode) — never from a third party's (W5). The
ceiling caps impact claims at what the operator's grant
demonstrated.

## 4. Falsifiers — what would prove this method wrong

* A variant class is accepted but the code never lands anywhere
  attacker-usable → acceptance ≠ redirect: the landing observation
  downgrades the class; record both halves.
* The state test passes forged/replayed but a later CVE shows
  validation bypass → the bypass class wasn't in the three
  conditions: add it as a fourth condition with the CVE as source,
  re-run — the protocol grows by falsification, not by trust.
* PKCE verification holds for S256 but plain is accepted →
  half-downgrade: graded as its own row (plain-accepted class),
  never merged into the full finding.
* Introspection disagrees with JWT-decode on granted scope → the
  introspection source is authoritative; the decode stale — record
  the divergence as a lifecycle finding of its own (drift class).

## 5. Worked micro-example (numbers consistent, incident fictional)

Provider pinned (2.0-behavior + OIDC layer, evidence: authorize
requires client_id param grammar per observation). M2: exact
accepted (baseline 3/3); case-flipped accepted 3/3 (loose-compare
finding); path-append rejected 3/3 (guard). M3: forged-state
REJECTED 5/5, replayed-state ACCEPTED 4/5 → single-use broken,
session-fixation class, P3. M4: S256 verified (wrong-verifier
probe rejected 3/3), without-PKCE accepted 3/3 on the public test
client → downgrade row recorded. M5: granted scope = requested +
`profile` (delta class creep), expiry 3600 s, rotation single-use
observed n = 2. Ceiling: all rows on operator-owned grants; report
cites the FLOW-PIN and both spec layers.
