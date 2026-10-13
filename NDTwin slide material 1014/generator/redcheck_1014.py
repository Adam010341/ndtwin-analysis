#!/usr/bin/env python3
"""Red-check of the 1014 generators (template section 0 rule 11, 930 rule 10): break one input at a time in a
temporary copy, run the generator on the copy, and require (a) a non-zero exit and (b) the generator's OWN named
reason in its output.  Controls (unbroken inputs) must exit 0.  Writes nothing under the deck folder: figure
generators are run with --out to a temp dir, the deck build with OUT_1014 and TEMPLATE_1014 pointing to temp.

Usage: redcheck_1014.py [--log DIR]      (run with the plot venv's python or any python3; it shells out)
REDCHECK_P13_SCRIPT / REDCHECK_P10_SCRIPT (and REDCHECK_P22_SCRIPT, REDCHECK_P18_SCRIPT) point a case set at another copy of the
generator, e.g. a mutant with its checks removed, to see the cases themselves go red.
[Co-developed with claude code -- Adam]"""
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.dirname(HERE)
VENV = os.environ.get("NDTWIN_PLOTVENV") or os.path.normpath(
    os.path.join(DECK, "..", "NDTwin Slide material 820", ".plotvenv", "bin", "python3"))
KERNEL = os.environ.get("NDTWIN_KERNEL") or os.path.normpath(os.path.join(DECK, "..", "..", "NDTwin-Kernel"))
TMP = tempfile.mkdtemp(prefix="redcheck1014_")
OUT, BAD = [], [0]


def say(s):
    OUT.append(s)
    print(s)


def sub(text, old, new, count=1):
    assert old in text, f"redcheck harness: pattern not in input: {old!r}"
    return text.replace(old, new, count)


def run_py(script, extra):
    return subprocess.run([VENV, os.path.join(HERE, script)] + extra, capture_output=True, text=True)


def case(name, rc_out, expect):
    p = rc_out
    text = (p.stdout + p.stderr)
    if expect is None:
        ok = p.returncode == 0
        say(f"{'ok    ' if ok else 'FAIL  '}control {name}: rc={p.returncode}")
    else:
        ok = p.returncode != 0 and expect in text
        hit = [ln for ln in text.strip().splitlines() if expect in ln]
        last = hit[:1] or [ln for ln in text.strip().splitlines() if ln.strip()][-1:] or [""]
        say(f"{'ok    ' if ok else 'FAIL  '}{name}: rc={p.returncode}; wanted reason {expect!r}; got: {last[0].strip()[:170]}")
    if not ok:
        BAD[0] += 1


def tsv_mut(src, fn, name):
    d = os.path.join(TMP, name)
    os.makedirs(d, exist_ok=True)
    dst = os.path.join(d, os.path.basename(src))
    open(dst, "w", encoding="utf-8").write(fn(open(src, encoding="utf-8").read()))
    return dst, d


# ------------------------------------------------------------------ P04 (landscape)
L = os.path.join(DECK, "figures_spec", "landscape.tsv")


def p04(name, fn, expect):
    spec, d = tsv_mut(L, fn, name)
    case("P04 " + name, run_py("make_p04_map.py", ["--spec", spec, "--out", os.path.join(d, "o")]), expect)


p04("unbroken", lambda t: t, None)
p04("drop_a_row", lambda t: "\n".join(l for l in t.splitlines() if not l.startswith("Batfish\t")) + "\n", "has 15 data rows")
p04("renamed_column", lambda t: sub(t, "short_label", "label"), "columns are")
p04("bad_y", lambda t: sub(t, "\tnone\t", "\tdesign time\t"), "is not one of")
p04("bad_x", lambda t: sub(t, "\tconfig model\t", "\tconfig-model\t"), "x_category")
p04("tool_not_in_matrix", lambda t: sub(t, "Containerlab\t", "Containerlab2\t"), "not a matrix_final.json maturity column")
p04("tool_twice", lambda t: sub(t, "Batfish\t", "GNS3\t"), "listed twice")
p04("star_removed", lambda t: sub(t, "Forward*", "Forward"), "lacks the * mark")
p04("dagger_added", lambda t: sub(t, "\tBatfish\t", "\tBatfish†\t"), "has the dagger mark")
p04("label_too_long", lambda t: sub(t, "\tP4 tutorials VM\t", "\tP4 tutorials VM on a laptop\t"), "longer than 18")
p04("cell_count_differs_from_template", lambda t: sub(t, "Containerlab\tpacket-level emulation\tnone", "Containerlab\tpacket-level emulation\timports snapshots"),
    "the template says the emulation x none cell holds 10, the tsv has 9")
