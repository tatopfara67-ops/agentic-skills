# patch-archaeology.md — Mining Fixed Bugs for Surviving Variants

> Load when: a version pair, commit range, or advisory is on the table and
> you are mining fixes for variants. SKILL.md wins on conflict.

## 1. The Vein Theory

A fixed bug is the cheapest high-quality signal in source auditing:

- It **proves** the bug class exists in this codebase (someone already paid
  the discovery cost).
- Fixes are **frequently incomplete** — they patch the reported input, not
  the class; they enumerate the observed instance, not the family.
- A silent patch (fixed without advisory) means the vendor hoped nobody
  noticed — the variants may still be sitting there for whoever reads the
  diff.

This is the Big Sleep engine operationalized: Google's 2024 agent found the
SQLite zero-day by reasoning about *invariants* and *sibling code*, not by
grepping for sinks. The diff gives you the invariant for free, because a fix
is an invariant written in executable form.

Priority order for any audit: **patch archaeology → trust-map edges →
catalog lookups → sink triage → the middle of the codebase.** Deep reading
is the *last* thing you do, not the first, and only where the map points.

## 2. Collect

| Source | Command / route | Notes |
|--------|-----------------|-------|
| Version pair (installed deps) | `pip download --no-deps --no-binary :all: pkg==A`, `==B`, unpack both | sdist diff = full source, no VCS needed; record hashes (`PROVENANCE`) |
| Git history | `git log --oneline -p -- <path>`, `git log -S "blacklist_string"` (`-S` = pickaxe), `git log -L :func:file.py` | `-L` walks a function's lifetime — perfect for guards |
| Tag range | `git diff vA..vB -- src/` | isolate source from tests/docs churn |
| Release notes / changelogs | releases page, `CHANGELOG.md` | security entries name the class; **silent entries are the gold** |
| Advisory DBs | NVD/GHSA filtered by package name | gives you CVE text + affected range — verify against the actual diff, advisories lag and mislabel |

## 3. Triage Hunks (silent-patch heuristics)

A hunk is security-relevant if it touches a **guard, a limit, a format
parser, or a key/credential path** — or if its message smells like fear:

- Messages: `harden`, `strict`, `forbid`, `validate`, `sanitize`, `edge
  case`, `limit`, `bounds`, `reject`, `fix leak`, `security` — with **no CVE
  reference**. The vaguer the message on a guard-shaped hunk, the higher the
  prior that the author was patching something they did not fully understand.
