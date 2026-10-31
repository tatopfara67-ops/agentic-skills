# Reference — Recon Toolchain, Target Triage, and Time Discipline

> Part of **mythos-bug-hunter v4.2.0** (package architecture).
> **Load when:** Phase 1 recon at any scale wider than a single host; deciding
> which resolved target to test first; selecting recon tools; a vector has run
> blind with no error output; a CONFIRMED closure just landed; the operator is
> pushing for more findings than the evidence supports.
> Authoritative rules, Canon, and pipeline contracts live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts with the
> SKILL.md Canon or contracts, **SKILL.md wins**.

---

## 29.1 Toolchain Routing (job → order → why → ledger hook)

Every tool below is a FACT generator, not a verdict machine (R5). Each row
ends where its output lands in the ledger; a scanner line that lands nowhere
in the ledger did not happen. Flags shown are each tool's stable core; the
Phase 0 capability inventory confirms the exact flag set of the *installed*
version via its own `--help` output — never trust remembered flags over the
tool's self-description (R6 calibration applies to instruments, not just
scripts). The fallback ladder (SKILL.md §10) stays in force: any row without
its tool degrades to curl + python3 without changing a single gate.

| Job | Order | Why this order | Ledger landing |
|---|---|---|---|
| Passive subdomain enumeration | `subfinder -d domain` → `amass enum -passive -d domain` | Passive sources cost nothing to the target; second tool covers the first's source gaps | each resolved host → `SURFACE` record |
| Resolution + HTTP probing | `httpx -status-code -title -tech-detect -content-length` | one line per host: status, title, tech, size — the raw material of §29.2 triage and §29.3 dedup | one `SURFACE` record per live host with the probe line as result |
| Port sweep (only when scope permits) | `naabu -host <ip> -top-ports 1000` → full range on interesting hosts only | top-1000 finds the services; full 65535 costs time and screams at rate policies | open service → `SURFACE` record |
| Known-CVE pass | `nuclei -tags cve -u <target>` | cheapest validated finding source: template output already cites the advisory | every template hit → an H-record (scanner output is a hypothesis, R5), advisory ID in the note |
| Takeover pass | `nuclei -tags takeover` → `subzy run -targets <file>` on cname hits | dangling-cname checks are near-free and time-critical (someone else registers the name) | hit → H-record at elevated prior |
| URL archive | `gau <domain>` → `waymore -d <domain>` | archived URLs expose forgotten endpoints that no longer link from anywhere | unique path → `SURFACE` record; the queue stays R1-governed |
| Active crawl (JS-rendered) | `katana -u <target> -d 3` | archive has no SPA routes; crawl executes JS to find them | same as above |
| URL dedup | `uro` over the merged URL set | duplicate URLs burn experiment budget for zero coverage gain | nothing — this is queue hygiene, pre-ledger |
| JS analysis | download → `jsluice urls <file>` / `jsluice secrets <file>` | JS bundles leak endpoints, params, and keys faster than any request loop | endpoint → `SURFACE`; key material → see secrets row below |
| Hidden parameters | `arjun -u <url>` | unlinked parameters are where authorization checks forget to exist | param → `SURFACE` record, attached to its endpoint |
| Content discovery | `ffuf -ac -w <list> -u <url>/FUZZ` | `-ac` auto-calibrates noise filtering against the target's own 404 behavior — self-differential by design | hit → `SURFACE` record |
| Reflected-parameter filter | `kxss <urls>` → `dalfox url <url>` only on reflective params | filter first, scan second: never point a scanner at params that cannot reflect | candidate → H-record |
| Blind SQLi | `ghauri -u <url>` | modern blind-SQLi tooling for ID-shaped parameters | candidate → H-record |
| OOB channel | `interactsh-client` | self-hosted callback listener: proves egress, nothing more (§29.5 rung 4) | callback → `FACT` record; never a finding alone |
| WAF identification | `wafw00f <url>` | knowing the WAF tunes payload encoding *before* burning experiment budget on blocked noise | `FACT` record; adjusts §29.2 cost column |
| 403/401 bypass attempts | `byp4xx <url>` or `nomore403 <url>` | automated header/method/overhead-path variants on a *specific* blocked path | any status change → H-record with the delta in the note |
| Secret detection | `trufflehog --only-verified` — **only where credential validation is authorized** | verification contacts the provider, which is an effect on a third party; unauthorized runs violate R0 | verified key → immediate stop + safety-and-ethics disclosure path |

