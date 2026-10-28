#!/usr/bin/env python3
"""Check the built NDTwin_deck_1028.pptx against template section 1 / section 2 (adapted from verify_deck_1014.py).

Per slide, in order: the page id the template's section 1 puts there; notes present and equal to that page's
section-2 block (whitespace-insensitive; default NOTES_MODE=speaker compares from the speaker-notes line on, NOTES_MODE=block the whole block); a figure
page carries exactly one picture whose bytes are the intended figures/<topic>/_hires/<stem>.png (sha256) at
that PNG's aspect ratio (+-1 %) and no text but the page number; a table page carries the section-1 title and
a table whose cells equal the section-2 markdown table (backticks dropped) and no other text but the page
number; a page whose status "waits" for the hands-on run carries the title and ONE table cell "pending:
hands-on results"; the title page carries the title and "Adam".  Reads the pptx as a zip; writes nothing but
its log.  Then: a font-size / estimated-bottom report for every table page (Liberation Sans metrics, wider than
Calibri, so an upper bound), and negative controls (a cell, a note, a picture's bytes, a page order swapped in
copies of the pptx: each must FAIL).

Usage: verify_deck_1028.py [--no-negative] [--log DIR]
Also (1028): a geometry check -- every picture, table and text box lies inside the slide, a figure fills the
content area (its placed width or height is at least 95 % of the 12.90 x 6.72 in box) and no table frame
overlaps the title band.
[Co-developed with claude code -- Adam]"""
import datetime as dt
import hashlib
import io
import os
import re
import shutil
import struct
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PPTX = os.path.join(D, "NDTwin_deck_1028.pptx")
TPL = os.environ.get("TEMPLATE_1028") or os.path.join(D, "NDTwin-slide-template-1028.md")
NOTES_MODE = os.environ.get("NOTES_MODE", "speaker")
NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "rel": "http://schemas.openxmlformats.org/package/2006/relationships"}
EMU = 914400.0
PAGE_NUM_Y = 6.92      # inches; the page number sits here
FIT_LIMIT = 6.85       # a table bottom below this clears the page number
MIN_FONT = 12.0
NPAGES = 9
SLIDE_W, SLIDE_H = 13.333, 7.5
PENDING_TEXT = "pending: hands-on results"
SPEAKER_MARK = "講者備註"


def squash(s):
    return re.sub(r"\s+", "", s)


def png_wh(b):
    return struct.unpack(">II", b[16:24])


def load_template():
    t = open(TPL, encoding="utf-8").read()
    sec1 = t.split("\n## 1. ")[1].split("\n## 2. ")[0]
    order = []
    for ln in sec1.splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|\s*(P\d\d)\s*\|\s*(.+?)\s*\|\s*(\d+)\s*\|\s*(title|figure|table)(?:\s*`([\w\-/]+)`)?\s*\|"
                     r"\s*(.+?)\s*\|\s*(.*?)\s*\|\s*$", ln)
        if m:
            order.append({"n": int(m.group(1)), "id": m.group(2), "title": m.group(3), "form": m.group(5),
                          "fig": m.group(6), "status": m.group(8),
                          "pending": re.search(r"\bwaits\b", m.group(8), re.I) is not None})
    sec2 = t.split("\n## 2. ")[1].split("\n## 3. ")[0]
    notes = {}
    for b in sec2.split("\n### ")[1:]:
        bid = b.split()[0]
        body = "\n".join(b.split("\n")[1:]).strip()
        if NOTES_MODE == "speaker":
            i = body.find(SPEAKER_MARK)
            body = body[i:].strip() if i >= 0 else ""
        notes[bid] = body
    blocks = {}
    for b in sec2.split("\n### ")[1:]:
        blocks[b.split()[0]] = "\n".join(b.split("\n")[1:]).strip()
    return t, sec1, sec2, order, notes, blocks


