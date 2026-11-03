# The executable method — M1–M4 for prototype-playbook

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The lineage critique that
justifies each step (why these phases exist, what was weak in
Heyes' prototype-pollution research) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M4

### M1 — the merge-surface inventory (before any gadget exists)

Which endpoints merge user-controlled objects into trust-bearing
state? Four probes, all EXPERIMENT records, rate-capped (house civility
floor):

1. **Reflection probes**: POST `{ "a9zq7": "v" }` to JSON-body
   endpoints — any JSON reflection of the key at another depth
   (`o.a9zq7` echo) marks a serializer walk worth mapping.
2. **Merge-shape probes**: nested objects where the engine's merge
   chain is suspected (`{"__proto__": {}}` is M3's treatment; M1 sends
   only benign shapes) — responses whose timing/size class shifts with
   nesting depth are merge candidates.
3. **Stack fingerprints**: version-pin the merge-bearing libraries as
   FACT records — lodash version via `_.VERSION` reflection where
   exposed, jQuery via `$.fn.jquery`, express via `x-powered-by`,
   template engines via error pages. Each pin is the W4 fix.
4. **Sink census**: client globals the app reads from
   `Object.prototype` chains (`config.*`, `window.*` clobber
   interaction with the prototype-playbook corpus's PP-010
   negative-space rule: if nothing reads polluted keys, pollution is
   hygiene, not a finding).

Gate: no gadget hunt starts until the inventory's surface count is
zero or nonzero ON RECORD. Zero merge surface + zero key-readers =
the organ refuses gadget work and says why.

### M2 — the calibrated oracle ladder

Ranking by cost and noise, ENTERED IN ORDER, each step a recorded
observable:

```
O1 read-back    the response reflects the polluted key existing
                (e.g. reflected JSON gains a key) — cheapest, quiet
O2 signature    a DIFFERENT, reproducible error class between
                treatment and control (M3) — the error is evidence,
                the target stays up
O3 crash        REFUSED unless pre-registered, rate 1 req / 30 s,
                max 3 attempts, and the operator informed — the
                DoS-shaped gadget is a last resort, not a habit
```

Two analysts, same traffic, must reach the same hit/no-hit verdict:
the ladder's decision table IS the agreement protocol (the W2 floor
made mechanical).

### M3 — the `__proto__` differential protocol

Per endpoint hypothesis (one merge candidate):

1. **Conditions, n ≥ 5, interleaved**:
   * baseline — benign key `{"a9zq7": "v"}`;
   * treatment — `{"__proto__": {"a9zq7": "v"}}` from the corpus,
     byte-exact;
   * control — `{"constructor": {"prototype": {"a9zq7": "v"}}}` where
     the corpus carries the alternate, else the same shape with a
     benign top-level key (`{"zz9zq": {"a9zq7": "v"}}`).
2. **Observation vector**: response status, length bucket
   [same/±10%/>2×], JSON shape delta (new reflected keys), error
   class.
3. **Confirm rule (all three)**: treatment shows a pollution oracle
   (O1 or O2) in ≥ 4 of 5 AND control shows none in ≥ 4 of 5 AND
   baseline is stable across the interleave.
4. A read-back probe AFTER treatment (fetch the object-echo endpoint)
   that now reflects `a9zq7` where it did not before is the strongest
   O1 evidence — one post-treatment fetch, ledgered with the
   treatment id.

### M4 — the gadget chaining matrix

Pollution is proven; impact is a gadget. One row per gadget EXPERIMENT:

| Column | Content |
| ------ | ------- |
| pollution key | the exact key that must exist (`options.path`, `sanitizeHtml`, `child_process` option names) |
| gadget site | endpoint/component reading the key, from M1's sink census |
| library + version range | pinned from M1 stack FACTs; range from the corpus entry's source |
| effect class | file read / RCE primitive / auth bypass / options override |
| precondition | application-specific merge order (which merge runs LAST wins) |

