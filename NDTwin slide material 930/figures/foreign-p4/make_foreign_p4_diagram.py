#!/usr/bin/env python3
"""
make_foreign_p4_diagram.py -- fig_a1_foreign_p4_path: how one P4 tutorial exercise (a program
NDTwin did not write) is run on the NDTwin fabric, from the exercise folder to the report.

An architecture diagram, not a measurement.  Every box names a step or a component that the
live raw shows by name; the .md cites, for each box, the arm-report section or raw file where
it appears (T06 = live-p1/runs/2026-09-27T074635Z_06_thirteen and its 26 arm reports; 07 =
live-p1/runs/2026-09-26T202055Z_07_roles_basic).  No ran numbers are on the canvas (second
round, 2026-09-27 UTC: the page mixes ran boxes and read arrows, so its numbers went to the .md);
the range of pre-flight checks is still counted from those arm reports at run time and printed.

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/foreign-p4"
    "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_foreign_p4_diagram.py
"""
import csv
import os
import sys

import matplotlib

assert matplotlib.__version__.startswith("3.11"), matplotlib.__version__
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402

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

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")
STEM = "fig_a1_foreign_p4_path"

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
WHITE, GREEN = "#FFFFFF", "#2F7D4F"
W, H = 13.33, 6.9


def die(msg):
    raise SystemExit(f"make_foreign_p4_diagram: {msg}")


def count_pass(lines):
    """PASS lines of one pre-flight block ('pre-flight: <pkg>' ... 'PASS|FAIL -- ...')."""
    n, inside = 0, False
    for ln in lines:
        if ln.startswith("pre-flight: "):
            inside, n = True, 0
            continue
        if inside and ln.startswith("  PASS"):
            n += 1
        if inside and (ln.startswith("PASS --") or ln.startswith("FAIL --")):
            return n
    return None


def preflight_range():
    counts = {}
    with open(T06, newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if not r["verdict"].startswith("PASS"):
                continue          # the two designed refusals stop before or inside pre-flight
            with open(r["report"], encoding="utf-8", errors="replace") as g:
                n = count_pass(g.read().splitlines())
            if n is None:
                die(f"no pre-flight block in {r['report']}")
            counts[f"{r['exercise']}/{r['which']}"] = n
    with open(PRE07) as g:
        n07 = count_pass(g.read().splitlines())
    if n07 is None:                     # added 2026-09-27 UTC (red-check round, coordinator-approved)
        die(f"no pre-flight block in the 07 file {PRE07}")
    counts["07 basic_roles"] = n07
    lo, hi = min(counts.values()), max(counts.values())
    print(f"[preflight] {len(counts)} packages: PASS checks {lo}-{hi}: {counts}")
    return lo, hi


def box(ax, x, y, w, h, fill=WHITE, edge=INK, lw=1.2, ls="solid", r=0.06, z=2):
    ax.add_patch(FancyBboxPatch((x + r, y + r), w - 2 * r, h - 2 * r,
                                boxstyle=f"round,pad={r},rounding_size={r}", facecolor=fill,
                                edgecolor=edge, linewidth=lw, linestyle=ls, zorder=z))


def txt(ax, x, y, s, size=13, color=INK, weight="normal", ha="center", va="center",
        mono=False, z=6):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, zorder=z,
            family="monospace" if mono else None, linespacing=1.25)


def arrow(ax, x0, y0, x1, y1, color=INK, lw=1.4, both=False, ls="solid", z=3):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="<|-|>" if both else "-|>",
                                 mutation_scale=13, color=color, lw=lw, linestyle=ls,
                                 shrinkA=0, shrinkB=0, zorder=z))


