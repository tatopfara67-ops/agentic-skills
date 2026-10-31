#!/usr/bin/env python3
"""
mythos-code-audit v1.0.0 — White-Box Report Auditor
=====================================================

Mechanical slop detector for code-audit reports produced under this skill.
Extends the mythos-bug-hunter v4.1.0 auditor with the white-box checks of
the Report Contract (SKILL.md §13):

  R3/R4   no ungated victory language, no hedging slop; severity lines cite R-NNN
  §13.2   CONFIRMED blocks carry a versioned code anchor, n_runs, and
          per-arm runtime evidence (VERIFIED + REJECTED)
  §13.3   crypto findings name their CLASS-NN (crypto-misuse-catalog.md)
  §13.4   CVE/diff-derived claim lines cite the ledger
  §13.5   CONFIRMED findings ship a mitigation boundary section
  §13.7   INCONCLUSIVE blocks carry a Park ID (P-NNN)
  §13.2   regression control section present when anything is CONFIRMED

Design notes (honest limits):
- The auditor checks SYNTAX, not truth. The ledger remains the ground truth.
- Headings are exempt from citation checks, never from phrase checks.
- Exit code 0 = shippable; exit code 1 = violations listed on stdout.

Usage:
    python3 audit_code_report.py <report.md>
    python3 audit_code_report.py example/worked-example.md             # positive control
    python3 audit_code_report.py example/sloppy-code-report-fixture.md # negative control
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
    (re.compile(r"\bseems (vulnerable|exploitable)\b", re.I), "non-vocabulary state — use Closure terms (Canon R4)"),
    (re.compile(r"\blooks (vulnerable|exploitable|dangerous)\b", re.I), "non-vocabulary state — use Closure terms (Canon R4)"),
    (re.compile(r"\bi (think|believe)\b", re.I), "opinion — evidence decides, not the agent (Canon R4)"),
    (re.compile(r"should be tested further", re.I), "deferred work — park it formally (Canon R2/R7)"),
    (re.compile(r"\bTODO\b|\bFIXME\b|\bXXX\b|【"), "leftover placeholder"),
]

SEVERITY = re.compile(
    r"\b(critical|high|medium|low|severity|vulnerable|exploitable|exposed|exposure|"
    r"bypass|unauthorized|unauthenticated|remote code execution|rce|ssrf|xss|sqli|"
    r"sql injection|privilege escalation|confusion|forged|forgery|denial of service|"
    r"resource consumption)\b",
    re.I,
)
CRYPTO_LINE = re.compile(
    r"\b(jwt|jws|jwe|hmac|cipher|crypto|cryptographic|algorithm confusion|key[- ]type)\b",
    re.I,
)
CITE = re.compile(r"R-\d{1,4}")
CVE_LINE = re.compile(r"CVE-\d{4}-\d{4,7}")
CLOSURE = re.compile(r"Closure:\s*(CONFIRMED|FALSIFIED|INCONCLUSIVE)\b")
HYP_HEAD = re.compile(r"^#{2,4}\s*H-\d+", re.M)
N_RUNS = re.compile(r"n_runs\s*[:=]\s*(\d+)")
CODE_ANCHOR = re.compile(
    r"[\w./-]+\.(py|js|ts|tsx|java|go|rb|php|c|cpp|cc|h|rs|cs|kt):\d+@\d+\.\d+[\w.]*"
)
CLASS_REF = re.compile(r"CLASS-\d{2}\b")
PARK_ID = re.compile(r"\bP-\d{3}\b")
CANARY = re.compile(r"canary", re.I)
IMPACT_CHAIN = re.compile(r"impact chain", re.I)
MITIGATION = re.compile(r"mitigation boundary", re.I)
REGRESSION_CTRL = re.compile(r"regression control", re.I)


def audit(path: str):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()
    violations = []

    # Fenced code blocks are quoted artifacts (transcripts, ledger records,
    # diff hunks) — verbatim instrument output, not authored prose. They are
    # exempt from the per-line claim checks; the structural H-block checks
    # below still see them.
    def _authored(line, state):
        if line.lstrip().startswith("```"):
            state[0] = not state[0]
            return False
        return not state[0]

    fence = [False]

    # --- Check 1: forbidden phrases (authored lines, headings included) ---
    for i, line in enumerate(lines, 1):
        if not _authored(line, fence):
            continue
        for pat, why in FORBIDDEN:
            m = pat.search(line)
            if m:
                violations.append((i, "forbidden-phrase", f"{why}: …{m.group(0)}…"))

    # --- Check 2: severity-bearing claim lines without a citation ---
    claim_lines = 0
    fence = [False]
    for i, line in enumerate(lines, 1):
        if not _authored(line, fence):
            continue
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if SEVERITY.search(line) and not CITE.search(line):
            violations.append((i, "uncited-claim", line.strip()[:90]))
        elif SEVERITY.search(line):
            claim_lines += 1

    # --- Check 3: crypto findings must name their CLASS-NN ---
    fence = [False]
    for i, line in enumerate(lines, 1):
        if not _authored(line, fence):
            continue
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if SEVERITY.search(line) and CRYPTO_LINE.search(line) and not CLASS_REF.search(line):
            violations.append((i, "crypto-no-class",
                               "crypto-domain claim without CLASS-NN (crypto-misuse-catalog.md)"))

    # --- Check 4: CVE/diff-derived claims must cite the ledger ---
    fence = [False]
    for i, line in enumerate(lines, 1):
        if not _authored(line, fence):
            continue
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if CVE_LINE.search(line) and not CITE.search(line):
            violations.append((i, "diff-no-cite",
                               "diff-derived claim line without an R-NNN citation"))

    # --- Check 5: hypothesis blocks — Closure, anchors, n_runs, parks ---
    hyp_count = 0
    closures = {"CONFIRMED": 0, "FALSIFIED": 0, "INCONCLUSIVE": 0}
    heads = list(re.finditer(r"^#{2,4}\s*H-\d+.*$", text, flags=re.M))
    for idx, m in enumerate(heads):
        block = text[m.start(): heads[idx + 1].start() if idx + 1 < len(heads) else len(text)]
        start_line = text.count("\n", 0, m.start()) + 1
        hyp_count += 1
        head = block.splitlines()[0].strip()
        c = CLOSURE.search(block)
        if not c:
            violations.append((start_line, "no-closure", f"{head} — missing Closure line"))
            continue
        closures[c.group(1)] += 1
        if c.group(1) == "CONFIRMED":
            if not CODE_ANCHOR.search(block):
                violations.append((start_line, "no-code-anchor",
                                   f"{head} — CONFIRMED without a versioned code anchor (file.py:LINE@version)"))
            if not N_RUNS.search(block):
                violations.append((start_line, "no-n-runs",
                                   f"{head} — CONFIRMED without n_runs"))
            elif int(N_RUNS.search(block).group(1)) < 3:
                violations.append((start_line, "n-runs-below-floor",
                                   f"{head} — CONFIRMED with n_runs < 3 (deterministic floor)"))
            if not (re.search(r"VERIFIED", block) and re.search(r"REJECTED", block)):
                violations.append((start_line, "no-arm-evidence",
                                   f"{head} — CONFIRMED without per-arm runtime evidence (VERIFIED + REJECTED)"))
        if c.group(1) == "INCONCLUSIVE" and not PARK_ID.search(block):
            violations.append((start_line, "no-park-id",
                               f"{head} — INCONCLUSIVE without a Park ID (P-NNN)"))

    # --- Check 6: report-level requirements when findings are CONFIRMED ---
    if closures["CONFIRMED"] > 0:
        if not CANARY.search(text):
            violations.append((0, "no-canary", "CONFIRMED finding(s) without a canary reference (SKILL.md §8)"))
        if not IMPACT_CHAIN.search(text):
            violations.append((0, "no-impact-chain", "CONFIRMED finding(s) without an impact chain (SKILL.md §8)"))
        if not MITIGATION.search(text):
            violations.append((0, "no-mitigation-boundary",
                               "CONFIRMED finding(s) without a mitigation boundary section (SKILL.md §13.5)"))
        if not REGRESSION_CTRL.search(text):
            violations.append((0, "no-regression-control",
                               "CONFIRMED finding(s) without a regression control reference (SKILL.md §13.2)"))

    # --- Report ---
    print(f"audit_code_report.py — {path}")
    print(f"  hypothesis blocks : {hyp_count}  (confirmed {closures['CONFIRMED']}, "
          f"falsified {closures['FALSIFIED']}, inconclusive {closures['INCONCLUSIVE']})")
    print(f"  cited claim lines : {claim_lines}")
    if violations:
        print(f"\n  FAIL — {len(violations)} violation(s):")
        for lineno, kind, detail in violations:
            where = f"line {lineno}" if lineno else "file level"
            print(f"    [{kind:22s}] {where}: {detail}")
        return 1
    print("\n  PASS — report satisfies the White-Box Report Contract. Ship it.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Mechanical slop auditor for mythos-code-audit reports.")
    ap.add_argument("report", help="path to the markdown report to audit")
    args = ap.parse_args()
    sys.exit(audit(args.report))


if __name__ == "__main__":
    main()
