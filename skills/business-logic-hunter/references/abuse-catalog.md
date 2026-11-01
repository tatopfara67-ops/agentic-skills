# Workflow Abuse Catalog

## Workflow-map template (per in-scope flow)

```
Flow: checkout
Steps: 1 browse → 2 cart-add → 3 address → 4 payment-select → 5 confirm → 6 receipt
Server checks observed: price recomputed at 5 (not at 2); coupon validated at 5;
stock check at 2 and 5; state token issued at 4, consumed at 5
Owner records: R-201..R-212 (happy path, operator account)
```

The map's value is the CHECKS column: where the server re-validates, and
where it trusts an earlier step. Abuse shapes target the gaps.

## Abuse shapes (one hypothesis each)

| Shape | Treatment | Control | Typical falsifier |
| --- | --- | --- | --- |
| Sequence skip | call step 5 directly (state token missing) | call step 5 with garbage token | server rejects on missing state |
| Step replay | re-run step 2 after step 5 completed | re-run step 2 before starting | idempotency/replay guard fires |
| Reorder | swap steps 3 and 4 | swap unrelated two steps | invariant check rejects |
| Cross-flow splice | carry flow-1's state token into flow-2 | carry a random token | token scoping holds |
| Parameter resurrection | re-send a parameter from step 2 at step 5 (e.g. unit price) | re-send an unrelated step-2 field | server recomputes, ignores client value |
| Coupon stacking | apply two operator-created coupons | apply one coupon twice | stacking rejected |
| Negative quantity | qty=-1 on self-owned cart | qty=0 | validation floor rejects |
| Decimal/currency confusion | 0.001-unit prices, comma-vs-dot decimals | round normal price | precision normalization holds |
| Overflow-shaped values | large-but-typed-valid numbers (e.g. 2^31-ish quantities on a self-owned order) | large-but-invalid string | server caps or rejects cleanly |

## Interpretation discipline

* A weird RESPONSE is not a finding; a differential DELTA on a self-owned
  order is. Total-changed, state-token-accepted, receipt-issued — these
  are deltas; "server did not complain" is not.
* Sequence-skip CONFIRMED requires the skipped-step server-side check to
  be demonstrably absent, which the control request isolates.
* Report impact in currency-or-state terms on the self-owned order, with
  the canary attestation that no other account's state was touched.
