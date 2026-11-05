---
name: harness-smith
version: 1.1.0
type: ai-skill
architecture: package
description: >-
  Craft-lineage organ forged from Tavis Ormandy (Google Project Zero /
  Information Security Engineering; the 2011 corpus-distillation
  tradition, the Symantec enterprise-endpoint disclosures 2016, the
  Windows Defender engine bugs 2017, the MSCTF rabbit-hole 2019, the
  NSS "BigSig" postmortem 2021, the Zenbleed CPU research 2023) —
  fuzz-first attack-surface triage and oracle engineering. The
  doctrine: the juiciest target class is software that parses the
  LEAST trusted input at the HIGHEST privilege — antivirus unpackers
  loaded into the kernel, signature engines on every endpoint, crypto
  parsers in every browser, undocumented IPC protocols in legacy OS
  code. The organ ships with its method layer born in (A16): a
  mechanical critique of the published Ormandy art — the
  target-selection instinct never stated as a census rule, the
  instruments announced but shipped late, the method scattered across
  postmortems rather than one protocol, the disclosure cadence never
  written as a decision table, the missed-why postmortem exceptional
  rather than routine — and the replacement protocol M1–M6: the
  privileged-parser census with its boundary against feedback-fuzzer
  and scan-economist, harness engineering with corpus distillation and
  the missing-tool decision, oracle design with the classification
  table (crash / state-diff / serialized), minimization to the
  simplest repro, the public reproducible report with the no-terms
  vendor protocol, and the missed-why postmortem with its residual
  register. Born under charter v1.13+, it also ships its operator
  runtime (A17): the thinking rules, situation-to-action behavior,
  scripting arsenal, and rigid run-order characteristic of the
  lineage. Use when choosing where to point fuzzing effort by attack
  surface rather than habit; when a harness or oracle must be
  engineered for a parser target; when a finding must be minimized to
  its simplest reproducible form; or when a report must ship publicly
  without agreeing to vendor terms ("privileged parser", "attack
  surface triage", "fuzz-first", "oracle design", "harness
  engineering", "corpus distillation", "serialized oracle", "bug
  postmortem", "seleksi target fuzzing", "parser berprivilege",
  "rekayasa oracle").
category: security/craft-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: Tavis Ormandy (Google Project Zero / Information Security Engineering) — the 2009 model-inference fuzzing talk line, the 2011 "Fuzzing at scale" corpus-distillation tradition with Chris Evans and Matt Moore, the 2016 Symantec enterprise-endpoint disclosures ("as bad as it gets"), the 2017 Windows Defender engine bugs, the 2019 "Down the Rabbit-Hole" MSCTF research with ctftool, the 2021 NSS "BigSig" vulnerability postmortem with call-stack-monitoring fuzzing, the 2023 Zenbleed research (CVE-2023-20593) with the serialized-oracle technique; third candidate-queue execution of the lineage-smith forge
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+; skill-mythos charter v1.13+
---

# harness-smith v1.1.0 — The Ormandy Lineage

## 0. What This Skill Is — and Is Not

* **Is**: the organ that decides WHERE fuzzing strikes and engineers
  the instrument that makes the bug findable. Its unit of work is the
  privileged parser — software that consumes untrusted bytes while
  running at kernel/SYSTEM/every-endpoint privilege (the AV unpacker
  in the kernel, the signature engine parsing every downloaded file,
  the crypto library parsing every certificate, the undocumented IPC
  protocol with no access control) — and its craft is fourfold: the
  census that ranks such surfaces, the harness that feeds them, the
  oracle that decides what counts as signal, and the minimized
  reproducible report with its missed-why postmortem. In the
  lineage's own documented arc: corpus distillation over 20 TB of SWF
  (2011), the ctftool protocol client built over weeks (2019), the
  call-stack-monitoring fuzzer that found BigSig (2021), and the
  serialized-oracle fuzzer that found Zenbleed (2023).
* **Is not**: the fuzzing campaign runner — once the target is
  censused, the harness built, and the oracle declared, RUNNING the
  search loop (novelty buckets, saturation stop rules) is
  feedback-fuzzer's ground (the lcamtuf lineage). Nor is it a network
  sweep budgeter (scan-economist, the Fyodor lineage) or a static
  teardown organ (deep-teardown, the Hotz lineage). This organ
  selects the target and engineers the instrument; those organs
  execute other phases of the hunt.

## 1. The Lineage (attribution)

