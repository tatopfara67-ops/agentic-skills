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
Exit 0 = PASS. Exit 1 = violations listed. Fix the work, not the auditor.
"""
from __future__ import annotations

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

    # 2/3/5/6. block-level contracts
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
        if line.startswith("### "):
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
