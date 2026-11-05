# The executable method — the onboarding-preservation upgrade (W1–W6 → M1–M6)

> Part of **mythos-bug-hunter v4.8.0** (package architecture).
> **Load when:** onboarding a new operator or a fresh agent onto the
> stack; pinning corpus state at engagement start; a version bump of any
> bundle; drift suspected between doctrine rows and tool rows. The
> lineage layer's provenance lives in
> [`sources.md`](sources.md); the operator runtime in
> [`operator-os.md`](operator-os.md). Section numbering follows the
> spine's module convention.

This is the spine's first method-upgrade layer: the Jason Haddix
lineage (the queue's seventh execution) imported the corpus's own craft
— **methodology packaging**: an entire hunt compressed into a versioned,
re-runnable playbook a newcomer can run, with the deck itself as the
method artifact ("this preso ended up to be way too much to fit in a
45min talk so ... we turned it into a Git project" — the repo exists
because the talk overflowed). The spine's onboarding path now carries
that craft as its preservation protocol: what a newcomer must be pinned
to, what must be re-verified per era, and what proves the onboarding
happened.

## 1. The critique (W1–W6) — what was weak in the corpus's shipped form

The critique targets the FORM, not the figure; the license is the
attribution ledger (sources.md §4). Each floor below is documented in
the artifacts read:

* **W1 — versions without a version rule.** The series re-forges fast
  (v1 2015 → v2 2017 → v3 2018 → v4 2020 → Live 2023/24 → Core 2024+,
  with a two-deck split inside v4) and never states which parts churn
  (tools, sources, API limits) and which are durable (the philosophy,
  the question set, the checklists). A newcomer inheriting "the
  methodology" cannot tell perishable from persistent.
* **W2 — curation entangled with method.** His own method rows (the
  Big Questions, heat mapping, the HUNT parameter lists, wide-vs-
  narrow doctrine) ship interleaved with curated tool rows that rot on
  a different clock. Attribution is present everywhere — but there is
  no mechanical split between what a house must OWN (doctrine) and
  what it must merely RE-VERIFY per era (other people's tools).
* **W3 — checklists without gates.** The Fast Testing Checklist is
  task-checkboxes without pass/fail criteria, entry conditions, exit
  gates, or falsifiers. "Run the checklist" produces no
  completion-quality signal: a run with every box ticked and zero
  evidence captured looks identical to a rigorous one.
* **W4 — numbers without denominators.** "For every subdomain you find
  you 2x your chance of hacking the target. For every apex domain ...
  4x"; "configuring the APIs ... increases their efficacy by up to
  50%"; "about 3-10% increased discoveries"; the HUNT parameter
  likelihoods. All rules-of-thumb shipped as multipliers — no
  measurement protocol, no sample basis, no re-validation trigger.
* **W5 — onboarding assumes a human with a GUI.** The corpus onboards
  via conference decks, a paid course, and a Discord community. The
  newcomer's proof-of-competence is never defined: no first-run gate,
  no bounded first engagement, no calibration record separating "has
  watched the methodology" from "can run it".
* **W6 — the carriers drift.** Deck → repo → class → course re-state
  the methodology with content skew: the repo's per-class chapters
  stalled in 2016–2020 while the decks kept versioning (12_IDOR is a
  "To be continued ..." stub to this day). No canonical-anchor rule
  says which artifact is authoritative for which era — the version
  pinning this census had to do by hand is exactly what the corpus
  never did for itself.

## 2. The upgrades (M1–M6) — the executable preservation protocol

Each M answers named W's. An agent with zero prior exposure to the
figure runs this at full precision.

### M1 — PIN THE STATE (answers W1, W6)

At engagement start (Mode F/E entry, immediately after the R0 scope
record), emit the corpus pin into the engagement state:

```
PIN: corpus-state charter=<vX.Y.Z> spine=<vX.Y.Z> organs-loaded=<n>
  modules-pinned=<n> doctrine-rows=<n> curation-rows=<n, era-stamped>
  stamp=<iso-date> drift-policy="diff-before-bump, re-verify before
  first use"
```

Rules: the pin names the exact versions of the charter, the spine, and
every organ actually loaded for this engagement (not the whole corpus
— what is loaded is what can betray you). Doctrine rows and curation
rows are pinned with different expectations: doctrine is
version-stable until bumped; curation rows are era-stamped and
re-verified before first use (M2). An engagement never runs on an
unpinned state — the activation contract's preconditions (§1.2 of
activation-and-modes.md) gain this line.

### M2 — SPLIT METHOD FROM CURATION (answers W2)

Every onboarding artifact the operator ships — this corpus's own
modules included — carries the two-column split:

```
SPLIT: artifact=<module> method-rows=<owned, doctrine, version-stable>
  curation-rows=<attributed tool/source, era-stamp, re-verify-flag>
```

A tool row without an era stamp and an owner name is a defect, not a
style issue. Curation rows carry their attribution (A3) inline; the
row's truth lives in the tool's own current state, which M2's
re-verification step queries at first use — existence, behavior
change, paywall/rot ("the Twitter API workflow died", "WPscan went
paid" — the corpus's own rot record, turned into a mechanical step).

### M3 — CONVERT CHECKLISTS TO GATES (answers W3)

Every task row in an onboarding checklist gains three fields:

```
TASK: <row> entry=<precondition> evidence=<ledger record | capture |
  probe output | PIN field> falsifier=<what result marks it NOT done>
```

A row without its evidence artifact is NOT done — whatever the
checkbox says. This is the Fast Testing Checklist's form, upgraded
with the closure discipline the spine already enforces for hypotheses
(§7, §13): onboarding tasks close exactly the way findings do.

### M4 — CLASSIFY EVERY NUMBER (answers W4)

Any quantified claim entering the corpus (multipliers, efficacy
percentages, parameter likelihoods — his or the house's) carries a
basis class:

```
NUM: claim=<x> basis=<measured | stated-rule-of-thumb | heuristic>
  sample=<n | none-stated> revalidate=<trigger>
```

Rule-of-thumb numbers enter as capped priors (the §10 likelihood
discipline owns them: priors from stated-rule-of-thumb start ≤60%
pending behavioral confirmation, exactly as mistake-ledger calibration
already prices version-derived priors). A multiplier used where its
basis class is rule-of-thumb is a §13 report-contract violation in
the making — numbers that price effort must say what they are made
of.

### M5 — THE NEWCOMER PROOF GATE (answers W5)

A fresh operator or agent's first run is a bounded canary engagement:

```
PROOF: newcomer=<id> run=<canary-mode engagement> gates=<auditor
  exit-0, ledger discipline, closure states> calibration=<priors set
  vs observed, recorded> live-scope=<REFUSED until PROOF closes>
```

The first engagement runs the SAME gates a veteran runs — the
auditor, the ledger, the closure states — on self-owned targets
(the proving-ground labs). "Has read the methodology" is not a
competence state; a closed PROOF record is. Requests for live scope
without a PROOF record are refused with the routing rule (R4).

### M6 — THE DRIFT AUDIT (answers W1, W6)

At every version bump of any pinned bundle, before adopting it:

```
DRIFT: old-pin=<hash> new-pin=<hash> doctrine-delta=<rows>
  curation-rot=<rows past era or behavior-changed> reverify-queue=<n>
  ledger-record=<R-NNN>
```

The drift record is kept — what changed, what rotted, what needs
re-verification — and the rot rows surface as TODOs before the first
request. The repo-vs-deck skew (W6's evidence) is what this step
exists to prevent inside this corpus: no bump lands silent.

## 3. Where the upgrades land (the wiring)

* The spine's reference library (§17 of SKILL.md) gains the three
  module rows this layer ships in: method-upgrade.md (this file),
  operator-os.md (the runtime), sources.md (the provenance ledger).
* The activation contract (activation-and-modes.md §1.2) gains the PIN
  precondition (M1).
* The quick-reference card (§18) gains the pin line.
* The A16/A17 universality guards now cover the spine as the 35th
  method-upgrade module and the 30th operator-os module — the spine
  is the first non-lineage-born organ to adopt the two layers, via
  documented upgrade, born in this commit (not retrofitted).
* The lineage registry entry (mythos_lineages, organ mythos-bug-hunter)
  carries the figure, the distillation, the sources pointer, and the
  corrections.

## 4. Falsifiers

The layer is falsified — mechanically, in the ledger — if any of these
appear:

1. An engagement's state carries requests with no PIN record.
2. A checklist row reads complete with no evidence artifact.
3. A multiplier prices effort while its basis class is
   stated-rule-of-thumb with no revalidation trigger.
4. A tool row past its era stamp fires without a re-verification
   record.
5. A newcomer with no closed PROOF record holds live scope.
6. A version bump lands with no DRIFT record in the ledger.

Each is a defect named at audit time, not a judgment call; the fix is
the missing record, produced before the next run.
