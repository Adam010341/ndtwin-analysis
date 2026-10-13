# NDTwin 進度報告簡報 — 2026-09-30 版・資訊模板

**v1.2（2026-09-27 19:0xZ，判官第二輪之後；第三輪修訂 19:5xZ）；v1.3＝09-28 07:xxZ 狀態更新（README §9）；v1.4＝判官（READY AFTER FIXES）之後的修正（README §10）；**v1.5＝09-28 09:0xZ 重新釘住（README §11）**：Q3、Q4、Q5 釘在 trunk `3368412d`、main `eef173a9` 與公開 API 08:53Z 的快照；F1 釘在 trunk `3368412d` 與 08:38Z 的未認證公開查核；N1 釘在 trunk `3368412d`（commit 時間 07:45Z）；T1 讀 GAP-2b（Adam 09-28 裁定四格、提交為 `c8433963` 的那一版，已公開）；各圖的 as-of 標在圖上。在審那一項 PR #15 已 squash 進 main，中性磚規則解除（coordinator 裁定 D）。v1.6＝09-28 13:2xZ：F1 的在審加一條（README §12）。delta only，切點 2026-09-16。時間一律 UTC。** 本檔是唯一事實來源；產檔由 Adam 自己的 session 跑產生器（本機無 Node、無 LibreOffice，這裡不產 pptx）。
v1.1 依 `K/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926/slides930/judge-SLIDES930.md`（FIX：F-1…F-21）與 coordinator 的裁決改過；
v1.2 依同目錄 `judge-SLIDES930-r2.md`（READY AFTER FIXES）與 coordinator 第二輪的 18 項改過，第三輪依 `judge-SLIDES930-r3.md` 與 coordinator 的 12 項再修。逐頁改了什麼在 `README-930.md` §6（第一輪）、§7（第二輪）、§8（第三輪）。
圖全在同目錄 `figures/<主題>/`，每張都有同名 `.md`（出處 path:line、commit／binary、髒 checkout、可信度、紅檢、重生指令）與產生器。
總清單、每一頁一行、每個數字的出處、被拿掉的頁：`README-930.md`。修法清單正本：`FIXED-SINCE-916.md`。

**v1.7＝2026-09-29（Adam 09-29 的四條指示）**：拿掉 A1、A2（逐日進度，兩頁重複）、T2（逐輪史）、Q1–Q5（開發流程與 CI 史）、F1（修法看板）；開場後新增背景段 **B1–B5**（13 支 exercise 各在做什麼、basic 與 basic_tunnel 細講、09-16 的 NDTwin 為了接這些 exercise 缺什麼、最後用什麼辦法補上），T3 移到 B5 之後；N3 拿掉只因被拿掉的頁而存在的兩列（CI），改寫「使用者已經拿到」那一列；留下各頁的講者備註刪掉開發過程的敘述，保留出處與界定宣稱的但書。36 → 32 頁。拿掉的頁的講稿、§3 的列，以及留下的頁被刪掉的句子，原樣存在 `README-930.md` §13。v1.7 的 pptx 在本機以 conda 環境 `webgui-node` 的 node 產（§1b）；PDF 沒有重產（本機沒有 LibreOffice），資料夾裡的 PDF 仍是 09-28 的 36 頁版。

**v1.8＝2026-09-29**：R4、S2 兩張圖只畫最後狀態（R4＝09-26 live 07 兩個 package 各一列、圖上不印 sha；S2 的 OVS 半格＝碼裡 rc 5、not run live），N3 第 4 列證據改成 `30_cycles.tsv` 與設計上界，H4 講稿拿掉輪次字樣；pptx 重產（§1c），PDF 仍是 09-28 版；被換掉的字逐字在 `README-930.md` §13.7。

[Co-developed with claude code -- Adam]

## 0. 規則（全部常設）

1. **delta only，切點 2026-09-16**：只講 09-16 報告之後的事；916 講過的不重講、不提（已逐頁對過 `NDTwin_deck_916.pdf` 與 916 模板 §1a）。
   舊證據只能當**背景**：圖上放進灰底帶、標「BEFORE 09-16 · BACKGROUND」與日期（`fig_d1` 的 OVS 09-03、NDTwin 自己 P4 08-24 兩列）或畫成空心灰點並標「not run」（`fig_o2` 的 09-08；該圖 09-29 起只留存檔）；講者備註也要說。
   916 的 13×16 需求矩陣不重放（T1 已重切成 `fig_t1c`）；T1 保留的「NDTwin 09-16」那一列就是 916 的那一列，所以也放進灰底背景帶，標「as shown 09-16; read 09-08, trunk 1a284f75」。
   - 🆕 **B 段（背景）不受本條限制**（Adam 2026-09-29 裁）：教授不需要開發史與除錯史，只要技術決策與最後結果；開場先講 13 支 exercise 大概在做什麼、挑一兩支細講、09-16 的 NDTwin 為了接這些 exercise 缺什麼、最後用什麼辦法補上。B 頁講 exercise 本身、09-16 的狀態與做了的決定，所以 09-16 之前的東西可以講、不放背景帶；B 頁上跑過的數字仍照規則 5 標（B5 的 ran live 欄）。其他段照舊 delta only。
   背景帶蓋的是「09-16 報告之前就有的證據」，不論跑過還是讀碼（`fig_d1` 的舊 live 格、`fig_t1c` 的 09-16 讀碼列、`fig_s3` 的 09-10／09-11 old／new 兩列）；同一列若有讀**今天**的碼的格子（`fig_d1` 右表，trunk `3d740be0`），那些格子不進帶子。
2. 🔴 **每一頁只有一張圖或一張表**（Adam，2026-09-27 UTC）：沒有 bullet、沒有段落、沒有 caption／kicker／chip／判詞。
   開場、問教授的問題、誠實頁、下一步都一樣——問題與限制做成**表**、下一步做成**路線圖**。
   **頁標題是投影片上唯一的自由文字**；表格的格子短（名目 → 值），不寫句子。頁首小標也不放。
   需要「狀態」的頁（R1、S4）是**表格頁**（B1、B4、B5 也是表格頁）：格子寫「做到哪個範圍」與出處，不寫判詞；原本的卡片圖留在資料夾當存檔、不上 deck。
   每頁在 §1 有 **form:**（title／figure／table）。
3. **圖頁**＝一張圖撐滿內容區。每張圖畫布左上角已經有自己的標題（≤45 字元），**頁標題就是那一行**，產檔時不要再疊一個（916 的做法）。
4. **圖上字少**：只有標題、軸、數值標籤、方塊名、面板標題、少數關鍵註記。推導、但書、方法全在圖的 `.md` 與 §2 的講者備註。
5. **證據紀律**：每個實測數字標 commit／binary 與 raw 路徑。🟢**跑過（OBSERVED）**、🟠**讀碼或讀文件、未執行（READ）**、**推論（INFERRED）**不在同一張表、同一句混寫；
   圖上若兩者並陳，分成兩個標題分明的面板（`fig_t1c`、`fig_d1`、`fig_s2`、`fig_s3`、`fig_r2`、`fig_t9` 的 RAN IT／READ THE CODE）。
   - 🔴 live raw（`live-p1/runs/`、`runs/`、`scratch/`、`telemetry/raw/`）在 kernel trunk 上**不進版控**（`.gitignore` 擋）。本 deck 引用的 raw **幾乎都在 audit-raw `797c34ab`**
     （coordinator 推；依 coordinator，兩個 P4 repo 的 `audit-raw` 都公開是它）：integrator 2026-09-27 17:2xZ 以 `git rev-parse 797c34ab:<path>` 對 `git hash-object` 逐檔比過
     T06、兩次 07、兩次 08、spike 四輪、06 各完整輪、第五次 telemetry campaign 與判別輪、h14／h5b／07 的 log——blob 全同。
     09-19 早上三個開發輪（052518Z、063235Z、083257Z）與它們的 arm report 在 **audit-raw `5cf0364c`**（`797c34ab` 的後代；coordinator 以未認證 `git ls-remote` 核過兩個 P4 repo 公開；
     integrator 本機比對三個 run 目錄各 27 檔、arm report 403 檔，blob 全同）。**不在 audit-raw、只在本機工作樹**：`2026-09-19T052251Z_05` 與部分判官檔（`FIXED-SINCE-916.md` §0 列名）。
   - 🔴 **GAP-2b**（T1、T7、N3 引用它）：四個判斷格 2026-09-28 由 Adam 照建議值裁定（flowcache 的 twin＝IPv4 only），coordinator 讀 diff 後提交為 `c8433963`（07:15Z；08:19Z 未認證查已在公開 trunk 上）。本版讀的內容：sha256 `77afc4d5f4747351…`＝提交的那份（裁定前是 `0cf8a6d8…`）。
   - 🔴 **每一次 live run 都跑在髒 checkout 上**：arm report 或 `00_status_before.txt` 的 `code <sha> +N file(s) with uncommitted changes`（本 deck 引用的 run 是 +60 到 +95；09-29 拿掉的 F1、A2、T2 引用過 +29、+47），
     其中 2–3 個檔會改變行為（`p4_proxy/mininet/host_count_override`、`tools/remote-lab/dorm_lab/`；T06 另有 `app_package_override`）。
     v1.8 起沒有一張上 deck 的圖印 run 的 sha（原本唯一印的 `fig_r4` 改成只畫最後狀態）；run 的 sha 只在 `.md` 與講者備註，出現時帶 +N。圖上若要印，寫「<sha> · dirty」。
6. **不寫會議／期刊名，不提私有 repo**。標題 ≤45 字元（下表每一頁都核過；H2 恰 45）。
7. **模板精簡格式**：頁序（§1）、逐頁講者備註（§2）、出處速查（§3）、圖清單（§4）。
8. 🔴 **講者備註必守（guard，也寫在各頁）**：
   - ❌ 把 protobuf 5 切換（2026-09-27，`5dc7fc9a`）前後的效能數字放同一張圖。本 deck 沒有任何跨切換的效能數字。
   - ❌「修在 trunk 就是使用者拿得到」（手冊叫人 clone 的 P4-public 停在 09-03 `9e6cc307`，`FIXED-SINCE-916.md` §8–§9）。
   - ❌「CI 綠就是在 lab 上驗過」：hosted runner 上沒有 switch、沒有編好的 P4、沒有 Ryu，需要它們的項目在那裡跳過（`.github/workflows/ci.yml:130-138`）。
   - ❌「NDTwin 能操作外來 P4 程式」——Adam 2026-09-25 裁（orchestrator 記憶檔，非 repo）：第二刀做完之前**不對外**這樣說，第二刀之後的說法留待再裁。external 控制面的 detect-only 在分支上、未併，**不上圖、不上台描述**（N1、N3 已拿掉；含它的 N1 留作存檔 `fig_n1_roadmap_with_detect_only.*`；Adam 09-28：併入前不放回）。**實驗室內部會議要不要說由 Adam 決定**。能講的是「13 支在 NDTwin fabric 上**跑起來**、兩臂照預期」「NDTwin 能寫宣告了 roles 的**那一張目的路由表**」。
   - ❌ 自訂標頭的 exercise「NDTwin 觀測得到它們」——只能說「**轉得動（forward）**」；twin 看得見它們自己的幀，只有 p4runtime 的 0x1212 有位元組證據。
   - ❌「遙測把 pps 天花板壓低 N 倍」，也不給任何一對 pps 數字——這台機器量不出來（raw：`K/doc/audit/2026-09-19_telemetry-three-groups/raw/2026-09-19T130352Z_G2/G2/cooperative_f64_a.log:8`、`:15`、`:17`；見 M1）。
   - ❌「CI 一直是綠的」：PR #12–#14、#16、#17 與 ndtwin-lab trunk 從 `8d622ea4` 到 `3368412d` 的 run，四個 job 全綠（每個 run 的最後一次）；不是每一次都綠——一個不穩定的 shell 檢查（`test_apps_residue.sh`）讓 Adam010341 trunk `f253ed08` 的一次、PR #15 五次 GCC 裡的三次變紅，重跑後綠。見 Q4。
   - 權限缺陷那一項：一句「cleanup 路徑的權限缺陷，審查抓到，已修（#15）」；不描述機制、不給攻擊步驟。
