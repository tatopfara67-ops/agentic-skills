# Secrets Policy — Report-Only, Always

## The rule

Secret-shaped strings discovered in bundles, sourcemaps, or artifacts are
**triage hints, not verdicts, and never ammunition**:

1. **Masked in context.** The tool returns the first characters plus a
   length, never the full value. Full values exist only in on-disk
   artifacts under the operator's control.
2. **Never used.** The pipeline does not validate, redeem, sign, or
   transact with a discovered secret — not even "just to check". Using a
   leaked credential against a system is unauthorized access territory that
   a bug-bounty scope almost never covers, and our canary doctrine covers
   self-injected data only.
3. **Never transmitted.** Secret values are not echoed into requests,
   notes, or reports. The report says: kind, location (file + offset),
   masked head, and the artifact path where the operator can verify.

## Why this is also good methodology

* A hint's VALUE is irrelevant to the finding; the finding is that the
  secret's KIND is exposed at that LOCATION. The mask loses nothing that
  the report needs.
* Refusing to use secrets keeps the engagement inside the authorization
  envelope no matter how the scope dispute resolves later — the strongest
  legal position is the one where the accusation "you used it" is
  physically impossible.
* False positives are common (test keys, canary strings, tutorial keys).
  The operator verifies against the artifact; the pipeline does not burn
  credibility on guesses.

## Report syntax (auditor-checked)

Any CONFIRMED exposure finding cites: the discovery record (R-NNN), the
masked head, the artifact path, and a canary-style attestation that the
value was never used. A report that pastes a full secret value fails the
audit — mechanically, because the auditor greps for the pattern shapes the
tool is able to detect and cross-checks them against masks.
