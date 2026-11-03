# The executable method — M1–M5 for ghost-crawler

This file is the organ's executable method: numbered phases,
exact record formats, thresholds, decision gates, and falsifiers,
in run order. An agent that has never heard of any name in the
appendix runs this at full precision. The critique that
justifies each step (why these phases exist, what was weak in
the Lamo record) is preserved verbatim as the §4–§5 appendix.

## 1. The executable protocol — M1 through M5

Quickstart — the side-door census as commands (one EXPERIMENT record
per index, M2 classes gated, no-trace is accounting at M5):

```bash
# M1/M2 side-door census — documented classes only, low and slow
while read -r u; do
  for p in /.git/HEAD /.env /.DS_Store /backup.zip; do
    code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 8 "$u$p")
    echo "$code $u$p" >> sidedoor.tsv
  done
done < s2-live.txt
awk '$1==200' sidedoor.tsv                   # candidates only
# M2 dork grammar — query the index engines, never the target
#   site:TARGET intitle:"index of"          (see side-door-catalog.md)
# M5 trace ledger — every request above is one row, nothing uncounted
wc -l sidedoor.tsv                           # must equal requests sent
```

### M1 — the index protocol (the noticing, mechanized)

Ordered pass, one EXPERIMENT record PER INDEX, coverage tabulated:

```
INDEX-PASS: index=<ct-log|dork-class|archive-class|dns-records>
  query=<grammar used> coverage=<what this index CAN see, class>
  yield=<candidates> as-of=<M3 stamp>
```

Rules: the pass order is cheapest-public-first (CT before dork
before archive — the subdomain-hunter ladder habit); every query's
grammar is recorded verbatim so a second analyst re-runs it; the
coverage table sums at the end — `covered-classes 7/9, gaps:
<which>` — and the GAPS are named before any candidate is chased
(W1, W2).

### M2 — the census schema (side-door classes, gated)

Per discovered asset, classed against the full taxonomy
(the side-door catalog):

```
CENSUS: asset=<host/path> class=<abandoned-subdomain|panel|
  open-directory|backup-archive|staged-storage|ghost-endpoint|
  credential-artifact> evidence=<index + snapshot hash>
  liveness=<present|memory> next=<route>
```

**Completeness gate**: the census run is not closed until every
class in the catalog has been either (a) produced candidates or
(b) recorded as no-yield-for-this-target with the query grammar
that proved it — "I didn't look for backup archives" is a refused
closure (W3).

### M3 — the freshness rule

Every candidate from an archive/cache-class source carries its
as-of stamp, and the stamp PRICES the follow-up:

| As-of class | Disposition |
| ----------- | ----------- |
| ≤ 30 days | present-hypothesis; full verification budget |
| 30–180 days | stale-present; verification at reduced rate, flagged |
| > 180 days | MEMORY: hygiene record only; no active verification without operator override on record |

The rule converts "found in an old snapshot" into what it is —
a memory with a date (W4).

### M4 — the exposure differential (found vs claimed)

A candidate becomes an exposure finding only through the
differential: what the INDEX shows vs what the TARGET's present
surface claims.

1. **Baseline**: the target's declared surface (scope records,
   live DNS set from M1's pass).
2. **Treatment**: the index-derived candidate (present-class only).
3. **Confirm rule**: the candidate resolves/persists in the present
   AND is ABSENT from the declared surface (n ≥ 2 checks across ≥
   24 h for persistence-class claims) → exposure CONFIRMED at the
   forgetting class; present-but-declared → in-scope asset, route
   to the appropriate organ; memory-class → M3 hygiene row.

### M5 — the trace ledger (no-trace as accounting)

```
TRACE: session=<id> passive-reads=<per-index query count>
  active-touches=<count, target=0 by default> rationale=<for any
  non-zero touch: operator authorization + necessity>
```

The lineage's defining claim is now a row: the session CLOSES with
`active-touches: 0` or with each exception justified on record —
prose ethics cannot be audited; counts can (W5).

## 2. Falsifiers — what would prove this method wrong

* A "memory" candidate (as-of > 180 days) resolves live → the
  archive index was mis-dated: re-stamp, re-class as present, and
  the freshness table's cutoffs get a correction record.
