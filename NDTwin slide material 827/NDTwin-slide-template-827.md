# NDTwin 進度報告簡報 — 2026-08-27 版・資訊模板

**用途**：這份文件是生成 8/27 簡報的唯一資訊來源。
**風格與規則已經完整搬進來，不必重問也不要重新發明**。

**版本**：v2.0（2026-08-26 深夜二版，**33 頁；五條承諾、大規模併發解凍、merge 閘門進 deck**）。
v1.9 = 31 頁、08-25 兩輪與 truncate 進 deck；v1.8 = 三節 25 頁、圖表瘦身；v1.7 = 結構定案、26 頁；v1.6 = 範疇修正（主內容＝figures 的實驗）；
v1.5（2026-08-25，審查 session 代筆新實驗節；本檔頭原停在 v1.3、實含 v1.4 塊，一併補正）。
v1.4 = 08-21 深夜、誤判率補上；v1.3 = 08-21 傍晚、①結案；v1.2 = 同日下午、walk 量到；
v1.1 = 同日上午、§C 首次填入；v1.0 = 2026-08-20 建立、逐頁大綱全空。
上一份是 `~/Desktop/NDTwin Slide material/NDTwin-slide-template.md`（v4.8，8/20 報告用，44 頁）。

> ## 🟢 v1.6 修訂摘要（2026-08-25，緊接 v1.5）—— **範疇修正（Adam 口頭）：主內容＝figures 的量測實驗**
>
> Adam 更正 v1.5 的方向：**「我指的實驗是 figure 裡面的那些實驗，教授沒有想要看我的 debug
> 過程（除非是 baseline 就存在的 bug）」**。照此：
>
> 1. **C4 全部重寫成六張新圖的量測頁**（皆出自 `2026-08-20_sampling-rate-and-cpu` 輪，
>    逐張履歷在該輪 `FIGURES.md`）：sampling-tradeoff／where-the-cpu-goes／
>    matrix-decomposition／iperf-competes／api-concurrency-envelope／ladder-inherited。
> 2. **環從四頁縮成一頁**，資格＝baseline 就存在的 bug（ancestry 已核實）：缺陷→修法→
>    同機開機 A/B。卡點遷移史、靶率非單調、方法論三頁**撤下**，內容降級為該頁備註的口頭項。
> 3. C5（truncate/merge）維持——教授點名。
> 4. `page_ovs-before-after.png`／`page_ovs-vs-bmv2-after.png` 已存在（C1 兩頁的 ⏳ 可解除；
>    數字產檔時從 `2026-08-21_ovs-failover-after-fix/REPORT.md` 現拉，照 A3）。
> 5. v1.5 摘要第 1 條的「主要內容」表述作廢，其餘（C5、C3 備註、checklist 狀態、
>    來源措辭待裁）不變。
>
> ## 🟢 v1.5 修訂摘要（2026-08-25，審查 session 代筆；mainDev 修法 B 落地後校對、Adam 終審）
>
> **Adam 裁定：8/27 報告的主要內容＝08-24〜25 的新實驗。** 本版新增 **§C4**（開機死鎖環：
> 機制→修法→首驗，四頁）與 **§C5**（教授點名的 truncate/merge，一頁），C3 開機頁備註接上
> 「缺陷結案中」的最新狀態。B2 三題的既有頁不動。
>
> 1. 🆕 **C4 四頁**：兩佇列互鎖現行犯（USR2 佇列普查 `e27283a` 首戰＝推論升觀察）、
>    三站點與卡點遷移史、修法 A 同 boot A/B（2/3→0/3、fixa1 失明 **148 s** 自癒，
>    `cce9c5d`/`cb0eedc`）、靶率非單調與「先量靶再測修法」的 gate。全部觀察等級，
>    fine print 含 N=3 等四項 caveat。
> 2. 🆕 **C5 一頁**：truncate 三條路現況（emitter 開著／switch knob 08-20 實測＝無聲全滅／
>    P4 extern 未試）＋merge 建好未接＋Adam 08-25 裁定的實驗計畫（排修法 B 之後）。
> 3. **C3 開機頁**：收斂缺陷從「open 誠實版」升級為「已機制化＋修法首驗通過」、指向 C4；
>    **秒數禁令維持**。
> 4. ⚠️ **8/20 遺留五項 checklist 狀態**（審查 ⑧）：B4 ovs8-64 stale＝v1.4 已清；其餘四項
>    適用於沿用 8/20 素材的頁面、**產檔時執行**：「2,400→readings」用詞、throughput 頁
>    n≈1＋轉抄註記（`fig_throughput` 是唯一手打數字的圖）、fine print 的 epoch 句**保留**、
>    sampling PNG 用 trimmed 後數字重 render（08-20 REPORT 的 🔴 Corrected 塊）。
>    另：`page_where-the-cpu-goes` 若上台，「sFlow 對 bmv2 零成本」類句要並陳
>    **no-clone 控制組已撤回＋冷啟零點**（ab-control 案，兩裁決並陳）。
> 5. 🔴 **一條待 Adam 終審**：C4 對缺陷來源的措辭。缺陷在繼承的控制器碼上（ancestry 已
>    機械核實在案），但 B3.3 把「baseline 缺陷」章節延到 8/27 後——建議措辭
>    「**08-24 報告列 open 的開機不收斂缺陷、本輪結案**」，不做人的歸因；要不要點名
>    baseline 由你裁。
>
> ## 🟢 v1.4 修訂摘要（2026-08-21 深夜）—— **誤判率補上、重算項換數字**
>
> 1. ✅ **v1.3 第 3 點的「誤判率沒量」補上了，idle 情境是零**：三個 cell（Ryu 預設／
>    guard 0.01／guard 0.01＋backoff 10）各 20 分鐘 idle、每窗 ~4.8 萬次探測機會，
>    **零誤刪**、links 32→32，且每個 cell 之後都偵測到真實故障（陽性控制）。
>    投影片可以講 3.9× 了，但措辭是「**idle 誤判率已量＝零；載流情境未量**」——
>    預設值仍不動。`doc/audit/2026-08-21_lldp-guard-false-positives/REPORT.md`（`f176c02`）。
> 2. ⚠️ **主頁帳目表的重算項從 2.17 改成 0.25 s、殘差 1.7 → 3.6 s**。中間發生的事
>    值得口頭一句：`957a646` 的「索引化」實測**比線性掃描慢 1.69×**（token 每查一次
>    付 O(V) 的 `number_of_edges()`），修成 O(1) token（`4810e8f`）才到 0.25 s。
>    三代並陳在 `WALK_SWEEP.md` 尾節；圖已重繪（fine print 註明 epoch 差）。
> 3. ✅ **failover 的 walk 量到了：0.24 s ×3**（誤判率研究的陽性控制順帶印出
>    `_route_reinstall_worker` 那格）——「開機≈failover」從假設變實測，主頁備註已改。
> 4. 🆕 **偵測有第二支修法**：`NDTWIN_RYU_LLDP_BACKOFF=N`（`e44e956`，預設關）——
>    從未回應過 LLDP 的 port（＝host port）每 N 輪才真的探一次，sweep 成本改跟
>    **交換機數**走而不是 host 數。cell C 是它的首次 live 端到端驗證。
> 5. ⚠️ **WALK_SWEEP 的中尺寸掃法已死**：`ndt up ovs <N>` 的缺陷（v1.2 發現的那個）
>    被 ndt session 修掉、現在直接拒絕 N∉{4,128}，原掃法正是靠那個缺陷。縮放故事
>    改由離線四變體賽跑（`walk_variants.py`）承載。
>
> ## 🟢 v1.3 修訂摘要（2026-08-21 傍晚）—— **① 結案**
>
> **那 46.6 秒找到了：是鏈路故障偵測。** ① 的帳現在平了。
>
> 1. 🔴 **偵測 ＝ 44.86 s，佔 51.75 s 的 87%**（實測 n=3，`52cba51`／量於 `07ae07c`）。
>    44.86 ＋ 3.00 去抖 ＋ 2.17 重算 ＝ **50.0 s**，對上獨立量到的 51.75 s。**殘差 1.7 s。**
> 2. 🔑 **機制**：Ryu 對**每一個 port**依序探 LLDP、每次 sleep 0.05 s，要**連續六次沒回應**
>    才判死。所以偵測時間 ∝ **port 數**，而 host port 從不回 LLDP。
>    36 port → 13.1 s；160 port → 44.9 s。**加主機會拖慢自己的偵測。**
>    這也正是 8/20 那張圖上 **3.30× 對 1.21×** 的原因（P4 用固定間隔 beacon）。
> 3. ✅ **修法已量**：`LLDP_SEND_GUARD` 0.05 → 0.01，偵測 **44.9 → 11.5 s（3.9×）**，
>    整個中斷約 **18 s**，落進 P4 的區間。**門檻沒動**——仍是連續六次。
>    🔴 **但誤判率沒量**，B2 ② 的判準碰不到，投影片不可宣稱那條做完。
> 4. **C1 從三頁變四頁**：主頁改寫（帳平了）＋新增「One constant, 3.9× faster detection」。
>    `page_failover-budget.png` 已重繪，兩個 panel = 帳目 ＋ 修法。
>
> ## 🟢 v1.2 修訂摘要（2026-08-21 下午，**實驗室輪次**）
>
> **① 那題最大的一項量到了，v1.1 標成「有爭議」的兩個候選數字都作廢。**
>
> 1. 🔴 **128 台的 all-pairs walk ＝ 2.166 s**（`529e021`，量於 `91229f5`）。
>    四處複述的 ~60 s **差 28×**；13 s 的上界成立但鬆六倍。**C1 主頁的預算表已改寫。**
> 2. 🔴 **重算裡 95% 不是裝規則**：1,280 條 OpenFlow 只花 0.103 s，其餘 2.063 s 是建
>    `all_destination_paths`。兩者縮放不同（線性 vs 超二次），**C1 新增一頁專講這個**。
> 3. 📌 **① 的帳現在是：兩個最被懷疑的機制加起來 <5%，約 46.6 s 沒有歸屬**，
>    剩下的候選是偵測延遲——**正好接到 ② 那題**。
> 4. ⚠️ 量到的是**開機**的 walk；failover 的 walk 計時器已就位，下一輪自己會印。
>
> ## 🟢 v1.1 修訂摘要（2026-08-21 上午）
>
> **§C 從空的變成三頁**，全部來自 08-21 那輪實測，**只涵蓋 B2 的 ① 與 ③**，② 尚未動工。
>
> 1. 🆕 **C1（回答 ①）兩頁**：`The failover budget`（帳目主頁）＋
>    `Ruling out the controller's topology read path`（支撐它的量測）。
>    **控制器拓撲查詢已排除**——4 台與 128 台都低於 1.3 ms，對 51.75 s 差四個數量級。
> 2. 🆕 **C2（回答 ③ 的前置）一頁**：`Which bmv2 produced which number`。
>    兩顆 binary 的 `--version` 逐字相同，改用 sha256／BuildID／size 當識別碼；
>    **過去的 `-O3` 數字現在可以回溯歸屬**。
> 3. 🔴 **B2 ① 補了三處更正**：行號位移（`:473` → `:583`）、
>    **那 60 s 不在 failover 路徑上**（是開機的初始安裝）、
>    **「13 s」是推導的上界而程式註解說 ~60 s，差 4.6×**——它是帳目裡最大的一項，
>    在單獨計時之前投影片不可以給它數字。**已加進 B4 待辦。**
> 4. ✅ **新增 B3.4**：`ndt up ovs4` 曾起出 100% 不轉發的 fabric，**08-21 已修**。
>    留著是為了劃線——**手動設過變數的輪次成立**（8/20 的 15.71 s 不受影響），
>    **08-17～08-21 之間沒人看著的腳本輪次要當可疑**。不上投影片。
> 5. §C 的頁**刻意不編頁碼**——四件結構決定還沒定案，先寫死等於保證要重編（E5 第 26 條）。

**與 8/20 版的關係**：
- **搬過來的**：A 節（規則）、E 節（視覺與版面規格，含 26 條踩過的地雷）、D 節（素材出處）。
  這些是與內容無關的，**照用**。
- **沒搬的**：8/20 的逐頁大綱與當時的實測數字。那些屬於上一場，留在舊檔裡當索引。
- **B 節是新的**：它記的是「8/20 在台上講了什麼、承諾了什麼」，因為那決定 8/27 要交什麼。

> 🔴 **動筆前先讀 B2。** 8/20 的最後一頁 `Planned for the next report` 對教授承諾了三件事，
> 每一件都寫了「怎麼算做完」。**8/27 的簡報骨幹就是那三件事的答案**，其餘都是配菜。

---

## A. 生成簡報前必讀的規則

### A1. 範疇（已與 Adam 確認，不要重問）

1. **基準是 `28b8b13`。** 實驗室前人上傳的完整 OVS/Ryu 系統；Adam 的工作從 2026-07-23 的
   `6f32bca` 開始（`28b8b13` 是它的 direct parent，已核實）。所有 diff、行數、commit 數
   一律用 `28b8b13..HEAD`。
2. **只講 `NDTwin-Kernel` 這個 repo。** 其他 workspace repo（Energy-Saving-App 等）的修復不進簡報。
3. **不提 AI 協作開發流程本身。** mutation testing 只講方法論（「每個測試都親眼看它失敗過一次才算數」），
   不講用什麼工具、怎麼執行。
   ⚠️ **例外**：產品自己的 Intent Translator 在用 OpenAI，那是**產品功能**不是開發流程，可以講。
4. **投影片全英文**，與 Adam 的對話用中文。中文素材（`doc/HANDOFF.md` 等）必須完整翻譯，
   不可留中文殘句。

### A2. 敘事規則

- 🔴 **不講自己造成的 bug。** baseline 既有的缺陷另開一節處理（見 B3.3），
  自己開發過程中引入又修掉的一律不上台。
  8/20 因此刪掉的：`Robustness: defects in my own code` 整頁、Phase 7 的 gRPC subchannel 註記、
  Liveness 的「原本無條件回報 up」、Failover 的「原本會算回死掉的 link」。
- **誠實列出未完成，是加分不是扣分**（教授場合）。但要區分三種：
  **刻意不修**（講理由）／**已記錄未修**（指向 `doc/KNOWN-ISSUES.md`）／**不知道**（就說不知道）。
- **機制沒查明就不要猜。** 可以報告觀察，不要報告解釋。
  8/20 的範例句：「規模放大時兩條控制路徑的退化方式不同」——這是觀察，不是機制。

### A2b. 每個實測數字都要標它量在哪個 commit

**規則：實測數字寫上投影片或寫進本檔時，把當時的 commit 標在旁邊。**
`51.8 s (b6b75fa)`、`16.59 s (213d209)`、`603 tests (2fc430c)`。

量測只對產生它的那版程式成立，而程式會動。沒有 commit，讀的人分不出「現況」和「歷史」，
過期的數字就會被一直當成系統的性質引用。

⚠️ **這條是被咬出來的**：「OVS 斷鏈黑洞 291 秒零自癒」在修好它的 `034da18` 落地之後
**又被引用了四天、散進 11 個檔案**，而**上一份簡報模板就是其中之一**。

📌 **標了 commit，才看得出兩個數字不是矛盾而是不同輪次**：
`50.1 s` 是 n=3 的平均、`51.8 s` 是補到 n=10 之後的——沒有 commit 標記，這看起來像自相矛盾。

### A3. 事實查證規則（前幾輪踩過的坑，必遵守）

1. **所有數字動筆當下重新量**，不要沿用任何文件裡的數字，包括這一份。指令：
   - gtest 數：`grep -rhE '^(TEST|TEST_F|TEST_P)\(' tests --include='*.cpp' | wc -l`
   - Python 測試數：`grep -rh 'def test_' p4_proxy/tests | wc -l`、`... tests/python | wc -l`
   - commit 數：`git log 28b8b13..HEAD --oneline | wc -l`
   - **增刪行數**：`generator/count_lines.py`（見 E4），**不要**用 `git diff --shortstat`
     ——它含註解與空行，會虛胖約 40%。
   - 圖檔尺寸：`identify -format "%f %wx%h\n" figures/*.png`
2. **這個 repo 每天都在動。** 08-11→08-13→08-16→08-19 四次量測，commit 數 202→286→336→377。
   **動筆和產檔之間如果隔了幾小時，就再量一次。**
3. **CHANGELOG 的高層敘述不可信於 bug 來源分類**，只能當素材索引。
   `git show <hash>` 的完整 commit message 才是最好的素材——這個 repo 的 message 寫得極詳細。
4. **不要用 author date 推時間順序**（本 repo 的日期不單調）；要用 DAG
   （`git merge-base --is-ancestor`）。
5. **身份**：`Adam010341`（兩個 email 都是他本人）；`patty`／`joemou`／`JM`／`xxxPatty` 是實驗室前人。
6. **狀態文件會過期**：`doc/HANDOFF.md`、`doc/test_coverage_gaps.md`、CHANGELOG 底部統計。
   引用前對 `git log --since` 檢查有沒有更新的事實。
7. 🔑 **grep 式的「找不到證據」在雙語 repo 上有系統性盲點。** 外部審查曾把 Page 15 的數字標成
   「EVIDENCE NOT FOUND」——**證據在 repo 裡，只是寫成中文而它搜的是英文片語**。
   收到這種回報要自己再搜一次。

---

## B. 8/27 這一輪的起點

### B1. 8/20 交付了什麼（一句話）

P4/bmv2 資料面完整接入 NDTwin，kernel 與七個外圍元件一行都沒改；
五層測試架構讓兩個資料面都有可判定的健康標準；四節 44 頁。

### B2. 🔴 8/20 在台上承諾的三件事 —— **這是 8/27 的骨幹**

8/20 的 p.43 `Planned for the next report` 是對教授的承諾，每一條都寫了判準。
**8/27 要回答的就是這三題**，而且要**用當時寫的判準來回答**，不要換一組比較好看的。

| # | 題目 | 8/20 當時的數字 | 8/20 寫在投影片上的判準 |
|---|---|---|---|
| 1 | **查 OVS 128-host 復原時間花在哪** | OVS **51.75 s** vs P4 **16.59 s**，兩組範圍**零重疊** | 偵測＋重算＋裝規則要**加得起來等於 51.75 s** |
| 2 | **加快 failover 偵測** | beacon 5 s、timeout 15 s（衍生）、三次沒收到才判死 | **看誤判率，不看偵測時間** |
| 3 | **把 fast build 升成預設** | stock **40 Mbps / 3.6k pps** → fast **460–530 Mbps / 50.8k pps** | **L0–L4 整套在 fast build 上通過** |

