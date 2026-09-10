// Two replacement pages, drawn in the architecture-diagram style:
//   1. Liveness  — how the twin decides a bmv2 switch is alive
//   2. Failover  — what turns a missing beacon into a new route
// Both are the real control flow, read out of
//   DeviceConfigurationAndPowerManager.cpp (p4LivenessFor)
//   p4_proxy/proxy_agent/topology_manager.py (check_link_beacons, run_watchdog_pass)
const pptxgen = require("pptxgenjs");

const ACCENT = "065A82";
const ACCENT_BG = "EEF3F6";
const PANEL = "F7F8F9";
const MUTED = "4F4F4F";
const WARNC = "9C3B2E";
const AF = "Arial";
const FC = "Courier New";
const LINE = "000000";

const pres = new pptxgen();
pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
pres.layout = "WIDE";

function box(s, x, y, w, h, o) {
  o = o || {};
  s.addShape("rect", {
    x, y, w, h,
    fill: { color: o.fill || "FFFFFF" },
    line: { color: o.line || LINE, width: o.lw || 1, dashType: o.dash || "solid" },
  });
}
function txt(s, x, y, w, h, text, o) {
  o = o || {};
  s.addText(text, {
    x, y, w, h, align: o.align || "left", valign: o.valign || "middle",
    fontFace: o.ff || AF, fontSize: o.fs || 10, bold: !!o.bold,
    color: o.tc || "000000", margin: 0, lineSpacingMultiple: o.ls || 0.95,
  });
}
function arrow(s, x, y, w, h, dir, o) {
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
function dash(s, x, y, w, h) {
  s.addShape("line", { x, y, w, h, line: { color: "808080", width: 1, dashType: "dash" } });
}
function header(s, title, sub) {
  txt(s, 0.45, 0.50, 11.5, 0.34, title, { fs: 15, bold: true });
  txt(s, 0.45, 0.84, 12.0, 0.26, sub, { fs: 9.5, tc: MUTED });
}
// a step in the flow: heading line, then detail
function step(s, x, y, w, h, head, detail, o) {
  o = o || {};
  box(s, x, y, w, h, { fill: o.fill || "FFFFFF", line: o.line || LINE, lw: o.lw || 1 });
  if (detail) {
    txt(s, x + 0.14, y + 0.05, w - 0.28, h * 0.46, head,
      { fs: o.hfs || 10, bold: true, tc: o.tc || "000000", ff: o.hff || AF, valign: "middle" });
    txt(s, x + 0.14, y + h * 0.46, w - 0.28, h * 0.50 - 0.02, detail,
      { fs: o.dfs || 8, tc: MUTED, valign: "top", ls: 0.94 });
  } else {
    txt(s, x + 0.14, y, w - 0.28, h, head,
      { fs: o.hfs || 10, bold: true, tc: o.tc || "000000", ff: o.hff || AF, align: o.align || "left" });
  }
}
// a yes/no test: same box, but the condition is set in code face
function test(s, x, y, w, h, cond, note) {
  box(s, x, y, w, h, { fill: PANEL, lw: 1.25 });
  txt(s, x + 0.14, y + 0.04, w - 0.28, h * 0.52, cond, { fs: 9.5, bold: true, ff: FC, valign: "middle" });
  if (note) txt(s, x + 0.14, y + h * 0.52, w - 0.28, h * 0.44, note, { fs: 8, tc: MUTED, valign: "top", ls: 0.94 });
}
function branch(s, x, y, label, o) {
  o = o || {};
  txt(s, x, y, o.w || 0.42, o.h || 0.16, label, { fs: 7.5, tc: o.tc || MUTED, align: o.align || "left" });
}

/* ======================================================================
   Slide 1 — Liveness
   ====================================================================== */
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  header(s,
    "Liveness: how the twin decides a bmv2 switch is alive",
    "Two independent kinds of evidence, and a verdict that is allowed to come back “cannot tell”");

  // ---- evidence, gathered by the proxy ----
  txt(s, 0.85, 1.12, 5.0, 0.20, "GATHERED BY THE PROXY", { fs: 7.5, tc: ACCENT, bold: true });
  step(s, 0.85, 1.34, 4.60, 0.62, "p4_client.probe()  — every 2 s",
    "GetForwardingPipelineConfig with COOKIE_ONLY: the cheapest request P4Runtime has,\nand a real answer from the switch.   →  probe_ok, probe_age_s",
    { fill: ACCENT_BG, line: ACCENT, lw: 1.25, hff: FC, hfs: 9.5, tc: ACCENT, dfs: 7.5 });
  step(s, 6.05, 1.34, 4.60, 0.62, "an LLDP beacon arrives",
    "packet_in with reason = LLDP, recorded unconditionally rather than\nonly when the edge is new.   →  last_lldp_age_s",
    { fill: ACCENT_BG, line: ACCENT, lw: 1.25, hff: FC, hfs: 9.5, tc: ACCENT, dfs: 7.5 });

  arrow(s, 3.15, 1.96, 0, 0.20, "plain");
  arrow(s, 8.35, 1.96, 0, 0.20, "plain");
  arrow(s, 3.15, 2.16, 5.20, 0, "plain");
  arrow(s, 5.75, 2.16, 0, 0.22, "down");

  step(s, 3.30, 2.38, 4.90, 0.38, "GET /p4/switch_state   —   evidence, not a verdict", null,
    { fill: ACCENT_BG, line: ACCENT, lw: 1.25, hff: FC, hfs: 9.5, tc: ACCENT, align: "center" });

  arrow(s, 5.75, 2.76, 0, 0.26, "down");
  txt(s, 5.92, 2.76, 4.4, 0.24, "the kernel polls this and decides — nothing above this line changes",
    { fs: 7.5, tc: MUTED });

  dash(s, 0.45, 3.02, 12.53, 0);
  txt(s, 8.30, 3.08, 4.20, 0.20, "DECIDED BY THE KERNEL", { fs: 7.5, tc: "000000", bold: true, align: "right" });

  // ---- the decision chain ----
  const TX = 1.55, TW = 4.30, VX = 7.55, VW = 2.20, NX = 10.05, NW = 2.45;
  const rows = [
    ["probe_ok  is absent or not a boolean",
     "no probe of this switch has completed yet",
     "UNKNOWN", MUTED,
     "Reporting Down here would mark the whole fabric dead for the first seconds of every run."],
    ["probe_ok == true",
     "an RPC was round-tripped",
     "UP", ACCENT,
     "The only signal that proves a bmv2 process is serving. gRPC channel state was rejected: it sits in IDLE until something forces a connection."],
    ["probe_age_s  >  15 s",
     "kProbeStaleSeconds — the last probe result is stale",
     "UNKNOWN", MUTED,
     "The proxy’s poller has stalled. That is a fact about the poller, not about the switch."],
    ["last_lldp_age_s  ≤  12 s",
     "kLldpFreshSeconds — a beacon arrived after the probe failed",
     "UNKNOWN", MUTED,
     "bmv2 can answer control-plane RPCs while forwarding badly, and a loaded switch can miss one deadline while forwarding well. Fresh beacon against failed probe is a disagreement, not a verdict."],
  ];

  let y = 3.30;
  const PITCH = 0.78, H = 0.54;
  rows.forEach(([cond, note, verdict, vc, why], i) => {
    test(s, TX, y, TW, H, cond, note);
    // the branch that leaves the chain
    arrow(s, TX + TW, y + H / 2, VX - (TX + TW), 0, "right");
    branch(s, TX + TW + 0.10, y + H / 2 - 0.22, i === 1 ? "yes" : (i === 0 ? "yes" : "yes"));
    box(s, VX, y + H / 2 - 0.20, VW, 0.40, { line: vc, lw: verdict === "UP" ? 1.6 : 1.1, fill: verdict === "UP" ? ACCENT_BG : "FFFFFF" });
    txt(s, VX, y + H / 2 - 0.20, VW, 0.40, verdict, { fs: 10.5, bold: true, tc: vc, align: "center" });
    txt(s, NX, y + H / 2 - 0.34, NW, 0.68, why, { fs: 7.5, tc: MUTED, ls: 0.94 });
    if (i < rows.length) {
      arrow(s, TX + TW / 2, y + H, 0, PITCH - H, "down");
      branch(s, TX + TW / 2 + 0.08, y + H + 0.02, "no");
    }
    y += PITCH;
  });

  // terminal
  box(s, TX, y, TW, 0.44, { line: WARNC, lw: 1.6 });
  txt(s, TX, y, TW, 0.44, "DOWN   —   asked, and nothing else disagreed",
    { fs: 10.5, bold: true, tc: WARNC, align: "center" });
  txt(s, NX, y - 0.08, NW, 0.60,
    "Four ways to fail to know, and only one way to be told a switch is dead.",
    { fs: 7.5, tc: MUTED, ls: 0.94 });

  // ---- what each verdict does to the graph ----
  box(s, 0.85, 6.92, 11.65, 0.38, { fill: PANEL, line: "D0D0D0" });
  txt(s, 1.05, 6.92, 3.4, 0.38, "Up  →  setVertexUp", { fs: 9, ff: FC, tc: ACCENT });
  txt(s, 4.45, 6.92, 3.4, 0.38, "Down  →  setVertexDown", { fs: 9, ff: FC, tc: WARNC });
  txt(s, 7.85, 6.92, 4.5, 0.38, "Unknown  →  the graph is not touched", { fs: 9, ff: FC, tc: "000000", bold: true });
}

