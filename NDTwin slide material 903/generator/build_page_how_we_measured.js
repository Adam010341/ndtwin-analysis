// "How we measured" — the gate band. One-page and two-page variants.
//
// Replaces the 09-01 first attempt (a four-box flowchart with three hanging
// guards), which Adam rejected: it looked like a generic process diagram and
// it drew the discipline as uniform. It is not uniform, and the page is worth
// having only because it is not.
//
// THE ONE THING THE PAGE HAS TO SAY
//   Every number in §2 cleared five gates before it was allowed to be printed
//   — and we know which crossings we did not make cleanly, and say so.
//   "We were rigorous" is not the claim. "This is the shape of the rigour,
//   and here is where it breaks" is.
//
// SO THE DRAWING IS A BAND, NOT BOXES-AND-ARROWS
//   Five vertical gate posts. Three thin horizontal lines — the build, size
//   and flow experiments — run left to right through all five. A line's style
//   IS the claim:
//       solid   the experiment cleared that gate as registered
//       dashed  it cleared it in a weaker form, disclosed as weaker
//       broken  the gate did not exist for that experiment
//   Solid / dashed / dotted survive greyscale printing; colour is not carrying
//   any of it (827 E1: one accent, and never as the only channel).
//
// EVERY NUMBER HERE IS QUOTED, NOT DERIVED
//   Source of record: paper/abstract/abstract.tex §"Three preregistered
//   measurements" (l.170–200) plus l.290–303 for the second machine. Nothing
//   on this page is recomputed or rounded — the ladder rungs, ≤0.5%, ±1 rung,
//   1.15.3-f0b7d201 and 79.66% are transcribed.
//
// Placement: immediately after the §2 cover, before page_M_cost-and-benefit —
// the position the template gives it (§C, row 15 of the 32-page table), so in
// the 23-page deck it becomes p.8 and the deck becomes 24 pages.
// It does not repeat the M page's COST PRE-REGISTERED / BENEFIT POST-HOC band:
// that band is about ticket M's own registration, this page is the three bmv2
// experiments, and neither number appears on the other.
const pptxgen = require("pptxgenjs");
const S = require("./deck_style");

const ONE = __dirname + "/../NDTwin_p08_how-we-measured.pptx";
const TWO = __dirname + "/../NDTwin_p08_how-we-measured_2page.pptx";

const { INK, WARNC, BODY, MUTED, FAINT, RULE, ACCENT, ACCENT_BG, PANEL,
        FH, FB, FC, M, CW } = S;

const TAB = "2 · WHAT THE EXPERIMENTS SAY";

// ---------------------------------------------------------------------------
// band geometry
// ---------------------------------------------------------------------------
const GX = [2.62, 4.66, 6.70, 8.74, 10.78];   // gate centres
const BAND_L = 2.30, BAND_R = 11.06;
// row pitch is 0.56, not 0.50: the two disclosure annotations live in the gaps
// between the lines, and at 0.50 they sat on the line below them.
const ROWY = [3.92, 4.48, 5.04];              // build · size · flow
const POST_T = 3.70, POST_B = 5.26;
const ICON_Y = 2.46, NAME_Y = 2.88, NOTE_Y = 5.46;
const COLW = 1.96;                            // per-gate text column

const GATES = [
  ["PREREGISTERED",     "intervals, meanings and when to abandon — all before data", INK],
  ["TWO MIRRORED ARMS", "the arm is the unit; a rep is a re-read",                   INK],
  ["BINARY IDENTITY",   "both builds print 1.15.3-f0b7d201",                         INK],
  ["CPU GATE",          "a sampler — on m2 it missed a co-tenant",                   WARNC],
  ["DUAL READOUT",      "kernel drops read 0 while bmv2 lost 79.66%",                INK],
];

// per experiment, the state of each of the six segments between L, the five
// gates, and R.  "s" solid · "d" dashed (weaker, disclosed) · "x" dotted after
// a break.  The break itself is drawn where the style first becomes "x".
const LINES = [
  ["BUILD", ["s", "s", "s", "s", "s", "s"]],
  ["SIZE",  ["s", "s", "s", "d", "d", "d"]],
  ["FLOW",  ["s", "s", "s", "d", "x", "x"]],
];

