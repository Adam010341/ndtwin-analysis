// NDTwin progress report, 2026-09-09. Thirty-one pages, three sections.
//
// = the 903 deck (23 pages) + the two method pages 903 added afterwards
//   (§C0-v2: the gate band and the outcome bands) + the six pages 909 adds.
// The 903 pages are required, not copied, so a fix there lands here too.
//
// v2 (2026-09-01), from Adam's four notes on the 32-page draft:
//
//   1. "廢話還是太多" — 32 → 23 pages. §1 went from eight content pages to two.
//      Nothing was summarised into a shorter sentence; whole pages were cut,
//      because a page that needs a sentence to justify it is the waffle.
//   2. "background 可以去掉" — the Background page is gone. The deck opens on
//      the promise ledger, which is the only orientation a returning reader
//      actually needs.
//   3. "manual 我主要是要直接給教授看 website" — so §1 does not reproduce the
//      site. Page 5 is five numbers set at 68 pt and nothing else; the talk
//      moves to the browser there. Page 6 carries the one thing the website
//      cannot show: what the verification found by running it.
//   4. "原本的字太小了" — type scale v2 in deck_style: body 16 → 18, labels
//      14 → 16, tables 13 → 15, and the big-number page at 68.
//
// Figure pages still carry their §G REQUIRED band (template §F). Two figures
// with §G entries are NOT in this cut — page_Q_assumed-denominator and
// page_Q_gate-after-fix, the template's own droppable ④ and ⑤ — so G3 and G4
// do not apply to this deck. If either page comes back, its band comes with it.
const pptxgen = require("pptxgenjs");

const HERE = __dirname;
const HERE903 = HERE + "/../../NDTwin slide material 903";
// §2 inherits 903's figures unchanged; 909 only adds its own
const FIG = HERE903 + "/figures/";
const HIRES = HERE903 + "/figures/_hires/";
const FIG909 = HERE + "/../figures/";
const OUT = HERE + "/../NDTwin_deck_909.pptx";

// One shared deck_style instance across every page module: the automatic page
// counter lives inside it, so a second copy would restart numbering midway.
const P903 = HERE903 + "/generator/";
const S = require(P903 + "deck_style");
const HWM = require(P903 + "build_page_how_we_measured");
const OB  = require(P903 + "build_page_outcome_bands");
const HIRES909 = HERE + "/../figures/p4-tutorials/_hires/";
const P909 = require("./pages_909");

const { INK, WARNC, BODY, MUTED, FAINT, RULE, ACCENT, FH, FB, FC, M, CW, T } = S;

const pres = new pptxgen();
pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
pres.layout = "WIDE";
S.bind(pres);
const NEW = P909(S, FIG909, HIRES909);

const TAB1 = "1 · THE MANUAL";
const TAB2 = "2 · WHAT THE EXPERIMENTS SAY";
const TAB3 = "3 · ENGINEERING, AND WHAT'S NEXT";

// ---------------------------------------------------------------------------

function table(s, x, y, w, colW, head, rows, opt) {
  opt = opt || {};
  const hdr = head.map(h => ({
    text: h, options: { bold: true, color: "FFFFFF", fill: { color: ACCENT },
      fontSize: opt.hfs || 13, charSpacing: 0.5 },
  }));
  const body = rows.map((r, i) => r.map((cell, j) => {
    const c = typeof cell === "object" ? cell : { t: cell };
    return {
      text: c.t,
      options: {
        fill: { color: c.bg || (i % 2 ? "FFFFFF" : "F7F9FA") },
        bold: !!c.b || j === 0,
        color: c.c || (j === 0 ? INK : BODY),
        fontSize: c.fs || opt.fs || T.table,
        fontFace: c.mono ? FC : FB,
        align: c.align || "left",
      },
    };
  }));
  s.addTable([hdr, ...body], {
    x, y, w, colW,
    rowH: [opt.hh || 0.42, ...rows.map(() => opt.rh || 0.50)],
    border: { type: "solid", color: "E4EAEE", pt: 1 },
    fontFace: FB, valign: "middle", margin: [0.05, 0.12, 0.05, 0.12],
  });
}

