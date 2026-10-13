# NDTwin 進度報告簡報 — 2026-09-16 版・資訊模板

**v0.6（09-16：§1 頁序重寫成 43 張圖／七段的完整存貨＋建議核心 26 頁；新增 §6c–§6f 四節逐頁規格；v0.5 09-15 新增 §0 規則 6）。本檔是唯一事實來源，Adam 直接編輯；產檔由 Adam 的 cowork session 跑 JS 產生器（本機無 Node），動工前先讀最新版。**
v0.2 全文（含被刪掉的圖規格與更正紀錄）在 `_superseded/NDTwin-slide-template-916_v0.2-full_0908.md（909 原稿）`。

## 0. 六條規則

1. **只講 09-03 之後的事。** 903 講過的一頁不放、不提（Adam 09-08 裁）。09-08 17:56 產的 31 頁 `NDTwin_deck_909.pptx`／`.pdf`（已移到 `_superseded/`）含 903 的 23 頁 ⇒ **作廢，照 §1 重產為 `NDTwin_deck_916`。**
2. **圖頁只放圖。** p.2、p.5–p.8、p.A、p.B＝標題＋一張圖撐滿內容區（寬 ≥ 12"），**沒有 caption、kicker、chip、判詞**（Adam 09-08：字太小、口頭講）。要講的全進講者備註。p.7 兩張並排各半寬，嫌小就拆兩頁。
3. **圖檔**：`figures/<主題>/<name>.{pdf,png,svg}`＋`_hires/`＋同名 `.md`（資料來源、可信度、regenerate）。現有的全是 **matplotlib 草稿**（數字與結構對帳過）；定稿由 Adam 交另一位 agent，以草稿＋同名 `.md` 為規格。
4. **證據紀律**：每個實測數字旁標 commit；🟢 親自執行／🟠 讀過未執行**不可混寫**；場地名不上台面。頁腳統一 `Read at trunk 1a284f75 · exercises run 09-08 on their own harness`，不寫 `Measured at`。
5. **視覺規約**沿用 827 §E2（色票／字型）、§E3a（版面文法）、§E5（標題 ≤45 字元）：`../NDTwin slide material 827/NDTwin-slide-template-827.md`。
6. 🔴 **版面只有四種元件**（Adam 09-15 裁，常設）：**表格／大標題／架構圖／資料視覺化圖**。
   這四種**以外的東西一律不上投影片**——散文句、bullet 清單、副標句、caption、kicker、chip、判詞、說明段，全部進**講者備註**。
   **How to apply**：每頁先選它是哪一種（一頁一種為主，表格頁可帶大標題）；寫不進表格的話就是它不該上台，改口頭講。
   句子想留在台上時的唯一出路＝**把它拆成表格的欄**（左欄名目、右欄值），不是縮小字級塞進去。
   ⚠️ **既有頁面不合規、要改**：p.3（左右欄＋散文＋底部裁決一行）與 p.9（三列 label→value 可留，但講者備註裡的散文不得上台）
   ——p.3 要重做成**一張兩欄表**（`寫 is_up 的人 → 它的意思`）＋**一張後果表**（`量到的 → 值`），副標句刪掉。

## 1. 頁序

> 🔴 **09-16 重寫。舊的「11 頁」表已作廢**——它停在 09-10，而 09-15／09-16 之間新增了 29 張圖。
> **現在素材是 43 張圖、如果一張一頁就是 45 頁左右，那超過一場報告講得完的量。**
> 下表是**完整存貨**，分成七段；`✅` 是我建議的核心 26 頁，`○` 是可略。**最終取捨與頁碼 Adam 定。**