p04("one_point_rule_missing", lambda t: sub(t, "One point per tool", "Targets per tool"), "one-point-per-tool rule")
p04("no_rule_header", lambda t: "\n".join(l for l in t.splitlines() if not l.startswith("#")) + "\n", "no `#` placement-rule header")
p04("unsure_count_differs", lambda t: sub(t, "\tno\n", "\tyes: test\n"), "rows are unsure")
p04("ndtwin_moved_out_of_cell", lambda t: sub(t, "NDTwin\tpacket-level emulation\tnone", "NDTwin\tpacket-level emulation\tstays synced live"), "NDTwin is not in the packet-level emulation x none cell")

# ------------------------------------------------------------------ P22 (roadmap)
P = os.path.join(DECK, "figures_spec", "problems.tsv")
R = os.path.join(DECK, "figures_spec", "roadmap.txt")


def p20(name, fn_tsv, fn_roadmap, expect, extra=()):
    d = os.path.join(TMP, "p20_" + name)
    os.makedirs(d, exist_ok=True)
    spec = os.path.join(d, "problems.tsv")
    road = os.path.join(d, "roadmap.txt")
    open(spec, "w", encoding="utf-8").write(fn_tsv(open(P, encoding="utf-8").read()))
    open(road, "w", encoding="utf-8").write(fn_roadmap(open(R, encoding="utf-8").read()))
    case("P22 " + name, run_py(os.environ.get("REDCHECK_P22_SCRIPT", "make_p22_roadmap.py"),
                               ["--spec", spec, "--roadmap", road, "--out", os.path.join(d, "o")] + list(extra)), expect)


def tsv_line(t, rank, fn):
    return "\n".join(fn(l) if l.startswith(f"{rank}\t") else l for l in t.splitlines()) + "\n"


ID = lambda t: t
p20("unbroken", ID, ID, None)
p20("rank_duplicated_in_tsv", lambda t: sub(t, "\n18\t", "\n17\t"), ID, "duplicated")
p20("rank_missing_in_tsv", lambda t: sub(t, "\n19\t", "\n20\t"), ID, "missing: [19]")
p20("rank_count_not_stated", ID, lambda t: sub(t, "any rank 1-19 is missing", "any rank is missing"), "states no rank count")
p20("rank_count_differs", ID, lambda t: sub(t, "any rank 1-19 is missing", "any rank 1-18 is missing"), "roadmap.txt states 18")
p20("rank_not_drawn", ID, lambda t: "\n".join(l for l in t.splitlines() if "#11  Ryu" not in l and not l.strip().startswith("NEXT  #11 ")) + "\n",
    "rank 11 is in problems.tsv but not drawn")
p20("rank_drawn_twice", ID, lambda t: sub(t, "    NOW   #17 configurable LLM endpoint", "    NOW   #2  configurable LLM endpoint"), "draws rank 2 twice")
p20("fixable_no_in_fix_lane", lambda t: tsv_line(t, 13, lambda l: l.rsplit("\t", 1)[0] + "\tno (test)"), ID,
    "rank 13 is fixable=no but is drawn in a fix lane")
p20("fixable_yes_in_disclose", lambda t: tsv_line(t, 18, lambda l: l.rsplit("\t", 1)[0] + "\tyes"), ID,
    "rank 18 is fixable=yes but is drawn in DISCLOSE")
p20("no_persona", lambda t: tsv_line(t, 3, lambda l: "\t".join(c if i != 2 else "somebody" for i, c in enumerate(l.split("\t")))), ID,
    "names no persona")
p20("column_rule_violated", lambda t: tsv_line(t, 15, lambda l: sub(l, "1-2 days", "about 1 week")), ID,
    "rank 15 is drawn in NOW but the column rule")
