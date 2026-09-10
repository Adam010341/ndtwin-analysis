#!/usr/bin/env python3
"""
make_overnight_figs.py -- 09-04 夜巡「第一批」現況圖.

fig1/fig2/fig3/fig5/fig6 仍是 09-04 的現況圖（current behaviour, no after side yet）.
fig4 在 2026-09-05 補上 after 側（09-05 R0，kernel 4c9e0be122e1c5ea）——它是這份腳本裡
唯一有 before/after 兩側的圖；其餘五張的數字與輸出檔一個 byte 都沒動。

[Co-developed with claude code -- Adam]

Regenerate:
    python3 make_overnight_figs.py
(the system /usr/bin/python3 has no matplotlib on this machine; the interpreter that
resolves first on PATH is ~/miniconda3/bin/python3, matplotlib 3.10.8 -- confirmed
2026-09-04. ~/miniconda3/bin/python has the same package if PATH differs.)
writes fig1..fig6 as .pdf + .png (300 dpi) + .svg into this directory, byte-for-byte
from the numbers embedded below (each number's raw source is cited in the companion
<figN>.md next to it -- this script is the vector source, the .md is the provenance).

matplotlib version is asserted below (this repo's convention per
doc/2026-08-29_bmv2-performance-study-figs/README-generators.md).
"""
import matplotlib
assert matplotlib.__version__.startswith("3.10") or matplotlib.__version__.startswith("3.11"), \
    f"unexpected matplotlib {matplotlib.__version__}; re-verify numbers render as expected"
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import os

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["svg.fonttype"] = "none"

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# ---- palette (dataviz skill, references/palette.md -- validated default) ----
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
YELLOW = "#eda100"
MAGENTA = "#e87ba4"
VIOLET = "#4a3aa7"

INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
SURFACE = "#fcfcfb"

GOOD = "#0ca30c"
CRITICAL = "#d03b3b"
CRITICAL_WASH = "#fbe4e3"
GOOD_WASH = "#e2f4e2"

def style_axes(ax, x_grid=True, y_grid=False):
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(BASELINE)
        ax.spines[spine].set_linewidth(1)
    ax.tick_params(colors=INK_MUTED, labelsize=9.5)
    if x_grid:
        ax.xaxis.grid(True, color=GRID, linewidth=1, zorder=0)
    if y_grid:
        ax.yaxis.grid(True, color=GRID, linewidth=1, zorder=0)
    ax.set_axisbelow(True)

