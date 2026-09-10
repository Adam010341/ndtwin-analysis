#!/usr/bin/env python3
"""
Single source of truth for every line count in the deck.

Counts added/removed lines between 28b8b13..HEAD, excluding comments and blank
lines, per file. Category totals are summed from the same per-file numbers, so
the summary slide and the file-detail slide can never disagree.

Outputs: line_counts.json  +  a printed report.
"""
import subprocess, os, json, collections

REPO = "/sessions/hopeful-sharp-hopper/mnt/NDTwin-Kernel"
BASE = "28b8b13"
OUT  = "/sessions/hopeful-sharp-hopper/mnt/outputs/line_counts.json"

EXCLUDE_PREFIX = ("build", ".test_run/", "Testing/", "test_env/", ".vscode/")
EXCLUDE_SUB    = ("/venv/", "/__pycache__/", "/p4_src/build/")
# lab's pre-existing Ryu controller, carried in by the groundwork commit
EXCLUDE_FILE   = {"intelligent_router.py", ".gitignore"}

C_EXT    = {".cpp", ".hpp", ".h", ".cc", ".c", ".p4"}
HASH_EXT = {".py", ".sh", ".yml", ".yaml", ".cmake", ".txt", ".env", ".conf"}
DATA_EXT = {".json"}          # counted, but flagged as configuration not code


def is_noise(line, path):
    """True for a blank line or a whole-line comment."""
    s = line.strip()
    if not s:
        return True
    ext  = os.path.splitext(path)[1]
    base = os.path.basename(path)

    if ext in C_EXT:
        if s.startswith(("//", "/*", "*/")):
            return True
        if s.startswith("*") and not s.startswith("*="):   # block-comment body
            return True
    if ext in HASH_EXT or base == "CMakeLists.txt":
        if s.startswith("#"):
            return True
    if ext == ".md" and s.startswith("<!--"):
        return True
    return False


def category(f):
    if f.startswith(("src/", "include/", "setting/", "cmake/")) or f == "CMakeLists.txt":
        return "kernel"
    if f.startswith("p4_proxy/tests/"):
        return "test"
    if f.startswith("p4_proxy/"):
        return "proxy"
    if f.startswith(("tests/", "tools/", ".github/")):
        return "test"
    if f in ("test_modify.py", "test_modify_error.py", "check_env.py",
             "dump_table.py", "testbed_topo.py"):
        return "test"
    if f.startswith("doc/") or f.endswith(".md"):
        return "doc"
    return None


def run(*a):
    return subprocess.run(a, cwd=REPO, capture_output=True, text=True).stdout


# ---------------------------------------------------------------- collect
rows = []
for f in run("git", "diff", "--name-only", f"{BASE}..HEAD").splitlines():
    if f.startswith(EXCLUDE_PREFIX) or any(x in f for x in EXCLUDE_SUB):
        continue
    if f.endswith(".pyc") or f in EXCLUDE_FILE:
        continue
    cat = category(f)
    if cat is None:
        continue

    add = dele = raw_add = raw_del = 0
    for line in run("git", "diff", "--unified=0", f"{BASE}..HEAD", "--", f).splitlines():
        if line.startswith(("+++", "---")):
            continue
        if line.startswith("+"):
            raw_add += 1
            if not is_noise(line[1:], f):
                add += 1
        elif line.startswith("-"):
            raw_del += 1
            if not is_noise(line[1:], f):
                dele += 1

    if raw_add + raw_del == 0:          # binary / no textual change
        continue

    rows.append({
        "f": f,
        "cat": cat,
        "add": add,
        "del": dele,
        "raw_add": raw_add,
        "raw_del": raw_del,
        "new": subprocess.run(["git", "cat-file", "-e", f"{BASE}:{f}"],
                              cwd=REPO, capture_output=True).returncode != 0,
        "data": os.path.splitext(f)[1] in DATA_EXT,
    })

rows.sort(key=lambda r: -(r["add"] + r["del"]))
json.dump(rows, open(OUT, "w"), indent=1)

# ---------------------------------------------------------------- report
agg = collections.defaultdict(lambda: dict(files=0, add=0, dele=0, raw_add=0, raw_del=0))
for r in rows:
    a = agg[r["cat"]]
    a["files"] += 1; a["add"] += r["add"]; a["dele"] += r["del"]
    a["raw_add"] += r["raw_add"]; a["raw_del"] += r["raw_del"]

print("SLIDE 2 — category totals (code lines only)")
print(f"{'category':10}{'files':>7}{'+code':>9}{'-code':>8}{'  (+raw':>10}{'-raw)':>8}")
tot = dict(files=0, add=0, dele=0, raw_add=0, raw_del=0)
for c in ("test", "doc", "kernel", "proxy"):
    a = agg[c]
    print(f"{c:10}{a['files']:>7}{a['add']:>9}{a['dele']:>8}{a['raw_add']:>10}{a['raw_del']:>8}")
    for k in tot: tot[k] += a[k]
print(f"{'TOTAL':10}{tot['files']:>7}{tot['add']:>9}{tot['dele']:>8}"
      f"{tot['raw_add']:>10}{tot['raw_del']:>8}")

# kernel split: source vs configuration data
ks = [r for r in rows if r["cat"] == "kernel" and not r["data"]]
kd = [r for r in rows if r["cat"] == "kernel" and r["data"]]
print(f"\n  kernel source only : {len(ks)} files  +{sum(r['add'] for r in ks)} "
      f"-{sum(r['del'] for r in ks)}")
print(f"  kernel config data : {len(kd)} files  +{sum(r['add'] for r in kd)}")

print("\nSLIDE 3 — per-file detail")
for cat, title in (("kernel", "KERNEL"), ("proxy", "P4 PROXY")):
    sel = [r for r in rows if r["cat"] == cat]
    print(f"\n===== {title} — {len(sel)} files, "
          f"+{sum(r['add'] for r in sel)} / -{sum(r['del'] for r in sel)} =====")
    for r in sel:
        tag = "NEW" if r["new"] else "mod"
        flag = " [data]" if r["data"] else ""
        print(f"  {tag}  +{r['add']:<6} -{r['del']:<5} {r['f']}{flag}")
