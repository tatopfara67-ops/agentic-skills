# sources.md — the census, read ledger, and psych-read evidence

The verification record for the harness-smith forge (the third
candidate-queue execution). What was actually read, in what depth,
and what every psych-read line cites.

## 1. The census and the reading bound

The Ormandy report corpus is enormous — hundreds of public Project
Zero tracker reports across Windows, antivirus engines, crypto
libraries, password managers, and CPUs. The honest bound (per the
queue's Q5 gate): the tracker corpus is NOT read line-by-line; the
census reads the method-bearing long-form artifacts in full, the
event record multi-sourced, and the boundary is stated here rather
than silently collapsed into snippet-mining.

| Artifact | Class | Year | Read status |
| --- | --- | --- | --- |
| "This shouldn't have happened: A vulnerability postmortem" (BigSig, NSS) — projectzero.google | long-form blog (own) | 2021 | READ-FULL |
| "Down the Rabbit-Hole" (MSCTF / ctftool research) — projectzero.google | long-form blog (own) | 2019 | READ-FULL |
| "How to Compromise the Enterprise Endpoint" (the Symantec disclosures) — projectzero.google | long-form blog (own) | 2016 | READ-FULL |
| Zenbleed writeup — cmpxchg8b.com (his own site) | long-form writeup (own) | 2023 | READ-FULL |
| "Fuzzing at scale" — Google Security Blog (with Chris Evans, Matt Moore) | long-form blog (own) | 2011 | READ-FULL |
| "The poisoned NUL byte, 2014 edition" — projectzero.google (Chris Evans on the Ormandy glibc bug; the wargame culture) | long-form blog (about, by teammate) | 2014 | READ-FULL |
| HITB 2009 speaker record / abstract (model inference assisted fuzzing, set cover) — conference record | talk abstract | 2009 | READ (abstract + bio) |
| Personal site taviso.decsystem.org (About/Research/Resources; superseded by cmpxchg8b.com) | site census | — | READ (index) |
| Documented X/@taviso posts: no-terms stance (2019); "never fuzzed or audited… irresponsible to ship code like this" (2020); Defender recommendation; Msftsecurity kudos (2017) | documented posts | 2015–2020 | READ (captured) |
| Press record, multi-sourced: Wired (Symantec 2016; "billion PCs" MsMpEng 2017), Computerworld (Kaspersky emergency patch 2015), SecurityWeek (MsMpEng fuzzing 2017; Kaspersky cert flaws 2017), ZDNet (2017, "bugs in products from just about every major vendor"), AMD advisory AMD-SB-7008 + PCWorld/Windows Central (Zenbleed 2023: reported May 15, 2023; microcode coordination), LastPass extension bugs (2016, 2019) | press/advisory record | 2015–2023 | READ (multi-source) |
| The Project Zero bug tracker corpus (his hundreds of reports) | bug reports | 2014–2023 | BOUNDED: not read line-by-line — selection criteria: long-form method-bearing writing first; tracker reports cited only via their public titles/press where an event fact needed a second source |

## 2. The psych-read — documented behavior, per lens

* **L1 heuristics** (repeating shortcuts, ≥ 3 independent artifacts
  each):
  * Fuzz-first discovery — 2011 (corpus distillation at scale), 2017
    (SecurityWeek: the MsMpEng heap overflow found by fuzzing), 2021
    (call-stack-monitoring fuzzer found BigSig), 2023 ("I found this
    bug by fuzzing, big surprise 🙂").
  * The privileged parser as target — 2016 (Symantec: unpackers and
    emulators, loaded in the kernel), 2017 (the Defender signature
    engine parsing every file), 2019 (the undocumented MSCTF IPC
    protocol, no access control), 2021 (NSS parsing every
    certificate/signature).
  * Simple test case → chase the discrepancy — 2019 (the
    rabbit-hole's opening move, quoted), 2016 (NASM testcase +
    debugger verification), 2021 (the three-command repro).
  * Build the missing instrument — 2019 (ctftool, weeks, own
    scripting language), 2021 (the call-stack library, "a lot of
    optimization"), 2023 (the serialized-oracle transformer).
* **L2 obsession** (the multi-year arc): software parsing the least
  trusted input at the highest privilege — the AV engine arc
  (Kaspersky 2015 → Symantec 2016 → Defender/Trend/McAfee/ESET/
  Comodo/FireEye/Sophos 2016–2018, per the ZDNet summary and his own
  "we've written about examples in" list), then crypto libraries
  (glibc 2014, NSS 2021), then silicon (Zenbleed 2023). And the
  set-cover/corpus-distillation thread: 2009 talk → 2011 blog → the
  2021 fuzzer's token extraction/recombination.
* **L3 aesthetics** (his own words, cited): "This shouldn't have
  happened" (2021 title — the simple-bug-in-critical-parser shame);
  "Sometimes, hacking is just someone spending more time on something
  than anyone else might reasonably expect" (2019); "It's
  irresponsible to ship code like this" (2020); "It turns out that
  memory management is hard, even in silicon 🙂" (2023); "These
  vulnerabilities are as bad as it gets" (2016); the reproducibility
  flourish — "Reproducing the BigSig vulnerability in three easy
  commands" (2021).
* **L4 failure mode** (how being wrong is handled): the BigSig
  postmortem (2021) is a public self-and-ecosystem examination —
  "This should have been caught earlier, and I want to explore why
  that didn't happen"; the Zenbleed writeup credits colleagues by
  name (Eduardo Vela Nava, Alexandra Sandulescu, Josh Eads). Documented
  wargame culture around his own bugs (the 2014 poisoned-NUL-byte
  wargame, Chris Evans' post).
* **L5 cadence** (when the hunt stops and disclosure ships): the
  Project Zero 90-day policy; the 2017 Friday-night public
  announcement of the MsMpEng bug (Wired); the 2015 Kaspersky
  emergency patch; Zenbleed reported May 15, 2023, disclosed July
  2023 in coordination with AMD's microcode rollout, workaround
  published free (the wrmsr chicken bit). Public kudos for fast
  vendor response (2017, Msftsecurity).

## 3. Cross-lens rows (the assembly crosswalk inputs)

* **Risk appetite**: targets where the entire industry depends —
  AV on every endpoint, NSS in every browser, AMD Zen 2 in every
  server (documented target set, 2015–2023).
* **Evidence standard**: the public, reproducible bug report AS the
  artifact — minimized repro, pinned versions, testcase attached
  (BigSig's three commands; the NASM testcase of 2016).
* **Composition habit**: techniques stack — corpus distillation +
  coverage feedback + call-stack monitoring + oracle serialization;
  tools built on tools (ctftool's scripting, the 2021 library's
  optimization).

## 4. Quarantined opinions (the OPINION gate — never feed distillation)

```
OPINION figure=Tavis Ormandy lens=L3 reading="conceives bugs in the
  shower (the LastPass anecdote)" artifact=PRESS-RECORD-ONLY
  status=quarantined next=a primary artifact (his bug report or post)
  would admit it; the press retelling is not admissible
OPINION figure=Tavis Ormandy lens=cross reading="the lack of an EE
  background helped him find Zenbleed" artifact=HIS-OWN-CLAIM
  status=admissible-as-aesthetic-only (his stated outsider view,
  cited to the 2023 writeup; not evidence about method mechanics)
```

## 5. The attribution note

Nothing here is his code or his words beyond quoted fragments; the
organ ships his DECISION LOGIC re-expressed as engagement rules
(the charter's A3 assimilation doctrine). Corrections belong in the
registry entry; none on record at forge time.
