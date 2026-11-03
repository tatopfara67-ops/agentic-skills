#!/usr/bin/env python3
"""Reorder references/method-upgrade.md so the EXECUTABLE PROTOCOL leads.

Before:  title -> lineage intro -> 1. critique -> 2. upgrades -> 3. protocol
         -> 4. falsifiers -> 5. worked example
After:   title (method-first) -> 2-line directive intro -> 1. protocol
         -> 2. falsifiers -> 3. worked example -> 4. appendix critique
         -> 5. appendix upgrades (original lineage intro preserved there)

Every touched bundle gets a patch version bump (frontmatter + H1 title).
Run from repo root:  python3 scripts/reorder_method_upgrade.py
"""
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

# organ -> (protocol label, lineage person phrase for the appendix pointer)
META = {
    "adversary-tracker": ("M0–M5", "Shimomura's 1994–95 hunt"),
    "auth-boundary-mapper": ("M1–M5", "Frans Rosen's public practice"),
    "business-logic-hunter": ("M1–M5", "Soroush Dalili's public practice"),
    "cache-playbook": ("M1–M5", "Gil's and Kettle's published work"),
    "chain-architect": ("M1–M5", "Orange Tsai's published chains"),
    "cloud-config-auditor": ("M1–M5", "de la Fuente's Prowler practice"),
    "content-discovery": ("M1–M5", "Miessler's SecLists practice"),
    "deep-teardown": ("M1–M5", "Hotz's public teardowns"),
    "desync-hunter": ("M1–M4", "Kettle's desync research"),
    "feedback-fuzzer": ("M1–M5", "lcamtuf's fuzzing corpus"),
    "ghost-crawler": ("M1–M5", "the Lamo record"),
    "glm-self-model": ("M1–M5", "this engine's own calibration record"),
    "injection-lab": ("M1–M5", "the sqlmap-era tradition"),
    "interior-cartographer": ("M1–M6", "Forshaw's published interior work"),
    "lineage-smith": ("M1–M6", "the folk method and its worked example"),
    "mirror-hunter": ("M1–M5", "Willison's published prompt-injection wave"),
    "mobile-hunter": ("M1–M5", "Miller's and Mulliner's public research"),
    "module-smith": ("M1–M5", "HD Moore's module corpus"),
    "oauth-flow-auditor": ("M1–M5", "Parecki's OAuth practice"),
    "packet-orchestrator": ("M1–M5", "the Searle-era corpus"),
    "pipeline-smith": ("M1–M5", "Tomnomnom's toolmaking corpus"),
    "protocol-forensics": ("M1–M6", "Kaminsky's published DNS work"),
    "prototype-playbook": ("M1–M4", "Heyes' prototype-pollution research"),
    "rival-playbook": ("M1–M5", "the strategist tradition"),
    "scan-economist": ("M1–M5", "Fyodor's 1997 scan paper"),
    "signal-smith": ("M1–M5", "the Draper-era signal record"),
    "ssrf-playbook": ("M1–M5", "the Collaborator-era habit"),
    "subdomain-hunter": ("M1–M5", "EdOverflow's takeover corpus"),
    "template-scanner": ("M1–M5", "ProjectDiscovery's template practice"),
    "trust-graph-hunter": ("M1–M5", "the Mitnick record"),
    "xss-playbook": ("M1–M5", "the Heiderich–Heyes–Bentkowski corpus"),
}

SECTIONS = [
    "## 1. The critique",
    "## 2. The upgrades",
    "## 3. The executable protocol",
    "## 4. Falsifiers",
    "## 5. Worked micro-example",
]


def split_sections(text: str):
    """Return (intro, {prefix: section_text}) using the 5 known headings."""
    idx = []
    for pref in SECTIONS:
        m = re.search(r"(?m)^" + re.escape(pref) + r"[^\n]*\n", text)
        if not m:
            return None
        idx.append((m.start(), m.end(), pref))
    idx.sort()
    intro = text[: idx[0][0]].rstrip() + "\n"
    parts = {}
    for i, (s, e, pref) in enumerate(idx):
        end = idx[i + 1][0] if i + 1 < len(idx) else len(text)
        parts[pref] = text[s:end].rstrip() + "\n"  # includes own heading
    return intro, parts


