// NDTwin progress report, 2026-08-27. Thirty-three pages, three sections.
//
// Structure (Adam, 2026-08-25, revised 08-26): three sections. The promises
// written down on 20 August and the experiments asked for since are one
// section, because they are the same kind of thing — a question that was put
// to us and now has an answer. Target is a 30-minute talk; the cut order is
// recorded in the template's C0.
//
// 08-26 late revision, from template v2.0:
//  - "Where we left off" carries five asks, not three. The jitter re-measure
//    and truncate/merge were asked for in the meetings since, so they are
//    promises on the same footing as the three written on the closing slide.
//  - The scale × concurrency page is unfrozen: the reversal that froze it was
//    a misread column, and four rounds all over-report (independently recounted).
//  - Merge is wired and through its gate, so it gets the figure page the
//    template's C5b asks for.
//
// Every number here is quoted from a doc/audit/ report and carries the commit
// it was measured at (template A2b). Style comes from deck_style.js — do not
// re-derive the palette or the margins.
const pptxgen = require("pptxgenjs");
const S = require("./deck_style");

const FIG = "/sessions/hopeful-sharp-hopper/mnt/NDTwin slide material 827/figures/";
const OUT = "/sessions/hopeful-sharp-hopper/mnt/outputs/NDTwin_deck_827.pptx";

const { INK, WARNC, BODY, MUTED, FAINT, RULE, ACCENT, ACCENT_BG, PANEL,
        FH, FB, FC, M, CW } = S;

const pres = new pptxgen();
pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
pres.layout = "WIDE";
S.bind(pres);

const TAB1 = "1 · ANSWERING THE OPEN QUESTIONS";
const TAB2 = "2 · ENGINEERING, AND WHAT'S NEXT";

// a plain table with the deck's header style
function table(s, x, y, w, colW, head, rows, opt) {
  opt = opt || {};
  const hdr = head.map(h => ({
    text: h, options: { bold: true, color: "FFFFFF", fill: { color: ACCENT }, fontSize: opt.hfs || 11 },
  }));
  const body = rows.map((r, i) => {
    const bg = { color: i % 2 ? "FFFFFF" : "F7F9FA" };
    return r.map((cell, j) => {
      const c = typeof cell === "object" ? cell : { t: cell };
      return {
        text: c.t,
        options: {
          fill: bg,
          bold: !!c.b || j === 0,
          color: c.c || (j === 0 ? INK : BODY),
          fontSize: c.fs || opt.fs || 10.5,
          fontFace: c.mono ? FC : FB,
        },
      };
    });
  });
  s.addTable([hdr, ...body], {
    x, y, w, colW,
    rowH: [opt.hh || 0.32, ...rows.map(() => opt.rh || 0.40)],
    border: { type: "solid", color: "E4EAEE", pt: 1 },
    fontFace: FB, valign: "middle",
    margin: [0.05, 0.10, 0.05, 0.10],
  });
}

function foot(s, text) {
  s.addText(text, {
    x: M, y: 6.96, w: CW - 0.75, h: 0.28,
    fontFace: FB, fontSize: 10, color: MUTED, margin: 0,
  });
}

/* ========================================================================
   1 — Title
   ======================================================================== */
{
  const s = S.newSlide();
  s.addText("NDTwin Network Digital Twin", {
    x: M, y: 2.16, w: 11.0, h: 0.42,
    fontFace: FB, fontSize: 16, color: ACCENT, margin: 0, charSpacing: 1.2,
  });
  s.addText("Where the Failover Time Went", {
    x: M, y: 2.72, w: 11.0, h: 0.95,
    fontFace: FH, fontSize: 44, bold: true, color: INK, margin: 0,
  });
  s.addText("— and what a sample costs", {
    x: M, y: 3.72, w: 11.0, h: 0.55,
    fontFace: FB, fontSize: 22, color: MUTED, margin: 0,
  });
  s.addShape("line", { x: M, y: 4.66, w: 1.1, h: 0.01, line: { color: ACCENT, width: 2 } });
  s.addText("Adam　·　2026-08-27", {
    x: M, y: 6.42, w: 8.0, h: 0.34,
    fontFace: FB, fontSize: 13, color: MUTED, margin: 0,
  });
}

/* ========================================================================
   2 — Outline
   ======================================================================== */
{
  const s = S.newSlide();
  S.pageTitle(s, "Outline", null);

  const sections = [
    { n: "0", t: "Background",
      d: "What was promised last time, and where the three data planes attach.",
      p: "pp. 4–5" },
    { n: "1", t: "Answering the open questions",
      d: "The failover budget, faster detection, what a sample costs, and a deadlock in the baseline.",
      p: "pp. 7–26" },
    { n: "2", t: "Engineering, and what's next",
      d: "Bring-up as one command, truncation and batching, and what the next report will carry.",
      p: "pp. 28–33" },
  ];

  let y = 2.40;
  sections.forEach((sec, i) => {
    s.addText(sec.n, { x: M, y: y - 0.02, w: 0.4, h: 0.34,
      fontFace: FH, fontSize: 17, bold: true, color: ACCENT, margin: 0 });
    s.addText(sec.t, { x: M + 0.5, y: y - 0.04, w: 7.6, h: 0.36,
      fontFace: FB, fontSize: 18, bold: true, color: INK, margin: 0 });
    s.addText(sec.d, { x: M + 0.5, y: y + 0.36, w: 9.2, h: 0.34,
      fontFace: FB, fontSize: 12.5, color: BODY, margin: 0 });
    s.addText(sec.p, { x: M + CW - 1.5, y: y - 0.02, w: 1.5, h: 0.34, align: "right",
      fontFace: FB, fontSize: 12, color: FAINT, margin: 0 });
    y += 0.92;
    if (i < sections.length - 1) {
      s.addShape("line", { x: M, y: y - 0.12, w: CW, h: 0.01, line: { color: "EFEFEF", width: 1 } });
    }
  });
  S.pageNum(s);
}

