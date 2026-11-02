# Reference — Sources (lineage verification)

> Part of **mobile-hunter v1.0.0** (package architecture).
> **Load when:** the lineage claim needs its citation; the
> attribution boundary (what is Miller's public record, what is this
> bundle's doctrine) needs restating. Authoritative rules live in
> [`../SKILL.md`](../SKILL.md) — **SKILL.md wins** on any conflict.

---

## 1. The lineage, verified

**Charlie Miller.** Public record consulted: the Wikipedia article
"Charlie Miller (security researcher)" — five years at the National
Security Agency; Pwn2Own 2008 winner (the MacBook Air, $10,000) and
2009 winner (Safari, $5,000); the 2009 SMS-processing vulnerability
demonstrated **with Collin Mulliner** that allowed complete compromise
of the iPhone; the 2011 *Instastock* proof-of-concept — an
App-Store-approved app that downloaded unapproved logic at runtime —
after which Apple expelled his developer account; the first remote car
exploit lineage (Jeep, with Chris Valasek, 2015). *iOS Hacker's
Handbook* (Miller, Dai Zovi, Portnoy, Weinstein — Wiley, 2012):
catalog records verified (Wiley, Google Books). What is distilled here
is the DOCTRINE — the shipped binary is the attack surface, store
review is an attacker-effort hypothesis, client protections are effort
walls — re-implemented as this organ's decision logic. Nothing of
Miller's is vendored; the mobile teardown ladder (SKILL.md §4,
mobile-method.md) is this bundle's own contribution.

**Collin Mulliner.** Verified as the co-demonstrator of the 2009
iPhone SMS compromise (the same Wikipedia record); his telephony/SMS
research direction is the reason this organ's surface inventory
includes the platform's inter-app and message channels rather than
stopping at HTTP.

## 2. What the lineage is NOT

* Not "Miller endorses this bundle" — he has never heard of it. The
  lineage entry records what his public work teaches, nothing more.
* Not iOS-only. The 2012 handbook's discipline (teardown before
  exploitation) is platform-neutral; this organ applies it to Android
  and iOS alike.
* Not an exploit library. No Miller/Mulliner exploit, code, or
  unpublished technique appears here; every technical step in
  mobile-method.md is generic platform knowledge organized by this
  bundle's evidence law.

## 3. The platform knowledge base

The mobile-attack-surface anatomy (manifest layer, exported
components, deep-link schemes, ATS exceptions, WebView bridges,
certificate pinning as client code) is public platform documentation
knowledge: the Android manifest and iOS Info.plist specifications,
both vendors' security guidance, and the standard bug-bounty mobile
categories in the Bugcrowd VRT taxonomy (shipped with skill-mythos as
`references/vrt-taxonomy.json`, Apache-2.0). No vendor documentation
is redistributed; the VRT is carried under its license with
attribution (see skill-mythos NOTICE.md).

## 4. Verification record

| Claim | Source | Status |
| --- | --- | --- |
| Miller: 5 years NSA | Wikipedia bio | verified |
| Pwn2Own 2008 (MacBook Air), 2009 (Safari) | Wikipedia bio | verified |
| 2009 iPhone SMS compromise with Mulliner | Wikipedia bio | verified |
| 2011 Instastock / App Store expulsion | Wikipedia bio | verified |
| 2015 Jeep remote exploit (with Valasek) | Wikipedia bio | verified |
| *iOS Hacker's Handbook* authorship + 2012 Wiley | Wiley catalog, Google Books | verified |
| Mulliner: SMS/telephony research direction | co-demonstration record above | verified |
