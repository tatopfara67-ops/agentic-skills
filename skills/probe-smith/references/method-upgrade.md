# The executable method — M1–M6 for probe-smith

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The critique that
justifies each step (why these phases exist, what was weak in the
published Goodspeed art) is preserved verbatim as the §4–§5
appendix.

## 1. The executable protocol — M1 through M6

### M1 — the probeable-interface census

Before any rig exists, one census row per physical way into the
device:

```
CENSUS: device=<name+rev> chip=<marking+package>
  interface=<JTAG|SWD|BSL|UART|proprietary-debug|SPI|I2C|CAN|
  1-Wire|subGHz-radio|2.4G-radio|BLE|power|clock|silicon>
  access=<exposed-pads|test-pads|hidden-under-shield|requires-decap>
  yield=<full-image|partial-image|bus-traffic|execution|nothing>
  rig_economy=<junk-class|adapter-class|lab-class>
  rank_score=<access_weight x yield_weight x economy_weight>
  boundary=<vs deep-teardown / signal-smith, one sentence each>
```

Scoring weights are pre-registered per engagement (defaults:
access 1–3, yield 1–3, economy 1–3 where junk-class scores 3 and
lab-class scores 1; rank = product, max 27). The boundary rows are
mandatory:

* vs **deep-teardown**: this organ ACQUIRES the artifact from
  silicon when the vendor refuses to hand it over; once a verified
  image exists, static dissection is deep-teardown's protocol (the
  hand-off is M6's recorded gate).
* vs **signal-smith**: this organ opens the PHY layer — the
  channel itself (promiscuous mode, raw frame injection at the
  physical layer); forging precision application-layer variations
  against validators is signal-smith's protocol.

Gate: top-ranked interface(s) selected with the arithmetic on
record; a census with fewer than three rows parks the engagement
as a datasheet reading (a census of one port is not a census).

### M2 — the rig decision and the missing-instrument gate

For the selected interface, the rig decision is a recorded gate:

| Option | When | Record |
| --- | --- | --- |
| ADAPT | an existing adapter reaches the bus (OpenOCD-class, GoodFET-class, Bus-Pirate-class, USB-SPI-class) | adapter model + supported protocol + price |
| JUNK | the cheapest SHIPPING hardware carries the interface (the IM-ME rule: a ten-dollar toy with the right radio or MCU) | the junk part + what it carries + price |
| BUILD | no instrument exists that reaches the surface (the GoodFET rule) | the missing-instrument row: what does not exist, the build budget in sessions |

