#!/usr/bin/env python3
"""
make_p02_architecture.py -- arch/fig_p02_architecture: what NDTwin is, as built today.  Page P02 of the
1021 deck.  Evidence class: READ (code and docs at trunk 2ece656c, read with `git show`, not executed).

A redraw of the 827 layout (NDTwin slide material 827/generator/build_arch_merged.js): apps on top, the
kernel, the control-plane adapters, three data planes side by side, the tools column on the right.  The
four changes of figures_spec/architecture.txt section 0 are applied: no "Local LLM (fine-tuning)", no
"AI/ML inference apps", the physical network dashed and tagged "no run on record", a small "ndt / ndtwin-lab"
box; "Data cache manager" is named Historical data manager.  Colours: kernel = blue, everything outside the
kernel = grey, coded-with-no-run = dashed white.  There is NO tint or legend by which repository holds a box
(template section 0 rule 7).

The boxes and arrows are drawn here; figures_spec/architecture.txt is the evidence: the generator reads it,
checks that every element id it draws (A1-A4, B0-B8, C1-C3, D1-D3, E1-E7) has an entry, that the
removed names do not come back, and copies each element's evidence lines into the companion .md.

Stops with a named reason if: the spec lacks an element id that is drawn; the spec's canvas title is not the
title drawn; a removed box name is among the drawn labels; the spec text asks for a repo tint or legend again; the spec no longer says the generator arrow goes to D1
only or that the proxy sFlow arrow starts at the proxy box (the figure draws both);
a drawn label is empty or a canvas title is over 45 characters.

[Co-developed with claude code -- Adam]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle_1021 as S  # noqa: E402
from figstyle_1021 import (ACCENT, BODY, FAINT, INK, MUTED, WHITE, REPO_FILL, REPO_EDGE, SEP_FILL,  # noqa: E402
                           SEP_EDGE, RULE, plt)
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle  # noqa: E402

WHO = "make_p02_architecture"
STEM = "fig_p02_architecture"
TITLE = "What NDTwin is, as built today"
args = sys.argv[1:]


def opt(name, default):
    return args[args.index(name) + 1] if name in args else default


SPEC = opt("--spec", os.path.join(S.DECK, "figures_spec", "architecture.txt"))
OUTDIR = opt("--out", os.path.join(S.DECK, "figures", "arch"))

REMOVED = ["Local LLM", "AI/ML", "Data cache manager"]

# id -> (label, style); style: "kernel" (blue), "out" (grey, outside the kernel), "dashed" (white, dashed),
# "plane" (data plane, drawn separately)
ELEMENTS = {
    "A1": ("Traffic-engineering App", "out"),
    "A2": ("Energy-saving App", "out"),
    "A4": ("Energy-saving simulator", "out"),
    "A3": ("... your app", "dashed"),
    "B0": ("REST server :8000", "kernel"),
    "B1": ("Topology and flow monitor", "kernel"),
    "B2": ("Flow and link usage collector (sFlow)", "kernel"),
    "B3": ("Flow routing manager", "kernel"),
    "B4": ("Device config and power manager", "kernel"),
    "B5": ("App registration and simulation requests", "kernel"),
    "B6": ("Intent translator", "kernel"),
    "B7": ("Historical data manager", "kernel"),
    "B8": ("Fault injection (netem)", "kernel"),
    "C1": ("Ryu + NDTwin Ryu app", "out"),
    "C2": ("P4 proxy agent", "out"),
    "C3": ("Link heartbeat helper", "out"),
    "D1": ("Mininet + OVS", "plane"),
    "D2": ("Physical switches", "plane"),
    "D3": ("Mininet + bmv2", "plane"),
    "E1": ("Simulation platform manager", "out"),
    "E2": ("Web GUI", "out"),
    "E3": ("Network state recorder", "out"),
    "E4": ("Network traffic visualizer", "out"),
    "E6": ("On-line LLM (OpenAI)", "dashed"),
    "E5": ("Network traffic generator", "out"),
    "E7": ("ndt / ndtwin-lab", "out"),
}


def read_spec():
    if not os.path.exists(SPEC):
        S.die(WHO, f"spec file missing: {SPEC}")
    lines = open(SPEC, encoding="utf-8").read().splitlines()
    ev, cur = {}, None
    for ln in lines:
        m = re.match(r"^\s{2}([A-E]\d)\s+(\S.*)$", ln)
        if m:
            cur = m.group(1)
            ev[cur] = [m.group(2).strip()]
            continue
        if cur and re.match(r"^\s{4,}\S", ln):
            ev[cur].append(ln.strip())
        else:
            cur = None
    full = "\n".join(lines)
    m = re.search(r"Title on canvas[^:]*:\s*(.+)", full)
    if not m or m.group(1).strip() != TITLE:
        S.die(WHO, f"architecture.txt canvas title is {m.group(1).strip() if m else None!r}, the figure draws {TITLE!r}")
    for need, why in (("double-headed arrow to D1", "the traffic generator's arrow goes to Mininet + OVS only"),
                      ("drawn FROM the P4 proxy box", "the proxy's sFlow arrow starts at the P4 proxy box")):
        if need not in full:
            S.die(WHO, f"architecture.txt no longer says {need!r} ({why}); the figure draws it that way")
    for bad in ("legend: \"this repo\"", "tint every box by the repo"):
        if bad in full:
            S.die(WHO, f"architecture.txt asks for a repo tint or legend again ({bad!r}); template section 0 rule 7 excludes it")
    for eid in ELEMENTS:
        if eid not in ev:
            S.die(WHO, f"architecture.txt has no entry for element {eid} ({ELEMENTS[eid][0]!r})")
    for eid, (lab, style) in ELEMENTS.items():
        if not lab.strip():
            S.die(WHO, f"element {eid} has an empty label")
        for bad in REMOVED:
            if bad.lower() in lab.lower():
                S.die(WHO, f"element {eid} label {lab!r} is a removed box name ({bad!r})")
    return ev


def main():
    ev = read_spec()
    W, H = 13.33, 7.66
    fig, ax = S.new_canvas(W, H)
    S.title(ax, TITLE, W)

    def box(eid, x, y, w, h, fs=10.5, bold=False, label=None, z=3, sub=None):
        lab, style = ELEMENTS[eid]
        lab = label or lab
        if style == "kernel":
            fc, ec, ls, lw = REPO_FILL, REPO_EDGE, "-", 1.3
        elif style == "out":
            fc, ec, ls, lw = SEP_FILL, SEP_EDGE, "-", 1.3
        else:
            fc, ec, ls, lw = WHITE, SEP_EDGE, (0, (4, 3)), 1.3
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.05", facecolor=fc,
                                    edgecolor=ec, lw=lw, ls=ls, zorder=z))
        if sub:
            ax.text(x + w / 2, y + h * 0.36, lab, ha="center", va="center", fontsize=fs, color=INK,
                    fontweight="bold" if bold else "normal", zorder=z + 1)
            ax.text(x + w / 2, y + h * 0.74, sub, ha="center", va="center", fontsize=9.5, color=MUTED,
                    zorder=z + 1)
        else:
            ax.text(x + w / 2, y + h / 2, lab, ha="center", va="center", fontsize=fs, color=INK,
                    fontweight="bold" if bold else "normal", zorder=z + 1, linespacing=1.12)

    def arrow(p, q, both=False, dashed=False, color=INK, lw=1.4):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="<|-|>" if both else "-|>", mutation_scale=12,
                                     color=color, lw=lw, ls=(0, (4, 3)) if dashed else "-", shrinkA=0,
                                     shrinkB=0, zorder=6))

    def note(x, y, text, ha="left", fs=10, color=MUTED, **kw):
        ax.text(x, y, text, ha=ha, va="center", fontsize=fs, color=color, zorder=7, **kw)

    # ---- apps (separate repos)
    ax.text(0.45, 1.20, "Apps", fontsize=12.5, fontweight="bold", color=INK, va="center")
    for eid, x in (("A1", 1.35), ("A2", 3.20), ("A4", 5.05), ("A3", 6.95)):
        box(eid, x, 0.88, 1.75 if eid != "A3" else 1.45, 0.64, label="Energy-saving\nsimulator" if eid == "A4"
            else ("Traffic-engineering\nApp" if eid == "A1" else None))
    ax.plot([0.30, 9.95], [1.70, 1.70], color="#8A9399", lw=1, ls=(0, (5, 3)), zorder=1)
    arrow((5.15, 1.54), (5.15, 2.08), both=True)
    note(5.27, 1.84, "REST :8000")

    # ---- kernel
    ax.add_patch(FancyBboxPatch((0.30, 2.08), 9.65, 2.28, boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor="#EEF3F6", edgecolor=REPO_EDGE, lw=1.6, zorder=2))
    ax.text(0.48, 2.28, "NDTwin kernel", fontsize=12.5, fontweight="bold", color=ACCENT, va="center", zorder=3)
    grid = [["B0", "B1", "B2"], ["B3", "B4", "B5"], ["B6", "B7", "B8"]]
    xs = [0.55, 3.72, 6.89]
    for r, row in enumerate(grid):
        for c, eid in enumerate(row):
            box(eid, xs[c], 2.46 + r * 0.62, 2.95, 0.50, bold=(eid == "B0"))

    # ---- tools column (separate repos), dashed divider
    ax.plot([10.20, 10.20], [0.80, 7.0], color="#8A9399", lw=1, ls=(0, (5, 3)), zorder=1)
    ax.text(10.45, 1.02, "Tools", fontsize=12.5, fontweight="bold", color=INK, va="center")
    for k, eid in enumerate(("E1", "E2", "E3", "E4", "E6")):
        box(eid, 10.45, 1.30 + k * 0.56, 2.60, 0.46, sub="cases via NFS" if eid == "E1" else None)
    arrow((9.98, 2.80), (10.45, 2.80), both=True)

    # ---- control-plane adapters. The planes are mirrored against the 827 figure (bmv2 left, OVS right) so the
    # traffic generator, which builds the OVS fabric and nothing else, can reach Mininet + OVS only.
    CY, CH = 4.98, 0.50
    box("C3", 0.40, CY, 1.20, CH, fs=9.5, label="Link heartbeat\nhelper")
    box("C2", 1.75, CY, 2.30, CH, bold=True)
    box("C1", 5.15, CY, 2.90, CH, bold=True)
    ax.plot([1.60, 1.75], [CY + CH / 2, CY + CH / 2], color=SEP_EDGE, lw=1.2, ls=(0, (3, 2)), zorder=4)
    arrow((2.30, 4.38), (2.30, CY), both=True)
    note(2.20, 4.66, "REST :8081", ha="right")
    arrow((6.60, 4.38), (6.60, CY), both=True)
    note(6.70, 4.66, "REST :8080")

    # ---- the three data planes (exactly one per run)
    PY, PH, PW = 6.02, 0.72, 2.70
    cx = {"D3": 1.90, "D2": 4.98, "D1": 7.95}
    for eid, c in cx.items():
        lab, _ = ELEMENTS[eid]
        dashed = eid == "D2"
        ax.add_patch(FancyBboxPatch((c - PW / 2, PY), PW, PH, boxstyle="round,pad=0,rounding_size=0.34",
                                    facecolor=WHITE, edgecolor=SEP_EDGE if dashed else INK, lw=1.4,
                                    ls=(0, (4, 3)) if dashed else "-", zorder=2))
        for k in range(3):
            sx = c - 0.98 + k * 0.70
            ax.add_patch(FancyBboxPatch((sx, PY + 0.16), 0.60, 0.40, boxstyle="round,pad=0,rounding_size=0.04",
                                        facecolor=WHITE, edgecolor=SEP_EDGE if dashed else INK, lw=1.1,
                                        ls=(0, (3, 2)) if dashed else "-", zorder=3))
            ax.text(sx + 0.30, PY + 0.36, {"D1": "OVS", "D2": "HW", "D3": "bmv2"}[eid], ha="center", va="center",
                    fontsize=9.5, color=SEP_EDGE if dashed else INK, zorder=4)
        ax.text(c, PY + PH + 0.24, lab, ha="center", va="center", fontsize=11.5, fontweight="bold",
                color=SEP_EDGE if dashed else INK, zorder=4)
    # the tag belongs to the physical plane: it sits beside that plane's name, on its own row
    ax.add_patch(FancyBboxPatch((cx["D2"] + 0.88, PY + PH + 0.11), 1.17, 0.26,
                                boxstyle="round,pad=0,rounding_size=0.12", facecolor=WHITE, edgecolor=ACCENT,
                                lw=1.4, ls=(0, (3, 2)), zorder=8))
    ax.text(cx["D2"] + 0.88 + 0.585, PY + PH + 0.24, "no run on record", ha="center", va="center", fontsize=10,
            color=ACCENT, style="italic", zorder=9)
    note((cx["D3"] + cx["D2"]) / 2 + 0.01, PY + PH / 2, "or", ha="center", fs=11, color=BODY)
    note((cx["D2"] + cx["D1"]) / 2 + 0.01, PY + PH / 2, "or", ha="center", fs=11, color=BODY)
    # "one data plane per run" is a note about all three planes: a bracket under all of them
    by = PY + PH + 0.55
    x0, x1 = cx["D3"] - PW / 2 + 0.10, cx["D1"] + PW / 2 - 0.10
    ax.plot([x0, x0, x1, x1], [by - 0.09, by, by, by - 0.09], color=BODY, lw=1.2, zorder=4)
    note((x0 + x1) / 2, by + 0.20, "one data plane per run", ha="center", fs=10.5, color=BODY)

    # control -> planes
    arrow((2.70, CY + CH), (2.70, PY), color=INK)
    note(2.80, 5.76, "P4Runtime")
    arrow((5.50, CY + CH), (5.50, PY), dashed=True, color=SEP_EDGE)
    note(5.60, 5.76, "OpenFlow 1.3")
    arrow((7.40, CY + CH), (7.40, PY), color=INK)
    note(7.50, 5.76, "OpenFlow 1.3")
    # telemetry up into the collector: the bmv2 plane's sFlow is built by the proxy, so its arrow starts at the
    # P4 proxy box; the others start at their plane
    arrow((3.10, CY), (3.10, 4.38), color=INK)
    note(3.20, 4.62, "sFlow, synthesised", ha="left")
    note(3.20, 4.80, "by the proxy", ha="left")
    arrow((4.65, PY), (4.65, 4.38), dashed=True, color=SEP_EDGE)
    note(4.75, 4.66, "sFlow", ha="left", color=SEP_EDGE)
    arrow((9.00, PY), (9.00, 4.38), color=INK)
    note(8.90, 4.66, "sFlow 1/256", ha="right")

    # the traffic generator builds the OVS fabric: its arrow goes to Mininet + OVS only; lab tool
    box("E5", 10.45, 6.02, 2.60, 0.50, sub="builds the OVS fabric")
    arrow((cx["D1"] + PW / 2 + 0.02, 6.27), (10.45, 6.27), both=True)
    box("E7", 10.45, 6.66, 2.60, 0.42)

    S.save_all(fig, OUTDIR, STEM)
    print(f"[out] {STEM}: {len(ELEMENTS)} boxes drawn")

    # companion .md
    rows = ["| id | label on the canvas | fill | evidence from architecture.txt |", "|---|---|---|---|"]
    fills = {"kernel": "kernel (blue)", "out": "outside the kernel (grey)", "dashed": "dashed white",
             "plane": "data plane (white)"}
    for eid in sorted(ELEMENTS):
        lab, style = ELEMENTS[eid]
        fill = fills[style] + (", dashed" if eid == "D2" else "")
        ev_txt = " ; ".join(ev[eid]).replace("|", "/")
        rows.append(f"| {eid} | {lab} | {fill} | {ev_txt} |")
    table = "\n".join(rows)
    text = f"""# `{STEM}` -- What NDTwin is, as built today (page P02)

