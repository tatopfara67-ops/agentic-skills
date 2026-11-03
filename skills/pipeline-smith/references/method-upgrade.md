# The executable method — M1–M5 for pipeline-smith

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The lineage critique that
justifies each step (why these phases exist, what was weak in
Tomnomnom's toolmaking corpus) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M5

Quickstart — the spine as commands (passive sources first, dedupe
measured, freshness stamped; the record formats below are what these
runs produce):

```bash
# M1 passive collect — zero target-side packets
subfinder -d example.com -silent | tee s1-domains.txt
cat s1-domains.txt | httprobe -c 50 | tee s2-live.txt
cat s2-live.txt | waybackurls | tee s3-urls.txt
# M2 collapse ledger — dedupe MEASURED, not asserted
cat s3-urls.txt | sort -u | tee s4-dedupe.txt
wc -l < s3-urls.txt; wc -l < s4-dedupe.txt    # ratio -> COLLAPSE
# M3 stage contract — one thing well, speaks stdout, version pinned
cat s4-dedupe.txt | unfurl -u paths | sort -u | tee s5-paths.txt
# M4 as-of stamp — source freshness recorded with the run
date -u +%FT%TZ | tee s6-asof.txt
# M5 replay proof — rerun the chain; the diff must be empty
./run-pipeline.sh > r1.txt && ./run-pipeline.sh > r2.txt
diff r1.txt r2.txt || echo "REPLAY GATE FAILED"
```

### M1 — the pipeline record

```
PIPELINE v3: stages=[S1 passive-collect (sources A,B,C)
  S2 normalize-lowercase (contract: hostname-charset)
  S3 dedupe (M2) S4 liveness-probe (bounded: top-N by priority)
  S5 pattern-tag (gf-equivalent packs, versioned)]
  hash=<sha256 of stage specs> created=<date> runs=<count>
```

Rules: a stage spec change = a new version; findings cite the
pipeline version + run id that produced them (W1, W5). The record
lives in the dossier, not in shell history.

### M2 — the collapse ledger (dedupe as measurement)

Every dedupe-adjacent stage reports its numbers:

```
S3 COLLAPSE: in=<count> out=<count> ratio=<x.xx>
  duplicate-classes: same-source-repeat=<a> cross-source=<b>
```

*Decision gate*: cross-source duplicate ratio < 0.2 means the
sources barely agree — either a source is stale (M4 check) or
normalization is too weak (contract audit); the gate fires and the
cause is recorded before further spend (W2).

### M3 — the stage contract

Each stage declares its OUTPUT schema and validates its INPUT
against the upstream's declaration before running:

1. Schema fields for hostname-class stages: charset class, case
   state, trailing-dot state, port-suffix allowed.
2. A mismatch (upstream emits `Example.com.` while downstream
   contract is lowercase-no-dot) is a HARD failure of the pipeline
   version — fix at the stage spec, never patch mid-run (W3).
3. Contracts are part of the pipeline hash: same stages + changed
   contract = new version.

### M4 — the as-of stamp (source freshness as FACT)

Per passive source, per run:

```
SOURCE: name=<wayback-class> as-of=<retrieval date> span=<archive
  coverage claim, source-cited> trust=<memory|present> rule:
  candidates older than <window> are tagged STALE and priced last
```

Rule: STALE-tagged candidates never consume liveness budget ahead
of fresh ones; the liveness stage's queue order is
fresh-first-then-stale, on record (W4).

### M5 — the replay proof

1. Every candidate finding cites: `pipeline v, run id, stage, source,
   as-of` — five fields, no exceptions at the report gate.
2. Replay discipline: a second analyst (or the same agent, next
   session) re-runs the pipeline version from the recorded sources
   and must reproduce the candidate within the recorded collapse
   ratios; a miss is a pipeline defect, filed as a CONTROL
   correction.
3. The pipeline's yield is reported per stage — spend and selectivity
   are visible (the scan-economist footprint habit, applied to
   recon).

## 2. Falsifiers — what would prove this method wrong

* Replay misses a recorded candidate → the pipeline was
  non-deterministic (source drift, unrecorded flag): the version is
  broken; findings from it are re-verified before they ride any
  report.
* Collapse ratio spikes without a source change → normalization
  contract too weak (mixed case surviving): contract audit, new
  version.
* A stage consumes its full budget on STALE candidates → the M4
  queue order was violated (bug or drift): the run is void for
  those candidates, re-queued fresh-first.
* Two pipeline versions disagree on the same source data → diff the
  stage specs (the hash makes this mechanical); the disagreement is
  resolved by re-running the older version ONCE with its own
  contracts, never by eyeball.

## 3. Worked micro-example (numbers consistent, incident fictional)

Pipeline v3, run 12: S1 collects 3,142 raw names (sources: CT-log
as-of today, wayback-class as-of 8 months back). S2 normalizes
(contract: lowercase, no trailing dot) — 12 hard-failures logged
(port-suffix emitters), fixed at spec, v3.1. S3 collapse: in 3,130,
out 1,871, ratio 0.40 (cross-source 0.31 → gate fires: wayback
staleness confirmed by M4). S4 liveness priced on the fresh 1,204
first; STALE 667 queued behind. S5 pattern-tags 34 candidates.
Finding cites: `pipeline v3.1, run 12, S5, CT-log source, as-of
<date>` — replayable, five fields present.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
Tomnomnom's art is real — the small-tool Unix school (assetfinder,
httprobe, gf, meg, waybackurls) reshaped bug bounty recon — but the
published form has floors: pipelines built per-operator as shell
history, dedupe asserted but never measured, tool stdout formats
drifting silently, and passive-source freshness never recorded. This
module extracts what is protocol-shaped and ships the replacement:
the pipeline as a versioned record, dedup as measured stages, source
freshness as FACTs, stage contracts pinned, and a replay proof. An
agent that cannot install a single tool must run this at its
discipline.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the published method (context, not steps)

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | Pipelines as shell history — the canonical usage is a talk slide with a one-liner; every operator rebuilds their own, slightly wrong | Nothing is versioned: a finding traced to "my pipeline" cannot be replayed by a second analyst; stages mutate (flag renames, output changes) with no record |
| W2 | Dedupe asserted, not measured — "sort -u" appears in every one-liner, and the school preaches dedupe-before-paying, but no stage ever reports its collapse ratio | Silent over-count: the same subdomain from 5 sources reads as 5 candidates until a human notices; the pipeline's actual selectivity is unknown to its own operator |
| W3 | Tool stdout as an unwritten contract — each tool's output format is stable until it isn't; pipelines break mid-campaign on version bumps | No stage validates its input schema before paying for the next stage's cost; a format change upstream poisons everything downstream, quietly |
| W4 | Passive-source freshness unrecorded — waybackurls/certificate data are read as if current, with no per-source as-of date | Stale-archive artifacts (an endpoint dead for a year) consume liveness budget by the thousands; the pipeline cannot tell memory from present |
| W5 | Results narrated, not replayed — the writeup says "found via waybackurls + gf", which is a recipe anecdote, not a run record | The finding's provenance chain (which source, which pattern, which stage) is unverifiable — exactly what a report gate should refuse |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Pipelines versioned, hashable, replayable | **M1** — the pipeline record |
| U2 | Dedupe measured per stage | **M2** — the collapse ledger |
| U3 | Stage input contracts pinned and checked | **M3** — the stage contract |
| U4 | Source freshness as a FACT per run | **M4** — the as-of stamp |
| U5 | Findings cite replayable runs | **M5** — the replay proof |