9. **視覺**沿用 827 §E2 色票與 916 的圖風格（matplotlib 3.11.1、Liberation Sans）。本機沒有 Node，dataviz 的色盤驗證腳本沒跑；兩組類別色另有形狀第二編碼（`fig_m1` 圓／方、`fig_h2` 圓／方）；`fig_f1` 的五色層另以本機 python 算過 CVD 距離（更正：有磚的四色兩兩 ≥ 14.6；tests `#E6E9EC` 對 docs `#FFFFFF` 只有 6.6–6.8，docs 本窗 0 格、只在圖例——`K/scratch/overnight-2026-09-05/logs/slides930/cvd_layer_fills.log:10`、`cvd_layer_fills-r2-20260927T1835Z.log`）。
10. **紅檢**（竄改輸入 → 腳本停下、印出**它自己的**原因；對照組綠；只看 rc≠0 不算）。腳本與 log 在 `K/scratch/overnight-2026-09-05/logs/slides930/`（git-ignored）。紅檢輪（2026-09-27 20:00–20:20Z）、修正輪（20:28–20:50Z）、API 欄位輪（20:50–21:00Z）、09-28 的狀態更新（06:30–06:57Z）與判官修正輪（08:0x–08:xxZ）的 log 列在這裡與 README §1、§9、§10；改過的圖在自己的 `.md` 最後產出行引用。範圍照實寫：**18 支腳本都有紅檢**（09-29 加 `make_background_figs.py`；09-29 拿掉的頁的腳本仍在碟上、紅檢不變，它們的圖只留存檔）。
    - **09-29**：`make_background_figs.py`（B2、B3）81 個竄改 81/81 以它自己的具名理由停、對照組綠；2 個停止點任何輸入都到不了，理由逐條在 log（`make_background_figs-redcheck-20260929T0740Z.log`）。B1、B4、B5 三張表的每個可查的事實另由 `b-section-sources-check.py` 對來源核過（`b-section-sources-20260929T0741Z.log`，0 CHECK-FAIL）。
    - **09-29 v1.8**（R4、S2 只畫最後狀態，兩支產生器加 `--only`，只重畫這兩張）：`make_roles_figs.py` 新增與改過的 `fig_r4` 停止條件 11/11 以它自己的具名理由停、對照組 2/2（`make_roles_figs-redcheck-20260929T0810Z.log`）；`make_serve_s2_s4.py` 新增的 `fig_s2` 停止條件 8/8、對照組 4/4（`make_serve_s2_s4-redcheck-20260929T0811Z.log`）。舊 harness 對改過的產生器重跑：`roles-flowapi-redcheck-20260929T0812Z.log`（12/12）、`ndt-serve-s2s4-red-checks-v18-20260929T0812Z.log`（9/9）、`make_serve_s2_s4-s3date-redcheck-20260929T0812Z.log`（3/3），對照組都綠。
    - **逐一停止條件看過紅**（log `<腳本>-redcheck-<UTC>.log`）：`make_coverage_0930.py`（T1，12/12，`t1c-coverage-redcheck-repin-20260928T0847Z.log`；裁定那一跑 `…-ruling-20260928T0654Z.log`；09-27 版 11/11 在 `…-r3-20260927T1943Z.log`）、`make_sampling_error_fig.py`（M1，6 個停止條件、7 個竄改，`m1-sampling-error-redcheck-r2b-20260927T1854Z.log`）、
      `make_tutorial_figs_0927.py`（59 個停止點、69 個竄改 69/69；另 7 個停止點任何輸入都到不了，理由逐條在 log，`T20260928T0847Z`）、`make_engineering_figs.py`（五張圖 133 個停止點：130 個看過紅、181 個竄改 181/181、對照組 4/4、harness 自檢 4/4；3 個到不了，`T20260928T0857Z`）、
      `make_heartbeat_figs.py`（9/9，`T2000Z`）、`make_heartbeat_extra_figs.py`（圖底以外 12/12，`T2001Z`；圖底 5 個竄改，`h0-footer-redcheck-20260927T1941Z.log`）、`make_arms_grid.py`（6/6，`T2001Z`）、
      `make_foreign_p4_diagram.py`（2/2，`T2005Z`）、`make_roadmap.py`（5/5，git 的回答用模擬，`T20260928T0847Z`；09-27 版 3/3）、`make_flow_api_matrix.py`（15/15，`T2003Z`）、
      `make_serve_s2_s4.py` 為 S3 背景帶加的日期停止條件（3/3，`make_serve_s2_s4-s3date-redcheck-20260927T2003Z.log`）。
    - `make_serve_diagram.py` 只有**一個合併的**停止條件（5 個錨點缺任一個就停，但不說缺哪個）：5 個竄改 5/5（`T2002Z`）；維持原樣（coordinator 裁）。
    - **修正輪**（coordinator 裁）：紅檢輪探針找到的三類問題都已改成具名停止條件，各有紅檢（`regen-check-fixround-20260927T2054Z.log`，當時 14 張 PNG 逐位元相同）。
      ① Q4：compare 記錄存在、但第一行不再寫出那兩個 run 的四個 job 結果，就停；只有記錄不存在才畫「no record」。
      ② GAP-1 §2 的子表裡同一支 exercise 出現兩次、或少了某一支，就停。
      ③ 原本是未具名 Python 例外的解析失敗改成具名停止條件（regex 取值、CI log 查找、T06 flowcache 列、開檔、API 快照的每個欄位、`codes.txt` 每一行）。
      還會以未具名例外停下的（探針實測，rc≠0、不出圖）：`make_tutorial_figs_0927.py`（T1 也 import）遇到表格列的格數少於它讀的那一欄，或 T06 的 rc 欄不是整數（`make_tutorial_figs_0927-probe-remaining-20260927T2055Z.log`）；`make_engineering_figs.py` 沒有檢查 git 自己的輸出格式。
    - **09-28 狀態更新**（README §9）：Q4／Q5／N1／F1／T1／t1b 的產生器又改了（新停止條件都有紅檢，數字見上）；F1 18/18。判官修正輪（08:0x–08:2xZ，README §10）：Q4 的產生器與紅檢又改了（`T20260928T0809Z`）；F1 在最後一次改 `FIXED-SINCE-916.md` 之後重跑，`mutation_check_fixed_since_916.judgefix-20260928T0826Z.log`（18/18，檔頭記產生器、harness 與清單的 sha256，檔尾 rc=0）。 重新釘住（README §11）：engineering、roadmap、F1 的產生器又改了（`T20260928T0857Z`、`T20260928T0847Z`；F1 拿掉中性標題與它的停止條件，跟著拿掉的變異 7 個、改瞄準的 2 個，`mutation_check_fixed_since_916.repin-20260928T0905Z.log` 13/13）。
    - **變異自檢**：`make_fixed_since_916.py`（F1，13/13，`mutation_check_fixed_since_916.repin-20260928T0905Z.log`；判官修正輪的 18/18 在 `…judgefix-20260928T0826Z.log`；09-28 更新時的 `…refresh-20260928T0634Z.log`；09-27 的 17 個與「位置」停止條件拿掉時 6 個存活的那一跑在 `…r3b-20260927T1952Z.log`、`…without-placement-stop-20260927T1934Z.log`）、
      `make_overview_figs.py`＋`make_exercise_path_figs.py`（14/14，`o1-o2-t6-t9/run_mutations-r3-20260927T1948Z.log`）、`make_roles_figs.py`＋`make_queued_readback.py`（12/12，`roles-flowapi-redcheck-20260927T1704Z.log`）、
      `make_serve_s2_s4.py`（9/9，`ndt-serve-s2s4-red-checks-r3-20260927T1948Z.log`）。
## 1. 頁序（32 頁；`✅` 建議核心、`○` 可略，最終取捨 Adam 定；v1.7，2026-09-29）

| 段 | # | 頁 | 標題（＝圖上標題） | form | 圖檔（`figures/…`）或表 |
|---|---|---|---|---|---|
| **A 開場** | 1 | ✅ A0 | NDTwin progress · 2026-09-30 | title | — |
| **B 背景**（不受 delta only 限制） | 2 | ✅ B1 | The 13 P4 tutorial exercises | table | §2 B1 表 |
| | 3 | ✅ B2 | basic: one packet through the program | figure | `background/fig_b2_basic_walkthrough`（新） |
| | 4 | ✅ B3 | basic_tunnel: its own header, its own table | figure | `background/fig_b3_basic_tunnel`（新） |
| | 5 | ✅ B4 | What the 09-16 NDTwin lacked for them | table | §2 B4 表 |
| | 6 | ✅ B5 | How each gap was bridged | table | §2 B5 表 |
| **T P4 tutorial 上 NDTwin** | 7 | ✅ T3 | How a foreign P4 program runs on NDTwin | figure | `foreign-p4/fig_a1_foreign_p4_path`（B5 的機制怎麼一起跑） |
| | 8 | ✅ T1 | What NDTwin covered: 09-16 vs 09-27 | figure | `p4-tutorials/fig_t1c_ndtwin_coverage`（09-16 列在背景帶；四個判斷格 09-28 Adam 已裁定） |
| | 9 | ○ T4 | multicast, end to end on the NDTwin fabric | figure | `p4-tutorials/fig_t6_multicast_end_to_end`（T3 的一個實例） |
| | 10 | ✅ T5 | What pre-flight checks before ndt up | figure | `p4-tutorials/fig_t7_preflight_checks` |
| | 11 | ○ T6 | What the exercise brings, what convert adds | figure | `p4-tutorials/fig_t8_what_you_bring`（與 B5 第 1 列重疊） |
| | 12 | ✅ T7 | Seven custom-header exercises forward | figure | `p4-tutorials/fig_t9_custom_headers` |
| **R 外來 P4 的 API 形狀（第一刀）** | 13 | ✅ R1 | Four rulings on the P4 API shape (09-24) | table | §2 R1 表（`roles/fig_r1_four_rulings` 只留存檔） |
| | 14 | ✅ R2 | roles.ipv4_route: from package to table | figure | `roles/fig_r2_roles_path` |
| | 15 | ✅ R3 | Live 07: roles on basic, run twice | figure | `roles/fig_r3_live07` |
| | 16 | ○ R4 | What each switch reports: capabilities | figure | `roles/fig_r4_capabilities` |
| **H 第二刀：心跳** | 17 | ✅ H1 | Why link discovery stops at a foreign P4 | figure | `heartbeat/fig_h0_why_not_lldp` |
| | 18 | ✅ H2 | The veth heartbeat, from wire to kernel graph | figure | `heartbeat/fig_h0b_heartbeat_path` |
| | 19 | ✅ H3 | One cut, one restore — on the kernel graph | figure | `heartbeat/fig_h1_one_cut_cycle` |
| | 20 | ✅ H4 | Detection time: 7 live cuts | figure | `heartbeat/fig_h2_detect_vs_phase` |
| | 21 | ✅ H5 | The detection bound, piece by piece | figure | `heartbeat/fig_h3_upper_bound` |
| | 22 | ✅ H6 | Heartbeat on, forwarding unchanged | figure | `heartbeat/fig_h4_forwarding_unchanged` |
| **D 執行期改規則** | 23 | ✅ D1 | Changing rules at runtime, per data plane | figure | `flow-api/fig_d1_flow_api_matrix` |
| | 24 | ✅ D2 | "queued" is not "installed": read it back | figure | `flow-api/fig_d2_queued_readback` |
| **S ndt serve** | 25 | ✅ S1 | ndt serve: one local door to the lab | figure | `ndt-serve/fig_s1_serve_path` |
| | 26 | ○ S2 | ndt serve: threats and defenses | figure | `ndt-serve/fig_s2_security_model` |
| | 27 | ✅ S3 | Live cells: two guided walks, 09-24 | figure | `ndt-serve/fig_s3_cells_and_walks` |
| | 28 | ✅ S4 | Where the ndt serve page goes | table | §2 S4 表（`ndt-serve/fig_s4_gui_plan` 只留存檔） |
| **M 遙測比較** | 29 | ✅ M1 | Sampling error of two telemetry paths | figure | `telemetry/fig_m1_sampling_error` |
| **N 收尾** | 30 | ✅ N1 | The road to “bring your own .p4” | figure | `next/fig_n1_roadmap` |
| | 31 | ✅ N2 | Open questions | table | §2 N2 |
| | 32 | ✅ N3 | What we do not claim | table | §2 N3 |

✅ 28 頁、○ 4 頁（T4、T6、R4、S2）。form：title 1（A0）、table 7（B1、B4、B5、R1、S4、N2、N3）、figure 24。
**敘事**：開場（A0）→ 背景（B：exercise 在做什麼、細看兩支、09-16 的 NDTwin 缺什麼、怎麼補）→ 補上之後怎麼一起跑（T3）與結果（T）→ NDTwin 怎麼寫它的表（R）與偵測斷線（H）→ 執行期規則（D）→ 工具（S）→ 遙測（M）→ 下一步與限制（N）。
頁 ID 沿用 v1.6（T3 排在 T1 前面，但 ID 不改：各圖 `.md` 與 README 用 ID 互相引用）。
**2026-09-29 拿掉的頁**（Adam：教授不需要開發史與除錯史）：A1 `fig_o1_since_0916`、A2 `fig_o2_thirteen`、T2 `fig_t5_arms_by_run`、Q1 `fig_q1_protobuf5`、Q2 `fig_q2_review_path`、Q3 表、Q4 `fig_q4_ci_state`、Q5 `fig_q5_main_by_pr`、F1 `fig_f1_fixed_since_916`；圖都留在碟上、列入 §4 的存檔清單，講稿原樣在 `README-930.md` §13。
09-30 前要重跑的（shas 會過期）：`fig_n1`，以及 S4 表的 v2 狀態（腳本會在狀態變了時停下，逼人更新）。

## 1a. 產檔紀錄（2026-09-28，cowork session）

- 產生器 `generator/build_deck_930.js`（沿用 903 `deck_style.js`）→ `NDTwin_deck_930.pptx`／`.pdf`，**36 頁，§1 全部 ✅＋○**，頁序與 §1 相同。
- 圖：35 張在碟上＝30 張上 deck（`_hires/` 500 dpi）＋5 張 §4 列的只留存檔；產生器對「沒用也不在存檔清單」的圖會停下（0 張）。
- 規則 2 的落實：沒有 section tab、kicker、caption；圖頁不加頁標題（圖上有），圖撐滿 0.28–7.00 in、寬 ≤12.9 in；表頁＝§1 標題（sentence case、30 pt）＋表；只留頁碼。標題頁只有標題與「Adam」。
- 表的字級：R1 15、S4 18、Q3 18、N2 16、N3 14（9 列，是最密的一頁）。表格內文逐字照 §2。
- 講者備註：產生器在產檔時把 §2 各頁的內容原樣放進 pptx notes——§2 改了就重跑，不用手抄。
- 圖沒有重畫：30 張在全頁尺寸下字都讀得到（逐頁看過 render）。

