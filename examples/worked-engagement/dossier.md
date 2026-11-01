# Attack-Surface Dossier — mythos-lab-demo

Generated 2026-11-01T10:12:16Z from ledger records only; surfaces without evidence are structurally impossible (no-slop law).

- Surfaces registered: 11 (active 10, backlog 1)
- Authorization artifacts: self-owned lab declaration (lab/target_app.py)

## Asset graph

**127.0.0.1:8477**

- `http://127.0.0.1:8477/api/v0/debug` S-010 — debug-interface, priority 90, evidence R-521
- `http://127.0.0.1:8477/backup.zip` S-004 — backup-artifact, priority 85, evidence R-273
- `http://127.0.0.1:8477/api/v2/admin/metrics` S-008 — admin-console, priority 80, evidence R-536
- `http://127.0.0.1:8477/admin` S-003 — admin-console, priority 75, evidence R-016
- `http://127.0.0.1:8477/login` S-002 — auth-endpoint, priority 70, evidence R-019
- `http://127.0.0.1:8477/api/v2/admin/export` S-009 — api-rest, priority 65, evidence R-538
- `http://127.0.0.1:8477/api/v1/users` S-007 — api-rest, priority 60, evidence R-537
- `http://127.0.0.1:8477/api/v1/invoices` S-011 — api-rest, priority 55, evidence R-539 (backlog)
- `http://127.0.0.1:8477/.env.example` S-005 — config-exposure, priority 50, evidence R-129
- `http://127.0.0.1:8477/` S-001 — web-app, priority 40, evidence R-005
- `http://127.0.0.1:8477/app.js` S-006 — static-content, priority 30, evidence R-520

## Priority queue

| ID | Surface | Class | Reachability | Priority | Evidence | Note |
| --- | --- | --- | --- | --- | --- | --- |
| S-010 | http://127.0.0.1:8477/api/v0/debug | debug-interface | reachable | 90 | R-521 | commented-out route, unloved +8; auth absent |
| S-004 | http://127.0.0.1:8477/backup.zip | backup-artifact | reachable | 85 | R-273 | archive artifact; robots.txt Disallow |
| S-008 | http://127.0.0.1:8477/api/v2/admin/metrics | admin-console | auth-gated | 80 | R-536 | 401 without session; auth-boundary +10 |
| S-003 | http://127.0.0.1:8477/admin | admin-console | login-gated | 75 | R-016 | 307 to /login; robots.txt Disallow |
| S-002 | http://127.0.0.1:8477/login | auth-endpoint | reachable | 70 | R-019 | auth-boundary +10 (scoring.md) |
| S-009 | http://127.0.0.1:8477/api/v2/admin/export | api-rest | auth-gated | 65 | R-538 | spec-only endpoint: absent from JS, unloved +8 |
| S-007 | http://127.0.0.1:8477/api/v1/users | api-rest | reachable | 60 | R-537 | public list endpoint; found via JS extraction |
| S-005 | http://127.0.0.1:8477/.env.example | config-exposure | reachable | 50 | R-129 | structure only, no live values |
| S-001 | http://127.0.0.1:8477/ | web-app | reachable | 40 | R-005 | entry page; links and bundle reference |
| S-006 | http://127.0.0.1:8477/app.js | static-content | reachable | 30 | R-520 | bundle; endpoint source for js-recon |

## Backlog (parked discoveries — R1)

- `http://127.0.0.1:8477/api/v1/invoices` S-011 — api-rest, evidence R-539 — parked: needs two test accounts (R2)

## Phase 2 gate

Every active surface above needs at least one pre-registered hypothesis (H-record) or an explicit why-not note before Phase 3 testing opens — no surface is left hypothesis-less.
