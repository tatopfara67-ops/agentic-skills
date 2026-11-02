"""Active probing tools — every request scope-gated, ledgered, rate-limited.

http_probe      : single request, no redirect-following, body to artifact
content_discover: calibrated wordlist walk (control requests FIRST)
api_introspect  : bounded discovery of API documentation & introspection

Calibration is the differential discipline inherited from the spine: before
any wordlist entry is tested, three random non-existent paths establish the
target's 404 profile. A hit is only a deviation from that baseline — never
a bare "status != 404" guess. Soft-404 traps (200 + "not found" body) are
detected during calibration, not discovered the hard way.
"""
from __future__ import annotations

import json
import os
import random
import re
import string
import time

from .. import ledger, paths
from . import util

_GRAPHQL_INTROSPECTION = (
    '{"query":"query { __schema { queryType { name } types { name kind } }}"}'
)

_DOC_ENDPOINTS = (
    "/openapi.json", "/swagger.json", "/swagger/v1/swagger.json",
    "/api-docs", "/api-docs.json", "/v1/api-docs", "/v2/api-docs",
    "/api/openapi.json", "/api/swagger.json", "/api/v1/openapi.json",
    "/graphql", "/graphiql", "/playground", "/altair",
)


def http_probe(program: str, url: str, method: str = "GET",
               headers: dict | None = None, body: str | None = None,
               tag: str = "FACT", note: str = "",
               save_body: bool = True, timeout: int = 15,
               canary: bool = False) -> dict:
    """One request, one ledger record. Redirects are NOT followed — the
    3xx + Location header is itself the observation. Body is saved to an
    artifact and kept OUT of the returned context (spine §3).

    canary=True polls the operator's declared callback collector (scope.csv
    class `canary`) — the ONLY way to reach a canary-class host, and a
    deliberately narrow channel: GET-only, no body, no query string, the
    CANARY tag forced. Out-of-band exfiltration through the canary channel
    is refused and ledgered, not merely discouraged."""
    if canary:
        if method.upper() != "GET" or body is not None:
            rid = ledger.append(program, "http_probe",
                                "canary poll refused: non-GET or body",
                                "method=%s body=%dB" % (method,
                                                         len(body or "")),
                                "", "REFUSED",
                                "canary polls are GET-only, no body")
            raise ValueError("canary polls are GET-only with no body — the "
                             "out-of-band data channel is closed (refused "
                             "as %s)" % rid)
        util.require_canary(program, url)
        tag = "CANARY"
        note = (note + " canary poll").strip()
    else:
        util.require_scope(program, url, active=True)
    r = util.http_fetch(url, method=method, headers=headers, body=body,
                        timeout=timeout)
    rid = ledger.append(program, "%s %s" % (method, url.split("//", 1)[-1][:100]),
                        url, "%s %s" % (r["status"], (r["reason"] or "")[:40]),
                        "%dB" % len(r["body"]), tag,
                        (note + " sha12=%s" % r["sha12"]).strip())
    out = util.compact(r)
    out["rid"] = rid
    if save_body and r["body"]:
        out["artifact"] = util.save_artifact(
            program, "%s.body" % rid, r["body"])
    return out


def _calibrate(program: str, base: str, timeout: int) -> dict:
    """Three random paths = the control round (spine §6: control first)."""
    statuses, sizes = [], []
    for _ in range(3):
        junk = "".join(random.choices(string.ascii_lowercase, k=14))
        r = util.http_fetch(base.rstrip("/") + "/" + junk, timeout=timeout)
        statuses.append(r["status"])
        sizes.append(len(r["body"]))
        ledger.append(program, "content_discover", "control /%s" % junk,
                      "%s %dB" % (r["status"], len(r["body"])),
                      "%dB" % len(r["body"]), "CONTROL",
                      "404-profile calibration")
    soft_404 = statuses and all(s == 200 for s in statuses)
    return {"status": max(set(statuses), key=statuses.count),
            "size_min": min(sizes), "size_max": max(sizes),
            "soft_404": soft_404}


def _load_wordlist(name: str) -> list[str]:
    if os.path.isabs(name):
        path = name
    else:
        path = os.path.join(paths.wordlists_dir(), "%s.txt" % name)
    if not os.path.isfile(path):
        raise ValueError("wordlist not found: %s (expected %s)" % (name, path))
    with open(path, encoding="utf-8", errors="replace") as fh:
        return [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]


