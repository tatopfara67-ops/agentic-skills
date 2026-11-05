# operator-os.md — the Gil + Kettle-cache runtime: notice, think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> origin/cache disagreement laws; the M-protocol
> (references/method-upgrade.md) states the key-audit and nonce
> protocol; THIS module is the runtime — how the agent notices,
> thinks, behaves, and scripts while executing them, characteristic of
> the Omer Gil cache-deception craft and Kettle's cache-poisoning
> corpus: the cache is a second silent parser, the cache key is its
> grammar, and the proof runs on nonce paths with the operator as the
> only victim.

## 1. The thinking framework — decision rules

R1 **The cache is a parser with its own grammar.** The cache key
decides which requests are "the same request"; everything NOT in the
key (headers, cookies, path quirks) is invisible to it. Hunt the
difference between what the ORIGIN varies on and what the CACHE keys
on. *From:* the two source lines — Gil's deception (the cache stores
what the origin renders for a DIFFERENT principal) and Kettle's
poisoning (unkeyed inputs write the stored response).

R2 **The cache key is audited, not guessed.** Vary headers, path
segments, extensions, cookies one at a time and observe the cache's
 HIT/MISS behavior — the key audit IS the first experiment set.

R3 **Nonce paths carry the proof.** Every poisoning demonstration runs
on a fresh random path (never `/` or shared entries), so nothing real
is ever overwritten; the nonce IS the canary discipline applied to
caches.

R4 **Deception and poisoning are different findings.** Deception =
the cache stores MY response for YOUR request class (personal data
cached under a shared key). Poisoning = MY response is served to OTHER
requesters. Classify before demonstrating; the demos differ.

R5 **The operator is the only victim.** Demonstrations that need a
"victim fetch" use an operator-owned session; reading anyone else's
cached personal data stops at existence + one marker row.

R6 **Cache state is evidence.** HIT/MISS/X-Cache headers, TTLs, and
age at each step are recorded as artifacts — a cache claim without
cache-state rows is prose.

### The opening ladder — where Gil's and Kettle's candidates come from

The rules above govern the run once a candidate is in hand; the
ladder produces the candidates FIRST — the deception-era and
poisoning-era perception (Gil's class was found by asking which path
shapes the cache would classify as static while the origin still
rendered the authenticated page beneath them; Kettle's corpus began
by asking which inputs the cache key ignores) made runnable as
questions. Every rung is a census question that writes rows — no rung
sends a marker, poisons an entry, or spends the nonce budget;
demonstrations stay gated behind R3/R5 and consume the ladder's rows.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | Does a cache layer exist here at all, and does it announce itself? | the presence record: Age/X-Cache/Via headers, HIT/MISS differential on double-fetch, TTL directives — the fact row every later rung is priced against | R2's audit-first tradition — the corpus opens by working out how the cache caches before any exploit craft (CACHE-001, corpus v1.0.0; sources.md, Practical Web Cache Poisoning BH'18) |
| G2 | Which path shapes does the cache classify as static while the origin still renders the authenticated page? | suffix classes — the deception candidates as path-confusion families, personal body under a static-looking key | Gil's class on record: a path the cache classifies as static while the origin serves the authenticated page beneath it (sources.md, BH USA 2017 whitepaper) |
| G3 | Which delimiter families does this cache tier honor as static markers? | the delimiter census: `;`, `%0a`, `%23`, `?`, nonexistent-file shapes — families measured in the wild, tier by tier | the delimiter-based path-confusion variations measured at scale (Mirheidari et al., USENIX Security 2020 — sources.md, the recorded measurement) |
| G4 | Which inputs does the cache key ignore while the origin varies on them? | unkeyed inputs — headers, cookies, query values whose variation still HITs — the poisoning candidates | Kettle's unkeyed-input methodology (sources.md, BH'18; the reflected-then-cached family, CACHE-002/003/005) |
| G5 | Where do cache key and display key disagree? | the discrepancy row: content stored under one key but displayed under another — the entangled candidates | Kettle's cache-key/display-key discrepancy craft (sources.md, Web Cache Entanglements, 2020; the fat-GET family, CACHE-004) |
| G6 | Which stored entries would a poison or deception actually reach? | the exposure ceiling: shared-across-principals entries, TTL/age magnitudes, cache-control/Vary posture — what a stored row would serve, to whom, for how long | the organ's own exposure-pricing, labeled (R4's family separation + R6's state-as-evidence; the posture oracle, CACHE-009) |

