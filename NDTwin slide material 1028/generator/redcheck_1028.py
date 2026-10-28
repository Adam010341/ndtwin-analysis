#!/usr/bin/env python3
"""Red-check of the 1028 deck (template section 0 rules 3-7 and 11).

Part A, the content scan (`redcheck_1028.py [--target DIR]`): read every text the audience or the speaker will
see -- slide text and speaker notes of DIR/NDTwin_deck_1028.pptx, the speaker script
DIR/NDTwin-speaker-script-1028.md, the read-aloud script DIR/NDTwin-verbatim-script-1028.md, and the text of every figure under DIR/figures (from its .svg, which
matplotlib writes with real text) -- and FAIL, naming the rule, on:
  * a commit-like token: 7 or more hex characters with at least one digit and one letter;
  * a PR reference: "PR #n", "PR n", "#4x", "pull request";
  * a source citation in notes or script (path:line, or a file name with a code/log extension);
  * a fix item from rule 5 (write replies that used to say 200 on failure, priority/dpid validation,
    Release-build warnings, in_port masking, binding to 127.0.0.1, table-entry journal replay, the
    modify-priority landing fix);
  * a 10/14 repeat from rule 6 (ternary/range/optional writes, P4Runtime error codes in a 502, detect-only
    link down, the P4 health check);
  * on a figure: a date or time stamp, or any provenance text (figstyle_1028.PROVENANCE);
  * a slide title over 45 characters; a script without a section per page or without the
    "被問到時不要這樣說" section.
Exit 0 only when nothing is found.

Part B, `--selftest`: copy the real deck into a temp dir, seed ONE bad thing into the copy per case (in a slide,
a note, the script or a figure), run part A on the copy and require a FAIL with that case's rule; the unseeded
copy is the control and must pass. Then the generator cases: each figure generator and the deck build is run
on a broken copy of its input and must stop with its own named reason (controls: unbroken inputs exit 0).
Writes nothing under the deck folder except the log (--log DIR).

[Co-developed with claude code -- Adam]"""
import datetime as dt
import glob
import hashlib
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.dirname(HERE)
VENV = os.environ.get("NDTWIN_PLOTVENV") or os.path.normpath(
    os.path.join(DECK, "..", "NDTwin Slide material 820", ".plotvenv", "bin", "python3"))
PPTX_NAME, SCRIPT_NAME = "NDTwin_deck_1028.pptx", "NDTwin-speaker-script-1028.md"
VERBATIM_NAME = "NDTwin-verbatim-script-1028.md"   # the read-aloud script; same rules as the speaker script
NPAGES = 9

