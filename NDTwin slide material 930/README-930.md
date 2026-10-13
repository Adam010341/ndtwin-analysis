# 930 素材總覽（2026-09-30 進度報告）

[Co-developed with claude code -- Adam]

整理：integrator，v1.2＝2026-09-27 19:0xZ（判官第二輪 READY AFTER FIXES 之後），第三輪修訂 19:5xZ（v1.1 是 17:4xZ，v1.0 是 16:4xZ）；**v1.3＝2026-09-28 07:xxZ 狀態更新**（Q4、Q5、F1、N1、T1，見 §9）；**v1.4＝判官 READY AFTER FIXES 之後的修正，08:xxZ**（§10）；**v1.5＝09:0xZ 重新釘住到 trunk `3368412d`、main `eef173a9`**（§11；在審那一項已 squash 進 main，中性磚規則解除）；v1.6＝13:2xZ F1 在審加一條（§12）；**v1.7＝2026-09-29**：Adam 09-29 的四條指示——拿掉 A1、A2、T2、Q1–Q5、F1，開場後新增背景段 B1–B5，T3 移到 B5 之後，N3 刪兩列、改一列，留下的頁的講稿刪掉開發過程的敘述（§13）。**36 → 32 頁**。**delta only，切點 2026-09-16。時間一律 UTC。** 投影片模板 `NDTwin-slide-template-930.md`；修法清單 `FIXED-SINCE-916.md`。
**v1.8＝2026-09-29**：R4、S2 兩張圖只畫最後狀態，N3 第 4 列換成非審查的證據，H4 講稿拿掉輪次字樣；pptx 重產、PDF 沒有（§13.7，模板 §1c）。
這個資料夾在 `NDTwin slide material` 這個 git 工作樹裡，而那個 repo 的 remote 是**公開的**。所以這裡的檔案一個都沒有 `git add`／commit／push，全部是 untracked（`git diff --cached` 為空，17:4xZ 查；09-28 07:2xZ 再查仍為空；2026-09-29 v1.7 改完再查仍為空，§13）。
kernel repo 只讀（證據讀自 trunk `3d740be0`→`fed37cff`，兩者之間只差 `tests/python/test_ndt_serve.py`；09-28 的更新讀到 trunk `85bec430`，重新釘住後讀到 `3368412d`，Q3、Q4、Q5、F1、N1 釘在那裡）；寫入 kernel 樹的是 git-ignored 的 `scratch/overnight-2026-09-05/logs/slides930/`（各產生器的紅檢腳本與 log，判官 F-20 要求移出 scratchpad），以及 09-28 依 Adam 裁定改的 GAP-2b 四格（coordinator 讀 diff 後提交 `c8433963`，見 §9）。
判官報告：`K/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926/slides930/judge-SLIDES930.md`（第一輪 FIX，見 §6）、同目錄 `judge-SLIDES930-r2.md`（第二輪 READY AFTER FIXES；coordinator 的 18 項，見 §7）。

## 1. 檔案

**頂層**
- `NDTwin-slide-template-930.md`：頁序、form、講者備註、出處、圖清單（**v1.7，2026-09-29**；v1.5 是 09-28 重新釘住）
- `FIXED-SINCE-916.md`：09-16 之後的修法，分三種狀態，快照 trunk `3368412d`（之前是 `85bec430`、09-27 版是 `fed37cff`）
- `README-930.md`：本檔
- `NDTwin_deck_930.pptx`：2026-09-29 以 v1.7 重產，32 頁（模板 §1b、本檔 §13）
- `NDTwin_deck_930.pdf`：🔴 **仍是 09-28 的 36 頁版，沒有重產**（本機沒有 LibreOffice）；要 PDF 就從新的 pptx 重轉
- `FIXED-SINCE-916.md` 對應的 F1 頁 09-29 拿掉了；清單本身沒動，N3 第 7 列仍引它的 §8–§9

**`figures/`**：每張圖都有 `.pdf`、`.png`（300 dpi）、`.svg`、`_hires/<stem>.png`（500 dpi），以及同名 `.md`（出處、髒 checkout、可信度、紅檢、重生指令）。

| 資料夾 | 圖 | 產生器 | 其他 |
|---|---|---|---|
| `background/`（09-29 新） | `fig_b2_basic_walkthrough`（B2）、`fig_b3_basic_tunnel`（B3） | `make_background_figs.py` | 全部讀自 tutorials `c80d83e`（`git show`）；紅檢 81/81 |
| `overview/` | `fig_o1_since_0916`、`fig_o2_thirteen` | `make_overview_figs.py` | 09-29 起兩張都只留存檔（A1、A2 拿掉） |
| `p4-tutorials/` | `fig_t1c_ndtwin_coverage`（T1，本輪新）、`fig_t5_arms_by_run`、`fig_t6_multicast_end_to_end`、`fig_t7_preflight_checks`、`fig_t8_what_you_bring`、`fig_t9_custom_headers`；存檔 `fig_t1b_requirements_matrix_0927`（由 916 **複製**，不上 deck） | `make_coverage_0930.py`（新）、`make_tutorial_figs_0927.py`（複製版；t1c 當模組 import）、`make_arms_grid.py`、`make_exercise_path_figs.py` | 09-29 起 `fig_t5_arms_by_run` 只留存檔（T2 拿掉） |
| `foreign-p4/` | `fig_a1_foreign_p4_path` | `make_foreign_p4_diagram.py` | |
| `roles/` | `fig_r2_roles_path`、`fig_r3_live07`、`fig_r4_capabilities`；存檔 `fig_r1_four_rulings`（R1 改表格） | `make_roles_figs.py` | |
| `heartbeat/` | `fig_h0_why_not_lldp`、`fig_h0b_heartbeat_path`、`fig_h1_one_cut_cycle`、`fig_h2_detect_vs_phase`、`fig_h3_upper_bound`、`fig_h4_forwarding_unchanged` | `make_heartbeat_figs.py`（h1、h2）、`make_heartbeat_extra_figs.py`（其餘四張） | |
| `flow-api/` | `fig_d1_flow_api_matrix`、`fig_d2_queued_readback` | `make_flow_api_matrix.py`、`make_queued_readback.py` | |
| `ndt-serve/` | `fig_s1_serve_path`、`fig_s2_security_model`、`fig_s3_cells_and_walks`；存檔 `fig_s4_gui_plan`（S4 改表格） | `make_serve_diagram.py`、`make_serve_s2_s4.py` | `_raw/last-run.log`、`_raw/ss-listen-3000-8765-20260927.txt` |
| `telemetry/` | `fig_m1_sampling_error` | `make_sampling_error_fig.py` | |
| `engineering/` | `fig_q1_protobuf5`、`fig_q2_review_path`、`fig_q4_ci_state`、`fig_q5_main_by_pr`；存檔 `fig_q3_review_catches`（Q3 改表格） | `make_engineering_figs.py` | 09-29 起 q1、q2、q4、q5 也只留存檔（Q 段拿掉）；`_net/`：未認證 GitHub API 快照（2026-09-28 08:53:29Z，`when.txt` 逐次記；`prev-*` 是之前各份，最近的是 `prev-20260928T0832Z/`、`prev-20260928T0645Z/`、`prev-20260928T0616Z/`）；`jobs_*.json` 是各 run 的四個 job |
| `fixed-since-916/` | `fig_f1_fixed_since_916` | `make_fixed_since_916.py` | 09-29 起只留存檔（F1 拿掉）；圖是解析 `FIXED-SINCE-916.md` 畫的；`public-check-20260927.log` 是未認證 curl 的紀錄；`public-check-20260928/` 是 09-28 06:20Z 未認證 GET 的 5 個 JSON（每次請求逐行在 `slides930/net-refresh-20260928T0616Z.log`）；`public-check-20260928b/` 是重新釘住時 08:38Z 的 5 個 JSON（`slides930/net-repin-20260928T0831Z.log`） |
| `next/` | `fig_n1_roadmap`（不含 detect-only）；存檔 `fig_n1_roadmap_with_detect_only`（第一輪原檔） | `make_roadmap.py`（`--with-detect-only` 重生存檔版） | |

總數（2026-09-27 19:0xZ `find`；09-28 07:2xZ 再數圖、腳本、`.md` 都沒變，檔案 260 個，多的是 `_net/` 與 `public-check-20260928/` 的快照）：**35 張圖**（30 張上 deck、5 張存檔：t1b、r1、s4、q3、n1_with_detect_only）、**17 支腳本**（16 支產生器＋`make_tutorial_figs_0927.py` 複製版，t1c 把它當模組用）、
**34 份圖 `.md`**（存檔的 n1 變體沒有自己的 `.md`，寫在 `fig_n1_roadmap.md` 裡）、**223 個檔**（35 個 300 dpi PNG、35 個 `_hires` PNG），沒有 `__pycache__`。每份 `.md` 的「最後產出」行記 PNG 時間與產生器 sha256。
**09-29 再數**（`find`）：**37 張圖**（24 張上 deck、13 張存檔＝原本 5 張＋09-29 拿掉的頁的 8 張）、**18 支腳本**（加 `make_background_figs.py`）、**36 份圖 `.md`**；`figures/` 底下 295 個檔（37 個 300 dpi PNG、37 個 `_hires` PNG），整個資料夾 301 個檔，沒有 `__pycache__`。
`p4-tutorials/fig_t1b_*` 與 `_hires/fig_t1b_*` 是從 `NDTWIN slide material 916/figures/p4-tutorials/` **複製**來的，916 那份沒動；09-27 重生後的 PNG 和 916 版逐位元相同；**09-28 起不同了**：GAP-2b 四格裁定後重生，虛線待審框拿掉、flowcache 的 twin 格變 IPv4 only（§9）。它是 916 第 3 頁，所以不上 930 的 deck（判官 F-2）。

紅檢在 `K/scratch/overnight-2026-09-05/logs/slides930/`（git-ignored）。**範圍照實寫**（模板規則 10；紅檢輪 2026-09-27 20:00–20:20Z、修正輪 20:28–20:50Z、API 欄位輪 20:50–21:00Z、09-28 狀態更新 06:30–06:57Z）：17 支腳本都有紅檢；每個竄改都查停下的**具名**理由，對照組綠。下面列的是 09-27 各輪；09-28 改過的五支腳本的紅檢在 §9（T1 12/12、tutorial 69/69、engineering 172/172、roadmap 5/5、F1 18/18），判官修正輪之後的在 §10，重新釘住之後的在 §11（engineering 181/181、F1 13/13、roadmap 5/5）；這裡的舊數字留作紀錄。
- 逐一停止條件看過紅（log `<腳本>-redcheck-<UTC>.log`；共用 helper `redcheck_common.py`）：T1 `make_coverage_0930.py`（11/11，`t1c-coverage-redcheck-r3-20260927T1943Z.log`；換上修正後的模組重跑相同，`t1c-coverage-redcheck-fixround-20260927T2054Z.log`）、M1 `make_sampling_error_fig.py`（6 個停止條件、7 個竄改，`m1-sampling-error-redcheck-r2b-20260927T1854Z.log`）、
  `make_tutorial_figs_0927.py`（59 個停止點 69/69、7 個到不了，`T2053Z`）、`make_engineering_figs.py`（118 個停止點：162 個竄改 162/162、3 個到不了、對照組 3/3，`T2053Z`）、`make_heartbeat_figs.py`（9/9，`T2000Z`）、
  `make_heartbeat_extra_figs.py`（圖底以外 12/12，`T2001Z`；圖底 `h0-footer-redcheck-20260927T1941Z.log`）、`make_arms_grid.py`（6/6，`T2001Z`）、`make_foreign_p4_diagram.py`（2/2，`T2005Z`）、`make_roadmap.py`（3/3，`T2002Z`）、
  `make_flow_api_matrix.py`（15/15，`T2003Z`）、`make_serve_s2_s4.py` 的 S3 日期停止條件（3/3，`make_serve_s2_s4-s3date-redcheck-20260927T2003Z.log`）；`make_serve_diagram.py` 只有一個合併停止條件（缺哪個錨點不說），5/5（`T2002Z`），維持原樣。
- 紅檢輪：`make_foreign_p4_diagram.py` 加了「07 檔沒有 pre-flight 段」的具名停止條件（之前是 TypeError，`…-20260927T2001Z.log`）；重跑 PNG 逐位元相同，所以沒重生，只改 `fig_a1_foreign_p4_path.md` 最後產出行的 sha（`8239f33506d018bd`）。
- 修正輪（coordinator 裁；探針找到的都修了）：`make_engineering_figs.py` → sha `834b7b0d74b46d0c`（Q4 的 compare 記錄規則；regex 取值、CI log 查找、T06 flowcache 列、`api_json()`／`table06()` 開檔都改成具名停止條件；06／01 檢查逐項給原因；squash 鏈印長度；REQ 兩條 suite 標籤要不同）、
  `make_tutorial_figs_0927.py` → sha `69fc08ebe8768a92`（GAP-1 §2 子表重複列或缺列就停）。兩支重跑，Q1–Q5、t1b、t1c 的 14 張 PNG 都與現有檔逐位元相同（`regen-check-fixround-20260927T2044Z.log`；用修正前的備份重跑也一樣，`regen-check-fixround-old-20260927T2036Z.log`），沒重生，只改七份圖 `.md` 的最後產出行。
  兩個 harness 同步改：行號對到新腳本、探針改成紅檢案例、舊版留在 `make_engineering_figs-redcheck.pre-fixround.py`、`make_tutorial_figs_0927-redcheck.pre-fixround.py`。
- API 欄位輪（coordinator 裁）：`make_engineering_figs.py` → sha `3c44f472b1ac2292`（API 快照載入時就檢查圖要讀的每個欄位；之前欄位改名是 `KeyError 'jobs'`，`make_engineering_figs-probe-json-field-20260927T2047Z.log`；`codes.txt` 每一行也檢查；9 個新竄改）、
  `make_tutorial_figs_0927.py` → sha `e6fd01ce00672507`（產生 t1b `.md` 時保留第三輪手改的第 10 行，最後產出行改成 UTC、標時區）。重跑：14 張 PNG 逐位元相同、產出的 t1b `.md` 除了最後產出行與現有檔逐行相同（`regen-check-fixround-20260927T2054Z.log`），沒重生，只改七份圖 `.md` 的最後產出行。harness 修正輪版留在 `make_engineering_figs-redcheck.fixround.py`。
- 還會以未具名例外停下的（rc≠0、不出圖；探針實測）：`make_tutorial_figs_0927.py`（T1 也 import）遇到表格列的格數少於它讀的那一欄（GAP-1 §4a／§4b、GAP-2／2b §1、GAP-ANALYSIS §6；§4a 與 GAP-2 是同一段程式、沒單獨探），或 T06 的 rc 欄不是整數（`make_tutorial_figs_0927-probe-remaining-20260927T2055Z.log`）。`make_engineering_figs.py` 不檢查 git 自己的輸出格式。其他腳本沒做這種探查。
- 變異自檢（先前輪次，本輪沒重跑）：F1 `make_fixed_since_916.py`（17/17，`mutation_check_fixed_since_916.r3b-20260927T1952Z.log`；拿掉位置停止條件時 6 個存活，`…without-placement-stop-20260927T1934Z.log`）、`o1-o2-t6-t9/run_mutations-r3-20260927T1948Z.log`（14/14）、
  `roles-flowapi-redcheck-20260927T1704Z.log`（12/12，worker）、`ndt-serve-s2s4-red-checks-r3-20260927T1948Z.log`（9/9）、`engineering-verdict-regex-redcheck-r2-20260927T1855Z.log`（PASS）、`cvd_layer_fills*`。
- 被取代、但留著的 log：
  - `make_engineering_figs-redcheck-20260927T2020Z.log`、`make_tutorial_figs_0927-redcheck-20260927T2008Z.log`：修正前的腳本（`2c82ff1b…`、`df2a3b9b…`）的紅檢，由兩份 `T2042Z` 取代；兩份 `T2042Z`（`834b7b0d…`、`69fc08eb…`）再由 API 欄位輪的兩份 `T2053Z` 取代。
  - `make_engineering_figs-redcheck-20260927T2041Z.log`：RED-CHECK FAIL 是 harness 自己的錯（`must_case` 的行號被換算了兩次，line map STALE），`T2042Z` 取代。
  - `regen-check-fixround-20260927T2035Z.log`（把 t1b `.md` 的一行差異算進了判定）、`regen-check-fixround-20260927T2036Z.log`（engineering 還是中間版 `897e5541…`），由 `…-20260927T2044Z.log` 取代；`…-20260927T2044Z.log` 與 `t1c-coverage-redcheck-fixround-20260927T2044Z.log`（修正輪的腳本）再由兩份 `…T2054Z.log` 取代。
  - `make_heartbeat_extra_figs-redcheck-20260927T2000Z.harness-bug.log`（harness 自己的錯）、`make_tutorial_figs_0927-redcheck-20260927T2006Z.log`（67/68，harness 預期字串錯，`T2008Z` 取代）。
- 第三輪最終重生的紀錄：`regen-r3-*.log`（見 §8）；第二輪 `regen-r2-20260927T1854Z.log`。
## 2. 頁序（32 頁，每頁一行；v1.7，2026-09-29）

| # | 頁 | form | 內容 |
|---|---|---|---|
| 1 | A0 | title | NDTwin progress · 2026-09-30 |
| 2 | B1 | table | 13 支 exercise：學生寫什麼、封包帶什麼、表由誰灌（模板 §2 B1 表；讀 tutorials `c80d83e` 與 GAP-1） |
| 3 | B2 | figure | basic：學生要寫的四塊（TODO）、一個封包穿過 parser → `ipv4_lpm` → `ipv4_forward` → deparser、pod 拓樸上 h1 → h3 的路、s1 的 5 條 entry（`fig_b2`，讀 tutorials `c80d83e`） |
| 4 | B3 | figure | basic_tunnel：`myTunnel` 標頭（0x1212）、parser 分支、`myTunnel_exact`；同一個目的 IP 帶不帶 tunnel 走到不同主機（`fig_b3`） |
| 5 | B4 | table | 09-16 的 NDTwin 缺什麼：九列「需求 → 當時的樣子 → 擋住了什麼」（模板 §2 B4 表；全部讀碼，`70615ec5` 上重核） |
| 6 | B5 | table | 怎麼補：九列「決定 → 機制 → 跑過 → 還沒」（模板 §2 B5 表） |
| 7 | T3 | figure | 外來 P4 程式怎麼在 NDTwin 上跑：七步＋執行中的元件（`fig_a1`）；09-29 起排在 B5 之後 |
| 8 | T1 | figure | NDTwin 涵蓋了什麼：09-16 列（916 那一列，灰底背景帶）對 09-27 列（RAN · JUDGED）＋T06 右兩欄（RAN IT／JUDGED）；四個判斷格 09-28 Adam 已裁定（不再有虛線）；flowcache 的 twin 格＝IPv4 only（與 T7 同字），twin 6／4／3＝GAP-2b 裁定後的彙總（`fig_t1c`） |
| 9 | T4 ○ | figure | multicast 從頭到尾，一支 exercise 的實例（`fig_t6`） |
| 10 | T5 | figure | pre-flight 檢查什麼，以及唯一的一次拒絕（`fig_t7`） |
| 11 | T6 ○ | figure | exercise 帶來什麼、convert 加了什麼（`fig_t8`） |
| 12 | T7 | figure | 七支自訂標頭 exercise 轉得動；twin 看過自己幀的只有 p4runtime（`fig_t9`） |
| 13 | R1 | table | 09-24 四條裁決 → 跑過／只離線或讀碼／還沒做（模板 §2 R1 表） |
| 14 | R2 | figure | roles.ipv4_route：從 package 到程式自己的表（`fig_r2`） |
| 15 | R3 | figure | live 07 跑兩次：L1–L6 全過；剪線時的掉包只記錄、不斷言（`fig_r3`） |
| 16 | R4 ○ | figure | 每台交換機回報的 capabilities：09-26 那次 07 的兩個 package 各一列（`fig_r4`；v1.8 起只畫最後狀態、圖上不印 sha） |
| 17 | H1 | figure | 為什麼 LLDP 在外來 P4 上不能跑（`fig_h0`） |
| 18 | H2 | figure | veth 心跳的架構（`fig_h0b`） |
| 19 | H3 | figure | 一次剪線、一次復原，量在 kernel 圖上：16.8 s／4.6 s（`fig_h1`） |
| 20 | H4 | figure | 偵測時間對剪線相位，7 次 live 剪線（4 點重疊處有放大圖）（`fig_h2`） |
| 21 | H5 | figure | 偵測上界拆開：16.8 s 實測、約 20 s 設計值（`fig_h3`） |
| 22 | H6 | figure | 心跳開著，26 臂的判定不變；17 個心跳 session、0 幀離開 host 埠（`fig_h4`） |
| 23 | D1 | figure | 執行期改規則：09-26 兩列新證據；09-16 前的兩列在灰底背景帶（`fig_d1`） |
| 24 | D2 | figure | 「queued」不等於「已裝上」，要讀回（P4 平面）（`fig_d2`） |
| 25 | S1 | figure | ndt serve 的請求路徑（`fig_s1`） |
| 26 | S2 ○ | figure | ndt serve 的威脅與防線（跑過／讀碼分開）；別人 claim 下的 up：碼裡 P4 與 OVS 都 rc 5，live 只有 P4（`fig_s2`；v1.8 起只畫最後狀態） |
| 27 | S3 | figure | 09-24 的兩條 guided walk；red→green 4 與 4（+4 fixture gap）（`fig_s3`） |
| 28 | S4 | table | 頁面往哪走：v1 → v2 → 與 Web-GUI 合一（模板 §2 S4 表） |
| 29 | M1 | figure | 兩條遙測路徑在同一 fabric 上的取樣誤差；帶外的點畫空心（`fig_m1`） |
| 30 | N1 | figure | 通往「帶自己的 .p4 來」的路線圖：cut 3 的 kernel 側已併、GUI 側在分支上；不含 external detect-only（`fig_n1`；釘在 `3368412d`；含它的版本存檔） |
| 31 | N2 | table | 要問教授的五題 |
| 32 | N3 | table | 我們不宣稱的七件事（09-29 拿掉兩列 CI；「使用者已經拿到」改寫成這份工作能不能到使用者手上） |

