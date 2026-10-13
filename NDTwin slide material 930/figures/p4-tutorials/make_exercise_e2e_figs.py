#!/usr/bin/env python3
"""
make_exercise_e2e_figs.py -- three P4-tutorial figures in the style of fig_t6 (T4, multicast):

    fig_t6b_basic_tunnel_end_to_end   basic_tunnel: the tunnel's dst_id picks the host; the
                                      skeleton stops at pre-flight
    fig_t6c_firewall_end_to_end       firewall on s1, basic on s2-s4: h1 -> h3 connects,
                                      h3 -> h1 is blocked; the skeleton lets both through
    fig_t6d_p4runtime_end_to_end      the exercise's own controller programs s1 and s2 through
                                      NDTwin's adapter; ping, tunnel counter, link bytes

Each figure has the fig_t6 layout: the arm's steps on top, what was put on the fabric at the
bottom left, the packet test of both arms at the bottom right, plus the twin's link reading of
the solution arm (bottom right, under the packet test).

Data (read at run time; every number on a canvas is parsed, and what it relies on is asserted):
  T06 = doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/2026-09-27T074635Z_06_thirteen
        /00_table.tsv and the six arm reports it names for these three exercises
        (runs/<UTC>_<exercise>_<arm>_ndtwin.md) with their same-named directories
        (link_usage/, driver-*.log); code 5dc7fc9a +95 (dirty checkout) per their `ndt status`.
  READ (not run): the tutorials checkout the arms ran (/home/adam/tutorials, c80d83e):
        exercises/<ex>/<topology> for the drawn wiring (cross-checked against the arms' own
        output), exercises/p4runtime/advanced_tunnel.p4 for the tunnel header's width.
Layout, palette and drawing helpers are imported from make_exercise_path_figs.py (fig_t6);
nothing in that file is changed.

Every stop is `stop(TAG, ...)`; the red check drives each TAG with a tampered input
(K/scratch/overnight-2026-09-05/logs/slides930/make_exercise_e2e_figs-redcheck.py).

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/p4-tutorials"
    nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_exercise_e2e_figs.py
"""
import sys

sys.dont_write_bytecode = True  # the figure folder is in a work tree with a public remote

import csv  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_exercise_path_figs as mep  # noqa: E402  (fig_t6's layout, palette and helpers)
from make_exercise_path_figs import (  # noqa: E402
    plt, Rectangle, canvas, box, txt, arrow, preflight_blocks,
    INK, BODY, MUTED, FAINT, RULE, ACCENT, ACCENT_BG, PANEL, WARNC, WARN_BG, WHITE, GREEN, AMBER,
    GREY)

REPO = os.environ.get("NDTWIN_REPO", "/home/adam/Desktop/NDTwin-Kernel")
PREP = os.path.join(REPO, "doc/audit/2026-09-04_p4-tutorial-exercise-prep")
RUNS = os.path.join(PREP, "runs")
T06 = os.path.join(PREP, "live-p1/runs/2026-09-27T074635Z_06_thirteen/00_table.tsv")
TUT = os.environ.get("TUTORIALS", "/home/adam/tutorials")
OUTDIR = os.environ.get("E2E_OUTDIR", HERE)
HIRES = os.path.join(OUTDIR, "_hires")

CODE_SHA, CODE_PLUS = "5dc7fc9a", 95          # what the .md files say the arms ran on
EXERCISES = ("basic_tunnel", "firewall", "p4runtime")


def stop(tag, msg):
    raise SystemExit(f"make_exercise_e2e_figs: [{tag}] {msg}")


def read(path, tag, what):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError as e:
        stop(tag, f"{what}: cannot read {path}: {e.strerror}")


def one(pattern, text, tag, what, flags=re.M):
    m = re.search(pattern, text, flags)
    if not m:
        stop(tag, f"{what}: /{pattern}/ not found")
    return m


def section(text, head_re, tag, what):
    """(command, output) of the step whose heading is `### N. <head_re>` -- the first two fenced
    blocks between that heading and the next `### ` heading."""
    m = re.search(r"^### \d+\. " + head_re + r"$", text, re.M)
    if not m:
        stop(tag, f"{what}: no step heading /{head_re}/")
    nxt = re.search(r"^#{2,3} ", text[m.end():], re.M)
    body = text[m.end(): m.end() + nxt.start()] if nxt else text[m.end():]
    blocks = re.findall(r"```\n(.*?)```", body, re.S)
    if len(blocks) < 2:
        stop(tag, f"{what}: step /{head_re}/ has no output block")
    return blocks[0], blocks[1]


def title(ax, s):
    if len(s) > 45:
        stop("TITLE", f"title over 45 characters: {s!r}")
    txt(ax, 0.45, 0.48, s, size=22, weight="bold", ha="left")


