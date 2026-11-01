# mindset.md — the Fyodor decision logic, translated

Load when applying the five laws to a live engagement, or when arguing
a scan-budget decision in the plan note.

## 1. The mind, as observed in the sources

The 1997 paper is a catalog of *decisions under constraint*, not a
list of packets:

* **Every technique is priced.** connect() scanning: fast, no
  privileges, but "easily detectable and filterable" and it trashes
  the target's logs. SYN scanning: fewer logs, needs root. FIN
  scanning: passes filters that watch SYNs, but "not 100% reliable
  (some systems, notably Micro$oft boxes, seem to be immune)". FTP
  bounce: hard to trace, "slow, and some FTP servers finally got a
  clue". The paper never recommends a technique; it states each
  technique's bill.
* **Reliability is engineered, not hoped for.** "Some scanners just
  send out all the query packets and collect the responses. But this
  can lead to false positives or negatives in the case where packets
  are dropped" — hence retransmission, configurable, especially for
  negative-logic scans where the signal is *absence*.
* **The scan adapts to the target.** Dynamic delay: "the response time
  of many hosts changes dramatically when they are being flooded with
  requests… nmap tries to determine the best delay time for you" and
  modifies it mid-scan.
* **Parallelism has an optimum, not a maximum.** Non-blocking I/O
  everywhere, but "on a very fast network you will actually decrease
  performance if you do more than 18 or so."
* **Dead hosts are the expensive failure.** "Some scanners allow you
  to scan large networks, but they waste a huge amount of time
  scanning 65535 ports of a dead host!" Ping first; also bail on hosts
  that develop strange errors mid-scan.
* **Priors are data.** The -F option scans "/etc/services" ports —
  the 1997 ancestor of today's top-ports tables built from internet
  scan data.
* **Even the tool's ergonomics follow the budget**: nmap detects your
  source IP "because I don't want to have to ifconfig every time" —
  operator attention is a resource to spend on the target, not the
  tool.

## 2. The translation table (1997 → arsenal)

| Then | Now (organ behavior) |
| --- | --- |
| ping sweep before port scan | `dns_resolve` + 1 probe before any sweep; park dead hosts |
| connect/SYN/FIN tradeoffs | triangle corner chosen per engagement and recorded in the plan note |
| retransmission counters | n_runs ≥ 2 on every signal; absence-based verdicts need repeats |
| dynamic delay from RTT | rate_per_s from observed latency; never a silent re-run at higher rate |
| bounded parallelism (-M) | batch sizes tuned to observed throughput; more is not a strategy |
| /etc/services priors | wordlist priors (top paths/params) + 404-baseline calibration |
| filtered = "we don't know" | three-valued verdicts recorded with their inference rule |
| reverse-ident after connect | version/banner facts follow only on live surfaces (R5: probes→surfaces) |

## 3. Failure modes this organ exists to kill

* Sweeping a host that never answered a cheap probe (paying 65535-port
  prices for a ping).
* Treating a single dropped-packet artifact as a closed port — or as
  an open one.
* "Full scan" ambitions that hit rate limits at 10% and quietly
  truncate — with no park note.
* Reading scanner output as ground truth (R5 in the spine: scanner
  output is hypothesis; probe records turn it into surfaces).
* Cranking the rate because nothing was found — effort discipline
  says park and re-plan, not re-run harder.

## 4. What the engine already enforces (do not re-implement)

* Every network tool gates through scope.csv first (R0) — the
  scan-economist never gets to price an unauthorized target.
* `content_discover` runs control requests first (404 baseline) and
  reports deviations only — the calibration law, already mechanical.
* Cap bits land in tool output; the contract requires parking, not
  silent re-runs.
