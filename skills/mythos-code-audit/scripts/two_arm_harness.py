#!/usr/bin/env python3
"""
mythos-code-audit v1.0.0 — Two-Arm Differential Harness (template)
====================================================================

Instrument skeleton for Phase 4 oracle construction (SKILL.md §5, §11;
references/differential-oracles.md). The calibration engagement
(example/worked-example.md) ran a target-specific version of this file.

Design contract — keep ALL of these when you specialize it:

  1. One script, two arms. The SAME file runs under the vulnerable and the
     fixed environment; never fork a per-arm copy (arm drift, bug #3 in
     differential-oracles.md §9).
  2. Cells are isolated: a crash in one cell must not kill the matrix.
  3. Verdicts are classified, not eyeballed:
       VERIFIED — the behavior occurred (attack accepted)
       REJECTED — a security control fired (exception from the library)
       ERROR    — the instrument failed (environment rot) -> voids evidence
  4. Stability compares verdict + digit-normalized detail; timing jitter is
     not instability.
  5. A canary rides inside every forged input; a VERIFIED line is then also
     a canary round-trip (SKILL.md §8).
  6. Every treatment cell names its hypothesis (H-NNN) in the docstring and
     states its falsifier.
  7. Regression control cells run on BOTH arms; treatment results without a
     green control are void.

Usage:
    <vulnerable-venv-python> two_arm_harness.py --runs 3 | tee transcript_vuln.txt
    <fixed-venv-python>      two_arm_harness.py --runs 3 | tee transcript_fixed.txt
"""

import argparse
import hashlib
import re
import sys
import time

CANARY = "MYTHOS-CANARY-00000000"  # replace: 8 hex chars, chosen in Phase 0

CELLS = []


def cell(name):
    def deco(fn):
        CELLS.append((name, fn))
        return fn
    return deco


INSTRUMENT_FAILURES = (AttributeError, ImportError, ModuleNotFoundError)


def _classify(exc):
    """REJECTED = control fired; ERROR = instrument failed. Never conflate."""
    if isinstance(exc, INSTRUMENT_FAILURES):
        return "ERROR"
    msg = str(exc)
    if "module 'lib'" in msg or "no attribute" in msg or "backend" in msg.lower():
        return "ERROR"
    return "REJECTED"


def arm_id():
    """Print package + dependency versions: provenance lives in the transcript."""
    versions = {}
    for mod in ("jose", "jwt", "cryptography", "flask", "django"):  # replace with your target
        try:
            m = __import__(mod)
            versions[mod] = getattr(m, "__version__", "?")
        except ImportError:
            continue
    return " ".join(f"{k}=={v}" for k, v in versions.items()) or f"python=={sys.version.split()[0]}"


# ---------------------------------------------------------------- cells ----
# REPLACE the demo cells below with your target's cells. Demo cells show the
# required shapes: treatment + regression control, both arms, falsifiers.

@cell("T1 TREATMENT-DEMO")
def t1():
    """H-001 demo treatment. Falsifier: fixed arm raises a control error
    while the regression control E1 stays green on both arms."""
    # forge the attack input; CANARY must ride inside it
    attack_input = {"role": "admin", "canary": CANARY}  # ... build the real input
    result = attack_input  # ... execute against the target entry point
    return f"accepted, canary={result.get('canary')}"


@cell("E1 REGRESSION-CONTROL-DEMO")
def e1():
    """Regression control for T1: the legitimate flow must stay green on
    BOTH arms, or T1's evidence is void."""
    legit_input = {"role": "user", "canary": CANARY}  # ... build the real input
    result = legit_input  # ... execute the legitimate flow
    return f"accepted, canary={result.get('canary')} (legit flow intact)"


# ---------------------------------------------------------------- runner ---
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=3,
                    help="floor is 3 for deterministic cells; 20 for stochastic")
    args = ap.parse_args()

    print(f"# ARM {arm_id()}")
    print(f"# CANARY {CANARY} sha256={hashlib.sha256(CANARY.encode()).hexdigest()[:16]}")
    summary = {}
    for name, fn in CELLS:
        results = []
        for i in range(1, args.runs + 1):
            t0 = time.perf_counter()
            try:
                detail = fn()
                verdict = "VERIFIED"
            except Exception as exc:  # noqa: BLE001 — the oracle records the control firing
                detail = f"{type(exc).__name__}: {exc}"
                verdict = _classify(exc)
            ms = (time.perf_counter() - t0) * 1000
            results.append((verdict, detail))
            print(f"R-LAB | {name} | run {i}/{args.runs} | {verdict} | {detail} | {ms:.0f}ms")
        verdicts = {v for v, _ in results}
        details = {re.sub(r"\d+", "N", d) for _, d in results}
        stable = len(verdicts) == 1 and len(details) == 1
        v = verdicts.pop() if len(verdicts) == 1 else "MIXED"
        print(f"SUMMARY | {name} | {args.runs}/{args.runs} {v} | {'STABLE' if stable else 'UNSTABLE'}")
        summary[name] = stable
    print(f"# END runs={args.runs} cells={len(CELLS)} all_stable={all(summary.values())}")
    # The trailer line must read all_stable=True before transcripts are citable.


if __name__ == "__main__":
    main()
