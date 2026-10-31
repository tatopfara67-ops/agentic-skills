---
name: aas-catalog
version: 1.0.0
description: >
  Search and install skills on demand from the Agentic Awesome Skills catalog
  (2,884+ SKILL.md playbooks for Claude Code, Codex, Cursor, Gemini CLI).
  Use when the operator asks to find a ready-made skill, browse the skill
  catalog, or install a third-party skill ("cari skill", "cari di katalog",
  "install skill X dari katalog", "aas", "agentic awesome skills", "butuh
  skill untuk <tugas>"). Never bulk-installs; each install is one reviewed
  skill.
license: MIT
metadata:
  author: tatopfara67-ops
  requires: local git clone of github.com/sickn33/agentic-awesome-skills (MIT)
---

# AAS Catalog — on-demand skill search & install

Finds an existing skill in the Agentic Awesome Skills catalog instead of
writing one from scratch. Search, inspect, install exactly one skill at a
time — the catalog is a read-only clone, installs land in `skills/`.

## One-time setup

```bash
git clone --depth 1 https://github.com/sickn33/agentic-awesome-skills.git \
  /home/z/my-project/external-skills/agentic-awesome-skills
```

Path override: set `AAS_CATALOG_DIR` to the clone location. Default:
`/home/z/my-project/external-skills/agentic-awesome-skills`.

## Usage

```bash
python3 skills/aas-catalog/scripts/aas.py search "code review" --risk safe
python3 skills/aas-catalog/scripts/aas.py info <skill-id>
python3 skills/aas-catalog/scripts/aas.py install <skill-id>          # -> skills/<name>
python3 skills/aas-catalog/scripts/aas.py install <skill-id> --dest /tmp/test
python3 skills/aas-catalog/scripts/aas.py categories
```

Search matches name, id and description; filters: `--category`, `--risk`,
`--limit`. Every entry carries a `risk` field — treat it as a triage hint,
not a verdict.

## Hard rules

1. **One skill per install, never bulk.** "Install everything matching X"
   is a refusal: curate instead.
2. **Risk gate.** The script refuses non-`safe` skills without
   `--allow-risky`. That flag means the operator reviewed the skill's
   SKILL.md manually — say so before using it.
3. **Post-install is part of the install.** No skill from this catalog is
   "done" until: the repo validation gate (`scripts/validate_skill.py`) ran
   on it, INDEX.md was regenerated, and its SKILL.md was actually read. The
   script prints these steps; do them.
4. **The catalog stays a clone.** Never vendor its 500+ MB into any repo,
   never edit files inside the clone.
5. **Write beats copy.** If a searched skill almost fits but not quite,
   building a small local skill under the repo's CONTRIBUTING workflow
   beats installing and patching a foreign one.

## Feedback on this skill

Methodology feedback: open an issue in the operator's `agentic-skills`
repository. Upstream catalog issues belong to
github.com/sickn33/agentic-awesome-skills, not here.
