# operator-os.md — the Mitnick + Metcalf trust runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> trust-graph laws; the M-protocol (references/method-upgrade.md)
> states the edge protocol (M1–M5) and the directory extension
> (M6–M9); THIS module is the runtime — how the agent thinks,
> behaves, and scripts while executing them, characteristic of
> Kevin Mitnick's documented craft (trust beats firewalls, context
> is forgeable from public facts, every approach is rehearsed, the
> demonstration ends on operator-owned ground) and of Sean
> Metcalf's documented craft (rights are the union of eight
> sources, the mechanism is stated before the technique, every
> technique priced by position/contact/signal, defense validated
> as tier rows, attribution on record). R1–R6 and T1–T4 carry the
> Mitnick runtime; R7–R12 and T5–T8 carry the Metcalf extension.

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

### 1b. The Metcalf rules (R7–R12, v1.3.0 — the directory extension)

R7 **Membership is one source of eight; the census reads all eight.**
A principal's real power is the union of membership, computer rights,
ACL delegation, SIDHistory, GPO rights, user-rights assignments, local
groups, and share delegation — the escalation paths live in the seven
everyone skips. *From:* the documented key point of the scanning
corpus: "rights to Active Directory and key resources is more than
just group membership, it is the combined rights".

R8 **Mechanism before technique.** Name who signs what, which service
validates it, and what contact is required — THEN price the
technique. A golden ticket is "a TGT encrypted by the KRBTGT hash,
no AS-REQ, KDC checks the account only after 20 minutes"; a silver
ticket is "a TGS encrypted by the service hash, no DC contact at
all". The mechanism is the price's ingredients. *From:* every attack
post in the corpus opens with the authentication flow, steps 1a
through 6, before any exploit.

R9 **Every technique is a priced door, and the price has three
columns: position, contact, signal.** Cheaper position wins: the
SYSVOL read prices before ticket forgery; the no-DC-contact paths
price above the DC-contact ones for stealth. *From:* the corpus's own
ordering instinct — "the simplest since no special tool is
required" — made into a law.

R10 **The boundary is the forest, not the domain.** Any trust
question inside a forest resolves at forest scope: SIDHistory carries
RID 519 across domains; a child-domain compromise prices a
forest-wide path. *From:* the documented statement — "the Active
Directory domain is not the security boundary; the AD forest is".

R11 **Attack, detection, mitigation ship as one record — and the
indicator rots while the method class persists.** Every priced path
carries its event IDs and its honest half-life; an indicator stated as
permanent is a false guarantee. *From:* the on-record sequence — the
original golden-ticket detection indicator (2015) was closed by a
mimikatz update (2016-01-05), documented as an honest update note,
while the technique itself was untouched.

