#!/usr/bin/env python3
"""
make_queued_readback.py -- fig_d2_queued_readback: one kernel batch install on a foreign P4
program, drawn as a sequence diagram, twice -- with roles.ipv4_route (the write lands) and
without roles (the same "200 queued", then the switch side refuses it).  The point: "queued"
is not "installed"; the outcome is read back afterwards.

Data (NDTwin-Kernel checkout): live-p1/runs/2026-09-26T202055Z_07_roles_basic, repo HEAD
b2eeb71d per its 01_binaries.txt -- an uncommitted observation (runs/ is not tracked):
    roles     40_batch_install.{code,json}  41_dispatch_install.json
              42_stats_flow_1_after_install.json
    no roles  74_batch_install_plain.{code,json}  75_dispatch_plain.json
              76_dispatch_global.json (read right after request 1)
The request body the script sent is 07_roles_basic.sh's INSTALL (b2eeb71d:824, trunk
3d740be0:873); the endpoint is its batch() (b2eeb71d:706, 3d740be0:755).  Every value on the
canvas is read from those files at run time and asserted; nothing is typed.  The manual lines
the .md cites (doc/2026-01-02_ndt_api.md:1754-1758, 1920-1928) are asserted at 3d740be0.

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/flow-api"
    nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_queued_readback.py
"""
import json
import os
import re
import subprocess
import sys

import matplotlib

assert matplotlib.__version__.startswith("3.11"), matplotlib.__version__
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["font.monospace"] = ["Courier New", "Liberation Mono", "DejaVu Sans Mono"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

REPO = os.environ.get("NDTWIN_REPO", "/home/adam/Desktop/NDTwin-Kernel")
TRUNK = "3d740be0"
RUN = os.path.join(REPO, "doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/"
                         "2026-09-26T202055Z_07_roles_basic")
SCRIPT = "doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/07_roles_basic.sh"
MANUAL = "doc/2026-01-02_ndt_api.md"

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")
STEM = "fig_d2_queued_readback"

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
WARNC, WHITE, GREEN, AMBER = "#9C3B2E", "#FFFFFF", "#2F7D4F", "#E3A21A"


def die(msg):
    raise SystemExit(f"make_queued_readback: {msg}")


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError as e:
        die(f"cannot read {path}: {e}")


def jload(name):
    try:
        with open(os.path.join(RUN, name)) as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        die(f"cannot read JSON {name}: {e}")


def code(name):
    return int(read(os.path.join(RUN, name)).strip())


def at(rev, path):
    p = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"], capture_output=True,
                       text=True)
    if p.returncode != 0:
        die(f"git show {rev}:{path}: {p.stderr.strip()}")
    return p.stdout.splitlines()


