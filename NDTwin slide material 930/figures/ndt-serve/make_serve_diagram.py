#!/usr/bin/env python3
"""
make_serve_diagram.py -- fig_s1_serve_path: `ndt serve`, the local web entry point to the lab,
drawn as the path one request takes.  Where the page is going (GUI v2) is a separate figure.

An architecture diagram; no measured number is on it.  Each box is a mechanism named in the
code at trunk 3d740be0 (tools/ndt_serve/serve.py, verbs.py) -- the .md cites the line for each
-- and the two literals on the canvas are read from serve.py at run time (BIND and the --port
default), so the picture cannot drift from the code without this script failing.

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/ndt-serve"
    "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_serve_diagram.py
"""
import os
import re
import sys

import matplotlib

assert matplotlib.__version__.startswith("3.11"), matplotlib.__version__
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["font.monospace"] = ["Courier New", "Liberation Mono", "DejaVu Sans Mono"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

REPO = os.environ.get("NDTWIN_REPO", "/home/adam/Desktop/NDTwin-Kernel")
SERVE = os.path.join(REPO, "tools/ndt_serve/serve.py")

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")
STEM = "fig_s1_serve_path"

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
WARNC, WHITE, GREEN = "#9C3B2E", "#FFFFFF", "#2F7D4F"
W, H = 13.33, 5.6


def die(msg):
    raise SystemExit(f"make_serve_diagram: {msg}")


def from_code():
    src = open(SERVE, encoding="utf-8").read()
    m_bind = re.search(r'^BIND = "([0-9.]+)"', src, re.M)
    m_port = re.search(r'ap\.add_argument\("--port", type=int, default=(\d+)', src)
    m_hdr = re.search(r'^TOKEN_HEADER = "([^"]+)"', src, re.M)
    m_claim = re.search(r"def _require_own_claim\(self\)", src)
    m_dry = re.search(r'"dry_run"', src)
    if not (m_bind and m_port and m_hdr and m_claim and m_dry):
        die("serve.py no longer has BIND / --port default / TOKEN_HEADER / "
            "_require_own_claim / dry_run where this script reads them")
    print(f"[code] BIND {m_bind.group(1)}  port {m_port.group(1)}  header {m_hdr.group(1)}")
    return m_bind.group(1), m_port.group(1)


def box(ax, x, y, w, h, fill=WHITE, edge=INK, lw=1.2, ls="solid", r=0.06, z=2):
    ax.add_patch(FancyBboxPatch((x + r, y + r), w - 2 * r, h - 2 * r,
                                boxstyle=f"round,pad={r},rounding_size={r}", facecolor=fill,
                                edgecolor=edge, linewidth=lw, linestyle=ls, zorder=z))


def txt(ax, x, y, s, size=13, color=INK, weight="normal", ha="center", va="center",
        mono=False, z=6):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, zorder=z,
            family="monospace" if mono else None, linespacing=1.25)


def arrow(ax, x0, y0, x1, y1, color=INK, lw=1.5, ls="solid", z=3, both=False):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="<|-|>" if both else "-|>",
                                 mutation_scale=14, color=color, lw=lw, linestyle=ls,
                                 shrinkA=0, shrinkB=0, zorder=z))


def main():
    bind, port = from_code()
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    txt(ax, 0.45, 0.48, "ndt serve: one local door to the lab", size=22, weight="bold",
        ha="left")

    # browser + one-time URL
    box(ax, 0.45, 1.25, 1.95, 1.05, fill=WHITE, edge=MUTED, ls=(0, (4, 3)))
    txt(ax, 1.425, 1.60, "one-time URL", size=13, weight="bold", color=BODY)
    txt(ax, 1.425, 1.95, "#k=…", size=12, color=MUTED, mono=True)
    box(ax, 0.45, 2.85, 1.95, 1.45, edge=INK, lw=1.4)
    txt(ax, 1.425, 3.35, "browser", size=15, weight="bold")
    txt(ax, 1.425, 3.80, "page", size=12.5, color=MUTED)
    arrow(ax, 1.425, 2.32, 1.425, 2.83, color=MUTED)

    # the server and its four gates
    sx, sy, sw, sh = 2.95, 1.10, 6.80, 3.35
    box(ax, sx, sy, sw, sh, fill=PANEL, edge=ACCENT, lw=2.0, r=0.08, z=1)
    txt(ax, sx + 0.22, sy + 0.30, "ndt serve", size=15, weight="bold", color=ACCENT, ha="left")
    txt(ax, sx + sw - 0.22, sy + 0.30, f"{bind}:{port} only", size=12.5, color=ACCENT,
        ha="right", mono=True)
    gates = [("token", "one-time\nnonce → token"),
             ("same origin", "token on\nevery call"),
             ("preview", "the exact\nndt command"),
             ("your claim?", "one job\nat a time")]
    gw, gh, gg = 1.47, 2.05, 0.18
    gx0 = sx + (sw - (4 * gw + 3 * gg)) / 2
    gy = sy + 0.85
    for i, (a, b) in enumerate(gates):
        x = gx0 + i * (gw + gg)
        box(ax, x, gy, gw, gh, fill=WHITE, edge=INK, lw=1.2)
        txt(ax, x + gw / 2, gy + 0.45, a, size=14, weight="bold")
        txt(ax, x + gw / 2, gy + 1.22, b, size=12, color=MUTED)
        if i:
            arrow(ax, x - gg + 0.01, gy + gh / 2, x - 0.01, gy + gh / 2)
    arrow(ax, 2.42, 3.575, gx0 - 0.01, 3.575, color=INK)

    # ndt and the lab
    nx = 10.25
    box(ax, nx, 1.25, 2.65, 1.30, edge=INK, lw=1.4)
    txt(ax, nx + 1.325, 1.62, "ndt", size=16, weight="bold", mono=True)
    txt(ax, nx + 1.325, 2.10, "up · down · claim\nrelease · apps", size=11.5, color=MUTED)
    box(ax, nx, 3.05, 2.65, 1.25, edge=GREEN, lw=1.6)
    txt(ax, nx + 1.325, 3.45, "lab", size=16, weight="bold", color=GREEN)
    txt(ax, nx + 1.325, 3.90, "ndt's own guard", size=11.5, color=MUTED)
    gx_last = gx0 + 3 * (gw + gg) + gw
    arrow(ax, gx_last + 0.01, 1.90, nx - 0.01, 1.90, color=INK)
    arrow(ax, nx + 1.325, 2.57, nx + 1.325, 3.03, color=INK)
    # the job's log goes back to the page
    ax.add_patch(FancyArrowPatch((sx + sw / 2, sy + sh + 0.02), (1.425, 4.32),
                                 connectionstyle="arc3,rad=-0.25", arrowstyle="-|>",
                                 mutation_scale=14, color=MUTED, lw=1.3, ls=(0, (4, 3)),
                                 shrinkA=0, shrinkB=0, zorder=3))
    txt(ax, 4.05, 4.68, "job log, polled", size=12, color=MUTED)

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
