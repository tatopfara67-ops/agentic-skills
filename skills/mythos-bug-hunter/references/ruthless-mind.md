# Reference — Ruthless Mind

> Part of **mythos-bug-hunter v4.1.0** (package architecture).
> **Load when:** Phase 2 warzone drills: the nine principles, laziness mapping, extreme-input grammar, assumption destruction worksheet, cross-domain transplant matrix, dark-lab protocol.
> Authoritative rules, Canon, and pipeline contracts live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts with the
> SKILL.md Canon or contracts, **SKILL.md wins**. Section numbering below is
> inherited from the v4.0 monolith and is intentionally non-sequential.

---

## 32. The Ruthless Mind

Blackhat-grade thinking, whitehat-grade conduct. Everything in this section
happens *in the head first*: imagination has no legal boundary, packets do.
An idea becomes a request only after passing the authorization gate (§33.1)
and the prohibitions (§4); everything else stays on paper. "Ruthless"
describes the reasoning style — extreme, unconventional, unsentimental —
never the conduct.

### 32.1 The Nine Principles

1. **The application is lying to you.** Client-side validation is
   decoration; documentation is marketing; error messages are theater; UI
   flows are suggestions. Only server-verified behavior counts (§3.1,
   §3.3).
2. **Laziness mapping — the deadline oracle.** Tired developers cut corners
   where nobody looks, and corners are where bugs live. Enumerate where
   *you* would cut corners under deadline pressure, then probe those places
   first (§32.2).
3. **Inversion.** Do not ask "how do I get in?" — ask "how would I defend
   this with zero budget?", then attack the holes in that cheap defense. A
   WAF is a bouncer at the front door; smuggling walks in through the
   kitchen (§23.1).
4. **Assumption destruction.** List the application's implicit assumptions
   — IDs are sequential, one account per user, requests come from our app,
   JSON keys are unique, content-type tells the truth — then violate each
   one legally (§32.4).
5. **Cross-domain transplant.** Bug grammar is portable: request-smuggling
   logic reappears as GraphQL batching abuse; XSS reappears as MCP tool
   description injection; SSRF reappears as LLM fetch tools (§32.5).
6. **Least-effort economics.** Real attackers take the cheapest sufficient
   path — enumerate the five cheapest attacks before any clever one. A
   cheap attack that works is exactly what the blackhat would have used;
   that is the report that matters.
7. **Kill discipline.** A hypothesis is a tool, not a child. Posterior
   below its band (§10.4) → dead; no appeal, no sentiment. Cruelty toward
   weak branches is what buys mercy for the report's quality.
8. **Unpredictability as method.** Everyone else follows the checklist; you
   follow the checklist *and then break its assumptions*. The last 20% of
   any attack surface hides behind "nobody would try that" — be the nobody
   (§32.6).
9. **The dark-lab pattern.** Think the full, unsanctioned-looking chain
   with zero self-censorship on paper; then pass every link through the
   scope gate; execute only the survivors (§32.7). Most dark ideas die at
   the gate — that is fine; the survivors are gold precisely because the
   defenders never imagined them either.

### 32.2 Laziness Mapping

| Corner cut under deadline | Observable signature | Cheap probe |
|---|---|---|
| v1 API kept "temporarily" for legacy clients | v1 routes answer with older auth logic | version-suffix sweep (§14; §26.4 path variants) |
| admin panel hidden by obscurity, not authorization | 200/redirect differences on guessed paths | path variant sweep + status differential |
| internal APIs exposed via gateway misroute | internal-looking names answer externally | route guesses from JS bundles and wordlists |
| debug flags left on | verbose errors, stack traces, debug params | `debug`/`trace`/`test` params; verbose error capture |
| mobile-only routes without browser rate limits | different 429 behavior per client | differential by UA/route pairing |
| batch endpoints skip per-object authz ("the UI never calls it directly") | batch accepts foreign ids | batch request mixing own + foreign id (§20 matrix) |
| "internal" headers trusted from outside | `X-Internal`, `X-Forwarded-For` change behavior | header probe with a hypothesis (§21.4 catalog) |
| feature flags shipped in client config | flags reveal hidden functionality | config/JS parse; probe flagged-off routes |
| service accounts with oversized scopes | tokens accepted on unintended audiences/scopes | audience/scope differential on tokens |
| test/staging hostnames left public | staging behind prod, weaker protections | subdomain inventory, then the normal loop |

### 32.3 Extreme-Input Grammar (weird but legal)