function icon(s, kind, cx, cy) {
  const A = ACCENT;
  const r = (x, y, w, h, fill) => s.addShape("rect",
    { x, y, w, h, fill: { color: fill || A }, line: { type: "none" } });
  if (kind === 0) {                       // a sealed sheet
    s.addShape("rect", { x: cx - 0.13, y: cy - 0.15, w: 0.26, h: 0.30,
      fill: { color: "FFFFFF" }, line: { color: A, width: 1.4 } });
    r(cx - 0.08, cy - 0.07, 0.16, 0.032);
    r(cx - 0.08, cy + 0.01, 0.16, 0.032);
    s.addShape("ellipse", { x: cx + 0.04, y: cy + 0.06, w: 0.13, h: 0.13,
      fill: { color: A }, line: { type: "none" } });
  } else if (kind === 1) {                // two mirrored bars
    r(cx - 0.16, cy - 0.10, 0.24, 0.075);
    r(cx - 0.08, cy + 0.03, 0.24, 0.075);
  } else if (kind === 2) {                // identity: [ ] = [ ]
    s.addShape("rect", { x: cx - 0.20, y: cy - 0.10, w: 0.14, h: 0.20,
      fill: { color: "FFFFFF" }, line: { color: A, width: 1.4 } });
    s.addShape("rect", { x: cx + 0.06, y: cy - 0.10, w: 0.14, h: 0.20,
      fill: { color: "FFFFFF" }, line: { color: A, width: 1.4 } });
    r(cx - 0.035, cy - 0.045, 0.07, 0.032);
    r(cx - 0.035, cy + 0.02, 0.07, 0.032);
  } else if (kind === 3) {                // a chip with pins
    s.addShape("rect", { x: cx - 0.11, y: cy - 0.11, w: 0.22, h: 0.22,
      fill: { color: "FFFFFF" }, line: { color: WARNC, width: 1.4 } });
    [-0.05, 0.02].forEach(o => {
      r(cx - 0.17, cy + o, 0.06, 0.032, WARNC);
      r(cx + 0.11, cy + o, 0.06, 0.032, WARNC);
    });
  } else {                                // two counters
    s.addShape("ellipse", { x: cx - 0.17, y: cy - 0.10, w: 0.20, h: 0.20,
      fill: { color: "FFFFFF" }, line: { color: A, width: 1.4 } });
    s.addShape("ellipse", { x: cx - 0.03, y: cy - 0.10, w: 0.20, h: 0.20,
      fill: { color: ACCENT_BG }, line: { color: A, width: 1.4 } });
  }
}

function machineGlyph(s, x, y) {
  s.addShape("rect", { x, y, w: 0.50, h: 0.34,
    fill: { color: "FFFFFF" }, line: { color: ACCENT, width: 1.4 } });
  s.addShape("rect", { x: x + 0.19, y: y + 0.34, w: 0.12, h: 0.07,
    fill: { color: ACCENT }, line: { type: "none" } });
  s.addShape("rect", { x: x + 0.07, y: y + 0.41, w: 0.36, h: 0.05,
    fill: { color: ACCENT }, line: { type: "none" } });
}

function seg(s, x1, x2, y, style) {
  if (x2 - x1 < 0.02) return;
  const o = { x: x1, y, w: x2 - x1, h: 0.008 };
  if (style === "s") o.line = { color: ACCENT, width: 2.6 };
  else if (style === "d") o.line = { color: ACCENT, width: 2.2, dashType: "dash" };
  else o.line = { color: MUTED, width: 2.4, dashType: "sysDot" };
  s.addShape("line", o);
}