// A figure page. `req` is the §G REQUIRED band — the sentences the 08-30
// clean-figure ruling took off the figure, which §F makes this page's job.
function figPage(file, ar, tab, o) {
  o = o || {};
  const s = S.newSlide();
  if (tab) S.sectionTab(s, tab);

  const req = o.req || [];
  const bandH = req.length ? 0.42 + req.length * 0.66 : 0;

  let top = 0.50;
  if (o.title) {
    s.addText(o.title, { x: M, y: 0.44, w: CW, h: 0.48,
      fontFace: FH, fontSize: 24, bold: true, color: INK, margin: 0 });
    top = 1.08;
  }

  const availH = (req.length ? 6.84 - bandH : 7.02) - top;
  let w = CW, h = w / ar;
  if (h > availH) { h = availH; w = h * ar; }
  s.addImage({ path: (o.dir || FIG) + file,
    x: (13.333 - w) / 2, y: top + (availH - h) / 2, w, h });

  if (req.length) {
    let y = 7.02 - bandH + 0.06;
    s.addShape("line", { x: M, y: y - 0.16, w: CW, h: 0.01,
      line: { color: RULE, width: 1 } });
    req.forEach(([label, value, colour]) => {
      S.row(s, M, y, CW, label, value,
        { tick: colour || ACCENT, lc: colour || ACCENT, lw: o.lw || 3.05,
          fs: 15, lfs: 14, h: 0.58 });
      y += 0.66;
    });
  }
  S.pageNum(s);
  return s;
}

/* =========================================================================
   1 — title
   ========================================================================= */
{
  const s = S.newSlide();
  s.addText("NDTwin Network Digital Twin", {
    x: M, y: 2.16, w: 11.0, h: 0.44,
    fontFace: FB, fontSize: 17, color: ACCENT, margin: 0, charSpacing: 1.2 });
  s.addText("The Manual, Proven End to End", {
    x: M, y: 2.70, w: 11.6, h: 1.00,
    fontFace: FH, fontSize: 46, bold: true, color: INK, margin: 0 });
  s.addText("— and what one unstated build flag is worth", {
    x: M, y: 3.76, w: 11.6, h: 0.58,
    fontFace: FB, fontSize: 23, color: MUTED, margin: 0 });
  s.addShape("line", { x: M, y: 4.70, w: 1.1, h: 0.01,
    line: { color: ACCENT, width: 2 } });
  s.addText("Adam　·　2026-09-03", {
    x: M, y: 6.42, w: 8.0, h: 0.34,
    fontFace: FB, fontSize: 14, color: MUTED, margin: 0 });
}

/* =========================================================================
   2 — outline
   ========================================================================= */
{
  const s = S.newSlide();
  S.head(s, "Outline", null);

  const sections = [
    ["1", "The manual", "installed from the public document, in a clean room", "pp. 4–6"],
    ["2", "What the experiments say",
     "one build flag = 8× · capacity depends on flow count · 18 papers", "pp. 7–17"],
    ["3", "Engineering, and what's next",
     "the traffic round · a criterion that measured the wrong thing", "pp. 18–23"],
  ];

  let y = 2.60;
  sections.forEach(([n, t, d, p], i) => {
    s.addText(n, { x: M, y: y - 0.04, w: 0.46, h: 0.44,
      fontFace: FH, fontSize: 24, bold: true, color: ACCENT, margin: 0 });
    s.addText(t, { x: M + 0.64, y: y - 0.06, w: 7.8, h: 0.46,
      fontFace: FB, fontSize: 24, bold: true, color: INK, margin: 0 });
    s.addText(d, { x: M + 0.64, y: y + 0.46, w: 9.6, h: 0.36,
      fontFace: FB, fontSize: 15.5, color: BODY, margin: 0 });
    s.addText(p, { x: M + CW - 1.7, y: y - 0.04, w: 1.7, h: 0.40, align: "right",
      fontFace: FB, fontSize: 14, color: FAINT, margin: 0 });
    y += 1.34;
    if (i < sections.length - 1) {
      s.addShape("line", { x: M, y: y - 0.22, w: CW, h: 0.01,
        line: { color: "EFEFEF", width: 1 } });
    }
  });
  S.pageNum(s);
}

