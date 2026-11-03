# The executable method — M1–M5 for xss-playbook

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The critique that
justifies each step (why these phases exist, what was weak in
the Heiderich–Heyes–Bentkowski corpus) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M5

### M1 — the rendering-context decision table

Before any payload is chosen, the sink's context class is decided by
PROBE, not judgment. One observable: which bucket the browser places
the injected marker into after render.

| Probe sent (marker = `9zq7x` per EXPERIMENT) | Rendered bucket observed | Context class | Grammar family |
| -------------------------------------------- | ------------------------ | ------------- | -------------- |
| `9zq7x` into element innerHTML | Text node, no markup | HTML body | corpus body-class entries |
| `9zq7x` inside a quoted attribute value | Attribute value intact | attr (quoted) | break-out quotes + corpus attr-class |
| `"9zq7x"` in a JS string literal | String content only | JS string | escape-class + `</script` break-out |
| `9zq7x` appended to URL/path | Reflected in href/action | URL context | scheme/encode grammar |
| Raw marker inside `<script>`/`<style>` block | Executes as code/markup | raw text | close-tag grammar |

Rules of the table:

1. Two probes that disagree on bucket = the sink is
   **context-unstable** — an mXSS candidate, promote to M2 with the
   mutation noted (this is the W3 floor made mechanical).
2. The marker is operator-owned and unique per EXPERIMENT (canary
   doctrine); it never appears in any shipped payload grammar.
3. The bucket decision is a CONTROL record citing the probe bytes —
   the report's grammar choice cites this record, not taste.

### M2 — the mutation differential protocol

Per mXSS hypothesis (one mutation class, one corpus probe):

1. **Conditions, n ≥ 5 each, interleaved** (A,B,A,B…):
   * baseline — benign mutation input (`innerHTML = "9zq7x"`), bucket
     recorded;
   * treatment — the corpus mutation probe, byte-exact from
     `references/corpus.json` (re-serialization, namespace confusion,
     or parsing-context switch entry), marker embedded;
   * control — the same probe minus ONE byte that disables the
     mutation trigger (the malformed nesting, the foreign-content
     tag) while keeping length and charset class.
2. **Confirm rule (all three)**: treatment bucket ≠ baseline bucket in
   ≥ 4 of 5 runs AND control bucket == baseline bucket in ≥ 4 of 5
   runs AND no baseline drift across the interleave (else void,
   re-baseline, record the void).
3. The mutated DOM (serialized post-mutation via `js_analyze`
   artifact) is the artifact — the screenshot equivalent, but
   hashable and re-checkable.

### M3 — the sanitizer version-oracle ladder

The corpus's failure modes convert a MISS into a dated FACT:

| Corpus evidence pattern | Oracle reading | Ledger record |
| ----------------------- | -------------- | ------------- |
| Old-generation entries execute, newer fail | sanitizer at least as old as the bypass ceiling of the executing set | FACT: sanitizer ≥ vX.Y |
| All mXSS entries fail, DOMPurify-class signature present | patched or post-fix version | FACT: sanitizer post-fix |
| Failures cite engine-specific mutation | engine, not sanitizer, is the varying half | FACT: engine oracle — pin via M5 |

