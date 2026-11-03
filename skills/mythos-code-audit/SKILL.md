---
name: mythos-code-audit
version: 1.0.0
type: ai-skill
architecture: package
description: >-
  White-box source-code audit engine and the companion skill to
  mythos-bug-hunter. Use this skill whenever the operator wants source code
  audited for vulnerabilities, a dependency or library checked before use, a
  patch or version-pair diff analyzed, a silent patch mined for unfixed
  variants, crypto usage reviewed for misuse, or a hypothesis about code
  behavior proven or falsified at runtime. Core doctrine: static analysis
  proposes, the runtime disposes — no finding ships without a differential
  oracle. Ships with a calibration proof (rediscovery of CVE-2024-33663 and
  CVE-2024-33664 plus two predicted variants, example/worked-example.md).
category: security/white-box-audit
license: MIT
metadata:
  author: tatopfara67-ops
---

# mythos-code-audit v1.0.0 — The White-Box Engine

## 0. What This Skill Is — and Is Not

- **Is**: the white-box half of the Mythos stack. Where mythos-bug-hunter
  (v4.1.0) aims an agent at a running target and disciplines what comes back,
  this skill aims an agent at *source code* and disciplines what comes out:
  every static observation is a **hypothesis** until a runtime oracle confirms
  it. The one-line law: **static analysis proposes; the runtime disposes.**
- **Is not**: a "dangerous function grep with extra steps." Market code-audit
  skills list sinks (`eval`, `exec`, raw SQL) and stop there. Lists do not
  survive triage. This skill ships three things the market does not:
  1. **Oracle discipline** — every finding is a *differential experiment*
     (vulnerable arm vs fixed arm, treatment vs regression control), with
     reproduction counts, not a screenshot of a grep hit.
  2. **Patch archaeology** — recently fixed bugs are mined for *variants that
     remain unfixed*. A fixed bug is proof the bug class lives in this
     codebase; its siblings are the highest-prior hypotheses in the entire
     audit. No market skill does this; it is the Big Sleep engine.
  3. **A crypto misuse catalog** — 16 usage classes with a runtime oracle per
     class. Crypto primitives are never the target; their *usage* is.
- **Calibration, not promises.** The package ships with a worked engagement in
  which the method rediscovered two real CVEs from a version diff and
  *predicted two additional variants from the shape of the old code*, then
  confirmed them at runtime (§16). If the method stops working, the
  calibration example is the first thing to re-run — an uncalibrated
  instrument is a random number generator.

Package layout:

```
mythos-code-audit/
├── SKILL.md                     # this file — the only always-loaded part
├── README.md                    # positioning, install, calibration quickstart
├── references/                  # load-on-demand library (4 modules)
│   ├── patch-archaeology.md
│   ├── trust-map-and-sinks.md
│   ├── crypto-misuse-catalog.md
│   └── differential-oracles.md
├── scripts/
│   ├── audit_code_report.py     # mechanical slop auditor for white-box reports
│   └── two_arm_harness.py       # reusable differential harness template
└── example/                     # calibration engagement + audit fixtures + raw evidence
```

## 1. Stack Integration

This skill shares the Canon, the ledger format, the Closure vocabulary, and
the No-Slop law with **mythos-bug-hunter v4.1.0**. They compose into one loop:

```
mythos-bug-hunter (black-box)      mythos-code-audit (white-box)
  recon → hypotheses → oracle   ←→  diff → variants → oracle
        └────────── shared ledger R-NNN ──────────┘
```

- Findings from either side enter the same ledger and obey the same report
  contract.
- White-box output feeds black-box engagements (a code-level hypothesis about
  a deployed product becomes an HTTP-level experiment there) and vice versa.
- Conflict rule: if the two skills ever disagree on procedure, the one whose
  gate is *mechanical* wins; if both are mechanical, the stricter wins.

## 2. The Canon — White-Box Instantiation

The eight rules are inherited verbatim from mythos-bug-hunter v4.1.0 (see its
SKILL.md §1 for the canonical text and mechanical enforcement). Here is what
each rule *means on a code audit*:

