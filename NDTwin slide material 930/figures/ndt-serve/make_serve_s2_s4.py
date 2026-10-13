#!/usr/bin/env python3
"""
make_serve_s2_s4.py -- three more `ndt serve` figures for the 2026-09-30 report (fig_s1, the
request path, is make_serve_diagram.py's and is not touched here).

    fig_s2_security_model   threat -> defense: READ THE CODE (trunk) beside RAN IT (09-24 live);
                            the final state only (template v1.8, 2026-09-29 UTC): under someone
                            else's claim `up` is refused by ndt on both planes in the code, P4
                            also live (rc 5); OVS is "not run live" -- its only live record
                            predates the OVS guard merge 68ace017 and stays in the .md, not on
                            the canvas
    fig_s3_cells_and_walks  the guided walk's steps (READ, cells.py) above what the two 09-24
                            walks showed, assertion by assertion (RAN IT)
    fig_s4_gui_plan         where the page goes: v1 merged 09-27 -> v2 ruled 09-27 -> one app
                            with Web-GUI (not scheduled)

Data, all read at run time (nothing measured is hand-typed):
  * code: tools/ndt_serve/{serve.py,cells.py}, tools/test_workflow/ndt in the NDTwin-Kernel
    checkout; every file:line the .md files cite is asserted below (a moved line fails the run).
    tools/ndt_serve must equal the GUI v1 merge f186ce98 and the working tree must equal HEAD.
  * live (09-24, uncommitted observations under scratch/overnight-2026-09-05/logs/ndt-serve-0924/):
    live-20260924T2201/ (api/03, 04, 10), live-fixes-20260924T2249/ (01-listen-and-token.txt,
    b/03, b/04, b/14, a/summary.json + a/18, a2/summary.json + a2/01 + knob diffs),
    live-cells-20260924T2224/walk-*/ (the last GET of each walk);
    the recorded verdicts: logs/orchestrator-0924/intake-0926/walks/<walk id>.json.
  * rulings: logs/orchestrator-0924/intake-0926/RULINGS-0927-ndtserve-gui-{v2,scope}.md;
    Web-GUI's own docker-compose.yml and package.json (~/Web-GUI, read only);
    git refs (read only) for the merge dates and for how far v2 is (no branch = "not started";
    a v2 branch touching only doc/ = "scope draft only"; other files but no page files = "on a
    branch, no page yet"; page files (static/, package.json, vite/tailwind config, .ts/.tsx) stop
    the run).  fig_s4 was replaced in the deck by a table on 2026-09-27 UTC (judge F-13).

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/ndt-serve"
    nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_serve_s2_s4.py [--only fig_s2_security_model ...]
`--only` draws just the named figures (code_facts, live_facts and walks are checked in full
either way); without it, all three are drawn.
"""
import argparse
import datetime
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
plt.rcParams["hatch.linewidth"] = 1.3

REPO = os.environ.get("NDTWIN_REPO", "/home/adam/Desktop/NDTwin-Kernel")
WEBGUI = os.environ.get("WEBGUI_REPO", os.path.expanduser("~/Web-GUI"))
SERVE = os.path.join(REPO, "tools/ndt_serve/serve.py")
CELLS = os.path.join(REPO, "tools/ndt_serve/cells.py")
APPJS = os.path.join(REPO, "tools/ndt_serve/static/app.js")
NDT = os.path.join(REPO, "tools/test_workflow/ndt")
LOGS = os.path.join(REPO, "scratch/overnight-2026-09-05/logs")
LIVE = os.path.join(LOGS, "ndt-serve-0924")
FIRST = os.path.join(LIVE, "live-20260924T2201")
FIX = os.path.join(LIVE, "live-fixes-20260924T2249")
CELLRUN = os.path.join(LIVE, "live-cells-20260924T2224")
INTAKE = os.path.join(LOGS, "orchestrator-0924/intake-0926")
RUL_V2 = os.path.join(INTAKE, "RULINGS-0927-ndtserve-gui-v2.md")
RUL_SCOPE = os.path.join(INTAKE, "RULINGS-0927-ndtserve-gui-scope.md")
VERDICTS = os.path.join(INTAKE, "walks")

GUI_V1 = "f186ce98"      # Merge feat/ndt-serve-gui-0927 (GUI v1)
API_MERGE = "48209682"   # Merge feat/ndt-serve-0924 (API + cells + walks)
OVS_GUARD = "68ace017"   # Merge fix/ndt-ovs-claim-0925 (ndt up refuses a foreign claim on OVS)

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
WARNC, WARN_BG, WHITE = "#9C3B2E", "#FBF2F0", "#FFFFFF"
GREEN, AMBER, GREY = "#2F7D4F", "#E3A21A", "#C9CDD0"
W = 13.33
UTC = datetime.timezone.utc   # every date on the canvases and in the .md files is UTC (judge F-18)


def die(msg):
    raise SystemExit(f"make_serve_s2_s4: {msg}")


