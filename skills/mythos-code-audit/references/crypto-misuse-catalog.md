# crypto-misuse-catalog.md — 16 Usage Classes with Runtime Oracles

> Load when: any crypto touchpoint is in scope (JWT/JWS/JWE, TLS, ciphers,
> KDF, RNG, signatures). SKILL.md wins on conflict.

## 0. Doctrine

**Primitives are not targets; usage is.** No agent breaks AES/SHA/RSA in a
skill session; any report claiming primitive breakage is slop and fails the
audit. What agents *can* do — better than scanners, because it requires
reading intent — is find where correct primitives are *used incorrectly*.
Each class below is a card: static signature → violated invariant → runtime
oracle → common false positive → severity gate. Findings must cite their
`CLASS-NN`; the auditor enforces it.

Severity gate (uniform): a misuse class escalates one level when it sits on
an authn/authz boundary, and caps at Medium when it requires attacker
control of configuration. Nothing below Medium ships as a standalone
finding; below that it is a hardening note in the report appendix.

## 1. The Cards

### CLASS-01 — Algorithm not pinned
- **Signature**: algorithm taken from token/config-supplied-by-client,
  `algorithms=None`, empty allowlist, `alg` read before allowlist check.
- **Invariant**: the accepted algorithm set is fixed by the verifier's
  configuration, never by the token header.
- **Oracle**: forge token with off-family `alg`; decode under
  `['ES256']`-only config → acceptance = hit. Boundary cells: mixed-family
  allowlists (`['HS256','RS256']`) — the realistic victim shape.
- **FP**: libraries that *do* enforce order (verify allowlist before key
  construction — the 3.3.0 lesson: key-wrap errors can mask a working
  allowlist; test both orderings).
- **CWE-347**. Pairs with CLASS-02.

### CLASS-02 — Key-type / algorithm confusion
- **Signature**: symmetric secret accepted from asymmetric material; any
  place key bytes and `alg` are independently attacker-influenced.
