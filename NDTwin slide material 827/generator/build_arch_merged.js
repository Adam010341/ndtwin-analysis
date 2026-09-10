// One slide: the NDTwin architecture with all three data planes on it.
//
// Merges the original figure (Open vSwitch + hardware switches, driven by Ryu)
// with the P4 figure (bmv2, driven by the proxy agent). Nothing is dropped:
// the physical network keeps its place beside the two emulated ones.
//
// Drawn all in black like the original — this is the framework as it stands,
// not a diff, so there is no "new" badge and no accent colour.
//
// Vertical budget (2026-08-21 revision): apps, kernel and tools are tightened
// so the three fabrics can be 1.40" tall instead of 1.02". The top half is
// boxes with two lines of text in them and compresses without losing anything;
// the bottom half is the part a reader actually looks at.
const pptxgen = require("pptxgenjs");

const AF = "Arial";
const LINE = "000000";
const MUTED = "4F4F4F";

const pres = new pptxgen();
pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
pres.layout = "WIDE";

function aBox(s, x, y, w, h, text, o) {
  o = o || {};
  s.addShape("rect", {
    x, y, w, h,
    fill: { color: o.fill || "FFFFFF" },
    line: { color: o.line || LINE, width: o.lw || 1 },
  });
  if (text) {
    s.addText(text, {
      x: x + 0.04, y, w: w - 0.08, h, align: "center", valign: "middle",
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
    line: { color: o.color || LINE, width: o.lw || 1.1 },
  };
  if (dir === "up")        { opt.flipV = true;  opt.line.endArrowType = "triangle"; }
  else if (dir === "down") { opt.line.endArrowType = "triangle"; }
  else if (dir === "right"){ opt.line.endArrowType = "triangle"; }
  else if (dir === "left") { opt.flipH = true;  opt.line.endArrowType = "triangle"; }
  else if (dir === "plain"){ /* no head */ }
  else { opt.line.beginArrowType = "triangle"; opt.line.endArrowType = "triangle"; }
  s.addShape("line", opt);
}
function aDash(s, x, y, w, h) {
  s.addShape("line", { x, y, w, h, line: { color: "808080", width: 1, dashType: "dash" } });
}
function aCloud(s, x, y, w, h) {
  s.addShape("cloud", { x, y, w, h, fill: { color: "FFFFFF" }, line: { color: LINE, width: 1 } });
}

const s = pres.addSlide();
s.background = { color: "FFFFFF" };

// ===========================================================================
// apps, kernel, tools — same content as the original, tightened vertically
// ===========================================================================
const KERNEL_TOP = 1.78, KERNEL_BOT = 4.20;

aText(s, 0.30, 0.14, 8.0, 0.34, "NDTwin: A Framework for Network Digital Twins", { fs: 13, bold: true });

aText(s, 0.24, 0.92, 1.49, 0.34, "NDTwin Apps", { fs: 12 });
aBox(s, 1.75, 0.72, 1.48, 0.70, "Traffic-engineering App", { fs: 10 });
aBox(s, 3.36, 0.72, 1.48, 0.70, "Energy-saving App", { fs: 10 });
aText(s, 4.92, 0.85, 0.50, 0.44, "...", { fs: 13 });
aBox(s, 5.33, 0.72, 2.11, 0.70, "Apps (using simulation for prediction and optimal control)", { fs: 10 });
aBox(s, 7.56, 0.72, 2.26, 0.70, "Apps (using AI/ML model inference for prediction and optimal control)", { fs: 10 });

aDash(s, 0.13, 1.60, 9.89, 0.004);
aDash(s, 10.02, 0.66, 0.004, 6.60);
aArrow(s, 5.17, 1.44, 0, 0.30, "both");

aBox(s, 0.29, KERNEL_TOP, 9.31, KERNEL_BOT - KERNEL_TOP, null);
aText(s, 0.42, 1.84, 1.6, 0.28, "NDTwin Kernel", { fs: 12 });
[
  [0.68, 2.16, 2.69, "Device configuration and power manager"],
  [3.63, 2.16, 2.63, "Application registration and coordination manager"],
  [6.62, 2.16, 2.63, "Intent to tasks translator"],
  [0.65, 2.86, 2.69, "Flow routing manager"],
  [3.64, 2.86, 2.63, "Simulation request and reply manager"],
  [6.67, 2.86, 2.63, "Topology and flow monitor"],
  [0.73, 3.56, 2.63, "Data cache manager"],
  [3.65, 3.56, 2.64, "Controller and other events handler"],
  [6.67, 3.56, 2.63, "Flow information and link bandwidth usage collector"],
].forEach(([x, y, w, t]) => aBox(s, x, y, w, 0.48, t, { fs: 10 }));

aText(s, 10.27, 1.10, 1.6, 0.34, "NDTwin Tools", { fs: 12 });
[
  "Local LLM (fine-tuning)",
  "On-line LLM (e.g., ChatGPT)",
  "Simulation platform manager",
  "Network traffic visualizer",
  "Web GUI (supporting intent inputs)",
  "Network state recorder",
].forEach((t, i) => aBox(s, 10.33, 1.78 + i * 0.44, 2.77, 0.40, t, { fs: 10 }));
aArrow(s, 9.63, 2.99, 0.70, 0, "both");

// ===========================================================================
// control plane and data planes — mirrored about the physical network
//
// CX = 4.95 is the centre of the kernel box and of the middle cloud. Every
// pair below is placed at CX ± the same offset, so the figure reads as a
// mirror. The one line without a mirror is Ryu's second leg into the physical
// network, and that is information rather than decoration: hardware switches
// are OpenFlow-driven by the same controller as the OVS fabric.
//
// sFlow is drawn the same way on all three planes — straight from the fabric
// into the kernel's collector. On the P4 side the proxy is what actually
// builds the datagram, but that is a detail of how, not of what talks to what,
// so it is carried by the word "synthesised" rather than by a different route.
// ===========================================================================
const CX = 4.95;
const CTRL_Y = 4.72, CTRL_H = 0.46, CTRL_W = 2.55, CTRL_OFF = 1.625;
const CLOUD_Y = 5.66, CLOUD_H = 1.40, CLOUD_W = 2.80, CLOUD_OFF = 3.25;

const RYU_CX   = CX - CTRL_OFF;          // 3.325
const PROXY_CX = CX + CTRL_OFF;          // 6.575

aBox(s, RYU_CX   - CTRL_W / 2, CTRL_Y, CTRL_W, CTRL_H, "SDN controller (Ryu)", { fs: 10.5 });
aBox(s, PROXY_CX - CTRL_W / 2, CTRL_Y, CTRL_W, CTRL_H, "P4 proxy agent",       { fs: 10.5 });

// kernel <-> control plane: one link each, at mirrored positions.
// The same word on both sides on purpose. That the proxy answers in Ryu's
// shapes is said by the figure itself — it sits exactly where Ryu sits, and
// the kernel reaches it the same way — so it does not need a longer label.
aArrow(s, RYU_CX,   KERNEL_BOT + 0.04, 0, CTRL_Y - KERNEL_BOT - 0.04, "both");
aArrow(s, PROXY_CX, KERNEL_BOT + 0.04, 0, CTRL_Y - KERNEL_BOT - 0.04, "both");
aText(s, RYU_CX - 1.12,  4.30, 1.02, 0.28, "REST", { fs: 9, tc: MUTED, align: "right" });
aText(s, PROXY_CX + 0.10, 4.30, 1.02, 0.28, "REST", { fs: 9, tc: MUTED });

// telemetry: one arrow per fabric, straight into the kernel's collector
[CX - 3.85, CX, CX + 3.85].forEach(x =>
  aArrow(s, x, KERNEL_BOT + 0.04, 0, CLOUD_Y - KERNEL_BOT - 0.04, "up"));
aText(s, CX - 3.77, 4.30, 0.70, 0.28, "sFlow", { fs: 9, tc: MUTED });
aText(s, CX + 0.08, 4.30, 0.70, 0.28, "sFlow", { fs: 9, tc: MUTED });
aText(s, CX + 2.60, 4.30, 1.17, 0.28, "sFlow (synthesised)", { fs: 9, tc: MUTED, align: "right" });

// control plane -> data planes
[CX - 2.55, CX - 0.50, CX + 2.55].forEach(x =>
  aArrow(s, x, CTRL_Y + CTRL_H, 0, CLOUD_Y - (CTRL_Y + CTRL_H), "down"));
aText(s, CX - 2.47, 5.20, 0.95, 0.26, "OpenFlow",  { fs: 9, tc: MUTED });
aText(s, CX - 0.42, 5.20, 0.95, 0.26, "OpenFlow",  { fs: 9, tc: MUTED });
aText(s, CX + 1.40, 5.20, 1.07, 0.26, "P4Runtime", { fs: 9, tc: MUTED, align: "right" });

// the line between NDTwin and the network it is a twin of
s.addShape("line", { x: 0.00, y: 5.52, w: 10.05, h: 0.004, line: { color: LINE, width: 1 } });

// ---- the three fabrics, drawn identically ----
function dataPlane(cx, label, switchText) {
  const x = cx - CLOUD_W / 2;
  aCloud(s, x, CLOUD_Y, CLOUD_W, CLOUD_H);
  // links first, so the switch boxes sit on top of them
  s.addShape("line", { x: x + 1.02, y: 6.32, w: 0.06, h: 0.18, line: { color: LINE, width: 1 } });
  s.addShape("line", { x: x + 1.02, y: 6.12, w: 0.72, h: 0.20, line: { color: LINE, width: 1 } });
  s.addShape("line", { x: x + 1.72, y: 6.24, w: 0.06, h: 0.26, line: { color: LINE, width: 1 } });
  [[x + 0.32, 6.06], [x + 1.02, 6.38], [x + 1.72, 5.98]]
    .forEach(([bx, by]) => aBox(s, bx, by, 0.76, 0.50, switchText, { fs: 9 }));
  aText(s, x - 0.10, 7.14, CLOUD_W + 0.20, 0.28, label, { fs: 11, align: "center" });
}

dataPlane(CX - CLOUD_OFF, "Emulated Network (Mininet)",       "Open vSwitch");
dataPlane(CX,             "Physical Network",                 "Hardware switch");
dataPlane(CX + CLOUD_OFF, "Emulated Network (Mininet, bmv2)", "bmv2 switch");

aText(s, CX - CLOUD_OFF / 2 - 0.22, 6.30, 0.45, 0.30, "or", { fs: 11, align: "center" });
aText(s, CX + CLOUD_OFF / 2 - 0.22, 6.30, 0.45, 0.30, "or", { fs: 11, align: "center" });

// the traffic generator drives whichever fabric is in use
aBox(s, 10.31, 6.16, 2.77, 0.42, "Network traffic generator", { fs: 10 });
aArrow(s, 9.64, 6.37, 0.67, 0, "both");

pres.writeFile({ fileName: "/sessions/hopeful-sharp-hopper/mnt/outputs/NDTwin_Arch_merged.pptx" })
  .then(() => console.log("done"))
  .catch(e => { console.error(e); process.exit(1); });
