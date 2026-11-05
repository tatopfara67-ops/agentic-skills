# Reference — Ruthless Mind

> Part of **mythos-bug-hunter v4.6.0** (package architecture).
> **Load when:** Phase 2 warzone drills: the nine principles, laziness mapping, extreme-input grammar, assumption destruction worksheet, cross-domain transplant matrix, dark-lab protocol; the trained-eye cue catalog (any phase — perception fires before reasoning).
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

### 32.10 The Trained Eye (instinct as a measurable asset)

Hunters call it a gut feeling. Strip the mysticism: instinct is pattern
recognition compressed from repetitions — a library of smells, a protocol
for noticing, and a score that says which smells pay. An agent has no
subconscious, so all three live on paper — which is better, because paper
can be audited and trained.

**The cue catalog.** What a sharpened eye actually reacts to — each row:
the smell, why it smells, what it historically yields, the first cheap
probe:

| # | Cue (the thing you noticed) | Why it smells | Historical yield | First probe |
|---|---|---|---|---|
| C1 | one resource uses sequential ints while the app otherwise uses UUIDs | that code path predates the convention — and per-object authz | IDOR | id swap between two own accounts (§20 matrix) |
| C2 | same status code, different body across roles on one endpoint | hand-rolled authorization layering | authz bypass | role×resource cell differential (§8) |
| C3 | the object id is accepted in two positions (path + body/query) | two parsers; one of them unchecked | IDOR / mass assignment | mutate one position, hold the other constant |
| C4 | v1 and v2 are both alive for the same resource | v1's authz froze when v2 shipped | IDOR on v1 | replay the v2 request against v1 |
| C5 | error text echoes input or object metadata | a verbose oracle | enumeration / injection oracle | echo differential — same shape, one field changed |
| C6 | bimodal timing on identical requests | cache path vs origin path | cache deception / poisoning | timing buckets + cache headers on both arms |
| C7 | response headers differ across roles on one endpoint | middleware skipped per route | authz bypass | header inventory diff, then the missing-header hypothesis |
| C8 | a route 404s on GET but answers on another verb | dead-but-alive surface | hidden functionality | method matrix, non-destructive verbs first |
| C9 | a "new" feature ships an old build hash / sourcemap | stale code in production | patched bugs alive again | version diff against the vendor changelog |
| C10 | the app behaves identically with a token claim removed | the claim is decorative | auth bypass | remove-claim differential, both own accounts |
| C11 | docs or OPTIONS admit methods the UI never uses | orphan state-changers | logic abuse | one bounded probe per method, canary payload |
| C12 | tenant A's id is accepted on tenant B's endpoint shape | tenancy enforced in the UI only | cross-tenant IDOR | tenant-slice differential, own tenants ×2 |
| C13 | GraphQL and REST twins serve the same data | resolvers skip the field authz the REST layer had | field-level IDOR | twin diff — same object via both, compare fields |
| C14 | a rate limit differs by client type (web vs mobile UA) | the limiter sits at one edge, not the backend | race window | paired courteous bursts, floors per R7 |

Cues are priors, not verdicts: every row still enters through the normal
hypothesis gates (§11, §5). A cue that skips the gate is a hunch — and
hunches are exactly what §5 exists to kill.

**The notice protocol.** Perception is a first-class pipeline stage:

1. Log the perception the moment it fires — one line, the cue id and the
   two records that produced it. "I'll remember it" is how surface
   evaporates.
2. Every cue becomes an H-record in the same session, or is explicitly
   parked with its id and the reason. A cue that never becomes anything
   is deleted by the calibration step below.
3. The motivating H-record carries its `cue:` line. An untagged noticing
   is unauditable; an unauditable instinct is a vibe.

**The calibration loop.** The eye sharpens by scoring, not by feeling. At
engagement close, tally per cue: fired → hypothesis → confirmed /
killed / parked. Cue yield = confirmed ÷ fired.

- yield ≥ 20% over the engagement: the cue moves earlier — its probe
  family runs in the first hour of the next Phase 2.
- yield < 5% on two consecutive engagements: demote to opportunistic
  ("check only when the records already cross its path").
- Never retire a cue on one bad engagement — base rates are noisy at
  small n (§10.4); two is the floor, three is the signal.

This is §31.5's calibration audit applied to perception: priors calibrate
the reasoning, cues calibrate the eye. A hunter whose catalog is scored
every engagement stops having hunches and starts having throughput.

---
