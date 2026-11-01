# Worked Engagement — mythos-lab-demo

Full Tier-1 pipeline plus one Phase-3 mini-cycle, executed by `scripts/run_worked_example.py` against the self-owned mythos-lab (`lab/target_app.py`, 127.0.0.1:8477). Every value below is a real tool output captured at run time.


## Phase 0 — Scoping


### scope_check('http://127.0.0.1:8477/')

```json
{
 "authorized": true,
 "reason": "authorized: class in_scope, artifact 'self-owned lab declaration (lab/target_app.py)'",
 "matched": "127.0.0.1",
 "class": "in_scope",
 "auth_artifact": "self-owned lab declaration (lab/target_app.py)"
}
```

### AUTH record

R-001 | 2026-11-01T10:12:03Z | operator | engagement scope declaration | self-owned lab declaration (lab/target_app.py) |  | AUTH | scope.csv row: 127.0.0.1 in_scope

### http_probe('http://93.184.216.34/') — out of scope

```json
{
 "refused": "R0/scope: target 'http://93.184.216.34/' matches no scope.csv row \u2014 deny-by-default. Add a row citing the authorizing artifact (bug-bounty scope page, engagement letter, or self-owned lab declaration) to unblock.",
 "ledger": "R-002 | 2026-11-01T10:12:03Z | scope-gate | target='http://93.184.216.34/' active=True | R0/scope: target 'http://93.184.216.34/' matches no scope.csv row \u2014 deny-by-default. Add a row citing the authorizing artifact (bug-bounty scope page, engagement letter, or self-owned lab declaration) to unblock. |  | REFUSED | gate refusal"
}
```

### capability inventory

R-003 | 2026-11-01T10:12:03Z | operator | capability inventory | stdlib http tools; no CLI arsenal installed |  | FACT | fallback ladder level: python3

## Phase 1 — Recon


### dns_resolve('127.0.0.1')

```json
{
 "addresses": [
  "127.0.0.1"
 ],
 "rid": "R-004"
}
```

### http_probe('/')

```json
{
 "status": 200,
 "size": 225,
 "rid": "R-005",
 "sha12": "82a5a3b91426"
}
```

### http_probe('/robots.txt')

```json
{
 "status": 200,
 "rid": "R-006",
 "note": "Disallow: /admin, /backup"
}
```

### http_probe('/sitemap.xml')

```json
{
 "status": 200,
 "rid": "R-007"
}
```

### content_discover(wordlist=default, exts=['','.zip','.example'], max=500)

```json
{
 "calibration": {
  "status": 404,
  "size_min": 49,
  "size_max": 49,
  "soft_404": false
 },
 "probes": 500,
 "findings": [
  {
   "path": "/robots.txt",
   "status": 200,
   "rid": "R-012"
  },
  {
   "path": "/sitemap.xml",
   "status": 200,
   "rid": "R-014"
  },
  {
   "path": "/admin",
   "status": 307,
   "rid": "R-016"
  },
  {
   "path": "/login",
   "status": 200,
   "rid": "R-019"
  },
  {
   "path": "/openapi.json",
   "status": 200,
   "rid": "R-051"
  },
  {
   "path": "/.env.example",
   "status": 200,
   "rid": "R-129"
  },
  {
   "path": "/backup.zip",
   "status": 200,
   "rid": "R-209"
  },
  {
   "path": "/backup.zip",
   "status": 200,
   "rid": "R-273"
  }
 ]
}
```

### js_analyze('/app.js')

```json
{
 "endpoints": [
  "/api/v2/admin/metrics",
  "/api/v1/users"
 ],
 "commented_routes": [
  "/api/v0/debug"
 ],
 "secret_hints": [
  {
   "kind": "generic-api-key",
   "masked": "MYTHOS\u2026(21 chars, masked; full value in artifact only)"
  }
 ],
 "surface_rid": "R-520"
}
```

### http_probe('/api/v0/debug') — from commented route

```json
{
 "status": 200,
 "size": 71,
 "rid": "R-521"
}
```

### api_introspect()

```json
{
 "found": [
  "/openapi.json"
 ],
 "openapi_paths": [
  "/api/v1/invoices",
  "/api/v1/users",
  "/api/v2/admin/export",
  "/api/v2/admin/metrics"
 ],
 "rid_artifact": "/home/z/my-project/download/mythos-arsenal/engagements/mythos-lab-demo/artifacts/api_openapi.json.body"
}
```

