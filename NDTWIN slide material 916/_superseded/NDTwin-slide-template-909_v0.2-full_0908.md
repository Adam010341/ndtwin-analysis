# NDTwin 進度報告簡報 — 2026-09-09 版・資訊模板

**v0.2（2026-09-08 晚，auditor）——909 是一份獨立的 delta deck。**
🔴 **Adam 09-08 裁：903 的內容已經向教授講過，909 不放 903 的任何一頁、也不提它。** 這份 deck 只講 09-03 之後發生的事：
修掉的 bug（§C-909-H）、Q12（§C-909）、09-04 夜巡（§F-909）、P4 tutorials 四頁（§C-909-T）、下一步。頁序見 §C0-909-v2。
規約沿用：**§A（敘事）與 §E（視覺）全文沿用 827 版**
（`../NDTwin slide material 827/NDTwin-slide-template-827.md`）；827 的三節制 **不沿用**——delta deck 撐不起三節。
照 E6 慣例：**本檔是唯一事實來源，Adam 直接編輯**；產檔由 cowork session 跑 JS 產生器（本機無 Node）。動工產檔前先讀最新版。
🔴 **v0.1 產出的 31 頁 `NDTwin_deck_909.pptx`／`.pdf`（09-08 17:56）含 903 的 23 頁 ⇒ 作廢，照 §C0-909-v2 重產。**

三條規則 inline 重申（同 903）：**A2b 每個實測數字旁標 commit**；**兩級證據（親自執行／讀過未執行）不可混寫**；**場地名不上台面**。

---

## B. 9/03 → 9/09 的增量（本檔第一筆：Q12）

| 項 | 內容 | 正本 |
|---|---|---|
| Q12 | `is_up` 一欄兩義 → **裁決拆成 `admin_state`＋`reachable`**（09-03 21:1x，Adam，表單） | `doc/audit/2026-09-03_night-rounds/QUESTIONS-FOR-ADAM.md` §Q12＋補充＋裁決行（trunk `b57736cd`）；修法分支 `fix/is-up-split-admin-state-reachable`（🔴 **09-08 更正：已在 trunk**，見 §C-909 底部） |
| H | **903 → 909 修掉的 bug**：trunk 47 支修法（09-03→09-05）＋09-02 campaign 20 支（切點前一天，🟡 Adam 確認講過沒）＋直接落 trunk 的 5 顆＋分支上 29 支修好未併＋純文件 7 顆；**推到公開 ref 的 0**。09-08 19:xx 一支 opus agent 逐格核過（35 處更正，含三格上台會說錯話的：F-6 一句話寫反、#46 的 18/18 是零鑑別力的臂、Q12 的 1069 是併前的數）。（Adam 09-08 問「清單在哪」——之前不存在於任何檔案，09-08 18:xx 起草） | `FIXED-SINCE-903.md`（本目錄；每列附進 trunk 的 commit／分支 tip＋證據） |

---

## C-909. 新增頁：**Q12 — One flag, two meanings**

建議放在 `3 · ENGINEERING, AND WHAT'S NEXT`、「Found, then fixed」之後；**頁碼由 Adam 定，本檔不寫死**。

**版型**：左欄「問題」（一張兩列表）＋右欄「量到的後果」（三個數字）＋底部「裁決」一行。整頁不放圖（沒有現成圖；要圖的話見 §G-909）。

**標題**：`One flag, two meanings`
**副標（E4d，一個事實 → 這頁講什麼，≤130 字元）**：
`is_up answered "did we switch it off?" and "does it answer?" with one bit — the twin now keeps two.`

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

🟡 讀過未執行（不要寫得像跑過）：修 #46 之前，被 kill 的交換機 **7.5 分鐘**後 twin 仍報 `is_up=True`（09-03 night-rounds 的 persona 輪，見 §Q12 第一段）。#46 修後 poll 那扇門已關：fixed 臂 **6/9** 在 poll 瞬間（t_off+2.56–2.60 s）印出拒絕復活，逐筆對上 harness 記的 poll 落點。

