"""Scope gate — the L1 authorization layer (R0 operationalized).

Every network tool in mythos-arsenal calls `check_target()` BEFORE any byte
leaves the machine. Deny-by-default: no matching scope.csv row, no traffic.
Refusals return a reason plus what artifact would unblock the engagement.

Row classes:
  in_scope  — full testing authorized
  recon_only— passive sources only (CT logs, DNS); active tools refused
  denied    — explicit refusal; overrides any other matching row
  canary    — the operator's OWN callback collector: reachable only through
              `check_canary()` (GET-only poll, no body, no query string,
              bounded path) so out-of-band canary verification can never
              double as an exfiltration channel to a third party

House doctrine: a rule without enforcement is a suggestion. This module IS
the enforcement; the tools cannot bypass it because they all route through it.
"""
from __future__ import annotations

import csv
import ipaddress
import os
import re
from dataclasses import dataclass
from datetime import date
from urllib.parse import urlsplit

from . import paths

CLASSES = ("in_scope", "recon_only", "denied", "canary")

_URLISH = re.compile(r"^[a-z][a-z0-9+.-]*://", re.IGNORECASE)

# how far a canary poll path may extend the declared collector path —
# a session suffix, never a data channel
CANARY_PATH_SLACK = 64


@dataclass
class ScopeRow:
    target: str
    klass: str
    auth_artifact: str
    issued: str
    expires: str
    operator: str
    notes: str
    line_no: int


@dataclass
class CheckResult:
    authorized: bool
    reason: str
    matched: str = ""
    klass: str = ""
    artifact: str = ""

    def as_dict(self) -> dict:
        return {
            "authorized": self.authorized,
            "reason": self.reason,
            "matched": self.matched,
            "class": self.klass,
            "auth_artifact": self.artifact,
        }


def load_scope(path: str | None = None) -> list[ScopeRow]:
    """Parse scope.csv. Comments (#) and an optional header line are skipped."""
    path = path or paths.scope_csv()
    rows: list[ScopeRow] = []
    if not os.path.isfile(path):
        return rows
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line_no, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.lower().startswith("target,"):
                continue  # optional header
            fields = next(csv.reader([line]))
            fields = [f.strip() for f in fields]
            while len(fields) < 7:
                fields.append("")
            target, klass, artifact, issued, expires, operator, notes = fields[:7]
            if klass not in CLASSES:
                klass = "denied"
            rows.append(ScopeRow(target, klass, artifact, issued, expires,
                                 operator, notes, line_no))
    return rows


def _split_target(target: str) -> tuple[str, str, str, str]:
    """Normalize a target string to (scheme, host, port, path).

    Accepts full URLs, host, host:port, bare IPs.
    """
    target = target.strip()
    if _URLISH.match(target):
        parts = urlsplit(target)
        return parts.scheme or "http", parts.hostname or "", str(parts.port or ""), parts.path or "/"
    # bare host[:port]
    host, port = target, ""
    if ":" in target and not target.count(":") > 1:  # not an IPv6 literal
        host, port = target.rsplit(":", 1)
        if not port.isdigit():
            host, port = target, ""
    return "", host, port, ""


def _row_matches(row: ScopeRow, scheme: str, host: str, port: str, url: str) -> int:
    """Return match precedence rank (lower = stronger) or 0 = no match."""
    rt = row.target.strip()

    # 1. URL-prefix row (http(s)://... or path-bearing)
    if _URLISH.match(rt) or "/" in rt:
        if url and (url.rstrip("/") + "/").startswith(rt.rstrip("/") + "/"):
            return 5
        try:  # CIDR rows also contain "/"
            net = ipaddress.ip_network(rt, strict=False)
            if host and _ip_in_net(host, net):
                return 4
        except ValueError:
            pass
        return 0

    # 2. host:port exact
    if ":" in rt:
        rhost, rport = rt.rsplit(":", 1)
        if host == rhost and port == rport:
            return 1
        return 0

    # 3. wildcard domain *.example.com
    if rt.startswith("*."):
        base = rt[2:]
        if host == base or host.endswith("." + base):
            return 3
        return 0

    # 4. plain domain / IP — exact or subdomain suffix
    if host == rt or host.endswith("." + rt):
        return 2
    return 0