def save(fig, name):
    os.makedirs(HIRES, exist_ok=True)
    for ext in ("pdf", "png", "svg"):
        kw = {"dpi": 300} if ext == "png" else {}
        fig.savefig(os.path.join(OUTDIR, f"{name}.{ext}"), facecolor=WHITE, **kw)
    fig.savefig(os.path.join(HIRES, f"{name}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"[out] {name}.{{pdf,png,svg}} + _hires/{name}.png")


def swnum(s):
    return int(s[1:])


def ifkey(i):
    m = re.fullmatch(r"s(\d+)-eth(\d+)", i)
    return (int(m.group(1)), int(m.group(2)))


# ---------------------------------------------------------------------------
# T06 and the arm reports
# ---------------------------------------------------------------------------

REPORT_RE = (r"^/.+/doc/audit/2026-09-04_p4-tutorial-exercise-prep/runs/"
             r"(2026-09-27T\d{6}Z_([a-z0-9_]+)_(solution|skeleton)_ndtwin\.md)$")


def t06_rows():
    try:
        with open(T06, newline="") as f:
            rows = list(csv.DictReader(f, delimiter="\t"))
    except OSError as e:
        stop("T06_OPEN", f"cannot read {T06}: {e.strerror}")
    if len(rows) != 26:
        stop("T06_ROWS", f"{T06}: {len(rows)} rows, not 26")
    out = {}
    for r in rows:
        if (r.get("exercise"), r.get("which")) in out:
            stop("T06_DUP", f"{T06}: {r.get('exercise')}/{r.get('which')} twice")
        out[(r.get("exercise"), r.get("which"))] = r
    for ex in EXERCISES:
        for which in ("solution", "skeleton"):
            r = out.get((ex, which))
            if r is None:
                stop("T06_MISSING", f"{T06}: no row {ex}/{which}")
            m = re.match(REPORT_RE, r.get("report") or "")
            if not m or m.group(2) != ex or m.group(3) != which:
                stop("T06_REPORT", f"{T06}: {ex}/{which} names report {r.get('report')!r}")
            r["path"] = os.path.join(RUNS, m.group(1))
            if not re.fullmatch(r"-?\d+", r.get("rc") or ""):
                stop("T06_RC", f"{T06}: {ex}/{which} rc {r.get('rc')!r} is not an integer")
    return out


def verdict_rows(text, what):
    i = text.find("## 5. 判定表")
    j = text.find("\n## ", i + 1)
    if i < 0:
        stop("VT_TABLE", f"{what}: no verdict table (## 5. 判定表)")
    rows = re.findall(r"^\| (PASS|FAIL) \| ([^|]+) \|", text[i:j if j > 0 else None], re.M)
    return [(s, e.strip()) for s, e in rows]


def first_preflight(text, what):
    blocks = preflight_blocks(text.splitlines())
    if not blocks:
        stop("PF_NONE", f"{what}: no pre-flight block")
    rows, end = blocks[0]
    for other, oend in blocks[1:]:
        if [(s, lab) for s, lab, _ in other] != [(s, lab) for s, lab, _ in rows] or oend != end:
            stop("PF_DISAGREE", f"{what}: two pre-flight blocks disagree")
    n = {k: sum(1 for s, _, _ in rows if s == k) for k in ("PASS", "INFO", "FAIL")}
    return rows, end, n


def parse_common(row, ex, which):
    """What every arm report says about itself: verdict, the package, pre-flight."""
    what = f"{ex}/{which}"
    text = read(row["path"], "ARM_OPEN", what)
    a = {"what": what, "text": text, "path": row["path"], "dir": row["path"][:-3]}
    m = one(r"^\| 判定 \| \*\*(.+?)\*\* \(exit (\d+)\) \|$", text, "ARM_VERDICT", what)
    a["verdict"], a["exit"] = m.group(1), int(m.group(2))
    if a["verdict"] != row["verdict"] or a["exit"] != int(row["rc"]):
        stop("ARM_T06", f"{what}: report says {a['verdict']!r} (exit {a['exit']}), T06 says "
                        f"{row['verdict']!r} (rc {row['rc']})")
    m = one(r"^(PASS|RED ARM) \((\d+)/(\d+)\)", a["verdict"], "ARM_VERDICT_FORM", what)
    a["n_ok"], a["n_all"] = int(m.group(2)), int(m.group(3))
    vt = verdict_rows(text, what)
    if len(vt) != a["n_all"] or a["n_ok"] != a["n_all"] or any(s != "PASS" for s, _ in vt):
        stop("VT_COUNT", f"{what}: verdict {a['verdict']!r} over table rows {vt}")
    a["vt"] = [e for _, e in vt]
    topo = one(r"^## 3\. 拓樸\n+```\n(.*?)```", text, "ARM_TOPO", what, re.M | re.S).group(1)
    a["topofile"] = one(r"^topology\s+:\s+(\S+)$", topo, "ARM_TOPO", what).group(1)
    a["hosts"] = [h.strip() for h in one(r"^hosts\s+:\s+(.+)$", topo, "ARM_TOPO", what)
                  .group(1).split(",")]
    a["switches"] = [s.strip() for s in one(r"^switches\s+:\s+(.+)$", topo, "ARM_TOPO", what)
                     .group(1).split(",")]
    a["n_links"] = int(one(r"^links\s+:\s+(\d+)$", topo, "ARM_TOPO", what).group(1))
    _, conv = section(text, r"N1  convert\.py", "SEC_CONVERT", what)
    a["files"] = int(one(r"^\s+files\s+:\s+(\d+)$", conv, "CONVERT", what).group(1))
    a["mode"] = one(r"^\s+control plane\s+:\s+(\S+)$", conv, "CONVERT", what).group(1)
    pipes = one(r"^\s+pipelines\s+:\s+(.+)$", conv, "CONVERT", what).group(1)
    a["pipes"] = dict(p.strip().split("=", 1) for p in pipes.split(","))
    first = one(r"^\s+files\s+:\s+\d+\n\s+(\S+)$", conv, "CONVERT", what).group(1)
    listed = [first] + [f for f in re.findall(r"^\s{18}(\S+)$", conv, re.M) if f != first]
    if len(listed) != a["files"] or sorted(a["pipes"], key=swnum) != a["switches"]:
        stop("CONVERT_LIST", f"{what}: convert lists {len(listed)} files for {a['files']}, "
                             f"pipelines for {sorted(a['pipes'])} vs switches {a['switches']}")
    a["pf_rows"], a["pf_end"], a["pf"] = first_preflight(text, what)
    return a


def parse_ran(row, ex, which):
    """An arm that went through ndt up: claim, up, switch_state, teardown."""
    a = parse_common(row, ex, which)
    what, text = a["what"], a["text"]
    if a["pf"]["FAIL"] != 0 or not a["pf_end"].startswith("PASS --"):
        stop("PF_RAN", f"{what}: ran, but its pre-flight has {a['pf']['FAIL']} FAIL / {a['pf_end']!r}")
    m = one(r"^\s+code\s+([0-9a-f]{7,40})\s+\+(\d+) file\(s\) with uncommitted changes$", text,
            "CODE", what)
    if m.group(1) != CODE_SHA or int(m.group(2)) != CODE_PLUS:
        stop("CODE", f"{what}: ran on {m.group(1)} +{m.group(2)}, the .md says {CODE_SHA} "
                     f"+{CODE_PLUS}")
    a["claim_min"] = int(one(r"^\s*ok\s+lab claimed by \S+ for (\d+)m", text, "CLAIM",
                             what).group(1))
    _, up = section(text, r"N3  ndt up p4 --app", "SEC_UP", what)
    a["up"] = up
    m = one(r"ok\s+(\d+) switches up after (\d+)s", up, "UP_SWITCHES", what)
    a["n_up"] = int(m.group(1))
    if a["n_up"] != len(a["switches"]):
        stop("UP_SWITCHES", f"{what}: {a['n_up']} switches up for {a['switches']}")
    a["binary"] = one(r"ok\s+running binary: (\S+)", up, "UP_BINARY", what).group(1)
    a["hb_links"] = [tuple(sorted([(x, int(p)), (y, int(q))])) for x, p, y, q in re.findall(
        r"^\s*link (s\d+)-eth(\d+) \(dpid \d+ port \d+\) <-> (s\d+)-eth(\d+) \(dpid \d+ port \d+\)$",
        up, re.M)]
    # the proxy's own account (section 3b of the report: GET /p4/switch_state, one line a switch)
    i = text.find("### 3b.")
    j = text.find("## 4.", i)
    if i < 0 or j < 0:
        stop("SS_SECTION", f"{what}: no section 3b (GET /p4/switch_state)")
    ss = text[i:j]
    a["ss_mode"] = one(r"^control_plane\.mode\s+(\S+)$", ss, "SS_MODE", what).group(1)
    if a["ss_mode"] != a["mode"]:
        stop("SS_MODE", f"{what}: switch_state mode {a['ss_mode']} vs convert {a['mode']}")
    a["ss"] = {}
    for sw, nd, sha, rec, app, fail in re.findall(
            r"^(s\d+)\s+ndtwin=(True|False) p4info_sha256=([0-9a-f]{16})\s+entries recorded=(\d+) "
            r"applied=(\d+) failed=(\d+) api_writes=\d+", ss, re.M):
        a["ss"][sw] = dict(ndtwin=nd == "True", sha=sha, rec=int(rec), app=int(app),
                           fail=int(fail))
    if sorted(a["ss"], key=swnum) != a["switches"]:
        stop("SS_ROWS", f"{what}: switch_state rows {sorted(a['ss'])} vs switches {a['switches']}")
    if any(v["ndtwin"] for v in a["ss"].values()):
        stop("SS_NDTWIN", f"{what}: a switch runs NDTwin's own program, not the package's")
    if any(v["fail"] or v["app"] != v["rec"] for v in a["ss"].values()):
        stop("SS_ENTRIES", f"{what}: per-switch entries {a['ss']}")
    # teardown
    _, down = section(text, r"N9  ndt down", "SEC_DOWN", what)
    if not re.search(r"^\s*verify clean$", down, re.M) or not re.search(r"^\s*clean$", down, re.M):
        stop("DOWN_CLEAN", f"{what}: ndt down has no 'verify clean' ... 'clean'")
    if int(one(r"^\s*ndt down rc=(\d+)$", text, "DOWN_RC", what).group(1)) != 0:
        stop("DOWN_RC", f"{what}: ndt down rc is not 0")
    _, rel = section(text, r"N10 ndt release", "SEC_RELEASE", what)
    if not re.search(r"^\s*ok\s+lab released$", rel, re.M):
        stop("RELEASED", f"{what}: ndt release did not print 'ok  lab released'")
    if int(one(r"^\s*ndt release rc=(\d+)$", text, "RELEASE_RC", what).group(1)) != 0:
        stop("RELEASE_RC", f"{what}: ndt release rc is not 0")
    return a


def need_rows(a, rows, tag):
    for r in rows:
        if r not in a["vt"]:
            stop(tag, f"{a['what']}: verdict table has no PASS row {r!r} (rows: {a['vt']})")


def entries_total(a):
    """Sum of the per-switch counts, reconciled with pre-flight and with ndt up's own line."""
    what, up = a["what"], a["up"]
    rec = sum(v["rec"] for v in a["ss"].values())
    app = sum(v["app"] for v in a["ss"].values())
    pf = [d for s, lab, d in a["pf_rows"] if lab == "entries match p4info"]
    m = re.match(r"(\d+) entries across (\d+) switch\(es\)", pf[0] if pf else "")
    if not m or int(m.group(1)) != rec or int(m.group(2)) != len(a["switches"]):
        stop("ENTRIES_PF", f"{what}: pre-flight {pf} vs switch_state total {rec}")
    per = {(v["app"], v["rec"]) for v in a["ss"].values()}
    m = one(r"ok\s+table entries: (\d+)/(\d+) applied (on|across) (\d+) switch\(es\)", up,
            "ENTRIES_UP", what)
    n, d, prep, k = int(m.group(1)), int(m.group(2)), m.group(3), int(m.group(4))
    # ndt prints the per-switch pair when every switch has the same one ("on"), else totals
    ok = k == len(a["switches"]) and (
        (prep == "on" and per == {(n, d)}) or (prep == "across" and (n, d) == (app, rec)
                                              and len(per) > 1))
    if not ok:
        stop("ENTRIES_UP", f"{what}: ndt up says {m.group(0)!r}; switch_state per switch {per}")
    return app, rec


# ---------------------------------------------------------------------------
# topology (READ, tutorials checkout) cross-checked against the arm's own output
# ---------------------------------------------------------------------------

def topology(ex, a):
    what = f"{ex} topology"
    path = os.path.join(TUT, "exercises", ex, a["topofile"])
    try:
        j = json.loads(read(path, "TOPO_OPEN", what))
    except json.JSONDecodeError as e:
        stop("TOPO_JSON", f"{path}: {e.msg}")
    hosts = sorted(j.get("hosts", {}), key=swnum)
    switches = sorted(j.get("switches", {}), key=swnum)
    host_at, sw_links, types = {}, [], {}
    for pair in j.get("links", []):
        ends = []
        for e in pair[:2]:
            m = re.fullmatch(r"(s\d+)-p(\d+)", e)
            ends.append((m.group(1), int(m.group(2))) if m else e)
        sws = [e for e in ends if isinstance(e, tuple)]
        if len(sws) == 2:
            sw_links.append(tuple(sorted(sws)))
            for s, p in sws:
                types[f"{s}-eth{p}"] = "switch"
        elif len(sws) == 1 and ends[0] in hosts:
            host_at[ends[0]] = sws[0]
            types[f"{sws[0][0]}-eth{sws[0][1]}"] = "host"
        else:
            stop("TOPO_LINK", f"{path}: link {pair} is neither host-switch nor switch-switch")
    if hosts != a["hosts"] or switches != a["switches"] or \
            len(j.get("links", [])) != a["n_links"] or sorted(host_at) != hosts:
        stop("TOPO_ARM", f"{path}: hosts {hosts} / switches {switches} / {len(j.get('links', []))} "
                         f"links vs the arm's {a['hosts']} / {a['switches']} / {a['n_links']}")
    if a["mode"] == "ndtwin" and sorted(a["hb_links"]) != sorted(sw_links):
        stop("TOPO_HEARTBEAT", f"{what}: ndt up's link list {sorted(a['hb_links'])} is not the "
                               f"topology's {sorted(sw_links)}")
    return dict(hosts=hosts, switches=switches, host_at=host_at, sw_links=sw_links, types=types)


# ---------------------------------------------------------------------------
# the twin's link reading (G1) of a solution arm
# ---------------------------------------------------------------------------

def link_reading(a, topo):
    what, text = a["what"], a["text"]
    _, out = section(text, r"N8  G1 link usage follows the iperf path", "SEC_G1", what)
    m = one(r"^LINK_USAGE (\S+) expect=follows primary=(\d+) minor=(\d+) rc=(\d+)$", out,
            "G1_LINE", what)
    n_primary, rc = int(m.group(2)), int(m.group(4))
    if rc != 0 or int(m.group(3)) != 0:
        stop("G1_RC", f"{what}: {m.group(0)}")
    it = one(r"^\s*\S+: (h\d+) -> (h\d+) \(([0-9.]+)\), iperf (.+)$", out, "G1_IPERF", what)
    if not it.group(4).startswith("-u "):
        stop("G1_NOT_UDP", f"{what}: the G1 traffic is not a plain UDP iperf: {it.group(4)!r}")
    pm = one(r"^\s*\S+: primary=(.*?)\s+minor=(.*)$", out, "G1_PRIMARY", what)
    primary = pm.group(1).split()
    if len(primary) != n_primary or pm.group(2).split():
        stop("G1_PRIMARY", f"{what}: primary {primary} for primary={n_primary}, minor "
                           f"{pm.group(2)!r}")
    twin = read(os.path.join(a["dir"], "link_usage/twin_integral.txt"), "TWIN_OPEN", what)
    rows = re.findall(r"^(s\d+-eth\d+) ([0-9.]+) (host|switch)$", twin, re.M)
    vals = {i: float(v) for i, v, _ in rows}
    types = {i: t for i, _, t in rows}
    if types != topo["types"]:
        stop("TWIN_TYPES", f"{what}: twin_integral.txt interfaces {types} vs the topology's "
                           f"{topo['types']}")
    if any(vals[i] <= 0 for i in primary):
        stop("TWIN_ONPATH", f"{what}: the twin reads 0 on an on-path interface: "
                            f"{[(i, vals[i]) for i in primary]}")
    others = sorted((i for i in vals if i not in primary), key=ifkey)
    if any(vals[i] != 0 for i in others):
        stop("TWIN_OFFPATH", f"{what}: the twin reads > 0 off the path: "
                             f"{[(i, vals[i]) for i in others if vals[i]]}")
    rep = {i: float(v) for i, v in re.findall(
        r"^\s*\S+: (?:on|off)-path\s+(s\d+-eth\d+)\s+([0-9.]+) bit", out, re.M)}
    if rep != vals:
        stop("TWIN_REPORT", f"{what}: the report's on/off-path lines are not twin_integral.txt")
    return dict(src=it.group(1), dst=it.group(2), ip=it.group(3), flags=it.group(4),
                primary=primary, others=others, vals=vals, types=types)


# ---------------------------------------------------------------------------
# drawing, shared by the three figures (fig_t6's geometry)
# ---------------------------------------------------------------------------

X0, Y0, BW, BH, GAP = 0.45, 1.00, 1.36, 0.92, 0.221
PY, PH = 2.55, 4.05


def steps_row(ax, steps, hot):
    cx = []
    for i, (a, b) in enumerate(steps):
        x = X0 + i * (BW + GAP)
        h = a in hot
        box(ax, x, Y0, BW, BH, fill=ACCENT_BG if h else WHITE, edge=ACCENT if h else INK,
            lw=2.2 if h else 1.2)
        txt(ax, x + BW / 2, Y0 + 0.32, a, size=13.5, weight="bold", color=ACCENT if h else INK)
        txt(ax, x + BW / 2, Y0 + 0.64, b, size=11.5, color=MUTED)
        cx.append(x + BW / 2)
        if i:
            arrow(ax, x - GAP + 0.02, Y0 + BH / 2, x - 0.02, Y0 + BH / 2)
    return cx


def connector(ax, x, y_to):
    ax.plot([x, x], [Y0 + BH, y_to], color=ACCENT, lw=1.8, ls=(0, (4, 3)), zorder=1)


def panel(ax, x, y, w, h, head):
    box(ax, x, y, w, h, fill=PANEL, edge=RULE, lw=1.0, r=0.08, z=1)
    txt(ax, x + 0.2, y + 0.28, head, size=11.5, color=FAINT, weight="bold", ha="left")


SW_STYLE = {  # fill, edge, lw, linestyle, label colour
    "prog": (WHITE, ACCENT, 2.0, "solid", ACCENT),
    "other": (WHITE, INK, 1.4, "solid", INK),
    "empty": (WHITE, MUTED, 1.2, (0, (3, 2)), MUTED),
}


def fabric(ax, gx, gy, gw, gh, topo, pos, style, key, host_y):
    """The switches (in a white group), their links, and the hosts under the group.
    pos: switch -> (cx, cy) and host -> cx; every drawn node must be a topology node."""
    nodes = sorted(pos)
    if nodes != sorted(topo["switches"] + topo["hosts"]):
        stop("LAYOUT", f"the topology's nodes {sorted(topo['switches'] + topo['hosts'])} are not "
                       f"the drawn layout's {nodes}")
    box(ax, gx, gy, gw, gh, fill=WHITE, edge=RULE, lw=1.0, r=0.06, z=1)
    for k, (st, label) in enumerate(key):
        fc, ec, lw, ls, _ = SW_STYLE[st]
        ky = gy + 0.24 + k * 0.29
        ax.add_patch(Rectangle((gx + 0.18, ky - 0.09), 0.18, 0.18, facecolor=fc, edgecolor=ec,
                               lw=lw * 0.8, linestyle=ls, zorder=3))
        txt(ax, gx + 0.46, ky, label, size=10.5, color=BODY, ha="left", mono=label.endswith(".json"))
    sw_w, sw_h = 0.92, 0.5
    for (s1, _), (s2, _) in topo["sw_links"]:
        (x1, y1), (x2, y2) = pos[s1], pos[s2]
        ax.plot([x1, x2], [y1, y2], color=MUTED, lw=1.4, zorder=2)
    for s in topo["switches"]:
        x, y = pos[s]
        fc, ec, lw, ls, tc = SW_STYLE[style[s]]
        box(ax, x - sw_w / 2, y - sw_h / 2, sw_w, sw_h, fill=fc, edge=ec, lw=lw, ls=ls, r=0.05,
            z=3)
        txt(ax, x, y, s, size=13.5, weight="bold", color=tc)
    for h in topo["hosts"]:
        s, _ = topo["host_at"][h]
        hx = pos[h]
        sx, sy = pos[s]
        ax.plot([hx if abs(hx - sx) <= sw_w / 2 - 0.08 else sx, hx], [sy + sw_h / 2, host_y - 0.2],
                color=MUTED, lw=1.2, zorder=2)
        box(ax, hx - 0.25, host_y - 0.2, 0.5, 0.4, fill=WHITE, edge=MUTED, lw=1.0, r=0.04, z=3)
        txt(ax, hx, host_y, h, size=11.5, color=BODY)


def cell(ax, cx, cy, w, h, fc, label, tc=WHITE):
    ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h, facecolor=fc, edgecolor=fc, lw=0.8,
                           zorder=3))
    if label:
        txt(ax, cx, cy, label, size=12, color=tc, weight="bold")


