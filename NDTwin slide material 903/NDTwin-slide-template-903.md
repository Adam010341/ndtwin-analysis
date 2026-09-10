# NDTwin 進度報告簡報 — 2026-09-03 版・資訊模板

**v0.6（2026-09-01 深夜，Adam 四條口頭裁定：**廢話再砍、background 去掉、
manual 改成大數字＋現場看網站、字級再上調**）＝ §C0-v2（23 頁）＋ §E-delta-3（字級 v2）。
⚠️ **v0.6 的 pptx 尚未產出**——產檔當下 sandbox 因本機硬碟滿無法啟動，
原始碼與模板已就緒，空間清出後跑 `node generator/build_deck_903.js`，
**並照 E3 最後一條逐頁看過**（這一版的幾何沒有量過）。**

v0.5（2026-09-01。v0.1 骨架＝`8/29 auditor` 起草；v0.2＝reviewer 線依 Adam 指示
補文獻回顧＋解凍改寫研究價值頁；v0.3＝加 fig5 報告矩陣、fig6 十二數一軸；
v0.4＝「教授喜歡圖」再加兩張——fig7 把 p.20 的 aggregate 表格化成圖、
fig8「已知≠報告規範」圖解收尾 §2；**v0.5＝09-01 兩條線的輪次結果落檔**——E 輪
（B1③、p.29、§G5，另一條線已落）＋ **§B／§C（reviewer 線：B2 兩塊、p.19、p.20、§C'、§D、
§F、新開 §G6／§G7、p.30 列 1 的備答；順手改正標題的「31 頁」＝表已 32 列）**；
**v0.6＝09-01 夜 Adam 指示補「實驗方法」頁**——新開 §C''、插入新 p.15、原 p.15–32 全數 +1
⇒ **33 頁**，§C0 標為存證不動）。
⚠️ **上面 v0.4／v0.5 那幾句裡的頁碼是當時的**（fig7 那時是 p.20＝現 p.21、§G5 那時是
p.29＝現 p.30）——changelog 不回頭改，**要頁碼就看 §C 表**。** 照 E6 慣例：**本檔是唯一事實來源，
Adam 直接編輯**；產檔由 cowork session 跑 JS 產生器（本機無 Node）。動工產檔前先讀最新版。

規約沿用：**§A（敘事）與 §E（視覺）全文沿用 827 版**
（`../NDTwin slide material 827/NDTwin-slide-template-827.md`），本檔只寫 903 特有內容與 delta。
827 的 E5 三十條地雷照踩不誤，副標句型照 E4d（一個事實 → 這頁講什麼，≤130 字元）。

三條規則因為這輪特別容易踩，inline 重申：

- **A2b：每個實測數字旁標 commit**。本檔已照做；新增數字時照做。
- **兩級證據不可混寫**（本輪手冊線的核心紀律）：「親自執行」與「讀過未執行」在頁面上
  也要分得開——desk-check 來的東西不可以寫得像跑過。
- 🏁 **投稿計畫頁凍結已解除、整頁換掉（現 p.31，規格 §C'）**：LINE 已發（08-30 夜）、教授已回
  ——「量測結果可以報告；但這個問題早已被世人得知、缺乏創新性、沒有研究價值（投稿不會被
  接受）；星期四先報告和展示技術文件」。Adam 裁定：報告時**簡單提一次**研究價值（請教式、一頁）。
  🔴 頁面紅線：**任何場地名（CoNEXT/PAM/EuroP4）不上台面**、不提外部指導選項、
  不掏排版英文 poster——slide 只呈現數據與文獻回顧。**🔴 09-01 覆裁（Adam）：「成品稿不揭露」改為「教授鬆口才拿兩頁版」**——
  兩頁版＝`../paper/abstract/abstract-2page.pdf`（2 頁含 refs），六頁版仍不掏；講法＝「已寫過一輪、沒投是想先讓老師看過、
  現在要做的是取捨不是產出」；順序＝揭露稿子→affiliation 那格→12/7 Utrecht 與註冊費→才提會議與 9/6。

---

## B. 8/27 → 9/03 的起點與增量

### B1. 8/27 停在哪（p.32「Planned for the next report」的兌現狀況）

| 8/27 承諾（p.32 原文，已從 pptx 抽出核對） | 判準（原文） | 9/03 的答案 |
|---|---|---|
| ① Take the boot-ring result from suggestive to conclusive | arms 加到 0/6–0/8＋fixed build 重測開機成功率 | **沒跑**（帳面既有「環已結案」是先前結論；加臂升級這兩週未動）——原樣進 p.32 或明講降序 |
| ② Finish the third question on its own terms（L0–L4 全過 fast build） | the whole L0–L4 suite passes on the fast build | **IN PART**：§6.7 把 fast build 的安裝旅程與 provenance 驗完（7 PASS、byte-identical）；**功能套件對 fast binary＝§6.7 note-3，排明日 fabric 半邊**——9/03 前可能轉 ANSWERED，等結果 |
| ③ Ask whether batching moves the ceiling（1/8 格、開關 batching） | 1-in-8 cell 的 loss 動或不動 | 🏁 **跑了，而判準沒撐過去**（09-01 更新，取代原本的「沒跑」）：E 輪 08-31 23:26–09-01 07:25 跑滿 **72 格**（八階 × 四臂 × n=3）。判準的答案不是天花板——`SATURATED` **0/72** ⇒ 四臂全右截斷於 ≥1/1 ⇒ **不可分辨**；而 batching 的**主效應在本輪設計下不可估**（與 leg／時段完全混疊，F-28）。真正問出來的是**判準量錯了量** ⇒ 🖼 `page_ceiling-not-read-out.png`＋**§G5 三條 REQUIRED**（缺一就會被讀成「天花板是 1/1」） |

（p.32 還有一句版式約定值得沿用：「Same shape as the 20 August page, so the next report can be
checked against it the way this one was」——p.32 照做。）

### B2. 這兩週實際發生的（每條都有正本，數字帶 commit）

1. **bmv2 效能研究定稿**：`doc/2026-08-29_bmv2-performance-study.md`（最新修訂 `b2cd6b5`＝
   OvS 歸因更正落稿，取代本檔 v0.1 寫的 `c37abea`）。
   三張工單收案：①build 加速 **三跳 12×、隔離單跳 8.0×**（量化區間 5.14–12.0）；
   ②**pps 只變 1.25× 而 bit rate 變 16×**——用 Mbps 報容量不講封包大小＝16 倍歧義；
   ③**容量是流數的函數**：bmv2 每流 160→1–2 Mbit（n=1→16）且 **aggregate 自塌 ~10×**，
   OvS 同梯對照 aggregate 撐住（0.72–0.96 G 均分）。
   ⚠️ OvS 臂全程跑在 as-configured **1G-shaped** fabric（htb），bmv2 臂 unshaped——
   **不對稱方向保守**；頁面措辭照 FINDINGS 紅線，禁用「unshaped／shaping removed」。

   🔴 **09-01 §B 給 ③ 加了一個限定詞：塌陷是 UDP 特有的**（`7f58cef4`，reviewer 線）。
   同一顆交換機、同一條 h1→h65 五跳路徑，把負載換成 TCP 之後 `T(16)/T(1)`＝
   **1.222／1.108（均 1.165）** ⇒ 落在預註冊三支裡的「**UDP 特有**（≥0.9）」，
   離「同型」那一支（≤0.5）差一個數量級，不是邊界案例。
   **先跑先印**的 loopback 對照（路徑上沒有交換機）讀 **3.854** ⇒ 宿主自己不塌，
   所以經 fabric 量到的塌陷可歸因於 fabric。正本＝`doc/audit/2026-08-31_completeness-experiments/
   B-tcp-control/FINDINGS.md`（引數字前先讀同目錄 `PROVENANCE-and-deviations.md`）。
   ⚠️ 兩件事**不准做**，PREREG §B.2 在資料之前就凍了：**不得**把 TCP 的 269 Mbit 與 ③ 的
   24 Mbit 並排（TCP goodput 與本研究的「最高乾淨速率」不是同一個量——TCP 對丟包有壅塞
   反應，`clean (loss ≤0.5%)` 在 TCP 上沒有意義），**不得**引 Chen 組作旁證。
   ⇒ **凡是講 ③ 的頁面都要帶「UDP」——是 p.20 與 p.21 兩頁，不是一頁**
   （兩張都是整頁圖，圖上都沒有這個詞；p.20 見 §G7、p.21 見 §G6，兩者共用同一條 REQUIRED）。

   🆕 **08-31 §C 給 ① 加了適用範圍，也指出了比值的哪一半在動**（`9601a010`＋`cfe07a92`）。
   把 P4 程式從我們自己那支（`ndtwin_switch.json`，508 行、10 處 clone、每包取樣）換成
   tutorial solution（`firewall.json`，284 行）重跑 A／D 兩臂：R 從 **(3.27, 7.71)** 變成
   **(2.25, 4.91)**，**兩區間相交** ⇒ 註冊判定＝「**程式無關**」，① 的適用範圍擴大到兩支程式。
   🔑 **相交的原因比判定本身值得講**：差異**全部在分母**——stock 臂換程式差 **1.57×**
   （70→110），fast 臂**幾乎不動**（同 offered 下 recv 差 0.1–4.4%）。
   ⇒ 可主張的版本是「**在 fast build 上 P4 程式已經不是瓶頸，在 stock build 上它還是**」。
   🔴 **收緊（§E 之後）**：這句只能講到「在 20 Mbit 解析度、±1 階重複性下兩支程式的 fast 臂
   **分不出來**」，**不可**講成「fast build 對 P4 程式不敏感」——「分不出來」大部分是解析度的
   陳述，不是等價的陳述。
   **文獻普查（同檔 §1 spread 表＋§2-1 統計段；p.23–26 素材）**：18 篇 corpus、量 bmv2
   **12 篇**（其中報吞吐 **10 篇**，另 2 篇僅量 latency/delay）、自陳吞吐 ~0.57 Mbps–
   ~1.4 Gbps＝**~2,500×**；build flags **0/12**、build 對照實驗 **0/12**、變體載明 **3/12**
   （全出自同一實驗室譜系；以獨立工作計 2/11）、版本載明 1/12、對 bmv2 的封包大小掃描
   0/12、固定拓樸流數自變數 0/12、多流帶對照平面 0/12。
   🔴 否定句主詞一律「**這 18 篇**」（study §5-4 檢索邊界），不寫成「文獻」。
2. **手冊驗證線（教授上次點名的）**：正本＝`doc/2026-08-30_manual-verification-report.md`
   （`798f9f5`＋`8775675`）。安裝手冊 §1–§6.6 乾淨室兩輪、整機 T-4 兩臂、DM API 頁 T-6、
   桌面核對 28 條；找到的手冊缺陷（M-1〜M-5）與程式缺陷（P-1、鎖端點三族）全修或已裁修。
   08-30 晚 Adam 升標：**測到可公開等級**（暫不公開）——§6.7／NTG／128-host／WebGUI 在途。
3. **F-5 機制指認**（T-4 FINDING-03，`569f976`）：kernel 把「已排隊未編程」的請求當流表列
   服務出去、僅 t=0 可見；08-18 的「no phantom, ever」是取樣格第一點在事件之後造成的假陰性。
4. **鎖端點三部曲修好**：acquire（`dff87f9`）→ release/renew（`db02d45`，635/635、
   mutation A–D 紅→綠、auditor 親驗）；P-1 雙 proxy 搶寫（`e29424e`）。
5. **投稿線現況（凍結已解除，見上）**：EuroP4 9/1 放生；LINE 已發、教授裁「缺乏創新性、
   沒有研究價值」＋週四先報技術文件；Adam 裁報告時**簡單提一次**（p.31、§C' 規格）。
   場地與後續選項一律不上台面。
6. **有流量整機輪**已預註冊（`doc/audit/2026-08-30_live-traffic-round/PREREG.md`，`5cbd672`），
   9/03 前會跑完——結果落 p.29 與 p.13。

### B3. 產檔前一定要等的結果（🔲＝落點）

| 在跑的 | 預計 | 落到哪頁 |
|---|---|---|
| §6.7 fast build（VM 過夜）＋ NSR／SimPlatform／NTG 三頁 | 08-31 晨 | p.7 覆蓋地圖＋p.13 |
| T-8／T-10 儀器修復（agent） | 08-31 | p.13（一句話）＋p.29 前置 |
| 有流量輪 TR-1〜TR-6（含 128-host 例子） | 08-31–09-01 | p.29、p.7、p.9 |
| website 修復 push（等 Adam 給權限） | — | p.8 註記「已修待上線」 |

---

### 🔴 C0-v2. **23 頁（Adam 2026-09-01 口頭，四條）——這是現行的頁序**