def _ip_in_net(host: str, net) -> bool:
    try:
        return ipaddress.ip_address(host) in net
    except ValueError:
        return False


def check_target(target: str, active: bool = True,
                 scope_path: str | None = None) -> CheckResult:
    """Authorization check for one target.

    active=True : the caller will send requests to the target (probes,
                  content discovery, invasive CLIs) — requires class in_scope.
    active=False: passive sources only (CT logs, DNS) — recon_only suffices.
    """
    rows = load_scope(scope_path)
    scheme, host, port, path = _split_target(target)
    if not host:
        return CheckResult(False, "unparsable target: %r" % target)
    url = "%s://%s%s%s" % (scheme or "http", host, ":" + port if port else "", path)

    matches = [(rank, row) for row in rows
               if (rank := _row_matches(row, scheme, host, port, url))]
    if not matches:
        return CheckResult(
            False,
            "R0/scope: target %r matches no scope.csv row — deny-by-default. "
            "Add a row citing the authorizing artifact (bug-bounty scope page, "
            "engagement letter, or self-owned lab declaration) to unblock." % target)

    # 'denied' rows always win, regardless of precedence.
    if any(row.klass == "denied" for _rank, row in matches):
        denied = next(row for _r, row in matches if row.klass == "denied")
        return CheckResult(False, "scope: target %r is explicitly denied (row %d)"
                           % (target, denied.line_no),
                           denied.target, "denied", denied.auth_artifact)

    # canary rows never authorize ordinary probing — a callback collector
    # is not a test target. Polls reach it only through check_canary().
    probe_matches = [m for m in matches if m[1].klass != "canary"]
    if not probe_matches:
        crow = matches[0][1]
        return CheckResult(
            False,
            "scope: target %r matches only a canary-class row — canary hosts "
            "are the operator's callback collectors, not test targets. Canary "
            "verification polls go through http_probe(canary=True), never "
            "through probing or content discovery." % target,
            crow.target, "canary", crow.auth_artifact)
    matches = probe_matches

    # Most restrictive surviving class wins; then strongest precedence.
    best_rank, row = min(matches, key=lambda m: (m[0], m[1].line_no))
    if any(r.klass == "recon_only" for _r, r in matches):
        row = next(r for _r, r in matches if r.klass == "recon_only")
        if active:
            return CheckResult(
                False,
                "scope: target %r is recon_only — passive sources allowed, "
                "active requests refused. Upgrade requires a new scope.csv row "
                "with an authorizing artifact." % target,
                row.target, "recon_only", row.auth_artifact)

    if not row.auth_artifact:
        return CheckResult(
            False,
            "R0: matching scope row (line %d) carries no authorizing artifact — "
            "no AUTH record, no traffic. Fill the auth_artifact column." % row.line_no,
            row.target, row.klass, "")

    if row.expires:
        try:
            if date.fromisoformat(row.expires) < date.today():
                return CheckResult(
                    False,
                    "scope: authorization for %r expired on %s" % (target, row.expires),
                    row.target, row.klass, row.auth_artifact)
        except ValueError:
            return CheckResult(
                False,
                "scope: unparseable expires date %r on row %d — refusing "
                "(fix the row)" % (row.expires, row.line_no),
                row.target, row.klass, row.auth_artifact)

    if row.klass == "in_scope":
        return CheckResult(
            True,
            "authorized: class in_scope, artifact %r" % row.auth_artifact,
            row.target, row.klass, row.auth_artifact)

    return CheckResult(
        True,
        "authorized for passive recon only: artifact %r" % row.auth_artifact,
        row.target, row.klass, row.auth_artifact)


