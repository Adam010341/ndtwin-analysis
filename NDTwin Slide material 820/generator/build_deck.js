const pptxgen = require("pptxgenjs");

// ============ minimal palette: one accent, everything else ink/grey ============
const INK      = "1A1A1A";   // titles
const WARNC    = "9C3B2E";   // used only where a measured value is the bad one
const BODY     = "2E2E2E";   // body text
const MUTED    = "4F4F4F";   // secondary text — still clearly legible
const FAINT    = "6E6E6E";   // captions, column labels
const RULE     = "D0D0D0";   // hairlines
const ACCENT   = "065A82";   // the single accent
const ACCENT_BG= "EEF3F6";   // very light accent wash
const PANEL    = "F7F8F9";   // neutral panel

const FH = "Cambria";
const FB = "Calibri";
const FC = "Courier New";

const pres = new pptxgen();
pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
pres.layout = "WIDE";

const M = 0.85;              // left margin
const CW = 13.333 - M * 2;   // content width

function pageTitle(s, title, sub) {
  s.addText(title, {
    x: M, y: 0.62, w: CW, h: 0.68,
    fontFace: FH, fontSize: 30, bold: true, color: INK, margin: 0,
  });
  if (sub) {
    s.addText(sub, {
      x: M, y: 1.32, w: CW, h: 0.38,
      fontFace: FB, fontSize: 14, color: MUTED, margin: 0,
    });
  }
  s.addShape("line", {
    x: M, y: sub ? 1.86 : 1.46, w: CW, h: 0.01,
    line: { color: RULE, width: 1 },
  });
}

let PAGE = 0;
function newSlide() { PAGE++; return pres.addSlide(); }

function pageNum(s) {
  s.addText(String(PAGE), {
    x: 12.0, y: 6.92, w: 0.48, h: 0.3, align: "right",
    fontFace: FB, fontSize: 10, color: FAINT, margin: 0,
  });
}

// numbered list item: returns next y
function listItem(s, x, y, w, n, head, body, bodyW) {
  s.addText(n, {
    x, y: y - 0.02, w: 0.32, h: 0.3,
    fontFace: FB, fontSize: 13, bold: true, color: ACCENT, margin: 0,
  });
  s.addText(head, {
    x: x + 0.36, y: y - 0.03, w: (bodyW || w) - 0.36, h: 0.32,
    fontFace: FB, fontSize: 15.5, bold: true, color: INK, margin: 0,
  });
  s.addText(body, {
    x: x + 0.36, y: y + 0.34, w: (bodyW || w) - 0.36, h: 0.9,
    fontFace: FB, fontSize: 12.5, color: BODY, margin: 0, lineSpacingMultiple: 1.24,
  });
}

// ============================================================
// Page 1 — Title (white, minimal)
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };

  s.addText("P4 / bmv2 Data-Plane Support", {
    x: M, y: 2.72, w: 11.0, h: 0.95,
    fontFace: FH, fontSize: 44, bold: true, color: INK, margin: 0,
  });
  s.addText("— a second data plane, with nothing above it changed", {
    x: M, y: 3.72, w: 11.0, h: 0.55,
    fontFace: FB, fontSize: 22, color: MUTED, margin: 0,
  });

  s.addShape("line", { x: M, y: 4.66, w: 1.1, h: 0.01, line: { color: ACCENT, width: 2 } });

  s.addText("NDTwin Network Digital Twin", {
    x: M, y: 2.16, w: 11.0, h: 0.42,
    fontFace: FB, fontSize: 16, color: ACCENT, margin: 0, charSpacing: 1.2,
  });

  s.addText("Adam　·　2026-08-19", {
    x: M, y: 6.42, w: 8.0, h: 0.34,
    fontFace: FB, fontSize: 13, color: MUTED, margin: 0,
  });
}

// ============================================================
// Architecture diagrams (pages 2 and 4)
// Redrawn from NDTwin_Arch.pptx, same coordinates and style.
// ============================================================
const AF = "Arial";
const LINE = "000000";

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
// straight arrow; dir: "up" | "down" | "both" | "right" | "left"
function aArrow(s, x, y, w, h, dir, o) {
  o = o || {};
  const opt = {
    x, y, w: w || 0.008, h: h || 0.008,
    line: { color: o.color || "000000", width: o.lw || 1.1 },
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

// everything above the lower dashed rule — identical on both diagrams
function archTop(s) {
  aText(s, 0.30, 0.16, 8.0, 0.34, "NDTwin: A Framework for Network Digital Twins", { fs: 13, bold: true });

  // apps band
  aText(s, 0.24, 1.05, 1.49, 0.37, "NDTwin Apps", { fs: 12 });
  aBox(s, 1.75, 0.82, 1.48, 0.84, "Traffic-engineering App", { fs: 10.5 });
  aBox(s, 3.36, 0.84, 1.48, 0.84, "Energy-saving App", { fs: 10.5 });
  aText(s, 4.92, 0.97, 0.5, 0.5, "...", { fs: 13 });
  aBox(s, 5.33, 0.82, 2.11, 0.84, "Apps (using simulation for prediction and optimal control)", { fs: 10.5 });
  aBox(s, 7.56, 0.82, 2.26, 0.84, "Apps (using AI/ML model inference for prediction and optimal control)", { fs: 10.5 });

  aDash(s, 0.13, 1.77, 9.89, 0.004);
  aDash(s, 10.02, 0.78, 0.004, 6.30);

  // kernel
  aBox(s, 0.29, 1.99, 9.31, 2.93, null);
  aText(s, 0.42, 2.06, 1.6, 0.3, "NDTwin Kernel", { fs: 12 });
  const k = [
    [0.68, 2.45, 2.69, 0.55, "Device configuration and power manager"],
    [3.63, 2.48, 2.63, 0.49, "Application registration and coordination manager"],
    [6.62, 2.48, 2.63, 0.40, "Intent to tasks translator"],
    [0.65, 3.34, 2.69, 0.40, "Flow routing manager"],
    [3.64, 3.34, 2.63, 0.50, "Simulation request and reply manager"],
    [6.67, 3.35, 2.63, 0.40, "Topology and flow monitor"],
    [0.73, 4.07, 2.63, 0.55, "Data cache manager"],
    [3.65, 4.10, 2.64, 0.55, "Controller and other events handler"],
    [6.67, 4.11, 2.63, 0.55, "Flow information and link bandwidth usage collector"],
  ];
  k.forEach(([x, y, w, h, t]) => aBox(s, x, y, w, h, t, { fs: 10.5 }));
  aArrow(s, 5.17, 1.63, 0, 0.31, "both");

  // tools column
  aText(s, 10.27, 1.22, 1.6, 0.37, "NDTwin Tools", { fs: 12 });
  const tools = [
    [1.94, 0.50, "Local LLM (fine-tuning)"],
    [2.59, 0.50, "On-line LLM (e.g., ChatGPT)"],
    [3.21, 0.42, "Simulation platform manager"],
    [3.77, 0.42, "Network traffic visualizer"],
    [4.32, 0.50, "Web GUI (supporting intent inputs)"],
    [4.97, 0.42, "Network state recorder"],
  ];
  tools.forEach(([y, h, t]) => aBox(s, 10.33, y, 2.77, h, t, { fs: 10.5 }));
  aArrow(s, 9.63, 3.67, 0.70, 0, "both");
  aBox(s, 10.31, 6.32, 2.77, 0.50, "Network traffic generator", { fs: 10.5 });
}

// ============================================================
// Page 2 — Outline
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  pageTitle(s, "Outline", null);

  const sections = [
    { n: "0", t: "Background",
      d: "The system I inherited, the architecture, the stack, and the scale of what changed.",
      p: "pp. 4–9" },
    { n: "1", t: "New capabilities",
      d: "The P4 pipeline, the proxy agent, telemetry synthesis, liveness, failover, power.",
      p: "pp. 11–18" },
    { n: "2", t: "Test tooling and documentation",
      d: "The methodology, the five-layer harness, and what was written down.",
      p: "pp. 20–23" },
    { n: "3", t: "Measured results",
      d: "Differential testing, failover, throughput, load, twin accuracy — and a live demo.",
      p: "pp. 25–40" },
  ];

  let y = 2.40;
  sections.forEach((sec, i) => {
    s.addText(sec.n, {
      x: M, y: y - 0.02, w: 0.4, h: 0.34,
      fontFace: FH, fontSize: 17, bold: true, color: ACCENT, margin: 0,
    });
    s.addText(sec.t, {
      x: M + 0.5, y: y - 0.04, w: 7.6, h: 0.36,
      fontFace: FB, fontSize: 18, bold: true, color: INK, margin: 0,
    });
    s.addText(sec.d, {
      x: M + 0.5, y: y + 0.36, w: 8.6, h: 0.34,
      fontFace: FB, fontSize: 12.5, color: BODY, margin: 0,
    });
    s.addText(sec.p, {
      x: M + CW - 1.5, y: y - 0.02, w: 1.5, h: 0.34, align: "right",
      fontFace: FB, fontSize: 12, color: FAINT, margin: 0,
    });
    y += 0.92;
    if (i < sections.length - 1) {
      s.addShape("line", { x: M, y: y - 0.12, w: CW, h: 0.01, line: { color: "EFEFEF", width: 1 } });
    }
  });

  pageNum(s);
}

// ============================================================
// Page 3 — section divider: Background
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };

  s.addText("SECTION 0", {
    x: M, y: 2.16, w: 11.0, h: 0.42,
    fontFace: FB, fontSize: 16, color: ACCENT, margin: 0, charSpacing: 1.2,
  });
  s.addText("Background", {
    x: M, y: 2.72, w: 11.0, h: 0.95,
    fontFace: FH, fontSize: 44, bold: true, color: INK, margin: 0,
  });
  s.addText("The system I inherited, and where the P4 path attaches to it", {
    x: M, y: 3.72, w: 11.0, h: 0.62,
    fontFace: FB, fontSize: 20, color: MUTED, margin: 0, lineSpacingMultiple: 1.15,
  });
  s.addShape("line", { x: M, y: 4.66, w: 1.1, h: 0.01, line: { color: ACCENT, width: 2 } });

  pageNum(s);
}

// ============================================================
// Page 4 — Background
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  pageTitle(s, "Background: the system, and the task",
    "NDTwin is a network digital twin — a live model of a running network, kept in step with it");

  const LW2 = 7.05;
  let y = 2.24;
  const points = [
    { h: "A C++ kernel holds the model",
      b: "It owns the topology graph, ingests sFlow telemetry, tracks flows and link usage, and answers queries about the live network." },
    { h: "Seven components depend on it",
      b: "Every one of them reaches the kernel only through the /ndt/ HTTP API — no shared memory, no shared files, no other channel." },
    { h: "The existing system drove OVS",
      b: "Mininet with Open vSwitch, controlled by Ryu. Built by the lab before me; treated here as the given starting point." },
    { h: "My task",
      b: "Make the same twin drive a P4 / bmv2 data plane as well — without the seven components having to change." },
  ];
  points.forEach((p, i) => {
    s.addText(String(i + 1), {
      x: M, y: y - 0.02, w: 0.32, h: 0.3,
      fontFace: FB, fontSize: 13, bold: true, color: ACCENT, margin: 0,
    });
    s.addText(p.h, {
      x: M + 0.36, y: y - 0.03, w: LW2 - 0.36, h: 0.32,
      fontFace: FB, fontSize: 15.5, bold: true, color: INK, margin: 0,
    });
    s.addText(p.b, {
      x: M + 0.36, y: y + 0.33, w: LW2 - 0.36, h: 0.72,
      fontFace: FB, fontSize: 12.5, color: BODY, margin: 0, lineSpacingMultiple: 1.22,
    });
    y += 1.16;
  });

  // right: the seven consumers
  const RX2 = 8.45, RW2 = 4.03;
  s.addText("The seven consumers", {
    x: RX2, y: 2.18, w: RW2, h: 0.3,
    fontFace: FB, fontSize: 13, bold: true, color: INK, margin: 0,
  });
  s.addShape("line", { x: RX2, y: 2.50, w: RW2, h: 0.01, line: { color: RULE, width: 1 } });

  const consumers = [
    ["Energy-Saving-App", "C++"],
    ["Traffic-Engineering-App", "Python"],
    ["Web-GUI", "React / Node"],
    ["Network-Traffic-Visualizer", "JavaFX"],
    ["Network-State-Recorder", "Python"],
    ["Network-Traffic-Generator", "Python"],
    ["Simulation-Platform-Manager", "C++"],
  ];
  let cy = 2.66;
  consumers.forEach(([name, lang]) => {
    s.addText(name, {
      x: RX2, y: cy, w: RW2 - 1.15, h: 0.24,
      fontFace: FB, fontSize: 11.5, color: BODY, margin: 0,
    });
    s.addText(lang, {
      x: RX2 + RW2 - 1.15, y: cy, w: 1.15, h: 0.24, align: "right",
      fontFace: FB, fontSize: 10.5, color: FAINT, margin: 0,
    });
    cy += 0.30;
  });

  s.addShape("line", { x: RX2, y: cy + 0.06, w: RW2, h: 0.01, line: { color: "EFEFEF", width: 1 } });
  s.addText("All seven read the graph through /ndt/get_graph_data. If that endpoint breaks, all seven break at once.", {
    x: RX2, y: cy + 0.18, w: RW2, h: 0.8,
    fontFace: FB, fontSize: 11, color: MUTED, margin: 0, lineSpacingMultiple: 1.2,
  });

  pageNum(s);
}

// ============================================================
// Page 5 — the original architecture
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  archTop(s);

  // control plane
  aBox(s, 3.63, 5.19, 2.63, 0.40, "SDN controller", { fs: 11 });
  aArrow(s, 4.95, 4.93, 0, 0.26, "both");

  // sFlow, switch to kernel, on both sides
  aArrow(s, 2.11, 5.03, 0, 1.11, "up");
  aText(s, 2.22, 5.28, 0.9, 0.34, "sFlow", { fs: 11 });
  aArrow(s, 8.36, 5.03, 0, 1.09, "up");
  aText(s, 8.47, 5.25, 0.9, 0.34, "sFlow", { fs: 11 });

  // controller to the two fabrics
  aArrow(s, 4.16, 5.65, 0.38, 0.62, "down", { flipH: true });
  aArrow(s, 5.50, 5.65, 0.44, 0.67, "down");
  aText(s, 3.16, 5.85, 1.05, 0.32, "OpenFlow", { fs: 10.5 });
  aText(s, 5.80, 5.84, 1.05, 0.32, "OpenFlow", { fs: 10.5 });

  aDash(s, 0.00, 5.86, 10.05, 0.004);

  // emulated fabric
  aCloud(s, 0.30, 6.24, 4.39, 1.15);
  aText(s, 0.04, 5.85, 1.9, 0.55, "Emulated Network\n(Mininet)", { fs: 11 });
  aBox(s, 0.87, 6.52, 0.72, 0.49, "Open vSwitch", { fs: 9 });
  aBox(s, 2.05, 6.71, 0.80, 0.49, "Open vSwitch", { fs: 9 });
  aBox(s, 3.19, 6.37, 0.84, 0.47, "Open vSwitch", { fs: 9 });
  s.addShape("line", { x: 1.59, y: 6.81, w: 0.46, h: 0.10, line: { color: LINE, width: 1.2 } });
  s.addShape("line", { x: 1.59, y: 6.50, w: 1.60, h: 0.16, line: { color: LINE, width: 1.2 } });
  s.addShape("line", { x: 2.85, y: 6.60, w: 0.34, h: 0.28, flipV: true, line: { color: LINE, width: 1.2 } });

  aText(s, 4.72, 6.38, 0.6, 0.5, "or", { fs: 13, align: "center" });

  // physical fabric
  aCloud(s, 5.35, 6.23, 4.39, 1.15);
  aText(s, 8.99, 5.81, 1.4, 0.55, "Physical\nNetwork", { fs: 11 });
  aBox(s, 5.83, 6.56, 0.88, 0.49, "Hardware switch", { fs: 9 });
  aBox(s, 7.12, 6.74, 0.93, 0.49, "Hardware switch", { fs: 9 });
  aBox(s, 8.25, 6.38, 0.84, 0.49, "Hardware switch", { fs: 9 });
  s.addShape("line", { x: 6.72, y: 6.87, w: 0.39, h: 0.10, line: { color: LINE, width: 1.2 } });
  s.addShape("line", { x: 6.72, y: 6.50, w: 1.53, h: 0.17, line: { color: LINE, width: 1.2 } });
  s.addShape("line", { x: 8.06, y: 6.63, w: 0.20, h: 0.34, flipV: true, line: { color: LINE, width: 1.2 } });
  aArrow(s, 9.69, 6.56, 0.62, 0, "both");

  pageNum(s);
}

