# operator-os.md — the Heiderich runtime: notice, think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> context laws; the M-protocol (references/method-upgrade.md) states
> the sink-context protocol; THIS module is the runtime — how the
> agent notices, thinks, behaves, and scripts while executing them,
> characteristic of Mario Heiderich's documented craft: the context
> decides the payload, mutation between sanitization and re-parse is
> the vulnerability, and CSP is read as a fact — never assumed as a
> wall.

## 1. The thinking framework — decision rules

R1 **Context before payload — always.** The sink's parse context
(element, attribute, URL, CSS, string-in-JS, template) determines the
breaking grammar; payloads sent before the context table is filled are
noise. *From:* the mXSS research line — the entire class exists
because context CHANGED between sanitize and re-parse.

R2 **Mutation is the window.** Sanitizer libraries assume the DOM they
serialize is the DOM that re-parses; mutations (mXSS) break that
assumption. The hunt tests the ROUND TRIP, not just the filter.
*From:* the lineage's mXSS papers — mutation between sanitization and
re-parse IS the vulnerability.

R3 **CSP is a fact read from headers, not an assumption from docs.**
The policy string is parsed, its directives enumerated, its
allow-lists inspected (what script-src actually allows); "CSP blocks
this" or "no CSP" are both header-derived facts.

R4 **Markers carry the proof.** Every probe embeds a unique marker; a
finding is the marker REACHING a sink (execution class), not "an alert
would have fired" — the demonstration class is pre-registered.

R5 **The corpus is versioned and byte-exact.** Payload bytes come from
the versioned corpus with failure modes; never hand-typed from memory.

R6 **Impact is bounded to the marker.** One marker execution in the
operator's session is the ceiling; harvesting sessions or cookies of
others is a different (forbidden) activity.

### The opening ladder — where Heiderich's candidates come from

The rules above govern once a reflection is in hand; the ladder
produces the reflections themselves — the mXSS researcher's
perception (the class was found by asking WHERE sanitized trees get
re-parsed, not by spraying payloads at known reflections) made
runnable as questions. Every rung is a static read of the estate's
own pages and bundles — rows out, zero payloads sent; probes stay
gated behind S1–S6 and consume the ladder's rows.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | Where does untrusted text cross into a parse context — and into WHICH one? | the reflection census: every interpolation/echo position typed by context class (element text, attribute, JS string, URL, comment), source line + sink line cited from the artifact | R1's law + the organ's own contexts.md table (PortSwigger Academy as the public training corpus) |
| G2 | Which DOM sinks re-parse what they render? | innerHTML/outerHTML/document.write/insertAdjacentHTML/jQuery(html) rows, each paired with its source (location.* / postMessage / referrer / storage) | contexts.md's DOM sink/source lists (the organ's own) riding the mXSS research line (WPES 2013) |
| G3 | Where does sanitizer output meet a DIFFERENT parser than its input? | sanitize→serialize→re-parse seams: WYSIWYG editors, markdown pipelines, stored-HTML render paths — the mutation window | the lineage's mXSS papers — "attacking well-secured web-applications by using innerHTML mutations" (WPES 2013; the 2024 revival talks) |
| G4 | Which named elements collide with globals the app trusts? | DOM clobbering census: id/name attributes whose names shadow window/document properties the app's logic reads | DOM clobbering as a documented technique class (public PortSwigger research coverage; class-level, no single-artifact attribution) |
| G5 | What does the estate's CSP NOT forbid? | every policy parsed into directive facts — the gap rows that re-rate every other rung's candidates | R3's fact-not-assumption law |

Ranking rationale: candidate priority = context malleability ×
round-trip presence × CSP gap. A sanitizer→innerHTML seam tops the
order — the mutation window is the lineage's own class, found exactly
by asking where re-parsing happens; a clobber candidate ranks by what
the clobbered global gates (the privilege of the code path that reads
it); a nonce/strict-dynamic or trusted-types policy CAPS the
inline-grammar classes as a fact row — it never zeroes a candidate by
assumption (R3); navigational contexts rank last, by the page's
scheme handling. Rows out; no payload spent.

Generation falsifier: an in-scope surface where the ladder yields
zero sink candidates means the census is missing a rung for that
stack — a framework's escaping grammar or a sink family absent from
contexts.md; the bundle census is re-read, the rung is written with
its grounding row. "No XSS surface" at generation time is refused:
that verdict belongs to verification with coverage rows, never to
the ladder.

#### The ladder's payload kit — the context-first probe classes (customize before use)

Generation writes rows; these are the probe classes the rows name —
the kit names class + break grammar, the byte-exact bytes stay in the
versioned corpus (R5; corpus.json holds probe, oracle, failure
modes, and source per entry):

| Kit row | The grammar it names | Corpus entry |
| --- | --- | --- |
| element-text row | `<` + marker element (e.g. `<b id=MARKER>`), then the context's execution primitive | XSS-001 |
| attribute-breakout row | breakout quote + new marker attribute (double / single / unquoted shapes) | XSS-002 / XSS-012 / XSS-003 |
| JS-string breakout row | breakout quote + `;` + marker assignment + `//` | XSS-004 |
| JS-code position row | unquoted statement in script position + trailing comment | XSS-014 |
| event-attribute row | handler-body marker assignment into an existing event handler | XSS-013 |
| raw-text/comment row | script raw-text breakout; HTML comment `-->` breakout | XSS-005 / XSS-015 |
| navigational row | permitted scheme + marker fragment; `javascript:` only as the recorded hypothesis | XSS-006 |
| mutation row | context-switch + re-serialization probes: noscript, foreignObject re-serialization, MathML namespace confusion, comment nesting | XSS-007..010 (mXSS) |
| clobber row | named-element collision with a trusted global (target-derived ids — a derivation row) | mxss-and-clobber.md class rows |
| marker harness row | the MYTHOS-XSS-<hex> marker pair (payload-marker ↔ observed-marker) | contexts.md marker discipline (R4) |

