# Takeover Verification & Storage Bounds

## Verifying a takeover candidate (record pairs only)

From subdomain-hunter, a candidate arrives as: in-scope name → CNAME →
third-party service host. This organ adds the second half of the pair:

1. `http_probe` the service host (and, where the provider documents it,
   the tenant-shaped path on that host).
2. Match the response against the provider signature table maintained in
   the subdomain-hunter organ's takeover reference (the shared table of
   dangling markers per provider).
3. Record the pair: CNAME-chain record + provider-marker record. Classify
   the surface `third-party-asset` with note `takeover-candidate`, and let
   Phase 2 write the hypothesis with a stated prior.
4. CONFIRMED "claimable" requires, at minimum, the marker pair plus a
   controlled check the OPERATOR performs by provisioning a no-op resource
   on their own account that answers the name — an explicit operator
   decision, recorded in the ledger before it happens. This organ never
   provisions anything itself.

CloudFront note (the most misreported class): require the viewer-error
shape AND an SNI/alias mismatch observation; cap the prior until both
exist. Azure/Azurewebsites claims: the error-code family in the marker
response is part of the evidence pair.

## Object-storage anonymous access (bounded)

| Step | Request | Record |
| --- | --- | --- |
| Baseline | GET bucket root with no credentials | FACT |
| Treatment | GET bucket root anonymous (same thing — this IS the anonymous check; baseline is the WITH-token round if any auth context exists) | EXPERIMENT |
| Control | GET with a garbage Authorization header | CONTROL |
| Bounded proof | read ONE page of the listing XML; save artifact; stop | SURFACE + attestation note |

Verdict grammar: `anonymous-list` (200 + ListBucketResult), `denied`
(403/404 with the provider's AccessDenied shape), `partial` (some prefixes
200, others 403 — record per-prefix, park the rest). Object-level
anonymity (GET on a named key) is a separate hypothesis per key family,
never a sweep.

## Hygiene header fact set

Record per main surface: CSP (full policy text to artifact), HSTS
(max-age), X-Frame-Options / frame-ancestors, X-Content-Type-Options,
referrer-policy, cookie attributes (Secure/HttpOnly/SameSite) on the
session cookie. These are FACTs; they become report content only when a
reachable sink (from xss-playbook or clickjacking-susceptible UI evidence)
pairs with the absence to form a mechanism.
