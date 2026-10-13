#!/usr/bin/env python3
"""
make_heartbeat_figs.py -- the two heartbeat figures of the 2026-09-30 report.

    fig_h1_one_cut_cycle      one cut and one restore on a foreign P4 fabric, on the kernel graph
    fig_h2_detect_vs_phase    detection time of every live cut against where in the 5 s beat it landed

Data: live-p1/runs/2026-09-26T152605Z_08_heartbeat/30_cycles.tsv (H1, six cycles) and
64_cycle.tsv (H3, one cycle) in the NDTwin-Kernel checkout.  Every number drawn is read from
those two files at run time; nothing below is a hand-typed measurement.  The only literals are
the proxy's design constants (5 s beacon, 15 s timeout, 5 s watchdog), which the run itself
printed (raw 01_binaries.txt does not carry them; the run log does -- see the .md).

The raw is not tracked on the kernel's trunk (git ls-files: 0 hits); the whole run directory is
in audit-raw 797c34ab (first mirrored in 543a3aa2, an ancestor), blob-identical to the working tree.

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/heartbeat"
    "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_heartbeat_figs.py
"""
import csv
import os
import sys

import matplotlib

assert matplotlib.__version__.startswith("3.11"), matplotlib.__version__
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

REPO = os.environ.get("NDTWIN_REPO", "/home/adam/Desktop/NDTwin-Kernel")
RUN = os.path.join(REPO, "doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/"
                         "2026-09-26T152605Z_08_heartbeat")
H1_TSV = os.path.join(RUN, "30_cycles.tsv")
H3_TSV = os.path.join(RUN, "64_cycle.tsv")

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
WARNC, WARN_BG, WHITE = "#9C3B2E", "#FBF2F0", "#FFFFFF"
GREEN = "#2F7D4F"

# design constants of the proxy (topology_manager.py:369,415 per TICKET-P4-heartbeat.md:9);
# the run printed them: "beacon interval 5 s, timeout 15 s, watchdog every 5 s"
BEACON_S, TIMEOUT_S, WATCHDOG_S = 5.0, 15.0, 5.0
ACCEPTED_BOUND_S = 20.0


def die(msg):
    raise SystemExit(f"make_heartbeat_figs: {msg}")


