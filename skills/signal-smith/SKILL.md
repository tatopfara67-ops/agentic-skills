---
name: signal-smith
version: 1.1.0
type: ai-skill
architecture: package
description: Legend-tier organ (Tier B — The Human & Signal Manipulators) built from the John Draper (Captain Crunch) lineage — input grammar and precision signal craft. Before any payload is sent, it calibrates the validator's expected grammar (type, length, charset, encoding, frequency/rate), maps every double-parse seam where frontend normalization and backend interpretation can diverge, then crafts ONE or TWO minimally-modified byte/encoding variations that the filter accepts while the deeper parser reads diffeSince v1.1.0 the organ carries the executable method layer (A16) — a mechanical critique of the Draper-era form's floors (the craft transmitted as legend with the method inseparable from dead trunks, grammar calibration by ear, indistinguishability asserted never tested, precision without a tolerance envelope, in-band and out-of-band blurred in retellings) shipped as protocol M1–M5: the measured calibration table with verbatim rejection classes, the double-parse seam map with pair-probes, the in-band differential with a blind judge, the precision budget with edge-tested margins, and the escalation gate to the backend observable. Use when a WAF or validator blocks honest payloads, when hunting encoding/canonicalization bypasses, when tuning request frequency to stay under rate filters, or when the operator asks for manual evasion with minimal requests ("bypass validasi", "WAF blocks my payload", "encoding trick", "byte-level manipulation", "satu variasi presisi", "avoid triggering the alarm").
category: security/legend-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: John Draper (Captain Crunch — the 1971-72 2600 Hz blue box: one precisely-forged in-band signal indistinguishable from a legitimate one)
  tier: B — The Human & Signal Manipulators
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; an in-scope target with a validation/WAF layer under study
---

# signal-smith v1.1.0 — One Precise Tone

## 0. What This Skill Is — and Is Not

* **Is**: the craft organ for INPUT ITSELF. It learns what the
  filter expects — the grammar (type, length, charset, encoding)
  and the frequency (rate) — then forges minimal variations that
  pass the validator while the deeper parser reads different bytes.
  Its product is the grammar map plus at most two precision
  variations per seam, handed to the payload organs
  (injection-lab, xss-playbook, ssrf-playbook, desync-hunter).
* **Is not**: a brute-force bypass dictionary. Volume is the
  anti-doctrine: the blue box worked because ONE precisely-forged
  2600 Hz tone was indistinguishable from the legitimate one —
  not because someone sprayed thousands of noisy tones at the
  network.

## 1. Inherited Contracts

Plugs into **Phase 2** (grammar hypotheses) and **Phase 3**
(variation experiments) of the mythos-bug-hunter spine, as a
supporting craft organ for the payload-carrying organs. Inherits
the experiment contract (§6 — validator verdict AND backend
behavior are separate observables, both recorded), R7 effort
budgets (the two-variation cap is the budget made explicit), and
the calibration discipline of content-discovery (control requests
before treatments). Craft layer: feedback-fuzzer governs any
search-shaped exploration; scan-economist prices the calibration
rounds.

## 2. The Lineage (attribution)

