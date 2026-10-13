#!/usr/bin/env python3
"""
make_p04_map.py -- landscape/fig_p04_map: where 16 tools sit, model fidelity (x) against the link to a
running network (y).  Page P04 of the 1014 deck.  Evidence class: READ (public material for the 15
other tools, code and docs at trunk 3a47bdb7 for NDTwin).

Data: figures_spec/landscape.tsv: `#` lines at the top carry the one placement rule (read, checked present,
copied to the companion .md); then the columns tool, x_category, y_category, short_label, rationale, source,
unsure.  The generator reads tool / x_category / y_category / short_label; rationale, source and the unsure
flag go to the companion .md.  The persona (marker colour) of each tool is taken from
research/matrix_final.json (personas.*.columns), so a tool cannot be coloured by hand.

Stops with a named reason (template section 0 rule 11 style) if: the tsv does not have exactly 16 rows
or lacks a column; an x/y category is not on the axis; a tool is not a matrix column; a short label
lacks the * (commercial) or dagger (academic) mark its matrix column name carries (or has one it does
not); a short label is empty or longer than 18 characters; NDTwin is missing or not in the 'packet-level
emulation x none' cell; the tsv header does not state "one point per tool" (the figure draws exactly one point
per tool, no hollow second marker); the tsv has no `#` placement-rule header; the number of `unsure = yes`
rows differs from the number the header states; the template's P04 text states a different count for the
packet-level emulation x none cell than the tsv holds (the count itself is read from the tsv).

[Co-developed with claude code -- Adam]
"""
import csv
import io
import json
import re
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle_1014 as S  # noqa: E402
from figstyle_1014 import (ACCENT, ACCENT_BG, BODY, FAINT, INK, MUTED, PANEL, RULE, WHITE, PERSONA,  # noqa: E402
                           plt)
from matplotlib.patches import Rectangle, FancyBboxPatch  # noqa: E402

WHO = "make_p04_map"
STEM = "fig_p04_map"
TITLE = "Where 16 tools sit: fidelity vs live link"
AXIS_Y = "link to a network the tool does not build or control"
args = sys.argv[1:]


def opt(name, default):
    return args[args.index(name) + 1] if name in args else default


SPEC = opt("--spec", os.path.join(S.DECK, "figures_spec", "landscape.tsv"))
MATRIX = opt("--matrix", os.path.join(S.DECK, "research", "matrix_final.json"))
OUTDIR = opt("--out", os.path.join(S.DECK, "figures", "landscape"))
TEMPLATE = opt("--template", os.environ.get("TEMPLATE_1014") or os.path.join(S.DECK, "NDTwin-slide-template-1014.md"))

XCATS = ["config model", "ML model", "flow-level model", "packet-level emulation", "real devices"]
YCATS = ["none", "imports snapshots", "stays synced live"]   # bottom -> top
NDT = "NDTwin"


