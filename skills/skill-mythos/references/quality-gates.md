# quality-gates.md — the triage-grade standard

Load when writing a finding block, assembling a report, or hardening a
submission. This is the standard the auditor enforces mechanically;
know it before you write, not after you fail.

## 1. The reader is a triage analyst

Every gate below exists because a triage desk needs it:

* they will NOT re-derive your claim — they check whether the evidence
  you cite supports it;
* they will re-run your reproduction steps, once, unattended;
* they will compare your severity against the program's taxonomy, not
  your enthusiasm;
* they see hundreds of reports — anything hedged, uncited, or
  un-reproducible goes to the reject pile without appeal.

## 2. Gate 1 — zero false positives (the differential triad)

A finding is CONFIRMED only when three record classes agree:

| Leg | What it is | What it kills |
| --- | --- | --- |
| baseline | the normal response for the protected case (e.g. 401) | "everything returns 200" |
| treatment | the same effort aimed at the claimed weakness (200 + payload effect) | "the route is dead" |
| control | the same effort aimed at a NEIGHBORING route (404) | "any request returns data" |

n_runs ≥ 2 with stable deltas across runs, or attempts + success_rate
for probabilistic paths. One leg missing = the finding stays a lead,
files under INCONCLUSIVE, lands in the leads appendix.

## 3. Gate 2 — full reproducibility

Write reproduction steps a third party can replay verbatim: exact
request(s), order, and the observable to watch. The E-NNN experiment
card (or an explicit `reproduction:` line) is mandatory in the finding
block. If a step requires privileged setup, say exactly which —
"requires an account with role X" is reproducible; "requires access"
is not.

## 4. Gate 3 — the classification set (mandatory in every CONFIRMED
finding block that declares a severity)

```
### H-NNN — <title> (facts R-NNN, R-NNN)

- claim: …
- facts: R-NNN
- prior: NN% — …
- falsifier: …
- Closure: CONFIRMED (E-NNN: R-NNN; closure R-NNN)
- severity: <program-context call> (records R-NNN)
- impact-chain: <attack path, bounded, with records>
- canary attestation: <what proves you touched nothing you shouldn't>
- cvss: CVSS:3.1/<metrics> = <score> (band: <band>; <why the impact
  metrics are what they are>; records R-NNN)
- vrt: <dotted.category.id> [P<N>] — <why this node and not its
  siblings; the program-context argument; records R-NNN>
- reproduction: E-NNN — <one-line replay summary> (n_runs N; baseline
  R-NNN, treatment R-NNN, control R-NNN)
```

The auditor enforces this set mechanically: the CVSS score is
RECOMPUTED from your vector (`arsenal/cvss.py`, FIRST spec — a
mismatch fails the report), the VRT id is looked up in the shipped
official taxonomy, and the reproduction reference must exist in the
block. Incident handoffs (adversary hunts) rate `Risk:` instead of
`severity:` and are exempt — IR handoffs are not vulnerability
reports.

## 5. The three-layer severity discipline

Never merge these three into one number:

| Layer | Instrument | Answers |
| --- | --- | --- |
| Technical | CVSS 3.1 base vector + score | how bad is this weakness in the abstract, on the observed path |
| Taxonomy | Bugcrowd VRT P1–P5 (+ HackerOne crosswalk) | how does this class rate on this platform's baseline |
| Program context | your argued call | what THIS program pays for, given its scope and exclusions |

State all three. Divergences are expected and honest: a self-owned
lab banner exposure can be CVSS 5.3 (Medium) technically, VRT P3 as
the taxonomy baseline, and a low/P4 submission call after the program
context (non-sensitive content, self-owned surface). What is NEVER
honest is a single flattering number with the other two silent.

## 6. Language gates

* Every line carrying a severity or vulnerability-class word cites an
  R-NNN record on the same line.
* No hedging ("appears to", "potentially") — hedge words mean the
  differential triad has not run; run it or park the lead.
* No ungated victory language. The closure line is the victory.
* No placeholders, no unfilled fields, no "see above" where a record
  id belongs.

## 7. Pre-submission checklist

1. `ledger_merge(program)` — fold the append log.
2. Report written ONLY from `ledger_read` outputs.
3. `cvss3_score` on every vector you wrote — write what it returns.
4. `vrt_classify` on every class you claim — copy the exact dotted id.
5. `python3 auditor/audit_report.py <report.md>` — exit 0 or fix the
   WORK behind the report, never the auditor.