> **Adam 看完 32 頁版之後的四條**：①廢話還是太多　②background 去掉
> ③**manual 主要是要直接給教授看 website，用幾個大字講重點就好**　④字太小。
> ⇒ **32 → 23 頁**，產生器 `generator/build_deck_903.js` v2。
>
> ✅ **已產出並逐頁檢查完畢（09-01）**：`NDTwin_deck_903.pptx`／`.pdf`，23 頁，
> 60 dpi 逐頁看過。字級 v2 只撞了一處，已修：
> **p.21 五列 pitch 0.66 會把最後一列壓在 `keyLine` 上 → 改 3.24／0.62。**
> （產檔當下 sandbox 曾因本機硬碟滿無法啟動——`~/.config/Claude/vm_bundles/claudevm.bundle`
> 是 12 G 的 VM 映像，跟 deck 無關；🔴 **那顆 bundle 不可刪，刪了要重抓 12 G**。）
>
> **①②③ 是同一刀的三個切面：砍掉的是頁，不是句子。**
> 一頁如果需要一句話來解釋它為什麼在，那句話就是廢話——所以整頁拿掉，而不是把它縮短。
>
> | 動作 | 原 32 頁的頁 | 理由 |
> |---|---|---|
> | **刪** | p.3 Background | Adam 明示。回訪的讀者需要的定位是承諾表，不是系統介紹 |
> | **併成一頁大字** | p.7 覆蓋地圖、p.9 Installed and it runs、p.12 API surface | ③：這三頁在講「網站上看得到的東西」，而教授要看的是網站本身 |
> | **併成一頁** | p.8 Found then fixed、p.10 FINDING-01、p.11 FINDING-03、p.13 what remains | 四頁講同一件事＝跑過才會知道的缺陷。剩下的進 p.23 open 欄 |
> | **刪** | p.16 `page_Q_assumed-denominator`、p.17 `page_Q_gate-after-fix` | 模板自己的可略 ④⑤ |
> | **刪** | p.22 普查記分板以外的重複、p.28 traffic round 的表格版 | 表格降成五條列 |
>
> **新的 23 頁**：
>
> | # | 頁 | 版型 |
> |---|---|---|
> | 1–2 | Title／Outline（三節） | — |
> | 3 | Where we left off（四條，manual 排第一） | 四列＋判詞 |
> | 4 | ▎§1 The manual | 節封面 |
> | 5 | 🔑 **It installs, and it runs** | **六個大數字（68pt）** |
> | 6 | What running it found | 五列 |
> | 7 | ▎§2 節封面 | — |
> | **8** | 🆕 **How we measured**（關卡帶，規格＝C''-產檔紀錄 v2） | 五柱＋三線 |
> | **9** | 🆕 **Every outcome had a meaning first**（註冊結果空間，規格＝C'''） | 三條數線 |
> | 10–14 | 🖼 M cost-benefit／bandwidth-ceiling／fig2／fig7／fig1 | 整頁圖＋REQUIRED band |
> | 15 | 18 papers, and what they report | 表＋THE GAP 一列 |
> | 16–19 | 🖼 fig5／fig6／fig4／fig8 | 整頁圖＋band |
> | 20 | ▎§3 節封面 | — |
> | 21 | 🖼 `page_ceiling-not-read-out` | 整頁圖＋三條 REQUIRED |
> | 22 | The traffic round | 五列 |
> | 23 | Worth writing up? | 問句＋五列 |
> | 24 | Planned for the next report | 三欄＋判準 |
> | 25 | Where it stands | 左右欄 |
>
> ⚠️ **p.8＋p.9 插入之後全份是 25 頁**（p.8 取兩頁版則 26 頁）。
> 目前 `NDTwin_deck_903.pptx` **仍是 23 頁**——兩張新頁都是獨立檔案，下次重生整份 deck 時
> 把 `build_page_how_we_measured.js` 的 `bandPage()` 與 `build_page_outcome_bands.js`
> 併進 `build_deck_903.js` 的第 8、9 個位置，並同步 Outline 的 `pp.` 範圍。

### 🔴 C'''. p.9 **Every outcome had a meaning first**（09-01 深夜新增，Adam 指定）

> 產出 `NDTwin_p09_outcome-bands.pptx`；產生器 `generator/build_page_outcome_bands.js`。
> **一頁三條數線**（BUILD／SIZE／FLOWS，順序與 p.8 三條實驗線相同——**刻意的視覺押韻**）。
>
> **要傳達的一件事**：出手前把每個變數的結果空間切成幾段，每段預先寫好它代表什麼
> ⇒ **沒有「實驗失敗」這個選項，只有「落在哪一段」。三段都是結果。**
>
> 🔴 **三段等寬，而且是刻意的。** 依實際尺度畫，會讓「剛好命中的那一段」看起來像正確答案，
> 那正是這頁要反對的信念。**命中的那段不加勾、不加亮、不加粗框**——頁底註寫明等寬的理由。
> 每段的區間數值印在該段下方，所以等寬不等於藏數字。
>
> **兩列各自扛一個論點，其餘都是襯托**：
> - **BUILD**：R = 8.0 落在 H2，**但量化區間 (5.14, 12.0) 橫跨註冊切點 9**。
>   誤差橫條騎在切點上就是這一列的全部意義，旁註 `interval crosses the cut — a gap we disclose`。
> - **FLOWS**：形狀刻意不同——**一條註冊帶 95–150，實測 220.0 明顯在帶子外**，
>   `ABANDON RULE FIRED`，下方 `the curve stands, the intervals do not`。
>   🔴 **n=4／8／16 的區間不畫**：那些區間已隨判準發火作廢，畫了會誤導。
> - SIZE 的作用是把 **H3（mixed cost）畫得跟另外兩段一樣正式**——它是預先註冊的第三種結果，
>   不是「沒結論」。這是那一列唯一的論點。
>
> **與 p.8 的分工（不重複）**：p.8 說一個數字**過了哪些關**；p.9 說**不管結果怎麼出來，
> 它各自代表什麼**。p.8 的 `PREREGISTERED` 柱是承諾，p.9 是那個承諾的內容。兩頁數字不交叉。
>
> **刻意不上頁的**：第二台機器的區間 (3.27, 7.71)。它與 m1 相交是**複製**的主張，
> 而複製已經由 p.8 右端的 `registered replication` 承擔；在這裡加第二條橫條會讓 BUILD 那列
> 失去單一論點。被問到就口頭答。
>
> **數字全部回讀正本核對過**（不是照抄使用者訊息）：
> `2026-08-28_single-switch-build-ratio/PREREG.md:69–73`、
> `2026-08-28_packet-size-sweep/PREREG.md:79–90`、
> `2026-08-28_flow-count-capacity/PREREG.md:70–77`、放棄判準
> `…/HANDOFF-CONTEXT.md:65–67`（`48487ed`，資料之前）。
> 灰階已驗：等寬色塊、切點粗線、點線、誤差橫條去色後全部仍可辨。
>
> 一次幾何修正：三列原本各有「量測標籤」與「旁註」兩層，區間數值那一排把上層擠掉
> ⇒ 兩者改成**同一行、左右分置**（三列都撞過，一次修完）。
>
> 🔑 **p.5 是這一版唯一的新版型，而它是為了「不要在投影片上重做網站」而存在的。**
> 六個數字、68pt、每個底下一行說明，`keyLine` 只有一句 **`→ the manual itself, live`**
> ——那是**換到瀏覽器**的提示，不是結論。頁上沒有任何一句完整句子。
> **p.6 承擔網站看不到的那一半**：跑過才會知道的缺陷（手冊三條、程式兩條、
> FINDING-01 的假綠燈、FINDING-03 的幻影列）。**網站證明它能裝，p.6 證明我們真的跑過。**
>
> 🔴 **G3／G4 這一版不適用**——`page_Q_*` 兩張沒上台，REQUIRED 只在圖上台時才是義務。
> **那兩頁若補回來，band 要一起補回來**，逐字在 §G3／§G4。
> 其餘 **G1／G2／G5／G6／G7 五條全部落成 band**（p.8、p.9、p.19、p.11、p.10）。
>
> **兩件保留下來、看起來像廢話但不是的**：
> - p.13 的 `in our sample of 18` 與 p.21 的 `DESK CHECK` 標籤：兩者都是紅線
>   （E-delta-1 第 3、4 條），**不因為要變短而刪**。
> - p.3 第四列的 `NOT RUN`：承諾表的價值全在它敢標紅。

---

### C0（歷史）. **32 頁版**（2026-09-01 稍早產檔，已被 C0-v2 取代）

> 🔴 **這一節整節是存證，頁碼停在 09-01 19:51 那一版。09-01 夜之後它已經對不上了**——
> Adam 指示補「實驗方法」頁，插在 §2 節封面之後，**≥15 的頁碼一律 +1（見 §C）**。
> 本節**刻意不改**：改了它就從「當時產出了什麼」變成一份說謊的紀錄。
> ⇒ **下面的 §G↔頁 對帳表與可略順位都不可拿去產檔**（照它砍會砍錯頁：
> 「② p.17」現在是 p.18、「③ p.16」現在是 p.17）。產檔一律看 §C 表。
> 這一版 pptx／pdf 因此是**上一版**，方法頁進去之後要重產。
>
> 產生器 `generator/build_deck_903.js`（`require("./deck_style")`），全篇新文法（E-delta-1）。
> **頁碼與 §C 表逐列相同**，沒有跳頁、沒有加頁。逐頁 60 dpi 看過，零溢出、零撞行。
>
> **§F 的 §G 義務對帳（七節全部落地，這是產檔的驗收條件）**：
>
> | §G | 圖 | 落在 | 形式 |
> |---|---|---|---|
> | G1 | `page_M_cost-and-benefit` | p.15 | `COST PRE-REGISTERED`／`BENEFIT POST-HOC` 兩列 |
> | G2 | `page_bandwidth-ceiling` | p.18 | `THE FOUR SHORT BARS`／`WHAT 53.1 IS` 兩列 |
> | G3 | `page_Q_assumed-denominator` | p.16 | `THE EFFECT IS REAL`／`AND HONESTLY SMALL` 兩列 |
> | G4 | `page_Q_gate-after-fix` | p.17 | `WHAT IT PROVES`／`WHAT IT DOES NOT` 兩列 |
> | G5 | `page_ceiling-not-read-out` | p.29 | 三條 REQUIRED 三列（`lw: 3.30`，標籤才不折行） |
> | G6 | `fig7_aggregate_two_planes` | p.20 | `UDP, ON BOTH PLANES`／`SO THE CLAIM IS` 兩列 |
> | G7 | `fig2_perflow_monotone` | p.19 | `UDP`／`THE CONTROL` 兩列 |
>
> 🔑 **新文法解決了 §F 那個結構問題。** 舊文法的整頁圖沒有放字的地方，所以 REQUIRED 只能
> 進講稿——而講稿會被忘記。新的 `figPage()` 讓圖上方留標題、下方留一條 band，
> **REQUIRED 就是那條 band**，圖與防誤讀句同台是版型保證的，不是紀律保證的。
> 「一圖一頁、頁上不放字」這條 827 規則到此為止，理由寫在產生器檔頭。
>
> **四個產檔時的裁定，理由記在這裡**：
>
> 1. 🟠 **p.7「User Manual, main path」的措辭收緊。** 兩份正本對不上：
>    `COVERAGE.md`（08-28）寫 **OVS 三終端啟動「never executed」**，
>    `manual-verification-report`（08-30）寫**主流程頁（Terminals 1–3）✅ 跑過**。
>    後者較新且是彙整正本，但我不拿它去否定前者的逐項紀錄 ⇒ 頁面只寫**兩者都支持的那半**：
>    「the main flow page, run · traffic generation checked by content, not by exit code」。
>    🔴 **要講 OVS 三終端那條的話，先把兩份對帳**——這是頁面上唯一一處我主動降低了解析度。
> 2. 🟠 **p.13 的「in flight」拿掉了有流量輪。** §B3 寫它在跑、落 p.28——**它已經跑完**
>    （`RESULTS.md`，六臂六判定），所以它進「done」而不是「in flight」，
>    空出來的位置給 T-7b（release/renew 待合併）。
> 3. 🟠 **`fig5`–`fig8` 改用 PDF 重新點陣化。** 原 PNG 約 890 px 寬，在投影片寬度只有
>    80–100 dpi，新文法內文放大到 16pt 之後它們變成頁面上最糊的東西（E5 第 32 條的另一面）。
>    `figures/_hires/` ＝ 同目錄 **PDF** 的 `pdftoppm -r 500`，**同一份向量源、沒有重畫**，
>    所以數字不可能漂移。**先驗過 repo 的四張 PNG sha256 與本資料夾逐張相同**
>    （含 fig7 = `f7aeeede…`，09-01 的 UDP 版）⇒ PDF 與部署的 PNG 同代，不是舊批。
>    `fig1`–`fig4` 沒有 PDF，照原尺寸用。重建指令在 `figures/_hires/README.md`。
> 4. 🟠 **p.4 第一列（boot ring）寫 `NOT RUN` 而不是含糊帶過。**
>    §B1 ① 的原文是「沒跑」，判詞就照實給，`WARNC` 色，右欄寫「deliberately deprioritised ·
>    carried forward as written」——**承諾表的價值全在它敢標紅**。
>
> **可略順位不變**（① p.10、② p.17、③ p.16）；p.11／p.19／p.22–26 仍不可略。

