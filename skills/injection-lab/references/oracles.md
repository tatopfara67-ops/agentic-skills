# The Oracle Catalog

## Grammar per injection class

### SQL (relational)

* Boolean: `param=1' AND 1=1--` vs `param=1' AND 1=2--` — the pair is ONE
  treatment; delta = a stable response difference. Control: `param=1' AND
  1=1 XOR 1=2--` or a syntactically-valid always-true shape on a
  non-injectable field of the same request.
* Error signature: quote-imbalance producing a DRIVER-SPECIFIC error
  family (syntax/unterminated/aggregate messages). Control: same quotes
  on a field the server echoes but does not parse.
* Timing: arithmetic-delay functions with an interleaved no-delay control
  and latency subtraction. Single slow responses close nothing.
* Out-of-band: DNS/HTTP canary channel via string functions; the callback
  payload embeds a self-owned marker.

### NoSQL (document/key-value)

* Boolean via operator injection: `{"$ne": null}` shapes, `$regex`
  truth-probing; delta discipline identical to SQL boolean.
* Timing: `$where`-style script fields or regex catastrophic-backtracking
  shapes — repetition floors apply.
* Type confusion: sending an array/object where a scalar is expected —
  the CONTROL sends a DIFFERENT wrong type, separating parser leniency
  from evaluator injection.

### Command injection

* Separator grammar (`;`, `|`, `&&`, newline, backtick) with a canary
  echo: the treatment appends a marker-writing command; the control
  appends the marker as inert text. Delta = the marker arriving through
  the execution channel only.

### Template injection (SSTI)

* Probe expressions per engine family (`${7*7}`, `{{7*7}}`, `<%= 7*7 %>`,
  `#{7*7}`) — CONFIRMED requires the evaluated artifact (`49`) in the
  response, not a reflected template string. Control: the same expression
  wrapped so the engine treats it as literal.

## Oracle strength ladder (weakest sufficient channel first)

1. error signature (cheapest, if errors surface)
2. boolean differential (silent drivers)
3. timing (blind drivers; expensive — floors apply)
4. out-of-band (blind + filtered; needs operator interaction host)

Choosing a STRONGER channel than needed wastes requests and weakens the
evidence (timing deltas argue with clocks; OOB argues with infrastructure).
The report states which rung closed the hypothesis and why the weaker
rungs could not.

## Floor-and-skyline quick table

| Oracle | Floor | Skyline |
| --- | --- | --- |
| Error / boolean | 3 identical deltas | continue while unstable |
| Timing | 5 timed pairs + interleaved controls, delta > 2× control spread | until spread stabilizes |
| OOB | 1 canary callback + 1 negative control payload | callbacks counted, not spammed |

## Extraction bounds (Phase 4 only)

Canary-marker extraction first (self-injected string through the channel);
then ONE bounded schema step (version banner or single name) — then
synthesis. The impact story is "arbitrary query execution demonstrated on
a canary", never "the database was dumped".
