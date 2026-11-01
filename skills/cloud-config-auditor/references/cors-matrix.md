# CORS Origin-Differential Matrix

## The three-request pattern (per endpoint under test)

| Round | Origin header sent | What it isolates |
| --- | --- | --- |
| Baseline | none | the endpoint's native behavior |
| Treatment | `https://evil-operator-host` (operator-owned domain) | does an ARBITRARY origin get reflected/allowed? |
| Control | `https://sub.target-domain` (a real subdomain of the target) | separates `*` / reflected-allow from deliberate subdomain allow-listing |

Read from the RESPONSE records: `Access-Control-Allow-Origin`,
`Access-Control-Allow-Credentials`, and (if the treatment also sent a
preflight) `Access-Control-Allow-Methods/Headers`.

## Verdict table

| ACAO on treatment | ACAC | Verdict | Impact shape |
| --- | --- | --- | --- |
| reflects evil origin | true | credentialed CORS misconfig | authenticated cross-origin reads (operator account proves it, canary data only) |
| `*` | false/absent | wildcard, unauthenticated | matters only when the endpoint serves non-public data without auth — pair with an auth-boundary fact |
| reflects evil origin | false | origin reflection without credentials | bounded impact; pair with token-in-URL or other ambient-leak hypothesis |
| subdomain only (control) | — | deliberate allow-list | check subdomain takeover/attacker-controllable subdomain separately; that chain is the real hypothesis |
| no ACAO anywhere | — | closed | record and move on |

## Preflight discipline

Only when the hypothesized attack needs a non-simple request: one OPTIONS
preflight with the treatment origin + the method/headers the attack needs.
The preflight response records complete the verdict row. No preflight
spam: one per hypothesis.

## Report grammar

Every CONFIRMED CORS claim cites: the three records, the operator-owned
origin used, and a bounded read proof (one canary response body read
cross-origin from the operator's page, captured as an artifact) — plus
the attestation that only the operator's own account/session was the
credentialed subject.
