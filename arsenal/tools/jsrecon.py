"""js-recon — fetch a JS bundle and analyze it LOCALLY.

Secrets policy (hard rule, mechanically enforced here):
  * discovered key-shaped strings are REPORTED as triage hints and their
    VALUES are masked in the returned context; full values live only in
    the on-disk artifact for the operator
  * the tool never uses, validates, or exfiltrates a discovered secret —
    that is the operator's decision, made outside this pipeline
"""
from __future__ import annotations

import re

from .. import ledger
from . import util

# Report-only patterns. Values are masked to the first 6 chars in context.
_SECRET_PATTERNS = (
    ("aws-access-key", re.compile(r"\b(AKIA[0-9A-Z]{16})\b")),
    ("google-api-key", re.compile(r"\b(AIza[0-9A-Za-z_\-]{35})\b")),
    ("jwt", re.compile(r"\b(eyJ[0-9A-Za-z_\-]{20,}\.[0-9A-Za-z_\-]{10,}\.[0-9A-Za-z_\-]{10,})\b")),
    ("private-key", re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("generic-api-key", re.compile(
        r"""["']?(?:api[_-]?key|apikey|secret|token|passwd|password)["']?\s*[:=]\s*["']([A-Za-z0-9_\-\.+/]{16,})["']""", re.IGNORECASE)),
)

# Path-shaped strings inside quotes: endpoints, routes, template URIs.
_ENDPOINT_RE = re.compile(
    r"""["'](\/[A-Za-z0-9_\-\.~\/\{\}:]{2,140})["']""")

# Unquoted paths (for comment lines): "/api/v0/debug" style, at least one
# segment, no quotes required, and never the "//" comment marker itself.
_COMMENT_PATH_RE = re.compile(
    r"(\/[A-Za-z0-9_\-\.]+(?:\/[A-Za-z0-9_\-\.]+)*)")

_SOURCEMAP_RE = re.compile(r"sourceMappingURL=([^\s\)]+)")


def _mask(value: str) -> str:
    return value[:6] + "…(%d chars, masked; full value in artifact only)" % len(value)


def js_analyze(program: str, url: str, timeout: int = 20) -> dict:
    """Fetch one JS asset, save it as an artifact, extract surfaces.

    Returns endpoints, secret HINTS (masked), sourcemap references, and a
    canary-grade note for the ledger. Local analysis only — one request
    total is sent to the target.
    """
    util.require_scope(program, url, active=True)
    r = util.http_fetch(url, timeout=timeout)
    rid = ledger.append(program, "js_analyze", "fetch %s" % url,
                        "%s %dB" % (r["status"], len(r["body"])),
                        "%dB" % len(r["body"]), "FACT",
                        "sha12=%s" % r["sha12"])
    if r["status"] != 200 or not r["body"]:
        return {"ok": False, "rid": rid, "status": r["status"],
                "error": "asset not retrievable (status %s)" % r["status"]}
    text = r["body"].decode("utf-8", "replace")
    artifact = util.save_artifact(
        program, "js_%s.body" % rid, r["body"])

    endpoints = []
    for match in _ENDPOINT_RE.findall(text):
        clean = match.rstrip("/")
        if clean and clean not in endpoints and not clean.startswith("//"):
            endpoints.append(clean)

    # commented-out routes are archaeological gold — flag them separately.
    # Comment text is unquoted, so this pattern does NOT require quotes.
    commented = []
    for line in text.splitlines():
        if "//" in line or "/*" in line:
            for match in _COMMENT_PATH_RE.findall(line):
                if match not in commented:
                    commented.append(match)

    secrets = []
    for label, pattern in _SECRET_PATTERNS:
        for match in pattern.findall(text) if pattern.groups else pattern.findall(text):
            value = match if isinstance(match, str) else match[0]
            secrets.append({"kind": label, "masked": _mask(value)})

    sourcemaps = _SOURCEMAP_RE.findall(text)

    rid_surface = ledger.append(
        program, "js_analyze", "analyze %s" % url,
        "%d endpoints, %d secret-hints, %d sourcemaps"
        % (len(endpoints), len(secrets), len(sourcemaps)),
        "%dB" % len(r["body"]), "SURFACE",
        "artifact=%s" % artifact)
    return {
        "ok": True, "rid": rid, "surface_rid": rid_surface,
        "status": r["status"], "artifact": artifact,
        "endpoints": endpoints[:120],
        "endpoints_total": len(endpoints),
        "commented_routes": commented[:40],
        "secret_hints": secrets[:20],
        "sourcemaps": sourcemaps[:10],
    }
