"""Payload release gate — the weapons vault (R0 + A19 operationalized).

The corpora hold extreme-tier probe classes (time-based blind oracles,
mutation XSS, parser desync). They are transcribed, attributed, and
versioned — and they leave the vault through ONE door, this gate:

  1. instruction-override scan of every string the caller passed —
     "ignore previous instructions", "no authorization needed",
     "act as if authorized" — the gate does not negotiate with its
     own instructions; the attempt is refused and ledgered.
  2. corpus resolution — an entry id that matches no versioned corpus
     entry never releases (A19: hand-crafted bytes are the defect).
  3. banned-class scan — destructive impact and weaponization classes
     (DDL/DML destruction, file-write implants, command execution
     implants, C2/malware tooling) are banned from the vault outright;
     there is no tier, no scope row, and no parameter that releases
     them. The vault has no door for weaponized classes.
  4. scope check — deny-by-default through scope_gate.check_target
     (active=True: the probe is headed to a target).

The gate is a pure function of its arguments (A4): no environment
variable, no override flag, no bulk-dump path exists in the API
surface. One entry per call — the vault never sprays.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

from . import paths
from .scope_gate import check_target

TIERS = ("T1", "T2", "T3")

# --- instruction-override attempts (the jailbreak surface) --------------
# English phrasings, structural: verb-of-dismissal against the rule
# artifacts (instructions/scope/authorization/gate), pretended
# authorization, mode-escalation roleplay, bypass verbs.
JAILBREAK_PATTERNS = tuple(re.compile(p, re.IGNORECASE) for p in (
    r"ignore\s+(all\s+|any\s+)?(previous|prior|above|earlier|earlier)\s+"
    r"(instructions|rules|directives|constraints|prompts)",
    r"ignore\s+(the\s+)?(scope|gate|authorization|rules|safety)",
    r"disregard\s+(the\s+|all\s+|any\s+)?(instructions|rules|scope|"
    r"authorization|gate|safety|guardrails?)",
    r"override\s+(the\s+)?(scope|authorization|gate|rules|safety|guard)",
    r"no\s+(authorization|scope|permission)\s+(is\s+)?"
    r"(needed|required|necessary)",
    r"pretend\s+(that\s+)?(you\s+(are|'re)\s+|you're\s+|youre\s+)?"
    r"(authorized|approved|"
    r"scoped|allowed)",
    r"act\s+as\s+if\s+(you('re| are)\s+)?(authorized|scoped|allowed)",
    r"you\s+are\s+now\s+(in\s+)?(developer|god|dan|unrestricted|admin|"
    r"root|privileged)\s+mode",
    r"\bjailbreak\b",
    r"\bdan\s+mode\b",
    r"bypass\s+(the\s+)?(scope|gate|authorization|guard|filter|check)",
    r"(scope|authorization|rules|gates?)\s+(does\s+not|do\s+not|don't|"
    r"doesn't)\s+apply",
    r"skip\s+(the\s+)?(scope|authorization|gate|check)",
    r"emergency\s+(override|access|release)",
    r"off\s+the\s+(books|record)",
    r"(i\s+am|we're|we\s+are)\s+(already\s+)?(authorized|scoped)\b"
    r"(?!\s*(by|under|via|per)\s)",
    # --- second hardening wave: forget-verbs, pretended-authorization
    # verbs, mode-escalation verbs, prompt-exfiltration attempts ------
    # (third hardening pass, found by the vault accuracy bench: the
    # forget family also matches noun-before-positional order, e.g.
    # "forget the context above")
    r"forget\s+(all\s+|any\s+|everything\s+|the\s+)?"
    r"((previous|prior|above|earlier|initial)\s+"
    r"(instructions|rules|directives|constraints|prompts|context)|"
    r"(instructions|rules|directives|constraints|prompts|context)\s+"
    r"(above|earlier|before))",
    r"forget\s+(everything|all|anything)\s+"
    r"(you('ve| have)\s+been\s+told|above|before\s+now)",
    r"treat\s+(this|it|that|me|us)\s+as\s+"
    r"(authorized|approved|scoped|allowed|in\s+scope)",
    r"assume\s+(i\s+am|we\s+are|you\s+are|you're)\s+"
    r"(authorized|scoped|allowed|approved|permitted)"
    r"(?!\s*(by|under|via|per)\s)",
    r"(switch|enter|enable|activate|toggle)\s+(to\s+|into\s+)?"
    r"(developer|god|dan|admin|root|privileged|unrestricted|"
    r"unfiltered|uncensored)\s+mode",
    r"(reveal|show|print|dump|expose|repeat|output)\s+(me\s+)?"
    r"(your|the)\s+(system\s+prompt|hidden\s+instructions|"
    r"initial\s+instructions|full\s+instructions)",
))

# --- weaponized / destructive-only classes: banned outright --------------
# Detection oracles (delay pairs, mutation vectors, boolean differentials)
# are standard authorized-testing classes. What the vault refuses to hold
# AT ALL is destruction-as-impact and weaponization: DDL/DML destruction,
# file-write implants, command-execution implants, C2 and malware tooling.
BANNED_PATTERNS = tuple(re.compile(p, re.IGNORECASE) for p in (
    r"\bdrop\s+(table|database|schema|index)\b",
    r"\btruncate\s+(table|partition)\b",
    r"\bdelete\s+from\s+\w",
    r"\balter\s+table\b",
    r"\bshutdown\b",
    r"\binto\s+(out|dump)file\b",
    r"\bxp_cmdshell\b",
    r"\bsp_addextendedproc\b",
    r"\b(attach|create)\s+database\b",
    r"\bmsfvenom\b|\bmeterpreter\b|\bwebshell\b|\bbackdoor\b",
    r"\b(c2|command[_ -]?and[_ -]?control)\s+(server|channel|beacon)\b",
    r"\bransomware\b|\bcryptolocker\b",
    r"\bkeylogger\b|\bscreen[_ -]?scraper\s+implant\b",
    r"\bpersist(ence|ent)\s+(implant|hook|backdoor)\b",
    r"\brm\s+-rf\s+/",
))

# --- tier rules (deterministic, checked T3 first: extreme wins) ---------
_T3_HINTS = ("time-based", "timing oracle", "mutation xss", "mxss",
             "smuggl", "desync", "poison", "pollution", "gadget",
             "chain", "delay", "sleep", "benchmark", "exfiltrat")
_T1_HINTS = ("detection", "marker", "canary", "encoding", "grammar",
             "signature", "comment-context", "arithmetic")
_T2_HINTS = ("boolean", "differential", "error", "union", "context",
             "sink", "takeover", "redirect", "callback", "oracle")

CORPUS_RELPATH = os.path.join("references", "corpus.json")


@dataclass
class ReleaseResult:
    released: bool
    reason: str
    ledger_tag: str
    entry_id: str
    tier: str
    organ: str
    corpus_version: str
    technique: str
    probe: str
    source_url: str
    scope: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            "released": self.released,
            "reason": self.reason,
            "ledger_tag": self.ledger_tag,
            "entry": {
                "id": self.entry_id,
                "tier": self.tier,
                "organ": self.organ,
                "corpus_version": self.corpus_version,
                "technique": self.technique,
                "probe": self.probe,
                "source": self.source_url,
            },
            "scope": self.scope,
        }


def _scan_blob(*texts: str) -> str:
    """Fold every caller-supplied string into one lowercase scan blob,
    decoding the trivial obfuscations first (+ and %20 as space)."""
    blob = " \n ".join(t or "" for t in texts).lower()
    return blob.replace("+", " ").replace("%20", " ")


def jailbreak_hit(*texts: str) -> re.Pattern | None:
    """Return the first instruction-override pattern found in texts."""
    blob = _scan_blob(*texts).replace("_", " ")
    for pattern in JAILBREAK_PATTERNS:
        if pattern.search(blob):
            return pattern
    return None


def banned_hit(*texts: str) -> re.Pattern | None:
    """Return the first weaponized/destructive pattern found in texts.

    Underscores are preserved here (xp_cmdshell, reverse_tcp) — the
    banned vocabulary is technical, not prose.
    """
    blob = _scan_blob(*texts)
    for pattern in BANNED_PATTERNS:
        if pattern.search(blob):
            return pattern
    return None


def classify_tier(entry: dict) -> str:
    """T1 marker/detection, T2 standard probe, T3 extreme.

    T3 wins over T1 when both match (a detectable extreme class is still
    extreme); anything matching no known hint classifies T3 too — the
    conservative default is the most restricted tier, never the loosest.
    """
    text = "%s %s" % (entry.get("technique", ""), entry.get("probe", ""))
    text = text.lower()
    if any(h in text for h in _T3_HINTS):
        return "T3"
    if any(h in text for h in _T1_HINTS):
        return "T1"
    if any(h in text for h in _T2_HINTS):
        return "T2"
    return "T3"


def load_corpora(skills_root: str | None = None) -> dict[str, tuple]:
    """Walk every organ that ships references/corpus.json (the covered
    organ set grows only by execution — A19).

    Returns {entry_id: (organ, corpus_version, entry_dict)}.
    """
    root = skills_root or paths.skills_dir()
    corpora: dict[str, tuple] = {}
    if not os.path.isdir(root):
        return corpora
    import json
    for organ in sorted(os.listdir(root)):
        corpus_path = os.path.join(root, organ, CORPUS_RELPATH)
        if not os.path.isfile(corpus_path):
            continue
        with open(corpus_path, encoding="utf-8") as fh:
            corpus = json.load(fh)
        version = str(corpus.get("corpus_version", ""))
        for entry in corpus.get("entries", []):
            corpora[str(entry.get("id", ""))] = (organ, version, entry)
    return corpora


def vault_status(skills_root: str | None = None) -> dict:
    """Inspect-only posture: tier counts per organ, banned and jailbreak
    pattern counts. No probe bytes leave through this call."""
    counts: dict[str, dict[str, int]] = {}
    for _eid, (organ, _ver, entry) in sorted(
            load_corpora(skills_root).items()):
        tier = classify_tier(entry)
        counts.setdefault(organ, {"T1": 0, "T2": 0, "T3": 0})
        counts[organ][tier] += 1
    return {
        "organs": counts,
        "entries_total": sum(sum(c.values()) for c in counts.values()),
        "banned_patterns": len(BANNED_PATTERNS),
        "jailbreak_patterns": len(JAILBREAK_PATTERNS),
        "policy": "one entry per call; deny-by-default scope check; "
                  "instruction-override attempts refused and ledgered; "
                  "weaponized classes banned outright; no override "
                  "parameter exists",
    }


def release_payload(entry_id: str, target: str,
                    operator_note: str = "",
                    scope_path: str | None = None) -> ReleaseResult:
    """The vault door. One versioned entry, one scope-authorized target.

    Refusal order: jailbreak scan -> corpus resolution -> banned-class
    scan -> scope check. Every refusal carries its reason; the caller
    ledger-records it (tag REFUSED) exactly like the scope gate doctrine.
    """
    empty = dict.fromkeys(
        ("tier", "organ", "corpus_version", "technique", "probe",
         "source_url"), "")

    def refuse(reason: str, tag: str = "REFUSED") -> ReleaseResult:
        return ReleaseResult(False, reason, tag, entry_id, "", "", "",
                             "", "", "")

    # 1. instruction-override scan over EVERY caller-supplied string —
    #    the gate does not parse intent, it matches structure.
    hit = jailbreak_hit(entry_id, target, operator_note)
    if hit is not None:
        return refuse(
            "vault: instruction-override attempt (%r) — the release gate "
            "does not negotiate with its own instructions; the refusal is "
            "ledgered and the attempt is on record" % hit.pattern)

    # 2. corpus resolution — the vault releases only transcribed,
    #    attributed, versioned entries (A19).
    corpora = load_corpora()
    resolved = corpora.get(entry_id.strip())
    if resolved is None:
        return refuse(
            "vault: %r matches no versioned corpus entry — the vault "
            "releases only transcribed, attributed entries; hand-crafted "
            "bytes are the defect the corpus discipline forbids (A19)"
            % entry_id)
    organ, corpus_version, entry = resolved
    technique = str(entry.get("technique", ""))
    probe = str(entry.get("probe", ""))
    source_url = str((entry.get("source") or {}).get("url", ""))

    # 3. banned-class scan — permanent, no tier, no scope row, no
    #    parameter releases a weaponized class.
    banned = banned_hit(technique, probe)
    if banned is not None:
        return refuse(
            "vault: entry %s matches the banned-class list (%r) — "
            "destructive-impact and weaponization classes are banned "
            "from the corpus outright; the vault has no door for them"
            % (entry_id, banned.pattern))

    tier = classify_tier(entry)

    # 4. scope check — deny-by-default, active probe, artifact required.
    scope_result = check_target(target, active=True, scope_path=scope_path)
    if not scope_result.authorized:
        result = refuse(scope_result.reason)
        result.tier = tier
        result.organ = organ
        result.corpus_version = corpus_version
        result.scope = scope_result.as_dict()
        return result

    reason = ("released: %s tier %s (corpus %s %s) to authorized target "
              "%r — %s"
              % (entry_id, tier, organ, corpus_version, target,
                 scope_result.reason))
    if tier == "T3":
        reason += ("; EXTREME TIER: the differential pair is mandatory, "
                   "a single delayed or mutated observation stays a lead")
    return ReleaseResult(
        True, reason, "FACT", entry_id, tier, organ, corpus_version,
        technique, probe, source_url, scope_result.as_dict())