| 段 | 頁 | 內容 | 圖 | 規格 |
|---|---|---|---|---|
| **A 開場** | ✅ A1 | Title | — | — |
| | ✅ A2 | **用需求驅動測試**（本報告的主軸） | 無，做成 §1b 那張兩列表 | §1b |
| **B 需求來自外部的程式**<br>P4 tutorial | ✅ B1 | What the tutorials ask for | `p4-tutorials/fig_t1_requirements_matrix` | §5 |
| | ✅ B2 | Where the five gaps live | `fig_t2_gap_architecture` | §5 |
| | ✅ B3 | What only a foreign P4 program reveals | `fig_t3a_silent_zero`＋`fig_t3b_election_wipe` | §5 |
| | ○ B4 | Three phases to a regression gate | `fig_t4_phases` | §5 |
| **C 需求來自外部的人**<br>夜巡與角色扮演 | ✅ C1 | One night of the hunt | `overnight-hunt/fig_m1_hunt_pipeline` | §6b |
| | ✅ C2 | A role is two assumptions, crossed | `fig_m2_persona_axis` | §6b |
| | ✅ C3–C9 | **七種實驗方法，一頁一種**（蓋住 11 個角色） | `fig_f1_successor_first` … `fig_f7_manual_follower` | §6c |
| **D 角色找到了什麼**<br>🔴 **這一段是我們自己的工具** | ○ D1 | 機器空了而分身不知道 | `fig_r2_empty_but_confident` | §6d |
| | ✅ D2 | 同一個欄位，兩扇門相反的答案 | `fig_r3_two_doors_one_field` | §6d |
| | ✅ D3 | 兩個人同時被告知實驗室是他的 | `fig_r4_claim_race_window` | §6d |
| | ○ D4 | 拆除標記沒有主人 | `fig_r12_stolen_marker` | §6d |
| | ○ D5 | 取樣的那一秒決定了結論 | `fig_r10_sampling_instant` | §6d |
| **E 我們修好的 baseline 缺陷** | ✅ E1 | One flag, two meanings（Q12） | 無圖，**要改成兩張表** | §3 |
| | ✅ E2 | 遙測越忙越說謊（#53） | `baseline-bugs/fig_b02_loss_ladder` | §6e |
| | ✅ E3 | 輪詢把關機的交換機寫回 up（#46） | `fig_b04_poll_resurrects` | §6e |
| | ○ E4 | 一台交換機死了，幾乎沒東西跟著死（F-14） | `fig_b07_nothing_goes_down` | §6e |
| | ✅ E5 | 刪除說沒了，group 還在（#1） | `fig_b08_delete_reports_gone` | §6e |
| | ✅ E6 | 流表早 13 秒就有那一列（#2） | `fig_b09_ghost_rule` | §6e |
| | ✅ E7 | 272 條邊剛好對（F-8） | `fig_b10_accidentally_right` | §6e |
| | ○ E8 | 會說出自己算什麼的計數器（A-7） | `fig_b11_counter_cover` | §6e |
| | ✅ E9 | 拓樸檔的 11 扇門 | `fig_b_topology_doors` | §6e |
| | ○ E10–E12 | 09-04 夜巡量到的三條（B-6／#27／#54） | `overnight-0904/fig1`／`fig2`／`fig3` | §4 |
| **F 我們建的工具**<br>🔴 **不是 baseline** | ✅ F1–F9 | `ndt` 九個指令，一頁一個 | `ndt-commands/fig_c1_up` … `fig_c9_release` | §6f |
| **G 收尾** | ✅ G1 | Found, then fixed（看板） | `fixed-since-903/fig_h1`（🔴 **必須重生**，見 §2） | §2 |
| | ✅ G2 | Where it stands | 無 | §6 |
| | ✅ G3 | **誠實頁**：這套方法自己承認的六項限制 | 無，做成表 | §6b 末 |
| | ○ G4 | 找到但沒修的（含 `fig5_path_switch_count_static`） | `overnight-0904/fig5` | §4 |

**核心 26 頁的敘事**：怎麼測（A、B、C）→ 測出什麼（D、E）→ 我們建了什麼（F）→ 帳與限制（G）。
**逐角色的 11 頁細表**（比 C 段更細）在同目錄 `ROLES-PAGE-BY-PAGE.md`；那是 C 段講不夠時的展開，不是另一段。

### 舊表（09-10，已作廢，保留供對帳）

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
| 🆕 A | One night of the hunt | `figures/overnight-hunt/fig_m1_hunt_pipeline` | §6b |
| 🆕 B | A role is two assumptions, crossed | `figures/overnight-hunt/fig_m2_persona_axis` | §6b |

🆕 **09-15 Adam：「報告內要介紹我們 overnight-hunt 的測試方式」＋「角色扮演這次會講到很多」＋「十頁以上，逐一講解每個角色的定位」**
⇒ 加 A／B 兩張總覽圖頁＋**每個角色一頁**（11 頁），逐頁內容在同目錄 **`ROLES-PAGE-BY-PAGE.md`**（13 頁的完整排版），規格見 §6b。

## 🔴 1a. **實際產出的 47 頁**（2026-09-16 產檔，`NDTwin_deck_916.pptx`／`.pdf`）

