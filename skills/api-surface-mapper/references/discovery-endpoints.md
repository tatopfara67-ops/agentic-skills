# Discovery Endpoints & Inventory Schema

## The bounded sweep list (what api_introspect probes)

`/openapi.json` · `/swagger.json` · `/swagger/v1/swagger.json` · `/api-docs`
· `/api-docs.json` · `/v1/api-docs` · `/v2/api-docs` · `/api/openapi.json`
· `/api/swagger.json` · `/api/v1/openapi.json` · `/graphql` · `/graphiql`
· `/playground` · `/altair`

That is the whole list. If none hit, the API inventory proceeds from JS
extraction and version probes — the sweep does not grow speculatively.

## Endpoint inventory schema (one row per method-path pair)

| Field | Source |
| --- | --- |
| method + path | spec or probe |
| parameters: name, type, required, location (query/body/path/header) | spec |
| auth marking: anonymous / session / token / unknown | spec security field + probe verdict |
| version | path prefix or spec info.version |
| documented: yes / no (JS-only) | spec-vs-JS cross-reference |
| deprecated_candidate: yes / no | version diff evidence |
| evidence: R-NNN list | spec artifact record + probe record |

## Parameter taxonomy for hypothesis generation

| Parameter shape | Phase-2 hint |
| --- | --- |
| Object identifiers (`id`, `uuid`, `ref`) | IDOR/BOLA differential (auth-boundary-mapper) |
| Free-text reflected in responses | injection + XSS contexts |
| URL/hostname-shaped (`url`, `callback`, `webhook`, `redirect`) | SSRF / open-redirect |
| Numeric quantity/price/limit | business-logic arithmetic |
| File/attachment pointers | upload/file-storage abuse |
| Version/format selectors (`format=json\|xml`, `fields=`) | smuggling/mass-assignment shapes |

## Version-diff procedure

1. From evidence, list version prefixes present (spec info, JS paths,
   response headers like `api-version`).
2. Probe the SAME endpoint across versions, one request each.
3. A 200 on an old version where the current spec dropped the endpoint →
   `deprecated-endpoint` candidate, note the version pair.
4. Record both probe results; the pair IS the evidence — neither alone
   earns the class.
