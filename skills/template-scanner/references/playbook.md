# playbook.md — running template campaigns

Load when executing template-based detection work under this organ.

## 1. Author the template (or cite the existing one)

1. Class it: `vrt_classify(finding_class=…)` → the VRT dotted id for
   the `class` field.
2. Write the file per mindset.md §3 — matcher BEFORE any run, the
   `negative` leg included.
3. Register: EXPERIMENT record carrying the file's hash as its
   version. (A template that changes without a new hash is a
   different template.)

## 2. Run it (engine-side)

* HTTP-shaped: `http_probe` with the template's request; the matcher
   conditions go in the note (they were pre-registered).
* Sweep-shaped: `content_discover` over the surface set; the
  template's matcher defines what "deviation" means.
* The tool writes the records; the template is the declared intent —
  both are needed for a campaign fact.

## 3. Confirm hits (never skip)

A fired matcher is a candidate:

1. baseline leg (the protected case),
2. treatment leg (the matcher's target), n_runs ≥ 2,
3. control leg (the template's `negative` or a neighbor surface).

Then the candidate goes to module-smith's card. Templates find;
triads prove.

## 4. Compose campaigns

```
campaign: <name>
date: <ISO date>
surfaces: <surface set + dossier ids>
templates: [<id@version>, <id@version>, …]     # the WHOLE set
budget: <probe cap — scan-economist pricing>
```

* The campaign record (EXPERIMENT) cites all three: set, date,
  template list.
* Re-runs either cite the identical set (reproducibility check) or
  diff it loudly ("+tpl-002, -tpl-004, reason: …").
* Prevalence claims from campaign data carry the denominator
  (module-smith law 4).

## 5. Maintain the pack

* Every template accumulates: runs, hits, false-positives-on-controls
  (each with R-NNN).
* A template firing on its own negative leg is paused (matcher bug)
  until tightened — recorded as the tightening diff.
* Retired templates stay in the pack history with their retirement
  reason; packs grow by versioned diff only.

## 6. Share the artifact

The shareable unit is the template file — data, not code:

* it names its class (VRT id), its matcher, its negative leg, and its
  references;
* another operator with the same engine can replay it verbatim;
* that is the community-compounding property, kept intact.

## 7. Exit criteria

Campaign done when: every template in the set has run-or-parked
status with records, hits have triads or are parked leads, the
campaign record cites set+date+surfaces, and pack stats are updated.
Numbers at the exit gate: templates run, hits, confirmed, parked,
false-positive rate on controls, probes spent.