// ---------------------------------------------------------------------------
// page 1 — the band
// ---------------------------------------------------------------------------
function bandPage(pres) {
  const s = S.newSlide();
  S.sectionTab(s, TAB);
  S.head(s, "How we measured",
    "five gates · three experiments · and where they do not hold");

  // the ladder is what enters the pipeline
  s.addText("ENTRY", { x: M, y: 1.92, w: 0.72, h: 0.26,
    fontFace: FB, fontSize: 11.5, bold: true, color: FAINT, margin: 0, charSpacing: 0.8 });
  s.addText("×1.5 rungs  ·  clean = loss ≤ 0.5% on 3-rep medians  ·  ±1 rung is the resolution",
    { x: M + 0.80, y: 1.90, w: CW - 0.80, h: 0.30,
      fontFace: FB, fontSize: 13.5, color: BODY, margin: 0 });

  // gates: icon, name, one short note
  GATES.forEach(([name, note, noteColour], i) => {
    const cx = GX[i];
    icon(s, i, cx, ICON_Y);
    s.addText(name, { x: cx - COLW / 2, y: NAME_Y, w: COLW, h: 0.62,
      align: "center", valign: "top", fontFace: FB, fontSize: 14.5, bold: true,
      color: i === 3 ? WARNC : INK, margin: 0, charSpacing: 0.4,
      lineSpacingMultiple: 1.06 });
    s.addShape("rect", { x: cx - 0.075, y: POST_T, w: 0.15, h: POST_B - POST_T,
      fill: { color: i === 3 ? WARNC : ACCENT }, line: { type: "none" } });
    s.addText(note, { x: cx - COLW / 2, y: NOTE_Y, w: COLW, h: 0.66,
      align: "center", valign: "top", fontFace: FB, fontSize: 11.5,
      color: noteColour === WARNC ? WARNC : MUTED, margin: 0,
      lineSpacingMultiple: 1.12 });
  });

  // the three experiments
  LINES.forEach(([label, styles], r) => {
    const y = ROWY[r];
    s.addText(label, { x: M, y: y - 0.17, w: 1.32, h: 0.34, align: "right",
      valign: "middle", fontFace: FB, fontSize: 14, bold: true, color: INK,
      margin: 0, charSpacing: 0.5 });
    s.addShape("ellipse", { x: BAND_L - 0.07, y: y - 0.06, w: 0.14, h: 0.14,
      fill: { color: ACCENT }, line: { type: "none" } });

    const xs = [BAND_L, ...GX, BAND_R];
    styles.forEach((st, i) => {
      const brokeHere  = st === "x" && styles[i - 1] !== "x";
      const breaksNext = styles[i + 1] === "x" && st !== "x";
      const a = brokeHere ? xs[i] + 0.14 : xs[i];
      // stop short of the post so the break sits in clear space: a WARNC cross
      // drawn on the WARNC post is invisible, and this mark is the whole row
      const b = breaksNext ? xs[i + 1] - 0.32 : xs[i + 1];
      seg(s, a, b, y, st);
      if (breaksNext) {
        // the gate did not exist for this experiment: show the break, do not
        // let a reader mistake a thin line for a passing one
        const bx = xs[i + 1] - 0.17, d = 0.115;
        [[-1, -1, 1, 1], [-1, 1, 1, -1]].forEach(([x1, y1, x2, y2]) =>
          s.addShape("line", {
            x: bx + x1 * d, y: y + y1 * d, w: (x2 - x1) * d, h: (y2 - y1) * d,
            line: { color: WARNC, width: 2.8 },
          }));
      }
    });
  });

  // the three annotations that are the whole point of the drawing
  // Three annotations, each in the empty lane above its own line so that it
  // crosses no post and no other experiment. Short on purpose: the sentence
  // they compress is on the facing page / in the script, not here.
  s.addText("restarts per arm", {
    x: GX[1] + 0.16, y: ROWY[0] - 0.34, w: 1.70, h: 0.28, align: "left",
    fontFace: FB, fontSize: 11.5, bold: true, color: ACCENT, margin: 0 });
  s.addText("weaker, disclosed", {
    x: GX[2] + 0.16, y: ROWY[1] - 0.34, w: 1.80, h: 0.28, align: "left",
    fontFace: FB, fontSize: 11.5, bold: true, color: ACCENT, margin: 0 });
  s.addText("no detector", {
    x: GX[3] + 0.20, y: ROWY[2] - 0.34, w: 1.50, h: 0.28, align: "left",
    fontFace: FB, fontSize: 11.5, bold: true, color: WARNC, margin: 0 });

  // the registered replication closes the band
  s.addShape("line", { x: BAND_R + 0.06, y: POST_T + 0.06, w: 0.008,
    h: POST_B - POST_T - 0.12, line: { color: RULE, width: 1.2 } });
  machineGlyph(s, 11.32, 3.84);
  machineGlyph(s, 11.98, 3.84);
  s.addText("m1", { x: 11.32, y: 4.36, w: 0.50, h: 0.24, align: "center",
    fontFace: FB, fontSize: 11, color: MUTED, margin: 0 });
  s.addText("m2", { x: 11.98, y: 4.36, w: 0.50, h: 0.24, align: "center",
    fontFace: FB, fontSize: 11, color: MUTED, margin: 0 });
  s.addText("registered\nreplication", {
    x: 11.20, y: 4.66, w: 1.32, h: 0.60, align: "center", valign: "top",
    fontFace: FB, fontSize: 12, bold: true, color: ACCENT, margin: 0,
    lineSpacingMultiple: 1.08 });

  S.keyLine(s,
    "Not “we were rigorous” — this is the shape of it, and where it breaks.");
  S.footNote(s,
    "Transcribed from paper/abstract §“Three preregistered measurements”. Solid = as registered · dashed = weaker, disclosed · broken = the gate did not exist for that experiment.");
  S.pageNum(s);
}