// ============================================================
// Page 6 — the same architecture with the P4 path added
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  archTop(s);

  // --- control plane: Ryu on the left, the new P4 proxy on the right ---
  aBox(s, 1.55, 5.32, 2.40, 0.42, "SDN controller (Ryu)", { fs: 11 });
  aArrow(s, 2.75, 4.96, 0, 0.36, "both");

  aBox(s, 5.85, 5.32, 2.60, 0.42, "P4 proxy agent", { fs: 11, bold: true, line: ACCENT, lw: 1.75 });
  aText(s, 8.52, 5.30, 0.9, 0.24, "new", { fs: 9.5, tc: ACCENT });

  // northbound: the proxy answers in Ryu's shapes and feeds the same collector
  aArrow(s, 6.45, 4.96, 0, 0.36, "both");
  aText(s, 4.45, 5.00, 1.92, 0.28, "Ryu-compatible REST", { fs: 8.5, align: "right" });

  aArrow(s, 7.95, 4.96, 0, 0.36, "up");
  aText(s, 8.06, 5.00, 1.9, 0.28, "sFlow (synthesised)", { fs: 8.5, tc: ACCENT });

  // --- sFlow on the OVS side comes from the switches themselves ---
  aArrow(s, 0.95, 4.96, 0, 1.34, "up");
  aText(s, 1.06, 5.36, 0.9, 0.30, "sFlow", { fs: 11 });

  // --- southbound ---
  aArrow(s, 2.75, 5.74, 0, 0.56, "down");
  aText(s, 2.86, 5.94, 1.05, 0.30, "OpenFlow", { fs: 10.5 });

  aArrow(s, 7.15, 5.74, 0, 0.56, "down", { color: ACCENT });
  aText(s, 7.26, 5.94, 1.2, 0.30, "P4Runtime", { fs: 10.5, tc: ACCENT });

  aDash(s, 0.00, 5.86, 10.05, 0.004);

  // --- OVS fabric ---
  aCloud(s, 0.35, 6.30, 4.05, 1.10);
  aText(s, 0.06, 5.92, 1.9, 0.52, "Emulated Network\n(Mininet)", { fs: 11 });
  aBox(s, 0.88, 6.55, 0.72, 0.46, "Open vSwitch", { fs: 9 });
  aBox(s, 1.98, 6.74, 0.78, 0.46, "Open vSwitch", { fs: 9 });
  aBox(s, 3.05, 6.43, 0.80, 0.46, "Open vSwitch", { fs: 9 });
  s.addShape("line", { x: 1.60, y: 6.84, w: 0.38, h: 0.10, line: { color: LINE, width: 1.2 } });
  s.addShape("line", { x: 1.60, y: 6.55, w: 1.45, h: 0.14, line: { color: LINE, width: 1.2 } });
  s.addShape("line", { x: 2.76, y: 6.66, w: 0.29, h: 0.28, flipV: true, line: { color: LINE, width: 1.2 } });

  aText(s, 4.55, 6.46, 0.6, 0.5, "or", { fs: 13, align: "center" });

  // --- bmv2 fabric (new) ---
  aCloud(s, 5.30, 6.30, 4.05, 1.10);
  aText(s, 8.35, 5.92, 1.62, 0.52, "Emulated Network\n(Mininet, bmv2)", { fs: 11, tc: ACCENT });
  aBox(s, 5.82, 6.55, 0.78, 0.46, "bmv2 switch", { fs: 9, line: ACCENT, lw: 1.5 });
  aBox(s, 6.95, 6.74, 0.78, 0.46, "bmv2 switch", { fs: 9, line: ACCENT, lw: 1.5 });
  aBox(s, 8.02, 6.43, 0.78, 0.46, "bmv2 switch", { fs: 9, line: ACCENT, lw: 1.5 });
  s.addShape("line", { x: 6.60, y: 6.84, w: 0.35, h: 0.10, line: { color: LINE, width: 1.2 } });
  s.addShape("line", { x: 6.60, y: 6.55, w: 1.42, h: 0.14, line: { color: LINE, width: 1.2 } });
  s.addShape("line", { x: 7.73, y: 6.66, w: 0.29, h: 0.28, flipV: true, line: { color: LINE, width: 1.2 } });

  // --- the one sentence this diagram exists to make ---
  s.addText([
    { text: "bmv2 emits no sFlow of its own.", options: { bold: true, breakLine: true } },
    { text: "The proxy synthesises it, so the kernel's collector cannot tell the two fabrics apart.", options: {} },
  ], {
    x: 10.33, y: 5.52, w: 2.77, h: 0.72,
    fontFace: AF, fontSize: 9, color: "000000", margin: 0, lineSpacingMultiple: 1.06,
  });

  pageNum(s);
}

// ============================================================
// Page 7 — Architecture (apps on top, switches at the bottom)
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  pageTitle(s, "Architecture: how P4 attaches to the existing system",
    "The proxy agent impersonates Ryu's northbound API — nothing above the kernel changes");

  const listW = 6.0;
  let y = 2.28;
  listItem(s, M, y, listW, "1", "The proxy speaks Ryu, not the kernel",
    "Topology, /stats/flow and destination paths are returned in Ryu's data shapes, so the kernel issues exactly the requests it has always issued.");
  y += 1.44;
  listItem(s, M, y, listW, "2", "sFlow v5 synthesised in the proxy",
    "bmv2's sampled packets are synthesised into sFlow v5 and sent to the kernel's existing UDP:6343 collector, byte-layout compatible with OVS.");
  y += 1.44;
  listItem(s, M, y, listW, "3", "Result: zero changes above the kernel",
    "Classifier, FlowLinkUsageCollector, every /ndt/ endpoint, the Intent Translator and all 7 downstream apps are untouched.");

  // ---------- diagram: apps top → switches bottom ----------
  const dx = 7.35, dw = 5.15;
  function box(x, y, w, h, text, sub, opts) {
    const o = opts || {};
    s.addShape("rect", {
      x, y, w, h,
      fill: { color: o.fill || "FFFFFF" },
      line: { color: o.line || RULE, width: o.lw || 1 },
    });
    s.addText(
      sub
        ? [{ text, options: { bold: true, fontSize: o.fs || 12.5, color: o.tc || INK, breakLine: true } },
           { text: sub, options: { fontSize: (o.fs || 12.5) - 3, color: o.sc || MUTED } }]
        : text,
      { x: x + 0.08, y, w: w - 0.16, h, align: "center", valign: "middle",
        fontFace: FB, fontSize: o.fs || 12.5, bold: !sub, color: o.tc || INK,
        margin: 0, lineSpacingMultiple: 1.1 }
    );
  }
  // upward arrow (state / telemetry flows up)
  function up(x, yTop, h) {
    s.addShape("line", {
      x, y: yTop, w: 0.01, h,
      flipV: true,
      line: { color: "B4BEC4", width: 1.5, endArrowType: "triangle" },
    });
  }

  const half = (dw - 0.22) / 2;
  const cx1 = dx, cx2 = dx + half + 0.22;

  box(dx, 2.22, dw, 0.56, "7 downstream apps", null, { fill: PANEL });
  up(dx + dw/2, 2.78, 0.36);
  box(dx, 3.14, dw, 0.52, "/ndt/*  HTTP API", null, { fill: PANEL });
  up(dx + dw/2, 3.66, 0.36);
  box(dx, 4.02, dw, 0.78, "NDTwin Kernel", "unchanged",
      { fill: ACCENT_BG, line: ACCENT, lw: 1.5, fs: 15, tc: ACCENT, sc: ACCENT });
  up(cx1 + half/2, 4.80, 0.40);
  up(cx2 + half/2, 4.80, 0.40);
  box(cx1, 5.20, half, 0.68, "Ryu controller", "existing");
  box(cx2, 5.20, half, 0.68, "P4 proxy agent", "new");
  up(cx1 + half/2, 5.88, 0.34);
  up(cx2 + half/2, 5.88, 0.34);
  box(cx1, 6.22, half, 0.5, "OVS switches", null, { fs: 11.5 });
  box(cx2, 6.22, half, 0.5, "bmv2 switches", null, { fs: 11.5 });

  pageNum(s);
}

// ============================================================
// shared helpers for section 1
// ============================================================
function sectionTab(s, label) {
  s.addText(label, {
    x: M, y: 0.28, w: 6.0, h: 0.26,
    fontFace: FB, fontSize: 10.5, bold: true, color: ACCENT, margin: 0, charSpacing: 1.0,
  });
}

// plain framed box used in the small diagrams
function nodeBox(s, x, y, w, h, text, sub, o) {
  o = o || {};
  s.addShape("rect", {
    x, y, w, h,
    fill: { color: o.fill || "FFFFFF" },
    line: { color: o.line || RULE, width: o.lw || 1 },
  });
  s.addText(
    sub
      ? [{ text, options: { bold: true, fontSize: o.fs || 12, color: o.tc || INK, breakLine: true } },
         { text: sub, options: { fontSize: (o.fs || 12) - 2.5, color: o.sc || MUTED, bold: false } }]
      : text,
    { x: x + 0.08, y, w: w - 0.16, h, align: "center", valign: "middle",
      fontFace: FB, fontSize: o.fs || 12, bold: !sub, color: o.tc || INK,
      margin: 0, lineSpacingMultiple: 1.1 }
  );
}
function arrowDown(s, x, y, h) {
  s.addShape("line", { x, y, w: 0.01, h,
    line: { color: "B4BEC4", width: 1.5, endArrowType: "triangle" } });
}

// two-column key/value rows with a hairline under each
function kvRows(s, x, y, w, rows, opt) {
  opt = opt || {};
  const rh = opt.rh || 0.34, kw = opt.kw || 2.6;
  rows.forEach((r, i) => {
    s.addText(r[0], {
      x, y: y + i * rh, w: kw, h: rh, valign: "middle",
      fontFace: opt.mono ? FC : FB, fontSize: opt.ks || 11.5,
      bold: opt.kb !== false, color: opt.kc || INK, margin: 0,
    });
    s.addText(r[1], {
      x: x + kw, y: y + i * rh, w: w - kw - (opt.tw || 0), h: rh, valign: "middle",
      fontFace: FB, fontSize: opt.vs || 11.5, color: BODY, margin: 0,
    });
    if (r[2] !== undefined) {
      s.addText(r[2], {
        x: x + w - (opt.tw || 0.9), y: y + i * rh, w: opt.tw || 0.9, h: rh,
        align: "right", valign: "middle",
        fontFace: FB, fontSize: 11, color: FAINT, margin: 0,
      });
    }
    s.addShape("line", { x, y: y + (i + 1) * rh - 0.02, w, h: 0.01,
      line: { color: "EFEFEF", width: 1 } });
  });
  return y + rows.length * rh;
}

// ============================================================
// Technology stack — moved into the opening
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  pageTitle(s, "The stack", "What the two data planes and the layer between them are built out of");

  const cols = [
    ["Kernel", "C++23", [
      ["CMake", "build, with opt-in sanitizer targets"],
      ["Boost.Beast / Asio / URL", "the /ndt/ HTTP server"],
      ["nlohmann::json", "every request and reply"],
      ["spdlog", "logging, with a level-gated trap of its own"],
      ["libssh", "southbound to hardware switches"],
      ["GTest", "603 cases"],
      ["ASan / TSan", "reproducible sanitizer builds"],
    ]],
    ["P4 data plane", "P4_16", [
      ["v1model architecture", "the target the pipeline compiles for"],
      ["bmv2 simple_switch_grpc", "the software switch"],
      ["p4c-bm2-ss", "the compiler"],
      ["P4Runtime", "gRPC + protobuf control API"],
      ["PRE clone session", "how telemetry samples reach the CPU"],
      ["Mininet", "the fabric the switches run in"],
    ]],
    ["Proxy and control plane", "Python", [
      ["FastAPI / uvicorn", "the proxy's north side"],
      ["grpcio", "the proxy's south side"],
      ["networkx", "graph state and BFS routing"],
      ["Ryu / OpenFlow 1.3", "the API being impersonated"],
      ["sFlow v5", "synthesised, not forwarded"],
      ["LLDP", "link discovery and liveness beacons"],
      ["hypothesis", "property-based topology tests"],
    ]],
  ];

  const cw6 = (CW - 0.9) / 3;
  cols.forEach((c, i) => {
    const x = M + i * (cw6 + 0.45);
    s.addText(c[0], {
      x, y: 2.06, w: cw6 - 1.0, h: 0.32,
      fontFace: FB, fontSize: 15, bold: true, color: INK, margin: 0,
    });
    s.addText(c[1], {
      x: x + cw6 - 1.0, y: 2.08, w: 1.0, h: 0.3, align: "right",
      fontFace: FC, fontSize: 11, color: ACCENT, margin: 0,
    });
    s.addShape("line", { x, y: 2.44, w: cw6, h: 0.01, line: { color: RULE, width: 1 } });

    let yy = 2.58;
    c[2].forEach(([name, note]) => {
      s.addText(name, {
        x, y: yy, w: cw6, h: 0.24,
        fontFace: FB, fontSize: 12, bold: true, color: BODY, margin: 0,
      });
      s.addText(note, {
        x, y: yy + 0.22, w: cw6, h: 0.34,
        fontFace: FB, fontSize: 10.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.08,
      });
      yy += 0.52;
    });
  });

  pageNum(s);
}