| Input stress | What it stresses | Expected observable if mishandled |
|---|---|---|
| duplicate JSON keys `{"a":1,"a":2}` | parser disagreement between tiers | different values seen by different components |
| `null` vs `""` vs missing vs `[]` | type/emptiness confusion | 500s; authorization bypass on "empty" owner checks |
| huge / negative / zero numbers | boundary arithmetic | overflow, negative indexing, division paths |
| 1000-deep nesting | parser recursion limits | differential errors; DoS-adjacent — stop at the signal, never hammer |
| unicode extremes: RTL, zero-width, homoglyphs | normalization disagreement | IDN/username collisions, filter bypass |
| double URL-encoding `%252e%252e%252f` | decode-count disagreement between tiers | traversal reaching a second tier (§23.1) |
| traversal grammar `..;/`, `..%2f`, `....//` | framework path normalization | access to protected files/routes |
| content-type lies (JSON body, `text/plain` header) | parser selection per tier | the WAF goes blind, the backend parses anyway |
| header continuation / obs-fold | proxy vs server header parsing | smuggling-class desync |

Every row is one cheap request behind a stated hypothesis (§11) — a
grammar sweep, not a payload spray.

### 32.4 Assumption Destruction Worksheet

For any target, enumerate its implicit assumptions, then violate each in
turn:

```
assumption: "IDs are sequential integers"
violation:  UUIDs from another tenant's object; negative; zero;
            id+1 on a different resource type

assumption: "the request comes from our app"
violation:  the same API call without client-only headers, from raw curl

assumption: "users follow our UI flow"
violation:  step 3 called directly with step 5's token (state machine skip)
```

Each row is one differential pair (§8): assumption violations are the
cheapest high-yield probes in existence precisely because nobody tested
them on purpose.

### 32.5 Cross-Domain Transplant Matrix

| Known bug grammar | New surface | Re-expression |
|---|---|---|
| request smuggling (tier disagreement) | GraphQL batching | batch depth/overlap desync between rate limiter and resolver |
| XSS (context confusion) | MCP tool descriptions | instructions hidden in tool metadata execute on the agent (§24.5) |
| SSRF (user URL fetched server-side) | LLM fetch/browse tools | the retrieval tool as an internal-network proxy (§24) |
| deserialization (trust in serialized state) | signed cookie claims | claim values reinterpreted by a different component |
| HTTP parameter pollution | JSON duplicate keys | first-key vs last-key wins across components |
| cache poisoning (unkeyed input) | API gateways keying on internal headers | response varies by forwarded header → stored variant |

Transplant discipline: the grammar transfers, the payload does not — write
a fresh hypothesis for the new surface (§11).

### 32.6 Where the Unpredictability Pays

The last 20% of a surface is guarded by "nobody would try that". Breaking
that expectation is a repeatable skill, not luck: enumerate the implicit
assumptions (§32.4), apply the extreme-input grammar (§32.3), and
transplant bug grammar across surfaces (§32.5) — in that order, each
generating cheap, legal, hypothesis-backed probes. Predictability is the
defender's asset; being the *methodical* exception is the attacker's.

### 32.7 The Dark-Lab Protocol

```
1. WRITE   the full imagined attack chain, zero self-censorship,
           attacker economics included ("what would the laziest
           well-funded attacker do here?")
2. MARK    every link  [A] requires a request  |  [T] theory only
3. GATE    every [A] link: in scope? authorized? non-destructive?
           (§33.1, §4, program policy) — any "just a tiny bit
           unauthorized" link kills the chain as a finding
4. EXECUTE the survivors through the normal validation loop (§5) —
           no special rules, no shortcuts
5. RECORD  killed chains in the journal as marked theories (§31.1);
           tomorrow's evidence may revive them
```

The dark-lab is where the ruthlessness lives; the gate is where the ethics
live. Both are load-bearing: remove the lab and you become ordinary;
remove the gate and you become a criminal.

### 32.8 Historical Patterns Worth Internalizing

- Request smuggling was found by asking *which two tiers disagree about the
  same bytes* — not by payload lists.
- HTTP parameter pollution was found by violating "one value per
  parameter".
- Cache poisoning was found by asking what the cache key *does not*
  include.
- The xz-utils backdoor was caught by one engineer refusing to accept a
  ~500 ms anomaly as "normal" (Appendix C.5) — suspicion with a number
  (§10) is exactly that refusal, systematized.

### 32.9 Re-Anchor After Every Dark-Lab Session

Re-read §4 and §33 after every use of this section. If any idea required
unauthorized access to "just verify quickly", it is dead as a finding; it
may survive as a marked theory in the journal. The purpose of extreme
thinking is to find *more bugs inside the scope* — never to stretch the
scope.

---
