#!/usr/bin/env python3
"""Render docs/logo-lockup.png — the Mythos Arsenal header mark.

The Evidence Ledger lockup: the repo's most distinctive mechanism is
the append-only R-NNN evidence ledger ("no claim without a record"),
so the mark is three record rows — tag square + evidence bar — with
the newest append in burnt orange. Palette and type system match the
repo's other renders (paper #F7F5F0 / ink #1E2430 / orange #B3541E,
DejaVu Sans): one system.

Re-run after any logo change:
    python3 scripts/render_logo.py

Deterministic: same Chromium, same geometry -> same PNG bytes
(the render is run twice below and the md5s must match).
"""
import hashlib
import os
import sys

from playwright.sync_api import sync_playwright

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO_ROOT, "docs", "logo-lockup.png")
CHROME = ("/home/z/.cache/ms-playwright/chromium-1200/"
          "chrome-linux64/chrome")

PAPER = "#F7F5F0"
INK = "#1E2430"
ORANGE = "#B3541E"
GREY = "#5A6473"
FONT = "DejaVu Sans, sans-serif"


def ledger_rows(x0, y_top, tag, gap_y, bar_w, gap_x, fills, rx):
    """Three record rows: [tag square][evidence bar]. Row 3 = the append."""
    out = []
    for i, (w, fill) in enumerate(zip(bar_w, fills)):
        y = y_top + i * (tag + gap_y)
        out.append(
            f'<rect x="{x0}" y="{y:.1f}" width="{tag}" height="{tag}" '
            f'rx="{rx}" fill="{fill}"/>'
            f'<rect x="{x0 + tag + gap_x}" y="{y:.1f}" width="{w}" '
            f'height="{tag}" rx="{rx}" fill="{fill}"/>'
        )
    return "".join(out)


def svg_lockup():
    rows = ledger_rows(x0=106, y_top=125.5, tag=25, gap_y=17,
                       bar_w=[98, 66, 82], gap_x=9,
                       fills=[PAPER, PAPER, ORANGE], rx=5)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1560" height="360">
<rect width="1560" height="360" fill="{PAPER}"/>
<rect x="72" y="80" width="200" height="200" rx="26" fill="{INK}"/>
{rows}
<text x="332" y="186" font-family="{FONT}" font-size="76" font-weight="bold"
      fill="{INK}" style="letter-spacing:3px">MYTHOS ARSENAL</text>
<text x="335" y="232" font-family="{FONT}" font-size="26"
      fill="{GREY}" style="letter-spacing:11px">AGENTIC SECURITY SKILLS</text>
</svg>"""


def render_once(browser):
    page = browser.new_page(viewport={"width": 1560, "height": 360},
                            device_scale_factor=2)
    page.set_content(svg_lockup())
    page.wait_for_timeout(250)
    page.screenshot(path=OUT)
    page.close()
    with open(OUT, "rb") as fh:
        data = fh.read()
    return hashlib.md5(data).hexdigest(), len(data)


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=CHROME,
                                     args=["--no-sandbox"])
        md5_a, size_a = render_once(browser)
        md5_b, size_b = render_once(browser)
        browser.close()
    if md5_a != md5_b:
        sys.exit("NON-DETERMINISTIC RENDER: %s != %s" % (md5_a, md5_b))
    print("wrote %s (%d bytes, md5 %s — deterministic)"
          % (OUT, size_a, md5_a))


if __name__ == "__main__":
    main()