#### 🆕 B2-bis. 會議上追加的兩條，**與上表同級**（Adam 2026-08-26 裁）

理由與 v1.8 併節同一條：**教授要求的就是承諾**，不因為沒寫在收尾投影片上而降級。
**p.4 一頁列五條，不是三條。**

| # | 題目 | 判準（我們自己設的） | 8/27 的答案 |
|---|---|---|---|
| 4 | **sFlow jitter 重新量測**（baseline 與不同取樣率） | 同一張 fabric、同一條流：**先只換 kernel binary，再只換取樣率** | **ANSWERED**：離散度是**繼承的**（HEAD 1.06× vs 28b8b13 0.98× 於理論地板），而且**1/32 之後買不到精度**。素材＝C4 的 fork-point A/B ＋ C4-bis 第一頁。 |
| 5 | **packet truncate 與 merge** | **任一個要能移動取樣天花板**，否則成本就不是 per byte | **IN PART**：truncate 位元組 −5.6× 而天花板不動 ⇒ per-byte 出局；merge 已接線並過閘門（datagram −6.87×、λ 與 ratio 皆平），**對天花板的作用尚未量測**。素材＝C5。 |

⚠️ **第 5 條的 verdict 是 IN PART 不是 ANSWERED**，顏色用 WARNC。
「做完了」與「答完了」在這一頁必須分得開——merge 過的是**能不能做**的閘門，不是**有沒有用**。

**每一題已經先排除掉的東西（講的時候要帶，否則像亂查）**：

- **① 路徑計算不是原因。** 同一張 fabric，16,256 條路徑在 Ryu 側實際只花約 **13 s**
  （量到 73 s，其中 **60 s 是當時寫死的 `hub.sleep(60)`**），P4 側 **11 s**。
  - 🔴 **2026-08-24 更正**：那個 `hub.sleep` 已經不存在了。等待現在是 `NDTWIN_RYU_SETTLE_S`，
    預設 **40**，而 73 s 這個開機數字連帶作廢——見本檔 C3 的備註與
    `doc/audit/2026-08-22_settle-gate-acceptance/`。這一頁講的是「路徑計算不是原因」，
    那個結論不受影響（13 s vs 11 s 兩邊都沒動），但**不要再引 73 s 或 60 s sleep 當現況**。
  🔑 **判準寫成「帳要平」而不是「找到原因」是刻意的**——前者可證偽，後者不能。
  - 🔴 **2026-08-21 三處更正，動筆前一定要讀**：
    (a) **行號變了**：`hub.sleep(60)` 現在在 `intelligent_router.py:583`（原記 `:473`，
        `5affd93` 之後檔案 1012 → 1122 行）。
    (b) **那 60 s 不在 failover 路徑上**：它在 `load_static_topology` 裡、被 `if is_mininet`
        包著，是**開機的初始安裝**。Failover 走 `_schedule_route_reinstall`（`:252`）→
        `_route_reinstall_worker`（`:269`），去抖是 `reinstall_quiet_period = 3`（`:123`）。
    (c) 🔴 **「13 s」是推導值不是量測值，而且程式自己講的是 ~60 s。**
        13 s ＝ 73 s 開機總時間 − 60 s sleep，中間還含 JSON 解析與建圖，所以它是 walk 的**上界**。
        `intelligent_router.py:113` 與 `:127` 兩處註解、以及 `5affd93` 的 commit message
        都寫「the 128-host walk itself is ~60s」（源頭 `doc/2026-07-29_HANDOFF.md 1g`，
        **早於 128-host 能跑的 `cc249c8`**）。**兩者差 4.6×，而它是 ① 帳目裡最大的一項。**
        ⚠️ **在 walk 被單獨計時之前，不要在投影片上給這一項一個數字。**
- 🆕 **① 又排除掉一項（2026-08-21）：控制器的拓撲查詢不是原因。**
  `/v1.0/topology/{switches,hosts,links}` 在 4 台與 128 台**全部低於 1.3 ms**，
  對 51.75 s 差四個數量級；而且時間比一路落後位元組比（＝序列化次線性），
  形狀與「控制器在更大的圖上做超線性工作」相反。
  完整資料 `doc/audit/2026-08-21_ryu-topology-scaling/`（`2de67b7`，量於 `d9f580b`）。
- 🔴 **① 的重算項已經量到了（2026-08-21），上面 (c) 的兩個數字都作廢。**
  128 台的 walk ＝ **2.166 s**（`529e021`，量於 `91229f5`），不是 13 s 也不是 ~60 s。
  **而且 95% 不是裝規則**：1280 條 OpenFlow 只花 0.103 s，其餘 2.063 s 是建
  `all_destination_paths` 的巢狀迴圈——它是**三次方**的，因為 `find_host_by_ip`
  （`intelligent_router.py:641`）在最內層做線性掃描（A/B 介入證實，換成 dict 差 13.7×）。
  **未修**，只記錄。
  ⚠️ **（08-21 深夜再更新）2.166 也過期了**：`957a646` 的索引實測**更慢**（token 每查
  一次付 O(V)），修成 O(1) token（`4810e8f`）後 live n=3 ＝ **0.25 s**。主頁表已改。
  三代並陳見 `WALK_SWEEP.md` 尾節。
  📌 **① 的帳已經平了（2026-08-21 傍晚；深夜口徑更新）**：**偵測 44.86 s（87%）**＋去抖
  3.00＋重算 0.25（修好後）＝ 48.1 s，對上 51.75 s，殘差 3.6 s（含 epoch 差，見主頁表）。
  **兩個最被懷疑的機制加起來不到 5%，真正的答案是等待。**
  機制與修法見 `DETECTION.md`（`52cba51`）與 C1 的兩頁。
  ✅ failover 的 walk 也量到了：0.24 s ×3（誤判率研究的陽性控制），與開機 walk 同級。
  逐頁內容見 C1，**C1 主頁的數字要照這條改，不要再用 13 s**。
- **② 常數都在 `p4_proxy/proxy_agent/topology_manager.py:137,155,158`**，
  `LINK_BEACON_TIMEOUT_S` 與 `LINK_WATCHDOG_INTERVAL_S` **都是從 `LLDP_BEACON_INTERVAL_S` 衍生的**，
  改一個動三個。實驗設計已經寫在 `doc/KNOWN-ISSUES.md` §D-2：掃 5 / 3 / 2 / 1 秒。
  - 🔴 **投影片上不要承諾偵測時間會降多少。** 每一次誤判都讓 kernel 拆邊、退出 BFS、重算全域路徑，
    `topology_manager.py:147-150` 的註解自己論證過「**會抖動的鏈路報告比慢的更糟**」。
  - ⚠️ **兩個沒放上 8/20 投影片、但被問到要答得出來的**：
    (a) `kLldpFreshSeconds = 12.0` 是 **C++ 常數**
    （`DeviceConfigurationAndPowerManager.hpp:259`），beacon 減半會讓**交換機**存活判斷的
    相對容忍度變兩倍，要維持比例得改 C++ 重編；
    (b) `handleLinkFailure` 對單向故障把**雙向**標 down，修正它的是 `kOnceConverged = 30 s`
    的 topology poll——**所以「收斂」是兩個數字，調 LLDP 只改得動一個。**
  - 🔑 **調參之前要先解決的疑點**（8/20 寫在頁底）：註解說偵測要 **15–20 s**，
    round 4 實測 **10.7–14 s**。**在模型對上之前調參，調完不知道是什麼在動。**
- **③ seam 已經在了**（topo 的 `bmv2_binary_override`，`4b339f2`，`LD_LIBRARY_PATH` 自動攜帶、
  壞 override 大聲拒絕），**預設仍是 stock**。所以這條不是「做不做得到」是「敢不敢換預設」。
  **解鎖兩件現在量不了的事**：TE 的 70% 壅塞門檻（stock 上物理不可觸發）、
  多流併發下的遙測精度（8/20 的 Page 33／35 都明寫這是它們不支持的）。
  判準寫「整套測試通過」是因為**換交換機 binary 就是換掉每一層依賴的時序**。

### B3. 8/20 留下的待辦

1. 🔴 **模組表行數已過期。** 8/20 的 Page 13 用的是舊值，正確值（量於 `cc249c8`）：
   `topology_manager` **1,516**（表上 1,392）、`p4_client` **755**（587）、
   `api_routes` **366**（256）、`main` **345**（305）、`kernel_notifier` **184**（144）；
   `sflow_emitter` 448、`ryu_topology` 338、`ryu_flow_stats` 190 不變。
   ⚠️ 這是**目前檔案大小**不是 diff 行數，兩種口徑不可混用，表下必須註明。
2. **Phase 7 頁還是條列版。** 流程圖已經畫好在
   `NDTwin_phase7_power_flow.pptx`（上一個資料夾），要換直接搬。
3. 🔴 **第 2 節「Baseline defects fixed」仍然延後中。**
   Adam 2026-08-19 裁定延到「下下次」，**也就是 8/27 之後**，理由是還沒跟寫那些程式的學長姐對帳。
   ⚠️ **這個顧慮不是多慮**：該節最強的一條（`034da18`）的歸因在 08-19 被自己的實測推翻——
   讓那行程式碼**構得到**的兩個條件都是我們自己的 `2c81b26` 帶進來的。
   🔑 **如果 8/27 要動這一節，前置作業是對帳，不是寫投影片。**
   折衷方案（8/19 提過、未裁定）：**保留方法論而不做逐條歸因**——講「我們建立了一套能發現
   無聲缺陷的方法，以下是它抓到的**形狀**」，不宣稱「baseline 有這 N 個 bug」。
4. ✅ **`ndt up ovs4` 曾經起出 100% 不轉發的 fabric ——已於 2026-08-21 修好。**
   **這條的作用是劃線：哪些 OVS 4-host 數字能引用。**
   症狀：`ndt up ovs4` 印完 `ok model matches fabric: 4 hosts, 40 edges` / `up. ready` 之後，
   `h1 → 10.0.0.{2,3,4}` **三對全部 100% 遺失**。原因是 `intelligent_router.py:36-38` 的 Ryu
   主機清單來自**它自己的**靜態拓撲檔（預設 128 台），與 fabric 實際大小無關；
   `NDTWIN_RYU_TOPO_FILE` 可覆寫，而當時全 repo **一個 reader、零個自動 setter**，
   唯一的 `export` 是 08-17 報告裡手打的那行。
   - **能不能引用的分界**：✅ **手動設過變數的輪次成立**——8/20 的 OVS/4 **15.71 s** 就是這種，
     不受影響。🔴 **08-17 到 08-21 之間任何「跑腳本、沒人看著」的 OVS 4-host 數字都要當可疑**。
   - **修法（已 commit：`c8d73a5`，`ndt:742`）**：設 `NDTWIN_RYU_TOPO_FILE` = `TOPO_OVS`；
     另加 `verify_dataplane`——**真的送一個封包**（`mnexec -a <host-pid> ping`），OVS 與 P4 兩條
     verify 路徑都接上了。
   - 🔑 **這個缺陷值得記住的是它為什麼躲得掉所有結構性檢查。** 對方跑了 mutation gate，
     把 setter 拿掉之後：`all_destination_paths` 從 902 B 變 **1,110,528 B**、128 個 host、
     `h1 → 10.0.0.2` 100% 遺失、exit code 1——但 **`model matches fabric` 仍然回 ok**。
     **兩邊的拓撲視圖都是對的**，所以只有送封包才抓得到。
     （那個 1,110,528 與我方獨立一輪量到的**逐位元組相同**。）
   - 🔴 **不上投影片**（A2：自己造成的 bug）。
   - 出處：`doc/audit/2026-08-20_lab-bringup-inventory/INVENTORY.md` §8.3；
     複現腳本 `doc/audit/2026-08-21_ryu-topology-scaling/ovs4_connectivity_check.sh`。

### B4. 動筆前一定要重量的

- [ ] `count_lines.py`（四類增刪行數）
- [ ] commit 數、gtest 數、Python 測試數
- [ ] 上一輪所有引用到的實測值，確認 commit 標記還對得上
- [ ] `ls doc/` 與 `identify figures/*.png`（檔名與尺寸都會變）
- [x] 🆕 **`install_all_pair_paths` 已加計時**（`c2afbac`）。每次 walk 印一行
      `install_all_pair_paths done: hosts=N pairs=N rules=N paths=N walk=Xs install=Xs report=Xs`，
      warning 級、開機與 failover 兩條路徑都會印，所以**不必再為這題單獨佔實驗室**——
      任何一輪跑完 grep 一次就有。
      **拆兩相是因為它們縮放方式不同**：`install` 是每 (switch, dst) 一條 OpenFlow 規則
      （128 台 = 1280 條），`report` 是每個**有序 host pair** 一筆（= 16256，「16256 pairs」
      指的是這個）。帳要怪「路徑計算」得先知道怪的是哪一半。
- [x] ✅ **已量到，兩個數字都是錯的**（`529e021`，量於 `91229f5`）：128 台的 walk 是 **2.166 s**。
      **~60 s 那個差 28×**，13 s 的上界成立但鬆了六倍。
      🔴 **而且 95% 不是裝規則**：1280 條 OpenFlow 只花 **0.103 s**，其餘 **2.063 s** 全在建
      `all_destination_paths`（每個有序 pair 一筆，純粹給 kernel 讀）。
      完整五格掃描與機制見 `doc/audit/2026-08-21_ryu-topology-scaling/WALK_SWEEP.md`。
      ⚠️ **（08-21 深夜）此格再被取代兩次**：`957a646` 的索引更慢（1.69×，O(V) token）、
      `4810e8f` 修好後 **0.25 s**（live n=3）。三代並陳在 `WALK_SWEEP.md` 尾節。
      ✅ **failover 的 walk 也量到了**：誤判率研究的陽性控制實測 **0.24 s**
      （`_route_reinstall_worker` 呼叫點，兩個 cell），與開機 walk 同級——收尾量測完成。
- [x] 🆕 **掃 host 數的模型已備妥**（`f70e95a`）：`setting/` 現在有 **4 / 8 / 16 / 32 / 64 / 128
      六個尺寸**（倍增序列，log-log 上才分得出線性與二次）。產生器 `tools/make_topology.py`。
      **不必再接任何線**——`ndt` 的 `topo_for_hosts` 是數檔案裡的 host 數來挑。
      ⚠️ **（08-21 深夜更正）「`ndt up ovs8｜…｜ovs64` 直接可用」已不成立**：當時「可用」
      靠的是 fabric 永遠建 128 台的缺陷（模型≠fabric），該缺陷 16:02 被修掉後
      `ndt` 對 N∉{4,128} **直接拒絕**（`ndt:689`，rc=2）。中尺寸**模型**仍然有效
      （離線 walk 掃描靠它們），中尺寸 **fabric** 目前不存在。
      兩個消費端都驗過：`topo_from_json`（`3b88f5a` 之後 **fabric 是照模型建的**，所以這些檔
      決定的是實際接線不只是 Ryu 的視圖）與真正的 `install_all_pair_paths`
      （六個模型都算出剛好 n(n−1) 條路徑＝完全可繞送）。
      📌 **這張表本身就是 C1 要的圖**：規則 40→1280（線性 **32×**）、
      路徑 12→16256（二次 **1355×**）。
- [ ] 🆕 **`intelligent_router.py` 的行號**：它 08-21 動過兩次（`5affd93` 1012 → 1122 行、
      `c2afbac` 加計時後再長），本檔引用的行號動筆時重 `grep` 一次。

---

## C. 逐頁大綱

### 🔴 C0. **實際產出的 33 頁**（v2.0，2026-08-26 深夜二版，這是現在 `NDTwin_deck_827.pptx` 裡的順序）

> ## 🟢 v2.0 改動（Adam 口頭＋模板 08-26 01:17 修訂）
>
> **1. 🔑「Where we left off」從三條變五條，版型從三欄改五列。**
> Adam：那頁還要包含 **(a) sFlow jitter 重新量測（baseline 與不同取樣率）**、
> **(b) truncate 與 merge**。理由與 v1.8 併節同一條——**教授會議上要求的，也是承諾**，
> 和 20 日寫在收尾投影片上的三條同一種東西。
> - 第 4 條「Re-measure the sFlow jitter — baseline, and across sampling rates」：
>   判準＝**同一張 fabric、同一條流，先只換 kernel binary、再只換取樣率**；
>   verdict **ANSWERED**；今天＝「**繼承的，不是我們加的——而且 1/32 之後買不到精度**」。
>   （素材：`page_ladder-inherited` 的 fork-point A/B ＋ C4-bis 的 `page_ladder-across-rates`。）
> - 第 5 條「Try packet truncation, and batching」：判準＝**任一個要能移動天花板，
>   否則成本就不是 per byte**；verdict **IN PART**（WARNC 色）；
>   今天＝「truncate 有效但買不到東西；merge 已接線並驗證，**對天花板的作用尚未量測**」。
> - 🔴 **三欄放不下五條，縮字級是錯的取捨**——這頁的閱讀順序是「問題→判準→結論」，那是一**列**。
>   五列 pitch 0.90、內容高 0.80。**判準那行釘在 y+0.50 的固定位置**，不跟著標題浮動：
>   五條裡有一條標題會折兩行，讓判準行浮動會為了那一條把整欄弄亂。（E5 新增第 29 條。）
>
> **2. 🔑 「大規模×並發」那頁解凍，並且做進 deck（p.24）。**
> v1.9 照封條跳過它；模板 08-26 01:17 撤回封條——**那個變號的 0.92 是讀錯欄**
> （per-edge min 欄，不是 ratio 欄），四輪全部高報、審查獨立複算吻合。
> 頁上**不給單一倍率的結論**：三類邊「作者值 vs 複算值」並列，右註兩條——
> 「為什麼不引單一倍率」（世代差 14%、同代四位小數重複）與「這頁沒有證明什麼」
> （規模與產流器同時換＝混淆；機制未指認）。
> ⚠️ 頁標題用 `Under concurrency, the twin reads high`（不是模板那句 45 字元以上的原文）。
>
> **3. 🔑 merge 閘門拿到自己的整頁圖（p.30）。** C5b 的 `figures/page_merge-gate.png` 上台，
> 排在 truncate 圖之後、文字頁之前——**兩張圖先講完，文字頁只負責收尾**。
> 文字頁改名 `Truncation and batching, after the experiments`（複數），三條列改成
> ①truncate 有效但買不到 ②**merge 有接、而且真的在 merge** ③**它會不會移動牆是未答的問題**。
> 🔴 **`Effect on the sampling ceiling: NOT MEASURED` 原樣保留在圖上、也寫進頁底 footnote。**
>
> **連帶更新**：
> - Outline 範圍 `4–5 / 7–26 / 28–33`。
> - p.32「下一次」第 ③ 條從「接線 merge」改成「**問 merge 會不會移動天花板**」——
>   接線已經完成，剩下的是 **1/8 那格**（第一個會掉包的率）開關 batching 各跑一次。
> - p.33 settled 加第六條「Under concurrency the twin reads high」（body 降 10.5pt、
>   pitch 0.70，六條才不會撞下一個標題）；open 的 `Scale × concurrency` 從「凍結」
>   改成「方向成立、量級跨世代差 14%」並**取消標記**，改標 `Batching (merge)`——
>   標記的三條必須與 p.32 的三條一致（v1.9 這裡對不上，一併修正）。
>
> **可略順位重編**：① p.5 架構圖　② p.21 iperf　③ p.9 拓撲讀取路徑　④ p.12 OVS vs BMv2
> ⑤ p.29 一行指令　⑥ p.17 誰是瓶頸　⑦ p.25 撤回的結論　⑧ 🆕 p.31 truncate/batching 文字頁
> （**兩張圖已經把故事講完**，時間不夠時留圖砍字）。
> 🔴 **p.24 與 p.30 不在可略清單裡**：前者是 08-25 最重要的量測結果，後者是教授點名那條線的現況。

