# operator-os.md — the Parecki runtime: notice, think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> flow laws; the M-protocol (references/method-upgrade.md) states the
> flow-pin and exactness protocol; THIS module is the runtime — how
> the agent notices, thinks, behaves, and scripts while executing them,
> characteristic of Aaron Parecki's documented craft: pin the exact
> flow first, exactness is a differential, state and PKCE are tested
> as behavior — and token lifetimes are arithmetic.

## 1. The thinking framework — decision rules

R1 **Pin the flow before touching it.** Which grant, which response
type, which client, which redirect, which scopes — the flow pin is a
written record; an unpinned flow test is noise. *From:* the lineage's
documented discipline (OAuth 2.0 Simplified, the oauth.net
maintenance): name the flow precisely, then test it precisely.

R2 **Exactness is a differential, not an opinion.** redirect_uri
matching is tested by sending NEIGHBORS (case, trailing slash, path
append, fragment, subdomain-swap, open redirector) and observing
accept vs reject — the acceptance set IS the policy. Never say "sloppy
validation" without the neighbor matrix.

R3 **State and PKCE are behavior, not checkboxes.** "state present" is
step one; "state validated" is proven by tampering it and observing
rejection. A PKCE downgrade probe (authorized code flow accepting
requests without the verifier) is a first-class test.

R4 **Lifetimes are arithmetic.** Token TTL, refresh rotation, code
single-use windows — measured in seconds and counted in uses; a
lifetime claim without numbers is a vibe.

R5 **The 12-check catalog is the floor, not the ceiling.** Every organ
run walks the catalog; findings outside it are welcome but the catalog
must exit complete or explicitly parked.

R6 **Client secrets and tokens are evidence, not trophies.** Captured
artifacts (code, token) live in the ledger hashed, used once for the
proof, never replayed.

### The opening ladder — the client inventory first

T2's neighbor matrix generates variants once a flow is pinned. The
ladder runs UPSTREAM — which flows, clients, and registrations to
pin at all. The perception is inventory discipline, the lineage's
own emphasis made active: the IdP's client population is the attack
surface, and the weakest redirect lives in the crowd. Every rung
reads registration metadata and observed authorize redirects; no
rung sends a probe — the matrix is verification's tool, not
generation's.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | How many clients share this IdP? | every registered app is a surface; the count per grant type is the real scope statement | R1's pin-first discipline applied at population scale |
| G2 | Which clients still run legacy grants? | implicit and token-endpoint remnants — retired grants are the hunted class | the grant taxonomy the lineage maintains (OAuth 2.0 Simplified) |
| G3 | Which redirect registrations are widest? | prefix, regex, and wildcard registrations ranked by width BEFORE any probe — width is read from metadata, not tested | R2's exactness discipline inverted — measure the policy's shape first |
| G4 | Which flows cross origin boundaries? | custom schemes, deep links, localhost callbacks — public-client territory where client secrets cannot protect anything | the public/confidential client distinction |
| G5 | Which tokens live longest? | TTL outliers and rotation gaps — the lifetime that outlives its session | R4's arithmetic applied as ranking |

Ranking rationale: policy width × grant age × client exposure. The
widest redirect on the oldest grant in the most exposed client is
pinned first; a narrow, fresh, confidential client parks. The
ordering mirrors the failure record — OAuth incidents cluster where
registration was loose and the grant was old.

Generation falsifier: an IdP whose inventory yields nothing to pin
means the inventory READ is incomplete — a source row is missing
(an undocumented client, an internal authorize endpoint), not the
population innocent. The census re-runs before any "clean" claim.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| An OAuth surface in scope | Pin the flow from observed traffic/docs | T1 writes the flow pin record | Never test "OAuth in general" |
| redirect_uri policy unknown | Build the neighbor matrix | T2 sends the neighbor set; records accept/reject per cell | Never assert looseness from one accepted variant |
| state parameter present | Prove it is VALIDATED | T3 tampers state; observes the rejection (or its absence) | Never call state "implemented" from presence alone |
| PKCE in the flow | Downgrade probe | T4 sends the code request without the verifier pair | Never assume S256 enforcement from the docs |
| A code is captured | Use once, hash, ledger | Single exchange; hash recorded; no replays | Never replay codes "to check single-use" twice past the first |
| Refresh tokens live | Measure rotation + TTL | T5 clocks expiry + rotation behavior with timestamps | Never report lifetimes in adjectives (R4) |
| Open redirector found nearby | Cross-reference the matrix | redirect chain tested against the exactness rows | Never chain an external redirector without scope covering it |