**底部：裁決（09-03，Adam）**
拆成 `admin_state`（on／off，由命令決定、立刻正確）＋ `reachable`（probe 的答案，可以誠實說「快取未過期」）；`is_up` 暫留為 `reachable` 的別名；四個 consumer 分批改。
🔴 **09-08 auditor 更正（v0.1 這一行寫錯了）：修法已經在 trunk 上。** `fix/is-up-split-admin-state-reachable` 09-04 06:51 併進 integrate 線（`95a9f743`，MERGE-LOG 列 38），該線 09-05 15:27 併入 trunk（`cdc8dad9`）；`git merge-base --is-ancestor` 09-08 查證為真；API 文件 `2cd796ff` 記了 `admin_state`／`reachable` 與 `is_up` 的棄用別名；合併後 R0 驗收 ctest 1069/1069。**但沒推到任何公開 ref**（本機 tracking ref：`p4public/main` 停在 09-03 `9e6cc307`、落後 trunk 1689 顆；tracking ref 只證明沒推，不證公開狀態）。⇒ **上台講法：「決定了、修了、在 trunk 上（09-05）；還沒發布，使用者拿不到」**，不講「已修好可以用」。keyLine 改成 `Decided and on trunk since 09-05 -- not yet published.`。🔴 唯一的 breaking change 要講：`/ndt/get_switches_power_state` 的 body 從 `{"ip":"OFF"}` 變 `{"ip":{"admin_state":"off","reachable":false}}`。

**講者備註**：這是設計裁決不是補丁。候選 (b)「一欄加 `source`」只是把歧義搬進欄位；(c)「不動」等於接受 8–13 s 的謊。與 #46（poll 不得覆蓋關機命令）同根：#46 在 twin 內部先把兩個旗子分開，Q12 把分開的結果搬到 API 上；順帶把 #80 的 15 s「不信任窗」從時間改成證據（下一次真的 probe 成功才關窗）。

---

## 🔴 C0-909-v2. 頁序（delta only；Adam 09-08 裁「903 講過的不放」；頁碼 Adam 定）

| # | 頁 | 來源 | 圖 |
|---|---|---|---|
| 1 | Title | — | — |
| 2 | **Found, then fixed — since 09-03**（整頁圖：修法看板） | §C-909-H | `fig_h1_fixed_since_903` |
| 3 | **One flag, two meanings**（Q12；已在 trunk、未發布） | §C-909 | 無（§G-909 時間軸可選） |
| 4 | **What the night round found**（09-04 夜巡六條，一頁六列） | §F-909 | `figures/overnight-0904/` 六張縮圖 |
| 5 | **What the tutorials ask for**（T1） | §C-909-T | `fig_t1_requirements_matrix` |
| 6 | **Where the five gaps live**（T2） | §C-909-T | `fig_t2_gap_architecture` |
| 7 | **What only a foreign P4 program reveals**（T3，兩張並排） | §C-909-T | `fig_t3a`＋`fig_t3b` |
| 8 | **Three phases to a regression gate**（T4） | §C-909-T | `fig_t4_phases` |
| 9 | **Where it stands**（三件待做） | 本節下方 | 無 |

**p.9 的三列**（label→value，不要句子）：`29 branches · not merged`／`0 commits · on the public repo since 09-03`／`phase 1 · ~140 lines · unlocks basic`。
v0.1 的四個產檔裁定（下面 ❌ 那節）裡 **1（夜巡一頁六列）、3（證據 chip）、4（Q12 只講決定）仍有效**——4 的 keyLine 依 §C-909 底部的更正改寫；2 的「§G-909-T 改成已產」已做。

## ❌ C0-909（v0.1，作廢——含 903 的 23 頁）. 實際產出的 31 頁（2026-09-08 17:56 產檔，`NDTwin_deck_909.pptx`／`.pdf`）

