---
name: injection-lab
version: 1.3.0
type: ai-skill
architecture: package
description: Phase-3 injection organ — differential oracles only: every injection class (SQL/NoSQL/command/template/LDAP) tested as baseline vs treatment vs control with a stated falsifier; timing oracles honor repetition floors; sqlmap runs only as a differential oracle via governed routing. Since v1.3.0 the organ carries the executable method layer (A16) — a mechanical critique of the scan-first tradition's floors (battery before oracle census, boolean pairs read by eyes, timing without jitter baselines, error signatures as lore, unbudgeted extraction) shipped as protocol M1–M5: the oracle census, the parity differential with reversed passes, the jitter-gated timing oracle, the extraction budget table with shown arithmetic, and the operator-owned out-of-band collector rule. Use when the operator asks to test SQLi or NoSQLi, command or template injection, build a boolean/error/timing/out-of-band oracle, or run sqlmap within discipline ("tes SQLi", "injection", "blind boolean", "time-based", "template injection", "SSTI", "command injection", "differential oracle").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# injection-lab v1.3.0 — Oracles, Not Payload Sprays

## 0. What This Skill Is — and Is Not

* **Is**: the Phase-3 organ that proves or refutes injection hypotheses
  with differentials: an oracle is a measurement channel whose delta only
  the postulated mechanism can explain, and whose control request kills
  every rival explanation.
* **Is not**: a payload list with ambition. Payload dictionaries without
  a pre-registered mechanism are noise generators that burn scope goodwill.

## 1. Inherited Contracts

Plugs into **Phase 3** of the mythos-bug-hunter spine. Inherits the
hypothesis grammar (§5 — mechanism, prior, falsifier BEFORE the payload),
experiment contract (§6 — baseline/treatment/control/n_runs/delta),
reproduction floors (deterministic: 3 identical deltas; timing: repetition
until stable, never single-shot), closure vocabulary (§7), and canary
doctrine (§8 — extraction proofs use self-injected markers, bounded).

## 2. Oracle Classes

The full catalog — boolean, error-signature, timing, out-of-band, and
per-injection-class grammar — is in `references/oracles.md`. Summary:

| Oracle | Channel | Falsifier shape |
| --- | --- | --- |
| Boolean differential | response differs ONLY on truth-value of the injected expression | control expression flips the delta away |
| Error signature | specific error family appears only for the injected syntax | malformed-but-non-injected input produces generic errors |
| Timing | delay correlates with injected arithmetic | equivalent non-injected delay absent; clock-skew control request run interleaved |
| Out-of-band | self-owned interaction host receives a canary callback | no callback for the control payload |

## 2.5 First Principles — the WWH registers (A14)

* **WHAT** — an interpreter sits behind an input: SQL, NoSQL,
  LDAP, XPath, OS command, template engines (SSTI), expression
  languages. The class is unified by shape, not by syntax: user data
  crosses into a language the backend will EXECUTE.
* **WHY** — code and data share one channel: whenever the app
  builds program text by concatenation/interpolation, the interpreter
  cannot tell the developer's text from the attacker's — that is the
  root cause, and every flavor (quote break, comment swallows,
  stacked queries, directive injection in templates) is a dialect of
  it. Prepared statements fix it by separating the channels; their
  absence anywhere is the seam.
* **HOW** — differential oracles (§2): each payload is designed to
  flip ONE observable — a boolean, an error grammar, a timing delta,
  an out-of-band callback — against its benign-twin control. The
  oracle decides, the payload only asks; spray without a registered
  oracle is not this organ's method.

War note (A15): the cheng sweep is the catalog's oracles per
interpreter in scope; the ch'i is the oracle only THIS target's error
grammar or timing profile exposes. W2 binds absolutely — a
destructive payload proves nothing a differential could not, and
time-based oracles are the last resort because they are the noisiest
march.

## 2.6 The Method Layer — Critique, Upgrade, M1–M5 (A16)

