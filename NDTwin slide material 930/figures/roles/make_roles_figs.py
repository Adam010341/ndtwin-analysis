#!/usr/bin/env python3
"""
make_roles_figs.py -- the four `roles` figures of the 2026-09-30 report.

    fig_r1_four_rulings   Adam's four 2026-09-24 rulings on the P4-driven API shape, one card each,
                          with a status tag per card that this script checks against git and raw
    fig_r2_roles_path     how roles.ipv4_route gets from package.json into the program's own table:
                          the build steps as the 09-26 live run printed them (RAN IT), and the write
                          path as the code at trunk 3d740be0 names it (READ THE CODE)
    fig_r3_live07         live 07 twice (09-24, before the heartbeat; 09-26, heartbeat running):
                          the L1-L6 verdict lines of each run's stdout log, and the three pingalls
    fig_r4_capabilities   what every switch's `capabilities` says in switch_state in the newest
                          live 07 run (09-26, heartbeat on): the roles package and the no-roles
                          package, one row each -- the final state only (template v1.8,
                          2026-09-29 UTC: no 09-24 -> 09-26 progression, no run sha on the canvas;
                          the sha and its dirty count stay in the .md and the speaker notes)

Data (NDTwin-Kernel checkout, REPO below):
  * live runs  doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/
               2026-09-24T160256Z_07_roles_basic   (01_binaries.txt: repo HEAD 572d9462)
               2026-09-26T202055Z_07_roles_basic   (01_binaries.txt: repo HEAD b2eeb71d)
    and their stdout logs under scratch/overnight-2026-09-05/logs/orchestrator-0924/
               live-0925/07_roles_basic.log, intake-0926/live07/07.log
    -- all uncommitted observations in this checkout (runs/ and scratch/ are not tracked).
  * the heartbeat live logs (fig_r1's status only): intake-0926/hbw-live/h14-*.log, h5b-*.log
  * committed files read through `git show 3d740be0:<path>` (ANALYSIS.md section 8, the code).

Every number drawn is parsed from those files at run time; a mismatch with what the figure
claims ends the script with SystemExit.  The only literals are labels, and the names in the
READ THE CODE boxes, each of which is asserted to still be in its file at trunk 3d740be0.

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/roles"
    nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_roles_figs.py [--only fig_r4_capabilities ...]
`--only` draws just the named figures (evidence() is checked in full either way); without it,
all four are drawn.
"""
import argparse
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
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["font.monospace"] = ["Courier New", "Liberation Mono", "DejaVu Sans Mono"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

REPO = os.environ.get("NDTWIN_REPO", "/home/adam/Desktop/NDTwin-Kernel")
TRUNK = "3d740be0"             # the tree the READ THE CODE boxes were read at
LIVE = os.path.join(REPO, "doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs")
R24 = os.path.join(LIVE, "2026-09-24T160256Z_07_roles_basic")
R26 = os.path.join(LIVE, "2026-09-26T202055Z_07_roles_basic")
ORCH = os.path.join(REPO, "scratch/overnight-2026-09-05/logs/orchestrator-0924")
LOG24 = os.path.join(ORCH, "live-0925/07_roles_basic.log")
LOG26 = os.path.join(ORCH, "intake-0926/live07/07.log")
HB14 = os.path.join(ORCH, "intake-0926/hbw-live/h14-20260926T152605Z.log")
HB5 = os.path.join(ORCH, "intake-0926/hbw-live/h5b-20260926T172912Z.log")
HB14_RUN = os.path.join(LIVE, "2026-09-26T152605Z_08_heartbeat")
HB5_RUN = os.path.join(LIVE, "2026-09-26T172912Z_08_heartbeat")
OFFLINE = os.path.join(ORCH, "merged-R-572d9462.offline_5-3.log")
RULINGS_NIGHT = os.path.join(ORCH, "intake-0926/RULINGS-0927-night.md")
WEBGUI = os.path.expanduser("~/Web-GUI")

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
WARNC, WARN_BG, WHITE = "#9C3B2E", "#FBF2F0", "#FFFFFF"
GREEN, AMBER, GREY = "#2F7D4F", "#E3A21A", "#C9CDD0"


# ------------------------------------------------------------------ small helpers
def die(msg):
    raise SystemExit(f"make_roles_figs: {msg}")


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError as e:
        die(f"cannot read {path}: {e}")


def jload(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        die(f"cannot read JSON {path}: {e}")


def git(*args, check=True):
    p = subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True)
    if check and p.returncode != 0:
        die(f"git {' '.join(args)}: rc {p.returncode}: {p.stderr.strip()}")
    return p


def at_trunk(path):
    """The committed file at TRUNK, never the shared working tree."""
    return git("show", f"{TRUNK}:{path}").stdout


def line_of(text, needle, path):
    """1-based line number of the first line containing `needle`, or die."""
    for i, ln in enumerate(text.splitlines(), 1):
        if needle in ln:
            return i
    die(f"{path}@{TRUNK} no longer contains {needle!r}")


def is_ancestor(a, b):
    return git("merge-base", "--is-ancestor", a, b, check=False).returncode == 0


def head_of(run):
    t = read(os.path.join(run, "01_binaries.txt"))
    m = re.search(r"^repo HEAD\s+([0-9a-f]{40})", t, re.M)
    if not m:
        die(f"{run}/01_binaries.txt has no repo HEAD line")
    return m.group(1)


def last_line(path):
    lines = [ln for ln in read(path).splitlines() if ln.strip()]
    if not lines:
        die(f"{path} is empty")
    return lines[-1]


def pingall(path):
    m = re.fullmatch(r"PINGALL_LOSS pairs=(\d+) zero_loss=(\d+) lossy=(\d+) untested=(\d+)",
                     last_line(path))
    if not m:
        die(f"{path}: last line is not a PINGALL_LOSS summary")
    pairs, zero, lossy, untested = (int(x) for x in m.groups())
    if pairs != zero + lossy + untested:
        die(f"{path}: pairs {pairs} != {zero}+{lossy}+{untested}")
    return dict(pairs=pairs, zero=zero, lossy=lossy, untested=untested)


def save(fig, name):
    os.makedirs(HIRES, exist_ok=True)
    for ext in ("pdf", "png", "svg"):
        kw = {"dpi": 300} if ext == "png" else {}
        fig.savefig(os.path.join(OUTDIR, f"{name}.{ext}"), facecolor=WHITE, **kw)
    fig.savefig(os.path.join(HIRES, f"{name}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"[out] {name}.{{pdf,png,svg}} + _hires/{name}.png")


def canvas(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fill=WHITE, edge=INK, lw=1.2, ls="solid", r=0.06, z=2):
    ax.add_patch(FancyBboxPatch((x + r, y + r), w - 2 * r, h - 2 * r,
                                boxstyle=f"round,pad={r},rounding_size={r}", facecolor=fill,
                                edgecolor=edge, linewidth=lw, linestyle=ls, zorder=z))


def txt(ax, x, y, s, size=13, color=INK, weight="normal", ha="center", va="center",
        mono=False, z=6):
    return ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va,
                   zorder=z, family="monospace" if mono else None, linespacing=1.3)


def arrow(ax, x0, y0, x1, y1, color=INK, lw=1.4, ls="solid", z=3, both=False):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="<|-|>" if both else "-|>",
                                 mutation_scale=13, color=color, lw=lw, linestyle=ls,
                                 shrinkA=0, shrinkB=0, zorder=z))


