#!/usr/bin/env python3
"""
make_p20_roadmap.py -- next/fig_p20_roadmap: what we fix first, and what we disclose.  Page P20 of the
1021 deck.  Evidence class: a plan (INFERRED from the ranked problems of P17-P19); no dates, no
commitments.

Everything about the picture is READ from the specs at run time, nothing about ranks, columns or arrows is
typed in this file:
  figures_spec/roadmap.txt   canvas title, the four lane names, the PLACEMENT block (rank -> lane, column,
                             fix text, in the order listed), the DISCLOSE block, the DEPENDENCY ARROWS block;
  figures_spec/problems.tsv  rank, problem, hurts, cost, fixable.  Box fill = persona hurt most = the first
                             persona in `hurts` (shape as second encoding: round corner = control-app developer,
                             square = P4-program developer, diamond tab = network operator).
Layout (rows of two boxes per cell, arrow routes) is computed from that.

Stops with a named reason if: roadmap.txt does not state the rank count ("any rank 1-N is missing");
problems.tsv does not have each rank 1..N exactly once; roadmap.txt draws a
rank twice, omits one, or draws one that problems.tsv does not have; a fixable=no row is drawn in a fix lane or
a fixable=yes row in DISCLOSE; a rank's column disagrees with the column rule applied to its cost (NOW: every
part under about a week; NEXT: a part of about a week or more; LATER: needs a design decision); a `hurts` text
names no persona; the spec's canvas title is not the title drawn; an arrow names a rank that is not drawn; the
spec has no ARROW LEGEND line; a box sticks out of its column; no route exists that crosses no box; or no route
exists whose segments stay at least MIN_ARROW_GAP_PT (10 pt) from every other arrow's segments along one line; or
no route exists in which two different arrows that lie on one line (across distance under 10 pt, both vertical or
both horizontal) are at least MIN_COLLINEAR_GAP_PT (72 pt) apart end to end, so two arrows never read as one line.
Test hooks (red-check only): --min-gap-pt N, --min-collinear-gap-pt N, --colw NAME=INCHES,
--routes-json PATH (writes the chosen routes, in inches, as json; the red-check points it into its temp dir).

[Co-developed with claude code -- Adam]
"""
import csv
import itertools
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle_1021 as S  # noqa: E402
from figstyle_1021 import (ACCENT, BODY, INK, PANEL, RULE, WHITE, PERSONA)  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon, FancyArrowPatch  # noqa: E402

ARROW_LABEL = None
WHO = "make_p20_roadmap"
STEM = "fig_p20_roadmap"
TITLE = "What we fix first, and what we disclose"
args = sys.argv[1:]


def opt(name, default):
    return args[args.index(name) + 1] if name in args else default


SPEC = opt("--spec", os.path.join(S.DECK, "figures_spec", "problems.tsv"))
ROADMAP = opt("--roadmap", os.path.join(S.DECK, "figures_spec", "roadmap.txt"))
OUTDIR = opt("--out", os.path.join(S.DECK, "figures", "next"))
COLS = ["NOW", "NEXT", "LATER", "DISCLOSE"]
MIN_GAP_PT = float(opt("--min-gap-pt", "10"))        # arrows may not run closer than this along one line
# two different arrows on one line (across < MIN_GAP_PT) must be at least this far apart end to end
MIN_COLLINEAR_GAP_PT = float(opt("--min-collinear-gap-pt", "72"))
ROUTES_JSON = opt("--routes-json", None)


