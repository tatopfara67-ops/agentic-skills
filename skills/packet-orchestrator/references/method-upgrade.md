# The method upgrade — critiquing the manual-craft lineages, shipping the executable packet discipline

The charter's A16 charge: **a lineage named is not expertise delivered.**
packet-orchestrator stands on three real lineages — Searle's
manual-to-structured teaching craft, the Mantis school of
state-backed orchestration, and Scapy's packet-crafting — but the
published forms have floors: manual craft shown as classroom
wizardry, orchestration demonstrated without state gates, Scapy
invoked without send discipline, and protocol dissection told as
single-shot demos. This module extracts what is protocol-shaped and
ships the replacement: a translation table, a send discipline, a
state-backed pipeline record, a dissection differential, and
orchestrator abort gates. An agent with no classroom seat must run
this at its precision.

## 1. The critique — five mechanical weaknesses of the published method

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | Manual craft as wizardry — Searle's teaching demos show an expert hand-driving Wireshark/scapy live; the INTENT→FIELDS translation is performed, not written | The craft lives in the demonstrator: two analysts translate "test the restart behavior" into different packets with no protocol to reconcile them (the recurring W3 floor, packet edition) |
| W2 | Orchestration without state gates — Mantis-style pipelines demonstrate stages and schedulers; the ABORT conditions are demo conveniences | A pipeline that cannot state, mechanically, when it stops is a liability with a scheduler: mid-run target state changes (service restarts, connection drops) must gate the next stage or the run lies |
| W3 | Scapy invoked raw — the classic pattern is `sr1(IP(...)/TCP(...))` in a loop with no rate, no count cap, no response classing | Craft without send discipline is a flood wearing a lab coat: the civility floor is not optional metadata, it is part of the method |
| W4 | Dissection as single-shot narration — "look at the handshake, see the odd FIN" | One capture, one observer, no expected-vs-observed differential: anomaly calls are taste, and taste does not survive an audit |
| W5 | Layered expectations implicit — the analyst "knows" what a compliant exchange looks like; the expectation is never written | Without a per-layer expectation table, "weird" is un-falsifiable: nobody can say what response would have been NORMAL, so nothing can be judged abnormal |

## 2. The upgrades — and where they land

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Intent→fields as a written translation table | **M1** — the translation table |
| U2 | Orchestration with mechanical abort gates | **M2** — the state gates |
| U3 | Send discipline as first-class method | **M3** — the send rule |
| U4 | Dissection as expected-vs-observed differential | **M4** — the dissection differential |
| U5 | Layer expectations written per probe family | **M4(a)** — the expectation table |

## 3. The executable protocol — M1 through M5

### M1 — the translation table (intent → fields)

Every manual-craft intent is translated through a written row BEFORE
any packet exists:

```
TRANSLATE: intent="restart-behavior under half-open sessions"
  fields: flags=S (seq randomized, window house-default)
  count=3 rate=1/2s response-classes=[RST|no-answer|SYN-ACK]
  artifact=<pcap slice + per-send record>
```

Rules: an intent with no response-classes cell is refused — you
cannot run a probe whose outcomes you have not enumerated (W1). The
row is the EXPERIMENT's pre-registration; the packets derive from
it, never the reverse.

### M2 — the state gates (orchestration that can stop)

```
PIPELINE: stages=[S1 baseline S2 treatment-family S3 verify]
  gate-1 (before S2): baseline class == expected-quiet, else HOLD
  gate-2 (per treatment batch): error-rate < 5% and no state-change
    token observed (service banner/uptime unchanged), else ABORT
  gate-3 (before S3): treatment response-class distribution recorded
  abort-actions: stop sends; drain in-flight; state re-baseline;
    resume only through gate-1
```

A stage entered without its gate's record is an audit failure — the
run is void from that stage on (W2).

### M3 — the send rule (Scapy discipline)

1. Every crafted-send loop carries: `count`, `rate` (default
   1 send / 2 s — the house floor), `timeout` per send (2 × measured
   RTT), and a per-send response CLASS not a raw dump.
2. **Burst ban**: never n > 1 in-flight on the same 5-tuple; stateful
   sequences (handshakes) are walked one step at a time with the
   observed reply driving the next field values — crafting a whole
   "conversation" blind and sending it is spray, not craft.
3. Every send is ledgered: `send-id, count-position, response-class,
   wall-time` — a pcap artifact without its send ledger is half an
   artifact (W3).

### M4 — the dissection differential (expectation vs observation)

**(a) Expectation table** per probe family — written before capture:

| Layer | Compliant expectation | Anomaly classes watched |
| ----- | --------------------- | ----------------------- |
| TCP | SYN→SYN-ACK/ACK exact flag sequence | RST mid-handshake; SYN-ACK with anomalous window (0 or ≥ 64k) |
| App (per protocol) | grammar-complete reply per RFC class | truncation; extra fields; re-ordered segments at reassembly |

**(b) Differential rule**: a claim of anomaly requires the SAME
exchange run n ≥ 3 with the anomaly class reproducing ≥ 2 of 3,
AND a compliant control exchange (the baseline probe from M2's S1)
observed in the same window — one weird capture is a story (W4, W5).

### M5 — the orchestrator record

```
ORCH-RECORD: pipeline=<id> gates=<fired/-held/aborted with times>
  sends=<count, per-stage> pcap-artifacts=<ids + hashes>
  verdicts=<per response-class table> resume=<ledger cursor>
```

The orchestrator exists to make the run re-runnable by a second
analyst from the record alone — the demo conveniences (schedulers,
alerting) are plumbing; the RECORD is the method.

## 4. Falsifiers — what would prove this method wrong

* Gate-2's state-change token fires but the service still answers
  normally → the token was under-inclusive (e.g. banner unchanged,
  config reloaded): add the observable, re-baseline, record the
  correction.
* The anomaly class fails the n ≥ 3 reproduction but the control
  ALSO shows it once → environment noise (middlebox): both captures
  are artifacts, verdict "unattributed", never "target anomaly".
* Two analysts translate the same intent into different field rows
  → the table lacks a row for this intent class: add both with
  their rationales, arbitrate by differential (run both, keep the
  one whose response-classes discriminate).
* A crafted stateful sequence desyncs (mid-conversation reset by
  the target) → the burst ban was violated upstream or the target
  is state-machine-defensive: check the send ledger FIRST (the
  method suspects itself before the target).

## 5. Worked micro-example (numbers consistent, incident fictional)

Intent "half-open session restart behavior" (M1 row: flags=S,
count 3, rate 1/2 s, response-classes enumerated). M3: sends at
1/2 s, timeout 44 ms (2 × RTT 22 ms); responses: 2 × RST, 1 ×
no-answer — classes recorded per send. M4: expectation table says
compliant = SYN-ACK; anomaly classes include RST-mid-handshake;
n = 3 runs → RST reproduces 3/3; control (full handshake to the
same port in-window) compliant 2/2 → anomaly CONFIRMED as class
"RST-on-SYN-from-second-source" (source-port pattern noted from
the ledger, not memory). ORCH-RECORD: gate-1 held (baseline quiet),
gate-2 never tripped (banner stable), 6 sends total, 2 pcap
artifacts hashed. Verdict table: RST 5/6, no-answer 1/6.
