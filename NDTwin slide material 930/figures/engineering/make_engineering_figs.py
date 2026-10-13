#!/usr/bin/env python3
"""
make_engineering_figs.py -- the five engineering-process figures of the 2026-09-30 report.

    fig_q1_protobuf5        the P4 proxy's protobuf 3.20.3 -> 5.29.6 move, step by step, with the
                            check each step passed (no performance number on it, by design)
    fig_q2_review_path      how a change gets into trunk, with counts since 2026-09-16 and one
                            worked example (heartbeat segment W, merge cafd518a)
    fig_q3_review_catches   five things review caught this period, as cards
    fig_q4_ci_state         L1 problem groups per CI run, and the four jobs' outcomes per run
    fig_q5_main_by_pr       how main is updated since 2026-09-27 (PR + squash merge only)

Data: everything is read at run time from the NDTwin-Kernel checkout (read-only: files under
scratch/overnight-2026-09-05/logs, doc/audit, and read-only `git show / log / rev-parse /
merge-base --is-ancestor / diff --name-only`), plus the unauthenticated GitHub API snapshots
saved next to this script in _net/ (the exact curl commands are in fig_q4/fig_q5's .md).
Nothing measured is typed by hand; every number drawn is parsed, and the script stops
(SystemExit) when a file no longer says what the figure relies on.  Raw under scratch/ and
live-p1/runs/ is NOT in version control in the checkout (uncommitted observations).

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/engineering"
    nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_engineering_figs.py
"""
import csv
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys

import matplotlib

assert matplotlib.__version__.startswith("3.11"), matplotlib.__version__
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle  # noqa: E402

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["font.monospace"] = ["Courier New", "Liberation Mono", "DejaVu Sans Mono"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

REPO = os.environ.get("NDTWIN_REPO", "/home/adam/Desktop/NDTwin-Kernel")
LOGS = os.path.join(REPO, "scratch/overnight-2026-09-05/logs")
I26 = os.path.join(LOGS, "orchestrator-0924/intake-0926")
I25 = os.path.join(LOGS, "orchestrator-0924/intake-0925")
GATES = os.path.join(LOGS, "gates-0910")
PREP = os.path.join(REPO, "doc/audit/2026-09-04_p4-tutorial-exercise-prep")
LIVE = os.path.join(PREP, "live-p1/runs")
ARMS = os.path.join(PREP, "runs")
SNAPSHOT = "3d740be0"          # the trunk commit this report stands on (brief-930): fig_q1, fig_q3
# the state fig_q4 and fig_q5 are drawn at (the 2026-09-28 refresh): the public trunk head and the
# time of the unauthenticated API snapshot in _net/ (when.txt, last line).  A later refresh bumps
# these two, refetches _net/ and copies the new GCC job logs into CIRAW.
STATE = "3368412d"
STATE_AT = "2026-09-28T08:53"
# the commit whose CLAUDE.md states the rule fig_q5 draws: from 2026-09-28 (Adam) ndtwin-lab main
# follows the PR-merged main (fast-forwarded after each squash); 08f67b7a was on the local trunk only
# when the refresh read it
RULE_AT = "08f67b7a"

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")
NET = os.path.join(OUTDIR, "_net")

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
WARNC, WARN_BG, WHITE = "#9C3B2E", "#FBF2F0", "#FFFFFF"
GREEN, AMBER, GREY, SECOND = "#2F7D4F", "#E3A21A", "#C9CDD0", "#C0701C"
W = 13.33


def die(msg):
    raise SystemExit(f"make_engineering_figs: {msg}")


def text(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError as e:
        die(f"cannot read {path}: {e}")


def must(path, *needles):
    t = text(path)
    for n in needles:
        if n not in t:
            die(f"{path} no longer contains {n!r}")
    return t


def grab(pattern, s, what, flags=0, at_start=False):
    """Group 1 of a pattern that must match: a named stop instead of an AttributeError."""
    m = (re.match if at_start else re.search)(pattern, s, flags)
    if not m:
        die(f"{what} not found")
    return m.group(1)


def git(*args, ok_rc=(0,)):
    p = subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True)
    if p.returncode not in ok_rc:
        die(f"git {' '.join(args)} -> rc {p.returncode}: {p.stderr.strip()}")
    return p.stdout if p.returncode == 0 else None


def is_ancestor(a, b):
    p = subprocess.run(["git", "-C", REPO, "merge-base", "--is-ancestor", a, b],
                       capture_output=True)
    if p.returncode not in (0, 1):
        die(f"merge-base --is-ancestor {a} {b}: rc {p.returncode}")
    return p.returncode == 0


# ------------------------------------------------------------------ drawing helpers
def canvas(h):
    fig = plt.figure(figsize=(W, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(h, 0)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fill=WHITE, edge=INK, lw=1.2, ls="solid", r=0.06, z=2):
    ax.add_patch(FancyBboxPatch((x + r, y + r), w - 2 * r, h - 2 * r,
                                boxstyle=f"round,pad={r},rounding_size={r}", facecolor=fill,
                                edgecolor=edge, linewidth=lw, linestyle=ls, zorder=z))


def txt(ax, x, y, s, size=13, color=INK, weight="normal", ha="center", va="center",
        mono=False, z=6):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, zorder=z,
            family="monospace" if mono else None, linespacing=1.25)


def arrow(ax, x0, y0, x1, y1, color=INK, lw=1.4, ls="solid", z=3, rad=None, ms=13):
    kw = {}
    if rad is not None:
        kw["connectionstyle"] = f"arc3,rad={rad}"
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=ms,
                                 color=color, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0,
                                 zorder=z, **kw))


def dot(ax, x, y, color, hollow=False, size=8):
    ax.plot([x], [y], "o", ms=size, color=color, mfc=WHITE if hollow else color, mew=1.8,
            zorder=6)


