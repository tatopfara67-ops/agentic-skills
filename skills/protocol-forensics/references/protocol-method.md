# protocol-method.md — the hunt, end to end

The depth module for the Kaminsky lineage: the invariant classes
worth auditing, the full worked arithmetic (the DNS 2008 case,
constants recorded in CERT VU#800113, all other numbers computed by
the house script — recompute, never recall), the disagreement-matrix
schema, and the disclosure and deployment machinery. Load when the
organ is actually running; the SKILL.md routing layer stays lean.

## 1. Where class-level bugs live — the invariant classes

A specification's implicit invariants sort into four classes, and
each class has a standard audit question:

| Invariant class | Audit question | DNS 2008 instance |
| --- | --- | --- |
| entropy budgets | what must be unpredictable, and how many bits does it actually have? | query/reply match carried 16 bits (TXID); fixed source ports added zero |
| ordering assumptions | what must arrive/happen in the order the spec implies, and who enforces it? | a forged reply racing the authoritative answer inside the RTT window |
| trust delegations | whom does each side believe without authentication, and is that belief transferable? | resolvers trusting any reply that matches the outstanding query; bailiwick as the only scope check |
| encoding rules | which byte-level readings does the spec allow to diverge? | name compression, casing (0x20-style encodings as later hardening), label boundaries |

The 2008 attack was a COMPOSITION (the lineage's signature move):
entropy budget (16 bits) × ordering (the race window) × trust
delegation (unauthenticated reply wins the race). The audit prices
each class separately, then the composition — a single-class finding
rarely survives; compositions across classes are where classes fall.

## 2. The arithmetic, in full — DNS 2008 as the worked case

Recorded constants (CERT VU#800113, read in full):

* transaction ID field: **16 bits** — 65,536 values
* average attempts to predict the transaction ID, single blind
  race: **32,768**
* source-port randomization adds **approximately 16 bits** (65,535
  ports available, not all usable; NAT/PAT reduces the effective
  pool — recorded caveat)
* birthday attacks enabled by **multiple outstanding requests** —
  implementations generating multiple identical queries

Computed by the house script (birthday approximation
`1 − exp(−n(n−1)/2·space)`; single-race `m50 = ln 2 / ln(1 − 1/space)`):

### Table A — birthday race, fixed source port (16-bit space)

| outstanding queries n | P(at least one forged reply matches) |
| --- | --- |
| 10 | 0.07% |
| 50 | 1.85% |
| 100 | 7.27% |
| 200 | 26.19% |
| 300 | 49.56% |
| 400 | 70.41% |
| 500 | 85.10% |

**Threshold row: n ≈ 302 outstanding queries → ~50% win.**

### Table B — single-query race (one outstanding, m forged replies)

| regime | m for 50% win |
| --- | --- |
| fixed port (16-bit) | 45,426 forged replies |
| port-randomized (~32-bit) | 2,977,044,471 forged replies |

### Table C — birthday race with port randomization (~32-bit space)

n ≈ 77,163 outstanding queries → ~50% win (≈ 2^16.2 — the race
remains structurally winnable, only priced up; this is exactly why
the record calls port randomization a stopgap, not a fix).

### Table D — NAT-reduced port pools (the recorded caveat, priced)

| usable ports | effective entropy | per-reply odds |
| --- | --- | --- |
| 1,024 | ~26.0 bits | 1 in 67,108,864 |
| 4,096 | ~28.0 bits | 1 in 268,435,456 |
| 16,384 | ~30.0 bits | 1 in 1,073,741,824 |
| 64,511 | ~32.0 bits | 1 in 4,227,792,896 |

Reading of the tables (the decision procedure W2 wanted): the
invariant is declared BROKEN when the computed win probability
crosses the stated threshold within the attacker budget the
engagement declares; the same tables then price the fix — every
added entropy bit multiplies the required budget, and every
removed NAT port divides it back. The bailiwick bypass that made
the 2008 race CONTINUOUS (query a fresh nonexistent subdomain each
round so the cache never blocks the next race) is an ordering-class
finding riding on the entropy-class one: the audit must compose the
classes before any threshold row is written.

## 3. The disagreement matrix — schema and discipline

```
MATRIX: class=<id> invariant=<id>
  rows: implementations (name+version, census-pinned)
  columns: invariants (id, threshold row from M2)
  cell: observable=<what was sent/seen> runs=<n> verdict=<AGREE|
        DIVERGE|FLAKY> ledger=<R-NNN>
  rule: one variable per probe; load-bearing cells n_runs >= 2;
        a FLAKY cell re-runs at n>=3 and its instability is data
```

The matrix, not any single cell, is the class-level finding: the
2008 aftermath on record showed resolvers, stub resolvers, and NAT
middlewares resolving the same ambiguity differently — uniform
behavior would have routed the whole matter to a per-product organ,
and a uniform matrix is the organ's honest negative result.

## 4. Disclosure engineering — the checklists

The 2008 record, mechanized (M5):

1. **Vendor matrix**: one row per affected implementer — channel,
   status, patch ETA; the matrix is a living artifact from the day
   the invariant is declared broken (the record's secret Microsoft
   HQ meeting and DHS involvement are the trust-network version of
   this row set; an agent's version is the matrix itself).
2. **Advisory registration**: the coordinator ID is part of the
   method (VU#800113 in the record); register early, publish late.
3. **Simultaneous release**: one date, all vendors, drafts in hand —
   drip disclosure re-opens the window it closes.
4. **Leak fallback**: when details leak early (July 21, 2008 in the
   record), the accelerated reveal executes from the pre-drafted
   materials — the fallback is designed before it is needed.
5. **The report as instrument**: the writeup exists to drive patch
   adoption, not to celebrate the find; every table in it serves a
   patching decision.

## 5. Post-patch verification — measurement with a stop rule

```
VERIFY: sample=<population sample or full census, stated>
  dates=<measurement dates> deployed=<k/n at each date>
  gate=<saturation threshold> OR deadline=<date>
  residual: stopgap=<name> structural-fix=<name+eta> dated rows
```

The 2008 pattern held honestly: port randomization deployed
worldwide within months (measured by the industry's own campaigns),
while the record itself insisted DNSSEC was the structural fix —
the organ's version files both as dated rows and refuses closure
while the stopgap row is open. Deployment is a curve; a single
"patched" checkbox is an anecdote (the W4 floor, closed).

## 6. Where this organ stops

Two neighbors own adjacent ground, and the census's boundary rows
keep the peace: desync-hunter takes the seam INSIDE one request
path (front-end vs back-end parser disagreement on the same bytes);
scan-economist governs the probe budget this organ spends while
running its matrix. When the disagreement is between two parsers
behind one front door, route there; when the question is how many
probes the race can afford, route there. When the disagreement is
between implementations of one spec — the class itself — this is
home ground.