def parse_roadmap():
    if not os.path.exists(ROADMAP):
        S.die(WHO, f"roadmap spec missing: {ROADMAP}")
    lines = open(ROADMAP, encoding="utf-8").read().splitlines()
    full = "\n".join(lines)
    m = re.search(r"Title on canvas[^:]*:\s*(.+)", full)
    if not m or m.group(1).strip() != TITLE:
        S.die(WHO, f"roadmap.txt canvas title is {m.group(1).strip() if m else None!r}, the figure draws {TITLE!r}")
    try:
        i0 = next(i for i, l in enumerate(lines) if l.startswith("PLACEMENT"))
        i1 = next(i for i, l in enumerate(lines) if l.startswith("DEPENDENCY ARROWS"))
    except StopIteration:
        S.die(WHO, "roadmap.txt has no PLACEMENT or no DEPENDENCY ARROWS block")
    lanes, place, order, cur_lane, section = [], {}, {}, None, "lane"
    for ln in lines[i0 + 1:i1]:
        ml = re.match(r'^\s+Lane\s+(\d+)\s+"(.+)"\s*$', ln)
        if ml:
            lanes.append(ml.group(2))
            cur_lane, section = len(lanes) - 1, "lane"
            continue
        if re.match(r"^\s+DISCLOSE\b", ln):
            cur_lane, section = None, "disclose"
            continue
        mp = re.match(r"^\s+(NOW|NEXT|LATER)\s+#(\d+)\s+(.+?)\s*$", ln)
        md_ = re.match(r"^\s+#(\d+)\s+(.+?)\s*$", ln)
        if mp and section == "lane":
            col, rk, txt = mp.group(1), int(mp.group(2)), mp.group(3)
            parts = re.split(r"\s{2,}", txt, maxsplit=1)          # the spec puts the cost after 2+ spaces
            txt, cost = parts[0], (parts[1] if len(parts) > 1 else None)
        elif md_ and section == "disclose":
            col, rk, txt, cost = "DISCLOSE", int(md_.group(1)), md_.group(2), None
        else:
            continue
        if rk in place:
            S.die(WHO, f"roadmap.txt draws rank {rk} twice")
        txt = re.sub(r"\s*--\s*one box in \w+\s*$", "", txt)
        txt = re.sub(r"\s*\([^)]*(?:day|week)[^)]*\)", "", txt)      # costs live in the notes, not on the canvas
        txt = txt.strip()
        place[rk] = {"lane": cur_lane, "col": col, "text": txt[0].upper() + txt[1:], "cost_spec": cost}
        order.setdefault((cur_lane, col), []).append(rk)
    if len(lanes) != 4:
        S.die(WHO, f"roadmap.txt names {len(lanes)} lanes, want 4")
    ml = re.search(r"ARROW LEGEND \(on canvas\):\s*(.+)", full)
    if not ml:
        S.die(WHO, "roadmap.txt has no `ARROW LEGEND (on canvas): <label>` line")
    global ARROW_LABEL, NRANK
    ARROW_LABEL = ml.group(1).strip()
    mn = re.search(r"any rank 1-(\d+) is missing", full)
    if not mn:
        S.die(WHO, "roadmap.txt states no rank count (want a line saying 'any rank 1-N is missing')")
    NRANK = int(mn.group(1))
    arrows = []
    for ln in lines[i1 + 1:]:
        if ln.strip().startswith("ON THE CANVAS") or ln.strip().startswith("WHY THIS ORDER"):
            break
        ma = re.match(r"^\s+#(\d+)\s*->\s*#(\d+)", ln)
        if ma:
            arrows.append((int(ma.group(1)), int(ma.group(2))))
    return lanes, place, order, arrows


def first_persona(rank, hurts):
    h = hurts.lower()
    pos = {key: h.find(token) for token, key in (("app dev", "app"), ("p4 dev", "p4"), ("operator", "ops"))
           if h.find(token) >= 0}
    if not pos:
        S.die(WHO, f"rank {rank}: `hurts` {hurts!r} names no persona")
    return min(pos, key=pos.get)


def column_rule(cost):
    c = cost.lower()
    if "design decision" in c:
        return "LATER"
    if re.search(r"\bweeks?\b", c):
        return "NEXT"
    return "NOW"