def read_h1():
    with open(H1_TSV, newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    if len(rows) != 6:
        die(f"{H1_TSV}: expected 6 cycles, got {len(rows)}")
    for r in rows:
        if r["strict_20s"] != "yes":
            die(f"cycle {r['cycle']} strict_20s={r['strict_20s']}")
    return rows


def read_h3():
    # 64_cycle.tsv is two header/value pairs: line 1 header (cut), line 2 values,
    # line 3 header (restore), line 4 values.
    with open(H3_TSV) as f:
        lines = [ln.rstrip("\n").split("\t") for ln in f if ln.strip()]
    if len(lines) != 4:
        die(f"{H3_TSV}: expected 4 lines, got {len(lines)}")
    cut = dict(zip(lines[0], lines[1]))
    rest = dict(zip(lines[2], lines[3]))
    return cut, rest


def fl(r, k):
    try:
        return float(r[k])
    except (KeyError, ValueError):
        die(f"field {k!r} missing or not a number in {r}")


def save(fig, name):
    os.makedirs(HIRES, exist_ok=True)
    for ext in ("pdf", "png", "svg"):
        kw = {"dpi": 300} if ext == "png" else {}
        fig.savefig(os.path.join(OUTDIR, f"{name}.{ext}"), facecolor=WHITE, **kw)
    fig.savefig(os.path.join(HIRES, f"{name}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"[out] {name}.{{pdf,png,svg}} + _hires/{name}.png")


# ---------------------------------------------------------------------------
# fig_h1_one_cut_cycle
# ---------------------------------------------------------------------------

def fig_h1(rows):
    # the worst cycle of the run (largest detect_s) -- the conservative pick
    r = max(rows, key=lambda x: fl(x, "detect_s"))
    t_last = max(fl(r, "last_heard_ab_mono"), fl(r, "last_heard_ba_mono"))
    t_cut = fl(r, "cut_a_start_mono")
    t_pprev = fl(r, "pass_prev_start_mono")
    t_pass = fl(r, "pass_start_mono")
    t_down = fl(r, "graph_down_mono")
    detect = fl(r, "detect_s")
    if abs((t_down - t_cut) - detect) > 0.002:
        die(f"detect_s {detect} != graph_down - cut_a_start {t_down - t_cut:.3f}")

    t_r = fl(r, "restore_a_start_mono")
    t_first = max(fl(r, "first_heard_ab_mono"), fl(r, "first_heard_ba_mono"))
    rep = fl(r, "restore_report_s")
    t_pup = fl(r, "pass_up_start_mono")
    t_up = fl(r, "graph_up_mono")
    restore = fl(r, "restore_s")
    if abs((t_up - t_r) - restore) > 0.002:
        die(f"restore_s {restore} != graph_up - restore_a_start {t_up - t_r:.3f}")

    # time zero of each panel: the cut (left) and the restore (right)
    L = dict(last=t_last - t_cut, pprev=t_pprev - t_cut, pass_=t_pass - t_cut,
             down=detect, timeout=t_last + TIMEOUT_S - t_cut)
    R = dict(first=t_first - t_r, report=rep, pass_=t_pup - t_r, up=restore)
    print(f"[h1] cycle {r['cycle']}: phi {fl(r, 'phi_s'):.3f} s, detect {detect:.3f} s, "
          f"restore {restore:.3f} s; left {L}; right {R}")

    xl_max, xr_max = 18.0, 6.0
    fig = plt.figure(figsize=(13.33, 5.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[xl_max + 0.8, xr_max + 0.8], wspace=0.08,
                          left=0.10, right=0.985, top=0.80, bottom=0.17)
    axl = fig.add_subplot(gs[0, 0])
    axr = fig.add_subplot(gs[0, 1])
    lanes = {"heartbeat": 2.0, "watchdog": 1.0, "kernel graph": 0.0}

    def base(ax, xmax, xlabel):
        ax.set_xlim(-0.4, xmax + 0.4)
        ax.set_ylim(-1.15, 2.75)
        for y in lanes.values():
            ax.axhline(y, color=RULE, lw=1.0, zorder=0)
        ax.set_yticks(list(lanes.values()))
        ax.set_yticklabels([])
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(MUTED)
        ax.tick_params(axis="x", colors=MUTED, labelsize=12)
        ax.tick_params(axis="y", length=0)
        ax.set_xlabel(xlabel, fontsize=13, color=MUTED, labelpad=8)

    base(axl, xl_max, "seconds after the cut")
    base(axr, xr_max, "seconds after the restore")
    axl.set_xticks(range(0, 19, 3))
    axr.set_xticks(range(0, 7, 2))
    for name, y in lanes.items():
        axl.text(-0.9, y, name, ha="right", va="center", fontsize=14, color=INK)

    # --- left: heartbeat frames.  the last frame heard, then three sends nobody hears.
    axl.plot([L["last"]], [2.0], "o", ms=11, color=GREEN, zorder=4)
    for k in (1, 2, 3):
        x = L["last"] + k * BEACON_S
        axl.plot([x], [2.0], "o", ms=11, mfc=WHITE, mec=WARNC, mew=2.0, zorder=4)
    # the cut itself
    axl.axvline(0, color=WARNC, lw=2.0, zorder=1)
    axl.text(0.15, 2.62, "cut", ha="left", va="center", fontsize=14, color=WARNC,
             fontweight="bold")
    # the 15 s timeout, counted from the last frame heard
    axl.annotate("", xy=(L["timeout"], 2.3), xytext=(L["last"], 2.3),
                 arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.3))
    axl.text((L["last"] + L["timeout"]) / 2, 2.36, f"{TIMEOUT_S:.0f} s timeout", ha="center",
             va="bottom", fontsize=13, color=MUTED)
    # watchdog passes (the two the run recorded)
    for x in (L["pprev"], L["pass_"]):
        axl.plot([x, x], [0.8, 1.2], color=ACCENT, lw=3.0, solid_capstyle="butt", zorder=4)
    # kernel graph: up until the pass reports it, then down
    axl.plot([-0.4, L["down"]], [0, 0], color=GREEN, lw=6, solid_capstyle="butt", zorder=3)
    axl.plot([L["down"], xl_max + 0.4], [0, 0], color=WARNC, lw=6, solid_capstyle="butt",
             zorder=3)
    axl.text(L["down"] + 0.1, 0.12, "down", ha="left", va="bottom", fontsize=13, color=WARNC)
    # the headline bracket: cut -> down
    axl.annotate("", xy=(L["down"], -0.42), xytext=(0, -0.42),
                 arrowprops=dict(arrowstyle="<->", color=INK, lw=1.6))
    axl.text(L["down"] / 2, -0.55, f"{detect:.1f} s", ha="center", va="top", fontsize=17,
             color=INK, fontweight="bold")

    # --- right: restore
    axr.axvline(0, color=GREEN, lw=2.0, zorder=1)
    axr.text(0.1, 2.62, "restore", ha="left", va="center", fontsize=14, color=GREEN,
             fontweight="bold")
    axr.plot([R["first"]], [2.0], "o", ms=11, color=GREEN, zorder=4)
    axr.plot([R["pass_"], R["pass_"]], [0.8, 1.2], color=ACCENT, lw=3.0,
             solid_capstyle="butt", zorder=4)
    axr.plot([-0.4, R["up"]], [0, 0], color=WARNC, lw=6, solid_capstyle="butt", zorder=3)
    axr.plot([R["up"], xr_max + 0.4], [0, 0], color=GREEN, lw=6, solid_capstyle="butt",
             zorder=3)
    axr.text(R["up"] + 0.08, 0.12, "up", ha="left", va="bottom", fontsize=13, color=GREEN)
    axr.annotate("", xy=(R["up"], -0.42), xytext=(0, -0.42),
                 arrowprops=dict(arrowstyle="<->", color=INK, lw=1.6))
    axr.text(R["up"] / 2, -0.55, f"{restore:.1f} s", ha="center", va="top", fontsize=17,
             color=INK, fontweight="bold")

    fig.text(0.10, 0.93, "One cut, one restore — on the kernel graph", fontsize=22,
             fontweight="bold", color=INK, ha="left", va="center")
    # legend for the frame marks, three items, no sentences
    lx, ly = 0.47, 0.855
    fig.text(lx, ly, "●", color=GREEN, fontsize=15, ha="left", va="center")
    fig.text(lx + 0.018, ly, "frame heard", color=MUTED, fontsize=12.5, ha="left", va="center")
    fig.text(lx + 0.13, ly, "○", color=WARNC, fontsize=15, ha="left", va="center",
             fontweight="bold")
    # the lost-frame positions are inferred from the 5 s period, not measured frame by frame
    # (rule 3: mark inferred marks as such on the canvas)
    fig.text(lx + 0.148, ly, "frame lost (inferred)", color=MUTED, fontsize=12.5, ha="left",
             va="center")
    fig.text(lx + 0.315, ly, "|", color=ACCENT, fontsize=17, ha="left", va="center",
             fontweight="bold")
    fig.text(lx + 0.328, ly, "watchdog pass", color=MUTED, fontsize=12.5, ha="left",
             va="center")
    save(fig, "fig_h1_one_cut_cycle")
    return r


# ---------------------------------------------------------------------------
# fig_h2_detect_vs_phase
# ---------------------------------------------------------------------------

def fig_h2(rows, h3cut):
    pts = [(fl(r, "phi_s"), fl(r, "detect_s")) for r in rows]
    pts.append((fl(h3cut, "phi_s"), fl(h3cut, "detect_s")))
    for phi, d in pts:
        lo, hi = TIMEOUT_S - phi, TIMEOUT_S - phi + WATCHDOG_S
        if not (lo <= d <= hi + 0.5):
            die(f"point phi={phi} detect={d} outside the design band [{lo:.3f}, {hi:.3f}]+0.5")
        if d > ACCEPTED_BOUND_S:
            die(f"point {d} over {ACCEPTED_BOUND_S}")
    print(f"[h2] {len(pts)} live cuts: " + ", ".join(f"({p:.3f}, {d:.3f})" for p, d in pts))

    fig, ax = plt.subplots(figsize=(13.33, 6.0))
    fig.subplots_adjust(left=0.09, right=0.97, top=0.84, bottom=0.15)
    xs = [0.0, BEACON_S]
    band = Polygon([(0, TIMEOUT_S), (BEACON_S, TIMEOUT_S - BEACON_S),
                    (BEACON_S, TIMEOUT_S - BEACON_S + WATCHDOG_S), (0, TIMEOUT_S + WATCHDOG_S)],
                   closed=True, facecolor=ACCENT_BG, edgecolor="none", zorder=0)
    ax.add_patch(band)
    ax.plot(xs, [TIMEOUT_S - x for x in xs], color=ACCENT, lw=1.6, zorder=1)
    ax.plot(xs, [TIMEOUT_S - x + WATCHDOG_S for x in xs], color=ACCENT, lw=1.6, ls=(0, (5, 4)),
            zorder=1)
    ax.axhline(ACCEPTED_BOUND_S, color=WARNC, lw=1.4, ls=(0, (2, 3)), zorder=1)
    ax.text(BEACON_S, ACCEPTED_BOUND_S + 0.25, f"{ACCEPTED_BOUND_S:.0f} s · design bound (derived)",
            color=WARNC, fontsize=13, ha="right", va="bottom")
    # rule 3: the band and the 20 s line are arithmetic on the design constants, not measured
    ax.text(3.05, TIMEOUT_S - 3.05 + WATCHDOG_S / 2, "design bound (derived)", color=ACCENT,
            fontsize=12, ha="center", va="center", style="italic", zorder=2)
    h1, h3 = pts[:-1], pts[-1:]
    ax.plot([p for p, _ in h1], [d for _, d in h1], "o", ms=12, color=INK, mec=WHITE,
            mew=2.0, zorder=3, clip_on=False, label=f"H1 · owned table · {len(h1)} cuts")
    ax.plot([p for p, _ in h3], [d for _, d in h3], "s", ms=11, color=ACCENT, mec=WHITE,
            mew=2.0, zorder=4, clip_on=False, label=f"H3 · unbound · {len(h3)} cut")
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 1.13), ncol=2, frameon=False,
              fontsize=12.5, labelcolor=MUTED, handletextpad=0.4, columnspacing=1.6)
    # the four cuts at phi ~0.02 s sit on top of each other: a zoomed inset shows all four
    near = [(p, d) for p, d in pts if p < 0.1]
    if len(near) != 4:
        die(f"expected 4 cuts at phi < 0.1 s, got {len(near)}")
    ins = ax.inset_axes([0.10, 0.06, 0.26, 0.30])
    ins.set_facecolor(WHITE)
    ins.plot([p for p, _ in h1 if p < 0.1], [d for p, d in h1 if p < 0.1], "o", ms=10,
             color=INK, mec=WHITE, mew=1.5)
    ins.plot([p for p, _ in h3], [d for _, d in h3], "s", ms=9, color=ACCENT, mec=WHITE, mew=1.5)
    for p_, d_ in near:
        ins.annotate(f"{d_:.2f}", xy=(p_, d_), xytext=(8, 0), textcoords="offset points",
                     fontsize=11, color=INK, va="center")
    ins.set_xlim(0.010, 0.036)
    ins.set_ylim(16.40, 16.95)
    ins.set_xticks([0.015, 0.025, 0.035])
    ins.set_yticks([16.5, 16.7, 16.9])
    ins.tick_params(labelsize=10.5, colors=MUTED)
    for sp in ins.spines.values():
        sp.set_color(MUTED)
    ax.indicate_inset_zoom(ins, edgecolor=MUTED, lw=1.0)
    # value labels on the extremes only
    worst = max(pts, key=lambda t: t[1])
    best = min(pts, key=lambda t: t[1])
    ax.annotate(f"{best[1]:.1f} s", xy=best, xytext=(-14, -6), textcoords="offset points",
                fontsize=14, color=INK, fontweight="bold", ha="right", va="top")
    # line labels, placed on the lines' right ends
    ax.text(BEACON_S - 0.05, TIMEOUT_S - BEACON_S + WATCHDOG_S - 0.35, "+ one watchdog wait",
            color=ACCENT, fontsize=12.5, ha="right", va="top")
    ax.text(BEACON_S - 0.05, TIMEOUT_S - BEACON_S - 0.35, "15 s after the last frame",
            color=ACCENT, fontsize=12.5, ha="right", va="top")
    ax.set_xlim(-0.15, BEACON_S)
    ax.set_ylim(8, 21.5)
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_yticks([10, 12, 14, 16, 18, 20])
    ax.grid(axis="y", color=RULE, lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=12.5)
    ax.set_xlabel("when the cut landed: seconds after the last heartbeat frame", fontsize=13.5,
                  color=MUTED, labelpad=8)
    ax.set_ylabel("cut → down on the kernel graph (s)", fontsize=13.5, color=MUTED, labelpad=8)
    fig.text(0.09, 0.93, f"Detection time: {len(pts)} live cuts", fontsize=22,
             fontweight="bold", color=INK, ha="left", va="center")
    save(fig, "fig_h2_detect_vs_phase")
    return pts


def main():
    rows = read_h1()
    h3cut, _h3rest = read_h3()
    r = fig_h1(rows)
    pts = fig_h2(rows, h3cut)
    d = sorted(x for _, x in pts)
    print(f"[summary] H1 detect {min(fl(x, 'detect_s') for x in rows):.3f}-"
          f"{max(fl(x, 'detect_s') for x in rows):.3f} s; restore "
          f"{min(fl(x, 'restore_s') for x in rows):.3f}-{max(fl(x, 'restore_s') for x in rows):.3f}"
          f" s; all 7 cuts {d[0]:.3f}-{d[-1]:.3f} s; h1 figure cycle {r['cycle']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