> **v1.9 加了六頁，全部來自 08-25 之後的新輪次。**
> 節數與節名不變（三節），Outline 的範圍改成 `4–5 / 7–25 / 27–31`。
>
> | 新頁 | 版型 | 來源 |
> |---|---|---|
> | Sampling harder stops buying precision | 🖼 `page_ladder-across-rates.png` | C4-bis |
> | Above 1-in-16, sampling costs the data plane | 🖼 `page_sampling-ceiling.png` | C4-bis |
> | The wall is the proxy — BMv2 is starved, not saturated | 🖼 `page_who-is-the-bottleneck.png` | C4-bis 建議加頁 |
> | The 45-point thread is not sampling cost | 表格＋兩條列＋右註 | C4-bis |
> | A result we pre-registered, and then withdrew | 三條列＋右兩註 | C4-bis「Does only λ decide precision?」 |
> | Truncation works, and buys nothing | 🖼 `page_truncate-bought-nothing.png` | C5 |
>
> **三個裁定，理由記在這裡**：
>
> 1. 🔴 **「128 台並發下孿生全面高報」那一頁沒有做。** 模板自己標了審查凍結——
>    同設定重跑 1.18 → 0.92、方向相反、採集層嫌疑未排除。**照辦，跳過。**
>    它現在只出現在 p.31 的 open 清單裡，寫成「一輪沒有重現，找到成因前凍結」。
> 2. 🟠 **`The staircase dissolves as you sample harder` 與 `Sampling harder stops buying
>    precision` 是同一張圖**（`page_ladder-across-rates.png`），只做一頁。
>    採 C4-bis 的框法，因為它多帶了 1/32 之後脫離地板那件事——**主張更強而且是新的**。
> 3. 🟠 **C5 從「status and plan」改成結果頁。** 模板已註明那個實驗 08-25 20:05 跑完、
>    結論是否定的；再用計畫式寫法上台，講的是一件已經有答案的事。
>    原本的三欄現況表**降級成講稿備援**（照模板指示）。
>
> **連帶更新**：
> - p.30「下一次」第 ③ 條從 truncate 改成 **merge**——truncate 已經答完而且是否定的，
>   merge 是剩下唯一沒試過的候選。
> - p.31「Where it stands」settled 加兩條（取樣天花板、truncate 不是解法），
>   open 把 `Truncate extern / merge` 改成 `Batching (merge)`、
>   `Sub-floor dispersion` 改成 `The ceiling's mechanism`，並新增 `Scale × concurrency`。

> **v1.8 的三項改動（Adam 2026-08-26 口頭）**
>
> 1. 🟠 **舊 §2「What the new measurements say」併進 §1**，整節改名
>    **`Answering the open questions`**。
>    🔑 **理由是 Adam 的**：那六個實驗大部分也是教授要求做的，**所以它們也是承諾**。
>    合併之後這一節的定義變成「**被問到、而現在有答案的事**」——20 日寫下的三條，
>    加上之後會議裡要求的，是同一種東西。
>    ⚠️ 節名先試過 `Pick up where we left off`，Adam 覺得不夠正式，改現在這個。
>    **四節 → 三節，26 → 25 頁**（少一張節封面）。
> 2. 🟠 **全面改用 experiment，不用 measurement**（Adam：比較正式）。
>    受影響的字串已全部換掉，包括 p.22 的右欄註記標題。
> 3. 🟠 **投影片與圖表都再瘦一輪。** 見下方 F2。
>
> **節次標記**：`1 · ANSWERING THE OPEN QUESTIONS`／`2 · ENGINEERING, AND WHAT'S NEXT`。
> §0 的頁不放標記。

> **結構已定案（Adam 2026-08-25 裁）**，四個決定：
> ① **先兌現承諾再開新局**（C1／C2 → C4）；② **四節**；
> ③ **boot deadlock 留在新實驗節當一頁**，不特別標榜它是前人的碼；
> ④ **先做 30 分鐘版**（26 頁），每頁標好可略順位、臨場再砍。
>
> 🔴 **§C 原本那句「刻意不給頁碼」到此為止。** 結構定了，頁碼就編死在下表，
> 動結構的人負責同步它與 Outline 的 `pp.` 範圍（E5 第 26 條）。

| # | 頁 | 版型 | 可略 |
|---|---|---|---|
| 1–3 | Title／Outline／▎§0 Background | — | |
| 4 | Where we left off（**五條承諾**） | 五列：問題＋判準／verdict／今天 | |
| 5 | 🖼 三資料面架構圖 | 整頁圖 | **①** |
| 6 | ▎**§1 Answering the open questions** | 節封面 | |
| 7 | 🖼 The failover budget | 整頁圖 | |
| 8 | Where the recompute time actually goes | 表＋兩列 | |
| 9 | Ruling out the controller's topology read path | 表＋兩列 | **③** |
| 10 | One constant, and what it did not change | 三列＋兩註 | |
| 11 | 🖼 The same link failure, before and after | 整頁圖 | |
| 12 | 🖼 OVS vs BMv2 after the fix | 整頁圖 | **④** |
| 13 | Which bmv2 produced which number | 表＋兩列 | |
| 14 | 🖼 Sampling harder buys precision on a √ law | 整頁圖 | |
| 15 | 🖼 **…and stops buying it at 1-in-32** 🆕 | 整頁圖 | |
| 16 | 🖼 **Above 1-in-16 it costs throughput** 🆕 | 整頁圖 | |
| 17 | 🖼 **The wall is the proxy; BMv2 is starved** 🆕 | 整頁圖 | **⑥** |
| 18 | 🖼 The sampling bill lands on kernel and proxy | 整頁圖 | |
| 19 | 🖼 206 µs of CPU per sample | 整頁圖 | |
| 20 | **The 45-point thread is not sampling cost** 🆕 | 表＋兩列＋註 | |
| 21 | 🖼 The busiest process is the instrument | 整頁圖 | **②** |
| 22 | 🖼 The northbound API serves one request at a time | 整頁圖 | |
| 23 | 🖼 The staircase, and its jitter, predate the fork | 整頁圖 | |
| 24 | **Under concurrency, the twin reads high** 🆕 | 表＋兩列＋兩註 | |
| 25 | **A result we pre-registered, and then withdrew** | 三列＋兩註 | **⑦** |
| 26 | A boot deadlock, and a same-boot A/B | 三列＋表＋兩註 | |
| 27 | ▎**§2 Engineering, and what's next** | 節封面 | |
| 28 | One command brings the lab up and checks it | 表＋三列＋三註 | **⑤** |
| 29 | 🖼 **Truncation works, and buys nothing** | 整頁圖 | |
| 30 | 🖼 **Merge merges — and nothing else moved** 🆕 | 整頁圖 | |
| 31 | **Truncation and batching, after the experiments** | 三列＋三註 | **⑧** |
| 32 | Planned for the next report | 三欄＋判準 | |
| 33 | Where it stands | 左六／右九 | |

**節次標記字串**：`1 · DELIVERING THE THREE PROMISES`／`2 · WHAT THE NEW MEASUREMENTS SAY`／
`3 · ENGINEERING, AND WHAT'S NEXT`。§0 的頁**不放標記**（沿用 8/20 的做法）。

**產生器**：`generator/build_deck_827.js`，`require("./deck_style")`。跑之前把 `FIG` 與 `OUT`
兩個絕對路徑改成本機的。**頁碼自動計數**，不要寫死。

🔑 **§1 內部是結論先行**：先給會平的帳目圖（p.7），再給支撐它的兩頁（p.8、p.9）。
🔑 **p.20 的 jitter A/B 刻意排在 §2 最後一張圖**——那是教授上次親口問的問題，
放在該節收尾處最有回音。

**兩件在生成時做掉的事**：
- 🔴 **p.20 的「~60 s walk」與「13 s 上界」都沒有上台。** 主頁的帳目表用 **0.25 s**
  （`4810e8f`，索引修好後）並在圖的副標裡註明總額量在它之前、省下的秒數落在殘差。
- ✅ **p.12 的兩個 ⏳ 已解除**：after-fix 實測到位（128 台 16.4 s、4 台 15.0 s，n=3，
  `45eccba`），縮放懲罰 **3.30× → 1.10×**，圖已重畫。

---

### 🔴 舊的填寫狀態說明（2026-08-21，已被 C0 取代，保留為歷史）

> **部分填入（2026-08-21）。** 目前只有 B2 ① 與 ③ 有新實測，下面三頁是它們的內容。
> **② 尚未動工**（要起實驗室掃 5/3/2/1 秒）。
> ⚠️ **這兩句已過期**：② 在 08-21 深夜做完（3.9×＋誤判率零），C0 是現行的事實。
>
> 🔴 **刻意不給頁碼。** §C 開頭那四件事（分幾節／三題各佔幾頁／新圖／第 2 節解禁）是 Adam 的決定，
> 還沒定案；先寫死頁碼，等結構一定案就要全部重編（E5 第 26 條踩過）。
> 每頁只標它回答 B2 的哪一題。
>
> 每頁格式：
>
> ```
> **Page N — 頁標題**
> - 版型：（左三條列＋右註記／三欄／表格＋兩條列／整頁圖／流程圖）
> - 要點：① … ② … ③ …
> - 素材：commit hash、檔案路徑、doc/audit/ 下的報告
> - 備註：口頭要補的、會被問的、可略與否
> ```

---

### C1. 回答 B2 ①：OVS 128-host 的復原時間花在哪

**Page ?? — The failover budget: it balances, and detection is 87% of it** 🆕（**這是 ① 的主頁**）
- 副標：`The promise was that detection, recompute and install add up to 51.75 s — they do, and one of the three is all of it`（116 字元）
- 版型：**整頁圖**（`figures/page_failover-budget.png`，2 panel）＋ 表下兩條列。
  產生器 `doc/audit/2026-08-21_ryu-topology-scaling/plot_budget.py`（`ec03d5b`）。
  🔑 **這張是 8/20 那張 `page36_failover-decomposition.png` 的續篇**，兩張要能並排講：
  舊圖答「**什麼讓中斷變長**」（拓撲 3.30×、資料面 3.12×），新圖答「**中斷是由什麼組成的**」。
  51.75 s 是**從舊圖的 `failover_cells()` import 進來的**，不是重打的，所以兩張圖不可能漂移。
- 🔑 **這頁的敘事是「帳目」。** B2 ① 的判準刻意寫成「加得起來等於 51.75 s」而不是「找到原因」，
  因為前者可證偽。**08-21 它平了**，而且平的方式比預期乾淨：四項裡有一項就是全部。

  | term | 128-host cost | 怎麼定出來的 |
  |---|---|---|
  | **detect the failure** | **44.86 s**（87%） | 實測 n=3，`07ae07c`（42.48／45.84／46.25） |
  | debounce before recompute | **3.00 s**（固定） | `reinstall_quiet_period = 3` |
  | recompute（1,280 rules ＋ 16,256 path entries） | **0.25 s** | 實測 n=3，`4810e8f`（O(1) token 修好後；51.75 s 錄的當時是 ~2.2 s） |
  | controller topology query | **< 1.3 ms** | 實測 n=20，`d9f580b` |
  | residual | **3.6 s** | 含 epoch 差：總額量在索引修好之前，省下的 ~1.9 s 落在這裡 |
  | **要解釋的總額** | **51.75 s** | n=10，47.0–56.4，`b6b75fa`＋`9467ea0` |

- 要點：
  ① **OVS 沒有在「慢慢做」任何事——它在等。** 等 LLDP 探測連續六次沒有回應。
  ② **加主機會拖慢自己的故障偵測，而交換機拓撲根本沒動**：Ryu 對每個 port 依序探測、
     每送一次 sleep 0.05 s，所以同一個 port 兩次探測的間隔 ＝ **port 數 × 0.05 s**。
     36 port → 偵測 13.1 s；160 port → **44.9 s**。而 host port 從來不會回 LLDP。
  ③ **這就是 8/20 那張圖上 3.30× 對 1.21× 的原因**：P4 的 proxy 用**固定間隔**發 beacon，
     與 port 數無關。兩張圖在這裡接起來。
- 素材：`doc/audit/2026-08-21_ryu-topology-scaling/DETECTION.md`（`52cba51`，量於 `07ae07c`）＋
  `WALK_SWEEP.md`（`529e021`）＋`REPORT.md`（`2de67b7`）；
  `doc/audit/2026-08-19_failover-provenance/raw_ovs128_n10/`；`ryu/topology/switches.py`。
- 備註：
  - ✅ **08-21 之前這一列寫的是「≤ 13 s，有爭議」，兩個候選數字現在都作廢了。**
    量到的是 **2.166 s**：四處複述的 ~60 s **差 28×**，13 s 的上界成立但鬆了六倍。
    🔑 **這件事本身值得口頭講一句**：那個 ~60 s 是從 `doc/2026-07-29_HANDOFF.md 1g` 散出來的，
    源頭**早於 128-host 能跑的 `cc249c8`**，而它一路擴散到程式註解兩處、測試 docstring、
    以及 `5affd93` 的 commit message。**沒有人量過它。**
    這正是 A2b 那條規則的第二個實例（第一個是 291 秒散進 11 個檔）。
  - ✅ **failover 的 walk 補到了（08-21 深夜）**：誤判率研究的陽性控制斷了真鏈路，
    `_route_reinstall_worker` 印出 **0.24 s**（兩個 cell 各一次：0.242／0.241），
    與開機 walk 的 0.25 s 中位數同級——「同函式同圖、成本相同」的假設實測成立。
    原始檔 `doc/audit/2026-08-21_lldp-guard-false-positives/fp_study.txt`。
  - 🪞 **重算那格的數字換過兩代，本身是一頁好故事（可放附錄或口頭）**：`957a646` 的
    「索引化」實測**比它取代的線性掃描慢 1.69×**（live 3.634 vs 2.166）——cache token
    每次查詢都呼叫 `net.number_of_edges()`，而 networkx 那是對每個節點加總 degree 的
    O(V)。四變體離線賽跑（`walk_variants.txt`）三個尺度全部 1.69×。O(1) token 修好
    （`4810e8f`）→ live n=3 = **0.25 s**。教訓＝「相信某 API 是 O(1)」也要開原始碼驗，
    同一個 helper 兩度成為瓶頸、兩次都看起來顯然沒問題。
  - ⚠️ **`hub.sleep(60)` 不在 failover 路徑上**，它屬於開機的初始安裝。**被問到時不要把 60 s
    算進 failover。**（這也是為什麼「開機 73 s」推不出 failover 的重算成本。）
  - ✅ **兩個沒去瞄準卻自己對上的檢查，值得口頭講**（它們是「這不是湊出來的」的證據）：
    port 數剛好是 **36 和 160**，正是佈局算出來的值；而「偵測＋去抖＋walk」比偵測多出的
    量＝去抖＋當時的 walk——**4-host 剛好 3.00 秒**（walk 是毫秒級），**128-host 兩格都是
    6.4 秒**（raw 6.46/6.43/6.44 與 6.41/6.39/6.40 ＝ 3.00 去抖＋當時慢索引的 ~3.4 s walk）。
    🔑 那個 6.4 其實是**慢索引的獨立 live 目擊**，在任何人知道要找它之前就錄下來了。
    ⚠️ 口頭**不要**講「每格都剛好 3.00」——早期版本這樣寫過，raw 不支持。
  - 🔑 **① 和 ② 在這裡接起來了。** ① 剩下的缺口就是 ② 要調的東西，而且 ② 的槓桿已經量過
    （見下一頁）。**講 ① 的最後一句應該是「所以我們去調了它」，不是「所以下次再說」。**
  - ⚠️ **殘差不要解釋，一律引 3.6 s（walk=0.25 口徑，與主頁表一致）。** 偵測 n=3、總額
    n=10、不同輪次不同 commit，而且總額量在索引修好之前（省下的 ~1.9 s 落在殘差裡，
    fine print 已註明）。**被問就說「在雜訊裡＋epoch 差」**，不要編故事。
    （舊口徑的 1.7 s 只存在於 v1.3 摘要，是歷史紀錄，口頭不要再用。）
  - ⚠️ **這一項量的是「黑洞型」故障**（`netem loss 100%`），不是實體斷線。
    真的把 port 拉下來，交換機會送 `OFPT_PORT_STATUS`，那是立即的。
    **LLDP 逾時是唯一能抓到「線還在、但封包不見」的機制**——而那正好是孿生系統存在的理由。
    被問「為什麼不用 port-status」時這句話要答得出來。

**Page ?? — One constant, 3.9× faster detection** 🆕（**這頁同時開始回答 B2 ②**）
- 副標：`The interval between probes is a constant; the number of misses required is a different one — only the first was changed`（124 字元）
- 版型：**沿用主頁那張圖的下半 panel**（同一個 `page_failover-budget.png`）。
  若要獨立一頁，請從 `plot_budget.py` 另存 panel 2，**不要重打數字**。