def md_table(block):
    first = []
    for ln in block.splitlines():
        if ln.startswith("|"):
            first.append(ln)
        elif first:
            break
    if len(first) < 3:
        return None
    cells = [[c.strip().replace("`", "") for c in r.strip().strip("|").split("|")] for r in first]
    return [cells[0]] + cells[2:]


# ------------------------------------------------------------------ table height estimate
try:
    from PIL import ImageFont
    _F = {}

    def _font(bold, size):
        k = (bold, round(size * 4))
        if k not in _F:
            path = "/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf" % ("Bold" if bold else "Regular")
            _F[k] = ImageFont.truetype(path, int(round(size * 10)))     # 10 px per pt: fine metrics
        return _F[k]

    def text_w_in(text, size, bold):
        w = 0.0
        for ch in text:
            if ch in "●◐○⚠◌":
                w += size * 1.0
            else:
                w += _font(bold, size).getlength(ch)
        return (w / 10.0 if True else w) / 72.0 if False else _mixed(text, size, bold)

    def _mixed(text, size, bold):
        tot = 0.0
        for ch in text:
            if ch in "●◐○⚠◌":
                tot += size
            else:
                tot += _font(bold, size).getlength(ch) / 10.0
        return tot / 72.0
    HAVE_PIL = True
except Exception:     # no PIL: 0.55 em average
    HAVE_PIL = False

    def text_w_in(text, size, bold):
        return len(text) * size * 0.55 / 72.0
if HAVE_PIL:
    text_w_in = _mixed


def lines_needed(runs, avail_in):
    """runs: [(text, size, bold)]; greedy wrap on spaces and after hyphens; returns (lines, tallest size)."""
    words = []
    for text, size, bold in runs:
        for tok in re.findall(r"[^ \-]+-?| ", text):
            words.append((tok, size, bold))
    lines, cur = 1, 0.0
    maxsz = max([r[1] for r in runs] or [12])
    for tok, size, bold in words:
        w = text_w_in(tok, size, bold)
        if tok == " ":
            cur += w
            continue
        if cur + w > avail_in and cur > 0:
            lines += 1
            cur = w
        else:
            cur += w
    return lines, maxsz


def estimate_table(tbl, frame_y_in):
    cols = [int(g.get("w")) / EMU for g in tbl.find("a:tblGrid", NS)]
    total, minsz, sizes = frame_y_in, 99.0, set()
    for tr in tbl.findall("a:tr", NS):
        rowh = int(tr.get("h")) / EMU
        need = 0.0
        ci = 0
        for tc in tr.findall("a:tc", NS):
            span = int(tc.get("gridSpan", "1"))
            if tc.get("hMerge"):
                ci += 1
                continue
            w = sum(cols[ci:ci + span])
            ci += span
            pr = tc.find("a:tcPr", NS)
            mL = int(pr.get("marL", "91440")) / EMU if pr is not None else 0.1
            mR = int(pr.get("marR", "91440")) / EMU if pr is not None else 0.1
            mT = int(pr.get("marT", "45720")) / EMU if pr is not None else 0.05
            mB = int(pr.get("marB", "45720")) / EMU if pr is not None else 0.05
            runs = []
            for r in tc.iter("{%s}r" % NS["a"]):
                rp = r.find("a:rPr", NS)
                sz = float(rp.get("sz", "1800")) / 100.0 if rp is not None else 18.0
                bold = rp is not None and rp.get("b") == "1"
                t = r.find("a:t", NS)
                if t is not None and t.text:
                    runs.append((t.text, sz, bold))
                    minsz = min(minsz, sz)
                    sizes.add(sz)
            if not runs:
                continue
            n, msz = lines_needed(runs, max(w - mL - mR, 0.1))
            need = max(need, n * msz * 1.2 / 72.0 + mT + mB)
        total += max(rowh, need)
    return total, (minsz if minsz < 99 else None), sorted(sizes)