// ============================================================
// Page 8 — Scale of the work (lines changed)
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  pageTitle(s, "Scale of the work",
    "377 commits, 2026-07-23 → 2026-08-19, on top of baseline 28b8b13");

  const data = [
    { label: "Documentation",   files: 207, add: 46290, del: 5,
      note: "Runbooks, design and status docs, investigation records" },
    { label: "Tests & tooling", files: 117, add: 25148, del: 0,
      note: "gtest suites, P4-proxy Python tests, the L0–L4 harness" },
    { label: "Kernel (C++)",    files: 56,  add: 6068,  del: 1053,
      note: "39 existing files modified, 17 new" },
    { label: "P4 proxy",        files: 26,  add: 4431,  del: 0,
      note: "All new — P4Runtime client, REST shim, sFlow emitter, P4 pipeline" },
  ];

  const maxAdd = 46290;
  const barX = 4.55, barMaxW = 4.55;
  const filesX = 10.05, delX = 11.35;
  let y = 2.16;

  // column headers
  s.addText("lines added", {
    x: barX, y: 1.90, w: 2.0, h: 0.24,
    fontFace: FB, fontSize: 10.5, color: FAINT, margin: 0, charSpacing: 0.6,
  });
  s.addText("files", {
    x: filesX, y: 1.90, w: 1.1, h: 0.24, align: "right",
    fontFace: FB, fontSize: 10.5, color: FAINT, margin: 0, charSpacing: 0.6,
  });
  s.addText("removed", {
    x: delX, y: 1.90, w: 1.15, h: 0.24, align: "right",
    fontFace: FB, fontSize: 10.5, color: FAINT, margin: 0, charSpacing: 0.6,
  });

  data.forEach(d => {
    s.addText(d.label, {
      x: M, y, w: 3.5, h: 0.3,
      fontFace: FB, fontSize: 15, bold: true, color: INK, margin: 0,
    });
    s.addText(d.note, {
      x: M, y: y + 0.31, w: 3.6, h: 0.46,
      fontFace: FB, fontSize: 10.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.12,
    });

    const w = barMaxW * (d.add / maxAdd);
    s.addShape("rect", {
      x: barX, y: y + 0.05, w, h: 0.28,
      fill: { color: ACCENT }, line: { type: "none" },
    });
    s.addText("+" + d.add.toLocaleString(), {
      x: barX + w + 0.12, y: y + 0.02, w: 1.25, h: 0.32, valign: "middle",
      fontFace: FB, fontSize: 12.5, bold: true, color: ACCENT, margin: 0,
    });

    s.addText(String(d.files), {
      x: filesX, y: y + 0.02, w: 1.1, h: 0.32, align: "right", valign: "middle",
      fontFace: FB, fontSize: 12.5, color: BODY, margin: 0,
    });
    s.addText(d.del ? "−" + d.del.toLocaleString() : "—", {
      x: delX, y: y + 0.02, w: 1.15, h: 0.32, align: "right", valign: "middle",
      fontFace: FB, fontSize: 12.5, color: MUTED, margin: 0,
    });

    y += 0.98;
    s.addShape("line", { x: M, y: y - 0.14, w: CW, h: 0.01, line: { color: "EFEFEF", width: 1 } });
  });

  // total row
  s.addText("Total", {
    x: M, y: y + 0.02, w: 3.5, h: 0.32,
    fontFace: FB, fontSize: 15, bold: true, color: INK, margin: 0,
  });
  s.addText("+81,937", {
    x: barX, y: y + 0.02, w: 2.0, h: 0.32, valign: "middle",
    fontFace: FB, fontSize: 15, bold: true, color: ACCENT, margin: 0,
  });
  s.addText("406", {
    x: filesX, y: y + 0.02, w: 1.1, h: 0.32, align: "right", valign: "middle",
    fontFace: FB, fontSize: 15, bold: true, color: INK, margin: 0,
  });
  s.addText("−1,058", {
    x: delX, y: y + 0.02, w: 1.15, h: 0.32, align: "right", valign: "middle",
    fontFace: FB, fontSize: 15, color: MUTED, margin: 0,
  });

  // footnote
  s.addText("Diffed against baseline 28b8b13. Comment lines, blank lines and build artefacts are excluded; intelligent_router.py is excluded as the lab's pre-existing Ryu controller.", {
    x: M, y: 6.72, w: CW, h: 0.34,
    fontFace: FB, fontSize: 11, color: MUTED, margin: 0,
  });

  pageNum(s);
}

// ============================================================
// Page 10 — section divider: New capabilities
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };

  s.addText("SECTION 1", {
    x: M, y: 2.16, w: 11.0, h: 0.42,
    fontFace: FB, fontSize: 16, color: ACCENT, margin: 0, charSpacing: 1.2,
  });
  s.addText("New capabilities", {
    x: M, y: 2.72, w: 11.0, h: 0.95,
    fontFace: FH, fontSize: 44, bold: true, color: INK, margin: 0,
  });
  s.addText("The P4 pipeline, the proxy agent, telemetry synthesis, liveness, failover, power", {
    x: M, y: 3.72, w: 11.0, h: 0.62,
    fontFace: FB, fontSize: 20, color: MUTED, margin: 0, lineSpacingMultiple: 1.15,
  });
  s.addShape("line", { x: M, y: 4.66, w: 1.1, h: 0.01, line: { color: ACCENT, width: 2 } });

  pageNum(s);
}

// ============================================================
// Page 11 — The P4 pipeline
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, "1 · NEW CAPABILITIES");
  pageTitle(s, "The P4 pipeline",
    "Phase 4 — ndtwin_switch.p4, extended from a forwarding table into something that produces the same signal OVS does");

  const LW4 = 6.9;
  let y = 2.32;
  [
    ["A ternary 5-tuple table, ahead of LPM",
     "flow_5tuple carries a real priority and is evaluated before ipv4_lpm, so a specific flow rule wins over the default route rather than depending on table order."],
    ["Non-IPv4 frames are no longer dropped",
     "ARP, TCP, UDP and ICMP are parsed, and an L2 table forwards what the IPv4 path cannot. Before this, anything that was not IPv4 disappeared silently."],
    ["Telemetry is generated in the pipeline",
     "Direct and per-port counters, a TTL guard, and 1-in-256 clone-to-CPU sampling — the source of every flow sample the kernel later sees."],
  ].forEach(([h, b], i) => {
    listItem(s, M, y, LW4, String(i + 1), h, b);
    y += 1.42;
  });

  // right: pipeline diagram
  const RX4 = 8.15, RW4 = 4.33;
  let py = 2.28;
  const stages = [
    ["Parser", "Ethernet · ARP · IPv4 · TCP / UDP / ICMP", {}],
    ["flow_5tuple", "ternary · real priority", { fill: ACCENT_BG, line: ACCENT, tc: ACCENT, sc: ACCENT }],
    ["ipv4_lpm", "longest-prefix match", {}],
    ["l2_forward", "exact · non-IPv4 frames", {}],
    ["Egress", "TTL guard · counters · 1-in-256 clone to CPU", {}],
  ];
  stages.forEach(([t, sub, o], i) => {
    nodeBox(s, RX4, py, RW4, 0.60, t, sub, Object.assign({ fs: 12 }, o));
    py += 0.60;
    if (i < stages.length - 1) { arrowDown(s, RX4 + RW4 / 2, py, 0.28); py += 0.28; }
  });

  s.addText("482 lines of P4_16 / v1model, compiled with p4c-bm2-ss.", {
    x: RX4, y: py + 0.24, w: RW4, h: 0.3,
    fontFace: FB, fontSize: 11, color: MUTED, margin: 0,
  });

  pageNum(s);
}

// ============================================================
// Page 12 — Inside the pipeline
// Same drawing style as the architecture diagrams: Arial, black
// 1pt frames, white fill, ACCENT only on what this project added.
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, "1 · NEW CAPABILITIES");
  pageTitle(s, "Inside the pipeline",
    "What a packet actually meets, in the order it meets it");

  // ---------- left column: three short notes ----------
  const LX = M, LW = 3.05;
  let ly = 2.32;
  [
    ["Order is the design",
     "flow_5tuple is consulted before ipv4_lpm, so a specific rule beats the default route without depending on table order."],
    ["Two exits before routing",
     "A packet_out from the controller leaves immediately; LLDP goes to the CPU. Neither reaches the forwarding tables."],
    ["Cloning is not ours",
     "The ingress block only marks a packet. The Traffic Manager performs the copy, and that stage is not programmable."],
  ].forEach(([h, b]) => {
    s.addText(h, {
      x: LX, y: ly, w: LW, h: 0.3,
      fontFace: FB, fontSize: 13, bold: true, color: INK, margin: 0,
    });
    s.addText(b, {
      x: LX, y: ly + 0.30, w: LW, h: 1.0,
      fontFace: FB, fontSize: 11.5, color: BODY, margin: 0, lineSpacingMultiple: 1.2,
    });
    ly += 1.46;
  });

  // ---------- right: the diagram ----------
  const DX = 3.95, DW = 8.5;
  const CX = DX + DW / 2;

  function stageBox(x, y, w, h, o) {
    o = o || {};
    s.addShape("rect", {
      x, y, w, h,
      fill: { color: o.fill || "FFFFFF" },
      line: { color: o.line || LINE, width: o.lw || 1 },
    });
  }
  // label sitting on the frame's upper edge, like a header comment
  function frameTitle(x, y, text) {
    const w = 0.20 + text.length * 0.088;
    s.addShape("rect", { x, y: y - 0.115, w, h: 0.23, fill: { color: "FFFFFF" }, line: { type: "none" } });
    s.addText(text, {
      x, y: y - 0.115, w, h: 0.23, align: "center", valign: "middle",
      fontFace: AF, fontSize: 11, bold: true, color: INK, margin: 0,
    });
  }
  function row(x, y, w, parts, fs) {
    s.addText(parts, {
      x, y, w, h: 0.26, valign: "middle",
      fontFace: FC, fontSize: fs || 10.5, color: BODY, margin: 0,
    });
  }
  function vArrow(x, y, h) {
    s.addShape("line", { x, y, w: 0.008, h,
      line: { color: "000000", width: 1.1, endArrowType: "triangle" } });
  }

  // Parser
  stageBox(DX, 2.00, DW, 0.42);
  s.addText([
    { text: "Parser", options: { bold: true, fontSize: 11.5, color: INK } },
    { text: "     Ethernet · ARP · IPv4 · TCP / UDP / ICMP", options: { fontSize: 10.5, color: MUTED } },
  ], { x: DX + 0.24, y: 2.00, w: DW - 0.48, h: 0.42, valign: "middle", fontFace: AF, margin: 0 });
  vArrow(CX, 2.42, 0.22);

  // MyIngress
  const IY = 2.64, IH = 2.50;
  stageBox(DX, IY, DW, IH);
  frameTitle(DX + 0.55, IY, "MyIngress");

  let ry = IY + 0.20;
  row(DX + 0.30, ry, DW - 0.6, [
    { text: "packet_out?", options: { color: INK, bold: true } },
    { text: "  →  leave on the port the controller named, return", options: { fontFace: FB, fontSize: 11, color: BODY } },
  ]);
  ry += 0.36;

  row(DX + 0.30, ry, DW - 0.6, [
    { text: "IPv4?", options: { color: INK, bold: true } },
    { text: "  →  ", options: { color: BODY } },
    { text: "flow_5tuple", options: { color: ACCENT, bold: true } },
    { text: "   ternary, real priority", options: { fontFace: FB, fontSize: 10.5, color: MUTED } },
  ]);
  ry += 0.25;
  row(DX + 1.45, ry, DW - 1.75, [
    { text: "miss  →  ipv4_lpm", options: { color: BODY } },
    { text: "   longest-prefix match", options: { fontFace: FB, fontSize: 10.5, color: MUTED } },
  ]);
  ry += 0.31;

  row(DX + 0.30, ry, DW - 0.6, [
    { text: "LLDP?", options: { color: INK, bold: true } },
    { text: "  →  send_to_cpu", options: { color: BODY } },
    { text: "   link discovery", options: { fontFace: FB, fontSize: 10.5, color: MUTED } },
  ]);
  ry += 0.28;
  row(DX + 0.30, ry, DW - 0.6, [
    { text: "anything else?", options: { color: INK, bold: true } },
    { text: "  →  ", options: { color: BODY } },
    { text: "l2_forward", options: { color: ACCENT, bold: true } },
    { text: "   exact — non-IPv4 frames are no longer dropped", options: { fontFace: FB, fontSize: 10.5, color: MUTED } },
  ]);
  ry += 0.36;

  s.addShape("line", { x: DX + 0.30, y: ry - 0.04, w: DW - 0.6, h: 0.004,
    line: { color: "E2E2E2", width: 1 } });
  ry += 0.08;
  row(DX + 0.30, ry, DW - 0.6, [
    { text: "TTL guard", options: { color: ACCENT, bold: true } },
    { text: "   inside the ipv4_forward action", options: { fontFace: FB, fontSize: 10.5, color: MUTED } },
  ]);
  ry += 0.27;
  row(DX + 0.30, ry, DW - 0.6, [
    { text: "1-in-256", options: { color: ACCENT, bold: true } },
    { text: "  →  clone_preserving_field_list(I2E)", options: { color: BODY } },
  ]);

  vArrow(CX, IY + IH, 0.22);

  // Traffic Manager — not ours
  const TY = IY + IH + 0.22;
  stageBox(DX + 1.50, TY, DW - 3.0, 0.42, { fill: "F2F2F2", line: "9A9A9A" });
  s.addText([
    { text: "Traffic Manager", options: { bold: true, fontSize: 11, color: "3A3A3A" } },
    { text: "     not programmable — the copy actually happens here", options: { fontSize: 10, color: MUTED } },
  ], { x: DX + 1.62, y: TY, w: DW - 3.24, h: 0.42, align: "center", valign: "middle",
       fontFace: AF, margin: 0 });
  vArrow(CX, TY + 0.42, 0.22);

  // MyEgress
  const EY = TY + 0.64, EH = 0.80;
  stageBox(DX, EY, DW, EH);
  frameTitle(DX + 0.55, EY, "MyEgress");

  row(DX + 0.30, EY + 0.20, DW - 0.6, [
    { text: "is this a clone?", options: { color: INK, bold: true } },
    { text: "  →  attach the packet_in header, and do not count it", options: { color: BODY } },
  ]);
  row(DX + 0.30, EY + 0.48, DW - 0.6, [
    { text: "otherwise", options: { color: INK, bold: true } },
    { text: "         →  egress_port_counter", options: { color: BODY } },
  ]);

  s.addText("482 lines of P4_16 / v1model, compiled with p4c-bm2-ss.", {
    x: DX, y: EY + EH + 0.14, w: 7.5, h: 0.3,
    fontFace: FB, fontSize: 11, color: MUTED, margin: 0,
  });

  pageNum(s);
}
// ============================================================
// Page 13 — The P4 proxy agent
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, "1 · NEW CAPABILITIES");
  pageTitle(s, "The P4 proxy agent",
    "A FastAPI service that answers in Ryu's shapes on the north side and speaks P4Runtime on the south");

  const LW5 = 5.55;
  let y = 2.30;
  [
    ["Ryu's northbound API, reimplemented",
     "/v1.0/topology/*, /stats/flowentry/*, /stats/flow/<dpid> and destination paths, all returned in the exact shapes Ryu produces — including its string-action flow format."],
    ["P4Runtime on the south side",
     "gRPC to bmv2's simple_switch_grpc. Switch connections are opened concurrently at startup, and every unary call carries a deadline so one dead switch cannot stall the rest."],
    ["Only /p4/ is new vocabulary",
     "Where Ryu has no equivalent to impersonate — switch liveness — the endpoint is namespaced under /p4/ rather than pretending to be something Ryu offers."],
  ].forEach(([h, b], i) => {
    listItem(s, M, y, LW5, String(i + 1), h, b);
    y += 1.50;
  });

  // right: module table
  const RX5 = 6.95, RW5 = 5.53;
  s.addText("Modules", {
    x: RX5, y: 2.20, w: 3.0, h: 0.28,
    fontFace: FB, fontSize: 13, bold: true, color: INK, margin: 0,
  });
  s.addText("lines", {
    x: RX5 + RW5 - 0.9, y: 2.22, w: 0.9, h: 0.26, align: "right",
    fontFace: FB, fontSize: 10.5, color: FAINT, margin: 0,
  });
  s.addShape("line", { x: RX5, y: 2.52, w: RW5, h: 0.01, line: { color: RULE, width: 1 } });

  kvRows(s, RX5, 2.62, RW5, [
    ["topology_manager.py", "Graph state, BFS routing, LLDP beacons", "1,392"],
    ["p4_client.py", "P4Runtime gRPC, clone session, packet-in split", "587"],
    ["sflow_emitter.py", "sFlow v5 synthesis", "448"],
    ["ryu_topology.py", "/v1.0/topology/* in Ryu's shapes", "338"],
    ["main.py", "Startup, concurrent switch connect", "305"],
    ["api_routes.py", "/stats/flowentry/*, /p4/*", "256"],
    ["ryu_flow_stats.py", "/stats/flow/<dpid>, string-action form", "190"],
    ["kernel_notifier.py", "Pushes switch and link events north", "144"],
  ], { rh: 0.355, kw: 1.95, mono: true, ks: 10.5, vs: 10.5, tw: 0.72 });

  s.addText("Current file sizes, not diff counts.", {
    x: RX5, y: 5.62, w: RW5, h: 0.28,
    fontFace: FB, fontSize: 10.5, color: FAINT, margin: 0,
  });

  pageNum(s);
}