## C. 逐頁大綱 v0.6（30 分鐘版，**33 頁**，節構照 827 三節制）

⚠️ **頁碼動過兩次，本表是唯一權威**：v0.4 是 31 頁；09-01 日間加 `page_ceiling-not-read-out`
成 32 頁；**09-01 夜 Adam 指示補「實驗方法」頁，插在 §2 節封面之後＝新 p.15，
原 p.15–32 一律 +1 ⇒ 33 列**。本檔其餘各節的頁碼**都已同步改過**（唯二例外見下）。
頁碼以本表列數為準，不寫死。

🔴 **兩處故意不改，不要「順手修正」**：
① **§C0 的頁碼是 09-01 產檔那一版（32 頁）的紀錄**——那是「當時產出了什麼」的存證，
改了它就變成一份說謊的紀錄。§C0 的 §G↔頁 對帳表**不可拿去產檔**，產檔看本表。
② **§B1 抬頭與表內的 `p.32` 是 8/27 那份 deck 的頁碼**，與本檔的頁數無關。

**節次標記**：`1 · THE MANUAL, PROVEN END TO END`／`2 · WHAT THE EXPERIMENTS SAY`／
`3 · ENGINEERING, AND WHAT'S NEXT`。§0 不放標記。頁碼產生器自動計數。
先兌現承諾再開新局：教授點名的手冊線＝§1 主菜（08-30 夜 LINE 教授明示
「先報告和展示你撰寫的技術文件」——§1 先行自此是教授指示，不只是排序判斷）。

| # | 頁 | 版型 | 可略 |
|---|---|---|---|
| 1 | Title | — | |
| 2 | Outline | — | |
| 3 | ▎§0 Background（雙資料面一句話＋這兩週的兩條線） | 兩欄 | |
| 4 | Where we left off（B1 表；①②③＋手冊線點名＝第 4 條 ANSWERED） | 列式 | |
| 5 | ▎§1 節封面 | — | |
| 6 | A clean room, and two grades of evidence | 流程＋兩列 | |
| 7 | The coverage map（Install／UM／DM × 狀態；⛔ not-coverable 誠實標） | 表格 | |
| 8 | Found, then fixed（M-1〜M-5／P-1／鎖三族 對照表；「已修待上線」註） | 表格 | |
| 9 | Installed, and it runs（12/12 pingall `faffdbe`；T_stack 16 s `89c1754`；energy 7/0 帳一致） | 三列 | |
| 10 | A check that could never fail（FINDING-01：模型比模型，fabric 沒被讀過） | 表＋兩註 | ② |
| 11 | The phantom was the sampling grid（FINDING-03：t=0；指紋三件；08-18 假陰性成因） | 三列＋兩註 | |
| 12 | The API surface: 29 documented, 12 not（T-6；29% 缺口；兩家族成套） | 圖或表 | |
| 13 | To publishable grade: what remains（🔲 B3 結果落此；not-coverable 清單） | 三欄 | |
| 14 | ▎§2 節封面 | — | |
| 15 | **How we measured**（09-01 夜新增。三個工單**共通**的量測紀律，六列；規格＝§C''。🔴 **不可略**——它是 p.16–27 每一個數字的授權書，也是「這個實驗做得完不完整」被問到時唯一能指的那一頁） | 列式 | |
| 16 | 🖼 `page_M_cost-and-benefit.png`（工單①：12× 收窄到單跳 8.0×） | 整頁圖 | |
| 17 | 🖼 `page_Q_assumed-denominator.png` | 整頁圖 | ④ |
| 18 | 🖼 `page_Q_gate-after-fix.png` | 整頁圖 | ⑤ |
| 19 | 🖼 `page_bandwidth-ceiling.png`（08-28 裁決：比值不上圖，非轉移性當標題。🔴 **08-30 乾淨圖裁決之後，圖上已經沒有 ECMP 短條標註、沒有 footer、沒有 stamp** ⇒ 防誤讀責任**整份落在 §G2 兩條 REQUIRED**，產檔時必須落成頁面文字或講稿。08-31 參數行左半補上 `32 TCP flows, 53.1 is one link's ECMP share`，兩邊的聚合單位才對稱） | 整頁圖 | |
| 20 | 🖼 `fig2_perflow_monotone.png`（容量是流數的函數；副標帶 as-configured 紅線）。🔴 **同一條 UDP 限定詞也管這頁**——y 軸 `per-flow highest clean rate` 是丟包讀出來的量（所以圖本身沒說謊），但頁面的宣稱句「容量是流數的函數」會被讀成協定通用，見 **§G7** | 整頁圖 | |
| 21 | 🖼 `fig7_aggregate_two_planes.png`（v0.4：原表格版換整頁圖——OvS 540/960/720 撐住配置帽 vs bmv2 160–240→32–16 自塌 ~10×；**08-30 當時已知的**紅線句已入圖）。🔴 **09-01 §B 的「UDP」限定詞不在圖上**——PNG 渲於 08-30 21:40，§B 判定 09-01 11:24，圖內註記逐字是 `collapses ≈10× — to 30× below the cap it does not even wear`，**全圖沒有任何協定字樣**（兩臂都是 `iperf3 -u`）⇒ 限定詞**必須落成頁面文字或講稿**，見 **§G6** | 整頁圖 | |
| 22 | 🖼 `fig1_unit_ambiguity.png`（工單②：同批資料 pps 1.25× vs bps 16×） | 整頁圖 | |
| 23 | The survey: 18 papers, and what they report（普查記分板表格，study §2-1：12 量 bmv2／10 報吞吐／build flags 0/12／變體 3/12 同譜系／版本 1/12／pkt-size 掃描 0/12／流數自變數 0/12） | 表格 | |
| 24 | 🖼 `fig5_reporting_matrix.png`（p.23 的視覺版：12 篇 × 9 報告面向；合計列＝study 統計段、腳本內建 assert 防漂移） | 整頁圖 | |
| 25 | 🖼 `fig6_twelve_numbers_one_axis.png`（十二個頭條數字上同一根 log 軸：4/12 上不了軸、1/12 是工作點、0/12 報 build） | 整頁圖 | |
| 26 | 🖼 `fig4_literature_spread.png`（自陳吞吐 ~0.57 Mbps–~1.4 Gbps＝~2,500× spread vs 我們同機 8×） | 整頁圖 | |
| 27 | 🖼 `fig8_known_but_never_reported.png`（v0.4：「已知≠報告規範」圖解——performance.md 原句＋引用它的兩篇仍不報 flags＋Zhang '21 對照組；§2 收尾＝對「早已被世人得知」的回答） | 整頁圖 | |
| 28 | ▎§3 節封面 | — | |
| 29 | The traffic round（TR-1〜6 結果 🔲；PREREG 先於儀器修復的紀律可講一句） | 表＋兩列 | |
| 30 | 🖼 `page_ceiling-not-read-out.png`（09-01 新增，Adam 裁排此位）：E 輪 72 格的答案**不是天花板**——`SATURATED` 0/72、四臂全右截斷 ⇒ 不可分辨。圖畫的是兩條線分道揚鑣：送出的流量塌 87–89%，而保真度判準讀 1.01。🔴 **防誤讀整份落在 §G5 三條 REQUIRED**，缺一就會被讀成「天花板是 1/1」 | 整頁圖 | |
| 31 | Worth writing up? — the case in one page（原投稿計畫頁整頁換掉；規格與紅線見 §C'） | 三列 | |
| 32 | Planned for the next report（含 8/27 ③ merge 那條原樣搬入 ⚠️ **③ 已於 09-01 有答案，見 §B1 與 p.30**——搬入時不要再寫「沒跑」） | 三欄＋判準 | |
| 33 | Where it stands（settled／open） | 左右欄 | |

**可略順位**：① p.10 FINDING-01　② p.18 gate-after-fix　③（再需要時砍 p.17）。
p.11（FINDING-03）與 p.20（容量）**不在可略清單**——前者是本輪最重的機制發現，
後者是效能研究的中心結果。🔴 **p.23–27（文獻回顧五頁）自 v0.2–v0.4 起也不可略**——
Adam 08-30 明指 9/03 要用（「量測數據與文獻回顧都放進 template」＋「再新增幾張圖」＋
「教授很喜歡圖片」），且 p.31 的論證以它們為前提。
🔴 **p.15（How we measured）也不可略**（v0.6 新增）——p.16–27 的每個數字都靠它授權，
而「你的實驗夠不夠完整」這個問題只有這一頁答得出來。砍它等於把 §2 變成一疊沒有方法的數字。

🔑 §1 內部結論先行：p.7 覆蓋地圖先把全景給完，p.8–13 支撐它。
🔑 p.11 排在 §1 中段而非附錄——它是「手冊線的整機測試自己挖出系統缺陷」的證據，
把驗證線從「照著做一遍」升級成「測出別人沒測到的」。

### C'. p.21／p.23–27／p.31 內容規格（v0.2–v0.4 新增與改寫各頁的落筆依據）

**p.23 普查記分板（表格版）**——數字全出自 study §2-1 統計段（`b2cd6b5`），照抄不重算：

| 量測面向 | 這 18 篇（量 bmv2 的 12 篇計） |
|---|---|
| 報吞吐數字 | 10/12（另 2 篇僅量 latency/delay） |
| build flags／optimisation level | **0/12** |
| build 對照實驗 | **0/12** |
| bmv2 變體載明 | **3/12**（全出自同一實驗室譜系；以獨立工作計 2/11） |
| 版本載明 | 1/12 |
| 對 bmv2 的封包大小掃描 | 0/12（pps 本位 1/12） |
| 固定拓樸流數當自變數／多流帶對照平面 | 0/12／0/12 |

副標方向（照 E4d ≤130 字元）：*The one variable we measured at 8x is the one none of
them state.* 🔴 措辭紅線照 study：否定句主詞＝「這 18 篇」、「in our sample」限定不可丟。

**p.24 fig5 報告矩陣（v0.3 新增）**：`fig5_reporting_matrix.png` 整頁——p.23 記分板的
視覺版（同一統計、逐篇逐格）；腳本逐欄 `assert` 合計＝study 統計段，數字漂移會 crash 而非
默默出圖。副標方向：*Twelve papers, nine reporting dimensions — the gaps are the data.*
半格（質性敘述）與「variant 3/12＝同一譜系」的說明都已在圖內 legend。

**p.25 fig6 十二數一軸（v0.3 新增）**：`fig6_twelve_numbers_one_axis.png` 整頁——每篇的
**頭條數字**照普查表原樣上 log 軸：4/12 無 bit-rate 頭條只能以文字列出、Fernando 虛線＝
工作點非天花板（不入 spread 統計）、右緣 build-flags 欄全 ✗（0/12）。副標方向：
*Twelve headline numbers, one axis — a third cannot even be placed on it.*
🔴 紅線：P4CEP 的 12 kpps **不代換算成 Mbps**（換算＝替他們做他們沒做的事）；
TSSA 沿用 fig4 已驗的 106 B frame 口徑；PADS'23–TOMACS'25 同譜系註記在 fig5。

**p.26 spread 圖**：`fig4_literature_spread.png` 整頁；副標帶對比句一類
*self-reported throughputs span ~0.57 Mbps–~1.4 Gbps (~2,500x); our same-machine
build effect alone is 8x*。

**p.27 fig8「已知≠報告規範」（v0.4 新增，§2 收尾）**：`fig8_known_but_never_reported.png`
整頁——官方 `performance.md` 原句（引文一句、逐字、已在 study §1-4 對 main 與 `f0b7d201`
兩版驗過）＋建議 flags 與參考數字（~1,047 Mbps 中位／80 kpps，c4.2xlarge）＋
issues #311/#823 流通→引用它的兩篇（ICNCC、TSSA）自己的 flags 仍不報（ICNCC 標
qualitative note only＝§2-1 的 🟡，不寫成全無敘述）→對照組 Zhang '21 逐 switch 給
commit。**這頁是對「早已被世人得知」的正面回答：已知成立，我們畫的是「已知」到
「有報」之間的斷裂**。keyline＝*Common knowledge is not a reporting norm — build flags
stated: 0/12.*（55_ 收斂措辭）。
五頁講述順序＝缺什麼（23–24）→ 數字擺一起也比不了（25）→ 單一已知變數就值 8×（26）→
而且這不是無知、是規範缺席（27）→ 落到 p.31 的「所以值得寫」。

