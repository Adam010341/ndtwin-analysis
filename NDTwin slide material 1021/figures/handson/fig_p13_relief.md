# `fig_p13_relief` -- Time to relief after the trigger (page P13)

[Co-developed with claude code -- Adam]

Evidence class: **RAN** (both panels). Every mark is one archived trial; nothing is modelled.

## Data source

- Left panel: `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-10-08_why-ndtwin-handson/controls.tsv` sha256 `c5e89713f73f1529...` (git commit dcff37b6 in the kernel repo, local only).
  Planned counts read from `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-10-08_why-ndtwin-handson/run_controls.sh` sha256 `cb92dec905a88594...`: NDTwin 5 per plane, DIY 3 per
  baseline. 5 rows are designed RED controls and are not drawn: the NDTwin `red-bothpaths` rows (both
  uplinks of s1 cut, no path exists) and the `diy-static` rows (DIY static routes: 3/3 not recovered, by design --
  static routes never recompute). Each is NOT_RECOVERED; the generator stops otherwise.
- Right panel: `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-10-08_why-ndtwin-handson/congestion/results.tsv` sha256 `55b265758fb0f52f...` (kernel commits 80a4e29f and 9335b189, local only), rows
  `ndtwin-app` and `diy-app`; planned 5 per arm x plane (`/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-10-08_why-ndtwin-handson/congestion/PREREG.txt` section 7). The 27 `*-ctl` rows
  (scripted reference movers) are checked against the pre-registered verdicts and NOT drawn: their ~22 s time to
  relief is the harness's own schedule (act at t0+20 s plus a 2 s look), not a property of any controller.
- Binary identity, hashed BEFORE the trials (identity files written 02:47Z for the reroute controls,
  ../raw/identity.20261008T104711.txt, and 03:43Z for the congestion runs, raw/identity.20261008T114343.txt; raw
  trees archived in the kernel repo's audit-raw branch, commit ed24e5e5); per-trial tree state in
  raw/ndt_status_up_*.txt lines 9-12 (HEAD + uncommitted set): kernel build/bin/ndtwin_kernel sha256
  6fc7e4187df49ee9 (built 2026-10-03, no commit stamp; the P4 proxy and NDTwin's Ryu app are Python run from the
  shared tree), bmv2-fast simple_switch_grpc sha256 3ff54b5c1901c9d3, P4 pipeline json sha256
  0b19d789d74fc996, stock Ryu 4.34, Mininet 2.3.0, OVS 3.3.9, iperf3 3.16. App dirs: ndtwin_app controller.py
  sha256 8f861d3c, run.sh 4672a502 (same bytes on both planes); diy_app app.py sha256 3a4f76c6.

## Encoding

- x: seconds after the trigger. Left: after the link cut (gap_ms / 1000: first ping reply sent after the cut).
  Right: after congestion start (time_to_relief_s: first held GOOD bin, checker definition PREREG section 6).
  The two panels have their own x scales (left 0..80 s, right 0..15 s).
- Dot = trial; dots closer than 0.13 in are stacked vertically (several trials share one value).
- Red cross in the grey "failed" zone: a relief that did not hold (right, RED_FLAPPED); a cross has no x value.
  A panel without a failed trial has no "failed" zone (the left panel, now that the designed red controls are
  not drawn).
- Median bar + label: over the recovered / held-relief trials of the strip.

## Values

- NDTwin, OVS: 5 trials, 5 drawn as dots, 0 as crosses; median 20.3 s
- NDTwin, bmv2: 5 trials, 5 drawn as dots, 0 as crosses; median 15.2 s
- DIY, Ryu STP sample: 3 trials, 3 drawn as dots, 0 as crosses; median 67.7 s
- NDTwin app, OVS: 5 trials, 5 drawn as dots, 0 as crosses; median 10 s
- NDTwin app, bmv2: 5 trials, 4 drawn as dots, 1 as crosses; median 10 s
- DIY app, OVS: 5 trials, 5 drawn as dots, 0 as crosses; median 6 s

| panel | strip | trial | verdict | seconds |
|---|---|---|---|---|
| left | NDTwin, OVS | 1 | RECOVERED | 18.5 |
| left | NDTwin, OVS | 2 | RECOVERED | 20.6 |
| left | NDTwin, OVS | 3 | RECOVERED | 20.8 |
| left | NDTwin, OVS | 4 | RECOVERED | 15.9 |
| left | NDTwin, OVS | 5 | RECOVERED | 20.3 |
| left | NDTwin, bmv2 | 1 | RECOVERED | 19.2 |
| left | NDTwin, bmv2 | 2 | RECOVERED | 15.2 |
| left | NDTwin, bmv2 | 3 | RECOVERED | 14.4 |
| left | NDTwin, bmv2 | 4 | RECOVERED | 14.9 |
| left | NDTwin, bmv2 | 5 | RECOVERED | 15.3 |
| left | DIY, Ryu STP sample | 1 | RECOVERED | 67.3 |
| left | DIY, Ryu STP sample | 2 | RECOVERED | 67.7 |
| left | DIY, Ryu STP sample | 3 | RECOVERED | 67.7 |
| right | NDTwin app, OVS | app-1 | PASS | 10.0 |
| right | NDTwin app, OVS | app-2 | PASS | 10.0 |
| right | NDTwin app, OVS | app-3 | PASS | 10.0 |
| right | NDTwin app, OVS | app-4 | PASS | 10.0 |
| right | NDTwin app, OVS | app-5 | PASS | 10.0 |
| right | NDTwin app, bmv2 | app-1 | PASS | 10.0 |
| right | NDTwin app, bmv2 | app-2 | PASS | 10.0 |
| right | NDTwin app, bmv2 | app-3 | RED_FLAPPED |  |
| right | NDTwin app, bmv2 | app-4 | PASS | 10.0 |
| right | NDTwin app, bmv2 | app-5 | PASS | 10.0 |
| right | DIY app, OVS | app-1 | PASS | 6.0 |
| right | DIY app, OVS | app-2 | PASS | 6.0 |
| right | DIY app, OVS | app-3 | PASS | 6.0 |
| right | DIY app, OVS | app-4 | PASS | 6.0 |
| right | DIY app, OVS | app-5 | PASS | 6.0 |

## Reconciliation

- Left, NDTwin: comparable with doc/audit/2026-08-17_p4-vs-ovs-matched-topology/REPORT.md (same cell, n=10 per
  plane, all recovered). Mean to mean: OVS 19.2 s now
  vs 15.7 s then; bmv2 15.8 s now vs 13.7 s then.
  This run cut both directions of the on-path s1 uplink for h1->h3 at 100 pings/s; that one cut one direction for
  h1->h2 at 5 pings/s. Same order of magnitude, all recovered again: an update, not a reversal; the ~2-3 s
  higher means are not explained (not investigated).
- Right: no earlier app-level congestion result exists; the scripted `good` controls (22 s on every plane) bound
  the harness side only.

## Regenerate

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 1021/generator"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_p13_relief.py
```

Last produced: 2026-10-08T10:06:29Z (UTC); matplotlib 3.11.1; generator `make_p13_relief.py` sha256 `e3a56bb6bbec4aaa...`, shared style `figstyle_1021.py` sha256 `59bd0d3643375882...`.

[Co-developed with claude code -- Adam]
