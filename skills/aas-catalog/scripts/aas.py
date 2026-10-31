#!/usr/bin/env python3
"""aas.py — search & install skills from the Agentic Awesome Skills catalog.

Commands:
  aas.py search <query> [--category C] [--risk R] [--limit N]
  aas.py info <skill-id>
  aas.py install <skill-id> [--dest DIR] [--allow-risky]
  aas.py categories

Catalog location: env AAS_CATALOG_DIR (default: the local clone path below).
The catalog is a plain git clone of github.com/sickn33/agentic-awesome-skills.
Exit codes: 0 ok, 1 error, 2 usage.
"""
import json
import os
import shutil
import sys

DEFAULT_CATALOG = "/home/z/my-project/external-skills/agentic-awesome-skills"
CATALOG_DIR = os.environ.get("AAS_CATALOG_DIR", DEFAULT_CATALOG)
INDEX_FILE = os.path.join(CATALOG_DIR, "skills_index.json")
DEFAULT_DEST = "/home/z/my-project/skills"

USAGE = __doc__


def load_index():
    if not os.path.isfile(INDEX_FILE):
        sys.stderr.write(
            f"Katalog tidak ditemukan: {INDEX_FILE}\n"
            f"Clone dulu: git clone --depth 1 https://github.com/sickn33/agentic-awesome-skills.git "
            f"{CATALOG_DIR}\nlalu set AAS_CATALOG_DIR bila path berbeda.\n"
        )
        sys.exit(1)
    with open(INDEX_FILE, encoding="utf-8") as f:
        return json.load(f)


def cmd_search(args):
    query = args[0].lower()
    category = risk = None
    limit = 15
    rest = args[1:]
    i = 0
    while i < len(rest):
        if rest[i] == "--category" and i + 1 < len(rest):
            category = rest[i + 1].lower(); i += 2
        elif rest[i] == "--risk" and i + 1 < len(rest):
            risk = rest[i + 1].lower(); i += 2
        elif rest[i] == "--limit" and i + 1 < len(rest):
            limit = int(rest[i + 1]); i += 2
        else:
            usage_error(f"opsi tidak dikenal: {rest[i]}")
    hits = []
    for s in load_index():
        if category and s.get("category", "").lower() != category:
            continue
        if risk and s.get("risk", "").lower() != risk:
            continue
        hay = " ".join([s.get("id", ""), s.get("name", ""), s.get("description", "")]).lower()
        if query in hay:
            hits.append(s)
    if not hits:
        print(f"0 hasil untuk '{query}'")
        return
    print(f"{min(len(hits), limit)} dari {len(hits)} hasil untuk '{query}':")
    for s in hits[:limit]:
        desc = (s.get("description") or "").strip().replace("\n", " ")
        if len(desc) > 90:
            desc = desc[:87] + "..."
        print(f"  {s['id']}  [{s.get('risk', '?')}|{s.get('category', '?')}]  {desc}")


def cmd_info(args):
    if not args:
        usage_error("info butuh <skill-id>")
    sid = args[0]
    for s in load_index():
        if s.get("id") == sid:
            print(json.dumps(s, indent=2, ensure_ascii=False))
            d = os.path.join(CATALOG_DIR, s.get("path", ""))
            if os.path.isdir(d):
                files = []
                for root, _, names in os.walk(d):
                    files += [os.path.relpath(os.path.join(root, n), d) for n in names]
                print("file di paket skill:")
                for f in sorted(files)[:25]:
                    print(f"  {f}")
            else:
                print(f"[warn] dir paket tidak ada: {d}")
            return
    sys.stderr.write(f"skill id tidak ditemukan: {sid}\n")
    sys.exit(1)


def cmd_install(args):
    if not args:
        usage_error("install butuh <skill-id>")
    sid = args[0]
    dest_root = DEFAULT_DEST
    allow_risky = False
    rest = args[1:]
    i = 0
    while i < len(rest):
        if rest[i] == "--dest" and i + 1 < len(rest):
            dest_root = rest[i + 1]; i += 2
        elif rest[i] == "--allow-risky":
            allow_risky = True; i += 1
        else:
            usage_error(f"opsi tidak dikenal: {rest[i]}")

    entry = None
    for s in load_index():
        if s.get("id") == sid:
            entry = s
            break
    if entry is None:
        sys.stderr.write(f"skill id tidak ditemukan: {sid}\n")
        sys.exit(1)

    risk = (entry.get("risk") or "").lower()
    if risk != "safe" and not allow_risky:
        sys.stderr.write(
            f"ditolak: risk='{risk or '?'}' (bukan 'safe').\n"
            f"Review manual skill ini dulu, lalu jalankan ulang dengan --allow-risky bila lolos.\n"
        )
        sys.exit(1)

    src = os.path.join(CATALOG_DIR, entry.get("path", ""))
    if not os.path.isdir(src):
        sys.stderr.write(f"dir paket tidak ada: {src}\n")
        sys.exit(1)
    dst = os.path.join(dest_root, entry.get("name") or sid)
    if os.path.exists(dst):
        sys.stderr.write(f"target sudah ada, tidak menimpa: {dst}\n")
        sys.exit(1)
    shutil.copytree(src, dst)
    n = sum(len(f) for _, _, f in os.walk(dst))
    print(f"terpasang: {dst} ({n} file, risk={risk})")
    print("langkah wajib berikutnya:")
    print(f"  1. python3 scripts/validate_skill.py {dst}   (dari root repo agentic-skills)")
    print(f"  2. regen INDEX: python3 /home/z/my-project/scripts/gen_skill_index.py")
    print(f"  3. review manual isi SKILL.md-nya sebelum dipakai (skill pihak ketiga)")


def cmd_categories(args):
    counts = {}
    for s in load_index():
        counts[s.get("category", "?")] = counts.get(s.get("category", "?"), 0) + 1
    for cat, n in sorted(counts.items(), key=lambda kv: -kv[1])[:30]:
        print(f"  {n:5d}  {cat}")


def usage_error(msg):
    sys.stderr.write(f"{msg}\n\n{USAGE}\n")
    sys.exit(2)


def main():
    args = sys.argv[1:]
    if not args:
        print(USAGE)
        sys.exit(0)
    cmd, rest = args[0], args[1:]
    {"search": cmd_search, "info": cmd_info, "install": cmd_install,
     "categories": cmd_categories}.get(cmd, lambda a: usage_error(f"perintah tidak dikenal: {cmd}"))(rest)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)
