# Reference — Report Templates

> Part of **mythos-bug-hunter v4.2.0** (package architecture).
> **Load when:** Phase 5: candidate-record and engagement-state JSON schemas, full report templates.
> Authoritative rules, Canon, and pipeline contracts live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts with the
> SKILL.md Canon or contracts, **SKILL.md wins**. Section numbering below is
> inherited from the v4.0 monolith and is intentionally non-sequential.

---

## 28. Output Schemas and Report Templates

### 28.1 Candidate Record Schema (JSON)

```json
{
  "id": "string, e.g. AUTHZ-001",
  "asset": "url",
  "boundary": "auth | authz | tenant | object | function | trust | protocol | supply-chain",
  "attack_class": "e.g. IDOR | smuggling | cache-poisoning | race | jwt-jku | prompt-injection | ssrf | ...",
  "hypothesis": "falsifiable statement in the section 11 grammar",
  "p_prior": "number 0-1, set at creation with provenance (§10.5)",
  "p_post": "number 0-1, latest posterior (§10.2)",
  "evidence_log": [{"event": "observation", "lr": "+4", "rationale": "why this LR"}],
  "baseline": {"request": "...", "response": "..."},
  "control": {"request": "...", "response": "..."},
  "test": {"request": "...", "response": "..."},
  "difference": "precise difference between test and baseline/control",
  "security_significance": "which section 8.2 criterion it affects and why",
  "impact": "concrete demonstrated impact",
  "reproduction": {"steps": ["..."], "runs": 0, "successes": 0, "rate": "0.0"},
  "verdict": "CONFIRMED | LIKELY | INCONCLUSIVE | FALSE POSITIVE | NOT APPLICABLE",
  "verdict_rationale": "why this verdict under section 6.3",
  "validation_gaps": ["missing component, empty only when CONFIRMED"],
  "reportability": {"gate": "PASS | FAIL | NOT_EVALUATED", "failed_criteria": ["A-G ids"]},
  "next_todo": "todo id or null"
}
```

### 28.2 TODO and Engagement State Schemas (JSON)

```json
{
  "id": "T-014",
  "priority": "P0 | P1 | P2 | P3",
  "target": "endpoint/surface",
  "hypothesis": "section 11 grammar",
  "p_prior": "number 0-1",
  "p_post": "number 0-1",
  "method": ["step 1", "step 2"],
  "expected_signal": "what supports",
  "refuting_signal": "what refutes",
  "evidence_required": ["captures"],
  "status": "TODO | IN-PROGRESS | DONE | BLOCKED | WONT-DO",
  "fed_candidate": "candidate id",
  "resulting_verdict_change": "from -> to"
}
```

```json
{
  "target": "program name",
  "mode": "R | V | E | F",
  "phase": "1-8",
  "scope": {"assets": [], "allowed": [], "forbidden": []},
  "inventory_ref": "section 14 structure",
  "candidates": ["candidate records per 24.1"],
  "tested": [{"asset": "", "endpoint": "", "method": "", "hypothesis": ""}],
  "disproven": [{"hypothesis": "", "evidence": ""}],
  "todo_queue": ["todo records per 24.2"],
  "next_todo": "id",
  "blockers": [{"what": "", "unblocked_by": ""}]
}
```

### 28.3 Report Templates

**Operational response (default, every turn — section 29):**

```
[STATE]   <phase> | candidates: C/L/I/FP/NA counts
[MODE]    <R/V/E/F>
[OBJ]     <one-line current objective>
[OBS]     <key observation from last test — data, not interpretation>
[EVID]    <artifact references>
[TODO]    <next pin-point TODO with priority>
[BLOCK]   <blocker or none>
```

**Candidate finding report (operator-facing):**

```
CANDIDATE: <id>
ASSET:     <url>
BOUNDARY:  <per section 3.2>
CLASS:     <attack class>
HYPOTHESIS:
  <precise statement>

TESTS:
  1. BASELINE  <request> → <response fingerprint + excerpt>
  2. CONTROL   <request> → <response>
  3. TEST      <request> → <response>

DIFFERENCE:           <what changed, precisely>
SECURITY SIGNIFICANCE:<why it matters — section 8.2 criterion>
IMPACT:               <concrete, demonstrated>
REPRODUCTION:         <steps> (runs: n/m)
VERDICT:              <verdict> — reason: <rationale / missing component>
NEXT:                 <TODO or reportability status>
```

**Final report (submission-ready):**

```
# Vulnerability Report: <short title>

## Summary
<1-3 sentences: issue + impact>

## Severity
<qualitative> (CVSS <version> <vector> = <score>, only if computed per section 12.4)

## Affected Component
- Asset / Endpoint / Parameter / Version-build evidence

## Scope Confirmation
- In-scope per <program reference>; testing method used

## Root Cause
<why the issue occurs, at behavior level>

## Security Boundary Violated
<named boundary>

## Evidence
### Baseline Request / Response
### Control Request / Response
### Test Request / Response
### Difference
<verbatim captures, annotated>

## Impact
<demonstrated impact, not hypothetical>

## Reproduction Steps
1. ...
2. ...
(run rate for stochastic/AI findings per section 24.4)

## Suggested Remediation
<concrete fix>

## Disclosure Timeline
- <date>: discovered / reported / ...
```

---
