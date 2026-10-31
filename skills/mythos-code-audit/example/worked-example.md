# Worked Example — python-jose 3.3.0 → 3.4.0: Two CVEs Rediscovered, Two Variants Predicted

Calibration engagement for mythos-code-audit v1.0.0. Every transcript line
below is real output from the engagement sandbox; raw artifacts live next to
this file (`transcript_330.txt`, `transcript_340.txt`, `env_330.txt`,
`env_340.txt`, `patch-diff-native.txt`, `patch-diff-jwe.txt`,
`patch-diff-utils.txt`).

| Item | Value |
|------|-------|
| Target | python-jose (self-owned pip copies — supply-chain audit, R0 self-authorized) |
| Arms | 3.3.0 (2021-06-05) vs 3.4.0 (2025-02-14), both pinned, `cryptography==42.0.8` era-matched |
| Outcome | 2 rediscovered CVEs (CONFIRMED), 1 predicted variant CONFIRMED, 1 marker variant INCONCLUSIVE + parked, 2 hypotheses FALSIFIED, 14 cells × 2 arms, all 3× STABLE |

Honest bias note, recorded before anything else: the version pair was chosen
*because* its release notes name two CVEs. Target-selection bias is real and
logged in the mistake ledger (§8). What this engagement calibrates is the
**method**: diff → invariant → enumeration gap → pre-registered prediction →
two-arm oracle — executed end to end, with self-corrections on the record.

## 1. Phase 0 — Authorization, Provenance, Environment

```
R-001 | 2026-10-30T12:18Z | operator | AUTH | local sandbox | self-owned pip copies of python-jose | — | AUTH | supply-chain audit of own environment; zero third-party systems in scope
R-002 | 2026-10-30T12:24Z | pip download | PROVENANCE | python-jose==3.3.0 sdist (129068 B) + ==3.4.0 sdist (92145 B) | pinned both arms | 2 | PROVENANCE | --no-deps --no-binary :all:; trees unpacked under src/
R-003 | 2026-10-30T12:26Z | pip freeze | PROVENANCE | env_330.txt / env_340.txt recorded | cryptography==42.0.8 on both arms | 2 | PROVENANCE | era-matched after R-004 incident
R-004 | 2026-10-30T12:21Z | harness | ENV | first run: JWE cells raised `module 'lib' has no attribute 'RAND_bytes'` | instrument failure | 6 | MISTAKE,ENV | jose 3.3.0 (2021) vs cryptography 50.x (2026): environment rot, not behavior — see §8 M-2
R-005 | 2026-10-30T12:25Z | pip | ENV | pinned cryptography==42.0.8 on both arms; JWE cells re-ran clean | fixed | 1 | ENV | ERROR cells voided and re-executed, per SKILL.md §11
R-006 | 2026-10-30T12:18Z | operator | CANARY | canary chosen: MYTHOS-CANARY-4d81f3a2 (sha256 644af5ba88f8d9ab…) | seeded | 1 | CANARY | rides inside every forged claim
```

Smoke test on both arms: import + one golden RS256 round-trip → green
before any cell counted.

## 2. Phase 1 — Trust Map

```
R-010 | 2026-10-30T12:27Z | read | TRUST-MAP | jose/jwt.py:decode → jws.verify → key construction → backend verify | entry | 1 | TRUST-MAP | untrusted: token string; trusted: caller's key + alg allowlist
R-011 | 2026-10-30T12:27Z | read | TRUST-MAP | jose/jwt.py:encode → HMACKey/RSAKey/ECKey construction | entry | 1 | TRUST-MAP | key material crosses from config into primitive choice
R-012 | 2026-10-30T12:27Z | read | TRUST-MAP | jose/jwe.py:decrypt → _jwe_compact_deserialize → _decrypt → _decompress | entry | 1 | TRUST-MAP | zip param is attacker-controlled; decompression unbounded pre-3.4.0
R-013 | 2026-10-30T12:27Z | read | TRUST-MAP | jose/backends/native.py:HMACKey.__init__ | guard | 1 | TRUST-MAP | shape-based guard: 4-string blacklist (see R-020) — flagged as lead
```