def title(ax, s):
    if len(s) > 45:
        die(f"title over 45 characters: {s!r}")
    txt(ax, 0.45, 0.48, s, size=22, weight="bold", ha="left")


# ------------------------------------------------------------------ evidence
def evidence():
    """Everything the four figures show, parsed and cross-checked. Returns a dict."""
    E = {}
    # ---- the two runs: which code, and the stdout log that carries the verdicts
    E["head24"], E["head26"] = head_of(R24), head_of(R26)
    if not E["head24"].startswith("572d9462") or not E["head26"].startswith("b2eeb71d"):
        die(f"run heads moved: {E['head24'][:8]} / {E['head26'][:8]}")
    # both runs stood on a dirty checkout: `ndt status`'s code line, captured before the run
    # (00_status_before.txt), says HEAD plus N files with uncommitted changes
    for key, run in (("24", R24), ("26", R26)):
        head = E["head" + key]
        m = re.search(r"^\s*code\s+" + head[:8] + r"\s+\+(\d+) file\(s\) with uncommitted changes",
                      read(os.path.join(run, "00_status_before.txt")), re.M)
        if not m:
            die(f"{run}/00_status_before.txt: no dirty-checkout code line for {head[:8]}")
        E["dirty" + key] = int(m.group(1))
    if (E["dirty24"], E["dirty26"]) != (61, 92):
        die(f"dirty counts are {E['dirty24']} / {E['dirty26']}, the .md files say 61 / 92")
    for log, run in ((LOG24, R24), (LOG26, R26)):
        t = read(log)
        if f"raw : {run}" not in t:
            die(f"{log} is not the log of {run}")
        if last_line(log) != "PASS 07_roles_basic":
            die(f"{log}: last line is {last_line(log)!r}")
        if re.search(r"^   !! ", t, re.M):
            die(f"{log}: carries a fail line")
    # ---- L-cell verdict lines: `judge` prints '   <label>: <OK text>' and every label starts
    # with its cell, L1..L6 (07_roles_basic.sh judge(); a BAD one would be '   !! ...').
    cells = {}
    for key, log in (("24", LOG24), ("26", LOG26)):
        per = {f"L{i}": [] for i in range(1, 7)}
        for ln in read(log).splitlines():
            m = re.match(r"^   (L[1-6])\b", ln)
            if m:
                per[m.group(1)].append(ln.strip())
        for c, lines in per.items():
            if not lines:
                die(f"{log}: no verdict line for {c}")
        cells[key] = per
    E["cells"] = cells
    # ---- pingall: bring-up (32), during the cut (54), after recovery (61)
    E["ping"] = {}
    for key, run, log in (("24", R24, LOG24), ("26", R26, LOG26)):
        d = {"up": pingall(os.path.join(run, "32_pingall.txt")),
             "cut": pingall(os.path.join(run, "54_pingall_during_cut.txt")),
             "after": pingall(os.path.join(run, "61_pingall_after_recovery.txt"))}
        t = read(log)
        # the log's own record of the cut-time loss must be the raw's (it is a note, not a verdict)
        want = "traffic during the cut (recorded, NOT asserted -- (c) does not hold): " + \
               last_line(os.path.join(run, "54_pingall_during_cut.txt"))
        if want not in t:
            die(f"{log} does not record the cut-time pingall as 'recorded, NOT asserted'")
        for k, v in d.items():
            if v["pairs"] != 12 or v["untested"] != 0:
                die(f"{run} {k}: pairs {v['pairs']} untested {v['untested']}")
        if d["up"]["zero"] != 12 or d["after"]["zero"] != 12:
            die(f"{run}: bring-up / after-recovery not 12/12")
        E["ping"][key] = d
    if (E["ping"]["24"]["cut"]["lossy"], E["ping"]["26"]["cut"]["lossy"]) != (8, 3):
        die(f"cut-time lossy pairs are {E['ping']['24']['cut']['lossy']} / "
            f"{E['ping']['26']['cut']['lossy']}, the figure's notes say 8 / 3")
    # ---- capabilities in switch_state
    E["caps"] = {}
    for key, run in (("24", R24), ("26", R26)):
        for pkg, f in (("roles", "30_switch_state_roles.json"),
                       ("plain", "71_switch_state_plain.json")):
            sw = jload(os.path.join(run, f)).get("switches") or {}
            caps = [json.dumps(s.get("capabilities"), sort_keys=True) for s in sw.values()]
            if len(sw) != 4 or len(set(caps)) != 1 or caps[0] == "null":
                die(f"{run}/{f}: {len(sw)} switches, {len(set(caps))} distinct capabilities")
            E["caps"][(key, pkg)] = (json.loads(caps[0]), len(sw), len(sw))
    # ---- the build steps, 09-26 run
    conv = read(os.path.join(R26, "10_convert_roles.txt"))
    m = re.search(r"roles\s+: ipv4_route owner=(\S+) table=(\S+) match_field=(\S+) "
                  r"action=(\S+) dst_mac=(\S+) port=(\S+)", conv)
    if not m:
        die("10_convert_roles.txt has no roles line")
    E["role"] = dict(zip(("owner", "table", "match_field", "action", "dst_mac", "port"),
                         m.groups()))
    m = re.search(r"owned table\s+: (\d+) match entries for (\S+) taken out of the runtime "
                  r"files \(([^)]*)\)", conv)
    if not m:
        die("10_convert_roles.txt has no 'owned table' line")
    per = [int(x) for x in re.findall(r"s\d+: (\d+)", m.group(3))]
    if int(m.group(1)) != sum(per) or m.group(2) != E["role"]["table"]:
        die(f"convert: {m.group(1)} != sum {per} or table {m.group(2)}")
    E["taken_out"], E["taken_out_per"] = int(m.group(1)), per
    pre = read(os.path.join(R26, "12_preflight_basic_roles.txt"))
    for name in ("roles.ipv4_route resolves", "owned table has no package entries"):
        if not re.search(r"^  PASS  " + re.escape(name) + r"\s", pre, re.M):
            die(f"12_preflight_basic_roles.txt: no PASS for {name!r}")
    if last_line(os.path.join(R26, "12_preflight_basic_roles.txt")) != \
            "PASS -- every check passed":
        die("12_preflight_basic_roles.txt did not pass")
    lines21 = read(os.path.join(R26, "21_proxy_roles_lines.txt"))
    m = re.search(r"(\d+) of (\d+) initial routes written into the package's route tables",
                  lines21)
    if not m or m.group(1) != m.group(2):
        die("21_proxy_roles_lines.txt: no 'N of N initial routes written'")
    E["initial"] = (int(m.group(1)), int(m.group(2)))
    print(f"[evidence] heads {E['head24'][:8]} (+{E['dirty24']} dirty) / {E['head26'][:8]} "
          f"(+{E['dirty26']} dirty); role {E['role']}; "
          f"taken out {E['taken_out']} {per}; initial routes {E['initial']}")
    return E