/* ========================================================================
   3 — section cover 0
   ======================================================================== */
S.sectionCover("0", "Background",
  "What was promised last time, and where the three data planes attach");

/* ========================================================================
   4 — Where we left off
   ======================================================================== */
{
  const s = S.newSlide();
  S.pageTitle(s, "Where we left off",
    "Five things were asked for — three on the 20 August closing slide, two in the meetings since. Each came with a test");

  // Five rows, not three columns. Three asks fitted across the page; five do
  // not, and shrinking the type to make them fit is the wrong trade — the
  // reading order here is "ask → test → verdict", which is a row.
  const rows = [
    ["1", "Find where the OVS 128-host recovery time goes",
     "detection + recompute + install must add up to 51.75 s",
     "ANSWERED", ACCENT,
     "It balances — and 87% of it is waiting to notice."],
    ["2", "Make failure detection faster without making it wrong",
     "judged on the false-positive rate, not on the detection time",
     "ANSWERED", ACCENT,
     "3.9× faster. Idle false positives: zero."],
    ["3", "Promote the fast bmv2 build to the default",
     "the whole L0–L4 suite must pass on the fast build",
     "PREREQUISITE", WARNC,
     "The binaries can be told apart. The suite has not been run."],
    ["4", "Re-measure the sFlow jitter — baseline, and across sampling rates",
     "one fabric, one flow: swap only the kernel binary, then only the sample rate",
     "ANSWERED", ACCENT,
     "Inherited, not ours — and it stops buying precision at 1-in-32."],
    ["5", "Try packet truncation, and batching",
     "either one moves the sampling ceiling, or the cost is not per byte",
     "IN PART", WARNC,
     "Truncation works and buys nothing. Merge is wired and verified; its effect on the ceiling is not measured."],
  ];

  const AX = M + 0.34, AW = 4.30;      // the ask
  const VX = 5.86, VW = 1.42;          // the verdict chip
  const NX = 7.46, NW = M + CW - NX;   // where it stands today

  s.addText("the test we set ourselves", { x: AX, y: 2.02, w: AW, h: 0.22,
    fontFace: FB, fontSize: 9, color: FAINT, margin: 0, charSpacing: 0.6 });

  rows.forEach(([n, head, test, verdict, vc, now], i) => {
    const y = 2.30 + i * 0.90;
    s.addText(n, { x: M, y: y - 0.02, w: 0.30, h: 0.28,
      fontFace: FB, fontSize: 12, bold: true, color: ACCENT, margin: 0 });
    // the test line sits at a fixed offset in every row, not under the heading:
    // one of the five headings takes two lines, and a floating test line makes
    // the whole column look ragged for the sake of that one row.
    s.addText(head, { x: AX, y: y - 0.04, w: AW, h: 0.52, valign: "top",
      fontFace: FB, fontSize: 13, bold: true, color: INK, margin: 0, lineSpacingMultiple: 1.1 });
    s.addText(test, { x: AX, y: y + 0.50, w: AW, h: 0.30, valign: "top",
      fontFace: FB, fontSize: 9.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.16 });

    s.addShape("rect", { x: VX, y: y + 0.04, w: VW, h: 0.34,
      fill: { color: vc === ACCENT ? ACCENT_BG : "FBF2F0" }, line: { color: vc, width: 1.3 } });
    s.addText(verdict, { x: VX, y: y + 0.04, w: VW, h: 0.34, align: "center",
      fontFace: FB, fontSize: 10.5, bold: true, color: vc, margin: 0 });

    s.addText(now, { x: NX, y: y - 0.02, w: NW, h: 0.74, valign: "top",
      fontFace: FB, fontSize: 11.5, color: BODY, margin: 0, lineSpacingMultiple: 1.2 });

    if (i < rows.length - 1) {
      s.addShape("line", { x: M, y: y + 0.80, w: CW, h: 0.01,
        line: { color: "EFEFEF", width: 1 } });
    }
  });

  foot(s, "Tests 1–3 are quoted verbatim from the 20 August closing slide; 4 and 5 were asked for in the meetings since, and are answered on the same terms.");
  S.pageNum(s);
}

/* ========================================================================
   5 — architecture (figure)
   ======================================================================== */
S.figurePage(FIG, "page_architecture.png", 4000 / 2250, null);

/* ========================================================================
   6 — section cover 1
   ======================================================================== */
S.sectionCover("1", "Answering the open questions",
  "Everything in this section was asked for — three written down on 20 August, the rest in the meetings since");