**p.21 fig7（v0.4：表格頁換圖）**：`fig7_aggregate_two_planes.png`——FINDINGS 的
n/aggregate 表原數（OvS 540/960/720；bmv2 160–240/120–180/32–16）；紅線全數入圖＝
n=1 掛 receiver-socket-limited、天花板歸給 configured htb cap（≈971 goodput 虛線）、
bmv2 無帽的不對稱明畫（「塌到帽以下 30 倍——它根本沒戴那頂帽」）、n=1 上緣標
top-rung censored（≥240）。原表格數字轉頁面列，不丟。
🔴 **這頁多一條 08-30 當時不存在的義務：整頁的主張只在 UDP 下成立**（§B，`7f58cef4`）。
兩臂的梯階都是 `iperf3 -u -b <rate>M -l 1400`，而「最高乾淨階」是丟包率讀出來的
⇒ **這是一個 UDP 專屬的量測，不是協定通用的結論**。圖上沒有這個詞，所以
**頁面列或講稿必須帶它**——§G6 是逐字稿。

**p.31 Worth writing up?（原投稿計畫頁全換；語氣＝請教，不辯論）**，三列：

1. **量化的洞**：量 bmv2 的 12 篇無一報 build flags，而這個變數同機值 **8.0×**
   （區間 5.14–12.0、三跳 12×）——**大到使 18 篇無 build 資訊的已發表數字互相不可比較**
   （study C1 定稿句）；單位歧義另貢獻 **16×**（同批資料 pps 1.25× vs bit rate 16×）。
   💬 **只在被問到時答（不寫上頁面）：「那會不會只是你們自己那支 P4 程式？」**
   ——換成 tutorial 的 `firewall.p4` 重跑兩臂，R 的區間仍相交（§C，`9601a010`）
   ⇒ 註冊判定「程式無關」。**但答案要連下半句一起講**：兩個點估計差很多（5.14 vs 3.27），
   而差異**全部在分母**——換程式只動得了 stock 臂（1.57×），動不了 fast 臂。
   ⇒ **build 與 program 要一起報**，因為比值只對「一組（build, program）」有定義。
2. **後果與文類（09-01 夜 Adam 裁定改寫：RFC 8204 當主打）**：~2,500× 的 spread 無從歸因；
   而「已知」與「有報」之間的斷裂**在標準文件上量得出來**——
   🔑 **RFC 8204 是唯一一份專為軟體交換機寫的量測標準**，它的 §3.3 已經走到要求
   OS 版本、kernel 版本、hypervisor 型別與版本、vSwitch 的**版本號或 commit ID**、
   DPDK 與其他相依的版本，理由明寫是 repeatability——**然後它停在 commit ID。**
   五份標準（RFC 1242／2544／2889／8204＋ETSI GS NFV-TST 009 V3.4.1，約 **51,000 字**）
   合起來，**編譯旗標／最佳化等級／build 組態當成應報項目：0 次**。
   ⇒ 台上那一句：**「兩顆完全符合 RFC 8204 §3.3 欄位清單的組態，在我這台機器上差 8.0×。」**
   文類先例＝Mytkowicz et al.（ASPLOS '09）——**收緊版，不要再寫成泛稱的 measurement bias**：
   **他們的應變數本身就是最佳化等級**（O2→O3 的 speedup），被 link order 與環境變數大小
   擾動到結論反轉，跨三顆處理器、兩種編譯器，外加 ASPLOS／PACT／PLDI／CGO 的 133 篇普查。
   🔴 **證據等級：這一列全部是文獻級，不是實測級**（兩級證據紅線）——判詞標 `DESK CHECK`
   或 `LITERATURE`，語氣不可寫得像我們自己量的。**唯一的實測是那個 8.0×。**
   🔴 **可信度自陳（三級不可混用）**：RFC 8204 與 Mytkowicz 兩條**我方本 session 是轉述**，
   正本＝`~/Desktop/NDTwin slide material/paper/poster-package/71_related-work-DRAFT.md`
   （該稿宣稱 25 篇逐篇對**主文**驗過，並記著零命中 grep 的**兩個陽性對照**：
   同一條 pattern 對 bmv2 `docs/performance.md` 打到 8 次、`version` 對 `rfc8204.txt`
   打到 9 次 ⇒ 零命中是資訊不是壞掉的 grep）。**被教授追問細節前先自己打開 RFC 讀一次。**
   ⚠️ 範圍限制照抄：**宣稱只及於 RFC 8204 本文**，OPNFV VSPERF 的 Level Test Design
   未取得、不在宣稱內（71 §5-5）。
3. **請教（slide 只放這一問）**：這 18 篇裡沒找到有人量化過此事——想請老師指點是否
   已有文獻做過、要個 pointer 對帳。

**🔴 09-01 夜 Adam 覆裁：場地紅線維持，但理由換了一個（兩個理由都記著，免得下次被重開）。**
原理由是氣氛判斷；**新理由是結構的——點了場地名，話題就從「這裡有沒有貢獻」變成
「X 會收不收」，而後者正是教授已公開表態否定、且比 Adam 有發言權的那一軸。**
⇒ 不上 slide、**也不主動口頭提**。**只有教授先鬆口時**，才反問一句
「如果要投，老師覺得該往哪個方向？」——那是請益不是提案，而且他一旦說出方向就有了投入。

講稿備忘（不上台面）：教授若維持否定，口頭請示「課餘自行整理練習投稿是否介意」；
🔴 不提場地、不提其他指導可能；**poster 成品＝只在鬆口分支拿兩頁版（09-01 覆裁），六頁版不掏**。教授的「已知」對 base fact 成立
（bmv2 官方 `performance.md` 自寫 debug 慢——corpus 裡兩篇引用了它、仍未報自己的 build），
頁面只補「量化後果」那半，不反駁「已知」。

**請求要拆小，週四只提最小的那一個**（09-01 夜裁）：

| | 請求 | 對教授的成本 | 週四 |
|---|---|---|---|
| A | 給一個 pointer：有沒有人做過 | 30 秒 | ✅ **只問這個**＝上面第 3 列 |
| B | 之後看一次草稿 | 讀一次 | 🟡 A 順利才升級，**不寫上頁面** |
| C | 掛名指導、決定投哪裡 | 他的名字 | ❌ 週四不提 |

🔑 **「投稿不會被接受」裡面藏著一個成本：被拒的話他的名字在上面。** 若對話走到那裡，
直接把它拆掉——「我知道被拒的機率不低。我現在想做的不是投稿，是把它整理到老師願意看一次的程度。」

**🆕 09-02 晚 Adam 表單裁：姿態升到 B（A 順利就主動請老師看兩頁版）；判詞是 EuroP4 延期前說的；學姐在場。講稿草稿（23 頁 deck 的 p.21）：**
> 老師上次說這個問題早已被世人得知。我照這句去查了：把普查擴到 34 篇量 bmv2 的論文，沒有一篇報 build flags——包括引用了官方效能文件的那兩篇；RFC 8204 要求到 commit ID 就停。所以「已知」是對的，「有報」是零。我在同一台機器量到這個沒被報的變數值 8 倍，比 corpus 裡好幾篇宣稱的增益還大；兩篇同行審過的論文把 bmv2 和 OvS 排成相反方向、都沒報 build。我不敢說完整，每一個沒做的都寫在跑之前。**想請教老師：這 34 篇裡我沒找到有人量化過「不報 build 的後果」，老師知不知道有人做過？**
講完停。A 順利（給 pointer／「應該沒有」／開始問細節）才接 B：「我把它整理成兩頁，想請老師有空時看一次——不是要投，是想知道它有沒有到能給人看的程度。」紙本印兩份（一份給學姐）、不要求當場讀；**延期只在老師自己問時程時才提**；「投不上」就退回拆成本那句、退回 A。學姐的兩題（備答 8、9）在 p.13–14 先講掉，用「學姐上週提的這點我去查了」開頭。

### 🔴 C''-產檔紀錄 v2（09-01 深夜）：**改成「關卡帶」，第一版流程圖作廢**

> **頁序**：插在 **§2 節封面之後、`page_M_cost-and-benefit` 之前**（＝ §C 表給它的位置），
> 所以在 23 頁版裡是 **p.8，整份變 24 頁**；原 p.8 之後全部 +1。
> **它取代的是 09-01 稍早那張四方框流程圖**（Adam：太醜、沒把嚴謹度講清楚），那版作廢。
> 產出：`NDTwin_p08_how-we-measured.pptx`（一頁）與 `..._2page.pptx`（兩頁版，供挑選）。
> 產生器 `generator/build_page_how_we_measured.js`。
>
> **🔑 這一版跟第一版的差別，是它不再把嚴謹度畫成一致的。**
> 五根關卡柱，三條實驗線（BUILD／SIZE／FLOW）由左到右穿過去，**線的樣式就是主張**：
>
> | 樣式 | 意思 |
> |---|---|
> | 實線 | 照註冊的方式過了這一關 |
> | 虛線 | 過了，但形式較弱，而且我們自己標出來 |
> | ✕＋點線 | 那一關對這個實驗**根本不存在** |
>
> 圖上因此看得見三個破口：**SIZE／FLOW 的 binary identity 只從 command line 讀**
> （`weaker, disclosed`）、**FLOW 早於 CPU gate**（✕＋`no detector`）、
> **CPU GATE 那一柱是 WARNC 色**，柱下註記寫 `a sampler — on m2 it missed a co-tenant`。
> 🔴 **五關全綠的畫法會被一個問題戳破；標出破口的畫法戳不破**（§C'' 的「有界，不說完整」框架）。
>
> **灰階已驗**：實線／虛線／點線／✕ 四種在去色之後仍分得出來，顏色沒有獨自承載任何訊息。
>
> **數字全部照抄 `paper/abstract/abstract.tex` §"Three preregistered measurements"**
> （l.170–200，第二台機器見 l.290–303）：ladder ×1.5、`clean = loss ≤0.5% on 3-rep medians`、
> `±1 rung`、`1.15.3-f0b7d201`、`79.66%`。**沒有重算、沒有四捨五入。**
> 右端兩台機器只寫 `m1`／`m2` ＋ `registered replication`——**不寫機型、不寫 nslab**。
>
> **與 p.9（原 p.8）的 `COST PRE-REGISTERED` band 不重複**：那條講工單 M 自己的註冊
> （+0.530 s／0.4–0.6 s），本頁講的是 build／size／flow 三個實驗，兩邊數字不交叉。
>
> **兩頁版的第二頁 `Where it does not hold`**：把三個破口攤開成五列，多帶兩件圖上放不下的——
> 為什麼 binary identity 值得留（**它抓到的是我們自己**）、以及污染的方向
> （**外來負載只會讓臂變慢 ⇒ 被污染的那個讀數是比較好看的那個**）。
> 🔑 **選一頁版還是兩頁版，看你要不要在台上把「破口」講滿**：一頁版圖上標得到，但講稿要扛；
> 兩頁版讓第二頁替你講，代價是多一頁。
>
> 兩次幾何修正：`✕` 原本畫在柱子上（WARNC 疊 WARNC ＝看不見）⇒ 移到柱左 0.17"；
> 第二頁五列 pitch 0.86 會壓到 `keyLine` ⇒ 改 2.18／0.82。

### 🔴 C''-產檔紀錄（09-01 夜，**已被上面的 v2 取代**）：這一頁改畫成流程圖，而且它在 23 頁版裡漏掉了

