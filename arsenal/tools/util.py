"""Shared plumbing for mythos-arsenal tools: gating, HTTP, refusing."""
from __future__ import annotations

import hashlib
import io
import time
import urllib.error
import urllib.request

from .. import ledger
from ..scope_gate import CheckResult, ScopeViolation, guard, guard_canary

UA = "MythosArsenal/1.0 (authorized-research; scope-gated)"


def require_scope(program: str, target: str, active: bool = True) -> CheckResult:
    """Gate a target; on refusal, record it in the ledger and raise.

    Every network tool calls this FIRST. A refusal is itself an observation
    worth keeping: the REFUSED record is the audit trail that the gate held.
    """
    try:
        return guard(target, active=active)
    except ScopeViolation as exc:
        ledger.append(program, "scope-gate",
                      "target=%r active=%s" % (target, active),
                      exc.result.reason, "", "REFUSED", "gate refusal")
        raise RuntimeError(exc.result.reason) from exc


def require_canary(program: str, target: str) -> CheckResult:
    """Gate a canary verification poll (narrower channel: GET-only, no
    query string, bounded path — see scope_gate.check_canary). Refusals
    are ledgered like every other gate decision."""
    try:
        return guard_canary(target)
    except ScopeViolation as exc:
        ledger.append(program, "scope-gate",
                      "canary target=%r" % target,
                      exc.result.reason, "", "REFUSED", "canary gate refusal")
        raise RuntimeError(exc.result.reason) from exc


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


def http_fetch(url: str, method: str = "GET", headers: dict | None = None,
               body: str | None = None, timeout: int = 15) -> dict:
    """Fetch without redirect-following (the 3xx itself is the signal).

    Returns {status, reason, headers, body, ms, sha12, location}.
    Never raises for HTTP status codes; raises only on network failure.
    """
    req = urllib.request.Request(url, method=method.upper())
    req.add_header("User-Agent", UA)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    data = body.encode("utf-8") if body is not None else None
    started = time.monotonic()
    try:
        resp = _OPENER.open(req, timeout=timeout, data=data)
        raw = resp.read()
        status, reason, hdrs = resp.status, resp.reason, dict(resp.headers)
    except urllib.error.HTTPError as exc:
        try:
            raw = exc.read()
        except Exception:
            raw = b""
        status, reason, hdrs = exc.code, exc.reason, dict(exc.headers or {})
    ms = int((time.monotonic() - started) * 1000)
    return {
        "status": status,
        "reason": reason,
        "headers": {k.lower(): v for k, v in hdrs.items()},
        "body": raw,
        "ms": ms,
        "sha12": hashlib.sha256(raw).hexdigest()[:12],
        "location": hdrs.get("location", "") or hdrs.get("Location", ""),
    }


def compact(r: dict, body_limit: int = 0) -> dict:
    """Ledger-sized view of an http_fetch result. Bodies stay out of context."""
    out = {
        "status": r["status"],
        "reason": r["reason"],
        "size": len(r["body"]),
        "ms": r["ms"],
        "sha12": r["sha12"],
    }
    for key in ("location", "content-type", "server", "x-powered-by", "cf-ray"):
        val = r["headers"].get(key)
        if val:
            out[key] = val[:120]
    if body_limit:
        out["body_head"] = r["body"][:body_limit].decode("utf-8", "replace")
    return out


def save_artifact(program: str, name: str, payload: bytes) -> str:
    """Persist raw evidence on disk; return the artifact path (§3)."""
    import os

    from .. import paths

    d = os.path.join(paths.program_dir(program), "artifacts")
    os.makedirs(d, exist_ok=True)
    safe = "".join(c for c in name if c.isalnum() or c in "-_.")
    path = os.path.join(d, safe)
    with open(path, "wb") as fh:
        fh.write(payload)
    return path