- 要點：
  ① `LLDP_SEND_GUARD` 從 Ryu 預設 **0.05 → 0.01**，128 台的偵測 **44.9 s → 11.5 s（3.9×）**，
     整個中斷約 **51.75 s → 18 s** —— 落進 P4（16.59 s）同一個區間。
  ② 🔑 **門檻沒有動。** 一條鏈路仍然要**連續六次**探測沒回應才判死，只是兩次之間的間隔縮短。
     **判定死亡所需的證據完全沒變。**
  ③ 對照組是刻意不選的那個槓桿：`LINK_LLDP_DROP` 從 5 降到 2 也能拿到同樣的數字，
     但那是**降低證據門檻**——`topology_manager.py:147-150` 自己就論證過
     「會抖動的鏈路報告比慢的更糟」。**這個對比就是整頁的訊息。**
- 素材：`doc/audit/2026-08-21_ryu-topology-scaling/DETECTION.md`（`52cba51`）；
  旗標 `NDTWIN_RYU_LLDP_GUARD`，`intelligent_router.py`；`ryu/topology/switches.py`。
- 備註：
  - ✅ **（08-21 深夜取代下面那條紅線）誤判率的 idle 情境量到了，是零**：三個 cell
    （預設／guard 0.01／guard 0.01＋backoff 10）各 20 分鐘、每窗 ~4.8 萬次探測機會，
    零誤刪＋陽性控制全過（`doc/audit/2026-08-21_lldp-guard-false-positives/REPORT.md`）。
    措辭升級為「**idle 誤判率＝零，載流情境未量**」；仍不能講「偵測問題解決了」。
  - ⚠️ **另外兩件沒量的**：控制通道成本（160 port 下 LLDP 從約 20 漲到 100 pps）、
    以及 0.01 是不是對的值（它是為了讓效果明確而選的，不是調出來的）。
  - ✅ **（08-21 深夜）「更好的修法」做掉了**：`NDTWIN_RYU_LLDP_BACKOFF=N`（`e44e956`）——
    從未回應過 LLDP 的 port 每 N 輪才真的探一次（host port 從不回應、故障的 sw-sw port
    **曾經**回過，一個 bit 分得開），故障鏈路維持全速探測、判死門檻不動。
    偵測成本改跟**交換機數**走。已在誤判率研究 cell C live 驗證（零誤判＋真故障照抓）。
  - ⚠️ **預設值都沒有改**（guard 與 backoff 皆是）。旗標存在、override 會在 Ryu log 印一行
    自證生效（這個 repo 出過「setter 沒有 reader」和「reader 沒有 setter」各一次）。

**Page ?? — The fix, recorded: 52 s → 16 s, and what exactly was changed** 🆕（**B2 ② 的收尾頁**）
- 副標：`Three changes, none of which touch the evidence required to declare a link dead`（79 字元）
- 版型：左半 = before/after 對比圖（`figures/page_ovs-before-after.png`，⏳ 08-21 深夜
  量測中，產生器 `doc/audit/2026-08-21_ovs-failover-after-fix/plot_after_fix.py`）；
  右半 = 三條修法列表。
- 要點（**修法的完整記錄**）：
  ① **探測間隔**：`NDTWIN_RYU_LLDP_GUARD` 0.05 → 0.01（`intelligent_router.py`，override
     自證生效）。偵測 44.86 → 11.51 s（n=3）。**判死門檻六次連續未回應，未動。**
  ② **重算**：`find_host_by_ip` 索引化＋O(1) cache token（`957a646` ＋ `4810e8f`）。
     walk 2.17 → **0.25 s**（live n=3）；failover 呼叫點實測 0.24 s ×3。
  ③ **（備援，預設關）** host port 退避：`NDTWIN_RYU_LLDP_BACKOFF`（`e44e956`），
     偵測成本從 port 數改跟交換機數走。
  安全性：三者都不降低判死證據；idle 誤判率實測零（20 min ×3 cell）。
- 素材：`DETECTION.md`、`lldp-guard-false-positives/REPORT.md`、
  `ovs-failover-after-fix/after_fix_outage.txt`（⏳）。
- 備註：⚠️ after 的 outage 用與 before 完全相同的儀器量（measure_failover.sh 的 ping gap），
  不是用各項相加估的——相加估值 ~15 s 已寫成預測，量測結果取代它。

**Page ?? — OVS vs BMv2, after the fix: does the scaling penalty survive?** 🆕
- 副標：`Before the fix, growing 4 → 128 hosts cost OVS 3.30× and P4 1.21× — this is the same plot with the constant changed`（113 字元）
- 版型：整頁圖（`figures/page_ovs-vs-bmv2-after.png`，⏳ 同上量測中）：
  4-host 與 128-host 兩組、每組 OVS-before（淡）／OVS-after／P4 三條。
  產生器同一支 `plot_after_fix.py`，**before 與 P4 的 cells 一律 import
  `failover_cells()`、after 的 outage 用同一個 `outage_from_pings()` 解析，不重打**。
- 要點（預期，數字以量測為準）：
  ① before 的縮放懲罰 3.30× 是 guard×port 數的算術；guard 縮 5× 之後懲罰應大幅消失。
  ② P4 的 beacon 本來就與 port 數無關（1.21×）——**修完的 OVS 是不是也變成這個形狀**，
     就是這頁要回答的問題。
  ③ 4-host 的 after 預測 ~13-14 s（僅比 before 15.70 略降）：**guard 項在小 fabric 本來就小**，
     這個不對稱正是機制的另一個指紋。

**Page ?? — Where the recompute time actually goes** 🆕（**支撐主頁第三列**）
- 副標：`The walk installs 1,280 rules and builds 16,256 path entries — only one of those grows with the square`（101 字元）
- 版型：表格（五列掃描）＋ 表下兩條列。**若要出圖：log-log 雙線圖**，x = hosts、
  y = seconds，兩條線（install / report）。這張圖比表格更有說服力，因為兩條斜率不同**看得出來**。
- 要點：
  ① **裝規則是線性的**：host 數 16×，install 只漲 14.7×（每 (switch, dst) 一條，128 台 = 1,280 條）。
  ② **建路徑表是超二次的**：同樣 16×，report 漲了 688×。它是每個**有序 host pair** 一筆，
     而「16,256 pairs」講的一直是**這個**，不是規則數。
  ③ 所以「路徑計算很慢」這句話要拆開才成立——**慢的是簿記，不是下發**。

  | hosts | rules | install | path entries | report | report 佔比 |
  |---|---|---|---|---|---|
  | 8 | 80 | 0.007 s | 56 | 0.003 s | 30% |
  | 16 | 160 | 0.009 s | 240 | 0.009 s | 50% |
  | 32 | 320 | 0.022 s | 992 | 0.052 s | 70% |
  | 64 | 640 | 0.044 s | 4,032 | 0.286 s | 86% |
  | **128** | **1,280** | **0.103 s** | **16,256** | **2.063 s** | **95%** |

- 素材：`doc/audit/2026-08-21_ryu-topology-scaling/WALK_SWEEP.md`＋`walk_sweep.{sh,txt}`（`529e021`）；
  中間尺寸模型由 `tools/make_topology.py` 生（`f70e95a`）。
- 備註：
  - **方法值得講一句**：五格**共用同一張 fabric**，只換模型。walk 走的圖完全來自拓樸檔，
    只有那 10 台交換機是真的，所以這樣掃**只變一個東西**、噪音底線固定。
  - 🔴 **機制查明了，但要先跟 Adam 確認能不能上台**：report 那一相是**三次方**的，
    因為 `find_host_by_ip`（`intelligent_router.py:641`）在最內層對 `net.nodes` 做線性掃描。
    **用介入證實，不是拿算式硬套**——同一張 fabric 跑真的方法兩次、只換那個 helper，
    斜率從 3.00/2.88/2.75 掉到 2.00/1.86，128 台那格差 **13.7×**。
    ⚠️ **A2 的張力**：`intelligent_router.py` 是實驗室既有的 Ryu 控制程式，所以這屬於
    **baseline 缺陷**，而 B3.3 把那一節延到 8/27 之後。
    🔑 **建議的折衷**：這頁只講**量到的成本分佈**（那是系統的性質、是 ① 的答案），
    機制留口頭答問。**不要**在投影片上寫成「baseline 有一個三次方 bug」。
  - **未修**，`install_all_pair_paths` 在活的 OVS 控制路徑上，這輪的任務是量它不是改它。

**Page ?? — Ruling out the controller's topology read path** 🆕
- 副標：`The kernel re-reads three Ryu topology endpoints on every change — so we timed all three at both fabric sizes`（110 字元）
- 版型：表格 ＋ 右側註記
- 要點：
  ① 四個端點在兩個規模下**全部低於 1.3 ms**；
  ② **形狀也不對**——時間比一路落後位元組比（`/hosts` 送 32× 的資料只花 3.5× 的時間），
     那是序列化**次線性**，正好與「控制器在更大的圖上做超線性工作」相反；
  ③ 所以這條路徑**排除**，不要再回頭推導它。

  | endpoint | 4 host | 128 host | time ratio | byte ratio |
  |---|---|---|---|---|
  | `/v1.0/topology/switches` | 0.461 ms / 4,158 B | 1.127 ms / 17,154 B | 2.44× | 4.13× |
  | `/v1.0/topology/hosts` | 0.346 ms / 812 B | 1.225 ms / 26,345 B | 3.54× | 32.44× |
  | `/v1.0/topology/links` | 0.449 ms / 7,176 B | 0.797 ms / 7,176 B | 1.78× | 1.00× |

- 素材：`doc/audit/2026-08-21_ryu-topology-scaling/`（`2de67b7`，量於 `d9f580b`）；
  探針 `ryu_topo_latency.py`、raw `ryu_topo_{4,128}host.json`。
- 備註：
  - 方法上值得講的兩點：**n=20 取中位數、前面丟 3 次熱身**；**每一格之間 `ndt down`**，
    三次 `ndt up` 各自印出不同的 kernel pid（239930 / 261900 / 264715），所以沒有一格繼承前一格的 kernel。
  - ⚠️ **`all_destination_paths` 那一列不要放上投影片。** 它兩格回**逐位元組相同**的
    1,110,528 B，因為 4-host 那格的路徑表其實是 128 台的（見 B3.4）。
    探針有斷言 host 數且**誠實通過**了，但斷言查的是 `/v1.0/topology/hosts`，而
    `all_destination_paths` 不從那裡衍生。
    🔑 **可以講的一般性教訓（如果有版面）：斷言要蓋住「被改變的那個量」，不是它旁邊那個。**

---

### C2. 回答 B2 ③ 的前置：fast build 升成預設

**Page ?? — Which bmv2 produced which number** 🆕
- 副標：`Both builds answer --version with the same string — so this page identifies them by what actually differs`（105 字元）
- 版型：表格 ＋ 兩條列
- 🔑 **這頁在 ③ 裡的位置：它不是「換預設」本身，是換之前必須先有的東西。**
  兩顆 binary 的 `--version` 逐字相同（`1.15.3-f0b7d201`），差**約一個數量級**的效能。
  沒有識別碼就無法宣稱「這個數字量在 fast 上」。

  | | stock | fast |
  |---|---|---|
  | path | `/usr/local/bin/` | `/usr/local/bmv2-fast/bin/` |
  | `--version` | `1.15.3-f0b7d201` | `1.15.3-f0b7d201` ← **相同，不可當 ID** |
  | sha256 | `327fa7d1…` | `3ff54b5c…` |
  | size | 9,576,568 B | 92,147,960 B |
  | 最佳化 | `-O0 -g` | `-O3 -march=native` |
  | logging / elogger | **on** | **off** |
  | 實測吞吐 | ~40 Mbps / 3.6k pps | 460–530 Mbps / 50.8k pps |

- 要點：
  ① 識別碼用 **sha256 / BuildID / size**，不用 `--version`；
  ② **過去的 `-O3` 數字現在可以回溯歸屬**——source SHA 就印在 binary 自己的 `--version` 裡，
     而 `f0b7d201` 那棵樹還在磁碟上；
  ③ 選 binary 只有**一個 seam**（`bmv2_binary_override` → `resolve_bmv2_launcher()`），
     兩份拓撲共用，沒有第二條路要同步。
- 素材：`doc/audit/bmv2-binary-provenance.md`（`2c8486a`，量於 `d9f580b`）；
  吞吐數字出自 `doc/2026-08-15_bmv2-performance-report.md`。
- 備註：
  - 🔴 **這頁更正了一份自己的文件。** `METHOD_jitter-and-load.md:205-217` 判定 `-O3` 那格
    「永遠釘不住」，只有前兩個子句成立；**第三個不成立**。那份報告引用的 binary
    （92,147,960 B、2026-08-15 15:11）今天還在磁碟上，位元組數與時間戳都對得上。
  - ⚠️ **不要在投影片上講 override 的靜默回退。** 那是我方工具的缺陷（A2：不講自己造成的 bug）。
    但**被問到要答得出來**：override 檔不見或整份被註解掉時，下一輪會**安靜地**跑 stock，
    而回來的數字大約低 10×，讀起來像「fabric 很忙」而不是「binary 拿錯了」。
  - 判準是「L0–L4 整套在 fast build 上通過」，**這頁不宣稱那件事已完成**——它只交出前置條件。

---

### C3. 不屬於 B2 三題：實驗室開機變成一行指令

> **這節不回答 B2 的任何一題**，是 8/20 之後獨立做完的基礎工程。Adam 2026-08-21 指定加入，
> **頁碼待排**（他的原話：「不知道要放第幾頁就接在別人後面，後續會再安排順序」）。
> 給教授的定位是**簡短介紹**，一頁；真要展開有第二頁的材料（見本節末）。

**Page ?? — One command brings the lab up and checks it** 🆕（43 字元，量過；45 會卡在 E5 第 4 條的邊界）
- 副標：`Two data planes start in opposite orders and neither fails loudly when reversed — so this page shows what bring-up now enforces`（127 字元）
- 版型：表格 ＋ 三條列
- 🔑 **這頁的敘事不是「工具比較好用」，是「量測的前提現在被強制執行」。**
  教授關心的是可重現性：**在此之前，每一個數字都附帶一個沒有被檢查的假設——
  測試床真的是操作者以為的那個樣子。**

  兩個平面的啟動順序是**相反的**，而弄反不會大聲失敗：

  | | 誰先起 | 為什麼 | 弄反的後果 |
  |---|---|---|---|
  | **OVS** | 控制平面（Ryu） | switch 主動撥給 controller | switch 撥向死埠，**任何 log 都不提 port**，只看到拓撲永不收斂 |
  | **P4** | 資料平面（bmv2） | proxy 是 gRPC **client** | proxy 第一個 RPC 就 ECONNREFUSED，uvicorn 在開 :8081 前退出 |

- 要點：
  ① **一個數字決定全部。** fabric 的規模與 kernel 的模型都由 host 數推導，所以
     「128 台的 fabric 旁邊載了一份 4 台的模型」**無法因為忘記設環境變數而發生**——
     這個錯誤真的發生過，結果是每一對 host 之間 100% 掉包，
     而**三個獨立的視圖同時顯示正確**。
  ② **開機以送出一個真封包作結**，不是以讀一個狀態頁作結（`mnexec -a <host-pid> ping`）。
     拓撲畫面十台全綠而網路完全不通，發生過兩次。
  ③ **收機要證明它殺掉的是什麼**：比對行程啟動時間與 pidfile 寫入時間——
     晚於 pidfile 才啟動的 PID，不可能是那個 pidfile 指名的行程。
     名字和 argv 都不能用（每個服務都是 wrapper `exec` 過去的）。

- 實測（`52cba51`）：`ndt up p4 128` **33.6 s**、`ndt down` **13.3 s**、`ndt status` **0.3–0.7 s**。
  🔴 **OVS 的開機秒數暫時不要上投影片**，理由見備註。

- 素材：`tools/test_workflow/ndt`（`c8d73a5`…`957a646`）；
  開機手冊 `doc/2026-08-17_testing-manual.md` §2（`b4d4541`）；
  實跑逐字輸出與腳本 `doc/audit/2026-08-21_bringup-manual-verification/`。

- 備註：
  - 🔴 **OVS 的 24.1 s 不要用。** 那個數字量在一個**孿生模型看不見自己 host** 的組態上
    （settle=10：Ryu 0/128 學到、kernel 圖 256 條邊 down，而資料平面完全正常）。
  - ✅ **2026-08-24 已重量，可以填**：預設 `NDTWIN_RYU_SETTLE_S=40`，
    `ndt up ovs` **52 s**（n=3；51/52/52）。比 settle=60 時代的 73 s 更快而且孿生是對的。
    P4 的 33.6 s 不受影響。
  - ⚠️ **這個 52 s 要帶一個 caveat，別裸引**：它**只量到成功的開機**。同一預設下
    2026-08-24 已知結果 5 次開機失敗 3 次（`kernel: 10 switches, 0 up, 0 enabled`、
    不轉發，與 settle 值無關的上游缺陷，**尚未解決**）。也就是說 52 s 是
    「開起來的時候要多久」，不是「開一次要多久」。缺陷細節見
    `doc/audit/2026-08-24_path-switch-count-404/REPORT.md`。
  - 🔑 **裁決規則（review session 2026-08-24 定，數字出來前先定的）**：正在跑 defaults ×10
    開機成功率，結果決定這頁怎麼處理，**不要臨場判斷**：
    - **失敗 ≤1/10**（與 bisect 時代一致）→ 52 s 上台，加一行 caveat。
    - **接近 3/5** → **這頁不放任何秒數**，改放「收斂缺陷 open」的誠實版。
      理由：一個**一半時間開不起來**的系統，引用它「開機多快」本身就失去意義，
      caveat 救不回來——「以成功開機計」是地板不是天花板，它只在率量出來之前可用。
    - 率還沒量到之前，這頁維持「不放數字」。
  - ✅ **2026-08-24 已量，規則已觸發：10 次 defaults 開機 6 次不收斂**
    （`doc/audit/2026-08-24_full-stack-run/boot_rate.txt`）。**結果**二值分明沒有中間態：
    收斂或不收斂。成功一律 58 s；失敗的 413–415 s **是 `ndt` 自己放棄等待的常數、不是缺陷的
    簽名**（別把它當數據引用），失敗態在那之後還持續著。
    **→ 走「接近 3/5」臂：這頁不放任何秒數。**
    52 s 與 24.1 s 都不要用。改放「收斂缺陷 open」的誠實版。
  - 🔬 機制已定位（非 switch 沒連上）：失敗 boot 的 `EventOFPStateChange` 是 10/10、
    waiter 也看到 10 online 照裝路由，但 `/v1.0/topology/links` 整場空
    ⇒ **LLDP link discovery 零產出**，walk 對無邊圖無事可裝。
    辨識法：settle 迴歸＝288 邊 **256** down（只有 host 邊）；本缺陷＝288 邊 **288** down。
  - 🟢 **（08-25 續）那個缺陷已完整機制化、修法首驗通過**：環＝兩個 event queue 互鎖、
    殺傷＝餓死 kernel 的拓撲輪詢；修法 A 同 boot 對照 2/3→0/3。**完整故事在 C4**，
    本頁維持不放秒數、備註改指向 C4（「收斂缺陷 open」的誠實版由 C4 接手結案）。
  - ⚠️ **不要在投影片上講那個 settle 迴歸本身**——A2：自己造成又修掉的 bug 不上台。
    但**被問到「你怎麼知道這套開機是對的」要答得出來**：手冊寫完之後從乾淨環境實跑一輪，
    而那一輪**推翻了手冊自己的三條**（驗收關卡、veth 計數、秒數），三條都當場改正。
    這是可以講的——它示範的是流程有效，不是缺陷。
  - **誠實的未完成**（A2 說這是加分）：
    ① `claim` 是**約定不是鎖**——它擋工具自己的動詞，擋不住裸指令；
    ② `ndt clean` **不斷言** veth / OVS bridge / netns / `tc netem`，
       正常路徑上 `mn -c` 會清掉，但沒有被檢查。
  - **可略**：這頁與 B2 三題無關，時間不夠時整頁抽掉不影響主線敘事。

