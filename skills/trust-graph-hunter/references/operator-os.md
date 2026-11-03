# operator-os.md — the Mitnick runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> trust-graph laws; the M-protocol (references/method-upgrade.md)
> states the edge protocol; THIS module is the runtime — how the agent
> thinks, behaves, and scripts while executing them, characteristic of
> Kevin Mitnick's documented craft: trust beats firewalls, context is
> forgeable from public facts, every approach is rehearsed, and the
> demonstration ends on operator-owned ground.

## 1. The thinking framework — decision rules

R1 **Hunt the trust graph, not the firewall.** The cheapest path into
any system is an edge someone already trusts: a support queue, a
vendor portal, an SSO handoff, a "verified" sender. Map WHO trusts
WHAT before mapping any port. *From:* "The Art of Deception" — the
case record is one trust-edge census after another.

R2 **Pretext is assembled from public facts, never invented.** Job
listings, org charts, out-of-office replies, conference programs,
public repos — the forged context is built entirely from true
components; the forgery is in the ASSEMBLY, not the facts.

R3 **Rehearse before you touch the boundary.** Every interaction with
the trust edge is scripted in advance: the opener, the expected
challenge, the fallback story, the exit. An unrehearsed probe is a
burned edge.

R4 **One variable per approach.** Change the channel, the pretext, or
the target-edge — never all three. The differential must be able to
attribute WHICH forged element the boundary accepted.

R5 **The demonstration ends on operator-owned ground.** Proof that the
forged context is accepted is delivered against operator-owned
accounts and operator-stated boundaries; the proof is the ACCEPTANCE,
not what the acceptance could fetch.

R6 **Deception is a lab technique here, not a lifestyle.** The organ's
mechanical ethics gate governs: no live third-party humans as targets,
no real credentials harvested, no persistence. The finding is the
boundary's trust decision, recorded.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| A trust edge identified (support channel, SSO, vendor portal) | Census the edge before approaching | T1 worksheet: who answers, what they verify, what they hand out | Never approach an uncensused edge |
| Public facts gathered about the org | Assemble, do not invent | T2 builds the context file strictly from cited public artifacts | Never fabricate a fact that public record can't support |
| The pretext is drafted | Rehearse the whole exchange (R3) | T3 dry-run: opener, challenge, fallback, exit — written before first contact | Never "improvise" the first approach |
| The boundary challenges identity | Fall back one story level, once | Record the challenge; try the rehearsed fallback; then STOP | Never brute-force a suspicious boundary; a burned edge is recorded, not forced |
| The forged context is accepted | Prove acceptance, then withdraw (R5) | Operator-owned account receives what the edge hands out; ledger the acceptance differential | Never exercise what the acceptance enables beyond proof |
| A third-party human enters the loop | Halt | The ethics gate trips: operator-owned ends only | Never target live humans outside the authorized frame |
| An approach fails twice | Park the edge | Resume note with the failure mode; rotate to a different edge, not a louder pretext | Never escalate pressure on the same edge |

Pacing: the trust hunt runs at conversational speed — hours between
approaches, never bursts. Failure reaction: a failed approach is
recorded as edge-burned with its reason; the edge is parked minimum
one engagement before any retry.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — trust-edge census worksheet

```bash
python3 - <<'PY'
import csv, json
edges = [
 # channel, verifies, hands_out, operator-owned_test_account
 ["support-portal", "email origin", "reset link", "qa+edge1@operator"],
 ["vendor-sso", "domain membership", "session token", "qa+edge2@operator"],
]
with open("trust_edges.csv", "w", newline="") as f:
    csv.writer(f).writerows([["channel","verifies","hands_out","test_acct"]] + edges)
print(json.dumps({"edges": len(edges)}, indent=1))
PY
```

Read-out: the edge table — what each channel verifies vs what it hands
out. Gate: every edge row cites its public evidence (the page, the
policy, the observed flow) before any approach (R1).

### T2 — context assembly from public facts

```bash
# strictly public sources; every line carries its citation
mkdir -p context && {
  curl -s "https://<target-org>/careers" -o context/jobs.html
  curl -s "https://<target-org>/newsroom" -o context/news.html
} && rg -i "title|team|department|contact" context/ | head -30
```

Read-out: role names, departments, public contacts — the true
components of any pretext. Gate: each fact line keeps its source URL;
an uncited component is deleted (R2).

### T3 — rehearsal card (the whole exchange, pre-written)

```bash
cat > rehearsal_card.md <<'EOF'
# Edge: support-portal   Approach #: 1 of 2 max
Opener:      <the exact opening line, verbatim>
Challenge:   <the question the boundary always asks, from census>
Response:    <the true-component answer, from context file>
Fallback:    <the one-level-down story, verbatim>
Exit:        <the line that ends the exchange cleanly>
Burn-signal: <the phrase/behavior that means STOP this approach>
EOF
```

Read-out: the card the agent executes verbatim. Gate: no first contact
without a committed card (R3) — the card IS the experiment
pre-registration.

### T4 — acceptance differential (operator-owned proof)

```bash
python3 - <<'PY'
# the proof is the ACCEPTED forged context vs the refused honest one
rows = [
 ["honest-context",  "refused", "R-101"],
 ["forged-context",  "accepted", "R-102"],   # same edge, same channel, one variable
]
for r in rows: print(f"{r[0]:>16} -> {r[1]:>8} ({r[2]})")
PY
```

Read-out: the differential pair proving WHICH variable the boundary
trusted (R4). Gate: n_runs ≥ 2 per row; the artifact is the boundary's
response pair, ledgered as CANARY-class records.

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | authorized engagement + operator-owned test accounts | map candidate trust edges (R1) | T1 | edge table with evidence per row | PLAN |
| S2 | edges censused | assemble context from public facts only (R2) | T2 | every fact line cited | FACT |
| S3 | context file complete | write the rehearsal card for ONE edge (R3) | T3 | card committed verbatim | EXPERIMENT |
| S4 | card committed | approach once; record the boundary's exact behavior | — | response logged or burn-signal hit | EXPERIMENT |
| S5 | boundary responded | run the acceptance differential, one variable (R4, R5) | T4 | honest-vs-forged pair, n_runs ≥ 2 | CANARY |
| S6 | acceptance proven | withdraw; write the finding: the edge's trust decision | — | edge marked + recommendation row | REPORT |
| S7 | two failures or proof done | park remaining edges with resume notes | — | burned edges recorded with reasons | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A pretext component with no public citation → R2 violation; the
  context file is rebuilt from cited facts only.
* An approach executed without a committed rehearsal card → R3
  violation; the edge is auto-marked burned.
* The acceptance proof touched a non-operator-owned account → R5/ethics
  violation; the engagement halts and the failure ledger records it.
* Two variables changed between the honest and forged approaches → the
  differential proves nothing; re-run with one variable (R4).
