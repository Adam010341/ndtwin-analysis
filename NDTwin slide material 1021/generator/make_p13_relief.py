#!/usr/bin/env python3
"""
make_p13_relief.py -- handson/fig_p13_relief: time to relief after the trigger, two titled panels.  Page P13
of the 1021 deck.  Evidence class: RAN (both panels; every dot is one archived trial).

Left panel "Built-in reroute, no app (link cut)": H/controls.tsv (columns arm, data_plane, trial, cut_time,
first_reply_after_cut, gap_ms, stayed_up, notes; the verdict is the `verdict=` token of `notes`).  One strip
per (arm, plane): NDTwin OVS, NDTwin bmv2, DIY Ryu STP sample.  Dot = trial at gap_ms/1000 s, red cross in the
"failed" zone for NOT_RECOVERED.  Two kinds of designed RED controls are not drawn and must all be NOT_RECOVERED:
the NDTwin `red-bothpaths` rows (both uplinks cut, no path exists) and the `diy-static` rows (static routes that
never recompute).
Right panel "Congestion relief by the app": H/congestion/results.tsv, rows ndtwin-app and diy-app.  Strips
NDTwin OVS, NDTwin bmv2, DIY OVS.  Dot = PASS (or RED_LATE) trial at time_to_relief_s; red cross in the "failed"
zone for every other RED_* verdict.  The scripted reference movers (the *-ctl rows, ~22 s by the harness's own
schedule) are NOT drawn: they are checked, not plotted.
Median label per strip: over the recovered / held-relief trials (PREREG section 9).

Stops with a named reason if: a file lacks a column; a strip has a different number of trials than planned
(control plan read from run_controls.sh: `trials ndtwin "$dp" N`, `trials "$tag" ovs N`; app plan read from
PREREG.txt section 7: "n = N per arm x plane"); a row's verdict is INVALID_* / SUDO_REFUSED / ANALYZER_FAILED /
PRECUT_DEAD; a PASS row has no numeric time_to_relief_s; a *-ctl row of results.tsv does not carry the verdict
the pre-registration expects for its control; a designed red control (red-bothpaths, diy-static) recovered or
has a different number of trials than planned.

[Co-developed with claude code -- Adam]
"""
import csv
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle_1021 as S  # noqa: E402
from figstyle_1021 import ACCENT, BODY, FAINT, INK, MUTED, PANEL, RULE, WHITE, plt  # noqa: E402,F401
from matplotlib.patches import Rectangle  # noqa: E402

WHO = "make_p13_relief"
STEM = "fig_p13_relief"
TITLE = "Time to relief after the trigger"
H = "/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-10-08_why-ndtwin-handson"
args = sys.argv[1:]


def opt(name, default):
    return args[args.index(name) + 1] if name in args else default


CONTROLS = opt("--controls", os.path.join(H, "controls.tsv"))
RESULTS = opt("--results", os.path.join(H, "congestion", "results.tsv"))
PLAN = opt("--plan", os.path.join(H, "run_controls.sh"))
PREREG = opt("--prereg", os.path.join(H, "congestion", "PREREG.txt"))
OUTDIR = opt("--out", os.path.join(S.DECK, "figures", "handson"))

RED = "#9C3B2E"            # the deck's defect red (build_deck_1021.js GLYPH "⚠")
DIY_C = MUTED
BAD_VERDICT = re.compile(r"^(INVALID_\w*|SUDO_REFUSED|ANALYZER_FAILED|PRECUT_DEAD)$")
CTL_EXPECT = {"none": "RED_NO_ACTION", "good": "PASS", "wrongflow": "RED_WRONG_FLOW",
              "wrongpath": "RED_STILL_CONGESTED", "busypath": "RED_STILL_CONGESTED", "flap": "RED_FLAPPED",
              "late": "RED_LATE"}

# (key in the file, strip name on the canvas, colour)
LEFT = [(("ndtwin", "ovs"), "NDTwin, OVS", ACCENT), (("ndtwin", "bmv2"), "NDTwin, bmv2", ACCENT),
        (("diy-stp", "ovs"), "DIY, Ryu STP sample", DIY_C)]
