#!/usr/bin/env python3
"""Commit semua perubahan via MCP github-mcp-server (push_files).

Alur: kirim isi 68 file (dari working tree) ke push_files dengan pesan
commit gaya rumah. Token hanya lewat env var, TIDAK pernah dicetak.
Output: SHA commit remote (dibersihkan dari token).
"""
import json
import os
import subprocess
import sys

BIN = "/home/z/my-project/bin/github-mcp-server"
REPO_DIR = "/home/z/my-project/repo/agentic-skills"
OWNER, REPO, BRANCH = "tatopfara67-ops", "agentic-skills", "main"

MSG = """refactor(skills): the method-first reorder — the executable protocol leads

Every references/method-upgrade.md now opens with its numbered
executable protocol (M0-M6); the lineage critique and upgrades tables
move to a 4-5 appendix. history-1995.md converts to a case-fact
table; the Forshaw/Kaminsky psych-reads gain explicit extracted-as
organ rules; five organs gain quickstart command blocks; nine fused
descriptions, four duplicate section numbers, the aas-catalog
frontmatter, and the adversary-tracker lineage key are fixed.
32 patch bumps. The migration scripts are committed with the corpus."""


def main():
    token = open("/tmp/.ghtoken").read().strip()
    env = os.environ.copy()
    env["GITHUB_PERSONAL_ACCESS_TOKEN"] = token

    # file list dari commit HEAD (commit lokal yang akan dicerminkan ke remote)
    out = subprocess.run(
        ["git", "-C", REPO_DIR, "diff-tree", "--no-commit-id",
         "--name-only", "-r", "HEAD"],
        capture_output=True, text=True, check=True).stdout
    paths = [l.strip() for l in out.splitlines() if l.strip()]
    if not paths:
        print("TIDAK ADA perubahan — batal.")
        sys.exit(1)

    files = []
    for p in paths:
        full = os.path.join(REPO_DIR, p)
        with open(full, "r", encoding="utf-8") as fh:
            files.append({"path": p, "content": fh.read()})

    print(f"[1] {len(files)} file siap dipush (total "
          f"{sum(len(f['content']) for f in files)} karakter)")

    p = subprocess.Popen([BIN, "stdio"], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         env=env, text=True)

    def rpc(method, params=None, _id=[0]):
        _id[0] += 1
        m = {"jsonrpc": "2.0", "id": _id[0], "method": method}
        if params is not None:
            m["params"] = params
        p.stdin.write(json.dumps(m) + "\n")
        p.stdin.flush()
        return json.loads(p.stdout.readline())

    init = rpc("initialize", {
        "protocolVersion": "2025-03-26", "capabilities": {},
        "clientInfo": {"name": "commit-via-mcp", "version": "1.0"}})
    info = init.get("result", {}).get("serverInfo", {})
    print(f"[2] initialize OK -> {info.get('name')} v{info.get('version')}")
    rpc("notifications/initialized")

    res = rpc("tools/call", {
        "name": "push_files",
        "arguments": {
            "owner": OWNER, "repo": REPO, "branch": BRANCH,
            "message": MSG, "files": files,
        }})
    blob = json.dumps(res)
    if '"error"' in blob and res.get("error"):
        print("[X] push_files GAGAL:", str(res)[:400])
        sys.exit(2)

    # ekstrak SHA hasil dari teks respons (bentuk: status message)
    import re
    msha = re.search(r"([0-9a-f]{40})", blob)
    print(f"[3] push_files OK -> commit remote: "
          f"{msha.group(1) if msha else '(sha tidak terbaca, cek manual)'}")
    txt = res.get("result", {}).get("content", [])
    for c in txt[:2]:
        s = str(c.get("text", ""))[:300]
        print("[i]", s.replace(token, "***") if token in s else s)
    p.terminate()


if __name__ == "__main__":
    main()