/* ========================================================================
   7 — the budget (figure)
   ======================================================================== */
S.figurePage(FIG, "page_failover-budget.png", 1590 / 990, TAB1);

/* ========================================================================
   8 — where the recompute time goes
   ======================================================================== */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB1);
  S.pageTitle(s, "Where the recompute time actually goes",
    "The walk installs 1,280 rules and builds 16,256 path entries — only one of those grows with the square");

  table(s, M, 2.24, 7.55,
    [1.15, 1.15, 1.35, 1.65, 1.15, 1.10],
    ["hosts", "rules", "install", "path entries", "report", "report %"],
    [
      ["8",   "80",    "0.007 s", "56",     "0.003 s", "30%"],
      ["16",  "160",   "0.009 s", "240",    "0.009 s", "50%"],
      ["32",  "320",   "0.022 s", "992",    "0.052 s", "70%"],
      ["64",  "640",   "0.044 s", "4,032",  "0.286 s", "86%"],
      [{ t: "128", b: true }, { t: "1,280", b: true },
       { t: "0.103 s", b: true }, { t: "16,256", b: true },
       { t: "2.063 s", b: true, c: ACCENT }, { t: "95%", b: true, c: ACCENT }],
    ], { rh: 0.38, fs: 10.5 });

  let y = 4.72;
  [
    ["Installing rules is linear",
     "16× the hosts, 14.7× the install. One rule per (switch, destination)."],
    ["Building the path table is super-quadratic",
     "The same 16× costs 688×. One entry per ordered host pair — that is what “16,256 paths” has always meant."],
  ].forEach(([h, b], i) => {
    S.listItem(s, M, y, 7.5, String(i + 1), h, b);
    y += 1.12;
  });

  S.marginNote(s, 8.75, 2.26, 3.73, 1.30, "One variable per cell",
    "Same live fabric in all five; only the topology model is swapped. Ten real switches, one noise floor.");

  S.marginNote(s, 8.75, 3.78, 3.73, 1.55, "So “routing is slow” has to be split",
    "The bookkeeping is slow, not the programming of the switches. At 128 hosts the recompute is 0.25 s once the host lookup is indexed.");

  foot(s, "Sweep at 529e021; recompute re-measured at 4810e8f. Method: five sizes, one fabric, one variable.");
  S.pageNum(s);
}

/* ========================================================================
   9 — ruling out the topology read path
   ======================================================================== */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB1);
  S.pageTitle(s, "Ruling out the controller's topology read path",
    "The kernel re-reads three Ryu topology endpoints on every change — so all three were timed at both fabric sizes");

  table(s, M, 2.30, 7.55,
    [2.55, 1.65, 1.65, 0.85, 0.85],
    ["endpoint", "4 hosts", "128 hosts", "time", "bytes"],
    [
      [{ t: "/v1.0/topology/switches", mono: true, fs: 9.5 },
       "0.461 ms / 4,158 B", "1.127 ms / 17,154 B", "2.44×", "4.13×"],
      [{ t: "/v1.0/topology/hosts", mono: true, fs: 9.5 },
       "0.346 ms / 812 B", "1.225 ms / 26,345 B", { t: "3.54×", b: true, c: ACCENT }, { t: "32.44×", b: true, c: ACCENT }],
      [{ t: "/v1.0/topology/links", mono: true, fs: 9.5 },
       "0.449 ms / 7,176 B", "0.797 ms / 7,176 B", "1.78×", "1.00×"],
    ], { rh: 0.44, fs: 10 });

  let y = 4.30;
  [
    ["Under 1.3 ms at both sizes",
     "Four orders of magnitude below the 51.75 s being explained."],
    ["The shape is wrong too — the stronger argument",
     "/hosts ships 32× the data for 3.5× the time. Sub-linear serialisation, the opposite of super-linear work on a bigger graph."],
  ].forEach(([h, b], i) => {
    S.listItem(s, M, y, 7.5, String(i + 1), h, b);
    y += 1.24;
  });

  S.marginNote(s, 8.75, 2.32, 3.73, 1.50, "Why these hold",
    "n = 20, median, first three discarded. Each cell separated by a full teardown — three different kernel pids, so nothing was inherited.");

  S.marginNote(s, 8.75, 4.04, 3.73, 1.70, "One assertion missed what moved",
    "A fourth endpoint was dropped: byte-identical at both sizes, because the small cell served a path table built for the large one. The probe asserted the host count — against an endpoint the path table is not derived from.");

  foot(s, "Measured at d9f580b, reported at 2de67b7. Probe and raw JSON in doc/audit/2026-08-21_ryu-topology-scaling/.");
  S.pageNum(s);
}