Tavis Ormandy, security researcher — Google Security Team, then
Project Zero / Google Information Security Engineering; earlier
UNIX security research documented on his personal site
(taviso.decsystem.org, superseded by cmpxchg8b.com). The documented
corpus: the model-inference-assisted fuzzing line (HITB 2009 speaker
record — set-cover corpus selection, years before it was mainstream);
"Fuzzing at scale" (Google Security Blog, 2011, with Chris Evans and
Matt Moore — 20 TB of SWF distilled to ~20,000 files on 2,000 cores,
~400 crash signatures, ~106 bugs); the antivirus-engine arc
(Kaspersky emergency patch 2015; "How to Compromise the Enterprise
Endpoint" — the Symantec disclosures, Project Zero blog, June 2016;
the Windows Defender / MsMpEng engine bugs of 2017, including the
wormable "billion PCs" bug announced the night it was found);
"Down the Rabbit-Hole" (Project Zero blog, 2019 — the MSCTF
rabbit-hole that began with one unexplained test-case discrepancy and
ended with ctftool and Winlogon compromise); the NSS "BigSig"
postmortem (Project Zero blog, 2021 — a bounds bug found by
call-stack-monitoring fuzzing, reproduced in three commands, and
postmortemed publicly); the LastPass extension bugs (2016, 2019); and
Zenbleed (cmpxchg8b.com, 2023 — CVE-2023-20593, the AMD Zen 2
speculative-execution leak found with a serialized-oracle fuzzer,
reported May 15, 2023, coordinated with AMD, with the chicken-bit
workaround published for free). Nothing here is his code; this is his
decision logic, re-expressed as engagement rules. Sources and the
read ledger: references/sources.md — the verification record.

## 2. The Five Laws of Harness-Smithing

1. **The privileged parser is the target.** Where the least trusted
   input meets the highest privilege, a trivial bug is a critical
   bug: no user interaction, default configuration, kernel or SYSTEM
   context, every-endpoint deployment. The 2016 record's own words:
   "These vulnerabilities are as bad as it gets." The census ranks
   surfaces by privilege × deployment × input hostility BEFORE any
   harness exists.