Map summary (edges → guards → sinks): both token entries funnel key
construction through `jwk`/backends; the HMAC guard sits in
`backends/native.py` (and a twin in `cryptography_backend.py`); the JWE
entry ends in `zlib.decompress` with no size bound on the 3.3.0 side.

## 3. Phase 2 — Patch Archaeology

### 3.1 The hunks

```
R-020 | 2026-10-30T12:28Z | diff -u | PATCH-DIFF | jose/backends/native.py:39@3.3.0→3.4.0 | blacklist replaced by structural check | +2/-8 | PATCH-DIFF | full hunk in patch-diff-native.txt
R-021 | 2026-10-30T12:28Z | diff -u | PATCH-DIFF | jose/jwe.py:456@3.3.0→3.4.0 | bounded decompression + entry-size cap | +11/-4 | PATCH-DIFF | full hunk in patch-diff-jwe.txt
R-022 | 2026-10-30T12:28Z | diff -u | PATCH-DIFF | jose/utils.py@3.3.0→3.4.0 | new is_pem_format()/is_ssh_key() with 6-format family list | +34/-0 | PATCH-DIFF | full hunk in patch-diff-utils.txt
R-023 | 2026-10-30T12:29Z | diff -u | PATCH-DIFF | jose/constants.py@3.4.0 | JWE_SIZE_LIMIT = 250*1024 (=256000) | +1/-0 | PATCH-DIFF | cited by both jwe.py hunks
```

Hunk 1 — the old guard was this blacklist (3.3.0, `native.py`):

```python
invalid_strings = [
    b"-----BEGIN PUBLIC KEY-----",
    b"-----BEGIN RSA PUBLIC KEY-----",
    b"-----BEGIN CERTIFICATE-----",
    b"ssh-rsa",
]
if any(string_value in key for string_value in invalid_strings):
    raise JWKError("The specified key is an asymmetric key or x509 certificate and"
                   " should not be used as an HMAC secret.")
```

3.4.0 replaced it with `if is_pem_format(key) or is_ssh_key(key):` and the
same error. Hunk 2 — 3.4.0 bounds decompression:

```python
decompressor = zlib.decompressobj()
decompressed = decompressor.decompress(compressed, max_length=JWE_SIZE_LIMIT)
if decompressor.unconsumed_tail:
    raise JWEError(f"Decompressed JWE string exceeds {JWE_SIZE_LIMIT} bytes")
```

### 3.2 Invariant reconstruction

| Fix hunk (R-020, R-021) | Reconstructed invariant |
|--------------------------|------------------------|
| structural key-type check | key material must never be used as an HMAC secret unless it is symmetric |
| bounded decompression | decompressed size must never exceed a fixed bound, whatever the compressed size |

### 3.3 Enumeration-gap analysis (R-020 × R-022)

The 3.3.0 blacklist contains exactly one OpenSSH marker: `ssh-rsa`. The
3.4.0 family list contains six: `ssh-ed25519`, `ssh-rsa`, `ssh-dss`,
`ecdsa-sha2-nistp256`, `ecdsa-sha2-nistp384`, `ecdsa-sha2-nistp521`
(R-022). Diffing list against family, the pre-registered prediction set is:
{`ssh-ed25519`, `ssh-dss`, `ecdsa-sha2-*` — three format families that
should slip past the 3.3.0 guard}. These become H-003 and H-006 before any
payload runs.

## 4. Phase 3 — Pre-Registered Hypotheses

### Contract — H-001: OpenSSH-format public key usable as HMAC secret (CLASS-02)
- claim: an EC public key in OpenSSH format passes the 3.3.0 HMAC guard and verifies a forged HS256 token under a mixed-family allowlist — key-type confusion, CLASS-02, evidence chain at R-020.
- anchor: jose/backends/native.py:39@3.3.0 (blacklist) / :40@3.4.0 (structural check).
- invariant: key material must never be used as an HMAC secret unless it is symmetric.
- oracle: E7 cell — forge HS256 with the OpenSSH public key string as secret, decode under `['HS256','ES256']`, both arms. Falsifier: 3.3.0 arm rejects the token.
- prior: 75% — the release notes say "signing JWT with public key is now forbidden" and the CVE text names OpenSSH keys (R-020, R-024).

### Contract — H-002: JWE decompression bomb unbounded on 3.3.0 (CLASS-14)
- claim: a 1MiB deflated JWE payload materializes fully on decode
  (resource consumption / decompression bomb, CLASS-14) — chain at R-021.