RED_CONTROL_ARMS = {"diy-static"}      # designed RED controls (never recompute): checked, not drawn
RIGHT = [(("ndtwin-app", "ovs"), "NDTwin app, OVS", ACCENT), (("ndtwin-app", "bmv2"), "NDTwin app, bmv2", ACCENT),
         (("diy-app", "ovs"), "DIY app, OVS", DIY_C)]


def read_tsv(path, need, who):
    if not os.path.exists(path):
        S.die(WHO, f"{who} not found: {path}")
    with open(path, encoding="utf-8") as f:
        rd = csv.DictReader(f, delimiter="\t")
        miss = [c for c in need if c not in (rd.fieldnames or [])]
        if miss:
            S.die(WHO, f"{who} lacks column(s) {miss}; columns are {rd.fieldnames}")
        return list(rd)


def plans():
    t = open(PLAN, encoding="utf-8").read()
    a = re.search(r'trials ndtwin "\$dp" (\d+)', t)
    b = re.search(r'trials "\$tag" ovs (\d+)', t)
    if not (a and b):
        S.die(WHO, f"cannot read the planned trial counts from {PLAN}")
    p = open(PREREG, encoding="utf-8").read()
    c = re.search(r"n = (\d+) per arm x plane", p)
    if not c:
        S.die(WHO, f"cannot read the app trial count (n = N per arm x plane) from {PREREG}")
    return int(a.group(1)), int(b.group(1)), int(c.group(1))


def load():
    n_ndt, n_diy, n_app = plans()
    # ---- left: built-in reroute controls
    crow = read_tsv(CONTROLS, ["arm", "data_plane", "trial", "gap_ms", "stayed_up", "notes"], "controls.tsv")
    left = {k: [] for k, _, _ in LEFT}
    negctl = []
    for r in crow:
        m = re.search(r"verdict=(\w+)", r["notes"])
        if not m:
            S.die(WHO, f"controls.tsv row {r['arm']}/{r['data_plane']}/{r['trial']} has no verdict= in notes")
        v = m.group(1)
        if BAD_VERDICT.match(v):
            S.die(WHO, f"controls.tsv row {r['arm']}/{r['data_plane']}/{r['trial']} is {v} (an INVALID_* row "
                       f"is not a result)")
        if r["trial"] == "red-bothpaths" or r["arm"] in RED_CONTROL_ARMS:
            if v != "NOT_RECOVERED":
                S.die(WHO, f"designed red control {r['arm']}/{r['data_plane']}/{r['trial']} is {v}, must be NOT_RECOVERED")
            negctl.append(r)
            continue
        k = (r["arm"], r["data_plane"])
        if k not in left:
            S.die(WHO, f"controls.tsv has a strip {k} the page does not draw")
        x = float(r["gap_ms"]) / 1000.0 if v == "RECOVERED" else None
        left[k].append({"trial": r["trial"], "v": v, "x": x})
    for k, name, _ in LEFT:
        want = n_ndt if k[0] == "ndtwin" else n_diy
        if len(left[k]) != want:
            S.die(WHO, f"strip {name!r} has {len(left[k])} trials, the plan is {want} (run_controls.sh)")
    for arm in RED_CONTROL_ARMS:
        got = sum(1 for r in negctl if r["arm"] == arm)
        if got != n_diy:
            S.die(WHO, f"designed red control {arm} has {got} trials, the plan is {n_diy} (run_controls.sh)")
    # ---- right: app trials, and the scripted controls checked against the pre-registration
    rrow = read_tsv(RESULTS, ["arm", "data_plane", "trial", "variant", "app", "verdict", "time_to_relief_s", "raw"],
                    "results.tsv")
    right = {k: [] for k, _, _ in RIGHT}
    nctl = 0
    for r in rrow:
        v = r["verdict"]
        tag = f"{r['arm']}/{r['data_plane']}/{r['trial']}"
        if BAD_VERDICT.match(v):
            S.die(WHO, f"results.tsv row {tag} is {v} (an INVALID_* row is not a result; PREREG section 7 reruns it)")
        if r["arm"].endswith("-ctl"):
            kind = r["trial"].split("-")[0]
            if kind not in CTL_EXPECT:
                S.die(WHO, f"results.tsv control row {tag}: unknown control {kind!r}")
            if v != CTL_EXPECT[kind]:
                S.die(WHO, f"results.tsv control row {tag} is {v}, pre-registered {CTL_EXPECT[kind]}")
            nctl += 1
            continue
        k = (r["arm"], r["data_plane"])
        if k not in right:
            S.die(WHO, f"results.tsv has a strip {k} the page does not draw")
        x = None
        if v in ("PASS", "RED_LATE"):
            try:
                x = float(r["time_to_relief_s"])
            except ValueError:
                S.die(WHO, f"results.tsv row {tag} is {v} without a numeric time_to_relief_s")
        right[k].append({"trial": r["trial"], "v": v, "x": x, "app": r["app"], "raw": r["raw"]})
    for k, name, _ in RIGHT:
        if len(right[k]) != n_app:
            S.die(WHO, f"strip {name!r} has {len(right[k])} trials, the plan is {n_app} (PREREG section 7)")
    return left, right, negctl, nctl, (n_ndt, n_diy, n_app)


