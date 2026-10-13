#!/usr/bin/env python3
"""
make_coverage_0930.py -- fig_t1c_ndtwin_coverage: the T1 page re-cut after the judge audit of 2026-09-27 UTC
(F-2).  The 13x16 requirements block of fig_t1b is gone (it is the 916 deck's page 3); what is
left is what changed since 09-16, in three titled panels so that ran and read never share one:

  BACKGROUND · READ THE CODE   NDTwin 09-16 row = the 916 deck's "NDTwin today" row (GAP-2
                          section 1, all read from NDTwin's own P4 at trunk 1a284f75; the reading
                          is from 09-08, shown on 09-16) -- drawn inside a grey background band
  RAN · JUDGED · 09-27 · exercise's P4   NDTwin 09-27 row (GAP-2b section 1: judgements made on
                          ran evidence); cells whose evidence is read-only are hatched and must be
                          "cannot" (legend "cannot · read only"); the two judgement cells were
                          ruled by Adam on 2026-09-28 (GAP-2b marks them "（Adam 2026-09-28 裁定）")
  T06 · 09-27             13 exercises x (runs on NDTwin: RAN IT; twin sees it: JUDGED) from
                          GAP-2b section 3, checked arm by arm against T06.  flowcache's "twin sees
                          it" is drawn "IPv4 only" (the same label as the T7 page), not GAP-2b's
                          "sees it": in T06 the flow did leave s1, on s1-eth3, the twin read it
                          there and read 0 on every s3 interface -- which is where the bytes went
                          (netdev) -- and nothing was delivered to h3 (coordinator ruling,
                          2026-09-27 UTC, second round; Adam's ruling 2026-09-28 put the same
                          value into GAP-2b, so there is no override any more).

All parsing and all consistency checks are the ones of make_tutorial_figs_0927.py (imported,
not copied), so the two figures cannot disagree on a cell except where this script says so.

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/p4-tutorials"
    "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_coverage_0930.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_tutorial_figs_0927 as T  # noqa: E402  (parsers, constants, T06 checks)

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")
STEM = "fig_t1c_ndtwin_coverage"
TITLE = "What NDTwin covered: 09-16 vs 09-27"          # 35 chars

INK, MUTED, FAINT, RULE, WHITE = "#1A1A1A", "#4F4F4F", "#6E6E6E", "#D0D0D0", "#FFFFFF"
PEND_EDGE = "#1A1A1A"
BAND = "#F1F2F3"          # the background band, as on fig_d1

FC_LU = T.REPO / ("doc/audit/2026-09-04_p4-tutorial-exercise-prep/runs/"
                  "2026-09-27T081256Z_flowcache_solution_ndtwin/link_usage")
FLOWCACHE_ONPATH = FC_LU / "onpath.txt"
RULED = "（Adam 2026-09-28 裁定）"      # GAP-2b's mark on the four cells Adam ruled
FLOWCACHE_TWIN = FC_LU / "twin_integral.txt"
FLOWCACHE_CLIENT = FC_LU / "iperf_client.txt"
FLOWCACHE_SERVER = FC_LU / "iperf_server.txt"
FLOWCACHE_NETDEV = (FC_LU / "netdev.before", FC_LU / "netdev.after")


def die(msg):
    raise SystemExit(f"make_coverage_0930: {msg}")


def flowcache_t06_reading():
    """The T06 flowcache G1 raw, read the way the twin cell is drawn ("IPv4 only"):
    the twin's own reading (twin_integral.txt) is > 0 on s1-eth3 and 0 on every s3 interface;
    the interface counters agree (s1-eth3 carried the flow, s3-eth1 towards h3 moved < 1 kB);
    onpath.txt names s1-eth3 alone; and nothing was delivered to h3 (no server report row, the
    client never got the server's ack).  Any of these changing stops the script."""
    twin = {}
    for ln in T.read(FLOWCACHE_TWIN).splitlines():
        p = ln.split()
        if len(p) >= 2 and not ln.startswith("#"):
            twin[p[0]] = float(p[1])
    if not twin.get("s1-eth3", 0) > 0:
        die(f"flowcache twin_integral.txt: s1-eth3 is not > 0 ({twin.get('s1-eth3')}) -- "
            "the twin no longer read the flow where it went")
    s3 = {k: v for k, v in twin.items() if k.startswith("s3-")}
    if len(s3) != 3 or any(v != 0 for v in s3.values()):
        die(f"flowcache twin_integral.txt: the s3 interfaces are not all 0: {s3}")
    nd = []
    for f in FLOWCACHE_NETDEV:
        nd.append({p[0]: int(p[1]) for p in (ln.split() for ln in T.read(f).splitlines())
                   if len(p) == 2 and p[1].isdigit()})
    d_s1 = nd[1]["s1-eth3"] - nd[0]["s1-eth3"]
    d_h3 = nd[1]["s3-eth1"] - nd[0]["s3-eth1"]
    if not (d_s1 > 1_000_000 and d_h3 < 1_000):
        die(f"flowcache netdev: s1-eth3 +{d_s1} B, s3-eth1 +{d_h3} B -- no longer 'left s1 on "
            "s1-eth3, not delivered towards h3'")
    onpath = [ln.split() for ln in T.read(FLOWCACHE_ONPATH).splitlines() if ln.strip()]
    if [p[0] for p in onpath if len(p) >= 2 and p[1] == "P"] != ["s1-eth3"]:
        die(f"flowcache onpath.txt is not 's1-eth3 only': {onpath}")
    if "did not receive ack of last datagram" not in T.read(FLOWCACHE_CLIENT):
        die("flowcache iperf client no longer reports the missing server ack")
    if " sec " in T.read(FLOWCACHE_SERVER):
        die("flowcache iperf_server.txt now has a report row")
    return (f"twin s1-eth3 {twin['s1-eth3']:.1f}, s3 all 0; netdev s1-eth3 +{d_s1} B, "
            f"s3-eth1 +{d_h3} B; server report missing")


def main():
    gap2b = T.read(T.GAP2B)
    cap_old, _r0, _b0, _w0, chk_old = T.parse_gap2(T.read(T.GAP2), "GAP-2")
    cap_new, _r1, basis, where, chk_new = T.parse_gap2(gap2b, "GAP-2b")
    strip, chk_strip = T.parse_gap2b_s3(gap2b, "GAP-2b")
    if T.T06_REL not in gap2b:
        die(f"GAP-2b does not name {T.T06_REL}")
    t06_checks = T.check_against_t06(strip, T.read_t06(T.T06))
    order, _stage, _note = T.parse_row_order(T.read(T.GAPA))

    read_only = [d for d in T.DIMS if "【跑過】" not in basis[d] + where[d]]
    judged_dims = [d for d in T.DIMS if "(judgement)" in basis[d]]
    judged_ex = [e for e in order if strip[e]["twin_judgement"]]
    ruled_dims = [d for d in T.DIMS if RULED in basis[d]]
    ruled_ex = [e for e in order if RULED in strip[e]["twin_raw"]]
    if sorted(read_only) != ["digest", "meters"]:
        die(f"read-only 09-27 cells moved: {read_only}")
    # the legend draws read-only cells as the "cannot" fill plus a cross hatch, labelled
    # "cannot · read only" -- so every read-only cell must be "cannot" in GAP-2b
    not_cannot = [d for d in read_only if cap_new[d] != T.CAP_NO]
    if not_cannot:
        die(f"read-only 09-27 cells that are not 'cannot': {not_cannot}")
    # Adam ruled the four judgement cells on 2026-09-28: none may still be open, and the ruled ones
    # are exactly the four
    if judged_dims or judged_ex:
        die(f"cells still marked (judgement) after Adam's 09-28 ruling: {judged_dims} {judged_ex}")
    if sorted(ruled_dims) != ["queue_metadata", "registers"] or \
            sorted(ruled_ex) != ["flowcache", "multicast"]:
        die(f"the four ruled cells moved: {ruled_dims} {ruled_ex}")
    why = flowcache_t06_reading()
    twin = {e: strip[e]["twin"] for e in order}
    if twin["flowcache"] != T.TWIN_IPV4:
        die(f"GAP-2b's flowcache twin cell is not 'IPv4 only' as ruled ({twin['flowcache']})")
    for c in [chk_old, chk_new, chk_strip] + t06_checks:
        print("[check] " + c)
    cnt = lambda cap: [sum(1 for d in T.DIMS if cap[d] == k)
                       for k in (T.CAP_YES, T.CAP_PARTIAL, T.CAP_NO)]
    c_old, c_new = cnt(cap_old), cnt(cap_new)
    t_cnt = [sum(1 for e in order if twin[e] == k) for k in (T.TWIN_YES, T.TWIN_IPV4, T.TWIN_NONE)]
    runs_yes = sum(1 for e in order if strip[e]["runs"] == T.RUN_YES)
    print(f"[counts] 09-16 {c_old}  09-27 {c_new}  runs {runs_yes}/13  twin {t_cnt} "
          f"(flowcache as ruled: {why})")

    # ---------------------------------------------------------------- draw
    W, H = 13.33, 6.7
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    ax.text(0.45, 0.48, TITLE, fontsize=22, fontweight="bold", color=INK, va="center")
    ax.text(W - 0.45, 0.52, "as of GAP-2b with Adam's 2026-09-28 ruling", fontsize=11, color=FAINT,
            ha="right", va="center")

    def tile(x, y, w, h, key, hatch=None, pending=False):
        ax.add_patch(Rectangle((x + 0.02, y + 0.02), w - 0.04, h - 0.04,
                               facecolor=T.FILL[key], edgecolor=T.EDGE.get(key, T.FILL[key]),
                               lw=0.8, hatch=hatch))
        if pending:
            ax.add_patch(Rectangle((x + 0.05, y + 0.05), w - 0.10, h - 0.10, facecolor="none",
                                   edgecolor=PEND_EDGE, lw=1.6, ls=(0, (2, 1.5)), zorder=5))

    x0, cw, rh = 2.35, 0.40, 0.48
    ya, yb = 1.55, 2.95
    # the 09-16 row is background: the 916 deck's row, read on 09-08 at trunk 1a284f75
    ax.add_patch(FancyBboxPatch((0.30, ya - 0.50), 9.45, rh + 0.95,
                                boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor=BAND, edgecolor=RULE, lw=0.9, zorder=0))
    ax.text(x0, ya - 0.22, "BACKGROUND · READ THE CODE · NDTwin's own P4", fontsize=12,
            color=FAINT, fontweight="bold", va="bottom")
    ax.text(x0, ya + rh + 0.22, "as shown 09-16; read 09-08, trunk 1a284f75", ha="left",
            va="center", fontsize=10.5, color=MUTED)
    ax.text(x0, yb - 0.22, "RAN · JUDGED · 09-27 · each exercise's own P4 on the NDTwin fabric", fontsize=12,
            color=FAINT, fontweight="bold", va="bottom")
    for yy, lab, cap, counts in ((ya, "NDTwin 09-16", cap_old, c_old),
                                 (yb, "NDTwin 09-27", cap_new, c_new)):
        ax.text(x0 - 0.12, yy + rh / 2, lab, ha="right", va="center", fontsize=13.5,
                fontweight="bold", color=INK)
        for j, d in enumerate(T.DIMS):
            ro = cap is cap_new and d in read_only
            tile(x0 + j * cw, yy, cw, rh, cap[d], hatch="xx" if ro else None,
                 pending=(cap is cap_new and d in judged_dims))
        ax.text(x0 + 16 * cw + 0.12, yy + rh / 2, " / ".join(str(c) for c in counts),
                ha="left", va="center", fontsize=13, color=INK, fontweight="bold")
    for j, d in enumerate(T.DIMS):
        ax.text(x0 + j * cw + cw / 2, yb + rh + 0.12, d, rotation=50, ha="right", va="top",
                fontsize=11, color=INK, rotation_mode="anchor")
    ax.text(x0 + 16 * cw + 0.12, yb + rh + 0.08, "can / partial\n/ cannot", fontsize=10.5,
            color=MUTED, ha="left", va="top", linespacing=1.1)

    # right panel: T06
    rx, rcw, rrh = 11.25, 0.92, 0.305
    ry0 = 1.72
    ax.plot([9.95, 9.95], [1.1, ry0 + 13 * rrh + 0.4], color=RULE, lw=1.5)
    ax.text(10.2, 1.02, "T06 · 09-27", fontsize=12, color=FAINT, fontweight="bold",
            va="bottom")
    for k, (panel, lab) in enumerate((("RAN IT", "runs on\nNDTwin"), ("JUDGED", "twin\nsees it"))):
        ax.text(rx + k * rcw + rcw / 2, ry0 - 0.50, panel, ha="center", va="bottom", fontsize=11,
                color=FAINT, fontweight="bold")
        ax.text(rx + k * rcw + rcw / 2, ry0 - 0.06, lab, ha="center", va="bottom", fontsize=11,
                color=MUTED, linespacing=1.1)
    for i, e in enumerate(order):
        y = ry0 + i * rrh
        ax.text(rx - 0.1, y + rrh / 2, e, ha="right", va="center", fontsize=11.5, color=INK)
        tile(rx, y, rcw, rrh, strip[e]["runs"])
        tile(rx + rcw, y, rcw, rrh, twin[e], hatch=T.HATCH.get(twin[e]),
             pending=e in judged_ex)
    ax.text(rx + rcw / 2, ry0 + 13 * rrh + 0.12, f"{runs_yes}/13", ha="center", va="top",
            fontsize=12.5, fontweight="bold", color=INK)
    ax.text(rx + rcw * 1.5, ry0 + 13 * rrh + 0.12, " / ".join(str(c) for c in t_cnt),
            ha="center", va="top", fontsize=12.5, fontweight="bold", color=INK)

    # legends (legend entries only), two rows under the left panels
    rows = [[(T.CAP_YES, "can do / yes", None, False), (T.CAP_PARTIAL, "partial / IPv4 only", None, False),
             (T.CAP_NO, "cannot", None, False)],
            [(T.TWIN_NONE, "no evidence", "////", False), (T.CAP_NO, "cannot · read only", "xx", False)]]
    for r, items in enumerate(rows):
        ly = 5.45 + r * 0.45
        for k, (key, lab, hatch, pend) in enumerate(items):
            lx = x0 + k * 2.35
            if pend:
                ax.add_patch(Rectangle((lx, ly - 0.12), 0.32, 0.24, facecolor=WHITE,
                                       edgecolor=PEND_EDGE, lw=1.6, ls=(0, (2, 1.5))))
            else:
                ax.add_patch(Rectangle((lx, ly - 0.12), 0.32, 0.24, facecolor=T.FILL[key],
                                       edgecolor=T.EDGE.get(key, T.FILL[key]), lw=0.8,
                                       hatch=hatch))
            ax.text(lx + 0.42, ly, lab, fontsize=11.5, color=MUTED, va="center")

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