def chip(ax, x, cy, w, fc, tc, label):
    box(ax, x, cy - 0.2, w, 0.4, fill=fc, edge=fc, r=0.05, z=3)
    txt(ax, x + w / 2, cy, label, size=12, color=tc, weight="bold")


def iface_list(names):
    return ", ".join(names)


def twin_ipv4_panel(ax, x, y, w, h, lr):
    panel(ax, x, y, w, h, f"TWIN LINK READING · UDP iperf {lr['src']} → {lr['dst']}")
    cy = y + 0.8
    chip(ax, x + 0.25, cy, 1.4, AMBER, INK, "IPv4 only")
    txt(ax, x + 1.85, cy, f"> 0 on {iface_list(lr['primary'])}  ·  0 on the other "
                         f"{len(lr['others'])} ports", size=12, color=BODY, ha="left")


def num(n):
    return f"{n:,}"


# ---------------------------------------------------------------------------
# fig_t6b_basic_tunnel_end_to_end
# ---------------------------------------------------------------------------

def bt_tests(a):
    what, text = a["what"], a["text"]
    sends = re.findall(r"^### \d+\. (T(\d+))  h1 send\.py --dst_id (\d+)$", text, re.M)
    if [d for _, _, d in sends] != ["2", "3"]:
        stop("BT_SENDS", f"{what}: send steps {sends}, not --dst_id 2 then 3")
    hosts_ip = dict(p.split("=") for p in one(r"^\s*hosts: ((?:h\d+=[0-9.]+(?:, )?)+)$", text,
                                              "BT_HOSTS_IP", what).group(1).split(", "))
    ips, mat = set(), {}
    for tl, k, d in sends:
        cmd, out = section(text, rf"{tl}  h1 send\.py --dst_id {d}", "BT_SEND", what)
        ips.add(one(rf"send\.py (\d+\.\d+\.\d+\.\d+) .* --dst_id {d}$", cmd, "BT_SEND", what)
                .group(1))
        if not re.search(rf"^sending on interface \S+ to dst_id {d}$", out, re.M) or \
                not re.search(r"^\s+type\s+=\s+0x1212$", out, re.M) or \
                not re.search(r"^###\[ MyTunnel \]###", out, re.M):
            stop("BT_SENT", f"{what}: {tl}: send.py did not report a 0x1212 MyTunnel frame with "
                            f"dst_id {d}")
        for h in ("h2", "h3"):
            _, sn = section(text, rf"{tl}  {h} sniffer", "BT_SNIFF", what)
            got = len(re.findall(r"^got a packet$", sn, re.M))
            ids = re.findall(r"^\s+dst_id\s+=\s+(\d+)$", sn, re.M)
            if len(ids) != got or any(i != d for i in ids):
                stop("BT_RECV", f"{what}: {tl} {h} got {got} packet(s) carrying dst_id {ids}, "
                                f"sent {d}")
            log = read(os.path.join(a["dir"], f"driver-{h}-{k}-receive.log"), "BT_LOG", what)
            if len(re.findall(r"^got a packet$", log, re.M)) != got:
                stop("BT_LOG", f"{what}: driver-{h}-{k}-receive.log disagrees with the report")
            mat[(d, h)] = got
    if len(ips) != 1:
        stop("BT_SEND_IP", f"{what}: the two sends went to different IPs {sorted(ips)}")
    ip = ips.pop()
    if hosts_ip.get("h2") != ip:
        stop("BT_HOSTS_IP", f"{what}: the sends' IP {ip} is not h2's ({hosts_ip})")
    if not (mat[("2", "h2")] >= 1 and mat[("2", "h3")] == 0 and mat[("3", "h2")] == 0
            and mat[("3", "h3")] >= 1):
        stop("BT_MATRIX", f"{what}: who received what {mat} is not dst_id 2 -> h2, 3 -> h3")
    return ip, mat, len(sends)


