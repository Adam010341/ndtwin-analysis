#!/usr/bin/env python3
"""
make_p09_next.py -- next/fig_p09_next: what comes next. Page P09 of the 1028 deck. Evidence class: INFERRED
(a plan). A small roadmap in the style of the 1014 deck's P22: column bars NOW / NEXT, lanes, one box per step,
no dates and no arrows.

Everything drawn is read from figures_spec/next.txt. The generator also reads the deck template's P07 and P08
tables (§2) and stops if any row there names a next step that no box here comes from -- so a weakness on
P07/P08 cannot lose its next step on the roadmap. There is no exemption: every row's next step must be drawn.

Stops with a named reason if: the canvas title differs; a section is missing; a box names a lane or column the
spec does not list; a box has no evidence line; a box's `from` is not "P07 row N", "P08 row N" or "brief"; a
P07/P08 row with a next step has no box; a label does not fit its box on two lines.

[Co-developed with claude code -- Adam]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle_1028 as S  # noqa: E402
from figstyle_1028 import (ACCENT, INK, WHITE, REPO_FILL, REPO_EDGE, SEP_FILL, SEP_EDGE, PANEL,  # noqa: E402
                           RULE)
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

WHO = "make_p09_next"
STEM = "fig_p09_next"
TITLE = "What comes next"
args = sys.argv[1:]


def opt(name, default):
    return args[args.index(name) + 1] if name in args else default


SPEC = opt("--spec", os.path.join(S.DECK, "figures_spec", "next.txt"))
TEMPLATE = opt("--template", os.path.join(S.DECK, "NDTwin-slide-template-1028.md"))
OUTDIR = opt("--out", os.path.join(S.DECK, "figures", "next"))


def template_next_steps():
    """[(page, row number, next step)] from the P07 and P08 tables of the template's section 2."""
    if not os.path.exists(TEMPLATE):
        S.die(WHO, f"template missing: {TEMPLATE}")
    t = open(TEMPLATE, encoding="utf-8").read()
    out = []
    for pid in ("P07", "P08"):
        m = re.search(r"^### " + pid + r" .*?\n((?:\|.*\n)+)", t, re.M)
        if not m:
            S.die(WHO, f"template has no {pid} table")
        rows = [r.strip().strip("|").split("|") for r in m.group(1).strip().splitlines()]
        head = [c.strip() for c in rows[0]]
        if "next step" not in head:
            S.die(WHO, f"template {pid} table has no 'next step' column")
        j = head.index("next step")
        for n, r in enumerate(rows[2:], 1):
            out.append((pid, n, r[j].strip()))
    return out


def read():
    text, sec = S.read_spec(WHO, SPEC, TITLE)
    cols = {r["fields"][0]: r["fields"][1] for r in S.need_section(WHO, sec, "COLUMNS", SPEC)}
    lanes = {r["fields"][0]: r["fields"][1] for r in S.need_section(WHO, sec, "LANES", SPEC)}
    boxes = []
    for r in S.need_section(WHO, sec, "BOXES", SPEC):
        f = r["fields"]
        if len(f) != 5:
            S.die(WHO, f"BOXES row {f} is not 'id | lane | column | label | from'")
        bid, lane, col, label, frm = f
        if lane not in lanes:
            S.die(WHO, f"box {bid} names lane {lane!r}, which LANES does not list")
        if col not in cols:
            S.die(WHO, f"box {bid} names column {col!r}, which COLUMNS does not list")
        if not r["evidence"]:
            S.die(WHO, f"box {bid} has no evidence line")
        if not re.fullmatch(r"P0[78] row \d+|brief", frm):
            S.die(WHO, f"box {bid} from {frm!r} is not 'P07 row N', 'P08 row N' or 'brief'")
        boxes.append({"id": bid, "lane": lane, "col": col, "label": label, "from": frm, "ev": r["evidence"]})
    froms = {b["from"] for b in boxes}
    for pid, n, step in template_next_steps():
        if f"{pid} row {n}" not in froms:
            S.die(WHO, f"{pid} row {n} names next step {step!r}, but no box comes from it")
    return cols, lanes, boxes