## 1b. 產檔紀錄（2026-09-29）

- 產生器 `generator/build_deck_930.js`（v1.7：B 段五頁、T3 移到 B5 之後、A1／A2／T2／Q1–Q5／F1 拿掉、N3 七列、存檔清單 13 張、頁數斷言 32）以 `conda run -n webgui-node node`（node v22.23.2）跑；`pptxgenjs` 4.0.1 用的是 09-28 那次產檔所用的同一份 `node_modules`（cowork session 的 outputs 目錄，經 `NODE_PATH` 指過去；沒有下載、沒有安裝任何東西）。執行輸出：`figures: 37 on disk / 24 used / 13 archive-only / 0 unaccounted`、`done — 32 pages`。
- `NDTwin_deck_930.pptx` 在 2026-09-29 07:52Z 重產（sha256 `ead0f033b1daec98…`；09-28 那份是 `4c7f862b3f984b48…`）。講者備註仍由產生器在產檔時從本檔 §2 原樣取用。
- 驗證（`K/scratch/overnight-2026-09-05/logs/slides930/verify-deck-930.py`，log `verify-deck-930-20260929T0757Z.log`；它記下所核對的 §1 頁序＋§2 講稿的 sha256 `e66ee4b81038042f…`，§1b 之後再改不影響這兩段）：32 頁依 §1 的順序；每頁的 notes 等於 §2 那一段；24 個圖頁各只有一張圖，位元組與 `figures/<主題>/_hires/<stem>.png` 相同、長寬比相符，頁上除頁碼外沒有別的字；7 個表頁的表逐格等於 §2 的表、標題等於 §1——0 FAIL。陰性對照：同一支腳本對 09-28 的 36 頁 deck 報 64 FAIL（`verify-deck-930-negcontrol-v1.6deck-20260929T0753Z.log`）。
- 沒有 render（本機沒有 LibreOffice）：表格高度用比 Calibri 寬的 Liberation Sans 字寬估，B1、B4、B5、N3 的表底約在 6.54、6.60、6.64、6.36 in（頁碼在 6.92 in）；新的兩張圖在全頁尺寸下的字級與既有的圖相同（10–14 pt 級）。
- 🔴 **`NDTwin_deck_930.pdf` 沒有重產，仍是 09-28 的 36 頁版本**（sha256 `e89ec9b8ec3f05f7…`）：本機沒有 LibreOffice。PDF 要在有 LibreOffice 的環境從新的 pptx 重轉。

## 1c. 產檔紀錄（2026-09-29，v1.8）

- 圖：只重畫 `roles/fig_r4_capabilities`、`ndt-serve/fig_s2_security_model`（兩支產生器的 `--only`；`K/scratch/overnight-2026-09-05/logs/slides930/regen-v18-roles-20260929T0812Z.log`、`regen-v18-serve-20260929T0812Z.log`，rc 0）；兩個資料夾其餘 23 個檔（PNG、SVG、`_hires`，以及 r1–r3、s3、s4 的 PDF）與改前 sha256 相同。R4 畫布改成 13.33 × 5.2 in（a/r 2.563，原 2.318），產生器的 `fig("R4", …)` 跟著改；S2 畫布大小不變。
- `NDTwin_deck_930.pptx` 在 2026-09-29 08:18Z 重產，方法同 §1b（`conda run -n webgui-node node`，node v22.23.2；`NODE_PATH` 指向同一份 cowork `outputs/node_modules`；沒有下載、沒有安裝）：`figures: 37 on disk / 24 used / 13 archive-only / 0 unaccounted`、`done — 32 pages`；sha256 `ee1dc54c1dd851d9…`（v1.7 那份 `ead0f033b1daec98…` 備份在 `slides930/v18-0929-bak/`）；紀錄 `slides930/build-deck-v18-20260929T0818Z.log`。
- 驗證：同一支 `verify-deck-930.py` → `verify-deck-930-20260929T0818Z.log`，0 FAIL（32 頁依 §1；每頁 notes＝§2；24 個圖頁的圖與 `_hires` PNG 位元組相同、長寬比相符，頁上除頁碼沒有別的字；7 個表頁的表＝§2）。所核的 §1＋§2 sha256 `ac5060e73d735f32…`；本節是之後才寫的，不影響那兩段。
- 沒有 render：N3 第 4 列本來就是兩行，表底仍估約 6.36 in（Liberation Sans 上界）。
- 🔴 **PDF 沒有重產**，仍是 09-28 的 36 頁版本（本機沒有 LibreOffice）。

## 1d. 產檔紀錄（2026-09-29 09:03Z，cowork session，v1.8）

- 產生器沒改（§1b／§1c 那一版），在 cowork sandbox 重跑：`figures: 37 on disk / 24 used / 13 archive-only / 0 unaccounted`、`done — 32 pages`；pptx sha256 `efad58aa6eabe080…`（pptx 內含時間戳，與 §1c 的 `ee1dc54c…` 不同是預期的）。產生器裡 24 個 `fig()` 的長寬比逐一對 `_hires` PNG 核過，0 不符。
- **PDF 已重產**：LibreOffice headless 從這份 pptx 轉出，32 頁，sha256 `2b85e7a3bb4d6947…`；取代 09-28 的 36 頁版。
- Render 逐頁看過：32 頁沒有溢出、重疊；B1、B4、B5、N3 的表底實測都在頁碼（6.92 in）之上（B1 約 6.5、B5 約 6.6 in），§1b 的估計成立。B5 表字級 12、B1 13 是全 deck 最小的字；要放大就得拆頁或刪欄，留給 Adam 定。

## 2. 逐頁講者備註

記號：🟢 跑過（OBSERVED）、🟠 讀碼或讀文件（READ）、推論（INFERRED）。縮寫：K＝`/home/adam/Desktop/NDTwin-Kernel`；
L＝`K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs`；E＝`K/doc/audit/2026-09-04_p4-tutorial-exercise-prep`；
I＝`K/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926`；T06＝`L/2026-09-27T074635Z_06_thirteen/00_table.tsv`（code `5dc7fc9a +95`，audit-raw `797c34ab`）。
每一條的完整 path:line 在該圖的 `.md`。所有 run 的 code sha 都是髒 checkout，+N 見規則 5 與各 `.md`。

### A0 `NDTwin progress · 2026-09-30`　form: title
投影片上只有這一行標題（署名「Adam」要不要放由 Adam 定；916 放了）。
- 「先用五頁講背景：13 支 P4 tutorial exercise 各在做什麼，細看 basic 與 basic_tunnel 兩支，09-16 的 NDTwin 對它們缺什麼，我們用什麼辦法補上。
  之後只講結果：13 支現在都在 NDTwin 的 fabric 上跑起來、兩臂照預期；兩刀讓 NDTwin 能寫外來程式宣告的那一張路由表、能偵測它的斷線；執行期改規則；一個本機的網頁入口；一份遙測比較。」
- ❌ 不說「NDTwin 能操作外來 P4 程式」。

### B1 `The 13 P4 tutorial exercises`　form: table
背景段（Adam 2026-09-29：先講 13 支 exercise 大概在做什麼；不受 delta only 限制，§0 規則 1）。投影片上是這張表。

| exercise | the student writes | the packet carries | its tables are filled by |
|---|---|---|---|
| basic | lpm lookup, MAC rewrite, TTL − 1 | IPv4 | sN-runtime.json |
| basic_tunnel | a tunnel header and its own exact table | myTunnel 0x1212 + IPv4 | sN-runtime.json |
| calc | a calculator that answers the sender | calc header 0x1234 | none: constant entries in the .p4 |
| ecn | ECN marking when the queue is deep | IPv4, ECN bits | sN-runtime.json |
| firewall | a stateful firewall (bloom filter) on s1 | IPv4 + TCP | sN-runtime.json; s1 has its own program |
| flowcache | packet-in on a miss; idle timeout | IPv4; packet-in/out header | its own controller |
| link_monitor | probes that collect link utilization | probe 0x812 + header stacks | sN-runtime.json |
| load_balance | a 5-tuple hash picks one of two hosts | IPv4 + TCP | sN-runtime.json |
| mri | per hop: switch ID + queue depth | IPv4 option + header stack | sN-runtime.json |
| multicast | MAC lookup; a miss floods a group | Ethernet (ARP, IPv4) | sN-runtime.json + 1 multicast group |
| p4runtime | a controller that writes tunnel rules | myTunnel 0x1212 + IPv4 | its own controller |
| qos | DiffServ marking by protocol | IPv4, DSCP bits | sN-runtime.json |
| source_routing | pop one output port per hop | route stack 0x1234 | none: the path is in the packet |

- 🟠 全表讀自 p4lang/tutorials（checkout `c80d83e`；working tree 只有 `exercises/basic/basic.p4` 三行註解的本機改動，不影響任何一格）：各 exercise 的 README「Introduction」、solution `.p4`、`topology.json`、`sN-runtime.json`；與 GAP-1 §2（`E/GAP-1-exercise-requirements.md:47-100`）、§3 逐支說明（`:104-237`）對得上。逐格的行號與檢查：`K/scratch/overnight-2026-09-05/logs/slides930/b-section-sources-20260929T0741Z.log`（B1 段）。
- 「the packet carries」：自訂標頭的是 7 支（GAP-1 §2a 標 `custom_headers` 關鍵的那 7 支，與 T7 同一組）。etherType 讀自各自的程式：basic_tunnel `solution/basic_tunnel.p4:7`、p4runtime `advanced_tunnel.p4:7`（0x1212）；calc `solution/calc.p4:62`、source_routing `solution/source_routing.p4:8`（0x1234）；link_monitor `solution/link_monitor.p4:8`（0x812）。mri 是 IPv4 option 加堆疊（`solution/mri.p4:44`）；flowcache 在交換機之間走一般 IPv4，自訂的是送控制器的 packet-in／out 標頭（`solution/flowcache.p4:91`）。
- 「tables filled by」：9 支開機灌 `sN-runtime.json`；calc 的 entry 寫死在 `.p4`（`solution/calc.p4:201` `const entries`，`s1-runtime.json` 是空的）；source_routing 三個 runtime 檔都是空的（路徑在封包裡）；p4runtime、flowcache 的拓樸沒有 runtime_json，表由自己的 `solution/mycontroller.py` 在跑時寫（GAP-1 §2b `:66-82`）。multicast 的 group 在 `sig-topo/s1-runtime.json`（1 個）；firewall 的 s1 跑 firewall 程式、s2–s4 跑 basic（`firewall/pod-topo/topology.json`；GAP-1 §3.5）。
- 講法：basic 是 NDTwin 自己路由表的同一形狀（B2），7 支帶自己的標頭（B3 是其中一支），2 支帶自己的控制器。❌ 不說「NDTwin 看得到自訂標頭」（T7、N3）。

### B2 `basic: one packet through the program`　form: figure　`background/fig_b2_basic_walkthrough`
- 🟠 全圖讀自 tutorials `c80d83e`（`git show`，不讀 working tree）：`exercises/basic/solution/basic.p4`、骨架 `basic.p4`、`Makefile`（TOPO＝`pod-topo/topology.json`）、`pod-topo/topology.json`、`pod-topo/s1–s4-runtime.json`、`README.md`。產生器從這些檔讀出圖上每個名字、常數、埠與 entry，任一錨點不見就以具名理由停下（紅檢 81/81，§0 規則 10）。沒有跑任何東西。
- 上排是程式：parser 的 ethernet → etherType 0x800 → ipv4（`solution/basic.p4:60-71`）→ MyIngress：`ipv4_lpm`（key `hdr.ipv4.dstAddr`、lpm、沒命中＝drop，`:102-113`），命中就呼叫 `ipv4_forward(dstAddr, port)`：設 egress port、src MAC ← 原 dst MAC、dst MAC ← dstAddr、TTL − 1（`:95-100`）→ 重算 IPv4 header checksum（`:136-154`）→ deparser 送出 ethernet、ipv4（`:160-165`）。
- 藍框＋TODO＝學生要寫的：骨架的 parser、`ipv4_forward` 的內容、`apply`、deparser 都是 TODO（骨架 `basic.p4:67-73`、`:120-128`、`:151-156`、`:204-209`）；`ipv4_lpm` 這張表與 checksum 是給好的。README：骨架「drops all packets」（`README.md:47`，圖右下）。
- 下排：pod-topo，4 台交換機、4 台主機。藍線是 h1 送往 10.0.3.3 的封包照 runtime entry 走的路：s1 port 3 → s3 port 2 → s2 port 1 → h3（腳本沿 entry 與拓樸的埠算出，不是手畫）。右邊是 s1 開機裝進去的 5 條 entry（1 條 default drop＋4 條 /32），藍底那一條就是這個封包在 s1 命中的。
- 為什麼挑它：它的 `MyIngress.ipv4_lpm`／`ipv4_forward(dstAddr, port)` 與 NDTwin 自己的路由表同形，也就是 roles 綁定的那一張（B5 第 6 列、R1、R2）。