> 產生器 `generator/build_deck_909.js`＋`generator/pages_909.js`。
> 🔑 **903 的頁是 `require` 進來的，不是複製的**——deck_style、關卡帶、結果空間三個模組
> 都從 `903/generator/` 取，所以在那邊修一次，909 這邊跟著好；也因此**只有一份 `deck_style`
> 實例**，自動頁碼才不會中途重數。（為此把 903 的兩支單頁產生器改成
> `require.main === module` 才自跑，其餘行為不變。）
>
> **＝ 903 的 23 頁 ＋ §C0-v2 後補的兩頁（p.8 關卡帶、p.9 結果空間）＋ 909 的六頁 ＝ 31 頁。**
>
> | # | 頁 | 來源 |
> |---|---|---|
> | 1–7 | Title … §2 節封面 | 903 |
> | 8–9 | How we measured／Every outcome had a meaning first | 903 §C0-v2 後補 |
> | 10–21 | §2 圖組與普查 | 903 |
> | 22 | ▎§3 節封面、ceiling-not-read-out、The traffic round | 903 |
> | **23** | 🆕 **One flag, two meanings**（Q12） | §C-909 |
> | **24** | 🆕 **What the night round found**（六條） | §F-909 |
> | **25** | 🆕 🖼 **What the tutorials ask for**（T1，用現成熱圖） | §C-909-T |
> | **26** | 🆕 **Where the five gaps live**（T2，架構圖，**本次現畫**） | §C-909-T |
> | **27** | 🆕 **What only a foreign P4 program reveals**（T3，兩張流程圖，**現畫**） | §C-909-T |
> | **28** | 🆕 **Three phases to a regression gate**（T4，階梯＋2×2，**現畫**） | §C-909-T |
> | 29–31 | Worth writing up?／Planned／Where it stands | 903 |
>
> **四個產檔裁定，理由記在這裡：**
>
> 1. 🟠 **§F-909 的夜巡六項做成一頁，不是六張圖頁。**
>    圖已經渲好（`figures/overnight-0904/`，含 `_hires/`），但 §F 自己寫著
>    「**第一批，只有 current behaviour，沒有 after 側**」——一批明講只做了一半的發現，
>    誠實的版型是一頁六列，不是六頁。**after 側補上之後再拆頁**，圖都在，隨時可換。
> 2. 🟠 **T2／T3／T4 用 `figures/p4-tutorials/` 的現成圖，不是手畫的。**
>    §G-909-T 還標「待畫」，但 `make_gap_diagrams.py` 09-08 17:54 已經把四張都渲出來了
>    （`_hires/` 也在）。**§G-909-T 那張狀態表要改成「已產」。**
>    我先手畫過一版當備援，看到現成圖之後撤掉——現成的在三個地方更好：
>    t2 有**三種邊框＝三個階段的圖例**、t3a 有 `no` 分支（不只失敗出口）、
>    t4 把每一支 exercise 名字做成磚而不是一行折行文字。
>    T3 兩張並排一頁（各 ar 0.98，等高 4.36"），下方兩個小標＋頁底註分載 ①②
>    的證據等級——**一張讀碼、一張實測，同頁並列必須看得出來**。
> 3. 🟠 **每頁右上角一個證據判詞 chip**（`MEASURED`／`READ-CODE / NOT RUN`／`MIXED — SEE CHIPS`）。
>    §B-T 的兩級證據紅線在這一組特別容易糊掉（同一頁上既有實跑的 2×2、又有讀碼估的行數），
>    所以**等級由版面承擔，不靠語氣**。T4 頁面上直接寫 **`0 of 13 have run on an NDTwin fabric`**。
> 4. 🟠 **Q12 頁只講「決定了」與量到的數字，不講「已修好」**（§C-909 紅線）。
>    keyLine ＝ `Decided, not shipped: the fix is dispatched and not yet on trunk.`
>    🔴 **產檔前要查 `MERGE-LOG.md` 有沒有 `fix/is-up-split-admin-state-reachable`
>    那一列**——本次沒查到，所以維持「未併」的講法；併了就把這句改掉。
>
> 三處幾何修正（逐頁 60 dpi 看過）：Q12 左欄原用 `S.row` 但標籤欄只有 0.06" ⇒ 改成標籤／值兩行；
> T2 有兩條連線直接穿過目標上方的方框 ⇒ 改走面板之間與左側走線；T4 的 2×2 超出右界 ⇒ 縮欄寬。

## C-909-H. 新增頁：**Found, then fixed — since 09-03**（整頁圖）

**資料正本**：`FIXED-SINCE-903.md`（本目錄）。**圖上只有代號、日期、三個 chip、一個判詞；每一條的一句話與證據都在正本，不上圖。**

**標題**：`Found, then fixed — since 09-03`（33 字元）
**kicker**：`47 on trunk · 29 on branches · 0 published`
**圖 `fig_h1_fixed_since_903`（看板；E4a 口徑：黑框白底、只有一個強調色）**：
- 橫軸＝日期 `09-02 | 09-03 | 09-04 | 09-05 | 09-06 | 09-07 | 09-08`；09-05 15:27（最後一次併 trunk）畫一條 `ACCENT` 豎虛線標 `last merge`。
- 兩個橫帶：上 **`ON TRUNK`**（實線磚）、下 **`ON BRANCHES · NOT MERGED`**（虛線磚）。豎線左邊只有實線磚、右邊只有虛線磚——**這條線就是這頁的論點**。
- 每支修法一塊磚，磚上只寫代號（`#46` `B-5` `Q12` `W8` `E-2` …，照正本 §2／§3「代號」欄；沒代號的寫分支短名）。底色三類：kernel C++＝`ACCENT_BG`、`ndt`／lab 工具＝`PANEL`、proxy／harness／docs＝白；圖例三格。
- 09-02 那一欄的磚全部加 `?` 角標（🟡 切點前一天；Adam 確認口頭講過沒，講過就整欄拿掉）。
- 09-02 欄＝正本 §2.0 的 **20** 塊（16 修法＋4 儀器／接線測試）；§2.5 直接落 trunk 的 5 顆修法 commit **不畫磚**（47 的定義是分支）。
- 純文件 commit **不畫磚**，只在 `ON TRUNK` 帶右端一個小字 `+7 docs`。
- 三個 chip（圖下）：`47 FIXES ON TRUNK` · `29 BRANCHES WAITING` · `0 ON THE PUBLIC REPO`。
**判詞**：**`FIXED / NOT SHIPPED`**
**講者備註**：每支都有變異閘門看過紅（「沒看過紅不算交付」）；標 live 的在 lab 親自重跑過；29 支的併序在正本 §3 末；Q12 是唯一 breaking change；「修在 trunk」對外不等於「使用者拿得到」——公開路徑是 `NDTwin-Kernel-P4-public`，它停在 09-03。
**證據 chip（頁右上）**：`COUNTED FROM GIT · 09-08`。