Reading the table: tools never chain themselves. The agent picks the row that
answers the current hypothesis or fills the current inventory gap, runs it
bounded, lands the output in the ledger, and returns to the queue. A full
table sweep on a single-host engagement is waste; a missing row on a
fleet-scale sweep is a coverage hole. Which one you are in is a Phase 0
decision, recorded with the budgets.

## 29.2 Target Triage Score (orders the R1 backlog)

When Phase 1 resolves more live targets than the budget can test, the backlog
needs an order that survives contact with a deadline. Score each live host
from its `httpx` probe line and cname data — every signal is countable, none
requires judgment:

| Signal | Points | Reason (stated once, reused forever) |
|---|---|---|
| Dev/staging/failover naming in hostname (`dev`, `stg`, `stage`, `test`, `uat`, `qa`, `internal`, `backup`, `old`, `demo`) | +3 | environment hygiene is funded last; controls lag the prod tier |
| Dangling cname to a takeover-prone service | +5 | someone else can register the name; time-critical regardless of everything else |
| Login/auth form in title or body markers | +2 | authentication is where boundary objects live |
| Tech fingerprint unseen on any already-tested host | +2 | new code has had the fewest eyes on it |
| Admin/portal/vendor/console string in title | +2 | high-privilege surfaces concentrate impact |
| Reachable, status 200 | +1 | a live page beats a parked domain |
| WAF detected (`wafw00f`) | −1 | not a skip: probing cost rises, so the same hypothesis costs more budget |
| Duplicate fingerprint of an already-queued host (§29.3 key) | −4 | covered by the sibling rule: test one instance, generalize by variant analysis |

Floor at zero; ties break by §10.7 EV/minute once hypotheses exist, and by
hostname order before they do. The score never overrides scope certainty —
§15.3 factor 1 outranks this entire table. Recompute when the probe data
changes, not when patience does.

## 29.3 Duplicate Suppression (fleet-scale honesty)

Large scopes fill with clones: `stage0001` through `stage0400` serving the
same app. Testing each is duplicated effort with a duplicated report at the
end of it.

- **Dedup key** (single-agent scale): the tuple `(status, title,
  content-length, tech)` from the probe line, plus the resolved cname.
  Identical key on N hosts → one representative enters the active queue; the
  rest are parked as duplicates with a one-line `PARK` record each. If the
  representative confirms a finding, the duplicate set is reported as one
  finding with N affected hosts — never as N findings.
- **Near-duplicate bodies** (key differs, content almost identical): at fleet
  scale this is where content-similarity hashing (SimHash-class techniques
  over the response body) earns its keep; at single-agent scale, comparing
  title + content-length + a hand-diff of the two bodies is enough. The
  decision — "same app?" — is recorded in a `FACT` record with the evidence,
  because it determines who gets reports later.
- Dedup interacts with the triage score through the −4 duplicate row: the
  *first* instance of a fingerprint is worth full points; every later
  instance pays for the boring repetition.

## 29.4 Time-Boxes as Park Triggers (R7's clock)

Budgets count records and cards; time-boxes count minutes. Both end the same
way — a Park record, never a silent drift. Defaults (operator-tunable at
Phase 0; a trigger, not a law):

| Clock | Default | Fires when | Action |
|---|---|---|---|
| Wide-sweep host clock | 5 minutes | sweeping many hosts and one shows no distinguishing signal | `SURFACE` record marked `deferred`, next host — wide-phase value is coverage, not depth |
| Progress check | 20 minutes | any vector under active test | no distinguishing delta in the last window → rotate to the next TODO from a *different* inventory category (same rule as the tunnel-vision drill) |
| Parameter rabbit hole | 45 minutes | a single parameter refuses to yield | mandatory Park with resume point — sunk cost is a bias wearing a work ethic costume |