/* ========================================================================
   10 — the fix
   ======================================================================== */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB1);
  S.pageTitle(s, "One constant, and what it did not change",
    "Detection is set by how often a port is probed, not by how much evidence is required — only the first of those was touched");

  let y = 2.30;
  [
    ["The probe interval",
     "0.05 → 0.01. Ryu probes every port in turn and sleeps between sends, so the gap between two probes of one port is port-count × guard. At 160 ports: 44.9 s, then 11.5 s."],
    ["The recompute",
     "Host lookup indexed, cache token made O(1). The walk goes 2.17 s → 0.25 s."],
    ["A spare lever, left off by default",
     "Ports that never answer LLDP can be probed once every N rounds, so detection scales with switches, not ports."],
  ].forEach(([h, b], i) => {
    S.listItem(s, M, y, 7.35, String(i + 1), h, b);
    y += 1.42;
  });

  S.marginNote(s, 8.55, 2.32, 3.93, 1.90, "The threshold is untouched",
    "Still six consecutive misses before a link is called dead. The other lever — dropping that to two — reaches the same number by accepting weaker evidence. That contrast is the point of this page.");

  S.marginNote(s, 8.55, 4.48, 3.93, 1.90, "Judged on false positives, as promised",
    "Three cells, 20 minutes idle each, ~48,000 probe opportunities per window: zero links deleted, zero topology-changed events — and every cell still caught a real injected failure.");

  foot(s, "Detection at 07ae07c. Idle only — the loaded case is not measured, and neither default has been changed.");
  S.pageNum(s);
}

/* ========================================================================
   11 — before / after (figure)
   ======================================================================== */
S.figurePage(FIG, "page_ovs-before-after.png", 1440 / 660, TAB1);

/* ========================================================================
   12 — OVS vs BMv2 after (figure)
   ======================================================================== */
S.figurePage(FIG, "page_ovs-vs-bmv2-after.png", 1440 / 690, TAB1);

/* ========================================================================
   13 — which bmv2 produced which number
   ======================================================================== */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB1);
  S.pageTitle(s, "Which bmv2 produced which number",
    "Both builds answer --version with the same string — so this page identifies them by what actually differs");

  table(s, M, 2.30, 7.55,
    [2.05, 2.75, 2.75],
    ["", "stock", "fast"],
    [
      [{ t: "path", mono: true }, { t: "/usr/local/bin/", mono: true, fs: 9.5 }, { t: "/usr/local/bmv2-fast/bin/", mono: true, fs: 9.5 }],
      [{ t: "--version", mono: true }, { t: "1.15.3-f0b7d201", mono: true, fs: 9.5 },
       { t: "1.15.3-f0b7d201  ← same", mono: true, fs: 9.5, c: WARNC, b: true }],
      [{ t: "sha256", mono: true }, { t: "327fa7d1…", mono: true, fs: 9.5, c: ACCENT, b: true }, { t: "3ff54b5c…", mono: true, fs: 9.5, c: ACCENT, b: true }],
      [{ t: "size", mono: true }, "9,576,568 B", "92,147,960 B"],
      [{ t: "build", mono: true }, { t: "-O0 -g, logging on", mono: true, fs: 9.5 }, { t: "-O3 -march=native, logging off", mono: true, fs: 9.5 }],
      [{ t: "measured", mono: true }, "~40 Mbps / 3.6k pps", { t: "460–530 Mbps / 50.8k pps", b: true, c: ACCENT }],
    ], { rh: 0.34, fs: 10 });

  let y = 4.84;
  [
    ["Identify by hash, not by version string",
     "sha256, BuildID and size separate the two; --version does not."],
    ["Past -O3 numbers can be attributed backwards",
     "The source SHA is inside the binary's own --version, and that tree is still on disk — so an earlier report calling the -O3 cell unpinnable was wrong."],
  ].forEach(([h, b], i) => {
    S.listItem(s, M, y, 7.5, String(i + 1), h, b);
    y += 1.10;
  });

  S.marginNote(s, 8.75, 2.32, 3.73, 1.90, "The prerequisite, not the test",
    "The criterion was that the whole L0–L4 suite passes on the fast build. It has not been run. What exists now is the thing that had to come first — being able to say which binary produced a number.");

  S.marginNote(s, 8.75, 4.48, 3.73, 1.25, "One seam, not two",
    "Choosing a binary happens in one place, shared by both topologies.");

  foot(s, "Provenance at 2c8486a, measured at d9f580b.");
  S.pageNum(s);
}

/* ========================================================================
   14–19 — the six experiment figures
   ======================================================================== */
S.figurePage(FIG, "page_sampling-tradeoff.png",        2440 / 1040, TAB1);
// ...and the three pages that say where that trend stops. Same fabric, same
// flow, same edge — only the pipeline's sample rate moves.
S.figurePage(FIG, "page_ladder-across-rates.png",      3040 / 1270, TAB1);
S.figurePage(FIG, "page_sampling-ceiling.png",         3040 / 1270, TAB1);
S.figurePage(FIG, "page_who-is-the-bottleneck.png",    3040 / 1270, TAB1);
S.figurePage(FIG, "page_where-the-cpu-goes.png",       2520 / 1300, TAB1);
S.figurePage(FIG, "page_matrix-decomposition.png",     2600 / 1120, TAB1);

