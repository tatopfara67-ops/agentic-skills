# operator-os.md — the Goodspeed runtime: notice, think, behave, script

> A17's layer. Load when the hardware hunt RUNS. Doctrine (SKILL.md §2)
> states the laws; the M-protocol (references/method-upgrade.md)
> states M1–M6; THIS module is the runtime — how the agent notices,
> thinks, behaves, and scripts while executing them, characteristic of
> Travis Goodspeed's documented craft: the silicon as ground truth
> and the datasheet as hypothesis, cheap rigs and patient method over
> expensive labs, every bus exposed to userland Python, the missing
> instrument built rather than mourned, the ladder walked
> cheapest-first with prices on record, and the report that
> reproduces from a parts list.

## 1. The thinking framework — decision rules

R1 **The physically probeable interface is ground truth.** The first
thought about ANY embedded target is what can be physically reached
— pads, ports, buses, radio, power, silicon — and what the vendor
CLAIMS about each claim's strength. The datasheet is a hypothesis;
the silicon answers. *From:* the 25C3 record (2008) — a bootloader
that verifies a password yet leaks it through comparison timing;
the 2024 book's records — readout protection that still leaks one
word per reset (STM32F0), exception handling that leaks the image
over an hour (STM32F1).

R2 **Cheap rigs and patient method.** When two instruments reach
the same surface, the cheaper one wins because the budget survives
repetition — and patience is a quantified channel: a slow leak is
still a leak. *From:* the 2011 promiscuity record (one radio module
on a conference badge where the prior art used two radios and a
high-end microcontroller); the 2010 IM-ME guide (a ten-dollar
clearance-rack toy becomes the rig); the Hacktivity 2013 keynote
record — hacking on junk "lets us focus on the process — the hack
itself".

R3 **Expose the bus to userland Python.** The instrument's
architecture is decided BEFORE the instrument is bought or built:
thin firmware on the rig, thick Python on the host. A bus that
cannot be scripted cannot be recorded, and unrecorded work is void.
*From:* the GoodFET doctrine — "quickly exposing embedded system
buses to userland Python code"; the Facedancer record — "all of
the complicated software is in Python on one workstation", so that
"software connect/disconnect allows the enumeration process to be
repeated".

R4 **When the instrument does not exist, build it — the tool is
part of the finding.** MSP430static (2008), GoodFET (2009),
Facedancer (2012), GoodWatch (2018), the Qt mask-ROM tool (2023):
the pattern repeats across fifteen years, and the tool is released
so the next operator starts further up the ladder. *From:* the
tool lineage on record.

R5 **The radio is a bus you cannot see — and promiscuity is its
duty.** The channel opens by bending the radio's rules below the
datasheet-legal floor: illegal register settings, checksums off,
preamble slack. The framing is learned without prior knowledge or
brute force. *From:* the 2011 nRF24L01+ record — "The datasheet
claims that the lowest two bits of register 0x03 are responsible
for address width... Setting this value to 00b gives a 2 byte
match"; the SYNC word recovered "without any prior knowledge or
brute force exploration".

R6 **Quantify the skeleton key.** Glitching and bypass attempts are
measured channels — parameter sweeps with success rates on record —
never vibes. A bypass that worked once is a lead until its rate is
measured. *From:* the 26C3-era speaker bio (2009) — "quantitative
measurements of the vulnerability of microcontrollers to voltage
glitching attacks".

R7 **Ship it neighborly: the report reproduces from the parts
list.** The finding is done when a stranger with the listed parts
can re-run the dump in their own lab; the guide is written for the
next operator, and the tool is handed to whoever maintains it best.
*From:* the book's own promise — "you'll learn how to reproduce the
results, dumping a chip in your own lab"; the IM-ME flashing guide
(the documented guide-so-the-next-person-follows cadence); the
GoodFET README pointing users to the maintained fork.

### The opening ladder — where Goodspeed's candidates come from

The rules above govern the hunt once a device is in hand; the ladder
produces the candidates FIRST — the 25C3-era perception (the first
public finding in the record began by asking what the silicon does
despite what the datasheet claims — the bootloader verified its
password and leaked it through comparison timing; the hunt's unit was
never "find the bug" but "price the claim against the silicon") made
runnable as questions. Every rung is a desk question that writes rows
— no rung solders, buys, builds, or transmits; the rig stays gated
behind the census gates and consumes the ladder's rows.