def save(fig, name):
    fig.savefig(os.path.join(OUTDIR, f"{name}.pdf"), bbox_inches="tight", facecolor=SURFACE)
    fig.savefig(os.path.join(OUTDIR, f"{name}.png"), bbox_inches="tight", facecolor=SURFACE, dpi=300)
    fig.savefig(os.path.join(OUTDIR, f"{name}.svg"), bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print(f"wrote {name}.{{pdf,png,svg}}")


# ============================================================================
# fig1 -- declared vs. real link failure: how long the DOWN state survives
# ============================================================================
def fig1():
    # rows: (label, seconds, group)  -- group in {"p4","ovs","real"}
    p4 = [1.576, 10.598, 13.558, 19.624]        # p4-4-14-linkfail.log, trials 1/3/4/5 (trial 2 right-censored, see .md)
    ovs = [21.479, 22.455, 23.414, 24.432, 25.354]  # r2-20-linkfail-probe.log, trials 5..1
    real = 60.0  # r2-21-netem-control.log: held down the entire 60 s window; recovered only after manual `tc qdisc del`

    rows = []
    for i, v in enumerate(sorted(p4)):
        rows.append((f"P4 declared #{i+1}", v, "p4"))
    for i, v in enumerate(sorted(ovs)):
        rows.append((f"OVS declared #{i+1}", v, "ovs"))
    rows.append(("real cut (tc netem)", real, "real"))

    color = {"p4": ORANGE, "ovs": BLUE, "real": AQUA}
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    y = list(range(len(rows)))[::-1]
    for (label, v, g), yi in zip(rows, y):
        if g == "real":
            bar = ax.barh(yi, v, height=0.62, color=color[g], zorder=3)
            ax.plot(v, yi, marker=">", color=color[g], markersize=9, zorder=4)
            ax.text(v + 1.0, yi, "≥ 60 s · manual restore only", va="center", ha="left",
                    fontsize=9.5, color=INK_PRIMARY)
        else:
            ax.barh(yi, v, height=0.62, color=color[g], zorder=3)
            ax.text(v + 1.0, yi, f"{v:.1f} s", va="center", ha="left", fontsize=9.5, color=INK_PRIMARY)

    ax.axvline(30, color=INK_SECONDARY, linewidth=1.4, linestyle=(0, (4, 3)), zorder=2)
    ax.text(28.5, 9.35, "30 s poll period", color=INK_SECONDARY, fontsize=9.5,
            ha="right", va="bottom", zorder=6,
            bbox=dict(facecolor=SURFACE, edgecolor="none", pad=0.5))

    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in rows])
    ax.set_ylim(-0.7, 9.9)
    ax.set_xlim(0, 78)
    ax.set_xlabel("seconds from declaration until the DOWN state was no longer observed")
    ax.set_title("Declared link failure vs. a real cut: how long DOWN survives", fontsize=13,
                 color=INK_PRIMARY, loc="left", pad=12)
    style_axes(ax, x_grid=True, y_grid=False)

    legend_handles = [
        mpatches.Patch(color=BLUE, label="OVS4 — declared (link_failure_detected)"),
        mpatches.Patch(color=ORANGE, label="P4-4 — declared (link_failure_detected)"),
        mpatches.Patch(color=AQUA, label="OVS4 — real cut (tc netem loss 100%)"),
    ]
    ax.legend(handles=legend_handles, loc="upper right", frameon=False, fontsize=9)
    fig.tight_layout()
    save(fig, "fig1_declared_vs_real_link_failure")


# ============================================================================
# fig2 -- shutdown southbound writes: kernel keeps writing after "Exiting"
# ============================================================================
def fig2():
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    t_sigint = 0.0
    t_exiting = 0.595
    t_gone = 11.338
    t_idle_ref = 2.5  # FINDINGS #27 baseline, different round/binary -- see .md

    # background lane
    ax.plot([0, 12.5], [0.5, 0.5], color=BASELINE, linewidth=2, zorder=1, solid_capstyle="butt")
    # critical span: claims stopped, still writing southbound
    ax.axvspan(t_exiting, t_gone, ymin=0.36, ymax=0.64, color=CRITICAL, alpha=0.18, zorder=1)
    ax.plot([t_exiting, t_gone], [0.5, 0.5], color=CRITICAL, linewidth=5, solid_capstyle="round", zorder=2)

    # event markers -- staggered above/below the lane so close-together events don't collide
    ax.plot(t_sigint, 0.5, "o", color=INK_PRIMARY, markersize=7, zorder=5,
            markeredgecolor=SURFACE, markeredgewidth=1.5)
    ax.annotate("SIGINT", xy=(t_sigint, 0.5), xytext=(t_sigint + 0.12, 0.40), ha="left", va="top",
                fontsize=9.7, color=INK_PRIMARY)

    for t, label in [(t_exiting, "“Exiting” printed"), (t_gone, "process exits")]:
        ax.plot(t, 0.5, "o", color=INK_PRIMARY, markersize=7, zorder=5,
                markeredgecolor=SURFACE, markeredgewidth=1.5)
        ha = "left" if t < 6 else "right"
        xo = 0.15 if t < 6 else -0.15
        ax.annotate(label, xy=(t, 0.5), xytext=(t + xo, 0.74), ha=ha, va="bottom",
                    fontsize=9.7, color=INK_PRIMARY)

    # sits below the band, in the empty lane between the band and the x-axis --
    # clear of both the event labels above and the axis tick numbers below
    ax.annotate("still writing to real switches — 10.7 s\n(1500 queued entries, 0 log lines say so)",
                xy=((t_exiting + t_gone) / 2, 0.378), xytext=((t_exiting + t_gone) / 2, 0.30),
                ha="center", va="top", fontsize=9.7, color=INK_PRIMARY, linespacing=1.3)

    ax.axvline(t_idle_ref, color=INK_MUTED, linewidth=1.2, linestyle=(0, (1, 2)), zorder=1, ymin=0.15, ymax=0.85)
    ax.text(t_idle_ref + 0.15, 0.97, "idle SIGINT baseline ≈ 2.5 s (other round)", ha="left", va="top",
            fontsize=8.7, color=INK_MUTED)

    ax.set_xlim(-0.3, 12.6)
    ax.set_ylim(0, 1.05)
    ax.set_yticks([])
    ax.set_xlabel("seconds since SIGINT")
    ax.set_title("Shutdown: southbound writes continue after “Exiting” is printed", fontsize=13,
                 color=INK_PRIMARY, loc="left", pad=12)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["bottom"].set_color(BASELINE)
    ax.tick_params(colors=INK_MUTED, labelsize=9.5)
    fig.tight_layout()
    save(fig, "fig2_shutdown_southbound_writes")


