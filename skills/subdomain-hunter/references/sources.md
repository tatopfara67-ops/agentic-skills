# Source Ladder & Permutation Set

## Passive source ladder (cheapest first)

| Rung | Source | Notes |
| --- | --- | --- |
| 1 | Certificate transparency (`ct_subdomains`) | Public DB, no target contact |
| 2 | subfinder / amass -passive via `arsenal_route` | Aggregates many passive APIs; needs API keys configured by the operator, out of band |
| 3 | DNS zone hints: NS/SOA/MX on the parent | `dns_resolve` + manual SOA walking only when authorized for zone transfer — never attempt AXFR outside explicit scope |
| 4 | Search-engine-style archives (wayback) | Read public archives, not the target |
| 5 | Permutation + resolution | DNS-side; still no HTTP flood |

## Permutation generator

Apply to every known label; resolve all products (bounded: cap at a few
hundred per engagement, record the cap):

* Prefixes: `dev`, `staging`, `stage`, `test`, `qa`, `uat`, `prod`, `internal`,
  `intra`, `admin`, `api`, `app`, `www2`, `beta`, `demo`, `edge`, `gateway`,
  `auth`, `sso`, `cdn`, `assets`, `static`, `mail`, `docs`, `status`, `vpn`
* Joins: `LABEL-word`, `word-LABEL`, `LABELword`, `LABEL.word` (dot only when
  the parent uses dotted conventions)
* TLD widening only inside scope: if scope covers `example.com`, candidates
  like `example.co` are OUT of scope unless the scope row says otherwise —
  the gate enforces this mechanically anyway.

## Deduplication rules

* Names are lowercased, leading `*.` stripped, trailing dots stripped.
* A name resolving to the same A record as an existing surface is one
  surface with an alias note, not two surfaces.
* Non-resolving candidates are recorded as FACTs (negatives are observations)
  and never re-resolved in the same engagement.

## Rate courtesy

The permutation round resolves via the configured resolver, not the
target's authoritative servers directly. Keep it boring: small batches,
no parallel flood. The point is coverage, not speed.
