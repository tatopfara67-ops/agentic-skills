# Priority Scoring — 0 to 100, computed, never felt

Priority is a number with a stated derivation, produced BEFORE any
hypothesis work, and it is revisable only by appending a note (never by
silently re-scoring). The score ranks the Phase-2 operator rotation order:
the highest-priority class-boundary surfaces get the first hypotheses.

## Base scores by class

| Class band | Base |
| --- | --- |
| admin-console, auth-endpoint, payment-flow, ai-agent-surface | 70 |
| api-rest, api-graphql, api-rpc, upload-endpoint, file-storage, redirect-handler | 60 |
| debug-interface, deprecated-endpoint, backup-artifact, config-exposure | 65 |
| search, job-worker, email-handler, websocket | 50 |
| web-app, static-content, third-party-asset | 40 |

## Adjustments (sum, then clamp to 0–100)

| Signal | Adjustment | Why |
| --- | --- | --- |
| Requires authentication or carries role semantics | +10 | Boundary confusion (IDOR/BOLA) lives here |
| Accepts user-controlled input reflected in responses | +8 | Injection and XSS surface |
| Discovered via a deprecated/commented route, spec diff, or soft signal | +8 | Unloved asset — hygiene decays where nobody looks |
| Unversioned or behind an old version prefix (`/v0`, `/v1` while `/v3` exists) | +5 | Variant-analysis target (Big Sleep shape) |
| Login-gated during recon (307/401) | +5 | The door tells you what is worth guarding |
| Static, no parameters, CDN-served | −10 | Low variance |
| Backup/config artifact with structure only (`.env.example`) | −5 | Inventory value, low direct impact |

## The unloved-asset bonus

A surface is **unloved** when it shows no signal of recent change: not in
the current sitemap, absent from the openapi spec, referenced only by old
JS bundles or comments, or served by an older stack fingerprint than its
siblings. Apply the +8 adjustment and say why in the dossier note. The
highest-yield public bug-bounty pattern is variant analysis on unloved
assets — the same bug shape, fixed in the loved twin, alive in the unloved
one.

## Output contract

The score, its class, and the two strongest adjustment reasons go into the
`note` field of `dossier_add`, e.g.:

```
note="auth-boundary +10, unloved (absent from sitemap) +8"
```

A score without its derivation sentence is slop — the auditor flags notes
that state a priority with no reason tokens.