| # | Rule | White-box instantiation |
|---|------|------------------------|
| **R0** | Authorization gate | Auditing your own copy of code — a repo you own, a dependency installed in your own environment — is always in scope (you are auditing your own supply chain). Anything else (a vendor's private tree, a leaked source drop) requires an authorizing artifact in Phase 0. |
| **R1** | Plan before action | The trust map (Phase 1) and the diff inventory (Phase 2) exist *before* deep reading and before any payload runs. Discoveries mid-audit go to the backlog. |
| **R2** | Finish or formally park | A code path is closed only by Closure or a Park record with a resume point. "Got bored of the crypto module" is not a state. |
| **R3** | Victory language is gated | JACKPOT/BREAKTHROUGH only attached to a Closure line with oracle results in the same breath. The auditor rejects anything else. |
| **R4** | No lying, no premature conclusions | A claim without a ledger record ID is syntactically invalid (No-Slop law). "Looks vulnerable" is not a state — CONFIRMED / FALSIFIED / INCONCLUSIVE are. |
| **R5** | Tools are evidence generators | semgrep / CodeQL / bandit output is a **hypothesis factory**, never a findings list. Every scanner hit becomes an H-record and passes the same oracle gates. |
| **R6** | Scripts are instruments, calibrated | The two-arm harness runs control cells with known outcomes before any treatment cell counts. An uncalibrated harness is noise with a log line. |
| **R7** | Effort budget | Default: 12 cells per hypothesis cluster, 300 ledger records per audit, operator-tunable at Phase 0. Exhausted budget → Park, not an infinite loop. |

## 3. The White-Box Contract

> **No finding ships without a runtime oracle.** A finding is confirmed only
> when a differential experiment shows the vulnerable behavior and the
> regression control keeps passing. Static evidence alone can justify a
> hypothesis, a Park, or a note — never a CONFIRMED finding.

Consequences:

- Every CONFIRMED finding carries a **code anchor**: `path/to/file.py:LINE@version`
  (or commit hash). Unanchored findings are syntax errors.
- Every CONFIRMED finding carries the **violated invariant** in one sentence
  ("the key type must match the token algorithm family").
- Every CONFIRMED finding carries the **regression control** result: the
  legitimate flow still works on both arms. A fix that breaks legit flow is
  not a finding, it is a different finding — and a park.
- Findings you cannot afford to test go to the **Park lot** (§4.4 of
  mythos-bug-hunter; format below in §12) with a resume point, not into the
  report with the word "probably."

## 4. The Evidence Ledger (white-box format)

One record per observation, append-only, pipe-separated — identical field
order to mythos-bug-hunter so both skills write the same book:

```
R-NNN | ISO-8601 | tool | action | target(file:line@ref) | result | size | tags | note
```

White-box tags: `AUTH`, `PROVENANCE`, `ENV`, `TRUST-MAP`, `PATCH-DIFF`,
`HYP`, `CELL`, `FACT`, `CONTROL`, `CANARY`, `PARK`, `MISTAKE`, `REPORT`.

Storage discipline is inherited: full records on disk, summary + IDs in
context. The report is written only from the ledger (role separation).

## 5. The Pipeline — Six Phases with Hard Gates

| Phase | Purpose | Exit gate (mechanical) |
|-------|---------|------------------------|
| **0** Scope, provenance, environment | Authorized scope, pinned versions, a *runnable* two-arm lab | `AUTH` + `PROVENANCE` records exist; both arms import and pass a smoke test |
| **1** Trust map | Terrain: entry points, trust boundaries, guards, sinks | every entry point has a `TRUST-MAP` row |
| **2** Patch archaeology | Mine fixed bugs for surviving variants — **runs before deep reading** | every security-relevant diff hunk → hypothesis or Park; every blacklist hunk gets an enumeration-gap analysis |
| **3** Hypothesis forge | Operators + catalog turn the map into pre-registered hypotheses | all H-records committed before any treatment cell runs (no HARKing) |
| **4** Oracle construction | Two-arm differential harness; cells with verdicts | every CONFIRMED has treatment delta + regression control VERIFIED on both arms; every ERROR cell resolved or voided |
| **5** Impact, report, audit | Canary-bounded impact, ledger-only report, mechanical audit | auditor exit 0 on the report, exit >0 on the sloppy fixture (dual control) |

### Phase 0 — Scope, Provenance, Environment

1. `AUTH` record (R0). Auditing a dependency installed in your own
   environment is self-authorized; write it down anyway.
2. `PROVENANCE` records: pin **both arms** — exact version or commit each,
   how obtained (`pip download --no-deps --no-binary :all: pkg==X`,
   `git fetch`), and the hash of what you got. An audit without pinned arms
   is a blog post.
3. **Environment curation — era-match the dependencies.** Old code expects
   old libraries. In the calibration engagement, python-jose 3.3.0 (2021)
   against cryptography 50.x (2026) broke inside the JWE path with
   `module 'lib' has no attribute 'RAND_bytes'` — an *instrument* failure
   that masquerades as a *behavior* difference. Pin both arms to a common,
   era-compatible dependency set **before** concluding anything from cells.
4. Capability census: can the code be imported? Does its own test suite
   pass on both arms? If the code cannot run, say so in Phase 0 — static-only
   audits are allowed but every finding is capped at hypothesis strength.
5. Canary seeding: choose a canary value now; it rides inside test claims
   for the whole engagement (§8).

### Phase 1 — Trust Map

Census, not reading: entry points (routes, handlers, RPC methods, queue
consumers, CLI args, cron jobs), trust boundaries (where untrusted input
crosses into privileged code), authorization checkpoints, and crypto
touchpoints. Output is a table, one row per entry:

```
entry                → parser            → guard                 → sink
jwt.decode(token,k)  → jws._load         → alg allowlist,        → backend verify,
                        header             HMACKey blacklist        zlib.decompress
```

Reading order is **edges → guards → sinks → middle**. The middle of a
codebase is where bugs go to die of old age; the edges are where they are
born. Details and the sink catalogs: `references/trust-map-and-sinks.md`.

### Phase 2 — Patch Archaeology (before deep reading)

The highest-yield vein in source auditing: a fixed bug is a *proof* the class
exists here, and fixes are frequently incomplete. Protocol — collect the diff
(version pair or commit range), triage hunks for security relevance
(silent-patch heuristics), reconstruct the invariant, then **sweep for
variants** the fix missed. Special move: **enumeration-gap analysis** — when
the old code guarded with a *list* (blacklist/allowlist), the list is a map
of its author's blind spots; diff the list against the family it belongs to
and every missing member is a pre-registerable variant. Full protocol with
worked micro-cases: `references/patch-archaeology.md`.

### Phase 3 — Hypothesis Forge

Operators (§9) applied to the trust map; crypto touchpoints looked up in the
misuse catalog (§10 / `references/crypto-misuse-catalog.md`); every candidate
becomes a pre-registered H-record in the 5-slot contract (§6). Priors are
stated, not implied: a variant predicted from an enumeration gap starts at
60–75%, a bare scanner hit at 5–15% (guidance table in
`references/trust-map-and-sinks.md`).

### Phase 4 — Oracle Construction

Every hypothesis gets an oracle: the minimal runtime experiment whose
outcome changes iff the hypothesis is true. Build it as a **two-arm
differential harness** (template: `scripts/two_arm_harness.py`): vulnerable
arm vs fixed arm, each running identical **cells** —

- **treatment cell** — the attack input;
- **regression control cell** — the legitimate input that must keep working
  on both arms;
- **boundary probe** — which configs/mitigations stop the attack and which
  do not;
- **variant probe / marker probe** — sibling inputs predicted by the sweep.

Cell verdicts: `VERIFIED` (behavior occurred), `REJECTED` (a control fired),
`ERROR` (the instrument itself failed — environment rot, import breakage).
Conflating REJECTED with ERROR is how false negatives are born; the harness
classifies them separately and ERROR cells void the run until fixed.
Reproduction floors and stability rules: §7. Full oracle design patterns:
`references/differential-oracles.md`.

### Phase 5 — Impact, Report, Audit

Impact is proven with the canary inside the forged input, in the self-owned
lab, against versions you pinned — never against real data or third-party
systems (§8). The report is written from ledger records only and must satisfy
the Report Contract (§13). Then run the auditor in **dual control**: the
worked example passes (exit 0) and the sloppy fixture fails (exit >0). An
auditor that cannot fail its own negative control is decoration.

## 6. The Hypothesis Contract (code edition)

Five slots, committed before the treatment runs:

```
H-NNN
  claim        : one sentence, falsifiable
  anchor       : path/file.py:LINE@version (or @commit)
  invariant    : the rule the code should uphold
  oracle       : cell design + falsifier (what result falsifies the claim)
  prior        : stated %, with its reason (patch sibling / enumeration gap /
                 scanner hit / smell)
```

Closure maps to cell evidence: `CONFIRMED` (differential reproduced at the
floor), `FALSIFIED` (the control held — including "good news" falsifications
like a mitigation that works), `INCONCLUSIVE` (budget exhausted or the cell
only partially executes, e.g. a marker probe) — INCONCLUSIVE blocks must
carry a Park ID.

## 7. Closure and Reproduction Floors

- **Deterministic behavior** (crypto math, parsing, guards — most of what
  this skill touches): floor **3 identical runs** per arm. "Identical" means
  verdict + digit-normalized detail: `re.sub(r"\d+", "N", detail)` — timing
  jitter is not instability, and treating it as such wastes budget (mistake
  ledger entry in the calibration engagement).
- **Stochastic behavior** (races, hash-order, GC): floor 20 runs with a
  stability criterion (two consecutive 10-run windows within 10pp).
- **Budget exhausted without a stable read** → `INCONCLUSIVE` + Park. No
  exceptions, and no "it worked once, ship it."

## 8. Impact Proof Without Harm

White-box edition of the mythos rule: the impact chain runs entirely in your
own lab —

1. Forge the input with a **canary** value inside it
   (`MYTHOS-CANARY-<8hex>`, chosen in Phase 0).
2. Show the canary **round-trips** through the vulnerable path (the forged
   token verifies and its claims — the canary among them — come back).
3. Bound the blast radius: affected versions, required config (e.g. "alg
   allowlist includes HS256 alongside an asymmetric family"), preconditions.
4. Zero real data. A dependency audit that exfiltrates nothing and touches
   nobody is an audit nobody can ask you to stop running.

## 9. Warzone Operators — Applied to Code

| Operator | Code application | From the calibration engagement |
|----------|------------------|--------------------------------|
| **Inversion** | For every guard: *what input is accepted-but-wrong?* | 3.3.0's HMAC guard rejects PEM strings → invert: which string shapes pass? → OpenSSH formats |
| **Rotation** | Force the sibling: other backend, other format, other entry point | guard tested in `backends/native.py` → rotate to `cryptography_backend.py`; JWS path → rotate to JWE path |
| **Abduction** | Weirdest artifact → best explanation → testable prediction | the blacklist contains `ssh-rsa` but no EC/Ed25519/DSS markers → "the author enumerated from memory" → predicts `ssh-ed25519` slips through (confirmed, E7C) |
| **Variant analysis** | Fixed bug → same shape elsewhere | the confusion fix → check *every* key construction path; the JWE cap → check every decompression site |
| **One-step-back** | Odd code → step back to the design level | the fix replaced a *shape check* (string blacklist) with a *structure check* (`is_pem_format or is_ssh_key`) → what other shape checks exist in this codebase? |

## 10. Crypto Misuse Catalog (summary)

Doctrine: **primitives are not targets; usage is.** No agent breaks AES in a
skill session, and any report claiming to is slop. The 16 usage classes, each
with static signature, violated invariant, runtime oracle, common false
positive, and severity gate, live in `references/crypto-misuse-catalog.md`:

CLASS-01 alg-not-pinned · CLASS-02 key-type confusion · CLASS-03 cipher-mode
misuse · CLASS-04 unauthenticated encryption · CLASS-05 hash downgrade ·
CLASS-06 MAC-from-raw-hash · CLASS-07 weak KDF · CLASS-08 non-constant-time
compare · CLASS-09 padding-oracle surface · CLASS-10 RNG misuse · CLASS-11
hardcoded/derivable keys · CLASS-12 cert validation bypass · CLASS-13
malleability/replay · CLASS-14 unvalidated header params & decompression
bombs · CLASS-15 kid/rotation confusion · CLASS-16 downgrade negotiation.

Findings in the crypto domain must name their CLASS-NN; the auditor enforces
it. CLASS-02 and CLASS-14 are the two classes rediscovered live in the
calibration engagement.

## 11. Tool and Script Discipline

- **Precision ladder for static work**: AST query > targeted regex >
  plain grep > eyeball. Grep for `eval` in a JS codebase is a hypothesis
  generator with a 95% false-positive rate; an AST call-graph walk is an
  instrument.
- **Scanners are hypothesis factories** (R5): every semgrep/CodeQL hit enters
  the ledger as an H-record with prior 5–15% and waits for an oracle.
- **Environment rot is not vulnerability**: dependency incompatibilities
  produce ERROR cells, and ERROR cells are re-pinned and re-run — never
  reported as behavior. The RAND_bytes incident in the calibration engagement
  is the canonical example.
- **Harness dogma** (R6): cells are pure functions of (arm, input); a crash
  in one cell must not kill the matrix; verdicts are classified, not
  eyeballed; stability is digit-normalized. The template ships as
  `scripts/two_arm_harness.py` and is the recommended starting point.

## 12. Mistake Ledger (format)

Identical to mythos-bug-hunter: every self-correction is recorded, because an
agent that hides its misses trains itself to hide worse things.

```
MISTAKE | H-NNN or phase | what I believed → what happened | pattern to avoid | adjustment made
```

## 13. The Report Contract (white-box syntax)

1. Written only from ledger records; every severity-bearing line cites `R-NNN`.
2. Every CONFIRMED finding carries: code anchor `file.py:LINE@version`, the
   violated invariant in one sentence, per-arm oracle results with `n_runs`,
   and the regression control result.
3. Crypto findings name their `CLASS-NN`.
4. Diff-derived claims cite the version pair (or commit hashes) they came from.
5. CONFIRMED findings carry a **mitigation boundary** section: what
   configuration stops the attack, what does not, with cell evidence — the
   boundary table is often the most valuable part of the report for a
   defender, and it is the part market skills never produce.
6. Impact chains are canary-bounded; zero real data.
7. Closure vocabulary only; INCONCLUSIVE blocks carry a Park ID.
8. Victory language is gated to Closure lines (R3).

## 14. Self-Audit

```
python3 scripts/audit_code_report.py example/worked-example.md      # exit 0
python3 scripts/audit_code_report.py example/sloppy-code-report-fixture.md  # exit 1, N violations
```

Exit 0 = shippable. Exit 1 = violations listed. The auditor checks syntax,
not truth — the ledger remains the ground truth, and its checks are the
white-box additions to the v4.1.0 auditor: code anchors, diff citations,
CLASS citations, regression-control section, Park IDs on INCONCLUSIVE.

## 15. Module Index

| Module | Load when |
|--------|-----------|
| `references/patch-archaeology.md` | a version pair / commit range / advisory is on the table; you are mining fixes for variants |
| `references/trust-map-and-sinks.md` | entering a codebase cold; building the trust map; triaging sinks and validators |
| `references/crypto-misuse-catalog.md` | any crypto touchpoint is in scope (JWT/JWS/JWE, TLS, cipher, KDF, RNG) |
| `references/differential-oracles.md` | designing or running the two-arm harness; verdict taxonomy; reproduction floors |

Conflict rule: SKILL.md wins over any module; a module wins over your
improvisation.

## 16. Calibration and Provenance

This package was calibrated on a real target in a fresh sandbox: python-jose
3.3.0 vs 3.4.0, both arms pinned, era-matched dependencies. The engagement
recorded in `example/worked-example.md`:

- **Rediscovered** CVE-2024-33663 (OpenSSH-key → HMAC-secret confusion) and
  CVE-2024-33664 (JWE decompression bomb) purely from the version diff,
  with runtime differentials on both arms.
- **Predicted** two further variants (`ssh-ed25519`, `ssh-dss`) from the
  enumeration gap in the old blacklist — *before running them* — and
  confirmed them at runtime.
- Mapped the mitigation boundary (single-family allowlists stop the
  confusion even on 3.3.0; mixed-alg configs do not) and kept the regression
  controls green throughout.

Honest limits, stated up front: the target was *chosen* because two CVEs
ship in one version pair — target-selection bias is recorded in the
engagement's mistake ledger. The calibration proves the method executes
end-to-end and self-corrects; it does not prove every audit finds two CVEs.

## 17. Cheatsheet

```
pin both arms            → era-match deps            → smoke test
trust map (edges first)  → diff before reading       → enumeration gaps
pre-register H-NNN       → two-arm cells             → 3× stable or park
canary in the claim      → regression control green  → audit dual control
```

The receipt printer rule, inherited: a report line that cannot trace to a
ledger record is not a weak line — it is an unprinted line.
