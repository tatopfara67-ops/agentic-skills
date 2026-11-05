# operator-os.md — the Hotz runtime: notice, think, behave, script

> A17's layer. Load when the teardown RUNS. Doctrine (SKILL.md) states
> the dismantle laws; the M-protocol (references/method-upgrade.md)
> states the gated ladder and symbol-trust protocol; THIS module is
> the runtime — how the agent notices, thinks, behaves, and scripts
> while executing them, characteristic of George Hotz's documented craft:
> the shipped artifact is a confession — read it before you debug it,
> primitives before exploits, and local data flow before network flow.

## 1. The thinking framework — decision rules

R1 **The artifact confesses first.** Strings, symbols, class dumps,
entitlements, syscall surface — the binary/package tells you what it
does before any debugger attaches. Reading beats executing. *From:*
the lineage's documented method arc — the iPhone/PS3 work began in
static artifact analysis (the first unlock came from reading what the
baseband checked, not from spraying it).

R2 **Primitives before exploits.** A write primitive, a read
primitive, a call primitive — collect them as named capabilities with
preconditions; the exploit is the composition, and composition comes
later.

R3 **Local data flow before network flow.** Where does the artifact
store, cache, and trust local state (prefs, keychains, sqlite,
logs)? Local trust mistakes outnumber network ones and compose into
them.

