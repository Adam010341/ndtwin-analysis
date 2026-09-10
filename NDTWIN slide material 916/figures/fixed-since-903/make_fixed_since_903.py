#!/usr/bin/env python3
"""
make_fixed_since_903.py -- fig_h1_fixed_since_903, the kanban for the 909 deck's
"Found, then fixed -- since 09-03" page.

Spec:  NDTwin-slide-template-916.md   section C-909-H   (this figure, element by element)
Data:  FIXED-SINCE-903.md             sections 1, 2.0-2.4, 3
Style: NDTwin-slide-template-827.md   section E2 (palette + Arial), E4a (black frame,
                                      white ground, exactly one accent colour)

DRAFT.  Adam's other agent produces the final artwork; this script exists so the numbers,
the brick set and the layout can be reconciled against git.  Every datum below is a
literal with its source next to it -- nothing is read from the repo at run time, so the
output is byte-stable.  The classification column was derived once, by hand, from

    git show  --numstat --format= -m --first-parent <merge commit>     (section 2 rows)
    git diff  --numstat <nearest ancestor branch>...<branch>           (section 3 rows)

and the rule + every per-brick result is written out in fig_h1_fixed_since_903.md.

[Co-developed with claude code -- Adam]

Regenerate:
    "/home/adam/Desktop/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_fixed_since_903.py

writes into this directory:
    fig_h1_fixed_since_903.pdf   .png (300 dpi)   .svg   _hires/<same>.png (500 dpi)
"""
import os

import matplotlib

assert matplotlib.__version__.startswith("3.10") or matplotlib.__version__.startswith("3.11"), \
    f"unexpected matplotlib {matplotlib.__version__}; re-verify the figure renders as expected"

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Arial per 827 E2; Liberation Sans is the metric-compatible stand-in on this laptop.
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["svg.fonttype"] = "none"   # keep SVG text editable
plt.rcParams["pdf.fonttype"] = 42       # embed TrueType, not Type 3

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")
NAME = "fig_h1_fixed_since_903"

# ---- 827 E2 palette --------------------------------------------------------------------
INK = "#1A1A1A"
MUTED = "#4F4F4F"
FAINT = "#6E6E6E"
RULE = "#D0D0D0"
ACCENT = "#065A82"
ACCENT_BG = "#EEF3F6"
PANEL = "#F7F8F9"
WHITE = "#FFFFFF"

# brick fill by layer -- C-909-H: kernel C++ = ACCENT_BG, ndt/lab tools = PANEL,
# proxy / harness / docs = white.  "MIX" (undecidable) also renders white; see the .md.
#
# DEVIATION (flagged in the .md): 827 E2's PANEL is #F7F8F9, three levels off white.  On a
# 0.72" brick that is invisible -- two of the three classes then read identically and the
# fill stops carrying meaning.  The tools class is drawn one neutral step deeper.  It is
# still a neutral, so E4a's "exactly one accent colour" still holds.  Chips and the legend
# swatch use the same value so the legend keeps matching the bricks.
PANEL_DEEP = "#DEE3E7"
FILL = {"K": ACCENT_BG, "T": PANEL_DEEP, "W": WHITE, "MIX": WHITE}


# =========================================================================================
# DATA -- literals.  (code, layer) per brick, in the order the source file lists them.
#
#   layer  K   kernel C++            src/ , include/ , tests/*.cpp
#          T   ndt / lab tooling     tools/test_workflow/ , tools/remote-lab/
#          W   proxy / harness/docs  p4_proxy/ , chaos harness, contract_test, gate scripts
#          MIX no single layer >= 60% of the production churn -> drawn white
#
# The merge commit / branch tip that each brick was measured on is in the .md table.
# =========================================================================================