> **漏掉的原因，記下來免得再犯**：23 頁的 deck 產於 v0.5，**p.15 是 v0.6 才加的**——
> 產檔 session 讀的是舊版，而它被標 🔴 不可略。
> 🔑 **教訓：template 是活的，產檔前要重讀一次 §C，不能靠 session 記憶裡的頁表。**
> （§F 已有「動工產檔前先讀最新版」，但那句話沒有指定**重讀哪一節**——現在指定：**§C 頁表**。）
>
> **Adam 09-01 裁：這一頁畫成流程圖，不用 §C'' 的六列。** 產出＝
> `NDTwin_p15_how-we-measured.pptx`（單頁），產生器 `generator/build_page_how_we_measured.js`。
> 下次重生整份 deck 時把它併回 `build_deck_903.js` 的第 15 頁位置。
>
> **六列 → 一條管線＋三個守門**，對應不是裝飾的：
>
> ```
>   1 PRE-REGISTER → 2 RUN → 3 READ OUT → 4 REPORT
>        │              │           │
>   WHEN TO STOP   THE BINARY  TWO COUNTERS
> ```
>
> - `WHEN TO STOP` 掛在 1 底下，因為**放棄判準是註冊時就寫的**，不是跑到一半才想的；
> - `THE BINARY` 掛在 2 底下，因為 binary 身分是**臂的屬性**；
> - `TWO COUNTERS` 掛在 3 底下，因為它是**讓讀數可信**的那道交叉檢查；
> - **4 REPORT 沒有守門**——到那一步只剩算術。
> - 右下一句 `EVERY STAGE CARRIES A CHECK THAT CAN STOP IT` 是給讀者的第二列說明。
>
> ✅ **§C'' 那六個不准掉的片語全部在圖上**：`before any arm ran`（1）／`the arm`（2）／
> `≤0.5%`（3）／`interval, not a point estimate`（4）／`answer no`（THE BINARY）／
> `zero cells`（WHEN TO STOP）。keyLine 與 §C'' 逐字相同。
> 頁底註帶上「**Not "complete" — bounded, and the bounds were written before the runs**」，
> 把 §C'' 那個口頭框架也釘在頁面上，講稿忘了還有頁面擋著。
>
> 兩次算錯高度已修：stage 1 與 guard 3 的內文都是四行，`SH 1.22 → 1.44`、`GH 1.34 → 1.52`。

### C''. p.15 **How we measured** 內容規格（v0.6 新增）

**為什麼要有這一頁**（寫給未來的自己，免得它被當成填充頁砍掉）：
§2 有十二頁數字，而**方法從來只以每頁的 footer／provenance 形式出現**——
讀者要把 12 個碎片拼起來才知道我們怎麼量的，而現場沒有人會做這件事。
教授的判詞是「缺乏創新性」；**我們能拿出來的不是數字更大，是這些數字被產生的方式**。
這一頁把那個方式一次講完，並且讓 p.31「值不值得寫」有東西可以指。

**素材出處**：`doc/2026-08-29_bmv2-performance-study.md` §3-0（三個工單共通的紀律表）
＋§5-1（預註冊）＋§5-2（放棄判準），皆 `b2cd6b5`；梯階與 clean 判準的定稿措辭
另見 `~/Desktop/NDTwin slide material/paper/abstract/abstract.tex` §"Three preregistered
measurements"。**照抄不重算**。

版型＝**列式六列＋一條 `keyLine()`**，照 E-delta-1 新文法（標籤 → 值，不做三段式條列）。
kicker 方向：`WRITTEN DOWN FIRST`。

🔴 **這一頁的口頭框架（09-01 夜 Adam 裁）：不要說「完整」，說「有界，而且界寫在跑之前」。**
講這一頁時的定調句＝**「我不敢說完整。我能說的是每一個沒做的，都寫在跑之前。」**
理由：「我的實驗很完整」會觸發指導教授的**找洞本能**，而洞找得到（單機、Mininet/veth
不是實體 NIC、單一 bmv2 commit、UDP 為主——全在 study §5-3），一個問題就能戳破，
接下來整段變防守。**「有界」這個框架戳不破**——每個洞都已經在投影片上，
而且它把對方的角色從「挑錯的人」換成「評估設計的人」，**那才是會答應指導的那個角色**。
⇒ 被追問外部效度時**不要辯護，直接承認並指回這一頁**：那些限制是註冊時就列的。

| 標籤 | 值（英文上頁，逐字可改，數字不可改） |
|---|---|
| `PRE-REGISTERED` | Comparison baseline, outcome intervals, and **what each outcome would mean** — frozen before any arm ran. Amendments only if zero-data, existing-data, or tightening. |
| `REPLICATION UNIT` | The interleaved arm, ≥2 per cell, mirrored schedule `1 2 4 8 16 \| 16 8 4 2 1`. A rep inside one arm is a re-read, not a replicate. |
| `THE READOUT` | ×1.5 ladder to the highest clean rung; clean = loss ≤0.5% on 3-rep medians. We report the quantisation interval (5.14–12.0), not a point estimate. |
| `THE BINARY` | Per-arm symbol signature, checked against a negative control that has to answer *no* (`3367d0e9`). Experiments 2–3 read argv only — weaker, and stated as weaker. |
| `TWO COUNTERS` | Endpoint counters **and** paired ingress-RX / egress-TX. Kernel drop counters read zero on a run where bmv2 lost 79.66% inside itself. |
| `WHEN TO STOP` | Abandonment rules written first. One fired at n=2. One round was voided at **zero cells** — either verdict was reachable from the generator alone. |

`keyLine()`：*The four-line minimum, applied to us: we had not named our own binary either.*

⚠️ **值欄放不下就砍字，但這六樣不准掉**：`before any arm ran`／`the arm`／`≤0.5%`／
`interval, not a point estimate`／`answer no`／`zero cells`。**它們各自是一列存在的理由**
——砍掉之後那一列會退化成「我們很小心」，那句話在台上沒有重量。
六列若真的塞不下，**砍 `TWO COUNTERS`**（它是六列裡唯一不影響其他頁可信度的），不要砍前四列。

🔴 **這條 keyLine 是本頁的重點，不是謙辭。** 它指的是 09-01 查出來的自報漏洞
（八臂全部跑 `simple_switch_grpc`，逐臂記在 `arm.meta` 的 `/proc/<pid>/exe`，**稿件沒說**，
而我們自己那份四行最低限度清單原本也沒有「哪一顆 target」那一格）。
**被問到就照實答**——它是這一頁可信度的來源：一份會抓到作者本人的檢查表，才是檢查表。
（同一件事已入稿：abstract.tex 的 build 段兩條 self-disclosure。）

**被問到才答（不上頁面，十一條備答；8–11 為 09-02 晚新增）**：

1. **「你怎麼知道量的時候機器沒有別人在用？」**——量測窗內取 `/proc/stat` delta 的 busy
   fraction，超出中位臂 0.15（絕對值）⇒ 整臂重跑；`load1` 只當 pre-screen（14 核上它是
   落後＋複合指標，而且會對臂自己的轉發負載發火——**gate 不能對它要保護的訊號發火**）。
   🔴 **誠實補一句**：第二台機器那一輪的 gate 是**開跑前的快照**，漏掉了一個共租 VM，
   是從對方自己的帳本查出來的、不是 gate 抓到的（已入稿）。**點取樣不算連續證據。**
2. **「量測的時候你們在做什麼？」**——不 commit。commit 會觸發背景 `agy` review
   （實測 207% CPU、突發）⇒ **記錄實驗的動作本身會污染實驗**，所以 raw 先落盤、窗後補 commit。
3. **「原始資料呢？」**——raw 一律進 `audit-raw` 分支，圖表以**內容雜湊**引用。
   🔴 **不可以說成「hook 強制」**：`pre-commit` 只擋 raw 出現在工作分支，
   **它不檢查 raw 有沒有真的進 `audit-raw`**——這是規範＋擋錯目的地的機制，不是自動保證。
4. **「那一輪『零格作廢』是什麼意思？」**——OvS 的封包大小掃描。那個 fabric 的
   1 Gbit 帽換算成三個尺寸是 1145/407/114 kpps，比值 0.10，**落在我們註冊給 per-byte 假說的
   區間內**；拿掉帽也不能救，只是把瓶頸換成發送端（同機 loopback 讀 529/536/513 kpps，
   比值 0.970，**落在 per-packet 假說的區間內，而且是對我們有利的那一邊**）。
   ⇒ **兩種結論都只靠儀器就構得到，取決於我們拿掉哪一個帽** ⇒ 一格都沒跑就作廢。
   這三個除法的成本是三次除法，我們把它寫成建議規範：**報數字時一併報發送端自己的天花板**。
5. 🔴 **「那你們註冊的預測中了嗎？」——這一題一定會被問，而且目前整份 deck 沒有答案。**
   （09-01 夜查核：`判死`／`模型判死` 在本檔出現 **0** 次；p.20／p.21 兩張圖都只講現象。）
   講完 p.15 的 `PRE-REGISTERED` 之後，這是最自然的下一問，**照實答三格**：
   - **① build**：落 **H2**（R<9）＝**主張收窄**。論文句因此改成「三跳 12×、隔離單跳 8.0×，
     差額歸屬本輪不可推論」——**註冊語義先寫好，所以收窄是照著執行不是事後解釋**。
   - **② frame size**：落 **H1（天花板是 pps）**，而且離 H2 極遠。
   - **③ 流數**：🔴 **兩個註冊模型都不中——判死即結果**。量得合計 200/220/150/52/24，
     對固定開銷模型 160/138/109/76/48、冪律 160/118/88/65/48 皆不合；四個註冊區間只有
     一格由區間裁決、**兩格反向出界**。**放棄判準在 n=2 發火**（兩臂皆 220.0 對區間 95–150）
     ⇒ 照字面執行 `Stop`：**不由這十臂重推區間**（拿十臂推的區間裁判同十臂＝循環），
     re-derive 屬下一輪、未來區間須出自 ①② 的量測。
   🔑 **這一格才是 p.15 最好的示範**：兩個模型被判死本身就是那一輪的結果之一，不是失敗
   ——**而它能算結果，唯一的原因是判準在資料之前就寫死了。**
   ⚠️ **不要把它講成「所以我們知道為什麼會塌」**：③ 至今**沒有機制**（見備答 6）。
6. 🔑 **「為什麼 frame size／流數會影響 throughput？」——兩半的答案不對稱，不可混講。**
   - **frame size：機制問到了，而且有直接證據。** 三條獨立支持（`packet-size-sweep/
     FINDINGS.md` §2/§4/§5）：(a) 六臂**全部在同一階（110 kpps）截斷**，而截斷規則只看
     loss、**對 frame size 全盲**，三個尺寸在該階的 bit rate 差 16× ⇒ 若天花板是 bps，
     1024 B 臂應在低得多的 pps 就截斷；(b) **bmv2 行程自己的 CPU 佔用橫跨整條軸近乎常數**
     （**0.1456–0.1660**，逐行程 `/proc/<pid>/stat`）＝**H1 主張的機制本身**；
     (c) 跨輪對帳（開跑前註冊於 ② AMENDMENT-1 §7.4.2）：③ 的 n=1 換算 **17.9 kpps
     @1442 B frame** 對 ② 的 1024 B 格 **16.0** ⇒ **1.12**，而 ③ 的梯子是 Mbit/s 刻度
     ⇒ 該點不可能被 ② 的 pps 軸塑形。
     ⇒ **台上一句**：「frame size 其實沒有動到瓶頸。瓶頸是**每包 CPU**，frame size 只是把
     同一個 pps 天花板換算成 bit rate 之後放大了 16 倍。」**這正是工單②那個 16× 歧義的來源。**
   - **流數：沒有機制，而且是明文判死的**（備答 5）。現象紮實——兩臂各自單調遞減
     （160/110/30/5/2 與 240/110/45/8/1 M/流，五格全部落在相鄰一階以內）——**但「為什麼」空著**。
     唯一與機制相容的**方向性**線索：把流散到多個 path class 會**抬高**合計 ⇒ 與
     「per-switch 共享 CPU」一致。🔴 **只引方向不引差值**（舊點單臂＋粗梯）。
     🔴 而 09-01 §B 又把範圍收窄一層：那個 ~10× 自塌是 **UDP 特有的**，TCP 不塌
     （`T(16)/T(1)`＝1.222／1.108）⇒ **連現象本身都比原本以為的窄。**
   🔴 **這一條的紀律**：稿件只宣稱「容量是流數的函數，報一個數字不夠」，**不宣稱機制**。
   被追問就講「兩個預先註冊的模型都被資料判死了，我們沒有拿同一批資料重推新模型——那是循環」。
   **「量到」與「因為」在本專案是兩件事**，把它們合起來講會毀掉 p.15 的全部可信度。
7. 🔴 **「別人沒在 bmv2 上掃過封包大小嗎？」——不要答「沒有人」。**（09-02 F 軸：corpus 外找到兩篇）
   答：「**我們普查的 12 篇裡沒有**。圈外有兩篇——一篇 APNOMS 2021 的 vCPE 應用論文在 10 Mbps 鏈路上掃了五個大小，只印 Mbps、沒換成 pps、build 只寫『without logging support』；一篇 VSTTE 2025 的形式方法論文用 RFC 2544 七個大小、Mbps 與 pps 雙軸，bmv2 的 pps 近乎常數，**形狀跟我們的 ② 一樣**，同樣沒有 build line。」
   ⇒ 這兩篇是 ② 的**旁證**，不是反例；稿子的否定句全部有 the 12／surveyed 設限，一句都不用改。
