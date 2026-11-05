# Reference — Research Protocol

> Part of **mythos-bug-hunter v4.7.0** (package architecture).
> **Load when:** Long engagements (context-window discipline) and keeping the skill current (TRENDFRESH web-research protocol, source priority).
> Authoritative rules, Canon, and pipeline contracts live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts with the
> SKILL.md Canon or contracts, **SKILL.md wins**. Section numbering below is
> inherited from the v4.0 monolith and is intentionally non-sequential.

---

# Part VI — Governance and Mindset

## 29. Context-Window Discipline and Response Format

Context is a finite budget. Wasting it on restatement degrades precision.

### 29.1 Default Response Shape

Unless a technical decision requires depth, every response contains only:

```
OBJECTIVE : what we are doing right now
OBSERVATION: data from the last test (not interpretation)
EVIDENCE  : artifact references
STATUS    : current verdict / state summary
NEXT      : the next TODO
BLOCKER   : if any
```

### 29.2 Verbosity Rules

- Do not restate known context, repeat prior reasoning, or re-explain the
  methodology to the operator mid-engagement.
- Prefer tables, lists, and structured blocks over prose.
- State assumptions inline instead of padding disclaimers.
- Be verbose only for: a CONFIRMED finding's full evidence chain, a
  non-obvious root cause, a stop/skip justification, or an explicit
  operator request for detail.

### 29.3 Forbidden Wastes

Restating the full scope every turn; re-explaining the validation loop;
listing all TODOs every turn (state lives in §18); preambles ("I will now
analyze..."); postambles ("In conclusion...").

---

## 30. Web Research and Trend Refresh Protocol

### 30.1 Source Priority

1. **Primary/authoritative** — vendor advisories (php.net, Next.js/Vercel),
   CVE records (NVD/MITRE), CISA alerts/KEV, OWASP project pages (top10,
   genai.owasp.org), RFCs, official program policy.
2. **Credible secondary** — established research teams and labs
   (PortSwigger Research, watchTowr, Huntress, Sansec, Unit42, Datadog
   Security Labs, Google Cloud blog, Invariant Labs), conference talks.
3. **Community** — forums, Reddit, aggregators: cross-verify before use.

### 30.2 TRENDFRESH — Keeping This Skill Current

The threat landscape moves (php2shell landed days before this revision).
When engaging a new target, or when the operator mentions a recent
incident, run a refresh pass:

```
1. TRIGGER — new engagement, new stack fingerprint, operator mentions an
   incident/CVE, or the last research pass is >90 days old.
2. QUERY — current advisories for the identified stack (engine, framework,
   CDN, auth library, AI provider/MCP tooling).
3. VERIFY — affected versions/configurations against primary sources;
   note publication dates; discard unsourced claims.
4. CLASSIFY — for each item: exposure state per section 25.2 step 3
   (vulnerable version / vulnerable configuration / exploitable path).
5. INTEGRATE — new items become inventory entries (section 14) and
   hypothesis TODOs (section 15), not conclusions.
6. CITE — every fact carried into a report cites its primary source.
```

### 30.3 Research Discipline

- A single source is never absolute truth, especially where the target's
  context differs.
- Verify time-sensitive claims ("affects version X") against the target's
  observed version evidence.
- Distinguish documented fact from hypothesis; cite facts.
- If research contradicts observed behavior, trust the observation and
  investigate the discrepancy.

---
