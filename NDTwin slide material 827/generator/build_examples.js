// Five sample pages: our house style, cut down to the reference deck's word count.
//
// What is kept from us: white ground, one accent (065A82), Cambria titles,
// the margins, automatic page numbers, section tabs, and a footnote that
// carries the commit a number was measured at.
//
// What is taken from the reference deck (qec_week1):
//   1. LABEL → VALUE rows. A short all-caps label on the left with a tick bar,
//      the content on the right. No paragraph anywhere on the page.
//   2. The dot separator does the work of a sentence:
//      "detect 44.9 s · debounce 3.0 · recompute 0.25". No verbs, no articles.
//   3. A two-word verdict vocabulary — ANSWERED / OPEN, RESULT / LIMIT,
//      CONFIRMED / WITHDRAWN — instead of a sentence that says the same thing.
//   4. A QUESTION block at the top of an evidence page, so the page states what
//      it is answering before it answers it.
//   5. The figure sits beside the findings rather than owning a page.
//
// The one deliberate deletion: our 110-character subtitle. Every content page
// had one; none of them survive here. That alone is about a third of the words.
//
// TYPE SCALE (second pass, Adam: "字太小"). Cutting the words is what pays for
// the type, so the two changes belong together — the first pass cut the words
// and then kept the old 12.5 pt body, which wastes the space it just freed.
// Body is 16, labels 14, the smallest thing on a content page is the 11 pt
// footnote. Nothing is under 11 except nothing.
const pptxgen = require("pptxgenjs");
const S = require("./deck_style");

const FIG = "/sessions/hopeful-sharp-hopper/mnt/outputs/exfig/";
const OUT = "/sessions/hopeful-sharp-hopper/mnt/outputs/NDTwin_style-examples.pptx";

const { INK, WARNC, BODY, MUTED, FAINT, RULE, ACCENT, ACCENT_BG, WARN_BG,
        FH, FB, FC, M, CW } = S;

const pres = new pptxgen();
pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
pres.layout = "WIDE";
S.bind(pres);

const TAB = "STYLE SAMPLE";

// ---------------------------------------------------------------------------
// the new primitives
// ---------------------------------------------------------------------------

// Title with no sentence under it. The kicker is fragments, not prose: it says
// what the page is made of, not what it means. Max about six words.
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

// label → value, with the tick bar. The label is a name, never a sentence;
// the value is fragments joined by " · ".
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

function chip(s, x, y, w, text, color) {
  const bg = color === ACCENT ? ACCENT_BG : WARN_BG;
  s.addShape("rect", { x, y, w, h: 0.36, fill: { color: bg },
    line: { color, width: 1.2 } });
  s.addText(text, { x, y, w, h: 0.36, align: "center", valign: "middle",
    fontFace: FB, fontSize: 12, bold: true, color, margin: 0, charSpacing: 0.4 });
}

// The question the page answers, said once, in one line.
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

function foot(s, text) {
  s.addText(text, { x: M, y: 6.94, w: CW - 0.75, h: 0.30,
    fontFace: FB, fontSize: 11, color: FAINT, margin: 0 });
}

// One line, bottom-left, in accent. It costs 0.34" of the page, so the last
// row of a page that carries one has to end by 6.46 — measured, twice.
function note(s, text) {
  s.addText(text, { x: M, y: 6.48, w: CW - 0.75, h: 0.32,
    fontFace: FB, fontSize: 14, bold: true, color: ACCENT, margin: 0 });
}

