# The method upgrade — critiquing Shimomura, shipping the executable hunt

The charter's A16 charge: **a lineage named is not expertise delivered.**
This module reads the 1994–95 hunt (references/history-1995.md) as a
*method*, grades it against what a tracker can do today, keeps what was
right, names what was weak, and ships the replacement as executable
protocol M0–M5 — numbered steps, exact commands, thresholds, decision
tables, and the ledger points where each artifact lands. An agent that
has never heard of Shimomura must be able to run this at his precision.

## 1. The critique — six mechanical weaknesses of the 1994–95 method

The hunt succeeded. The method still had floors, and pretending
otherwise is mythology, not lineage. Each weakness below is mechanical,
not biographical:

| # | What he did (documented) | Why it was weak |
| - | ------------------------ | --------------- |
| W1 | Detection by instrumented luck — the intrusion surfaced because tcpdump traces and accounting logs happened to be running on a curious physicist's machines | Detection depended on a person's habits, not on a system. Nothing fired on first touch; the discovery came at morning-after review |
| W2 | Triangulation by telephone — friends at other sites were phoned and asked to run taps; clock state across sites was never disciplined; arrival-time deltas were eyeballed | Inter-sensor timing evidence with unsynced clocks carries error of tens to hundreds of ms — thousands of km of slack. It worked only because the adversary was noisy and stationary |
| W3 | Ad-hoc fingerprinting — headers, sequence arithmetic, and TTL quirks were read by one expert's eyes | Irreproducible: two analysts reading the same capture could disagree with no protocol to resolve them. The fingerprint lived in the man, not the method |
| W4 | Pure observation from his own vantage — no deception layer, no tarpit, nothing that slowed or steered the adversary | Dwell time was the attacker's choice. The defender's budget (their exposure) was spent at the attacker's preferred rate |
| W5 | The person-level fix came from carrier records and RF measurement — out-of-band assets a network defender cannot assume | Correct as a handoff, but the network method itself stopped at metro granularity and never said so: no stated localization floor |
| W6 | Narrative epistemology — conclusions in the writeup are single-run stories; no pre-registration, no n_runs, no falsifier | The account is convincing because of who told it. Swap the physicist for a mediocre analyst and the same steps could convict a dial-up modem |

## 2. The upgrades — what he should have had, and what we ship

| # | The should-have-been | What this organ implements |
| - | -------------------- | -------------------------- |
| U1 | Detection as an always-on, tamper-evident tripwire layer — canaries and flow records that fire on FIRST touch | **M0** — the tripwire layer, installed before any hunt exists |
| U2 | NTP-disciplined sensor mesh with recorded offsets; timing evidence quoted with its error bar, or not at all | **M0 clock gate + M3(b)** — multi-sensor arrival deltas with a sync-error table |
| U3 | Fingerprinting as a calibration protocol against KNOWN stacks in the same environment, with a clustering predicate two analysts must agree on | **M2** — the four-feature signature, the decision table, the clustering rule |
| U4 | Deception that spends the adversary's budget, not ours — tarpits, per-placement canary tokens, latency shaping | **M4** — under the tip-off gate; every deployed deception is a FACT record |
| U5 | The localization floor stated in the pack: network evidence ends at metro/ASN granularity; person-level attribution is the consumer's lane | **M5** — handoff fields, floor stated, no overclaim |
| U6 | Pre-registered halving, two-channel confirmation, append-only records | The SBB engine itself (`arsenal/sbb.py`) — this module supplies the concrete network-hunt instantiations |

## 3. The executable protocol — M0 through M5

### M0 — the tripwire layer (before any hunt exists)

1. File canaries: one unreadable-but-tempting file per sensitive
   directory (`~/backup-keys.tar.gz.pgp`, `/etc/.ops_readme`), each
   containing a **unique per-placement token**. Any read of a canary
   with its token seen anywhere (DNS query, HTTP body, log line) is
   SIGNAL=1 with a provenance channel already attached.
2. Kernel audit watches (Linux): `auditctl -w ~/.ssh/authorized_keys
   -p wa -k ssh-keys`, `-w /etc/passwd -p wa -k identity`,
   `-w /etc/sudoers -p wa -k privilege`. Tripwire events are FACT
   records the moment they appear.
3. Always-on ring-buffer capture on each sensor (no hunt needed):
   `tcpdump -i <if> -G 3600 -W 48 -C 256 -w /var/cap/ring` — 48 hours
   of 256 MB slices. The BPF filter EXCLUDES your own scanner subnets
   so the ring holds third-party traffic only.
