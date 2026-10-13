#!/usr/bin/env python3
"""
make_flow_api_matrix.py -- fig_d1_flow_api_matrix: which data planes let the kernel API change
match-table rules at runtime (install / modify / delete), and what it can express there.

Two tables on one canvas, never mixed (rule 5 of the 930 template):
  * left, RAN IT: only what a live run's raw shows.  Every green or red cell is asserted
    against its raw file below; a cell with no live raw is drawn "not run" and claims nothing.
  * right, READ THE CODE: what the code at trunk 3d740be0 says each plane can match and do.
    Each string is asserted to still be in the file it paraphrases.

The two foreign-P4 rows (2026-09-26 roles run) are the new evidence and come first; the OVS row
(09-03) and NDTwin's-own-P4 row (08-24) are pre-09-16 background: their RAN IT cells are drawn
greyed inside a dated band (judge F-4, coordinator ruling 2026-09-27 UTC); their READ THE CODE
cells stay outside the band, since they read today's code at trunk 3d740be0 (second round).
The .md gives every path:line.

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/flow-api"
    "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_flow_api_matrix.py
"""
import json
import os
import sys

import matplotlib

assert matplotlib.__version__.startswith("3.11"), matplotlib.__version__
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

REPO = os.environ.get("NDTWIN_REPO", "/home/adam/Desktop/NDTwin-Kernel")
A = os.path.join(REPO, "doc/audit")
OVS_LOG = os.path.join(A, "2026-09-02_manual-usertest/run-06-opus/logs/d9-d11-flow-mutation.log")
FT_LOG = os.path.join(A, "2026-08-24_five-tuple-live/five_tuple_live.txt")
R07 = os.path.join(A, "2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/"
                      "2026-09-26T202055Z_07_roles_basic")
R08 = os.path.join(A, "2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/"
                      "2026-09-26T152605Z_08_heartbeat")
SRC = {
    "strategy": os.path.join(REPO, "src/ndt_core/routing_management/HttpRoutingStrategyBase.cpp"),
    "topo": os.path.join(REPO, "p4_proxy/proxy_agent/topology_manager.py"),
    "binding": os.path.join(REPO, "p4_proxy/proxy_agent/route_binding.py"),
    "routes": os.path.join(REPO, "p4_proxy/proxy_agent/api_routes.py"),
}

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")
STEM = "fig_d1_flow_api_matrix"

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
WHITE, GREEN, RED, GREY = "#FFFFFF", "#2F7D4F", "#9C3B2E", "#C9CDD0"


def die(msg):
    raise SystemExit(f"make_flow_api_matrix: {msg}")