> 產生器 `generator/build_deck_916.js`；色票／版面 `require` 的是
> `../NDTwin slide material 903/generator/deck_style.js`（**同一個實例**，自動頁碼才不會中途重數）。
> 逐頁 50／95 dpi 看過，零溢出、零撞行。
>
> 🔑 **取捨＝「`figures/` 裡的每一張都要上台」（Adam 09-16）。**
> §1 的 ✅／○ 是建議，最終取捨寫明由 Adam 定——這就是那個決定。
> **43 張圖全部在 deck 裡**（機器核過：`43 on disk / 43 used / 0 unused`）。
> 唯一合併的是 `t3a`＋`t3b`，那兩張本來就是設計成並排的
> ⇒ **42 張圖頁 ＋ 5 張文字頁 ＝ 47 頁**，正好落在 §1 自己估的「45 頁左右」。
>
> | 頁 | 內容 |
> |---|---|
> | 1 | Title（大標題） |
> | 2 | Requirements drive the tests（§1b 兩列表＋「為什麼有效」一列） |
> | 3–6 | 🖼 t1／t2／**t3a＋t3b 並排**／t4 |
> | 7–8 | 🖼 m1 夜巡管線／m2 角色 × 軸 |
> | 9–15 | 🖼 f1–f7 七種實驗方法 |
> | 16–20 | 🖼 r2／r3／r4／r12／r10（§1 的 D1–D5 全收） |
> | 21 | One flag, two meanings（Q12，**兩張表**） |
> | 22–29 | 🖼 b02／b04／b07／b08／b09／b10／b11／b_topology_doors（E2–E9 全收） |
> | 30–33 | 🖼 09-04 夜巡 fig1／fig2／fig3／fig6 |
> | 34 | 🖼 09-04 夜巡 fig4（**有 after 側，所以不掛 4b 標**，見下） |
> | 35–43 | 🖼 c1–c9 `ndt` 九個指令 |
> | 44 | 🖼 h1 看板（**本次重生**） |
> | 45 | Where it stands（三列表） |
> | 46 | What this method admits about itself（七列表） |
> | 47 | 🖼 09-04 夜巡 fig5（§1 的 G4：找到但沒修的） |
>
> **沒有做節封面頁，改用頁首小標**，因為 §6d 與 §0.3 都警告「教授會以為我們修的是別人的系統」
> ——節封面只看得到一次，頁首小標整段都在螢幕上。七個標：
> `REQUIREMENTS DRIVE THE TESTS`／`1 · …OUTSIDE PROGRAMS`／`2 · …OUTSIDE PEOPLE`／
> `3 · WHAT THE ROLES FOUND`／`4 · BASELINE DEFECTS WE FIXED`／
> **`4b · MEASURED 09-04 · BEFORE THE FIX`**／`5 · THE TOOL WE BUILT — NOT BASELINE`／
> `6 · WHERE IT STANDS`。
>
> 🔴 **`4b` 那個標是刻意的，而且它替規則 6 解決了一個問題。**
> §4 的紅字口徑是「圖上是修之前；修法已在 trunk 且已公開，after 側還沒量」——
> 那句話在規則 6 下**不能當 caption 放上頁面**。把它放進**頁首小標**就合法了
> （小標是每一頁本來就有的導覽元件，不是說明文字），而且它在那四頁上**整段都看得見**。
> ⚠️ **`fig4` 不掛這個標**：六張裡只有它有 after 側（kernel `4c9e0be1`），
> 掛「before the fix」在那一頁上就是假的 ⇒ 它回到 `4 · BASELINE DEFECTS WE FIXED`。
>
> ### 🔴 規則 6 怎麼落地的（四種元件以外一律不上台）
>
> | 頁 | 它是哪一種 | 被搬去講者備註的 |
> |---|---|---|
> | 2、21、45、46 | **表格**（＋大標題） | §1b 的 🔑 共同句、Q12 的副標與「一個 bit 分不出…」、§6 的公開查證方法 |
> | 1 | **大標題** | — |
> | 其餘 43 頁 | **架構圖／資料視覺化圖** | 全部 caption、kicker、chip、判詞 |
>
> - **label→value 列保留**，因為規則 6 自己給的出路就是「拆成表格的欄」
>   ⇒ 這幾頁一律用真的 `addTable`，不是排版成表格樣子的文字框。
> - **圖頁沒有頁標題**：每張圖畫布裡已經有自己的標題，再加一個既重複又違反規則 2
>   （827 §E-delta-2 同一條）。圖頁上只有頁首小標與頁碼。
> - Q12 與 Where it stands 留了頁底出處行——那是 A2b 的 commit 標記，不是 caption。
>
> ### 三個產檔裁定
>
> 1. 🔴 **`fig_h1` 重生了**（§2／§8 標「現況會把假訊息送上台」，照辦）：
>    - `ON BRANCHES · NOT MERGED` 整條帶子刪掉，29 塊磚移進 trunk 帶、日期記 **09-10**；
>      虛線磚與 09-05 的 `last merge` 垂直線一起拿掉——沒有東西要分開了，虛線會變成沒有意義的裝飾。
>    - chip 換成 **`104 FIXES ON TRUNK · 0 WAITING · ALL PUBLISHED`**，判詞 **`FIXED AND SHIPPED`**。
>    - **09-02 那一欄（20 塊帶 `?`）拿掉**——§2 標成待 Adam，但規則 1（只講 09-03 之後）
>      已經隱含這個答案，這是讓這一頁留在 deck 自己範圍規則內的讀法。
>    - 順手修兩個渲染瑕疵：`ON TRUNK` 帶名用的 U+2009 在 Liberation Sans 缺字會渲成豆腐
>      ⇒ 單帶之後帶名本來就多餘，直接刪；`+7 docs` 原本壓在最右那塊磚上 ⇒ 移到格線下方。
>    - 空出一整帶之後，每欄 8 列改 10 列（磚更寬）、磚高 0.21→0.26、字級上限 7.0→8.6
>      ⇒ **磚上的字明顯變大**，畫布 7.00"→6.30"。
>    - 🔴 **要知道的不一致**：chip 說 104，板上只有 **76 塊磚**。板子畫的是「有逐筆紀錄、
>      排得上日期」的修法；104 是 trunk 總數（含 09-12 那批與 §2.5）。**兩個是不同的量**
>      ——被問到就這樣答，不要說「板上就是全部」。
> 2. 🟠 **`fig_t1` 重新渲染過**（Adam：有些圖字太小）。原畫布 9.2×6.6（ar 1.39），
>    在 16:9 上**高度受限** ⇒ 只用到 8.9" 寬，8.8pt 標籤到螢幕只剩 ~8.5pt。
>    改成 **13.3×6.6（ar 2.02）** 吃滿 12.6" 寬，字級同步放大（列標 13.2、格標 11.8、
>    標題 21）⇒ 螢幕上約 12–13pt。**資料一格沒改**，腳本 15 條計數斷言照跑。
>    🆕 產生器的 repo 路徑改成吃 `NDTWIN_REPO` 環境變數（預設值不變，Adam 那邊照舊）。
> 3. 🟠 **t3a／t3b 沒有拆兩頁，維持並排。** §0 規則 2 說「嫌小就拆兩頁」，但這兩張 ar ≈ 0.98，
>    **單獨一頁也是高度受限**（h 6.24 ⇒ w 6.11），跟並排拿到的寬度一模一樣
>    ⇒ 拆頁多花一頁、尺寸一點沒變。已逐頁確認並排版本讀得到。
>
> **剩下的取捨留給你**：47 頁是「全部素材」的長度，不是一場報告的長度。
> 要砍的話 §1 的 ○ 記號就是現成的砍序（十頁：B4、D1／D4／D5、E4／E8、E10–E12、G4），
> 砍完回到 37 頁；再砍就得動 C3–C9 或 F1–F9 那兩段。