p20("new_rank12_cost_a_week", lambda t: tsv_line(t, 12, lambda l: sub(l, "2-3 days OVS + 2-3 days P4 emitter", "about 1 week")), ID,
    "rank 12 is drawn in NOW but the column rule")
p20("arrow_to_undrawn", ID, lambda t: sub(t, "#2 -> #13", "#2 -> #99"), "names a rank that is not drawn")
p20("arrows_too_close", ID, ID, "cannot keep 1000 pt from the other arrows", extra=["--min-gap-pt", "1000"])
p20("collinear_rule_unsatisfiable", ID, ID, "within 100000 pt end to end", extra=["--min-gap-pt", "20", "--min-collinear-gap-pt", "100000"])
p20("box_outside_column", ID, ID, "sticks out of its NEXT column", extra=["NEXT=2.0"])
p20("arrow_legend_missing", ID, lambda t: sub(t, "ARROW LEGEND (on canvas): needed by", "ARROW KEY: needed by"), "ARROW LEGEND")
p20("title_differs", ID, lambda t: sub(t, "Title on canvas (= slide title): What we fix first, and what we disclose", "Title on canvas (= slide title): What we fix first"),
    "canvas title is")



def p20_no_arrows_read_as_one_line():
    """Run the unbroken P22 generator, read the routes it chose (--routes-json, written into the temp dir, never into
    figures/) and require: no two different arrows have segments on one line (across < 10 pt, both vertical or both
    horizontal) that are less than 72 pt apart end to end -- so two arrows never read as one long line."""
    import json
    d = os.path.join(TMP, "p20_collinear_routes")
    os.makedirs(d, exist_ok=True)
    rj = os.path.join(d, "routes.json")
    script = os.environ.get("REDCHECK_P22_SCRIPT", "make_p22_roadmap.py")     # lets the red run point at an old copy
    p = run_py(script, ["--out", os.path.join(d, "o"), "--routes-json", rj])
    if p.returncode != 0 or not os.path.exists(rj):
        say(f"FAIL  P22 no_arrows_read_as_one_line: rc={p.returncode}; no routes json written to {rj}")
        BAD[0] += 1
        return
    routes = {k: [tuple(pt) for pt in v] for k, v in json.load(open(rj))["routes"].items()}
    bad, nearest = [], None
    keys = list(routes)
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            for p0, q0 in zip(routes[keys[i]][:-1], routes[keys[i]][1:]):
                for r0, s0 in zip(routes[keys[j]][:-1], routes[keys[j]][1:]):
                    for k in (0, 1):
                        o = 1 - k
                        if abs(p0[k] - q0[k]) < 1e-9 and abs(r0[k] - s0[k]) < 1e-9 and abs(p0[k] - r0[k]) * 72 < 10:
                            a0, a1 = sorted((p0[o], q0[o]))
                            b0, b1 = sorted((r0[o], s0[o]))
                            g = (max(a0, b0) - min(a1, b1)) * 72
                            nearest = g if nearest is None else min(nearest, g)
                            if g < 72:
                                bad.append(f"#{keys[i]} and #{keys[j]} {'vertical' if k == 0 else 'horizontal'} "
                                           f"on one line, {g:.1f} pt end to end")
    ok = not bad
    say(f"{'ok    ' if ok else 'FAIL  '}P22 no_arrows_read_as_one_line: wanted every same-line pair >= 72 pt end to end; "
        + ("got " + ("no same-line pair" if nearest is None else f"closest {nearest:.1f} pt")
           if ok else "got " + "; ".join(bad)))
    if not ok:
        BAD[0] += 1


p20_no_arrows_read_as_one_line()

# ------------------------------------------------------------------ P18 (P4 health check)
H18 = os.path.join(DECK, "figures_spec", "p4_health.tsv")
P18S = os.environ.get("REDCHECK_P18_SCRIPT", "make_p18_health.py")
CELLS_SRC = subprocess.run(["git", "-C", KERNEL, "show", "3a47bdb7:tools/p4_health/cells/table.py"],
                           capture_output=True, text=True).stdout


def p18(name, fn, expect, fn_cells=None):
    spec, d = tsv_mut(H18, fn, "p18_" + name)
    extra = []
    if fn_cells is not None:
        cf = os.path.join(d, "table.py")
        open(cf, "w", encoding="utf-8").write(fn_cells(CELLS_SRC))
        extra = ["--cells-file", cf]
    case("P18 " + name, run_py(P18S, ["--spec", spec, "--out", os.path.join(d, "o")] + extra), expect)