Ranking rationale: candidate priority = exposure ceiling × family
sharpness. A delimiter family that renders personalized content under
a cacheable class ranks first (deception: the PII ceiling, family
separated per R4); an unkeyed input whose value surfaces in the
stored body ranks next (poisoning: the marker row's reach priced by
the entry's sharing); a key/display discrepancy row ranks by the
entangled route's cross-principal reach; TTL-only rows rank last —
they price reach, they do not generate. Rows out; no entry poisoned,
no victim fetched.

Generation falsifier: an in-scope host with a live cache layer where
the sweep yields zero candidate rows across every row class means
the ladder is missing a rung for that cache tier (a service-worker
cache, a layered CDN-on-CDN, an authenticated-only origin with no
shared tier) — the census is re-read (Doyhenard's DEF CON 32
delimiter expansion is the recorded next ring, sources.md), the
missing rung written with its grounding row. The host is never
excused as "clean" at generation time: a zero-yield verdict belongs
to verification's coverage row, never to the ladder.

#### The ladder's payload kit — the confusion-class sweep rows (customize before use)

Generation writes rows; these are the sweep classes the rows name,
every one a one-variable census probe on the operator's own session
(recorded; single-shot where the path is shared; byte-exact probes
live in corpus.json v1.0.0 — the kit names the entries, it does not
re-quote them):

| Sweep row | The read payload class | Writes which row |
| --- | --- | --- |
| extension row | the authenticated path × one suffix each (`.css` `.png` `.jpg` `.txt` `.js`), double-fetched, one variable per probe (CACHE-006) | deception-class row (personal body under a static-looking key) |
| delimiter row | the tier's delimiter families (`;`, `%0a`, `%23`, `?`, the nonexistent-file shape, then the encoded/traversal second edition `%2e`, `%3f`, `..;/`), one family per probe (CACHE-007 + CACHE-010, the USENIX'20 set) | delimiter-family row (which markers this tier honors) |
| unkeyed row | the header/query vary list (User-Agent, Accept, Cookie, X-Forwarded-*), one input per probe, second-fetch comparison (CACHE-002/003/005) | keyed/unkeyed table row |
| display-key row | the fat-GET comparison: same key, different display route (CACHE-004) | key-vs-display discrepancy row |
| cache-state row | the evidence sweep: Age, X-Cache, TTL directives, Vary posture, ETag (CACHE-009) | exposure-ceiling row (sharing × lifetime) |

Customization knobs, stated in the plan note: the cache tier (CDN
edge vs origin reverse proxy vs service worker — which delimiter
families and extension classes load), the corpus vintage (which
delimiter ring: Gil's originals, the USENIX'20 measured set, the
Doyhenard expansion), and the exposure policy (deception proofs stop
at the marker row vs full operator-victim demonstration, per R5).

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| A cache layer detected | Audit the key before anything | T1 varies inputs; observes HIT/MISS per probe | Never fire payload probes at an unaudited key |
| A hit on a varied header | That header is unkeyed — flag it | unkeyed-input row; poisoning candidate | Never exploit mid-audit |
| Path extension changes cacheability | Deception candidate | T2 probes the accept-rules of extension classes | Never claim deception without the class row |
| Ready to demonstrate poisoning | Nonce path first, always | T3 registers fresh nonce + marker payload | Never poison a shared or production entry |
| Demo needs a victim fetch | Operator-owned session only | second operator session reads the poisoned nonce | Never measure real users' exposure |
| Deception candidate shows personal data | Existence + one marker row | the marker row is the impact ceiling | Never page through cached PII |
| Cache seems absent/transparent | Record the negative | X-Cache absent + no HIT/MISS differential rows | Never assume a cache from a vendor name |

