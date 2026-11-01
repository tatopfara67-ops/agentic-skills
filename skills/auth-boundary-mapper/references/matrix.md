# The Role × Resource Matrix

## Template

Rows: resource type × instance ownership (A-owned, B-owned, nonexistent).
Columns: actions (list, read, update, delete, admin-actions).
Cells: `(actor, expected, observed, records)`.

```
| Resource          | Action | Actor | Expected   | Observed | Records (B/T/C) |
| invoice A-0001    | read   | B     | deny       | 200      | R-101/102/103   |
| invoice B-0007    | read   | B     | allow      | 200      | R-104/—/—       |
| invoice 99999999  | read   | B     | 404-or-deny| 200      | —/—/R-105       |
```

The "expected" column comes from the app's own claims (docs, UI hints,
role names) — when the app claims nothing, write `unspecified` and treat
the cell as a hypothesis, not a violation.

## Verdict grammar

* `granted` — treatment returns the object (2xx + body matches A-owned
  object's shape/content-hash family).
* `denied` — 401/403/404 on treatment.
* `leaky-denial` — denial status but the body/timing leaks existence
  (different error for existing vs nonexistent ids: the CONTROL proves it).
* `unspecified` — no expectation claim; record, park, move on.

`granted` + `unspecified` is a LEAD, not a CONFIRMED violation — programs
reject reports where the "boundary" was never claimed. Say so in the report.

## Differential details that survive triage

* Same request shape everywhere: only the identifier changes between
  baseline/treatment/control. Different shapes measure your bug, not theirs.
* Repeat the granted treatment 3 times (deterministic floor, spine §6) —
  some gates are flaky-by-design (rate-limited second checks, cache races).
* Check the RESPONSE body is the cross-tenant object (hash it against the
  baseline artifact), not a same-tenant echo with a swapped label —
  the classic false positive in IDOR reports.
* For list endpoints, the unit under test is the filter parameter, and the
  control is the unfiltered call; "list everything" claims need the
  bounded one-page proof, not a dump.

## Vertical boundaries

Admin-marked surfaces (307/401 during recon) get the same three-round
treatment with the LOW-privilege account. `granted` on an admin action is
the strongest cell in the matrix — impact synthesis still runs the canary
ladder before any severity word appears in the report.
