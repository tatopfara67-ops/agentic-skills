# operator-os.md — the Miller runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> mobile teardown laws; the M-protocol (references/method-upgrade.md)
> states the teardown and boundary protocol; THIS module is the
> runtime — how the agent thinks, behaves, and scripts while executing
> them, characteristic of Charlie Miller's documented craft (with
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
