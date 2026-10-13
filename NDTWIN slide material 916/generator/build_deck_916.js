// NDTwin progress report, 2026-09-16. Forty-seven pages.
//
// Built from NDTwin-slide-template-916.md §1 — the FULL inventory, not the ✅
// subset. §1 offers 26 ✅ rows and marks the rest ○, then says the final cut is
// Adam's; Adam's cut is "every figure in figures/ is used". All 43 drafts are on
// a page, and the only pairing is t3a/t3b, which were drawn to sit together. This deck covers
// the 09-09 report that never got delivered *and* the 09-16 material, which is
// exactly what §1's inventory already is — §0 rule 1 voids the 31-page 909 deck
// because it carried 903's 23 pages forward, not because its own six pages were
// wrong. Those six are all still here, inside the seven-segment order.
//
// 🔴 RULE 6 (Adam 09-15, standing) governs every page: a slide may contain only
//    a table, a large heading, an architecture diagram, or a data visualisation.
//    Prose, bullets, subtitles, captions, kickers, chips and verdicts are out —
//    they go in the speaker notes. So, against the 903/909 decks:
//      · S.head() is called with no kicker anywhere;
//      · no keyLine(), no chip() outside a figure's own canvas;
//      · label→value rows survive only because a label and a value ARE the two
//        columns of a table — which is rule 6's own stated escape hatch.
//
// 🔴 RULE 2: a figure page is the figure. No caption, no kicker, no verdict.
//    Every figure here carries its own title inside the canvas, so the page adds
//    no second title — that would be both a duplicate and a rule-2 breach.
//    The only text on a figure page is the section tab and the page number.
//
// Figures are used at their _hires/ resolution (pdftoppm -r 500 of the committed
// PDF) wherever one exists, so nothing is upscaled.
const pptxgen = require("pptxgenjs");

const HERE = __dirname;
const F = HERE + "/../figures/";
const OUT = HERE + "/../NDTwin_deck_916.pptx";

// one shared deck_style instance: the automatic page counter lives inside it
const S = require(HERE + "/../../NDTwin slide material 903/generator/deck_style");
const { INK, WARNC, BODY, MUTED, FAINT, RULE, ACCENT, ACCENT_BG, PANEL,
        FH, FB, FC, M, CW, T } = S;

const pres = new pptxgen();
pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
pres.layout = "WIDE";
S.bind(pres);

// The seven segments of §1. The tab is on every content page rather than on
// four cover pages, and one of them does a job no cover could: §6d and §0.3
// both warn that the professor will otherwise hear "we fixed their system"
// when half of section D/F is our own tooling. The tab says so continuously.
const TAB = {
  A: "REQUIREMENTS DRIVE THE TESTS",
  B: "1 · REQUIREMENTS FROM OUTSIDE PROGRAMS",
  C: "2 · REQUIREMENTS FROM OUTSIDE PEOPLE",
  D: "3 · WHAT THE ROLES FOUND",
  E: "4 · BASELINE DEFECTS WE FIXED",
  // The 09-04 night round is current-behaviour only: the binaries were never
  // rebuilt, so every one of those figures shows the machine BEFORE the fix —
  // and two of the fixes (B-6, #54) have since merged and shipped. Rule 6 bans
  // a caption that would say so, so the scope goes in the tab, which is the one
  // piece of furniture already on every page.
  E2: "4b · MEASURED 09-04 · BEFORE THE FIX",
  F: "5 · THE TOOL WE BUILT — NOT BASELINE",
  G: "6 · WHERE IT STANDS",
};

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
        valign: "top",
      },
    };
  }));
  s.addTable([hdr, ...body], {
    x, y, w, colW,
    rowH: [opt.hh || 0.40, ...rows.map(() => opt.rh || 0.52)],
    border: { type: "solid", color: "E4EAEE", pt: 1 },
    fontFace: FB, valign: "top", margin: [0.09, 0.13, 0.09, 0.13],
  });
}