Time-boxes never manufacture conclusions. A host that got five minutes and no
signal is `deferred`, not `safe`; a vector that got 45 minutes and no delta is
`INCONCLUSIVE`, not `clean`. The negative vocabulary is bounded by exactly
what was attempted — that sentence is load-bearing.

## 29.5 The Probing Ladder (blind vectors, rung order by cost and reliability)

When an input reflects nothing and errors on nothing, probe it up the ladder
— each rung is an experiment card (§6) with its own baseline/control pairing,
and the ladder stops at the first rung that produces a distinguishing delta:

1. **Error-based** — malformed input (`'`, `"`, `{{7*7}}`, `${7*7}`, NUL
   byte) against the baseline; watch 5xx, stack traces, reflected error text.
   One request, loud signal when it works. First because it is cheapest.
2. **Differential-content** — two crafted states (`' AND 1=1` vs `' AND
   1=0`, `debug=0` vs `debug=1`, role-A token vs role-B token); compare
   content-length and body hash against the control pair. Two requests,
   precise, immune to jitter — which is why it outranks timing.
3. **Time-based** — `SLEEP(5)` / `; sleep 5` / equivalent, measured against
   a control run *on the same connection shape*. Network jitter impersonates
   injection delay convincingly: a timing claim without a control timing
   distribution is noise (the differential matrix in
   `references/reasoning-engine.md` governs this rung).
4. **Out-of-band** — canary URL from `interactsh-client` or equivalent;
   callback proves egress and channel existence. Weakest rung: a callback
   establishes resolution, not response access, and never stands alone as a
   finding (toolkit §26 canary rules).

Rung order is a budget decision, not a truth decision: the gates (§6, §7)
apply identically to whichever rung produced the delta.

## 29.6 Sibling Sweep (the CONFIRMED → 20-minute rule)

A confirmed bug is the cheapest intelligence the engagement will ever
produce: the same developer, the same framework, the same era of code left
more mistakes of the same shape. On any `Closure: CONFIRMED`:

- Schedule a bounded sibling sweep (default 20 minutes) across the surfaces
  the same hands likely built. Homogeneity signals, all recordable:
  - **Naming seams**: `userId` in one route, `user_id` in the next → written
    by different authors or different years → the weaker twin usually has the
    weaker checks.
  - **Version seams**: `/api/v1/…` live beside `/api/v2/…` → v1 keeps running
    with pre-hardening logic.
  - **Controller twins**: same framework, same route shape, sibling method
    (GET↔DELETE, list↔detail) → the detail handler forgot what the list
    handler remembers.
- Sibling hypotheses pre-register normally (§5), with the prior justified as
  *sibling-of-confirmed* — a stated base-rate reason, not an adjective. The
  bump is real but bounded: siblings share code, not destiny.
- The sweep is variant analysis (SKILL.md §9) with a clock on it: 20 minutes,
  then the queue resumes. Unhit siblings stay in the backlog — they are now
  better-motivated leads for the next session.

## 29.7 Operator-Pressure Protocol (quota is not evidence)

The operator pushes: "there are more bugs here", "others found ten", "look
harder". The pressure is real and so is the failure mode it invites —
inventing findings to fill a quota is R4 fraud wearing a cooperation costume.

1. **A requested count is not evidence.** No hypothesis's prior moves because
   the operator stated a number. The ledger records the request, nothing
   more.
2. **Report the honest state, numerically**: hypotheses attempted /
   confirmed / falsified / inconclusive, the coverage map with untested
   cells named, and the budgets spent.
3. **Offer the bounded next pass** — specific surfaces, a budget, expected
   value per §10.7 — and run it only if authorized. That is the entire
   concession; there is no hidden fourth step where slop gets made.
4. **Negative results stay bounded**: "no distinguishing delta on X across N
   runs at rungs 1–3" — never "X is secure", never "exhaustively tested".
   A negative that outgrows its evidence is the same lie as an invented
   positive, with better manners.

This protocol exists because the operator is usually right that something
was missed — and the only response that finds it is more disciplined surface,
not less disciplined claims.