/* ======================================================================
   Slide 2 — Failover
   ====================================================================== */
{
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  header(s,
    "Failover: what turns a missing beacon into a new route",
    "bmv2 raises no link-down signal, so the absence of a packet the proxy sent itself is the only evidence there is");

  const SX = 1.10, SW = 6.60, NX = 8.20, NW = 4.30;
  let y = 1.06;
  const P = 0.72;

  // 1
  step(s, SX, y, SW, 0.56, "Beacon out   —   every 5 s",
    "TopologyManager sends one LLDP frame out of every port of every switch, as a packet_out.",
    { fill: ACCENT_BG, line: ACCENT, lw: 1.25, tc: ACCENT });
  arrow(s, SX + SW / 2, y + 0.56, 0, P - 0.56, "down"); y += P;

  // 2
  step(s, SX, y, SW, 0.56, "Beacon in",
    "The neighbour’s pipeline sends it to the CPU port. It arrives as packet_in with reason = LLDP,\nand stamps the arrival time of that one link direction.",
    { fill: ACCENT_BG, line: ACCENT, lw: 1.25, tc: ACCENT });
  arrow(s, SX + SW / 2, y + 0.56, 0, P - 0.56, "down"); y += P;

  // 3 — the watchdog loop
  const WD_Y = y;
  step(s, SX, y, SW, 0.42, "Watchdog pass   —   every 5 s", null, { fill: PANEL });
  arrow(s, SX + SW / 2, y + 0.42, 0, P - 0.42, "down"); y += P;

  // 4 — the timeout test
  const T1_Y = y;
  test(s, SX, y, SW, 0.56, "now  −  last beacon   >   15 s   ?",
    "Three missed beacons. A link that has never spoken at all gets 30 s instead.");
  txt(s, NX, y - 0.10, NW, 0.90,
    "Why three and not one. One interval of tolerance would report a failure every time a scan landed just before a beacon did — and a flapping link report is worse than a slow one, because each one tears the edge out of the graph and recomputes every path.",
    { fs: 7.5, tc: MUTED, ls: 0.94 });
  // the "no" branch loops back to the watchdog
  arrow(s, SX, T1_Y + 0.28, -0.42, 0, "plain", { flipH: true });
  s.addShape("line", { x: SX - 0.42, y: T1_Y + 0.28, w: 0.42, h: 0, line: { color: LINE, width: 1.1 } });
  s.addShape("line", { x: SX - 0.42, y: WD_Y + 0.21, w: 0, h: T1_Y + 0.28 - (WD_Y + 0.21), line: { color: LINE, width: 1.1 } });
  arrow(s, SX - 0.42, WD_Y + 0.21, 0.42, 0, "right");
  branch(s, SX - 0.40, T1_Y + 0.06, "no", { w: 0.40 });
  arrow(s, SX + SW / 2, y + 0.56, 0, P - 0.56, "down");
  branch(s, SX + SW / 2 + 0.08, y + 0.58, "yes", { h: 0.15 }); y += P;

  // 5 — belief flips, kernel is told
  step(s, SX, y, SW, 0.56, "The link’s belief flips to down, and the kernel is told",
    "POST /ndt/link_failure_detected, retried on every following pass until the kernel accepts it — a kernel\nthat happened to be restarting would otherwise cost the notification permanently.");
  arrow(s, SX + SW / 2, y + 0.56, 0, P - 0.56, "down"); y += P;

  // 6 — the over-reporting test
  const T2_Y = y;
  test(s, SX, y, SW, 0.60, "every inbound link of that switch went quiet, and  probe_ok  is still true  ?",
    "Then this is a switch-level symptom, not a link failure — report it, but leave its links in the routing graph.");
  arrow(s, SX + SW, y + 0.30, 0.38, 0, "right");
  branch(s, SX + SW + 0.04, y + 0.06, "yes");
  box(s, SX + SW + 0.38, y + 0.08, 2.05, 0.44, { line: WARNC, lw: 1.35 });
  txt(s, SX + SW + 0.38, y + 0.08, 2.05, 0.44, "reported, not rerouted",
    { fs: 9, bold: true, tc: WARNC, align: "center" });
  txt(s, 10.30, y - 0.30, 2.20, 1.40,
    "The one measured failure mode. Taking a bmv2 interface down stalls that switch’s whole packet-in path, so every link into it falls silent at once — one real break produced five down directions, three of them healthy links whose beacons simply had nowhere to be delivered. Reporting may over-report safely; reprogramming may not.",
    { fs: 7, tc: MUTED, ls: 0.94 });
  arrow(s, SX + SW / 2, y + 0.60, 0, P - 0.60, "down");
  branch(s, SX + SW / 2 + 0.08, y + 0.61, "no", { h: 0.13 }); y += P;

  // 7 — reprogram
  step(s, SX, y, SW, 0.56, "install_initial_routes()   —   reprogram first",
    "BFS over the graph with the down endpoints removed, so a reinstall cannot recompute the same route\nback into the broken link. insert_ipv4_route falls back to MODIFY, so the pass is idempotent.",
    { fill: ACCENT_BG, line: ACCENT, lw: 1.25, tc: ACCENT, hff: FC, hfs: 9.5 });
  arrow(s, SX + SW / 2, y + 0.56, 0, P - 0.56, "down"); y += P;

  // 8 — announce
  step(s, SX, y, SW, 0.52, "push_destination_paths()   —   announce second",
    "POST /ndt/inform_all_destination_paths. The kernel’s own pull runs every 60 s, so this only buys latency.",
    { fill: ACCENT_BG, line: ACCENT, lw: 1.25, tc: ACCENT, hff: FC, hfs: 9.5 });
  txt(s, NX, y - 0.22, NW, 0.96,
    "The order is the point. The push advertises the routes that are installed, so announcing first would publish a snapshot that is honest and already out of date — and the corrected one would not arrive until the next transition.",
    { fs: 7.5, tc: MUTED, ls: 0.94 });

  // ---- the detection budget ----
  box(s, 0.85, 6.88, 11.65, 0.42, { fill: PANEL, line: "D0D0D0" });
  txt(s, 1.05, 6.88, 11.3, 0.42,
    "Detection costs between the timeout and the timeout plus one scan — 15 to 20 s by the constants, 10.7 to 14 s measured. Which of those two is right is not yet settled, and tuning the timer before it is would leave us unable to say what moved.",
    { fs: 8, tc: MUTED });
}

pres.writeFile({ fileName: "/sessions/hopeful-sharp-hopper/mnt/outputs/NDTwin_liveness_failover_flows.pptx" })
  .then(() => console.log("done"))
  .catch(e => { console.error(e); process.exit(1); });
