#!/usr/bin/env python3
"""
make_p10_setup.py -- handson/fig_p10_setup: one task, two setups.  Page P10 of the 1021 deck.
Evidence class: READ (the topology from files; the highlighted path pair read from the NDTwin agent's own
development log, not re-run here).

Centre: the shared 10-switch / 4-host fabric drawn from H/topology.tsv (core s9 s10, aggregation s5-s8, edge
s1-s4, hosts on port 3).  Highlighted: the development pair of H/congestion/variants_dev.tsv (role A, h1 -> h3)
with the path its largest flow had before the move (solid, accent) and after it (dashed), both read from the
first `moving <flow>: <before>  ->  <after>` line of that pair in the NDTwin agent's development log
(H/congestion/raw/agent_ndtwin_dev/evidence/ctl7.log, the run its NOTES.txt cites).  A load glyph marks the
first switch-to-switch link of the before path.  Side panels: "NDTwin arm" (app -> REST :8000 -> NDTwin kernel ->
Ryu on OVS, P4 proxy on bmv2) and "DIY arm" (the app is a Ryu app inside stock Ryu 4.34 -> OpenFlow 1.3 -> OVS).
No numbers on the canvas but box names; bottom line "same wiring for both arms".

Stops with a named reason if: topology.tsv does not hold 10 switches, 16 switch-switch links and 4 hosts each on
port 3 of its edge switch; the dev variant has no role-A row; the log has no move line for that pair; a hop of the
before or after path is not a topology link on the port the log names; a path does not start at the source
host's edge switch or end at the destination host's port; before and after are the same path; the DIY agent's
log (H/congestion/raw/agent_diy_dev/ryu.log) has no base path for the pair, or a hop of it is not a topology link
(that path is recorded in the companion .md, not drawn).

[Co-developed with claude code -- Adam]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle_1021 as S  # noqa: E402
from figstyle_1021 import (ACCENT, ACCENT_BG, BODY, FAINT, INK, MUTED, PANEL, RULE, WHITE,  # noqa: E402
                           SEP_EDGE, SEP_FILL, plt)
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon  # noqa: E402

WHO = "make_p10_setup"
STEM = "fig_p10_setup"
TITLE = "Hands-on: one task, two setups"
H = "/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-10-08_why-ndtwin-handson"
args = sys.argv[1:]


def opt(name, default):
    return args[args.index(name) + 1] if name in args else default


TOPO = opt("--topology", os.path.join(H, "topology.tsv"))
VARIANTS = opt("--variants", os.path.join(H, "congestion", "variants_dev.tsv"))
DEVLOG = opt("--devlog", os.path.join(H, "congestion", "raw", "agent_ndtwin_dev", "evidence", "ctl7.log"))
DIYLOG = opt("--diylog", os.path.join(H, "congestion", "raw", "agent_diy_dev", "ryu.log"))
OUTDIR = opt("--out", os.path.join(S.DECK, "figures", "handson"))
RED = "#9C3B2E"


def load():
    sw_links, hosts = {}, {}
    if not os.path.exists(TOPO):
        S.die(WHO, f"topology.tsv not found: {TOPO}")
    for ln in open(TOPO, encoding="utf-8"):
        if ln.startswith("#") or not ln.strip():
            continue
        f = ln.rstrip("\n").split("\t")
        if len(f) != 5:
            S.die(WHO, f"topology.tsv line has {len(f)} fields, want 5: {ln.strip()!r}")
        kind, a, ap, b, bp = f
        if kind == "sw":
            sw_links[(a, int(ap))] = (b, int(bp))
            sw_links[(b, int(bp))] = (a, int(ap))
        elif kind == "host":
            hosts[a] = (b, int(bp))
        else:
            S.die(WHO, f"topology.tsv: unknown kind {kind!r}")
    switches = {k[0] for k in sw_links}
    if len(switches) != 10 or len(sw_links) != 32 or len(hosts) != 4:
        S.die(WHO, f"topology.tsv holds {len(switches)} switches, {len(sw_links) // 2} switch-switch links, "
                   f"{len(hosts)} hosts; the page draws 10 switches, 16 switch-switch links, 4 hosts")
    for h, (s, p) in hosts.items():
        if p != 3 or s != "s" + h[1:]:
            S.die(WHO, f"host {h} is on {s} port {p}; the page draws hN on sN port 3")
    pair = None
    for ln in open(VARIANTS, encoding="utf-8"):
        f = ln.rstrip("\n").split("\t")
        if not ln.startswith("#") and len(f) == 6 and f[0] == "dev" and f[1] == "A":
            pair = (f[2], f[3])
    if not pair:
        S.die(WHO, f"variants_dev.tsv has no dev role-A row: {VARIANTS}")
    src_ip, dst_ip = "10.0.0." + pair[0][1:], "10.0.0." + pair[1][1:]
    mv = None
    if not os.path.exists(DEVLOG):
        S.die(WHO, f"development log not found: {DEVLOG}")
    for ln in open(DEVLOG, encoding="utf-8"):
        m = re.search(r"moving (\S+?):\d+->(\S+?):\d+/tcp: (\S+)\s+->\s+(\S+)", ln)
        if m and m.group(1) == src_ip and m.group(2) == dst_ip:
            mv = (m.group(3), m.group(4))
            break
    if not mv:
        S.die(WHO, f"no move line for {pair[0]} -> {pair[1]} in {DEVLOG}")
    paths = []
    for which, txt in zip(("before", "after"), mv):
        hops = [(h.split(":")[0], int(h.split(":")[1])) for h in txt.split(">")]
        for (s, p), (ns, _) in zip(hops, hops[1:]):
            if sw_links.get((s, p), (None,))[0] != ns:
                S.die(WHO, f"{which} path hop {s}:{p} -> {ns} is not a topology link on that port")
        if hops[0][0] != hosts[pair[0]][0]:
            S.die(WHO, f"{which} path starts at {hops[0][0]}, not at {pair[0]}'s edge switch")
        if hops[-1] != hosts[pair[1]]:
            S.die(WHO, f"{which} path ends at {hops[-1]}, not at {pair[1]}'s port")
        paths.append([s for s, _ in hops])
    if paths[0] == paths[1]:
        S.die(WHO, "before and after are the same path")
    # the DIY app's base path for the same pair, from its own startup line (recorded in the .md, not drawn)
    diy = None
    if not os.path.exists(DIYLOG):
        S.die(WHO, f"DIY development log not found: {DIYLOG}")
    for ln in open(DIYLOG, encoding="utf-8"):
        m = re.search(r"base paths: (.*)$", ln)
        if m:
            for tok in m.group(1).split():
                a, _, p = tok.partition(":")
                if a in (f"{pair[0]}>{pair[1]}", f"{pair[1]}>{pair[0]}"):
                    diy = p.split("-") if a.startswith(pair[0]) else p.split("-")[::-1]
            break
    if not diy:
        S.die(WHO, f"no base path for {pair[0]} -> {pair[1]} in the DIY log {DIYLOG}")
    for u, v in zip(diy, diy[1:]):
        if not any(k[0] == u and nb[0] == v for k, nb in sw_links.items()):
            S.die(WHO, f"DIY base path hop {u} -> {v} is not a topology link")
    return sw_links, hosts, pair, paths, mv, diy


def box(ax, x, y, w, h, text, fill=WHITE, edge=SEP_EDGE, fs=12, bold=False, color=INK, sub=None, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.07", facecolor=fill,
                                edgecolor=edge, lw=1.4, ls=ls, zorder=3))
    if sub:
        ax.text(x + w / 2, y + h / 2 - 0.12, text, ha="center", va="center", fontsize=fs, color=color,
                fontweight="bold" if bold else "normal", zorder=4)
        ax.text(x + w / 2, y + h / 2 + 0.15, sub, ha="center", va="center", fontsize=10.5, color=MUTED, zorder=4)
    else:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color,
                fontweight="bold" if bold else "normal", zorder=4)


def arrow(ax, x0, y0, x1, y1, color=FAINT, lw=1.6):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=13, color=color, lw=lw,
                                 zorder=2, shrinkA=0, shrinkB=0))


def main():
    sw_links, hosts, pair, paths, mv, diy = load()
    W, Hh = 13.33, 6.6
    fig, ax = S.new_canvas(W, Hh)
    S.title(ax, TITLE, W)

    # ---------------- centre: the fabric
    col = {1: 5.25, 2: 6.25, 3: 7.65, 4: 8.65}
    pos = {}
    for i in range(1, 5):
        pos[f"s{i}"] = (col[i], 4.15)          # edge
        pos[f"h{i}"] = (col[i], 5.15)          # hosts
    for i, n in zip(range(1, 5), ("s5", "s6", "s7", "s8")):
        pos[n] = (col[i], 2.85)                # aggregation
    pos["s9"], pos["s10"] = (6.45, 1.6), (7.45, 1.6)
    seen = set()
    for (a, _), (b, _) in sw_links.items():
        if (b, a) in seen:
            continue
        seen.add((a, b))
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color=RULE, lw=1.6, zorder=1)
    for h, (s, _) in hosts.items():
        ax.plot([pos[h][0], pos[s][0]], [pos[h][1], pos[s][1]], color=RULE, lw=1.6, zorder=1)
    before, after = paths
    full_b = [pair[0]] + before + [pair[1]]
    full_a = [pair[0]] + after + [pair[1]]
    for p, ls, lw in ((full_b, "-", 4.2), (full_a, (0, (4, 2.5)), 3.2)):
        ax.plot([pos[n][0] for n in p], [pos[n][1] for n in p], color=ACCENT, lw=lw, ls=ls, zorder=2,
                solid_capstyle="round")
    # nodes
    for n, (x, y) in pos.items():
        on = n in full_b or n in full_a
        if n.startswith("h"):
            box(ax, x - 0.27, y - 0.2, 0.54, 0.4, n, fill=ACCENT if n in pair else WHITE,
                edge=ACCENT if n in pair else SEP_EDGE, fs=12, bold=n in pair, color=WHITE if n in pair else INK)
        else:
            ax.scatter([x], [y], s=780, color=ACCENT_BG if on else WHITE, edgecolors=ACCENT if on else SEP_EDGE,
                       linewidths=1.6, zorder=3)
            ax.text(x, y, n, ha="center", va="center", fontsize=11, color=INK, zorder=4,
                    fontweight="bold" if on else "normal")
    # load glyph on the first switch-switch link of the before path: three bars rising
    a, b = before[0], before[1]
    gx, gy = (pos[a][0] + pos[b][0]) / 2 - 0.52, (pos[a][1] + pos[b][1]) / 2 - 0.25
    for k, hgt in enumerate((0.14, 0.24, 0.34)):
        ax.add_patch(Polygon([(gx + k * 0.1, gy + 0.17), (gx + k * 0.1 + 0.07, gy + 0.17),
                              (gx + k * 0.1 + 0.07, gy + 0.17 - hgt), (gx + k * 0.1, gy + 0.17 - hgt)],
                             closed=True, color=RED, zorder=5))
    ax.text(gx + 0.135, gy + 0.45, "over\nthe limit", ha="center", va="center", fontsize=11, color=INK,
            linespacing=1.1)
    # path key under the fabric
    ky = 5.85
    ax.plot([5.2, 5.7], [ky, ky], color=ACCENT, lw=4.2)
    ax.text(5.8, ky, "largest flow, before", va="center", fontsize=11, color=BODY)
    ax.plot([7.55, 8.05], [ky, ky], color=ACCENT, lw=3.2, ls=(0, (4, 2.5)))
    ax.text(8.15, ky, "after the move", va="center", fontsize=11, color=BODY)
    ax.text(6.95, 6.3, "same wiring for both arms", ha="center", va="center", fontsize=12.5, color=INK,
            fontweight="bold")

    # ---------------- left: NDTwin arm
    lx, lw_ = 0.45, 3.55
    ax.text(lx, 1.15, "NDTwin arm", fontsize=15, fontweight="bold", color=INK, va="center")
    box(ax, lx, 1.5, lw_, 0.55, "your app", fill=ACCENT_BG, edge=ACCENT, bold=True)
    arrow(ax, lx + lw_ / 2, 2.05, lx + lw_ / 2, 2.4)
    box(ax, lx, 2.4, lw_, 0.5, "REST :8000", fill=WHITE, edge=ACCENT)
    arrow(ax, lx + lw_ / 2, 2.9, lx + lw_ / 2, 3.25)
    box(ax, lx, 3.25, lw_, 0.8, "NDTwin kernel", fill="#D3E4EE", edge=ACCENT, bold=True,
        sub="topology, base forwarding, flow views")
    arrow(ax, lx + 0.85, 4.05, lx + 0.85, 4.4)
    arrow(ax, lx + lw_ - 0.85, 4.05, lx + lw_ - 0.85, 4.4)
    box(ax, lx, 4.4, 1.7, 0.55, "Ryu (OVS)", fill=SEP_FILL)
    box(ax, lx + lw_ - 1.7, 4.4, 1.7, 0.55, "P4 proxy (bmv2)", fill=SEP_FILL)
    ax.text(lx + lw_ / 2, 5.35, "OVS + bmv2", ha="center", va="center", fontsize=13, fontweight="bold", color=ACCENT)

    # ---------------- right: DIY arm
    rx, rw = 9.35, 3.55
    ax.text(rx, 1.15, "DIY arm", fontsize=15, fontweight="bold", color=INK, va="center")
    ax.add_patch(FancyBboxPatch((rx, 1.5), rw, 1.55, boxstyle="round,pad=0,rounding_size=0.07", facecolor=SEP_FILL,
                                edgecolor=SEP_EDGE, lw=1.4, zorder=2))
    ax.text(rx + rw / 2, 2.82, "stock Ryu 4.34", ha="center", va="center", fontsize=12, color=INK, zorder=4)
    box(ax, rx + 0.25, 1.65, rw - 0.5, 0.95, "your app = a Ryu app", fill=WHITE, edge=SEP_EDGE, bold=True,
        sub="base forwarding, counters, moves")
    arrow(ax, rx + rw / 2, 3.05, rx + rw / 2, 3.4)
    box(ax, rx, 3.4, rw, 0.5, "OpenFlow 1.3", fill=WHITE)
    arrow(ax, rx + rw / 2, 3.9, rx + rw / 2, 4.4)
    box(ax, rx, 4.4, rw, 0.55, "OVS", fill=SEP_FILL)
    ax.text(rx + rw / 2, 5.35, "OVS only", ha="center", va="center", fontsize=13, fontweight="bold", color=MUTED)

    # both arms reach the same fabric
    arrow(ax, lx + lw_ + 0.1, 4.75, 4.75, 4.55, color=FAINT)
    arrow(ax, rx - 0.1, 4.75, 9.1, 4.55, color=FAINT)

    S.save_all(fig, OUTDIR, STEM)
    print(f"[out] {STEM}: pair {pair[0]} -> {pair[1]}; before {'-'.join(before)}; after {'-'.join(after)}")
    text = f"""# `{STEM}` -- {TITLE} (page P10)

