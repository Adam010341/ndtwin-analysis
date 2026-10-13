#!/usr/bin/env python3
"""
make_arms_grid.py -- fig_t5_arms_by_run: every full live run of the 13 P4 tutorial exercises on
the NDTwin fabric since 2026-09-16, one column per run, two cells per exercise (skeleton arm,
solution arm).

Data (all read at run time, nothing hand-typed):
  * live-p1/runs/<UTC>_06_thirteen/00_table.tsv -- every run directory whose table has the full
    26 rows (partial ONLY= runs, e.g. the ecn-only re-runs of 09-24 and 09-26T062049Z, are
    left out and listed in the .md);
  * the arm reports each table names (column 5): the `code` line of their `ndt status`
    section (the trunk commit the run stood on) and the line "heartbeat started (pid" (the arm
    ran with the veth heartbeat under it);
  * which runs used protobuf 5: the pb5 trial journal (phase 3 = 06 on the candidate venv)
    and the migration's live acceptance log, both under
    scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926/pb5-{trial,merge}/.

"As the exercise says" follows live-p1/06_thirteen.sh:107-150: the arm's rc equals the expected
rc (solution 0; skeleton 0, except flowcache and basic_tunnel skeletons 1) and, where 1 is
expected, the verdict starts with "RED ARM".  A verdict starting "ERROR" is drawn as
"no verdict" (the run's teardown failed, TICKET-P3 section 9 rulings 19-20); anything else is
"not as expected".  "No verdict" covers two different things, both named in the .md: the
first run's teardown that did not return the lab (rulings 19-20), and one arm whose
`ndt up` stopped before any packet (basic_tunnel/solution at 09-19T063235Z, ruling 23(2)).

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/p4-tutorials"
    "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_arms_grid.py
"""
import csv
import glob
import os
import re
import sys

import matplotlib

assert matplotlib.__version__.startswith("3.11"), matplotlib.__version__
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["hatch.linewidth"] = 1.2

REPO = os.environ.get("NDTWIN_REPO", "/home/adam/Desktop/NDTwin-Kernel")
RUNS = os.path.join(REPO, "doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs")
INTAKE = os.path.join(REPO, "scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926")
PB5_JOURNAL = os.path.join(INTAKE, "pb5-trial/JOURNAL.txt")
PB5_ACCEPT = os.path.join(INTAKE, "pb5-merge/live-accept.log")
CUT = "2026-09-16"

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")
STEM = "fig_t5_arms_by_run"

INK, MUTED, FAINT, RULE = "#1A1A1A", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, WHITE = "#065A82", "#FFFFFF"
OK_C, BAD_C, NONE_EDGE = "#2F7D4F", "#9C3B2E", "#9AA0A5"

# row order = the stage order of the requirements matrix (GAP-ANALYSIS section 6), the same
# order fig_t1b_requirements_matrix_0927 uses, so the two figures read row for row
ORDER = ["basic", "qos", "ecn", "mri", "firewall", "basic_tunnel", "source_routing", "calc",
         "link_monitor", "load_balance", "multicast", "p4runtime", "flowcache"]
ARMS = ["skeleton", "solution"]


def die(msg):
    raise SystemExit(f"make_arms_grid: {msg}")


def expected_rc(ex, which):
    if which == "solution":
        return 0
    return 1 if ex in ("flowcache", "basic_tunnel") else 0


def classify(ex, which, rc, verdict):
    if verdict.startswith("ERROR"):
        return "none"
    want = expected_rc(ex, which)
    if rc != want:
        return "bad"
    if want == 1 and not verdict.startswith("RED ARM"):
        return "bad"
    if want == 0 and not verdict.startswith("PASS"):
        return "bad"
    return "ok"


def code_of(report):
    with open(report, encoding="utf-8", errors="replace") as f:
        for ln in f:
            m = re.match(r"^\s+code\s+([0-9a-f]{7,40})\b", ln)
            if m:
                return m.group(1)
    return None


