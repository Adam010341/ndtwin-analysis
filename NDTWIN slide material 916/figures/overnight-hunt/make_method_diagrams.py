#!/usr/bin/env python3
"""
make_method_diagrams.py -- the two method diagrams for the 916 deck.

    fig_m1_hunt_pipeline   one night of the overnight hunt, six stages + the loop  (827 E4b)
    fig_m2_persona_axis    the role-play grid: six personas x four axes + R7       (827 E4a)

Every number and label in here comes from
    .claude/skills/overnight-hunt/SKILL.md                     (the written spec: axes, deck)
    scratch/overnight-2026-09-05/hunt-0911/00-LEDGER.md        (the 09-11 night ledger)
    scratch/overnight-2026-09-05/hunt-0911/ROLE-*.md           (the eleven role briefs)
    tests/fixtures/live_cells/README.md                        (the red half of a cell)
    tools/test_workflow/live_cells/CELLS.md                    (round 0)
and is cited line-by-line in the companion <name>.md next to each figure. This script is the
vector source; the .md is the provenance. Nothing is computed at run time -- the numbers are
literals below so the output is byte-stable.

Drawing rules: 827 template E2 (palette + Arial), E4a (architecture), E4b (flowchart).
916 template rule 6 (Adam 09-15): a slide carries only tables, big headings, architecture
diagrams and data visualisations -- so these two carry no caption and no verdict chip. The
reading goes in the speaker notes.

[Co-developed with claude code -- Adam]

Regenerate:
    "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_method_diagrams.py

writes, for each of the two names, into this directory:
    <name>.pdf   <name>.png (300 dpi)   <name>.svg   _hires/<name>.png (500 dpi)
"""
import os

import matplotlib

assert matplotlib.__version__.startswith("3.10") or matplotlib.__version__.startswith("3.11"), \
    f"unexpected matplotlib {matplotlib.__version__}; re-verify the figures render as expected"

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["font.monospace"] = ["Courier New", "Liberation Mono", "DejaVu Sans Mono"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

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


# ---- primitives (same shapes as make_gap_diagrams.py) ----------------------------------
def canvas(w, h):
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
        mono=False, z=5, rot=0):
    kw = dict(MONO) if mono else {}
    return ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=z, rotation=rot, **kw)


def arrow(ax, x1, y1, x2, y2, color=INK, lw=1.0, ls="-", head=0.09, z=3):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), zorder=z,
                arrowprops=dict(arrowstyle=f"-|>,head_width={head*1.6},head_length={head*2.4}",
                                color=color, linewidth=lw, linestyle=ls,
                                shrinkA=0, shrinkB=0, joinstyle="miter"))


def elbow(ax, pts, color=INK, lw=1.0, ls="-", head=0.09, z=3):
    for a, b in zip(pts[:-1], pts[1:-1]):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw, ls=ls, zorder=z,
                solid_capstyle="butt")
    arrow(ax, *pts[-2], *pts[-1], color=color, lw=lw, ls=ls, head=head, z=z)


