# Contributing Skills

This repo builds skills under one house discipline. Read this before creating or changing a skill here.

## House rules

1. **Evidence-first.** A claim ships only with an artifact behind it (README → Doctrine).
2. **Minimal but complete.** Ship the smallest skill that fully covers the job. If a section doesn't earn its place, it goes; if callers, examples, or the auditor a change breaks need updating, they ship in the same change. Bloat is a bug.
3. **Original work only.** This repository contains original work — nothing is vendored. External material (tools, catalogs, references) is called at runtime or cloned outside the repo, never committed. If a dependency must land here, write an in-house implementation under this workflow instead.

## Workflow

1. **Observe before authoring.** Is the friction you're fixing real (seen at least twice) or imagined? A skill for an imagined problem is bloat. Log the pattern first in your session/observation notes.
2. **Draft with required frontmatter.** Every skill ships with `name`, `version`, `description` (including trigger phrases — when should the skill activate), `license`, `author` (top level or under `metadata:`). Without triggers, a skill never fires; without license/author, it can't leave this repo.
3. **Progressive disclosure.** `SKILL.md` is the routing layer: what the skill does, when to use it, hard rules. Depth lives in `references/` loaded on demand. The core file is measured by the gate, not guessed.
4. **Rules need enforcement.** If the skill has rules, it needs a mechanism that checks output against them (an auditor script, a PASS/FAIL gate, a checklist the agent must run before delivery). A rule nobody verifies is decoration.
5. **Timelessness.** Shared skills must not capture current state (dates, session tokens, "today"). State goes in the payload slot or the operator's message, never the skill body.
6. **Validation gate — must pass before commit:**

   ```bash
   python3 scripts/validate_skill.py skills/<skill-name>
   ```

   Exit non-zero or a FAIL line = fix the skill, not the gate. `--all` checks every bundle under `skills/`.

7. **Commit message format:** `feat|fix|docs(skill-name): <what and why>`. One skill change per commit when practical.

## Versioning

- Patch: clarifications, reference fixes, no behavior change.
- Minor: new references, new triggers, relaxed/added non-breaking rules.
- Major: changed doctrine, renamed skill, incompatible activation.
