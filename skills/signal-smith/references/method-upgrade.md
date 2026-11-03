# The executable method — M1–M5 for signal-smith

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The lineage critique that
justifies each step (why these phases exist, what was weak in
the Draper-era signal record) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M5

### M1 — the calibration table (the grammar, measured)

Before any payload is forged, the validator's expected grammar is
measured with benign inputs, each cell a FACT:

```
CALIBRATE: surface=<param/endpoint> type=<int|string|enum|...>
  length-range=<min..max observed> charset-classes=<observed>
  encoding=<form|json|...> rate-limit=<observed threshold>
  rejection-classes=<how invalids are answered, verbatim>
```

Rules: every cell comes from ≥ 3 benign observations; the rejection
classes are recorded VERBATIM (the error text is the validator
talking — its dialect is data). An uncalibrated surface is a
refused forge (W1, W2).

### M2 — the seam map (two parsers, one payload)

Where a frontend normalizes and a backend re-interprets, the seam
is mapped with pair-probes (n ≥ 3, interleaved):

| Probe pair | Seam evidence |
| ---------- | ------------- |
| NFC vs NFD unicode form of the same glyph | divergence in stored/echoed form names a normalization seam |
| `+` vs `%20` vs raw space | accepted-differently names an encoding seam |
| duplicate parameter (`a=1&a=2`) | which value each layer reads names a parse-order seam |
| overlong length at boundary (max, max+1) | clamp vs reject names a length seam |

Each seam is a CONTROL record the forge cites: the payload is
SHAPED to fall INTO a seam (W5's layers, separated and used).

### M3 — the in-band differential (indistinguishable, tested)

The claim "the forged signal is indistinguishable from legitimate"
is an experiment, not a mood:

1. **Conditions, n ≥ 5 each**: legitimate-benign signal (valid
   grammar, harmless content) vs forged signal (seam-shaped, attack
   content) — interleaved.
2. **Blind judge**: the surface's OWN response classes are the judge
   (status/length/error-class buckets); where a human must judge
   (rendered output), the judge sees relabeled shuffled artifacts
   and must classify each as legit/forged.
3. **Indistinguishable rule**: judge-class identical across
   conditions in ≥ 4 of 5 pairs. Accepted-but-distinguishable
   (judge separates them) is a DIFFERENT finding class — recorded
   as accepted-with-tells, and the tells are named (W3).

### M4 — the precision budget (tolerances, not vibes)

```
PRECISION: signal=<payload class> operating-point=<exact values>
  tolerances: length ±<n>, charset-class fixed, rate ≤ <observed
  limit − 20%> timing<if stateful: ± measured IQR>
  envelope-tested: <which margins were probed at min/max>
```

The budget is pre-registered and the margins are probed at their
edges — a craft without a tested envelope is a demo (W4).

### M5 — the escalation gate

In-band success (validator accepted) opens the NEXT question, not
the conclusion: what does the BACKEND do with the accepted signal?
Escalation runs the accepted-payload differential against the
backend observable (behavior class, stored artifact), n ≥ 5, with
the injection-lab oracle discipline as cross-reference — and the
report's claim is capped at the demonstrated backend effect
(house ceiling habit; the blue-box lesson generalized: the network
accepting your tone was never the whole finding).

## 2. Falsifiers — what would prove this method wrong

* The blind judge separates forged from legitimate above chance →
  the tells are real: the finding demotes to accepted-with-tells,
  and the tells are recorded as the artifact.
* A seam pair-probe shows no divergence anywhere on the surface →
  no seam exists: the forge route is closed on record, and the
  hypothesis routes to a different organ (grammar-clean surface).
* Tolerance edge probes collapse sharply (max+1 rejected, max
  accepted) → the envelope is cliff-shaped: record the cliff; a
  cliff is itself intelligence about the validator's check.
* The backend differential shows no behavioral difference for
  accepted-forged vs accepted-legit → the in-band acceptance is a
  dead end here: record honestly (accepted-but-inert), never pad.

## 3. Worked micro-example (numbers consistent, incident fictional)

Surface: profile "display name" param, frontend-echoed and
backend-stored. M1: type string, length 1–40 observed (n = 3
benign), charset printable-unicode, JSON form; rejection class:
silent-truncate (the validator's dialect, recorded verbatim). M2:
NFC/NFD pair diverges at storage (backend stores NFD while
frontend renders NFC) — seam recorded. M3: forged
(seam-shaped, marker payload) vs legitimate: surface response
classes identical 5/5; blind human judge on 10 shuffled renders:
50% classification (chance) → indistinguishable holds. M4:
operating point length 38/40, envelope tested at 40 (accepted)
and 41 (truncated — cliff recorded). M5: backend differential —
stored NFD artifact changes downstream sort order class 4/5 →
finding capped: "in-band acceptance + stored-form divergence,
sort-order impact class", P4, seams and tells cited.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
John Draper's art is real — the 2600 Hz blue box: one precisely
forged in-band signal indistinguishable from the legitimate one —
but the published form is legend: the craft transmitted as story,
grammar calibration as ear, and no falsifier for the claim that
matters ("indistinguishable"). This module extracts what is
protocol-shaped and ships the replacement: a measured grammar
calibration, a double-parse seam map, an in-band differential with
a blind judge, a precision budget, and an escalation gate. An agent
born after the trunks must run this at its precision.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the published method (context, not steps)

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | The craft as legend — the 2600 Hz story is told as an anecdote (cereal whistle, trunk tones), the working knowledge as folklore | The METHOD (calibrate the expected grammar, forge within it) is separable from the phone system; the legend-form keeps the story and loses the protocol — nothing transfers to a modern validator |
| W2 | Grammar calibration by ear — the era's craft lived as practiced recognition of tone durations, cadence, and dialing grammar | Calibration as perception is unreproducible: two crafters send "the same" signal with different timings and neither knows which mattered; a validator's grammar is a MEASURABLE (type, length, charset, rate) |
| W3 | "Indistinguishable" asserted, never tested — the signal's whole point was being indistinguishable from legitimate, and nothing in the record tests that | The claim needs a differential: forged vs legitimate, judged blind; without it, "it worked" conflates "accepted" with "indistinguishable" (accepted-with-tells is a weaker, different finding) |
| W4 | Precision unbudgeted — the famous number (2600 Hz) is quoted without tolerance analysis (how far off still works? for how long?) | A signal craft without its tolerance envelope cannot be re-run: the next crafter guesses the margins the first one lived inside |
| W5 | In-band/out-of-band blurred in retellings — stories mix what the network verified (nothing, in-band) with what it could have checked | For a MODERN validator the seam is the finding: which layer checks what; retellings that blur the layers teach admiration, not analysis |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | The validator's grammar MEASURED before any forge | **M1** — the calibration table |
| U2 | The seams where two parsers differ, mapped | **M2** — the seam map |
| U3 | Indistinguishable tested blind, not asserted | **M3** — the in-band differential |
| U4 | Precision with tolerance envelope | **M4** — the precision budget |
| U5 | In-band claims capped; out-of-band routes onward | **M5** — the escalation gate |