// ============================================================
// Page 14 — sFlow synthesis
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, "1 · NEW CAPABILITIES");
  pageTitle(s, "sFlow synthesis, and how it was proven",
    "bmv2 emits no sFlow of its own — so the proxy manufactures it, byte-compatible with what OVS sends");

  const LW6 = 6.6;
  let y = 2.30;
  [
    ["Valid sFlow was not enough",
     "The kernel's decoder is a hand-rolled fixed-word-offset parser, not a general sFlow library. The datagram must have the same shape OVS produces — two flow records, extended_switch then raw header."],
    ["Agent addresses come from the same file",
     "The kernel attributes a sample to an edge by AgentKey{agentIP, port}. An address it does not recognise yields telemetry attributed to nothing, with no error — so the emitter reads the topology JSON the kernel reads."],
    ["Proven by cross-language round trip",
     "The Python emitter's real output is fed through the actual C++ parser the kernel uses, and separately compared byte for byte against datagrams captured from a working OVS run."],
  ].forEach(([h, b], i) => {
    listItem(s, M, y, LW6, String(i + 1), h, b);
    y += 1.52;
  });

  // right: round-trip diagram
  const RX6 = 7.85, RW6 = 4.63;
  let ry = 2.34;
  nodeBox(s, RX6, ry, RW6, 0.6, "sflow_emitter.py", "Python — synthesised datagram", { fs: 12 });
  ry += 0.6; arrowDown(s, RX6 + RW6 / 2, ry, 0.38); ry += 0.38;
  nodeBox(s, RX6, ry, RW6, 0.6, "The kernel's C++ sFlow parser", "the real one, not a stub",
          { fs: 12, fill: ACCENT_BG, line: ACCENT, tc: ACCENT, sc: ACCENT });
  ry += 0.6; arrowDown(s, RX6 + RW6 / 2, ry, 0.38); ry += 0.38;
  nodeBox(s, RX6, ry, RW6, 0.6, "Parsed flow matches what was sent", null, { fs: 12 });

  ry += 0.98;
  s.addText("Two independent checks", {
    x: RX6, y: ry, w: RW6, h: 0.28,
    fontFace: FB, fontSize: 11.5, bold: true, color: INK, margin: 0,
  });
  s.addShape("line", { x: RX6, y: ry + 0.30, w: RW6, h: 0.01, line: { color: RULE, width: 1 } });
  kvRows(s, RX6, ry + 0.40, RW6, [
    ["Round trip", "test_SFlowEmitterRoundtrip.cpp"],
    ["Byte compare", "test_sflow_emitter.py vs OVS capture"],
  ], { rh: 0.34, kw: 1.5, ks: 11, vs: 10.5 });

  pageNum(s);
}

// ============================================================
// Page 15 — Telemetry sample path
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, "1 · NEW CAPABILITIES");
  pageTitle(s, "The telemetry sample path",
    "From a sampled packet in the pipeline to a flow the kernel can attribute");

  const LW7 = 6.5;
  let y = 2.30;
  [
    ["A PRE clone session, programmed over P4Runtime",
     "Session 250 is what the pipeline clones sampled packets into. It lives in the pipeline's PRE, so bmv2 rejects it if no pipeline is loaded — the proxy programs it only after it has pushed the config itself."],
    ["Samples and packet-ins share one channel",
     "Both arrive as packet_in. They are separated by a reason field, and the split matters for load as well as correctness: sampling is 1-in-256 of all traffic, so letting samples reach the LLDP parser would bury discovery."],
    ["A trap worth naming",
     "A third controller header compiles cleanly but is silently ignored — P4Runtime matches controller headers by name, and only knows packet_in and packet_out."],
  ].forEach(([h, b], i) => {
    listItem(s, M, y, LW7, String(i + 1), h, b);
    y += 1.52;
  });

  const RX7 = 7.75, RW7 = 4.73;
  let ry = 2.34;
  const chain = [
    ["bmv2 pipeline", "1-in-256 clone to CPU"],
    ["PRE clone session 250", "programmed over P4Runtime"],
    ["packet_in", "split on reason"],
  ];
  chain.forEach(([t, sub], i) => {
    nodeBox(s, RX7, ry, RW7, 0.62, t, sub, { fs: 12 });
    ry += 0.62;
    arrowDown(s, RX7 + RW7 / 2, ry, 0.34); ry += 0.34;
  });

  const halfW = (RW7 - 0.2) / 2;
  nodeBox(s, RX7, ry, halfW, 0.62, "Telemetry", "→ sFlow emitter",
          { fs: 11.5, fill: ACCENT_BG, line: ACCENT, tc: ACCENT, sc: ACCENT });
  nodeBox(s, RX7 + halfW + 0.2, ry, halfW, 0.62, "LLDP", "→ discovery", { fs: 11.5 });
  ry += 0.62;

  s.addText("Verified on ten live bmv2 switches: 2,700 packets over ten hops produced 107 samples against a model prediction of 105.", {
    x: RX7, y: ry + 0.30, w: RW7, h: 0.8,
    fontFace: FB, fontSize: 11, color: MUTED, margin: 0, lineSpacingMultiple: 1.2,
  });

  pageNum(s);
}

// ============================================================
// Flow-diagram primitives — same look as the architecture pages
// ============================================================
function fBox(s, x, y, w, h, o) {
  o = o || {};
  s.addShape("rect", {
    x, y, w, h,
    fill: { color: o.fill || "FFFFFF" },
    line: { color: o.line || LINE, width: o.lw || 1, dashType: o.dash || "solid" },
  });
}
function fTxt(s, x, y, w, h, text, o) {
  o = o || {};
  s.addText(text, {
    x, y, w, h, align: o.align || "left", valign: o.valign || "middle",
    fontFace: o.ff || AF, fontSize: o.fs || 10, bold: !!o.bold,
    color: o.tc || "000000", margin: 0, lineSpacingMultiple: o.ls || 0.95,
  });
}
function fArrow(s, x, y, w, h, dir, o) {
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
function fDash(s, x, y, w, h) {
  s.addShape("line", { x, y, w, h, line: { color: "808080", width: 1, dashType: "dash" } });
}
function fHeader(s, title, sub) {
  fTxt(s, 0.45, 0.50, 11.5, 0.34, title, { fs: 15, bold: true });
  fTxt(s, 0.45, 0.84, 12.0, 0.26, sub, { fs: 9.5, tc: MUTED });
}
// a step in the flow: heading line, then detail
function fStep(s, x, y, w, h, head, detail, o) {
  o = o || {};
  fBox(s, x, y, w, h, { fill: o.fill || "FFFFFF", line: o.line || LINE, lw: o.lw || 1 });
  if (detail) {
    fTxt(s, x + 0.14, y + 0.05, w - 0.28, h * 0.46, head,
      { fs: o.hfs || 10, bold: true, tc: o.tc || "000000", ff: o.hff || AF, valign: "middle" });
    fTxt(s, x + 0.14, y + h * 0.46, w - 0.28, h * 0.50 - 0.02, detail,
      { fs: o.dfs || 8, tc: MUTED, valign: "top", ls: 0.94 });
  } else {
    fTxt(s, x + 0.14, y, w - 0.28, h, head,
      { fs: o.hfs || 10, bold: true, tc: o.tc || "000000", ff: o.hff || AF, align: o.align || "left" });
  }
}
// a yes/no test: same box, but the condition is set in code face
function fTest(s, x, y, w, h, cond, note) {
  fBox(s, x, y, w, h, { fill: PANEL, lw: 1.25 });
  fTxt(s, x + 0.14, y + 0.04, w - 0.28, h * 0.52, cond, { fs: 9.5, bold: true, ff: FC, valign: "middle" });
  if (note) fTxt(s, x + 0.14, y + h * 0.52, w - 0.28, h * 0.44, note, { fs: 8, tc: MUTED, valign: "top", ls: 0.94 });
}
function fBranch(s, x, y, label, o) {
  o = o || {};
  fTxt(s, x, y, o.w || 0.42, o.h || 0.16, label, { fs: 7.5, tc: o.tc || MUTED, align: o.align || "left" });
}

// ============================================================
// Page 16 — Liveness, as the decision it actually is
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, "1 · NEW CAPABILITIES");
  fHeader(s,
    "Liveness: how the twin decides a bmv2 switch is alive",
    "Two independent kinds of evidence, and a verdict that is allowed to come back “cannot tell”");

  // ---- evidence, gathered by the proxy ----
  fTxt(s, 0.85, 1.12, 5.0, 0.20, "GATHERED BY THE PROXY", { fs: 7.5, tc: ACCENT, bold: true });
  fStep(s, 0.85, 1.34, 4.60, 0.62, "p4_client.probe()  — every 2 s",
    "GetForwardingPipelineConfig with COOKIE_ONLY: the cheapest request P4Runtime has,\nand a real answer from the switch.   →  probe_ok, probe_age_s",
    { fill: ACCENT_BG, line: ACCENT, lw: 1.25, hff: FC, hfs: 9.5, tc: ACCENT, dfs: 7.5 });
  fStep(s, 6.05, 1.34, 4.60, 0.62, "an LLDP beacon arrives",
    "packet_in with reason = LLDP, recorded unconditionally rather than\nonly when the edge is new.   →  last_lldp_age_s",
    { fill: ACCENT_BG, line: ACCENT, lw: 1.25, hff: FC, hfs: 9.5, tc: ACCENT, dfs: 7.5 });

  fArrow(s, 3.15, 1.96, 0, 0.20, "plain");
  fArrow(s, 8.35, 1.96, 0, 0.20, "plain");
  fArrow(s, 3.15, 2.16, 5.20, 0, "plain");
  fArrow(s, 5.75, 2.16, 0, 0.22, "down");

  fStep(s, 3.30, 2.38, 4.90, 0.38, "GET /p4/switch_state   —   evidence, not a verdict", null,
    { fill: ACCENT_BG, line: ACCENT, lw: 1.25, hff: FC, hfs: 9.5, tc: ACCENT, align: "center" });

  fArrow(s, 5.75, 2.76, 0, 0.26, "down");
  fTxt(s, 5.92, 2.76, 4.4, 0.24, "the kernel polls this and decides — nothing above this line changes",
    { fs: 7.5, tc: MUTED });

  fDash(s, 0.45, 3.02, 12.53, 0);
  fTxt(s, 8.30, 3.08, 4.20, 0.20, "DECIDED BY THE KERNEL", { fs: 7.5, tc: "000000", bold: true, align: "right" });

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
    fTest(s, TX, y, TW, H, cond, note);
    // the branch that leaves the chain
    fArrow(s, TX + TW, y + H / 2, VX - (TX + TW), 0, "right");
    fBranch(s, TX + TW + 0.10, y + H / 2 - 0.22, i === 1 ? "yes" : (i === 0 ? "yes" : "yes"));
    fBox(s, VX, y + H / 2 - 0.20, VW, 0.40, { line: vc, lw: verdict === "UP" ? 1.6 : 1.1, fill: verdict === "UP" ? ACCENT_BG : "FFFFFF" });
    fTxt(s, VX, y + H / 2 - 0.20, VW, 0.40, verdict, { fs: 10.5, bold: true, tc: vc, align: "center" });
    fTxt(s, NX, y + H / 2 - 0.34, NW, 0.68, why, { fs: 7.5, tc: MUTED, ls: 0.94 });
    if (i < rows.length) {
      fArrow(s, TX + TW / 2, y + H, 0, PITCH - H, "down");
      fBranch(s, TX + TW / 2 + 0.08, y + H + 0.02, "no");
    }
    y += PITCH;
  });

  // terminal
  fBox(s, TX, y, TW, 0.44, { line: WARNC, lw: 1.6 });
  fTxt(s, TX, y, TW, 0.44, "DOWN   —   asked, and nothing else disagreed",
    { fs: 10.5, bold: true, tc: WARNC, align: "center" });
  fTxt(s, NX, y - 0.08, NW, 0.60,
    "Four ways to fail to know, and only one way to be told a switch is dead.",
    { fs: 7.5, tc: MUTED, ls: 0.94 });

  // ---- what each verdict does to the graph ----
  fBox(s, 0.85, 6.92, 11.65, 0.38, { fill: PANEL, line: "D0D0D0" });
  fTxt(s, 1.05, 6.92, 3.4, 0.38, "Up  →  setVertexUp", { fs: 9, ff: FC, tc: ACCENT });
  fTxt(s, 4.45, 6.92, 3.4, 0.38, "Down  →  setVertexDown", { fs: 9, ff: FC, tc: WARNC });
  fTxt(s, 7.85, 6.92, 4.5, 0.38, "Unknown  →  the graph is not touched", { fs: 9, ff: FC, tc: "000000", bold: true });

  pageNum(s);
}