- Non-messages: pure refactors, version bumps, test-only changes, doc
  rewrites — deprioritize, but note: a fix hidden *inside* a refactor ("move
  parse logic to utils") is a classic silent patch.

For each security-relevant hunk, record a `PATCH-DIFF` ledger line:
`R-NNN | time | diff | hunk | file:line@A→B | semantic change | +N/-M | PATCH-DIFF | invariant guess`.

## 4. Reconstruct the Invariant

Write it as one sentence in the template:

> "The `«object»` must never be used as `«role»` unless `«condition»`."

Examples, all from real fixes:

| Fix hunk | Reconstructed invariant |
|----------|------------------------|
| python-jose 3.4.0: HMACKey rejects `is_pem_format(key) or is_ssh_key(key)` | key material must never be used as an HMAC secret unless it is symmetric |
| python-jose 3.4.0: `decompressobj().decompress(c, max_length=JWE_SIZE_LIMIT)` | decompressed size must never exceed a fixed bound, whatever the ciphertext size |
| Next.js 14.2.25: middleware skips on `X-Middleware-Subrequest` | an internal header must never be forgeable by an external request |
| SQLite (Big Sleep 2024): `iColumn = -1` index handling | a sentinel must never flow into a code path that treats it as a real column |

The invariant sentence is what you sweep with. Grep can't search for "key
confusion"; it can search for the *shape* the invariant forbids.

## 5. Enumeration-Gap Analysis (the star move)

When the OLD side of a diff guards with a **list** — blacklist, allowlist,
switch over types, table of formats — the list is a snapshot of its author's
knowledge at time T. The fix usually replaces it with a **structural check**
(regex/class detection) or extends the list. Either way the diff tells you
exactly which family members were missing before. Every missing member is a
pre-registerable variant with prior 60–75%.

The canonical example (calibration engagement, `example/patch-diff-native.txt`):

```python
# 3.3.0 — the guard was a 4-string blacklist:
invalid_strings = [
    b"-----BEGIN PUBLIC KEY-----",
    b"-----BEGIN RSA PUBLIC KEY-----",
    b"-----BEGIN CERTIFICATE-----",
    b"ssh-rsa",                    # ← RSA OpenSSH keys remembered...
]
# 3.4.0 — replaced by structure:
if is_pem_format(key) or is_ssh_key(key):
    raise JWKError(...)
```

Reading the old list against the OpenSSH public key family
(`ssh-rsa`, `ssh-dss`, `ssh-ed25519`, `ecdsa-sha2-nistp256/384/521`, plus
`*-cert-v01@openssh.com` certificates) predicts, *before any payload runs*:
`ecdsa-sha2-*` slips through, `ssh-ed25519` slips through, `ssh-dss` slips
through. All three confirmed at runtime on 3.3.0; all three blocked by the
3.4.0 structural check. That is a variant harvest earned by reading, not by
spraying payloads.

Procedure:

1. Find every list-shaped guard in the old version (`rg "= \[.*b?\""` near
   `if`/`in`; `switch` statements over types; `startswith` chains).
2. For each, write the family the list *belongs to* (all key formats? all
   PEM types? all HTTP methods? all header names?).
3. Diff list-members against family-members → the gap set.
4. Pre-register one H-record per gap member with prior 60–75% and a marker
   or real-input cell as oracle.
5. Also ask the inverse (one-step-back): why was the guard a list at all?
   Shape checks (string matching) vs structure checks (type/parsing) — sweep
   the codebase for other shape checks guarding structural problems.

## 6. Variant Sweep

Beyond enumeration gaps, sweep for siblings of the fixed bug:

- **Same shape, same file**: the fix touched one code path; are there other
  paths with the same pattern? (python-jose: the confusion fix lives in
  `backends/native.py` HMACKey — check `backends/cryptography_backend.py`
  has the same fix, or a different one.)
- **Same shape, other module**: the JWE size cap lives in `jwe.decrypt` —
  does `jws` have any decompression or unbounded-materialization path? (JWS
  has no `zip` — confirmed by constants; write the cell anyway as a boundary
  probe if the harness supports it.)
- **Same invariant, other object**: key-type confusion applies to *every*
  place key material and algorithm meet: encode-side, decode-side, JWKS
  import, kid lookup.
- **Backport check**: vendors backport silently to LTS branches — the fix in
  `main` may be absent or partial in the version line you actually run.
  Diff your *deployed* version against the advisory range, not the GitHub
  default branch.

## 7. Diff Hygiene

- Pin both sides; diff the **source tree**, not the repo root (skip test
  churn, lockfiles, docs) — but skim test diffs separately: new tests often
  name the exact attack input, which is a free oracle design.
- Isolate hunks: one commit may mix a security fix with a refactor; the
  security hunk is the one touching guards/limits/parsers (§3).
- Incomplete fixes are a **goldmine**: if the fix still contains a
  shape-check, an enumeration, or a bounds check that only covers the
  reported instance, the variant sweep just became the main audit.
- Fixed-in-version claims in advisories lag reality: trust the diff, cite
  the version pair, and re-verify affected ranges yourself with cells.

## 8. Worked Micro-Cases

| Case | Vein | Result |
|------|------|--------|
| python-jose 3.3.0→3.4.0 | one version pair, two CVEs, one blacklist | 2 rediscoveries + 2 predicted variants + mitigation boundary (see `example/worked-example.md`) |
| Next.js CVE-2025-29927 | advisory → header invariant → config-level reproduction | middleware bypass reproduced by an internal-header forgery; fixed 12.3.5/13.5.9/14.2.25/15.2.3 |
| Big Sleep / SQLite 2024 | invariant reasoning over sibling code paths | agent-found zero-day (`iColumn = -1` sentinel misuse) — the existence proof that invariant-first beats sink-grep |
| Trail of Bits / DARPA AIxCC 2025 | proof layer over AI-generated candidates | 28 findings at ~90% precision — evidence gates, not volume, win trials |

## 9. Failure Modes

- Reading the changelog instead of the diff — changelogs under-report and
  mislabel (the 3.4.0 release notes say "signing JWT with public key is now
  forbidden"; the actual fix is a structural *input* check that also closes
  decode-side confusion).
- Diffing with mismatched dependency eras → ERROR cells masquerading as
  behavior differences (SKILL.md §11).
- Sweeping only the fixed file — the same author wrote the sibling files.
- Trusting the advisory's "fixed in X.Y.Z" without a cell on X.Y.Z itself.
