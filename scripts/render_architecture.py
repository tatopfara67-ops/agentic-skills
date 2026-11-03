#!/usr/bin/env python3
"""Render docs/mythos-arsenal-arsitektur.png — the repo architecture
diagram (three panels: stack anatomy / session flow / always-on rails).

Re-run after any organ addition or tier change:
    python3 scripts/render_architecture.py

Kept as a persisted script so the diagram is regenerable from source
data instead of being a one-off artifact. Layout is computed top-down
with an overlap assertion so panels can never silently collide.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

matplotlib.rcParams["font.family"] = "DejaVu Sans"

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
        "cloud-config-auditor", "mobile-hunter", "cache-playbook",
        "prototype-playbook"]),
    ("Tier 4 — Incident Branch", [
        "adversary-tracker (Binary Brain, event-triggered)"]),
    ("Tier 5 — Craft Lineages", [
        "scan-economist", "module-smith", "pipeline-smith",
        "feedback-fuzzer", "template-scanner", "packet-orchestrator",
        "protocol-forensics"]),
    ("Tier 6 — Legend Tier", [
        "chain-architect", "desync-hunter", "deep-teardown",
        "ghost-crawler", "mirror-hunter", "signal-smith",
        "trust-graph-hunter"]),
    ("Tier 7 — Forge & Competition", [
        "lineage-smith", "rival-playbook"]),
]
NEW_ORGANS = {"lineage-smith", "rival-playbook", "protocol-forensics"}
N_ORGANS = sum(len(o) for _, o in TIERS)          # 32 organs (30 hunting + 2 forge)
N_BUNDLES = 38
N_TOOLS = 27
N_TESTS = 137

BOXES = []  # (x0, y0, x1, y1) registry per panel for the overlap check


def begin_panel():
    del BOXES[:]


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
    BOXES.append((x, y, x + w, y + h))


def arrow(ax, x0, y0, x1, y1):
    ax.add_patch(FancyArrowPatch(
        (x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=16,
        linewidth=1.6, color=ACCENT, zorder=1))


def assert_no_overlap():
    for i in range(len(BOXES)):
        for j in range(i + 1, len(BOXES)):
            a, b = BOXES[i], BOXES[j]
            if (a[0] < b[2] and b[0] < a[2] and
                    a[1] < b[3] and b[1] < a[3]):
                raise SystemExit("OVERLAP between boxes %r and %r"
                                 % (a, b))


def main():
    fig = plt.figure(figsize=(13.8, 34.4), dpi=200, facecolor=PAPER)
    gs = fig.add_gridspec(3, 1, height_ratios=[14, 10.5, 9.9],
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
    begin_panel()
    ax1.text(0.5, 0.985, "MYTHOS-ARSENAL — STACK ANATOMY",
             ha="center", va="top", fontsize=17, weight="bold", color=INK)
    ax1.text(0.5, 0.955,
             "charter → engine → spine → %d organs → the execution hand"
             "   ·   %d bundles   ·   %d tools   ·   %d tests"
             % (N_ORGANS, N_BUNDLES, N_TOOLS, N_TESTS),
             ha="center", va="top", fontsize=10.5, color=GREY)

    box(ax1, 0.18, 0.848, 0.64, 0.052, "skill-mythos — THE CHARTER",
        CHARTER, fs=13, bold=True,
        sub="fifteen articles · A13 escalation · A14 WWH registers · "
            "A15 war logic · autonomy · quality gates")
    box(ax1, 0.18, 0.770, 0.64, 0.052, "glm-self-model — THE ENGINE MANUAL",
        ENGINE, fs=13, bold=True,
        sub="five truths · failure geometry E1–E8 · compensation gates "
            "G1–G4 · written to the engine, not the operator")
    box(ax1, 0.18, 0.692, 0.64, 0.052,
        "mythos-bug-hunter v4.5.0 — THE SPINE", SPINE, fs=13, bold=True,
        sub="R0–R7 canon · append-only R-NNN ledger · hypothesis grammar "
            "· closure gates · mission horizon")
    arrow(ax1, 0.5, 0.848, 0.5, 0.826)
    arrow(ax1, 0.5, 0.770, 0.5, 0.748)
    arrow(ax1, 0.5, 0.692, 0.5, 0.670)

    # tier rows: organ chips (computed top-down, no overlap possible)
    chip_h = 0.030
    step = 0.040
    tier_gap = 0.030
    y = 0.645                      # bottom of each tier's first chip row
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
            yy = y - r * step
            xx = x0 + c * cw
            box(ax1, xx, yy, cw * 0.94, chip_h, organ, SLATE, fs=8.2,
                accent=organ in NEW_ORGANS)
        y = y - (rows - 1) * step - tier_gap - chip_h
        if tier_name.startswith("Tier 4"):
            y += 0.010
    last_bottom = y + tier_gap + chip_h  # bottom edge of final chip row

    hand_y = 0.037
    box(ax1, 0.18, hand_y, 0.64, 0.075,
        "THE EXECUTION HAND", HAND, fs=13, bold=True,
        sub="arsenal/ MCP server — %d scope-gated tools (R0 deny-by-default)"
            " · auditor/ PASS-FAIL report gate · lab/ self-owned targets"
            " · agent/ARCHITECTURE.md ten-layer agent" % N_TOOLS)
    arrow(ax1, 0.5, last_bottom, 0.5, hand_y + 0.075)
    ax1.text(0.035, hand_y + 0.012, "orange border = newest wave",
             ha="left", va="center", fontsize=8.5, color=ACCENT,
             style="italic")

    # ================= panel 2 — session flow ==========================
    assert_no_overlap()          # panel 1 closed — check before clearing
    begin_panel()
    ax2.text(0.5, 0.985, "SESSION FLOW", ha="center", va="top",
             fontsize=17, weight="bold", color=INK)
    ax2.text(0.5, 0.962, "every operator instruction, however terse, "
                         "becomes an explicit doctrine order before any "
                         "organ acts",
             ha="center", va="top", fontsize=10.5, color=GREY)

    flow = [
        ("A13 · doctrine_forge", "terse operator line (any language) → "
         "intent · phase plan · war logic W1–W7 · gates", CHARTER),
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
    y = 0.838
    h = 0.095
    for i, (title, sub, fill) in enumerate(flow):
        box(ax2, 0.14, y, 0.72, h, title, fill, fs=12.5, bold=True,
            sub=sub)
        if i < len(flow) - 1:
            arrow(ax2, 0.5, y, 0.5, y - 0.045)
        y -= h + 0.045

    # ================= panel 3 — always-on rails ========================
    assert_no_overlap()          # panel 2 closed — check before clearing
    begin_panel()
    ax3.text(0.5, 0.985, "ALWAYS-ON RAILS", ha="center", va="top",
             fontsize=17, weight="bold", color=INK)
    ax3.text(0.5, 0.962, "the constraints that ride along every step of "
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
        ("THREE REGISTERS (A14)", "every organ states WHAT the class is, "
         "WHY the bug lives where it lives, HOW it is hunted — a "
         "technique missing a register is not shipped"),
        ("WAR LOGIC (A15)", "W1 spies before armies · W2 win without "
         "fighting · W3 strike weakness · W4 cheng + ch'i · W5 shih · "
         "W6 sovereign sets intent · W7 no prolonged war"),
    ]
    h = 0.125
    for i, (title, sub) in enumerate(rails):
        yy = 0.805 - (i // 2) * 0.19
        xx = 0.06 if i % 2 == 0 else 0.52
        box(ax3, xx, yy, 0.42, h, title, SLATE, fs=11.5, bold=True,
            sub=sub)
    box(ax3, 0.06, 0.02, 0.88, 0.105,
        "THE ONE THESIS (agent/ARCHITECTURE.md)", HAND, fs=12.5,
        bold=True,
        sub="the LLM is the least trusted component — every layer exists "
            "to catch it when it hallucinates; the repo is the only self "
            "this agent has")

    assert_no_overlap()
    fig.savefig(OUT, dpi=200, facecolor=PAPER)
    plt.close(fig)
    print("wrote %s (%d organs, %d bundles, %d tools, %d tests)"
          % (OUT, N_ORGANS, N_BUNDLES, N_TOOLS, N_TESTS))


if __name__ == "__main__":
    main()
