#!/usr/bin/env python3
"""
make_p04_rules_lost.py -- p4/fig_p04_rules_lost: how the rule-loss notice reaches the app. Page P04 of the 1028
deck. Evidence class: READ (code and docs of the PR tree, not executed).

Four lanes (App, NDTwin kernel, P4 proxy, bmv2 switch) and six numbered steps left to right, all read from
figures_spec/rules_lost_flow.txt: the lane labels, each step's lane, column, title and second line, the arrows
and their annotations. A step whose spec row ends in "| dashed" is drawn dashed (NDTwin
does not do it, or no shipped app does it yet); an arrow likewise. Boxes in NDTwin's own components are
blue, the switch and the app grey, as on the 1014 architecture figure.

Stops with a named reason if: the spec's canvas title differs from the one drawn; a section is missing; a step
names a lane the spec does not list or a column outside 1-5; a step has no evidence line; two steps share a
lane and column; an arrow names a step that is not drawn; S1-S6 are not exactly the steps listed; a label line is
longer than 30 chars or its rendered text sticks out of its box (or a lane label into column 1).

[Co-developed with claude code -- Adam]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle_1028 as S  # noqa: E402
from figstyle_1028 import (ACCENT, INK, MUTED, WHITE, REPO_FILL, REPO_EDGE, SEP_FILL, SEP_EDGE,  # noqa: E402
                           PANEL, RULE)
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle  # noqa: E402
from matplotlib.path import Path  # noqa: E402
from matplotlib.patches import PathPatch  # noqa: E402

WHO = "make_p04_rules_lost"
STEM = "fig_p04_rules_lost"
TITLE = "How the rule-loss notice reaches the app"
STEP_IDS = ["S1", "S2", "S3", "S4", "S5", "S6"]
LANE_IDS = ["app", "kernel", "proxy", "switch"]
NDTWIN_LANES = {"kernel", "proxy"}
MAX_LINE = 30
args = sys.argv[1:]


def opt(name, default):
    return args[args.index(name) + 1] if name in args else default


SPEC = opt("--spec", os.path.join(S.DECK, "figures_spec", "rules_lost_flow.txt"))
OUTDIR = opt("--out", os.path.join(S.DECK, "figures", "p4"))


def read():
    text, sec = S.read_spec(WHO, SPEC, TITLE)
    lanes = {}
    for r in S.need_section(WHO, sec, "LANES", SPEC):
        if len(r["fields"]) != 2:
            S.die(WHO, f"LANES row {r['fields']} is not 'id | label'")
        lanes[r["fields"][0]] = r["fields"][1]
    if list(lanes) != LANE_IDS:
        S.die(WHO, f"LANES are {list(lanes)}, the figure draws {LANE_IDS}")
    steps, seen = {}, set()
    for r in S.need_section(WHO, sec, "STEPS", SPEC):
        f = r["fields"]
        if len(f) not in (5, 6) or (len(f) == 6 and f[5] != "dashed"):
            S.die(WHO, f"STEPS row {f} is not 'id | lane | column | title | second line [| dashed]'")
        sid, lane, col, t1, t2 = f[:5]
        if lane not in lanes:
            S.die(WHO, f"step {sid} names lane {lane!r}, which LANES does not list")
        if not col.isdigit() or not 1 <= int(col) <= 5:
            S.die(WHO, f"step {sid} column {col!r} is not 1-5")
        if not r["evidence"]:
            S.die(WHO, f"step {sid} has no evidence line")
        if (lane, col) in seen:
            S.die(WHO, f"step {sid} shares lane {lane} and column {col} with another step")
        seen.add((lane, col))
        for line in (t1, t2):
            if not line or len(line) > MAX_LINE:
                S.die(WHO, f"step {sid} label line {line!r} is empty or longer than {MAX_LINE} chars")
        steps[sid] = {"lane": lane, "col": int(col), "t1": t1, "t2": t2, "ev": r["evidence"],
                      "dashed": len(f) == 6}
    if list(steps) != STEP_IDS:
        S.die(WHO, f"STEPS are {list(steps)}, the figure draws {STEP_IDS}")
    arrows = []
    for r in S.need_section(WHO, sec, "ARROWS", SPEC):
        f = r["fields"]
        ends = [x.strip() for x in f[0].split("->")]
        if len(ends) != 2:
            S.die(WHO, f"ARROWS row {f} has no 'from -> to'")
        for e in ends:
            if e not in steps:
                S.die(WHO, f"arrow {f[0]} names {e}, which is not a drawn step")
        ann = f[1] if len(f) > 1 and f[1] != "-" else None
        arrows.append({"a": ends[0], "b": ends[1], "ann": ann, "dashed": len(f) > 2 and f[2] == "dashed"})
    return lanes, steps, arrows


def main():
    lanes, steps, arrows = read()
    W, H = 13.33, 6.95
    fig, ax = S.new_canvas(W, H)
    S.title(ax, TITLE, W)

    LX, RX = 0.30, 13.03            # lane band extent
    TOP, LH, GAP = 1.05, 1.36, 0.10
    lane_y = {lid: TOP + i * (LH + GAP) + LH / 2 for i, lid in enumerate(LANE_IDS)}
    C0, CW = 2.85, 2.25              # column 1 centre, column pitch
    col_x = {c: C0 + (c - 1) * CW for c in range(1, 6)}
    BW, BH = 2.12, 0.92

    for lid in LANE_IDS:
        y0 = lane_y[lid] - LH / 2
        ax.add_patch(FancyBboxPatch((LX, y0), RX - LX, LH, boxstyle="round,pad=0,rounding_size=0.02",
                                    facecolor=PANEL, edgecolor=RULE, lw=1.0, zorder=1))
        lab = ax.text(0.48, lane_y[lid], lanes[lid], fontsize=13, fontweight="bold", color=INK, va="center",
                      ha="left", zorder=2)
        S.text_fits(WHO, fig, ax, lab, 0.40, col_x[1] - BW / 2, pad=0.04)

    box = {}
    for n, sid in enumerate(STEP_IDS, 1):
        st = steps[sid]
        cx, cy = col_x[st["col"]], lane_y[st["lane"]]
        x0, y0 = cx - BW / 2, cy - BH / 2
        dashed = st["dashed"]
        if dashed:
            fc, ec, ls = WHITE, SEP_EDGE, (0, (4, 3))
        elif st["lane"] in NDTWIN_LANES:
            fc, ec, ls = REPO_FILL, REPO_EDGE, "-"
        else:
            fc, ec, ls = SEP_FILL, SEP_EDGE, "-"
        ax.add_patch(FancyBboxPatch((x0, y0), BW, BH, boxstyle="round,pad=0,rounding_size=0.06", facecolor=fc,
                                    edgecolor=ec, lw=1.4, ls=ls, zorder=3))
        ax.add_patch(Circle((x0 + 0.02, y0 + 0.02), 0.17, facecolor=ACCENT if not dashed else SEP_EDGE,
                            edgecolor=WHITE, lw=1.2, zorder=5))
        ax.text(x0 + 0.02, y0 + 0.025, str(n), ha="center", va="center", fontsize=10.5, fontweight="bold",
                color=WHITE, zorder=6)
        a1 = ax.text(cx, cy - 0.15, st["t1"], ha="center", va="center", fontsize=11.5, fontweight="bold",
                     color=INK, zorder=4)
        a2 = ax.text(cx, cy + 0.20, st["t2"], ha="center", va="center", fontsize=10.5, color=MUTED, zorder=4)
        for a in (a1, a2):
            S.text_fits(WHO, fig, ax, a, x0, x0 + BW)
        box[sid] = (x0, y0, BW, BH, cx, cy)

    def route(a, b):
        """Vertical out of a's top or bottom edge to b's row, then horizontal into b's left edge; straight down
        or up when both share a column."""
        ax0, ay0, aw, ah, acx, acy = box[a]
        bx0, by0, bw, bh, bcx, bcy = box[b]
        if abs(acx - bcx) < 1e-6:
            return [(acx, ay0 + ah if bcy > acy else ay0), (bcx, by0 if bcy > acy else by0 + bh)]
        sy = ay0 + ah if bcy > acy else ay0
        return [(acx, sy), (acx, bcy), (bx0, bcy)]

    for ar in arrows:
        pts = route(ar["a"], ar["b"])
        ls = (0, (4, 3)) if ar["dashed"] else "-"
        if len(pts) > 2:
            ax.add_patch(PathPatch(Path(pts[:-1]), fill=False, edgecolor=INK, lw=1.5, ls=ls, zorder=2.5,
                                   capstyle="butt", joinstyle="miter"))
        ax.add_patch(FancyArrowPatch(pts[-2], pts[-1], arrowstyle="-|>", mutation_scale=14, color=INK, lw=1.5,
                                     ls=ls, shrinkA=0, shrinkB=0, zorder=2.6))
        if ar["ann"]:
            (x1, y1), (x2, y2) = pts[0], pts[1]
            ax.text(x1 + 0.10, (y1 + y2) / 2, ar["ann"], ha="left", va="center", fontsize=11, color=ACCENT,
                    fontweight="bold", zorder=7,
                    bbox=dict(boxstyle="round,pad=0.15", facecolor=WHITE, edgecolor="none"))

    os.makedirs(OUTDIR, exist_ok=True)
    S.save_all(fig, OUTDIR, STEM)
    rows = "\n".join(f"| {i} {sid} | {lanes[st['lane']]} | {st['t1']} / {st['t2']} | {' '.join(st['ev'])} |"
                     for i, (sid, st) in enumerate(steps.items(), 1))
    text = f"""# {STEM} -- {TITLE}

Page P04 of the 1028 deck. Evidence class: READ (code and docs of the PR tree, read, not executed).
Spec: figures_spec/rules_lost_flow.txt (lanes, steps, arrows and their evidence). Generator:
generator/make_p04_rules_lost.py with the shared style generator/figstyle_1028.py.

## Steps and evidence

| # step | lane | label | evidence |
|---|---|---|---|
{rows}

## Drawing

- NDTwin's own components (kernel, P4 proxy) blue; the switch and the app grey; dashed white steps:
  {", ".join(k for k, v in steps.items() if v["dashed"])} (no shipped app resends on the notice yet; replayed is always false).
- Arrows: {", ".join(a["a"] + "->" + a["b"] + (" (" + a["ann"] + ")" if a["ann"] else "") for a in arrows)}.
"""
    S.write_companion(OUTDIR, STEM, __file__, text)
    print(f"{WHO}: wrote {STEM} (6 steps, {len(arrows)} arrows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
