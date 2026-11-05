# operator-os.md — the Miller runtime: notice, think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> mobile teardown laws; the M-protocol (references/method-upgrade.md)
> states the teardown and boundary protocol; THIS module is the
> runtime — how the agent notices, thinks, behaves, and scripts while
> executing them, characteristic of Charlie Miller's documented craft (with
> Collin Mulliner's SMS line): the shipped binary is a confession,
> store review is a hypothesis — not a guarantee, and the findings
> land at the API boundary where the app's assumptions meet the
> server's checks.

## 1. The thinking framework — decision rules

R1 **Ship-store-run: the binary is the ground truth.** Whatever the
store review claims, the IPA/APK on the device is what executes — its
entitlements, its flags, its bundled keys are the facts. *From:* the
2011 Instastock demonstration — the store shipped a binary whose
behavior contradicted every assumption about review; code-signing held
and the signed app still misbehaved.

R2 **The API boundary is where findings land.** The app's checks
(root detection, cert pinning, input validation) are CLIENT
assumptions; the server's behavior at its endpoints is the boundary
where assumptions either hold or die. Hunt the divergence.

R3 **One attack surface class at a time.** IPC surface, deep-link
surface, local-storage surface, transport surface — enumerated as
classes before any exploitation; the class census selects the target,
not the exploit we happen to have.

R4 **Fuzz the entry points the platform hands you.** SMS, push
payloads, deep links, malformed local files — the platform feeds these
to the app unasked (the Mulliner line: the SMS stack was the surface
nobody asked for); entry-point fuzzing beats UI-poking.

R5 **Pinned or not is a measured fact.** TLS pinning presence is
tested by observation (does the app accept an operator-owned proxy
cert?), never assumed from strings alone.

R6 **The demo ends at the operator's devices and accounts.**
Demonstrations run on owned hardware with operator accounts; other
users' devices, messages, and sessions are never in scope.

### The opening ladder — where Miller's candidates come from

The rules above govern posture once a candidate exists. The ladder
produces the candidates — the documented perception (the shipped
binary read as a confession before the device is ever touched; the
entry points the platform feeds the app unasked) made runnable as
questions. Every rung reads artifacts already in hand — the pinned
binary, the platform's own documentation, the server's live
behavior; NO rung spends fuzz budget. Bounded mutation is T4's job,
and T4 fires on lab devices only (R4, R6). Rows out; anomaly budget
untouched.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | What does the shipped binary confess before anyone runs it? | manifest and Info.plist rows — exported components, URL schemes, ATS exceptions, entitlements, bundled keys: the review assumption vs. the binary fact | the Instastock lesson — the shipped binary's behavior contradicted every review assumption; reading it first is the documented posture |
| G2 | Which entry points does the platform feed the app unasked? | push payloads, SMS/MMS delivery, deep links, shared-file open requests — surfaces the app receives without initiating anything | the 2009 SMS line (with Mulliner): the surface that was compromised was the one nobody asked for |
| G3 | Where will the app's checks and the server's rules disagree? | the client-check inventory (root detection, pinning, input validation) read as hypotheses about SERVER enforcement — divergence candidates | the organ's own operationalization of the API-boundary doctrine, labeled on the sources ledger |
| G4 | What did the platform change since this binary was built? | new-OS attack surface against the pinned build — the fresh-surface question for a stale binary | the Pwn2Own pattern (2008, 2009): each new platform release is new surface, read as a candidate class |
| G5 | Which ghost endpoints does the binary still trust? | endpoints in strings and configs absent from the live server surface — stale trust speaking old protocols | the teardown ladder's ghost-endpoint diff (mobile-method.md, rung 4) — the organ's own, labeled |

