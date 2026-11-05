# operator-os.md — the EdOverflow runtime: notice, think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> passive-first laws; the M-protocol (references/method-upgrade.md)
> states the takeover and freshness protocol; THIS module is the
> runtime — how the agent notices, thinks, behaves, and scripts while
> executing them, characteristic of EdOverflow's documented craft: the takeover
> question is a TAXONOMY (which service, which dangling shape, which
> fingerprint), dead records are a differential, and fingerprints
> expire.

## 1. The thinking framework — decision rules

R1 **Passive sources name the subdomains; active probes only verify.**
CT logs, DNS aggregators, archives, and config leaks produce the name
set — the census precedes any query against the target's zone. *From:*
the can-i-take-over-xyz discipline: the project itself began as a
taxonomy, not a scanner.

R2 **A takeover candidate is a typed row, not a vibe.** The row states
the service (Heroku/GitHub Pages/S3/…), the dangling shape (NXDOMAIN?
CNAME to deleted service? unclaimed?), and the fingerprint signature
the service currently serves — typed against the registry before any
claim.

R3 **Dead/dangling/claimable is a THREE-way differential.** NXDOMAIN
(name gone), dangling (CNAME points at something gone), claimable
(the gone thing can be re-registered by the operator) — each is a
different verdict with different impact.

R4 **Fingerprints expire; freshness is checked per-run.** The service's
"unclaimed" page changes (the documented fingerprint drifts); every
claim cites the fingerprint OBSERVED TODAY, not the registry's
yesterday.

R5 **The chain walk runs before the claim.** A dangling record inside
a delegated zone (NS chain) multiplies impact: verify the delegation
before pricing.

R6 **Proof is operator-side registration, gated by scope.** Actually
claiming an orphan is a scope decision (usually a REPORT
recommendation, not an action); the default proof stops at the
observed fingerprint + the registry row.

### The opening ladder — where EdOverflow's candidates come from