p18("unbroken", ID, None)
p18("unbroken_from_cells_file", ID, None, fn_cells=ID)
p18("cell_dropped_from_spec", lambda t: sub(t, "T1,T2,T3,T4,T5,T6,T7,T8,PF-T", "T1,T2,T3,T4,T5,T6,T7,T8"), "differ from CELLS in the code")
p18("code_gained_a_cell", ID, "differ from CELLS in the code",
    fn_cells=lambda s: sub(s, 'Cell("T1", "tables"', 'Cell("T0", "tables", "core", "active", "A", 2, t1),\n    Cell("T1", "tables"'))
p18("title_not_offline", lambda t: sub(t, "# title: P4 health check: 57 cells, offline only", "# title: P4 health check: 57 cells"), "does not say offline")
p18("title_count_wrong", lambda t: sub(t, "57 cells, offline only", "58 cells, offline only"), "title says 58 cells")
p18("live_lab_words_missing", lambda t: sub(t, "Offline results; not yet run against a live lab", "Offline results"), "not yet run against a live lab")
p18("prediction_row", lambda t: t + "off\tT8 journaled (expected)\tRED\tstock\n", "names a prediction")
p18("unknown_row_kind", lambda t: t + "pred\tK2\tRED\tstock\n", "is not `dim` or `off`")
p18("writer_result_not_a_count", lambda t: sub(t, "52 cases\t0 disagree", "52 cases\tall fine"), "is not '<n> disagree'")
p18("offline_row_not_a_cell", lambda t: sub(t, "off\tT7 priority order", "off\tX7 priority order"), "neither S0, the writer comparison nor a cell")
p18("offline_result_not_a_run_result", lambda t: sub(t, "T6 optional entry\tGREEN", "T6 optional entry\tlikely green"), "is not a run result")
p18("offline_target_is_the_lab", lambda t: sub(t, "T5 range entry\tGREEN\tstock · fast", "T5 range entry\tGREEN\tlive lab"), "is not throwaway stock / fast bmv2")
p18("footer_on_canvas", lambda t: sub(t, "# right: Offline results; not yet run against a live lab", "# right: Offline results; not yet run against a live lab (commit e17d39e5)"),
    "provenance text on the canvas")


def footer_guard():
    """Every figure generator saves through figstyle.save_all: a figure with a provenance footer must be refused."""
    code = ("import sys; sys.path.insert(0, %r); import figstyle_1014 as S\n"
            "fig, ax = S.new_canvas(4, 3); S.title(ax, 'x', 4)\n"
            "ax.text(0.2, 2.8, %r, fontsize=7, color=S.FAINT)\n"
            "S.save_all(fig, %r, 'footer')\n")
    for i, footer in enumerate(["source: results.tsv", "trunk 3a47bdb7", "2026-10-08", "make_p13_relief.py",
                                "intelligent_router.py:617"]):
        p = subprocess.run([VENV, "-c", code % (HERE, footer, os.path.join(TMP, "footer%d" % i))],
                           capture_output=True, text=True)
        case("figstyle footer_refused_%d %r" % (i, footer), p, "provenance text on the canvas")


footer_guard()

# ------------------------------------------------------------------ P02 (architecture)
A = os.path.join(DECK, "figures_spec", "architecture.txt")


def p02(name, fn, expect):
    spec, d = tsv_mut(A, fn, name)
    case("P02 " + name, run_py("make_p02_architecture.py", ["--spec", spec, "--out", os.path.join(d, "o")]), expect)


