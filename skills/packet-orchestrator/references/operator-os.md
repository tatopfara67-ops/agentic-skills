# operator-os.md — the Searle + Scapy runtime: notice, think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> orchestration laws; the M-protocol (references/method-upgrade.md)
> states the translation and state-gate protocol; THIS module is the
> runtime — how the agent notices, thinks, behaves, and scripts while
> executing them, characteristic of Justin Searle's documented craft (manual
> first, then layer-by-layer automation, ICS discipline) on the Scapy
> packet-crafting lineage (Philippe Biondi): one packet, read the
> answer, then the next — bursts are the enemy of attribution.

## 1. The thinking framework — decision rules

R1 **Manual before automated — one packet at a time first.** A new
protocol conversation starts as single hand-crafted packets, each
observed, until the exchange is understood; only then does it become a
scripted layer. *From:* the lineage's ICS tradecraft — on fragile
control protocols, automation is earned, never assumed.

R2 **Every send has an expectation.** A packet leaves only with a
pre-registered expectation (reply class, timeout, or silence-means-X);
the dissection differential compares expected vs observed.

R3 **State is a first-class variable.** Sequenced protocols (TCP,
modbus unit ids, session tokens) carry a state table; every packet
cites the state it assumes and the state it leaves.

R4 **Bytes shown, bytes cited.** The evidence artifact is the hex of
what went out and what came back — layered dissection explains it, it
never replaces it.