def check_canary(target: str,
                 scope_path: str | None = None) -> CheckResult:
    """Authorization check for ONE canary callback verification poll.

    Canary verification is out-of-band by nature — the whole point is that
    the target server calls BACK to a collector the operator owns. That
    same out-of-band channel is the classic exfiltration route, so this
    path is deliberately narrower than `check_target`:

      * only canary-class rows authorize it (in_scope test-target rows do
        NOT — being allowed to probe a host never makes it your collector)
      * denied rows still override everything
      * GET only, no body (enforced by http_probe's canary mode)
      * no query string — ?data=... exfil is closed by policy
      * the polled path may extend the declared collector row by at most
        CANARY_PATH_SLACK characters — a session suffix, not a payload
    """
    rows = load_scope(scope_path)
    scheme, host, port, path = _split_target(target)
    if not host:
        return CheckResult(False, "unparsable canary target: %r" % target)
    if urlsplit(target if _URLISH.match(target) else "http://%s" % target).query:
        return CheckResult(
            False,
            "canary: query strings are forbidden on callback polls — the "
            "out-of-band data channel is closed by policy")
    url = "%s://%s%s%s" % (scheme or "http", host,
                            ":" + port if port else "", path)

    matches = [(rank, row) for row in rows
               if (rank := _row_matches(row, scheme, host, port, url))]
    if any(row.klass == "denied" for _rank, row in matches):
        denied = next(row for _r, row in matches if row.klass == "denied")
        return CheckResult(False, "canary: target %r is explicitly denied "
                           "(row %d)" % (target, denied.line_no),
                           denied.target, "denied", denied.auth_artifact)
    matches = [(rank, row) for rank, row in matches if row.klass == "canary"]
    if not matches:
        return CheckResult(
            False,
            "canary: %r matches no canary-class scope.csv row — declare the "
            "operator-owned collector (class canary, with artifact) before "
            "any out-of-band interaction. Test-target rows do not authorize "
            "canary polls, and third-party URLs are never auto-authorized." % target)
    _rank, row = min(matches, key=lambda m: (m[0], m[1].line_no))

    if not row.auth_artifact:
        return CheckResult(
            False,
            "canary: row %d carries no operator artifact — fill the "
            "auth_artifact column (who owns this collector)" % row.line_no,
            row.target, "canary", "")

    rt = row.target.strip()
    if _URLISH.match(rt):
        row_path = (urlsplit(rt).path or "/").rstrip("/")
        asked = (path or "/")
        slack = len(asked) - len(row_path)
        if slack > CANARY_PATH_SLACK:
            return CheckResult(
                False,
                "canary: polled path exceeds the declared collector row by "
                "%d characters — data-in-path is an exfiltration channel, "
                "not a callback" % slack,
                row.target, "canary", row.auth_artifact)

    if row.expires:
        try:
            if date.fromisoformat(row.expires) < date.today():
                return CheckResult(
                    False,
                    "canary: authorization for %r expired on %s"
                    % (target, row.expires),
                    row.target, "canary", row.auth_artifact)
        except ValueError:
            return CheckResult(
                False,
                "canary: unparseable expires date %r on row %d — refusing "
                "(fix the row)" % (row.expires, row.line_no),
                row.target, "canary", row.auth_artifact)

    return CheckResult(
        True,
        "canary poll authorized: collector %r (artifact %r)"
        % (row.target, row.auth_artifact),
        row.target, "canary", row.auth_artifact)


class ScopeViolation(Exception):
    """Raised by tools when the gate refuses a target.

    Carries the CheckResult so the caller (and the ledger) can record WHY.
    """

    def __init__(self, result: CheckResult):
        super().__init__(result.reason)
        self.result = result


def guard(target: str, active: bool = True,
          scope_path: str | None = None) -> CheckResult:
    """Check-or-raise helper used by every network tool."""
    result = check_target(target, active=active, scope_path=scope_path)
    if not result.authorized:
        raise ScopeViolation(result)
    return result


def guard_canary(target: str,
                 scope_path: str | None = None) -> CheckResult:
    """Check-or-raise helper for canary verification polls."""
    result = check_canary(target, scope_path=scope_path)
    if not result.authorized:
        raise ScopeViolation(result)
    return result