// ============================================================
// Page 17 — Failover, from a missing beacon to a new route
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, "1 · NEW CAPABILITIES");
  fHeader(s,
    "Failover: what turns a missing beacon into a new route",
    "bmv2 raises no link-down signal, so the absence of a packet the proxy sent itself is the only evidence there is");

  const SX = 1.10, SW = 6.60, NX = 8.20, NW = 4.30;
  let y = 1.06;
  const P = 0.72;

  // 1
  fStep(s, SX, y, SW, 0.56, "Beacon out   —   every 5 s",
    "TopologyManager sends one LLDP frame out of every port of every switch, as a packet_out.",
    { fill: ACCENT_BG, line: ACCENT, lw: 1.25, tc: ACCENT });
  fArrow(s, SX + SW / 2, y + 0.56, 0, P - 0.56, "down"); y += P;

  // 2
  fStep(s, SX, y, SW, 0.56, "Beacon in",
    "The neighbour’s pipeline sends it to the CPU port. It arrives as packet_in with reason = LLDP,\nand stamps the arrival time of that one link direction.",
    { fill: ACCENT_BG, line: ACCENT, lw: 1.25, tc: ACCENT });
  fArrow(s, SX + SW / 2, y + 0.56, 0, P - 0.56, "down"); y += P;

  // 3 — the watchdog loop
  const WD_Y = y;
  fStep(s, SX, y, SW, 0.42, "Watchdog pass   —   every 5 s", null, { fill: PANEL });
  fArrow(s, SX + SW / 2, y + 0.42, 0, P - 0.42, "down"); y += P;

  // 4 — the timeout test
  const T1_Y = y;
  fTest(s, SX, y, SW, 0.56, "now  −  last beacon   >   15 s   ?",
    "Three missed beacons. A link that has never spoken at all gets 30 s instead.");
  fTxt(s, NX, y - 0.10, NW, 0.90,
    "Why three and not one. One interval of tolerance would report a failure every time a scan landed just before a beacon did — and a flapping link report is worse than a slow one, because each one tears the edge out of the graph and recomputes every path.",
    { fs: 7.5, tc: MUTED, ls: 0.94 });
  // the "no" branch loops back to the watchdog
  fArrow(s, SX, T1_Y + 0.28, -0.42, 0, "plain", { flipH: true });
  s.addShape("line", { x: SX - 0.42, y: T1_Y + 0.28, w: 0.42, h: 0, line: { color: LINE, width: 1.1 } });
  s.addShape("line", { x: SX - 0.42, y: WD_Y + 0.21, w: 0, h: T1_Y + 0.28 - (WD_Y + 0.21), line: { color: LINE, width: 1.1 } });
  fArrow(s, SX - 0.42, WD_Y + 0.21, 0.42, 0, "right");
  fBranch(s, SX - 0.40, T1_Y + 0.06, "no", { w: 0.40 });
  fArrow(s, SX + SW / 2, y + 0.56, 0, P - 0.56, "down");
  fBranch(s, SX + SW / 2 + 0.08, y + 0.58, "yes", { h: 0.15 }); y += P;

  // 5 — belief flips, kernel is told
  fStep(s, SX, y, SW, 0.56, "The link’s belief flips to down, and the kernel is told",
    "POST /ndt/link_failure_detected, retried on every following pass until the kernel accepts it — a kernel\nthat happened to be restarting would otherwise cost the notification permanently.");
  fArrow(s, SX + SW / 2, y + 0.56, 0, P - 0.56, "down"); y += P;

  // 6 — the over-reporting test
  const T2_Y = y;
  fTest(s, SX, y, SW, 0.60, "every inbound link of that switch went quiet, and  probe_ok  is still true  ?",
    "Then this is a switch-level symptom, not a link failure — report it, but leave its links in the routing graph.");
  fArrow(s, SX + SW, y + 0.30, 0.38, 0, "right");
  fBranch(s, SX + SW + 0.04, y + 0.06, "yes");
  fBox(s, SX + SW + 0.38, y + 0.08, 2.05, 0.44, { line: WARNC, lw: 1.35 });
  fTxt(s, SX + SW + 0.38, y + 0.08, 2.05, 0.44, "reported, not rerouted",
    { fs: 9, bold: true, tc: WARNC, align: "center" });
  fTxt(s, 10.30, y - 0.30, 2.20, 1.40,
    "The one measured failure mode. Taking a bmv2 interface down stalls that switch’s whole packet-in path, so every link into it falls silent at once — one real break produced five down directions, three of them healthy links whose beacons simply had nowhere to be delivered. Reporting may over-report safely; reprogramming may not.",
    { fs: 7, tc: MUTED, ls: 0.94 });
  fArrow(s, SX + SW / 2, y + 0.60, 0, P - 0.60, "down");
  fBranch(s, SX + SW / 2 + 0.08, y + 0.61, "no", { h: 0.13 }); y += P;

  // 7 — reprogram
  fStep(s, SX, y, SW, 0.56, "install_initial_routes()   —   reprogram first",
    "BFS over the graph with the down endpoints removed, so a reinstall cannot recompute the same route\nback into the broken link. insert_ipv4_route falls back to MODIFY, so the pass is idempotent.",
    { fill: ACCENT_BG, line: ACCENT, lw: 1.25, tc: ACCENT, hff: FC, hfs: 9.5 });
  fArrow(s, SX + SW / 2, y + 0.56, 0, P - 0.56, "down"); y += P;

  // 8 — announce
  fStep(s, SX, y, SW, 0.52, "push_destination_paths()   —   announce second",
    "POST /ndt/inform_all_destination_paths. The kernel’s own pull runs every 60 s, so this only buys latency.",
    { fill: ACCENT_BG, line: ACCENT, lw: 1.25, tc: ACCENT, hff: FC, hfs: 9.5 });
  fTxt(s, NX, y - 0.22, NW, 0.96,
    "The order is the point. The push advertises the routes that are installed, so announcing first would publish a snapshot that is honest and already out of date — and the corrected one would not arrive until the next transition.",
    { fs: 7.5, tc: MUTED, ls: 0.94 });

  // ---- the detection budget ----
  fBox(s, 0.85, 6.88, 11.65, 0.42, { fill: PANEL, line: "D0D0D0" });
  fTxt(s, 1.05, 6.88, 11.3, 0.42,
    "Detection costs between the timeout and the timeout plus one scan — 15 to 20 s by the constants, 10.7 to 14 s measured. Which of those two is right is not yet settled, and tuning the timer before it is would leave us unable to say what moved.",
    { fs: 8, tc: MUTED });

  pageNum(s);
}

// ============================================================
// Page 18 — Phase 7: switch power management
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, "1 · NEW CAPABILITIES");
  pageTitle(s, "Phase 7: switch power management",
    "A twin has to be able to switch a node off and take it back again — and the order those steps land in is part of the mechanism");

  const LW9 = 6.6;
  let y = 2.30;
  [
    ["Power off, and keep enough to come back",
     "The ndtwin-p4-power helper shuts a bmv2 switch down entirely while preserving the state needed to restart it. A switch that is off disappears from /v1.0/topology/switches rather than staying in the list pretending to exist."],
    ["Re-adoption after a restart",
     "POST /p4/readopt/{dpid} rebuilds mastership, the pipeline, the clone session and the routes. It is one call because those four have to happen in that order, and a partial re-adoption is worse than none."],
    ["A known 30-second window, stated plainly",
     "Re-adoption reports \"adopted, routes not yet installed\" while the links are still being rediscovered by LLDP. The gap is expected and observable rather than hidden."],
  ].forEach(([h, b], i) => {
    listItem(s, M, y, LW9, String(i + 1), h, b);
    y += 1.52;
  });

  const RX9 = 7.85, RW9 = 4.63;
  s.addText("Live acceptance", {
    x: RX9, y: 2.20, w: RW9, h: 0.28,
    fontFace: FB, fontSize: 13, bold: true, color: INK, margin: 0,
  });
  s.addShape("line", { x: RX9, y: 2.52, w: RW9, h: 0.01, line: { color: RULE, width: 1 } });

  kvRows(s, RX9, 2.62, RW9, [
    ["The switch was held off for", "135 s"],
    ["From power-on to fully re-adopted", "1.50 s"],
    ["The graph was sampled at 10 Hz for", "678 readings"],
    ["Readings that wrongly showed it up", "0"],
  ], { rh: 0.52, kw: 3.05, ks: 11, vs: 11 });

  s.addShape("rect", { x: RX9, y: 4.90, w: 0.035, h: 0.95, fill: { color: ACCENT }, line: { type: "none" } });
  s.addText("Re-adoption is one call, not four, because mastership, pipeline, clone session and routes have to land in that order — and the 10 Hz sampling is there to prove the graph never flickered up in between.", {
    x: RX9 + 0.22, y: 4.86, w: RW9 - 0.22, h: 1.05,
    fontFace: FB, fontSize: 11, color: MUTED, margin: 0, lineSpacingMultiple: 1.2,
  });

  s.addText("Phase 7 and Phase 8 are both complete. Phase 3 — proxy endpoint completion — is the only one not started.", {
    x: M, y: 6.86, w: CW, h: 0.3,
    fontFace: FB, fontSize: 11, color: MUTED, margin: 0,
  });

  pageNum(s);
}

// ============================================================
// helper for the bug section: numbered defect with S/R/F
// ============================================================
function defect(s, x, y, w, n, head, sym, why, fix) {
  s.addText(n, {
    x, y: y - 0.02, w: 0.32, h: 0.3,
    fontFace: FB, fontSize: 13, bold: true, color: ACCENT, margin: 0,
  });
  s.addText(head, {
    x: x + 0.36, y: y - 0.03, w: w - 0.36, h: 0.32,
    fontFace: FB, fontSize: 14.5, bold: true, color: INK, margin: 0,
  });
  const parts = [];
  if (sym) parts.push(
    { text: "Symptom　", options: { bold: true, color: MUTED, fontSize: 10 } },
    { text: sym, options: { color: BODY, fontSize: 11.5, breakLine: !!(why || fix), paraSpaceAfter: 4 } });
  if (why) parts.push(
    { text: "Root cause　", options: { bold: true, color: MUTED, fontSize: 10 } },
    { text: why, options: { color: BODY, fontSize: 11.5, breakLine: !!fix, paraSpaceAfter: 4 } });
  if (fix) parts.push(
    { text: "Fix　", options: { bold: true, color: MUTED, fontSize: 10 } },
    { text: fix, options: { color: BODY, fontSize: 11.5 } });
  s.addText(parts, {
    x: x + 0.36, y: y + 0.32, w: w - 0.36, h: 1.05,
    fontFace: FB, margin: 0, valign: "top", lineSpacingMultiple: 1.16,
  });
}

// short note in the right-hand margin, with an accent rule
function marginNote(s, x, y, w, h, title, body) {
  s.addShape("rect", { x, y, w: 0.03, h, fill: { color: ACCENT }, line: { type: "none" } });
  let ty = y - 0.04;
  if (title) {
    s.addText(title, {
      x: x + 0.22, y: ty, w: w - 0.22, h: 0.26,
      fontFace: FB, fontSize: 11.5, bold: true, color: ACCENT, margin: 0,
    });
    ty += 0.30;
  }
  s.addText(body, {
    x: x + 0.22, y: ty, w: w - 0.22, h: h - (title ? 0.30 : 0),
    fontFace: FB, fontSize: 11, color: BODY, margin: 0, lineSpacingMultiple: 1.2,
  });
}

const TAB2 = "2 · TEST TOOLING AND DOCUMENTATION";

// ============================================================
// Page 30 — section divider: Test tooling and documentation
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };

  s.addText("SECTION 2", {
    x: M, y: 2.16, w: 11.0, h: 0.42,
    fontFace: FB, fontSize: 16, color: ACCENT, margin: 0, charSpacing: 1.2,
  });
  s.addText("Test tooling and documentation", {
    x: M, y: 2.72, w: 11.0, h: 0.95,
    fontFace: FH, fontSize: 44, bold: true, color: INK, margin: 0,
  });
  s.addText("The five-layer harness, what each layer gates, and what was written down", {
    x: M, y: 3.72, w: 11.0, h: 0.62,
    fontFace: FB, fontSize: 20, color: MUTED, margin: 0, lineSpacingMultiple: 1.15,
  });
  s.addShape("line", { x: M, y: 4.66, w: 1.1, h: 0.01, line: { color: ACCENT, width: 2 } });

  pageNum(s);
}

// ============================================================
// Page 29 — Methodology
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, TAB2);
  pageTitle(s, "The methodology is the real technology",
    "Four ideas, each one replacing a judgement call with something that can fail");

  const items = [
    ["Differential testing",
     "The OVS path is known-good, so its behaviour is the specification the P4 path is checked against. No separate spec to write, and no argument about what correct means.",
     "The same method timed the inherited router at 180.75 s \u00d7 3 against 51.8 s now — no claim about anyone\u2019s code required."],
    ["Mutation testing as an acceptance gate",
     "A test does not count until it has been watched failing: break the implementation, see it go red, restore. The evidence is filed per test.",
     "This caught eleven tests that passed while proving nothing at all."],
    ["Allowlist gates",
     "Any warning or OVS/P4 difference not on a list is a failure. Every accepted difference has to be written down as a sentence with a reason.",
     "New problems cannot hide inside old noise."],
    ["Evidence-based design",
     "Liveness has three states, not two. Southbound calls return OpResult, not bool. \"I could not tell\" and \"it failed\" are never allowed to render as \"it worked\".",
     "Liveness on page 16 is the instance of this that carries the most weight."],
  ];

  const cw7 = (CW - 0.6) / 2;
  items.forEach((it, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = M + col * (cw7 + 0.6);
    const yy = 2.26 + row * 2.22;
    s.addText(String(i + 1), {
      x, y: yy - 0.02, w: 0.32, h: 0.3,
      fontFace: FB, fontSize: 13, bold: true, color: ACCENT, margin: 0,
    });
    s.addText(it[0], {
      x: x + 0.36, y: yy - 0.03, w: cw7 - 0.36, h: 0.32,
      fontFace: FB, fontSize: 15, bold: true, color: INK, margin: 0,
    });
    s.addText(it[1], {
      x: x + 0.36, y: yy + 0.34, w: cw7 - 0.36, h: 0.95,
      fontFace: FB, fontSize: 12, color: BODY, margin: 0, lineSpacingMultiple: 1.2,
    });
    s.addShape("rect", { x: x + 0.36, y: yy + 1.36, w: 0.03, h: 0.52,
      fill: { color: ACCENT }, line: { type: "none" } });
    s.addText(it[2], {
      x: x + 0.60, y: yy + 1.32, w: cw7 - 0.60, h: 0.58,
      fontFace: FB, fontSize: 11, color: MUTED, margin: 0, lineSpacingMultiple: 1.18,
    });
  });

  pageNum(s);
}

// ============================================================
// Page 31 — Five-layer test architecture
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, TAB2);
  pageTitle(s, "Five layers, five different questions",
    "Different failure modes surface at different stages, and each layer costs a different amount to run and to debug");

  const rows = [
    ["L0", "Build check", "Does every component still compile?", "seconds–minutes", "no"],
    ["L1", "Unit tests", "Is unit behaviour correct — and still correct in a shared process?", "~2 minutes", "no"],
    ["L2", "API contract", "Does /ndt/* honour its structure, invariants and error paths?", "needs a running stack", "yes"],
    ["L3", "Component contract", "Change one endpoint — which of the seven components break?", "needs a running stack", "yes"],
    ["L4", "Differential", "Does the P4 path behave like the known-good OVS path?", "full stack + traffic", "yes"],
  ];

  const tableRows = [
    [
      { text: "Layer", options: { bold: true, color: "FFFFFF", fill: { color: ACCENT }, fontSize: 11.5 } },
      { text: "The question it answers", options: { bold: true, color: "FFFFFF", fill: { color: ACCENT }, fontSize: 11.5 } },
      { text: "Cost", options: { bold: true, color: "FFFFFF", fill: { color: ACCENT }, fontSize: 11.5 } },
      { text: "Mininet", options: { bold: true, color: "FFFFFF", fill: { color: ACCENT }, fontSize: 11.5 } },
    ],
    ...rows.map((r, i) => [
      { text: r[0] + "   " + r[1], options: { bold: true, color: ACCENT, fontSize: 11.5,
          fill: { color: i % 2 ? "FFFFFF" : "F7F9FA" } } },
      { text: r[2], options: { color: BODY, fontSize: 11, fill: { color: i % 2 ? "FFFFFF" : "F7F9FA" } } },
      { text: r[3], options: { color: MUTED, fontSize: 10.5, fill: { color: i % 2 ? "FFFFFF" : "F7F9FA" } } },
      { text: r[4], options: { color: MUTED, fontSize: 10.5, fill: { color: i % 2 ? "FFFFFF" : "F7F9FA" } } },
    ]),
  ];

  s.addTable(tableRows, {
    x: M, y: 2.16, w: CW,
    colW: [2.45, 5.0, 2.35, 1.83],
    rowH: [0.40, 0.66, 0.66, 0.66, 0.66, 0.66],
    border: { type: "solid", color: "E4EAEE", pt: 1 },
    fontFace: FB, valign: "middle",
    margin: [0.06, 0.12, 0.06, 0.12],
  });

  pageNum(s);
}

