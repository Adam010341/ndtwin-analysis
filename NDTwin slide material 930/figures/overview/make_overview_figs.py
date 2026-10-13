#!/usr/bin/env python3
"""
make_overview_figs.py -- the two overview figures of the 2026-09-30 report.

    fig_o1_since_0916   what landed between 2026-09-16 and 2026-09-30, one lane per theme
    fig_o2_thirteen     exercises with BOTH arms as the exercise says, per full live run

Data (all read at run time; nothing on either canvas is a hand-typed measurement):
  * fig_o1: every merge/commit date is `git show -s --format=%cI <sha>` in the NDTwin-Kernel
    checkout (read-only git); every live-run date is the UTC stamp in the run directory's name
    under doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/ or
    doc/audit/2026-09-19_telemetry-three-groups/raw/.  Each milestone is asserted: a merge has
    two parents and its subject names the branch; a live run's directory exists, names the
    commit it stood on (01_binaries.txt "repo HEAD", or the arm reports' `ndt status` code
    line), and holds the files the label claims (H1 30_cycles.tsv, H3 64_cycle.tsv, H4
    82_flowentry_*.code, H5 51_06.txt's PASS line; 13/13 is recomputed from 00_table.tsv).
  * fig_o2: every live-p1/runs/<UTC>_06_thirteen/00_table.tsv since 2026-09-16 with the full
    26 rows (partial ONLY= runs are skipped and printed).  "As the exercise says" is the rule
    of live-p1/06_thirteen.sh:107-150, copied (not imported) from
    ../p4-tutorials/make_arms_grid.py classify(): solution rc 0 and PASS; skeleton rc 0 and
    PASS, except flowcache and basic_tunnel skeletons, rc 1 and a verdict starting "RED ARM";
    a verdict starting "ERROR" is "no verdict".  An exercise counts when both arms are "as the
    exercise says".  The 09-08 context point (0 of 13 RUN on the NDTwin fabric -- a different
    quantity from the y axis) is parsed from the 09-16 deck template,
    NDTwin-slide-template-916.md:257, and drawn as a "not run" marker below the scale.

Times are UTC throughout (the run directories are named in UTC; commit dates are converted).

Raw status: every run directory read here is in audit-raw, byte-identical to the working tree:
797c34ab, and its descendant 5cf0364c for the three 09-19 morning 06 runs (052518Z, 063235Z,
083257Z) and their arm reports.  Every run stood on a dirty checkout ("+N file(s)" in its code
line).

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/overview"
    nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_overview_figs.py
"""
import csv
import datetime as dt
import glob
import os
import re
import subprocess
import sys

import matplotlib

assert matplotlib.__version__.startswith("3.11"), matplotlib.__version__
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

REPO = os.environ.get("NDTWIN_REPO", "/home/adam/Desktop/NDTwin-Kernel")
PREP = os.path.join(REPO, "doc/audit/2026-09-04_p4-tutorial-exercise-prep")
RUNS = os.path.join(PREP, "live-p1/runs")
TELE = os.path.join(REPO, "doc/audit/2026-09-19_telemetry-three-groups")
TEMPLATE_916 = ("/home/adam/Desktop/NDTwin slide material/NDTWIN slide material 916/"
                "NDTwin-slide-template-916.md")
TEMPLATE_916_LINE = 257
CUT = "2026-09-16"
REPORT_DAY = dt.datetime(2026, 9, 30, tzinfo=dt.timezone.utc)

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
WARNC, WHITE, GREEN, GREY = "#9C3B2E", "#FFFFFF", "#2F7D4F", "#C9CDD0"
SECOND = "#C0701C"

# row order of fig_t5 / GAP-ANALYSIS section 6 (only used to validate the table's names)
ORDER = ["basic", "qos", "ecn", "mri", "firewall", "basic_tunnel", "source_routing", "calc",
         "link_monitor", "load_balance", "multicast", "p4runtime", "flowcache"]
ARMS = ["skeleton", "solution"]


def die(msg):
    raise SystemExit(f"make_overview_figs: {msg}")