## G-909-H. 圖面清單

| 圖 | 頁 | 型 | 狀態 |
|---|---|---|---|
| `figures/fixed-since-903/fig_h1_fixed_since_903` | H | 看板（磚 × 日期 × 兩帶） | ✅ **草稿已出**（09-08 18:5x；3732×2100／`_hires/` 6220×3500；`make_fixed_since_903.py` 內建磚數 assert）。auditor 看過：豎線左只實線磚、右只虛線磚；09-02 欄 16 塊全帶 `?`。**三處刻意偏離規格**（記在同名 `.md` §6）：`PANEL` 底色加深到 `#DEE3E7`（原色與白差 3/255，磚上分不出）；日期欄不等寬（09-03 有 30 塊）；chip 寫 29 不是 27（git 實數：未併 `fix/*` 28＋`chore/conventions-0906`）。92 塊逐磚分類表在 `.md` §4（kernel 46／ndt 18／其他 27／混合 1＝E-2）。**定稿由 Adam 交另一位 agent** |

## D-909. 素材出處速查（只列本檔新增）

| 數字 | 出處（正本＋commit） |
|---|---|
| 0.3–1.5 s、8–13 s、18/18 | `doc/audit/2026-09-03_fix-poll-resurrect/FIX-POLL-RESURRECT.md` §3.3.2；raw `audit-raw:doc/audit/2026-09-03_fix-poll-resurrect/raw/02_phase_a_base.log`／`03_phase_a_fixed.log`（`19e3ab88`） |
| 6/9、t_off+2.56–2.60 s | 同上 §3.3.1；`raw/04_fixed_arm_kernel_declines.log` |
| OFF／ON 不一致、A-8 恆空、7.5 min | `QUESTIONS-FOR-ADAM.md` §Q12 第一段；FINDINGS-ALL #33、#34、#46 |
| 裁決與三個選項 | `QUESTIONS-FOR-ADAM.md` §Q12 補充＋裁決行（trunk `b57736cd`） |

## G-909. 圖面建議（尚未畫；要畫再開，照 08-30 乾淨圖裁決：圖上只留標題＋軸＋少數標籤）

一張時間軸就夠：t=0 命令關機（helper 回 `already-stopped`）→ t≈0.3–1.5 s `is_up` 回 1（liveness 快取）→ t≈2.6 s poll 拒絕復活（#46 修後）→ t≈8–13 s `is_up` 回 0（LLDP 過期）。橫軸秒、縱軸 `is_up`；上方畫 `admin_state`（t=0 起恆 off）與 `reachable`（照實）兩條「應有」線。四個時間標籤之外的字全部寫在本節。

---

## F-909. 09-04 夜巡素材（auditor 起草，Adam 定稿）

**第一批，只有 current behaviour，沒有 after 側**——今晚 09-04 的修法輪（`scratch/overnight-2026-09-04/fix/`）還在跑，等它併入、確認輪跑完，after 側由 Adam 或下一個 session 補上這節（見各圖旁 `.md` 的「Regenerate」段，補的時候直接改同一個 `make_overnight_figs.py`）。全部**跑過**（🟢，逐圖旁 `.md` 標credibility），沒有讀 code 推的假說。

路徑：`figures/overnight-0904/`（本檔所在目錄下）。生成腳本：`figures/overnight-0904/make_overnight_figs.py`（一支腳本產六張，matplotlib，同時寫 `.pdf`＋`.png` 300dpi＋`.svg`；`_hires/` 是同目錄 PDF 的 `pdftoppm -r 500`）。binary 全部是 kernel `cca5e3e4ebc42358`（09-04 14:42）、helper `6685d3a9`；trunk 依取數那一輪各自不同，見下表。