HEX = re.compile(r"\b(?=[0-9a-f]*[0-9])(?=[0-9a-f]*[a-f])[0-9a-f]{7,64}\b", re.I | re.A)
PRREF = re.compile(r"\bPR\s*#?\s*\d+|#4\d\b|pull request", re.I | re.A)
CITE = re.compile(r"[\w/.-]+\.(py|js|sh|cpp|hpp|md|json|log|txt|tsv|p4)(:\d+)?\b|[\w/.-]+:\d+-\d+\b", re.A)
FIX = [
    ("rule-5 fix item: write replies that used to say 200 on failure",
     r"200 on failure|used to (say|answer|return) 200|honest (p4 )?write|non-2xx|誠實的寫入|失敗.{0,8}(回|說).{0,4}200"),
    ("rule-5 fix item: priority / dpid validation",
     r"priority (validation|check)|dpid (validation|check)|0 (to|-) ?65535|priority.{0,20}not an integer|優先權.{0,4}檢查|dpid.{0,4}檢查"),
    ("rule-5 fix item: Release-build warnings",
     r"maybe-uninitiali[sz]ed|release[- ]build warning|-Werror|Release.{0,6}(警告|warning)"),
    ("rule-5 fix item: in_port masking", r"in_port.{0,20}mask|mask(ed|ing|s)? .{0,12}in_port|in_port.{0,6}遮罩"),
    ("rule-5 fix item: binding bmv2/proxy to 127.0.0.1",
     r"127\.0\.0\.1|listens? on (localhost|loopback)|bind(s|ing)? .{0,20}(localhost|loopback|127)|綁.{0,4}(本機|127)|NDTWIN_BMV2_HOST"),
    ("rule-5 fix item: table-entry journal replay after a proxy restart",
     r"table[_ -]entry.{0,40}(replay|journal)|journal.{0,20}replay(ed)? .{0,20}(after|on) .{0,10}restart|table_entry.{0,20}重放"),
    ("rule-5 fix item: modify-priority landing fix",
     r"modify.{0,40}(lands?|landing)|slot'?s? priority|slot priority|modify.{0,10}priority"),
]
REPEAT = [
    ("rule-6 repeat of 10/14: ternary/range/optional writes",
     r"\bternary\b|\brange (entry|entries|match|write)s?\b|\boptional (entry|entries|match|write)s?\b"),
    ("rule-6 repeat of 10/14: P4Runtime error codes in a 502", r"p4rt_error|P4Runtime error code|P4Runtime 錯誤碼"),
    ("rule-6 repeat of 10/14: detect-only link down", r"detect[- ]only|只偵測"),
    ("rule-6 repeat of 10/14: the P4 health check", r"health check|健檢|p4_health"),
]
# re.A everywhere: under re.U a CJK character counts as \w, so "在12e5c080之後" has no \b around the token.
FIX = [(n, re.compile(r, re.I | re.A)) for n, r in FIX]
REPEAT = [(n, re.compile(r, re.I | re.A)) for n, r in REPEAT]
FIGDATE = [
    ("date stamp on a figure", re.compile(r"\b20\d\d-[01]\d-[0-3]\d\b|\b\d{1,2}/\d{1,2}(/20\d\d)?\b|\b20\d\d[01]\d[0-3]\d\b", re.A)),
    ("time stamp on a figure", re.compile(r"\b\d\d:\d\d(:\d\d)?Z?\b|\bT\d{6}Z\b", re.A)),
]


# ------------------------------------------------------------------ part A: what to read
def pptx_texts(path):
    """[(where, text)]: one entry per paragraph of every slide and every notes slide."""
    out = []
    z = zipfile.ZipFile(path)
    names = sorted((n for n in z.namelist() if re.match(r"ppt/(slides|notesSlides)/\w+?\d+\.xml$", n)),
                   key=lambda n: (n.split("/")[1], int(re.findall(r"\d+", n.rsplit("/", 1)[1])[0])))
    for n in names:
        x = z.read(n).decode("utf-8")
        kind = "slide" if "/slides/" in n else "notes"
        num = re.findall(r"\d+", n.rsplit("/", 1)[1])[0]
        for para in re.findall(r"<a:p>.*?</a:p>|<a:p .*?</a:p>", x, re.S):
            t = "".join(html.unescape(m) for m in re.findall(r"<a:t>(.*?)</a:t>", para, re.S))
            if t.strip():
                out.append((f"{kind} {num}", t))
    return out


def slide_titles(path):
    """The first text of every non-notes slide that is not the page number."""
    z = zipfile.ZipFile(path)
    titles = []
    for n in sorted((n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)),
                    key=lambda n: int(re.findall(r"\d+", n)[0])):
        ts = [html.unescape(t) for t in re.findall(r"<a:t>(.*?)</a:t>", z.read(n).decode("utf-8"), re.S)]
        ts = [t for t in ts if t.strip() and not t.strip().isdigit()]
        if ts:
            titles.append((n, ts[0]))
    return titles


def svg_texts(path):
    s = open(path, encoding="utf-8").read()
    out = []
    for m in re.findall(r"<text\b[^>]*>(.*?)</text>", s, re.S):
        t = html.unescape(re.sub(r"<[^>]+>", "", m)).strip()
        if t:
            out.append(t)
    return out


