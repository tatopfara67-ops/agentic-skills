#!/usr/bin/env python3
"""mythos-arsenal report auditor — PASS/FAIL evidence-discipline gate.

Usage:
    python3 auditor/audit_report.py <report.md> [--program NAME]
                                          [--ledger DIR]

Grounding context resolution order: explicit --ledger DIR, explicit
--program NAME (engagements/<program>/ledger/), auto-detect when the
report lives under engagements/<program>/, auto-detect a sibling
ledger/ directory next to the report (the shipped worked example).
Without any of these the auditor runs standalone, syntax-only — see
check 9.

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
 8. skill-mythos gates (a CONFIRMED finding block that declares a
    `severity:` rating must carry the full triage-grade classification
    set, in the SAME block):
      a. cvss: line — a CVSS v3.1 base vector + the computed score; the
         score is RECOMPUTED here (arsenal/cvss.py, FIRST spec) and a
         mismatch fails the report
      b. vrt: line — a Bugcrowd VRT category (dotted id) + P-rating,
         validated against the shipped official taxonomy
         (skills/skill-mythos/references/vrt-taxonomy.json)
      c. a reproduction reference — an E-NNN experiment card or an
         explicit reproduction: line
    Incident handoffs (adversary hunts) rate `Risk:`, not `severity:` —
    the classification gates do not apply to them.
 9. citation grounding — existence: every R-NNN cited anywhere in the
    report must exist in the engagement's own ledger. A cited-but-missing
    record (fabricated, or borrowed from another engagement) fails the
    report — citation laundering of the first kind.
 10. citation grounding — relevance (entailment PROXY): each severity/
     class claim line is token-checked against the records it cites.
     two or more shared salient tokens -> grounded
     one shared token                     -> INFO (human review)
     zero shared, and the line NAMES a probed surface token the record
     never touched                        -> FAIL (misdirected citation —
     the claim describes a different surface than the evidence)
     zero shared, assessment-only prose   -> INFO (grounding rests on the
     block's facts lines — human review)
     Records tagged CONTROL / REFUSED / MISTAKE cited as vulnerability
     evidence FAIL outright — those tags are non-evidence by definition.
     Honest limit: token overlap is a proxy, not semantic understanding;
     it kills fabricated and misdirected citations and flags weak ones,
     but a full entailment judgment needs an LLM judge (documented,
     deliberate).
Exit 0 = PASS. Exit 1 = violations listed. Fix the work, not the auditor.
"""
from __future__ import annotations

import os
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
SEVERITY_LINE = re.compile(r"^(?:[-*]\s*)?[Ss]everity:\s*\S")
CVSS_LINE = re.compile(r"^(?:[-*]\s*)?cvss:\s*(.+)$", re.I)
VRT_LINE = re.compile(r"^(?:[-*]\s*)?vrt:\s*(.+)$", re.I)
CVSS_VECTOR = re.compile(r"CVSS:3\.[01](?:/[A-Z]+:[A-Z0-9]+)+")
CVSS_STATED = re.compile(r"=\s*(\d+(?:\.\d+)?)\b")
VRT_PATH = re.compile(r"\b([a-z][a-z_]*(?:\.[a-z_0-9]+)+)\b")
P_LEVEL = re.compile(r"\bP([1-5])\b")
E_REF = re.compile(r"\bE-\d{3,}\b")
REPRO_LINE = re.compile(r"^(?:[-*]\s*)?reproduction:\s*\S", re.I)
RECORD_LINE = re.compile(r"^(R-\d{3,})\s*\|")
XREF = re.compile(r"\b[A-Za-z]+-\d{2,}\b")       # R-042, H-012, E-003, CVE-…
TOKEN = re.compile(r"[a-z0-9][a-z0-9_./\-]{2,}")
NON_EVIDENCE_TAGS = frozenset({"CONTROL", "REFUSED", "MISTAKE"})
_GENERIC = frozenset("""
the and for with that this from was were are has have had not but its
their they when then than into over under without http https www com net
org response responses request requests line lines record records ledger
report reports finding findings evidence cited citation severity class
note notes critical high medium low informational
""".split())

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (_ROOT,):
    if _p not in sys.path:
        sys.path.insert(0, _p)
try:
    from arsenal import cvss as _cvss  # noqa: E402
except Exception:  # pragma: no cover — standalone use outside the tree
    _cvss = None