/* =========================================================================
   3 — where we left off
   ========================================================================= */
{
  const s = S.newSlide();
  S.head(s, "Where we left off",
    "three written on 27 August · one asked for since");

  const LX = M, LW = 3.55;
  const TX = 4.60, TW = 2.85;
  const VX = 7.62, VW = 1.50;
  const NX = 9.30, NW = M + CW - NX;

  [["THE ASK", LX + 0.24, LW], ["TEST SET IN ADVANCE", TX, TW], ["TODAY", NX, NW]]
    .forEach(([t, x, w]) => {
      s.addText(t, { x, y: 2.06, w, h: 0.28,
        fontFace: FB, fontSize: 11.5, color: FAINT, margin: 0, charSpacing: 0.8 });
    });

  const rows = [
    ["THE MANUAL", "install from the public document, clean room",
     "ANSWERED", ACCENT, "§1 · and the site is open in the next tab"],
    ["DOES MERGE MOVE THE WALL", "the 1-in-8 cell's loss moves, or it does not",
     "ANSWERED", ACCENT, "72 cells ran — the criterion could not see the wall (p. 19)"],
    ["FAST BUILD DEFAULT", "the L0–L4 suite passes on the fast build",
     "IN PART", WARNC, "install and provenance verified · the suite has not run"],
    ["THE BOOT RING", "arms to 0/6–0/8 on the fixed build",
     "NOT RUN", WARNC, "deliberately deprioritised · carried forward as written"],
  ];

  rows.forEach(([ask, test, verdict, vc, now], i) => {
    const y = 2.50 + i * 1.10;
    s.addShape("rect", { x: LX, y, w: 0.055, h: 0.84,
      fill: { color: vc }, line: { type: "none" } });
    s.addText(ask, { x: LX + 0.24, y, w: LW - 0.24, h: 0.84, valign: "middle",
      fontFace: FB, fontSize: 17, bold: true, color: INK, margin: 0, charSpacing: 0.4 });
    s.addText(test, { x: TX, y, w: TW, h: 0.84, valign: "middle",
      fontFace: FB, fontSize: 14, color: MUTED, margin: 0, lineSpacingMultiple: 1.1 });
    S.chip(s, VX, y + 0.22, VW, verdict, vc);
    s.addText(now, { x: NX, y, w: NW, h: 0.84, valign: "middle",
      fontFace: FB, fontSize: 15, color: BODY, margin: 0, lineSpacingMultiple: 1.1 });
    if (i < rows.length - 1) {
      s.addShape("line", { x: LX, y: y + 0.96, w: CW, h: 0.01,
        line: { color: "F0F0F0", width: 1 } });
    }
  });

  S.pageNum(s);
}

/* =========================================================================
   4 — §1 cover
   ========================================================================= */
S.sectionCover("1", "The manual",
  "Installed from the public document in a clean room — the site itself is the demo");

/* =========================================================================
   5 — the manual in five numbers.  The talk moves to the browser here.
   ========================================================================= */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB1);
  S.head(s, "It installs, and it runs", "clean-room VM · every command as printed");

  S.bigStats(s, [
    ["31", "installation steps run verbatim — zero non-zero exit codes"],
    ["12/12", "hosts reach each other on the fabric the manual builds"],
    ["29/29", "documented API endpoints exist, with the right methods"],
    ["7", "checks pass on the optional fast build — the debug install untouched"],
    ["16 s", "for the whole stack to converge, on a real clock"],
    ["12", "routes with no page — 29% of the HTTP surface"],
  ], 2.16);

  S.keyLine(s, "→ the manual itself, live");
  S.pageNum(s);
}