Pacing: the matrix fills one neighbor per EXPERIMENT, spaced like a
user, not a scanner. Failure reaction: an unexpected accept (neighbor
granted) → the flow pin is RE-READ for what grant variant actually
answered — the record updates before any impact step.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — flow pin record

```bash
python3 - <<'PY'
pin = {"grant": "authorization_code", "response_type": "code",
       "client": "web-app-7", "redirect_uri": "https://app.example/cb",
       "scopes": ["openid", "profile"], "pkce_declared": "S256"}
print("FLOW-PIN:", pin)   # from observed authorize redirect, not docs alone
PY
```

Read-out: the pinned flow. Gate: every later test cites this pin (R1);
a test that cannot cite a pin is refused.

### T2 — redirect exactness neighbor matrix

```bash
python3 - <<'PY'
base = "https://app.example/cb"
neighbors = {
  "exact":        base,
  "case":         "https://APP.example/cb",
  "trailing":     base + "/",
  "path-append":  base + "/../../evil",
  "subdomain":    "https://app.example.evil.host/cb",
  "fragment":     base + "#x",
  "userinfo":     "https://app.example@evil.host/cb",
}
for name, uri in neighbors.items(): print(f"{name:12} {uri}")
PY
```

Read-out: the neighbor set (sent one per EXPERIMENT via the authorize
endpoint with the operator's own client session). Gate: the
accept/reject verdict per cell IS the policy record (R2); "loose" as a
word is refused.

### T3 — state validation differential

```bash
# tamper the state on the callback; the server's verdict is the test
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" \
  "https://<client>/cb?code=<operator-code>&state=TAMPERED-xyz"
```

Read-out: accepted (redirect to app, session minted) vs rejected
(error, dropped). Gate: "state validated" claims cite the tamper row
(R3); presence-only claims are marked UNVERIFIED.

### T4 — PKCE downgrade probe

```bash
# code flow: request the token WITHOUT the code_verifier
curl -s -X POST "https://<as>/token" -d "grant_type=authorization_code" \
  -d "code=<operator-code>" -d "redirect_uri=https://app.example/cb" \
  -d "client_id=web-app-7" | python3 -c "import json,sys; r=json.load(sys.stdin); print('DOWNGRADE-ACCEPTED' if 'access_token' in r else r.get('error'))"
```

Read-out: token granted without verifier = downgrade finding; error
row = enforcement. Gate: the probe runs on the operator's own code
from the operator's own session (R6 — artifacts hashed, used once).

### T5 — lifetime + rotation arithmetic

```bash
python3 - <<'PY'
from datetime import datetime, timezone
issued = datetime(2026, 11, 3, 12, 0, 0, tzinfo=timezone.utc)
expired = datetime(2026, 11, 3, 13, 0, 0, tzinfo=timezone.utc)
ttl = (expired - issued).total_seconds()
print(f"access_token TTL = {ttl:.0f}s ({ttl/3600:.1f}h)")
print("refresh rotation: old-token-after-rotation -> observed revoked/still-valid (row required)")
PY
```

Read-out: measured TTL + rotation behavior. Gate: lifetime sentences
carry these numbers (R4); "short-lived" without seconds is refused.

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | OAuth surface authorized | pin the flow from observed traffic | T1 | flow pin cited | PLAN |
| S2 | pin exists | run the exactness neighbor matrix | T2 | accept/reject per cell | EXPERIMENT |
| S3 | matrix done | state tamper + PKCE downgrade probes | T3, T4 | validation verdicts recorded | EXPERIMENT |
| S4 | validations verdicted | lifetimes + rotation arithmetic | T5 | TTL + rotation rows | FACT |
| S5 | deltas found | impact proof bounded to operator accounts | governed probes | ceiling stated, artifacts hashed | CANARY |
| S6 | catalog walked | exit: 12-check floor complete or parked | — | park notes per open check | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A test executed with no flow pin record → R1 violation; the result
  is unattributable and void.
* "Sloppy redirect validation" with no neighbor matrix → R2
  violation; the sentence is rewritten from the matrix or deleted.
* "state implemented" from presence alone → R3 violation; the tamper
  row is mandatory.
* Token artifacts found unhashed or replayed → R6 violation; the
  evidence chain is broken and re-collected.