def content_discover(program: str, base_url: str, wordlist: str = "default",
                     extensions: list[str] | None = None,
                     max_requests: int = 150, rate_per_s: float = 8.0,
                     timeout: int = 12) -> dict:
    """Calibrated content discovery. GET-only, rate-courteous, capped.

    Returns deviations from the calibrated baseline only — volume is not
    the product, signal is. Extension '' (bare path) is always included.
    """
    util.require_scope(program, base_url, active=True)
    base = base_url.rstrip("/")
    words = _load_wordlist(wordlist)[:max_requests]
    exts = list(dict.fromkeys([""] + list(extensions or [])))
    plan = [w + e for e in exts for w in words][:max_requests]

    cal = _calibrate(program, base, timeout)
    findings, probe_count = [], 0
    delay = 1.0 / max(rate_per_s, 0.1)
    for path_ in plan:
        if probe_count >= max_requests:
            break
        time.sleep(delay)
        probe_count += 1
        url = "%s/%s" % (base, path_.lstrip("/"))
        try:
            r = util.http_fetch(url, timeout=timeout)
        except Exception as exc:
            ledger.append(program, "content_discover", "GET /%s" % path_,
                          "network-error %s" % exc.__class__.__name__,
                          "", "FACT", "")
            continue
        status, size = r["status"], len(r["body"])
        ledger.append(program, "content_discover", "GET /%s" % path_,
                      "%s %dB" % (status, size), "%dB" % size, "FACT", "")
        deviates = status != cal["status"]
        if status == cal["status"] and cal["size_min"] <= size <= cal["size_max"]:
            deviates = False  # same status, baseline-sized body
        if cal["soft_404"] and status == 200:
            # 200s are the trap baseline: only size outliers deviate
            deviates = not (cal["size_min"] <= size <= cal["size_max"])
        if deviates:
            rid = ledger.append(program, "content_discover",
                                "GET /%s" % path_,
                                "%s %dB deviates-from-baseline" % (status, size),
                                "%dB" % size, "SURFACE",
                                "cal=%s %d-%dB soft404=%s"
                                % (cal["status"], cal["size_min"],
                                   cal["size_max"], cal["soft_404"]))
            findings.append({"path": "/" + path_, "status": status,
                             "size": size, "rid": rid,
                             "location": r["location"][:120]})
    return {"ok": True, "base": base, "probes": probe_count,
            "calibration": cal, "findings": findings}


def api_introspect(program: str, base_url: str, timeout: int = 12,
                   delay: float = 0.25) -> dict:
    """Bounded API-documentation & introspection sweep (max: the endpoint
    list + one GraphQL introspection POST). Read-only queries only, with
    a courteous delay between requests — authorized is not unlimited."""
    util.require_scope(program, base_url, active=True)
    base = base_url.rstrip("/")
    found = []
    for endpoint in _DOC_ENDPOINTS:
        url = base + endpoint
        try:
            r = util.http_fetch(url, timeout=timeout)
        except Exception as exc:
            ledger.append(program, "api_introspect", "GET %s" % endpoint,
                          "network-error %s" % exc.__class__.__name__,
                          "", "FACT", "")
            continue
        finally:
            time.sleep(delay)
        size = len(r["body"])
        interesting = r["status"] == 200 and (
            endpoint.endswith((".json", "-docs", "/api-docs")) or size > 0)
        if r["status"] == 200 and endpoint == "/graphql":
            interesting = True
        ledger.append(program, "api_introspect", "GET %s" % endpoint,
                      "%s %dB" % (r["status"], size), "%dB" % size,
                      "SURFACE" if interesting else "FACT", "")
        if not interesting:
            continue
        entry = {"endpoint": endpoint, "status": r["status"], "size": size}
        body = r["body"][:200000]
        if endpoint == "/graphql":
            try:
                q = util.http_fetch(url, method="POST", timeout=timeout,
                                    headers={"Content-Type": "application/json"},
                                    body=_GRAPHQL_INTROSPECTION)
                if q["status"] == 200 and b"__schema" in q["body"]:
                    entry["introspection"] = "enabled"
                    entry["rid"] = ledger.append(
                        program, "api_introspect", "POST /graphql introspection",
                        "schema exposed", "%dB" % len(q["body"]), "SURFACE",
                        "bounded read-only query")
            except Exception:
                entry["introspection"] = "query-failed"
        else:
            try:
                spec = json.loads(body)
                paths_ = sorted((spec.get("paths") or {}).keys())
                if paths_:
                    entry["paths"] = paths_[:80]
                    entry["path_count"] = len(paths_)
            except ValueError:
                entry["note"] = "non-JSON body"
            if r["body"]:
                entry["artifact"] = util.save_artifact(
                    program, "api_%s.body" % endpoint.strip("/").replace("/", "_"),
                    r["body"])
        found.append(entry)
    return {"ok": True, "base": base, "probed": len(_DOC_ENDPOINTS),
            "found": found}
