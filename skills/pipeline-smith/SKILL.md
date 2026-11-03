---
name: pipeline-smith
version: 1.1.0
type: ai-skill
architecture: package
description: >-
  Craft-lineage organ distilled from Tom Hudson (Tomnomnom) — the
  Unix-pipeline school of bug bounty recon. Every stage is a small tool that
  does one thing well and speaks stdout; passive sources feed the pipeline
  before the target is ever touched; names are deduplicated before probing;
  liveness is proved with minimal requests (httprobe discipline); curated
  pattern packs (gf) encode expert pattern knowledge as data rather than
  bespoke scripts; the same path is fetched across many hoSince v1.1.0 the
  organ carries the executable method layer (A16) — a mechanical critique of
  the pipeline school's floors (pipelines as unversioned shell history, dedupe
  asserted but never measured, tool stdout as an unwritten contract,
  passive-source freshness unrecorded, results narrated without replayable
  provenance) shipped as protocol M1–M5: the versioned pipeline record, the
  collapse ledger with a cross-source gate, the stage contract with hard-fail
  semantics, the as-of stamp that prices liveness budget, and the five-field
  replay citation the report gate enforces. Use when chaining recon stages,
  when deciding what composes with what, when building or trimming a
  wordlist/pattern pack, or when a recon step must stay cheap and composable
  ("pipeline this", "dedupe first", "passive sources before probes", "pattern
  pack", "fetch the same path everywhere").
category: security/craft-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: Tom Hudson (Tomnomnom) — assetfinder, httprobe, gf, meg, gron, waybackurls; the Unix-philosophy recon pipeline
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# pipeline-smith v1.1.0 — The Tomnomnom Lineage

## 0. What This Skill Is — and Is Not

* **Is**: the organ for *composability* — how recon stages chain, what
  each stage is allowed to know, and where the cheap half-lives of a
  pipeline live. Its doctrine: one tool, one job, stdout as the
  contract; the pipeline is the product, no stage is precious.
* **Is not**: a set of Go tools. The arsenal is Python and speaks
  records, not pipes — this organ governs the *shape* of stages and
  their composition, translated into ledger discipline.

## 1. The Lineage (attribution)

Tom Hudson ("Tomnomnom") — Yorkshire, UK; "open-source tool maker,
trainer, talker" — built the recon toolchain a generation of bug
bounty hunters runs on (assetfinder, httprobe, gf, meg, gron,
waybackurls, qsreplace) and teaches the toolmaking craft (Ekoparty
2024, "Confessions of a Toolmaker"). Sources:
references/sources.md — the verification record

## 2. The Six Laws of the Pipeline

1. **One tool, one job, stdout.** Each stage answers exactly one
   question and hands on lines. In arsenal terms: one tool call = one
   question = its own records. A stage that answers two questions is
   two stages wearing a trench coat.
2. **Passive before active.** assetfinder's model: names from
   certificate transparency and other public sources *before* the
   target is touched. Modern form: `ct_subdomains`,
   `dns_resolve`, wayback-style history → only then liveness probes.
3. **Dedupe before you pay.** Names are deduplicated and normalized
   BEFORE the probing stage — you never pay probe prices for the same
   asset twice.
4. **Liveness is the cheapest question.** httprobe converts names to
   live URLs with minimal requests and no ceremony; depth is a later,
   pricier stage. Probe with defaults; escalate deliberately.
5. **Pattern knowledge is data.** gf's insight: vulnerability-class
   patterns live in curated pattern files (`gf xss`, `gf redirect`),
   not in bespoke scripts — experts encode, pipelines consume. Modern
   form: per-class pattern packs (wordlists, regex sets) versioned as
   data, aligned with the VRT classes of `vrt_classify`.
6. **Diff to decide.** meg's model: fetch the SAME path across MANY
   hosts, then compare — the outlier is the signal. Modern form:
   uniform-path probes across a surface set; the deviation from the
   pack, not any absolute response, is the finding candidate.

## 2.5 The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published pipeline art where it was mechanically weak — the
one-liner as the artifact (nothing versioned, nothing replayable),
`sort -u` asserted without a collapse ratio, stdout formats drifting
between tool versions with no schema check, archives read as if current,
"found via waybackurls + gf" as the whole provenance chain — and ships the
executable replacement: **M1** the pipeline record (versioned, hashed,
cited by findings), **M2** the collapse ledger (in/out/ratio per stage;
cross-source ratio < 0.2 fires the source-staleness gate), **M3** the stage
contract (input schema validated before spend; mismatch = hard version
bump, never a mid-run patch), **M4** the as-of stamp (memory-class
candidates priced last), **M5** the replay proof (pipeline v + run id +
stage + source + as-of — five fields, no exceptions).

## 3. Procedure — Numbered Actions

1. List the pipeline as stages, each with: input artifact, the ONE
   question, output artifact (records + park note). No stage without
   a single question.
2. Feed it passive first: `ct_subdomains`, `dns_resolve`; historical
   artifacts (wayback-class) where available.
3. Normalize + dedupe (the pipeline's own stage): lowercase hosts,
   strip ports/schemes consistently; record the count before/after —
   the dedupe ratio is a pipeline health metric.
4. Liveness probe the survivors (`http_probe`, one per host); dead
   names park, live names pass.
5. Uniform-path probing (meg discipline): the same path set across
   every live host; record response classes; candidates = deviations.
6. Pattern-pack filtering on text artifacts (gf discipline): per-class
   packs select what leaves the pipeline for hypothesis work.
7. Every stage's output cites its input records — the pipeline is a
   chain of custody, not a chain of hopes.

## 4. Tool Routing

| When | Tool |
| --- | --- |
| Passive names | `ct_subdomains` |
| Normalize/resolve | `dns_resolve` |
| Liveness | `http_probe` (one per host) |
| Uniform-path sweeps | `content_discover` (calibrated) / `http_probe` loop |
| Pattern packs | wordlists + per-class regex sets (data, versioned) |
| Reshaping artifacts for the next stage | local transforms (gron's lesson: make data greppable, don't write a bespoke parser) |
| Chain-of-custody records | `ledger_append` per stage |

## 5. Hard Rules

1. A stage answers ONE question — split stages that don't.
2. Active probing never precedes the passive stage's exhaustion
   (within budget).
3. Dedupe is a recorded stage, not an implicit courtesy.
4. Pattern packs are data files, versioned and cited — never inline
   regex folklore in a probe call.
5. Depth follows liveness, never the reverse.

## 6. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Designing or arguing a pipeline's stages | references/mindset.md |
| Running the recon pipeline end to end | references/playbook.md |
| Checking lineage claims and reading list | references/sources.md |
| Grading the published method, measuring collapse ratios, stamping freshness | references/method-upgrade.md |
