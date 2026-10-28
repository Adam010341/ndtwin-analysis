# fig_p04_rules_lost -- How the rule-loss notice reaches the app

Page P04 of the 1028 deck. Evidence class: READ (code and docs of the PR tree, read, not executed).
Spec: figures_spec/rules_lost_flow.txt (lanes, steps, arrows and their evidence). Generator:
generator/make_p04_rules_lost.py with the shared style generator/figstyle_1028.py.

## Steps and evidence

| # step | lane | label | evidence |
|---|---|---|---|
| 1 S1 | P4 proxy | Pipeline push / proxy restart, or re-adopt | W/doc/2026-01-02_ndt_api.md:660-662 (a proxy restart and POST /p4/readopt/{dpid} push the pipeline); W/doc/KNOWN-ISSUES.md:338 (A-4c: every push the proxy makes itself: at start, and readopt). Re-adopt follows a switch restart: W/p4_proxy/proxy_agent/api_routes.py:900. |
| 2 S2 | bmv2 switch | Every table emptied / Ryu-path rules gone | W/doc/2026-01-02_ndt_api.md:661-664 (the push empties every table; rules installed through the Ryu-compatible routes are not put back). |
| 3 S3 | P4 proxy | Lost rules recorded / per switch: ryu_rules_lost | W/p4_proxy/proxy_agent/topology_manager.py:1462 (record per dpid), :2349 (served in GET /p4/switch_state); W/doc/2026-01-02_ndt_api.md:666-667, :688-698 (key table; replayed always false). |
| 4 S4 | NDTwin kernel | Copied to its graph node / in get_graph_data | W/src/ndt_core/power_management/P4RulesLost.cpp:117 (node["ryu_rules_lost"] = the proxy's object), :99-101 (ERROR line "They were NOT replayed"); ndt_api.md:667-668 (copied verbatim, same 1 Hz request). |
| 5 S5 | App | Reads it, resends its rules / no app does this yet | W/doc/2026-01-02_ndt_api.md:666 ("so whoever installed the rules can resend them"), :690 ("Act once per id"); W/doc/KNOWN-ISSUES.md:350-352 (apps poll get_graph_data and resend their own rules). Dashed: no shipped app reads ryu_rules_lost (git grep at HEAD of the seven sibling repos is empty; template P08 row 5 sources). |
| 6 S6 | bmv2 switch | Rules back / only if the app resends | W/doc/2026-01-02_ndt_api.md:698 (replayed: always false); W/doc/KNOWN-ISSUES.md:372 (the rules stay gone after a restart; this only makes it visible). Drawn DASHED: it is not done by NDTwin. |

## Drawing

- NDTwin's own components (kernel, P4 proxy) blue; the switch and the app grey; dashed white steps:
  S5, S6 (no shipped app resends on the notice yet; replayed is always false).
- Arrows: S1->S2, S2->S3, S3->S4 (polled at 1 Hz), S4->S5, S5->S6 (resend).

## Regenerate

```bash
cd generator   # from the deck folder
"${NDTWIN_PLOTVENV:-../../NDTwin Slide material 820/.plotvenv/bin/python3}" make_p04_rules_lost.py
```

Last produced: 2026-10-27T15:06:35Z (UTC); matplotlib 3.11.1; generator `make_p04_rules_lost.py` sha256 `4002fc7dd7ff5844...`, shared style `figstyle_1028.py` sha256 `67385b0eb73c39b9...`.

[Co-developed with claude code -- Adam]
