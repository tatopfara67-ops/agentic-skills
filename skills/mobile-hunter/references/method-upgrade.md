# The executable method — M1–M5 for mobile-hunter

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The critique that
justifies each step (why these phases exist, what was weak in
Miller's and Mulliner's public research) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M5

### M1 — the device baseline inventory

Before any binary is opened, the target is pinned as FACT records:

```
BASELINE: device=<model> os=<exact build> carrier-config=<variant>
  signed-by=<cert chain class> entitlement-set=<observed>
  sources=<build fingerprint + how obtained>
```

1. Build fingerprint from the device (settings dump / OTA metadata /
  `uname` equivalent) — the exact build, never "iOS 9-ish".
2. Entitlement and code-signing posture observed, not assumed: which
  entitlements the target app class carries, which signature chain
  verifies it. (The Instastock lesson made data: signature CHECKS are
  a config surface, so the config is the FACT.)
3. Fleet variance table when the claim's scope is a fleet: firmware
  version distribution and config variance from public recall/release
  notes, recorded with sources — the W3 floor, bounded on record.
4. IPC/URL-scheme/surface census: every entry point class (custom URL
  schemes, IPC handlers, notification parsers, accessory protocols)
  listed as the attack-surface ledger — this feeds M2.

### M2 — harness discipline (coverage-gated, budgeted)

1. One harness per surface class from M1's census; each harness first
   PROVES reachability: a benign marker input whose full path through
   the parser is observable (log/coverage bit) before any mutation
   budget is spent. No reachability proof = no fuzz budget.
2. Coverage gate: mutation budget is released in slices tied to new
   coverage — if a slice of N executions adds zero new covered
   branches, the harness is re-seeded or retired ON RECORD (the W2
   floor made mechanical).
3. Budget table, per harness:

```
FUZZ-BUDGET: harness=<sms-parser-class> exec-rate=<Hz, device-safe>
  slice=<2,000 execs> coverage-new=<count> crash-buffer=<on>
  resume=<ledger id> — slice gate: +0 branches = retire/reseed
```

4. Crash buffer ON: every crash writes a full core/state artifact to
   the harness store; crashes are never triaged in-place.

### M3 — crash triage protocol (dedup before conclusions)

1. Every crash gets a stack signature: top-K frames (K = 5) +
   faulting access class + parser state hash → `sha256` of the tuple.
2. Cluster table: signature hash → count, first/last exec id,
   representative artifact. One signature = one candidate bug, no
   matter how many raw crashes carry it.
3. **Repro rule**: a candidate is a FINDING candidate only if the
   representative artifact reproduces under a clean rerun, n ≥ 5,
   with the same signature ≥ 4 of 5. Non-repro crashes park with the
   artifact and a resume note — "flaky" is a data point, not a
   discard (the W1 floor, applied downward).
4. Reachability of the crashing input from a REMOTE/attacker-reachable
   surface (M1 census) is the severity gate: a crash only reachable
   via local debug sockets is hygiene, not a bug bounty finding.

### M4 — the exploit differential (reliability as data)

Per exploit claim (one chain candidate):

1. **Conditions, n ≥ 10 runs**: clean-state setup per run (the
   precondition reset is part of the protocol), the chain fired, the
   outcome bucketed: full compromise / partial / crash-only / clean
   fail.
2. Reported: success rate with the bucket distribution and the exact
   precondition list that each successful run required. "90%" without
   conditions is a story, not a number.
3. The end-state proof is operator-owned: the marker (a file write /
   command output tagged with the EXPERIMENT id on the device)
   observed by the operator's own collection step — the demo theater
   retired (W5).
4. A run that succeeds only when the debugger is attached is recorded
   as bench-conditioned and the field claim is DOWNGRADED, not
   published as-is.

### M5 — the fleet-gap statement (mandatory in the pack)

```
SCOPE-FLOOR: proven on <exact build/config, M1 baseline>
  fleet-variance: <versions/configs known to differ, with sources>
  field-conditions: <carrier/network/head-unit prerequisites
  actually tested> — NONE CLAIMED BEYOND <tested set>
```

