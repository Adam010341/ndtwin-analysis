#!/usr/bin/env python3
"""
Re-render the deck's figures with less prose on them.

The figures were written for a report, so each carries a headline plus two to
four lines of explanatory subtitle. On a slide that text gets read aloud, so it
is dead weight — and it costs the plot its vertical space.

This does not paint over the PNGs. It copies each plotting script, drops the
figure-level paragraphs, shortens the headline, gives the freed height back to
the axes, and runs the copy. Every number is still computed from the committed
raw data on each run, so a slimmed figure cannot drift from the report it came
out of.

    python3 slim_figures.py <repo> <out-dir>
"""
import os
import re
import subprocess
import sys
import tempfile

REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Desktop/NDTwin-Kernel")
OUT = sys.argv[2] if len(sys.argv) > 2 else "."

# Headlines, shortened. Given as exact source fragments rather than as the
# rendered sentence, because the scripts wrap long strings across source lines
# and one headline is built from an f-string.
Q = '"'
HEADLINE_EDITS = [
    (Q + "Sampling harder buys precision on a √ law — and the data plane does not pay " + Q,
     Q + "Sampling harder buys precision on a √ law" + Q),
    ('                 "for it", fontsize=13',
     '                 "", fontsize=13'),

    (Q + "Deleting sampling entirely costs the data plane nothing — the bill was never " + Q,
     Q + "The sampling bill lands on the kernel and the proxy" + Q),
    ('                 "there", fontsize=13',
     '                 "", fontsize=13'),

    ('"The northbound API serves one request at a time \\u2014 measured, and it has "',
     '"The northbound API serves one request at a time"'),
    ('                 "room today"',
     '                 ""'),

    (Q + "Almost all of the kernel's sFlow cost is already paid at the lowest rate " + Q,
     Q + "206 µs of CPU per sample, inside the range measured" + Q),
    ('                 "measured", fontsize=13',
     '                 "", fontsize=13'),

    ('f"An OVS link failure at 128 hosts lasts {total:.1f} s, and "\n'
     '             f"{detect / total * 100:.0f}% of it is waiting to notice"',
     'f"{detect / total * 100:.0f}% of a 128-host OVS outage is waiting to notice"'),
]

# Figure-level text blocks. The headline is the only one set in bold, in all
# three scripts, so weight is what separates it from the paragraphs — no
# coordinate has to be guessed and nothing depends on the wording.
FIGTEXT = re.compile(r"^[ \t]*fig\.text\((?:.*\n)*?.*?\)\s*$", re.MULTILINE)

# Axes-level blocks that are prose rather than numbers. Listed one by one,
# because the rest of them carry values that appear nowhere else on the plot.
PROSE = [
    '"Deleting the clone session removes every downstream cost and\\n"',
    '"leaves the forwarding path byte-identical. bmv2 is nominally\\n"',
    '"HIGHER with sampling off \\u2014 that difference is noise, not a saving."',
]


def slim(src_text):
    out = src_text

    for old, new in HEADLINE_EDITS:
        out = out.replace(old, new, 1)

    for m in list(FIGTEXT.finditer(out)):
        block = m.group(0)
        if 'weight="bold"' in block:
            continue
        out = out.replace(block, "", 1)

    for line in PROSE:
        out = out.replace(line, '""')

    # give the freed height back to the axes
    out = re.sub(r"rect=\[0, ([0-9.]+), 1, 0\.8[0-9]+\]", r"rect=[0, \1, 1, 0.915]", out)
    out = re.sub(r"subplots_adjust\(top=0\.6[0-9]+,", "subplots_adjust(top=0.74,", out)
    out = re.sub(r"top=0\.8[0-9]+, bottom=", "top=0.90, bottom=", out)
    # Panel padding is deliberately left alone. The block under each panel
    # title is numbers, not prose, so it stays — and the title needs the pad to
    # clear it. Shrinking the pad with the block still there was tried once and
    # put the title straight through the text.
    return out


def run(script_dir, script, out_dir):
    src = os.path.join(REPO, "doc/audit", script_dir, script)
    slimmed = slim(open(src, encoding="utf-8").read())

    # The scripts find their raw data with os.path.dirname(__file__), so the
    # copy has to be told where the original lived. Pinning HERE lets the copy
    # run out of a scratch directory instead of littering the audit folder.
    here = os.path.dirname(src)
    slimmed = re.sub(r"^HERE = os\.path\.dirname\(os\.path\.abspath\(__file__\)\)$",
                     "HERE = %r" % here, slimmed, count=1, flags=re.MULTILINE)

    with tempfile.TemporaryDirectory() as td:
        tmp = os.path.join(td, "slim_" + script)
        open(tmp, "w", encoding="utf-8").write(slimmed)
        r = subprocess.run([sys.executable, tmp, out_dir],
                           capture_output=True, text=True, cwd=here)
        print("ok" if r.returncode == 0 else "FAILED", script)
        if r.returncode:
            print(r.stdout[-1500:], r.stderr[-1500:])


if __name__ == "__main__":
    run("2026-08-20_sampling-rate-and-cpu", "plot_figures.py", OUT)
    run("2026-08-21_ryu-topology-scaling", "plot_budget.py", OUT)
    run("2026-08-21_ovs-failover-after-fix", "plot_after_fix.py", OUT)
