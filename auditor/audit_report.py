#!/usr/bin/env python3
"""mythos-arsenal report auditor — PASS/FAIL evidence-discipline gate.

Usage:
    python3 auditor/audit_report.py <report.md>

Checks (the spine's report contract, applied to arsenal engagements):
 1. any line carrying a severity or vulnerability-class word cites an
    R-NNN record on that same line
 2. hypothesis blocks (### H-NNN) each carry a Closure: line with exactly
    one of CONFIRMED / FALSIFIED / INCONCLUSIVE
 3. experiment cards (### E-NNN) carry n_runs: N (or attempts: N +
    success_rate: NN%)
 4. no hedging slop phrases; no ungated victory language
 5. CONFIRMED + severity requires an impact-chain line and a canary
    reference in the finding block
 6. INCONCLUSIVE closures appear in the leads appendix
 7. no placeholder markers
 8. skill-mythos gates (a CONFIRMED finding block that declares a
    `severity:` rating must carry the full triage-grade classification
    set, in the SAME block):
      a. cvss: line — a CVSS v3.1 base vector + the computed score; the
         score is RECOMPUTED here (arsenal/cvss.py, FIRST spec) and a
         mismatch fails the report
      b. vrt: line — a Bugcrowd VRT category (dotted id) + P-rating,
         validated against the shipped official taxonomy
         (skills/skill-mythos/references/vrt-taxonomy.json)
      c. a reproduction reference — an E-NNN experiment card or an
         explicit reproduction: line
    Incident handoffs (adversary hunts) rate `Risk:`, not `severity:` —
    the classification gates do not apply to them.
Exit 0 = PASS. Exit 1 = violations listed. Fix the work, not the auditor.
"""
from __future__ import annotations

import os
import re
import sys

SEVERITY_WORDS = re.compile(
    r"\b(critical|high|medium|low|informational|severity)\b", re.I)
CLASS_WORDS = re.compile(
    r"\b(IDOR|BOLA|XSS|SSRF|SQLi|SQL injection|takeover|RCE|CSRF|"
    r"misconfiguration|vulnerable|vulnerability)\b", re.I)
HEDGING = re.compile(
    r"(might be|could be|maybe|appears to|seems to|probably|potentially)",
    re.I)
VICTORY = re.compile(r"\b(JACKPOT|BREAKTHROUGH|bingo)\b", re.I)
PLACEHOLDER = re.compile(r"TODO|FIXME|\bXXX\b|\bTBD\b|【|_{5,}")
RID = re.compile(r"\bR-\d{3,}\b")
H_BLOCK = re.compile(r"^###\s+(H-\d{3,})\b")
E_BLOCK = re.compile(r"^###\s+(E-\d{3,})\b")
CLOSURE = re.compile(r"^(?:[-*]\s*)?Closure:\s*(CONFIRMED|FALSIFIED|INCONCLUSIVE)\b")
N_RUNS = re.compile(r"^(?:[-*]\s*)?n_runs:\s*(\d+)")
ATTEMPTS = re.compile(r"^(?:[-*]\s*)?attempts:\s*(\d+)")
RATE = re.compile(r"^(?:[-*]\s*)?success_rate:\s*(\d+)%")
SEVERITY_LINE = re.compile(r"^(?:[-*]\s*)?[Ss]everity:\s*\S")
CVSS_LINE = re.compile(r"^(?:[-*]\s*)?cvss:\s*(.+)$", re.I)
VRT_LINE = re.compile(r"^(?:[-*]\s*)?vrt:\s*(.+)$", re.I)
CVSS_VECTOR = re.compile(r"CVSS:3\.[01](?:/[A-Z]+:[A-Z0-9]+)+")
CVSS_STATED = re.compile(r"=\s*(\d+(?:\.\d+)?)\b")
VRT_PATH = re.compile(r"\b([a-z][a-z_]*(?:\.[a-z_0-9]+)+)\b")
P_LEVEL = re.compile(r"\bP([1-5])\b")
E_REF = re.compile(r"\bE-\d{3,}\b")
REPRO_LINE = re.compile(r"^(?:[-*]\s*)?reproduction:\s*\S", re.I)

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (_ROOT,):
    if _p not in sys.path:
        sys.path.insert(0, _p)
try:
    from arsenal import cvss as _cvss  # noqa: E402
except Exception:  # pragma: no cover — standalone use outside the tree
    _cvss = None