4. Flow telemetry retention: VPC flow logs / netflow export with a
   written retention window (≥ 14 days) — the netflow channel is only
   a channel if its history exists.
5. **Clock gate**: `chronyc tracking` on every sensor; record
   `system time` offset per host as a CONTROL record.
   *Decision gate*: any sensor with offset > **10 ms** → its timing
   evidence is demoted to "coarse" for the whole hunt (M3(b) error
   table shows what that costs). Fix it, or quote the floor.

### M1 — freeze-plus (volatile state the 1994 capture could not hold)

P0 froze the disk-and-packet scene; M1 also grabs state that dies with
the connection table, within the first minutes, before any sbb call:

```
ss -tunapE                       # socket→process mapping, live
conntrack -L -o timestamp        # flow table with ages
ps -eo pid,lstart,etimes,cmd --sort=lstart   # process ages vs claim times
ip neigh show                    # L2 neighbors at freeze moment
last -F -n 50 && lastb -F -n 50  # login history incl. failed
```

Each output is hashed (`sha256sum`), stored as an artifact, and
ledgered FACT with sensor origin and the clock CONTROL it cites.
Freeze is not complete until the volatile set exists.

### M2 — stack fingerprint discipline (the W3 fix)

Four features, one extraction, one clustering rule. All values are
**calibrated against known hosts in the same environment first** —
your own fleet is the control group; the table below narrows, it never
concludes alone.

Extraction (one pass over the capture):

```
tshark -r <ring-or-capture.pcap> -Y "ip.src==<attacker-ip>" \
  -T fields -e tcp.stream -e ip.ttl -e ip.id \
  -e tcp.window_size -e tcp.options.timestamp_tsval
```

Table F-1 — the four features:

| Feature | Reading | Discriminates |
| ------- | ------- | ------------- |
| `ip.ttl` → initial TTL | nearest ceiling of {32, 64, 128, 255} minus observed | OS family + hop distance (64/128/255 are the common ceilings) |
| `ip.id` arithmetic | per-stream series: incrementing / constant-zero / per-destination / randomized | stack family; a CHANGE mid-session = NAT or tool swap |
| `tcp.window_size` | value + its scaling multiple through the handshake | stack family (calibrate: your Linux fleet, your Windows fleet) |
| TSval cadence | ΔTSval / Δcapture-time = stack clock Hz; TSval at SYN / Hz = host uptime seconds | host identity + reboot history; uptime is the strongest cluster key |

**Clustering predicate** (two analysts must reach the same partition
from the same capture — that is the point):

> Sessions S1, S2 are the SAME HOST iff initial-TTL class is equal AND
> IP-ID family is equal AND TSval Hz is equal AND implied boot times
> agree within **±300 s** AND both use the same window-size class.

Calibration rule: run the predicate over sessions from ≥ 3 KNOWN
distinct hosts (your own fleet, same sensors) first. If known-distinct
hosts merge, the thresholds are wrong for this environment — re-baseline
and record the corrected predicate as a CONTROL record. Only then run
it over the adversary's sessions.

Output: one FINGERPRINT record per cluster — features, member streams,
implied uptime, calibration CONTROLs cited. This is the W3 fix made
mechanical: the fingerprint lives in the table, not the man.

### M3 — localization at the network floor (the W2 fix)

Two passive techniques. Both are EXPERIMENT records with thresholds
pre-registered BEFORE the numbers are read.

**(a) Passive RTT from the captured handshake.** For each adversary
session in the capture: RTT = time(their SYN) → time(their ACK
completing the handshake). One sample per session, free and quiet.
Physics: fiber carries ~200 km per ms one-way, so distance ≤
(RTT/2) × 200 km/ms. RTT 30 ms → ≤ 3,000 km; RTT 5 ms → ≤ 500 km.
Distribution over sessions: report the **median and IQR, never a
single sample**.
*Hard caveat*: a VPN or relay inflates RTT while shrinking apparent
distance error — so RTT is a **consistency check** (does it agree with
the AS path and hop count from TTL?) unless the path is known-direct.
A contradiction (RTT 3 ms but 6 AS hops) is recorded as relay-suspected
and RTT is demoted to coarse for that cluster.

**(b) Multi-sensor arrival deltas** — the U2 upgrade of the telephone
triangulation. The same attacker packet, mirrored at N disciplined
sensors: pairwise Δt of arrival, each Δt × 200 km/ms = the bound on
path-length DIFFERENCE to that pair. Three sensors bracket a region.
Error budget is mechanical, not aspirational:

