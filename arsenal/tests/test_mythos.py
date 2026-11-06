"""skill-mythos tests — charter, doctrine forge, CVSS engine, VRT classifier.

Covers: the nineteen-article activation payload, the doctrine_forge
prompt-escalation engine (intent grammar, severity/quota extraction,
persona mixes, determinism), spec-exact CVSS 3.1 base scoring (including
the FIRST published example scores), VRT classification against the
shipped official taxonomy (variant selection, HackerOne crosswalk,
template shaping), and the hardened auditor gates (cvss recomputation,
vrt validation, reproduction reference, incident-handoff exemption).
"""
import importlib.util
import json
import os
import re
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

from arsenal import cvss as _cvss  # noqa: E402
from arsenal.tools import mythos as _mythos  # noqa: E402

_TREE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
_AUDITOR_PATH = os.path.join(_TREE_ROOT, "auditor", "audit_report.py")


def _auditor():
    spec = importlib.util.spec_from_file_location("mythos_audit_report",
                                                  _AUDITOR_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------ CVSS v3.1

class TestCvssEngine(unittest.TestCase):
    SPEC_VECTORS = [
        # published CVSS v3.1 example scores (FIRST calculator)
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", 9.8),
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H", 10.0),
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N", 6.1),
        ("CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N", 6.5),
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N", 5.3),
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N", 7.5),
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N", 0.0),
        ("CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H", 9.9),
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N", 8.6),
    ]

    def test_spec_example_scores(self):
        for vector, expected in self.SPEC_VECTORS:
            got = _cvss.base_score(vector)
            self.assertEqual(got["score"], expected, vector)
            self.assertEqual(got["vector"],
                             vector if vector.startswith("CVSS:")
                             else "CVSS:3.1/" + vector)

    def test_bare_vector_and_prefixes(self):
        for prefix in ("CVSS:3.1/", "CVSS:3.0/", ""):
            vec = prefix + "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
            self.assertEqual(_cvss.base_score(vec)["score"], 9.8, vec)

    def test_severity_bands(self):
        cases = [(0.0, "None"), (3.9, "Low"), (4.0, "Medium"),
                 (6.9, "Medium"), (7.0, "High"), (8.9, "High"),
                 (9.0, "Critical"), (10.0, "Critical")]
        for score, band in cases:
            self.assertEqual(_cvss.severity_band(score), band, score)

    def test_pr_weight_depends_on_scope(self):
        # same PR:L and same impact metrics; only Scope changes, and the
        # PR weight relaxes (0.62 -> 0.68, spec table 7): 8.8 -> 9.9
        u = _cvss.base_score("AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H")
        c = _cvss.base_score("AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H")
        self.assertEqual(u["score"], 8.8)
        self.assertEqual(c["score"], 9.9)

    def test_rejects_broken_vectors(self):
        bad = [
            "",                                  # empty
            "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H",   # missing A
            "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:X",  # bad value
            "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/A:H",  # duplicate
            "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/XX:N",  # unknown metric
            "CVSS:2.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",  # old version
        ]
        for vector in bad:
            with self.assertRaises(ValueError, msg=vector):
                _cvss.parse_vector(vector)

    def test_error_messages_stay_instructive(self):
        with self.assertRaises(ValueError) as cm:
            _cvss.parse_vector("AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H")
        self.assertIn("missing metric(s): A", str(cm.exception))


# ------------------------------------------------------------- charter

class TestMythosCharter(unittest.TestCase):
    def setUp(self):
        self.charter = _mythos.mythos_charter()

    def test_nineteen_articles(self):
        self.assertEqual(len(self.charter["articles"]), 19)
        for article in self.charter["articles"]:
            self.assertRegex(article, r"^A\d+ ")
        self.assertIn("CVSS 3.1", "".join(self.charter["articles"]))
        self.assertTrue(self.charter["articles"][-1].startswith("A19"))
        self.assertIn("three registers", self.charter["articles"][13])
        self.assertIn("war logic", self.charter["articles"][14])
        self.assertIn("method over mythology",
                      self.charter["articles"][15])
        self.assertIn("expert precision",
                      self.charter["articles"][15])
        self.assertIn("behavior over biography",
                      self.charter["articles"][16])
        self.assertIn("operator-os.md",
                      self.charter["articles"][16])
        self.assertIn("the opening ladder",
                      self.charter["articles"][17])
        self.assertIn("Hypothesis Rail",
                      self.charter["articles"][17])
        self.assertIn("test_opening_ladder_rollout",
                      self.charter["articles"][17])
        self.assertIn("payload corpus depth",
                      self.charter["articles"][18])
        self.assertIn("corpus_version",
                      self.charter["articles"][18])
        self.assertIn("test_payload_kit_depth",
                      self.charter["articles"][18])

    def test_charter_full_text_lives_in_references(self):
        """The routing layer stays lean (v1.21.2): the full binding
        text of the nineteen articles lives in references/charter.md
        (moved verbatim — SKILL.md back under the validator's WARN
        threshold), and the two forms never drift: the full text
        counts exactly nineteen articles, carries every distilled
        article's keyword and lock-test, and the routing layer points
        at it. Regrowing the routing layer past the threshold is the
        defect this test refuses.
        """
        bundle = os.path.join(_TREE_ROOT, "skills", "skill-mythos")
        core_path = os.path.join(bundle, "SKILL.md")
        full_path = os.path.join(bundle, "references", "charter.md")
        with open(core_path, encoding="utf-8") as fh:
            core = fh.read()
        with open(full_path, encoding="utf-8") as fh:
            full = fh.read()

        self.assertIn("references/charter.md", core)
        self.assertLessEqual(os.path.getsize(core_path), 32768,
                             "SKILL.md regrew past the WARN threshold — "
                             "depth belongs in references/charter.md")

        # the full text counts exactly the nineteen articles
        numbered = [line for line in full.splitlines()
                    if re.match(r"^\d+\. \*\*", line)]
        self.assertEqual(len(numbered), 19)

        # and the two forms never drift: each distilled article's
        # keyword and lock-test survive in the full binding text
        # (casefold: the full text headlines "War logic.", the
        # distilled form says "war logic" mid-sentence)
        full_cf = full.casefold()
        for keyword in ("prompt escalation", "three registers",
                        "war logic", "method over mythology",
                        "behavior over biography", "the opening ladder",
                        "payload corpus depth"):
            self.assertIn(keyword, full_cf)
        self.assertIn("test_opening_ladder_rollout", full)
        self.assertIn("test_payload_kit_depth", full)
        self.assertIn("test_operator_os_is_universal", full)

    def test_charter_carries_prompt_escalation(self):
        escalation = self.charter["prompt_escalation"]
        self.assertEqual(escalation["tool"], "doctrine_forge")
        self.assertIn("A13", escalation["rule"])

    def test_tier_registry_lists_all_organs(self):
        tiers = self.charter["tiers"]
        self.assertEqual(sum(len(v) for v in tiers.values()), 40)
        self.assertEqual(tiers["0-engine"], {"glm-self-model": True})
        self.assertEqual(tiers["0-master"], {"skill-mythos": True})
        self.assertEqual(sorted(tiers["7-forge"]),
                         ["lineage-smith", "rival-playbook"])
        self.assertEqual(sorted(tiers["4-incident"]),
                         ["adversary-tracker", "php2shell-forensics"])
        self.assertEqual(sorted(tiers["3-deep-technical"]), [
            "cache-playbook", "cloud-config-auditor", "injection-lab",
            "mobile-hunter", "prototype-playbook", "ssrf-playbook",
            "xss-playbook"])
        self.assertEqual(sorted(tiers["5-craft"]), [
            "feedback-fuzzer", "harness-smith", "interior-cartographer",
            "module-smith", "opsec-discipline", "packet-orchestrator",
            "pipeline-smith", "protocol-forensics", "scan-economist",
            "template-scanner"])
        self.assertEqual(sorted(tiers["6-legend"]), [
            "chain-architect", "deep-teardown", "desync-hunter",
            "ghost-crawler", "mirror-hunter", "probe-smith",
            "signal-smith", "threshold-hunter",
            "trust-graph-hunter"])
        for tier, skills in tiers.items():
            for name, installed in skills.items():
                self.assertTrue(installed, "%s missing in tier %s"
                                % (name, tier))

    def test_reporting_tools_routing(self):
        self.assertIn("cvss3_score", self.charter["reporting_tools"])
        self.assertIn("vrt_classify", self.charter["reporting_tools"])
        self.assertIn("mythos_lineages", self.charter["reporting_tools"])

    def test_quality_gates_name_the_instruments(self):
        gates = " ".join(self.charter["quality_gates"])
        for token in ("differential triad", "CVSS 3.1", "VRT",
                      "HackerOne", "reproduction", "impact-chain"):
            self.assertIn(token, gates)


class TestMythosLineages(unittest.TestCase):
    def test_registry_lists_thirty_three_lineages_all_installed(self):
        registry = _mythos.mythos_lineages()
        self.assertEqual(registry["count"], 33)
        by_organ = {e["organ"]: e for e in registry["lineages"]}
        for organ in ("adversary-tracker", "scan-economist", "module-smith",
                      "pipeline-smith", "feedback-fuzzer",
                      "template-scanner", "packet-orchestrator",
                      "chain-architect", "desync-hunter", "deep-teardown",
                      "ghost-crawler", "mirror-hunter",
                      "auth-boundary-mapper",
                      "signal-smith", "trust-graph-hunter",
                      "subdomain-hunter", "xss-playbook",
                      "oauth-flow-auditor", "content-discovery",
                      "business-logic-hunter", "cloud-config-auditor",
                      "mobile-hunter", "cache-playbook",
                      "prototype-playbook", "interior-cartographer",
                      "lineage-smith",
                      "rival-playbook", "harness-smith", "probe-smith",
                      "opsec-discipline", "mythos-bug-hunter",
                      "threshold-hunter"):
            self.assertIn(organ, by_organ)
            self.assertTrue(by_organ[organ]["installed"], organ)
            for field in ("figure", "distillation", "sources"):
                self.assertTrue(by_organ[organ][field], "%s lacks %s"
                                % (organ, field))

    def test_lineage_figures_are_the_verified_names(self):
        registry = _mythos.mythos_lineages()
        joined = " ".join(e["figure"] for e in registry["lineages"])
        for name in ("Shimomura", "Gordon Lyon", "HD Moore", "Tom Hudson",
                     "Zalewski", "Sandeep Singh", "Nizamul Rana",
                     "Justin Searle", "PhonePe", "Orange Tsai",
                     "James Kettle", "George Hotz", "Adrian Lamo",
                     "Frans Rosen", "John Draper", "Kevin Mitnick",
                     "EdOverflow", "Heiderich", "Parecki", "Miessler",
                     "Dalili", "de la Fuente", "Simon Willison",
                     "Dan Kaminsky", "James Forshaw", "Sun Tzu",
                     "Tavis Ormandy", "Travis Goodspeed",
                     "Sean Metcalf", "the grugq", "Jason Haddix",
                     "Deviant Ollam", "Howard Payne", "Matt Blaze"):
            self.assertIn(name, joined, name)
        # the unverified attributions from the operator brief stay out
        self.assertNotIn("Skappen", joined)
        self.assertNotIn("Franz Rosen", joined)  # misspelling stays out

    def test_method_layer_is_universal(self):
        """A16's debt register is closed and stays closed: every organ
        that shipped a method-upgrade module still carries it, and the
        module keeps its three-part shape (critique, upgrades, and
        where they land, falsifiers). New organs are born with the
        layer — the guard list covers all 36 modules on record."""
        organs = [
            "adversary-tracker", "auth-boundary-mapper",
            "business-logic-hunter", "cache-playbook", "chain-architect",
            "cloud-config-auditor", "content-discovery", "deep-teardown",
            "desync-hunter", "feedback-fuzzer", "ghost-crawler",
            "glm-self-model", "harness-smith", "injection-lab",
            "interior-cartographer", "lineage-smith",
            "mirror-hunter", "mobile-hunter", "module-smith",
            "mythos-bug-hunter", "oauth-flow-auditor",
            "opsec-discipline",
            "packet-orchestrator", "pipeline-smith",
            "probe-smith", "protocol-forensics", "prototype-playbook",
            "rival-playbook", "scan-economist", "signal-smith",
            "ssrf-playbook", "subdomain-hunter", "template-scanner",
            "threshold-hunter", "trust-graph-hunter", "xss-playbook",
        ]
        skills_root = os.path.join(_TREE_ROOT, "skills")
        shipped = {n for n in os.listdir(skills_root)
                   if os.path.isfile(os.path.join(skills_root, n,
                                                 "references",
                                                 "method-upgrade.md"))}
        self.assertEqual(shipped, set(organs),
                         "method-upgrade.md set drifted: %s"
                         % (set(organs) ^ shipped))
        for organ in organs:
            with open(os.path.join(skills_root, organ, "references",
                                   "method-upgrade.md"),
                      encoding="utf-8") as fh:
                body = fh.read()
            for token in ("The critique", "upgrades", "Falsifiers"):
                self.assertIn(token, body,
                              "%s: A16 layer incomplete (%s)" % (organ, token))

    def test_operator_os_is_universal(self):
        """A17's layer is shipped and locked: every organ forged from a
        named person carries references/operator-os.md, and the module
        keeps its four-part runtime shape (thinking framework,
        behavioral protocol, scripting arsenal, rigid run-order) plus
        falsifiers. The forge-tier organs carry their named
        equivalents instead (psychology-catalog, campaign-protocol,
        failure-geometry — plus, since the forge tier's own runtime
        wave, references/forge-os.md) — the guard covers the 31
        person-lineage organs on record."""
        organs = [
            "adversary-tracker", "auth-boundary-mapper",
            "business-logic-hunter", "cache-playbook", "chain-architect",
            "cloud-config-auditor", "content-discovery", "deep-teardown",
            "desync-hunter", "feedback-fuzzer", "ghost-crawler",
            "harness-smith", "interior-cartographer", "mirror-hunter",
            "mobile-hunter", "module-smith", "mythos-bug-hunter",
            "oauth-flow-auditor", "opsec-discipline", "packet-orchestrator",
            "pipeline-smith",
            "probe-smith",
            "protocol-forensics", "prototype-playbook", "scan-economist",
            "signal-smith", "subdomain-hunter", "template-scanner",
            "threshold-hunter", "trust-graph-hunter", "xss-playbook",
        ]
        skills_root = os.path.join(_TREE_ROOT, "skills")
        shipped = {n for n in os.listdir(skills_root)
                   if os.path.isfile(os.path.join(skills_root, n,
                                                 "references",
                                                 "operator-os.md"))}
        self.assertEqual(shipped, set(organs),
                         "operator-os.md set drifted: %s"
                         % (set(organs) ^ shipped))
        for organ in organs:
            with open(os.path.join(skills_root, organ, "references",
                                   "operator-os.md"),
                      encoding="utf-8") as fh:
                body = fh.read()
            for token in ("The thinking framework",
                          "The behavioral protocol",
                          "The scripting arsenal",
                          "The rigid run-order",
                          "Falsifiers"):
                self.assertIn(token, body,
                              "%s: A17 layer incomplete (%s)" % (organ, token))

    def test_opening_ladder_rollout(self):
        """A18's rollout is CLOSED at the full corpus: every
        person-lineage organ's operator-os carries The opening
        ladder — the figure's perception as a candidate-generation
        question ladder (rungs write census rows, never packets;
        ranking rationale stated; generation falsifier on record).
        The staged rollout grew only by execution (one organ done
        well beats a mass wave done thin — the A17 lesson) and
        closed with its two person-lineage special cases: the
        Shimomura runtime (the hunt's telemetry-reading ladder) and
        the spine itself (the onboarding corpus-reading ladder) —
        all 31 person-lineage organs carry the ladder, so this list
        is the lock."""
        rollout = [
            "adversary-tracker", "auth-boundary-mapper",
            "business-logic-hunter", "cache-playbook", "chain-architect",
            "cloud-config-auditor", "content-discovery", "deep-teardown",
            "desync-hunter", "feedback-fuzzer", "ghost-crawler",
            "harness-smith", "interior-cartographer", "mirror-hunter",
            "mobile-hunter", "module-smith", "mythos-bug-hunter",
            "oauth-flow-auditor", "opsec-discipline",
            "packet-orchestrator", "pipeline-smith", "probe-smith",
            "protocol-forensics", "prototype-playbook", "scan-economist",
            "signal-smith", "subdomain-hunter", "template-scanner",
            "threshold-hunter", "trust-graph-hunter", "xss-playbook",
        ]
        skills_root = os.path.join(_TREE_ROOT, "skills")
        for organ in rollout:
            path = os.path.join(skills_root, organ, "references",
                                "operator-os.md")
            self.assertTrue(os.path.isfile(path),
                             "%s: operator-os.md missing" % organ)
            with open(path, encoding="utf-8") as fh:
                body = fh.read()
            for token in ("The opening ladder",
                          "Ranking rationale",
                          "Generation falsifier"):
                self.assertIn(token, body,
                              "%s: A18 layer incomplete (%s)" % (organ,
                                                                 token))

    def test_forge_os_runtime(self):
        """The forge tier's runtime wave: the two forge-tier organs
        carry their A17-equivalent runtime as references/forge-os.md
        (the universality guard reserves operator-os.md for the
        person-lineage organs; the forge tier's named equivalent is
        this module) — the four-part runtime shape plus The opening
        ladder (A18): the nomination-reading / artifact-reading
        questions that write census rows before the score gate or the
        hollow map runs (rungs write census rows, never verdicts;
        ranking rationale stated; generation falsifier on record)."""
        organs = ["lineage-smith", "rival-playbook"]
        skills_root = os.path.join(_TREE_ROOT, "skills")
        for organ in organs:
            path = os.path.join(skills_root, organ, "references",
                                "forge-os.md")
            self.assertTrue(os.path.isfile(path),
                            "%s: forge-os.md missing" % organ)
            with open(path, encoding="utf-8") as fh:
                body = fh.read()
            for token in ("The thinking framework",
                          "The behavioral protocol",
                          "The scripting arsenal",
                          "The rigid run-order",
                          "Falsifiers",
                          "The opening ladder",
                          "Ranking rationale",
                          "Generation falsifier"):
                self.assertIn(token, body,
                              "%s: forge runtime incomplete (%s)"
                              % (organ, token))

    def test_payload_kit_depth(self):
        """A19's lock: the payload organs' corpora carry the
        deepened classes — corpus_version 1.1.0 on record (1.2.0 on the
        vault-wave organs), the new
        entry ids present, every entry schema-complete (probe, oracle,
        failure modes, attributed source), and every FAMILY-id
        citation in the organ's markdown resolves to a real corpus
        entry: a kit row that names probe bytes must cite the
        versioned corpus, never a prose reference — hand-crafting is
        the defect the corpus discipline forbids. The covered organ
        set grows only by execution: the second wave joins the seam
        organ (signal-smith, corpus SIG 1.0.0) and walks the spine's
        coordinator kit (toolkit-and-canaries.md), whose FAMILY-id
        tokens must resolve against the organ corpora they name; the
        third wave deepens the extreme tier behind the weapons vault
        (INJ-016, XSS-016 — released only through payload_release); the
        fourth wave extends the vault to the desync and cache organs
        (DS-013/014, CACHE-011/012 — the H2.TE downgrade, the 0.CL
        early-response gadget seam, the smuggled poison and deception
        chains, same gate, same discipline); the fifth wave carries the
        ssrf/prototype credential-and-gadget seams (SSRF-013/014 — the
        IMDSv2 token dance and the Azure managed-identity token;
        PP-013/014 — the browser fetch-body default and the GTM
        sequence gadget) and the live-event php2shell forensics organ
        joins the covered set (P2S-001..008, corpus 1.0.0 — the
        CVE-2026-109618/109619 assessment arc)."""
        organs = {
            "xss-playbook": ("XSS", ["XSS-012", "XSS-013", "XSS-014",
                                     "XSS-015", "XSS-016"]),
            "injection-lab": ("INJ", ["INJ-011", "INJ-012", "INJ-013",
                                      "INJ-014", "INJ-015", "INJ-016"]),
            "ssrf-playbook": ("SSRF", ["SSRF-011", "SSRF-012",
                                      "SSRF-013", "SSRF-014"]),
            "desync-hunter": ("DS", ["DS-010", "DS-011", "DS-012",
                                     "DS-013", "DS-014"]),
            "cache-playbook": ("CACHE", ["CACHE-010", "CACHE-011",
                                       "CACHE-012"]),
            "prototype-playbook": ("PP", ["PP-011", "PP-012",
                                        "PP-013", "PP-014"]),
            "php2shell-forensics": ("P2S", ["P2S-001", "P2S-002",
                                          "P2S-003", "P2S-004",
                                          "P2S-005", "P2S-006",
                                          "P2S-007", "P2S-008"]),
            "signal-smith": ("SIG", ["SIG-001", "SIG-002", "SIG-003",
                                     "SIG-004", "SIG-005", "SIG-006",
                                     "SIG-007", "SIG-008", "SIG-009",
                                     "SIG-010"]),
        }
        skills_root = os.path.join(_TREE_ROOT, "skills")
        corpora = {}
        for organ, (family, new_ids) in organs.items():
            corpus_path = os.path.join(skills_root, organ, "references",
                                      "corpus.json")
            with open(corpus_path, encoding="utf-8") as fh:
                corpus = json.load(fh)
            expected_version = {"signal-smith": "1.0.0",
                                "xss-playbook": "1.2.0",
                                "injection-lab": "1.2.0",
                                "desync-hunter": "1.2.0",
                                "cache-playbook": "1.2.0",
                                "ssrf-playbook": "1.2.0",
                                "prototype-playbook": "1.2.0",
                                "php2shell-forensics": "1.0.0"}.get(
                                    organ, "1.1.0")
            self.assertEqual(corpus["corpus_version"], expected_version,
                             "%s: corpus_version not bumped" % organ)
            ids = {e["id"] for e in corpus["entries"]}
            for new_id in new_ids:
                self.assertIn(new_id, ids,
                              "%s: %s missing" % (organ, new_id))
            for entry in corpus["entries"]:
                for field in ("id", "technique", "prerequisites",
                              "probe", "oracle", "failure_modes",
                              "source"):
                    self.assertIn(field, entry,
                                  "%s: %s lacks %s"
                                  % (organ, entry.get("id", "?"), field))
                self.assertIn("url", entry["source"])
                self.assertTrue(entry["failure_modes"])
            corpora[organ] = ids
            pattern = re.compile(r"\b%s-[0-9]{3}\b" % family)
            for dirpath, _dirnames, filenames in os.walk(
                    os.path.join(skills_root, organ)):
                for fname in filenames:
                    if not fname.endswith(".md"):
                        continue
                    with open(os.path.join(dirpath, fname),
                              encoding="utf-8") as fh:
                        body = fh.read()
                    for token in set(pattern.findall(body)):
                        self.assertIn(token, ids,
                                      "%s: %s cites unknown %s"
                                      % (organ, fname, token))
        spine_kit = os.path.join(skills_root, "mythos-bug-hunter",
                                 "references", "toolkit-and-canaries.md")
        with open(spine_kit, encoding="utf-8") as fh:
            spine_body = fh.read()
        spine_pattern = re.compile(
            r"\b((?:XSS|INJ|SSRF|DS|CACHE|PP|SIG)-[0-9]{3})\b")
        organ_by_family = {
            "XSS": "xss-playbook", "INJ": "injection-lab",
            "SSRF": "ssrf-playbook", "DS": "desync-hunter",
            "CACHE": "cache-playbook", "PP": "prototype-playbook",
            "SIG": "signal-smith",
        }
        for token in sorted(set(spine_pattern.findall(spine_body))):
            family = token.partition("-")[0]
            self.assertIn(
                token, corpora[organ_by_family[family]],
                "spine toolkit-and-canaries cites unknown %s" % token)

    def test_attribution_corrections_are_on_record(self):
        registry = _mythos.mythos_lineages()
        corrections = {e["organ"]: e["correction"] for e in
                       registry["lineages"]}
        self.assertIsNone(corrections["scan-economist"])
        self.assertIn("Nizamul Rana", corrections["template-scanner"])
        self.assertIn("PhonePe", corrections["packet-orchestrator"])
        self.assertIn("Skappen", corrections["packet-orchestrator"])
        self.assertIn("Frans Rosen", corrections["auth-boundary-mapper"])
        self.assertIn("unauthorized", corrections["ghost-crawler"])
        self.assertIn("translation", corrections["trust-graph-hunter"])
        self.assertIn("Bernstein", corrections["protocol-forensics"])
        self.assertIn("Jurczyk", corrections["interior-cartographer"])

    def test_interior_cartographer_lineage_entry(self):
        """Q2's retirement record: the second candidate-queue execution
        is wired with the figure, the distillation, and the Jurczyk
        attribution correction on record."""
        registry = _mythos.mythos_lineages()
        by_organ = {e["organ"]: e for e in registry["lineages"]}
        entry = by_organ["interior-cartographer"]
        self.assertIn("Project Zero", entry["figure"])
        self.assertIn("boundary taxonomy", entry["distillation"])
        self.assertIn("interior-cartographer/references/sources.md",
                      entry["sources"])
        self.assertIn("Jurczyk", entry["correction"])

    def test_harness_smith_lineage_entry(self):
        """Q5's retirement record: the third candidate-queue execution
        is wired with the figure, the distillation, the bounded census
        (the enormous tracker corpus stated as bounded, not line-read),
        and the quarantined-anecdote correction on record."""
        registry = _mythos.mythos_lineages()
        by_organ = {e["organ"]: e for e in registry["lineages"]}
        entry = by_organ["harness-smith"]
        self.assertIn("Project Zero", entry["figure"])
        self.assertIn("Zenbleed", entry["figure"])
        for token in ("privileged parser", "census", "oracle",
                      "missed-why"):
            self.assertIn(token, entry["distillation"])
        self.assertIn("bounded", entry["sources"])
        self.assertIn("quarantined", entry["correction"])

    def test_probe_smith_lineage_entry(self):
        """Q3's retirement record: the fourth candidate-queue execution
        is wired with the figure, the distillation, the consolidated
        census (the scattered talk corpus gathered via the consolidated
        talk record before any psych-read line landed), and the
        persona/quarantine corrections on record."""
        registry = _mythos.mythos_lineages()
        by_organ = {e["organ"]: e for e in registry["lineages"]}
        entry = by_organ["probe-smith"]
        self.assertIn("Travis Goodspeed", entry["figure"])
        self.assertIn("Microcontroller Exploits", entry["figure"])
        for token in ("probeable interface", "lock-bypass ladder",
                      "promiscuity", "parts list"):
            self.assertIn(token, entry["distillation"])
        self.assertIn("bounded", entry["sources"])
        self.assertIn("sources.md", entry["sources"])
        self.assertIn("quarantined", entry["correction"])
        self.assertIn("aesthetic only", entry["correction"])

    def test_metcalf_upgrade_entry(self):
        """Q7's retirement record: the fifth candidate-queue execution
        is the queue's standing demonstration that an UPGRADE is an
        assimilation too — the Sean Metcalf directory-interior layer
        folded into trust-graph-hunter with the eight-source census,
        the priced path matrix, the tier gate carrying the
        double-reset law, the paired detection rows with rot
        caveats, the bounded census stated, and the attribution
        ledger (Delpy, Le Toux, Medin) kept in the correction field
        alongside the Mitnick translation note."""
        registry = _mythos.mythos_lineages()
        by_organ = {e["organ"]: e for e in registry["lineages"]}
        entry = by_organ["trust-graph-hunter"]
        self.assertIn("Kevin Mitnick", entry["figure"])
        self.assertIn("Sean Metcalf", entry["figure"])
        self.assertIn("ADSecurity.org", entry["figure"])
        for token in ("eight-source", "priced attack-path matrix",
                      "tier", "double-reset", "detection row",
                      "rot caveat"):
            self.assertIn(token, entry["distillation"])
        self.assertIn("read in full", entry["sources"])
        self.assertIn("BOUNDED", entry["sources"])
        self.assertIn("skills/trust-graph-hunter/references/sources.md",
                      entry["sources"])
        self.assertIn("translation", entry["correction"])
        self.assertIn("Delpy", entry["correction"])
        self.assertIn("Le Toux", entry["correction"])
        self.assertIn("Medin", entry["correction"])
        self.assertIn("quarantined", entry["correction"])

    def test_opsec_discipline_lineage_entry(self):
        """Q4's retirement record: the sixth candidate-queue execution
        is wired with the figure (the maintained pseudonym, the @stake
        firing over Phrack 59, the 2002-2018 corpus arc), the
        distillation (campaign hygiene priced as an economic
        discipline: the exposure census, the plumbing-first law,
        compartmentation with identity/activity/association, cover
        over concealment, the suspect pool, the priced closure), the
        bounded census stated (decks and the 2013 blog cycle read in
        full; videos, Phrack full text, and tool trees bounded), and
        the on-record translation correction (the clandestine
        framing re-targeted to authorized engagements)."""
        registry = _mythos.mythos_lineages()
        by_organ = {e["organ"]: e for e in registry["lineages"]}
        entry = by_organ["opsec-discipline"]
        self.assertIn("the grugq", entry["figure"])
        self.assertIn("Phrack 59", entry["figure"])
        self.assertIn("Ekoparty", entry["figure"])
        self.assertIn("COMSEC", entry["figure"])
        for token in ("detection", "plumbing", "paranoia doesn't work "
                      "retroactively", "suspect pool", "cover",
                      "never destroyed"):
            self.assertIn(token, entry["distillation"])
        self.assertIn("read in full", entry["sources"])
        self.assertIn("BOUNDED", entry["sources"])
        self.assertIn("skills/opsec-discipline/references/sources.md",
                      entry["sources"])
        self.assertIn("translated", entry["correction"])
        self.assertIn("authorized-engagement", entry["correction"])
        self.assertIn("Ben Nagy", entry["correction"])
        self.assertIn("quarantined", entry["correction"])

    def test_mythos_bug_hunter_onboarding_lineage_entry(self):
        """Q6's retirement record: the seventh candidate-queue execution
        is the spine's first documented lineage UPGRADE — the
        methodology-preservation layer on the onboarding path. The
        registry entry carries the figure (the versioned deck chain
        2015-2024), the distillation (pin/split/gate/classify/proof/
        drift), the version-pinned census with its BOUNDED rows, and
        the curation-attribution correction; the spine itself carries
        both layers born in (method-upgrade.md and operator-os.md,
        the 35th and 30th of their sets)."""
        registry = _mythos.mythos_lineages()
        by_organ = {e["organ"]: e for e in registry["lineages"]}
        entry = by_organ["mythos-bug-hunter"]
        self.assertIn("Jason Haddix", entry["figure"])
        self.assertIn("DEF CON 23", entry["figure"])
        self.assertIn("LevelUp 0x02", entry["figure"])
        self.assertIn("Fast Testing Checklist", entry["figure"])
        for token in ("methodology packaging", "PIN the corpus state",
                      "SPLIT method from curation",
                      "checklists to gates", "CLASSIFY every number",
                      "PROOF gate", "DRIFT audit"):
            self.assertIn(token, entry["distillation"])
        self.assertIn("read in full", entry["sources"])
        self.assertIn("BOUNDED", entry["sources"])
        self.assertIn("skills/mythos-bug-hunter/references/sources.md",
                      entry["sources"])
        self.assertIn("the tools are theirs", entry["correction"])
        self.assertIn("WAHH", entry["correction"])
        self.assertIn("quarantined", entry["correction"])
        # the upgraded organ carries both layers, born in
        skills_root = os.path.join(_TREE_ROOT, "skills")
        spine = os.path.join(skills_root, "mythos-bug-hunter")
        with open(os.path.join(spine, "SKILL.md"),
                  encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn("version: 4.8.0", text)
        self.assertIn("Jason Haddix", text)
        for module in ("references/method-upgrade.md",
                       "references/operator-os.md",
                       "references/sources.md"):
            path = os.path.join(spine, module)
            self.assertTrue(os.path.isfile(path),
                             "spine layer missing: %s" % module)

    def test_threshold_hunter_lineage_entry(self):
        """Q8's retirement record: the eighth and final candidate-queue
        execution is wired with the figure (the documented career —
        TOOOL board 14 years, The CORE Group, Red Team Alliance, the
        certifications, the talk index 2005-2024), the distillation
        (the physical trust boundary translated to the information
        layer: the cost-ordered entry ladder, the egress reversal,
        OR-logic privilege leakage by component isolation, installation
        over design, detection as the deliverable, the fix-pair), the
        bounded census stated (the free chain read in full — the talk
        index, the bio, the Darknet Diaries transcript, Blaze's essay,
        the Wiegand and OSDP records — with the books and videos
        BOUNDED), and the correction row carrying the engagement-fit
        verdict: physical execution bounded as human-operator craft,
        no pretexting, no life-safety actuation, and the fit gate
        argued and closed BEFORE drafting."""
        registry = _mythos.mythos_lineages()
        by_organ = {e["organ"]: e for e in registry["lineages"]}
        entry = by_organ["threshold-hunter"]
        self.assertIn("Deviant Ollam", entry["figure"])
        self.assertIn("TOOOL", entry["figure"])
        self.assertIn("DEF CON 22", entry["figure"])
        self.assertIn("I'll Let Myself In", entry["figure"])
        for token in ("cost-ordered", "egress", "OR-logic",
                      "component isolation", "installation beats design",
                      "detection is the deliverable", "fix-pair",
                      "OSDP"):
            self.assertIn(token, entry["distillation"])
        self.assertIn("read in full", entry["sources"])
        self.assertIn("BOUNDED", entry["sources"])
        self.assertIn("skills/threshold-hunter/references/sources.md",
                      entry["sources"])
        self.assertIn("human-operator", entry["correction"])
        self.assertIn("no human pretexting", entry["correction"])
        self.assertIn("life-safety", entry["correction"])
        self.assertIn("Matt Blaze", entry["correction"])
        self.assertIn("BEFORE drafting", entry["correction"])
        # the organ carries both layers, born in
        skills_root = os.path.join(_TREE_ROOT, "skills")
        organ = os.path.join(skills_root, "threshold-hunter")
        with open(os.path.join(organ, "SKILL.md"),
                  encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn("version: 1.1.0", text)
        self.assertIn("Deviant Ollam", text)
        for module in ("references/method-upgrade.md",
                       "references/operator-os.md",
                       "references/sources.md"):
            path = os.path.join(organ, module)
            self.assertTrue(os.path.isfile(path),
                            "organ layer missing: %s" % module)

    def test_second_wave_lineage_organs_are_v2(self):
        """The six v2 organs carry the lineage in frontmatter, not
        just in the registry — the SKILL.md metadata and the registry
        entry must agree. Since the WWH re-edit (A14) the version is a
        floor (2.x), not a pin: minor bumps are the house semver."""
        registry = _mythos.mythos_lineages()
        by_organ = {e["organ"]: e for e in registry["lineages"]}
        skills_root = os.path.join(_TREE_ROOT, "skills")
        for organ in ("subdomain-hunter", "xss-playbook",
                      "oauth-flow-auditor", "content-discovery",
                      "business-logic-hunter", "cloud-config-auditor"):
            path = os.path.join(skills_root, organ, "SKILL.md")
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            m = re.search(r"^version: (2\.(\d+))\.(\d+)$", text, re.M)
            self.assertIsNotNone(m, "%s: not a v2.x organ" % organ)
            self.assertIn("lineage:", text, organ)
            figure = by_organ[organ]["figure"]
            surname = figure.split("(")[0].split("—")[0].strip()
            self.assertIn(surname, text,
                          "%s: figure %r not in SKILL.md lineage"
                          % (organ, surname))


# --------------------------------------------------------- vrt_classify

class TestVrtClassify(unittest.TestCase):
    def test_ssrf_variants(self):
        hot = _mythos.vrt_classify("ssrf", internal=True, sensitive=True)
        self.assertEqual(hot["vrt_id"],
                         "server_security_misconfiguration."
                         "server_side_request_forgery_ssrf."
                         "internal_secrets_exposure")
        self.assertEqual(hot["p"], 2)
        self.assertEqual(hot["hackerone_severity"], "High")
        cold = _mythos.vrt_classify("ssrf", internal=False)
        self.assertTrue(cold["vrt_id"].endswith("external_low_impact"))
        self.assertEqual(cold["p"], 5)
        self.assertEqual(cold["cvss_template"]["base_score"], 0.0)

    def test_idor_variants(self):
        read = _mythos.vrt_classify("idor", sensitive=True)
        self.assertTrue(read["vrt_id"].endswith(
            "view_sensitive_information_iterable_object_identifiers"))
        self.assertEqual(read["p"], 3)
        write = _mythos.vrt_classify("idor", sensitive=True,
                                     scope_changed=True)
        self.assertTrue(write["vrt_id"].endswith(
            "modify_view_sensitive_information_iterable_object_identifiers"))
        self.assertEqual(write["p"], 1)
        trivial = _mythos.vrt_classify("idor", sensitive=False)
        self.assertEqual(trivial["p"], 5)
        self.assertEqual(trivial["cvss_template"]["base_score"], 5.3)

    def test_xss_variants(self):
        refl = _mythos.vrt_classify("xss_reflected")
        self.assertEqual(refl["p"], 3)
        self.assertEqual(refl["cvss_template"]["base_score"], 6.1)
        self_xss = _mythos.vrt_classify("xss_reflected", self_only=True)
        self.assertEqual(self_xss["p"], 5)
        stored = _mythos.vrt_classify("xss_stored")
        self.assertEqual(stored["p"], 2)

    def test_fixed_priority_classes(self):
        self.assertEqual(_mythos.vrt_classify("auth_bypass")["p"], 1)
        self.assertEqual(_mythos.vrt_classify("auth_bypass")
                         ["hackerone_severity"], "Critical")
        self.assertEqual(_mythos.vrt_classify("exposed_debug_portal")["p"], 3)
        admin = _mythos.vrt_classify("exposed_debug_portal", admin=True)
        self.assertEqual(admin["p"], 1)

    def test_all_mapped_vrt_ids_resolve_in_shipped_taxonomy(self):
        for klass in _mythos.FINDING_CLASSES:
            result = _mythos.vrt_classify(klass)
            self.assertTrue(result["taxonomy_resolved"],
                            "%s -> %s not in shipped taxonomy"
                            % (klass, result["vrt_id"]))

    def test_varies_classes_flag_context(self):
        ssti = _mythos.vrt_classify("ssti")
        self.assertIsNone(ssti["p"])
        self.assertIn("Varies", ssti["priority"])
        self.assertIn("context", " ".join(ssti["notes"]))

    def test_context_flags_shape_cvss_template(self):
        authed = _mythos.vrt_classify("idor", authenticated=True)
        self.assertIn("PR:L", authed["cvss_template"]["vector"])
        self.assertEqual(authed["cvss_template"]["base_score"], 6.5)

    def test_unknown_class_raises_with_supported_list(self):
        with self.assertRaises(ValueError) as cm:
            _mythos.vrt_classify("time_travel")
        self.assertIn("supported classes", str(cm.exception))
        self.assertIn("sql_injection", str(cm.exception))

    def test_class_name_normalization(self):
        quiet = _mythos.vrt_classify("SQL Injection")
        self.assertEqual(quiet["vrt_id"],
                         _mythos.vrt_classify("sql_injection")["vrt_id"])


# ------------------------------------------------------ auditor gates

_GOOD = """# Report

### H-001 — Unauthenticated debug route (facts R-001)

- claim: unauthenticated read of diagnostic state (R-001)
- Closure: CONFIRMED (E-001: R-003; closure R-004)
- severity: low (records R-001, R-003)
- impact-chain: one bounded read of the banner (R-003)
- canary attestation: self-owned lab only (AUTH R-000)
- cvss: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N = 5.3 (records R-001)
- vrt: server_security_misconfiguration.exposed_portal.non_admin_portal [P3] (records R-001)
- reproduction: E-001 — GET /debug, n_runs 3

### E-001 — differential probe

- baseline: R-002 (401, 3/3)
- n_runs: 3
"""


class TestReportGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit_mod = _auditor()

    def _audit_text(self, text):
        fd, path = tempfile.mkstemp(suffix=".md")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        try:
            return self.audit_mod.audit(path)
        finally:
            os.unlink(path)

    def _fails(self, text):
        return [msg for status, msg in self._audit_text(text)
                if status == "FAIL"]

    def test_good_report_passes_classification_gates(self):
        results = self._audit_text(_GOOD)
        self.assertEqual([m for s, m in results if s == "FAIL"], [])
        self.assertIn("H-001 CONFIRMED finding carries the full "
                      "classification set",
                      " ".join(m for _s, m in results))

    def test_missing_cvss_line_fails(self):
        fails = self._fails(_GOOD.replace(
            "- cvss: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N = 5.3 "
            "(records R-001)\n", ""))
        self.assertTrue(any("cvss" in m and "lacks" in m or "no cvss" in m
                            for m in fails), fails)

    def test_score_mismatch_fails_with_recomputed_value(self):
        bad = _GOOD.replace("= 5.3", "= 7.5")
        fails = self._fails(bad)
        self.assertTrue(any("cvss score mismatch" in m and "5.3" in m
                            for m in fails), fails)

    def test_bogus_vrt_category_fails(self):
        bad = _GOOD.replace(
            "server_security_misconfiguration.exposed_portal."
            "non_admin_portal", "totally.made_up.category")
        fails = self._fails(bad)
        self.assertTrue(any("not found in the shipped taxonomy" in m
                            for m in fails), fails)

    def test_vrt_without_p_rating_fails(self):
        bad = _GOOD.replace("[P3]", "baseline")
        fails = self._fails(bad)
        self.assertTrue(any("no P-rating" in m for m in fails), fails)

    def test_missing_reproduction_fails(self):
        # the E-001 id in the Closure line itself counts as the
        # reproduction reference — remove BOTH to prove the gate bites
        bad = _GOOD.replace(
            "- reproduction: E-001 — GET /debug, n_runs 3\n", "")
        bad = bad.replace("Closure: CONFIRMED (E-001: R-003; closure R-004)",
                          "Closure: CONFIRMED (R-003; closure R-004)")
        fails = self._fails(bad)
        self.assertTrue(any("reproduction reference" in m for m in fails),
                        fails)

    def test_incident_handoff_risk_line_skips_classification_gates(self):
        handoff = """# Adversary handoff

### H-004 compromised container

Risk: high — unauthorized actor with valid credentials — R-009
- Closure: CONFIRMED — R-008, R-009
- impact-chain: login anomaly to confirmed access (R-001, R-008)
- canary: none during the trace — TIP-OFF discipline held (R-003)
"""
        fails = self._fails(handoff)
        self.assertEqual(fails, [], fails)

    def test_summary_sections_do_not_leak_into_blocks(self):
        # a severity line under a ## section after the finding block must
        # NOT arm the classification gates for that block (strict blocks)
        sneaky = _GOOD + """## Impact

- severity: low (records R-001) — summary restating
"""
        fails = self._fails(sneaky)
        self.assertEqual(fails, [], fails)


if __name__ == "__main__":
    unittest.main()
