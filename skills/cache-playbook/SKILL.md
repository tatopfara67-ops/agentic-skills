---
name: cache-playbook
version: 1.3.0
type: ai-skill
architecture: package
description: >-
  Deep-technical organ (tier 3) built from the Omer Gil lineage (Web Cache
  Deception, Black Hat USA 2017) with James Kettle's cache-poisoning corpus
  (Practical Web Cache Poisoning, Black Hat USA 2018; Web Cache Entanglements,
  2020) and the USENIX Security 2020 measurement "Cached and Confused" as its
  academic anchor — hunting the disagreement between origin and cache. The
  cache is treated as a second, silent parser: every disagreement between how
  the origin resolves a request and how the cache keys it (path confusion,
  unkeyed inputs, cache-key vs display-key gaps) becomes either stored secrets
  (deception: a victim's personalized response cached under a public path) or
  stored payloads (poisoning: an unkeyed input cached into other users'
  responses). Carries the WWH registers, the nonce-path discipline for
  poisoning proofs (never a real user's path), and the operator-as-victim law
  for deception proofs. Since v1.2.0 the organ carries the executable method
  layer (A16) — a mechanical critique of the Gil/Kettle art's floors (suffix
  guessing by habit, single-shot poison demos, cache keys narrated instead of
  measured, deception and poisoning families conflated, borrowed victims)
  shipped as protocol M1–M5: the pairwise cache-key baseline matrix, the
  suffix decision table, the poisoning differential with operator-owned
  victims, the served-check decay curve, and the family-separated ceiling
  statement. Use when a CDN or caching proxy sits in front of the target, when
  X-Cache/Age/cache-control headers appear, when the operator suspects cache
  attacks ("cek cache poisoning", "ada CDN cloudflare/akamai", "web cache
  deception di target ini", "cache misconfiguration", "kenapa halaman ini
  ke-cache").
category: security/deep-technical
license: MIT
metadata:
  author: tatopfara67-ops
  lineage: Omer Gil (web cache deception, Black Hat USA 2017) with James Kettle's cache-poisoning corpus (Black Hat USA 2018; Web Cache Entanglements, PortSwigger Research 2020) — Kettle's desync lineage anchors desync-hunter; this organ cites his cache works specifically, kept distinct on record
  tier: 3 — deep technical (the second-parser doctrine)
  requires: mythos-arsenal MCP server (arsenal/server.py); mythos-bug-hunter spine v4.5+ (R0, ledger, differential triad); desync-hunter (parser-seam discipline, adjacent surface); packet-orchestrator (raw-request precision when discrepancies need it)
---

# cache-playbook v1.3.0 — The Second Silent Parser

## 0. What This Skill Is — and Is Not

* **Is**: the organ for authorized hunting of web-cache attack
  classes — **cache deception** (personalized content stored and
  served to the unauthenticated) and **cache poisoning** (attacker
  input stored and served to everyone else) — on targets where a CDN
  or caching layer sits between users and the origin. Its unit of work
  is the cached-response differential: proof that a response stored
  under condition X is served under condition Y, with the cache's own
  HIT/MISS transitions as the instrument panel.
* **Is not**: a general CDN misconfiguration checklist (that is
  cloud-config-auditor's edge territory), and not HTTP desync hunting
  (desync-hunter's parser seams — though the two share the
  "specification as hypothesis" worldview; where a desync leads to
  cache impact, the organs hand off deliberately).

## 1. Inherited Contracts

Plugs into **Phase 1** (cache fingerprinting joins the dossier: cache
headers, key indicators, edge presence) and **Phase 3** (the
differentials). Inherits the experiment contract (§6), the canary
doctrine (§8 — the victim is the operator's own account; the poisoned
path is a nonce path only the operator requests), the closure
vocabulary (§7), and R0/R7 unchanged. desync-hunter's one-discrepancy-
per-request discipline governs delimiter probing; packet-orchestrator
governs any raw-byte request a discrepancy demands.

## 2. The Lineage (attribution)

**Omer Gil** named and demonstrated web cache deception (Black Hat
USA 2017 whitepaper; the class was covered industry-wide in Feb 2017):
a URL path the cache classifies as static while the origin serves the
authenticated page underneath it. **James Kettle's** cache corpus —
*Practical Web Cache Poisoning: Redefining "Unexploitable"* (Black Hat
USA 2018) and *Web Cache Entanglements: Novel Pathways for Poisoning
the Cache* (PortSwigger Research, 2020) — built the poisoning
methodology: unkeyed inputs, cache-key vs display-key discrepancies,
and the parser-differential craft this organ inherits. The academic
anchor is **Mirheidari, Arshad, Onarlioglu, Crispo, Kirda, Robertson —
"Cached and Confused: Web Cache Deception in the Wild"** (USENIX
Security 2020): the large-scale measurement of the class, and the
delimiter-based path-confusion variations that widened it. Attribution
boundary: Kettle anchors desync-hunter (his desync corpus); this organ
cites his cache works specifically — different works, different organ,
kept distinct in the lineage registry's correction field. The
second-parser doctrine and the nonce-path proof law are this bundle's
own contribution. The verification record is
`references/sources.md`.

## 3. First Principles — the WWH registers (A14)

### WHAT — the cache layer, anatomized

1. **The players**: browser → CDN/edge cache (Cloudflare, Akamai,
   Fastly, varnish/nginx/tomcat-style reverse proxies) → origin. The
   cache is a store keyed by ITS OWN idea of the request.
2. **The cache key**: the subset of request elements the cache decides
   to key on (typically method + normalized path + selected params,
   sometimes `Vary`-listed headers) — everything else is an *unkeyed
   input* the origin may still read.
3. **The store heuristic**: what the cache decides to store and for
   how long (cache-control, edge heuristics, static-looking
   extensions) — the misjudgment deception exploits.
4. **The observable panel**: `X-Cache`/`CF-Cache-Status` HIT/MISS,
   `Age`, `Cache-Control`/`Vary`/`X-Served-By` — the instrumentation
   every proof in this organ reads.

### WHY — the root causes, mechanically

1. **Deception exists because two parsers classify one path
   differently**: the cache's static-file heuristic (extension,
   delimiter handling) says "cacheable asset" while the origin's
   router says "user page" — a path-confusion delimiter (`/`,
   encoded delimiters, `;`, `.css`, `%2f`) makes both true at once,
   and the personalized response is stored under a key any anonymous
   request can repeat. (Gil's class; USENIX'20 measured the delimiter
   space.)
2. **Poisoning exists because the cache key is smaller than the
   request**: inputs the origin reads but the cache does not key on
   (headers, path segments after normalizable delimiters, query
   params dropped by the key) let one request's response be stored
   and served to every other request with the same key — the
   attacker's bytes riding another user's cache entry. (Kettle's
   unkeyed-input law.)
3. **Cache-key vs display-key gaps exist because normalization is
   per-layer**: the cache normalizes for lookup, the origin resolves
   what it displays, and two requests that LOOK different to a human
   can collapse into one key — the entanglement that lets a poisoned
   entry be reached by a path nobody intended.
4. **The class pays because the cache serves without re-asking
   authorization**: whatever the origin decided once is replayed to
   every holder of the same key — a frozen authorization meeting fresh
   requesters.

### HOW — the procedure, in order

The numbered procedure is §4; `references/cache-method.md` expands
each step with its oracles and falsifiers. The one-line form:
fingerprint the cache and its key, then make origin and cache
disagree — once for storage (a confusion or an unkeyed input), once
for retrieval (the anonymous fetch or the nonce path) — and let the
HIT/MISS transitions carry the proof.

War note (A15): the cheng sweep is cache-key probing with benign
markers (HIT/MISS as the instrument); the ch'i is the path-confusion
delimiter nobody canonicalized — the one byte-shape where the cache
trims and the origin does not. W2 governs the poisoning proof: the
stored payload is demonstrated by an operator-owned fetch hitting the
poisoned key — other users' responses are never observed, and a
persistent poisoned production entry is un-weaponized (purged or
expiry-bounded) before the report ships; leaving poison in place is
sabotage, not evidence.

## 3.5 The Method Layer — Critique, Upgrade, M1–M5 (A16)

A lineage named is not expertise delivered. `references/method-upgrade.md`
grades the published cache art where it was mechanically weak — suffixes
guessed from intuition, poisons fired once and screenshotted, unkeyedness
told as a discovery story, the deception and poisoning families mixed in
one narrative, third-party victims borrowed for impact — and ships the
executable replacement: **M1** the pairwise cache-key baseline matrix
(two requests differing in exactly one dimension decide keyed/unkeyed),
**M2** the WCD suffix protocol over the corpus suffix+delimiter set
(operator's own profile, rate-capped), **M3** the poisoning differential
(treatment/victim/control fetches, n ≥ 5, canary in the entry), **M4**
the served-check decay curve (t = 0 s/30 s/2 min/10 min, window ×
traffic-class arithmetic shown), **M5** the family-separated ceiling
statement (third-party exposure NOT claimed, measured window only).

## 3.6 The Operator Layer (A17) — the Omer Gil + James Kettle runtime

`references/operator-os.md` ships the figure's documented psychology
as the agent's RUNTIME, in four parts: the thinking framework (numbered
if-then decision rules, each citing the documented behavior it
distills), the behavioral protocol (situation → move → agent action →
refusal, with pacing and failure-reaction rules — how the agent acts
and behaves while hunting), the scripting arsenal (the organ's core
techniques as exact, tool-agnostic commands and micro-scripts, each
with its read-out and decision gate), and the rigid run-order binding
rules, behavior, and scripts onto the M-protocol above. Load it when
the hunt runs: the doctrine states the posture, the M-protocol states
the procedure — the operator OS is how the agent BEHAVES while
executing, characteristic of Omer Gil + James Kettle.

## 4. Procedure — Numbered Actions

1. **Fingerprint the cache.** Identify the layer (headers, edge IP
   behavior, `X-Cache`/`CF-Cache-Status`, `Age` on repeat fetch);
   record cache-control/Vary verbatim in the dossier. No cache, no
   organ — record that and stop.
2. **Map the cache key.** Same path with varied query params, headers,
   and casings: which variations share a HIT (same key) and which
   MISS (keyed)? The key map is a dossier table, cited by request
   records.
3. **Locate cacheable personalized pages** (deception candidates):
   authenticated responses with private content and store-capable
   cache directives or heuristic-friendly neighbors.
4. **Sweep path-confusion delimiters** on a candidate page (the
   USENIX'20 delimiter set plus target-specific ones): one delimiter
   per request, response bytes compared — the cache storing the
   personalized body under a static-looking variant is the mechanism
   half-proven.
5. **Deception differential, operator-as-victim.** Operator account
   fetches the confused path (response stored, MISS→HIT observed);
   anonymous fetch of the same path retrieves the private body —
   CONFIRMED, with the operator's own data and nothing else.
6. **Unkeyed-input probing** (poisoning candidates): for each input
   the key map showed unkeyed (headers, normalizable path segments),
   a benign marked value (self-owned marker, never a real payload)
   that the origin reflects into the response; stored (HIT) and
   served on a clean retrieval = reflection confirmed.
7. **Poisoning proof on a nonce path.** The poisoning proper runs
   ONLY on a path containing a long random nonce no real user will
   ever request: store the marked response, retrieve clean, show the
   marked body served under the victimless key. That proves the class
   without ever serving attacker bytes to another human. A poisoning
   demonstrated any other way on a shared path is a program-policy
   violation, not a finding.
8. **Impact chain where the program asks for it.** Reflection →
   stored-script escalation (xss-playbook's sink law on the reflected
   context) → nonce-path proof again; the chain states per-link
   severities (chain-architect law).
9. **Classify.** `cvss3_score` on the observed serving path (deception
   vectors ride confidentiality; poisoning rides what the payload
   achieved); `vrt_classify` under the server misconfiguration /
   cache-attack rows.
10. **Exit gate numbers.** Cache fingerprinted, key map size,
    delimiters swept (each by verdict), unkeyed inputs probed,
    deception/poisoning proofs with their HIT/MISS records — stated,
    not summarized.

## 5. Hard Rules (mechanically enforced)

1. **The victim is the operator.** Deception proofs fetch private
   content only from the operator's own session; any proof touching
   another user's data is out of doctrine and out of scope.
2. **The poisoned path is a nonce path.** Poisoning proofs store
   attacker-controlled bytes only under keys containing a fresh random
   nonce; poisoning shared, guessable, or real-user paths is
   forbidden — the mechanism proof does not need it.
3. **One discrepancy per request.** Delimiter and unkeyed probes vary
   exactly one element; combined variations are separate
   experiments with separate records (desync-hunter's law, inherited).
4. **HIT/MISS is the instrument.** A cache-attack claim without its
   MISS→HIT (and clean-retrieval) records is a lead, closure
   INCONCLUSIVE.
5. **Reflection ≠ finding.** An unkeyed reflected input is a
   mechanism; the finding is the reflected-bytes-to-victim path,
   proven under rules 1–2 and classified on that path.
6. **Cache purge discipline.** After any proof that stored content,
   attempt the documented purge/invalidate (or record that none
   exists); the campaign leaves the cache as it found it (W2 — win
   without fighting).
7. **Marked values are self-owned.** Every probe value is a unique
   marker attributable to this engagement; no payload proof carries
   anything but the operator's own objects and accounts.

## 6. Tool Routing

| When | Tool |
| --- | --- |
| Cache fingerprinting, key mapping, delimiter sweeps | `http_probe` (repeat-fetch mode, headers verbatim) + `ledger_append` |
| Deception differential (operator session → anonymous) | `http_probe` (two sessions) + `ledger_append` |
| Unkeyed-input reflection probes | `http_probe` + `ledger_append` (EXPERIMENT: one variable, marker value) |
| Raw-byte discrepancies where needed | packet-orchestrator discipline via `arsenal_route` |
| Classification | `cvss3_score` + `vrt_classify` |
| Report gate | `auditor/audit_report.py` — exit 0 or it does not ship |

## 7. Reference Library (load on demand)

| Load when… | Module |
| --- | --- |
| Expanding any step of §3/§4 into exact probes, oracles, falsifiers | `references/cache-method.md` |
| Exact technique set (cache buster discipline, unkeyed inputs, fat GET, Gil's deception suffix, delimiter confusion set, boundary mapping), per-technique failure modes, primary sources | `references/corpus.json` (versioned payload corpus) |
| Verifying the Gil/Kettle/USENIX lineage and its sources | `references/sources.md` |
| Grading the published method, baselining the cache key, measuring decay | `references/method-upgrade.md` |
| Running the hunt — the Omer Gil + James Kettle runtime: thinking rules, situation-to-action behavior, scripting, rigid run-order | references/operator-os.md |

The corpus is versioned (`corpus_version`) and every entry carries its
primary source and its **failure modes** — read them before closing any
hypothesis as negative: a technique that failed for a documented reason
(full-URL keys, Vary segmentation, router 404 posture, honored
Cache-Control) leaves the cache untested, not secure. Every poisoning
probe carries a cache buster — collateral poisoning of a shared entry
is an incident, never a finding.
