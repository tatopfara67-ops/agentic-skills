# Worked Example — Full Engagement Walkthrough (Authorized Lab)

This walkthrough demonstrates the complete mythos-bug-hunter pipeline on a
**self-owned lab**: scoping → recon → pre-registered hypotheses → differential
experiments → impact synthesis with a canary → self-audit → report.

Two honesty notes before the ledger opens:

1. This engagement **rediscovers a known vulnerability** (CVE-2025-29927, the
   Next.js middleware skip, fixed in 12.3.5 / 13.5.9 / 14.2.25 / 15.2.3).
   Rediscovery on an owned lab is the calibration standard for this skill:
   it proves the machine works before it is pointed at anything novel.
2. Every byte of "user data" in this lab is synthetic and was planted by the
   operator. The only marker used to prove data reach is a self-injected
   canary. Zero real data exists in this environment.

Lab under test: **TaskBoard** — a self-hosted demo app built on Next.js
14.2.5 (standalone server), reachable at `http://127.0.0.1:3100`. Routes:
`/` (public board list), `/login` (form), `/admin` (dashboard, gated),
`/api/admin/users` (JSON, gated).

---

## Phase 0 — Scoping

Authorization first (Canon R0):

```
AUTH | A-001 | self-owned lab | artifact: operator declaration + process ownership (taskboard demo on 127.0.0.1:3100) | scope: 127.0.0.1:3100 only | rate: unrestricted (localhost) | budgets: 15 cards/vector, 400 records, 2h wall clock
```

Capability inventory (Canon R5): curl 8.x, python3 11, jq. No MCP toolchain
attached in this environment → the fallback ladder applies (curl one-liners,
python3 for repetition loops). Recorded so the engagement never "discovers"
mid-flight that a tool it assumed was absent… or present.

Fact table — facts only, interpretation waits for Phase 2:

```
R-001 | 2026-10-30T09:02:11Z | curl | GET / | 200 | HTML, title "TaskBoard", asset paths /_next/static/... | 11.4KB | FACT | framework fingerprint: /_next/ asset namespace
R-002 | 2026-10-30T09:02:40Z | curl | GET /_next/static/chunks/app/page-4c1f.js | 200 | webpack chunk comment contains "14.2.5" | 89KB | FACT | version marker
R-003 | 2026-10-30T09:03:05Z | curl | GET /admin | 307 | location: /login | 412B | SURFACE | redirect-style gate, no WWW-Authenticate
R-004 | 2026-10-30T09:03:22Z | curl | GET /api/admin/users | 307 | location: /login | 412B | SURFACE | API uses the same redirect gate
R-005 | 2026-10-30T09:03:58Z | curl | GET /login | 200 | HTML form, fields user/pass | 3.1KB | SURFACE | login form
R-006 | 2026-10-30T09:04:30Z | curl | HEAD / | 200 | no Server header, no X-Powered-By | 0B | FACT | header hygiene present
```

Canary planted before the first crafted payload (Phase 4 will recover it):

```
R-020 | 2026-10-30T09:10:00Z | operator | planted synthetic DB row: user canary_user, note "MYTHOS-CANARY-9f2c7b41" | — | — | CANARY | self-owned lab, synthetic data only
```

Phase 0 exit gate: technology claims later in this engagement cite R-001/R-002
or they do not get made.

## Phase 1 — Recon and Surface Inventory

| AS-ID | Surface | Class | Evidence | Reachability (anonymous) |
|---|---|---|---|---|
| AS-001 | `/` public board | web page | R-001 | 200 |
| AS-002 | `/login` form | auth surface | R-005 | 200 |
| AS-003 | `/admin` dashboard | gated page | R-003 | 307 → /login |
| AS-004 | `/api/admin/users` | gated JSON API | R-004 | 307 → /login |
| AS-005 | `/_next/static/*` | framework assets | R-002 | 200 |

Backlog seeds (Canon R1 — held, not queued): login-form CSRF angle (prior
10%, needs a second browser session); board write-spam (out of lab interest);
`/_next/static` source-map leak (quick card, queued after the gate vector).

Exit gate: every surface classified, none hypothesis-less (Phase 2 does that
now), 307s treated as **signals, not verdicts** (Canon R2 — a redirect gate is
an invitation, not a wall).

## Phase 2 — Hypothesis Pre-Registration

Registered in the ledger before the first crafted payload leaves the machine
(Canon R4 / SKILL.md §5). Closure lines shown filled for readability; at
registration time they were empty.

