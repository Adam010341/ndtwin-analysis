# `fig_p10_setup` -- Hands-on: one task, two setups (page P10)

[Co-developed with claude code -- Adam]

Evidence class: **READ** (topology read from files; the highlighted before/after paths read from a development
log of the NDTwin agent, not re-run here). Nothing on this figure is a trial result.

## Data source

- Fabric: `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-10-08_why-ndtwin-handson/topology.tsv` sha256 `2e5b66442868e743...` (10 switches, 16 switch-switch links, 4 hosts on port 3; the same
  wiring as setting/StaticNetworkTopology{P4,OVS}_10Switches_4Hosts.json and tools/test_workflow/ovs_4host_topo.py,
  checked offline in H/raw/helper_topo_vs_tsv.txt).
- Pair: `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-10-08_why-ndtwin-handson/congestion/variants_dev.tsv` sha256 `b9ff26bb2a007d9a...`, dev role A = h1 -> h3 (the development
  workload handed to both agents).
- Paths: `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-10-08_why-ndtwin-handson/congestion/raw/agent_ndtwin_dev/evidence/ctl7.log` sha256 `afe9cbcc033c9d36...` (the NDTwin agent's dev run on OVS that its NOTES.txt cites),
  first move line of that pair: `s1:1>s5:3>s9:4>s8:1>s3:3  ->  s1:2>s6:3>s9:3>s7:1>s3:3` (switch:egress-port hops). Before =
  s1-s5-s9-s8-s3; after = s1-s6-s9-s7-s3. Every hop is checked against topology.tsv. The DIY app's base
  routing chose s1-s6-s10-s7-s3 for this pair (read at run time from `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-10-08_why-ndtwin-handson/congestion/raw/agent_diy_dev/ryu.log` sha256 `f7f0a392041b77cd...`,
  its startup "base paths" line); the figure shows one real example, the NDTwin arm's, not every arm's path.

## Encoding

- Grey lines: every link of topology.tsv. Solid accent: the largest flow before the move; dashed accent: after.
- Red bars: a load glyph on the first switch-to-switch link of the before path (all links of that path carried
  the three flows; the task threshold is 40 Mbit/s per direction, TASK.txt).
- The kernel box says "base forwarding": on OVS it is NDTwin's own Ryu app (intelligent_router.py) that installs
  it, on bmv2 the P4 proxy; the developer of the NDTwin arm writes none of it.
- Side panels: NDTwin arm = app -> REST :8000 -> NDTwin kernel -> Ryu (OVS) or P4 proxy (bmv2); DIY arm = the app is
  a Ryu application inside stock Ryu 4.34, speaking OpenFlow 1.3 to OVS. Both arms run the same fabric file
  (ovs_4host_topo.py through the lab helper); the NDTwin arm also runs the same wiring on bmv2.

## Regenerate

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 1021/generator"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_p10_setup.py
```

Last produced: 2026-10-08T10:06:53Z (UTC); matplotlib 3.11.1; generator `make_p10_setup.py` sha256 `2d5c5c5a60de34ac...`, shared style `figstyle_1021.py` sha256 `59bd0d3643375882...`.

[Co-developed with claude code -- Adam]
