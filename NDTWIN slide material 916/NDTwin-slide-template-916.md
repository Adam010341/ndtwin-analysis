# NDTwin 進度報告簡報 — 2026-09-16 版・資訊模板

**v0.4（09-10：909 場次取消，素材整份遷到 916；09-08 晚 v0.3 瘦身）。本檔是唯一事實來源，Adam 直接編輯；產檔由 Adam 的 cowork session 跑 JS 產生器（本機無 Node），動工前先讀最新版。**
v0.2 全文（含被刪掉的圖規格與更正紀錄）在 `_superseded/NDTwin-slide-template-916_v0.2-full_0908.md（909 原稿）`。

## 0. 五條規則

1. **只講 09-03 之後的事。** 903 講過的一頁不放、不提（Adam 09-08 裁）。09-08 17:56 產的 31 頁 `NDTwin_deck_909.pptx`／`.pdf`（已移到 `_superseded/`）含 903 的 23 頁 ⇒ **作廢，照 §1 重產為 `NDTwin_deck_916`。**
2. **圖頁只放圖。** p.2、p.5–p.8＝標題＋一張圖撐滿內容區（寬 ≥ 12"），**沒有 caption、kicker、chip、判詞**（Adam 09-08：字太小、口頭講）。要講的全進講者備註。p.7 兩張並排各半寬，嫌小就拆兩頁。
3. **圖檔**：`figures/<主題>/<name>.{pdf,png,svg}`＋`_hires/`＋同名 `.md`（資料來源、可信度、regenerate）。現有的全是 **matplotlib 草稿**（數字與結構對帳過）；定稿由 Adam 交另一位 agent，以草稿＋同名 `.md` 為規格。
4. **證據紀律**：每個實測數字旁標 commit；🟢 親自執行／🟠 讀過未執行**不可混寫**；場地名不上台面。頁腳統一 `Read at trunk 1a284f75 · exercises run 09-08 on their own harness`，不寫 `Measured at`。
5. **視覺規約**沿用 827 §E2（色票／字型）、§E3a（版面文法）、§E5（標題 ≤45 字元）：`../NDTwin slide material 827/NDTwin-slide-template-827.md`。

## 1. 頁序（9 頁；頁碼 Adam 定）

| # | 頁標題 | 圖 | 規格 |
|---|---|---|---|
| 1 | Title | — | — |
| 2 | Found, then fixed — since 09-03 | `figures/fixed-since-903/fig_h1_fixed_since_903` | §2 |
| 3 | One flag, two meanings | 無 | §3 |
| 4 | What the night round found | `figures/overnight-0904/fig1…fig6`（一頁六列縮圖） | §4 |
| 5 | What the tutorials ask for | `figures/p4-tutorials/fig_t1_requirements_matrix` | §5 |
| 6 | Where the five gaps live | `figures/p4-tutorials/fig_t2_gap_architecture` | §5 |
| 7 | What only a foreign P4 program reveals | `fig_t3a_silent_zero`＋`fig_t3b_election_wipe`（並排） | §5 |
| 8 | Three phases to a regression gate | `figures/p4-tutorials/fig_t4_phases` | §5 |
| 9 | Where it stands | 無 | §6 |

## 2. p.2 Found, then fixed — since 09-03（圖頁）

資料正本 `FIXED-SINCE-903.md`（同目錄；每列附進 trunk 的 commit／分支 tip＋證據；09-08 一支 opus agent 逐格核過）。
圖＝看板（磚 × 日期 × 兩帶）；chip 與判詞都在圖裡：`47 FIXES ON TRUNK · 29 BRANCHES WAITING · 0 ON THE PUBLIC REPO`、`FIXED / NOT SHIPPED`。
🔴 **待 Adam**：09-02 那一欄 20 塊（切點前一天，磚帶 `?`）——09-03 講過就拿掉：把 `make_fixed_since_903.py` 的 `TRUNK_0902` 清空重跑。
要細講哪幾支：`REPORT-PICK-FIXED.md`（同目錄，Adam 挑；09-10 尚未挑）。

**講者備註**
- 09-03 之後 trunk 多 47 支修法、分支上 29 支修好等併、直接落 trunk 5 顆；**沒有一顆推到公開 repo**（`p4public/main` 停在 09-03 `9e6cc307`、落後 1689 顆——tracking ref，只證明沒推）。
- 絕大多數修法有變異閘門看過紅；例外寫在正本證據欄（#85 的 TESTBED 半、#64/#65 那支閘門 auditor 沒重跑）。標 live 的在 lab 親自重跑過。
- Q12 是唯一 breaking change。「修在 trunk」≠「使用者拿得到」——公開路徑是 `NDTwin-Kernel-P4-public`。