def bt_skeleton(row):
    a = parse_common(row, "basic_tunnel", "skeleton")
    what, text = a["what"], a["text"]
    fails = [(lab, d) for s, lab, d in a["pf_rows"] if s == "FAIL"]
    labelled = [(lab, d) for lab, d in fails if lab]
    if len(labelled) != 1 or labelled[0][0] != "entries match p4info" or \
            not a["pf_end"].startswith("FAIL --"):
        stop("BTSK_PF", f"{what}: failing checks {labelled}, end {a['pf_end']!r}")
    m = re.match(r"(\d+) problem\(s\); first: (s\d+) entry (\d+): table '([^']+)' is not in the "
                 r"p4info \(it has: ([^)]+)\)", labelled[0][1])
    if not m:
        stop("BTSK_DETAIL", f"{what}: FAIL detail changed: {labelled[0][1]!r}")
    if a["exit"] != 1 or not a["verdict"].startswith("RED ARM") or \
            "pre-flight FAILED (rc 1)" not in text:
        stop("BTSK_RC", f"{what}: not refused with rc 1 ({a['verdict']!r}, exit {a['exit']})")
    if "== ndt up p4 --app" in text or re.search(r"^### \d+\. N3  ndt up", text, re.M):
        stop("BTSK_UP", f"{what}: the refused arm shows an ndt up")
    return dict(table=m.group(4), problems=int(m.group(1)), verdict=a["verdict"].split(":")[0])