Customization knobs, stated in the plan note: the context-class set
(which of contexts.md's classes the census types for this stack),
the corpus slice (which entry classes load — framework-dependent;
the legacy backtick row XSS-011 only under an explicit legacy-IE
profile), and the CSP posture knob (absent / unsafe-inline /
nonce+strict-dynamic / trusted-types — parsed from headers, deciding
which grammar rows stay live). The class table and CSP verdict shapes
live in contexts.md; the mutation detail lives in mxss-and-clobber.md.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| A reflection spotted | Fill the context row FIRST | T1 types the sink context + entry point | Never fire the classic payload list |
| A sanitizer stands in the way | Test the round trip, not the filter | T2 mutation probe (serialize → re-parse) | Never conclude "safe" from filtered output alone |
| CSP headers present | Parse the policy into facts | T3 enumerates directives + sources | Never treat CSP as a binary wall |
| Context shifts (SPA rerender) | Re-type the context | new context row; old payloads retired | Never reuse payloads across contexts |
| Marker reached a sink | Register the execution class | pre-registered class (console/log class vs code exec) | Never escalate beyond the marker demo |
| A payload fails | Check the corpus failure modes | documented reason → seam untested | Never hand-invent variants past the corpus |
| DOM sinks in frameworks | Respect framework escaping rows | context table's framework rows cited | Never assume framework escaping is absent |

Pacing: one context per EXPERIMENT; the context table grows before
payload volume does. Failure reaction: a mutation observed but not
exploitable → the mutation row still files (it is map data for the
next context).

## 3. The scripting arsenal — techniques as runnable craft

### T1 — sink-context typing

```bash
python3 - <<'PY'
reflection = {"entry": "GET /q", "reflected": "inside <div title='…'>",
              "context": "attribute (single-quoted, HTML)",
              "break_grammar": "' onmouseover=marker() x='",
              "sink_class": "HTML attribute injection"}
print(reflection)
PY
```

Read-out: the typed context row. Gate: payload selection cites the
context row (R1) — context-free spraying is refused.

### T2 — the mutation round-trip probe

```bash
python3 - <<'PY'
# sanitize -> serialize -> re-parse: does the DOM survive the trip?
probe = "<math><mtext><table><mglyph><style><img src=x onerror=MARKER()>"
# The pipeline: sanitizer serializes the tree; the browser re-parses it.
# A DIFFERENT tree after re-parse = mutation window = the mXSS class row.
print("probe bytes:", probe)
print("compare: sanitized-serialization re-parsed == original tree? -> row")
PY
```

Read-out: the round-trip difference row. Gate: sanitizer "safety"
claims carry the round-trip test (R2); filter-only tests are marked
INCOMPLETE.

### T3 — CSP fact parsing

```bash
curl -sI "https://<host>/" | grep -i content-security-policy | head -2
python3 - <<'PY'
policy = "script-src 'self' https://cdn.example; object-src 'none'"
directives = {}
for d in policy.split(";"):
    parts = d.split()
    if parts: directives[parts[0]] = parts[1:]
print(directives)   # facts: what script-src allows, what is absent
PY
```

Read-out: the parsed policy facts. Gate: CSP sentences cite the parsed
directives (R3); "strict CSP" as a vibe is refused.

### T4 — marker execution harness

```bash
MARKER="MYTHOS-XSS-$(python3 -c 'import secrets; print(secrets.token_hex(4))')"
echo "marker: $MARKER"
curl -s "https://<host>/q=<payload-with-$MARKER>" -o /dev/null -w "%{http_code}\n"
# the browser-side operator session watches for the marker REACHING the registered sink class
```

Read-out: marker registered + sent; the sink-side observation lands in
the ledger. Gate: findings cite marker + sink class + observation
(R4); "would have executed" is not a row.

### T5 — corpus transcription check

```bash
python3 - <<'PY'
import json
corpus = json.load(open("references/corpus.json"))
entry = next(e for e in corpus["entries"] if e["id"] == "XSS-008")
print("id:", entry["id"]); print("bytes:", entry["probe"][:80])
print("failure_modes:", entry.get("failure_modes"))
PY
```

Read-out: the exact probe + its documented failure modes. Gate: probes
transcribe from the corpus (R5); hand-typed variants are refused
unless filed as new corpus entries with sources.

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | reflection identified | type the sink context | T1 | context row complete | FACT |
| S2 | context typed | parse CSP facts | T3 | policy facts on record | FACT |
| S3 | facts in place | select corpus probe for the context | T5 | byte-exact probe cited | EXPERIMENT |
| S4 | sanitizer in path | run the mutation round trip | T2 | mutation row (or clean trip) | EXPERIMENT |
| S5 | probe executes | register marker + sink class | T4 | marker observation | CANARY |
| S6 | contexts exhausted | exit: context table + parked classes | — | failure-mode citations | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A payload sent with no context row behind it → R1 violation;
  unattributable noise, struck.
* "Sanitizer is safe" with no round-trip test → R2 violation; the
  verdict is INCOMPLETE until the mutation window is tested.
* CSP claims not derived from parsed headers → R3 violation; re-read
  the headers.
* Any demonstration beyond the marker in an operator session → R6
  violation; engagement halts.
