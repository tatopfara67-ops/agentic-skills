---
name: content-discovery
version: 1.0.0
type: ai-skill
architecture: package
description: Phase-1 content discovery organ — calibrated, rate-courteous wordlist walks that report baseline deviations only, plus backup/config artifact hunting with differential triage. Use when the operator asks to find hidden paths, hunt backup or config files, brute directories politely, or triage discovered files ("cari path tersembunyi", "backup hunting", "wordlist", "directory brute", "file discovery", "cari .env").
category: security/offensive-web
license: MIT
metadata:
  author: tatopfara67-ops
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.3+
---

# content-discovery v1.0.0 — Calibrate, Then Walk

## 0. What This Skill Is — and Is Not

* **Is**: the Phase-1 organ that finds what the sitemap forgot — with a
  calibrated oracle deciding what counts as "found". The `content_discover`
  tool fires three control requests at random non-existent paths BEFORE the
  wordlist walk: the target's own 404/soft-404 profile IS the baseline.
* **Is not**: an uncapped fuzzer. Requests are GET-only, rate-courteous,
  capped per invocation, and every request lands in the ledger.

## 1. Inherited Contracts

Plugs into **Phase 1** (primary sweep) and **Phase 3** (targeted re-walks)
of the mythos-bug-hunter spine. Inherits the Canon, ledger discipline,
backlog mechanics, and the differential mindset (control first — spine §6).

## 2. Why Calibration Is Not Optional

A bare "status != 404" rule is slop with a for-loop. Targets answer
non-existent paths with soft-404s (200 + "not found" body), wildcard
handlers, and redirect-to-search chains. The calibration round measures the
target's actual behavior on three random junk paths; a finding is a
DEVIATION from that measured baseline — status deviation, or (under
soft-404) a size outlier. `references/wordlists.md` documents the ladder;
the calibration mechanics are enforced inside the tool.

## 3. Procedure — Numbered Actions

1. Entry: AUTH record present; base URL in scope (`scope_check`).
2. First walk: `content_discover(program, base, wordlist="default",
   extensions=["", ".bak", ".old", ".zip"])` — capped, default rate.
3. Read the calibration verdict in the result. If `soft_404: true`, treat
   every 200 with baseline size as noise and trust size outliers only.
4. Triage each finding with the matrix in `references/patterns.md`:
   * backup/config artifacts → `backup-artifact` / `config-exposure`
   * redirect findings → `redirect-handler` + record Location
   * auth/admin shapes → `auth-endpoint` / `admin-console`
   * interesting-but-unripe → `backlog=True` with a resume note
5. Targeted second walk only for signals that earned it: tech-specific
   wordlist (see `references/wordlists.md` ladder), extensions round
   (`.tar.gz`, `.sql`, `.example`), bounded by the same cap.
6. `dossier_add` each triaged finding citing the SURFACE record the tool
   emitted.
7. Exit gate: numbers stated — probes sent, calibration verdict, findings,
   backlog count. Every finding cites its record.

## 4. Hard Rules (mechanically enforced)

1. **Control requests first.** The tool refuses to walk before calibrating;
   the CONTROL records precede all FACT records of the walk in the ledger.
2. **GET-only.** No POST/PUT content discovery in this organ.
3. **Capped and courteous.** `max_requests` and `rate_per_s` defaults are
   the ceiling unless the operator explicitly raises them and the reason
   lands in the ledger note.
4. **Findings are deviations.** The SURFACE record carries the calibration
   numbers in its note — the auditor checks.

## 5. Tool Routing

| When | Tool |
| --- | --- |
| Calibrated walk | `content_discover` |
| Targeted artifact fetch (headers/body) | `http_probe` |
| Faster local walk when `ffuf` installed | `arsenal_route(program, "ffuf", base, "-w default.txt -mc all -ac")` — output still goes through triage as hypotheses |
| Registering findings | `dossier_add` (surface-cartographer) |

## 6. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Choosing the ladder rung / tech-specific list | `references/wordlists.md` |
| Triage of a specific finding class | `references/patterns.md` |
