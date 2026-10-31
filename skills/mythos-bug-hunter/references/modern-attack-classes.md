# Reference — Modern Attack Classes

> Part of **mythos-bug-hunter v4.2.0** (package architecture).
> **Load when:** Phase 2 hypothesis sources: HTTP request smuggling, cache poisoning/deception, single-packet race conditions, SSRF at the modern edge, framework-internal header bypasses, OAuth 2.1-era pitfalls.
> Authoritative rules, Canon, and pipeline contracts live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts with the
> SKILL.md Canon or contracts, **SKILL.md wins**. Section numbering below is
> inherited from the v4.0 monolith and is intentionally non-sequential.

---

## 23. Modern Attack Classes (2024-2026)

Each class below follows one structure: **model → hypothesis → validation
recipe → impact gate → false-positive traps**. All references in Appendix C.

### 23.1 HTTP Request Smuggling and Protocol-Edge Attacks

**Model.** Front and back tiers parse the same request differently
(Content-Length vs Transfer-Encoding, or HTTP/1.1 vs HTTP/2 framing). The
disagreement lets one physical request be interpreted as two ("CL.TE",
"TE.CL", "TE.TE" over HTTP/1.1; "H2.CL", "H2.TE" when an HTTP/2 front end
downgrades to an HTTP/1.1 back end). A related surface is `h2c` upgrade
smuggling: a proxy that forwards `Upgrade: h2c` lets attackers bypass the
WAF tier entirely and talk HTTP/2 straight to the back end.

**Hypothesis template.** "If the front tier uses `<framing A>` and the
back tier uses `<framing B>`, then sending a request with conflicting
framing should produce `<desync signal>` (timing differential, unexpected
400/502 from a follow-up request, or a poisoned next-user response)."

**Validation recipe.**
1. Identify the tier chain (§3.7): CDN? gateway? backend protocol?
2. Send benign differential probes only — a normal request, the same
   request with both CL and TE, an HTTP/2 request with a body — and
   compare status/timing/body across repeats.
3. Confirm desync with a **self-contained** two-request test where the
   second request's response reflects the smuggling effect (e.g. a
   shortened/smuggled prefix returning a distinctive 400).
4. Only within explicit authorization and policy: no poisoning of other
   users' responses in live programs; demonstrate on your own sessions.

**Impact gate.** Reportable when you demonstrate request-queue poisoning,
auth bypass, or cache poisoning chaining — not when a single 400 anomaly
appears.

**FP traps.** CDNs normalize conflicting framing (probe returns clean
400 — no desync); intermittent 502s from origin health, not desync;
timing noise (repeat per §12).

### 23.2 Web Cache Poisoning and Web Cache Deception

**Model.** Two distinct classes (PortSwigger taxonomy):
- **Cache poisoning** — an *unkeyed* input (a header or path component
  not part of the cache key) changes the stored response; other users
  then receive the poisoned response.
- **Cache deception** — the victim is tricked into requesting a sensitive
  dynamic page under a path that cache rules treat as static (classic:
  `/account/nonexistent.css`); the cache stores the private response and
  the attacker fetches it.

**Hypothesis templates.**
- "If header X is unkeyed and reflected/used in the response, then two
  requests differing only in X should both be `X-Cache: HIT` on the same
  key with different bodies."
- "If the cache stores paths with static extensions and the origin routes
  `/account/anything.css` to `/account`, then a cache-buster request
  under my own session should return *my* private page from cache to an
  unauthenticated follow-up."

**Validation recipe.**
1. Identify cache keys/rules: vary each candidate element; watch
   `X-Cache`, `Age`, `X-Cache-Status`, `CF-Cache-Status`.
2. Use a cache buster (unique query param) on every probe so you never
   poison real users during testing.
3. Poisoning: prove with your own two-session setup that user B receives
   the response user A's input generated. Deception: prove the cached
   private content is retrievable by the attacker identity.
4. Explore discrepancy classes for deception: path mapping, delimiters,
   delimiter decoding, normalization (cache vs origin).

**Impact gate.** Poisoning: another user demonstrably receives your
injected content. Deception: another user's private data retrieved from
cache. Length/timing deltas alone are not impact.

**FP traps.** `Age`/`X-Cache` from intermediate hops (verify which tier);
personalization (per-user cached variants); the origin 404ing the
deception path (no cache rule matched); CPDoS-style effects — usually
availability impact, check program policy.

### 23.3 Race Conditions (Single-Packet Era)

**Model.** Time-of-check-to-time-of-use gaps in endpoints that perform a
check-then-write (balance, stock, coupon, vote, invite quota, follow
limits). Modern tooling collapses network jitter: the **single-packet
attack** (PortSwigger, Black Hat USA 2023) completes multiple HTTP/2
requests inside one TCP packet so they are processed near-simultaneously;
on HTTP/1.1, **last-byte synchronization** achieves the same by holding
final bytes and releasing them together.

**Hypothesis template.** "If endpoint E validates state before writing
without locking, then N concurrent copies of the request should produce
more than the permitted number of successful effects."

**Validation recipe.**
1. Baseline: single request → 1 success; the limiting rule identified.
2. Concurrency: send N (start with 2, then 5, 20) near-simultaneous
   copies — HTTP/2 single-packet (Turbo Intruder or equivalent) where
   available, last-byte sync otherwise (§26.8 tool notes).
3. Count *effects*, not responses: rows created, units consumed, emails
   sent. Response-body "success" claims are validated against actual
   state (query the resource afterwards).
