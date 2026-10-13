#!/usr/bin/env python3
"""
make_fixed_since_916.py -- fig_f1_fixed_since_916, the board for the 930 deck's
"Found, then fixed -- since 09-16" page.

What: one tile per fix (a merge or an unmerged branch) since the 09-16 report, x = the date it
entered the trunk line (or the branch tip's date), fill = the layer the defect lived in, three
separate bands (and border styles) for the three statuses, which are never mixed:
    MERGED . PUBLIC      (section 2 of the list)
    MERGED . LOCAL ONLY  (section 3)
    IN REVIEW            (section 4)

Data: ../../FIXED-SINCE-916.md, parsed at run time -- sections 1-4 (tables), 6-7 (the merges
that are not fixes), 0 (the snapshot sha) and 9.1 (the public trunk head, taken there from
unauthenticated HTTPS).  An empty status band keeps its label and its count (0) and no rows.
Nothing drawn is typed here: tile labels, dates, layers, statuses and every count come from
the .md.  The .md is then checked against git, read-only, in the kernel
checkout, and the script refuses to draw (SystemExit) on any mismatch:
  * section 1's stated counts == the rows of sections 2-4, per status and per layer; a section-1
    row with a bold count that is neither a status nor a layer stops the script (so a leftover
    count row is not skipped quietly), and so does a section 2-4 heading that names no layer;
  * fixes + features + others == `git log --first-parent --merges --since=2026-09-16 <snapshot>`,
    sha for sha, each exactly once;
  * every MERGED . PUBLIC sha is an ancestor of the public trunk head, every MERGED . LOCAL ONLY
    sha is an ancestor of the snapshot and not of the public head, every IN REVIEW tip exists
    and is not an ancestor of the snapshot;
  * every row's date (sections 2-4, 6, 7) equals the commit's committer date in UTC
    (`TZ=UTC git log --date=format-local:%m-%d`); every date in the .md and on the canvas is UTC.
The canvas carries its as-of stamp: the snapshot sha (section 0) and the time the public heads
were read (section 9.1).
09-28 re-pin (coordinator, ruling D): the neutral "不標層" heading, its hatched tile and its placement
stop are gone -- the item they held is merged and is an ordinary tile in its layer.  The version
with them is kept as slides930/repin-0928-bak/make_fixed_since_916.py.
The layer fills are design constants (derived from the 930 palette's ACCENT #065A82 and second
series #C0701C; CVD separation checked, see the .md).

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/fixed-since-916"
    nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_fixed_since_916.py
writes fig_f1_fixed_since_916.{pdf,png,svg} and _hires/fig_f1_fixed_since_916.png here.
"""
import os
import re
import logging
import subprocess
from collections import Counter, OrderedDict

import matplotlib

assert matplotlib.__version__.startswith("3.11"), matplotlib.__version__
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.font_manager import FontProperties  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from matplotlib.textpath import TextPath  # noqa: E402

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)  # Arial absent: Liberation Sans

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")
STEM = "fig_f1_fixed_since_916"
MD = os.path.normpath(os.path.join(OUTDIR, "..", "..", "FIXED-SINCE-916.md"))
REPO = os.environ.get("NDTWIN_REPO", "/home/adam/Desktop/NDTwin-Kernel")
SINCE = "2026-09-16"          # the cut: FIXED-SINCE-916.md section 0, first bullet

# ---- palette (930 brief) ---------------------------------------------------------------------
INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, WHITE = "#065A82", "#FFFFFF"

# layer fills: design constants.  kernel = ACCENT itself (white text); proxy = a light step of the
# second series #C0701C; ndt = a light step of ACCENT; tests = a neutral; docs = white.
# OKLab distance under protan/deutan/tritan simulation: >= 14.6 among the four fills that have
# tiles; tests vs docs (white) only 6.6-6.8 -- docs has no tile this window (see the .md).
LAYERS = OrderedDict([
    ("kernel", dict(key="kernel C++", label="kernel C++", fill=ACCENT, text=WHITE)),
    ("proxy", dict(key="proxy", label="proxy", fill="#E2A266", text=INK)),
    ("ndt", dict(key="ndt tool", label="ndt tool", fill="#86AFCF", text=INK)),
    ("tests", dict(key="tests-instruments", label="tests / instruments", fill="#E6E9EC", text=INK)),
    ("docs", dict(key="docs", label="docs", fill=WHITE, text=INK)),
])
STATUSES = OrderedDict([
    ("public", dict(emoji="✅", label="MERGED · PUBLIC", ls="solid", lw=1.0)),
    ("local", dict(emoji="🔧", label="MERGED · LOCAL ONLY", ls=(0, (4.0, 2.2)), lw=1.7)),
    ("review", dict(emoji="🕓", label="IN REVIEW", ls=(0, (1.0, 1.8)), lw=1.9)),
])
ROWS = {"public": 5, "local": 1, "review": 2}     # tile rows per sub-column in each band