R4 **Symbols are graded, not trusted.** Symbol names assert ("secure
verify") but the disassembly decides — the symbol-trust table grades
each load-bearing name: verified, contradicting, or unknown.

R5 **The ladder is gated.** Static read → dynamic confirm → primitive
isolation → composition; each gate requires the previous rung's
records. Skipping to "try the exploit" is the failure mode this organ
exists to kill.

R6 **Debuggers are for questions, not tours.** Attach with a specific
question ("what validates this blob?"), answer it, detach; wandering
sessions generate noise and burn the engagement's rhythm.

### The opening ladder — where Hotz's candidates come from

The rules above govern the descent once the artifact is in hand; the
ladder produces what the descent hunts FIRST — the unlock-era
perception (the first unlock came from READING what the baseband
checked, not from spraying it; the artifact confesses to a reader
before it performs for an executor) made runnable as questions. Every
rung is a static question that writes inventory rows — no rung
attaches a debugger, sends a packet, or spends the anomaly budget;
dynamic work stays gated behind R5/R6 and consumes the ladder's rows.

| # | The question | What it hunts | Grounding |
| --- | --- | --- | --- |
| G1 | What does the artifact confess before anyone runs it? | strings, symbols, class dumps, entitlements, manifest — the surface inventory every later rung reads | R1's tradition: the 2007 unlock began in static reading of what the baseband checked (sources.md, primary record) |
| G2 | Where does the artifact store, cache, and trust local state? | prefs, keychain, sqlite, logs, plaintext caches — the local-data trust map with its read/write actors | R3's law; the operator-brief lineage ("understand how it manages sensitive data locally client-side before it is sent to the server" — sources.md) |
| G3 | Which symbols claim authority the bytes never earned? | load-bearing names ("verify", "harden", "secure") graded against disassembly — a CONTRADICTING grade is a candidate | R4's symbol-trust table — the organ's own operationalization, labeled |
| G4 | What did the newer build silently stop doing? | the version delta: removed checks, retired strings, changed constants — the vendor's unannounced edit | T5's diff economy — the organ's own operationalization, labeled |
| G5 | Which client-side gates does the client itself trust? | admin gates, feature flags, debug stubs, hidden routes — each a differential hypothesis about what the server re-checks | SKILL §3 law 5 (client logic is a hypothesis about server logic) + the four-inventory contract (teardown-ladder §4B) |

Ranking rationale: candidate priority = contradiction × local-trust
reach × delta freshness. A CONTRADICTING symbol grade tops the order —
the name claimed security and the bytes disagree, which is exactly
where the unlock-era reading lived; plaintext local state holding
tokens/PII ranks next (report-grade, priced by reach); a silent
version-delta candidate ranks by what the removed check used to gate;
UNKNOWN-graded symbols rank last — they are questions, not candidates.
Rows out; the artifact untouched by executors.

Generation falsifier: an in-scope artifact where the sweep yields
zero candidate rows across every row class means the ladder is
missing a rung for that artifact class (a container image, a WASM
bundle, a signed desktop daemon) — the census is re-read, the missing
rung is written with its grounding row. The artifact is never excused
as "clean" at generation time: a zero-yield verdict belongs to
verification's coverage row (M5), never to the ladder.

#### The ladder's payload kit — the confession sweep rows (customize before use)

Generation writes rows; these are the static sweep classes the rows
name, every one a local read of the pinned artifact (the sourcemap row
is the single fetch exception and runs under the acquisition record —
one fetch, same host, recorded):

| Sweep row | The read payload | Writes which row |
| --- | --- | --- |
| host/endpoint row | `strings -n 8 Art.bin > s.txt; rg -io "https?://[a-z0-9._-]+" s.txt \| sort -u` | endpoint inventory row (incl. internal/debug hosts) |
| secret-hint row | `rg -i "api.?key\|token\|secret\|passwd\|bearer" s.txt` | masked secrets-hint row (policy: report-only) |
| gate row | `rg -i "debug\|staging\|verbose\|test.?mode\|isAdmin" s.txt` + the manifest's flag list | client-gate candidate row |
| storage-profile row | the platform paths (iOS keychain/NSHomeDirectory; Android SharedPreferences/data/data; desktop %APPDATA% equivalents) | local-state trust row |
| entitlement row | the permission/entitlement list as claimed by the manifest | privilege-claim row (graded, never trusted — R4) |
| sourcemap row | `rg -o "sourceMappingURL=[^ ]+" bundle.js` then the one recorded fetch | original-source row |
| delta row | `diff <(sort -u s1.txt) <(sort -u s2.txt)` across pinned builds | silent-change candidate row |

Customization knobs, stated in the plan note: the artifact class
(JS / APK / IPA / binary — which descent ladder and which
storage-profile rows load), the sweep depth (strings min-length and
which row classes run — narrowed to the hypothesis class that
justifies the descent, per R7's budget), and the entitlement/storage
profile (iOS vs Android vs desktop path sets). The descent mechanics
per class live in teardown-ladder.md; this kit is the opening sweep
that decides which rung of it is worth climbing.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| A client artifact lands | Read before you run it | T1 strings/symbols/entitlements sweep | Never open with a debugger attached |
| A juicy symbol name appears | Grade it against disassembly | T2 symbol-trust row | Never trust the name (R4) |
| Static reading stalls | ONE dynamic question | T3 target the exact validation point; answer; detach | Never tour the process |
| A capability emerges | Name it as a primitive | T4 primitive card with preconditions | Never chase impact mid-isolation |
| Two artifacts differ (versions) | Diff is the map | T5 binary diff rows | Never re-read both from scratch |
| Exploit composition tempting | Check the ladder gates | gate rows verified first | Never skip isolation (R5) |
| Local storage found | Map its trust decisions | prefs/keychain rows with read/write actors | Never skip local for network glamour (R3) |

Pacing: long quiet static phases punctuated by surgical dynamic
probes — minutes of execution per hours of reading. Failure reaction:
a dynamic answer that contradicts the static map → the MAP is corrected
first, then the primitive re-graded (static-first discipline).

## 3. The scripting arsenal — techniques as runnable craft

### T1 — the artifact confession sweep

```bash
# mobile binary shape: classes, entitlements, linked libs, strings of interest
<otool-class-dump> App.bin > classes.txt 2>/dev/null; wc -l classes.txt
<otool-entitlements> App.bin 2>/dev/null | head -20
strings -n 8 App.bin | rg -i "api|key|token|secret|debug|http" | head -30 > strings_hits.txt; wc -l strings_hits.txt
```

Read-out: the static surface inventory. Gate: the teardown ledger's
first rows come from here (R1) — dynamic work cites them.

### T2 — symbol-trust grading

```bash
python3 - <<'PY'
rows = [
 # symbol, claimed behavior, disassembly verdict, grade
 ["_verifySignature", "validates sig", "checks length only", "CONTRADICTING"],
 ["_decryptConfig",   "decrypts",      "xor with fixed key",  "VERIFIED (weaker than name implies)"],
 ["_hardenSession",   "hardening",     "not reached in any path", "UNKNOWN"],
]
for s, c, d, g in rows: print(f"{s:20} {g:34} disasm: {d}")
PY
```

Read-out: the graded symbol table. Gate: load-bearing claims cite
grades, never raw names (R4).

### T3 — one question, one breakpoint

```bash
# attach with a purpose; the question is pre-written
lldb -b -o "breakpoint set --name _verifySignature" \
     -o "process launch --stop-at-entry" \
     -o "register read x0 x1" \
     -o "memory read \$x0" -o "detach" -- App.bin 2>&1 | tail -12
```

Read-out: the targeted answer (argument + memory at the validation
point). Gate: dynamic sessions file their question + answer pair (R6);
tours are refused.

### T4 — primitive card

```bash
python3 - <<'PY'
card = {"name": "fixed-key-config-read",
        "class": "read primitive",
        "precondition": "config blob cached locally (found: R-503)",
        "observable": "plaintext config on disk after launch",
        "composed_into": "pending"}
print(card)
PY
```

Read-out: the named capability. Gate: primitives carry preconditions +
observables (R2); unconditioned "bugs" are not material yet.

### T5 — version diff rows

```bash
# two builds of the same artifact: what changed is the map of what to re-read
<bindiff-tool> App-v1.bin App-v2.bin 2>/dev/null | rg "changed|added|removed" | head -20
# or at the string level:
diff <(strings -n 8 App-v1.bin | sort -u) <(strings -n 8 App-v2.bin | sort -u) | head -20
```

Read-out: changed symbols/strings between versions. Gate: re-analysis
targets the diff, not the whole artifact (R1's economy).

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | artifact + version pinned | static confession sweep | T1 | inventory rows | FACT |
| S2 | inventory exists | grade load-bearing symbols | T2 | trust table graded | FACT |
| S3 | trust table hot | one question per dynamic probe | T3 | question/answer pairs | EXPERIMENT |
| S4 | behavior understood | file primitive cards | T4 | preconditioned capabilities | FACT |
| S5 | primitives collected | compose across gates (ladder verified) | T5 when versions differ | gate rows cited | EXPERIMENT |
| S6 | composition proven | exit: primitive register + re-grade notes | — | symbol table final | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A dynamic probe with no pre-written question → R6 violation; the
  session is noise and its rows are struck.
* A claim citing a symbol NAME against a CONTRADICTING grade → R4
  violation; the disassembly wins.
* Composition attempted with unconditioned primitives → R5 violation;
  back to the isolation rung.
* A full re-read of both artifact versions where a diff existed →
  burned budget; the economy rule (R1) was violated.
