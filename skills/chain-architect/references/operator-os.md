# operator-os.md — the Orange Tsai runtime: notice, think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> compound kill-chain laws; the M-protocol (references/method-upgrade.md)
> states the chain protocol; THIS module is the runtime — how the
> agent notices, thinks, behaves, and scripts while executing them,
> characteristic of Orange Tsai's documented craft: name collisions
> are attack surface, low-severity primitives compose into critical
> chains, and every link is proven by its own differential before the
> chain is claimed.

## 1. The thinking framework — decision rules

R1 **Confusion is a class — hunt the name collision.** Two systems
agreeing on a name (a filename, a hostname, a header, a variable)
that each resolve differently is attack surface: "confusion attacks"
is a repeatable hunt, not a lucky day. *From:* the lineage's published
lines — ProxyLogon began in a namespace collision (a path prefix that
meant two things to two components); the Apache confusion line
formalized the class.

R2 **The chain's power is composition, not any single bug.** A chain
of "low" findings (SSRF + path confusion + auth skip) outscores one
shiny primitive; the hunter's instinct reads primitives as CHAIN
MATERIAL. *From:* the DEVCORE kill chains — each link modest, the
composition critical.

R3 **Prove every link with its own differential.** A chain reported
with three claimed links and one demonstrated is a fabricated chain;
each link's EXPERIMENT record exists before the chain record does.

R4 **SSRF is an interior door, not a finding.** An SSRF primitive's
value is what it REACHES: internal services, metadata endpoints,
protocol handlers — the follow-through is a census, then a chain.

R5 **Name the composition mechanism precisely.** "Bug chaining" is
not a mechanism; "the unvalidated redirect preserves the internal
prefix across the router's normalization" is. Chain records state the
mechanism per link.

R6 **Respect the escalation ladder.** Chain impact demonstrations run
one rung at a time (reach → read → write → execute) and stop at the
engagement's stated ceiling — the report's ceiling statement names the
rung actually proven.

### The opening ladder — where Orange Tsai's candidates come from

The rules above govern once a primitive is in hand; the ladder
produces the primitives themselves — the architecture-first
perception (the 3-year Pwn2Own campaign read the target's architecture
DEEP before touching it; ProxyLogon began by noticing a path prefix
that meant two things to two components) made runnable as questions.
Every rung is a reading of the estate's architecture, configs, and
bundles — collision candidate rows out, no differentials sent; the
T2 collision probe stays gated behind S2 and consumes the ladder's
rows.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | What does the estate's own architecture admit about its component boundaries? | the architecture read: deployment diagrams, proxy configs, module lists, published docs — every place the vendor names a seam | the 3-year architecture-first campaign posture (HEXACON 2023, sources.md) |
| G2 | Where do two components parse the SAME name form? | the parser-seam census: scheme/host/path/port forms each component resolves — edge vs origin, router vs backend, language vs language | "A New Era of SSRF — Exploiting URL Parser in Trending Programming Languages" (DEF CON 28 — the canonical hunt-the-seams source) |
| G3 | Which module seams validate the same request twice? | module-ambiguity census: path handling, auth, rewrite modules that both claim a request class with different semantics | "Confusion Attacks: Exploiting Hidden Semantic Ambiguity in Apache HTTP Server" (OrangeCon 2023) |
| G4 | Which name forms collide across consumers? | the collision census: path prefixes, hostnames, headers, filenames — each a candidate row naming the two consumers and the form | R1's class riding ProxyLogon's namespace collision (DEVCORE, sources.md) |
| G5 | Which "harmless" capabilities would compose — and toward what rung? | the composition census: redirects, fetches, file writes, auth skips, debug endpoints read as CHAIN MATERIAL with their position potential | R2 + the DEVCORE kill chains (each link modest, the composition critical) + the operator brief ("find 3-4 small harmless-seeming gaps, chain them into a critical") |

Ranking rationale: candidate priority = composition depth × seam
multiplicity × pre-auth position. A collision on a pre-auth path tops
the order — ProxyLogon's pre-auth SSRF was the door the chain opened
through; a seam family with several consumer pairs outranks a single
pair (each pair is a separate disagreement to prove); a primitive
whose composition question answers toward write/execute outranks
read-only material; architecture-named seams outrank inferred ones —
the vendor's own boundary statement is the map the 3-year campaign
trusted. Rows out; no differential spent.

Generation falsifier: an in-scope estate where the ladder yields zero
primitive candidates means the census is missing a rung — a name-form
class it does not type (a cookie name, a header form, a port
convention), a parser family absent from the collision table; the
architecture census is re-read, the rung is written with its grounding
row. The estate is never excused as "un-chainable" at generation
time: low primitives are found by reading, not by luck.

#### The ladder's payload kit — the collision-form and primitive rows (customize before use)

Generation writes rows; these are the form and primitive classes the
probes and composition questions later load (the vocabulary and the
chain archetypes live in chaining-catalog.md §1/§3):

| Kit row | The form it names | Catalog anchor |
| --- | --- | --- |
| parser-form row | scheme/host/path oddities each consumer may resolve differently (backslash, encoded separator, fragment, port suffix) | chaining-catalog §1 "Parser confusion" + T2's name-form classes |
| collision-form row | path prefixes and hostnames that mean two things to two components | R1's ProxyLogon namespace collision (sources.md) |
| module-seam row | the double-validation request class two modules both claim | chaining-catalog §1 + OrangeCon's Apache module ambiguity |
| primitive rows | info disclosure / endpoint leak / SSRF / auth-bypass / file write / file read / redirect / takeover / race / debug exposure — each rated by position, not standalone severity | chaining-catalog §1 vocabulary table |
| composition row | "what does this give me a position FOR?" — the per-primitive composition question | chaining-catalog §2 |
| chain archetype row | the pre-registration template: links + mechanisms + ceiling, every link pre-registered before impact | chaining-catalog §3/§4 + T3 |
| ceiling row | reach → read → write → execute, stopped at the authorized rung | T5 (R6) |

