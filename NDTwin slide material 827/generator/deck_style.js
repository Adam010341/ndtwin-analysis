// ---------------------------------------------------------------------------
// deck_style.js — the house style, with no content in it.
//
// Everything here was extracted from the 2026-08-20 deck's generator after it
// had been through four rounds of render-and-fix, so the defaults are the ones
// that actually survived projection. Require it, or paste it in; either way do
// not re-derive the palette or the margins by eye.
//
//   const S = require("./deck_style");
//   const pres = new pptxgen();
//   pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
//   pres.layout = "WIDE";
//   S.bind(pres);                       // wires newSlide()/pageNum() to this deck
//   const s = S.newSlide();
//   S.pageTitle(s, "Title", "Subtitle");
//
// Rules that are not expressible as code live in the template's section E.
// ---------------------------------------------------------------------------

// ============ minimal palette: one accent, everything else ink/grey ============
const INK      = "1A1A1A";   // titles
const WARNC    = "9C3B2E";   // used only where a measured value is the bad one
const BODY     = "2E2E2E";   // body text
const MUTED    = "4F4F4F";   // secondary text — still clearly legible
const FAINT    = "6E6E6E";   // captions, column labels
const RULE     = "D0D0D0";   // hairlines
const ACCENT   = "065A82";   // the single accent
const ACCENT_BG= "EEF3F6";   // very light accent wash
const PANEL    = "F7F8F9";   // neutral panel
const WARN_BG  = "FBF2F0";   // very light warning wash

const FH = "Cambria";        // page titles, big numbers
const FB = "Calibri";        // body
const FC = "Courier New";    // code, identifiers, endpoints
const AF = "Arial";          // diagrams only
const LINE = "000000";

const M  = 0.85;             // left margin
const CW = 13.333 - M * 2;   // content width

// Page numbering is automatic: newSlide() increments, pageNum() reads.
// Hard-coding page numbers is how the 2026-08-19 renumbering went wrong.
let pres = null;
let PAGE = 0;
function bind(p) { pres = p; PAGE = 0; }
function newSlide() { PAGE++; const s = pres.addSlide(); s.background = { color: "FFFFFF" }; return s; }
function currentPage() { return PAGE; }

// One figure, one page. The figures carry their own title, so the page adds
// nothing but the section tab and the page number. `ar` is the raw pixel ratio.
function figurePage(figDir, file, ar, tab) {
  const s = newSlide();
  if (tab) sectionTab(s, tab);
  const wide = ar > 2.5;                       // 16:9 starves a very wide figure
  const maxW = wide ? 12.53 : 12.13, maxH = 5.62;
  const w = Math.min(maxW, maxH * ar), h = w / ar;
  s.addImage({ path: figDir + file, x: (13.333 - w) / 2,
               y: 0.98 + (maxH - h) * (wide ? 0.34 : 0.5), w, h });
  pageNum(s);
  return s;
}

// A section divider. Same layout as the title page, only the words change.
function sectionCover(n, name, oneLine) {
  const s = newSlide();
  s.addText("SECTION " + n, { x: M, y: 2.16, w: 11.0, h: 0.42,
    fontFace: FB, fontSize: 16, color: ACCENT, margin: 0, charSpacing: 1.2 });
  s.addText(name, { x: M, y: 2.72, w: 11.0, h: 0.95,
    fontFace: FH, fontSize: 44, bold: true, color: INK, margin: 0 });
  s.addText(oneLine, { x: M, y: 3.72, w: 11.0, h: 0.62,
    fontFace: FB, fontSize: 20, color: MUTED, margin: 0, lineSpacingMultiple: 1.15 });
  s.addShape("line", { x: M, y: 4.66, w: 1.1, h: 0.01, line: { color: ACCENT, width: 2 } });
  pageNum(s);
  return s;
}


// ============================================================
// page furniture — title, number, section tab
// ============================================================

function pageTitle(s, title, sub) {
  s.addText(title, {
    x: M, y: 0.62, w: CW, h: 0.68,
    fontFace: FH, fontSize: 30, bold: true, color: INK, margin: 0,
  });
  if (sub) {
    s.addText(sub, {
      x: M, y: 1.32, w: CW, h: 0.38,
      fontFace: FB, fontSize: 14, color: MUTED, margin: 0,
    });
  }
  s.addShape("line", {
    x: M, y: sub ? 1.86 : 1.46, w: CW, h: 0.01,
    line: { color: RULE, width: 1 },
  });
}