/* =========================================================================
   6 — what the verification found (the half a browser cannot show)
   ========================================================================= */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB1);
  S.head(s, "What running it found",
    "defects the document could not show · four fixed, two open");

  [
    ["THE MANUAL", "grep for the wrong error string · an undocumented interactive prompt · “wait 60 s” measured 80", ACCENT],
    ["THE PROGRAM", "a second proxy wrote rules before noticing the port was taken · the lock API accepted malformed requests", ACCENT],
    ["A GREEN CHECK", "“model matches fabric: 4 hosts” printed over 128 — it compares the model with the model", WARNC],
    ["A PHANTOM ROW", "a queued, unprogrammed request served as a flow-table row · visible at t = 0 only, on both planes", WARNC],
    ["STILL OPEN", "the Ubuntu Server variant · twelve undocumented routes, one of them called by the shipping GUI", MUTED],
  ].forEach(([l, v, c], i) => {
    S.row(s, M, 2.24 + i * 0.86, CW, l, v, { tick: c, lc: c, lw: 3.05, h: 0.70 });
  });

  S.keyLine(s, "The last two are system defects — found by running the document, not by reading it.");
  S.footNote(s, "doc/2026-08-30_manual-verification-report.md (798f9f5) · FINDING-01 and FINDING-03 at 569f976 · fixes at 89c1754, e29424e, dff87f9.");
  S.pageNum(s);
}

/* =========================================================================
   7 — §2 cover
   ========================================================================= */
S.sectionCover("2", "What the experiments say",
  "One unstated build flag, a capacity that depends on flow count, and eighteen papers that state neither");

/* =========================================================================
   8–9 — the two method pages 903 added after its §2 cover (§C0-v2)
   ========================================================================= */
HWM.bandPage(pres);
OB.outcomeBandsPage();

/* =========================================================================
   8–12 — the measurement figures
   ========================================================================= */
figPage("page_M_cost-and-benefit.png", 3040 / 1270, TAB2, {
  req: [
    ["COST PRE-REGISTERED", "effect +0.530 s, inside the registered 0.4–0.6 s band", ACCENT],
    ["BENEFIT POST-HOC", "not registered before the data was read — an observation, not a result", WARNC],
  ],
});

figPage("page_bandwidth-ceiling.png", 3040 / 1270, TAB2, {
  title: "The ceiling was the access layer; BMv2's is real",
  req: [
    ["THE FOUR SHORT BARS", "ECMP hashed onto the top four — not a capacity floor", WARNC],
    ["WHAT 53.1 IS", "an interface-counter rate · 32 TCP flows · one link's ECMP share · host CPU 98.7%", WARNC],
  ],
});

figPage("fig2_perflow_monotone.png", 638 / 464, TAB2, {
  title: "Capacity is a function of flow count",
  req: [
    ["UDP", "the ladder is iperf3 -u and “clean rate” is read from loss — this is a UDP claim", WARNC],
    ["THE CONTROL", "same path on TCP: T(16)/T(1) = 1.222 and 1.108 — no collapse", ACCENT],
  ],
});

figPage("fig7_aggregate_two_planes.png", 1916 / 1242, TAB2, {
  dir: HIRES,
  title: "One plane holds its cap; the other collapses below it",
  req: [
    ["UDP, BOTH PLANES", "both ladders are iperf3 -u -l 1400 · with TCP the collapse does not appear", WARNC],
    ["SO THE CLAIM IS", "“UDP collapses ≈10×”, not “BMv2 collapses”", ACCENT],
  ],
});

figPage("fig1_unit_ambiguity.png", 667 / 511, TAB2, {
  title: "Same data, two units, sixteen times apart",
  req: [["THE AMBIGUITY", "packet rate moves 1.25× while bit rate moves 16× — Mbit/s without a packet size is a 16× hole", WARNC]],
});