def fig_bt(rows):
    ex = "basic_tunnel"
    sol = parse_ran(rows[(ex, "solution")], ex, "solution")
    sk = bt_skeleton(rows[(ex, "skeleton")])
    topo = topology(ex, sol)
    need_rows(sol, ["--dst_id 2 lands on h2", "--dst_id 3 lands on h3, same IP",
                    "G1  link usage follows the iperf path"], "BT_VT")
    if sol["mode"] != "ndtwin" or len(set(sol["pipes"].values())) != 1:
        stop("BT_PIPES", f"{sol['what']}: mode {sol['mode']}, pipelines {sol['pipes']}")
    pipe = next(iter(sol["pipes"].values()))
    app, rec = entries_total(sol)
    ip, mat, n_frames = bt_tests(sol)
    lr = link_reading(sol, topo)
    print(f"[t6b] solution {sol['verdict']}: files {sol['files']}, pre-flight {sol['pf']}, claim "
          f"{sol['claim_min']} min, bmv2 x {sol['n_up']} ({sol['binary']}) running {pipe}, "
          f"entries {app}/{rec} ({ {s: v['app'] for s, v in sol['ss'].items()} }), send to {ip}, "
          f"received {mat}; twin > 0 on {lr['primary']}, 0 on {lr['others']}")
    print(f"[t6b] skeleton {sk['verdict']}: pre-flight refused, {sk['problems']} problems, first "
          f"{sk['table']} not in its p4info")

    fig, ax = canvas(7.0)
    title(ax, "basic_tunnel, end to end on the NDTwin fabric")
    cx = steps_row(ax, [
        ("convert.py", f"{sol['files']} files"),
        ("pre-flight", f"{sol['pf']['PASS']} PASS · {sol['pf']['FAIL']} FAIL"),
        ("ndt claim", f"{sol['claim_min']}-min lease"),
        ("ndt up", f"bmv2 × {sol['n_up']}"),
        ("packet test", f"{n_frames} tunnel frames"),
        ("ndt down", "verified clean"),
        ("ndt release", "released"),
        ("arm report", "verdict table"),
    ], hot=("ndt up", "packet test"))
    # ---- left: what ndt up put on the fabric
    lx, lw_ = 0.45, 5.75
    panel(ax, lx, PY, lw_, PH, "NDT UP")
    connector(ax, cx[3], PY)
    ndt_up_left(ax, lx, sol)
    gx, gy, gw, gh = 3.35, 3.0, 2.65, 2.35
    arrow(ax, 2.47, 3.75, gx - 0.02, 3.75, color=ACCENT, lw=1.8)
    txt(ax, (2.47 + gx) / 2, 3.55, "P4Runtime", size=11, color=ACCENT)
    fabric(ax, gx, gy, gw, gh, topo,
           {"s1": (4.0, 4.02), "s2": (5.35, 4.02), "s3": (4.675, 4.95),
            "h1": 4.0, "h2": 5.35, "h3": 4.675},
           {s: "prog" for s in topo["switches"]}, [("prog", pipe)], host_y=5.95)
    # ---- right: the packet test, both arms
    rx, rw, ph = 6.55, 6.33, 2.5
    panel(ax, rx, PY, rw, ph, f"PACKET TEST · h1 sends to {ip}, h2's IP")
    connector(ax, cx[4], PY)
    c, gx0, gy0 = 0.42, rx + 1.3, PY + 1.12
    txt(ax, gx0 + c, PY + 0.68, "solution", size=14, weight="bold")
    for j, h in enumerate(("h2", "h3")):
        txt(ax, gx0 + j * c + c / 2, gy0 - 0.15, h, size=11.5, color=BODY)
    for i, d in enumerate(("2", "3")):
        txt(ax, gx0 - 0.12, gy0 + i * c + c / 2, f"dst_id {d}", size=11.5, color=BODY, ha="right")
        for j, h in enumerate(("h2", "h3")):
            got = mat[(d, h)]
            ax.add_patch(Rectangle((gx0 + j * c + 0.025, gy0 + i * c + 0.025), c - 0.05, c - 0.05,
                                   facecolor=GREEN if got else WHITE,
                                   edgecolor=GREEN if got else RULE, lw=0.8, zorder=3))
    txt(ax, gx0 + c, PY + 2.22, sol["verdict"], size=13, weight="bold", color=GREEN)
    lgx = gx0 + 2 * c + 0.3
    for k, (fc, ec, lab) in enumerate([(GREEN, GREEN, "received"), (WHITE, RULE, "nothing")]):
        ly = gy0 + k * c + c / 2
        ax.add_patch(Rectangle((lgx, ly - 0.11), 0.22, 0.22, facecolor=fc, edgecolor=ec,
                               lw=0.8, zorder=3))
        txt(ax, lgx + 0.32, ly, lab, size=11.5, color=MUTED, ha="left")
    kx = rx + 4.95
    txt(ax, kx, PY + 0.68, "skeleton (red arm)", size=14, weight="bold")
    box(ax, kx - 1.25, PY + 0.95, 2.5, 1.05, fill=WARN_BG, edge=WARNC, lw=1.6, r=0.06, z=2)
    txt(ax, kx, PY + 1.18, "pre-flight FAIL", size=12.5, weight="bold", color=WARNC)
    txt(ax, kx, PY + 1.49, sk["table"], size=10.5, color=INK, mono=True)
    txt(ax, kx, PY + 1.78, "not in its p4info", size=11.5, color=BODY)
    txt(ax, kx, PY + 2.22, sk["verdict"], size=13, weight="bold", color=WARNC)
    twin_ipv4_panel(ax, rx, PY + ph + 0.17, rw, PH - ph - 0.17, lr)
    save(fig, "fig_t6b_basic_tunnel_end_to_end")
    return sol, sk, topo, lr, mat


def ndt_up_left(ax, lx, a):
    """fig_t6's proxy box and the entries count under it (the proxy's own switch_state)."""
    app, rec = entries_total(a)
    fail = sum(v["fail"] for v in a["ss"].values())
    box(ax, lx + 0.25, PY + 0.6, 1.75, 1.2, fill=WHITE, edge=INK)
    txt(ax, lx + 1.125, PY + 0.95, "P4 proxy", size=14, weight="bold")
    txt(ax, lx + 1.125, PY + 1.4, "the package's\nentries", size=11, color=MUTED)
    ty = PY + 2.3
    txt(ax, lx + 0.35, ty, "table entries", size=13, ha="left", color=BODY)
    txt(ax, lx + 0.35, ty + 0.33, f"{app}/{rec} applied", size=13, ha="left", color=GREEN,
        weight="bold")
    txt(ax, lx + 1.85, ty + 0.33, f"{fail} failed", size=13, ha="left", color=MUTED)


# ---------------------------------------------------------------------------
# fig_t6c_firewall_end_to_end
# ---------------------------------------------------------------------------

