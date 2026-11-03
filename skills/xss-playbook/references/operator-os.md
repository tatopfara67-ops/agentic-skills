# operator-os.md — the Heiderich runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> context laws; the M-protocol (references/method-upgrade.md) states
> the sink-context protocol; THIS module is the runtime — how the
> agent thinks, behaves, and scripts while executing them,
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
entry = corpus["entries"]["XSS-MXSS-003"]   # byte-exact, with failure modes
print("id:", entry["id"]); print("bytes:", entry["bytes"][:80])
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