## 3. p.3 One flag, two meanings（Q12）

**版型**：左欄「問題」（兩列表）＋右欄「量到的後果」（三個數字）＋底部「裁決」一行。無圖。
**標題** `One flag, two meanings`
**副標** `is_up answered "did we switch it off?" and "does it answer?" with one bit — the twin now keeps two.`

**左欄：問題**

| 寫 `is_up` 的人 | 它的意思 |
|---|---|
| 電源 API（`powerOff` 在 helper 確認行程已殺之後） | **決定**：我命令它關 |
| 1 Hz liveness worker（讀 proxy 快取的 `probe_ok`）、拓樸 poll | **觀測**：它有回應 |

一個 bit 分不出「牆上開關關了」與「燈泡燒了」。

**右欄：量到的後果**
🟢 親自執行（#46 修法的 live 兩臂各 9 次，`ndt up p4 4`；碼 `7e8d91e0`、併入 trunk `85c1a159`；raw `audit-raw @ 19e3ab88`）：
- 命令關機後 **0.3–1.5 s** `is_up` 被 liveness 快取寫回 true，撐 **8–13 s** 才回 false（兩臂 **18/18**）。
- 兩台一樣死透的交換機：被命令關的報 **OFF**、自己掛的報 **ON**——`/ndt/get_switches_power_state` 報的是指令不是量測（#33）。
- 「有沒有不該掛的東西掛了」（A-8 三態檢查）兩邊讀同一個 bit ⇒ **結構上永遠不會響**（#34）。

🟡 讀過未執行（不要寫得像跑過）：修 #46 之前，被 kill 的交換機 **7.5 分鐘**後 twin 仍報 `is_up=True`（09-03 night-rounds 的 persona 輪）。#46 修後 poll 那扇門已關：fixed 臂 **6/9** 在 poll 瞬間（t_off+2.56–2.60 s）印出拒絕復活，逐筆對上 harness 記的 poll 落點。

**底部：裁決（09-03，Adam）**
拆成 `admin_state`（on／off，由命令決定、立刻正確）＋ `reachable`（probe 的答案，可以誠實說「快取未過期」）；`is_up` 暫留為 `reachable` 的別名；四個 consumer 分批改。

**狀態（09-08 查證）**：修法**已在 trunk**——`fix/is-up-split-admin-state-reachable` 09-04 併進 integrate 線（`95a9f743`），09-05 15:27 隨 `cdc8dad9` 進 trunk；API 文件 `2cd796ff`；合併樹 ctest 1022/1022，W2/W3 併後的 trunk 樹 1083/1083＋R0b live。**未發布。**
keyLine：`Decided and on trunk since 09-05 -- not yet published.`
🔴 唯一 breaking change 要講：`/ndt/get_switches_power_state` 的 body 從 `{"ip":"OFF"}` 變 `{"ip":{"admin_state":"off","reachable":false}}`。

**講者備註**：這是設計裁決不是補丁。候選 (b)「一欄加 `source`」只是把歧義搬進欄位；(c)「不動」等於接受 8–13 s 的謊。與 #46（poll 不得覆蓋關機命令）同根：#46 在 twin 內部先把兩個旗子分開，Q12 把分開的結果搬到 API 上；順帶把 #80 的 15 s「不信任窗」從時間改成證據（下一次真的 probe 成功才關窗）。

## 4. p.4 What the night round found（09-04 夜巡六條，一頁六列）

第一批**只有 current behaviour、沒有 after 側**（binary 沒重建；after 側補上後再拆成六頁）。全部 🟢 跑過；kernel `cca5e3e4ebc42358`、helper `6685d3a9`。圖在 `figures/overnight-0904/`（`make_overnight_figs.py` 一支產六張；`_hires/` 是 `pdftoppm -r 500`）。

