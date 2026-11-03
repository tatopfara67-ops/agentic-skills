# The executable method — M1–M6 for harness-smith

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The critique that
justifies each step (why these phases exist, what was weak in the
published Ormandy art) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M6

### M1 — the privileged-parser census

Before any harness exists, one census row per in-scope component:

```
CENSUS: component=<name+version> privilege=<kernel|SYSTEM|user>
  deployment=<every-endpoint|server|optional> input=<network-remote|
  file-attached|local|peripheral> reach=<default-on|opt-in>
  rank_score=<privilege_weight x deployment_weight x input_weight>
  boundary=<vs feedback-fuzzer / scan-economist, one sentence each>
```

Scoring weights are pre-registered per engagement (defaults:
privilege 1–3, deployment 1–3, input hostility 1–3; rank = product,
max 27). The boundary rows are mandatory:

* vs **feedback-fuzzer**: this organ selects the target and
  engineers the instrument; the search LOOP (novelty buckets,
  saturation) is feedback-fuzzer's protocol once target+harness+
  oracle exist.
* vs **scan-economist**: this organ prices PARSER surfaces by
  privilege and deployment, not network sweeps by packets and
  ports; a port sweep budget belongs to the Fyodor lineage.

Gate: top-ranked row(s) selected with the arithmetic on record; a
census with fewer than three rows parks the engagement as a product
review (the Kaminsky-rule shape, applied to parsers).

### M2 — harness engineering and the missing-tool gate

For the selected parser, the harness decision is a recorded gate:

| Option | When | Record |
| --- | --- | --- |
| ADAPT | an existing corpus/harness covers the format | corpus source + version |
| WRAP | the component can be loaded in-process with coverage instrumentation | instrumentation method + entry point |
| BUILD | no instrument exists that can reach the surface (the ctftool case) | the missing-instrument row: what does not exist, and the build budget |

Corpus distillation (the 2009/2011 tradition, made arithmetic):

1. Collect the sample corpus for the format (N files).
2. Measure per-file coverage (blocks/edges reached).
3. Greedy set-cover: repeatedly pick the file that adds the most
   uncovered blocks until coverage of the full set is achieved.
4. Record the arithmetic: `N files → M files, same coverage,
   reduction = 1 − M/N`.

Gate: distillation row on record BEFORE mutation starts; an
undistilled fat corpus is a recorded decision, never an accident.
The BUILD option carries its own gate: weeks are the budget, not a
blocker (the 2019 record: "after a few weeks I had built..."); a
build exceeding its stated budget re-plans rather than silently
overruns.

### M3 — oracle design (declare before the first run)

The oracle class is chosen from the classification table and
pre-registered:

| Oracle class | Catches | Blind spots | Decision rule |
| --- | --- | --- | --- |
| CRASH (sanitizer/segfault) | memory corruption | logic bugs, data leaks | nonzero exit / sanitizer report = LEAD; reproduce n ≥ 2 to promote |
| STATE-DIFF (compare observable state) | logic bugs, parsing divergence | bugs with no observable state change | treatment state ≠ baseline state on identical input = LEAD |
| SERIALIZED (serialize execution, compare final state) | non-deterministic, concurrent, micro-architectural bugs | bugs needing specific interleavings the barrier removes | serialized final state ≠ reference final state = LEAD |
| STACK-MONITOR (call-stack novelty) | deep paths oracles miss | requires instrumentation, slower | new call-stack signature on an input = keep, mutate from |

Gate: `ORACLE: class=<...> rule=<exact decision rule> blind=<stated>`
filed as a record before the first input is fed. The Zenbleed shape
is the model: a random program, its serialized twin, and the
discrepancy between final states — "that could indicate a bug."

### M4 — minimization to the simplest repro

Every CONFIRMED candidate walks the minimization ladder:

1. Reproduce n ≥ 2 with stable failure signature (class + hash).
2. Delta-debug the input: remove chunks; keep the removal if the
   signature survives. Iterate to a fixed point.
3. Reduce the ENVIRONMENT: strip flags, defaults only, minimal
   command line — the BigSig standard is the three-command-class
   repro (`genpkey → req → vfychain`).
4. Record the minimization ledger: sizes at each step + the floor
   reached; a blob that cannot shrink below X bytes keeps the
   ledger row saying why.

Gate: the report cites the minimized artifact; the original blob
stays in the archive. Unminimized findings are LEADs.

### M5 — the public reproducible report and the vendor protocol

1. The report ships the minimized repro verbatim (commands a third
   party can run), affected versions pinned, and the oracle
   declaration that found it.