def evidence():
    head = re.search(r"^repo HEAD\s+([0-9a-f]{40})", read(os.path.join(RUN, "01_binaries.txt")),
                     re.M)
    if not head or not head.group(1).startswith("b2eeb71d"):
        die("the run is not on b2eeb71d")
    # what the script sent, and where (the run's own script version, and trunk's line numbers)
    for rev, ln_post, ln_body in (("b2eeb71d", 706, 824), (TRUNK, 755, 873)):
        s = at(rev, SCRIPT)
        if "/ndt/install_flow_entries_modify_flow_entries_and_delete_flow_entries" not in \
                s[ln_post - 1]:
            die(f"{SCRIPT}@{rev}:{ln_post} is not the batch endpoint")
        if '"ipv4_dst\\":\\"$PROBE_DST\\"' not in s[ln_body - 1] or \
                '\\"port\\":3' not in s[ln_body - 1]:
            die(f"{SCRIPT}@{rev}:{ln_body} is not the install body")
        if not any(ln.startswith('PROBE_DST="10.0.9.9"') for ln in s):
            die(f"{SCRIPT}@{rev}: PROBE_DST is no longer 10.0.9.9")
    # the manual's two passages
    man = at(TRUNK, MANUAL)
    if "Note on the flow-entry endpoints (9, 10, 11 and 23)" not in man[1753] or \
            "*accepted for programming*, not *programmed*" not in man[1756]:
        die(f"{MANUAL}:1754-1758 moved")
    if "A client cannot learn from this API whether a delete removed anything" not in man[1926] \
            or "is to read the rule back afterwards" not in man[1927]:
        die(f"{MANUAL}:1927-1928 moved")

    E = {}
    for side, post, disp in (("roles", "40_batch_install", "41_dispatch_install.json"),
                             ("plain", "74_batch_install_plain", "75_dispatch_plain.json")):
        c, b = code(post + ".code"), jload(post + ".json")
        if c != 200 or b.get("status") != "queued" or b.get("accepted") != 1:
            die(f"{side}: POST answered {c} {b.get('status')} accepted={b.get('accepted')}")
        d = jload(disp)
        if d.get("request_id") != b.get("request_id") or not d.get("complete"):
            die(f"{side}: dispatch record is not the POST's request, or not complete")
        E[side] = dict(code=c, status=b["status"], accepted=b["accepted"], rid=b["request_id"],
                       ok=d["counters"]["dispatched_ok"], failed=d["counters"]["dispatch_failed"],
                       acc=d["switch_outcome"]["accepted_by_switch"],
                       rej=d["switch_outcome"]["rejected_by_switch"])
    r, p = E["roles"], E["plain"]
    if (r["ok"], r["acc"], r["rej"]) != (1, 1, 0) or (p["ok"], p["acc"], p["rej"]) != (0, 0, 1):
        die(f"dispatch outcomes changed: roles {r}, plain {p}")
    # roles: read back from the proxy
    rows = jload("42_stats_flow_1_after_install.json").get("1") or []
    hit = [e for e in rows if e.get("match", {}).get("nw_dst") == "10.0.9.9"]
    if len(hit) != 1 or hit[0].get("actions") != ["OUTPUT:3"]:
        die(f"42: 10.0.9.9 read back as {hit}")
    r["readback"] = f"{hit[0]['match']['nw_dst']} → {hit[0]['actions'][0]}"
    # no roles: why, from the kernel's own failure record
    fails = jload("76_dispatch_global.json").get("recent_failures") or []
    f1 = [f for f in fails if f.get("match", {}).get("ipv4_dst") == "10.0.9.9"]
    if len(f1) != 1:
        die(f"76: {len(f1)} failure records for 10.0.9.9")
    f1 = f1[0]
    m = re.search(r'"outcome":"(\w+)","reason":"(\w+)"', f1.get("message", ""))
    if f1.get("controller_status") != 501 or not m:
        die(f"76: failure is {f1.get('controller_status')} {f1.get('message', '')[:80]}")
    p["status_code"], p["outcome"], p["reason"] = f1["controller_status"], m.group(1), m.group(2)
    if (p["outcome"], p["reason"]) != ("unsupported_on_p4", "unbound"):
        die(f"76: outcome/reason {p['outcome']}/{p['reason']}")
    # the later, cumulative read (76d) must still carry the same record
    if not any(x.get("seq") == f1.get("seq") and x.get("controller_status") == 501
               for x in jload("76d_dispatch_global.json").get("recent_failures") or []):
        die("76d no longer carries request 1's failure")
    print(f"[evidence] roles {r}\n[evidence] plain {p}")
    return E


def box(ax, x, y, w, h, fill=WHITE, edge=INK, lw=1.2, r=0.06, z=2):
    ax.add_patch(FancyBboxPatch((x + r, y + r), w - 2 * r, h - 2 * r,
                                boxstyle=f"round,pad={r},rounding_size={r}", facecolor=fill,
                                edgecolor=edge, linewidth=lw, zorder=z))


def txt(ax, x, y, s, size=12, color=INK, weight="normal", ha="center", va="center",
        mono=False, z=6):
    return ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va,
                   zorder=z, family="monospace" if mono else None)


