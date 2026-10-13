#!/usr/bin/env python3
"""
make_roadmap.py -- fig_n1_roadmap: the road from the first cut to "bring your own .p4".

Each step's status is COMPUTED from git at run time (read-only):
  done         the step's merge commit is an ancestor of trunk AT (the refresh's trunk commit);
  in progress  a branch for it exists and is not merged into trunk (or, for the GUI side of the
               third cut, into the Web-GUI repo's main);
  later        nothing in git yet (the step's source is a ruling or an analysis, cited in .md).
So the picture cannot claim a merge that did not happen.  The canvas carries the trunk commit
and its date (UTC) the statuses were computed against.

2026-09-28 UTC refresh: the third cut's kernel side merged (85bec430); its GUI side is a draft
branch in the Web-GUI repo, so the step is drawn as two boxes.

The deck version leaves out the unmerged external detect-only step (coordinator, 2026-09-27 UTC,
second round: not to be described outside until Adam decides).  `--with-detect-only` draws the
archive-only variant with that step, as fig_n1_roadmap_with_detect_only.*, so it can go back in
quickly.

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/next"
    "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_roadmap.py
"""
import os
import subprocess
import sys

import matplotlib

assert matplotlib.__version__.startswith("3.11"), matplotlib.__version__
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

REPO = os.environ.get("NDTWIN_REPO", "/home/adam/Desktop/NDTwin-Kernel")
WEBGUI = os.environ.get("NDTWIN_WEBGUI", "/home/adam/Web-GUI")
# the trunk commit the statuses are computed against: the deck refresh's state (the public trunk
# head of the 09-28 refresh), not the moving `trunk` ref; a later refresh bumps it
AT = "3368412d"
OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")
WITH_DETECT_ONLY = "--with-detect-only" in sys.argv[1:]
STEM = "fig_n1_roadmap_with_detect_only" if WITH_DETECT_ONLY else "fig_n1_roadmap"

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
WHITE, GREEN, AMBER, GREY = "#FFFFFF", "#2F7D4F", "#E3A21A", "#C9CDD0"

# (label, sub-label, merge sha or None, branch or None, repo the branch is in: None = the kernel)
STEPS = [
    ("cut 1", "NDTwin writes the\nroute table (roles)", "572d9462", None, None),
    ("cut 2", "heartbeat: detect\n+ reroute", "cafd518a", None, None),
    ("cut 3", "capabilities on\nthe graph API", "85bec430", None, None),
    ("cut 3 GUI", "GUI greys out\nwhat a switch lacks", None, "draft/p4-capabilities-0924", "webgui"),
    ("next", "twin sees\ncustom headers", None, None, None),
    ("later", "multi-table roles\n(load_balance)", None, None, None),
]
if WITH_DETECT_ONLY:
    STEPS.insert(2, ("cut 2b", "detect-only for\nexternal controllers", None,
                     "feat/external-detect-only-0927", None))
GOAL = "bring your own .p4"


def die(msg):
    raise SystemExit(f"make_roadmap: {msg}")


def git(*args, repo=None):
    env = dict(os.environ, TZ="UTC", GIT_OPTIONAL_LOCKS="0")   # dates in UTC, like fig_o1
    return subprocess.run(["git", "-C", repo or REPO, *args], capture_output=True, text=True,
                          env=env)


def status(sha, branch, where):
    repo, into = (WEBGUI, "main") if where == "webgui" else (REPO, AT)
    if sha:
        if git("merge-base", "--is-ancestor", sha, AT).returncode != 0:
            die(f"{sha} is not in trunk {AT}")
        date = git("show", "-s", "--format=%cd", "--date=format-local:%m-%d", sha).stdout.strip()
        return "done", f"merged {date} UTC"
    if branch:
        if git("rev-parse", "--verify", "--quiet", branch, repo=repo).returncode != 0:
            die(f"branch {branch} does not exist in {repo}")
        if git("merge-base", "--is-ancestor", branch, into, repo=repo).returncode == 0:
            die(f"branch {branch} is already merged into {into} of {repo} -- update the figure")
        return "progress", "on a branch"
    return "later", "not started"


