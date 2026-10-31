#!/usr/bin/env python3
"""
mythos-bug-hunter v4.1.0 — Report Auditor
=========================================

Mechanical slop detector for vulnerability reports produced under this skill.
Enforces the Report Contract (SKILL.md §13) of the Canon:

  R3  no ungated victory language, no hedging slop
  R4  every claim line cites a ledger record R-NNN
  §7  every hypothesis block reaches a Closure (CONFIRMED/FALSIFIED/INCONCLUSIVE)
  §6  confirmed findings show reproduction counts (n_runs / attempts)
  §8  confirmed findings with severity show an impact chain and a canary

Design notes (honest limits):
- The auditor checks SYNTAX, not truth. The ledger remains the ground truth.
- Heading lines (starting with '#') are treated as labels, not claims, and are
  exempt from the citation check — but NOT from the forbidden-phrase check.
- Exit code 0 = report is shippable; exit code 1 = violations listed on stdout.

Usage:
    python3 audit_report.py <report.md>
    python3 audit_report.py example/worked-example.md     # positive control
    python3 audit_report.py example/sloppy-report-fixture.md  # negative control
"""

import argparse
import re
import sys

FORBIDDEN = [
    (re.compile(r"\bjackpot\b", re.I), "victory language without a gated Closure (Canon R3)"),
    (re.compile(r"\bbreakthrough\b", re.I), "victory language without a gated Closure (Canon R3)"),
    (re.compile(r"\bbingo\b", re.I), "victory language without a gated Closure (Canon R3)"),
    (re.compile(r"\bmight be\b", re.I), "hedging — pre-register a hypothesis instead (Canon R4)"),
    (re.compile(r"\bmay be\b", re.I), "hedging — pre-register a hypothesis instead (Canon R4)"),
    (re.compile(r"\bmaybe\b", re.I), "hedging — pre-register a hypothesis instead (Canon R4)"),
    (re.compile(r"\bcould (be|potentially)\b", re.I), "hedging — pre-register a hypothesis instead (Canon R4)"),
    (re.compile(r"\bpotentially\b", re.I), "hedging — pre-register a hypothesis instead (Canon R4)"),
    (re.compile(r"\bpossibly\b", re.I), "hedging — pre-register a hypothesis instead (Canon R4)"),
    (re.compile(r"\bprobably\b", re.I), "hedging — pre-register a hypothesis instead (Canon R4)"),
    (re.compile(r"\bappears to\b", re.I), "hedging — state the observation with a record ID (Canon R4)"),
    (re.compile(r"\bseems to\b", re.I), "hedging — state the observation with a record ID (Canon R4)"),
    (re.compile(r"\bi (think|believe)\b", re.I), "opinion — evidence decides, not the agent (Canon R4)"),
    (re.compile(r"should be tested further", re.I), "deferred work — park it formally (Canon R2/R7)"),
    (re.compile(r"\bTODO\b|\bFIXME\b|\bXXX\b|【"), "leftover placeholder"),
]

SEVERITY = re.compile(
    r"\b(critical|high|medium|low|severity|vulnerable|exploitable|exposed|exposure|"
    r"bypass|unauthorized|unauthenticated|remote code execution|rce|ssrf|xss|sqli|"
    r"sql injection|privilege escalation)\b",
    re.I,
)
CITE = re.compile(r"R-\d{1,4}")
CLOSURE = re.compile(r"Closure:\s*(CONFIRMED|FALSIFIED|INCONCLUSIVE)\b")
HYP_HEAD = re.compile(r"^#{2,4}\s*H-\d+", re.M)
N_RUNS = re.compile(r"n_runs\s*[:=]\s*\d+")
CANARY = re.compile(r"canary", re.I)
IMPACT_CHAIN = re.compile(r"impact chain", re.I)


def audit(path: str):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()
    violations = []

    # --- Check 1: forbidden phrases (all lines, headings included) ---
    for i, line in enumerate(lines, 1):
        for pat, why in FORBIDDEN:
            m = pat.search(line)
            if m:
                violations.append((i, "forbidden-phrase", f"{why}: …{m.group(0)}…"))

    # --- Check 2: claim lines without a citation (non-heading lines) ---
    claim_lines = 0
    for i, line in enumerate(lines, 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if SEVERITY.search(line) and not CITE.search(line):
            violations.append((i, "uncited-claim", line.strip()[:90]))
        elif SEVERITY.search(line):
            claim_lines += 1

    # --- Check 3: hypothesis blocks must reach Closure ---
    hyp_blocks = re.split(r"(?=^#{2,4}\s*H-\d+)", text, flags=re.M)
    hyp_count = 0
    closures = {"CONFIRMED": 0, "FALSIFIED": 0, "INCONCLUSIVE": 0}
    for block in hyp_blocks[1:]:
        hyp_count += 1
        head = block.splitlines()[0].strip()
        m = CLOSURE.search(block)
        if not m:
            violations.append((text[: block].count("\n") + 1, "no-closure", f"{head} — missing Closure line"))
        else:
            closures[m.group(1)] += 1

    # --- Check 4: reproduction counts for confirmed findings ---
    n_runs_count = len(N_RUNS.findall(text))
    if closures["CONFIRMED"] > 0 and n_runs_count < closures["CONFIRMED"]:
        violations.append((0, "missing-reproduction",
                           f"{closures['CONFIRMED']} CONFIRMED closure(s) but only {n_runs_count} n_runs field(s)"))

    # --- Check 5: impact chain + canary for confirmed+severe findings ---
    if closures["CONFIRMED"] > 0 and claim_lines > 0:
        if not CANARY.search(text):
            violations.append((0, "no-canary", "CONFIRMED finding(s) without a canary reference (SKILL.md §8)"))
        if not IMPACT_CHAIN.search(text):
            violations.append((0, "no-impact-chain", "CONFIRMED finding(s) without an impact chain (SKILL.md §8)"))

    # --- Report ---
    print(f"audit_report.py — {path}")
    print(f"  hypothesis blocks : {hyp_count}  (confirmed {closures['CONFIRMED']}, "
          f"falsified {closures['FALSIFIED']}, inconclusive {closures['INCONCLUSIVE']})")
    print(f"  cited claim lines : {claim_lines}")
    print(f"  n_runs fields     : {n_runs_count}")
    if violations:
        print(f"\n  FAIL — {len(violations)} violation(s):")
        for lineno, kind, detail in violations:
            where = f"line {lineno}" if lineno else "file level"
            print(f"    [{kind:20s}] {where}: {detail}")
        return 1
    print("\n  PASS — report satisfies the Report Contract. Ship it.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Mechanical slop auditor for mythos-bug-hunter reports.")
    ap.add_argument("report", help="path to the markdown report to audit")
    args = ap.parse_args()
    sys.exit(audit(args.report))


if __name__ == "__main__":
    main()