### B3 `basic_tunnel: its own header, its own table`　form: figure　`background/fig_b3_basic_tunnel`
- 🟠 同 B2 的讀法（tutorials `c80d83e`、`git show`、具名停止條件）：`exercises/basic_tunnel/solution/basic_tunnel.p4`、骨架 `basic_tunnel.p4`、`topology.json`（TOPO 用 `utils/Makefile` 的預設）、`s1–s3-runtime.json`、`myTunnel_header.py`、`send.py`。
- 左上：自訂標頭 `myTunnel_t`＝`proto_id`、`dst_id` 各 16 bit（`solution/basic_tunnel.p4:24-27`），夾在 ethernet 與 ipv4 之間，etherType **0x1212**（`:7`；主機端 `myTunnel_header.py` 同值、綁在 Ether 之下）。主機用 `send.py <ip> <msg> --dst_id N` 送出 Ether／MyTunnel(dst_id)／IP（`send.py:40`）。
- 右上 parser：etherType 0x1212 → myTunnel，proto_id 0x800 → ipv4；0x800 直接 → ipv4（`:67-87`）。
- 中排 MyIngress：有 tunnel 標頭就查 `myTunnel_exact`（key `hdr.myTunnel.dst_id`、exact）→ `myTunnel_forward(port)` 只設 egress port（`:131-145`）；否則是 IPv4 就走和 basic 一樣的 `ipv4_lpm`（`:147-157`）。deparser 依序送出 ethernet、myTunnel、ipv4（`:198-204`）。
- 藍框＋TODO：骨架的 parser、`myTunnel_forward`、`myTunnel_exact`、`apply`、deparser 都是 TODO（骨架 `basic_tunnel.p4:61`、`:127`、`:130`、`:135`、`:183`）；標頭型別與 IPv4 那一半是給好的。骨架的 `sN-runtime.json` 已經寫了 `MyIngress.myTunnel_exact` 的 entry，而骨架沒有這張表，所以 README 說骨架 `make run` 跑不起來（`README.md:41-43`）——T5 那唯一一次 pre-flight 拒絕就是它。
- 下排：同一個目的 IP 10.0.3.3（h3）。不帶 tunnel：s1 port 3 → s3 port 1 → h3（灰虛線）；帶 `dst_id 2`：s1 port 2 → s2 port 1 → **h2**（藍線）——tunnel 標頭蓋過 IP 目的地（README 第 6 步，`README.md:134-140`）。每台 6 條 entry＝3 條 ipv4_lpm＋3 條 myTunnel_exact；右邊是 s1 的三條 exact。
- 為什麼挑它：它是帶自己標頭的那 7 支之一。🟢 在 NDTwin fabric 上解答臂轉得動（T06 PASS (4/4)：`--dst_id 2`／`3` 各落在對的主機，`E/runs/2026-09-27T075455Z_basic_tunnel_solution_ndtwin.md:833-835`，code `5dc7fc9a +95`）；twin 只看過同一 fabric 上的一般 IPv4（T7「IPv4 only」）。❌ 不說「NDTwin 觀測得到 0x1212」。

### B4 `What the 09-16 NDTwin lacked for them`　form: table
投影片上是這張表。每一列是一件「exercise 要、而 09-16 的 NDTwin（kernel＋P4 proxy＋ndt）沒有」的事。全部 🟠 讀碼：GAP-2（09-08 在 trunk `1a284f75` 的盤點）、PLAN-0917 §0 與 §3.2（09-17 逐處 grep 確認那些寫死點在 trunk `70615ec5` 還在），並在 `70615ec5` 上以 `git grep` 重核一次——它就是 2026-09-16 00:00Z 的 trunk（前一個 first-parent commit 在 09-12，下一個在 09-17）。

| need | NDTwin on 09-16 | what that blocked |
|---|---|---|
| own program per switch | every bmv2 ran ndtwin_switch.p4 | all 13 (firewall: two programs) |
| entries by its own names | fixed names: ipv4_lpm, flow_5tuple | 9 exercises' start-up entries |
| multicast groups | no way to write one | multicast |
| its own topology | 10 switches fixed; hosts by formula; no shaping | other shapes, 1 switch; ecn/mri queues |
| link up/down detection | LLDP via packet-out/in: needs ndtwin_switch.p4 | link state on any other program |
| NDTwin routes in its table | /32 routes into its own ipv4_lpm | NDTwin routing on its program |
| its own controller | one fixed election id for every client | p4runtime, flowcache |
| link usage of its traffic | samples cloned by ndtwin_switch.p4 | every link rate 0, no error |
| what a switch cannot do | no capability field | writes that fail after "queued" |

- 第 1 列：artefact 路徑寫死 `ndtwin_switch.{p4info.txt,json}`（`70615ec5:p4_proxy/proxy_agent/main.py:185-186`、`p4_proxy/mininet/p4_testbed_topo.py:361`、`:806`；GAP-2 `:22`、`:45-58`）。firewall 要 s1 與 s2–s4 兩支程式（GAP-1 §4a `:246`）。
- 第 2 列：表名、action 名寫死（`p4_client.py:816-817` 的 `IPV4_LPM_TABLE`／`FIVE_TUPLE_TABLE`；GAP-2 `:23`、`:59-66`），沒有「照 exercise 的 `sN-runtime.json` 灌表」的路。9 支＝開機 runtime 帶 entry 的那 9 支（B1）。
- 第 3 列：`p4_proxy/` 裡沒有任何 multicast group 寫入（`git grep` 無命中；GAP-2 `:24`、`:74-78`）。
- 第 4 列：交換機清單寫死 1..10（`main.py:154`）、主機位置用四等分公式、選檔只看主機數（GAP-2 `:219-222`）；沒有交換機間鏈路的模型被拒（`p4_proxy/mininet/topo_from_json.py:114`；calc、multicast 是單交換機，PLAN-0917 `:108-109`）；P4 fabric 上沒有 TCLink（`git grep` 無命中；GAP-2 `:224-225`），ecn、mri 的 0.5 Mbit/s 瓶頸做不出來、qdepth 恆 0（GAP-1 §4b `:263-264`）。
- 第 5 列：LLDP 走 packet-out／packet-in，靠 `ndtwin_switch.p4` 的 controller header（`p4_proxy/p4_src/ndtwin_switch.p4:156`、`:167`；`topology_manager.py:1374` 造 LLDP 幀；GAP-2 `:148-159`）。別的程式沒有這個標頭，鏈路發現與斷線偵測就都沒有（H1）。
- 第 6 列：開機以 BFS 對每台主機寫一條 `/32` 進自己的 `MyIngress.ipv4_lpm`（`topology_manager.py:1151`；GAP-2 `:229-232`）。在別人的程式上「NDTwin 能不能寫它的表」沒有任何宣告；同名同形的表反而可能被悄悄蓋掉（INFERRED，ANALYSIS `:26`）。
- 第 7 列：十個 client 同投寫死的 election id (0, 1)（`p4_client.py:62`、`:255-256`）；另一個控制器用同一個 id 推 pipeline 會被接受並清空每一張表（🟢 2026-08-13 實測，09-16 之前的背景證據，GAP-2 `:237-240`）。
- 第 8 列：遙測靠程式合作——ingress clone 到 session 250、egress 補 packet-in（`ndtwin_switch.p4:48`、`:411`）；換一支程式，每個鏈路速率都是 0 而且沒有錯誤（GAP-2 §3 第 1 條 `:265-269`）。
- 第 9 列：kernel 與 proxy 都沒有 `capabilities` 欄位（`git grep` 無命中；kernel LLM 意圖翻譯器的 `GetSwitchCapabilities` 講的是 OpenFlow 機型，不相干）；不支援的寫入 kernel 先回 `queued`、之後才失敗（ANALYSIS `:338`、`:349`，讀 09-24 的 trunk `057a01f0`；D2 是 P4 平面上跑過的樣子）。
- 逐列的指令與輸出：`slides930/b-section-sources-20260929T0741Z.log`（B4 段）。

### B5 `How each gap was bridged`　form: table
投影片上是這張表，列與 B4 一一對應。**ran live** 欄只放跑過的（🟢）；**not yet** 欄寫明是哪一種（offline＝只有離線的 convert／pre-flight；not done＝沒做；not run＝沒跑）；decision、mechanism 兩欄是 🟠（讀 PLAN-0917、09-24 的裁決與 trunk `3368412d` 的碼）。

| need | decision | mechanism | ran live | not yet |
|---|---|---|---|---|
| own program per switch | the exercise comes as a package (09-17) | convert.py → package; ndt up p4 --app | 13/13 exercises (T06) | — |
| entries by its own names | names checked before anything starts | pre-flight; proxy writes by p4info names | 9 exercises, 0 failed | not done: ternary, range |
| multicast groups | the package declares them | proxy writes them over P4Runtime | multicast: 1 group | — |
| its own topology | the package carries it | ndtwin/topology.json; shaping if declared | pod, triangle, 5h/3s, 1 switch | — |
| link up/down detection | no .p4 change (09-24) | veth heartbeat from a root helper | 6/6 cuts detected (08) | not done: p4runtime, flowcache |
| NDTwin routes in its table | roles: NDTwin owns one table (09-24) | proxy binds its route writes to it | basic (07, twice) | offline: 6 same-shape exercises |
| its own controller | the proxy stays out | an adapter points it at the fabric | p4runtime, flowcache | — |
| link usage of its traffic | sample the links, not the program | tc sampling on switch veths → sFlow | 10/13 (plain IPv4 iperf) | not run: 3 (drop plain iperf) |
| what a switch cannot do | capabilities, read once (09-24) | switch_state → get_graph_data → GUI | proxy (07, twice) | kernel: unit tests · GUI: local draft |

- 第 1 列：Adam 09-17 裁路線 2——「exercise 只是階段目標；教授要的是帶自己的 .p4 來」⇒ package（PLAN-0917 §8 `:121-132`；沒有 package 時行為與原本逐位元組相同，§2 `:28`）。機制：`tools/p4_exercise/convert.py`（`386eb20c`）、`ndt up p4 --app`（`54f69d15`）、每台跑 package 指定的程式（`b392f111`）。🟢 T06 13/13 兩臂照預期（code `5dc7fc9a +95`）；firewall 兩支程式同時在線（GAP-2b `:88`）。
- 第 2 列：pre-flight 在起 fabric 之前對每台的 p4info 驗表名、欄位、位寬，對不上就拒絕（PLAN-0917 `:131-132`；`tools/p4_exercise/preflight.py`，T5）；proxy 依 p4info 的名字寫 package 的 entries（`78067633`；GAP-2b `:89`）。🟢 T06：basic、basic_tunnel、ecn、firewall、link_monitor、load_balance、mri、multicast、qos 的解答臂都是「table entries: N/N applied …, 0 failed」（逐臂行號見 log）。只做 exact／lpm（13 支只要這兩種）；`journaled: false`，proxy 重啟表項就消失（T3）。
- 第 3 列：`write_multicast_group`，開機套 package 的 `multicast_group_entries`（`5ce3bf74`；`p4_client.py:912`）。🟢 multicast 解答臂 group applied 1、failed 0（`E/runs/2026-09-27T075305Z_multicast_solution_ndtwin.md:332-336`）；細節在 T4。
- 第 4 列：convert 寫出 `ndtwin/topology.json`（`convert.py:527`、`:786`），fabric、proxy、kernel 讀同一份（`f282b895`；單交換機合法 `b392f111`；主機介面 `eth0` `8e62b423`；宣告了整形才開 TCLink `f5ad6890`）。🟢 T06 四類拓樸：pod 4h/4s、三角 3h/3s、5h/3s、單交換機（calc 2h/1s、multicast 4h/1s），kernel 圖、拓樸檔、主機 namespace 三方一致（GAP-2b `:101`）。
- 第 5 列：Adam 09-24 裁決 ②——不要求使用者改 `.p4`，改用 root 的 veth 心跳（ANALYSIS `:404`）；`cafd518a`。🟢 08 H1 六次剪線都在 20 s 內偵測（12.2–16.8 s，`L/2026-09-26T152605Z_08_heartbeat/30_cycles.tsv`，`cafd518a +85`）；細節在 H1–H6。帶自己控制器的兩支不起心跳（🟢 `I/hbw-live/h14-20260926T152605Z.log:168`）。
- 第 6 列：Adam 09-24 裁決 ①（ANALYSIS `:403`）——package 用 `roles` 宣告，`owner: ndtwin` 時 NDTwin 獨佔那一張目的路由表；`572d9462`。🟢 basic 上 07 跑兩次、16/16 條初始路由（`L/2026-09-26T202055Z_07_roles_basic/21_proxy_roles_lines.txt:2`）；另 6 支同形只在離線過 convert＋pre-flight。細節在 R1–R3。❌ 這是**一張表**，不是「NDTwin 能操作外來 P4 程式」。
- 第 7 列：這兩支的 package 標 external：proxy 不開仲裁、不推 pipeline、不寫任何東西（TICKET-P1 `:57`；`f282b895`）；`tools/p4_exercise/run_external_controller.py:70-97` 把控制器寫死的 `127.0.0.1:5005N` 改到 fabric 的埠。🟢 T06 p4runtime、flowcache 解答臂 PASS。
- 第 8 列：Adam 09-17 要兩種遙測都做、在同一 fabric 上比（PLAN-0917 `:149-151`；比較在 M1）；別人的程式預設走鏈路級：每條交換機 veth 上 `tc … action sample`，root emitter 轉成 kernel 本來就吃的 sFlow（`f5ad6890`；T06 arm report 的 `telemetry.source … anybody else's gets link telemetry`）。🟢 G1（twin 的鏈路使用率跟著 iperf 走）在 10/13 解答臂 PASS；not yet 欄的 3 支是 calc、source_routing、load_balance：它們的程式丟掉一般 iperf，G1 NOT RUN。G1 用的是一般 IPv4 iperf——❌ 不說它證明 twin 看得到自訂標頭（T7）。
- 第 9 列：Adam 09-24 裁決 ③（ANALYSIS `:405`）——proxy `switch_state` 帶 capabilities（`572d9462`）→ kernel `get_graph_data` 的節點原樣帶（`85bec430`，09-28）→ GUI 把做不到的操作變灰（`~/Web-GUI` 的本機草稿分支，未推）。🟢 只有 proxy 那一段（兩次 07）；kernel 那一段只有單元測試與 CI；GUI 沒有 live（R1 ③、R4）。
- 逐列的檢查：`slides930/b-section-sources-20260929T0741Z.log`（B5 段：trunk `3368412d` 上的檔、十個 merge 的祖先關係、T06／07／08 的 raw）。