| 圖檔 | 一句話 | 現況數字（commit） | raw 出處 |
|---|---|---|---|
| `fig1_declared_vs_real_link_failure` | API 宣告的斷鏈會被 30 s 拓樸輪詢默默蓋回 up；真斷鏈（`tc netem`）60 s 窗口內從不自己回來 | OVS4 declared 自己翻回：25.4／24.4／23.4／22.5／21.5 s（trunk `4088b237`）；P4-4 declared：1.6／10.6／13.6／19.6 s（trunk `f943de8f`，5 次裡 1 次在 20s 窗口內未翻回，右設限未畫）；真斷鏈：≥60 s 才由 `tc qdisc del` 手動復原 | `logs/r2-20-linkfail-probe.log`、`logs/p4-4-14-linkfail.log`、`logs/r2-21-netem-control.log` |
| `fig2_shutdown_southbound_writes` | kernel 印出「All subsystems stopped. Exiting.」之後又花 10.7 s 寫真交換機，過程 0 行 log 提到這件事 | SIGINT→Exiting 0.595 s；Exiting→行程消失 10.743 s（SIGINT→消失合計 11.338 s，trunk `4088b237`）；對照 idle SIGINT 基準 ≈2.4–2.53 s（🟡讀過，另一輪／另一顆 binary，git rev `6283ff5e`，非本輪 `cca5e3e4ebc42358`） | `logs/r2-60-graph-during-shutdown.log`、`logs/r2-61-batch-response.log`、`logs/r2-62-shutdown-analysis.log`；idle 對照：`doc/audit/2026-09-02_live-round/B5-REPORT.md` §6 |
| `fig3_dispatch_counters_vs_switch_truth` | `get_flow_dispatch_status.succeeded` 數的是「POST 沒噴錯」，不是「交換機真的變了」 | 20× 裝同一條 match：succeeded +20／交換機 +1；15× 刪不存在的 match：succeeded +15／交換機 +0；對照組 1× 真的刪除：succeeded +1／交換機真變 1 列（皆 trunk `4088b237`） | `logs/r2-30-b3-same-match.log` |
| `fig4_group_install_delete_readback`（表，非圖——見旁 `.md` 說明為什麼不畫長條） | `install_group_entry` 對兩個保留 group id 都回「200 installed」，但 `groupdesc` 上從來沒出現過；同一支程式的 delete 分支老實回 404 | group id `4294967295`／`4294967293`：install 200「installed」、groupdesc 缺席、delete 404「no_such_group」（trunk `4088b237`）；控制組 id `899`（從未裝過）：modify／delete 皆誠實 404 | `logs/r2-40-b1-group.log`、`logs/r2-41-b1-group-extra.log` |
| `fig5_path_switch_count_static` | `get_path_switch_count` 不讀活拓樸，是靜態模型算出來的常數 | 32/40 與 20/40 交換機間邊判 down 前後，12 條路徑的 `switch_count` 逐格相同（3 或 5，trunk `f943de8f`） | `logs/p4-4-15-pathmetric.log`、`logs/p4-4-pathcount-allon.json`、`logs/p4-4-pathcount-3off.json` |
| `fig6_endpoint_latency_profile` | 同樣是 OpenFlow write，meter install/delete 比 group 慢了約 40 倍 | `install_meter_entry` 1024 ms／`delete_meter_entry` 1029 ms vs `install_group_entry` 20 ms／`modify_group_entry` 24 ms／`delete_group_entry` 34 ms（皆 OVS4，trunk `f943de8f`，client 端量的 HTTP 往返，不是南向可見延遲） | `logs/ovs128-02b-sweep2.log`（P4 對照數字在旁 `.md`，來源 `logs/p4-4-02-sweep.log`） |

**沒有畫進候補清單、但資料已經齊的**（下一批可以先做，不等修法）：#87／W1 的讀回狀態碼＝已經是 fig4；OV-2／OV-3 未知 IP／dpid 的狀態碼（500／200）——見 rounds/03 §3 與 `FINDINGS-CANDIDATES.md`，這批沒做是因為指派單第一批只點名上面六張。`ndt up`／`ndt down` 秒數（OVS 128：28 s／14 s；P4 4：15 s／14 s）與 R1 重開循環、R4 規模那幾張需要的資料在 `rounds/04-R1.md`／`rounds/07-R4.md`（本 session 沒讀，不確定是否已經寫出），留給補 after 側的那個 session 一併處理。

[Co-developed with claude code -- Adam]

---

## B-T. 09-08 增量：P4 tutorials 當需求來源（auditor 起草，Adam 定稿）