def scan(target):
    """[(rule, where, snippet)] for every hit in the deck folder `target`."""
    hits = []

    def text_rules(where, t, cite=True):
        for m in HEX.finditer(t):
            hits.append(("commit-like token", where, m.group(0)))
        for m in PRREF.finditer(t):
            hits.append(("PR reference", where, m.group(0)))
        if cite:
            for m in CITE.finditer(t):
                hits.append(("source citation", where, m.group(0)))
        for name, rx in FIX + REPEAT:
            m = rx.search(t)
            if m:
                hits.append((name, where, m.group(0)))

    pptx = os.path.join(target, PPTX_NAME)
    if not os.path.exists(pptx):
        hits.append(("deck missing", pptx, ""))
    else:
        for where, t in pptx_texts(pptx):
            text_rules(where, t)
        for n, t in slide_titles(pptx):
            if len(t) > 45:
                hits.append(("slide title over 45 chars", n, t))
    script = os.path.join(target, SCRIPT_NAME)
    if not os.path.exists(script):
        hits.append(("speaker script missing", script, ""))
    else:
        st = open(script, encoding="utf-8").read()
        for i, ln in enumerate(st.splitlines(), 1):
            text_rules(f"script line {i}", ln)
        for k in range(1, NPAGES + 1):
            if not re.search(rf"^## P{k:02d}\b", st, re.M):
                hits.append(("script has no section for a page", f"P{k:02d}", ""))
        if "被問到時不要這樣說" not in st:
            hits.append(("script has no '被問到時不要這樣說' section", script, ""))
    verb = os.path.join(target, VERBATIM_NAME)
    if not os.path.exists(verb):
        hits.append(("verbatim script missing", verb, ""))
    else:
        vt = open(verb, encoding="utf-8").read()
        for i, ln in enumerate(vt.splitlines(), 1):
            text_rules(f"verbatim line {i}", ln)
        for k in range(1, NPAGES + 1):
            if not re.search(rf"^## P{k:02d} ", vt, re.M):
                hits.append(("verbatim script has no section for a page", f"P{k:02d}", ""))
        for need in ("## 被問到時可以這樣答", "## 不要這樣說"):
            if need not in vt:
                hits.append((f"verbatim script has no '{need[3:]}' section", verb, ""))
    sys.path.insert(0, HERE)
    import figstyle_1028 as FS  # the figure generators' own provenance list
    svgs = sorted(glob.glob(os.path.join(target, "figures", "*", "*.svg")))
    if not svgs:
        hits.append(("no figure svg to read", os.path.join(target, "figures"), ""))
    for svg in svgs:
        where = "figure " + os.path.relpath(svg, target)
        for t in svg_texts(svg):
            for name, rx in FIGDATE:
                m = rx.search(t)
                if m:
                    hits.append((name, where, t))
            for why, rx in FS.PROVENANCE:
                if rx.search(t):
                    hits.append((f"provenance on a figure ({why})", where, t))
                    break
            text_rules(where, t, cite=False)
    return hits


def report(target, say):
    hits = scan(target)
    for rule, where, snip in hits:
        say(f"FAIL  {rule}: {where}: {snip[:120]!r}")
    say(f"# content scan of {target}: {len(hits)} hit(s) -> {'RED' if hits else 'GREEN'}")
    return hits


# ------------------------------------------------------------------ part B: seeded copies + generator cases
OUT, BAD = [], [0]


def say(s):
    OUT.append(s)
    print(s)


def copy_deck(dst):
    os.makedirs(dst, exist_ok=True)
    shutil.copy2(os.path.join(DECK, PPTX_NAME), dst)
    shutil.copy2(os.path.join(DECK, SCRIPT_NAME), dst)
    shutil.copy2(os.path.join(DECK, VERBATIM_NAME), dst)
    shutil.copytree(os.path.join(DECK, "figures"), os.path.join(dst, "figures"))


def edit_pptx(path, member_rx, fn):
    tmp = path + ".tmp"
    zin, zout = zipfile.ZipFile(path), zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED)
    done = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if not done and re.match(member_rx, item.filename):
            new = fn(data.decode("utf-8"))
            if new is not None:
                data, done = new.encode("utf-8"), 1
        zout.writestr(item, data)
    zout.close()
    os.replace(tmp, path)
    assert done, f"redcheck harness: nothing in {member_rx} was edited"


def into_first_at(xml, text):
    """Append `text` to the first <a:t> of the XML (a run the reader will read)."""
    assert "<a:t>" in xml, "redcheck harness: no <a:t> to seed"
    return xml.replace("<a:t>", "<a:t>" + html.escape(text) + " ", 1)