The Jeep-era gap made mechanical: what is proven is what was tested;
the fleet is arithmetic on the variance table with sources, stated
under the same rule as the adversary-tracker's localization floor —
never rounded up.

## 2. Falsifiers — what would prove this method wrong

* Two analysts' harness reachability proofs disagree → the surface
  census (M1) is incomplete or wrong: re-census before any fuzz
  result stands.
* A cluster's signature hash splits under clean reruns (same crash,
  two signatures) → K or the state hash is too coarse: re-derive with
  K = 8 and record the correction as a CONTROL.
* The exploit differential shows ≥ 50% clean-fail under field-class
  preconditions → the chain is a lab artifact: report as unreliable,
  or do not report as an exploit at all.
* Coverage stays flat while crash counts grow → harness is spraying
  already-covered inputs: retire it; the crash pile from a retired
  harness is still triaged (M3), because bugs found badly are still
  bugs.

## 3. Worked micro-example (numbers consistent, incident fictional)

Target: messaging app on a pinned OS build (M1: entitlement set + URL
scheme census, 4 surface classes). Harness on the attachment parser
class proves reachability with a marker input, then 6 slices of 2,000
execs: coverage +41/+9/+0 → slice 3 retires that seed. Crash pile: 63
raw crashes → 3 signature clusters → 2 reproduce 5/5 and 4/5; cluster
2 is reachable from the remote-message surface (severity gate: armed).
Exploit differential n = 10: 7 full / 2 crash-only / 1 clean fail,
preconditions = clean process state + attachment auto-fetch ON.
Fleet-gap: tested build 20F75, variance table from release notes
3 build configs — field claim capped to "the tested build class".
Marker: EXPERIMENT-tagged output file observed by operator collection.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
Charlie Miller and Collin Mulliner's art is real — the iOS Handbook,
Pwn2Own wins, the Instastock code-signing demo, the Jeep chain — but
it is told as exploit narrative: one-shot stories, dumb fuzzing,
expert-eye reversing. This module extracts what is tool-agnostic,
names the floors, and ships the replacement: a device-baseline
inventory, coverage-gated harness discipline, a crash triage protocol,
reliability differentials for exploit claims, and a bench-vs-field
floor statement. An agent with no IDA seat and no trophy must run this
at their precision.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the published method (context, not steps)

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | One-shot exploit narratives — Pwn2Own writeups and the Jeep account tell the winning path after the fact, without rerun counts, failure rates, or the branches that died | Reliability is the difference between a demo and a weapon, and it is exactly what the narrative omits; Miller himself publicly noted live-demo flakiness — the method never recorded it as data |
| W2 | Dumb mutational fuzzing — the SMS/MMS era fuzzed by brute mutation without coverage feedback; crash triage by eyes | Budget burns on inputs that never reach new code; crash piles dedup by nothing — one real bug reads as fifty, or fifty read as one |
| W3 | Bench-to-field gap unmeasured — the Jeep exploit tuned on one bench vehicle; fleet variance (firmware versions, carrier configs, head units) stayed unquantified | The claim's scope is the fleet; the evidence is one VIN. Nothing in the method states or bounds that gap |
| W4 | Reversing as expert narration — the Handbook era's method lives in IDA seats and pattern recognition, not in scripted, re-runnable harnesses | The method lives in the man: two analysts on the same binary produce different maps with no protocol to reconcile them (the same floor as adversary-tracker's W3) |
| W5 | Demo theater as proof — code-signing shown by an app that should not run; the demo IS the evidence | No canary/marker doctrine, no operator-owned observable: the proof cannot be re-checked, only admired |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | The target fingerprinted as DATA before any work | **M1** — the device baseline inventory |
| U2 | Fuzzing gated on coverage, budgeted by table | **M2** — harness discipline |
| U3 | Crash triage as a dedup protocol, not eyes | **M3** — signature-hash clustering |
| U4 | Reliability measured, reported with conditions | **M4** — the exploit differential |
| U5 | The bench-vs-field floor stated in the pack | **M5** — the fleet-gap statement |
