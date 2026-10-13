# `fig_p04_map` -- Where 16 tools sit: fidelity vs live link (page P04)

[Co-developed with claude code -- Adam]

Evidence class: **READ** (competitor positions from public material read 2026-10-08, commercial = vendor
material, academic = paper or draft; NDTwin from code and docs at trunk 3a47bdb7, full
3a47bdb7612d2608a7feb17614c8d686032ef38f). Nothing on this figure was run.

## Data source

- Positions: `figures_spec/landscape.tsv` sha256 `1ddfbd490685316d...` (16 rows, read as-is; its `#` header is the
  placement rule below).
- Marker colour (persona of the tool's matrix group): `research/matrix_final.json` sha256
  `6fb9ea515383bc8a...`, `personas.*.columns`; NDTwin in the accent colour.
- Axes: x = config model, ML model, flow-level model, packet-level emulation, real devices (equal
  spacing); y = none, imports snapshots, stays synced live; y axis title "link to a network the tool does not build or control".

## Placement rule (verbatim from the tsv header)

> P04 placement rule (one rule for all 16 rows; applied over research/matrix_final.json).
> x = the fidelity class named in the tool's maturity.M6 note: config/state model -> config model;
> ML model -> ML model; flow-level -> flow-level model; packet-level emulation or simulation ->
> packet-level emulation (simulation gets an open marker); no model, reads devices -> real devices;
> a controller with no fidelity of its own -> the data plane of the setup its matrix column names;
> a framework with no model -> 'not applicable' (drawn as a band).
> y = link to a network the tool does not build or control, read from ops.O1 note/scope where the tool
> has an O1 cell, else from maturity.M6 note plus app.A8 / p4.P8:
> stays synced live = a documented feature keeps ingesting state from such a network;
> imports snapshots = it ingests point-in-time config or state collected from such a network;
> none = it models only a network it builds, or controls as its controller
> (a topology seeded from an inventory such as NetBox counts as building).
> One point per tool, for the setup its matrix column names. Other targets a tool can reach (hardware
> paths, coded or documented) are not drawn for any tool.
> unsure = 'yes: <why>' when the M6/O1 text allows a second cell; 8 rows are unsure.

## How the markers are drawn (spec: template section 2 P04)

- Filled circle per tool; label = `short_label`; `*` = vendor material only, `†` = paper or draft only.
- Layout decision for the emulation x none cell, which holds 10 tools (the count is read from the tsv): the
  cell is one vertical list with NDTwin as its first entry, in the same band as the other 9: same x,
  same vertical range, no row of its own, so the map shows no difference in y. NDTwin is highlighted (accent colour,
  larger marker, bold label). The other entries follow in one column (control-app tools, ns-3 first with an open
  circle = packet-level SIMULATION, then P4 tools, then operator tools). All 10 labels sit at 10.5 pt or
  larger on the canvas, so neither two columns nor abbreviations were needed; the bottom row is taller instead.
  The template's 3 x 3 cluster was already not used (under 0.8 in per label at equal column spacing).
- NDTwin's whisker (dashed) runs left from its entry to the flow-level model column: the shipped what-if
  (flow-level max-min). It runs at the height of NDTwin's own entry, at the top of the cell, so it crosses no label.
- One point per tool: there is NO second marker for NDTwin's physical path (coded, no run on record), and none for
  any other tool's hardware path; P02 and P16 disclose the physical path. The generator stops if the tsv header
  stops saying "one point per tool".
- sFlow-RT: hollow diamond = monitor, not a model.
- IRTF NDT draft: dashed band across the whole top row, label at its left end, no point; legend entry "framework (draft)".
- Persona is encoded by colour only on this figure: marker shape is already used for the marker kinds.

## Unsure positions (landscape.tsv column `unsure`)

8 rows carry `unsure` = yes (ONOS+Mininet, ns-3, sFlow-RT, ONOS+Stratum, Forward*, CML*, IP Fabric*, IRTF NDT draft†); the header states the same number.
The reasons are verbatim in the table below.

## All rows

| tool | x | y | label | unsure | rationale | source |
|---|---|---|---|---|---|---|
| Mininet + Ryu (assemble it yourself) | packet-level emulation | none | Mininet+Ryu | no | Real kernel and OVS in namespaces; a lab you build; nothing imported from a running network. | matrix_final.json maturity.M6 (https://mininet.org/overview/); personas.ops none; app.A8 note |
| ONOS (+ Mininet) | packet-level emulation | none | ONOS+Mininet | yes: x depends on the data plane chosen; on real switches it would sit at real devices (y still none, as their controller); placed as the dev setup the matrix column names | Controller of the Mininet fabric it runs on; fidelity is that data plane. It models no network it does not control. | matrix_final.json maturity.M6 (onos README); app.A1, A3, A5 (live view of the fabric it controls) |
| Containerlab | packet-level emulation | none | Containerlab | no | Real NOS containers joined by veth; topology from YAML; no live import. | matrix_final.json maturity.M6 (https://containerlab.dev/manual/network/); app.A1 scope |
| ns-3 | packet-level emulation | none | ns-3 | yes: x axis has no 'packet-level simulation' column; draw it on the left edge of the emulation column with a distinct marker, or add a column | Discrete-event packet-level SIMULATION; network and traffic modelled in code, no live import. | matrix_final.json maturity.M6 (https://www.nsnam.org/about/); app.A6 note |
| sFlow-RT | real devices | stays synced live | sFlow-RT | yes: it measures, it does not model; hollow diamond meaning 'monitor, not a model' | No model at all: analytics on live sFlow from devices it does not control (real or emulated); not a twin. | matrix_final.json maturity.M6 (https://sflow-rt.com/intro.php); app.A3, A8 |
| p4lang/tutorials VM | packet-level emulation | none | P4 tutorials VM | no | Mininet with bmv2; topology.json per exercise. | matrix_final.json maturity.M6 (tutorials utils/run_exercise.py); p4.P2 |
| p4-utils (ETH Zurich nsg) | packet-level emulation | none | p4-utils | no | Mininet with bmv2 (and FRR); network defined in Python/JSON. | matrix_final.json maturity.M6 (https://nsg-ethz.github.io/p4-utils/introduction.html) |
| ONOS + Stratum | packet-level emulation | none | ONOS+Stratum | yes: x could also be real devices (Tofino/Tomahawk); one point keeps the map readable | Tutorial runs stratum_bmv2 in Mininet; Stratum also runs on Tofino/Tomahawk (hardware arrow optional). | matrix_final.json maturity.M6 (stratum README); p4.P8 |
| Batfish | config model | imports snapshots | Batfish | no | Open source. Computes control and data plane from config files exported from a network it does not control; one snapshot per analysis. | matrix_final.json maturity.M6 (https://par.nsf.gov/servlets/purl/10534020); ops.O1, O8 |
| GNS3 | packet-level emulation | none | GNS3 | no | Runs real or virtualised NOS images; lab built by hand or via REST; no live-state import. | matrix_final.json maturity.M6 (gns3-server); ops.O1 |
| Forward Networks (commercial, public docs only) | config model | imports snapshots | Forward* | yes: the rule sets no snapshot cadence, so continuous or scheduled snapshots could also read as 'keeps ingesting state' (stays synced live) | Vendor material: config and state model from SSH-collected snapshots, taken continuously (vendor claim); flow and load telemetry not stated. | matrix_final.json maturity.M6 (Forward ProductDataSheet.pdf); ops.O1, O8 |
| Cisco Modeling Labs (commercial, public docs only) | packet-level emulation | none | CML* | yes: NetBox seeding is close to 'imports snapshots', but it carries topology from an inventory, not state from the network | Vendor material: VM/container NOS images in a lab it builds; a NetBox export can seed the topology (inventory, not device state); configs are yours. | matrix_final.json maturity.M6 (developer.cisco.com/modeling-labs); ops.O1 |
| IP Fabric (commercial, public docs only) | config model | imports snapshots | IP Fabric* | yes: the rule sets no snapshot cadence, so continuous or scheduled snapshots could also read as 'keeps ingesting state' (stays synced live); IP Fabric's snapshots are scheduled | Vendor material: config and state model from scheduled discovery snapshots; path lookup on the model. | matrix_final.json maturity.M6 (docs.ipfabric.io Path_Lookup); ops.O1, O8 |
| RouteNet-Fermi (academic, paper only) | ML model | none | RouteNet-Fermi† | no | Paper: GNN predicting delay, jitter, loss; trained offline, ingests no running network. | matrix_final.json maturity.M6 (https://arxiv.org/abs/2212.12070); ops.O1 |
| IRTF NMRG network digital twin architecture draft (academic reference framework) | not applicable (spans all) | stays synced live | IRTF NDT draft† | yes: it is a framework (draft), not software; a band avoids implying a position on x | Framework (draft) requiring real-time data; model type left open; no implementation. Draw as a dashed band across the top row, not a point. | matrix_final.json maturity.M6, ops.O1 (draft-irtf-nmrg-network-digital-twin-arch-13 sec 4, 9.1) |
| NDTwin | packet-level emulation | none | NDTwin | no | Packet-level Mininet OVS/bmv2 fabric that it builds and controls through its own Ryu app or P4 proxy, mirrored live; it attaches to no network it does not control. Whisker to flow-level model = shipped what-if (max-min). The physical path (coded, no run on record) is not drawn; P02 and P16 disclose it. | matrix_final.json maturity.M6 (README.md:32; Energy-Saving-App@9facb78 src/sim/max_min_fairness.cpp:12); ops.O1 scope ('Does not attach to an existing non-Ryu controller'); app.A8 note and scope |

## Caveats

- The bottom row is named "none" (no link to a network the tool does not build or control): NDTwin and
  ONOS+Mininet both sit there although both keep a live view of the fabric they control; the axis title says
  what the rows measure.
- 'Live' for NDTwin means synced with the emulated fabric it builds and controls through its own Ryu app or P4
  proxy, not with an external production network.
- A cell is about the documented feature, not about how well it works.

## Regenerate

```bash
cd generator   # from the deck folder
"${NDTWIN_PLOTVENV:-../../NDTwin Slide material 820/.plotvenv/bin/python3}" make_p04_map.py
```

Last produced: 2026-10-12T06:20:00Z (UTC); matplotlib 3.11.1; generator `make_p04_map.py` sha256 `a9f38a44489c04b8...`, shared style `figstyle_1014.py` sha256 `be4a908ad5c4fbab...`.

[Co-developed with claude code -- Adam]