## 🔴 1b. 這份報告的主軸（Adam 09-15 點出，**它改變了整份 deck 的敘事順序**）

原話：「**教授當初叫我去做 p4 tutorial 就是想要用需求來驅動測試。**」

⇒ **P4 tutorial（p.5–p.8）與角色扮演（p.A、p.B、11 頁角色）不是兩個題目，是同一個方法的兩半。**

| | 需求從哪來 | 拿來驅動什麼 | 結果 |
|---|---|---|---|
| **外部的程式** | `p4lang/tutorials` 的 13 支 exercise——**別人寫的、不是為我們寫的** | 逐支對 16 個能力維度，盤 NDTwin 做不做得到 | 5 個缺的能力；**2 條只有跑別人的程式才會暴露** |
| **外部的人** | 六種真實操作者的**動機**——接班、趕論文、照手冊、併發、壓流量、重開循環 | 派他們上機，看他們踩到哪組沒被一起想過的假設 | 兩夜 11 輪，數十條缺陷 |

🔑 **共同的一句**：**我們不再只測「我們想得到要測的東西」，而是讓外面的需求告訴我們要測什麼。**
自己寫的測試只走作者想過的路；**外部需求會走到作者沒想過的地方**，而 bug 就住在那裡。

**⇒ 建議的敘事順序（頁碼 Adam 定）**：
① 主軸這一頁（本節做成一張兩列表）→ ② 需求來自外部程式（P4 tutorial 四頁）→
③ 需求來自外部的人（角色扮演總覽兩頁＋逐角色）→ ④ 找到並修好了什麼 → ⑤ 誠實頁。
**「怎麼找的」放在「找到什麼」前面**——後面每一頁的可信度都靠前面這幾頁撐。

## 2. p.2 Found, then fixed — since 09-03（圖頁）

資料正本 `FIXED-SINCE-903.md`（同目錄；每列附進 trunk 的 commit／分支 tip＋證據；09-08 一支 opus agent 逐格核過）。
圖＝看板（磚 × 日期 × 兩帶）；chip 與判詞都在圖裡。
🔴 **09-15 更正：舊 chip `47 FIXES ON TRUNK · 29 BRANCHES WAITING · 0 ON THE PUBLIC REPO`＋判詞 `FIXED / NOT SHIPPED` 全部作廢、不可上台。**
新口徑（查證見 `REPORT-PICK-FIXED.md` §0.1）：`104 FIXES ON TRUNK · 0 WAITING · ALL PUBLISHED`、判詞 `FIXED AND SHIPPED`。
29 支已於 09-10 全數併入；兩個公開 repo 的預設分支 `main` 都含全部 baseline 修法（未認證 compare `behind_by: 0`）。
🔴 **待 Adam**：09-02 那一欄 20 塊（切點前一天，磚帶 `?`）——09-03 講過就拿掉：把 `make_fixed_since_903.py` 的 `TRUNK_0902` 清空重跑。
要細講哪幾支：`REPORT-PICK-FIXED.md`（同目錄，Adam 挑；09-10 尚未挑）。

