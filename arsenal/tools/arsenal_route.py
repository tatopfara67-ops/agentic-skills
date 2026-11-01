"""arsenal_route — governed execution of locally-installed recon CLIs.

This is the L4 hook from the Mythos architecture: when the environment has
Kali-style tools (subfinder, httpx, ffuf, nmap, nuclei, sqlmap...), route
to them instead of reimplementing them. When it does not, say so and point
at the fallback ladder — never pretend a tool ran.

Governance (mechanical, not stylistic):
  * allowlist  : only the named tools execute
  * blacklist  : destructive/intrusive flag tokens are refused outright —
                 --dump/--os-shell/--script style flags belong to manual
                 operator sessions, not to an agent loop
  * scope gate : active=True — the target must be in_scope BEFORE exec
  * ledger     : exit code + output head recorded for every execution
  * timeout    : hard 180s ceiling; partial output is still evidence
"""
from __future__ import annotations

import os
import shutil
import subprocess

from .. import ledger
from . import util

ALLOWED_TOOLS = (
    "subfinder", "amass", "httpx", "ffuf", "gobuster", "massdns",
    "nmap", "nuclei", "sqlmap", "dig",
)

_BLOCKED_TOKENS = {
    "--os-shell", "--os-pwn", "--os-cmd", "--os-smbany",
    "--dump", "--dump-all", "--dump-format", "--priv-esc",
    "--msf", "--msf-path", "--batch-smart", "--smoke-test",
    "-T5", "-T4", "-A", "-sS", "-sA", "-sN", "-sF", "-sX",
    "--script", "-exec", "--interactive", "-iL",
}
_BLOCKED_SUBSTRINGS = ("--script=", "--os-", "--tamper=", "aggressive")


def _blocked(args: list[str]) -> list[str]:
    bad = [t for t in args if t in _BLOCKED_TOKENS]
    bad += [t for t in args if any(sub in t for sub in _BLOCKED_SUBSTRINGS)]
    return sorted(set(bad))


def arsenal_route(program: str, tool: str, target: str,
                  args: str = "", timeout: int = 180) -> dict:
    """Run one allowed CLI against one scope-authorized target.

    `args` is a single space-separated string (tokens are never re-parsed
    by a shell — subprocess list form only, quoting accidents impossible).
    """
    if tool not in ALLOWED_TOOLS:
        return {"ok": False,
                "error": "tool %r is not on the allowlist: %s. The fallback "
                         "ladder (rich CLI -> curl -> python3) applies; do not "
                         "route around the gate." % (tool, ", ".join(ALLOWED_TOOLS))}
    util.require_scope(program, target, active=True)

    tokens = [t for t in (args or "").split() if t]
    if tool == "sqlmap" and "--batch" not in tokens:
        return {"ok": False,
                "error": "sqlmap runs in this arsenal only as a differential "
                         "oracle: --batch is mandatory (spine doctrine: no "
                         "interactive shells from an agent loop)"}
    bad = _blocked(tokens)
    if bad:
        rid = ledger.append(program, "arsenal_route", "%s %s" % (tool, target),
                            "refused blocked flags %s" % bad, "", "REFUSED",
                            "flag blacklist")
        return {"ok": False, "rid": rid,
                "error": "blocked flag tokens refused: %s — destructive modes "
                         "belong to manual operator sessions" % bad}

    binary = shutil.which(tool)
    if binary is None:
        rid = ledger.append(program, "arsenal_route", "%s %s" % (tool, target),
                            "tool-not-installed", "", "FACT",
                            "fallback ladder: curl/python3 equivalents")
        return {"ok": False, "rid": rid, "installed": False,
                "error": "%s is not installed in this environment — use the "
                         "stdlib tools (http_probe, content_discover) instead" % tool}

    argv = [binary] + tokens + ([target] if target and target not in tokens else [])
    try:
        proc = subprocess.run(argv, capture_output=True, timeout=timeout,
                              env={**os.environ, "LC_ALL": "C"})
    except subprocess.TimeoutExpired:
        rid = ledger.append(program, "arsenal_route", " ".join(argv[:12]),
                            "timeout after %ds" % timeout, "", "FACT", "")
        return {"ok": False, "rid": rid, "error": "timeout after %ds" % timeout}
    out = (proc.stdout or b"") + (proc.stderr or b"")
    head = out[:8192].decode("utf-8", "replace")
    rid = ledger.append(program, "arsenal_route", " ".join(argv[:12]),
                        "exit=%d output=%dB" % (proc.returncode, len(out)),
                        "%dB" % len(out), "FACT", "head saved to artifact")
    artifact = util.save_artifact(program, "%s_%s.out" % (tool, rid), out) if out else ""
    return {"ok": proc.returncode == 0, "rid": rid, "tool": tool,
            "exit": proc.returncode, "artifact": artifact,
            "output_head": head[:2000]}