- anchor: jose/jwe.py:456@3.3.0 (unbounded `zlib.decompress`) /
  :456@3.4.0 (bounded decompressobj).
- invariant: decompressed size must never exceed a fixed bound.
- oracle: E6 cell (1MiB bomb) + E6B regression control (100KB legit), both
  arms. Falsifier: 3.3.0 arm refuses or truncates.
- prior: 70% — hunk R-021 adds a bound where none existed; the CVE text
  describes exactly this input shape (R-024).

### Contract — H-003: ssh-ed25519 public key slips the 3.3.0 guard (CLASS-02)
- claim: predicted from the enumeration gap (R-022) — a real Ed25519 public key in OpenSSH format passes the 3.3.0 blacklist and verifies a forged HS256 token (R-020), the variant class beyond the CVE's EC headline.
- anchor: jose/backends/native.py:39@3.3.0.
- invariant: as H-001.
- oracle: E7C cell, real generated Ed25519 key, both arms. Falsifier: 3.3.0 arm rejects.
- prior: 65% — pre-registered BEFORE the cell ran; the prediction comes from reading the diff, not from the CVE text.

### Contract — H-004: the fix breaks legitimate flows
- claim: 3.4.0 rejects or corrupts legitimate RS256 and JWE round-trips (R-024).
- anchor: jose/jws.py@3.4.0 / jose/jwe.py@3.4.0.
- invariant: fixes change attacker behavior only.
- oracle: E3 (legit RS256) and E6B (legit 100KB JWE) on both arms. Falsifier: either control fails on 3.4.0.
- prior: 15% — release notes list unrelated crypto changes (R-024).

### Contract — H-005: single-family allowlist does not save 3.3.0 users
- claim: with `algorithms=['ES256']` pinned, a forged HS256 OpenSSH token still verifies on 3.3.0 because key construction runs before the allowlist check (map row R-013, R-030).
- anchor: jose/jws.py@3.3.0.
- invariant: an allowlist is the verifier's policy, so it must be enforced before any key operation.
- oracle: E7B cell, both arms. Falsifier: 3.3.0 arm rejects the header.
- prior: 40% — E2's error ordering suggests key-wrap runs first (R-030).

### Contract — H-006: ssh-dss public keys pass the 3.3.0 guard (CLASS-02)
- claim: predicted from the enumeration gap (R-022) — a DSS public key in OpenSSH format passes the guard like its siblings, a confusion-class breadth check (R-020).
- anchor: jose/backends/native.py:39@3.3.0.
- invariant: as H-001.
- oracle: E7D marker probe (synthetic `ssh-dss AAAA…` string) — a real DSA-key roundtrip plus victim-realism study exceed this engagement's budget, so the marker is the recorded evidence.
- prior: 60% string-level, 55% real-key.

```
R-024 | 2026-10-30T12:29Z | web | FACT | NVD/GitHub: CVE-2024-33663 (algorithm confusion, OpenSSH ECDSA + other formats, ≤3.3.0, CWE-327); CVE-2024-33664 (JWE decompression bomb, ≤3.3.0, CWE-400); both fixed in 3.4.0 (2025-02-14) | verified | 2 | FACT | release notes: "signing JWT with public key is now forbidden"; "JWE limited to 250KiB"
R-025 | 2026-10-30T12:29Z | operator | HYP | H-001..H-006 pre-registered before any treatment cell ran | committed | 6 | HYP | no HARKing; predictions from R-020/R-021/R-022 only
```

## 5. Phase 4 — Oracle Cells and Differential Results

Harness: one script, two arms (`--runs 3`), cells isolated, verdicts
classified VERIFIED/REJECTED/ERROR, stability digit-normalized. Full logs:
`transcript_330.txt`, `transcript_340.txt` (trailer: `# END runs=3 cells=14
all_stable=True` on both).