def save(fig, name):
    os.makedirs(HIRES, exist_ok=True)
    fig.savefig(os.path.join(OUTDIR, f"{name}.pdf"), facecolor=WHITE)
    fig.savefig(os.path.join(OUTDIR, f"{name}.png"), facecolor=WHITE, dpi=300)
    fig.savefig(os.path.join(OUTDIR, f"{name}.svg"), facecolor=WHITE)
    fig.savefig(os.path.join(HIRES, f"{name}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"wrote {name}.{{pdf,png,svg}} + _hires/{name}.png")


# ==========================================================================================
# fig_m1 -- one night of the hunt.  Six stages left to right; the sixth feeds the first.
# The lab-touching stage is the only filled one: everything before it is read-only, and that
# ordering is the method's main claim ("reconnaissance first", LEDGER 23:5x).
# ==========================================================================================
STAGES = [
    # (kicker, title, line 1, line 2)
    ("ROUND 0", "Last night's cells", "11 regression cells", "each one failed once"),
    ("RECON", "Read the code", "2 agents, read-only", "51 + 13 hypotheses"),
    ("FALSIFY", "Kill them offline", "27 held · 12 died", "8 unreachable"),
    ("ROLES", "Play the operator", "11 roles on the lab", "45 min each, serialised"),
    ("FIX", "Fix behind a gate", "mutation gate", "no red, no delivery"),
    ("CELL", "Freeze the evidence", "pre-fix raw = old/", "must FAIL forever"),
]


def fig_m1():
    W, H = 12.44, 5.42
    fig, ax = canvas(W, H)

    txt(ax, W / 2, 0.50, "One night of the hunt", size=19, weight="bold", color=INK)

    n = len(STAGES)
    x0, gap = 0.42, 0.26
    bw = (W - 2 * x0 - (n - 1) * gap) / n
    top, bh = 1.28, 1.14

    for i, (kick, title, l1, l2) in enumerate(STAGES):
        x = x0 + i * (bw + gap)
        lab = (i == 3)                      # the only stage that touches the testbed
        box(ax, x, top, bw, bh,
            fill=ACCENT_BG if lab else WHITE,
            edge=ACCENT if lab else INK,
            lw=2.2 if lab else 1.0, radius=0.05)

        # Adam 09-16: keep the black bold headings, drop the grey small text.  The kicker
        # row is gone and the two detail lines are one colour, not BODY over MUTED.
        # Adam 09-16: the box carries its black bold heading and nothing else.  The two
        # detail lines and the rule between them are gone -- those numbers live in
        # SPEAKING-GUIDE-0916.md, which is where the reading belongs (916 rule 6).
        # 13.0 pushed "Freeze the evidence" past its box edge; 1.72 in is the box width.
        txt(ax, x + bw / 2, top + bh / 2, title, size=11.8, weight="bold", color=INK)

        if i < n - 1:
            arrow(ax, x + bw + 0.03, top + bh / 2, x + bw + gap - 0.03, top + bh / 2,
                  color=INK, lw=1.2)

    # ---- the loop: stage 6 back to stage 1 -----------------------------------------------
    xl = x0 + (n - 1) * (bw + gap)
    y_loop = top + bh + 0.62
    elbow(ax, [(xl + bw / 2, top + bh + 0.03),
               (xl + bw / 2, y_loop),
               (x0 + bw / 2, y_loop),
               (x0 + bw / 2, top + bh + 0.03)],
          color=ACCENT, lw=1.3, ls=(0, (3.2, 2.0)))
    txt(ax, (x0 + xl) / 2 + bw / 2, y_loop - 0.24,
        "tonight's finding becomes tomorrow's round 0",
        size=10.0, color=ACCENT, weight="bold")

    # ---- the read-only / lab divider ------------------------------------------------------
    xdiv = x0 + 3 * (bw + gap) - gap / 2
    ax.plot([xdiv, xdiv], [top - 0.46, top + bh + 0.16],
            color=RULE, lw=1.0, ls=(0, (2.0, 2.0)), zorder=1)
    txt(ax, xdiv - 0.14, top - 0.30, "read-only", size=10.5, color=INK,
        weight="bold", ha="right")
    txt(ax, xdiv + 0.14, top - 0.30, "on the testbed", size=10.5, color=ACCENT,
        ha="left", weight="bold")

    # ---- the parallel auditor band --------------------------------------------------------
    by = top + bh + 1.02
    box(ax, x0, by, W - 2 * x0, 0.62, fill=PANEL, edge=RULE, lw=0.9, radius=0.05)
    txt(ax, x0 + 0.30, by + 0.31, "R7", size=9.0, color=ACCENT, weight="bold",
        ha="left", mono=True)
    txt(ax, x0 + 0.86, by + 0.31,
        "a reconciler runs the whole night, read-only, one pass every 10 minutes",
        size=11.0, color=INK, weight="bold", ha="left")

    # ---- the per-role envelope ------------------------------------------------------------
    ey = by + 0.92
    box(ax, x0, ey, W - 2 * x0, 0.76, fill=WHITE, edge=INK, lw=1.0, radius=0.05)
    # Explicit x positions, not an accumulator: the widths of the four labels are not equal
    # and guessing them once put "compare to baseline" on top of the warning (caught on the
    # rendered PNG, 09-15).  Steps live left of the divider, the warning right of it.
    steps = [("baseline first", 0.86), ("45 minutes", 2.90),
             ("restore", 4.66), ("compare to baseline", 6.20)]
    for j, (s, sx) in enumerate(steps):
        txt(ax, sx, ey + 0.38, s, size=11.0, color=ACCENT if j == 3 else INK,
            weight="bold", ha="left")
        if j < len(steps) - 1:
            a0 = sx + {0: 1.48, 1: 1.26, 2: 0.86}[j]
            arrow(ax, a0, ey + 0.38, steps[j + 1][1] - 0.16, ey + 0.38,
                  color=FAINT, lw=1.0, head=0.075)
    xsep = 8.70
    ax.plot([xsep, xsep], [ey + 0.14, ey + 0.62], color=RULE, lw=0.9, zorder=4)
    txt(ax, W - x0 - 0.30, ey + 0.38, "if they differ, the round is void",
        size=11.0, color=WARNC, weight="bold", ha="right")

    save(fig, "fig_m1_hunt_pipeline")


# ==========================================================================================
# fig_m2 -- the role-play grid.  Rows are personas, columns are the axes a role is sent
# down.  A role is a persona crossed with one or two axes; the cells say which role that was.
# ==========================================================================================
# SKILL.md:149-168 defines FOUR axes, in this order.  "Docs" is not an axis: the spec says a
# role is "one axis + one concrete action surface", and ROLE-11's surface is the handbook.
AXES = ["Time", "Scale", "State", "Intent"]

# persona -> {axis: role label}.  From the first line of each hunt-0911/ROLE-*.md, and the
# role deck at SKILL.md:170-181.  R7 is in that deck too, as the standing cross-axis role.
PERSONAS = [
    ("The successor",           "starts from someone else's wreckage",
     {"State": "1 · 6 · 8", "Intent": "1 · 8", "Time": "6"}),
    ("The restart cycler",      "up and down, over and over, never cleaning",
     {"Time": "2 · 9", "State": "2", "Scale": "9"}),
    ("The grad student",        "wants one figure, edits the topology file",
     {"Intent": "3", "Scale": "3"}),
    ("The second operator",     "starts while the first one is mid-teardown",
     {"Time": "4 · 12"}),
    ("The traffic pusher",      "rules every second for an hour",
     {"Scale": "5 · 10"}),
    ("The manual follower",     "reads only the handbook, one step no more",
     {"Intent": "11"}),
]

# The sixth row of the spec's deck: read-only, spans every axis, runs beside the others.
STANDING = ("The reconciler", "R7", "reads only, all night, beside whoever is on the lab")


def fig_m2():
    W, H = 12.44, 7.34      # six persona rows + the standing role + the footer band
    fig, ax = canvas(W, H)

    txt(ax, W / 2, 0.50, "A role is two assumptions, crossed",
        size=19, weight="bold", color=INK)

    left, top = 4.62, 1.30
    cw = (W - left - 0.46) / len(AXES)
    rh = 0.66            # 0.735 put the footer band past the canvas edge (caught on the PNG)

    for j, a in enumerate(AXES):
        txt(ax, left + j * cw + cw / 2, top - 0.30, a, size=11.0,
            weight="bold", color=BODY)

    for i, (name, blurb, cells) in enumerate(PERSONAS):
        y = top + i * rh
        if i % 2 == 0:
            box(ax, 0.42, y, W - 0.88, rh, fill=PANEL, edge="none", lw=0, z=1)
        # Adam 09-16: keep the black bold headings, drop the grey small text.
        txt(ax, 0.62, y + rh / 2, name, size=12.5, weight="bold", color=INK, ha="left")

        for j, a in enumerate(AXES):
            cx = left + j * cw + cw / 2
            if a in cells:
                bwid = 0.96
                box(ax, cx - bwid / 2, y + 0.12, bwid, rh - 0.24,
                    fill=ACCENT_BG, edge=ACCENT, lw=1.2, z=6, radius=0.045)
                txt(ax, cx, y + rh / 2, cells[a], size=10.0, color=ACCENT,
                    weight="bold", z=7, mono=True)
            else:
                ax.plot([cx], [y + rh / 2], marker=".", ms=2.6, color=RULE, zorder=4)

    # ---- the standing role: one row, spanning every axis --------------------------------
    sy = top + len(PERSONAS) * rh + 0.10
    name, tag, blurb = STANDING
    txt(ax, 0.62, sy + rh / 2, name, size=12.5, weight="bold", color=INK, ha="left")
    box(ax, left + 0.02, sy + 0.12, len(AXES) * cw - 0.52, rh - 0.24,
        fill=PANEL, edge=ACCENT, lw=1.2, ls=(0, (2.6, 1.8)), z=6, radius=0.045)
    txt(ax, left + (len(AXES) * cw - 0.48) / 2, sy + rh / 2,
        f"{tag}   every axis, in parallel", size=10.0, color=ACCENT,
        weight="bold", z=7)

    ax.plot([left - 0.20, left - 0.20], [top - 0.50, sy + rh],
            color=RULE, lw=0.9, zorder=1)

    # ---- the footer band: the one sentence the spec puts on dispatch --------------------
    fy = sy + rh + 0.34
    box(ax, 0.42, fy, W - 0.88, 0.78, fill=WHITE, edge=INK, lw=1.0, radius=0.05)
    txt(ax, W / 2, fy + 0.39, "A role is handed a motive, never a test case",
        size=13.5, color=INK, weight="bold")
    assert fy + 0.78 < H, f"footer band ends at {fy + 0.78:.2f}, past the {H} canvas"

    save(fig, "fig_m2_persona_axis")


if __name__ == "__main__":
    # count assertions -- the figure must not drift from the ledger
    n_roles = len({r for _, _, c in PERSONAS for cell in c.values() for r in cell.split(" · ")})
    assert n_roles == 11, f"grid names {n_roles} roles, the 09-11 hunt ran 11 (no ROLE-7)"
    assert len(STAGES) == 6, "the pipeline has six stages"
    print(f"roles named in the grid: {n_roles}")
    fig_m1()
    fig_m2()