8. 🔴 **「這些參數（build／frame／流數）對你們引的那些效能量測論文真的重要嗎？」**（學姐 09-02 提；她 9/3 在場⇒在 p.23–24 先講掉，用「學姐上週提的這點我去查了」開頭）
   **先讓一步**：對「同一個 binary、同一個 workload 上比 A 與 B」的論文，這些參數不改變它**自己的**結論——稿子說的本來就是 *incomparable, not irreproducible*（六頁版 `:118–119`），所有否定句都框在 the 12。
   **再收回四點（全是稿裡有數字的）**：
   - 12 篇裡 **8 篇把 bit rate 當 headline，這 8 個 headline 差 ~2,500×**（`:91–93`）——被引用、被拿來比的就是這個數字；沒有 build／frame／binary，讀者看不出 0.57 Mbps（106 B frame、27.8% loss）與 1.4 Gbps（實體 NIC 均值天花板）不是同一種量。
   - **跨論文的結論已經在被下**：兩篇同行審過的論文把 bmv2 vs OvS 排成相反方向，兩篇都沒報 build（`:108–114`）。
   - **比值也不免疫**：換成 tutorial firewall，stock 臂動 1.57×（70→110）、fast 臂不動（360→360）（Table 1）——一個在 stock build 上量到的 A/B 差距，換到 fast build 可能整個消失。**build 決定了什麼東西是 program-sensitive。**
   - **同一個實驗室都對不齊自己**：PADS'24 vs PADS'26 的 per-switch RTT 差 1.7×，CPU 都寫了、build 都沒寫（`:114–118`）。
   **收尾接住她的話**：對 bmv2 數字只是附帶的論文（SOSR'17 latency only、PoliTO delay only、P4-NIDS 的 CPU 自報），參數確實較不重要——fig5 早就把它們編成 latency only，稿子沒靠它們撐任何比例。**重要的是 headline 那八篇，而那八篇正是 2,500× 的來源。**
   🔴 紅線：不說「所有論文都需要」；主詞永遠是「這 8 篇／the 12」。
9. **「12 篇太少吧？擴大 survey 之後這個數字要不要換？」**（Adam 09-02 問過；學姐可能問）
   答：「12 篇是**五欄碼本、有協定**編的；凍結後又找到 22 篇量 bmv2 的論文，用同一張表快篩——**34 篇沒有一篇報 build flags**（質性提到『關 log／改編版』的 3 篇，都不寫 flag）。」圖＝**fig5b**（`figures/fig5b_reporting_matrix_34.png`；合計數對 `poster-package/80f_ §7`）。
   🔴 **兩個分母不混**：12（全碼本；fig5、2,500× 兩端、所有 0/12 比例都算在它上面）與 22（事後篩；只保證 build／variant／version／sweep／pps／limit-check 六欄）。口頭一定帶 `post-hoc screen`／`in our sample`。
   **為什麼 9/7 前不把「12」換成「34」**：母體是先凍結再看結果的，看到結果才改分母正是稿子在批評別人的動作；而且 fig5、「八篇 headline」、2,500× 兩端全部連動，兩頁版對長度零餘裕。真正的擴大（40–80 篇、全碼本、雙 coder）排在 PAM 之後的期刊版（`80a` #1／`59_` #5／`64_` §3-1）。
   被追問「那 22 篇裡有沒有人掃過封包大小」→ 接備答 7（Elangovan、HOL4P4.EXE，形狀一樣、同樣沒 build line）。
10. **「你們普查的那 12 篇各自在做什麼？」**（講矩陣頁時可能被問；三組正好對應備答 8 的「哪些論文參數才要緊」）
    | 組 | 論文 | 核心目的 | bmv2 數字在其中的角色 |
    |---|---|---|---|
    | 修模擬真度 | TOMACS'25／PADS'23（同譜系，期刊擴充＋會議版） | 用 virtual time system 提升 P4 模擬真度 | bmv2 太慢是它們要修的病——**絕對值是論點本身** |
    | 比環境／比交換器 | PADS'24 | 比較多種 P4 模擬測試環境 | 環境間的吞吐差＝結果 |
    | | PADS'26 | 可動態卸載到硬體的 P4 模擬測試床 | headline＝per-switch RTT 729 µs；對 base Mininet 延遲降 58–84% |
    | | ICNCC'23 | 實驗比較 BMv2 vs T4P4S | corpus 最大值 1.4 Gbps（實體 NIC 均值天花板）；唯一說了 non-logging 建置、仍不寫 flags |
    | | TSSA'23 | Mininet＋P4 測試床效能分析 | corpus 最小值 0.57 Mbps（106 B frame、27.8% loss，三個 iperf buffer 情境之最低） |
    | | Network'25（MDPI） | SDN＋P4 效能評估（bmv2 vs OvS） | 排序與 TOMACS 線**相反**；工作點低 1.2–5.3 個數量級——稿裡算「control-plane effect」，不在 headline 八篇 |
    | | P4sim'25 | 把 P4 搬進 ns-3 | 以 bmv2 飽和點（≈43 Mbps）當對照 |
    | bmv2 只是載具 | P4CEP'18 | in-network 複雜事件處理 | corpus 唯一用 pps 報的（≈12 kpps @ min-size） |
    | | P4-NIDS'24 | P4 上的入侵偵測 | 80 Mbps＋CPU 自報 0.3%——**雖是載具組，仍是 headline 八篇之一** |
    | | Whippersnapper SOSR'17 | P4 語言 benchmark suite | latency only（bmv2 parse 11.2 ms） |
    | | PoliTO 碩論 | 可程式化資料平面做延遲控制 | delay only（RTT 0.98／2.16 ms） |
    台上一句：「第一組把 bmv2 的慢當成要修的病，第二組把它的數字當成結果，第三組只拿它當載具——**參數真正要緊的是有 headline 數字的那八篇：前兩組的七篇，加上第三組的 P4-NIDS。**」（八篇＝稿子 `:91–92`：TOMACS、PADS'23、PADS'24、ICNCC、TSSA、P4-NIDS、PADS'26、P4sim；其餘四篇＝pps only 1、control-plane 1、latency only 2。）
    🔴 可信度標記：這張表是 **`refs.bib` 標題＋fig5／fig6 註記的轉述**，不是 09-02 親讀；逐篇全文編碼在 study §2-1（`b2cd6b5`）與 `80a`。被追問某一篇細節就翻那一列，不要現場補。

11. **「這 34 篇是不是都發在很弱的地方？那頂會裡會不會有人有報 build？」**（學姐／教授最可能的第三題；09-02 晚清點 34 篇的場地）

    | 級別（我的判讀，非官方排名） | 篇數 | 是哪些 |
    |---|---|---|
    | 網路量測／系統旗艦會（SIGCOMM／NSDI／CoNEXT／IMC／PAM） | **0** | — |
    | 在自己領域站得住的期刊或會議 | 8 | TOMACS'25（ACM 期刊）、SIGSIM-PADS ×3、SOSR'17（ACM，已停辦）、NetCompute'18（SIGCOMM workshop）、IEEE Network'21（雜誌）、VSTTE'25（LNCS，形式方法主場） |
    | 綜合型 mega-journal | 10 | IEEE Access ×2、Sci Rep ×4、MDPI ×4（Network ×2、IoT、Electronics） |
    | 區域性／小型會議與 proceedings series | 9 | ICNCC、TSSA、MedComNet、LNNS ×2（ICAETA／INCoS）、SBRC、WPEIF、APNOMS、LOGIC |
    | 未經同儕審查或學位論文 | 7 | arXiv ×5（P4-NIDS、P4sim、MQTT-P4、Tokmakov、RL paths）、碩論 ×2（PoliTO、交大） |

    台上三句（**照這個順序講，不要先承認場地弱**）：
    1. **「這個分布本身是結果的一部分，不是抽樣瑕疵。」** 我們的檢索框是「**量了 bmv2 的論文**」，
       不是「好場地的論文」——bmv2 的效能數字本來就不出現在旗艦會，因為那些場地量的是硬體與 DPDK。
       要找 bmv2 的數字，就只能到這些地方找。
    2. **「而且 0/34 裡面包含不弱的那幾個。」** TOMACS 是 ACM 期刊、IEEE Network 是雜誌；
       圈外還有 **Elbediwy, IEEE/ACM ToN'25**（這領域最好的期刊之一，**改了 bmv2 的 C++ 重建**、仍然零 build 資訊）。
       ⇒ **不是弱場地才不報，是這件事沒有人報。**
    3. **「隔壁社群證明規範做得到。」** Zhang et al., *Computer Networks* 188 (2021)（Elsevier Q1，
       在我們 18 篇裡但**不量 bmv2**）對它量的 7 個 switch **逐一給 commit**（FastClick 9d5e9c6、t4p4s b1161b2…）
       ＋附錄逐 switch 參數＋單核釘住定頻。⇒ **差別不在場地等級，在社群慣例。**

    ⚠️ 誠實邊界（被追問時主動說）：(a) 級別是**我的判讀**，沒有引用任何官方排名（CORE／JCR 都沒查）；
    (b) 22 篇是**事後篩不是普查**，所以「旗艦會 0 篇」只描述我們手上這 34 篇，**不是說旗艦會裡沒有**；
    (c) 真要反駁我們，最省力的路就是在旗艦會裡找出一篇報了 build 的——**我們自己也想要那一篇**
    （80a A-3 停止規則第 5 條：出現了就當展品進稿，那是稿子最想要的例子，不是威脅）。

---

## D. 素材出處速查

- **四張 page 圖**：本資料夾 `figures/`（`page_M_cost-and-benefit`、`page_bandwidth-ceiling`、
  `page_Q_assumed-denominator`、`page_Q_gate-after-fix`）。
  ⚠️ `page_bandwidth-ceiling.png` 已是 **08-28 裁決版**（08-30 依裁決重渲更換；
  舊版在 `figures/_superseded/`，**勿用**）。
  重渲指令（byte-exact 驗證過，`98aea55`）：
  `"…/NDTwin Slide material 820/.plotvenv/bin/python3" plot_deck_903_round2.py <outdir>`
  （腳本在 repo `doc/audit/2026-08-28_QM-mirrored-block/`，檔頭寫著直譯器路徑）。
- 🔴 **09-02 `fig4` 重渲（p.26 用的那張）**：圖內字 `~2,500×, zero papers report build` 是全稿**唯一沒有分母的否定句**
  （C 軸審稿抓到；紅線＝否定句主詞一律「這 18 篇／the 12／the eight」），Adam 09-02 裁「改」。
  改 `make_figs.py:181` 為 `…; none of the eight reports its build`（the eight＝畫在這根軸上的八篇 bit-rate 論文，
  與論文 caption「in any of the eight」同口徑）→ 用 `.plotvenv` 重渲：**fig1／fig2／fig3 逐位元不變（陽性對照）**，
  fig4 `c4c17795…` → **`6b55336a…`**；三處部署（repo 根、`paper/abstract/figs/`、本資料夾 `figures/`）sha 同；
  舊圖存 `figures/_superseded/fig4_literature_spread_pre-denominator-0902.png`。
  ⇒ **09-01 產出的 `NDTwin_deck_903.pptx` 裡的 fig4 是舊字**；重產 deck 時會自動帶到新圖（§C0 已標整份要重產）。
