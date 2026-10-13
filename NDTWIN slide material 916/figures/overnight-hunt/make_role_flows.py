#!/usr/bin/env python3
"""
make_role_flows.py -- the experiment method of each role, as a flowchart.

Adam 09-16: "把角色 1-12 的實驗方法都畫出流程圖來，一人一張，如果流程有重複畫一種就好".

Eleven roles ran (1-6, 8-12; there is no ROLE-7).  They collapse to SEVEN distinct methods,
because four personas were re-dispatched with the same method and a different setting:

    fig_f1_successor_first    ROLE-1              inherit a running lab, follow its own advice
    fig_f2_successor_verify   ROLE-6, ROLE-8      re-measure the same observations, fix in place
    fig_f3_restart_cycler     ROLE-2, ROLE-9      cycle up/down without cleaning
    fig_f4_second_operator    ROLE-4, ROLE-12     act in the middle of someone else's operation
    fig_f5_traffic_pusher     ROLE-5, ROLE-10     sustained rule updates, read every reply
    fig_f6_grad_student       ROLE-3              hand-edit the topology the system serves
    fig_f7_manual_follower    ROLE-11             execute the manual literally, nothing else

Where a method was used twice, the second use differs only in the SETTING -- that difference
is the one line under the chain, never a second chart.

Sources: each role's brief, scratch/overnight-2026-09-05/hunt-0911/ROLE-*.md (first line and
the mission section), and the round entries in 00-LEDGER.md.  Provenance per figure in the
companion .md files.

Drawing rules: 827 E2 palette.  916 rule 6: the slide carries the title and the figure.

[Co-developed with claude code -- Adam]

Regenerate:
    "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_role_flows.py
"""
import os

import matplotlib

assert matplotlib.__version__.startswith("3.10") or matplotlib.__version__.startswith("3.11"), \
    f"unexpected matplotlib {matplotlib.__version__}; re-verify the figures render as expected"

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["font.monospace"] = ["Courier New", "Liberation Mono", "DejaVu Sans Mono"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
WARNC, WARN_BG, WHITE = "#9C3B2E", "#FBF2F0", "#FFFFFF"
MONO = {"family": "monospace"}

W = 12.44


def canvas(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fill=WHITE, edge=INK, lw=1.0, ls="solid", z=2, radius=0.0):
    if radius:
        p = FancyBboxPatch((x + radius, y + radius), w - 2 * radius, h - 2 * radius,
                           boxstyle=f"round,pad={radius},rounding_size={radius}",
                           facecolor=fill, edgecolor=edge, linewidth=lw, linestyle=ls, zorder=z)
    else:
        p = Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge,
                      linewidth=lw, linestyle=ls, zorder=z)
    ax.add_patch(p)
    return p


def txt(ax, x, y, s, size=9.5, color=INK, weight="normal", ha="center", va="center",
        mono=False, z=5):
    kw = dict(MONO) if mono else {}
    return ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=z, **kw)


def arrow(ax, x1, y1, x2, y2, color=INK, lw=1.0, head=0.09, z=3):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), zorder=z,
                arrowprops=dict(arrowstyle=f"-|>,head_width={head*1.6},head_length={head*2.4}",
                                color=color, linewidth=lw, shrinkA=0, shrinkB=0,
                                joinstyle="miter"))