# ------------------------------------------------------------------ the checks
def verify(pptx_path, say, label=""):
    """Run every structural check on pptx_path; returns the number of FAILs. say(line) prints a line."""
    t, sec1, sec2, order, notes, blocks = load_template()
    bad = [0]
    report = []

    def check(ok, s):
        say(("ok    " if ok else "FAIL  ") + s)
        if not ok:
            bad[0] += 1

    z = zipfile.ZipFile(pptx_path)
    pres = ET.fromstring(z.read("ppt/presentation.xml"))
    prels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("ppt/_rels/presentation.xml.rels"))}
    slides = ["ppt/" + prels[s.get("{%s}id" % NS["r"])] for s in pres.find("p:sldIdLst", NS)]
    check(len(slides) == len(order) == NPAGES, f"{len(slides)} slides; template section 1 lists {len(order)} pages; want {NPAGES}")
    bad_ppr = sum(len(re.findall(rb"</a:r><a:pPr", z.read(n))) for n in z.namelist()
                  if re.match(r"ppt/slides/slide\d+\.xml$", n))
    check(bad_ppr == 0, f"no <a:pPr> after a run inside any paragraph (schema order): {bad_ppr} found")
    forms = [o["form"] for o in order]
    check([forms.count("title"), forms.count("figure"), forms.count("table")] == [1, 3, 5],
          f"section-1 form counts title/figure/table = {forms.count('title')}/{forms.count('figure')}/{forms.count('table')}")
    seen_notes = {}
    for o, path in zip(order, slides):
        num, pid, title, form, fig = o["n"], o["id"], o["title"], o["form"], o["fig"]
        x = ET.fromstring(z.read(path))
        rp = path.replace("slides/", "slides/_rels/") + ".rels"
        rels = {r.get("Id"): (r.get("Type").rsplit("/", 1)[-1], r.get("Target")) for r in ET.fromstring(z.read(rp))}
        pend = " pending" if o["pending"] else ""
        tag = f"p{num:02d} {pid} {form:6s}{pend:8s}"
        # notes
        nt = [v[1] for v in rels.values() if v[0] == "notesSlide"]
        if not nt:
            check(False, f"{tag} no notes slide")
        else:
            nx = ET.fromstring(z.read(os.path.normpath(os.path.join(os.path.dirname(path), nt[0]))))
            text = "".join(e.text or "" for e in nx.iter("{%s}t" % NS["a"]))
            # the notes slide also holds a slide-number field; its text is a digit string
            want = notes.get(pid, "")
            sq, sw = squash(text), squash(want)
            ok = bool(want) and (sq == sw or sq == sw + str(num) or sq == str(num) + sw)
            check(ok, f"{tag} notes = section 2 {pid} ({len(want)} chars in section 2, {len(text)} in the notes slide)")
            if ok:
                seen_notes[pid] = True
        pics = x.findall(".//p:pic", NS)
        tables = x.findall(".//a:tbl", NS)
        alltext = [e.text or "" for e in x.iter("{%s}t" % NS["a"])]
        # text outside the table(s): title, page number, signature
        tbl_text = set()
        for tb in tables:
            for e in tb.iter("{%s}t" % NS["a"]):
                tbl_text.add(id(e))
        free = [e.text or "" for e in x.iter("{%s}t" % NS["a"]) if id(e) not in tbl_text and (e.text or "").strip()]
        if form == "title":
            ok = free == [title, "Adam"] and not pics and not tables
            check(ok, f"{tag} title page text {free} (want [{title!r}, 'Adam'])")
        elif o["pending"]:
            cells = [["".join(e.text or "" for e in tc.iter("{%s}t" % NS["a"])) for tc in tr.findall("a:tc", NS)]
                     for tr in tables[0].findall("a:tr", NS)] if len(tables) == 1 else None
            check(len(tables) == 1 and not pics and cells == [[PENDING_TEXT]],
                  f"{tag} one grey cell {PENDING_TEXT!r}: cells {cells}, pictures {len(pics)}")
            check(sorted(free) == sorted([title, str(num)]),
                  f"{tag} other text = title {title!r} + page number only: {free}")
        elif form == "figure":
            ok = len(pics) == 1 and not tables
            if ok:
                rid = pics[0].find(".//a:blip", NS).get("{%s}embed" % NS["r"])
                media = os.path.normpath(os.path.join(os.path.dirname(path), rels[rid][1]))
                b = z.read(media)
                topic, stem = fig.split("/")
                src = os.path.join(D, "figures", topic, "_hires", stem + ".png")
                if not os.path.exists(src):
                    check(False, f"{tag} figure source {src} missing")
                else:
                    same = hashlib.sha256(b).hexdigest() == hashlib.sha256(open(src, "rb").read()).hexdigest()
                    w, h = png_wh(b)
                    ext = pics[0].find(".//a:xfrm/a:ext", NS)
                    ar = int(ext.get("cx")) / int(ext.get("cy"))
                    ok = same and abs(ar / (w / h) - 1) < 0.01
                    check(ok, f"{tag} one picture = {topic}/_hires/{stem}.png (bytes {'identical' if same else 'DIFFER'}; "
                              f"placed a/r {ar:.3f} vs png {w / h:.3f})")
            else:
                check(False, f"{tag} expected one picture, found {len(pics)} pictures and {len(tables)} tables")
            check(free == [str(num)], f"{tag} no text on the page but the page number: {free}")
        elif form == "table":
            if len(tables) != 1 or pics:
                check(False, f"{tag} expected one table, found {len(tables)} tables and {len(pics)} pictures")
                continue
            cells = [["".join(e.text or "" for e in tc.iter("{%s}t" % NS["a"])) for tc in tr.findall("a:tc", NS)]
                     for tr in tables[0].findall("a:tr", NS)]
            want = md_table(blocks.get(pid, ""))
            check(cells == want, f"{tag} table = section 2 {pid} verbatim ({len(cells) - 1} rows x {len(cells[0])} cols)")
            if cells != want:
                for i, (a, b) in enumerate(zip(cells, want or [])):
                    if a != b:
                        say(f"      row {i}: pptx {a}\n      row {i}: sec2 {b}")
            check(sorted(free) == sorted([title, str(num)]),
                  f"{tag} other text = title {title!r} ({len(title)} chars) + page number only: {free}")
    check(len(seen_notes) == NPAGES, f"notes matched on {len(seen_notes)} of {NPAGES} pages")
    geometry(z, slides, order, check)
    return bad[0], z, slides, order