**講者備註**
- 🔴 **09-15 改口徑**：09-03 之後 trunk 多 **104 支**修法（47 到 09-05 ＋ 57 到 09-12），**全部已公開發布**。舊講稿「沒有一顆推到公開 repo」**作廢**。
- 絕大多數修法有變異閘門看過紅；例外寫在正本證據欄（#85 的 TESTBED 半、#64/#65 那支閘門 auditor 沒重跑）。標 live 的在 lab 親自重跑過。
- Q12 是唯一 breaking change。🔴 **「修在 trunk ≠ 使用者拿得到」09-15 起不成立**：09-12 兩個 P4 本體轉公開，預設分支就含全部修法。

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

**講者備註**：🔴 **09-15 更正——舊備註寫 fig1／fig3 的修法「都未併」，那已經過期、不可再講。**
兩條都在 09-10 併進 trunk 並已公開：B-6（W8／W8b）→ merge `8b51caf4`／`fe2b03b8`；#54（W11）→ merge `31ae5d13`。
⚠️ **但圖本身仍然只有 before 側**（09-04 量的 current behaviour，binary 沒重建）⇒
口徑是「**圖上是修之前；修法已在 trunk 且已公開，after 側還沒量**」，
不要因為修好了就把圖講成修後的樣子。要補 after 側見 `REPORT-PICK-FIXED.md` §6 的選項 (b)。
下一批候補（#87 讀回狀態碼、OV-2／OV-3 狀態碼、`ndt up/down` 秒數）資料已齊，見 `scratch/overnight-2026-09-05/rounds/`。

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

🔴 **09-15 改**：舊三列（`29 branches · not merged`／`0 commits · on the public repo since 09-03`）**作廢**。
新三列 label→value：`104 fixes · on trunk`／`0 branches · waiting`／`phase 1 · ~140 lines · unlocks basic`。
**講者備註**：29 支已於 09-10 全數併入；公開狀態與查證方法見 `REPORT-PICK-FIXED.md` §0.1（兩個公開 repo 的 `main` 都含全部 baseline 修法，未認證 compare `behind_by: 0`；⚠️ 單打一次 `git ls-remote` 會拿到過期答案，要兩種管道交叉驗）；三階段第一階＝T4＋T1，驗證＝`basic` 在 NDTwin fabric 上跑通。

## 6b. 🆕 p.A／p.B　overnight hunt 的測試方式（兩張圖頁）

**規則 6 適用：這兩頁只有標題＋一張圖**，沒有 caption、沒有判詞。下面的字全部進講者備註。
資料正本＝兩張圖的同名 `.md`（`figures/overnight-hunt/`），每一格都附 `檔:行`。
🔴 兩份 `.md` 各有一節「已知限制」與「我自己下的判斷」，**上台前請 Adam 過目那兩節**。

### p.A `ONE NIGHT OF THE HUNT`　圖 `fig_m1_hunt_pipeline`

六階段管線＋一條回饋邊＋兩條並行帶。要講的三句：

| 要講的 | 一句話 |
|---|---|
| 順序是主張 | 偵察與離線證偽在前、上機在後——**六個階段只有一個碰受測系統**，所以一夜能跑 11 個角色 |
| 回饋邊是本體 | 一條發現**不以「修好」收尾**，以「它的修法前證據被凍成一個永遠會紅的判決」收尾（11 個 cell 就是這樣來的） |
| 每一輪都可作廢 | 角色上機前記基線、下機後還原並逐項比對；對不上，那一輪的觀測不算數 |

### p.B `ELEVEN ROLES, SIX OPERATORS, FIVE AXES`　圖 `fig_m2_persona_axis`

六個人格 × 五條軸的格子，格子裡是角色編號。要講的三句：

| 要講的 | 一句話 |
|---|---|
| 角色＝人格 × 軸 | 人格決定它會做什麼蠢事（接班人、趕論文的研究生、照手冊的人…），軸決定往哪壓（狀態／意圖／時間／規模／文件） |
| 派工給什麼 | 一個要扮的人、一個時間預算、**具名的假設**——回來記證實或證偽（ROLE-4 的 T3 就是證偽掉的） |
| 同一個人格會重派 | 接班人派了三次：第二、三次是**拿修好的儀器回頭量同一組觀測**（ROLE-6／ROLE-8），修法自己也要被角色測一次 |

「照手冊做的人」是唯一會發現「手冊說的和工具做的不一樣」的角色，
而 09-12 那批 `doc-1`～`doc-5` 五支修法幾乎都源自它。這句值得單獨講。

### 成文規格在哪（這套方法不是臨時起意）

🔑 **`.claude/skills/overnight-hunt/SKILL.md`，312 行**。兩張圖的結構都照它，格子裡的編號照 09-11 那一夜。
要引一句就引這句（`:137`）：