A lineage named is not expertise delivered — and a tradition inherited
is no better. `references/method-upgrade.md` grades the scan-first
tradition this organ was forged against — payload batteries before
oracle census, one true/false pair read by eyes, SLEEP(5) once on an
unmeasured host, error signatures as lore, dump-the-table reflex at
scanner rates — and ships the executable replacement: **M1** the
oracle census (channel set per parameter, ON RECORD; empty channel =
closed, no battery fired), **M2** the parity differential (n ≥ 10
interleaved pairs + reversed pass + re-issue jitter check), **M3**
the jitter-gated timing oracle (baseline IQR FIRST; threshold
max(3 × IQR, 2 s); interleaved never five sleeps in a row), **M4**
the extraction budget table (rows × ceil(log2 charset) arithmetic
shown, abort-on-5xx-streak, resumable cursor), **M5** the out-of-band
canary rule (operator-owned collector, out-of-scope, unique label per
EXPERIMENT — a callback proves the CHANNEL, never the impact).

## 3. Procedure — Numbered Actions

1. Entry: hypotheses already pre-registered from Phase 2 (surface +
   parameter + suspected sink). Injection work without a pre-registered
   mechanism is refused here, not merely discouraged.
2. Build the baseline: the parameter's happy-path request, recorded.
3. Choose the WEAKEST oracle that can close the hypothesis (error before
   boolean before timing before out-of-band — weakest channel first
   keeps request counts low and evidence strong).
4. Craft treatment + control per `references/oracles.md`; record the
   falsifier in the hypothesis BEFORE sending.
5. Run the differential; measure the delta; repeat to the floor.
6. Timing oracles: interleave a clock-skew control (identical request,
   no injected delay) and subtract observed baseline latency; report the
   delta with its spread, never a single lucky slow response.
7. `sqlmap` — only as a differential oracle through
   `arsenal_route(program, "sqlmap", url, "--batch --risk=1 --level=1
   --technique=BE")`: banner/version confirmation is its ceiling here.
   Dump modes are flag-blacklisted in the router itself; the spine's
   doctrine (scanner output is a hypothesis) applies to its output too.
8. Extraction (Phase 4, only after CONFIRMED): bounded, canary-first —
   extract the self-injected marker (e.g. a known string via
   string-concat functions) before ANY schema curiosity, one bounded step,
   then stop and synthesize.
9. Exit gate: every hypothesis closed with its oracle class, floor, delta,
   and control cited; no closure without its control record.

## 4. Hard Rules (mechanically enforced)

1. **Falsifier precedes payload.** Ledger order is auditable.
2. **Control mandatory.** The auditor counts control records per
   experiment card; their absence fails the report.
3. **Floors honored.** Timing closures without repetition data fail.
4. **sqlmap is an oracle, not a harvester.** The router's flag blacklist
   is the enforcement; there is no override flag.
5. **Bounded extraction.** One canary-marker extraction before any
   database content; reports that narrate unbounded dumps fail the audit
   and the ethics gate simultaneously.

## 5. Tool Routing

| When | Tool |
| --- | --- |
| All manual differentials | `http_probe` (EXPERIMENT/CONTROL tags) |
| Governed sqlmap oracle | `arsenal_route` |
| Out-of-band canary host | operator-provided interaction host; callbacks observed by the operator, recorded as CANARY records |
| Recording hypotheses/closures | `ledger_append` |

## 6. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Choosing/crafting an oracle for a class | `references/oracles.md` |
| Exact oracle payloads per backend (boolean/UNION/time/error, comment grammar), per-technique failure modes, primary sources | `references/corpus.json` (versioned payload corpus) |
| Grading the scan-first tradition, running the census and parity gate, budgeting extraction | `references/method-upgrade.md` |

The corpus is versioned (`corpus_version`) and every entry carries its
primary source and its **failure modes** — read them before closing any
hypothesis as negative: an oracle that failed for a documented reason
(result caching, statement timeouts, stacked-queries disabled) leaves
the sink untested, not clean.
