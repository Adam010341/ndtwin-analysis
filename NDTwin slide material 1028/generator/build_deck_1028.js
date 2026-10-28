// NDTwin report deck, 2026-10-28, "P4 support since 10/14". Nine pages. Adapted from build_deck_1014.js.
//
// Built from NDTwin-slide-template-1028.md: section 1 gives the page order, title and form of every page;
// section 2 gives the tables (cell for cell) and the speaker notes (verbatim, from the line "講者備註" to the end
// of the page's block; the "Sources" lines above it stay in the template). Nothing about a page is typed in this
// file except layout (column widths, font sizes).
//
// Rules carried over from 1014: one figure OR one table per page, nothing else; figure pages carry no page
// title (the figure's own canvas title is the slide title); table pages carry the section-1 title and the
// table; page number only. Title page: the title and "Adam".
//
// Stops (throws) if: the page count is not 9; a section-1 row breaks the id sequence, has a title over 45
// characters or a `chars` column that differs from the title's length; the form counts are not title 1 /
// figure 3 / table 5; a figure page references a figure that is not on disk (pdf, png, svg, _hires png,
// companion md) or whose canvas title (in the companion .md heading) differs from the section-1 title; a table
// page has no section-2 table or its column count does not match the layout; a table cell or a note contains a
// commit-like hex token or a PR reference (the full scan is redcheck_1028.py); figures on disk are not used.
//
// Run:  NODE_PATH=<cowork outputs/node_modules> conda run -n webgui-node node generator/build_deck_1028.js
//
// [Co-developed with claude code -- Adam]
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const HERE = __dirname;
const ROOT = HERE + "/..";
const F = ROOT + "/figures/";
const OUT = process.env.OUT_1028 || (ROOT + "/NDTwin_deck_1028.pptx");
const TEMPLATE = process.env.TEMPLATE_1028 || (ROOT + "/NDTwin-slide-template-1028.md");
const NPAGES = 9, FORMS = { title: 1, figure: 3, table: 5 };

const S = require(HERE + "/../../NDTwin slide material 903/generator/deck_style");
const { INK, BODY, ACCENT, MUTED, FB } = S;

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
  PAGES.push({ n: +m[1], id: m[2], title: m[3], chars: +m[4], form: m[5], fig: m[6] || null, evidence: m[7] });
}
if (PAGES.length !== NPAGES) throw new Error("template section 1 lists " + PAGES.length + " pages, want " + NPAGES);
PAGES.forEach((p, i) => {
  if (p.n !== i + 1 || p.id !== "P" + String(i + 1).padStart(2, "0")) throw new Error("page sequence broken at " + p.id);
  if (p.title.length > 45) throw new Error(p.id + " title longer than 45 chars");
  if (p.title.length !== p.chars) throw new Error(p.id + " chars column says " + p.chars + ", title is " + p.title.length);
  if (p.form === "figure" && !p.fig) throw new Error(p.id + " is a figure page without a figure stem");
});
const count = f => PAGES.filter(p => p.form === f).length;
for (const f of Object.keys(FORMS))
  if (count(f) !== FORMS[f])
    throw new Error("form counts are title/figure/table " + [count("title"), count("figure"), count("table")] +
      ", want " + [FORMS.title, FORMS.figure, FORMS.table]);