2. The vendor notice goes out by direct report — WITHOUT agreeing
   to platform or vendor terms first (the lineage's documented
   stance: "I refuse to agree to terms before reporting a
   vulnerability. I prefer email, they're still free to not read my
   reports if they like"). The house disclosure policy and deadline
   ride on record.
3. Emergency handling: a wormable/default-config/kernel finding
   shortens the cycle per the house policy — the 2015 Kaspersky
   emergency-patch shape.
4. Fast vendor responses are acknowledged on record (the 2017
   "can't give enough kudos" shape) — praise is also a public
   artifact.

### M6 — the missed-why postmortem

For every CONFIRMED finding, the mandatory row set:

```
MISSED-WHY: finding=<id>
  defense=<project's own fuzzing | static analysis | code review |
  sandboxing | patch pipeline> expected=<why it SHOULD have caught it>
  actual=<mechanical reason it did not> 
  residual=<what still would not have caught it>
```

The BigSig standard: the postmortem asks why a nine-year-old bounds
bug survived the project's own fuzzing, static analysis, and review
— and answers mechanically (the fuzzers never generated inputs
exceeding the fixed buffer; the code path guarded a case nobody
priced). The residual register names what STILL would not have
caught it — the honest floor.

## 2. Falsifiers — what would prove this method wrong

* A fuzz run started with no oracle declaration on record → the run
  is void; M3 exists because "we'll know a bug when we see one" is
  the exact failure mode that misses logic bugs.
* A census row without its rank arithmetic → the selection was
  vibes; re-rank on record before any harness work stands.
* A minimized repro that fails on a clean environment → the
  minimization corrupted the trigger; back off one step and re-
  verify (n ≥ 2 at every step).
* A missed-why row that names no mechanical reason → it is an
  apology, not a postmortem; rewrite it or strike it.
* The distillation arithmetic does not reproduce (M files do not
  cover what N covered) → recompute; a corpus that silently lost
  coverage is the W2 floor recurring.

## 3. Worked micro-example (numbers consistent, scenario illustrative)

Census (3 rows): AV-engine unpacker (privilege 3, deployment 3,
input 3 → 27); PDF renderer (2/3/2 → 12); image thumbnailer
(2/2/2 → 8). Top rank: the unpacker — kernel privilege, every
endpoint, network-remote input: the 2016 shape exactly.

Harness: WRAP (in-process, coverage-instrumented). Corpus: 40,000
field samples → greedy set-cover → 4,100 files at equal coverage
(reduction 89.75%, on record).

Oracle: CRASH+SANITIZER (blind spot: logic bugs — stated). Run:
feedback-fuzzer's loop governs; 71 crash candidates → 23 unique
signatures → 9 reproduce n ≥ 2 → best candidate delta-minimized
184,233 bytes → 961 bytes → 61 bytes, env-reduced to a
three-command repro.

Report: minimized repro verbatim; vendor emailed directly, no
terms; 90-day clock on record. Missed-why: the project's own
fuzzer (never generated >64KB sections — the BigSig shape),
static analysis (the checker tracks allocations, not
SizeOfRawData-vs-SizeOfImage mismatches), review (the unpacker
predates the review process). Residual: a grammar-aware generator
would still not reach the path — priced, on record.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
The published Ormandy art is real — hundreds of reproducible public
reports, the postmortem tradition, the instrument-building arc — but
it is lived as instinct and narrated per-bug. This module extracts
what is protocol-shaped, names the mechanical weaknesses, and ships
the replacement: a census rule for the target instinct, a harness
gate with distillation arithmetic, an oracle classification table,
a minimization ladder, a no-terms vendor protocol, and a mandatory
missed-why register. An agent that has never read a Project Zero
report must run this at the lineage's precision.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the published method (context, not steps)

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | Target selection by instinct — "I normally write posts to highlight some hidden attack surface", the AV engine arc chosen by taste | The instinct is real but unstated as a rule: an agent inherits the stories, not the selection logic; "look at AV" is a biography, privilege × deployment × input hostility is a census |
| W2 | Instruments announced but shipped late — the call-stack library "planning to open source this in the future" (2021), ctftool released after the research | The BUG repro is public and precise while the TECHNIQUE repro lags; a student can replay the finding but not the finding process |
| W3 | The method lives in postmortems and report narratives, not one protocol — hundreds of tracker reports, each self-contained | The procedure must be reconstructed by reading many narratives; what repeats across them (census → instrument → oracle → minimize → publish) was never written down as steps by the lineage itself |
| W4 | The disclosure cadence lived, never tabled — Friday-night announcements (2017), 90-day deadlines, no-terms email reports, emergency patches (2015), public kudos (2017) | Each cadence decision was correct and public, but scattered; an agent needs the decision TABLE (which situation triggers which clock), not the anecdote |
| W5 | The missed-why postmortem run once — BigSig (2021) asks "why didn't we catch this" for ONE bug | The postmortem is the lineage's crown jewel and its rarest artifact; run per-finding it is a register; run once it is a curiosity |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | The target instinct stated as a census rule with arithmetic | **M1** — the privileged-parser census |
| U2 | The instrument shipped with the finding, and the build decision gated | **M2** — harness engineering + the missing-tool gate + distillation arithmetic |
| U3 | The oracle named before the run, with blind spots stated | **M3** — the oracle classification table |
| U4 | The three-command repro as a standard, not a flourish | **M4** — the minimization ladder with its ledger |
| U5 | The disclosure cadence as one decision table | **M5** — the no-terms vendor protocol |
| U6 | The missed-why question asked of every finding | **M6** — the postmortem row set with its residual register |
