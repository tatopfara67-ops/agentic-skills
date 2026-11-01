# The 21-Class Surface Taxonomy

Every surface gets exactly one class. When two classes argue, the more
specific wins. When no class fits, that is a taxonomy gap — record the
surface as `web-app` with a note describing the gap; do not invent class
strings (the `dossier_add` tool rejects them anyway).

| Class | Definition | Typical evidence |
| --- | --- | --- |
| `static-content` | Served bytes with no server-side execution | 200 + content-type text/html on marketing pages, docs |
| `web-app` | Interactive application surface, unclassified | Parameterized URLs, forms, sessions |
| `api-rest` | REST-style JSON/HTTP interface | Path patterns `/api/vN/...`, JSON bodies, openapi spec |
| `api-graphql` | GraphQL endpoint | POST `/graphql` with introspection success |
| `api-rpc` | RPC/JSON-RPC/SOAP/gRPC-gateway | `method`-style bodies, `/rpc`, proto reflections |
| `admin-console` | Privileged interface | `/admin`, `/console`, 307-to-login on admin paths |
| `auth-endpoint` | Login, token issuance, password reset | `/login`, `/oauth`, `/token` |
| `file-storage` | File serving/storage surface | `/uploads`, `/files`, object-store paths |
| `redirect-handler` | Redirector surface | 30x with Location under operator control |
| `upload-endpoint` | Accepts file input | multipart forms, PUT to file paths |
| `websocket` | WS endpoint | `/ws`, upgrade headers |
| `job-worker` | Background job surface | `/jobs`, `/queue`, cron-styled paths |
| `email-handler` | Mail-flow surface | `/webhook` receiving mail events, unsubscribe handlers |
| `payment-flow` | Money movement | `/checkout`, `/billing`, coupon endpoints |
| `search` | Query interface | `/search`, `?q=` with reflected results |
| `debug-interface` | Diagnostic remnant | `/debug`, `/trace`, actuator endpoints, verbose errors |
| `deprecated-endpoint` | Old version left mounted | `/api/v0`, commented-out routes in JS |
| `backup-artifact` | Backup left reachable | `backup.zip`, `.bak`, `dump.sql` |
| `config-exposure` | Configuration reachable | `.env`, `config.json`, `Dockerfile` served |
| `third-party-asset` | External dependency surface | CDN scripts, third-party iframes, OAuth IdP |
| `ai-agent-surface` | AI/LLM endpoint or agent tool surface | `/chat`, `/completions`, MCP-style tool routes |

## Disambiguation rules

1. **api-rest vs api-rpc**: if requests carry resource paths and HTTP verbs,
   it is `api-rest`; if they carry method names in bodies, it is `api-rpc`.
2. **backup-artifact vs config-exposure**: archives of anything = backup;
   live configuration values = config exposure. `db.sql` dumped is both —
   classify `backup-artifact`, note the config content.
3. **admin-console vs auth-endpoint**: the door is `auth-endpoint`; what the
   door guards is `admin-console`.
4. **deprecated-endpoint vs debug-interface**: old-but-functional business
   routes are deprecated; diagnostic-only routes are debug.
5. **ai-agent-surface**: any endpoint where the server reasons or executes
   model output — includes MCP tool routes exposed over HTTP.

## Worked classification examples

* `/api/v0/debug` found in a commented-out JS route → `debug-interface`
  (diagnostic nature beats version age).
* `backup.zip` returning 200 during calibrated discovery → `backup-artifact`.
* `.env.example` returning 200 → `config-exposure` (structure without
  secrets; still inventory — it maps what the app expects).
* `/api/v2/admin/metrics` in an openapi spec, marked 401 → `admin-console`
  (it is the metrics face of the console).
* `app.js` served from a CDN host → `third-party-asset` on that host, and
  the endpoints inside it are surfaces on the app host once probed.