[Co-developed with claude code -- Adam]

Evidence class: **READ**: code and documents at trunk 2ece656c (full 2ece656c4a280477209a09b6fb7a51304d38b8ff),
read with `git show 2ece656c:<path>`; sibling repos at their HEAD commits (Energy-Saving-App 9facb78,
Simulation-Platform-Manager b7efd93, Web-GUI f63a55c, Network-State-Recorder 850f61d,
Network-Traffic-Visualizer 9b56b30, Network-Traffic-Generator 6e3f388). Nothing in the drawing was run; the
physical network is drawn dashed and tagged "no run on record": there is no hardware run log in the kernel
tree, and the repo's own API document says only the physical power-state branch "has not been exercised"
(doc/2026-01-02_ndt_api.md:1598-1599).

## Data source

`figures_spec/architecture.txt` sha256 `{S.sha16(SPEC)}...`. The boxes are drawn in the generator; the spec is
read to check that every drawn element has an evidence entry, that its canvas title is the title drawn, that
the removed names do not return and that no repository tint or legend is asked for.

## What changed against the 827 figure (spec section 0)

1. "Local LLM (fine-tuning)" removed (no local-model code; the only LLM call is LLMAgent.cpp:138, OpenAI).
2. "Apps (using AI/ML model inference ...)" removed; the "simulation" apps box is the Energy-saving simulator.
3. Physical network kept, dashed, "no run on record".
4. New small box "ndt / ndtwin-lab" (lab lifecycle tool and root helper).
Also: "Data cache manager" is the module's real name, Historical data manager. Colours: kernel blue, everything
outside the kernel grey. There is no tint and no legend by which repository holds a box (template rule 7).

