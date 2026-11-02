# object-model-attacks.md — the three families, probe by probe

> Part of **prototype-playbook v1.0.0** (package architecture).
> **Load when:** any family of the SKILL.md procedure needs its exact
> probes, oracles, and falsifiers. Authoritative rules live in
> [`../SKILL.md`](../SKILL.md) — **SKILL.md wins** on any conflict.

---

## 1. Client-side prototype pollution

### The source sweep

Per source, one probe each, canary property, benign-twin control:

| Source | Probe shape | Oracle |
| --- | --- | --- |
| URL hash | `#__proto__[cb]=marker` then trigger the read | canary observable fires; twin does not |
| query string | `?__proto__[cb]=marker` | same |
| JSON body | `{"__proto__":{"cb":"marker"}}` | same, via the merge path |
| constructor path | `?constructor[prototype][cb]=marker` | bypasses naive `__proto__` filters |

Canary properties are reads the page performs anyway (a link text, a
field default, a console-detectable lookup). The twin request is the
identical probe with a non-directive key (`__protoz[x]=marker`) — if
the twin also fires, the observable is not ours.

### Falsifiers worth recording

Sanitized merges (keys filtered, `Object.create(null)` targets, Map
instead of plain objects) — record which defense, because the
*absence* of a defense on a sibling endpoint is the next hypothesis.

## 2. Server-side pollution — the no-DoS repertoire (Heyes 2023)

The server-side danger: a real property write persists for the Node
process's lifetime and breaks function for everyone. The safe
repertoire probes with **harmless properties whose only footprint is
an observable response difference**:

1. **Status-code override** — pollute a property the framework reads
   as the response status (`{"__proto__":{"status":510}}`): a 510
   where 200 came back is the oracle; harmless, request-scoped in
   effect.
2. **JSON spaces** — pollute the serializer's indent option
   (`{"__proto__":{"jsonSpaces":3}}`): the next JSON response comes
   back pretty-printed. The most famous safe oracle.
3. **Exposed headers / OPTIONS reflection** — pollute CORS option
   objects; the preflight response reflects the canary header name.
4. **Content-type override** — response `Content-Type` shifts to the
   canary value.
5. **Immutable-prototype error** — probing with an
   `Object.prototype`-bound key that raises a framework 500/400 with
   a distinguishable signature when the write path exists.
6. **OAST callback** — where a sink could perform a fetch, a canary
   DNS/HTTP callback under the operator's own OAST-style endpoint
   (channel law applies: one hit, then stop).

Each probe: benign-twin control (`__protoz`), n_runs ≥ 2, and the
reversibility note (request-scoped effects only; no persistent
process state written — that is the law, not a preference).

### The escalation ladder after a safe positive

Positive safe probe ⇒ pollution exists ⇒ NOW the gadget hunt runs
(never before): read the target's own code for option-object reads
(`cfg.x`, `options.y` defaults) reachable from the polluted surface,
then chain to the sink with the nonce/self-owned discipline of
xss-playbook's proof law.

## 3. DOM clobbering

### The source precondition

An HTML injection point with **attribute control** (even limited:
`id`, `name`, `href`, `src`) — clobbering writes the page's namespace,
not its markup.

### The probe families

| Target reference | Clobber element | Notes |
| --- | --- | --- |
| `window.x` (object expected) | `<a id=x>` | the anchor object with `href`'s parsed parts answers |
| nested `x.y.z` | `<a id=x><a id=x name=y>`... | stepped clobbering for deeper references |
| form/document refs | `<form id=f><input name=...>` | form controls bind as named properties |
| `document.x` vs `window.x` | distinct binds per host object | probe both sides |

Oracle: the script's behavior changes as its reference resolves to the
crafted element (observable: a value used in text, a fetch URL, a
redirect). Falsifier: the reference resolves to the genuine object
despite injection (explicit `var`/`let` declarations shadow clobbering
— record which, same-lesson rule).

### The classic amplifier

Clobbering → gadget in framework/library code that reads
`window.CONFIG.something` defensively — the crafted element's parsed
`href` parts answer the read; the sink does the rest.

## 4. postMessage origin confusion

### The listener map (from js-recon's inventory)

Per listener: which frames register it, what the handler reads
(`e.data` command shape), what it checks (`e.origin` exact? substring?
nothing? `e.source === parent`?), and what it does (DOM write, fetch,
reply).

### The probe, self-owned on both ends

The operator's sender page (self-owned origin) posts the crafted
message shape to the in-scope frame:

```
window.frames[0].postMessage({command:"..."}, "*")
```

Oracle families:
* **no check / weak check** — the handler executes the command for a
  foreign origin (observable: the DOM/fetch action fires);
* **substring origin check** — an attacker-controlled substring host
  passes (`target-attacker.tld` vs `target.tld`);
* **source-reply leak** — the handler replies sensitive data to
  `e.source` without re-checking it.

Falsifier: the handler rejects foreign origins cleanly — recorded, and
the next listener is the march.

### The escalation

postMessage confusion → DOM-write sink is xss-playbook's grammar;
postMessage → fetch-with-token is an ssrf-playbook/exfil question —
the channel law (one canary hit, then stop) rides along unchanged.

## 5. The gadget library (growable, versioned)

Entries follow module-smith's card shape (rank, references, worked
engagements) — the seed set:

| Gadget | Read family | Sink family |
| --- | --- | --- |
| string callbacks | `setTimeout(cbName, ...)` resolving a name through the chain | eval-family execution |
| transport/config options | `$.ajax`-style option objects read defensively | request shape, URL, headers |
| redirect targets | `location = cfg.next` | open-redirect sinks |
| sanitizer bypasses | polluting sanitizer option objects (allowed tags lists) | markup injection that WAS sanitized |
| framework router options | route option objects read at dispatch | DOM write, navigation |

Every entry carries the library and version it was proven on; every
fresh engagement re-verifies before use (first-written-prior rule,
glm-self-model G3: an untested gadget is a PROJECTION until its own
record exists).

## 6. Classification notes

* Client-side chain to DOM sink: the XSS-family vector on the serving
  path — xss-playbook's CVSS geometry, this organ's chain evidence.
* Server-side pollution with a status/serializer oracle only: the
  finding is the pollution itself (server misconfiguration/validation
  family); the RCE-class rating requires the observed sink chain,
  never the library's worst CVE folklore.
* Clobbering with attribute-only injection: score the achieved sink,
  not the injection primitive.
* postMessage confusion: score what the listener did for a foreign
  origin — a leak rides confidentiality; a command execution rides
  integrity of the frame.
