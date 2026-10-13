# `fig_h0_why_not_lldp` —— 為什麼 NDTwin 的鏈路偵測到外來 P4 就停了

[Co-developed with claude code -- Adam]

（本檔所有時間為 UTC；run 目錄名的 `…Z` 就是 UTC。）

## 一句話

NDTwin 自己的 LLDP 靠 packet-out／packet-in 來回，而那需要 P4 程式裡有 controller header；
外來程式（tutorials 的 exercise）沒有 ⇒ proxy 在外來 fabric 上整個跳過 LLDP、link watchdog、初始路由，
於是剪一條線 twin 看不到。這就是第二刀（veth 心跳）要解的問題。

## 資料來源

K＝`/home/adam/Desktop/NDTwin-Kernel`

| 用途 | 檔 | commit／binary |
|---|---|---|
| 為什麼跳過（設計理由） | `K/p4_proxy/proxy_agent/main.py:2141-2148`（「LLDP discovery, the link watchdog and (through them) install_initial_routes all ride packet-out and packet-in. Those need a controller header」） | trunk `3d740be0` |
| NDTwin 自己的程式有 controller header | `K/p4_proxy/p4_src/ndtwin_switch.p4:156`（`@controller_header("packet_in")`）、`:167`（`packet_out`） | trunk `3d740be0` |
| 圖底下那三個字（live 上真的被跳過；第三輪改源） | 09-24、心跳還不存在時的 live 07：`K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/2026-09-24T160256Z_07_roles_basic/70_up_plain.txt:63`（`control_plane.skipped: install_initial_routes, link_watchdog, lldp_discovery`）；同一次 bring-up 的 proxy `switch_state`（同目錄 `71_switch_state_plain.json:7`，`control_plane.skipped` 同三項、**沒有** `heartbeat` 這一欄） | code `572d9462 +61`（`00_status_before.txt:7`；2 個會改變行為：`p4_proxy/mininet/host_count_override`、`tools/remote-lab/dorm_lab/`）；raw 在 audit-raw `797c34ab` |
| 旁證 | 心跳 H1 run 的 `ndt up` 輸出 `…/live-p1/runs/2026-09-26T152605Z_08_heartbeat/20_up_roles.txt:82`：「NDTwin discovered no links and installed no routes on this fabric」 | repo HEAD `cafd518a` |

腳本斷言：`main.py` 仍含那兩句、`ndtwin_switch.p4` 仍有兩個 `@controller_header`；圖底的清單由 `footer_skipped()` 讀出來畫——09-24 的 up log 與 switch_state 必須列同樣三項，且清單說 `link_watchdog` 被跳過時，同一個 switch_state 的心跳 watchdog 不得在跑（第三輪加的停止條件）。

## 可信度

**OBSERVED**：底部三個被跳過的步驟（09-24 live 07，心跳加入之前；圖上標「RAN IT · 09-24, before the heartbeat」；raw 在 audit-raw `797c34ab`，逐檔 blob 與工作樹相同，2026-09-27 17:2xZ 本機比對）。

**髒 checkout**：圖底來源（09-24）是 `code 572d9462 +61`（上表）；旁證的 H1 run 是 `cafd518a +85`（`…/2026-09-26T152605Z_08_heartbeat/00_status_before.txt:7`），其中 2 個會改變行為：`p4_proxy/mininet/host_count_override`、`tools/remote-lab/dorm_lab/`（`…/intake-0926/hbw-live/h14-20260926T152605Z.log:14-17`）。

（2026-09-27 UTC 第二輪，coordinator 第 13 項：畫布上兩個小圖右上標「READ THE CODE」，底行標「RAN IT · T06」。）

**READ**：左右兩個小圖的機制（packet-out／packet-in 需要 controller header；外來程式沒有）＝ `main.py:2141-2148` 的說明與 `ndtwin_switch.p4:156-167`。本輪沒有 live 實驗「故意在外來程式上送 LLDP 看它不回來」——proxy 根本不送。

**INFERRED**：無。

## 圖怎麼讀

左：NDTwin 自己的 P4——proxy 從 A 送 LLDP（packet-out），B 收到後上送（packet-in），proxy 知道 A–B 這條線在。
右：外來 P4——packet-out 對它的 parser 來說是一個「從沒被寫來處理」的幀，沒有 packet-in 回來 ⇒ 看不到線。
第一刀（09-24）時，外來 fabric 上 kernel 圖裡的鏈路 `is_up` 只來自**宣告**（`doc/audit/2026-09-24_p4-driven-api-shape/REPORT-P4-2026-09-25.md:87-88`），不是偵測。

## 已知但書

- **為什麼不再用 T06 當來源（判官第三輪，coordinator 2026-09-27 UTC 裁）**：T06 那份 arm report 的清單仍列 `link_watchdog`（`E/runs/2026-09-27T074826Z_basic_solution_ndtwin.md:58`、`:236`），但同一個 switch_state 寫著心跳 watchdog 在跑（`:301` `"watchdog": "running"`；`:202-203` 心跳已啟動）——那是清單的誤報（`FIXED-SINCE-916.md` 的 rulings AEG 列，E 項，修在未併的分支上）。所以圖底改用 09-24、心跳還不存在時的那一次，三項都是真的。
- 紅檢：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/h0-footer-redcheck.py` 與同目錄 `h0-footer-redcheck-20260927T1941Z.log`：對照組過；心跳 watchdog 在跑、up log 與 switch_state 不一致、兩邊都拿掉 `link_watchdog`、up log 沒有 skipped 行、沒有 code 行——5 個竄改各停在對應原因。這支腳本其他的停止條件沒有紅檢。
- 「一台外來 ⇒ 整個 fabric 跳過」的理由也在 `main.py:2151-2153`：信標從一台出去、到另一台收，混合的線一樣偵測不到。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/heartbeat"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_heartbeat_extra_figs.py
```

一次產出 `fig_h0_why_not_lldp`、`fig_h0b_heartbeat_path`、`fig_h3_upper_bound`、`fig_h4_forwarding_unchanged`。最後產出：2026-09-27T19:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_heartbeat_extra_figs.py` sha256 `9f5bcc908075125b…`（產圖之後腳本沒再改過）。