def _load_vrt_taxonomy():
    """Shipped official Bugcrowd VRT taxonomy, or None when absent."""
    path = os.path.join(_ROOT, "skills", "skill-mythos", "references",
                        "vrt-taxonomy.json")
    try:
        import json
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        return data.get("content") or data
    except (OSError, ValueError):
        return None


_VRT_TAXONOMY = None
_VRT_TRIED = False


def _vrt_node(dotted: str):
    global _VRT_TAXONOMY, _VRT_TRIED
    if not _VRT_TRIED:
        _VRT_TRIED = True
        _VRT_TAXONOMY = _load_vrt_taxonomy()
    if _VRT_TAXONOMY is None:
        return None
    node = {"children": _VRT_TAXONOMY}
    for part in dotted.split("."):
        node = next((ch for ch in node.get("children", []) or []
                     if ch.get("id") == part), None)
        if node is None:
            return None
    return node


def audit(path: str) -> list[tuple[str, str]]:
    results = []

    def note(status, msg):
        results.append((status, msg))

    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        return [("FAIL", "report unreadable: %s" % exc)]

    lines = text.splitlines()
    if not text.strip():
        return [("FAIL", "report is empty")]

    # 7. placeholders
    ph = sorted(set(PLACEHOLDER.findall(text)))
    if ph:
        note("FAIL", "placeholder markers present: %s" % ph)
    else:
        note("PASS", "no placeholder markers")

    # 4. hedging + victory language
    hedges = sorted(set(m.group(1).lower() for m in HEDGING.finditer(text)))
    if hedges:
        note("FAIL", "hedging slop phrases present: %s" % hedges)
    else:
        note("PASS", "no hedging slop")
    if VICTORY.search(text):
        note("FAIL", "ungated victory language present")
    else:
        note("PASS", "no ungated victory language")

    # 1. severity/class lines cite records
    uncited = []
    for i, line in enumerate(lines, 1):
        if (SEVERITY_WORDS.search(line) or CLASS_WORDS.search(line)) \
                and not RID.search(line):
            uncited.append("line %d: %s" % (i, line.strip()[:90]))
    if uncited:
        note("FAIL", "severity/class claims without R-NNN citation: %s"
             % "; ".join(uncited[:6]))
    else:
        note("PASS", "all severity/class lines cite records")

    # 2/3/5/6/8. block-level contracts. A block is strict: it runs from
    # its ### heading to the NEXT heading of any level — summary sections
    # (##) never leak into a finding block.
    h_blocks = {}
    e_blocks = {}
    current = None
    for i, line in enumerate(lines, 1):
        m = H_BLOCK.match(line)
        if m:
            current = ("H", m.group(1), i)
            h_blocks[m.group(1)] = {"start": i, "closure": None,
                                    "body": []}
            continue
        m = E_BLOCK.match(line)
        if m:
            current = ("E", m.group(1), i)
            e_blocks[m.group(1)] = {"start": i, "n_runs": None,
                                    "attempts": None, "rate": None,
                                    "body": []}
            continue
        if line.startswith("## ") or line.startswith("### "):
            current = None
        if current:
            kind, bid, _ = current
            store = h_blocks[bid] if kind == "H" else e_blocks[bid]
            cm = CLOSURE.match(line)
            if cm:
                store["closure"] = cm.group(1)
            nm = N_RUNS.match(line)
            if nm:
                store["n_runs"] = int(nm.group(1))
            am = ATTEMPTS.match(line)
            if am:
                store["attempts"] = int(am.group(1))
            rm = RATE.match(line)
            if rm:
                store["rate"] = int(rm.group(1))
            store["body"].append(line)

    bad_h = [h for h, d in h_blocks.items() if not d["closure"]]
    if bad_h:
        note("FAIL", "hypotheses without Closure line: %s" % bad_h)
    elif h_blocks:
        note("PASS", "%d hypothesis block(s) closed" % len(h_blocks))

    bad_e = []
    for e, d in e_blocks.items():
        if d["n_runs"] is None and (d["attempts"] is None or d["rate"] is None):
            bad_e.append(e)
    if bad_e:
        note("FAIL", "experiment cards without n_runs/attempts+rate: %s" % bad_e)
    elif e_blocks:
        note("PASS", "%d experiment card(s) carry reproduction data"
             % len(e_blocks))

    # 5. CONFIRMED + severity => impact chain + canary in the block
    for h, d in h_blocks.items():
        body = "\n".join(d["body"])
        if d["closure"] == "CONFIRMED" and SEVERITY_WORDS.search(body):
            if "impact-chain:" not in body:
                note("FAIL", "%s CONFIRMED with severity lacks impact-chain"
                     % h)
            if "canary" not in body.lower():
                note("FAIL", "%s CONFIRMED with severity lacks canary "
                     "reference" % h)

    # 8. skill-mythos classification gates: a CONFIRMED finding block that
    # declares a `severity:` rating is a vulnerability finding, and must
    # carry the full triage-grade set IN the block
    for h, d in h_blocks.items():
        if d["closure"] != "CONFIRMED":
            continue
        body_lines = d["body"]
        if not any(SEVERITY_LINE.match(l) for l in body_lines):
            continue
        body = "\n".join(body_lines)
        cvss_line = next((l for l in body_lines if CVSS_LINE.match(l)), "")
        vrt_line = next((l for l in body_lines if VRT_LINE.match(l)), "")
        if not cvss_line:
            note("FAIL", "%s declares a severity rating but carries no "
                 "cvss: line (vector + score — skill-mythos gate A10)" % h)
        else:
            vm = CVSS_VECTOR.search(cvss_line)
            if not vm:
                note("FAIL", "%s cvss: line carries no CVSS v3.1 base "
                     "vector" % h)
            else:
                vector = vm.group(0)
                sm = CVSS_STATED.search(cvss_line)
                if not sm:
                    note("FAIL", "%s cvss: line states no computed score "
                         "(write '= N.N' from cvss3_score)" % h)
                elif _cvss is None:
                    note("INFO", "%s cvss score not recomputed "
                         "(arsenal/cvss.py unavailable here)" % h)
                else:
                    try:
                        recomputed = _cvss.base_score(vector)["score"]
                    except ValueError as exc:
                        note("FAIL", "%s cvss vector invalid: %s" % (h, exc))
                    else:
                        stated = float(sm.group(1))
                        if abs(stated - recomputed) > 0.001:
                            note("FAIL", "%s cvss score mismatch: line says "
                                 "%.1f, vector computes %.1f — fix one of "
                                 "them" % (h, stated, recomputed))
        if not vrt_line:
            note("FAIL", "%s declares a severity rating but carries no "
                 "vrt: line (Bugcrowd category + P-rating)" % h)
        else:
            pm = P_LEVEL.search(vrt_line)
            if not pm:
                note("FAIL", "%s vrt: line states no P-rating (P1-P5)" % h)
            vpm = VRT_PATH.search(vrt_line)
            if vpm:
                node = _vrt_node(vpm.group(1))
                if node is None and _VRT_TAXONOMY is not None:
                    note("FAIL", "%s vrt category %r not found in the "
                         "shipped taxonomy — copy the exact dotted id from "
                         "vrt_classify" % (h, vpm.group(1)))
            else:
                note("FAIL", "%s vrt: line carries no dotted category id "
                     "(e.g. broken_access_control.idor)" % h)
        if not (E_REF.search(body) or any(REPRO_LINE.match(l)
                                          for l in body_lines)):
            note("FAIL", "%s lacks a reproduction reference (E-NNN card "
                 "or reproduction: line) — fully reproducible or it does "
                 "not ship" % h)
        else:
            note("PASS", "%s CONFIRMED finding carries the full "
                 "classification set (cvss + vrt + reproduction)" % h)

    # 6. INCONCLUSIVE => leads appendix
    inconclusive = [h for h, d in h_blocks.items()
                    if d["closure"] == "INCONCLUSIVE"]
    if inconclusive:
        lead_section = re.search(r"^##\s.*[Ll]eads", text, re.M)
        if not lead_section:
            note("FAIL", "INCONCLUSIVE hypotheses (%s) but no leads "
                 "appendix section" % inconclusive)
        else:
            note("PASS", "INCONCLUSIVE hypotheses parked in leads appendix")

    note("INFO", "blocks: %d hypotheses, %d experiments"
         % (len(h_blocks), len(e_blocks)))
    return results


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    path = argv[1]
    print("== audit: %s" % path)
    failed = False
    for status, msg in audit(path):
        print("[ %s ] %s" % (status, msg))
        if status == "FAIL":
            failed = True
    print("RESULT: %s" % ("FAIL — fix the work behind the report, not the "
                          "auditor" if failed else "PASS"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