**第二頁的材料（如果教授追問，或之後決定展開成兩頁）**：`ndt status` 一頁把
「決定每一個數字的組態」列在同一個畫面上——host 數、拓撲模型檔、**哪一顆 bmv2 binary**、
pipeline 編進去的取樣率，外加誰正在用實驗室。這對應 C2 那頁的識別問題：
C2 說「必須能指認 binary」，`ndt status` 是**日常操作裡指認它的地方**。

---

### C4. 🆕 新實驗（六張量測圖）：取樣的成本、精度與歸屬——08-20 輪

> **報告主內容（Adam 08-25 口頭：主內容＝figures 裡的實驗）。** 六張圖全部出自
> `doc/audit/2026-08-20_sampling-rate-and-cpu/`（REPORT.md＋FIGURES.md＋`plot_figures.py`；
> 圖從已 commit 的 raw 重算、與報告不可能漂移——同 08-19 慣例）。頁碼不編（§C 規則）。
> ⚠️ 全節統一口徑：**CPU 一律用 trimmed 值**（每 trace 頭 6 s 丟棄；REPORT §1 未 trim、
> FIGURES.md 兩式並列復算，圖用 trimmed——fine print 註明）。數字帶 commit（A2b）。

**Page ?? — What sampling harder buys**（25 字元）
- 副標：`Three sampling rates against one fixed 200 Mbit/s flow — quantum, dispersion and bias, measured against what √λ predicts`（121 字元）
- 版型：整頁圖 `figures/page_sampling-tradeoff.png`。
- 要點：
  ① 4× 取樣率 → 量化階 **4.00× 變細**、離散度 **1.83× 收緊**（√4 預測 2.00×）；
  ② **每個率都無偏**（twin/truth 全在 ±0.1%）；Fano ≈ 1＝計數就是 Poisson、上面沒有別的雜訊；
  ③ 代價見下一頁——精度是拿 kernel／proxy 的 CPU 換的，不是免費的。
- 素材：REPORT §1（用 FIGURES.md 的 trimmed 復算表）；raw（`d50f8a1`）。
- 備註：quantum ＝ `N × 1442 B × 8` 逐格吻合（1442 = 1400 payload ＋ 42 header）——
  口頭可講「連量化階的位元組數都對得上」。

**Page ?? — At 128 hosts under real concurrency, the twin over-reports every edge class** 🆕🔑
（頁標題超過 45 字元，產檔時縮成 `The twin over-reports at scale`）

> ✅ **2026-08-26 解凍（前一版封條的前提已撤回）。方向可以講，倍率要帶但書。**
>
> 昨晚一度以為「同設定重跑變號成低報 0.92」——**那是讀錯欄位**：0.924/0.874/0.974 是
> `analyze.py` 的 **per-edge min** 欄，不是 `ratio` 欄（mainDev 自己抓到並更正）。
> **審查員用自己的積分器與 veth 對映獨立重算四輪，全部吻合 2% 內 ⇒ 更正 CONFIRMED。**
> **四輪全部是高報，沒有變號。**
>
> ⚠️ **但仍有一個真實的未解問題，倍率不可講死**：同樣 16 流、同組態，
> **15:53 那代 fabric 是 1.19，23:2x 那代是 1.03–1.05**——差約 14%，機制未指認。
> 候選：機器負載（15:53 有別的 session 在跑實驗、23:2x 安靜）而**迴圈週期 T 是隨負載變大的**；
> 儀器 binary；fabric 世代差異。**mainDev 的臂 I 證明同代之內高度可重複（四位小數逐字相同）
> ⇒ 那 14% 不是 run-to-run 雜訊。**
>
> ⇒ **可以講**：三類邊系統性高報、兩平面都高報、成因在共用記帳碼（那條靠的是預註冊的
> 「差不到 2×」粗判準，14% 的世代差吃不掉它）、OVS 64 流三邊類平坦到 0.2%。
> ⇒ **要帶但書**：任何**單一倍率**（1.19 / 1.23 / 1.39…）都必須說明是哪一輪、哪一代 fabric。
> ⇒ **不得**把跨世代的兩個數字相除當成效應量。
- 副標：`Every previous 128-host measurement carried one flow and loaded three of ten switches — this one loads all ten, and the model disagrees with the wire`（→ 產檔前縮到 ≤130）
- 版型：表格＋右側註記（圖待補；`analyze.py` 已可出數）。
- 🔑 **這是 08-25 最重要的量測結果，也是「大規模×並發」這格從未被填過的直接後果。**
- 要點：
  ① P4、128 host、**64 條並發流、十台交換機全部有負載**（歷來 128 台量測都只有 3/10）：
     三類邊**全部系統性高報**——host→switch **1.23**、switch→host **1.34**、
     switch→switch **1.26**（作者值）；**審查用不同視窗＋自寫對映＋不篩邊獨立複算
     ＝1.26／1.41／1.33，方向、量級、三類順序全部一致**。
  ② **遠超聚合取樣誤差地板**（~1.7–2.9%）⇒ 不是雜訊。
  ③ 對照 08-16 的 4 台（1.03）：**形狀變了，但不得宣稱「規模是原因」**——產流器同時換了
     （NTG 混合 → iperf3 UDP）。分離需要一輪 **4 台 × iperf3** 對照，**未做**。
- fine print：邊集合有兩種定義（篩「有負載」62/62/8 vs 全部 122/128/32），兩組比值都要標；
  機制**未指認**；本輪 OVS 側未做、條件 B 未分析。
- 素材：`doc/audit/2026-08-25_large-scale-concurrent/`（`dee0512`，PREREG 先寫、raw 在
  `audit-raw` orphan branch）；審查複算件在同輪目錄。
- 備註（口頭）：順帶量到**實驗室的硬限制是並發數不是頻寬**——14 核只能可靠產生
  40 Mb/s÷64 流 或 100 Mb/s÷16 流（全機 CPU 從未超過 67%，**機制未指認、不得寫成
  「bmv2 撐不住」**）。另：**F-9 沒有現形**（62 條 host 邊全在 3 Mb/s 門檻以下卻無一讀 0）
  ⇒ 我們自己文件對 F-9 的描述範圍被這輪推翻，KNOWN-ISSUES 要改。

**Page ?? — The staircase dissolves as you sample harder** 🆕（47 字元 → 用 `The staircase dissolves as you sample`，36）
- 副標：`Two existing ladders vary the data plane and the code generation — this one varies the sampling rate, which is the axis that moves the step`（135 字元 → 產檔前縮到 ≤130）
- 版型：整頁圖 `figures/page_ladder-across-rates.png`（3040×1270、ar 2.39，**刻意避開 E5 #22 的寬圖模式**）。
- 🔑 **這頁補的是既有兩張 ladder 都沒變的那個軸**：deck 的 `page39_quantisation-ladder`
  變資料面（OVS vs P4，皆 1/256）、`page_ladder-inherited` 變程式世代（三代，皆 1/256）；
  取樣率掃過但只畫成 log-log 摘要（`page_sampling-tradeoff`）。
- 要點：
  ① 五個取樣率、**同一張 fabric、同一條 200 Mbit/s 流、同一條邊**，只有 pipeline 的
     `SAMPLE_RATE` 不同；量子 **11.81 → 0.74 Mbit/s（16×）**，可達值 23 → 72 個。
  ② **每一格都貼在取樣地板上**（1.01–1.11×）——沒有人加雜訊、也沒有人在平滑。
  ③ ground truth 五格皆 **205.2–205.4 Mbit/s**＝同一條流的內部控制組，證明差異只來自取樣。
- 素材：`doc/audit/2026-08-20_sampling-rate-and-cpu/plot_ladder_rates.py`（**新增**，
  載入器／配色／量子算術全部 import 自 `plot_figures.py`，不重打數字）；raw＝matrix 的
  `m{64,128,256,512,1024}_poll_twin.jsonl.gz`（`matrix.sh`，已 commit）。**無新量測**。
- 備註：統計取全 240 s、**畫面只畫 60 s**（240 s×1 Hz 會把離散階糊成雜訊帶，那就變成
  tradeoff 那頁已經講過的事）；淡格線只在數得清的那一格畫（FIGURES.md item 14 記過
  「λ 大時格線＝灰霧」）。⚠️ 1/256 這格的 spread 12.1% 與 tradeoff 圖的 11.2% 是**不同輪次**
  （矩陣 cell vs 單因子 sweep），並非矛盾，並列時要註明。

**Page ?? — Where the CPU actually goes**（27 字元）
- 副標：`Every component is its own process, so /proc answers per component — sampling cost lands on the kernel and proxy, not the switches`（129 字元）
- 版型：整頁圖 `figures/page_where-the-cpu-goes.png`。
- 要點：
  ① 1/64 取樣的成本＝**kernel 57＋proxy 20 個百分點（單核）**；**bmv2 跨 1/256→1/64 平坦**
     （149–158%，率間內部對照）——**取樣成本不落在資料面**；
  ② 冷啟零點 n=3：poll-off **2.89±0.03**；polling 成本 **7.53 點**，落在矩陣自己的
     6.3–8.0 區間（兩臂互證）；
  ③ 機器 14 核、idle 全機 4.0%（口頭一句：舊的 idle 100% spin 已是歷史）。
- 素材：REPORT §2／§4（trimmed）＋FIGURES.md item 1／9；`cpu_probe.py`（讀 /proc 差分、
  用 cmdline 認 pid——comm 15 字元截斷的坑已處理）。
- 🆕 **08-25 逐執行緒重算（審查，用既有 raw、無新量測）——這頁的結論要升級**：
  `cpu_probe` 的 `thread` 欄一直都在，拆開來看，「取樣的成本」根本不是取樣在花：
  | 取樣率 | 隨樣本放大的執行緒合計 | **不隨樣本放大的那一條** | kernel 全部 |
  |---|---|---|---|
  | 1/1024（34.7 樣本/s） | ~0.3 | **45.1** | 55.4 |
  | 1/64（556 樣本/s，16×） | **~8.8** | **46.5** | 67.9 |
  ① **真正處理樣本的工作，即使在 556 樣本/秒也不到 9 個百分點**（ingest 執行緒 10× 放大、
     worker pool 十餘條各約 0.5）；② **一條不隨樣本數變動的執行緒獨自燒 46 點**；
  ③ 交叉條件證實它由「**有沒有流記錄**」觸發：取樣開但無流量 2.3%、有流量但取樣關 10.6%，
     **只有兩者同時成立才貴**。
  ⇒ **可引用的措辭**：「**遙測的成本幾乎與取樣率無關**——邊際成本極低（每樣本約 200 µs），
     固定成本極高。所以『能不能取樣更密』的答案是**可以、而且幾乎免費**。」
  🔴 **機制候選（消去法，尚未直接觀察，措辭要留餘地）**：kernel 內唯一以**毫秒級**週期執行的
     迴圈是 `FlowLinkUsageCollector::calFlowPathByQueried()`——**每 1 ms 重算所有流的路徑**
     （程式註解自述），其餘週期性執行緒皆 200 ms–1 s。**血緣：`28b8b13` 就有＝繼承缺陷**
     （因此在 A2 規則下**可以講**，但 B3.3 的 baseline 章節裁定仍適用，見 v1.5 摘要第 5 條）。
     未指認執行緒身分（tid 偏移跨版本不穩），**一次帶 kernel.log 的 live 跑即可定案**（工單 A）。
- 備註：⚠️ **涉及「刪掉 clone 也沒差」的句子必須並陳**：原 no-clone 控制組已撤回（裸 DELETE
  打在空簿記上＝no-op），零點由冷啟 n=3 重建——slide 用重建後數字、fine print 註明換過控制組。
  ⚠️ **這頁與 `page_matrix-decomposition` 的「206 µs/樣本」必須並陳讀**：那條線的斜率是**尾巴**，
  截距（48.5% vs 冷啟零點 2.89%）才是主體；由斜率外推的容量天花板**已撤回**，不得引用。

**Page ?? — The marginal cost of a sample**（31 字元）
- 副標：`Five genuine load cells fit a line at 206 µs per sample — this page states the range it holds in, and the intercept it lacks`（125 字元）
- 版型：整頁圖 `figures/page_matrix-decomposition.png`。
- 要點：
  ① 邊際成本 **206 µs/sample**，在 **34.7–556.1 samples/s** 內殘差 ≤0.4；
  ② 🔑 **線不過原點**：擬合截距 48.5% vs 實測零點 2.8%（差 65× 噪音地板）——所以它是
     **區間內的邊際成本、不是可以拿去除的容量**；外推的天花板已撤回；
  ③ poll-off 臂的零由 poll-on 臂繼承、兩臂差 7.7 點＝落在矩陣 poll 欄內（自洽檢查）。
- 素材：FIGURES.md item 5／7／9；`analyse_matrix.py`。
- 備註：這頁是「誠實量測陳述」的示範——被問「上限多少」→「這條線只在量過的範圍內成立，
  範圍外我們量到它就是錯的」。

**Page ?? — iperf3 competes with the system under test**（41 字元）
- 副標：`The load generator's sending side is the single largest process on the box — so contention is measured, not assumed away`（119 字元）
- 版型：整頁圖 `figures/page_iperf-competes.png`。
- 要點：
  ① sender **100.6%（單核）≈ 最忙交換機的 2×**；receiver 13.1%；
  ② 三個同名 process 的角色由**出現時間**指認（server 先起、client `sleep 2` 後起——
     與 measure.sh 逐字吻合）；
  ③ 含意：所有共機量測都帶這個 confound——**量出來**，別假裝沒有。
- 素材：FIGURES.md item 2。

**Page ?? — The northbound API is one lane**（30 字元）
- 副標：`The kernel serves REST from a single-threaded io_context, present since the fork point — so the envelope is measured, not argued`（127 字元）
- 版型：整頁圖 `figures/page_api-concurrency-envelope.png`。
- 要點：
  ① 吞吐跨 **16× 併發持平**、延遲線性成長——與「完全序列化」預測差 **<2%**；
  ② 今天不咬人：7 個 app @1 Hz ≈ 執行緒的 8.3%；
  ③ 風險句（屬 baseline，A2 允許）：**一個卡 500 ms 的南向呼叫會佔掉 42 個請求的時間**。
- 素材：`doc/audit/2026-08-19_api-latency-vs-baseline/`＋FIGURES.md；`main.cpp:119`
  （`io_context{1}`，**28b8b13 就在**）。
- 備註：被問「要不要修」→「先量、再依風險排」；與本節環頁互相呼應——環正是
  「南向卡住把 REST 全部拖死」的極端實例。

**Page ?? — Is the jitter ours? A fork-point A/B**（37 字元）
- 副標：`One fabric, one flow, only the kernel binary swapped — today's kernel and the fork point both sit on the sampling floor`（117 字元）
- 版型：整頁圖 `figures/page_ladder-inherited.png`（三 panel）。
- 要點：
  ① **教授上次的問題，正面回答**：讀數離散度是**繼承的**——HEAD **1.06×** vs 28b8b13
     **0.98×** 於理論地板（100/√λ），差 0.05＝深在噪音裡；
  ② 沒有人加可避免的雜訊、也**沒有人在平滑**（比值遠低於 1 才是壞消息＝拿延遲換方差）；
  ③ 第三 panel＝deck 裡 08-18 的舊圖同框（1.11×）——不同天、不同開機、同一個地板。
- 素材：FIGURES.md item 10／14；`analyse_jitter_ab.py`；28b8b13 建置註記
  （`-Wno-error` 一行、語意不變）。
- 備註：rate 換算碼與拓撲模型跨 fork **逐位元組相同**＝靜態證據與動態 A/B 互證；
  量化階從格線改 scale bar 的取捨已記錄（λ≈70 時格線會糊掉主體）。

**Page ?? — A boot deadlock in the baseline, fixed**（39 字元）
- 副標：`Six of ten boots never converged; the dump names two full queues — mechanism, fix, and a same-boot A/B on one page`（115 字元）
- 版型：左半機制小圖（🆕 `figures/ring_two_queues.png`，讀 dump 畫；產生器待建，
  **ar 抓 ~1.9–2.1** 與本節其餘圖同帶，避免 E5 第 22 條的寬圖模式跳版）＋右半 A/B 表。
- 要點：
  ① **缺陷（08-24 報告列 open、本輪結案；存在於繼承的控制器碼，ancestry 已核實）**：
     控制器事件佇列互鎖——dump 直接印出**兩個佇列同滿**（12＋43 個發送者被擋，被擋數＝
     stack frames 逐格整除）；殺傷＝**餓死 kernel 的拓撲輪詢**（卡死 boot 回 4 次後永默
     vs 健康 23 次）。
  ② **修法**：handler 內兩個無時限查詢接上真 deadline（`cce9c5d`；timeout 原語上場前對
     「環真正卡住的兩種等待」自測 PASS）。**判死證據門檻未動。**
  ③ **同機開機 A/B（一小時內）**：無修法 **2/3 永久卡死** → 修法 **0/3、保真 3/3**
     （128 hosts＋288 edges）；關鍵格＝阻塞真的發生（28 次逾時）而後**自癒**——kernel
     輪詢斷流 **148 s** 後完整恢復（`cb0eedc`）。
  ④ **互補修法 B 已完成並驗證**（`bfb0569`/`c986ca0`）：重建整個搬離事件迴圈，
     驗證方式從「要召喚得出缺陷」換成**可直接檢查的不變量**——事件迴圈的呼叫堆疊不得
     含同步拓撲查詢；**3 次開機 × 9 份快照 ＝ 159 個迴圈堆疊、零違規**，保真 3/3。
     **A 的上限在 B 之後仍生效（B 疊在 A 上，不是取代）。**