def load():
    lanes, place, order, arrows = parse_roadmap()
    with open(SPEC, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f, delimiter="\t")
        need = ["rank", "problem", "hurts", "evidence", "fix", "cost", "fixable"]
        if rd.fieldnames != need:
            S.die(WHO, f"problems.tsv columns are {rd.fieldnames}, want {need}")
        rows = list(rd)
    ranks = [int(r["rank"]) for r in rows]
    dup = sorted({x for x in ranks if ranks.count(x) > 1})
    if dup:
        S.die(WHO, f"problems.tsv rank(s) duplicated: {dup}")
    miss = [x for x in range(1, NRANK + 1) if x not in ranks]
    if miss:
        S.die(WHO, f"problems.tsv rank(s) missing: {miss}")
    if len(ranks) != NRANK:
        S.die(WHO, f"problems.tsv has {len(ranks)} rows, roadmap.txt states {NRANK}")
    byr = {int(r["rank"]): r for r in rows}
    for rk in range(1, NRANK + 1):
        if rk not in place:
            S.die(WHO, f"rank {rk} is in problems.tsv but not drawn on the roadmap (roadmap.txt)")
    for rk in place:
        if rk not in byr:
            S.die(WHO, f"rank {rk} is drawn but not in problems.tsv")
    for rk, pl in place.items():
        r = byr[rk]
        no = r["fixable"].strip().lower().startswith("no")
        if no and pl["col"] != "DISCLOSE":
            S.die(WHO, f"rank {rk} is fixable=no but is drawn in a fix lane ({pl['col']})")
        if not no and pl["col"] == "DISCLOSE":
            S.die(WHO, f"rank {rk} is fixable=yes but is drawn in DISCLOSE")
        if not no:
            want = column_rule(r["cost"])
            if want != pl["col"]:
                S.die(WHO, f"rank {rk} is drawn in {pl['col']} but the column rule on its cost "
                           f"({r['cost']!r}) gives {want}")
        r["persona"] = first_persona(rk, r["hurts"])
    for a, b in arrows:
        if a not in place or b not in place:
            S.die(WHO, f"arrow {a}->{b} names a rank that is not drawn")
    return lanes, place, order, arrows, byr


