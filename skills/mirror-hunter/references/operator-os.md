# operator-os.md — the Willison runtime: notice, think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> mirror laws; the M-protocol (references/method-upgrade.md) states the
> eligibility and craft protocols; THIS module is the runtime — how the
> agent notices, thinks, behaves, and scripts while executing them,
> characteristic of Simon Willison's documented craft: name the class
> precisely, treat model output as stochastic, and look for the
> deterministic wrapper the model feeds.

## 1. The thinking framework — decision rules

R1 **Name the class before the payload.** "Prompt injection" is a
class with a defined anatomy: untrusted text becomes instructions to a
system that trusted other text. If the surface cannot be described in
that sentence, it is not this organ's target. *From:* the class was
named in the lineage's October 2022 writing before any technique
existed — naming IS the discipline.

R2 **The model is stochastic; the wrapper is deterministic.** A model
output is a rate, not a fact. The finding lives where the model's
output crosses into deterministic code: a tool call, a fetch, a
template render, a log line. Hunt the WRAPPER's behavior, measure the
MODEL's behavior.

R3 **Eligibility before craft.** The program's eligibility table gates
before the first payload: is an LLM/agent surface in scope, is data
exfiltration in scope, are rate-based proofs acceptable? An
ineligible program gets zero payloads, not quieter ones.

R4 **Markers make the differential.** Every injection probe carries a
unique marker (canary-class); every observation records whether the
MARKER reached the deterministic side. Attribution without markers is
vibes.

R5 **Measure, then report as rates.** "The model leaked" is not a
finding; "marker reached the wrapper in 12 of 30 runs (40%, CI
95% [23–59%])" is. n ≥ 30 for rate claims; both successes and
failures ledgered.

R6 **The exfil ceiling is pre-declared.** What the demonstration is
allowed to move (one canary marker, one operator-owned sink) is
written before the first probe; the proof is the REACH, not the haul.

### The opening ladder — where Willison's candidates come from

The rules above govern once an AI surface is in hand; the ladder
produces the surfaces themselves — the coinage-era perception (the
class was named in reaction to instruction-following models being
WIRED to retrieval and external tools — the surfaces came first in
the noticing, the payloads never existed yet) made runnable as
questions. Every rung is a census read of the estate's pages,
bundles, and program rules — rows out, zero generations spent;
probes stay gated behind the eligibility pin (R3) and consume the
ladder's rows.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | Where does the estate wire model output to deterministic code? | the surface census: agent endpoints, copilot features, chat-with-doc, summarizers, tool-calling paths — each with the wrapper contract (what code consumes the model's call) | R2's law riding the coining essay's trigger — models "wired to retrieval and external tools" (sources.md §1) |
| G2 | Which untrusted text does the model retrieve or ingest? | the channel census: RAG corpora, scraped pages, tickets/mail, uploaded docs, agent context files — every channel feeding text the model did not author | the indirect-injection record (Greshake et al., arXiv:2302.12173 — instructions embedded in retrieved content) |
| G3 | Where does model output get RENDERED rather than used? | the render census: markdown rendering of model output, HTML previews, chat UIs — the exfil-channel shapes (image/link payloads) | the Rehberger exfiltration-chain record (model output rendered as markdown images/links carrying data out) |
| G4 | Which tools can the model call — and who wrote their descriptions? | the tool census: tool list per surface, each tool's privilege and its description's provenance (MCP servers, plugins, skill/context files) | the Invariant Labs record (tool poisoning, rug pulls, cross-server shadowing) + the CSA context-poisoning note |
| G5 | What does the program's eligibility table actually say? | the pin rows: qualifying/ineligible classes, exfil authorization, rate-proof acceptability — negative scope read as data | R3's law + eligibility-and-evidence.md §1.2 (the rules page read directly as primary source) |