function pageNum(s) {
  s.addText(String(PAGE), {
    x: 12.0, y: 6.92, w: 0.48, h: 0.3, align: "right",
    fontFace: FB, fontSize: 10, color: FAINT, margin: 0,
  });
}

function sectionTab(s, label) {
  s.addText(label, {
    x: M, y: 0.28, w: 6.0, h: 0.26,
    fontFace: FB, fontSize: 10.5, bold: true, color: ACCENT, margin: 0, charSpacing: 1.0,
  });
}

// ============================================================
// the numbered list that most content pages are built from
// ============================================================

function listItem(s, x, y, w, n, head, body, bodyW) {
  s.addText(n, {
    x, y: y - 0.02, w: 0.32, h: 0.3,
    fontFace: FB, fontSize: 13, bold: true, color: ACCENT, margin: 0,
  });
  s.addText(head, {
    x: x + 0.36, y: y - 0.03, w: (bodyW || w) - 0.36, h: 0.32,
    fontFace: FB, fontSize: 15.5, bold: true, color: INK, margin: 0,
  });
  // valign top, not the renderer's default: a two-line body centred inside a
  // 0.9" box sinks far enough to touch the next item's heading. Measured.
  s.addText(body, {
    x: x + 0.36, y: y + 0.34, w: (bodyW || w) - 0.36, h: 0.86, valign: "top",
    fontFace: FB, fontSize: 12.5, color: BODY, margin: 0, lineSpacingMultiple: 1.24,
  });
}

function marginNote(s, x, y, w, h, title, body) {
  s.addShape("rect", { x, y, w: 0.03, h, fill: { color: ACCENT }, line: { type: "none" } });
  let ty = y - 0.04;
  if (title) {
    s.addText(title, {
      x: x + 0.22, y: ty, w: w - 0.22, h: 0.26,
      fontFace: FB, fontSize: 11.5, bold: true, color: ACCENT, margin: 0,
    });
    ty += 0.30;
  }
  s.addText(body, {
    x: x + 0.22, y: ty, w: w - 0.22, h: h - (title ? 0.30 : 0),
    fontFace: FB, fontSize: 11, color: BODY, margin: 0, lineSpacingMultiple: 1.2,
  });
}

function defect(s, x, y, w, n, head, sym, why, fix) {
  s.addText(n, {
    x, y: y - 0.02, w: 0.32, h: 0.3,
    fontFace: FB, fontSize: 13, bold: true, color: ACCENT, margin: 0,
  });
  s.addText(head, {
    x: x + 0.36, y: y - 0.03, w: w - 0.36, h: 0.32,
    fontFace: FB, fontSize: 14.5, bold: true, color: INK, margin: 0,
  });
  const parts = [];
  if (sym) parts.push(
    { text: "Symptom　", options: { bold: true, color: MUTED, fontSize: 10 } },
    { text: sym, options: { color: BODY, fontSize: 11.5, breakLine: !!(why || fix), paraSpaceAfter: 4 } });
  if (why) parts.push(
    { text: "Root cause　", options: { bold: true, color: MUTED, fontSize: 10 } },
    { text: why, options: { color: BODY, fontSize: 11.5, breakLine: !!fix, paraSpaceAfter: 4 } });
  if (fix) parts.push(
    { text: "Fix　", options: { bold: true, color: MUTED, fontSize: 10 } },
    { text: fix, options: { color: BODY, fontSize: 11.5 } });
  s.addText(parts, {
    x: x + 0.36, y: y + 0.32, w: w - 0.36, h: 1.05,
    fontFace: FB, margin: 0, valign: "top", lineSpacingMultiple: 1.16,
  });
}

function kvRows(s, x, y, w, rows, opt) {
  opt = opt || {};
  const rh = opt.rh || 0.34, kw = opt.kw || 2.6;
  rows.forEach((r, i) => {
    s.addText(r[0], {
      x, y: y + i * rh, w: kw, h: rh, valign: "middle",
      fontFace: opt.mono ? FC : FB, fontSize: opt.ks || 11.5,
      bold: opt.kb !== false, color: opt.kc || INK, margin: 0,
    });
    s.addText(r[1], {
      x: x + kw, y: y + i * rh, w: w - kw - (opt.tw || 0), h: rh, valign: "middle",
      fontFace: FB, fontSize: opt.vs || 11.5, color: BODY, margin: 0,
    });
    if (r[2] !== undefined) {
      s.addText(r[2], {
        x: x + w - (opt.tw || 0.9), y: y + i * rh, w: opt.tw || 0.9, h: rh,
        align: "right", valign: "middle",
        fontFace: FB, fontSize: 11, color: FAINT, margin: 0,
      });
    }
    s.addShape("line", { x, y: y + (i + 1) * rh - 0.02, w, h: 0.01,
      line: { color: "EFEFEF", width: 1 } });
  });
  return y + rows.length * rh;
}

