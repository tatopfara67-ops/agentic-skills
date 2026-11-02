# bypass-craft.md — the Dalili lineage layer for business-logic-hunter (v2)

Load when a business guard blocks a treatment (admin path, step gate,
role check), when two components disagree about "the same" input, or
when a comparison function is the thing under test.

## 1. Reshape Before Declaring the Wall

The public WAF-bypass grammar (reshaping HTTP requests via the standard
and web-server behavior — the Dalili talk line) applies unchanged to
BUSINESS guards. A blocked treatment gets one reshaping pass before the
hypothesis closes as REFUTED:

| Lever | Example reshape | Why servers differ |
| --- | --- | --- |
| case | `/ADMIN/main.aspx` | guard matches case-sensitively, router doesn't |
| path params | `/admin/;/main.aspx` | the router treats `;params` differently than the guard |
| segment padding | `/admin//main`, `/./admin/main` | normalization order differs per component |
| encoding | `%61dmin`, double-encoded | decode happens at different layers |
| header/verb | `X-Original-URL`, method swap | routing headers honored by the executor, unread by the guard |

One canonical reshape per hypothesis (spine §5, one mechanism); a
CONFIRMED reshape records the EXACT request bytes — the reshape is the
finding, not the fact that some encoding worked somewhere.

## 2. Parser Differential as a Logic Splitter

When front guard and backend executor parse differently, the workflow
has a SEAM — and seams are where business logic breaks. The check
pattern:

1. Map which component enforces the step (workflow-map records say).
2. Send the semantically-equal-but-parsed-differently variant from §1.
3. Read the VERDICT from the executor's response (did the step run?),
   not from the guard's response code.
A seam confirmed here is chain-architect input: guards that disagree
compose with everything downstream.

## 3. Intended-Behavior Inversion

The check that works on step A becomes the bypass when the workflow
applies it at step B. Canonical shapes:

* case/Unicode normalization making two "different" identifiers equal
  at the dedup check, different at the audit log — the dedup passes
  what the audit thought it blocked;
* a limit enforced as `value <= max` on one path and `value < max` on
  the retry path — off-by-one across steps;
* cancel/refund logic applied to a step whose state machine never
  intended it (reorder abuse, spine catalog).

Field rule: for every observed check, ask "inverted or displaced, what
does this check become?" — one hypothesis per inversion, still
self-owned accounts.

## 4. Comparison Functions Are Testable Units

Identity/privilege/limit comparisons are units with inputs: case
folding (does the comparison fold like the DB collation does?), Unicode
normalization forms (NFC vs NFKC across components), type juggling
(`0 == "0"` class — language-specific, pin the runtime as a FACT).
Differential: two operator-owned identifiers that fold together in one
component and stay distinct in the other. The ledger records both
identifiers' bytes verbatim.

## 5. The Restraint Rule

The grammar is combinatorial; the craft is NOT sweeping it. One
canonical differential per seam proves the seam. Firing every encoding
permutation is request-budget slop that buries the ledger and risks the
engagement's rate contract. Two variants max per hypothesis (signal-
smith's law applies), then park.

## 6. The Craft, Stated As Five Field Rules

1. Reshape once, canonically, before closing any blocked hypothesis.
2. Seams are found at the executor's verdict, not the guard's status.
3. Invert every check: displaced, what does it become?
4. Comparison functions are units — record bytes, pin the runtime.
5. Two variants per seam, then park; the ledger stays readable.
