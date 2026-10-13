#!/usr/bin/env python3
"""
make_sampling_error_fig.py -- fig_m1_sampling_error: the two telemetry paths (cooperative =
the P4 pipeline clones 1 in 256 packets; link = tc samples 1 in 256 on the switch-side veths),
measured on the same 10-switch bmv2 fabric, h1 -> h4, at 2 / 20 / 100 Mbit/s.

Data: doc/audit/2026-09-19_telemetry-three-groups/raw/2026-09-19T115737Z_full/summary.json
(the fifth, canonical campaign; git-ignored raw in the kernel checkout, .gitignore:84), keys
  sampling_error_by_group[group=*]["H-B1"].rates[*].{offered_mbit, median_abs_error, band}
  sampling_error_cross_group_registered.rates[*].ratio      (asserted against, not drawn)
Every drawn value is read from that file at run time.

Not drawn, on purpose (see the .md): the pps ceiling (not resolvable on this machine,
REPORT-P3-2026-09-24.md section 1 item 1) and CPU (FINDINGS section 4 erratum).  All of it was
measured before the protobuf 5 switch (5dc7fc9a, 2026-09-27) and must not share a chart with
anything measured after it.

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/telemetry"
    "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_sampling_error_fig.py
"""
import json
import os
import sys

import matplotlib

assert matplotlib.__version__.startswith("3.11"), matplotlib.__version__
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator  # noqa: E402

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

REPO = os.environ.get("NDTWIN_REPO", "/home/adam/Desktop/NDTwin-Kernel")
RAW = os.path.join(REPO, "doc/audit/2026-09-19_telemetry-three-groups/raw/2026-09-19T115737Z_full")
SUMMARY = os.path.join(RAW, "summary.json")
# each series' own generation: cooperative windows ran in G2, link windows in G3; the binaries are
# read from that generation's arm.meta (lines 12-15), not from another group's
ARM_META = {"cooperative": os.path.join(RAW, "G2/cooperative_f64_a/arm.meta"),
            "link": os.path.join(RAW, "G3/link_f64_a/arm.meta")}

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")
STEM = "fig_m1_sampling_error"

INK, MUTED, FAINT, RULE = "#1A1A1A", "#4F4F4F", "#6E6E6E", "#D0D0D0"
WHITE = "#FFFFFF"
# two series, fixed order; told apart by marker shape as well as hue
SERIES = [("cooperative", "#065A82", "o"), ("link", "#C0701C", "s")]


def die(msg):
    raise SystemExit(f"make_sampling_error_fig: {msg}")


def load():
    with open(SUMMARY) as f:
        d = json.load(f)
    if d.get("invalid_arms"):
        die(f"invalid_arms is not empty: {d['invalid_arms']}")
    by = {g["group"]: g for g in d["sampling_error_by_group"]}
    out = {}
    for name, _c, _m in SERIES:
        rates = by[name]["H-B1"]["rates"]
        out[name] = {int(r["offered_mbit"]): (r["median_abs_error"], r["band"]) for r in rates}
        # the hollow/filled marker must agree with the file's own position field
        for r in rates:
            lo, hi = r["band"]
            mine = "inside" if lo <= r["median_abs_error"] <= hi else (
                "above" if r["median_abs_error"] > hi else "below")
            if mine != r["position"]:
                die(f"{name} {r['offered_mbit']} Mbit/s: computed {mine}, file says {r['position']}")
    if sorted(out["cooperative"]) != [2, 20, 100] or sorted(out["link"]) != [2, 20, 100]:
        die("rates are not 2 / 20 / 100 Mbit/s")
    # cross-check against the registered cross-group ratios in the same file
    for r in d["sampling_error_cross_group_registered"]["rates"]:
        m = int(r["offered_mbit"])
        ratio = out["link"][m][0] / out["cooperative"][m][0]
        if abs(ratio - r["ratio"]) > 1e-9:
            die(f"{m} Mbit/s: link/coop {ratio} != summary ratio {r['ratio']}")
    for name in out:
        for m, (e, b) in sorted(out[name].items()):
            print(f"[data] {name:11s} {m:3d} Mbit/s  median |err| {e:.4f}  band "
                  f"[{b[0]:.4f}, {b[1]:.4f}]")
    return out, d


