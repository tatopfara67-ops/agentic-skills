# teardown-ladder.md — the dissection path of deep-teardown

Load when an artifact is in hand and the descent must be planned.
Each layer: entry conditions, the tool class, what to record, and
the hypothesis classes it answers. Assume a Kali-grade toolchain.

## 0. Layer 0 — Artifact Map (always)

```
tree / file listing        formats + sizes + signature
manifest / metadata        permissions, services, build ids
hash                       sha256 recorded in the ledger FACT
```

Answers: what is this, is it complete, which ladder applies.

## 1. The JavaScript Ladder

| Depth | Action (tool class) | Records out |
| --- | --- | --- |
| 1 | fetch + inventory (js_analyze) | endpoints, commented routes, secret hints |
| 2 | beautify/unminify (prettier-class) | readable module tree |
| 3 | sourcemap resolution (if exposed) | original sources — file names + logic |
| 4 | module-graph reconstruction | route table, feature-flag branches, state stores |
| 5 | logic reading | client checks, admin gates, debug stubs, hidden routes |

Stop when the hypothesis class in hand is answered; layer 5 is
where the four inventories (§4 of the SKILL) get filled.

## 2. The Mobile Ladder (APK / IPA)

| Depth | Action (tool class) | Records out |
| --- | --- | --- |
| 1 | unpack (apktool/unzip-class) | manifest, permissions, activities/services |
| 2 | dex→source (jadx-class) | readable Java/Kotlin; the REAL endpoint list |
| 3 | resources + assets | config files, feature flags, embedded URLs |
| 4 | native libs (.so) | strings + symbols; exported functions |
| 5 | storage/runtime map | SharedPreferences/Keychain paths, encryption status |

IPA note: class-dump/otool-class tooling; entitlements list is part
of layer 1 output.

## 3. The Binary / Firmware Ladder

| Depth | Action (tool class) | Records out |
| --- | --- | --- |
| 1 | file/identify + hashes | format, arch, packing status |
| 2 | strings (with encodings) | URLs, keys, paths, build hosts |
| 3 | symbols/objdump or disassembler | import/export surface |
| 4 | config extraction | embedded settings, update channels |
| 5 | targeted RE of one function | only with a named hypothesis (budget gate) |

## 4. The Four Inventories (template — fill at the deepest layer reached)

```
A. endpoints:    [host, path, auth-model-as-client-sees-it, internal?]
B. client logic: [check/flag/stub, where in code, what it gates]
C. local data:   [token/key/PII, storage path, encrypted?, when written]
D. secrets:      [type, masked hint, artifact path]  (policy: report-only)
```

Each entry becomes a hypothesis line in the ledger; A feeds
reachability probes (scope-checked), B feeds differentials with/without
the flag, C is directly report-grade, D is operator intel only.

## 5. Anti-patterns (record as MISTAKEs)

* Descending layers without a hypothesis class — "let's see what's
  in here" burns budget (R7).
* Dumping decompiled source into context — bodies stay in artifacts;
  the ledger records counts and paths.
* Probing an internal host discovered in the artifact when that host
  is out of scope — it is reported intel, not a target.
* Treating a client-side admin flag as CONFIRMED server privilege —
  only the server differential confirms (R5).