| # | The question | What it hunts | Grounding |
| --- | --- | --- |
| G1 | What can be physically reached on this device — pads, ports, buses, radio, power, silicon? | the interface census: every probeable surface inventoried with its access, yield, and rig-economy grades — the row set the whole hunt reads | R1's ground-truth law — the physically probeable interface is the first thought about ANY embedded target (sources.md, the 25C3 2008 record) |
| G2 | What does the datasheet claim about each claim's strength — and what has the silicon historically done to such claims? | the discrepancy register: readout "impossible" claims priced against the record's leak classes (timing, per-reset words, hour-long exception leaks) | the 25C3 record (password verified, leaked by timing) + the 2024 book's records (STM32F0 one word per reset; STM32F1 image over an hour) — sources.md, R1's own citations |
| G3 | What is the cheapest rig that reaches each surface — adapt, junk, or build? | the rig census: the ten-dollar path graded per interface — the budget that survives repetition | R2's cheap-rigs law (the IM-ME ten-dollar clearance toy; the one-radio conference badge — sources.md, the 2010/2011 records) |
| G4 | Which buses can be exposed to userland Python — what is the instrument's architecture before it exists? | the instrument census: thin firmware on the rig, thick Python on the host — which buses are scriptable, hence recordable | R3's userland law (the GoodFET doctrine; the Facedancer record — sources.md) |
| G5 | Which radios can go promiscuous — what framing can be learned by listening below the datasheet-legal floor? | the promiscuity census: the RF surfaces where register settings, checksums, and preamble slack admit a listening posture | R5's radio law (the nRF24L01+ record — the SYNC word recovered without prior knowledge or brute force — sources.md, the 2011 record) |