### T3 `How a foreign P4 program runs on NDTwin`　form: figure　`foreign-p4/fig_a1_foreign_p4_path`
- 這是 B5 那幾個機制在一次 `ndt up` 裡一起跑的樣子。
- 七步：exercise → `convert.py` 打包 → pre-flight（圖上寫「package checks」；🟢 **21–25 項 PASS**，依 package 而異，腳本從 T06 與 07 的報告數出——數字只在講稿，不上圖）→ claim → `ndt up p4 --app` → 它自己的封包測試 → down／release／報告。每步在 T06 的 arm report 都找得到（`.md` 逐格列行號）。
  圖上沒有跑出來的數字（這頁同時有跑過的方塊與讀碼的箭頭）：bmv2 每個 fabric 1–4 台、自帶控制器的是 p4runtime 與 flowcache（13 支中 2 支）都只在講稿。
- 下半是 `ndt up` 起來的東西：每台 bmv2 跑 **exercise 自己編出來的程式**；proxy 方塊裡四個名字＝它經 P4Runtime 寫的東西（pipeline、table entries、multicast groups，宣告了 roles 就寫 `roles.ipv4_route` 那張路由表）；root helper 跑心跳。
  方塊的**存在**是 🟢（T06、07 raw），箭頭的**機制**是 🟠——圖上照寫：上排標「RAN IT · every step appears in T06's arm reports」，下半標「RAN IT: the boxes · READ THE CODE: the arrows」。
- 13 支裡 2 支（p4runtime、flowcache）帶自己的控制器：proxy 不仲裁、不寫；控制器經 adapter 連到 fabric 的埠（🟠 `tools/p4_exercise/run_external_controller.py:70-97`）。
- 表項只有 exact／lpm、`journaled: false`（proxy 重啟就消失）。
- ❌ 不說「NDTwin 能操作外來 P4 程式」。

### T1 `What NDTwin covered: 09-16 vs 09-27`　form: figure　`p4-tutorials/fig_t1c_ndtwin_coverage`
兩列 NDTwin 與右邊兩欄，分三個有標題的面板。
- **BACKGROUND · READ THE CODE · NDTwin's own P4**（灰底背景帶，標「as shown 09-16; read 09-08, trunk 1a284f75」）：這一列就是 916 deck 第 3 頁的「NDTwin today」列，只當對照。
  問的是「NDTwin **自己那支** P4 程式（`ndtwin_switch.p4`）提供得了這一維嗎？」全部 🟠 讀碼（GAP-2，trunk `1a284f75`，09-08 的盤點）。做得到 1／部分 9／做不到 6。
- **RAN · JUDGED · 09-27 · each exercise's own P4 on the NDTwin fabric**（格子是依跑過的證據下的判斷）：「需要這一維的 exercise 在 NDTwin fabric 上跑得起來，而且歸 NDTwin 負責的那一半是 NDTwin 的碼做的嗎？」（GAP-2b §1）8／6／2。
  14 格的依據含跑過；`meters`、`digest` 兩格只有讀碼，而且都是做不到（交叉斜線，圖例「cannot · read only」；腳本斷言 read-only ⊆ 做不到，GAP-2b `:93`、`:95`、`:105`）。
- 🔴 **兩列回答不同的問題，不可講成「NDTwin 多了 7 個能力」**：變化一部分是 NDTwin 多做了事（每台自己的 pipeline、依 p4info 灌表、multicast group、拓樸、心跳），一部分是**題目換了**——程式是 exercise 自己的，register／checksum／queue 的讀寫本來就在它的程式裡（GAP-2b §2）。
- **T06 · 09-27**：runs on NDTwin 欄標 **RAN IT**——13/13 兩臂照預期（🟢 T06）；twin sees it 欄標 **JUDGED**（讀同一批 run 的 raw 判的，與 T7 同一用詞）——看得到 6／只看過 IPv4 4／無證據 3。
  與 GAP-2b §3 裁定後的彙總相同；**flowcache** 是與 T7 同一個字「**IPv4 only**」：**T06 的流只到了 s1→s3 那一段，沒有送達 h3**（s1-eth3 就是 s1 往 s3 的那條線：tutorials `exercises/flowcache/topology.json:48-51` 的 `["s1-p3", "s3-p2"]`，Mininet 的 pN＝ethN；tutorials checkout `c80d83e`，乾淨）。
  twin 自己的讀數在 s1-eth3 約 31.8 Mbit、s3 三個介面都是 0（`FC/link_usage/twin_integral.txt:3`、`:7-9`）；介面計數器說位元組正是這樣走的——s1-eth3 3151 → 4596340 B、往 h3 的 s3-eth1 只 +273 B（`netdev.before:7`／`netdev.after:7`、`:3`／`:3`）——所以 s3 的 0 是正確讀數，不是 twin 的錯；沒有送達：`iperf_server.txt` 沒有報告列、`iperf_client.txt:10` 沒收到 ack。
  flowcache 那一格 Adam 09-28 裁定為 IPv4 only（N3 第 5 列）。FC＝`E/runs/2026-09-27T081256Z_flowcache_solution_ndtwin`。
- **四個判斷格 Adam 09-28 裁定**（照建議值）：`registers`＝部分、`queue_metadata`＝做得到、twin 欄的 multicast＝看得到、flowcache＝IPv4 only；右上標「as of GAP-2b with Adam's 2026-09-28 ruling」。
- B4／B5 是這一頁的文字版：09-16 那一列缺的，B5 逐列說怎麼補、哪些跑過。
- GAP-2b 裁定後提交為 `c8433963`（已公開）；T06 與 flowcache 那一臂的 raw 在 audit-raw `797c34ab`；code `5dc7fc9a +95`。

### T4 `multicast, end to end on the NDTwin fabric`　form: figure　`p4-tutorials/fig_t6_multicast_end_to_end`（○）
- 🟢 T06 multicast 兩臂（code `5dc7fc9a +95`）：convert 出 7 個檔；pre-flight 24 PASS、0 FAIL；claim 45 分鐘；`ndt up` 起 1 台 bmv2 跑 exercise 自己的 `build/multicast.json`；proxy 經 P4Runtime 寫表項 4/4、multicast group 1/1，都 0 失敗。
- 🟢 解答臂：h1／h2／h3 互通；h1／h2／h3→h4 三對 100% loss；h4→其他三台 0% loss；清掉 ARP 快取重量一樣；**PASS (6/6)**。骨架臂 12 對全 100% loss，正是它該有的樣子，PASS (2/2)。
- 為什麼 h4 收不到：group 只複製到 1、2、3 埠（🟠 package 的 `sig-topo/s1-runtime.json:47-65`）；h4 自己的 MAC 有轉送項，所以它發得出去。
- 這支是單交換機，心跳沒東西可看——不要在這頁講心跳。

### T5 `What pre-flight checks before ndt up`　form: figure　`p4-tutorials/fig_t7_preflight_checks`
- 🟢 26 份真實 pre-flight 輸出（T06 的 25 臂＋07 roles 那份）：通過的 package 各 21–25 個 PASS；每列右邊數字＝這一項在 26 份裡以 PASS（綠）／INFO（灰）／FAIL（紅）出現的份數。分六組是產圖時的判斷（INFERRED），名稱 🟠 `tools/p4_exercise/preflight.py:292-326`。
- 🟢 紅框＝唯一的拒絕：basic_tunnel 骨架，9 個問題，第一個是 `MyIngress.myTunnel_exact` 不在它的 p4info → rc 1、沒有 `ndt up`（`E/runs/2026-09-27T075454Z_basic_tunnel_skeleton_ndtwin.md:239`、`:244`；T06 第 10 行）——這是 exercise 設計好的紅臂。rc 1 與「沒有 ndt up」只在講者口中，圖上不寫。
- ❌ 不說「7 個 check 失敗」：輸出末行的「7 check(s) failed」其實是 1 個 check 的 7 行 FAIL（🟠 `preflight.py:1136-1142`、`:1239`）。

### T6 `What the exercise brings, what convert adds`　form: figure　`p4-tutorials/fig_t8_what_you_bring`（○）
- 🟢 作者帶來：自己的 `.p4`、p4c 編出的 bmv2 json 與 p4info、`topology.json`、每台的 `sN-runtime.json`（T06 basic/solution arm report `:78-88`）。
- 🟢 convert 照原路徑複製（basic 8 份），再新寫 `package.json` 與 `ndtwin/topology.json`，共 10 個檔；寫完讀回一次：ok（同檔 `:89`）。
- 自帶控制器的 2/13：只把名字記進 `package.json`，不複製（🟢 兩份 solution report；🟠 `convert.py:461,502`）。

### T7 `Seven custom-header exercises forward`　form: figure　`p4-tutorials/fig_t9_custom_headers`
- 🟢 七支自訂標頭 exercise 的解答臂在 T06 全 PASS：**它們在 NDTwin fabric 上轉得動**（左面板 RAN IT）。
- 🟢 只有 p4runtime 有 twin 看到自己幀的位元組證據：s1-eth2 比 s2-eth1 多 14,000 B＝3,500 datagram × 4 B tunnel 標頭，twin 在那條鏈路積分 > 0（「那就是 0x1212 幀」是由位元組推的，沒抓 pcap＝INFERRED；右面板標 JUDGED）。
- 🟢 basic_tunnel、flowcache、link_monitor、mri 只驗過同一 fabric 上的一般 IPv4 iperf；calc、source_routing 的 G1 NOT RUN（它們的程式丟掉一般 iperf）。
- flowcache 在這頁與 T1 都是「**IPv4 only**」：**T06 的流只到了 s1→s3 那一段，沒有送達 h3**——twin 在 s1-eth3 讀到流量、s3 各介面讀 0，與介面計數器一致（raw 見 T1）；它的自訂標頭只走 CPU 通道，twin 沒看過。
- 「6 支還是 7 支」：GAP-1 §2a 標 7 支；GAP-ANALYSIS G6 寫 6 支（差的是 p4runtime）；「走在交換機鏈路上的自訂標頭」也是 6 支，但是 GAP-1 的 7 支扣掉 flowcache。對帳在 `.md`。
- ❌ 只說「轉得動」，**絕不說「NDTwin 觀測得到它們」**。

### R1 `Four rulings on the P4 API shape (09-24)`　form: table
Adam 2026-09-24 四題全按建議裁（🟠 `K/doc/audit/2026-09-24_p4-driven-api-shape/ANALYSIS.md:401-408`）。投影片上是這張表；`roles/fig_r1_four_rulings` 留作存檔。

| ruling (09-24) | ran live | offline / read only | not done yet |
|---|---|---|---|
| ① owner: ndtwin → NDTwin owns that table | pass path: 0 package entries, 16/16 routes written (07, twice) | refusing package entries: unit test + caught mutant | a live refusal; "rerouted table derivable from the declaration" |
| ② no .p4 changes; root veth heartbeat | owned route tables: detect + reroute (08 H1–H5) | tutorials' own `basic.p4` unmodified | external control planes: no heartbeat; worst watchdog phase |
| ③ GUI reads capabilities once, greys out | proxy reports capabilities, 4/4 switches, both 07 runs | kernel `get_graph_data` carries them: unit tests + CI (merged 09-28); GUI draft on a local branch | kernel side on a live fabric; grey-out in a pushed GUI (cut 3, GUI side) |
| ④ first cut: 7 same-shape programs, one table | basic only (07, twice) | 6 others: convert + pre-flight PASS; 4 other shapes FAIL as intended | the 6 on a fabric; multi-table, tunnel, ternary; no 5-tuple role |

- ① 🟢 `L/2026-09-26T202055Z_07_roles_basic/12_preflight_basic_roles.txt:29`（PASS owned table has no package entries）、`21_proxy_roles_lines.txt:2`（16/16）、`10_convert_roles.txt:6`（拿掉 16 條）；09-24 那次 `L/2026-09-24T160256Z_07_roles_basic`。code `b2eeb71d +92`／`572d9462 +61`。
  🟠 拒收只在離線：`tools/p4_exercise/tests/test_preflight.py:747`；變異 M-R4（pre-flight 不再拒收）被抓到（`K/scratch/overnight-2026-09-05/logs/orchestrator-0924/rerun-R-177b9f03.mutate_roles_binding.log:34`）；合併樹上 187 OK。裁決的後半（改路後的表可由宣告推出，`ANALYSIS.md:403`）**沒有任何地方檢查**。
