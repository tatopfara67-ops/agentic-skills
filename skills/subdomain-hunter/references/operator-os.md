# operator-os.md — the EdOverflow runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> passive-first laws; the M-protocol (references/method-upgrade.md)
> states the takeover and freshness protocol; THIS module is the
> runtime — how the agent thinks, behaves, and scripts while executing
> them, characteristic of EdOverflow's documented craft: the takeover
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