> **bug 不住在功能裡，住在假設的交界。作者寫每一行的時候心裡都有一組沒有寫下來的假設，
> 而那些假設彼此之間從來沒有被一起想過。一個好的視角＝一組作者沒有一起想過的假設。**

派新角色的入場費（`:204`）：「**每派一個新角色，先講得出它踩的是哪兩個假設的交界**——講不出來的不要派。」

### 一夜的規模（09-02→09-03 那一夜，口徑最完整）

| 量 | 值 | 出處 |
|---|---|---|
| 輪數 | 6 輪，一輪接一輪（只有一座 lab） | `2026-09-03_night-rounds/MORNING-BRIEF.md:9` |
| 編號 log | 178 份，全部入庫 | 同上 |
| 確認缺陷 | **68 條**（有證據檔、有對照組、說得出重現方式；假設與待查不計） | `MORNING-BRIEF.md:8`、`FINDINGS-ALL.md:1-4` |
| 修法 | 16 支進 trunk、8 支留分支，每支都有變異閘門 | `MORNING-BRIEF.md:11-12` |
| **閘門攔下來的假綠** | **6 個，沒有一個是讀碼看得出來的** | 同上 |

🔴 **不要說「六個 persona」**：persona 工單 5 份，其中 `PERSONA-1` 自己聲明「Not a persona」，
而 round 6 沒有對應的工單檔。**安全口徑＝「6 輪：4 份角色工單＋1 份清單式輪次＋1 輪形狀考古」。**

### 兩個「只有那個動機才問得出來」的案例（建議各一列，放進 p.A 的講者備註）

| 發現 | 為什麼只有那個角色看得到 |
|---|---|
| **#58** 同一個指令 8 次 bring-up 產生 **4 種路由表**（BFS 平手由十條並行 gRPC 的到達順序決定），而檢查它的端點 8 次逐位元組相同 | 研究生那一輪的任務**就是**「同一個實驗做兩次，看兩個數字合不合」。功能測試只問「有沒有路徑」，不問「兩次一不一樣」 |
| **#51** 高負載下分身**低報 2.76×**，而所有健康訊號都正常（線上零丟失 0/98213、每個端點回 200 且比對照組還快、`avg_link_usage` 反向上升，唯一痕跡 33 行 WARN） | 那個角色的目標明寫成「不是要弄壞它——是要**讓它在看起來健康的時候報出假的東西**，因為那才是會進論文的那種失敗」 |

### 🔴 誠實那一頁（這套方法自己承認的限制；建議做成一頁表，不要跳過）

| 限制 | 原文依據 |
|---|---|
| 偵察的假說錯誤率很高 | `SKILL.md:127`「外部 agent 沒跑過任何東西，它的假說是從讀 code 猜的，**錯誤率很高**」；09-11 實測：證實 27／推翻 12／構不到 8 |
| **儀器會自證** | `SKILL.md:194-202`：09-05 一晚踩三次（`wc -l` 少算一個、色碼夾在 token 中間讓 grep 0 命中、掃描字串撈到自己）⇒「**先驗證儀器看得見一個已知存在的東西，再相信它回報的 0**」 |
| 修法會生出更糟的缺陷 | `SKILL.md:252-263`：一條修法把 note 改寫成 `lab free`，於是實驗室一邊灌流量一邊宣告自己是空的——「**修法引入的新缺陷比原缺陷難發現，因為沒有人在找它**」 |
| 綠色不代表驗過 | `CELLS.md:58`「**a grid that is read as "the fixes are verified" is worse than no grid**」；覆蓋表自陳「整張表回答的是**誰在修**，不是**修好了沒**」 |
| 覆蓋率有系統性偏斜 | `SKILL.md:147`「如果一整晚的發現全部落在這五項之內，那不是驗證了他的直覺，是**你的測試只走了他指的路**」 |
| 大部分 ROLE 發現**未經獨立複驗** | `doc/KNOWN-ISSUES.md` 多條標「live 數字是 ROLE-N 實測（🟢），**本條登記者未複驗（🟠 轉述）**」 |
| 工單與 raw **不在版控** | `scratch/` 被 `.gitignore:46` 擋著 ⇒ ROLE-N 這批的工單、報告、raw log 不隨 repo 散布。**對外講這套方法前要先講這句。** |

## 6c. 🆕 C3–C9　七種實驗方法（七張流程圖）

**規則 6**：每頁只有標題與一張圖。圖上**不標任何 bug**——方法與發現是 deck 的兩段，混在一起
會讓整份報告讀起來像一張 bug 清單（Adam 09-16 裁）。