/* =========================================================================
   13 — the survey scoreboard
   ========================================================================= */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB2);
  S.head(s, "18 papers, and what they report",
    "12 of them measure BMv2 · counted, not estimated");

  table(s, M, 2.20, CW, [6.55, 1.85, 3.23],
    ["reporting dimension", "of the 12", "note"],
    [
      ["reports a throughput number", { t: "10 / 12", b: true, align: "center" },
       "two measure latency only"],
      ["states build flags", { t: "0 / 12", b: true, c: WARNC, align: "center" },
       "the variable worth 8× here"],
      ["runs a build comparison", { t: "0 / 12", b: true, c: WARNC, align: "center" }, ""],
      ["names the BMv2 variant", { t: "3 / 12", b: true, align: "center" },
       "all from one lab lineage"],
      ["states the version", { t: "1 / 12", b: true, c: WARNC, align: "center" }, ""],
      ["sweeps packet size", { t: "0 / 12", b: true, c: WARNC, align: "center" }, ""],
      ["uses flow count as a variable", { t: "0 / 12", b: true, c: WARNC, align: "center" }, ""],
    ], { rh: 0.52 });

  S.row(s, M, 6.16, CW, "THE GAP",
    "the one variable we measured at 8× is the one none of them state — in our sample of 18",
    { lw: 1.75, fs: 17, b: true });

  S.footNote(s, "doc/2026-08-29_bmv2-performance-study.md §2-1 at b2cd6b5. Every negative is a statement about these 18 papers and the search boundary in §5-4 — not about the literature.");
  S.pageNum(s);
}

/* =========================================================================
   14–17 — the survey figures
   ========================================================================= */
figPage("fig5_reporting_matrix.png", 2230 / 1493, TAB2, {
  dir: HIRES,
  title: "Twelve papers, nine reporting dimensions",
  req: [["THE GAPS ARE THE DATA", "column totals are asserted against the survey table — a drift crashes the plot rather than drawing it", MUTED]],
});

figPage("fig6_twelve_numbers_one_axis.png", 2363 / 1543, TAB2, {
  dir: HIRES,
  title: "Twelve headline numbers, one axis",
  req: [
    ["A THIRD CANNOT BE PLACED", "4/12 publish no bit-rate headline · 1/12 is a working point, not a ceiling", WARNC],
    ["NOTHING WAS CONVERTED", "a packets-per-second headline stays in packets per second", MUTED],
  ],
});

figPage("fig4_literature_spread.png", 717 / 430, TAB2, {
  title: "Self-reported throughputs span ~2,500×",
  req: [["FOR SCALE", "~0.57 Mbit/s to ~1.4 Gbit/s · one build flag on one machine is worth 8× of that", WARNC]],
});

figPage("fig8_known_but_never_reported.png", 2015 / 986, TAB2, {
  dir: HIRES,
  title: "Known is not the same as reported",
  req: [
    ["DESK CHECK", "sources read, not re-measured · BMv2's own page says the debug build is slow, and two papers cite it", MUTED],
    ["AND STILL", "neither states its own build · build flags stated: 0/12", WARNC],
  ],
});

/* =========================================================================
   18 — §3 cover
   ========================================================================= */
S.sectionCover("3", "Engineering, and what's next",
  "The traffic round, a criterion that measured the wrong quantity, and what the next report will carry");

/* =========================================================================
   19 — the ceiling was not read out
   ========================================================================= */
figPage("page_ceiling-not-read-out.png", 3040 / 1270, TAB3, {
  title: "The criterion never measured the quantity its name says",
  lw: 3.75,
  req: [
    ["NOT READ OUT", "SATURATED fired 0 times in 72 cells · all four arms right-censored · indistinguishable, not equal", WARNC],
    ["THE FLAT LINE MISLEADS", "twin ÷ truth reads 1.009 at the rung that destroys 87–89% of the traffic", WARNC],
    ["BATCHING NOT ESTIMABLE", "batch on/off is aliased with leg and time of day — a confound, not noise", MUTED],
  ],
});

