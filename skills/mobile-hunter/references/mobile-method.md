# mobile-method.md — the teardown ladder, rung by rung

> Part of **mobile-hunter v1.0.0** (package architecture).
> **Load when:** any rung of the SKILL.md procedure needs its exact
> steps, its oracle, or its falsifier. Authoritative rules live in
> [`../SKILL.md`](../SKILL.md) — if anything here conflicts with the
> SKILL.md laws, **SKILL.md wins**.

---

## 1. The ladder, in one view

```
rung 1  artifact scope + provenance      (R0 gate, hash recorded)
rung 2  unpack + manifest inventory      (file:line citations begin)
rung 3  confession sweep                 (strings, secrets, endpoints)
rung 4  reconciliation vs the web map    (ghost endpoint diff)
rung 5  targeted code reading            (WebView, IPC, pinning, crypto)
rung 6  boundary differentials           (API, auth-boundary-mapper law)
rung 7  runtime proofs, operator-owned   (deep links, storage, IPC)
rung 8  classification + exit numbers    (CVSS on the crossed path)
```

Static is rungs 1–5; dynamic is rungs 6–7; the rule is absolute:
**no rung-N action before rung-(N−1) has its records.** W1 (spies
before armies) is this ladder; W3 (strike weakness) is why rung 4
exists — the ghost endpoint is the neglected seam.

## 2. Rung 2 — the manifest inventory, with oracles

**Android (`AndroidManifest.xml`, decompiled):**
* exported components — activities, services, broadcast receivers,
  content providers with `exported="true"` or intent filters implying
  export. Oracle: each component's input validation path read to its
  sink. Falsifier: an exported component whose every input is
  validated = surface recorded, no finding.
* deep links — custom schemes (`myapp://`) and intent filters with
  `BROWSABLE`; autoverify app links. Oracle: a crafted link reaching a
  sensitive handler unauthenticated. Falsifier: handler re-checks
  authorization server-side (client-side checks alone do NOT falsify —
  they are the classic gap).
* flags — `debuggable`, `allowBackup`, `usesCleartextTraffic`,
  network security config exceptions. Each is one dossier row with its
  file:line.

**iOS (`Info.plist`, entitlements):**
* URL schemes (`CFBundleURLTypes`), universal link association files,
  ATS exceptions (`NSAllowsArbitraryLoads` and per-domain exceptions),
  background modes, export custom entitlements. Same oracle/falsifier
  law as Android deep links.

## 3. Rung 3 — the confession sweep

Ordered by yield-per-byte:
1. URL/endpoint strings — every scheme+host+path in the binary and
   resources; staging/test hosts that resolve publicly are high-value
   hypotheses (they usually sit on older, less-audited deploys).
2. Secret-shaped strings — API keys, tokens, push certificates'
   fingerprints. Masked immediately (secrets policy absolute);
   report-only. A bundled secret's finding is "secret shipped in
   binary", never the secret's use.
3. SDK/version strings — bundled libraries with their versions; each
   version checked against public advisories; a match is a lead that
   needs its own runtime or boundary confirmation, never a finding on
   its own.
4. Feature flags and remote-config defaults — often reveal disabled
   admin surfaces the client can request anyway.

## 4. Rung 4 — reconciliation (the ghost-endpoint diff)

The app's endpoint set (rung 3) minus the web inventory
(api-surface-mapper) equals the ghost set. Each ghost gets a
HYPOTHESIS card: "route R is authorized as of the app's release era;
objects from era E are under [role]". The differential that decides:
operator account's own object (baseline) → same request with another
object identifier (treatment) → request repeated without the
client-attested mobile headers (control, isolating whether the server
trusts the header claim). Deprecation is a seam, not the bug — the bug
is frozen authorization meeting fresh identifiers.

## 5. Rung 5 — targeted code reading

Four neighborhoods, in this order:
1. **WebView configs** — JS enabled, file access, universal links
   inside the WebView, `addJavascriptInterface`-style bridges: the
   bridge's exposed methods are sinks; deep links are sources; the
   pairing is a DOM-side xss-playbook question.
2. **IPC handlers** — exported components' input paths to storage,
   network, or command execution; the same source→sink discipline.
3. **Certificate pinning** — where pins live, whether failure is open
   or closed, whether the pin set includes a user-added-CA escape
   hatch. Recorded as an effort wall; a bypass demonstration is only
   in scope when the program allows client-instrumentation testing.
4. **Crypto call sites** — hardcoded keys, ECB selection, static IVs:
   each is a hypothesis for a plaintext-observable differential where
   the oracle is the app's own ciphertext (self-owned data only).

## 6. Rung 6 — boundary differentials, the exact pattern

For every mobile-only route R with an object parameter:
```
baseline   operator account, own object A        -> 200, A's fields
treatment  operator account, object B (other's)  -> ??? (the question)
control    treatment minus mobile-attested headers -> ???
```
CONFIRMED requires the treatment response to differ from the baseline
in B's favor AND the control to localize the cause (header trust vs
route authorization). n_runs ≥ 2; both mobile and web user-agents
recorded — a route that answers only the app's user-agent is itself a
dossier row (version-frozen authorization).

## 7. Rung 7 — runtime proofs, the ownership law

Operator-owned device or emulator, operator account, self-owned
objects:
* deep-link reachability: link fired from a neutral page (not the
  app's own webview) — the neutral origin is what makes the proof
  cross-context.
* storage observation: what the app writes where (SharedPreferences,
  plists, caches); sensitive cleartext at rest is a finding when the
  platform offers the protected store and the app ignored it — cite
  both the write site (rung 5) and the observed file.
* IPC behavior: another operator-owned app (or an instrumentation
  harness the operator runs) invoking the exported component.

Every runtime record carries device/account provenance. A capture
without provenance is a lead, not evidence.

## 8. Rung 8 — classification notes for mobile geometry

* CVSS vector on the crossed path: a client-side-only observation
  (pinning bypass, debuggable flag) rarely crosses privilege on its
  own — it is a link, and chain-architect's per-link discipline
  composes it with the boundary differential that does.
* VRT: use the taxonomy's mobile rows (improper input handling on
  mobile, insecure data storage on mobile) — never the server row for
  a client-only observation, and vice versa.
* The report's reproduction section states the artifact version and
  hash, the exact request set, and the runtime provenance — a triager
  with the store app and a proxy replays it without asking questions.
