# The method upgrade — critiquing Kaminsky, shipping the executable protocol forensics

The charter's A16 charge: **a lineage named is not expertise
delivered.** Kaminsky's art is real — the 2008 disclosure coordinated
a simultaneous industry patch of historic proportion (July 8, 2008,
CERT VU#800113), the Black Ops series ran 2001–2016, and the corpus
repeatedly demonstrates the class-level move — but the published
form has floors: the hunt itself was narrated as story, the entropy
arithmetic was scattered across talks and advisories instead of
consolidated into decision tables, the vendor census ran through
personal trust networks, and post-patch deployment was tracked by
anecdote. This module extracts what is replayable by an agent and
ships the replacement: a population census with a boundary argument,
an invariant audit with computed collision arithmetic, disagreement
matrix probes, an impact ladder with denominators, disclosure
engineering, and a measured post-patch gate. An agent without
Kaminsky's rolodex or stage presence runs this at his precision.

## 1. The critique — six mechanical weaknesses of the published method

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | The hunt told as story — "how I found it" lives in webcast interviews and press coverage (Black Hat Webcast #2, 2008; press, Aug 2008), never as a pre-registered procedure | No replayable search-space ordering exists: an agent cannot re-derive WHERE in a spec to look, only retell the anecdote of one legendary find |
| W2 | Entropy arithmetic scattered — 16-bit TXID and 32,768 average attempts in VU#800113; "+16 bits" from ports in CNET/press; birthday structure in slides and third-party follow-ups (Black Hat DC 09) — never one table | The numbers exist but not as a DECISION procedure: no computed thresholds bind "invariant broken" to a win probability at a stated packet budget; every re-teller re-derives differently |
| W3 | The vendor census run through trust networks — a secret meeting at Microsoft HQ with DHS involvement (Internet Hall of Fame record), phone-tree coordination, personal credibility as the transport | Powerful for one man in 2008, unreproducible for an agent: no vendor-matrix artifact, no per-vendor status ledger, no fallback when the channel does not exist |
| W4 | Post-patch deployment tracked by anecdote — "the patch was applied simultaneously worldwide" stated as history, deployment saturation never measured publicly with a stop rule | Without a measured saturation curve and a deadline, "is the population patched?" is a vibe; the residual window after a stopgap stays unquantified |
| W5 | Humor compresses the method — the Black Ops format optimizes for audience; the documented cost: the PKI talk drew "several very interesting points, but it fails on delivery" (Ristić, 2009), and DEF CON ran "the two-beer version" | The executable steps never ship inside the talk; delight displaces procedure, and the method must be reconstructed by listeners from punchlines |
| W6 | The stopgap's limits stated verbally — the pivot to DNSSEC advocacy happened in talks and interviews (2009–2010) after the port-randomization stopgap | A verbal pivot is not a tracked residual-risk register: no dates, no named structural fix per stopgap, no closure criterion — the debt lives in oratory instead of records |

## 2. The upgrades — and where they land

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | The hunt as a pre-registered class-level procedure | **M1** — the population census |
| U2 | The entropy arithmetic as one computed decision table | **M2** — the invariant audit with thresholds |
| U3 | Disagreement between implementations as the evidence artifact | **M3** — the disagreement-matrix probes |
| U4 | Impact with a counted denominator, not adjectives | **M4** — the impact ladder |
| U5 | Coordination as an artifact matrix, not a trust network | **M5** — the disclosure engineering |
| U6 | Post-patch truth as a measurement with a stop rule | **M6** — the post-patch verification |

## 3. The executable protocol — M1 through M6

### M1 — the population census (the class before the product)

The census header is written before any probing:

```
CENSUS: class=<RFC or spec class>
  suspected-ambiguity=<one sentence>
  boundary: desync-hunter=<why this is not a single-request seam>
  boundary: scan-economist=<why this is not a probe-budget question>
  population: <name+version per implementation, one row each>
  floor: |population| < 3 -> park as product review (recorded)
```

Rules: every implementation pinned by name AND version (the 2008
record's lesson — djbdns was already safe by an independent design
choice while siblings shipped vulnerable for nine years after the
risk was published, 1999–2008); the boundary rows are mandatory
(W1's floor — the class claim must be argued, not assumed).

### M2 — the invariant audit (entropy as arithmetic)

Extract the spec's implicit invariants — entropy budgets, ordering
assumptions, trust delegations, encoding rules — and price each one
with computed arithmetic from recorded constants. The DNS 2008
worked example (constants from VU#800113, birthday tables computed
in references/protocol-method.md):

```
INVARIANT: query/reply match = TXID only (fixed source port)
  recorded: TXID space 65,536 -> average blind attempts 32,768
  birthday structure: 300 outstanding queries -> ~50% win
  threshold: WIN >= 50% within budget B=<stated packets> => BROKEN
INVARIANT: match = TXID + randomized source port (~32 bits)
  computed: single-query race m50 = 2,977,044,471 forged replies
  birthday structure: ~77,163 outstanding queries -> ~50% win
  caveat: NAT-reduced port pools cut effective entropy (26-30 bits
  observed at 1,024-16,384 usable ports) -> re-price, never assume
```

A declared-broken verdict cites its threshold row; an entropy claim
without its arithmetic is a lead (house hard rule 2).

### M3 — the disagreement-matrix probes

One minimal probe per invariant, one variable per probe, run across
the whole census population; n_runs ≥ 2 on load-bearing cells (A8).
The matrix (implementation × invariant) is the evidence artifact —
each cell records the observable, the run count, and the ledger id.
Disagreement across implementations of one spec is the class-level
signature: same input class, divergent resolutions (the 2008
aftermath on record — resolvers, stub resolvers, and NAT middles
all resolved the ambiguity differently).

### M4 — the impact ladder (denominators, not adjectives)

```
RUNG 1 single implementation degrades   -> cite: census row
RUNG 2 class-wide failure               -> cite: matrix column + |population|
RUNG 3 ecosystem trust root             -> cite: measured sample (Sony-
                                          style count) or counted registry
```

Every rung cites a denominator. "Widespread" without a count is
refused at the report gate — the Sony rootkit census (568,000+
machines, 2005) is the lineage's own standard, held against it.

### M5 — the disclosure engineering

```
DISCLOSURE: vendor-matrix=<rows: vendor, contact channel, status,
  patch-eta> advisory=<registry+id target> embargo=<date>
  simultaneous-release=<date> fallback=<accelerated reveal if
  leaked — executed July 21, 2008 in the record>
```

The report is the fix's instrument: drafts ride with the matrix,
the advisory registration is part of the method, and a leak
triggers the recorded fallback rather than improvisation.

### M6 — the post-patch verification (measurement, not anecdote)

Sample the population on stated dates; deployment is a curve with a
stop rule: saturation ≥ the stated gate OR the stated deadline —
whichever hits first, on record. The residual-risk register files
each stopgap with the structural fix it deferred (port
randomization → DNSSEC is the 2008 row), and no partial fix is
reported as closure (W4/W6's floor, closed).

## 4. Falsifiers — what would prove this method wrong

* The census population AGREES on every invariant (matrix is
  uniform) → the class-level hypothesis is falsified for this spec:
  record it, park the organ, route to the per-product organs — a
  uniform matrix is a negative result worth its ledger row.
* Computed win probability never crosses the threshold within the
  stated budget → the invariant holds; the arithmetic row is the
  finding's spine, and re-pricing after NAT/pool discoveries is
  mandatory, not optional.
* The simultaneous-release date slips per vendor → the disclosure
  engineering failed: file the post-mortem row, re-run M5 with the
  fallback path, never silently convert to drip disclosure.
* The saturation gate is never reached by the deadline → escalation
  per M4's ladder, with the unpatched fraction as the measured
  denominator — extending the deadline silently is the refused move.
* A disagreement cell flips between runs (n=2) → the probe was
  flaky, not the implementation: re-run with n≥3 and record the
  instability as the cell's own data.

## 5. Worked micro-example (numbers consistent, incident fictional)

Class: session-token match invariant across four API gateways of one
internal spec. M1 census: 4 implementations pinned by version,
boundary rows filed (no single-seam ambiguity; no probe-budget
question). M2: match key = 32-bit token, no port-equivalent second
field → average blind attempts 2,147,483,648; birthday structure at
n outstanding = 1,518 for ~50% — thresholds written at budget
B=10,000 probes. M3: probe = token-mismatch rejection observables
across the four gateways; matrix shows one gateway accepting
reordered fields (disagreement cell CONFIRMED at n_runs=3, ledger
R-4xx). M4: rung 2 claimed with denominator 4/4 population, rung 3
parked (no ecosystem root). M5: internal advisory registered,
two-team simultaneous fix date set. M6: post-fix sample on the four
gateways = 4/4 patched, saturation gate met; residual-risk row filed
(32-bit match key remains the stopgap; structural fix = 128-bit key
per spec revision, dated).