- ② 🟢 08 H1：6 次剪線 20 s 內偵測、路由改寫；H2 心跳停了不偵測；H3 沒綁定只偵測不改路；幀到主機 0（`I/hbw-live/h14-20260926T152605Z.log:72`、`:129`、`:143`、`:151`，code `cafd518a +85`）；H5 心跳恰在該有的 17 臂上跑、26 臂同參照（`h5b-20260926T172912Z.log:47-59`，`3f8c2abf +89`）。
  外來控制器（p4runtime、flowcache）不起心跳（h14 `:168`、`:173` reason `external_control_plane`）；external 控制面目前沒有斷線偵測。最壞 ψ 沒取樣到（h14 `:129`）。
- ③ 🟢 proxy `/p4/switch_state` 兩次 07 都給 4 台相同 capabilities、L6 PASS（`30_／71_switch_state_*.json`）。🟠 `p4_proxy/proxy_agent/main.py:1151`、`:1205`。kernel 在 `3d740be0` 沒有 capabilities；**第三刀 kernel 側 09-28 03:41Z 併入 `85bec430`**：每台 bmv2 的 `get_graph_data` 節點帶 proxy 回報的 capabilities（原樣複製）；PR #14 的 CI 四個 job 全綠、ctest 1385/1385（1368＋17 個 P4Capabilities*，`I/ci-compare-pr14.txt:1-2`）——🔴 kernel 這一側**沒有 live run**。GUI 側在 `~/Web-GUI` 的本機草稿分支。
- ④ 🟢 basic 兩次 07，L1–L6 全 PASS。🟠 離線：basic_tunnel（IP 部分）、ecn、qos、mri、link_monitor、firewall 過 convert＋pre-flight；calc、load_balance、multicast、source_routing 照設計 FAIL（`K/scratch/overnight-2026-09-05/logs/orchestrator-0924/merged-R-572d9462.offline_5-3.log:1-37`）。沒有五元組 role（`route_binding.py:75`）。
- ❌ 這是**一張目的路由表**，不是「NDTwin 能操作外來 P4 程式」。

### R2 `roles.ipv4_route: from package to table`　form: figure　`roles/fig_r2_roles_path`
- 上排 🟢（09-26 live 07，`L/2026-09-26T202055Z_07_roles_basic`，repo `b2eeb71d +92`（髒）、kernel `be70b5dd32356847`）：package 宣告表、比對欄位、動作三個名字 → convert 拿掉那張表原有的 16 條（每台 4）→ pre-flight 兩條 PASS → proxy 開機寫進 **16 of 16** 條初始路由（`21_proxy_roles_lines.txt:2`）。
- 下排 🟠（trunk `3d740be0`）：kernel `installAnEntry` → proxy `route_flow` → `RouteBinding` → P4Runtime Write，寫進**練習程式自己的** `MyIngress.ipv4_lpm`；沒有 roles 時同一條路回 501。pre-flight 與 proxy 用同一個 `resolve()`。
- 同一個 run 的 `ndt up` 收尾橫幅仍印「NDTwin discovered no links and installed no routes」——那是過時的字句（🟠 `tools/test_workflow/ndt:4151-4157` 只要是外來 pipeline 就印），不是路由沒寫。

### R3 `Live 07: roles on basic, run twice`　form: figure　`roles/fig_r3_live07`
- 🟢 兩次 live 07：09-24（`572d9462 +61`，心跳還沒進來）與 09-26（`b2eeb71d +92`，心跳在跑），L1–L6 每格 PASS（stdout：`K/scratch/overnight-2026-09-05/logs/orchestrator-0924/live-0925/07_roles_basic.log`、`I/live07/07.log`；判定行 20／21 條，末行 `PASS 07_roles_basic`）。
- 🟢 pingall：開機 12/12、恢復後 12/12；**剪線期間**有掉包的對數 8/12（09-24）→ 3/12（09-26）（`54_pingall_during_cut.txt`）。
- 🔴 那一項 07 **只記錄、不斷言**（07 腳本寫成 note）；L4 **不斷言改路**——改路的斷言在 08 的 H1（H3 頁）。「8→3 是心跳改路造成的」只算推論：兩次之間 proxy 也改了別的碼。

### R4 `What each switch reports: capabilities`　form: figure　`roles/fig_r4_capabilities`（○）
- 🟢 最新一次 live 07（09-26，`L/2026-09-26T202055Z_07_roles_basic`，repo `b2eeb71d +92`（髒，腳本從 `00_status_before.txt:7` 讀）、kernel `be70b5dd32356847`）：proxy 的 `switch_state` 每台都報 capabilities，每列 4 台完全相同（`30_switch_state_roles.json`、`71_switch_state_plain.json`）。
- 🟢 宣告 roles 的那包：`ipv4_route` ndtwin、`reroute` true；沒 roles 的：`ipv4_route` unbound、`reroute` false（頂層 `reroute.reason` unbound）——只偵測、不改路。兩包的 `link_discovery` 都是 heartbeat（存檔時 8 條鏈路方向都由心跳餵、沒有 down）；`five_tuple` 一律 false（第一刀沒有五元組 role）。
- `ipv4_route: ndtwin` 只代表目的 IP 路由表這一張。帶自己控制器的 exercise（p4runtime、flowcache）不在圖上：那裡不起心跳。
- kernel 的 `get_graph_data` 也帶這個欄位（第三刀 kernel 側 `85bec430`，只有單元測試與 CI，沒有 live）；GUI 變灰仍在 Web-GUI 的本機草稿分支。本圖只畫 proxy 的 switch_state。

### H1 `Why link discovery stops at a foreign P4`　form: figure　`heartbeat/fig_h0_why_not_lldp`
- 🟠 NDTwin 自己的 LLDP 走 packet-out／packet-in，需要程式裡有 controller header（`p4_proxy/p4_src/ndtwin_switch.p4:156`、`:167`）；外來程式沒有，packet-out 對它是「parser 從沒寫過的幀」（`p4_proxy/proxy_agent/main.py:2141-2148`）。兩個機制小圖是讀碼，本輪沒有 live 去送（proxy 根本不送）。
- 🟢 所以 proxy 在外來 fabric 上跳過三件事（圖底那一行標「RAN IT · 09-24, before the heartbeat」；上面兩個小圖右上標「READ THE CODE」）——09-24、心跳還不存在時的 live 07 印出 `control_plane.skipped: install_initial_routes, link_watchdog, lldp_discovery`（`L/2026-09-24T160256Z_07_roles_basic/70_up_plain.txt:63`，同次 switch_state 同三項、沒有心跳；code `572d9462 +61`）。
- 第一刀時外來 fabric 上鏈路的 `is_up` 只來自**宣告**（REPORT-P4-2026-09-25.md:87-88），剪線 twin 不知道 ⇒ 第二刀：veth 心跳。一台外來就整個 fabric 跳過（`main.py:2151-2153`）。

### H2 `The veth heartbeat, from wire to kernel graph`　form: figure　`heartbeat/fig_h0b_heartbeat_path`
- 🟠 root helper 每 5 s 在每條交換機間 veth 送一個 0x88B5 幀、在對端聽（`tools/test_workflow/ndtwin-lab:715`、`:734`）；**只寫報告、不判**（`link_heartbeat.py:6-18`）。
- 🟠 proxy watchdog 每 5 s 讀報告，用跟自家 LLDP **同一條規則、同一組常數**：沉默 > 15 s ⇒ 不通（`topology_manager.py:373`、`:419`、`:422`），`_notify_link` 通知 kernel（`:2049`）。改路只在 NDTwin 擁有路由表的 package。
- 🟢 心跳幀從沒到過主機：spike 普查 20 臂 0 幀（`580767a8 +79`）；H5：17 個心跳 session、0 幀（`3f8c2abf +89`；1645 是每秒一次的輪詢筆數，見 H6）。
- 報告不新鮮（daemon 死）⇒ watchdog 凍結、不判、揭露（Adam 09-27 裁決 D，orchestrator 記錄）。external 控制面目前不起心跳（🟢 `I/hbw-live/h14-20260926T152605Z.log:168`）。

### H3 `One cut, one restore — on the kernel graph`　form: figure　`heartbeat/fig_h1_one_cut_cycle`
- 🟢 H1 最慢的一次（cycle 3）：剪線 → kernel 圖兩向 down **16.8 s**；復原 → up **4.6 s**（`L/2026-09-26T152605Z_08_heartbeat/30_cycles.tsv`，repo `cafd518a +85`（髒）、kernel `be70b5dd32356847`；整個 run 在 audit-raw `797c34ab`）。
- 🟢 六次剪線 12.2–16.8 s、六次復原 4.6–5.1 s；`strict_20s` 全 yes；改路之後（線仍斷著）pingall 12/12 0% loss（`34_pingall_cut.txt`），4 條經過那條線的路由被移開（run log `:72`）。
- 三個「frame lost」圓圈的位置是由 5 s 週期推的（INFERRED），不是逐幀量的——圖例寫「frame lost (inferred)」。

### H4 `Detection time: 7 live cuts`　form: figure　`heartbeat/fig_h2_detect_vs_phase`
- 🟢 七點：H1 六次（圓點，owned table、會改路）＋H3 一次（方點，unbound、只偵測）。x＝剪線落在最後一幀之後幾秒（φ），y＝剪線到 kernel 圖 down。規則從**最後聽到的那一幀**算 15 s，所以 φ 越小等越久；色帶＝15 − φ 到 15 − φ + 5（🟠 由常數推）；圖上色帶與 20 s 線都標「design bound (derived)」。
- 四點擠在 φ≈0.02 s（16.52／16.60／16.83 H1、16.61 H3），在左下的放大圖裡各自標值——主圖上看起來只有五個點，是重疊，不是少了。
- 剪線相位：H1 前三次刻意剪在最壞相位（φ≈0.02 s，剛聽到一幀之後），後三次相位均勻隨機（`E/live-p1/08_heartbeat.sh:873-874`、`:934-937`；`30_cycles.tsv` 的 `phi_target` 依序 0.02、0.02、0.02、4.48、4.53、0.98）。早先的「中位數約 14.3 s」**不用**（相位鎖住的 report 層級數字，不是 kernel 圖上的偵測時間）。

### H5 `The detection bound, piece by piece`　form: figure　`heartbeat/fig_h3_upper_bound`
- 🟢 最慢那次拆開：(15 − φ) 14.972 ＋ ψ 1.610 ＋ d＋ε 0.245 ＝ 16.827 s（`30_cycles.tsv` cycle 3，腳本斷言三段相加；`cafd518a +85`）。
- 🟠／INFERRED 設計最壞：φ→0、ψ→5 s ⇒ 20 s 再加 d＋ε ⇒ **約 20 s**，與 NDTwin 自家 LLDP 同級（同一條規則、同一組常數）。這一 run 只取樣到一段 ψ（1.474–1.755 s：H1 六次 1.493–1.755、H3 一次 1.474），**最壞 ψ 沒被量到**。
- Adam 2026-09-27 05:2xZ 裁決 A：**接受「約 20 s」**，`strict_20s` 照記、超過只揭露（orchestrator 記錄，不在 repo）。要嚴格 ≤20 s 的選項＝事件驅動 pass（推算最壞約 15.5 s，代價是 LLDP 與心跳不再共用 pass）——沒排（見 N2）。

### H6 `Heartbeat on, forwarding unchanged`　form: figure　`heartbeat/fig_h4_forwarding_unchanged`
- 🟢 參照＝心跳出現前最後一次完整 06（09-24 18:55Z，`0c96c1d0 +79`）；之後三次（`cafd518a +88`、`3f8c2abf +91`、`5dc7fc9a +95`）心跳在 17 臂下跑，**26 臂的 rc 與判定逐臂相同**。
- 🟢 09-26 17:29Z 那輪的「0」：**17 個心跳 session、0 幀**離開 host 埠（`L/2026-09-26T172912Z_08_heartbeat/50_samples.tsv`，`3f8c2abf +89`）。1645 是 sampler 每秒一次的輪詢筆數（`status running` 的 1063 筆），不是 1645 次獨立量測；08 判定行的 1617＝01 開始前那一刻的筆數，另 28 筆是 01 期間的取樣（已從 raw 對帳）。
- 🔴 **這個 0 沒有 live 陽性對照**：主機 sniff 與 daemon 計數兩個偵測器只在離線證過「真的有幀到主機時會認出來」（P4-HB-SPIKE.md §3.3）。講「0」時要一起說。
- 這是 Adam 09-25 的停止條件（「改變使用者的轉送結果就停下來回報」）——沒有觸發。沒有心跳的 9 臂：單交換機 4、external 3、設計上建不起來的骨架 2。
- ⚠️ 第三欄（09-26 17:29Z）有 12 s 的外來 2 Mbit/s iperf 進了 p4runtime 解答臂的 G1 位元組（約 +8.6%，判定仍 PASS；`E/runs/2026-09-26T175425Z_p4runtime_solution_ndtwin.md:613`）；本頁比的是 rc＋判定與 host 埠幀數，不看 G1 位元組，所以「相同」與「0」不受影響。