/* =========================================================================
   20 — the traffic round
   ========================================================================= */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB3);
  S.head(s, "The traffic round",
    "six arms · registered before any data");

  [
    ["IT DISCRIMINATES", "the flow endpoint went 8 → 12 under load and tracked the churn — the gate held on both arms", ACCENT],
    ["CONTRACT", "39/39 against the live kernel, plus a 52-check self-test", ACCENT],
    ["THE 128-HOST EXAMPLE", "the manual's own worked example passes as printed", ACCENT],
    ["THE HALF NOT ASKED", "the timing question is unanswerable at 128 hosts — one sample costs 735 ms and needs 500", WARNC],
    ["AND NOT BY SAMPLING HARDER", "the instrument is slower than the thing it measures · answered at 4 hosts instead", WARNC],
  ].forEach(([l, v, c], i) => {
    S.row(s, M, 2.24 + i * 0.86, CW, l, v, { tick: c, lc: c, lw: 3.85, h: 0.70 });
  });

  S.footNote(s, "PREREG 5cbd672, written before any data; kernel 1208d22, rebuild byte-identical. One sample = three endpoints, of which all_destination_paths is 699 ms and 931 KB.");
  S.pageNum(s);
}

/* =========================================================================
   909 additions — Q12, the night round, and the tutorials group
   ------------------------------------------------------------------------
   §C-909 places Q12 in section 3; §C-909-T places T1–T4 after it and before
   "Planned for the next report". The night-round page sits between them: it
   is the same kind of claim as Q12 (an endpoint that reports the order rather
   than the state), so the two read as one argument.
   ========================================================================= */
NEW.q12();
NEW.nightRound();
NEW.t1();
NEW.t2();
NEW.t3();
NEW.t4();

/* =========================================================================
   worth writing up?
   ========================================================================= */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB3);
  S.head(s, "Worth writing up?", "asking, not arguing");

  S.question(s, M, 2.14, CW,
    "Has anyone quantified what an unstated build flag costs?");

  [
    ["MEASURED", "one build flag · 8.0× on a single hop · 12× across three", ACCENT],
    ["MEASURED", "unit ambiguity adds 16× on the same data", ACCENT],
    ["SURVEYED", "0/12 state that flag, in our sample of 18", ACCENT],
    ["DESK CHECK", "so a ~2,500× spread has no attributable cause — from reading, not measured", MUTED],
    ["THE QUESTION", "we did not find anyone who has done this · a pointer would be the useful answer", ACCENT],
  ].forEach(([l, v, c], i) => {
    // 3.24 / 0.62, not 3.36 / 0.66: five rows at the larger pitch put the last
    // one under the key line. Measured on the first render of the v2 scale.
    S.row(s, M, 3.24 + i * 0.62, CW, l, v, { tick: c, lc: c, lw: 2.55, fs: 16.5 });
  });

  S.keyLine(s, "Not that this is unknown — that being known has not made it reported.");
  S.pageNum(s);
}

