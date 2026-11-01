# activation.md — installing and bootstrapping Skill Mythos

Load at install time or when wiring the arsenal into a new workspace.

## 1. Prerequisites

```bash
pip install "mcp>=1.2.0"        # the FastMCP SDK
python3 arsenal/server.py --selftest   # must list 25 tools
```

## 2. Wiring the MCP server

`.mcp.json` (Claude Code / Cursor), adjusting the path:

```json
{
  "mcpServers": {
    "mythos-arsenal": {
      "command": "python3",
      "args": ["/absolute/path/to/mythos-arsenal/arsenal/server.py"]
    }
  }
}
```

Environment overrides: `MYTHOS_ARSENAL_ROOT` (package root),
`MYTHOS_ARSENAL_SCOPE` (scope.csv path), `MYTHOS_ARSENAL_ENGAGEMENTS`
(engagement state dir), `MYTHOS_ARSENAL_SKILLS` (skills dir — point it
at the repo checkout's skills/ to include the spine and every other
bundle).

## 3. The contract file

Copy `CLAUDE.md` to the workspace root. The MCP server serves tools;
the contract makes the agent use them in discipline. The contract's
session-start sequence begins with `mythos_charter()` — the charter
loads before the skill list, by design.

## 4. First-session bootstrap

1. `mythos_charter()` — articles, bundle map with install status,
   quality gates. If the spine (mythos-bug-hunter) reports missing,
   stop and install it: organs without the spine have no conduct
   layer.
2. `list_skills()` — metadata only.
3. `auth_status()` — scope.csv rows, classes, expiries. An
   authorization table with no rows means no traffic, ever (R0).
4. Load the spine's SKILL.md and its conduct module.
5. Run the self-owned lab once (`lab/target_app.py`) before touching
   any external surface — rehearsal is cheap, and the worked example
   (`examples/worked-engagement/`) shows what a finished engagement
   looks like.

## 5. Validation (before every commit of skills/*)

```bash
python3 scripts/validate_skill.py skills/skill-mythos
python3 -m unittest discover -s arsenal/tests
python3 auditor/audit_report.py examples/worked-engagement/report.md
```

## 6. Upgrading the VRT data file

The classifier resolves against
`references/vrt-taxonomy.json` (the official Bugcrowd taxonomy under
Apache-2.0 — see NOTICE.md). To upgrade:

```bash
curl -o references/vrt-taxonomy.json \
  https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/vulnerability-rating-taxonomy.json
python3 -m unittest arsenal.tests.test_mythos   # mappings re-resolve
```

If a rename upstream breaks a mapping, the test
`test_all_mapped_vrt_ids_resolve_in_shipped_taxonomy` fails loudly —
fix the map in `arsenal/tools/mythos.py`, not the test.

## 7. What "installed" means

A tier-0 install is real when all of this is true: the selftest lists
25 tools including `mythos_charter`, `cvss3_score`, `vrt_classify`;
`mythos_charter()` shows every organ green under its tier; the
auditor passes both shipped examples; and the operator's activation
phrase — "activate Skill Mythos" — triggers the bootstrap sequence
above without further instruction. That last clause is the one the
contract file enforces; MCP cannot, and does not pretend to.
