#!/usr/bin/env python3
"""
make_p18_health.py -- p4/fig_p18_health: the P4 health check.  Page P18 of the 1014 deck.
Two titled panels, never mixed: left = READ (which cells the check decides, from the code at 3a47bdb7);
right = RAN, offline only (the S0 static stage and cells T4-T7 on throwaway bmv2, not on the NDTwin fabric).

Everything is read from figures_spec/p4_health.tsv at run time. The left panel is checked against the code:
the generator reads tools/p4_health/cells/table.py with `git -C <kernel> show 3a47bdb7:<path>` and stops if the
spec's cells per dimension (in order) differ from the Cell(id, dimension) rows of CELLS.

Stops with a named reason if: the spec is missing, has a row kind other than `dim` / `off`, or a row that names a
prediction; the title does not say "offline" or its cell count differs from the cells drawn; the right panel's
title does not say "not yet run against a live lab"; the spec's cells differ from the code (or the code cannot be
read); an `off` row is neither S0 nor a cell of the left panel, has a result outside the run vocabulary, or names
a target other than throwaway stock / fast bmv2; any text on the canvas looks like provenance (figstyle).
Test hooks (red-check only): --spec PATH, --out DIR, --cells-file PATH (read CELLS from a file instead of git).

[Co-developed with claude code -- Adam]
"""
import csv
import io
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle_1014 as S  # noqa: E402
from figstyle_1014 import ACCENT, ACCENT_BG, BODY, GREEN, INK, MUTED, PANEL, RULE, WHITE  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

WHO = "make_p18_health"
STEM = "fig_p18_health"
KERNEL = S.KERNEL
PIN = "3a47bdb7"
CELLS_PATH = "tools/p4_health/cells/table.py"
RESULTS = ("COMPLETE", "GREEN", "RED", "PROBE-BROKEN", "INCOMPLETE", "NOT RUN")
args = sys.argv[1:]


def opt(name, default):
    return args[args.index(name) + 1] if name in args else default


SPEC = opt("--spec", os.path.join(S.DECK, "figures_spec", "p4_health.tsv"))
OUTDIR = opt("--out", os.path.join(S.DECK, "figures", "p4"))
CELLS_FILE = opt("--cells-file", None)


def load_spec():
    if not os.path.exists(SPEC):
        S.die(WHO, f"spec missing: {SPEC}")
    raw = open(SPEC, encoding="utf-8").read()
    meta = dict(re.findall(r"^#\s*(title|left|right|source):\s*(.+?)\s*$", raw, re.M))
    for k in ("title", "left", "right"):
        if k not in meta:
            S.die(WHO, f"p4_health.tsv has no `# {k}:` line")
    body = "\n".join(l for l in raw.splitlines() if not l.startswith("#"))
    rows = list(csv.reader(io.StringIO(body), delimiter="\t"))
    if not rows or rows[0][:3] != ["kind", "label", "cells_or_result"]:
        S.die(WHO, f"p4_health.tsv header is {rows[0] if rows else None}, want kind/label/cells_or_result/bmv2")
    dims, offs = [], []
    for r in rows[1:]:
        if not r or not "".join(r).strip():
            continue
        if re.search(r"(?i)predict|expect", "\t".join(r)):
            S.die(WHO, f"row {r[:2]} names a prediction; predictions never go on this figure")
        if r[0] == "dim":
            dims.append((r[1], [c.strip() for c in r[2].split(",") if c.strip()]))
        elif r[0] == "off":
            if len(r) < 4:
                S.die(WHO, f"offline row {r[1]!r} has no bmv2 column")
            offs.append((r[1], r[2].strip(), r[3].strip()))
        else:
            S.die(WHO, f"row kind {r[0]!r} is not `dim` or `off`")
    return meta, dims, offs


def code_cells():
    if CELLS_FILE:
        src = open(CELLS_FILE, encoding="utf-8").read()
    else:
        p = subprocess.run(["git", "-C", KERNEL, "show", f"{PIN}:{CELLS_PATH}"], capture_output=True, text=True)
        if p.returncode != 0:
            S.die(WHO, f"cannot read {CELLS_PATH}@{PIN}: {p.stderr.strip()[:120]}")
        src = p.stdout
    if "CELLS = [" not in src:
        S.die(WHO, f"{CELLS_PATH}@{PIN} has no CELLS list")
    out = []
    for cid, dim in re.findall(r'Cell\("([^"]+)", "([^"]+)"', src[src.index("CELLS = ["):]):
        if not out or out[-1][0] != dim:
            out.append((dim, []))
        out[-1][1].append(cid)
    return out


def check(meta, dims, offs):
    code = code_cells()
    if [c for _, c in dims] != [c for _, c in code]:
        S.die(WHO, "the spec's cells differ from CELLS in the code: spec "
                   f"{sum(len(c) for _, c in dims)} cells / {len(dims)} dimensions, code "
                   f"{sum(len(c) for _, c in code)} cells / {len(code)} dimensions")
    n = sum(len(c) for _, c in dims)
    if "offline" not in meta["title"].lower():
        S.die(WHO, f"title {meta['title']!r} does not say offline")
    m = re.search(r"(\d+) cells", meta["title"])
    if not m or int(m.group(1)) != n:
        S.die(WHO, f"title says {m.group(1) if m else 'no'} cells, the figure draws {n}")
    if "not yet run against a live lab" not in meta["right"]:
        S.die(WHO, f"right panel title {meta['right']!r} does not say 'not yet run against a live lab'")
    ids = {c for _, cs in dims for c in cs}
    for label, res, target in offs:
        cid = label.split(" ")[0]
        if cid not in ("S0", "writer") and cid not in ids:
            S.die(WHO, f"offline row {label!r} is neither S0, the writer comparison nor a cell of the left panel")
        if cid == "writer":
            if not re.fullmatch(r"\d+ disagree", res):
                S.die(WHO, f"offline row {label!r} result {res!r} is not '<n> disagree'")
        elif res not in RESULTS:
            S.die(WHO, f"offline row {label!r} result {res!r} is not a run result ({', '.join(RESULTS)})")
        if not re.fullmatch(r"(stock|fast)( (\+|·) (stock|fast))?|stock; fast ×\d+", target):
            S.die(WHO, f"offline row {label!r} target {target!r} is not throwaway stock / fast bmv2")
    return n


