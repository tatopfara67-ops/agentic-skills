# Reference — Auth And Http Playbook

> Part of **mythos-bug-hunter v4.5.0** (package architecture).
> **Load when:** Phase 2-3: authorization testing matrix (actor-resource-action), HTTP status-code 12-step diagnosis, header-probe catalog, authentication/session flow and JWT attack catalog.
> Authoritative rules, Canon, and pipeline contracts live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts with the
> SKILL.md Canon or contracts, **SKILL.md wins**. Section numbering below is
> inherited from the v4.0 monolith and is intentionally non-sequential.

---

# Part IV — Target Playbooks

## 20. Authorization Testing

The highest-value category in web/API bug bounty, and the easiest to do
badly. Use the Actor → Resource → Action model; run the matrix.

### 20.1 Actor → Resource → Action

For every authorization test, define explicitly:

```
ACTOR:    who is requesting — anonymous / user A (role) / user B (role,
          tenant) / admin / an AI agent acting under user A's token
RESOURCE: what is acted upon — user B's invoice (id=200), admin endpoint
          /api/admin/users, tenant Y's data, another user's file
ACTION:   what is attempted — READ (GET) / CREATE (POST) / UPDATE
          (PUT/PATCH) / DELETE (DELETE) / EXECUTE (action endpoint)
```

### 20.2 Systematic Test Matrix

Each row is a separate TODO with baseline + control + test (§8 axis D).

| # | Transition | Hypothesis (abbreviated) | Secure signal | Violation signal |
|---|---|---|---|---|
| A | Anonymous → protected resource | Authn missing on this route | 401/403 | 200 with data |
| B | User A → user B's object (horizontal) | Object-level authz missing | 403/404 | 200 with B's data |
| C | User → admin function (vertical) | Function-level authz missing | 403 | 200 / admin action performed |
| D | Same-role user across tenants | Tenant isolation missing | 403/404 | 200 with tenant Y data |
| E | Low-priv → high-priv endpoint | Privilege escalation via direct access | 403 | 200 / privileged effect |
| F | Object id manipulation | Ids predictable/enumerable AND authz missing | 403/404 on foreign ids | 200 on foreign ids |
| G | UI-hidden function | UI hiding ≠ server enforcement | 403 on direct API call | Action executes |
| H | Per-object variance | Authz enforced on some objects only | consistent 403/404 | mixed 200s across ownership |
| I | HTTP method variation | Enforcement on GET but not PUT/PATCH/DELETE | 403 across methods | 200 on alternate method |
| J | Alternate path/representation | Enforcement differs on /v2/, /internal/, case, trailing slash, encoding, `?id=` vs `/id` | consistent enforcement | bypass via variant |
| K | Write authz | Read enforced, write missing | 403 on writes | A modifies B's object |
| L | Cross-account action on shared resources | Missing per-owner authz on comments/files | 403 | A deletes/edits B's item |
| M | GraphQL field-level authz | Resolver checks the query, not each field | sensitive field blocked/null | sibling field leaks B's data |
| N | Middleware variance (framework edge) | Authz lives in middleware, not the handler; middleware is skippable via framework-internal mechanics (e.g. Next.js `x-middleware-subrequest`, §23.5) | handler enforces too | protected route reachable with the bypass header |
| O | Content-type/method-ignore | Authz on JSON body but bypassed via multipart/form or absent body parse | consistent enforcement | 200 via alternate encoding |
| P | Agent identity (AI surface) | The AI agent acts with the user's token; tool calls are not scoped per action | tool enforces caller scopes | agent performs action the user cannot do directly |

### 20.3 Discipline

- Capture baseline (own resource), control (non-existent resource), and
  test (foreign resource) for every row executed.
- A 403 on the test request is an observation of access-control behavior —
  investigate consistency, differential, alternates (section 21); never
  conclude "authorization is secure" from one 403.
- Bypass probes need a hypothesis grounded in observed behavior (§11).
  "Try X-Original-URL" is noise; "the router dispatches on
  X-Original-URL while authz checks the original path" is a hypothesis.
- Reference mapping: WSTG-ATHZ-01/02; OWASP API1:2023 (BOLA) and
  API5:2023 (BFLA); OWASP A01:2025.