def save(fig, name):
    os.makedirs(HIRES, exist_ok=True)
    for ext, dpi in (("pdf", None), ("png", 300), ("svg", None)):
        fig.savefig(os.path.join(OUTDIR, f"{name}.{ext}"), facecolor=WHITE,
                    **({"dpi": dpi} if dpi else {}))
    fig.savefig(os.path.join(HIRES, f"{name}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"wrote {name}.{{pdf,png,svg}} + _hires/{name}.png")


def flow(name, who, axis, roles, steps, found=None, again=None):
    """One role's method: a chain of steps, the last one being what was watched.

    steps  -- list of (line1, line2); the LAST entry is drawn in accent as the observation
    again  -- None, or (label, text): the same method re-dispatched with a different setting

    No finding appears on these pages: the method and the bugs are separate sections of the
    deck (Adam 09-16).  `found` is kept in the data below as the provenance link only.
    """
    H = 3.32 if again is None else 4.02
    fig, ax = canvas(W, H)

    txt(ax, W / 2, 0.48, who, size=19, weight="bold", color=INK)
    txt(ax, 0.58, 0.48, roles, size=9.5, color=INK, weight="bold", ha="left", mono=True)
    txt(ax, W - 0.58, 0.48, axis, size=9.5, color=ACCENT, weight="bold", ha="right")

    n = len(steps)
    x0, gap = 0.58, 0.30
    bw = (W - 2 * x0 - (n - 1) * gap) / n
    top, bh = 1.12, 1.62

    for i, (l1, l2) in enumerate(steps):
        x = x0 + i * (bw + gap)
        last = (i == n - 1)
        box(ax, x, top, bw, bh,
            fill=ACCENT_BG if last else WHITE, edge=ACCENT if last else INK,
            lw=2.0 if last else 1.0, radius=0.05)
        # Adam 09-16: keep the black bold headings, drop the grey small text -- the step
        # numbers and the WATCH kicker are gone, so the phrase centres in its box.
        c = INK if last else BODY
        wgt = "bold" if last else "normal"
        if l2:
            txt(ax, x + bw / 2, top + bh / 2 - 0.19, l1, size=12.0, color=c, weight=wgt)
            txt(ax, x + bw / 2, top + bh / 2 + 0.19, l2, size=12.0, color=c, weight=wgt)
        else:
            txt(ax, x + bw / 2, top + bh / 2, l1, size=12.0, color=c, weight=wgt)
        if not last:
            arrow(ax, x + bw + 0.03, top + bh / 2, x + bw + gap - 0.03, top + bh / 2,
                  color=INK, lw=1.2)

    # (3) Adam 09-16: these pages introduce the METHOD.  What each role found belongs on the
    # bug pages, not here -- mixing the two is what made the deck read as one long bug list.
    if again is not None:
        lab, body = again
        ay = top + bh + 0.40
        box(ax, 0.58, ay, W - 1.16, 0.66, fill=PANEL, edge=RULE, lw=1.0, radius=0.05)
        txt(ax, W / 2, ay + 0.33, body, size=12.0, color=INK, weight="bold")

    save(fig, name)


# =========================================================================================
FLOWS = [
    dict(
        name="fig_f1_successor_first", who="The successor", axis="state × intent",
        roles="ROLE-1",
        steps=[("Inherit a lab", "someone left it running"),
               ("Read what the system", "advises you to do"),
               ("Do exactly that", "nothing clever"),
               ("Whose state", "did it touch?")],
        found="it deleted a fault someone else had set, and reported success"),
    dict(
        name="fig_f2_successor_verify", who="The successor, second visit",
        axis="state × time", roles="ROLE-6  ·  ROLE-8",
        steps=[("Take last night's", "findings, unchanged"),
               ("Rebuild", "with the fix in"),
               ("Re-run the same", "observations"),
               ("Fixed?", "and what else moved?")],
        found="the findings were fixed — and one fix had broken the bring-up command",
        again=("SAME METHOD, TWICE",
               "ROLE-6 checked three findings from the restart cycler; "
               "ROLE-8 checked the successor's own")),
    dict(
        name="fig_f3_restart_cycler", who="The restart cycler", axis="time × state",
        roles="ROLE-2  ·  ROLE-9",
        steps=[("Bring it up", ""),
               ("Tear it down", "and do not clean"),
               ("Repeat", "ten to twelve times"),
               ("Sample every round", "and overlap two on purpose")],
        found="an empty machine, and two instruments that would not say so",
        again=("SAME METHOD, TWICE",
               "ROLE-9 switched between 4 and 128 hosts on every cycle "
               "— 128 ran for the first time")),
    dict(
        name="fig_f4_second_operator", who="The second operator", axis="time",
        roles="ROLE-4  ·  ROLE-12",
        steps=[("A starts", "something long"),
               ("B acts", "in the middle of it"),
               ("Vary the gap", "between them"),
               ("Who won,", "and does either know?")],
        found="at the same millisecond, both were told the lab was theirs",
        again=("SAME METHOD, TWICE",
               "ROLE-12 made A's long action a LIVE teardown of ten switches, "
               "not an empty lab — nobody had measured that")),
    dict(
        name="fig_f5_traffic_pusher", who="The traffic pusher", axis="scale",
        roles="ROLE-5  ·  ROLE-10",
        steps=[("Bring up the fabric", ""),
               ("Push rule updates", "at a fixed rate"),
               ("Read the reply", "to every single one"),
               ("Reply vs", "what the switch holds")],
        found="every reply said accepted; a batch of them the switch never took",
        again=("SAME METHOD, TWICE",
               "ROLE-10 ran it on 128 hosts for a full hour "
               "— 7106 requests, 3599 seconds")),
    dict(
        name="fig_f6_grad_student", who="The graduate student", axis="intent × scale",
        roles="ROLE-3",
        steps=[("Export the topology", "the system itself serves"),
               ("Edit it the way", "someone in a hurry would"),
               ("Load it back", ""),
               ("Which mistakes", "were caught?")],
        found="none of them — and the same field is refused when it arrives by API"),
    dict(
        name="fig_f7_manual_follower", who="The manual follower", axis="intent × docs",
        roles="ROLE-11",
        steps=[("Open the manual", "and read only that"),
               ("Type what it says", "in order, nothing more"),
               ("Record every place", "output differs from text"),
               ("Never open", "the source code")],
        found="eight places where the manual and the tool disagree, in one round"),
]

if __name__ == "__main__":
    covered = set()
    for f in FLOWS:
        for r in f["roles"].replace("·", " ").split():
            if r.startswith("ROLE-"):
                covered.add(r)
    expect = {f"ROLE-{i}" for i in [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]}
    assert covered == expect, f"roles not covered: {expect - covered}; extra: {covered - expect}"
    print(f"{len(FLOWS)} distinct methods covering {len(covered)} roles (no ROLE-7)")
    for f in FLOWS:
        flow(**f)