| 項 | 內容 | 正本 |
|---|---|---|
| T | **教授的題目「拿 p4lang/tutorials 的 exercise 測 NDTwin」；Adam 09-08 定調目的＝「用真實需求找出 kernel／proxy 缺什麼」** ⇒ 13 支 × 16 維（需求）→ 同 16 維盤點 NDTwin（供給）→ 對表 ⇒ **五個真 gap、兩個只有換程式才暴露的發現、三階段** | `doc/audit/2026-09-04_p4-tutorial-exercise-prep/GAP-ANALYSIS.md`（合成正本，§1 一頁摘要）；`GAP-1-exercise-requirements.md`；`GAP-2-ndtwin-p4-capabilities.md`；`runs/*.md`（四次實跑）。讀的樹＝trunk `1a284f75`、tutorials `c80d83e` |

**證據紀律（這一組的 🟢／🟠 分界）**
- 🟢 **實跑**：09-08 17:24 Adam 以 root 跑 `drive_exercise.py` 四次——`source_routing` solution **5/5**（h2 收 2 包、ttl **{59, 62}**、無 SourceRoute 層）／skeleton **2/2**（h2 收 0 包；s1.log 91 行 `Dropping packet at the end of ingress`）；`basic`（pod-topo）solution **5/5**（pingall 0% 丟、ttl 63）／skeleton **4/4**（pingall 100% 丟）。**跑的是 tutorials 自己的 harness＋`/usr/local/bin/simple_switch_grpc`（`327fa7d1`，不是 bmv2-fast）**——它證明的是 exercise 的預期行為與 driver，**不是** NDTwin 能跑它：**0/13 在 NDTwin fabric 上跑過。** 另兩個 🟢：編譯矩陣（09-04 實編 26 支）、發現②（08-13 三情境實測）。
- 🟠 **讀碼**：五個 gap、發現①、三階段的行數全部是讀碼推導與估計。頁腳寫 `Read at trunk 1a284f75 · exercises run 09-08 on their own harness`，不寫 `Measured at`。

## E-909-T. 視覺優先（Adam 09-08 裁：「教授喜歡看圖片，能視覺化就不用文字」）

這一組**每頁一張圖是主體**；文字只剩 kicker、≤3 列 label→value、一個兩字判詞，解讀全進講者備註。架構圖照 827 §E4a（apps 在最上、新增／指出的元素 `ACCENT`、其餘黑、sFlow 從 proxy 出不從 bmv2 雲出）；流程圖照 §E4b（畫真控制流、失敗出口 `WARNC`＋`WARN_BG`）。五張圖全部產在 `figures/p4-tutorials/`（PDF＋PNG 300 dpi＋SVG＋`_hires/`＋同名 `.md`：資料來源、重生指令、可信度）。**圖上只有元件名、G 編號、數字；不放句子。**

**分工（Adam 09-08）：實際生成圖片由 Adam 交給另一位 agent。** 本模板交的是每張圖的**規格**（層次、元件、箭頭、徽章、色階、資料來源與可信度標記）；`figures/p4-tutorials/` 裡的 matplotlib 版只是**資料對帳與版面草稿**——拿它核數字與結構，不拿它當定稿。

## C-909-T. 新增頁組：**P4 tutorials as requirements**（4 頁）

放 `3 · ENGINEERING, AND WHAT'S NEXT`、Q12 之後、「Planned for the next report」之前；頁碼 Adam 定。標題 ≤45 字元；kicker 是片語。

### T1 — `WHAT THE TUTORIALS ASK FOR`　整頁圖 `fig_t1_requirements_matrix`
**kicker**：`13 exercises · 16 capability dims · read, not run`
**圖**：13 列 exercise × 16 欄維度熱圖（關鍵／用到／沒用到三色階），列序照解鎖階段（basic 最上、flowcache 最下）；底部隔一條 **`NDTwin today`**（做得到／部分／做不到）。圖下三個 chip：`EXACT + LPM ONLY` · `1/13 RUNS UNCHANGED` · `0/13 NEED METERS · DIGEST`。
**判詞**：**`PIPELINE LOAD / NOT FEATURES`**
**講者備註**：8 支要的是「載入任意 P4 程式」這件事，不是新功能；16 維裡 6 維問的是「NDTwin 自己那支 `.p4` 有沒有」，每支 exercise 都自帶 `.p4` ⇒ 能載任意 pipeline 就自動滿足。basic 唯一零改動，但三個 caveat：pod-topo 仍要走拓樸選檔三處推導；NDTwin `ipv4_lpm` 預設 `send_to_cpu()`、basic 是 `drop()` ⇒ 骨架在 NDTwin 上是 punt 不是 drop；載 basic 自己的 pipeline 後 clone 取樣遙測不存在。registers 兩支只在資料面用。