/* =========================================================================
   22 — planned for the next report
   ========================================================================= */
{
  const s = S.newSlide();
  S.head(s, "Planned for the next report",
    "three, each with the test that settles it");

  const cols = [
    ["1", "Measure the ceiling with a criterion that can see it",
     "SATURATED never fired in 72 cells, so the arms cannot be told apart.",
     "Done when a registered criterion reads out a rung the data plane actually fails at."],
    ["2", "Finish the third question on its own terms",
     "The fast build's install and provenance are verified. The functional suite is not.",
     "Done when the whole L0–L4 suite passes on the fast build."],
    ["3", "Close the manual line to publishable grade",
     "Install, whole-stack and API page are green. Four executable pages remain.",
     "Done when every executable page has been executed."],
  ];

  const cw = (CW - 0.9) / 3;
  cols.forEach(([n, head, body, gate], i) => {
    const x = M + i * (cw + 0.45);
    s.addText(n, { x, y: 2.24, w: 0.34, h: 0.34,
      fontFace: FB, fontSize: 17, bold: true, color: ACCENT, margin: 0 });
    s.addText(head, { x, y: 2.70, w: cw, h: 0.90,
      fontFace: FB, fontSize: 18, bold: true, color: INK, margin: 0, lineSpacingMultiple: 1.1 });
    s.addText(body, { x, y: 3.76, w: cw, h: 1.30, valign: "top",
      fontFace: FB, fontSize: 15, color: BODY, margin: 0, lineSpacingMultiple: 1.2 });
    s.addShape("rect", { x, y: 5.20, w: 0.055, h: 1.16,
      fill: { color: ACCENT }, line: { type: "none" } });
    s.addText(gate, { x: x + 0.26, y: 5.16, w: cw - 0.26, h: 1.24, valign: "top",
      fontFace: FB, fontSize: 15, color: BODY, margin: 0, lineSpacingMultiple: 1.2 });
  });

  S.footNote(s, "Same shape as the 20 and 27 August pages, so the next report can be checked against this one.");
  S.pageNum(s);
}

/* =========================================================================
   23 — where it stands
   ========================================================================= */
{
  const s = S.newSlide();
  S.head(s, "Where it stands", "settled · open");

  const LX = M, RX = 7.05, W = 5.45;
  [["SETTLED", LX], ["OPEN", RX]].forEach(([t, x]) => {
    s.addText(t, { x, y: 2.06, w: W, h: 0.34,
      fontFace: FB, fontSize: 17, bold: true, color: ACCENT, margin: 0, charSpacing: 0.8 });
    s.addShape("line", { x, y: 2.50, w: W, h: 0.01, line: { color: RULE, width: 1 } });
  });

  const settled = [
    ["The manual installs", "clean room · 12/12 up"],
    ["The API page", "29/29 correct"],
    ["One build flag", "8.0× · 12× across three hops"],
    ["Units", "1.25× or 16×, by choice of unit"],
    ["Capacity", "a function of flow count (UDP)"],
    ["The survey", "0/12 state build flags"],
  ];
  const open = [
    ["The sampling ceiling", "measured fidelity, not the wall", true],
    ["Fast build as default", "L0–L4 has not run", true],
    ["Manual, remaining", "four executable pages", true],
    ["The boot ring", "arms never taken to 6–8"],
    ["Batching", "aliased with time of day"],
    ["Undocumented routes", "twelve · one used by the GUI"],
  ];

  function col(items, x) {
    let y = 2.72;
    items.forEach(([k, v, mark]) => {
      s.addShape("rect", { x, y: y + 0.06, w: 0.055, h: 0.32,
        fill: { color: mark ? ACCENT : RULE }, line: { type: "none" } });
      s.addText(k, { x: x + 0.24, y, w: 2.45, h: 0.44, valign: "middle",
        fontFace: FB, fontSize: 16, bold: true, color: mark ? ACCENT : INK, margin: 0 });
      s.addText(v, { x: x + 2.72, y, w: W - 2.72, h: 0.44, valign: "middle",
        fontFace: FB, fontSize: 15, color: BODY, margin: 0 });
      y += 0.68;
    });
  }
  col(settled, LX);
  col(open, RX);

  s.addText("Marked items are what the next report answers.", {
    x: RX + 0.24, y: 6.86, w: W, h: 0.30,
    fontFace: FB, fontSize: 12.5, color: FAINT, margin: 0 });

  S.pageNum(s);
}

pres.writeFile({ fileName: OUT })
  .then(() => console.log("done —", S.currentPage(), "pages"))
  .catch(e => { console.error(e); process.exit(1); });