R5 **Bursts destroy attribution.** N packets in flight means N unknowns
per observation; the send rule keeps one outstanding conversation per
target (the M-protocol's burst ban).

R6 **Fragile targets get read-only grammar.** On ICS/SCADA surfaces,
the legal read set is enumerated and everything else is out of bounds
by default — writing to a PLC is a different engagement class entirely.

### The opening ladder — where Searle's candidates come from

The rules above govern posture once a candidate exists. The ladder
produces the candidates — the documented perception (the NESCOR
sequence begins at the capture, not at the send: manual dissection,
entropy analysis, reverse-engineering, and only then fuzzing) made
runnable as questions. Every rung reads what already exists —
captures, banners, vendor protocol documents, the resolver's answer
— NO rung sends a packet. Crafting is T1's job, and T1 fires one
packet at a time with its expectation row (R1, R2). Rows out; one
conversation per target, untouched.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | What does the wire already say about this protocol? | existing captures and banners — operator-grown lab captures, vendor PCAP samples, protocol documents — dissected before any conversation is proposed | the NESCOR sequence (the lineage's documented training basis): the capture precedes everything; manual dissection is step one |
| G2 | Where does the medium differ from the protocol? | the same protocol spoken over a different medium — serial, RF, TCP, UDP — where framing, timing, or checksums change behavior | the documented "network mediums vs network protocols" distinction (BlackHat training page) |
| G3 | Which bytes carry entropy the protocol does not explain? | fields with encrypted-looking content in a plaintext conversation; constant fields that suddenly vary run-to-run | the entropy-analysis step of the documented sequence, read as a generative question |
| G4 | Where will the implementation disagree with its own spec? | spec-vs-observed divergences: lengths that lie, state transitions the spec forbids but the wire shows, silently ignored fields | the organ's own operationalization of the expectation-table discipline (R2), labeled on the sources ledger |
| G5 | What did the parser never get taught to refuse? | error paths: unknown opcodes, malformed length fields, truncated trailers — the conversation candidates fuzzing will later prove | the RE-before-fuzzing step (documented sequence), expressed as a census question |

Ranking rationale: candidates rank by observability distance ×
fragility class. What a passive capture already demonstrates
outranks what must be probed to be seen; a medium-boundary
divergence outranks a spec typo (it survives implementation review
because nobody tests the other medium); on ICS-class targets the
read-only grammar (R6) gates the whole order — a candidate that can
only be proven with a write-class opcode parks at the bottom with
its refusal row. The sequence's order is the ranking: capture, then
medium, then entropy, then spec, then parser — each rung is cheaper
than the probes the next one justifies.

Generation falsifier: a protocol target with captures in hand where
the ladder yields zero conversation candidates means the ladder is
missing a rung — the capture is re-read for the layer it cannot see
(a trailer, a keepalive cadence, a retransmission shape), and the
new rung is written with its grounding row. The protocol is never
excused as boring; that verdict belongs to verification, not
generation.

#### The ladder's payload kit — one-packet craft templates (customize before use)

Generation writes rows; these templates are the craft the rows name,
pre-registered for T1's single-send verification — the ladder itself
never sends them. Kit rows are the organ's own operationalization of
the exact-bytes law (R4) on the credited Scapy lineage; no Scapy
feature is claimed as consulted evidence (the sources ledger's
boundary):

| Template | Craft shape | Writes which row |
| --- | --- | --- |
| The banner invitation | SYN to the service port, expectation row stating reply class + timeout + silence-means-X | conversation candidate + expectation row |
| The lying length | a captured request replayed with the declared length field +1 / −1 | parser-boundary candidate |
| The unknown opcode | a well-formed frame carrying a function code absent from the dissected grammar | error-path candidate |
| The entropy mutant | a captured constant field mutated once, all else byte-identical | implementation-divergence candidate |

Customization knobs, stated in the plan note before any send: the
protocol profile (dissected grammar + opcode namespace, from the
capture), the medium profile (the transport the capture actually
shows), and the expectation table (reply class, timeout,
silence semantics per R2). On ICS-class surfaces the read-only
grammar gate (R6) is a fourth knob that cannot be turned off — a
write-class template is recorded as refused, never staged.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| New protocol target | Craft ONE packet, observe, repeat | T1 single send + expectation; dissect; iterate | Never open with a scripted conversation |
| The exchange is understood | Translate it into a scripted layer | T2 records the translation table (manual step → automated step) | Never automate what was never understood |
| A reply surprises you | Stop and re-read | Expectation mismatch recorded; dissection updated | Never "retry harder" past a surprise |
| Sequenced conversation needed | Track state explicitly | T3 state row per packet (assumes/leaves) | Never let implicit state creep in |
| Protocol is ICS/fragile | Read-only grammar gate | T4 enumerates the legal read set; writes refused | Never send a write/function-class opcode to a control device |
| A scan would be "faster" | Stay in the send rule | One outstanding conversation; queue the rest | Never trade attribution for speed (R5) |
| Evidence time | Show the hex | T5 dumps bytes + dissection side by side | Never report dissection without the bytes |

Pacing: one conversation per target; think-time between sends is the
method, not latency. Failure reaction: a timeout is an OBSERVATION
(silence-means-X) — recorded, not retried blindly.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — single packet with expectation

```bash
python3 - <<'PY'
from scapy.all import IP, TCP, sr1, conf
conf.verb = 0
expectation = {"reply_class": "SYN-ACK", "timeout_s": 2.0}
resp = sr1(IP(dst="<host>")/TCP(dport=502, flags="S"), timeout=2)
observed = "SYN-ACK" if resp and resp.haslayer(TCP) and resp[TCP].flags == 0x12 else \
           ("RST" if resp else "silence")
print(f"expected={expectation['reply_class']} observed={observed}")
PY
```

Read-out: expected vs observed per send. Gate: no packet leaves
without its expectation row (R2).

### T2 — manual-to-automated translation table

```bash
python3 - <<'PY'
translation = [
 # manual step, understood-exchange evidence, automated form
 ["single modbus read, observed", "3 packets ledgered", "read_unit(id,addr)"],
 ["single banner grab, observed", "2 packets ledgered", "grab_banner()"],
]
for m, ev, a in translation:
    print(f"{m:32} evidence={ev:22} automates_as={a}")
PY
```

Read-out: which manual steps earned automation. Gate: an automated
form with no understood-exchange evidence is refused (R1).

### T3 — state row per packet

```bash
python3 - <<'PY'
state = {"tcp": {"seq": 100, "ack": 0, "phase": "SYN_SENT"}}
def on_synack(pkt):
    state["tcp"] = {"seq": state["tcp"]["seq"], "ack": pkt.seq + 1, "phase": "ESTABLISHED"}
print("assumes:", state, "-> leaves:", "ESTABLISHED after SYN-ACK")
PY
```

Read-out: assumes/leaves per conversation step. Gate: sequenced sends
without state rows are refused (R3).

### T4 — read-only grammar gate (ICS)

```bash
python3 - <<'PY'
legal_reads = {0x01: "read_coils", 0x02: "read_discrete_inputs",
               0x03: "read_holding_registers", 0x04: "read_input_registers"}
proposed = 0x05   # write_single_coil
verdict = "REFUSED (write class)" if proposed not in legal_reads else legal_reads[proposed]
print(f"opcode=0x{proposed:02x} -> {verdict}")
PY
```

Read-out: the grammar verdict. Gate: write-class opcodes never run on
ICS surfaces without an explicit engagement class change (R6).

### T5 — bytes + dissection evidence dump

```bash
python3 - <<'PY'
from scapy.all import IP, TCP, raw
pkt = IP(dst="<host>")/TCP(dport=443, flags="S")
b = raw(pkt)
print("hex  :", b.hex())
print("layers:", "IP > TCP [SYN] seq=0")
PY
```

Read-out: the hex artifact beside its dissection. Gate: findings cite
both (R4) — dissection-only claims are refused.

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | protocol target authorized | craft single packets with expectations | T1 | exchange understood + ledgered | EXPERIMENT |
| S2 | exchange understood | write the translation table | T2 | each automated form has evidence | FACT |
| S3 | automation justified | run scripted layers with state rows | T3 | every send cites assumes/leaves | EXPERIMENT |
| S4 | ICS/fragile class detected | apply the read-only grammar gate | T4 | writes refused + recorded | FACT |
| S5 | conversation complete | dump bytes + dissection artifacts | T5 | evidence pairs archived | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* An automated send with no manual-exchange evidence row → R1
  violation; automation rolled back to single-packet mode.
* A packet sent with no expectation row → R2 violation; the
  observation is unattributable and void.
* More than one outstanding conversation per target in the log → R5
  violation; the burst ban is the audit's bright line.
* A write-class opcode sent to an ICS device → R6 violation;
  engagement halts, incident recorded.
