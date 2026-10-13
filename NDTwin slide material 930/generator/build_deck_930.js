// NDTwin progress report, 2026-09-30. Thirty-two pages (template v1.8, 2026-09-29).
//
// Built from NDTwin-slide-template-930.md §1 — all 32 rows, ✅ and ○ alike.
// 24 figure pages + 7 table pages + 1 title page.
// 2026-09-29 (Adam): A1, A2, T2, Q1–Q5 and F1 are out (development and debugging
//    history); section B (background: the 13 exercises, basic and basic_tunnel in
//    detail, what the 09-16 NDTwin lacked, how each gap was bridged) comes after A0,
//    and T3 follows B5. The removed pages' figures are on the ARCHIVE list below.
// v1.8 (2026-09-29): R4 and S2 show the final state only (fig_r4 is two rows, one
//    run, aspect 2.563); N3 row 4 cites 30_cycles.tsv and the design bound.
//
// 🔴 Rule 2 of the 930 template (Adam 09-27): one figure OR one table per page,
//    nothing else. No section tab, no kicker, no caption, no chip, no verdict.
//    Figure pages carry no page title (the figure's own canvas title is it);
//    table pages carry the §1 title and the table. Page number stays.
// 🔴 Thirteen figures are archive-only by template §4; they are deliberately
//    NOT placed: the five from 09-27/28 (fig_n1_roadmap_with_detect_only,
//    fig_t1b_requirements_matrix_0927, fig_r1_four_rulings, fig_s4_gui_plan,
//    fig_q3_review_catches) and the eight of the pages removed on 09-29
//    (fig_o1_since_0916, fig_o2_thirteen, fig_t5_arms_by_run, fig_q1_protobuf5,
//    fig_q2_review_path, fig_q4_ci_state, fig_q5_main_by_pr, fig_f1_fixed_since_916).
//
// Speaker notes are taken verbatim from template §2 at build time, so the
// template stays the single source of truth for what is said on each page.
//
// [Co-developed with claude code -- Adam]
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const HERE = __dirname;
const ROOT = HERE + "/..";
const F = ROOT + "/figures/";
const OUT = ROOT + "/NDTwin_deck_930.pptx";
const TEMPLATE = ROOT + "/NDTwin-slide-template-930.md";

const S = require(HERE + "/../../NDTwin slide material 903/generator/deck_style");
const { INK, BODY, MUTED, FAINT, ACCENT, FB, T } = S;

const pres = new pptxgen();
pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
pres.layout = "WIDE";
S.bind(pres);