def bump_version(skill_md: pathlib.Path, h1_old: str):
    """Patch-bump version in frontmatter + H1 title; return new version."""
    t = skill_md.read_text()
    m = re.search(r"(?m)^version:\s*(\d+)\.(\d+)\.(\d+)\s*$", t)
    if not m:
        raise SystemExit(f"no version in {skill_md}")
    major, minor, patch = map(int, m.groups())
    new = f"{major}.{minor}.{patch + 1}"
    t = re.sub(r"(?m)^version:.*$", f"version: {new}", t, count=1)
    t = re.sub(r"(?m)^(#\s+.+?)v\d+\.\d+\.\d+", rf"\g<1>v{new}", t, count=1)
    skill_md.write_text(t)
    return new


def main():
    report = []
    for organ, (proto, lineage) in META.items():
        mu = SKILLS / organ / "references" / "method-upgrade.md"
        skill_md = SKILLS / organ / "SKILL.md"
        text = mu.read_text()
        cut = split_sections(text)
        if cut is None:
            report.append(f"SKIP (section mismatch): {organ}")
            continue
        intro, parts = cut

        # 1) new method-first title
        old_title = intro.splitlines()[0]  # '# The method upgrade — ...'
        new_title = f"# The executable method — {proto} for {organ}"

        # 2) two-line directive intro
        directive = (
            f"{new_title}\n\n"
            "This file is the organ's executable method: numbered phases,\n"
            "exact record formats, thresholds, decision gates, and falsifiers,\n"
            "in run order. An agent that has never heard of any name in the\n"
            "appendix runs this at full precision. The lineage critique that\n"
            "justifies each step (why these phases exist, what was weak in\n"
            f"{lineage}) is preserved verbatim as the §4–§5 appendix.\n"
        )

        # 3) retitle the moved sections
        p3 = parts["## 3. The executable protocol"]
        p3 = re.sub(r"(?m)^## 3\. The executable protocol",
                    "## 1. The executable protocol", p3)
        p4 = parts["## 4. Falsifiers"]
        p4 = re.sub(r"(?m)^## 4\. Falsifiers", "## 2. Falsifiers", p4)
        p5 = parts["## 5. Worked micro-example"]
        p5 = re.sub(r"(?m)^## 5\. Worked micro-example",
                    "## 3. Worked micro-example", p5)
        p1 = parts["## 1. The critique"]
        p1 = re.sub(
            r"(?m)^## 1\. The critique(.*)$",
            r"## 4. Appendix — the lineage critique\1 (context, not steps)", p1,
        )
        p2 = parts["## 2. The upgrades"]
        p2 = re.sub(
            r"(?m)^## 2\. The upgrades(.*)$",
            r"## 5. Appendix — the upgrades table\1 (context, not steps)", p2,
        )

        # 4) original intro (minus its H1) becomes the appendix preamble
        old_intro_body = "\n".join(intro.splitlines()[1:]).strip()
        preamble = (
            "*The appendix preserves the original framing text: what the\n"
            "named lineage practiced, what was weak, and what this organ\n"
            "ships instead. It is context for humans; the agent's run order\n"
            "is §1–§3 above.*\n\n" + old_intro_body + "\n"
        )

        new_text = (
            directive + "\n" + p3 + "\n" + p4 + "\n" + p5 + "\n"
            + preamble + "\n" + p1 + "\n" + p2
        )
        mu.write_text(new_text)

        # 5) patch bump
        ver = bump_version(skill_md, old_title)
        report.append(f"OK: {organ} -> protocol-first, v{ver}")

    print("\n".join(report))
    print(f"\n{sum(1 for r in report if r.startswith('OK'))} reordered, "
          f"{sum(1 for r in report if r.startswith('SKIP'))} skipped")


if __name__ == "__main__":
    main()
