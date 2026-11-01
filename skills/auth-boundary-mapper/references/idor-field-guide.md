# idor-field-guide.md — the Frans Rosen lineage layer for auth-boundary-mapper (v2)

Load when running the v2 passes: identifier construction, parameter
positions, 2nd-order flows, response diffing, tenant slices.

## 1. Identifier Construction Classes

Analyze BEFORE swapping — the class decides the strategy and the
blast-radius argument.

| Class | Shape | Swap strategy | Blast-radius argument |
| --- | --- | --- | --- |
| sequential int | 1001, 1002 | direct swap; control id = ±1 and nonexistent | enumeration is trivial — wide horizontal |
| UUID v4 | random 128-bit | no guessing; harvest ids from own objects, shares, exports, logs | access control is the ONLY barrier — sharp verdicts |
| UUID v1/v7 | time-embedded | time-window reasoning for adjacent objects | creation-order leakage rides along |
| username/email | human-readable | cross-account swap with operator-owned pair | lookup-vs-authorization confusion common |
| org-prefixed composite | `org123_user456` | swap BOTH segments independently, then jointly | partial checks show as one-segment-only failures |
| opaque cursor/token | base64/encoded | decode; test whether the token embeds the object id | tamper the decoded id, re-encode, one probe |

Record the class per resource in the matrix (step 2 of the
procedure) — the class is a FACT, not a guess.

## 2. Parameter Positions (swap everywhere the reference appears)

Same object, four positions, four separate cells:

```
path   : GET /api/v1/invoices/1001
query  : GET /api/v1/invoices?invoice_id=1001
body   : POST /api/v1/invoices/preview {"id": 1001}
header : X-Resource-Id: 1001
```

Checks are frequently per-position: the route middleware checks
`path`, the handler checks `body`, and `header` is decoration.
A position where the swap is granted while others deny is its own
finding line (with its own triad).

## 3. 2nd-Order IDOR (reference created now, consumed later)

Flows where the differential pair spans TWO features:

```
create leg : POST /invites {"email": "b@op.test"}          (tenant A)
consume leg: GET /accept?token=<token-from-create-leg>      (tenant B)
```

The sweep: run the create leg with account A, then attempt the
consume leg authenticated as account B (both operator-owned). The
triad is (A-create+A-consume) baseline, (A-create+B-consume)
treatment, (garbage-token) control. Typical surfaces: invites,
shares, exports/reports, email-linked actions, scheduled jobs,
webhook subscriptions.

## 4. Response-Body Diff Rigor (the false-positive killer)

For every granted treatment:

1. hash the treatment body and the A-own-baseline body;
2. compare STRUCTURE (field set) and VALUES (owner fields);
3. verdict `granted` requires the cross-tenant object's content
   family — `200` with the same-tenant echo and a swapped label is
   a near-miss MISTAKE record, not a finding;
4. `leaky-denial` (denial status, different error for existing vs
   nonexistent ids) is its own low-severity line — the CONTROL
   request proves it.

## 5. Attribution Record (kept on record per doctrine A3)

* **Figure**: Frans Rosen — Detectify co-founder, long-time
  top-ranked bug bounty hunter. Public record consulted: his
  "Attacking Modern Web Technologies" talk material (Nullcon-era),
  the 2nd-order IDOR keynote material (referenced via Intigriti's
  Bug Bytes #55 coverage), and his public IDOR writeup series;
  Bugcrowd's podcast record (Detectify founding context).
* **Correction on record**: the operator's brief spelled the name
  "Franz Rosen" — verified spelling is **Frans Rosen**. The organ
  and the lineage registry carry the verified spelling.
* **What is NOT claimed**: no Detectify content, no proprietary
  scanning technology, and no endorsement. The five field rules
  are a distillation of the public methodology shape (study how
  references are constructed and consumed; hunt where checks are
  positional; hunt across features; distrust status codes), with
  this bundle's own matrix/triad integration.

## 6. Non-Obvious Verbs (the positions hunters skip)

* **PATCH partial update** — one field swapped, others untouched:
  partial authorization shows as update-succeeded-on-foreign-object.
* **Bulk endpoints** — arrays of ids: the swap is ONE foreign id
  inside an own-id array (bounded: one foreign, self-owned).
* **Export/download tokens** — the token granted for A's export,
  replayed against B's export id (2nd-order + position combined).
* **DELETE** — never against non-self-owned objects: the matrix
  row stays EXPECTED-deny; a granted DELETE on a foreign object is
  proven by existence-disappearance of the OPERATOR's own object
  (create-B-object via B, delete it as A — self-owned both ends).