### T2 — `WHERE THE FIVE GAPS LIVE`　整頁架構圖 `fig_t2_gap_architecture`
**kicker**：`proxy + kernel side · sizes are estimates`
**圖規格**（E4a 三層，上→下）：
- 上：**Exercise**＝四個小框 `its .p4`／`topology.json`／`sX-runtime.json`／`mycontroller.py`。
- 中左 **Kernel**：`sFlow parser + FlowKey`、`topology model`、`northbound API`；中右 **Proxy**：`pipeline loader`、`P4Runtime client (table writer · election_id)`、`packet-in decoder → sFlow emitter`。
- 下：雲 **Mininet fabric · bmv2 × N**（今天：同一份 p4info）。
- 箭頭：`.p4 → pipeline loader`；`runtime json / controller → table writer`；`topology.json → topology model → fabric`；`bmv2 clone → packet-in decoder → sFlow → kernel parser`。
- **五個 `ACCENT` 徽章釘在元件上**：`G4` pipeline loader、`G5` table writer、`G3` election_id、`G2` topology model（含 `TCLink`）、`G1` packet-in decoder、`G6` kernel sFlow parser。徽章旁只放行數：`~150`／`~180`／`~15`／`~85`／`~40`／`~30+250`。用三種邊框粗細或底色標階段一／二／三（圖例三格）。
**判詞**：**`READ-CODE / NOT RUN`**
**講者備註**：順序＝解鎖支數 ÷ 工作量：G2（13/13）、G4（12/13）、G5（12/13，含 default_action 無寫入路徑）、G1（12 支的遙測）、G6（6 支轉得動但分身全盲）。**一行都還沒改**，不講「修好了」。其餘 G7／G8／G9 在正本 §3。

### T3 — `WHAT ONLY A FOREIGN P4 PROGRAM REVEALS`　左右兩張流程圖
**kicker**：`same p4info on ten switches, for months`
**左 `fig_t3a_silent_zero`**（E4b）：`bmv2 clone 1/256` → `packet_in header · fields 1..5 by position` → `emitter reads id 5 = sampling_rate` → 判斷框 `== 0 ?` → `WARNC` 終端 **`sample dropped · no log`**；旁邊一條「換程式」分支：欄位重排 ⇒ id 5 不是 sampling_rate。chip **`READ-CODE / NOT RUN`** 🟠。
**右 `fig_t3b_election_wipe`**（序列圖）：`proxy client · election (0,1)` 與 `mycontroller · election (0,1)` 兩條生命線對 `bmv2`：controller 的 stream **虛線＝當重複殺掉**、unary `SetForwardingPipelineConfig` **實線＝接受** → `tables wiped` → 回 **`OK`**（`WARNC`）。chip **`MEASURED / 08-13`** 🟢。
**講者備註**：①三處行號（`sflow_emitter.py:425-429,468-470`、`p4_client.py:217,222`）逐字核過，但沒實際換程式驗證歸零——講機制不講觀察。② bmv2 全程符合規格（第三方 client 真正非 primary 的推送被 `PERMISSION_DENIED`）；tutorials 普遍自帶控制器（p4runtime／flowcache 的教學就是跑 `mycontroller.py`），且它寫死 `50051/dev 0`、NDTwin 是 `30050+dpid`——連位址都對不上。

### T4 — `THREE PHASES TO A REGRESSION GATE`　階梯圖 `fig_t4_phases`＋實跑 2×2
**kicker**：`~675 lines · gate after phase two · 4 runs green`
**圖規格**：左 2/3 階梯——x＝累計行數【估】140／470／675，y＝可跑支數 1／10／13；每階上放該階解鎖的 exercise 名字磚（一：basic；二：qos ecn mri firewall basic_tunnel source_routing calc link_monitor load_balance；三：multicast p4runtime flowcache）；第二階之後一條 `ACCENT` 豎線標 **`GATE`**。右 1/3 一個 2×2 磚：列＝`source_routing`／`basic`，欄＝`solution`／`skeleton`，格內 `5/5`／`2/2`／`5/5`／`4/4`，skeleton 欄用 `PANEL` 底標 **expected fail, observed**——這就是「紅綠都看過」。
**判詞**：**`AFTER PHASE 2 / GATE`**
**講者備註**：三件成立（載任意 pipeline、依 p4info 寫任意表、換程式遙測不歸零）後 `drive_exercise.py` 的 exit code 0／1／2 就是閘門，skeleton／solution 兩向都有預期輸出 ⇒ 看得到紅。第三階段前 ecn／mri 會「綠得很可疑」（qdepth 恆 0），不可進閘門。2×2 那四格是 tutorials 自己的 harness 跑出來的，**不是 NDTwin**。

## D-909-T. 素材出處速查（只列 T 頁組）