**John Draper** ("Captain Crunch") demonstrated in 1971–72, with a
toy whistle from a cereal box that happened to emit a 2600 Hz tone,
the founding lesson of signal manipulation: the phone network
carried its CONTROL SIGNALS IN-BAND — on the same channel as the
voice it carried — so a precisely forged control tone was
indistinguishable from a legitimate one. The system trusted its
signal grammar absolutely; the grammar was the vulnerability.
Distilled here as decision logic: learn the expected grammar
exactly, forge the minimal signal that the receiver cannot
distinguish, and never make noise while doing it. The historical
record is public (the phreaking era's documentation); the
operationalization against web validators is this organ's own
content. The verification record is `references/sources.md`.

## 3. Doctrine — How Draper-Thinking Runs

1. **The filter publishes its grammar on every rejection.** What is
   accepted, what is rejected, at which lengths, which characters,
   which encodings, which rate — each probe reply is grammar data,
   and the grammar map is the product.
2. **Every double-parse is a seam.** Wherever bytes are parsed twice
   (WAF normalize → backend interpret; URL-decode at edge →
   URL-decode at origin; charset A assumed → charset B applied),
   the two parsers CAN disagree — that disagreement is the target.
3. **Minimal edit distance.** The crafted variation changes the
   FEWEST bytes that still moves the two parsers apart; every
   extra changed byte is an uncontrolled variable and a louder
   signal.
4. **Frequency is part of the grammar.** The rate at which the
   system expects input is a filter dimension like any other;
   matching it is how the work stays invisible.
5. **Two variations per seam, then park.** If two precision
   variations do not split the parsers, the seam goes to the
   backlog — volume is not the next move, honesty about the seam
   is.

## 3.5 The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published signal-craft form where it was mechanically weak —
the 2600 Hz story kept while the protocol (calibrate the grammar, forge
within it) was lost, calibration living as practiced perception, "it
worked" conflating accepted with indistinguishable, the famous number
quoted without tolerances, retellings blurring which layer checks what —
and ships the executable replacement: **M1** the calibration table
(type/length/charset/encoding/rate measured from ≥ 3 benign observations;
rejection classes recorded VERBATIM), **M2** the seam map (NFC/NFD,
encoding, duplicate-parameter, length-boundary pair-probes; each seam a
CONTROL the forge cites), **M3** the in-band differential (legitimate vs
forged, n ≥ 5 interleaved, blind judge; identical classes ≥ 4/5 =
indistinguishable; accepted-with-tells is its own finding class), **M4**
the precision budget (operating point + tolerances, margins probed at
edges; cliffs recorded as intelligence), **M5** the escalation gate
(in-band acceptance opens the backend differential, never the conclusion).

## 4. Procedure — Numbered Actions

1. Calibration round (CONTROL records): a small fixed input ladder
   — length edges (0, 1, max-1, max, max+1), charset edges
   (letters, digits, symbols, unicode, control bytes), encoding
   edges (raw, %-encoded, double-%-encoded, unicode escapes),
   content-type edges (json/form/text, charset parameters). The
   ladder template is `references/encoding-grammar.md`.
2. Record the verdict pairs: validator verdict (accept/reject/
   sanitize/latency) AND backend behavior class (response class +
   body hash) — separate observables, separate records.
3. Map the seams: wherever the same logical input produces
   different backend behavior classes under different encodings,
   a double-parse seam exists. Each seam becomes a pre-registered
   hypothesis.
4. Craft ONE minimal variation for the strongest seam: the smallest
   byte edit that the validator accepts but the backend reads
   differently. Case flip, single %-encode, one homoglyph, one
   null byte, one terminator, one charset parameter — the catalog
   with selection rules is `references/encoding-grammar.md`.
5. Send it: one `http_probe`, exact bytes recorded as artifact;
   validator verdict and backend differential recorded as the
   EXPERIMENT. Rate discipline: calibration and variation requests
   ride the frequency the system expects (its own rate floor
   observed in step 1).
6. If the seam splits: hand the variation grammar to the payload
   organ (injection-lab/xss/ssrf/desync) — the SPLIT is this
   organ's finding; what rides through it is the payload organ's
   differential work.
7. At most TWO variations per seam per session (hard cap); park
   untested variations in the ledger with resume notes.
8. Exit gate: grammar-map edges probed (by dimension), seams
   mapped, variations sent (≤ 2 per seam), splits confirmed with
   differential records, alarm status stated (no WAF alerts — or
   the alerts that did fire, reported as facts).

## 5. Hard Rules (mechanically enforced)

1. **Volume cap: two variations per seam.** A third requires a new
   hypothesis class and a ledgered reason; sprays are forbidden.
2. **Calibration is CONTROL-tagged.** The input ladder never
   carries payloads — it measures, it does not attack.
3. **WAF alerts are engagement facts.** An alarm that fires is
   reported to the operator (when, which probe); the response is
   NEVER more volume or faster requests (refusal-is-final).
4. **A split is not a finding's impact.** This organ CONFIRMs the
   parser split; the vulnerability class and its impact belong to
   the payload organ's differential triad.
5. **Exact bytes in artifacts.** Every variation ships its literal
   bytes; "an encoded version of the payload" without bytes is
   not a record.

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Calibration ladder + variations | `http_probe` (exact bytes, artifacts) |
| Grammar + seam records | `ledger_append` (CONTROL/EXPERIMENT) |
| Payload work once a seam splits | injection-lab / xss-playbook / ssrf-playbook / desync-hunter |
| Header-level grammar for protocol seams | desync-hunter organ (its asymmetry-catalog module) |
| Search-shaped exploration governance | feedback-fuzzer organ |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Building the input ladder / choosing the minimal variation | `references/encoding-grammar.md` |
| Verifying the Draper lineage and sources | `references/sources.md` |
| Grading the published form, calibrating grammar, testing indistinguishability blind | `references/method-upgrade.md` |