Rules: a gadget row without all five cells is a parked hypothesis
(resume note), not a finding; the matrix's EFFECT is capped by the
chain-architect ceiling statement — pollution + gadget proven ≠
end-to-end impact claimed.

## 2. Falsifiers — what would prove this method wrong

* The CONTROL also fires O1/O2 → the top-level key shape, not
  `__proto__`, caused the delta: hypothesis dies.
* O1 read-back flips 1 of 5 with clean control → serialization
  jitter: LEAD, re-run with n = 10 before any claim.
* A gadget works with the library OUTSIDE its pinned range → the
  corpus entry's version range is wrong; file a corpus correction.
* M1's census says nothing reads polluted keys, yet a gadget "works" →
  re-derive the census first: the sink census, not the demo, is the
  arbiter (the PP-010 negative-space rule).

## 3. Worked micro-example (numbers consistent, incident fictional)

Express app, `x-powered-by: Express`, `lodash` 4.17.12 exposed via a
reflection path (FACT). M1: `/api/prefs` reflects nested keys at deeper
depth (merge candidate). M3 on `/api/prefs`: treatment
`{"__proto__": {"a9zq": "v"}}` → reflected JSON gains `a9zq` 5/5;
control `{"zz9zq": ...}` → no gain 5/5; baseline stable. O1 confirmed.
M4: gadget matrix row — pollution key `options.deleteFile`, gadget
site `/.well-known/tmp-clean` job, lodash merge-order precondition
runs last, version range pinned to the corpus entry. Ceiling:
pollution + gadget primitive proven; end-to-end file-delete impact
parked pending operator-owned canary file (chain-architect ladder).

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
Gareth Heyes' prototype-pollution art is real — black-box detection,
gadget catalogs, DOM Invader — but it is told through Burp's browser,
single error messages read by eyes, and crash-flavored gadgets. This
module extracts what is tool-agnostic, names the floors, and ships the
replacement: a merge-surface inventory before any gadget, a calibrated
oracle ladder, a differential with a same-shape control, and a
version-pinned gadget matrix. An agent with no Burp license must run
this at his precision.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the published method (context, not steps)

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | Delivery is DOM Invader / Burp Browser — the extension's findings panels ARE the procedure | The method does not transfer: "look at the canary tab" is not a step an agent can run; passive extension heuristics replace surface math |
| W2 | Detection leans on error side effects — gadgets that throw readable errors; the crash-free black-box detection still keys on one observable read by eyes | One error message, one observer, no calibrated oracle: two analysts can disagree on "is this a hit" with no rule to settle it |
| W3 | Gadget hunting BEFORE merge-surface mapping — the published flow finds gadgets in code it already has, not by mapping which endpoints merge user objects into trust-bearing state | Scan-first map-later burns budget on apps whose merge surface is empty (nothing merges user input into `Object.assign`/`defaultsDeep`/settings chains) while looking busy |
| W4 | Library and runtime versions unpinned — gadget writeups rarely record lodash/jquery/express/node versions as data, though gadget behavior is version-bounded | The finding cannot be scoped or re-tested: a gadget claim without a version range is an anecdote |
| W5 | Single-shot narrative — "it polluted Object.prototype" from one request | No n_runs, no same-shape control, no read-back gate: a one-off error from a flaky validator reads as pollution exactly once |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | The merge surface mapped FIRST, from traffic, not from extension heuristics | **M1** — the merge-surface inventory |
| U2 | Detection oracles calibrated and ranked by cost | **M2** — the oracle ladder (read-back → error-signature → crash, refused last) |
| U3 | Pollution claims as differentials with same-shape controls | **M3** — the `__proto__` differential |
| U4 | Gadgets as a version-pinned matrix, not anecdotes | **M4** — the gadget chaining matrix |
| U5 | Byte-exact probes with sources and failure modes | `references/corpus.json` (PP-001…010, shipped v1.1.0) — consumed here, never re-typed |
