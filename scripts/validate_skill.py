#!/usr/bin/env python3
"""House skill-bundle validator — the pre-commit gate for agentic-skills.

Usage:
    python3 scripts/validate_skill.py skills/<skill-name>
    python3 scripts/validate_skill.py --all

Enforces the authoring contract in CONTRIBUTING.md:
  - SKILL.md exists, parses, and stays a lean routing layer
  - required frontmatter: name, version, description, license, author
    (author may sit at top level or under `metadata:`)
  - name matches the bundle directory; version is MAJOR.MINOR.PATCH
  - description is substantive (>= 40 chars) — it is what makes a skill fire
  - no placeholder markers left in SKILL.md (TODO / FIXME / XXX / TBD / ____ / 【)
  - no junk top-level entries; only the known module set
  - every internal path mentioned in SKILL.md actually exists
    (bundle-relative, or repo-relative for cross-bundle references)
  - no empty module files

Exit 0 = PASS (warnings allowed). Exit 1 = at least one FAIL.
Fix the skill, not the gate.
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CORE_MAX_BYTES = 131072    # SKILL.md above this = FAIL: the routing layer is broken
CORE_WARN_BYTES = 32768    # SKILL.md above this = WARN: push depth into references/
MIN_DESCRIPTION_CHARS = 40

REQUIRED_KEYS = ("name", "version", "description", "license")
ALLOWED_ENTRIES = {
    "SKILL.md", "README.md", "LICENSE", "NOTICE.md", "NOTICES.md",
    "scripts", "references", "example", "examples", "targets",
    "assets", "data", "tests",
}
PLACEHOLDER_RE = re.compile(r"TODO|FIXME|\bXXX\b|\bTBD\b|【|_{5,}")
INTERNAL_PATH_RE = re.compile(
    r"(?:references|scripts|example|examples|targets|assets|data)/[A-Za-z0-9._\-/]*"
)
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def parse_frontmatter(text):
    """Minimal stdlib frontmatter parser (one nesting level).

    Returns (dict, None) on success, (None, reason) on failure.
    Handles `key: value`, folded blocks (`>` / `|` and their strip/chomp
    variants), and one indented sub-dict under `metadata:`.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "no opening `---` frontmatter fence"
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, "no closing `---` frontmatter fence"

    data = {}
    metadata = {}
    i = 1
    while i < end:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line[:1].isspace():
            i += 1  # stray indent outside a known block — skip
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            return None, "unparsable frontmatter line %d: %r" % (i + 1, line)
        key, value = m.group(1), m.group(2).strip()
        if key == "metadata":
            i += 1
            while i < end and (not lines[i].strip() or lines[i][:1].isspace()):
                mm = re.match(r"^\s+([A-Za-z0-9_-]+):\s*(.*)$", lines[i])
                if mm:
                    metadata[mm.group(1)] = mm.group(2).strip()
                i += 1
            data["metadata"] = metadata
            continue
        if value in (">", "|", ">-", "|-", ">+", "|+"):
            parts = []
            i += 1
            while i < end and (not lines[i].strip() or lines[i][:1].isspace()):
                parts.append(lines[i].strip())
                i += 1
            data[key] = " ".join(p for p in parts if p)
            continue
        data[key] = value
        i += 1
    return data, None


