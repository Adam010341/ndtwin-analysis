#!/usr/bin/env python3
"""
make_heartbeat_extra_figs.py -- the other four heartbeat figures of the 2026-09-30 report.

    fig_h0_why_not_lldp          why NDTwin's own link discovery cannot run on a foreign pipeline
    fig_h0b_heartbeat_path       the veth heartbeat, from the wire to the kernel graph
    fig_h3_upper_bound           the detection bound, (15 - phi) + psi + d + eps, observed vs design
    fig_h4_forwarding_unchanged  26 arms with and without the heartbeat under them

Every name on the two diagrams is asserted to still be in the code it comes from (the .md
gives file:line); every number on the two charts is read at run time from the live raw:
  live-p1/runs/2026-09-26T152605Z_08_heartbeat/30_cycles.tsv   (H1 cycles)
  live-p1/runs/<UTC>_06_thirteen/00_table.tsv                   (the 06 runs compared)
  live-p1/runs/2026-09-26T172912Z_08_heartbeat/50_samples.tsv  (H5 report sampler)
Those raw files are uncommitted observations in the kernel checkout.

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/heartbeat"
    "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_heartbeat_extra_figs.py
"""
import csv
import json
import os
import re
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
plt.rcParams["hatch.linewidth"] = 1.2

REPO = os.environ.get("NDTWIN_REPO", "/home/adam/Desktop/NDTwin-Kernel")
PREP = os.path.join(REPO, "doc/audit/2026-09-04_p4-tutorial-exercise-prep")
RUNS = os.path.join(PREP, "live-p1/runs")
H14 = os.path.join(RUNS, "2026-09-26T152605Z_08_heartbeat")
H5 = os.path.join(RUNS, "2026-09-26T172912Z_08_heartbeat")
CODE = {
    "main": os.path.join(REPO, "p4_proxy/proxy_agent/main.py"),
    "p4": os.path.join(REPO, "p4_proxy/p4_src/ndtwin_switch.p4"),
    "hb": os.path.join(REPO, "p4_proxy/proxy_agent/link_heartbeat.py"),
    "topo": os.path.join(REPO, "p4_proxy/proxy_agent/topology_manager.py"),
    "helper": os.path.join(REPO, "tools/test_workflow/ndtwin-lab"),
}
T06_BASIC = os.path.join(PREP, "runs/2026-09-27T074826Z_basic_solution_ndtwin.md")
# H1's footer (judge round 3, coordinator ruling 2026-09-27 UTC): the skipped list comes from the
# 09-24 run, before the heartbeat existed -- there all three skips were true.  In T06 the same
# list still says link_watchdog while the heartbeat watchdog was running (a known misreport,
# fixed on a branch), so T06 is no longer the source.
RUN0924 = os.path.join(PREP, "live-p1/runs/2026-09-24T160256Z_07_roles_basic")
REF_06 = "2026-09-24T185505Z"              # the last full run before the heartbeat existed
HB_06 = ["2026-09-26T153300Z", "2026-09-26T172913Z", "2026-09-27T074635Z"]

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
WARNC, WARN_BG, WHITE, GREEN = "#9C3B2E", "#FBF2F0", "#FFFFFF", "#2F7D4F"
GREY = "#C9CDD0"


def die(msg):
    raise SystemExit(f"make_heartbeat_extra_figs: {msg}")


