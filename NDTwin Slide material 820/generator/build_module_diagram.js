// Standalone: one slide, the P4 proxy agent's eight modules and how they
// relate to each other, to the kernel above and to the switches below.
// Same drawing style as the two architecture diagrams in NDTwin_deck.pptx:
// Arial, white boxes, 1 pt black outlines, ACCENT for the new (proxy) side.
const pptxgen = require("pptxgenjs");

const ACCENT = "065A82";
const ACCENT_BG = "EEF3F6";
const PANEL = "F7F8F9";
const MUTED = "4F4F4F";
const AF = "Arial";
const LINE = "000000";

const pres = new pptxgen();
pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
pres.layout = "WIDE";

// ---- the same primitives the deck's architecture pages use -------------
function aBox(s, x, y, w, h, text, o) {
  o = o || {};
  s.addShape("rect", {
    x, y, w, h,
    fill: { color: o.fill || "FFFFFF" },
    line: { color: o.line || LINE, width: o.lw || 1, dashType: o.dash || "solid" },
  });
  if (text) {
    s.addText(text, {
      x: x + 0.05, y, w: w - 0.1, h, align: "center", valign: "middle",
      fontFace: AF, fontSize: o.fs || 11, bold: !!o.bold,
      color: o.tc || "000000", margin: 0, lineSpacingMultiple: 0.92,
    });
  }
}
function aText(s, x, y, w, h, text, o) {
  o = o || {};
  s.addText(text, {
    x, y, w, h, align: o.align || "left", valign: o.valign || "middle",
    fontFace: AF, fontSize: o.fs || 12, bold: !!o.bold,
    color: o.tc || "000000", margin: 0, lineSpacingMultiple: 0.95,
  });
}
function aArrow(s, x, y, w, h, dir, o) {
  o = o || {};
  const opt = {
    x, y, w: w || 0.008, h: h || 0.008,
    line: { color: o.color || "000000", width: o.lw || 1.1, dashType: o.dash || "solid" },
  };
  if (dir === "up")        { opt.flipV = true;  opt.line.endArrowType = "triangle"; }
  else if (dir === "down") { opt.line.endArrowType = "triangle"; }
  else if (dir === "right"){ opt.line.endArrowType = "triangle"; }
  else if (dir === "left") { opt.flipH = true;  opt.line.endArrowType = "triangle"; }
  else { opt.line.beginArrowType = "triangle"; opt.line.endArrowType = "triangle"; }
  if (o.flipH) opt.flipH = !opt.flipH;
  s.addShape("line", opt);
}
function aDash(s, x, y, w, h) {
  s.addShape("line", { x, y, w, h, line: { color: "808080", width: 1, dashType: "dash" } });
}
function aCloud(s, x, y, w, h) {
  s.addShape("cloud", { x, y, w, h, fill: { color: "FFFFFF" }, line: { color: LINE, width: 1 } });
}

// a module box: file name, one short statement of what it is for, line count at the foot
function mod(s, x, y, w, h, name, role, lines, o) {
  o = o || {};
  aBox(s, x, y, w, h, null, { line: ACCENT, lw: o.lw || 1.25, fill: o.fill || "FFFFFF" });
  s.addText(name, {
    x: x + 0.05, y: y + 0.05, w: w - 0.1, h: 0.24, align: "center", valign: "middle",
    fontFace: "Courier New", fontSize: o.fs || 10.5, bold: true, color: ACCENT, margin: 0,
  });
  if (role) {
    s.addText(role, {
      x: x + 0.07, y: y + 0.30, w: w - 0.14, h: h - 0.56,
      align: "center", valign: o.rvalign || "top",
      fontFace: AF, fontSize: o.rfs || 8, color: "1A1A1A", margin: 0, lineSpacingMultiple: 0.94,
    });
  }
  s.addText(lines + " lines", {
    x: x + 0.05, y: y + h - 0.24, w: w - 0.1, h: 0.2, align: "center", valign: "middle",
    fontFace: AF, fontSize: 7, color: MUTED, margin: 0,
  });
}