- fine print：A 臂 N=3（P(0/3|2/3)≈3.7% 單尾）＝首驗非結論；B 的不變量檢查器先在
  **六份已知故障快照上驗過偵測力（6/6、逐一點名正確站點）**才用於判定。
- 素材：`doc/audit/2026-08-25_ring-edge-fix/`（PREREG＋phase0/2＋兩份 selftest PASS）、
  `doc/audit/2026-08-24_full-stack-run/`（6/10 與 dumps）、審查複算件（同目錄
  `auditer_sweep_replicate.txt`）。
  ⑤ **「是不是我們自己的加速造成的」——量測型否定答案**（08-25 Phase 5，教授可能會問）：
     stock Ryu 常數下佇列 **2.3 s** 填滿、我們的設定 **1.8 s**（到達率 56–59 vs 69–72 /s），
     **兩者皆遠小於任何一次阻塞事件**（settle 窗 40 s、通知鏈 10×5 s）⇒ **加速改變的是
     填滿速度的 1.2 倍，不是缺陷的存在性**。機制：`LLDP_SEND_PERIOD_PER_PORT=0.9` 綁住
     每 port 探測週期，該常數只節流同一輪內的發送。
- 備註（口頭備，**不上台**）：被問「為什麼之前修不好」→ 卡點遷移史（早期兩修法只蓋三站
  之一、逾時擋停車不擋佔用）；被問「怎麼重現」→ 靶率非單調（同 boot 4/4→1/4→2/4→2/3）、
  示範日 SOP＝先重開機器；被問「來源」→ ancestry 核實紀錄在案（措辭待 Adam 終審，
  見 v1.5 摘要第 5 條）。⚠️ 同一常數對**兩個量**的槓桿不同（sweep 完成時間 3.9× vs 穩態
  到達率 1.2×）——若同時引 08-21 的 3.9×，兩者必須並陳說明量的是不同東西。

---

#### C4-bis. 🆕 08-25 輪：把取樣率往上推到 1/1（三頁）

> 出自 `doc/audit/2026-08-25_sampling-rounds/`（PREREG `a7c2bd7`＋`cell_verdict.py`＋
> `ticket_a.py`＋`ladder_ext.sh`），raw 在 08-20 那個 `raw/`（前綴 `r001…r032`，與 `m*` 互斥）。
> 判準與中止條件**在跑之前**寫死於 PREREG §4/§7；圖的載入器與量子算術 import 自 `plot_figures.py`。
> 指認：kernel `3367d0e9…`、bmv2-fast `3ff54b5c…`、HEAD `85bbecc`。審查驗收 PASS（複算全符）。

**Page ?? — Sampling harder stops buying precision** 🆕🔑（38 字元）
- 副標：`Five sampling rates on one fixed 200 Mbit/s flow — the dispersion tracks √λ exactly, until 1 in 32, and then stops`（114 字元）
- 版型：整頁圖 `figures/page_ladder-across-rates.png`（五格單列，ar 2.39）。
- 要點：
  ① **到 1/64 為止，實測離散度就是理論地板**——1.03× / 1.01× / 1.03×，取樣統計是唯一雜訊源；
  ② **1/32 起脫離**（1.12×），**1/16 已達 1.74×**：地板照 √λ 降到 3.0%，實測卻**升回** 5.2%；
  ③ ⇒ **再往上取樣買不到精度**。08-20 那條「4× 取樣換 1.83× 收緊」的趨勢在 1/64 之後**終止**。
- 素材：`doc/audit/2026-08-25_sampling-rounds/`（`8c0516d`）；λ 17.1→1112、量子 11.81→0.185 Mbit/s。
- 備註：五格是**從十一格挑的、理由寫在 `plot_ladder_rates.py` 的 CELLS 註解裡**（不是靜默截斷）：
  丟掉的四格全是 DATAPLANE-HURT，它們的離散度不是量化離散度，畫在量化梯上會宣稱資料不支持的事。

**Page ?? — Above 1-in-16, sampling costs the data plane** 🆕🔑（44 字元）
- 副標：`The ceiling is not in the sample path — the twin/counter ratio never moves, while the receiver loses 85% of the flow`（116 字元）
- 版型：🆕 **整頁圖 `figures/page_sampling-ceiling.png`**（3040×1270、ar 2.39）＋表下兩條列。
  三個 panel 共用一條 x 軸：**吞吐 206→30 Mbit/s**、**掉包 0.03%→85.2%**、**λ 平在 ~2550**。
  🔑 **第三個 panel 是這頁的重點**——它證明「取樣調更兇並沒有換到更多樣本，只是把資料面打爛」。
  淺底色區＝可用區（≤1/16），紅虛線＝天花板。**表格降級成講稿備援，不上版。**
  ⚠️ 產圖時 **不可**用 `delivered()[0]` 當吞吐：那是 iperf3 **發送端**的 offered，六格都是平的 200，
  畫出來會宣稱吞吐從未變過（正好相反）。用 verdict 的 `gt_mbit`。這個錯我犯過一次，看圖才發現。
- 🆕 **建議加一頁在本頁之後**：`figures/page_who-is-the-bottleneck.png`
  （CPU 三條線＋掉包長條）。**bmv2 爬到 206% 之後往下掉的那條線，就是「被餓死不是飽和」的視覺證據**，
  而 proxy 壓平在 ~144% 的位置正好對上掉包起點。這頁回答「那為什麼不加機器」。
- 要點：
  ① **天花板是資料面的，不是樣本路徑的**：七格 `twin/gt` 全部 ≈1.00，**SATURATED 一次都沒觸發**；
  ② 接收端掉包 0.03% → **5.1% → 45.3% → 70.8% → 85.2%**，吞吐 206 → **29.5 Mbit/s**；
  ③ **λ 卡在單邊 ~2,550/秒**，取樣率再翻倍只加 1.7%。
     🔴 **全邊換算（~5,100）已撤回**：它依賴一個 2.03 的倍率，而工單 D 由位元組獨立推出的
     倍率是 ~1.0，兩者矛盾未解 ⇒ **只講單邊**（單邊數字不依賴那個倍率）。
  ④ 🆕 **可以開到哪、再往上會怎樣、我們推測為什麼**（Adam 08-25 指定要講）：
     **可用天花板 ≈ 1/16。** 再往上：1/8 開始掉 5.1%，1/1 掉 **87%**、吞吐從 206 崩到 **21 Mbit/s**。
     **推測的機制（明標為推測）**：牆在遙測管線的**接收路徑**，且成本是**每樣本的固定成本**
     （syscall＋解析），不是每 byte ⇒ 修法是把固定成本攤掉＝**merge**，**尚未量測**。
     🔑 **這個推測不是猜的**：工單 D 事前寫死「若成本每 byte ⇒ 截短後牆上移一個數量級」，
     實測截短 5.6× 之後四格全部略差 ⇒ **per-byte 已被否證**（見 C5 那頁）。
     支持的 CPU 形狀：**proxy 在 ~145% 平掉、掉包同時開始**；**bmv2 峰值 206% 之後往下掉**
     ＝被餓死不是飽和；全機最忙只用到 **14 核裡的 4.4 核** ⇒ **不是機器不夠力**。
- 表格（1/32、1/16、1/8、1/4、1/2、1/1）：`ratio` 1.000/0.997/1.000/1.005/1.003/0.998；
  `lost%` 0.03/0.02/**5.1**/**45.3**/**70.8**/**85.2**；`gt` 206/206/196/110/57.8/29.5 Mbit/s。
- 素材：同上（`8c0516d`）；門檻 2.0% 的出處＝單流基線 0.513% vs `5965983` 的 1.1/24.8/34.1。
- 備註（**兩條措辭上限，審查明令**）：
  🔴 **不得**說「當初撤回的 ~4,900 樣本/秒其實是對的」——數字接近但**機制不同**（那個預測 CPU
  天花板，實測是吞吐崩塌），必須並陳。🔴 **不得**說「bmv2 撐不住」——**機制未指認**（同大規模輪紀律）。
  口頭可講的內部一致性：λ 停止線性**完全由吞吐解釋**（`2394×2×(57.79/109.8)=2520` vs 實測 2511，
  三格皆吻合 <0.7%）。**這四格是被第三道檢查抓到的**——前兩道（ratio、gt）在 45% 掉包時毫無反應。

**Page ?? — The 45-point thread is not sampling cost** 🆕🔑（40 字元）
- 副標：`Named from the kernel log of the same boot, not from a tid offset — 32× more samples move it by 1%`（99 字元）
- 版型：三條列＋右四欄表。
- 要點：
  ① **`calFlowPathByQueried` = 46.31% → 46.84%，取樣 ×32 只動 1%** ⇒ 那 45 個點與樣本數**無關**，
     是 1 kHz 全流路徑重算迴圈（**繼承缺陷，baseline `28b8b13` 就有**）；
  ② **`run` 才是 ingest**（3.98% → 13.86%，×3.48 隨取樣放大）；
  ③ 兩條具名執行緒（`testCalAvgFlowSendingRatesRandomly`、`purgeIdleFlows`）**每一格都是 0.00%**。
- 素材：`ticket_a.py`（`8c0516d`）；每格的 `kernel.log` 與 cpu trace 出自**同一次開機**。
- 備註：46.31% 落在 08-20 發表的 45.0/46.6 之間＝**單位換算的獨立佐證**。
  方法上的一句話（口頭備）：08-20 那輪**沒有歸檔 kernel.log**，而 tid−pid 偏移**跨版本不穩**
  （該 trace +13、今日 build +11）⇒ 舊資料的執行緒身分**永遠對不回名字**，只能靠新一輪同時留兩份。

**Page ?? — Does only λ decide precision?**（36 字元）⏳ **進行中，勿定稿**
- 副標：`Six cells, two levels, each reached from opposite directions — the pairing worked, the answer is not yet decidable`（113 字元）
- 版型：六列表格＋兩條列。
- 🔴 **審查裁定 INCONCLUSIVE，本頁在控制組回來之前不得寫成結論。**
- 已經成立的（可上台）：
  ① **配對成功**——λ 在各水準內吻合到 **0.84%（A）/ 0.44%（B）**，所以任何分歧都不是沒對齊造成的；
  ② 六格 **全部健康**（無 SATURATED、無 DATAPLANE-HURT，掉包 0.005–0.666%）；
  ③ 實測 `spread/floor`：A ＝ 1.005 / 1.145 / 1.523，B ＝ 1.532 / 2.095 / 2.421。
- 🔴 **還不能上台的**：「同 λ 的格子不等價 ⇒ 矩陣不能被省」這個**反轉結論**。
  它掛在「每一對都超過 0.1」，而那句話**靠一對只超標 0.040 的邊際案例**（A 的 1.005 vs 1.145 ＝ 0.140）。
  **格間條件噪聲目前沒有任何數字。**
- ✅ **控制組已跑完（`c62bf3e`），而且事前寫死的判讀觸發了 ⇒ 反轉結論永久收回。**
  同參數三次、每次夾一次完整 fabric 重建：`spread/floor` ＝ **1.145 / 1.249 / 1.385**，
  正式 Δ ＝ **0.136**、三次全距 **0.240**，而 λ 仍吻合到 1.1%（⇒ 散佈在量測、不在設計）。
  **0.136 ≥ 0.1 ⇒ 判準分辨不了格與格**，而且它幾乎吃掉水準 A 那個只超標 0.040 的邊際對——
  審查指名整個主張就靠那一對，**確實如此**。
  🔴 **有幾對確實超過 0.240 的散佈，但那救不回來**：預註冊寫的是「每一對都超過 0.1」，
  看完資料才把門檻放寬到 0.24，正是預註冊存在的目的所要禁止的動作。那是**下一輪的假說**
  （要自己的預註冊和一份真的噪聲分布），不是三個點的全距。
- **⇒ 本頁現在可以定稿了，但方向相反**：它是一個**被自己的控制組推翻的假說**，不是一個結論。
  兩個選擇（Adam 裁）：**(a)** 留著，當「我們押了一個漂亮的反轉、控制組把它殺掉」的實例；
  **(b)** 整頁拿掉，六格資料併進講稿備援。
  🔑 **選 (a) 的理由**：這頁原本的反轉結論**已經被寫進 deck 草稿**，是審查堅持標「進行中」才沒上台——
  這件事本身比那六格數字有價值得多。
- 素材：`doc/audit/2026-08-25_sampling-rounds/`（`8d109f2` 結果、`760775f` 校準、`70f2e64` 前提）。
- 備註：兩個事前預測在本輪被推翻，其中一個是**寫下之後的下一格**打臉的（quantum 歸因）——
  這條是否上台，框法待 Adam 裁，**先不做成一頁**。

---

### C5. 🆕 教授點名：packet truncate 與 merge

**Page ?? — Truncation: tried, works, and buys nothing** 🆕🔑（41 字元，產檔時用 `Truncation buys nothing`）
- 副標：`The switch knob was an outage; the P4 extern is not — it cuts 5.6x of the bytes and moves the ceiling not at all`（111 字元）
- 版型：🆕 **整頁圖 `figures/page_truncate-bought-nothing.png`**（3040×1270、ar 2.39）＋結果條列。
  **左 panel**＝兩根長條，P4Runtime stream 位元組 13.4 MB → 2.4 MB，標「5.60× fewer bytes」；
  **右 panel**＝四個取樣率的 λ 截短前→後斜線圖，**四條線全部往下**（2123→2003、2394→2068、
  2511→2126、2554→**1880**）。
  🔑 **左右對比本身就是論證**：左邊看起來大獲全勝、右邊什麼都沒買到。教授不需要讀任何一行字
  就會看出「做了、真的有效、但沒用」。原本的三欄現況表降級成講稿備援。
- ⚠️ **08-25 22:xx 改寫**：本頁原為「status and **plan**」，第 ④ 點寫著「Adam 08-25 裁：要做 P4
  truncate extern 實驗」。**那個實驗 08-25 20:05 已經跑完，而且結論是否定的。** 計畫式寫法若上台，
  講的是一件已經有答案的事。
- 要點：
  ① **emitter 側截短一直開著**（128 B，`sflow_emitter.py:88/:174`，07-28 起、無旗標）。
  ② **switch 側 runtime 截短已實測＝無聲全滅**（clone `packet_length_bytes=128` → 全邊讀 0、
     無任何錯誤；08-20 REPORT §「not an optimisation, it is an outage」）——
     **「量測過的否決」已在手**；emitter 側自此是量測過的必要條件（`p4_client.py:347`）。
  ③ **merge 建好、有測試、有意識未接**（`build_datagram` 原生多樣本＋三樣本測試；
     docstring 明寫「kernel 兩種都吃」；production 單發）。
  ④ 🆕 **P4 `truncate()` extern ＝ 做了、有效、但買不到東西**（08-25，`9424535`）。
     **有效**：A/B 只動一個常數，bmv2→proxy 的 gRPC 位元組 **5.60× 下降**（13.39→2.39 MB / 120 s）；
     **沒有全滅**（ratio 1.016、λ 70.76、**35** 個相異讀值，對照臂 32——與 knob 的
     「全邊讀 0」正好相反）；
     ⚠️ **審查更正（08-25）**：此處原寫「201 個相異讀值」，那是 `t008_poll`（1/8 那格）的值，
     不是閘門那格的。閘門兩臂的真值是 `d256trunc_poll` **35** 與 `d256full_poll` **32**
     （`gate_d.out`）。**結論不變**（35≠0 一樣證明沒有全滅），但引用要指對格子。
     **量子逐位元不變** ⇒ 速率換算沒被動到。
     **但天花板沒有移動**：1/8→1/1 四格重跑，掉包 5.09→**8.11**、45.3→**50.1**、70.8→**74.4**、
     85.2→**87.1**，四格**全部略差**。⇒ **成本是每樣本、不是每 byte。**
  ⑤ 🔑 **比「沒幫助」更強的一條**：λ 平台從 ~2550 掉到 ~2100（1/1 那格 **1880**）。
     **少送 5.6 倍的資料，擠過去的樣本反而更少** ⇒ 位元組不只不是限制，減少它還要付代價。
  ⑥ **merge 因此是被指認出來的下一步，而不是備選。**
     🆕 **08-26 01:07 已接線並通過驗證閘門**（`gate_e.out`，審查獨立複算）：
     同一格 1/256 兩臂，只差 `NDTWIN_SFLOW_BATCH`（1 vs 8）——
     **proxy→kernel 的 datagram 從 209.8/s 降到 30.6/s（6.87×）**，
     而 **λ 70.81 → 70.27（−0.8%）、`ratio` 1.016 → 1.008、quantum 逐位元相同**
     ⇒ **merge 真的在 merge，樣本一個都沒少，遙測沒被殺死。**
     理想是 8×、實測 6.87×，差額（超出 518 個 datagram ＝ 14.2%）與 `batch_max_delay_s=0.2`
     的 age-timer 沖出未滿批次一致。**事前寫死的 E-P4 滿足**（ratio 與 λ 都沒掉
     ⇒ 收尾時未滿的那批有被 flush，不是實作 bug）。
  ⑦ 🆕🔑 **08-26 03:16 工單 F：merge 真的省下工作，而且這次分得開。**
     整頁圖 **`figures/page_merge-effect.png`**。1/16 交替跑六次、只換一個值：
     **proxy CPU 72.4 → 62.7（−13.4%）、kernel CPU 103.6 → 86.7（−16.4%）**，
     而**同設定重跑的全距只有 2.8 / 1.8 點** ⇒ **效果大於自己的噪聲，三對三完全沒有重疊。**
     斷言：datagram **3334/s → 447/s（7.46×）**＝merge 真的開著；
     **λ 全程 1112–1120 不變** ⇒ 樣本量相同，這是**同樣工作量下的成本**。
     🔑 **為什麼是 1/16**：工單 E 在 1/8 問同一題失敗了（對照組 22.01 vs 29.49，差 7.5 點、
     效果只有 4.4 點）。而同一批 fabric 在 1/256 跨兩次完整重建只差 0.3 點
     ⇒ **吵的不是儀器，是工作點。** 1/16 有 16 倍樣本量、卻離懸崖很遠。
  ⑧ 🔴 **但這**不是**天花板的數字，講的時候要分清楚。**
     量到的是「同一個工作點上，每單位取樣工作的成本降低」。
     **不得**把這條 CPU-vs-取樣率的線外推去算飽和點——08-20 那輪已經證明它外推到零
     會比實測零點高 45 點。**「省下 13-16% 的成本」可以講；「天花板上移多少」不能。**
  ⑨ 🔴 **原第 ⑦ 條（對天花板影響尚未量測）仍然成立，只是範圍縮小了：**
     閘門證明的是「它做得到」，不是「它有用」。事前寫死的兩個結局都還開著：
     成本若在**送側** ⇒ 牆上移；若在**收側**（gRPC 收流＋Python 解析＋per-callback）⇒ 牆不動，
     而下一把刀是收側的並行度。**1/8 那格沒跑，所以沒有答案。**
  ⑧ ⚠️ **一個未預期的副作用，要記不要解釋**：`distinct` 從 **34 掉到 14**
     ——批次化改變了 twin 讀值的時間粒度（`spread` 11.52→12.04）。總量沒變（ratio 不變），
     但**若日後有人在 batching 開啟下引用 spread/floor，這條會咬人**。機制未指認。
