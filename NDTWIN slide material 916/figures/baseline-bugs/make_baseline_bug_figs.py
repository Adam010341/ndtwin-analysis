#!/usr/bin/env python3
"""
make_baseline_bug_figs.py -- one figure per baseline defect, for the ranks Adam picked 09-16.

    fig_b02_loss_ladder          rank 2   #53          telemetry lies harder as load rises
    fig_b04_poll_resurrects      rank 4   #46/#36      the poll undoes a power-off command
    fig_b07_nothing_goes_down    rank 7   F-14/16/4    a dead switch leaves its hosts up
    fig_b08_delete_reports_gone  rank 8   #1/A-10      delete says gone, the group is there
    fig_b09_ghost_rule           rank 9   #2/C-4       the table answers 13 s before the switch
    fig_b10_accidentally_right   rank 10  F-8          272 edges right by coincidence
    fig_b11_counter_cover        rank 11  A-7          a count that now says what it counts
    fig_b_topology_doors         the topology JSON file as a whole: every door, before / after

All of these are FIRST-LAYER baseline defects (files first committed 2025-12-15), unlike the
role figures in ../overnight-hunt/, four of which are our own ndt tooling.  Keep the two
sections of the deck apart (REPORT-PICK-FIXED.md section 0.3).

Numbers come from doc/audit/2026-09-02_fix-design-campaign/findings/*.md,
doc/audit/2026-09-03_night-rounds/FINDINGS-ALL.md, and REPORT-PICK-FIXED.md; cited per figure
in the companion .md.  Literals only, so the output is byte-stable.

One phrase, one colour (Adam 09-16): a sentence that wraps is never two colours.

[Co-developed with claude code -- Adam]

Regenerate:
    "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_baseline_bug_figs.py
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
W = 12.44
_BANDS = []


def canvas(h):
    _BANDS.clear()
    fig = plt.figure(figsize=(W, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(h, 0)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fill=WHITE, edge=INK, lw=1.0, ls="solid", z=2, radius=0.05):
    if radius:
        p = FancyBboxPatch((x + radius, y + radius), w - 2 * radius, h - 2 * radius,
                           boxstyle=f"round,pad={radius},rounding_size={radius}",
                           facecolor=fill, edgecolor=edge, linewidth=lw, linestyle=ls, zorder=z)
    else:
        p = Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge,
                      linewidth=lw, linestyle=ls, zorder=z)
    ax.add_patch(p)
    return p


def txt(ax, x, y, s, size=10.5, color=INK, weight="normal", ha="center", va="center",
        mono=False, z=5):
    kw = dict(MONO) if mono else {}
    return ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=z, **kw)


def arrow(ax, x1, y1, x2, y2, color=INK, lw=1.0, ls="-", head=0.09, z=3):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), zorder=z,
                arrowprops=dict(arrowstyle=f"-|>,head_width={head*1.6},head_length={head*2.4}",
                                color=color, linewidth=lw, linestyle=ls,
                                shrinkA=0, shrinkB=0, joinstyle="miter"))


def head(ax, title_s, found_by=None, rank=None):
    txt(ax, W / 2, 0.50, title_s, size=19, weight="bold", color=INK)
    if rank:
        txt(ax, 0.58, 0.50, rank, size=8.5, color=FAINT, weight="bold", ha="left", mono=True)
    if found_by:
        txt(ax, W - 0.58, 0.50, found_by, size=9.5, color=ACCENT, weight="bold", ha="right")


def band(ax, y, kicker, text, h=0.80, fill=WARN_BG, edge=WARNC, kc=WARNC, tc=INK, x0=0.58):
    """A kicker on the left, the sentence to its right.

    The body x is derived from the kicker's own width -- a fixed 2.30 put the body on top of
    "THE NUMBER WAS READ, JUST NOT USED" (caught on the rendered PNG, 09-16).  Mono at 8.5 pt
    is about 0.0708 in per character.
    """
    for prev_y, prev_h in _BANDS:
        assert y >= prev_y + prev_h or y + h <= prev_y, \
            f"band at {y} overlaps the one at {prev_y} (height {prev_h})"
    _BANDS.append((y, h))
    box(ax, x0, y, W - 2 * x0, h, fill=fill, edge=edge, lw=1.2)
    txt(ax, x0 + 0.36, y + h / 2, kicker, size=8.5, color=kc, weight="bold",
        ha="left", mono=True)
    bodyx = max(x0 + 2.30, x0 + 0.36 + len(kicker) * 0.0708 + 0.34)
    txt(ax, bodyx, y + h / 2, text, size=12.0, color=tc, weight="bold", ha="left")


def save(fig, name):
    os.makedirs(HIRES, exist_ok=True)
    for ext, dpi in (("pdf", None), ("png", 300), ("svg", None)):
        fig.savefig(os.path.join(OUTDIR, f"{name}.{ext}"), facecolor=WHITE,
                    **({"dpi": dpi} if dpi else {}))
    fig.savefig(os.path.join(HIRES, f"{name}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"wrote {name}")


# =========================================================================================
# rank 2 -- #53.  A load ladder: loss climbs, every reply still says success.
# =========================================================================================
def fig_b02():
    fig, ax = canvas(6.48)
    head(ax, "The telemetry lied harder as the load rose", rank="RANK 2  ·  #53")

    rungs = [("2 000/s", 0.0, "0"), ("20 000/s", 0.0, "0"), ("60 000/s", 0.0, "0"),
             ("150 000/s", 0.34, "0.34%"), ("654 709/s", 72.5, "72.5%")]
    bx0, bw, gap = 0.72, 2.06, 0.26
    base, maxh = 3.46, 1.86
    for i, (lab, pct, show) in enumerate(rungs):
        x = bx0 + i * (bw + gap)
        h = max(pct / 72.5 * maxh, 0.035)
        heavy = pct > 0
        box(ax, x, base - h, bw, h, fill=WARN_BG if heavy else PANEL,
            edge=WARNC if heavy else RULE, lw=1.6 if heavy else 1.0, radius=0.03)
        txt(ax, x + bw / 2, base - h - 0.26, show, size=13.0,
            color=WARNC if heavy else MUTED, weight="bold")
        txt(ax, x + bw / 2, base + 0.30, lab, size=11.0, color=BODY, mono=True)
    ax.plot([0.58, W - 0.58], [base, base], color=INK, lw=1.2, zorder=4)
    # the caption sat at base+0.72 and touched the first band's border
    txt(ax, 0.58, base + 0.72, "samples the network offered, per second",
        size=10.0, color=FAINT, ha="left")
    txt(ax, 0.58, 1.18, "share of them dropped", size=10.0, color=FAINT, ha="left")

    band(ax, 4.62, "AT EVERY RUNG", "every endpoint answered success — "
                                    "and four drop counters existed that no API could read")
    band(ax, 5.50, "AFTER THE FIX",
         "status · loss_fraction · the numerator and the denominator, on the wire",
         fill=ACCENT_BG, edge=ACCENT, kc=ACCENT)
    assert 5.50 >= 4.62 + 0.80, "the two bands overlap"
    save(fig, "fig_b02_loss_ladder")


# =========================================================================================
# rank 4 -- #46/#36.  The poll undoes the command.
# =========================================================================================
def fig_b04():
    fig, ax = canvas(5.36)
    head(ax, "You switched it off. The poll switched it back.", rank="RANK 4  ·  #46 / #36")

    ay = 2.72
    x0, x1 = 1.30, W - 1.00
    ax.plot([x0, x1], [ay, ay], color=INK, lw=1.2, zorder=3)
    for f, lab in [(0.0, "you command it off"), (0.30, "3.08 s later"),
                   (1.0, "the 30 s poll keeps running")]:
        x = x0 + f * (x1 - x0)
        ax.plot([x, x], [ay - 0.10, ay + 0.10], color=INK, lw=1.2, zorder=4)
        txt(ax, x, ay + 0.36, lab, size=10.0, color=MUTED)

    box(ax, 0.72, 1.10, 4.10, 1.18, fill=PANEL, edge=RULE, lw=1.0)
    txt(ax, 2.77, 1.44, "THE SWITCH", size=8.5, color=FAINT, weight="bold", mono=True)
    txt(ax, 2.77, 1.88, "off, and it stays off", size=13.0, color=BODY)

    box(ax, 5.50, 1.10, 6.22, 1.18, fill=WARN_BG, edge=WARNC, lw=1.8)
    txt(ax, 8.61, 1.44, "WHAT THE TWIN SAYS", size=8.5, color=WARNC, weight="bold", mono=True)
    txt(ax, 8.61, 1.88, "up", size=15.0, color=WARNC, weight="bold")
    arrow(ax, 4.90, 1.69, 5.42, 1.69, color=WARNC, lw=1.4)

    band(ax, 3.42, "HOW OFTEN", "2 runs out of 9 — the poll wrote is_up back to true")
    band(ax, 4.36, "WHY IT MATTERS",
         "the power command is the only way back, and it reads the flag the poll just overwrote",
         fill=PANEL, edge=RULE, kc=FAINT, tc=BODY)
    save(fig, "fig_b04_poll_resurrects")


# =========================================================================================
# rank 7 -- F-14 / F-16 / F-4.  One switch dies; almost nothing goes down with it.
# =========================================================================================
def fig_b07():
    fig, ax = canvas(5.62)
    head(ax, "A switch died. Almost nothing died with it.", rank="RANK 7  ·  F-14 / F-16 / F-4")

    sx, sy = 5.52, 1.26
    box(ax, sx, sy, 1.40, 0.92, fill=WARN_BG, edge=WARNC, lw=2.0)
    txt(ax, sx + 0.70, sy + 0.30, "SWITCH", size=8.0, color=WARNC, weight="bold", mono=True)
    txt(ax, sx + 0.70, sy + 0.66, "dead", size=13.0, color=WARNC, weight="bold")

    rows = [("the edges to other switches", "marked down", True),
            ("the edges facing its hosts", "still up", False),
            ("the hosts themselves", "still up", False),
            ("a dead link, next poll", "brought back up", False)]
    ry = 2.54
    for i, (what, said, ok) in enumerate(rows):
        y = ry + i * 0.66
        box(ax, 0.58, y, W - 1.16, 0.56,
            fill=PANEL if ok else WARN_BG, edge=RULE if ok else WARNC,
            lw=1.0 if ok else 1.4)
        txt(ax, 1.00, y + 0.28, what, size=11.5, color=BODY, ha="left")
        txt(ax, W - 1.00, y + 0.28, said, size=12.5,
            color=MUTED if ok else WARNC, weight="bold", ha="right")
    txt(ax, 0.58, 5.34, "one switch, four questions, and only the first was answered honestly",
        size=10.5, color=FAINT, ha="left")
    save(fig, "fig_b07_nothing_goes_down")


# =========================================================================================
# rank 8 -- #1 / A-10.  Delete says gone; the group is still there.
# =========================================================================================
def fig_b08():
    fig, ax = canvas(5.14)
    head(ax, "Deleted, it said. The group was still there.", rank="RANK 8  ·  #1 / A-10")

    # 09-16 correction: the first cut said "OVS refuses -- you may not send buckets" and "Ryu
    # returns no error".  Both were invented.  The fix commit d599c476 states the mechanism:
    # the delete was forwarded with the caller's INSTALL-SHAPED body, and OVS rejects it
    # ASYNCHRONOUSLY (OFPGMFC_INVALID_GROUP) -- after Ryu has already answered 200.
    # The answer was given before the refusal existed.
    steps = [("the kernel", "forwards the delete with\nthe caller's install-shaped body"),
             ("Ryu", "answers 200\nstraight away"),
             ("OVS", "rejects it later, asynchronously\nOFPGMFC_INVALID_GROUP"),
             ("the kernel", "has already replied\n200 deleted")]
    x0, gap = 0.62, 0.30
    bw = (W - 2 * x0 - (len(steps) - 1) * gap) / len(steps)
    top, bh = 1.12, 1.62
    for i, (who, what) in enumerate(steps):
        x = x0 + i * (bw + gap)
        last = i == len(steps) - 1
        box(ax, x, top, bw, bh, fill=WARN_BG if last else WHITE,
            edge=WARNC if last else INK, lw=1.8 if last else 1.0)
        txt(ax, x + bw / 2, top + 0.34, who.upper(), size=8.0,
            color=WARNC if last else FAINT, weight="bold", mono=True)
        txt(ax, x + bw / 2, top + 1.02, what, size=9.5,
            color=WARNC if last else BODY, weight="bold" if last else "normal")
        if not last:
            arrow(ax, x + bw + 0.03, top + bh / 2, x + bw + gap - 0.03, top + bh / 2, lw=1.2)

    band(ax, 3.04, "READ IT BACK",
         "the group is still there, and its id stays unusable until the switch restarts")
    band(ax, 3.98, "THE FIX",
         "deleted is claimed only after a read-back finds the entry absent",
         fill=ACCENT_BG, edge=ACCENT, kc=ACCENT)
    save(fig, "fig_b08_delete_reports_gone")


# =========================================================================================
# rank 9 -- #2 / C-4.  The table answers before the switch has the rule.
# =========================================================================================
def fig_b09():
    fig, ax = canvas(4.94)
    head(ax, "The table had the rule 13 seconds early", rank="RANK 9  ·  #2 / C-4")

    ay = 2.56
    x0, x1 = 1.10, W - 0.80
    ax.plot([x0, x1], [ay, ay], color=INK, lw=1.2, zorder=3)
    pts = [(0.0, "install", MUTED), (0.02, "0.257 s", WARNC), (1.0, "13.4 s", ACCENT)]
    for f, lab, col in pts:
        x = x0 + f * (x1 - x0)
        ax.plot([x], [ay], marker="o", ms=10, color=col, zorder=6)
        txt(ax, x, ay + 0.36, lab, size=11.0, color=col, weight="bold", mono=True)

    box(ax, 0.80, 1.06, 5.30, 1.14, fill=WARN_BG, edge=WARNC, lw=1.8)
    txt(ax, 3.45, 1.38, "WHAT THE FLOW TABLE SHOWED", size=8.5, color=WARNC,
        weight="bold", mono=True)
    txt(ax, 3.45, 1.82, "the rule, from the cache", size=12.5, color=WARNC, weight="bold")

    box(ax, 6.60, 1.06, 5.04, 1.14, fill=ACCENT_BG, edge=ACCENT, lw=1.8)
    txt(ax, 9.12, 1.38, "WHEN THE SWITCH ACTUALLY HAD IT", size=8.5, color=ACCENT,
        weight="bold", mono=True)
    txt(ax, 9.12, 1.82, "13.4 s after the install", size=12.5, color=ACCENT, weight="bold")

    band(ax, 3.20, "IN BETWEEN",
         "for 13 seconds the twin answered from a queue and called it the network")
    band(ax, 4.06, "THE FIX",
         "an entry is confirmed only by a decisive success on the southbound path",
         fill=ACCENT_BG, edge=ACCENT, kc=ACCENT)
    save(fig, "fig_b09_ghost_rule")


# =========================================================================================
# rank 10 -- F-8.  272 of 288 edges were right by coincidence.
# =========================================================================================
def fig_b10():
    fig, ax = canvas(6.18)
    head(ax, "272 edges were right by coincidence", rank="RANK 10  ·  F-8")

    txt(ax, 0.58, 1.14, "EVERY EDGE REPORTS A CAPACITY OF 1 Gbit/s — "
                        "IT IS THE FIELD'S INITIAL VALUE, NEVER OVERWRITTEN",
        size=8.5, color=FAINT, weight="bold", ha="left", mono=True)

    groups = [("272 edges", "declare 1 Gbit/s", "right — because the initial value\n"
                                                "happens to equal the declared one", PANEL, RULE, MUTED),
              ("16 edges", "declare 10 Gbit/s", "wrong by 9 Gbit/s each —\n"
                                                "one tenth of the headroom reported",
               WARN_BG, WARNC, WARNC)]
    gy, gh = 1.46, 1.74
    for i, (n, decl, verdict, fillc, edgec, col) in enumerate(groups):
        x = 0.58 + i * (W / 2 - 0.40)
        bw = W / 2 - 0.76
        box(ax, x, gy, bw, gh, fill=fillc, edge=edgec, lw=2.0 if i else 1.0)
        txt(ax, x + bw / 2, gy + 0.42, n, size=20.0, color=col, weight="bold")
        txt(ax, x + bw / 2, gy + 0.86, decl, size=12.0, color=BODY, mono=True)
        txt(ax, x + bw / 2, gy + 1.36, verdict, size=10.5, color=col)

    band(ax, 3.46, "AND THE POINT",
         "nothing in the response tells the 16 apart from the 272")
    band(ax, 4.34, "READ FROM THE FILE, JUST NOT USED",
         "the declared capacity was loaded from the file and written to the neighbouring field",
         fill=PANEL, edge=RULE, kc=FAINT, tc=BODY)
    band(ax, 5.22, "THE FIX",
         "report the declared capacity, and add a field saying where the number came from",
         h=0.72, fill=ACCENT_BG, edge=ACCENT, kc=ACCENT)
    save(fig, "fig_b10_accidentally_right")


# =========================================================================================
# rank 11 -- A-7.  How it was fixed: publish the denominator, refuse to invent a counter.
# =========================================================================================
def fig_b11():
    fig, ax = canvas(6.04)
    head(ax, "A count that now says what it counts", rank="RANK 11  ·  A-7")

    cy, ch = 1.14, 2.06
    bw = (W - 1.16 - 0.34) / 2
    box(ax, 0.58, cy, bw, ch, fill=WARN_BG, edge=WARNC, lw=1.8)
    txt(ax, 0.58 + bw / 2, cy + 0.36, "BEFORE", size=8.5, color=WARNC,
        weight="bold", mono=True)
    txt(ax, 0.58 + bw / 2, cy + 0.88, "succeeded: N", size=15.0, color=WARNC,
        weight="bold", mono=True)
    txt(ax, 0.58 + bw / 2, cy + 1.42, "a queued write that failed\n"
                                      "appears in no API at all", size=11.5, color=BODY)

    rx = 0.58 + bw + 0.34
    box(ax, rx, cy, bw, ch, fill=ACCENT_BG, edge=ACCENT, lw=1.8)
    txt(ax, rx + bw / 2, cy + 0.36, "AFTER", size=8.5, color=ACCENT, weight="bold", mono=True)
    for i, line in enumerate(["dispatcher_running: true",
                              "counters_cover: the four dispatch routes",
                              "includes_boot_time_programming: false",
                              "includes_intent_translator: false"]):
        # four fields of the same reply: one colour.  Emphasis is weight, not hue.
        txt(ax, rx + 0.34, cy + 0.80 + i * 0.34, line, size=10.5,
            color=ACCENT, weight="bold" if i == 0 else "normal",
            ha="left", mono=True)

    band(ax, 3.46, "WHAT THAT BUYS",
         "running true with zero drops is health; running false with zero drops is "
         "delivery already over",
         fill=PANEL, edge=RULE, kc=FAINT, tc=BODY)
    band(ax, 4.34, "AND WHAT WAS REFUSED",
         "counters for the boot-time installs — they would have been pinned at zero forever")
    txt(ax, 0.58, 5.62, "a counter that can never move is worse than no counter",
        size=12.0, color=INK, weight="bold", ha="left")
    save(fig, "fig_b11_counter_cover")


# =========================================================================================
# The topology JSON file as a whole: every door, before and after.
# =========================================================================================
DOORS = [
    ("an edge pointing at a node that is not there", "#61 / #62"),
    ("a port or interface number out of range", "#61 / #62"),
    ("a switch with an empty address", "#89 / W3"),
    ("a missing bridge_name", "#89 / W3"),
    ("a host declared with no address at all", "B-11"),
    ("a brand_name this build cannot drive", "B-12"),
    ("a vertex_type outside the range", "B-14"),
    ("a link bandwidth of 0, or of -1", "B-13"),
    ("a loose address that two hosts then share", "B-15"),
    ("switches from two different data planes", "BUG-17"),
    ("a topology with no switch in it", "E-26"),
]


def fig_doors():
    # 11 rows at 0.482 plus two bands ran off a 7.30 canvas (caught on the PNG, 09-16).
    # Tighter rows, and the two bands merged into one two-line band.
    fig, ax = canvas(7.34)
    head(ax, "One file. Eleven doors. All of them open.")
    txt(ax, W / 2, 0.92, "what the topology file could contain, and what the loader checked",
        size=11.5, color=FAINT)

    rh, top = 0.40, 1.34
    txt(ax, 7.90, top - 0.22, "BEFORE", size=9.0, color=WARNC, weight="bold", mono=True)
    txt(ax, 10.40, top - 0.22, "NOW", size=9.0, color=ACCENT, weight="bold", mono=True)
    for i, (what, code) in enumerate(DOORS):
        y = top + i * rh
        if i % 2 == 0:
            box(ax, 0.58, y, W - 1.16, rh, fill=PANEL, edge="none", lw=0, z=1, radius=0)
        txt(ax, 0.90, y + rh / 2, what, size=11.5, color=BODY, ha="left")
        txt(ax, 7.00, y + rh / 2, code, size=9.0, color=FAINT, ha="right", mono=True)
        txt(ax, 7.90, y + rh / 2, "taken in silence", size=11.0, color=WARNC, weight="bold")
        txt(ax, 10.40, y + rh / 2, "refused", size=11.0, color=ACCENT, weight="bold")

    fy = top + len(DOORS) * rh + 0.30
    bh = 1.14
    box(ax, 0.58, fy, W - 1.16, bh, fill=WARN_BG, edge=WARNC, lw=1.2)
    txt(ax, 0.94, fy + 0.36, "THE SHAPE", size=8.5, color=WARNC, weight="bold",
        ha="left", mono=True)
    txt(ax, 2.88, fy + 0.36,
        "the same value is refused when it arrives by API, and taken when it arrives by file",
        size=12.0, color=INK, weight="bold", ha="left")
    txt(ax, 0.94, fy + 0.80, "AND NOW", size=8.5, color=ACCENT, weight="bold",
        ha="left", mono=True)
    txt(ax, 2.88, fy + 0.80,
        "the whole file is validated before the first vertex enters the graph",
        size=12.0, color=ACCENT, weight="bold", ha="left")
    assert fy + bh < 7.34, f"the band ends at {fy + bh:.2f}, past the canvas"
    save(fig, "fig_b_topology_doors")


if __name__ == "__main__":
    assert len(DOORS) == 11, f"the title says eleven doors, the list has {len(DOORS)}"
    for f in (fig_b02, fig_b04, fig_b07, fig_b08, fig_b09, fig_b10, fig_b11, fig_doors):
        f()