def die(msg):
    raise SystemExit(f"make_fixed_since_916: {msg}")


# =============================================================================================
# parse the .md
# =============================================================================================
SHA8 = re.compile(r"`([0-9a-f]{8})`")
DATE = re.compile(r"\b(09-\d\d)\b")


def cells(line):
    parts = line.rstrip("\n").split("|")
    if len(parts) < 3 or parts[0].strip() or parts[-1].strip():
        return None
    return [c.strip() for c in parts[1:-1]]


def parse_md(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    tiles, stated, features, others = [], {}, [], []
    snapshot, public_heads, public_times = None, [], []
    h2 = h3 = ""
    for ln in lines:
        if ln.startswith("## "):
            h2, h3 = ln.strip(), ""
            continue
        if ln.startswith("### "):
            h3 = ln.strip()
            continue
        m = re.search(r"\*\*快照\*\*：本機 trunk `([0-9a-f]{8})`", ln)
        if m:
            snapshot = m.group(1)
        c = cells(ln) if ln.startswith("|") else None
        if not c or set(c[0]) <= set("-: ") or c[0] in ("代號", "量", "merge", "#", "repo"):
            continue
        status = next((k for k, v in STATUSES.items() if v["emoji"] in h2), None)
        if h2.startswith("## 1."):
            m = re.fullmatch(r"\*\*(\d+)\*\*", c[1])
            key = next((k for k, v in STATUSES.items() if c[0].startswith(v["emoji"])), None)
            if key is None and c[0].startswith("層："):
                key = next((k for k, v in LAYERS.items() if c[0] == "層：" + v["key"]), None)
            if key is None and re.fullmatch(r"\*\*\d+\*\*", c[1]):
                die(f"section 1 row {c[0]!r} has a bold count but is neither a status nor a layer")
            if key is not None:
                if not m:
                    die(f"section 1 row {c[0]!r}: value {c[1]!r} is not **N**")
                stated[key] = int(m.group(1))
        elif status is not None:
            if len(c) != 4:
                die(f"{h2} / {h3}: row with {len(c)} cells: {ln.strip()[:80]}")
            layer = next((k for k, v in LAYERS.items() if v["key"] in h3), None)
            if layer is None:
                die(f"no layer in heading {h3!r}")
            shas, dates = SHA8.findall(c[2]), DATE.findall(c[2])
            if not shas or not dates:
                die(f"row {c[0]!r}: no sha or date in {c[2]!r}")
            tiles.append(dict(code=c[0], status=status, layer=layer, sha=shas[-1], date=dates[-1],
                              text=c[1]))
        elif h2.startswith("## 6.") or h2.startswith("## 7."):
            m = SHA8.fullmatch(c[0])
            if not m or not DATE.fullmatch(c[1]):
                die(f"{h2}: row {c[0]!r} / {c[1]!r} is not `sha8` | MM-DD")
            (features if h2.startswith("## 6.") else others).append((m.group(1), c[1]))
        elif h2.startswith("## 9.") and h3.startswith("### 9.1"):
            if c[0] in ("ndtwin-lab/NDTwin-Kernel-P4", "Adam010341/NDTwin-Kernel-P4"):
                m = re.fullmatch(r"`([0-9a-f]{40})`", c[3])
                t = re.fullmatch(r"(\d{4}-\d\d-\d\d)T(\d\d:\d\d):\d\dZ", c[1])
                if not m or c[2] != "200":
                    die(f"section 9.1 row {c[0]}: no HTTP 200 + 40-hex trunk head")
                if not t:
                    die(f"section 9.1 row {c[0]}: time {c[1]!r} is not YYYY-MM-DDTHH:MM:SSZ")
                public_heads.append(m.group(1))
                public_times.append(f"{t.group(1)} {t.group(2)}")
    if snapshot is None:
        die("no snapshot sha in section 0")
    if len(public_heads) != 2 or len(set(public_heads)) != 1:
        die(f"section 9: expected the same public trunk head for both repos, got {public_heads}")
    return tiles, stated, features, others, snapshot, public_heads[0], max(public_times)


# =============================================================================================
# check the .md against git (read-only)
# =============================================================================================
GIT_ENV = dict(os.environ, TZ="UTC")      # every git date below is UTC


def git(*args, check=True):
    r = subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True, env=GIT_ENV)
    if check and r.returncode != 0:
        die(f"git {' '.join(args)}: rc {r.returncode}: {r.stderr.strip()[:200]}")
    return r


def is_ancestor(a, b):
    rc = git("merge-base", "--is-ancestor", a, b, check=False).returncode
    if rc not in (0, 1):
        die(f"merge-base --is-ancestor {a} {b}: rc {rc}")
    return rc == 0