# FIXED-SINCE-903.md section 2.0 -- 09-02 fix-design campaign, 20 rows, all merged 09-02
# (16 fixes + 4 instrument/wiring commits; the last four were added to the source on 09-08
# after `git log --merges 06bc60ac..36d832f5` was checked against the table).
# Flagged "?" on the figure: this is the day before the 903 cut, pending Adam's word on
# whether he already presented them (section 0, first bullet).
TRUNK_0902 = [
    ("A-2", "W"),            # 404b11a8  tools/ryu_apps/rest_topology_bounded.py
    ("A-4c", "W"),           # 0da64329  p4_proxy/proxy_agent/rule_journal.py
    ("A-4d", "W"),           # 8b87a9de  p4_proxy/proxy_agent/topology_manager.py
    ("A-4f", "K"),           # 36e3d78a  src/.../OVSPowerStrategy.cpp
    ("A-7", "W"),            # a4a8eb2c  tools/contract_test/ + p4_proxy/ dominate
    ("A-9", "K"),            # 49a3f084  include/.../LockManager.hpp
    ("B-2b/B-4", "K"),       # 4c49b050  include/utils/Utils.hpp
    ("B-3", "K"),            # bac267cb  src/ndt_core/http/HttpSession.cpp
    ("B-x", "K"),            # cc9a9ea4  include/common_types/SFlowType.hpp
    ("F-1", "K"),            # b259c4d9  src/.../DeviceConfigurationAndPowerManager.cpp
    ("F-6", "K"),            # fc2cd427  include/.../StaleTableCarryForward.hpp
    ("F-8", "K"),            # dc969792  include/common_types/GraphTypes.hpp
    ("F-13", "K"),           # 9430bfbe  src/.../HttpRoutingStrategyBase.cpp
    ("F-14/16/4", "K"),      # 2bda7af1  src/.../TopologyAndFlowMonitor.cpp
    ("F-15", "W"),           # 33338e15  p4_proxy/mininet/grpc_ports.py
    ("A-8", "W"),            # aa44bdf1  tools/contract_test/{spec,check_logs,run_contract_test}.py
    ("B-1 test", "W"),       # e88f1b71  wiring test only: tests/python/test_t11_filter_is_wired.py
    ("G-2 instr", "W"),      # 9f022901  doc/audit/2026-08-30_live-full-stack-round/harness/lib.sh
    ("A-4e instr", "W"),     # 99e9abd9  tests/shell/check_gate_anchors.py (gate instrument)
    ("rate denom", "W"),     # aba03849  gate bookkeeping only -- no production file
]

