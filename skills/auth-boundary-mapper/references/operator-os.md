# operator-os.md — the Rosén runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> boundary laws; the M-protocol (references/method-upgrade.md) states
> the identifier census and access matrix; THIS module is the runtime
> — how the agent thinks, behaves, and scripts while executing them,
> characteristic of Frans Rosén's documented craft: identifiers are a
> construction space, every parameter position is a candidate, and the
> response diff — full, not skimmed — is the only verdict that counts.

## 1. The thinking framework — decision rules

R1 **The identifier is a construction space, not a string.** Every ID
has a grammar: type (int/uuid/slug/base64), source (sequential =
enumerable), scope (tenant-scoped or global), and transformation
(base64/JSON wrappers). Read the grammar before touching the value.
*From:* the lineage's method-bearing talks on IDOR methodology —
identifier construction is step one.

R2 **Every parameter position gets a ticket.** Body, path, query,
header, JSON-nested, array-indexed — each position where an identifier
travels is a census row; unvisited positions are untested surface,
not "probably fine".

R3 **Full response diffs, always.** Status-code-only comparison misses
the leaking field, the extra object, the timing tell. The verdict
machine diffs status + headers + body (normalized) + timing class.

R4 **Second-order beats first-order.** The juicy boundary is often one
step removed: the ID stored via endpoint A and READ via endpoint B
(the 2nd-order map) — write-read pairs are hunted explicitly.

R5 **Swap, don't synthesize.** The differential uses REAL identifiers
of the operator's second account (the canonical victim), never
invented ids — the proof needs the server to actually resolve both.

R6 **The matrix closes or the hunt is open.** Exit means every
role×resource row has a verdict; anything less is a resume note, not a
finding set.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| Two operator-owned accounts ready | Census identifiers before any swap | T1 builds the identifier census (grammar + positions) | Never swap IDs before the census exists |
| An ID looks opaque | Decode before deciding | T2 classifies grammar (uuid/int/base64-json) | Never call an ID "random" without decoding it |
| A swap planned | Pre-register the expected outcome | EXPERIMENT row: swap in position P, expect denial if boundary holds | Never send swaps unregistered |
| Responses differ slightly | Full diff, not a glance | T3 diffs all four channels; the delta class is the verdict | Never eyeball two JSON blobs |
| A direct swap is blocked | Go second-order | T4 hunts write→read pairs across endpoints | Never conclude "no IDOR" from direct-only |
| A tenant boundary appears | Tenant-slice the matrix | rows per tenant×resource added | Never treat tenancy as "just another header" |
| Impact tempting (read the other tenant's data) | Stay at the marker | The differential record is the impact ceiling — one marker row | Never page through another account's objects |

Pacing: one swap position per EXPERIMENT; matrix cells fill in
sequence, not in parallel bursts. Failure reaction: a boundary that
blocks one position but leaks via its second-order pair is recorded as
a partial-boundary row — the matrix keeps both facts.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — identifier census

```bash
python3 - <<'PY'
census = [
 # endpoint, position, name, grammar, source
 ("/api/orders/12345",           "path",   "order_id", "int-seq",    "enumerable"),
 ("/api/orders?user=QWJl",       "query",  "user_ref", "base64",     "decodes to 'Abe'"),
 ("/api/orders",                 "body",   "owner_uuid", "uuid-v4",  "doc field"),
 ("/api/orders",                 "header", "X-Account", "slug",      "tenant hint"),
]
for row in census: print(f"{row[0]:28} {row[1]:7} {row[2]:11} {row[3]:8} {row[4]}")
PY
```

Read-out: the census table. Gate: every endpoint in scope has rows for
EVERY position an identifier occupies (R2) — gaps are parked, not
assumed safe.

### T2 — identifier grammar decoder

```bash
python3 - <<'PY'
import base64, re, uuid
def grammar(v):
    if re.fullmatch(r"\d+", v): return "int (sequential? arithmetic-check)"
    try: uuid.UUID(v); return "uuid"
    except ValueError: pass
    try:
        d = base64.b64decode(v + "==").decode()
        return f"base64 -> {d!r}"
    except Exception: return "opaque"
for v in ["12345", "9f2a…", "QWJl", "eyJ1c2VyIjo1fQ=="]:
    print(f"{v:24} {grammar(v)}")
PY
```

Read-out: per-ID grammar classification. Gate: "opaque" ids still get
swap-tested — grammar informs enumeration, never replaces the
differential (R1).

### T3 — full response diff machine

```bash
python3 - <<'PY'
import json
def norm(b):
    try: return json.dumps(json.loads(b), sort_keys=True)
    except Exception: return repr(b)[:200]
def diff(a, b):   # a: own-account response, b: swapped-victim response
    for k in ("status", "headers_len", "body_sha", "time_ms"):
        if a[k] != b[k]: print(f"DELTA {k}: {a[k]} -> {b[k]}")
print("verdict: UNAUTHORIZED-NO-DELTA = boundary holds; any DELTA = boundary row")
PY
```

Read-out: delta classes across all four channels. Gate: verdicts cite
the full diff — status-only comparisons are refused (R3).

### T4 — second-order pair hunter

```bash
python3 - <<'PY'
pairs = [
 # write endpoint, id field, read endpoint, observable
 ("POST /api/profile", "account_ref", "GET /api/orders?expand=profile", "profile block"),
 ("PUT /api/cart",     "coupon_owner", "GET /api/checkout/review",       "coupon row"),
]
for w, f, r, o in pairs: print(f"write {w} [{f}] -> read {r} reveals {o}")
PY
```

Read-out: the 2nd-order map. Gate: direct-swap-only hunts cannot exit
(R4) — the map is a mandatory section of the matrix.

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | two operator accounts live | census identifiers + positions | T1, T2 | census table complete per endpoint | FACT |
| S2 | census exists | baseline BOTH accounts' normal responses | T3 (canonical) | baseline pair per row | FACT |
| S3 | baselines stable | swap ONE position per EXPERIMENT | T3 | verdict recorded (delta/no-delta) | EXPERIMENT |
| S4 | direct rows done | hunt second-order pairs | T4 | write→read rows verdicted | EXPERIMENT |
| S5 | deltas found | marker-bounded impact proof (one row, one victim account) | governed probe | impact ceiling stated | CANARY |
| S6 | matrix closing | exit: every row verdicted or parked | — | resume notes for open rows | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A swap executed with no census row behind it → R1/R2 violation; the
  observation is unattributable and void.
* A "no IDOR" conclusion from direct swaps only → R4 violation; the
  2nd-order map is mandatory before that sentence.
* A verdict from status-code-only comparison → R3 violation; re-run
  the full diff.
* Impact demonstrations beyond the single marker row → the ceiling is
  the record; everything beyond it is an incident, not a finding.