```
R-030 | 2026-10-30T12:30Z | harness | CELL | E1/E2/E2B/E4/E5/E8/E9 (PEM, cert, JWK-JSON vectors) | REJECTED on both arms, 3/3 STABLE each | 14 | CELL,CONTROL | guard blocks PEM/cert strings on 3.3.0 too — the hole is format-specific (R-020)
R-031 | 2026-10-30T12:30Z | harness | CELL | E7 OpenSSH EC confusion, 3.3.0 arm | VERIFIED 3/3: accepted, role=admin, canary=MYTHOS-CANARY-4d81f3a2 | 3 | CELL | transcript_330.txt
R-032 | 2026-10-30T12:30Z | harness | CELL | E7 OpenSSH EC confusion, 3.4.0 arm | REJECTED 3/3: JWSError "asymmetric key or x509 certificate … not be used as an HMAC secret" | 3 | CELL | transcript_340.txt
R-033 | 2026-10-30T12:30Z | harness | CELL | E6 JWE bomb 1MiB, 3.3.0 arm | VERIFIED 3/3: plaintext len=1048576 | 3 | CELL | transcript_330.txt
R-034 | 2026-10-30T12:30Z | harness | CELL | E6 JWE bomb 1MiB, 3.4.0 arm | REJECTED 3/3: JWEError "Decompressed JWE string exceeds 256000 bytes" | 3 | CELL | transcript_340.txt
R-035 | 2026-10-30T12:30Z | harness | CELL | E7B allowlist ES256-only, both arms | REJECTED 3/3 each: JWTError "The specified alg value is not allowed" | 6 | CELL,CONTROL | mitigation boundary evidence (H-005)
R-036 | 2026-10-30T12:30Z | harness | CELL | E7C ssh-ed25519, 3.3.0 arm | VERIFIED 3/3 (predicted variant) | 3 | CELL | transcript_330.txt
R-037 | 2026-10-30T12:30Z | harness | CELL | E7C ssh-ed25519, 3.4.0 arm | REJECTED 3/3 | 3 | CELL | transcript_340.txt
R-038 | 2026-10-30T12:30Z | harness | CELL | E7D ssh-dss marker, 3.3.0 arm | VERIFIED 3/3 (marker-level only) | 3 | CELL | see H-006 honesty limit
R-039 | 2026-10-30T12:30Z | harness | CELL | E3/E6B regression controls, both arms | VERIFIED 3/3 each: legit RS256 + legit 100KB JWE intact | 12 | CONTROL | fix does not break legitimate flows (H-004)
```

Transcript excerpts (verbatim):

```
# ARM python-jose==3.3.0 cryptography==42.0.8 python==3.12.16
R-LAB | E7 OPENSSH-EC-PUB-CONFUSION | run 1/3 | VERIFIED | accepted, role=admin (OpenSSH-key variant) | 0ms
R-LAB | E6 JWE-BOMB-1MB | run 1/3 | VERIFIED | plaintext len=1048576 (1MiB decompressed), encrypt=5ms decrypt=3ms | 9ms
R-LAB | E7C ED25519-SSH-CONFUSION | run 1/3 | VERIFIED | accepted, role=admin (ed25519 variant predicted from patch, confirmed) | 0ms
R-LAB | E7B OPENSSH-ALLOWLIST-ES256-ONLY | run 1/3 | REJECTED | JWTError: The specified alg value is not allowed | 0ms

# ARM python-jose==3.4.0 cryptography==42.0.8 python==3.12.16
R-LAB | E7 OPENSSH-EC-PUB-CONFUSION | run 1/3 | REJECTED | JWSError: The specified key is an asymmetric key or x509 certificate and should not be used as an HMAC secret. | 0ms
R-LAB | E6 JWE-BOMB-1MB | run 1/3 | REJECTED | JWEError: Decompressed JWE string exceeds 256000 bytes | 7ms
R-LAB | E3 REGRESSION-RS256-CONTROL | run 1/3 | VERIFIED | accepted, sub=attacker@lab.local (legit flow intact) | 33ms
```

Cell matrix (verdict per arm, 3/3 STABLE everywhere):