/* ========================================================================
   The 45-point thread — the largest CPU consumer is not sampling at all
   ======================================================================== */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB1);
  S.pageTitle(s, "The 45-point thread is not sampling cost",
    "Named from the kernel log of the same boot, not from a thread-id offset — 32× more samples move it by 1%");

  table(s, M, 2.30, 7.55,
    [3.15, 1.35, 1.35, 1.70],
    ["thread", "1/1024", "1/32", "what it is"],
    [
      [{ t: "calFlowPathByQueried", mono: true, fs: 9.5 },
       { t: "46.31%", b: true, c: WARNC }, { t: "46.84%", b: true, c: WARNC },
       { t: "a 1 kHz path recompute", fs: 9.5 }],
      [{ t: "run", mono: true, fs: 9.5 },
       "3.98%", { t: "13.86%", b: true, c: ACCENT },
       { t: "the sFlow ingest", fs: 9.5 }],
      [{ t: "testCalAvgFlowSendingRates…", mono: true, fs: 9 },
       "0.00%", "0.00%", { t: "never runs", fs: 9.5 }],
      [{ t: "purgeIdleFlows", mono: true, fs: 9.5 },
       "0.00%", "0.00%", { t: "never runs", fs: 9.5 }],
    ], { rh: 0.40, fs: 10 });

  let y = 4.44;
  [
    ["Thirty-two times the samples moves it by one percent",
     "So those 45 points have nothing to do with sampling. It is a full path recompute running at 1 kHz — and it is inherited: present at 28b8b13."],
    ["The ingest thread is the one that scales",
     "3.98% → 13.86%, a factor of 3.48 as the sample rate rises. That is what sampling actually costs inside the kernel."],
  ].forEach(([h, b], i) => {
    S.listItem(s, M, y, 7.5, String(i + 1), h, b);
    y += 1.24;
  });

  S.marginNote(s, 8.75, 2.32, 3.73, 1.90, "Why the threads could be named at all",
    "Both the CPU trace and the kernel log come from the same boot. The earlier round archived no log, and the thread-id offset moves between builds — so those traces can never be mapped back to names.");

  foot(s, "Measured at 8c0516d. 46.31% falls between the 45.0 and 46.6 published on 20 August — an independent check on the unit conversion.");
  S.pageNum(s);
}
S.figurePage(FIG, "page_iperf-competes.png",           2320 / 1240, TAB1);
S.figurePage(FIG, "page_api-concurrency-envelope.png", 2320 / 980,  TAB1);
S.figurePage(FIG, "page_ladder-inherited.png",         2720 / 1240, TAB1);

/* ========================================================================
   Scale × concurrency — every previous 128-host run carried one flow
   ------------------------------------------------------------------------
   Unfrozen on 26 August. The reversal that froze this page (a 0.92 that
   looked like under-reporting) was a per-edge minimum read out of the wrong
   column; four rounds all over-report, and an independent recount agrees.
   What is still open is the magnitude, so no single ratio appears here
   without the round it came from.
   ======================================================================== */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB1);
  S.pageTitle(s, "Under concurrency, the twin reads high",
    "Every 128-host measurement until now carried one flow and loaded three switches in ten — this one loads all ten");

  table(s, M, 2.30, 7.55,
    [2.35, 1.75, 1.75, 1.70],
    ["edge class", "as measured", "recounted", "edges"],
    [
      ["host → switch", { t: "1.23×", b: true, c: WARNC }, { t: "1.26×", b: true, c: WARNC }, "62 of 122"],
      ["switch → host", { t: "1.34×", b: true, c: WARNC }, { t: "1.41×", b: true, c: WARNC }, "62 of 128"],
      ["switch → switch", { t: "1.26×", b: true, c: WARNC }, { t: "1.33×", b: true, c: WARNC }, "8 of 32"],
      [{ t: "OVS, 64 flows", fs: 10 }, { t: "flat to 0.2%", c: ACCENT, b: true },
       { t: "—", c: MUTED }, { t: "all three classes", fs: 9.5 }],
    ], { rh: 0.42, fs: 10.5 });

  let y = 4.62;
  [
    ["High on every edge class, well past the noise",
     "The aggregate sampling error floor here is 1.7–2.9%. Twenty-plus points is not it — and four rounds all point the same way."],
    ["Recounted from the raw with a different method",
     "Different windows, an independently written interface mapping, no filtering of edges: same direction, same size, same ordering of the three classes."],
  ].forEach(([h, b], i) => {
    S.listItem(s, M, y, 7.5, String(i + 1), h, b);
    y += 1.16;
  });

  S.marginNote(s, 8.75, 2.32, 3.73, 1.60, "Why a single ratio is not quoted",
    "Sixteen flows, same settings, two fabric generations: 1.19 on one and 1.03–1.05 on the other. Within one generation the repeats agree to four decimals, so that 14% is not run-to-run noise — it is unexplained. Ratios from different generations are never divided.");

  S.marginNote(s, 8.75, 4.16, 3.73, 2.05, "What this does not show",
    "Not that scale is the cause. The traffic generator changed at the same time as the host count, so the two are confounded; separating them needs a four-host run with the new generator, which has not been done. The mechanism is unidentified — the shared accounting path is the candidate, on the strength of both planes behaving alike.");

  foot(s, "Pre-registered before the run, raw on the audit-raw branch: doc/audit/2026-08-25_large-scale-concurrent/ (dee0512). Recount in the same directory.");
  S.pageNum(s);
}