def text(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError as e:
        die(f"cannot read {path}: {e}")


def jload(path):
    try:
        return json.loads(text(path))
    except ValueError as e:
        die(f"{path} is not JSON: {e}")


def must(path, *needles):
    t = text(path)
    for n in needles:
        if n not in t:
            die(f"{path} no longer contains {n!r}")


def at_lines(path, table):
    """Each (line number, needle): the needle is on exactly that line -- the .md cites it there."""
    lines = text(path).splitlines()
    for n, needle in table:
        if n > len(lines) or needle not in lines[n - 1]:
            die(f"{os.path.relpath(path, REPO)}:{n} no longer holds {needle!r}")


def git(*args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    r = subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True, env=env)
    return r.returncode, r.stdout


def commit_day(sha):
    rc, out = git("log", "-1", "--format=%cI", sha)
    if rc:
        die(f"no commit {sha}")
    return datetime.datetime.fromisoformat(out.strip()).astimezone(UTC)


def md(d):
    return d.strftime("%m-%d")


# ------------------------------------------------------------------------------ the code (READ)
SERVE_LINES = [
    (72, 'BIND = "127.0.0.1"'), (73, 'TOKEN_HEADER = "X-NDT-Token"'), (94, "NONCE_TTL_S = "),
    (95, "MAX_NONCES = 8"), (188, 'return "http://%s:%d/#k=%s"'), (209, "def take(self, key):"),
    (359, "class DryRun(Exception):"), (376, "def confirm_policy("), (395, "SLOT = threading.Lock()"),
    (406, "Access-Control-*"), (453, "if path in STATIC:"),
    (463, "route is not Handler.r_health"), (477, "def _check_host(self):"),
    (484, "def _check_token(self):"), (490, "def _check_origin(self):"),
    (496, "def _check_read(self):"), (501, "def _check_write(self):"),
    (601, "def w_session(self, query):"), (608, 'if origin != "http://" + self.headers["Host"]'),
    (614, "if not self.cfg.nonces.take(key):"), (690, "def w_app(self, query, name, action):"),
    (696, "precheck=self._require_own_claim)"), (703, "def _spawn("),
    (709, "raise DryRun(kind, argv)"), (710, "with SLOT:"),
    (713, '"one state-changing job at a time"'),
    (785, 'precheck=self._require_own_claim if cell["requires"] != "none"'),
    (787, "def _require_own_claim(self):"), (809, 'if not OWN_CLAIM.fullmatch(line or ""):'),
    (956, '{"minutes": 30'), (1031, 'OWN_CLAIM = re.compile(r"yours -- [0-9]+m left'),
    (1118, "DRY_RUN_OK = {"), (1163, 'ap.add_argument("--port", type=int, default=8765'),
    (1214, "httpd = Server((BIND, a.port), Handler)"),
]
NDT_LINES = [(996, "guard_up_lab_free() {"), (3313, 'guard_up_lab_free "$up_what"'),
             (4362, 'guard_up_lab_free "ovs $ovs_hosts"'),
             (5799, "printf 'yours -- %dm left (until %s)\\n'")]
CELLS_LINES = [(293, "STEP_TITLES = {"), (305, "def guided_steps(cell):"),
               (307, 'steps = ["old"] + (["new"] if cell.get("new") else []) + '
                     '(["status", "claim"] if lab else [])'),
               (308, '+ ["run"] + (["release"] if lab else []) + ["compare", "verdict"]')]


def code_facts():
    rc, head = git("rev-parse", "HEAD")
    if rc:
        die("cannot read HEAD")
    head = head.strip()
    rc, _ = git("diff", "--quiet", "HEAD", "--", "tools/ndt_serve", "tools/test_workflow/ndt")
    if rc:
        die("tools/ndt_serve or tools/test_workflow/ndt differs from HEAD in the working tree")
    rc, _ = git("diff", "--quiet", GUI_V1, "HEAD", "--", "tools/ndt_serve")
    if rc:
        die(f"tools/ndt_serve at HEAD is no longer the GUI v1 merge {GUI_V1}: re-read the code")
    at_lines(SERVE, SERVE_LINES)
    at_lines(NDT, NDT_LINES)
    at_lines(CELLS, CELLS_LINES)
    # fig_s2's READ cell "P4 and OVS": the OVS call of the shared guard (ndt:4362, asserted above)
    # came in with OVS_GUARD, and HEAD -- the tree read here -- contains it.
    # [Co-developed with claude code -- Adam]
    rc, _ = git("merge-base", "--is-ancestor", OVS_GUARD, "HEAD")
    if rc == 1:
        die(f"the OVS guard merge {OVS_GUARD} is not in HEAD: the READ cell 'P4 and OVS' has no "
            f"code behind it")
    if rc:
        die(f"git cannot place {OVS_GUARD} against HEAD (rc {rc})")
    rc, diff = git("diff", f"{OVS_GUARD}^1", OVS_GUARD, "--", "tools/test_workflow/ndt")
    if rc or not re.search(r'^\+\s*guard_up_lab_free "ovs \$ovs_hosts"', diff, re.M):
        die(f"{OVS_GUARD} did not add the OVS call of guard_up_lab_free: the notes and the .md "
            f"name the wrong commit for 'OVS refused in the code'")
    src = text(SERVE)
    bind = re.search(r'^BIND = "([0-9.]+)"', src, re.M).group(1)
    ttl = int(re.search(r"^NONCE_TTL_S = (\d+)", src, re.M).group(1))
    claim_min = int(re.search(r'\{"minutes": (\d+), "note": "guided walk', src).group(1))
    print(f"[code] HEAD {head[:8]}  BIND {bind}  nonce ttl {ttl} s  walk claim {claim_min} min")
    return {"head": head, "bind": bind, "ttl": ttl, "claim_min": claim_min}


# ------------------------------------------------------------------------ the live raw (RAN IT)
def http_file(path):
    """One saved exchange: '# <name> sent ...', the request, a blank line, the response."""
    t = text(path)
    req, sep, resp = t.partition("\nHTTP/1.")
    if not sep:
        die(f"{path}: no response line")
    status = int(resp.split()[1])
    rlines = req.splitlines()[1:]
    headers = {}
    for line in rlines[1:]:
        if not line.strip():
            break
        k, _, v = line.partition(":")
        headers[k.strip().lower()] = v.strip()
    i = resp.find("{")
    body = json.loads(resp[i:]) if i >= 0 else None
    return {"req": rlines[0], "headers": headers, "status": status, "body": body}


def step_of(summary_path, name):
    hits = [s for s in jload(summary_path) if s.get("step") == name]
    if len(hits) != 1:
        die(f"{summary_path}: {len(hits)} steps named {name!r}")
    return hits[0]


def live_facts():
    obs = {}
    # which code and which ndt the 09-24 runs stood on
    fb = text(os.path.join(FIX, "00-before.txt"))
    m = re.search(r"^branch HEAD ([0-9a-f]{40})$", fb, re.M)
    ndt_sum = re.search(r"^([0-9a-f]{64})  \S+/tools/test_workflow/ndt$", fb, re.M)
    first = text(os.path.join(FIRST, "00-before.txt")).splitlines()
    if not (m and ndt_sum and re.fullmatch(r"[0-9a-f]{40}", first[1]) and
            any(ln.startswith(ndt_sum.group(1)) for ln in first)):
        die("00-before.txt of the two 09-24 runs no longer name their code head and ndt sha256")
    obs["code_fix"], obs["code_first"], obs["ndt256"] = m.group(1), first[1], ndt_sum.group(1)

    # 1. one listener, on loopback
    lt = text(os.path.join(FIX, "01-listen-and-token.txt"))
    hdr = re.search(r"ss -ltnpH 'sport = :(\d+)'", lt)
    listens = [ln.split() for ln in lt.splitlines() if ln.startswith("LISTEN")]
    if not hdr or len(listens) != 1 or not listens[0][3].startswith("127.0.0.1:") \
            or listens[0][3] != "127.0.0.1:" + hdr.group(1):
        die("01-listen-and-token.txt: not exactly one LISTEN line, on 127.0.0.1:<port>")
    obs["listen"] = listens[0][3]
    # the day of the two runs, in UTC, from their own first lines
    days = set()
    for p in (os.path.join(FIX, "01-listen-and-token.txt"), os.path.join(FIRST, "00-before.txt")):
        m = re.search(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2})", text(p).splitlines()[0])
        if not m:
            die(f"{p}: first line has no timestamp")
        days.add(datetime.datetime.fromisoformat(m.group(1)).astimezone(UTC).date())
    if len(days) != 1:
        die(f"the 09-24 runs are on different UTC days: {days}")
    obs["day"] = days.pop()
    port = hdr.group(1)

    # 2. a foreign Host header -> 403 host (both runs)
    for p in (os.path.join(FIRST, "api/04-probe-foreign-host.http"),
              os.path.join(FIX, "b/04-probe-foreign-host.http")):
        h = http_file(p)
        if h["headers"].get("host") in ("127.0.0.1:" + port, "localhost:" + port) or \
                h["status"] != 403 or h["body"].get("error") != "host":
            die(f"{p}: not a foreign Host answered 403 host")
        obs["host"] = (h["status"], h["body"]["error"], h["headers"]["host"])

    # 3. no token -> 403 token (a write and two reads, one of them the lock-probing check=1)
    for p in (os.path.join(FIRST, "api/03-probe-no-token.http"),
              os.path.join(FIX, "b/03-probe-no-token.http"),
              os.path.join(FIX, "b/14-probe-check-no-token.http")):
        h = http_file(p)
        if "x-ndt-token" in h["headers"] or h["status"] != 403 or \
                h["body"].get("error") != "token":
            die(f"{p}: not a token-less request answered 403 token")
        obs["token"] = (h["status"], h["body"]["error"])

    # 6. a second write while `up` runs -> 409 busy
    h = http_file(os.path.join(FIRST, "api/10-probe-busy-while-up.http"))
    if "x-ndt-token" not in h["headers"] or h["status"] != 409 or \
            h["body"].get("error") != "busy" or h["body"]["job"]["kind"] != "up" or \
            h["body"]["job"]["state"] != "running":
        die("api/10-probe-busy-while-up.http: not 409 busy naming the running up")
    obs["busy"] = (h["status"], h["body"]["error"])

    # 7. `up` under somebody else's claim, both planes
    for plane, d, status_http, step, argv_tail in (
            ("P4", "a2", "01-status-under-the-foreign-claim.http", "up-p4-under-a-foreign-claim",
             ["up", "p4"]),
            ("OVS", "a", "18-status-under-the-foreign-claim.http", "up-under-a-foreign-claim",
             ["up", "4"])):
        st = http_file(os.path.join(FIX, d, status_http))
        if not re.search(r"^  claim +ndt-serve-0924-foreign -- \d+m left", st["body"]["stdout"],
                         re.M):
            die(f"{d}/{status_http}: the claim row is not the foreign owner's")
        s = step_of(os.path.join(FIX, d, "summary.json"), step)
        if s["argv"][1:] != argv_tail:
            die(f"{d}: {step} ran {s['argv'][1:]}, not {argv_tail}")
        obs["up_" + plane] = (s["rc"], s["rc_class"], s["meaning"])
        obs["job_" + plane] = s.get("job")
    if obs["up_P4"][:2] != (5, "refused"):
        die(f"P4 up under a foreign claim: {obs['up_P4']}")
    if text(os.path.join(FIX, "a2/before-up.knob.diff")) != \
            text(os.path.join(FIX, "a2/after-up.knob.diff")):
        die("a2: the host-count knob moved across the refused up")
    if obs["up_OVS"][0] != 0 or not obs["up_OVS"][2].startswith("the fabric came up"):
        die(f"OVS up under a foreign claim: {obs['up_OVS']}")
    # fig_s2 draws OVS as "not run live" (template v1.8): the one OVS record above ran the ndt of
    # before the OVS guard merge, and no ndt serve live run of an OVS `up` under a foreign claim
    # exists after it.  [Co-developed with claude code -- Adam]
    fix_at = commit_day(OVS_GUARD)
    ovs_at = job_time(obs["job_OVS"], "a/summary.json")
    if ovs_at >= fix_at:
        die(f"the OVS up under a foreign claim ran at {ovs_at:%Y-%m-%dT%H:%M:%SZ}, not before the "
            f"OVS guard merge {OVS_GUARD} ({fix_at:%Y-%m-%dT%H:%M:%SZ}): it is evidence about the "
            f"fixed code -- draw it instead of 'not run live'")
    scanned, ovs_steps = 0, []
    for p in sorted(glob.glob(os.path.join(LIVE, "**", "summary.json"), recursive=True)):
        steps = jload(p)
        scanned += 1
        if not isinstance(steps, list):
            die(f"{os.path.relpath(p, LIVE)}: not a list of steps")
        for st in steps:
            argv = st.get("argv") or []
            if "foreign-claim" in str(st.get("step")) and argv[1:2] == ["up"] and \
                    argv[2:3] != ["p4"]:
                ovs_steps.append(st.get("job"))
                if job_time(st.get("job"), p) >= fix_at:
                    die(f"{os.path.relpath(p, LIVE)}: an OVS up under a foreign claim ran after "
                        f"the OVS guard merge {OVS_GUARD} (job {st.get('job')}): draw it instead "
                        f"of 'not run live'")
    obs["ovs_before_fix"] = (f"{ovs_at:%Y-%m-%dT%H:%M:%SZ}", f"{fix_at:%Y-%m-%dT%H:%M:%SZ}",
                             f"{scanned} summaries scanned, OVS foreign-claim ups {ovs_steps}")
    dirty = set()
    for p in (os.path.join(FIX, "a2/01-status-under-the-foreign-claim.http"),
              os.path.join(FIX, "a/18-status-under-the-foreign-claim.http")):
        dirty.add(dirty_line(http_file(p)["body"]["stdout"], p))
    dirty.add(dirty_line(text(os.path.join(FIRST, "99-after.txt")), "live-20260924T2201/99-after.txt"))
    if len(dirty) != 1:
        die(f"the 09-24 runs' ndt checkout differs between runs: {dirty}")
    obs["dirty"] = dirty.pop()
    for k, v in obs.items():
        print(f"[live 09-24] {k:12s} {v}")
    return obs


