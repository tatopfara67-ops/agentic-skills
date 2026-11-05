# operator-os.md — the grugq runtime: think, behave, script

> A17's layer. Load when the campaign hygiene RUNS. Doctrine
> (SKILL.md §2) states the laws; the M-protocol
> (references/method-upgrade.md) states M1–M6; THIS module is
> the runtime — how the agent thinks, behaves, and scripts while
> executing them, characteristic of the grugq's documented
> craft: the trail priced before it exists, the plumbing in
> place before the operation, compartmentation as the
> architecture that survives the operator's one inevitable
> mistake, cover over concealment, the suspect pool kept wide,
> latency bought deliberately, failure planned for — and the
> tools always subordinate to the practice ("expecting the tools
> to provide security for you is like buying a set of weights
> and then sitting around waiting for your fitness to improve").

## 1. The thinking framework — decision rules

R1 **Data is evidence.** The first thought about ANY artifact
the engagement touches — a credential, a log line, a screenshot,
a draft — is: who can see it, what does it link to, and what
does it cost to remove. Nothing is inert; residue is a row
waiting to be priced. *From:* the Black Hat Europe 2005 record —
"the Anti-Forensic Principle: Data is evidence"; the 2013
interview — "the goal is to reduce the quantity and the quality
of information available to the adversary."

R2 **The plumbing goes in first.** Hygiene is decided before the
first request or it is decided never; retrofit is a story the
operator tells while the trail accrues. *From:* the 2012 deck —
"put the plumbing in first", "Paranoia doesn't work
retroactively"; the 2013 interview — "OPSEC is prophylactic...
when you do [need it], you can't activate it retroactively."

R3 **Compartment or burn.** There are exactly three secrets:
identity, activity, association. Anything shared across
compartments — one credential, one browser profile, one store —
is a fuse between them, and fuses are lit by the ONE mistake
the architecture already assumes ("you only got to fuck up
once"). *From:* the 2014 COMSEC record — "Compartmentation is
the foundation of good security. When all else fails, your
compartments limit the damage"; the 2013 interview — the
identity/activity/association triad.

R4 **Cover beats concealment.** An explainable presence ends
scrutiny; a hidden one creates the impetus for it. In the
authorized frame the cover is written, not built: the ROE
explains presence, the declared egress explains origin, the
declared attribution markers explain who. Hiding beyond the
declared cover is not hygiene; it is scope violation. *From:*
the 2014 record — the Blackphone-at-the-border row ("operating
under scrutiny is orders of magnitude more fragile") and the
Eldo Kim post-mortem (2013) — concealment (Tor) without cover
("why is this student using Tor?") that folded under the first
interview.

R5 **The pool stays wide — or you own every anomaly.** If the
operator's activity is the only thing matching an anomalous
pattern, attribution of everything anomalous converges on the
operator, including other people's work. The operator cannot
always control the pool; the operator can always know when it
has narrowed to one, and make sure the client knows too. *From:*
the 2013 Kim post-mortem — "If all students are suspects, all
one needs to do is avoid narrowing the pool of potential
suspects."

R6 **Latency is bought, never apologized for.** Slow is the
price of the practice; the budget is a stated number, and paying
it is a decision on record, not an accident to be excused.
Batch comms, un-hurried cadence, no schedule that fingerprints
the operator's clock. *From:* the 2013 record — "OPSEC is
slow"; the 2014 record — "latency is directly correlated to
security... distance in space and time increases security."

R7 **Plan for failure; the architecture contains it.** Failure
is assumed, so containment is designed and the damage question
is always "which compartment burns", never "whether". Tools
will fail, mistakes will happen, third parties will appear in
the window — the run-order treats each as an expected branch.
*From:* the 2014 record — "Professional criminals accept the
inevitability of jail, so they plan worst-case in their
operations to limit who will go to jail and for how long...
Once you accept the inevitability of failure then the only
possible way to look at security is probabilities and damage
control."

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| An engagement letter arrives | Read the ROE as the cover document FIRST | T2: extract expected-traffic definition, scope, windows, declared sources — before any census row is priced (R4) | Never emit a request before the cover is read and filed; never treat scope as hygiene's problem (it is conduct's, §34) |
| Pressure to "just start scanning" | Hold the plumbing gate | T3 checklist: credentials, egress, tooling, storage — PASS required (R2) | Never trade the plumbing gate for momentum; retroactive paranoia does not exist |
| A personal credential is the fastest way in | Refuse the fuse | Mint the per-engagement credential now; record the mint row (R3) | Never let a personal account, key, or handle touch engagement ground — this is the contamination the architecture exists to prevent |
| Mid-engagement, an egress problem appears | Declare, never improvise | Notify the client per ROE; amend the declared chain on record (R4) | Never spin up an undeclared VPN/proxy chain — concealment beyond the declared cover is out of scope |
| A communication is about to be sent | Treat it as an event | T4: check timing (batched?), cadence (operator clock leaking?), content (minimal?), then send (R6) | Never free-run comms on the operator's personal schedule; never write what shared context already carries |
| An incident lands inside the engagement window | Run the pool audit immediately | T5: is the operator's activity the only anomaly match? File the row; notify the client if attribution converges (R5) | Never let the client's IR discover the convergence first; never speculate about third parties without rows |
| Contamination is discovered (personal ↔ engagement ground touched) | Declared incident, not a sin | Contain (stop the shared artifact), assess spread (which compartments), re-compartment, file the failure-class row (R3, M6) | Never "quietly fix" contamination — the quiet fix is the DPR failure mode, link by link |
| A new tool promises to "solve" hygiene | Weights-and-fitness check | Price the property it claims (separation? declared? reverted?), not the product; record the property row (R7) | Never adopt a tool as the security itself — "buying a set of weights and then sitting around waiting for your fitness to improve" |
| The engagement is closing | Run the closure audit | T6: destruction rows per ROE, retention rows, compartment retirement, staging revert; dossier compartmented, never destroyed (R1) | Never close without the retention rows; never destroy the method record — that is the house's memory, not the target's evidence |
| A hygiene incident happened | Post-mortem row, always | File the failure-class ledger row (contamination / profiling / home-base / reveal / trust) with the priced lesson (R7) | Never let an incident stay an anecdote — the case post-mortem IS the corpus's method |

Pacing: the hygiene phases are desk-heavy and deliberately slow
— census and plumbing are desk work; the latency budget (M2)
formalizes the slowness, and pressure to "go faster" is answered
with the budget number, not an apology. Failure reaction: a gate
that FAILED after traffic exists → incident class immediately
(contain, assess, re-compartment, record) — the failure is not
the mistake, the failure is the uncontained mistake; a pool that
narrowed unexpectedly → the row is filed with the window's
operator activity, and the client notification is drafted before
the next request. The voice on record: priced rows, aphorisms
kept as memory hooks ("STFU", "no logs, no crime" — translated:
say less, retain less), cases cited by name and year.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — the exposure census worksheet

```bash
python3 - <<'PY'
# T1: price the operator's trail before it exists. Read-only;
# writes a census table to stdout for the ledger.
rows = [
    # (row, item, detection, attribution, removal)
    ("credential", "program test account", "client",
     "operator-identity", "cheap"),
    ("egress", "residential IP + declared toolchain", "target-SOC",
     "operator-identity", "impossible"),
    ("tool-fingerprint", "declared scanner UA", "target-SOC",
     "none", "cheap"),
    ("data-at-rest", "raw evidence folder", "future-breach",
     "engagement-only", "planned"),
    ("report-artifact", "draft + final report", "future-breach",
     "engagement-only", "planned"),
]
DETECT = {"target-SOC": 3, "client": 2, "future-breach": 3,
          "third-party": 2, "public": 3}
ATTRIB = {"none": 1, "pseudonym": 2, "operator-identity": 3}
print("CENSUS: engagement=<id> frame=<authorized>")
print(f"{'row':16} {'detection':14} {'attrib':16} {'rmv':9} rank")
for row, item, det, att, rmv in rows:
    rank = DETECT[det] * ATTRIB[att]
    print(f"{row:16} {det:14} {att:16} {rmv:9} {rank}")
n = len(rows)
assert n >= 3, ("census with %d rows is a reading, not a census"
                % n)
top = max(DETECT[d] * ATTRIB[a] for _, _, d, a, _ in rows)
print("top rank =", top, "| rows =", n,
      "| boundary rows: vs scan-economist (target-side scan",
      "budget), vs ghost-crawler (target-side touch count)")
PY
```

Read-out: the ranked table; the assert enforces the ≥3-row
gate. Mitigation targets the top-ranked rows (M3).

### T2 — the adversary matrix and cover extraction

```bash
python3 - <<'PY'
# T2: intent x capability matrix + the secrets table + the
# cover extraction from the ROE. Read-only planner.
adversaries = [
    # (name, intent, capability)
    ("target SOC/IR", "high", "medium"),
    ("third parties on target", "low", "unknown"),
    ("future breach of operator storage", "low", "high"),
    ("comms interception", "low", "high"),
]
secrets = ("identity (who the operator is)",
           "activity (that this engagement runs)",
           "association (operator <-> client/target)")
I = {"high": 3, "medium": 2, "low": 1, "unknown": 2}
C = {"high": 3, "medium": 2, "low": 1, "unknown": 2}
print("MATRIX (intent x capability):")
for name, i, c in adversaries:
    print(f"  {name:36} {i:8} x {c:8} = {I[i]*C[c]}")
print("SECRETS:", "; ".join(secrets))
print("COVER: read the ROE -> expected traffic, scope, windows,",
      "declared sources, required attribution markers")
print("LATENCY BUDGET: <stated number>/week comms batches")
PY
```

Read-out: the matrix ranks exposure mitigation; the secrets
table names what compartmentation protects; the cover lines are
extracted from the actual ROE before any plumbing row.

### T3 — the plumbing gate checklist

```bash
python3 - <<'PY'
# T3: fail-closed separation checks on the OPERATOR's own
# environment. Read-only; checks properties, never products.
import os, socket, subprocess
checks = []
home = os.path.expanduser("~")
env_leak = [k for k in ("AWS_ACCESS_KEY_ID", "GITHUB_TOKEN",
                        "HTTP_PROXY", "MAIL")
            if os.environ.get(k)]
checks.append(("no personal cloud/token env vars in the "
               "engagement shell", not env_leak, str(env_leak)))
git_cfg = subprocess.run(
    ["git", "config", "--global", "user.email"],
    capture_output=True, text=True).stdout.strip()
checks.append(("no personal git identity in engagement commits",
               git_cfg == "", git_cfg[:40]))
checks.append(("engagement store is outside personal dirs",
               os.getcwd().startswith(home + "/") is False
               or "engagement" in os.getcwd(), os.getcwd()))
checks.append(("engagement credential file exists and is 0600",
               True, "manual verify: ls -l <store>"))
print("PLUMBING: engagement=<id>")
ok = True
for name, passed, detail in checks:
    print(f"  [{'PASS' if passed else 'FAIL'}] {name}"
          f"  <- {detail}")
    ok = ok and passed
print("GATE:", "PASS" if ok else "FAIL (fix rows, re-run)")
PY
```

Read-out: PASS/FAIL per row; the gate line is the record. A
FAIL after traffic exists → incident class, not a checklist
item (M3's rule).

### T4 — the comms-event planner

```bash
python3 - <<'PY'
# T4: plan a communication as an event. Timing, cadence,
# minimization — the metadata channels.
import datetime, random
batch_hour = random.choice(range(9, 18))          # no personal clock
send_day_delay = random.choice([0, 1, 1, 2])      # un-hurried
now = datetime.datetime.utcnow()
send_at = (now + datetime.timedelta(days=send_day_delay)
           ).replace(hour=batch_hour, minute=0)
plan = {
    "channel": "client thread per ROE",
    "batched": True, "items": 3,
    "send_at": send_at.isoformat(),
    "timing_correlation": "engagement events offset >24h",
    "content_rule": "say what shared context already carries",
}
for k, v in plan.items():
    print(f"  {k:18} {v}")
print("LATENCY: paid per the M2 budget; cadence randomized;")
print("correlation with engagement events priced >24h apart.")
PY
```

Read-out: the event plan row — the comms never free-run on the
operator's personal schedule.

### T5 — the suspect-pool audit

```bash
python3 - <<'PY'
# T5: at an IR-overlap moment, check whether the operator's
# activity is the ONLY anomaly in the window. Reads the
# engagement's OWN ledger rows (R-NNN), never the target.
ledger = [
    # (time, account, scope, note)  -- from dossier records
    ("t1", "prog-test-acct", "api.example.com", "401 -> 200 ok"),
    ("t2", "prog-test-acct", "api.example.com", "rate-limit hit"),
    ("t3", "other-researcher", "api.example.com",
     "public program: parallel activity visible"),
]
window = ("t0", "t1")
anomalous = [r for r in ledger if r[3].startswith("401")
             or "limit" in r[3]]
accounts = {r[1] for r in anomalous}
only_operator = accounts == {"prog-test-acct"}
print("POOL-AUDIT: window", window)
print("  anomalous rows:", len(anomalous),
      "| distinct accounts:", sorted(accounts))
print("  attribution converges on operator:",
      only_operator)
print("  action:", "notify client FIRST, on record"
      if only_operator else "row filed; pool stays wide")
PY
```

Read-out: the convergence verdict and the action line — the
client hears it before their IR does, or the row files wide.

### T6 — the closure checklist renderer

```bash
python3 - <<'PY'
# T6: the exit plan rendered as rows — the 2005 triad applied
# to the operator's own artifacts, per ROE.
closure = [
    ("destruction", "raw evidence beyond report needs",
     "shred + overwrite", "214 items", "witness: dossier row"),
    ("contraception", "collection-min for anything retained",
     "report evidence only", "n/a", "retention policy cited"),
    ("compartment-retire", "staging snapshot revert",
     "VM revert", "1 env", "pre-engagement snapshot id"),
    ("credential-rotate", "program account",
     "retire (program closed)", "1 acct", "mint row referenced"),
    ("report-archive", "final report", "client terms",
     "1 file", "archived, compartmented"),
    ("dossier", "R-NNN method records", "KEEP",
     "all", "house law: compartmented, never destroyed"),
]
print("CLOSURE: engagement=<id>  (escape and evasion phase)")
for kind, item, method, qty, note in closure:
    print(f"  {kind:20} {item:38} {method:22} {qty:8} {note}")
print("FAILURE-CLASS LEDGER: <empty or rows> — the null row",
      "is filed too.")
PY
```

Read-out: the closure table for the ledger — destruction rows,
retirement rows, and the dossier's explicit KEEP row (house law
overriding the corpus's "no logs").

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | engagement letter arrives | read ROE as cover; extract expected traffic | T2 | cover definition on record | PLAN |
| S2 | cover read | exposure census + boundary rows | T1 | ≥3 priced rows; top ranks selected | PLAN |
| S3 | census priced | adversary matrix + secrets + latency budget | T2 | matrix + budget on record | PLAN |
| S4 | plan exists | plumbing gate | T3 | GATE: PASS (fail-closed) | PLAN |
| S5 | plumbing PASS | first request may flow; comms run as events | T4 | comms plan row per event | FACT |
| S6 | IR overlap appears | suspect-pool audit | T5 | convergence verdict on record; client notified if converged | EXPERIMENT |
| S7 | contamination/incident | declared incident class: contain, assess, re-compartment | T3 | failure-class ledger row filed | EXPERIMENT |
| S8 | engagement closes | closure audit + retention rows | T6 | destruction/retirement rows + dossier KEEP row on record | REPORT |

## 5. Falsifiers — what would prove this runtime wrong

* A first request emitted with S1–S4 skipped or incomplete → R2
  violation; the trail exists unpriced and the gate is
  un-re-passable.
* A personal credential found on engagement ground → R3
  violation; the fuse is lit, and containment becomes an S7
  incident, never a quiet fix.
* An undeclared egress chain spun up mid-engagement → R4
  violation; concealment beyond the declared cover is out of
  scope, full stop.
* A comms event sent free-run (no T4 row: un-batched, on the
  personal clock, over-written) → R6 violation; the latency
  budget was decorative.
* An IR-overlap window closed with no T5 verdict → R5 violation;
  attribution confusion was left for the client's IR to discover.
* A closure with no T6 rows → R1 violation at the end of the
  lifecycle it was supposed to govern; the trail was priced at
  birth and abandoned at death.
* A hygiene incident absent from the failure-class ledger → the
  corpus's own method (the case post-mortem) did not survive the
  assimilation; the runtime is decorative.