# section 2.1 -- 09-03, 30 fixes (MERGE-LOG rows 1-32 minus the 2 documentation-only rows
# 9b85ee11 and 582241ef, which are not drawn; see the .md, "what is not on the figure").
TRUNK_0903 = [
    ("#58", "W"),            # 76d299d3  (REPORT-PICK A-8; KNOWN-ISSUES A-8 is the 09-02 brick)  p4_proxy/proxy_agent/ryu_topology.py
    ("P4 priority", "W"),    # 323668ad  p4_proxy/proxy_agent/api_routes.py
    ("L-9", "W"),            # 002e226c  tools/make_topology.py
    ("G-7", "T"),            # 2152d368  tools/test_workflow/ndtwin-lab
    ("G-9", "T"),            # 5e5989c7  tools/test_workflow/ndtwin-lab
    ("G-6", "T"),            # c42cc07d  tools/test_workflow/ndt
    ("redirection", "T"),    # 49b91654  tools/test_workflow/ndt + tools/remote-lab/*.sh
    ("#22/#23/#24", "T"),    # fbb83b03  tools/test_workflow/ports.sh
    ("A-14", "T"),           # b5fe780f  tools/test_workflow/sudo_surface.sh
    ("ndt up ovs", "T"),     # 50e8b78e  tools/test_workflow/ndt
    ("B-5/#5", "T"),         # 0e11c229  tools/test_workflow/stack.sh + supervise.sh
    ("#32", "K"),            # 0b34af5f  include/.../TopologyAndFlowMonitor.hpp
    ("#10/#18", "K"),        # b76a2493  src/.../FlowLinkUsageCollector.cpp
    ("sflow health", "K"),   # ea139d1c  src/.../FlowLinkUsageCollector.cpp
    ("#69/#70 doc", "K"),    # 89857244  src/utils/Logger.cpp
    ("topo round", "K"),     # d00fa57c  src/.../TopologyAndFlowMonitor.cpp
    ("topo load", "K"),      # 70c324e1  src/.../TopologyAndFlowMonitor.cpp
    ("#4/A-12", "T"),        # 5e355dda  tools/test_workflow/ndt + ovs_4host_topo.py
    ("#71", "W"),            # 486d89fb  p4_proxy/proxy_agent/main.py
    ("#17", "W"),            # 65d4a32f  chaos harness probes.py / invariants.py
    ("#73/#74", "W"),        # 431d98a5  tools/contract_test/components.py
    ("#47", "K"),            # 08267dcb  src/utils/FdHygiene.cpp
    ("#42/G-10", "W"),       # 014903fb  testbed_topo.py
    ("#6/#48/G-11", "T"),    # 31b9ea8a  tools/test_workflow/ndt
    ("#78", "W"),            # 1ec39977  tests/shell/check_gate_anchors.py (gate instrument)
    ("#46/#36/#35", "K"),    # 34e2109d is the raw-removal merge; body 7e8d91e0 = src/+include/
    ("#69/#70", "K"),        # ec0a0445  src/utils/Logger.cpp
    ("#77", "T"),            # 06bc713d  tools/test_workflow/ndtwin-lab
    ("#75", "W"),            # 078b2736  chaos harness chaos.py / invariants.py
    ("#8", "T"),             # 48c929fc  tools/test_workflow/ndt
]

# section 2.2 -- 09-04, 9 fixes (MERGE-LOG rows 33-42).
TRUNK_0904 = [
    ("A-11", "T"),           # 257e4eb0  tools/test_workflow/ndt   (row "#3/#21/#49/#83")
    ("#61/#62", "K"),        # e9d8a486  src/.../TopologyAndFlowMonitor.cpp
    ("#38", "K"),            # 27d48eda  src/.../SimulationRequestManager.cpp
    ("#82", "K"),            # 3d2b38fe  src/.../OVSPowerStrategy.cpp
    ("#27/#76", "K"),        # ac703196 is the follow-up; body 63792cc9 = include/utils/StopSignal.hpp
    ("Q12", "K"),            # 95a9f743  src/.../DeviceConfigurationAndPowerManager.cpp
    ("#1/A-10", "K"),        # d599c476  src/.../HttpRoutingStrategyBase.cpp
    ("#85", "K"),            # 93edd0fd (+8103457b)  src/.../DeviceConfigurationAndPowerManager.cpp
    ("#2/C-4", "K"),         # c2b55184  src/.../DeviceConfigurationAndPowerManager.cpp
]

# section 2.3 -- 09-05, 8 items (4 W-series through cdc8dad9, 2 fixes, 2 gate instruments).
# W4/#54 is NOT here: section 2.3's closing note says options only, no code -> not a fix.
TRUNK_0905 = [
    ("W7", "T"),             # 9de04f53  tools/test_workflow/ndt
    ("W6", "K"),             # f8dbad66  src/ndt_core/http/HttpSession.cpp
    ("W1/#87", "K"),         # f2126cc5  src/.../HttpRoutingStrategyBase.cpp
    ("W5/OV-1", "K"),        # 0903b202  src/.../TopologyAndFlowMonitor.cpp
    ("#89/W3", "K"),         # 336d831e  src/.../TopologyAndFlowMonitor.cpp
    ("#88/W2", "K"),         # cff98191  src/.../TopologyAndFlowMonitor.cpp
    ("anchor L1", "W"),      # 11fd457e  tests/shell/check_gate_anchors.py
    ("anchor 68", "W"),      # 68c1dde4  tests/shell/check_gate_anchors.py
]