4. Repeat ≥3 times; a one-off double-spend is a weak signal.
5. Multi-endpoint races: pairing two different endpoints (e.g. transfer +
   change-email) with interleaved timing.

**Impact gate.** Demonstrated overdraw/multi-effect beyond the business
rule. A single duplicated effect once, unreproducible, is not.

**FP traps.** Idempotency keys doing their job (all-but-one 409s — secure
behavior); message queues making effects *eventually* single (check final
state after settling, not immediate responses); rate limiting turning the
race into a 429 test (§12.2).

### 23.4 SSRF at the Modern Edge

**Model.** Server-side fetch of a URL you control or influence. Modern
entry points beyond classic "import from URL": **AI features** (link
preview generators, LLM web-browsing tools, RAG fetchers, agent URL
tools), webhook validators, PDF/image renderers, SSO metadata fetch
(OIDC `/.well-known` config URLs), OAuth avatar import.

**Hypothesis template.** "If feature F fetches attacker-supplied URLs
server-side without an egress allow-list, then a canary URL
(`http://<canary-host>/<unique-token>`) supplied through F should produce
a canary hit, and internal targets (`http://169.254.169.254/...`) should
produce a differential response vs a blocked control."

**Validation recipe.**
1. Out-of-band confirmation first: canary (interact.sh / Burp
   Collaborator or equivalent) — record the DNS/HTTP hit.
2. Then internal reachability *differentially*: response to
   `http://127.0.0.1:<port>/` vs `http://127.0.0.1:<closed-port>/`
   (timing + status), metadata endpoint vs blocked control.
3. For AI surfaces: separate "the model *talks about* fetching" (no
   effect) from "the tool actually fetched" (canary hit) — §24.

**Impact gate.** Internal resource access demonstrated (response content
or reliable timing/status differential), or canary hit plus an internal
target confirmed. A canary hit alone with zero internal reachability is
usually informational in modern programs.

**FP traps.** Client-side previews (fetch happens in the browser, not the
server); sandboxed egress proxies (canary hits from scanner IPs, not the
target); DNS rebinding defenses (IMDSv2-style session tokens on cloud
metadata make the classic 169.254.169.254 path far less impactful on
modern AWS — check the provider).

### 23.5 Framework-Internal Header Bypasses (Next.js Pattern)

**Model.** Frameworks use internal headers/flags to manage request
lifecycle. If an externally-supplied header can set an internal state, the
framework's own logic (including middleware-based authz) can be skipped.
Canonical case: **CVE-2025-29927** (Next.js, published 2025-03-21) —
supplying `x-middleware-subrequest` with the middleware path made Next.js
treat the request as an internal subrequest and bypass middleware
entirely; patched in 12.3.5 / 13.5.9 / 14.2.25 / 15.2.3. Self-hosted
`next start` deployments relying on middleware for auth were affected;
Vercel/Netlify/static-export deployments were not.

**Hypothesis template.** "If this app is self-hosted Next.js <14.2.25 /
<15.2.3 and enforces authz in middleware only, then GET /admin with
`x-middleware-subrequest: middleware` should return the protected page."

**Validation recipe.**
1. Fingerprint Next.js (version hints in headers/static assets; `next
   start` deployments).
2. Identify a middleware-protected route (one that redirects without a
   session).
3. Replay with the bypass header (variants: `middleware`,
   `pages/_middleware`, `src/middleware`; on 15.x the
   `MAX_RECURSION_DEPTH` form).
4. Differential: same route without the header (control) must still
   redirect. Confirm the bypass actually yields protected *data or
   action*, not just a 200 shell page.

**Impact gate.** Protected functionality actually reached. A 200 that
renders a client-side shell which still fails its own API authz is not a
bypass of impact.

**FP traps.** Patched versions; middleware that only does logging;
authz ALSO enforced in route handlers (defense in depth — the app is not
vulnerable even if middleware is skipped); managed hosting unaffected.

### 23.6 OAuth 2.1-Era Pitfalls

**Model.** Authorization-code flow issues that survive into modern
deployments.

| # | Class | Hypothesis | Signal |
|---|---|---|---|
| 1 | `redirect_uri` validation flaws | Prefix/pattern matching can be subverted (`https://app.example.com/.attacker.com/`, open redirect inside the app completing the chain) | code/token delivered to attacker-controlled destination |
| 2 | Missing `state` | CSRF on the OAuth handshake | victim's provider session linked to attacker's app account (login CSRF / session fixation) |
| 3 | PKCE downgrade | Public client omits PKCE or accepts `code_challenge` removed mid-flight | code interception usable |
| 4 | Token mix-up | App accepts tokens from multiple IdPs without `iss`/`aud` pinning | token from IdP A accepted by app expecting IdP B |
| 5 | Implicit/token-in-URL remnants | Tokens in URLs leak via Referer/logs | token observed in a Referer header |
| 6 | IdP metadata SSRF | Configurable issuer/metadata URL fetched server-side | canary + internal differential (§23.4) |

**Validation recipe.** Every row is a differential: complete the flow
normally (baseline), then the mutated flow (test), with a deliberately
broken variant as control. Authorization-server interactions must respect
the program's scope and the IdP's own terms.

**Impact gate.** Account takeover, token theft, or cross-tenant linkage
demonstrated. "Flow allows downgrade but no intercept path exists" is a
hardening note.

**FP traps.** IdPs enforcing exact redirect match (probe returns
`invalid_redirect_uri` — secure); `state` present but not validated
(check both); pre-prod IdP configurations in scope confusion.

---
