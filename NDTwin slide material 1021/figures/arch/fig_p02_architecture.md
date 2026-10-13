# `fig_p02_architecture` -- What NDTwin is, as built today (page P02)

[Co-developed with claude code -- Adam]

Evidence class: **READ**: code and documents at trunk 2ece656c (full 2ece656c4a280477209a09b6fb7a51304d38b8ff),
read with `git show 2ece656c:<path>`; sibling repos at their HEAD commits (Energy-Saving-App 9facb78,
Simulation-Platform-Manager b7efd93, Web-GUI f63a55c, Network-State-Recorder 850f61d,
Network-Traffic-Visualizer 9b56b30, Network-Traffic-Generator 6e3f388). Nothing in the drawing was run; the
physical network is drawn dashed and tagged "no run on record": there is no hardware run log in the kernel
tree, and the repo's own API document says only the physical power-state branch "has not been exercised"
(doc/2026-01-02_ndt_api.md:1598-1599).

## Data source

`figures_spec/architecture.txt` sha256 `d40e40746c15a656...`. The boxes are drawn in the generator; the spec is
read to check that every drawn element has an evidence entry, that its canvas title is the title drawn, that
the removed names do not return and that no repository tint or legend is asked for.

## What changed against the 827 figure (spec section 0)

1. "Local LLM (fine-tuning)" removed (no local-model code; the only LLM call is LLMAgent.cpp:138, OpenAI).
2. "Apps (using AI/ML model inference ...)" removed; the "simulation" apps box is the Energy-saving simulator.
3. Physical network kept, dashed, "no run on record".
4. New small box "ndt / ndtwin-lab" (lab lifecycle tool and root helper).
Also: "Data cache manager" is the module's real name, Historical data manager. Colours: kernel blue, everything
outside the kernel grey. There is no tint and no legend by which repository holds a box (template rule 7).

## REST, and its two exceptions

Apps and tools talk to the kernel over REST (:8000); the kernel talks REST to Ryu (:8080) and to the P4 proxy
(:8081). Two exceptions are written inside their boxes: simulation cases reach the Simulation platform manager
over NFS ("cases via NFS", Simulation-Platform-Manager@b7efd93 app.cpp:286), and the Network traffic generator
builds the OVS fabric itself ("builds the OVS fabric", Network-Traffic-Generator@6e3f388 testbed_topo.py:39-48),
which is why it has its own arrow to the data planes.

## Layout notes

- The data planes are mirrored against the 827 figure (bmv2 on the left, OVS on the right, with the P4 proxy
  and Ryu swapped to match) so that the Network traffic generator's double-headed arrow reaches Mininet + OVS
  only. The "sFlow, synthesised by the proxy" arrow starts at the P4 proxy box (C2), as the spec says. "one data
  plane per run" is a note under a bracket that spans all three planes; the "no run on record" tag sits beside
  the physical plane's name.

## Differences from the spec text

- Kernel modules are drawn as nine boxes (B0-B8); the spec allows dropping the inner detail if crowded, it
  was not needed. The "sFlow 1/256" label on the OVS plane is switch sampling; on the bmv2 plane the sFlow is
  synthesised by the proxy; the physical plane's sFlow is dashed (no run on record).
- OpenAI (E6) is drawn as a dashed outline in the tools column (external service, off by default); the spec
  lists keeping it as an open point for the orchestrator.

## Boxes and evidence