# ------------------------------------------------------------------ fig_r1
def ruling_status(E):
    """Each card's tags, every one checked here. Returns {card: [(text, color), ...]}."""
    # the rulings themselves, ANALYSIS.md section 8 at TRUNK
    ap = "doc/audit/2026-09-24_p4-driven-api-shape/ANALYSIS.md"
    an = at_trunk(ap).splitlines()
    want = {401: "## 8. Adam 的裁決", 403: "`owner: ndtwin` 時 NDTwin 獨佔該表",
            404: "存活偵測以 root 的 veth 心跳為主", 405: "`get_graph_data` 的節點帶 `capabilities`",
            406: "7 支同形"}
    for ln, s in want.items():
        if s not in an[ln - 1]:
            die(f"{ap}:{ln} no longer says {s!r}")
    if "load_balance 多表範本" not in an[405] or "之後" not in an[405]:
        die(f"{ap}:406 no longer defers load_balance / tunnel / ternary")

    # 1 ownership: merged, and live 07 ran it (pre-flight PASS, 16 taken out, 16 routes written)
    if not is_ancestor("572d9462", TRUNK):
        die("572d9462 (roles merge) is not in trunk")
    s1 = [("done", GREEN)]

    # 2 heartbeat: merged; 08 H1-H4 PASS on cafd518a, H5 PASS on 3f8c2abf; external: no heartbeat
    if not is_ancestor("cafd518a", TRUNK):
        die("cafd518a (heartbeat segment W merge) is not in trunk")
    if not head_of(HB14_RUN).startswith("cafd518a") or last_line(HB14) != "PASS 08_heartbeat":
        die("08 H1-H4 run is not a PASS on cafd518a")
    if not head_of(HB5_RUN).startswith("3f8c2abf") or last_line(HB5) != "PASS 08_heartbeat":
        die("08 H5 rerun is not a PASS on 3f8c2abf")
    if "H4 reroute: reroute.available False, reason external_control_plane" not in read(HB14) \
            or "no heartbeat on the external fabric (rc 3), as designed" not in read(HB14):
        die("08 H4 no longer records external_control_plane / no heartbeat on external")
    if "a heartbeat ran on exactly the 17 expected arm(s)" not in read(HB5):
        die("08 H5 no longer records the 17 expected arms")
    if is_ancestor("feat/external-detect-only-0927", TRUNK):
        die("feat/external-detect-only-0927 is in trunk now: the 'external: open' tag is stale")
    s2 = [("owned tables: done", GREEN), ("external: open", AMBER)]

    # 3 capabilities: proxy switch_state has them (live L6); kernel + GUI not in trunk
    if E["caps"][("26", "roles")][0].get("ipv4_route") != "ndtwin":
        die("09-26 switch_state capabilities are not the roles ones")
    if git("grep", "-q", '"capabilities"', TRUNK, "--", "src", "include",
           check=False).returncode == 0:
        die(f"the kernel at {TRUNK} mentions \"capabilities\" now: the kernel tag is stale")
    br = git("rev-parse", "--verify", "-q", "feat/kernel-capabilities-0927", check=False)
    if br.returncode != 0 or is_ancestor("feat/kernel-capabilities-0927", TRUNK):
        die("third-cut branch missing or merged: re-check the 'kernel · GUI' tag")
    if "third cut: kernel get_graph_data capabilities -> GUI grey  -> YES" not in \
            read(RULINGS_NIGHT):
        die("RULINGS-0927-night.md no longer records the third cut")
    g = subprocess.run(["git", "-C", WEBGUI, "merge-base", "--is-ancestor",
                        "draft/p4-capabilities-0924", "origin/main"], capture_output=True)
    if g.returncode != 1:
        die(f"~/Web-GUI draft branch state changed (merge-base rc {g.returncode})")
    s3 = [("proxy: done", GREEN), ("kernel · GUI: open", AMBER)]

    # 4 first cut: ipv4_route live on basic (07), the 6 other same-shape offline PASS
    off = read(OFFLINE)
    same = re.findall(r"^(\w+)\s+convert rc=0  preflight PASS \(want PASS\) -- as expected",
                      off, re.M)
    if len(same) != 6 or "OFFLINE-5-3: every exercise as expected" not in off:
        die(f"offline 5-3: {len(same)} same-shape PASS lines")
    rb = at_trunk("p4_proxy/proxy_agent/route_binding.py")
    line_of(rb, 'REASON_NO_FIVE_TUPLE_ROLE = "no_five_tuple_role"',
            "p4_proxy/proxy_agent/route_binding.py")
    s4 = [("ipv4_route: done", GREEN), ("multi-table: later", GREY)]
    print(f"[r1] offline same-shape PASS: {same}")
    return [s1, s2, s3, s4]


