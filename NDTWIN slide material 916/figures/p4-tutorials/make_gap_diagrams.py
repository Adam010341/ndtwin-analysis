#!/usr/bin/env python3
"""
make_gap_diagrams.py -- the four diagrams for the 909 deck's T2/T3/T4 pages.

    fig_t2_gap_architecture   three-layer architecture, six G badges   (827 E4a)
    fig_t3a_silent_zero       vertical flowchart, silent zero          (827 E4b)
    fig_t3b_election_wipe     sequence diagram, election_id collision
    fig_t4_phases             staircase + the 2x2 of the 09-08 runs

Every number in here comes from
    doc/audit/2026-09-04_p4-tutorial-exercise-prep/GAP-ANALYSIS.md   (§1 table, §3, §5, §6)
    doc/audit/2026-09-04_p4-tutorial-exercise-prep/runs/*.md         (the four 09-08 runs)
and is cited line-by-line in the companion <name>.md next to each figure. This script is the
vector source; the .md is the provenance. Nothing is computed from data files at run time --
the numbers are literals below so the output is byte-stable.

Drawing rules: 827 template E2 (palette + Arial), E4a (architecture), E4b (flowchart).

[Co-developed with claude code -- Adam]

Regenerate:
    "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_gap_diagrams.py

writes, for each of the four names, into this directory:
    <name>.pdf   <name>.png (300 dpi)   <name>.svg   _hires/<name>.png (500 dpi)
"""
import os

import matplotlib

assert matplotlib.__version__.startswith("3.10") or matplotlib.__version__.startswith("3.11"), \
    f"unexpected matplotlib {matplotlib.__version__}; re-verify the figures render as expected"

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, PathPatch, Rectangle
from matplotlib.path import Path

# Arial per 827 E2; Liberation Sans is the metric-compatible stand-in on this laptop, DejaVu
# supplies the few glyphs (arrow, middot) if a fallback is needed.
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["font.monospace"] = ["Courier New", "Liberation Mono", "DejaVu Sans Mono"]
plt.rcParams["svg.fonttype"] = "none"   # keep SVG text editable
plt.rcParams["pdf.fonttype"] = 42       # embed TrueType, not Type 3

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")

# ---- 827 E2 palette --------------------------------------------------------------------
INK = "#1A1A1A"
BODY = "#2E2E2E"
MUTED = "#4F4F4F"
FAINT = "#6E6E6E"
RULE = "#D0D0D0"
ACCENT = "#065A82"
ACCENT_BG = "#EEF3F6"
PANEL = "#F7F8F9"
WARNC = "#9C3B2E"
WARN_BG = "#FBF2F0"
WHITE = "#FFFFFF"

MONO = {"family": "monospace"}


# ---- primitives ------------------------------------------------------------------------
def canvas(w, h):
    """Inch-for-inch canvas, y growing downward (matches how E4a states coordinates)."""
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fill=WHITE, edge=INK, lw=1.0, ls="solid", z=2, radius=0.0):
    if radius:
        p = FancyBboxPatch((x + radius, y + radius), w - 2 * radius, h - 2 * radius,
                           boxstyle=f"round,pad={radius},rounding_size={radius}",
                           facecolor=fill, edgecolor=edge, linewidth=lw, linestyle=ls, zorder=z)
    else:
        p = Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge,
                      linewidth=lw, linestyle=ls, zorder=z)
    ax.add_patch(p)
    return p


def txt(ax, x, y, s, size=9.5, color=INK, weight="normal", ha="center", va="center",
        mono=False, z=5, rot=0, spacing=None):
    kw = dict(MONO) if mono else {}
    if spacing is not None:
        # matplotlib has no letter-spacing; emulate it with thin spaces for the band labels.
        s = (" ").join(s)
    return ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=z, rotation=rot, **kw)


