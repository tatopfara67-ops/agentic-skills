# operator-os.md — the Ollam runtime: think, behave, script

The A17 layer of threshold-hunter (the 31st operator-os module on
record): the runtime that executes the organ's method (the M1-M6
protocol in method-upgrade.md). Everything here is behavior, not
biography — the lineage's decision logic re-expressed as rules the
operator runs. The hands-on physical craft that produced this logic
is bounded knowledge (sources.md records it; the runtime never
executes it).

## 1. The thinking framework — decision rules

* **The Eyes-of-a-Thief loop (perception before action).** The
  lineage's own training talk is a perception drill: "here's what
  you see; now here's what I see" — the same surface, annotated
  with exploit-annotated attention. The operator's version: every
  surface in scope gets a second reading where each element is
  tagged with what it assumes, what it costs to defeat, and what
  it leaks. The first reading maps; the second reading hunts. Do
  not probe a boundary until the second reading is done.
* **The Antwerp wall (attack the adjacent component).** The vault
  door had every sensor; the wall had none — the investment
  concentrated on the NAMED interface while the adjacent component
  carried the boundary. The operator's question at every trust
  edge: where did the investment concentrate, and what is the
  adjacent, less-loved component that actually holds the line?
  (In the web translation: the guarded login form vs the
  unguarded reset flow; the authenticated API vs the pre-auth
  status endpoint; the hardened front door vs the webhook
  receiver.)
* **The observation phase (parking lot before door).** The
  Darknet Diaries record opens with the car in the parking lot:
  watching who enters, who patrols, where the motion is. Inference
  from behavior, not assumption: the guards never leave the desk,
  therefore the perimeter's back doors are the soft surface. The
  operator's version: baseline the target's normal traffic,
  cadence, and response shapes BEFORE the first probe — the
  anomaly budget is spent against a measured normal, never a
  guessed one.
* **The 100%-entry reframing (measure the response, not the
  entry).** "You're always gonna get in ... The question is are we
  detected? Is there a response? How competent is that response?"
  The operator treats entry as the given and the detection ledger
  (M5) as the real measurement instrument — an engagement that
  reports only "I got in" has reported nothing.
* **Resist, Recognize, React (the measurement frame).** The
  lineage's Secure360 formulation: all security fails eventually;
  what matters is how well defenses resist, recognize, and react.
  Every boundary in the report is scored on those three axes, in
  that order.
* **"Good enough, consistently" (the economics of technique).**
  The lineage's documented preference — keep looking for the
  simpler entry even when a workable one is in hand; the cheap
  exploit is the report's headline because it is the one the
  client can actually fix and the one an unskilled adversary
  can actually repeat. Skill is spent on the ladder's order, not
  on its deepest rung.
* **The deliverable is the value.** "The value isn't in the
  success of the tester. It's in the deliverable. It's in the
  report, the knowledge that they will give you." The operator's
  output is the report row, the evidence chain, the fix-pair —
  never the trophy. This is the same doctrine the house's report
  templates enforce; here it arrives from the physical domain,
  on record, in the lineage's own words.

## 2. The behavioral protocol — situation, move, refusal

* **R1 — a boundary enters scope.**
  Move: second reading (perception loop), then the ladder, rung
  R0 first, every verdict to the ledger. The cheapest successful
  rung becomes the boundary's headline finding, permanently.
  Refusal: none at entry — the ladder itself is the discipline.
* **R2 — the ladder reaches a life-safety surface.**
  (Fire panels, suppression, emergency broadcast, lockdown
  controllers, and their protocol equivalents — emergency
  endpoints, kill switches, safety interlocks.)
  Move: census and document the surface, its trust model, and its
  evidence trail; write the resist row from passive observation
  only.
  Refusal: no actuation, no state-changing test traffic, ever.
  The refusal row is written to the ledger as protocol compliance.