R12 **Attribute the tool, price the method.** The corpus credits
every technique's author inline — Delpy (mimikatz), Le Toux (DCSync),
Duckwall (the golden-ticket presentation), Medin (Kerberoast), Monné
(PyKEK), harmj0y (PowerView), Wald0 (BloodHound's ACL graph) — and
so does every record this runtime writes. Detection prices the
METHOD (the protocol behavior), never the tool artifact. *From:* the
corpus's own reference sections and its documented rule — "it's
better to focus on detecting the method instead of specific
artifacts".

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

### 2b. The directory rows (Metcalf extension — v1.3.0)

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| An identity directory is in scope | Census all eight right sources before any technique talk | T5 seeds the principals; T6 resolves nesting; every DIR-EDGE row cites its read | Never present group membership as the privilege picture |
| A technique is named in planning | State its mechanism and price it (R8, R9) | PATH row: position + contact + signal — before any further discussion | Never execute a technique on live estate to "see if it works" (hard rule 6) |
| A principal shows an unexpected right | Ask what ELSE that right composes into | the inheritance chain is followed (R7): delegation → WriteDACL → new edges; forest scope checked (R10) | Never stop at the first surprising group membership |
| A tier boundary is claimed to hold | Validate it mechanically (M8) | T8 runs the pass/fail rows with evidence reads — KRBTGT rotation, password lengths, replication rights | Never accept hardening prose as a validation |
| A finding is drafted | Pair its detection row at birth (R11) | DETECT row: event IDs, filter, baseline rate, rot statement | Never ship an attack row without its signal, or a signal without its rot |
| A tool is credited in a draft | Attribution row, every time (R12) | the record names the technique's documented author | Never price detection on a tool artifact instead of the method |
| A recovery plan proposes ONE KRBTGT reset | Correct it — the 2× law | both modes stated: maintenance (converge 12–24 h between resets) vs breach double-tap | Never let an incomplete recovery pass as remediated |

Pacing: the directory tier is a patient read-only census — one
variable per query, rows ledgered as they land. Failure reaction: a
census source that cannot be read is GAPED, named, and excluded from
claims — never silently skipped; an observed power exceeding the
census union re-opens the census (M6's falsifier), it does not get
explained away.

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

### 3b. The directory arsenal (T5–T8, v1.3.0 — the Metcalf extension)

Every command below is a READ-ONLY, standard, authenticated LDAP
search an in-scope account can issue (hard rule 6). Placeholders:
`<dc-host>` = a domain controller reachable in scope, `<base>` = the
naming context (e.g. `DC=corp,DC=example`).

### T5 — the directory census seed (the privileged-principal read)

```bash
# one read seeds the census: every principal SDProp has flagged
ldapsearch -x -H ldap://<dc-host> -b "<base>" -LLL \
  '(AdminCount=1)' sAMAccountName objectSID memberOf \
  servicePrincipalName pwdLastSet > dir-seed.ldif
rg -c '^dn:' dir-seed.ldif   # the seed row count
```

Read-out: the seed list of privileged principals with their SPNs,
membership, and password ages — the interesting-principals RID
table cross-checks it (RID 512/518/519/548/550/551/520/1102 must
appear or the gap is named). Gate: the census is not "done" — the
seed is one of EIGHT sources; a report presenting only this read
fails M6.

### T6 — the membership chain resolution (nesting made effective)

```bash
# read-only: the group table, then nesting resolved transitively
ldapsearch -x -H ldap://<dc-host> -b "<base>" -LLL \
  '(objectClass=group)' sAMAccountName member > groups-flat.ldif
python3 - <<'PY'
import re
members, cur = {}, None
for line in open("groups-flat.ldif", encoding="utf-8", errors="replace"):
    if line.startswith("dn:"):
        m = re.search(r'CN=([^,]+),', line)
        cur = m.group(1).lower() if m else None
        members.setdefault(cur, set())
    elif line.startswith("member:") and cur:
        m = re.search(r'CN=([^,]+),', line)
        if m:
            members[cur].add(m.group(1).lower())

def effective(group, seen=None):
    seen = set() if seen is None else seen
    if group in seen or group not in members:
        return set()
    seen.add(group)
    out = set()
    for m in members[group]:
        out.add(m)
        out |= effective(m, seen)
    return out

for g in sorted(members):
    eff = effective(g)
    nested = {m for m in eff if m in members}
    if nested:
        print(f"{g}: effective={len(eff)} through-nesting={sorted(nested)}")
PY
```

Read-out: the effective-membership table with the nesting chains
named per row (source 1 closed). Gate: a cycle is PARKED and named,
never silently truncated; every group whose effective set exceeds
its flat set is a DIR-EDGE candidate for the other seven sources.

### T7 — the path pricing table (the valuation computed, not vibes)

```bash
python3 - <<'PY'
# PATH rows priced from the census: position | contact | signal
rows = [
 # technique,            position,                          contact,        signal
 ["sysvol-gpp-read",     "any-authenticated",               "none",         "none distinctive"],
 ["kerberoast",           "any-authenticated + SPN target",  "DC-TGS",       "4769 0x17 bursts"],
 ["credential-shuffle",  "local-admin on any host",          "none",          "local auth logs only"],
 ["silver-ticket",        "one service/computer hash",       "none",          "target-server events only"],
 ["golden-ticket",        "krbtgt hash",                     "DC-TGS",       "account may not exist; 20-min window"],
 ["dcsync",               "replication rights",              "DC-replication", "DsGetNCChanges from non-DC IP"],
]
# price-rank = cheapest qualifying position; operator positions FAIL to M8
print(f"{'technique':<20} {'contact':<16} signal")
for t, pos, con, sig in sorted(rows, key=lambda r: (r[2], r[0])):
    print(f"{t:<20} {con:<16} {sig}")
PY
```

Read-out: the valuation table ordered by contact cost — the report's
own copy of which doors the client's adversaries would buy first.
Gate: a row only ships when the census shows its position EXISTS in
the estate; a row whose position the OPERATOR already holds is a
tier-validation failure (M8), not an attack row.

### T8 — the tier validation runner (pass/fail with evidence reads)

```bash
# KRBTGT rotation row: pwdLastSet vs the domain's creation
ldapsearch -x -H ldap://<dc-host> -b "<base>" -LLL \
  '(sAMAccountName=krbtgt)' pwdLastSet whenCreated > krbtgt.ldif
python3 - <<'PY'
import re
epoch = (1601, 1, 1)
def filetime_to_date(ft):
    import datetime
    return datetime.datetime(1601, 1, 1) + datetime.timedelta(seconds=int(ft) / 1e7)
vals = dict(re.findall(r"^(\w+): (.+)$", open("krbtgt.ldif").read(), re.M))
if "pwdLastSet" in vals and vals["pwdLastSet"].isdigit() and int(vals["pwdLastSet"]) > 0:
    print("krbtgt pwdLastSet:", filetime_to_date(vals["pwdLastSet"]).date())
else:
    print("krbtgt pwdLastSet: never (set at domain creation)")
print("domain whenCreated:", vals.get("whenCreated", "?"))
# pass|fail row: rotation within policy window? 2x-reset law stated?
PY
```

Read-out: the KRBTGT rotation row with its evidence — `pwdLastSet`
never changed since creation is the documented default and a FAIL;
the recommendation carries BOTH reset modes (maintenance:
reset → converge 12–24 h → reset; breach: double-tap, all tickets
dead, service restarts expected). Gate: every TIER row ships
pass|fail + the read that decided it — prose-only advice fails M8.

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

### 4b. The directory tier (S8–S12, v1.3.0 — the Metcalf extension)

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S8 | an identity directory is in scope (authorized, read-only account) | run the eight-source census; seed with AdminCount + the RID table (R7) | T5 | seed rows cited base+filter; sources beyond the seed scheduled or GAPED | FACT |
| S9 | seed landed | resolve effective membership + walk the other seven sources (R7, R10) | T6 | nesting chains named; forest scope stated; DIR-CENSUS mask filled | FACT |
| S10 | census closed or honestly gapped | price every qualifying path: position → technique → contact → signal (R8, R9) | T7 | price table filled from census rows only; operator-position rows routed to S11 | REPORT |
| S11 | price table done | run the tier validation rows, pass/fail with evidence (R8; M8) | T8 | every row pass|fail + read; KRBTGT recommendation carries both reset modes | REPORT |
| S12 | tier rows done | pair every priced path with its DETECT row + rot caveat; exit | — | no attack row without its signal; no signal without its rot; census gaps named | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A pretext component with no public citation → R2 violation; the
  context file is rebuilt from cited facts only.
* An approach executed without a committed rehearsal card → R3
  violation; the edge is auto-marked burned.
* The acceptance proof touched a non-operator-owned account → R5/ethics
  violation; the engagement halts and the failure ledger records it.
* Two variables changed between the honest and forged approaches → the
  differential proves nothing; re-run with one variable (R4).
* A directory technique EXECUTED against live estate instead of priced
  → hard-rule-6 violation: the run halts, the row is withdrawn, and
  the incident is ledgered before anything else happens (R9, R12).
* A census row without its LDAP read cited → the row is not evidence;
  re-issue the read or drop the claim (M6 gate).
* A DETECT row shipped without its rot statement → the record is
  incomplete by M9; the finding is returned to draft until paired
  (R11).