def read_file(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def check_bundle(bundle_path):
    """Run every gate check on one skill bundle.

    Returns a list of (status, message) tuples, status in {PASS, WARN, FAIL}.
    """
    results = []

    def note(status, msg):
        results.append((status, msg))

    if not os.path.isdir(bundle_path):
        note("FAIL", "bundle directory not found: %s" % bundle_path)
        return results
    name_expected = os.path.basename(os.path.normpath(bundle_path))

    skill_md = os.path.join(bundle_path, "SKILL.md")
    if not os.path.isfile(skill_md):
        note("FAIL", "SKILL.md missing — a bundle without a routing layer is not a skill")
        return results
    try:
        core = read_file(skill_md)
    except OSError as exc:
        note("FAIL", "SKILL.md unreadable: %s" % exc)
        return results
    if not core.strip():
        note("FAIL", "SKILL.md is empty")
        return results
    note("PASS", "SKILL.md present and non-empty")

    size = os.path.getsize(skill_md)
    if size > CORE_MAX_BYTES:
        note("FAIL", "SKILL.md is %d bytes (> %d) — split it: depth belongs in references/"
             % (size, CORE_MAX_BYTES))
    elif size > CORE_WARN_BYTES:
        note("WARN", "SKILL.md is %d bytes (> %d) — routing layer getting fat, consider "
             "pushing depth into references/" % (size, CORE_WARN_BYTES))
    else:
        note("PASS", "SKILL.md size discipline ok (%d bytes)" % size)

    fm, err = parse_frontmatter(core)
    if fm is None:
        note("FAIL", "frontmatter: %s" % err)
        return results
    note("PASS", "frontmatter fences and syntax ok")

    for key in REQUIRED_KEYS:
        value = str(fm.get(key, "")).strip()
        if not value:
            note("FAIL", "required frontmatter key missing or empty: `%s`" % key)
        else:
            note("PASS", "frontmatter `%s` present" % key)

    author = str(fm.get("author", "")).strip()
    if not author:
        author = str((fm.get("metadata") or {}).get("author", "")).strip()
    if author:
        note("PASS", "author present (%s)" % author)
    else:
        note("FAIL", "author missing — set `author:` (or `metadata.author:`); "
             "without it the skill cannot leave this repo")

    name = str(fm.get("name", "")).strip()
    if name != name_expected:
        note("FAIL", "frontmatter name `%s` != bundle directory `%s`" % (name, name_expected))
    else:
        note("PASS", "name matches bundle directory (`%s`)" % name)

    version = str(fm.get("version", "")).strip()
    if not SEMVER_RE.match(version):
        note("FAIL", "version `%s` is not MAJOR.MINOR.PATCH" % version)
    else:
        note("PASS", "version format ok (%s)" % version)

    description = str(fm.get("description", "")).strip()
    if len(description) < MIN_DESCRIPTION_CHARS:
        note("FAIL", "description too short (%d < %d chars) — it is what makes the skill fire"
             % (len(description), MIN_DESCRIPTION_CHARS))
    else:
        note("PASS", "description substantive (%d chars)" % len(description))

    hits = sorted(set(PLACEHOLDER_RE.findall(core)))
    if hits:
        note("FAIL", "placeholder markers left in SKILL.md: %s" % hits)
    else:
        note("PASS", "no placeholder markers in SKILL.md")

    junk = sorted(
        e for e in os.listdir(bundle_path) if e not in ALLOWED_ENTRIES
    )
    if junk:
        note("FAIL", "unexpected top-level entries %s — allowed set: %s"
             % (junk, sorted(ALLOWED_ENTRIES)))
    else:
        note("PASS", "top-level layout within the allowed module set")

    missing = []
    for match in sorted(set(INTERNAL_PATH_RE.findall(core))):
        rel = match.rstrip("/")
        if not rel:
            continue
        if os.path.exists(os.path.join(bundle_path, rel)):
            continue
        if os.path.exists(os.path.join(REPO_ROOT, rel)):
            continue
        missing.append(match)
    if missing:
        note("FAIL", "SKILL.md mentions paths that do not exist: %s" % missing)
    else:
        note("PASS", "all internal paths mentioned in SKILL.md resolve")

    empty_files = []
    for sub in ("references", "scripts", "example", "examples",
                "targets", "assets", "data", "tests"):
        sub_dir = os.path.join(bundle_path, sub)
        if not os.path.isdir(sub_dir):
            continue
        for root, _dirs, files in os.walk(sub_dir):
            for fname in files:
                fpath = os.path.join(root, fname)
                if os.path.getsize(fpath) == 0:
                    empty_files.append(os.path.relpath(fpath, bundle_path))
    if empty_files:
        note("FAIL", "empty module files: %s" % empty_files)
    else:
        note("PASS", "no empty module files")

    return results


def main(argv):
    if len(argv) == 2 and argv[1] == "--all":
        skills_root = os.path.join(REPO_ROOT, "skills")
        if not os.path.isdir(skills_root):
            print("no skills/ directory at repo root")
            return 1
        bundles = sorted(
            os.path.join(skills_root, d)
            for d in os.listdir(skills_root)
            if os.path.isdir(os.path.join(skills_root, d))
        )
        if not bundles:
            print("no skill bundles found under skills/")
            return 1
    elif len(argv) == 2:
        bundles = [argv[1]]
    else:
        print(__doc__)
        return 2

    failed = []
    warnings = 0
    for bundle in bundles:
        name = os.path.basename(os.path.normpath(bundle))
        print("== %s %s" % (name, "=" * max(0, 58 - len(name))))
        bundle_failed = False
        for status, msg in check_bundle(bundle):
            print("[ %s ] %s" % (status, msg))
            if status == "FAIL":
                bundle_failed = True
            elif status == "WARN":
                warnings += 1
        if bundle_failed:
            failed.append(name)
            print("RESULT: FAIL — fix the skill, not the gate\n")
        else:
            print("RESULT: PASS\n")

    if failed:
        print("GATE: FAIL (%d bundle(s): %s; %d warning(s))"
              % (len(failed), ", ".join(failed), warnings))
        return 1
    print("GATE: PASS (%d bundle(s), %d warning(s))" % (len(bundles), warnings))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