The rules above govern verification once a candidate exists. The
ladder produces the candidates — the registry-founder's perception
(the takeover question began as a TAXONOMY: which service, which
dangling shape, which fingerprint — before it was ever a scanner)
made runnable as questions. Every rung reads public records — CT
logs, passive aggregators, archives, the zone's own delegation —
NO rung claims anything. Claiming is a scope decision and defaults
to REPORT (R6); the ladder only types rows. Rows out; the zone
untouched.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | Which names does the public record know that the zone never admitted? | CT logs, passive DNS aggregators, archives — the census of names the estate forgot it ever minted | the passive-first law: the census precedes any query against the zone (R1's tradition; the registry project itself began as a taxonomy, not a scanner) |
| G2 | Which chains leave the parent toward a third-party service? | CNAME rows pointing outside the estate — the shape the registry exists to type | the registry's own structure (fingerprints.json: service, CNAME targets, fingerprint, NXDOMAIN flag per entry) |
| G3 | Which leaving chains point at services the registry marks claimable? | chains typed against the signature table — service + dangling shape + today's fingerprint | the registry's verdict-table tradition, with its correction discipline (entries argued, demoted, retired as providers add verification — Unbounce #11, Google Sites #277) |
| G4 | What combinations did the ops team never mint? | the permutation round: dev/staging/uat/… × known labels — bounded, DNS-side | the permutation generator (sources.md's passive ladder, rung 5) — the organ's own, labeled |
| G5 | Which delegations would multiply the blast? | NS chains: a dangling record inside a delegated zone multiplies impact | the chain-walk law (R5) |

Ranking rationale: candidate priority = claimability × chain depth ×
staleness. A dangling CNAME to a registry-claimable service inside a
delegated zone is the top of the order (claimable now, impact
multiplied); a merely dead name is a negative-observation row, not a
candidate; a chain whose service the registry retired (the provider
added ownership verification) ranks below one still live — retirement
is exactly the correction the registry tracks. Freshness is checked
at claim time, not at rank time (R4): the ranking orders WHERE to
look, today's fingerprint decides WHAT is true.

Generation falsifier: an in-scope domain where the ladder yields zero
typed candidates means the ladder is missing a rung — the census is
re-read for the name class it cannot see (a vendor subdomain, a
TLD-widening row the scope gate permits), and the new rung is written
with its grounding row. The zone is never excused as owned; that
verdict belongs to verification, not generation.

#### The ladder's payload kit — the signature rows (customize before use)

Generation writes rows; these are the signatures the rows name, a
local sync of the community registry (date-pinned in
takeover-signatures.md — upstream wins on any disagreement):

| Signature row | The marker payload | Writes which row |
| --- | --- | --- |
| Heroku | CNAME `*.herokuapp.com` + body "No such app" | claimable-candidate row |
| GitHub Pages | CNAME `*.github.io` + 404 with GitHub chrome | claimable-candidate row |
| Shopify | CNAME `*.myshopify.com` + "Sorry, this shop is currently unavailable" | claimable-candidate row |
| Azure | CNAME `*.cloudapp.azure.com` / `*.azurewebsites.net` + 404 with Azure error code | claimable-candidate row |
| AWS CloudFront | CNAME `*.cloudfront.net` + "Bad request" viewer-error page with x-amz-cf-id present — claim requires SNI mismatch evidence; low prior | low-prior candidate row |
| The wildcard control | a random hex label resolved before anything counts | the zone-verdict row |

Customization knobs, stated in the plan note: the provider set
(restrict the signature table to the clouds the scope actually
names), the registry sync date (the local table's pin — re-sync when
older than the engagement), and the permutation cap (a few hundred
per engagement, recorded). The full table with its procedure lives in
takeover-signatures.md; the CloudFront row carries its own warning —
the most misreported class in public reports.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| Domain in scope | Census names from passive sources | T1 harvests CT/DNS/archive sources | Never brute-force names against the zone first |
| A name resolves oddly | Type the dangling shape | T2 runs the three-way differential (NXDOMAIN/dangling/claimable) | Never call everything "takeover-able" |
| CNAME points at a service | Check TODAY's fingerprint | T3 fetches the service's current unclaimed signature | Never trust the registry's cached fingerprint |
| Fingerprint matches the claimable signature | Walk the NS chain | T4 checks delegation depth + zone parent | Never price impact before the chain |
| Scope authorizes actual claim | Claim operator-side, once, marked | governed registration with canary naming | Never claim orphans outside explicit scope |
| Fingerprint mismatch | The registry drifted | Record the new signature; registry correction row | Never force the old signature into the report |
| Wildcard DNS detected | Mark the zone wildcard-bound | Wildcard verdict row; random-name control | Never report wildcard hits as discoveries |

Pacing: census is quiet and long; verification queries are spaced and
few. Failure reaction: a fingerprint that matches nothing in the
registry → NEW entry row (contribution candidate), never a squeezed
match.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — passive name census

```bash
for src in "https://crt.sh/?q=%.<target-domain>&output=json" ; do
  curl -s "$src" | python3 -c "import json,sys; print('\n'.join(sorted({n for e in json.load(sys.stdin) for n in e['name_value'].split('\n')})))"
done > names_passive.txt; wc -l names_passive.txt
```

Read-out: the passive name set. Gate: the census list is the sweep's
ONLY input (R1); brute-forced names are marked as such or refused.

### T2 — the three-way differential

```bash
for name in $(cat names_passive.txt); do
  dig +short "$name" CNAME | sed "s/^/$name CNAME /" || true
  dig +short "$name" A | sed "s/^/$name A /" || true
done | tee resolve_map.txt | head -10
# NXDOMAIN rows vs CNAME-present rows vs A-present rows = the three verdicts
```

Read-out: the resolve map with three-valued verdicts. Gate: every
candidate row states its class — dead, dangling, or resolving (R3).

### T3 — fingerprint freshness check

```bash
# what does the pointed-at service serve TODAY?
cname=$(dig +short sub.<target-domain> CNAME | head -1)
curl -s -o /dev/null -w "%{http_code}\n" "https://${cname%.}/" | sed "s/^/today_status /"
curl -s "https://${cname%.}/" | head -c 120; echo " <- fingerprint bytes now"
```

Read-out: today's signature (status + body prefix). Gate: claims cite
the observed-today fingerprint with its date (R4); registry text alone
is refused.

### T4 — NS chain walk

```bash
dig +short <target-domain> NS
dig +short sub.<target-domain> NS 2>/dev/null   # delegation depth if any
# a dangling record inside a delegated zone = chain impact row
```

Read-out: delegation structure. Gate: impact pricing for dangling
records cites the chain depth (R5).

### T5 — wildcard control

```bash
rnd=$(python3 -c "import secrets; print(secrets.token_hex(8))")
dig +short "$rnd.<target-domain>" A | sed "s/^/wildcard-control /"
# an answer here means the zone answers ANYTHING: hits are noise until filtered
```

Read-out: the wildcard verdict. Gate: sweeps on wildcard zones apply
the control's signature as a second baseline (R6).

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | domain authorized | passive name census | T1 | name set with sources | FACT |
| S2 | names in hand | run the wildcard control | T5 | zone verdict recorded | CONTROL |
| S3 | zone typed | resolve map + three-way differential | T2 | candidates typed | FACT |
| S4 | dangling rows exist | fingerprint freshness per candidate | T3 | observed-today signatures | EXPERIMENT |
| S5 | signature matches claimable class | NS chain walk; price impact | T4 | chain row cited | FACT |
| S6 | claims composed | exit: typed register + registry corrections | — | scope-gated claim rows only | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A takeover claim citing a registry fingerprint without today's
  observation → R4 violation; re-fetch before the claim stands.
* A "dead" verdict from a single query → negative-logic failure;
  repeat or void.
* Wildcard hits reported as discoveries → R6 violation; the control
  row must precede any hit claim.
* An actually-claimed orphan with no scope authorization on record →
  R6 violation; the engagement halts and the incident is ledgered.