def load():
    raw = open(SPEC, encoding="utf-8").read().splitlines()
    rule = [ln[1:].strip() for ln in raw if ln.startswith("#")]
    if not rule:
        S.die(WHO, "landscape.tsv has no `#` placement-rule header")
    body = [ln for ln in raw if not ln.startswith("#")]
    with io.StringIO("\n".join(body) + "\n") as f:
        rd = csv.DictReader(f, delimiter="\t")
        need = ["tool", "x_category", "y_category", "short_label", "rationale", "source", "unsure"]
        if rd.fieldnames != need:
            S.die(WHO, f"landscape.tsv columns are {rd.fieldnames}, want {need}")
        rows = list(rd)
    if len(rows) != 16:
        S.die(WHO, f"landscape.tsv has {len(rows)} data rows, the page needs 16")
    with open(MATRIX, encoding="utf-8") as f:
        m = json.load(f)
    cols = m["maturity"]["columns"]
    group = {}
    for g, p in m["personas"].items():
        for c in p["columns"]:
            group.setdefault(c, g)
    seen = set()
    for r in rows:
        t = r["tool"]
        if t in seen:
            S.die(WHO, f"tool listed twice: {t}")
        seen.add(t)
        if t not in cols:
            S.die(WHO, f"tool {t!r} is not a matrix_final.json maturity column")
        if r["y_category"] not in YCATS:
            S.die(WHO, f"{t}: y_category {r['y_category']!r} is not one of {YCATS}")
        if r["x_category"] not in XCATS and not r["x_category"].startswith("not applicable"):
            S.die(WHO, f"{t}: x_category {r['x_category']!r} is not one of {XCATS}")
        lab = r["short_label"].strip()
        if not lab or len(lab) > 18:
            S.die(WHO, f"{t}: short label {lab!r} is empty or longer than 18 characters")
        commercial = "commercial" in t
        academic = "academic" in t
        if commercial != lab.endswith("*"):
            S.die(WHO, f"{t}: commercial={commercial} but label {lab!r} "
                       f"{'lacks' if commercial else 'has'} the * mark")
        if academic != lab.endswith("†"):
            S.die(WHO, f"{t}: academic={academic} but label {lab!r} "
                       f"{'lacks' if academic else 'has'} the dagger mark")
        r["group"] = "ndt" if t == NDT else group.get(t)
        if r["group"] is None:
            S.die(WHO, f"{t}: not in any matrix persona column list")
    if NDT not in seen:
        S.die(WHO, "NDTwin row missing")
    cell = [r for r in rows if r["x_category"] == "packet-level emulation"
            and r["y_category"] == "none"]
    ndt = [r for r in rows if r["tool"] == NDT][0]
    if ndt not in cell:
        S.die(WHO, "NDTwin is not in the packet-level emulation x none cell")
    stated = re.search(r"(\d+) rows are unsure", " ".join(rule))
    n_unsure = sum(1 for r in rows if r["unsure"].startswith("yes"))
    if stated and int(stated.group(1)) != n_unsure:
        S.die(WHO, f"the header says {stated.group(1)} rows are unsure, the tsv has {n_unsure} `yes` rows")
    if os.path.exists(TEMPLATE):
        m = re.search(r"x none cell holds (\d+)", open(TEMPLATE, encoding="utf-8").read())
        if m and int(m.group(1)) != len(cell):
            S.die(WHO, f"the template says the emulation x none cell holds {m.group(1)}, the tsv has {len(cell)}")
    if "one point per tool" not in " ".join(rule).lower():
        S.die(WHO, "the tsv header no longer states the one-point-per-tool rule (no second marker for any tool)")
    for r in rows:
        r["_rule"] = rule
    return rows