---

## 21. HTTP Status Code Playbook

Status codes are the most common reason AI testers give up prematurely.
This section is the antidote — the single source of truth for non-2xx
diagnosis.

### 21.1 General Rule

```
STATUS CODE = OBSERVATION, not VERDICT
```

A non-2xx never means "endpoint cannot be tested", "testing failed",
"no vulnerability", or "access is secure" until the diagnosis below has
run.

### 21.2 The 12-Step Diagnosis

Run in order; stop at the first step that resolves the situation.

```
1. SCOPE          — is the endpoint in-scope? If not: stop.
2. BASELINE       — was the request itself valid (host, path, method,
                    content-type, required headers)? Fix before interpreting.
3. AUTHN STATE    — token present? not expired? for the intended user?
4. AUTHZ STATE    — is the actor supposed to reach this resource? If not,
                    403 is the expected secure behavior → test the boundary
                    (section 20), not the status code.
5. RESPONSE ORIGIN— which tier answered (app / proxy / WAF / CDN / gateway /
                    middleware)? Record evidence (Server, Via, X-Cache,
                    CF-Ray, protocol version).
6. CONSISTENCY    — same response on repeats? Intermittent 403 → rate limit
                    or WAF heuristic; consistent → stable rule; differing
                    bodies → different rule sources.
7. DIFFERENTIAL   — does the response differ by actor / resource / method /
                    parameter? That difference is the signal (§8).
8. ALTERNATES     — alternate representations: /v1 vs /v2 vs /internal;
                    case; trailing slash; ?id= vs /id; URL-encoded forms;
                    each may be enforced differently.
9. SIBLING EVIDENCE — can a related endpoint prove the resource exists or
                    leaks behavior (verbose error on sibling, GraphQL query
                    for the same data)?
10. AC AS TEST    — the access-control behavior itself as the object of
                    study: does 403 leak existence (403 vs 404 differential)?
                    does it differ per role?
11. NEXT HYPOTHESIS — what next test yields a distinguishing signal?
                    None possible → only now consider stopping the branch
                    (§17.1).
12. RULES         — is the next test in-scope and policy-compliant? If not:
                    document and move on.
```

### 21.3 Per-Code Guidance

**401 Unauthorized** — authentication missing/invalid. Check token
presence, expiry, intended user. Do not conclude "authentication works"
from one 401: test whether endpoints that should require auth accept
anonymous requests (§20.2 row A).

**403 Forbidden** — authenticated, not authorized. This is the
access-control behavior itself: investigate consistency, differential,
alternates (§21.2 steps 5-10). Do not bypass without a hypothesis (§20.3).

**404 Not Found** — may be a real 404, an auth-gated 404, a soft-404 (app
returns 200 with a "not found" page), or method-dependent. Distinguish
hard vs soft 404 by comparing body, headers, and timing against a known
non-existent path; test other methods and auth states.

**405 Method Not Allowed** — the path exists; the method does not. This is
a signal the route is real: sweep other methods (§26.3) and test whether
enforcement differs by method (§20.2 row I).

**429 Too Many Requests** — respect it, back off, schedule retry. Note the
rate-limit behavior itself as a potential signal (per-user vs per-IP;
endpoint-specific vs global; characterize per §12.2). Never hammer.

**500 Internal Server Error** — a server-side error, not a vulnerability
by itself. Check: reproducible? leaks stack trace / internal paths / SQL?
input-dependent? A leaking 500 is an information-disclosure candidate
(OWASP A10:2025, Mishandling of Exceptional Conditions); a 500 that only
occurs on malformed input is usually a stability note, not a finding.