2. **Fuzz-first — but the oracle is the design problem.** Coverage
   feedback finds the paths; the oracle decides what counts as a
   finding. Crash oracles miss logic bugs; state-comparison oracles
   catch them; serialized oracles catch micro-architectural ones
   (Zenbleed's final states didn't match — "that could indicate a
   bug"). Declaring the oracle class is a mandatory step, not an
   implementation detail.
3. **Write the simple test case; chase the discrepancy.** In the
   lineage's own words: "I often find it valuable to write simple
   test cases confirming things work the way I think they do.
   Sometimes I can't explain the results, and getting to the bottom
   of those discrepancies can reveal new research opportunities"
   (2019). An unexplained result is not noise — it is the entrance.
4. **When the instrument does not exist, build it.** ctftool took
   weeks and grew its own scripting language; the call-stack monitor
   needed "a lot of optimization" before it was fast enough; the
   serialized-oracle transformer was written for the silicon target.
   The instrument is part of the finding — and the harness decision
   (adapt, wrap, or build) is a recorded gate, never an accident.
5. **The simplest repro and the missed-why are the report.** A
   finding ships as commands a third party can run (BigSig: three
   openssl/vfychain commands) and as the question the ecosystem owes
   an answer: "This should have been caught earlier, and I want to
   explore why that didn't happen" (2021). A bug without its
   missed-why is half a finding.

## 3. The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published Ormandy art where it was mechanically weak — the
target-selection instinct never stated as a census rule ("hidden
attack surface" named, never enumerated), the instruments announced
but not shipped with their findings, a method scattered across
postmortem narratives instead of one protocol, a disclosure cadence
lived (Friday-night announcements, 90-day deadlines, no-terms email
reports) but never written as a decision table, and the missed-why
postmortem run once instead of on every finding — and ships the
executable replacement: **M1** the privileged-parser census (with the
feedback-fuzzer and scan-economist boundary rows argued on record),
**M2** harness engineering with corpus distillation and the
missing-tool gate, **M3** oracle design with the classification
table, **M4** minimization to the simplest repro, **M5** the public
reproducible report with the no-terms vendor protocol, and **M6** the
missed-why postmortem with its residual register.

## 4. The Operator Layer (A17) — the Ormandy runtime

`references/operator-os.md` ships the figure's documented psychology
as the agent's RUNTIME: the thinking framework (numbered if-then
rules — fuzz-first but oracle-designed, chase the discrepancy, build
the missing instrument), the behavioral protocol (situation → move →
agent action → refusal, with pacing and failure-reaction rules), the
scripting arsenal (the census worksheet, the coverage harness
skeleton, the oracle runner with serialized transforms, the
minimization loop, the repro builder — exact commands with read-outs
and gates), and the rigid run-order binding all of it onto M1–M6.
Load it when the hunt runs: the doctrine states the posture, the
M-protocol states the procedure — the operator OS is how the agent
BEHAVES while executing, characteristic of Tavis Ormandy. Since
v1.1.0 it also ships **The opening ladder** (A18): where Ormandy's
candidates come from — the perception layer that PRODUCES ranked
parser candidates by the privilege × deployment × hostility census
before any harness is built (rungs write census rows, never inputs;
ranking rationale stated; generation falsifier on record; the
parser-census kit is the pinned desk row set).

## 5. Procedure — Numbered Actions

1. **Scope the census** (M1): write the census header — the
   engagement's software classes, and the boundary rows (why this is
   harness-smith and not feedback-fuzzer's search loop or
   scan-economist's network sweep — one sentence each, on record).
2. **Census the privileged parsers** (M1): every in-scope component
   that parses untrusted input, each row pinned with privilege level
   (kernel/SYSTEM/user), deployment breadth (every endpoint /
   server-only / optional), and input hostility (network-remote /
   file-attached / local). Rank by the product; the top rows are the
   targets. A census with fewer than three rows is a product review,
   not a class hunt — park and say so.
3. **Engineer the harness** (M2): for the top-ranked parser, decide
   the harness gate — adapt an existing corpus, wrap the component
   in-process with coverage instrumentation, or build the missing
   instrument (the ctftool rule: weeks are the budget, not a
   blocker). Distill the corpus (set-cover against measured
   coverage); record the distillation arithmetic.
4. **Declare the oracle** (M3): pick the oracle class BEFORE the
   first run — crash/sanitizer, state-comparison, or serialized
   (for non-deterministic or concurrent targets); write its decision
   rule and its known blind spots. No oracle declared, no run
   starts.
5. **Run, triage, minimize** (M4): the fuzz campaign runs under
   feedback-fuzzer's loop discipline where it applies; every crash
   candidate reproduces n ≥ 2, dedupes by failure class, and is
   delta-minimized toward the three-command-class repro. The
   minimization ledger rides with the finding.
6. **Report publicly, reproducibly** (M5): the report ships the
   minimized repro verbatim, the affected versions, and the vendor
   notice — by direct report/email, WITHOUT agreeing to terms first
   (the lineage's documented stance); deadlines follow the house
   disclosure policy; fast vendor responses are acknowledged on
   record (the 2017 Msftsecurity kudos shape).
7. **Postmortem the miss** (M6): for every CONFIRMED finding, write
   the missed-why row — which defenses (the project's own fuzzing,
   static analysis, code review, sandboxing) SHOULD have caught it,
   and the mechanical reason each did not. File the residual register:
   what still would not have caught it.
8. Every step files its record in the ledger (R-NNN); a census row, a
   harness decision, an oracle declaration, or a missed-why row
   without its record is an anecdote, not a measurement.

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Census rows, harness decisions, oracle declarations | `dossier_add` + this organ's M1–M3 record formats |
| Corpus distillation arithmetic | computed on record (references/method-upgrade.md M2; recompute, never recall) |
| Fuzz campaign execution (once target+harness+oracle exist) | feedback-fuzzer organ (its loop and stop rules govern) |
| Crash reproduction and minimization | governed probes + the M4 minimization loop |
| Report drafting, vendor notice | `dossier_render` + report organs (report gates apply) |
| Classification at report time | `cvss3_score` + `vrt_classify` |

## 7. Hard Rules

1. The census before the harness: a fuzz run against an uncensused
   target list is refused — ranking IS the method.
2. No oracle, no run: every campaign states its oracle class and
   blind spots before the first input is fed.
3. The repro ships minimized: a finding reported from an unminimized
   blob is a LEAD; the minimization ledger explains any floor it
   could not pass.
4. No terms before reporting: vulnerability reports go out without
   agreeing to platform or vendor terms — the vendor is free not to
   read them; the house disclosure policy rides on record.
5. Every CONFIRMED finding carries its missed-why row: a bug that
   cannot say why the ecosystem missed it is half-shipped.

## 8. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Running the full hunt end to end (census schema, harness gates, oracle classification, minimization, postmortem) | references/method-upgrade.md |
| Running the hunt — the Ormandy runtime: the opening ladder (A18), thinking rules, situation-to-action behavior, scripting, rigid run-order | references/operator-os.md |
| Checking what was actually read; the census, read ledger, psych-read evidence | references/sources.md |
