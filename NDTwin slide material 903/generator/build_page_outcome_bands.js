// One slide: the registered outcome spaces. Follows the gate band (p.8).
//
// WHAT THE PAGE HAS TO SAY
//   Before any arm ran, each variable's result space was cut into bands and
//   every band was given a meaning. So there is no "the experiment failed"
//   outcome — only which band the number landed in. All three bands are
//   results; that is the whole claim, and it is why they are drawn identically.
//
// WHY THE BANDS ARE EQUAL WIDTH
//   Because registration's point is that all three were equally admissible
//   before the data existed. Drawing them to scale would make the band that
//   happened to be hit look like the "right" one on two of the three rows —
//   which is the belief the page exists to contradict. Bands are schematic;
//   every interval is printed on the band, and the footnote says so.
//   🔴 No tick, no highlight, no heavier border on the band that was hit.
//
// THE TWO ROWS THAT CARRY THE ARGUMENT
//   BUILD — R = 8.0 lands in H2, but its quantisation interval (5.14, 12.0)
//           straddles the registered cut at 9. The bar crossing the cut IS the
//           row: we disclose a decision-rule gap rather than picking a side.
//   FLOWS — 220.0 sits outside the registered band, so the abandonment rule
//           fired. The row is shaped differently on purpose: this one is not
//           "another landing", it is the round being stopped.
//
// EVERY NUMBER IS TRANSCRIBED, NOT DERIVED — read back from the PREREGs:
//   doc/audit/2026-08-28_single-switch-build-ratio/PREREG.md:69–73
//   doc/audit/2026-08-28_packet-size-sweep/PREREG.md:79–90
//   doc/audit/2026-08-28_flow-count-capacity/PREREG.md:70–77
//   ...flow-count-capacity/HANDOFF-CONTEXT.md:65–67  (abandon rule, 48487ed)
//
// Division of labour with p.8: the gate band says WHICH CHECKS a number had to
// clear; this page says WHAT THE ANSWER WOULD HAVE MEANT whichever way it came
// out. p.8's PREREGISTERED post is the promise; this page is the content of it.
// Neither repeats the other's numbers.
//
// Not on the page, on purpose: the second machine's interval (3.27, 7.71).
// It intersects m1's, which is a replication claim — p.8 already carries the
// replication, and a second bar here would cost the row its single argument.
const pptxgen = require("pptxgenjs");
const S = require("./deck_style");

const OUT = __dirname + "/../NDTwin_p09_outcome-bands.pptx";
const { INK, WARNC, BODY, MUTED, FAINT, RULE, ACCENT, ACCENT_BG, PANEL,
        FH, FB, FC, M, CW } = S;

