#!/usr/bin/env python3
"""
make_exercise_path_figs.py -- four P4-tutorial figures of the 2026-09-30 report.

    fig_t6_multicast_end_to_end   one exercise, every step, from the two T06 multicast arm reports
    fig_t7_preflight_checks       what pre-flight checks, counted from 26 real pre-flight outputs,
                                  and the one real refusal (basic_tunnel skeleton)
    fig_t8_what_you_bring         what an exercise brings, what convert.py adds (basic/solution)
    fig_t9_custom_headers         the seven custom-header exercises: they forward; whether the
                                  twin's link reading covered their own frames

Data (read at run time; every number on a canvas is parsed, and what it relies on is asserted):
  T06 = doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/2026-09-27T074635Z_06_thirteen
        /00_table.tsv and the 26 arm reports it names (runs/<UTC>_<exercise>_<arm>_ndtwin.md),
        trunk 5dc7fc9a per their `ndt status` code line;
  07  = live-p1/runs/2026-09-26T202055Z_07_roles_basic/12_preflight_basic_roles.txt (b2eeb71d);
  code = tools/p4_exercise/{preflight,convert}.py at trunk fed37cff (identical to 3d740be0 for
        these files); GAP-1-exercise-requirements.md and GAP-ANALYSIS.md at 532b6c31.
  The raw read here (T06, its 26 arm reports with their link_usage/, and 07) is not tracked by
  the kernel checkout; the same files are in audit-raw 797c34ab (690 files compared by blob hash,
  all identical).  The arm reports ran on a dirty checkout: T06's code line is "5dc7fc9a +95
  file(s) with uncommitted changes".  GAP-2b is uncommitted (pending Adam's review).

Architecture boxes (fig_t8) name strings asserted to exist in convert.py; the group assignment of
fig_t7 is this script's judgement (GROUPS below) and every observed label must fall in a group.

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/p4-tutorials"
    nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_exercise_path_figs.py
"""
import collections
import csv
import json
import os
import re
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
PREP = os.path.join(REPO, "doc/audit/2026-09-04_p4-tutorial-exercise-prep")
T06 = os.path.join(PREP, "live-p1/runs/2026-09-27T074635Z_06_thirteen/00_table.tsv")
PRE07 = os.path.join(PREP, "live-p1/runs/2026-09-26T202055Z_07_roles_basic/"
                           "12_preflight_basic_roles.txt")
GAP1 = os.path.join(PREP, "GAP-1-exercise-requirements.md")
GAPA = os.path.join(PREP, "GAP-ANALYSIS.md")
GAP2B = os.path.join(PREP, "GAP-2b-ndtwin-p4-capabilities-2026-09-27.md")
PREFLIGHT = os.path.join(REPO, "tools/p4_exercise/preflight.py")
CONVERT = os.path.join(REPO, "tools/p4_exercise/convert.py")
# the tutorials checkout the arms ran (c80d83e); read only for the tunnel header's width
TUNNEL_P4 = "/home/adam/tutorials/exercises/p4runtime/advanced_tunnel.p4"

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
WARNC, WARN_BG, WHITE = "#9C3B2E", "#FBF2F0", "#FFFFFF"
GREEN, AMBER, GREY = "#2F7D4F", "#E3A21A", "#C9CDD0"
W = 13.33


def die(msg):
    raise SystemExit(f"make_exercise_path_figs: {msg}")


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def save(fig, name):
    os.makedirs(HIRES, exist_ok=True)
    for ext in ("pdf", "png", "svg"):
        kw = {"dpi": 300} if ext == "png" else {}
        fig.savefig(os.path.join(OUTDIR, f"{name}.{ext}"), facecolor=WHITE, **kw)
    fig.savefig(os.path.join(HIRES, f"{name}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"[out] {name}.{{pdf,png,svg}} + _hires/{name}.png")


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


def arrow(ax, x0, y0, x1, y1, color=INK, lw=1.4, ls="solid", z=3, both=False, rad=None):
    kw = {"connectionstyle": f"arc3,rad={rad}"} if rad else {}
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="<|-|>" if both else "-|>",
                                 mutation_scale=13, color=color, lw=lw, linestyle=ls,
                                 shrinkA=0, shrinkB=0, zorder=z, **kw))


def title(ax, s):
    if len(s) > 45:
        die(f"title over 45 characters: {s!r}")
    txt(ax, 0.45, 0.48, s, size=22, weight="bold", ha="left")


# ---------------------------------------------------------------------------
# shared parsing
# ---------------------------------------------------------------------------

