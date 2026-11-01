# Finding Triage Matrix

Every deviation from baseline gets exactly one row here. Classification
determines the dossier class, the priority band, and the Phase-2 hint.

| Finding shape | Dossier class | Priority band | Phase-2 hint |
| --- | --- | --- | --- |
| `backup.zip`, `*.sql`, `*.tar.gz` returning 200 | backup-artifact | 65–85 | contents inventory (bounded), source disclosure |
| `.env`, `config.php`, `settings.json` with live values | config-exposure | 70–90 | secrets policy: report-only, never use |
| `.env.example`, `Dockerfile`, `composer.json` | config-exposure | 45–60 | structure mapping, dependency inventory |
| `/admin`, `/console` → 307/401 | admin-console | 65–80 | boundary bypass hypotheses |
| `/api/*` JSON 200 | api-rest | 55–75 | parameter inventory, auth semantics |
| 30x with operator-influencable Location | redirect-handler | 50–70 | open-redirect differentials |
| `.git/HEAD` 200 | config-exposure | 75–90 | repository exposure — snapshot analysis only, bounded |
| Soft-404 size outlier during calibrated walk | web-app | 40–60 | fetch once, read, classify |
| Framework marker (wp-login, actuator/env) | per marker | 60–80 | version-derived hypotheses (cap priors, see spine §12) |

## Bounded artifact inspection

When a backup or dump is found: record size and content-type; download at
most one bounded sample (a few MB) to an artifact; inventory top-level
names ONLY. "Could download everything" is proven by downloading exactly
one page and stopping (spine §8.2) — and the report says so with the record.

## Secrets found in artifacts

Report-only, always. Values are masked in context; full values live in the
on-disk artifact for the operator. The pipeline never uses, validates, or
exfiltrates a discovered secret (R0's canary doctrine extends here: only
self-injected synthetic data proves a channel).

## Park criteria

Park (backlog=True) when: the finding needs credentials the engagement
does not have; needs a second test account; needs a tool not in the
capability inventory; or priority lands below the current queue's floor.
A parked finding keeps its evidence and its resume note — silent drops are
the sin against R2.