def binaries():
    """kernel and bmv2 sha256 from each series' own generation; both must name one binary pair."""
    seen = {}
    for name, path in ARM_META.items():
        kv = dict(ln.split("=", 1) for ln in open(path).read().splitlines() if "=" in ln)
        k, b = kv.get("kernel_sha256_start", ""), kv.get("switch_binary_sha256", "")
        if len(k) != 64 or len(b) != 64:
            die(f"{path}: no kernel / switch sha256")
        seen[name] = (k, b)
        print(f"[bin] {name:11s} kernel {k[:16]}  bmv2 {b[:16]}  ({os.path.relpath(path, RAW)})")
    if len(set(seen.values())) != 1:
        die(f"the two generations ran different binaries: {seen}")
    return seen["cooperative"]


def main():
    data, d = load()
    binaries()
    fig, ax = plt.subplots(figsize=(13.33, 6.2))
    fig.subplots_adjust(left=0.10, right=0.97, top=0.80, bottom=0.13)
    rates = [2, 20, 100]
    xs = {2: 0, 20: 1, 100: 2}
    off = {"cooperative": -0.13, "link": 0.13}
    for name, color, marker in SERIES:
        for m in rates:
            e, (lo, hi) = data[name][m]
            x = xs[m] + off[name]
            ax.plot([x, x], [lo * 100, hi * 100], color=color, alpha=0.22, lw=16,
                    solid_capstyle="butt", zorder=1)
            outside = not (lo <= e <= hi)
            if outside:      # hollow: outside the band expected from 1-in-256 sampling alone
                ax.plot([x], [e * 100], marker, ms=14, mfc=WHITE, mec=color, mew=3, zorder=3)
                ax.plot([x - 0.035, x + 0.07], [hi * 100, hi * 100], color=color, lw=1.6, zorder=2)
                ax.annotate(f"band top {hi * 100:.1f}%", xy=(x - 0.035, hi * 100),
                            xytext=(x - 0.10, hi * 100 * 0.76), fontsize=11.5, color=MUTED,
                            ha="right", va="center",
                            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
            else:
                ax.plot([x], [e * 100], marker, ms=13, color=color, mec=WHITE, mew=2, zorder=3)
            ax.annotate(f"{e * 100:.1f}%", xy=(x, e * 100),
                        xytext=(-14 if name == "cooperative" else 14, 0),
                        textcoords="offset points",
                        ha="right" if name == "cooperative" else "left", va="center",
                        fontsize=14, color=INK, fontweight="bold")
    ax.set_yscale("log")
    ax.set_ylim(0.7, 45)
    ax.yaxis.set_major_locator(FixedLocator([1, 2, 5, 10, 20, 40]))
    ax.yaxis.set_minor_locator(NullLocator())
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:g}%"))
    ax.set_xlim(-0.6, 2.6)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels([f"{m} Mbit/s" for m in rates], fontsize=14, color=INK)
    ax.tick_params(axis="y", colors=MUTED, labelsize=12.5)
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="y", color=RULE, lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.set_ylabel("twin vs. interface counters\n(median |error|)", fontsize=13.5, color=MUTED,
                  labelpad=10)

    fig.text(0.10, 0.935, "Sampling error of two telemetry paths", fontsize=22,
             fontweight="bold", color=INK, ha="left", va="center")
    # legend: two series + the band
    lx, ly = 0.10, 0.855
    for i, (name, color, marker) in enumerate(SERIES):
        fx = lx + i * 0.17
        fig.lines.append(plt.Line2D([fx + 0.005], [ly], marker=marker, ms=11, color=color,
                                    mec=WHITE, transform=fig.transFigure, ls="none"))
        fig.text(fx + 0.018, ly, name, fontsize=13, color=MUTED, va="center")
    bx = lx + 2 * 0.17
    fig.lines.append(plt.Line2D([bx - 0.004, bx + 0.014], [ly, ly], color=MUTED, alpha=0.25,
                                lw=12, transform=fig.transFigure, solid_capstyle="butt"))
    fig.text(bx + 0.022, ly, "expected from 1-in-256 sampling alone", fontsize=13,
             color=MUTED, va="center")
    hx = bx + 0.33
    fig.lines.append(plt.Line2D([hx], [ly], marker="o", ms=11, mfc=WHITE, mec=MUTED, mew=2.5,
                                transform=fig.transFigure, ls="none"))
    fig.text(hx + 0.014, ly, "outside the band", fontsize=13, color=MUTED, va="center")

    os.makedirs(HIRES, exist_ok=True)
    for ext in ("pdf", "png", "svg"):
        kw = {"dpi": 300} if ext == "png" else {}
        fig.savefig(os.path.join(OUTDIR, f"{STEM}.{ext}"), facecolor=WHITE, **kw)
    fig.savefig(os.path.join(HIRES, f"{STEM}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"[out] {STEM}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