// ============================================================
// Page 32 — Test assets
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, TAB2);
  pageTitle(s, "What the suite contains, and what makes it trustworthy",
    "A test count proves nothing on its own — so every test here was watched failing before it was allowed to count");

  const stats = [
    ["603", "gtest cases", "in 47 files"],
    ["453", "P4-proxy tests", "in 17 files"],
    ["243", "kernel-side Python", "in 7 files"],
    ["7", "shell suites", "orchestration and gates"],
  ];
  let sx = M;
  const sw = (CW - 0.6) / 4;
  stats.forEach(([big, cap, sub]) => {
    s.addText(big, {
      x: sx, y: 2.16, w: sw, h: 0.58,
      fontFace: FH, fontSize: 28, bold: true, color: ACCENT, margin: 0,
    });
    s.addText(cap, {
      x: sx, y: 2.76, w: sw, h: 0.26,
      fontFace: FB, fontSize: 12, bold: true, color: INK, margin: 0,
    });
    s.addText(sub, {
      x: sx, y: 3.00, w: sw, h: 0.26,
      fontFace: FB, fontSize: 10.5, color: MUTED, margin: 0,
    });
    sx += sw + 0.2;
  });
  s.addShape("line", { x: M, y: 3.42, w: CW, h: 0.01, line: { color: RULE, width: 1 } });

  let y = 3.64;
  [
    ["Every test ships with the mutation that breaks it",
     "Applied, observed failing, reverted — and the evidence filed in four dated records under doc/audit/. This is what caught eleven tests that passed while proving nothing."],
    ["The tooling's own false passes were fixed",
     "Four of them. unittest counts skipped tests inside \"Ran N\", so a fully-skipped file printed green — and three tests sat below unittest.main(), so they had never executed at all."],
    ["Log output is a pass/fail gate, not a thing to read",
     "check_logs.py fails on any warning or error not on the allowlist, has a FORBID list that overrides it, and treats crash signatures as unconditional failures that no allowlist can excuse."],
  ].forEach(([h, b], i) => {
    listItem(s, M, y, 7.5, String(i + 1), h, b);
    y += 1.24;
  });

  marginNote(s, 8.75, 3.66, 3.73, 1.5, "Why the count moves",
    "426 → 547 → 603 in seven days. That is real growth, not miscounting: three live defects each got a regression test, and four new tool suites arrived with their own.");

  marginNote(s, 8.75, 5.42, 3.73, 1.45, "The claim being made",
    "Not \"we have many tests\". The claim is that each one has been observed failing for the reason it exists — which is a different and checkable statement.");

  pageNum(s);
}

// ============================================================
// Page 33 — Documentation
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, TAB2);
  pageTitle(s, "What was written down",
    "Twenty-four documents under doc/, organised so that the next person has a route through");

  const groups = [
    ["Operational — how to run it", [
      ["full_test_runbook", "the whole stack, end to end"],
      ["ovs_manual_test_runbook", "the OVS round"],
      ["p4_manual_test_runbook", "the P4 round"],
      ["environment_gotchas", "sudo, pgrep, cleanup, ordering"],
      ["testing-manual", "the current consolidated guide"],
    ]],
    ["Design and status", [
      ["p4_bmv2_support_plan", "phase-by-phase plan and status"],
      ["phase7_power_mechanism_design", "the power path"],
      ["ndt_api", "every /ndt/ endpoint, with byte-order and lock-type clarifications"],
      ["HANDOFF", "what is still open"],
    ]],
    ["Investigation records", [
      ["p4runtime-mastership-spec-check", "the conclusion that was withdrawn"],
      ["bmv2-performance-report", "the throughput A/B"],
      ["src-ip-endianness-review", "a field that looked wrong and was not"],
      ["doc/audit/", "wedge trace, mutation evidence, scoped reviews"],
    ]],
  ];

  const gw = (CW - 0.9) / 3;
  groups.forEach((g, i) => {
    const x = M + i * (gw + 0.45);
    s.addText(g[0], {
      x, y: 2.18, w: gw, h: 0.3,
      fontFace: FB, fontSize: 13, bold: true, color: ACCENT, margin: 0,
    });
    s.addShape("line", { x, y: 2.52, w: gw, h: 0.01, line: { color: RULE, width: 1 } });
    let yy = 2.66;
    g[1].forEach(([name, note]) => {
      s.addText(name, {
        x, y: yy, w: gw, h: 0.24,
        fontFace: FC, fontSize: 10.5, color: BODY, margin: 0,
      });
      s.addText(note, {
        x, y: yy + 0.23, w: gw, h: 0.42,
        fontFace: FB, fontSize: 10.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.12,
      });
      yy += 0.68;
    });
  });

  marginNote(s, M, 6.02, CW, 0.95, "The one that matters most is the one listing what is not done",
    "test_coverage_gaps records what has no test yet, and HANDOFF records what is still open — including a defect found and deliberately left unfixed. A handover document that only lists successes is not a handover document.");

  pageNum(s);
}

const TAB3 = "3 · MEASURED RESULTS";

const FIGDIR = "/sessions/hopeful-sharp-hopper/mnt/NDTwin Slide material/figures/";

// one figure, one page. The figures carry their own title and subtitle,
// so the page adds nothing but the section tab and the page number.
function figurePage(file, ar) {
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, TAB3);
  // A figure wider than 2.5:1 is width-starved on a 16:9 page: give it the extra
  // margin and bias the leftover height upwards rather than splitting it evenly.
  const wide = ar > 2.5;
  const maxW = wide ? 12.53 : 12.13, maxH = 5.62;
  const w = Math.min(maxW, maxH * ar), h = w / ar;
  s.addImage({
    path: FIGDIR + file,
    x: (13.333 - w) / 2,
    y: 0.98 + (maxH - h) * (wide ? 0.34 : 0.5),
    w, h,
  });
  pageNum(s);
}

// small placeholder marker for visuals Adam still owes
function pending(s, x, y, w, label) {
  s.addShape("rect", { x, y, w, h: 0.34, fill: { color: "F7F8F9" }, line: { color: RULE, width: 1 } });
  s.addText("TO ADD   " + label, {
    x: x + 0.16, y, w: w - 0.32, h: 0.34, valign: "middle",
    fontFace: FB, fontSize: 10.5, color: MUTED, margin: 0, charSpacing: 0.4,
  });
}

// ============================================================
// Page 34 — section divider: Results on real hardware
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };

  s.addText("SECTION 3", {
    x: M, y: 2.16, w: 11.0, h: 0.42,
    fontFace: FB, fontSize: 16, color: ACCENT, margin: 0, charSpacing: 1.2,
  });
  s.addText("Measured results", {
    x: M, y: 2.72, w: 11.0, h: 0.95,
    fontFace: FH, fontSize: 44, bold: true, color: INK, margin: 0,
  });
  s.addText("Differential testing, failover, load, twin accuracy \u2014 and a live demo", {
    x: M, y: 3.72, w: 11.0, h: 0.62,
    fontFace: FB, fontSize: 20, color: MUTED, margin: 0, lineSpacingMultiple: 1.15,
  });
  s.addShape("line", { x: M, y: 4.66, w: 1.1, h: 0.01, line: { color: ACCENT, width: 2 } });

  pageNum(s);
}

// ============================================================
// Page 35 — L4 differential
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, TAB3);
  pageTitle(s, "The P4 path matches the OVS baseline",
    "L4 differential: the OVS path is the specification, and every difference the P4 path shows has to be justified in writing or it fails");

  const figs = [
    ["PASS", "L4 differential"],
    ["18", "allowlist entries, each with a reason"],
    ["0", "unexplained differences"],
    ["12", "allowlist entries deleted once P4 caught up"],
  ];
  let fx = M;
  const fw = (CW - 0.6) / 4;
  figs.forEach(([big, cap], i) => {
    s.addText(big, {
      x: fx, y: 2.18, w: fw, h: 0.6,
      fontFace: FH, fontSize: 28, bold: true, color: i === 2 ? ACCENT : INK, margin: 0,
    });
    s.addText(cap, {
      x: fx, y: 2.80, w: fw, h: 0.5,
      fontFace: FB, fontSize: 11.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.14,
    });
    fx += fw + 0.2;
  });
  s.addShape("line", { x: M, y: 3.46, w: CW, h: 0.01, line: { color: RULE, width: 1 } });

  let y = 3.68;
  [
    ["The allowlist is the mechanism, not a formality",
     "compare_baseline.py fails on any difference not listed. Each entry is an endpoint, a regex and a reason, so \"P4 cannot do this yet\" has to be written as a sentence."],
    ["Entries are deleted as phases land",
     "Twelve were removed once P4 implemented what they excused — each re-verified against the live system first, not just crossed off."],
  ].forEach(([h, b], i) => {
    listItem(s, M, y, 7.5, String(i + 1), h, b);
    y += 1.42;
  });

  marginNote(s, 8.75, 3.70, 3.73, 2.15, "Why this is the strongest single result",
    "It is the only check that compares two independent implementations of the same behaviour. Unit tests confirm the code does what I thought it should; this confirms the P4 path does what the known-good path does — a claim I could not have written down myself.");

  s.addText("PASS was recorded at dac192b and is stated as of that commit, not as a live status.", {
    x: M, y: 6.60, w: 7.5, h: 0.3,
    fontFace: FB, fontSize: 10.5, color: MUTED, margin: 0,
  });

  pending(s, 8.75, 6.42, 3.73, "comparison output, difference table");

  pageNum(s);
}

// ============================================================
// Failover, measured — four cells
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, TAB3);
  pageTitle(s, "Failover, measured under controlled conditions",
    "One fault model, one script, four cells, forty runs — the outage is timed from a continuous ping, not inferred from logs");

  const rows = [
    ["P4 / 4 hosts",    "10", "13.68 s", "1.6", "11.0 – 16.4", ACCENT],
    ["OVS / 4 hosts",   "10", "15.71 s", "1.5", "13.7 – 18.1", BODY],
    ["P4 / 128 hosts",  "10", "16.59 s", "2.0", "14.3 – 20.8", ACCENT],
    ["OVS / 128 hosts", "10", "51.75 s", "3.3", "47.0 – 56.4", WARNC],
  ];
  const tableRows = [
    ["Cell", "n", "Mean", "SD", "Range"].map(h => (
      { text: h, options: { bold: true, color: "FFFFFF", fill: { color: ACCENT }, fontSize: 11.5 } })),
    ...rows.map((r, i) => {
      const bg = { color: i % 2 ? "FFFFFF" : "F7F9FA" };
      return [
        { text: r[0], options: { bold: true, color: INK, fontSize: 11.5, fill: bg } },
        { text: r[1], options: { color: MUTED, fontSize: 11, fill: bg } },
        { text: r[2], options: { bold: true, color: r[5], fontSize: 11.5, fill: bg } },
        { text: r[3], options: { color: MUTED, fontSize: 11, fill: bg } },
        { text: r[4], options: { color: BODY, fontSize: 11, fill: bg } },
      ];
    }),
  ];
  s.addTable(tableRows, {
    x: M, y: 2.26, w: 7.5,
    colW: [2.35, 0.75, 1.35, 0.95, 2.10],
    rowH: [0.34, 0.46, 0.46, 0.46, 0.46],
    border: { type: "solid", color: "E4EAEE", pt: 1 },
    fontFace: FB, valign: "middle",
    margin: [0.05, 0.12, 0.05, 0.12],
  });

  s.addText([
    { text: "At 4 hosts P4 is 2.0 s faster — 13%.  ", options: { bold: true, color: ACCENT } },
    { text: "Welch t = 2.89, p = 0.0098, 95% CI 0.55 – 3.50 s. At 128 hosts the gap is 3.12\u00d7 and the two ranges do not overlap at all. Every one of the forty runs broke once and then recovered fully.  ", options: { color: BODY } },
    { text: "(9467ea0 / b6b75fa / 213d209)", options: { fontFace: FC, fontSize: 9.5, color: FAINT } },
  ], {
    x: M, y: 4.50, w: 7.5, h: 0.86,
    fontFace: FB, fontSize: 11.5, margin: 0, lineSpacingMultiple: 1.2,
  });

  s.addText("What separating the variables shows", {
    x: M, y: 5.46, w: 7.5, h: 0.3,
    fontFace: FB, fontSize: 13, bold: true, color: INK, margin: 0,
  });
  s.addShape("line", { x: M, y: 5.78, w: 7.5, h: 0.01, line: { color: RULE, width: 1 } });
  s.addText("Scaling 4 → 128 hosts costs OVS 3.29\u00d7 but P4 only 1.21\u00d7, so the interaction is larger than either main effect. \"The data plane is the smallest of the three\" is true at 4 hosts and false at 128 — the mechanism is not established, and the honest statement is that the two control paths degrade differently with scale.", {
    x: M, y: 5.90, w: 7.5, h: 1.0,
    fontFace: FB, fontSize: 11.5, color: BODY, margin: 0, lineSpacingMultiple: 1.2,
  });

  marginNote(s, 8.35, 2.28, 4.13, 2.05, "What makes these hold",
    "Continuous timestamped ping at 5 packets/s, so the outage is measured rather than inferred; the link to break is resolved at run time from the live path; netem re-checked every 5 s; recovery counted only while the fault is still present. \u201cRecovered fully\u201d is a filter rather than an impression \u2014 the raster only accepts a run with exactly one gap longer than a second, and all forty qualified.");

  marginNote(s, 8.35, 4.58, 4.13, 1.90, "128 hosts was assumed to be too heavy",
    "A comment in the topology script said bmv2 might not take it, and that assumption had gone unchecked. It takes it — 10/10 switches up, 16,256 paths converged in 11 s. What actually blocked the cell was four hard-coded four-host lists in three files.");

  s.addText("Single fault, single host pair, single machine. Quote the interval, not the mean.", {
    x: 8.35, y: 6.62, w: 4.13, h: 0.3,
    fontFace: FB, fontSize: 10.5, color: MUTED, margin: 0,
  });

  pageNum(s);
}

// ---- the three failover figures, one page each ----
figurePage("page36_failover-boxplot.png",       1840 / 860);
figurePage("page36_failover-raster.png",        2480 / 880);
figurePage("page36_failover-decomposition.png", 1920 / 980);