The architecture law rides every option, as a mandatory row:
`THIN-THICK: firmware=<minimal rig-side code> host=<python client>`
— thin firmware on the rig, thick Python on the host. A rig whose
bus operations cannot be scripted from the host is a demo, not an
instrument (the GoodFET doctrine: "quickly exposing embedded
system buses to userland Python code").

Gate: the BUILD option carries its budget; weeks are the budget,
not a blocker — a build exceeding its stated budget re-plans on
record rather than silently overruns. The rig budget is a stated
number BEFORE purchase or build (junk-hacking economics is a
decision gate, not a vibe).

### M3 — port discovery and entry (the datasheet is a hypothesis)

1. Identify the chip: package marking, date code, vendor family;
   open the datasheet — every claim in it is filed as HYPOTHESIS,
   never as fact.
2. Census the test pads and connector pins; note the shielded or
   unpopulated positions too (an unpopulated header is a row).
3. Pinout identification: continuity to ground/power rails, voltage
   levels under power, response probing (the pin that answers an
   IDCODE or a bootloader sync is the port).
4. Open the channel: JTAG/SWD IDCODE read, BSL handshake, UART
   autobaud — the first successful read is pinned as the ENTRY
   record.
5. The discrepancy register begins here and rides the whole hunt:

```
DISCREPANCY: claim=<datasheet/vendor statement, quoted>
  measurement=<what the silicon did> artifact=<record id>
  consequence=<what the claim hid>
```

Gate: the ENTRY record exists before any extraction attempt; a
channel "opened" with no record of which pin answered what is a
lead, not an entry.

### M4 — the lock-bypass ladder (each rung priced)

Readout protection met → the ladder, cheapest rung first, each
rung a recorded decision row:

| Rung | Technique | Price to record | Collateral |
| --- | --- | --- | --- |
| 0 | default/blank password (0xFF or vendor default) | attempts made | none — always tried first |
| 1 | credential/timing side channel on the password check | intercept attempts + trials per byte (arithmetic on record) | none if passive |
| 2 | voltage glitching to skip the check | parameter sweep sessions + MEASURED success rate (glitches tried vs bypasses achieved) | resets; possible lockout counters |
| 3 | unconventional erasure of the protection state (the camera-flash MSP430 shape: erase the state, re-enter with defaults) | erasure setup + what state is lost | the protected image may be reduced to mask ROM + boot ROM |
| 4 | decap + photographic mask-ROM extraction (the REcon 2023 method: photographs converted to bits when the debug protocol is undocumented) | consumables + imaging + bit-marking labor | the chip is destroyed |

Gate: skipping rungs requires a recorded cost reason; arriving at
rung 4 with rungs 0–3 unpriced is a protocol violation. Every
bypass lands with its price row. Success rates are measured, never
vibed (the 26C3-era bio's own standard: "quantitative measurements
of the vulnerability of microcontrollers to voltage glitching
attacks").

### M5 — the radio channel (promiscuity before injection)

When the census's top interface is RF, the channel opens with the
promiscuity method (the 2011 nRF24L01+ record, made mechanical):

1. Register plan: reduce the address width BELOW the
   datasheet-legal minimum (illegal register settings), disable
   checksums, set the match address to the preamble pattern
   (0x0055-class).
2. The preamble-slack trick: background noise wakes the radio
   early; the preamble is mistaken for the SYNC word, and the real
   SYNC/MAC lands at the head of the payload — the channel's
   framing is learned "without any prior knowledge or brute force
   exploration".
3. Record the learned SYNC/MAC, the observed packet rate, and the
   false-positive rate (stated, not hidden — the 2011 record's own
   honesty: reception odds "significantly worse than we'd like",
   but far better than 1/2^16).
4. Injection decision gate: packet-in-packet raw frame injection
   (a valid frame delivered inside a weaker received frame) is an
   ACTIVE probe — the engagement letter's authorization and the
   house conduct rules are cited on record BEFORE any transmission.

Gate: passive promiscuity precedes any injection decision; an
injection attempted without the authorization row is refused, and
the refusal is the record.

### M6 — extraction verification and the rig-reproducible report

1. Image integrity: checksum on record; entropy map over the
   datasheet memory map — code regions, data regions, constant
   tables, and any anomalous high-entropy region flagged as
   candidate crypto material (flagged, never assumed).
2. The gap register: which documented memory regions are MISSING
   from the dump, each with a reason (locked region not bypassed;
   external flash not censused; OTP unreadable) — an incomplete
   dump with no gap register is a false "full extraction".
3. The hand-off row: the verified image passes to deep-teardown's
   static protocol; the boundary is mechanical, not polite.
4. The report ships rig-reproducible: the parts list (priced), the
   steps a third party runs verbatim, the discrepancy register, the
   ladder price rows, and the gap register. The book's own standard
   is the gate: the reader must be able to reproduce the dump "in
   your own lab".

## 2. Falsifiers — what would prove this method wrong

* A census row without its rank arithmetic → the selection was
  vibes; re-rank on record before any rig work stands.
* A bypass without its price row (attempts, sessions, success
  rate) → the rung was skipped in spirit; the ladder is void back
  to the last priced rung.
* An image verified by "it looks like code" instead of checksum +
  entropy map + gap register → the extraction claim is unproven;
  re-verify or downgrade to PARTIAL on record.
* A rig-reproducible report whose parts list is incomplete or
  unpriced → the finding is half-shipped; a third party must be
  able to re-run the dump with the listed parts.
* A radio channel claimed "unsniffable" with only the
  datasheet-legal register settings tried → the promiscuity method
  was not attempted; the channel claim is untested until the
  illegal-settings plan is on record.
* A run started with no thin-firmware/thick-Python row → the rig
  is a demo; bus operations that cannot be scripted from the host
  generate no ledger records, and unrecorded work is void.

## 3. Worked micro-example (numbers consistent, scenario illustrative)

Census (5 rows) for an in-scope smart-lock controller board:
external SPI flash (access 3, yield 3, economy 3 → 27); UART test
pads (3/2/3 → 18); SWD (2/3/2 → 12); sub-GHz radio (2/2/3 → 12);
power glitch (1/3/2 → 6); decap (1/3/1 → 3). Top rank: the
external flash — read the whole image with a junk-class adapter
before touching the MCU. (The MCU's own debug port stays in the
census as the rung-1 target if the flash holds a locked
bootstrap.)

Rig: ADAPT — a 15-dollar USB SPI adapter + clip, host-side
Python; THIN-THICK row filed (firmware: none on the adapter beyond
stock; host: the read/verify client). Entry: JEDEC ID 0x9F answers
on the pads — ENTRY record pinned; no datasheet discrepancy yet.

Ladder: the flash dumps clean, but the MCU's BSL region is
readout-locked → rung 0 default password fails (attempts: 1);
rung 1 timing channel priced: 32-byte password, byte-wise recovery
at ~256 trials per byte → ~8,192 attempts, 41 minutes of
automated trials, password recovered, arithmetic on record; rungs
2–4 unneeded, prices not incurred.

Verification: 128 KB image; checksum pinned; entropy map — code
6.2 bits/byte, constants 4.1, one 4 KB region at 7.9 (flagged
candidate key material); gap register: none (flash map fully
covered). Hand-off row to deep-teardown filed with the image id.

Report: parts list (adapter + clip + clip retention tool, priced);
steps verbatim (attach → 0x9F → full read → verify); discrepancy
register: datasheet claims "BSL password verification cannot be
bypassed" vs measured byte-wise timing leak (consequence: the
claim hid the timing channel); ladder price rows (rung 0: 1
attempt; rung 1: 8,192 trials / 41 minutes). A third party with
the parts list re-runs the dump — the book's own standard, met.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise
delivered.** The published Goodspeed art is real — fifteen years
of reproducible public work, tools released open-source, a
408-page consolidating book — but it is lived as craft and
narrated per-chip. This module extracts what is protocol-shaped,
names the mechanical weaknesses, and ships the replacement: a
census rule for the interface instinct, a rig economics table for
the junk-hacking aesthetic, a priced lock-bypass ladder for the
per-target bypass demonstrations, one protocol for the scattered
method, and a design law for the thin-firmware/thick-Python
architecture. An agent that has never held a soldering iron must
run this at the lineage's precision.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the published method (context, not steps)

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | Interface selection by instinct — "look for JTAG", the CC2430/EM2xx choices in the 2009 bio, the IM-ME chosen by walking a clearance rack | The instinct is real but unstated as a rule: an agent inherits the stories, not the selection logic; "probe the UART" is a biography, access × yield × rig economy is a census |
| W2 | The rig economics lived as an aesthetic — "junk hacking" keynoted (Hacktivity 2013), the hillbilly persona, "Real Men Carry Pink Pagers" | Cheap is a value statement, not a decision gate; without a budget table and a junk-class option in the rig decision, "cheap" cannot be executed or audited — it can only be admired |
| W3 | The lock-bypass escalation demonstrated per-target — BSL timing (2008), voltage glitching (2009), the camera-flash MSP430 (the 2024 book), decap and photographic mask ROM (2023–2024) | Each demonstration is correct and public, but scattered across sixteen years and venues; the LADDER (default → timing → glitch → erasure → decap, each priced with yield, collateral, cost) was never written down as one table by the lineage itself |
| W4 | The method is scattered — a blog (2008–2013), 25+ talks across DEF CON, CCC, REcon, ShmooCon, ToorCon, HOPE, TROOPERS, Summercon, Hacktivity, five PoC||GTFO essays, and a 408-page book organized per-chip | The book is the closest to consolidation and it organizes by TARGET, not by PROCEDURE; what repeats across everything (census → rig → port → ladder → verify → report) was never written as numbered steps by the lineage itself |
| W5 | The thin-firmware/thick-Python architecture is the load-bearing pattern — GoodFET ("quickly exposing embedded system buses to userland Python code"), Facedancer ("all of the complicated software is in Python on one workstation") — but stated as implementation commentary | The architecture is never stated as a LAW with its consequence: a rig whose bus cannot be scripted from the host generates no records, and unrecorded work is void to an agent; as commentary it reads as style, and style gets skipped |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | The interface instinct stated as a census rule with arithmetic | **M1** — the probeable-interface census with boundary rows |
| U2 | The junk-hacking aesthetic as an executable economics table | **M2** — the rig decision gate (ADAPT / JUNK / BUILD + the thin-thick law) |
| U3 | The datasheet treated as the hypothesis it always was | **M3** — port discovery with the discrepancy register riding from entry |
| U4 | The per-target bypass demos as one priced ladder | **M4** — the lock-bypass ladder with success-rate arithmetic |
| U5 | The promiscuity trick and the injection restraint as one radio protocol | **M5** — the radio channel: promiscuity before injection, authorization on record |
| U6 | The reproducibility flourish as a report standard | **M6** — verification gates + the rig-reproducible report with its parts list |