def fig_r1(E):
    tags = ruling_status(E)
    W, H = 13.33, 6.0
    fig, ax = canvas(W, H)
    title(ax, "Four rulings on the P4 API shape (09-24)")
    cards = [
        ("NDTwin owns\nthe route table", [("owner: ndtwin", True),
                                          ("package entries", False),
                                          ("refused at pre-flight", False)]),
        ("No .p4 changes", [("liveness from a", False), ("root veth heartbeat", False)]),
        ("GUI reads\ncapabilities once", [("greys out what a", False),
                                          ("switch cannot do", False)]),
        ("Seven same-shape\nprograms first", [("one table:", False),
                                               ("roles.ipv4_route", True)]),
    ]
    x0, y0, gap = 0.45, 1.05, 0.22
    cw = (W - 2 * x0 - 3 * gap) / 4
    ch = 4.55
    for i, ((head, sub), tg) in enumerate(zip(cards, tags)):
        x = x0 + i * (cw + gap)
        box(ax, x, y0, cw, ch, fill=PANEL, edge=RULE, lw=1.0, r=0.08, z=1)
        txt(ax, x + 0.28, y0 + 0.45, str(i + 1), size=26, weight="bold", color=ACCENT,
            ha="left")
        txt(ax, x + 0.28, y0 + 0.95, head, size=16, weight="bold", ha="left", va="top")
        for k, (s, mono) in enumerate(sub):
            txt(ax, x + 0.28, y0 + 2.05 + k * 0.30, s, size=12.5 if not mono else 12,
                color=BODY if mono else MUTED, ha="left", mono=mono)
        ax.plot([x + 0.28, x + cw - 0.28], [y0 + 3.08, y0 + 3.08], color=RULE, lw=1.0,
                zorder=2)
        for k, (s, col) in enumerate(tg):
            ty = y0 + 3.30 + k * 0.52
            tw = cw - 0.56
            box(ax, x + 0.28, ty, tw, 0.40, fill=col, edge=col, lw=1.0, r=0.07, z=3)
            txt(ax, x + 0.28 + tw / 2, ty + 0.20, s, size=12.5, weight="bold",
                color=WHITE if col == GREEN else INK)
    save(fig, "fig_r1_four_rulings")


