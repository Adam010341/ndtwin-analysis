// The pages 909 adds on top of the 903 deck.
//
// Everything here is specified by NDTwin-slide-template-916.md:
//   §C-909    Q12 — one flag, two meanings
//   §F-909    the 09-04 night round (six findings, figures already rendered)
//   §C-909-T  the P4-tutorials group, T1–T4  (§E-909-T: picture first)
//
// 🔴 Evidence grades are load-bearing on this group and are carried by a chip
// on every page, never by tone:
//   MEASURED    ran it, this round, this binary
//   READ-CODE   derived by reading source — never written like a run
//   RAN ELSEWHERE  the tutorials' own harness, not NDTwin's fabric
// §B-T is explicit that 0/13 exercises have run on an NDTwin fabric, so T4's
// 2×2 says so on the page itself rather than in the script.
//
// T1 uses the rendered heat-map. T2–T4 are drawn here because their figures
// are still 待畫 in §G-909-T, and §E-909-T asks for pictures rather than prose;
// they follow 827 §E4a (architecture) and §E4b (flow) so they read as the same
// family as the deck's other diagrams.
module.exports = function (S, FIG909, HIRES909) {
  const { INK, WARNC, BODY, MUTED, FAINT, RULE, ACCENT, ACCENT_BG, WARN_BG,
          PANEL, FH, FB, FC, M, CW } = S;

  const TAB3 = "3 · ENGINEERING, AND WHAT'S NEXT";

  // a two-word evidence grade, top right, on every page of this group
  function grade(s, text, colour) {
    S.chip(s, M + CW - 2.30, 0.30, 2.30, text, colour || ACCENT);
  }

  function figPage(file, ar, o) {
    o = o || {};
    const s = S.newSlide();
    S.sectionTab(s, TAB3);
    let top = 0.52;
    if (o.title) {
      s.addText(o.title, { x: M, y: 0.44, w: CW - 2.5, h: 0.48,
        fontFace: FH, fontSize: 24, bold: true, color: INK, margin: 0 });
      top = 1.08;
    }
    if (o.kicker) {
      s.addText(o.kicker, { x: M, y: 0.96, w: CW - 2.5, h: 0.30,
        fontFace: FB, fontSize: 14, color: FAINT, margin: 0 });
      top = 1.40;
    }
    const req = o.req || [];
    const bandH = req.length ? 0.36 + req.length * 0.62 : 0;
    const availH = (req.length ? 6.84 - bandH : 7.02) - top;
    let w = CW, h = w / ar;
    if (h > availH) { h = availH; w = h * ar; }
    s.addImage({ path: (o.dir || FIG909) + file,
      x: (13.333 - w) / 2, y: top + (availH - h) / 2, w, h });
    if (req.length) {
      let y = 7.02 - bandH + 0.04;
      s.addShape("line", { x: M, y: y - 0.14, w: CW, h: 0.01,
        line: { color: RULE, width: 1 } });
      req.forEach(([l, v, c]) => {
        S.row(s, M, y, CW, l, v,
          { tick: c || ACCENT, lc: c || ACCENT, lw: o.lw || 3.05,
            fs: 14.5, lfs: 13.5, h: 0.54 });
        y += 0.62;
      });
    }
    if (o.foot) S.footNote(s, o.foot);
    if (o.gradeText) grade(s, o.gradeText, o.gradeColour);
    S.pageNum(s);
    return s;
  }

  /* =====================================================================
     Q12 — one flag, two meanings          (§C-909)
     ===================================================================== */
  function q12() {
    const s = S.newSlide();
    S.sectionTab(s, TAB3);
    S.head(s, "One flag, two meanings",
      "a decision and an observation, sharing one bit");

    // left: who writes is_up, and what they mean by it
    s.addText("WHO WRITES is_up", { x: M, y: 2.06, w: 5.4, h: 0.28,
      fontFace: FB, fontSize: 11.5, bold: true, color: FAINT, margin: 0,
      charSpacing: 0.8 });
    // stacked, not S.row: the label and the value belong on separate lines
    // here, and S.row's label column would have to be absurdly narrow
    [
      ["THE POWER API", "a decision — I commanded it off"],
      ["THE 1 Hz LIVENESS WORKER", "an observation — it answers"],
    ].forEach(([l, v], i) => {
      const y = 2.42 + i * 0.88;
      s.addShape("rect", { x: M, y, w: 0.055, h: 0.72,
        fill: { color: ACCENT }, line: { type: "none" } });
      s.addText(l, { x: M + 0.24, y, w: 5.2, h: 0.32, valign: "middle",
        fontFace: FB, fontSize: 13.5, bold: true, color: ACCENT, margin: 0,
        charSpacing: 0.5 });
      s.addText(v, { x: M + 0.24, y: y + 0.34, w: 5.2, h: 0.36, valign: "top",
        fontFace: FB, fontSize: 16, color: BODY, margin: 0 });
    });
    s.addText("One bit cannot tell “the wall switch is off” from “the bulb burned out”.",
      { x: M + 0.24, y: 4.20, w: 5.4, h: 0.56, valign: "top",
        fontFace: FB, fontSize: 15, bold: true, color: INK, margin: 0,
        lineSpacingMultiple: 1.14 });

    // right: what that cost, measured
    s.addText("WHAT IT COST, MEASURED", { x: 7.05, y: 2.06, w: 5.4, h: 0.28,
      fontFace: FB, fontSize: 11.5, bold: true, color: FAINT, margin: 0,
      charSpacing: 0.8 });
    [
      ["8–13 s", "of “on” after the machine was commanded off — the liveness cache writes it back within 0.3–1.5 s. 18/18 across both arms"],
      ["OFF vs ON", "two switches equally dead: the commanded one reads OFF, the crashed one reads ON. The endpoint reports the order, not the state"],
      ["never fires", "the three-state check for “something died that should not have” reads the same bit on both sides"],
    ].forEach(([n, v], i) => {
      const y = 2.42 + i * 1.24;
      s.addText(n, { x: 7.05, y, w: 2.35, h: 0.52, valign: "middle",
        fontFace: FH, fontSize: 28, bold: true, color: WARNC, margin: 0 });
      s.addText(v, { x: 9.50, y: y - 0.02, w: 2.98, h: 1.10, valign: "top",
        fontFace: FB, fontSize: 12.5, color: BODY, margin: 0,
        lineSpacingMultiple: 1.12 });
    });

    S.row(s, M, 5.34, CW, "RULED",
      "split into admin_state (the command) and reachable (the probe) · is_up stays as an alias for reachable",
      { lw: 1.60, fs: 15.5 });
    S.keyLine(s,
      "Decided, not shipped: the fix is dispatched and not yet on trunk.");
    S.footNote(s,
      "Live two-arm run, 9 each, at 7e8d91e0 (merged 85c1a159); raw at audit-raw 19e3ab88. Ruling recorded at b57736cd.");
    grade(s, "MEASURED", ACCENT);
    S.pageNum(s);
  }

  /* =====================================================================
     The night round — six findings, one page        (§F-909)
     ===================================================================== */
  function nightRound() {
    const s = S.newSlide();
    S.sectionTab(s, TAB3);
    S.head(s, "What the night round found",
      "six endpoints · what they report vs what the switch does");

    [
      ["A LINK COMES BACK", "a link declared down through the API is silently restored by the 30 s topology poll — 21.5–25.4 s. A real cut never restores itself", WARNC],
      ["SHUTDOWN KEEPS WRITING", "“All subsystems stopped. Exiting.” is printed, and 10.7 s of southbound writes follow it — no log line mentions them", WARNC],
      ["A COUNTER COUNTS POSTS", "20 installs of one match: succeeded +20, the switch +1 · 15 deletes of a match that is not there: succeeded +15, the switch +0", WARNC],
      ["A 200 THAT INSTALLED NOTHING", "two reserved group ids answer “200 installed” and never appear in groupdesc · the delete branch of the same code answers 404 honestly", WARNC],
      ["A METRIC THAT NEVER MOVES", "path switch_count is computed from the static model: identical across 12 paths with 8 of 40 switch-to-switch edges down", WARNC],
      ["40× FOR THE SAME WRITE", "meter install 1024 ms against group install 20 ms — both are one OpenFlow write, measured at the client", MUTED],
    ].forEach(([l, v, c], i) => {
      S.row(s, M, 2.16 + i * 0.74, CW, l, v,
        { tick: c, lc: c, lw: 3.55, fs: 13.5, lfs: 13, h: 0.62 });
    });

    S.keyLine(s,
      "Current behaviour only — the fixes were still running when these were taken.");
    S.footNote(s,
      "Kernel cca5e3e4, helper 6685d3a9; trunk 4088b237 / f943de8f by round. Figures and raw logs in figures/overnight-0904/. The shutdown baseline (~2.4 s idle) is read from another round, on another binary, and is marked as such.");
    grade(s, "MEASURED", ACCENT);
    S.pageNum(s);
  }

  /* =====================================================================
     T1 — what the tutorials ask for      (§C-909-T)
     ===================================================================== */
  function t1() {
    figPage("fig_t1_requirements_matrix.png", 4600 / 3300, {
      dir: HIRES909,
      title: "What the tutorials ask for",
      kicker: "13 exercises · 16 capability dimensions · read, not run",
      gradeText: "READ-CODE / NOT RUN", gradeColour: WARNC,
      lw: 3.85,
      req: [
        ["PIPELINE LOAD, NOT FEATURES", "8 of the 13 want one thing: load the .p4 they ship with · 6 of the 16 dimensions only ask whether NDTwin's own program has a feature", ACCENT],
        ["EXACT + LPM ONLY · 1/13 UNCHANGED", "0/13 need meters or digest · only basic runs as-is, and even then the skeleton punts where the exercise drops", WARNC],
      ],
    });
  }

  /* =====================================================================
     T2 / T3 / T4 — the rendered figures
     ---------------------------------------------------------------------
     These three were drawn by hand here on 09-09 because §G-909-T still had
     them as 待畫. They are not any more: make_gap_diagrams.py rendered all
     four at 17:54 on 09-08, and the rendered versions are better in ways that
     matter — the phase legend (three border styles) is on t2, t3a has the
     "no" branch as well as the failure exit, and t4 carries every exercise
     name as a tile instead of one wrapped line. Hand-drawing was the fallback;
     the fallback is withdrawn.
     ===================================================================== */
  function t2() {
    figPage("fig_t2_gap_architecture.png", 6220 / 3500, {
      dir: HIRES909,
      title: "Where the five gaps live",
      kicker: "proxy side and kernel side · sizes are estimates",
      gradeText: "READ-CODE / NOT RUN", gradeColour: WARNC,
      lw: 2.55,
      req: [["NOT ONE LINE WRITTEN", "the badges are estimated sizes, not progress · border style is the phase, and phase three is the sFlow parser", ACCENT]],
      foot: "Read at trunk 1a284f75 · exercises run 09-08 on their own harness. Line counts estimated in GAP-ANALYSIS §1/§3.",
    });
  }

  // two figures side by side: one mechanism read out of the source, one
  // measured in August. The chips under them are not decoration — they are
  // the reason the two may sit on the same page.
  function t3() {
    const s = S.newSlide();
    S.sectionTab(s, TAB3);
    S.head(s, "What only a foreign P4 program reveals",
      "the same p4info on ten switches, for months");

    const AR = 1680 / 1710;
    const h = 4.36, w = h * AR;
    const gap = 0.60;
    const x0 = (13.333 - (2 * w + gap)) / 2;
    s.addImage({ path: HIRES909 + "fig_t3a_silent_zero.png",
      x: x0, y: 1.98, w, h });
    s.addImage({ path: HIRES909 + "fig_t3b_election_wipe.png",
      x: x0 + w + gap, y: 1.98, w, h });

    s.addText("① fields read by position", { x: x0, y: 6.42, w, h: 0.28,
      align: "center", fontFace: FB, fontSize: 13, bold: true, color: INK, margin: 0 });
    s.addText("② two controllers, one switch", { x: x0 + w + gap, y: 6.42, w,
      h: 0.28, align: "center", fontFace: FB, fontSize: 13, bold: true,
      color: INK, margin: 0 });

    S.footNote(s,
      "① line-checked at sflow_emitter.py:425-429,468-470 and p4_client.py:217,222 — the mechanism, not an observation. ② measured 2026-08-13; bmv2 follows the spec throughout.");
    S.pageNum(s);
  }

  function t4() {
    figPage("fig_t4_phases.png", 6220 / 2800, {
      dir: HIRES909,
      title: "Three phases to a regression gate",
      kicker: "~675 lines · the gate opens after phase two",
      gradeText: "MIXED — SEE CHIPS", gradeColour: WARNC,
      lw: 3.15,
      req: [
        ["0 OF 13 ON NDTWIN", "the 2×2 ran on the tutorials' own harness with their switch binary — it shows the exercises behave as expected, not that NDTwin can host them", WARNC],
        ["WHY THE SKELETONS", "an expected failure, observed · a gate nobody has seen go red is not a gate", ACCENT],
      ],
      foot: "Line counts estimated in GAP-ANALYSIS §6. Runs 09-08 with /usr/local/bin/simple_switch_grpc (327fa7d1), not the NDTwin build.",
    });
  }

  return { q12, nightRound, t1, t2, t3, t4 };
};