def read(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def must(p, *needles):
    t = read(p)
    for n in needles:
        if n not in t:
            die(f"{p} no longer contains {n!r}")


def const(p, name):
    m = re.search(rf"^{name}\s*=\s*(.+?)\s*(#.*)?$", read(p), re.M)
    if not m:
        die(f"{name} not found in {p}")
    return m.group(1)


def save(fig, name):
    os.makedirs(HIRES, exist_ok=True)
    for ext in ("pdf", "png", "svg"):
        kw = {"dpi": 300} if ext == "png" else {}
        fig.savefig(os.path.join(OUTDIR, f"{name}.{ext}"), facecolor=WHITE, **kw)
    fig.savefig(os.path.join(HIRES, f"{name}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"[out] {name}")


def canvas(h, title):
    W = 13.33
    fig = plt.figure(figsize=(W, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(h, 0)
    ax.axis("off")
    ax.text(0.45, 0.48, title, fontsize=22, fontweight="bold", color=INK, va="center")
    return fig, ax


def box(ax, x, y, w, h, fill=WHITE, edge=INK, lw=1.2, ls="solid", r=0.06, z=2):
    ax.add_patch(FancyBboxPatch((x + r, y + r), w - 2 * r, h - 2 * r,
                                boxstyle=f"round,pad={r},rounding_size={r}", facecolor=fill,
                                edgecolor=edge, linewidth=lw, linestyle=ls, zorder=z))


def txt(ax, x, y, s, size=13, color=INK, weight="normal", ha="center", va="center",
        mono=False, z=6):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, zorder=z,
            family="monospace" if mono else None, linespacing=1.25)


def arrow(ax, x0, y0, x1, y1, color=INK, lw=1.5, ls="solid", z=3, rad=0.0):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=14,
                                 color=color, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0,
                                 connectionstyle=f"arc3,rad={rad}", zorder=z))


# ---------------------------------------------------------------------------
def footer_skipped():
    """The footer's skipped list, from the 09-24 run: the `ndt up` verify line (70_up_plain.txt)
    and the proxy's own switch_state of the same bring-up (71_switch_state_plain.json) must name
    the same three items, and a list that says `link_watchdog` is skipped must not come with a
    heartbeat watchdog that is running in that same switch_state."""
    up = read(os.path.join(RUN0924, "70_up_plain.txt"))
    m = re.search(r"control_plane\.skipped:\s*([a-z_, ]+)\)", up)
    if not m:
        die("09-24 70_up_plain.txt: no control_plane.skipped line")
    items_up = sorted(x.strip() for x in m.group(1).split(","))
    with open(os.path.join(RUN0924, "71_switch_state_plain.json")) as f:
        cp = json.load(f).get("control_plane", {})
    items = sorted(cp.get("skipped", []))
    if items != items_up:
        die(f"09-24: switch_state skipped {items} != the up log's {items_up}")
    if items != ["install_initial_routes", "link_watchdog", "lldp_discovery"]:
        die(f"09-24: unexpected skipped list {items}")
    wd = (cp.get("heartbeat") or {}).get("watchdog")
    if "link_watchdog" in items and wd == "running":
        die("footer: link_watchdog is listed as skipped, but the same switch_state has the "
            "heartbeat watchdog running")
    code = re.search(r"code\s+([0-9a-f]{8})\s+\+(\d+) file", read(os.path.join(RUN0924,
                                                                        "00_status_before.txt")))
    if not code:
        die("09-24: no code line in 00_status_before.txt")
    print(f"[h0] footer from 09-24 (code {code.group(1)} +{code.group(2)}): skipped {items}; "
          f"heartbeat watchdog {wd!r}")
    return items, (code.group(1), code.group(2))


def fig_h0():
    must(CODE["main"], "LLDP discovery, the link watchdog and (through them) "
                       "install_initial_routes all ride",
         "packet-out and packet-in. Those need a controller header")
    must(CODE["p4"], '@controller_header("packet_in")', '@controller_header("packet_out")')
    items, run_code = footer_skipped()
    fig, ax = canvas(6.2, "Why link discovery stops at a foreign P4")
    for k, (title, own) in enumerate((("NDTwin's own P4", True), ("a foreign P4 program", False))):
        x0 = 0.45 + k * 6.55
        box(ax, x0, 0.95, 6.2, 4.15, fill=PANEL, edge=RULE, lw=1.0, r=0.08, z=1)
        txt(ax, x0 + 6.0, 1.25, "READ THE CODE", size=11, weight="bold", ha="right",
            color=FAINT)
        txt(ax, x0 + 0.25, 1.25, title, size=15, weight="bold", ha="left",
            color=INK if own else WARNC)
        # proxy on top, two switches below
        box(ax, x0 + 2.1, 1.65, 2.0, 0.8)
        txt(ax, x0 + 3.1, 2.05, "P4 proxy", size=14, weight="bold")
        for j, sw in enumerate(("switch A", "switch B")):
            sx = x0 + 0.5 + j * 3.6
            box(ax, sx, 3.45, 1.6, 0.8)
            txt(ax, sx + 0.8, 3.85, sw, size=13.5, weight="bold")
        # the link between them
        ax.plot([x0 + 2.1, x0 + 4.1], [3.85, 3.85], color=MUTED, lw=2.5, zorder=1)
        if own:
            arrow(ax, x0 + 2.3, 2.47, x0 + 1.4, 3.43, color=ACCENT)
            txt(ax, x0 + 1.25, 2.85, "packet-out", size=12, color=ACCENT, ha="right")
            arrow(ax, x0 + 4.8, 3.43, x0 + 3.9, 2.47, color=ACCENT)
            txt(ax, x0 + 4.95, 2.85, "packet-in", size=12, color=ACCENT, ha="left")
            txt(ax, x0 + 3.1, 3.62, "LLDP", size=12, color=ACCENT)
            box(ax, x0 + 1.6, 4.45, 3.0, 0.5, fill=WHITE, edge=GREEN, lw=1.6)
            txt(ax, x0 + 3.1, 4.70, "link seen", size=13.5, color=GREEN, weight="bold")
        else:
            arrow(ax, x0 + 2.3, 2.47, x0 + 1.4, 3.43, color=WARNC, ls=(0, (4, 3)))
            txt(ax, x0 + 1.25, 2.85, "packet-out", size=12, color=WARNC, ha="right")
            cx_, cy_, d_ = x0 + 1.85, 2.95, 0.13
            ax.plot([cx_ - d_, cx_ + d_], [cy_ - d_, cy_ + d_], color=WARNC, lw=3, zorder=6)
            ax.plot([cx_ - d_, cx_ + d_], [cy_ + d_, cy_ - d_], color=WARNC, lw=3, zorder=6)
            txt(ax, x0 + 4.95, 2.85, "no controller\nheader", size=12, color=WARNC,
                ha="left")
            box(ax, x0 + 1.6, 4.45, 3.0, 0.5, fill=WHITE, edge=WARNC, lw=1.6)
            txt(ax, x0 + 3.1, 4.70, "no link seen", size=13.5, color=WARNC, weight="bold")
    # the footer is the one ran-it item on this page (T06's arm report); the two panels above
    # are read from code -- rule 3: say which is which on the canvas
    txt(ax, 0.45, 5.55, "RAN IT · 09-24, before the heartbeat · skipped on a foreign fabric:",
        size=12.5, color=MUTED, ha="left")
    txt(ax, 6.55, 5.55, "   ·   ".join(sorted(items)), size=12.5, color=WARNC, ha="left",
        mono=True)
    save(fig, "fig_h0_why_not_lldp")
    return items


# ---------------------------------------------------------------------------
def fig_h0b():
    ethertype = const(CODE["helper"], "ETHERTYPE")
    period = const(CODE["helper"], "PERIOD_S")
    rep_min = const(CODE["helper"], "REPORT_MIN_INTERVAL_S")
    report = const(CODE["hb"], "REPORT_PATH").strip('"')
    beacon = const(CODE["topo"], "LLDP_BEACON_INTERVAL_S")
    timeout = const(CODE["topo"], "LINK_BEACON_TIMEOUT_S")
    wd = const(CODE["topo"], "LINK_WATCHDOG_INTERVAL_S")
    if (ethertype, period, beacon, timeout, wd) != ("0x88B5", "5", "5",
                                                     "3 * LLDP_BEACON_INTERVAL_S",
                                                     "LLDP_BEACON_INTERVAL_S"):
        die(f"constants moved: {ethertype} {period} {beacon} {timeout} {wd}")
    must(CODE["topo"], "def check_link_beacons", "def _notify_link")
    print(f"[h0b] ethertype {ethertype} period {period} s report {report} (min rewrite "
          f"{rep_min} s); proxy beacon {beacon} s timeout {timeout} watchdog {wd}")

    fig, ax = canvas(6.2, "The veth heartbeat, from wire to kernel graph")
    # fabric: two switches and the veth between them
    box(ax, 0.45, 1.3, 3.2, 3.3, fill=PANEL, edge=RULE, lw=1.0, r=0.08, z=1)
    txt(ax, 0.62, 1.58, "FABRIC", size=11.5, color=FAINT, weight="bold", ha="left")
    for j, sw in enumerate(("s1", "s3")):
        y = 1.95 + j * 1.75
        box(ax, 0.95, y, 1.5, 0.8)
        txt(ax, 1.70, y + 0.40, sw, size=14, weight="bold", mono=True)
    ax.plot([1.70, 1.70], [2.77, 3.68], color=GREEN, lw=3.0, zorder=1)
    txt(ax, 1.55, 3.22, "veth", size=12, color=GREEN, ha="right")
    # root helper
    box(ax, 4.15, 1.3, 2.5, 1.55, edge=GREEN, lw=1.8)
    txt(ax, 5.40, 1.72, "root helper", size=14, weight="bold", color=GREEN)
    txt(ax, 5.40, 2.28, f"{ethertype} frame\nevery {period} s", size=12, color=MUTED)
    arrow(ax, 4.13, 1.85, 1.82, 2.95, color=GREEN)
    arrow(ax, 1.82, 3.45, 4.13, 2.60, color=GREEN)
    txt(ax, 3.05, 2.12, "send", size=11.5, color=GREEN)
    txt(ax, 3.05, 3.30, "hear", size=11.5, color=GREEN)
    # report file
    box(ax, 4.15, 3.30, 2.5, 1.30, edge=MUTED, lw=1.2, ls=(0, (4, 3)))
    txt(ax, 5.40, 3.72, "report", size=14, weight="bold", color=BODY)
    txt(ax, 5.40, 4.20, "last heard,\nper direction", size=12, color=MUTED)
    arrow(ax, 5.40, 2.87, 5.40, 3.28, color=MUTED)
    # proxy watchdog
    box(ax, 7.15, 2.40, 2.75, 1.65, edge=ACCENT, lw=1.8)
    txt(ax, 8.525, 2.82, "proxy watchdog", size=14, weight="bold", color=ACCENT)
    txt(ax, 8.525, 3.45, f"every {period} s:\nsilent > 15 s → down", size=12, color=MUTED)
    arrow(ax, 6.67, 3.95, 7.13, 3.40, color=ACCENT)
    # kernel
    box(ax, 10.4, 1.30, 2.5, 1.30, edge=INK, lw=1.4)
    txt(ax, 11.65, 1.72, "kernel graph", size=14, weight="bold")
    txt(ax, 11.65, 2.18, "is_up", size=12.5, color=MUTED, mono=True)
    arrow(ax, 9.92, 2.75, 10.38, 2.20, color=INK)
    # reroute back to the fabric, only where NDTwin owns the route table
    box(ax, 10.4, 3.30, 2.5, 1.30, edge=INK, lw=1.4)
    txt(ax, 11.65, 3.72, "reroute", size=14, weight="bold")
    txt(ax, 11.65, 4.18, "owned tables only", size=12, color=MUTED)
    arrow(ax, 9.92, 3.70, 10.38, 3.95, color=INK)
    ax.add_patch(FancyArrowPatch((11.65, 4.62), (2.45, 4.35), arrowstyle="-|>",
                                 mutation_scale=14, color=MUTED, lw=1.3, ls=(0, (4, 3)),
                                 connectionstyle="arc3,rad=-0.12", shrinkA=0, shrinkB=0,
                                 zorder=3))
    txt(ax, 7.0, 5.35, "P4Runtime", size=12, color=MUTED)
    save(fig, "fig_h0b_heartbeat_path")


# ---------------------------------------------------------------------------
def fig_h3():
    with open(os.path.join(H14, "30_cycles.tsv"), newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    r = max(rows, key=lambda x: float(x["detect_s"]))
    phi = float(r["phi_s"])
    last = max(float(r["last_heard_ab_mono"]), float(r["last_heard_ba_mono"]))
    cut = float(r["cut_a_start_mono"])
    pass_s = float(r["pass_start_mono"])
    down = float(r["graph_down_mono"])
    rule = last + 15.0
    seg_rule = rule - cut                      # = 15 - phi (phi measured from the cut start)
    seg_psi = pass_s - rule                    # watchdog wait after the rule holds
    seg_d = down - pass_s                      # pass + HTTP + kernel + the script's poll
    total = float(r["detect_s"])
    if abs(seg_rule + seg_psi + seg_d - total) > 0.003:
        die(f"segments {seg_rule}+{seg_psi}+{seg_d} != detect {total}")
    if abs(seg_psi - float(r["watchdog_phase_s"])) > 0.003:
        die("psi does not match watchdog_phase_s")
    if abs(seg_d - float(r["pass_to_graph_s"])) > 0.003:
        die("d does not match pass_to_graph_s")
    ds = [float(x["pass_to_graph_s"]) for x in rows]
    print(f"[h3] cycle {r['cycle']}: 15-phi {seg_rule:.3f} + psi {seg_psi:.3f} + d {seg_d:.3f}"
          f" = {total:.3f}; d over the 6 cycles {min(ds):.3f}-{max(ds):.3f}")

    fig, ax = canvas(5.2, "The detection bound, piece by piece")
    ax2 = fig.add_axes([0.20, 0.22, 0.76, 0.52])
    rows_ = [("observed worst\n(live, 6 cuts)", [(seg_rule, "15 s − φ", ACCENT),
                                                (seg_psi, "ψ", "#6FA1BD"),
                                                (seg_d, "d + ε", GREY)], total),
             ("design worst\n(φ → 0, ψ → 5 s)", [(15.0, "15 s", ACCENT),
                                                 (5.0, "ψ = 5 s", "#6FA1BD")], 20.0)]
    for i, (lab, segs, tot) in enumerate(rows_):
        y = 1 - i
        x = 0.0
        for w, name, c in segs:
            ax2.barh(y, w, left=x, height=0.52, color=c, edgecolor=WHITE, lw=2)
            if w > 1.0:
                ax2.text(x + w / 2, y, name, ha="center", va="center", fontsize=13,
                         color=WHITE, fontweight="bold")
            x += w
        if i == 1:
            ax2.barh(y, 0.6, left=x, height=0.52, color=WHITE, edgecolor=MUTED, lw=1.0,
                     hatch="///")
            ax2.text(x + 0.75, y, "+ d + ε  ≈ 20 s", ha="left", va="center", fontsize=14,
                     color=INK, fontweight="bold")
        else:
            ax2.text(x + 0.15, y, f"{tot:.1f} s", ha="left", va="center", fontsize=14,
                     color=INK, fontweight="bold")
            ax2.annotate("d + ε", xy=(seg_rule + seg_psi + seg_d / 2, y + 0.27),
                         xytext=(0, 10), textcoords="offset points", ha="center",
                         fontsize=12, color=MUTED)
        ax2.text(-0.4, y, lab, ha="right", va="center", fontsize=13.5, color=INK)
    ax2.set_xlim(0, 23.5)
    ax2.set_ylim(-0.6, 1.6)
    ax2.set_yticks([])
    ax2.set_xticks([0, 5, 10, 15, 20])
    ax2.axvline(20, color=WARNC, lw=1.3, ls=(0, (2, 3)))
    for s in ("top", "right", "left"):
        ax2.spines[s].set_visible(False)
    ax2.spines["bottom"].set_color(MUTED)
    ax2.tick_params(colors=MUTED, labelsize=12.5)
    ax2.set_xlabel("seconds from the cut to down on the kernel graph", fontsize=13,
                   color=MUTED, labelpad=8)
    save(fig, "fig_h3_upper_bound")
    return dict(cycle=r["cycle"], rule=seg_rule, psi=seg_psi, d=seg_d, total=total,
                d_min=min(ds), d_max=max(ds))


# ---------------------------------------------------------------------------
def table06(stamp):
    p = os.path.join(RUNS, f"{stamp}_06_thirteen/00_table.tsv")
    with open(p, newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    if len(rows) != 26:
        die(f"{p}: {len(rows)} rows")
    return {(r["exercise"], r["which"]): (r["rc"], r["verdict"], r["report"]) for r in rows}


def fig_h4():
    ref = table06(REF_06)
    cols = [(REF_06, ref, False)]
    for s in HB_06:
        t = table06(s)
        cols.append((s, t, True))
        diff = [k for k in ref if (ref[k][0], ref[k][1]) != (t[k][0], t[k][1])]
        if diff:
            die(f"{s} differs from {REF_06} on {diff}")
    # which arms ran with the heartbeat under them (the arm report says so)
    def hb(report):
        return os.path.isfile(report) and "heartbeat started (pid" in read(report)
    n_hb = {s: sum(hb(v[2]) for v in t.values()) for s, t, on in cols}
    if n_hb[REF_06] != 0 or any(n_hb[s] != 17 for s in HB_06):
        die(f"heartbeat arm counts {n_hb}")
    with open(os.path.join(H5, "50_samples.tsv"), newline="") as f:
        samples = list(csv.DictReader(f, delimiter="\t"))
    fwd = sum(int(x["forwarded_to_hosts"]) for x in samples)
    sessions = len({x["session"] for x in samples if x["status"] == "running"})
    if fwd != 0:
        die(f"forwarded_to_hosts sums to {fwd}")
    print(f"[h4] {len(HB_06)} heartbeat runs identical to {REF_06} on 26/26 arms (rc+verdict);"
          f" heartbeat arms {n_hb}; H5 sampler {len(samples)} samples, {sessions} sessions, "
          f"forwarded_to_hosts {fwd}")

    order = ["basic", "qos", "ecn", "mri", "firewall", "basic_tunnel", "source_routing",
             "calc", "link_monitor", "load_balance", "multicast", "p4runtime", "flowcache"]
    fig, ax = canvas(7.35, "Heartbeat on, forwarding unchanged")
    left, top, cw, ch, gap = 2.3, 1.75, 0.36, 0.34, 0.32
    for j, (s, t, on) in enumerate(cols):
        x0 = left + j * (2 * cw + gap)
        txt(ax, x0 + cw, top - 0.55, s[5:10], size=12)
        txt(ax, x0 + cw, top - 0.30, f"{s[11:13]}:{s[13:15]}", size=10.5, color=MUTED)
        txt(ax, x0 + cw, top - 0.85, "heartbeat" if on else "none", size=11,
            color=GREEN if on else FAINT, weight="bold")
        for i, ex in enumerate(order):
            for k, which in enumerate(("skeleton", "solution")):
                rc, v, rep = t[(ex, which)]
                x, y = x0 + k * cw, top + i * ch
                ax.add_patch(Rectangle((x + 0.02, y + 0.03), cw - 0.04, ch - 0.06,
                                       facecolor=GREEN, edgecolor=GREEN, lw=0.8))
                if on and hb(rep):
                    ax.plot([x + cw / 2], [y + ch / 2], "o", ms=3.2, color=WHITE, zorder=5)
        if j:
            txt(ax, x0 - gap / 2, top + 13 * ch + 0.18, "=", size=16, color=INK,
                weight="bold")
    for i, ex in enumerate(order):
        txt(ax, left - 0.15, top + i * ch + ch / 2, ex, size=12.5, ha="right")
    txt(ax, left - 0.15, top - 0.08, "skeleton | solution", size=10.5, color=MUTED,
        ha="right", va="bottom")
    txt(ax, left - 0.15, top - 0.42, "run (UTC)", size=10.5, color=MUTED, ha="right")
    # the host-side number
    bx = left + len(cols) * (2 * cw + gap) + 0.55
    box(ax, bx, top + 0.2, 13.33 - bx - 0.45, 3.2, fill=PANEL, edge=RULE, lw=1.0, r=0.08,
        z=1)
    cx = bx + (13.33 - bx - 0.45) / 2
    txt(ax, cx, top + 1.15, f"{fwd}", size=54, weight="bold", color=GREEN)
    txt(ax, cx, top + 2.15, "heartbeat frames\nleaving a host port", size=14, color=INK)
    txt(ax, cx, top + 2.95, f"{sessions} heartbeat sessions · run 09-26 17:29Z",
        size=12.5, color=MUTED)
    # legend
    ly = top + 13 * ch + 0.70
    ax.add_patch(Rectangle((left, ly - 0.12), 0.30, 0.24, facecolor=GREEN, edgecolor=GREEN))
    txt(ax, left + 0.40, ly, "as the exercise says", size=12, color=MUTED, ha="left")
    ax.add_patch(Rectangle((left + 3.0, ly - 0.12), 0.30, 0.24, facecolor=GREEN,
                           edgecolor=GREEN))
    ax.plot([left + 3.15], [ly], "o", ms=3.2, color=WHITE)
    txt(ax, left + 3.40, ly, "heartbeat running", size=12, color=MUTED, ha="left")
    save(fig, "fig_h4_forwarding_unchanged")
    return dict(n_hb=n_hb, samples=len(samples), sessions=sessions, fwd=fwd)


def main():
    fig_h0()
    fig_h0b()
    fig_h3()
    fig_h4()
    return 0


if __name__ == "__main__":
    sys.exit(main())