def main():
    rows = []
    for lab, sub, sha, br, where in STEPS:
        st, tag = status(sha, br, where)
        rows.append((lab, sub, st, tag))
        print(f"[step] {lab:9s} {st:9s} {tag}  ({sha or br or '-'}{' in ' + WEBGUI if where else ''})")
    head = git("rev-parse", "--short=8", AT).stdout.strip()
    when = git("show", "-s", "--format=%cd", "--date=format-local:%Y-%m-%d %H:%M", AT).stdout.strip()
    if not head or not when:
        die(f"cannot read trunk {AT}'s sha and date")
    print(f"[state] trunk {head}, committed {when} UTC")

    W, H = 13.33, 6.4
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    ax.text(0.45, 0.48, "The road to “bring your own .p4”", fontsize=22, fontweight="bold",
            color=INK, va="center")
    ax.text(W - 0.45, 0.52, f"as of trunk {head} · {when} UTC", fontsize=11, color=FAINT,
            ha="right", va="center")
    style = {"done": (GREEN, GREEN, WHITE, "solid"),
             "progress": (WHITE, AMBER, INK, "solid"),
             "later": (WHITE, GREY, BODY, (0, (4, 3)))}
    n = len(rows)
    gap, bh, x0, goal_w = 0.24, 1.55, 0.45, 1.9
    bw = min(1.52, (W - 2 * x0 - goal_w - n * gap) / n)
    base, rise = 5.55, min(0.52, 3.05 / n)
    k = min(1.0, (bw + 0.01) / 1.52)          # narrower boxes (the 7-step archive) get smaller text
    for i, (lab, sub, st, tag) in enumerate(rows):
        fill, edge, fg, ls = style[st]
        x = x0 + i * (bw + gap)
        y = base - bh - i * rise
        ax.add_patch(FancyBboxPatch((x + 0.06, y + 0.06), bw - 0.12, bh - 0.12,
                                    boxstyle="round,pad=0.06,rounding_size=0.06",
                                    facecolor=fill, edgecolor=edge, lw=2.2 if st != "done" else 1,
                                    ls=ls, zorder=2))
        ax.text(x + bw / 2, y + 0.33, lab, ha="center", va="center", fontsize=15 * k,
                fontweight="bold", color=fg, zorder=5)
        ax.text(x + bw / 2, y + 0.90, sub, ha="center", va="center", fontsize=11.5 * k,
                color=fg, zorder=5, linespacing=1.2)
        ax.text(x + bw / 2, y + bh + 0.22, tag, ha="center", va="center", fontsize=11,
                color={"done": GREEN, "progress": "#9A6A00", "later": FAINT}[st], zorder=5)
        if i:
            px = x - gap
            ax.add_patch(FancyArrowPatch((px + 0.01, y + bh / 2 + rise), (x - 0.01, y + bh / 2),
                                         arrowstyle="-|>", mutation_scale=12, color=MUTED,
                                         lw=1.2, shrinkA=0, shrinkB=0, zorder=3))
    # the goal
    gx = x0 + n * (bw + gap)
    gy = base - bh - n * rise
    gw = min(W - 0.45 - gx, 2.9)
    ax.add_patch(FancyBboxPatch((gx + 0.06, gy + 0.06), gw - 0.12, bh - 0.12,
                                boxstyle="round,pad=0.06,rounding_size=0.06",
                                facecolor=ACCENT_BG, edgecolor=ACCENT, lw=2.4, zorder=2))
    ax.text(gx + gw / 2, gy + bh / 2, GOAL.replace("your ", "your\n"), ha="center",
            va="center", fontsize=16, fontweight="bold", color=ACCENT, zorder=5,
            linespacing=1.3)
    ax.text(gx + gw / 2, gy + bh + 0.22, "the goal", ha="center", va="center", fontsize=11,
            color=ACCENT, zorder=5)
    ax.add_patch(FancyArrowPatch((gx - gap + 0.01, gy + bh / 2 + rise), (gx - 0.01, gy + bh / 2),
                                 arrowstyle="-|>", mutation_scale=12, color=MUTED, lw=1.2,
                                 shrinkA=0, shrinkB=0, zorder=3))

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