const s = pres.addSlide();
s.background = { color: "FFFFFF" };

// ---------------- title ----------------
aText(s, 0.45, 0.20, 10.0, 0.34, "The P4 proxy agent, module by module", { fs: 15, bold: true });
aText(s, 0.45, 0.54, 11.4, 0.26,
  "Eight files. One of them talks to the switches, two of them talk to the kernel, and one holds all the state.",
  { fs: 9.5, tc: MUTED });

// ---------------- kernel ----------------
aBox(s, 0.85, 0.94, 11.65, 0.62, null, { lw: 1.25 });
aText(s, 0.98, 0.96, 4.0, 0.58, "NDTwin Kernel", { fs: 11.5, bold: true });
aText(s, 4.20, 0.96, 8.17, 0.58,
  "/ndt/* HTTP API   ·   sFlow collector on UDP 6343   ·   unchanged by this work",
  { fs: 9, tc: MUTED, align: "right" });

aDash(s, 0.45, 2.00, 12.53, 0);

// ---- the three things that cross the kernel boundary ----
aArrow(s, 4.30, 1.56, 0, 0.94, "both");
aText(s, 4.46, 1.60, 1.78, 0.36, "Ryu-compatible REST\nthe kernel polls, unmodified", { fs: 7.5, tc: MUTED });

aArrow(s, 11.05, 1.56, 0, 0.94, "up");
aText(s, 6.30, 1.58, 4.60, 0.20,
  "/ndt/ push — switch entered, link failure and recovery, destination paths",
  { fs: 7.5, tc: MUTED, align: "right" });

aArrow(s, 12.20, 1.56, 0, 3.46, "up", { color: ACCENT, lw: 1.4 });
aText(s, 6.30, 1.80, 4.60, 0.20, "sFlow v5, synthesised — straight into the collector on UDP 6343",
  { fs: 7.5, tc: ACCENT, align: "right" });

// ---------------- the proxy frame ----------------
aBox(s, 0.85, 2.20, 11.65, 3.72, null, { line: ACCENT, lw: 1.75 });
s.addShape("rect", { x: 1.00, y: 2.10, w: 3.20, h: 0.20, fill: { color: "FFFFFF" }, line: { type: "none" } });
aText(s, 1.05, 2.08, 3.15, 0.24, "P4 proxy agent   ·   FastAPI / uvicorn", { fs: 9.5, bold: true, tc: ACCENT });

// ---- main.py: constructs the other seven ----
mod(s, 1.05, 2.50, 1.75, 3.22, "main.py",
  "Startup.\n\nOpens all ten switch\nconnections at once,\nbuilds every box on\nthis page, and wires\nthe callbacks between\nthem.", 345,
  { fill: PANEL, rfs: 7.5, rvalign: "middle" });
[3.02, 4.31, 5.41].forEach(yy => aArrow(s, 2.80, yy, 0.30, 0, "right", { dash: "dash", color: ACCENT }));

// ---- north row: the only door in, and the two renderers behind it ----
mod(s, 3.10, 2.50, 2.55, 1.05, "api_routes.py",
  "The only door in.\n/v1.0/topology/*  ·  /stats/flowentry/*\n/stats/flow/<dpid>  ·  /p4/*", 366, { fill: ACCENT_BG });

mod(s, 5.95, 2.50, 2.15, 0.48, "ryu_topology.py", "", 338, { fs: 9.5 });
mod(s, 5.95, 3.07, 2.15, 0.48, "ryu_flow_stats.py", "", 190, { fs: 9.5 });
aArrow(s, 5.65, 2.74, 0.30, 0, "right");
aArrow(s, 5.65, 3.31, 0.30, 0, "right");
aText(s, 8.18, 2.50, 0.30, 1.05, "}", { fs: 26, tc: MUTED, align: "center" });
aText(s, 8.42, 2.56, 1.80, 0.94,
  "Shape only, no state.\nThey turn the graph into\nthe exact JSON Ryu\nwould have returned.", { fs: 7.5, tc: MUTED });