* The completeness gate's no-yield proof later yields a finding →
  the query grammar recorded as proof was too narrow: the grammar is
  the defect, re-write it, and the census re-opens for that class
  only.
* Coverage gaps remain after the full pass (2/9 classes unreachable
  by any public index) → recorded as closure-limiting FACTS in the
  report — honest gaps, never silently dropped.
* Trace ledger shows active-touches > 0 without a rationale row →
  the session is void for report purposes: the discipline failed,
  and the failure is the finding about ourselves.

## 3. Worked micro-example (numbers consistent, incident fictional)

Target: corp-front scope. M1 pass: CT-log (as-of today) yield 214
names; dork-class grammar 12 queries yield 9 candidates; archive
class as-of 14 months yield 31. Coverage 8/9 classes (no
credential-artifact index available — gap recorded). M2 census:
3 panels, 2 open-directories, 1 backup-archive class (as-of 14
months → MEMORY), 1 ghost-endpoint. M4: ghost-endpoint absent
from declared surface, resolves live, persists across 24 h
(2/2 checks) → exposure CONFIRMED at forgetting class, P4 with
the persistence evidence. M5: passive-reads 27 queries,
active-touches 2 (the two 24 h resolution checks, operator-authorized
necessity rows present) — no-trace held to its accounting.

*The appendix preserves the original framing text: what the
named lineage practiced, what was weak, and what this organ
ships instead. It is context for humans; the agent's run order
is §1–§3 above.*

The charter's A16 charge: **a lineage named is not expertise delivered.**
Adrian Lamo's art is real — infrastructure entries via misconfigured
side doors, the passive-first discipline — but the published form is
anecdote: entries told as stories, the index-reading method never
written as steps, proxy discipline narrated as personal ethics,
archive freshness unrecorded. The caveat this organ already carries
(his authorship of the caveat-worthy later history) does not exempt
the METHOD from A16: the floors are named mechanically, and the
replacement ships as executable protocol. An agent with no legend
must run this at its discipline.

## 4. Appendix — the lineage critique — five mechanical weaknesses of the published method (context, not steps)

| # | What the art shows (documented) | Why it is weak as a shipped method |
| - | ------------------------------- | --------------------------------- |
| W1 | Entries as anecdotes — the Yahoo/Microsoft/NYT accounts are told as stories ("I noticed a misconfig…") | The noticing is the whole method and it stays in the man: no census protocol, no coverage accounting — a reader cannot re-run the hunt on a new target, only admire the old one |
| W2 | Passive indexes read without a coverage record — CT logs, dorks, archives are consulted ad hoc; which index answered WHAT is never tabulated | Selectivity is invisible: two hunters reading "the indexes" touch different fractions of the same surface with no way to know their coverage gaps |
| W3 | Side-door classes per-story — the exposed panel appears in the anecdote; the CLASS (abandoned subdomain, open directory, backup archive, staged storage) is implicit | Without a class census with a completeness gate, every hunt starts from zero and the census quality is luck (the same floor every W3 names, ghost edition) |
| W4 | Archive freshness unrecorded — cached copies and old snapshots are treated as findings-relevant without as-of dates | A panel in a 3-year-old archive snapshot is a memory, not an exposure; the story-form cannot tell them apart and reports both as "found" |
| W5 | The no-trace discipline as personal ethics — "I used public proxies, I didn't disturb anything" is narrated, not instrumented | The claim that defines the lineage (enter without knocking) is exactly the claim that needs a mechanical record: request counts per index, zero-active-touch accounting — prose cannot carry it |

## 5. Appendix — the upgrades table — and where they land (context, not steps)

| # | The should-have-been | Shipped as |
| - | -------------------- | ---------- |
| U1 | The index pass as an ordered protocol with coverage | **M1** — the index protocol |
| U2 | Side-door census with a completeness gate | **M2** — the census schema |
| U3 | Every archive hit as-of stamped | **M3** — the freshness rule |
| U4 | Found-vs-claimed differential | **M4** — the exposure differential |
| U5 | No-trace as accounting, not ethics | **M5** — the trace ledger |