# ============================================================================
# fig3 -- dispatch "succeeded" counts calls, not changes
# ============================================================================
def fig3():
    groups = ["20× install\n(same match)", "15× delete\n(never existed)", "1× delete\n(real entry, control)"]
    succeeded = [20, 15, 1]
    switch_rows_changed = [1, 0, 1]

    x = range(len(groups))
    width = 0.32
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    b1 = ax.bar([i - width / 2 - 0.02 for i in x], succeeded, width=width, color=BLUE, zorder=3,
                label="get_flow_dispatch_status: Δ succeeded")
    b2 = ax.bar([i + width / 2 + 0.02 for i in x], switch_rows_changed, width=width, color=ORANGE, zorder=3,
                label="switch truth (Ryu stats/flow): Δ rows")

    for bars in (b1, b2):
        for rect in bars:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2, h + 0.35, f"{int(h)}", ha="center", va="bottom",
                    fontsize=10, color=INK_PRIMARY)

    ax.set_xticks(list(x))
    ax.set_xticklabels(groups, fontsize=9.5)
    ax.set_ylabel("count")
    ax.set_ylim(0, 23)
    ax.set_title("“succeeded” counts POSTs, not switch-state changes", fontsize=13,
                 color=INK_PRIMARY, loc="left", pad=12)
    style_axes(ax, x_grid=False, y_grid=True)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    fig.tight_layout()
    save(fig, "fig3_dispatch_counters_vs_switch_truth")


# ============================================================================
# fig4 -- install/delete readback, before (09-04) vs. after (09-05 W1 fix)
#         still a table, not a chart: every cell is a status code / outcome
#         string, so there is no magnitude for an axis to represent.
# ============================================================================
FIG4_COLUMNS = ["group_id", "install_group_entry", "groupdesc (switch truth)",
                "delete_group_entry (same id)"]
# relative column widths; the table is placed with an explicit bbox, so these are
# proportions, not absolute fractions. col3/col4 are sized for their (bold) headers,
# which are the widest strings in those columns.
FIG4_COLWIDTHS = [0.205, 0.265, 0.235, 0.265]
# cell tint: 0=neutral, 1=critical wash, 2=good wash
FIG4_TINT_COLOR = {0: "white", 1: CRITICAL_WASH, 2: GOOD_WASH}


def _fig4_block(ax, rows, tint, block_title):
    """One before/after block of fig4: same columns, same widths, so the reader's
    eye compares straight down a column across the two blocks. bbox=[0,0,1,1] makes
    the table fill its axes exactly -- the subplot height_ratios (rows+1 each) then
    give both blocks the same row height with no dead space between them."""
    ax.axis("off")
    tbl = ax.table(cellText=rows, colLabels=FIG4_COLUMNS, cellLoc="center",
                   colWidths=FIG4_COLWIDTHS, bbox=[0, 0, 1, 1])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9.6)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor(GRID)
        if r == 0:
            cell.set_facecolor("#eeede8")
            cell.set_text_props(color=INK_PRIMARY, fontweight="bold", fontsize=9.2)
        else:
            cell.set_facecolor(FIG4_TINT_COLOR[tint[r - 1][c]])
            cell.set_text_props(color=INK_PRIMARY)
    ax.set_title(block_title, fontsize=10.5, color=INK_SECONDARY, loc="left", pad=7)
    return tbl