# section 3 -- fixed but sitting on branches, nothing pushed.  Date = the "chain / round"
# column: second half = 09-06, round 2 = 09-07, round 3 = 09-08.
# Branch diffs are taken against the branch's nearest ancestor in its chain, not against
# trunk, or a stacked branch inherits its predecessors' files (see the .md).
BRANCH_0906 = [
    ("W8", "K"),             # fix/w8-declared-link-failure-sticky   include/utils/NetemLinkFault.hpp
    ("W3-3b", "K"),          # fix/w3-door3b-host-empty-ip           src/.../TopologyAndFlowMonitor.cpp
    ("W15", "K"),            # fix/w15-unknown-brand-rejected        src/.../TopologyAndFlowMonitor.cpp
    ("W10", "K"),            # fix/w10-nickname-overlay              src/.../TopologyAndFlowMonitor.cpp
    ("W14", "K"),            # fix/w14-index-zero-guards             src/.../IntentTranslator.cpp
    ("W11", "K"),            # fix/w11-dispatch-status-...           include/.../DispatchOutcomeLog.hpp
    ("W12/W13", "T"),        # fix/ndt-honesty-0906                  tools/test_workflow/ndt
    ("W16", "T"),            # fix/w16-apps-stop-lists-rules         tools/test_workflow/ndt
    ("conventions", "W"),    # chore/conventions-0906                cmake/sanitizer-flags.cmake
]
BRANCH_0907 = [
    ("W8-8", "W"),           # fix/chaos-blackhole-attach-under-shaper  chaos harness actions.py
    ("W3b-3", "W"),          # fix/contract-per-node-identity           tools/contract_test/spec.py
    ("intent-tmpdir", "W"),  # fix/intent-task-outcomes-per-test-tmpdir tests only, no prod file
    ("W15-2", "K"),          # fix/w15b-switch-kind-exemption           include/common_types/GraphTypes.hpp
    ("W18", "K"),            # fix/w18-eighth-index-zero                src/.../TopologyAndFlowMonitor.cpp
    ("W17", "K"),            # fix/w17-capacity-current-plane           src/.../OpenflowCapacityReport.cpp
]
BRANCH_0908 = [
    ("W16-1/2/3", "T"),      # fix/ndt-round2-0907                tools/test_workflow/ndt
    ("3-51", "T"),           # fix/ndt-3-51-helper-apps-window    tools/test_workflow/ndt
    ("W8b", "K"),            # fix/w8b-withdrawal-...             src/ndt_core/http/HttpSession.cpp
    ("E-20", "K"),           # fix/e20-startup-sweep-...          src/.../TopologyAndFlowMonitor.cpp
    ("E-21", "W"),           # fix/e21-link-endpoints-in-contract tools/contract_test/spec.py
    ("BUG-17", "K"),         # fix/bug17-mixed-dataplane-refused  src/.../TopologyAndFlowMonitor.cpp
    ("E-23/25", "K"),        # fix/e23-e25-exempt-switch-on-wire  src/.../DeviceConfig...Manager.cpp
    ("E-4", "W"),            # fix/e4-chaos-needs-opt-in-...      chaos harness chaos.py
    ("E-17", "W"),           # fix/e17-test-tmpdir-carries-pid    tests/shell/check_test_tmpdirs.py
    ("G-13", "W"),           # fix/g13-p4-rule-install-time       p4_proxy/proxy_agent/rule_install_times.py
    ("E-2", "MIX"),          # fix/e2-kernel-reports-loaded-model K 43% / T 32% / W 26% -> mixed
    ("E-29", "K"),           # fix/e29-update-hosts-race-evidence src/.../TopologyAndFlowMonitor.cpp
    ("KIREF", "W"),          # fix/known-issues-refs-by-entry-code gate + tests only
    ("E-1/E-3", "W"),        # fix/docs-e1-e3-findings-coverage    documentation only
]