def fw_tests(a):
    what, text = a["what"], a["text"]
    _, pg = section(text, r"pingall -- every ordered pair, ping -c 5 -W 2", "FW_PINGALL", what)
    m = one(r"^(\d+)% \((\d+)/(\d+) pairs at 0%, (\d+) lossy\)$", pg, "FW_PINGALL", what)
    if int(m.group(4)) != 0 or m.group(2) != m.group(3):
        stop("FW_PINGALL", f"{what}: pingall {m.group(0)}")
    n_pairs = int(m.group(3))
    heads = re.findall(r"^### \d+\. (F\d)  iperf (h\d+) -> (h\d+) \((\w+) to (\w+)\)$", text, re.M)
    if [(f, s, d) for f, s, d, _, _ in heads] != [("F1", "h1", "h3"), ("F2", "h3", "h1")]:
        stop("FW_IPERF_STEPS", f"{what}: iperf steps {heads}")
    res = {}
    for f, s, d, _, _ in heads:
        cmd, out = section(text, rf"{f}  iperf {s} -> {d} \(\w+ to \w+\)", "FW_IPERF", what)
        secs = int(one(r"iperf -c \S+ -t (\d+) on (h\d+)$", cmd, "FW_IPERF", what).group(1))
        if "server:" not in out:
            stop("FW_IPERF", f"{what}: {f} output has no server part")
        cli, srv = out.split("server:", 1)
        if not re.search(r"^Client connecting to \S+, TCP port \d+$", cli, re.M):
            stop("FW_IPERF_TCP", f"{what}: {f} is not a TCP iperf")
        tr = r"^\[\s*\d+\] [0-9.]+-[0-9.]+ sec\s+(\d+) MBytes\s+\d+ Mbits/sec$"
        c, v = re.findall(tr, cli, re.M), re.findall(tr, srv, re.M)
        if c and c == v and "connect failed" not in cli:
            res[(s, d)] = ("through", int(c[0]), secs)
        elif not c and not v and re.search(r"^tcp connect failed: Connection timed out$", cli,
                                           re.M):
            res[(s, d)] = ("timed out", None, secs)
        else:
            stop("FW_IPERF_SIDES", f"{what}: {f} client {c} / server {v} is neither a transfer "
                                   f"both sides saw nor a timed-out connect")
    if len({r[2] for r in res.values()}) != 1:
        stop("FW_IPERF", f"{what}: the two iperf runs have different durations")
    return res, n_pairs


def fig_fw(rows):
    ex = "firewall"
    sol = parse_ran(rows[(ex, "solution")], ex, "solution")
    sk = parse_ran(rows[(ex, "skeleton")], ex, "skeleton")
    topo = topology(ex, sol)
    need_rows(sol, ["iperf h1 -> h3 (internal -> external)", "iperf h3 -> h1 is blocked",
                    "the fabric still forwards (pingall)", "G1  link usage follows the iperf path"],
              "FW_VT")
    need_rows(sk, ["iperf h1 -> h3 (internal -> external)", "RED ARM: iperf h3 -> h1 must connect",
                   "the fabric forwards (pingall)"], "FW_VT")
    progs = {}
    for a in (sol, sk):
        if a["mode"] != "ndtwin":
            stop("FW_PIPES", f"{a['what']}: control plane {a['mode']}")
        ps = a["pipes"]
        odd = [s for s in ps if list(ps.values()).count(ps[s]) == 1]
        if odd != ["s1"] or ps["s1"] != "build/firewall.json" or \
                {ps[s] for s in ps if s != "s1"} != {"build/basic.json"}:
            stop("FW_PIPES", f"{a['what']}: pipelines {ps} are not firewall on s1, basic elsewhere")
        shas = {s: v["sha"] for s, v in a["ss"].items()}
        pf_sha = {lab.split()[0]: re.search(r"p4info sha256:([0-9a-f]{16})", d).group(1)
                  for s, lab, d in a["pf_rows"] if re.fullmatch(r"s\d+ pipeline", lab)
                  and re.search(r"p4info sha256:([0-9a-f]{16})", d)}
        if pf_sha != shas or len(set(shas.values())) != 2 or \
                list(shas.values()).count(shas["s1"]) != 1:
            stop("FW_SHAS", f"{a['what']}: p4info shas {shas} (pre-flight {pf_sha}) are not one "
                            f"on s1 and one on the rest")
        progs[a["what"]] = (ps, shas)
    if progs[sol["what"]] != progs[sk["what"]]:
        stop("FW_SHAS", "the two arms ran different programs")
    app, rec = entries_total(sol)
    res_sol, pairs_sol = fw_tests(sol)
    res_sk, pairs_sk = fw_tests(sk)
    if not (res_sol[("h1", "h3")][0] == "through" and res_sol[("h3", "h1")][0] == "timed out"):
        stop("FW_SOL", f"{sol['what']}: h1 -> h3 {res_sol[('h1', 'h3')]}, h3 -> h1 "
                       f"{res_sol[('h3', 'h1')]}: not 'through' then 'blocked'")
    if not all(r[0] == "through" for r in res_sk.values()):
        stop("FW_SK", f"{sk['what']}: {res_sk}: the red arm does not let both directions through")
    lr = link_reading(sol, topo)
    secs = res_sol[("h1", "h3")][2]
    print(f"[t6c] solution {sol['verdict']}: files {sol['files']}, pre-flight {sol['pf']}, claim "
          f"{sol['claim_min']} min, bmv2 x {sol['n_up']} ({sol['binary']}), programs "
          f"{progs[sol['what']]}, entries {app}/{rec} "
          f"({ {s: v['app'] for s, v in sol['ss'].items()} }), iperf {res_sol}, pingall "
          f"{pairs_sol} pairs at 0%; twin > 0 on {lr['primary']}, 0 on {lr['others']}")
    print(f"[t6c] skeleton {sk['verdict']}: iperf {res_sk}, pingall {pairs_sk} pairs at 0%")

    fig, ax = canvas(7.0)
    title(ax, "firewall, end to end on the NDTwin fabric")
    cx = steps_row(ax, [
        ("convert.py", f"{sol['files']} files"),
        ("pre-flight", f"{sol['pf']['PASS']} PASS · {sol['pf']['FAIL']} FAIL"),
        ("ndt claim", f"{sol['claim_min']}-min lease"),
        ("ndt up", f"bmv2 × {sol['n_up']}"),
        ("packet test", f"iperf × {len(res_sol)} · ping"),
        ("ndt down", "verified clean"),
        ("ndt release", "released"),
        ("arm report", "verdict table"),
    ], hot=("ndt up", "packet test"))
    lx, lw_ = 0.45, 5.75
    panel(ax, lx, PY, lw_, PH, "NDT UP")
    connector(ax, cx[3], PY)
    ndt_up_left(ax, lx, sol)
    gx, gy, gw, gh = 3.35, 3.0, 2.65, 2.35
    arrow(ax, 2.47, 3.75, gx - 0.02, 3.75, color=ACCENT, lw=1.8)
    txt(ax, (2.47 + gx) / 2, 3.55, "P4Runtime", size=11, color=ACCENT)
    ps = sol["pipes"]
    fabric(ax, gx, gy, gw, gh, topo,
           {"s3": (4.0, 4.1), "s4": (5.35, 4.1), "s1": (4.0, 4.95),
            "s2": (5.35, 4.95), "h1": 3.7, "h2": 4.3, "h3": 5.05, "h4": 5.65},
           {s: "prog" if s == "s1" else "other" for s in topo["switches"]},
           [("prog", ps["s1"]), ("other", ps["s2"])], host_y=5.95)
    rx, rw, ph = 6.55, 6.33, 2.5
    panel(ax, rx, PY, rw, ph, f"PACKET TEST · TCP iperf {secs} s each way · ping every pair")
    connector(ax, cx[4], PY)
    cols = [("solution", rx + 2.85, res_sol, pairs_sol, sol["verdict"]),
            ("skeleton (red arm)", rx + 4.95, res_sk, pairs_sk, sk["verdict"])]
    ys = [PY + 1.06, PY + 1.48, PY + 1.90]
    for lab, y in zip([f"TCP h1 → h3", f"TCP h3 → h1", f"ping, {pairs_sol} pairs"], ys):
        txt(ax, rx + 0.3, y, lab, size=12, color=BODY, ha="left")
    for name, ccx, res, pairs, verdict in cols:
        txt(ax, ccx, PY + 0.68, name, size=14, weight="bold")
        for (s, d), y in zip((("h1", "h3"), ("h3", "h1")), ys):
            kind, mb, _ = res[(s, d)]
            cell(ax, ccx, y, 1.6, 0.34, GREEN if kind == "through" else WARNC,
                 f"{mb} MBytes" if kind == "through" else "timed out")
        cell(ax, ccx, ys[2], 1.6, 0.34, GREEN, f"{pairs}/{pairs} at 0% loss")
        txt(ax, ccx, PY + 2.26, verdict, size=13, weight="bold", color=GREEN)
    twin_ipv4_panel(ax, rx, PY + ph + 0.17, rw, PH - ph - 0.17, lr)
    save(fig, "fig_t6c_firewall_end_to_end")
    return sol, sk, topo, lr, res_sol, res_sk