def main():
    cols, lanes, boxes = read()
    W, H = 13.33, 6.95
    fig, ax = S.new_canvas(W, H)
    S.title(ax, TITLE, W)
    LX, CX0, GAPC = 0.30, 2.55, 0.20
    CW = (13.03 - CX0 - GAPC) / len(cols)
    col_x0 = {c: CX0 + i * (CW + GAPC) for i, c in enumerate(cols)}
    for c, x0 in col_x0.items():
        ax.add_patch(Rectangle((x0, 1.02), CW, 0.42, facecolor=ACCENT, edgecolor="none", zorder=2))
        ax.text(x0 + CW / 2, 1.23, cols[c], ha="center", va="center", fontsize=15, fontweight="bold", color=WHITE,
                zorder=3)
    PER_ROW, BH, BG, PADY = 2, 0.72, 0.12, 0.13
    bw = (CW - GAPC * (PER_ROW + 1)) / PER_ROW
    y = 1.60
    drawn = []
    for lid, lab in lanes.items():
        cells = {c: [b for b in boxes if b["lane"] == lid and b["col"] == c] for c in cols}
        nrows = max(1, max((len(v) + PER_ROW - 1) // PER_ROW for v in cells.values()))
        lh = nrows * BH + (nrows - 1) * BG + 2 * PADY
        ax.add_patch(FancyBboxPatch((LX, y), 13.03 - LX, lh, boxstyle="round,pad=0,rounding_size=0.02",
                                    facecolor=PANEL, edgecolor=RULE, lw=1.0, zorder=1))
        t = ax.text(0.48, y + lh / 2, lab, fontsize=13, fontweight="bold", color=INK, va="center", zorder=2)
        S.text_fits(WHO, fig, ax, t, LX, CX0, pad=0.04)
        for c, bl in cells.items():
            for k, b in enumerate(bl):
                rr, cc = divmod(k, PER_ROW)
                x0 = col_x0[c] + GAPC + cc * (bw + GAPC)
                y0 = y + PADY + rr * (BH + BG)
                now = c == list(cols)[0]
                ax.add_patch(FancyBboxPatch((x0, y0), bw, BH, boxstyle="round,pad=0,rounding_size=0.06",
                                            facecolor=REPO_FILL if now else SEP_FILL,
                                            edgecolor=REPO_EDGE if now else SEP_EDGE, lw=1.4, zorder=3))
                a = ax.text(x0 + bw / 2, y0 + BH / 2, b["label"], ha="center", va="center", fontsize=12.5,
                            color=INK, zorder=4, linespacing=1.15)
                r = fig.canvas.get_renderer()
                bb = a.get_window_extent(renderer=r).transformed(ax.transData.inverted())
                if abs(bb.x1 - bb.x0) > bw - 0.40:
                    words = b["label"].split(" ")
                    best = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(b["label"]) / 2)) \
                        if len(words) > 1 else None
                    if best is None:
                        S.die(WHO, f"box {b['id']} label {b['label']!r} does not fit and has no space to break at")
                    a.set_text(" ".join(words[:best]) + "\n" + " ".join(words[best:]))
                S.text_fits(WHO, fig, ax, a, x0, x0 + bw, pad=0.08)
                drawn.append(b["id"])
        y += lh + 0.12
    if y > H - 0.05:
        S.die(WHO, f"lanes end at {y:.2f} in, below the canvas ({H} in)")
    os.makedirs(OUTDIR, exist_ok=True)
    S.save_all(fig, OUTDIR, STEM)
    rows = "\n".join(f"| {b['id']} | {lanes[b['lane']]} | {cols[b['col']]} | {b['label']} | {b['from']} | "
                     f"{' '.join(b['ev'])} |" for b in boxes)
    text = f"""# {STEM} -- {TITLE}

Page P09 of the 1028 deck. Evidence class: INFERRED (a plan; no dates). Spec: figures_spec/next.txt. Generator:
generator/make_p09_next.py with generator/figstyle_1028.py. It reads the template's P07 and P08 tables and
stops if a next step there has no box here.

## Boxes

| id | lane | column | label | from | stated in |
|---|---|---|---|---|---|
{rows}
"""
    S.write_companion(OUTDIR, STEM, __file__, text)
    print(f"{WHO}: wrote {STEM} ({len(drawn)} boxes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