p02("unbroken", lambda t: t, None)
p02("element_B3_missing", lambda t: sub(t, "  B3 Flow routing manager", "  Bx Flow routing manager"), "no entry for element B3")
p02("title_differs", lambda t: sub(t, "What NDTwin is, as built today\n", "What NDTwin is: one API over three data planes\n"), "canvas title is")
p02("repo_tint_asked_again", lambda t: sub(t, "No tint by where the code lives", "tint every box by the repo"), "asks for a repo tint")
p02("generator_arrow_not_to_D1", lambda t: sub(t, "double-headed arrow to D1", "double-headed arrow to D3"), "double-headed arrow to D1")
p02("proxy_sflow_not_from_proxy", lambda t: sub(t, "drawn FROM the P4 proxy box", "drawn from the bmv2 plane"), "drawn FROM the P4 proxy box")
p02("element_E7_missing", lambda t: sub(t, "  E7 ndt / ndtwin-lab", "  Ex ndt / ndtwin-lab"), "no entry for element E7")

# ------------------------------------------------------------------ P13 (time to relief, hands-on)
HO = os.path.join(KERNEL, "doc/audit/2026-10-08_why-ndtwin-handson")
CT = os.path.join(HO, "controls.tsv")
RT = os.path.join(HO, "congestion", "results.tsv")
P13 = os.environ.get("REDCHECK_P13_SCRIPT", "make_p13_relief.py")     # lets a red run point at a mutant copy
P10 = os.environ.get("REDCHECK_P10_SCRIPT", "make_p10_setup.py")


def drop_line(t, start):
    lines = t.splitlines()
    hit = [i for i, l in enumerate(lines) if l.startswith(start)]
    assert hit, f"redcheck harness: no line starts with {start!r}"
    del lines[hit[0]]
    return "\n".join(lines) + "\n"


def p13(name, fn_ctl, fn_res, expect):
    d = os.path.join(TMP, "p13_" + name)
    os.makedirs(d, exist_ok=True)
    c, r = os.path.join(d, "controls.tsv"), os.path.join(d, "results.tsv")
    open(c, "w", encoding="utf-8").write(fn_ctl(open(CT, encoding="utf-8").read()))
    open(r, "w", encoding="utf-8").write(fn_res(open(RT, encoding="utf-8").read()))
    case("P13 " + name, run_py(P13, ["--controls", c, "--results", r, "--out", os.path.join(d, "o")]), expect)


p13("unbroken", ID, ID, None)
p13("app_strip_short", ID, lambda t: drop_line(t, "ndtwin-app\tbmv2\tapp-5\t"),
    "strip 'NDTwin app, bmv2' has 4 trials, the plan is 5")
p13("diy_app_strip_short", ID, lambda t: drop_line(t, "diy-app\tovs\tapp-2\t"),
    "strip 'DIY app, OVS' has 4 trials, the plan is 5")
p13("control_strip_short", lambda t: drop_line(t, "ndtwin\tbmv2\t3\t"), ID,
    "strip 'NDTwin, bmv2' has 4 trials, the plan is 5")
p13("invalid_app_row", ID, lambda t: sub(t, "ndtwin-app\tovs\tapp-3\tv3\tndtwin_app@767a4b32\tPASS",
                                         "ndtwin-app\tovs\tapp-3\tv3\tndtwin_app@767a4b32\tINVALID_RECEIVER"),
    "is INVALID_RECEIVER (an INVALID_* row is not a result")
p13("invalid_control_row", lambda t: sub(t, "verdict=RECOVERED; cut=s1-s6; add_ms=35.2",
                                         "verdict=INVALID_NO_OUTAGE; cut=s1-s6; add_ms=35.2"), ID,
    "is INVALID_NO_OUTAGE (an INVALID_* row is not a result)")
p13("pass_without_time", ID, lambda t: sub(t, "diy_app@98691518\tPASS\t1\t6\t", "diy_app@98691518\tPASS\t1\tNA\t"),
    "is PASS without a numeric time_to_relief_s")
p13("scripted_control_mismatch", ID, lambda t: sub(t, "good-1\tv1\tcontrol:good\tPASS", "good-1\tv1\tcontrol:good\tRED_LATE"),
    "pre-registered PASS")
p13("diy_static_recovered", lambda t: sub(t, "verdict=NOT_RECOVERED; cut=s1-s5; add_ms=16.5", "verdict=RECOVERED; cut=s1-s5; add_ms=16.5"),
    ID, "designed red control diy-static/ovs/1 is RECOVERED, must be NOT_RECOVERED")
p13("diy_static_short", lambda t: drop_line(t, "diy-static\tovs\t2\t"), ID,
    "designed red control diy-static has 2 trials, the plan is 3")
