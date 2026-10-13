#!/usr/bin/env python3
"""
figstyle_1021.py -- shared style and output helpers for the 1021 deck's figure generators
(make_p02_architecture.py, make_p04_map.py, make_p20_roadmap.py).

Imitates the 930 figure generators: matplotlib 3.11, Liberation Sans (Arial first), the 827 E2
palette, outputs <stem>.pdf / .png (300 dpi) / .svg plus _hires/<stem>.png (500 dpi), and a
companion <stem>.md (data source, generator command, evidence class).  The three persona colours
are defined here once (template section 0, rule 10); build_deck_1021.js carries the same hex values.

[Co-developed with claude code -- Adam]
"""
import datetime as dt
import hashlib
import os
import sys

import matplotlib

assert matplotlib.__version__.startswith("3.11"), matplotlib.__version__
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

DECK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLOTVENV = ("/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3")

# 827 E2 palette (as used by the 930 figures)
INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
WHITE, GREEN, AMBER, GREY = "#FFFFFF", "#2F7D4F", "#E3A21A", "#C9CDD0"
REPO_FILL, REPO_EDGE = "#D3E4EE", ACCENT          # "this repo" = blue fill
SEP_FILL, SEP_EDGE = "#E4E7EA", "#7C858B"         # "separate repo" = grey fill

# persona colours: the same on pages 3, 5-7 and 17-20; a shape is the second encoding
# (circle-corner = control-app developer, square = P4-program developer, diamond tab = operator)
PERSONA = {
    "app": {"name": "control-app developer", "color": GREEN, "text": WHITE, "shape": "round"},
    "p4":  {"name": "P4-program developer", "color": AMBER, "text": INK, "shape": "square"},
    "ops": {"name": "network operator", "color": "#7B5EA7", "text": WHITE, "shape": "diamond"},
}


def die(who, msg):
    raise SystemExit(f"{who}: {msg}")


def sha16(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def new_canvas(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis("off")
    return fig, ax


def title(ax, text, w):
    assert len(text) <= 45, f"canvas title longer than 45 chars: {text!r}"
    ax.text(0.45, 0.48, text, fontsize=22, fontweight="bold", color=INK, va="center")


def save_all(fig, outdir, stem):
    hires = os.path.join(outdir, "_hires")
    os.makedirs(hires, exist_ok=True)
    for ext in ("pdf", "png", "svg"):
        kw = {"dpi": 300} if ext == "png" else {}
        fig.savefig(os.path.join(outdir, f"{stem}.{ext}"), facecolor=WHITE, **kw)
    fig.savefig(os.path.join(hires, f"{stem}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)


def write_companion(outdir, stem, script_path, text):
    """Write <stem>.md from the generator (the file tool may refuse .md; the generator does not)."""
    when = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cmd = (f'cd "{os.path.dirname(os.path.abspath(script_path))}"\n'
           f'"{PLOTVENV}" \\\n    {os.path.basename(script_path)}')
    body = (text.rstrip() + "\n\n## Regenerate\n\n```bash\n" + cmd + "\n```\n\n"
            f"Last produced: {when} (UTC); matplotlib {matplotlib.__version__}; generator "
            f"`{os.path.basename(script_path)}` sha256 `{sha16(script_path)}...`, shared style "
            f"`figstyle_1021.py` sha256 `{sha16(os.path.join(os.path.dirname(script_path), 'figstyle_1021.py'))}...`.\n"
            "\n[Co-developed with claude code -- Adam]\n")
    with open(os.path.join(outdir, stem + ".md"), "w", encoding="utf-8") as f:
        f.write(body)