function pending(s, x, y, w, label) {
  s.addShape("rect", { x, y, w, h: 0.34, fill: { color: "F7F8F9" }, line: { color: RULE, width: 1 } });
  s.addText("TO ADD   " + label, {
    x: x + 0.16, y, w: w - 0.32, h: 0.34, valign: "middle",
    fontFace: FB, fontSize: 10.5, color: MUTED, margin: 0, charSpacing: 0.4,
  });
}

// ============================================================
// architecture-diagram primitives (Arial, white boxes, 1 pt black)
// ============================================================

function aBox(s, x, y, w, h, text, o) {
  o = o || {};
  s.addShape("rect", {
    x, y, w, h,
    fill: { color: o.fill || "FFFFFF" },
    line: { color: o.line || LINE, width: o.lw || 1 },
  });
  if (text) {
    s.addText(text, {
      x: x + 0.04, y, w: w - 0.08, h, align: "center", valign: "middle",
      fontFace: AF, fontSize: o.fs || 11, bold: !!o.bold,
      color: o.tc || "000000", margin: 0, lineSpacingMultiple: 0.92,
    });
  }
}

function aText(s, x, y, w, h, text, o) {
  o = o || {};
  s.addText(text, {
    x, y, w, h, align: o.align || "left", valign: o.valign || "middle",
    fontFace: AF, fontSize: o.fs || 12, bold: !!o.bold,
    color: o.tc || "000000", margin: 0, lineSpacingMultiple: 0.95,
  });
}

function aArrow(s, x, y, w, h, dir, o) {
  o = o || {};
  const opt = {
    x, y, w: w || 0.008, h: h || 0.008,
    line: { color: o.color || "000000", width: o.lw || 1.1 },
  };
  if (dir === "up")        { opt.flipV = true;  opt.line.endArrowType = "triangle"; }
  else if (dir === "down") { opt.line.endArrowType = "triangle"; }
  else if (dir === "right"){ opt.line.endArrowType = "triangle"; }
  else if (dir === "left") { opt.flipH = true;  opt.line.endArrowType = "triangle"; }
  else { opt.line.beginArrowType = "triangle"; opt.line.endArrowType = "triangle"; }
  if (o.flipH) opt.flipH = !opt.flipH;
  s.addShape("line", opt);
}

function aDash(s, x, y, w, h) {
  s.addShape("line", { x, y, w, h, line: { color: "808080", width: 1, dashType: "dash" } });
}

function aCloud(s, x, y, w, h) {
  s.addShape("cloud", { x, y, w, h, fill: { color: "FFFFFF" }, line: { color: LINE, width: 1 } });
}

function nodeBox(s, x, y, w, h, text, sub, o) {
  o = o || {};
  s.addShape("rect", {
    x, y, w, h,
    fill: { color: o.fill || "FFFFFF" },
    line: { color: o.line || RULE, width: o.lw || 1 },
  });
  s.addText(
    sub
      ? [{ text, options: { bold: true, fontSize: o.fs || 12, color: o.tc || INK, breakLine: true } },
         { text: sub, options: { fontSize: (o.fs || 12) - 2.5, color: o.sc || MUTED, bold: false } }]
      : text,
    { x: x + 0.08, y, w: w - 0.16, h, align: "center", valign: "middle",
      fontFace: FB, fontSize: o.fs || 12, bold: !sub, color: o.tc || INK,
      margin: 0, lineSpacingMultiple: 1.1 }
  );
}

function arrowDown(s, x, y, h) {
  s.addShape("line", { x, y, w: 0.01, h,
    line: { color: "B4BEC4", width: 1.5, endArrowType: "triangle" } });
}

// ============================================================
// flow-chart primitives — same look, but steps and yes/no tests
// ============================================================

function fBox(s, x, y, w, h, o) {
  o = o || {};
  s.addShape("rect", {
    x, y, w, h,
    fill: { color: o.fill || "FFFFFF" },
    line: { color: o.line || LINE, width: o.lw || 1, dashType: o.dash || "solid" },
  });
}

