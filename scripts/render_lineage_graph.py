#!/usr/bin/env python3
"""Render docs/lineage-corpus.png — the lineage knowledge graph.

A bipartite map of the assimilation registry: one row per entry
(practitioner -> organ), grouped into tier bands. The source of truth
is arsenal.tools.mythos.LINEAGES; the layout below must cover every
entry exactly or the render refuses to run.

Re-run after any lineage change:
    python3 scripts/render_lineage_graph.py

Rows are laid out by normal document flow (no absolute positioning),
so chips cannot overlap by construction. Palette matches
render_architecture.py (paper / ink / burnt-orange accent).
"""
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)
OUT = os.path.join(REPO_ROOT, "docs", "lineage-corpus.png")

from arsenal.tools.mythos import LINEAGES, TIERS  # noqa: E402

# ---- display data ----------------------------------------------------------
# Each row: (practitioner, artifact tag, organ, queue-assimilated flag).
# Dual-lineage organs carry a list of (practitioner, tag) chips instead.
BANDS = [
    ("SPINE · METHODOLOGY LAYER", "spine", [
        ("Jason Haddix", "Bug Hunter's Methodology",
         "mythos-bug-hunter", True),
    ]),
    ("TIER 1 · RECON & MAPPING", "t1", [
        ("EdOverflow", "can-i-takeover-xyz", "subdomain-hunter", False),
        ("Daniel Miessler", "SecLists", "content-discovery", False),
    ]),
    ("TIER 2 · ACCESS & LOGIC", "t2", [
        ("Frans Rosen", "Detectify", "auth-boundary-mapper", False),
        ("Aaron Parecki", "OAuth 2.0 Simplified", "oauth-flow-auditor",
         False),
        ("Soroush Dalili", "NCC Group", "business-logic-hunter", False),
    ]),
    ("TIER 3 · DEEP TECHNICAL", "t3", [
        ("Mario Heiderich", "Cure53", "xss-playbook", False),
        ([("Omer Gil", "Black Hat USA 2017"),
          ("James Kettle", "cache-poisoning corpus")],
         None, "cache-playbook", False),
        ("Toni de la Fuente", "Prowler", "cloud-config-auditor", False),
        ("Charlie Miller", "2009 iPhone SMS", "mobile-hunter", False),
        ("Gareth Heyes", "PortSwigger Research", "prototype-playbook",
         False),
    ]),
    ("TIER 4 · INCIDENT BRANCH", "t4", [
        ("Tsutomu Shimomura", "Takedown, 1995", "adversary-tracker",
         False),
    ]),
    ("TIER 5 · CRAFT LINEAGES", "t5", [
        ("Gordon Lyon", "Nmap", "scan-economist", False),
        ("HD Moore", "Metasploit", "module-smith", False),
        ("Tom Hudson", "Tomnomnom tools", "pipeline-smith", False),
        ("Michal Zalewski", "AFL", "feedback-fuzzer", False),
        ("ProjectDiscovery", "nuclei", "template-scanner", False),
        ("Justin Searle", "SamuraiWTF · Mantis", "packet-orchestrator",
         False),
        ("Dan Kaminsky", "2008 DNS poisoning", "protocol-forensics",
         True),
        ("James Forshaw", "Project Zero", "interior-cartographer", True),
        ("Tavis Ormandy", "Project Zero", "harness-smith", True),
        ("the grugq", "OPSEC corpus", "opsec-discipline", True),
    ]),
    ("TIER 6 · LEGEND TIER", "t6", [
        ("Orange Tsai", "DEVCORE", "chain-architect", False),
        ("James Kettle", "PortSwigger Research", "desync-hunter", False),
        ("George Hotz", "geohot", "deep-teardown", False),
        ("Adrian Lamo", "NYT intrusion, 2002", "ghost-crawler", False),
        ("Simon Willison", "coined 'prompt injection'", "mirror-hunter",
         False),
        ("Travis Goodspeed", "Microcontroller Exploits", "probe-smith",
         True),
        ("John Draper", "Captain Crunch", "signal-smith", False),
        ([("Kevin Mitnick", "The Art of Deception"),
          ("Sean Metcalf", "ADSecurity.org")],
         None, "trust-graph-hunter", True),
        ("Deviant Ollam", "Practical Lock Picking", "threshold-hunter",
         True),
    ]),
    ("TIER 7 · FORGE & COMPETITION", "t7", [
        ("the operator", "assimilation doctrine", "lineage-smith",
         False),
        ("Sun Tzu", "The Art of War", "rival-playbook", False),
    ]),
]

