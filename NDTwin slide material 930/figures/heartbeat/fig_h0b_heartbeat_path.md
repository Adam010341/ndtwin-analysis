# `fig_h0b_heartbeat_path` —— veth 心跳：從線上到 kernel 圖

[Co-developed with claude code -- Adam]

（本檔所有時間為 UTC；run 目錄名的 `…Z` 就是 UTC。）

## 一句話

root helper 在每條交換機間 veth 上每 5 s 送一個 0x88B5 幀、在對端 veth 上聽；只把「每個方向最後聽到的時刻」寫進報告檔，
**不做任何判斷**。proxy 的 watchdog 每 5 s 讀報告，用跟自家 LLDP 同一條規則（沉默 > 15 s ⇒ 不通）判，
通知 kernel 圖；只有 NDTwin 擁有路由表的 package（roles owner ndtwin）才會改路。

## 資料來源（方塊上的名字與數字都由腳本從碼讀出並斷言）

K＝`/home/adam/Desktop/NDTwin-Kernel`，trunk `3d740be0`。

| 方塊 | 檔:行 |
|---|---|
| root helper、0x88B5、每 5 s | `K/tools/test_workflow/ndtwin-lab:715`（`ETHERTYPE = 0x88B5`）、`:734`（`PERIOD_S = 5`）；送出 `:1327` |
| 報告：每個方向最後聽到的時刻 | `K/p4_proxy/proxy_agent/link_heartbeat.py:54`（`REPORT_PATH = "/run/ndtwin-lab/heartbeat.json"`）；報告在聽到後 ≥ 0.5 s 才重寫：`ndtwin-lab:765`（`REPORT_MIN_INTERVAL_S = 0.5`） |
| helper 不做判斷，proxy 判 | `link_heartbeat.py:6-18`（說明） |
| proxy watchdog：每 5 s、沉默 > 15 s ⇒ down | `K/p4_proxy/proxy_agent/topology_manager.py:373`（`LLDP_BEACON_INTERVAL_S = 5`）、`:419`（`LINK_BEACON_TIMEOUT_S = 3 * LLDP_BEACON_INTERVAL_S`）、`:422`（watchdog 間隔）、`:1991` `check_link_beacons`、`:2086` watchdog 迴圈 |
| kernel 圖 `is_up` | `topology_manager.py:2049` `_notify_link` |
| 改路只在 owned 表 | `topology_manager.py:2154`（「link transition reported to the kernel and NOT rerouted」分支）；live：H1 roles package 改路（run log `…/intake-0926/hbw-live/h14-20260926T152605Z.log:72`）、H3 沒綁定只偵測（同 log `:149-158`） |

## 可信度

**READ**：整張圖是架構圖，每個方塊都是讀碼；腳本斷言上述常數與函式名仍在碼裡。

**OBSERVED（佐證，不在圖上）**：心跳的語意在真 veth、真 netem 上對（P4-HB-SPIKE.md §5.1，`:562-567`）；
心跳幀從沒到過主機：spike 普查 20 臂 0 幀（`doc/audit/2026-09-25_p4-heartbeat/spike/runs/2026-09-26T052148Z_S_heartbeat/40_census.tsv`，P4-HB-SPIKE.md §3.2 `:404-406`）、
H5 的 sampler 1645 筆 `forwarded_to_hosts` 全 0（`…/live-p1/runs/2026-09-26T172912Z_08_heartbeat/50_samples.tsv`；1645 是 1 Hz 輪詢筆數，單位是 17 個心跳 session、0 幀，見 `fig_h4_forwarding_unchanged.md`）。
兩份 raw 都在 audit-raw `797c34ab`（逐檔 blob 與工作樹相同，2026-09-27 17:2xZ 本機比對；依 coordinator 已公開在兩個 P4 repo）。
**髒 checkout**：spike 普查 run `code 580767a8 +79`；H5 run `3f8c2abf +89`（`00_status_before.txt:7`）；兩者都含 2 個會改變行為的檔：`p4_proxy/mininet/host_count_override`、`tools/remote-lab/dorm_lab/`。

**INFERRED**：無。

## 已知但書

- 心跳證明的是**那條 veth**，不是交換機：daemon 在對端 veth 上、在交換機之前就讀到幀（P4-HB-SPIKE.md §2.5 `:333`）。
- 報告不新鮮（daemon 死了）時 watchdog **凍結、不判**，並揭露（`link_heartbeat.py:23-27`）——daemon 的死不是網路的死；Adam 09-27 裁決 D「接受並揭露」（orchestrator 記憶，非 repo 檔）。
- external 控制面的 package 目前**不起心跳**（H4，run log `:168-173`）；Adam 09-27 裁決 B 要做 detect-only，分支 `feat/external-detect-only-0927` 未併入。

## 重生指令

見 `fig_h0_why_not_lldp.md`（同一支 `make_heartbeat_extra_figs.py`）。最後產出：2026-09-27T19:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_heartbeat_extra_figs.py` sha256 `9f5bcc908075125b…`（產圖之後腳本沒再改過）。
