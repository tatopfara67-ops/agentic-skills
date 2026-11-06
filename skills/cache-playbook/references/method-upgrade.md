# The executable method — M1–M5 for cache-playbook

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The critique that
justifies each step (why these phases exist, what was weak in
Gil's and Kettle's published work) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M5

### M1 — the cache-key baseline matrix (before any suffix or poison)

For each cached surface, one pairwise EXPERIMENT per input dimension —
two requests differing in EXACTLY one dimension, n ≥ 3 pairs,
interleaved:

| Dimension varied | Probe pair | Keyed (expected) | Unkeyed (evidence) |
| ---------------- | ---------- | ---------------- | ------------------ |
| path suffix | `/acct` vs `/acct/a9zq7.js` | different entries (miss, miss) | SAME entry served (hit on variant) → suffix class is cache-eligible grammar |
| query | `?a9zq7=1` vs `?a9zq7=2` | different | same → query stripped from key |
| request header | custom `X-A9zq7: 1` vs `: 2` | ignored | response body/headers vary BY header value → the header is an unkeyed INPUT (poisoning candidate, M3) |
| cookie | session A vs session B | different (private) | same → shared entry: the WCD precondition is armed |

Observables per fetch: `X-Cache`/`Age`/`CF-Cache-Status` class AND
response body hash. The completed matrix is a CONTROL record — every
later claim cites it. This is the W3 floor made mechanical: the matrix,
not the story, decides what is keyed.

### M2 — the WCD suffix protocol (the deception family)

1. Suffix classes come from the corpus's suffix + delimiter set
   (byte-exact; the Gil class, the delimiter set from the
   Cached-and-Confused corpus entries) — never typed from memory.
2. One suffix class per EXPERIMENT; each candidate suffix is fetched
   at the house rate floor with the operator's OWN session.
3. **Hit rule**: cached-entry evidence (age > 0 / hit class) on a
   dynamic, operator-private response = WCD confirmed at deception
   level; the response body hash is the artifact.
4. **Profile gate**: WCD against profile pages carrying other users'
   data is a P1-class privacy finding and the operator decides
   escalation — the organ runs it against the OPERATOR's own profile
   (borrowed victims are forbidden, W5).
5. Rate discipline: max 1 suffix class per 30 s; the whole suffix pass
   is capped at the civility floor — a cache that never misses under
   suffixing is recorded as rule-negative and closed ON RECORD.

### M3 — the poisoning differential (the unkeyed family)

Per unkeyed input found by M1:

1. **Conditions, n ≥ 5, interleaved**:
   * baseline — plain fetch, response hash recorded;
   * treatment — fetch carrying the poisoning input (unkeyed header
     value / delimiter probe from the corpus, byte-exact) with an
     operator-owned canary marker embedded in the input's reflection;
   * victim fetch — a SECOND operator-owned session fetching the plain
     URL, checking for the canary in the served entry.
2. **Confirm rule (all three)**: treatment responses carry the canary
   in ≥ 4 of 5 AND victim fetches serve the canary in ≥ 4 of 5 AND
   baseline fetches never do (else the cache is unstable → void,
   re-baseline).
3. The victim is operator-owned, ALWAYS — third-party exposure is
   claimed never, only computed from the decay curve and the surface's
   traffic class in the ceiling statement.

### M4 — the served-check decay curve

Impact without decay is a snapshot, not a finding. Post-confirm
served-checks at t = 0 s, 30 s, 2 min, 10 min (operator victim
fetches only):

```
DECAY: entry=<url+key class> hit@0s=5/5 hit@30s=5/5 hit@2m=3/5
  hit@10m=0/5 ttl_class≈120s purge=n/a
```

The curve is a mandatory report block; the impact estimate multiplies
the observed hit window by the surface's request class (from scope
records), with the arithmetic shown — never a bare "users were
affected".

### M5 — the ceiling statement

Mandatory in the report, separating the two families and the levels:

```
FAMILY: {deception|poisoning} KEY-BASIS: {M1 matrix row}
PROVEN: entry stored/served with canary to OPERATOR fetch (n=5/5)
IMPACT: served window {decay curve} × traffic class {scope record}
THIRD-PARTY EXPOSURE: NOT CLAIMED — measured window only
```