def fig4():
    # -- before: 2026-09-04, kernel cca5e3e4ebc42358 / helper 6685d3a9.
    #    raw logs/r2-41-b1-group-extra.log (the two reserved ids); outcome strings verbatim.
    before_rows = [
        ["4294967295\n(OFPG_ALL, reserved)", "200 {\"outcome\":\n\"installed\"}",
         "absent", "404 {\"outcome\":\n\"no_such_group\"}"],
        ["4294967293\n(reserved)", "200 {\"outcome\":\n\"installed\"}",
         "absent", "404 {\"outcome\":\n\"no_such_group\"}"],
    ]
    # install says "installed", the switch does not have it, delete of the same id says
    # "no_such_group" -- install and groupdesc contradict each other; delete told the truth.
    before_tint = [
        [0, 1, 1, 2],
        [0, 1, 1, 2],
    ]

    # -- after: 2026-09-05, kernel 4c9e0be122e1c5ea / helper 6685d3a9 / trunk 68c1dde4,
    #    W1 fix f2126cc5. raw logs/r0-30-w1.log; rounds/00-R0-postmerge.md §3-3 is the
    #    verbatim authority for these four rows.
    after_rows = [
        ["4294967295\n(OFPG_ALL, reserved)", "502 {\"outcome\":\"absent\"}\n“the switch did NOT take it”",
         "absent", "404 {\"outcome\":\n\"no_such_group\"}"],
        ["4294967293\n(reserved)", "502 {\"outcome\":\"absent\"}\n“the switch did NOT take it”",
         "absent", "404 {\"outcome\":\n\"no_such_group\"}"],
        ["813\n(control, OVS accepts)", "200 {\"outcome\":\n\"installed\"}",
         "present\n(type SELECT)", "200 {\"outcome\":\n\"deleted\"}"],
        ["899\n(control, never installed)", "— not attempted\n(modify: 404 no_such_group)",
         "absent", "— not attempted"],
    ]
    # all three channels now give the same answer on every row -> no critical wash.
    # 899's delete was not run this round (09-04 ran it) -> neutral, not green.
    after_tint = [
        [0, 2, 2, 2],
        [0, 2, 2, 2],
        [0, 2, 2, 2],
        [0, 2, 2, 0],
    ]

    fig, (ax_b, ax_a) = plt.subplots(
        2, 1, figsize=(10.6, 5.3),
        gridspec_kw={"height_ratios": [len(before_rows) + 1, len(after_rows) + 1],
                     "hspace": 0.30, "left": 0.008, "right": 0.992,
                     "top": 0.862, "bottom": 0.072})
    _fig4_block(ax_b, before_rows, before_tint, "BEFORE — kernel cca5e3e4, 2026-09-04")
    _fig4_block(ax_a, after_rows, after_tint, "AFTER — kernel 4c9e0be1, 2026-09-05")

    fig.suptitle("install vs. delete readback, before and after the W1 fix",
                 fontsize=13, color=INK_PRIMARY, x=0.008, y=0.985, ha="left", va="top")
    fig.text(0.008, 0.008,
             "install now says “installed” only once the switch has taken it",
             fontsize=10.5, color=INK_PRIMARY, ha="left", va="bottom")
    save(fig, "fig4_group_install_delete_readback")