Customization knobs, stated in the plan note: the seam slice (which
component pairs the census types — edge/origin only vs every
intermediary and module pair), the form set (which name-form classes
run — narrowed to the stack the architecture read actually shows),
and the ceiling profile (the rung the engagement authorizes — decides
which archetype rows are even sketched). The primitive vocabulary,
composition questions, and archetypes live in chaining-catalog.md.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| A primitive found (SSRF, redirect, path oddity) | Read it as material | T1 files the primitive with its composition potential | Never report the primitive and stop |
| Two components share a name form | Suspect the collision | T2 probes whether each resolves it differently | Never assume both sides agree |
| A chain sketch emerges | Write the chain map FIRST | T3 records link hypotheses + mechanisms | Never fire links ad-hoc toward impact |
| A link is unproven | Prove it before the next | Per-link differential (n ≥ 2) | Never claim chains with unproven links |
| SSRF confirmed | Census the reachable interior | T4 enumerates internal endpoints via the primitive | Never exfiltrate through it during census |
| Impact tempting (RCE rung) | Check the ceiling | The engagement's stated rung governs; stop there | Never "just test" one rung past authorization |
| A link refuses to compose | The negative is a map datum | Collision table updated with the failed joint | Never force the chain by hammering the link |

Pacing: chain work alternates desk (map, mechanism) and probe (one
link, one differential); the map grows before the traffic does.
Failure reaction: a broken link is re-diagnosed at the MECHANISM level
(R5) — "try more payloads" is not a diagnosis.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — primitive record with composition potential

```bash
python3 - <<'PY'
primitive = {"name": "open-redirect-relay",
             "observed": "302 preserves internal /%5c prefix",
             "material_for": ["router normalization confusion", "ssrf transport"],
             "record": "R-401"}
print(primitive)
PY
```

Read-out: the material card. Gate: primitives carry composition
potential (R2); bare primitives without potential assessment are just
findings for other organs.

### T2 — name-collision differential

```bash
# one name form, two consumers: does each resolve it differently?
form="/legacy%5cadmin"
for consumer in edge origin; do
  curl -s -o /dev/null -w "$consumer %{http_code} %{size_download}\n" \
    "https://<host>/?next=$form"
done
```

Read-out: per-consumer resolution of the same name form. Gate: a
confusion claim cites DIFFERENT resolutions (R1) — identical handling
means no collision.

### T3 — chain map with mechanisms

```bash
python3 - <<'PY'
chain = [
 {"link": 1, "primitive": "ssrf-fetch", "mechanism": "router treats %5c as separator; backend as literal", "proven": "R-405"},
 {"link": 2, "primitive": "metadata-read", "mechanism": "internal endpoint trusts proxy source", "proven": None},
 {"link": 3, "primitive": "cred-reuse", "mechanism": "cloud role keys accepted by adjacent service", "proven": None},
]
for l in chain: print(f"L{l['link']}: {l['primitive']:16} proven={l['proven']}")
print("chain status: 1/3 proven — chain NOT claimable yet")
PY
```

Read-out: the chain map with per-link provenance. Gate: the chain
record ships only when every link cites its differential (R3).

### T4 — SSRF interior census (bounded)

```bash
# what does the primitive REACH? read-only census, one request per candidate
for target in "http://169.254.169.254/latest/meta-data/" \
              "http://internal-api:8080/health" \
              "file:///etc/hostname"; do
  curl -s --max-time 5 -o /dev/null -w "%{http_code} %{size_download} $target\n" \
    "https://<host>/fetch?url=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$target")"
done
```

Read-out: reachable-interior rows (status/size class only). Gate:
census is read-only (R4); deeper interaction routes through the
engagement's ceiling decision.

### T5 — escalation-rung ceiling check

```bash
python3 - <<'PY'
rungs = ["reach", "read", "write", "execute"]
authorized_ceiling, proven = "read", "read"
for i, r in enumerate(rungs):
    print(f"{r:8} {'PROVEN' if r == proven else ''} {'CEILING' if r == authorized_ceiling else ''}")
print("verdict: proven == ceiling -> STOP; report states the read rung")
PY
```

Read-out: the rung statement. Gate: the report's ceiling sentence
names the proven rung (R6) — rounding up a rung is a fabrication.

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | primitive in hand | file the material card | T1 | composition potential stated | FACT |
| S2 | collision suspected | run the name-collision differential | T2 | different resolutions cited | EXPERIMENT |
| S3 | links sketched | write the chain map with mechanisms | T3 | every link has a mechanism sentence | PLAN |
| S4 | map written | prove link 1..n, one differential each | T2/T4 per link | all links cite records | EXPERIMENT |
| S5 | all links proven | demonstrate impact one rung at a time to the ceiling | T5 | ceiling statement written | CANARY |
| S6 | chain complete or parked | exit: map, links, rung, resume notes | — | unproven links parked with reasons | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A chain claimed with any unproven link → R3 violation; the chain
  record is withdrawn until the link's differential exists.
* An impact sentence above the proven rung → R6 violation; corrected
  to the ceiling statement.
* A collision claim where both consumers resolve identically → R1's
  core condition failed; re-classify as non-collision.
* Interior interaction past read-only during census → R4 violation;
  the census halts and the event is ledgered.