# ------------------------------------------------------------------ fig_r2
def read_names():
    """The READ THE CODE boxes: every name asserted in its file at TRUNK; line numbers printed."""
    spots = [
        ("src/ndt_core/routing_management/HttpRoutingStrategyBase.cpp",
         "HttpRoutingStrategyBase::installAnEntry("),
        ("src/ndt_core/routing_management/HttpRoutingStrategyBase.cpp",
         'return post("/stats/flowentry/add", body, "install flow entry");'),
        ("include/ndt_core/routing_management/P4RoutingStrategy.hpp",
         "class P4RoutingStrategy : public HttpRoutingStrategyBase"),
        ("p4_proxy/proxy_agent/api_routes.py", '@router.post("/stats/flowentry/add")'),
        ("p4_proxy/proxy_agent/api_routes.py", "success = await run_in_threadpool(topology.route_flow"),
        ("p4_proxy/proxy_agent/api_routes.py", "raise _route_write_unsupported(err, dpid)"),
        ("p4_proxy/proxy_agent/api_routes.py", '"outcome": "unsupported_on_p4",'),
        ("p4_proxy/proxy_agent/topology_manager.py", "def route_flow(self, dpid"),
        ("p4_proxy/proxy_agent/topology_manager.py",
         "success = bool(client.insert_ipv4_route(ipv4_dst, 32, next_hop_mac, out_port))"),
        ("p4_proxy/proxy_agent/topology_manager.py", "def install_initial_routes(self"),
        ("p4_proxy/proxy_agent/topology_manager.py",
         "if client.insert_ipv4_route(ipv4_dst, 32, next_hop_mac, out_port):"),
        ("p4_proxy/proxy_agent/route_binding.py", "class RouteBinding:"),
        ("p4_proxy/proxy_agent/route_binding.py", "def resolve(role, p4info"),
        ("p4_proxy/proxy_agent/route_binding.py", 'REASON_UNBOUND = "unbound"'),
        ("p4_proxy/proxy_agent/main.py", "def build_p4_client("),
        ("p4_proxy/proxy_agent/main.py",
         "client.bind_routes(route_binding_for(package, dpid, client.p4info, base_dir))"),
        ("p4_proxy/proxy_agent/main.py", "return route_binding.resolve(role.as_manifest(), p4info,"),
        ("p4_proxy/proxy_agent/p4_client.py", "def bind_routes(self, binding):"),
        ("p4_proxy/proxy_agent/p4_client.py", "def _writable_route_binding(self, what):"),
        ("p4_proxy/proxy_agent/p4_client.py", "raise RouteWriteUnsupported(route_binding_module.REASON_UNBOUND"),
        ("p4_proxy/proxy_agent/p4_client.py", "def insert_ipv4_route(self, dst_ip, prefix_len"),
        ("p4_proxy/proxy_agent/p4_client.py", 'binding = self._writable_route_binding("an ipv4_lpm route insert")'),
        ("tools/p4_exercise/convert.py", "def apply_route_role(exercise_dir, package, copies, role):"),
        ("tools/p4_exercise/preflight.py", "def _check_roles(report, package_dir"),
        ("tools/p4_exercise/preflight.py", "binding = route_binding.resolve(role.as_manifest(), p4info,"),
        ("tools/p4_exercise/preflight.py", 'report.ok("owned table has no package entries",'),
    ]
    cache = {}
    for path, needle in spots:
        if path not in cache:
            cache[path] = at_trunk(path)
        print(f"[read {TRUNK}] {path}:{line_of(cache[path], needle, path)}  {needle}")
    # the code read here is the code the 09-26 run ran: its 01_binaries.txt sha256 of each
    # source equals the file at TRUNK, and the rest of the path did not change in between
    import hashlib
    for m in re.finditer(r"^source\s+([0-9a-f]{16})\s+(\S+)$",
                         read(os.path.join(R26, "01_binaries.txt")), re.M):
        got = hashlib.sha256(git("show", f"{TRUNK}:{m.group(2)}").stdout.encode()).hexdigest()
        if got[:16] != m.group(1):
            die(f"{m.group(2)} at {TRUNK} is not what the 09-26 run ran")
    if git("diff", "--quiet", "b2eeb71d", TRUNK, "--", "p4_proxy/proxy_agent/api_routes.py",
           "src/ndt_core/routing_management", "include/ndt_core/routing_management",
           "src/ndt_core/http/HttpSession.cpp", check=False).returncode != 0:
        die(f"the write path changed between b2eeb71d and {TRUNK}")
    print(f"[read {TRUNK}] = the 09-26 run's code on this path (01_binaries sha256 + git diff)")
    # insert_ipv4_route writes through stub.Write, after the binding check
    t = cache["p4_proxy/proxy_agent/p4_client.py"]
    a = line_of(t, "def insert_ipv4_route(self, dst_ip, prefix_len", "p4_client.py")
    body = t.splitlines()[a:a + 40]
    if not any("self.stub.Write(req, timeout=RPC_TIMEOUT_S)" in ln for ln in body):
        die("insert_ipv4_route no longer calls self.stub.Write within 40 lines")


