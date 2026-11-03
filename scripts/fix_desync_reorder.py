#!/usr/bin/env python3
"""desync-hunter special case: 4-section method-upgrade.md, reorder manually."""
import pathlib
import re

MU = pathlib.Path("/home/z/my-project/repo/agentic-skills/skills/desync-hunter/references/method-upgrade.md")
SK = pathlib.Path("/home/z/my-project/repo/agentic-skills/skills/desync-hunter/SKILL.md")

t = MU.read_text()
heads = ["## 1. The critique", "## 2. The upgrades",
         "## 3. The executable protocol", "## 4. Falsifiers"]
pos = []
for h in heads:
    m = re.search(r"(?m)^" + re.escape(h) + r"[^\n]*\n", t)
    pos.append((m.start(), m.end()))
pos.sort()
intro = t[: pos[0][0]].rstrip() + "\n"
body = {}
for i, (s, e) in enumerate(pos):
    end = pos[i + 1][0] if i + 1 < len(pos) else len(t)
    body[i] = t[s:end].rstrip() + "\n"  # includes own heading

p3 = re.sub(r"(?m)^## 3\. The executable protocol", "## 1. The executable protocol", body[2])
p4 = re.sub(r"(?m)^## 4\. Falsifiers", "## 2. Falsifiers", body[3])
p1 = re.sub(r"(?m)^## 1\. The critique(.*)$",
            r"## 3. Appendix — the lineage critique\1 (context, not steps)", body[0])
p2 = re.sub(r"(?m)^## 2\. The upgrades(.*)$",
            r"## 4. Appendix — the upgrades table\1 (context, not steps)", body[1])
old_intro_body = "\n".join(intro.splitlines()[1:]).strip()
preamble = ("*The appendix preserves the original framing text: what the\n"
            "named lineage practiced, what was weak, and what this organ\n"
            "ships instead. It is context for humans; the agent's run order\n"
            "is §1–§2 above.*\n\n" + old_intro_body + "\n")
new = ("# The executable method — M1–M4 for desync-hunter\n\n"
       "This file is the organ's executable method: numbered phases,\n"
       "exact record formats, thresholds, decision gates, and falsifiers,\n"
       "in run order. An agent that has never heard of any name in the\n"
       "appendix runs this at full precision. The lineage critique that\n"
       "justifies each step (why these phases exist, what was weak in\n"
       "Kettle's published desync research) is preserved verbatim as the\n"
       "§3–§4 appendix.\n\n" + p3 + "\n" + p4 + "\n" + preamble + "\n" + p1 + "\n" + p2)
MU.write_text(new)

s = SK.read_text()
m = re.search(r"(?m)^version:\s*(\d+)\.(\d+)\.(\d+)\s*$", s)
new_v = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"
s = re.sub(r"(?m)^version:.*$", f"version: {new_v}", s, count=1)
s = re.sub(r"(?m)^(#\s+.+?)v\d+\.\d+\.\d+", rf"\g<1>v{new_v}", s, count=1)
SK.write_text(s)
print(f"desync-hunter reordered, v{new_v}")
