# The method upgrade — critiquing Fyodor, shipping the executable scan economy

The charter's A16 charge: **a lineage named is not expertise delivered.**
Fyodor's art is real — Phrack 51 (1997) invented the modern port
scan, Nmap industrialized it, the book (2009) systematized it — but
the published form has floors: techniques told one at a time, the
timing engine's intelligence hidden behind tool defaults, version
detection as an opaque database, and scan stories reported at machine
speed with no footprint accounting. This module extracts what is
tool-agnostic and ships the replacement: an explicit cost hierarchy
with arithmetic, empirical port priors, measured timing gates,
liveness-before-depth as a hard gate, and a footprint ledger. An
agent without Nmap must run this at its economy.

## 1. The critique — five mechanical weaknesses of the published method

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | Techniques catalogued singly — Phrack 51 presents scan types (TCP connect, SYN, FIN, NULL, Xmas, UDP) as a menu of tricks | No decision procedure binds technique to PURPOSE: which scan, for which question, at which point in the budget — the reader inherits a toolbox, not an economy |
| W2 | Timing intelligence hidden in defaults — Nmap's adaptive timing (congestion window, RTT tracking) is tuned by the tool, and the book documents the KNOBS, not the policy | Operators who cannot run Nmap (agent environments, restricted toolsets) inherit nothing: the adaptive policy was never published as a portable rule |
| W3 | Version detection as an opaque DB — the service probes and match lines are a shipped artifact, matched silently | The METHOD (probe ladder cheap-first, match-line confidence) is not transferable as written; re-implementers guess and call it "version scanning" |
| W4 | Scan narratives without footprint accounting — writeups report ports found, not packets sent, rates held, or alerts risked | Without a footprint ledger the same "successful scan" is un-ratable for stealth and civility; two scans with identical finds are treated as equal when one burned 50× the budget |
| W5 | Port priors by habit — "scan top 1000" is a Nmap default, not a stated prior with an empirical basis per environment | The default is invisible: nobody re-derives whether 1000 is right for THIS target class, and the alternative (empirical prior from the target's own exposed service class) is never computed |

## 2. The upgrades — and where they land

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | Cost hierarchy as arithmetic, questions binding technique | **M1** — the budget table |
| U2 | The adaptive timing policy, portable | **M2** — the measured timing gates |
| U3 | Version detection as a probe ladder with confidence classes | **M3** — the service-ID ladder |
| U4 | Every scan accounted in packets and rates | **M4** — the footprint ledger |
| U5 | Port priors derived per target class, defaults demoted | **M5** — the prior table |
| U6 | Liveness before depth as a hard gate | House doctrine (§2 law 2), given its enforcement record here |

## 3. The executable protocol — M1 through M5

### M1 — the budget table (cost hierarchy as arithmetic)

Before scanning, the budget is written down; each probe class priced:

```
BUDGET: question="which mail ports on 25 live hosts"
  assets=25 prices: icmp-echo=1u udp-recvonly=4u tcp-syn=2u
  tcp-connect=6u tcp-syn+ack-service-probe=12u full-banner=20u
  allocation: discovery 60u · liveness 40u · depth 120u
  abort: any unit overrun > 20% = re-derive plan on record
```

Rules: the QUESTION binds the technique (W1) — "is it alive" buys
icmp/arp class only; "which service" buys syn probes on the prior
table's ports only; "which version" buys M3's ladder only after a
service answered. A probe class purchased without its question on
record is a refused request.

### M2 — the measured timing gates (the portable adaptive policy)

The Nmap policy, re-stated as rules an agent can execute with any
socket:

1. **RTT baseline first**: 10 probe round-trips, median + IQR
   recorded as CONTROL. Initial parallelism = 1.
2. **Scale rule**: parallelism doubles only when loss < 2% AND
   RTT-IQR/median < 0.3 across the last 50 sends; halves on any
   retransmit or loss > 5%.
3. **Rate floor**: never exceed max(1 probe / (2 × median-RTT) per
   stream, house civility cap) — the target's own response time is
   the pacing clock, not the scanner's patience.
4. All four numbers ride every scan record: `parallelism, loss%,
   rtt-median, rtt-iqr` — a scan reported without its timing state is
   an anecdote, not a measurement (the W2/W4 floor, shared).

### M3 — the service-ID ladder (version detection, portable)

1. Cheap-first probe ladder per open port: (a) passive — wait for a
   banner or observe the port's response to the SYN-ACK alone;
   (b) generic newline / HTTP GET (for web-class ports only);
   (c) class-specific probes (SMTP EHLO, SSH version exchange) —
   each rung only after the previous returned nothing.
2. Match confidence classes, not product strings: CONFIRMED (banner
   states product+version), CLASS-ONLY (banner states family),
   INFERRED (behavior class only — e.g. "HTTP/1.1 + specific header
   order"). The finding's version pin cites the class; INFERRED pins
   are never reported as versions (the W3 floor).
3. Each rung's response is an artifact (hash + first 128 bytes) —
   match lines are OURS, versioned, auditable.

### M4 — the footprint ledger

Every scan session closes with an accounting row:

```
FOOTPRINT: session=<id> sends=<n> retrans=<n> unique-dst-ip=<k>
  unique-dst-port=<m> peak-rate=<pps> duration=<s> finding-yield=
  <open-ports, versions> noise-risk=<low|medium — basis>
```

The ledger enables the honest comparisons the writeups omit (W4):
two candidate plans for the same question are chosen by expected
yield per unit, on record — not by habit.

### M5 — the prior table (defaults demoted)

| Source | Prior class | Use |
| ------ | ----------- | --- |
| target's own exposure class (from dossier) | e.g. web-front: 80/443/8080/8443 weighted | first depth pass |
| environment evidence (ASN neighbors, banner census if available) | same-provider service classes | second pass |
| house default top-100 | generic fallback | LAST, and only with a resume note |

Rule: the default prior is spent only after the derived priors are
exhausted or absent ON RECORD; "top 1000" without a derivation is
the refused habit (W5).

## 4. Falsifiers — what would prove this method wrong

* Loss stays < 2% but a depth probe still gets dropped repeatedly →
  a filtering device, not congestion: record firewall-suspected,
  switch technique class (e.g. syn → fin/ack-echo class), never
  brute the drop.
* The derived prior misses a port that the default top-100 would
  have found → the prior table underweighted this target class:
  record the miss, correct the weights, and the correction is a
  CONTROL record for the next campaign.
* A CONFIRMED version pin contradicts an INFERRED one from the same
  ladder run → the inference class row is wrong: file it, re-derive
  the behavior signature.
* Footprint ledger shows yield collapsed (0 new ports in the last
  30% of budget) → the economy is broken: the scan should have
  stopped at the marginal-yield gate, and the NEXT plan cites this
  row as the reason it stops earlier.

## 5. Worked micro-example (numbers consistent, incident fictional)

Question: mail-service exposure on 12 hosts. M1 budget: discovery
(arp/icmp) 12u spent; liveness: syn on prior table ports
(25/465/587 — mail class) = 36 probes at parallelism 2. M2: RTT
median 11 ms, IQR 3 ms, loss 0% → parallelism scales to 4, holds.
M3: port 25 banner "220 mail ESMTP Postfix" = CONFIRMED pin
(Postfix, no version stated — CLASS-ONLY version cell); 587 silent
to newline → INFERRED "TLS-wait class", recorded as class only.
M4: 48 sends, 0 retrans, peak 4 pps, duration 9.4 s, yield
2 open ports 1 confirmed service class. M5: default top-100 not
spent — derived prior covered the question; resume note says so.
