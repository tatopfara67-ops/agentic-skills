#!/usr/bin/env python3
"""mythos-arsenal MCP server — the L4 execution hand, scope-gated.

Run (stdio transport):
    python3 arsenal/server.py

Wire into Claude Code / Cursor via .mcp.json (see README.md §Install).

Tool groups:
  loader     list_skills, get_skill, get_skill_reference   (progressive
             disclosure — name+description first, bodies on demand)
  governance scope_check, auth_status                      (R0/L1)
  evidence   ledger_append, ledger_summary, ledger_read,
             ledger_merge                                   (L5)
  passive    ct_subdomains, dns_resolve                    (L2, active=False)
  active     http_probe, content_discover, api_introspect,
             js_analyze                                     (L2, active=True)
  cartograph dossier_add, dossier_render, dossier_summary  (organized map)
  brain      sbb_declare, sbb_decide, sbb_apply            (adversary-tracker
             organ: the Shimomura Binary Brain — event-triggered hunts on
             assets you are authorized to defend)
  charter    mythos_charter, mythos_lineages, doctrine_forge  (skill-mythos
             master module: articles, bundle map, quality gates; the
             assimilated-lineage registry with corrections on record; A13
             prompt escalation — any operator request forged into an
             explicit doctrine order)
  report     cvss3_score, vrt_classify                      (triage-grade
             classification: CVSS 3.1 base score, Bugcrowd VRT + P-rating
             + HackerOne crosswalk, from the shipped official taxonomy)
  arsenal    arsenal_route                                 (L4 CLI routing)
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:  # official MCP SDK 1.x — FastMCP lives at mcp.server.fastmcp.
    # The local package is `arsenal`, deliberately NOT named `mcp`, so this
    # import always resolves to the official SDK, never to a sibling dir.
    from mcp.server.fastmcp import FastMCP  # noqa: E402
except ModuleNotFoundError:  # mcp SDK 2.x reduced mcp.server.fastmcp to a
    # raising stub — fall back to the standalone fastmcp package (2/3/4.x),
    # which keeps the FastMCP/run()/tool()/list_tools() surface identical.
    from fastmcp import FastMCP  # noqa: E402

from arsenal.scope_gate import check_target, load_scope  # noqa: E402
from arsenal import ledger, paths, sbb as _sbb  # noqa: E402
from arsenal.tools import arsenal_route as _route  # noqa: E402
from arsenal.tools import dossier as _dossier  # noqa: E402
from arsenal.tools import jsrecon as _jsrecon  # noqa: E402
from arsenal.tools import mythos as _mythos  # noqa: E402
from arsenal.tools import passive as _passive  # noqa: E402
from arsenal.tools import probe as _probe  # noqa: E402

mcp = FastMCP("mythos-arsenal")

_BUNDLE_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
_FM_LINE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
_FM_BLOCK = (">", "|", ">-", "|-", ">+", "|+")


def _norm_program(program: str) -> str:
    return (program or "").strip() or "default"


def _parse_frontmatter(text: str) -> dict:
    fm: dict = {}
    if not text.startswith("---"):
        return fm
    lines = text.splitlines()
    i = 1
    while i < len(lines):
        line = lines[i]
        if line.strip() == "---":
            break
        m = _FM_LINE.match(line)
        if m and not line[:1].isspace():
            value = m.group(2).strip()
            if value in _FM_BLOCK:
                parts = []
                i += 1
                while (i < len(lines) and lines[i].strip() != "---"
                       and (not lines[i].strip() or lines[i][:1].isspace())):
                    if lines[i].strip():
                        parts.append(lines[i].strip())
                    i += 1
                fm[m.group(1)] = " ".join(p for p in parts if p)
                continue
            fm[m.group(1)] = value
        i += 1
    return fm


def _bundle_dir(name: str) -> str:
    if not _BUNDLE_RE.match(name or ""):
        raise ValueError("invalid skill name %r" % name)
    path = os.path.join(paths.skills_dir(), name)
    if not os.path.isdir(path):
        raise ValueError("skill %r not found under %s" % (name, paths.skills_dir()))
    return path


# ---------------------------------------------------------------- loader

@mcp.tool()
def list_skills() -> list[dict]:
    """Inventory of installed skills: name, version, description.

    Metadata only — bodies are loaded on demand via get_skill. This is the
    progressive-discipline contract: the routing layer stays cheap."""
    out = []
    root = paths.skills_dir()
    if not os.path.isdir(root):
        return out
    for entry in sorted(os.listdir(root)):
        skill_md = os.path.join(root, entry, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue
        with open(skill_md, encoding="utf-8", errors="replace") as fh:
            fm = _parse_frontmatter(fh.read(4096))
        out.append({"name": fm.get("name", entry),
                    "version": fm.get("version", ""),
                    "description": (fm.get("description", "") or "")[:240]})
    return out


@mcp.tool()
def get_skill(name: str) -> str:
    """Load the full SKILL.md of one skill (the routing layer, on demand)."""
    with open(os.path.join(_bundle_dir(name), "SKILL.md"),
              encoding="utf-8", errors="replace") as fh:
        return fh.read()


@mcp.tool()
def get_skill_reference(name: str, ref_path: str) -> str:
    """Load one reference module of a skill, path-guarded to its bundle.

    Example: get_skill_reference("subdomain-hunter", "references/sources.md")"""
    bundle = _bundle_dir(name)
    candidate = os.path.normpath(os.path.join(bundle, ref_path))
    if not candidate.startswith(os.path.abspath(bundle) + os.sep):
        raise ValueError("path escapes the skill bundle")
    if not os.path.isfile(candidate) or os.path.getsize(candidate) > 262144:
        raise ValueError("reference not found or too large: %s" % ref_path)
    with open(candidate, encoding="utf-8", errors="replace") as fh:
        return fh.read()


# ------------------------------------------------------------ governance

@mcp.tool()
def scope_check(target: str, active: bool = True) -> dict:
    """Would this target pass the authorization gate? Sends nothing.

    active=True simulates an active request (needs class in_scope);
    active=False simulates passive sources (recon_only suffices)."""
    return check_target(target, active=active).as_dict()


@mcp.tool()
def auth_status() -> dict:
    """Authorization posture: every scope.csv row, plus counts by class."""
    rows = load_scope()
    by_class = {}
    for row in rows:
        by_class[row.klass] = by_class.get(row.klass, 0) + 1
    return {
        "rows": [{"target": r.target, "class": r.klass,
                  "auth_artifact": r.auth_artifact or "MISSING",
                  "expires": r.expires or "-"} for r in rows],
        "counts": by_class,
        "policy": "deny-by-default; active tools require in_scope; "
                  "every row must cite an auth artifact",
    }


# -------------------------------------------------------------- evidence

@mcp.tool()
def ledger_append(program: str, tool: str, action: str, result: str,
                  size: str = "", tag: str = "FACT", note: str = "") -> str:
    """Append one observation record. Returns its R-NNN id.

    Tags: FACT, SURFACE, EXPERIMENT, CONTROL, CANARY, PARK, AUTH,
    REFUSED, MISTAKE. Append-only: history is never edited."""
    return ledger.append(_norm_program(program), tool, action, result,
                         size, tag, note)


@mcp.tool()
def ledger_summary(program: str, limit: int = 0) -> list[dict]:
    """Compact ledger view: record ids + one-line gists (bodies stay on disk)."""
    return ledger.summary(_norm_program(program), limit)


@mcp.tool()
def ledger_read(program: str, rid: str) -> str:
    """Re-read one full record from disk, exactly when needed."""
    return ledger.read(_norm_program(program), rid)


@mcp.tool()
def ledger_merge(program: str) -> int:
    """Fold append.md into records.md. Call at phase boundaries."""
    return ledger.merge(_norm_program(program))


# --------------------------------------------------------------- passive

@mcp.tool()
def ct_subdomains(program: str, domain: str) -> dict:
    """Passive subdomain names from crt.sh certificate transparency.

    Reads a public database; the target itself is never contacted. Graceful
    offline: returns ok=False instead of failing."""
    return _passive.ct_subdomains(_norm_program(program), domain)


@mcp.tool()
def dns_resolve(program: str, host: str) -> dict:
    """Resolve A/AAAA (stdlib) + CNAME/MX (if dnspython present). Passive."""
    return _passive.dns_resolve(_norm_program(program), host)


# ---------------------------------------------------------------- active

@mcp.tool()
def http_probe(program: str, url: str, method: str = "GET",
               headers: dict | None = None, body: str | None = None,
               tag: str = "FACT", note: str = "") -> dict:
    """One scope-gated request, one ledger record, body saved as artifact.

    Redirects are NOT followed — a 3xx + Location IS the observation. The
    response body never enters context (spine §3): hash + artifact path only."""
    return _probe.http_probe(_norm_program(program), url, method=method,
                             headers=headers, body=body, tag=tag, note=note)


@mcp.tool()
def content_discover(program: str, base_url: str, wordlist: str = "default",
                     extensions: list[str] | None = None,
                     max_requests: int = 150, rate_per_s: float = 8.0) -> dict:
    """Calibrated content discovery: control requests first, then a
    rate-courteous wordlist walk. Reports baseline deviations only."""
    return _probe.content_discover(_norm_program(program), base_url,
                                   wordlist=wordlist, extensions=extensions,
                                   max_requests=max_requests,
                                   rate_per_s=rate_per_s)


@mcp.tool()
def api_introspect(program: str, base_url: str) -> dict:
    """Bounded sweep for API docs & introspection (openapi/swagger/graphql).
    Read-only queries; spec bodies saved as artifacts with paths extracted."""
    return _probe.api_introspect(_norm_program(program), base_url)


@mcp.tool()
def js_analyze(program: str, url: str) -> dict:
    """Fetch one JS asset, analyze locally: endpoints, commented-out routes,
    secret HINTS (masked in context, full values only in the on-disk
    artifact), sourcemap references. One request total."""
    return _jsrecon.js_analyze(_norm_program(program), url)


# ----------------------------------------------------------- cartography

@mcp.tool()
def dossier_add(program: str, url: str, klass: str, evidence: str,
                reachability: str = "reachable", priority: int = 50,
                note: str = "", backlog: bool = False) -> dict:
    """Register one attack-surface entry. Evidence must cite existing R-NNN
    ledger records — a surface without records is structurally impossible.
    Class must be one of the 21-class taxonomy (see surface-cartographer)."""
    return _dossier.dossier_add(_norm_program(program), url, klass,
                                evidence, reachability, priority, note, backlog)


@mcp.tool()
def dossier_render(program: str) -> dict:
    """Render dossier.md: asset graph, priority queue, backlog, Phase-2 gate."""
    return _dossier.dossier_render(_norm_program(program))


@mcp.tool()
def dossier_summary(program: str) -> list[dict]:
    """Compact dossier view for context: id, url, class, priority."""
    return _dossier.dossier_summary(_norm_program(program))


# ------------------------------------------------------------------ brain

@mcp.tool()
def sbb_declare(program: str, case: str, trigger: str,
                hypotheses: list[str], tests: list[dict]) -> dict:
    """Open (or extend) a Binary Brain hunt: hypotheses + discriminating tests.

    Fires on signal, not curiosity — the trigger is the anomalous observation.
    The engine inserts the null hypothesis (authorized/benign activity) for
    you; do not include your own. Each test: {label, channel, tip_off,
    kills_one: [labels], kills_zero: [labels]} — hypotheses unlisted on a
    side survive that outcome. Tests must span >= 2 channels or CONFIRMED
    is unreachable (Rule T)."""
    return _sbb.declare(_norm_program(program), case, trigger,
                        hypotheses, tests)


@mcp.tool()
def sbb_decide(program: str) -> dict:
    """One Binary Brain step: four registers + the max-information-gain test.

    The chosen test is pre-registered in the ledger BEFORE any outcome
    exists (EXPERIMENT record) — partitions frozen, halving provable.
    Tip-off tests are gated while passive eliminators remain (Rule P)."""
    return _sbb.decide(_norm_program(program))


@mcp.tool()
def sbb_apply(program: str, test_id: str, outcome: int,
              note: str = "") -> dict:
    """Apply one observed binary outcome to its pre-registered test.

    Mechanical refusals: tip-off while passive tests still eliminate
    (Rule P); zero-capability tests while the space is plural (Rule H).
    A singleton survivor is CONFIRMED only through two independent
    channels (Rule T — reverse double triangulation)."""
    return _sbb.apply(_norm_program(program), test_id, outcome, note)


# ---------------------------------------------------------------- arsenal

@mcp.tool()
def arsenal_route(program: str, tool: str, target: str, args: str = "") -> dict:
    """Governed execution of an installed recon CLI (subfinder/httpx/ffuf/
    nmap/nuclei/sqlmap...). Allowlist + flag blacklist + scope gate + ledger.
    sqlmap runs only as a differential oracle (--batch mandatory)."""
    return _route.arsenal_route(_norm_program(program), tool, target, args)


# ---------------------------------------------------------------- charter

@mcp.tool()
def mythos_charter() -> dict:
    """The Skill Mythos activation payload, in one call.

    Thirteen charter articles, the bundle map with per-skill install status,
    and the quality gates every report must pass (differential triad,
    reproducibility, CVSS 3.1 + Bugcrowd VRT classification). Call at
    session start — before list_skills — or whenever the operator says
    'activate Skill Mythos' / 'aktifkan Skill Mythos'."""
    return _mythos.mythos_charter()


@mcp.tool()
def mythos_lineages() -> dict:
    """The assimilated-lineage registry (doctrine A3, verbatim).

    Every organ distilled from a named public figure or team — Shimomura
    (Binary Brain), Fyodor (scan economy), HD Moore (module composition),
    Tomnomnom (Unix pipelines), lcamtuf (feedback search), ProjectDiscovery
    (template scanning), Searle + Mantis/PhonePe (manual-to-orchestrated
    automation), and the legend tier — Orange Tsai (chaining), James
    Kettle (protocol asymmetry), George Hotz (deep teardown), Adrian
    Lamo (the silent infiltrator), Frans Rosen (IDOR methodology, folded
    into auth-boundary-mapper v2), John Draper (signal craft), Kevin
    Mitnick (trust-graph context deception) — with what was distilled,
    which sources were actually consulted, and attribution corrections
    kept on record. The registry IS the legitimate-assimilation
    compliance artifact."""
    return _mythos.mythos_lineages()


@mcp.tool()
def doctrine_forge(request: str, context: str = "") -> dict:
    """Prompt escalation (charter A13): expand ANY operator instruction —
    however terse or informal, in any language — into the professional
    doctrine order the agent will actually execute.

    'tolong lanjutkan pekerjaan bug bounty yang tertunda' becomes the
    resume order (re-ground state, PARK record, phase routing); 'get me
    at least 3 high-medium bugs, no scanner' becomes the full legend
    hunting order — Orange Tsai's chaining + Kettle's protocol
    manipulation + Lamo's stealth misconfig principle + Rosen's IDOR
    discipline + Mitnick's trust audit + Draper's signal craft + Hotz's
    teardown — with the quality gates and quota discipline attached
    (the quota is an effort budget, never a severity mandate). Always
    call this BEFORE acting on an operator instruction; execute the
    expanded order, not the bare words."""
    return _mythos.doctrine_forge(request, context)


# ---------------------------------------------------------------- report

@mcp.tool()
def cvss3_score(vector: str) -> dict:
    """Spec-exact CVSS v3.1 base score from a base vector.

    Feed the vector that describes the OBSERVED attack path (AV/AC/PR/UI/
    S/C/I/A). Returns score, severity band, ISS / Impact / Exploitability,
    parsed metrics, and the canonical vector. Same arithmetic the report
    auditor uses to recheck the cvss: line — write what this returns."""
    return _mythos.cvss3_score(vector)


@mcp.tool()
def vrt_classify(finding_class: str, authenticated: bool = False,
                 user_interaction: bool = False, scope_changed: bool = False,
                 internal: bool = False, sensitive: bool = True,
                 admin: bool = False, self_only: bool = False) -> dict:
    """Classify a finding class into Bugcrowd VRT (P1-P5) + HackerOne
    severity + a CVSS 3.1 template for the observed context.

    Pass the flags you OBSERVED: authenticated, user_interaction,
    scope_changed, internal, sensitive, admin, self_only. Resolution runs
    against the shipped official taxonomy (skills/skill-mythos/references/
    vrt-taxonomy.json); the live bugcrowd.com/vrt stays the submission-time
    authority."""
    return _mythos.vrt_classify(finding_class, authenticated,
                                user_interaction, scope_changed, internal,
                                sensitive, admin, self_only)


def _selftest() -> int:
    """Import-path sanity: all tool modules and the FastMCP registry."""
    try:
        import asyncio

        async def _collect():
            tools = await mcp.list_tools()
            return sorted(t.name for t in tools)
        names = asyncio.run(_collect())
        print("registered MCP tools (%d): %s" % (len(names), ", ".join(names)))
    except Exception as exc:  # selftest must never crash the import path
        print("selftest introspection failed: %s" % exc)
        return 1
    print("mythos-arsenal server import OK")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    mcp.run()