**502/503/504** — usually infrastructure. Note and move on unless a clear
security angle exists (e.g. the gateway's error page reflects input).

### 21.4 Header-Probe Catalog (hypothesis-first)

Only send these when a mechanism plausibly exists (observed router/proxy
behavior, stack fingerprint). Every probe is a hypothesis in §11 grammar,
not a spray:

| Probe | Hypothesis mechanism | Where seen |
|---|---|---|
| `X-Original-URL` / `X-Rewrite-URL` | Router dispatches on header path; authz checks request path | reverse-proxy setups |
| `x-middleware-subrequest: middleware` | Next.js internal recursion check bypasses middleware (CVE-2025-29927, §23.5) | self-hosted Next.js <14.2.25/15.2.3 |
| `X-Forwarded-For`, `X-Real-IP`, `X-Custom-IP-Authorization` | IP-based access control trusts spoofable headers | admin panels behind proxies |
| `X-Forwarded-Host` / `X-Host` | Host-derived URL generation (password-reset links, redirects) | password reset poisoning |
| `Content-Type` swap (JSON ↔ multipart) | Authz/parse path differs per parser | API gateways (§20.2 row O) |
| Path case/slash/encoding variants | Path normalization differs between tiers | caches, gateways (§23.1-23.2) |

**Forbidden:** treating any probe's outcome as terminal without the §21.2
diagnosis; probing without a mechanism hypothesis.

---

## 22. Authentication and Session Testing

### 22.1 Flow Checklist

- **Login** — response uniformity for valid/invalid users (user
  enumeration); error verbosity; rate limiting and lockout; timing
  differences between "no such user" and "wrong password".
- **Token lifecycle** — issuance, refresh (old token revoked on refresh?),
  revocation (logout invalidates server-side?), expiry enforcement (§20.2
  row A for expired/invalid tokens).
- **MFA/OTP flows** — is the OTP endpoint rate-limited? is the OTP space
  small enough to brute-force at the allowed rate (compute per §12)? do
  responses differ at the "code sent" step (phone/email enumeration)? does
  an expired code still verify? is the MFA check skippable by jumping
  directly to the post-MFA endpoint (§20.2 row N/G pattern)?
- **Password reset** — token entropy and single-use; uniform responses;
  reset-link host taken from `Host`/`X-Forwarded-Host` headers (reset
  poisoning); reset token returned in the response body; account takeover
  chain via email truncation/unicode.
- **Sessions** — fixation (id regenerated on login?); cookie flags
  (`Secure`, `HttpOnly`, `SameSite`) relative to what the cookie carries;
  concurrent-session policy on password change.

### 22.2 JWT Attack Catalog

Each row is a hypothesis template with its validation recipe. Only test
tokens you are authorized to handle.

| # | Technique | Hypothesis | Validation recipe | Notes |
|---|---|---|---|---|
| 1 | `alg=none` | Server accepts unsigned tokens | Flip header to alg:none, strip signature, keep claims | classic; mostly patched, still found |
| 2 | Algorithm confusion RS256→HS256 | Server verifies HS256 using the RSA **public** key as HMAC secret | Fetch public key (jwks endpoint), sign HS256 token with it | public key must be available to you |
| 3 | `kid` path traversal / injection | `kid` is used unsafely (path or SQL or command) | `kid: ../../dev/null` style probes with matching signature material; SQL error differentials | watch for SQLi in kid (error-based confirm) |
| 4 | `jku` header injection | Server fetches the JWKS URL from the token header | Host your own JWKS (authorized canary endpoint), point jku at it, sign with your key | requires outbound fetch by server = SSRF-flavored |
| 5 | `x5u` / `x5c` injection | Same as jku with X.509 URLs/certs | Same recipe with x5u/x5c | — |
| 6 | Embedded `jwk` header | Server trusts the key embedded in the token | Put your public key in jwk header, sign | — |
| 7 | Weak HMAC secret | HS256/HS384 signed with a guessable secret | Offline dictionary attack on a captured token (hashcat/john, authorized targets only) | never claim without recovering a secret |
| 8 | Expiry/audience/issuer ignored | Claims not enforced | Alter `exp` to past, `aud` to foreign value; observe acceptance | differential vs original token |
| 9 | Header parameter injection | Extra JWS header params confuse verifiers (JSWS-style confusion) | Add duplicate/conflicting header params | advanced; validate carefully |

**Discipline:** every JWT test is a differential (original token as
baseline, modified token as test, tampered-signature token as control that
MUST be rejected). A modified token that is accepted where the control is
rejected is the signal. Report the exact header/payload deltas verbatim.

---