def t06_rows():
    with open(T06, newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    if len(rows) != 26:
        die(f"{T06}: {len(rows)} rows, not 26")
    return {(r["exercise"], r["which"]): r for r in rows}


def code_line(lines):
    for ln in lines:
        m = re.match(r"^\s+code\s+([0-9a-f]{7,40})\b", ln)
        if m:
            return m.group(1)
    return None


def preflight_blocks(lines):
    """Every pre-flight block in a text: [(rows, end_line)], rows = [(status, label, detail)].

    A row is `  STATUS  <label padded>  <detail>` (preflight.py Report.render); a FAIL row with
    an empty label continues the check above it (preflight.py:1137-1142)."""
    out, cur = [], None
    for ln in lines:
        if ln.startswith("pre-flight: "):
            cur = []
            continue
        if cur is None:
            continue
        if ln.startswith("PASS --") or ln.startswith("FAIL --"):
            out.append((cur, ln))
            cur = None
            continue
        m = re.match(r"^  (PASS|FAIL|INFO)  (.*)$", ln)
        if not m:
            continue
        status, rest = m.group(1), m.group(2)
        if rest.startswith(" "):
            label, detail = "", rest.strip()
        else:
            parts = re.split(r"\s{2,}", rest.strip(), maxsplit=1)
            label, detail = parts[0], (parts[1] if len(parts) > 1 else "")
        cur.append((status, label, detail))
    return out


def first_preflight(path):
    blocks = preflight_blocks(read(path).splitlines())
    if not blocks:
        return None
    rows, end = blocks[0]
    for other, oend in blocks[1:]:
        if [(s, l) for s, l, _ in other] != [(s, l) for s, l, _ in rows] or oend != end:
            die(f"{path}: two pre-flight blocks disagree")
    return rows, end


# ---------------------------------------------------------------------------
# fig_t6_multicast_end_to_end
# ---------------------------------------------------------------------------

def one(pattern, text, what, flags=re.M):
    m = re.search(pattern, text, flags)
    if not m:
        die(f"{what}: /{pattern}/ not found")
    return m


def section(text, head, what):
    """The first fenced output block after the heading line `head` (the step's raw output)."""
    i = text.find(head)
    if i < 0:
        die(f"{what}: no section {head!r}")
    blocks = re.findall(r"```\n(.*?)```", text[i:], re.S)
    if len(blocks) < 2:
        die(f"{what}: section {head!r} has no output block")
    return blocks[1]            # [0] is the command, [1] its output


def ping_matrix(text, what):
    """pingall -> {(src, dst): loss%} from the step-8 output; unlisted pairs are the 0% ones."""
    out = section(text, "pingall -- every ordered pair", what)
    m = one(r"^(\d+)% \((\d+)/(\d+) pairs at 0%, (\d+) lossy\)$", out, what)
    n_zero, n_pairs, n_lossy = int(m.group(2)), int(m.group(3)), int(m.group(4))
    hosts = [h.strip() for h in one(r"^hosts\s+:\s+(.+)$", text, what).group(1).split(",")]
    if n_pairs != len(hosts) * (len(hosts) - 1) or n_zero + n_lossy != n_pairs:
        die(f"{what}: pingall summary {m.group(0)} does not add up over hosts {hosts}")
    lossy = {}
    for a, b, loss, got, sent in re.findall(
            r"^(h\d+) -> (h\d+) \([0-9.]+\): (\d+)% loss, (\d+)/(\d+) received$", out, re.M):
        lossy[(a, b)] = (int(loss), int(got), int(sent))
    if len(lossy) != n_lossy:
        die(f"{what}: {len(lossy)} lossy lines, summary says {n_lossy}")
    mat = {}
    for a in hosts:
        for b in hosts:
            if a != b:
                mat[(a, b)] = lossy[(a, b)][0] if (a, b) in lossy else 0
    return hosts, mat, (n_zero, n_pairs)


def verdict_table(text, what):
    sec = text[text.find("## 5. 判定表"):]
    rows = re.findall(r"^\| (PASS|FAIL) \| ([^|]+) \|", sec, re.M)
    if not rows:
        die(f"{what}: no verdict table")
    return [(a, b.strip()) for a, b in rows]


def switch_state(text, what):
    blk = section(text, "N4  GET /p4/switch_state", what)
    return json.loads(blk)


def parse_arm(path, which):
    what = os.path.basename(path)
    text = read(path)
    lines = text.splitlines()
    a = {"path": path, "code": code_line(lines)}
    a["verdict"] = one(r"^\| 判定 \| \*\*(.+?)\*\* \(exit (\d+)\) \|$", text, what).group(1)
    conv = section(text, "N1  convert.py", what)
    a["files"] = int(one(r"^\s+files\s+:\s+(\d+)$", conv, what).group(1))
    a["pipeline"] = one(r"^\s+pipelines\s+:\s+s1=(\S+)$", conv, what).group(1)
    pf = first_preflight(path)
    if pf is None:
        die(f"{what}: no pre-flight block")
    cnt = collections.Counter(s for s, _, _ in pf[0])
    a["pf"] = (cnt["PASS"], cnt["INFO"], cnt["FAIL"], pf[1])
    a["claim_min"] = int(one(r"ok\s+lab claimed by \S+ for (\d+)m", text, what).group(1))
    up = section(text, "N3  ndt up p4 --app", what)
    m = one(r"ok\s+(\d+) switches up after (\d+)s", up, what)
    a["n_switches"] = int(m.group(1))
    a["binary"] = one(r"ok\s+running binary: (\S+)", up, what).group(1)
    m = one(r"ok\s+table entries: (\d+)/(\d+) applied on (\d+) switch\(es\), (\d+) failed",
            up, what)
    a["entries"] = tuple(int(g) for g in m.groups())
    st = switch_state(text, what)
    sw = st["switches"]["1"]
    a["pipeline_is_ndtwin"] = sw["pipeline"]["ndtwin"]
    a["mcast"] = sw["pre_entries"]["multicast"]
    a["tbl"] = sw["table_entries"]
    a["hosts"], a["ping"], a["zero_pairs"] = ping_matrix(text, what)
    a["vt"] = verdict_table(text, what)
    down = section(text, "N9  ndt down", what) if which == "solution" else None
    a["down_rc"] = int(one(r"ndt down rc=(\d+)", text, what).group(1))
    a["release_rc"] = int(one(r"ndt release rc=(\d+)", text, what).group(1))
    if "ok  lab released" not in text:
        die(f"{what}: no 'ok  lab released'")
    if down is not None and not re.search(r"^clean$", down, re.M):
        die(f"{what}: ndt down has no 'clean' section")
    a["down_clean"] = down is not None
    return a


def fig_t6(rows):
    sol_row, sk_row = rows[("multicast", "solution")], rows[("multicast", "skeleton")]
    sol, sk = parse_arm(sol_row["report"], "solution"), parse_arm(sk_row["report"], "skeleton")
    # the table and the reports must agree
    for row, a in ((sol_row, sol), (sk_row, sk)):
        if row["verdict"] != a["verdict"] or int(row["rc"]) != 0:
            die(f"T06 row {row['which']} {row['verdict']}/{row['rc']} vs report {a['verdict']}")
        if a["code"] != "5dc7fc9a":
            die(f"{a['path']} ran on {a['code']}, not 5dc7fc9a")
    # what the solution arm's verdict table asserts, and that the ping matrix says the same
    vt = dict((b, s) for s, b in sol["vt"])
    for need in ("h1/h2/h3 reach each other", "nobody reaches h4", "but h4 reaches them"):
        if vt.get(need) != "PASS":
            die(f"multicast/solution verdict row {need!r} is {vt.get(need)}")
    m = sol["ping"]
    inner = [(a, b) for a in ("h1", "h2", "h3") for b in ("h1", "h2", "h3") if a != b]
    if any(m[p] != 0 for p in inner) or any(m[(a, "h4")] != 100 for a in ("h1", "h2", "h3")) \
            or any(m[("h4", b)] != 0 for b in ("h1", "h2", "h3")):
        die(f"multicast/solution ping matrix is not h1-h3 mutual / h4 unreached: {m}")
    if any(v != 100 for v in sk["ping"].values()):
        die("multicast/skeleton: some pair got through")
    for a in (sol, sk):
        if a["entries"][0] != a["entries"][1] or a["entries"][3] != 0:
            die(f"{a['path']}: entries {a['entries']}")
        if a["mcast"]["applied"] != a["mcast"]["recorded"] or a["mcast"]["failed"] != 0:
            die(f"{a['path']}: multicast group {a['mcast']}")
        if a["pipeline_is_ndtwin"] is not False:
            die(f"{a['path']}: s1 did not run the package's own program")
        if a["pf"][2] != 0 or not a["pf"][3].startswith("PASS --"):
            die(f"{a['path']}: pre-flight {a['pf']}")
        if a["down_rc"] != 0 or a["release_rc"] != 0:
            die(f"{a['path']}: down/release rc {a['down_rc']}/{a['release_rc']}")
    print(f"[t6] solution {sol['verdict']}: files {sol['files']}, pre-flight PASS {sol['pf'][0]} "
          f"INFO {sol['pf'][1]} FAIL {sol['pf'][2]}, claim {sol['claim_min']} min, bmv2 x "
          f"{sol['n_switches']} ({sol['binary']}) running {sol['pipeline']}, entries "
          f"{sol['entries']}, multicast {sol['mcast']}, pairs at 0% {sol['zero_pairs']}")
    print(f"[t6] skeleton {sk['verdict']}: entries {sk['entries']}, multicast {sk['mcast']}, "
          f"pairs at 0% {sk['zero_pairs']}")

    H = 7.0
    fig, ax = canvas(H)
    title(ax, "multicast, end to end on the NDTwin fabric")
    n_pairs = sol["zero_pairs"][1]
    steps = [
        ("convert.py", f"{sol['files']} files"),
        ("pre-flight", f"{sol['pf'][0]} PASS · {sol['pf'][2]} FAIL"),
        ("ndt claim", f"{sol['claim_min']}-min lease"),
        ("ndt up", f"bmv2 × {sol['n_switches']}"),
        ("packet test", f"{n_pairs} host pairs"),
        ("ndt down", "verified clean"),
        ("ndt release", "released"),
        ("arm report", "verdict table"),
    ]
    x0, y0, bw, bh, gap = 0.45, 1.00, 1.36, 0.92, 0.221
    cx = []
    for i, (a, b) in enumerate(steps):
        x = x0 + i * (bw + gap)
        hot = a in ("ndt up", "packet test")
        box(ax, x, y0, bw, bh, fill=ACCENT_BG if hot else WHITE, edge=ACCENT if hot else INK,
            lw=2.2 if hot else 1.2)
        txt(ax, x + bw / 2, y0 + 0.32, a, size=13.5, weight="bold", color=ACCENT if hot else INK)
        txt(ax, x + bw / 2, y0 + 0.64, b, size=11.5, color=MUTED)
        cx.append(x + bw / 2)
        if i:
            arrow(ax, x - gap + 0.02, y0 + bh / 2, x - 0.02, y0 + bh / 2)

    # ---- left panel: what ndt up put on the fabric
    py = 2.55
    lx, lw_, lh = 0.45, 5.75, 4.05
    box(ax, lx, py, lw_, lh, fill=PANEL, edge=RULE, lw=1.0, r=0.08, z=1)
    ax.plot([cx[3], cx[3]], [y0 + bh, py], color=ACCENT, lw=1.8, ls=(0, (4, 3)), zorder=1)
    txt(ax, lx + 0.2, py + 0.28, "NDT UP", size=11.5, color=FAINT, weight="bold", ha="left")
    # proxy
    box(ax, lx + 0.3, py + 0.6, 1.95, 1.2, fill=WHITE, edge=INK)
    txt(ax, lx + 1.275, py + 0.95, "P4 proxy", size=14, weight="bold")
    txt(ax, lx + 1.275, py + 1.4, "the package's\nentries + group", size=11, color=MUTED)
    # switch
    sx, sy, sw_, sh = lx + 3.3, py + 0.6, 2.2, 1.2
    box(ax, sx, sy, sw_, sh, fill=WHITE, edge=ACCENT, lw=2.0)
    txt(ax, sx + sw_ / 2, sy + 0.35, "s1 · bmv2", size=14, weight="bold", color=ACCENT)
    txt(ax, sx + sw_ / 2, sy + 0.8, sol["pipeline"], size=11, color=MUTED, mono=True)
    arrow(ax, lx + 2.27, sy + 0.6, sx - 0.02, sy + 0.6, color=ACCENT, lw=1.8)
    txt(ax, (lx + 2.27 + sx) / 2, sy + 0.40, "P4Runtime", size=11, color=ACCENT)
    # the two counts the proxy reported, under the proxy
    ty = py + 2.3
    tbl, mc = sol["tbl"], sol["mcast"]
    for k, (name, applied, recorded, failed) in enumerate([
            ("table entries", tbl["applied"], tbl["recorded"], tbl["failed"]),
            ("multicast group", mc["applied"], mc["recorded"], mc["failed"])]):
        yy = ty + k * 0.78
        txt(ax, lx + 0.35, yy, name, size=13, ha="left", color=BODY)
        txt(ax, lx + 0.35, yy + 0.33, f"{applied}/{recorded} applied", size=13, ha="left",
            color=GREEN, weight="bold")
        txt(ax, lx + 1.85, yy + 0.33, f"{failed} failed", size=13, ha="left", color=MUTED)
    # hosts on s1's four ports
    hy = py + 2.75
    hs = sol["hosts"]
    for k, h in enumerate(hs):
        hx = sx + 0.3 + k * (sw_ - 0.6) / (len(hs) - 1)
        ax.plot([hx, hx], [sy + sh + 0.02, hy - 0.2], color=MUTED, lw=1.2, zorder=1)
        box(ax, hx - 0.25, hy - 0.2, 0.5, 0.4, fill=WHITE, edge=MUTED, lw=1.0, r=0.04)
        txt(ax, hx, hy, h, size=11.5, color=BODY)

    # ---- right panel: the packet test, both arms
    rx, rw = 6.55, 6.33
    box(ax, rx, py, rw, lh, fill=PANEL, edge=RULE, lw=1.0, r=0.08, z=1)
    ax.plot([cx[4], cx[4]], [y0 + bh, py], color=ACCENT, lw=1.8, ls=(0, (4, 3)), zorder=1)
    txt(ax, rx + 0.2, py + 0.28, "PACKET TEST · ping every pair", size=11.5, color=FAINT,
        weight="bold", ha="left")
    cell = 0.42
    for j, (arm, a, head) in enumerate([("solution", sol, sol["verdict"]),
                                        ("skeleton (red arm)", sk, sk["verdict"])]):
        mx = rx + 0.95 + j * 3.1
        my = py + 1.25
        txt(ax, mx + 2 * cell, py + 0.72, arm, size=14, weight="bold")
        for i, src in enumerate(a["hosts"]):
            txt(ax, mx - 0.12, my + i * cell + cell / 2, src, size=11.5, color=BODY, ha="right")
            for k, dst in enumerate(a["hosts"]):
                if i == 0:
                    txt(ax, mx + k * cell + cell / 2, my - 0.14, dst, size=11.5, color=BODY)
                if src == dst:
                    fc, ec = WHITE, RULE
                else:
                    loss = a["ping"][(src, dst)]
                    fc = GREEN if loss == 0 else WARNC if loss == 100 else AMBER
                    ec = fc
                ax.add_patch(Rectangle((mx + k * cell + 0.025, my + i * cell + 0.025),
                                       cell - 0.05, cell - 0.05, facecolor=fc, edgecolor=ec,
                                       lw=0.8, zorder=3))
        txt(ax, mx + 2 * cell, my + 4 * cell + 0.3, head, size=13, weight="bold",
            color=GREEN)
    # legend
    ly = py + lh - 0.35
    for k, (fc, lab) in enumerate([(GREEN, "0% loss"), (WARNC, "100% loss")]):
        lxx = rx + 0.95 + k * 1.9
        ax.add_patch(Rectangle((lxx, ly - 0.11), 0.24, 0.22, facecolor=fc, edgecolor=fc,
                               zorder=3))
        txt(ax, lxx + 0.34, ly, lab, size=12, color=MUTED, ha="left")
    txt(ax, rx + 0.95 + 3.75, ly, "from row to column", size=12, color=MUTED, ha="left")
    save(fig, "fig_t6_multicast_end_to_end")
    return sol, sk


# ---------------------------------------------------------------------------
# fig_t7_preflight_checks
# ---------------------------------------------------------------------------

# the group assignment is a judgement (stated in the .md); order follows run() in preflight.py
GROUPS = [
    ("package & control plane",
     ["format", "name", "control_plane.mode", "control_plane.grpc_base",
      "control_plane.device_id", "control_plane.election_id", "bmv2.cpu_port",
      "switches keys", "switches name", "referenced files"]),
    ("topology agrees",
     ["topo_from_json.switches", "topo_from_json.hosts", "topo_from_json.switch_links",
      "topo_from_json.host_links", "switches agree", "links agree",
      "hosts named h<last octet>", "hosts agree"]),
    ("pipeline & p4info",
     ["switches pipeline", "sN pipeline", "p4info parses", "telemetry.source"]),
    ("entries",
     ["entries", "entries match p4info", "entries p4info is the pipeline's", "PRE entries"]),
    ("roles",
     ["roles.ipv4_route resolves", "owned table has no package entries",
      "owned table default action", "roles suggestion"]),
    ("ports & compile", ["gRPC port block", "p4c-bm2-ss"]),
]


def norm_label(label):
    return "sN pipeline" if re.fullmatch(r"s\d+ pipeline", label) else label


def collect_preflights(rows):
    outs = {}
    for (ex, which), r in rows.items():
        pf = first_preflight(r["report"])
        if pf is None:
            continue
        outs[f"{ex}/{which}"] = pf
    pf07 = preflight_blocks(read(PRE07).splitlines())
    if len(pf07) != 1:
        die(f"{PRE07}: {len(pf07)} pre-flight blocks")
    outs["07 basic_roles"] = pf07[0]
    return outs


def fig_t7(rows):
    outs = collect_preflights(rows)
    missing = sorted(f"{e}/{w}" for (e, w) in rows if f"{e}/{w}" not in outs)
    if missing != ["flowcache/skeleton"]:
        die(f"arms without a pre-flight block: {missing} (expected only flowcache/skeleton, "
            f"refused by p4c before convert)")
    if len(outs) != 26:
        die(f"{len(outs)} pre-flight outputs")
    # per check label: {status: number of outputs}; continuation FAIL rows fold into the check
    per = collections.defaultdict(collections.Counter)
    passes = {}
    for name, (prow, end) in outs.items():
        seen = {}
        last = None
        for status, label, detail in prow:
            if label == "":
                if status != "FAIL" or last is None:
                    die(f"{name}: an unlabelled {status} row with nothing above it")
                continue
            lab = norm_label(label)
            last = lab
            prev = seen.get(lab)
            # a label seen twice in one output (sN pipeline) counts once, worst status wins
            rank = {"FAIL": 2, "PASS": 1, "INFO": 0}
            if prev is None or rank[status] > rank[prev]:
                seen[lab] = status
        for lab, status in seen.items():
            per[lab][status] += 1
        passes[name] = sum(1 for s, l, _ in prow if s == "PASS")
    grouped = {l for _, ls in GROUPS for l in ls}
    extra = sorted(set(per) - grouped)
    if extra:
        die(f"observed pre-flight labels not in any group: {extra}")
    src = read(PREFLIGHT)
    for _, ls in GROUPS:
        for l in ls:
            needle = '"{} pipeline"' if l == "sN pipeline" else f'"{l}"'
            if l == "sN pipeline":
                if 'f"{where} pipeline"' not in src:
                    die("preflight.py no longer writes the per-switch pipeline INFO row")
            elif l.startswith("topo_from_json."):
                if ('f"topo_from_json.{name}"' not in src or
                        f'"{l.split(".", 1)[1]}"' not in src):
                    die(f"preflight.py no longer writes {l!r}")
            elif needle not in src:
                die(f"preflight.py no longer has the label {l!r}")
    t06_pass = sorted(v for k, v in passes.items() if k != "07 basic_roles"
                      and not outs[k][1].startswith("FAIL"))
    print(f"[t7] {len(outs)} pre-flight outputs; PASS rows per passing T06 arm "
          f"{t06_pass[0]}-{t06_pass[-1]}, 07 {passes['07 basic_roles']}")
    for g, ls in GROUPS:
        for l in ls:
            print(f"[t7]   {g:24s} {l:36s} {dict(per.get(l, {}))}")

    # the refusal
    bt = rows[("basic_tunnel", "skeleton")]
    prow, end = outs["basic_tunnel/skeleton"]
    fails = [(l, d) for s, l, d in prow if s == "FAIL"]
    labelled = [(l, d) for l, d in fails if l]
    if len(labelled) != 1 or labelled[0][0] != "entries match p4info":
        die(f"basic_tunnel/skeleton: failing checks {labelled}")
    m = re.match(r"(\d+) problem\(s\); first: (s\d+) entry (\d+): table '([^']+)' is not in the "
                 r"p4info \(it has: ([^)]+)\)", labelled[0][1])
    if not m:
        die(f"basic_tunnel/skeleton FAIL detail changed: {labelled[0][1]}")
    n_problems, bad_table, has_table = int(m.group(1)), m.group(4), m.group(5)
    m_end = re.match(r"FAIL -- (\d+) check\(s\) failed; do NOT bring this package up", end)
    if not m_end or int(m_end.group(1)) != len(fails):
        die(f"basic_tunnel/skeleton end line {end!r} vs {len(fails)} FAIL rows")
    if int(bt["rc"]) != 1 or not bt["verdict"].startswith("RED ARM"):
        die(f"basic_tunnel/skeleton T06 row {bt['rc']} {bt['verdict']}")
    bt_text = read(bt["report"])
    if "pre-flight FAILED (rc 1)" not in bt_text or "== ndt up p4 --app" in bt_text:
        die("basic_tunnel/skeleton: pre-flight rc 1 / no ndt up not both shown")
    print(f"[t7] refusal: {n_problems} problems, {bad_table} not in p4info (has {has_table}); "
          f"end line says {m_end.group(1)} check(s) -- that is {len(fails)} FAIL rows of ONE check")

    H = 7.0
    fig, ax = canvas(H)
    title(ax, "What pre-flight checks before ndt up")
    N = len(outs)
    # three columns of groups; the refusal panel on the right
    cols = [[0], [1, 2], [3, 4, 5]]
    colx = [0.40, 3.52, 6.64]
    colw = 3.00
    rh, hh, gg = 0.285, 0.50, 0.20
    y_top = 1.05
    status_c = {"PASS": GREEN, "INFO": FAINT, "FAIL": WARNC}
    fail_anchor = None
    for c, gidx in enumerate(cols):
        y = y_top
        for gi in gidx:
            gname, labels = GROUPS[gi]
            gh = hh + len(labels) * rh + 0.12
            box(ax, colx[c], y, colw, gh, fill=PANEL, edge=RULE, lw=1.0, r=0.06, z=1)
            txt(ax, colx[c] + 0.15, y + 0.27, gname, size=13.5, weight="bold", ha="left")
            for k, lab in enumerate(labels):
                yy = y + hh + k * rh + rh / 2
                txt(ax, colx[c] + 0.15, yy, lab, size=10.5, color=BODY, ha="left")
                cnt = per.get(lab, {})
                xr = colx[c] + colw - 0.12
                for st in ("FAIL", "INFO", "PASS"):
                    v = cnt.get(st, 0)
                    if not v:
                        continue
                    txt(ax, xr, yy, f"{v}", size=11, color=status_c[st], weight="bold",
                        ha="right")
                    if st == "FAIL":
                        fail_anchor = (xr + 0.02, yy)
                    xr -= 0.30
            y += gh + gg
    # refusal box: a box title and the raw FAIL row, nothing else (rule 2: no kicker, no verdict)
    fx, fy, fw, fh = 9.80, 1.05, 3.13, 2.55
    box(ax, fx, fy, fw, fh, fill=WARN_BG, edge=WARNC, lw=1.6, r=0.08, z=1)
    txt(ax, fx + 0.18, fy + 0.34, "basic_tunnel · skeleton", size=13.5, weight="bold",
        ha="left")
    txt(ax, fx + 0.18, fy + 0.82, "FAIL", size=12.5, color=WARNC, weight="bold", ha="left")
    txt(ax, fx + 0.72, fy + 0.82, "entries match p4info", size=12, ha="left", color=BODY)
    txt(ax, fx + 0.18, fy + 1.28, f"{n_problems} problems, first:", size=12, ha="left",
        color=BODY)
    txt(ax, fx + 0.18, fy + 1.66, bad_table, size=11, ha="left", color=INK, mono=True)
    txt(ax, fx + 0.18, fy + 2.04, "not in its p4info", size=12, ha="left", color=BODY)
    if fail_anchor:
        ax.add_patch(FancyArrowPatch(fail_anchor, (fx - 0.02, fy + 0.82),
                                     connectionstyle="arc3,rad=-0.18", arrowstyle="-|>",
                                     mutation_scale=13, color=WARNC, lw=1.4, shrinkA=6,
                                     shrinkB=0, zorder=4))
    # legend only: the colour of a count
    lx, ly = fx, fy + fh + 0.55
    for k, st in enumerate(("PASS", "INFO", "FAIL")):
        xx = lx + k * 1.0
        ax.add_patch(Rectangle((xx, ly - 0.11), 0.22, 0.22, facecolor=status_c[st],
                               edgecolor=status_c[st], zorder=3))
        txt(ax, xx + 0.32, ly, st, size=12, color=MUTED, ha="left")
    save(fig, "fig_t7_preflight_checks")
    return outs, per, (n_problems, bad_table, len(fails), passes)


# ---------------------------------------------------------------------------
# fig_t8_what_you_bring
# ---------------------------------------------------------------------------

def convert_output(path):
    text = read(path)
    m = re.search(r"^package '([^']+)' -> \S+\n((?:  .*\n)+?)  read back through "
                  r"p4_proxy/mininet/topo_from_json\.py: ok", text, re.M)
    if not m:
        die(f"{path}: no convert.py output")
    body = m.group(2)
    n = int(one(r"^\s+files\s+:\s+(\d+)$", body, path).group(1))
    files = re.findall(r"^\s{18}(\S+)$", body, re.M)
    first = one(r"^\s+files\s+:\s+\d+\n\s+(\S+)$", body, path).group(1)
    files = [first] + [f for f in files if f != first]
    mode = one(r"^\s+control plane\s+:\s+(\S+)$", body, path).group(1)
    if len(files) != n:
        die(f"{path}: files says {n}, lists {len(files)}")
    return n, sorted(files), mode


def fig_t8(rows):
    src = read(CONVERT)
    for needle in ('"controller": "mycontroller.py" if mode == "external" else None',
                   'written.append("ndtwin/topology.json")', 'written.append("package.json")',
                   "shutil.copyfile(abs_src, dest)", "read_back(model)",
                   'mode = "external" if os.path.isfile(os.path.join(exercise_dir, '
                   '"mycontroller.py")) else "ndtwin"'):
        if needle not in src:
            die(f"convert.py no longer has {needle!r}")
    n, files, mode = convert_output(rows[("basic", "solution")]["report"])
    new = [f for f in files if f in ("package.json", "ndtwin/topology.json")]
    copies = [f for f in files if f not in new]
    if len(new) != 2 or mode != "ndtwin":
        die(f"basic/solution package: new {new}, mode {mode}")
    runtime = [f for f in copies if re.fullmatch(r"pod-topo/s\d+-runtime\.json", f)]
    prog = [f for f in copies if f.endswith(".p4")]
    built = [f for f in copies if f.startswith("build/")]
    topo = [f for f in copies if f.endswith("topology.json")]
    if len(prog) != 1 or len(built) != 2 or len(topo) != 1 or \
            len(runtime) + 4 != len(copies):
        die(f"basic/solution copies do not split as expected: {copies}")
    ext = sorted(ex for (ex, w), r in rows.items() if w == "solution"
                 and convert_output(r["report"])[2] == "external")
    all_n = sorted(convert_output(r["report"])[0] for (ex, w), r in rows.items()
                   if w == "solution")
    print(f"[t8] basic/solution: {n} files ({len(copies)} copies + {new}); runtime x "
          f"{len(runtime)}; external-mode exercises {ext}; files per solution package "
          f"{all_n[0]}-{all_n[-1]}")

    H = 6.45
    fig, ax = canvas(H)
    title(ax, "What the exercise brings, what convert adds")
    ih, ig, top = 0.72, 0.16, 1.62
    rows_y = [top + k * (ih + ig) for k in range(6)]     # 6 slots: 4 files, (gap), controller
    # left: the exercise folder
    lx, ly, lw_, lh = 0.45, 1.05, 4.35, 5.0
    box(ax, lx, ly, lw_, lh, fill=PANEL, edge=RULE, lw=1.0, r=0.08, z=1)
    txt(ax, lx + 0.2, ly + 0.3, "EXERCISE FOLDER · basic", size=11.5, color=FAINT,
        weight="bold", ha="left")
    items = [
        (prog[0], "its program"),
        (f"{built[0]}  +  p4info", "p4c output"),
        (topo[0], "topology"),
        (f"pod-topo/s1…s{len(runtime)}-runtime.json", "table entries"),
    ]
    for k, (name, role) in enumerate(items):
        y = rows_y[k]
        box(ax, lx + 0.25, y, lw_ - 0.5, ih, fill=WHITE, edge=INK, lw=1.2)
        txt(ax, lx + 0.45, y + 0.25, name, size=11.5, mono=True, ha="left")
        txt(ax, lx + 0.45, y + 0.53, role, size=11.5, color=MUTED, ha="left")
    cy = 5.18
    box(ax, lx + 0.25, cy, lw_ - 0.5, ih, fill=WHITE, edge=MUTED, lw=1.2, ls=(0, (4, 3)))
    txt(ax, lx + 0.45, cy + 0.25, "mycontroller.py", size=11.5, mono=True, ha="left",
        color=BODY)
    txt(ax, lx + 0.45, cy + 0.53, f"optional · {len(ext)} of 13", size=11.5, color=MUTED,
        ha="left")

    # middle: convert.py
    mx, mw = 5.35, 1.75
    my, mh = 2.35, 1.3
    box(ax, mx, my, mw, mh, fill=ACCENT_BG, edge=ACCENT, lw=2.2)
    txt(ax, mx + mw / 2, my + 0.45, "convert.py", size=15, weight="bold", color=ACCENT)
    txt(ax, mx + mw / 2, my + 0.9, "read back: ok", size=11.5, color=MUTED)
    arrow(ax, lx + lw_ + 0.05, my + mh / 2, mx - 0.02, my + mh / 2, color=INK, lw=1.6)

    # right: the package
    rx, ry, rw, rh = 7.65, 1.05, 5.25, 5.0
    box(ax, rx, ry, rw, rh, fill=PANEL, edge=ACCENT, lw=1.6, r=0.08, z=1)
    txt(ax, rx + 0.2, ry + 0.3, f"PACKAGE · {n} files", size=11.5, color=ACCENT,
        weight="bold", ha="left")
    arrow(ax, mx + mw + 0.02, my + mh / 2, rx - 0.02, my + mh / 2, color=INK, lw=1.6)
    # the copies, same exercise-relative paths
    cy2, chh = top, 2.36
    box(ax, rx + 0.25, cy2, rw - 0.5, chh, fill=WHITE, edge=INK, lw=1.2)
    txt(ax, rx + 0.45, cy2 + 0.28, f"{len(copies)} copies, same paths", size=11.5,
        color=MUTED, ha="left")
    listing = [prog[0], built[0], built[1], topo[0],
               f"pod-topo/s1…s{len(runtime)}-runtime.json"]
    for k, f in enumerate(listing):
        txt(ax, rx + 0.45, cy2 + 0.66 + k * 0.33, f, size=11, mono=True, ha="left",
            color=BODY)
    # the two NDTwin-made files; package.json sits on the controller's row
    for name, role, y in [("ndtwin/topology.json", "NDTwin's model", 4.26),
                          ("package.json", "control plane, hosts, links", cy)]:
        box(ax, rx + 0.25, y, rw - 0.5, ih, fill=ACCENT_BG, edge=ACCENT, lw=1.6)
        txt(ax, rx + 0.45, y + 0.25, name, size=11.5, mono=True, ha="left", color=ACCENT,
            weight="bold")
        txt(ax, rx + 0.45, y + 0.53, role, size=11.5, color=MUTED, ha="left")
        txt(ax, rx + rw - 0.45, y + ih / 2, "new", size=12, color=ACCENT, weight="bold",
            ha="right")
    # the controller is recorded, not copied
    arrow(ax, lx + lw_ - 0.23, cy + ih / 2, rx + 0.23, cy + ih / 2, color=MUTED, lw=1.3,
          ls=(0, (4, 3)))
    txt(ax, (lx + lw_ + rx) / 2, cy + ih / 2 - 0.22, "name recorded, not copied", size=11.5,
        color=MUTED)
    save(fig, "fig_t8_what_you_bring")
    return n, files, copies, new, ext, all_n


# ---------------------------------------------------------------------------
# fig_t9_custom_headers
# ---------------------------------------------------------------------------

# short header tags for the row labels; each is asserted against GAP-1 section 2a's cell
TAGS = {
    "basic_tunnel": ("0x1212 tunnel", "0x1212"),
    "calc": ("0x1234 + lookahead", "0x1234"),
    "flowcache": ("packet-in/out header", "packet_in/out"),
    "link_monitor": ("0x812 probe + stacks", "0x812"),
    "mri": ("IPv4 option + stack", "IPv4 option"),
    "p4runtime": ("0x1212 tunnel", "0x1212"),
    "source_routing": ("0x1234 + route stack", "0x1234"),
}


def gap1_custom_header_exercises():
    text = read(GAP1)
    sec = text[text.find("### 2a."):text.find("### 2b.")]
    head = [c.strip() for c in re.search(r"^\| exercise \|(.*)\|$", sec, re.M).group(1).split("|")]
    col = head.index("`custom_headers`")
    out = {}
    for ln in sec.splitlines():
        if not ln.startswith("| ") or ln.startswith("| exercise") or ln.startswith("|---"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        ex, cell = cells[0], cells[1 + col]
        if "**關鍵**" in cell:
            out[ex] = cell
    return out


def gap_analysis_g6():
    text = read(GAPA)
    m = re.search(r"\*\*受影響 (\d+) 支\*\*：(.*?)＝", text, re.S)
    if not m:
        die("GAP-ANALYSIS.md G6 list moved")
    # the list runs over two lines: basic_tunnel(..)/calc(..)/source_routing(..)/link_monitor(..)
    # ＝看不見；mri(..)＝看錯；flowcache(..)＝CPU 通道另計
    blob = text[m.start():m.start() + 400]
    names = re.findall(r"(basic_tunnel|calc|source_routing|link_monitor|mri|flowcache|"
                       r"p4runtime)\(", blob)
    return int(m.group(1)), names


def g1_status(report):
    text = read(report)
    if re.search(r"N8  G1 link usage follows the iperf path -- NOT RUN", text):
        return "NOT RUN", None
    m = re.search(r"^LINK_USAGE \S+ expect=follows primary=(\d+) minor=\d+ rc=(\d+)$", text, re.M)
    if not m or m.group(2) != "0":
        die(f"{report}: G1 neither NOT RUN nor a passing LINK_USAGE line")
    it = one(r"^\s+\S+: (h\d+ -> h\d+) \(([0-9.]+)\), iperf (-u -b \S+ -t \d+ -l \d+)$", text,
             report)
    return "PASS", (it.group(1), it.group(3))


def p4runtime_tunnel_evidence(report):
    d = report[:-3]
    onpath = read(os.path.join(d, "link_usage/onpath.txt")).split()
    by = dict(zip(onpath[0::3], zip(onpath[1::3], onpath[2::3])))
    sw_b, host_b = int(by["s1-eth2"][1]), int(by["s2-eth1"][1])
    sent = int(one(r"Sent (\d+) datagrams", read(os.path.join(d, "link_usage/iperf_client.txt")),
                   "p4runtime iperf").group(1))
    twin = read(os.path.join(d, "link_usage/twin_integral.txt"))
    tw = float(one(r"^s1-eth2 ([0-9.]+) switch$", twin, "p4runtime twin").group(1))
    hdr = read(TUNNEL_P4)
    m = one(r"header myTunnel_t \{\s*bit<(\d+)> proto_id;\s*bit<(\d+)> dst_id;\s*\}", hdr,
            TUNNEL_P4)
    hdr_bytes = (int(m.group(1)) + int(m.group(2))) // 8
    if sw_b - host_b != sent * hdr_bytes:
        die(f"p4runtime: s1-eth2 {sw_b} - s2-eth1 {host_b} != {sent} x {hdr_bytes}")
    if tw <= 0:
        die("p4runtime: twin integral on s1-eth2 is not > 0")
    return dict(sw_b=sw_b, host_b=host_b, sent=sent, hdr=hdr_bytes, twin_bit=tw)


def fig_t9(rows):
    ch = gap1_custom_header_exercises()
    n_g6, g6 = gap_analysis_g6()
    if len(ch) != 7:
        die(f"GAP-1 section 2a marks {len(ch)} custom_headers as 關鍵, not 7: {sorted(ch)}")
    if n_g6 != 6 or len(g6) != 6:
        die(f"GAP-ANALYSIS G6: {n_g6} / {g6}")
    diff = sorted(set(ch) - set(g6)), sorted(set(g6) - set(ch))
    print(f"[t9] GAP-1 2a 關鍵 custom_headers: {sorted(ch)}; GAP-ANALYSIS G6 ({n_g6}): {g6}; "
          f"GAP-1 minus G6 {diff[0]}, G6 minus GAP-1 {diff[1]}")
    if diff != (["p4runtime"], []):
        die("the 6-vs-7 difference is no longer exactly p4runtime")
    for ex, (tag, needle) in TAGS.items():
        if needle not in ch[ex]:
            die(f"GAP-1 cell for {ex} no longer contains {needle!r}: {ch[ex]}")
    if set(TAGS) != set(ch):
        die("TAGS and GAP-1's list differ")
    g2b = read(GAP2B)
    if "7 支自訂標頭 exercise 的解答臂全綠" not in g2b:
        die("GAP-2b no longer says 7 custom-header exercises")

    info = {}
    for ex in ch:
        r = rows[(ex, "solution")]
        if int(r["rc"]) != 0 or not r["verdict"].startswith("PASS"):
            die(f"{ex}/solution in T06: {r['rc']} {r['verdict']}")
        g1, it = g1_status(r["report"])
        if g1 == "NOT RUN":
            cls = "none"
        elif ex == "p4runtime":
            ev = p4runtime_tunnel_evidence(r["report"])
            print(f"[t9] p4runtime: s1-eth2 {ev['sw_b']} B - s2-eth1 {ev['host_b']} B = "
                  f"{ev['sw_b'] - ev['host_b']} = {ev['sent']} datagrams x {ev['hdr']} B "
                  f"(myTunnel_t); twin integral on s1-eth2 {ev['twin_bit']:.0f} bit")
            cls = "yes"
        else:
            if not it[1].startswith("-u "):
                die(f"{ex}: G1 traffic is not the IPv4 UDP iperf: {it}")
            cls = "ipv4"
        info[ex] = dict(verdict=r["verdict"], g1=g1, it=it, cls=cls)
        print(f"[t9] {ex:15s} {r['verdict']:12s} G1 {g1:7s} {it}  -> {cls}")

    order_cls = {"yes": 0, "ipv4": 1, "none": 2}
    gap1_order = list(ch)
    exs = sorted(ch, key=lambda e: (order_cls[info[e]["cls"]], gap1_order.index(e)))

    H = 6.4
    fig, ax = canvas(H)
    title(ax, "Seven custom-header exercises forward")
    top, rh = 1.75, 0.60
    lx = 0.45
    x1, pw1 = 4.35, 3.75            # left panel
    x2, pw2 = 8.40, 4.48            # right panel
    box(ax, x1, top - 0.75, pw1, 0.75 + 7 * rh + 0.15, fill=PANEL, edge=RULE, lw=1.0, z=0)
    box(ax, x2, top - 0.75, pw2, 0.75 + 7 * rh + 0.15, fill=PANEL, edge=RULE, lw=1.0, z=0)
    txt(ax, x1 + 0.2, top - 0.52, "RAN IT · 09-27", size=11.5, color=FAINT, weight="bold",
        ha="left")
    txt(ax, x1 + 0.2, top - 0.2, "forwards (solution arm)", size=13.5, weight="bold",
        ha="left")
    txt(ax, x2 + 0.2, top - 0.52, "SAME RUNS' RAW · JUDGED", size=11.5, color=FAINT,
        weight="bold", ha="left")
    txt(ax, x2 + 0.2, top - 0.2, "twin saw its own frames", size=13.5, weight="bold",
        ha="left")
    chip = {"yes": (GREEN, WHITE, "yes · 0x1212 bytes"),
            "ipv4": (AMBER, INK, "IPv4 only"),
            "none": (GREY, INK, "no evidence")}
    for i, ex in enumerate(exs):
        y = top + 0.12 + i * rh + rh / 2
        if i:
            for a0, a1 in ((lx, x1 - 0.1), (x1, x1 + pw1), (x2, x2 + pw2)):
                ax.plot([a0, a1], [y - rh / 2, y - rh / 2], color=RULE, lw=0.8, zorder=1)
        txt(ax, lx, y - 0.1, ex, size=13.5, weight="bold", ha="left")
        txt(ax, lx, y + 0.17, TAGS[ex][0], size=11, color=MUTED, ha="left")
        # left: the verdict
        box(ax, x1 + pw1 / 2 - 0.9, y - 0.2, 1.8, 0.4, fill=GREEN, edge=GREEN, r=0.05, z=3)
        txt(ax, x1 + pw1 / 2, y, info[ex]["verdict"], size=12.5, color=WHITE, weight="bold")
        # right: the evidence class
        fc, tc, lab = chip[info[ex]["cls"]]
        box(ax, x2 + pw2 / 2 - 1.3, y - 0.2, 2.6, 0.4, fill=fc, edge=fc, r=0.05, z=3)
        txt(ax, x2 + pw2 / 2, y, lab, size=12.5, color=tc, weight="bold")
    save(fig, "fig_t9_custom_headers")
    return ch, g6, info


def main():
    rows = t06_rows()
    fig_t6(rows)
    fig_t7(rows)
    fig_t8(rows)
    fig_t9(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