| 頁 | 圖 | 代表的角色 | 重派時換了什麼（圖下方那條） |
|---|---|---|---|
| C3 | `fig_f1_successor_first` | ROLE-1 | — |
| C4 | `fig_f2_successor_verify` | ROLE-6、ROLE-8 | 6 驗重開循環那三條；8 驗接班人自己那條 |
| C5 | `fig_f3_restart_cycler` | ROLE-2、ROLE-9 | 9 每輪在 4 ↔ 128 之間切換 |
| C6 | `fig_f4_second_operator` | ROLE-4、ROLE-12 | 12 把 A 換成活著的十台交換機拆除 |
| C7 | `fig_f5_traffic_pusher` | ROLE-5、ROLE-10 | 10 在 128 台上跑滿一小時 |
| C8 | `fig_f6_grad_student` | ROLE-3 | — |
| C9 | `fig_f7_manual_follower` | ROLE-11 | — |

🔴 **講者備註必講**：圖上那四個步驟**是 auditor 整理的，不是派工時給的**。
規格明訂派工只寫角色動機、不寫「請測試 X」（`SKILL.md:172`）——講成「我們給了它一份流程」會把這套方法講反。

## 6d. 🆕 D1–D5　角色找到了什麼（五張）

🔴 **這一段開場第一句就要講清楚層級**：這五條**有四條是我們自己的 `ndt` 工具**
（`tools/test_workflow/ndt`，2026-08-21 才有），只有 D2 是繼承來的 baseline。
不講這句，教授會以為角色扮演找到的都是別人系統的缺陷。

| 頁 | 圖 | 層 | 上台那句（進備註，不上投影片） |
|---|---|---|---|
| D1 | `fig_r2_empty_but_confident` | 工具 | 兩個儀器都沒說謊，一個說「我沒查」一個說「乾淨」，而機器上什麼都沒有了 |
| D2 | `fig_r3_two_doors_one_field` | **baseline** | 同一個欄位，走檔案全收、走 API 回 400 |
| D3 | `fig_r4_claim_race_window` | 工具 | 差 50 毫秒就正確了，所以這是一個窗口不是一個壞掉的判斷 |
| D4 | `fig_r12_stolen_marker` | 工具 | 標記記了「有人在拆」，但沒記是誰 |
| D5 | `fig_r10_sampling_instant` | 工具 | 修法是對的，不穩定的是量測窗口本身 |

五張圖左上角都標了**發現者的名字**（不是代號），與 C 段的角色頁對得起來。

## 6e. 🆕 E2–E9　我們修好的 baseline 缺陷（八張）

全部是第一層 baseline（受影響的檔首次提交 2025-12-15）。各圖的數字出處與但書在同名 `.md`。

| 頁 | 圖 | 一句話 |
|---|---|---|
| E2 | `fig_b02_loss_ladder` | 五個負載階梯，丟包從 0 爬到 72.5%，而每一階每個端點都回 success |
| E3 | `fig_b04_poll_resurrects` | 命令關機 3.08 秒後，輪詢把它寫回 up；9 次中 2 次 |
| E4 | `fig_b07_nothing_goes_down` | 一台交換機死了，四個問題只有第一個誠實回答 |
| E5 | `fig_b08_delete_reports_gone` | 刪除帶 buckets 被拒、Ryu 不回錯、kernel 回 200 deleted |
| E6 | `fig_b09_ghost_rule` | 流表 0.257 秒就有那一列，交換機 13.4 秒才真的有 |
| E7 | `fig_b10_accidentally_right` | 288 條邊裡 272 條剛好對，而沒有欄位分得出那 16 條 |
| E8 | `fig_b11_counter_cover` | 修法怎麼做的：不發明計數器，改成公布分母 |
| E9 | `fig_b_topology_doors` | 拓樸檔 11 扇門，以前全開，現在全關 |

🔴 **三張的座標軸是示意不是比例**（E2 的階梯、E3 與 E6 的時間軸）——**產檔時不要在上面加秒數或刻度**。

## 6f. 🆕 F1–F9　`ndt` 九個指令（一頁一個）

🔴 **這一段是「我們建了什麼」，不是「我們修了什麼」**：`ndt` 是我們自己寫的工具（2026-08-21）。

每頁的骨架一樣：指令名（大字等寬）＋一句用途＋怎麼呼叫＋**退出碼各代表什麼**＋一條「最容易踩的邊」。

**退出碼是這一段的主軸，值得單獨講一句**：09-12 之前 `up`／`down`／`clean` 的碼互相重疊，
那一輪讓每個碼只有一個意思、而且三個指令共用同一套：

| 碼 | 意思 |
|---|---|
| 0 | 它做了那件事 |
| 1 | 它量過機器，而讀數是髒的 |
| 3 | **它什麼都沒量到** |
| 5 | **守衛拒絕了，什麼都沒做** |
| 2 | 呼叫方式錯了 |
| 4 | 只有 `check` 有：絆線響了 |