// ---------------------------------------------------------------- notes (§2)
const md = fs.readFileSync(TEMPLATE, "utf8");
const sec2 = md.split(/^## 2\. /m)[1].split(/^## 3\. /m)[0];
const NOTES = {};
for (const blk of sec2.split(/^### /m).slice(1)) {
  const id = blk.split(/\s/)[0];
  NOTES[id] = blk.split("\n").slice(1).join("\n").trim();
}
function notes(s, id) {
  if (!NOTES[id]) throw new Error("template §2 has no notes for " + id);
  s.addNotes(NOTES[id]);
}

// ---------------------------------------------------------------- helpers
const USED = [];
function fig(id, path, ar) {
  const s = S.newSlide();
  const TOP = 0.28, BOT = 7.00, availH = BOT - TOP, availW = 12.90;
  let w = availW, h = w / ar;
  if (h > availH) { h = availH; w = h * ar; }
  const p = F + path.replace(/\/([^/]+)$/, "/_hires/$1") + ".png";
  if (!fs.existsSync(p)) throw new Error("missing " + p);
  s.addImage({ path: p, x: (13.333 - w) / 2, y: TOP + (availH - h) / 2, w, h });
  USED.push(path);
  notes(s, id);
  S.pageNum(s);
}

const X = 0.62, W = 12.10;
function title(s, text) {
  s.addText(text, { x: X, y: 0.42, w: W, h: 0.66, fontFace: FB, fontSize: 30,
    bold: true, color: INK, margin: 0 });
}
function table(s, y, colW, head, rows, opt) {
  opt = opt || {};
  const hdr = head.map(h => ({ text: h, options: { bold: true, color: "FFFFFF",
    fill: { color: ACCENT }, fontSize: opt.hfs || 15 } }));
  const body = rows.map((r, i) => r.map((cell, j) => ({
    text: cell,
    options: { fill: { color: i % 2 ? "FFFFFF" : "F4F7F9" }, bold: j === 0,
      color: j === 0 ? INK : BODY, fontSize: opt.fs || 16, valign: "middle" },
  })));
  s.addTable([hdr, ...body], {
    x: X, y, w: W, colW,
    rowH: [opt.hh || 0.46, ...rows.map(() => opt.rh || 0.6)],
    border: { type: "solid", color: "DDE4E9", pt: 1 },
    fontFace: FB, valign: "middle", margin: [0.08, 0.14, 0.08, 0.14],
  });
}
function tablePage(id, t, y, colW, head, rows, opt) {
  const s = S.newSlide();
  title(s, t);
  table(s, y, colW, head, rows, opt);
  notes(s, id);
  S.pageNum(s);
}

/* ========================================================== A — opening */
{
  const s = S.newSlide();
  s.addText("NDTwin progress · 2026-09-30", { x: X, y: 2.9, w: W, h: 1.1,
    fontFace: FB, fontSize: 48, bold: true, color: INK, margin: 0 });
  s.addShape("line", { x: X, y: 4.2, w: 1.1, h: 0.01, line: { color: ACCENT, width: 2.5 } });
  s.addText("Adam", { x: X, y: 6.3, w: 6, h: 0.4, fontFace: FB, fontSize: 18,
    color: MUTED, margin: 0 });
  notes(s, "A0");
}
/* ========================================================== B — background (09-29) */
tablePage("B1", "The 13 P4 tutorial exercises", 1.18,
  [1.60, 3.90, 2.95, 3.65],
  ["exercise", "the student writes", "the packet carries", "its tables are filled by"],
  [
    ["basic", "lpm lookup, MAC rewrite, TTL − 1", "IPv4", "sN-runtime.json"],
    ["basic_tunnel", "a tunnel header and its own exact table", "myTunnel 0x1212 + IPv4", "sN-runtime.json"],
    ["calc", "a calculator that answers the sender", "calc header 0x1234", "none: constant entries in the .p4"],
    ["ecn", "ECN marking when the queue is deep", "IPv4, ECN bits", "sN-runtime.json"],
    ["firewall", "a stateful firewall (bloom filter) on s1", "IPv4 + TCP", "sN-runtime.json; s1 has its own program"],
    ["flowcache", "packet-in on a miss; idle timeout", "IPv4; packet-in/out header", "its own controller"],
    ["link_monitor", "probes that collect link utilization", "probe 0x812 + header stacks", "sN-runtime.json"],
    ["load_balance", "a 5-tuple hash picks one of two hosts", "IPv4 + TCP", "sN-runtime.json"],
    ["mri", "per hop: switch ID + queue depth", "IPv4 option + header stack", "sN-runtime.json"],
    ["multicast", "MAC lookup; a miss floods a group", "Ethernet (ARP, IPv4)", "sN-runtime.json + 1 multicast group"],
    ["p4runtime", "a controller that writes tunnel rules", "myTunnel 0x1212 + IPv4", "its own controller"],
    ["qos", "DiffServ marking by protocol", "IPv4, DSCP bits", "sN-runtime.json"],
    ["source_routing", "pop one output port per hop", "route stack 0x1234", "none: the path is in the packet"],
  ], { fs: 13, rh: 0.38, hfs: 14, hh: 0.42 });
fig("B2", "background/fig_b2_basic_walkthrough", 1.932);
fig("B3", "background/fig_b3_basic_tunnel", 1.932);
tablePage("B4", "What the 09-16 NDTwin lacked for them", 1.30,
  [3.10, 4.90, 4.10],
  ["need", "NDTwin on 09-16", "what that blocked"],
  [
    ["own program per switch", "every bmv2 ran ndtwin_switch.p4", "all 13 (firewall: two programs)"],
    ["entries by its own names", "fixed names: ipv4_lpm, flow_5tuple", "9 exercises' start-up entries"],
    ["multicast groups", "no way to write one", "multicast"],
    ["its own topology", "10 switches fixed; hosts by formula; no shaping", "other shapes, 1 switch; ecn/mri queues"],
    ["link up/down detection", "LLDP via packet-out/in: needs ndtwin_switch.p4", "link state on any other program"],
    ["NDTwin routes in its table", "/32 routes into its own ipv4_lpm", "NDTwin routing on its program"],
    ["its own controller", "one fixed election id for every client", "p4runtime, flowcache"],
    ["link usage of its traffic", "samples cloned by ndtwin_switch.p4", "every link rate 0, no error"],
    ["what a switch cannot do", "no capability field", "writes that fail after \"queued\""],
  ], { fs: 15, rh: 0.54, hfs: 15, hh: 0.44 });
tablePage("B5", "How each gap was bridged", 1.18,
  [2.25, 2.60, 2.95, 2.10, 2.20],
  ["need", "decision", "mechanism", "ran live", "not yet"],
  [
    ["own program per switch", "the exercise comes as a package (09-17)", "convert.py → package; ndt up p4 --app", "13/13 exercises (T06)", "—"],
    ["entries by its own names", "names checked before anything starts", "pre-flight; proxy writes by p4info names", "9 exercises, 0 failed", "not done: ternary, range"],
    ["multicast groups", "the package declares them", "proxy writes them over P4Runtime", "multicast: 1 group", "—"],
    ["its own topology", "the package carries it", "ndtwin/topology.json; shaping if declared", "pod, triangle, 5h/3s, 1 switch", "—"],
    ["link up/down detection", "no .p4 change (09-24)", "veth heartbeat from a root helper", "6/6 cuts detected (08)", "not done: p4runtime, flowcache"],
    ["NDTwin routes in its table", "roles: NDTwin owns one table (09-24)", "proxy binds its route writes to it", "basic (07, twice)", "offline: 6 same-shape exercises"],
    ["its own controller", "the proxy stays out", "an adapter points it at the fabric", "p4runtime, flowcache", "—"],
    ["link usage of its traffic", "sample the links, not the program", "tc sampling on switch veths → sFlow", "10/13 (plain IPv4 iperf)", "not run: 3 (drop plain iperf)"],
    ["what a switch cannot do", "capabilities, read once (09-24)", "switch_state → get_graph_data → GUI", "proxy (07, twice)", "kernel: unit tests · GUI: local draft"],
  ], { fs: 12, rh: 0.56, hfs: 13, hh: 0.42 });

/* ========================================================== T — tutorials */
fig("T3", "foreign-p4/fig_a1_foreign_p4_path", 1.932);
fig("T1", "p4-tutorials/fig_t1c_ndtwin_coverage", 1.990);
fig("T4", "p4-tutorials/fig_t6_multicast_end_to_end", 1.904);
fig("T5", "p4-tutorials/fig_t7_preflight_checks", 1.904);
fig("T6", "p4-tutorials/fig_t8_what_you_bring", 2.067);
fig("T7", "p4-tutorials/fig_t9_custom_headers", 2.083);

/* ========================================================== R — roles */
tablePage("R1", "Four rulings on the P4 API shape (09-24)", 1.30,
  [2.95, 3.25, 3.15, 2.75],
  ["ruling (09-24)", "ran live", "offline / read only", "not done yet"],
  [
    ["① owner: ndtwin → NDTwin owns that table",
     "pass path: 0 package entries, 16/16 routes written (07, twice)",
     "refusing package entries: unit test + caught mutant",
     "a live refusal; \"rerouted table derivable from the declaration\""],
    ["② no .p4 changes; root veth heartbeat",
     "owned route tables: detect + reroute (08 H1–H5)",
     "tutorials' own basic.p4 unmodified",
     "external control planes: no heartbeat; worst watchdog phase"],
    ["③ GUI reads capabilities once, greys out",
     "proxy reports capabilities, 4/4 switches, both 07 runs",
     "kernel get_graph_data carries them: unit tests + CI (merged 09-28); GUI draft on a local branch",
     "kernel side on a live fabric; grey-out in a pushed GUI (cut 3, GUI side)"],
    ["④ first cut: 7 same-shape programs, one table",
     "basic only (07, twice)",
     "6 others: convert + pre-flight PASS; 4 other shapes FAIL as intended",
     "the 6 on a fabric; multi-table, tunnel, ternary; no 5-tuple role"],
  ], { fs: 15, rh: 1.28 });
fig("R2", "roles/fig_r2_roles_path", 2.005);
fig("R3", "roles/fig_r3_live07", 2.116);
fig("R4", "roles/fig_r4_capabilities", 2.563);

/* ========================================================== H — heartbeat */
fig("H1", "heartbeat/fig_h0_why_not_lldp", 2.150);
fig("H2", "heartbeat/fig_h0b_heartbeat_path", 2.150);
fig("H3", "heartbeat/fig_h1_one_cut_cycle", 2.380);
fig("H4", "heartbeat/fig_h2_detect_vs_phase", 2.222);
fig("H5", "heartbeat/fig_h3_upper_bound", 2.563);
fig("H6", "heartbeat/fig_h4_forwarding_unchanged", 1.814);

/* ========================================================== D — flow API */
fig("D1", "flow-api/fig_d1_flow_api_matrix", 2.116);
fig("D2", "flow-api/fig_d2_queued_readback", 1.904);

/* ========================================================== S — ndt serve */
fig("S1", "ndt-serve/fig_s1_serve_path", 2.380);
fig("S2", "ndt-serve/fig_s2_security_model", 1.904);
fig("S3", "ndt-serve/fig_s3_cells_and_walks", 2.116);
tablePage("S4", "Where the ndt serve page goes", 1.55,
  [1.75, 3.05, 2.35, 2.45, 2.50],
  ["stage", "stack", "served by", "refresh", "state (UTC)"],
  [
    ["v1", "static HTML + JS + CSS, no build step", "ndt serve, 127.0.0.1 only",
     "manual; job log re-read every 2 s", "merged f186ce98, 09-27 12:35"],
    ["v2", "React · Vite · Tailwind · TypeScript · i18next", "ndt serve, 127.0.0.1 only",
     "every 10 s; paused while measuring", "ruled 09-27; on a branch, no page yet"],
    ["one app with Web-GUI", "Web-GUI's", "undecided", "—", "long-term; not scheduled"],
  ], { fs: 18, rh: 1.45, hfs: 17, hh: 0.52 });

/* ========================================================== M — telemetry */
fig("M1", "telemetry/fig_m1_sampling_error", 2.150);

/* ========================================================== N — close */
fig("N1", "next/fig_n1_roadmap", 2.083);
tablePage("N2", "Open questions", 1.40,
  [3.55, 2.95, 2.80, 2.80],
  ["question", "why we ask", "if yes", "if no"],
  [
    ["next: custom headers, or multi-table roles?", "one person, two roadmap items",
     "observation side table → flow identity", "load_balance template first"],
    ["is \"about 20 s\" link detection enough?", "same class as NDTwin's own LLDP",
     "keep one shared watchdog", "event-driven pass, ≈15.5 s design worst"],
    ["re-measure the pps ceiling?", "not resolvable on this machine",
     "one night, a new preregistration", "report sampling error only"],
    ["ndt serve + Web-GUI as one app: which guard?", "Web-GUI listens on 0.0.0.0:3000",
     "loopback-only Web-GUI", "login or an auth proxy"],
    ["\"bring your own .p4\": what counts as done?", "defines the next cuts",
     "forwarding + link view", "+ per-flow view of its own headers"],
  ], { fs: 16, rh: 0.98, hfs: 16 });
tablePage("N3", "What we do not claim", 1.30,
  [3.35, 4.55, 4.20],
  ["we do not claim", "because", "evidence"],
  [
    ["NDTwin operates any foreign P4", "roles bind one dst-IP table; no link detection under an external controller", "route_binding.py:159-161; h14 log :168"],
    ["the twin observes custom headers", "own-frame evidence only for 0x1212", "T7; GAP-2b §3"],
    ["telemetry lowers the pps ceiling", "no resolution at 20 kpps", "cooperative_f64_a.log :8, :15"],
    ["detection ≤ 20 s, guaranteed", "one watchdog phase sampled", "30_cycles.tsv: phase 1.49–1.76 s only; design bound ≈ 20 s"],
    ["flowcache G1 PASS = delivered", "flow reached s1→s3 only; h3 got nothing", "netdev s3-eth1 +273 B; iperf_server.txt; iperf_client.txt :10"],
    ["the serve GUI ran on the lab", "stub server only", "ndt-serve-gui REPORT :10"],
    ["users already have this work", "the manual's clone target stops at 09-03", "FIXED-SINCE-916 §8–§9"],
  ], { fs: 15, rh: 0.66, hfs: 15, hh: 0.44 });

// ---------------------------------------------------------------- checks
const ARCHIVE = ["next/fig_n1_roadmap_with_detect_only", "p4-tutorials/fig_t1b_requirements_matrix_0927",
  "roles/fig_r1_four_rulings", "ndt-serve/fig_s4_gui_plan", "engineering/fig_q3_review_catches",
  // removed from the deck on 2026-09-29 (Adam: no development or debugging history)
  "overview/fig_o1_since_0916", "overview/fig_o2_thirteen", "p4-tutorials/fig_t5_arms_by_run",
  "engineering/fig_q1_protobuf5", "engineering/fig_q2_review_path", "engineering/fig_q4_ci_state",
  "engineering/fig_q5_main_by_pr", "fixed-since-916/fig_f1_fixed_since_916"];
const onDisk = fs.readdirSync(F, { withFileTypes: true }).filter(d => d.isDirectory())
  .flatMap(d => fs.readdirSync(F + d.name).filter(f => f.endsWith(".png"))
    .map(f => d.name + "/" + f.replace(/\.png$/, "")));
const unaccounted = onDisk.filter(p => !USED.includes(p) && !ARCHIVE.includes(p));
if (unaccounted.length) throw new Error("figures neither used nor archived: " + unaccounted);
if (S.currentPage() !== 32) throw new Error("expected 32 pages, got " + S.currentPage());
console.log(`figures: ${onDisk.length} on disk / ${USED.length} used / ${ARCHIVE.length} archive-only / 0 unaccounted`);

pres.writeFile({ fileName: OUT })
  .then(() => console.log("done — " + S.currentPage() + " pages → " + OUT))
  .catch(e => { console.error(e); process.exit(1); });
