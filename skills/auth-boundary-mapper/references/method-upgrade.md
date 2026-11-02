# The method upgrade — critiquing Rosen, shipping the executable boundary map

The charter's A16 charge: **a lineage named is not expertise delivered.**
Frans Rosen's art is real — the IDOR-through-methodology line:
identifier construction, second-order IDOR, response-diff rigor —
but the published form has floors: one-finding writeups, identifier
intuition taught as attention ("look for GUIDs"), response
differences read by eyes, the access matrix never assembled as
data. This module extracts what is protocol-shaped and ships the
replacement: an identifier census, a pre-registered role×resource
matrix, the three-condition IDOR differential, a second-order flow
map, and an impact ceiling. An agent that has never read the blog
must run this at its rigor.

## 1. The critique — five mechanical weaknesses of the published method

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | One-finding narratives — each writeup walks ONE IDOR end-to-end; the mapping protocol that FOUND it stays implicit | Readers inherit bug stories, not a surface procedure; every new target restarts from zero with "pay attention to ids" as the entire toolkit |
| W2 | Identifier intuition — "sequential ids are juicy, GUIDs can still leak" taught as attention rules | Without an identifier CENSUS (every id class, its construction grammar, its predictability measured), the hunter samples the surface by taste and misses the classes nobody blogged about |
| W3 | Response-diff rigor asserted — "compare the responses" with no bucket rule, no n, no threshold | Two analysts diffing the same pair disagree on "different"; jitter ( CSRF tokens, timestamps) reads as access divergence exactly once — the false positive engine of the whole class |
| W4 | The access matrix never built — role × resource × action as a grid is implied by every writeup and assembled by none | Without the pre-registered matrix, "tested the boundary" is unfalsifiable: nobody can say which cells were probed, so coverage is feeling |
| W5 | Second-order IDOR as eureka — "the id traveled server-side into another query" narrated per bug | The travel of identifiers through server-side flows is MAP-ABLE (which handlers consume which ids); per-bug eureka means the map is rebuilt by luck every engagement |

## 2. The upgrades — and where they land

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Every identifier censused with grammar + predictability | **M1** — the identifier census |
| U2 | The matrix pre-registered from operator-owned roles | **M2** — the access matrix |
| U3 | IDOR as a three-condition differential with buckets | **M3** — the boundary differential |
| U4 | Identifier travel mapped as data | **M4** — the second-order map |
| U5 | Claims capped at operator-owned pair evidence | **M5** — the impact ceiling |

## 3. The executable protocol — M1 through M5

### M1 — the identifier census

From the surface records and observed traffic, every identifier
class gets a row:

```
IDENT: class=<order-id|user-uuid|doc-slug|...> grammar=<construction:
  sequential|uuid|opaque|derived-from> observed-in=<endpoints>
  predictability=<measured: range seen, entropy class>
  ownership-basis=<which operator account mints them>
```

Rules: predictability is MEASURED from the operator's own minted
ids (n ≥ 10: the spread and reuse), not guessed; an id class with
no ownership basis is parked until the operator provides one —
probing ids you cannot own is out of bounds (the house rule).

### M2 — the access matrix (pre-registered before any probe)

```
MATRIX: rows=<resources × actions observed from surface>
  columns=<operator-owned roles: anon|userA|userB|admin-if-provided>
  cells pre-filled with EXPECTED access from the app's own claims
  (docs, UI affordances) — expectation, not verdict
```

The matrix rides the dossier; probe coverage is reported against it
(cells probed / cells expected) — the W4 floor made arithmetic.

### M3 — the boundary differential (three conditions)

Per matrix cell (resource × action, role pair):

1. **Conditions, n ≥ 5, interleaved**:
   * baseline — the role's OWN reference (userA → userA's id),
     benign;
   * treatment — the OTHER operator account's reference (userA →
     userB's id), same endpoint, same shape;
   * control — a NONEXISTENT id of the same grammar class (the
     not-found oracle).
2. **Observation vector**: status, length bucket, body-shape class,
   and the marker check (does userB's data — carrying an operator
     marker — appear?).
3. **Confirm rule (all three)**: treatment bucket ≠ control bucket
   in ≥ 4 of 5 (it behaves like a REAL object, not a miss) AND
   treatment exposes userB's marker in ≥ 4 of 5 AND baseline stable.
   Treatment = control (404 both) is a CLOSED cell on record; a
   single divergence is a LEAD (the n floor exists for exactly the
   jitter class W3 names).

### M4 — the second-order map

Where an identifier DISAPPEARS from the response and the effect
surfaces elsewhere: per disappearing id, one map row —

```
FLOW: id=<class> consumed-at=<endpoint> surfaces-at=<observed:
  notification|export|report|internal-call> evidence=<operator
  marker round-trip: minted id → marker observed at surface>
```

The marker round-trip (operator-owned id with an operator-observable
artifact downstream) is the only evidence class that closes a
second-order row — inference from response shape alone parks it as
a hypothesis.

### M5 — the impact ceiling

```
CEILING: proven=<access divergence on operator-owned pair, cells
  cited> scope=<role pair × resource class> NOT-CLAIMED=<real-user
  data exposure, cross-tenant reach> unless a third-party-impact
  arithmetic is provided by the operator's own telemetry
```

IDOR severity rides the resource class (payment settings > display
name) and the role distance — both from the matrix, both cited; the
report never rounds "userA saw userB's data (operator pair)" up to
"any user sees any user's data" without the matrix cells that prove
the generalization.

## 4. Falsifiers — what would prove this method wrong

* Treatment matches control in every cell but the app demonstrably
  leaks in production → the grammar class was wrong (the control id
  accidentally valid, or the treatment id stale): re-mint, re-run;
  the differential is the arbiter, not the rumor.
* Two analysts' bucket calls disagree on one pair → the bucket rule
  is under-specified for this response shape (dynamic CSRF noise):
  add the noise dimension to the bucket, re-run the pair, record
  the correction.
* The matrix shows 100% expected-access match but a later incident
  leaks cross-role → the matrix's ROLE set was incomplete (a
  service role existed unbeknownst): the gap is in the census, and
  the incident's role gets a column retroactively — the matrix
  self-corrects with the incident as data.
* A second-order row's marker round-trip fails on re-run → the
  downstream surface is batched/scheduled: park with the schedule
  hypothesis; never close it as negative from one timing.

## 5. Worked micro-example (numbers consistent, incident fictional)

Matrix: 3 roles (anon, userA, userB) × 14 resource×action cells.
M1 census: order-id sequential (n = 12 minted, spread 421xx —
predictable class), doc-uuid opaque. M3 on cell (order-detail,
userA→userB order): baseline userA→userA 200/4k 5/5; treatment
userA→userB 200/4k with userB marker 5/5; control nonexistent id
404/0.3k 5/5 → CONFIRMED (treatment ≠ control, marker present).
M4: order-id consumed at /receipt-send, surfaces at notification
(marker round-trip observed once, re-run scheduled-class parked
honestly). M5 ceiling: operator pair, order-detail class, P3;
"any user" NOT claimed — matrix cites exactly which cells were
probed (11/14; 3 cells parked with reasons).