### D1 `Changing rules at runtime, per data plane`　form: figure　`flow-api/fig_d1_flow_api_matrix`
- 左邊 RAN IT 只放跑過的（🟢），右邊 READ THE CODE 只放讀碼的（🟠）——不混。
- 🟢 **新的（09-26）**：外來 P4＋roles，kernel API 的 install／delete 都跑過並讀回（`L/2026-09-26T202055Z_07_roles_basic/40–45`）；外來 P4 沒 roles，kernel 先回 `queued`、逐筆結果是 **501 unsupported_on_p4**（`74–76d`）。`b2eeb71d +92`。
- 左下灰底帶「BEFORE 09-16 · BACKGROUND」**只蓋 RAN IT 的格子**：OVS 三個動作經 kernel API 都跑過（**09-03** run-06 D9–D11，公開快照 `9e6cc30`，kernel binary sha 與 checkout 乾淨與否都沒記錄）；NDTwin 自己 P4 的五元組 install／delete 只經 proxy 跑過（**08-24**，commit `e89fd4b`，checkout 乾淨與否沒記錄，+N 不詳）。灰色的 yes＝背景，不是這次的證據；916 第 32–33 頁講過 OVS 的 flow 端點。
  同兩列的 READ THE CODE 格讀的是今天的碼（trunk `3d740be0`），所以不在帶子裡；右表標題標「trunk 3d740be0」。
- 沒跑過就寫「not run」：P4 上的 modify、`/p4/table_entry` 的成功寫入都沒有 live raw。

### D2 `"queued" is not "installed": read it back`　form: figure　`flow-api/fig_d2_queued_readback`
- 🟢 同一個 kernel batch 寫入打兩種 package（09-26 07，`b2eeb71d +92`）：兩邊都回 **200 queued**、accepted 1、request_id 1。
- 🟢 有 roles：dispatch `accepted_by_switch 1`，讀回 `10.0.9.9 → OUTPUT:3`。沒 roles：`rejected_by_switch 1`，原因 501 unsupported_on_p4、reason unbound。
- 🟠 手冊早就寫明 queued＝「accepted for programming, not programmed」（`K/doc/2026-01-02_ndt_api.md:1754-1758`，背景）。916 第 26、28、32 頁講過的是 **OVS** 平面的同一主題；這頁是 **P4 平面**的新證據。
- `accepted_by_switch` 只在 P4 平面有意義；OVS 上永遠 unknown（OpenFlow 不回應 FLOW_MOD）。

### S1 `ndt serve: one local door to the lab`　form: figure　`ndt-serve/fig_s1_serve_path`
- 🟠 只聽 `127.0.0.1:8765`；一次性網址（`#k=<nonce>`，一次、600 s）換 token；每個請求 token＋同源；寫入前可預覽**確切的 ndt 指令**；一次一個工作；app 起停與要 lab 的 cell 在伺服器端檢查「claim 是你的」；`up`／`down` 交給 ndt 自己的守衛（rc 5）。行號在 `.md`（trunk `3d740be0`；`tools/ndt_serve/` 在 `fed37cff` 相同）。
- merge：API＋cells＋walks `48209682`（09-26 00:05Z）、GUI v1 `f186ce98`（09-27 12:35Z）。🔴 **GUI 這一刀沒有 live run**（只對 stub 點過）。畫成架構圖、不放截圖：頁面正依 v2 裁決重做（S4）。

### S2 `ndt serve: threats and defenses`　form: figure　`ndt-serve/fig_s2_security_model`（○）
- 🟢 09-24 live（右面板 RAN IT）：只有一個 listener `127.0.0.1:8765`；外來 Host 回 403 host；沒帶 token 回 403 token；up 跑著時再送寫入回 409 busy（`K/scratch/overnight-2026-09-05/logs/ndt-serve-0924/`，serve `a139bceb`／`c836cff0`；ndt 所在 checkout `fd7382a3 +60`，ndt 檔本身未改）。
- 別人的 claim 底下的 `up`：🟢 `up p4` 回 rc 5、什麼都沒建（09-24 live）。🟠 OVS 的 `up` 在碼裡同樣由 ndt 的 guard 回 rc 5（trunk 上 `68ace017` 起，`tools/test_workflow/ndt:4362`），**沒有在 lab 上跑過**（not run live）。
- 🟠 一次性連結、指令預覽、apps／cells 要自己的 claim：都在碼裡，都是 09-24 之後加的，沒在 lab 上跑過（not run live）。「別台機器連不到」「跨源被擋」是推的（INFERRED）。
- ❌ 不說「ndt serve 已經安全」或「做過滲透測試」。

### S3 `Live cells: two guided walks, 09-24`　form: figure　`ndt-serve/fig_s3_cells_and_walks`
- old／new 凍結格的概念 **9/16 已講過**（916 第 7 頁 CELL 框）；這頁的新東西是 ndt serve 的 API、guided walk，以及 09-24 兩條 live walk。
- 🟠 上方細帶是 walk 的步驟名：old → new →（lab 格才有 status、claim）→ run →（release）→ compare → verdict（判定一定留給人；`RULINGS-0927-ndtserve-gui-v2.md:15-18`、`tools/ndt_serve/cells.py:285-309`）。
- old／new 兩列是 09-10／09-11 的凍結紀錄，放在 09-16 前的灰底背景帶裡（圖右上有圖例）；run 列是 09-24 的 live。
- 🟢 09-24 走了兩格（ndt blob `3273df8b`，checkout `fd7382a3 +60`）：`help_drops_deleted_claims` 6 條斷言，old 4 紅，重跑 6 條全 ok、PASS；`up_target_names_a_readable_model`（OVS 4 台）9 條，old **4 紅＋4 條 fixture gap**（存檔缺檔，不算缺陷證據；圖上斜線），重跑 9 條全 ok、PASS。old 的日期 09-10／09-11 是 UTC（檔內 +08）。
- 兩條 walk 在 09-26 由 Adam 判 green（`I/walks/*.json`）——判定不在圖上。
- ❌ 不說「11 格都在 lab 上重跑過」——live 重跑的只有這兩格。

### S4 `Where the ndt serve page goes`　form: table
投影片上是這張表；`ndt-serve/fig_s4_gui_plan` 留作存檔。

| stage | stack | served by | refresh | state (UTC) |
|---|---|---|---|---|
| v1 | static HTML + JS + CSS, no build step | ndt serve, 127.0.0.1 only | manual; job log re-read every 2 s | merged `f186ce98`, 09-27 12:35 |
| v2 | React · Vite · Tailwind · TypeScript · i18next | ndt serve, 127.0.0.1 only | every 10 s; paused while measuring | ruled 09-27; on a branch, no page yet |
| one app with Web-GUI | Web-GUI's | undecided | — | long-term; not scheduled |

- v1：🟠 `tools/ndt_serve/serve.py:84-86`、`:453-458`；`static/app.js:433`；`I/RULINGS-0927-ndtserve-gui-scope.md:16`（這一刀只手動更新）。
- v2：🟠 `I/RULINGS-0927-ndtserve-gui-v2.md:22-30`（Adam 09-27 約 13:1xZ 裁）；技術棧＝Web-GUI 的（`~/Web-GUI/package.json:23`、`:26`、`:52`、`:53`、`:55`）；仍由 ndt serve 送、紅線不變。
  分支 `feat/ndt-serve-gui-v2-0927`（tip `6d5621ab`，09-28 重查）：**還沒有頁面檔、未併**。
- 合一：🟠 同檔 `:32-47`（「not scheduled」在 `:43`）；得先解決 Web-GUI 對外開 `0.0.0.0:3000`（`~/Web-GUI/docker-compose.yml:52-53`）與 ndt serve 只聽本機的衝突。見 N2 第 4 題。

### M1 `Sampling error of two telemetry paths`　form: figure　`telemetry/fig_m1_sampling_error`
- 這是 Adam 09-17 要的「兩種遙測在同一個 fabric 上量、做比較圖」（`E/PLAN-0917-exercise-support.md:149`）。
- 🟢 第五次 campaign（2026-09-19 11:57Z 起，`K/doc/audit/2026-09-19_telemetry-three-groups/raw/2026-09-19T115737Z_full/summary.json`；kernel sha256 `be70b5dd3235…`、bmv2 `3ff54b5c1901c9d3…`——各取自該序列自己那一代的 arm.meta：cooperative `…/G2/cooperative_f64_a/arm.meta:12-15`、link `…/G3/link_f64_a/arm.meta:12-15`，腳本斷言兩代同一組 binary；code `4d3f294f +60`；audit-raw `797c34ab`）：20／100 Mbit/s 兩條路誤差都在 1.5–3.4%；**2 Mbit/s 時 cooperative 29.5%、link 7.5%**。
- 空心點＝在帶外：只有 cooperative 2 Mbit/s（29.5% 對帶頂 28.5%，圖上畫出帶頂並標值；腳本對 `summary.json` 的 `position` 欄斷言）。
- 判決（組級，FINDINGS §3）：link＝H-B1 成立（誤差就是取樣雜訊）；cooperative 2 M 在帶上方——PREREG 沒註冊的結局，**只報數字不貼標籤**；「兩條路一樣準」（H-B4）不成立（2 M 比值 0.253）。
- 🔴 pps 天花板這台機器量不出來：判別輪同一臂同一階 20 kpps，爬梯時三次中位數 0.2532%（clean），確認時三次中位數 0.5276%（不過 0.5% 門檻）——門檻落在同一階的重複量測之間（raw `…/raw/2026-09-19T130352Z_G2/G2/cooperative_f64_a.log:8`、`:15`、`:17`；kernel `be70b5dd…`、bmv2 `3ff54b5c…`，arm 起跑 13:07:34Z；code `4d3f294f +60`）⇒ ❌「遙測把天花板壓低 N 倍」，也不給 pps 對比。CPU 這頁不談。全部在 protobuf 5 之前量的。

### N1 `The road to “bring your own .p4”`　form: figure　`next/fig_n1_roadmap`
- 狀態由腳本用 git 算、釘在 trunk `3368412d`（右上 as-of）：cut 1（`572d9462`）、cut 2（`cafd518a`）、**cut 3 的 kernel 側（`85bec430`，09-28）**已併；cut 3 的 GUI 側（把 switch 做不到的操作變灰）在 `~/Web-GUI` 的本機草稿分支上（`draft/p4-capabilities-0924`，未推；要不要推由 Adam 定）。
- 還沒開始：twin 看得見自訂標頭的流量（六、七支目前只能說「轉得動」）；多表 roles（load_balance）、tunnel、五元組 role（ANALYSIS §8 裁決 4 列為「之後」）。
- 教授的目標「帶自己的 .p4 來、NDTwin 把它模擬起來」在最右；**不承諾日期**。

### N2 `Open questions`　form: table
| question | why we ask | if yes | if no |
|---|---|---|---|
| next: custom headers, or multi-table roles? | one person, two roadmap items | observation side table → flow identity | load_balance template first |
| is "about 20 s" link detection enough? | same class as NDTwin's own LLDP | keep one shared watchdog | event-driven pass, ≈15.5 s design worst |
| re-measure the pps ceiling? | not resolvable on this machine | one night, a new preregistration | report sampling error only |
| ndt serve + Web-GUI as one app: which guard? | Web-GUI listens on 0.0.0.0:3000 | loopback-only Web-GUI | login or an auth proxy |
| "bring your own .p4": what counts as done? | defines the next cuts | forwarding + link view | + per-flow view of its own headers |

- 第 1 題：兩件都在 N1 上。自訂標頭的現況見 T7；非 IPv4 的流身份目前只進上限 1024 筆的側表（🟠 `K/include/ndt_core/collection/FlowLinkUsageCollector.hpp:747`）。
- 第 2 題：Adam 09-27 已在內部接受「約 20 s」（H5 頁）；事件驅動 pass 最壞約 15.5 s 是設計推算（INFERRED，`I/judge-HBW-1a3ebd7f.md:73`）。
- 第 3 題：量不出來的原因見 M1（raw `cooperative_f64_a.log:8`、`:15`、`:17`）；換工作點要**先**註冊再取資料，一晚約 1.5 小時機器時間（REPORT-P3-2026-09-24.md:9-19）。
- 第 4 題：v2 裁決列的三個候選：Web-GUI 只聽本機、加登入、或帶自己驗證的 proxy（`I/RULINGS-0927-ndtserve-gui-v2.md:32-47`）；合併會動到公開的 Web-GUI repo，需要 PR 與別人審。
- 第 5 題：這決定第三刀之後要做到哪裡。

### N3 `What we do not claim`　form: table
| we do not claim | because | evidence |
|---|---|---|
| NDTwin operates any foreign P4 | roles bind one dst-IP table; no link detection under an external controller | route_binding.py:159-161; h14 log :168 |
| the twin observes custom headers | own-frame evidence only for 0x1212 | T7; GAP-2b §3 |
| telemetry lowers the pps ceiling | no resolution at 20 kpps | cooperative_f64_a.log :8, :15 |
| detection ≤ 20 s, guaranteed | one watchdog phase sampled | 30_cycles.tsv: phase 1.49–1.76 s only; design bound ≈ 20 s |
| flowcache G1 PASS = delivered | flow reached s1→s3 only; h3 got nothing | netdev s3-eth1 +273 B; iperf_server.txt; iperf_client.txt :10 |
| the serve GUI ran on the lab | stub server only | ndt-serve-gui REPORT :10 |
| users already have this work | the manual's clone target stops at 09-03 | FIXED-SINCE-916 §8–§9 |