def fig_r2(E):
    read_names()
    W, H = 13.33, 6.65
    fig, ax = canvas(W, H)
    title(ax, "roles.ipv4_route: from package to table")

    # ---------------- RAN IT: the build, as the 09-26 run printed it
    txt(ax, 0.45, 1.0, "RAN IT  ·  live 07, 09-26", size=12, weight="bold", color=FAINT,
        ha="left")
    ty, th = 1.25, 1.55
    r = E["role"]
    # A package.json
    ax_, aw = 0.45, 3.45
    box(ax, ax_, ty, aw, th)
    txt(ax, ax_ + 0.22, ty + 0.30, "package.json", size=14, weight="bold", ha="left")
    for k, (kk, vv) in enumerate((("table", r["table"]), ("match", r["match_field"]),
                                  ("action", r["action"]))):
        txt(ax, ax_ + 0.22, ty + 0.68 + k * 0.27, f"{kk:<7}{vv}", size=10.5, color=BODY,
            ha="left", mono=True)
    txt(ax, ax_ + aw - 0.2, ty + 0.30, "roles.ipv4_route", size=10.5, color=ACCENT,
        ha="right", mono=True)
    # B convert.py
    bx, bw = 4.3, 2.35
    box(ax, bx, ty, bw, th)
    txt(ax, bx + bw / 2, ty + 0.30, "convert.py", size=14, weight="bold")
    txt(ax, bx + bw / 2, ty + 0.80, f"{E['taken_out']}", size=22, weight="bold")
    txt(ax, bx + bw / 2, ty + 1.22, "package entries\ntaken out", size=11.5, color=MUTED)
    # C pre-flight
    cx, cwid = 7.05, 2.75
    box(ax, cx, ty, cwid, th)
    txt(ax, cx + cwid / 2, ty + 0.30, "pre-flight", size=14, weight="bold")
    for k, s in enumerate(("roles resolve", "no package entries")):
        yy = ty + 0.78 + k * 0.40
        txt(ax, cx + 0.25, yy, "PASS", size=11.5, weight="bold", color=GREEN, ha="left")
        txt(ax, cx + 0.88, yy, s, size=12, color=BODY, ha="left")
    # D ndt up
    dx, dw = 10.2, 2.68
    box(ax, dx, ty, dw, th)
    txt(ax, dx + dw / 2, ty + 0.30, "ndt up p4 --app", size=14, weight="bold")
    txt(ax, dx + dw / 2, ty + 0.80, f"{E['initial'][0]} of {E['initial'][1]}", size=22,
        weight="bold")
    txt(ax, dx + dw / 2, ty + 1.22, "routes written\nby the proxy", size=11.5, color=MUTED)
    for xa, xb in ((ax_ + aw, bx), (bx + bw, cx), (cx + cwid, dx)):
        arrow(ax, xa + 0.03, ty + th / 2, xb - 0.03, ty + th / 2)

    # ---------------- READ THE CODE: the write path at trunk 3d740be0
    ry = 3.35
    txt(ax, 0.45, ry, f"READ THE CODE  ·  trunk {TRUNK}", size=12, weight="bold", color=FAINT,
        ha="left")
    py0, py1 = 3.6, 6.4                         # the proxy panel
    px0, px1 = 3.0, 9.95
    box(ax, px0, py0, px1 - px0, py1 - py0, fill=PANEL, edge=RULE, lw=1.0, r=0.08, z=1)
    txt(ax, px0 + 0.18, py0 + 0.24, "P4 PROXY", size=11, weight="bold", color=FAINT,
        ha="left")
    rowy, rowh = 4.0, 0.95
    # kernel
    kx, kw = 0.45, 2.15
    box(ax, kx, rowy, kw, rowh)
    txt(ax, kx + kw / 2, rowy + 0.30, "kernel", size=14, weight="bold")
    txt(ax, kx + kw / 2, rowy + 0.66, "installAnEntry", size=10.5, color=BODY, mono=True)
    # route_flow
    fx, fw = 3.25, 2.45
    box(ax, fx, rowy, fw, rowh)
    txt(ax, fx + fw / 2, rowy + 0.30, "route_flow", size=14, weight="bold", mono=True)
    txt(ax, fx + fw / 2, rowy + 0.66, "/stats/flowentry/add", size=10.5, color=BODY,
        mono=True)
    arrow(ax, kx + kw + 0.03, rowy + rowh / 2, fx - 0.03, rowy + rowh / 2)
    # install_initial_routes (the proxy's own caller, at start)
    ix, iy, ih = 3.25, 5.3, 0.8
    box(ax, ix, iy, fw, ih)
    txt(ax, ix + fw / 2, iy + 0.28, "install_initial_routes", size=10.5, weight="bold",
        mono=True)
    txt(ax, ix + fw / 2, iy + 0.56, "at start", size=11, color=MUTED)
    # RouteBinding
    bx2, bw2 = 6.95, 2.55
    box(ax, bx2, rowy, bw2, rowh, fill=ACCENT_BG, edge=ACCENT, lw=2.4)
    txt(ax, bx2 + bw2 / 2, rowy + 0.30, "RouteBinding", size=14, weight="bold", color=ACCENT)
    txt(ax, bx2 + bw2 / 2, rowy + 0.66, "table · match · action", size=11, color=BODY)
    arrow(ax, fx + fw + 0.03, rowy + rowh / 2, bx2 - 0.03, rowy + rowh / 2)
    arrow(ax, ix + fw + 0.03, iy + ih / 2, bx2 - 0.03, rowy + rowh - 0.12)
    # refusal
    ux, uy, uh = bx2, 5.3, 0.8
    box(ax, ux, uy, bw2, uh, fill=WARN_BG, edge=WARNC, lw=1.4)
    txt(ax, ux + bw2 / 2, uy + 0.28, "no roles → 501", size=12.5, weight="bold", color=WARNC)
    txt(ax, ux + bw2 / 2, uy + 0.56, "unsupported_on_p4", size=10.5, color=WARNC, mono=True)
    arrow(ax, bx2 + bw2 / 2, rowy + rowh + 0.03, bx2 + bw2 / 2, uy - 0.03, color=WARNC)
    # the switch
    sx, sw = 10.55, 2.33
    box(ax, sx, rowy - 0.1, sw, rowh + 0.2, fill=WHITE, edge=INK, lw=1.4)
    txt(ax, sx + sw / 2, rowy + 0.20, "bmv2 × 4", size=14, weight="bold")
    txt(ax, sx + sw / 2, rowy + 0.52, "its own", size=11, color=MUTED)
    txt(ax, sx + sw / 2, rowy + 0.80, r["table"], size=10.5, color=BODY, mono=True)
    arrow(ax, bx2 + bw2 + 0.03, rowy + rowh / 2, sx - 0.03, rowy + rowh / 2, color=ACCENT,
          lw=1.8)
    txt(ax, (bx2 + bw2 + sx) / 2, rowy + rowh / 2 - 0.2, "P4Runtime", size=11, color=ACCENT)
    txt(ax, (bx2 + bw2 + sx) / 2, rowy + rowh / 2 + 0.22, "Write", size=11, color=ACCENT)
    # pre-flight and the proxy run one resolve()
    rx = cx + cwid / 2 - 0.25
    ax.plot([rx, rx], [ty + th + 0.03, rowy - 0.03], color=ACCENT, ls=(0, (4, 3)), lw=1.5,
            zorder=3)
    txt(ax, rx + 0.12, 3.12, "same resolve()", size=11, color=ACCENT, ha="left", mono=True)
    save(fig, "fig_r2_roles_path")


# ------------------------------------------------------------------ fig_r3
ROW_LABELS = {
    "L1": "links up in the graph",
    "L2": "kernel write, read back",
    "L3": "pingall at bring-up",
    "L4": "cut held, recovered",
    "L5": "no roles → 501",
    "L6": "capabilities",
}


