# cvss-guide.md — constructing and scoring a CVSS 3.1 vector

Load when a finding needs its cvss: line. The instrument is
`cvss3_score(vector)`; the auditor recomputes every vector you write
with the same arithmetic, so write what the tool returns.

## 1. The eight base metrics

| Metric | Values | Question it answers |
| --- | --- | --- |
| AV Attack Vector | N / A / L / P | where must the attacker be: network / adjacent / local / physical |
| AC Attack Complexity | L / H | beyond privileges, does the exploit depend on conditions outside the attacker's control |
| PR Privileges Required | N / L / H | what privileges does the attacker need before the attack |
| UI User Interaction | N / R | must a human user participate |
| S Scope | U / C | does the impact cross a trust boundary (component A compromised, component B harmed) |
| C / I / A | H / L / N | confidentiality / integrity / availability impact on the COMPONENTS IN SCOPE |

Weights (spec tables): AV N .85, A .62, L .55, P .2; AC L .77, H .44;
PR N .85, L .62, H .27 (relaxing to .68 / .5 when Scope is Changed);
UI N .85, R .62; each of C/I/A H .56, L .22, N 0.

## 2. The arithmetic (FIRST spec §7.1 — implemented in arsenal/cvss.py)

```
ISS            = 1 − (1−C)(1−I)(1−A)
Impact         = 6.42·ISS                          (Scope Unchanged)
Impact         = 7.52·(ISS−0.029) − 3.25·(ISS−0.02)^15   (Scope Changed)
Exploitability = 8.22·AV·AC·PR·UI
Base           = Roundup(min(Impact + Exploitability, 10))          (S:U)
Base           = Roundup(min(1.08·(Impact + Exploitability), 10))   (S:C)
Base           = 0 when Impact ≤ 0
```

Bands: None 0.0 · Low 0.1–3.9 · Medium 4.0–6.9 · High 7.0–8.9 ·
Critical 9.0–10.0.

## 3. Worked example (the lab's H-001 shape)

Unauthenticated read of a diagnostic banner — internal state exposed,
nothing else:

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N
ISS            = 1 − (1−.22) = 0.22
Impact         = 6.42 × 0.22 = 1.4124
Exploitability = 8.22 × .85 × .77 × .85 × .85 = 3.8870
Base           = Roundup(5.2994) = 5.3   → Medium
```

Reference scores to sanity-check your intuition (all reproducible via
`cvss3_score`):

| Vector pattern | Score |
| --- | --- |
| AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H | 9.8 |
| AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H | 10.0 |
| AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H | 9.9 |
| AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N | 8.6 |
| AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N | 7.5 |
| AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N | 6.5 |
| AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N | 6.1 |
| AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N | 5.3 |
| AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N | 0.0 |

## 4. Construction discipline (what the cvss: line is judged on)

1. **Score the OBSERVED path, not the imagined one.** You proved an
   unauthenticated read of diagnostic state — that is C:L, I:N, A:N.
   You did not prove RCE; writing C:H/I:H/A:H is a false positive
   wearing a vector.
2. **PR follows the attack's front door** — the privileges needed
   BEFORE the exploit, not the victim's privileges.
3. **S changes only when the impact crosses a component boundary**
   (SSRF into an internal service, XSS hijacking the browser beyond
   the vulnerable page). Same-app impact is S:U.
4. **The parenthetical argues the impact metrics** — the cvss: line
   states why C/I/A are what they are, citing the records that showed
   it. The auditor recomputes the arithmetic; the argument is what
   triage reads.
5. **Temporal/environmental metrics stay out** — the arsenal ships
   base vectors describing the observed path. ESSL/ARMIL/CRE changes
   belong to the analyst, with their own justification.

## 5. About CVSS v4.0

CVSS v4.0 exists and adds threat/environmental detail; this bundle
scores v3.1 because (a) bug-bounty triage desks overwhelmingly still
speak v3.1, and (b) v3.1 base vectors are complete and defensible for
the observed-path doctrine. When a program asks for v4.0, score it on
the program's own calculator and say which system you used — never
silently mix the two in one report.