- 這一頁延續 916 的誠實頁：每一條都是有人想講、而證據撐不住的說法。完整路徑在 `README-930.md` 與各圖 `.md`。
- 第 1 列：證據＝roles 只綁一張目的 IP 表（`route_binding.py:159-161`），以及帶自己控制器的 exercise 沒有斷線偵測（🟢 `I/hbw-live/h14-20260926T152605Z.log:168`）。
- 第 4 列：🟢 `L/2026-09-26T152605Z_08_heartbeat/30_cycles.tsv` 的 `watchdog_phase_s`：H1 六次 1.493–1.755 s（同 run `64_cycle.tsv` 的 H3 一次 1.474 s），全落在 5 s 週期裡不到 0.3 s 寬的一段（repo `cafd518a +85`（髒）、kernel `be70b5dd32356847`）。🟠／INFERRED 設計上界（H5 頁）：φ→0、ψ→5 s ⇒ 20 s 再加 d＋ε，約 20 s。最壞 ψ 沒被量到，所以不說「保證 ≤ 20 s」。
- 第 5 列：🟢 `FC/link_usage/netdev.before:3`→`netdev.after:3`（s3-eth1 3531 → 3804 B，+273）、`FC/link_usage/iperf_server.txt`（沒有報告列）與 `iperf_client.txt:10`（沒收到 ack）；FC＝`E/runs/2026-09-27T081256Z_flowcache_solution_ndtwin`。只有 client 那一行只能說「最後的 ack 沒回來」，不能說「0 個送到」。這一列界定 T1、T7 的 flowcache 格（IPv4 only）。
- 第 6 列的完整路徑：`doc/audit/2026-09-27_ndt-serve-gui/REPORT.md:10`。
- 第 7 列：手冊叫人 clone 的那個 repo 停在 09-03 的 `9e6cc307`（`FIXED-SINCE-916.md` §8–§9；未認證查核 09-28 06:20:07Z 與 08:38:41Z 都一樣，`figures/fixed-since-916/public-check-20260928b/branch_P4-public_main.json`）。本 deck 講的 package、roles、心跳、ndt serve 都是 09-17 之後才進 trunk 的，照手冊裝的人一樣都拿不到。

## 3. 出處速查（每頁的全部 path:line 在該圖 `.md`；這裡只列最常被問的）

| 數字／主張 | 出處 | commit／binary |
|---|---|---|
| B1 13 支的標頭、灌表方式 | tutorials `c80d83e` 各 exercise 的 solution `.p4`、`topology.json`、`sN-runtime.json`、README；GAP-1 §2、§3 | 🟠 讀；`slides930/b-section-sources-20260929T0741Z.log` B1 段 |
| B2、B3 圖上的名字、常數、埠、entry、路徑 | tutorials `c80d83e`（`git show`）；錨點行號在 `fig_b2_basic_walkthrough.md`、`fig_b3_basic_tunnel.md` | 🟠 讀；紅檢 81/81 |
| B4 九列（09-16 缺什麼） | GAP-2（`1a284f75`）、PLAN-0917 §0／§3.2（`70615ec5`）、ANALYSIS `:26`、`:338`；`70615ec5` 上 `git grep` 重核 | 🟠 讀；同一份 log 的 B4 段 |
| B5 ran live 欄 | T06 各解答臂（entries applied、group 1/1、G1 10/13）；07 `21_proxy_roles_lines.txt:2`；08 `30_cycles.tsv`；07 `30_／71_switch_state_*.json` | 🟢 `5dc7fc9a +95`、`b2eeb71d +92`、`cafd518a +85`；同一份 log 的 B5 段 |
| T06 26/26（protobuf 5 之後） | T06 `00_table.tsv`；`I/pb5-merge/live-accept.log:6-7` | code `5dc7fc9a +95`、bmv2 `3ff54b5c1901c9d3`、p4c `226f3f66df515c9e`；audit-raw `797c34ab` |
| 1／9／6 → 8／6／2 | GAP-2 §1、GAP-2b §1「計數」行 | GAP-2b 四格 09-28 Adam 裁定；提交 `c8433963`（已公開） |
| twin 6／4／3 | GAP-2b §3（裁定後）；flowcache＝IPv4 only（與 T7 同字）的 raw：`FC/link_usage/twin_integral.txt:3`、`:7-9`，`netdev.before:3,7`→`netdev.after:3,7`（`fig_t1c_ndtwin_coverage.md`） | 同上；`5dc7fc9a +95` |
| 21–25 pre-flight checks | T06 各 arm report 的 pre-flight 區塊；`L/2026-09-26T202055Z_07_roles_basic/12_preflight_basic_roles.txt` | `5dc7fc9a`／`b2eeb71d` |
| 16 of 16 initial routes | `L/2026-09-26T202055Z_07_roles_basic/21_proxy_roles_lines.txt:2` | `b2eeb71d +92` |
| 07 cut 8/12 → 3/12（只記錄） | 兩次 07 的 `54_pingall_during_cut.txt` | `572d9462 +61`／`b2eeb71d +92` |
| 16.8／12.2–16.8／4.6–5.1 s | `L/2026-09-26T152605Z_08_heartbeat/30_cycles.tsv`（`detect_s`、`restore_s`） | `cafd518a +85`、kernel `be70b5dd32356847` |
| H3 16.607 s | 同目錄 `64_cycle.tsv` | 同上 |
| 14.972＋1.610＋0.245 | 同 `30_cycles.tsv` cycle 3 | 同上 |
| ψ 1.474–1.755 s | 同上 `watchdog_phase_s`（H1 1.493–1.755、H3 1.474） | 同上 |
| 相位鎖 18 次 14.197–14.382＋13.275／13.298；去相位 10.077–14.904、10.668–14.791 s | `K/doc/audit/2026-09-25_p4-heartbeat/spike/runs/2026-09-26T{023021Z,052148Z,085020Z,085506Z}_S_heartbeat/20_cycles.tsv` | `4bc1201b +79`／`580767a8 +79`／`094f417f +84` |
| 17 sessions、0 幀（1645 筆輪詢） | `L/2026-09-26T172912Z_08_heartbeat/50_samples.tsv` | `3f8c2abf +89` |
| 29.5%／7.5%／2.7%／3.4%／1.5%／2.3%；帶頂 28.5% | telemetry `summary.json` `sampling_error_by_group` | kernel `be70b5dd…`、bmv2 `3ff54b5c…`（`G2/cooperative_f64_a/arm.meta:12-15`、`G3/link_f64_a/arm.meta:12-15`）；`4d3f294f +60` |
| 0.2532%／0.5276%（只在講稿，不上圖） | `…/raw/2026-09-19T130352Z_G2/G2/cooperative_f64_a.log:8`、`:15`、`:17` | kernel `be70b5dd…`、bmv2 `3ff54b5c…`；`4d3f294f +60` |

## 4. 圖面清單（32 頁用 24 張圖＋1 標題＋7 表；全部 matplotlib，產物＝pdf／png 300 dpi／svg／`_hires` 500 dpi＋同名 `.md`）

| 圖 | 頁 | 產生器 | 狀態／紅檢 |
|---|---|---|---|
| `background/fig_b2_basic_walkthrough`、`fig_b3_basic_tunnel` | B2、B3 | `make_background_figs.py`（新，09-29） | 全部讀自 tutorials `c80d83e`（`git show`），錨點缺就具名停下；圖上標「READ · p4lang/tutorials c80d83e」；紅檢 `slides930/make_background_figs-redcheck-20260929T0740Z.log`（81/81，對照組綠，2 個停止點到不了、理由在 log） |
| `p4-tutorials/fig_t1c_ndtwin_coverage` | T1 | `make_coverage_0930.py`（import `make_tutorial_figs_0927.py` 的解析） | 四個判斷格已裁定（09-28）；09-16 列在背景帶；twin 欄標 JUDGED；09-27 列標 RAN · JUDGED；圖例「cannot · read only」；紅檢 `slides930/t1c-coverage-redcheck-ruling-20260928T0654Z.log`（12/12 停下、對照綠）；它 import 的 `make_tutorial_figs_0927.py` 紅檢 `slides930/make_tutorial_figs_0927-redcheck-20260928T0656Z.log`（69/69） |
| `foreign-p4/fig_a1_foreign_p4_path` | T3 | `make_foreign_p4_diagram.py` | 圖上沒有跑出來的數字（21–25 由腳本數、只在 `.md`）；上排標 RAN IT、下半標「RAN IT: the boxes · READ THE CODE: the arrows」；紅檢 `slides930/make_foreign_p4_diagram-redcheck-20260927T2005Z.log`（2/2） |
| `p4-tutorials/fig_t6…`、`fig_t7…`、`fig_t8…`、`fig_t9…` | T4–T7 | `make_exercise_path_figs.py` | 紅檢 `slides930/o1-o2-t6-t9/` |
| `roles/fig_r2…`–`fig_r4…` | R2–R4 | `make_roles_figs.py`（`--only` 可只畫一張） | 紅檢 `slides930/roles-flowapi-redcheck*`（12/12；v1.8 重跑 `…-20260929T0812Z.log` 相同）；r4 只畫 09-26 那次 07 的最後狀態、圖上不印 sha，它的停止條件 `slides930/make_roles_figs-redcheck-20260929T0810Z.log`（11/11，對照 2/2） |
| `heartbeat/fig_h1…`、`fig_h2…` | H3、H4 | `make_heartbeat_figs.py` | h1 的 frame lost 標 inferred；h2 有放大內嵌圖、H1／H3 分形狀、色帶與 20 s 線標「design bound (derived)」；紅檢 `slides930/make_heartbeat_figs-redcheck-20260927T2000Z.log`（9/9） |
| `heartbeat/fig_h0…`、`fig_h0b…`、`fig_h3…`、`fig_h4…` | H1、H2、H5、H6 | `make_heartbeat_extra_figs.py` | 圖上常數由碼讀出並斷言；h0 的底行改用 09-24（心跳之前）並標 RAN IT、兩個小圖標 READ THE CODE；h4 單位＝17 sessions；圖底停止條件紅檢 `slides930/h0-footer-redcheck-20260927T1941Z.log`；其他 `slides930/make_heartbeat_extra_figs-redcheck-20260927T2001Z.log`（12/12） |
| `flow-api/fig_d1…` | D1 | `make_flow_api_matrix.py` | 09-16 前兩列的 RAN IT 格在灰底背景帶，READ 格在帶外（trunk `3d740be0`）；紅檢 `slides930/make_flow_api_matrix-redcheck-20260927T2003Z.log`（15/15） |
| `flow-api/fig_d2…` | D2 | `make_queued_readback.py` | 紅檢同 roles |
| `ndt-serve/fig_s1…` | S1 | `make_serve_diagram.py` | BIND／port 由碼讀出；紅檢 `slides930/make_serve_diagram-redcheck-20260927T2002Z.log`（一個合併停止條件，5/5） |
| `ndt-serve/fig_s2…`、`fig_s3…` | S2、S3 | `make_serve_s2_s4.py`（`--only` 可只畫一張） | s3 的 old／new 列在 09-16 前背景帶；s2 的 up/down 列只畫最後狀態（OVS＝碼裡 rc 5、not run live），它的停止條件 `slides930/make_serve_s2_s4-redcheck-20260929T0811Z.log`（8/8，對照 4/4）；紅檢 `slides930/ndt-serve-s2s4-red-checks-r3-20260927T1948Z.log`（9/9；v1.8 重跑 `…-v18-20260929T0812Z.log` 9/9）；S3 日期停止條件 `slides930/make_serve_s2_s4-s3date-redcheck-20260927T2003Z.log`（3/3；v1.8 重跑 `…-20260929T0812Z.log` 3/3） |
| `telemetry/fig_m1…` | M1 | `make_sampling_error_fig.py` | 帶外的點空心；binary 取各代自己的 arm.meta；紅檢 `slides930/m1-sampling-error-redcheck-r2b-20260927T1854Z.log`（6 個停止條件、7/7 竄改） |
| `next/fig_n1_roadmap` | N1 | `make_roadmap.py` | 狀態由 git 算、釘在 `3368412d`（as-of 在圖上）；不含 detect-only（存檔 `fig_n1_roadmap_with_detect_only.*`，`--with-detect-only` 重生）；紅檢 `slides930/make_roadmap-redcheck-20260928T0847Z.log`（5/5） |

**不上 deck、只留存檔**：09-29 拿掉的頁的圖（Adam：不要開發史與除錯史）——`overview/fig_o1_since_0916`、`overview/fig_o2_thirteen`（A1、A2）、`p4-tutorials/fig_t5_arms_by_run`（T2）、`engineering/fig_q1_protobuf5`、`fig_q2_review_path`、`fig_q4_ci_state`、`fig_q5_main_by_pr`（Q1、Q2、Q4、Q5）、`fixed-since-916/fig_f1_fixed_since_916`（F1）；它們的產生器、紅檢與 `.md` 不變，原本的圖清單列在 `README-930.md` §13。更早的：`next/fig_n1_roadmap_with_detect_only`（第二輪；Adam 09-28：分支併入前不放回）、`p4-tutorials/fig_t1b_requirements_matrix_0927`（916 的 13×16，判官 F-2）、`roles/fig_r1_four_rulings`（F-5 → R1 表）、`ndt-serve/fig_s4_gui_plan`（F-13 → S4 表）、`engineering/fig_q3_review_catches`（F-13 → Q3 表）。

`slides930/`＝`K/scratch/overnight-2026-09-05/logs/slides930/`（git-ignored）。每張圖 `.md` 的「最後產出」行記產圖時間（UTC）與產生器的 sha256。重生：每張圖的 `.md` 末有指令；Python 一律 `"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3"`。