def heartbeat_in(report):
    with open(report, encoding="utf-8", errors="replace") as f:
        return any("heartbeat started (pid" in ln for ln in f)


def pb5_runs():
    """UTC stamps (YYYY-MM-DDTHHMMSSZ) of the 06 runs whose proxy ran on protobuf 5."""
    out = set()
    with open(PB5_JOURNAL) as f:
        for ln in f:
            m = re.match(r"^(\d{4}-\d\d-\d\d)T(\d\d):(\d\d):(\d\d)Z phase3 start: 06 on venv-cand", ln)
            if m:
                out.add(f"{m.group(1)}T{m.group(2)}{m.group(3)}{m.group(4)}Z")
    with open(PB5_ACCEPT) as f:
        for ln in f:
            m = re.search(r"06 run dir: .*/runs/(\S+)_06_thirteen", ln)
            if m:
                out.add(m.group(1))
    if len(out) != 2:
        die(f"expected two protobuf-5 runs (trial + acceptance), found {sorted(out)}")
    return out


def load_runs():
    runs = []
    for d in sorted(glob.glob(os.path.join(RUNS, "*_06_thirteen"))):
        stamp = os.path.basename(d).split("_")[0]
        if stamp[:10] < CUT:
            continue
        tsv = os.path.join(d, "00_table.tsv")
        with open(tsv, newline="") as f:
            rows = list(csv.DictReader(f, delimiter="\t"))
        if len(rows) != 26:
            print(f"[skip] {os.path.basename(d)}: {len(rows)} rows (partial run)")
            continue
        cells, codes, hb = {}, set(), 0
        for r in rows:
            ex, which, rc, verdict, report = (r["exercise"], r["which"], int(r["rc"]),
                                              r["verdict"], r["report"])
            if ex not in ORDER or which not in ARMS:
                die(f"{tsv}: unknown arm {ex}/{which}")
            cls = classify(ex, which, rc, verdict)
            h = False
            if os.path.isfile(report):
                c = code_of(report)
                if c:
                    codes.add(c)
                h = heartbeat_in(report)
            hb += h
            cells[(ex, which)] = (cls, h, rc, verdict)
        if len(cells) != 26:
            die(f"{tsv}: {len(cells)} distinct arms")
        if not codes:
            die(f"{tsv}: no arm report names the code it ran on")
        # the checkout is shared: trunk can move during a 25-minute run (09-19T083257Z did),
        # so a run may name more than one commit; all of them are listed in the .md
        runs.append(dict(stamp=stamp, dir=d, cells=cells, code="+".join(sorted(codes)), hb=hb))
    return runs