## 3. 每個數字的出處

縮寫：
- K＝`/home/adam/Desktop/NDTwin-Kernel`
- L＝`K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs`
- R＝`K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/runs`
- I＝`K/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926`

🟢＝跑過（live raw）；🟠＝讀碼、讀文件或讀 git（沒有執行）；（推）＝推論。
L、R、I 底下的東西都**沒有進 kernel trunk 的版控**，但本 deck 引用的幾乎都在 **audit-raw `797c34ab`**（依 coordinator 兩個 P4 repo 公開；integrator 17:2xZ 逐檔比 blob 相同），
09-19 早上三個 06 開發輪（052518Z、063235Z、083257Z）與它們的 arm report 在後代 **`5cf0364c`**（coordinator 以未認證 `git ls-remote` 核過兩邊公開；integrator 本機比對 81＋403 檔 blob 全同）。
**不在 audit-raw**：`2026-09-19T052251Z_05` 與 `FIXED-SINCE-916.md` §0 列名的幾份判官檔。**GAP-2b 09-28 裁定後提交為 `c8433963`**（08:19Z 起在公開 trunk 上）。
**每個 live run 都在髒 checkout 上跑**（`code <sha> +N`，+29～+95：F1 的修法證據最早 +29，其他頁 +47 起；各 `.md` 有逐 run 的數字）。行號與完整路徑見各圖的 `.md`。

### B 背景（2026-09-29 新；全部讀碼或讀文件，除了 B5 的 ran live 欄）
| 數字／主張 | 出處 | commit／binary |
|---|---|---|
| 13 支的標頭（0x1212、0x1234、0x812、IPv4 option、packet-in/out） | 🟠 各 solution `.p4`（`basic_tunnel.p4:7`、`advanced_tunnel.p4:7`、`calc.p4:62`、`source_routing.p4:8`、`link_monitor.p4:8`、`mri.p4:44`、`flowcache.p4:91`） | tutorials `c80d83e` |
| 誰由 runtime json 灌、誰自帶控制器、誰沒有 entry | 🟠 各 `topology.json`、`sN-runtime.json`、`solution/mycontroller.py`；GAP-1 §2b | 同上；`K/scratch/overnight-2026-09-05/logs/slides930/b-section-sources-20260929T0741Z.log`（B1 段） |
| B2、B3 圖上的每個名字、埠、entry、路徑 | 🟠 `git show c80d83e:exercises/basic…`、`…/basic_tunnel…`（錨點行號在兩張圖的 `.md`） | 產生器 `8497ac0b…`；紅檢 81/81 |
| 09-16 的 trunk＝`70615ec5` | 🟠 `git log --first-parent --until=2026-09-16T00:00:00Z trunk` | — |
| B4 九列 | 🟠 GAP-2 `:22-36`、`:45-58`、`:148-159`、`:219-240`、`:265-269`；PLAN-0917 `:11-13`、`:57-64`、`:108-109`；ANALYSIS `:26`、`:338`；`70615ec5` 上 `git grep` 重核（log 的 B4 段） | 讀 `1a284f75`／`70615ec5`／`057a01f0` |
| B5 決定 | 🟠 PLAN-0917 `:28`、`:121-132`、`:149-151`；ANALYSIS `:403-406`；TICKET-P1 `:57` | — |
| B5 機制已在 trunk | 🟠 `386eb20c`、`54f69d15`、`f282b895`、`b392f111`、`78067633`、`f5ad6890`、`5ce3bf74`、`572d9462`、`cafd518a`、`85bec430` 都是 `3368412d` 的祖先 | — |
| B5 ran live：13/13、9 支 entries 0 failed、group 1/1、四類拓樸、p4runtime／flowcache PASS、G1 10/13 | 🟢 T06 `00_table.tsv` 與 13 份解答臂報告 | `5dc7fc9a +95` |
| B5 ran live：16/16、proxy capabilities | 🟢 `L/2026-09-26T202055Z_07_roles_basic/21_proxy_roles_lines.txt:2`、`30_switch_state_roles.json`、`71_switch_state_plain.json` | `b2eeb71d +92` |
| B5 ran live：6/6 次剪線 | 🟢 `L/2026-09-26T152605Z_08_heartbeat/30_cycles.tsv`（`strict_20s` 全 yes，12.204–16.827 s） | `cafd518a +85` |

### A 開場（09-29 起 A1、A2 拿掉；下表留作紀錄）
| 數字 | 出處 | commit／binary |
|---|---|---|
| 09-08「not run」 | 🟠 `NDTWIN slide material 916/NDTwin-slide-template-916.md:257`（0/13 在 NDTwin fabric 上跑過） | 背景資料 |
| 各輪兩臂都照預期的支數：0、8、10、13、12、13、13、13、13、13 | 🟢 十個 `L/<UTC>_06_thirteen/00_table.tsv`，照 `live-p1/06_thirteen.sh:107-115`、`:142-155` 的規則重算 | 各輪 code：`dfb9d0d7 +47`、`cbc968d8 +54`、`7242e127`／`1ea07e7b +60`、`f3b6d09c +61`、`67b64869 +64`、`0c96c1d0 +79`、`580767a8 +83`、`cafd518a +88`、`3f8c2abf +91`、`5dc7fc9a +95` |
| 時間軸上的 11 個 merge／commit 日期 | 🟠 `git show -s --format=%cI <sha>`，換成 UTC | `fig_o1_since_0916.md` 的表 |
| 時間軸上的 7 次 run 時刻 | 🟢 run 目錄名的 UTC 時間戳 | 同上 |