def main():
    lo, hi = preflight_range()
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")

    txt(ax, 0.45, 0.48, "How a foreign P4 program runs on NDTwin", size=22, weight="bold",
        ha="left")

    # ---- row 1: the steps, left to right
    steps = [
        ("exercise", "its own .p4"),
        ("convert.py", "package"),
        ("pre-flight", "package checks"),     # the ran count (lo-hi) stays in the .md
        ("ndt claim", "the lab"),
        ("ndt up", "p4 --app"),
        ("packet test", "its own checks"),
        ("ndt down", "release · report"),
    ]
    x0, y0, bw, bh, gap = 0.45, 1.05, 1.52, 0.92, 0.24
    centers = []
    for i, (a, b) in enumerate(steps):
        x = x0 + i * (bw + gap)
        hot = a == "ndt up"
        box(ax, x, y0, bw, bh, fill=ACCENT_BG if hot else WHITE, edge=ACCENT if hot else INK,
            lw=2.4 if hot else 1.2)
        txt(ax, x + bw / 2, y0 + 0.33, a, size=14, weight="bold",
            color=ACCENT if hot else INK)
        txt(ax, x + bw / 2, y0 + 0.64, b, size=11.5, color=MUTED)
        centers.append(x + bw / 2)
        if i:
            arrow(ax, x - gap + 0.02, y0 + bh / 2, x - 0.02, y0 + bh / 2)
    up_x = x0 + 4 * (bw + gap)
    # rule 3 (coordinator, round 3): which parts are run-derived and which are read from code
    txt(ax, x0, y0 - 0.17, "RAN IT · every step appears in T06's arm reports", size=11,
        weight="bold", color=FAINT, ha="left")

    # ---- the running stack under "ndt up"
    sy = 2.55
    # a bracket from ndt up down to the stack
    by = sy - 0.28
    ax.plot([up_x + bw / 2, up_x + bw / 2], [y0 + bh, by], color=ACCENT, lw=2.0,
            ls=(0, (4, 3)), zorder=1)
    ax.plot([0.45, 12.90], [by, by], color=ACCENT, lw=2.0, ls=(0, (4, 3)), zorder=1)
    txt(ax, 12.90, by + 0.17, "RAN IT: the boxes  ·  READ THE CODE: the arrows", size=11,
        weight="bold", color=FAINT, ha="right")

    # NDTwin: kernel + proxy
    box(ax, 0.45, sy, 7.10, 2.35, fill=PANEL, edge=RULE, lw=1.0, r=0.08, z=1)
    txt(ax, 0.62, sy + 0.24, "NDTWIN", size=11.5, color=FAINT, weight="bold", ha="left")
    box(ax, 0.70, sy + 0.50, 2.35, 1.55)
    txt(ax, 1.875, sy + 0.95, "kernel", size=14, weight="bold")
    txt(ax, 1.875, sy + 1.45, "graph\nlink usage", size=12, color=MUTED)
    box(ax, 3.35, sy + 0.50, 3.95, 1.55)
    txt(ax, 5.325, sy + 0.80, "P4 proxy", size=14, weight="bold")
    # what the proxy writes, as box names only (judge F-21: no bullet list)
    items = ["pipeline", "table entries", "multicast groups", "roles.ipv4_route"]
    for k, s in enumerate(items):
        cx = 3.58 + (k % 2) * 1.80
        cy = sy + 1.07 + (k // 2) * 0.47
        box(ax, cx, cy, 1.68, 0.38, fill=WHITE, edge=MUTED, lw=0.9, r=0.04, z=3)
        txt(ax, cx + 0.84, cy + 0.20, s, size=11.5, color=BODY, va="center_baseline")
    arrow(ax, 3.33, sy + 1.28, 3.07, sy + 1.28, color=MUTED, both=True)

    # heartbeat helper
    box(ax, 8.35, sy + 0.50, 2.35, 1.10, fill=WHITE, edge=GREEN, lw=1.8)
    txt(ax, 9.525, sy + 0.86, "heartbeat", size=14, weight="bold", color=GREEN)
    txt(ax, 9.525, sy + 1.24, "root helper · 0x88B5", size=11.5, color=MUTED)
    arrow(ax, 8.33, sy + 1.05, 7.32, sy + 1.05, color=GREEN, lw=1.6)
    txt(ax, 7.83, sy + 0.80, "link\nup / down", size=10.5, color=GREEN, ha="center")

    # exercise's own controller (external mode)
    box(ax, 10.95, sy + 0.50, 1.95, 1.10, fill=WHITE, edge=MUTED, lw=1.3, ls=(0, (4, 3)))
    txt(ax, 11.925, sy + 0.86, "its controller", size=13, weight="bold", color=BODY)
    txt(ax, 11.925, sy + 1.24, "p4runtime · flowcache", size=11.5, color=MUTED)

    # the fabric
    fy = 5.45
    box(ax, 0.45, fy, 12.45, 1.05, fill=WHITE, edge=INK, lw=1.4, r=0.10)
    txt(ax, 6.675, fy + 0.36, "Mininet fabric  ·  bmv2", size=15, weight="bold")
    txt(ax, 6.675, fy + 0.74, "each switch runs the exercise's own program", size=12,
        color=MUTED)

    # arrows into the fabric
    arrow(ax, 5.325, sy + 2.07, 5.325, fy - 0.02, color=ACCENT, lw=1.8)
    txt(ax, 5.425, (sy + 2.07 + fy) / 2, "P4Runtime", size=11.5, color=ACCENT, ha="left")
    arrow(ax, 1.875, fy - 0.02, 1.875, sy + 2.07, color=MUTED, lw=1.4)
    txt(ax, 1.975, (sy + 2.07 + fy) / 2, "samples", size=11.5, color=MUTED, ha="left")
    arrow(ax, 9.525, sy + 1.62, 9.525, fy - 0.02, color=GREEN, both=True, lw=1.6)
    txt(ax, 9.625, (sy + 1.62 + fy) / 2, "switch-to-switch\nveths", size=11.5, color=GREEN,
        ha="left")
    arrow(ax, 11.925, sy + 1.62, 11.925, fy - 0.02, color=MUTED, lw=1.4, ls=(0, (4, 3)))
    txt(ax, 12.025, (sy + 1.62 + fy) / 2, "P4Runtime", size=11.5, color=MUTED, ha="left")

    os.makedirs(HIRES, exist_ok=True)
    for ext in ("pdf", "png", "svg"):
        kw = {"dpi": 300} if ext == "png" else {}
        fig.savefig(os.path.join(OUTDIR, f"{STEM}.{ext}"), facecolor=WHITE, **kw)
    fig.savefig(os.path.join(HIRES, f"{STEM}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"[out] {STEM}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
