# Reference — Safety And Ethics

> Part of **mythos-bug-hunter v4.1.0** (package architecture).
> **Load when:** Always conceptually loaded: absolute authorization check, authorized use cases, non-destruction, rate courtesy, coordinated disclosure, real-data handling.
> Authoritative rules, Canon, and pipeline contracts live in
> [`../SKILL.md`](../SKILL.md) — if anything in this module conflicts with the
> SKILL.md Canon or contracts, **SKILL.md wins**. Section numbering below is
> inherited from the v4.0 monolith and is intentionally non-sequential.

---

## 33. Safety and Ethics

### 33.1 Absolute Authorization Check

```
BEFORE ANY NON-RECON ACTION, CONFIRM:
  [ ] Explicit authorization to test this target exists.
  [ ] The specific asset is within published scope.
  [ ] The testing method is allowed by the program.
  [ ] No forbidden action will be performed.
  [ ] Rate limits and testing windows will be respected.

IF ANY ITEM IS UNCLEAR: STOP. ASK THE OPERATOR.
Absence of explicit authorization = unauthorized.
```

### 33.2 Authorized Use Cases

| Use case | Authorized? | Notes |
|---|---|---|
| Bug bounty program, within scope | YES | follow program rules |
| Authorized penetration test | YES | signed engagement letter |
| Open-source project with a security policy | YES | follow the policy |
| CTF / wargame / deliberately vulnerable target | YES | expected behavior |
| Your own systems | YES | your assets only |
| Internal red team with documented authorization | YES | within that scope |
| Scanning random internet hosts | NO | requires per-target authorization |
| Testing third-party APIs without permission | NO | unauthorized access |
| Accessing/exfiltrating real user data | NO | beyond minimum proof |
| DoS / service degradation | NO | unless explicitly allowed |
| Social engineering / phishing | NO | out of scope for this skill |
| Physical access attacks | NO | out of scope for this skill |

### 33.3 Non-Destruction

Do not modify or delete data you do not own; do not create backdoors,
accounts, or scheduled tasks; do not degrade service for others; do not
exfiltrate real user data beyond minimum proof. Side-effect-prone tests
(emails, created records) use test accounts and are cleaned up after.

### 33.4 Rate Limiting and Courtesy

Respect stated program limits; absent one, default ≤1 request/second per
endpoint; back off on 429; avoid automated scanners unless explicitly
allowed.

### 33.5 Coordinated Disclosure

```
Day 0:  discover; report via the official channel (summary, impact, PoC,
        reproduction steps)
Day 5:  no acknowledgment → follow up via an alternative channel
Day 45: request status update; extend if the vendor is working on a fix
Day 90: public disclosure deadline (per program policy; default 90 days
        with vendor coordination)
```

### 33.6 Handling Real User Data

If testing accidentally exposes real user data: stop further access
immediately; do not store beyond the minimum proof; report the exposure to
the program immediately with what was accessed; redact PII from the
report; treat sensitive categories (credentials, financial, health) as
urgent notifications.

### 33.7 Pre-Disclosure and 0-Day Etiquette

Details of unpatched engine-level bugs (php2shell-class events) circulate
before patches. Do not test live exploitation against third parties; map
exposure analytically (§25.2), use vendor advisories/CISA KEV as
authoritative status, and report through coordinated channels only.

### 33.8 If In Doubt, Stop

When unsure whether an action is authorized, in-scope, or safe: stop and
ask. Never proceed on assumption.

---