Ranking rationale: candidate priority = wrapper determinism ×
channel reach × tool privilege. A surface whose model output feeds a
privileged tool call (mail sender, file writer, SQL runner) tops the
order — the finding lives where output crosses into deterministic
code (R2); a retrieved-content channel ranks by who can write to it
(public web > authenticated collaborator > internal-only); a
render-only surface ranks by whether rendered markdown can carry data
out (the image/link exfil shapes); ineligible surfaces rank zero —
they get no payloads, not quieter ones (R3). Rows out; no generation
spent.

Generation falsifier: an in-scope estate where the ladder yields
zero AI surfaces means the census is missing a rung for that surface
class — a copilot integration, a feature-flagged LLM path the bundle
strings show but the census table does not; the census is re-read
(bundle strings, JS endpoints, docs), the rung is written with its
grounding row. "No AI surface here" at generation time is refused
unless the rows that would show one are themselves on record with
coverage.

#### The ladder's payload kit — the injection-craft row classes (customize before use)

Generation writes rows; these are the craft classes the differential
later loads — every row is marker-carrying and twin-controlled (same
content, one dimension varied), per the craft law (attention is the
interpreter; the catalog lives in injection-craft.md §2):

| Kit row | The craft it names | Catalog entry |
| --- | --- | --- |
| edge-load row | directive placed at the retrieval artifact's edge vs its middle | 2.1 (positional decay) |
| salience row | urgent/loud directive vs quiet twin | 2.2 |
| authority row | developer-voice framing vs user-voice twin | 2.3 |
| commitment row | multi-turn ladder vs cold-open twin | 2.4 (documented class) |
| burial row | directive diluted inside a large benign document | 2.5 |
| smuggling row | token-level / invisible-unicode carriers | 2.7 (CSA-documented) |
| exfil-channel row | markdown image/link payload carrying the marker toward the operator sink | 2.8 (Rehberger class) |
| tool-hijack row | the confused-deputy chain through a privileged tool | 2.10 |
| marker harness row | MYTHOS-<hex> canary + n ≥ 30 rate differential (T2/T3) | R4/R5 + the M-protocol |

Customization knobs, stated in the plan note: the surface set (which
AI surfaces the census types — narrowed to what the eligibility table
actually qualifies), the channel set (which ingestion channels are in
scope and writable by whom — the RAG/collaborator mix), and the rate
budget (generations per differential, guard-on/guard-off rows —
priced before S3 runs). The craft detail and per-entry impact gates
live in injection-craft.md; the eligibility quotes live in
eligibility-and-evidence.md.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| An AI surface spotted in scope | Read the eligibility table FIRST | T1 pins: is the LLM surface authorized, is exfil authorized, what proof class counts | Never fire a marker at an unlisted surface |
| The model "seems" to follow injected text | Convert the seeming into a measurement (R2) | T3 runs the marker differential n ≥ 30; record the rate | Never report a single lucky generation |
| The model calls a tool deterministically | Hunt the wrapper's contract | T4 diffs wrapper behavior: what does the code DO with the model's call | Never claim "full RCE" from one tool invocation shape |
| A defensive prompt ("ignore instructions") is present | It is a fact, not a wall | Record the guard; re-run the differential WITH the guard on; report both rates | Never call a guard "bypassed" from one generation |
| The demo could read real user data | Stay at the ceiling (R6) | canary marker → operator-owned sink; one reach, then stop | Never pull real data through the injection |
| Output looks confident and coherent | Discount confidence, count runs | Confidence is a model property, not evidence (R5) | Never let fluency upgrade a LEAD |
| Rate is borderline (e.g., 40%) | Report the interval | CI stated, both outcomes ledgered | Never round a rate up to "reliable" |

Pacing: generations are the unit of cost — spaced, counted, and
budgeted in the plan note; a rate claim with unknown n is void.
Failure reaction: a guard that suppresses the marker 30/30 is a
recorded NEGATIVE with its own report value (the guard held — under
what conditions?).