def arrow(ax, x1, y1, x2, y2, color=INK, lw=1.0, ls="-", head=0.09, z=3):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), zorder=z,
                arrowprops=dict(arrowstyle=f"-|>,head_width={head*1.6},head_length={head*2.4}",
                                color=color, linewidth=lw, linestyle=ls,
                                shrinkA=0, shrinkB=0, joinstyle="miter"))


def elbow(ax, pts, color=INK, lw=1.0, ls="-", head=0.09, z=3):
    """Polyline with the arrowhead on the last segment."""
    for a, b in zip(pts[:-1], pts[1:-1]):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw, ls=ls, zorder=z,
                solid_capstyle="butt")
    arrow(ax, *pts[-2], *pts[-1], color=color, lw=lw, ls=ls, head=head, z=z)


# phase -> badge border style. 827 E1: one accent colour only, so the phase rides on the
# border, never on a second hue.
PHASE_STYLE = {1: dict(lw=0.9, ls="solid"),
               2: dict(lw=2.2, ls="solid"),
               3: dict(lw=1.1, ls=(0, (2.2, 1.6)))}


def badge(ax, x, y, w, h, label, phase, size=8.5):
    st = PHASE_STYLE[phase]
    box(ax, x, y, w, h, fill=ACCENT_BG, edge=ACCENT, lw=st["lw"], ls=st["ls"], z=6, radius=0.035)
    txt(ax, x + w / 2, y + h / 2 + 0.005, label, size=size, color=ACCENT, weight="bold", z=7)


def chip(ax, x, y, w, h, label, fill=PANEL, edge=RULE, color=MUTED, size=8.5):
    box(ax, x, y, w, h, fill=fill, edge=edge, lw=0.9, z=6, radius=0.04)
    txt(ax, x + w / 2, y + h / 2 + 0.005, label, size=size, color=color, weight="bold", z=7)