def main():
    meta, dims, offs = load_spec()
    n = check(meta, dims, offs)
    W, H = 13.33, 7.15
    fig, ax = S.new_canvas(W, H)
    S.title(ax, meta["title"], W)
    # ---- left panel: READ
    lx, ly, lw = 0.45, 1.25, 7.15
    ax.text(lx, ly, meta["left"], fontsize=15, fontweight="bold", color=INK, va="center")
    cols, rows_per = 2, (len(dims) + 1) // 2
    cw, ch, gx, gy = (lw - 0.15) / cols, 0.40, 0.15, 0.065
    y0 = ly + 0.42
    for i, (label, cells) in enumerate(dims):
        c, r = i // rows_per, i % rows_per
        x, y = lx + c * (cw + gx), y0 + r * (ch + gy)
        hot = False                      # no highlight: an outline would need a key (few words)
        ax.add_patch(FancyBboxPatch((x, y), cw - gx, ch, boxstyle="round,pad=0,rounding_size=0.05",
                                    facecolor=ACCENT_BG if hot else PANEL, edgecolor=ACCENT if hot else RULE,
                                    lw=1.6 if hot else 0.8, zorder=2))
        ax.text(x + 0.14, y + ch / 2, label, fontsize=12, color=INK, va="center", zorder=3,
                fontweight="bold" if hot else "normal")
        ax.text(x + cw - gx - 0.14, y + ch / 2, str(len(cells)), fontsize=12, color=ACCENT if hot else MUTED,
                va="center", ha="right", fontweight="bold", zorder=3)
    # ---- separator
    sx = lx + lw + 0.25
    ax.plot([sx, sx], [1.05, H - 0.35], color=RULE, lw=1.2)
    # ---- right panel: RAN offline
    rx, rw = sx + 0.30, W - (sx + 0.30) - 0.40
    ax.text(rx, ly, meta["right"], fontsize=15, fontweight="bold", color=INK, va="center")
    head = ("check", "result", "bmv2")
    cx = [rx, rx + rw * 0.49, rx + rw * 0.74]
    hy = ly + 0.62
    for x, h in zip(cx, head):
        ax.text(x + 0.08, hy, h, fontsize=12, color=MUTED, va="center", fontweight="bold")
    ax.plot([rx, rx + rw], [hy + 0.25, hy + 0.25], color=RULE, lw=1.0)
    rh = 0.62
    for k, (label, res, target) in enumerate(offs):
        y = hy + 0.30 + k * rh
        ax.add_patch(Rectangle((rx, y), rw, rh - 0.06, facecolor=PANEL if k % 2 == 0 else WHITE,
                               edgecolor="none", zorder=1))
        ax.text(cx[0] + 0.08, y + (rh - 0.06) / 2, label, fontsize=13, color=INK, va="center", zorder=3)
        ax.text(cx[1] + 0.08, y + (rh - 0.06) / 2, res, fontsize=13, va="center", fontweight="bold", zorder=3,
                color=GREEN if res in ("GREEN", "COMPLETE", "0 disagree") else BODY)
        ax.text(cx[2] + 0.08, y + (rh - 0.06) / 2, target, fontsize=13, color=BODY, va="center", zorder=3)
    S.save_all(fig, OUTDIR, STEM)
    print(f"[out] {STEM}: {n} cells over {len(dims)} dimensions (READ, checked against {CELLS_PATH}@{PIN}); "
          f"{len(offs)} offline rows (RAN offline)")
    text = f"""# `{STEM}` -- {meta['title']} (page P18)

[Co-developed with claude code -- Adam]

Two panels, two evidence classes, never mixed.

- Left, **READ**: the cells the health check decides, one box per P4 feature dimension with its cell count, read
  from `{CELLS_PATH}@{PIN}` (CELLS: {n} cells, {len(dims)} dimensions). The generator re-reads that file with
  `git show {PIN}:{CELLS_PATH}` on every run and stops if the spec differs. No box is highlighted.
- Right, **RAN, offline only**: the S0 static stage, cells T4-T7 and the table-writer comparison (52 shape cases), observed on throwaway bmv2 switches (stock
  and fast), not on the NDTwin fabric and not against a live lab. Commits and binary identity are in the P19
  speaker notes of the template (T4-T7 and the writer comparison: bmv2 binaries identified by install path only, no hash).
- No prediction is drawn (`doc/audit/2026-10-03_p4-health-check/expected_today.tsv` is not read).

## Data source

- `figures_spec/p4_health.tsv` sha256 `{S.sha16(SPEC)}...`.
"""
    S.write_companion(OUTDIR, STEM, __file__, text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
