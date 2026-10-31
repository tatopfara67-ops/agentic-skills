# Sloppy Code-Audit Report — Negative Control

This report is an intentional negative control for the auditor. It contains
planted violations of the White-Box Report Contract; the key listing them
lives in README.md, not here. The auditor must reject it.

## Executive Summary

Audited the auth module this afternoon. JACKPOT — found a critical bug in
the JWT handler within minutes, this agent is on fire. The HMAC path is
vulnerable to forged tokens and the whole module might be exploitable
remotely. The JWT decode function is exposed to key-type confusion attacks
(R-101), so this is probably a critical finding.

## Findings

The signing helper at auth/jwt_helper.py:88 uses the configured public key
as the HMAC secret when the token header says HS256. This looks vulnerable
to me. CVE-2024-33663 was fixed upstream so the same pattern here is
definitely exploitable.

### H-001 — Algorithm confusion in the JWT handler

The library might be vulnerable to algorithm confusion where the public key
is used as an HMAC secret. I believe the attack works because the header
controls the algorithm choice. This seems vulnerable in production configs.
The upstream fix landed in 3.4.0.

Closure: CONFIRMED

### H-002 — Session token entropy

Session tokens come from the standard library random module; an attacker
could predict them with enough samples. Should be tested further during the
next sprint.

Closure: INCONCLUSIVE

### H-003 — Padding oracle in the legacy decrypt endpoint

The decrypt endpoint returns different errors for bad padding versus bad
MAC, which seems exploitable as a padding oracle. TODO: confirm with the
team. No runtime test was attempted because the endpoint looked complicated.

## Recommendations

Upgrade the library, rotate the keys, and add a WAF rule. The rest of the
codebase seemed fine after a quick scan.