/* =========================================================================
   1 — the promises page. Five asks, four columns, no sentences.
   ========================================================================= */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB);
  head(s, "Where we left off", "five asks · the test each was given · today");

  const LX = M, LW = 3.15;          // the ask
  const TX = 4.15, TW = 3.30;       // the test
  const VX = 7.62, VW = 1.40;       // verdict
  const NX = 9.20, NW = M + CW - NX;

  [["THE ASK", LX + 0.22, LW], ["TEST SET IN ADVANCE", TX, TW],
   ["TODAY", NX, NW]].forEach(([t, x, w]) => {
    s.addText(t, { x, y: 2.00, w, h: 0.26,
      fontFace: FB, fontSize: 11, color: FAINT, margin: 0, charSpacing: 0.8 });
  });

  const rows = [
    ["OVS RECOVERY", "detect + recompute + install = 51.75 s",
     "ANSWERED", ACCENT, "it balances · 87% is detection"],
    ["FASTER DETECTION", "false positives, not detection time",
     "ANSWERED", ACCENT, "3.9× faster · idle false positives 0"],
    ["FAST BUILD DEFAULT", "L0–L4 suite passes on the fast build",
     "PREREQ", WARNC, "binaries separable · suite not run"],
    ["SFLOW JITTER", "one fabric · swap kernel, then rate",
     "ANSWERED", ACCENT, "inherited · stops paying at 1-in-32"],
    ["TRUNCATE / MERGE", "either moves the ceiling, or cost ≠ per byte",
     "IN PART", WARNC, "truncate: no · merge: wall unmeasured"],
  ];

  rows.forEach(([ask, test, verdict, vc, now], i) => {
    const y = 2.38 + i * 0.88;
    s.addShape("rect", { x: LX, y, w: 0.05, h: 0.62,
      fill: { color: vc }, line: { type: "none" } });
    s.addText(ask, { x: LX + 0.22, y, w: LW - 0.22, h: 0.62, valign: "middle",
      fontFace: FB, fontSize: 15.5, bold: true, color: INK, margin: 0, charSpacing: 0.4 });
    s.addText(test, { x: TX, y, w: TW, h: 0.62, valign: "middle",
      fontFace: FB, fontSize: 13.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.1 });
    chip(s, VX, y + 0.13, VW, verdict, vc);
    s.addText(now, { x: NX, y, w: NW, h: 0.62, valign: "middle",
      fontFace: FB, fontSize: 14.5, color: BODY, margin: 0, lineSpacingMultiple: 1.1 });
    if (i < rows.length - 1) {
      s.addShape("line", { x: LX, y: y + 0.74, w: CW, h: 0.01,
        line: { color: "F0F0F0", width: 1 } });
    }
  });

  foot(s, "Three from the 20 August closing slide, two from the meetings since.");
  S.pageNum(s);
}

/* =========================================================================
   2 — question, four findings, figure on the right.
   ========================================================================= */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB);
  head(s, "The failover budget", "128 hosts · one inter-switch link down · n = 10");

  const RW = 6.30;
  question(s, M, 2.04, RW, "Where do the 51.75 s go?",
    "the test was that the terms add up, not that a cause is found");

  [
    ["RESULT", "detect 44.9 s · debounce 3.0 · recompute 0.25", ACCENT],
    ["SO", "87% is waiting to notice · both suspects < 5%", ACCENT],
    ["FIX", "one constant · probe 0.05 → 0.01 · 51.8 → 16.4 s", ACCENT],
    ["LIMIT", "idle false positives only · threshold untouched", WARNC],
  ].forEach(([l, v, c], i) => {
    row(s, M, 3.28 + i * 0.88, RW, l, v,
      { tick: c, lc: c, lw: 1.45, h: 0.66, fs: 15.5 });
  });

  // The before/after figure, not the decomposition one. Once the body type is
  // 16 pt, a two-panel figure at 5" wide has the smallest text on the page —
  // and the decomposition is already spelled out in the RESULT row above, so
  // the figure only has to carry the one number a reader remembers.
  s.addImage({ path: FIG + "ovs-before-after.png",
    x: 7.30, y: 3.34, w: 5.18, h: 5.18 * (660 / 1440) });

  foot(s, "Decomposition at 4810e8f · detection at 07ae07c · after-fix at 45eccba.");
  S.pageNum(s);
}

/* =========================================================================
   3 — a table page. The table stays; the paragraphs under it become rows.
   ========================================================================= */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB);
  head(s, "The 45-point thread", "one boot · CPU trace and kernel log from the same run");

  const hdr = ["THREAD", "1/1024", "1/32", "WHAT IT IS"];
  const body = [
    [{ t: "calFlowPathByQueried", mono: true }, "46.31%", "46.84%", "1 kHz path recompute"],
    [{ t: "run", mono: true }, "3.98%", "13.86%", "the sFlow ingest"],
    [{ t: "testCalAvgFlowSendingRates…", mono: true }, "0.00%", "0.00%", "never runs"],
    [{ t: "purgeIdleFlows", mono: true }, "0.00%", "0.00%", "never runs"],
  ];
  const rowsX = [
    hdr.map(h => ({ text: h, options: { bold: true, color: "FFFFFF",
      fill: { color: ACCENT }, fontSize: 12, charSpacing: 0.5 } })),
    ...body.map((r, i) => r.map((c, j) => {
      const o = typeof c === "object" ? c : { t: c };
      const hot = (i === 0 && j > 0 && j < 3);
      return { text: o.t, options: {
        fill: { color: i % 2 ? "FFFFFF" : "F7F9FA" },
        bold: j === 0 || hot || (i === 1 && j === 2),
        color: hot ? WARNC : (j === 0 ? INK : BODY),
        fontSize: o.mono ? 12 : 13.5,
        fontFace: o.mono ? FC : FB } };
    })),
  ];
  s.addTable(rowsX, {
    x: M, y: 2.04, w: 11.63, colW: [3.85, 1.70, 1.70, 4.38],
    rowH: [0.38, ...body.map(() => 0.46)],
    border: { type: "solid", color: "E4EAEE", pt: 1 },
    fontFace: FB, valign: "middle", margin: [0.05, 0.12, 0.05, 0.12],
  });

  [
    ["FINDING", "32× the samples · +0.53 points · sampling is not the cost", ACCENT],
    ["IT IS", "a path recompute at 1 kHz · inherited · present at 28b8b13", ACCENT],
    ["INGEST", "3.98 → 13.86% · ×3.48 with the rate · this is the cost", ACCENT],
    ["NAMED HOW", "log and trace from one boot · tid offset moves per build", MUTED],
  ].forEach(([l, v, c], i) => {
    row(s, M, 4.48 + i * 0.62, CW, l, v, { tick: c, lc: c, lw: 2.05, fs: 16 });
  });

  foot(s, "Measured at 8c0516d · 46.31% falls between the 45.0 and 46.6 published on 20 August.");
  S.pageNum(s);
}

