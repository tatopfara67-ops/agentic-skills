# operator-os.md — the Tomnomnom runtime: notice, think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> Unix-philosophy laws; the M-protocol (references/method-upgrade.md)
> states the pipeline records and collapse ledger; THIS module is the
> runtime — how the agent notices, thinks, behaves, and scripts while executing
> them, characteristic of Tom Hudson's documented craft: small
> composable tools, passive first, dedupe before probes, and the diff
> IS the decision.

## 1. The thinking framework — decision rules

R1 **Passive sources before active packets — always.** Wayback,
certificate transparency, public repos, and archives produce the
candidate set; an active probe exists only to VERIFY a passive
candidate. *From:* the lineage's toolset (waybackurls, assetfinder) —
the pipeline's input end is entirely passive.

R2 **One tool, one job, connected by pipes.** assetfinder finds;
httprobe checks; gf filters; meg fetches. A tool that does two jobs
cannot be reasoned about in a pipeline — compose, don't monolith.

R3 **Dedupe before you probe.** Cross-source collapse (the M-protocol's
collapse ledger) runs before any network contact; duplicates are paid
for twice if not collapsed once.

R4 **The diff decides.** Two pipeline states (yesterday vs today,
live vs archive, source-A vs source-B) compared mechanically — new
lines ARE the signal. Human eyeballs on big lists are the failure
mode.

R5 **As-of stamps on everything.** Every pipeline output carries its
generation timestamp and source versions; an undated list is a rumor.

R6 **Small outputs, cited stages.** Each stage's row count is a
citation ("1,204 hosts from waybackurls at 2026-11-03"); the replay
runs five-field citations — tool, version, input, flags, stamp.

### The opening ladder — the pattern is the hypothesis

The rules above keep the pipeline honest. The ladder is the lineage's
actual craft: the tools generate the mass (waybackurls, assetfinder),
and the perception SELECTS — the passive mass filtered by named
patterns, each pattern a hypothesis about what neglect looks like.
Every rung is a question over pipeline rows; no rung adds a probe —
R1's verify-only boundary holds.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | What did the estate ever publish that it stopped advertising? | archived paths absent from the live surface — the historical admission nobody retracted | waybackurls — the lineage's own input end |
| G2 | Which file shapes mean "left behind"? | environment files, VCS directories, dumps, backups — the shapes haste leaves when it moves fast | the gf tradition — named pattern families as selection |
| G3 | Which parameter families mean "old code path"? | debug, test, and verbose keys in archived URLs — parameters are code paths exposed in public | same — the pattern IS the hypothesis |
| G4 | What is new since the last run? | diff lines only — the estate's freshest mistakes, R4's rule read as generation | the lineage's diff-first doctrine |
| G5 | Which hosts appear in exactly ONE source? | single-source hosts — the estate doesn't know them either; uncorroborated means unmanaged | the collapse ledger read as signal instead of hygiene |

Ranking rationale: yield priors per pattern family × freshness.
Each pattern family carries its historical hit rate (R5's "priors
are data" applied to patterns); new diff lines outrank the stale
mass — a fresh residue row beats a two-year-old path, because
fresh neglect is live neglect.

Generation falsifier: zero leads from a full passive mass means a
pattern family is MISSING, not the estate clean — the mass is
re-read for the shape no current pattern selects, and the new
pattern is written, named, and versioned (R2: one job).

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| Engagement opens | Build the passive pipeline, touch nothing active | T1 runs the source chain; collapse ledger written | Never open with an active sweep |
| Two sources disagree on a host | Collapse with a cross-source gate | T3 records the host with per-source bits; the gate decides inclusion | Never resolve conflicts by sending packets |
| A big candidate list emerges | Diff it against the last run's state | T4 diffs; only NEW lines move forward | Never re-probe the whole list each run |
| A stage gets slow | Split it, don't scale it | The slow stage becomes two piped stages with counts | Never "just add threads" to a bloated stage |
| Active verification is finally needed | Hand off to the probing organs | Candidates exported with stamps for governed probes | Never let the pipeline itself start spraying |
| A source rate-limits | Back off and record the partial | Output stamped "partial, source capped"; resume note | Never rotate identities to dodge a public API's limit |
| Findings day arrives | Cite stages, not vibes | Every reported surface traces to a pipeline row | Never report a surface the pipeline can't replay |

Pacing: the pipeline is bursty — long quiet passive phases, then short
governed verification windows. Failure reaction: a broken stage is
replaced by TWO smaller stages (R2), never patched into a bigger one.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — the passive source chain

```bash
# compose small tools; every stage counts its lines
assetfinder --subs-only <target-domain> | sort -u > hosts_raw.txt
cat hosts_raw.txt | httprobe --prefer https | tee hosts_live.txt | wc -l
```

Read-out: raw host set → live host set, with counts per stage. Gate:
stage outputs stamped (T2); raw and live both kept for replay (R5).

### T2 — as-of stamping

```bash
stamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
{ echo "# as-of: $stamp"; echo "# sources: assetfinder=$(assetfinder --version 2>&1 | head -1)"; cat hosts_raw.txt; } \
  > "hosts_raw.$stamp.txt"
```

Read-out: versioned, source-attributed snapshots. Gate: an unstamped
list cannot feed the next stage (R5).

### T3 — cross-source collapse gate

```bash
python3 - <<'PY'
import itertools
sources = {"assetfinder": {"a.target", "b.target"},
           "crtsh":       {"a.target", "c.target"},
           "wayback":     {"b.target", "d.target"}}
all_hosts = sorted(set().union(*sources.values()))
for h in all_hosts:
    bits = "".join("1" if h in s else "0" for s in sources)
    print(f"{h:20} {bits} include={'yes' if bits.count('1') >= 1 else 'no'}")
PY
```

Read-out: the collapse ledger — per-host source bits + the inclusion
decision. Gate: the gate rule is stated (≥1 source here; the
M-protocol's cross-source rule governs on record) (R3).

### T4 — the deciding diff

```bash
diff <(sort -u hosts_live.previous.txt) <(sort -u hosts_live.txt) \
  | grep '^>' | sed 's/^> //' | tee hosts_new.txt | wc -l
```

Read-out: ONLY the new lines move to verification. Gate: re-probing
known-live hosts without a diff reason is refused (R4).

### T5 — pattern-pack filtering

```bash
# gf-style pattern packs: filter what the next stage needs, cite the pack
cat hosts_live.txt | gf redirects > candidates_redirects.txt; wc -l candidates_redirects.txt
```

Read-out: class-filtered candidate files. Gate: the pack name + version
cited in the stage log (R6 — pattern packs are data, versioned).

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | authorized domain/scope | run the passive chain, stamped | T1, T2 | source counts + stamps on record | FACT |
| S2 | raw candidates exist | collapse cross-source with the gate | T3 | collapse ledger complete | FACT |
| S3 | collapsed set ready | probe liveness once per host | T1 (httprobe stage) | live set + counts | EXPERIMENT |
| S4 | live set current | diff vs previous state | T4 | only-new list produced | FACT |
| S5 | new lines exist | filter by pattern packs; export to probing organs | T5 | pack citations + export rows | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* An active packet sent before the collapse ledger exists → R1/R3
  violated; the run restarts at the passive phase.
* A reported surface with no pipeline row behind it → unreplayable;
  refused at the report gate (R6).
* Undated lists found feeding active stages → R5 violation; the stage
  is re-stamped and re-run.
* A stage that silently grew two jobs → R2 violation; split it or the
  pipeline's audit property is broken.