| Cell | 3.3.0 | 3.4.0 | Feeds |
|------|-------|-------|-------|
| E1 RSA-PEM confusion, mixed algs | REJECTED | REJECTED | boundary (R-030) |
| E2 allowlist `['RS256']` only | REJECTED | REJECTED | boundary (R-030) |
| E2B no allowlist | REJECTED | REJECTED | boundary (R-030) |
| E3 regression control RS256 | VERIFIED | VERIFIED | H-004 (R-039) |
| E4 EC-PEM confusion | REJECTED | REJECTED | boundary (R-030) |
| E5 encode-side PEM as secret | REJECTED | REJECTED | root cause (R-030) |
| E6 JWE bomb 1MiB | VERIFIED | REJECTED | H-002 (R-033, R-034) |
| E6B regression control 100KB JWE | VERIFIED | VERIFIED | H-004 (R-039) |
| E7 OpenSSH EC confusion, mixed algs | VERIFIED | REJECTED | H-001 (R-031, R-032) |
| E7B OpenSSH + `['ES256']` only | REJECTED | REJECTED | H-005 (R-035) |
| E7C ssh-ed25519 confusion | VERIFIED | REJECTED | H-003 (R-036, R-037) |
| E7D ssh-dss marker probe | VERIFIED | REJECTED | H-006 (R-038) |
| E8 JWK-JSON confusion | REJECTED | REJECTED | boundary (R-030) |
| E9 cert-PEM scope probe | REJECTED | REJECTED | boundary (R-030) |

## 6. Closures

### H-001 — OpenSSH public key as HMAC secret (CLASS-02)
Closure: CONFIRMED — 3.3.0 arm VERIFIED 3/3 with the canary claim accepted
(R-031); 3.4.0 arm REJECTED 3/3 (R-032); regression control green on both
arms (R-039); n_runs: 3 per arm. Rediscovery of CVE-2024-33663 from the
version diff (R-020, R-024). Anchor: jose/backends/native.py:39@3.3.0.

### H-002 — JWE decompression bomb (CLASS-14)
Closure: CONFIRMED — 3.3.0 arm: VERIFIED 3/3, materialized 1048576 plaintext
bytes (R-033); 3.4.0 arm: REJECTED 3/3 with the 256000-byte cap (R-034); 100KB
regression control green on both arms (R-039); n_runs: 3 per arm.
Rediscovery of CVE-2024-33664 (R-021, R-024). Anchor:
jose/jwe.py:456@3.3.0.

### H-003 — ssh-ed25519 predicted variant (CLASS-02)
Closure: CONFIRMED — predicted from the enumeration gap before execution
(R-022, R-025); 3.3.0 arm VERIFIED 3/3 (R-036); 3.4.0 arm REJECTED 3/3
(R-037); n_runs: 3 per arm. Anchor: jose/backends/native.py:39@3.3.0.

### H-004 — fix breaks legitimate flows
Closure: FALSIFIED — regression controls E3 and E6B green on both arms, 3/3
each (R-039). Good-news falsification: the 3.4.0 fix is clean.

### H-005 — single-family allowlist insufficient on 3.3.0
Closure: FALSIFIED — E7B rejected the forged header on 3.3.0 with "The specified alg value is not allowed", 3/3 (R-035); good-news falsification: 3.3.0 users who pin one asymmetric family are outside this attack surface, mixed-family allowlists are inside it (R-030, R-031).

### H-006 — ssh-dss variant (CLASS-02)
Closure: INCONCLUSIVE — marker probe VERIFIED on 3.3.0 / REJECTED on 3.4.0
(R-038), but a real DSA-key roundtrip and victim-realism study were outside
budget; marker-level evidence only, per differential-oracles.md §3. Park
P-001: resume with a real DSA keypair, cell E7D-real, prior 60%, plus a
victim-config survey of JWK/allowlist shapes in the wild.

## 7. Phase 5 — Impact Without Harm, Mitigation Boundary, Report Excerpt

Impact chain (canary-bounded, R-006): the forged HS256 tokens carried
`canary=MYTHOS-CANARY-4d81f3a2` and `role=admin`; the canary round-tripped
through the vulnerable path on the 3.3.0 arm (R-031, R-036, R-038) —
attacker-controlled claims accepted by a self-owned lab verifier, zero real
data, zero third-party systems (R-001). Blast radius: python-jose ≤ 3.3.0
where HS256 shares an allowlist with an asymmetric family and an OpenSSH
public key string is the configured secret (R-030, R-031, R-035).

Mitigation boundary (defender-facing table, all rows cell-backed):