### http_probe('/api/v2/admin/metrics') — no session

```json
{
 "status": 401,
 "rid": "R-536"
}
```

### http_probe('/api/v1/users') + http_probe('/api/v2/admin/export')

```json
{
 "users": {
  "status": 200,
  "rid": "R-537"
 },
 "export": {
  "status": 404,
  "rid": "R-538"
 }
}
```

## Cartography — dossier


- `dossier_add` S-001 `http://127.0.0.1:8477/` web-app prio 40 (evidence R-005)

- `dossier_add` S-002 `http://127.0.0.1:8477/login` auth-endpoint prio 70 (evidence R-019)

- `dossier_add` S-003 `http://127.0.0.1:8477/admin` admin-console prio 75 (evidence R-016)

- `dossier_add` S-004 `http://127.0.0.1:8477/backup.zip` backup-artifact prio 85 (evidence R-273)

- `dossier_add` S-005 `http://127.0.0.1:8477/.env.example` config-exposure prio 50 (evidence R-129)

- `dossier_add` S-006 `http://127.0.0.1:8477/app.js` static-content prio 30 (evidence R-520)

- `dossier_add` S-007 `http://127.0.0.1:8477/api/v1/users` api-rest prio 60 (evidence R-537)

- `dossier_add` S-008 `http://127.0.0.1:8477/api/v2/admin/metrics` admin-console prio 80 (evidence R-536)

- `dossier_add` S-009 `http://127.0.0.1:8477/api/v2/admin/export` api-rest prio 65 (evidence R-538)

- `dossier_add` S-010 `http://127.0.0.1:8477/api/v0/debug` debug-interface prio 90 (evidence R-521)

### dossier_render()

```json
{
 "ok": true,
 "path": "/home/z/my-project/download/mythos-arsenal/engagements/mythos-lab-demo/dossier.md",
 "surfaces": 11,
 "active": 10,
 "backlog": 1,
 "hosts": [
  "127.0.0.1:8477"
 ]
}
```

## Phase 2–3 — hypothesis, experiment, closure


### H-001 pre-registration (EXPERIMENT record)

R-540 | 2026-11-01T10:12:16Z | operator | pre-register H-001 | claim: If /api/v0/debug is mounted without authorization, then an unauthenticated GET returns diagnostic content while /api/v2/admin/metrics returns 401. |  | EXPERIMENT | prior 70% — debug remnants frequently lose their gate; falsifier: /api/v0/debug returns 401 like the console endpoints

### E-001 differential (3 runs)

```json
{
 "baseline": [
  [
   "R-541",
   "401 Unauthorized"
  ],
  [
   "R-544",
   "401 Unauthorized"
  ],
  [
   "R-547",
   "401 Unauthorized"
  ]
 ],
 "treatment": [
  [
   "R-542",
   "200 OK"
  ],
  [
   "R-545",
   "200 OK"
  ],
  [
   "R-548",
   "200 OK"
  ]
 ],
 "control": [
  [
   "R-543",
   "404 Not Found"
  ],
  [
   "R-546",
   "404 Not Found"
  ],
  [
   "R-549",
   "404 Not Found"
  ]
 ]
}
```

### Closure record

R-550 | 2026-11-01T10:12:16Z | operator | closure H-001 | CONFIRMED: treatment 200 with diagnostic banner in 3/3 runs; baseline 401 in 3/3; control 404 in 3/3 |  | EXPERIMENT | delta stable; specificity proven by control

### ledger_merge()

```json
{
 "records_merged": 550,
 "total": 550
}
```

## Report + audit


### report.md written

/home/z/my-project/download/mythos-arsenal/engagements/mythos-lab-demo/report.md

### auditor/audit_report.py report.md

== audit: /home/z/my-project/download/mythos-arsenal/engagements/mythos-lab-demo/report.md
[ PASS ] no placeholder markers
[ PASS ] no hedging slop
[ PASS ] no ungated victory language
[ PASS ] all severity/class lines cite records
[ PASS ] 1 hypothesis block(s) closed
[ PASS ] 1 experiment card(s) carry reproduction data
[ INFO ] blocks: 1 hypotheses, 1 experiments
RESULT: PASS
exit=0