def fig_r3(E):
    W, H = 13.33, 6.3
    fig, ax = canvas(W, H)
    title(ax, "Live 07: roles on basic, run twice")
    # ---- left: the verdict grid
    cx0, cw, rh, gapx = 3.6, 1.25, 0.6, 0.1
    ytop = 1.95
    cols = (("24", "09-24", "no heartbeat"), ("26", "09-26", "heartbeat on"))
    txt(ax, 0.45, 1.02, "verdict per cell", size=12, weight="bold", color=FAINT, ha="left")
    for j, (key, day, hb) in enumerate(cols):
        x = cx0 + j * (cw + gapx) + cw / 2
        txt(ax, x, 1.38, day, size=14, weight="bold")
        txt(ax, x, 1.66, hb, size=11, color=MUTED)
    for i in range(1, 7):
        c = f"L{i}"
        y = ytop + (i - 1) * (rh + 0.1)
        txt(ax, 0.45, y + rh / 2, c, size=14, weight="bold", color=ACCENT, ha="left")
        txt(ax, 0.95, y + rh / 2, ROW_LABELS[c], size=13, ha="left")
        for j, (key, *_rest) in enumerate(cols):
            n = len(E["cells"][key][c])
            x = cx0 + j * (cw + gapx)
            box(ax, x, y, cw, rh, fill=GREEN, edge=GREEN, r=0.05)
            txt(ax, x + cw / 2, y + rh / 2 - 0.1, "PASS", size=13.5, weight="bold",
                color=WHITE)
            txt(ax, x + cw / 2, y + rh / 2 + 0.16, f"{n} check{'s' if n > 1 else ''}",
                size=10.5, color=WHITE)
    # ---- right: the three pingalls
    axp = fig.add_axes([0.555, 0.13, 0.415, 0.62])
    groups = (("up", "bring-up"), ("cut", "during the cut"), ("after", "after recovery"))
    bw, off = 0.34, 0.2
    for gi, (k, _lab) in enumerate(groups):
        for j, key in enumerate(("24", "26")):
            d = E["ping"][key][k]
            x = gi + (-off if j == 0 else off)
            axp.bar(x, d["zero"], bw, color=GREEN, zorder=3)
            if d["lossy"]:
                axp.bar(x, d["lossy"], bw, bottom=d["zero"], color=WARNC, zorder=3)
            if d["zero"]:
                axp.text(x, d["zero"] / 2, str(d["zero"]), ha="center", va="center",
                         fontsize=13, color=WHITE, fontweight="bold", zorder=4)
            if d["lossy"]:
                axp.text(x, d["zero"] + d["lossy"] / 2, str(d["lossy"]), ha="center",
                         va="center", fontsize=13, color=WHITE, fontweight="bold", zorder=4)
            axp.text(x, -0.45, ("09-24", "09-26")[j], ha="center", va="top", fontsize=11,
                     color=MUTED)
    axp.set_xlim(-0.55, 2.55)
    axp.set_ylim(0, 12)
    axp.set_yticks([0, 3, 6, 9, 12])
    axp.set_xticks([0, 1, 2])
    axp.set_xticklabels([g[1] for g in groups], fontsize=13, color=INK)
    axp.tick_params(axis="x", length=0, pad=26)
    axp.tick_params(axis="y", colors=MUTED, labelsize=12)
    for s in ("top", "right"):
        axp.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        axp.spines[s].set_color(MUTED)
    axp.grid(axis="y", color=RULE, lw=0.8, zorder=0)
    axp.set_ylabel("host pairs (of 12)", fontsize=13, color=MUTED, labelpad=8)
    # the one key annotation: the cut-time numbers are recorded, not asserted
    axp.annotate("recorded, not asserted", xy=(1, 12), xytext=(1, 12.55), ha="center",
                 va="bottom", fontsize=12, color=WARNC, annotation_clip=False)
    txt(ax, 0.505 * W, 1.02, "pingall, every ordered host pair", size=12, weight="bold",
        color=FAINT, ha="left")
    # legend
    lgx, lgy = 0.505 * W + 3.55, 1.02
    ax.add_patch(Rectangle((lgx, lgy - 0.1), 0.2, 0.2, facecolor=GREEN, edgecolor="none"))
    txt(ax, lgx + 0.3, lgy, "0% loss", size=12, color=MUTED, ha="left")
    ax.add_patch(Rectangle((lgx + 1.35, lgy - 0.1), 0.2, 0.2, facecolor=WARNC,
                           edgecolor="none"))
    txt(ax, lgx + 1.65, lgy, "packets lost", size=12, color=MUTED, ha="left")
    save(fig, "fig_r3_live07")


# ------------------------------------------------------------------ fig_r4
FIELDS = ("ipv4_route", "five_tuple", "reroute", "link_discovery", "binding_source")
CAN = {("ipv4_route", "ndtwin"), ("five_tuple", True), ("reroute", True),
       ("link_discovery", "heartbeat"), ("link_discovery", "lldp")}
CANNOT = {("ipv4_route", "unbound"), ("ipv4_route", "package"), ("five_tuple", False),
          ("reroute", False), ("link_discovery", "declared"), ("link_discovery", "none")}


def word(v):
    return "null" if v is None else ("true" if v is True else ("false" if v is False else v))


# the fabric-wide `reroute` the proxy reports beside the switches, per package, as the .md states it
R4_REROUTE = {"roles": (True, None), "plain": (False, "unbound")}
R4_FILES = (("roles", "30_switch_state_roles.json"), ("plain", "71_switch_state_plain.json"))


def run_day(run):
    """MM-DD (UTC) of a run directory named <YYYY-MM-DD>T<HHMMSS>Z_<name>."""
    m = re.match(r"\d{4}-(\d{2})-(\d{2})T\d{6}Z_", os.path.basename(run))
    if not m:
        die(f"{os.path.basename(run)}: run directory name carries no UTC date")
    return f"{m.group(1)}-{m.group(2)}"