// ============================================================
// Page 37 — Throughput ceiling A/B
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, TAB3);
  pageTitle(s, "What the data planes can actually carry",
    "Same fabric, same 3-hop path, same iperf3 script — two bmv2 builds and an OVS control");

  const rows = [
    ["bmv2 — stock build", "-O0, all logging", "~40 Mbps", "24.2 Mbps", "~3.6k pps"],
    ["bmv2 — fast rebuild", "-O3, logging macros disabled", "~460–530 Mbps", "431 Mbps", "~50.8k pps"],
    ["OVS — control", "shaped by TCLink at 1 G", "980 Mbps", "—", "—"],
  ];
  const tableRows = [
    [
      { text: "Build", options: { bold: true, color: "FFFFFF", fill: { color: ACCENT }, fontSize: 11.5 } },
      { text: "Configuration", options: { bold: true, color: "FFFFFF", fill: { color: ACCENT }, fontSize: 11.5 } },
      { text: "UDP delivered", options: { bold: true, color: "FFFFFF", fill: { color: ACCENT }, fontSize: 11.5 } },
      { text: "TCP goodput", options: { bold: true, color: "FFFFFF", fill: { color: ACCENT }, fontSize: 11.5 } },
      { text: "Packet rate", options: { bold: true, color: "FFFFFF", fill: { color: ACCENT }, fontSize: 11.5 } },
    ],
    ...rows.map((r, i) => {
      const bg = { color: i % 2 ? "FFFFFF" : "F7F9FA" };
      return [
        { text: r[0], options: { bold: true, color: INK, fontSize: 11, fill: bg } },
        { text: r[1], options: { color: MUTED, fontSize: 10.5, fill: bg } },
        { text: r[2], options: { color: i === 1 ? ACCENT : BODY, bold: i === 1, fontSize: 11, fill: bg } },
        { text: r[3], options: { color: i === 1 ? ACCENT : BODY, bold: i === 1, fontSize: 11, fill: bg } },
        { text: r[4], options: { color: BODY, fontSize: 11, fill: bg } },
      ];
    }),
  ];
  s.addTable(tableRows, {
    x: M, y: 2.24, w: CW,
    colW: [2.6, 3.1, 2.15, 1.95, 1.83],
    rowH: [0.34, 0.5, 0.5, 0.5],
    border: { type: "solid", color: "E4EAEE", pt: 1 },
    fontFace: FB, valign: "middle",
    margin: [0.06, 0.12, 0.06, 0.12],
  });

  let y = 4.26;
  [
    ["The ceiling is packets, not bits",
     "bmv2 is an interpreted reference implementation; at -O0 with logging macros the per-packet fixed cost dominates. 64-byte and 1400-byte frames hit the same packet rate, which is what identifies the limit."],
    ["The loss is invisible to interface counters",
     "It happens in the first on-path switch's input buffer. h1 sent 89,296, s1-eth3 received 89,296 — and s1-eth1 transmitted 33,456. Nothing in between reports a drop."],
  ].forEach(([h, b], i) => {
    listItem(s, M, y, 7.5, String(i + 1), h, b);
    y += 1.42;
  });

  marginNote(s, 8.75, 4.28, 3.73, 1.5, "The published figure describes neither build",
    "~170 Mbps [2] is 4× above the stock build and ~3× below the fast one, so it is cited as an order of magnitude and nothing more.");

  marginNote(s, 8.75, 6.00, 3.73, 1.0, "What it costs the twin",
    "At 1 Gbps declared, single-flow utilisation caps at ~4% on stock and ~43–53% on fast — so TE's 70% congestion threshold is physically unreachable on stock.");

  pageNum(s);
}

figurePage("page37_throughput-ab.png", 1840 / 760);

// ============================================================
// Page 38 — Load test
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, TAB3);
  pageTitle(s, "210 Mbps sustained, then a link broken underneath it",
    "The earlier runbook only ever loaded one flow at 10 Mbps, and only broke links while idle");

  const figs = [
    ["210 Mbps", "carried, four concurrent flows, five minutes"],
    ["288 / 288", "the graph never moved"],
    ["0", "spurious link events from Ryu"],
    ["2.7% / 0%", "loss on the broken flow / the other three"],
  ];
  let fx = M;
  const fw = (CW - 0.6) / 4;
  figs.forEach(([big, cap], i) => {
    s.addText(big, {
      x: fx, y: 2.18, w: fw, h: 0.58,
      fontFace: FH, fontSize: i === 0 || i === 3 ? 24 : 27, bold: true, color: ACCENT, margin: 0,
    });
    s.addText(cap, {
      x: fx, y: 2.80, w: fw, h: 0.5,
      fontFace: FB, fontSize: 11.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.14,
    });
    fx += fw + 0.2;
  });
  s.addShape("line", { x: M, y: 3.46, w: CW, h: 0.01, line: { color: RULE, width: 1 } });

  let y = 3.68;
  [
    ["Rerouting does not disturb traffic it is not rerouting",
     "Breaking s1-eth2 under load cost 35,445 of 1,337,473 datagrams on the flow using it, and exactly zero on the other three — including the one sharing two switches with it."],
    ["The link-usage metric tracked the load correctly",
     "About 5× for 20× the traffic, which is what the metric's own definition predicts: the denominator grows with the load."],
    ["One measurement points somewhere specific",
     "The stale-path window reproduced at 14 s under load against 13 s idle — which points at a fixed cache period rather than anything load-dependent."],
  ].forEach(([h, b], i) => {
    listItem(s, M, y, 7.5, String(i + 1), h, b);
    y += 1.24;
  });

  marginNote(s, 8.75, 3.70, 3.73, 2.4, "An old warning left standing",
    "The runbook records 100 Mbps starving LLDP badly enough that Ryu deleted 19 healthy links. Not reproduced here — but this was four 50 Mbps flows on different paths at half the per-flow packet rate, which is a different condition. The warning stays until someone reruns it as written.");

  pageNum(s);
}

// ============================================================
// Twin flow-rate accuracy
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, TAB3);
  pageTitle(s, "How accurate the twin's link usage is",
    "Accuracy is not a number here but a curve — the estimate is unbiased, and its spread is the sampling-theory floor");

  const rows = [
    ["1 s",   "20.7", "23.9", "70.9", "75.6"],
    ["10 s",  "8.1",  "7.6",  "25.7", "23.9"],
    ["60 s",  "3.1",  "3.1",  "6.8",  "9.8"],
    ["150 s", "1.9",  "2.0",  "4.9",  "6.2"],
    ["430 s", "1.2",  "1.2",  "—",    "—"],
  ];
  const tableRows = [
    ["Window", "200 Mbit/s  ±%", "theory", "20 Mbit/s  ±%", "theory"].map(h => (
      { text: h, options: { bold: true, color: "FFFFFF", fill: { color: ACCENT }, fontSize: 11 } })),
    ...rows.map((r, i) => {
      const bg = { color: i % 2 ? "FFFFFF" : "F7F9FA" };
      return [
        { text: r[0], options: { bold: true, color: INK, fontSize: 11, fill: bg } },
        { text: r[1], options: { bold: true, color: ACCENT, fontSize: 11, fill: bg } },
        { text: r[2], options: { color: MUTED, fontSize: 11, fill: bg } },
        { text: r[3], options: { bold: true, color: ACCENT, fontSize: 11, fill: bg } },
        { text: r[4], options: { color: MUTED, fontSize: 11, fill: bg } },
      ];
    }),
  ];
  s.addTable(tableRows, {
    x: M, y: 2.30, w: 7.35,
    colW: [1.25, 1.85, 1.20, 1.85, 1.20],
    rowH: [0.34, 0.40, 0.40, 0.40, 0.40, 0.40],
    border: { type: "solid", color: "E4EAEE", pt: 1 },
    fontFace: FB, valign: "middle",
    margin: [0.05, 0.12, 0.05, 0.12],
  });

  let y = 4.66;
  [
    ["Unbiased across 430× of window and 10× of load",
     "Median ratio 0.97 – 1.02 at every window and both loads. Over 3,599 samples the mean reads 205.5 Mbit/s against a true 205.8 — 0.15% out."],
    ["The resolution floor is one sample",
     "quantum = 256 × frame bytes × 8 — per-flow, not a constant: four runs gave 1490, 1490, 1494, 1506 bytes."],
  ].forEach(([h, b], i) => {
    listItem(s, M, y, 7.5, String(i + 1), h, b);
    y += 1.14;
  });

  marginNote(s, 8.75, 2.32, 3.73, 2.15, "The sentence that survives questioning",
    "Not \"we are accurate to X%\" — that number does not exist. The same instrument is ±21% at a one-second window and ±1.2% at 430 s. What can be claimed is: unbiased, with precision set by sample count, exactly as sampling theory predicts [1].");

  marginNote(s, 8.75, 4.74, 3.73, 2.15, "Where it stops working",
    "On a 1 Gbps link a flow below about 3 Mbit/s is invisible and utilization_percent moves in 0.31% steps. A single one-second reading at 20 Mbit/s ranged from 0.15× to 2.38× of truth. And the four-host OVS cell has no sFlow configured at all: it reads zero, with status success.");

  s.addText("Measured at 04b8933 on the OVS 128-host topology, one fixed-rate UDP flow, no other traffic.", {
    x: M, y: 6.96, w: CW - 0.75, h: 0.28,
    fontFace: FB, fontSize: 10, color: MUTED, margin: 0,
  });

  pageNum(s);
}

figurePage("page39_quantisation-ladder.png", 1920 / 1000);

// ============================================================
// Telemetry accuracy — synthesised (P4) vs native (OVS)
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, TAB3);
  pageTitle(s, "Synthesised telemetry against native",
    "bmv2 emits no sFlow of its own, so the proxy manufactures it — this measures whether a manufactured sample is as good as a real one");

  const rows = [
    ["1 s",  "0.965", "0.966", "54.6", "70.9", "75.5"],
    ["2 s",  "1.001", "0.967", "47.5", "51.3", "53.4"],
    ["5 s",  "1.008", "0.989", "29.6", "35.0", "33.8"],
    ["10 s", "1.016", "1.022", "20.1", "25.7", "23.9"],
    ["30 s", "1.008", "0.990", "8.8",  "11.8", "13.8"],
    ["60 s", "1.003", "1.007", "6.3",  "6.8",  "9.7"],
  ];
  const tableRows = [
    ["Window", "P4 median", "OVS median", "P4  ±%", "OVS  ±%", "theory"].map(h => (
      { text: h, options: { bold: true, color: "FFFFFF", fill: { color: ACCENT }, fontSize: 10.5 } })),
    ...rows.map((r, i) => {
      const bg = { color: i % 2 ? "FFFFFF" : "F7F9FA" };
      return [
        { text: r[0], options: { bold: true, color: INK, fontSize: 11, fill: bg } },
        { text: r[1], options: { bold: true, color: ACCENT, fontSize: 11, fill: bg } },
        { text: r[2], options: { color: BODY, fontSize: 11, fill: bg } },
        { text: r[3], options: { bold: true, color: ACCENT, fontSize: 11, fill: bg } },
        { text: r[4], options: { color: BODY, fontSize: 11, fill: bg } },
        { text: r[5], options: { color: MUTED, fontSize: 11, fill: bg } },
      ];
    }),
  ];
  s.addTable(tableRows, {
    x: M, y: 2.30, w: 7.35,
    colW: [1.05, 1.35, 1.40, 1.20, 1.25, 1.10],
    rowH: [0.34, 0.36, 0.36, 0.36, 0.36, 0.36, 0.36],
    border: { type: "solid", color: "E4EAEE", pt: 1 },
    fontFace: FB, valign: "middle",
    margin: [0.05, 0.10, 0.05, 0.10],
  });

  let y = 4.96;
  [
    ["Synthesised is as unbiased as native",
     "Median ratio 0.97 – 1.02 at every window on both planes, each against its own measured ground truth of 20.6 Mbit/s. Both sample at 1-in-256, so the theory column is shared."],
    ["And it adds no error of its own",
     "The P4 spread is at or below the sampling-theory floor at every window."],
  ].forEach(([h, b], i) => {
    listItem(s, M, y, 7.5, String(i + 1), h, b);
    y += 1.10;
  });

  marginNote(s, 8.75, 2.32, 3.73, 2.30, "One result I cannot explain yet",
    "P4 sits consistently below the theoretical floor — 54.6% against 75.5% at one second — while OVS sits on it. Below the floor is not a problem, but the mechanism is unproven. One candidate is that bmv2's per-packet random() is not independent, making the sampling closer to systematic than Bernoulli. Reported as an observation, not a claim.");

  marginNote(s, 8.75, 4.90, 3.73, 1.95, "Why the two cells are comparable",
    "Different host counts, but the same switch core — ten switches, thirty-two inter-switch links — and the same 1-in-256 rate. Sampling precision depends on the samples taken on the link, not on how many hosts hang off it. The per-hop figure therefore shows four hops on OVS and two on P4: the flow is shorter in the smaller layout, and each panel is an internal comparison.");

  s.addText("Measured at b6b75fa. P4 stock build, 20 Mbit/s, 600 s, 2,400 samples, none dropped.", {
    x: M, y: 6.96, w: CW - 0.75, h: 0.28,
    fontFace: FB, fontSize: 10, color: MUTED, margin: 0,
  });

  pageNum(s);
}

figurePage("page39_sflow-accuracy-20M.png",  1840 / 920);
figurePage("page39_sflow-accuracy-200M.png", 1840 / 920);
figurePage("page39_per-hop-consistency.png", 1840 / 800);

// ============================================================
// Page 40 — Independent cross-check
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, TAB3);
  pageTitle(s, "An independent pass over the running system",
    "Read-only checks against the live OVS stack, run from a perspective that did not know the implementation");

  const figs = [
    ["51", "read-only checks against the live stack"],
    ["12", "findings raised"],
    ["1", "real defect — fixed"],
    ["11", "documented behaviour or false positives, each adjudicated"],
  ];
  let fx = M;
  const fw = (CW - 0.6) / 4;
  figs.forEach(([big, cap], i) => {
    s.addText(big, {
      x: fx, y: 2.20, w: fw, h: 0.6,
      fontFace: FH, fontSize: 28, bold: true, color: i === 2 ? ACCENT : INK, margin: 0,
    });
    s.addText(cap, {
      x: fx, y: 2.82, w: fw, h: 0.5,
      fontFace: FB, fontSize: 11.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.14,
    });
    fx += fw + 0.2;
  });
  s.addShape("line", { x: M, y: 3.48, w: CW, h: 0.01, line: { color: RULE, width: 1 } });

  let y = 3.72;
  [
    ["Every finding was adjudicated, including the wrong ones",
     "Eleven of twelve turned out to be documented behaviour or false leads. Each was run to ground and the verdict written down, because an unadjudicated finding is indistinguishable from an ignored one."],
    ["A separate pass over unreviewed findings",
     "Forty-seven high-severity items produced twenty-one real problems. That ratio is worth stating rather than reporting only the hits."],
  ].forEach(([h, b], i) => {
    listItem(s, M, y, 7.5, String(i + 1), h, b);
    y += 1.42;
  });

  marginNote(s, 8.75, 3.74, 3.73, 2.2, "Why an outside perspective was worth arranging",
    "Everything else in this deck was verified by the person who wrote the code. That is a real limit, and the only way past it is to have something check the system without knowing what it is supposed to do.");

  pageNum(s);
}

