"""CVSS v3.1 base-score engine — FIRST spec, section 7.1, verbatim.

Shared by the `cvss3_score` MCP tool and the report auditor so the score an
agent writes is the score the auditor recomputes (one arithmetic, one truth).

Reference: FIRST, "Common Vulnerability Scoring System version 3.1:
Specification Document", sections 7.1-7.3 (base metrics and equations).
The spec is public; the arithmetic below follows it exactly, including the
Roundup function (smallest number with one decimal place >= the input).

Scope of this module: BASE score only. Temporal and environmental metrics
belong to the analyst; the arsenal ships vectors that describe the observed
attack path, nothing more.
"""
from __future__ import annotations

import math

# ------------------------------------------------------------- metric tables

AV = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.2}
AC = {"L": 0.77, "H": 0.44}
UI = {"N": 0.85, "R": 0.62}
CIA = {"H": 0.56, "L": 0.22, "N": 0.0}
SCOPE = ("U", "C")

REQUIRED = ("AV", "AC", "PR", "UI", "S", "C", "I", "A")

_PREFIX_RE_OK = ("CVSS:3.1/", "CVSS:3.0/")

SEVERITY_BANDS = (
    (0.0, "None"),
    (0.1, "Low"), (3.9, "Low"),
    (4.0, "Medium"), (6.9, "Medium"),
    (7.0, "High"), (8.9, "High"),
    (9.0, "Critical"), (10.0, "Critical"),
)


def severity_band(score: float) -> str:
    """Qualitative severity label for a base score (spec table 14)."""
    if score <= 0.0:
        return "None"
    if score <= 3.9:
        return "Low"
    if score <= 6.9:
        return "Medium"
    if score <= 8.9:
        return "High"
    return "Critical"


def _pr_weight(pr: str, scope: str) -> float:
    """PR weight depends on Scope (spec table 7): changed scope relaxes PR."""
    if scope == "C":
        return {"N": 0.85, "L": 0.68, "H": 0.5}[pr]
    return {"N": 0.85, "L": 0.62, "H": 0.27}[pr]


def parse_vector(vector: str) -> dict:
    """Parse and validate a CVSS v3.1 base vector.

    Accepts `CVSS:3.1/AV:N/...`, `CVSS:3.0/AV:N/...`, or a bare `AV:N/...`.
    Returns the 8 base metrics as a dict. Raises ValueError with the exact
    defect for anything that is not a complete, well-formed base vector —
    the auditor relies on these messages staying instructive.
    """
    text = (vector or "").strip()
    if not text:
        raise ValueError("empty CVSS vector")
    version = "3.1"
    for prefix in _PREFIX_RE_OK:
        if text.upper().startswith(prefix):
            version = prefix.split(":", 1)[1].rstrip("/")
            text = text[len(prefix):]
            break
    else:
        if text.upper().startswith("CVSS:"):
            raise ValueError(
                "unsupported CVSS version prefix (supported: %s) — this engine "
                "scores v3.1 base vectors" % ", ".join(_PREFIX_RE_OK))
    metrics: dict = {}
    for token in text.split("/"):
        token = token.strip()
        if not token:
            continue
        if ":" not in token:
            raise ValueError("malformed vector token %r — expected METRIC:VALUE "
                             "pairs joined by '/'" % token)
        key, _, value = token.partition(":")
        key = key.strip().upper()
        value = value.strip().upper()
        if key not in REQUIRED:
            raise ValueError("unknown metric %r — the 8 base metrics are %s"
                             % (key, "/".join(REQUIRED)))
        if key in metrics:
            raise ValueError("duplicate metric %r — each base metric appears "
                             "exactly once" % key)
        valid = {"AV": AV, "AC": AC, "UI": UI, "C": CIA, "I": CIA, "A": CIA}
        if key == "PR":
            if value not in ("N", "L", "H"):
                raise ValueError("PR:value must be N, L, or H (got %r)" % value)
        elif key == "S":
            if value not in SCOPE:
                raise ValueError("S:value must be U or C (got %r)" % value)
        elif key in valid and value not in valid[key]:
            allowed = ", ".join(sorted(valid[key]))
            raise ValueError("%s:value must be one of %s (got %r)"
                             % (key, allowed, value))
        metrics[key] = value
    missing = [m for m in REQUIRED if m not in metrics]
    if missing:
        raise ValueError("incomplete base vector — missing metric(s): %s"
                         % ", ".join(missing))
    metrics["_version"] = version
    return metrics


def roundup(value: float) -> float:
    """Spec Roundup: smallest number with one decimal place >= value."""
    int_input = round(value * 100000)
    if int_input % 10000 == 0:
        return int_input / 100000.0
    return (math.floor(int_input / 10000) + 1) / 10.0


def base_score(vector: str) -> dict:
    """Score one CVSS v3.1 base vector (spec equations 1-9).

    Returns score, severity band, the three intermediate quantities
    (ISS, Impact, Exploitability), the parsed metrics, and the canonical
    vector string — everything a report line needs, computed once.
    """
    m = parse_vector(vector)
    iss = 1.0 - (1.0 - CIA[m["C"]]) * (1.0 - CIA[m["I"]]) * (1.0 - CIA[m["A"]])
    if m["S"] == "U":
        impact = 6.42 * iss
    else:
        impact = 7.52 * (iss - 0.029) - 3.25 * (iss - 0.02) ** 15
    exploitability = (8.22 * AV[m["AV"]] * AC[m["AC"]]
                      * _pr_weight(m["PR"], m["S"]) * UI[m["UI"]])
    if impact <= 0:
        score = 0.0
    elif m["S"] == "U":
        score = roundup(min(impact + exploitability, 10.0))
    else:
        score = roundup(min(1.08 * (impact + exploitability), 10.0))
    canonical = "CVSS:%s/%s" % (
        m["_version"],
        "/".join("%s:%s" % (k, m[k]) for k in REQUIRED))
    return {
        "vector": canonical,
        "score": round(score, 1),
        "severity": severity_band(score),
        "iss": round(iss, 6),
        "impact": round(impact, 6),
        "exploitability": round(exploitability, 6),
        "metrics": {k: m[k] for k in REQUIRED},
    }