| 圖檔 | 一句話 | 現況數字（commit） | raw 出處 |
|---|---|---|---|
| `fig1_declared_vs_real_link_failure` | API 宣告的斷鏈會被 30 s 拓樸輪詢默默蓋回 up；真斷鏈（`tc netem`）60 s 窗口內從不自己回來 | OVS4 declared 自己翻回：25.4／24.4／23.4／22.5／21.5 s（trunk `4088b237`）；P4-4 declared：1.6／10.6／13.6／19.6 s（trunk `f943de8f`，5 次裡 1 次在 20s 窗口內未翻回，右設限未畫）；真斷鏈：≥60 s 才由 `tc qdisc del` 手動復原 | `logs/r2-20-linkfail-probe.log`、`logs/p4-4-14-linkfail.log`、`logs/r2-21-netem-control.log` |
| `fig2_shutdown_southbound_writes` | kernel 印出「All subsystems stopped. Exiting.」之後又花 10.7 s 寫真交換機，過程 0 行 log 提到這件事 | SIGINT→Exiting 0.595 s；Exiting→行程消失 10.743 s（SIGINT→消失合計 11.338 s，trunk `4088b237`）；對照 idle SIGINT 基準 ≈2.4–2.53 s（🟡讀過，另一輪／另一顆 binary，git rev `6283ff5e`，非本輪 `cca5e3e4ebc42358`） | `logs/r2-60-graph-during-shutdown.log`、`logs/r2-61-batch-response.log`、`logs/r2-62-shutdown-analysis.log`；idle 對照：`doc/audit/2026-09-02_live-round/B5-REPORT.md` §6 |
| `fig3_dispatch_counters_vs_switch_truth` | `get_flow_dispatch_status.succeeded` 數的是「POST 沒噴錯」，不是「交換機真的變了」 | 20× 裝同一條 match：succeeded +20／交換機 +1；15× 刪不存在的 match：succeeded +15／交換機 +0；對照組 1× 真的刪除：succeeded +1／交換機真變 1 列（皆 trunk `4088b237`） | `logs/r2-30-b3-same-match.log` |
| `fig4_group_install_delete_readback`（表，非圖——見旁 `.md` 說明為什麼不畫長條） | `install_group_entry` 對兩個保留 group id 都回「200 installed」，但 `groupdesc` 上從來沒出現過；同一支程式的 delete 分支老實回 404 | group id `4294967295`／`4294967293`：install 200「installed」、groupdesc 缺席、delete 404「no_such_group」（trunk `4088b237`）；控制組 id `899`（從未裝過）：modify／delete 皆誠實 404 | `logs/r2-40-b1-group.log`、`logs/r2-41-b1-group-extra.log` |
| `fig5_path_switch_count_static` | `get_path_switch_count` 不讀活拓樸，是靜態模型算出來的常數 | 32/40 與 20/40 交換機間邊判 down 前後，12 條路徑的 `switch_count` 逐格相同（3 或 5，trunk `f943de8f`） | `logs/p4-4-15-pathmetric.log`、`logs/p4-4-pathcount-allon.json`、`logs/p4-4-pathcount-3off.json` |
| `fig6_endpoint_latency_profile` | 同樣是 OpenFlow write，meter install/delete 比 group 慢了約 40 倍 | `install_meter_entry` 1024 ms／`delete_meter_entry` 1029 ms vs `install_group_entry` 20 ms／`modify_group_entry` 24 ms／`delete_group_entry` 34 ms（皆 OVS4，trunk `f943de8f`，client 端量的 HTTP 往返，不是南向可見延遲） | `logs/ovs128-02b-sweep2.log`（P4 對照數字在旁 `.md`，來源 `logs/p4-4-02-sweep.log`） |

**講者備註**：fig1 與 fig3 的缺陷 09-05 之後已有修法（B-6 → 分支 W8／W8b；#54 → 分支 W11），**都未併**——講「量到」不講「修好」。下一批候補（#87 讀回狀態碼、OV-2／OV-3 狀態碼、`ndt up/down` 秒數）資料已齊，見 `scratch/overnight-2026-09-05/rounds/`。

## 5. p.5–p.8 P4 tutorials as requirements（四張圖頁）

**題目**：教授要「拿 p4lang/tutorials 的 exercise 測 NDTwin」；Adam 09-08 定調目的＝「用真實需求找出 kernel／proxy 缺什麼」⇒ 13 支 × 16 維需求 → 同 16 維盤點 NDTwin → 對表 ⇒ **五個真 gap、兩個只有換程式才暴露的發現、三階段**。正本 `doc/audit/2026-09-04_p4-tutorial-exercise-prep/GAP-ANALYSIS.md`（＋`GAP-1`、`GAP-2`、`runs/*.md`）；讀的樹＝trunk `1a284f75`、tutorials `c80d83e`。

