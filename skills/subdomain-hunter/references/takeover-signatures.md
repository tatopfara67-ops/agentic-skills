# CNAME Dangling — Provider Signature Table

A takeover candidate needs TWO records before it earns a Phase-2 hypothesis:

1. **The chain**: CNAME from the in-scope name to a third-party service
   host (from `dns_resolve`).
2. **The marker**: the third-party host serves its "no such tenant /
   not configured" page (from `http_probe` of the service host — this
   probes the SERVICE, which you are verifying state on, not the target).

## Provider signatures

| Provider (CNAME shape) | Dangling marker to look for | Note |
| --- | --- | --- |
| Heroku (`*.herokuapp.com`) | "No such app" in body | Classic; custom-domain add-on flow |
| GitHub Pages (`*.github.io`) | 404 with GitHub chrome | Org/user page deleted |
| Shopify (`*.myshopify.com`) | "Sorry, this shop is currently unavailable" | |
| Azure (`*.cloudapp.azure.com`, `*.azurewebsites.net`) | 404 with Azure error code | Azurewebsites: check the exact subscription marker |
| AWS CloudFront (`*.cloudfront.net`) | error "Bad request" / viewer-error page with x-amz-cf-id header present | Claim requires SNI mismatch evidence; note carefully |
| Fastly (`*.fastly.net`) | Fastly "please contact support" 500-style page | |
| Pantheon (`*.pantheonsite.io`) | "The gods have left Olympus" style 404 | |
| Tumblr (`*.tumblr.com`) | "There's nothing here." | |
| WordPress VIP / wpengine (`*.wpengine.com`) | "The site you were looking for…" | |
| Zendesk (`*.zendesk.com`) | help-center "not found" page | |
| Helpjuice/HelpScout/Ghost/Readme style SaaS hosts | their branded 404 tenant page | pattern: branded 404 + tenant in CNAME |

Rules of the table:

* The marker text is a HYPOTHESIS about the provider's state, not proof —
  providers change wording. The record pair (CNAME + marker response) is
  what earns the hypothesis; claiming "takeover confirmed" additionally
  requires the Phase-3 canary discipline (a harmless marker of our own),
  which for takeover means: do NOT register the dangling resource during
  recon. Registration proofs are operator decisions outside this skill.
* CloudFront claims are the most misreported class in public reports.
  Require the x-cache error shape AND an SNI mismatch observation, and set
  a low prior until a controlled check exists.

## Procedure

1. `dns_resolve` the in-scope name; note any CNAME leaving the parent domain.
2. Classify the target host against the table (shape match).
3. `http_probe` the service host (scheme from the provider's default).
4. Record both observations as FACT records.
5. If both exist and the marker matches: `dossier_add` with class
   `third-party-asset`, note `takeover-candidate`, priority ≥ 70, and a
   Phase-2 hypothesis per the spine's grammar.