def msg(ax, x0, x1, y, label, sub=None, reply=False, color=INK, lw=1.4, weight="normal",
        mono=False, hl=None, size=12):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>", mutation_scale=12,
                                 color=color, lw=lw, linestyle=(0, (4, 3)) if reply else "solid",
                                 shrinkA=0, shrinkB=0, zorder=3))
    xm = (x0 + x1) / 2
    t = txt(ax, xm, y - 0.15, label, size=size, color=color, weight=weight, mono=mono,
            va="bottom")
    if hl:
        t.set_bbox(dict(boxstyle="round,pad=0.3,rounding_size=0.15", facecolor=WHITE,
                        edgecolor=hl, linewidth=1.8))
    else:   # keep the dashed lifelines from showing through a label that crosses them
        t.set_bbox(dict(boxstyle="square,pad=0.08", facecolor=WHITE, edgecolor="none"))
    if sub:
        txt(ax, xm, y + 0.12, sub, size=10.5, color=MUTED, mono=True, va="top")


def panel(ax, px, head, E, side):
    xs = {"client": px + 0.75, "kernel": px + 3.2, "proxy": px + 5.35}
    names = {"client": "07 script", "kernel": "kernel", "proxy": "P4 proxy"}
    txt(ax, px + 0.05, 1.0, head, size=15, weight="bold", ha="left")
    top, bot = 1.35, 6.65
    for k, x in xs.items():
        box(ax, x - 0.72, top, 1.44, 0.44, fill=PANEL, edge=RULE, lw=1.0)
        txt(ax, x, top + 0.22, names[k], size=12.5, weight="bold")
        ax.plot([x, x], [top + 0.44, bot], color=RULE, lw=1.2, ls=(0, (3, 3)), zorder=1)
    c, k, p = xs["client"], xs["kernel"], xs["proxy"]
    d = E[side]
    msg(ax, c, k, 2.3, "POST batch install", sub="10.0.9.9 → port 3")
    msg(ax, k, c, 3.05, f"{d['code']}  {d['status']}", sub=f"request_id {d['rid']}", reply=True,
        weight="bold", hl=AMBER, size=12.5)
    if side == "roles":
        msg(ax, k, p, 3.75, "dispatch", color=MUTED, size=11.5)
        msg(ax, p, k, 4.15, "ok", reply=True, color=GREEN, weight="bold", size=11.5)
    else:
        msg(ax, k, p, 3.75, "dispatch", color=MUTED, size=11.5)
        msg(ax, p, k, 4.15, f"{d['status_code']}", reply=True, color=WARNC, weight="bold",
            size=11.5)
    msg(ax, c, k, 4.8, "GET dispatch status", sub=f"?request_id={d['rid']}")
    if side == "roles":
        msg(ax, k, c, 5.5, f"accepted_by_switch {d['acc']}", reply=True, color=GREEN,
            weight="bold", mono=True)
        msg(ax, c, p, 6.05, "GET /stats/flow/1", mono=False)
        msg(ax, p, c, 6.6, d["readback"], reply=True, color=GREEN, weight="bold", mono=True)
    else:
        msg(ax, k, c, 5.5, f"rejected_by_switch {d['rej']}", reply=True, color=WARNC,
            weight="bold", mono=True)
        msg(ax, c, k, 6.05, "GET dispatch status")
        msg(ax, k, c, 6.6, f"{d['status_code']} {d['outcome']}", reply=True, color=WARNC,
            weight="bold", mono=True, sub=f"reason {d['reason']}")


def main():
    E = evidence()
    W, H = 13.33, 7.0
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    ttl = '"queued" is not "installed": read it back'
    if len(ttl) > 45:
        die("title too long")
    txt(ax, 0.45, 0.48, ttl, size=22, weight="bold", ha="left")
    panel(ax, 0.45, "basic + roles", E, "roles")
    ax.plot([6.72, 6.72], [0.85, 6.9], color=RULE, lw=1.5)
    panel(ax, 6.95, "basic, no roles", E, "plain")
    os.makedirs(HIRES, exist_ok=True)
    for ext in ("pdf", "png", "svg"):
        kw = {"dpi": 300} if ext == "png" else {}
        fig.savefig(os.path.join(OUTDIR, f"{STEM}.{ext}"), facecolor=WHITE, **kw)
    fig.savefig(os.path.join(HIRES, f"{STEM}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"[out] {STEM}.{{pdf,png,svg}} + _hires/{STEM}.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