def geometry(z, slides, order, check):
    """Every picture / table / text frame inside the slide; a figure fills the content area (>= 95 % of the
    12.90 x 6.72 in box in width or height); a table frame starts below the title band (y >= 1.10 in)."""
    for o, path in zip(order, slides):
        x = ET.fromstring(z.read(path))
        tag = f"p{o['n']:02d} {o['id']} {o['form']:6s}"
        frames = []
        for el in list(x.iter("{%s}pic" % NS["p"])) + list(x.iter("{%s}graphicFrame" % NS["p"])) + \
                list(x.iter("{%s}sp" % NS["p"])):
            off = el.find(".//a:off", NS)
            ext = el.find(".//a:ext", NS)
            if off is None or ext is None or ext.get("cx") is None:
                continue
            fx, fy = int(off.get("x")) / EMU, int(off.get("y")) / EMU
            fw, fh = int(ext.get("cx")) / EMU, int(ext.get("cy")) / EMU
            frames.append((el.tag.rsplit("}", 1)[-1], fx, fy, fw, fh))
        inside = all(fx >= -1e-3 and fy >= -1e-3 and fx + fw <= SLIDE_W + 1e-3 and fy + fh <= SLIDE_H + 1e-3
                     for _, fx, fy, fw, fh in frames)
        check(inside, f"{tag} geometry: {len(frames)} frames, all inside {SLIDE_W} x {SLIDE_H} in")
        if o["form"] == "figure":
            pics = [f for f in frames if f[0] == "pic"]
            if pics:
                _, fx, fy, fw, fh = pics[0]
                fill = max(fw / 12.90, fh / 6.72)
                check(fill >= 0.95, f"{tag} geometry: figure fills {fill * 100:.1f} % of the content box (want >= 95 %)")
        if o["form"] == "table":
            gf = [f for f in frames if f[0] == "graphicFrame"]
            check(bool(gf) and gf[0][2] >= 1.10, f"{tag} geometry: table frame top {gf[0][2] if gf else None} in "
                                                  f"(title band ends at 1.10 in)")