# Column assignment: SPINE+T1+T2+T3 | T4+T5+house-methods | T6+T7.
COLUMNS = [[0, 1, 2, 3], [4, 5], [6, 7]]

# Hunting organs with no named lineage (house methods) — asserted below.
HOUSE_METHODS = ["surface-cartographer", "js-recon", "api-surface-mapper",
                 "injection-lab", "ssrf-playbook"]

# ---- coverage gate: layout must equal the registry exactly -----------------
layout_organs = set()
queue_count = 0
for _title, _cls, rows in BANDS:
    for who, tag, organ, acc in rows:
        assert organ not in layout_organs, f"duplicate organ: {organ}"
        layout_organs.add(organ)
        if acc:
            queue_count += 1
registry_organs = {e["organ"] for e in LINEAGES}
assert layout_organs == registry_organs, (
    f"layout != registry\n  missing: {sorted(registry_organs - layout_organs)}"
    f"\n  extra:   {sorted(layout_organs - registry_organs)}")
assert queue_count == 8, f"queue accents: {queue_count} != 8"

# The house-methods card must be exactly the hunting organs (tiers 1-6)
# that carry no registry entry.
hunting = set()
for key, names in TIERS.items():
    if key[0] in "123456":
        hunting.update(names)
house_calc = sorted(hunting - registry_organs)
assert house_calc == sorted(HOUSE_METHODS), (
    f"house methods drift: {house_calc} != {sorted(HOUSE_METHODS)}")

N_ENTRIES = len(LINEAGES)          # 33
N_FIGURES = N_ENTRIES - 1          # 32 (lineage-smith is the operator's own)

FILL = {
    "spine": "#D4DCE4", "t1": "#EFECE4", "t2": "#EAE6DC", "t3": "#E5E0D4",
    "t4": "#E0DACC", "t5": "#DBD4C3", "t6": "#D6CEB9", "t7": "#DFD6C2",
}
FILL_KEY = {organ: cls
            for _t, cls, rows in BANDS
            for _w, _g, organ, _a in rows}

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #F7F5F0; font-family: 'DejaVu Sans', sans-serif;
       -webkit-font-smoothing: antialiased; }
.page { width: 1180px; padding: 34px 30px 24px; }
.eyebrow { font-size: 9.5px; letter-spacing: 2.4px; color: #8A8578;
           font-weight: 700; }
h1 { font-size: 23px; color: #1E2430; margin: 7px 0 8px;
     letter-spacing: -0.2px; }