## 3. The scripting arsenal — techniques as runnable craft

### T1 — eligibility pin

```bash
python3 - <<'PY'
pin = {
  "surface": "https://<target>/copilot",       # in-scope AI surface?
  "exfil_authorized": True,                    # program policy, quoted
  "proof_class": "rate + deterministic wrapper",
  "sink": "https://<operator-owned-callback>/canary",
}
missing = [k for k, v in pin.items() if v in (None, "")]
print("PIN:", "complete" if not missing else f"missing {missing}")
PY
```

Read-out: the pin record. Gate: `complete` before any probe (R3);
the policy quotes live in the plan note.

### T2 — marker generation (canary-class)

```bash
python3 - <<'PY'
import secrets
marker = "MYTHOS-" + secrets.token_hex(8)
print(marker)   # unique per EXPERIMENT; logged before first use
PY
```

Read-out: the canary marker. Gate: marker pre-registered in the
EXPERIMENT record; probes without markers are refused (R4).

### T3 — the marker differential (rate measurement)

```bash
python3 - <<'PY'
import json, statistics
runs = json.load(open("marker_runs.json"))   # [{marker_emitted, wrapper_hit}]
n = len(runs); hits = sum(r["wrapper_hit"] for r in runs)
p = hits / n
import math
ci = 1.96 * math.sqrt(p * (1 - p) / n) if n else 0
print(f"n={n} hits={hits} rate={p:.0%} CI95≈[{max(0,p-ci):.0%},{min(1,p+ci):.0%}]")
PY
```

Read-out: the rate + interval. Gate: n ≥ 30 for any rate claim (R5);
both guard-on and guard-off rows when a guard exists.

### T4 — deterministic wrapper diff

```bash
# what does the CODE do with the model's call? one variable: with vs without marker
for variant in with_marker without_marker; do
  curl -s -o /dev/null -w "$variant %{http_code} %{size_download}\n" \
    -H "Content-Type: application/json" \
    -d "{\"prompt\":\"<probe-$variant>\"}" "https://<target>/<agent-endpoint>"
done
```

Read-out: wrapper-side behavior pair (status/size/latency class).
Gate: the finding sentence cites the WRAPPER's change, with the rate
from T3 as the mechanism measurement (R2).

### T5 — exfil ceiling harness (operator-owned sink)

```bash
# exactly one canary reach per EXPERIMENT; sink is operator-owned
curl -s "https://<operator-owned-callback>/canary?m=<marker>" -o /dev/null -w "%{http_code}\n"
# then check the sink log for INBOUND reaches during the run window
```

Read-out: inbound reach records at the operator sink. Gate: any reach
of REAL user data or a non-operator sink halts the run (R6).

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | AI surface in scope | pin eligibility + sink + ceiling | T1 | pin complete | PLAN |
| S2 | pin complete | generate + pre-register the marker | T2 | marker in EXPERIMENT record | EXPERIMENT |
| S3 | marker registered | run the injection differential, n ≥ 30 | T3 | rate + CI computed | EXPERIMENT |
| S4 | rate ≥ threshold | diff the deterministic wrapper, one variable | T4 | wrapper behavior pair cited | FACT |
| S5 | wrapper changed on marker | prove the reach at the ceiling, once | T5 | one canary reach, operator sink | CANARY |
| S6 | proof done | report: class + rate + wrapper delta + guard rows | — | all four elements present | REPORT |

## 5. Falsifiers — what would prove this runtime wrong

* A rate claim with n < 30 → void at the report gate (R5).
* An injection claim with no marker in the probe or the record →
  attribution impossible; re-run from S2.
* A "bypass" claim citing one generation → stochastic luck; re-measure.
* A demo that moved anything beyond the declared ceiling → R6
  violation; engagement halts, failure ledger written.
* A guard declared absent without reading the surface's configuration
  on record → the guard row is fabricated; re-census the surface.