### T P4 tutorial
| 數字 | 出處 | commit／binary |
|---|---|---|
| 能力計數 1／9／6（09-16）→ 8／6／2（09-27） | 🟠 `K/…/GAP-2-ndtwin-p4-capabilities.md` §1（`:39`）；`GAP-2b-…-2026-09-27.md` §1（`:105`；09-28 裁定後提交 `c8433963`） | GAP-2 讀的是 trunk `1a284f75`；GAP-2b 讀碼是 `7746832e` |
| read-only 兩格（meters、digest）、判斷格（registers、queue_metadata） | 🟠 GAP-2b §1 依據欄（腳本斷言） | 同上 |
| runs on NDTwin 13/13 | 🟢 T06 | `5dc7fc9a +95` |
| twin 看得到 6／只看過 IPv4 4／無證據 3 | 🟠 GAP-2b §3（裁定後 6／4／3；裁定前 7／3／3，flowcache 是 T1 腳本覆寫的）；flowcache＝IPv4 only（與 T7 同字）的 🟢 T06 raw：twin 的讀數 `R/2026-09-27T081256Z_flowcache_solution_ndtwin/link_usage/twin_integral.txt:3`（s1-eth3 約 31.8 Mbit）、`:7-9`（s3 全 0）；`netdev.before:7`→`netdev.after:7`（s1-eth3 3151 → 4596340 B）、`:3`→`:3`（s3-eth1 +273 B）；沒送達：`iperf_server.txt`（無報告列）、`iperf_client.txt:10` | 同上 |
| 每欄照預期的臂數：2、20、23、26、25、26、26、26、26、26 | 🟢 十個 `00_table.tsv` | 同 A |
| 每個 run 的心跳臂數：0（前 7 輪）、17、17、17 | 🟢 各 arm report 中的「heartbeat started (pid」 | `cafd518a`、`3f8c2abf`、`5dc7fc9a` |
| pre-flight 通過 21–25 項 | 🟢 T06 中 24 份 PASS 臂的 pre-flight 區塊；`L/2026-09-26T202055Z_07_roles_basic/12_preflight_basic_roles.txt`（25 項） | `5dc7fc9a +95`／`b2eeb71d +92` |
| multicast：convert 7 個檔 | 🟢 `R/2026-09-27T075305Z_multicast_solution_ndtwin.md:77` | `5dc7fc9a +95` |
| multicast：pre-flight 24 PASS、claim 45 m | 🟢 同檔，`:695` | 同上 |
| multicast：表項 4/4 | 🟢 同檔 `:198` | 同上 |
| multicast：group 1/1 | 🟢 同檔 `:332-336` | 同上 |
| multicast：PASS (6/6) | 🟢 同檔 `:589-594` | 同上 |
| multicast 骨架：PASS (2/2) | 🟢 `R/2026-09-27T075133Z_multicast_skeleton_ndtwin.md` | 同上 |
| basic_tunnel 骨架：9 個問題、rc 1（rc 1 只在講稿） | 🟢 `R/2026-09-27T075454Z_basic_tunnel_skeleton_ndtwin.md:113-119`、`:127`、`:239`、`:244` | 同上 |
| package 10 個檔（複製 8、新寫 2）；讀回 ok | 🟢 `R/2026-09-27T074826Z_basic_solution_ndtwin.md:78-89` | 同上 |
| 自帶控制器的 2/13 | 🟠 GAP-1 §2b；🟢 兩份 solution report | 同上 |
| 自訂標頭：7 支解答臂都 PASS | 🟢 T06 第 5、7、11、17、23、25、27 行 | 同上 |
| p4runtime 多出 14,000 B＝3,500 × 4 B | 🟢 `R/2026-09-27T081205Z_p4runtime_solution_ndtwin/link_usage/onpath.txt`、`iperf_client.txt:9`；推論部分寫在 `.md` | 同上 |
| 6 支還是 7 支 | 🟠 GAP-1 `:53-64`、GAP-ANALYSIS `:44,211-212` | GAP-1、GAP-ANALYSIS 在 `532b6c31` 已提交 |

### R 第一刀
| 數字 | 出處 | commit／binary |
|---|---|---|
| 四條裁決 | 🟠 `K/doc/audit/2026-09-24_p4-driven-api-shape/ANALYSIS.md:401-408` | 已提交 `46ef4813` |
| ① pass path：0 package entries、16/16 | 🟢 `L/2026-09-26T202055Z_07_roles_basic/12_preflight_basic_roles.txt:29`、`21_proxy_roles_lines.txt:2` | `b2eeb71d +92`、kernel `be70b5dd32356847` |
| ① 拒收只在離線 | 🟠 `tools/p4_exercise/tests/test_preflight.py:747`；變異 M-R4 `K/scratch/overnight-2026-09-05/logs/orchestrator-0924/rerun-R-177b9f03.mutate_roles_binding.log:34` | trunk `3d740be0` |
| ④ 另 6 支離線 PASS、4 支照設計 FAIL | 🟠 `K/scratch/overnight-2026-09-05/logs/orchestrator-0924/merged-R-572d9462.offline_5-3.log:1-37` | `572d9462` |
| convert 拿掉 16 條表項 | 🟢 `L/2026-09-26T202055Z_07_roles_basic/10_convert_roles.txt:6` | `b2eeb71d +92` |
| L1–L6 全 PASS（判定行 20／21 條） | 🟢 `K/scratch/…/orchestrator-0924/live-0925/07_roles_basic.log`、`I/live07/07.log` | `572d9462 +61`／`b2eeb71d +92` |
| pingall：12/12；剪線期間有掉包 8/12 → 3/12（只記錄）；恢復後 12/12 | 🟢 兩次 07 的 `32_`、`54_`、`61_` 檔 | 同上 |
| capabilities 各欄（R4 圖） | 🟢 09-26 那次 07 的 `30_`、`71_switch_state_*.json` | `b2eeb71d +92`、kernel `be70b5dd32356847` |

### H 心跳
| 數字 | 出處 | commit／binary |
|---|---|---|
| 16.827／4.623 s（cycle 3）；六次 12.204–16.827 s、4.623–5.099 s | 🟢 `L/2026-09-26T152605Z_08_heartbeat/30_cycles.tsv` | repo `cafd518a +85`、kernel `be70b5dd32356847`、helper `6a558fe452955de3` |
| H3：φ 0.017 s、16.607 s | 🟢 同目錄 `64_cycle.tsv` | 同上 |
| 14.972＋1.610＋0.245 | 🟢 同 `30_cycles.tsv` cycle 3；腳本斷言三段相加 | 同上 |
| ψ 1.474–1.755 s（H1 六次 1.493–1.755、H3 1.474） | 🟢 同上 `watchdog_phase_s` 欄與 `64_cycle.tsv` | 同上 |
| d 0.031–0.245 s | 🟢 同上，`pass_to_graph_s` 欄 | 同上 |
| 5 s、15 s、5 s、0x88B5 | 🟠 `p4_proxy/proxy_agent/topology_manager.py:373`、`:419`、`:422`；`tools/test_workflow/ndtwin-lab:715`、`:734` | trunk `3d740be0` |
| 相位鎖：20 次中 18 次 14.197–14.382 s＋cycle 1 的 13.275／13.298 s | 🟢 `K/doc/audit/2026-09-25_p4-heartbeat/spike/runs/2026-09-26T023021Z_S_heartbeat/20_cycles.tsv`、`…/2026-09-26T052148Z_S_heartbeat/20_cycles.tsv` | `4bc1201b +79`、`580767a8 +79` |
| 去相位：sweep 10.077–14.904 s、random 10.668–14.791 s | 🟢 `…/2026-09-26T085020Z_S_heartbeat/20_cycles.tsv`、`…/2026-09-26T085506Z_S_heartbeat/20_cycles.tsv` | `094f417f +84` |
| 改路後 pingall 12/12 | 🟢 `34_pingall_cut.txt` | `cafd518a +85` |
| 移開 4 條路由 | 🟢 `I/hbw-live/h14-20260926T152605Z.log:72` | `cafd518a +85` |
| `PASS 08_heartbeat`（H1–H4、H5） | 🟢 `I/hbw-live/h14-…log:190`、`h5b-…log:59` | `cafd518a +85`／`3f8c2abf +89` |
| 26/26 與參照相同 | 🟢 參照 `L/2026-09-24T185505Z_06_thirteen` 對 `…153300Z`、`…172913Z`、`…074635Z` 的 `00_table.tsv` | `0c96c1d0 +79` 對 `cafd518a +88`、`3f8c2abf +91`、`5dc7fc9a +95` |
| 17 個心跳 session、0 幀（1645 筆每秒輪詢，其中 running 1063 筆） | 🟢 `L/2026-09-26T172912Z_08_heartbeat/50_samples.tsv` | `3f8c2abf +89` |
| 1617 對 1645 | **已對帳**：判定在 17:56:10Z 印出，那時檔裡有 1617 筆；之後 01 期間又多了 28 筆（`fig_h4_forwarding_unchanged.md`） | 同上 |
| 「0」沒有 live 陽性對照 | 🟠 P4-HB-SPIKE.md §3.3（偵測器只在離線證過） | — |

### D 執行期改規則
| 數字 | 出處 | commit／binary |
|---|---|---|
| OVS D9／D11／D10：200 queued，讀回 130→131→130 | 🟢 `K/doc/audit/2026-09-02_manual-usertest/run-06-opus/logs/d9-d11-flow-mutation.log:5-29`（**09-03，背景帶**） | 公開快照 `9e6cc30`；kernel binary sha **沒有記錄** |
| 五元組 install／delete（proxy） | 🟢 `K/doc/audit/2026-08-24_five-tuple-live/five_tuple_live.txt:19-25`、`:46-52`（**08-24，背景帶**） | `e89fd4b`（`:2`；checkout 乾淨與否沒記錄，+N 不詳） |
| roles：queued、accepted_by_switch 1、讀回 10.0.9.9→OUTPUT:3、刪後不見 | 🟢 `L/2026-09-26T202055Z_07_roles_basic/40–45` | `b2eeb71d +92` |
| 沒 roles：queued → rejected_by_switch 1、501 unsupported_on_p4 | 🟢 同目錄 `74`、`75`、`76d`；`73_proxy_add.code`；`L/…152605Z_08_heartbeat/66_proxy_add.code` | `b2eeb71d +92`／`cafd518a +85` |
| 「queued」的意思 | 🟠 `K/doc/2026-01-02_ndt_api.md:1754-1758` | — |

### S ndt serve
| 數字 | 出處 | commit／binary |
|---|---|---|
| 127.0.0.1、8765、X-NDT-Token、600 s | 🟠 `tools/ndt_serve/serve.py:72`、`:1163`、`:73`、`:94` | trunk `3d740be0`（`tools/ndt_serve/` 在 `fed37cff` 相同） |
| 只有 1 個 listener | 🟢 `K/scratch/overnight-2026-09-05/logs/ndt-serve-0924/live-fixes-20260924T2249/01-listen-and-token.txt:2` | serve `c836cff0`；ndt checkout `fd7382a3 +60` |
| 403 host、403 token、409 busy | 🟢 同一 log 目錄的 `live-20260924T2201/api/04`、`03`、`10`，`live-fixes…/b/…` | `a139bceb`／`c836cff0` |
| P4 rc 5（live） | 🟢 `live-fixes…/a2/summary.json` | ndt blob `3273df8b` |
| OVS rc 5（碼裡；not run live） | 🟠 `tools/test_workflow/ndt:4362`（`68ace017` 加入）；`a/summary.json` 那一筆 rc 0 跑的是修法之前的 ndt，不上圖 | trunk `3368412d` |
| walk：6 條斷言、old 4 紅；9 條、old 4 紅＋4 fixture gap | 🟢 `live-cells-20260924T2224/walk-*/`（最後一次 GET 的 JSON）；fixture gap 由 PROVENANCE 解析 | serve `940c1233`、ndt `3273df8b` |
| walks 在 09-26 判 green（不在圖上） | 🟢 `I/walks/*.json` | — |
| v1／v2／合一（S4 表） | 🟠 `serve.py:84-86`、`:453-458`；`I/RULINGS-0927-ndtserve-gui-scope.md:16`；`I/RULINGS-0927-ndtserve-gui-v2.md:22-47`；`~/Web-GUI/package.json`、`docker-compose.yml:52-53` | `f186ce98`；v2 分支 `0d7f6ce8`→`f3a20447`→`6d5621ab`，沒有頁面檔 |
| 測試數（74、35、40、150/0）只放講稿 | 🟢 `I/gui/rerun-*.d09a4f17.log` | test merge `d09a4f17` |

### M 遙測
| 數字 | 出處 | commit／binary |
|---|---|---|
| cooperative 0.2953／0.0274／0.0154；link 0.0746／0.0344／0.0229；各條帶；2 M 帶頂 0.2853 | 🟢 `K/doc/audit/2026-09-19_telemetry-three-groups/raw/2026-09-19T115737Z_full/summary.json` 的 `sampling_error_by_group[*]["H-B1"].rates`（含 `position`） | kernel sha256 `be70b5dd3235…`；bmv2 `3ff54b5c1901…`——各序列自己那一代：`G2/cooperative_f64_a/arm.meta:12-15`、`G3/link_f64_a/arm.meta:12-15`（腳本斷言兩代相同）；code `4d3f294f +60` |
| link/coop 比值 0.253／1.255／1.489 | 🟢 同檔 `sampling_error_cross_group_registered`（腳本對帳） | 同上 |
| 組級判決 | 🟠 `FINDINGS.md:120-126` | 已提交 `611a08d3` |
| 0.2532%／0.5276%（只在講稿，說明量不出來） | 🟢 `…/raw/2026-09-19T130352Z_G2/G2/cooperative_f64_a.log:8`、`:15`、`:17`；arm 起跑 13:07:34Z（`cooperative_f64_a/arm.meta`） | kernel `be70b5dd…`（start＝end）、bmv2 `3ff54b5c…`；code `4d3f294f +60` |
| Adam 09-17 的要求 | 🟠 `K/…/PLAN-0917-exercise-support.md:149` | — |

### Q 工程（09-29 起整段拿掉；下表留作紀錄）
| 數字 | 出處 | commit／binary |
|---|---|---|
| 1557＋187 | 🟢 `K/scratch/…/intake-0925/rerun-REQ-851cefd7.summary.log:1-2` | `851cefd7` |
| 試跑：01 rc 0、06 26/26 | 🟢 `I/pb5-trial/JOURNAL.txt:4-7`；`L/2026-09-26T055148Z_06_thirteen` | `580767a8 +83` |
| 閘門 5/6 | 🟢 `I/pb5-merge/rerun-summary.ac0c3b64.txt:1-6` | `ac0c3b64` |
| 1658＋187、4 個 descriptor | 🟢 `I/pb5-merge/migrate.log:25-28`、`:135-139`、`:146` | `5dc7fc9a` |
| 驗收：01 PASS、06 26/26 | 🟢 `I/pb5-merge/live-accept.log:3`、`:6` | `5dc7fc9a +95` |
| CI：12 組、29 行相同（紅） | 🟢 `I/ci-36303713298-gcc.raw.log:6871`、`I/ci-36305829213-gcc.raw.log:6900`；`I/ci-compare-7746832e.txt:4` | Actions run id |
| Dependabot：兩個 high 以 fixed 關閉（2026-09-27 08:20:24Z／:25Z） | coordinator 以 gh api 已認證查核，不是公開 URL | — |
| ≥ 49 個判決（23／23／3），`logs/**/judge-*.md` 的 38 份判官檔，mtime ≤ 15:55Z（範圍外另有 `hunt-0911/fix/` 的 6 份） | 🟠 讀判官檔文字（逐檔表見 `fig_q2_review_path.md`；計數 log `K/scratch/…/logs/slides930/engineering-figs-run-20260927T1705Z.log`） | 快照 `fed37cff` |
| 58 個 merge、45 個點名判官（訊息全文；只看主旨 23） | 🟠 `git log --first-parent --merges --since=2026-09-16T00:00:00Z fed37cff`，逐個 `git log -1 --format=%B`（指令全文在 `fig_q2_review_path.md`；coordinator 另核 58／45） | 同上 |
| 103/103、183/0 | 🟢 `K/scratch/…/logs/gates-0910/mutate_p4_heartbeat_w.p4hbw-ebdf365e.log:213`、`:216` | `ebdf365e` |
| 1658 OK | 🟢 `I/hbw/rerun3-summary.7b600ab0.txt:1` | `7b600ab0` |
| Q3 表五列 | 🟠／🟢 `fig_q3_review_catches.md`「表格版」逐列 path:line | 各列 merge sha |
| L1 14→15→14→12→1→0 | 🟢 `I/ci-*-gcc.raw.log`、`slides930/ci-raw/ci-*-gcc.job*.raw.log`（PR #9–#17 的 18 次 GCC log，`MANIFEST.txt`；PR #15 較早 attempt 的 3 份在 `ci-raw/earlier/`）的 `L1 FAILED`／`L1 passed` 行（逐次列在 `fig_q4_ci_state.md`） | Actions run id |
| 四個 job 全綠：第一次是 ndtwin-lab trunk `8d622ea4` 的 run 36365963530（09-28 01:26Z）；第一個全綠的 PR 是 #12（01:38Z） | 🟢 未認證 GET（`engineering/_net/jobs_*.json`、`runs_*.json`，08:53Z） | — |
| `fed37cff` 的 CI run 36331119197：failure（09-27 不畫；09-28 起畫成只有公開 API 結果的一點） | 🟢 未認證 GET（`engineering/_net/jobs_36331119197.json`） | — |
| PR #6–#17 的 CI 符合預測（#15 是紅的 attempt 重跑綠之後） | 🟢 `I/ci-compare-pr6-48e8005d.txt`、`ci-compare-pr7.txt` … `ci-compare-pr17.txt`（`prediction met`） | — |
| main：兩個 repo 都是 `eef173a9`（#6 `ce6a9832` → … → #14 `be01cc7a` → #16 `9a74408b` → #15 `299c9e23` → #17 `eef173a9`）；ndtwin-lab 的 main 09-28 起跟著同步（CLAUDE.md `08f67b7a`，已公開、也已經 #17 進 main） | 🟢 未認證 GET 08:53:29Z（`engineering/_net/branch_*_main.json`、`pulls_Adam010341.json`）；`eef173a9` 的 tree＝`3368412d` 的 tree 去掉三個 `doc/audit/**/*.md`（本機唯讀） | — |
| trunk `3368412d`（兩個 repo） | 🟢 未認證 GET 08:38:26Z／08:38:27Z（F）、08:53:30Z（engineering）；之前 06:20Z／06:45Z 是 `85bec430` | — |

### F 修法（09-29 起拿掉；下表留作紀錄，N3 第 7 列仍引 `FIXED-SINCE-916.md` §8–§9）
| 數字 | 出處 | commit／binary |
|---|---|---|
| 39 已公開、0 只在本機、2 在審；66 個 merge＝39＋21＋6 | `FIXED-SINCE-916.md` §1、§4（腳本解析、並用 git 對帳） | 快照 trunk `3368412d` |
| 各層格數 2／6／5／28／0（含在審 2 格） | `FIXED-SINCE-916.md` §1、§2、§4 | 同上 |
| 27 格儀器／測試缺陷由 live run、CI、判官或閘門抓到 | `FIXED-SINCE-916.md` §2.4 末（誰抓到） | — |
| 手冊用的 P4-public 停在 `9e6cc307` | `FIXED-SINCE-916.md` §8–§9、`fixed-since-916/public-check-20260927.log`；09-28 06:20:07Z 與 08:38:41Z 再查同（`public-check-20260928/`、`public-check-20260928b/branch_P4-public_main.json`） | — |

### N 收尾
| 數字 | 出處 | commit／binary |
|---|---|---|
| cut 1、cut 2、cut 3 的 kernel 側已併 | 🟠 git：`572d9462`、`cafd518a`、`85bec430` 是 trunk `3368412d` 的祖先 | — |
| cut 3 的 GUI 側在分支上 | 🟠 git：`~/Web-GUI` 的 `draft/p4-capabilities-0924`（`65eecf6d`），不在 Web-GUI `main`、沒有 remote 分支含它 | — |
| 側表上限 1024 | 🟠 `K/include/ndt_core/collection/FlowLinkUsageCollector.hpp:747` | — |
| 事件驅動約 15.5 s | 推論；`I/judge-HBW-1a3ebd7f.md:73` | — |

## 4. 拿掉的頁與理由

| 候選 | 為什麼沒放 |
|---|---|
| pps 天花板比較圖（以及任何一對 pps 數字） | 這台機器量不出來：同臂同階爬梯時 0.2532%、確認時 0.5276%，門檻 0.5% 落在中間（raw `cooperative_f64_a.log:8`、`:15`）。只能說「量不出來」，所以不畫、不給倍數。 |
| 遙測 CPU 比較圖 | FINDINGS §4 的逐階時間窗有勘誤（`d39959ba`）。這一頁的題目是取樣誤差，CPU 不在其中。 |
| 「spike 偵測中位數約 14.3 s、10/10」的分布圖 | 那是相位鎖住的 report 層級數字（raw 見 H 表），已改用 kernel 層級的 H1／H3（H3、H4 頁）。 |
| 13×16 需求矩陣（`fig_t1b`） | 916 第 3 頁逐格相同，違反 delta only（判官 F-2）；T1 改用 `fig_t1c`。 |
| R1、S4、Q3 的卡片圖 | 狀態色塊與判語式標籤違反「只有圖或表、不寫判詞」（F-5、F-13）；改成表格頁，圖留存檔。 |
| ndt serve 的頁面截圖 | 頁面正依 v2 裁決重做，所以改畫架構圖（S1）。 |
| 「NDTwin 看得見 13 支的流量」 | 沒有證據。只有 p4runtime 的 0x1212 有 twin 看到自己幀的位元組證據（T7）。 |
| 獨立一頁講 protobuf 5 前後的效能 | 違反規則：切換前後的效能數字不同框。 |
| 權限缺陷的攻擊方式與位置 | 只寫「cleanup 路徑的權限缺陷，審查抓到，已修（#15）」；不描述機制。 |

| A1 `fig_o1_since_0916`、A2 `fig_o2_thirteen`（2026-09-29） | Adam 09-29：頭兩頁的逐日進度重複；教授不需要開發史。 |
| T2 `fig_t5_arms_by_run`（2026-09-29） | 每一次完整 run 一欄的逐輪史；最後結果在 T1、H6。 |
| Q1–Q5（2026-09-29） | 開發流程與 CI 史（protobuf 遷移步驟、改動怎麼進 trunk、審查抓到什麼、CI 逐次 run、main 的 squash 鏈）。 |
| F1 `fig_f1_fixed_since_916`（2026-09-29） | 修法看板＝除錯史。 |
| N3 的「CI green = checked on the lab」「CI stays green」兩列（2026-09-29） | 只因 Q 段而存在；「users already have these fixes」改寫成「users already have this work」（證據不變）。 |

○ 的 4 頁（T4、T6、R4、S2）有素材也有證據，砍不砍由 Adam 定（09-29 之前是 6 頁，T2、Q5 已拿掉）。

## 5. 沒驗到、或和 brief 不一樣的

- **2026-09-29**：`NDTwin_deck_930.pdf` 沒有重產（本機沒有 LibreOffice），仍是 09-28 的 36 頁版；pptx 是新的 32 頁版。新的表格頁沒有 render 過，高度是用字寬估的（模板 §1b）。
- **2026-09-29**：B4、B5 多了一列「link usage of its traffic」（遙測）——orchestrator 的列表沒有它，但 GAP-2 §3 第 1 條與 PLAN-0917 §8.2 都把它列為換程式之後最先失效的事，M1 也在比這兩條路；要拿掉只要在 §2 與產生器各刪一列。

- **09-24 那兩次完整 06 不是都 26/26。** 16:06Z 那次是 25/26（ecn），只有 18:55Z 那次是 26/26。第一個 26/26 是 09-19 14:43Z。
- **「10/10、中位數約 14.3 s、復原約 4.9 s」沒有用。** 那是 spike run 1–2 的相位鎖 report 層級值，改用 H1 的 kernel 層級值：12.2–16.8 s、4.6–5.1 s。
- **Adam 的裁決 A（接受約 20 s）、B（external 做 detect-only）、D（報告不新鮮就凍結）與 09-25 的對外說法**只記在 orchestrator 的記憶檔，repo 裡沒有原文。
- **T06 在 audit-raw `797c34ab`；09-19 早上三輪在 `5cf0364c`**。audit-raw 的公開性是 coordinator 查的（`5cf0364c` 以未認證 `git ls-remote`），integrator 只做了本機 blob 比對，**沒有自己打公開 URL**。
- **GAP-2b 四個判斷格 09-28 Adam 已裁定**（照建議值；flowcache 的 twin＝IPv4 only），我照裁定改了那四格、它們的六個標記，**以及 §3 的彙總行（7／3／3 → 6／4／3）——這一行不在「只改那幾格」之內**，不改的話 T1 腳本的計數對帳會停；coordinator 讀 diff 後提交為 `c8433963`（08:19Z 起在公開 trunk 上；內容 sha256 `77afc4d5…`＝本版讀的；裁定前 `0cf8a6d8…`）。T1、T7、N3 依賴它；T1 的虛線框已拿掉。
- **flowcache 在 T1 與 T7 已統一為「IPv4 only」**（第二輪，coordinator 更正第一輪的「no evidence」）：T06 的流只到了 s1→s3 那一段，沒有送達 h3；twin 在 s1-eth3 的讀數與 s3 的 0 都與介面計數器一致。若 Adam 要把「G1 PASS 但沒送達」另立一格，兩頁要一起改（新圖例項，不叫 no evidence）。
- **external 控制面的 detect-only 暫時拿掉**（N1 圖、N3 第 1 列）：分支未併；09-28 coordinator 確認併入前不放回；含它的 N1 存檔在 `next/fig_n1_roadmap_with_detect_only.*`，N3 舊的第 1 列是「NDTwin operates any foreign P4 | detect-only not merged; roles bind one dst-IP table | N1; route_binding.py:159-161」。
- **紅檢範圍**（見 §1、模板規則 10）：紅檢輪（2026-09-27 20:00–20:20Z）之後 17 支腳本都有紅檢；修正輪（20:28–20:50Z）與 API 欄位輪（20:50–21:00Z）把探針找到的問題改成具名停止條件。還會以未具名例外停下的輸入，逐條列在 §1（`make_tutorial_figs_0927.py` 的短表格列與非整數 rc；`make_engineering_figs.py` 不檢查 git 自己的輸出）；都是 rc≠0、不出圖。
- **Dependabot 關閉的證據**只有 coordinator 的已認證查核；我們用未認證方式查不到。
- **那一項已是一般的修法格**：PR #15 08:28Z squash 進 main（之後 #17 併入，兩個 main 08:53Z 都是 `eef173a9`），coordinator 裁定 D 解除中性磚規則；F1 上它是 proxy 層的 `rulings KJL`。只說「cleanup 路徑的權限缺陷，審查抓到，已修（#15）」，不描述機制。
- **sha 會過期**：Q3、Q4、Q5 釘在 trunk `3368412d`、main `eef173a9`、公開 API 08:53Z；F1、N1 釘在 trunk `3368412d`；圖上都標了 as-of。S4 表的 v2 分支 09-28 08:3xZ 重查仍是 `6d5621ab`、沒有頁面檔。09-29 晚上再跑一次（`slides930/regen-check-all.py` 會列出哪支腳本停、哪張圖會變）。
- **CI 的講法**：「PR #12–#14、#16、#17 與 ndtwin-lab trunk 從 `8d622ea4` 到 `3368412d` 的 run，四個 job 全綠（每個 run 的最後一次）；不是每一次都綠——一個不穩定的 shell 檢查（`test_apps_residue.sh`）讓 Adam010341 trunk `f253ed08` 的一次、PR #15 五次 GCC 裡的三次變紅，重跑後綠。」第一個全綠的 PR 是 #12；更早的全綠是 ndtwin-lab trunk `8d622ea4` 的 run（01:26Z）。`f253ed08` 的原因依 coordinator 查到的是同一個不穩定的檢查（那份 log 要認證，我沒讀）；PR #15 那三次紅的 log 我讀了（`slides930/ci-raw/earlier/`）。

- **worker 看到但不在這次範圍的 kernel 端小問題**：沒有修，列給 Adam。
  - `ndt up` 的收尾橫幅對外來 pipeline 一律印「installed no routes」，但同一次 run 的 proxy 寫了 16 of 16（`tools/test_workflow/ndt:4151-4157`）。
  - 07 腳本的 cut note 還寫「(c) does not hold」，已經過時。
  - `preflight.py:1239` 把多行 FAIL 算成「N check(s) failed」。
  - multicast arm report 第 27 行說用的是 `/usr/local/bin` 那顆 bmv2，但同一份報告第 24、183 行顯示是 bmv2-fast。
- **本輪寫入 kernel 樹**：git-ignored 的 `scratch/overnight-2026-09-05/logs/slides930/`（紅檢腳本與 log、重生紀錄）。brief 原說 kernel 只讀；這是 coordinator 轉達的 F-20 要求。09-28 另有 GAP-2b 那一次（Adam 裁定、coordinator 授權，見上）。
  第二輪 F1 變異 harness 的 log 同名覆寫了第一輪那份（新結果另存 `…r2-…`、`…r2b-…`）。

## 6. 判官 FIX 輪：每頁改了什麼（2026-09-27 UTC）

| 頁 | 改了什麼 | 判官項 |
|---|---|---|
| 全部 | 時間改 UTC；每份 `.md` 加髒 checkout 行（+N 與會改變行為的檔）；raw 狀態改引 audit-raw `797c34ab`（逐檔 blob 比過）；紅檢移到 `slides930/` | F-6、F-16、F-18、F-20 |
| A1 | 圖不變；`.md` 補 H1–H5 的 PASS log 行、髒 checkout、UTC | F-16、F-18 |
| A2 | 09-08 的點改成空心灰方塊「not run」、畫在 0 線下方；講稿「心跳開著的兩輪」→ 三輪 | F-7 |
| T1 | 換圖 `fig_t1c`：拿掉 916 的 13×16，只留兩列＋T06 右兩欄，分 READ THE CODE／RAN IT 面板；read-only 兩格交叉斜線；4 格虛線「pending review」；flowcache twin 格改 no evidence（G1 儀器缺陷），twin 計數 6／3／4 | F-2 |
| T2 | 圖不變；`.md` 補每欄 +N、audit-raw 收錄範圍 | F-16 |
| T3 | proxy 方塊裡的條列改成四個只有名字的小方塊 | F-21 |
| T5 | 拿掉 kicker「ONE REAL REFUSAL」、判詞「rc 1 · never brought up」與圖說；圖例改三色 PASS／INFO／FAIL；rc 1 移到講稿 | F-8 |
| T4、T6、T7 | 圖不變；`.md` 補 audit-raw、+95、UTC；講稿 T7 的 flowcache 說明改寫 | F-6、F-16 |
| R1 | 改表格頁（裁決 → 跑過／只離線或讀碼／還沒做）；① 只驗了 pass path、④ 只有 basic 跑過 live | F-5 |
| R2、R3 | 圖不變；`.md` 補髒 checkout、UTC | F-16、F-18 |
| R4 | 圖上 sha 標「· dirty」 | F-16 |
| H1、H2、H3、H5 | 圖不變；`.md` 補髒 checkout、audit-raw、UTC；H5 講稿 ψ 改 1.474–1.755（含 H3） | F-9、F-16、F-18 |
| H4 | H1 圓點、H3 方點分開；4 個重疊點加放大內嵌圖、各標值；相位鎖數字改引 raw（18 次＋2 次 cycle 1） | F-9 |
| H6 | 單位改「17 heartbeat sessions」；講稿補「0 沒有 live 陽性對照」 | F-10 |
| D1 | OVS（09-03）與自家 P4（08-24）兩列移進灰底「BEFORE 09-16 · BACKGROUND」帶、標日期、yes 改灰 | F-4 |
| D2 | 圖不變；`.md` 補 916 重疊說明（916 p26／28／32 是 OVS，這頁是 P4 平面） | 判官 D2 註 |
| S1 | 圖不變；`.md` 的 TMPDIR 修正改為已併 `fed37cff` | F-11 |
| S2 | 右面板標題加「(UTC)」；`.md` 補髒 checkout | F-16、F-18 |
| S3 | red→green 改「4 (+4 fixture gap)」；步驟縮成細帶；判定移出圖面；標題改「Live cells: two guided walks, 09-24」；講稿註明 cell 概念 916 已講 | F-12 |
| S4 | 改表格頁（stage／stack／served by／refresh／state），v2 狀態更新為「on a branch, no page yet」 | F-13 |
| M1 | 29.5% 改空心點、畫出帶頂 28.5% 並標值；`.md` 拿掉 pps 對比數字，0.2532%／0.5276% 改引 raw＋binary；腳本對 `position` 欄斷言 | F-14 |
| Q1 | CI 那一步改紅點、圖例「CI red (same 12 groups)」 | F-15 |
| Q2 | 判決計數規則改成不限行首：49＝23／23／3（38 份）；58 merges、45 點名判官；單一快照 `fed37cff`；標為讀（READ） | F-1、F-19 |
| Q3 | 改表格頁（catch／caught by／when／state） | F-13 |
| Q4、Q5 | 公開狀態重查（17:02:58Z）：沒有移動；`fed37cff` 的 CI 已完成 failure 記入 `.md` | F-18 |
| N1 | `.md` 裡轉述 ANALYSIS 裁決 4 的一句改寫成不帶投稿字眼的說法；UTC | 措辭掃描、F-18 |
| N3 | pps 列的證據改引 raw；flowcache 列改引 `iperf_client.txt :10` | F-14 |
| README | 檔案數 219、腳本 17 支（16 產生器＋1 模組）、圖 34 張；「ran／read」標示與模板一致 | F-17、F-19 |

| 頁 | 改了什麼 | 判官項 |
|---|---|---|
| F1 | 權限缺陷一律「cleanup 路徑的權限缺陷」；相關列改寫不指位置（第二輪起那一格也不標層、不計入層數，見 §7 第 1 項）；main＝`f9be5842`（內容含全部 32 格）；審查狀態更新（當時在審的三條皆 MERGE AFTER FIXES）；日期 UTC；「live 或 CI 先抓到」改為依抓到者分開 | F-3、F-18 |

## 7. 判官第二輪（`judge-SLIDES930-r2.md`，READY AFTER FIXES）：coordinator 的 18 項落在哪（2026-09-27 UTC）

T＝`NDTwin-slide-template-930.md`，R＝本檔，F＝`FIXED-SINCE-916.md`，P＝`figures/`。行號是 v1.2 的。

| # | 項目 | 做了什麼 | 落在 |
|---|---|---|---|
| 2 | 🔴 flowcache 的 twin 格 | T1 改成與 T7 同字「IPv4 only」（橘）、保留虛線待審框，twin 6／4／3；兩頁講稿都寫「T06 的流只到了 s1→s3，沒有送達 h3」；更正「流沒離開 s1」「GAP-2b 的綠用 09-26」；T1 腳本新增讀 twin 自己讀數的停止條件，歸零即停（紅檢 10/10） | P/p4-tutorials/make_coverage_0930.py:16、:67、:127；P/p4-tutorials/fig_t1c_ndtwin_coverage.md:20、:35、:43；P/p4-tutorials/fig_t9_custom_headers.md:32；T:133-134、:175、:404；R:113、:251 |
| 3 | audit-raw `5cf0364c` | 09-19 早上三輪與 arm report 改引 `5cf0364c`（本機 blob 比對 81＋403 檔全同） | T:29、:121；R:95；F:46；P/p4-tutorials/fig_t5_arms_by_run.md:64；P/overview/fig_o2_thirteen.md:38 |
| 4 | T1 的 09-16 列是背景 | 灰底背景帶，標「as shown 09-16; read 09-08, trunk 1a284f75」 | P/p4-tutorials/make_coverage_0930.py:161；T:15、:128 |
| 5 | Q3 第 3 列 | caught by 改 raw review（live run 自己判 PASS，`00_table.tsv:27`）；存檔卡片同步 | T:326、:332；P/engineering/fig_q3_review_catches.md:18；P/engineering/make_engineering_figs.py:811 |
| 6 | N3 的 flowcache 證據 | 改引 netdev（s3-eth1 +273 B）、`iperf_server.txt`、`iperf_client.txt:10` | T:384 |
| 7 | Q2 | 圖上標「READ · SINCE 09-16」「RAN IT · EXAMPLE」；「≥ 49」並寫明範圍只含 `logs/**/judge-*.md`；45＝訊息全文（主旨只有 23），重算指令寫進 `.md` | P/engineering/make_engineering_figs.py:684、:705、:715；P/engineering/fig_q2_review_path.md:31、:32；T:312、:316；R:202 |
| 8 | detect-only 拿下 N1、N3 | N1 重生不含那一步；原檔存成 `fig_n1_roadmap_with_detect_only.*`（`--with-detect-only` 可重生）；N3 第 1 列改字 | P/next/make_roadmap.py:42；P/next/fig_n1_roadmap.md:12；T:90、:192、:358、:380；R:252 |
| 9 | CVD 說法 | 更正為「有磚的四色 ≥ 14.6；最淺的兩個底色之間 6.6–6.8」；斜線那一格靠圖樣區分（斜線色對最接近的圖例底色 4.4–6.3，重算 log 已存） | T:44；P/fixed-since-916/fig_f1_fixed_since_916.md:67；`slides930/cvd_layer_fills-r2-20260927T1835Z.log` |
| 10 | 缺的紅 | M1 補「速率不是 2／20／100」與兩條 binary 停止條件；T1 補「GAP-2b 不寫 T06 路徑」「read-only 格移動」等；模板規則 10 改成照實寫範圍（7 支產生器沒有紅檢） | T:45；M1 的 `fig_m1_sampling_error.md`:72；P/p4-tutorials/fig_t1c_ndtwin_coverage.md:53；R:37、:253 |
| 11 | M1 的 binary | 改引各序列自己那一代的 arm.meta（G2、G3），腳本斷言兩代同一組 binary | M1 產生器 `make_sampling_error_fig.py`:46、:95；M1 的 `fig_m1_sampling_error.md`:21；T:296；R:185 |
| 12 | 裸 sha | A2 的各輪 code 帶 +N；08-24 那列寫明 checkout 乾淨與否沒記錄 | T:121-123、:253；P/flow-api/fig_d1_flow_api_matrix.md:31；R:165 |
| 13 | 規則 3 的標籤 | T1 twin 欄標 JUDGED；H1 底行標 RAN IT、兩個小圖標 READ THE CODE；H3 圖例「frame lost (inferred)」；T3 拿掉圖上跑出的數字；Q1 每步一個結果格 | P/p4-tutorials/make_coverage_0930.py:189；P/heartbeat/make_heartbeat_extra_figs.py:146、:179；P/heartbeat/make_heartbeat_figs.py:219；P/foreign-p4/make_foreign_p4_diagram.py:122、:178、:183；P/engineering/make_engineering_figs.py:568；T:133、:148、:214、:226、:305 |
| 14 | H6 揭露 | 09-26 17:55Z 的外來 2 Mbit/s iperf（F 的「5e no-lab」列）；175515Z flowcache 臂沒有加倍 | P/heartbeat/fig_h4_forwarding_unchanged.md:16；T:246 |
| 15 | 916 資料夾 | 沒動 | — |
| 16 | D1 | 灰底帶只蓋 RAN IT 格；READ 表標「trunk 3d740be0」；`.md` 的 audit-raw 說明更新 | P/flow-api/make_flow_api_matrix.py:193、:202；P/flow-api/fig_d1_flow_api_matrix.md:13、:46；T:253 |
| 17 | 重生＋sha | 改到的 10 支腳本全部重生（`slides930/regen-r2-20260927T1854Z.log`，rc 0）；34 份圖 `.md` 的「最後產出」行都寫 PNG 時間與產生器 sha256，並核過產圖之後腳本沒再改 | 每份 `P/*/fig_*.md` 末行；T:445 |
| 18 | 存檔的 fig_r1.md | detect-only 分支 tip 改為 `17e40e29` | P/roles/fig_r1_four_rulings.md:25 |

| # | 項目 | 做了什麼 | 落在 |
|---|---|---|---|
| 1 | 🔴 F1 的在審權限缺陷不可帶層別 | 那一格改成白底灰斜線的中性磚（任何圖例色塊都沒有斜線）、不在圖例裡、不計入任何層數；清單裡那一列放在中性標題「4.4 不標層」底下；§1 多一列「不標層 1」。腳本實際檢查的是：§1 的不標層數等於不標層底下的列數（第二輪）；以及（第三輪加）帶核定說法的列必須在不標層底下、不標層底下只能是它——這個位置檢查在數字對帳之前。變異 17/17（第三輪加的位置檢查，見 §8） | F:69（不標層那一列，第三輪移到 §1 表尾）、:158（§4.4 標題）；P/fixed-since-916/make_fixed_since_916.py（`NEUTRAL`、`APPROVED_PHRASE`、畫法）；P/fixed-since-916/fig_f1_fixed_since_916.md:52；T:43、:352 |

另外：GAP-2b 的內容雜湊記下來了（T:31、R:250）；程式註解裡最後三個 +08 日期（09-28）改成 UTC。

## 8. 判官第三輪（`judge-SLIDES930-r3.md`，READY AFTER FIXES）：落在哪（2026-09-27 UTC）

T＝模板、R＝本檔、F＝`FIXED-SINCE-916.md`、P＝`figures/`、S＝`K/scratch/overnight-2026-09-05/logs/slides930/`。行號是本版的。（之後兩支腳本的行號動過：`make_foreign_p4_diagram.py` 紅檢輪在 :84 加了兩行，本節的 :143 現在是 :145；`make_engineering_figs.py` 修正輪與 API 欄位輪改了多處，本節的 :533 現在是 :636。）

| # | 項目 | 做了什麼 | 落在 |
|---|---|---|---|
| 5 | 🔴 H1 圖底 | 改用 09-24（心跳之前）的 up log 與同次 switch_state，畫布標「RAN IT · 09-24, before the heartbeat」；新停止條件：清單列 `link_watchdog` 時同一個 switch_state 的心跳 watchdog 不得在跑（5 個竄改的紅） | P/heartbeat/make_heartbeat_extra_figs.py:137；P/heartbeat/fig_h0_why_not_lldp.md:21；T:214；S/h0-footer-redcheck.py、`h0-footer-redcheck-20260927T1941Z.log` |
| 6 | 🔴 T1 圖例 | 改成「cannot · read only」；斷言 read-only 格都是做不到（新紅：`meters` 改部分且計數同步），T1 紅檢 11/11 | P/p4-tutorials/make_coverage_0930.py:122、:214；S/t1c-coverage-redcheck-r3-20260927T1943Z.log；T:130-131 |
| 8 | Q2 的截止數與最後一跑 | 截止之後的判官檔：18:54Z 時 4 份、本輪 8 份；最後一跑改指 `regen-r3` | T:315；P/engineering/fig_q2_review_path.md:19、:117；P/engineering/fig_q3_review_catches.md:89 |
| 9 | overview 的 docstring | 改成 `5cf0364c`；o1／o2／t6–t9 自檢重跑 14/14 | P/overview/make_overview_figs.py:30；S/o1-o2-t6-t9/run_mutations-r3-20260927T1948Z.log |
| 10 | 紅檢範圍 | 把 `make_tutorial_figs_0927.py` 列進沒有紅檢的，共 8 支；H1 圖底、F1 位置、T1 新停止條件另列 | T:45-54；R:37-42 |
| 11 | 小字 | R:13 v1.2；R:224 拿掉 cut 2b；o1 的 telemetry 補 G2–G6 `4d3f294f`；`make_heartbeat_figs.py` docstring 改 `797c34ab`；Q3 四種抓法；t1b 拿掉「已知的儀器缺陷」；H6 的 +8.6% 寫明基準（T06 同一臂 4,361,273 B）；T:16 背景帶規則改寫；+N 範圍改 +29 起；flowcache 補 s1-eth3↔s3 那條線（tutorials `topology.json:48-51`） | R:13、:224、:97；P/overview/fig_o1_since_0916.md:65；P/heartbeat/make_heartbeat_figs.py:15；P/engineering/fig_q3_review_catches.md:71-72、:80；P/p4-tutorials/fig_t1b_requirements_matrix_0927.md:10；T:248；P/heartbeat/fig_h4_forwarding_unchanged.md:19；T:16、:32；T:134；P/p4-tutorials/fig_t1c_ndtwin_coverage.md:21；P/p4-tutorials/fig_t9_custom_headers.md:32 |
| 12 | 設計點（coordinator 裁） | S3 的 09-10／09-11 old／new 列進 09-16 前背景帶（加日期停止條件）；T1 的 09-27 列標「RAN · JUDGED」；H4 的色帶與 20 s 線標「design bound (derived)」；T3 與 Q1 分標跑出來的與讀出來的 | P/ndt-serve/make_serve_s2_s4.py:593；P/p4-tutorials/make_coverage_0930.py（09-27 列標題）；P/heartbeat/make_heartbeat_figs.py:255、:258；P/foreign-p4/make_foreign_p4_diagram.py:143；P/engineering/make_engineering_figs.py:533；T:130、:150、:230、:277、:307 |

| # | 項目 | 做了什麼 | 落在 |
|---|---|---|---|
| 1 | 🔴 R 第 7 節第 1 列引用了單一層的 §1 列 | 改成只引不標層那一列與 §4.4 標題；「兩條對帳」的說法改成腳本實際檢查的內容 | R:304 |
| 2 | 🔴 Q3 `.md` 把 (e) 的抓法連到在審那條分支 | 刪掉那一句 | P/engineering/fig_q3_review_catches.md（原 :80） |
| 3 | 🔴 F 裡在審那一列帶了會讓人聯想到層別的字 | 刪掉那一句；harness 的 M11 不再寫任何層名：改成從產生器的常數逐一取五個層、輸出只印編號 | F:164；S/mutation_check_fixed_since_916.py；P/fixed-since-916/fig_f1_fixed_since_916.md:33-38 |
| 4 | 🔴 中性位置沒有真的被檢查 | 產生器加位置停止條件（帶核定說法的列必須在不標層底下、不標層底下只能是它，先於數字對帳）；新變異 M11.1–M11.5（那一列搬回每個層標題、§1 同步改好）與 M12（另一列放進不標層、§1 改好），都停在新的理由；拿掉這個停止條件時 6 個都存活 | P/fixed-since-916/make_fixed_since_916.py:100、:215；S/mutation_check_fixed_since_916.r3b-20260927T1952Z.log、`…without-placement-stop-20260927T1934Z.log`；R:304 |
| 7 | clang／TSan 的狀態 | 快照之後判官 MERGE、19:03Z 併入 trunk `18c83aba`、19:24Z 經 PR #9 進 main `bad4cc7a`；其他在審的都寫「截至 2026-09-27 19:37Z」與目前 tip | F:144、:150、:156、:164；T:342、:357；R:217；P/fixed-since-916/fig_f1_fixed_since_916.md（已知但書第 2 條） |

另外：為了讓在審那一項附近不出現任何層別字，把模板的 guard 清單、F1 講稿、F1 `.md` 的「圖怎麼讀」與色盲那一段重新排序或改寫（內容不變），並把 F 的不標層那一列移到 §1 表尾。
第三輪最終重生：`S/regen-r3-20260927T1951Z.log`（9 支腳本 rc 0，各附 sha256）；每份圖 `.md` 的「最後產出」行已更新。

## 9. 09-28 狀態更新（2026-09-28 06:09–07:2xZ UTC）

S＝`K/scratch/overnight-2026-09-05/logs/slides930`。起因：coordinator 要把 09-27 21:0xZ 之後的新狀態帶進 deck；Adam 同日裁定 GAP-2b 四格、detect-only 維持不上、ndtwin-lab 的 main 改為跟著同步。

**狀態點**：trunk `85bec430`（本機 git 唯讀）、公開 API 2026-09-28 06:45:52Z（未認證，每次請求逐行在 `S/net-refresh-20260928T0616Z.log`；3 次 HTTP 000 已重試；另有一次沒記進 log 的診斷 GET，log 裡有註記）。
之後本機 trunk 又往前走了（其中有 `08f67b7a`，06:41Z，CLAUDE.md 的新 main 規則；`c8433963`，07:15Z，GAP-2b）；08:19Z 未認證查，兩個公開 trunk 都是 `3368412d`。圖不追這幾顆，釘在 `85bec430`，圖上標 as-of。

**改了的圖**（PNG sha256 前 16 碼，300 dpi／`_hires` 500 dpi；舊→新）：

| 圖 | 300 dpi | 500 dpi | 為什麼 |
|---|---|---|---|
| Q4 `fig_q4_ci_state` | `27d8597c6d2ea1f1`→`db0293eebabf0354` | `8da45aa6122b1dd9`→`d3cb598c69771f79` | 48 次 run（新增 PR #9–#14 的 GCC log 與 8 次只有 API 結果的 ndtwin-lab trunk run）；L1 到 0、四個 job 全綠；as-of |
| Q5 `fig_q5_main_by_pr` | `9161c3bf1dd1cd8e`→`649f31a762f283e2` | `207e14477cb0e367`→`3599e616af5916e5` | #6–#14；ndtwin-lab main 標 follows（新規則）；as-of |
| F1 `fig_f1_fixed_since_916` | `88c8d98b0f1f8902`→`df361f53c369dfa3` | `38bb99920572e373`→`74c367a931eeb21a` | 32／0／4 → 37／0／2；as-of |
| N1 `fig_n1_roadmap` | `debaf06e892f5439`→`db11947bf74e338f` | `8f33e9f7d8ee6746`→`4a9190d6aa7c55fa` | cut 3 分成 kernel 側（已併 `85bec430`）與 GUI 側（Web-GUI 分支）；原腳本在「分支已併」停下；as-of |
| N1 存檔 `…_with_detect_only` | `9a84657b807cc184`→`9b08e87556d8c95d` | `15aa6c4991a7c80e`→`b4d7c6d6bdf6b931` | 同上（不上 deck） |
| T1 `fig_t1c_ndtwin_coverage` | `3c8de362213d95e2`→`651617dc8e6572fc` | `63636da8767e1522`→`42824ea5a68d842d` | 四格裁定：虛線框拿掉、圖例拿掉「pending review」；twin 6／4／3 直接來自 GAP-2b；as-of |
| t1b 存檔 `fig_t1b_requirements_matrix_0927` | `c5b1d03a9af01867`→`d10e52ed940f539a` | `de16cda248ab1c4c`→`08552d2dd5510665` | 同一個裁定（flowcache 的 twin 格變 IPv4 only）；不上 deck、**沒有 as-of** |

其他 56 個 PNG（28 張圖）逐位元不變：`S/regen-check-all-20260928T0736Z.log`（全部文字改完之後的最後一次；17 支腳本在暫存副本重跑，共 18 次：70 個 PNG 與本資料夾相同、0 個停、真的圖資料夾沒被動、沒有 `__pycache__`）。`…T0714Z.log` 是改文字之前的同一個普查，結果相同；`…T0729Z／T0731Z／T0733Z.log` 只跑 F1。
重生進本資料夾的紀錄 `S/regen-refresh-20260928T0658Z.log`（每支 rc 0）；前後的 PNG 清單 `S/png-sha-before-refresh-0928.txt`、`S/png-sha-after-regen-0928.txt`。Q1–Q3 的 PNG 被同一次重生重寫、內容相同（檔案時間變了）；PDF／SVG 沒有逐位元比。

**改了的腳本**（sha256 前 16 碼，舊→新）：`make_engineering_figs.py` `3c44f472…`→`468618f9…`；`make_fixed_since_916.py` `00cfcf63…`→`6ebcf0cc…`；`make_roadmap.py` `d6133ee0…`→`595aab61…`；
`make_coverage_0930.py` `2ac46740…`→`703bd7cb…`；`make_tutorial_figs_0927.py` `e6fd01ce…`→`2fb26471…`。改前的版本都在 `S/refresh-0928-bak/`。

**紅檢（09-28 更新當時；之後的見 §10）**：engineering `S/make_engineering_figs-redcheck-20260928T0649Z.log`（判官修正輪由 `T0809Z` 取代）（127 個停止點：124 個看過紅、3 個到不了；172 個竄改 172/172；對照組 3/3）；
roadmap `…-redcheck-20260928T0640Z.log`（5/5）；F1 `mutation_check_fixed_since_916.refresh-20260928T0634Z.log`（18/18，新增 M13）；T1 `t1c-coverage-redcheck-ruling-20260928T0654Z.log`（12/12，新案例：裁定格移動、還有「(judgement)」、flowcache 的 twin 不是 IPv4 only）；
tutorial `make_tutorial_figs_0927-redcheck-20260928T0656Z.log`（69/69，7 個到不了）。

**被取代、但留著的 log**（09-28）：
- `make_engineering_figs-redcheck-20260928T0637Z.log`（FAIL：line map 在 287 過期，24 個停在別的理由；腳本是中間版 `54f5a438…`）、`…T0640Z.log`（FAIL：fig_q3 加了兩行註解後 line map 差 2，竄改本身 172/172 紅；中間版 `db3927e9…`）、
  `…T0643Z.log`（PASS，但腳本是改 main 規則之前的中間版 `db3927e9…`）、`…T0647Z.log`（FAIL：1 個 SURVIVED——1233a。兩次跑的是同一支產生器 `468618f9`；判官的判讀：那一版 harness 沒把竄改送到、或沒計分，不是產生器的洞；那一版 harness 沒另存。07:28Z 對現行產生器直接跑三個變體，三個都停在具名理由（`S/probe-1233a-main-variants-20260928T0728Z.log`）；判官修正輪起，覆蓋是 harness 的三個案例 1185（只改 ndtwin-lab main）、1185b（只改 Adam010341 main，新加）、1233a（兩個都改），三個都要求產生器讀到的是竄改後的位元組才算紅（見 §10，`T0809Z`）。）
- `make_roadmap-redcheck-20260928T0634Z.log`（5/5，中間版 `f69979a5…`；`T0640Z` 取代）。
- `make_tutorial_figs_0927-redcheck-20260928T0655Z.log`（68/69：harness 的彙總案例還用裁定前的 7／3／3；`T0656Z` 取代）。
- `regen-check-all-20260928T0609Z.log`（更新前的普查：F1 停在找不到 `FIXED-SINCE-916.md`——是 harness 的暫存目錄少一層，已改，改前版本 `regen-check-all.pre-f1path.py`；N1 兩次停在「分支已併」）。
- 09-27 的 `t1c-coverage-redcheck-r3-…`／`…fixround-…` 由 `…ruling-20260928T0654Z.log` 取代；`mutation_check_fixed_since_916.r3b-…` 由 `….refresh-20260928T0634Z.log` 取代。

**`FIXED-SINCE-916.md` §0 的更正（07:3xZ）**：「`J25/`、`J26/` 下本檔引用的判決檔都已進 audit-raw」在 09-28 版不成立——新加的列引用的 7 份判決檔不在 `797c34ab`、也不在本機 audit-raw 最新的 `5cf0364c`（逐檔 `git cat-file -e`），已逐一列出。改完（連同下一段的用字）F1 重跑：`S/mutation_check_fixed_since_916.refresh-fixed0c-20260928T0733Z.log`（18/18）、`S/regen-check-all-20260928T0733Z.log`（F1 兩個 PNG 相同）；中間兩次 `…refresh-fixed0-20260928T0729Z.log`、`…refresh-fixed0b-20260928T0731Z.log` 與 `regen-check-all-20260928T0729Z.log`、`…T0731Z.log` 是同一檔較早的改法，被取代（結果相同）。

另外：09-28 07:3xZ 為了排版又挪了幾處文字（內容沒改）；判官修正輪用新的字表重做，見 §10。

**文字**：模板（版本行、規則 3 的 GAP-2b、規則 8 的 CI guard、規則 10、T1、R1 ③、R4、S4、Q1 的 CI 註記、Q3 第 1 列、Q4、Q5、F1、N1、N3 第 6、7 列、§3、§4）；本檔 §1–§5 與本節；`FIXED-SINCE-916.md` 重寫到 `85bec430`；
改了的圖的 `.md`，以及引用 GAP-2b「未提交」的 t5、t6、o1、q3、n1 `.md`。N3 第 6 列原本是「CI is green」，09-28 起不成立，改成 CI 綠的範圍（舊列在模板 N3 講稿）；這是內容改動，要不要留由 Adam 定。

**沒驗到**：
- Adam010341 trunk `f253ed08` 那一次 GCC 失敗（ndtwin-lab 同一顆 sha 通過）——沒拿到 log（要認證）；判官修正輪時 coordinator 轉告原因是不穩定的 `test_apps_residue.sh`（§10）。
- 新 main 規則的 CLAUDE.md `08f67b7a` 我讀的時候只在本機 trunk；GAP-2b 的 `c8433963` 公開與否當時沒查（判官修正輪查了：公開，§10）。
- 本資料夾在公開 repo 的工作樹裡：仍全部 untracked，`git diff --cached` 為空（07:2xZ）。

## 10. 判官修正輪（2026-09-28 08:0x–08:3xZ UTC；判官 READY AFTER FIXES，coordinator 轉來八項與四個裁定）

S＝`K/scratch/overnight-2026-09-05/logs/slides930`。這一輪只有 Q4 重畫；其他全是文字。

**Q4 重畫（第 8 項）**：PR 的點標「PR #11」「PR #12」（原本是 PR 分支的 commit）；8 次沒有 GCC log 的 trunk run 由直寫的「no log」改成短豎線，圖例只寫一次「no log」。
- PNG：300 dpi `db0293eebabf0354`→`b83fffcb53bc27a8`；500 dpi `d3cb598c69771f79`→`7475c6ebd52b12ad`。重生紀錄 `S/regen-judgefix-q4-20260928T0810Z.log`（rc 0；Q1、Q2、Q3、Q5 的 PNG 同一次重生逐位元不變）。
- 產生器 `make_engineering_figs.py` `468618f9…`→`6f26e0ad…`：新停止條件——PR 的分支在 pulls 快照裡找不到，就不標、停下。
- 紅檢 `S/make_engineering_figs-redcheck-20260928T0809Z.log`：128 個停止點，125 個看過紅、3 個到不了；174 個竄改 174/174；對照組 4/4（新的 ctl-q4l 斷言兩個 PR 點的標籤）；harness 自檢 4/4。
  第 6 項也在這一跑：1185（只改 ndtwin-lab main）、1185b（只改 Adam010341 main，新加）、1233a（兩個都改）三個案例都要求產生器讀到的是竄改後的位元組才算紅（`must_read`：包住產生器的 `api_json()`，逐檔比對讀到的 sha256）；
  新自檢 S-read 證明這個檢查會擋（名字對、但讀到的不是竄改的那個檔 → 不算紅）。`…T0808Z.log` 是加 S-read 之前的同一跑（3/3 自檢，其餘相同），被取代。
- 全部 PNG 的普查：見本節末。

**第 3 項（清單 §0 的 audit-raw）**：`S/audit-raw-check.py` 把清單引用的每一個 `J25/`、`J26/` 路徑（判決檔、rerun 摘要、INTAKE）、其他 scratch log 與 live run 目錄逐一 `git cat-file -e`，對 `797c34ab` 與 `5cf0364c`。
兩個都沒有的 25 項逐一寫進清單 §0；`J26/qn1/` 是一份判決檔加一份 `INTAKE.md`。log：`…-20260928T0821Z.log`（清單 §0 引用的那份）、`…-20260928T0826Z.log`（清單最後一次改完之後，逐檔結果與 T0821Z 相同）；`…T0815Z.log` 還沒有 live run 目錄，被取代。

**第 5 項**：F1 在清單最後一次改完之後重跑，`S/mutation_check_fixed_since_916.judgefix-20260928T0826Z.log`（18/18；檔頭記產生器 `6ebcf0cc…`、harness `eef110fd…`、清單 `3be0d968…` 的 sha256，檔尾 `rc=0`）；harness 改前的版本在 `S/judge-fix-0928-bak/`。

**第 7 項**：模板版本行寫清每張圖釘在哪（Q4、Q5：`85bec430`＋公開 API 06:45Z；F1：`85bec430`＋06:20Z 公開查核；N1：`85bec430`，commit 時間 03:41Z；T1：GAP-2b `c8433963` 那一版）。

**第 4 項**：模板 F1 講稿「09-28 新併的 5 格」改成「`fed37cff` 之後新併的 5 格」。

**公開查核（coordinator 要的，08:19Z，未認證）**：`S/net-judgefix-20260928T0819Z.log`（API 六次請求＋不帶任何 git 設定的 `git ls-remote`），回應存在 `S/public-check-judgefix-20260928T0819Z/`。
- 兩個 repo 的 trunk 都是 `3368412d`（committer 07:45:54Z）。
- `compare/c8433963...trunk` 兩邊都是 `ahead`、`behind_by 0`、merge base＝`c8433963` ⇒ GAP-2b 那一顆已公開。
- main：Adam010341 是 `9a74408b`（committer 08:19:30Z），ndtwin-lab 還是 `be01cc7a` ⇒ 08:19:35Z 時兩個 main 還沒同步；我沒有去看那一顆的內容。
- 圖與清單都照舊釘在 `85bec430`；TERM trap 那條 08:19Z 已在公開 trunk 上、不在 main 上，清單在釘住的那一點仍把它算在審。

**第 2 項（CI 的講法）**：模板規則 8、Q1 註記、Q4 講稿、§3，本檔 §2、§5 都改成有界的說法；N3 第 6 列縮成「名字 → 值」，另加第 6b 列（CI 不是一直綠；一個不穩定的 shell 檢查，修法在進行）。`f253ed08` 的原因照 coordinator 轉告寫（那份 log 要認證，我沒讀）。

**沒動的**：存檔的 `fig_q3_review_catches.png`（不上 deck）卡片上還是「fix in progress」；Q3、N3 的投影片表與講稿已改成新說法。

**普查與掃描**：判官修正輪結束時的普查 `S/regen-check-all-20260928T0828Z.log`（70 個 PNG 相同、0 個停）；逐行掃描 `S/proximity-scan-20260928T0827Z.log`（錨點 62、命中 14，全部只是 repository／組織名稱，標 JUSTIFIED；`…T0812Z`、`…T0822Z`、`…T0824Z` 是改之前或掃描器還在調的幾跑，被取代）。重新釘住之後掃描停做（coordinator，見 §11）。

下面三段各自與前後隔兩行，因為它們提到在審那一項。

- **第 1 項（在審那一項前後兩行）**：字表照 coordinator 的裁定 A，寫在 `S/proximity-scan.py`；範圍是模板、本檔、清單與每一份圖 `.md`。錨點是提到這一項（名稱、分支、判決檔、sha）或提到在審狀態與數目的每一行。
  改法：模板規則 8 拆開，CI 與核定說法各自一段；Q3、N3 兩張投影片表把那一列放成單獨一塊（兩塊之間空兩行）；F1 講稿、§3 的在審數目各自一段；本檔 §2 的 F1 列不再寫在審數，§3、§4、§6、§7、§8 的那一列各自一塊；
  清單 §0、§1、§4、§8、§10 分塊或空行；fig_q3 與 fig_f1 的 `.md` 分塊、改序。剩下的命中只有 repository 或組織名稱（`ndtwin-lab`、`NDTwin-Kernel`），掃描器逐行標成 JUSTIFIED 並寫理由。

- **裁定 B**：在審那一項當時只用一個說法（重新釘住之後改成「已修（#15）」，§11）；沒有換成別的狀態說法。英文表格當時用「fix in review」。

- **裁定 C、D**：在審的那個 PR 不寫編號（N3 第 6b 列與 CI 講法只說「一個在審的 PR」）。中性磚規則要等 coordinator 說那個 PR 已 squash 進 main、兩個 main 都同步之後才解除；這一輪沒動。

## 11. 重新釘住（2026-09-28 08:3x–09:0xZ UTC）

S＝`K/scratch/overnight-2026-09-05/logs/slides930`。起因：coordinator 08:2x 轉告在審那一項的 PR #15 已 squash 進 main、兩個 main 同步，裁定 D 解除中性磚規則，並要我照先前的提議重新釘住一次；
之後 PR #17（只改 CLAUDE.md）也併入，改釘到 main `eef173a9`＋trunk `3368412d`。同時：鄰近字的掃描（第 1 項、裁定 A）停做；那一項照一般修法格畫在它的層，只用一句不含機制的說法；不引用那一項的判官紀錄；不寫任何「還有後續」的暗示。

**公開查核（未認證）**：`S/net-repin-20260928T0831Z.log`（08:31:56–08:38:49Z）與 `S/net-repin2-20260928T0853Z.log`（08:53:29–08:56:01Z）。
兩個 trunk 都是 `3368412d`；兩個 main 08:32Z 是 `299c9e23`（#17 開著）、08:53Z 是 `eef173a9`（#6–#17 都已併、沒有開著的）；P4-public 仍是 `9e6cc307`。回應在 `figures/engineering/_net/`（前兩份移到 `_net/prev-20260928T0645Z/`、`prev-20260928T0832Z/`）與 `figures/fixed-since-916/public-check-20260928b/`。

**改了的圖**（PNG sha256 前 16 碼，300 dpi／500 dpi；判官修正輪之後 → 現在）：

| 圖 | 300 dpi | 500 dpi | 為什麼 |
|---|---|---|---|
| Q3 存檔 `fig_q3_review_catches` | `0a3edc21981718bc`→`1b4607ee0068123b` | `4627ab002cfd47de`→`d7c04ffe70d8d685` | 第一張卡改成 fixed · merged（綠） |
| Q4 `fig_q4_ci_state` | `b83fffcb53bc27a8`→`aadbb90594fea77f` | `7475c6ebd52b12ad`→`0a6e0f1e3c3afaae` | 56 次 run（加 PR #15–#17、兩次 trunk run）；紅圈＝較早 attempt 紅；as-of 08:53Z |
| Q5 `fig_q5_main_by_pr` | `649f31a762f283e2`→`2221e0486072e7ef` | `3599e616af5916e5`→`1815a874f13531b3` | main `eef173a9`、#6–#17 |
| F1 `fig_f1_fixed_since_916` | `df361f53c369dfa3`→`97ea8e0255f1510d` | `74c367a931eeb21a`→`3e2944d75e989d2e` | 39／0／1；那一格在 proxy 層；中性磚沒了 |
| N1 `fig_n1_roadmap` | `db11947bf74e338f`→`65776ce7c65ba5d7` | `8b135fa9d7bc09bc`（前 `4a9190d6aa7c55fa`） | 只有 as-of（`3368412d`） |
| N1 存檔 `…_with_detect_only` | `9b08e87556d8c95d`→`fa51a42259779340` | `b4d7c6d6bdf6b931`→`3a5cc142c1aaef58` | 同上 |

08:48Z 那一次重生（釘在 main `299c9e23`）的 Q4 `e776f09cf0e32b11`、Q5 `1ee55fa6be46c241` 已被 08:58Z 那一次取代。其他 58 個 PNG 逐位元不變：`S/regen-check-all-20260928T0907Z.log`（17 支腳本、18 次、70 個 PNG 相同、0 個停、真的圖資料夾沒被動、沒有 `__pycache__`）。
重生紀錄：`S/regen-repin-20260928T0848Z.log`、`S/regen-repin2-20260928T0858Z.log`；PNG 清單 `S/png-sha-before-repin-0928.txt`、`…after-repin-0928.txt`、`…after-repin-final-0928.txt`。

**改了的腳本**（sha256 前 16 碼）：`make_engineering_figs.py` `6f26e0ad…`→`a0f7cc8a…`（中間版 `8959a132…`）；`make_fixed_since_916.py` `6ebcf0cc…`→`d93cead0…`；`make_roadmap.py` `595aab61…`→`0c746837…`。改前的版本在 `S/repin-0928-bak/`。
- engineering：`STATE` `3368412d`、`STATE_AT` 08:53；fig_q3 第一張卡改成 fixed · merged，它的檢查反過來（分支與修正 commit 必須在 `STATE` 裡）；fig_q4 畫每個 run 的最後一次 attempt，較早 attempt 的 GCC log（`S/ci-raw/earlier/`）有紅就在那一點外畫紅圈；
  PR #15–#17 的 GCC log 抄進 `S/ci-raw/`（`MANIFEST.txt`）；compare 記錄的第一行可以寫 PR 的 head 而不寫 run id（`ci-compare-pr17.txt` 就是這樣），此時由 PR 編號找它畫出的 run、並斷言其中一個在那個 head 上；fig_q5 的綠字依編號排序（#16 比 #15 先 squash）。
- F1：拿掉中性標題、斜線磚與它的位置停止條件；新增兩個停止條件（§1 帶粗體數字卻不是狀態也不是層的列、沒有層名的 §2–§4 標題）。
- roadmap：`AT` `3368412d`。

**紅檢**：
- engineering `S/make_engineering_figs-redcheck-20260928T0857Z.log`：133 個停止點，130 個看過紅、3 個到不了；181 個竄改 181/181；對照組 4/4；harness 自檢 4/4。
  跟著改的案例：925c／925d 反過來（分支 head 或修正 commit 不在 `3368412d` 就停）；1032、1190、1185、1185b、1233a、1210、443e、443f 的預期字串換成 `3368412d`／`eef173a9` 與新的列號；新加 1060、1064、1070a、1070b、1075a、1075b（較早 attempt）與 396（寫 head 的 compare 記錄）。
  被取代：`…T0841Z.log`（行號還沒重對，FAIL）、`…T0844Z.log`（我先前一支腳本在 S 留了 `__pycache__`，FAIL；已刪）、`…T0846Z.log`（PASS，但產生器是 `8959a132…`、PR #17 之前）。
- roadmap `S/make_roadmap-redcheck-20260928T0847Z.log` 5/5（`…T0846Z.log`：模擬的 git 回答還寫 `85bec430`，3 個 SURVIVED，被取代）。
- F1 `S/mutation_check_fixed_since_916.repin-20260928T0905Z.log` 13/13（檔頭：產生器 `d93cead0…`、harness `0483aaf7…`、清單 `d9887430…`）。拿掉的變異（它們的目標不存在了，不留著空轉）：M10、M11.1–M11.5、M12；改瞄準的：M10b、M11b。
  被取代：`…repin-20260928T0841Z.log`、`…T0859Z.log`、`…T0904Z.log`（清單後來又改過字）。
- T1 `S/t1c-coverage-redcheck-repin-20260928T0847Z.log` 12/12；tutorial `S/make_tutorial_figs_0927-redcheck-20260928T0847Z.log` 69/69（這兩支腳本沒改）。

**清單 §0 的 audit-raw**：`S/audit-raw-check-20260928T0905Z.log`（清單最後一版之前的最後一次；兩份 compare 記錄 `ci-compare-pr15.txt`、`-pr16.txt` 不在 audit-raw，已列）；那一項的判官檔不再引用。

**拿掉的引用與暗示**（coordinator 09-28）：那一項的判官紀錄的路徑在模板 Q3 講稿、Q3 `.md` 的兩張表與「when」行、Q2 `.md` 的判官檔表、清單 §0 與 §2.2 那一列都拿掉了（Q2 表寫「另一個子目錄的 2 份，不列路徑」）；
清單那一列不再連到 PR #15 的 CI 紅與 §4.2 的修法；§4.2 那一列不再提 PR #15；N3 拿掉「the cleanup privilege bug is fixed」那一列（它已修）；模板規則 8 的核定說法段落改成一句。
engineering 產生器的 fig_q3 仍會讀那兩份判官檔的判決行（只查字串、不印內容，紅檢的訊息也不寫出來）；路徑字串在程式碼裡。要連這個也拿掉，卡片上的「judge」就沒有東西可以核對。

**在審的那一格**：`residue clock`（ndt tool，`fix/residue-live-pid-wait-0928` @ `74d1383f`，tip 08:18Z，本機沒有判決檔）。照清單 §0 的規則（每條未併、tip ≥ 09-16 的修法分支都算），它在 F1 的 IN REVIEW 帶；只算有判決的在審分支的話，這格不會出現。

**沒驗到**：`f253ed08` 那一次 GCC 的 log（要認證）；Q4 的紅圈只看 PR #15 兩個 run 的較早 attempt（其他 run 沒有較早 attempt 的 log，公開 API 的 jobs 只報最後一次）。

## 12. 09-28 13:2xZ：F1 在審加一條（v1.6）

1. 改了什麼：清單 §4.3 加 `spawn helpers`（tests / instruments；`fix/spawn-helper-subshell-0928` @ `dfdb2121`，`3368412d` 上一顆 commit，沒推、還沒判決）⇒ 39／0／**2**、層 2／6／5／**28**／0、41 格；跟著改清單 §0、§1、§4、§8、§10，模板 F1 段與來源表，本檔 §2、§3 的 F1 列，F1 `.md`。快照、merge、公開狀態不變（13:20 未認證：兩個 trunk `3368412d`、兩個 main `eef173a9`，`S/net-spawnhelpers-20260928T1320Z.log`）；residue 那條的 tip 已是 `571fa6fd`，清單 §4.2 仍寫 08:3x 的 `74d1383f`（§0 註明，沒跟）。
2. 為什麼：09-28 診斷 residue 偶發紅時找到第二條修法——六支 shell 套件的 fixture spawn helper 失敗只離開 subshell、從沒被算到；照清單 §0 的規則（未併、tip ≥ 09-16 的修法分支都算）列進 IN REVIEW 帶。
3. 證據：F1 PNG `97ea8e0255f1510d`→`c057decb32fc5fa6`（500 dpi `3e2944d75e989d2e`→`dab7e3fe3a4dbb9f`）；產生器沒改（`d93cead0…`），重生 `S/regen-spawnhelpers-20260928T1321Z.log`；紅檢 `S/mutation_check_fixed_since_916.spawnhelpers-20260928T1321Z.log` 13/13、對照綠、rc=0（harness 只換 M6、M10b 兩個錨點，`0483aaf7…`→`d664c704…`；清單 `26ff3d6a…`）；其他 PNG 逐位元不變 `S/regen-check-all-20260928T1321Z.log`（70 相同、0 停、真的圖資料夾沒動）；改前的檔在 `S/spawnhelpers-0928-bak/`。

## 13. Removed 2026-09-29（v1.7：Adam 09-29 的四條指示）

### 13.1 改了什麼
- Adam 2026-09-29（轉述）：① 前兩頁逐日進度重複 → 拿掉 A1（`fig_o1_since_0916`）、A2（`fig_o2_thirteen`）；② 教授不需要開發史、除錯史，只留技術決策與最後結果；③ 開場先講：各 exercise 大概在做什麼（挑一兩支細講）、09-16 的 NDTwin kernel 為了接這些 exercise 需要哪些改動、最後用什麼辦法做到；④ 第 33 頁 F1「Found, then fixed」拿掉。
- orchestrator 的決定（照做）：新增 B 段（B1 表、B2 圖、B3 圖、B4 表、B5 表），T3 接在 B5 之後；拿掉 T2、Q1–Q5、F1；N3 刪兩列 CI、改寫「users already have these fixes」；留下的頁的講稿刪掉開發過程的敘述、保留出處與界定宣稱的但書。
- 模板 v1.7：§0 規則 1 記下 B 段不受 delta only 限制（Adam 09-29）；規則 2、5、10 跟著改；§1 重排（32 頁）；§1b 產檔紀錄；§2 新增 B1–B5、刪 9 頁、修 20 頁的句子；§3、§4 跟著改。
- 新檔：`figures/background/make_background_figs.py`、`fig_b2_basic_walkthrough.*`、`fig_b3_basic_tunnel.*`（含 `_hires/` 與兩份 `.md`）。kernel 樹只寫了 git-ignored 的 `scratch/overnight-2026-09-05/logs/slides930/`：`make_background_figs-redcheck.py` 與 log（81/81）、`b-section-sources-check.py` 與 log、`verify-deck-930.py` 與兩份 log、`RESTRUCTURE-0929.md`。
- 產生器 `generator/build_deck_930.js`：B 段五頁、頁序、N3 七列、存檔清單 5 → 13 張、頁數斷言 36 → 32。重產的 pptx 驗過（模板 §1b）；PDF 沒有重產。
- 沒刪任何檔：拿掉的頁的圖、產生器、紅檢 log、`.md` 都還在，只是列進存檔清單。

### 13.2 拿掉的頁的講者備註（v1.6 §2 原文，逐字）

~~~markdown
### A1 `What landed since the 09-16 report`　form: figure　`overview/fig_o1_since_0916`
- 六條線各一列；◇＝merge／commit（🟠 git 日期），●＝跑過的 live run（🟢 run 目錄的 UTC 戳）。時間一律 UTC。
- 09-17／18：package 工具（convert、pre-flight）、`ndt up p4 --app`、每台跑自己的程式（`386eb20c`、`54f69d15`、`b392f111`）。
- 09-19 14:43Z：13 支兩臂第一次全照預期（🟢 `L/2026-09-19T144328Z_06_thirteen`，code `f3b6d09c +61`）。
- 09-24：roles 第一刀（`572d9462`），2 分鐘後 live 07；09-26：心跳段 W（`cafd518a`），1.5 分鐘後 H1–H4、17:29Z H5；09-27：protobuf 5（`5dc7fc9a`），3 分鐘後又 13/13；`3d740be0` 起 main 只經 PR。
- 09-20～09-23 的空白是真的：trunk 那四天 0 個 commit（🟠 `git log --first-parent`）。
- 🟢 H1–H4 與 H5 的 `PASS 08_heartbeat` 在 `I/hbw-live/h14-20260926T152605Z.log:190`、`h5b-20260926T172912Z.log:59`（run 目錄沒存 stdout；兩份 log 都在 audit-raw `797c34ab`）。
~~~

~~~markdown
### A2 `Exercises with both arms as expected`　form: figure　`overview/fig_o2_thirteen`
- 09-08 那一點是 **not run**（空心灰方塊，畫在 0 線下方、不在刻度上）：916 模板 :257 的「0/13」是「0 支在 NDTwin fabric 上**跑過**」，那時還沒有「兩臂照預期」這個判定可比；它是 09-16 報告前的背景。
- 🟢 09-19 四輪：0 → 8 → 10 → **13**（code `dfb9d0d7 +47`→`cbc968d8 +54`→`7242e127`／`1ea07e7b +60`→`f3b6d09c +61`，都是髒 checkout）。第一輪的 0 不是 exercise 失敗：24 臂是「LAB NOT RETURNED」（收尾沒交回 lab），圖上是空心點「no verdict」。前三輪在 audit-raw `5cf0364c`。
- 🟢 09-24 16:06Z 掉到 12（code `67b64869 +64`；ecn 的探測只看得到 2–4 個封包，是儀器鑑別力不足）→ 修 driver（`0c96c1d0`，斷言一字未改）→ 18:55Z 回到 13（code `0c96c1d0 +79`；REPORT-P4-2026-09-25.md §5）。
- 🟢 之後四輪都 13/13：protobuf 5 試跑（code `580767a8 +83`，候選 venv，心跳還沒進來）與**心跳開著的三輪**（code `cafd518a +88`、`3f8c2abf +91`、`5dc7fc9a +95`，都是髒 checkout；最後一輪也是 protobuf 5 遷移後的驗收）。
- 「兩臂照預期」＝骨架臂紅在該紅的地方、解答臂綠（規則 `live-p1/06_thirteen.sh:107-115`、`:142-155`）。❌ 不等於 twin 看得見每一支（見 T1、T7）。
~~~

~~~markdown
### T2 `13 exercises × 2 arms, every full run`　form: figure　`p4-tutorials/fig_t5_arms_by_run`（○）
- A2 的逐臂版：10 次完整 run（26 列）一欄一次。🟢 每欄底下是照預期的臂數：2、20、23、26、25、26、26、26、26、26。
- 白點＝該臂的 arm report 記錄了 `ndt up` 啟動心跳（09-26 起三輪各 17 臂）；「protobuf 5」兩欄：09-26 05:51Z 是試跑（候選 venv）、09-27 07:46Z 是遷移後驗收。
- 09-19 前三欄的紅／斜線逐格原因在 `fig_t5_arms_by_run.md`：多數是量測工具本身的缺陷；**有一格是 NDTwin proxy 的缺陷**（06:32Z 的 basic_tunnel 解答臂：proxy 拒收單元素 exact 值，修在 `7d6c88a2`）。
- 每欄的 checkout 都髒：+47（09-19 05:25Z）遞增到 +95（T06）。十欄的 raw 都在 audit-raw：前三欄在 `5cf0364c`，其餘七欄在 `797c34ab`（`5cf0364c` 的祖先）。
~~~

~~~markdown
### Q1 `protobuf 3.20.3 → 5.29.6 in the P4 proxy`　form: figure　`engineering/fig_q1_protobuf5`
- 🟢 09-25：requirements 對齊實際 venv（p4runtime 1.5.0、grpcio 1.82.1，protobuf 仍 3.20.3），兩套測試 1557＋187 OK。
- 🟢 09-26：在獨立候選 venv（protobuf 5.29.6）上 live 試跑：01 rc 0、06 26/26（`L/2026-09-26T055148Z_06_thirteen`，`580767a8 +83`）。
- 09-27：merge `5dc7fc9a`（判官最終 READY FOR ADAM'S DECISION，Adam 裁併；test merge 上 6 個閘門 5 個過，紅的那個是 TMPDIR 長度問題，後來 `fed37cff` 修）。🟢 遷移後新 venv 跑 1658＋187 與舊 venv 輸出一字不差、4 個 descriptor 相同；🟢 live 驗收 01 PASS、06 26/26（T06，`5dc7fc9a +95`）。
- 圖上兩帶分開標：上面「READ · requirements, step names and dates from git」，下面結果格「RAN IT · test, gate, live-run and CI logs」（第三輪）。
- 每一步底下是一個結果格（第二輪：不再是一列列帶點的字），格頂的色條＝那一步的結果：綠＝過、黃＝部分、紅＝CI 紅。
- 🟢 CI（紅色條）：前後都是 12 個 L1 組、29 行 FAILED 逐行相同——**CI 是紅的，前後一樣紅**（09-27 遷移當時；之後：PR #12–#14、#16、#17 與 ndtwin-lab trunk 從 `8d622ea4` 到 `3368412d` 的 run 四個 job 全綠，但不是每一次都綠，見 Q4）。
- Dependabot：ndtwin-lab repo 上兩個 high 的 protobuf alert 在 2026-09-27 08:20:24Z／08:20:25Z 以 fixed 關閉（coordinator 以 gh api **已認證**查核，沒有存 raw、不是公開 URL）；Adam010341 那份的 Dependabot alerts 是關的。
- ❌ 這頁沒有任何效能數字；切換前後的效能數字不同框。
~~~

~~~markdown
### Q2 `How a change gets into trunk`　form: figure　`engineering/fig_q2_review_path`
- 路徑：worker 在自己的 worktree、測試先寫紅 → **獨立判官** → orchestrator 在 test merge 上重跑閘門 → `merge --no-ff` → 推兩個 repo → CI 對事先寫下的預測。
- 🟠 圖上那一帶標「**READ** · SINCE 09-16 / at fed37cff」：09-16 以來**至少 49 個判決**（圖上「≥ 49」）＝23 MERGE／23 AFTER FIXES（20 MERGE AFTER FIXES＋3 READY AFTER FIXES）／3 其他（2 READY FOR ADAM'S DECISION＋1 REQ），來自 `logs/**/judge-*.md` 的 38 份判官檔（mtime ≤ 2026-09-27T15:55Z，腳本確認 `fed37cff` 那時仍是 trunk tip；截止之後的判官檔不算——18:54Z 重生時有 4 份、19:4xZ 這一跑有 8 份，都是之後才寫的，名單在執行 log）。
  「≥」是因為範圍只含 `logs/**/judge-*.md`：`FIXED-SINCE-916.md` 引用的 `hunt-0911/fix/` 底下另有 6 份 `*-JUDGE.md`，不在這個計數裡。
  trunk `fed37cff` 上 09-16 起 **58 個 first-parent merge，45 個在訊息全文裡點名判官**（只看主旨是 23 個；以 +08 的 09-16 00:00 起算也是 58）。指令在 `fig_q2_review_path.md`；coordinator 另以同一方法核過 58／45。這些是**讀 git 與判官檔的文字**，不是跑出來的。
- 舊版的「43（18／22／3）」錯了：計數規則只認行首的判決，漏掉六份心跳複審把「合併裁決：X」寫在行中的判決（判官 F-1；紅檢見 `.md`）。
- 🟢 範例那一帶標「**RAN IT** · EXAMPLE · HEARTBEAT W · 09-26」：103/103 新測試看過紅、183/183 變異被殺；判官 AFTER FIXES → MERGE；test merge `7b600ab0` 1658 測試 OK；merge `cafd518a` 推上去後 CI 的 L1 從 14 變 15（新紅），`329dc555` 修好回到 14。
- 這些數字是判決行，不是改動數。
~~~

~~~markdown
### Q3 `What review caught since 09-16`　form: table
投影片上是這張表；`engineering/fig_q3_review_catches` 留作存檔。

| catch | caught by | when (UTC) | state |
|---|---|---|---|
| privilege bug in a cleanup path | judge | 09-27 | fixed; merged `fc25112e` (#15) |
| heartbeat test was phase-locked | judge | 09-26 | re-measured; merged `9c2e59e4` |
| G1 PASS, nothing delivered (flowcache) | raw review | 09-27 08:12 | open |
| H5 sampler recorded nothing | live run | 09-26 15:32 | fixed; merged `0925d9fc` |
| an ndt edit moved serve's line anchors | CI | 09-26 15:25 | fixed; merged `329dc555` |

- 第 1 列：判官抓到；分支 `fix/rulings-kjl-0927`（tip `945d695d`）09-28 06:36Z 以 `fc25112e` 併入 trunk，PR #15 08:28Z squash 進 main（`299c9e23`）。只說「cleanup 路徑的權限缺陷，審查抓到，已修（#15）」；不描述機制、不給攻擊步驟。
- 第 2 列：`I/judge-HBSPIKEDOC-4820862b.md:9`；去相位重量後併入 `9c2e59e4`（09-26 09:38Z；H4 頁）。
- 第 3 列：caught by 是 **raw review**——那一輪 live run 自己判 PASS（`E/live-p1/runs/2026-09-27T074635Z_06_thirteen/00_table.tsv:27`），沒送達是事後讀 raw 才看到的（GAP-2b:239；09-28 提交 `c8433963`）。
  🟢 raw：`FC/link_usage/iperf_client.txt:9-10`、`iperf_server.txt`（沒有報告列）、`netdev.before:3`→`netdev.after:3`（往 h3 的 s3-eth1 只 +273 B）。T06 的流只到了 s1→s3 那一段；twin 的讀數與它一致（T1、T7 都標 IPv4 only）。沒送達是 exercise 控制器的競賽，不是 twin 的錯（INFERRED）。
- 第 4 列：🟢 `I/hbw-live/h5-20260926T153259Z.log:59`（那輪 FAIL）；修在 `0925d9fc`，重跑有樣本且 PASS。第 5 列：🟢 `I/ci-36251857977-gcc.raw.log:6888`、`I/ci-compare-cafd518a.txt:11`（L1 14→15）。
~~~

~~~markdown
### Q4 `CI: L1 problem groups per run`　form: figure　`engineering/fig_q4_ci_state`
- 🟢 09-25～09-28 的 56 次 run（46 次有 GCC log、10 次是只有公開 API 結果的 ndtwin-lab trunk run）：L1 從 14 開始，被推到 15 兩次（`377a1271`、`cafd518a`）、當天修回；`b005bf50` 降到 12；PR #11（CI L1 lane，`9ef10250`）降到 1；PR #12 起是 0（`L1 passed`）。
- 🟢 四個 job：09-27 以前 GCC、clang、TSan 失敗、ASan 過；PR #9（clang／TSan 的修法，`18c83aba`）起 clang、TSan 過；**四個 job 第一次全綠是 ndtwin-lab trunk `8d622ea4` 的 run（09-28 01:26Z）**；**第一個全綠的 PR 是 #12**（01:38Z）；圖上 PR #12–#17 與 ndtwin-lab trunk 從 `8d622ea4` 到 `3368412d` 的 run，最後一次都是四個 job 全綠（公開 API 的 jobs 快照 `engineering/_net/jobs_*.json`；09-28 的 GCC log 在 `slides930/ci-raw/`）。
- 🟢 PR #15 的兩個 run 各有紅的較早 attempt（五次 GCC 裡三次紅，L1 1 組：`test_apps_residue.sh`；原因是 ndt 的 residue report 兩次讀鐘之間跨秒，與那個 PR 的改動無關），重跑後綠；圖上畫最後一次 attempt，外面加紅圈。
- 狀態釘在 trunk `3368412d`、公開 API 08:53Z（圖左下 as-of）；之後的 run 不在圖上。圖上 PR 的點標「PR #11」「PR #12」；沒有 GCC log 的 10 次 trunk run 各畫一條短豎線，圖例一個「no log」；紅圈的圖例「red on an earlier attempt」。
- 講法：「PR #12–#14、#16、#17 與 ndtwin-lab trunk 從 `8d622ea4` 到 `3368412d` 的 run，四個 job 全綠（每個 run 的最後一次）；不是每一次都綠——一個不穩定的 shell 檢查（`test_apps_residue.sh`）讓 Adam010341 trunk `f253ed08` 的一次、PR #15 五次 GCC 裡的三次變紅，重跑後綠。」`f253ed08` 的原因依 coordinator 查到的是同一個不穩定的檢查（那份 log 我沒讀，要認證）；圖不畫 Adam010341 自己的 trunk run。
~~~

~~~markdown
### Q5 `main moves only by squash-merged PR`　form: figure　`engineering/fig_q5_main_by_pr`（○）
- 🟠 規則（`CLAUDE.md` 授權邊界）：審查只在 trunk；main 只經 Adam010341 上的 PR＋squash；PR 排除 `doc/audit/**/*.md` 與 `REPORT*.md`；**09-28 Adam 改：ndtwin-lab 的 main 跟著同步**（每次 squash 後把同一顆 main 快轉推過去；`08f67b7a`，已在公開 trunk、也已經 PR #17 進 main），取代 09-27 的「凍在 `f186ce98`」。
- 🟢 未認證（2026-09-28 08:53:29Z，`engineering/_net/`）：兩個 trunk `3368412d`；兩個 main 都是 `eef173a9`＝squash 鏈 #6 `ce6a9832` → … → #14 `be01cc7a` → #16 `9a74408b` → #15 `299c9e23` → #17 `eef173a9`（十二個 PR 都已併、沒有開著的）。`eef173a9` 的 tree＝trunk `3368412d` 去掉三個 `doc/audit/**/*.md`（本機唯讀 `git diff --name-status`）。
- 圖上 ndtwin-lab 的 main 標「follows」；綠字「#6–#17」依編號（#16 比 #15 先 squash）；as-of 在右上。
~~~

~~~markdown
### F1 `Found, then fixed — since 09-16`　form: figure　`fixed-since-916/fig_f1_fixed_since_916`
- 🟢 09-16 之後 trunk 進了 **39 個修法 merge，全部在兩個公開 repo 的 trunk 上**（未認證 HTTPS，2026-09-28 08:38Z，兩邊都是 `3368412d`），也都在兩個 main（08:53Z `eef173a9`）的內容裡；**0 個只在本機**；**2 條修法分支在審**。清單截止於 trunk `3368412d`；日期一律 UTC（圖上欄位 09-18…09-28 UTC，右上標 as-of）。
- 41 格裡 **28 格是量測儀器與測試本身的缺陷**（已併的 27 格由 live run、CI、判官或閘門抓到，1 格在審）——不是全部都由 live 或 CI 先抓到（誰抓到見 `FIXED-SINCE-916.md` §2.4 末）；先修儀器，再相信數字。kernel C++ 的 2 格都已公開：sFlow 取樣先記鏈路位元組、再辨識封包（P3-A），以及 clang／TSan 抓到的解構子與 `localtime`。
- `rulings KJL`（proxy）：cleanup 路徑的權限缺陷，審查抓到，已修（#15）。
- 🔴 公開 trunk 有 ≠ 使用者拿得到：手冊叫人 clone 的 P4-public 停在 09-03、一格都沒有（`FIXED-SINCE-916.md` §8–§9）。
- 每一格的 live 證據都是髒 checkout（「code <sha> +N」，+29 到 +92）；`fed37cff` 之後新併的 7 格沒有 live。FIX／FEATURE 的界線是判斷，換規則會動 1–5 格（§0）。
- IN REVIEW 帶有兩格。第一格是 `residue clock`（ndt tool：residue report 兩次讀鐘的跨秒競態，就是讓 CI 偶發紅的那個；`fix/residue-live-pid-wait-0928` @ `74d1383f`）。tip 在快照前 14 分鐘、本機還沒有判決檔——只算有判決的在審分支的話，這格不會出現。
- 第二格是 `spawn helpers`（tests / instruments：六支 shell 套件用 `X="$(…)"` 叫 fixture 的 spawn helper，helper 失敗只離開 subshell、從沒被算到；修法在父 shell 算成具名的失敗檢查，等待上限 30 s；09-28 診斷 residue 偶發紅時發現；`fix/spawn-helper-subshell-0928` @ `dfdb2121`，tip 10:57，快照之後）。本機也還沒有判決檔。
- 09-28 06:2x 的版本是 37／0／2（`85bec430`），09-27 的是 32／0／4（`fed37cff`）；清單 §1 的對帳段寫了每次動了哪幾格。
~~~

### 13.3 留下的頁被刪掉或改寫的句子（v1.6 原文 → v1.7）

A0 的開場白因為多了 B 段而改寫；N3 整段換成新的七列版（下面的 v1.6 原文含舊的九列表與講稿）。其他都是刪掉開發過程的敘述，出處與但書留著。

**A0**

~~~markdown
- 「這次只講 9/16 之後的事。主線一條：13 支 P4 tutorial exercise 現在都在 NDTwin 的 fabric 上跑起來、兩臂照預期；
  另外是兩刀讓 NDTwin 能寫外來程式的路由表、能偵測它的斷線，一個本機的網頁入口，一份遙測比較，還有工程上的事。」
~~~
→
~~~markdown
- 「先用五頁講背景：13 支 P4 tutorial exercise 各在做什麼，細看 basic 與 basic_tunnel 兩支，09-16 的 NDTwin 對它們缺什麼，我們用什麼辦法補上。
  之後只講結果：13 支現在都在 NDTwin 的 fabric 上跑起來、兩臂照預期；兩刀讓 NDTwin 能寫外來程式宣告的那一張路由表、能偵測它的斷線；執行期改規則；一個本機的網頁入口；一份遙測比較。」
~~~

**T1**

~~~markdown
依判官 F-2 重切：916 第 3 頁的 13×16 需求矩陣**拿掉**（逐格同 916），只留兩列 NDTwin 與右邊兩欄，分三個有標題的面板。
~~~
→
~~~markdown
兩列 NDTwin 與右邊兩欄，分三個有標題的面板。
~~~

**T1**

~~~markdown
（第三輪改標：格子是依跑過的證據下的判斷）
~~~
→
~~~markdown
（格子是依跑過的證據下的判斷）
~~~

**T1**

~~~markdown
  GAP-2b 裁定前把它判「看得到 (judgement)」，先引的就是 T06 的 `flowcache/sol:588-604`（第一輪說「用的是 09-26 那輪」是錯的）；09-28 Adam 裁定為 IPv4 only，GAP-2b 那一格也改了，腳本不再覆寫。FC＝`E/runs/2026-09-27T081256Z_flowcache_solution_ndtwin`。
~~~
→
~~~markdown
  flowcache 那一格 Adam 09-28 裁定為 IPv4 only（N3 第 5 列）。FC＝`E/runs/2026-09-27T081256Z_flowcache_solution_ndtwin`。
~~~

**T1**

~~~markdown
- **四個判斷格 Adam 09-28 已裁定**（照建議值）：`registers`＝部分、`queue_metadata`＝做得到、twin 欄的 multicast＝看得到、flowcache＝IPv4 only；圖上不再有虛線框，右上標「as of GAP-2b with Adam's 2026-09-28 ruling」。
~~~
→
~~~markdown
- **四個判斷格 Adam 09-28 裁定**（照建議值）：`registers`＝部分、`queue_metadata`＝做得到、twin 欄的 multicast＝看得到、flowcache＝IPv4 only；右上標「as of GAP-2b with Adam's 2026-09-28 ruling」。
~~~

**T3**

~~~markdown
下半標「RAN IT: the boxes · READ THE CODE: the arrows」（第三輪）。
~~~
→
~~~markdown
下半標「RAN IT: the boxes · READ THE CODE: the arrows」。
~~~

**T4**

~~~markdown
- ❌ 早先流傳的「h2／h3／h4 收得到」是錯的（raw 對過）。這支是單交換機，心跳沒東西可看——不要在這頁講心跳。
~~~
→
~~~markdown
- 這支是單交換機，心跳沒東西可看——不要在這頁講心跳。
~~~

**T7**

~~~markdown
都是「**IPv4 only**」（第二輪統一）：
~~~
→
~~~markdown
都是「**IPv4 only**」：
~~~

**R1**

~~~markdown
；external 控制面目前沒有斷線偵測；分支上的工作**不上台講**（N1 已拿掉；09-28 確認併入前不放回）。
~~~
→
~~~markdown
；external 控制面目前沒有斷線偵測。
~~~

**H1**

~~~markdown
  不用 T06 當來源：T06 的清單仍列 `link_watchdog`，但同一個 switch_state 寫心跳 watchdog 在跑（`E/runs/2026-09-27T074826Z_basic_solution_ndtwin.md:58` 對 `:301`）——清單誤報，修在未併的分支上（FIXED 的 rulings AEG 列 E 項）。腳本現在會在這種不一致時停下（紅檢 `slides930/h0-footer-redcheck-20260927T1941Z.log`）。
~~~
→
~~~markdown
（刪除）
~~~

**H4**

~~~markdown
- 🔴 **教訓：相位鎖。** 09-26 第一次 spike 的迴圈總在「剛聽到一幀後約 0.7 s」剪線（判官 `I/judge-HBSPIKEDOC-4820862b.md` Blocking 1）。raw：
  `K/doc/audit/2026-09-25_p4-heartbeat/spike/runs/2026-09-26T023021Z_S_heartbeat/20_cycles.tsv` 與 `…/2026-09-26T052148Z_S_heartbeat/20_cycles.tsv`：20 次裡 **18 次在 14.197–14.382 s**、另兩次是各 run 的 cycle 1（13.275、13.298 s）——同一相位的重複，不是分布。
  補了去相位：`…/2026-09-26T085020Z_S_heartbeat`（sweep 10 次，10.077–14.904 s）、`…/2026-09-26T085506Z_S_heartbeat`（random 20 次，10.668–14.791 s）；H1 再刻意剪在最壞相位（φ≈0.02 s）三次。四份都在 audit-raw `797c34ab`；code `4bc1201b +79`、`580767a8 +79`、`094f417f +84`。
  ⇒ 早先的「中位數約 14.3 s」是相位鎖住的 report 層級數字，**不用**。
~~~
→
~~~markdown
- 剪線相位：H1 前三次刻意剪在最壞相位（φ≈0.02 s，剛聽到一幀之後），後三次相位均勻隨機（`E/live-p1/08_heartbeat.sh:873-874`、`:934-937`；`30_cycles.tsv` 的 `phi_target` 依序 0.02、0.02、0.02、4.48、4.53、0.98）。早先的「中位數約 14.3 s」**不用**（相位鎖住的 report 層級數字，不是 kernel 圖上的偵測時間）。
~~~

**H6**

~~~markdown
- 🔴 **要揭露：09-26 17:29Z 那輪（第三欄）混進過一次外來流量。** 17:55:05–17:55:17Z，另一個 worker 的離線測試（`tests/shell/test_live_p1_common.sh` 的 5e 格）在這輪 live 06 的真主機之間跑了 2 Mbit/s iperf（`FIXED-SINCE-916.md` 的「5e no-lab」列；事故紀錄 `I/hbw-live/INCIDENT-20260926T1755Z-worker-traffic-into-live-06.md:1-29`）。
  受影響的只有 `E/runs/2026-09-26T175425Z_p4runtime_solution_ndtwin` 的 G1 位元組（約 +8.6%；`E/runs/2026-09-26T175425Z_p4runtime_solution_ndtwin.md:613` 的 s1-eth2 4,735,073 B，對 T06 同一臂 `E/runs/2026-09-27T081205Z_p4runtime_solution_ndtwin.md:612` 的 4,361,273 B，+8.57%；判定仍 PASS）；下一臂 `E/runs/2026-09-26T175515Z_flowcache_solution_ndtwin.md:593-594` 兩條主路徑各約 4.59 MB，**沒有加倍**。
  本頁比的是 rc＋判定與 host 埠幀數，都不看 G1 位元組，所以「相同」與「0」不受影響；修法 `3db3b9a8`。
~~~
→
~~~markdown
- ⚠️ 第三欄（09-26 17:29Z）有 12 s 的外來 2 Mbit/s iperf 進了 p4runtime 解答臂的 G1 位元組（約 +8.6%，判定仍 PASS；`E/runs/2026-09-26T175425Z_p4runtime_solution_ndtwin.md:613`）；本頁比的是 rc＋判定與 host 埠幀數，不看 G1 位元組，所以「相同」與「0」不受影響。
~~~

**S1**

~~~markdown
- merge：API＋cells＋walks `48209682`（09-26 00:05Z）、GUI v1 `f186ce98`（09-27 12:35Z）、claim-note 測試不再依賴 TMPDIR 長度 `fed37cff`（09-27 15:47Z，只動測試）。
~~~
→
~~~markdown
- merge：API＋cells＋walks `48209682`（09-26 00:05Z）、GUI v1 `f186ce98`（09-27 12:35Z）。
~~~

**S3**

~~~markdown
（第三輪；圖右上有圖例）
~~~
→
~~~markdown
（圖右上有圖例）
~~~

**S4**

~~~markdown
分支 `feat/ndt-serve-gui-v2-0927`：`0d7f6ce8` 範圍草案（15:53Z）、`f3a20447` 伺服器端準備（16:20Z）、`6d5621ab` headless Chrome 測試驅動（16:36Z）；**還沒有頁面檔、未併**（2026-09-28 06:1xZ 重查：tip 仍是 `6d5621ab`；`make_serve_s2_s4.py` 重跑 rc 0、圖逐位元相同）。出現頁面檔腳本就會停。
~~~
→
~~~markdown
分支 `feat/ndt-serve-gui-v2-0927`（tip `6d5621ab`，09-28 重查）：**還沒有頁面檔、未併**。
~~~

**M1**

~~~markdown
CPU 有勘誤，這頁不談。
~~~
→
~~~markdown
CPU 這頁不談。
~~~

**N1**

~~~markdown
- 🔴 external 控制面的 detect-only **不在這張圖上、不上台講**（分支 `480e9f2e` 未併；coordinator 09-28 確認：併入前不放回）。含它的版本存檔在 `next/fig_n1_roadmap_with_detect_only.*`，放回只要換圖檔（或跑 `make_roadmap.py --with-detect-only`）。
~~~
→
~~~markdown
（刪除）
~~~

**N2**

~~~markdown
事件驅動 pass 最壞約 15.5 s 是段 W worker 的推算
~~~
→
~~~markdown
事件驅動 pass 最壞約 15.5 s 是設計推算
~~~

**N3**

~~~markdown
### N3 `What we do not claim`　form: table
| we do not claim | because | evidence |
|---|---|---|
| NDTwin operates any foreign P4 | roles bind one dst-IP table; no link detection under an external controller | route_binding.py:159-161; h14 log :168 |
| the twin observes custom headers | own-frame evidence only for 0x1212 | T7; GAP-2b §3 |
| telemetry lowers the pps ceiling | no resolution at 20 kpps | cooperative_f64_a.log :8, :15 |
| detection ≤ 20 s, guaranteed | one watchdog phase sampled | 30_cycles.tsv; judge-HBW :73 |
| flowcache G1 PASS = delivered | flow reached s1→s3 only; h3 got nothing | netdev s3-eth1 +273 B; iperf_server.txt; iperf_client.txt :10 |
| CI green = checked on the lab | hosted runner: switch, compiled P4, Ryu → skipped | .github/workflows/ci.yml :130-138 |
| CI stays green | one shell check flakes (a clock race); its fix is on a branch | run 36373153486 (f253ed08); PR #15's red attempts |
| the serve GUI ran on the lab | stub server only | ndt-serve-gui REPORT :10 |
| users already have these fixes | manual's repo stops at 09-03 | FIXED-SINCE-916 §8–§9 |

- 這一頁延續 916 的誠實頁：每一條都是這兩週裡有人想講、而證據撐不住的說法。完整路徑在 `README-930.md` 與各圖 `.md`。（重新釘住時拿掉了「the cleanup privilege bug is fixed」那一列——它已修，#15。）
- 第 1 列（第二輪改）：不再提 detect-only（分支未併、不上台）；證據改成 roles 只綁一張目的 IP 表，以及 external 控制面下沒有斷線偵測（🟢 `I/hbw-live/h14-20260926T152605Z.log:168`）。含舊字的表留在 README §7。
- 第 5 列（第二輪改）：證據改引 `FC/link_usage/netdev.before:3`→`netdev.after:3`（s3-eth1 3531 → 3804 B，+273）、`FC/link_usage/iperf_server.txt`（沒有報告列）與 `iperf_client.txt:10`（沒收到 ack）；FC＝`E/runs/2026-09-27T081256Z_flowcache_solution_ndtwin`。只有 client 那一行只能說「最後的 ack 沒回來」，不能說「0 個送到」。
- 第 6 列（09-28 改）：舊列是「CI is green | L1 12 groups; clang, TSan fail | ci-36319541715-jobs.txt」，現在 PR #12–#14、#16、#17 與 ndtwin-lab trunk 從 `8d622ea4` 到 `3368412d` 的 run 最後一次都全綠，舊列不成立；改成 CI 綠的範圍。🟠 證據是讀 `ci.yml`（trunk `3368412d`，註解說明 hosted runner 上哪些項目跳過、為什麼不算失敗），不是跑出來的。
- 第 6b 列：不是每一次都綠。Adam010341 trunk `f253ed08` 的 run 36373153486 GCC 失敗（公開 API：`engineering/_net/runs_Adam010341.json`），ndtwin-lab 同一顆 sha 的 run 通過；PR #15 五次 GCC 裡三次紅（`slides930/ci-raw/earlier/`；與那個 PR 的改動無關）。原因是 ndt 的 residue report 兩次讀鐘之間跨秒（`I/ci-compare-pr15.txt:9-11`，coordinator 的量測）；修法在 `fix/residue-live-pid-wait-0928`（F1 在審的那一格）。
- 第 7 列的完整路徑：`doc/audit/2026-09-27_ndt-serve-gui/REPORT.md:10`。
~~~
→
~~~markdown
### N3 `What we do not claim`　form: table
| we do not claim | because | evidence |
|---|---|---|
| NDTwin operates any foreign P4 | roles bind one dst-IP table; no link detection under an external controller | route_binding.py:159-161; h14 log :168 |
| the twin observes custom headers | own-frame evidence only for 0x1212 | T7; GAP-2b §3 |
| telemetry lowers the pps ceiling | no resolution at 20 kpps | cooperative_f64_a.log :8, :15 |
| detection ≤ 20 s, guaranteed | one watchdog phase sampled | 30_cycles.tsv; judge-HBW :73 |
| flowcache G1 PASS = delivered | flow reached s1→s3 only; h3 got nothing | netdev s3-eth1 +273 B; iperf_server.txt; iperf_client.txt :10 |
| the serve GUI ran on the lab | stub server only | ndt-serve-gui REPORT :10 |
| users already have this work | the manual's clone target stops at 09-03 | FIXED-SINCE-916 §8–§9 |

- 這一頁延續 916 的誠實頁：每一條都是有人想講、而證據撐不住的說法。完整路徑在 `README-930.md` 與各圖 `.md`。
- 第 1 列：證據＝roles 只綁一張目的 IP 表（`route_binding.py:159-161`），以及帶自己控制器的 exercise 沒有斷線偵測（🟢 `I/hbw-live/h14-20260926T152605Z.log:168`）。
- 第 5 列：🟢 `FC/link_usage/netdev.before:3`→`netdev.after:3`（s3-eth1 3531 → 3804 B，+273）、`FC/link_usage/iperf_server.txt`（沒有報告列）與 `iperf_client.txt:10`（沒收到 ack）；FC＝`E/runs/2026-09-27T081256Z_flowcache_solution_ndtwin`。只有 client 那一行只能說「最後的 ack 沒回來」，不能說「0 個送到」。這一列界定 T1、T7 的 flowcache 格（IPv4 only）。
- 第 6 列的完整路徑：`doc/audit/2026-09-27_ndt-serve-gui/REPORT.md:10`。
- 第 7 列：手冊叫人 clone 的那個 repo 停在 09-03 的 `9e6cc307`（`FIXED-SINCE-916.md` §8–§9；未認證查核 09-28 06:20:07Z 與 08:38:41Z 都一樣，`figures/fixed-since-916/public-check-20260928b/branch_P4-public_main.json`）。本 deck 講的 package、roles、心跳、ndt serve 都是 09-17 之後才進 trunk 的，照手冊裝的人一樣都拿不到。
~~~

**T5**

~~~markdown
分六組是 worker 的判斷（INFERRED）
~~~
→
~~~markdown
分六組是產圖時的判斷（INFERRED）
~~~

### 13.4 v1.6 §3 拿掉的列（原文）

| 數字／主張 | 出處 | commit／binary |
|---|---|---|
| 09-08「not run」（0/13 跑過） | 916 模板 `NDTwin-slide-template-916.md:257` | 背景 |
| 第一個 13/13 | `L/2026-09-19T144328Z_06_thirteen/00_table.tsv`；REPORT-P3-2026-09-24.md:99-102 | code `f3b6d09c +61` |
| 各輪 2／20／23／26／25／26×5 臂 | 十個 `L/*_06_thirteen/00_table.tsv`（`fig_t5_arms_by_run.md` 表） | 各輪 code 行，+47…+95 |
| ecn 25/26 的原因與修正 | REPORT-P4-2026-09-25.md §2 第 1 條、§5 | 修 `0c96c1d0`；兩輪 code `67b64869 +64`、`0c96c1d0 +79` |
| ≥ 49 判決（23／23／3，只數 `logs/**/judge-*.md`）、58／45 merges（45＝訊息全文點名判官；主旨只有 23） | `fig_q2_review_path.md` 逐檔表與重算指令；`git log --first-parent --merges --since=2026-09-16T00:00:00Z fed37cff` | 🟠 讀；快照 `fed37cff` |
| L1 14→15→14→12→1→0；PR #12–#17 與 ndtwin-lab trunk `8d622ea4`→`3368412d` 的 run 最後一次都四個 job 全綠（第一個全綠 PR＝#12；PR #15 有紅的較早 attempt，見 Q4） | `I/ci-*-gcc.raw.log`、`slides930/ci-raw/*.raw.log` 的 `L1 FAILED`／`L1 passed` 行；公開 API 的 jobs 快照（`fig_q4_ci_state.md`） | GitHub Actions run id 在 `.md`；快照 08:53Z |
| 39 已公開／0 只在本機（修法 merge） | `FIXED-SINCE-916.md` §1、§9 | trunk `3368412d` |
| 各層格數 2／6／5／28／0（圖例；含在審 2 格） | `FIXED-SINCE-916.md` §1、§2、§4 | 同上 |
| 兩個 main `eef173a9`（#6–#17） | `engineering/_net/pulls_Adam010341.json`、`branch_*_main.json` | 08:53:29Z 快照 |
| Dependabot 兩個 high 關為 fixed | coordinator 以 gh api 已認證查核（2026-09-27 UTC） | 不是公開 URL |
| 2 條修法分支在審（`residue clock`、`spawn helpers`） | `FIXED-SINCE-916.md` §1、§4 | trunk `3368412d` |

### 13.5 v1.6 §4 拿掉的列（原文）

| 圖 | 頁 | 產生器 | 狀態／紅檢 |
|---|---|---|---|
| `overview/fig_o1_since_0916`、`fig_o2_thirteen` | A1、A2 | `make_overview_figs.py` | 日期由 git／run 目錄算；o2 的 09-08 點＝not run；紅檢 `slides930/o1-o2-t6-t9/run_mutations-r3-20260927T1948Z.log`（14/14） |
| `p4-tutorials/fig_t5_arms_by_run` | T2 | `make_arms_grid.py` | 紅檢 `slides930/make_arms_grid-redcheck-20260927T2001Z.log`（6/6） |
| `engineering/fig_q1…`、`fig_q2…`、`fig_q4…`、`fig_q5…` | Q1、Q2、Q4、Q5 | `make_engineering_figs.py` | q1 每步一個結果格、上下兩帶標 READ／RAN IT；q2 標 READ／RAN IT、「≥ 49」；q4／q5 用 `_net/` 快照（2026-09-28 08:53:2xZ），as-of 標在圖上；q4 的 PR 點標「PR #N」、沒有 log 的 run 一個圖例；q4 的紅圈＝較早 attempt 紅；紅檢 `slides930/make_engineering_figs-redcheck-20260928T0857Z.log`（181/181，控制組 4/4）、判決計數 `slides930/engineering-verdict-regex-redcheck*` |
| `fixed-since-916/fig_f1…` | F1 | `make_fixed_since_916.py`（解析 `FIXED-SINCE-916.md`） | 快照 trunk `3368412d`（as-of 在圖上）；中性標題已拿掉（裁定 D）；紅檢 `slides930/mutation_check_fixed_since_916.repin-20260928T0905Z.log`（13/13；檔頭有產生器、harness、清單的 sha256） |

### 13.6 v1.6 §1 頁序（原文）

~~~markdown
## 1. 頁序（36 頁；`✅` 建議核心、`○` 可略，最終取捨 Adam 定）

| 段 | # | 頁 | 標題（＝圖上標題） | form | 圖檔（`figures/…`）或表 |
|---|---|---|---|---|---|
| **A 開場** | 1 | ✅ A0 | NDTwin progress · 2026-09-30 | title | — |
| | 2 | ✅ A1 | What landed since the 09-16 report | figure | `overview/fig_o1_since_0916` |
| | 3 | ✅ A2 | Exercises with both arms as expected | figure | `overview/fig_o2_thirteen` |
| **T P4 tutorial 上 NDTwin** | 4 | ✅ T1 | What NDTwin covered: 09-16 vs 09-27 | figure | `p4-tutorials/fig_t1c_ndtwin_coverage`（重切；09-16 列在背景帶；四個判斷格 09-28 Adam 已裁定，不再有虛線） |
| | 5 | ○ T2 | 13 exercises × 2 arms, every full run | figure | `p4-tutorials/fig_t5_arms_by_run`（A2 的逐臂版；可當備用） |
| | 6 | ✅ T3 | How a foreign P4 program runs on NDTwin | figure | `foreign-p4/fig_a1_foreign_p4_path` |
| | 7 | ○ T4 | multicast, end to end on the NDTwin fabric | figure | `p4-tutorials/fig_t6_multicast_end_to_end`（T3 的一個實例） |
| | 8 | ✅ T5 | What pre-flight checks before ndt up | figure | `p4-tutorials/fig_t7_preflight_checks` |
| | 9 | ○ T6 | What the exercise brings, what convert adds | figure | `p4-tutorials/fig_t8_what_you_bring` |
| | 10 | ✅ T7 | Seven custom-header exercises forward | figure | `p4-tutorials/fig_t9_custom_headers` |
| **R 外來 P4 的 API 形狀（第一刀）** | 11 | ✅ R1 | Four rulings on the P4 API shape (09-24) | table | §2 R1 表（`roles/fig_r1_four_rulings` 只留存檔） |
| | 12 | ✅ R2 | roles.ipv4_route: from package to table | figure | `roles/fig_r2_roles_path` |
| | 13 | ✅ R3 | Live 07: roles on basic, run twice | figure | `roles/fig_r3_live07` |
| | 14 | ○ R4 | What each switch reports: capabilities | figure | `roles/fig_r4_capabilities` |
| **H 第二刀：心跳** | 15 | ✅ H1 | Why link discovery stops at a foreign P4 | figure | `heartbeat/fig_h0_why_not_lldp` |
| | 16 | ✅ H2 | The veth heartbeat, from wire to kernel graph | figure | `heartbeat/fig_h0b_heartbeat_path` |
| | 17 | ✅ H3 | One cut, one restore — on the kernel graph | figure | `heartbeat/fig_h1_one_cut_cycle` |
| | 18 | ✅ H4 | Detection time: 7 live cuts | figure | `heartbeat/fig_h2_detect_vs_phase` |
| | 19 | ✅ H5 | The detection bound, piece by piece | figure | `heartbeat/fig_h3_upper_bound` |
| | 20 | ✅ H6 | Heartbeat on, forwarding unchanged | figure | `heartbeat/fig_h4_forwarding_unchanged` |
| **D 執行期改規則** | 21 | ✅ D1 | Changing rules at runtime, per data plane | figure | `flow-api/fig_d1_flow_api_matrix` |
| | 22 | ✅ D2 | "queued" is not "installed": read it back | figure | `flow-api/fig_d2_queued_readback` |
| **S ndt serve** | 23 | ✅ S1 | ndt serve: one local door to the lab | figure | `ndt-serve/fig_s1_serve_path` |
| | 24 | ○ S2 | ndt serve: threats and defenses | figure | `ndt-serve/fig_s2_security_model` |
| | 25 | ✅ S3 | Live cells: two guided walks, 09-24 | figure | `ndt-serve/fig_s3_cells_and_walks` |
| | 26 | ✅ S4 | Where the ndt serve page goes | table | §2 S4 表（`ndt-serve/fig_s4_gui_plan` 只留存檔） |
| **M 遙測比較** | 27 | ✅ M1 | Sampling error of two telemetry paths | figure | `telemetry/fig_m1_sampling_error` |
| **Q 工程與品質** | 28 | ✅ Q1 | protobuf 3.20.3 → 5.29.6 in the P4 proxy | figure | `engineering/fig_q1_protobuf5` |
| | 29 | ✅ Q2 | How a change gets into trunk | figure | `engineering/fig_q2_review_path` |
| | 30 | ✅ Q3 | What review caught since 09-16 | table | §2 Q3 表（`engineering/fig_q3_review_catches` 只留存檔） |
| | 31 | ✅ Q4 | CI: L1 problem groups per run | figure | `engineering/fig_q4_ci_state` |
| | 32 | ○ Q5 | main moves only by squash-merged PR | figure | `engineering/fig_q5_main_by_pr`（sha 是 2026-09-28 08:53Z 的快照，圖上標 as-of） |
| **F 修法** | 33 | ✅ F1 | Found, then fixed — since 09-16 | figure | `fixed-since-916/fig_f1_fixed_since_916` |
| **N 收尾** | 34 | ✅ N1 | The road to “bring your own .p4” | figure | `next/fig_n1_roadmap`（不含 detect-only；含它的版本存檔 `fig_n1_roadmap_with_detect_only`） |
| | 35 | ✅ N2 | Open questions | table | §2 N2 |
| | 36 | ✅ N3 | What we do not claim | table | §2 N3 |

✅ 30 頁、○ 6 頁（T2、T4、T6、R4、S2、Q5）。form：title 1（A0）、table 5（R1、S4、Q3、N2、N3）、figure 30。
**敘事**：主線（A）→ 怎麼跑外來程式（T）→ NDTwin 怎麼寫它的表（R）與偵測斷線（H）→ 執行期規則（D）→ 工具（S）→ 遙測（M）→ 工程（Q、F）→ 下一步與限制（N）。
09-30 前要重跑的（shas 會過期）：`fig_q4`、`fig_q5`、`fig_f1`、`fig_n1`，以及 S4 表的 v2 狀態（腳本會在狀態變了時停下，逼人更新）。
~~~

### 13.7 v1.8（2026-09-29）：R4、S2、N3 第 4 列、H4 講稿——被換掉的字（原文逐字）

- 指示（coordinator 轉 Adam 2026-09-29 的常設規則：給教授看的只放技術決策與最後結果，不放開發史、除錯史）：R4 只畫 09-26 那次 live 07 的最後狀態，sha 與 dirty 只留在 `.md` 與講稿；S2 拿掉 OVS「rc 0, fabric came up」與「since 09-25」，改畫碼裡 rc 5、not run live；N3 第 4 列的證據格拿掉審查檔名；H4 講稿拿掉「（第三輪）」。
- 圖：只重畫 `fig_r4_capabilities`、`fig_s2_security_model`（兩支產生器加 `--only`）；其他圖的 PNG／SVG／PDF 逐位元沒動（改前改後 sha256 對過）。改前的檔備份在 `K/scratch/overnight-2026-09-05/logs/slides930/v18-0929-bak/`。
- 紅檢、pptx 驗證：模板 §0 規則 10、§1c；`K/scratch/overnight-2026-09-05/logs/slides930/RESTRUCTURE-0929.md` §「v1.8 patch」。

**模板**（v1.7 原文 → v1.8）

~~~markdown
     圖上印 sha 的地方寫「<sha> · dirty」（`fig_r4`）；其他 sha 只在 `.md` 與講者備註，出現時帶 +N。
~~~
→
~~~markdown
     v1.8 起沒有一張上 deck 的圖印 run 的 sha（原本唯一印的 `fig_r4` 改成只畫最後狀態）；run 的 sha 只在 `.md` 與講者備註，出現時帶 +N。圖上若要印，寫「<sha> · dirty」。
~~~

~~~markdown
- 🟢 proxy 的 `switch_state` 每台都報 capabilities，每列 4 台完全相同（`30_／71_switch_state_*.json`，兩次 07）。圖上的 sha 標「572d9462 · dirty」「b2eeb71d · dirty」（+61／+92，腳本從 `00_status_before.txt:7` 讀）。
- 🟢 09-24 → 09-26：`link_discovery` 從 declared 變 heartbeat；`reroute` 只有 roles 那包變 true；沒 roles 的只偵測不改路（`reroute.reason` unbound）。`five_tuple` 一律 false（第一刀沒有五元組 role）。
- 09-28 起 kernel 的 `get_graph_data` 也帶這個欄位（第三刀 kernel 側 `85bec430`，只有單元測試與 CI，沒有 live）；GUI 變灰仍在 Web-GUI 的本機草稿分支。本圖只畫兩次 07 的 proxy switch_state，沒有變。
~~~
→
~~~markdown
- 🟢 最新一次 live 07（09-26，`L/2026-09-26T202055Z_07_roles_basic`，repo `b2eeb71d +92`（髒，腳本從 `00_status_before.txt:7` 讀）、kernel `be70b5dd32356847`）：proxy 的 `switch_state` 每台都報 capabilities，每列 4 台完全相同（`30_switch_state_roles.json`、`71_switch_state_plain.json`）。
- 🟢 宣告 roles 的那包：`ipv4_route` ndtwin、`reroute` true；沒 roles 的：`ipv4_route` unbound、`reroute` false（頂層 `reroute.reason` unbound）——只偵測、不改路。兩包的 `link_discovery` 都是 heartbeat（存檔時 8 條鏈路方向都由心跳餵、沒有 down）；`five_tuple` 一律 false（第一刀沒有五元組 role）。
- `ipv4_route: ndtwin` 只代表目的 IP 路由表這一張。帶自己控制器的 exercise（p4runtime、flowcache）不在圖上：那裡不起心跳。
- kernel 的 `get_graph_data` 也帶這個欄位（第三刀 kernel 側 `85bec430`，只有單元測試與 CI，沒有 live）；GUI 變灰仍在 Web-GUI 的本機草稿分支。本圖只畫 proxy 的 switch_state。
~~~

~~~markdown
- 🟢 七點：H1 六次（圓點，owned table、會改路）＋H3 一次（方點，unbound、只偵測）。x＝剪線落在最後一幀之後幾秒（φ），y＝剪線到 kernel 圖 down。規則從**最後聽到的那一幀**算 15 s，所以 φ 越小等越久；色帶＝15 − φ 到 15 − φ + 5（🟠 由常數推）；圖上色帶與 20 s 線都標「design bound (derived)」（第三輪）。
~~~
→
~~~markdown
- 🟢 七點：H1 六次（圓點，owned table、會改路）＋H3 一次（方點，unbound、只偵測）。x＝剪線落在最後一幀之後幾秒（φ），y＝剪線到 kernel 圖 down。規則從**最後聽到的那一幀**算 15 s，所以 φ 越小等越久；色帶＝15 − φ 到 15 − φ + 5（🟠 由常數推）；圖上色帶與 20 s 線都標「design bound (derived)」。
~~~

~~~markdown
- 🟢 別人的 claim 底下：`up p4` 回 rc 5、什麼都沒建；**OVS 的 `up` 卻回 rc 0、fabric 建起來了**——那是當時 ndt 的缺陷，09-25 修（`68ace017`），修後沒有再 live 跑過。
~~~
→
~~~markdown
- 別人的 claim 底下的 `up`：🟢 `up p4` 回 rc 5、什麼都沒建（09-24 live）。🟠 OVS 的 `up` 在碼裡同樣由 ndt 的 guard 回 rc 5（trunk 上 `68ace017` 起，`tools/test_workflow/ndt:4362`），**沒有在 lab 上跑過**（not run live）。
~~~

~~~markdown
| detection ≤ 20 s, guaranteed | one watchdog phase sampled | 30_cycles.tsv; judge-HBW :73 |
~~~
→
~~~markdown
| detection ≤ 20 s, guaranteed | one watchdog phase sampled | 30_cycles.tsv: phase 1.49–1.76 s only; design bound ≈ 20 s |
~~~

~~~markdown
| `roles/fig_r2…`–`fig_r4…` | R2–R4 | `make_roles_figs.py` | 紅檢 `slides930/roles-flowapi-redcheck*`（12/12） |
~~~
→
~~~markdown
| `roles/fig_r2…`–`fig_r4…` | R2–R4 | `make_roles_figs.py`（`--only` 可只畫一張） | 紅檢 `slides930/roles-flowapi-redcheck*`（12/12；v1.8 重跑 `…-20260929T0812Z.log` 相同）；r4 只畫 09-26 那次 07 的最後狀態、圖上不印 sha，它的停止條件 `slides930/make_roles_figs-redcheck-20260929T0810Z.log`（11/11，對照 2/2） |
~~~

~~~markdown
| `ndt-serve/fig_s2…`、`fig_s3…` | S2、S3 | `make_serve_s2_s4.py` | s3 的 old／new 列在 09-16 前背景帶；紅檢 `slides930/ndt-serve-s2s4-red-checks-r3-20260927T1948Z.log`（9/9）；S3 日期停止條件 `slides930/make_serve_s2_s4-s3date-redcheck-20260927T2003Z.log`（3/3） |
~~~
→
~~~markdown
| `ndt-serve/fig_s2…`、`fig_s3…` | S2、S3 | `make_serve_s2_s4.py`（`--only` 可只畫一張） | s3 的 old／new 列在 09-16 前背景帶；s2 的 up/down 列只畫最後狀態（OVS＝碼裡 rc 5、not run live），它的停止條件 `slides930/make_serve_s2_s4-redcheck-20260929T0811Z.log`（8/8，對照 4/4）；紅檢 `slides930/ndt-serve-s2s4-red-checks-r3-20260927T1948Z.log`（9/9；v1.8 重跑 `…-v18-20260929T0812Z.log` 9/9）；S3 日期停止條件 `slides930/make_serve_s2_s4-s3date-redcheck-20260927T2003Z.log`（3/3；v1.8 重跑 `…-20260929T0812Z.log` 3/3） |
~~~

**本檔**（v1.7 原文 → v1.8）

~~~markdown
| 16 | R4 ○ | figure | 每台交換機回報的 capabilities（`fig_r4`；sha 標 dirty） |
~~~
→
~~~markdown
| 16 | R4 ○ | figure | 每台交換機回報的 capabilities：09-26 那次 07 的兩個 package 各一列（`fig_r4`；v1.8 起只畫最後狀態、圖上不印 sha） |
~~~

~~~markdown
| 26 | S2 ○ | figure | ndt serve 的威脅與防線（跑過／讀碼分開）（`fig_s2`） |
~~~
→
~~~markdown
| 26 | S2 ○ | figure | ndt serve 的威脅與防線（跑過／讀碼分開）；別人 claim 下的 up：碼裡 P4 與 OVS 都 rc 5，live 只有 P4（`fig_s2`；v1.8 起只畫最後狀態） |
~~~

~~~markdown
| capabilities 各欄 | 🟢 兩次 07 的 `30_`、`71_switch_state_*.json` | 同上 |
~~~
→
~~~markdown
| capabilities 各欄（R4 圖） | 🟢 09-26 那次 07 的 `30_`、`71_switch_state_*.json` | `b2eeb71d +92`、kernel `be70b5dd32356847` |
~~~

~~~markdown
| P4 rc 5；OVS rc 0 | 🟢 `live-fixes…/a2/summary.json`、`a/summary.json` | ndt blob `3273df8b` |
~~~
→
~~~markdown
| P4 rc 5（live） | 🟢 `live-fixes…/a2/summary.json` | ndt blob `3273df8b` |
| OVS rc 5（碼裡；not run live） | 🟠 `tools/test_workflow/ndt:4362`（`68ace017` 加入）；`a/summary.json` 那一筆 rc 0 跑的是修法之前的 ndt，不上圖 | trunk `3368412d` |
~~~

**`generator/build_deck_930.js`**（v1.7 原文 → v1.8）

~~~js
// NDTwin progress report, 2026-09-30. Thirty-two pages (template v1.7, 2026-09-29).
~~~
→
~~~js
// NDTwin progress report, 2026-09-30. Thirty-two pages (template v1.8, 2026-09-29).
~~~

~~~js
fig("R4", "roles/fig_r4_capabilities", 2.318);
~~~
→
~~~js
fig("R4", "roles/fig_r4_capabilities", 2.563);
~~~

~~~js
    ["detection ≤ 20 s, guaranteed", "one watchdog phase sampled", "30_cycles.tsv; judge-HBW :73"],
~~~
→
~~~js
    ["detection ≤ 20 s, guaranteed", "one watchdog phase sampled", "30_cycles.tsv: phase 1.49–1.76 s only; design bound ≈ 20 s"],
~~~

**`figures/ndt-serve/fig_s2_security_model.md`**：被換掉的行（v1.7 原文，依出現順序；新文在該檔）

~~~markdown
其中五條在 **09-24（UTC）的真 lab** 上跑過（右欄綠／紅），**一條當場被打穿**：OVS 平面的 `ndt up`
在別人的 claim 底下照樣建起 fabric（rc 0）。ndt 在 09-25 12:23Z 補上（`68ace017`，**讀碼，沒有再跑過 live**）。
~~~

~~~markdown
| READ：up／down 由 ndt 自己擋 | `tools/test_workflow/ndt:996` `guard_up_lab_free`（rc 5＝拒絕）；P4 在 `:3313` 呼叫、OVS 在 `:4362` 呼叫；誰擋什麼的說明 `serve.py:381-384` | ndt 同上 HEAD；OVS 那一處由 `68ace017`（2026-09-25 12:23Z）併入 |
~~~

~~~markdown
| OBSERVED：別人的 claim 下 `up`（OVS） | `live-fixes…/a/summary.json` step `up-under-a-foreign-claim`：argv `ndt up 4`、`rc 0`、meaning「the fabric came up and verified」、8.5 s；`a/18-…http` 的 claim 行是外人的；fabric 在無人 claim 下活了約 29 秒（`doc/audit/2026-09-24_ndt-serve/REPORT.md:56-63`） | 同上 |
~~~

~~~markdown
- 外人 claim 下 `up`（OVS 4）⇒ **rc 0，fabric 建起來了**。這是當時 ndt 的缺陷，不是 ndt serve 的。
~~~

~~~markdown
- OVS 的 rc 5：`68ace017`（09-25 12:23Z）讓 `up_ovs` 呼叫 `guard_up_lab_free`（ndt:4362）。**我沒看到它在 lab 上被重打的 raw**
  （ticket `doc/audit/2026-09-25_ndt-ovs-claim/TICKET-ndt-ovs-claim.md:24` 把 live 交給 orchestrator，我沒去找）。
~~~

~~~markdown
- 右欄綠＝防線擋住了（值是 raw 裡的 HTTP 碼／rc 與 `error` 欄）；紅＝沒擋住；白框「not run live」＝沒有 live 證據，**不代表壞**。
- 「someone else's claim: up/down」那列右欄分兩半：P4 rc 5（擋住）、OVS rc 0（沒擋住）。中欄寫的是今天的碼：P4 與 09-25（UTC）起的 OVS 都由 ndt 回 rc 5。
~~~

~~~markdown
- **OVS 那格是 ndt 的洞，不是 ndt serve 的**：ndt serve 對 up/down 本來就交給 ndt 的 guard（serve.py:381-384）。
  09-24 的 ndt help 說 up 在 lab 被別人 claim 時回 5，只對 P4 成立（`doc/audit/2026-09-24_ndt-serve/REPORT.md:47`）。
  REPORT.md:6 的 09-26 補註已說明自 `68ace017` 起不再成立。
~~~

~~~markdown
- 對帳舊結果：09-24 REPORT §4 的表（`REPORT.md:180-188`）列的 live 證據與本圖右欄一致；本圖沒有推翻它，只把 09-25 的 OVS 修正（讀碼）放進中欄。
~~~

~~~markdown
- 避免說法：不要說「ndt serve 已經安全了」或「做過滲透測試」；只能說「八條防線在碼裡，五條在 09-24 的真 lab 上看過，其中 OVS 那條當時沒擋住、隔天在 ndt 修掉（讀碼）」。
~~~

~~~markdown
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_serve_s2_s4.py
~~~

~~~markdown
（一支產三張：`fig_s2_security_model`、`fig_s3_cells_and_walks`、`fig_s4_gui_plan`；最後一次的輸出在 `_raw/last-run.log`。）
~~~

~~~markdown
最後產出：2026-09-27T19:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_serve_s2_s4.py` sha256 `2f79ae137d352705…`（產圖之後腳本沒再改過）。
~~~

**`figures/roles/fig_r4_capabilities.md`**：v1.8 幾乎整份重寫，v1.7 全文如下

~~~markdown
# fig_r4_capabilities —— 每台交換機在 switch_state 裡報的能力旗標

[Co-developed with claude code -- Adam]

本檔所有日期與時間皆為 **UTC**（run 目錄名的 `…Z`；commit 時間以 `TZ=UTC git log` 換算）。

## 一句話

proxy 的 `GET /p4/switch_state` 每台交換機都帶一個 `capabilities` 物件（第一刀 `572d9462` 加的；這是裁決 ③「GUI 讀一次能力旗標」的資料源）。同一支 tutorials basic，宣告 roles 與不宣告 roles 各跑一次，兩天各一次：roles 那包 `ipv4_route` 是 `ndtwin`（NDTwin 能寫路由），不宣告的是 `unbound`；09-24 時鏈路只能「宣告」（`declared`、`reroute false`），09-26 心跳上線後 `link_discovery` 變成 `heartbeat`，而 `reroute` 只在 roles 那包變成 `true`——沒有 roles 的只偵測、不改路。五元組兩包都是 `false`。每一列都是 4 台交換機回報完全相同的值（4 of 4）。

## 資料來源

L＝`/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs`。

| 用途 | 檔（JSON key） | commit／binary |
|---|---|---|
| basic＋roles，09-24 | `L/2026-09-24T160256Z_07_roles_basic/30_switch_state_roles.json` `switches.{1..4}.capabilities` | repo HEAD `572d9462`、kernel `be70b5dd32356847`（同 run `01_binaries.txt`） |
| basic＋roles，09-26 | `L/2026-09-26T202055Z_07_roles_basic/30_switch_state_roles.json` `switches.{1..4}.capabilities` | repo HEAD `b2eeb71d`、kernel `be70b5dd32356847` |
| basic 無 roles，09-24 | `L/2026-09-24T160256Z_07_roles_basic/71_switch_state_plain.json` 同 key | `572d9462` |
| basic 無 roles，09-26 | `L/2026-09-26T202055Z_07_roles_basic/71_switch_state_plain.json` 同 key | `b2eeb71d` |
| 「4 of 4」 | 同上四檔：`switches` 有 4 台、`capabilities` 序列化後只有 1 種值（腳本斷言） | — |
| 欄位的語意 | `K/p4_proxy/proxy_agent/main.py:1151`（`capabilities_for`）、`:1205`（`capabilities_report`）；規格 `K/doc/audit/2026-09-24_p4-driven-api-shape/TICKET-P4-roles.md` §2.5-2、附錄 A | trunk `3d740be0`（READ；main.py 與 `b2eeb71d` 版 sha256 相同 `54c9bd96c181b0dd`） |

## 可信度

**OBSERVED（跑過，JSON）**
- 四列的五個欄位值如圖；每列 4 台相同。
- 09-26 兩包的頂層 `reroute`：roles 那包 `available: true`、`reason: null`；無 roles 那包 `available: false`、`reason: "unbound"`（`30_…json`、`71_…json` 的 `reroute` key）。09-24 的檔沒有頂層 `reroute`、`heartbeat` 這兩個 key（段 W 之前）。
- 這些值同時也是 07 的 L6 判定（07 log 的 `L6 capabilities` 行；見 `fig_r3`）。

**READ（讀碼，沒執行）**
- `reroute` 是整個 fabric 的事實、逐台回報；在宣告鏈路的 fabric 上，`reroute` 與 `link_discovery` 每次請求依 watchdog 最後讀到的心跳重算（`main.py:1205-1212` docstring：心跳一停，`reroute` 在一次讀取內變 false）。
- 附錄 A 規定：kernel `get_graph_data` 的節點將來原樣抄這個物件；**沒有 `capabilities` ⇒ 一切視為支援**（OVS、舊 kernel）。

**INFERRED**
- 顏色是我依附錄 A 的語意分的：綠＝這台做得到（`ndtwin`、`true`、`heartbeat`）、灰＝做不到（`unbound`、`false`、`declared`）、白＝`binding_source` 只說綁定從哪來，不是能力。

## 圖怎麼讀

上兩列是宣告了 `roles.ipv4_route` 的 basic，下兩列是同一支程式不宣告 roles；每組上列 09-24、下列 09-26。欄位名照 JSON 原樣（等寬字）。09-24→09-26 變綠的格子就是心跳帶來的：兩包的 `link_discovery`，以及只有 roles 那包的 `reroute`。

## 已知但書

- 🔴 這是 **proxy** 報的。09-28 起 kernel 的 `get_graph_data` 節點也帶這個欄位（第三刀 kernel 側，merge `85bec430`，03:41Z；PR #14 的 CI 四個 job 全綠、ctest 1385/1385，`K/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926/ci-compare-pr14.txt:1-2`）；GUI 還沒讀它——「GUI 會變灰」目前只存在於 `~/Web-GUI` 的本機草稿分支（`draft/p4-capabilities-0924`）。本圖的內容（兩次 07 的 switch_state）沒有變，PNG 不動。
- `five_tuple` 在外來程式上一律 `false`：第一刀沒有五元組的 role，外來交換機上的五元組寫入一律 501（`route_binding.py:75` `REASON_NO_FIVE_TUPLE_ROLE`）。
- `ipv4_route: ndtwin` 只代表「目的 IP 路由表這一張」；不要說成「NDTwin 能操作外來 P4 程式」。
- 09-26 的值要心跳在跑才成立。07 在 `ndt up` 後輪詢 switch_state：前兩次（約 4 s）`links` 仍全是 `source: declared`，第 3 次才全是 `heartbeat`（`30_switch_state_roles.json.polls`、`71_switch_state_plain.json.polls`）；圖上的值取自輪詢結束時存下的那一份。輪詢檢查的是 `links`，前兩次的 `capabilities` 長什麼樣沒有存。
- external 控制面的 fabric（p4runtime、flowcache）不在這張圖裡；那裡 `ndt up` 不起心跳（08 H4）。
- raw 在 trunk 未提交（`runs/`），已鏡射到本機 `audit-raw` 分支 `36f8dd8d`，blob 相同（2026-09-27 17:2xZ integrator 再比：`36f8dd8d` 是 audit-raw `797c34ab` 的祖先，引用的 run 目錄在 `797c34ab` 逐檔 blob 與工作樹相同；`797c34ab` 依 coordinator 已公開在兩個 P4 repo）。
- 🔴 **兩次 07 都跑在 dirty checkout 上**：`ndt status` 的 code 行（各 run 的 `00_status_before.txt:7`）是 `572d9462  +61 file(s) with uncommitted changes`（09-24）與 `b2eeb71d  +92 file(s) with uncommitted changes`（09-26），其中點名兩個可能改變行為的：`p4_proxy/mininet/host_count_override`（值 4）與 `tools/remote-lab/dorm_lab/`。sha 只說 HEAD，不代表 run 的整棵樹；本頁用到的六個 proxy／工具原始檔另有 sha256（`01_binaries.txt`）。 圖上的 sha 因此標成「· dirty」（腳本從 `00_status_before.txt` 讀出並斷言 +61／+92）。
- 產生器斷言的紅燈檢查：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/roles-flowapi-redcheck.py`，紀錄 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/roles-flowapi-redcheck-20260927T1704Z.log`（12 個變異全因指名的原因中止、2 個對照通過；第一版在 `…/roles-flowapi-redcheck.first-20260927T1606Z.log`）。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/roles"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_roles_figs.py
```

最後產出：2026-09-27T17:05Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_roles_figs.py` sha256 `280b76fbbdf34135…`（產圖之後腳本沒再改過）。
~~~