def cdate(sha):
    return git("log", "-1", "--format=%cd", "--date=format-local:%m-%d", sha).stdout.strip()


def check(tiles, stated, features, others, snapshot, public_head):
    by_status = Counter(t["status"] for t in tiles)
    by_layer = Counter(t["layer"] for t in tiles)
    for k in STATUSES:
        if stated.get(k) != by_status.get(k, 0):
            die(f"section 1 says {k}={stated.get(k)}, the tables have {by_status.get(k, 0)}")
    for k in LAYERS:
        if stated.get(k) != by_layer.get(k, 0):
            die(f"section 1 says layer {k}={stated.get(k)}, the tables have {by_layer.get(k, 0)}")

    merges = git("log", "--first-parent", "--merges", f"--since={SINCE}", "--format=%h",
                 "--abbrev=8", snapshot).stdout.split()
    fix_merges = [t["sha"] for t in tiles if t["status"] in ("public", "local")]
    for sha, d in features + others:
        if cdate(sha) != d:
            die(f"section 6/7 {sha}: .md date {d} != committer date (UTC) {cdate(sha)}")
    features, others = [f[0] for f in features], [o[0] for o in others]
    listed = fix_merges + features + others
    dup = [s for s, n in Counter(listed).items() if n > 1]
    if dup:
        die(f"merges listed more than once: {dup}")
    if set(listed) != set(merges):
        die(f"merge set differs from git: missing {sorted(set(merges) - set(listed))}, "
            f"extra {sorted(set(listed) - set(merges))}")
    for t in tiles:
        if cdate(t["sha"]) != t["date"]:
            die(f"{t['code']}: .md date {t['date']} != committer date (UTC) {cdate(t['sha'])}")
        if t["status"] == "public" and not is_ancestor(t["sha"], public_head):
            die(f"{t['code']} {t['sha']} is not in the public trunk head {public_head[:8]}")
        if t["status"] == "local" and (not is_ancestor(t["sha"], snapshot)
                                       or is_ancestor(t["sha"], public_head)):
            die(f"{t['code']} {t['sha']} is not local-only")
        if t["status"] == "review":
            git("cat-file", "-e", t["sha"] + "^{commit}")
            if is_ancestor(t["sha"], snapshot):
                die(f"{t['code']} {t['sha']} is already merged into the snapshot {snapshot}")
    print(f"[ok] {len(tiles)} tiles; statuses {dict(by_status)}; layers {dict(by_layer)}")
    print(f"[ok] {len(merges)} merges since {SINCE} at {snapshot} = {len(fix_merges)} fix + "
          f"{len(features)} feature + {len(others)} other; public trunk head {public_head[:8]}")
    return by_status, by_layer


# =============================================================================================
# draw
# =============================================================================================
W = 13.33
M = 0.50
CW = W - 2 * M
PITCH, TILE_H, GAP = 0.40, 0.32, 0.10
LABEL_BAND = 0.36       # height of a band's label row
BAND_GAP = 0.16
FP = FontProperties(family=["sans-serif"])    # resolves through rcParams, like the text


def text_w(s, size):
    return TextPath((0, 0), s, size=size, prop=FP).get_extents().width / 72.0


def fit(s, avail, start=13.0, floor=10.5):
    size = start
    while size > floor and text_w(s, size) > avail:
        size -= 0.25
    if text_w(s, size) > avail:
        die(f"tile label {s!r} does not fit {avail:.2f} in at {floor} pt")
    return size


def split(n, k):
    base, rem = divmod(n, k)
    return [base + (1 if i < rem else 0) for i in range(k)]


