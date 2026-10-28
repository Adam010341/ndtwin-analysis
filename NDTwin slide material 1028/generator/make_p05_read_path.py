#!/usr/bin/env python3
"""
make_p05_read_path.py -- p4/fig_p05_read_path: reading registers and direct counters. Page P05 of the 1028
deck. Evidence class: READ (code of the PR tree, not executed; the bmv2 fact on the P4Runtime channel was
measured offline and is cited in the spec).

Top to bottom: the app; the P4 proxy's REST API with its two routes; two channels down to one bmv2 switch --
P4Runtime for the direct counter (left), Thrift for the register (right) behind its two checks, each check with
its refusal (status, nothing read). Every label is read from figures_spec/read_path.txt; positions are here.

Stops with a named reason if: the spec's canvas title differs; an element id the figure draws is missing from
the spec, has no evidence line, or an id the figure does not draw is listed; an arrow names an element that is
not drawn, or an arrow the figure draws is not in the spec; a label's rendered text sticks out of its box.

[Co-developed with claude code -- Adam]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle_1028 as S  # noqa: E402
from figstyle_1028 import (ACCENT, INK, MUTED, WHITE, REPO_FILL, REPO_EDGE, SEP_FILL, SEP_EDGE,  # noqa: E402
                           ACCENT_BG, RULE)
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402

WHO = "make_p05_read_path"
STEM = "fig_p05_read_path"
TITLE = "Reading registers and direct counters"
IDS = ["APP", "PROXY", "R_DC", "R_REG", "CH_P4RT", "CH_THRIFT", "CHK1", "CHK2", "REF1", "REF2", "SW", "SW_DC",
       "SW_REG"]
DRAWN_ARROWS = [("APP", "R_DC"), ("APP", "R_REG"), ("R_DC", "SW_DC"), ("R_REG", "CHK1"), ("CHK1", "CHK2"),
                ("CHK2", "SW_REG"), ("CHK1", "REF1"), ("CHK2", "REF2")]
REFUSE = "#9C3B2E"
args = sys.argv[1:]


def opt(name, default):
    return args[args.index(name) + 1] if name in args else default


SPEC = opt("--spec", os.path.join(S.DECK, "figures_spec", "read_path.txt"))
OUTDIR = opt("--out", os.path.join(S.DECK, "figures", "p4"))


def read():
    text, sec = S.read_spec(WHO, SPEC, TITLE)
    el = {}
    for r in S.need_section(WHO, sec, "ELEMENTS", SPEC):
        f = r["fields"]
        if len(f) != 3:
            S.die(WHO, f"ELEMENTS row {f} is not 'id | label | second line'")
        if not r["evidence"]:
            S.die(WHO, f"element {f[0]} has no evidence line")
        el[f[0]] = {"t1": f[1], "t2": None if f[2] == "-" else f[2], "ev": r["evidence"]}
    for i in IDS:
        if i not in el:
            S.die(WHO, f"read_path.txt has no entry for element {i}")
    extra = [i for i in el if i not in IDS]
    if extra:
        S.die(WHO, f"read_path.txt lists {extra}, which the figure does not draw")
    arrows = []
    for r in S.need_section(WHO, sec, "ARROWS", SPEC):
        ends = tuple(x.strip() for x in r["fields"][0].split("->"))
        if len(ends) != 2 or any(e not in el for e in ends):
            S.die(WHO, f"arrow {r['fields'][0]} names an element that is not drawn")
        arrows.append(ends)
    for a in DRAWN_ARROWS:
        if a not in arrows:
            S.die(WHO, f"the figure draws arrow {a[0]} -> {a[1]}, which read_path.txt does not list")
    for a in arrows:
        if a not in DRAWN_ARROWS:
            S.die(WHO, f"read_path.txt lists arrow {a[0]} -> {a[1]}, which the figure does not draw")
    return el


def main():
    el = read()
    W, H = 13.33, 6.95
    fig, ax = S.new_canvas(W, H)
    S.title(ax, TITLE, W)
    geo = {}

    def box(eid, x, y, w, h, style, fs=12.5, bold=True, sub_fs=10.5, mono=False):
        fc, ec, ls = {"ndt": (REPO_FILL, REPO_EDGE, "-"), "grey": (SEP_FILL, SEP_EDGE, "-"),
                      "white": (WHITE, SEP_EDGE, "-"), "panel": (ACCENT_BG, REPO_EDGE, "-")}[style]
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.06", facecolor=fc,
                                    edgecolor=ec, lw=1.4, ls=ls, zorder=3))
        e = el[eid]
        fam = "DejaVu Sans Mono" if mono else None
        if e["t2"]:
            a1 = ax.text(x + w / 2, y + h * 0.36, e["t1"], ha="center", va="center", fontsize=fs,
                         fontweight="bold" if bold else "normal", color=INK, zorder=4, family=fam)
            a2 = ax.text(x + w / 2, y + h * 0.72, e["t2"], ha="center", va="center", fontsize=sub_fs, color=MUTED,
                         zorder=4)
            S.text_fits(WHO, fig, ax, a2, x, x + w)
        else:
            a1 = ax.text(x + w / 2, y + h / 2, e["t1"], ha="center", va="center", fontsize=fs,
                         fontweight="bold" if bold else "normal", color=INK, zorder=4, family=fam)
        S.text_fits(WHO, fig, ax, a1, x, x + w)
        geo[eid] = (x, y, w, h)

    def arrow(p, q, color=INK, lw=1.6):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=color, lw=lw, shrinkA=0,
                                     shrinkB=0, zorder=6))

    def bottom(eid, dx=0.0):
        x, y, w, h = geo[eid]
        return (x + w / 2 + dx, y + h)

    def top(eid, dx=0.0):
        x, y, w, h = geo[eid]
        return (x + w / 2 + dx, y)

    # app
    box("APP", 5.42, 0.98, 2.5, 0.62, "grey", fs=13.5)
    # proxy panel with its two routes
    ax.add_patch(FancyBboxPatch((0.55, 2.02), 12.23, 1.30, boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor=ACCENT_BG, edgecolor=REPO_EDGE, lw=1.4, zorder=2))
    pl = ax.text(0.72, 2.20, el["PROXY"]["t1"], fontsize=12.5, fontweight="bold", color=ACCENT, va="center",
                 zorder=4)
    ax.text(0.72 + S.text_fits(WHO, fig, ax, pl, 0.55, 4.0) + 0.15, 2.20, el["PROXY"]["t2"], fontsize=11,
            color=MUTED, va="center", zorder=4)
    geo["PROXY"] = (0.55, 2.02, 12.23, 1.30)
    box("R_DC", 1.05, 2.42, 4.45, 0.78, "ndt", fs=12, mono=True)
    box("R_REG", 7.85, 2.42, 4.45, 0.78, "ndt", fs=12, mono=True)
    ax.plot([3.275, 10.075], [1.80, 1.80], color=INK, lw=1.6, zorder=5, solid_capstyle="butt")
    ax.plot([6.30, 6.30], [1.60, 1.80], color=INK, lw=1.6, zorder=5)
    arrow((3.275, 1.80), top("R_DC"))
    arrow((10.075, 1.80), top("R_REG"))

    # the two checks of the register path
    box("CHK1", 8.30, 3.62, 3.55, 0.56, "white", fs=11.5)
    box("CHK2", 8.30, 4.46, 3.55, 0.56, "white", fs=11.5)
    arrow(bottom("R_REG"), top("CHK1"))
    arrow(bottom("CHK1"), top("CHK2"))
    for chk, ref in (("CHK1", "REF1"), ("CHK2", "REF2")):
        x, y, w, h = geo[chk]
        arrow((x + w, y + h / 2), (x + w + 0.42, y + h / 2), color=REFUSE, lw=1.4)
        t = ax.text(x + w + 0.50, y + h / 2 - 0.11, el[ref]["t1"], fontsize=11.5, fontweight="bold", color=REFUSE,
                    va="center", zorder=7)
        t2 = ax.text(x + w + 0.50, y + h / 2 + 0.13, el[ref]["t2"], fontsize=10, color=REFUSE, va="center", zorder=7)
        S.text_fits(WHO, fig, ax, t2, x + w + 0.40, W - 0.10, pad=0.0)
        geo[ref] = (x + w + 0.5, y, 0.8, h)

    # the switch
    ax.add_patch(FancyBboxPatch((0.55, 5.52), 12.23, 1.25, boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor=SEP_FILL, edgecolor=SEP_EDGE, lw=1.4, zorder=2))
    sw = ax.text(0.72, 5.70, el["SW"]["t1"], fontsize=12.5, fontweight="bold", color=INK, va="center", zorder=4)
    S.text_fits(WHO, fig, ax, sw, 0.55, 4.0)
    geo["SW"] = (0.55, 5.52, 12.23, 1.25)
    box("SW_DC", 1.55, 5.90, 3.45, 0.62, "white", fs=11.5, bold=False)
    box("SW_REG", 8.35, 5.90, 3.45, 0.62, "white", fs=11.5, bold=False)
    arrow(bottom("R_DC"), top("SW_DC"))
    arrow(bottom("CHK2"), top("SW_REG", dx=-0.0))

    # channel labels beside their arrows
    for ch, xa, ya in (("CH_P4RT", 3.275 + 0.16, 4.30), ("CH_THRIFT", 10.075 - 0.16 - 3.35, 5.25)):
        e = el[ch]
        ha = "left"
        if ch == "CH_THRIFT":
            xa = 10.075 + 0.16
            ya = 5.27
            t1 = ax.text(xa, ya - 0.0, e["t1"], fontsize=12, fontweight="bold", color=ACCENT, va="center",
                         ha=ha, zorder=7)
            t2 = ax.text(xa + S.text_fits(WHO, fig, ax, t1, xa - 0.1, W, pad=0.0) + 0.14, ya, e["t2"], fontsize=10.5,
                         color=MUTED, va="center", ha=ha, zorder=7)
            S.text_fits(WHO, fig, ax, t2, xa, W - 0.1, pad=0.0)
            geo[ch] = (xa, ya, 1, 0.3)
            continue
        t1 = ax.text(xa, ya - 0.14, e["t1"], fontsize=12, fontweight="bold", color=ACCENT, va="center", ha=ha,
                     zorder=7)
        t2 = ax.text(xa, ya + 0.14, e["t2"], fontsize=10.5, color=MUTED, va="center", ha=ha, zorder=7)
        for t in (t1, t2):
            S.text_fits(WHO, fig, ax, t, xa - 0.1, 7.8, pad=0.0)
        geo[ch] = (xa, ya, 1, 0.3)

    missing = [i for i in IDS if i not in geo]
    if missing:
        S.die(WHO, f"elements not drawn: {missing}")
    os.makedirs(OUTDIR, exist_ok=True)
    S.save_all(fig, OUTDIR, STEM)
    rows = "\n".join(f"| {i} | {e['t1']}{' / ' + e['t2'] if e['t2'] else ''} | {' '.join(e['ev'])} |"
                     for i, e in el.items())
    text = f"""# {STEM} -- {TITLE}

Page P05 of the 1028 deck. Evidence class: READ (code of the PR tree, read, not executed); the fact on the
P4Runtime channel ("no register reads on bmv2") was measured offline on throwaway bmv2 and is cited below.
Spec: figures_spec/read_path.txt. Generator: generator/make_p05_read_path.py with generator/figstyle_1028.py.

## Elements and evidence

| id | label | evidence |
|---|---|---|
{rows}

## Drawing

- NDTwin's proxy and its two routes blue; the app and the switch grey; the two checks white, each with its
  refusal in red (status, nothing read). The register arrow reaches the switch only through both checks.
"""
    S.write_companion(OUTDIR, STEM, __file__, text)
    print(f"{WHO}: wrote {STEM} ({len(IDS)} elements, {len(DRAWN_ARROWS)} arrows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