// Two figures on one page, same height, as the pair was designed. Splitting them
// was considered and rejected: both are ar ~0.98, so alone each is still
// height-limited to 6.24" tall and 6.1" wide — exactly the width it gets here.
// The split would have cost a page and bought nothing.
function figPair(tab, dir, a, b, ar) {
  const s = S.newSlide();
  S.sectionTab(s, tab);
  const TOP = 0.60, h = 6.24, w = h * ar, gap = 0.30;
  const x0 = (13.333 - (2 * w + gap)) / 2;
  s.addImage({ path: F + dir + "/_hires/" + a + ".png", x: x0, y: TOP, w, h });
  s.addImage({ path: F + dir + "/_hires/" + b + ".png", x: x0 + w + gap, y: TOP, w, h });
  S.pageNum(s);
}

// A figure page: the figure, as large as the slide allows, and nothing else.
// `dir` is the folder under figures/; `hires` picks the 500-dpi rasterisation.
function fig(tab, dir, name, ar, hires) {
  const s = S.newSlide();
  S.sectionTab(s, tab);
  const TOP = 0.60, BOT = 6.84;
  const availH = BOT - TOP, availW = 12.60;
  let w = availW, h = w / ar;
  if (h > availH) { h = availH; w = h * ar; }
  s.addImage({
    path: F + dir + "/" + (hires === false ? "" : "_hires/") + name + ".png",
    x: (13.333 - w) / 2, y: TOP + (availH - h) / 2, w, h,
  });
  S.pageNum(s);
}

function foot(s, text) {
  s.addText(text, { x: M, y: 6.94, w: CW - 0.75, h: 0.32,
    fontFace: FB, fontSize: 11.5, color: FAINT, margin: 0 });
}

/* =========================================================================
   A1 — title
   ========================================================================= */
{
  const s = S.newSlide();
  s.addText("NDTwin Network Digital Twin", {
    x: M, y: 2.16, w: 11.6, h: 0.44,
    fontFace: FB, fontSize: 17, color: ACCENT, margin: 0, charSpacing: 1.2 });
  s.addText("Let the Outside Decide What to Test", {
    x: M, y: 2.70, w: 11.8, h: 1.06,
    fontFace: FH, fontSize: 46, bold: true, color: INK, margin: 0 });
  s.addShape("line", { x: M, y: 4.36, w: 1.1, h: 0.01,
    line: { color: ACCENT, width: 2 } });
  s.addText("Adam　·　2026-09-16", {
    x: M, y: 6.42, w: 8.0, h: 0.34,
    fontFace: FB, fontSize: 14, color: MUTED, margin: 0 });
}

/* =========================================================================
   A2 — the thesis, as one table  (§1b)
   ========================================================================= */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB.A);
  S.head(s, "Requirements drive the tests", null);

  table(s, M, 2.10, CW, [2.55, 3.35, 3.05, 2.68],
    ["the requirement comes from", "what it is", "what it drives", "what it found"],
    [
      ["OUTSIDE PROGRAMS",
       "13 exercises in p4lang/tutorials — written by other people, and not for us",
       "each exercise against 16 capability dimensions, then NDTwin against the same 16",
       "5 real gaps · 2 findings only a foreign program exposes"],
      ["OUTSIDE PEOPLE",
       "six operators' motives — inherit, rush a paper, follow the handbook, collide, push traffic, restart",
       "send each one at the machine and watch which untested pair of assumptions it crosses",
       "two nights · 11 rounds · dozens of defects"],
    ], { rh: 1.70, fs: 15 });

  table(s, M, 5.86, CW, [2.55, 9.08],
    ["the claim", ""],
    [["WHY IT WORKS",
      "a test we write walks the path its author already thought of — an outside requirement walks somewhere else, and that is where the defects live"]],
    { rh: 0.78, fs: 15, hh: 0.36 });

  S.pageNum(s);
}

/* =========================================================================
   B — requirements from outside programs   (§5)
   ========================================================================= */
// re-rendered 09-16 at slide proportions: see the generator's own note
fig(TAB.B, "p4-tutorials", "fig_t1_requirements_matrix", 6650 / 3300);
fig(TAB.B, "p4-tutorials", "fig_t2_gap_architecture", 6220 / 3500);
figPair(TAB.B, "p4-tutorials", "fig_t3a_silent_zero", "fig_t3b_election_wipe",
        2800 / 2850);