/* =========================================================================
   4 — the withdrawal. Verdict vocabulary carries the whole argument.
   ========================================================================= */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB);
  head(s, "Pre-registered, then withdrawn", "six cells · two levels · one control");

  question(s, M, 2.02, CW, "Does the same sample count mean the same precision?");

  [
    ["CONFIRMED", "pairing held · 0.84% and 0.44% · six cells healthy", ACCENT, false],
    ["ABOUT TO CLAIM", "cells not equivalent ⇒ the matrix cannot be skipped", INK, false],
    ["RESTED ON", "every pair clearing 0.1 · one cleared it by 0.040", MUTED, false],
    ["CONTROL", "same parameters ×3 · spread moved 0.136 · range 0.240", WARNC, false],
    ["WITHDRAWN", "the threshold cannot separate cell from cell", WARNC, true],
    ["NOT TAKEN", "widening to 0.24 rescues it — registration forbids that", ACCENT, true],
  ].forEach(([l, v, c, b], i) => {
    row(s, M, 2.98 + i * 0.58, CW, l, v, { tick: c, lc: c, lw: 2.55, fs: 15.5, b });
  });

  note(s, "The reversal was already in a draft of this deck. The control is why it is not in this one.");
  foot(s, "Pre-registration a7c2bd7 · result 8d109f2 · control c62bf3e.");
  S.pageNum(s);
}

/* =========================================================================
   5 — the closing page. Two columns of fragments, nothing else.
   ========================================================================= */
{
  const s = S.newSlide();
  head(s, "Where it stands", "settled · open · what the next report answers");

  const LX = M, RX = 7.05, W = 5.45;

  [["SETTLED", LX], ["OPEN", RX]].forEach(([t, x]) => {
    s.addText(t, { x, y: 2.00, w: W, h: 0.32,
      fontFace: FB, fontSize: 15, bold: true, color: ACCENT, margin: 0, charSpacing: 0.8 });
    s.addShape("line", { x, y: 2.40, w: W, h: 0.01, line: { color: RULE, width: 1 } });
  });

  const settled = [
    ["Failover budget", "balances · detection 87%"],
    ["Detection", "3.9× · false positives 0"],
    ["A sample", "206 µs · switches flat"],
    ["Precision", "stops paying at 1-in-32"],
    ["Truncation", "−5.6× bytes · ceiling unmoved"],
    ["Concurrency", "reads high · four rounds"],
  ];
  const open = [
    ["Boot convergence", "verified at N = 3 only", true],
    ["Fast build", "L0–L4 not run", true],
    ["Merge", "wired · wall unmeasured", true],
    ["Ceiling mechanism", "receive-side · inferred"],
    ["Scale × concurrency", "14% between generations"],
    ["Loaded false positives", "idle only"],
    ["Residual", "3.6 s · unexplained"],
  ];

  function col(items, x) {
    let y = 2.58;
    items.forEach(([k, v, mark]) => {
      s.addShape("rect", { x, y: y + 0.05, w: 0.05, h: 0.30,
        fill: { color: mark ? ACCENT : RULE }, line: { type: "none" } });
      s.addText(k, { x: x + 0.22, y, w: 2.60, h: 0.40, valign: "middle",
        fontFace: FB, fontSize: 15, bold: true,
        color: mark ? ACCENT : INK, margin: 0 });
      s.addText(v, { x: x + 2.84, y, w: W - 2.84, h: 0.40, valign: "middle",
        fontFace: FB, fontSize: 14.5, color: BODY, margin: 0 });
      y += 0.60;
    });
  }
  col(settled, LX);
  col(open, RX);

  s.addText("Marked items are what the next report answers.", {
    x: RX + 0.22, y: 6.86, w: W, h: 0.30,
    fontFace: FB, fontSize: 12, color: FAINT, margin: 0 });

  S.pageNum(s);
}

pres.writeFile({ fileName: OUT })
  .then(() => console.log("done —", S.currentPage(), "pages"))
  .catch(e => { console.error(e); process.exit(1); });