Pacing: key audit is a patient one-variable-per-probe phase; poisoning
demos are single-shot events on fresh nonces. Failure reaction: a MISS
where a HIT was expected → the key model is wrong; re-audit before ANY
further probe (the model precedes the payload).

## 3. The scripting arsenal — techniques as runnable craft

### T1 — the cache key audit

```bash
base="https://<host>/account/settings"
for variant in "baseline" "user-agent: curl-x" "cookie: session=operator" \
               "accept: text/csv" "x-nonce: 1"; do
  curl -s -o /dev/null -w "%{http_code} " -H "${variant^}" "$base"
  curl -s -o /dev/null -w "2nd:%{http_code} age:%{header_json}" "$base" 2>/dev/null || true
  echo " <- $variant"
done
# HIT on 2nd fetch of a VARIED input = that input is unkeyed
```

Read-out: keyed vs unkeyed input table. Gate: poisoning candidates
cite unkeyed rows (R2); probes before the audit are refused.

### T2 — extension/deception class probe

```bash
for ext in "" ".css" ".png" "/a.css" "?x=.js"; do
  curl -s -o /dev/null -w "%{http_code} %{size_download} $ext\n" \
    "https://<host>/account/settings${ext}"
done
```

Read-out: which path decorations still render the personalized page
AND get cached (the deception shape: personal body under a
static-looking key). Gate: deception claims carry the class row (R4).

### T3 — nonce registration + marker payload

```bash
NONCE="n$(python3 -c 'import secrets; print(secrets.token_hex(6))')"
echo "nonce: $NONCE"   # fresh per EXPERIMENT; logged before first use
curl -s -o /dev/null -w "poison-send %{http_code}\n" \
  "https://<host>/$NONCE<script>MYTHOS_CACHE_MARKER()</script>"
```

Read-out: the poisoning send on the fresh path. Gate: the nonce is
pre-registered (R3); a poisoning probe on a non-nonce path is refused.

### T4 — victim read-back (operator-owned)

```bash
# the operator's SECOND session fetches the nonce path cold
curl -s -o /dev/null -w "victim-fetch %{http_code} size:%{size_download}\n" \
  -H "Cookie: session=<operator-second-session>" "https://<host>/$NONCE"
# marker present in the victim fetch = poisoning PROVEN at the demo ceiling
```

Read-out: the poisoned entry served cross-session. Gate: victim
sessions are operator-owned (R5); any other source halts the run.

### T5 — cache-state evidence row

```bash
curl -sI "https://<host>/$NONCE" | grep -iE "x-cache|age|cache-control|etag" | head -5
```

Read-out: the artifact row (HIT/MISS, age, TTL directives). Gate:
cache claims cite these rows (R6) — stateless prose is refused.

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | cache layer suspected | detect + record cache state | T5 | cache facts on record | FACT |
| S2 | cache present | audit the key, one variable per probe | T1 | keyed/unkeyed table | EXPERIMENT |
| S3 | unkeyed inputs found | classify deception vs poisoning candidates | T2 | class rows per candidate | FACT |
| S4 | candidate selected | register nonce + marker | T3 | nonce pre-registered | EXPERIMENT |
| S5 | nonce live | demonstrate at the ceiling (operator victim only) | T4 | marker observed cross-session | CANARY |
| S6 | proof complete | exit: key audit + classes + nonce records | — | TTL/stopgap notes included | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A payload probe sent before the key audit table exists → R2
  violation; restart at the audit.
* A poisoning demo on a shared or production path → R3 violation;
  nonce-only is the bright line.
* A victim fetch from any non-operator session → R5 violation; the
  engagement halts.
* A cache claim with no cache-state rows attached → R6 violation; the
  finding is prose until the artifacts exist.
