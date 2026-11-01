# Engagement Report — mythos-lab-demo

Authorization: self-owned lab declaration, scope.csv row 127.0.0.1 (AUTH R-001).

## Surfaces

| ID | Surface | Class | Priority | Evidence |
| --- | --- | --- | --- | --- |
| S-001 | http://127.0.0.1:8477/ | web-app | 40 | R-005 |
| S-002 | http://127.0.0.1:8477/login | auth-endpoint | 70 | R-019 |
| S-003 | http://127.0.0.1:8477/admin | admin-console | 75 | R-016 |
| S-004 | http://127.0.0.1:8477/backup.zip | backup-artifact | 85 | R-273 |
| S-005 | http://127.0.0.1:8477/.env.example | config-exposure | 50 | R-129 |
| S-006 | http://127.0.0.1:8477/app.js | static-content | 30 | R-520 |
| S-007 | http://127.0.0.1:8477/api/v1/users | api-rest | 60 | R-537 |
| S-008 | http://127.0.0.1:8477/api/v2/admin/metrics | admin-console | 80 | R-536 |
| S-009 | http://127.0.0.1:8477/api/v2/admin/export | api-rest | 65 | R-538 |
| S-010 | http://127.0.0.1:8477/api/v0/debug | debug-interface | 90 | R-521 |
| S-011 | http://127.0.0.1:8477/api/v1/invoices | api-rest | 55 | R-539 |

## Hypotheses

### H-001 — Unauthenticated debug-interface route (facts R-521, R-536)

- claim: If /api/v0/debug is mounted without authorization, then an unauthenticated GET returns diagnostic content while /api/v2/admin/metrics returns 401.
- facts: R-521, R-536
- prior: 70% — debug remnants frequently lose their gate (base rate from public advisory patterns)
- falsifier: /api/v0/debug answering 401 exactly like the console endpoints
- Closure: CONFIRMED (E-001: R-542 R-545 R-548; closure R-550)

### E-001 — unauthenticated differential probe

- hypothesis: H-001
- baseline: R-541 (401, 3/3 runs)
- treatment: R-542 R-545 R-548 (200 + diagnostic banner, 3/3)
- control: R-543 (404, 3/3 — same effort, wrong knob)
- n_runs: 3
- delta: treatment 200 vs baseline 401, stable across runs; control 404 proves the 200 is route-specific

## Impact

- impact-chain: unauthenticated read of the lab debug banner (treatment R-542); bounded to one response read, no further enumeration (records R-542, R-521)

- severity: low (records R-542, R-521) — diagnostic banner exposure on a self-owned lab surface

- canary attestation: engagement touched only the self-owned mythos-lab and self-injected markers; no real-user data involved (AUTH R-001)

## Leads

- S-011 /api/v1/invoices (parked: requires two test accounts; resume note in dossier backlog)