// ---------------------------------------------------------------------------
// page 2 (two-page variant only) — the three breaches, spelled out
// ---------------------------------------------------------------------------
function breachPage() {
  const s = S.newSlide();
  S.sectionTab(s, TAB);
  S.head(s, "Where it does not hold",
    "three crossings we did not make cleanly");

  [
    ["BINARY IDENTITY",
     "the build experiment checks a bidirectional symbol signature per arm against a negative control · size and flow read the binary off the process command line",
     ACCENT],
    ["WHY THAT MATTERS",
     "it is how we know both builds print the same version string, 1.15.3-f0b7d201 — the check that caught us out is the one worth keeping",
     MUTED],
    ["NO DETECTOR",
     "the flow experiment predates the CPU gate entirely and is reported with no foreign-load detector",
     WARNC],
    ["GATE COVERAGE",
     "on m2 the gate was a pre-run snapshot · it missed a co-tenant, and we found that from the tenant's own ledger, not from the gate",
     WARNC],
    ["WHICH WAY IT CUT",
     "foreign load can only slow an arm, so the contaminated reading was the flattering one",
     MUTED],
  ].forEach(([l, v, c], i) => {
    // 2.18 / 0.82: at 2.24 / 0.86 the fifth row's second line touches the key line
    S.row(s, M, 2.18 + i * 0.82, CW, l, v, { tick: c, lc: c, lw: 3.35, h: 0.70 });
  });

  S.keyLine(s, "A gate is a sampler, so we report its coverage — not its presence.");
  S.footNote(s,
    "paper/abstract §“Three preregistered measurements” and the second-machine paragraph. Every line here is already in the written record; none of it is new to this deck.");
  S.pageNum(s);
}

// ---------------------------------------------------------------------------

function build(file, twoPage) {
  const pres = new pptxgen();
  pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
  pres.layout = "WIDE";
  S.bind(pres);
  bandPage(pres);
  if (twoPage) breachPage();
  return pres.writeFile({ fileName: file });
}

// Requireable so a full-deck build can drop the page in at its position
// without a second copy of it: `require(...).bandPage(pres)` after S.bind().
// Both callers share one deck_style instance, so the page counter stays right.
module.exports = { bandPage, breachPage };

if (require.main === module) {
  build(ONE, false)
    .then(() => build(TWO, true))
    .then(() => console.log("done — 1-page and 2-page variants"))
    .catch(e => { console.error(e); process.exit(1); });
}
