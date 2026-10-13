#!/usr/bin/env python3
"""The P4 proxy, module by module -- the 820 module diagram redrawn for trunk 3368412d.

Same logic as `NDTwin Slide material 820/generator/build_module_diagram.js`: the kernel on top,
the proxy's modules in the middle with who talks to whom, the switches below. What changed since
09-16 is filled: the modules that let a switch run somebody else's program.

Line counts are read from `git show <TRUNK>:<path>` at run time, never typed.
Every module the figure names must exist at TRUNK, or the script stops and says which.

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
BASE_0916 = "70615ec5"  # trunk as of 2026-09-16 00:00Z
HERE = os.path.dirname(os.path.abspath(__file__))
STEM = "fig_p1_proxy_modules"

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"

W, H = 13.333, 7.2


def git(*args):
    return subprocess.run(["git", "-C", KERNEL, *args], capture_output=True, text=True)


def lines_at(path):
    r = git("show", f"{TRUNK}:{path}")
    if r.returncode != 0:
        sys.exit(f"STOP: {path} does not exist at {TRUNK}")
    return r.stdout.count("\n")


def is_new(path):
    """True when the file is absent from the 09-16 trunk."""
    return git("cat-file", "-e", f"{BASE_0916}:{path}").returncode != 0


fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)  # y grows downward, like a slide
ax.axis("off")


def rect(x, y, w, h, fc=WHITE if False else "#FFFFFF", ec=INK, lw=1.0, ls="-"):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls))


def text(x, y, s, size=9, color=BODY, ha="left", va="center", weight="normal", family=None):
    kw = {"fontfamily": family} if family else {}
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, fontweight=weight, **kw)


def arrow(x0, y0, x1, y1, color=INK, lw=1.1, both=False, ls="-"):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1),
                                 arrowstyle="<|-|>" if both else "-|>", mutation_scale=11,
                                 color=color, linewidth=lw, linestyle=ls, shrinkA=0, shrinkB=0))


def module(x, y, w, h, path, role, size=10.5, count=False):
    new = is_new(path)
    rect(x, y, w, h, fc=ACCENT_BG if new else "#FFFFFF", ec=ACCENT if new else INK,
         lw=1.6 if new else 1.0)
    name = os.path.basename(path)
    ny = y + 0.24 if role else y + h / 2
    text(x + w / 2, ny, name, size=size, color=ACCENT if new else INK, ha="center",
         weight="bold", family="monospace")
    if role:
        text(x + w / 2, y + h / 2 + 0.14, role, size=8.5, color=BODY, ha="center")
    n = lines_at(path)
    if count:
        text(x + w / 2, y + h - 0.14, f"{n} lines", size=7, color=FAINT, ha="center")
    return new


PA = "p4_proxy/proxy_agent/"
MONO_FONT = "monospace"
MN = "p4_proxy/mininet/"

# ---------------- title ----------------
text(0.45, 0.36, "The P4 proxy, module by module", size=18, color=INK, weight="bold")
text(W - 0.45, 0.36, f"READ · trunk {TRUNK}", size=10, color=MUTED, ha="right", weight="bold")

# ---------------- kernel ----------------
rect(0.6, 0.72, 12.1, 0.55, lw=1.25)
text(0.78, 0.995, "NDTwin kernel", size=12, color=INK, weight="bold")
text(12.55, 0.995, "/ndt/* HTTP API  ·  sFlow collector, UDP 6343", size=9, color=MUTED, ha="right")

# kernel <-> proxy
arrow(3.9, 1.27, 3.9, 1.75, both=True)
text(4.02, 1.61, "Ryu-compatible REST", size=8, color=MUTED)
arrow(8.575, 1.95, 8.575, 1.27)
text(8.45, 1.61, "/ndt/ push", size=8, color=MUTED, ha="right")

# ---------------- proxy frame ----------------
rect(0.6, 1.75, 11.45, 3.5, ec=ACCENT, lw=1.8)
ax.add_patch(Rectangle((0.75, 1.64), 2.2, 0.22, facecolor="#FFFFFF", edgecolor="none"))
text(0.8, 1.75, "P4 proxy agent", size=10, color=ACCENT, weight="bold")

# column 1: startup and which package
module(0.8, 1.95, 1.6, 1.95, PA + "main.py", "startup:\nconnect, push,\nfill, wire")
module(0.8, 4.05, 1.6, 1.0, PA + "profile.py", "which\npackage")

# row 1: the door in, the renderers, the push north
module(2.6, 1.95, 2.6, 0.85, PA + "api_routes.py", "the only door in")
module(5.5, 1.95, 1.95, 0.4, PA + "ryu_topology.py", "", size=9.5, count=False)
module(5.5, 2.4, 1.95, 0.4, PA + "ryu_flow_stats.py", "", size=9.5, count=False)
arrow(5.2, 2.15, 5.5, 2.15)
arrow(5.2, 2.6, 5.5, 2.6)
rect(9.7, 1.95, 2.1, 0.85, fc=PANEL, ec=RULE)
text(10.75, 2.2, "bookkeeping", size=9, color=MUTED, ha="center", weight="bold")
for i, f in enumerate(("rule_journal.py", "rule_install_times.py", "boot_identity.py")):
    lines_at(PA + f)
    text(10.75, 2.42 + i * 0.13, f, size=7, color=FAINT, ha="center", family="monospace")
module(7.75, 1.95, 1.65, 0.85, PA + "kernel_notifier.py", "", size=9)

# row 2: all the state
module(2.6, 3.05, 6.0, 0.85, PA + "topology_manager.py",
       "graph · BFS routes · LLDP beacon + link watchdog · Ryu rule → table entry", size=11)
module(8.85, 3.05, 2.95, 0.85, PA + "link_heartbeat.py", "heartbeat report → up / down")
arrow(3.9, 2.8, 3.9, 3.05, both=True)
arrow(8.85, 3.475, 8.6, 3.475)
arrow(8.3, 3.05, 8.3, 2.8)

# row 3: which table, one client per switch, the sFlow builder
module(2.6, 4.15, 2.3, 0.9, PA + "route_binding.py", "roles → which table\nno roles → 501")
module(5.1, 4.15, 3.5, 0.9, PA + "p4_client.py", "one per switch · entries by p4info name")
module(8.85, 4.15, 2.95, 0.9, PA + "sflow_emitter.py", "sFlow v5 builder")
arrow(3.75, 3.9, 3.75, 4.15)
arrow(4.9, 4.6, 5.1, 4.6)
arrow(6.85, 3.9, 6.85, 4.15)
arrow(8.6, 4.6, 8.85, 4.6, color=ACCENT)
# cooperative telemetry to the kernel
arrow(11.8, 4.6, 12.3, 4.6, color=ACCENT, lw=1.4)
arrow(12.3, 4.6, 12.3, 1.27, color=ACCENT, lw=1.4)
ax.text(12.43, 3.0, "sFlow v5", fontsize=7.5, color=ACCENT, ha="center", va="center", rotation=90)

# ---------------- below the proxy ----------------
arrow(6.85, 5.05, 6.85, 5.6, both=True)
text(6.97, 5.36, "P4Runtime gRPC", size=8, color=MUTED)
rect(2.6, 5.6, 6.0, 0.95, fc=PANEL)
text(5.6, 5.95, "bmv2 simple_switch_grpc × N", size=11, color=INK, ha="center", weight="bold")
text(5.6, 6.27, "each runs the program its package names", size=9, color=BODY, ha="center")

# the app package
rect(0.6, 5.6, 1.8, 0.95, fc="#FFFFFF", ec=FAINT, ls="--")
text(1.5, 5.85, "app package", size=9.5, color=INK, ha="center", weight="bold")
text(1.5, 6.18, "program · topology\nsN-runtime · roles", size=7.5, color=MUTED, ha="center")
arrow(1.5, 5.6, 1.5, 5.05, color=FAINT, ls="--")
text(1.5, 6.78, "convert.py → pre-flight", size=7.5, color=MUTED, ha="center")
lines_at(MN + "app_package.py")

# the root helper: heartbeat and link telemetry
new_lt = is_new(MN + "link_telemetry.py") and is_new(MN + "psample_sflow_emitter.py")
rect(8.85, 5.6, 3.85, 1.1, fc=ACCENT_BG if new_lt else "#FFFFFF", ec=ACCENT, lw=1.6, ls="--")
text(10.775, 5.83, "outside the proxy, as root", size=9.5, color=ACCENT, ha="center", weight="bold")
text(10.775, 6.07, "ndtwin-lab: veth heartbeat → heartbeat.json", size=8, color=BODY, ha="center")
text(10.775, 6.3, "fabric: tc sample 1/256 →", size=8, color=BODY, ha="center")
ax.text(10.775, 6.5, ("psample_sflow_emitter.py" if lines_at(MN + 'psample_sflow_emitter.py') else ""),
        fontsize=8.5, color=ACCENT, ha="center", va="center", fontweight="bold", fontfamily=MONO_FONT)
# the emitter process reuses the proxy's sFlow builder module (code, not the proxy process)
arrow(10.3, 5.6, 10.3, 5.05, color=ACCENT, ls=":")
text(10.22, 5.33, "same builder (import)", size=7.5, color=ACCENT, ha="right")
lines_at(MN + "link_telemetry.py")
lines_at(MN + "psample_sflow_emitter.py")
ax.plot([11.95, 11.95], [5.6, 3.475], color=ACCENT, linewidth=1.1, linestyle="--")
arrow(11.95, 3.475, 11.8, 3.475, color=ACCENT)
text(11.88, 5.4, "heartbeat.json", size=7.5, color=ACCENT, ha="right")
arrow(12.55, 5.6, 12.55, 1.27, color=ACCENT, lw=1.4, ls="--")
text(12.6, 5.05, "link sFlow", size=8, color=ACCENT, ha="left", va="center")

# legend
rect(0.62, 6.93, 0.28, 0.16, fc=ACCENT_BG, ec=ACCENT, lw=1.6)
text(0.98, 7.01, "added since 09-16, for a program that is not NDTwin's own", size=8.5, color=MUTED)

for ext, kw in (("png", {"dpi": 300}), ("pdf", {}), ("svg", {})):
    fig.savefig(os.path.join(HERE, f"{STEM}.{ext}"), **kw)
os.makedirs(os.path.join(HERE, "_hires"), exist_ok=True)
fig.savefig(os.path.join(HERE, "_hires", f"{STEM}.png"), dpi=500)
print("wrote", STEM)
