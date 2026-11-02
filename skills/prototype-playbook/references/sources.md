# Reference — Sources (lineage verification)

> Part of **prototype-playbook v1.0.0** (package architecture).
> **Load when:** the lineage claim needs its citation; the attribution
> boundary (what is Heyes', what is PortSwigger's wave, what is this
> bundle's) needs restating. Authoritative rules live in
> [`../SKILL.md`](../SKILL.md) — **SKILL.md wins** on any conflict.

---

## 1. The lineage, verified

**Gareth Heyes — PortSwigger Research.** Verified record:
* *Server-side prototype pollution: Black-box detection without the
  DoS* — portswigger.net/research, published Feb 15, 2023 (updated
  Mar 28, 2023); presented at NullCon Berlin 2023 and OWASP Global
  AppSec Dublin 2023 (slides on record). The safe-detection corpus
  (status-code override, JSON spaces, header reflection, OPTIONS,
  immutable prototype, OAST) that this organ's no-DoS law implements.
* *Widespread prototype pollution gadgets* — PortSwigger Research;
  the research behind the Web Security Academy's third-party-library
  pollution labs; the codification of gadget hunting as a discipline.
* **DOM Invader** — the Burp browser extension that finds XSS,
  prototype pollution, and postMessage issues; Heyes is its public
  author/face (his own usage documentation and talks). The proof that
  the object world is systematically scannable — this organ's
  automation thesis.

**The research wave** (cited without individual figure attribution
where the record does not carry one):
* *DOM Clobbering strikes back* — PortSwigger Research, Feb 6, 2020:
  the modern clobbering revival (record verified as PortSwigger
  Research; no individual author attribution is claimed on it here —
  the lineage registry's correction field keeps this explicit).
* PortSwigger **Web Security Academy** — the prototype-pollution
  module (client-side sources, server-side safe detection, gadget
  chains, DOM Invader workflows): the codified teaching order this
  organ's source→gadget→sink procedure follows.

## 2. Attribution boundary

Heyes' verified corpus = the safe-detection repertoire, the gadget
discipline, DOM Invader. This organ's own contributions: the
three-family unification under one root-cause doctrine (inherited /
ambient / channel trust), the no-DoS law stated as a hard rule with
the benign-twin control on every probe, the self-owned-both-ends law
for postMessage proofs, and the gadget library's versioned
card format. None of those rules appear in the cited research; they
are the arsenal's evidence law applied to the object world.

## 3. Verification record

| Claim | Source | Status |
| --- | --- | --- |
| Heyes: PortSwigger Research, server-side PP article Feb 2023 | portswigger.net/research/server-side-prototype-pollution | verified |
| Presented NullCon Berlin 2023 + OWASP Global AppSec Dublin 2023 | the article itself (presentation note + slides) | verified |
| Widespread prototype pollution gadgets (Heyes) | academy lab citations naming the research | verified |
| DOM Invader finds XSS, PP, postMessage (Heyes) | PortSwigger blog + his own usage record | verified |
| DOM Clobbering strikes back, Feb 2020 | portswigger.net/research/dom-clobbering-strikes-back | verified (as PortSwigger Research; author unnamed on record) |
| Academy PP module (source→gadget→sink order) | portswigger.net/web-security/prototype-pollution | verified |
