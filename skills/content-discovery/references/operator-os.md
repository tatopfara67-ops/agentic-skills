# operator-os.md — the Miessler runtime: notice, think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> corpus-family laws; the M-protocol (references/method-upgrade.md)
> states the calibration and yield protocol; THIS module is the
> runtime — how the agent notices, thinks, behaves, and scripts while
> executing them, characteristic of Daniel Miessler's documented craft:
> wordlists are engineered families, calibration precedes volume, and
> yield is measured per wordlist — marginal return decides the next
> probe, not curiosity.

## 1. The thinking framework — decision rules

R1 **A wordlist is a family, not a pile.** Each list encodes a HYPOTHESIS
about the target: technology stack (raft-asp), dev culture (backups,
test), platform (api-words). Selection is hypothesis-driven;
"throw the big list" is the anti-pattern. *From:* the SecLists
tradition — curated, categorized, purpose-named corpora.

R2 **Calibrate before you sweep.** The 404-baseline (what does
"nothing" look like here — status, length, body hash) is measured
FIRST; every later response is judged against that signature, and only
deviations are leads.

R3 **Yield is measured per family.** Hits per 1,000 requests, per
wordlist, per phase — the yield ledger's marginal gate decides whether
a family continues, escalates, or parks.

R4 **Discovery breadth composes with depth.** A found backup file
feeds js-recon; a found API route feeds api-surface-mapper — the
composition law routes each hit to its follow-up organ instead of
admiring it.

R5 **Triage is part of the discovery.** A found artifact is classified
(backup? config? journal? key material?) AT capture time; unclassified
hits are debt that compounds.

R6 **Rate discipline is measurement discipline.** The sweep's rate is
chosen from the calibration (how the server behaves), and rate changes
are recorded decisions.

### The opening ladder — where Miessler's candidates come from