| Configuration | PEM attack vector | OpenSSH attack vector | Evidence |
|---------------|------------------|----------------------|----------|
| allowlist `['ES256']` (or any single asymmetric family) | rejected | rejected | R-030, R-035 |
| mixed `['HS256','ES256']` | rejected | accepted on 3.3.0, rejected on 3.4.0 | R-030, R-031, R-032 |
| no allowlist, PEM key | rejected | — | R-030 |
| upgrade to ≥ 3.4.0 | rejected | rejected | R-032, R-034, R-037 |

Report excerpt (finding format per SKILL.md §13):

> **F-1 OpenSSH public key as HMAC secret — key-type confusion, CLASS-02 (R-031, R-032).**
> python-jose ≤ 3.3.0 verifies HS256 tokens whose secret is an OpenSSH-format
> public key, when HS256 appears in the accepted algorithm list (R-030,
> R-031, R-035). Anchor jose/backends/native.py:39@3.3.0; the 3.3.0 guard is
> a 4-string blacklist that lists `ssh-rsa` but no EC/Ed25519/DSS OpenSSH
> markers (R-020); 3.4.0 replaces it with `is_pem_format or is_ssh_key`
> (R-022). Impact: forged admin claims round-trip in the lab with canary
> MYTHOS-CANARY-4d81f3a2 (R-006, R-031). n_runs: 3 per arm, STABLE.

> **F-2 JWE decompression bomb (CLASS-14).** A 1MiB deflated payload
> materializes fully on decode in ≤ 3.3.0 (resource consumption) (R-033);
> 3.4.0 caps decompressed size at 256000 bytes (R-023, R-034). Legit 100KB
> JWE flows stay green on both arms (R-039). n_runs: 3 per arm, STABLE.

## 8. Audit — Dual Control

```
$ python3 scripts/audit_code_report.py example/worked-example.md
  hypothesis blocks : 6  (confirmed 3, falsified 2, inconclusive 1)
  PASS — report satisfies the White-Box Report Contract. Ship it.   (exit 0)
$ python3 scripts/audit_code_report.py example/sloppy-code-report-fixture.md
  FAIL — 31 violation(s) listed                                       (exit 1)
```

The negative control's 31 violations span every check family: 10 forbidden
phrases (victory language, hedging, non-vocabulary states, placeholder), 8
uncited claims, 3 crypto claims without CLASS-NN, 1 uncited diff claim, 5
structural hypothesis violations (missing anchor / n_runs / arm evidence /
park / closure), and 4 file-level omissions (canary, impact chain,
mitigation boundary, regression control). The key is in README.md.

## 9. Mistake Ledger

```
MISTAKE | pre-lab | memory held CVE-2024-33664 as the confusion bug → web check showed 33664 is the JWE bomb and 33663 the confusion | trusting recall over source | verification-first even for "known" CVEs; swap recorded before any claim (R-024)
MISTAKE | Phase 0 | cryptography 50.x made JWE cells ERROR (RAND_bytes) and the first harness labeled them REJECTED | conflating instrument failure with control firing | verdict taxonomy split VERIFIED/REJECTED/ERROR; era-pin dependencies in Phase 0 (R-004, R-005)
MISTAKE | Phase 4 | first stability check flagged the 1MiB bomb cell UNSTABLE because decrypt took 2ms vs 3ms | timing jitter read as behavioral instability | digit-normalize details before comparing (SKILL.md §7)
MISTAKE | target selection | version pair chosen because release notes name two CVEs | calibration-on-known-answer bias | bias disclosed up front (§0); variant predictions (H-003, H-006) are the part that was NOT in the release notes — they came from reading the diff
MISTAKE | Phase 3 | H-006 initially drafted as CONFIRMED from the marker cell | marker-level evidence overclaimed as real-key evidence | marker probes cap at INCONCLUSIVE + Park (differential-oracles.md §3)
```

## 10. What This Calibration Proves — and Does Not

Proves: the pipeline executes end to end on a real target; enumeration-gap
analysis yields testable predictions that confirm at runtime (H-003); the
verdict taxonomy catches a real instrument failure that would otherwise have
been a false negative; regression controls catch fix-breakage claims before
they are made (H-004); the auditor's dual control works.

Does not prove: that every audit finds two CVEs, or that priors transfer to
other codebases. It proves the instrument is calibrated — which is exactly
what a discipline layer is for.