# axis: C-909-H, "09-02 | 09-03 | 09-04 | 09-05 | 09-06 | 09-07 | 09-08"
DATES = ["09-02", "09-03", "09-04", "09-05", "09-06", "09-07", "09-08"]
TRUNK_BY_DATE = {"09-02": TRUNK_0902, "09-03": TRUNK_0903,
                 "09-04": TRUNK_0904, "09-05": TRUNK_0905}
BRANCH_BY_DATE = {"09-06": BRANCH_0906, "09-07": BRANCH_0907, "09-08": BRANCH_0908}

# ---- counts asserted against the source file --------------------------------------------
N_TRUNK = sum(len(v) for v in TRUNK_BY_DATE.values())
N_BRANCH = sum(len(v) for v in BRANCH_BY_DATE.values())

# FIXED-SINCE-903.md section 1: 47 merged fixes (2.1 + 2.2 + 2.3) plus the 20 of 2.0.
# 47 stays the chip's number -- it is defined as the branches merged 09-03 -> 09-05, so the
# 09-02 column (the "?" bricks) is deliberately outside it.
# Section 2.5 (5 fixes + 1 follow-up that landed straight on the trunk line, never on a
# branch) gets no bricks: section 1 excludes it from the 47 and C-909-H draws only 2.0-2.3.
EXPECT_TRUNK = 47 + 20
# Section 3's *header* still says 27, and so does C-909-H's chip string, but section 3's
# table has 29 rows -- and `git for-each-ref` + `git merge-base --is-ancestor` finds 29
# unmerged branches on 09-08 (28 under refs/heads/fix/ plus chore/conventions-0906).
# Section 1 was corrected to 29 on 09-08 20:4x.  The figure follows git.
EXPECT_BRANCH_STATED = 29
EXPECT_BRANCH_ROWS = 29

print(f"bricks ON TRUNK              : {N_TRUNK}   (section 1 expects {EXPECT_TRUNK} = 47 + 20)")
print(f"bricks ON BRANCHES, NOT MERGED: {N_BRANCH}   (section 3 header says "
      f"{EXPECT_BRANCH_STATED}; its table has {EXPECT_BRANCH_ROWS} rows, git agrees with "
      f"{EXPECT_BRANCH_ROWS})")
assert N_TRUNK == EXPECT_TRUNK, f"trunk bricks {N_TRUNK} != {EXPECT_TRUNK}"
assert N_BRANCH == EXPECT_BRANCH_ROWS, f"branch bricks {N_BRANCH} != {EXPECT_BRANCH_ROWS}"
assert len(TRUNK_0902) == 20 and len(TRUNK_0903) == 30
assert len(TRUNK_0904) == 9 and len(TRUNK_0905) == 8
assert len(BRANCH_0906) == 9 and len(BRANCH_0907) == 6 and len(BRANCH_0908) == 14

# the three chips of C-909-H.  47 is right (2.1+2.2+2.3); 27 is not (see above) -> 29.
CHIPS = ["47 FIXES ON TRUNK", "29 BRANCHES WAITING", "0 ON THE PUBLIC REPO"]
VERDICT = "FIXED / NOT SHIPPED"
TITLE = "Found, then fixed — since 09-03"
LEGEND = [("K", "kernel C++"), ("T", "ndt / lab tools"), ("W", "proxy / harness / docs")]

# ---- geometry (inches; y grows downward) -------------------------------------------------
W, H = 12.44, 7.00           # 16:9
M = 0.50                     # left/right margin
CW = W - 2 * M
ROWS = 8                     # bricks stacked per sub-column before a new sub-column starts
BR_H = 0.21                  # brick height
PITCH = 0.245                # brick row pitch
GAP = 0.10                   # horizontal gap between bricks

Y_TITLE = 0.50
Y_DATES = 1.05
Y_AXRULE = 1.20
Y_T_LABEL = 1.44             # "ON TRUNK"
Y_T_TOP = 1.58
Y_B_LABEL = 3.82             # "ON BRANCHES . NOT MERGED"
Y_B_TOP = 3.96
Y_GRIDBOT = 6.02
Y_LEGEND = 6.22
Y_CHIPS = 6.56
CHIP_H = 0.26