def main():
    lanes, place, order, arrows, byr = load()
    W = 13.33
    LX, LW, gap = 0.45, 1.40, 0.12
    colw = {"NOW": 3.5, "NEXT": 3.5, "LATER": 1.7, "DISCLOSE": 1.65}
    for a_ in args:                                   # red-check hook: --colw NEXT=2.0
        if re.match(r"^(NOW|NEXT|LATER|DISCLOSE)=[\d.]+$", a_):
            colw[a_.split("=")[0]] = float(a_.split("=")[1])
    colx, x = {}, LX + LW + gap
    for c in COLS:
        colx[c] = x
        x += colw[c] + gap
    assert x - gap <= W - 0.40, x
    per_row = {"NOW": 2, "NEXT": 2, "LATER": 1, "DISCLOSE": 1}
    HEAD_Y, HEAD_H, PAD, VGAP, BOX_H = 0.90, 0.36, 0.07, 0.07, 0.58

    # ---- slot order inside each cell: spec order, adjusted so an arrow's source sits at the end of its row
    # (nothing to its right) and its target at the start (nothing to its left); fewest inversions wins
    out_x = {a for a, b in arrows if (place[a]["col"], place[a]["lane"]) != (place[b]["col"], place[b]["lane"])
             and place[a]["col"] != place[b]["col"]}
    in_x = {b for a, b in arrows if place[a]["col"] != place[b]["col"]}
    slots = {}
    for key, lst in order.items():
        pr = per_row[key[1]]
        best = None
        for perm in itertools.permutations(lst):
            viol = 0
            for pos, rk in enumerate(perm):
                c = pos % pr
                if rk in out_x and c != pr - 1:
                    viol += 1
                if rk in in_x and c != 0:
                    viol += 1
            inv = sum(1 for i in range(len(perm)) for j in range(i + 1, len(perm))
                      if lst.index(perm[i]) > lst.index(perm[j]))
            cost = (viol, inv)
            if best is None or cost < best[0]:
                best = (cost, perm)
        for pos, rk in enumerate(best[1]):
            slots[rk] = (pos // pr, pos % pr)

    # ---- text per box (hanging indent for the #N tag), so row heights follow the longest label
    import matplotlib.pyplot as plt
    fig0 = plt.figure(figsize=(W, 7))
    ax0 = fig0.add_axes([0, 0, 1, 1])
    rend = fig0.canvas.get_renderer()

    def width_in(txt, fs):
        t = ax0.text(0, 0, txt, fontsize=fs)
        w = t.get_window_extent(rend).width / fig0.dpi
        t.remove()
        return w

    def hang(text, bw, fs, first_pad=0.0):
        words, lines, cur = [], [], ""
        for w in text.split(" "):
            words.extend(re.findall(r"[^-]+-?", w) if (len(w) > 14 and "-" in w) else [w])
        glue = False
        for w in words:
            sep = "" if glue else " "
            trial = (cur + sep + w).strip() if cur else w
            avail = bw - 0.20 - ((0.40 + first_pad) if not lines else 0.0)
            if width_in(trial, fs) > avail and cur:
                lines.append(cur)
                cur = w
            else:
                cur = trial
            glue = w.endswith("-") and len(w) > 1 and w != "-"
        lines.append(cur)
        return lines

    # box widths: in a two-box row the width is shared in proportion to the label length
    def widths_for(col, members):
        inner = colw[col] - 0.10 * (len(members) + 1)
        wts = [len(place[m]["text"]) + 14 for m in members]
        floor = 1.15
        if inner >= floor * len(members):          # every box gets the floor, the rest is shared by label length
            ws = [floor + (inner - floor * len(members)) * w / sum(wts) for w in wts]
        else:                                      # cannot fit: equal split (the inside-column check will say so)
            ws = [floor] * len(members)
        if len(members) == 1:                      # a lone box keeps the width of a half cell
            ws = [min(ws[0], (colw[col] - 0.30) / 2)]
        return ws

    rows_members = {}
    for rk, (r, c) in slots.items():
        pl = place[rk]
        rows_members.setdefault((pl["lane"], pl["col"], r), []).append((c, rk))
    box_wd, box_dx = {}, {}
    for (lane, col, r), mem in rows_members.items():
        mem = [rk for c, rk in sorted(mem)]
        if per_row[col] == 1:
            ws = [colw[col] - 0.20]
        else:
            ws = widths_for(col, mem)
        x_off = 0.10
        for rk, w in zip(mem, ws):
            box_wd[rk], box_dx[rk] = w, x_off
            x_off += w + 0.10

    FS, PITCH = 10.5, 10.5 * 1.18 / 72
    lines_of = {rk: hang(pl["text"], box_wd[rk] if pl["col"] != "DISCLOSE" else colw["DISCLOSE"] - 0.20, FS,
                         0.16 if byr[rk]["persona"] == "ops" else 0.0)
                for rk, pl in place.items() if pl["col"] != "DISCLOSE" or True}
    need_h = {rk: max(BOX_H, len(lines_of[rk]) * PITCH + 0.14) for rk in place}
    plt.close(fig0)

    # ---- row heights per (lane, row); lane heights; y positions
    lane_rows = {}
    for rk, pl in place.items():
        if pl["lane"] is None:
            continue
        key = (pl["lane"], slots[rk][0])
        lane_rows[key] = max(lane_rows.get(key, 0), need_h[rk])
    lane_y, lane_h, row_y, y = [], [], {}, HEAD_Y + HEAD_H + 0.10
    for li in range(4):
        rows_here = sorted(r for (l, r) in lane_rows if l == li)
        lane_y.append(y)
        yy = y + PAD
        for r in rows_here:
            row_y[(li, r)] = yy
            yy += lane_rows[(li, r)] + VGAP
        lane_h.append(yy - VGAP + PAD - y)
        y = yy - VGAP + PAD + 0.08
    LANES_BOTTOM = y - 0.08
    H = LANES_BOTTOM + 0.58
    fig, ax = S.new_canvas(W, H)
    S.title(ax, TITLE, W)

    for c in COLS:
        grey = c == "DISCLOSE"
        ax.add_patch(Rectangle((colx[c], HEAD_Y), colw[c], HEAD_H, facecolor="#8A9399" if grey else ACCENT,
                               edgecolor="none", zorder=2))
        ax.text(colx[c] + colw[c] / 2, HEAD_Y + HEAD_H / 2, c, ha="center", va="center", color=WHITE,
                fontsize=13, fontweight="bold", zorder=3)
    import textwrap
    for i, name in enumerate(lanes):
        ax.add_patch(Rectangle((LX, lane_y[i]), colx["LATER"] + colw["LATER"] - LX, lane_h[i],
                               facecolor=PANEL if i % 2 == 0 else WHITE, edgecolor=RULE, lw=0.8, zorder=1))
        ax.text(LX + 0.10, lane_y[i] + lane_h[i] / 2, "\n".join(textwrap.wrap(name, 15)), ha="left", va="center",
                fontsize=11.5, fontweight="bold", color=INK, linespacing=1.15, zorder=3)
    ax.add_patch(Rectangle((colx["DISCLOSE"], HEAD_Y + HEAD_H + 0.10), colw["DISCLOSE"],
                           LANES_BOTTOM - (HEAD_Y + HEAD_H + 0.10), facecolor="#EEF0F1", edgecolor=RULE,
                           lw=0.8, zorder=1))

    # ---- boxes
    boxes = {}
    disc = [rk for rk in sorted(place) if place[rk]["col"] == "DISCLOSE"]
    dy = HEAD_Y + HEAD_H + 0.10 + 0.14
    for rk, pl in sorted(place.items()):
        if pl["col"] == "DISCLOSE":
            bh = max(need_h[rk], BOX_H + 0.30)
            boxes[rk] = (colx["DISCLOSE"] + 0.10, dy, colw["DISCLOSE"] - 0.20, bh)
            dy += bh + 0.14
            continue
        r, c = slots[rk]
        bw = box_wd[rk]
        bx = colx[pl["col"]] + box_dx[rk]
        by = row_y[(pl["lane"], r)]
        row_h = lane_rows[(pl["lane"], r)]
        boxes[rk] = (bx, by, bw, row_h)

    for rk, (bx, by, bw, bh) in sorted(boxes.items()):
        pl = place[rk]
        P = PERSONA[byr[rk]["persona"]]
        isd = pl["col"] == "DISCLOSE"
        fill = "#C9CDD0" if isd else P["color"]
        tc = INK if isd else P["text"]
        rs = 0.20 if P["shape"] == "round" else 0.0
        ax.add_patch(FancyBboxPatch((bx, by), bw, bh, boxstyle=f"round,pad=0,rounding_size={rs}",
                                    facecolor=fill, edgecolor=P["color"] if isd else "none",
                                    lw=2.2 if isd else 0, zorder=4))
        if P["shape"] == "diamond":
            d = 0.11
            tx = bx + bw - 0.16
            ax.add_patch(Polygon([(tx, by - d), (tx + d, by), (tx, by + d), (tx - d, by)], closed=True,
                                 facecolor=P["color"], edgecolor=WHITE, lw=1.2, zorder=6))
        lines = lines_of[rk]
        y0 = by + bh / 2 - (len(lines) - 1) * PITCH / 2
        ax.text(bx + 0.10, y0, f"#{rk}", ha="left", va="center", fontsize=12, fontweight="bold", color=tc, zorder=7)
        for k, ln in enumerate(lines):
            ax.text(bx + 0.10 + (0.40 if k == 0 else 0.0), y0 + k * PITCH, ln, ha="left", va="center",
                    fontsize=FS, color=tc, zorder=7)

    # ---- every box stays inside its column
    for rk, (bx, by, bw, bh) in sorted(boxes.items()):
        c0, c1 = colx[place[rk]["col"]], colx[place[rk]["col"]] + colw[place[rk]["col"]]
        if bx < c0 - 1e-6 or bx + bw > c1 + 1e-6:
            S.die(WHO, f"box #{rk} sticks out of its {place[rk]['col']} column "
                       f"(box x {bx:.2f}-{bx + bw:.2f} in, column x {c0:.2f}-{c1:.2f} in)")

    # ---- dependency arrows: candidate routes in order; the first that crosses no box and keeps every segment at
    # least MIN_GAP_PT from every segment of an earlier arrow that runs along the same line wins
    GAP = MIN_GAP_PT / 72.0
    COLL = max(MIN_COLLINEAR_GAP_PT, MIN_GAP_PT) / 72.0

    def edge(rk, side, frac=0.5):
        bx, by, bw, bh = boxes[rk]
        return {"l": (bx, by + bh * frac), "r": (bx + bw, by + bh * frac), "b": (bx + bw / 2, by + bh),
                "t": (bx + bw / 2, by)}[side]

    def seg_hits_box(p, q, rect, eps=0.015):
        bx, by, bw, bh = rect
        x0, x1 = sorted((p[0], q[0]))
        y0, y1 = sorted((p[1], q[1]))
        return x1 > bx + eps and x0 < bx + bw - eps and y1 > by + eps and y0 < by + bh - eps

    def too_close(p, q, r, s_, along=None):
        """Two axis-aligned segments on (nearly) one line: closer than GAP across, and overlapping or within `along`
        (default GAP; COLL for the end-to-end rule) along the line."""
        along = GAP if along is None else along
        for k in (0, 1):                       # k=1: horizontal pair (compare y, extent in x); k=0: vertical pair
            o = 1 - k
            if abs(p[k] - q[k]) < 1e-9 and abs(r[k] - s_[k]) < 1e-9 and abs(p[k] - r[k]) < GAP:
                a0, a1 = sorted((p[o], q[o]))
                b0, b1 = sorted((r[o], s_[o]))
                if max(a0, b0) - min(a1, b1) < along:
                    return True
        return False

    def same_line_gaps(route_a, route_b):
        """[(orientation, line position in, end-to-end gap pt)] for every segment pair of two routes on one line."""
        res = []
        for p, q in zip(route_a[:-1], route_a[1:]):
            for r, s_ in zip(route_b[:-1], route_b[1:]):
                for k in (0, 1):
                    o = 1 - k
                    if abs(p[k] - q[k]) < 1e-9 and abs(r[k] - s_[k]) < 1e-9 and abs(p[k] - r[k]) < GAP:
                        a0, a1 = sorted((p[o], q[o]))
                        b0, b1 = sorted((r[o], s_[o]))
                        res.append(("vertical x" if k == 0 else "horizontal y", p[k],
                                    (max(a0, b0) - min(a1, b1)) * 72))
        return res

    def min_gap_pt(route_a, route_b):
        best = None
        for p, q in zip(route_a[:-1], route_a[1:]):
            for r, s_ in zip(route_b[:-1], route_b[1:]):
                for k in (0, 1):
                    o = 1 - k
                    if abs(p[k] - q[k]) < 1e-9 and abs(r[k] - s_[k]) < 1e-9:
                        a0, a1 = sorted((p[o], q[o]))
                        b0, b1 = sorted((r[o], s_[o]))
                        if max(a0, b0) - min(a1, b1) < GAP:
                            d = abs(p[k] - r[k]) * 72
                            best = d if best is None else min(best, d)
        return best

    drawn_routes, route_of = [], {}
    for a, b in arrows:
        gx = colx[place[a]["col"]] + colw[place[a]["col"]] + gap / 2
        cand = []
        for fy in (0.5, 0.2, 0.8):                       # where the arrow leaves / enters the box edges
            for ty in (0.5, 0.2, 0.8):
                p, q = edge(a, "r", fy), edge(b, "l", ty)
                if abs(p[1] - q[1]) < 1e-6:
                    cand.append([p, q])
                for off in (0.0, 1.5 * GAP, -1.5 * GAP):        # offsets must clear the GAP rule themselves
                    if not p[0] + 0.02 < gx + off < q[0] - 0.02:   # the vertical stays in the gutter between the two
                        continue                                   # boxes, never inside the source or target box
                    cand.append([p, (gx + off, p[1]), (gx + off, q[1]), q])
        for ty in (0.5, 0.2, 0.8):
            pb, q = edge(a, "b"), edge(b, "l", ty)
            cand.append([pb, (pb[0], q[1]), q])
        chosen, box_ok, coll_fail = None, False, False
        for route in cand:
            segs = list(zip(route[:-1], route[1:]))
            if any(seg_hits_box(s0, s1, boxes[k]) for s0, s1 in segs for k in boxes if k not in (a, b)):
                continue
            box_ok = True
            if any(too_close(s0, s1, r0, r1) for s0, s1 in segs for rr in drawn_routes
                   for r0, r1 in zip(rr[:-1], rr[1:])):
                continue
            if any(too_close(s0, s1, r0, r1, COLL) for s0, s1 in segs for rr in drawn_routes
                   for r0, r1 in zip(rr[:-1], rr[1:])):
                coll_fail = True
                continue
            chosen = route
            break
        if chosen is None:
            if coll_fail:
                S.die(WHO, f"arrow #{a} -> #{b} runs on the same line as an earlier arrow within "
                           f"{MIN_COLLINEAR_GAP_PT:g} pt end to end (every box-free route that keeps {MIN_GAP_PT:g} pt "
                           f"from the other arrows does so)")
            if box_ok:
                S.die(WHO, f"arrow #{a} -> #{b} cannot keep {MIN_GAP_PT:g} pt from the other arrows along one line "
                           f"(every box-free route runs within {MIN_GAP_PT:g} pt of an earlier arrow)")
            S.die(WHO, f"no non-crossing route exists for arrow #{a} -> #{b}")
        drawn_routes.append(chosen)
        route_of[(a, b)] = chosen
        for s0, s1 in zip(chosen[:-2], chosen[1:-1]):
            ax.plot([s0[0], s1[0]], [s0[1], s1[1]], color=INK, lw=1.7, zorder=8, solid_capstyle="round")
        ax.add_patch(FancyArrowPatch(chosen[-2], chosen[-1], arrowstyle="-|>", mutation_scale=15, color=INK,
                                     lw=1.7, shrinkA=0, shrinkB=0, zorder=8))
    # the same test, run on the final picture as a whole
    keys = list(route_of)
    worst = None
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            for p, q in zip(route_of[keys[i]][:-1], route_of[keys[i]][1:]):
                for r, s_ in zip(route_of[keys[j]][:-1], route_of[keys[j]][1:]):
                    if too_close(p, q, r, s_):
                        S.die(WHO, f"arrows #{keys[i][0]}->#{keys[i][1]} and #{keys[j][0]}->#{keys[j][1]} run within "
                                   f"{MIN_GAP_PT:g} pt of each other along one line")
                    if too_close(p, q, r, s_, COLL):
                        S.die(WHO, f"arrows #{keys[i][0]}->#{keys[i][1]} and #{keys[j][0]}->#{keys[j][1]} run on the same "
                                   f"line within {MIN_COLLINEAR_GAP_PT:g} pt end to end")
            g_ = min_gap_pt(route_of[keys[i]], route_of[keys[j]])
            if g_ is not None:
                worst = g_ if worst is None else min(worst, g_)
    print(f"[arrows] routes: " + "; ".join(f"#{a}->#{b} via {len(r) - 1} segment(s)" for (a, b), r in route_of.items())
          + f"; closest pair of parallel overlapping segments: {'none' if worst is None else '%.1f pt' % worst}")
    shared = []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            for orient, pos, g_ in same_line_gaps(route_of[keys[i]], route_of[keys[j]]):
                shared.append(f"#{keys[i][0]}->#{keys[i][1]} / #{keys[j][0]}->#{keys[j][1]} {orient}={pos:.2f} in: "
                              f"{g_:.1f} pt end to end")
    print(f"[arrows] same-line pairs (min {MIN_COLLINEAR_GAP_PT:g} pt end to end): "
          + ("none" if not shared else "; ".join(shared)))
    if ROUTES_JSON:
        import json
        os.makedirs(os.path.dirname(os.path.abspath(ROUTES_JSON)), exist_ok=True)
        with open(ROUTES_JSON, "w", encoding="utf-8") as fh:
            json.dump({"unit": "inch", "routes": {f"{a}->{b}": [list(pt) for pt in r] for (a, b), r in route_of.items()}},
                      fh, indent=1)

    # ---- persona legend
    ly = LANES_BOTTOM + 0.30
    x = LX
    rend2 = fig.canvas.get_renderer()
    for key in ("app", "p4", "ops"):
        P = PERSONA[key]
        rs = 0.09 if P["shape"] == "round" else 0.0
        ax.add_patch(FancyBboxPatch((x, ly - 0.11), 0.34, 0.22, boxstyle=f"round,pad=0,rounding_size={rs}",
                                    facecolor=P["color"], edgecolor="none", zorder=4))
        if P["shape"] == "diamond":
            d, tx = 0.08, x + 0.28
            ax.add_patch(Polygon([(tx, ly - 0.11 - d), (tx + d, ly - 0.11), (tx, ly - 0.11 + d), (tx - d, ly - 0.11)],
                                 closed=True, facecolor=P["color"], edgecolor=WHITE, lw=1, zorder=6))
        t = ax.text(x + 0.46, ly, P["name"], ha="left", va="center", fontsize=10.5, color=BODY)
        x += 0.46 + t.get_window_extent(rend2).width / fig.dpi + 0.40
    ax.add_patch(FancyArrowPatch((x, ly), (x + 0.45, ly), arrowstyle="-|>", mutation_scale=13, color=INK, lw=1.6))
    ax.text(x + 0.58, ly, ARROW_LABEL, ha="left", va="center", fontsize=10.5, color=BODY)

    S.save_all(fig, OUTDIR, STEM)
    print(f"[out] {STEM}: {len(place)} ranks drawn ({NRANK} expected), {len(arrows)} arrows; "
          f"columns NOW {sum(1 for p in place.values() if p['col'] == 'NOW')} / NEXT "
          f"{sum(1 for p in place.values() if p['col'] == 'NEXT')} / LATER "
          f"{sum(1 for p in place.values() if p['col'] == 'LATER')} / DISCLOSE "
          f"{sum(1 for p in place.values() if p['col'] == 'DISCLOSE')}; canvas {W} x {H:.2f} in")

    # ---- companion .md
    rows = ["| # | problem | hurts (first = fill) | column | lane | label on the figure | fixable | cost |",
            "|---|---|---|---|---|---|---|---|"]
    for rk in sorted(place):
        pl, r = place[rk], byr[rk]
        rows.append(f"| {rk} | {r['problem']} | {r['hurts']} | {pl['col']} | "
                    f"{lanes[pl['lane']] if pl['lane'] is not None else 'no lane'} | {pl['text']} | "
                    f"{r['fixable']} | {r['cost']} |")
    arrow_txt = "; ".join(f"#{a} -> #{b}" for a, b in arrows)
    text = f"""# `{STEM}` -- What we fix first, and what we disclose (page P20)

[Co-developed with claude code -- Adam]

Evidence class: **INFERRED (a plan)**. The ordering is derived from the ranked problems of P17-P19; the
costs are rough estimates (INFERRED in problems.tsv), the columns are horizons, not dates. Nothing here is
a commitment and nothing on it was run.

## Data source

- `figures_spec/problems.tsv` sha256 `{S.sha16(SPEC)}...` ({NRANK} ranked problems; evidence paths are @2ece656c and
  are in the file, not on the canvas).
- `figures_spec/roadmap.txt` sha256 `{S.sha16(ROADMAP)}...`: lanes, the rank -> lane/column placement with the
  fix text, DISCLOSE, and the arrows are all read from it at run time; box fill = persona hurt most = the
  first persona named in `hurts`; shape as second encoding: round corner = control-app developer, square =
  P4-program developer, diamond tab = network operator.
- Column rule, checked against each rank's cost in problems.tsv: NOW if every part is under about a week; NEXT if
  any part is about a week or more (up to 6 weeks); LATER if it needs a design decision first; DISCLOSE if
  fixable = no.
- Arrows (only these, from roadmap.txt): {arrow_txt}.
- Box labels are the roadmap.txt fix texts with the cost parentheticals removed (costs live in the notes).
  Within a cell the boxes keep the spec order except that an arrow's source sits at the end of its row and its
  target at the start (so the route crosses no box); the generator searches the orderings.

## Placement actually drawn

{chr(10).join(rows)}

## Checks the generator makes

Every rank 1-{NRANK} in problems.tsv exactly once and drawn exactly once; no fixable=no row in a fix lane; no
fixable=yes row in DISCLOSE; every rank's column equals the column rule on its cost; every arrow endpoint drawn
and a non-crossing route found.
"""
    S.write_companion(OUTDIR, STEM, __file__, text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