/* ========================================================================
   A reversal we bet on, and the control that killed it
   ======================================================================== */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB1);
  S.pageTitle(s, "A result we pre-registered, and then withdrew",
    "Six cells said the same sample count does not mean the same precision — the control says we cannot tell them apart");

  let y = 2.34;
  [
    ["What the six cells showed",
     "Two levels, each reached from opposite directions. The pairing worked — sample counts matched to 0.84% and 0.44% — and every cell was healthy."],
    ["What was about to be claimed",
     "That two cells with the same sample count are not equivalent, so the whole matrix has to be run. It rested on every pair clearing 0.1, and one pair cleared it by 0.040."],
    ["What the control did to it",
     "Same parameters three times, a full fabric rebuild between each: the spread moved 0.136 on its own, and across the three runs by 0.240. The threshold cannot separate cell from cell."],
  ].forEach(([h, b], i) => {
    S.listItem(s, M, y, 7.35, String(i + 1), h, b);
    y += 1.40;
  });

  S.marginNote(s, 8.55, 2.36, 3.93, 2.15, "The rule that made this decidable",
    "The threshold was written down before the run. Afterwards there was a reading that would have rescued the claim — widen it to 0.24 — and taking it is exactly what pre-registration exists to forbid. That is next round's hypothesis, with its own registration.");

  S.marginNote(s, 8.55, 4.74, 3.93, 1.70, "Why this page is here at all",
    "The reversal had already been written into a draft of this deck. It came out because the control came back — which is worth more than the six cells were.");

  foot(s, "Pre-registration a7c2bd7; result 8d109f2; control c62bf3e. Sample counts still agree to 1.1%, so the spread is in the measurement, not the design.");
  S.pageNum(s);
}

/* ========================================================================
   21 — a boot deadlock in the baseline, fixed
   ======================================================================== */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB1);
  S.pageTitle(s, "A boot deadlock, and a same-boot A/B",
    "Six of ten boots never converged; the dump names two queues full at the same time — mechanism, fix, and the control");

  let y = 2.30;
  [
    ["The dump names the mechanism",
     "Two controller event queues full at once, 12 and 43 senders blocked. The damage is not the stall — it is the kernel's topology poll starving behind it."],
    ["The fix gives two unbounded waits a deadline",
     "Both inside the handler. The evidence required to call a link dead is untouched. A second fix moves the work out of the loop entirely."],
    ["The control is a same-boot A/B, within one hour",
     "Same machine, same defaults, alternating arms — drift is bounded by an hour, not a day."],
  ].forEach(([h, b], i) => {
    S.listItem(s, M, y, 7.35, String(i + 1), h, b);
    y += 1.34;
  });

  table(s, 8.55, 2.32, 3.93,
    [1.35, 0.85, 0.85, 0.88],
    ["arm", "stuck", "fidelity", "invariant"],
    [
      [{ t: "no fix", fs: 9.5 }, { t: "2/3", b: true, c: WARNC }, { t: "1/3", c: WARNC }, { t: "violated", fs: 9, c: WARNC }],
      [{ t: "deadline", fs: 9.5 }, { t: "0/3", b: true, c: ACCENT }, { t: "3/3", b: true, c: ACCENT }, { t: "violated", fs: 9, c: MUTED }],
      [{ t: "out of loop", fs: 9.5 }, { t: "0/3", b: true, c: ACCENT }, { t: "3/3", b: true, c: ACCENT }, { t: "holds", fs: 9, b: true, c: ACCENT }],
    ], { rh: 0.40, hfs: 9.5, fs: 9.5 });

  S.marginNote(s, 8.55, 4.30, 3.93, 1.30, "The key cell is not the zero",
    "It is the run where the block did happen — 28 timeouts — and the poll came back on its own after 148 s. That is the fix working, not the fault being absent.");

  S.marginNote(s, 8.55, 5.78, 3.93, 1.05, "What N = 3 does not buy",
    "At the old rate, three clean runs happen 3.7% of the time by chance. A first verification, not a conclusion.");

  foot(s, "Pre-registered, with both self-tests: doc/audit/2026-08-25_ring-edge-fix/. Fabric: 128 hosts, 288 edges.");
  S.pageNum(s);
}

/* ========================================================================
   22 — section cover 3
   ======================================================================== */
S.sectionCover("2", "Engineering, and what's next",
  "Bring-up as one command, truncation and batching, and what the next report will carry");