- **Invariant**: key material must never be used as an HMAC secret unless it
  is symmetric (python-jose 3.4.0's own fix sentence).
- **Oracle**: two-arm, forge HS256 with each *public* key format the victim
  may hold (PEM, OpenSSH `ecdsa-sha2-*`, `ssh-ed25519`, `ssh-dss`, JWK-JSON,
  cert) × each allowlist shape (mixed / single-family / none). This exact
  matrix is the calibration engagement's E1–E9/E7 series.
- **FP**: guard present but shape-based (string blacklist) → not a false
  positive but a *variant lead*: run enumeration-gap analysis.
- **CWE-327**. Family: CVE-2024-33663, CVE-2022-29217 (PyJWT), and the 2026
  PyJWT JWK-HMAC fixes — the class persists across ecosystems; check your
  dependency tree's turn.

### CLASS-03 — Cipher-mode misuse
- **Signature**: ECB anywhere; static/hardcoded IV; GCM nonce derived from a
  counter that resets or from a CSPRNG seeded once per process.
- **Invariant**: identical plaintext must never produce identical
  ciphertext; nonces never repeat under one key.
- **Oracle**: encrypt the same plaintext twice → equal prefixes = ECB/static
  IV (deterministic, 3× floor).
- **FP**: fixed test vectors that *look* static; deterministic-but-intended
  protocols.

### CLASS-04 — Unauthenticated encryption
- **Signature**: cipher without MAC (or MAC computed over plaintext only).
- **Invariant**: ciphertext integrity must be checked before any plaintext
  use (AEAD or encrypt-then-MAC).
- **Oracle**: flip one ciphertext bit → observable difference in
  plaintext-processing vs authentication error = hit.

### CLASS-05 — Hash downgrade in security context
- **Signature**: MD5/SHA-1 on passwords, tokens, signatures, cache keys of
  secrets.
- **Invariant**: security decisions use hash families without practical
  collision/preimage attacks (SHA-256+).
- **Oracle**: static + config-level proof; runtime oracle rarely needed —
  cite the call site anchor and the decision it feeds.

### CLASS-06 — MAC from raw hash
- **Signature**: `hash(secret + message)` constructions instead of HMAC.
- **Invariant**: MACs use HMAC (or AEAD tags); length-extension must be
  structurally impossible.
- **Oracle**: append `|| padding || attacker_msg` to a captured digest and
  show a valid MAC (local lab only).

### CLASS-07 — Weak KDF
- **Signature**: `key = md5/sha256(password)`; PBKDF2 < 100k rounds; no
  salt; shared salt across users.
- **Invariant**: keys from passwords pass a memory/iteration-hard KDF with
  per-user salt.
- **Oracle**: static signature + cost computation (cite parameters, do not
  crack anything).

### CLASS-08 — Non-constant-time comparison
- **Signature**: `==`/`!=` on secrets, MAC tags, tokens; `in` on secret sets.
- **Invariant**: secret comparison time is independent of match position.
- **Oracle**: timing distribution over N=20 aligned-vs-misaligned inputs;
  significant delta = hit. On local lab only; on remote targets this is
  noisy — mark INCONCLUSIVE and park rather than claim.

### CLASS-09 — Padding-oracle surface
- **Signature**: decrypt → error type/latency depends on padding validity.
- **Invariant**: decryption failure is indistinguishable across failure
  causes.
- **Oracle**: two-arm differential: same ciphertext with valid vs invalid
  padding → distinguishable error/latency = surface (do NOT decrypt
  anything real; surface proof ≠ decryption).

### CLASS-10 — RNG misuse
- **Signature**: `random.*` for tokens/ids/keys; `uuid1()`; time-seeded;
  `os.urandom` absent from token generation.
- **Invariant**: security values come from a CSPRNG.
- **Oracle**: generate a batch, test for state correlation (reseed window,
  monotone outputs) — 20× floor, stochastic rules.

### CLASS-11 — Hardcoded or derivable keys
- **Signature**: base64/hex literals near crypto calls; keys from
  hostname/username/date; keys committed to the repo you audit.
- **Invariant**: keys are provisioned, not authored.
- **Oracle**: static proof is sufficient (anchor + the literal); runtime
  proof = decrypt a canary with the recovered key.

### CLASS-12 — Certificate / TLS validation bypass
- **Signature**: `verify=False`, `CERT_NONE`, hostname check disabled,
  `check_hostname=False`, custom `verify` that returns True.
- **Invariant**: chain + hostname validation cannot be disabled in
  production paths.
- **Oracle**: local MITM proxy with a self-signed cert → connection
  succeeds = hit (own lab only).

### CLASS-13 — Signature malleability / replay
- **Signature**: ECDSA without low-S normalization; no `jti`/`nbf`/`exp`
  enforcement; signature accepted then re-accepted.
- **Invariant**: a signature validates exactly one message exactly once.
- **Oracle**: mutate the s-component (malleability) or replay the token
  (replay) → acceptance = hit.

### CLASS-14 — Unvalidated header params & decompression bombs
- **Signature**: `crit` ignored; `zip` honored without a size bound;
  decompression of attacker-controlled compressed data (`zlib.decompress`
  on JWE/network input).
- **Invariant**: decompressed size must never exceed a fixed bound,
  whatever the compressed size; critical headers must be understood or
  rejected.
- **Oracle**: two-arm: compress `A × 1MiB` (deflate), send through the
  path → vulnerable arm materializes the full plaintext, fixed arm raises a
  size error. Exactly CVE-2024-33664's oracle (calibration E6/E6B).
- **FP**: paths that cap input *before* decompression — read where the cap
  sits; a cap on ciphertext is not a cap on plaintext.

### CLASS-15 — kid / rotation confusion
- **Signature**: JWKS fetched per-tenant without kid scoping; kid taken
  from token and used to select from *all* tenants' keys.
- **Invariant**: a token's key is selected from its own issuer's set only.
- **Oracle**: tenant-A token validated against tenant-B JWKS → acceptance
  = cross-tenant confusion (two-account proof in a local lab).

### CLASS-16 — Downgrade negotiation
- **Signature**: client-offered crypto params preferred over server policy
  (hash, cipher, TLS version chosen from the request).
- **Invariant**: the weaker party never selects the crypto policy.
- **Oracle**: request with weak params → weak params accepted = hit.

## 2. Reporting Rules

- Name the CLASS-NN in the finding title area; the auditor checks it.
- Every card's oracle runs under the two-arm discipline (Phase 4): the
  finding needs the differential plus a regression control showing legit
  crypto flows still work.
- Chain classes honestly: CLASS-01 + CLASS-02 is the classic pair, but each
  needs its own cell evidence — "obviously chains" is not evidence.
- Anything you cannot test in-lab (CLASS-08 remote, CLASS-12 on third-party
  infra) → INCONCLUSIVE + Park, never a hedged claim.

## 3. What This Catalog Is Not

It is not a substitute for a cryptographer, and it deliberately contains no
primitive-level attacks (differential cryptanalysis, side-channel capture
hardware, fault injection). It is the usage layer: where correct math is
wired into incorrect decisions. That layer is where real-world JWT/TLS bugs
actually live — including both CVEs rediscovered in the calibration
engagement (CLASS-02 and CLASS-14).
