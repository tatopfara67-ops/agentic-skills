# Sloppy Report Fixture — Negative Control

> **This file is deliberately bad.** It exists so you can watch
> `scripts/audit_report.py` reject it. Every line below violates the Report
> Contract (SKILL.md §13). Do not learn from it — feed it to the auditor.

# Security Test Report — demo target (fixture)

## Findings

JACKPOT!!! I found a critical vulnerability in the login form!
The /api/users endpoint might be vulnerable to SQL injection — probably worth a look.
Looks like there is an exposed /admin panel somewhere. BREAKTHROUGH!
The server could be running an old Apache version, I think.
TODO: verify the XSS in the search box later.
Also the JWT tokens maybe have a weak algorithm. Should be tested further.