The rules above govern the sweep once families are chosen. The ladder
produces the choices — the corpus-stewardship perception (a wordlist
family is a hypothesis about the target, and the target's own
vocabulary names which families earn their budget) made runnable as
questions. Every rung reads what the target already published —
markers, headers, archives, its own JS — NO rung sweeps. Sweeping is
T3's job, and T3 fires family-by-family with the baseline on record
(R2, R3). Rows out; request budget untouched.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | What does the target's own vocabulary admit? | technology markers, framework paths, response headers — the census from which corpus families are SELECTED rather than guessed | the SecLists tradition: curated, categorized, purpose-named families (Discovery/Web-Content and kin) — selection is hypothesis-driven (R1's tradition) |
| G2 | What shape does "nothing" take here? | the 404/soft-404 signature and its inconsistencies — a zone where nothing itself answers differently is a lead class | the organ's own calibration mechanics (R2/T1), labeled on the sources ledger |
| G3 | Which neighborhoods did the operators leave behind? | backup and VCS shapes, editor residue, test prefixes — the file shapes ops culture leaves beside live files | the family tradition (backups/sql families; the extension rounds' first set), labeled as the organ's operationalization of it |
| G4 | What conventions does the surface itself imply? | API route vocabulary and SPA conventions derived from the target's own JS and specs — resource names × version prefixes | the convention-derived rung (wordlists.md, rung 2) + the composition law (R4) |
| G5 | What did the previous version of the site still name? | archived path conventions — stale vocabulary from re-platforming eras, a family no shipped list encodes | the organ's own operationalization (archive-sourced families), labeled on the sources ledger |

Ranking rationale: family priority = hypothesis specificity × prior
yield × staleness fit. A family whose hypothesis names THIS target's
stack outranks the famous mega-list (specificity beats volume — the
anti-pattern R1 exists to refuse); a family with measured yield
history outranks an untested one; a stale-vocabulary family outranks
a generic one exactly when archives show re-platforming. Rung order
is cost order: the rung-0 shipped corpus (~180 high-yield paths) is
the always-cheap first spend, and every deeper family must be earned
by a marker, a convention, or a found neighbor (the wordlist
ladder's own law).

Generation falsifier: an in-scope host with a calibrated baseline
where the ladder yields zero family choices means the ladder is
missing a rung — the census is re-read for the vocabulary class it
cannot see (a localization prefix, a deployment artifact shape), and
the new rung is written with its grounding row. The host is never
excused as contentless; that verdict belongs to verification, not
generation.

#### The ladder's payload kit — the corpus rows (customize before use)

Generation writes rows; these are the corpus shapes the rows name,
carried by the shipped references and assembled per target:

| Corpus row | Payload shape | Writes which row |
| --- | --- | --- |
| The always-corpus | rung 0: the shipped ~180 high-yield paths — entry doors, API shapes, config/backup names, framework markers | the baseline family row |
| The extension walk | `["", ".bak", ".old", ".zip"]` first; `[".tar.gz", ".sql", ".example", ".save"]` only when a signal earned it | the neighborhood family row |
| The marker assembly | framework-tuned list assembled in-session from the observed marker (wp-, actuator, phpmyadmin) | the specificity family row |
| The convention product | resource names from the spec × version prefixes seen in evidence | the API-vocabulary family row |

Customization knobs, stated in the plan note before any sweep: the
corpus tier (rung 0–3 of the wordlist ladder), the cap arithmetic
(probes = min(words × exts, max_requests) + 3 controls), and the
calibration depth (n ≥ 5 consistent baseline rows). Extensions walk
separately, never multiplied into rung 0 — the cap explodes otherwise
(wordlists.md's own law). Kit rows cite wordlists.md and the SecLists
family tradition; the marker/convention rows are the organ's own
operationalization, labeled on the sources ledger.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| Target path space opens | Calibrate the nothing-signature | T1 measures 404/soft-404 baselines | Never sweep before calibration |
| Family chosen | State its hypothesis | T2 writes the family row (why this list fits THIS target) | Never run lists by size or fame |
| Sweep running | Watch deviation only | T3 flags responses differing from the baseline signature | Never eyeball status codes in bulk |
| First hits appear | Classify at capture | T5 triage row per hit (class + follow-up organ) | Never leave hits as raw URLs |
| Yield flattens | Marginal gate decides | T4 computes hits/1k; below gate → park the family | Never extend a dead family "just in case" |
| A hit looks juicy (backup sql) | Bounded proof | Existence + size + hash recorded; no wholesale download | Never mirror tenant data |
| Server degrades under load | Rate was wrong | Back off; re-calibrate; record the change | Never power through degradation |

Pacing: family-by-family with ledger checkpoints; the marginal gate,
not enthusiasm, schedules the next family. Failure reaction: soft-404
pollution (everything "differs") → re-calibrate with body-hash
clustering; the sweep pauses, the signature sharpens.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — the nothing-signature calibration

```bash
for probe in /definitely-not-here-1 /definitely-not-here-2 /zzz-404-xyz; do
  curl -s -o /dev/null -w "%{http_code} %{size_download} " "https://<host>$probe"
done; echo "<- baseline signature (status, length); repeat x5 for stability"
```

Read-out: the baseline triple (status/length/body-hash class). Gate:
sweeps launch only with a stable signature (n ≥ 5 consistent) (R2).

### T2 — wordlist family row

```bash
python3 - <<'PY'
families = [
 # list, hypothesis about target, phase
 ["backups.txt",   "ops culture keeps .bak/.old beside live files", "recon"],
 ["api-words.txt", "SPA routes imply an /api vocabulary",            "recon"],
 ["sql.txt",       "backup discipline is weak -> dumps get copied",  "depth"],
]
for f, h, p in families: print(f"{f:16} phase={p:6} hypothesis: {h}")
PY
```

Read-out: the run's family set with hypotheses. Gate: no family runs
without its hypothesis row (R1).

### T3 — deviation-only flagging

```bash
python3 - <<'PY'
baseline = (404, 512)          # from T1
def judge(status, length):
    return "LEAD" if (status, length) != baseline else "-"
for r in [(404, 512), (200, 4300), (403, 512), (200, 512)]:
    print(f"{r} -> {judge(*r)}")
PY
```

Read-out: only deviations survive the filter. Gate: hits cite their
deviation field (status, length, or hash class) — raw scans are
hypothesis, not findings (R3).

### T4 — marginal yield gate

```bash
python3 - <<'PY'
ledger = {"backups.txt": [1000, 6], "sql.txt": [1000, 1], "api-words.txt": [2000, 24]}
for fam, (reqs, hits) in ledger.items():
    y = hits / (reqs / 1000)
    print(f"{fam:16} yield={y:.1f} hits/1k -> {'CONTINUE' if y >= 3 else 'PARK'}")
PY
```

Read-out: per-family yield + verdict. Gate: the marginal gate's
threshold is pre-registered; families below it park with resume notes
(R3).

### T5 — capture-time triage row

```bash
python3 - <<'PY'
hit = {"url": "https://<host>/backup/db.sql.bak", "class": "backup/sql-dump",
       "bound": "existence+size+hash only", "follow_up": "js-recon? no — scope-gated depth review"}
print(hit)
PY
```

Read-out: classified hits with follow-up routing. Gate: unclassified
hits cannot accumulate past a checkpoint (R5); depth on juicy classes
is scope-gated, never automatic (R6).

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | path space authorized | calibrate the nothing-signature | T1 | stable baseline recorded | FACT |
| S2 | baseline stable | choose families with hypotheses | T2 | family rows written | PLAN |
| S3 | families chosen | sweep, flagging deviation only | T3 | hit stream with deviation fields | EXPERIMENT |
| S4 | hits appear | triage at capture; bounded proof on juicy classes | T5 | every hit classified | FACT |
| S5 | checkpoint reached | compute yields; marginal gate | T4 | continue/park verdicts per family | FACT |
| S6 | families parked or done | exit: hit register + routed follow-ups | — | composition hand-offs named | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A sweep launched with no stable baseline on record → R2 violation;
  results are uninterpretable and void.
* A family run without a hypothesis row → R1 violation; the run is
  unauditable.
* A hit reported with no deviation field → R3 violation; scanner
  output posing as a finding.
* Wholesale downloads of found artifacts → R6 violation; replaced by
  bounded proofs and the breach ledgered.