/* ========================================================================
   23 — one command brings the lab up
   ======================================================================== */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB2);
  S.pageTitle(s, "One command brings the lab up and checks it",
    "Two data planes start in opposite orders and neither fails loudly when reversed — so this page shows what bring-up now enforces");

  table(s, M, 2.30, 7.55,
    [1.25, 2.05, 4.25],
    ["", "starts first", "and reversing it looks like"],
    [
      [{ t: "OVS" }, { t: "the control plane", fs: 10 },
       { t: "switches dial a dead port; no log line mentions the port, only a topology that never converges", fs: 9.5, c: WARNC }],
      [{ t: "P4" }, { t: "the data plane", fs: 10 },
       { t: "the proxy's first RPC is refused and it exits before opening its own port", fs: 9.5, c: WARNC }],
    ], { rh: 0.52, fs: 10 });

  let y = 3.84;
  [
    ["One number decides everything downstream",
     "Fabric size and the kernel's model both come from the host count. A 128-host fabric beside a 4-host model happened once, silently."],
    ["Bring-up ends by sending a real packet",
     "Not by reading a status page. Ten green switches over a network carrying nothing has happened twice."],
    ["Shutdown proves what it killed",
     "Process start time against the pidfile's write time. Names and argv are useless — every service is exec'd through a wrapper."],
  ].forEach(([h, b], i) => {
    S.listItem(s, M, y, 7.5, String(i + 1), h, b);
    y += 1.05;
  });

  S.marginNote(s, 8.75, 2.32, 3.73, 1.70, "Why this belongs in an experiment talk",
    "Before it, every number carried an unchecked assumption: that the testbed was the shape the operator believed. This is that assumption becoming enforced.");

  S.marginNote(s, 8.75, 4.24, 3.73, 1.50, "No boot times here, on purpose",
    "Ten boots at defaults, six never converged. “How long a successful boot takes” is a floor, not a number — and that defect is the previous page.");

  S.marginNote(s, 8.75, 5.96, 3.73, 1.05, "Stated as unfinished",
    "The claim is a convention, not a lock — it stops the tool's own verbs, not a bare command. Cleanup does not assert what it removed.");

  S.pageNum(s);
}

/* ========================================================================
   Truncation — tried, works, and buys nothing
   ======================================================================== */
S.figurePage(FIG, "page_truncate-bought-nothing.png", 3040 / 1270, TAB2);

// Merge went through its gate at 01:07 on 26 August, so the plan page it used
// to sit on has become a result page too. The two flat panels are the evidence,
// not the decoration — they were written down before the run as the thing that
// would make a 6.87× saving a bug instead of a saving.
S.figurePage(FIG, "page_merge-gate.png", 3040 / 1270, TAB2);

{
  const s = S.newSlide();
  S.sectionTab(s, TAB2);
  S.pageTitle(s, "Truncation and batching, after the experiments",
    "One cut the bytes and bought nothing; the other cuts the datagrams and has not been asked the question yet");

  let y = 2.34;
  [
    ["Truncation works, and buys nothing",
     "5.6× fewer gRPC bytes, nothing silent — 35 distinct readings against the control's 32. Yet all four rates move the wrong way. Per-byte was the registered test, and it is out."],
    ["Merge is wired, and it merges",
     "One variable, batch 1 against 8: datagrams fall 209.8/s → 30.6/s, while the sample count moves 0.8% and the ratio 1.016 → 1.008. Both of those staying flat was the gate."],
    ["Whether it moves the wall is the open question",
     "The gate proves it can be done, not that it helps. If the cost sits on the send side the wall moves; if it sits on the receive side it will not, and the next cut is receive-side concurrency."],
  ].forEach(([h, b], i) => {
    S.listItem(s, M, y, 7.35, String(i + 1), h, b);
    y += 1.42;
  });

  S.marginNote(s, 8.55, 2.36, 3.93, 1.85, "The switch-side knob, for contrast",
    "Truncating the clone inside the switch reads zero on every edge and reports no error at all. Not an optimisation — an outage. That is why emitter-side truncation is a measured necessity rather than a preference.");

  S.marginNote(s, 8.55, 4.44, 3.93, 1.15, "6.87×, not 8×",
    "518 extra datagrams, which is what a 0.2 s age timer flushing part-full batches looks like.");

  S.marginNote(s, 8.55, 5.82, 3.93, 1.00, "One side effect, recorded not explained",
    "Distinct readings 34 → 14. The total is unchanged; the time grain is not.");

  foot(s, "Extern A/B at 9424535; merge gate at gate_e.out, independently recounted. Effect on the sampling ceiling: not measured — the 1-in-8 cell has not been run.");
  S.pageNum(s);
}

/* ========================================================================
   25 — planned for the next report
   ======================================================================== */
{
  const s = S.newSlide();
  S.pageTitle(s, "Planned for the next report",
    "Three again, in the same format — each with the number it starts from and the test that decides it");

  const cols = [
    ["1", "Take the boot-ring result from suggestive to conclusive",
     "0/3 against 2/3, and the second fix holds the invariant outright — 159 stack samples, no violation. Three clean runs happen by chance 3.7% of the time.",
     "Done when the arms reach 0/6 to 0/8 and the boot-success rate is re-measured on the fixed build."],
    ["2", "Finish the third question on its own terms",
     "The binaries can be told apart, which was the prerequisite. Swapping the switch binary changes the timing every layer depends on.",
     "Done when the whole L0–L4 suite passes on the fast build — the test written down on 20 August."],
    ["3", "Ask whether batching moves the ceiling",
     "Merge is wired and through its gate: 6.87× fewer datagrams with the sample count and the ratio both flat. What that buys at the wall is the part nobody has measured.",
     "Done when the 1-in-8 cell — the first rate that loses packets — is run with batching on and off, and the loss either moves or does not."],
  ];

  const cw = (CW - 0.9) / 3;
  cols.forEach(([n, head, body, gate], i) => {
    const x = M + i * (cw + 0.45);
    s.addText(n, { x, y: 2.26, w: 0.32, h: 0.3,
      fontFace: FB, fontSize: 13, bold: true, color: ACCENT, margin: 0 });
    s.addText(head, { x, y: 2.62, w: cw, h: 0.62,
      fontFace: FB, fontSize: 15, bold: true, color: INK, margin: 0, lineSpacingMultiple: 1.1 });
    s.addText(body, { x, y: 3.34, w: cw, h: 1.60,
      fontFace: FB, fontSize: 11.5, color: BODY, margin: 0, lineSpacingMultiple: 1.22 });
    s.addShape("rect", { x, y: 5.10, w: 0.03, h: 0.94, fill: { color: ACCENT }, line: { type: "none" } });
    s.addText(gate, { x: x + 0.24, y: 5.06, w: cw - 0.24, h: 1.02,
      fontFace: FB, fontSize: 11, color: BODY, margin: 0, lineSpacingMultiple: 1.2 });
  });

  foot(s, "Same shape as the 20 August page, so the next report can be checked against it the way this one was.");
  S.pageNum(s);
}