// Requireable: `require(...).outcomeBandsPage()` after S.bind(pres) drops the
// page into a full deck at its position, sharing one deck_style instance so
// the automatic page counter stays right.
function outcomeBandsPage() {
const s = S.newSlide();
S.sectionTab(s, "2 · WHAT THE EXPERIMENTS SAY");
S.head(s, "Every outcome had a meaning first",
  "three variables · three registered bands each · no “failed experiment”");

// ---------------------------------------------------------------------------
const X0 = 2.60, W = 9.88;               // the number line
const ROW = [2.16, 3.62, 5.08];          // pitch 1.46
const BLOCK_H = 0.52;

function rowLabel(y, name, variable) {
  s.addText(name, { x: M, y: y + 0.02, w: 1.62, h: 0.32, valign: "middle",
    fontFace: FB, fontSize: 15.5, bold: true, color: INK, margin: 0, charSpacing: 0.5 });
  s.addText(variable, { x: M, y: y + 0.36, w: 1.62, h: 0.44, valign: "top",
    fontFace: FB, fontSize: 12, color: MUTED, margin: 0, lineSpacingMultiple: 1.08 });
}

// three equal blocks, one registered band each. Identical in every respect —
// the hit band gets no mark of any kind.
function bands(y, labels, intervals) {
  const bw = W / 3;
  labels.forEach((lab, i) => {
    const x = X0 + i * bw;
    s.addShape("rect", { x, y, w: bw, h: BLOCK_H,
      fill: { color: PANEL }, line: { color: RULE, width: 1 } });
    s.addText(lab, { x: x + 0.08, y, w: bw - 0.16, h: BLOCK_H, align: "center",
      valign: "middle", fontFace: FB, fontSize: 13, bold: true, color: INK,
      margin: 0, lineSpacingMultiple: 1.05 });
    s.addText(intervals[i], { x, y: y + BLOCK_H + 0.04, w: bw, h: 0.24,
      align: "center", fontFace: FB, fontSize: 12.5, color: MUTED, margin: 0 });
  });
  // the registered cuts, drawn heavier than the block borders: they are the
  // decisions, the blocks are only their consequence
  [1, 2].forEach(i => {
    const x = X0 + i * bw;
    s.addShape("line", { x, y: y - 0.06, w: 0.008, h: BLOCK_H + 0.12,
      line: { color: INK, width: 2 } });
  });
  return bw;
}

function axis(y) {
  s.addShape("line", { x: X0, y, w: W, h: 0.008,
    line: { color: MUTED, width: 1.4 } });
}

function dot(x, y, colour, big) {
  const r = big ? 0.20 : 0.15;
  s.addShape("ellipse", { x: x - r / 2, y: y - r / 2, w: r, h: r,
    fill: { color: colour }, line: { color: "FFFFFF", width: 1 } });
}

/* =========================================================================
   A — BUILD: the ratio R, and an interval that straddles the cut at 9
   ========================================================================= */
{
  const y = ROW[0];
  rowLabel(y, "BUILD", "ratio R = fast ÷ stock,\none hop");
  const bw = bands(y,
    ["H2 · partly the path", "H1 · build property", "H3 · path was capping"],
    ["R < 9", "R = 9 – 20", "R > 20"]);
  const ay = y + 0.90;
  axis(ay);

  // positions are proportional inside the band the value belongs to
  const inB1 = v => X0 + (v / 9) * bw;                       // H2 spans 0–9
  const inB2 = v => X0 + bw + ((v - 9) / 11) * bw;           // H1 spans 9–20
  const xLo = inB1(5.14), xHi = inB2(12.0), xPt = inB1(8.0);

  // the quantisation interval, drawn across the cut it does not respect
  s.addShape("line", { x: xLo, y: ay, w: xHi - xLo, h: 0.008,
    line: { color: ACCENT, width: 3 } });
  [xLo, xHi].forEach(x => s.addShape("line", { x, y: ay - 0.10, w: 0.008, h: 0.20,
    line: { color: ACCENT, width: 2.4 } }));
  dot(xPt, ay, ACCENT, true);

  s.addText("R = 8.0", { x: xPt - 0.85, y: ay + 0.10, w: 1.70, h: 0.26,
    align: "center", fontFace: FB, fontSize: 13, bold: true, color: ACCENT, margin: 0 });
  s.addText("(5.14, 12.0)", { x: xHi + 0.14, y: ay + 0.10, w: 1.60, h: 0.26,
    fontFace: FB, fontSize: 12, color: MUTED, margin: 0 });
  s.addText("interval crosses the cut — a gap we disclose", {
    x: X0 + W - 4.20, y: ay + 0.10, w: 4.20, h: 0.26, align: "right",
    fontFace: FB, fontSize: 12, bold: true, color: WARNC, margin: 0 });
}

/* =========================================================================
   B — SIZE: three bands, and the middle one is a registered result too
   ========================================================================= */
{
  const y = ROW[1];
  rowLabel(y, "SIZE", "ratio P(1024) ÷ P(64),\ndelivered pps");
  const bw = bands(y,
    ["H2 · bandwidth-limited", "H3 · mixed cost", "H1 · per-packet cost"],
    ["0.03 – 0.12", "anything between", "0.65 – 1.30"]);
  const ay = y + 0.90;
  axis(ay);

  const xPt = X0 + 2 * bw + ((1.00 - 0.65) / 0.65) * bw;
  dot(xPt, ay, ACCENT, true);
  s.addText("1.00", { x: xPt - 0.85, y: ay + 0.10, w: 1.70, h: 0.26,
    align: "center", fontFace: FB, fontSize: 13, bold: true, color: ACCENT, margin: 0 });
  s.addText("H3 was registered as a result, not as “inconclusive”  ·  P(256)/P(64) also inside its H1", {
    x: X0, y: ay + 0.10, w: 7.20, h: 0.26,
    fontFace: FB, fontSize: 12, bold: true, color: INK, margin: 0 });
}

/* =========================================================================
   C — FLOWS: one registered band, and a number outside it
   ========================================================================= */
{
  const y = ROW[2];
  rowLabel(y, "FLOWS", "aggregate at n = 2,\nMbit");

  // a real scale here, not schematic blocks: this row is about a distance,
  // and the distance is the point
  const V0 = 60, V1 = 240;
  const X = v => X0 + ((v - V0) / (V1 - V0)) * W;

  s.addShape("rect", { x: X(95), y, w: X(150) - X(95), h: BLOCK_H,
    fill: { color: PANEL }, line: { color: RULE, width: 1 } });
  s.addText("registered", { x: X(95), y, w: X(150) - X(95), h: BLOCK_H,
    align: "center", valign: "middle", fontFace: FB, fontSize: 13, bold: true,
    color: INK, margin: 0 });
  s.addText("95 – 150", { x: X(95), y: y + BLOCK_H + 0.04, w: X(150) - X(95),
    h: 0.24, align: "center", fontFace: FB, fontSize: 12.5, color: MUTED, margin: 0 });
  [95, 150].forEach(v => s.addShape("line", { x: X(v), y: y - 0.06, w: 0.008,
    h: BLOCK_H + 0.12, line: { color: INK, width: 2 } }));

  const ay = y + 0.90;
  axis(ay);
  // the run stopped here, so the line beyond the band is not a path taken
  s.addShape("line", { x: X(150), y: ay, w: X(220) - X(150), h: 0.008,
    line: { color: MUTED, width: 2.2, dashType: "sysDot" } });
  dot(X(220), ay, WARNC, true);
  s.addText("220.0 · both arms", { x: X(220) - 1.70, y: ay + 0.10, w: 1.70,
    h: 0.26, align: "right", fontFace: FB, fontSize: 13, bold: true,
    color: WARNC, margin: 0 });

  S.chip(s, X(220) - 3.30, ay - 0.54, 1.90, "ABANDON RULE FIRED", WARNC);
  s.addText("the model that generated every interval was wrong — the curve stands, the intervals do not", {
    x: X0, y: ay + 0.10, w: 6.90, h: 0.26,
    fontFace: FB, fontSize: 12, bold: true, color: WARNC, margin: 0 });
}

S.keyLine(s,
  "A result is which band it landed in. All three bands were results.");
S.footNote(s,
  "Bands drawn equal-width on purpose: before the data, all three were equally admissible. Intervals transcribed from the three PREREGs; the abandonment rule is 48487ed, written before data.");
S.pageNum(s);

}

module.exports = { outcomeBandsPage };

if (require.main === module) {
  const pres = new pptxgen();
  pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
  pres.layout = "WIDE";
  S.bind(pres);
  outcomeBandsPage();
  pres.writeFile({ fileName: OUT })
    .then(() => console.log("done — 1 page"))
    .catch(e => { console.error(e); process.exit(1); });
}