| Sensor clock sync (per pair) | Distance-difference error |
| ---------------------------- | ------------------------- |
| 1 ms | ± 200 km |
| 100 µs | ± 20 km |
| 10 µs (PTP-class) | ± 2 km |

*Decision gate*: quote the sync class in every delta record. Deltas
from a coarse sensor (M0 gate tripped) may bound a continent, never a
city.

*Rule T applies*: a localization claim needs a second independent
channel (netflow path history, host-audit DHCP/lease records) — timing
alone is one story told with precision, which is still one story.

### M4 — deception under the tip-off gate (the W4 fix)

Deception exists to spend THEIR budget: every minute a tarpit holds a
connection is a minute they are not touching real assets, and every
canary fetch is a fresh SIGNAL with provenance.

1. **Tarpit** on ports nothing legitimate uses (e.g. 2222, 5555): an
   endlessh-style service that answers and never finishes a banner.
   Deployed = FACT record with port and start time.
2. **Honeypot content with per-placement tokens**: the M0 canary files,
   now placed where the adversary's demonstrated intent points
   (their download pattern from P2). Token design: unique per
   placement, never reused — a hit maps to one file, one incident.
3. **Latency shaping**: if you can shape response times, slow
   enticement (200–400 ms) reads as "loaded old server" and holds
   scanners longer than instant refusal.
4. **The gate**: deploying deception changes state the adversary can
   observe — TIP-OFF=1 by definition. The engine already refuses
   tip-off actions while passive eliminators remain; when passive
   reserves are exhausted, deception is IR's call at containment
   time (playbook P4), not the tracker's during the trace.
5. Canary callbacks convert to a PASSIVE channel the moment they fire:
   `dns_resolve` on the canary domain is quiet reading, and the
   callback's source IP feeds M2 fingerprinting.

### M5 — handoff with the floor stated (the W5/W6 fix)

The pack (references/evidence-templates.md) gains one mandatory block:

```
LOCALIZATION FLOOR: network evidence ends at {metro|ASN|path-distance} X.
Fingerprint clusters: {cluster table from M2, calibration CONTROLs cited}
Dwell timeline: {first-touch → last-activity, per sensor}
Person-level attribution: out of scope — IR/law-enforcement lane.
```

Every line cites R-NNN records; the auditor recomputes what it can.
Overclaiming past the floor ("the attacker IS in city Y" from a 200 km
error bar) fails the audit exactly like an uncited claim.

## 4. Falsifiers — what would prove this method wrong

* Two sync-≤100 µs sensors disagree by more than the error table
  allows → path asymmetry, not distance: record a MISTAKE, never
  average the disagreement away.
* The M2 predicate merges two known-distinct control hosts → the
  thresholds are miscalibrated for this environment: re-baseline
  before any adversary conclusion drawn from it stands.
* RTT bound contradicted by AS-path/hop evidence → relay suspected:
  RTT demoted, never defended.
* A null-hypothesis elimination later shown to rest on a noisy channel
  → re-open via `sbb_declare`; eliminated hypotheses stay dead only
  while the eliminating record stands.

## 5. Worked micro-example (numbers consistent, incident fictional)

Sensor mesh: 3 taps, chrony offsets 0.4/0.8/1.2 ms → all under the
10 ms gate, sync class 1 ms (±200 km per pair).

| Evidence | Value | Reading |
| -------- | ----- | ------- |
| attacker SYN TTL | 61 | initTTL 64, ~3 hops to nearest sensor |
| IP-ID series | +1 per packet | incrementing family |
| TSval Hz / uptime | 250 Hz / 17 days | one host, no reboot across sessions |
| handshake RTTs (11 sessions) | median 22 ms, IQR 3 ms | distance ≤ ~2,200 km (consistency: 4 AS hops — plausible) |
| Δt sensor1↔2 | 0.9 ms ± sync 1 ms | path-difference ≤ 180 km — metro-scale bracket with sensor 3 |
| netflow channel | source ASN stable across 11 sessions | second channel agrees: single origin AS |

Floor statement: *path-distance and AS granularity — a metro region at
best; person-level attribution not claimed.* Two channels (timing +
netflow), both ledgered, null hypothesis eliminated first (scheduled
authorized scan calendar — the cheap bit). That is the 1995 hunt with
the floors fixed.