def text(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def must(path, *needles):
    t = text(path)
    for n in needles:
        if n not in t:
            die(f"{path} no longer contains {n!r}")


def code(path):
    return int(text(path).strip())


def jload(path):
    with open(path) as f:
        return json.load(f)


# ---------------------------------------------------------------- the observed cells
def observed():
    cells = {}
    # row 1: OVS, run-06 D9/D11/D10 through the kernel's singular endpoints
    t = text(OVS_LOG)
    for step, verb, after in (("D9: POST /ndt/install_flow_entry", "install",
                               "actions=output:1"),
                              ("D11: POST /ndt/modify_flow_entry", "modify", "actions=output:2"),
                              ("D10: POST /ndt/delete_flow_entry", "delete", "gone from switch")):
        blk = t.split(step, 1)
        if len(blk) != 2 or '"status":"queued"' not in blk[1][:600] or after not in blk[1][:900]:
            die(f"OVS {verb}: {step} with queued + read-back {after!r} not found")
        cells[("ovs", verb)] = ("yes", "kernel API")
    # row 2: NDTwin's own P4, 08-24 five-tuple, posted to the proxy directly
    t = text(FT_LOG)
    if not ("install ONE 5-tuple rule" in t and "prio=101 match={'nw_dst': '10.0.0.2', "
            "'nw_proto': 6, 'tp_dst': 5001" in t and "delete it and confirm" in t):
        die("five-tuple install / read-back / delete not found")
    cells[("own", "install")] = ("yes", "proxy only")
    cells[("own", "delete")] = ("yes", "proxy only")
    # row 3: foreign P4 + roles.ipv4_route, L2 through the kernel batch endpoint
    for verb, req, disp, stats, want in (
            ("install", "40_batch_install", "41_dispatch_install",
             "42_stats_flow_1_after_install", True),
            ("delete", "43_batch_delete", "44_dispatch_delete",
             "45_stats_flow_1_after_delete", False)):
        if code(os.path.join(R07, req + ".code")) != 200 or \
                jload(os.path.join(R07, req + ".json")).get("status") != "queued":
            die(f"roles {verb}: kernel did not answer 200 queued")
        d = jload(os.path.join(R07, disp + ".json"))
        if d["switch_outcome"]["accepted_by_switch"] != 1:
            die(f"roles {verb}: not accepted_by_switch")
        flows = list(jload(os.path.join(R07, stats + ".json")).values())[0]
        has = any(e["match"].get("nw_dst") == "10.0.9.9" for e in flows)
        if has != want:
            die(f"roles {verb}: read-back 10.0.9.9 present={has}, wanted {want}")
        cells[("roles", verb)] = ("yes", "kernel API")
    # row 4: foreign P4 without roles: kernel queues, the switch-side answer is 501
    if jload(os.path.join(R07, "74_batch_install_plain.json")).get("status") != "queued":
        die("unbound: kernel did not answer queued")
    d = jload(os.path.join(R07, "75_dispatch_plain.json"))
    if d["switch_outcome"]["rejected_by_switch"] != 1:
        die("unbound: not rejected_by_switch")
    fails = jload(os.path.join(R07, "76d_dispatch_global.json"))["recent_failures"]
    if not any(f.get("controller_status") == 501 and "unsupported_on_p4" in f.get("message", "")
               for f in fails):
        die("unbound: no 501 unsupported_on_p4 in recent_failures")
    for p in (os.path.join(R07, "73_proxy_add.code"), os.path.join(R08, "66_proxy_add.code")):
        if code(p) != 501:
            die(f"{p} is not 501")
    cells[("unbound", "install")] = ("refused", "501")
    return cells


def read_only():
    must(SRC["strategy"], '"/stats/flowentry/add"', '"/stats/flowentry/delete_strict"')
    must(SRC["topo"], 'if action.get("type") == "OUTPUT":', "FIVE_TUPLE_FIELD_MAP")
    must(SRC["binding"], "only a destination route can be bound")
    must(SRC["routes"], '@router.post("/p4/table_entry")', "501  the entry needs a ternary",
         "not journaled", "a table / field / action / parameter this switch's p4info does")
    return {
        "ovs": ("OpenFlow match, passed on", "passed on to Ryu"),
        "own": ("dst IP  ·  5-tuple", "OUTPUT only"),
        "roles": ("dst IP", "the declared action"),
        "unbound": ("exact · lpm\nvia /p4/table_entry", "any in its p4info\nnot journaled"),
    }


def rbox(ax, x, y, w, h, fill, edge, lw=1.0, hatch=None):
    ax.add_patch(FancyBboxPatch((x + 0.09, y + 0.08), w - 0.18, h - 0.16,
                                boxstyle="round,pad=0.03,rounding_size=0.05", facecolor=fill,
                                edgecolor=edge, linewidth=lw, hatch=hatch, zorder=2))


def main():
    obs = observed()
    rd = read_only()
    for k, v in sorted(obs.items()):
        print(f"[observed] {k[0]:8s} {k[1]:8s} {v}")

    # new evidence (09-26) first; the two pre-09-16 rows sit in a greyed, dated background band
    # (judge F-4, coordinator ruling 2026-09-27 UTC)
    rows = [("roles", "foreign P4 + roles", "09-26", False),
            ("unbound", "foreign P4, no roles", "09-26", False),
            ("ovs", "OVS", "09-03", True),
            ("own", "NDTwin's own P4", "08-24", True)]
    verbs = ["install", "modify", "delete"]
    W, H = 13.33, 6.3
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    ax.text(0.45, 0.48, "Changing rules at runtime, per data plane", fontsize=22,
            fontweight="bold", color=INK, va="center")

    lx, top, rh = 2.95, 1.55, 0.86      # label column width, first row y, row height
    cw = 1.55
    rx0 = lx + 3 * cw + 0.55            # right table start
    rcw = [2.75, 2.25]
    band_gap = 0.55                     # room for the band's label
    ys = [top, top + rh, top + 2 * rh + band_gap, top + 3 * rh + band_gap]
    bg_top = ys[2] - 0.42
    # the band covers the RAN IT cells only: the READ THE CODE cells of those two rows are today's
    # code (trunk 3d740be0), not background (coordinator, 2026-09-27 UTC, second round)
    ax.add_patch(FancyBboxPatch((0.35, bg_top), (rx0 - 0.28 - 0.14) - 0.35,
                                ys[3] + rh - bg_top + 0.08,
                                boxstyle="round,pad=0.02,rounding_size=0.06",
                                facecolor="#F1F2F3", edgecolor=RULE, lw=1.0, zorder=0))
    ax.text(0.55, bg_top + 0.2, "BEFORE 09-16 · BACKGROUND", fontsize=11.5, color=FAINT,
            fontweight="bold", va="center")
    ax.text(lx, 1.02, "RAN IT", fontsize=12, color=FAINT, fontweight="bold", va="center")
    ax.text(rx0, 1.02, "READ THE CODE · trunk 3d740be0", fontsize=12, color=FAINT,
            fontweight="bold", va="center")
    for j, v in enumerate(verbs):
        ax.text(lx + j * cw + cw / 2, 1.33, v, fontsize=13.5, color=MUTED, ha="center",
                va="center")
    for j, h in enumerate(["matches", "actions"]):
        ax.text(rx0 + sum(rcw[:j]) + rcw[j] / 2, 1.33, h, fontsize=13.5, color=MUTED,
                ha="center", va="center")
    ax.plot([rx0 - 0.28, rx0 - 0.28], [0.85, ys[3] + rh], color=RULE, lw=1.5)

    OLDYES = "#A9AFB4"
    for (key, label, date, old), y in zip(rows, ys):
        ax.text(lx - 0.2, y + rh / 2 - 0.13, label, fontsize=14, color=MUTED if old else INK,
                ha="right", va="center")
        ax.text(lx - 0.2, y + rh / 2 + 0.2, date, fontsize=12, color=MUTED if old else INK,
                ha="right", va="center", fontweight="bold")
        for j, v in enumerate(verbs):
            x = lx + j * cw
            state, sub = obs.get((key, v), ("not run", ""))
            if state == "yes":
                fill = OLDYES if old else GREEN
                rbox(ax, x, y, cw, rh, fill, fill)
                ax.text(x + cw / 2, y + rh / 2 - (0.12 if sub else 0), "yes", fontsize=15,
                        color=WHITE, fontweight="bold", ha="center", va="center", zorder=5)
            elif state == "refused":
                rbox(ax, x, y, cw, rh, RED, RED)
                ax.text(x + cw / 2, y + rh / 2 - 0.12, "refused", fontsize=14.5, color=WHITE,
                        fontweight="bold", ha="center", va="center", zorder=5)
            else:
                rbox(ax, x, y, cw, rh, WHITE, GREY)
                ax.text(x + cw / 2, y + rh / 2, "not run", fontsize=12.5, color=FAINT,
                        ha="center", va="center", zorder=5)
            if sub:
                ax.text(x + cw / 2, y + rh / 2 + 0.2, sub, fontsize=11, color=WHITE,
                        ha="center", va="center", zorder=5)
        m, a = rd[key]
        for j, s_ in enumerate((m, a)):
            x = rx0 + sum(rcw[:j])
            rbox(ax, x, y, rcw[j], rh, PANEL, RULE)
            ax.text(x + rcw[j] / 2, y + rh / 2, s_, fontsize=12.5, color=BODY,
                    ha="center", va="center", zorder=5, linespacing=1.3)

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