🔑 **3 與 0 都「沒有抱怨」，但它們不是同一個答案。** 這句是整段的收尾。

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
| `figures/fixed-since-903/fig_h1_fixed_since_903` | 2 | 🔴 **09-15 必須重生，現況會把假訊息送上台**：圖裡 `BRANCH_0906/0907/0908` 那條「29 支在分支上」的磚帶**已全數併入 trunk**（09-10），判詞 `FIXED / NOT SHIPPED` 也作廢。重生＝把三個 `BRANCH_*` 併進 trunk 帶（日期 09-10）、磚數 assert 改 96→96（總數不變、歸屬變）、chip 換成 §2 的新口徑 | 同名 `.md` §4 逐磚分類（kernel 46／ndt 18／其他 31／混合 1）；新數字見 `REPORT-PICK-FIXED.md` §0.1 |
| `figures/overnight-0904/fig1…fig6` | 4 | 09-05 16:01；只有 current 側 | 各同名 `.md` |
| `figures/p4-tutorials/fig_t1_requirements_matrix` | 5 | 17:42；`make_tutorial_figs.py` 15 條計數斷言 | 同名 `.md`（208＋16 格） |
| `figures/p4-tutorials/fig_t2_gap_architecture` | 6 | 17:54；兩處刻意不照原規格（中層排序讓 sFlow 箭只跨一格；G2 畫成第一階） | 同名 `.md` |
| `figures/p4-tutorials/fig_t3a_silent_zero`／`fig_t3b_election_wipe` | 7 | 17:54；同高，設計成並排 | 同名 `.md` |
| `figures/p4-tutorials/fig_t4_phases` | 8 | 17:54；GATE 在 470 | 同名 `.md` |

| 🆕 `figures/overnight-hunt/fig_m1_hunt_pipeline` | A | 09-15 起草；`make_method_diagrams.py` 一支產兩張，內建 `assert` 守磚數與版面不出界 | 同名 `.md` 逐格 `檔:行`；數字全來自 09-11 那一夜的 `00-LEDGER.md` |
| 🆕 `figures/overnight-hunt/fig_m2_persona_axis` | B | 09-15 起草；11 個角色的軸逐檔取自 `ROLE-*.md` 第一行；`assert n_roles == 11` | 同名 `.md`；🔴 ROLE-9 的 Time 格是**推論不是原文**，該 `.md` 已標 |
| 🆕 `fig_r2_empty_but_confident`／`fig_r3_two_doors_one_field`／`fig_r4_claim_race_window`／`fig_r12_stolen_marker`／`fig_r10_sampling_instant` | 角色頁 | 09-15 起草；`make_role_diagrams.py` 一支產五張；五張都逐一看過 PNG 確認無疊字、無出血 | 各同名 `.md`。🔴 **三張的座標軸是示意不是比例**（r4 的 ms 軸、r12 的時間軸、r10 的秒刻度），各 `.md` 都寫了但書，**不要在圖上加秒數** |

| 🆕 `fig_f1_successor_first` … `fig_f7_manual_follower`（七張） | 角色頁 | 09-16 起草；`make_role_flows.py` 一支產七張，內建 `assert` 七張點名的角色集合＝11 個角色（無 ROLE-7） | 各同名 `.md`。🔴 **四個步驟是 auditor 整理的，不是派工時給的流程**——規格明訂只給動機不給題目，各 `.md` 都標了 |

| 🆕 `figures/baseline-bugs/fig_b02` … `fig_b10`、`fig_b11`、`fig_b_topology_doors`（八張） | baseline 缺陷頁 | 09-16 起草；`make_baseline_bug_figs.py` 一支產八張，內建色帶重疊 assert 與畫布出界 assert | 各同名 `.md`。🔴 **三張的座標軸非等比例**（b02 的階梯、b04 與 b09 的時間軸），各 `.md` 標了 |
| 🆕 `figures/ndt-commands/fig_c1_up` … `fig_c9_release`（九張） | `ndt` 指令頁 | 09-16 起草；`make_ndt_command_figs.py` 一支產九張，畫布高度由版面算術推導 | 各同名 `.md`。內容逐字讀自 `tools/test_workflow/ndt:8316` 的 `usage` |

🔴 **三個資料夾分屬三段，不可混講**（`REPORT-PICK-FIXED.md` §0.3）：
`baseline-bugs/` ＝ 繼承來的系統（檔案 2025-12-15）；
`ndt-commands/` ＝ **我們自己建的工具**（2026-08-21）；
`overnight-hunt/` ＝ 方法，其中五張缺陷圖**有四張也是我們自己的工具**。

**交給產檔 agent 時三樣一起給，不要只給 PNG**：`.svg`（文字未轉外框、可直接編輯）＋同名 `.md`（出處與但書）＋產生器（版面參數化，改一行重跑）。

不畫「五個 gap 長條圖」：行數是【估】，畫成長條會被讀成量出來的。
🆕 **同理不畫「每個角色找到幾條」的長條圖**：各角色報告的計數口徑不一致（有的記假設證實數、有的記工單數），畫成長條會被讀成可比的。要講數字就用 §6b 的表。

[Co-developed with claude code -- Adam]