// ---------------------------------------------------------------- template, section 2
const sec2 = md.split(/^## 2\. /m)[1].split(/^## 3\. /m)[0];
const BLOCK = {};
for (const blk of sec2.split(/^### /m).slice(1)) BLOCK[blk.split(/\s/)[0]] = blk.split("\n").slice(1).join("\n").trim();
// a commit-like token (7+ hex chars with a digit and a letter) or a PR reference must never reach the pptx
const HEX = /\b(?=[0-9a-f]*[0-9])(?=[0-9a-f]*[a-f])[0-9a-f]{7,64}\b/i;
const PRREF = /\bPR\s*#?\s*\d+|#4\d\b|pull request/i;
function guard(id, what, text) {
  const h = text.match(HEX), p = text.match(PRREF);
  if (h) throw new Error(id + " " + what + " carries a commit-like token '" + h[0] + "'");
  if (p) throw new Error(id + " " + what + " carries a PR reference '" + p[0] + "'");
}
function notesText(id) {
  const b = BLOCK[id];
  if (!b) throw new Error("template section 2 has no block for " + id);
  const i = b.indexOf("講者備註");
  if (i < 0) throw new Error(id + " has no speaker-notes line");
  const t = b.slice(i).trim();
  guard(id, "speaker notes", t);
  return t;
}
function notes(s, id) { s.addNotes(notesText(id)); }
function mdTable(id) {
  if (!BLOCK[id]) throw new Error("template section 2 has no block for " + id);
  const first = [];
  for (const l of BLOCK[id].split("\n")) {
    if (l.startsWith("|")) first.push(l); else if (first.length) break;
  }
  if (first.length < 3 || !/^\|[\s|:\-]+\|$/.test(first[1].trim())) throw new Error(id + " has no section-2 table");
  const cells = first.map(r => r.replace(/^\||\|$/g, "").split("|").map(c => c.trim().replace(/`/g, "")));
  const n = cells[0].length;
  cells.forEach((r, i) => { if (i !== 1 && r.length !== n) throw new Error(id + " table row " + i + " has " + r.length + " cells, header has " + n); });
  cells.forEach(r => r.forEach(c => guard(id, "table cell", c)));
  return [cells[0]].concat(cells.slice(2));
}

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
    dir + "/_hires/" + stem + ".png", dir + "/" + stem + ".md"])
    if (!fs.existsSync(F + f)) throw new Error(pg.id + ": missing figure file " + f);
  const head = fs.readFileSync(F + dir + "/" + stem + ".md", "utf8").split("\n")[0];
  if (head !== "# " + stem + " -- " + pg.title)
    throw new Error(pg.id + ": figure " + stem + " canvas title is '" + head.replace(/^# \S+ -- /, "") + "', section 1 says '" + pg.title + "'");
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
// cfg: { widths, fs, hfs, rh, hh, y, margin }
function tableOf(s, rows, cfg) {
  const ncol = rows[0].length;
  if (cfg.widths.length !== ncol) throw new Error("layout has " + cfg.widths.length + " columns, table has " + ncol);
  const sumW = cfg.widths.reduce((a, b) => a + b, 0);
  if (Math.abs(sumW - W) > 0.011) throw new Error("column widths sum to " + sumW + ", want " + W);
  const hdr = rows[0].map(h => ({ text: h, options: { bold: true, color: "FFFFFF", fill: { color: ACCENT },
    fontSize: cfg.hfs, align: "left" } }));
  const body = rows.slice(1).map((r, i) => r.map((cell, j) => ({ text: cell, options: {
    fill: { color: i % 2 ? "FFFFFF" : "F4F7F9" }, valign: "middle", fontSize: cfg.fs,
    color: j === 0 ? INK : BODY, bold: j === 0 } })));
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
  tableOf(s, mdTable(pg.id), cfg);
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
  P02: { widths: [2.7, 6.6, 2.8], fs: 18, hfs: 17, rh: 0.80, hh: 0.52, y: 1.40 },
  P03: { widths: [3.6, 4.0, 4.5], fs: 20, hfs: 18, rh: 0.78, hh: 0.56, y: 1.45 },
  P06: { widths: [3.9, 6.0, 2.2], fs: 18, hfs: 17, rh: 0.78, hh: 0.52, y: 1.40 },
  P07: { widths: [4.6, 4.3, 3.2], fs: 18, hfs: 17, rh: 1.05, hh: 0.52, y: 1.45 },
  P08: { widths: [3.7, 4.6, 3.8], fs: 17, hfs: 17, rh: 0.84, hh: 0.52, y: 1.40 },
};
if (process.env.LAYOUT_JSON) Object.assign(LAYOUT, JSON.parse(fs.readFileSync(process.env.LAYOUT_JSON, "utf8")));

// ---------------------------------------------------------------- build
for (const pg of PAGES) {
  guard(pg.id, "title", pg.title);
  if (pg.form === "title") titlePage(pg);
  else if (pg.form === "figure") figPage(pg);
  else {
    if (!LAYOUT[pg.id]) throw new Error("no layout for table page " + pg.id);
    tablePage(pg, LAYOUT[pg.id]);
  }
}

// ---------------------------------------------------------------- checks
const onDisk = fs.readdirSync(F, { withFileTypes: true }).filter(d => d.isDirectory())
  .flatMap(d => fs.readdirSync(F + d.name).filter(f => f.endsWith(".png"))
    .map(f => d.name + "/" + f.replace(/\.png$/, "")));
const unaccounted = onDisk.filter(p => !USED.includes(p));
if (unaccounted.length) throw new Error("figures on disk but not used: " + unaccounted);
if (S.currentPage() !== NPAGES) throw new Error("expected " + NPAGES + " pages, got " + S.currentPage());
console.log(`figures: ${onDisk.length} on disk / ${USED.length} used / 0 unaccounted`);

// pptxgenjs writes an <a:pPr> before EVERY run of a multi-run paragraph; the schema allows one, first.
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
    console.log("done — " + S.currentPage() + " pages → " + OUT);
  })
  .catch(e => { console.error(e); process.exit(1); });
