"""Passive recon tools — no packet ever touches the target itself.

ct_subdomains : certificate-transparency lookup via crt.sh (public database)
dns_resolve   : resolver via stdlib socket (+ dnspython if installed)

Both pass the scope gate with active=False (recon_only rows suffice) —
but they still refuse unknown targets: deny-by-default has no exceptions,
because even passive tooling must be auditable against scope.
"""
from __future__ import annotations

import json
import socket
import urllib.parse
import urllib.request

from .. import ledger
from . import util


def ct_subdomains(program: str, domain: str, timeout: int = 25) -> dict:
    """Query crt.sh certificate transparency for names under `domain`.

    Passive: reads a public database, never the target. Unique names only.
    On network failure returns ok=False with the error — never a crash.
    """
    util.require_scope(program, domain, active=False)
    url = "https://crt.sh/?q=%s&output=json" % urllib.parse.quote("%." + domain)
    started_note = "crt.sh CT lookup for %s" % domain
    try:
        req = urllib.request.Request(url, headers={"User-Agent": util.UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8", "replace"))
    except Exception as exc:  # offline lab, blocked egress, timeout
        rid = ledger.append(program, "ct_subdomains", started_note,
                            "unreachable: %s" % exc.__class__.__name__,
                            "", "FACT", "passive source unavailable; fallback ladder applies")
        return {"ok": False, "rid": rid, "names": [],
                "error": "crt.sh unreachable: %s" % exc}
    names = set()
    for entry in payload:
        for key in ("common_name", "name_value"):
            val = entry.get(key, "")
            for nm in str(val).split("\n"):
                nm = nm.strip().lstrip("*.").lower()
                if nm.endswith("." + domain.lower()) or nm == domain.lower():
                    names.add(nm)
    ordered = sorted(names)
    rid = ledger.append(program, "ct_subdomains", started_note,
                        "%d unique names" % len(ordered),
                        len(payload), "SURFACE",
                        ";".join(ordered[:12]) + ("…" if len(ordered) > 12 else ""))
    return {"ok": True, "rid": rid, "count": len(ordered), "names": ordered}


def dns_resolve(program: str, host: str) -> dict:
    """Resolve A/AAAA records (stdlib) plus CNAME when dnspython is present.

    Passive resolution against the resolver, not the target's servers.
    """
    util.require_scope(program, host, active=False)
    addr_info = []
    try:
        for info in socket.getaddrinfo(host, None):
            entry = info[4][0]
            if entry not in addr_info:
                addr_info.append(entry)
    except socket.gaierror as exc:
        rid = ledger.append(program, "dns_resolve", "resolve %s" % host,
                            "NXDOMAIN/unresolvable (%s)" % exc.__class__.__name__,
                            "", "FACT", "")
        return {"ok": False, "rid": rid, "host": host, "addresses": [],
                "error": str(exc)}
    result = {"ok": True, "host": host,
              "addresses": addr_info, "cname": None, "mx": None}
    try:  # optional depth when dnspython exists in the environment
        import dns.resolver  # type: ignore

        resolver = dns.resolver.Resolver()
        try:
            result["cname"] = str(
                resolver.resolve(host, "CNAME")[0].target).rstrip(".")
        except Exception:
            pass
        try:
            result["mx"] = [str(r.exchange).rstrip(".")
                            for r in resolver.resolve(host, "MX")]
        except Exception:
            pass
    except ImportError:
        result["note"] = "CNAME/MX require dnspython (pip install dnspython)"
    rid = ledger.append(program, "dns_resolve", "resolve %s" % host,
                        "A %s" % ",".join(addr_info[:6]),
                        "", "FACT",
                        "cname=%s" % result["cname"] if result["cname"] else "")
    result["rid"] = rid
    return result