# ============================================================================
# fig5 -- get_path_switch_count ignores live topology (dumbbell, before==after)
# ============================================================================
def fig5():
    # (src,dst,switch_count) from p4-4-pathcount-allon.json; identical in p4-4-pathcount-3off.json
    # and, per pathmetric_test.py's own row-diff assertion, identical again at 32/40 edges down.
    pairs = [
        (1, 2, 3), (2, 1, 3), (3, 4, 3), (4, 3, 3),
        (1, 3, 5), (1, 4, 5), (2, 3, 5), (2, 4, 5),
        (3, 1, 5), (3, 2, 5), (4, 1, 5), (4, 2, 5),
    ]
    pairs.sort(key=lambda p: (p[2], p[0], p[1]))
    labels = [f".{s}→.{d}" for s, d, _ in pairs]
    values = [c for _, _, c in pairs]
    y = list(range(len(pairs)))[::-1]

    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    for yi, v in zip(y, values):
        ax.plot(v, yi, marker="o", markersize=13, markerfacecolor="none",
                markeredgecolor=BLUE, markeredgewidth=2, zorder=2, alpha=0.55)
        ax.plot(v, yi, marker="o", markersize=6, color=BLUE, zorder=3)

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9.5, family="monospace")
    ax.set_xticks([3, 5])
    ax.set_xlim(2, 6.4)
    ax.set_ylim(-1.5, len(pairs) - 0.3)
    ax.set_xlabel("get_path_switch_count — switch_count")
    ax.set_title("Path length unchanged at 32/40 and at 20/40 switch-switch edges down",
                 fontsize=12.5, color=INK_PRIMARY, loc="left", pad=12)
    style_axes(ax, x_grid=True, y_grid=False)

    legend_handles = [
        Line2D([0], [0], marker="o", linestyle="none", markersize=11, markerfacecolor="none",
               markeredgecolor=BLUE, markeredgewidth=2, alpha=0.55, label="before (40/40 edges up)"),
        Line2D([0], [0], marker="o", linestyle="none", markersize=6, color=BLUE,
               label="after (12/40 or 8/40 edges up) — lands on “before”"),
    ]
    ax.legend(handles=legend_handles, loc="lower center", frameon=False, fontsize=8.7)
    fig.tight_layout()
    save(fig, "fig5_path_switch_count_static")


# ============================================================================
# fig6 -- API endpoint latency profile (OVS)
# ============================================================================
def fig6():
    # (endpoint, ms, category)
    data = [
        ("set_switches_power_state (on)", 1485, "power"),
        ("delete_meter_entry", 1029, "meter"),
        ("install_meter_entry", 1024, "meter"),
        ("set_switches_power_state (off)", 571, "power"),
        ("get_path_switch_count (full matrix)", 113, "read"),
        ("delete_group_entry", 34, "group"),
        ("modify_meter_entry", 26, "meter"),
        ("modify_group_entry", 24, "group"),
        ("get_graph_data", 23, "read"),
        ("install_group_entry", 20, "group"),
        ("get_switch_openflow_table_entries", 18, "read"),
        ("get_static_topology_json", 8, "read"),
        ("modify_flow_entry", 4, "flow"),
        ("get_average_link_usage", 3, "read"),
        ("delete_flow_entry", 3, "flow"),
        ("install_flow_entry", 1, "flow"),
    ]
    color = {"read": BLUE, "flow": ORANGE, "group": AQUA, "meter": YELLOW, "power": MAGENTA}
    cat_label = {"read": "read / query", "flow": "flow write", "group": "group write",
                 "meter": "meter write", "power": "power write"}

    fig, ax = plt.subplots(figsize=(7.6, 6.4))
    y = list(range(len(data)))[::-1]
    for (name, ms, cat), yi in zip(data, y):
        ax.barh(yi, ms, height=0.62, color=color[cat], zorder=3)
        label = f"{ms/1000:.2f} s" if ms >= 1000 else f"{ms} ms"
        ax.text(ms * 1.15, yi, label, va="center", ha="left", fontsize=9, color=INK_PRIMARY)

    ax.set_yticks(y)
    ax.set_yticklabels([d[0] for d in data], fontsize=9.5)
    ax.set_xscale("log")
    ax.set_xlim(0.5, 4000)
    ax.set_xlabel("HTTP response time, ms (log scale)")
    ax.set_title("API response time by endpoint (OVS4, one sweep)", fontsize=13,
                 color=INK_PRIMARY, loc="left", pad=12)
    style_axes(ax, x_grid=True, y_grid=False)

    handles = [mpatches.Patch(color=c, label=cat_label[k]) for k, c in color.items()]
    ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=8.8, ncol=1)
    fig.tight_layout()
    save(fig, "fig6_endpoint_latency_profile")


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    fig6()