- 🆕 **C5 建議拆成兩頁**（各有整頁圖，兩張都已產出）：
  - **C5a ＝ truncate**：`figures/page_truncate-bought-nothing.png`（要點 ①–⑤）
  - **C5b ＝ merge 閘門**：🆕 **`figures/page_merge-gate.png`**（要點 ⑥–⑧）。
    三個 panel 都是 batch=1 → batch=8 的長條對照：
    **① 該變的變了**——datagram 209.8/s → **30.6/s（6.86×）**，紅虛線標理想的 8×；
    **② 不該變的沒變**——λ 70.8 → 70.3（**−0.76%**）；
    **③ 不該變的沒變**——ratio 1.016 → 1.008（**−0.79%**）。
    🔑 **兩個平的 panel 才是證據，不是裝飾**：E-P4 在跑之前就寫死「merge 若動到這兩個之一，
    那是實作 bug 不是 merge 有效」。右下角固定一行紅字：**Effect on the sampling ceiling: NOT MEASURED.**
- 🔑 **這頁的誠實版故事線**（不需要 1/8 也完整）：
  試了最直覺的解法（truncate）→ **它有效但買不到東西** → 那個代價本身指認出成本是每樣本
  → 做出 merge 並**驗證它真的合併** → **它對牆的作用是下一個問題**。
  **一個驗證過的「尚未量測」，勝過一個沒驗證的數字。**
- 素材：`p4_proxy/proxy_agent/sflow_emitter.py`、`ndtwin_switch.p4:389`、
  `doc/audit/2026-08-20_sampling-rate-and-cpu/REPORT.md`、`p4_proxy/tests/test_sflow_emitter.py`。
- 備註：開銷的既有實測口頭帶：1/64 取樣成本落在 **kernel 57＋proxy 20 個百分點（單核）**、
  bmv2 跨率平坦（率間內部對照）；⚠️ 涉及「sFlow 對 bmv2 零成本」的句子必須並陳
  no-clone 控制組撤回＋冷啟零點（v1.5 摘要第 4 條同一件事）。

---

## D. 素材出處速查

| 主題 | 首選出處 |
|---|---|
| bug 的完整技術細節 | `git show <hash>` 的 commit message（品質極高，多數可直接改寫成投影片） |
| 已知問題的單一清單 | **`doc/KNOWN-ISSUES.md`**（17 條，按「正常操作會不會踩到」排序） |
| 測試工具敘述 | `doc/2026-08-07_testing_tools_overview.md` |
| P4 計畫與 phase 狀態 | `doc/2026-07-27_p4_bmv2_support_plan.md` |
| 實測結果 | `doc/audit/` 下各輪的 `REPORT.md`（含 raw log 與可重跑的腳本） |
| failover 控制實驗 | `doc/audit/2026-08-17_p4-vs-ovs-matched-topology/`、`doc/audit/2026-08-19_failover-provenance/` |
| **① 拓撲查詢已排除** 🆕 | **`doc/audit/2026-08-21_ryu-topology-scaling/`**（含探針、raw、`ovs4_connectivity_check.sh`） |
| **兩顆 bmv2 的識別碼** 🆕 | **`doc/audit/bmv2-binary-provenance.md`**（sha256／BuildID／flags；`--version` 兩顆相同） |
| sFlow 精度 | `doc/audit/2026-08-19_p4-sflow-accuracy/` |
| API 延遲 vs baseline | `doc/audit/2026-08-19_api-latency-vs-baseline/` |
| bmv2 吞吐 A/B | `doc/2026-08-15_bmv2-performance-report.md` |
| mastership 規格核對 | `doc/2026-08-13_p4runtime-mastership-spec-check.md` |
| demo 錄製 | `<8/20 資料夾>/2026-08-19_demo-recording-runbook.md` |
| 增刪行數 | `generator/count_lines.py`（見 E4） |

⚠️ **`doc/` 底下的檔名都有日期前綴且持續有新檔。引用前先 `ls doc/`，不要照抄上表的路徑。**

---

## E. 視覺與版面規格（Adam 已認可，照用）

**產生器**：`generator/deck_style.js` —— 8/20 那份 `build_deck.js` 的 helper 全部抽出來、
去掉內容之後的版本。**新頁一律沿用裡面的 helper 與色票，不要另創風格。**

```js
const S = require("./deck_style");
const pres = new pptxgen();
pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
pres.layout = "WIDE";
S.bind(pres);
const s = S.newSlide();
S.pageTitle(s, "Title", "Subtitle");
```

### E1. 設計原則

1. **極簡。** 實驗室簡報風格，不是行銷簡報。白底、大量留白、細線分隔。
2. **顏色克制。** 全篇只有一個強調色。不用色塊卡片、不用深色底頁（封面也不用）、不用彩色徽章。
3. ~~**以編號條列為主軸。** `1 / 2 / 3` ＋ 粗體小標 ＋ 說明段。需要時才加示意圖。~~
   🔴 **2026-08-30 起改成「標籤 → 值」的列式，見 E3a。** 編號條列只留給 8/20、8/27 兩份既有 deck。
4. **不要淡灰字。** 淡灰在投影機上幾乎看不見。判準：不重要的資訊**直接刪掉**（口述帶過即可），
   重要的用可辨識的深色或強調色。
5. **不要為了填版面加字。** 寧可留白。
6. 🔑 **精簡的判準**：一段內文如果口述時一定會講、而投影片上只是把口述寫下來，**就只留粗體標題**。
   投影片留給「聽的人自己看比較快」的東西：**數字、表格、圖**。

### E2. 色票與字體

| 用途 | 色碼 | 說明 |
|---|---|---|
| `INK` 標題 | `1A1A1A` | 頁標題、條列小標 |
| `BODY` 內文 | `2E2E2E` | 主要說明文字 |
| `MUTED` 次要 | `4F4F4F` | 副標、註記、腳註（**不得再淡**） |
| `FAINT` 說明 | `6E6E6E` | 欄位標籤、頁碼 |
| `RULE` 細線 | `D0D0D0` | 分隔線、方框外框 |
| `ACCENT` 強調 | `065A82` | 條列編號、關鍵數字、強調句、圖中的新增元素、節次標記 |
| `ACCENT_BG` | `EEF3F6` | 極淡強調底 |
| `PANEL` | `F7F8F9` | 中性淡底（判斷框、對照框） |
| `WARNC` | `9C3B2E` | **只用在「量到的那個值是壞消息」的地方** |
| `WARN_BG` | `FBF2F0` | 極淡警示底（失敗出口框） |

| 元素 | 字體 | 字級 |
|---|---|---|
| 頁標題 | Cambria bold | 30–32pt（封面／節封面 44pt） |
| 副標 | Calibri | 14pt，`MUTED`　🔴 **新頁不用副標，改 kicker，見 E3a** |
| 節次標記 | Calibri bold | 10.5pt，`ACCENT`，y=0.28，`charSpacing: 1.0` |
| 條列小標 | Calibri bold | 15.5pt，`INK` |
| 條列編號 | Calibri bold | 13pt，`ACCENT` |
| 內文 | Calibri | 11.5–12.5pt，`BODY`　🔴 **新頁改 16pt，見 E3a** |
| 腳註 | Calibri | 10–11pt，`MUTED` |
| 程式碼／識別碼／endpoint | Courier New | 隨上下文 |
| **圖（架構圖、流程圖）** | **Arial** | 標題 15pt bold、內文 8–10pt |

**不要用 Aptos 或微軟正黑體**（前者無可靠替代、後者是中文版設定）。

### E3. 版面

- 版面尺寸 **13.333 × 7.5 吋（16:9）**。左右邊界 `M = 0.85"`，內容寬 `CW = 11.633"`。
- 頁標題 y=0.62、副標 y=1.32、標題下細線 y=1.86；內容自 y≈2.16 起。
- **圖頁例外**：圖自帶標題時用 Arial 標題畫在 **y=0.50**、副標 y=0.84。
  🔴 **y 一定要 ≥ 0.50**，因為 `sectionTab` 畫在 y=0.28。
- 頁碼右下 `x=12.0, y=6.92`，10pt `FAINT`。封面不放頁碼，**節封面要放**。
- 條列間距至少 **1.24"**（兩行內文）／**1.42"**（三行）；每段內文寬度不超過 7.5"。
- **頁碼自動計算**：`newSlide()` 遞增、`pageNum(s)` 讀取。**不要寫死頁碼**——
  8/19 的重編頁碼就是這樣出錯的。
  ⚠️ 但 **Outline 的 `pp. x–y` 與內文的「page N」交叉引用仍是寫死字串**，改結構後要人工對一次。
- **產出後必做**：轉 PDF → `pdftoppm` 逐頁看圖，檢查文字溢出與撞行。**這步不能省。**

### 🆕 E3a. **版面文法（Adam 2026-08-30 裁定：以後一律照這個）**

> 起因：Adam 拿 `qec_week1_weekly_update_unified.pptx` 對照——「**字少、沒有廢話、
> 很清楚地傳達資訊**」。範例五頁在 `903/NDTwin_style-examples.pptx`，
> 參考實作 `generator/build_examples.js`，helper 已進 `deck_style.js`。
>
> 🔴 **這一節取代 E1 第 3 條（編號條列為主軸）與 E4d（副標句型）在新頁上的效力。**
> 8/20 與 8/27 兩份既有 deck 不回頭改，它們照舊。

**五條規則，缺一不可：**

1. **標籤 → 值。** 左邊全大寫短標籤＋色條，右邊放值。**標籤是名字，不是句子**
   （`RESULT`／`LIMIT`／`WITHDRAWN`／`NAMED HOW`）。helper：`S.row()`。
2. **`·` 取代動詞。** 值是片語串接，不是句子：
   `detect 44.9 s · debounce 3.0 · recompute 0.25`。**沒有動詞、沒有冠詞。**
   一行值超過兩行就是內容太多，砍內容，不要縮字。
3. **兩個字的判詞。** `ANSWERED / IN PART`、`RESULT / LIMIT`、`CONFIRMED / WITHDRAWN`、
   `NARROWED / OPEN`。這就是原本 settled／open 的紀律，只是從一句話壓成一個詞。
   色條顏色本身承載判定（`ACCENT` ＝成立、`WARNC` ＝不成立），**不需要另外再上色**。
   helper：`S.chip()`。
4. **證據頁先問問題。** `QUESTION` 區塊放在證據上方，頁面先說它在回答什麼。
   helper：`S.question()`。
5. **圖可以放在條列旁邊，不必獨佔一頁。** 前提見下面第 32 條。

**字級表 v2（🔴 覆蓋 E2 那張表的內文列；v1 的數字放在括號裡，僅供對照）：**

| 元素 | 字級 | 說明 |
|---|---|---|
| 頁標題 | **36pt**（v1 34）Cambria bold，全大寫 | `S.head()` |
| kicker（取代副標） | **15pt**（13.5）`FAINT` | **片語，不是句子**，六個詞為上限 |
| 值（內文） | **18pt**（16）`BODY` | 頁面主體 |
| 標籤 | **16pt**（14）bold | |
| 問句 | **22pt**（19）／qualifier 14.5pt | |
| 表格 | **15pt**（13.5） | |
| 判詞 chip | **13pt**（12）bold | |
| keyLine | **16pt**（14）bold `ACCENT` | |
| 頁底註 | **12pt**（11）`FAINT` | **全頁最小的東西，不得再小** |
| 🆕 大數字頁 | **68pt** 數字＋15.5pt 說明 | `S.bigStats()`，見下 |

常數集中在 `deck_style.js` 的 **`T` 物件**，helper 全部從 `T` 取預設——再調只改一處。

🆕 **`S.bigStats(s, [[數字, 說明], …], y0)`：一頁四到六個大數字，其他什麼都不放。**
用在「投影片只是跳板」的時候——9/03 的手冊節就是：**教授要看的是網站本身**，
所以那頁只給六個數字，`keyLine` 一句 `→ the manual itself, live` 就換到瀏覽器。
🔑 **判準：如果聽眾接下來會直接看到那個東西，投影片就不要在上面重做一次它。**

🔑 **砍字與放大是同一件事，不是兩件事。** 第一版只砍字、字級沒動（維持 12.5），
等於把剛空出來的版面浪費掉——Adam 的回覆是「**字太小**」。
**砍掉的字就是拿來換字級的**，兩者要一起做。
🔴 **這個錯犯了兩次。** 09-01 把 903 從 32 頁砍到 23 頁，字級又忘了跟著動，
Adam 第二次講「原本的字太小了」⇒ 才有上表的 v2。
**規則：每砍一輪字，字級預設就往上一階，然後再問要不要收回來**——
反過來（先問再調）兩次都失敗了。

🔑 **副標（E4d 那種 ≤130 字元的完整句子）在新格式裡整條刪掉。**
每頁都有一句約 110 字元的副標，光這一項就佔全部字數的三分之一。

### E4. 增刪行數的計算口徑

**只有一支腳本：`generator/count_lines.py`。** 它逐檔計算，再由同一份逐檔資料彙總出四大類，
所以彙總頁與明細頁**不可能兜不攏**。輸出 `line_counts.json`。

> ⚠️ 曾經寫過兩支腳本各算各的，規則沒對齊，兩頁 kernel 數字差 24 行卻找不出原因。
> **不要再拆成兩支。**

規則：

- 基準 `28b8b13..HEAD`，`--unified=0`。
- **排除註解行與空行**。`.cpp/.hpp/.h/.p4` 去 `//`、`/* */`、`*` 開頭；
  `.py/.sh/.yml/.cmake` 去 `#` 開頭；`.md` 只去空行與 `<!-- -->`。
- 排除路徑：`build*`、`.test_run/`、`Testing/`、`test_env/`、`.vscode/`、`**/venv/**`、`*.pyc`。
- 排除檔案：`intelligent_router.py`（實驗室既有的 Ryu 控制程式，隨 groundwork commit 帶入）、`.gitignore`。
- 分類：`kernel` = `src/`、`include/`、`setting/`、`cmake/`、`CMakeLists.txt`；
  `proxy` = `p4_proxy/`（但 `p4_proxy/tests/` 歸 test）；
  `test` = `tests/`、`tools/`、`.github/`、`p4_proxy/tests/`、根目錄測試/工具腳本；
  `doc` = `doc/`、任何 `.md`。
- `setting/*.json` 是**設定資料不是程式碼**。要嘛兩頁都含、要嘛兩頁都不含，
  **混用就要在腳註寫清楚差額是哪幾個檔**。
- **簡報上必須註明口徑**（8/20 的腳註原句）：
  `Diffed against baseline 28b8b13. Comment lines, blank lines and build artefacts are excluded;
  intelligent_router.py is excluded as the lab's pre-existing Ryu controller.`

### E4a. 架構圖的畫法

用 `aBox` / `aText` / `aArrow` / `aDash` / `aCloud` 畫，字體 Arial、框線黑 1pt、白底。
座標取自 Adam 的 `NDTwin_Arch.pptx`（`<a:off>` / `<a:ext>`，EMU ÷ 914400 = 吋）。

- **兩張架構圖（原始／加上 P4）的上半部共用一個 `archTop()`**，只有虛線以下不同——
  這是刻意的，讓聽眾一眼看出「上面沒動」。
  🔴 `archTop()` 太長沒抽進 `deck_style.js`，**在
  `<8/20 資料夾>/generator/build_deck.js` 裡，要用直接搬**。
- 關鍵座標：上虛線 y=1.77、kernel 框 y=1.99 h=2.93（底 4.92）、下虛線 y=5.86、
  雲 y≈6.30 h=1.10、右側 Tools 分隔虛線 x=10.02。控制器框放 y=5.32（**不是 5.16**）。
- **新增元素一律 `ACCENT`，既有元素維持全黑**——這個對比就是整頁的訊息。
- `aArrow(s, x, y, w, h, dir)` 的 `dir`：`"up"`／`"down"`／`"both"`／`"right"`／`"left"`／`"plain"`（無箭頭）。
- 要再加第三條資料面時：雲寬 4.05" × 2 已經吃滿 0.35→9.35，第三朵得把三朵都縮到 ~3.0"。

### E4b. 流程圖的畫法（8/20 新增，三頁在用）

用 `fStep` / `fTest` / `fArrow` / `fBranch` / `fHeader`。**畫的是程式裡真正的控制流，
不是敘述的圖示化**——8/20 的三張都是直接讀原始碼畫的。

- **判斷框** `fTest`：`PANEL` 淡底 ＋ 1.25pt 框，條件用 **Courier New 粗體**，下面一行 8pt 灰字解釋。
- **步驟框** `fStep`：白底或 `ACCENT_BG`（我方新增的用後者），粗體標題 ＋ 灰色細節。
- **終端框**：細框 ＋ 該色文字。成功用 `MUTED`／`ACCENT`，失敗用 `WARNC` ＋ `WARN_BG`。
- **分支標籤** `fBranch`：7.5pt，`h` 給 0.13–0.16（**預設 0.16 在 0.12" 的箭頭間隙裡會被下面的框切到**）。
- **輪詢要畫回頭線**，否則看不出它是迴圈（三段：往左、往上、往右）。
- 右欄 7.5pt 灰字註記，**每個終端配一則**，講「為什麼是這個判定」。
- 🔑 **流程圖比表格多講一件事：順序。** 8/20 的 Liveness 原本是三態並列表，
  看起來像三個平等選項；實際上原始碼是**一條有順序的判斷鏈**，而順序就是設計。

### E4c. 節封面頁

`sectionCover(n, name, oneLine)`。沿用標題頁的版型，只換文字：