mod(s, 10.35, 2.50, 1.45, 1.05, "kernel_notifier.py",
  "Northbound push.\nThe four /ndt/ calls\nRyu used to make.", 184, { fs: 9 });
aArrow(s, 11.05, 3.55, 0, 0.35, "up");
aText(s, 8.90, 3.58, 2.00, 0.28, "link events, paths", { fs: 7.5, tc: MUTED, align: "right" });

// ---- the state row ----
mod(s, 3.10, 3.90, 8.55, 0.82, "topology_manager.py",
  "All of the state. The networkx graph, BFS routing, the LLDP beacon sender and its watchdog,\nand the translation from a Ryu flow rule into a P4 table entry.", 1516,
  { fill: ACCENT_BG, fs: 11.5, rfs: 8.5 });
aArrow(s, 4.30, 3.55, 0, 0.35, "both");
aText(s, 4.46, 3.58, 2.60, 0.28, "reads state, installs rules", { fs: 7.5, tc: MUTED });

// ---- the south row: one client per switch, and the emitter it feeds ----
mod(s, 3.10, 5.02, 4.20, 0.78, "p4_client.py",
  "One per switch. P4Runtime gRPC, the clone session, and the split of\nevery packet_in on its reason field.", 755, { fill: ACCENT_BG });
aArrow(s, 4.30, 4.72, 0, 0.30, "down");
aText(s, 4.46, 4.75, 2.90, 0.26, "route writes  ·  LLDP beacons out", { fs: 7.5, tc: MUTED });
aArrow(s, 6.60, 4.72, 0, 0.30, "up");
aText(s, 6.76, 4.75, 2.10, 0.26, "reason = LLDP", { fs: 7.5, tc: MUTED });

mod(s, 10.35, 5.02, 2.00, 0.78, "sflow_emitter.py",
  "Builds a datagram byte-compatible\nwith what OVS sends.", 448, { fill: ACCENT_BG, fs: 9.5, rfs: 7.5 });
aArrow(s, 7.30, 5.41, 3.05, 0, "right", { color: ACCENT, lw: 1.4 });
aText(s, 7.46, 5.10, 3.00, 0.26, "reason = sample", { fs: 7.5, tc: ACCENT });

// ---------------- switches ----------------
aArrow(s, 5.20, 5.92, 0, 0.42, "both");
aText(s, 5.36, 5.95, 4.00, 0.15, "P4Runtime gRPC — one connection per switch", { fs: 8, tc: MUTED, valign: "top" });
aDash(s, 0.45, 6.12, 12.53, 0);

aCloud(s, 3.00, 6.34, 7.30, 0.98);
aText(s, 3.45, 6.58, 6.40, 0.50,
  "Emulated network (Mininet)   —   bmv2 simple_switch_grpc × 10", { fs: 10, align: "center" });

// ---------------- the one file both sides read ----------------
aBox(s, 10.55, 6.34, 2.43, 0.98, null, { line: "9A9A9A", dash: "dash", fill: PANEL });
aText(s, 10.66, 6.38, 2.21, 0.90,
  "setting/…Topology*.json\nRead by the emitter for its agent\naddresses and by the kernel for the\nsame graph. An address the kernel\ndoes not recognise becomes\ntelemetry attributed to nothing.",
  { fs: 7, tc: MUTED, valign: "top" });
aArrow(s, 11.90, 5.80, 0, 0.54, "up", { color: "9A9A9A", dash: "dash" });

aText(s, 0.45, 6.42, 2.35, 0.80,
  "Nothing above the kernel line\nchanges. The proxy answers in\nRyu's shapes and manufactures\nthe telemetry bmv2 never sends.",
  { fs: 7.5, tc: MUTED });
aText(s, 0.45, 7.20, 6.0, 0.22, "Line counts are current file sizes at cc249c8, not diff counts.", { fs: 7, tc: "6E6E6E" });

pres.writeFile({ fileName: "/sessions/hopeful-sharp-hopper/mnt/outputs/NDTwin_proxy_modules.pptx" })
  .then(() => console.log("done"))
  .catch(e => { console.error(e); process.exit(1); });