**證據紀律（這四頁的 🟢／🟠 分界）**
- 🟢 實跑：09-08 17:24 Adam 以 root 跑 `drive_exercise.py` 四次——`source_routing` solution **5/5**（h2 收 2 包、ttl {59, 62}）／skeleton **2/2**（h2 收 0 包；`s1.log` 91 行 `Dropping packet at the end of ingress`）；`basic` solution **5/5**（pingall 0% 丟、ttl 63）／skeleton **4/4**（pingall 100% 丟）。**跑的是 tutorials 自己的 harness＋`/usr/local/bin/simple_switch_grpc`（`327fa7d1`，不是 bmv2-fast）**——證明的是 exercise 的預期行為與 driver，**不是** NDTwin 能跑它：**0/13 在 NDTwin fabric 上跑過。** 另兩個 🟢：編譯矩陣（09-04 實編 26 支）、發現②（08-13 三情境實測）。
- 🟠 讀碼：五個 gap、發現①、三階段的行數全是讀碼推導與估計。

### p.5 `WHAT THE TUTORIALS ASK FOR`　圖 `fig_t1_requirements_matrix`
**講者備註**：13 支 × 16 維（關鍵／用到／沒用到），底部一列 NDTwin today（做得到 1／部分 9／做不到 6）。8 支要的是「載入任意 P4 程式」這件事，不是新功能；16 維裡 6 維問的是「NDTwin 自己那支 `.p4` 有沒有」，每支 exercise 都自帶 `.p4` ⇒ 能載任意 pipeline 就自動滿足。只有 exact＋lpm；0/13 需要 meters／digest。basic 唯一零改動，但三個 caveat：pod-topo 仍要走拓樸選檔三處推導；NDTwin `ipv4_lpm` 預設 `send_to_cpu()`、basic 是 `drop()` ⇒ 骨架在 NDTwin 上是 punt 不是 drop；載 basic 自己的 pipeline 後 clone 取樣遙測不存在。

### p.6 `WHERE THE FIVE GAPS LIVE`　圖 `fig_t2_gap_architecture`
**講者備註**：六個徽章的行數全是【估】。順序＝解鎖支數 ÷ 工作量：G2 拓樸模型（13/13）、G4 pipeline loader（12/13）、G5 table writer（12/13，含 default_action 無寫入路徑）、G1 packet-in decoder（12 支的遙測）、G3 election_id、G6 kernel sFlow parser（6 支轉得動但分身全盲）。**一行都還沒改**，不講「修好了」。圖上 G2 畫成第一階，實際橫跨一、三（C＝`link=TCLink` 整形在第三階）——講 ecn／mri 時補一句。其餘 G7／G8／G9 在正本 §3。

### p.7 `WHAT ONLY A FOREIGN P4 PROGRAM REVEALS`　左 `fig_t3a_silent_zero`＋右 `fig_t3b_election_wipe`
**講者備註**：① 左圖是讀碼（`sflow_emitter.py:425-429,468-470`、`ndtwin_switch.p4:52`）：packet-in metadata 依位置取 id 5 當 `sampling_rate`，換一支欄位順序不同的 `.p4` 就讀成 0，`== 0` 的樣本直接丟、沒有 log——講機制不講「觀察到歸零」。② 右圖是 08-13 三情境實測：proxy 與 tutorials 的 `mycontroller.py` 投同一個寫死的 election_id (0,1)，bmv2 依規格把冒名者的 stream 當重複殺掉，但它的 `SetForwardingPipelineConfig` 照樣被接受、清空每一張表、回 OK。**bmv2 全程符合規格**（真正非 primary 的第三方推送被 `PERMISSION_DENIED` 擋下，08-13 情境 1）——一定要講，不然像在指控 bmv2。另：`mycontroller.py` 寫死 `50051/dev 0`、NDTwin 是 `30050+dpid`，連位址都對不上（讀碼）。

### p.8 `THREE PHASES TO A REGRESSION GATE`　圖 `fig_t4_phases`
**講者備註**：左階梯＝累計行數【估】140／470／675 對可跑支數 1／10／13；GATE 在第二階之後。右 2×2 是 09-08 的四次實跑（skeleton 欄＝expected fail，紅綠都看過）——**tutorials 自己的 harness，不是 NDTwin**。三件成立（載任意 pipeline、依 p4info 寫任意表、換程式遙測不歸零）後 `drive_exercise.py` 的 exit code 0／1／2 就是閘門。第三階段前 ecn／mri 會「綠得很可疑」（qdepth 恆 0），不可進閘門。

## 6. p.9 Where it stands

三列 label→value：`29 branches · not merged`／`0 commits · on the public repo since 09-03`／`phase 1 · ~140 lines · unlocks basic`。
**講者備註**：併序在 `FIXED-SINCE-903.md` §3 末（ndt 鏈／W8 鏈／W15 鏈各自線性）；推的目標是 `NDTwin-Kernel-P4-public`（不是 origin）；三階段第一階＝G1＋G3＋G2-A/B，驗證＝basic 在 NDTwin fabric 上跑通。