def layout(tiles):
    dates = sorted({t["date"] for t in tiles})
    cols = {}
    for d in dates:
        k = 1
        for s in STATUSES:
            n = sum(1 for t in tiles if t["date"] == d and t["status"] == s)
            k = max(k, -(-n // ROWS[s]))
        cols[d] = k
    # rows a band actually uses (<= ROWS[s]); 0 for an empty band
    used = {s: max([0] + [max(split(sum(1 for t in tiles if t["date"] == d and t["status"] == s),
                                     cols[d])) for d in dates]) for s in STATUSES}
    sub_w = CW / sum(cols.values())
    x0, x = {}, M
    for d in dates:
        x0[d] = x
        x += cols[d] * sub_w
    return dates, cols, sub_w, x0, used


def draw(tiles, by_status, by_layer, snapshot, checked):
    dates, cols, sub_w, x0, used = layout(tiles)
    y_title, y_dates, y_rule = 0.55, 1.12, 1.30
    y = y_rule + 0.08
    bands = {}
    for s in STATUSES:
        bands[s] = (y, y + LABEL_BAND)          # label row top, first tile row top
        y += LABEL_BAND + used[s] * PITCH + BAND_GAP    # an empty band keeps only its label
    y_grid_bot = y - BAND_GAP + 0.04
    y_legend = y_grid_bot + 0.30
    H = y_legend + 0.42

    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")

    ax.text(M, y_title, "Found, then fixed — since 09-16", fontsize=22, fontweight="bold",
            color=INK, ha="left", va="center")
    # as of: the snapshot the list stops at, and the time its public heads were read
    ax.text(M + CW, y_title, f"as of trunk {snapshot} · public check {checked} UTC", fontsize=11,
            color=FAINT, ha="right", va="center")

    # date header + column rules
    for d in dates:
        w = cols[d] * sub_w
        ax.text(x0[d] + w / 2, y_dates, d, fontsize=13, fontweight="bold", color=MUTED,
                ha="center", va="center")
    ax.text(M + CW, y_dates, "UTC", fontsize=11, color=FAINT, ha="right", va="center")
    ax.plot([M, M + CW], [y_rule, y_rule], color=RULE, lw=0.9, zorder=1)
    for d in dates[1:]:
        ax.plot([x0[d], x0[d]], [y_rule, y_grid_bot], color=RULE, lw=0.6, zorder=1)

    for s, st in STATUSES.items():
        y_lab, y_top = bands[s]
        # band label: a tile glyph in this band's border style, the name, the count
        gx, gy = M + 0.02, y_lab + 0.07
        ax.add_patch(Rectangle((gx, gy), 0.34, 0.20, facecolor=WHITE, edgecolor=INK,
                               linewidth=st["lw"], linestyle=st["ls"], zorder=3))
        ax.text(gx + 0.46, gy + 0.10, st["label"], fontsize=12, fontweight="bold", color=MUTED,
                ha="left", va="center", zorder=5,
                bbox=dict(facecolor=WHITE, edgecolor="none", pad=1.5))
        lw_ = text_w(st["label"], 12) * 1.04
        ax.text(gx + 0.46 + lw_ + 0.16, gy + 0.10, str(by_status.get(s, 0)), fontsize=15,
                fontweight="bold", color=INK, ha="left", va="center", zorder=5,
                bbox=dict(facecolor=WHITE, edgecolor="none", pad=1.5))
        if s != "public":
            ax.plot([M, M + CW], [y_lab - BAND_GAP / 2, y_lab - BAND_GAP / 2], color=RULE,
                    lw=0.9, zorder=1)
        for d in dates:
            items = [t for t in tiles if t["date"] == d and t["status"] == s]
            if not items:
                continue
            i = 0
            for sc, n in enumerate(split(len(items), cols[d])):
                bx = x0[d] + sc * sub_w + GAP / 2
                for r in range(n):
                    t = items[i]
                    i += 1
                    lay = LAYERS[t["layer"]]
                    by = y_top + r * PITCH
                    ax.add_patch(Rectangle((bx, by), sub_w - GAP, TILE_H,
                                           facecolor=lay["fill"], edgecolor=INK,
                                           linewidth=st["lw"], linestyle=st["ls"], zorder=3))
                    ax.text(bx + (sub_w - GAP) / 2, by + TILE_H / 2 + 0.005, t["code"],
                            fontsize=fit(t["code"], sub_w - GAP - 0.12), color=lay["text"],
                            ha="center", va="center", zorder=5)

    # legend: layers with their counts (all statuses together)
    lx = M
    for k, lay in LAYERS.items():
        ax.add_patch(Rectangle((lx, y_legend - 0.10), 0.34, 0.20, facecolor=lay["fill"],
                               edgecolor=INK, linewidth=0.9, zorder=3))
        lab = f"{lay['label']}  {by_layer.get(k, 0)}"
        ax.text(lx + 0.44, y_legend, lab, fontsize=12, color=BODY, ha="left", va="center")
        lx += 0.44 + text_w(lab, 12) + 0.45
    if lx - 0.45 > M + CW:
        die("legend runs off the canvas")
    return fig


def save(fig, name):
    os.makedirs(HIRES, exist_ok=True)
    for ext in ("pdf", "png", "svg"):
        kw = {"dpi": 300} if ext == "png" else {}
        fig.savefig(os.path.join(OUTDIR, f"{name}.{ext}"), facecolor=WHITE, **kw)
    fig.savefig(os.path.join(HIRES, f"{name}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"[out] {name}.{{pdf,png,svg}} + _hires/{name}.png")


if __name__ == "__main__":
    tiles, stated, features, others, snapshot, public_head, checked = parse_md(MD)
    by_status, by_layer = check(tiles, stated, features, others, snapshot, public_head)
    save(draw(tiles, by_status, by_layer, snapshot, checked), STEM)
