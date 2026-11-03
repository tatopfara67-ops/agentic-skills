---
name: content-discovery
version: 2.2.0
type: ai-skill
architecture: package
description: >-
  Phase-1 content discovery organ, upgraded (v2) with the Daniel Miessler
  (SecLists) lineage — calibrated, rate-courteous wordlist walks that report
  baseline deviations only, backup/config artifact hunting with differential
  triage, plus corpus science: family-based list selection, evidence-derived
  composition, extension derivation from the observed stack, per-base
  recalibration,Since v2.1.0 the organ carries the executable method layer
  (A16) — a mechanical critique of the SecLists-era practice's floors (list
  choice as taste, dictionaries sprayed uncalibrated to the target's naming
  grammar, yield never accounted per list class, freshness unstamped on living
  repo artifacts, interesting-by-glance triage) shipped as protocol M1–M5: the
  question→list-class binding table, grammar calibration harvested from known
  200-class paths, the yield ledger with a marginal-exhaustion gate, the as-of
  stamp rule, and the extension×status×size triage table. Use when the
  operator asks to find hidden paths, hunt backup or config files, brute
  directories politely, or triage discovered files ("cari path tersembunyi",
  "backup hunting", "wordlist", "directory brute", "file discovery", "cari
  .env", "seclists", "wordlist choice").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: v2 — Daniel Miessler (maintainer of SecLists; the corpus-family discipline and composition law)
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# content-discovery v2.2.0 — Calibrate, Then Walk

## 0. What This Skill Is — and Is Not

* **Is**: the Phase-1 organ that finds what the sitemap forgot — with a
  calibrated oracle deciding what counts as "found". The `content_discover`
  tool fires three control requests at random non-existent paths BEFORE the
  wordlist walk: the target's own 404/soft-404 profile IS the baseline.
* **Is not**: an uncapped fuzzer. Requests are GET-only, rate-courteous,
  capped per invocation, and every request lands in the ledger. Since v2
  it carries the **Daniel Miessler lineage** as its field-guide layer —
  corpus science: lists are chosen by FAMILY and composed from evidence,
  never grabbed by size.

## 1. Inherited Contracts

Plugs into **Phase 1** (primary sweep) and **Phase 3** (targeted re-walks)
of the mythos-bug-hunter spine. Inherits the Canon, ledger discipline,
backlog mechanics, and the differential mindset (control first — spine §6).

## 2. The Lineage Layer (v2 — the Miessler doctrine)

**Daniel Miessler** maintains SecLists, the community wordlist corpus
whose family structure (Discovery/Web-Content, Discovery/DNS, Passwords,
Miscellaneous) IS the selection discipline. v2 folds the lineage in as
five field rules, detailed in `references/corpus-science.md`:

1. **Choose by family, not by size.** Discovery/Web-Content feeds this
   organ; DNS families belong to subdomain-hunter; Passwords families
   live behind their own scope wall (§5).
2. **Compose rung-1/2 lists from evidence** (framework markers, JS/API
   conventions); never blast a mega-list. The cap arithmetic in
   `references/wordlists.md` governs composition unchanged.
3. **Extensions derive from the observed stack**; the archive round runs
   only when a signal earned it — then the NEIGHBORHOOD round follows.
4. **New base URL → new calibration round, always.** Soft-404 shapes are
   per-handler; re-using rung-0's profile on a new base is the classic
   false-positive generator.
5. **The password families are out of bounds here.** Authentication-
   surface testing is its own scope row and its own audit story; parking
   is one ledger note.

## 3. Why Calibration Is Not Optional

A bare "status != 404" rule is slop with a for-loop. Targets answer
non-existent paths with soft-404s (200 + "not found" body), wildcard
handlers, and redirect-to-search chains. The calibration round measures the
target's actual behavior on three random junk paths; a finding is a
DEVIATION from that measured baseline — status deviation, or (under
soft-404) a size outlier. `references/wordlists.md` documents the ladder;
the calibration mechanics are enforced inside the tool.

## 3.5 The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published discovery practice where it was mechanically
weak — WHICH list for WHICH question as folk knowledge, common.txt
sprayed against a grammar nobody harvested, no hit-rate or marginal
yield per list class, local list checkouts drifting unstamped for
months, found paths triaged by an operator's glance — and ships the
executable replacement: **M1** the binding table (questions bind list
CLASSES; "it's common" is refused), **M2** grammar calibration
(delimiter class, digits, extensions, locale harvested from KNOWN
paths; path-tied derivatives outperform generic lists by
construction), **M3** the yield ledger (hit-rate AND marginal yield
per list; marginal 0 = exhausted-for-this-target, same-class stacking
refused), **M4** the as-of rule (yield claims cite the stamp; > 90-day
pulls re-fetch before supporting coverage claims), **M5** the triage
table (extension × status × size buckets route every find; the
discount row for drama files; glance-triage refused).

## 3.6 The Operator Layer (A17) — the Daniel Miessler runtime

`references/operator-os.md` ships the figure's documented psychology
as the agent's RUNTIME, in four parts: the thinking framework (numbered
if-then decision rules, each citing the documented behavior it
distills), the behavioral protocol (situation → move → agent action →
refusal, with pacing and failure-reaction rules — how the agent acts
and behaves while hunting), the scripting arsenal (the organ's core
techniques as exact, tool-agnostic commands and micro-scripts, each
with its read-out and decision gate), and the rigid run-order binding
rules, behavior, and scripts onto the M-protocol above. Load it when
the hunt runs: the doctrine states the posture, the M-protocol states
the procedure — the operator OS is how the agent BEHAVES while
executing, characteristic of Daniel Miessler.