def _load_vrt_taxonomy():
    """Shipped official Bugcrowd VRT taxonomy, or None when absent."""
    path = os.path.join(_ROOT, "skills", "skill-mythos", "references",
                        "vrt-taxonomy.json")
    try:
        import json
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        return data.get("content") or data
    except (OSError, ValueError):
        return None


_VRT_TAXONOMY = None
_VRT_TRIED = False


def _vrt_node(dotted: str):
    global _VRT_TAXONOMY, _VRT_TRIED
    if not _VRT_TRIED:
        _VRT_TRIED = True
        _VRT_TAXONOMY = _load_vrt_taxonomy()
    if _VRT_TAXONOMY is None:
        return None
    node = {"children": _VRT_TAXONOMY}
    for part in dotted.split("."):
        node = next((ch for ch in node.get("children", []) or []
                     if ch.get("id") == part), None)
        if node is None:
            return None
    return node


def _resolve_program(path: str, explicit: str | None) -> str | None:
    """Explicit --program wins; else auto-detect engagements/<program>/."""
    if explicit:
        return explicit
    parts = os.path.normpath(os.path.abspath(path)).split(os.sep)
    if "engagements" in parts:
        i = parts.index("engagements")
        if i + 1 < len(parts) and parts[i + 1] not in ("", "..", "."):
            return parts[i + 1]
    return None


def _resolve_ledger_dir(path: str, explicit: str | None,
                        program: str | None) -> str | None:
    """Explicit --ledger wins; else a sibling ledger/ directory next to
    the report (how the shipped worked-engagement example is laid out)."""
    if explicit:
        return explicit
    if program:
        return None                      # engagements/<program>/ path applies
    sibling = os.path.join(os.path.dirname(os.path.abspath(path)),
                           "ledger")
    return sibling if os.path.isdir(sibling) else None


def _load_records(ledger_dir: str | None,
                  program: str | None) -> dict[str, tuple[str, str]] | None:
    """One pass over an engagement ledger -> {rid: (tag, full_line)}.
    Explicit --ledger DIR is read directly (exported evidence bundles);
    a program name goes through arsenal.ledger's own resolver. None when
    neither is available — standalone audits keep running."""
    out: dict[str, tuple[str, str]] = {}
    if ledger_dir:
        try:
            for name in ("records.md", "append.md"):
                p = os.path.join(ledger_dir, name)
                if not os.path.isfile(p):   # exported bundles may omit one
                    continue
                with open(p, encoding="utf-8", errors="replace") as fh:
                    for line in fh:
                        m = RECORD_LINE.match(line)
                        if not m or m.group(1) in out:
                            continue
                        parts = [q.strip() for q in line.split("|")]
                        tag = parts[6] if len(parts) > 6 else ""
                        out[m.group(1)] = (tag, line.rstrip("\n"))
        except OSError:
            return None
        return out or None
    if program:
        try:
            from arsenal import ledger as _ledger
        except Exception:
            return None
        try:
            for rid, line in _ledger._iter_records(program):
                parts = [q.strip() for q in line.split("|")]
                tag = parts[6] if len(parts) > 6 else ""
                out[rid] = (tag, line)
        except Exception:
            return None
        return out or None
    return None


def _salient(text: str) -> set[str]:
    """Salient tokens: lowercase runs (paths, params, statuses, probe
    vocabulary) with cross-references (R-/H-/E- ids) and generic report
    furniture stripped — the entailment proxy's vocabulary. Tokens that
    carry slashes also contribute their segments: a claim written as
    "/api/v0/debug" must ground against a record that logged
    "127.0.0.1:8477/api/v0/debug"."""
    toks = set()
    for m in TOKEN.finditer(XREF.sub(" ", text.lower())):
        t = m.group(0).strip("./-")
        if len(t) >= 3 and t not in _GENERIC:
            toks.add(t)
            if "/" in t:
                for seg in t.split("/"):
                    seg = seg.strip("./-")
                    if len(seg) >= 3 and seg not in _GENERIC:
                        toks.add(seg)
    return toks


def _evidence_text(raw_line: str) -> str:
    """Record fields that carry evidence: tool, action, result, note —
    never the id, timestamp, size, or tag columns (tag names like
    SURFACE would leak into the vocabulary as fake signal)."""
    parts = [q.strip() for q in raw_line.split("|")]
    if len(parts) < 7:
        return raw_line
    return " | ".join(parts[2:5] + parts[7:8])