fig(TAB.B, "p4-tutorials", "fig_t4_phases", 6220 / 2800);

/* =========================================================================
   C — requirements from outside people   (§6b, §6c)
   ========================================================================= */
fig(TAB.C, "overnight-hunt", "fig_m1_hunt_pipeline", 3732 / 1890, false);
fig(TAB.C, "overnight-hunt", "fig_m2_persona_axis", 3732 / 2202, false);
[["fig_f1_successor_first", 3732 / 996],
 ["fig_f2_successor_verify", 3732 / 1206],
 ["fig_f3_restart_cycler", 3732 / 1206],
 ["fig_f4_second_operator", 3732 / 1206],
 ["fig_f5_traffic_pusher", 3732 / 1206],
 ["fig_f6_grad_student", 3732 / 996],
 ["fig_f7_manual_follower", 3732 / 996]]
  .forEach(([n, ar]) => fig(TAB.C, "overnight-hunt", n, ar, false));

/* =========================================================================
   D — what the roles found   (§6d)
   ========================================================================= */
// §1 order D1..D5. Four of the five are our own ndt tooling and only r3 is
// inherited baseline (§0.3) — that is what the tab is for.
fig(TAB.D, "overnight-hunt", "fig_r2_empty_but_confident", 3732 / 1770, false);
fig(TAB.D, "overnight-hunt", "fig_r3_two_doors_one_field", 3732 / 1566, false);
fig(TAB.D, "overnight-hunt", "fig_r4_claim_race_window", 3732 / 1776, false);
fig(TAB.D, "overnight-hunt", "fig_r12_stolen_marker", 3732 / 1704, false);
fig(TAB.D, "overnight-hunt", "fig_r10_sampling_instant", 3732 / 1890, false);

/* =========================================================================
   E1 — Q12, rebuilt as two tables   (§3, and rule 6's explicit instruction)
   ========================================================================= */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB.E);
  S.head(s, "One flag, two meanings", null);

  table(s, M, 2.10, CW, [5.35, 6.28],
    ["who writes is_up", "what they mean by it"],
    [
      ["the power API — powerOff, after the helper confirms the process is dead",
       "a decision: I commanded it off"],
      ["the 1 Hz liveness worker, and the topology poll",
       "an observation: it answers"],
    ], { rh: 0.62, fs: 15.5 });

  table(s, M, 3.86, CW, [5.35, 6.28],
    ["what one bit cost", "measured"],
    [
      ["is_up written back to true", "0.3–1.5 s after the command"],
      ["and it stays true", "8–13 s · 18 of 18 across both arms"],
      ["two equally dead switches", "commanded reads OFF · crashed reads ON"],
      ["the check for “something died”", "reads the same bit on both sides — it can never fire"],
      ["the ruling", "admin_state (command) + reachable (probe)"],
      ["status", "on trunk since 09-05, and published"],
    ], { rh: 0.42, hh: 0.36, fs: 15 });

  foot(s, "Live two-arm run, 9 each, at 7e8d91e0 (merged 85c1a159); raw at audit-raw 19e3ab88. Ruling at b57736cd; on trunk via cdc8dad9.");
  S.pageNum(s);
}

/* =========================================================================
   E2–E9 — the baseline defects we fixed   (§6e)
   ========================================================================= */
[["fig_b02_loss_ladder", 3732 / 1944],
 ["fig_b04_poll_resurrects", 3732 / 1608],
 ["fig_b07_nothing_goes_down", 3732 / 1686],
 ["fig_b08_delete_reports_gone", 3732 / 1542],
 ["fig_b09_ghost_rule", 3732 / 1482],
 ["fig_b10_accidentally_right", 3732 / 1854],
 ["fig_b11_counter_cover", 3732 / 1812],
 ["fig_b_topology_doors", 3732 / 2202]]
  .forEach(([n, ar]) => fig(TAB.E, "baseline-bugs", n, ar, false));

/* =========================================================================
   E10+ — the 09-04 night round   (§4).  fig5 is not here: §1 files it under
   G4, "found but not fixed", and that is where it goes.
   ========================================================================= */
