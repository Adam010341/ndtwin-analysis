// NDTwin report deck, 2026-10-14, "Why would a developer use NDTwin?". Twenty-two pages (template v0.5 draft).
//
// Built from NDTwin-slide-template-1014.md:  section 1 gives the page order, title and form of every page;
// section 2 gives the tables (cell for cell) and the speaker notes (verbatim, from the speaker-notes line
// "講者備註" to the end of the page's block; NOTES_MODE=block puts the whole block in, as the 930 generator did). Nothing about a page is typed in this file except layout
// (column widths, font sizes) and the glyph / persona palettes.
//
// Rules carried over from 930 (template section 0):
//   one figure OR one table per page, nothing else; figure pages carry no page title (the figure's own
//   canvas title is the slide title); table pages carry the section-1 title and the table; page number only.
//   Title page: the title and the signature "Adam" (template P01).
//   A page whose section-1 status says it "waits" for the hands-on run is built as the title and ONE grey
//   table cell "pending: hands-on results", so the page count stays 20. Its notes are still taken verbatim
//   from section 2. Since the hands-on run is archived, P10-P14 are "ready": P10 and P13 are figure pages
//   (figures/handson/, make_p10_setup.py and make_p13_relief.py), P11, P12 and P14 are table pages.
//
// Stops (throws) if: the page count is not 20; section 1 has a row that does not match its id sequence or a
// title over 45 characters or a different title length than its `chars` column; the form counts are not
// title 1 / figure 5 / table 14; a figure page that is not pending references a figure that is not on disk
// (pdf, png, svg, _hires png, companion md); a table page has no section-2 table or its column count does not
// match the layout; a glyph cell of P05-P07 differs from research/matrix_final.json (verdict glyph + flags), or a glyph, flag or
// count copied onto P15 or P16 (NDTwin cells, the nearest-alternative cells, the 'on all four' and '(3 ?)' counts) does not follow
// from the matrix cells of the tasks named in the row; a text column that is not a persona token in a "hurts" column; figures on disk are neither used nor accounted for.
//
// Run:  NODE_PATH=<cowork outputs/node_modules> conda run -n webgui-node node generator/build_deck_1014.js
//
// [Co-developed with claude code -- Adam]
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const HERE = __dirname;
const ROOT = HERE + "/..";
const F = ROOT + "/figures/";
const OUT = process.env.OUT_1014 || (ROOT + "/NDTwin_deck_1014.pptx");
const TEMPLATE = process.env.TEMPLATE_1014 || (ROOT + "/NDTwin-slide-template-1014.md");

const S = require(HERE + "/../../NDTwin slide material 903/generator/deck_style");
const { INK, BODY, MUTED, FAINT, ACCENT, FB } = S;

// ---------------------------------------------------------------- palettes (defined once)
// glyphs of the matrix tables; the glyph shape is the primary encoding, colour the second
const GLYPH = {
  "●": "2F7D4F", // ● built in
  "◐": "B07A00", // ◐ you build it
  "○": "6E6E6E", // ○ no
  "?":      "7B5EA7", // ? docs silent
  "⚠": "9C3B2E", // ⚠ open defect (NDTwin only)
  "◌": "065A82", // ◌ no run on that target
};
// personas, same hex as figures/figstyle_1014.py; textOn = text colour on that fill, ink = darker text variant
const PERSONA = {
  app: { fill: "2F7D4F", textOn: "FFFFFF", ink: "2F7D4F" },
  p4:  { fill: "E3A21A", textOn: "1A1A1A", ink: "8A5E00" },
  ops: { fill: "7B5EA7", textOn: "FFFFFF", ink: "7B5EA7" },
};
const GLYPH_RE = /[●◐○⚠◌]|(?<![A-Za-z0-9])\?(?![A-Za-z0-9])/g;

const pres = new pptxgen();
pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
pres.layout = "WIDE";
S.bind(pres);