def _claim_tokens(line: str) -> set[str]:
    """Salient tokens of a report claim line, with CVSS vectors and
    stated scores stripped first — those are assessment furniture, not
    surface vocabulary."""
    text = CVSS_STATED.sub(" ", CVSS_VECTOR.sub(" ", line))
    return _salient(text)


def _grounding(ledger_dir: str | None, program: str | None,
               lines: list[str], results: list) -> None:
    """Checks 9 + 10: cited records must exist and must ground the claims
    that cite them (token-overlap entailment proxy)."""
    records = _load_records(ledger_dir, program)
    ctx = ledger_dir or ("engagement %r" % program if program else "")
    if records is None:
        results.append(("INFO", "ledger for %s unavailable — "
                        "existence/relevance checks skipped (pass --ledger "
                        "or --program to ground them)" % ctx))
        return
    cited = {m.group(0) for m in RID.finditer("\n".join(lines))}
    missing = sorted(cited - set(records))
    for rid in missing:
        results.append(("FAIL", "cited record %s does not exist in the %s "
                        "ledger — fabricated citation, or a record borrowed "
                        "from another engagement (which is not evidence "
                        "here)" % (rid, ctx)))
    if cited and not missing:
        results.append(("PASS", "citation existence: all %d cited record(s) "
                         "present in the %s ledger" % (len(cited), ctx)))

    # action-field vocabulary: every surface token this engagement has
    # actually probed (urls, params, hosts) — the oracle that separates
    # "misdirected citation" from "assessment-only prose"
    action_vocab: set[str] = set()
    for _tag, raw in records.values():
        parts = [q.strip() for q in raw.split("|")]
        if len(parts) > 3:
            action_vocab |= _salient(parts[3])

    checked = 0
    for i, line in enumerate(lines, 1):
        if not (SEVERITY_WORDS.search(line) or CLASS_WORDS.search(line)):
            continue
        if CVSS_LINE.match(line) or VRT_LINE.match(line):
            continue          # classification furniture, machine-verified in
                             # check 8 (score recomputed, taxonomy checked) —
                             # not an evidence claim
        rids = [m.group(0) for m in RID.finditer(line)]
        if not rids:
            continue                     # check 1 already fails those
        claim = _claim_tokens(line)
        for rid in rids:
            if rid not in records:
                continue                 # already failed above
            tag, raw = records[rid]
            if tag in NON_EVIDENCE_TAGS and CLASS_WORDS.search(line):
                results.append(("FAIL", "line %d cites %s (tag %s) as "
                                "vulnerability evidence — %s records are "
                                "non-evidence by definition" % (i, rid, tag,
                                                                tag)))
                continue
            checked += 1
            shared = claim & _salient(_evidence_text(raw))
            gist = raw.split("|", 2)[-1].strip()[:100]
            if len(shared) >= 2:
                continue
            if len(shared) == 1:
                results.append(("INFO", "line %d -> %s weak grounding: only "
                                "shared token %r — human review. Record says: "
                                "%s" % (i, rid, sorted(shared)[0], gist)))
                continue
            named = claim & action_vocab
            if named:
                results.append(("FAIL", "line %d cites %s but names probed "
                                "surface token(s) %s the record never "
                                "touched — the claim describes a different "
                                "surface than the evidence. Record says: %s"
                                % (i, rid, sorted(named)[:4], gist)))
            else:
                results.append(("INFO", "line %d -> %s assessment-only line: "
                                "no surface vocabulary to check (grounding "
                                "rests on the block's facts lines — human "
                                "review). Record says: %s" % (i, rid, gist)))
    if checked:
        results.append(("INFO", "citation relevance (entailment proxy): %d "
                        "claim-line/record pair(s) token-checked — misdirected "
                        "citations FAIL above, weak/assessment-only pairs "
                        "flagged for review" % checked))


