# The executable method — M1–M6 for opsec-discipline

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The critique that
justifies each step (why these phases exist, what was weak in
the published grugq art) is preserved verbatim as the §4–§5
appendix.

## 1. The executable protocol — M1 through M6

### M1 — the operator exposure census

Before the first request exists, one census row per item of
trail the engagement will generate or touch:

```
CENSUS: engagement=<id> frame=<authorized-pentest|bug-bounty>
  row=<credential|egress|tool-fingerprint|comms|data-at-rest|
  report-artifact>
  item=<specific: which account, which chain, which store>
  detection=<target-SOC|client|third-party|future-breach|public>
  attribution=<none|pseudonym|operator-identity>
  removal=<cheap|planned|expensive|impossible>
  rank_score=<detection_weight x attribution_weight>
  boundary=<vs scan-economist / ghost-crawler, one sentence each>
```

Scoring weights are pre-registered per engagement (defaults:
detection 1–3 where future-breach scores 3 and public scores 3;
attribution 1–3 where operator-identity scores 3 and none scores
1; rank = product, max 9). The boundary rows are mandatory:

* vs **scan-economist**: that organ prices the TARGET-side scan
  budget — packets, time, rate-vs-reliability of discovery; this
  organ prices the OPERATOR's whole-campaign footprint, of which
  the scan's visibility is one row among many.
* vs **ghost-crawler**: that organ minimizes TOUCHES on the
  target during passive recon (its trace ledger counts target
  contacts); this organ governs the operator side — who the
  operator is, from where, retaining what.

Gate: census ≥ 3 rows with the arithmetic on record; the
top-ranked rows proceed to M3 mitigation. A census with fewer
than three rows parks the hygiene plan as a reading exercise
(a one-row exposure list is not a census).

### M2 — the adversary-and-secrets gate

Two tables, both on record before the plumbing is built:

| Axis | The table | Source of the method |
| --- | --- | --- |
| Adversaries | intent × capability: target SOC/IR (high intent, medium capability), third parties on the same target (low intent, unknown capability), retention/breach of operator storage (low intent, high capability), comms interception (low intent, high capability) | the 2013 interview: "list your adversaries and group them by intent and capability" |
| Secrets | identity (who the operator is), activity (that this engagement runs), association (operator ↔ client/target link) | the 2013 interview: the three things a clandestine activity must secure — carried over verbatim |

Plus the cover extraction: the ROE/engagement letter is read as
the cover document — what presence is EXPECTED (declared source
IPs, scope, windows, test accounts). "Cover aims to avoid closer
scrutiny" (2014); in the authorized frame the cover is written
by the client, and the gate checks the operator read it before
acting under it.