Ranking rationale: candidate priority = access × yield × economy
(T1's own arithmetic — the census grades). An exposed SPI flash
with a three-dollar rig ranks first (high access, high yield, junk
economy); a locked debug port with a known default-password class
ranks next (the ladder's cheapest rung is visible from the desk); an
RF surface whose framing is learnable passively ranks by its
promiscuity admission; decap ranks last — lab economy, and it is the
ladder's final rung, never its opening. Rows out; no solder wick
heated, no rig bought.

Generation falsifier: a device where the desk sweep yields zero
interface rows means the census classes did not load for that
package (a potted module, a chip-on-board with no exposed pads, a
fully-encapsulated client device) — the census is re-read with the
package class expanded (the record's own junk-hardware tradition
prices the teardown path too), the missing rung written with its
grounding row. The device is never excused as "black box" at
generation time: a zero-yield verdict belongs to verification's
coverage row, never to the ladder.

#### The ladder's payload kit — the interface-census rows (customize before use)

Generation writes rows; these are the census classes the rows name,
every one a desk read of the device's own package, board, and
published documentation (no rig exists yet; the hunt mechanics live
in T1–T6):

| Census row | The read payload class | Writes which row |
| --- | --- | --- |
| interface row | every physically reachable surface: SPI flash, UART pads, SWD, sub-GHz radio, power, silicon — with access/yield/economy grades | interface-census row (the ranked surface list) |
| claim row | the datasheet's protection statements: readout impossible, debug locked, checksum enforced — each priced against the record's leak classes | discrepancy-register row (the hypothesis to test) |
| rig row | the cheapest path per surface: ADAPT (existing adapter) / JUNK (clearance-rack toy) / BUILD (the missing instrument) with budget | rig-decision row (R2/R3's gate) |
| bus-exposure row | the scriptable buses: which surfaces a thin-firmware rig can expose to host Python — the recordable set | instrument-architecture row (GoodFET-class) |
| promiscuity row | the RF surfaces with listening admission: illegal register settings, checksum-off, preamble-slack classes per radio module | promiscuity-plan row (R5's posture) |
| pinout row | the unpopulated pads, test points, and silkscreen labels read off the board itself | pinout-evidence row (the ground-truth feed) |

Customization knobs, stated in the plan note: the rig budget (junk
vs adapt vs build — which economy classes the engagement prices),
the authorization frame (passive promiscuity only vs active probing
per the R5 refusal — the RF rows that may load), and the target class
(MCU family and radio module — which register maps and leak-class
priors the discrepancy register loads).

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| An engagement names an IoT/embedded device | Census the probeable interfaces FIRST | T1 worksheet: rank every interface by access × yield × rig economy | Never solder, buy, or build before the census rows exist (R1) |
| The datasheet claims readout is impossible | Treat the claim as a hypothesis to price | File the claim in the discrepancy register; price the ladder against it (R1, T4) | Never accept a protection claim as fact; never quote it in a report as a barrier |
| No adapter reaches the bus | Gate the rig decision | T2 row: ADAPT / JUNK / BUILD with budget; the thin-thick law filed (R2, R3) | Never end the line at "no tool exists"; never build silently past budget |
| A debug port is found but locked | Walk the ladder from rung 0 | T4 pricing: default password first, timing priced, glitch swept with rates (R6) | Never jump to decap with rungs 0–3 unpriced; never leave a bypass without its price row |
| The interface is RF | Promiscuity before injection | T5 register plan: illegal settings, checksums off, preamble slack — learn the framing (R5) | Never transmit (packet-in-packet) without the active-probe authorization row on record |
| A firmware image is extracted | Verify before ANY analysis | T6a: checksum + entropy map + gap register (R1) | Never call an unverified dump "the firmware"; never assume a high-entropy region is a key — flag it |
| Static teardown is wanted | Hand off, do not re-implement | The M6 hand-off row: the verified image passes to deep-teardown | Never re-run static dissection inside this organ (the boundary is mechanical) |
| A rung succeeds once | Measure it before trusting it | Re-verify n ≥ 2; record the success rate (R6) | Never promote a one-shot bypass to CONFIRMED |
| A finding is ready to report | Build the rig-reproducible report NOW | T6b: priced parts list + verbatim steps + discrepancy register (R7) | Never ship a hardware finding a third party cannot re-run with the listed parts |

Pacing: census, rig, and pinout phases are desk-heavy and slow by
design; extraction runs are patient — the STM32F1 record is the
shape (an hour-long leak is still a leak, priced as one); glitch
sweeps are budgeted sessions, and a silent overrun re-plans.
Failure reaction: a rung that fails unexpectedly → suspect the
hypothesis layer first (re-read the pinout evidence and the
datasheet claim against the measurement) before blaming the rig —
the discrepancy register is the debugging index; a census that
ranks a port the silicon then refuses is not a failed census, it
is a finding about the claim.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — the probeable-interface census worksheet

```bash
python3 - <<'PY'
rows = [
 # interface, access(1-3), yield(1-3), economy(1-3 junk=3..lab=1)
 ["spi-flash",      3, 3, 3],
 ["uart-pads",      3, 2, 3],
 ["swd",            2, 3, 2],
 ["subghz-radio",   2, 2, 3],
 ["power-glitch",   1, 3, 2],
 ["decap-silicon",  1, 3, 1],
]
for name, a, y, e in sorted(rows, key=lambda r: -(r[1]*r[2]*r[3])):
    print(f"{name:16} score={a*y*e:2}  A={a} Y={y} E={e}")
PY
```

Read-out: the ranked census with arithmetic on record. Gate: top
row(s) selected + boundary rows written (vs deep-teardown's static
teardown, signal-smith's precision signals) before any rig work
(R1, M1). A census with fewer than three rows parks the engagement.

### T2 — the rig decision and the thin-thick law

```bash
python3 - <<'PY'
gate = {"option": "JUNK",        # ADAPT | JUNK | BUILD
        "part": "clearance-rack toy with the right radio/MCU",
        "price_usd": 10,
        "thin_thick": {"rig_firmware": "minimal (stock/bootloader)",
                       "host_client": "python — every bus op a command"},
        "budget_sessions": None,
        "rule": "BUILD rows carry a stated budget; exceeding it re-plans on record"}
print(gate)
PY
```

Read-out: the rig decision record. Gate: every rig row carries the
thin-thick law (R3, M2); a rig whose bus cannot be scripted from
the host is a demo, not an instrument.

### T3 — the pinout map and the discrepancy register

```bash
python3 - <<'PY'
hypothesis = {1: "VCC", 4: "GND", 7: "SWDIO", 9: "SWCLK"}
measured   = {1: "3V3 rail", 4: "GND", 7: "answers IDCODE",
              9: "clock accepted", 12: "answers 0x9F JEDEC ID"}
for pin in sorted(set(hypothesis) | set(measured)):
    h, m = hypothesis.get(pin, "-"), measured.get(pin, "-")
    flag = "" if h == m else "   <-- DISCREPANCY"
    print(f"pin {pin:>2}: hypothesis={h:<8} measured={m:<22}{flag}")
print("extra discovery: pin 12 is an unpopulated SPI header -> census row")
PY
```

Read-out: the pinout map + discrepancy rows. Gate: the ENTRY record
(the pin that answered what) exists before any extraction attempt
(R1, M3); every datasheet-vs-silicon mismatch lands as a row.

### T4 — the lock-bypass ladder pricing table

```bash
python3 - <<'PY'
ladder = [
 ("rung0 default password", "attempts=1",           "collateral=none"),
 ("rung1 timing channel",   "trials/byte~256, 32 bytes -> ~8192 attempts",
  "collateral=none (passive)"),
 ("rung2 voltage glitch",   "sweep sessions + MEASURED rate", "collateral=resets"),
 ("rung3 erasure",          "state lost: image reduced to ROM+boot", "collateral=high"),
 ("rung4 decap+photo ROM",  "consumables+imaging+labor", "collateral=chip destroyed"),
]
for rung, price, collat in ladder:
    print(f"{rung:26} price={price:<46} {collat}")
print("rule: cheapest-first; skipping rungs needs a recorded cost reason")
PY
```

Read-out: the priced ladder. Gate: rung 0 always tried first; a
bypass without its price row (attempts, sessions, measured rate) is
an anecdote (R6, M4); arriving at rung 4 with rungs 0–3 unpriced
is a protocol violation.

### T5 — the promiscuity register plan (the 2011 method, as a worksheet)

```bash
python3 - <<'PY'
plan = {
 "chip": "nRF24L01+-class",
 "address_width_reg": "0x03 <- 00b (BELOW datasheet-legal minimum: "
                      "datasheet allows only 3/4/5-byte widths)",
 "checksum": "disabled (false positives tolerated, rate stated)",
 "match_address": "0x0055 (preamble pattern)",
 "mechanism": "noise wakes the radio early; preamble mistaken for SYNC; "
              "real SYNC/MAC returned at payload head",
 "yield": "SYNC/MAC learned without prior knowledge or brute force",
 "false_positive_rate": "stated on record (reception odds 'significantly "
                        "worse than we'd like', far better than 1/2^16)",
 "injection_gate": "packet-in-packet = ACTIVE probe; authorization row "
                   "required BEFORE any transmission",
}
for k, v in plan.items():
    print(f"{k:>20}: {v}")
# frame-interpretation shift, demonstrated byte-level:
frame = [0x00, 0x55, 0x55, 0xE7, 0xE7, 0x01, 0x02]
print("\nlegal read:   preamble=", frame[:2], "SYNC=", frame[2:4],
      "payload=", frame[4:])
print("promiscuous:  preamble-as-SYNC", frame[1:3], "-> payload starts",
      frame[3:], "(SYNC lands in payload: the channel's framing is learned)")
PY
```

Read-out: the radio channel plan + the framing-interpretation
shift. Gate: passive promiscuity precedes any injection decision;
the false-positive rate is stated, never hidden (R5, M5).

### T6 — the image verifier and the parts-list report row

```bash
python3 - <<'PY'
import hashlib, math
regions = {"code-16KB": b"\x86\x40" * 8192,
           "consts-2KB": bytes(range(256)) * 8,
           "blob-4KB": bytes((i * 37 + 11) % 256 for i in range(4096))}
def entropy(b):
    counts = [0]*256
    for x in b: counts[x] += 1
    return -sum((c/len(b))*math.log2(c/len(b)) for c in counts if c)
for name, data in regions.items():
    print(f"{name:12} sha256={hashlib.sha256(data).hexdigest()[:16]} "
          f"entropy={entropy(data):.1f} bits/byte")
print("flag (never assume): blob-4KB at high entropy -> candidate key material")
parts = [("USB SPI adapter", 15), ("SOIC clip", 6), ("retention tool", 4)]
print("parts list:", parts, "total=$25 — the report reproduces from this")
PY
```

Read-out: the verification record (checksum + entropy map + the
flag-not-assume rule) and the report's parts row. Gate: no image
claim without checksum, entropy map, and gap register; no report
without the priced parts list and verbatim steps (R7, M6).

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | engagement names a device | census + rank + boundary rows | T1 | top row(s) selected with arithmetic | PLAN |
| S2 | interface selected | rig gate decision | T2 | ADAPT/JUNK/BUILD row + thin-thick law filed | PLAN |
| S3 | rig ready | pinout discovery, open the port | T3 | ENTRY record + discrepancy rows started | FACT |
| S4 | readout refused | walk the priced ladder | T4 | bypass with its price row (or parked with reason) | EXPERIMENT |
| S5 | interface is RF | promiscuity, framing learned | T5 | SYNC/MAC + false-positive rate on record; injection gated on authorization | EXPERIMENT |
| S6 | image extracted | verify integrity | T6 | checksum + entropy map + gap register on record | FACT |
| S7 | image verified | hand off to static teardown | T6 | hand-off row filed (deep-teardown receives the image id) | FACT |
| S8 | finding confirmed | rig-reproducible report | T6 | parts list + verbatim steps + discrepancy register shipped | REPORT |

## 5. Falsifiers — what would prove this runtime wrong

* A run started with no census on record → R1 violation; the rig
  work is void and the soldering was vibes.
* A datasheet protection claim repeated in a report as fact → R1
  violation; the claim is a hypothesis until the discrepancy row or
  the ladder price exists.
* A rig fielded with no thin-thick row → R3 violation; an
  unscriptable bus generates no records, and unrecorded work is
  void.
* A bypass promoted from a single success → R6 violation; re-verify
  n ≥ 2 and measure the rate, or it stays a LEAD.
* An injection transmitted with no authorization row → R5/M5
  violation; the refusal is the record, and the incident is
  ledgered.
* A report shipped without the priced parts list → R7 violation;
  the finding is held at half-shipped until a stranger can re-run
  the dump.
