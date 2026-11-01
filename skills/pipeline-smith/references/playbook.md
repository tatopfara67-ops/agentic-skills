# playbook.md — running a composable recon pipeline

Load when executing recon under this organ.

## 1. Declare the pipeline (before the first stage)

Write the stage list with the stage contract (mindset.md §3). A
minimal recon pipeline:

```
1 source      question: what names exist?        (passive)
2 dedupe      question: which names are unique?  (no probes)
3 liveness    question: which names answer?      (1 probe each)
4 surface     question: which paths exist?       (calibrated sweep)
5 outlier     question: what deviates from siblings? (uniform diff)
6 select      question: what leaves for hypotheses? (pattern packs)
```

## 2. Stage 1 — source (passive, zero target packets)

* `ct_subdomains(domain)` — CT logs are the free tier.
* `dns_resolve` per name — resolution is not probing.
* Record every stage's output with counts. No stage without a count.

## 3. Stage 2 — dedupe (recorded)

Normalize: lowercase, strip scheme and :port, collapse wildcard-ish
variants. Record `names_before`, `names_after`. If the dedupe ratio
ever looks absurd (>50% dropped), the source stage has a duplicate
bug — fix the source, not the symptom.

## 4. Stage 3 — liveness

One `http_probe` per name. Park the dead with the reason (NXDOMAIN /
timeout / refused). The live list is the only thing that ever
proceeds.

## 5. Stage 4 — surface sweep

`content_discover(base_url, wordlist=…)`: the wordlist is this
pipeline's pattern pack — cite which and why. Rate from observed
latency (scan-economist's law 5, same engine).

## 6. Stage 5 — outlier hunting (meg discipline)

* Pick the uniform path (e.g. `/.env`, `/api/v1/users`, or the
  surface class's signature path).
* Fetch it across EVERY live host with identical effort.
* Classify responses coarsely (status class, size bucket) — the
  pipeline-fuzzer's bucketing law applies here too.
* The deviation from the pack is the candidate; the pack's mode is
  the control. Both get records.

## 7. Stage 6 — selection (gf discipline)

Filter fetched artifacts with per-class pattern packs:

* packs live as versioned data files keyed by VRT class
  (vrt_classify's finding classes);
* a hit leaves the pipeline as a pre-registered hypothesis
  (module-smith's card), never as a "finding".

## 8. Pipeline hygiene

* One probe type per stage; a stage that mixes request shapes is two
  stages.
* Every stage's output artifact is the next stage's declared input —
  if a stage reads something not declared, the pipeline is lying.
* Sampling under budget pressure: state the sample rate, record it,
  and let the report carry the denominator (module-smith law 4).

## 9. Exit criteria

Pipeline done when: all stages have counts, the live set is fully
swept-or-parked, outliers have triads or are parked leads, and the
selection stage emitted its hypothesis cards. Numbers at the exit
gate: names found, deduped, live, swept, outliers, candidates,
probes spent.
