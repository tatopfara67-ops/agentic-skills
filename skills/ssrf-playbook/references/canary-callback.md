# Canary Callback — Channel-Existence Protocol

## The interaction host

Any endpoint the operator owns and can read logs from: a rented VPS with
a tiny request logger, a self-hosted webhook collector, or a commercial
interaction client whose session belongs to the operator. What matters:

1. The host is operator-owned (the canary doctrine's "marker we own").
2. Every request is logged with: path, query, headers of interest, time.
3. A unique marker per hypothesis: `MYTHOS-CANARY-<uuid4>` — never reuse a
   marker across hypotheses; the marker IS the linkage between the
   treatment request and the callback record.

## The round-trip, as records

```
R-301 | EXPERIMENT | http_probe | POST /fetch url=http://HOST/c/H-012-MYTHOS-CANARY-<uuid> | 202
R-302 | CANARY     | operator-log | callback GET /c/H-012-MYTHOS-CANARY-<uuid> | received
R-303 | CONTROL    | http_probe | POST /fetch url=htxp://HOST/invalid-<uuid> | 400
```

H-012 closes CONFIRMED only on the (R-301, R-302) pair with the SAME
marker, and the control R-303 showing the channel is not "callback on any
input". Callbacks arriving for markers we never sent are recorded as
FACTs and investigated as infrastructure noise, not findings.

## Callback interpretation table

| Observation | Meaning |
| --- | --- |
| Marker callback, control silent | channel exists — proceed to scheme matrix |
| Callback for control too (invalid URL still fetched) | fetch is lenient; narrow the falsifier, re-run |
| No callback, but response echoes fetch errors per-URL | blind-ish channel: error oracle replaces the callback; reclassify the oracle |
| DNS-only callbacks (host resolved, no HTTP) | resolver-level SSRF; record, re-hypothesize mechanism |
| Delayed callbacks | queueing; note latency in the CANARY record |

## Scheme matrix (one request per row)

`http`, `https`, `localhost`(name), `127.0.0.1`, `[::1]`, scheme-less
`//HOST`, userinfo `http://canary@HOST`, decimal/obfuscated loopback only
when internal probing is IN named scope. Each row: treatment + callback
check + verdict cell in the engagement table.

## Redirect-chain probe

The operator's redirector answers the canary URL with a 30x to a SECOND
canary path (different marker). A callback on the second marker proves
redirect-following; combined with any redirect-influencable surface
(redirect-handler class), that pair becomes the Phase-4 impact story —
without ever pointing the chain at a third party.
