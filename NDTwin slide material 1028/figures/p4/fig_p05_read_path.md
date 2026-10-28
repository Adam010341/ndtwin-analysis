# fig_p05_read_path -- Reading registers and direct counters

Page P05 of the 1028 deck. Evidence class: READ (code of the PR tree, read, not executed); the fact on the
P4Runtime channel ("no register reads on bmv2") was measured offline on throwaway bmv2 and is cited below.
Spec: figures_spec/read_path.txt. Generator: generator/make_p05_read_path.py with generator/figstyle_1028.py.

## Elements and evidence

| id | label | evidence |
|---|---|---|
| APP | App | The routes are HTTP GETs any client calls; no kernel route forwards them (grep of W/src and W/include for "p4/register" and "p4/direct_counter" is empty). |
| PROXY | NDTwin P4 proxy / REST :8081 | W/p4_proxy/proxy_agent/main.py:2767 (PORT = 8081). |
| R_DC | GET /p4/direct_counter/{name} / the whole table's counts | W/p4_proxy/proxy_agent/api_routes.py:1491-1500 (one wildcard P4Runtime read; every entry of the table with its counts). |
| R_REG | GET /p4/register/{name} / cells of one register array | api_routes.py:1604-1609. |
| CH_P4RT | P4Runtime / no register reads on bmv2 | api_routes.py:1610-1614 (bmv2's P4Runtime answers every RegisterEntry read UNIMPLEMENTED); R/DESIGN.md:38-44, :59 (measured on both builds). |
| CH_THRIFT | Thrift / bmv2 only | api_routes.py:1612-1616 (the switch's own Thrift service; a hardware target has none, 503 there). |
| CHK1 | 1  switch answers P4Runtime | api_routes.py:1628-1629, :1736-1742 (client.probe before every read; else 503 "switch not reachable", Thrift is not asked). |
| CHK2 | 2  same device id and port | api_routes.py:1630-1631, :1743; W/p4_proxy/proxy_agent/bm_thrift.py:285-292 (bm_mgmt_get_info on the read's own Thrift connection must answer this switch's device id and Thrift port; else 502 "thrift device mismatch", no register read). |
| REF1 | 503 / nothing read | api_routes.py:1739-1742. |
| REF2 | 502 / nothing read | api_routes.py:1630-1631 and the ThriftDeviceMismatch handler (":... nothing was read"). |
| SW | bmv2 switch | One switch per dpid; Thrift port 9090 + dpid (api_routes.py:1612-1614). |
| SW_DC | table + direct counter | api_routes.py:1494-1500. |
| SW_REG | register array | api_routes.py:1608-1609. |

## Drawing

- NDTwin's proxy and its two routes blue; the app and the switch grey; the two checks white, each with its
  refusal in red (status, nothing read). The register arrow reaches the switch only through both checks.

## Regenerate

```bash
cd generator   # from the deck folder
"${NDTWIN_PLOTVENV:-../../NDTwin Slide material 820/.plotvenv/bin/python3}" make_p05_read_path.py
```

Last produced: 2026-10-27T15:06:37Z (UTC); matplotlib 3.11.1; generator `make_p05_read_path.py` sha256 `d7974b6ec9066483...`, shared style `figstyle_1028.py` sha256 `67385b0eb73c39b9...`.

[Co-developed with claude code -- Adam]
