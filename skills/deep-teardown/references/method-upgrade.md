# The executable method — M1–M5 for deep-teardown

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The lineage critique that
justifies each step (why these phases exist, what was weak in
Hotz's public teardowns) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M5

### M1 — the artifact pin

```
ARTIFACT: name=<app> platform=<ios|android|web|binary> build=
  <exact version/build id> hash=<sha256> acquired=<source+date>
  scope-basis=<program covers this build class>
```

Every finding cites the pin (W4); a teardown without a pin is
unusable by anyone including its author next week. The pin is the
claim's scope contract.

### M2 — the gated ladder (intuition, externalized)

The rungs in fixed order; each rung GATES the next by producing
its declared output, on record:

| Rung | Action | Gate output (must exist to descend) |
| ---- | ------ | ------------------------------------ |
| R1 unpack | archive→components | component inventory with hashes |
| R2 deobfuscate | packed/minified→readable | de-obfuscated main bundle + map of renames |
| R3 sourcemap/dex | restore names where possible | symbol table with provenance (M3 grades) |
| R4 strings/secrets | full-dump + classification | secrets/endpoint catalog |
| R5 structure | classes/flows→business logic map | the reconstruction (M4 confirms) |

A skipped rung is recorded as SKIPPED-with-reason (impossible,
not convenient) — the ladder is a checklist with teeth, not a
suggestion (W2, W5).

### M3 — the symbol-trust table

Every symbol that carries a conclusion is graded:

| Grade | Meaning | Allowed use |
| ----- | ------- | ----------- |
| V-verified | behavior confirmed by M4 dynamic observation or code-path read to the call | load-bearing in findings |
| P-provisional | name+context consistent, path NOT walked | hypothesis labeling only |
| U-untrusted | from obfuscated/packed regions, anti-analysis suspects, or contradicts another symbol | never load-bearing; contradictions recorded |

Rule: a finding whose severity rests on a P-grade symbol is a
hypothesis, not a finding (W3).

### M4 — the cross-check (static proposes, dynamic disposes)

Per reconstructed business-logic claim (auth flow, privilege gate,
endpoint behavior):

1. Static claim stated as a prediction: "parameter X gates action Y
   client-side" → dynamic prediction: "omitting X still succeeds /
   fails".
2. Dynamic probe on operator-owned test accounts/devices, n ≥ 3
   (the mobile-hunter marker habit); observation buckets recorded.
3. **Confirm rule**: static prediction matches dynamic bucket in ≥
   2 of 3 → claim CONFIRMED and its symbols upgrade to V; mismatch
   → the static map is wrong at that node — record the correction
   (the tear-down's own error becomes data).

### M5 — the budget + coverage row

```
TEARDOWN-BUDGET: artifact=<pin> budget=<hours/units by rung>
COVERAGE: classes-total=<n per R5 map> examined=<n> untouched=
  <classes named> completeness=<%> "nothing-else-found" claim:
  <valid only at 100% coverage, else bounded to examined set>
```

The heroics become arithmetic: read-it-all is a number, and the
report's negative claims are bounded by it (W5).

## 2. Falsifiers — what would prove this method wrong

* A V-graded symbol's behavior fails to reproduce on a second build
  → the pin's scope contract was too broad: narrow it, downgrade
  cross-build claims to hypotheses.
* The M4 probe contradicts a confident static map → the map wins
  NOTHING: dynamic observation disposes; record which rung's gate
  let the wrong symbol through and tighten it.
* Coverage row shows < 70% at budget exhaustion → "nothing else
  found" is forbidden; untouched classes are named as open surface
  with resume notes.
* Two analysts' R5 maps differ structurally → rung gates were
  satisfied differently: the gate outputs are compared
  hash-by-hash; the divergence localizes to a rung, and the ladder
  spec — not the analyst — is corrected.

## 3. Worked micro-example (numbers consistent, incident fictional)

Android app, build 8.12.4, pinned sha256. R1: 214 components
inventoried. R2: main bundle de-obfuscated, rename map kept. R3:
symbol table — 61% P-grade (obfuscation survivors), 12% U (anti-
analysis class names contradicting string evidence). R4: secrets
catalog — 3 ghost endpoints (dead in static, M4 will dispose).
R5: business-logic map, 44 classes. M4 on claim "client-side
is-rooted check gates premium flow": omitting the check on
operator test device → premium still gated server-side 3/3 →
static claim REFUTED, node corrected, check-symbol stays P. M5:
coverage 38/44 examined (86%), untouched 6 classes named with
resume notes; "nothing else" bounded to the examined set.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
George Hotz's art is real — first iPhone SIM unlock, the PS3 work,
streams of live reverse engineering — but the published form has
floors: teardowns performed as unrecorded streams, intuition
replacing ladders, symbols trusted without bounds, and the
read-it-all heroics never budgeted. This module extracts what is
protocol-shaped and ships the replacement: artifact pinning, a
ladder with per-rung completeness gates, a symbol-trust table, a
static-vs-dynamic cross-check, and a teardown budget. An agent with
no stream audience must run this at its depth.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the published method (context, not steps)

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | Teardowns as streams — the method is PERFORMED live; what survives is the highlight reel, not the process record | Nothing replays: a second analyst cannot re-walk the path, and the hunter themselves (next session) inherits their own summary, not their method |
| W2 | Intuition as the ladder — "you just look at the strings around the crypto init" is the taught move | The ladder of where-to-look-next is in the demonstrator's pattern memory; without written rungs and gates, two analysts teardown the same binary to different maps with no arbiter |
| W3 | Symbols trusted unbounded — function names, class names, and debug strings are read as ground truth about behavior | Stripped, obfuscated, or LYING symbols (anti-analysis naming) flow straight into conclusions; the symbol-to-behavior link is asserted, never verified where it matters |
| W4 | Version pinning as afterthought — "this was on iOS x" mentioned in passing, never as the claim's scope contract | A teardown finding's scope IS the artifact version; the published form lets findings float free of their build and overclaim across versions |
| W5 | Read-it-all heroics unbudgeted — the stream runs for hours; coverage is felt ("I've been through most of it") | No completeness accounting: which classes of the artifact were examined vs untouched is unknown, so "nothing else found" is unprovable every time |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Every teardown a re-walkable record | **M1** — the artifact pin |
| U2 | The ladder written, with gates | **M2** — the gated ladder |
| U3 | Symbols graded by verification | **M3** — the symbol-trust table |
| U4 | Static claims cross-checked dynamically | **M4** — the cross-check |
| U5 | Coverage accounted, budget declared | **M5** — the budget + coverage row |