p13("negative_control_recovered", lambda t: sub(t, "verdict=NOT_RECOVERED; cut=s1-s5,s1-s6; add_ms=103.5",
                                                "verdict=RECOVERED; cut=s1-s5,s1-s6; add_ms=103.5"), ID,
    "must be NOT_RECOVERED")


# ------------------------------------------------------------------ P10 (setup)
TP = os.path.join(HO, "topology.tsv")
DL = os.path.join(HO, "congestion", "raw", "agent_ndtwin_dev", "evidence", "ctl7.log")


DY = os.path.join(HO, "congestion", "raw", "agent_diy_dev", "ryu.log")


def p10(name, fn_topo, fn_log, expect, fn_diy=lambda t: t):
    d = os.path.join(TMP, "p10_" + name)
    os.makedirs(d, exist_ok=True)
    t, lg, dy = os.path.join(d, "topology.tsv"), os.path.join(d, "ctl7.log"), os.path.join(d, "ryu.log")
    open(t, "w", encoding="utf-8").write(fn_topo(open(TP, encoding="utf-8").read()))
    open(lg, "w", encoding="utf-8").write(fn_log(open(DL, encoding="utf-8").read()))
    open(dy, "w", encoding="utf-8").write(fn_diy(open(DY, encoding="utf-8").read()))
    case("P10 " + name, run_py(P10, ["--topology", t, "--devlog", lg, "--diylog", dy, "--out", os.path.join(d, "o")]),
         expect)


p10("unbroken", ID, ID, None)
p10("link_dropped", lambda t: drop_line(t, "sw\ts8\t4\ts10\t4"), ID, "15 switch-switch links")
p10("host_moved", lambda t: sub(t, "host\th3\t1\ts3\t3", "host\th3\t1\ts3\t4"), ID, "the page draws hN on sN port 3")
p10("path_hop_not_a_link", ID, lambda t: sub(t, "s1:1>s5:3>s9:4>s8:1>s3:3  ->", "s1:1>s5:3>s9:3>s8:1>s3:3  ->"),
    "is not a topology link on that port")
p10("no_move_for_pair", ID, lambda t: t.replace("10.0.0.1:", "10.0.0.9:"), "no move line for h1 -> h3")
p10("before_equals_after", ID, lambda t: sub(t, "->  s1:2>s6:3>s9:3>s7:1>s3:3", "->  s1:1>s5:3>s9:4>s8:1>s3:3"),
    "before and after are the same path")
p10("diy_path_missing", ID, ID, "no base path for h1 -> h3 in the DIY log", fn_diy=lambda t: sub(t, "h1>h3:", "h1>hX:"))

# ------------------------------------------------------------------ deck build (template)
T = os.path.join(DECK, "NDTwin-slide-template-1014.md")
def node_path():
    """NODE_PATH from the caller, or the first cowork outputs/node_modules holding pptxgenjs (glob, not pinned)."""
    import glob
    if os.environ.get("NODE_PATH"):
        return os.environ["NODE_PATH"]
    hits = sorted(glob.glob(os.path.expanduser("~/.config/Claude/local-agent-mode-sessions/*/*/*/outputs/node_modules/pptxgenjs")))
    return os.path.dirname(hits[0]) if hits else ""


ENV = dict(os.environ, NODE_PATH=node_path())


def build(name, fn, expect):
    d = os.path.join(TMP, "b_" + name)
    os.makedirs(d, exist_ok=True)
    tpl = os.path.join(d, "t.md")
    open(tpl, "w", encoding="utf-8").write(fn(open(T, encoding="utf-8").read()))
    env = dict(ENV, TEMPLATE_1014=tpl, OUT_1014=os.path.join(d, "out.pptx"))
    p = subprocess.run(["conda", "run", "-n", "webgui-node", "node", os.path.join(HERE, "build_deck_1014.js")],
                       capture_output=True, text=True, env=env, cwd=DECK)
    case("build " + name, p, expect)