# ---------------------------------------------------------------------------
# fig_t6d_p4runtime_end_to_end
# ---------------------------------------------------------------------------

def p4r_controller(a):
    what = a["what"]
    log = read(os.path.join(a["dir"], "driver-controller-p4runtime.log"), "P4R_LOG", what)
    adapter = re.findall(r"^\[adapter\] (s\d+): (\S+):(\d+) device_id=(\d+)\s+->\s+(\S+):(\d+) "
                         r"device_id=(\d+)$", log, re.M)
    program = re.findall(r"^Installed P4 Program using SetForwardingPipelineConfig on (s\d+)$",
                         log, re.M)
    if not adapter or sorted(s for s, *_ in adapter) != sorted(program):
        stop("P4R_ADAPTER", f"{what}: adapter mapped {[s for s, *_ in adapter]}, the controller "
                            f"installed its program on {program}")
    if any(int(np_) != int(op) - 50051 + 30051 or int(nd) != swnum(s) for s, _, op, _, _, np_, nd
           in adapter):
        stop("P4R_ADAPTER", f"{what}: adapter mapping {adapter} is not :5005N -> :3005N, "
                            f"device id -> dpid")
    rules = re.findall(r"^Installed (ingress|transit|egress) tunnel rule on (s\d+)$", log, re.M)
    todo = re.findall(r"^TODO Install transit tunnel rule$", log, re.M)
    blocks = log.split("----- Reading tunnel counters -----")
    if len(blocks) < 2:
        stop("P4R_COUNTER", f"{what}: the controller never read its tunnel counters")
    # the last read: switch -> (tunnel id, packets) of its ingress tunnel counter
    ingress = {}
    for sw, tid, pk in re.findall(r"^(s\d+) MyIngress\.ingressTunnelCounter (\d+): (\d+) packets "
                                  r"\(\d+ bytes\)$", blocks[-1], re.M):
        if sw in ingress:
            stop("P4R_COUNTER", f"{what}: two ingress counters on {sw} in the last read")
        ingress[sw] = (int(tid), int(pk))
    cmd = one(r"^\[adapter\] running\s+(\S+)", log, "P4R_ADAPTER", what).group(1)
    return dict(adapter=adapter, programmed=sorted(program, key=swnum), rules=rules, todo=todo,
                ingress=ingress, controller=cmd)


def p4r_ping(a):
    _, out = section(a["text"], r"P1  h1 ping h2 with the controller running", "P4R_PING",
                     a["what"])
    m = one(r"^(\d+) packets transmitted, (\d+) received, (\d+)% packet loss", out, "P4R_PING",
            a["what"])
    return int(m.group(1)), int(m.group(2))