def save(fig, name):
    os.makedirs(HIRES, exist_ok=True)
    fig.savefig(os.path.join(OUTDIR, f"{name}.pdf"), facecolor=WHITE)
    fig.savefig(os.path.join(OUTDIR, f"{name}.png"), facecolor=WHITE, dpi=300)
    fig.savefig(os.path.join(OUTDIR, f"{name}.svg"), facecolor=WHITE)
    fig.savefig(os.path.join(HIRES, f"{name}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"wrote {name}.{{pdf,png,svg}} + _hires/{name}.png")


# ==========================================================================================
# fig_t2 -- where the five gaps live.  827 E4a: apps on top, cloud at the bottom, black
# 1pt outlines on white, the elements being pointed at carry ACCENT, sFlow leaves the PROXY
# (not the bmv2 cloud).
# ==========================================================================================
def fig_t2():
    W, H = 12.44, 7.0
    fig, ax = canvas(W, H)

    # --- band labels ---------------------------------------------------------------------
    txt(ax, 0.50, 0.34, "EXERCISE", size=9, color=MUTED, weight="bold", ha="left", spacing=1)
    txt(ax, 0.50, 2.06, "KERNEL", size=9, color=MUTED, weight="bold", ha="left", spacing=1)
    txt(ax, 6.60, 2.06, "PROXY", size=9, color=MUTED, weight="bold", ha="left", spacing=1)

    # --- top layer: what the exercise brings ---------------------------------------------
    top_y, top_h = 0.52, 0.70
    tops = [("topology.json", 2.09, 1.90),
            ("its .p4", 7.28, 1.20),
            ("sX-runtime.json", 8.66, 1.55),
            ("mycontroller.py", 10.39, 1.55)]
    for label, x, w in tops:
        box(ax, x, top_y, w, top_h)
        txt(ax, x + w / 2, top_y + top_h / 2, label, size=10, color=INK, mono=True)

    # --- middle layer --------------------------------------------------------------------
    grp_y, grp_h = 2.20, 2.05
    box(ax, 0.50, grp_y, 5.40, grp_h, fill="none", edge=RULE, lw=1.0, z=1)
    box(ax, 6.60, grp_y, 5.34, grp_h, fill="none", edge=RULE, lw=1.0, z=1)

    mb_y, mb_h = 2.48, 1.47
    # kernel, left -> right; the sFlow parser sits nearest the proxy so its arrow is one hop
    k_north = (0.70, 1.40)
    k_topo = (2.34, 1.40)
    k_sflow = (3.98, 1.72)
    # proxy, left -> right; the emitter sits nearest the kernel for the same reason
    p_pktin = (6.80, 1.33)
    p_pipe = (8.37, 1.21)
    p_p4rt = (9.82, 1.92)

    def mid_box(spec, badged):
        x, w = spec
        box(ax, x, mb_y, w, mb_h, fill=ACCENT_BG if badged else WHITE)
        return x, w

    mid_box(k_north, False)
    txt(ax, k_north[0] + k_north[1] / 2, mb_y + 0.40, "northbound", size=9.5, color=INK)
    txt(ax, k_north[0] + k_north[1] / 2, mb_y + 0.62, "API", size=9.5, color=INK)

    mid_box(k_topo, True)
    txt(ax, k_topo[0] + k_topo[1] / 2, mb_y + 0.40, "topology", size=9.5, color=INK)
    txt(ax, k_topo[0] + k_topo[1] / 2, mb_y + 0.62, "model", size=9.5, color=INK)
    badge(ax, k_topo[0] + k_topo[1] - 0.76, mb_y + mb_h - 0.40, 0.66, 0.28, "G2  ~85", 1)

    mid_box(k_sflow, True)
    txt(ax, k_sflow[0] + k_sflow[1] / 2, mb_y + 0.40, "sFlow parser", size=9.5, color=INK)
    txt(ax, k_sflow[0] + k_sflow[1] / 2, mb_y + 0.62, "+ FlowKey", size=9.5, color=INK)
    badge(ax, k_sflow[0] + k_sflow[1] - 1.00, mb_y + mb_h - 0.40, 0.90, 0.28, "G6  ~30+250", 3)

    mid_box(p_pktin, True)
    txt(ax, p_pktin[0] + p_pktin[1] / 2, mb_y + 0.40, "packet-in decoder", size=9, color=INK)
    txt(ax, p_pktin[0] + p_pktin[1] / 2, mb_y + 0.62, "→ sFlow emitter", size=9, color=INK)
    badge(ax, p_pktin[0] + p_pktin[1] - 0.72, mb_y + mb_h - 0.40, 0.62, 0.28, "G1  ~40", 1)

    mid_box(p_pipe, True)
    txt(ax, p_pipe[0] + p_pipe[1] / 2, mb_y + 0.40, "pipeline", size=9.5, color=INK)
    txt(ax, p_pipe[0] + p_pipe[1] / 2, mb_y + 0.62, "loader", size=9.5, color=INK)
    badge(ax, p_pipe[0] + p_pipe[1] - 0.80, mb_y + mb_h - 0.40, 0.70, 0.28, "G4  ~150", 2)

    mid_box(p_p4rt, True)
    txt(ax, p_p4rt[0] + p_p4rt[1] / 2, mb_y + 0.28, "P4Runtime client", size=9.5, color=INK)
    # two compartments so the two badges point at two different things
    for i, (name, blabel, ph, bw) in enumerate(
            [("table writer", "G5  ~180", 2, 0.70), ("election_id", "G3  ~15", 1, 0.60)]):
        cy = mb_y + 0.50 + i * 0.44
        box(ax, p_p4rt[0] + 0.10, cy, p_p4rt[1] - 0.20, 0.36, fill=WHITE, edge=RULE, lw=0.9, z=3)
        txt(ax, p_p4rt[0] + 0.20, cy + 0.185, name, size=8.5, color=BODY, ha="left",
            mono=(name == "election_id"), z=5)
        badge(ax, p_p4rt[0] + p_p4rt[1] - 0.20 - bw, cy + 0.04, bw, 0.28, blabel, ph, size=8)

    # --- bottom layer: the fabric --------------------------------------------------------
    cl_x, cl_y, cl_w, cl_h = 2.40, 5.15, 8.80, 1.30
    cloud_top = _cloud(ax, cl_x, cl_y, cl_w, cl_h)
    txt(ax, cl_x + cl_w / 2, cl_y + 0.86, "Mininet fabric  ·  bmv2 × N",
        size=11.5, color=INK, weight="bold")
    txt(ax, cl_x + cl_w / 2, cl_y + 1.11, "one p4info today", size=9, color=MUTED)

    # --- arrows --------------------------------------------------------------------------
    a = dict(color=INK, lw=1.0)
    # exercise -> the thing it lands on
    arrow(ax, 3.04, top_y + top_h, 3.04, mb_y, **a)                       # topology.json
    arrow(ax, 7.88, top_y + top_h, 8.76, mb_y, **a)                       # its .p4
    arrow(ax, 9.43, top_y + top_h, 10.20, mb_y, **a)                      # sX-runtime.json
    arrow(ax, 11.16, top_y + top_h, 11.35, mb_y, **a)                     # mycontroller.py
    # down to the fabric
    for px in (3.04, 8.975, 10.30):
        arrow(ax, px, mb_y + mb_h, px, cloud_top(px) + 0.02, **a)
    # bmv2 clone comes back up into the decoder
    arrow(ax, 7.465, cloud_top(7.465) + 0.02, 7.465, mb_y + mb_h, **a)
    txt(ax, 7.58, 4.68, "bmv2 clone", size=8.5, color=MUTED, ha="left")
    # sFlow leaves the PROXY, not the cloud (E4a)
    arrow(ax, p_pktin[0], mb_y + mb_h / 2, k_sflow[0] + k_sflow[1], mb_y + mb_h / 2, **a)
    txt(ax, (p_pktin[0] + k_sflow[0] + k_sflow[1]) / 2, mb_y + mb_h / 2 - 0.15, "sFlow",
        size=8.5, color=MUTED)

    # --- phase legend --------------------------------------------------------------------
    lx = 0.50
    for i, ph in enumerate((1, 2, 3)):
        badge(ax, lx + i * 1.25, 6.60, 0.36, 0.26, "", ph)
        txt(ax, lx + i * 1.25 + 0.44, 6.73, f"phase {ph}", size=9, color=MUTED, ha="left")

    save(fig, "fig_t2_gap_architecture")


def _cloud(ax, x, y, w, h):
    """A flat-bottomed cloud: bumps rising off a shoulder line, one closed path so the
    outline stays black 1pt on white (E4a). Returns top(px) so arrows can land on it."""
    import numpy as np
    radii = [0.62, 0.46, 0.66, 0.50, 0.58, 0.44, 0.64, 0.48, 0.60]
    x0, x1 = x + radii[0], x + w - radii[-1]
    cxs = np.linspace(x0, x1, len(radii))
    shoulder = y + h * 0.48
    cy = y + h * 0.52

    def top(px):
        t = shoulder
        for cx_, r in zip(cxs, radii):
            d = px - cx_
            if abs(d) < r:
                t = min(t, cy - (r * r - d * d) ** 0.5)
        return t

    pts = [(px, top(px)) for px in np.linspace(x, x + w, 900)]
    verts = [(x, y + h)] + pts + [(x + w, y + h), (x, y + h)]
    codes = [Path.MOVETO] + [Path.LINETO] * (len(pts) + 1) + [Path.CLOSEPOLY]
    ax.add_patch(PathPatch(Path(verts, codes), facecolor=WHITE, edgecolor=INK,
                           linewidth=1.0, zorder=2, joinstyle="round"))
    return top


# ==========================================================================================
# fig_t3a -- the silent zero.  827 E4b: real control flow, PANEL test box with the condition
# in monospace bold, failure exit in WARNC on WARN_BG.
# ==========================================================================================
def fig_t3a():
    W, H = 5.60, 5.70
    fig, ax = canvas(W, H)

    mx, mw = 0.30, 2.75          # main spine
    rx, rw = 3.45, 1.85          # right column

    # 1. clone
    box(ax, mx, 0.42, mw, 0.60)
    txt(ax, mx + mw / 2, 0.72, "bmv2 clone 1/256", size=10, color=INK, mono=True)
    arrow(ax, mx + mw / 2, 1.02, mx + mw / 2, 1.30, color=INK, lw=1.0)

    # 2. the header
    box(ax, mx, 1.30, mw, 0.72)
    txt(ax, mx + mw / 2, 1.55, "packet_in header", size=10, color=INK, mono=True)
    txt(ax, mx + mw / 2, 1.79, "fields 1..5 by position", size=8.5, color=MUTED)
    arrow(ax, mx + mw / 2, 2.02, mx + mw / 2, 2.30, color=INK, lw=1.0)

    # 3. the read (ours -> ACCENT_BG per E4b)
    box(ax, mx, 2.30, mw, 0.72, fill=ACCENT_BG)
    txt(ax, mx + mw / 2, 2.55, "emitter reads id 5", size=10, color=INK, weight="bold")
    txt(ax, mx + mw / 2, 2.79, "= sampling_rate", size=8.5, color=BODY, mono=True)
    arrow(ax, mx + mw / 2, 3.02, mx + mw / 2, 3.34, color=INK, lw=1.0)

    # 4. the test
    box(ax, mx, 3.34, mw, 0.64, fill=PANEL, lw=1.25)
    txt(ax, mx + mw / 2, 3.66, "== 0 ?", size=12, color=INK, weight="bold", mono=True)

    # yes -> the failure exit
    arrow(ax, mx + mw / 2, 3.98, mx + mw / 2, 4.32, color=WARNC, lw=1.1)
    txt(ax, mx + mw / 2 - 0.09, 4.15, "yes", size=7.5, color=MUTED, ha="right")
    box(ax, mx, 4.32, mw, 0.70, fill=WARN_BG, edge=WARNC, lw=1.1)
    txt(ax, mx + mw / 2, 4.67, "sample dropped · no log",
        size=10.5, color=WARNC, weight="bold")

    # no -> the normal exit
    arrow(ax, mx + mw, 3.66, rx, 3.66, color=INK, lw=1.0)
    txt(ax, (mx + mw + rx) / 2, 3.53, "no", size=7.5, color=MUTED)
    box(ax, rx, 3.34, rw, 0.64, edge=MUTED, lw=1.0)
    txt(ax, rx + rw / 2, 3.66, "sFlow → kernel", size=9.5, color=MUTED)

    # the branch that only a foreign program takes
    box(ax, rx, 2.30, rw, 0.72, fill=PANEL, edge=RULE, lw=1.0)
    txt(ax, rx + rw / 2, 2.55, "foreign .p4", size=9.5, color=BODY, mono=True)
    txt(ax, rx + rw / 2, 2.79, "fields renumbered", size=8.5, color=BODY)
    arrow(ax, rx, 2.66, mx + mw, 2.66, color=BODY, lw=1.0, ls=(0, (2.4, 1.8)))

    chip(ax, 3.45, 5.10, 1.30, 0.30, "READ-CODE")
    save(fig, "fig_t3a_silent_zero")


# ==========================================================================================
# fig_t3b -- election_id collision.  Three lifelines; the one measured fact on these pages.
# ==========================================================================================
def fig_t3b():
    W, H = 5.60, 5.70
    fig, ax = canvas(W, H)

    LIFE = [("proxy client", 0.25, 1.60), ("bmv2", 2.30, 1.20), ("mycontroller", 3.95, 1.60)]
    xs = [x + w / 2 for _, x, w in LIFE]
    hy, hh = 0.40, 0.66

    for i, (name, x, w) in enumerate(LIFE):
        box(ax, x, hy, w, hh)
        if name == "bmv2":
            txt(ax, xs[i], hy + hh / 2, name, size=10, color=INK, weight="bold", mono=True)
        else:
            txt(ax, xs[i], hy + 0.24, name, size=9.5, color=INK, weight="bold")
            txt(ax, xs[i], hy + 0.47, "election (0,1)", size=7.5, color=MUTED, mono=True)
        ax.plot([xs[i], xs[i]], [hy + hh, 5.05], color=RULE, lw=1.0,
                ls=(0, (2.2, 2.2)), zorder=1)

    def msg(y, a, b, label, note=None, ls="-", lcolor=INK, ncolor=MUTED, lw=1.0):
        arrow(ax, xs[a], y, xs[b], y, color=lcolor, lw=lw, ls=ls)
        mid = (xs[a] + xs[b]) / 2
        txt(ax, mid, y - 0.14, label, size=7.5, color=lcolor, weight="bold", mono=True)
        if note:
            txt(ax, mid, y + 0.16, note, size=7.5, color=ncolor)

    msg(1.62, 0, 1, "StreamChannel", note="primary")
    msg(2.42, 2, 1, "StreamChannel", note="killed: duplicate", ls=(0, (2.6, 1.8)))
    msg(3.22, 2, 1, "SetForwardingPipelineConfig", note="accepted")

    # what happens inside bmv2
    box(ax, xs[1] - 0.80, 3.58, 1.60, 0.46, fill=WARN_BG, edge=WARNC, lw=1.1, z=4)
    txt(ax, xs[1], 3.81, "tables wiped", size=10, color=WARNC, weight="bold", z=5)

    arrow(ax, xs[1], 4.52, xs[2], 4.52, color=WARNC, lw=1.1)
    txt(ax, (xs[1] + xs[2]) / 2, 4.38, "OK", size=11, color=WARNC, weight="bold", mono=True)

    chip(ax, 0.25, 5.16, 1.60, 0.30, "MEASURED 08-13",
         fill=ACCENT_BG, edge=ACCENT, color=ACCENT, size=8.5)
    save(fig, "fig_t3b_election_wipe")


# ==========================================================================================
# fig_t4 -- three phases, and the 2x2 of the runs that have actually happened.
# The rise of each riser IS the number of name tiles under the plateau it reaches.
# ==========================================================================================
def fig_t4():
    W, H = 12.44, 5.60
    fig, ax = canvas(W, H)

    # ---- left 2/3: the staircase --------------------------------------------------------
    PX0, PX1 = 1.55, 8.05
    PY0, PY1 = 4.55, 0.85           # y of data 0 and of data 14
    XMAX, YMAX = 790.0, 14.0
    X = lambda v: PX0 + v / XMAX * (PX1 - PX0)
    Y = lambda v: PY0 - v / YMAX * (PY0 - PY1)

    ax.plot([PX0, PX1], [PY0, PY0], color=RULE, lw=1.0, zorder=1)
    ax.plot([PX0, PX0], [PY0, PY1], color=RULE, lw=1.0, zorder=1)

    for v in (140, 470, 675):
        ax.plot([X(v), X(v)], [PY0, PY0 + 0.06], color=RULE, lw=1.0, zorder=1)
        txt(ax, X(v), PY0 + 0.20, str(v), size=8.5, color=MUTED)
    txt(ax, (PX0 + PX1) / 2, PY0 + 0.48, "cumulative lines (est.)", size=9, color=MUTED)
    for v in (1, 10, 13):
        ax.plot([PX0 - 0.06, PX0], [Y(v), Y(v)], color=RULE, lw=1.0, zorder=1)
        txt(ax, PX0 - 0.13, Y(v), str(v), size=8.5, color=MUTED, ha="right")
    txt(ax, 0.78, (PY0 + PY1) / 2, "exercises runnable", size=9, color=MUTED, rot=90)

    steps = [(0, 0), (140, 0), (140, 1), (470, 1), (470, 10), (675, 10), (675, 13), (790, 13)]
    ax.plot([X(a) for a, _ in steps], [Y(b) for _, b in steps],
            color=INK, lw=1.7, zorder=4, solid_joinstyle="miter")

    # GATE: *after phase two* -- i.e. at cumulative 470 lines, where the second riser lands
    # and 10 exercises become runnable. (Not 675: that is after phase three.)
    ax.plot([X(470), X(470)], [PY1 - 0.02, PY0], color=ACCENT, lw=1.2,
            ls=(0, (3.0, 2.2)), zorder=3)
    txt(ax, X(470), PY1 - 0.16, "GATE", size=9.5, color=ACCENT, weight="bold")

    PHASES = [(1, 140, 470, 0, 1, ["basic"]),
              (2, 470, 675, 1, 10, ["qos", "ecn", "mri", "firewall", "basic_tunnel",
                                    "source_routing", "calc", "link_monitor", "load_balance"]),
              (3, 675, 790, 10, 13, ["multicast", "p4runtime", "flowcache"])]
    for ph, x0, x1, y0, y1, names in PHASES:
        # phase number, sitting on the plateau it belongs to
        txt(ax, X(x0) + 0.12, Y(y1) - 0.15, str(ph), size=9.5, color=ACCENT,
            weight="bold", ha="left")
        tw = min(X(x1) - X(x0) - 0.12, 1.62)
        slot = (Y(y0) - Y(y1)) / len(names)
        for i, nm in enumerate(names):
            ty = Y(y1) + i * slot
            box(ax, X(x0) + 0.06, ty + 0.028, tw, slot - 0.056,
                fill=PANEL, edge=RULE, lw=0.8, z=2, radius=0.02)
            txt(ax, X(x0) + 0.06 + tw / 2, ty + slot / 2, nm, size=7.2, color=BODY, mono=True)

    # ---- divider ------------------------------------------------------------------------
    ax.plot([8.45, 8.45], [0.55, 5.05], color=RULE, lw=1.0, zorder=1)

    # ---- right 1/3: the four runs that exist --------------------------------------------
    RX = 8.70
    txt(ax, RX, 1.22, "4 runs · 09-08 · tutorials harness",
        size=9, color=MUTED, ha="left")

    rowlab_w = 1.20
    c_w, c_gap = 1.02, 0.12
    c_x = [RX + rowlab_w + 0.10, RX + rowlab_w + 0.10 + c_w + c_gap]
    hdr_y, hdr_h = 1.58, 0.34
    row_y, row_h, row_gap = 2.02, 1.00, 0.10

    # the skeleton column is the "we have seen red" half
    box(ax, c_x[1] - 0.06, hdr_y - 0.06, c_w + 0.12, hdr_h + 0.12 + 2 * row_h + row_gap + 0.10,
        fill=PANEL, edge=RULE, lw=0.9, z=1)

    for i, cname in enumerate(("solution", "skeleton")):
        txt(ax, c_x[i] + c_w / 2, hdr_y + hdr_h / 2, cname, size=9.5, color=MUTED, weight="bold")

    CELLS = [("source_routing", ["5/5", "2/2"]), ("basic", ["5/5", "4/4"])]
    for r, (rname, vals) in enumerate(CELLS):
        y = row_y + r * (row_h + row_gap)
        txt(ax, RX, y + row_h / 2, rname, size=9, color=INK, ha="left", mono=True)
        for i, v in enumerate(vals):
            box(ax, c_x[i], y, c_w, row_h, fill=WHITE, edge=RULE, lw=0.9, z=2)
            txt(ax, c_x[i] + c_w / 2, y + row_h / 2 + 0.03, v,
                size=24, color=INK, weight="bold", mono=True)

    txt(ax, c_x[1] + c_w / 2, row_y + 2 * row_h + row_gap + 0.26, "expected fail",
        size=8.5, color=MUTED)

    save(fig, "fig_t4_phases")


if __name__ == "__main__":
    fig_t2()
    fig_t3a()
    fig_t3b()
    fig_t4()
