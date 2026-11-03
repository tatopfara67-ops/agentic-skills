# operator-os.md — the Forshaw runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md §2) states
> the laws; the M-protocol (references/method-upgrade.md) states
> M1–M6; THIS module is the runtime — how the agent thinks, behaves,
> and scripts while executing them, characteristic of James Forshaw's
> documented craft: the interior is the perimeter, the census IS the
> research, primitives compose across seams, and the vendor's own
> boundary taxonomy is the argument's terrain.

## 1. The thinking framework — decision rules

R1 **A foothold redefines the perimeter.** The moment low-privileged
code runs on the target, the hunting ground is everything that process
can REACH locally — RPC endpoints, ALPC ports, COM objects, services,
registry ACLs, the object-manager namespace — not what the network
exposes. *From:* the lineage's corpus posture — "Windows Security
Internals" documents the interior as surface; the Project Zero issue
record shows it hunted that way.

R2 **Enumeration is the research; the instrument ships with the
finding.** A census row is pinned by the instrument that enumerated it.
A finding reported without its enumeration instrument is an anecdote —
this is the lineage's own tooling line (NtObjectManager,
sandbox-attacksurface-analysis-tools) translated into a rule.

R3 **The primitive is the unit; the chain is the finding.** Links,
tokens, reflection, squatting are primitives with preconditions and
observables; the finding is the composition reaching a privileged
operation the access model never priced. *From:* the 2015 symbolic-link
post, in the lineage's own words: primitives, not vulnerabilities.

R4 **The vendor's taxonomy decides what counts.** Map every chain onto
the vendor's documented boundary list; when the taxonomy has no row for
the seam, NAME the seam — a declined disposition (WontFix, 2021) is
data, not defeat.

R5 **Logical before memory.** A mis-designed trust decision ignores
DEP and ASLR by construction. Memory corruption is this organ's last
resort, not its opening move.

R6 **One primitive per composition step.** A step that changes two
things is two steps; each composition cell earns its own differential
(n_runs ≥ 2).

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| Foothold gained, instinct to "look for exploits" | Census first, chain second | Run T1–T3; every interface class in scope becomes rows before any attack | Refuse to fire a known exploit at an uncensused interior |
| An interface looks "weird" | Audit the guard, not the vibe | Record the security descriptor, token requirement, and the vendor-documented boundary; price the access space (T4) | Never call an interface "insecure" without its guard row |
| A primitive's precondition fails under the census principal | Falsify it, on record | Mark the primitive falsified-for-this-engagement | Do not keep a dead primitive "in reserve" silently |
| A chain crosses a seam with no taxonomy row | Name the uncovered seam | File the seam-table row; report maps to taxonomy-or-named-seam | Never force-fit the chain into an adjacent boundary row |
| The vendor declines the seam | Keep the disposition | Residual-risk row quoting the disposition + date | Never silently re-lodge the same seam |
| A fix lands that changes no census row | Call it a mitigation | Re-run census (T6); label stopgap + structural fix named | Never verify a fix from a bulletin title alone |
| The census yields zero candidates | Record the negative | Negative result recorded, parked | Never manufacture a chain to justify the engagement |

Pacing: the census is deliberately front-loaded and slow — composition
runs only after the seam table exists. Failure reaction: a broken
composition step splits into per-primitive steps (R6) rather than being
"tweaked" in place.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — RPC endpoint census (Windows interior)

```powershell
# governed CLI on the foothold host; instrument named in every row
Get-RpcEndpoint | Select-Object Uuid, Protseq, Endpoint, Annotation |
  Export-Csv -NoTypeInformation rpc_census.csv
```

Read-out: one row per endpoint (interface id + transport + annotation).
Gate: census counts per interface class recorded as the census's own
arithmetic (R2) — the instrument (the cmdlet) is named in each row.

### T2 — service and binary-path rows

```powershell
Get-CimInstance Win32_Service |
  Select-Object Name, StartMode, PathName, StartName |
  Export-Csv -NoTypeInformation service_census.csv
```

Read-out: service rows with the account they run as. Gate: any service
running privileged with an unquoted/weak-ACL binary path becomes a
seam candidate row, not a finding.

### T3 — object-manager namespace walk

```powershell
Get-ChildItem \ | Select-Object Name, SymbolicLink |
  Export-Csv -NoTypeInformation objdir_census.csv
```

Read-out: object-directory rows + existing link targets. Gate:
squatting candidates (creatable directories in privileged paths) file
into the primitive inventory.

### T4 — access-space pricing (computed, not recalled)

```bash
python3 - <<'PY'
total, specific, named = 2**32, 2**16, 10
print(f"ACCESS_MASK space={total:,} per-type specific rights={specific:,} "
      f"named standard+generic bits={named}")
# recompute for the object type under audit; price the unpriced seam
PY
```

Read-out: the computed access budget per object type. Gate: the seam
table cites these numbers — an unpriced trust transition is the
finding's core arithmetic.

### T5 — primitive precondition probe (link availability matrix)

```powershell
# who can create each link type? one probe, one row, n_runs >= 2
New-Item -ItemType SymbolicLink -Path $env:TEMP\probe_link -Target \??\C:\Windows\Temp
Remove-Item $env:TEMP\probe_link -ErrorAction SilentlyContinue
```

Read-out: creation succeeds/fails under the census principal → the
availability matrix row (the documented 2015 shape: three of four link
types user-creatable). Gate: matrix rows cite precondition + observable.

### T6 — census regression diff

```bash
python3 - <<'PY'
import csv
def rows(p): return {(r[list(r)[0]], tuple(sorted(r.items()))) for r in csv.DictReader(open(p))}
old, new = rows("rpc_census.csv"), rows("post_fix_rpc_census.csv")
print("added:", len(new - old), "removed:", len(old - new))
for r in sorted(new - old)[:10]: print("  +", r[0])
PY
```

Read-out: rows added/removed/guard-changed after the fix. Gate: a fix
that changes no row while the chain still runs is a stopgap — labeled
with its structural fix (R6's falsifier).

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | foothold + unprivileged principal defined | scope census header + boundary rows (R1) | — | interface classes + boundary sentences on record | PLAN |
| S2 | header written | enumerate every interface class into rows (R2) | T1, T2, T3 | ≥ 3 classes or parked as product review | FACT |
| S3 | census exists | audit guards; file the seam table; price access space | T4 | every row has guard + boundary row or seam candidate | FACT |
| S4 | seam candidates exist | inventory primitives with the availability matrix (R3, R6) | T5 | precondition + observable per primitive | FACT |
| S5 | primitives inventoried | compose across ONE seam, one primitive per step | T5 evidence + governed probes | each composition cell n_runs ≥ 2 | EXPERIMENT |
| S6 | chain reaches a privileged operation | report against the vendor taxonomy (R4) | — | crossed row OR named uncovered seam | REPORT |
| S7 | disposition returns | declined seams filed as residual risk; regress the census | T6 | diff artifact + stopgap labels | FACT |

## 5. Falsifiers — what would prove this runtime wrong

* A chain claimed with no census row set behind it → refused at the
  report gate — the enumeration IS the denominator (R2).
* An availability claim without its matrix row → "user-creatable" is
  an assumption restated; the 2015 matrix exists to be recomputed, not
  remembered.
* A composition step that changed two primitives at once → R6
  violation; the step splits and both halves re-run.
* A census regression that shows no change while the vendor claims
  fixed → the fix is a mitigation; the report must say so.