.sub { font-size: 11.5px; color: #5A6473; margin-bottom: 22px; }
.sub b { color: #1E2430; font-weight: 700; }
.cols { display: flex; gap: 20px; align-items: flex-start; }
.col { flex: 1; display: flex; flex-direction: column; gap: 16px; }
.band { background: #FCFBF8; border: 1px solid #DDD7CB; border-radius: 10px;
        padding: 12px 11px 13px; }
.band h2 { font-size: 10px; letter-spacing: 1.6px; color: #6B6455;
           font-weight: 700; padding-bottom: 8px; margin-bottom: 11px;
           border-bottom: 1px solid #E7E1D4; }
.row { display: flex; align-items: center; margin-bottom: 9px; }
.row:last-child { margin-bottom: 0; }
.whos { display: flex; flex-direction: column; gap: 4px; width: 168px; }
.who { width: 168px; background: #F1EEE6; border: 1px solid #DAD4C8;
       border-radius: 7px; padding: 5px 9px 6px; }
.who b { display: block; font-size: 12.5px; color: #1E2430; font-weight: 600;
         white-space: nowrap; overflow: hidden; }
.who span { display: block; font-size: 9px; color: #8A8272; margin-top: 1px;
            white-space: nowrap; overflow: hidden; }
.arrow { flex: 1; min-width: 16px; height: 12px; }
.arrow.dual { height: auto; min-height: 60px; align-self: stretch; }
.arrow svg { display: block; width: 100%; height: 100%; }
.organ { width: 146px; border-radius: 7px; padding: 10px 6px; text-align: center;
         font-family: 'DejaVu Sans Mono', monospace; font-size: 10px;
         color: #1E2430; font-weight: 600;
         border: 1px solid rgba(30, 36, 48, 0.14); }
.organ.acc { border: 1.5px solid #B3541E; }
.house { display: flex; flex-wrap: wrap; gap: 6px; padding-top: 2px; }
.house .organ { width: calc(50% - 3px); padding: 8px 4px; font-size: 9.5px; }
.house-note { font-size: 9px; color: #8A8272; margin-top: 8px; }
footer { margin-top: 22px; padding-top: 10px; border-top: 1px solid #E2DCCE;
         font-size: 10px; color: #7A7466; display: flex;
         justify-content: space-between; }
footer .q { color: #B3541E; }
"""


def chip(who, tag):
    return f'<div class="who"><b>{who}</b><span>{tag}</span></div>'


ARROW_SINGLE = ('<svg viewBox="0 0 22 12" preserveAspectRatio="none">'
                '<path d="M0 6 H17 M17 6 L12.5 2.5 M17 6 L12.5 9.5" '
                'stroke="#A39D90" stroke-width="1.3" fill="none"/></svg>')
ARROW_DUAL = ('<svg viewBox="0 0 22 76" preserveAspectRatio="none">'
              '<path d="M0 19 C10 19 10 38 17 38 '
              'M0 57 C10 57 10 38 17 38 '
              'M17 38 L12.5 34.5 M17 38 L12.5 41.5" '
              'stroke="#A39D90" stroke-width="1.6" fill="none"/></svg>')


def organ_chip(organ, acc):
    cls = "organ acc" if acc else "organ"
    style = f' style="background:{FILL[FILL_KEY[organ]]}"'
    return f'<div class="{cls}"{style}>{organ}</div>'


def row_html(entry):
    who, tag, organ, acc = entry
    if isinstance(who, list):
        chips = "".join(chip(w, t) for w, t in who)
        return (f'<div class="row"><div class="whos">{chips}</div>'
                f'<div class="arrow dual">{ARROW_DUAL}</div>'
                f'{organ_chip(organ, acc)}</div>')
    return (f'<div class="row">{chip(who, tag)}'
            f'<div class="arrow">{ARROW_SINGLE}</div>'
            f'{organ_chip(organ, acc)}</div>')


def band_html(band_idx):
    title, _cls, rows = BANDS[band_idx]
    body = "".join(row_html(r) for r in rows)
    return f'<section class="band"><h2>{title}</h2>{body}</section>'


HOUSE_CARD = (
    '<section class="band"><h2>HOUSE METHODS · NO NAMED LINEAGE</h2>'
    '<div class="house">' + "".join(
        f'<div class="organ" style="background:#EFECE4">{o}</div>'
        for o in HOUSE_METHODS) +
    '</div><div class="house-note">written for the corpus, not extracted '
    'from a figure</div></section>')


cols_html = (
    '<div class="col">' + "".join(band_html(i) for i in COLUMNS[0]) + "</div>"
    '<div class="col">' + "".join(band_html(i) for i in COLUMNS[1])
    + HOUSE_CARD + "</div>"
    '<div class="col">' + "".join(band_html(i) for i in COLUMNS[2]) + "</div>")

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="page">
<div class="eyebrow">MYTHOS ARSENAL · AGENTIC SECURITY SKILLS</div>
<h1>The lineage corpus</h1>
<p class="sub"><b>{N_ENTRIES}</b> registry entries · <b>{N_FIGURES}</b> named
figures · every entry cites its dated public sources</p>
<div class="cols">{cols_html}</div>
<footer>
<span>registry · arsenal/tools/mythos.py — sources ·
skills/&lt;organ&gt;/references/sources.md</span>
<span><span class="q">outlined</span> = candidate-queue assimilation,
8 of 8 retired</span>
</footer>
</div></body></html>"""


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp_html = "/tmp/lineage-corpus.html"
    with open(tmp_html, "w", encoding="utf-8") as fh:
        fh.write(html)

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1180, "height": 900}, device_scale_factor=2)
        page.goto("file://" + tmp_html)
        page.wait_for_timeout(200)
        h = page.evaluate(
            "document.querySelector('.page').getBoundingClientRect().height")
        page.set_viewport_size({"width": 1180, "height": int(h) + 1})
        page.screenshot(path=OUT, full_page=True)
        browser.close()

    # sanity: file exists, non-trivial, not blank paper
    from PIL import Image
    im = Image.open(OUT).convert("RGB")
    w, h = im.size
    small = im.resize((200, max(1, int(200 * h / w))))
    px = list(small.getdata())
    paper = sum(1 for p in px if abs(p[0] - 247) < 6 and abs(p[1] - 245) < 6
                and abs(p[2] - 240) < 6)
    ratio = 1 - paper / len(px)
    print(f"rendered {OUT}: {w}x{h}px, non-paper pixel ratio {ratio:.2%}")
    assert w >= 2000 and h >= 1200, "unexpected render size"
    assert ratio > 0.15, "image looks blank"


if __name__ == "__main__":
    main()
