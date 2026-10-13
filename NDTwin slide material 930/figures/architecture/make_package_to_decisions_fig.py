#!/usr/bin/env python3
"""From an exercise to a running proxy, as three pages (Adam 2026-09-29: fewer words, less crowded).

  fig_p2a_package_path       exercise -> convert -> pre-flight -> ndt up -> proxy, and what package/ holds
  fig_p2b_package_fields     each package.json field -> who reads it -> keywords
  fig_p2c_proxy_decisions    the proxy's start-up decisions as a tree

READ, trunk 3368412d: `p4_proxy/mininet/app_package.py` (`load`, `_switches`, `parse_roles`),
`p4_proxy/proxy_agent/main.py` (`startup`), `p4_proxy/proxy_agent/route_binding.py`,
`tools/p4_exercise/convert.py`. Every field name drawn must appear in app_package.py at TRUNK.

[Co-developed with claude code -- Adam]
"""
import os
import subprocess
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["font.monospace"] = ["Courier New", "Liberation Mono", "DejaVu Sans Mono"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

KERNEL = "/home/adam/Desktop/NDTwin-Kernel"
TRUNK = "3368412d"
HERE = os.path.dirname(os.path.abspath(__file__))

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
W, H = 13.333, 7.0
MONO = "monospace"

SRC = subprocess.run(["git", "-C", KERNEL, "show", f"{TRUNK}:p4_proxy/mininet/app_package.py"],
                     capture_output=True, text=True)
if SRC.returncode != 0:
    sys.exit(f"STOP: app_package.py not readable at {TRUNK}")
SRC = SRC.stdout


def need(token):
    if token not in SRC:
        sys.exit(f"STOP: {token!r} is not in app_package.py at {TRUNK}")


def page(title):
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    ax.text(0.45, 0.4, title, fontsize=20, color=INK, fontweight="bold", va="center")
    ax.text(W - 0.45, 0.4, f"READ · trunk {TRUNK}", fontsize=10, color=MUTED, ha="right",
            va="center", fontweight="bold")
    return fig, ax


def rect(ax, x, y, w, h, fc="#FFFFFF", ec=INK, lw=1.0, ls="-"):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls))


def text(ax, x, y, s, size=12, color=BODY, ha="center", va="center", weight="normal", family=None):
    kw = {"fontfamily": family} if family else {}
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, fontweight=weight, **kw)


def arrow(ax, x0, y0, x1, y1, color=INK, lw=1.3):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=14,
                                 color=color, linewidth=lw, shrinkA=0, shrinkB=0))


def box(ax, x, y, w, h, head, sub=None, accent=False, head_size=13, sub_size=11, family=None,
        fc=None):
    rect(ax, x, y, w, h, fc=fc or (ACCENT_BG if accent else "#FFFFFF"),
         ec=ACCENT if accent else INK, lw=1.7 if accent else 1.1)
    if sub:
        text(ax, x + w / 2, y + h * 0.36, head, size=head_size, color=ACCENT if accent else INK,
             weight="bold", family=family)
        text(ax, x + w / 2, y + h * 0.7, sub, size=sub_size, color=MUTED)
    else:
        text(ax, x + w / 2, y + h / 2, head, size=head_size, color=ACCENT if accent else INK,
             weight="bold", family=family)


def save(fig, stem):
    for ext, kw in (("png", {"dpi": 300}), ("pdf", {}), ("svg", {})):
        fig.savefig(os.path.join(HERE, f"{stem}.{ext}"), **kw)
    os.makedirs(os.path.join(HERE, "_hires"), exist_ok=True)
    fig.savefig(os.path.join(HERE, "_hires", f"{stem}.png"), dpi=500)
    plt.close(fig)
    print("wrote", stem)


# ============ page 1: the way in, and what the package holds ============
fig, ax = page("From an exercise to a package")
steps = [("exercise", None), ("convert.py", "package/"), ("pre-flight", "names vs p4info"),
         ("ndt up p4 --app", "builds fabric"), ("proxy", "reads package.json")]
sw, sh, sy, gap = 2.2, 1.1, 1.05, 0.33
for i, (name, sub) in enumerate(steps):
    x = 0.6 + i * (sw + gap)
    last = i == len(steps) - 1
    box(ax, x, sy, sw, sh, name, sub, accent=last, head_size=13,
        family=MONO if name.endswith(".py") or name.startswith("ndt") else None)
    if not last:
        arrow(ax, x + sw, sy + sh / 2, x + sw + gap, sy + sh / 2)

# the package folder
fx, fy, fw, fh = 1.6, 3.0, 10.1, 3.45
rect(ax, fx, fy, fw, fh, fc=PANEL, ec=FAINT, ls="--", lw=1.2)
text(ax, fx + 0.2, fy + 0.35, "package/", size=14, color=INK, ha="left", weight="bold", family=MONO)
arrow(ax, 0.6 + 1 * (sw + gap) + sw / 2, sy + sh, 0.6 + 1 * (sw + gap) + sw / 2, fy, color=FAINT)
files = [("package.json", "the manifest", True),
         ("sN program", "bmv2 json + p4info", False),
         ("sN-runtime.json", "start-up entries", False),
         ("ndtwin/topology.json", "switches · links · hosts", False)]
bw, bh, by = 2.25, 1.35, fy + 0.8
for i, (name, sub, acc) in enumerate(files):
    x = fx + 0.2 + i * (bw + 0.2)
    box(ax, x, by, bw, bh, name, sub, accent=acc, head_size=12, sub_size=10.5, family=MONO)
text(ax, fx + fw / 2, fy + fh - 0.5, "copied from the exercise: program, runtime  ·  written by convert: manifest, topology",
     size=10.5, color=MUTED)