| 數字／主張 | 出處 |
|---|---|
| 13×16、exact＋lpm only、0/13 meters／digest、per-switch pipeline、1/13 unchanged | `GAP-1` §2、§4a–4c（`firewall/pod-topo/topology.json:39` 的 `program` 鍵） |
| 25/26 rc=0 🟢 | `COMPILE-MATRIX.txt`（09-04；`p4c-bm2-ss` `226f3f66df515c9e`） |
| NDTwin 做得到 1／部分 9／做不到 6 | `GAP-2` §1 |
| 五個 gap 行號與量級 | `GAP-ANALYSIS` §1／§3；auditor 09-08 抽查：`p4_testbed_topo.py:120-134`、`main.py:185-186`、`p4_client.py:846`（default_action 只有 `:619` 一處讀）、`sflow_emitter.py:425-429,468-470`、`FlowLinkUsageCollector.cpp:1266`（全檔 `ihl` 0 命中） |
| 發現② 🟢 | `doc/2026-08-13_p4runtime-mastership-spec-check.md`；`p4_client.py:60-72`；`p4runtime_mastership_probe.py` |
| 三階段 ~140／~330／~205 | `GAP-ANALYSIS` §6（全部【估】） |
| 四次實跑 🟢 5/5、2/2、5/5、4/4；ttl {59,62}／63；91 行 drop | `runs/2026-09-08T0924*_*.md`（tutorials `c80d83e`；switch `327fa7d1`；logs 在 `~/tutorials/exercises/{source_routing,basic}/logs/`）。⚠️ **91 行不在 `runs/` 報告裡**——來源是 `source_routing/logs/s1.log` 本身（M7 §1.9）；auditor 09-08 18:0x `grep -c` 重查＝**91**（檔 159467 B、mtime 17:24:36；driver 回報 159371 B，差 96 B＝關機時的尾行） |
| 兩顆 bmv2 | `README.md` §3：tutorials `/usr/local/bin`（`327fa7d1`）vs ndt bmv2-fast（`3ff54b5c`），版本字串相同、sha 不同 |

## G-909-T. 圖面清單（`figures/p4-tutorials/`）

| 圖 | 頁 | 型 | 狀態 |
|---|---|---|---|
| `fig_t1_requirements_matrix` | T1 | 熱圖 13×16＋NDTwin today 列 | ✅ **草稿已出**（09-08 17:42；`.png` 2760×1980／`.pdf`／`.svg`／`_hires/` 500 dpi）。圖上只有標題（42 字元）、兩組圖例、軸標籤；列序＝§6 三階段（1／9／3，空白分組）。逐格對帳在 `fig_t1_requirements_matrix.md`（208＋16 格，3 格人工裁決都列了）；`make_tutorial_figs.py` 內建 15 條計數斷言，GAP-1／GAP-2 改了會自己爆。**定稿由 Adam 交另一位 agent 產製，這張只當資料對帳與版面草稿** |
| `fig_t2_gap_architecture` | T2 | 架構圖（E4a），五個 G 徽章 | ✅ **草稿已出**（09-08 17:54；`.png` 3732×2100／`.pdf`／`.svg`／`_hires/` 6220×3500）。auditor 核過：六徽章行數＝GAP-ANALYSIS §1；`election_id` 被 G3 徽章蓋住已修（框 1.74→1.92"）。**兩處刻意不照模板**：中層排序讓 sFlow 箭只跨一個間隙；G2 徽章畫成第一階（實際橫跨一、三），講 ecn／mri 整形時補一句。對帳在 `fig_t2_gap_architecture.md` |
| `fig_t3a_silent_zero`／`fig_t3b_election_wipe` | T3 | 流程圖（E4b）／序列圖 | ✅ **草稿已出**（09-08 17:54；各 1680×1710，同高、設計成同頁並排）。auditor 核過：t3a 的 `id 5`／`== 0 → return None`／`1/256` 對 `sflow_emitter.py:429,468-470`、`ndtwin_switch.p4:52`；t3b 五步對 `p4_client.py:60-72` 與 08-13 三情境表。chip 只放 `READ-CODE`／`MEASURED 08-13`（判詞另放頁面）。對帳在同名 `.md` |
| `fig_t4_phases` | T4 | 階梯＋2×2 實跑磚 | ✅ **草稿已出**（09-08 17:54；3732×1680）。auditor 核過：GATE 線首版畫在 675、已改 470（第二階之後）；2×2 四格＝`runs/` 四份報告的判定；「91 行 drop」刻意不上圖。對帳在 `fig_t4_phases.md` |

不畫「五個 gap 長條圖」：行數是【估】，畫成長條會被讀成量出來的。五張草稿皆為**資料對帳與版面草稿**，定稿由 Adam 交另一位 agent（§E-909-T）。

[Co-developed with claude code -- Adam]