def job_time(job, where):
    """UTC start of an ndt serve job, from its id `<YYYYMMDD>T<HHMMSS>Z-<hex>` (time.gmtime();
    tools/ndt_serve/jobs.py:88 names jobs that way).  [Co-developed with claude code -- Adam]"""
    m = re.fullmatch(r"(\d{8}T\d{6})Z-[0-9a-f]+", str(job))
    if not m:
        die(f"{where}: job id {job!r} carries no UTC start time")
    return datetime.datetime.strptime(m.group(1), "%Y%m%dT%H%M%S").replace(tzinfo=UTC)


def dirty_line(status_out, where):
    """`ndt status`'s code row: `code  <sha8>  +N file(s) with uncommitted changes` and the
    files it names as able to change behaviour."""
    m = re.search(r"^  code +([0-9a-f]{8})  \+(\d+) file\(s\) with uncommitted changes\n"
                  r" +(\d+) of them can change behaviour:\n((?: {10,}\S+\n)+)", status_out, re.M)
    if not m:
        die(f"{where}: no dirty-checkout code row")
    return (m.group(1), int(m.group(2)), int(m.group(3)), tuple(m.group(4).split()))


# ---------------------------------------------------------------------------------- drawing
def rbox(ax, x, y, w, h, fill, edge, lw=1.0, ls="solid", hatch=None, inset=0.07, r=0.05, z=2):
    ax.add_patch(FancyBboxPatch((x + inset, y + inset), w - 2 * inset, h - 2 * inset,
                                boxstyle=f"round,pad=0.02,rounding_size={r}", facecolor=fill,
                                edgecolor=edge, linewidth=lw, linestyle=ls, hatch=hatch,
                                zorder=z))