def audit(path: str, program: str | None = None,
          ledger_dir: str | None = None) -> list[tuple[str, str]]:
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

    # 9 + 10. citation grounding (existence + relevance proxy)
    program = _resolve_program(path, program)
    ledger_dir = _resolve_ledger_dir(path, ledger_dir, program)
    if program or ledger_dir:
        _grounding(ledger_dir, program, lines, results)
    else:
        results.append(("INFO", "no engagement context — citation grounding "
                        "skipped (pass --ledger or --program, or file the "
                        "report next to a ledger/ directory)"))

    # 2/3/5/6/8. block-level contracts. A block is strict: it runs from
    # its ### heading to the NEXT heading of any level — summary sections
    # (##) never leak into a finding block.
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
        if line.startswith("## ") or line.startswith("### "):
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

    # 8. skill-mythos classification gates: a CONFIRMED finding block that
    # declares a `severity:` rating is a vulnerability finding, and must
    # carry the full triage-grade set IN the block
    for h, d in h_blocks.items():
        if d["closure"] != "CONFIRMED":
            continue
        body_lines = d["body"]
        if not any(SEVERITY_LINE.match(l) for l in body_lines):
            continue
        body = "\n".join(body_lines)
        cvss_line = next((l for l in body_lines if CVSS_LINE.match(l)), "")
        vrt_line = next((l for l in body_lines if VRT_LINE.match(l)), "")
        if not cvss_line:
            note("FAIL", "%s declares a severity rating but carries no "
                 "cvss: line (vector + score — skill-mythos gate A10)" % h)
        else:
            vm = CVSS_VECTOR.search(cvss_line)
            if not vm:
                note("FAIL", "%s cvss: line carries no CVSS v3.1 base "
                     "vector" % h)
            else:
                vector = vm.group(0)
                sm = CVSS_STATED.search(cvss_line)
                if not sm:
                    note("FAIL", "%s cvss: line states no computed score "
                         "(write '= N.N' from cvss3_score)" % h)
                elif _cvss is None:
                    note("INFO", "%s cvss score not recomputed "
                         "(arsenal/cvss.py unavailable here)" % h)
                else:
                    try:
                        recomputed = _cvss.base_score(vector)["score"]
                    except ValueError as exc:
                        note("FAIL", "%s cvss vector invalid: %s" % (h, exc))
                    else:
                        stated = float(sm.group(1))
                        if abs(stated - recomputed) > 0.001:
                            note("FAIL", "%s cvss score mismatch: line says "
                                 "%.1f, vector computes %.1f — fix one of "
                                 "them" % (h, stated, recomputed))
        if not vrt_line:
            note("FAIL", "%s declares a severity rating but carries no "
                 "vrt: line (Bugcrowd category + P-rating)" % h)
        else:
            pm = P_LEVEL.search(vrt_line)
            if not pm:
                note("FAIL", "%s vrt: line states no P-rating (P1-P5)" % h)
            vpm = VRT_PATH.search(vrt_line)
            if vpm:
                node = _vrt_node(vpm.group(1))
                if node is None and _VRT_TAXONOMY is not None:
                    note("FAIL", "%s vrt category %r not found in the "
                         "shipped taxonomy — copy the exact dotted id from "
                         "vrt_classify" % (h, vpm.group(1)))
            else:
                note("FAIL", "%s vrt: line carries no dotted category id "
                     "(e.g. broken_access_control.idor)" % h)
        if not (E_REF.search(body) or any(REPRO_LINE.match(l)
                                          for l in body_lines)):
            note("FAIL", "%s lacks a reproduction reference (E-NNN card "
                 "or reproduction: line) — fully reproducible or it does "
                 "not ship" % h)
        else:
            note("PASS", "%s CONFIRMED finding carries the full "
                 "classification set (cvss + vrt + reproduction)" % h)

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
    rest: list[str] = []
    program = None
    ledger_dir = None
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--program" and i + 1 < len(argv):
            program = argv[i + 1]
            i += 2
            continue
        if a.startswith("--program="):
            program = a.split("=", 1)[1]
            i += 1
            continue
        if a == "--ledger" and i + 1 < len(argv):
            ledger_dir = argv[i + 1]
            i += 2
            continue
        if a.startswith("--ledger="):
            ledger_dir = a.split("=", 1)[1]
            i += 1
            continue
        rest.append(a)
        i += 1
    if not rest:
        print(__doc__)
        return 2
    path = rest[0]
    ctx = " (program: %s)" % program if program else ""
    ctx += " (ledger: %s)" % ledger_dir if ledger_dir else ""
    print("== audit: %s%s" % (path, ctx))
    failed = False
    for status, msg in audit(path, program, ledger_dir):
        print("[ %s ] %s" % (status, msg))
        if status == "FAIL":
            failed = True
    print("RESULT: %s" % ("FAIL — fix the work behind the report, not the "
                          "auditor" if failed else "PASS"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