Rounding up ("users poisoned") past this block fails the audit like
any uncited claim.

## 2. Falsifiers — what would prove this method wrong

* The CONTROL dimension pair (M1) also converges → the surface is not
  cached at all or keys on nothing: record rule-negative, close.
* The victim fetch serves the canary but the baseline ALSO does →
  origin reflection, not cache: the poisoning hypothesis dies.
* Decay curve shows 5/5 at every checkpoint past the claimed TTL →
  the TTL class estimate is wrong; re-derive before quoting a window.
* Suffix hits appear only on the operator's session with Age > 0 but
  body hash = private data of ANOTHER session → that is a finding,
  AND a stop-and-escalate signal: profile gate trips, operator
  decides (the P1 privacy rule outranks the hunt).

## 3. Worked micro-example (numbers consistent, incident fictional)

Surface `/u/settings`, CDN cache, `x-cache: MISS/HIT` exposed. M1: path
suffix pair converges (hit on `/u/settings/a9zq7.css`), query pair
diverges, custom header pair shows response VARYING by header value →
suffix-eligible + one unkeyed header candidate. M2 (deception):
operator profile fetch at suffix `.css` → Age 47, body hash = operator
private settings → WCD confirmed, profile gate: operator's own data
only, P1 note drafted. M3 (poisoning): treatment with canary header
value 5/5; victim session serves canary 5/5; baseline clean. M4: decay
5/5 → 5/5 → 3/5 → 0/5 (≈120 s window). Ceiling: both families proven
at operator-victim level; third-party exposure stated as window ×
traffic class arithmetic, no headcount drama.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
Gil's cache-deception and Kettle's cache-poisoning art are real — but
told as demo narratives: a guessed suffix, a screenshot of a second
user, a poison fired once. This module extracts what is tool-agnostic,
names the floors, and ships the replacement: a pairwise cache-key
baseline, a suffix decision table, a poisoning differential with
operator-owned victims, a measured decay curve, and a ceiling
statement. An agent that has never opened Black Hat slides must run
this at their precision.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the published method (context, not steps)

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | Suffix guessing by habit — the WCD demos enumerate path suffixes (`.js`, `.css`, `/nonexistent.png`) from intuition | No suffix inventory with expected-status matrix: the hunter burns requests on suffix classes the cache rule provably never caches, while missing the rule's actual grammar (path segments, delimiters, normalization) |
| W2 | Single-shot poisoning demos — poison once, fetch once, screenshot | No n_runs, no interleaved control fetch, no TTL/decay curve: "it was served" once is indistinguishable from a cold-cache coincidence at report time |
| W3 | Cache keys narrated, not measured — "X-Host turned out to be unkeyed!" told as a discovery story | Unkeyedness is a PAIRWISE property of the cache rule, knowable only by differential; the writeup's habit is to assume then confirm once |
| W4 | Method families conflated — deception (the cache stores what it should not) and poisoning (an unkeyed input controls what is stored) mix in one narrative | The two families need different preconditions and different confirmations; a single mental model produces false "poisoned" claims on pure-deception caches and vice versa |
| W5 | Borrowed third-party victims — impact demos that wait for another user to hit the poisoned entry | The victim must be operator-owned (canary doctrine); the published demos needed exactly the rule this organ enforces |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | The cache rule measured pairwise before claims | **M1** — the cache-key baseline matrix |
| U2 | Suffix hunting as a decision table with the corpus's suffix+delimiter set | **M2** — the WCD suffix protocol |
| U3 | Poisoning as a differential with operator-owned victims | **M3** — the poisoning differential |
| U4 | Decay and purge windows measured, not assumed | **M4** — the served-check decay curve |
| U5 | Family separation and impact ceiling on record | **M5** — the ceiling statement |
| U6 | Byte-exact suffix/delimiter probes with sources | `references/corpus.json` (CACHE-001…012; the smuggled chain classes CACHE-011/012 release through the weapons vault) — consumed here, never re-typed |