- 🔁 **fig5 09-02 18:06 重生**（`make_survey_figs.py` 提交 于 trunk）：合計列「10/12 3/12 …」原本壓在最後一列格子上，在兩頁版 .82 倍縮放時疊字（Adam 09-02 發現）。已下移；`figures/fig5_reporting_matrix.png` 已換新（sha `24e8d236`），舊圖在 `figures/_superseded/fig5_reporting_matrix_pre-totals-0902.png`。**p.23 用到它 ⇒ deck 重產時會自動吃到新圖。**
- 🆕 **fig5b（09-02 19:00，Adam 點名要的簡報圖）**：`figures/fig5b_reporting_matrix_34.png`（sha `cbc416df…`；repo 同目錄有 `.pdf`）——fig5 同一張矩陣擴到 **34 篇量測篇＝12 corpus＋22 事後篩**，7 欄（事後篩沒編碼的 build A/B／flows／comparison plane 三欄**不畫**，未編碼不冒充未報告）；欄合計 assert 對 `poster-package/80f_ §7`：**build flags 0/34**（質性 3＝ICNCC'23／SBRC'26／Elangovan「關 log／改編版」）、version 2/34、variant 8/34、**pkt-size sweep 2/34**（Elangovan APNOMS'21、HOL4P4.EXE VSTTE'25 兩篇圈外掃描，照實畫）、pps 4/34、limit check 0/34。給口頭那句「12 篇全編碼＋22 篇事後篩，34 篇沒有一篇報 build」用。腳本 `make_survey_figs.py::fig5b`（repo trunk 09-02 晚 commit）、逐列出處 `fig5b_reporting_matrix_34.md`。**排哪一頁 Adam 定**（候選：p.23 普查記分板旁、或緊接 p.24）。措辭紅線：`post-hoc screen`／`in our sample` 跟著 34 走，不可掉。
- **四張 fig 圖**：repo `doc/2026-08-29_bmv2-performance-study-figs/`（fig1 unit-ambiguity、
  fig2 perflow-monotone、fig3 build-two-working-points、fig4 literature-spread；
  PASS 版 byte-identical 搬移，`7ca06e0`）。
  🆕 v0.2（08-30 深夜）：四張已複製進本資料夾 `figures/`，sha256 與 repo 正本逐張比對相同
  ——**產檔 FIG 指本資料夾即可全取**（fig3 目前沒排頁，備而不用）。
  版面刻意維持扁平（Adam 授權裁量、我裁不分子資料夾）：兩族靠 `page_`／`fig` 前綴自明，
  大綱表引的是裸檔名、產生器單一 FIG 根目錄最不會出事；**唯一子資料夾＝`_superseded/`**
  ——「現行 vs 已取代」才是真正會拿錯的軸，那一軸已經隔開了。
- **手冊線數字**：`doc/2026-08-30_manual-verification-report.md`（彙整）＋
  `doc/audit/2026-08-30_live-full-stack-round/`（FINDING-01〜05、R2/R5 結果）。
- **容量／OvS 對照**：`doc/audit/2026-08-30_ovs-flowcount-control/FINDINGS.md`（更正版）＋
  `doc/2026-08-29_bmv2-performance-study.md` §4（兩檔最新修訂皆 `b2cd6b5`）。
- **文獻回顧（p.23–26）**：study §1 spread 表＋§2-1 普查表與統計段（`b2cd6b5`）；
  fig4 素材＝上列 study-figs。統計口徑照抄，含 TOMACS'25＝PADS'23 期刊擴充的
  「發表紀錄 3/12／獨立工作 2/11」雙算法（§2-1 註）。
- **新圖組（fig5–fig8；p.24、p.25、p.21、p.27）**：腳本＝study-figs 目錄
  `make_survey_figs.py`（fig5/6 逐格出自 study §2-1 @ `b2cd6b5`、欄合計 assert 護欄、
  與 fig4 重疊條目沿用其已驗 tuple；fig7 全數出自 OvS FINDINGS 的 n/aggregate 表＋
  ≈971 goodput 帽；fig8 事實出自 study §1-4 與 §2-1 列 13）。PNG/PDF 渲於同目錄＋
  已複製進本資料夾 `figures/`（byte 相同）。
  🔴 **fig7 的兩個平面都是 UDP**（`iperf3 -u -b <rate>M -l 1400`，兩支 driver 逐字可查：
  `2026-08-30_ovs-flowcount-control/drive_ovs.sh:81`、`run_ovs_arm.sh:88`），
  而 09-01 §B（`7f58cef4`）證明改 TCP 就不塌 ⇒ **x 軸 09-01 已改成 `same UDP ladder`
  並重新部署**（`figures/` 的 fig7＝`f7aeeede…`，舊版 `ce9664c0…` 在 `_superseded/`；
  fig5/6/8 同批重渲逐位元不變）。**其餘六條圖內註記仍無協定字樣** ⇒ §G6 的 REQUIRED 照留。
  🏁 **已 commit＝`408d31b`（08-31 11:15，"the A2b provenance chain closes"）**——
  量測窗內先落盤、窗後補 commit 的計畫如期執行，A2b 鏈閉合。
- **有流量輪**：`doc/audit/2026-08-30_live-traffic-round/`（9/03 前產出）。

## E. 視覺規格

**827 版 §E 全文照用**（含 E1–E6、三十二條地雷）。903 有兩條 delta：

### 🔴 E-delta-1. **9/03 是第一份全面採用新版面文法的 deck（Adam 2026-08-30 裁定）**

起因：Adam 拿 `qec_week1_weekly_update_unified.pptx` 對照——「**字少、沒有廢話、
很清楚地傳達資訊**」，看完五頁範例後裁定「**以後就照這個格式**」。

- **規格全文在 827 §E3a**，helper 在 `generator/deck_style.js`
  （`head` / `row` / `chip` / `question` / `footNote` / `keyLine`，已抄進本資料夾）。
- **五頁範例**：本資料夾 `NDTwin_style-examples.pptx`（＋ .pdf），
  參考實作 `generator/build_examples.js`。**產檔前先看過那五頁再動筆。**
- 五頁涵蓋五種版型原型，對得上本檔 §C 的頁：
  | 範例頁 | 原型 | 對應 903 的頁 |
  |---|---|---|
  | 1 Where we left off | 承諾表：問題／判準／判詞／今天 | **p.4**（B1 表，四條） |
  | 2 The failover budget | 問句＋列＋右側圖 | p.21（aggregate 對照，v0.4 起有 fig7）、p.29（有流量輪） |
  | 3 The 45-point thread | 表格＋表下四列 | **p.7 覆蓋地圖**、p.8、p.23 普查記分板 |
  | 4 Pre-registered, then withdrawn | 判詞串起整段論證 | **p.31 Worth writing up?**、**p.15 How we measured**、p.10、p.11 |
  | 5 Where it stands | 左右兩欄純片語 | **p.33 Where it stands**（本檔；§B1 的 p.32 是 8/27 那份——v0.5 時兩者剛好同號，v0.6 插入 p.15 之後又岔開了） |

**四件產檔時一定會踩到的**：

1. 🔴 **§C 大綱表裡的「三列＋兩註」「表＋兩列」這類版型敘述，是 827 的舊文法。**
   照 E3a 一律譯成「標籤 → 值」的列，**不要真的去做三段式條列**。
2. 🔴 **副標整條刪掉。** §C' 給了 p.23–26 的副標句（照 E4d ≤130 字元）——
   那是舊格式的規格，改成 **kicker（片語、六個詞以內）**。
   p.23 那句 *The one variable we measured at 8x is the one none of them state.*
   保留價值高，但它是**主張**不是副標 ⇒ 降成頁上的一列（標籤 `THE GAP`）或 `keyLine()`。
3. 🔴 **措辭紅線不因為變短而放寬**：p.23 否定句主詞＝「這 18 篇」、`in our sample`
   限定不可丟。片語化之後**更容易掉限定詞**——`0/12 build flags · in our sample of 18`，
   限定詞跟著數字走，不要獨立成句然後被砍掉。
4. 🔴 **兩級證據的區分要靠判詞承載**：desk-check 級的話用 `DESK CHECK`／`NOT MEASURED`
   當標籤，不要寫成跟實測同樣語氣的片語。p.31 第 2 列尤其；fig8 那頁（p.27）整頁是
   survey/desk 級，kicker 或判詞要讓這一點可見。

### 🔴 E-delta-3. **字級 v2（Adam 2026-09-01：「原本的字太小了」，第二次）**

第一版把內文從 12.5 加到 16，就是因為同一句話；**這次還是太小**。原因不是上一次調得不夠，
是**字砍了第二輪，所以字級可以再買一次**——頁面現在只放四到五列，不是八列，18pt 就放得下。

| 元素 | v1 | **v2** |
|---|---|---|
| 頁標題 | 34 | **36** |
| kicker | 13.5 | **15** |
| **值（內文）** | 16 | **18** |
| 標籤 | 14 | **16** |
| 問句／qualifier | 19／13 | **22／14.5** |
| 表格 | 13.5 | **15** |
| 判詞 chip | 12 | **13** |
| keyLine | 14 | **16** |
| 頁底註 | 11 | **12** ← 全頁最小，不得再小 |
| 🆕 **大數字頁** | — | **68pt 數字＋15.5pt 說明** |

常數集中在 `deck_style.js` 的 `T` 物件，**helper 全部從 `T` 取預設**——下次再調只改一處。
🆕 `S.bigStats(s, [[數字, 說明], …], y0)`：一到兩列、每列最多三個。

🔑 **砍字買字級，而且一次只能買一次。**
兩次都是同一個形狀——先砍了字，然後忘記把空出來的版面換成字級，於是 Adam 講第二次。
**以後砍完頁數，字級預設跟著往上調一階，再問要不要收回來。**

### E-delta-2. p.19 的頁標題不要重複圖內標題

p.19 那張圖的標題已在圖內（「A working point from one plane means nothing on the other」），
頁標題不要再重複同一句——取 `The ceiling was the access layer; bmv2's is real` 一類的對偶句。
（新文法下這頁的 kicker 也一樣不要複述圖內的字。）

## F. 給產檔 session 的注意事項

- 🔴 **v0.6 的頁碼與已產出的 pptx／pdf 不同，這是唯一一條會讓你整份放錯位置的事。**
  新增 p.15「How we measured」（規格 §C''，無圖、列式六列＋keyLine），
  **原 p.15–32 一律 +1 ⇒ 33 頁**。**§C0 那一節是 09-01 產檔的存證、頁碼停在 32 頁版，
  它的 §G↔頁 對帳表與可略順位都不可拿來用**——照 §C 表產檔，產完再自己重列一份 §G 對帳。
  新頁**不需要 §G 條目**（它不是圖，沒有「字被搬走」的問題）。
- 產生器沿用 `827/generator/build_deck_827.js` 的骨架，但**版面照 E-delta-1 的新文法**
  （`build_examples.js` 才是版型範本，`build_deck_827.js` 只是取內容與結構）；
  `deck_style.js` 已抄進 `903/generator/`；`FIG`/`OUT` 兩個絕對路徑改本機；
  頁碼自動計數不寫死。
- 圖的 provenance 都可重建（D 節指令），**不要**把 `_superseded/` 的東西撈回來。
- 本檔 🔲 未填處在產檔時仍未填的：照 E5 慣例整頁跳過並在 Outline 收斂頁碼範圍，
  不要留空頁或「TBD」上台。
- 🔴 **§G 標 REQUIRED 的那幾條是產檔義務，不是參考資料。** 08-30 乾淨圖裁決把副標、footer、
  stamp、圖上註記全搬出圖面，所以那些防誤讀的句子**只剩 §G 這一份**——逐條落成頁面文字或講稿，
  跟圖同台。**省掉的時候圖上不會有任何東西提醒你它曾經在**，這是唯一擋得住它的地方。
- 🔴 **§G 現在有七節，而 G6／G7 是 `fig*` 圖。** 不要照「§G＝那四張被搬過字的圖」去掃——
  **G5、G6、G7 的 REQUIRED 從來沒在圖上出現過**（一張沒有前身，兩張的紅線比圖晚一天）。
  產檔前**逐節走一遍 G1–G7**，不要憑「這張圖看起來很乾淨」跳過。
  🔑 09-01 `page_bandwidth-ceiling` 的失效就是這個形狀：義務寫在**存放文字的那一節**，
  沒接到**指揮執行者的這一節**，於是一張 32 流的圖跟一張 1 流的圖並排上了台。

[Co-developed with claude code -- Adam]

---

## G. 圖面補充資訊（08-30 乾淨圖裁決：圖上只留標題＋參數行，字句全搬到這裡）

四張圖已重渲部署（舊版在 `figures/_superseded/*_pre-cleanfig-0830.png`）。
每張的「原副標／原footer／原圖上註記」逐字存此；標 **REQUIRED** 的必須以頁面文字或講稿
形式跟圖同台出現，不可省。腳本改動＝repo `ad2fe42`＋label 修正 commit。

⚠️ **G5／G6 不是重渲來的，別照上面那句讀**：G5（E 輪）沒有前身，三條 REQUIRED 是首次落筆；
G6（fig7）是**圖畫完之後才產生的紅線**——這一節因此**不再只涵蓋四張 `page_*` 圖**。
🔑 判準不是「這張圖有沒有被 08-30 裁決搬過字」，是「**讀者會走的那條路徑上，看得到它嗎**」。

### G1. `page_M_cost-and-benefit.png`
- **REQUIRED（原 stamp）**：COST PRE-REGISTERED · BENEFIT POST-HOC——
  「Cost is the pre-registered primary measure — latency to first path, effect +0.530 s,
  inside the registered 0.4–0.6 s. Benefit is POST-HOC and was not registered before the
  data was read.」