def main():
    rows = load()
    rule = rows[0]["_rule"]
    ncell = sum(1 for r in rows if r["x_category"] == "packet-level emulation" and r["y_category"] == "none")
    W = 13.33
    X0, X1 = 1.95, 13.0
    cw = (X1 - X0) / 5
    PITCH = 0.265                      # list pitch in the emulation x none cell (NDTwin is its first entry)
    Y_TOP = 1.0
    rh = {"stays synced live": 1.05, "imports snapshots": 1.1,
          "none": 0.30 + (ncell - 1) * PITCH + 0.24}
    ytop, y = {}, Y_TOP
    for yc in reversed(YCATS):                       # top row first
        ytop[yc] = y
        y += rh[yc]
    Y_BOT = y
    H = Y_BOT + 1.12
    fig, ax = S.new_canvas(W, H)
    S.title(ax, TITLE, W)
    xc = {c: X0 + (i + 0.5) * cw for i, c in enumerate(XCATS)}
    rend = fig.canvas.get_renderer()

    # grid; the cell NDTwin sits in is tinted
    for i, c in enumerate(XCATS):
        for yc in YCATS:
            ndt_cell = (c == "packet-level emulation" and yc == "none")
            ax.add_patch(Rectangle((X0 + i * cw, ytop[yc]), cw, rh[yc],
                                   facecolor=ACCENT_BG if ndt_cell else (PANEL if (i + YCATS.index(yc)) % 2 else WHITE),
                                   edgecolor=RULE, lw=1, zorder=1))
    for c in XCATS:
        ax.text(xc[c], Y_BOT + 0.30, c.replace("packet-level emulation", "packet-level\nemulation")
                .replace("flow-level model", "flow-level\nmodel"), ha="center", va="center", fontsize=12,
                color=INK, fontweight="bold", linespacing=1.15)
    for yc in YCATS:
        ax.text(X0 - 0.12, ytop[yc] + rh[yc] / 2, yc.replace(" ", "\n", 1), ha="right", va="center", fontsize=12,
                color=INK, fontweight="bold", linespacing=1.15)
    ax.text(X0 - 0.12, Y_BOT + 0.30, "model fidelity \u2192", ha="right", va="center", fontsize=11, color=FAINT)
    ax.text(0.42, (Y_TOP + Y_BOT) / 2, AXIS_Y + " \u2192", rotation=90, ha="center",
            va="center", fontsize=11, color=FAINT)

    R = 0.085       # marker radius, inches (axes are in inches)
    ms = (2 * R * 72) ** 2 * 0.785  # scatter area in pt^2 for that diameter

    def colour(r):
        return ACCENT if r["group"] == "ndt" else PERSONA[r["group"]]["color"]

    def put(r, mx, my, kind="dot"):
        c = colour(r)
        if r["group"] == "ndt":       # highlighted, same band as the others: accent colour, bold label, no row of its own
            ax.scatter([mx], [my], s=ms * 2.2, color=c, zorder=7, linewidths=0)
            ax.text(mx + 0.19, my, r["short_label"], ha="left", va="center", zorder=7, fontsize=12.5,
                    color=c, fontweight="bold")
            return
        if kind == "dot":
            ax.scatter([mx], [my], s=ms, color=c, zorder=5, linewidths=0)
        elif kind == "sim":       # ns-3: packet-level SIMULATION, open circle
            ax.scatter([mx], [my], s=ms, facecolor=WHITE, edgecolor=c, linewidths=2.0, zorder=5)
        elif kind == "monitor":   # sFlow-RT: hollow diamond = monitor, not a model
            ax.scatter([mx], [my], s=ms * 1.15, marker="D", facecolor=WHITE, edgecolor=c,
                       linewidths=2.0, zorder=5)
        ax.text(mx + 0.17, my, r["short_label"], ha="left", va="center", zorder=6, fontsize=10.5, color=BODY)

    cells = {}
    for r in rows:
        if r["short_label"].startswith("IRTF"):
            continue
        cells.setdefault((r["x_category"], r["y_category"]), []).append(r)
    for (xcat, ycat), lst in cells.items():
        cx = xc[xcat]
        top = ytop[ycat]
        if (xcat, ycat) == ("packet-level emulation", "none"):
            # one list: NDTwin first (highlighted), then the control-app tools (ns-3 first of them, open
            # circle = packet-level SIMULATION), then the P4 tools, then the operator tools
            order = {"ndt": -1, "app": 0, "p4": 1, "ops": 2}
            lst.sort(key=lambda r: (order[r["group"]], r["short_label"] != "ns-3"))
            for k, r in enumerate(lst):
                my = top + 0.30 + k * PITCH
                put(r, cx - 0.95, my, "sim" if r["short_label"] == "ns-3" else "dot")
        else:
            n = len(lst)
            for k, r in enumerate(lst):
                my = top + rh[ycat] / 2 + (k - (n - 1) / 2) * 0.33
                kind = "monitor" if r["short_label"] == "sFlow-RT" else "dot"
                if r["short_label"] == "sFlow-RT":
                    my = ytop["stays synced live"] + 0.72
                put(r, cx - 0.78, my, kind)

    # IRTF draft: dashed horizontal band across the whole top row, label at the left end, no point
    irtf = [r for r in rows if r["short_label"].startswith("IRTF")][0]
    bc = colour(irtf)
    by0 = ytop["stays synced live"] + 0.10
    ax.add_patch(FancyBboxPatch((X0 + 0.08, by0), X1 - X0 - 0.16, 0.30,
                                boxstyle="round,pad=0,rounding_size=0.08", facecolor=WHITE,
                                edgecolor=bc, lw=1.6, ls=(0, (5, 3)), zorder=3))
    ax.text(X0 + 0.22, by0 + 0.15, irtf["short_label"], ha="left", va="center", fontsize=10.5,
            color=bc, fontweight="bold", zorder=6)

    # NDTwin's what-if whisker: dashed, left from its list entry to the flow-level model column (same y as the
    # entry, so the map shows no difference in y); no second marker for any other target
    nd = [r for r in rows if r["group"] == "ndt"][0]
    ny = ytop[nd["y_category"]] + 0.30 + 0 * PITCH
    nx = xc[nd["x_category"]] - 0.95
    wx = xc["flow-level model"]
    ax.plot([wx, nx - 0.17], [ny, ny], color=ACCENT, lw=1.8, ls=(0, (4, 3)), zorder=4)
    ax.plot([wx, wx], [ny - 0.10, ny + 0.10], color=ACCENT, lw=1.8, zorder=4)
    ax.text(wx + 0.06, ny - 0.20, "what-if", ha="left", va="center", fontsize=10.5, color=ACCENT, zorder=6)

    # legend, two lines
    ly1, ly2 = Y_BOT + 0.68, Y_BOT + 0.95
    x = 0.45
    for g in ("app", "p4", "ops"):
        ax.scatter([x + R], [ly1], s=ms, color=PERSONA[g]["color"], zorder=5, linewidths=0)
        t = ax.text(x + 0.2, ly1, PERSONA[g]["name"], ha="left", va="center", fontsize=10.5, color=BODY)
        x += 0.2 + t.get_window_extent(rend).width / fig.dpi + 0.30
    ax.text(x + 0.2, ly1, "* vendor material only    \u2020 paper or draft only", ha="left", va="center",
            fontsize=10.5, color=MUTED)
    x = 0.45
    ax.scatter([x + R], [ly2], s=ms, facecolor=WHITE, edgecolor=MUTED, linewidths=2.0, zorder=5)
    t = ax.text(x + 0.28, ly2, "packet-level simulation", ha="left", va="center", fontsize=10.5, color=BODY)
    x += 0.28 + t.get_window_extent(rend).width / fig.dpi + 0.30
    ax.scatter([x + R], [ly2], s=ms * 1.15, marker="D", facecolor=WHITE, edgecolor=MUTED, linewidths=2.0, zorder=5)
    t = ax.text(x + 0.28, ly2, "monitor, not a model", ha="left", va="center", fontsize=10.5, color=BODY)
    x += 0.28 + t.get_window_extent(rend).width / fig.dpi + 0.30
    ax.add_patch(FancyBboxPatch((x, ly2 - 0.09), 0.40, 0.18, boxstyle="round,pad=0,rounding_size=0.05",
                                facecolor=WHITE, edgecolor=MUTED, lw=1.4, ls=(0, (5, 3))))
    ax.text(x + 0.50, ly2, "framework (draft)", ha="left", va="center", fontsize=10.5, color=BODY)

    S.save_all(fig, OUTDIR, STEM)
    print(f"[out] {STEM}: {len(rows)} tools drawn (16 expected); emulation x none cell holds {ncell} "
          f"(incl. NDTwin); canvas {W} x {H:.2f} in")

    # companion .md
    lines = ["| tool | x | y | label | unsure | rationale | source |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append("| {tool} | {x} | {y} | {lab} | {u} | {ra} | {so} |".format(
            tool=r["tool"], x=r["x_category"], y=r["y_category"], lab=r["short_label"],
            u=r["unsure"].replace("|", "/"), ra=r["rationale"].replace("|", "/"), so=r["source"].replace("|", "/")))
    unsure_rows = [r["short_label"] for r in rows if r["unsure"].startswith("yes")]
    rule_txt = "\n".join("> " + ln for ln in rule)
    text = f"""# `{STEM}` -- Where 16 tools sit: fidelity vs live link (page P04)

[Co-developed with claude code -- Adam]

Evidence class: **READ** (competitor positions from public material read 2026-10-08, commercial = vendor
material, academic = paper or draft; NDTwin from code and docs at trunk 3a47bdb7, full
3a47bdb7612d2608a7feb17614c8d686032ef38f). Nothing on this figure was run.

## Data source

- Positions: `figures_spec/landscape.tsv` sha256 `{S.sha16(SPEC)}...` (16 rows, read as-is; its `#` header is the
  placement rule below).
- Marker colour (persona of the tool's matrix group): `research/matrix_final.json` sha256
  `{S.sha16(MATRIX)}...`, `personas.*.columns`; NDTwin in the accent colour.
- Axes: x = config model, ML model, flow-level model, packet-level emulation, real devices (equal
  spacing); y = none, imports snapshots, stays synced live; y axis title "{AXIS_Y}".

## Placement rule (verbatim from the tsv header)

{rule_txt}

## How the markers are drawn (spec: template section 2 P04)

- Filled circle per tool; label = `short_label`; `*` = vendor material only, `\u2020` = paper or draft only.
- Layout decision for the emulation x none cell, which holds {ncell} tools (the count is read from the tsv): the
  cell is one vertical list with NDTwin as its first entry, in the same band as the other {ncell - 1}: same x,
  same vertical range, no row of its own, so the map shows no difference in y. NDTwin is highlighted (accent colour,
  larger marker, bold label). The other entries follow in one column (control-app tools, ns-3 first with an open
  circle = packet-level SIMULATION, then P4 tools, then operator tools). All {ncell} labels sit at 10.5 pt or
  larger on the canvas, so neither two columns nor abbreviations were needed; the bottom row is taller instead.
  The template's 3 x 3 cluster was already not used (under 0.8 in per label at equal column spacing).
- NDTwin's whisker (dashed) runs left from its entry to the flow-level model column: the shipped what-if
  (flow-level max-min). It runs at the height of NDTwin's own entry, at the top of the cell, so it crosses no label.
- One point per tool: there is NO second marker for NDTwin's physical path (coded, no run on record), and none for
  any other tool's hardware path; P02 and P16 disclose the physical path. The generator stops if the tsv header
  stops saying "one point per tool".
- sFlow-RT: hollow diamond = monitor, not a model.
- IRTF NDT draft: dashed band across the whole top row, label at its left end, no point; legend entry "framework (draft)".
- Persona is encoded by colour only on this figure: marker shape is already used for the marker kinds.

## Unsure positions (landscape.tsv column `unsure`)

{len(unsure_rows)} rows carry `unsure` = yes ({", ".join(unsure_rows)}); the header states the same number.
The reasons are verbatim in the table below.

## All rows

{chr(10).join(lines)}

## Caveats

- The bottom row is named "none" (no link to a network the tool does not build or control): NDTwin and
  ONOS+Mininet both sit there although both keep a live view of the fabric they control; the axis title says
  what the rows measure.
- 'Live' for NDTwin means synced with the emulated fabric it builds and controls through its own Ryu app or P4
  proxy, not with an external production network.
- A cell is about the documented feature, not about how well it works.
"""
    S.write_companion(OUTDIR, STEM, __file__, text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