def fit_report(z, slides, order, say):
    over = []
    say("# table pages: font size and estimated bottom (in); page number at %.2f in; limit %.2f in; min font %.0f pt"
        % (PAGE_NUM_Y, FIT_LIMIT, MIN_FONT))
    say("# estimator: %s, 1.2 x font line height, cell margins as in the pptx; upper bound (Liberation Sans is wider than Calibri)"
        % ("Liberation Sans metrics via PIL" if HAVE_PIL else "0.55 em average (PIL missing)"))
    for o, path in zip(order, slides):
        if o["form"] != "table" or o["pending"]:
            continue
        x = ET.fromstring(z.read(path))
        gf = x.find(".//p:graphicFrame", NS)
        off = gf.find(".//p:xfrm/a:off", NS)
        y_in = int(off.get("y")) / EMU
        tbl = x.find(".//a:tbl", NS)
        bottom, minsz, sizes = estimate_table(tbl, y_in)
        fits = bottom <= FIT_LIMIT and (minsz or 99) >= MIN_FONT
        say("%s %-3s %-44s font %s pt  top %.2f  est. bottom %.2f  %s" % (
            "fit " if fits else "OVER", o["id"], o["title"][:44], "/".join("%g" % s for s in sizes), y_in, bottom,
            "" if fits else ("(bottom past limit)" if bottom > FIT_LIMIT else "(font below %.0f pt)" % MIN_FONT)))
        if not fits:
            over.append(o["id"])
    say("# tables that do not fit at >= %.0f pt: %s" % (MIN_FONT, ", ".join(over) if over else "none"))
    return over


# ------------------------------------------------------------------ negative controls
def mutate_copy(src, dst, fn):
    zin = zipfile.ZipFile(src)
    zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
    for item in zin.infolist():
        data = zin.read(item.filename)
        new = fn(item.filename, data)
        zout.writestr(item, new if new is not None else data)
    zout.close()


