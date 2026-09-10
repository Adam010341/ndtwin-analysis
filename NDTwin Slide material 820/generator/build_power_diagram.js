// One slide: Phase 7 switch power management, as the control flow it actually is.
// Read out of  src/ndt_core/power_management/P4PowerStrategy.cpp  (powerOn / powerOff)
// and          p4_proxy/proxy_agent/topology_manager.py            (readopt_switch)
// Same drawing style as the architecture and the liveness/failover flow pages.
const pptxgen = require("pptxgenjs");

const ACCENT = "065A82";
const ACCENT_BG = "EEF3F6";
const PANEL = "F7F8F9";
const MUTED = "4F4F4F";
const WARNC = "9C3B2E";
const WARN_BG = "FBF2F0";
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
function step(s, x, y, w, h, head, detail, o) {
  o = o || {};
  box(s, x, y, w, h, { fill: o.fill || "FFFFFF", line: o.line || LINE, lw: o.lw || 1 });
  if (detail) {
    txt(s, x + 0.13, y + 0.04, w - 0.26, h * 0.44, head,
      { fs: o.hfs || 9.5, bold: true, tc: o.tc || "000000", ff: o.hff || AF, valign: "middle" });
    txt(s, x + 0.13, y + h * 0.44, w - 0.26, h * 0.52, detail,
      { fs: o.dfs || 7.5, tc: MUTED, valign: "top", ls: 0.94 });
  } else {
    txt(s, x + 0.13, y, w - 0.26, h, head,
      { fs: o.hfs || 9.5, bold: true, tc: o.tc || "000000", ff: o.hff || AF, align: o.align || "left" });
  }
}
function test(s, x, y, w, h, cond, note) {
  box(s, x, y, w, h, { fill: PANEL, lw: 1.25 });
  txt(s, x + 0.13, y + 0.03, w - 0.26, h * 0.50, cond, { fs: 9, bold: true, ff: FC, valign: "middle" });
  if (note) txt(s, x + 0.13, y + h * 0.50, w - 0.26, h * 0.46, note, { fs: 7.5, tc: MUTED, valign: "top", ls: 0.94 });
}
function exitBox(s, x, y, w, label, colour, fill) {
  box(s, x, y, w, 0.36, { line: colour, lw: 1.35, fill: fill || "FFFFFF" });
  txt(s, x, y, w, 0.36, label, { fs: 9.5, bold: true, tc: colour, align: "center" });
}
function branch(s, x, y, label, o) {
  o = o || {};
  txt(s, x, y, o.w || 0.44, o.h || 0.16, label, { fs: 7.5, tc: o.tc || MUTED, align: o.align || "left" });
}

const s = pres.addSlide();
s.background = { color: "FFFFFF" };

txt(s, 0.45, 0.36, 11.5, 0.34, "Phase 7: switching a bmv2 node off, and getting it back", { fs: 15, bold: true });
txt(s, 0.45, 0.70, 12.2, 0.26,
  "Powering off is one step. Powering on is four, because a restarted bmv2 comes back with no memory of ever having been adopted.",
  { fs: 9.5, tc: MUTED });

// ---------------- entry ----------------
step(s, 3.55, 1.06, 6.20, 0.38, "POST /ndt/set_switches_power_state?action=…", null,
  { fill: ACCENT_BG, line: ACCENT, lw: 1.25, hff: FC, hfs: 9.5, tc: ACCENT, align: "center" });

const LC = 2.50, RC = 8.40;                       // left / right chain centres
arrow(s, 6.65, 1.44, 0, 0.18, "plain");
arrow(s, LC, 1.62, RC - LC, 0, "plain");
arrow(s, LC, 1.62, 0, 0.30, "down");
arrow(s, RC, 1.62, 0, 0.30, "down");
txt(s, LC + 0.10, 1.66, 1.6, 0.20, "action = off", { fs: 8, tc: MUTED });
txt(s, RC + 0.10, 1.66, 1.6, 0.20, "action = on", { fs: 8, tc: MUTED });

// ---------------- left: power off ----------------
const LX = 0.85, LW = 3.30, LEX = 4.35, LEW = 1.55;
txt(s, LX, 1.94, 3.0, 0.20, "POWER OFF", { fs: 8, bold: true, tc: "000000" });

test(s, LX, 2.16, LW, 0.48, "getVertexIsUp(node) == false ?", "it is already off");
arrow(s, LX + LW, 2.40, LEX - (LX + LW), 0, "right");
branch(s, LX + LW + 0.04, 2.20, "yes");
exitBox(s, LEX, 2.22, LEW, "success", MUTED);
txt(s, LEX, 2.60, LEW, 0.30, "nothing to do, and saying so is accurate", { fs: 7, tc: MUTED, ls: 0.94, valign: "top" });
arrow(s, LC, 2.64, 0, 0.28, "down");
branch(s, LC + 0.08, 2.66, "no");

step(s, LX, 2.92, LW, 0.74, "sudo -n  ndtwin-p4-power  off",
  "SIGTERMs the one PID the manifest names for this switch — after re-verifying that PID still is that switch — and exits 0 only once the process is gone.",
  { hff: FC, hfs: 9 });
arrow(s, LX + LW, 3.29, LEX - (LX + LW), 0, "right");
branch(s, LX + LW + 0.04, 3.09, "fail");
exitBox(s, LEX, 3.11, LEW, "500", WARNC, WARN_BG);
txt(s, LEX, 3.49, LEW, 0.62, "Left running is left up. Marking it down over a failed kill would hide a live switch.",
  { fs: 7, tc: MUTED, ls: 0.94, valign: "top" });
arrow(s, LC, 3.66, 0, 0.28, "down");
branch(s, LC + 0.08, 3.68, "ok");