/* ========================================================================
   26 — where it stands
   ======================================================================== */
{
  const s = S.newSlide();
  S.pageTitle(s, "Where it stands",
    "What is settled, what is run but not finished, and what is still unknown");

  s.addText("Settled", { x: M, y: 2.20, w: 5.6, h: 0.3,
    fontFace: FB, fontSize: 14, bold: true, color: ACCENT, margin: 0 });
  s.addShape("line", { x: M, y: 2.54, w: 5.6, h: 0.01, line: { color: RULE, width: 1 } });
  let y = 2.62;
  [
    ["The 128-host failover budget balances",
     "Detection is 87% of it, and the cause is arithmetic: hosts stretch the gap between two probes of one port."],
    ["Detection is 3.9× faster, threshold untouched",
     "One constant. Idle false-positive rate zero across ~10⁵ probe opportunities."],
    ["A sample has a price — on the kernel and the proxy",
     "206 µs per sample inside the range run; flat on the switches across a 4× change in rate."],
    ["Sampling harder stops paying at 1-in-32",
     "Above 1-in-16 it costs throughput instead — 85% of the flow lost at 1-in-1."],
    ["Truncation is not the fix",
     "5.6× fewer bytes moved the ceiling by nothing. The cost is not per byte."],
    ["Under concurrency the twin reads high",
     "Four rounds, three edge classes, and an independent recount agrees. How high is not settled."],
  ].forEach(([h, b]) => {
    // six items now, not five: the body drops to 10.5 so that two lines of it
    // still clear the next heading at a 0.70 pitch. Measured, not guessed.
    s.addText(h, { x: M, y, w: 5.6, h: 0.26,
      fontFace: FB, fontSize: 12.5, bold: true, color: INK, margin: 0 });
    s.addText(b, { x: M, y: y + 0.25, w: 5.6, h: 0.40, valign: "top",
      fontFace: FB, fontSize: 10.5, color: BODY, margin: 0, lineSpacingMultiple: 1.14 });
    y += 0.70;
  });

  const RX = 7.0, RW = 5.48;
  s.addText("Open, and stated as open", { x: RX, y: 2.20, w: RW, h: 0.3,
    fontFace: FB, fontSize: 14, bold: true, color: ACCENT, margin: 0 });
  s.addShape("line", { x: RX, y: 2.54, w: RW, h: 0.01, line: { color: RULE, width: 1 } });

  const open = [
    ["Boot convergence", "six of ten boots at defaults; fix verified at N = 3 only", true],
    ["Fast build as default", "the L0–L4 acceptance run is scheduled, not done", true],
    ["Loaded false positives", "the idle rate is zero; under load it is unmeasured"],
    ["Scale × concurrency", "the direction holds; the size moves 14% between fabric generations"],
    ["The intercept", "206 µs/sample is a marginal cost inside a range, not a ceiling"],
    ["The ceiling's mechanism", "receive-side, per sample — inferred, not identified"],
    ["Batching (merge)", "wired and gated; what it does to the wall is unmeasured", true],
    ["Northbound concurrency", "one lane, measured; not yet a problem, not yet addressed"],
    ["Residual in the budget", "3.6 s across noise and an epoch difference — not explained"],
  ];
  let oy = 2.66;
  open.forEach(([k, v, isNew]) => {
    s.addText(k, { x: RX, y: oy, w: 2.05, h: 0.40, valign: "middle",
      fontFace: FB, fontSize: 11, bold: true, color: isNew ? ACCENT : INK, margin: 0 });
    s.addText(v, { x: RX + 2.08, y: oy, w: RW - 2.38, h: 0.40, valign: "middle",
      fontFace: FB, fontSize: 10.5, color: BODY, margin: 0, lineSpacingMultiple: 1.12 });
    oy += 0.42;
    s.addShape("line", { x: RX, y: oy - 0.04, w: RW - 0.3, h: 0.01, line: { color: "F0F0F0", width: 1 } });
  });

  s.addText("The three marked items are what the next report answers; the rest are in doc/KNOWN-ISSUES.md.", {
    x: RX, y: oy + 0.16, w: RW - 0.3, h: 0.34,
    fontFace: FB, fontSize: 10.5, color: MUTED, margin: 0 });

  S.pageNum(s);
}

pres.writeFile({ fileName: OUT })
  .then(() => console.log("done —", S.currentPage(), "pages"))
  .catch(e => { console.error(e); process.exit(1); });