def save(fig, name):
    os.makedirs(HIRES, exist_ok=True)
    for ext in ("pdf", "png", "svg"):
        kw = {"dpi": 300} if ext == "png" else {}
        fig.savefig(os.path.join(OUTDIR, f"{name}.{ext}"), facecolor=WHITE, **kw)
    fig.savefig(os.path.join(HIRES, f"{name}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"[out] {name}.{{pdf,png,svg}} + _hires/{name}.png")


# ------------------------------------------------------------------ shared parsers
PIN_RE = re.compile(r"^([A-Za-z0-9_.-]+)\s*(==|>=|~=)\s*([0-9][0-9A-Za-z.]*)\s*$")


def pins_at(sha):
    out = {}
    for ln in git("show", f"{sha}:p4_proxy/requirements.txt").splitlines():
        m = PIN_RE.match(ln.strip())
        if m:
            out[m.group(1).lower()] = m.group(2) + m.group(3)
    return out


def table06(run):
    """(n rows, n as the exercise designs it, n PASS, n designed red, code shas of the arms)."""
    path = os.path.join(LIVE, run, "00_table.tsv")
    try:
        with open(path, newline="") as f:
            rows = list(csv.DictReader(f, delimiter="\t"))
    except OSError as e:
        die(f"{path}: cannot open the 06 table ({e})")
    if not rows or not {"rc", "verdict", "report"} <= set(rows[0]):
        die(f"{path}: no arm rows, or no rc / verdict / report column")
    npass = sum(1 for r in rows if r["rc"] == "0" and r["verdict"].startswith("PASS"))
    nred = sum(1 for r in rows if r["rc"] == "1" and r["verdict"].startswith("RED ARM")
               and "by design" in r["verdict"])
    codes = set()
    for r in rows:
        m = re.search(r"^  code\s+([0-9a-f]{8})\s", text(r["report"]), re.M)
        if m:
            codes.add(m.group(1))
    return len(rows), npass + nred, npass, nred, codes


def status_code(run):
    m = re.search(r"^  code\s+([0-9a-f]{8})\s", text(os.path.join(LIVE, run, "22_status.txt")),
                  re.M)
    if not m:
        die(f"{run}: no 'code <sha>' line in 22_status.txt")
    return m.group(1)


def check06(label, run06, run01, code):
    """A 06 run: 26 arm rows, all as the exercise designs them, every arm report on `code`, and
    the paired 01 run's status page on `code` too.  Each part stops with its own reason."""
    n, ok, npass, nred, codes = table06(run06)
    if n != 26:
        die(f"{label} 06 table {run06}: {n} arm rows, not 26")
    if ok != 26:
        die(f"{label} 06 table {run06}: {ok} of {n} arms as designed, not 26")
    if codes != {code}:
        die(f"{label} 06 table {run06}: the arm reports ran code {sorted(codes)}, not only {code}")
    c01 = status_code(run01)
    if c01 != code:
        die(f"{label} 01 run {run01}: 22_status.txt says code {c01}, not {code}")
    return n, ok, npass, nred


L1_RE = re.compile(r"L1 FAILED \((\d+) problem group\(s\)\)")
L1_PASS_RE = re.compile(r"L1 passed: ")
FETCH_RE = re.compile(r"\+?([0-9a-f]{40}):refs/remotes/(\S+)")
# a push run that fetches all heads (fetch-depth 0, from 09-28) names no sha in its fetch line:
# the ref is on the checkout line and the sha on the line after `git log -1 --format=%H`
CHECKOUT_RE = re.compile(r"git checkout --progress --force (?:-B \S+ )?refs/remotes/(\S+)")
HEAD_RE = re.compile(r"git log -1 --format=%H\n\S*Z ([0-9a-f]{40})\n")
REPO_RE = re.compile(r"Syncing repository: (\S+)")
TS_RE = re.compile(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})")
CI_CUTOFF = STATE_AT + ":00"            # UTC; runs whose log starts later are not drawn
# GCC job logs the orchestrator fetched through the API (auth needed for logs), copied verbatim with
# a MANIFEST.txt; named ci-<run>-gcc.job<job>.raw.log
CIRAW = os.path.join(LOGS, "slides930/ci-raw")
API_ONLY_SINCE = "2026-09-27T15:00:00Z"   # from here on, trunk runs without a log come from the API


def ci_logs():
    """Every GCC-job raw log on disk: run id, first timestamp, commit, ref, repo, L1 groups."""
    paths = sorted(glob.glob(os.path.join(I26, "ci-*-gcc.raw.log")) +
                   glob.glob(os.path.join(I25, "ci-*-gcc.log")) +
                   glob.glob(os.path.join(CIRAW, "ci-*-gcc.job*.raw.log")))
    runs = []
    for p in paths:
        rid = grab(r"ci-(\d+)-gcc", os.path.basename(p), f"{p}: the run id in the file name",
                   at_start=True)
        job = re.match(r"ci-\d+-gcc\.job(\d+)\.", os.path.basename(p))
        t = text(p)
        l1 = L1_RE.findall(t)
        l1_ok = len(L1_PASS_RE.findall(t))
        fe = FETCH_RE.search(t)
        co, hd = CHECKOUT_RE.search(t), HEAD_RE.search(t)
        sha, ref = (fe.group(1), fe.group(2)) if fe else \
            (hd.group(1), co.group(1)) if co and hd else (None, None)
        rp = REPO_RE.search(t)
        ts = TS_RE.search(t[:200])
        if len(l1) + l1_ok != 1 or not sha or not rp or not ts:
            die(f"{p}: expected one 'L1 FAILED' or 'L1 passed' line, a fetched or checked-out sha, "
                f"a repo and a timestamp")
        kind = "trunk" if ref.endswith("/trunk") else "main" if ref.endswith("/main") else "PR"
        if ts.group(1) >= CI_CUTOFF:
            print(f"[ci] {rid} starts {ts.group(1)}Z, after the window -- not drawn")
            continue
        runs.append(dict(id=rid, t=ts.group(1), sha=sha[:8], ref=ref, kind=kind,
                         repo=rp.group(1), l1=int(l1[0]) if l1 else 0, path=p,
                         job=job.group(1) if job else None))
    runs.sort(key=lambda r: r["t"])
    return runs


def l1_of(*shas):
    """L1 problem groups of the GCC CI run on each commit (one log each, in the window)."""
    by_sha = {r["sha"]: r for r in ci_logs()}
    missing = [s for s in shas if s not in by_sha]
    if missing:
        die(f"no GCC CI log in the window for {missing}")
    return tuple(by_sha[s]["l1"] for s in shas)


JOBS = [("gcc", "Build and unit tests (GCC)"), ("clang", "clang can compile it"),
        ("tsan", "TSan"), ("asan", "ASan + UBSan")]


def jobs_from_file(path):
    out = {}
    for ln in text(path).splitlines():
        for key, name in JOBS:
            if name in ln:
                if "failure" in ln:
                    out[key] = "failure"
                elif "success" in ln:
                    out[key] = "success"
    return out if len(out) == 4 else None


def api_jobs(rid):
    """The four job conclusions of CI run rid from _net/jobs_<rid>.json (public API snapshot),
    with the job ids; each job must belong to that run, be completed and be green or red."""
    name = f"jobs_{rid}.json"
    jd = api_json(name, each=("jobs", ["id", "run_id", "name", "status", "head_sha:str",
                                       "conclusion"]))
    out, ids = {}, {}
    for j in jd["jobs"]:
        if str(j["run_id"]) != str(rid):
            die(f"_net/{name}: job {j['id']} belongs to run {j['run_id']}, not {rid}")
        for key, jn in JOBS:
            if j["name"] == jn:
                if j["status"] != "completed" or j["conclusion"] not in ("success", "failure"):
                    die(f"_net/{name}: job {jn} is {j['status']}/{j['conclusion']}, not a "
                        f"completed success or failure")
                out[key], ids[key] = j["conclusion"], str(j["id"])
    if len(out) != 4:
        die(f"_net/{name}: not the four CI jobs: {sorted(out)}")
    return out, ids, jd["jobs"][0]["head_sha"] if jd["jobs"] else ""


_BY_REF = {}


def pr_number(r):
    """The PR a PR-kind CI run belongs to: N from pull/N/merge, or its branch in the pulls
    snapshot; None when neither says."""
    m_ = re.fullmatch(r"pull/(\d+)/merge", r["ref"])
    if m_:
        return m_.group(1)
    if not _BY_REF:
        _BY_REF.update({p_["head"]["ref"]: str(p_["number"]) for p_ in
                        api_json("pulls_Adam010341.json", each=("", ["number", "head.ref:str"]))})
    return _BY_REF.get(r["ref"].removeprefix("origin/"))


def ci_jobs(runs):
    """Four job outcomes per run: jobs files, then the public API's jobs snapshot, then the
    orchestrator's compare records."""
    for r in runs:
        cands = [os.path.join(I26, f"ci-{r['id']}.jobs.txt"), os.path.join(I26, f"ci-{r['id']}-jobs.txt"),
                 os.path.join(I25, f"ci-{r['id']}.jobs.txt")]
        r["jobs"] = None
        for c in cands:
            if os.path.exists(c):
                r["jobs"] = jobs_from_file(c)
                r["jobs_src"] = c
                if r["jobs"] is None:
                    die(f"{c}: not four job outcomes")
                break
        if r["jobs"] is None and os.path.exists(os.path.join(NET, f"jobs_{r['id']}.json")):
            r["jobs"], ids, _ = api_jobs(r["id"])
            r["jobs_src"] = f"_net/jobs_{r['id']}.json"
            if r["job"] is not None and ids["gcc"] != r["job"]:
                die(f"{r['path']}: GCC job {r['job']} is not run {r['id']}'s GCC job {ids['gcc']}")
        if r["jobs"] is not None and r["l1"] > 0 and r["jobs"]["gcc"] == "success":
            die(f"CI run {r['id']}: L1 failed ({r['l1']} groups) but the GCC job is a success")
    # cafd518a: its compare record names the four conclusions (checked with gh run view)
    cmp_ = os.path.join(I26, "ci-compare-cafd518a.txt")
    if "identical conclusions (GCC failure, clang failure, TSan failure, ASan+UBSan success)" \
            in text(cmp_):
        for r in runs:
            if r["sha"] == "cafd518a" and r["jobs"] is None:
                r["jobs"] = dict(gcc="failure", clang="failure", tsan="failure", asan="success")
                r["jobs_src"] = cmp_
    else:
        die(f"{cmp_}: the jobs sentence moved")
    # the two PR #6 runs: ci-compare-pr6-48e8005d.txt records the outcomes in words
    pr = os.path.join(I26, "ci-compare-pr6-48e8005d.txt")
    t = must(pr, "push run 36329482388", "ASan + UBSan: pass", "clang: fail", "TSan: fail",
             "GCC: fail;", "pull_request run 36329490324 GCC: IDENTICAL",
             "clang/TSan fail, ASan pass")
    for r in runs:
        if r["id"] in ("36329482388", "36329490324") and r["jobs"] is None:
            r["jobs"] = dict(gcc="failure", clang="failure", tsan="failure", asan="success")
            r["jobs_src"] = pr
    # later PRs' compare records, ci-compare-pr<N>.txt.  The first line names the PR and its two
    # runs; when either run is drawn it must also say '<…>: GCC 29 lines IDENTICAL to …;
    # clang/TSan fail; ASan pass => prediction met'.  A record that exists but no longer says so
    # stops the script -- only a PR with no record at all is drawn "no record".
    for cmp_ in sorted(glob.glob(os.path.join(I26, "ci-compare-pr[0-9]*.txt"))):
        if cmp_ == pr:
            continue
        no = grab(r"ci-compare-pr(\d+)\.txt$", os.path.basename(cmp_),
                  f"{cmp_}: a name of the form ci-compare-pr<N>.txt", at_start=True)
        head = (text(cmp_).splitlines() or [""])[0]
        mm = re.match(r"# PR #(\d+) runs (\d+) / (\d+)", head)
        mh = re.match(r"# PR #(\d+) \(head ([0-9a-f]{8})\):", head)
        if mm and mm.group(1) == no:
            drawn = [r for r in runs if r["id"] in mm.group(2, 3)]
        elif mh and mh.group(1) == no:
            # 09-28: a record that names the PR's head instead of its runs -- its runs are the
            # PR's own (pull/N/merge, or its branch in the pulls snapshot), and one is on that head
            drawn = [r for r in runs if r["kind"] == "PR" and pr_number(r) == no]
            if drawn and not any(r["sha"] == mh.group(2) for r in drawn):
                die(f"{cmp_}: PR #{no}'s head {mh.group(2)} is not the commit of any of its drawn "
                    f"runs {[(r['id'], r['sha']) for r in drawn]}")
            mm = mh
        else:
            die(f"{cmp_}: the first line no longer names PR #{no} and its two runs (or its head): "
                f"{head!r}")
        if not drawn:
            print(f"[ci] {os.path.basename(cmp_)}: PR #{no}'s runs are not in the window -- not drawn")
            continue
        # a record that says all four jobs passed must agree with what is drawn for its runs
        if re.search(r"all four jobs success", head, re.I):
            for r in drawn:
                if not r["jobs"] or set(r["jobs"].values()) != {"success"}:
                    die(f"{cmp_}: the first line says all four jobs passed, but run {r['id']} "
                        f"has {r['jobs']}")
        need = [r for r in drawn if r["jobs"] is None]
        if not need:
            continue
        if not re.fullmatch(r": GCC \d+ lines IDENTICAL to [0-9a-f]{8}; clang/TSan fail; "
                            r"ASan pass => prediction met", head[mm.end():]):
            die(f"{cmp_}: the first line no longer gives PR #{no}'s four job outcomes: {head!r}")
        for r in need:
            r["jobs"] = dict(gcc="failure", clang="failure", tsan="failure", asan="success")
            r["jobs_src"] = cmp_
    # a PR run left without outcomes: its PR (from pull/N/merge, or its branch in the pulls
    # snapshot) must have no compare record at all
    left = [r for r in runs if r["kind"] == "PR" and r["jobs"] is None]
    if left:
        by_ref = {p_["head"]["ref"]: str(p_["number"]) for p_ in
                  api_json("pulls_Adam010341.json", each=("", ["number", "head.ref:str"]))}
    for r in left:
        m = re.fullmatch(r"pull/(\d+)/merge", r["ref"])
        no = m.group(1) if m else by_ref.get(r["ref"].removeprefix("origin/"))
        if no is None:
            die(f"CI run {r['id']} on {r['ref']}: no PR in the pulls snapshot has that branch")
        recs = sorted(glob.glob(os.path.join(I26, f"ci-compare-pr{no}.txt")) +
                      glob.glob(os.path.join(I26, f"ci-compare-pr{no}-*.txt")))
        if recs:
            die(f"{recs[0]}: exists but gives no job outcomes for CI run {r['id']} (PR #{no})")
    return runs


def api_json(name, need=(), each=None):
    """An API snapshot in _net/.  need: dotted fields the snapshot must have; each: (the list's
    dotted field, or "" for a top-level list; the dotted fields every row of it must have).
    A field written "path:str" must also be a string.  Checked here, before anything reads
    them, so a renamed or missing field is a named stop instead of a KeyError or TypeError."""
    p = os.path.join(NET, name)
    try:
        with open(p) as f:
            d = json.load(f)
    except OSError as e:
        die(f"{p}: cannot open the API snapshot ({e})")
    except ValueError as e:
        die(f"{p}: not JSON ({e})")
    for spec in need:
        json_field(p, d, spec, "the snapshot")
    if each is not None:
        lst = json_field(p, d, each[0], "the snapshot") if each[0] else d
        if not isinstance(lst, list):
            die(f"{p}: {each[0] or 'the snapshot'} is not a list")
        for i, row in enumerate(lst):
            for spec in each[1]:
                json_field(p, row, spec, f"row {i} of {each[0] or 'the list'}")
    return d


def json_field(p, obj, spec, where):
    path, _, kind = spec.partition(":")
    v = obj
    for k in path.split("."):
        if not isinstance(v, dict) or k not in v:
            die(f"{p}: {where} has no field {path}")
        v = v[k]
    if kind == "str" and not isinstance(v, str):
        die(f"{p}: {where}: field {path} is {type(v).__name__}, not a string")
    return v


def api_codes():
    """URL -> HTTP code of the latest fetch that got an answer.  codes.txt is the append-only
    log of every GET; a 000 (no HTTP answer, curl wrote no usable body) does not replace the
    file saved by the earlier fetch of the same URL, so it does not replace its code either."""
    codes = {}
    path = os.path.join(NET, "codes.txt")
    for i, ln in enumerate(text(path).splitlines(), 1):
        m = re.fullmatch(r"(\S+) (\d{3})", ln)
        if not m:
            die(f"{path}:{i}: not '<url> <3-digit HTTP code>': {ln!r}")
        if m.group(2) != "000":
            codes[m.group(1)] = int(m.group(2))
    return codes


# ------------------------------------------------------------------ judge verdict tally
VERDICTS = ["MERGE AFTER FIXES", "READY AFTER FIXES", "READY FOR ADAM'S DECISION", "MERGE"]
_V = r"(MERGE AFTER FIXES|READY AFTER FIXES|READY FOR ADAM'S DECISION|MERGE)"
V_LINE = [
    re.compile(r"^#.*[:：]\s*\*\*" + _V + r"\*\*"),                       # '# 複審（…）：**MERGE**'
    re.compile(r"^\|\s*`[^`]+`\s*@\s*`[0-9a-f]+`\s*\|\s*\*\*" + _V + r"\*\*"),  # table rows
    re.compile(r"^- \*\*`[0-9a-f]{7,}`（[^）]*）[:：]\s*" + _V),            # '- **`sha`（…）：MERGE…'
    # a verdict statement anywhere in the line, e.g. '一句話：… **合併裁決：MERGE**（…）' or
    # '## 判決：**MERGE**' or '**Verdict: MERGE AFTER FIXES.**' -- the keyword and the colon are
    # required, so a merge message quoted in prose ('judge MERGE on …') is not a verdict
    re.compile(r"(?:合併裁決|判決|裁決|裁定|總判定|Verdict(?: the evidence supports)?)\s*[:：]\s*"
               r"(?:\*\*)?\s*" + _V),
]
V_OTHER = re.compile(r"^- \*\*`[0-9a-f]{7,}`（[^）]*）[:：](?!\s*" + _V + r")(.+?)\*\*")
UTC = dt.timezone.utc
JUDGE_SINCE = dt.datetime(2026, 9, 16, tzinfo=UTC).timestamp()
# the snapshot of fig_q2: trunk fed37cff (pushed 2026-09-27T15:47:38Z) and every judge file
# whose mtime is at or before 15:55Z that day; later files are printed and not counted
TRUNK_SNAP = "fed37cff"
JUDGE_CUTOFF = dt.datetime(2026, 9, 27, 15, 55, tzinfo=UTC).timestamp()
# verdicts the unanchored pattern must find (judge-SLIDES930.md F-1), and the one file with none
JUDGE_EXPECT = {
    "orchestrator-0924/intake-0925/judge-HB-r4-e1245b40.md": ["MERGE"],
    "orchestrator-0924/intake-0926/judge-HBR4-79670365.md": ["MERGE"],
    "orchestrator-0924/intake-0926/judge-HBR6-3d297c34.md": ["MERGE"],
    "orchestrator-0924/intake-0926/judge-HBR7-a77b8fe2.md": ["MERGE AFTER FIXES"],
    "orchestrator-0924/intake-0926/judge-HBR7b-96abb9b0.md": ["MERGE"],
    "orchestrator-0924/intake-0926/judge-HBR8-3a724b87.md": ["MERGE"],
    "orchestrator-0924/intake-0925/judge-HB-r3-01ff8368.md": [],
}


def utc(iso):
    """An ISO time with an offset (or a trailing Z) -> 'MM-DD' in UTC."""
    try:
        t = dt.datetime.fromisoformat(iso.replace("Z", "+00:00").replace(" +0800", "+08:00"))
    except ValueError:
        die(f"{iso!r} is not an ISO time")
    return t.astimezone(UTC).strftime("%m-%d")


def judge_tally():
    files = sorted(glob.glob(os.path.join(LOGS, "**", "judge-*.md"), recursive=True))
    used, late, per_file = [], [], {}
    for f in files:
        mt = os.path.getmtime(f)
        if mt < JUDGE_SINCE:
            die(f"{f} is older than 2026-09-16 -- the tally's scope assumption broke")
        if mt > JUDGE_CUTOFF:
            late.append(f)
            continue
        used.append(f)
        hits = []
        for ln in text(f).splitlines():
            for p in V_LINE:
                m = p.search(ln)
                if m:
                    hits.append(m.group(1))
                    break
            else:
                if V_OTHER.search(ln):
                    hits.append("OTHER")
        per_file[os.path.relpath(f, LOGS)] = hits
    for k, want in JUDGE_EXPECT.items():
        if per_file.get(k) != want:
            die(f"{k}: verdicts {per_file.get(k)} != {want}")
    for k, v in sorted(per_file.items()):
        print(f"[judge] {k}: {v if v else '(no one-word verdict)'}")
    tally = {v: 0 for v in VERDICTS + ["OTHER"]}
    for hits in per_file.values():
        for h in hits:
            tally[h] += 1
    none = [k for k, v in per_file.items() if not v]
    return tally, per_file, none, late


# =================================================================== fig_q1
def fig_q1():
    # pins at the three states of p4_proxy/requirements.txt
    if git("rev-parse", "a4c951a8^1").strip()[:8] != "c0602510":
        die("a4c951a8's first parent is not c0602510")
    before, aligned, merged = pins_at("c0602510"), pins_at("a4c951a8"), pins_at("5dc7fc9a")
    now = pins_at(SNAPSHOT)
    want = {"protobuf": ("==3.20.3", "==3.20.3", "==5.29.6"),
            "p4runtime": ("==1.4.1", "==1.5.0", "==1.5.0"),
            "grpcio": (">=1.50.0", "==1.82.1", "==1.82.1"),
            "grpcio-tools": (None, None, "==1.71.2")}
    for k, (a, b, c) in want.items():
        got = (before.get(k), aligned.get(k), merged.get(k))
        if got != (a, b, c):
            die(f"pin {k}: {got} != {(a, b, c)}")
        if now.get(k) != c:
            die(f"pin {k} at {SNAPSHOT} is {now.get(k)}, not {c}")
    git("cat-file", "-e", f"{SNAPSHOT}:p4_proxy/regen_p4runtime_pb2.py")
    if git("cat-file", "-e", "a4c951a8:p4_proxy/regen_p4runtime_pb2.py", ok_rc=(0, 128)) is not None:
        die("regen_p4runtime_pb2.py already exists at a4c951a8")
    print(f"[q1] pins before {want['protobuf'][0]}, p4runtime {before['p4runtime']} -> "
          f"{aligned['p4runtime']}, grpcio {before['grpcio']} -> {aligned['grpcio']}; "
          f"merged protobuf {merged['protobuf']}, grpcio-tools {merged['grpcio-tools']}")

    # step 1: the aligned file's suites (orchestrator rerun on 851cefd7 = a4c951a8^2)
    if git("rev-parse", "a4c951a8^2").strip()[:8] != "851cefd7":
        die("a4c951a8's second parent is not 851cefd7")
    s1 = text(os.path.join(I25, "rerun-REQ-851cefd7.summary.log"))
    m = re.findall(r"^(aligned2|mainvenv): Ran (\d+) tests in [0-9.]+s OK \(skipped=1\) # p4_proxy "
                   r"rc=0 Ran (\d+) tests in [0-9.]+s OK # p4_exercise rc=0", s1, re.M)
    if len(m) != 2 or {x[1:] for x in m} != {("1557", "187")}:
        die(f"rerun-REQ-851cefd7.summary.log: {m}")
    if sorted(x[0] for x in m) != ["aligned2", "mainvenv"]:
        die(f"rerun-REQ-851cefd7.summary.log: suite labels {[x[0] for x in m]}, "
            f"not aligned2 + mainvenv")
    s1_tests = (int(m[0][1]), int(m[0][2]))

    # step 2: the 09-26 trial on the candidate venv
    j = text(os.path.join(I26, "pb5-trial/JOURNAL.txt"))
    starts = dict(re.findall(r"(phase\d) start: (.+)", j))
    ends = dict(re.findall(r"(phase\d) end rc=(\d+)", j))
    cand01 = [p for p, d in starts.items() if d.startswith("01 on venv-cand")]
    cand06 = [p for p, d in starts.items() if d.startswith("06 on venv-cand")]
    if len(cand01) != 1 or len(cand06) != 1 or any(ends.get(p) != "0" for p in cand01 + cand06):
        die(f"trial journal: 01/06 on venv-cand not once each with rc 0: {starts} {ends}")
    idx = text(os.path.join(I26, "pb5-trial/INDEX.txt"))
    r01 = grab(r"^01cand\.out .* raw live-p1/runs/(\S+)$", idx,
               "pb5-trial/INDEX.txt: the 01cand.out line with its live-p1 run dir", re.M)
    r06 = grab(r"^06cand\.out .* raw live-p1/runs/(\S+)$", idx,
               "pb5-trial/INDEX.txt: the 06cand.out line with its live-p1 run dir", re.M)
    must(os.path.join(I26, "pb5-trial/01cand.out"), "PASS 01_baseline")
    must(os.path.join(I26, "pb5-trial/06cand.out"),
         "PASS 06_thirteen -- 26 arm(s), every arm as the exercise says it should be")
    trial = check06("trial", r06, r01, "580767a8")
    if "protobuf==5.29.6" not in text(os.path.join(I26, "pb5-trial/dists_cand.txt")) or \
            "protobuf==3.20.3" not in text(os.path.join(I26, "pb5-trial/dists_main.txt")):
        die("trial dists: candidate is not 5.29.6 or main is not 3.20.3")

    # step 3: the merge, and the orchestrator's gates on the test merge ac0c3b64
    if [x[:8] for x in git("log", "-1", "--format=%P", "5dc7fc9a").split()] != ["d9308f61",
                                                                                 "ab026ef0"]:
        die("5dc7fc9a is not the merge of ab026ef0 into d9308f61")
    must(os.path.join(I26, "judge-PB5PREP-6351be15.md"), "## 裁決：READY AFTER FIXES",
         "（`d2e4708a`）：**READY FOR ADAM'S DECISION**", "（`5bb5f1fa`）：**READY FOR ADAM'S DECISION**")
    gs = re.findall(r"^(\S+) # rc=(\d+)", text(os.path.join(I26, "pb5-merge/rerun-summary.ac0c3b64.txt")),
                    re.M)
    g_ok = sum(1 for _, rc in gs if rc == "0")
    if len(gs) != 6 or g_ok != 5 or dict(gs).get("test_ndt_serve") != "1":
        die(f"test-merge gates: {gs}")

    # step 4: the venv migration -- the same two suites before (old venv) and after (new venv)
    mig = text(os.path.join(I26, "pb5-merge/migrate.log"))
    if not mig.startswith("# 2026-09-27T07:43:38Z trunk 5dc7fc9a") or "old venv protobuf 3.20.3" \
            not in mig.splitlines()[0]:
        die("migrate.log line 1 is not trunk 5dc7fc9a / old venv 3.20.3")
    head, _, tail = mig.partition("parked: OLD=")
    ran = re.findall(r"^Ran (\d+) tests\nOK \(skipped=1\)$", head, re.M)
    if ran != ["1658", "187"]:
        die(f"migrate.log baseline suites: {ran}")
    if "VERIFIED: /home/adam/Desktop/NDTwin-Kernel/p4_proxy/venv passes what the old venv passed" \
            not in tail:
        die("migrate.log has no VERIFIED line after the move")
    inner = must(os.path.join(I26, "pb5-merge/inner-migrate.txt"),
                 'suites "$V" > "$OLD.new" && diff "$OLD.baseline" "$OLD.new"')
    del inner
    inst = tail.split("checking the installed package (default backend):", 1)
    if len(inst) != 2:
        die("migrate.log: no installed-package check")
    desc = re.findall(r"^  (\S+\.proto)\s+descriptor identical", inst[1], re.M)
    if len(desc) != 4:
        die(f"migrate.log installed-package descriptors: {desc}")
    parked_new = "/home/adam/p4_proxy-venv.protobuf3.20.3-20260927-154343.new"
    if os.path.exists(parked_new):     # the parked copy: when present, it must equal the baseline
        if re.findall(r"^Ran (\d+) tests", text(parked_new), re.M) != ["1658", "187"]:
            die(f"{parked_new} disagrees with the baseline")
    frz = text(os.path.join(I26, "pb5-merge/venv-after.freeze"))
    if "protobuf==5.29.6" not in frz or "grpcio-tools==1.71.2" not in frz:
        die("venv-after.freeze is not protobuf 5.29.6 + grpcio-tools 1.71.2")
    mig_tests = (int(ran[0]), int(ran[1]))

    # step 5: live acceptance on the migrated venv
    la = text(os.path.join(I26, "pb5-merge/live-accept.log"))
    for n_ in ("trunk 5dc7fc9a657cf58b12729ec14e2ead02f7afdab5; venv 5.29.6 upb",
               "end 01 rc=0 last: PASS 01_baseline",
               "end 06 rc=0 last: PASS 06_thirteen -- 26 arm(s), every arm as the exercise says it "
               "should be", "DONE rc01=0 rc06=0"):
        if n_ not in la:
            die(f"live-accept.log lacks {n_!r}")
    a01 = grab(r"01 run dir: .*/live-p1/runs/(\S+)", la, "live-accept.log: the '01 run dir:' line")
    a06 = grab(r"06 run dir: .*/live-p1/runs/(\S+)", la, "live-accept.log: the '06 run dir:' line")
    accept = check06("acceptance", a06, a01, "5dc7fc9a")

    # step 6: CI before (d9308f61, protobuf 3.20.3) and after (7746832e, protobuf 5.29.6)
    must(os.path.join(I26, "ci-compare-7746832e.txt"), "IDENTICAL -- prediction met")
    must(os.path.join(I26, "ci-prediction-7746832e.txt"), "BEFORE runs 36305829213")
    pre, post = (text(os.path.join(I26, f"ci-{r}-gcc.raw.log")) for r in ("36303713298",
                                                                          "36305829213"))
    if "protobuf-3.20.3" not in pre or "protobuf-5.29.6" not in post:
        die("CI installs: before is not 3.20.3 or after is not 5.29.6")
    if len(re.findall(r"descriptor identical", post)) != 8:
        die("CI after: not 2 x 4 'descriptor identical' lines")

    def failed(t):
        return [re.sub(r"^\S*Z ", "", ln.lstrip("﻿")) for ln in t.splitlines()
                if re.search(r"FAILED|FAIL:", ln)]
    fp, fq = failed(pre), failed(post)
    lp, lq = L1_RE.findall(pre), L1_RE.findall(post)
    if fp != fq or lp != lq or lp != ["12"]:
        die(f"CI failure lines differ or L1 is not 12 on both: {lp} {lq} {len(fp)} {len(fq)}")
    ci_groups = int(lq[0])
    print(f"[q1] REQ {s1_tests}; trial 06 {trial}; gates {g_ok}/{len(gs)}; migrate {mig_tests}, "
          f"{len(desc)} descriptors; accept 06 {accept}; CI L1 {ci_groups} both, "
          f"{len(fq)} failure lines identical")

    # the date of each step, in UTC, from its own record
    days = [utc(git("log", "-1", "--format=%cI", "a4c951a8").strip()),
            utc(grab(r"(\S+Z) ", j, "pb5-trial/JOURNAL.txt: a leading UTC time", at_start=True)),
            utc(git("log", "-1", "--format=%cI", "5dc7fc9a").strip()),
            utc(grab(r"# (\S+Z) ", mig, "migrate.log: a leading UTC time", at_start=True)),
            utc(grab(r"== (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d \+0800)", la,
                     "live-accept.log: a leading '== <time> +0800' line", at_start=True)
                .replace(" +0800", "+08:00").replace(" ", "T", 1)),
            utc(grab(TS_RE, post[:200], "ci-36305829213-gcc.raw.log: a time in its first 200 "
                                        "characters") + "Z")]
    print(f"[q1] step dates (UTC): {days}")

    # ---- draw
    H = 5.75
    fig, ax = canvas(H)
    txt(ax, 0.45, 0.48, f"protobuf {want['protobuf'][0][2:]} → {want['protobuf'][2][2:]} "
        "in the P4 proxy", size=22, weight="bold", ha="left")
    x0, bw, gap, by, bh = 0.45, 1.89, 0.222, 1.78, 1.36
    xs = [x0 + i * (bw + gap) for i in range(6)]
    # version lane
    ly, lh = 1.05, 0.42
    # rule 3 (coordinator, round 3): the lane and the step boxes are read from git; the result
    # cells come from test, gate, live and CI logs
    txt(ax, x0, ly - 0.16, "READ · requirements, step names and dates from git", size=11,
        weight="bold", color=FAINT, ha="left")
    ax.add_patch(Rectangle((xs[0], ly), xs[1] + bw - xs[0], lh, facecolor=GREY, edgecolor="none",
                           zorder=1))
    ax.add_patch(Rectangle((xs[2], ly), xs[5] + bw - xs[2], lh, facecolor=ACCENT,
                           edgecolor="none", zorder=1))
    txt(ax, (xs[0] + xs[1] + bw) / 2, ly + lh / 2,
        f"requirements: protobuf {want['protobuf'][0][2:]}", size=13.5, weight="bold", color=INK)
    txt(ax, (xs[2] + xs[5] + bw) / 2, ly + lh / 2,
        f"requirements: protobuf {want['protobuf'][2][2:]}", size=13.5, weight="bold",
        color=WHITE)
    steps = [
        (days[0], "pins = venv", f"p4runtime {aligned['p4runtime'][2:]}\ngrpcio {aligned['grpcio'][2:]}"),
        (days[1], "live trial", "candidate venv\n" + f"protobuf {want['protobuf'][2][2:]}"),
        (days[2], "merge", f"+ grpcio-tools {merged['grpcio-tools'][2:]}\n+ regen tool"),
        (days[3], "venv migrated", "old venv\nparked"),
        (days[4], "live acceptance", "migrated venv"),
        (days[5], "CI", "7746832e"),
    ]
    for i, (d, name, sub) in enumerate(steps):
        x = xs[i]
        hot = i == 2
        box(ax, x, by, bw, bh, fill=ACCENT_BG if hot else WHITE, edge=ACCENT if hot else INK,
            lw=2.2 if hot else 1.2)
        txt(ax, x + bw / 2, by + 0.25, d, size=11.5, color=FAINT)
        txt(ax, x + bw / 2, by + 0.55, name, size=14, weight="bold", color=ACCENT if hot else INK)
        txt(ax, x + bw / 2, by + 1.00, sub, size=11.5, color=MUTED, mono=(i == 5))
        if i:
            arrow(ax, x - gap + 0.02, by + bh / 2, x - 0.02, by + bh / 2)
    # checks under each step
    checks = [
        [(GREEN, f"{s1_tests[0]} + {s1_tests[1]} tests")],
        [(GREEN, "01: rc 0"), (GREEN, f"06: {trial[1]}/{trial[0]} arms")],
        [(AMBER, f"gates {g_ok}/{len(gs)}")],
        [(GREEN, f"{mig_tests[0]} + {mig_tests[1]} tests"), (GREEN, "same as old venv"),
         (GREEN, f"{len(desc)} descriptors same")],
        [(GREEN, "01: PASS"), (GREEN, f"06: {accept[1]}/{accept[0]} arms")],
        [(WARNC, f"L1: {ci_groups} groups"), (WARNC, "lines identical")],
    ]
    # one compact result cell per step (judge re-check item 13: not a bullet list); the step's
    # status is the colour of the cell's top strip -- every step here has a single status
    cy0, ch = by + bh + 0.38, 1.40
    txt(ax, x0, cy0 - 0.15, "RAN IT · test, gate, live-run and CI logs", size=11, weight="bold",
        color=FAINT, ha="left")
    for i, items in enumerate(checks):
        cols = {c for c, _ in items}
        if len(cols) != 1:
            die(f"q1 step {i}: mixed statuses {cols}")
        c = cols.pop()
        ax.add_patch(Rectangle((xs[i], cy0), bw, ch, facecolor=PANEL, edgecolor=RULE, lw=1.0,
                               zorder=2))
        ax.add_patch(Rectangle((xs[i], cy0), bw, 0.09, facecolor=c, edgecolor="none", zorder=3))
        n_ = len(items)
        for k, (_c, s_) in enumerate(items):
            y = cy0 + 0.09 + (ch - 0.09) / 2 + (k - (n_ - 1) / 2) * 0.36
            txt(ax, xs[i] + bw / 2, y, s_, size=12, color=BODY)
    # legend (three strips, no sentences)
    lx, lyy = 0.45, H - 0.30
    for c, lab in ((GREEN, "passed"), (AMBER, "partial"),
                   (WARNC, f"CI red (same {ci_groups} groups)")):
        ax.add_patch(Rectangle((lx, lyy - 0.05), 0.34, 0.10, facecolor=c, edgecolor="none"))
        txt(ax, lx + 0.44, lyy, lab, size=11.5, color=MUTED, ha="left")
        lx += 0.44 + 0.085 * len(lab) + 0.4
    save(fig, "fig_q1_protobuf5")
    return dict(s1=s1_tests, trial=trial, gates=(g_ok, len(gs)), mig=mig_tests, desc=len(desc),
                accept=accept, ci=ci_groups, nfail=len(fq))


# =================================================================== fig_q2
def fig_q2():
    tally, per_file, none, late = judge_tally()
    nverd = sum(tally.values())
    # one snapshot: trunk fed37cff, and it must still have been trunk's tip at the judge cutoff
    snap_t = dt.datetime.fromisoformat(git("log", "-1", "--format=%cI", TRUNK_SNAP).strip())
    if snap_t.timestamp() > JUDGE_CUTOFF:
        die(f"{TRUNK_SNAP} is younger than the judge cutoff")
    for t_ in git("log", "--first-parent", "--format=%cI", f"{TRUNK_SNAP}..trunk").split():
        if dt.datetime.fromisoformat(t_).timestamp() <= JUDGE_CUTOFF:
            die(f"trunk moved past {TRUNK_SNAP} before the judge cutoff -- re-pick the snapshot")
    merges = git("log", "--first-parent", "--merges", "--since=2026-09-16T00:00:00Z",
                 "--format=%H", TRUNK_SNAP).split()
    # a merge "names a judge" when its full message does (git log -1 --format=%B); only the
    # subject would give a smaller count, printed for the record
    named = [h for h in merges if re.search(r"judge", git("log", "-1", "--format=%B", h), re.I)]
    named_subj = [h for h in merges if re.search(r"judge", git("log", "-1", "--format=%s", h),
                                                 re.I)]
    cut = dt.datetime.fromtimestamp(JUDGE_CUTOFF, UTC).strftime("%Y-%m-%dT%H:%MZ")
    print(f"[q2] {len(per_file)} judge files (mtime <= {cut}), "
          f"{nverd} verdict lines: {tally}; files without a one-word verdict: {none}; "
          f"after cutoff (not counted): {late}")
    print(f"[q2] {len(merges)} first-parent merges since 2026-09-16T00:00Z on {TRUNK_SNAP} "
          f"(committed {snap_t.astimezone(UTC).isoformat()}); {len(named)} name a judge in the "
          f"full message ({len(named_subj)} in the subject)")

    # worked example: heartbeat segment W
    mut = text(os.path.join(GATES, "mutate_p4_heartbeat_w.p4hbw-ebdf365e.log"))
    m_red = re.search(r"every new proxy test seen red: (\d+) of (\d+)", mut)
    m_mut = re.search(r"mutation gate: (\d+) mutations, (\d+) survived", mut)
    if not (m_red and m_mut) or not mut.startswith("ebdf365e"):
        die("HB W mutation log: head / seen-red / mutation lines missing")
    hbw = text(os.path.join(I26, "judge-HBW-1a3ebd7f.md"))
    if "## 0. 總判定：**MERGE AFTER FIXES**" not in hbw or \
            "# R2 複審（`ebdf365e`，1a3ebd7f..ebdf365e 9 commits）：**MERGE**" not in hbw:
        die("judge-HBW: the two verdict lines moved")
    r3 = text(os.path.join(I26, "hbw/rerun3-summary.7b600ab0.txt"))
    m_px = re.search(r"^p4_proxy_suite # rc=0 \| Ran (\d+) tests in [0-9.]+s OK", r3, re.M)
    if not m_px or "tracked tree clean after the gates" not in r3 or \
            len(re.findall(r"# rc=0", r3)) != len(re.findall(r"# rc=", r3)):
        die("rerun3-summary.7b600ab0.txt: not every gate rc 0")
    par = [p[:8] for p in git("log", "-1", "--format=%P", "cafd518a").split()]
    if par != ["9c2e59e4", "ebdf365e"]:
        die(f"cafd518a parents {par}")
    push = must(os.path.join(I26, "push-cafd518a.log"), "To github.com:Adam010341/NDTwin-Kernel-P4.git",
                "To github.com:ndtwin-lab/NDTwin-Kernel-P4.git", "9c2e59e4..cafd518a  trunk -> trunk")
    n200 = len(re.findall(r"^200$", push, re.M))
    if n200 != 2:
        die(f"push-cafd518a.log: {n200} public 200 read-backs, want 2")
    l1_before, l1_after, l1_fixed = l1_of("9c2e59e4", "cafd518a", "3f8c2abf")
    must(os.path.join(I26, "ci-compare-cafd518a.txt"), "NEW RED: tests/python/test_ndt_serve.py")
    if not (l1_after == l1_before + 1 == l1_fixed + 1) or not is_ancestor("329dc555", "3f8c2abf"):
        die(f"HB W CI: {l1_before} -> {l1_after} -> {l1_fixed}")
    print(f"[q2] HB W: {m_red.group(1)}/{m_red.group(2)} red, {m_mut.group(1)} mutations "
          f"{m_mut.group(2)} survived; test merge 7b600ab0 proxy {m_px.group(1)} OK; "
          f"CI L1 {l1_before}->{l1_after}, fix 329dc555 -> {l1_fixed}")

    # ---- draw
    H = 6.9
    fig, ax = canvas(H)
    txt(ax, 0.45, 0.48, "How a change gets into trunk", size=22, weight="bold", ha="left")
    x0, bw, gap, by, bh = 0.45, 1.89, 0.222, 1.45, 1.0
    xs = [x0 + i * (bw + gap) for i in range(6)]
    names = [("worker", "worktree · red first"), ("judge", "independent"),
             ("test merge", "gates re-run"), ("merge --no-ff", "into trunk"),
             ("push", "both repos"), ("CI", "vs prediction")]
    for i, (a, b) in enumerate(names):
        hot = i == 1
        box(ax, xs[i], by, bw, bh, fill=ACCENT_BG if hot else WHITE, edge=ACCENT if hot else INK,
            lw=2.2 if hot else 1.2)
        txt(ax, xs[i] + bw / 2, by + 0.36, a, size=14, weight="bold", color=ACCENT if hot else INK,
            mono=(i == 3))
        txt(ax, xs[i] + bw / 2, by + 0.70, b, size=11.5, color=MUTED)
        if i:
            arrow(ax, xs[i] - gap + 0.02, by + bh / 2, xs[i] - 0.02, by + bh / 2)
    # the two ways back to the worker: a judge's AFTER FIXES (below), a new red in CI (above)
    arrow(ax, xs[1] + bw * 0.45, by + bh + 0.02, xs[0] + bw * 0.55, by + bh + 0.02, color=AMBER,
          lw=1.8, rad=-0.5)
    txt(ax, (xs[0] + xs[1] + bw) / 2, by + bh + 0.68, "AFTER FIXES", size=11.5, color=AMBER,
        weight="bold")
    x_a, x_b = xs[5] + bw * 0.5, xs[0] + bw * 0.5
    arrow(ax, x_a, by - 0.02, x_b, by - 0.02, color=WARNC, lw=1.4, rad=0.1, ls=(0, (4, 3)))
    txt(ax, (x_a + x_b) / 2, by - 0.02 - 0.1 * (x_a - x_b) / 2 - 0.16, "new red in CI",
        size=11.5, color=WARNC, weight="bold")

    # ---- counts since 09-16
    sy = 3.42
    txt(ax, 0.45, sy, "READ · SINCE 09-16", size=11.5, color=FAINT, weight="bold", ha="left")
    txt(ax, 0.45, sy + 0.28, f"at {TRUNK_SNAP}", size=11.5, color=FAINT, ha="left", mono=True)
    # verdict bar under judge (spanning judge + test merge columns)
    bx, bwid, bhh, byy = xs[1], xs[2] + bw - xs[1], 0.44, sy + 0.30
    segs = [(tally["MERGE"], GREEN, "MERGE"),
            (tally["MERGE AFTER FIXES"] + tally["READY AFTER FIXES"], AMBER, "AFTER FIXES"),
            (tally["READY FOR ADAM'S DECISION"] + tally["OTHER"], GREY, "other")]
    tot = sum(s[0] for s in segs)
    if tot != nverd:
        die("verdict segments do not add up")
    cx = bx
    for n_, col, lab in segs:
        w_ = bwid * n_ / tot
        ax.add_patch(Rectangle((cx, byy), w_, bhh, facecolor=col, edgecolor=WHITE, lw=1.5,
                               zorder=3))
        txt(ax, cx + w_ / 2, byy + bhh / 2, str(n_), size=13, weight="bold",
            color=WHITE if col != GREY else INK)
        txt(ax, cx + w_ / 2, byy + bhh + 0.24, lab, size=11, color=MUTED)
        cx += w_
    # ">=": the tally covers logs/**/judge-*.md only; judge files elsewhere (e.g. the hunt-0911
    # *-JUDGE.md that FIXED-SINCE-916 cites) are not in it
    txt(ax, bx, sy, f"≥ {tot} verdicts", size=13, weight="bold", color=INK, ha="left")
    # merges under merge
    mx = xs[3] + bw / 2
    txt(ax, mx, sy + 0.42, str(len(merges)), size=26, weight="bold", color=INK)
    txt(ax, mx, sy + 0.86, "merges", size=12, color=MUTED)
    txt(ax, mx, sy + 1.12, f"{len(named)} name a judge", size=11, color=MUTED)

    # ---- worked example
    ey = 5.12
    ex_day = utc(git("log", "-1", "--format=%cI", "cafd518a").strip())
    txt(ax, 0.45, ey - 0.22, f"RAN IT · EXAMPLE · HEARTBEAT W · {ex_day}", size=11.5, color=FAINT,
        weight="bold", ha="left")
    eh = 1.12
    facts = [
        [(f"{m_red.group(1)}/{m_red.group(2)} seen red", BODY, False),
         (f"{int(m_mut.group(1)) - int(m_mut.group(2))}/{m_mut.group(1)} mutants killed", BODY,
          False)],
        [("AFTER FIXES", AMBER, False), ("→ MERGE", GREEN, False)],
        [("7b600ab0", BODY, True), (f"{m_px.group(1)} tests OK", BODY, False)],
        [("cafd518a", BODY, True)],
        [("2 repos", BODY, False), (f"public: {n200}×200", BODY, False)],
        [(f"L1 {l1_before} → {l1_after}", WARNC, False), ("fix 329dc555", BODY, True)],
    ]
    for i, lines in enumerate(facts):
        box(ax, xs[i], ey, bw, eh, fill=PANEL, edge=RULE, lw=1.0)
        n_ = len(lines)
        for k, (s, col, mono) in enumerate(lines):
            y = ey + eh / 2 + (k - (n_ - 1) / 2) * 0.36
            txt(ax, xs[i] + bw / 2, y, s, size=12.5, color=col, mono=mono,
                weight="bold" if col in (AMBER, GREEN, WARNC) else "normal")
    save(fig, "fig_q2_review_path")
    return dict(tally=tally, per_file=per_file, none=none, late=late, merges=len(merges),
                named=len(named), named_subject=len(named_subj), red=(m_red.group(1), m_red.group(2)),
                mut=(m_mut.group(1), m_mut.group(2)), proxy=m_px.group(1),
                l1=(l1_before, l1_after, l1_fixed))


# =================================================================== fig_q3
def fig_q3():
    # (a) a privilege bug in a cleanup path, found by the KJL judge (blocker B2); only the
    #     verdict lines are checked here -- the finding itself is not restated anywhere
    must(os.path.join(I26, "kjl/judge-KJL-4a96f894.md"), "## 判決：MERGE AFTER FIXES", "### B2")
    must(os.path.join(I26, "kjl/judge-KJL-15217241.md"), "**Verdict: MERGE AFTER FIXES.**")
    rf = must(os.path.join(GATES, "redfirst_b2.rkjl6-15217241.log"),
              "judged: rc 1", "head: rc 0")
    del rf
    # "trunk" here is the refresh state STATE, not the moving ref, so this card and fig_q4/q5
    # describe the same trunk commit.  Re-pin 09-28: the branch is merged (fc25112e) and its PR
    # squash-merged into main (#15), so the card says "fixed / merged"; the fix must be in STATE
    kjl_head = git("rev-parse", "fix/rulings-kjl-0927").strip()[:8]
    if not is_ancestor("15217241", kjl_head) or not is_ancestor("06b162f7", "15217241") or \
            not is_ancestor(kjl_head, STATE) or not is_ancestor("06b162f7", STATE):
        die(f"KJL: the fix is not on fix/rulings-kjl-0927 above 15217241, or the branch is not "
            f"merged into trunk {STATE} -- the card says fixed and merged")
    print(f"[q3] fix/rulings-kjl-0927 at {kjl_head}, merged into trunk {STATE}")
    # (b) heartbeat measurement phase-locked (report judge Blocking 1; de-phased runs 3-4)
    must(os.path.join(I26, "judge-HBSPIKEDOC-4820862b.md"), "### Blocking 1：相位鎖的後果沒推到底",
         "φ≈0.62–0.80 s")
    must(os.path.join(REPO, "doc/audit/2026-09-25_p4-heartbeat/P4-HB-SPIKE.md"),
         "### 2.3 run 1–2 的相位鎖", "### 2.4 run 3–4：去相位鎖")
    if not is_ancestor("9c2e59e4", SNAPSHOT) or "de-phased" not in git("log", "-1", "--format=%s",
                                                                        "9c2e59e4"):
        die("9c2e59e4 is not the de-phased report merge in trunk")
    # (c) G1 PASS while nothing reached h3 (GAP-2b section 4-1, uncommitted)
    gap = os.path.join(PREP, "GAP-2b-ndtwin-p4-capabilities-2026-09-27.md")
    must(gap, "flowcache／solution 的 G1 在 T06 PASS，但 iperf 一個 datagram 都沒到 h3。")
    arm = os.path.join(ARMS, "2026-09-27T081256Z_flowcache_solution_ndtwin")
    srv = text(os.path.join(arm, "link_usage/iperf_server.txt"))
    if re.search(r"\bsec\b", srv) or "Server listening on UDP port 5001" not in srv:
        die("iperf_server.txt now has a report row")
    must(os.path.join(arm, "link_usage/iperf_client.txt"), "Sent 3500 datagrams",
         "did not receive ack of last datagram")
    must(arm + ".md", "   PASS G1  link usage follows the iperf path")
    t06 = os.path.join(LIVE, "2026-09-27T074635Z_06_thirteen/00_table.tsv")
    rows = {(r[0], r[1]): r for r in csv.reader(text(t06).splitlines(), delimiter="\t")
            if len(r) >= 2}
    if len(rows.get(("flowcache", "solution"), ())) < 4:
        die(f"{t06}: no flowcache/solution row with a verdict")
    if not rows[("flowcache", "solution")][3].startswith("PASS"):
        die("T06 flowcache/solution is not PASS")
    fixes = []
    for b in git("for-each-ref", "--format=%(refname:short)", "refs/heads").split():
        if b in ("audit-raw", "claude-memory"):      # raw archives, not code branches
            continue
        for s in git("log", "--format=%s", f"trunk..{b}").splitlines():
            if re.search(r"\bG1\b", s):
                fixes.append((b, s))
    c_status = "open" if not fixes else "fix on branch"
    # (d) H5 sampler recorded nothing (first H5 run), fixed by 0925d9fc
    h5 = os.path.join(LIVE, "2026-09-26T153259Z_08_heartbeat")
    if os.path.exists(os.path.join(h5, "50_samples.tsv")):
        die("the first H5 run now has 50_samples.tsv")
    must(os.path.join(I26, "hbw-live/h5-20260926T153259Z.log"), "FAIL 08_heartbeat -- H5")
    h5b = os.path.join(LIVE, "2026-09-26T172912Z_08_heartbeat/50_samples.tsv")
    if not os.path.exists(h5b):
        die("the H5 re-run has no 50_samples.tsv")
    must(os.path.join(I26, "hbw-live/h5b-20260926T172912Z.log"), "PASS 08_heartbeat")
    if not is_ancestor("0925d9fc", SNAPSHOT) or "SyntaxError" not in git("log", "-1", "--format=%B",
                                                                        "0925d9fc"):
        die("0925d9fc is not the H5 sampler fix in trunk")
    # (e) ndt edits moved ndt serve's line anchors -> CI L1 +1, fixed by 329dc555
    must(os.path.join(I26, "ci-compare-cafd518a.txt"), "NEW RED: tests/python/test_ndt_serve.py",
         "L1 FAILED (15 problem group(s))")
    if l1_of("9c2e59e4", "cafd518a", "3f8c2abf") != (14, 15, 14) \
            or not is_ancestor("329dc555", SNAPSHOT):
        die("anchor catch: L1 is not 14 -> 15 -> 14, or 329dc555 not in trunk")
    print(f"[q3] cards verified; G1 fix commits on local branches: {fixes or 'none'}")

    cards = [
        ("Privilege bug\nin a cleanup\npath", "judge", "09-27", "fixed\nmerged", GREEN),
        ("Heartbeat test\nwas phase-locked", "judge", "09-26", "re-measured\nmerged", GREEN),
        ("G1 PASS,\nnothing\ndelivered", "raw review", "09-27", c_status, WARNC),
        ("H5 sampler\nrecorded nothing", "live run", "09-26", "fixed\nmerged", GREEN),
        ("ndt edit broke\nserve anchors", "CI", "09-26", "fixed\nmerged", GREEN),
    ]
    H = 5.4
    fig, ax = canvas(H)
    txt(ax, 0.45, 0.48, "What review caught since 09-16", size=22, weight="bold", ha="left")
    x0, cw, gap, cy, ch = 0.45, 2.33, 0.2, 1.05, 3.95
    for i, (what, by, when, status, col) in enumerate(cards):
        x = x0 + i * (cw + gap)
        box(ax, x, cy, cw, ch, fill=WHITE, edge=RULE, lw=1.3, r=0.08)
        txt(ax, x + 0.2, cy + 0.32, what, size=15.5, weight="bold", color=INK, ha="left",
            va="top")
        ax.plot([x + 0.2, x + cw - 0.2], [cy + 1.72, cy + 1.72], color=RULE, lw=1.0, zorder=4)
        txt(ax, x + 0.2, cy + 2.02, "caught by", size=11, color=FAINT, ha="left",
            va="center_baseline")
        txt(ax, x + 0.2, cy + 2.38, by, size=14, weight="bold", color=ACCENT, ha="left",
            va="center_baseline")
        txt(ax, x + cw - 0.2, cy + 2.02, "found", size=11, color=FAINT, ha="right",
            va="center_baseline")
        txt(ax, x + cw - 0.2, cy + 2.38, when, size=14, color=BODY, ha="right",
            va="center_baseline")
        box(ax, x + 0.18, cy + 2.72, cw - 0.36, 0.98, fill=col, edge=col, lw=1.0, r=0.06, z=3)
        txt(ax, x + cw / 2, cy + 3.21, status, size=13.5, weight="bold",
            color=INK if col == AMBER else WHITE)
    save(fig, "fig_q3_review_catches")
    return dict(g1_fixes=fixes)


# =================================================================== fig_q4
def fig_q4():
    runs = ci_jobs(ci_logs())
    ids = [r["id"] for r in runs]
    # ndtwin-lab trunk CI runs since API_ONLY_SINCE that have no GCC log on disk, from the
    # unauthenticated API snapshot: jobs only (a job's log needs auth), drawn "no log"
    codes = api_codes()
    ru = "https://api.github.com/repos/ndtwin-lab/NDTwin-Kernel-P4/actions/runs?per_page=30"
    if codes.get(ru) != 200:
        die("API runs snapshot is not HTTP 200")
    rl = api_json("runs_ndtwin-lab.json", each=("workflow_runs", [
        "id", "name", "event", "head_branch", "status", "head_sha:str", "conclusion",
        "created_at:str"]))
    wr = rl["workflow_runs"]
    if not wr or min(r["created_at"] for r in wr) > API_ONLY_SINCE:
        die(f"API runs snapshot does not reach back to {API_ONLY_SINCE}")
    trunk_ci = [r for r in wr if r["name"] == "CI" and r["event"] == "push"
                and r["head_branch"] == "trunk" and API_ONLY_SINCE <= r["created_at"] < CI_CUTOFF + "Z"]
    if not trunk_ci or max(trunk_ci, key=lambda r: r["created_at"])["head_sha"][:8] != STATE:
        die(f"API runs: the newest trunk CI run is not on {STATE}: "
            f"{[(r['id'], r['head_sha'][:8]) for r in trunk_ci[:3]]}")
    for r in trunk_ci:
        if str(r["id"]) in ids:
            continue
        if r["status"] != "completed":
            die(f"API runs: trunk CI run {r['id']} on {r['head_sha'][:8]} is {r['status']}")
        ju = f"https://api.github.com/repos/ndtwin-lab/NDTwin-Kernel-P4/actions/runs/{r['id']}/jobs"
        if codes.get(ju) != 200:
            die(f"API jobs snapshot of run {r['id']} is not HTTP 200")
        api, _, head = api_jobs(r["id"])
        if head[:8] != r["head_sha"][:8]:
            die(f"_net/jobs_{r['id']}.json: jobs on {head[:8]}, the run is on {r['head_sha'][:8]}")
        runs.append(dict(id=str(r["id"]), t=r["created_at"][:19], sha=r["head_sha"][:8],
                         kind="trunk", l1=None, jobs=api, jobs_src=f"_net/jobs_{r['id']}.json",
                         repo="ndtwin-lab/NDTwin-Kernel-P4", ref="origin/trunk"))
    ids = [r["id"] for r in runs]
    if len(set(ids)) != len(ids):
        die(f"duplicate CI run id: {sorted({i for i in ids if ids.count(i) > 1})}")
    runs.sort(key=lambda r: r["t"])
    # earlier attempts of a drawn run (its red GCC job re-run): their GCC logs are
    # CIRAW/earlier/ci-<run>-gcc.job<job>.attempt<k>.raw.log; the drawn point is the run's latest
    # attempt (what the jobs snapshot reports), and a red earlier attempt puts a ring around it
    earlier = {}
    for p in sorted(glob.glob(os.path.join(CIRAW, "earlier", "*"))):
        mm = re.fullmatch(r"ci-(\d+)-gcc\.job(\d+)\.attempt(\d+)\.raw\.log", os.path.basename(p))
        if not mm:
            die(f"{p}: not ci-<run>-gcc.job<job>.attempt<k>.raw.log")
        rid, att = mm.group(1), int(mm.group(3))
        r = next((x for x in runs if x["id"] == rid), None)
        if r is None:
            die(f"{p}: an earlier attempt of run {rid}, which is not drawn")
        t = text(p)
        l1, ok = L1_RE.findall(t), len(L1_PASS_RE.findall(t))
        fe, co, hd = FETCH_RE.search(t), CHECKOUT_RE.search(t), HEAD_RE.search(t)
        sha = (fe.group(1) if fe else hd.group(1) if co and hd else "")[:8]
        if len(l1) + ok != 1 or sha != r["sha"]:
            die(f"{p}: not one 'L1 FAILED'/'L1 passed' line, or not on the drawn run's commit "
                f"{r['sha']} ({sha or 'none'})")
        latest = {j["run_attempt"] for j in api_json(f"jobs_{rid}.json",
                                                     each=("jobs", ["run_attempt"]))["jobs"]}
        if len(latest) != 1 or att >= min(latest):
            die(f"{p}: attempt {att} is not earlier than run {rid}'s attempt in the jobs snapshot "
                f"{sorted(latest)}")
        earlier.setdefault(rid, []).append((att, int(l1[0]) if l1 else 0))
    for r in runs:
        r["earlier"] = sorted(earlier.get(r["id"], []))
    for r in runs:
        print(f"[q4] {r['t']} {r['id']} {r['repo']:30s} {r['kind']:5s} {r['sha']} L1={r['l1']} "
              f"jobs={'' if not r['jobs'] else ','.join(r['jobs'][k][0] for k, _ in JOBS)}")
    # every recorded job pattern (printed for the record)
    pats = {tuple(r["jobs"][k] for k, _ in JOBS) for r in runs if r["jobs"]}
    print(f"[q4] job patterns seen: {pats}")

    H = 6.4
    fig = plt.figure(figsize=(W, H))
    top = fig.add_axes([0.125, 0.43, 0.845, 0.40])
    bot = fig.add_axes([0.125, 0.10, 0.845, 0.215])
    n = len(runs)
    xs = list(range(n))
    # day bands
    days = [r["t"][:10] for r in runs]
    starts = [i for i in range(n) if i == 0 or days[i] != days[i - 1]]
    for ax_ in (top, bot):
        for s in starts[1:]:
            ax_.axvline(s - 0.5, color=RULE, lw=1.0, ls=(0, (3, 3)), zorder=0)
    for k, s in enumerate(starts):
        e = starts[k + 1] if k + 1 < len(starts) else n
        top.text((s + e - 1) / 2, 1.01, days[s][5:], ha="center", va="bottom", fontsize=12.5,
                 color=MUTED, transform=top.get_xaxis_transform())
    # L1 series (runs with a log)
    pts = [(i, r["l1"]) for i, r in enumerate(runs) if r["l1"] is not None]
    top.plot([p[0] for p in pts], [p[1] for p in pts], color=RULE, lw=1.4, zorder=1)
    marker = {"trunk": ("o", ACCENT, ACCENT), "main": ("s", ACCENT, WHITE),
              "PR": ("^", SECOND, SECOND)}
    for i, r in enumerate(runs):
        if r["l1"] is None:
            # one tick per run without a GCC log; the legend says "no log" once
            top.plot([i], [7.5], "|", ms=18, mew=1.6, color=FAINT, zorder=2)
            continue
        mk, ec, fc = marker[r["kind"]]
        top.plot([i], [r["l1"]], mk, ms=10, mec=ec, mfc=fc, mew=1.8, zorder=3, clip_on=False)
        if any(l1_ > 0 for _, l1_ in r["earlier"]):
            top.plot([i], [r["l1"]], "o", ms=19, mec=WARNC, mfc="none", mew=1.8, zorder=2,
                     clip_on=False)
    # a PR point is labelled "PR #N": N from pull/N/merge, or from its branch in the pulls snapshot
    def point_label(r):
        if r["kind"] != "PR":
            return r["sha"]
        no = pr_number(r)
        if no is None:
            die(f"fig_q4: PR run {r['id']} on {r['ref']}: no PR in the pulls snapshot has that branch "
                f"-- cannot label its point")
        return f"PR #{no}"

    labels = {}
    # value labels where the count changes (and at the first run), in data units: above every
    # marker under the label, and a label that would overprint one already placed moves up a row
    pitch_in = 0.845 * W / max(n, 1)                 # inches per run on the top axes
    lab_w = 8 * 0.6 * 11.5 / 72 / pitch_in + 0.4     # an 8-character monospace label, in runs
    placed, prev, y_max = [], None, 15.0
    for i, r in enumerate(runs):
        if r["l1"] is None:
            continue
        if prev is None or r["l1"] != prev:
            left = prev is None or r["l1"] < prev    # a drop: the label runs right, over the lower runs
            x0_ = i - 0.3 if left else max(-0.3, i - lab_w / 2)
            # clear of every marker under the label's span
            y_ = max(v for j, v in pts if x0_ - 0.5 <= j <= x0_ + lab_w + 0.5) + 1.0
            while any(x0_ < px + lab_w and px < x0_ + lab_w and abs(y_ - py) < 1.6
                      for px, py in placed):
                y_ += 1.6
            placed.append((x0_, y_))
            y_max = max(y_max, y_)
            labels[r["id"]] = point_label(r)
            top.text(x0_ + (0 if left else lab_w / 2), y_, labels[r["id"]],
                     ha="left" if left else "center", va="bottom", fontsize=11.5,
                     color=INK, family="monospace")
        prev = r["l1"]
    top.set_xlim(-0.6, n - 0.4)
    top.set_ylim(-1.3, max(16.5, y_max + 1.9))
    top.set_yticks([0, 3, 6, 9, 12, 15])
    top.set_xticks([])
    top.grid(axis="y", color=RULE, lw=0.7)
    top.set_axisbelow(True)
    for s in ("top", "right", "bottom"):
        top.spines[s].set_visible(False)
    top.spines["left"].set_color(MUTED)
    top.tick_params(colors=MUTED, labelsize=12)
    top.set_ylabel("L1 problem groups", fontsize=13, color=MUTED, labelpad=8)
    # legend for the ref kinds
    hs = []
    for kind, lab in (("trunk", "trunk"), ("main", "main"), ("PR", "PR")):
        mk, ec, fc = marker[kind]
        hs.append(top.plot([], [], mk, ms=10, mec=ec, mfc=fc, mew=1.8, label=lab)[0])
    if any(r["l1"] is None for r in runs):
        hs.append(top.plot([], [], "|", ms=14, mew=1.6, color=FAINT, label="no log")[0])
    if any(any(l1_ > 0 for _, l1_ in r["earlier"]) for r in runs):
        hs.append(top.plot([], [], "o", ms=14, mec=WARNC, mfc="none", mew=1.8,
                           label="red on an earlier attempt")[0])
    top.legend(handles=hs, loc="upper right", bbox_to_anchor=(1.0, 1.36), ncol=len(hs), frameon=False,
               fontsize=12, handletextpad=0.3, columnspacing=1.2)
    # job strip
    col = {"failure": WARNC, "success": GREEN}
    for i, r in enumerate(runs):
        for k, (key, _) in enumerate(JOBS):
            y = 3 - k
            if r["jobs"]:
                bot.add_patch(Rectangle((i - 0.4, y - 0.38), 0.8, 0.76,
                                        facecolor=col[r["jobs"][key]], edgecolor="none"))
            else:
                bot.add_patch(Rectangle((i - 0.4, y - 0.38), 0.8, 0.76, facecolor=WHITE,
                                        edgecolor=GREY, lw=1.0))
    bot.set_xlim(-0.6, n - 0.4)
    bot.set_ylim(-0.6, 3.6)
    bot.set_yticks([3, 2, 1, 0])
    bot.set_yticklabels(["GCC + L1", "clang", "TSan", "ASan+UBSan"], fontsize=12, color=INK)
    bot.set_xticks([])
    for s in ("top", "right", "bottom", "left"):
        bot.spines[s].set_visible(False)
    bot.tick_params(axis="y", length=0)
    bot.set_xlabel("CI runs in order", fontsize=13, color=MUTED, labelpad=6)
    # strip legend
    lx = 0.66
    for c, lab, edge in ((WARNC, "failure", WARNC), (GREEN, "success", GREEN),
                         (WHITE, "no record", GREY)):
        fig.patches.append(Rectangle((lx, 0.028), 0.012, 0.028, transform=fig.transFigure,
                                     facecolor=c, edgecolor=edge, lw=1.0))
        fig.text(lx + 0.017, 0.042, lab, fontsize=12, color=MUTED, va="center")
        lx += 0.017 + 0.0075 * len(lab) + 0.03
    fig.text(0.045, 0.93, "CI: L1 problem groups per run", fontsize=22, fontweight="bold",
             color=INK, ha="left", va="center")
    fig.text(0.045, 0.042, f"as of {STATE_AT.replace('T', ' ')} UTC · trunk {STATE}", fontsize=11,
             color=FAINT, ha="left", va="center")
    save(fig, "fig_q4_ci_state")
    return dict(runs=runs, pats=pats, labels=labels)


# =================================================================== fig_q5
def fig_q5():
    cl = git("show", f"{RULE_AT}:CLAUDE.md")
    for n_ in ("**NDTwin-Kernel-P4 的 main 只經 PR＋squash merge 更新**（Adam 2026-09-27）",
               "PR 只開在 `Adam010341/NDTwin-Kernel-P4`；`ndtwin-lab/NDTwin-Kernel-P4`",
               "的 main 跟著同步：每次 squash 完，把同一顆 main 快轉推過去（Adam 2026-09-28，",
               "審核流程（判官、收件、裁決、報告）只在 trunk 與功能分支上進行。",
               "不再 `git push … trunk:main`", "排除 `doc/audit/**/*.md` 與各處 `REPORT*.md`"):
        if n_ not in cl:
            die(f"CLAUDE.md at {RULE_AT} lacks {n_!r}")
    codes = api_codes()
    heads = {}
    for org in ("ndtwin-lab", "Adam010341"):
        for br in ("main", "trunk"):
            url = f"https://api.github.com/repos/{org}/NDTwin-Kernel-P4/branches/{br}"
            if codes.get(url) != 200:
                die(f"{url} was not HTTP 200")
            d = api_json(f"branch_{org}_{br}.json", need=("name", "commit.sha:str"))
            if d.get("name") != br:
                die(f"branch_{org}_{br}.json is not branch {br}")
            heads[(org, br)] = d["commit"]["sha"][:8]
    if heads[("ndtwin-lab", "main")] != heads[("Adam010341", "main")]:
        die(f"ndtwin-lab main is {heads[('ndtwin-lab', 'main')]}, not Adam010341 main "
            f"{heads[('Adam010341', 'main')]} -- the rule says it follows")
    if heads[("ndtwin-lab", "trunk")] != heads[("Adam010341", "trunk")]:
        die("the two public trunks differ")
    if heads[("ndtwin-lab", "trunk")] != STATE:
        die(f"the public trunk is {heads[('ndtwin-lab', 'trunk')]}, not {STATE} -- refetch _net "
            f"and bump STATE")
    am = heads[("Adam010341", "main")]
    # Adam010341 main since the freeze: a first-parent chain of single-parent squash commits
    # "<subject> (#N)" back to f186ce98; each one carries exactly its PR branch's patch (from
    # the branch's merge base), no doc/audit/**/*.md or REPORT*.md, and the PR snapshot says
    # #N merged as it
    pulls = api_json("pulls_Adam010341.json", each=("", ["number", "state", "merged_at",
                                                         "merge_commit_sha", "head.sha:str",
                                                         "base.ref"]))
    pu = "https://api.github.com/repos/Adam010341/NDTwin-Kernel-P4/pulls?state=all&per_page=30"
    if codes.get(pu) != 200:
        die("pulls snapshot is not HTTP 200")
    byno = {str(p_["number"]): p_ for p_ in pulls}
    squashes, c, nfiles = [], am, 0
    while c[:8] != "f186ce98":
        info = git("log", "-1", "--format=%P%n%s%n%T", c).splitlines()
        parents, subject, tree = info[0].split(), info[1], info[2]
        m = re.search(r"\(#(\d+)\)$", subject)
        if len(squashes) > 20:
            die(f"squash chain from {am}: {len(squashes)} commits and f186ce98 not reached "
                f"(bound 20); at {c[:8]}")
        if len(parents) != 1 or not m:
            die(f"{c}: parents {parents}, subject {subject!r} -- not a squash chain to f186ce98")
        no = m.group(1)
        pr_ = byno.get(no)
        if not pr_ or pr_["merged_at"] is None or str(pr_["merge_commit_sha"])[:8] != c[:8]:
            die(f"PR #{no} in the snapshot is not merged as {c[:8]}")
        head_sha = pr_["head"]["sha"]
        base = git("merge-base", parents[0], head_sha).strip()
        if git("diff", base, head_sha) != git("diff", parents[0], c):
            die(f"{c[:8]} does not carry exactly PR #{no}'s patch")
        del tree
        files = git("diff", "--name-only", parents[0], c).split()
        excl = [f for f in files if re.match(r"doc/audit/.*\.md$", f) or
                re.search(r"REPORT[^/]*\.md$", f)]
        if excl:
            die(f"PR #{no} carries excluded files: {excl}")
        squashes.append((no, c[:8], len(files)))
        nfiles += len(files)
        c = parents[0]
    squashes.reverse()
    if not squashes or squashes[0][0] != "6":
        die(f"squash chain: {squashes}")
    pr_no = squashes[-1][0]
    must(os.path.join(I26, "ci-compare-pr6-48e8005d.txt"), "=> prediction met.",
         "prediction met on both runs")
    print(f"[q5] heads {heads}; main {am}: squash chain from f186ce98 {squashes}")
    opened = sorted((p_["number"] for p_ in pulls if p_["state"] == "open" and
                     p_["base"]["ref"] == "main"), key=int)
    print(f"[q5] open PRs into main at snapshot time: {opened}")

    H = 6.1
    fig, ax = canvas(H)
    txt(ax, 0.45, 0.48, "main moves only by squash-merged PR", size=22, weight="bold", ha="left")
    # right: the two public repos, each with its trunk and main
    rx, rw = 8.75, 4.15
    panels = {"ndtwin-lab": 1.0, "Adam010341": 3.45}
    cells = {}
    for org, y in panels.items():
        box(ax, rx, y, rw, 2.02, fill=PANEL, edge=RULE, lw=1.0, r=0.08, z=1)
        txt(ax, rx + 0.2, y + 0.3, f"{org}/NDTwin-Kernel-P4", size=12, color=FAINT, weight="bold",
            ha="left")
        for k, br in enumerate(("trunk", "main")):
            cy = y + 0.62 + k * 0.68
            frozen = False      # 09-28: ndtwin-lab main follows main (no frozen cell any more)
            box(ax, rx + 0.2, cy, rw - 0.4, 0.56, fill=WHITE, edge=GREY if frozen else INK,
                lw=1.2, ls=(0, (4, 3)) if frozen else "solid")
            txt(ax, rx + 0.4, cy + 0.28, br, size=13.5, weight="bold",
                color=FAINT if frozen else INK, ha="left", va="center_baseline")
            txt(ax, rx + 1.3, cy + 0.28, heads[(org, br)], size=13, mono=True,
                color=FAINT if frozen else BODY, ha="left", va="center_baseline")
            if org == "ndtwin-lab" and br == "main":
                txt(ax, rx + rw - 0.4, cy + 0.28, "follows", size=12.5, color=GREEN,
                    ha="right", weight="bold", va="center_baseline")
            if frozen:
                txt(ax, rx + rw - 0.4, cy + 0.28, "frozen", size=12.5, color=FAINT, ha="right",
                    weight="bold", va="center_baseline")
            if org == "Adam010341" and br == "main":
                # the numbers, not the merge order (#16 was squashed before #15)
                nos = sorted(int(q[0]) for q in squashes)
                lab = f"#{nos[0]}–#{nos[-1]}" if nos == list(range(nos[0], nos[-1] + 1)) \
                    and len(nos) > 3 else " ".join(f"#{n_}" for n_ in nos)
                txt(ax, rx + rw - 0.4, cy + 0.28, lab, size=13, color=GREEN, ha="right",
                    weight="bold", va="center_baseline")
            cells[(org, br)] = (rx + 0.2, cy + 0.28)
    # left: trunk, where review happens
    tx, ty, tw, th = 0.45, 1.25, 2.55, 1.6
    box(ax, tx, ty, tw, th, fill=ACCENT_BG, edge=ACCENT, lw=2.2)
    txt(ax, tx + tw / 2, ty + 0.45, "trunk", size=16, weight="bold", color=ACCENT)
    txt(ax, tx + tw / 2, ty + 1.02, "judge · intake\nrulings", size=12, color=MUTED)
    # push: one line from trunk to a bus beside the panels, one stub into each trunk cell
    bus = rx - 0.38
    (n_x, n_y), (a_x, a_y) = cells[("ndtwin-lab", "trunk")], cells[("Adam010341", "trunk")]
    ax.plot([tx + tw + 0.02, bus], [n_y, n_y], color=INK, lw=1.4, zorder=3)
    ax.plot([bus, bus], [n_y, a_y], color=INK, lw=1.4, zorder=3)
    arrow(ax, bus, n_y, n_x - 0.02, n_y)
    arrow(ax, bus, a_y, a_x - 0.02, a_y)
    txt(ax, (tx + tw + bus) / 2, n_y - 0.2, "push", size=12.5, color=INK)
    # the stopped path: trunk:main ends at a cross, short of ndtwin-lab main
    f_y = cells[("ndtwin-lab", "main")][1]
    x_end = bus - 0.55
    ax.plot([tx + tw + 0.02, x_end - 0.22], [f_y, f_y], color=GREY, lw=1.4, ls=(0, (4, 3)),
            zorder=3)
    txt(ax, x_end, f_y, "×", size=24, color=WARNC, weight="bold")
    txt(ax, (tx + tw + x_end) / 2, f_y + 0.25, "trunk:main", size=12, color=FAINT, mono=True)
    # the PR path: trunk -> PR branch -> PR -> squash merge -> Adam010341 main
    m_y = cells[("Adam010341", "main")][1]
    steps = [(0.45, 2.55, "PR branch", "− doc/audit/**/*.md\n− REPORT*.md", True),
             (3.4, 2.05, "PR", "CI on the PR", False),
             (5.85, 2.05, "squash merge", "one commit", False)]
    for x, w_, a, b, mono in steps:
        box(ax, x, m_y - 0.62, w_, 1.3, edge=INK, lw=1.3)
        txt(ax, x + w_ / 2, m_y - 0.25, a, size=14, weight="bold")
        txt(ax, x + w_ / 2, m_y + 0.25, b, size=11.5, color=MUTED, mono=mono)
    if opened:
        txt(ax, 3.4 + 2.05 / 2, m_y + 0.95, " · ".join(f"#{n_}" for n_ in opened) + " open",
            size=12, color=FAINT)
    arrow(ax, tx + tw / 2, ty + th + 0.02, tx + tw / 2, m_y - 0.64)
    arrow(ax, 0.45 + 2.55 + 0.02, m_y, 3.4 - 0.02, m_y)
    arrow(ax, 3.4 + 2.05 + 0.02, m_y, 5.85 - 0.02, m_y)
    arrow(ax, 5.85 + 2.05 + 0.02, m_y, cells[("Adam010341", "main")][0] - 0.02, m_y,
          color=GREEN, lw=1.8)
    txt(ax, W - 0.45, 0.52, f"as of {STATE_AT.replace('T', ' ')} UTC · public API, unauthenticated",
        size=11, color=FAINT, ha="right")
    save(fig, "fig_q5_main_by_pr")
    return dict(heads={f"{o}/{b}": v for (o, b), v in heads.items()}, am=am, pr=pr_no,
                squashes=squashes, open=opened)


def main():
    q1 = fig_q1()
    q2 = fig_q2()
    q3 = fig_q3()
    q4 = fig_q4()
    q5 = fig_q5()
    print("[summary]", json.dumps(dict(q1=q1, q2={k: v for k, v in q2.items() if k != "per_file"},
                                       q3=q3, q5=q5), default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