step(s, LX, 3.94, LW, 0.40, "setVertexDown(node)   →   success", null, { hff: FC, hfs: 9 });

box(s, LX, 4.58, LW + 0.20 + LEW, 0.82, { fill: PANEL, line: "D0D0D0" });
txt(s, LX + 0.14, 4.62, LW + LEW - 0.06, 0.74,
  "Everything the twin observes after this follows honestly: the stream dies with the process, the probe starts failing, and the watchdog reroutes around the switch. That is the acceptance criterion — the other nine keep forwarding.",
  { fs: 7.5, tc: MUTED, ls: 0.96, valign: "top" });

// ---------------- right: power on ----------------
const RX = 6.45, RW = 3.90, REX = 10.55, REW = 1.95;
txt(s, RX, 1.94, 3.0, 0.20, "POWER ON", { fs: 8, bold: true, tc: "000000" });

test(s, RX, 2.16, RW, 0.48, "getVertexIsUp(node) == true ?", "it is already up");
arrow(s, RX + RW, 2.40, REX - (RX + RW), 0, "right");
branch(s, RX + RW + 0.04, 2.20, "yes");
exitBox(s, REX, 2.22, REW, "success", WARNC, WARN_BG);
txt(s, REX, 2.60, REW, 0.86,
  "Known defect. For about ten seconds after a power-off this fires wrongly — the 1 Hz liveness worker has already flipped the dead switch back to up. Returns 200 in 0.01 s and does nothing. Wait 15 s.",
  { fs: 7, tc: WARNC, ls: 0.94, valign: "top" });
arrow(s, RC, 2.64, 0, 0.28, "down");
branch(s, RC + 0.08, 2.66, "no");

step(s, RX, 2.92, RW, 0.62, "sudo -n  ndtwin-p4-power  on",
  "Relaunches from the manifest and exits 0 only once bmv2 is accepting gRPC. That is where the helper’s knowledge ends.",
  { hff: FC, hfs: 9 });
arrow(s, RC, 3.54, 0, 0.26, "down");
branch(s, RC + 0.08, 3.56, "ok");

step(s, RX, 3.80, RW, 0.66, "POST /p4/readopt/{dpid}",
  "curl --fail-with-body, not -f — plain -f discards the body, and the body is the only place the failing step is named.",
  { fill: ACCENT_BG, line: ACCENT, lw: 1.4, hff: FC, hfs: 9.5, tc: ACCENT });
txt(s, REX, 3.62, REW, 1.30,
  "Why this step exists at all. A restarted bmv2 comes back with no pipeline, no clone session, no table entries and no mastership — and the probe cannot tell, because it is a unary RPC answered without any pipeline loaded. Skip it and the twin certifies Up a switch that cannot forward one packet.",
  { fs: 7, tc: MUTED, ls: 0.94, valign: "top" });
arrow(s, RC, 4.46, 0, 0.22, "down");

// the four named steps inside readopt
box(s, RX, 4.68, RW, 1.42, { fill: PANEL, lw: 1.25 });
txt(s, RX + 0.13, 4.72, RW - 0.26, 0.20, "four named steps, in this order", { fs: 7.5, bold: true, tc: "000000" });
const inner = [
  ["1  mastership", "arbitration after a 1 s settle. Not granted → 502, and the switch is not touched."],
  ["2  pipeline", "set_forwarding_pipeline_config() → 502 on any error."],
  ["3  clone session", "a failure costs telemetry, not the switch — it forwards, it just reports zero."],
  ["4  routes", "all writes refused after the pipeline was accepted → 502; the tables are empty."],
];
let iy = 4.96;
inner.forEach(([k, v]) => {
  txt(s, RX + 0.13, iy, 1.15, 0.16, k, { fs: 7.5, bold: true, ff: FC, tc: ACCENT });
  txt(s, RX + 1.32, iy, RW - 1.45, 0.28, v, { fs: 7, tc: MUTED, ls: 0.94, valign: "top" });
  iy += 0.28;
});

arrow(s, RX + RW, 5.39, REX - (RX + RW), 0, "right");
branch(s, RX + RW + 0.04, 5.19, "fail");
exitBox(s, REX, 5.21, REW, "502", WARNC, WARN_BG);
txt(s, REX, 5.59, REW, 1.30,
  "The vertex is not marked up. Recover by retrying the readopt directly — it is the only call that re-attempts the adoption. Do not repeat the power-on: the process is up, so liveness marks the switch up within a second and the retry returns success without re-attempting anything.",
  { fs: 7, tc: MUTED, ls: 0.94, valign: "top" });
arrow(s, RC, 6.10, 0, 0.26, "down");
branch(s, RC + 0.08, 6.12, "ok");

step(s, RX, 6.36, RW, 0.40, "setVertexUp(node)   →   success", null, { hff: FC, hfs: 9 });

// ---------------- measured, and the residual ----------------
box(s, 0.85, 6.92, 11.65, 0.42, { fill: PANEL, line: "D0D0D0" });
txt(s, 1.05, 6.92, 6.40, 0.42,
  "Live acceptance: held off 135 s  ·  power-on to fully re-adopted 1.50 s  ·  678 readings at 10 Hz  ·  0 of them wrongly showed it up",
  { fs: 8, tc: "000000" });
txt(s, 7.55, 6.92, 4.75, 0.42,
  "Residual, stated rather than hidden: re-adoption reports “adopted, routes not yet installed” for about 30 s while LLDP rediscovers the links.",
  { fs: 8, tc: MUTED, align: "right" });

pres.writeFile({ fileName: "/sessions/hopeful-sharp-hopper/mnt/outputs/NDTwin_phase7_power_flow.pptx" })
  .then(() => console.log("done"))
  .catch(e => { console.error(e); process.exit(1); });