Ranking rationale: candidate value = unasked delivery × check
divergence × trust staleness. The parser the platform feeds the app
without asking outranks any UI path (it fires without a user's
choice); a client check the server does not mirror outranks both
(the boundary is where Miller's findings land); a stale trusted
endpoint outranks a fresh one only when its protocol predates the
server's hardening era. Reading is free and fuzzing is budgeted —
the ladder orders candidates so the cheapest confession is read
first and the mutation budget is spent last.

Generation falsifier: a pinned shipped binary plus its live server
where the ladder yields zero candidates means the ladder is missing
a rung — the census is re-read for the surface class it cannot see,
and the new rung is written with its grounding row. The app is never
excused as clean; that verdict belongs to verification, not
generation.

#### The ladder's payload kit — entry-point seeds (customize before use)

Generation writes rows; these seeds are the craft the rows name,
fired ONLY inside T4's bounded runs on lab hardware. Kit rows are
the organ's own craft on generic platform knowledge — the sources
ledger's boundary for mobile-method.md applies here too:

| Seed class | Shape (mutate one axis per round) | Writes which row |
| --- | --- | --- |
| Deep-link depth | `scheme://host/` + path segments grown one per round, then a unicode-confusable segment | deep-link parser candidate + crash row |
| Push payload nesting | one extra object level per round; type-confused values (string where a number is declared) | deserialization candidate |
| Local-file truncation | magic bytes kept, declared length field overrun by 1, 2, 4 | file-parser candidate |
| Parameter repetition | the same query key repeated with ascending values until the guard's shape changes | input-validation candidate |

Customization knobs, stated in the plan note before any run: the
platform profile (iOS build pin / Android API level, from the T1
pin), the entry-point class focus (chosen from the T2 census, never
from preference), and the round budget (T4's pre-registered number).
A seed outside the census's classes is not run — it is recorded as
a kit-extension candidate with its grounding row.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| App in scope | Pull the exact shipped binary + version | T1 artifact pin (hash, version, store source) | Never analyze a debug build and call it shipped |
| Binary in hand | Enumerate surface classes BEFORE picking targets | T2 class census (IPC/deep-links/storage/transport) | Never open with a favorite exploit |
| A client check appears (root/cert) | Treat as hypothesis about the server | T3 tests whether the SERVER enforces the same rule | Never report a bypassed client check as a server vuln |
| Entry point enumerated | Fuzz it bounded | T4 mutated payload sets, crash artifacts captured | Never fuzz the device's shared services (SMS stack = lab devices only) |
| Pinning question raised | Measure it | proxy-cert acceptance test on operator device | Never assert pinning from strings |
| API behavior diverges from app checks | That divergence is the finding row | boundary differential ledgered | Never demonstrate with other users' data |
| Crash found | Reproduce, minimize, classify | n ≥ 2 + minimized input | Never file unreproduced crashes |

Pacing: long static census, surgical dynamic probes on lab hardware;
fuzzing runs are budgeted and checkpointed. Failure reaction: a crash
that vanishes on re-run → environment suspect (jailbreak state,
version drift) → re-pin the artifact before re-classifying.

## 3. The scripting arsenal — techniques as runnable craft

### T1 — artifact pin

```bash
sha256sum App.ipa
<plist-version-extract> App.ipa | head -3
unzip -l App.ipa | head -5
# the pin row: hash + version + store region + pull date
```

Read-out: the ground-truth artifact record. Gate: every later claim
cites the pin (R1) — version drift voids the run.

### T2 — surface class census

```bash
python3 - <<'PY'
classes = {
  "IPC": ["exported activities", "content providers", "broadcast receivers"],
  "deep-links": ["scheme handlers", "universal links", "app links"],
  "storage": ["prefs plist", "keychain items", "sqlite files", "cached blobs"],
  "transport": ["endpoints found in binary", "cert pins", "proxy acceptance"],
}
for c, items in classes.items(): print(f"{c:10} {len(items)} rows to enumerate")
PY
```

Read-out: the class census plan. Gate: class rows exist before any
exploitation claim (R3); "we tested what we know" is refused.

### T3 — client-check vs server-rule differential

```bash
# the app refuses X locally; does the SERVER refuse X?
curl -s -o /dev/null -w "%{http_code}\n" -X POST "https://<api>/transfer" \
  -H "Authorization: Bearer <operator-token>" -d "amount=99999&from=operator"
# refusal divergence (client blocks, server allows) = the boundary finding row
```

Read-out: the boundary differential pair. Gate: findings land as
divergence rows (R2); client-only bypasses are labeled as such.

### T4 — bounded entry-point fuzzing

```bash
python3 - <<'PY'
import json, hashlib
payloads = []
base = b"<platform-entry-payload-template>"
for i in range(50):
    mutated = base.replace(b"TYPE", bytes([65 + (i % 26)]) * 2) + bytes([i % 256])
    payloads.append({"id": i, "sha": hashlib.sha256(mutated).hexdigest()[:12]})
print(json.dumps({"budget": 50, "captured": "crash artifacts minimized + reproduced n>=2"}))
PY
```

Read-out: the fuzz budget + artifact policy. Gate: lab devices only
for platform entry points (R4); budget and checkpoints pre-registered.

### T5 — pinning measurement

```bash
# does the app accept the operator's proxy cert? observation, not strings
<device-proxy-setup> --cert <operator-ca>
<app-launch-with-entry> "https://<api>/health"
# proxy log rows: CONNECT seen? cert accepted? or hard fail = pinning HELD
```

Read-out: pinning verdict from observation. Gate: pinning claims cite
the proxy observation (R5); string-based claims are marked UNVERIFIED.

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | app authorized | pin the shipped artifact | T1 | hash + version row | FACT |
| S2 | artifact pinned | enumerate surface classes | T2 | class census table | FACT |
| S3 | census complete | pick target class; map client checks | T3 | check inventory | PLAN |
| S4 | checks inventoried | run boundary differentials + pinning measurement | T3, T5 | divergence rows | EXPERIMENT |
| S5 | entry points mapped | bounded fuzzing on lab devices | T4 | crash rows reproduced + minimized | EXPERIMENT |
| S6 | findings composed | exit: boundary register + surface map | — | client-only rows labeled | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* Claims from a non-pinned or debug artifact → R1 violation; re-pin
  and re-verify before anything stands.
* A "server vulnerability" that is only a client-check bypass → R2
  violation; reclassified to the boundary row it actually is.
* Platform-stack fuzzing on non-lab hardware → R4 violation; halt and
  ledger.
* Pinning asserted without the proxy observation → R5 violation; the
  verdict is UNVERIFIED until measured.