## REST, and its two exceptions

Apps and tools talk to the kernel over REST (:8000); the kernel talks REST to Ryu (:8080) and to the P4 proxy
(:8081). Two exceptions are written inside their boxes: simulation cases reach the Simulation platform manager
over NFS ("cases via NFS", Simulation-Platform-Manager@b7efd93 app.cpp:286), and the Network traffic generator
builds the OVS fabric itself ("builds the OVS fabric", Network-Traffic-Generator@6e3f388 testbed_topo.py:39-48),
which is why it has its own arrow to the data planes.

## Layout notes

- The data planes are mirrored against the 827 figure (bmv2 on the left, OVS on the right, with the P4 proxy
  and Ryu swapped to match) so that the Network traffic generator's double-headed arrow reaches Mininet + OVS
  only. The "sFlow, synthesised by the proxy" arrow starts at the P4 proxy box (C2), as the spec says. "one data
  plane per run" is a note under a bracket that spans all three planes; the "no run on record" tag sits beside
  the physical plane's name.

## Differences from the spec text

- Kernel modules are drawn as nine boxes (B0-B8); the spec allows dropping the inner detail if crowded, it
  was not needed. The "sFlow 1/256" label on the OVS plane is switch sampling; on the bmv2 plane the sFlow is
  synthesised by the proxy; the physical plane's sFlow is dashed (no run on record).
- OpenAI (E6) is drawn as a dashed outline in the tools column (external service, off by default); the spec
  lists keeping it as an open point for the orchestrator.

## Boxes and evidence

{table}

## Caveats (also in the speaker notes)

- Do not say NDTwin stays in sync with your production network: it mirrors a Mininet fabric it controls
  through its own Ryu app or P4 proxy.
- Exactly one data plane per run; mixing is refused (TopologyAndFlowMonitor.cpp:3425-3427).
"""
    S.write_companion(OUTDIR, STEM, __file__, text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