* **R3 — a human stands between the operator and the boundary.**
  (Pretexting would help: a cover story, a borrowed authority, an
  impersonated vendor.)
  Move: none. Record what the boundary's human layer costs and
  report it as a finding (the social layer is a real control).
  Refusal: this organ does not deceive persons — no fake badges,
  no borrowed trade identities, no pretext scripts. The lineage's
  human social craft is bounded knowledge, not agent runtime.
* **R4 — a rung fails.**
  Move: record the failure verdict with its evidence artifact and
  advance to the next rung. A boundary that survives the whole
  ladder is the resist measurement — a positive finding, not a
  silence.
  Refusal: skipping the recording to "save time" — the ledger
  without negatives is a ledger without measurements.
* **R5 — the probe cadence feels productive.**
  Move: hold the pacing to the measured normal (R1's baseline);
  the anomaly budget is a budget because detection is a finding
  to measure, not an obstacle to defeat. When the surface
  challenges (WAF, rate limit, captcha), log the challenge class
  and its latency — that IS the recognize row.
  Refusal: escalating rate or volume to "get through" — the
  recognize row is data; burning it is destroying the
  measurement.
* **R6 — engagement close.**
  Move: run the detection ledger summary (Resist/Recognize/React
  per boundary), close every finding with its fix-pair, and hand
  the report to the auditor's grounding gate.
  Refusal: closing with a finding that lacks its fix-pair, or a
  boundary with an unexplained empty detection ledger.

## 3. The scripting arsenal — techniques as runnable craft

All five tools are read-only, operator-side planning and analysis
aids. None of them touches the target (T3 and T4 plan requests;
execution routes through http_probe and the engagement's ROE);
T1 is pure offline arithmetic. They are the information-layer
translation of the lineage's field kit — the kit that a
protocol-bound agent can actually carry.

### T1 — the Wiegand 26-bit decoder/encoder

```python
#!/usr/bin/env python3
# T1: decode/encode the standard 26-bit Wiegand credential format
# (H10301). Pure offline bit math — no RF hardware, no capture.
# Structure: bit 1 even parity over bits 1-13, bits 2-9 facility
# code (8 bits), bits 10-25 card number (16 bits), bit 26 odd
# parity over bits 14-26. Use: sanity-check any 26-bit credential
# structure observed in scope (M4's structure table, rung R3 of
# the ladder). Read-only; prints to stdout.

import sys

def bits_from_int(value, width):
    return [(value >> (width - 1 - i)) & 1 for i in range(width)]

def encode(facility, card):
    if not (0 <= facility < 256 and 0 <= card < 65536):
        raise SystemExit("facility 0-255, card 0-65535")
    b = [0] + bits_from_int(facility, 8) + bits_from_int(card, 16) + [0]
    b[0] = sum(b[0:13]) % 2            # even parity over left 13
    b[25] = 1 if sum(b[13:26]) % 2 == 0 else 0  # odd over right 13
    raw = int("".join(map(str, b)), 2)
    return raw, "".join(map(str, b))

def decode(raw):
    b = bits_from_int(raw, 26)
    facility = int("".join(map(str, b[1:9])), 2)
    card = int("".join(map(str, b[9:25])), 2)
    even_ok = (sum(b[0:13]) % 2 == 0)
    odd_ok = (sum(b[13:26]) % 2 == 1)
    return facility, card, even_ok, odd_ok

if __name__ == "__main__":
    if len(sys.argv) == 3:                     # encode FC CN
        raw, pattern = encode(int(sys.argv[1]), int(sys.argv[2]))
        print("raw: %d  hex: 0x%07X" % (raw, raw))
        print("bits: %s" % pattern)
        print("ASSUMPTION ROW: formatted, not authenticated — "
              "cloneable/replayable class (M4 gate)")
    elif len(sys.argv) == 2:                   # decode raw
        raw = int(sys.argv[1], 0)
        fc, cn, ev, od = decode(raw)
        print("facility: %d  card: %d" % (fc, cn))
        print("parity: even=%s odd=%s" % (ev, od))
        if not (ev and od):
            print("VERDICT: parity FAIL — structure rejected")
        else:
            print("VERDICT: structure valid; authenticity is a "
                  "separate audit row (M4)")
    else:
        print("usage: wiegand26.py <facility> <card> | <raw>")
```

### T2 — the entry-ladder ledger

```python
#!/usr/bin/env python3
# T2: render and validate the M1 ledger. The ladder is an ORDER,
# not a menu — this tool enforces it. Reads a JSON file of rung
# rows; validates completeness, ordering, and verdict values;
# prints the boundary's headline (the cheapest successful rung).
# Read-only; writes nothing but stdout.

import json, sys

RUNGS = ["R0-open", "R1-installation", "R2-default",
         "R3-credential-format", "R4-protocol-logic",
         "R5-cryptographic"]
COST = {r: i for i, r in enumerate(RUNGS)}
VERDICTS = {"worked", "failed", "n/a", "skipped"}

def check(rows):
    seen = {}
    for row in rows:
        rung = row.get("rung")
        if rung not in COST:
            return "unknown rung %r" % rung, None
        if row.get("verdict") not in VERDICTS:
            return "bad verdict %r" % row.get("verdict"), None
        if row.get("verdict") == "skipped" and not row.get("reason"):
            return "skipped rung without reason: %s" % rung, None
        if not row.get("evidence") and row.get("verdict") != "n/a":
            return "rung without evidence artifact: %s" % rung, None
        seen[rung] = row
    for rung in RUNGS:
        if rung not in seen:
            return "missing rung %s" % rung, None
        if seen[rung]["verdict"] == "skipped":
            continue
        for cheaper in RUNGS[:COST[rung]]:
            if seen[cheaper]["verdict"] not in VERDICTS - {"skipped"}:
                if seen[cheaper]["verdict"] == "skipped" \
                        and not seen[cheaper].get("reason"):
                    return "cheap rung unresolved: %s" % cheaper, None
    worked = [r for r in RUNGS if seen[r]["verdict"] == "worked"]
    headline = min(worked, key=lambda r: COST[r]) if worked else None
    return "OK", headline

if __name__ == "__main__":
    rows = json.load(open(sys.argv[1]))
    verdict, headline = check(rows)
    print("ladder check: %s" % verdict)
    if headline:
        print("HEADLINE (cheapest success): %s — report this, "
              "not the deep rung" % headline)
    else:
        print("no rung worked — resist row is the finding")
```

### T3 — the egress-surface enumerator

```python
#!/usr/bin/env python3
# T3: generate the M2 egress census plan for a host — the
# exit-only surface candidates ("opens from the inside" class).
# PLANNING ONLY: prints the probe plan and trust-model rows; the
# requests themselves route through http_probe under the ROE.
# Life-safety-class surfaces are flagged read-only/no-actuation.

import sys

EGRESS_PATTERNS = [
    ("health/status", ["/health", "/healthz", "/status", "/ready",
                       "/metrics", "/api/health"]),
    ("pre-auth", ["/login", "/forgot", "/reset", "/signup",
                  "/api/public"]),
    ("unsubscribe", ["/unsubscribe", "/u/", "/opt-out",
                     "/notifications/off"]),
    ("webhook/callback", ["/webhook", "/callback", "/hooks/",
                          "/api/callback"]),
    ("error/recovery", ["/error", "/500", "/recover"]),
    ("emergency-class (READ-ONLY)", ["/shutdown", "/kill",
                                     "/panic", "/emergency"]),
]

def plan(base):
    print("M2 egress census plan for %s" % base)
    for label, paths in EGRESS_PATTERNS:
        for p in paths:
            flag = " [NO-ACTUATION: R2]" if "READ-ONLY" in label else ""
            print("  %-28s %s%s" % (label, p, flag))
    print("per surface, record the trust model row:")
    print("  stimulus | assumption-about-source | state-changed")

if __name__ == "__main__":
    plan(sys.argv[1] if len(sys.argv) > 1 else "https://TARGET")
```

### T4 — the OR-probe matrix planner

```python
#!/usr/bin/env python3
# T4: plan the M3 component-isolation matrix. Given the baseline
# request and the OR-composed components C1..Cn, emits one planned
# request per component (exactly one varies — the M3 gate), paced
# per the civility default. PLANNING ONLY; execution routes
# through http_probe after scope_check. Attribution row is
# mandatory: the attack class is Matt Blaze's rights-amplification
# (2003), taught publicly by the lineage (HOPE 9).

import json, sys

def plan(baseline, components, delay=0.25):
    out = []
    for comp in components:
        out.append({
            "request": baseline, "set_exactly_one": comp,
            "others": "baseline (unchanged)",
            "pacing_delay_s": delay,
            "ledger_note": "oracle answer -> open/no-open",
        })
    print(json.dumps(out, indent=2))
    print("GATE: exactly one component varies per request;")
    print("a probe varying two is uninterpretable — reject it.")
    print("ATTRIBUTION: rights-amplification, M. Blaze 2003 "
          "(IEEE S&P); taught by the lineage, HOPE 9 2012.")

if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1]))
    plan(cfg["baseline"], cfg["components"], cfg.get("delay", 0.25))
```

### T5 — the detection-ledger formatter

```python
#!/usr/bin/env python3
# T5: close the M5 measurement. Reads the engagement's detection
# rows (JSON), classifies response signatures, computes the
# first-anomaly-to-first-challenge latency in code (never by
# eye), and prints the per-boundary Resist/Recognize/React
# summary the report ships. Read-only.

import json, sys

CLASSES = ("waf-block", "rate-limit", "challenge",
           "alert-signal", "no-response")

def summarize(rows):
    lat = [r["t"] for r in rows if r["class"] == "alert-signal"]
    chal = [r["t"] for r in rows if r["class"] == "challenge"]
    recognize = "yes" if (lat or chal) else "NO (finding)"
    react = ("%ds anomaly->challenge"
             % (min(chal) - min(lat))) if lat and chal else "no pair"
    resist = sum(1 for r in rows if r.get("rung") == "failed")
    print("Resist:    %d ladder rungs held (failed verdicts)" % resist)
    print("Recognize: %s" % recognize)
    print("React:     %s" % react)
    empty = not any(r["class"] != "no-response" for r in rows)
    if empty:
        print("GATE: empty detection ledger — declare "
              "detection-free ON RECORD (a finding) or repair "
              "instrumentation before close.")

if __name__ == "__main__":
    summarize(json.load(open(sys.argv[1])))
```

## 4. The rigid run-order — step by step

* **S1 — inventory.** Enumerate the in-scope
  access-control-adjacent surfaces (procedure step 1). Out-of-scope
  devices: BOUNDED rows, no probes.
* **S2 — second reading.** Run the perception loop over the
  inventory; baseline normal traffic; tag each element's
  assumptions. No probes yet.
* **S3 — the ladder.** M1 rungs R0-R5 per boundary, T2 validating
  the ledger, cheapest-first enforced, every verdict recorded.
* **S4 — the reversal.** M2 egress census (T3 plan, http_probe
  read-only execution), trust-model rows, external
  triggerability tested on non-life-safety surfaces only.
* **S5 — the oracles and the formats.** M3 matrix (T4 plan) on
  every OR-composed decision point; M4 structure tables (T1 for
  Wiegand-shaped rows) on every observed credential.
* **S6 — the close.** M5 detection ledger (T5 summary), M6
  fix-pairs on every finding, report through the spine's
  templates, auditor's grounding gate last.

## 5. Falsifiers — what would prove this runtime wrong

* An engagement whose boundaries all resist the cheap rungs and
  fall only at R5 — the ordering thesis weakens; the failed-rung
  rows on record are the evidence either way.
* An OR-composed system that never leaks under isolation — M3's
  negative accumulates toward a population claim.
* A scope with no access-control-adjacent surfaces at all — the
  organ must report BOUNDED and stand down rather than
  fabricate relevance.
* A detection ledger that contradicts the report's narrative
  (challenges logged as failures, latencies miscomputed) — the
  T5 arithmetic is the ground truth; the narrative loses.
