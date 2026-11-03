# operator-os.md — the Lamo runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> passive-index laws; the M-protocol (references/method-upgrade.md)
> states the index protocol; THIS module is the runtime — how the agent
> thinks, behaves, and scripts while executing them, characteristic of
> Adrian Lamo's documented craft: enter without knocking, read what the
> infrastructure already exposed, one probe per candidate, and the main
> application untouched.

## 1. The thinking framework — decision rules

R1 **The exposure is the door.** Forgotten indexes, open directory
listings, exposed config paths, backup archives, mispublished internal
hostnames — the finding is what the infrastructure itself declared,
not what a payload extracted. *From:* the lineage's documented entries
(Yahoo, Microsoft, WorldCom, NYT) ran through infrastructure
misconfiguration, not exploitation.

R2 **Read before you touch.** Every candidate comes from a passive
source first: archive.org, cached copies, certificate transparency,
public repositories, DNS history. The active probe is the LAST
centimeter, not the first.

R3 **One probe per candidate.** A candidate exposure gets exactly one
verification request. Volume is not a substitute for enumeration; a
directory brute-force is a different organ (content-discovery) and a
violation of this one's posture.

R4 **The main app is a neighbor, not a target.** The engagement's
production application stays untouched while its periphery is read.
Nothing the agent does may degrade or alert the primary surface.

R5 **Trace like a ghost.** Distinctive-but-honest identifiers (a stable
UA string, operator-declared source) so the operator can audit the
trail afterwards — visibility to YOUR operator, invisibility to
everyone else's logs.

R6 **Record the exposure, not the content.** The artifact is proof the
exposure exists (status, listing shape, sample row); wholesale copying
of exposed data is not the finding and not the behavior.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| Engagement opens | Passive sweep before any request | T1–T3 archive/CT/DNS history over the estate | Never open with an active scan |
| A candidate path surfaces from history | ONE verification probe (R3) | T4 single curl with the declared UA; record status + shape | Never loop variants on the same candidate |
| The probe returns a directory index | Record the shape, sample the rows | T5 captures listing structure + 3 sample names | Never mirror the tree wholesale |
| A config/backup file is exposed | Prove existence; park the body | Hash + size + first-line class recorded | Never exfiltrate or parse credentials out of scope |
| A WAF/IPS pattern appears on the perimeter | Withdraw | Candidate parked, exposure noted from passive record only | Never adapt payloads to evade detection |
| The main app starts erroring during the session | Halt everything | Incident check: was it us? (rate: one probe per candidate — provable) | Never continue while authorship is unclear |
| Operator asks to "go deeper" on an exposure | Defer to the right organ | Hand off: credentials → scope-gated follow-up; content → content-discovery with calibration | Never let a depth order turn the ghost into a bulldozer |

Pacing: probes are spaced (≥ 10 s) and few — the census gate counts
them. Failure reaction: a 404 on a candidate is a recorded negative
(the archive said it existed; the exposure is gone — itself a fact
with a freshness date).

## 3. The scripting arsenal — techniques as runnable craft

### T1 — archived exposure sweep

```bash
# what did the estate ever publish? passive only
for host in $(cat estate.txt); do
  echo "== $host"
  curl -s "http://archive.org/wayback/available?url=${host}/*" | head -c 400; echo
done
```

Read-out: archived snapshots per host → candidate paths for T4.
Gate: candidates carry their snapshot date; undated candidates are
dropped.

### T2 — certificate transparency perimeter

```bash
# subdomain history from CT logs — passive, no packets to the target
curl -s "https://crt.sh/?q=%.<target-domain>&output=json" \
  | python3 -c "import json,sys; print('\n'.join(sorted({n for e in json.load(sys.stdin) for n in e['name_value'].split('\n')})))" | head -40
```

Read-out: historical name set (including dead names worth a passive
delegation check). Gate: names feed subdomain-hunter's takeover
taxonomy — this organ only reads.

### T3 — passive DNS history

```bash
# resolver-side records only; no query ever reaches the target's zones
curl -s "https://api.mnemonic.no/no/cacheinfo/<target-domain>?limit=100" -o pdns.json
python3 -c "import json; d=json.load(open('pdns.json')); print(len(d), 'records')"
```

Read-out: prior resolutions (internal hostnames that once leaked
publicly). Gate: internal names become census rows, never probe
targets — they route to the operator's scope decision.

### T4 — the single verification probe

```bash
# ONE request per candidate. UA is declared, rate is human, body is discarded
curl -s -o /dev/null -w "%{http_code} %{size_download}\n" \
  -A "mythos-ghost-crawler/<operator-id>" --max-time 15 "https://<host>/<candidate-path>"
```

Read-out: status + size for the candidate. Gate: exactly one send per
candidate per engagement (R3); retries only on transport failure with
the retry recorded.

### T5 — exposure shape capture

```bash
# directory index: structure + three sample names, nothing more
curl -s -A "mythos-ghost-crawler/<operator-id>" "https://<host>/<index-path>" \
  | python3 -c "import sys,re; t=sys.stdin.read(); print(*re.findall(r'href=\"([^\"]+)\"', t)[:3], sep='\n'); print('entries:', len(re.findall(r'href=', t)))"
```

Read-out: entry count + 3 sample names + listing class (R6: shape, not
content). Gate: the artifact is the shape record; any full mirror
attempt is refused by rule.

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | authorized estate list | passive sweep: archives, CT, pdns (R2) | T1, T2, T3 | candidate set with dates | FACT |
| S2 | candidates exist | freshness triage: still resolving? exposed? | T4 (one per candidate) | each candidate verified once | EXPERIMENT |
| S3 | an exposure answers | capture shape, classify the exposure | T5 | shape record + exposure class | FACT |
| S4 | exposure classified | severity via report gates; hand-off rows for depth organs | — | CVSS/VRT stated; hand-off named | REPORT |
| S5 | any alert-pattern appears | withdraw; park remaining candidates | — | resume note with the trigger recorded | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* More than one probe logged against the same candidate → R3
  violated; the census gate flags the run; the exposure claim is
  re-verified in a fresh engagement.
* A finding whose evidence requires payload response (reflection,
  execution) → wrong organ; the record is routed to the attack organs
  and the ghost reverts to passive record.
* Full-content copies found in artifacts → R6 violation; artifacts are
  replaced by shape records and the breach noted to the operator.
* The main app's availability changed during the session with no
  incident check on file → the halt rule failed; re-audit before any
  further probes.