def save(fig, name):
    os.makedirs(HIRES, exist_ok=True)
    for ext in ("pdf", "png", "svg"):
        kw = {"dpi": 300} if ext == "png" else {}
        fig.savefig(os.path.join(OUTDIR, f"{name}.{ext}"), facecolor=WHITE, **kw)
    fig.savefig(os.path.join(HIRES, f"{name}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"[out] {name}.{{pdf,png,svg}} + _hires/{name}.png")


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


# ---------------------------------------------------------------------------
# the 06 table rule, copied from ../p4-tutorials/make_arms_grid.py (not imported)
# ---------------------------------------------------------------------------

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


def read_table(run_dir):
    tsv = os.path.join(run_dir, "00_table.tsv")
    with open(tsv, newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def both_ok(rows, tsv):
    cells = {}
    for r in rows:
        ex, which = r["exercise"], r["which"]
        if ex not in ORDER or which not in ARMS:
            die(f"{tsv}: unknown arm {ex}/{which}")
        cells[(ex, which)] = classify(ex, which, int(r["rc"]), r["verdict"])
    if len(cells) != 26:
        die(f"{tsv}: {len(cells)} distinct arms, not 26")
    return [ex for ex in ORDER if all(cells[(ex, w)] == "ok" for w in ARMS)], cells


def full_runs():
    out = []
    for d in sorted(glob.glob(os.path.join(RUNS, "*_06_thirteen"))):
        stamp = os.path.basename(d).split("_")[0]
        if stamp[:10] < CUT:
            continue
        rows = read_table(d)
        if len(rows) != 26:
            print(f"[skip] {os.path.basename(d)}: {len(rows)} rows (partial run)")
            continue
        exs, cells = both_ok(rows, os.path.join(d, "00_table.tsv"))
        codes = sorted({c for c in (code_of(r["report"]) for r in rows
                                    if os.path.isfile(r["report"])) if c})
        if not codes:
            die(f"{d}: no arm report names the code it ran on")
        out.append(dict(stamp=stamp, dir=d, n=len(exs), exs=exs, cells=cells, codes=codes))
    if not out:
        die("no full 06 runs since the cut")
    return out


def utc_of_stamp(stamp):
    return dt.datetime.strptime(stamp, "%Y-%m-%dT%H%M%SZ").replace(tzinfo=dt.timezone.utc)


# ---------------------------------------------------------------------------
# fig_o1_since_0916
# ---------------------------------------------------------------------------

def git_commit(sha, subject_needle, merge=True):
    out = subprocess.run(["git", "-C", REPO, "show", "-s", "--format=%H%n%cI%n%P%n%s", sha],
                         capture_output=True, text=True, check=True).stdout.splitlines()
    full, cdate, parents, subject = out[0], out[1], out[2].split(), out[3]
    if merge and len(parents) != 2:
        die(f"{sha} is not a merge ({len(parents)} parent(s))")
    if not merge and len(parents) != 1:
        die(f"{sha} was expected to be a plain commit")
    if subject_needle not in subject:
        die(f"{sha} subject no longer names {subject_needle!r}: {subject[:90]}")
    when = dt.datetime.fromisoformat(cdate).astimezone(dt.timezone.utc)
    print(f"[git] {sha} {cdate} -> {when:%Y-%m-%dT%H:%M:%SZ}  {subject[:70]}")
    return when, full


def repo_head(run_dir):
    m = re.search(r"^repo HEAD\s+([0-9a-f]{40})$", read(os.path.join(run_dir, "01_binaries.txt")),
                  re.M)
    if not m:
        die(f"{run_dir}/01_binaries.txt names no repo HEAD")
    return m.group(1)


def live_dir(name, base=RUNS):
    d = os.path.join(base, name)
    if not os.path.isdir(d):
        die(f"no run directory {d}")
    return d, utc_of_stamp(name.split("_")[0])


def milestones(runs):
    """[(lane, kind, when, label, label_side)] -- label None = the marker joins the previous
    label (a merge and the live run on it minutes later)."""
    ms = []
    by_stamp = {r["stamp"]: r for r in runs}

    # --- P4 exercises: the first full run with 13/13 both arms
    first13 = next((r for r in runs if r["n"] == 13), None)
    if first13 is None or first13["stamp"] != "2026-09-19T144328Z":
        die(f"the first 13/13 full run is {first13 and first13['stamp']}, not 09-19T144328Z")
    if first13["codes"] != [c[:8] for c in ["f3b6d09c"]]:
        die(f"09-19T144328Z stood on {first13['codes']}, not f3b6d09c")
    ms.append(("P4 exercises", "live", utc_of_stamp(first13["stamp"]), "first 13/13", "above"))

    # --- P4 exercises: the ecn instrument fix, then 13/13 again on it
    t, full = git_commit("0c96c1d0", "fix/ecn-probe-power")
    r = by_stamp.get("2026-09-24T185505Z")
    if r is None or r["n"] != 13 or r["codes"] != [full[:8]]:
        die(f"09-24T185505Z is not a 13/13 full run on 0c96c1d0: {r and (r['n'], r['codes'])}")
    ms.append(("P4 exercises", "merge", t, "ecn probe fix, 13/13", "above"))
    ms.append(("P4 exercises", "live", utc_of_stamp(r["stamp"]), None, None))

    # --- foreign-P4 API: the app package tools and `ndt up p4 --app` (09-17), each switch
    # running the program its package names (09-18).  Not on the orchestrator's candidate list;
    # added because trunk's busiest days (09-17/18) would otherwise read as empty.
    t, _ = git_commit("386eb20c", "feat/p4-app-package-tools-0917")
    ms.append(("foreign-P4 API", "merge", t, "convert · pre-flight · --app", "above"))
    t, _ = git_commit("54f69d15", "feat/p4-app-package-ndt-0917")
    ms.append(("foreign-P4 API", "merge", t, None, None))
    t, _ = git_commit("b392f111", "feat/p4-app-package-p2-core-0918")
    ms.append(("foreign-P4 API", "merge", t, "own program per switch", "below"))

    # --- foreign-P4 API: roles first cut, merged and run live (07) minutes later
    t, full = git_commit("572d9462", "feat/p4-roles-first-cut")
    d, t07 = live_dir("2026-09-24T160256Z_07_roles_basic")
    if repo_head(d) != full:
        die(f"{d} did not stand on 572d9462")
    for f in ("12_preflight_basic_roles.txt", "32_pingall.txt"):
        if not os.path.isfile(os.path.join(d, f)):
            die(f"{d} has no {f}")
    ms.append(("foreign-P4 API", "merge", t, "roles first cut", "above"))
    ms.append(("foreign-P4 API", "live", t07, None, None))

    # --- heartbeat: segment W merged, H1-H4 live on it, H5 later the same day
    t, full = git_commit("cafd518a", "feat/p4-heartbeat-w")
    d, th = live_dir("2026-09-26T152605Z_08_heartbeat")
    if repo_head(d) != full:
        die(f"{d} did not stand on cafd518a")
    need = ["30_cycles.tsv", "64_cycle.tsv", "82_flowentry_add.code"]
    for f in need:
        if not os.path.isfile(os.path.join(d, f)):
            die(f"{d} has no {f} (H1 / H3 / H4)")
    ms.append(("heartbeat", "merge", t, "segment W, live H1–H5", "above"))
    ms.append(("heartbeat", "live", th, None, None))
    d5, t5 = live_dir("2026-09-26T172912Z_08_heartbeat")
    if "PASS 06_thirteen -- 26 arm(s)" not in read(os.path.join(d5, "51_06.txt")):
        die(f"{d5}/51_06.txt has no PASS line for the 06 it ran under the heartbeat")
    ms.append(("heartbeat", "live", t5, None, None))

    # --- ndt serve
    t, _ = git_commit("48209682", "feat/ndt-serve-0924")
    ms.append(("ndt serve", "merge", t, "local API merged", "above"))
    t, _ = git_commit("f186ce98", "feat/ndt-serve-gui-0927")
    ms.append(("ndt serve", "merge", t, "own page (GUI v1)", "below"))

    # --- telemetry: link-level telemetry for any program (09-18), then the three-group campaign
    t, _ = git_commit("f5ad6890", "feat/p3-link-telemetry-0919")
    ms.append(("telemetry", "merge", t, "link-level telemetry", "below"))
    # --- telemetry: the three-group campaign
    d, tt = live_dir("2026-09-19T115737Z_full", base=os.path.join(TELE, "raw"))
    if "2026-09-19T115737Z_full" not in read(os.path.join(TELE, "FINDINGS.md")):
        die("FINDINGS.md no longer names run 2026-09-19T115737Z_full")
    ms.append(("telemetry", "live", tt, "three-group campaign", "above"))

    # --- engineering: protobuf 5, then 13/13 on it; main only through PRs
    t, full = git_commit("5dc7fc9a", "fix/p4proxy-protobuf5")
    r = by_stamp.get("2026-09-27T074635Z")
    if r is None or r["n"] != 13 or r["codes"] != [full[:8]]:
        die(f"09-27T074635Z is not a 13/13 full run on 5dc7fc9a: {r and (r['n'], r['codes'])}")
    ms.append(("engineering", "merge", t, "protobuf 5, 13/13", "above"))
    ms.append(("engineering", "live", utc_of_stamp(r["stamp"]), None, None))
    t, _ = git_commit("3d740be0", "main is updated only through squash-merged PRs", merge=False)
    ms.append(("engineering", "merge", t, "main via PRs only", "below"))

    lo = dt.datetime.fromisoformat(CUT + "T00:00:00+00:00")
    for lane, kind, when, label, side in ms:
        if not (lo <= when < REPORT_DAY):
            die(f"{label or lane} at {when} is outside {CUT} .. report day")
    return ms


def fig_o1(runs):
    ms = milestones(runs)
    lanes = ["P4 exercises", "foreign-P4 API", "heartbeat", "ndt serve", "telemetry",
             "engineering"]
    t0 = dt.datetime(2026, 9, 16, tzinfo=dt.timezone.utc)

    def x(t):
        return (t - t0).total_seconds() / 86400.0

    fig = plt.figure(figsize=(13.33, 6.2))
    ax = fig.add_axes([0.165, 0.13, 0.815, 0.70])
    xmax = x(REPORT_DAY) + 1.0
    ax.set_xlim(0, xmax)
    ax.set_ylim(len(lanes) - 0.35, -0.75)
    for i, lane in enumerate(lanes):
        ax.axhline(i, color=RULE, lw=1.0, zorder=0)
        ax.text(-0.25, i, lane, ha="right", va="center", fontsize=14, color=INK,
                transform=ax.transData)
    # day boundaries, faint; day labels centred under each day
    for k in range(int(xmax) + 1):
        ax.axvline(k, color="#EDEDED", lw=0.8, zorder=0)
    days = [t0 + dt.timedelta(days=k) for k in range(int(xmax))]
    ax.set_xticks([k + 0.5 for k in range(len(days))])
    ax.set_xticklabels([f"{d:%m-%d}" for d in days], fontsize=11, color=MUTED)
    for lab, d in zip(ax.get_xticklabels(), days):
        if d.date() == REPORT_DAY.date():
            lab.set_color(ACCENT)
            lab.set_fontweight("bold")
    ax.tick_params(axis="x", length=0, pad=6)
    ax.set_yticks([])
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.set_xlabel("date (UTC)", fontsize=12.5, color=MUTED, labelpad=8)

    for lane, kind, when, label, side in ms:
        y = lanes.index(lane)
        xv = x(when)
        if kind == "merge":
            ax.plot([xv], [y], marker="D", ms=13, mfc=WHITE, mec=ACCENT, mew=2.2, zorder=4)
        else:
            ax.plot([xv], [y], marker="o", ms=8.5, mfc=GREEN, mec=GREEN, zorder=5)
        if label:
            dy = -0.30 if side == "above" else 0.34
            ax.text(xv, y + dy, label, ha="center", va="bottom" if side == "above" else "top",
                    fontsize=12.5, color=BODY, zorder=6)
        print(f"[o1] {lane:15s} {kind:5s} {when:%m-%d %H:%M}Z  x={xv:6.3f}  {label or ''}")

    fig.text(0.02, 0.935, "What landed since the 09-16 report", fontsize=22,
             fontweight="bold", color=INK, ha="left", va="center")
    handles = [Line2D([], [], marker="D", ls="none", ms=11, mfc=WHITE, mec=ACCENT, mew=2.0),
               Line2D([], [], marker="o", ls="none", ms=8.5, mfc=GREEN, mec=GREEN)]
    fig.legend(handles, ["merged / committed", "ran live"], loc="upper right",
               bbox_to_anchor=(0.98, 0.975), ncol=2, frameon=False, fontsize=12.5,
               labelcolor=MUTED, handletextpad=0.4, columnspacing=1.6)
    save(fig, "fig_o1_since_0916")
    return ms


# ---------------------------------------------------------------------------
# fig_o2_thirteen
# ---------------------------------------------------------------------------

def context_0908():
    lines = read(TEMPLATE_916).splitlines()
    ln = lines[TEMPLATE_916_LINE - 1]
    if "0/13 在 NDTwin fabric 上跑過" not in ln or "09-08" not in ln:
        die(f"{TEMPLATE_916}:{TEMPLATE_916_LINE} no longer says 0/13 on the NDTwin fabric at "
            f"09-08: {ln[:80]}")
    m = re.search(r"\*\*(\d+)/13 在 NDTwin fabric 上跑過", ln)
    val = int(m.group(1))
    if val != 0:
        die(f"the 09-08 context is {val}/13 run, not 'not run'")
    print(f"[o2] context: {TEMPLATE_916}:{TEMPLATE_916_LINE} -> {val}/13 run on the NDTwin "
          f"fabric (09-08) -> drawn as 'not run', off the scale")
    return val


def fig_o2(runs):
    v0 = context_0908()
    for r in runs:
        print(f"[o2] {r['stamp']}  both arms as the exercise says: {r['n']:2d}/13  "
              f"code {'+'.join(r['codes'])}  missing: "
              f"{[e for e in ORDER if e not in r['exs']]}")
    if runs[-1]["n"] != 13:
        die("the newest full run is not 13/13")

    # x positions: the 09-08 point, a gap, then the runs grouped by day
    xs, day_of, prev_day, xpos = [], [], None, 1.8
    for r in runs:
        day = r["stamp"][:10]
        if prev_day is not None:
            xpos += 1.0 if day == prev_day else 1.55
        xs.append(xpos)
        day_of.append(day)
        prev_day = day
    x0 = 0.0

    fig, ax = plt.subplots(figsize=(13.33, 6.0))
    fig.subplots_adjust(left=0.085, right=0.975, top=0.83, bottom=0.2)
    ys = [r["n"] for r in runs]
    ax.step(xs, ys, where="post", color=ACCENT, lw=2.0, zorder=2)
    # 09-08: nothing had run on the NDTwin fabric -- "not run", drawn below the scale, not as a 0
    y_nr = -1.9
    ax.plot([x0], [y_nr], "s", ms=11, mfc=WHITE, mec=FAINT, mew=2.0, zorder=3, clip_on=False)
    for k, (xv, yv, r) in enumerate(zip(xs, ys, runs)):
        n_none = sum(1 for c in r["cells"].values() if c == "none")
        r["n_none"] = n_none
        mostly_none = n_none > 13          # most arms had no verdict (teardown, not the twin)
        ax.plot([xv], [yv], "o", ms=11, mfc=WHITE if mostly_none else ACCENT, mec=ACCENT,
                mew=2.0 if mostly_none else 1.8, zorder=3)
        if mostly_none:
            ax.text(xv, yv + 1.45, "no verdict", ha="center", va="bottom", fontsize=12,
                    color=MUTED)
        dip = k > 0 and yv < ys[k - 1]
        ax.text(xv, yv - 0.55 if dip else yv + 0.55, f"{yv}", ha="center",
                va="top" if dip else "bottom", fontsize=14, fontweight="bold", color=INK)
    ax.text(x0, y_nr + 0.5, "not run", ha="center", va="bottom", fontsize=13, color=FAINT)
    # separator: the 09-16 report
    xsep = (x0 + xs[0]) / 2
    ax.axvline(xsep, color=RULE, lw=1.4, ls=(0, (4, 3)), zorder=1)
    ax.text(xsep, 15.1, "09-16 report", ha="center", va="bottom", fontsize=12, color=MUTED)

    ax.set_xlim(x0 - 0.6, xs[-1] + 0.6)
    ax.set_ylim(-3.0, 15.0)
    ax.axhline(0, color=MUTED, lw=1.0, zorder=1)
    ax.set_yticks([0, 5, 10, 13])
    ax.grid(axis="y", color=RULE, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_xticks([x0] + xs)
    ax.set_xticklabels(["09-08"] + [f"{r['stamp'][11:13]}:{r['stamp'][13:15]}" for r in runs],
                       fontsize=11, color=MUTED)
    ax.tick_params(axis="x", length=0, pad=6)
    ax.tick_params(axis="y", colors=MUTED, labelsize=12.5)
    # day labels under the time labels
    groups = {}
    for xv, d in zip(xs, day_of):
        groups.setdefault(d, []).append(xv)
    for d, v in groups.items():
        ax.text(sum(v) / len(v), -0.13, d[5:], ha="center", va="top", fontsize=12.5, color=INK,
                transform=ax.get_xaxis_transform())
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["left"].set_bounds(0, 13)
    ax.set_ylabel("exercises, both arms as expected", fontsize=13, color=MUTED, labelpad=8)
    ax.text(-0.012, -0.13, "run (UTC)", ha="right", va="top", fontsize=11, color=MUTED,
            transform=ax.transAxes)
    fig.text(0.02, 0.935, "Exercises with both arms as expected", fontsize=22,
             fontweight="bold", color=INK, ha="left", va="center")
    handles = [Line2D([], [], marker="o", ls="none", ms=10, color=ACCENT, mec=WHITE),
               Line2D([], [], marker="s", ls="none", ms=10, mfc=WHITE, mec=FAINT, mew=2.0)]
    fig.legend(handles, ["full live run, NDTwin fabric", "09-08, before the 09-16 report"],
               loc="upper right", bbox_to_anchor=(0.975, 0.975), ncol=2, frameon=False,
               fontsize=12.5, labelcolor=MUTED, handletextpad=0.4, columnspacing=1.6)
    save(fig, "fig_o2_thirteen")


def main():
    runs = full_runs()
    ms = fig_o1(runs)
    fig_o2(runs)
    print(f"[summary] {len(ms)} markers on o1; {len(runs)} full runs on o2: "
          + ", ".join(f"{r['stamp']}={r['n']}" for r in runs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