def r4_final(E):
    """fig_r4 draws the final state only (template v1.8, 2026-09-29 UTC): what every switch
    reported in the newest live 07 run, R26, for the roles and the no-roles package.
    [Co-developed with claude code -- Adam]"""
    # 1. R26 is the final state only while no newer live 07 run exists
    runs = sorted(glob.glob(os.path.join(LIVE, "*_07_roles_basic")))
    newest = runs[-1] if runs else None
    if newest is None or os.path.realpath(newest) != os.path.realpath(R26):
        die(f"the newest live 07 run is {os.path.basename(newest or '(none)')}, not "
            f"{os.path.basename(R26)}: fig_r4 draws {os.path.basename(R26)} as the final "
            f"state -- redraw it from the newest run")
    out = {}
    for pkg, f in R4_FILES:
        doc = jload(os.path.join(R26, f))
        caps, n, m = E["caps"][("26", pkg)]
        # 2. the proxy's fabric-wide reroute must say what every switch's capabilities say
        rr = doc.get("reroute") or {}
        got = (rr.get("available"), rr.get("reason"))
        if got[0] is not caps.get("reroute") or got != R4_REROUTE[pkg]:
            die(f"{f}: top-level reroute (available, reason) {got} does not match the switches' "
                f"capabilities.reroute {caps.get('reroute')!r} / the .md's {R4_REROUTE[pkg]}")
        # 3. link_discovery "heartbeat" is a final state only if the heartbeat fed every
        #    declared link direction when the file was saved, and none was down
        links = doc.get("links") or {}
        want = (doc.get("declared_links") or {}).get("directions")
        off = sorted(k for k, v in links.items()
                     if v.get("source") != "heartbeat" or v.get("down") is not False)
        if caps.get("link_discovery") != "heartbeat" or not links or len(links) != want or off:
            die(f"{f}: link_discovery {caps.get('link_discovery')!r}, {len(links)} links for "
                f"{want} declared directions, not heartbeat-fed or down: {off}")
        out[pkg] = (caps, n, m)
    return out


def fig_r4(E):
    fin = r4_final(E)
    for pkg, (caps, n, _m) in fin.items():
        if set(caps) != set(FIELDS):
            die(f"capabilities keys changed in 26/{pkg}: {sorted(caps)}")
        for f in FIELDS[:4]:
            if (f, caps[f]) not in CAN | CANNOT:
                die(f"unclassified value {f}={caps[f]!r} in 26/{pkg}")
    W, H = 13.33, 5.2
    fig, ax = canvas(W, H)
    title(ax, "What each switch reports: capabilities")
    txt(ax, 0.45, 1.10, f"RAN IT  ·  live 07, {run_day(R26)}", size=12, weight="bold",
        color=FAINT, ha="left")
    cx0, cw = 3.95, 1.49
    heads = FIELDS + ("switches",)
    for j, h in enumerate(heads):
        txt(ax, cx0 + j * cw + cw / 2, 1.62, h, size=11.5 if h != "switches" else 13,
            color=MUTED, mono=h != "switches")
    y, rh, gap = 1.95, 0.95, 0.2
    for i, (pkg, lab) in enumerate((("roles", "basic + roles"), ("plain", "basic, no roles"))):
        yy = y + i * (rh + gap)
        caps, n, m = fin[pkg]
        txt(ax, 0.45, yy + rh / 2, lab, size=16, weight="bold", ha="left")
        for j, f in enumerate(heads):
            x = cx0 + j * cw
            if f == "switches":
                txt(ax, x + cw / 2, yy + rh / 2, f"{m} of {n}", size=14.5, color=BODY)
                continue
            v = caps[f]
            if f == "binding_source":
                fill, edge, col = WHITE, RULE, BODY
            elif (f, v) in CAN:
                fill, edge, col = GREEN, GREEN, WHITE
            else:
                fill, edge, col = GREY, GREY, INK
            box(ax, x + 0.05, yy, cw - 0.1, rh, fill=fill, edge=edge, lw=1.0, r=0.05)
            txt(ax, x + cw / 2, yy + rh / 2, word(v), size=14, color=col, mono=True,
                weight="bold" if fill == GREEN else "normal")
    # legend
    ly = y + 2 * rh + gap + 0.62
    items = ((GREEN, GREEN, "can"), (GREY, GREY, "cannot"), (WHITE, RULE, "where it came from"))
    lx = cx0
    for fill, edge, lab in items:
        ax.add_patch(Rectangle((lx, ly - 0.11), 0.22, 0.22, facecolor=fill, edgecolor=edge,
                               lw=1.0))
        txt(ax, lx + 0.32, ly, lab, size=12, color=MUTED, ha="left")
        lx += 0.32 + 0.12 * len(lab) + 0.55
    save(fig, "fig_r4_capabilities")
    for pkg, v in fin.items():
        print(f"[r4] 26/{pkg}: {v[0]} on {v[1]} switches ({os.path.basename(R26)}, "
              f"{E['head26'][:8]} +{E['dirty26']} dirty)")


FIGS = {"fig_r1_four_rulings": fig_r1, "fig_r2_roles_path": fig_r2,
        "fig_r3_live07": fig_r3, "fig_r4_capabilities": fig_r4}


def main(argv=None):
    ap = argparse.ArgumentParser(description="the four roles figures of the 930 deck")
    ap.add_argument("--only", action="append", choices=sorted(FIGS),
                    help="draw only this figure (repeatable); evidence is checked in full")
    a = ap.parse_args(argv)
    E = evidence()
    for key in ("24", "26"):
        print(f"[r3] {key}: " + ", ".join(f"{c} {len(v)}" for c, v in E["cells"][key].items())
              + f"; ping {E['ping'][key]}")
    for name, draw in FIGS.items():
        if a.only and name not in a.only:
            print(f"[skip] {name} (not in --only)")
            continue
        draw(E)
    return 0


if __name__ == "__main__":
    sys.exit(main())
