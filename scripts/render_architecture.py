#!/usr/bin/env python3
"""Render docs/mythos-arsenal-arsitektur.png — the repo architecture
diagram (three panels: stack anatomy / session flow / always-on rails).

Re-run after any organ addition or tier change:
    python3 scripts/render_architecture.py

Kept as a persisted script so the diagram is regenerable from source
data instead of being a one-off artifact.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO_ROOT, "docs", "mythos-arsenal-arsitektur.png")

# ---- palette (muted, print-grade) -----------------------------------------
INK = "#1e2430"        # primary text / box borders
PAPER = "#f7f5f0"      # background
SLATE = "#e8e4db"      # organ fill
CHARTER = "#dfd6c3"    # charter fill
ENGINE = "#d8e0e8"     # engine fill
SPINE = "#d4dce4"      # spine fill
HAND = "#e2d9c8"       # execution-hand fill
ACCENT = "#b3541e"     # new-organ / flow accent
GREY = "#5a6473"

TIERS = [
    ("Tier 1 — Recon & Mapping", [
        "surface-cartographer", "subdomain-hunter", "content-discovery",
        "js-recon", "api-surface-mapper"]),
    ("Tier 2 — Access & Logic", [
        "auth-boundary-mapper", "oauth-flow-auditor",
        "business-logic-hunter"]),
    ("Tier 3 — Deep Technical", [
        "injection-lab", "ssrf-playbook", "xss-playbook",
        "cloud-config-auditor"]),
    ("Tier 4 — Incident Branch", [
        "adversary-tracker (Binary Brain, event-triggered)"]),
    ("Tier 5 — Craft Lineages", [
        "scan-economist", "module-smith", "pipeline-smith",
        "feedback-fuzzer", "template-scanner", "packet-orchestrator"]),
    ("Tier 6 — Legend Tier", [
        "chain-architect", "desync-hunter", "deep-teardown",
        "ghost-crawler", "mirror-hunter", "signal-smith",
        "trust-graph-hunter"]),
]
NEW_ORGANS = {"mirror-hunter"}
N_ORGANS = 28  # tiers 0-6 incl. charter + engine
N_BUNDLES = 32
N_TOOLS = 27
N_TESTS = 105


def box(ax, x, y, w, h, text, fill, fs=11, bold=False, accent=False,
        sub=None):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.014",
        linewidth=2.0 if accent else 1.2,
        edgecolor=ACCENT if accent else INK, facecolor=fill, zorder=2))
    weight = "bold" if (bold or accent) else "normal"
    if sub:
        ax.text(x + w / 2, y + h * 0.62, text, ha="center", va="center",
                fontsize=fs, color=INK, weight=weight, zorder=3)
        ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center",
                fontsize=fs - 2.5, color=GREY, zorder=3)
    else:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=fs, color=INK, weight=weight, zorder=3)


def arrow(ax, x0, y0, x1, y1, label=None, lx=0.0, ly=0.0):
    ax.add_patch(FancyArrowPatch(
        (x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=16,
        linewidth=1.6, color=ACCENT, zorder=1))
    if label:
        ax.text((x0 + x1) / 2 + lx, (y0 + y1) / 2 + ly, label,
                ha="center", va="center", fontsize=9, color=GREY,
                style="italic", zorder=3)


def main():
    fig = plt.figure(figsize=(13.8, 34.4), dpi=200, facecolor=PAPER)
    gs = fig.add_gridspec(3, 1, height_ratios=[14, 10.5, 8.4],
                          hspace=0.06)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    ax3 = fig.add_subplot(gs[2])
    for ax in (ax1, ax2, ax3):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_facecolor(PAPER)

    # ================= panel 1 — stack anatomy =========================
    ax1.text(0.5, 0.985, "MYTHOS-ARSENAL — STACK ANATOMY",
             ha="center", va="top", fontsize=17, weight="bold", color=INK)
    ax1.text(0.5, 0.955,
             "charter → engine → spine → 27 organs → the execution hand"
             "   ·   %d bundles   ·   %d tools   ·   %d tests"
             % (N_BUNDLES, N_TOOLS, N_TESTS),
             ha="center", va="top", fontsize=10.5, color=GREY)

    box(ax1, 0.18, 0.875, 0.64, 0.052, "skill-mythos — THE CHARTER",
        CHARTER, fs=13, bold=True,
        sub="thirteen articles · A13 prompt escalation · autonomy "
            "protocol · quality gates")
    box(ax1, 0.18, 0.795, 0.64, 0.052, "glm-self-model — THE ENGINE MANUAL",
        ENGINE, fs=13, bold=True,
        sub="five truths · failure geometry E1–E8 · compensation gates "
            "G1–G4 · written to the engine, not the operator")
    box(ax1, 0.18, 0.715, 0.64, 0.052,
        "mythos-bug-hunter v4.5.0 — THE SPINE", SPINE, fs=13, bold=True,
        sub="R0–R7 canon · append-only R-NNN ledger · hypothesis grammar "
            "· closure gates · mission horizon")
    arrow(ax1, 0.5, 0.875, 0.5, 0.847)
    arrow(ax1, 0.5, 0.795, 0.5, 0.767)
    arrow(ax1, 0.5, 0.715, 0.5, 0.692)

    # tier rows: organ chips
    y = 0.645
    chip_h = 0.034
    for tier_name, organs in TIERS:
        ax1.text(0.035, y + chip_h / 2, tier_name, ha="left", va="center",
                 fontsize=10.5, color=INK, weight="bold")
        n = len(organs)
        cols = min(n, 4)
        rows = (n + cols - 1) // cols
        area_w = 0.62
        x0 = 0.34
        cw = area_w / cols
        for i, organ in enumerate(organs):
            r, c = divmod(i, cols)
            # reverse rows so first row is on top
            yy = y - r * (chip_h + 0.014)
            xx = x0 + c * cw
            box(ax1, xx, yy, cw * 0.94, chip_h, organ, SLATE, fs=8.2,
                accent=organ in NEW_ORGANS)
        y = y - rows * (chip_h + 0.014) - 0.052
        if tier_name.startswith("Tier 4"):
            y += 0.028

    box(ax1, 0.18, 0.035, 0.64, 0.075,
        "THE EXECUTION HAND", HAND, fs=13, bold=True,
        sub="arsenal/ MCP server — %d scope-gated tools (R0 deny-by-default)"
            " · auditor/ PASS-FAIL report gate · lab/ self-owned targets"
            " · agent/ARCHITECTURE.md ten-layer agent" % N_TOOLS)
    arrow(ax1, 0.5, 0.095, 0.5, 0.11)

    # ================= panel 2 — session flow ==========================
    ax2.text(0.5, 0.985, "SESSION FLOW", ha="center", va="top",
             fontsize=17, weight="bold", color=INK)
    ax2.text(0.5, 0.955, "every operator instruction, however terse, "
                         "becomes an explicit doctrine order before any "
                         "organ acts",
             ha="center", va="top", fontsize=10.5, color=GREY)

    flow = [
        ("A13 · doctrine_forge", "terse operator line (any language) → "
         "intent · persona mix · phase plan · gates", CHARTER),
        ("R0 · SCOPE GATE", "scope.csv, deny-by-default — every network "
         "tool checks before a byte leaves", SPINE),
        ("THE HUNT LOOP · F0–F4", "map → hypothesize (pre-registered) → "
         "test (differential triads) → impact (canary ladder) → close "
         "(CONFIRMED / FALSIFIED / INCONCLUSIVE)", SLATE),
        ("INCIDENT BRANCH (event-triggered)", "adversary-tracker Binary "
         "Brain: freeze → halve by bits → two-channel fix → audited "
         "handoff — then the loop resumes", ENGINE),
        ("REPORT GATES", "write from ledger records only · CVSS 3.1 "
         "recomputed · VRT + H1 crosswalk · auditor exit 0 or it does "
         "not ship", HAND),
        ("INSTINCT CALIBRATION", "trained-eye cue catalog scored per "
         "engagement — instinct is a measurable asset, recalibrated at "
         "close", SLATE),
    ]
    y = 0.86
    h = 0.095
    for i, (title, sub, fill) in enumerate(flow):
        box(ax2, 0.14, y, 0.72, h, title, fill, fs=12.5, bold=True,
            sub=sub)
        if i < len(flow) - 1:
            arrow(ax2, 0.5, y, 0.5, y - 0.045)
        y -= h + 0.045

    # ================= panel 3 — always-on rails ========================
    ax3.text(0.5, 0.985, "ALWAYS-ON RAILS", ha="center", va="top",
             fontsize=17, weight="bold", color=INK)
    ax3.text(0.5, 0.955, "the constraints that ride along every step of "
                         "every engagement",
             ha="center", va="top", fontsize=10.5, color=GREY)

    rails = [
        ("EVIDENCE", "append-only R-NNN ledger — no claim without a "
         "record; bodies stay out of context; records beat memory"),
        ("CALIBRATION", "differential triad on every claim — baseline / "
         "treatment / control; rates over N runs on stochastic "
         "surfaces"),
        ("IMPACT", "canary proofs on self-owned objects only — one "
         "end-to-end demonstration, then stop"),
        ("ECONOMY", "R7 budgets, priced sweeps, exit numbers (R6) — "
         "'done' without numbers is a forbidden state"),
        ("ENGINE GATES", "G1 fresh-eyes re-derivation before CONFIRMED · "
         "G2 edges for critical state · G3 first-written priors · "
         "G4 queue over decibels"),
        ("MISSION HORIZON", "a quota is a continuation mandate — it ends "
         "only by exhaustion proof or operator release; context "
         "exhaustion is a pause"),
    ]
    y = 0.83
    h = 0.105
    for i, (title, sub) in enumerate(rails):
        yy = y - (i // 2) * (h + 0.05)
        xx = 0.06 if i % 2 == 0 else 0.52
        box(ax3, xx, yy, 0.42, h, title, SLATE, fs=11.5, bold=True,
            sub=sub)
    box(ax3, 0.06, 0.03, 0.88, 0.11,
        "THE ONE THESIS (agent/ARCHITECTURE.md)", HAND, fs=12.5,
        bold=True,
        sub="the LLM is the least trusted component — every layer exists "
            "to catch it when it hallucinates; the repo is the only self "
            "this agent has")

    fig.savefig(OUT, dpi=200, facecolor=PAPER)
    plt.close(fig)
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
