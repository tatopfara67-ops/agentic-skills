# trust-map-and-sinks.md — Terrain, Guards, and the Hypothesis Forge

> Load when: entering a codebase cold; building the trust map; triaging
> sinks and validators. SKILL.md wins on conflict.

## 1. Phase 1 — The Trust Map

A codebase is not a list of files; it is a set of **paths untrusted input
can walk**. The trust map is that set, one row per entry point:

```
entry                 → parser            → guard                 → sink
--------------------------------------------------------------------------------
POST /api/login       → json body         → schema check          → db.execute
jwt.decode(token,k)   → jws header/claims → alg allowlist;        → backend verify;
                                            HMACKey blacklist       zlib.decompress
jwe.decrypt(tok,k)    → header/zip        → JWE_SIZE_LIMIT (3.4+) → decompress → AESGCM
queue consumer        → protobuf          → none                  → os.system
```

Census targets (find them, don't read them yet):

- **Entry points**: routes/handlers, RPC methods, queue consumers, CLI
  argument parsers, cron entry functions, file/drop watchers, webhook
  receivers, template render entry.
- **Trust boundaries**: where untrusted bytes become objects (parsers,
  deserializers) and where identity is decided (authn), checked (authz), or
  assumed (internal-only calls reachable from outside anyway).
- **Guards**: allowlists, validators, sanitizers, type checks, size caps,
  blacklists — write down *which shape they are*: structural (type/parsing)
  or shape-based (string matching). Shape-based guards are leads, not
  comfort (see patch-archaeology §5).
- **Sinks**: exec/eval, SQL builders, path joins, serializers, decompress,
  template engines, crypto calls (→ catalog lookup, not sink triage).
- **Crypto touchpoints**: token issue/verify, TLS setup, KDF, RNG — one row
  each; these go to the misuse catalog in Phase 3, not to the generic sink
  pile.

Reading order: **edges → guards → sinks → middle.** Budget rule: no more
than 20% of reading time inside "the middle" before every edge has a map row
(Phase 1 gate).

Output: one `TRUST-MAP` ledger record per row. The map is the audit's table
of contents; every later hypothesis cites a row.

## 2. Validator Inversion (Phase 3 operator)

For every guard on the map, ask: **what input is accepted-but-wrong?**

| Inversion axis | Probe |
|----------------|-------|
| type           | wrong primitive that passes a duck-type check (`"5"` vs `5`) |
| encoding       | double-encoded, mixed-case hex, unicode-escaped (`%u002e`) |
| emptiness      | missing key, `null`, `[]`, `""`, `-1`, `0` as sentinel |
| boundaries     | off-by-one, negative, `2^31`, `-2^63`, float `NaN` |
| ordering       | check-then-use TOCTOU; reorder fields/claims |
| format family  | sibling formats the guard's strings don't cover (enumeration gaps) |

The last axis is the calibration engagement's engine: the HMAC guard
rejected PEM-string shapes; the *format-family* axis (OpenSSH markers) was
the accepted-but-wrong input. When a guard is a list, inversion = diffing
the list against its family.

## 3. Sibling Rotation (Phase 3 operator)

When you find one path with property P, rotate through its siblings and
require they be tested or parked:

- other **backend** for the same feature (python-jose: `native.py` vs
  `cryptography_backend.py` — the confusion guard had to be checked in both);
- other **format** accepted by the same entry (PEM / OpenSSH / JWK / DER);
- other **entry point** reusing the same parser (jws vs jwe share base64url
  and key-construction machinery);
- other **caller** of the same sink (every `zlib.decompress` caller, not
  just the JWE one).

Rotation is forced work: an audit that only follows the first anomaly it
sees is an audit with a sample size of one.

## 4. VCS Abduction (Phase 3 operator)

Weird code is evidence of a past event:

- `git blame` / `git log -L` on the odd line: what commit, what message?
  "fix #1234", "revert", "hotfix" near a guard = the guard is fear-driven;
  find what scared the author, then find whether the fear was fully
  addressed.
- Comments that contradict code ("this is safe because X" next to a check
  that does not implement X) — the comment records intent, the code records
  reality; the gap is a pre-registered hypothesis.
- Dead branches, commented-out checks, `# TODO` in guards: the author knew.

Abduction output is a *prediction*, not a finding: "this guard was added
after an SSRF report, but only covers http:// — predict file:// and gopher://
variants" → cells.

## 5. Sink Catalog (quick tables, per family)

Python: `eval exec compile __import__`, `pickle.loads`, `yaml.load` (no
Loader), `subprocess.*` with `shell=True` or list-strings, `os.system`,
raw SQL string concat (`execute(f"...{x}")`), `open()` with joined paths,
`jinja2 Template(...)` on user strings, `zlib.decompress`, `marshal`,
`ctypes`.

JS/TS: `eval`, `new Function`, `child_process.exec`, `vm.runIn*`,
`serialize unserialize` (node-serialize), template string SQL,
`res.sendFile` with user path, DOM sinks (`innerHTML`, `document.write`),
`JSON.parse` on prototype-polluted merge (`merge`, `lodash.set`).

Java: `Runtime.exec`, `ProcessBuilder`, JNDI lookups with user strings
(LDAP/RMI — log4shell class), `ObjectInputStream.readObject`, SpEL/OGNL on
user input, string-concat SQL, `XMLDecoder`, XXE-default parsers.

Go: `exec.Command` with user strings, `text/template` HTML contexts,
`unsafe`, `reflect` on user JSON, path joins with `..`, `md5` for security
decisions.

Each sink hit = hypothesis with prior 5–15% (scanner-grade) until raised by
an operator insight (reachable from an entry row? guard is shape-based?
format sibling unguarded?). Reachability is what turns a sink line into a
finding candidate: walk the map, don't just match strings.

## 6. Taint-Lite (manual data flow)

Between an entry row and its sink, walk the variables by hand (or with an
AST query): where is the value parsed, stored, transformed, checked? You are
not building a full taint engine; you are answering one question per map
row: **can untrusted bytes reach this sink without crossing a structural
guard?** If yes → H-record. If unknown (framework magic, reflection,
serialization boundaries) → H-record with lower prior and a runtime probe as
oracle. Tooling escalation path: manual → `rg` context walks → AST queries
(`ast`/`ts-morph`/`tree-sitter`) → semgrep/CodeQL as *hypothesis factories*
(R5 — their output enters the same gates).

## 7. Hypothesis Contract (code edition) — with priors guidance

```
H-NNN
  claim    : one sentence, falsifiable
  anchor   : path/file.py:LINE@version
  invariant: the rule the code should uphold
  oracle   : cell design + falsifier
  prior    : % + reason
```

| Reason | Prior band |
|--------|-----------|
| enumeration-gap prediction (list vs family) | 60–75% |
| patch sibling in same/adjacent module | 70–85% |
| guard is shape-based where structure is needed | 55–70% |
| VCS abduction (fear-driven guard, partial fix) | 40–60% |
| unguarded sink reachable from an entry row | 20–40% |
| bare scanner hit, reachability unknown | 5–15% |

Priors are for budget allocation (R7), never for report language: a 15%
hypothesis that gets a clean oracle result outranks an 85% hunch that never
ran.

## 8. Triage Matrix (what to run first)

1. Enumeration gaps and patch siblings (Phase 2 outputs) — highest prior,
   cheapest oracles.
2. Crypto touchpoints — catalog cards give ready-made cell designs.
3. Shape-based guards on the map — inversion + format-family sweep.
4. Reachable unguarded sinks from entry rows.
5. Scanner output backlog — bottom of the queue, top of the volume; run
   only what a map row makes reachable.