| 元素 | 座標 | 樣式 |
|---|---|---|
| `SECTION n` | x=M, y=2.16 | Calibri 16pt，`ACCENT`，`charSpacing: 1.2` |
| 節名稱 | x=M, y=2.72 h=0.95 | **Cambria 44pt bold**，`INK` |
| 一句話說明 | x=M, y=3.72 h=0.62 | Calibri 20pt，`MUTED` |
| 短橫線 | x=M, y=4.66 w=1.1 | `ACCENT`，2pt |

- 🔑 **說明句與 Outline 頁那一列的說明刻意用同一句**，讓聽眾看到封面時知道「這就是目錄上那一節」。
- 封面頁**有頁碼**（標題頁沒有）。
- ⚠️ 插入節封面會讓後面每一節的頁碼位移，**Outline 的 `pp. x–y` 要重算**。

### E4d. 副標的句型（Adam 2026-08-19 訂）

副標**只介紹這一頁在做什麼**，不放結論、不放賣點。**結構是「一個事實 → 所以這頁講／量什麼」。**

✅ 範本：`bmv2 emits no sFlow of its own — so the proxy manufactures it, byte-compatible with what OVS sends`

❌ 反例（都已改掉）：
- `A twin that cannot answer "what happens if I turn this one off" is not answering the question it exists for` — 是主張不是介紹
- `The count is the least interesting number on this page` — 機巧但沒說這頁有什麼

⚠️ **副標抓 ≤ 130 字元**（實測 141 字元一行、143 字元兩行，兩行會壓到標題底下那條細線）。

### E5. 已知的呈現地雷（實際踩過，32 條）

**版面**

1. **條列間距抓太緊**，兩行以上的說明會撞到下一段標題——`listItem` 間距 **1.24" 以上**並實際渲染確認。
2. **`listItem` 每段內文超過 2 行**（間距 1.10–1.12 時）就會撞到下一段標題。
   要嘛縮字數，要嘛把間距開到 1.42 以上並減少段數。
3. **左欄條列寬度超過右欄起點**——文字會蓋到右欄。
   🔑 **用式子倒推，不要抄別頁**：`左欄內文最大寬 = 右欄起點 − 左邊界 − 0.3`。
   （這條犯過**三次**，所以寫成可計算的形式。）
4. **頁標題超過約 45 字元**會換兩行並壓到副標。長話短說，細節放副標。
5. **副標超過約 140 字元**會換兩行、壓到標題底下那條細線。抓 ≤ 130。
6. **表格底部與其下第一個 `listItem` 至少留 0.12"。**
   表格高度 = `rowH` 陣列總和 ＋ 起始 y，算出來再放，憑感覺一定會壓到編號。
7. **頁底的 `Measured at <commit>` 腳註放 y=6.96、寬 `CW − 0.75`。**
   放 6.84 會被上面兩行內文追上，寬度不減會蓋到頁碼。
8. **垂直流程圖方框太高**——五格 × 0.66" ＋ 四個 0.34" 箭頭就會把腳註推出版面。
   五格以上用 0.60" / 0.28"。
9. **一頁塞四個 `defect()` 會爆版。** 可用高度只夠三個（間距 1.5–1.62"）。
   第四個放右欄，用 `ACCENT` 細條 ＋ 標題 ＋ 一段整合的敘述。
10. **表格右側多欄擠在同一個文字框裡會換行錯位**——每個數字欄各自一個右對齊文字框。
11. **逐檔清單一次列太多**，左欄長度爆出版面撞到腳註——每欄上限約 20 列，其餘摺成一行摘要。
12. **右欄 `marginNote` 的第五個參數是色條高度，不是文字高度。**
    文字短、條長會出現一截空的強調色條。加減文字之後條高要跟著調：約 `0.3 + 行數 × 0.19`。
13. **在兩欄頁的左欄加句子，要先看它下面還有沒有東西。**
    8/20 的 Page 26 在主句加一句就把下面的小標壓掉了——**該句改放右欄註記裡**，語意也對。
14. **流程圖的分支標籤預設高度 0.16"，在 0.12" 的箭頭間隙裡會被下面的框切到。** 改 0.13。

**顏色與字**

15. **淡灰字（`A6A6A6` 以下）在投影時看不見。**
16. **封面不要深色底、不要堆小字**（commit 數、branch 名）——白底，小字移除。

**圖**

17. **架構圖方向弄反**（controller 在上）——**apps 一定在最上面**。
18. **架構圖的 sFlow 起點畫錯**——P4 那條必須從 **proxy** 出來，不是從 bmv2 雲。
    bmv2 不發 sFlow，畫成從雲出來就把整頁的主張講反了。
19. **架構圖的控制器框離 kernel 太近**——留 0.36" 才放得下箭頭旁的標籤。
20. **整頁圖不要再加頁標題。** 圖若自帶標題與副標，投影片再加一個會出現兩層標題。
    圖頁只放左上角節次標記與右下角頁碼。
21. **圖重畫之後尺寸會變，而長寬比是寫死在呼叫端的——比例錯了不會報錯，只會變形。**
    換圖後先 `identify -format "%f %wx%h\n" figures/*.png` 對一次。
22. **`ar > 2.5` 的圖在 16:9 上會寬度不足**，`figurePage` 會自動進寬圖模式
    （邊界 0.4"、垂直留白上 34% 下 66%）。

**數字與交叉引用**

23. **同一個數字用兩支腳本各算一次**——一定會兜不攏。跨頁共用的數字要有唯一計算來源。
24. **直接用 `git diff --shortstat` 報行數**——含註解與空行，會虛胖約 40%。
25. **在 repo 還在動的時候量數字**——前後兩分鐘量出 313 檔／314 檔兩個結果。**產檔前最後再量一次。**
26. **刪頁之後，別頁的「page N」交叉引用會指向不存在的頁。**
    **刪頁的同一次就要 `grep -n "page [0-9]"` 一遍。**

27. 🟣 **`listItem` 的內文框沒有指定 valign，渲染器會把它置中在 0.9" 的框裡。**
    兩行內文因此**往下沉到撞上下一段的標題**——看起來像間距不夠，其實是對齊問題。
    **已在 `deck_style.js` 修掉**（`valign: "top"`、h 0.9 → 0.86）。
    🔑 **一般性教訓：版面出問題時先確認是「盒子太小」還是「東西在盒子裡的位置不對」。**
    今天先把間距從 1.02 加到 1.28、又縮短文字，都沒解決；改一個 valign 就全部好了，
    而且六頁一起好。**先量框、再改字。**
28. 🟣 **整頁圖之外的頁，底部腳註只有 `y=6.96` 一個位置可用。**
    表格＋三條列的頁一旦最後一條是兩行內文，腳註就得讓位——
    這時把它併進右欄最後一則 `marginNote`，不要硬塞。
29. 🟣 **多列版型裡的次要行（副標、判準）要釘在固定 offset，不要接在標題下面。**
    p.4 五條承諾裡只有一條標題折兩行；讓判準行跟著標題浮動，那一條會把整欄弄得參差，
    而其他四條完全沒問題。**釘死 y+0.50 之後整欄對齊，折行那條也不會撞。**
    🔑 **同一件事的另一面**：欄位數是內容決定的，不是版面決定的。
    三欄放三條剛好，放五條就只能縮字級——但那頁的閱讀順序是「問題→判準→結論」，
    那是一**列**，不是一欄。**版型跟著閱讀順序走，不要跟著上一版走。**
30. 🟣 **每欄項目數增加時，pitch 與字級要一起算，不能只加項目。**
    p.33 settled 從五條加到六條，pitch 0.86 → 0.70，內文 11 → 10.5pt——
    否則兩行內文（0.44"）會超過 pitch 而撞到下一個標題。**先算 head + body ≤ pitch 再排。**
31. 🟣 **`keyLine()`（頁底那行強調句）會吃掉 0.34"，最後一列必須在 y=6.46 前結束。**
    這條踩了兩次：E3a 格式的兩頁都是最後一列壓在強調句上。
    **判準**：帶 `keyLine` 的頁，列數 × pitch 起算點必須讓末列 `y + h ≤ 6.46`。
    另一個解法更好——**那行如果是出處，就併進 `footNote()`**，出處本來就是頁底註的用途。
32. 🔴 **圖與內文同頁時，圖內字級要跟頁面字級一起看。**
    E3a 把內文放大到 16pt 之後，原本併排的 `page_failover-budget.png`（兩個 panel、
    5" 寬）變成**整頁最小的字**——版面沒錯，是圖選錯了。
    **判準：併排的圖只能是「一兩根長條、數字很大」那種**；多 panel 或密座標軸的圖
    仍然一圖一頁。當時的解法是換成 `page_ovs-before-after.png`，
    而拆解的數字本來就已經寫在 `RESULT` 那一列——**圖只需要扛住讀者會記住的那一個數字。**

### E6. 與 Adam 協作的既定慣例

- **對話用中文，投影片用英文。**
- **樣本先行**：大改動先做 3–5 頁樣本看風格，確認後才展開全部頁數。
- **要改投影片，先改這份 template**，再依 template 重生投影片。**template 是唯一事實來源。**
- **正本在 `~/Desktop/NDTwin slide material 827/`**，不是 outputs。Adam 會直接編輯它，
  **動工前先讀最新版**。
- Adam 在對話中口頭給的偏好與逐頁修改，**要即時寫回這份文件**，不要只留在對話裡。
- **產出後一定要渲染成圖逐頁檢查**；程式跑得過不代表版面沒問題。
- **要單獨的圖就給單獨的檔**，不要順手改 deck；反之亦然。先問清楚是哪一種。

---

## F. 可重用的資產

### 這個資料夾

| 路徑 | 內容 |
|---|---|
| `generator/deck_style.js` | **本次的樣式庫**。色票、版面常數、23 個 helper，無內容。已實測可 `require`。 |
| `generator/count_lines.py` | 增刪行數的唯一計算來源。跑之前把 `REPO` / `OUT` 兩個路徑改成本機的。 |
| `NDTwin_Arch_merged.pptx` / `.pdf` / `figures/NDTwin_Arch_merged.png` | 🆕 **三個資料面合併版的架構圖**（官網用），見下方 F1 |
| `generator/build_arch_merged.js` | 上面那張的產生器。含一份 `archTop()` 的副本，所以它可以獨立跑。 |
| `figures/` | 量測圖與自畫的圖 |

### F1. 🆕 官網用的合併架構圖（2026-08-21）

**`NDTwin_Arch_merged.pptx`** ——把原始架構圖與 P4 架構圖合成一張，**三個資料面並排**：
`Emulated Network (Mininet)` / `Physical Network` / `Emulated Network (Mininet, bmv2)`。

🔴 **硬體交換機沒有被拿掉**，這是 Adam 明確要求的——P4 那張當初省略 Physical Network 是
**簡報用的取捨**（怕 Ryu 的線跨過 bmv2 雲），對官網不成立。

**與簡報版的三個差異，都是刻意的**：
1. **全黑，沒有 `ACCENT`、沒有 `new` 標籤。** 官網要呈現的是**框架現在長什麼樣**，不是
   「這一輪加了什麼」。用強調色標 P4 那半在簡報上是對的（那頁的訊息就是對比），
   在官網上會變成「這個子系統比較重要」的誤讀。
2. **雲從 4.05" × 2 縮成 2.80" × 3**，間距 0.45"。這正是 8/20 版 E4a 早就預告過的
   ——「要再加第三條資料面時，三朵都得縮到 ~3.0"」。交換機框跟著縮到 0.66"，字級 8pt。
3. **網路名稱移到雲的下方置中。** 三朵雲排滿之後，原本放在左右兩側的名稱沒有位置了。

**接線（三條路徑各自不同，這是這張圖的重點）**：

| 資料面 | 控制面 | 南向協定 | 遙測 |
|---|---|---|---|
| Open vSwitch | SDN controller (Ryu) | OpenFlow | 交換機**自己**發 sFlow，直達 kernel |
| Hardware switch | SDN controller (Ryu) | OpenFlow | 同上 |
| bmv2 switch | **P4 proxy agent** | **P4Runtime** | 🔑 **proxy 合成 sFlow**，從 proxy 出來不是從雲出來 |

🔴 **sFlow 那三條線的起點畫錯就把整張圖講反了**（E5 第 18 條）：
OVS 與 Hardware 那兩條**從雲往上**，bmv2 那條**從 proxy 框往上**。bmv2 不發 sFlow。
右下角那則註記就是在講這件事，**不要刪**。

**版面關鍵座標（2026-08-21 第三版，全部由 `CX = 4.95` 推導，不要寫死絕對值）**：

```
CX = 4.95                            // kernel 框的中心，也是中間那朵雲的中心
KERNEL_TOP 1.78   KERNEL_BOT 4.20    // 原本是 1.99..4.92
CTRL_Y 4.72  CTRL_H 0.46  CTRL_W 2.55  CTRL_OFF 1.625
CLOUD_Y 5.66 CLOUD_H 1.40  CLOUD_W 2.80  CLOUD_OFF 3.25
分界線 y = 5.52        網路名稱 y = 7.14
```

| 元素 | 左 | 中 | 右 |
|---|---|---|---|
| 雲中心 | `CX − 3.25` | **`CX`** | `CX + 3.25` |
| 控制器中心 | `CX − 1.625` | — | `CX + 1.625` |
| sFlow 箭頭 | `CX − 3.85` | **`CX`** | `CX + 3.85` |
| 南向箭頭 | `CX − 2.55` | `CX − 0.50` | `CX + 2.55` |

🔑 **三對都是 `CX ±` 同一個數，所以改任何一個都不會破壞對稱。**
**唯一沒有鏡像的是 `CX − 0.50`（Ryu 的第二隻腳下到 Physical Network）**——那是資訊：
硬體交換機跟 OVS 一樣是 Ryu 用 OpenFlow 驅動的。

**v2 → v3 的兩次改動（Adam 逐項）**：
1. **bmv2 的 sFlow 改成跟另外兩條一樣，從雲直接上到 kernel。**
   原本畫成從 proxy 出來（因為實際上是 proxy 合成的），但那讓左右結構不一樣。
   🔑 **裁定：那是「怎麼做」的細節，不是「誰跟誰講話」**，所以改由 `(synthesised)`
   這個字承擔，右下角那則長註記也一併刪掉。
2. **兩邊的 REST 標籤都只寫 `REST`。** 右邊原本是 `Ryu-compatible REST`，
   一來跟 `sFlow (synthesised)` 撞在一起，二來左右不等長會破壞對稱。
   🔑 **拿掉之後反而更強**——proxy 就坐在 Ryu 坐的位置、kernel 用同樣的方式接它，
   圖本身就把「它模仿 Ryu」說完了。**「Ryu-compatible」留給官網的文字說明。**
3. **上半部壓縮，空間讓給雲**（Adam：「下面太擁擠」）。
   apps 框 0.84 → 0.70、kernel 框 2.93 → 2.42（三列由 0.55/0.40/0.55 統一成 0.48、
   列距 0.85 → 0.70）、tools 六格由 0.50/0.42 統一成 0.40、列距 0.44。
   **省下的 0.7" 全部給雲**：`CLOUD_H` 1.02 → **1.40**，交換機框 0.66×0.42 → **0.76×0.50**、
   字級 8 → **9pt**。
   🔑 **會這樣壓是因為上半部全是「兩行字的方框」，垂直方向本來就有餘裕**；
   雲裡面的東西才是讀者真的在看的。

**輸出**：`.pptx`（可編輯）、`.pdf`（向量，網頁與印刷都用這個）、
`.png` 300 dpi = **4000 × 2250**（網頁直接嵌用這個）。

### 🟠 F2. 圖表瘦身（2026-08-26）

Adam：**教授不喜歡看文字，報告時間與版面也不允許。** 問的是「能不能直接把圖上的字塗掉」。

🔑 **答案是不用塗，也不用找當初畫的人重畫——重跑產生器就好。**
繪圖腳本都在 repo 裡，raw data 也 commit 了，matplotlib 這台機器有。
`generator/slim_figures.py` 做三件事，然後跑一份**副本**（原始腳本一個字都沒動）：

1. **刪掉圖層級的說明段落**。判準不是座標也不是字串，是 **`weight="bold"`**——
   三支腳本裡標題都是粗體、說明段都不是，所以這個判準不會因為改字而失效。
2. **縮短標題**。因為原始碼把長字串折行、其中一個還是 f-string，所以是逐條列出
   **原始碼片段**去換，不是去比對算出來的句子。
3. **把空出來的高度還給圖**（`rect` 上緣 0.86 → 0.915）。

⚠️ **panel 的 `pad` 刻意不動。** 每個 panel 標題底下那一塊是**數字不是廢話**，所以留著；
而標題需要那個 pad 才跨得過它。**試過把 pad 縮小、結果標題直接壓在字上**——
這是這一輪唯一踩到的坑。

📁 **原始（有完整文字的）圖備份在 `figures/_full-text-originals/`**，九張。
要回頭比對或改回去都在那裡。

**指令**：`python3 generator/slim_figures.py <repo> figures/`
⚠️ 跑之前確認 `REPO` 指到本機的 `NDTwin-Kernel`。

### 上一個資料夾（`~/Desktop/NDTwin Slide material/`）

| 路徑 | 什麼時候會用到 |
|---|---|
| `NDTwin-slide-template.md` | 8/20 的完整逐頁大綱。**要重用某一頁的內容時來這裡查。** |
| `generator/build_deck.js` | 44 頁的完整實作。**`archTop()`（兩張架構圖的共用上半部）只在這裡。** |
| `generator/build_flow_diagrams.js` | Liveness／Failover 流程圖 |
| `generator/build_power_diagram.js` | Phase 7 電源流程圖 |
| `generator/build_module_diagram.js` | 八個 proxy 模組的關係圖 |
| `figures/` | 8 張量測圖 ＋ 4 張自畫的圖（proxy_modules、liveness_flow、failover_flow、phase7_power_flow） |
| `NDTwin_deck.pptx` / `.pdf` | 8/20 的成品，44 頁 |
| `2026-08-19_demo-recording-runbook.md` | demo 錄製流程（含每段的畫面配置與會當場發作的地雷） |

### 環境備忘

- **這台機器沒有 Node**，簡報由 cowork session 產生。
- 繪圖用的 matplotlib venv 在 `~/Desktop/NDTwin Slide material/.plotvenv`
  ——⚠️ **不要裝進 `p4_proxy/venv`**，那支是 proxy 在用的。
- 量測圖的產生器在 repo 裡：`doc/audit/2026-08-19_p4-sflow-accuracy/plot_figures.py`。
  **每張圖都是從已 commit 的原始資料重新算出來的，不是從報告的表格抄的**，
  所以圖上的數字與報告裡的數字不可能漂移。
