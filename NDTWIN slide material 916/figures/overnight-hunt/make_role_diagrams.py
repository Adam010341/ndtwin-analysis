#!/usr/bin/env python3
"""
make_role_diagrams.py -- one diagram per role, for the roles whose finding is a MECHANISM
a table cannot show.  Adam 09-15: "每個 role 做的工作 -- 如果足夠顯著的話 -- 都可以做一張圖".

    fig_r2_empty_but_confident   ROLE-2  the machine is empty, the twin is not
    fig_r3_two_doors_one_field   ROLE-3  the same field: file accepts, API refuses
    fig_r4_claim_race_window     ROLE-4  two claims in the same second, both granted
    fig_r12_stolen_marker        ROLE-12 two teardowns, one marker, whoever ends first deletes it
    fig_r10_sampling_instant     ROLE-10 one cut, three verdicts, depending on the second

Roles NOT given a figure, and why (the choice is deliberate, not an omission):
    ROLE-1  the mechanism is one request and one reply -- the table says it faster
    ROLE-5  same shape as fig3 of overnight-0904 (200 OK vs what the switch took); do not
            draw the same picture twice
    ROLE-6  "fixed three, broke one" is a sentence, not a picture
    ROLE-8  worth a figure if there is time: tc replace keeps the handle, so ownership is
            misread.  Sequence diagram, not built tonight.
    ROLE-9  worth a figure if there is time: knob written before the check.
    ROLE-11 the finding IS a table (8 manual-vs-tool mismatches) -- leave it a table.

Numbers come from scratch/overnight-2026-09-05/hunt-0911/00-LEDGER.md (the two nights'
ledger) and each role's ROLE-*-REPORT.md.  Cited line by line in the companion .md files.
Literals only -- the output is byte-stable.

Drawing rules: 827 E2 palette, E4a/E4b.  916 rule 6: figure pages carry the title and the
figure, nothing else.

[Co-developed with claude code -- Adam]

Regenerate:
    "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_role_diagrams.py
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

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
WARNC, WARN_BG, WHITE = "#9C3B2E", "#FBF2F0", "#FFFFFF"
MONO = {"family": "monospace"}

W = 12.44          # every figure is the same width: they sit on the same deck


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


def title(ax, s):
    txt(ax, W / 2, 0.50, s, size=19, weight="bold", color=INK)


def byline(ax, who):
    """Adam 09-16: name the operator who found it, by name -- never by role number."""
    txt(ax, 0.60, 0.50, f"FOUND BY  {who.upper()}", size=8.5, color=FAINT,
        weight="bold", ha="left", mono=True)


def save(fig, name):
    os.makedirs(HIRES, exist_ok=True)
    for ext, dpi in (("pdf", None), ("png", 300), ("svg", None)):
        fig.savefig(os.path.join(OUTDIR, f"{name}.{ext}"), facecolor=WHITE,
                    **({"dpi": dpi} if dpi else {}))
    fig.savefig(os.path.join(HIRES, f"{name}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"wrote {name}.{{pdf,png,svg}} + _hires/{name}.png")


# =========================================================================================
# ROLE-2 -- the machine is empty, and two instruments still will not say so.
# =========================================================================================
def fig_r2():
    H = 5.90
    fig, ax = canvas(W, H)
    title(ax, "The machine was empty. The twin was not.")
    byline(ax, "the restart cycler")

    top, bh = 1.30, 2.05
    lw_, gap = 4.90, 1.30
    lx, rx = 0.60, 0.60 + lw_ + gap

    # left: what was actually running
    box(ax, lx, top, lw_, bh, fill=WHITE, edge=INK, lw=1.0, radius=0.05)
    txt(ax, lx + lw_ / 2, top + 0.36, "ON THE MACHINE", size=8.5, color=FAINT,
        weight="bold", mono=True)
    for i, (k, v) in enumerate([("bmv2 switches", "0"), ("mininet processes", "0"),
                                ("topology session", "none")]):
        y = top + 0.86 + i * 0.42
        txt(ax, lx + 0.42, y, k, size=11.0, color=BODY, ha="left")
        txt(ax, lx + lw_ - 0.42, y, v, size=13.0, color=INK, weight="bold",
            ha="right", mono=True)

    # right: what the twin was serving
    box(ax, rx, top, lw_, bh, fill=ACCENT_BG, edge=ACCENT, lw=2.2, radius=0.05)
    txt(ax, rx + lw_ / 2, top + 0.36, "ON PORT 8000", size=8.5, color=ACCENT,
        weight="bold", mono=True)
    txt(ax, rx + lw_ / 2, top + 1.12, "14", size=30.0, color=ACCENT, weight="bold")
    txt(ax, rx + lw_ / 2, top + 1.72, "nodes, served on request", size=11.0, color=BODY)

    txt(ax, lx + lw_ + gap / 2, top + bh / 2, "vs", size=12.0, color=FAINT, weight="bold")

    # the two instruments
    iy = top + bh + 0.72
    txt(ax, 0.60, iy - 0.14, "AND THE TWO INSTRUMENTS THAT SHOULD HAVE CAUGHT IT",
        size=8.5, color=WARNC, weight="bold", ha="left", mono=True)
    for i, (name, said) in enumerate([("ndt status --check", "did not check"),
                                      ("orphans verdict", "CLEAN, no caveat")]):
        y = iy + 0.26 + i * 0.86
        box(ax, 0.60, y, W - 1.20, 0.70, fill=WARN_BG, edge=WARNC, lw=1.1, radius=0.05)
        txt(ax, 1.00, y + 0.35, name, size=11.0, color=INK, weight="bold",
            ha="left", mono=True)
        txt(ax, W - 1.00, y + 0.35, said, size=13.0, color=WARNC, weight="bold", ha="right")

    save(fig, "fig_r2_empty_but_confident")


# =========================================================================================
# ROLE-3 -- one field, two doors, opposite strictness.
# =========================================================================================
def fig_r3():
    H = 5.22
    fig, ax = canvas(W, H)
    title(ax, "One field. Two doors. Opposite answers.")
    byline(ax, "the grad student")

    # the field in the middle-left
    fx, fy, fw, fh = 0.60, 2.28, 3.30, 1.00
    box(ax, fx, fy, fw, fh, fill=PANEL, edge=INK, lw=1.0, radius=0.05)
    txt(ax, fx + fw / 2, fy + 0.30, "THE SAME FIELD", size=8.5, color=FAINT,
        weight="bold", mono=True)
    txt(ax, fx + fw / 2, fy + 0.68, 'vertex_type: 2', size=15.0, color=INK,
        weight="bold", mono=True)

    dx, dw, dh = 5.30, W - 5.30 - 0.60, 1.50
    ty, by = 1.26, 3.22

    # door 1: the file
    box(ax, dx, ty, dw, dh, fill=WARN_BG, edge=WARNC, lw=2.0, radius=0.05)
    txt(ax, dx + 0.34, ty + 0.36, "THROUGH THE TOPOLOGY FILE", size=8.5, color=WARNC,
        weight="bold", ha="left", mono=True)
    txt(ax, dx + 0.34, ty + 0.82, "accepted", size=16.0, color=WARNC,
        weight="bold", ha="left")
    txt(ax, dx + 0.34, ty + 1.20, "no diagnostic · enters the graph",
        size=11.0, color=BODY, ha="left")

    # door 2: the API
    box(ax, dx, by, dw, dh, fill=ACCENT_BG, edge=ACCENT, lw=2.0, radius=0.05)
    txt(ax, dx + 0.34, by + 0.36, "THROUGH THE API", size=8.5, color=ACCENT,
        weight="bold", ha="left", mono=True)
    txt(ax, dx + 0.34, by + 0.82, "400", size=16.0, color=ACCENT,
        weight="bold", ha="left", mono=True)
    txt(ax, dx + 0.34, by + 1.20, "refused", size=11.0, color=BODY, ha="left")

    arrow(ax, fx + fw + 0.10, fy + 0.34, dx - 0.10, ty + dh / 2, color=WARNC, lw=1.4)
    arrow(ax, fx + fw + 0.10, fy + 0.68, dx - 0.10, by + dh / 2, color=ACCENT, lw=1.4)

    # the other two values the same door let through
    ny = fy + fh + 0.52
    txt(ax, fx, ny, "the same door also took", size=8.5, color=FAINT,
        weight="bold", ha="left", mono=True)
    for i, v in enumerate(["-1", "99", '["10.1"]']):
        bx = fx + i * 1.12
        box(ax, bx, ny + 0.22, 0.98, 0.52, fill=WHITE, edge=RULE, lw=1.0, radius=0.04)
        txt(ax, bx + 0.49, ny + 0.48, v, size=11.0, color=MUTED, weight="bold", mono=True)
    txt(ax, fx, ny + 1.06,
        'and ["10.1"] gave two hosts one address', size=10.0, color=WARNC,
        weight="bold", ha="left")

    save(fig, "fig_r3_two_doors_one_field")


# =========================================================================================
# ROLE-4 -- the claim race: the window is about 50 ms wide.
# =========================================================================================
def fig_r4():
    H = 5.92
    fig, ax = canvas(W, H)
    title(ax, "Two people, one lab, both told yes")
    byline(ax, "the second operator")

    ax_y = 3.30
    x0, x1 = 1.40, W - 1.20
    ax.plot([x0, x1], [ax_y, ax_y], color=INK, lw=1.2, zorder=3)
    # below the tick labels, not beside them: at +0.40 it sat on top of "100 ms"
    txt(ax, x1, ax_y + 1.00, "gap between the two claims", size=10.0,
        color=FAINT, ha="right")

    marks = [(0.00, "same\nmillisecond"), (0.34, "10 ms"), (0.62, "50 ms"), (0.92, "100 ms")]
    for f, lab in marks:
        x = x0 + f * (x1 - x0)
        ax.plot([x, x], [ax_y - 0.10, ax_y + 0.10], color=INK, lw=1.2, zorder=4)
        txt(ax, x, ax_y + 0.30, lab, size=9.5, color=MUTED, va="top")

    # the race region
    xr = x0 + 0.48 * (x1 - x0)
    box(ax, x0 - 0.16, ax_y - 1.72, xr - x0 + 0.16, 1.52,
        fill=WARN_BG, edge=WARNC, lw=1.6, radius=0.05)
    txt(ax, (x0 + xr) / 2 - 0.08, ax_y - 1.42, "BOTH GRANTED", size=9.0, color=WARNC,
        weight="bold", mono=True)
    txt(ax, (x0 + xr) / 2 - 0.08, ax_y - 0.96, "2 of 16", size=17.0, color=WARNC,
        weight="bold")
    txt(ax, (x0 + xr) / 2 - 0.08, ax_y - 0.52,
        'both replies said "ok lab claimed by <me>"', size=10.0, color=BODY)

    # the safe region
    box(ax, xr + 0.16, ax_y - 1.72, x1 - xr - 0.16 + 0.16, 1.52,
        fill=ACCENT_BG, edge=ACCENT, lw=1.6, radius=0.05)
    txt(ax, (xr + x1) / 2 + 0.16, ax_y - 1.42, "CORRECTLY REFUSED", size=9.0,
        color=ACCENT, weight="bold", mono=True)
    txt(ax, (xr + x1) / 2 + 0.16, ax_y - 0.96, "0 of 9", size=17.0, color=ACCENT,
        weight="bold")
    txt(ax, (xr + x1) / 2 + 0.16, ax_y - 0.52, "the second one is turned away",
        size=10.0, color=BODY)

    # the mechanism, one line
    my = ax_y + 1.34
    box(ax, 1.40, my, x1 - 1.40, 0.82, fill=WHITE, edge=INK, lw=1.0, radius=0.05)
    txt(ax, 1.74, my + 0.28, "WHY", size=8.5, color=FAINT, weight="bold",
        ha="left", mono=True)
    txt(ax, 1.74, my + 0.57,
        "the claim is read, then written — there is no lock between the two",
        size=12.0, color=INK, weight="bold", ha="left")
    txt(ax, 0.60, ax_y - 0.96, "file keeps\nonly the last\nwriter", size=10.0,
        color=WARNC, weight="bold")

    save(fig, "fig_r4_claim_race_window")


# =========================================================================================
# ROLE-12 -- two live teardowns, one marker, and whoever finishes first deletes it.
# =========================================================================================
def fig_r12():
    H = 5.68
    fig, ax = canvas(W, H)
    title(ax, "Two teardowns, one marker, no owner")
    byline(ax, "the second operator")

    lx, rx = 2.70, W - 0.70
    rows = [
        ("teardown A", 1.34, [("starts", 0.00), ("writes the marker", 0.14),
                              ("finishes first", 0.62)]),
        ("teardown B", 2.38, [("starts", 0.22), ("overwrites it", 0.34),
                              ("still running", 0.86)]),
    ]
    for name, y, events in rows:
        txt(ax, 0.66, y + 0.16, name, size=12.0, color=INK, weight="bold", ha="left")
        ax.plot([lx, rx], [y + 0.16, y + 0.16], color=RULE, lw=1.2, zorder=2)
        for lab, f in events:
            x = lx + f * (rx - lx)
            ax.plot([x], [y + 0.16], marker="o", ms=7, color=ACCENT, zorder=5)
            txt(ax, x, y - 0.18, lab, size=9.5, color=BODY)

    # the marker's life
    my = 3.26
    txt(ax, 0.66, my + 0.30, "the marker", size=12.0, color=WARNC,
        weight="bold", ha="left")
    xa = lx + 0.14 * (rx - lx)
    xb = lx + 0.34 * (rx - lx)
    xd = lx + 0.62 * (rx - lx)
    box(ax, xa, my + 0.04, xb - xa, 0.52, fill=PANEL, edge=RULE, lw=1.0, radius=0.04)
    txt(ax, (xa + xb) / 2, my + 0.30, "A's", size=10.0, color=MUTED, mono=True)
    box(ax, xb, my + 0.04, xd - xb, 0.52, fill=WARN_BG, edge=WARNC, lw=1.4, radius=0.04)
    txt(ax, (xb + xd) / 2, my + 0.30, "B's (A's is gone)", size=10.0,
        color=WARNC, weight="bold")
    ax.plot([xd, xd], [my - 0.06, my + 0.66], color=WARNC, lw=2.0, zorder=6)
    txt(ax, xd + 0.14, my + 0.30, "A deletes it — B is still running",
        size=10.5, color=WARNC, weight="bold", ha="left")

    # the consequence
    cy = 4.32
    box(ax, 0.66, cy, W - 1.32, 1.00, fill=WHITE, edge=INK, lw=1.6, radius=0.05)
    txt(ax, 1.04, cy + 0.32, "AND THEN", size=8.5, color=FAINT, weight="bold",
        ha="left", mono=True)
    txt(ax, 1.04, cy + 0.68,
        "with the marker gone, a new bring-up is not refused — it runs to the last step",
        size=13.0, color=INK, weight="bold", ha="left")
    txt(ax, W - 1.04, cy + 0.68, "missed by seconds", size=11.0,
        color=WARNC, weight="bold", ha="right")

    save(fig, "fig_r12_stolen_marker")


# =========================================================================================
# ROLE-10 -- the same cut, three verdicts, depending on which second you sampled.
# =========================================================================================
def fig_r10():
    """Three verdicts side by side UNDER the axis.  The first cut put 3.1-inch boxes at 4 s
    and 5 s on an 8 s axis: they overlapped each other and the title.  Fixed positions and a
    leader line to each sample instead."""
    H = 6.30
    fig, ax = canvas(W, H)
    title(ax, "Same cut. Three verdicts. Eight seconds.")
    byline(ax, "the traffic pusher")

    ax_y = 1.62
    x0, x1 = 1.10, W - 0.90
    ax.plot([x0, x1], [ax_y, ax_y], color=INK, lw=1.2, zorder=3)
    for s in range(0, 9):
        x = x0 + (s / 8.0) * (x1 - x0)
        ax.plot([x, x], [ax_y - 0.09, ax_y + 0.09], color=INK, lw=1.0, zorder=4)
        txt(ax, x, ax_y - 0.36, f"{s}s", size=9.0, color=MUTED)

    samples = [
        (0.8, 0.66, "BEFORE THE WINDOW", "nothing printed", "rc 0", MUTED, PANEL, RULE),
        (4.0, 4.56, "+3 s", "1.32  ok", "rc 0", ACCENT, ACCENT_BG, ACCENT),
        (5.0, 8.46, "+1 s LATER", "2.51  DOUBLE-COUNTING", "rc 4", WARNC, WARN_BG, WARNC),
    ]
    bw, bh, by = 3.32, 1.42, 2.42
    for s, bx, when, said, rc, col, fillc, edgec in samples:
        x = x0 + (s / 8.0) * (x1 - x0)
        ax.plot([x], [ax_y], marker="o", ms=10, color=col, zorder=6)
        box(ax, bx, by, bw, bh, fill=fillc, edge=edgec, lw=1.5, radius=0.05)
        txt(ax, bx + bw / 2, by + 0.30, when, size=8.5, color=col, weight="bold", mono=True)
        txt(ax, bx + bw / 2, by + 0.76, said, size=12.5, color=col, weight="bold", mono=True)
        txt(ax, bx + bw / 2, by + 1.16, rc, size=10.5, color=BODY, mono=True)
        ax.plot([x, bx + bw / 2], [ax_y + 0.12, by - 0.04], color=edgec, lw=1.0,
                ls=(0, (2.0, 1.6)), zorder=3)

    # the other half of the finding: scale made no difference at all
    sy = 4.36
    box(ax, 0.66, sy, W - 1.32, 1.52, fill=WHITE, edge=INK, lw=1.0, radius=0.05)
    txt(ax, 1.04, sy + 0.30, "AND THE SCALE AXIS DID NOT EXIST", size=8.5,
        color=FAINT, weight="bold", ha="left", mono=True)
    for i, (k, v) in enumerate([("4 hosts", "10 switches · 16 links"),
                                ("128 hosts", "10 switches · 16 links")]):
        cx = 2.30 + i * 3.30
        txt(ax, cx, sy + 0.76, k, size=13.0, color=INK, weight="bold")
        txt(ax, cx, sy + 1.16, v, size=11.0, color=BODY)
    txt(ax, 3.95, sy + 0.94, "=", size=18.0, color=FAINT, weight="bold")
    ax.plot([7.40, 7.40], [sy + 0.20, sy + 1.32], color=RULE, lw=0.9)
    txt(ax, 7.74, sy + 0.76, "the 248 extra edges are host-facing",
        size=11.5, color=BODY, ha="left")
    txt(ax, 7.74, sy + 1.16, "and every one is excluded",
        size=11.5, color=WARNC, ha="left", weight="bold")

    save(fig, "fig_r10_sampling_instant")


if __name__ == "__main__":
    fig_r2()
    fig_r3()
    fig_r4()
    fig_r12()
    fig_r10()