save(fig, "fig_p2a_package_path")

# ============ page 2: each field, who reads it, keywords ============
fig, ax = page("What package.json tells NDTwin")
ROWS = [  # field, token in app_package.py, reader, keywords
    ("topology", '"topology"', "all", "switch count · links · host ports"),
    ("hosts", '"hosts"', "fabric", "IP · MAC · start commands"),
    ("links", '"links"', "fabric", "bandwidth · delay"),
    ("switches.N.pipeline", '"pipeline"', "proxy", "program for switch N"),
    ("switches.N.entries", '"entries"', "proxy", "table entries · multicast groups"),
    ("control_plane.mode", '"mode"', "proxy", "ndtwin  |  external (read-only)"),
    ("control_plane.election_id", '"election_id"', "proxy", "mastership id"),
    ("roles.ipv4_route", '"roles"', "proxy", "NDTwin's route table"),
    ("telemetry.source", '"telemetry"', "proxy", "in-program clone  |  veth sampling"),
]
for _, tok, _, _ in ROWS:
    need(tok)
top, rh, rg = 1.15, 0.52, 0.09
text(ax, 0.6, top - 0.1, "field", size=11, color=MUTED, ha="left", weight="bold", va="bottom")
text(ax, 5.35, top - 0.1, "read by", size=11, color=MUTED, weight="bold", va="bottom")
text(ax, 7.0, top - 0.1, "decides", size=11, color=MUTED, ha="left", weight="bold", va="bottom")
for i, (field, _, who, keys) in enumerate(ROWS):
    y = top + i * (rh + rg)
    proxy = who == "proxy"
    rect(ax, 0.6, y, 4.1, rh, ec=ACCENT if proxy else INK, lw=1.5 if proxy else 1.0)
    text(ax, 0.8, y + rh / 2, field, size=12.5, color=ACCENT if proxy else INK, ha="left",
         weight="bold", family=MONO)
    rect(ax, 4.85, y + 0.08, 1.0, rh - 0.16, fc=ACCENT if proxy else "#FFFFFF",
         ec=ACCENT if proxy else FAINT)
    text(ax, 5.35, y + rh / 2, who, size=10.5, color="#FFFFFF" if proxy else MUTED, weight="bold")
    arrow(ax, 5.95, y + rh / 2, 6.8, y + rh / 2, color=FAINT)
    rect(ax, 6.9, y, 5.85, rh, fc=ACCENT_BG if proxy else PANEL, ec=RULE)
    text(ax, 7.1, y + rh / 2, keys, size=13, color=INK, ha="left")
save(fig, "fig_p2b_package_fields")

# ============ page 3: the proxy's start-up decisions ============
fig, ax = page("What the proxy decides at start-up")


def q(ax, x, y, w, h, s):  # a question, drawn as a rounded-looking panel
    rect(ax, x, y, w, h, fc=PANEL, ec=INK, lw=1.3)
    text(ax, x + w / 2, y + h / 2, s, size=13, color=INK, weight="bold")


def act(ax, x, y, w, h, lines, accent=False):
    rect(ax, x, y, w, h, fc=ACCENT_BG if accent else "#FFFFFF", ec=ACCENT if accent else INK,
         lw=1.6 if accent else 1.1)
    for j, ln in enumerate(lines):
        text(ax, x + w / 2, y + h / 2 + (j - (len(lines) - 1) / 2) * 0.33, ln, size=12,
             color=ACCENT if accent else BODY)


def label(ax, x, y, s):
    text(ax, x, y, s, size=11, color=MUTED, weight="bold")


# level 1: control_plane.mode
q(ax, 4.9, 1.0, 3.5, 0.7, "control_plane.mode ?")
act(ax, 9.6, 0.95, 3.2, 0.8, ["read-only: no push, no writes", "its own controller writes"])
arrow(ax, 8.4, 1.35, 9.6, 1.35)
label(ax, 9.0, 1.15, "external")
arrow(ax, 6.65, 1.7, 6.65, 2.25)
label(ax, 7.1, 1.98, "ndtwin")

# level 2: push, then whose program
act(ax, 4.9, 2.25, 3.5, 0.6, ["push each switch's program"])
arrow(ax, 6.65, 2.85, 6.65, 3.25)
q(ax, 4.9, 3.25, 3.5, 0.7, "NDTwin's own program ?")

# yes branch (left)
arrow(ax, 4.9, 3.6, 3.55, 3.6)
label(ax, 4.2, 3.4, "yes")
act(ax, 0.6, 3.1, 2.95, 1.35, ["BFS /32 routes", "LLDP + link watchdog", "in-program telemetry"])

# no branch (right): foreign program
arrow(ax, 8.4, 3.6, 9.6, 3.6)
label(ax, 9.0, 3.4, "no")
act(ax, 9.6, 2.95, 3.2, 1.3, ["entries by p4info name", "heartbeat watchdog", "veth sampling"], accent=True)
arrow(ax, 11.2, 4.25, 11.2, 4.75)
q(ax, 9.6, 4.75, 3.2, 0.7, "roles declared ?")
arrow(ax, 10.4, 5.45, 10.4, 5.9)
label(ax, 10.1, 5.68, "yes")
act(ax, 9.6, 5.9, 1.55, 0.75, ["route table", "bound"], accent=True)
arrow(ax, 12.0, 5.45, 12.0, 5.9)
label(ax, 12.35, 5.68, "no")
act(ax, 11.3, 5.9, 1.5, 0.75, ["routes", "→ 501"])
save(fig, "fig_p2c_proxy_decisions")

# the old single-page figure is superseded; keep its files, do not regenerate it here