build("unbroken", lambda t: t, None)
build("page_row_dropped", lambda t: "\n".join(l for l in t.splitlines() if not l.startswith("| 22 | P22 |")) + "\n", "lists 21 pages")
build("chars_wrong", lambda t: sub(t, "| 9 | P09 | Commercial and academic: public material only | 45 |", "| 9 | P09 | Commercial and academic: public material only | 44 |"), "chars column says 44")
build("title_over_45", lambda t: sub(t, "| 2 | P02 | What NDTwin is, as built today | 30 |", "| 2 | P02 | What NDTwin is, as built today, in one picture of everything | 30 |"), "longer than 45 chars")
build("figure_without_stem", lambda t: re.sub(r"(\| 8 \| P08 \|[^\n]*?\| )table( \|)", r"\1figure\2", t, count=1), "figure page without a figure stem")
build("form_counts", lambda t: sub(t, "| 3 | P03 | Three developers, three jobs | 28 | table |", "| 3 | P03 | Three developers, three jobs | 28 | title |"), "form counts")
build("figure_file_missing", lambda t: sub(t, "`landscape/fig_p04_map`", "`landscape/fig_p04_mapp`"), "missing figure file")
build("notes_block_missing", lambda t: sub(t, "### P07 ", "## P07 "), "no block for P07")
build("table_row_extra_cell", lambda t: sub(t, "| A1 Read topology via API | ● | ● | ◐ | ◐ | ◐ | ●◌ |", "| A1 Read topology via API | ● | ● | ◐ | ◐ | ◐ | ●◌ | ● |"), "table row")
build("sec2_table_missing", lambda t: sub(t, "### P15 `When NDTwin is the right pick`   form: table\n| you need | NDTwin | nearest alternative | tasks |\n", "### P15 `When NDTwin is the right pick`   form: table\n"), "no section-2 table")
build("matrix_cell_flag_dropped", lambda t: sub(t, "| A1 Read topology via API | ● | ● | ◐ | ◐ | ◐ | ●◌ |", "| A1 Read topology via API | ● | ● | ◐ | ◐ | ◐ | ● |"), "differs from matrix_final.json")
build("matrix_cell_glyph_changed", lambda t: sub(t, "| O5 Fault drills on a copy | ● | ● | ? | ● | ● | ◐ | ◐ | ●⚠ |", "| O5 Fault drills on a copy | ● | ● | ? | ● | ◐ | ◐ | ◐ | ●⚠ |"), "differs from matrix_final.json")
build("matrix_columns_swapped", lambda t: sub(t, "| task | P4 tutorials VM | p4-utils | ONOS+Stratum | NDTwin |", "| task | P4 tutorials VM | ONOS+Stratum | p4-utils | NDTwin |"), "differs from matrix_final.json")
build("p15_flag_changed", lambda t: sub(t, "| ●⚠ (no group/meter on P4) |", "| ●⚠◌ (no group/meter on P4) |"), "differs from matrix_final.json")
build("p15_count_word_changed", lambda t: sub(t, "● on all four (⚠ three, ◌ four)", "● on all four (⚠ four, ◌ four)"), "flag counts")
build("p15_question_count_changed", lambda t: sub(t, "no other ● on P07 (3 ?)", "no other ● on P07 (2 ?)"), "the number of ? on")
build("p15_alternative_glyph_changed", lambda t: sub(t, "ONOS+Mininet: A2 ◐ · A3 ●", "ONOS+Mininet: A2 ● · A3 ●"), "differs from matrix_final.json")
build("p16_ndtwin_cell_changed", lambda t: sub(t, "| ◐ · ◐⚠◌ | P1, P3 |", "| ◐ · ◐⚠ | P1, P3 |"), "differs from matrix_final.json")

say(f"# {BAD[0]} FAIL (a FAIL here means a generator did not stop with its own named reason, or a control did not run)")
shutil.rmtree(TMP, ignore_errors=True)
if "--log" in sys.argv:
    d = sys.argv[sys.argv.index("--log") + 1]
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, "redcheck-1014-%s.log" % dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    import hashlib
    head = (f"# redcheck {dt.datetime.now(dt.timezone.utc):%Y-%m-%dT%H:%M:%SZ}; template NDTwin-slide-template-1014.md sha256 "
            f"{hashlib.sha256(open(T, 'rb').read()).hexdigest()[:16]}")
    open(f, "w").write(head + "\n" + "\n".join(OUT) + "\n")
    print("[log] " + f)
sys.exit(1 if BAD[0] else 0)