## 7. 素材出處速查

| 數字／主張 | 出處 |
|---|---|
| 0.3–1.5 s、8–13 s、18/18 | `doc/audit/2026-09-03_fix-poll-resurrect/FIX-POLL-RESURRECT.md` §3.3.2；raw `audit-raw:doc/audit/2026-09-03_fix-poll-resurrect/raw/02_phase_a_base.log`／`03_phase_a_fixed.log`（`19e3ab88`） |
| 6/9、t_off+2.56–2.60 s | 同上 §3.3.1；`raw/04_fixed_arm_kernel_declines.log` |
| OFF／ON 不一致、A-8 恆空、7.5 min | `doc/audit/2026-09-03_night-rounds/QUESTIONS-FOR-ADAM.md` §Q12 第一段；FINDINGS-ALL #33、#34、#46 |
| Q12 裁決與三個選項 | `QUESTIONS-FOR-ADAM.md` §Q12 補充＋裁決行（trunk `b57736cd`） |
| Q12 修法在 trunk | MERGE-LOG 列 38（`95a9f743`）；`cdc8dad9`；`WAKEUP.md` §2.2（未提交檔） |
| 47／20／5／29／7／0／8 | `FIXED-SINCE-903.md` §1（git 09-08 18:0x；116 sha 機器核過） |
| 13×16、exact＋lpm only、0/13 meters／digest、1/13 unchanged | `GAP-1` §2、§4a–4c |
| 25/26 rc=0 🟢 | `COMPILE-MATRIX.txt`（09-04；`p4c-bm2-ss` `226f3f66df515c9e`） |
| NDTwin 做得到 1／部分 9／做不到 6 | `GAP-2` §1 |
| 五個 gap 行號與量級 | `GAP-ANALYSIS` §1／§3；auditor 09-08 抽查：`p4_testbed_topo.py:120-134`、`main.py:185-186`、`p4_client.py:846`、`sflow_emitter.py:425-429,468-470`、`FlowLinkUsageCollector.cpp:1266` |
| 發現② 🟢 | `doc/2026-08-13_p4runtime-mastership-spec-check.md`；`p4_client.py:60-72`；`p4runtime_mastership_probe.py` |
| 三階段 ~140／~330／~205 | `GAP-ANALYSIS` §6（全部【估】） |
| 四次實跑 5/5、2/2、5/5、4/4；ttl {59,62}／63 | `runs/2026-09-08T0924*_*.md`（tutorials `c80d83e`；switch `327fa7d1`） |
| 91 行 drop | `~/tutorials/exercises/source_routing/logs/s1.log` 本身（不在 `runs/`）；auditor 09-08 `grep -c`＝91（159467 B，mtime 17:24:36） |
| 兩顆 bmv2 | tutorial-prep `README.md` §3：tutorials `/usr/local/bin`（`327fa7d1`）vs ndt bmv2-fast（`3ff54b5c`），版本字串相同、sha 不同 |

## 8. 圖面清單（全部草稿；定稿由 Adam 交另一位 agent）

| 圖 | 頁 | 狀態（09-08） | 對帳 |
|---|---|---|---|
| `figures/fixed-since-903/fig_h1_fixed_since_903` | 2 | 21:18 重生；96 塊磚＝67 trunk（47＋09-02 的 20）＋29 分支；`make_fixed_since_903.py` 內建磚數 assert | 同名 `.md` §4 逐磚分類（kernel 46／ndt 18／其他 31／混合 1） |
| `figures/overnight-0904/fig1…fig6` | 4 | 09-05 16:01；只有 current 側 | 各同名 `.md` |
| `figures/p4-tutorials/fig_t1_requirements_matrix` | 5 | 17:42；`make_tutorial_figs.py` 15 條計數斷言 | 同名 `.md`（208＋16 格） |
| `figures/p4-tutorials/fig_t2_gap_architecture` | 6 | 17:54；兩處刻意不照原規格（中層排序讓 sFlow 箭只跨一格；G2 畫成第一階） | 同名 `.md` |
| `figures/p4-tutorials/fig_t3a_silent_zero`／`fig_t3b_election_wipe` | 7 | 17:54；同高，設計成並排 | 同名 `.md` |
| `figures/p4-tutorials/fig_t4_phases` | 8 | 17:54；GATE 在 470 | 同名 `.md` |

不畫「五個 gap 長條圖」：行數是【估】，畫成長條會被讀成量出來的。

[Co-developed with claude code -- Adam]