- 原副標另含：Six mirrored arms, one fabric generation.
- 原圖上註記：groups do not overlap (1 kHz min 0.623, 1 Hz max 0.335)。
- 原 footer：Source: REPORT.md (committed); every number is parsed from it and the parses
  assert their yield. CPU is /proc/<kernel pid>/stat utime+stime — the kernel process, not
  the machine, which ran 87% busy. Q2/Q5 carry ticket Q's fix but still recompute at 1 kHz.
  51.16% at full precision. Three figures were briefly in circulation — 51.22, 51.25, 51.3 —
  differing in the third significant digit, while this quantity's within-condition spread is
  0.033 cores (~5%): what needed correcting was a precision claim, not the effect, which is
  "about half" on every version.

### G2. `page_bandwidth-ceiling.png`
- **REQUIRED（原 ECMP 註記，~9000× 誤讀防線）**：these four carried almost no traffic this
  run (ECMP hashed onto the top four) — not a capacity floor.
- **REQUIRED（footer 核心句）**：OVS values are measured interface-counter rates, NOT
  capacities: 32 TCP flows, 53.1 is one link's ECMP share, the eight links carried 121.9
  Gbit/s together, and that run was host-CPU saturated (98.7%) — the host's ceiling divided
  by ECMP, not the link's. The 'before' run was not saturated (35.1%); 1.015 is the shaper.
- 原副標：Left: OVS — removing the access-layer bw= shaping takes a single core link from
  1.015 to 53.1 Gbit/s, so the '10 G is unreachable' belief was measuring the shaper.
  Right: bmv2 — the -O3 no-logging build — saturates at about 0.49 Gbit/s delivered no
  matter what is offered.
- 原 footer 其餘：bmv2's number is a single flow; sixteen flows together reach only
  ~48 Mbit/s（同路徑版 ~32 Mbit，見 study §4）, because the bottleneck is the switch's
  per-packet CPU and not the link — a single-flow ceiling does not extrapolate even within
  bmv2. Build named because two installs differ 12-18x: bmv2-fast/bin/simple_switch_grpc,
  sha256 3ff54b5c, fixed by p4_proxy/mininet/bmv2_binary_override.
- 原 stamp：MEASURED。

### G3. `page_Q_assumed-denominator.png`
- 原副標：The rate loop divides a per-round byte accumulator by a hard-coded 1 s. Every
  period we have ever measured is longer than that, so every published bit-rate is high —
  and the gap widens with load.
- 原 footer L：Source: drive_Q.log and survey_T64.log, both committed. Periods are recovered
  from clustered edge-update transitions; the two ticket-Q arms ran back to back in one
  fabric generation.
- **REQUIRED（原 footer R，效果量的誠實框）**：the effect is real and always in the same
  direction, but at these work points it is about the size of the arm-to-arm noise. That is
  why the verdict rests on the in-loop instrument rather than on this ratio.
- 原 stamp：MEASURED。

### G4. `page_Q_gate-after-fix.png`
- 原卡片一（GATE PASSED）：7/7 live checks · worst disagreement 0.0000% · threshold 1%。
  Intervals seen: 1.004–1.059 s. Not one of them is 1.000.
- 原卡片二：The baseline arm has no point on the plot, and that is the point — the
  instrument does not exist in the old binary, so the baseline records ABSENT — recorded as
  absent, never as a pass. An empty reading is not a zero.
- **REQUIRED（原卡片三）**：What this figure does not claim — that the over-report is gone.
  It proves the divisor is now the measured interval. Whether the published rate lands back
  on 1.00 is the ratio test.
- 原副標：Ticket Q divides the accumulator by the elapsed time it accumulated over. The
  gate instrument prints both numbers every round, and they must agree to within 1%.
- 原 footer：Source: raw/Q_Q1.divisor and the driver's own GATE line, both committed. The
  binary under measurement was verified by the sha256 of /proc/<pid>/exe rather than by
  its path.

### G5. `page_ceiling-not-read-out.png`（09-01 新增，E 輪）

這張圖**沒有前身**，所以下面沒有「原副標／原 footer」——三條 REQUIRED 是**首次落筆**，
不是從圖面搬下來的。規格見 auditor 09-01 08:1x 派工與 `ndtwin-current-state.md` 補記三十二 §C。

- **REQUIRED（誤讀防線一，最重要）**：**天花板沒有被讀出來。** `SATURATED` 判準在 72 格裡
  **一次都沒有觸發**，所以四條臂全部**右截斷於 ≥1/1**。這頁**不得**被講成「天花板是 1/1」
  ——兩個右截斷的值互相比較是**不可分辨**，不是相等。R-E1／R-E2 的答案就是「不可分辨」，
  而那是註冊設計的**合法結果，不是失敗**。
- **REQUIRED（誤讀防線二）**：**右邊那條平的線不是好消息。** 判準比的是「分身 ÷ 真值」，
  而在 1/4 與 1/1 兩者**一起塌**，所以比值仍然貼著 1.00——它在毀掉 87–89% 流量的階
  讀出 **1.009／1.014**，比 1/1024 的 1.000／1.002 還「好」。**判準對這個失效模式是結構性
  隱形的**，這是本輪最強的發現：不是天花板量測失敗，是判準從來沒在量它名字說的那個量。
  ⇒ 講稿必須帶一句：「ceiling on TELEMETRY FIDELITY ≠ 安全的操作取樣率。」
- **REQUIRED（誤讀防線三）**：**batching 的主效應在本輪設計下不可估。** `bl`/`p` 兩臂皆
  batch off、`m`/`mp` 皆 batch on，而兩者分屬相隔 3.3 小時的兩條 leg ⇒ **與時段完全混疊**
  （F-28）。**再多 rep 都救不回來，那是混淆不是雜訊。** 本圖**只畫 leg 1 的 `bl`/`p`** 正是
  為此；有人問「另外兩臂呢」，答案是它們在圖外，且合併畫會讓一個混淆的對比看起來像普通對比。
- 圖面讀法（非 REQUIRED，但被問到會用上）：
  - **左圖只看得到一條線是對的**——`bl` 與 `p` 在 1/1024–1/8 幾乎完全重合（皆 ~206 Mbit/s），
    紅線壓在藍線底下。到 1/4、1/1 才分開。
  - **兩張圖的線在灰帶裡行為不同，是刻意的**：註冊把 1/4、1/1 排除的是**精度曲線**
    （右圖），所以右圖的線停在灰帶邊界、點畫空心且不連；左圖的崩塌**正是**那兩階被判
    `DATAPLANE-HURT` 的原因，斷開它等於把證據藏起來。
  - **右圖 `bl` 在 1/8 掉到 0.972** 是 leg 內的臂間差異（`bl−p` = −0.0292）。那是**交互作用
    的一半、不是主效應**，且 Q2/E4 **禁止**拿它來補強 primary。被問就講「這是註冊之外的觀察，
    機制不宣稱」。
  - 「87–89%」的**分母是 1/1024 那階自己送出的量**（206 Mbit/s），不是 offered 的 200 Mbit/s。
- Provenance：產生器 `doc/audit/2026-08-31_sampling-ceiling-after-merge/plot_page_ceiling.py`
  （repo 內），資料 `raw/cells.tsv`（同目錄，且已在 `audit-raw` 分支 `e803c13`）。
  腳本自帶 assert：16 個 (arm,rung) 組 × n=3、`DATAPLANE-HURT` 恰好落在 {1/4, 1/1}、
  `SATURATED` 零命中——**最後一條若失敗，這張圖的前提就不成立了，會直接炸掉而不是畫錯**。
  重建 byte-exact 已驗。

### G6. `fig7_aggregate_two_planes.png`（09-01 新增，§B 之後）

這一節的存在本身是一個更正。**08-30 乾淨圖裁決只處理了四張 `page_*` 圖，`fig5–fig8`
沒有 §G 條目**——當時成立，因為那四張是「字被搬走」的圖，而 fig7 是「紅線句已入圖」的圖。
🔴 **但 09-01 §B 產生了一條圖裡沒有、也不可能有的紅線**（PNG 渲於 08-30 21:40，
§B 判定 09-01 11:24）。所以 fig7 現在也需要一個 §G 條目，而且只需要這一條。

- **REQUIRED（唯一一條，也是這頁最容易被問倒的地方）**：**這一頁的塌陷是 UDP 的。**
  兩個平面的梯階都用 `iperf3 -u -b <rate>M -l 1400`，判準是丟包率讀出來的「最高乾淨階」
  ⇒ **整張圖是一個 UDP 專屬的量測**。同一顆交換機、同一條五跳路徑改用 TCP，
  `T(16)/T(1)`＝**1.222／1.108**——**不塌**（§B，`7f58cef4`；loopback 對照 3.854 已排除宿主）。
  頁面或講稿必須出現「UDP」這個詞；**只講「aggregate 自塌 10×」就是超出量到的範圍**。
- **講稿建議句**：「這是 UDP 下的量測。同一條路徑我們用 TCP 跑過對照，十六條並發不塌——
  所以這張圖說的是『UDP 的塌陷』，不是『bmv2 的塌陷』。」
  （**主張沒有變弱**：本文的主張是「容量是流數的函數、報一個數字不夠」，
  而「連協定都會換掉答案」是同一個主張的第四種形態，不是它的反例。）
- 🔴 **禁止**（PREREG §B.2，資料前凍結）：**不得**把 TCP 的 269 Mbit 與 ③ 的 24 Mbit 並排——
  兩者不是同一個量，「11 倍的歧義只由傳輸協定決定」這句話**很好聽而且不准寫**；
  **不得**引 Chen 組作旁證。被問到 TCP 有多快，答「我們量了，但它跟這張圖的 y 軸不是同一個量」。
- 🏁 **09-01 圖已重渲，限定詞現在也在圖上了**（reviewer 線）：x 軸從
  `concurrent flows n (same ladder, mirrored arms)` 改成 **`… (same UDP ladder, …)`**。
  ⇒ 這條 REQUIRED **不再是唯一防線**，但**仍然是義務**——軸標只說得出「梯階是 UDP 的」，
  說不出「我們用 TCP 跑過對照而它不塌」，而後者才是被問到時要答的那半句。
- 圖內註記逐字（產檔時不必重打，供核對圖面用）：`configured htb 1 Gbit cap (≈971 Mbit
  goodput)`／`receiver-socket-limited`／`holds at the cap, split across flows`／
  `upper edge at n=1: top-rung censored (≥240)`／`collapses ≈10× — to 30× below the cap it
  does not even wear`／`per-flow gap at n=16: 22–45×`。
  ⚠️ **這六條仍然一條都沒提協定**——協定只在 x 軸上。所以「有人只讀了那句橘色註記」
  這個情境**沒有被修掉**，講稿那句照講。
- Provenance：產生器 `doc/2026-08-29_bmv2-performance-study-figs/make_survey_figs.py`
  （repo 內；`408d31b` 起，09-01 的 x 軸改動另有 commit），資料＝OvS FINDINGS 的
  n/aggregate 表（`b2cd6b5`）。
  🔴 **PNG 在 repo 外、腳本在 repo 內**——所以 09-01 是**改腳本再重渲再複製**，不是改 PNG
  （同 `page_bandwidth-ceiling` 的邊界更正：只改 PNG 會讓它掉回不可重建）。
  腳本有 `assert matplotlib.__version__.startswith("3.11")`；本機唯一合格直譯器＝
  `~/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3`（3.11.1）。
  **同批重渲的 fig5／fig6／fig8 sha256 逐位元不變**（只有 fig7 動），舊圖存
  `figures/_superseded/fig7_aggregate_two_planes_pre-udp-qualifier-0901.png`
  （`ce9664c0…` → 新 `f7aeeede…`）。

### G7. `fig2_perflow_monotone.png`（09-01 新增，與 G6 同一條 REQUIRED）

**同一個限定詞，第二頁。** p.20 與 p.21 出自同一批 UDP 梯階資料，所以 G6 的 REQUIRED
**原文照套**——這一節不重複，只記兩處差別：

- **圖本身沒有說謊**：y 軸逐字是 `per-flow highest clean rate (Mbit/s)`，而「最高乾淨速率」
  依定義是丟包讀出來的量 ⇒ **懂方法學的人看得出是 UDP**。
  🔑 **但頁面的宣稱句是「容量是流數的函數」，而那句話沒有協定。**
  ⇒ **REQUIRED 是掛在句子上，不是掛在圖上**：講「容量是流數的函數」的那一句要帶 UDP。
- **這頁不在可略清單**（見 §C 表下方的「可略順位」段），所以它一定會上台
  ⇒ 這條不能靠「那頁可能被跳過」省掉。
- Provenance：`make_figs.py`（study-figs 目錄，`3661525`）。fig1–4 那支與 fig5–8 那支
  是兩支不同腳本，同目錄 `README-generators.md` 記分工。