// ---------------------------------------------------------------- template, section 1
const md = fs.readFileSync(TEMPLATE, "utf8");
const sec1 = md.split(/^## 1\. /m)[1].split(/^## 2\. /m)[0];
const PAGES = [];
for (const ln of sec1.split("\n")) {
  const m = ln.match(/^\| (\d+) \| (P\d\d) \| (.+?) \| (\d+) \| (title|figure|table)(?: `([\w\-\/]+)`)? \| (.+?) \| (.*) \|$/);
  if (!m) continue;
  PAGES.push({ n: +m[1], id: m[2], title: m[3], chars: +m[4], form: m[5], fig: m[6] || null,
    evidence: m[7], status: m[8], pending: /\bwaits\b/i.test(m[8]) });
}
if (PAGES.length !== 22) throw new Error("template section 1 lists " + PAGES.length + " pages, want 22");
PAGES.forEach((p, i) => {
  if (p.n !== i + 1 || p.id !== "P" + String(i + 1).padStart(2, "0")) throw new Error("page sequence broken at " + p.id);
  if (p.title.length > 45) throw new Error(p.id + " title longer than 45 chars");
  if (p.title.length !== p.chars) throw new Error(p.id + " chars column says " + p.chars + ", title is " + p.title.length);
  if (p.form === "figure" && !p.fig) throw new Error(p.id + " is a figure page without a figure stem");
});
const count = f => PAGES.filter(p => p.form === f).length;
if (count("title") !== 1 || count("figure") !== 6 || count("table") !== 15)
  throw new Error("form counts are title/figure/table " + [count("title"), count("figure"), count("table")] + ", want 1/6/15");

// ---------------------------------------------------------------- template, section 2
const sec2 = md.split(/^## 2\. /m)[1].split(/^## 3\. /m)[0];
const BLOCK = {};
for (const blk of sec2.split(/^### /m).slice(1)) BLOCK[blk.split(/\s/)[0]] = blk.split("\n").slice(1).join("\n").trim();
const NOTES_MODE = process.env.NOTES_MODE || "speaker";   // "speaker" (default): from the speaker-notes line on; "block": whole block (930)
function notesText(id) {
  const b = BLOCK[id];
  if (!b) throw new Error("template section 2 has no block for " + id);
  if (NOTES_MODE === "block") return b;
  const i = b.indexOf("講者備註");
  if (i < 0) throw new Error(id + " has no speaker-notes line");
  return b.slice(i).trim();
}
function notes(s, id) { s.addNotes(notesText(id)); }
function mdTable(id) {
  if (!BLOCK[id]) throw new Error("template section 2 has no block for " + id);
  // the first contiguous table of the block
  const first = [];
  for (const l of BLOCK[id].split("\n")) {
    if (l.startsWith("|")) first.push(l); else if (first.length) break;
  }
  if (first.length < 3 || !/^\|[\s|:\-]+\|$/.test(first[1].trim())) throw new Error(id + " has no section-2 table");
  const cells = first.map(r => r.replace(/^\||\|$/g, "").split("|").map(c => c.trim().replace(/`/g, "")));
  const n = cells[0].length;
  cells.forEach((r, i) => { if (i !== 1 && r.length !== n) throw new Error(id + " table row " + i + " has " + r.length + " cells, header has " + n); });
  return [cells[0]].concat(cells.slice(2));
}


// ---------------------------------------------------------------- matrix cross-check (template rule 11)
// Pages 5-7 are generated from research/matrix_final.json: every glyph cell (verdict glyph + flags, in the
// matrix's own order) must equal the matrix cell, or the build stops.
const MATRIX = JSON.parse(fs.readFileSync(process.env.MATRIX_1014 || (ROOT + "/research/matrix_final.json"), "utf8"));
const COLMAP = {
  "Mininet+Ryu": "Mininet + Ryu (assemble it yourself)", "ONOS+Mininet": "ONOS (+ Mininet)",
  "Containerlab": "Containerlab", "ns-3": "ns-3", "sFlow-RT": "sFlow-RT", "NDTwin": "NDTwin",
  "P4 tutorials VM": "p4lang/tutorials VM", "p4-utils": "p4-utils (ETH Zurich nsg)", "ONOS+Stratum": "ONOS + Stratum",
  "Batfish": "Batfish", "GNS3": "GNS3", "Forward*": "Forward Networks (commercial, public docs only)",
  "CML*": "Cisco Modeling Labs (commercial, public docs only)", "IP Fabric*": "IP Fabric (commercial, public docs only)",
  "RouteNet-Fermi\u2020": "RouteNet-Fermi (academic, paper only)",
  "IRTF NDT draft\u2020": "IRTF NMRG network digital twin architecture draft (academic reference framework)",
};
function checkAgainstMatrix(id, persona, rows) {
  const P = MATRIX.personas[persona];
  const head = rows[0];
  const glyphOf = c => MATRIX.legend[c.verdict] + (c.flags || []).join("");
  for (const r of rows.slice(1)) {
    if (r[0] === "legend") continue;
    const rid = r[0].split(" ")[0];
    if (!P.cells[rid]) throw new Error(id + ": row " + rid + " is not a matrix row of persona " + persona);
    for (let j = 1; j < head.length; j++) {
      const col = COLMAP[head[j]];
      if (!col) throw new Error(id + ": column " + head[j] + " has no matrix column mapping");
      const cell = P.cells[rid][col];
      if (!cell) throw new Error(id + ": matrix has no cell " + rid + " x " + col);
      if (glyphOf(cell) !== r[j])
        throw new Error(id + ": cell " + rid + " x " + head[j] + " is " + r[j] + " in the template but " + glyphOf(cell) +
          " (differs from matrix_final.json)");
    }
  }
  const rowsInM = Object.keys(P.rows), rowsHere = rows.slice(1).filter(r => r[0] !== "legend").map(r => r[0].split(" ")[0]);
  if (JSON.stringify(rowsInM) !== JSON.stringify(rowsHere))
    throw new Error(id + ": task rows " + rowsHere + " differ from the matrix rows " + rowsInM);
  const colsM = P.columns, colsHere = head.slice(1).map(h => COLMAP[h]);
  if (JSON.stringify(colsM) !== JSON.stringify(colsHere))
    throw new Error(id + ": columns differ from the matrix columns of persona " + persona + " (differs from matrix_final.json)");
}
const MATRIX_PAGES = { P05: "app", P06: "p4", P07: "ops" };

// ---------------------------------------------------------------- the cells copied onto P15 and P16
// P15 and P16 repeat P05-P07 cells (and counts of them) in running text; each claim is re-derived from the matrix.
const WORDN = { one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8 };
const PERS = { A: "app", P: "p4", O: "ops" };
function taskIds(txt) {
  const ids = [];
  for (const part of txt.split(",").map(x => x.trim())) {
    const r = part.match(/^([APO])(\d)-([APO])?(\d)$/);
    if (r) { for (let k = +r[2]; k <= +r[4]; k++) ids.push(r[1] + k); continue; }
    if (/^[APO]\d$/.test(part)) ids.push(part);
  }
  return ids;
}
function mcell(id, col) {
  const P = MATRIX.personas[PERS[id[0]]];
  const c = P && P.cells[id] && P.cells[id][col];
  if (!c) throw new Error("matrix has no cell " + id + " x " + col);
  return c;
}
const gl = c => MATRIX.legend[c.verdict];
const gf = c => MATRIX.legend[c.verdict] + (c.flags || []).join("");
function checkCopied(id, rows) {
  const head = rows[0];
  const ndtCol = head.findIndex(h => h.startsWith("NDTwin"));
  const taskCol = head.indexOf("tasks");
  if (ndtCol < 0 || taskCol < 0) throw new Error(id + ": no NDTwin or tasks column");
  const fail = (r, m) => { throw new Error(id + " row '" + r[0] + "': " + m + " (differs from matrix_final.json)"); };
  for (const r of rows.slice(1)) {
    const ids = taskIds(r[taskCol]);
    const cell = r[ndtCol];
    // NDTwin cell
    const all = cell.match(/^[\u25CF\u25D0\u25CB] on all (\w+) \(\u26A0 (\w+), \u25CC (\w+)\)/);
    if (all) {
      if (ids.length !== WORDN[all[1]]) fail(r, "'all " + all[1] + "' but the task list has " + ids.length);
      const cs = ids.map(t => mcell(t, "NDTwin"));
      if (cs.some(c => gl(c) !== cell[0])) fail(r, "not every task is " + cell[0]);
      const w = cs.filter(c => (c.flags || []).includes("\u26A0")).length, n = cs.filter(c => (c.flags || []).includes("\u25CC")).length;
      if (w !== WORDN[all[2]] || n !== WORDN[all[3]]) fail(r, "flag counts are \u26A0 " + w + ", \u25CC " + n);
    } else {
      const toks = cell.match(/[\u25CF\u25D0\u25CB][\u26A0\u25CC]*/g) || [];
      if (toks.length) {
        if (toks.length !== ids.length) fail(r, toks.length + " NDTwin glyph groups for " + ids.length + " tasks");
        toks.forEach((t, k) => { if (gf(mcell(ids[k], "NDTwin")) !== t) fail(r, "NDTwin " + ids[k] + " is " + t + " here but " + gf(mcell(ids[k], "NDTwin"))); });
      }
    }
    // the alternative column of P15
    if (id === "P15") {
      const alt = r[2];
      if (/^no other \u25CF on P07 \((\d) \?\)$/.test(alt)) {
        const n = +alt.match(/\((\d)/)[1], t = ids[0];
        const cols = MATRIX.personas.ops.columns.filter(c => c !== "NDTwin");
        if (cols.some(c => mcell(t, c).verdict === "builtin")) fail(r, "another tool has \u25CF on " + t);
        const q = cols.filter(c => mcell(t, c).verdict === "unknown").length;
        if (q !== n) fail(r, "the number of ? on " + t + " is " + q + ", not " + n);
        continue;
      }
      const m = alt.match(/^(.+?): (.+)$/);
      if (!m) fail(r, "unparsed alternative '" + alt + "'");
      const tools = m[1].split(", ").map(x => { if (!COLMAP[x]) throw new Error(id + ": unknown tool " + x); return COLMAP[x]; });
      const claim = m[2].replace(/ \(.*\)$/, "");
      const pairs = [...claim.matchAll(/([APO]\d) ([\u25CF\u25D0\u25CB?])/g)];
      let on;
      if (pairs.length) {
        for (const [, t, g] of pairs) for (const col of tools) if (gl(mcell(t, col)) !== g) fail(r, col + " " + t + " is " + gl(mcell(t, col)) + ", not " + g);
      } else if ((on = claim.match(/^\u25CF on (\w+)$/))) {
        for (const col of tools) {
          const n = ids.filter(t => mcell(t, col).verdict === "builtin").length;
          if (n !== WORDN[on[1]]) fail(r, col + " has " + n + " \u25CF on " + ids + ", not " + on[1]);
        }
      } else if (/^[\u25CF\u25D0\u25CB?]$/.test(claim)) {
        for (const col of tools) for (const t of ids) if (gl(mcell(t, col)) !== claim) fail(r, col + " " + t + " is " + gl(mcell(t, col)) + ", not " + claim);
      } else fail(r, "unparsed claim '" + claim + "'");
    }
  }
}
const COPIED_PAGES = { P15: 1, P16: 1 };

// ---------------------------------------------------------------- helpers
const USED = [];
function pngAspect(p) {
  const b = fs.readFileSync(p);
  return b.readUInt32BE(16) / b.readUInt32BE(20);
}
function figPage(pg) {
  const s = S.newSlide();
  const TOP = 0.28, BOT = 7.00, availH = BOT - TOP, availW = 12.90;
  const stem = pg.fig.split("/")[1], dir = pg.fig.split("/")[0];
  for (const f of [dir + "/" + stem + ".pdf", dir + "/" + stem + ".png", dir + "/" + stem + ".svg",
    dir + "/_hires/" + stem + ".png"])
    if (!fs.existsSync(F + f)) throw new Error(pg.id + ": missing figure file " + f);
  if (!fs.existsSync(F + dir + "/" + stem + ".md") && !fs.existsSync(F + dir + "/" + stem + ".txt"))
    throw new Error(pg.id + ": figure " + stem + " has no companion .md/.txt");
  const p = F + dir + "/_hires/" + stem + ".png";
  const ar = pngAspect(p);
  let w = availW, h = w / ar;
  if (h > availH) { h = availH; w = h * ar; }
  s.addImage({ path: p, x: (13.333 - w) / 2, y: TOP + (availH - h) / 2, w, h });
  USED.push(pg.fig);
  notes(s, pg.id);
  S.pageNum(s);
}

const X = 0.62, W = 12.10;
function title(s, text) {
  s.addText(text, { x: X, y: 0.42, w: W, h: 0.66, fontFace: FB, fontSize: 30, bold: true, color: INK, margin: 0 });
}
// text -> runs: glyphs coloured from the palette (one place), the rest in the cell colour
function runs(text, base) {
  const out = [];
  let last = 0, m;
  GLYPH_RE.lastIndex = 0;
  while ((m = GLYPH_RE.exec(text))) {
    if (m.index > last) out.push({ text: text.slice(last, m.index), options: Object.assign({}, base) });
    if (!GLYPH[m[0]]) throw new Error("glyph outside the palette: " + m[0]);
    out.push({ text: m[0], options: Object.assign({}, base, { color: GLYPH[m[0]], bold: true }) });
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push({ text: text.slice(last), options: Object.assign({}, base) });
  return out.length ? out : text;
}
const GLYPH_ONLY = /^[●◐○⚠◌?]+$/;
const PERSONA_TOKEN = { "P4": "p4", "app": "app", "ops": "ops" };

// cfg: { widths, fs, hfs, rh, hh, y, hdrFill, hdrText, center (matrix: centre header and glyph cells),
//        persona: [{row0:i, fill}] first column fills, hurtsCol: index of a "P4 · app · ops" column, margin }
function tableOf(s, rows, cfg) {
  const ncol = rows[0].length;
  if (cfg.widths.length !== ncol) throw new Error("layout has " + cfg.widths.length + " columns, table has " + ncol);
  const sumW = cfg.widths.reduce((a, b) => a + b, 0);
  if (Math.abs(sumW - W) > 0.011) throw new Error("column widths sum to " + sumW + ", want " + W);
  const hdrFill = cfg.hdrFill || ACCENT, hdrText = cfg.hdrText || "FFFFFF";
  const hdr = rows[0].map((h, j) => ({ text: h, options: { bold: true, color: hdrText, fill: { color: hdrFill },
    fontSize: cfg.hfs, align: cfg.center && j > 0 ? "center" : "left" } }));
  const body = rows.slice(1).map((r, i) => {
    const isLegend = r[0] === "legend";
    const line = [];
    for (let j = 0; j < r.length; j++) {
      const cell = r[j];
      const base = { fontSize: cfg.fs, color: j === 0 ? INK : BODY, bold: j === 0 };
      const opt = { fill: { color: i % 2 ? "FFFFFF" : "F4F7F9" }, valign: "middle", fontSize: cfg.fs };
      if (isLegend) opt.fill = { color: "E9ECEE" };
      if (cfg.center && j > 0 && GLYPH_ONLY.test(cell)) opt.align = "center";
      if (cfg.persona && j === 0 && cfg.persona[i]) {
        const P = PERSONA[cfg.persona[i]];
        opt.fill = { color: P.fill };
        base.color = P.textOn;
      }
      let content;
      if (cfg.hurtsCol === j) {
        content = [];
        cell.split(" · ").forEach((tok, k, a) => {
          const key = PERSONA_TOKEN[tok];
          if (!key) throw new Error("unknown persona token in hurts cell: " + tok);
          content.push({ text: tok, options: { fontSize: cfg.fs, bold: true, color: PERSONA[key].ink } });
          if (k < a.length - 1) content.push({ text: " · ", options: { fontSize: cfg.fs, color: BODY } });
        });
      } else if (cell === "") {
        content = "";
      } else {
        content = runs(cell, base);
        if (typeof content === "string") opt.color = base.color, opt.bold = base.bold;
      }
      // a text cell followed only by empty cells absorbs them (legend rows)
      let span = 1;
      if (isLegend && cell !== "") {
        while (j + span < r.length && r[j + span] === "") span++;
      }
      line.push({ text: content, options: Object.assign(opt, span > 1 ? { colspan: span } : {}) });
      j += span - 1;
    }
    return line;
  });
  s.addTable([hdr, ...body], {
    x: X, y: cfg.y, w: W, colW: cfg.widths,
    rowH: [cfg.hh || 0.42, ...rows.slice(1).map(() => cfg.rh || 0.4)],
    border: { type: "solid", color: "DDE4E9", pt: 1 },
    fontFace: FB, valign: "middle", margin: cfg.margin || [0.06, 0.10, 0.06, 0.10],
  });
}
function tablePage(pg, cfg) {
  const s = S.newSlide();
  title(s, pg.title);
  const rows = mdTable(pg.id);
  if (MATRIX_PAGES[pg.id]) checkAgainstMatrix(pg.id, MATRIX_PAGES[pg.id], rows);
  if (COPIED_PAGES[pg.id]) checkCopied(pg.id, rows);
  tableOf(s, rows, cfg);
  notes(s, pg.id);
  S.pageNum(s);
}
function pendingPage(pg) {
  const s = S.newSlide();
  title(s, pg.title);
  s.addTable([[{ text: "pending: hands-on results", options: { fill: { color: "E3E6E8" }, color: "4F4F4F",
    fontSize: 24, align: "center", valign: "middle", bold: true } }]], {
    x: X, y: 1.55, w: W, colW: [W], rowH: [3.2], border: { type: "solid", color: "C9CDD0", pt: 1 },
    fontFace: FB, valign: "middle" });
  notes(s, pg.id);
  S.pageNum(s);
}
function titlePage(pg) {
  const s = S.newSlide();
  s.addText(pg.title, { x: X, y: 2.9, w: W, h: 1.1, fontFace: FB, fontSize: 48, bold: true, color: INK, margin: 0 });
  s.addShape("line", { x: X, y: 4.2, w: 1.1, h: 0.01, line: { color: ACCENT, width: 2.5 } });
  s.addText("Adam", { x: X, y: 6.3, w: 6, h: 0.4, fontFace: FB, fontSize: 18, color: MUTED, margin: 0 });
  notes(s, pg.id);
}

// ---------------------------------------------------------------- layout per table page (widths sum to 12.10)
const LAYOUT = {
  P03: { widths: [2.4, 3.6, 4.9, 1.2], fs: 18, hfs: 18, rh: 0.8, hh: 0.55, y: 1.4,
         persona: ["app", "p4", "ops"] },
  P05: { widths: [2.8, 1.55, 1.55, 1.55, 1.55, 1.55, 1.55], fs: 14, hfs: 13, rh: 0.46, hh: 0.5, y: 1.2,
         center: true, hdrFill: PERSONA.app.fill, hdrText: PERSONA.app.textOn, margin: [0.05, 0.08, 0.05, 0.08] },
  P06: { widths: [3.7, 2.1, 2.1, 2.1, 2.1], fs: 15, hfs: 14, rh: 0.5, hh: 0.5, y: 1.25,
         center: true, hdrFill: PERSONA.p4.fill, hdrText: PERSONA.p4.textOn },
  P07: { widths: [2.7, 1.175, 1.175, 1.175, 1.175, 1.175, 1.175, 1.175, 1.175], fs: 13, hfs: 12, rh: 0.44,
         hh: 0.55, y: 1.2, center: true, hdrFill: PERSONA.ops.fill, hdrText: PERSONA.ops.textOn,
         margin: [0.05, 0.06, 0.05, 0.06] },
  P08: { widths: [1.4, 1.3, 1.7, 2.15, 2.2, 1.75, 1.6], fs: 12, hfs: 12, rh: 0.3, hh: 0.34, y: 1.12,
         margin: [0.03, 0.06, 0.03, 0.06] },
  P09: { widths: [1.7, 1.3, 2.0, 1.9, 1.6, 1.9, 1.7], fs: 16, hfs: 15, rh: 0.5, hh: 0.5, y: 1.35 },
  P11: { widths: [2.9, 5.3, 3.9], fs: 13, hfs: 14, rh: 0.36, hh: 0.42, y: 1.15,
         margin: [0.04, 0.08, 0.04, 0.08] },
  P12: { widths: [3.9, 1.6, 1.6, 5.0], fs: 17, hfs: 16, rh: 0.62, hh: 0.5, y: 1.35 },
  P14: { widths: [4.0, 3.7, 4.4], fs: 16, hfs: 16, rh: 0.52, hh: 0.48, y: 1.3 },
  P15: { widths: [3.9, 2.4, 4.6, 1.2], fs: 17, hfs: 16, rh: 0.6, hh: 0.5, y: 1.3 },
  P16: { widths: [3.4, 3.4, 4.1, 1.2], fs: 15, hfs: 15, rh: 0.4, hh: 0.45, y: 1.2 },
  P17: { widths: [4.4, 7.7], fs: 18, hfs: 16, rh: 0.66, hh: 0.5, y: 1.4,
         margin: [0.05, 0.10, 0.05, 0.10] },
  P19: { widths: [0.5, 2.6, 1.3, 3.0, 3.4, 1.3], fs: 17, hfs: 15, rh: 0.5, hh: 0.45, y: 1.2, hurtsCol: 2,
         margin: [0.05, 0.08, 0.05, 0.08] },
  P20: { widths: [0.5, 2.6, 1.3, 3.0, 3.4, 1.3], fs: 17, hfs: 15, rh: 0.5, hh: 0.45, y: 1.2, hurtsCol: 2,
         margin: [0.05, 0.08, 0.05, 0.08] },
  P21: { widths: [0.5, 2.6, 1.3, 3.0, 3.4, 1.3], fs: 16, hfs: 15, rh: 0.46, hh: 0.45, y: 1.15, hurtsCol: 2,
         margin: [0.05, 0.08, 0.05, 0.08] },
};
// optional per-page overrides from a layout file written by the tuning step
if (process.env.LAYOUT_JSON) Object.assign(LAYOUT, JSON.parse(fs.readFileSync(process.env.LAYOUT_JSON, "utf8")));

// ---------------------------------------------------------------- build
for (const pg of PAGES) {
  if (pg.form === "title") titlePage(pg);
  else if (pg.pending) pendingPage(pg);
  else if (pg.form === "figure") figPage(pg);
  else {
    if (!LAYOUT[pg.id]) throw new Error("no layout for table page " + pg.id);
    tablePage(pg, LAYOUT[pg.id]);
  }
}

// ---------------------------------------------------------------- checks
const ARCHIVE = [];
const onDisk = fs.readdirSync(F, { withFileTypes: true }).filter(d => d.isDirectory())
  .flatMap(d => fs.readdirSync(F + d.name).filter(f => f.endsWith(".png"))
    .map(f => d.name + "/" + f.replace(/\.png$/, "")));
const unaccounted = onDisk.filter(p => !USED.includes(p) && !ARCHIVE.includes(p));
if (unaccounted.length) throw new Error("figures neither used nor archived: " + unaccounted);
if (S.currentPage() !== 22) throw new Error("expected 22 pages, got " + S.currentPage());
const pend = PAGES.filter(p => p.pending).map(p => p.id);
console.log(`figures: ${onDisk.length} on disk / ${USED.length} used / ${ARCHIVE.length} archive-only / 0 unaccounted`);
console.log(`pending pages (grey cell): ${pend.join(", ")}; notes mode: ${NOTES_MODE}`);

// pptxgenjs writes an <a:pPr> before EVERY run of a multi-run paragraph; the schema allows one, first.
// Table cells with coloured glyphs have several runs, so strip the repeats (and nothing else) after writing.
const JSZip = require("jszip");
pres.write({ outputType: "nodebuffer" })
  .then(async buf => {
    const zip = await JSZip.loadAsync(buf);
    let fixed = 0;
    for (const name of Object.keys(zip.files)) {
      if (!/^ppt\/slides\/slide\d+\.xml$/.test(name)) continue;
      const x = await zip.file(name).async("string");
      const y = x.replace(/<\/a:r><a:pPr\b[^>]*?(?:\/>|>[\s\S]*?<\/a:pPr>)/g, () => { fixed++; return "</a:r>"; });
      if (y !== x) zip.file(name, y);
    }
    fs.writeFileSync(OUT, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
    console.log("repeated <a:pPr> removed: " + fixed);
    console.log("done \u2014 " + S.currentPage() + " pages \u2192 " + OUT);
  })
  .catch(e => { console.error(e); process.exit(1); });
