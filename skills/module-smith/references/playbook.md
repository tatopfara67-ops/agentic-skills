# playbook.md — composing module proofs

Load when running module-shaped verification work under this organ.

## 1. Write the card first

For each hypothesis (spine Phase 2 output), fill the module card
(mindset.md §3) BEFORE the first probe. Pre-registration is the
framework's metadata discipline applied to thinking:

```
ledger_append(tag=EXPERIMENT, note="module card: inputs/observable/
falsifier/rank/refs — partitions frozen before outcomes")
```

## 2. Prove access (the triad)

1. **Baseline** — the protected case: the request as an unauthorized
   party against the gated surface. Expected: the gate's response
   (401/redirect). Record.
2. **Treatment** — the same effort against the claimed weakness
   (ungated route / wrong-knob parameter). Expected: the delta the
   card declared. Record, n_runs ≥ 2.
3. **Control** — the same effort against a neighboring surface that
   should NOT respond. Expected: baseline-class response (404). Record.

No triad, no door. A partial triad parks the hypothesis as a lead
with a resume note.

## 3. Prove impact (the payload)

Separate records, separate discipline — the spine's canary ladder:

* ONE canary (one page read, one callback, one transaction), chosen
  to prove the maximum the card claims and nothing more.
* The canary is cited in the finding block (auditor gate 5) —
  "canary attestation".
* Impact beyond the canary is impact you did NOT prove; the report
  says so in those words.

## 4. Rank from runs

After the triad: update the card's rank with the observed stability
(3/3 stable = promote; 1/3 = lead). The card's `runs` field is the
auditor's `n_runs:` line — they must agree, because they are the
same number.

## 5. Index for reuse

* Key modules by surface class (the 21-class taxonomy) + VRT class
  (from `vrt_classify`).
* New surface, known class → re-run the card: same inputs template,
  same observable, same falsifier shape. The dossier note says
  "module <name> re-run" with the new R-NNNs.
* A module that fails on a new surface does not die — it records the
  boundary of its class ("holds for v1 mounts, not v2") and gets a
  narrowed card.

## 6. Measure exposure (the Sonar move)

When the claim is systemic ("this misconfiguration is common in this
program"):

1. Define the probe set: which surfaces, same effort each (the
   denominator).
2. Run the module card once per surface — identical inputs.
3. Count hits; record CONTROL records for non-hits (they are the
   denominator's proof).
4. Report `hits / attempted` with both numbers; never "many" or
   "most".
5. Cadence claims ("still present a week later") need two dated
   probe sets — a re-run, not a memory.

## 7. Exit criteria

The organ hands to the report phase when every hypothesis is either a
closed module (CONFIRMED with card + triad + canary + rank), a
falsified module (with the elimination record), or a parked lead
(with resume note). Numbers at the exit gate: modules run, confirmed,
falsified, parked, reuse hits, exposure counts (hit/attempted).