Run the ladder BEFORE closing any negative hypothesis: an untested
sink with a dated stale sanitizer is itself reportable hygiene (the
organ's rule 4), and the ladder's outcome block is mandatory in the
park/close note.

### M4 — the marker proof (alert() retired)

Execution is proven only by the operator-owned marker:

1. The marker fires **exactly one observable the operator owns** — a
   `http_probe`-visible fetch to an operator-controlled, OUT-OF-SCOPE
   collector with the EXPERIMENT id, or an operator-rendered DOM node
   read back in the same session.
2. CSP is factored FIRST, not after: `Content-Security-Policy` is a
   ledgered FACT before treatment; if inline handlers are blocked, the
   grammar switches to the corpus's CSP-compatible class and the block
   is cited (a CSP block is an untested-execution note, never a
   "safe" verdict).
3. No `alert()`, no screenshot drama: the marker observation is a
   CANARY record citing the operator-captured artifact.

### M5 — the render-environment FACT block

Every render claim pins its engine, recorded before treatments:

```
RENDER-ENV: engine=Blink version=130.0.x platform=Linux headless=no
  evidence=<UA header + engine feature probe> jitter=<n=5 baseline
  bucket stability>
```

Engine class changes re-run M1 (buckets move between engines — this
is the W4 floor). The block rides in every EXPERIMENT record that
reports a render.

## 2. Falsifiers — what would prove this method wrong

* The CONTROL also mutates (bucket shifts in ≥ 4/5) → the trigger
  byte was not the cause; the mutation hypothesis dies.
* Bucket flips in 1 of 5 with no control movement → renderer jitter:
  LEAD, not a finding; the n_runs floor exists exactly here.
* The same corpus entry executes on two engines of the same family at
  the same version → the entry's engine pin is wrong; file a corpus
  correction (the corpus is versioned for precisely this).
* The marker fires on the baseline fetch → collector contamination;
  the canary is dirty, the run is void, re-issue markers.

## 3. Worked micro-example (numbers consistent, incident fictional)

Comment sink, DOMPurify 2.0.x-era target, Blink 130. Baseline: marker
renders as text 5/5. Treatment (corpus noscript-class mutation,
byte-exact): bucket flips to markup-execution 5/5. Control (one
nesting byte removed): text 5/5. Ladder: MathML/svg-class entries
execute, post-2.0.17-class entries fail → FACT sanitizer ≈ 2.0.17-era.
Marker: operator collector fetch with EXPERIMENT id, observed 5/5.
Ceiling: mutation proven at M2 confirm-rule level; severity rides the
chain it enables (chain-architect), not the render itself.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
Heiderich, Heyes, and Bentkowski published real findings — but as
conference demos and writeups told through single screenshots, slides,
and Burp-era habits. This module extracts what is tool-agnostic, names
the mechanical floors of the published method, and ships the
replacement: a rendering-context decision table, a mutation
differential with controls, the sanitizer version-oracle ladder, and
the marker proof. An agent that has never watched a single one of
their talks must run this at their precision.

## 4. Appendix — the lineage critique — six mechanical weaknesses of the published method (context, not steps)

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | Conference-demo epistemology — "Gmail executed it" with one screenshot (the Bentkowski Gmail mXSS reports, the WPES paper's case studies) | One render, one observer, no n_runs, no control rendering. A flaky sanitizer bypass reads as confirmed exactly once; rerun discipline is absent |
| W2 | Payloads told from memory and slides — talks display abstracted payloads, not byte-exact transcriptions with sources | Reproduction becomes a lottery: one wrong quote, one normalizer in the middle, and the mutation dies silently. Byte-exactness was never the published habit |
| W3 | Sink-context classification by expert eyes — the body/attribute/JS-string/URL contexts were applied in narration as judgment | Irreproducible grammar selection: two analysts pick different payload families for the same sink with no protocol to resolve them |
| W4 | Engine and version pinning missing or after-the-fact — mXSS is engine-specific (innerHTML re-serialization differs per engine), yet writeups often name the browser only in passing | The strongest cluster key (engine version) is not recorded as data, so the finding cannot be dated, scoped, or re-tested later |
| W5 | Sanitizer failure read as a dead end — a payload that the sanitizer blocks is retired in the narrative | Failures are version oracles: WHICH entries execute and WHICH fail dates the sanitizer. The published art let that evidence rot |
| W6 | `alert()`-family proof theater — execution proven by dialog screenshots, with no operator-owned marker doctrine | The proof lives in drama, not in an observable the operator owns; it also fails the triage gate (no artifact, no severity) |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Byte-exact payloads with sources and failure modes, versioned | `references/corpus.json` (XSS-001…011, shipped v2.2.0) — this module consumes it, never re-types it |
| U2 | Context selection as a decision table with rendering probes | **M1** — the five-context decision table |
| U3 | Mutation claims as differentials with controls | **M2** — baseline/treatment/control, n ≥ 5, interleaved |
| U4 | The sanitizer version as an actively-read oracle | **M3** — the version-oracle ladder over the corpus |
| U5 | Execution proofs the operator owns | **M4** — the canary-marker proof, CSP-aware |
| U6 | Engine+version pinned before claims | **M5** — the render-environment FACT block |