def negative_controls(say):
    tmp = tempfile.mkdtemp(prefix="verify1028_")
    t, sec1, sec2, order, notes, blocks = load_template()
    slide_of = {}
    z = zipfile.ZipFile(PPTX)
    pres = ET.fromstring(z.read("ppt/presentation.xml"))
    prels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("ppt/_rels/presentation.xml.rels"))}
    slides = ["ppt/" + prels[s.get("{%s}id" % NS["r"])] for s in pres.find("p:sldIdLst", NS)]
    for o, p in zip(order, slides):
        slide_of[o["id"]] = p
    results = []

    def run(name, fn):
        dst = os.path.join(tmp, name + ".pptx")
        mutate_copy(PPTX, dst, fn)
        buf = []
        n, *_ = verify(dst, buf.append)
        say(f"-- negative control {name}: {n} FAIL")
        for ln in buf:
            if ln.startswith("FAIL"):
                say("   " + ln)
        results.append((name, n))

    # 1. one table cell changed (P06: the proxy-restart result)
    def f1(fn, data):
        if fn == slide_of["P06"]:
            s = data.decode("utf-8")
            assert "records unchanged" in s
            return s.replace("records unchanged", "records changed", 1).encode("utf-8")
    run("one_cell_P06", f1)

    # 2. one note changed (P03)
    def f2(fn, data):
        if fn.startswith("ppt/notesSlides/") and fn.endswith(".xml"):
            s = data.decode("utf-8")
            if "最主要的設計取捨" in s:
                return s.replace("最主要的設計取捨", "次要的設計取捨").encode("utf-8")
    run("one_note_P03", f2)

    # 3. one picture's bytes changed (P04)
    zz = zipfile.ZipFile(PPTX)
    rp = slide_of["P04"].replace("slides/", "slides/_rels/") + ".rels"
    media = None
    for r in ET.fromstring(zz.read(rp)):
        if r.get("Type").endswith("/image"):
            media = os.path.normpath(os.path.join(os.path.dirname(slide_of["P04"]), r.get("Target")))

    def f3(fn, data):
        if fn == media:
            b = bytearray(data)
            b[-20] ^= 0xFF
            return bytes(b)
    run("one_picture_P04", f3)

    # 4. page order: P06 and P07 swapped in presentation.xml
    def f4(fn, data):
        if fn == "ppt/presentation.xml":
            s = data.decode("utf-8")
            ids = re.findall(r"<p:sldId [^>]*/>", s)
            a, b = ids[5], ids[6]
            return s.replace(a, "@@A@@").replace(b, a).replace("@@A@@", b).encode("utf-8")
    run("order_swap_P06_P07", f4)

    # 5. an extra text on a figure page (P05): add a stray run to the slide XML
    def f5(fn, data):
        if fn == slide_of["P05"]:
            s = data.decode("utf-8")
            extra = ('<p:sp><p:nvSpPr><p:cNvPr id="99" name="x"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr/>'
                     '<p:txBody><a:bodyPr/><a:p><a:r><a:t>caption</a:t></a:r></a:p></p:txBody></p:sp>')
            return s.replace("</p:spTree>", extra + "</p:spTree>").encode("utf-8")
    run("stray_text_P05", f5)

    # 6. geometry: the P09 picture pushed half off the slide
    def f6(fn, data):
        if fn == slide_of["P09"]:
            s = data.decode("utf-8")
            return re.sub(r'(<p:pic>.*?<a:off x=")(\d+)', lambda m: m.group(1) + str(int(m.group(2)) + 6000000), s,
                          count=1, flags=re.S).encode("utf-8")
    run("picture_off_slide_P09", f6)
    shutil.rmtree(tmp, ignore_errors=True)
    return results


def main():
    out = []

    def say(s):
        out.append(s)
        print(s)
    t, sec1, sec2, order, notes, blocks = load_template()
    say(f"# verify {os.path.basename(PPTX)} {dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')}; "
        f"sha256 {hashlib.sha256(open(PPTX, 'rb').read()).hexdigest()[:16]}; template sha256 "
        f"{hashlib.sha256(t.encode()).hexdigest()[:16]}; the parts checked (section 1 page table + section 2) sha256 "
        f"{hashlib.sha256((sec1 + sec2).encode()).hexdigest()[:16]}; notes mode {NOTES_MODE}")
    nbad, z, slides, order = verify(PPTX, say)
    say(f"# {nbad} FAIL")
    over = fit_report(z, slides, order, say)
    ctl = []
    if "--no-negative" not in sys.argv:
        say("# negative controls (copies of the pptx, one thing broken in each; every one must report FAIL)")
        ctl = negative_controls(say)
        say("# negative controls: " + ", ".join(f"{n}={k} FAIL" for n, k in ctl)
            + ("; ALL FAILED AS REQUIRED" if all(k > 0 for _, k in ctl) else "; SOME CONTROL DID NOT FAIL"))
    logdir = None
    if "--log" in sys.argv:
        logdir = sys.argv[sys.argv.index("--log") + 1]
    if logdir:
        os.makedirs(logdir, exist_ok=True)
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        log = os.path.join(logdir, f"verify-deck-1028-{stamp}.log")
        open(log, "w").write("\n".join(out) + "\n")
        print(f"[log] {log}")
    bad_ctl = any(k == 0 for _, k in ctl)
    sys.exit(1 if (nbad or bad_ctl) else 0)


if __name__ == "__main__":
    main()
