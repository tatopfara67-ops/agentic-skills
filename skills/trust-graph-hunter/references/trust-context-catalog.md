# trust-context-catalog.md — edges, signal classes, and the forgery matrix

Load when enumerating trust edges or designing a deception
differential.

## 1. The Edge Inventory (template — one FACT record per edge)

```
EDGE-<k>: <component A> --trusts--> <component B>
  signal: <what A accepts as proof of B>
  class: network | request-context | application | identity
  capability: <what the trust grants>
  producer: <who can legitimately produce the signal>
  zone: <inside which network/trust boundary the check runs>
```

## 2. Signal Classes (with typical forgery surfaces)

| Class | Signals | Typical forgery surface |
| --- | --- | --- |
| network-position | IP allowlists, mTLS client certs, VPC/private-subnet assumption | X-Forwarded-For trust chain, SSRF-originated requests, spoofed source where no ACL verifies |
| request-context | Referer, Origin, Host, port, scheme | client-controllable headers honored by origin |
| application-context | X-Internal/X-Debug/X-Forwarded-* custom headers, webhook HMAC signatures, shared secrets, callback URLs | headers forwarded from the edge; unsigned/weakly-signed callbacks; secrets leaked in artifacts |
| identity-context | JWT issuer/audience assumptions, server-to-server tokens, API keys with implicit role | token reuse across zones; aud/iss not enforced; key scope escalation |

## 3. The Forgery Matrix (priority scoring)

For each edge, answer three yes/no questions — the edge's priority
is how many are yes:

1. **Producible outside?** Can the signal be produced from where
   an external attacker actually stands (public internet /
   authenticated low-privilege user)?
2. **Unverified?** Does the checking component verify the signal's
   provenance (ACL, signature check, mTLS handshake) or merely
   read it?
3. **High-yield capability?** Does the granted capability cross a
   trust zone (internal reach, service identity, elevated role)?

3/3 edges go first; edges scoring 1 are parked with a note. Record
the score in the edge inventory — the priority queue is then
auditable.

## 4. Deception Differential (the pre-registration template)

```
DECEIVE-<k>: edge-<k> — "signal S forgeable by P grants capability C"
  baseline   : legitimate context via operator's trusted component
               (e.g. real internal request through A)          -> R-NNN
  treatment  : same capability request, forged S, sent from
               OUTSIDE the trust zone                          -> R-NNN
  control    : same request, unrelated wrong context (wrong
               header value / wrong signature)                 -> R-NNN
  prediction : treatment matches baseline class => context is
               decoration; control differs => the check reads S
  falsifier  : treatment rejected like control => edge holds
  bound      : ONE inherited-privilege action, canary-tagged
```

## 5. Chain Archetypes Involving Forged Trust

* **Webhook authority borrowing.** Unsigned/weak callback honored
  as a trusted event → action executed with service privileges.
* **Internal-header decoration.** X-Internal honored from outside
  → debug/admin surface reachable pre-auth.
* **Referer-gated capability.** Authorization decided by Referer →
  privileged action from any origin.
* **SSRF-as-trust-confusion.** Server trusts its own outbound
  request to reach internal-only endpoints (bridge: ssrf-playbook).
* **Token zone-crossing.** Server-to-server token accepted from
  user-controlled sessions → service identity inherited.
* **Position laundering.** Forged edge grants internal reach →
  second bug inside the zone (bridge: chain-architect).

## 6. Anti-patterns (MISTAKE records)

* Attacking an edge whose far end is out of scope — identify,
  report, never execute (hard rule 1).
* "It accepted my header" without the control request — a LEAD,
  not a finding (hard rule 3).
* Testing the graph edge-by-edge without drawing it first — the
  compound chains live in the graph's transitivity, and the report
  requires the graph anyway (hard rule 5).
* Any technique that touches a human being — out of the organ's
  boundary entirely (hard rule 2).
