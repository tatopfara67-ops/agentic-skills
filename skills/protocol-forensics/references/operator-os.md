# operator-os.md — the Kaminsky runtime: notice, think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md §2) states
> the laws; the M-protocol (references/method-upgrade.md) states
> M1–M6; THIS module is the runtime — how the agent notices, thinks,
> behaves, and scripts while executing them, characteristic of Dan
> Kaminsky's documented craft: the class before the product, entropy as
> arithmetic, the population as the denominator, and the fix
> engineered as an event.

## 1. The thinking framework — decision rules

R1 **Name the class before touching a product.** The first written
sentence of any engagement is the census header: "the RFC class, the
suspected load-bearing ambiguity, the population." If the target is
one implementation, this organ is the wrong organ — route to
desync-hunter or the app organs. *From:* the 2008 record — the finding
was never "a BIND bug" but one invariant failing across nearly every
resolver (VU#800113).

R2 **Numbers first, narrative second.** An invariant's strength is a
computed quantity — bits, attempts, birthday factors — produced BEFORE
any claim sentence is drafted. "Weak randomness" is a lead; "16 bits →
32,768 average blind attempts" is a finding-grade number. *From:* the
lineage's own stated specialty, "design-level fault analysis" — and
the entropy arithmetic recorded in the advisories.

R3 **The population is the denominator.** Impact claims about a class
carry a counted or measured population. "Widespread" is refused;
"568,000+ machines" (the 2005 Sony census shape) is a measurement.

R4 **One variable per probe, one probe per invariant.** A disagreement
matrix cell changes because of ONE difference. n_runs ≥ 2 on every
cell that matters — a single observation is weather, not climate.

R5 **The fix is part of the hunt.** Coordinated disclosure here is
infrastructure: vendor matrix, embargo, one simultaneous patch day,
advisory registration. A class-level fix that drips vendor by vendor
re-opens the window it was supposed to close.

R6 **A stopgap is named as a stopgap.** Partial fixes ship with their
residual-risk row, dates, and the structural fix they deferred. Never
let mitigation be reported as closure.

R7 **Humor compresses; the protocol must not.** The lineage's talks
entertain at the cost of executable steps — the operator OS
re-expands every step the talk compressed. When in doubt between a
clever sentence and a runnable table, ship the table.

### The opening ladder — where Kaminsky's candidates come from

The rules above govern the hunt once a class is in scope; the ladder
produces the candidates FIRST — the design-level-fault perception
(the corpus's one repeated move, three times six years apart: read
the SPEC's own ambiguity surface at the population level — DNS 2008,
PKI 2009, Sony 2005) made runnable as questions. Every rung is a desk
question that writes rows — no rung sends a packet to the population,
spends a probe budget, or drafts a vendor matrix; probing stays gated
behind R2/R4 and consumes the ladder's rows.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | Which RFC class does this behavior belong to, and what else implements it? | the census header: class, suspected load-bearing ambiguity, population — the first written sentence of any engagement | R1's class-first law — the 2008 record: never "a BIND bug" but one invariant failing across nearly every resolver (VU#800113, sources.md, full text) |
| G2 | Where does the spec's own text leave room for two legitimate readings? | the ambiguity census: under-specified fields, optional behaviors, silent defaults — the treaty's gray zones, named per RFC section | the treaty premise on record (a specification is a treaty between strangers; each implementation resolves the ambiguities independently — SKILL §0; the PKI-era X.509 structure hunt, sources.md P3) |
| G3 | Which implicit invariants hold the class together, and what is each one's entropy? | the invariant census: entropy × ordering × trust composed — bits, attempts, birthday factors computed per invariant before any claim | L1 heuristic 3 on record (compose the invariant classes — sources.md P3) + R2's arithmetic (the VU#800113 constants) |
| G4 | What is the population, pinned by name and version? | the implementation census: the denominator — every row pinned or marked declined (declines are census bits too) | L1 heuristic 1 on record — the same population-level move three times, six years apart (sources.md P3); R3's 568,000+ Sony count shape |
| G5 | What instrument would SEE this class — and does it exist yet? | the instrument census: the measurement tool per class (a scan, a signature probe, an arithmetic harness) — the corpus ships instruments WITH its findings | L1 heuristic 2 on record (build instruments to see the population — Paketto 2002, worldwide DNS scans 2005, the Conficker scanner 2009; sources.md P3) |

Ranking rationale: candidate priority = ambiguity sharpness ×
invariant weakness × population size. An ambiguity whose backing
invariant computes to weak entropy across a large population ranks
first (the disagreement is priced before it is probed); an
un-instrumented population ranks next (the instrument is built first
— the corpus's own move); a population under 3 parks as a product
review and routes out of this organ; already-patched classes rank by
residual deployment (the saturation gate), not by novelty. Rows out;
not one packet sent.

Generation falsifier: a protocol class where the desk sweep yields
zero rows across every row class means the spec's ambiguity surface
was not observable from the desk (the spec text is not public, or the
class is single-implementation — the boundary rows against
desync-hunter and scan-economist are the recorded routing) — the
census is re-read, the missing rung written with its grounding row.
The class is never excused as "tight spec" at generation time: a
zero-yield verdict belongs to verification's coverage row, never to
the ladder.

#### The ladder's payload kit — the spec-reading rows (customize before use)

Generation writes rows; these are the desk classes the rows name,
every one a reading of the spec's own text and the public
implementation record (no packet exists yet; the probe mechanics live
in T1–T5):

| Desk row | The read payload class | Writes which row |
| --- | --- | --- |
| class-header row | the RFC number, the suspected ambiguity sentence, the population sketch — the census header drafted | census-header row (the engagement's first sentence) |
| ambiguity row | the spec's gray zones per section: optional behaviors, silent defaults, under-specified fields — one reading pair per row | ambiguity row (where two implementations can both be legitimate) |
| invariant row | the composed classes — entropy × ordering × trust — with the computed bits, attempts, and birthday factors | threshold-table row (R2's arithmetic, pre-registered) |
| census row | the implementation pins: name+version per reachable vendor, declines recorded as bits | population row (the denominator, R3) |
| instrument row | the measurement plan: existing tool vs to-be-built harness, with its read-out class | instrument row (the corpus's instruments-with-findings move) |

Customization knobs, stated in the plan note: the protocol class (DNS
vs TLS/PKI vs HTTP framing — which ambiguity families load), the
census depth (internet-scale sample vs named-vendor matrix vs both,
priced per engagement), and the arithmetic policy (which invariant
classes compose — the entropy × ordering × trust subset carried).

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| Operator hands over one product to test | Class-first reflex | Ask: which RFC class does this implement, and what else implements it? Population < 3 → park as a product review | Refuse to run a class hunt on a population of one |
| An invariant "feels weak" | Compute before claiming | Run T2 entropy arithmetic; write the threshold table; only then draft the claim | Refuse the word "weak" without its bits |
| Two implementations disagree | Isolate the variable | One minimal probe per invariant across the population; matrix cell updated | Never change two variables between cells |
| Vendors must be told | Engineer the event | Build the vendor matrix with per-vendor status; propose embargo + simultaneous date; register the advisory | Never ad-hoc email one vendor "for a quick look" on a class finding |
| A patch has shipped | Measure, do not assume | Sample the population post-patch against the saturation gate (T5) | Never report "fixed" from a vendor statement alone |
| The embargo leaks | Execute the fallback on record | Accelerated reveal (the July 21, 2008 shape), documented as the contingency it was planned to be | Never improvise the reveal silently |
| A stopgap is all that landed | Label it | Residual-risk register row with dates + the deferred structural fix | Never round a stopgap up to closure |

Pacing: census (M1) and arithmetic (M2) are desk phases — no packets
to the population until both are ledgered. Failure reaction: a
disagreement cell that fails to replicate is VOIDED and re-run with a
fresh sample — never quietly averaged away.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — implementation census sweep

```bash
# population discovery: pin name+version per reachable implementation
for ns in 8.8.8.8 1.1.1.1 9.9.9.9; do
  dig @"$ns" CHAOS version.bind TXT +short 2>/dev/null | sed "s/^/$ns /"
done
```

Read-out: resolver name/version rows (many servers decline — record
the decline itself as a census bit). Gate: every row pinned or marked
declined; the census is the denominator (R3).

### T2 — collision arithmetic, computed not recalled

```bash
python3 - <<'PY'
import math
bits = 16                      # transaction-ID entropy (VU#800113 constant)
space = 2 ** bits
avg_attempts = space / 2       # expected blind attempts, single outstanding
outstanding = 1                # birthday factor: parallel queries in flight
p_win = 1 - math.exp(-outstanding / space)
print(f"avg_attempts={avg_attempts:.0f} p_win_per_race={p_win:.2e}")
# add source-port entropy (~16 bits) and recompute; show BOTH rows in the table
PY
```

Read-out: attempts + per-race win probability at the stated packet
budget. Gate: threshold table written BEFORE the probe — at what
computed win probability, within what budget, the invariant is
declared broken (R2).

### T3 — disagreement differential probe

```bash
# one invariant, one variable: does each resolver answer the ambiguity the same way?
for ns in $(cat census.txt); do
  dig @"$ns" +noall +comments "<ambiguous-name>" A 2>/dev/null \
    | grep -E "flags|status" | sed "s/^/$ns /"
done
```

Read-out: per-resolver behavior rows → the implementation × invariant
matrix. Gate: n_runs ≥ 2 on every cell that matters (R4); disagreement
is the evidence artifact, not prose.

### T4 — impact denominator measurement

```bash
# sample-based blast radius: count, never adjective
python3 - <<'PY'
import random
pop = [l.split()[0] for l in open("census.txt") if l.strip()]
sample = random.sample(pop, min(len(pop), 384))   # 384 ≈ 95%/5% for large pops
# probe the sample, count affected, extrapolate with the stated confidence
print(f"population={len(pop)} sample={len(sample)}")
PY
```

Read-out: counted denominator with the sampling statement attached.
Gate: no impact sentence ships without this number (R3).

### T5 — post-patch saturation gate

```bash
python3 - <<'PY'
sample, patched, deadline = 384, None, 0.95
# patched = count of sample rows answering with the fixed behavior after re-probe
sat = patched / sample if patched is not None else 0
print(f"saturation={sat:.2%} gate={deadline:.0%} "
      f"{'MEETS' if sat >= deadline else 'BELOW — residual risk row required'}")
PY
```

Read-out: measured deployment vs the engagement's stated gate.
Gate: below gate → residual-risk register row with dates (R6).

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | suspected spec-level weakness | write census header + boundary rows (R1) | — | class, ambiguity, boundary sentences on record | PLAN |
| S2 | header written | census the population, pin versions (R3) | T1 | population ≥ 3 or parked as product review | FACT |
| S3 | population censused | extract implicit invariants; compute arithmetic + thresholds (R2) | T2 | threshold table per invariant | FACT |
| S4 | thresholds pre-registered | run disagreement probes, build the matrix (R4) | T3 | every load-bearing cell n_runs ≥ 2 | EXPERIMENT |
| S5 | disagreement confirmed | ladder impact with a measured denominator | T4 | each rung cites its count | FACT |
| S6 | impact laddered | engineer disclosure: vendor matrix, embargo, patch day, advisory (R5) | — | simultaneous-release plan on record | PLAN |
| S7 | patch day passed | verify deployment as a measurement (R6) | T5 | saturation gate or residual-risk row | FACT |
| S8 | verification ledgered | exit gate: stopgaps named, residual risk dated, records complete | — | residual-risk register closed or dated | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* The arithmetic table is written after the probes → the thresholds
  were post-hoc; the invariant audit is voided and re-run from S3.
* An impact claim cites no denominator → refused at the report gate —
  "widespread" is an adjective, not a measurement (R3).
* A disagreement cell flips between runs without a void record → the
  matrix is unreliable; the census sample is re-drawn.
* A vendor-matrix row shows a drip release with no fallback executed →
  R5 was violated; the disclosure record must say what was risked.