### H-001 — Middleware auth-gate skip via internal routing header (facts R-002, R-003, R-004)
- claim: If the edge gate is skipped by the framework's internal subrequest routing header, then GET /admin carrying `X-Middleware-Subrequest: middleware` returns 200 with the dashboard body instead of 307.
- facts: R-002 (framework 14.2.5 — inside the advisory's affected range, fixed line at 14.2.25), R-003, R-004 (gate style: framework-level redirect)
- prior: 70% — base rate: the public advisory for CVE-2025-29927 maps this exact version range as affected; held below 90% because a fronting proxy that strips the header would sink the treatment.
- falsifier: treatment delta = 0 across n_runs, or the control header (same shape, wrong name) produces the same 200.
- Closure: CONFIRMED (E-101..E-104; R-101..R-109)

### H-002 — Auth-gate skip via client-IP trust (facts R-003)
- claim: If the gate trusts an internal-client IP signal, then GET /admin with `X-Forwarded-For: 127.0.0.1` returns 200.
- facts: R-003
- prior: 15% — base rate: IP-based local trust conflicts with the observed framework-level redirect pattern.
- falsifier: delta = 0 across n_runs.
- Closure: FALSIFIED (E-105..E-107; R-113..R-115)

### H-003 — Login username-existence timing side channel (facts R-005)
- claim: If the login endpoint leaks username existence through response time, then valid-user attempts with wrong passwords are measurably slower than invalid-user attempts across ≥20 samples per arm.
- facts: R-005
- prior: 30% — base rate: login timing differentials are common in the wild but frequently masked at localhost resolution.
- falsifier: fully overlapping timing distributions across samples.
- Closure: INCONCLUSIVE (E-108..E-110; distributions overlap at localhost resolution; Park P-001)

### H-004 — API gate shares the middleware skip (facts R-004, E-102)
- claim: If the API route's 307 gate is the same middleware, then the same header returns 200 JSON from /api/admin/users.
- facts: R-004, E-102 (page-route result)
- prior: 80% — base rate: same mechanism already evidenced on the page route; residual 20% for a layered session check behind the edge gate.
- falsifier: API stays 307, or returns 401 after the header.
- Closure: CONFIRMED (E-111..E-112; R-121..R-123)

## Phase 3 — Experiments

### E-101 — Baseline: anonymous /admin
- hypothesis: H-001
- baseline: this card IS the baseline
- treatment: n/a
- control: n/a
- n_runs: 3
- records: R-101..R-103 — 307 → /login, 412B, byte-identical bodies
- delta input: establishes the world-as-it-is

### E-102 — Treatment: internal routing header
- hypothesis: H-001
- baseline: E-101 (R-101..R-103)
- treatment: `curl -s -o /dev/null -w '%{http_code} %{size_download}' -H 'X-Middleware-Subrequest: middleware' http://127.0.0.1:3100/admin`
- control: E-103
- n_runs: 3
- records: R-104..R-106 — 200, 5.3KB, dashboard HTML ("Admin — TaskBoard", user-table markup)
- delta input: status 307→200, size 412B→5.3KB, body redirect-fragment→dashboard

### E-103 — Control: same-shape header, wrong name
- hypothesis: H-001
- baseline: E-101 (R-101..R-103)
- treatment: `X-Noop-Value: middleware` (same effort, unrelated name)
- control: this card IS the control
- n_runs: 3
- records: R-107..R-109 — 307 → /login, 412B, identical to baseline
- delta input: specificity proven — the 200 belongs to the header's name, not to sending any extra header

### E-104 — Delta analysis (H-001 gate check)
- baseline 307/412B [R-101..R-103] vs treatment 200/5.3KB [R-104..R-106] vs control 307/412B [R-107..R-109]
- reproduction: 3 identical consecutive deltas on both arms; deterministic behavior
- verdict input: falsifier never observed; control clean → H-001 closes CONFIRMED

### E-105..E-107 — X-Forwarded-For arms (H-002)
- treatment variants: `X-Forwarded-For: 127.0.0.1` / `X-Real-IP: 127.0.0.1` / `CF-Connecting-IP: 127.0.0.1`
- n_runs: 3 per variant
- records: R-113..R-115 — 307 → /login on every run, zero delta
- verdict input: falsifier observed → H-002 closes FALSIFIED

### E-108..E-110 — Timing arms (H-003)
- design: 20 requests per arm (valid-user/wrong-password vs invalid-user), python3 loop, `time.perf_counter()` around each request, medians compared
- attempts: 20 per arm
- records: R-116..R-118 — median 41.2ms vs 40.9ms, distributions fully overlapping
- verdict input: falsifier territory, but resolution at localhost is suspect → INCONCLUSIVE, not FALSIFIED; Park P-001

```
PARK | H-003 | budget exhausted at 12/15 cards | tried: E-108..E-110, localhost timing arms overlap (R-116..R-118) | next: re-run against the lab's LAN-facing binding with ≥1ms median deltas required in FACT records before card spend | resume-cost: low
```

### E-111..E-112 — API route arms (H-004)
- baseline: GET /api/admin/users → 307 [R-120]
- treatment: same + `X-Middleware-Subrequest: middleware` → 200, JSON array [R-121..R-123]
- n_runs: 3
- delta input: 307→200 with JSON body; deterministic

## Phase 4 — Impact Synthesis

Impact chain, every link carrying its record:

```
Impact chain: crafted header [R-104] → middleware execution skipped [R-105..R-106] → protected route bodies returned [R-106, R-123] → synthetic data exposure via /api/admin/users [R-122]
```

Canary round-trip (SKILL.md §8): the marker planted as R-020 was recovered in
the treatment response body — `MYTHOS-CANARY-9f2c7b41` appears verbatim in the
JSON note field of user `canary_user` [R-122]. Channel existence is proven
with self-injected data only.

Bounded scope: enumeration was bounded to a single page of the JSON array
(default page size 3) — reachability is proven by one page, not by harvest.
The engagement never requested a second page.

Attestation: zero real-data access. All rows in the lab are operator-planted
synthetic records; the only marker used for proof was the self-injected
canary.

## Phase 5 — Self-Audit

```console
$ python3 scripts/audit_report.py example/worked-example.md
audit_report.py — example/worked-example.md
  hypothesis blocks : 4  (confirmed 2, falsified 1, inconclusive 1)
  cited claim lines : 5
  n_runs fields     : 5

  PASS — report satisfies the Report Contract. Ship it.
```

Mistake ledger (Canon R4 learning loop, numeric not narrative):

```
MISTAKE | H-002 | prior 15% → FALSIFIED | pattern: IP-trust hypotheses contradict framework-level redirect gates | adjustment: cap IP-trust priors at 10% when R-evidence shows a framework gate
MISTAKE | H-003 | prior 30% → INCONCLUSIVE | pattern: timing arms on localhost lack resolution | adjustment: require a ≥1ms median FACT delta before spending cards on timing vectors
KEEP   | H-001 | operator Inversion (assumption negation) generated the winning hypothesis at zero tool cost | repeat first in future engagements
```

## Report (final artifact)

# Vulnerability Report: TaskBoard edge-gate skip on /admin and /api/admin/users

## Summary

The middleware protecting `/admin` and `/api/admin/users` is skipped when a
request carries the framework-internal routing header, returning protected
content to anonymous users [R-104..R-106, R-121..R-123].

## Severity

High [R-004, R-123] — class: authorization boundary failure; the public
advisory for CVE-2025-29927 scores this mechanism at CVSS 9.1 and lists
14.2.25 as the fixed line for the 14.x series.

## Affected Component

Middleware-based access gate; framework Next.js 14.2.5 [R-002].

## Root Cause

The gate executes in middleware; the router honors an internal header that
marks a request as an already-processed middleware subrequest, so an external
request spoofing that marker never reaches the gate's redirect branch
[R-104..R-106 vs R-107..R-109].

## Evidence

| Arm | Request | Result | Records |
|---|---|---|---|
| Baseline | GET /admin | 307 → /login, 412B | R-101..R-103 |
| Treatment | GET /admin + `X-Middleware-Subrequest: middleware` | 200, 5.3KB dashboard | R-104..R-106 |
| Control | GET /admin + `X-Noop-Value: middleware` | 307 → /login, 412B | R-107..R-109 |
| API baseline | GET /api/admin/users | 307 → /login | R-120 |
| API treatment | GET /api/admin/users + header | 200, JSON array | R-121..R-123 |

Reproduction: n_runs 3 per arm, byte-identical deltas across runs
(deterministic).

## Impact

See the impact chain and canary round-trip in Phase 4 above — protected page
and API content return to anonymous users [R-106, R-122, R-123]; the
recovered marker was the self-planted `MYTHOS-CANARY-9f2c7b41` [R-020, R-122].

## Reproduction Steps

```bash
# Baseline (expect 307):
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:3100/admin
# Treatment (expect 200 on an unpatched 14.2.5 lab):
curl -s -o /dev/null -w '%{http_code}\n' -H 'X-Middleware-Subrequest: middleware' \
  http://127.0.0.1:3100/admin
# Control (expect 307 — proves header-name specificity):
curl -s -o /dev/null -w '%{http_code}\n' -H 'X-Noop-Value: middleware' \
  http://127.0.0.1:3100/admin
```

Run each arm three times; deltas are deterministic on this lab build.

## Suggested Remediation

Derived from the observed mechanism, not pasted from a checklist: upgrade the
framework to ≥ 14.2.25 [R-002], or — if upgrade latency is unavoidable — strip
`X-Middleware-Subrequest` from all inbound requests at the fronting proxy, and
add a regression test asserting the header cannot reach the router from
outside.

## Leads Appendix (research capital, not trash)

- H-003 (INCONCLUSIVE): timing side channel at login — parked with resume
  point P-001; next step is a LAN-facing re-measurement with a resolution
  floor. [R-116..R-118]
