# `fig_h3_upper_bound` —— 偵測上界，一段一段拆開

[Co-developed with claude code -- Adam]

（本檔所有時間為 UTC；run 目錄名的 `…Z` 就是 UTC。）

## 一句話

剪線到 kernel 圖 down ＝ (15 s − φ) ＋ ψ ＋ d ＋ ε。上面那條是 live 最慢的一次（16.8 s）逐段拆開；
下面那條是設計上的最壞：φ→0、ψ→5 s ⇒ 20 s 再加上 d ＋ ε ——「約 20 s」，與 NDTwin 自家 LLDP 同級。

## 符號

- φ：剪線落在最後一幀之後多久（`phi_s`）。
- ψ：規則成立（最後一幀 + 15 s）之後，watchdog 下一次 pass 還要等多久（`watchdog_phase_s`，0 到 5 s）。
- d：pass 開始到 kernel 圖轉 down（pass 本身、`_notify_link` 的 HTTP、kernel 更新、以及 08 腳本自己輪詢圖的間隔；`pass_to_graph_s`）。
- ε：其他沒單獨量的（讀報告檔等）；live 那條把它併在 d 裡。

## 資料來源

R＝`/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/2026-09-26T152605Z_08_heartbeat`

| 用途 | 檔 | commit／binary |
|---|---|---|
| live 那條三段 | `R/30_cycles.tsv` cycle 3（最大 `detect_s`）：15 − φ ＝ (`last_heard_*_mono` 72142.316 ＋ 15) − `cut_a_start_mono` 72142.344 ＝ 14.972；ψ ＝ `pass_start_mono` 72158.926 − 72157.316 ＝ 1.610（＝ `watchdog_phase_s`）；d ＝ `graph_down_mono` 72159.171 − 72158.926 ＝ 0.245（＝ `pass_to_graph_s`）；合計 16.827（＝ `detect_s`） | repo HEAD `cafd518a`、kernel `be70b5dd32356847` |
| 六個 cycle 的 d 範圍 | 同檔 `pass_to_graph_s`：0.031–0.245 s | 同上 |
| 設計那條的 15 s、5 s | `p4_proxy/proxy_agent/topology_manager.py:419`、`:422`；08 腳本印的設計式 `…/intake-0926/hbw-live/h14-20260926T152605Z.log:64`（標 INFERRED） | trunk `3d740be0` |

腳本斷言三段相加等於 `detect_s`、ψ 與 d 各自等於 tsv 的對應欄（差 ≤ 3 ms）。

## 可信度

**OBSERVED**：上面那條（三段與 16.8 s）。raw 在 audit-raw `797c34ab`（逐檔 blob 與工作樹相同，2026-09-27 17:2xZ 本機比對；依 coordinator 已公開在兩個 P4 repo）。**髒 checkout**：`code cafd518a +85`（`R/00_status_before.txt:7`），含 2 個會改變行為的檔：`p4_proxy/mininet/host_count_override`、`tools/remote-lab/dorm_lab/`。

**INFERRED**：下面那條——它是常數的算術，不是量測；d ＋ ε 在最壞相位下的值**沒有量過**（本 run 只量到 ψ≈1.5–1.8 s 這一個相位下的 d）。判官已證明「20 s ＋ 量到的 pass／HTTP／kernel」這種判準在設計正常時恆為 OK，是循環的，不能當驗收（`…/intake-0926/judge-HBW-1a3ebd7f.md:73`）。

**RULING（不是量測）**：Adam 2026-09-27 05:2xZ 裁決 A（記憶檔寫的是 +08 的 13:2x）——接受「約 20 s」（與自家 LLDP 同級），`strict_20s` 欄照記、超過只揭露不判 FAIL。記錄在 orchestrator 的記憶檔 `~/.claude/projects/-home-adam-Desktop-NDTwin-Kernel/memory/phase5-post-roles-state.md` 的「09-27 13:2x Adam 裁決 A–M」段（+08 標題）第 A 條（記憶檔持續被改寫，不引行號），**不在 repo 裡**；工單原本的驗收是 ≤ 20 s（`doc/audit/2026-09-25_p4-heartbeat/TICKET-P4-heartbeat.md:8-9`，自家 fabric「最多約 20 s」）。

## 圖怎麼讀

兩條橫條同一個時間軸；紅色虛線＝20 s。上面那條的灰色小段是 d ＋ ε（0.245 s）。
下面那條的斜線段＝d ＋ ε 的最壞值未知，所以寫「≈ 20 s」而不是「≤ 20 s」。

## 已知但書

- 事件驅動的 pass（報告一寫就判）可以把最壞推到約 15.5 s，但代價是 proxy 要 watch 檔案、LLDP 與心跳不再共用 pass 節奏——是設計選擇，沒排（`judge-HBW-1a3ebd7f.md:73`、段 W worker 的提案）。
- 自家 fabric 用同一條規則、同一組常數，所以剪線方向兩邊同性質（P4-HB-SPIKE.md §1 第 2 點，`:65`）。

## 重生指令

見 `fig_h0_why_not_lldp.md`（同一支 `make_heartbeat_extra_figs.py`）。最後產出：2026-09-27T19:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_heartbeat_extra_figs.py` sha256 `9f5bcc908075125b…`（產圖之後腳本沒再改過）。