| id | label on the canvas | fill | evidence from architecture.txt |
|---|---|---|---|
| A1 | Traffic-engineering App | outside the kernel (grey) | Traffic-engineering App   Traffic-Engineering-App@f108c7c:Traffic-engineering-App.py:32 ; (ndt_url = http://localhost:8000/ndt/) |
| A2 | Energy-saving App | outside the kernel (grey) | Energy-saving App         Energy-Saving-App@9facb78:src/app/http.cpp:127,158 ; (set_switches_power_state, install_flow_entry) |
| A3 | ... your app | dashed white | "..."  your app           any HTTP client; doc/2026-01-02_ndt_api.md (REST reference) |
| A4 | Energy-saving simulator | outside the kernel (grey) | Energy-saving simulator   Energy-Saving-App@9facb78:src/sim/energy_saving_simulator.cpp:467,621 ; (the only shipped simulator; flow-level, max-min: ; src/sim/max_min_fairness.cpp:12) |
| B0 | REST server :8000 | kernel (blue) | REST server :8000         src/ndt_core/event_handling/ControllerAndOtherEventHandler.cpp:100 ; (tcp::v4(), port); routes src/ndt_core/http/HttpSession.cpp:326-345 ; (about 45 routes, no auth, no push) |
| B1 | Topology and flow monitor | kernel (blue) | Topology and flow monitor src/ndt_core/collection/TopologyAndFlowMonitor.cpp:2373 ; (polls the controller's topology; undeclared switches ignored) |
| B2 | Flow and link usage collector (sFlow) | kernel (blue) | Flow info and link usage  src/ndt_core/collection/FlowLinkUsageCollector.cpp; ; collector (sFlow)         include/ndt_core/collection/FlowLinkUsageCollector.hpp:33 (UDP 6343) |
| B3 | Flow routing manager | kernel (blue) | Flow routing manager      src/ndt_core/routing_management/FlowRoutingManager.cpp:82-86 ; (per-dpid strategy: P4 vs OVS/hardware); FlowDispatcher.cpp ; (queued writes); P4RoutingStrategy.cpp:27-33 (group/meter refused) |
| B4 | Device config and power manager | kernel (blue) | Device config and power   src/ndt_core/power_management/DeviceConfigurationAndPowerManager.cpp, ; manager                   OVSPowerStrategy.cpp, P4PowerStrategy.cpp |
| B5 | App registration and simulation requests | kernel (blue) | App registration and      src/ndt_core/application_management/ApplicationManager.cpp; ; simulation requests       SimulationRequestManager.cpp:17 (SIM_SERVER_URL); ; HttpSession.cpp:450,467 (received_a_simulation_case, app_register) |
| B6 | Intent translator | kernel (blue) | Intent translator         src/ndt_core/intent_translator/IntentTranslator.cpp, LLMAgent.cpp:138 ; (off by default: src/main.cpp --no-ai) |
| B7 | Historical data manager | kernel (blue) | Historical data manager   src/ndt_core/data_management/HistoricalDataManager.cpp |
| B8 | Fault injection (netem) | kernel (blue) | Fault injection (netem)   HttpSession.cpp:20,282 (inject_link_failure: tc netem on Mininet) |
| C1 | Ryu + NDTwin Ryu app | outside the kernel (grey) | Ryu + NDTwin Ryu app      intelligent_router.py:617-618@2ece656c (IntelligentRyu, OpenFlow 1.3); ; REST :8080 setting/AppConfig.hpp.example:8 ; Arrows: Kernel <-> C1 "REST :8080"; C1 -> OVS and -> hardware "OpenFlow 1.3" |
| C2 | P4 proxy agent | outside the kernel (grey) | P4 proxy agent            p4_proxy/proxy_agent/main.py:2466 (PORT = 8081); ; setting/AppConfig.hpp.example:10; p4_client.py:5,8 (grpc, P4Runtime) ; Arrows: Kernel <-> C2 "REST :8081 (Ryu-shaped)"; C2 -> bmv2 "P4Runtime" |
| C3 | Link heartbeat helper | outside the kernel (grey) | Link heartbeat helper     p4_proxy/proxy_agent/link_heartbeat.py:52-54; ; (runs as root)            tools/test_workflow/ndtwin-lab:588 ('heartbeat start') ; Only for a P4 program other than ndtwin_switch.p4. Small box beside C2; optional. |
| D1 | Mininet + OVS | data plane (white) | Emulated: Mininet + OVS   testbed_topo.py@2ece656c (root) / Network-Traffic-Generator@6e3f388 ; testbed_topo.py:39-48 (fixed 10-switch fabric); ; tools/test_workflow/ovs_4host_topo.py (4-host cell) ; Telemetry arrow up to B2: "sFlow 1/256" (switch sFlow; README.md:31-34) |
| D2 | Physical switches | data plane (white), dashed | Physical switches         include/common_types/GraphTypes.hpp:140-144 (HPE5520, ; DASHED, "no run on record"       BrocadeICX6610, BrocadeICX7250); src/main.cpp:59,72 (--mode testbed); ; no hardware run log in the kernel tree (api.md:1598 covers only ; the power-state branch) ; Telemetry arrow: "sFlow" (dashed) |
| D3 | Mininet + bmv2 | data plane (white) | Emulated: Mininet + bmv2  p4_proxy/mininet/p4_testbed_topo.py:1 (builder reads the topology ; model); p4_proxy/p4_src/ndtwin_switch.p4 (default program) or your ; own program via tools/p4_exercise/convert.py:1 + ndt up p4 --app ; Telemetry arrow: "sFlow, synthesised by the proxy", drawn FROM the P4 proxy box (C2) to B2, not ; from the bmv2 plane (p4_proxy/proxy_agent/sflow_emitter.py:1; ; own programs: p4_proxy/mininet/psample_sflow_emitter.py:6, tc sampling) |
| E1 | Simulation platform manager | outside the kernel (grey) | Simulation platform mgr   Simulation-Platform-Manager@b7efd93:app.cpp:286 (NFS mount per case); ; kernel side SIM_SERVER_URL localhost:9000 (AppConfig.hpp.example:6) |
| E2 | Web GUI | outside the kernel (grey) | Web GUI                   Web-GUI@f63a55c:src/api/index.ts:36 (get_graph_data) |
| E3 | Network state recorder | outside the kernel (grey) | Network state recorder    Network-State-Recorder@850f61d:network_state_recorder.py:21,23 |
| E4 | Network traffic visualizer | outside the kernel (grey) | Network traffic visualizer Network-Traffic-Visualizer@9b56b30:Network_Traffic_Visualizer.sh:4 ; (NDT_API_URL localhost:8000) |
| E5 | Network traffic generator | outside the kernel (grey) | Network traffic generator Network-Traffic-Generator@6e3f388:README.md:101 (ndtwin_kernel URL); ; double-headed arrow to D1 Mininet + OVS only (its testbed_topo.py ; builds the OVS fabric; it does not build the bmv2 plane) |
| E6 | On-line LLM (OpenAI) | dashed white | On-line LLM (OpenAI)      LLMAgent.cpp:138 -- external service, outline only |
| E7 | ndt / ndtwin-lab | outside the kernel (grey) | ndt / ndtwin-lab          tools/test_workflow/ndt, tools/test_workflow/ndtwin-lab ; (lab lifecycle and root helper) -- NEW, small |

## Caveats (also in the speaker notes)

- Do not say NDTwin stays in sync with your production network: it mirrors a Mininet fabric it controls
  through its own Ryu app or P4 proxy.
- Exactly one data plane per run; mixing is refused (TopologyAndFlowMonitor.cpp:3425-3427).

## Regenerate

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 1021/generator"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_p02_architecture.py
```

Last produced: 2026-10-08T10:57:32Z (UTC); matplotlib 3.11.1; generator `make_p02_architecture.py` sha256 `76a3d61b1a11e800...`, shared style `figstyle_1021.py` sha256 `59bd0d3643375882...`.

[Co-developed with claude code -- Adam]