def fig_p4r(rows):
    ex = "p4runtime"
    sol = parse_ran(rows[(ex, "solution")], ex, "solution")
    sk = parse_ran(rows[(ex, "skeleton")], ex, "skeleton")
    topo = topology(ex, sol)
    need_rows(sol, ["switches the controller programmed", "the transit rule went in",
                    "h1 -> h2 forwards through the tunnel", "G1  link usage follows the iperf path"],
              "P4R_VT")
    need_rows(sk, ["switches the controller programmed",
                   "RED ARM: the transit rule is still the student's TODO",
                   "RED ARM: h1 -> h2 does not forward"], "P4R_VT")
    for a in (sol, sk):
        if a["mode"] != "external":
            stop("P4R_MODE", f"{a['what']}: control plane {a['mode']}, not external")
        if any(v["rec"] for v in a["ss"].values()):
            stop("P4R_NDTWIN_ENTRIES", f"{a['what']}: NDTwin recorded entries on an external "
                                       f"fabric: {a['ss']}")
        if not re.search(r"ok\s+proxy: \d+/\d+ switches answered the liveness probe \(no pipeline "
                         r"loaded on any of them, by design\)", a["up"]):
            stop("P4R_EMPTY", f"{a['what']}: ndt up does not say it loaded no pipeline")
        if "its own controller owns every table and this proxy writes nothing" not in a["text"]:
            stop("P4R_WRITES", f"{a['what']}: switch_state does not say the proxy writes nothing")
    c_sol, c_sk = p4r_controller(sol), p4r_controller(sk)
    if c_sol["programmed"] != c_sk["programmed"]:
        stop("P4R_ADAPTER", f"the arms' controllers programmed {c_sol['programmed']} vs "
                            f"{c_sk['programmed']}")
    prog = c_sol["programmed"]
    empty = [s for s in topo["switches"] if s not in prog]
    if not empty or not set(prog) < set(topo["switches"]):
        stop("P4R_ADAPTER", f"programmed {prog} of {topo['switches']}")
    tr_sol = sorted(s for k, s in c_sol["rules"] if k == "transit")
    tr_sk = sorted(s for k, s in c_sk["rules"] if k == "transit")
    if tr_sol != prog or c_sol["todo"]:
        stop("P4R_SOL_TRANSIT", f"{sol['what']}: transit rules on {tr_sol}, TODO lines "
                                f"{len(c_sol['todo'])}")
    if tr_sk or len(c_sk["todo"]) != len(prog):
        stop("P4R_SK_TRANSIT", f"{sk['what']}: transit rules on {tr_sk}, TODO lines "
                               f"{len(c_sk['todo'])}")
    tx_sol, rx_sol = p4r_ping(sol)
    tx_sk, rx_sk = p4r_ping(sk)
    if rx_sol != tx_sol or rx_sk != 0:
        stop("P4R_PING_RESULT", f"solution {rx_sol}/{tx_sol}, skeleton {rx_sk}/{tx_sk}")
    lr = link_reading(sol, topo)
    sw_side = [i for i in lr["primary"] if lr["types"][i] == "switch"]
    host_side = [i for i in lr["primary"] if lr["types"][i] == "host"]
    if len(sw_side) != 1 or len(host_side) != 1:
        stop("P4R_PRIMARY", f"{sol['what']}: on-path {lr['primary']} is not one switch-facing and "
                            f"one host-facing interface")
    onp = read(os.path.join(sol["dir"], "link_usage/onpath.txt"), "P4R_BYTES", sol["what"])
    by = {i: int(b) for i, b in re.findall(r"^(s\d+-eth\d+) P (\d+)$", onp, re.M)}
    if sorted(by) != sorted(lr["primary"]):
        stop("P4R_BYTES", f"{sol['what']}: onpath.txt interfaces {sorted(by)} vs {lr['primary']}")
    ipc = read(os.path.join(sol["dir"], "link_usage/iperf_client.txt"), "P4R_BYTES", sol["what"])
    sent = int(one(r"Sent (\d+) datagrams", ipc, "P4R_BYTES", sol["what"]).group(1))
    p4 = read(os.path.join(TUT, "exercises/p4runtime/advanced_tunnel.p4"), "P4R_HEADER", ex)
    hm = one(r"header myTunnel_t \{\s*bit<(\d+)> proto_id;\s*bit<(\d+)> dst_id;\s*\}", p4,
             "P4R_HEADER", ex)
    hdr = (int(hm.group(1)) + int(hm.group(2))) // 8
    etype = one(r"^const bit<16> TYPE_MYTUNNEL = (0x[0-9A-Fa-f]+);$", p4, "P4R_HEADER",
                ex).group(1)
    in_sw = sw_side[0].split("-")[0]
    if in_sw not in c_sol["ingress"]:
        stop("P4R_COUNTER", f"{sol['what']}: no ingress tunnel counter on {in_sw} in the last read "
                            f"({c_sol['ingress']})")
    tid, pkts = c_sol["ingress"][in_sw]
    diff = by[sw_side[0]] - by[host_side[0]]
    if diff != sent * hdr:
        stop("P4R_BYTES", f"{sw_side[0]} {by[sw_side[0]]} B - {host_side[0]} {by[host_side[0]]} B "
                          f"= {diff}, not {sent} datagrams x {hdr} B")
    n_rules = len(c_sol["rules"])
    print(f"[t6d] solution {sol['verdict']}: files {sol['files']}, pre-flight {sol['pf']}, claim "
          f"{sol['claim_min']} min, bmv2 x {sol['n_up']} ({sol['binary']}), NDTwin entries "
          f"{sum(v['rec'] for v in sol['ss'].values())}; controller {c_sol['controller']} via "
          f"adapter {[(s, f'{op}->{np_}') for s, _, op, _, _, np_, _ in c_sol['adapter']]}, "
          f"programmed {prog}, rules {c_sol['rules']}; ping {rx_sol}/{tx_sol}; last ingress "
          f"counters {c_sol['ingress']}; {sw_side[0]} - {host_side[0]} = {diff} B = {sent} x "
          f"{hdr} B ({etype} header); twin "
          f"{sw_side[0]} {lr['vals'][sw_side[0]]:.0f} bit")
    print(f"[t6d] skeleton {sk['verdict']}: rules {c_sk['rules']}, TODO {len(c_sk['todo'])}, ping "
          f"{rx_sk}/{tx_sk}, last ingress counters {c_sk['ingress']}")

    fig, ax = canvas(7.0)
    title(ax, "p4runtime, end to end on the NDTwin fabric")
    cx = steps_row(ax, [
        ("convert.py", f"{sol['files']} files"),
        ("pre-flight", f"{sol['pf']['PASS']} PASS · {sol['pf']['FAIL']} FAIL"),
        ("ndt claim", f"{sol['claim_min']}-min lease"),
        ("ndt up", f"bmv2 × {sol['n_up']}"),
        ("controller", f"{n_rules} tunnel rules"),
        ("packet test", f"ping × {tx_sol}"),
        ("ndt down", "verified clean"),
        ("ndt release", "released"),
    ], hot=("ndt up", "controller", "packet test"))
    # ---- left: ndt up, then the exercise's own controller through NDTwin's adapter
    lx, lw_ = 0.45, 7.6
    panel(ax, lx, PY, lw_, PH, "NDT UP, THEN THE EXERCISE'S CONTROLLER")
    connector(ax, cx[3], PY)
    connector(ax, cx[4], PY)
    bx, bw_ = lx + 0.2, 1.75
    box(ax, bx, PY + 0.55, bw_, 0.9, fill=WHITE, edge=INK)
    txt(ax, bx + bw_ / 2, PY + 0.85, "P4 proxy", size=14, weight="bold")
    txt(ax, bx + bw_ / 2, PY + 1.17, "writes nothing", size=11, color=MUTED)
    cy0 = PY + 1.8
    box(ax, bx, cy0, bw_, 0.9, fill=WHITE, edge=INK)
    txt(ax, bx + bw_ / 2, cy0 + 0.32, os.path.basename(c_sol["controller"]), size=12,
        weight="bold", mono=True)
    txt(ax, bx + bw_ / 2, cy0 + 0.64, "the exercise's own", size=11, color=MUTED)
    ax_, aw = bx + bw_ + 0.3, 1.45
    box(ax, ax_, cy0, aw, 0.9, fill=ACCENT_BG, edge=ACCENT, lw=2.0)
    txt(ax, ax_ + aw / 2, cy0 + 0.32, "adapter", size=14, weight="bold", color=ACCENT)
    op, np_ = c_sol["adapter"][0][2], c_sol["adapter"][0][5]
    txt(ax, ax_ + aw / 2, cy0 + 0.64, f":{op} → :{np_}", size=10.5, color=MUTED, mono=True)
    arrow(ax, bx + bw_ + 0.02, cy0 + 0.45, ax_ - 0.02, cy0 + 0.45, color=INK, lw=1.6)
    gx, gy, gw, gh = 5.0, 3.0, 2.9, 2.35
    arrow(ax, ax_ + aw + 0.02, cy0 + 0.45, gx - 0.02, cy0 + 0.45, color=ACCENT, lw=1.8)
    txt(ax, (ax_ + aw + gx) / 2, cy0 + 0.25, "P4Runtime", size=11, color=ACCENT)
    fabric(ax, gx, gy, gw, gh, topo,
           {"s1": (5.75, 4.1), "s2": (7.15, 4.1), "s3": (6.45, 4.95),
            "h1": 5.75, "h2": 7.15, "h3": 6.45},
           {s: "prog" if s in prog else "empty" for s in topo["switches"]},
           [("prog", sol["pipes"][prog[0]]), ("empty", "no program")], host_y=5.95)
    ty = PY + 3.1
    txt(ax, bx + 0.1, ty, "tunnel rules", size=13, ha="left", color=BODY)
    txt(ax, bx + 0.1, ty + 0.36, f"{n_rules} installed", size=13, ha="left", color=GREEN,
        weight="bold")
    txt(ax, ax_, ty, "NDTwin's entries", size=13, ha="left", color=BODY)
    txt(ax, ax_, ty + 0.36, f"{sum(v['rec'] for v in sol['ss'].values())}", size=13,
        ha="left", color=MUTED, weight="bold")
    # ---- right: packet test (both arms), then the twin's reading of the solution's iperf
    rx, rw, ph = 8.3, 12.88 - 8.3, 2.1
    panel(ax, rx, PY, rw, ph, f"PACKET TEST · h1 ping h2, {tx_sol} packets")
    connector(ax, cx[5], PY)
    c1, c2 = rx + 1.95, rx + 3.5
    ys = [PY + 1.05, PY + 1.47]
    for lab, y in zip(["transit rule", "replies"], ys):
        txt(ax, rx + 0.2, y, lab, size=12, color=BODY, ha="left")
    for name, ccx, ok_rule, rx_, verdict in (("solution", c1, True, rx_sol, sol["verdict"]),
                                             ("skeleton (red arm)", c2, False, rx_sk,
                                              sk["verdict"])):
        txt(ax, ccx, PY + 0.66, name, size=14, weight="bold")
        cell(ax, ccx, ys[0], 1.3, 0.34, GREEN if ok_rule else WARNC,
             f"on {len(prog)} switches" if ok_rule else "TODO")
        cell(ax, ccx, ys[1], 1.3, 0.34, GREEN if rx_ else WARNC, f"{rx_}/{tx_sol}")
        txt(ax, ccx, PY + 1.86, verdict, size=13, weight="bold", color=GREEN)
    ty2 = PY + ph + 0.17
    th = PH - ph - 0.17
    panel(ax, rx, ty2, rw, th, f"TWIN LINK READING · UDP iperf {lr['src']} → {lr['dst']}")
    rows_ = [(f"{sw_side[0]} − {host_side[0]}", f"+{num(diff)} B"),
             (f"twin on {sw_side[0]}", "> 0"),
             (f"{in_sw} tunnel counter {tid}", f"{num(pkts)} pkts")]
    for k, (lab, val) in enumerate(rows_):
        y = ty2 + 0.6 + k * 0.27
        txt(ax, rx + 0.25, y, lab, size=12, color=BODY, ha="left")
        txt(ax, rx + rw - 0.25, y, val, size=12, color=INK, weight="bold", ha="right")
    iy = ty2 + th - 0.3
    chip(ax, rx + 0.25, iy, 1.25, GREY, INK, "INFERRED")
    txt(ax, rx + 1.65, iy, f"= {num(sent)} × {hdr} B: the {etype} frames", size=12, color=BODY,
        ha="left")
    save(fig, "fig_t6d_p4runtime_end_to_end")
    return sol, sk, topo, lr, c_sol, c_sk


def main():
    rows = t06_rows()
    fig_bt(rows)
    fig_fw(rows)
    fig_p4r(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