[Co-developed with claude code -- Adam]

Evidence class: **READ** (topology read from files; the highlighted before/after paths read from a development
log of the NDTwin agent, not re-run here). Nothing on this figure is a trial result.

## Data source

- Fabric: `{TOPO}` sha256 `{S.sha16(TOPO)}...` (10 switches, 16 switch-switch links, 4 hosts on port 3; the same
  wiring as setting/StaticNetworkTopology{{P4,OVS}}_10Switches_4Hosts.json and tools/test_workflow/ovs_4host_topo.py,
  checked offline in H/raw/helper_topo_vs_tsv.txt).
- Pair: `{VARIANTS}` sha256 `{S.sha16(VARIANTS)}...`, dev role A = {pair[0]} -> {pair[1]} (the development
  workload handed to both agents).
- Paths: `{DEVLOG}` sha256 `{S.sha16(DEVLOG)}...` (the NDTwin agent's dev run on OVS that its NOTES.txt cites),
  first move line of that pair: `{mv[0]}  ->  {mv[1]}` (switch:egress-port hops). Before =
  {'-'.join(before)}; after = {'-'.join(after)}. Every hop is checked against topology.tsv. The DIY app's base
  routing chose {'-'.join(diy)} for this pair (read at run time from `{DIYLOG}` sha256 `{S.sha16(DIYLOG)}...`,
  its startup "base paths" line); the figure shows one real example, the NDTwin arm's, not every arm's path.

## Encoding

- Grey lines: every link of topology.tsv. Solid accent: the largest flow before the move; dashed accent: after.
- Red bars: a load glyph on the first switch-to-switch link of the before path (all links of that path carried
  the three flows; the task threshold is 40 Mbit/s per direction, TASK.txt).
- The kernel box says "base forwarding": on OVS it is NDTwin's own Ryu app (intelligent_router.py) that installs
  it, on bmv2 the P4 proxy; the developer of the NDTwin arm writes none of it.
- Side panels: NDTwin arm = app -> REST :8000 -> NDTwin kernel -> Ryu (OVS) or P4 proxy (bmv2); DIY arm = the app is
  a Ryu application inside stock Ryu 4.34, speaking OpenFlow 1.3 to OVS. Both arms run the same fabric file
  (ovs_4host_topo.py through the lab helper); the NDTwin arm also runs the same wiring on bmv2.
"""
    S.write_companion(OUTDIR, STEM, __file__, text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