## 4. Procedure — Numbered Actions

1. Entry: AUTH record present; base URL in scope (`scope_check`).
2. First walk: `content_discover(program, base, wordlist="default",
   extensions=["", ".bak", ".old", ".zip"])` — capped, default rate.
3. Read the calibration verdict in the result. If `soft_404: true`, treat
   every 200 with baseline size as noise and trust size outliers only.
4. Triage each finding with the matrix in `references/patterns.md`:
   * backup/config artifacts → `backup-artifact` / `config-exposure`
   * redirect findings → `redirect-handler` + record Location
   * auth/admin shapes → `auth-endpoint` / `admin-console`
   * interesting-but-unripe → `backlog=True` with a resume note
5. Targeted second walk only for signals that earned it: tech-specific
   wordlist (see `references/wordlists.md` ladder + the v2 composition law
   in `references/corpus-science.md`), extensions round (`.tar.gz`, `.sql`,
   `.example`), bounded by the same cap. A different base URL recalibrates
   first (v2 rule 4).
6. `dossier_add` each triaged finding citing the SURFACE record the tool
   emitted.
7. Exit gate: numbers stated — probes sent, calibration verdict, findings,
   backlog count. Every finding cites its record.

## 5. Hard Rules (mechanically enforced)

1. **Control requests first.** The tool refuses to walk before calibrating;
   the CONTROL records precede all FACT records of the walk in the ledger.
2. **GET-only.** No POST/PUT content discovery in this organ.
3. **Capped and courteous.** `max_requests` and `rate_per_s` defaults are
   the ceiling unless the operator explicitly raises them and the reason
   lands in the ledger note.
4. **Findings are deviations.** The SURFACE record carries the calibration
   numbers in its note — the auditor checks.
5. **Family discipline (v2).** A walk's wordlist source names its SecLists
   family (or the evidence that composed it) in the ledger note;
   authentication-surface lists never run in this organ.

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Calibrated walk | `content_discover` |
| Targeted artifact fetch (headers/body) | `http_probe` |
| Faster local walk when `ffuf` installed | `arsenal_route(program, "ffuf", base, "-w default.txt -mc all -ac")` — output still goes through triage as hypotheses |
| Registering findings | `dossier_add` (surface-cartographer) |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Choosing the ladder rung / tech-specific list | `references/wordlists.md` |
| Triage of a specific finding class | `references/patterns.md` |
| Composing a list beyond rung 0 / family & scope questions | `references/corpus-science.md` |
| Citing the lineage artifacts behind the v2 layer | `references/sources.md` |
| Grading the published practice, binding questions to classes, holding the marginal gate | `references/method-upgrade.md` |
| Running the hunt — the Daniel Miessler runtime: thinking rules, situation-to-action behavior, scripting, rigid run-order | references/operator-os.md |