function fTxt(s, x, y, w, h, text, o) {
  o = o || {};
  s.addText(text, {
    x, y, w, h, align: o.align || "left", valign: o.valign || "middle",
    fontFace: o.ff || AF, fontSize: o.fs || 10, bold: !!o.bold,
    color: o.tc || "000000", margin: 0, lineSpacingMultiple: o.ls || 0.95,
  });
}

function fArrow(s, x, y, w, h, dir, o) {
  o = o || {};
  const opt = {
    x, y, w: w || 0.008, h: h || 0.008,
    line: { color: o.color || LINE, width: o.lw || 1.1, dashType: o.dash || "solid" },
  };
  if (dir === "up")        { opt.flipV = true;  opt.line.endArrowType = "triangle"; }
  else if (dir === "down") { opt.line.endArrowType = "triangle"; }
  else if (dir === "right"){ opt.line.endArrowType = "triangle"; }
  else if (dir === "left") { opt.flipH = true;  opt.line.endArrowType = "triangle"; }
  else if (dir === "plain"){ /* no head */ }
  else { opt.line.beginArrowType = "triangle"; opt.line.endArrowType = "triangle"; }
  s.addShape("line", opt);
}

function fDash(s, x, y, w, h) {
  s.addShape("line", { x, y, w, h, line: { color: "808080", width: 1, dashType: "dash" } });
}

function fHeader(s, title, sub) {
  fTxt(s, 0.45, 0.50, 11.5, 0.34, title, { fs: 15, bold: true });
  fTxt(s, 0.45, 0.84, 12.0, 0.26, sub, { fs: 9.5, tc: MUTED });
}

function fStep(s, x, y, w, h, head, detail, o) {
  o = o || {};
  fBox(s, x, y, w, h, { fill: o.fill || "FFFFFF", line: o.line || LINE, lw: o.lw || 1 });
  if (detail) {
    fTxt(s, x + 0.14, y + 0.05, w - 0.28, h * 0.46, head,
      { fs: o.hfs || 10, bold: true, tc: o.tc || "000000", ff: o.hff || AF, valign: "middle" });
    fTxt(s, x + 0.14, y + h * 0.46, w - 0.28, h * 0.50 - 0.02, detail,
      { fs: o.dfs || 8, tc: MUTED, valign: "top", ls: 0.94 });
  } else {
    fTxt(s, x + 0.14, y, w - 0.28, h, head,
      { fs: o.hfs || 10, bold: true, tc: o.tc || "000000", ff: o.hff || AF, align: o.align || "left" });
  }
}

function fTest(s, x, y, w, h, cond, note) {
  fBox(s, x, y, w, h, { fill: PANEL, lw: 1.25 });
  fTxt(s, x + 0.14, y + 0.04, w - 0.28, h * 0.52, cond, { fs: 9.5, bold: true, ff: FC, valign: "middle" });
  if (note) fTxt(s, x + 0.14, y + h * 0.52, w - 0.28, h * 0.44, note, { fs: 8, tc: MUTED, valign: "top", ls: 0.94 });
}

function fBranch(s, x, y, label, o) {
  o = o || {};
  fTxt(s, x, y, o.w || 0.42, o.h || 0.16, label, { fs: 7.5, tc: o.tc || MUTED, align: o.align || "left" });
}


// ============================================================
// THE 08-30 LAYOUT GRAMMAR — the default for every new page
// ------------------------------------------------------------
// Adopted after Adam compared the deck against qec_week1 ("字少，沒有廢話").
// The old grammar was numbered items with a paragraph under each; this one is
// label → value rows, and it exists to make two things true at once:
//
//   * no sentence appears on a slide — values are fragments joined by " · ";
//   * body type is 16 pt, because cutting the words is what pays for the type.
//
// Those two are one change, not two. The first pass cut the words and kept
// 12.5 pt body, which wasted the space it had just freed — Adam's note was
// "字太小". Anything under 11 pt does not go on a page.
//
// Reference implementation: generator/build_examples.js (five sample pages).
// ============================================================

// Title with no sentence under it. `kicker` is fragments — what the page is
// made of, not what it means. Six words is the ceiling. Replaces pageTitle()
// on new pages; pageTitle() stays for the 8/20 and 8/27 decks.
function head(s, title, kicker) {
  s.addText(title.toUpperCase(), {
    x: M, y: 0.62, w: CW, h: 0.66,
    fontFace: FH, fontSize: 34, bold: true, color: INK, margin: 0, charSpacing: 0.4,
  });
  if (kicker) {
    s.addText(kicker, {
      x: M, y: 1.34, w: CW, h: 0.30,
      fontFace: FB, fontSize: 13.5, color: FAINT, margin: 0, charSpacing: 0.3,
    });
  }
  s.addShape("line", { x: M, y: kicker ? 1.78 : 1.44, w: CW, h: 0.01,
    line: { color: RULE, width: 1 } });
}

