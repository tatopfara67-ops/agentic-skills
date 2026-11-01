# Wordlist Ladder

Volume is noise. The ladder spends request budget where signal density is
highest, and every rung is bounded by the same cap.

| Rung | When | Contents |
| --- | --- | --- |
| 0 | Always (built-in) | `default.txt` shipped with the arsenal: ~180 high-yield paths — entry doors (login/admin/dashboard), API shapes, config/backup names, framework markers |
| 1 | Base response reveals a framework (wp-, phpmyadmin, actuator markers) | Framework-tuned list assembled in-session from the marker (never blind generic mega-lists) |
| 2 | JS recon or API specs hint at path conventions (e.g. `/api/vN/<resource>`) | Convention-derived list: resource names from the spec × version prefixes seen in evidence |
| 3 | A finding suggests neighborhood density (backup.zip found) | Neighborhood round: siblings of the found name with archive extensions |

## Extension rounds

Run extensions as a separate walk, never multiplied into rung 0 (cap
explodes): `["", ".bak", ".old", ".zip"]` first; `[".tar.gz", ".sql",
".example", ".save"]` only when a signal earned it.

## Budget math, stated in the phase summary

probes = min(len(words) × len(exts), max_requests) + 3 control requests.
If the cap bit into the plan, say so at the exit gate — "walk truncated at
150/312 planned probes" — and park the remainder instead of silently
dropping it.

## When ffuf is available

`arsenal_route` with `-ac` (auto-calibration) mirrors the same discipline
at CLI speed. Its output is still a hypothesis list: every hit re-enters
triage through `http_probe` records before any dossier entry.
