"""surface-cartographer backend — the organized attack-surface map.

The dossier is the deliverable the whole Tier-1 pipeline aims at:
  * dossier_add    : register one surface WITH evidence (ledger R-NNN refs
                     are validated — a surface without a record does not
                     exist, spine §2 made mechanical)
  * dossier_render : emit dossier.md — asset graph tree + priority-sorted
                     surface table + backlog + hypothesis-coverage warning
  * dossier_summary: compact in-context view

The 21-class surface taxonomy is enforced HERE (spelling = mechanical
check), so every engagement speaks the same class language and the Phase 2
hypothesis sweep can rotate operators across classes without translation.
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone

from .. import ledger, paths
from ..scope_gate import load_scope

TAXONOMY = (
    "static-content", "web-app", "api-rest", "api-graphql", "api-rpc",
    "admin-console", "auth-endpoint", "file-storage", "redirect-handler",
    "upload-endpoint", "websocket", "job-worker", "email-handler",
    "payment-flow", "search", "debug-interface", "deprecated-endpoint",
    "backup-artifact", "config-exposure", "third-party-asset",
    "ai-agent-surface",
)

_RID_LIST_RE = re.compile(r"^R-\d{3,}$")


def _state_path(program: str) -> str:
    return os.path.join(paths.program_dir(program), "dossier.json")


def _load(program: str) -> dict:
    path = _state_path(program)
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    return {"surfaces": [], "meta": {"created": None}}


def _save(program: str, state: dict) -> None:
    os.makedirs(os.path.dirname(_state_path(program)), exist_ok=True)
    with open(_state_path(program), "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=1)


def dossier_add(program: str, url: str, klass: str, evidence: str,
                reachability: str = "reachable", priority: int = 50,
                note: str = "", backlog: bool = False) -> dict:
    """Register a surface. `evidence` = comma-separated R-NNN ids that MUST
    exist in the engagement ledger — the no-slop law applied to cartography."""
    if klass not in TAXONOMY:
        raise ValueError("class %r not in the 21-class taxonomy: %s"
                         % (klass, ", ".join(TAXONOMY)))
    if not 0 <= int(priority) <= 100:
        raise ValueError("priority must be 0..100")
    rids = [r.strip() for r in evidence.split(",") if r.strip()]
    if not rids:
        raise ValueError("a surface without evidence records is not a surface — "
                         "cite at least one R-NNN (no-slop law, spine §2)")
    missing = [r for r in rids if not _RID_LIST_RE.match(r) or not ledger.exists(program, r)]
    if missing:
        raise ValueError("evidence cites records absent from the ledger: %s — "
                         "if it is not in the ledger, it did not happen" % missing)
    state = _load(program)
    if any(s["url"] == url for s in state["surfaces"]):
        raise ValueError("surface %s already registered — update it via the "
                         "backlog flag or add evidence, never duplicate" % url)
    sid = "S-%03d" % (len(state["surfaces"]) + 1)
    if state["meta"].get("created") is None:
        state["meta"]["created"] = datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
    state["surfaces"].append({
        "id": sid, "url": url, "class": klass, "evidence": rids,
        "reachability": reachability, "priority": int(priority),
        "note": note, "backlog": bool(backlog)})
    _save(program, state)
    return {"id": sid, "url": url, "class": klass, "evidence": rids,
            "priority": int(priority), "backlog": bool(backlog)}


def _host_of(url: str) -> str:
    m = re.match(r"^[a-z]+://([^/]+)", url)
    return m.group(1) if m else url


def _scope_artifacts(program: str, hosts: list[str]) -> list[str]:
    artifacts = []
    for row in load_scope():
        for host in hosts:
            base = row.target.split("/")[0].split(":")[0].lstrip("*.")
            if base and (host == base or host.endswith("." + base)
                         or base in host):
                if row.auth_artifact and row.auth_artifact not in artifacts:
                    artifacts.append(row.auth_artifact)
                break
    return artifacts


def dossier_render(program: str) -> dict:
    """Render dossier.md — the attack-surface map, from records only."""
    state = _load(program)
    surfaces = state["surfaces"]
    active = [s for s in surfaces if not s["backlog"]]
    backlog = [s for s in surfaces if s["backlog"]]
    ranked = sorted(active, key=lambda s: -s["priority"])
    hosts = sorted({_host_of(s["url"]) for s in surfaces})
    artifacts = _scope_artifacts(program, hosts)

    lines = []
    lines.append("# Attack-Surface Dossier — %s" % program)
    lines.append("")
    lines.append("Generated %s from ledger records only; surfaces without "
                 "evidence are structurally impossible (no-slop law)."
                 % datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    lines.append("")
    lines.append("- Surfaces registered: %d (active %d, backlog %d)"
                 % (len(surfaces), len(active), len(backlog)))
    lines.append("- Authorization artifacts: %s"
                 % ("; ".join(artifacts) if artifacts else "none matched — verify scope.csv"))
    lines.append("")
    lines.append("## Asset graph")
    lines.append("")
    by_host: dict[str, list] = {}
    for s in surfaces:
        by_host.setdefault(_host_of(s["url"]), []).append(s)
    for host in hosts:
        lines.append("**%s**" % host)
        lines.append("")
        for s in sorted(by_host[host], key=lambda x: -x["priority"]):
            mark = " (backlog)" if s["backlog"] else ""
            lines.append("- `%s` %s — %s, priority %d, evidence %s%s"
                         % (s["url"], s["id"], s["class"], s["priority"],
                            ",".join(s["evidence"]), mark))
        lines.append("")
    lines.append("## Priority queue")
    lines.append("")
    lines.append("| ID | Surface | Class | Reachability | Priority | Evidence | Note |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for s in ranked:
        lines.append("| %s | %s | %s | %s | %d | %s | %s |"
                     % (s["id"], s["url"], s["class"], s["reachability"],
                        s["priority"], ",".join(s["evidence"]),
                        s["note"].replace("|", "/")))
    if backlog:
        lines.append("")
        lines.append("## Backlog (parked discoveries — R1)")
        lines.append("")
        for s in sorted(backlog, key=lambda x: -x["priority"]):
            lines.append("- `%s` %s — %s, evidence %s — %s"
                         % (s["url"], s["id"], s["class"],
                            ",".join(s["evidence"]), s["note"] or "no note"))
    lines.append("")
    lines.append("## Phase 2 gate")
    lines.append("")
    lines.append("Every active surface above needs at least one pre-registered "
                 "hypothesis (H-record) or an explicit why-not note before "
                 "Phase 3 testing opens — no surface is left hypothesis-less.")
    lines.append("")
    out_path = os.path.join(paths.program_dir(program), "dossier.md")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return {"ok": True, "path": out_path, "surfaces": len(surfaces),
            "active": len(active), "backlog": len(backlog),
            "hosts": hosts}


def dossier_summary(program: str) -> list[dict]:
    state = _load(program)
    return [{"id": s["id"], "url": s["url"], "class": s["class"],
             "priority": s["priority"], "backlog": s["backlog"]}
            for s in sorted(state["surfaces"], key=lambda x: -x["priority"])]