def seeded(name, where, text, expect, tmp):
    d = os.path.join(tmp, "seed_" + name)
    copy_deck(d)
    if where == "slide":
        edit_pptx(os.path.join(d, PPTX_NAME), r"ppt/slides/slide6\.xml$",
                  lambda x: x.replace("records unchanged", "records unchanged " + html.escape(text), 1)
                  if "records unchanged" in x else None)
    elif where == "title":
        edit_pptx(os.path.join(d, PPTX_NAME), r"ppt/slides/slide7\.xml$",
                  lambda x: x.replace("What a fresh machine exposed", html.escape(text), 1))
    elif where == "note":
        edit_pptx(os.path.join(d, PPTX_NAME), r"ppt/notesSlides/notesSlide\d+\.xml$",
                  lambda x: into_first_at(x, text) if "講者備註" in x else None)
    elif where == "script":
        p = os.path.join(d, SCRIPT_NAME)
        s = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(s.replace("\n## P03", "\n" + text + "\n\n## P03", 1))
    elif where == "verbatim":
        p = os.path.join(d, VERBATIM_NAME)
        s = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(s.replace("\n## P03", "\n" + text + "\n\n## P03", 1))
    elif where == "verbatim_drop":
        p = os.path.join(d, VERBATIM_NAME)
        s = open(p, encoding="utf-8").read()
        assert text in s
        open(p, "w", encoding="utf-8").write(s.replace(text, "## Q&A", 1))
    elif where == "script_drop":
        p = os.path.join(d, SCRIPT_NAME)
        s = open(p, encoding="utf-8").read()
        assert text in s
        open(p, "w", encoding="utf-8").write(s.replace(text, "## Q&A", 1))
    elif where == "figure":
        p = os.path.join(d, "figures", "p4", "fig_p04_rules_lost.svg")
        s = open(p, encoding="utf-8").read()
        m = re.search(r"(<text\b[^>]*>)([^<]*)(</text>)", s)
        assert m, "redcheck harness: no <text> in the svg"
        s = s[:m.end()] + m.group(1) + html.escape(text) + m.group(3) + s[m.end():]
        open(p, "w", encoding="utf-8").write(s)
    buf = []
    hits = report(d, buf.append)
    rules = {h[0] for h in hits}
    ok = bool(hits) and any(expect in r for r in rules)
    got = sorted(rules)[:3]
    say(f"{'ok    ' if ok else 'FAIL  '}seeded {name} ({where}: {text!r}): wanted RED with {expect!r}; got "
        f"{'RED ' + str(got) if hits else 'GREEN'}")
    if not ok:
        BAD[0] += 1


def run_py(script, extra):
    return subprocess.run([VENV, os.path.join(HERE, script)] + extra, capture_output=True, text=True)


def case(name, p, expect):
    text = p.stdout + p.stderr
    if expect is None:
        ok = p.returncode == 0
        say(f"{'ok    ' if ok else 'FAIL  '}control {name}: rc={p.returncode}")
    else:
        ok = p.returncode != 0 and expect in text
        hit = [ln for ln in text.strip().splitlines() if expect in ln] or text.strip().splitlines()[-1:] or [""]
        say(f"{'ok    ' if ok else 'FAIL  '}{name}: rc={p.returncode}; wanted reason {expect!r}; got: {hit[0].strip()[:160]}")
    if not ok:
        BAD[0] += 1


def sub(t, old, new):
    assert old in t, f"redcheck harness: pattern not in input: {old!r}"
    return t.replace(old, new, 1)


def spec_case(tmp, gen, specname, label, fn, expect, extra=()):
    d = os.path.join(tmp, "gen_" + label)
    os.makedirs(d, exist_ok=True)
    spec = os.path.join(d, specname)
    open(spec, "w", encoding="utf-8").write(fn(open(os.path.join(DECK, "figures_spec", specname), encoding="utf-8").read()))
    case(f"{gen} {label}", run_py(gen + ".py", ["--spec", spec, "--out", os.path.join(d, "o")] + list(extra)), expect)