def nice_max(v):
    for s in (10, 15, 20, 30, 40, 60, 80, 100, 120, 180, 240):
        if v * 1.12 <= s:
            return s
    return 300


def ticks(xmax):
    step = {10: 2, 15: 5, 20: 5, 30: 10, 40: 10, 60: 20, 80: 20, 100: 20, 120: 30, 180: 30, 240: 60}.get(xmax, 60)
    return list(range(0, xmax + 1, step))


def median(xs):
    return statistics.median(xs) if xs else None


def fmt_s(v):
    return f"{v:.0f} s" if abs(v - round(v)) < 0.05 else f"{v:.1f} s"


def panel(ax, fig, x0, x1, ytop, strips, data, ptitle):
    """x0..x1: inches of the panel; strip labels on the left of the plot area."""
    lab_w = 2.05
    px0, px1 = x0 + lab_w, x1 - 0.95           # plot area
    fz0, fz1 = x1 - 0.72, x1 - 0.12            # 'failed' zone
    xs = [p["x"] for k, _, _ in strips for p in data[k] if p["x"] is not None]
    has_fail = any(p["x"] is None for k, _, _ in strips for p in data[k])
    if not has_fail:
        px1 = x1 - 0.25                        # no 'failed' zone on a panel without a failed trial
    xmax = nice_max(max(xs) if xs else 10)
    sx = lambda v: px0 + (px1 - px0) * v / xmax            # noqa: E731
    pitch = 0.92
    y0 = ytop + 0.55
    ybot = y0 + pitch * len(strips) - 0.25
    ax.text(x0, ytop, ptitle, fontsize=15, fontweight="bold", color=INK, va="center")
    # grid + axis
    for t in ticks(xmax):
        ax.plot([sx(t), sx(t)], [y0 - 0.35, ybot], color=RULE, lw=0.8, zorder=1)
        ax.text(sx(t), ybot + 0.18, str(t), ha="center", va="center", fontsize=11, color=BODY)
    if has_fail:
        ax.add_patch(Rectangle((fz0, y0 - 0.35), fz1 - fz0, ybot - y0 + 0.35, facecolor=PANEL, edgecolor=RULE,
                               lw=0.8, zorder=0))
        ax.text((fz0 + fz1) / 2, ybot + 0.18, "failed", ha="center", va="center", fontsize=11, color=BODY)
    ax.plot([px0, px1], [ybot, ybot], color=FAINT, lw=1.0, zorder=2)
    ax.text((px0 + px1) / 2, ybot + 0.50, "seconds after the trigger", ha="center", va="center", fontsize=12,
            color=BODY)
    out = []
    for i, (k, name, col) in enumerate(strips):
        y = y0 + i * pitch
        ax.text(px0 - 0.15, y, name, ha="right", va="center", fontsize=12.5, color=INK, fontweight="bold")
        ax.plot([px0, px1], [y, y], color=RULE, lw=0.6, ls=(0, (2, 3)), zorder=1)
        pts = sorted([p for p in data[k] if p["x"] is not None], key=lambda p: p["x"])
        # stack dots that would touch (closer than 0.13 in) vertically, alternating above / below
        groups, cur = [], []
        for p in pts:
            if cur and sx(p["x"]) - sx(cur[0]["x"]) > 0.13:
                groups.append(cur)
                cur = []
            cur.append(p)
        if cur:
            groups.append(cur)
        for g in groups:
            for j, p in enumerate(g):
                off = ((j + 1) // 2) * 0.12 * (1 if j % 2 else -1)
                ax.scatter([sx(p["x"])], [y + off], s=95, color=col, edgecolors=WHITE, linewidths=1.2, zorder=5)
        fails = [p for p in data[k] if p["x"] is None]
        for j, p in enumerate(fails):
            off = ((j + 1) // 2) * 0.19 * (1 if j % 2 else -1)
            ax.scatter([(fz0 + fz1) / 2], [y + off], s=110, marker="x", color=RED, linewidths=2.6, zorder=5)
        med = median([p["x"] for p in pts])
        if med is not None:
            ax.plot([sx(med), sx(med)], [y - 0.30, y + 0.30], color=INK, lw=2.0, zorder=6)
            ax.text(sx(med) + 0.07, y - 0.33, fmt_s(med), ha="left", va="center", fontsize=12, color=INK,
                    fontweight="bold", zorder=7)
        out.append((name, len(data[k]), len(pts), len(fails), med))
    return out, xmax, ybot


def main():
    left, right, negctl, nctl, plan = load()
    W, Hh = 13.33, 5.7
    fig, ax = S.new_canvas(W, Hh)
    S.title(ax, TITLE, W)
    sl, xl, yb1 = panel(ax, fig, 0.45, 6.75, 1.25, LEFT, left, "Built-in reroute, no app (link cut)")
    sr, xr, yb2 = panel(ax, fig, 7.15, 12.95, 1.25, RIGHT, right, "Congestion relief by the app")
    # key, one line
    ky = max(yb1, yb2) + 0.98
    ax.scatter([0.6], [ky], s=95, color=FAINT, edgecolors=WHITE, linewidths=1.2)
    ax.text(0.75, ky, "trial", va="center", fontsize=11, color=BODY)
    ax.scatter([1.45], [ky], s=110, marker="x", color=RED, linewidths=2.6)
    ax.text(1.6, ky, "failed trial", va="center", fontsize=11, color=BODY)
    ax.plot([2.75, 2.75], [ky - 0.15, ky + 0.15], color=INK, lw=2.0)
    ax.text(2.88, ky, "median", va="center", fontsize=11, color=BODY)
    if ky + 0.3 > Hh:
        S.die(WHO, f"layout: the key at {ky:.2f} in does not fit a {Hh} in canvas")
    S.save_all(fig, OUTDIR, STEM)
    for name, n, nd, nf, med in sl + sr:
        print(f"[strip] {name}: {n} trials, {nd} dots, {nf} crosses, median {med}")
    print(f"[out] {STEM}: left x 0..{xl} s, right x 0..{xr} s; {len(negctl)} designed red control rows not drawn; "
          f"{nctl} scripted controls checked against the pre-registration")

    def rows_md(strips, data, kind):
        out = []
        for k, name, _ in strips:
            for p in data[k]:
                sec = "" if p["x"] is None else "%.1f" % p["x"]
                out.append(f"| {kind} | {name} | {p['trial']} | {p['v']} | {sec} |")
        return out

    tbl = ["| panel | strip | trial | verdict | seconds |", "|---|---|---|---|---|"]
    tbl += rows_md(LEFT, left, "left") + rows_md(RIGHT, right, "right")
    meds = "\n".join(f"- {name}: {n} trials, {nd} drawn as dots, {nf} as crosses; median "
                     f"{'n/a (no recovery)' if med is None else fmt_s(med)}" for name, n, nd, nf, med in sl + sr)
    text = f"""# `{STEM}` -- {TITLE} (page P13)

[Co-developed with claude code -- Adam]

Evidence class: **RAN** (both panels). Every mark is one archived trial; nothing is modelled.

## Data source

- Left panel: `{CONTROLS}` sha256 `{S.sha16(CONTROLS)}...` (git commit dcff37b6 in the kernel repo, local only).
  Planned counts read from `{PLAN}` sha256 `{S.sha16(PLAN)}...`: NDTwin {plan[0]} per plane, DIY {plan[1]} per
  baseline. {len(negctl)} rows are designed RED controls and are not drawn: the NDTwin `red-bothpaths` rows (both
  uplinks of s1 cut, no path exists) and the `diy-static` rows (DIY static routes: 3/3 not recovered, by design --
  static routes never recompute). Each is NOT_RECOVERED; the generator stops otherwise.
- Right panel: `{RESULTS}` sha256 `{S.sha16(RESULTS)}...` (kernel commits 80a4e29f and 9335b189, local only), rows
  `ndtwin-app` and `diy-app`; planned {plan[2]} per arm x plane (`{PREREG}` section 7). The {nctl} `*-ctl` rows
  (scripted reference movers) are checked against the pre-registered verdicts and NOT drawn: their ~22 s time to
  relief is the harness's own schedule (act at t0+20 s plus a 2 s look), not a property of any controller.
- Binary identity, hashed BEFORE the trials (identity files written 02:47Z for the reroute controls,
  ../raw/identity.20261008T104711.txt, and 03:43Z for the congestion runs, raw/identity.20261008T114343.txt; raw
  trees archived in the kernel repo's audit-raw branch, commit ed24e5e5); per-trial tree state in
  raw/ndt_status_up_*.txt lines 9-12 (HEAD + uncommitted set): kernel build/bin/ndtwin_kernel sha256
  6fc7e4187df49ee9 (built 2026-10-03, no commit stamp; the P4 proxy and NDTwin's Ryu app are Python run from the
  shared tree), bmv2-fast simple_switch_grpc sha256 3ff54b5c1901c9d3, P4 pipeline json sha256
  0b19d789d74fc996, stock Ryu 4.34, Mininet 2.3.0, OVS 3.3.9, iperf3 3.16. App dirs: ndtwin_app controller.py
  sha256 8f861d3c, run.sh 4672a502 (same bytes on both planes); diy_app app.py sha256 3a4f76c6.

## Encoding

- x: seconds after the trigger. Left: after the link cut (gap_ms / 1000: first ping reply sent after the cut).
  Right: after congestion start (time_to_relief_s: first held GOOD bin, checker definition PREREG section 6).
  The two panels have their own x scales (left 0..{xl} s, right 0..{xr} s).
- Dot = trial; dots closer than 0.13 in are stacked vertically (several trials share one value).
- Red cross in the grey "failed" zone: a relief that did not hold (right, RED_FLAPPED); a cross has no x value.
  A panel without a failed trial has no "failed" zone (the left panel, now that the designed red controls are
  not drawn).
- Median bar + label: over the recovered / held-relief trials of the strip.

## Values

{meds}

{chr(10).join(tbl)}

## Reconciliation

- Left, NDTwin: comparable with doc/audit/2026-08-17_p4-vs-ovs-matched-topology/REPORT.md (same cell, n=10 per
  plane, all recovered). Mean to mean: OVS {statistics.mean(p["x"] for p in left[("ndtwin", "ovs")]):.1f} s now
  vs 15.7 s then; bmv2 {statistics.mean(p["x"] for p in left[("ndtwin", "bmv2")]):.1f} s now vs 13.7 s then.
  This run cut both directions of the on-path s1 uplink for h1->h3 at 100 pings/s; that one cut one direction for
  h1->h2 at 5 pings/s. Same order of magnitude, all recovered again: an update, not a reversal; the ~2-3 s
  higher means are not explained (not investigated).
- Right: no earlier app-level congestion result exists; the scripted `good` controls (22 s on every plane) bound
  the harness side only.
"""
    S.write_companion(OUTDIR, STEM, __file__, text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
