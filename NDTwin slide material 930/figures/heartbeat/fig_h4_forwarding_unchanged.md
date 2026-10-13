# `fig_h4_forwarding_unchanged` —— 心跳開著，轉送結果不變

[Co-developed with claude code -- Adam]

（本檔所有時間為 UTC；run 目錄名的 `…Z` 就是 UTC。）

## 一句話

心跳加入之前的最後一次完整 06（09-24 18:55Z）當參照；之後三次完整 06 都有心跳跑在 17 臂下面，
**26 臂的 rc 與判定逐臂和參照相同**。心跳幀離開 host 埠的次數：09-26 17:29 那一輪的 1645 筆取樣全是 0。

## 判官修正（2026-09-27 UTC；F-10）

- 單位改成 **17 個心跳 session、0 幀**：1645 筆是 sampler 每秒一次的讀取（其中 `status running` 的 1063 筆），不是 1645 次獨立量測；畫布上改寫「17 heartbeat sessions · run 09-26 17:29Z」。
- 🔴 **這個「0」沒有 live 陽性對照**：主機 sniff 與 daemon 計數兩個偵測器只在離線證過「真的有幀到主機時會被認出來」（P4-HB-SPIKE.md §3.3 第 5 點）。講者備註要在「0」旁邊說。
- 🔴 **這一輪（09-26 17:29Z 起，H6 的第三欄）混進過一次外來流量，要揭露**（2026-09-27 UTC 第二輪，coordinator 第 14 項）：
  17:55:05–17:55:17Z，另一個 worker 的離線測試（`tests/shell/test_live_p1_common.sh` 的 5e 格）在這輪 live 06 的真主機之間跑了一段 2 Mbit/s iperf
  （`FIXED-SINCE-916.md` 的「5e no-lab」列；事故紀錄 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926/hbw-live/INCIDENT-20260926T1755Z-worker-traffic-into-live-06.md:1-29`）。
  受影響的只有 `2026-09-26T175425Z_p4runtime_solution_ndtwin` 的 G1 位元組（約 +8.6%；`E/runs/2026-09-26T175425Z_p4runtime_solution_ndtwin.md:613` 的 s1-eth2 4,735,073 B，對 T06 同一臂 `E/runs/2026-09-27T081205Z_p4runtime_solution_ndtwin.md:612` 的 4,361,273 B，+8.57%，該臂判定仍 PASS）；下一臂 `E/runs/2026-09-26T175515Z_flowcache_solution_ndtwin.md:593-594` 的兩條主路徑
  （s1-eth3 4594228 B、s3-eth1 4593189 B）是一份 iperf 的量、**沒有加倍**。這頁比的是每臂的 rc 與判定（26/26 相同），以及 sampler 的 host 埠幀數（0），兩者都不看 G1 位元組，
  所以本頁的「相同」與「0」不受影響——但那一臂的 G1 數字不可當乾淨數據。修法 `3db3b9a8`（假 fabric、sudo／mnexec／iperf 換成記錄並拒絕的 stub）。
- 🔴 dirty checkout：參照 run `0c96c1d0 +79 file(s)`、三輪心跳 run `cafd518a +88`、`3f8c2abf +91`、`5dc7fc9a +95`（各 arm report 的 `code` 行）；H5 那輪 08 本身 `3f8c2abf +89 file(s)`（`00_status_before.txt`）。09-27 那輪（T06）在 audit-raw `797c34ab`。

## 資料來源（腳本執行時讀取）

L＝`/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs`；E＝`/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep`（上面判官修正段的 `E/runs/…` 用這個）

| 用途 | 檔 | commit／binary |
|---|---|---|
| 參照 | `L/2026-09-24T185505Z_06_thirteen/00_table.tsv` 欄 1–4 | code `0c96c1d0`（arm report `ndt status`） |
| 心跳三輪 | `L/2026-09-26T153300Z_06_thirteen`、`L/2026-09-26T172913Z_06_thirteen`、`L/2026-09-27T074635Z_06_thirteen` 的 `00_table.tsv` | code `cafd518a`、`3f8c2abf`、`5dc7fc9a` |
| 哪 17 臂有心跳 | 各 `00_table.tsv` 欄 5 的 arm report 內 `heartbeat started (pid` | 同上 |
| host 埠 0 幀 | `L/2026-09-26T172912Z_08_heartbeat/50_samples.tsv`：1645 筆資料列，`forwarded_to_hosts` 欄全 0，`status running` 的 session 17 個 | repo HEAD `3f8c2abf`、kernel `be70b5dd32356847`（同目錄 `01_binaries.txt`） |
| 08 腳本自己的判定行 | `…/intake-0926/hbw-live/h5b-20260926T172912Z.log:47`（26 臂與 185505Z 相同）、`:48`（「a heartbeat ran on exactly the 17 expected arm(s); no host-port frame in 1617 samples」） | 同上 |

腳本斷言：三輪與參照在 26 臂的 (rc, verdict) 逐一相等；參照 0 臂、三輪各 17 臂有心跳；`forwarded_to_hosts` 總和 0。

## 可信度

**OBSERVED**：圖上所有格與「0」。raw 未提交（觀測）；audit-raw `797c34ab` 有 185505Z、153300Z、172913Z 與 09-27 T06 四輪的表（逐檔 blob 與工作樹相同，2026-09-27 17:2xZ 本機比對；`797c34ab` 依 coordinator 已公開在兩個 P4 repo）。

**READ**：`forwarded_to_hosts` 的定義——心跳幀以 OUTGOING 離開一個 host-facing 介面（`tools/test_workflow/ndtwin-lab:1095-1161`，轉引 P4-HB-SPIKE.md §3.1 `:360-363`）。

**INFERRED**：無。

## 已知但書

- 1645 對 1617（**已對帳**）：08 腳本在 06 結束、01 開始之前做 H5 判定（`08_heartbeat.sh:1968` 的 `v_h5_heartbeat` 以當下檔內筆數 `len(ss)` 印出，`:550-577`）。`50_samples.tsv` 第 1617 筆資料列的 wall 時刻是 17:56:10Z，正是 01 的 run 目錄 `2026-09-26T175610Z_01_baseline` 開始的那一秒；sampler 繼續讀到 17:56:38Z（01 期間，共 28 筆），檔案最後 1645 筆。兩個數字都是 0 幀，差的 28 筆是 01 那段的取樣（`v_no_session` 讀的正是那一段）。我用 python 從檔案重算：wall < 17:56:10Z 的有 1616 筆，第 1617 筆恰在 17:56:10Z。
- 第一次 H5（09-26 15:33）的 06 同樣 26/26 與參照相同，但它的 sampler 因為內嵌程式的 SyntaxError 一筆都沒記下（`L/2026-09-26T153259Z_08_heartbeat` 沒有 `50_samples.tsv`；修在 merge `0925d9fc`）⇒ 「0 幀」只來自 17:29 那一輪。
- 判定相同 ≠ 位元組相同：比的是 rc 與判定字串，不是每個封包。
- 26 − 17 ＝ 9 臂沒有心跳：單交換機（calc、multicast 各兩臂，沒有交換機間的線）、external 控制面（p4runtime 兩臂、flowcache 解答臂）、兩個設計上建不起來的骨架臂（basic_tunnel、flowcache）。那 9 臂的「相同」與心跳無關。
- 兩個副作用偵測器（主機 sniff、daemon 計數）只有離線的陽性對照，沒有 live 陽性對照（P4-HB-SPIKE.md §3.3 第 5 點）。

## 重生指令

見 `fig_h0_why_not_lldp.md`（同一支 `make_heartbeat_extra_figs.py`）。最後產出：2026-09-27T19:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_heartbeat_extra_figs.py` sha256 `9f5bcc908075125b…`（產圖之後腳本沒再改過）。