// label → value, with a tick bar in the label's own colour. The label is a
// name (RESULT / LIMIT / WITHDRAWN), never a sentence. Tick colour carries the
// verdict, so a page needs no other colour coding.
function row(s, x, y, w, label, value, o) {
  o = o || {};
  const lw = o.lw || 2.30;
  const h = o.h || 0.54;
  s.addShape("rect", { x, y, w: 0.05, h,
    fill: { color: o.tick || ACCENT }, line: { type: "none" } });
  s.addText(label, {
    x: x + 0.22, y, w: lw - 0.22, h, valign: "middle",
    fontFace: FB, fontSize: o.lfs || 14, bold: true,
    color: o.lc || INK, margin: 0, charSpacing: 0.5,
  });
  s.addText(value, {
    x: x + lw, y, w: w - lw, h, valign: "middle",
    fontFace: FB, fontSize: o.fs || 16, color: o.vc || BODY, margin: 0,
    lineSpacingMultiple: 1.12, bold: !!o.b,
  });
}

// A verdict, in one or two words. ACCENT = it holds; anything else = it does not.
function chip(s, x, y, w, text, color) {
  const bg = color === ACCENT ? ACCENT_BG : WARN_BG;
  s.addShape("rect", { x, y, w, h: 0.36, fill: { color: bg },
    line: { color, width: 1.2 } });
  s.addText(text, { x, y, w, h: 0.36, align: "center", valign: "middle",
    fontFace: FB, fontSize: 12, bold: true, color, margin: 0, charSpacing: 0.4 });
}

// What the page answers, stated before it answers it. One line, no full stop
// needed on the sub — it is a qualifier, not a sentence.
function question(s, x, y, w, q, sub) {
  s.addShape("rect", { x, y, w: 0.05, h: sub ? 0.86 : 0.50,
    fill: { color: ACCENT }, line: { type: "none" } });
  s.addText("QUESTION", { x: x + 0.22, y: y - 0.02, w: w - 0.22, h: 0.28,
    fontFace: FB, fontSize: 12, bold: true, color: ACCENT, margin: 0, charSpacing: 0.8 });
  s.addText(q, { x: x + 0.22, y: y + 0.28, w: w - 0.22, h: 0.34,
    fontFace: FB, fontSize: 19, bold: true, color: INK, margin: 0 });
  if (sub) {
    s.addText(sub, { x: x + 0.22, y: y + 0.64, w: w - 0.22, h: 0.26,
      fontFace: FB, fontSize: 13, color: MUTED, margin: 0 });
  }
}

// Provenance, bottom-left. Commits and file paths live here and nowhere else.
function footNote(s, text) {
  s.addText(text, { x: M, y: 6.94, w: CW - 0.75, h: 0.30,
    fontFace: FB, fontSize: 11, color: FAINT, margin: 0 });
}

// One line of takeaway above the footnote. It costs 0.34" of the page, so the
// last row on a page that carries one has to end by 6.46 — measured, twice.
function keyLine(s, text) {
  s.addText(text, { x: M, y: 6.48, w: CW - 0.75, h: 0.32,
    fontFace: FB, fontSize: 14, bold: true, color: ACCENT, margin: 0 });
}

module.exports = {
  head,
  row,
  chip,
  question,
  footNote,
  keyLine,
  INK,
  WARNC,
  BODY,
  MUTED,
  FAINT,
  RULE,
  ACCENT,
  ACCENT_BG,
  PANEL,
  WARN_BG,
  FH,
  FB,
  FC,
  AF,
  LINE,
  M,
  CW,
  bind,
  newSlide,
  currentPage,
  pageTitle,
  pageNum,
  sectionTab,
  sectionCover,
  listItem,
  marginNote,
  defect,
  kvRows,
  pending,
  figurePage,
  aBox,
  aText,
  aArrow,
  aDash,
  aCloud,
  nodeBox,
  arrowDown,
  fBox,
  fTxt,
  fArrow,
  fDash,
  fHeader,
  fStep,
  fTest,
  fBranch,
};
