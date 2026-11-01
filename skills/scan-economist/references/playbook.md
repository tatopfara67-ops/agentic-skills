# playbook.md — running an economy-priced sweep

Load when executing a discovery sweep under this organ. The mindset
module explains the laws; this one sequences them.

## 0. Entry conditions

* Authorization class is `in_scope` for the target (else the organ
  stops before it starts — R0).
* A scan budget exists: probe cap, stage order, stop condition. If the
  plan note lacks them, write them BEFORE the first probe.

## 1. Stages (strict order — the cost hierarchy)

### Stage 1 — Resolve (0 target-side packets)

`dns_resolve(host)` per candidate. Park unresolvable names in the
dossier backlog with a note; do not probe them "just in case".

### Stage 2 — Liveness (1 packet per host)

One `http_probe` GET to the base URL. Outcomes:

* 2xx/3xx/4xx (anything answered) → live; record FACT with latency.
* timeout/refused → one retry after a beat; still dead → PARK record,
  backlog, move on. A dead host is a fact, not a challenge.

### Stage 3 — Surface sweep with priors

`content_discover(base_url, wordlist="default")`:

* the wordlist IS the prior — say which one and why in the plan note;
* rate: start at the tool default; adjust once from observed latency,
  record the adjustment;
* the cap bit in the result is a park note waiting to be written (R1).

### Stage 4 — Signal confirmation (retransmission)

Every deviation the sweep reports gets `http_probe` repeated:

* n_runs ≥ 2, same request, stable result → state verdict (SURFACE
  record + inference rule);
* unstable → EXPERIMENT record, lead status, do not escalate.

### Stage 5 — Depth on live surfaces only

Version-class questions (server headers, /robots.txt, JS assets) only
for surfaces that survived Stage 2 — banner questions never precede
liveness questions.

### Stage 6 — Stop

At budget, or when the last K probes added no new states
(saturation). Write the park note: what remains, why it is safe to
park, the resume condition.

## 2. The plan-note skeleton (fill per sweep)

```
scan-budget:
  cap: <total probes>
  stages: resolve → liveness → sweep(priors=<wordlist>) → confirm
  triangle: <fast|quiet|paranoid> — why
  rate: <start> → <adjusted after N probes, reason>
  stop: budget OR saturation(<K>)
  park: where leftovers go, resume condition
```

## 3. Worked micro-example (from the lab's own run)

The mythos-lab engagement priced its discovery exactly this way:
liveness probe on 127.0.0.1:8477 (R-005), calibrated content walk with
a 404 control before treatment paths, backup/config triage as priors
(S-004 backup.zip at priority 85 — a prior-priced hit), and every
reported deviation re-probed before it became a surface. The
548-record ledger is what an economy-priced sweep looks like when it
is also honest.

## 4. CLI sweeps (arsenal_route)

When a Kali-class CLI (nmap/httpx/ffuf) is the engine:

* `arsenal_route` enforces allowlist + flag blacklist + scope gate;
* you still choose the triangle corner (timing template, top-ports
  priors) and record it;
* output is hypothesis (R5) — confirm signals with arsenal probes
  before surfaces are registered.

## 5. Exit criteria

The organ is done when: every candidate is resolved/parked, every
live host has surfaces-or-a-why-not, every signal has n_runs ≥ 2 or is
a parked lead, and the park note is written. Numbers at the exit gate
(spine): candidates, live, surfaces, parked, probes spent.
