---
name: scan-economist
version: 1.1.1
type: ai-skill
architecture: package
description: >-
  Craft-lineage organ distilled from Gordon Lyon (Fyodor), author of Nmap —
  the economics of network discovery. Treats every scan as a budget problem
  with a cost hierarchy (cheap host discovery before expensive port scans,
  liveness before depth), a speed-vs-stealth-vs-reliability triangle for every
  technique, empirical port priors instead of exhaustive 65535 sweeps,
  adaptive timing with retransmission. Since v1.1.0 the organ carries the
  executable method layer (A16) — a mechanical critique of the Fyodor art's
  floors (techniques catalogued as a menu without a decision procedure, the
  adaptive timing policy hidden in tool defaults, version detection as an
  opaque database, scan narratives without footprint accounting, port priors
  by invisible default) shipped as protocol M1–M5: the budget table with unit
  prices, the portable measured timing gates, the service-ID confidence
  ladder, the footprint ledger, and the derived prior table that demotes the
  default top-100. Use when mapping hosts, ports, or services; when choosing
  scan timing or rate; when deciding what to scan first; when a port/host
  state verdict must be defended ("which ports first", "is this host even up",
  "scan budget", "too noisy", "which targets are alive").
category: security/craft-lineage
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: Gordon Lyon (Fyodor) — Nmap, Phrack 51 "The Art of Port Scanning" (1997), Nmap Network Scanning (2009)
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# scan-economist v1.1.1 — The Fyodor Lineage

## 0. What This Skill Is — and Is Not

* **Is**: the organ that decides *what to probe, in what order, at what
  rate, and when to stop* — discovery as an economy. Fyodor's original
  1997 paper and two decades of Nmap engineering distill to one insight:
  a scan is a resource-allocation problem under uncertainty, not a
  brute-force loop.
* **Is not**: a port scanner. The arsenal probes HTTP surfaces; this
  organ governs the *discipline* of any sweep (ports, paths, hosts,
  parameters) — cost hierarchy, timing, reliability, and priors.

## 1. The Lineage (attribution)

Gordon Lyon ("Fyodor") published Nmap with "The Art of Port Scanning",
Phrack Magazine Volume 7, Issue 51 (September 1997), and later *Nmap
Network Scanning* (2009). Nothing here is his code; this is his
decision logic, re-expressed as engagement rules. Sources and what was
consulted: references/sources.md — the verification record

## 2. The Five Laws of Scan Economy

1. **Cost hierarchy.** Never spend expensive probes on cheap questions.
   Dead hosts wasted "a huge amount of time scanning 65535 ports" in
   the 1997 scanners — so Nmap pinged first. Modern form: liveness
   and DNS before content; one cheap request before a parameter sweep.
2. **The technique triangle.** Every probe trades speed, stealth, and
   reliability (connect vs SYN vs FIN, 1997; fast vs thorough, now).
   Pick the corner the engagement needs, record the choice, never
   pretend one corner is free.
3. **States are inferences.** open / closed / filtered are deductions
   from responses or their absence — negative-logic results (UDP's
   "no answer means open-ish") demand retransmission or they breed
   false positives. A verdict without its inference rule is not a
   verdict.
4. **Priors over exhaustiveness.** Empirical port frequency data
   (nmap-services; /etc/services' 1997 ancestor) buys most of the
   value for a fraction of the probes. Modern form: top-paths and
   top-parameters wordlists before full sweeps, calibrated against a
   control.
5. **Adaptive pacing.** Delay computed from observed latency, then
   adjusted mid-scan as the target's response time changes under load;
   parallelism bounded because past a point it *hurts* ("more than 18
   or so" decreased performance on fast networks, 1997). Fixed rates
   are guesses; observed rates are data.

## 2.5 The Method Layer — Critique, Upgrade (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published scan art where it was mechanically weak — scans as a
trick menu not an economy, timing intelligence locked inside Nmap defaults,
version detection as a silently-matched database, writeups reporting ports
without packets, "top 1000" as an invisible prior — and ships the
executable replacement: **M1** the budget table (questions bind technique;
priced probe classes; 20% overrun abort), **M2** the measured timing gates
(RTT baseline, parallelism doubles only under loss < 2% and stable IQR,
halves on retransmit), **M3** the service-ID ladder (passive → generic →
class-specific; CONFIRMED/CLASS-ONLY/INFERRED pins), **M4** the footprint
ledger (sends, retrans, rates, yield on every session), **M5** the prior
table (target-derived priors first; house defaults last, with a resume
note).

## 3. Procedure — Numbered Actions

1. Before any sweep, write the scan budget: total probe cap (R7),
   stage order by cost hierarchy, and the stop condition.
2. Liveness/resolve first: `dns_resolve`, one `http_probe` — a host
   that fails cheap probes is parked, not swept.
3. Choose the triangle corner: for in_scope web surfaces the default
   is fast+reliable (bounded rates, n_runs≥2 on signals); stealth
   needs are an operator instruction, never an agent guess.
4. Sweep with priors: `content_discover` wordlist = the port-frequency
   table of this pipeline; record the cap bit when it truncates.
5. On any signal, retransmit: repeat the probe (n_runs ≥ 2) before the
   state leaves the ledger — one answer is weather, two is climate.
6. Record each state verdict with its inference rule
   ("SYN|ACK ⇒ listening" / "404-baseline deviation ⇒ exists").
7. Stop at budget or saturation; park the remainder with a resume
   note (R1). Exhaustive is a plan to be rate-limited, not thorough.

## 4. Tool Routing

| When | Tool |
| --- | --- |
| Liveness / resolution | `dns_resolve`, one `http_probe` |
| Calibrated sweeps | `content_discover` (wordlist priors, rate_per_s) |
| State verdicts + retransmission | `http_probe` with `n_runs` in the experiment card |
| CLI sweeps (nmap/httpx/ffuf class) | `arsenal_route` (allowlist + flag blacklist) |
| Parking leftovers | `ledger_append` (PARK) + dossier backlog flag |

## 5. Hard Rules

1. Cheap question, cheap probe — the cost hierarchy is never inverted
   to feel busy.
2. A negative-logic verdict (absence-based) without retransmission is
   a lead, never a finding.
3. Rate is chosen from observed latency and recorded; silent
   re-running at a higher rate is forbidden (R7).
4. Every sweep states its priors (which wordlist, why) and its cap
   bit — sweeps without priors are noise with a UI.

## 6. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Applying the five laws to a live engagement | references/mindset.md |
| Running a sweep end to end | references/playbook.md |
| Checking what the lineage actually said | references/sources.md |
| Grading the published method, pricing the budget, holding timing gates | references/method-upgrade.md |