[["fig1_declared_vs_real_link_failure", 3793 / 2448],
 ["fig2_shutdown_southbound_writes", 4250 / 1748],
 ["fig3_dispatch_counters_vs_switch_truth", 3247 / 2254],
 ["fig6_endpoint_latency_profile", 3737 / 3140]]
  .forEach(([n, ar]) => fig(TAB.E2, "overnight-0904", n, ar));
// fig4 is the exception in that batch and so it does not take that tab: it is
// the one figure of the six that carries an after side (kernel 4c9e0be1), so
// "before the fix" would be false on it. It sits under the E tab instead.
fig(TAB.E, "overnight-0904", "fig4_group_install_delete_readback", 5316 / 2690);

/* =========================================================================
   F1–F9 — the ndt commands   (§6f)
   ========================================================================= */
[["fig_c1_up", 3732 / 2154],
 ["fig_c2_down", 3732 / 1902],
 ["fig_c3_status", 3732 / 1902],
 ["fig_c4_clean", 3732 / 1494],
 ["fig_c5_check", 3732 / 1218],
 ["fig_c6_apps", 3732 / 2028],
 ["fig_c7_ntg", 3732 / 1374],
 ["fig_c8_claim", 3732 / 1902],
 ["fig_c9_release", 3732 / 1218]]
  .forEach(([n, ar]) => fig(TAB.F, "ndt-commands", n, ar, false));

/* =========================================================================
   G1 — the board (regenerated 09-16: see the figure's own script header)
   ========================================================================= */
fig(TAB.G, "fixed-since-903", "fig_h1_fixed_since_903", 3732 / 1890, false);

/* =========================================================================
   G2 — where it stands   (§6)
   ========================================================================= */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB.G);
  S.head(s, "Where it stands", null);

  table(s, M, 2.30, CW, [4.05, 7.58],
    ["", ""],
    [
      ["104 fixes", "on trunk, and on the default branch of both public repositories"],
      ["0 branches", "waiting — the 29 that were open on 09-08 all merged on 09-10"],
      ["phase 1 · ~140 lines", "unlocks basic: the first tutorial exercise that would run unchanged"],
    ], { rh: 0.86, fs: 17, hh: 0.10 });

  foot(s, "Public status cross-checked two ways on 09-15: unauthenticated compare API reports behind_by 0 for both repositories. A single git ls-remote returned a stale answer and is not sufficient on its own.");
  S.pageNum(s);
}

/* =========================================================================
   G3 — what the method admits about itself   (§6b, the honesty page)
   ========================================================================= */
{
  const s = S.newSlide();
  S.sectionTab(s, TAB.G);
  S.head(s, "What this method admits about itself", null);

  table(s, M, 2.06, CW, [4.75, 6.88],
    ["the limit", "in its own words"],
    [
      ["reconnaissance guesses wrong a lot",
       "hypotheses are read out of source by an agent that has run nothing · 09-11: 27 confirmed, 12 refuted, 8 unreachable"],
      ["instruments certify themselves",
       "three in one night — a miscount, a colour code splitting a token, a scan matching itself ⇒ prove the instrument can see a known thing before believing its zero"],
      ["a fix can be worse than the defect",
       "one rewrote the note to read “lab free”, so the lab declared itself empty while carrying traffic"],
      ["green does not mean verified",
       "“a grid read as the fixes are verified is worse than no grid” — the coverage table answers who is fixing, not whether it is fixed"],
      ["coverage skews toward what we were told",
       "if a whole night's findings land inside the five things he pointed at, the tests only walked his path"],
      ["most role findings are not independently re-run",
       "the live numbers are the role's own; the person filing them did not repeat the measurement"],
      ["the dispatches and raw are not in version control",
       "scratch/ is git-ignored, so this batch's tickets, reports and logs do not travel with the repository"],
    ], { rh: 0.62, fs: 14 });

  S.pageNum(s);
}

/* =========================================================================
   G4 — found, and not fixed   (§1)
   ========================================================================= */
fig(TAB.G, "overnight-0904", "fig5_path_switch_count_static", 3496 / 2950);

pres.writeFile({ fileName: OUT })
  .then(() => console.log("done —", S.currentPage(), "pages"))
  .catch(e => { console.error(e); process.exit(1); });