def node_path():
    if os.environ.get("NODE_PATH"):
        return os.environ["NODE_PATH"]
    hits = sorted(glob.glob(os.path.expanduser("~/.config/Claude/local-agent-mode-sessions/*/*/*/outputs/node_modules/pptxgenjs")))
    return os.path.dirname(hits[0]) if hits else ""


def build_case(tmp, label, fn, expect):
    d = os.path.join(tmp, "b_" + label)
    os.makedirs(d, exist_ok=True)
    tpl = os.path.join(d, "t.md")
    open(tpl, "w", encoding="utf-8").write(fn(open(os.path.join(DECK, "NDTwin-slide-template-1028.md"), encoding="utf-8").read()))
    env = dict(os.environ, NODE_PATH=node_path(), TEMPLATE_1028=tpl, OUT_1028=os.path.join(d, "out.pptx"))
    p = subprocess.run(["conda", "run", "-n", "webgui-node", "node", os.path.join(HERE, "build_deck_1028.js")],
                       capture_output=True, text=True, env=env, cwd=DECK)
    case("build " + label, p, expect)


def selftest():
    tmp = tempfile.mkdtemp(prefix="redcheck1028_")
    ID = lambda t: t  # noqa: E731
    say("# part B.1: seeded copies of the deck (one bad thing each); the content scan must go RED with that rule")
    d0 = os.path.join(tmp, "control")
    copy_deck(d0)
    buf = []
    n0 = len(report(d0, buf.append))
    say(f"{'ok    ' if n0 == 0 else 'FAIL  '}control: unseeded copy -> {'GREEN' if n0 == 0 else 'RED (' + str(n0) + ' hits)'}")
    BAD[0] += n0 != 0
    for args in [
        ("hash_in_slide", "slide", "a9d8925f", "commit-like token"),
        ("hash_in_note", "note", "proxy 在 12e5c080 之後", "commit-like token"),
        ("hash_in_script", "script", "這是 commit 5ab1c66a 的結果。", "commit-like token"),
        ("hash_on_figure", "figure", "cd3bd43b", "commit-like token"),
        ("pr_ref_in_note", "note", "見 PR #42", "PR reference"),
        ("pr_hash4x_in_script", "script", "這在 #41 裡合併。", "PR reference"),
        ("hash_no_space_cjk_in_note", "note", "在12e5c080之後", "commit-like token"),
        ("hash_cjk_in_verbatim", "verbatim", "這是在a9d8925f上跑的。", "commit-like token"),
        ("pr_in_verbatim", "verbatim", "這些都在PR#42裡。", "PR reference"),
        ("fix_item_in_verbatim", "verbatim", "寫入失敗以前會回 200，現在改成 502。", "write replies that used to say 200"),
        ("repeat_in_verbatim", "verbatim", "上次的健檢工具。", "the P4 health check"),
        ("verbatim_qna_dropped", "verbatim_drop", "## 被問到時可以這樣答", "被問到時可以這樣答"),
        ("pr_no_space_cjk_in_script", "script", "這在PR#41裡合併", "PR reference"),
        ("pr_hash4x_no_space_cjk_in_note", "note", "這在#41裡合併", "PR reference"),
        ("date_on_figure", "figure", "2026-10-26", "date stamp on a figure"),
        ("short_date_on_figure", "figure", "10/26", "date stamp on a figure"),
        ("time_on_figure", "figure", "12:05Z", "time stamp on a figure"),
        ("generator_name_on_figure", "figure", "make_p04_rules_lost.py", "provenance on a figure"),
        ("citation_in_note", "note", "出處 api_routes.py:1604", "source citation"),
        ("fix_502_in_script", "script", "寫入失敗以前 used to say 200，現在 502。", "write replies that used to say 200"),
        ("fix_honest_write_in_slide", "slide", "honest write replies", "write replies that used to say 200"),
        ("fix_priority_check_in_note", "note", "priority validation 0 to 65535", "priority / dpid validation"),
        ("fix_release_warning_in_script", "script", "修掉 maybe-uninitialized 警告", "Release-build warnings"),
        ("fix_in_port_in_note", "note", "in_port is masked to its width", "in_port masking"),
        ("fix_localhost_in_slide", "slide", "bmv2 listens on 127.0.0.1", "binding bmv2/proxy to 127.0.0.1"),
        ("fix_journal_replay_in_script", "script", "table_entry journal replay after a proxy restart", "table-entry journal replay"),
        ("fix_modify_priority_in_note", "note", "a modify lands at the slot's priority", "modify-priority landing"),
        ("repeat_ternary_in_slide", "slide", "ternary entries", "ternary/range/optional"),
        ("repeat_p4rt_error_in_note", "note", "p4rt_error in the 502", "P4Runtime error codes"),
        ("repeat_detect_only_in_script", "script", "外部控制器下只偵測斷線", "detect-only link down"),
        ("repeat_health_check_in_note", "note", "P4 health check", "the P4 health check"),
        ("title_over_45", "title", "What a fresh machine exposed on the very first day of it", "slide title over 45"),
        ("script_qna_section_dropped", "script_drop", "## 被問到時不要這樣說", "被問到時不要這樣說"),
    ]:
        seeded(*args, tmp=tmp)

    say("# part B.2: generators on broken inputs must stop with their own named reason")
    for g, spec in (("make_p04_rules_lost", "rules_lost_flow.txt"), ("make_p05_read_path", "read_path.txt"),
                    ("make_p09_next", "next.txt")):
        spec_case(tmp, g, spec, "unbroken", ID, None)
    spec_case(tmp, "make_p04_rules_lost", "rules_lost_flow.txt", "title_differs",
              lambda t: sub(t, "How the rule-loss notice reaches the app\n", "How the notice reaches the app\n"), "canvas title is")
    spec_case(tmp, "make_p04_rules_lost", "rules_lost_flow.txt", "step_missing",
              lambda t: sub(t, "  S6 | switch | 5 |", "  S7 | switch | 5 |"), "STEPS are")
    spec_case(tmp, "make_p04_rules_lost", "rules_lost_flow.txt", "unknown_lane",
              lambda t: sub(t, "  S2 | switch | 2 |", "  S2 | fabric | 2 |"), "which LANES does not list")
    spec_case(tmp, "make_p04_rules_lost", "rules_lost_flow.txt", "no_evidence",
              lambda t: re.sub(r"(  S2 \| switch \| 2 \| [^\n]*\n)(    [^\n]*\n)+", r"\1", t, count=1), "has no evidence line")
    spec_case(tmp, "make_p04_rules_lost", "rules_lost_flow.txt", "arrow_to_undrawn",
              lambda t: sub(t, "  S4 -> S5 | -", "  S4 -> S9 | -"), "not a drawn step")
    spec_case(tmp, "make_p04_rules_lost", "rules_lost_flow.txt", "label_too_long_for_box",
              lambda t: sub(t, "| Lost rules recorded |", "| Lost rules recorded per switch |"), "stick out of its box")
    spec_case(tmp, "make_p04_rules_lost", "rules_lost_flow.txt", "date_annotation",
              lambda t: sub(t, "  S3 -> S4 | polled at 1 Hz", "  S3 -> S4 | polled at 1 Hz (2026-10-26)"), "provenance text on the canvas")
    spec_case(tmp, "make_p05_read_path", "read_path.txt", "element_missing",
              lambda t: sub(t, "  CHK2 | 2  same device id and port | -", "  CHKX | 2  same device id and port | -"), "no entry for element CHK2")
    spec_case(tmp, "make_p05_read_path", "read_path.txt", "arrow_not_drawn",
              lambda t: sub(t, "  CHK1 -> CHK2 | -", "  R_DC -> CHK2 | -"), "does not list")
    spec_case(tmp, "make_p05_read_path", "read_path.txt", "label_too_long_for_box",
              lambda t: sub(t, "| 1  switch answers P4Runtime |", "| 1  the dpid's own switch answers one P4Runtime round trip |"), "stick out of its box")
    spec_case(tmp, "make_p05_read_path", "read_path.txt", "commit_on_canvas",
              lambda t: sub(t, "| NDTwin P4 proxy | REST :8081", "| NDTwin P4 proxy | REST :8081 at a9d8925f"), "provenance text on the canvas")
    spec_case(tmp, "make_p09_next", "next.txt", "p07_step_not_drawn",
              lambda t: re.sub(r"  B3 \| docs[^\n]*\n(    [^\n]*\n)+", "", t, count=1), "P07 row 3 names next step")
    spec_case(tmp, "make_p09_next", "next.txt", "box_in_unknown_lane",
              lambda t: sub(t, "  B8 | apps   |", "  B8 | build  |"), "which LANES does not list")
    spec_case(tmp, "make_p09_next", "next.txt", "bad_from",
              lambda t: sub(t, "| An app that resends on the notice | P08 row 5", "| An app that resends on the notice | someday"), "is not 'P07 row N'")
    spec_case(tmp, "make_p09_next", "next.txt", "p08_decide_step_not_drawn",
              lambda t: re.sub(r"  B7 \| decide[^\n]*\n(    [^\n]*\n)+", "", t, count=1), "P08 row 4 names next step")

    say("# part B.3: the deck build on broken copies of the template")
    build_case(tmp, "unbroken", ID, None)
    build_case(tmp, "page_row_dropped", lambda t: "\n".join(l for l in t.splitlines() if not l.startswith("| 9 | P09 |")) + "\n", "lists 8 pages")
    build_case(tmp, "chars_wrong", lambda t: sub(t, "| 7 | P07 | What a fresh machine exposed | 28 |", "| 7 | P07 | What a fresh machine exposed | 27 |"), "chars column says 27")
    build_case(tmp, "form_counts", lambda t: sub(t, "| 8 | P08 | Limits of the new features | 26 | table |", "| 8 | P08 | Limits of the new features | 26 | title |"), "form counts")
    build_case(tmp, "figure_file_missing", lambda t: sub(t, "`p4/fig_p05_read_path`", "`p4/fig_p05_read_paths`"), "missing figure file")
    build_case(tmp, "figure_title_differs", lambda t: sub(t, "| 5 | P05 | Reading registers and direct counters | 37 |", "| 5 | P05 | Reading registers and direct counter | 36 |"), "canvas title is")
    build_case(tmp, "notes_block_missing", lambda t: sub(t, "### P06 ", "## P06 "), "no block for P06")
    build_case(tmp, "table_row_extra_cell", lambda t: sub(t, "| proxy restart | 2 rules listed;", "| proxy restart | x | 2 rules listed;"), "table row")
    build_case(tmp, "hash_in_note", lambda t: sub(t, "- 這一頁是新功能本身的弱點", "- 見 5ab1c66a。這一頁是新功能本身的弱點"), "commit-like token")
    build_case(tmp, "pr_in_cell", lambda t: sub(t, "| paper-app converter |", "| paper-app converter (PR #41) |"), "PR reference")
    shutil.rmtree(tmp, ignore_errors=True)