And the latency budget: a stated number of acceptable
communication/event delays per week ("OPSEC is slow... a
significant part of that cost is efficiency", 2013). The budget
is a permission slip for slowness, priced like any other
resource.

Gate: both tables + the budget exist before M3; an operator who
cannot name the exposure set is running on vibes.

### M3 — the hygiene architecture and the plumbing gate

The lineage's ops architecture, translated to the authorized
engagement:

| Corpus term (2012 deck) | Authorized-engagement translation | The rule |
| --- | --- | --- |
| Operations platform (a modern VT100, dual-use) | the operator console: the agent's working environment, engagement-dedicated | carries no personal accounts or history |
| Staging platform ($HOME, jump box) | per-engagement tooling environment: fresh VM or container, snapshot taken at creation | reverted at closure (M6); never mixed across clients |
| Launch pad (disposable, attack egress) | declared engagement egress: the source the ROE names or the client is told about | declared BEFORE the first request; an improvised mid-engagement chain is concealment, not hygiene |
| Bounces | only where the ROE declares them | never improvised; declared chains only |
| PORTAL (fail-closed hardware) | separation by construction: a credential that CANNOT reach personal ground, a store that CANNOT be written by personal tooling | fail-closed beats fail-open — architecture does the containing that discipline cannot sustain ("reduce the ability to make mistakes", 2012) |

The credential law rides every row: per-engagement accounts and
keys, minted for the engagement, stored separated, rotated or
retired at closure. The Bitcoin rules ("unique, uncontaminated
wallet per cover", 2012) translate to per-compartment resources
generally: nothing financial, registrative, or identifying is
shared across compartments.

The plumbing gate (a recorded checklist, run once, before the
first request):

```
PLUMBING: engagement=<id>
  credentials: per-engagement minted? personal reuse possible? <no>
  egress: declared in ROE or to client? <yes>
  tooling: fresh environment + snapshot? <yes>
  storage: engagement store separated? <yes>
  report drafts: stored in the engagement compartment? <yes>
  gate: PASS | FAIL(<row>)
```

Gate: PASS required. "Paranoia doesn't work retroactively"
(2012) — a FAIL after traffic exists is an incident class (M6
post-mortem), not a checklist item.

### M4 — the communications-event discipline

Every operator communication is an event whose METADATA leaks
before content does ("CEs are natural edges between
communicating parties... directed graph", 2014):

* Timing: correlation in time with engagement events is itself a
  channel; batch and un-hurry per the M2 latency budget
  ("latency is directly correlated to security... distance in
  space and time increases security", 2014).
* Cadence: no schedule regularity that fingerprints the
  operator's timezone and habits ("do not keep regular hours /
  habits (this can reveal your timezone, geographic locale)",
  2012) — translated: engagement comms do not run on the
  operator's personal clock.
* Minimization: shared-context messages — say what is needed, no
  more ("The less said, the safer it is", 2014).
* Boundary row: the disclosure ENGINEERING (multi-party vendor
  coordination, embargoes, the fix event) is protocol-forensics'
  ground; this organ owns only the operator's side — what the
  operator's own messages and timing leak.

Gate: a comms plan row exists (channels, timing rules, batching
policy, who knows what and when); disclosure threads coordinate
with the client per the ROE.

### M5 — the suspect-pool audit

Run at every moment incident response could overlap the
engagement — a live IR investigation, an unexpected incident in
the window, a client anomaly report:

```
POOL-AUDIT: engagement=<id> window=<t0..t1>
  operator_activity_rows=<from the engagement ledger: accounts,
  egress, scope touched, times>
  anomaly_match=<is the operator's activity the ONLY match for
  the anomalous pattern? yes|no>
  third_party_overlap=<any other activity in the window? yes|no>
  finding=<attribution converges on operator | attribution
  stays wide>
  client_notified=<when, on record>
```

The doctrine: "If all students are suspects, all one needs to do
is avoid narrowing the pool of potential suspects" (2013, the
Kim post-mortem) — inverted for the authorized engagement: the
operator cannot control the pool, but must KNOW when the pool
has narrowed to one. When it has, everything anomalous in the
window gets attributed to the operator, including other
people's work — so the client hears it first, on record.

The blending rules (from the 2012 anti-profiling guidelines,
translated): engagement accounts carry no operator-identifying
data (no real-name fragments, no personal handle reuse); where
the ROE REQUIRES attribution of the operator's traffic (the
normal case), the attribution markers are declared — that is
cover, stated, not leakage.

Gate: the audit row exists for every IR-overlap moment, or the
engagement records "no IR overlap risk" with a reason.

### M6 — the closure audit and the post-mortem habit

At engagement end, the 2005 triad applied to the operator's own
artifacts, per ROE and retention policy:

| Triad term (2005) | Closure action | Record |
| --- | --- | --- |
| Destruction | raw target evidence destroyed or returned per ROE | destruction row: item, method, date, witness |
| Data hiding | n/a in the authorized frame — hiding client-held evidence is fraud, out of scope | stated as out-of-scope on record |
| Data contraception | minimize at collection: only what a finding needs; the evidence prophylactic | collection-min rows for anything retained |

Plus compartment retirement: staging snapshot reverted;
per-engagement credentials rotated or retired; infrastructure
released; report archived per client terms. Plus the exit
phase: the five-phase operation frame (target selection →
planning → deployment → execution → **escape and evasion**) —
engagements habitually leave the exit unplanned; the closure
audit IS the exit plan ("the most important part of an operation
is the get away", 2013).

The dossier boundary (house law, overriding the corpus's "no
logs, no crime"): the R-NNN method records are the house's
epistemology — compartmented per engagement, never destroyed;
the triad governs raw evidence and residue only.

And the post-mortem row: every hygiene incident — contamination
(personal ↔ engagement ground touched), profiling (operator
identity leaked into account names or comms), home-base
(personal egress or storage used), reveal (operational detail
disclosed), trust (an undeclared party learned the activity) —
joins the failure-class ledger. The corpus's own method is the
case post-mortem (LulzSec 2012, DPR 2013, Kim 2013); the
upgrade makes the classes reusable instead of per-event.

Gate: closure checklist with retention/destruction rows + the
failure-class ledger updated; an engagement closed without its
retention rows left its trail unpriced at the end.

## 2. Falsifiers — what would prove this method wrong

* An engagement emitting traffic with no M1 census on record →
  the method failed at its own first gate; retroactive paranoia
  does not exist.
* A mitigation built without the M2 matrix → hygiene misdirected
  at a non-adversary (the classic: hiding from the client, who
  already knows).
* A plumbing FAIL discovered after traffic exists and treated as
  a checklist item instead of an incident → W2's failure mode
  recurring inside the upgrade that exists to fix it.
* An IR-overlap moment with no pool-audit row → the suspect-pool
  doctrine was decorative; attribution confusion was left to
  chance.
* A closure without retention/destruction rows → the trail was
  priced at birth and abandoned at death.
* A hygiene incident absent from the failure-class ledger → the
  post-mortem habit (the corpus's core method) did not survive
  the assimilation.

## 3. Worked micro-example (numbers consistent, scenario illustrative)

A bug-bounty engagement on a SaaS target, hygiene priced at start:

M1 census (abridged): row=credential, item=test account on
target's program, detection=client(program portal), attribution=
operator-identity (email used at signup), removal=cheap, rank=
3×3=9. row=egress, item=residential IP + declared toolchain,
detection=target-SOC, attribution=operator-identity, removal=
impossible (already in target logs), rank=3×3=9. row=data-at-
rest, item=screenshots folder, detection=future-breach,
attribution=engagement-only, removal=planned, rank=3×1=3.

M2: adversaries — target SOC (high intent, medium capability:
WAF and rate limits, no IR process published), future breach of
operator storage (low intent, high capability). Secrets —
identity: the program-account linkage; activity: public program,
low secrecy; association: declared by the program itself. Cover:
the program's rules = expected traffic (scope, no DoS, declared
UA where required). Latency budget: 2 comms batches/week.

M3 plumbing: dedicated program account (no personal email
fragments), declared toolchain UA, fresh tooling VM snapshotted,
engagement store created. PASS.

M5 (day 9): an unrelated incident hits the target; the window
overlaps the operator's active testing. Pool audit: operator
activity is NOT the only anomaly (other researchers active on
the public program) → attribution stays wide; row filed, client
not needed (public program, no private channel).

M6 closure: raw requests/screenshots beyond the report's
evidence needs destroyed (destruction row: 214 items, method
shred+overwrite, date); report archived per program terms;
credential retired (rotation row); staging reverted; dossier
R-NNN records compartmented and kept. Failure-class ledger:
empty this engagement — the null row is filed too.

The arithmetic is illustrative; the record shapes are the
deliverable.

## 4. Appendix — the lineage critique — six mechanical weaknesses of the published method (context, not steps)

### The critique

**W1 — The economics never became a table.** The corpus states
the price of OPSEC qualitatively and repeatedly — "OPSEC comes
at a cost, and a significant part of that cost is efficiency.
OPSEC is slow" (2013); "compartmentation is expensive and
fragile" (2013); "increased OPSEC security comes at the cost of
efficiency" — but never once tables a priced row. No budget
arithmetic, no rank, no latency number. The teaching works as
rhetoric and fails as procedure: an operator told OPSEC "costs"
cannot decide WHICH hygiene to buy.

**W2 — Prohibitions without recovery.** The Ten Hack
Commandments (2012) are ten "nevers" — never trust anyone, never
contaminate, never operate from home. What the corpus never
states: what to DO when a commandment is already broken. The DPR
post-mortem shows a backstop-less cover failing link by link,
but the response to discovered contamination is implied (flee,
re-compartment?) never stated. Prohibition-only method leaves
the operator sinless until the first accident, then helpless.

**W3 — Post-mortems ad hoc, never a taxonomy.** The LulzSec
violations are tagged one slide each (2012); the DPR chain drawn
once (2013); the Kim five-phase analysis run once (2013); the
Hezbollah rollback once (2013). Each is excellent; the corpus
never compiles them into reusable failure classes, so every
reader re-derives the taxonomy from scratch. The corpus's own
instruction — "read about other people's failures" (2014) — is
method without the machine.

**W4 — The architecture is clandestine-only.** Ops platform,
staging, launch pad, bounces, PORTAL — described for operators
hiding from states, purchased in Bitcoin over Tor. The dual-use
translation to the authorized engagement (where the "adversary"
is the client's own SOC, the cover is the ROE, and hiding from
the client is out of scope) is left entirely to the reader, and
most readers will read "hide" where the method says "separate".

**W5 — Two eras, never one lifecycle.** The anti-forensics era
(2002–2005: destruction, hiding, contraception — data at rest)
and the OPSEC/COMSEC era (2012–2014: cover, concealment,
compartmentation — behavior in flight) are the same discipline
at different phases of an operation, but the corpus never joins
them: nothing states that contraception at design time,
compartmentation during flight, and destruction at closure are
one operator-side lifecycle.

**W6 — Era-bound tools, no porting rule.** PORTAL's TP-LINK
models (2012), Pond (2014, retired), Tor Browser Bundle advice
(2013), the VPN-v-Bitcoin purchase ritual — every named product
is dead or dated, while the principles outlive them all. The
corpus never states the porting rule (check the property, not
the product), so each tool's death takes a chunk of apparent
method with it.

### The upgrades table — and where they land (context, not steps)

| Weakness | The upgrade | Where it lands |
| --- | --- | --- |
| W1 economics unpriced | exposure census with detection × attribution × removal pricing; latency budget as a stated number | M1, M2 |
| W2 no recovery path | contamination as a declared incident class with a response (contain, assess spread, re-compartment, record) | M3 gate, M6 ledger |
| W3 ad hoc post-mortems | the five failure classes (contamination, profiling, home-base, reveal, trust) as reusable audit rows | M6 |
| W4 clandestine-only architecture | the translation table: ops platform → operator console, staging → per-engagement tooling, launch pad → declared egress, PORTAL → separation by construction | M3 |
| W5 two eras, no lifecycle | M1→M6 runs census-before, hygiene-during, closure-after as one lifecycle with the 2005 triad at the end | the whole protocol |
| W6 era-bound tools | the principles-over-products law: every named tool is an example, never a dependency; the scripts check properties, not products | M3, the arsenal |

## 5. Falsifiers for the critique (kept from the lineage's own standard)

The critique is honest only if the corpus could refute it: a
priced-row table, a contamination-recovery procedure, a
failure-class taxonomy, an authorized-engagement architecture, a
unified lifecycle, or a porting rule — published anywhere in the
grugq corpus — would void the corresponding W-row. The census
(read ledger, sources.md §1) is the evidence that none exists;
the 2022 re-serveed keynote still ships the 2012 commandments
unpriced.
