#!/usr/bin/env python3
"""
make_ndt_command_figs.py -- one page per `ndt` command (Adam 09-16: "一頁一個指令就好").

    fig_c1_up  fig_c2_down  fig_c3_status  fig_c4_clean  fig_c5_check
    fig_c6_apps  fig_c7_ntg  fig_c8_claim  fig_c9_release

`ndt` is the lab's front door: nine verbs that bring a fabric up, tear it down, and say what
is on the machine.  It is OUR OWN tool (tools/test_workflow/ndt, first committed 2026-08-21),
not part of the baseline kernel -- so these pages belong to the tooling section of the deck,
never to "baseline defects we fixed" (REPORT-PICK-FIXED.md section 0.3).

The exit codes are the point of these pages.  Before 09-12 they overlapped; the 09-12 round
gave each one a single meaning, the same meaning across up / down / clean:

    0  it did the thing            3  IT MEASURED NOTHING
    1  it measured, and the reading was dirty
    5  A GUARD REFUSED and nothing was done          2  usage error
    4  check only: the tripwire fired

Text is quoted from the tool's own `usage` block, tools/test_workflow/ndt:8316 onward, read
2026-09-16.  Literals only, so the output is byte-stable.

One phrase, one colour (Adam 09-16).

[Co-developed with claude code -- Adam]

Regenerate:
    "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_ndt_command_figs.py
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

# rc -> (colour, fill).  0 and 3 are both "no complaint", but they are not the same answer.
RC_STYLE = {
    "0": (ACCENT, ACCENT_BG), "1": (WARNC, WARN_BG), "2": (MUTED, PANEL),
    "3": (MUTED, PANEL), "4": (WARNC, WARN_BG), "5": (WARNC, WARN_BG),
}


def canvas(h):
    fig = plt.figure(figsize=(W, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(h, 0)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fill=WHITE, edge=INK, lw=1.0, ls="solid", z=2, radius=0.05):
    if radius:
        p = FancyBboxPatch((x + radius, y + radius), w - 2 * radius, h - 2 * radius,
                           boxstyle=f"round,pad={radius},rounding_size={radius}",
                           facecolor=fill, edgecolor=edge, linewidth=lw, linestyle=ls, zorder=z)
    else:
        p = Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge,
                      linewidth=lw, linestyle=ls, zorder=z)
    ax.add_patch(p)
    return p


def txt(ax, x, y, s, size=10.5, color=INK, weight="normal", ha="center", va="center",
        mono=False, z=5):
    kw = dict(MONO) if mono else {}
    return ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=z, **kw)


def save(fig, name):
    os.makedirs(HIRES, exist_ok=True)
    for ext, dpi in (("pdf", None), ("png", 300), ("svg", None)):
        fig.savefig(os.path.join(OUTDIR, f"{name}.{ext}"), facecolor=WHITE,
                    **({"dpi": dpi} if dpi else {}))
    fig.savefig(os.path.join(HIRES, f"{name}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"wrote {name}")


def page(name, verb, tagline, forms, codes, edge):
    """One command: the verb, what it is for, its forms, its exit codes, and the sharp edge.

    forms -- list of (invocation, what it gives you); may be empty
    codes -- list of (rc, meaning); rc is a single character key of RC_STYLE
    edge  -- the one thing an operator gets wrong, or None
    """
    # The canvas height is derived with the SAME arithmetic the drawing uses below; a
    # separate estimate got the odd-code case wrong and ran off the page (09-16).
    nforms = len(forms)
    ch_, crow = 0.78, 0.78 + 0.14
    nrows = (len(codes) + 1) // 2
    h = (1.44
         + ((0.36 + 0.42 * nforms + 0.16) if nforms else 0.0)
         + 0.34
         + nrows * crow + 0.22
         + ((0.80 + 0.34) if edge else 0.30))
    fig, ax = canvas(h)

    txt(ax, 0.58, 0.62, f"ndt {verb}", size=27, color=INK, weight="bold",
        ha="left", mono=True)
    txt(ax, W - 0.58, 0.62, tagline, size=13.0, color=BODY, ha="right")
    ax.plot([0.58, W - 0.58], [1.04, 1.04], color=INK, lw=1.2)

    y = 1.44
    if nforms:
        txt(ax, 0.58, y, "HOW YOU CALL IT", size=8.5, color=FAINT, weight="bold",
            ha="left", mono=True)
        y += 0.36
        for inv, gives in forms:
            txt(ax, 0.72, y, inv, size=12.0, color=INK, weight="bold", ha="left", mono=True)
            txt(ax, 4.60, y, gives, size=11.5, color=BODY, ha="left")
            y += 0.42
        y += 0.16

    txt(ax, 0.58, y, "WHAT ITS EXIT CODE MEANS", size=8.5, color=FAINT, weight="bold",
        ha="left", mono=True)
    y += 0.34
    cw, ch, gap = (W - 1.16 - 0.26) / 2, ch_, 0.26
    for i, (rc, meaning) in enumerate(codes):
        col, fill = RC_STYLE[rc]
        cx = 0.58 + (i % 2) * (cw + gap)
        cy = y + (i // 2) * (ch + 0.14)
        box(ax, cx, cy, cw, ch, fill=fill, edge=col, lw=1.4)
        txt(ax, cx + 0.42, cy + ch / 2, rc, size=19, color=col, weight="bold", mono=True)
        txt(ax, cx + 0.94, cy + ch / 2, meaning, size=11.5, color=INK, ha="left")
    y += ((len(codes) + 1) // 2) * (ch + 0.14) + 0.22

    if edge:
        box(ax, 0.58, y, W - 1.16, 0.80, fill=WARN_BG, edge=WARNC, lw=1.2)
        txt(ax, 0.94, y + 0.40, "THE SHARP EDGE", size=8.5, color=WARNC, weight="bold",
            ha="left", mono=True)
        txt(ax, 2.72, y + 0.40, edge, size=12.0, color=INK, weight="bold", ha="left")
        assert y + 0.80 <= h + 0.001, f"{name}: the edge band ends at {y + 0.80:.2f} of {h}"
    save(fig, name)


PAGES = [
    dict(name="fig_c1_up", verb="up", tagline="bring the whole lab up, and verify it",
         forms=[("ndt up", "Ryu and OVS, 128 hosts — OVS is the default plane"),
                ("ndt up 4", "the same, on the P4 test bed's 4-host layout"),
                ("ndt up p4 4", "the P4 plane at 4 hosts"),
                ("ndt up p4 128", "the P4 plane at 128 hosts")],
         codes=[("0", "it came up and it verified"),
                ("1", "it measured the machine and did not like it"),
                ("5", "a guard refused — nothing was built"),
                ("2", "you called it wrong")],
         edge="1 and 5 are different questions: 1 looked and disliked what it saw, "
              "5 never looked"),
    dict(name="fig_c2_down", verb="down", tagline="take it all down, and prove the machine is clean",
         forms=[("ndt down", "tear down, then assert the machine is clean"),
                ("ndt down --deep", "also kill whatever holds any port in the table")],
         codes=[("0", "the teardown finished and verified clean"),
                ("1", "a step failed, or something is still running"),
                ("3", "there was nothing to tear down"),
                ("5", "a guard refused — nothing was torn down")],
         edge="3 says this teardown measured nothing — it does not say the round ended clean"),
    dict(name="fig_c3_status", verb="status", tagline="what is running, and who has the lab",
         forms=[("ndt status", "what is on the machine right now"),
                ("ndt status --check", "compare it against the baseline this lab was brought up with")],
         codes=[("0", "every compared field matches"),
                ("1", "one of them does not"),
                ("3", "there was no baseline to compare against")],
         edge="with no baseline on disk the whole report is rc 3, not rc 0"),
    dict(name="fig_c4_clean", verb="clean", tagline="just the teardown assertion, on its own",
         forms=[],
         codes=[("0", "it had something to be about, and none of it is residue"),
                ("1", "residue is still there"),
                ("5", "a guard refused — a teardown is in flight")],
         edge="it refuses while another teardown is running, "
              "because that teardown is releasing the very ports it would report"),
    dict(name="fig_c5_check", verb="check", tagline="the telemetry double-count tripwire",
         forms=[],
         codes=[("0", "the ratio is inside the band, or nothing was compared"),
                ("4", "double-counting — the tripwire fired")],
         edge="rc 0 also means nothing was compared — the quiet answer and "
              "the healthy answer are the same number"),
    dict(name="fig_c6_apps", verb="apps", tagline="start the readers and apps, and find what they left",
         forms=[("ndt apps", "an interactive picker, when you are on a terminal"),
                ("ndt apps <names>", "start those readers"),
                ("ndt apps orphans", "what is still running that nobody is tracking")],
         codes=[("0", "nothing untracked"),
                ("1", "untracked processes are running"),
                ("2", "you called it wrong")],
         edge="read the tally line, not the exit code — that is what the readers were "
              "taught to judge by"),
    dict(name="fig_c7_ntg", verb="ntg", tagline="which prompt the topology hands control to",
         forms=[("ndt ntg cli", "hand control to the CLI"),
                ("ndt ntg prompt", "hand control to the topology's own prompt")],
         codes=[("0", "the choice was applied"), ("2", "you called it wrong")],
         edge=None),
    dict(name="fig_c8_claim", verb="claim", tagline="reserve the lab, so nobody tears it down under you",
         forms=[("ndt claim", "thirty minutes, the default"),
                ("ndt claim 75 \"<note>\"", "seventy-five minutes, and say what you are doing")],
         codes=[("0", "the lab is yours"),
                ("1", "somebody else holds it"),
                ("2", "NDT_OWNER is not set")],
         edge="two claims in the same millisecond were both granted, 2 times in 16 — "
              "there was no lock between the read and the write"),
    dict(name="fig_c9_release", verb="release", tagline="give the lab back",
         forms=[],
         codes=[("0", "released"), ("1", "you were not holding it")],
         edge="the claim is a courtesy, not a lock: it stops the honest, "
              "not a command that never asks"),
]

if __name__ == "__main__":
    assert len(PAGES) == 9, f"the tool has nine verbs, this has {len(PAGES)}"
    for p in PAGES:
        page(**p)