def txt(ax, x, y, s, size=13, color=INK, weight="normal", ha="center", va=None, mono=False,
        z=6, ls=1.25):
    # one-line labels sit on a common baseline whatever their letters; multi-line ones centre
    va = va or ("center" if "\n" in s else "center_baseline")
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, zorder=z,
            family="monospace" if mono else None, linespacing=ls)


def arrow(ax, x0, y0, x1, y1, color=INK, lw=1.5, ls="solid", z=3):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=14,
                                 color=color, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0, zorder=z))


def canvas(h):
    fig = plt.figure(figsize=(W, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(h, 0)
    ax.axis("off")
    return fig, ax


def title(ax, s):
    if len(s) > 45:
        die(f"title longer than 45 characters: {s!r}")
    txt(ax, 0.45, 0.48, s, size=22, weight="bold", ha="left")


def save(fig, stem):
    os.makedirs(HIRES, exist_ok=True)
    for ext in ("pdf", "png", "svg"):
        kw = {"dpi": 300} if ext == "png" else {}
        fig.savefig(os.path.join(OUTDIR, f"{stem}.{ext}"), facecolor=WHITE, **kw)
    fig.savefig(os.path.join(HIRES, f"{stem}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"[out] {stem}")


def legend_item(ax, x, y, fill, edge, label, ls="solid", hatch=None, w=0.42, h=0.26):
    ax.add_patch(Rectangle((x, y - h / 2), w, h, facecolor=fill, edgecolor=edge, lw=1.1,
                           linestyle=ls, hatch=hatch, zorder=4))
    txt(ax, x + w + 0.12, y, label, size=12, color=MUTED, ha="left")


# ------------------------------------------------------------------------ fig_s2_security_model
def fig_s2(code, obs):
    # template v1.8 (2026-09-29 UTC): the final state only. The up/down row reads the code at HEAD
    # (P4 and OVS, code_facts) beside what ran live (P4 rc 5; OVS not run live since the fix,
    # live_facts). The pre-fix OVS record is in the .md, not on the canvas.
    H = 7.0
    fig, ax = canvas(H)
    title(ax, "ndt serve: threats and defenses")
    lx, rx, rw = 4.10, 4.10, 4.40          # label column right edge; READ column
    ox, ow = 8.95, 3.95                     # RAN IT column
    top, rh = 1.42, 0.62
    txt(ax, lx - 0.2, 1.06, "threat", size=13, color=MUTED, ha="right")
    txt(ax, rx + 0.07, 1.06, "READ THE CODE", size=12, color=FAINT, weight="bold", ha="left")
    txt(ax, ox + 0.07, 1.06, f"RAN IT · live {md(obs['day'])} (UTC)", size=12, color=FAINT,
        weight="bold", ha="left")
    ax.plot([ox - 0.22, ox - 0.22], [0.86, top + 8 * rh], color=RULE, lw=1.5)

    s_host, s_tok, s_busy = obs["host"], obs["token"], obs["busy"]
    rows = [
        ("another machine", f"bind {code['bind']} only",
         ("ok", obs["listen"], "1 listener")),
        ("a page rebinding DNS", "Host header must be ours",
         ("ok", str(s_host[0]), f'"{s_host[1]}"')),
        ("a page forging a call", "token on every call\nown Origin · no CORS",
         ("ok", str(s_tok[0]), f'"{s_tok[1]}"')),
        ("a leaked page link", f"one-time key · {code['ttl']} s · one use", None),
        ("a surprise command", "preview: the exact ndt argv", None),
        ("a second job mid-run", "one job at a time",
         ("ok", str(s_busy[0]), f'"{s_busy[1]}"')),
        ("someone else's claim: up/down", "ndt's own guard: rc 5\nP4 and OVS", "split"),
        ("someone else's claim: apps, cells", "server: claim must be yours", None),
    ]
    for i, (threat, defense, ran) in enumerate(rows):
        y = top + i * rh
        txt(ax, lx - 0.2, y + rh / 2, threat, size=13.5, ha="right")
        rbox(ax, rx, y, rw, rh, PANEL, RULE)
        txt(ax, rx + rw / 2, y + rh / 2, defense, size=12.5, color=BODY, ls=1.2)
        if ran is None:
            rbox(ax, ox, y, ow, rh, WHITE, GREY)
            txt(ax, ox + ow / 2, y + rh / 2, "not run live", size=12.5, color=FAINT)
        elif ran == "split":
            hw = ow / 2
            rc, cls, _m = obs["up_P4"]
            rbox(ax, ox, y, hw, rh, GREEN, GREEN)
            txt(ax, ox + hw / 2, y + rh / 2 - 0.11, f"P4  rc {rc}", size=13.5, color=WHITE,
                weight="bold")
            txt(ax, ox + hw / 2, y + rh / 2 + 0.12, cls, size=11, color=WHITE)
            rbox(ax, ox + hw, y, hw, rh, WHITE, GREY)
            txt(ax, ox + 1.5 * hw, y + rh / 2 - 0.11, "OVS", size=13.5, color=FAINT,
                weight="bold")
            txt(ax, ox + 1.5 * hw, y + rh / 2 + 0.12, "not run live", size=11, color=FAINT)
        else:
            _k, main, sub = ran
            rbox(ax, ox, y, ow, rh, GREEN, GREEN)
            txt(ax, ox + ow / 2, y + rh / 2 - 0.11, main, size=13.5, color=WHITE, weight="bold")
            txt(ax, ox + ow / 2, y + rh / 2 + 0.12, sub, size=11, color=WHITE)
    ly = top + 8 * rh + 0.36
    legend_item(ax, ox + 0.07, ly, GREEN, GREEN, "held")
    legend_item(ax, ox + 1.15, ly, WHITE, GREY, "not run live")
    save(fig, "fig_s2_security_model")


# ----------------------------------------------------------------------- fig_s3_cells_and_walks
WALK_DIRS = ("walk-help_drops_deleted_claims", "walk-up_target_names_a_readable_model")
REQUIRES_LABEL = {"none": "no lab", "ovs4": "lab · OVS 4 hosts"}


def cell_at(line, provenance=None):
    """The UTC date a CELL: line carries: at=<iso with offset>, or at=(replayed <date>) -- a
    date with no time, whose clock time only the fixture's PROVENANCE.md gives ("run <date> HH:..",
    +08): that is taken to UTC the same way."""
    m = re.search(r"\bat=(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2})", line)
    if m:
        return datetime.datetime.fromisoformat(m.group(1)).astimezone(UTC).date()
    m = re.search(r"\bat=\(replayed (\d{4}-\d{2}-\d{2})\)", line)
    pm = re.search(r"run (\d{4}-\d{2}-\d{2}) (\d{2}):\d", provenance or "")
    if not (m and pm and pm.group(1) == m.group(1)):
        die(f"no datable at= in {line!r}")
    local = datetime.datetime.fromisoformat(f"{pm.group(1)}T{pm.group(2)}:00:00+08:00")
    return local.astimezone(UTC).date()


def walks():
    code_steps = ["old", "new", "status", "claim", "run", "release", "compare", "verdict"]
    lab_only = {"status", "claim", "release"}
    before = text(os.path.join(CELLRUN, "00-before.txt")).splitlines()
    if not (re.fullmatch(r"[0-9a-f]{40}", before[1]) and
            re.match(r"[0-9a-f]{64}  \S+/tools/test_workflow/ndt$", before[2])):
        die("live-cells 00-before.txt no longer names the serve code head and ndt sha256")
    print(f"[walks] serve code {before[1][:8]}  ndt sha256 {before[2][:8]}")
    out = []
    for d in WALK_DIRS:
        files = sorted(glob.glob(os.path.join(CELLRUN, d, "*-GET-api_v1_guided_*.json")))
        if not files:
            die(f"{d}: no GET of the walk")
        raw = text(files[-1])
        if not raw.startswith("# GET ") or " -> 200 " not in raw.splitlines()[0]:
            die(f"{files[-1]}: not a 200 GET")
        w = json.loads(raw.split("\n", 1)[1])["walk"]
        steps = {s["step"]: s for s in w["steps"]}
        names = [s["step"] for s in w["steps"]]
        want = [s for s in code_steps if w["requires"] != "none" or s not in lab_only]
        if names != want:
            die(f"{d}: steps {names} are not cells.py's guided_steps {want}")
        if w["current"] != len(names) - 1 or steps["verdict"]["state"] != "pending":
            die(f"{d}: the walk did not stop at the verdict step")
        for s in names[:-1]:
            if steps[s]["state"] != "done":
                die(f"{d}: step {s} is {steps[s]['state']}")
        old_j, new_j = steps["old"]["result"]["judge"], steps["new"]["result"]["judge"]
        cmp_ = steps["compare"]["result"]
        run = steps["run"]["result"]
        rows = cmp_["rows"]
        ids = [r["id"] for r in rows]
        if [a["id"] for a in old_j["asserts"]] != ids or \
                sorted(a["id"] for a in new_j["asserts"]) != sorted(ids):
            die(f"{d}: old/new/compare do not name the same assertions")
        new_ok = {a["id"]: a["ok"] for a in new_j["asserts"]}
        old_ok = {a["id"]: a["ok"] for a in old_j["asserts"]}
        for r in rows:
            if (r["old"] == "ok") != old_ok[r["id"]]:
                die(f"{d}: compare's old column disagrees with old/ on {r['id']}")
        # which red rows on old/ carry the finding is the fixture's own PROVENANCE.md to say
        # (tests/fixtures/live_cells/README.md rule 2); the rest are the fixture's gaps
        failing = {r["id"] for r in rows if r["old"] == "FAIL"}
        prov = old_j["provenance"]
        pm = re.search(r"\*\*Assertions that carry the finding[^*]*\*\*[^:]*:\s*(.*?)(?:\n\n|\Z)",
                       prov, re.S)
        if pm:
            carriers = set(re.findall(r"`([a-z0-9_]+)`", pm.group(1)))
        elif "failing assertions carry the finding" in prov:
            carriers = set(failing)
        else:
            die(f"{d}: PROVENANCE.md names no carriers of the finding")
        gap = failing - carriers
        if not carriers <= failing:
            die(f"{d}: a named carrier is not red on old/")
        if gap:
            gm = re.search(r"\*\*Fixture gap[^*]*\*\*(.*?)(?:\n\n|\Z)", prov, re.S)
            if not gm or set(re.findall(r"`([a-z0-9_]+)`", gm.group(1))) & failing != gap:
                die(f"{d}: the fixture gap PROVENANCE.md names is not the non-carriers {gap}")
        r2g = [r["id"] for r in rows if r["old"] == "FAIL" and r["now"] == "ok"]
        if sorted(r2g) != sorted(cmp_["red_to_green"]) or cmp_["still_red"] or \
                any(r["now"] != "ok" for r in rows):
            die(f"{d}: red_to_green / still_red do not match the rows")
        if not old_j["failing_matches_expected"] or old_j["verdict"]["state"] != "FAIL" or \
                new_j["verdict"]["state"] != "PASS":
            die(f"{d}: old/ is not the expected FAIL or new/ is not PASS")
        if run["state"] != "finished" or run["rc"] != 0 or run["rc_class"] != "pass" or \
                run["cell_verdict"]["state"] != "PASS":
            die(f"{d}: the run is not a finished PASS")
        ndt = re.search(r"\bndt=([0-9a-f]{40})\b", run["cell_verdict"]["line"]).group(1)
        kern = re.search(r"\bkernel=([0-9a-f]{16})\b", run["cell_verdict"]["line"]).group(1)
        if w["requires"] != "none":
            print(f"[walk] {w['cell']} status step: "
                  f"{dirty_line(steps['status']['result']['stdout'], d + ' status step')}")
            for s in ("status", "claim", "release"):
                if steps[s]["result"]["rc"] != 0:
                    die(f"{d}: {s} rc {steps[s]['result']['rc']}")
        # the verdict recorded afterwards on the same walk
        v = jload(os.path.join(VERDICTS, w["id"] + ".json"))
        if v["id"] != w["id"] or (v.get("verdict") or {}).get("verdict") not in ("green", "red"):
            die(f"{w['id']}: no recorded verdict")
        vday = datetime.datetime.fromtimestamp(v["verdict"]["at"], UTC).date()
        out.append({
            "cell": w["cell"], "id": w["id"], "requires": w["requires"], "ids": ids,
            "old": [old_ok[i] for i in ids], "new": [new_ok[i] for i in ids],
            "now": [r["now"] == "ok" for r in rows], "gap": [i in gap for i in ids],
            "old_day": cell_at(old_j["verdict"]["line"], old_j["provenance"]),
            "new_day": cell_at(new_j["verdict"]["line"]),
            "run_day": cell_at(run["cell_verdict"]["line"]),
            "old_v": old_j["verdict"]["state"], "new_v": new_j["verdict"]["state"],
            "run_v": run["cell_verdict"]["state"], "r2g": len(r2g),
            "r2g_gap": len([i for i in r2g if i in gap]), "ndt": ndt, "kernel": kern,
            "verdict": v["verdict"]["verdict"], "verdict_day": vday})
        print(f"[walk] {w['cell']:34s} {w['requires']:5s} asserts {len(ids)}  old FAIL "
              f"{sum(not x for x in out[-1]['old'])} (fixture gap {len(gap)})  red->green "
              f"{len(r2g)}  run {out[-1]['run_v']}  ndt {ndt[:8]}  verdict {out[-1]['verdict']} "
              f"{vday}")
    if len({w["ndt"] for w in out}) != 1:
        die("the two walks ran different ndt blobs")
    return out


def fig_s3(code, wk):
    # the ruling's four words (v2 lines 15-18) and cells.py's step list, both asserted
    must(RUL_V2, "old = the pre-fix record, which should be red;",
         "new = the first green on the night of the fix;",
         "run = run the cell now on the lab, with a claim when the cell needs the lab;",
         "walk = the guided sequence old → new → claim → run → compare → your verdict.")
    run_day = {w["run_day"] for w in wk}
    if len(run_day) != 1:
        die("the two walks ran on different days")
    run_day = run_day.pop()
    H = 6.3
    fig, ax = canvas(H)
    title(ax, f"Live cells: two guided walks, {md(run_day)}")

    # READ THE CODE: the walk's steps, one thin strip (the old/new cell itself was on 9/16)
    txt(ax, 0.55, 1.02, "READ THE CODE", size=12, color=FAINT, weight="bold", ha="left")
    steps = ["old", "new", "status", "claim", "run", "release", "compare", "verdict"]
    lab_only = {"status", "claim", "release"}
    bw, gap, x0, y0, bh = 1.34, 0.21, 0.55, 1.24, 0.60
    for i, name in enumerate(steps):
        x = x0 + i * (bw + gap)
        rbox(ax, x, y0, bw, bh, WHITE, MUTED if name in lab_only else INK, lw=1.2,
             ls=(0, (4, 3)) if name in lab_only else "solid", inset=0.0)
        txt(ax, x + bw / 2, y0 + bh / 2, name, size=13.5, weight="bold")
        if i:
            arrow(ax, x - gap + 0.02, y0 + bh / 2, x - 0.02, y0 + bh / 2, lw=1.3)
    legend_item(ax, x0 + 7 * (bw + gap) + bw - 2.62, 1.02, WHITE, MUTED, "lab cells only",
                ls=(0, (4, 3)))

    ax.plot([0.45, W - 0.45], [2.18, 2.18], color=RULE, lw=1.5)

    # RAN IT: the two walks of 09-24
    txt(ax, 0.55, 2.50, "RAN IT · dates UTC", size=12,
        color=FAINT, weight="bold", ha="left")
    sq, pitch, rowh = 0.36, 0.45, 0.56
    gx = [0.55, 6.25]
    # the old/new rows are the fixture's frozen records from before the 09-16 report: they sit in
    # the deck's pre-09-16 background band (coordinator ruling, 2026-09-27 UTC, round 3)
    cut = datetime.date(2026, 9, 16)
    for w in wk:
        if not (w["old_day"] < cut and w["new_day"] < cut and w["run_day"] >= cut):
            die(f"{w['cell']}: old/new are not both before 09-16 or run is not after it")
    ax.add_patch(FancyBboxPatch((0.40, 3.78 - 0.34), W - 0.80, rowh + 0.68,
                                boxstyle="round,pad=0,rounding_size=0.06", facecolor="#F1F2F3",
                                edgecolor=RULE, lw=1.0, zorder=0))
    legend_item(ax, W - 4.10, 2.50, "#F1F2F3", RULE, "before 09-16 · background", w=0.34,
                h=0.24)
    for g, w in enumerate(wk):
        x = gx[g]
        txt(ax, x, 2.98, w["cell"], size=12.5, weight="bold", ha="left", mono=True)
        txt(ax, x, 3.30, REQUIRES_LABEL[w["requires"]], size=11.5, color=MUTED, ha="left")
        sx = x + 1.35
        for r, (lab, day, states, gaps, v) in enumerate((
                ("old", w["old_day"], w["old"], w["gap"], w["old_v"]),
                ("new", w["new_day"], w["new"], [False] * len(w["ids"]), w["new_v"]),
                ("run", w["run_day"], w["now"], [False] * len(w["ids"]), w["run_v"]))):
            y = 3.78 + r * rowh
            txt(ax, x, y, lab, size=13.5, weight="bold", ha="left")
            txt(ax, x + 0.52, y, md(day), size=11.5, color=MUTED, ha="left")
            for k, ok in enumerate(states):
                cx = sx + k * pitch
                if ok:
                    fc, ec, ht = GREEN, GREEN, None
                elif gaps[k]:
                    fc, ec, ht = WHITE, WARNC, "////"
                else:
                    fc, ec, ht = WARNC, WARNC, None
                ax.add_patch(Rectangle((cx, y - sq / 2), sq, sq, facecolor=fc, edgecolor=ec,
                                       lw=1.1, hatch=ht, zorder=4))
            vx = sx + len(states) * pitch + 0.12
            txt(ax, vx, y, v, size=13, ha="left", color=GREEN if v == "PASS" else WARNC)
        y = 3.78 + 3 * rowh + 0.12
        real = w["r2g"] - w["r2g_gap"]
        val = str(real) + (f"  (+{w['r2g_gap']} fixture gap)" if w["r2g_gap"] else "")
        txt(ax, x, y, "red → green", size=12, color=MUTED, ha="left")
        txt(ax, sx, y, val, size=13, weight="bold", ha="left")
    ly = 5.95
    legend_item(ax, 0.55, ly, GREEN, GREEN, "ok", w=0.30, h=0.26)
    legend_item(ax, 1.45, ly, WARNC, WARNC, "FAIL", w=0.30, h=0.26)
    legend_item(ax, 2.55, ly, WHITE, WARNC, "FAIL: fixture gap", hatch="////", w=0.30,
                h=0.26)
    txt(ax, 5.00, ly, "one square = one assertion", size=12, color=MUTED, ha="left")
    save(fig, "fig_s3_cells_and_walks")


# ------------------------------------------------------------------------------ fig_s4_gui_plan
def gui_facts(code):
    v1_day = commit_day(GUI_V1)
    rc, tree = git("ls-tree", "-r", "--name-only", GUI_V1, "tools/ndt_serve/static")
    files = sorted(os.path.basename(p) for p in tree.split())
    if rc or files != ["app.css", "app.js", "index.html"]:
        die(f"{GUI_V1}: tools/ndt_serve/static is {files}")
    rc, parents = git("log", "-1", "--format=%P", GUI_V1)
    if len(parents.split()) != 2:
        die(f"{GUI_V1} is not a merge")
    must(SERVE, '"/": ("index.html"', '"/app.js": ("app.js"', '"/app.css": ("app.css"')
    appjs = text(APPJS)
    if "setInterval" in appjs:
        die("app.js has a timer now: v1 is no longer manual refresh")
    must(RUL_SCOPE, "| 6 | auto refresh | **manual only in this cut**")
    v2 = text(RUL_V2)
    m_day = re.search(r"\((\d{4}-\d{2}-\d{2}) ~21:1x, interactive form\)", v2)
    m_stack = re.search(r"rebuild the page with Web-GUI's stack \(([^)]+)\)", v2)
    m_ref = re.search(r"every (\d+) s, paused while `measuring` is not `nothing`", v2)
    m_port = re.search(r"Web-GUI listens on ([0-9.]+):(\d+) in Docker", v2)
    for needle in ("keep it INSIDE ndt serve",
                   "The security red lines are unchanged: loopback only, no CORS, the one-time "
                   "URL fragment traded for a token.",
                   "merge ndt serve and Web-GUI into ONE app",
                   "The merge itself is a separate design question, not scheduled.",
                   "Topology and traffic stay in Web-GUI"):
        if needle not in v2:
            die(f"RULINGS v2 no longer says {needle!r}")
    if not (m_day and m_stack and m_ref and m_port):
        die("RULINGS v2: date / stack / refresh / Web-GUI port not where this script reads them")
    stack = [s.strip() for s in m_stack.group(1).split("+")]
    if stack != ["React", "Vite", "Tailwind", "TypeScript", "i18next"]:
        die(f"stack is {stack}")
    # Web-GUI's own files: the same stack, and port 3000 published with no host address
    pkg = jload(os.path.join(WEBGUI, "package.json"))
    deps = dict(pkg.get("dependencies", {}), **pkg.get("devDependencies", {}))
    for dep in ("react", "vite", "tailwindcss", "typescript", "i18next"):
        if dep not in deps:
            die(f"Web-GUI package.json has no {dep}")
    compose = text(os.path.join(WEBGUI, "docker-compose.yml"))
    if f"- '{m_port.group(2)}:{m_port.group(2)}'" not in compose:
        die("Web-GUI docker-compose.yml no longer publishes the ruling's port")
    # how far v2 is: a v2 branch, and what its commits (those not on trunk) touch. Only doc/
    # => "scope draft only"; no branch => "not started"; anything else stops this script.
    # A commit on any ref after the v1 merge whose subject names the new stack is held to the
    # same rule.
    rc, refs = git("for-each-ref", "--format=%(refname:short)", "refs/heads")
    v2refs = [r for r in refs.split() if re.search(r"gui[-_]?v2", r, re.I)]
    pat = re.compile(r"gui[-_ ]?v2|react|vite|tailwind|i18next|i18n", re.I)
    rc2, subj = git("log", "--all", "--format=%H %s", f"{GUI_V1}..")
    shas = [ln.split()[0] for ln in subj.splitlines() if pat.search(ln.split(" ", 1)[1])]
    touched, v2log = set(), []
    for r in v2refs:
        _rc, lg = git("log", "--format=%h %cI %s", r, "--not", "trunk")
        v2log += [(r, ln) for ln in lg.splitlines()]
        shas += [ln.split()[0] for ln in lg.splitlines()]
    for s in shas:
        _rc, files = git("show", "--format=", "--name-only", s)
        touched |= set(files.split())
    if rc or rc2:
        die("cannot list refs / commits")
    # the v2 PAGE is new static files / a Node build (tools/ndt_serve/static, package.json,
    # vite/tailwind config, .ts/.tsx); anything else on the branch is preparation
    page = sorted(f for f in touched if f.startswith("tools/ndt_serve/static/") or
                  re.search(r"(^|/)(package\.json|vite\.config\.\w+|tailwind\.config\.\w+)$|\.tsx?$", f))
    if page:
        die(f"the v2 page itself has started ({page[:5]}) -- update the tag")
    if any(not f.startswith("doc/") for f in touched):
        v2_state = "on a branch, no page yet"
    else:
        v2_state = "scope draft only" if touched else "not started"
    print(f"[gui] v1 {GUI_V1} {v1_day.date()}  v2 ruled {m_day.group(1)} stack {stack} "
          f"refresh {m_ref.group(1)} s  Web-GUI {m_port.group(1)}:{m_port.group(2)}  "
          f"v2: {v2_state} {v2log} files {sorted(touched)}")
    return {"v1_day": v1_day.date(), "v2_day": datetime.date.fromisoformat(m_day.group(1)),
            "stack": stack, "refresh": m_ref.group(1), "wg_addr": m_port.group(1),
            "wg_port": m_port.group(2), "bind": code["bind"], "v2_state": v2_state}


def fig_s4(code):
    gf = gui_facts(code)
    H = 5.75
    fig, ax = canvas(H)
    title(ax, "Where the ndt serve page goes")
    bw, bh, y0 = 3.75, 2.80, 1.55
    xs = [0.55, 4.79, 9.03]
    stages = [
        ("v1: a static page", ["index.html · app.js · app.css", "served by ndt serve",
                               "manual refresh"],
         GREEN, f"merged {md(gf['v1_day'])}", INK, "solid"),
        ("v2: Web-GUI's stack", [" · ".join(gf["stack"][:3]), " · ".join(gf["stack"][3:]),
                                 "still inside ndt serve",
                                 f"{gf['refresh']} s refresh", "paused while measuring"],
         AMBER, f"ruled {md(gf['v2_day'])} · {gf['v2_state']}", INK, "solid"),
        ("one app with Web-GUI", ["topology · traffic · lab"],
         GREY, "not scheduled", MUTED, (0, (4, 3))),
    ]
    for i, (head, lines, dot, tag, edge, ls) in enumerate(stages):
        x = xs[i]
        ax.plot([x + 0.12], [1.13], marker="o", ms=11, color=dot, zorder=6)
        txt(ax, x + 0.34, 1.13, tag, size=13, color=BODY, ha="left")
        rbox(ax, x, y0, bw, bh, WHITE, edge, lw=1.5, ls=ls, inset=0.0)
        txt(ax, x + bw / 2, y0 + 0.40, head, size=15, weight="bold")
        for k, ln in enumerate(lines):
            txt(ax, x + bw / 2, y0 + 0.92 + k * 0.40, ln, size=12.5, color=MUTED)
        if i:
            arrow(ax, xs[i - 1] + bw + 0.05, y0 + bh / 2, x - 0.05, y0 + bh / 2, lw=1.6,
                  color=MUTED)
    # stage 3: the conflict it must resolve first
    x = xs[2]
    cy, ch, cw = y0 + 1.22, 0.62, (bw - 0.5) / 2
    for j, (lab, sub, col) in enumerate(((f"Web-GUI", f"{gf['wg_addr']}:{gf['wg_port']}", WARNC),
                                         ("ndt serve", f"{gf['bind']} only", ACCENT))):
        cx = x + 0.2 + j * (cw + 0.1)
        rbox(ax, cx, cy, cw, ch, WHITE, col, lw=1.4, inset=0.0)
        txt(ax, cx + cw / 2, cy + 0.2, lab, size=12, weight="bold", color=col)
        txt(ax, cx + cw / 2, cy + 0.44, sub, size=11, color=col, mono=True)
    txt(ax, x + bw / 2, cy + ch + 0.32, "resolve first", size=12.5, color=WARNC, weight="bold")

    # the red lines under v1 and v2; open under the merged app
    by, bhh = y0 + bh + 0.35, 0.62
    rbox(ax, xs[0], by, xs[1] + bw - xs[0], bhh, ACCENT_BG, ACCENT, lw=1.4, inset=0.0)
    txt(ax, (xs[0] + xs[1] + bw) / 2, by + bhh / 2,
        f"{gf['bind']} only  ·  token per call  ·  one-time link  ·  no CORS",
        size=13, color=ACCENT, weight="bold")
    rbox(ax, xs[2], by, bw, bhh, WHITE, WARNC, lw=1.4, ls=(0, (4, 3)), inset=0.0)
    txt(ax, xs[2] + bw / 2, by + bhh / 2, "red lines: open question", size=13, color=WARNC)
    save(fig, "fig_s4_gui_plan")


def main(argv=None):
    figs = ("fig_s2_security_model", "fig_s3_cells_and_walks", "fig_s4_gui_plan")
    ap = argparse.ArgumentParser(description="fig_s2, fig_s3, fig_s4 of the 930 deck")
    ap.add_argument("--only", action="append", choices=figs,
                    help="draw only this figure (repeatable); the facts are checked in full")
    a = ap.parse_args(argv)
    want = set(a.only or figs)
    code = code_facts()
    obs = live_facts()
    wk = walks()
    if "fig_s2_security_model" in want:
        fig_s2(code, obs)
    if "fig_s3_cells_and_walks" in want:
        fig_s3(code, wk)
    if "fig_s4_gui_plan" in want:
        fig_s4(code)
    for f in figs:
        if f not in want:
            print(f"[skip] {f} (not in --only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
