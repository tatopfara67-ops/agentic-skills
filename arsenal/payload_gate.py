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
# Structural: verb-of-dismissal against the rule artifacts (instructions/
# scope/authorization/gate), pretended authorization, mode-escalation
# roleplay, bypass verbs. English carries the deep families; the fourth
# hardening wave extends the same structures across nine more languages
# (Indonesian deep, es/fr/de/pt/it/ru/zh/ja representative) — the gate
# does not negotiate with its own instructions in any covered language.
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
    # --- fourth hardening wave: the language-blindness gap --------------
    # The bench queue's own honest admission: every family above is
    # English-only, so the same structural attempt phrased in another
    # language sailed the scan untouched. The wave closes the gap the
    # structural way -- verb-of-dismissal against the rule artifacts,
    # pretended authorization, bypass verbs, mode escalation, one
    # representative form per family per language. The operator's
    # working language (Indonesian) is covered deep; the major
    # Romance/Germanic languages carry one structural form each;
    # Cyrillic and CJK ride \uXXXX escapes so the source stays pure
    # ASCII (the re engine reads \uXXXX as the character; real parens
    # remain the group syntax, and \s* between CJK tokens survives the
    # + / %20 folding the scan blob applies). The release side is
    # tested per language: clean basis-noted notes in every covered
    # language still release -- overblocking is a defect, not margin.
    # indonesian
    r"(meng)?abaikan\s+(semua\s+|segala\s+)?"
    r"(instruksi|perintah|aturan|konteks|prompt|skop|scope)"
    r"(\s+(di\s+atas|sebelumnya|sebelum\s+ini|tersebut))?",
    r"pura[\s-]?pura(\s+bahwa)?\s+(kamu\s+|anda\s+|kita\s+|saya\s+)?"
    r"(sudah\s+|telah\s+)?"
    r"(diizinkan|diberi\s+izin|berwenang|berotorisasi|disetujui)",
    r"anggap\s+saja\s+(kamu\s+|kita\s+|semuanya\s+)?(sudah\s+|telah\s+)?"
    r"(diizinkan|berwenang|disetujui|di\s+dalam\s+scope|aman)",
    r"tidak\s+(perlu|ada|butuh)\s+"
    r"(otorisasi|autorisasi|izin|persetujuan|validasi)",
    r"((me)?lewati|bypass)\s+(pemeriksaan\s+|validasi\s+)?"
    r"(otorisasi|autorisasi|gerbang|scope|lingkup)",
    r"lupakan\s+(semua\s+|segala\s+)?(yang\s+)?"
    r"(di\s+atas|sebelumnya|semua|konteks|instruksi|aturan)",
    r"mode\s+(dewa|pengembang|admin|root|tanpa\s+batas)|"
    r"(scope|lingkup|aturan)\s+(tidak|tak)\s+berlaku",
    # spanish
    r"ignora(r|ndo)?\s+(todas\s+las\s+|todos\s+los\s+|las\s+|los\s+|"
    r"la\s+|el\s+)?(instrucciones|reglas|indicaciones|contexto|todo)"
    r"(\s+(anteriores|previas|previos|de\s+arriba))?",
    r"(finge|simula)\s+que\s+.{0,24}(autorizado|aprobado|permitido)",
    r"no\s+(se\s+)?(necesita|requiere)\s+(ninguna\s+|ning\u00fan\s+)?"
    r"(autorizaci(o|\u00f3)n|permiso|aprobaci(o|\u00f3)n|"
    r"verificaci(o|\u00f3)n)",
    r"(salta|omite|evita)\s+(la\s+|el\s+|las\s+|los\s+|una?\s+)?"
    r"(verificaci(o|\u00f3)n|autorizaci(o|\u00f3)n|comprobaci(o|\u00f3)n|"
    r"puerta|filtros?)|olvida\s+(todo(\s+lo\s+anterior)?|"
    r"(todas\s+las\s+|las\s+|los\s+)?(instrucciones|reglas|"
    r"indicaciones)|el\s+contexto|lo\s+de\s+arriba)|modo\s+"
    r"(dios|desarrollador|administrador|sin\s+restricciones)",
    # french
    r"ignor(e|er|ez)\s+(les\s+|toutes\s+les\s+|tout\s+)?"
    r"(instructions|consignes|r(e|\u00e8)gles)"
    r"(\s+(pr(e|\u00e9)c(e|\u00e9)dentes|ci-dessus))?",
    r"(fais\s+comme\s+si|pr(e|\u00e9)tends\s+que)\s+.{0,40}"
    r"(autoris|approuv)",
    r"aucune\s+autoris(ation|(e|\u00e9)e)\s+n'?est\s+"
    r"(n(e|\u00e9)cessaire|requise)|(contourne|saute)\s+"
    r"(la\s+|le\s+|les\s+|une?\s+)?(v(e|\u00e9)rifications?|"
    r"autorisation|porte|contr(\u00f4|o)le|filtre)|mode\s+"
    r"(dieu|d(e|\u00e9)veloppeur|admin|sans\s+restrictions)",
    # german
    r"ignoriere\s+(die\s+|alle\s+|s(a|\u00e4)mlichen\s+)?"
    r"(vorherigen\s+|bisherigen\s+|obigen\s+)?"
    r"(anweisungen|regeln|instruktionen)",
    r"(stell\s+dir\s+vor|gib\s+vor).{0,32}"
    r"(autorisiert|befugt|genehmigt)",
    r"keine\s+(autorisierung|genehmigung|berechtigung)\s+"
    r"(n(o|\u00f6)tig|erforderlich|notwendig)|(umgehe|umgehen\s+sie)\s+"
    r"(die\s+|den\s+)?(autorisierung|pr(u|\u00fc)fung|kontrolle|sperre)|"
    r"vergiss\s+(alles\s+)?(dar(\u00fc|u)ber|oben|die\s+anweisungen|"
    r"den\s+kontext)",
    # portuguese + italian
    r"ignor(e|a)\s+(as\s+|todas\s+as\s+|os\s+|todos\s+os\s+)?"
    r"(instru(c|\u00e7)(o|\u00f5)es|regras|contexto)"
    r"(\s+(anteriores|acima))?|(finja|simule)\s+que\s+.{0,24}"
    r"(autorizado|aprovado|permitido)",
    r"ignora\s+(le\s+|tutte\s+le\s+|lo\s+|tutto\s+)?"
    r"(istruzioni|regole|contesto)"
    r"(\s+(precedenti|sopra|di\s+prima))?|fingi\s+di\s+(essere\s+)?"
    r"(autorizzato|approvato|abilitato)",
    # russian (cyrillic via escapes; source stays ascii)
    r"\u0438\u0433\u043d\u043e\u0440\u0438\u0440\u0443\u0439"
    r"(\u0442\u0435)?\s+(\u0432\u0441\u0435\s+)?"
    r"(\u043f\u0440\u0435\u0434\u044b\u0434\u0443\u0449\u0438\u0435\s+|"
    r"\u043f\u0440\u043e\u0448\u043b\u044b\u0435\s+)?"
    r"(\u0438\u043d\u0441\u0442\u0440\u0443\u043a\u0446\u0438\u0438|"
    r"\u043f\u0440\u0430\u0432\u0438\u043b\u0430|"
    r"\u0443\u043a\u0430\u0437\u0430\u043d\u0438\u044f|"
    r"\u043a\u043e\u043d\u0442\u0435\u043a\u0441\u0442)",
    r"\u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u044c,?\s*"
    r"\u0447\u0442\u043e\s+(\u0442\u044b\s+)?(\u0443\u0436\u0435\s+)?"
    r"(\u0430\u0432\u0442\u043e\u0440\u0438\u0437\u043e\u0432\u0430\u043d|"
    r"\u0443\u043f\u043e\u043b\u043d\u043e\u043c\u043e\u0447\u0435\u043d)",
    r"\u0440\u0435\u0436\u0438\u043c\s+(\u0431\u043e\u0433\u0430|"
    r"\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0430|"
    r"\u0430\u0434\u043c\u0438\u043d\u0430|"
    r"\u0431\u0435\u0437\s+\u043e\u0433\u0440\u0430\u043d\u0438\u0447\u0435"
    r"\u043d\u0438\u0439)|\u0437\u0430\u0431\u0443\u0434\u044c\s+"
    r"(\u0432\u0441\u0435,\s*\u0447\u0442\u043e\s+\u0432\u044b\u0448\u0435|"
    r"\u0432\u0441\u0435\s+\u043f\u0440\u0435\u0434\u044b\u0434\u0443\u0449"
    r"\u0435\u0435|\u043f\u0440\u0435\u0434\u044b\u0434\u0443\u0449\u0438"
    r"\u0435\s+\u0438\u043d\u0441\u0442\u0440\u0443\u043a\u0446\u0438\u0438)|"
    r"(\u043e\u0431\u043e\u0439\u0434\u0438|\u043f\u0440\u043e\u043f\u0443"
    r"\u0441\u0442\u0438)\s+(\u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0443|"
    r"\u0430\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u044e|"
    r"\u043a\u043e\u043d\u0442\u0440\u043e\u043b\u044c)",
    # mandarin (han via escapes; \s* between tokens survives folding)
    r"(\u5ffd\u7565|\u65e0\u89c6)\s*(\u4e4b\u524d|\u4ee5\u4e0a|"
    r"\u4e0a\u9762|\u5148\u524d|\u4e0a\u8ff0)?\s*\u7684?\s*"
    r"\u6240\u6709?\s*(\u6307\u4ee4|\u6307\u793a|\u89c4\u5219|"
    r"\u89c4\u5b9a)",
    r"\u5047\u88c5\s*\u4f60?\s*\u5df2\s*(\u83b7\u5f97|\u88ab)?\s*"
    r"(\u6388\u6743|\u8bb8\u53ef|\u6279\u51c6)|\u89c6\u4e3a\s*\u5df2\s*"
    r"(\u6388\u6743|\u8bb8\u53ef|\u6279\u51c6)|\u5f53\u4f5c\s*\u5df2\s*"
    r"(\u6388\u6743|\u8bb8\u53ef)",
    r"(\u65e0\u9700|\u4e0d\u9700\u8981)\s*(\u4efb\u4f55\s*)?"
    r"(\u6388\u6743|\u8bb8\u53ef|\u6279\u51c6|\u9a8c\u8bc1)|"
    r"\u7ed5\u8fc7\s*(\u6388\u6743|\u9a8c\u8bc1|\u68c0\u67e5|"
    r"\u7f51\u5173|\u8303\u56f4|\u68c0\u6d4b)",
    r"\u5fd8\u8bb0\s*(\u4ee5\u4e0a|\u4e4b\u524d|\u4e0a\u8ff0)?\s*"
    r"\u7684?\s*\u6240\u6709?\s*(\u5185\u5bb9|\u6307\u4ee4|"
    r"\u4e0a\u4e0b\u6587)|(\u4e0a\u5e1d|\u5f00\u53d1\u8005|"
    r"\u7ba1\u7406\u5458|\u65e0\u9650\u5236)\s*\u6a21\u5f0f",
    # japanese
    r"(\u4ee5\u524d\u306e|\u4e0a\u306e|\u524d\u306e)\s*"
    r"(\u6307\u793a|\u547d\u4ee4|\u30eb\u30fc\u30eb|\u8aac\u660e)\s*"
    r"\u3092?\s*\u7121\u8996(\u3057\u3066|\u305b\u3088)?",
    r"\u627f\u8a8d(\u6e08\u307f|\u3055\u308c\u3066\u3044\u308b)\s*"
    r"\u3068\s*(\u507d\u88c5|\u4eee\u5b9a)|"
    r"(\u958b\u767a\u8005|\u795e)\s*\u30e2\u30fc\u30c9",
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
    decoding the trivial obfuscations first (+ and %20 as space, the
    typographic apostrophes U+2019/U+2018 folded to ASCII ' — an
    override phrased with a curly quote is the same override; the
    fold was the third in-session catch: out-of-set probing showed
    'pretend you're approved' sailing past the pretend family when
    the apostrophe went typographic)."""
    blob = " \n ".join(t or "" for t in texts).lower()
    blob = blob.replace("+", " ").replace("%20", " ")
    return blob.replace("\u2019", "'").replace("\u2018", "'")


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