// ============================================================
// Page 41 — Demo
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  sectionTab(s, TAB3);
  pageTitle(s, "Demo", null);

  const opts = [
    ["Link failure and reroute",
     "Break a single link, watch the twin detect it, reroute, and read the rewritten rule back over P4Runtime. Roughly 30 seconds end to end."],
    ["The P4 fabric in the Web GUI",
     "The same interface the lab already uses, driven by a data plane it was never written for — topology, flows and link usage, all through the unchanged /ndt/ API. The GUI is read-only, so anything that changes state is done from the Mininet CLI beside it."],
    ["Liveness moving through three states",
     "Kill a switch and watch Up become Unknown before it becomes Down. Unknown is held while the LLDP beacon is still fresh and only becomes Down when it expires — so one failed probe never rewrites the topology."],
  ];

  const cw8 = (CW - 0.9) / 3;
  opts.forEach((o, i) => {
    const x = M + i * (cw8 + 0.45);
    s.addText(String(i + 1), {
      x, y: 2.24, w: 0.32, h: 0.3,
      fontFace: FB, fontSize: 13, bold: true, color: ACCENT, margin: 0,
    });
    s.addText(o[0], {
      x, y: 2.60, w: cw8, h: 0.6,
      fontFace: FB, fontSize: 15, bold: true, color: INK, margin: 0, lineSpacingMultiple: 1.1,
    });
    s.addText(o[1], {
      x, y: 3.16, w: cw8, h: 1.45,
      fontFace: FB, fontSize: 12, color: BODY, margin: 0, lineSpacingMultiple: 1.22,
    });
    pending(s, x, 4.70, cw8, "screen capture");
  });

  marginNote(s, M, 5.70, CW - 0.75, 0.9, "Recorded, not performed",
    "All three are procedures already written down and already executed on the live stack, each with its own recording runbook. What is shown is a replay of a recorded run rather than a new experiment carried out in front of an audience — the failure modes here are timing-sensitive, and a live attempt would be demonstrating luck rather than the system.");

  pageNum(s);
}

// ============================================================
// Page 42 — Summary and what is not done
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  pageTitle(s, "Where it stands",
    "What shipped, what is deliberately unfinished, and what is simply unknown");

  // left: what shipped
  s.addText("Delivered", {
    x: M, y: 2.20, w: 5.6, h: 0.3,
    fontFace: FB, fontSize: 14, bold: true, color: ACCENT, margin: 0,
  });
  s.addShape("line", { x: M, y: 2.54, w: 5.6, h: 0.01, line: { color: RULE, width: 1 } });
  let y = 2.68;
  [
    ["A second data plane, with nothing above it changed",
     "P4/bmv2 fully attached — the kernel, all seven components and the Intent Translator are untouched."],
    ["The shared path made honest",
     "The silent defects in the baseline are fixed, so the reference the P4 path is verified against can be trusted."],
    ["Both data planes have a decidable health standard",
     "Five layers, differential comparison, and mutation evidence per test."],
  ].forEach(([h, b]) => {
    s.addText(h, {
      x: M, y, w: 5.6, h: 0.3,
      fontFace: FB, fontSize: 12.5, bold: true, color: INK, margin: 0,
    });
    s.addText(b, {
      x: M, y: y + 0.28, w: 5.6, h: 0.62,
      fontFace: FB, fontSize: 11.5, color: BODY, margin: 0, lineSpacingMultiple: 1.18,
    });
    y += 1.02;
  });

  // right: open items
  const RX = 7.0, RW = 5.48;
  s.addText("Open, and stated as open", {
    x: RX, y: 2.20, w: RW, h: 0.3,
    fontFace: FB, fontSize: 14, bold: true, color: ACCENT, margin: 0,
  });
  s.addShape("line", { x: RX, y: 2.54, w: RW, h: 0.01, line: { color: RULE, width: 1 } });

  const open = [
    ["Locks have no owner", "any caller can release any other caller's lock — and seven components share them", true],
    ["Queued flow endpoints", "200 queued, but nothing can ask whether the rule landed", true],
    ["Power-on can be a no-op", "within ~10 s of shutdown it returns Success and does nothing", true],
    ["Proxy restart loses rules", "every installed rule is dropped, and the twin reports full health", true],
    ["Phase 3", "proxy endpoint completion — the only phase not started"],
    ["Ryu wedge", "root cause unproven after four falsified hypotheses"],
    ["Election-id reuse", "deliberately left; changing it means re-verifying re-adoption"],
    ["popen(\"curl …\")", "22 sites across 3 files, deferred on purpose"],
    ["bmv2 stock throughput", "~40 Mbps per switch — a design trade-off, not a defect"],
  ];
  let oy = 2.66;
  open.forEach(([k, v, isNew]) => {
    s.addText(k, {
      x: RX, y: oy, w: 1.95, h: 0.38, valign: "middle",
      fontFace: FB, fontSize: 11, bold: true, color: isNew ? ACCENT : INK, margin: 0,
    });
    s.addText(v, {
      x: RX + 1.98, y: oy, w: RW - 2.28, h: 0.38, valign: "middle",
      fontFace: FB, fontSize: 10.5, color: BODY, margin: 0, lineSpacingMultiple: 1.12,
    });
    oy += 0.40;
    s.addShape("line", { x: RX, y: oy - 0.04, w: RW - 0.3, h: 0.01, line: { color: "F0F0F0", width: 1 } });
  });

  s.addText("The four marked items were found in the last two rounds of live testing and are deliberately unfixed before this report. All seventeen open issues are collected in doc/KNOWN-ISSUES.md, ordered by whether normal operation reaches them.", {
    x: RX, y: oy + 0.12, w: RW - 0.3, h: 0.7,
    fontFace: FB, fontSize: 10.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.18,
  });

  marginNote(s, M, 5.60, 5.6, 1.05, "The queued-endpoint gap is worse on OVS than on P4",
    "Same rule, same 200 queued, both data planes. P4 writes \"dispatched install failed\"; OVS writes nothing at all — 16,324 log lines, zero errors, and the rule never installed. On OVS the gap is not just unqueryable, it is untraceable after the fact.");

  s.addText("Also worth asking about: a P4Runtime specification report was prepared and then disproved by its own final check before it was sent.", {
    x: M, y: 6.86, w: 5.6, h: 0.4,
    fontFace: FB, fontSize: 10.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.18,
  });

  pageNum(s);
}

// ============================================================
// Future work
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  pageTitle(s, "Future work",
    "Three directions, at three different levels — a design problem, a structural problem, and an architectural one");

  const items = [
    ["Concurrency control has two blocked routes, and both are located",
     "The pessimistic route: release_lock only checks that a lock exists, never who holds it — a second connection with no credentials released a live lock and took it. Adding an owner is not sufficient on its own: LockManager::renew checks isLocked but not expiry, so an already-expired lease can be renewed indefinitely and TTL stops meaning anything when a holder dies.",
     "Next: an owner token plus a now < expiry guard. The optimistic route stays blocked until commit failures are detectable at all."],
    ["topology_manager.py carries three responsibilities in one class",
     "1,516 lines covering graph and routing, LLDP and liveness, and rule translation. The evidence is already in the file: two mutually independent locks, one guarding the graph and one the liveness bookkeeping, with a comment stating they are never held at once.",
     "Next: split along the line the two locks already draw. A class that needs two unrelated locks is usually two classes."],
    ["Asynchronous dispatch needs a completion handle",
     "processFlowBatch returns 200 queued and the dispatcher sends afterwards, so a switch's rejection has no route back to the application. Both applications that write flows discard the response, so returning 202 instead would change nothing.",
     "Next: a queryable job id or a synchronous path — a contract change across seven components, which is why it is future work rather than a fix."],
  ];

  let y = 2.36;
  items.forEach(([h, b, n], i) => {
    s.addText(String(i + 1), {
      x: M, y: y - 0.02, w: 0.32, h: 0.3,
      fontFace: FB, fontSize: 13, bold: true, color: ACCENT, margin: 0,
    });
    s.addText(h, {
      x: M + 0.36, y: y - 0.03, w: 10.6, h: 0.32,
      fontFace: FB, fontSize: 15, bold: true, color: INK, margin: 0,
    });
    s.addText(b, {
      x: M + 0.36, y: y + 0.32, w: 6.85, h: 1.05,
      fontFace: FB, fontSize: 11.5, color: BODY, margin: 0, lineSpacingMultiple: 1.2,
    });
    s.addShape("rect", { x: 8.42, y: y + 0.30, w: 0.03, h: 0.95,
      fill: { color: ACCENT }, line: { type: "none" } });
    s.addText(n, {
      x: 8.66, y: y + 0.26, w: 3.82, h: 1.05,
      fontFace: FB, fontSize: 11, color: MUTED, margin: 0, lineSpacingMultiple: 1.2,
    });
    y += 1.52;
  });

  s.addText("Four smaller ones are written down but not on this slide: per-flow 5-tuple rules end to end, LLDP timer tuning judged on false-positive rate rather than detection time, telemetry accuracy with several flows and the applications running, and P4 measured beyond a single fault.", {
    x: M, y: 6.86, w: CW - 0.75, h: 0.4,
    fontFace: FB, fontSize: 10.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.16,
  });

  pageNum(s);
}

// ============================================================
// Planned for the next report
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  pageTitle(s, "Planned for the next report",
    "Three measurements already scoped — each one has a number it has to beat, and a way of being wrong");

  const cols = [
    ["1", "Find where the OVS 128-host recovery time goes",
     "OVS takes 51.75 s to recover on 128 hosts against P4's 16.59 s, with no overlap between the two ranges. The mechanism is not established, so the job is to attribute the time rather than explain it.",
     "Path computation is already excluded: the same fabric converges all 16,256 paths in about 13 s of real work on the Ryu side and 11 s on the P4 side.",
     "Done when detection, recomputation and rule installation add up to the 51.75 s that was measured."],
    ["2", "Make failure detection faster without making it wrong",
     "Detection is set by constants rather than by the network: the beacon interval is 5 s, and both the link timeout and the watchdog interval are derived from it. Three missed beacons before a link is called down.",
     "The experiment is a sweep of the beacon interval at 5, 3, 2 and 1 s, measuring detection time and false positives at each.",
     "Judged on the false-positive rate, not the detection time. Detection time is certain to fall; a flapping link costs a global path recomputation."],
    ["3", "Promote the fast bmv2 build to the default",
     "Same fabric, same script: the stock build carries ~40 Mbps at 3.6k pps, the -O3 build with logging macros disabled carries 460–530 Mbps at 50.8k pps. The seam that switches between them already exists; the default is still stock.",
     "It unlocks two things that are currently unmeasurable: TE's 70% congestion threshold, which is physically unreachable on stock, and telemetry accuracy with several concurrent flows.",
     "Done when the whole L0–L4 suite passes on the fast build — changing the switch binary changes the timing every layer depends on."],
  ];

  const cw = (CW - 0.9) / 3;
  cols.forEach(([n, head, body, mid, gate], i) => {
    const x = M + i * (cw + 0.45);
    s.addText(n, {
      x, y: 2.26, w: 0.32, h: 0.3,
      fontFace: FB, fontSize: 13, bold: true, color: ACCENT, margin: 0,
    });
    s.addText(head, {
      x, y: 2.62, w: cw, h: 0.62,
      fontFace: FB, fontSize: 15, bold: true, color: INK, margin: 0, lineSpacingMultiple: 1.1,
    });
    s.addText(body, {
      x, y: 3.32, w: cw, h: 1.35,
      fontFace: FB, fontSize: 11.5, color: BODY, margin: 0, lineSpacingMultiple: 1.22,
    });
    s.addText(mid, {
      x, y: 4.72, w: cw, h: 1.05,
      fontFace: FB, fontSize: 11, color: MUTED, margin: 0, lineSpacingMultiple: 1.2,
    });
    s.addShape("rect", { x, y: 5.86, w: 0.03, h: 0.86, fill: { color: ACCENT }, line: { type: "none" } });
    s.addText(gate, {
      x: x + 0.24, y: 5.82, w: cw - 0.24, h: 0.94,
      fontFace: FB, fontSize: 11, color: BODY, margin: 0, lineSpacingMultiple: 1.2,
    });
  });

  s.addText("One thing to settle before tuning anything: the code comment says detection takes 15–20 s and the last live round measured 10.7–14 s. Tuning a timer we cannot yet predict would leave us unable to say what moved.", {
    x: M, y: 6.90, w: CW - 0.75, h: 0.4,
    fontFace: FB, fontSize: 10.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.16,
  });

  pageNum(s);
}

// ============================================================
// References
// ============================================================
{
  const s = newSlide();
  s.background = { color: "FFFFFF" };
  pageTitle(s, "References", null);

  const refs = [
    ["1", "Phaal, P. & Panchen, S. ", "Packet Sampling Basics", ". sFlow.org.",
     "The ±196√(1/c) floor used on the two accuracy slides"],
    ["1a", "Jedwab, J., Phaal, P. & Pinna, B. ", "Traffic estimation for the largest sources on a network, using packet sampling with limited storage",
     ". HP Labs HPL-92-35, 1992.", "The binomial argument [1] rests on"],
    ["2", "Chen, Hu & Jin. ", "Performance Evaluation of P4 Programmable Switches in Emulation",
     ". ACM SIGSIM-PADS '23. doi:10.1145/3573900.3591120", "The published bmv2 throughput figure"],
    ["3", "p4lang/behavioral-model, ", "docs/performance.md",
     " — ~1047 Mbps / 80k pps for one simple_switch.", "The upstream baseline for the A/B"],
    ["4", "Zhou, Yang, Duan et al. ", "Network Digital Twin: Concepts and Reference Architecture",
     ". IRTF NMRG, draft-irtf-nmrg-network-digital-twin-arch-07, 2024.", "The definition of the term, and the scalability caveat"],
    ["5", "faucetsdn/ryu, ", "README",
     " — \u201cThe Ryu project needs new maintainers\u201d, pointing to OpenStack os-ken.", "Southbound dependency risk"],
  ];

  let y = 1.78;
  refs.forEach(([n, pre, em, post, supports]) => {
    s.addText("[" + n + "]", {
      x: M, y, w: 0.55, h: 0.3,
      fontFace: FB, fontSize: 12, bold: true, color: ACCENT, margin: 0,
    });
    s.addText([
      { text: pre, options: { color: BODY } },
      { text: em, options: { color: INK, italic: true } },
      { text: post, options: { color: BODY } },
    ], {
      x: M + 0.58, y: y - 0.02, w: 6.9, h: 0.62,
      fontFace: FB, fontSize: 12, margin: 0, lineSpacingMultiple: 1.16,
    });
    s.addText(supports, {
      x: 8.62, y: y - 0.02, w: 3.86, h: 0.62,
      fontFace: FB, fontSize: 10.5, color: MUTED, margin: 0, lineSpacingMultiple: 1.14,
    });
    y += 0.82;
    s.addShape("line", { x: M, y: y - 0.16, w: CW, h: 0.01, line: { color: "EFEFEF", width: 1 } });
  });

  marginNote(s, M, 6.42, CW - 0.75, 0.9, "Where the 196 actually comes from",
    "It is not a result from a paper. [1] is a technical page with no publication date that gives no citation for the expression itself; the mathematics underneath is the normal approximation to a binomial, and 196 = 1.96 × 100, the 95% z value. Phaal is an author of both [1] and [1a].");

  pageNum(s);
}

pres.writeFile({ fileName: "/sessions/hopeful-sharp-hopper/mnt/outputs/NDTwin_deck.pptx" })
  .then(() => console.log("done"))
  .catch(e => { console.error(e); process.exit(1); });