def main():
    runs = load_runs()
    pb5 = pb5_runs()
    for r in runs:
        r["pb5"] = r["stamp"] in pb5
    if not pb5 <= {r["stamp"] for r in runs}:
        die(f"a protobuf-5 run is not among the full runs: {sorted(pb5)}")
    for r in runs:
        n_ok = sum(1 for v in r["cells"].values() if v[0] == "ok")
        r["n_ok"] = n_ok
        print(f"[run] {r['stamp']} code {r['code']} as-expected {n_ok}/26 "
              f"heartbeat-arms {r['hb']} pb5 {r['pb5']}")
        for (ex, which), (cls, h, rc, v) in r["cells"].items():
            if cls != "ok":
                print(f"        {cls:4s} {ex}/{which} rc {rc} {v}")
    if runs[-1]["n_ok"] != 26:
        die("the newest full run is not 26/26 -- the figure's story would be wrong")

    # ---------------------------------------------------------------- draw
    n = len(runs)
    cw, gap, ch = 0.36, 0.30, 0.34        # cell width, gap between runs, cell height (inches)
    left, top, right, bottom = 2.25, 1.75, 0.35, 1.25
    grid_w = n * (2 * cw + gap) - gap
    W = left + grid_w + right
    H = top + len(ORDER) * ch + bottom
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")

    fill = {"ok": OK_C, "bad": BAD_C, "none": WHITE}
    for j, r in enumerate(runs):
        x0 = left + j * (2 * cw + gap)
        for i, ex in enumerate(ORDER):
            y = top + i * ch
            for k, which in enumerate(ARMS):
                cls, h, _rc, _v = r["cells"][(ex, which)]
                x = x0 + k * cw
                ax.add_patch(Rectangle((x + 0.02, y + 0.03), cw - 0.04, ch - 0.06,
                                       facecolor=fill[cls],
                                       edgecolor=NONE_EDGE if cls == "none" else fill[cls],
                                       hatch="////" if cls == "none" else None, lw=0.8))
                if h:
                    ax.plot([x + cw / 2], [y + ch / 2], "o", ms=3.2, color=WHITE, zorder=5)
        # run label (UTC, as in the raw directory names)
        s = r["stamp"]
        ax.text(x0 + cw, top - 0.42, f"{s[5:10]}", ha="center", va="bottom", fontsize=12,
                color=INK)
        ax.text(x0 + cw, top - 0.40, f"{s[11:13]}:{s[13:15]}", ha="center", va="top",
                fontsize=10.5, color=MUTED)
        # count, the one value label per column
        ax.text(x0 + cw, top + len(ORDER) * ch + 0.12, f"{r['n_ok']}", ha="center", va="top",
                fontsize=14, color=INK if r["n_ok"] == 26 else BAD_C, fontweight="bold")
        if r["pb5"]:
            ax.text(x0 + cw, top - 0.78, "protobuf 5", ha="center", va="bottom", fontsize=10.5,
                    color=ACCENT, fontweight="bold")
    ax.text(left - 0.15, top + len(ORDER) * ch + 0.12, "of 26", ha="right", va="top",
            fontsize=12, color=MUTED)
    for i, ex in enumerate(ORDER):
        ax.text(left - 0.15, top + i * ch + ch / 2, ex, ha="right", va="center", fontsize=13,
                color=INK)
    ax.text(left - 0.15, top - 0.42, "run (UTC)", ha="right", va="bottom", fontsize=11,
            color=MUTED)
    ax.text(left - 0.15, top - 0.12, "skeleton | solution", ha="right", va="bottom",
            fontsize=10.5, color=MUTED)

    ax.text(0.35, 0.45, "13 exercises × 2 arms, every full run", fontsize=20,
            fontweight="bold", color=INK, ha="left", va="center")
    # legend, bottom row
    ly = H - 0.38
    lx = left
    items = [("ok", "as the exercise says"), ("bad", "not as expected"),
             ("none", "no verdict")]
    step = (grid_w - 0.3) / 4.0
    for cls, label in items:
        ax.add_patch(Rectangle((lx, ly - 0.12), 0.30, 0.24, facecolor=fill[cls],
                               edgecolor=NONE_EDGE if cls == "none" else fill[cls],
                               hatch="////" if cls == "none" else None, lw=0.8))
        ax.text(lx + 0.40, ly, label, ha="left", va="center", fontsize=12, color=MUTED)
        lx += step
    ax.add_patch(Rectangle((lx, ly - 0.12), 0.30, 0.24, facecolor=OK_C, edgecolor=OK_C))
    ax.plot([lx + 0.15], [ly], "o", ms=3.2, color=WHITE)
    ax.text(lx + 0.40, ly, "heartbeat running", ha="left", va="center", fontsize=12,
            color=MUTED)

    os.makedirs(HIRES, exist_ok=True)
    for ext in ("pdf", "png", "svg"):
        kw = {"dpi": 300} if ext == "png" else {}
        fig.savefig(os.path.join(OUTDIR, f"{STEM}.{ext}"), facecolor=WHITE, **kw)
    fig.savefig(os.path.join(HIRES, f"{STEM}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"[out] {STEM}  {W:.2f}x{H:.2f} in  ({len(runs)} runs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