def main():
    target = sys.argv[sys.argv.index("--target") + 1] if "--target" in sys.argv else DECK
    if "--selftest" in sys.argv:
        say("# part A on the real deck")
        nreal = len(report(DECK, say))
        BAD[0] += nreal != 0
        selftest()
        say(f"# {BAD[0]} FAIL (a FAIL here means a seeded copy stayed GREEN, a generator did not stop with its own "
            f"reason, a control did not pass, or the real deck is not GREEN)")
    else:
        nreal = len(report(target, say))
        BAD[0] += nreal != 0
    if "--log" in sys.argv:
        d = sys.argv[sys.argv.index("--log") + 1]
        os.makedirs(d, exist_ok=True)
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        tag = "selftest" if "--selftest" in sys.argv else ("real" if target == DECK else "target")
        f = os.path.join(d, f"redcheck-1028-{tag}-{stamp}.log")
        pp = os.path.join(target, PPTX_NAME)
        head = (f"# redcheck {stamp}; target {os.path.relpath(target, DECK) if target.startswith(DECK) else target}; "
                f"{PPTX_NAME} sha256 {hashlib.sha256(open(pp, 'rb').read()).hexdigest()[:16] if os.path.exists(pp) else '-'}")
        open(f, "w", encoding="utf-8").write(head + "\n" + "\n".join(OUT) + "\n")
        print("[log] " + f)
    sys.exit(1 if BAD[0] else 0)


if __name__ == "__main__":
    main()