def sub_cols(n):
    """How many sub-columns a date needs, and how many bricks in each (balanced)."""
    k = max(1, -(-n // ROWS))
    base, rem = divmod(n, k)
    return [base + (1 if i < rem else 0) for i in range(k)]


# lay the date axis out proportionally to the sub-columns each date needs
SPLIT = {}
for d in DATES:
    items = TRUNK_BY_DATE.get(d) or BRANCH_BY_DATE[d]
    SPLIT[d] = sub_cols(len(items))
TOTAL_SUB = sum(len(v) for v in SPLIT.values())
SUB_W = CW / TOTAL_SUB

COL_X = {}
x = M
for d in DATES:
    w = len(SPLIT[d]) * SUB_W
    COL_X[d] = (x, w)
    x += w
X_LASTMERGE = COL_X["09-05"][0] + COL_X["09-05"][1]   # 09-05 15:27, cdc8dad9


# ---- primitives --------------------------------------------------------------------------
def canvas():
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    return fig, ax


def txt(ax, x, y, s, size=9.0, color=INK, weight="normal", ha="center", va="center", z=5):
    return ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=z)


def spaced(s, sp=" "):
    """Poor man's charSpacing (827 E2 uses 1.0 pt on band labels)."""
    return sp.join(s)


def band_label(ax, x, y, s):
    """Band name, on a white patch so the date grid lines do not run through it."""
    ax.text(x, y, spaced(s), fontsize=8.5, color=MUTED, fontweight="bold",
            ha="left", va="center", zorder=5,
            bbox=dict(facecolor=WHITE, edgecolor="none", pad=2.2))


def fit(s, avail_in, start=7.0, floor=5.6):
    """Largest size <= start at which s fits avail_in inches (Arial ~ 0.50 em average)."""
    size = start
    while size > floor and len(s) * 0.50 * size / 72.0 > avail_in:
        size -= 0.2
    return size


def brick(ax, x, y, w, layer, label, dashed, query=False):
    ls = (0, (2.2, 1.5)) if dashed else "solid"
    ax.add_patch(Rectangle((x, y), w, BR_H, facecolor=FILL[layer], edgecolor=INK,
                           linewidth=0.85, linestyle=ls, zorder=3))
    pad = 0.14 if query else 0.07
    txt(ax, x + (w - (0.09 if query else 0.0)) / 2, y + BR_H / 2 + 0.005, label,
        size=fit(label, w - pad), color=INK, z=5)
    if query:
        # C-909-H: every 09-02 brick carries a "?" corner mark (the day before the cut)
        txt(ax, x + w - 0.055, y + 0.062, "?", size=6.0, color=ACCENT, weight="bold", z=6)


def band(ax, date_list, by_date, y_top, dashed, query_dates=()):
    for d in date_list:
        items = by_date[d]
        x0, _ = COL_X[d]
        i = 0
        for sc, count in enumerate(SPLIT[d]):
            bx = x0 + sc * SUB_W + GAP / 2
            for r in range(count):
                label, layer = items[i]
                brick(ax, bx, y_top + r * PITCH, SUB_W - GAP, layer, label,
                      dashed, query=(d in query_dates))
                i += 1


def chip(ax, x, y, label, size=8.0, fill=PANEL, edge=RULE, color=MUTED, bar=None):
    pad = 0.16
    w = len(label) * 0.55 * size / 72.0 + 2 * pad
    ax.add_patch(Rectangle((x, y), w, CHIP_H, facecolor=fill, edgecolor=edge,
                           linewidth=0.8, zorder=3))
    if bar:
        ax.add_patch(Rectangle((x, y), 0.045, CHIP_H, facecolor=bar, edgecolor="none",
                               zorder=4))
    txt(ax, x + w / 2 + (0.02 if bar else 0), y + CHIP_H / 2 + 0.005, label,
        size=size, color=color, weight="bold", z=5)
    return w


# ---- the figure --------------------------------------------------------------------------
def build():
    fig, ax = canvas()

    txt(ax, M, Y_TITLE, TITLE, size=15.0, color=INK, weight="bold", ha="left")

    # date axis
    for d in DATES:
        x0, w = COL_X[d]
        txt(ax, x0 + w / 2, Y_DATES, d, size=9.5, color=MUTED, weight="bold")
    ax.plot([M, M + CW], [Y_AXRULE, Y_AXRULE], color=RULE, lw=0.8, zorder=1)
    for d in DATES[1:]:
        x0, _ = COL_X[d]
        ax.plot([x0, x0], [Y_AXRULE, Y_GRIDBOT], color=RULE, lw=0.5, zorder=1)
    ax.plot([M + CW, M + CW], [Y_AXRULE, Y_GRIDBOT], color=RULE, lw=0.5, zorder=1)

    # band 1: ON TRUNK, solid bricks, left of the line only
    band_label(ax, M, Y_T_LABEL, "ON TRUNK")
    band(ax, ["09-02", "09-03", "09-04", "09-05"], TRUNK_BY_DATE, Y_T_TOP,
         dashed=False, query_dates=("09-02",))
    # section 2.4: 7 documentation-only commits, no bricks -- one small note, band right end
    txt(ax, M + CW - 0.10, Y_T_TOP + BR_H / 2, "+7 docs", size=7.5, color=FAINT,
        ha="right", z=5)

    # band 2: ON BRANCHES . NOT MERGED, dashed bricks, right of the line only
    band_label(ax, M, Y_B_LABEL, "ON BRANCHES · NOT MERGED")
    band(ax, ["09-06", "09-07", "09-08"], BRANCH_BY_DATE, Y_B_TOP, dashed=True)

    # the line the page is about: last merge into trunk, 09-05 15:27 (cdc8dad9)
    ax.plot([X_LASTMERGE, X_LASTMERGE], [Y_AXRULE + 0.14, Y_GRIDBOT],
            color=ACCENT, lw=1.3, ls=(0, (3.4, 2.2)), zorder=4)
    txt(ax, X_LASTMERGE, Y_AXRULE + 0.055, "last merge", size=7.5, color=ACCENT,
        weight="bold", z=6)

    # legend, three cells
    lx = M
    for layer, label in LEGEND:
        ax.add_patch(Rectangle((lx, Y_LEGEND), 0.30, 0.17, facecolor=FILL[layer],
                               edgecolor=INK, linewidth=0.85, zorder=3))
        txt(ax, lx + 0.39, Y_LEGEND + 0.088, label, size=8.0, color=MUTED, ha="left", z=5)
        lx += 0.39 + len(label) * 0.50 * 8.0 / 72.0 + 0.42

    # chips, then the verdict
    cx = M
    for c in CHIPS:
        cx += chip(ax, cx, Y_CHIPS, c) + 0.16
    vw = len(VERDICT) * 0.60 * 9.5 / 72.0 + 0.34
    chip(ax, M + CW - vw, Y_CHIPS, VERDICT, size=9.5, fill=WHITE, edge=ACCENT,
         color=ACCENT, bar=ACCENT)
    return fig


def save(fig, name):
    os.makedirs(HIRES, exist_ok=True)
    fig.savefig(os.path.join(OUTDIR, f"{name}.pdf"), facecolor=WHITE)
    fig.savefig(os.path.join(OUTDIR, f"{name}.png"), facecolor=WHITE, dpi=300)
    fig.savefig(os.path.join(OUTDIR, f"{name}.svg"), facecolor=WHITE)
    fig.savefig(os.path.join(HIRES, f"{name}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"wrote {name}.{{pdf,png,svg}} + _hires/{name}.png")


if __name__ == "__main__":
    save(build(), NAME)
