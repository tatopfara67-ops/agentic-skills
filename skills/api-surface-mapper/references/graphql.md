# GraphQL Discipline

## Introspection (the single allowed discovery query)

`api_introspect` sends exactly one, depth-limited, read-only query:

```
query { __schema { queryType { name } types { name kind } } }
```

A 200 with `__schema` in the body = introspection enabled (SURFACE
record). Enabled introspection is an inventory gift, not a finding by
itself; disabled introspection does not end inventory work.

## When introspection is disabled

Schema reconstruction continues from evidence, as hypotheses:

* Query/mutation/fragment names in client bundles (js-recon extraction).
* Error-message shape leaks ("Cannot query field X on type Y" names both
  sides — record the exact pair).
* Persisted-query IDs and their client-side call sites.
Each reconstruction candidate cites its source record and is probed once
with a minimal valid-ish query to test existence — bounded, never a
brute-force dictionary of field names.

## Bounded query discipline (Phase 3 preview)

* Depth-limited queries only; no unbounded `__type` recursion.
* One page of any list field, then stop (spine §8.2 bounded scope).
* Mutation testing is Phase 3 work under business-logic-hunter — never
  during inventory.
* Batch-query abuse (packing N operations into one request) is a
  hypothesis to PRE-REGISTER with a rate-limit-impact story, then test
  with a small N, not the maximum the server will accept.

## Mass-assignment watchlist (from spec types)

Types whose input objects accept more fields than the UI sends are
mass-assignment candidates. The inventory records the type name, the
client-sent field set, and the spec's full field set — the DIFF is the
hypothesis, tested only with self-owned test-account data in Phase 3
(auth-boundary-mapper owns the differential).
