# NDTwin 進度報告簡報 — 資訊模板（給簡報生成 agent）

**用途**：這份文件是生成簡報的唯一資訊來源模板。逐頁大綱在第 C 節；每頁列出「要點」（簡報內容）、「素材出處」（查證用的 commit/檔案）、「備註」（口頭補充或注意事項）。視覺與版面規格在第 E 節。
**版本**：v4.5（2026-08-19 深夜，**投影片已依此版產出**）。v1 = 2026-08-11 原稿；v2 = 08-13 校訂（數字、Phase 狀態、A2 裁定表）；v3 = **併入視覺規格與英文化決定，並重編頁碼**；v4 = 第 2 節壓縮與兩張混淆表作廢；v4.1 = **Page 42 事實更正與數字重量**；v4.2 = Page 39 補齊＋KNOWN-ISSUES；v4.3 = P4 遙測精度實測、圖表產出、參考文獻與 future work 頁新增；v4.4 = **第 2 節延後、第 3 節拆解、Page 24 全頁改寫、P4/128 實測、用詞更正**；v4.5 = **v4.4 全部落地成 43 頁投影片、八張圖各佔一頁、行數重量、九項精簡裁定**；
v4.6 = **failover raster 補上第四格、decomposition 因第四格改版、23→40 次全面更正、demo 錄製流程**；
v4.7 = **v4.6 全部落地、新增「下一次的預計進度」頁，共 44 頁**；
v4.8 = **Page 16／17 由條列改為流程圖；另出兩張獨立圖：proxy 模組關係圖、liveness/failover 流程圖**。

> ## 🟢 v4.8 修訂摘要（2026-08-20）
>
> 1. 🟢 **Page 16（Liveness）與 Page 17（Failover）全頁改成流程圖**，風格比照架構圖。
>    詳細規格與逐格內容寫在該兩頁的條目裡。**頁數不變，仍是 44 頁。**
>    🔑 **不是把條列排版成圖，是把原始碼的控制流畫出來。**兩張都直接讀碼：
>    `p4LivenessFor()`（C++）與 `check_link_beacons()` / `run_watchdog_pass()`（Python）。
> 2. 🆕 **`NDTwin_proxy_modules.pptx`（本資料夾）**——八個 proxy 模組彼此、以及與 kernel／switch
>    的關係圖，**不在 deck 裡**，Adam 要求單獨出。同樣是讀執行期接線畫的（`main.py` 的
>    `sample_callback` / `packet_in_callback` 賦值），不是 import 圖。
>    圖檔另存 `figures/proxy_modules.png`。
> 3. 🆕 **`NDTwin_liveness_failover_flows.pptx`**——上面那兩張流程圖的獨立雙頁版（沒有節次標記），
>    圖檔 `figures/liveness_flow.png`、`figures/failover_flow.png`。
>    產生器 `generator/build_flow_diagrams.js`，deck 版由同一份程式碼搬進 `build_deck.js`。
> 4. 🆕 **`NDTwin_phase7_power_flow.pptx`（單頁）**——Phase 7 電源管理的流程圖，Adam 要求單獨出，
>    **deck 的 Page 18 尚未替換**（要換再說）。同樣是讀原始碼畫的：
>    `P4PowerStrategy.cpp` 的 `powerOn()` / `powerOff()` ＋ `topology_manager.py` 的 `readopt_switch()`。
>    左右兩欄（off 三格、on 五格），失敗出口全部畫成獨立小框（`success` / `500` / `502`）。
>    🔑 **這頁最值得講的是右欄第一個判斷**：`if (getVertexIsUp(node)) return success();`
>    ——關機後約 10 秒內它會誤觸發（1 Hz liveness worker 已經把死掉的交換機翻回 up），
>    回 200、0.01 秒、什麼都沒做。**這正好是人手動示範「關掉再打開」會踩到的窗口**，
>    所以圖上直接把繞法寫在旁邊：**等 15 秒**。
>    ⚠️ 其餘三則右欄註記各自回答一個會被問的問題：readopt 為什麼非做不可
>    （重啟的 bmv2 沒有 pipeline／clone session／table entries／mastership，而**探測看不出來**）、
>    為什麼是 `--fail-with-body` 不是 `-f`（`-f` 會把 body 丟掉，而 body 是唯一寫著哪一步壞掉的地方）、
>    以及失敗後**只能直接重試 readopt**（重打 power-on 會撞上上面那個 early-return；
>    off-then-on 也不行，實測回 500，因為 liveness prober 一直打死掉的 port，
>    grpc 的 process-global subchannel pool 會把累積的 backoff 交給下一個同位址的 channel）。
>    圖檔 `figures/phase7_power_flow.png`，產生器 `generator/build_power_diagram.js`。
> 5. 🔴 **Page 13 的模組表行數已過期**（`topology_manager` 1,392 → **1,516**、`p4_client` 587 → **755**、
>    `api_routes` 256 → **366**、`main` 305 → **345**、`kernel_notifier` 144 → **184**；
>    `sflow_emitter` 448 與 `ryu_topology` 338、`ryu_flow_stats` 190 不變）。**尚未更新，動筆時一起改。**

---

> ## 🟢 v4.7 修訂摘要（2026-08-20，**deck 已重生為 44 頁**）
>
> ### 🆕 新增一頁：`Planned for the next report`（**p.43，接在 Future work 後面**）
> Adam 2026-08-19 指定：結尾要有一頁講**下一次報告的預計進度**，三條。
> **這頁與 Future work 的分工要講清楚**（否則會被問「這兩頁差在哪」）：
> **Future work = 已經定位、但沒有排程的三個結構性問題**（併發控制、拆檔、completion handle）；
> **Planned = 下一次就要交出數字的三件事**，每一條都有「現在的數字」和「怎麼算做完」。
>
> | # | 題目 | 現在的數字 | 判準（寫在投影片上） |
> |---|---|---|---|
> | 1 | **查 OVS 128-host 復原時間到底花在哪** | OVS 51.75 s vs P4 16.59 s，**零重疊** | 偵測＋重算＋裝規則要**加得起來等於 51.75 s** |
> | 2 | **加快 failover 偵測** | beacon 5 s、timeout 15 s（衍生）、三次沒收到才判死 | **看誤判率，不看偵測時間** |
> | 3 | **把 fast build 升成預設** | stock 40 Mbps / 3.6k pps → fast 460–530 Mbps / 50.8k pps | **L0–L4 整套在 fast build 上通過** |
>
> **① 的關鍵是「已經排除了什麼」**：路徑計算不是原因——同一張 fabric 上
> Ryu 側 16,256 條路徑實際只花約 13 s（量到 73 s，其中 60 s 是寫死的 `hub.sleep(60)`），
> P4 側 11 s。🔑 **這句一定要講**，否則聽起來像「我們不知道，打算亂查」。
>
> **② 的常數都在 `p4_proxy/proxy_agent/topology_manager.py:137,155,158`**，
> 而且 timeout 與 watchdog 間隔**都是從 beacon 衍生的**，改一個動三個。
> 🔴 **投影片上不要承諾偵測時間會降多少**——`KNOWN-ISSUES.md` §D-2 已經論證過
> 「會抖動的鏈路報告比慢的更糟」，每一次誤判都讓 kernel 拆邊、退出 BFS、重算全域路徑。
> 🔑 **頁底那句「先解決一個疑點」是刻意放的**：註解寫偵測要 15–20 s，round 4 實測 10.7–14 s。
> **在對不上模型之前調參，調完會不知道是什麼在動。** 這句話本身就是在示範怎麼做實驗。
> ⚠️ 還有一個沒放上投影片、但被問到要答得出來的隱藏成本：`kLldpFreshSeconds = 12.0` 是
> **C++ 常數**（`DeviceConfigurationAndPowerManager.hpp:259`），beacon 減半會讓
> **交換機**存活判斷的相對容忍度變兩倍——要維持比例得改 C++ 重編。
>
> **③ 的 seam 已經在了**（topo 的 `bmv2_binary_override`，`4b339f2`），所以這條不是「做不做得到」
> 而是「敢不敢把預設換掉」。**解鎖兩件現在量不了的事**：TE 的 70% 壅塞門檻（stock 上物理不可觸發）、
> 多流併發下的遙測精度。判準寫成「整套測試通過」是因為**換交換機 binary 就是換掉每一層依賴的時序**。
>
> ### v4.6 的六項，落地情形
> 1. ✅ **raster `ar` 改 `2480 / 880`**、**decomposition 改 `1920 / 980`**。
>    🔵 `figurePage()` 新增**寬圖模式**：`ar > 2.5` 時左右邊界縮到 0.4"（`maxW` 12.53）、
>    垂直留白**上 34% 下 66%**（不平均分配）。這是照 F 節那句「raster 最不適合縮小」做的。
> 2. ✅ decomposition 換圖後，Page 26 的文字本來就已經寫成 `OVS 3.29× / P4 1.21×`，一致。
> 3. ✅ **「40 次」**：副標與內文都已是 forty runs。**再加一句它是篩選不是目測**——
>    raster 只收「恰好一個 >1 s 缺口」的 run，40 份全數入選。這句放在右欄 `What makes these hold`
>    裡（放內文會把 `What separating the variables shows` 那段擠掉，實測過）。
> 4. ✅ **per-hop 只有 2 跳**：答案寫進 Page 35 右欄 `Why the two cells are comparable` 的結尾，
>    講法照 Page 39b——**每一格是各自內部的比較，不是拿 P4 的跳去比 OVS 的跳。**
> 5. ✅ Documentation 頁已是 Twenty-four。
> 6. ✅ **Demo 頁改寫**：標題移除 "live"；②補上 **Web-GUI 是唯讀的**，改狀態要在 Mininet CLI；
>    ③改成 Up → Unknown（beacon 還新鮮）→ Down（beacon 過期）；
>    底部註記改為 **`Recorded, not performed`**，並寫出理由（這些失效模式對時序敏感，
>    現場做是在展示運氣不是展示系統）。
>
> ### 頁碼影響
> **43 → 44 頁。** 新頁插在 Future work 之後、References 之前，所以
> **Outline 的四個 `pp.` 範圍不受影響**（它們只涵蓋到 p.40）。收尾變成 41–44。

---

> ## 🔵 v4.6 修訂摘要（2026-08-19，Adam 六項提問的處理結果）
>
> 1. 🔴 **`page36_failover-raster.png` 少了 P4/128 那一格**——box plot 早就有,raster 沒有,
>    因為它**自己留了一份目錄清單與檔名分類器**。兩張圖現在共用 `failover_key()`（commit `ec918eb`）。
>    ⚠️ 那份重複的分類器還有陷阱:`p4_128_run*.log` 也滿足 `startswith("p4_")`,
>    **只補目錄不改順序的話,十份 128-host 的 run 會被安靜地併進 4-host 那格**——
>    那會是一張**錯的**圖而不是一張不完整的圖。
> 2. 🔴 **`page36_failover-decomposition.png` 已改版**。舊版「資料面 1.15×」＋副標「注意它們有多小」
>    **在量完第四格之後是錯的**:資料面在 128 台上是 3.12×,拓撲在 P4 上只有 1.21×。
>    **兩個乘數都沒有單一值**,現在各畫兩根。
> 3. 🔴 **「23 次量測」全部更正為 40 次**（四格 × n=10）。原本散在五處,包括
>    「23 次全數通過 netem 驗證」「這 23 次能站得住的原因」。
> 4. ✅ **per-hop 圖 P4 只有 2 跳**:已查證是拓撲造成（見 Page 39b），**Adam 裁定不重跑**,
>    改為在 Page 39b 與 F 節都寫清楚該怎麼回答。
> 5. ✅ **Page 33「What was written down」查證通過**:`doc/*.md` 目前確實 24 個,
>    頁上點名的 11 份文件**全部存在**。
> 6. ✅ **demo 錄製流程已寫成獨立 runbook**（見 Page 41）。**v2 全部改用平常在用的介面**
>    （Web-GUI 看、Mininet CLI 改、NTG 打流量），鏡頭前不再有長指令。
>    🔴 v1 有兩條指令是錯的（打到不存在的 host、量測腳本漏參數），錯法與原因記在 runbook 開頭。

> ## 🔵 v4.5 修訂摘要（2026-08-19 深夜，**deck 已重生為 43 頁**）
>
> **這一版的意義**：v4.4 之前的每一版都是「文件改了、投影片還沒跟上」。v4.5 把 v4.4 的
> 全部裁定實作進 `NDTwin_deck.pptx`，並執行 Adam 當場給的九項精簡。**兩邊現在是對齊的。**
>
> ### 落地的結構改動
> 1. **第 2 節（baseline defects）整節從投影片移除**（節封面＋5 頁）。內容仍保留在本文件 C 節。
> 2. **第 3 節拆解**：技術棧 → 開場（Page 8，接在 Architecture 後面）、方法論 → 測試節開頭（Page 20）。
> 3. **節次重編為四節**：`0 Background`／`1 New capabilities`／`2 Test tooling and documentation`／
>    `3 Measured results`。節封面剩四張（其中 Background 那張）。
> 4. **「Results on real hardware」全數改為「Measured results」**（沒有實體設備）。
> 5. 刪除三頁：`What changed, file by file`、`Robustness: defects in my own code`、`Four smaller pieces`。
> 6. 新增四頁文字頁：`Synthesised telemetry against native`（39b）、`Future work`、`References`，
>    以及技術棧移位後的獨立頁。
> 7. 🆕 **八張圖各自獨佔一頁**（Adam 2026-08-19 裁定）。**圖檔本身已內建標題與副標，
>    所以圖頁不放頁標題**，只有左上角節次標記與右下角頁碼。內容口述。
>
> ### Adam 當場給的九項精簡（全部已執行）
> | # | 要求 | 落地方式 |
> |---|---|---|
> | 1 | 整體廢話太多，有些地方只留粗體條列標題 | 各頁 body 縮短；`listItem` 間距由 1.10/1.12 一律提到 1.24 |
> | 2 | 刪 `What changed, file by file` | 已刪。Page 8 的四類彙總仍在 |
> | 3 | Liveness 只講「現在怎麼偵測」，不提原本實作與 bug；拿掉右邊 three states | 改為**三欄版型**，三欄分別是 round-trip 探測／LLDP beacon／Unknown 是獨立判定 |
> | 4 | Failover 只講用到的技術，不講改之前；刪 `Measured on the live stack` 表 | 左三條＋右一則 fault-model 註記。數據全部移到量測節 |
> | 5 | Phase 7 的 live 驗收數字講不清楚 | kv 標籤改成完整句：`The switch was held off for` / `From power-on to fully re-adopted` / `The graph was sampled at 10 Hz for` / `Readings that wrongly showed it up` |
> | 6 | 刪 `Two defects in my own code` | 已刪（也符合「不講自己造成的 bug」） |
> | 7 | 刪 `Four smaller pieces` | 已刪 |
> | 8 | 五層架構頁刪掉底下三則註記 | 已刪；表格 rowH 放大到 0.40/0.66 補版面 |
> | 9 | Phase 7／Liveness／What the suite contains 的副標改成「介紹這頁在做什麼」 | 見下方各頁。範本句型＝「事實 → 所以這頁量/做什麼」 |
>
> ### 連帶必須處理、已處理的
> - **封面副標 `— and the baseline defects it exposed` 已作廢**（第 2 節撤掉了），改為
>   `— a second data plane, with nothing above it changed`。
> - **方法論頁兩個交叉引用指向已刪頁**：`page 24`（第 2 節）與 `pages 16 and 20`。
>   已改為 180.75 s × 3 的實例與只指 page 16。
> - **Outline 改為四列**，頁碼範圍 `4–9 / 11–18 / 20–23 / 25–40`。
> - 節封面說明句與 Outline 該列**逐字相同**（E4c 規定）。
> - Documentation 頁「Twenty-three documents」→ **Twenty-four**（`ls doc/*.md` = 24）。
> - 技術棧頁 GTest `579` → **603**；並刪掉 protobuf 那則長註記（屬第 1 項精簡）。
>
> ### 🔴 這一版的產生器改動（結構性，不要退回去）
> **頁碼改成自動計數**：`newSlide()` 遞增 `PAGE`，`pageNum(s)` 不再收參數。
> 之前每頁寫死 `pageNum(s, 37)`，只要插一頁就要手改幾十處——這正是 v3→v4 頁碼出錯的成因。
> ⚠️ **Outline 那頁的 `pp. x–y` 仍是寫死的**，改結構後要回頭對一次（渲染後數頁碼即可）。

---

> **v4.4 修訂摘要（2026-08-19 深夜，Adam 逐項裁定）**
>
> 1. 🔴 **第 2 節「Baseline defects fixed」延後到下下次報告**——尚未與學長姐對帳，而今天正好有一條歸因被實測推翻。見 C 節前的專節。
> 2. 🔴 **第 3 節「使用技術」拆解**：技術棧→開場、方法論→測試節。節次要重編。
> 3. 🔴 **「實機測試／Results on real hardware」全部改掉**——這次沒有實體設備，全是 Mininet/bmv2 模擬。改為「量測結果／Measured results」。
> 4. 🔴 **Page 24 全頁改寫**：291 秒移出簡報（它量在我們自己的中間版本上），改用實測的「繼承版從不重繞」180.75 s × 3。`034da18` 那段搬到 Page 19 並已寫入。
> 5. 🆕 **P4 在 128 台上測了**（原本刻意不做的第四格）：n=10、16.59 s，**對照 OVS 的 51.75 s 差 3.12×且零重疊**。這推翻了「資料面是三項裡最小的」。
> 6. 🆕 **開機時間對照**、**API 延遲 vs baseline（沒有回歸）**、Page 15 引用更正、Page 44 併發那條補上 renew 的 TTL 缺口。
> 7. **8 張圖**在 `figures/`，全部由 `plot_figures.py` 從已 commit 的資料重算。

> **v4.3 修訂摘要（2026-08-19 晚）**
>
> 1. 🆕 **新增 Page 39b「遙測精度：合成的（P4）對原生的（OVS）」**——**這是新量的實驗**。
>    結論：**合成的遙測和原生的一樣無偏**，而且**散布沒有超過取樣理論地板**。
>    Page 39 原本寫的「本次只量 OVS」**已作廢**。含一個誠實的未解點（P4 散布一致低於地板，機制未明）。
> 2. 🆕 **新增 Page 43 參考文獻頁**。原本整份 42 頁**只有 1 個文獻引用**，
>    而 Page 39 整頁論證「誤差＝理論地板」卻沒標那個理論的出處——這是最大的缺口。
> 3. 🆕 **新增 Page 44 Future work**。原本 Page 42 只有 known limitations
>    （「你還欠什麼」），沒有 future work（「這件事往哪走」）。三條，層次不重複。
> 4. ✅ **五張圖已產出**，在 `figures/`，全部由 `doc/audit/2026-08-19_p4-sflow-accuracy/plot_figures.py`
>    從**已 commit 的原始資料**重新算出來——圖可以追回產生它的那一輪。清單見 F 節。
> 5. ⚠️ **仍未做**：B 節增刪行數表、Page 8、Page 9 還是 08-16 量的。
>    `count_lines.py` 現已救回 `generator/`（原本只在 Claude session 沙箱裡），所以這件事現在做得了。
**當前 repo 狀態**：HEAD **`cc249c8`（2026-08-19 21:06）**，`28b8b13..HEAD` 共 **377** 個 commit。repo 位置：`/home/adam/Desktop/NDTwin-Kernel`。
**簡報場合**：指導教授／實驗室進度報告。**投影片內容用英文**，口頭報告用中文。**實際產出 44 頁**（含 8 張整頁圖），可依報告時間刪減（每頁備註有標「可略」的優先刪）。

> **v4.2 修訂摘要（2026-08-19，round 4 實測＋sFlow 準確度量測之後）**
>
> 1. 🆕 **Page 39 從空殼補成完整一頁。** 原本寫「【Adam 後續提供】：誤差曲線、邊界條件表」——
>    那兩樣現在都量到了：跨 **430× 窗長 × 10× 負載**，孿生**無偏**（中位數比值 0.97–1.02）
>    而誤差**就是** `196√(1/c)` 的理論地板。⚠️ 頁內明寫「不要說我們準確到 X%」並給了替代講法。
> 2. 🆕 **Page 42 新增三條未完成**（電源開機回成功卻沒動作／P4 proxy 重啟摧毀規則／
>    單引號讓 kernel 指控健康元件），並把完整清單指向新建的 **`doc/KNOWN-ISSUES.md`**（17 條）。
> 3. 🆕 **Page 42 新增一條被推翻的「重大缺陷」當方法論講**：兩個獨立模型都判 CRITICAL 的
>    6633/6653，實測是它們錯的（Ryu 為向後相容多綁一個埠，而**這件事 repo 裡沒有記載**）。
>    一般性結論：**只讀原始碼會系統性高估缺陷。**
> 4. ⚠️ **仍未做**：B 節的增刪行數表**還是 08-16 量的**，而 HEAD `04b8933` 之後又有 commit。
>    Page 8／Page 9／B 節要一起重跑 `count_lines.py`，這是 v4.2 沒動的唯一大項。
>
> **v4.1 修訂摘要（2026-08-18 晚，四輪 live 實測之後）**
> 1. 🔴 **Page 42 的佇列式端點條目有一句事實錯誤，已更正**：「派送結果只寫在 kernel log 裡」
>    只對 P4 成立。OVS 側送一條會被拒絕的規則，整份 log 16,324 行 0 個 error，
>    **任何地方都沒有紀錄**。成因寫在該條目內。
> 2. **數字重量（`04b8933`）**：HEAD `7e0295b`→`04b8933`、commit 336→**373**、
>    `p4_proxy/tests` 16 檔/438→**17 檔/453**、`tests/python` 236→**243**。
>    gtest **47 檔 / 603** 不變。⚠️ **B 節的增刪行數表仍是 08-16 量的，動筆前要重跑 `count_lines.py`。**
> 3. **Page 36 的 TE 門檻宣稱今天再次佐證，可換成更具體的數字**（未改，留給動筆時決定）：
>    OVS 上 `congested link 8 -> 3`、單一 elephant flow **749 Mbps / 1 Gbps = 74.9%** 越過 70% 門檻，
>    同一輪 TE 實際裝規則 **15 次**。比原文「已實測成功觸發」硬。
> 4. **刻意不加**（Adam 2026-08-18 裁定「有點 trivial」）：OVS 寫入路徑結構上無法回報失敗、
>    而 P4 可以，這個差分不進簡報。**Mininet 忽略 `bw>1000` 導致 16/160 介面從未整形**
>    也不進（NTG 的 repo，且功能面無受害者）——兩者都留書面報告。
>
> **v4 修訂摘要（2026-08-18）**
> 1. 🔴 **Page 34（舊 34）的 P4-vs-OVS 對照表整張作廢**。舊表的 P4 欄跑 4 台 host、OVS 欄跑
>    128 台，而且 OVS 側跑的是尚未修復的碼——**三個變因同時在動**，caption 的「差異來自實作
>    而非設定」是不成立的歸因。改用 2026-08-17 的控制實驗：同一張拓撲、23 次量測、
>    **P4 快 2.0 s（13%），p=0.0098，95% CI 0.55–3.50 s**。
> 2. 🔴 **Page 24（舊 25）④ 同樣作廢並改寫**為「修復前後、同一張拓撲」的對照
>    （291 s 永不自癒 → 50.1 s 自己復原），並新增 ⑤ 說明混淆因子是怎麼被找出來的。
>    **⑤ 本身是加分項**：它展示的是「在自己的頭條數字裡找到混淆因子並重做實驗」。
> 3. **第 2 節由 10 頁壓縮為 5 頁**（Adam 2026-08-18 裁決，理由是**學長姐會在場**）：
>    舊 18 前提翻案 ＋ 新增的「baseline 是什麼」合併為新 Page 22；舊 19–24 六頁的逐條缺陷
>    壓縮為新 Page 23「五種重複出現的形狀」；舊 25→20、舊 26→21、舊 27→22。
>    **完整缺陷清單移到書面報告。**
> 4. **A1.1 的「既有系統一句話帶過」作廢**——Page 22 上半要具體交代 baseline 的規模。
>    這是本次改版要修掉的核心不對稱：一句話功勞對一整節缺陷。
> 5. **頁碼全部重編：40 → 35 頁**。舊 28–40 一律減 5。C 節內交叉引用已同步更新。
> 6. Page 25 新增 2026-08-17 找到的一條 baseline 缺陷（`setupNFSForApp` 提早 return）。
>
> **v3 修訂摘要**
> 1. **語言**：投影片改為**全英文**（v1/v2 原寫「中文為主」，已作廢）。與 agent 的對話用中文。
> 2. **視覺風格**：極簡風——白底、單一強調色、以編號條列為主軸。完整規格見新增的 E 節。
> 3. **新增兩頁在最前面**：Page 8「Scale of the work」（四類增刪行數）與 Page 9「What changed, file by file」（kernel 與 proxy 逐檔明細）。
> 4. **第 1 節新增兩頁**：Phase 7 電源管理（v2 的 12b）與穩健性頁（readopt 清表 ＋ event-loop 阻塞）。
> 5. **第 2 節新增兩頁**：後期測試輪發現的 baseline bug，獨立呈現（Adam 2026-08-16 裁決）。
> 6. **頁碼全部重編**：33 → 42 頁。C 節內所有交叉引用已同步更新。
> 7. **數字全部重量**（2026-08-16），見 B 節。行數一律扣除註解與空行，口徑見 E4。
> 8. **2026-08-16 全部做完**，逐頁渲染檢查通過。每頁的實際版型與踩過的坑寫在 C 節各頁的 ✅ 條目與 E5。
> 9. **2026-08-18 在最前面插入兩頁架構圖**（Page 5 原圖、Page 6 加上 P4 之後），因此原 Page 5 起全部後移兩頁。兩張都以 pptxgenjs 照原座標重畫，共用 `archTop()`。
> 10. **2026-08-18 重排與增刪**（Adam 裁決）：刪掉「One task became two workstreams」與「Typed dispatch, and one interface per concern」兩頁；兩張整體架構圖從最前面移到 Background 之後、`Architecture: how P4 attaches` 之前；`Scale of the work` 與 `What changed, file by file` 移到 `Architecture` 之後；P4 pipeline 後面新增 `Inside the pipeline` 詳圖。投影片 42 → 41 頁。
> 11. **2026-08-18 加入節封面頁與 Outline 的第 0 節**（Adam 裁決）：每一節前面插一張封面頁（含 Background），Outline 多一列 `0 Background`。投影片 41 → 47 頁。封面頁規格見 E4c。
> 12. **2026-08-18 `Typed dispatch` 頁刪除後的殘留**：headless 啟動已收到 Page 31 底部（見該頁）。**`SwitchKind` typed dispatch ＋ 兩個 strategy 介面尚未安置**——Page 7 的架構頁只講 proxy 模仿 Ryu，沒講 kernel 內部怎麼分派。待 Adam 決定要收到哪裡，或確認不講。
> 13. **2026-08-18 第 2 節改寫**（Adam 裁決）：10 頁壓縮為 5 頁，主張從「修復的 baseline bug」改為「建立一個可信的參照點」。**投影片尚未跟上**，見 C 節開頭的同步狀態表。

---

## A. 生成簡報前必讀的規則

### A1. 範疇（已與 Adam 確認，不要重問）

1. **基準就是 `28b8b13`——Adam 做的所有東西都建立在它之上，不必再確認。** 這是實驗室前人上傳的完整 OVS/Ryu 系統；Adam 的工作從 2026-07-23 的 `6f32bca` 開始。所有 diff、行數、commit 數一律用 `28b8b13..HEAD`。
   ⚠️ **2026-08-18 修訂：「既有 OVS/Ryu 產品只當背景一句話帶過」已作廢。**Page 22 上半要**具體交代 baseline 的規模與完整度**（76 檔、45 個 C++ 原始檔、約 13,200 行、41 個 `/ndt/` endpoint、七個元件靠它）。理由見第 2 節開頭：學長姐在場，而一句話功勞對一整節缺陷是本次改版要修掉的不對稱。
2. **只講 NDTwin-Kernel 這個 repo**。其他 workspace repo（Energy-Saving-App 等）的修復一律不進簡報。
3. **不提 AI 協作開發流程本身**。mutation testing 只講方法論（「每個測試都親眼看它失敗過一次才算數」），不講用什麼工具、怎麼執行。
4. **第 5 節（量測結果與 demo）採預填骨架**：每頁有實驗名稱、一句話結論、素材出處；還缺的視覺化標 `【Adam 後續提供】` 留白。
5. Bug 部分**只講 baseline 既有的 bug**，不講 Adam 開發過程中自己引入又修掉的。分類裁定見 A2，照表執行，不要自行重新分類。
   ⚠️ **2026-08-18：第 2 節由 10 頁壓縮為 5 頁**（見該節開頭的改版說明）。A2 仍然有效，但它現在決定的是「哪一條可以被當作 baseline 缺陷引用」，**不再是「放第幾頁」**——表格右欄的頁碼已重新對應，僅供索引。**完整缺陷清單移到書面報告，簡報不逐條列。**
6. **投影片全英文**。中文只用於與 Adam 的對話。`doc/HANDOFF.md` 等中文素材必須完整翻譯，不可留中文殘句。

### A2. Bug 歸類裁定表（已逐條查證，直接沿用）

判定規則：bug 所在的程式碼／行為必須**早於 `6f32bca` 就存在**才算 baseline bug。查證方法是直接讀 baseline tree（`git show 28b8b13:<path>`），不是看 CHANGELOG 敘述。

**排除（不進 bug 頁）**：
| 項目 | 排除理由 |
|---|---|
| SIGFPE flow-rate divide-by-zero（branch 名稱的由來） | Adam 在 `6f32bca` 自己把 guard 拿掉、`31b357a` 自己修回來。不是 baseline bug |
| bmv2 存活偵測早期版本無條件回報 up | 該程式碼本身就是 Adam 新寫的，沒有既有版本可比 |
| proxy `calculate_all_paths` 併發 race（`fbd8140` 修） | 在 Adam 自己新寫的 proxy 程式碼裡 |
| `describeCommandStatus` 指錯工具名（`1b50982` 修） | 該 helper 是 Adam 在 `ab7d0bb` 新增的，搬進 utils 後才指錯 |
| OpResult 被 Controller 丟棄（`8c25dbc` 修） | OpResult 是 Adam Phase 2 自己加的機制，這是補完自己的功能，放功能頁 |
| **readopt 清表回報 success**（`a72a168` 修） | 缺陷在 Adam 自己寫的 proxy 碼裡，同 OpResult 先例。放**穩健性頁 Page 19** |
| `3292653` | ⚠️ 它的 commit message 與 Page 23 ④ 對 graph 行為的描述**互相矛盾**。動筆前必須擇一，不要兩處都寫 |

**2026-08-13 新增裁定**（`fbd8140..2cb70e0` 這 69 個 commit，逐條對 baseline tree 開檔驗證過）：

| commit | bug | 為什麼算 baseline | 放哪頁 |
|---|---|---|---|
| `034da18` | 🔴 **2026-08-19 重新裁定，見下方專節。舊裁定「baseline 缺陷、本節最強的一條、Page 24 獨立一頁」已作廢。** 291 秒這個數字**不進簡報**（Adam 2026-08-19） | ——（原文保留於下方專節，含推翻它的證據） | **改放 Page 19 穩健性頁** |
| `f21d7a0` | 缺欄位的請求打死 kernel | baseline 檔案 | Page 23（Crash 類第 4 條）|
| `57346f6` | OpenAI API key 被寫進 log | baseline 檔案。⚠️ **這是產品自己的 Intent Translator 在用 OpenAI，不是 A1.3 禁止的「AI 協作開發流程」**——不加這句註記會被誤判成違規而整條砍掉 | Page 25 |
| `cbb504a` | 丟棄 `boost::edge` 的 found 旗標 | baseline 檔案 | Page 25 |
| `5054249` | VLAN 欄位名不符（未引爆的地雷） | baseline 檔案；issue #3 已立案，簡報只講不修 | Page 25 |
| `59dc5d3` | 十台 switch 共用一個插座 | baseline 檔案 | Page 25 |
| `ee7233b` | 一個功能在五個層次同時是死的 | baseline 檔案 | Page 25 |
| `916d330` | **要拆一半**：power 半邊算 baseline 列入 Page 25；OpResult 半邊照 `8c25dbc` 先例排除，放功能頁 | | Page 25（半） |
| `1a7d815` | **要拆一半**（Adam 08-13 裁決）：kernel 的 `/stats/flow/<dpid>` 請求沒有 `--max-time`，**baseline `28b8b13:src/…/DeviceConfigurationAndPowerManager.cpp:507` 就是這樣**，`6f32bca` 只是把寫死的 `RYU_IP_AND_PORT` 換成變數 → **這半列入 Page 23**。event-loop 阻塞那半在 Adam 自己的 proxy 碼裡 → 排除，放**穩健性頁 Page 19** | | Page 23 + Page 19 |

⚠️ **`1a7d815` 兩頁講的是同一條缺陷的一體兩面，必須交代清楚，否則聽起來像重複計數。**

**原有列入項**（皆已對 `28b8b13` baseline tree 驗證或屬 baseline 檔案）：見 C 節 Page 23–26。其中兩條有出處註記：
- **null-translator crash**：baseline `main.cpp` 不用 AI 時就把 translator 設 `nullptr`、baseline `HttpSession::handleInputTextIntent` 無 guard 直接解參考（已驗證 `28b8b13` 兩處原文）。Adam 的 `--no-ai` 讓它變成預設組態而曝光。→ 列入。
- **route recompute（`2c81b26`）**：`intelligent_router.py` 不在 `28b8b13` tree 裡，是隨 `6f32bca` 帶進 repo 的實驗室既有 Ryu 控制程式。缺陷邏輯（整支檔案沒有 `remove_edge`）是既有的。→ 列入，但註明「既有 Ryu 控制程式的缺陷」。

### A2b. 每個實測數字都要標它量在哪個 commit（2026-08-18 新增）

**規則：實測數字寫上投影片或寫進本檔時，把當時的 commit 標在旁邊。**
`51.8 s (b6b75fa)`、`13.7 s vs 15.7 s (9467ea0)`、`585 tests / 79 suites (13e53df)`。
⚠️ **這個範例自己就示範了為什麼要標**：原本寫的是 `50.1 s (9467ea0)`，那是 n=3 的平均；
08-19 補到 n=10 之後是 51.8 s。**標了 commit，才看得出兩個數字不是矛盾而是不同輪次。**

量測只對產生它的那版程式成立，而程式會動。沒有 commit，讀的人分不出「現況」和「歷史」，
過期的數字就會被一直當成系統的性質引用。**這條規矩是被咬出來的**：
「OVS 斷鏈黑洞 291 秒零自癒」在修好它的 `034da18` 落地之後**又被引用了四天、散進 11 個檔案**，
而且**這份簡報模板就是其中之一**（v3 的 Page 29 ④ 與 Page 41 對照表，v4 已作廢改寫）。

同一天還有第二個實例：C++ 基準線 `579 tests / 78 suites` 寫下後幾小時就被當天的 commit 追過。
兩個都是寫的時候完全正確。**標 commit 防不了數字過期，它防的是下一個人看不出它過期了。**

repo 側的完整版見 `doc/audit/README.md`「Every measured number carries the commit it was measured at」。

### A3. 事實查證規則（前幾輪踩過的坑，必遵守）

1. **所有數字動筆當下重新量**，不要沿用本文件或任何文件裡的數字。B 節的數字是 2026-08-16 量的，之後 repo 還會動。指令：
   - gtest 數：`grep -rhE '^(TEST|TEST_F|TEST_P)\(' tests --include='*.cpp' | wc -l`
   - Python 測試數：`grep -rh 'def test_' p4_proxy/tests | wc -l` 與 `grep -rh 'def test_' tests/python | wc -l`
   - commit 數：`git log 28b8b13..HEAD --oneline | wc -l`
   - **增刪行數**：用 `count_lines.py`（見 E4），不要用 `git diff --shortstat`——它含註解與空行，會虛胖約 40%。
   - ⚠️ **這個 repo 每天都在動**（08-11→08-13→08-16 三次量測，commit 數 202→286→336）。動筆和產檔之間如果隔了幾小時，就再量一次。
2. **CHANGELOG 的高層敘述不可信於 bug 來源分類**，只能當素材索引；分類一律以 A2 為準。CHANGELOG 上次更新是 `850c2f2`（08-08），之後的 commit 不在裡面，素材要直接讀 `git show <hash>` 的完整 message——這個 repo 的 commit message 寫得極詳細，是最好的素材來源。
3. **不要用 author date 推時間順序**（本 repo 的日期不單調）；要用 DAG（`git merge-base --is-ancestor`）。
4. **身份**：`Adam010341`（兩個 email 都是他本人）；`patty`/`joemou`/`JM`/`xxxPatty` 是實驗室前人；CHANGELOG 裡 v3.x–v4.3 各 tag 的敘述是文字紀錄，不是本 repo 的 git tag（實際只有 `v1.0.0`）。
5. **狀態文件會過期**：`doc/HANDOFF.md`、`doc/test_coverage_gaps.md`、CHANGELOG 底部統計都有過期紀錄。引用前對 `git log --since` 檢查有沒有更新的事實。

---

## B. 已查證的關鍵事實（2026-08-16 重量，可直接引用）

- **時間軸**：baseline tree = `28b8b13`。Adam 第一個 commit `6f32bca`（2026-07-23）。至 **2026-08-18 HEAD `04b8933`，`28b8b13..HEAD` 共 373 個 commit，全部是 Adam**（08-16 `bb9aa7e` 時是 336）。
  **已核實 `28b8b13` 是精確的分界，不是近似值**：`git log --format='%h %p' -1 6f32bca` 顯示 `28b8b13` 是 `6f32bca` 的 **direct parent**。**`9626b2a`（repo 真正的第一個 commit，2 行 README）不是 baseline**——它跟 `28b8b13` 之間還隔了 36 個 commit，是實驗室前人建置完整 OVS/Ryu 系統的過程；用它當基準會把那整段既有系統的建置史誤算成「新增」。
- **工作的兩條主線**（CHANGELOG L371-441 的框架，簡報敘事骨幹）：原本假設「baseline 功能正確，P4 是純新增」，實測發現 **baseline 有 11 個既有缺陷、且全部無聲**（不 crash、不留 log、每個 endpoint 都回 200）。所以工作變成兩件事：P4 支援 ＋ 修好共用路徑——因為「一個會說謊的 baseline 無法拿來驗證新的資料面」。
  ⚠️ 「11 個」是 08-11 那次盤點的數字；08-13 之後又新增 8 條裁定（見 A2），簡報上若要給總數，動筆時重數並說明是哪一輪的盤點。
- **增刪行數** 🔵 **2026-08-19 重量於 `cc249c8`**（扣除註解與空行，全部來自 `count_lines.py` **單一次計算**）：

  | 類別 | 檔案 | 新增（程式碼） | 刪除（程式碼） | 含註解的原始值 |
  |---|---|---|---|---|
  | Documentation | 207 | **+46,290** | −5 | +55,448 / −6 |
  | Tests & tooling | 117 | **+25,148** | 0 | +37,289 |
  | Kernel (C++) | 56 | **+6,068** | −1,053 | +10,195 / −1,262 |
  | P4 proxy | 26 | **+4,431** | 0 | +6,463 |
  | **Total** | **406** | **+81,937** | **−1,058** | +109,395 / −1,268 |

  ⚠️ **doc 從 122 檔 / +26,691 跳到 207 檔 / +46,290 是真的**，不是量錯：08-17 之後
  `doc/audit/` 下每一輪實測都留了完整紀錄（raw log、分析腳本、REPORT.md）。
  簡報上不必解釋，被問到就講「量測紀錄與原始資料都進版控」。
  Kernel 那 56 檔中有 **3 個設定資料檔共 +1,852 行**（兩份 topology JSON ＋ `node_positions_p4.json`）；
  扣掉後 kernel 原始碼為 **53 檔 / +4,216 / −1,053**。
  🔴 **v4.5 起 `What changed, file by file` 那頁已刪**，所以兩種口徑不再同時出現在投影片上，
  Page 8 用的是含設定資料的 56 檔版本。逐檔明細仍在 `line_counts.json`。
- **逐檔明細**（Page 9 用；完整清單見 `line_counts.json`，動筆時用 `count_lines.py` 重跑）。前幾大：
  - Kernel：`DeviceConfigurationAndPowerManager.cpp` +549/−150、`TopologyAndFlowMonitor.cpp` +454/−96、`FlowLinkUsageCollector.cpp` +442/−168、`HttpSession.cpp` +329/−234、`include/utils/Utils.hpp` +211/−28、`main.cpp` +210/−37、`ApplicationManager.cpp` +160/−64
  - Proxy（全新，24 檔）：`topology_manager.py` +912、`p4_client.py` +487、`p4_testbed_topo.py` +373、`sflow_emitter.py` +326、`p4runtime_mastership_probe.py` +325、`ndtwin_switch.p4` +306、`ryu_topology.py` +257、`api_routes.py` +247、`main.py` +171、`kernel_notifier.py` +146、`ryu_flow_stats.py` +135、`ntg_bmv2_topo.py` +120，其餘為 SPEC.md 與 `reference/` 下的工具腳本
- **P4 支援各 Phase 狀態**（2026-08-13 重新核對 `doc/p4_bmv2_support_plan.md`）：Phase 0–2、4 完成；Phase 5 flow-sample 半邊完成並對 golden capture 驗證（counter-sample 半邊未做——但這與 OVS 行為對等，MININET 模式本來就丟棄 counter sample）；**Phase 6 六項全部完成且 failover 端到端驗證完畢**（`ca72d22`）；**Phase 7 已完成**（電源機制、helper 安裝、live 驗收都過，見 Page 18）；**Phase 8 已完成**（散落腳本已搬、requirements 已修、CHANGELOG 已補、shell injection 已開 issue #2）；**Phase 3 未開始**（唯一還沒動的）。
- **測試資產（2026-08-18 重量，`04b8933`）**：`tests/` **47** 個 .cpp、**603** 個 gtest case；`p4_proxy/tests/` **17** 個 `test_*.py`、**453** 個 test function；`tests/python/` **7** 檔 **243** 個（未註冊進 ctest，獨立執行）；`tests/shell/` **7** 支。
  （08-16 `bb9aa7e` 時是 46 / 579 / 16 / 438 / 236，兩天內被追過——這正是 A3.1 要求動筆時重量的理由。）
  ⚠️ 五天內從 426→547→579 gtest 是真的成長不是量錯：08-12/13 的整夜測試輪為三個實測缺陷各補了迴歸測試，並新增 fuzz harness、P4 覆蓋閘門、故障注入 harness、twin 對帳工具四組工具與其測試。
- **架構關鍵決策**：P4 proxy agent 模仿 Ryu 的北向 API ＋ 自行合成 sFlow v5 打進 kernel 既有的 UDP:6343 collector，所以 **kernel 的上層（Classifier、FlowLinkUsageCollector、全部 `/ndt/` API、7 個外圍應用、Intent Translator）一行都不用改**。

---

## 🔴 第 2 節「Baseline defects fixed」——**延後到下下次報告**（Adam 2026-08-19 裁定）

**這一節（Page 21–31，含節封面）暫不上台。** 頁面內容全部保留在本文件裡，不要刪。

**理由（Adam 提出）**：這些缺陷**還沒跟寫這些程式的學長姐確認過**，直接在他們面前逐條列出
歸因，被當場推翻的風險很高。

**今天的工作證實了這個顧慮不是多慮**：

1. 🔴 **這一節最強的一條（`034da18`）歸因在 2026-08-19 被實測推翻。**
   原本寫「既有 Ryu 控制程式的缺陷」，實際上讓那行程式碼**構得到**的兩個條件
   （`remove_edge` 與週期性重算）**都是我們自己的 `2c81b26` 帶進來的**。
   詳見 `doc/audit/2026-08-19_failover-provenance/REPORT.md`。
2. **A2 裁定表上二十幾條全部是「讀 baseline tree 推斷」**，沒有一條跟原作者對帳過。
3. 本專案已有明確前例：**「只讀原始碼會系統性高估缺陷」**——6633/6653 那次
   兩個獨立模型都判 CRITICAL，實測是它們錯的（見 Page 42）。

**⚠️ 連帶要處理的**：
- Outline（Page 2）的五節與頁碼範圍要重編，節封面少一張，第 3–5 節頁碼前移。
- 第 2 節撤掉後，**簡報的敘事只剩「新增能力」一半**。Page 22 原本要交代 baseline 規模與
  完整度（A1.1 的修訂），那段仍然需要，只是不再是缺陷節的開場。

🔑 **建議的折衷（未裁定，供 Adam 決定）**：保留**方法論**而不做**逐條歸因**——
講「我們建立了一套能發現無聲缺陷的方法，以下是它抓到的**形狀**」（五種重複出現的型態、
綠燈與失敗可以同時存在、無聲失敗的三個方向），但不宣稱「baseline 有這 N 個 bug」。
這樣不需要事先對帳，也保住第 2 節的敘事功能。**Page 23「五種重複出現的形狀」正好已經是這個形狀。**

---

## C. 逐頁大綱

### 🔵 C0. **實際產出的 44 頁**（v4.7，2026-08-20，這是現在 pptx 裡的順序）

> ⚠️ **底下 C1 起的逐頁大綱仍用舊編號**（含已延後的第 2 節）。**要對照投影片就看這張表**，
> 舊編號只當作內容出處的索引。

| # | 頁 | 對應舊編號 | 備註 |
|---|---|---|---|
| 1 | Title | 1 | 副標已改為 `— a second data plane, with nothing above it changed` |
| 2 | Outline | 2 | **四列**，`4–9 / 11–18 / 20–23 / 25–40` |
| 3 | ▎SECTION 0 Background | 3 | |
| 4 | Background: the system, and the task | 4 | |
| 5 | 原始架構圖 | 5 | |
| 6 | 加上 P4 之後的架構圖 | 6 | |
| 7 | Architecture: how P4 attaches | 7 | |
| 8 | **The stack** | 舊 28 | 🔵 從第 3 節搬到開場；去掉節次標記與 protobuf 註記 |
| 9 | Scale of the work | 8 | 數字重量於 `cc249c8` |
| 10 | ▎SECTION 1 New capabilities | 10 | |
| 11 | The P4 pipeline | 11 | |
| 12 | Inside the pipeline | 12 | |
| 13 | The P4 proxy agent | 13 | |
| 14 | sFlow synthesis, and how it was proven | 14 | |
| 15 | The telemetry sample path | 15 | |
| 16 | **Liveness reported from evidence** | 16 | 🟢 **v4.8 全頁流程圖**（`p4LivenessFor()` 的判斷鏈） |
| 17 | **Failover: detect, reroute, recover** | 17 | 🟢 **v4.8 全頁流程圖**（beacon → watchdog → 重算） |
| 18 | **Phase 7: switch power management** | 18 | 🔵 副標與驗收表改寫，見精簡 #5、#9 |
| 19 | ▎SECTION 2 Test tooling and documentation | 舊 30 | |
| 20 | **The methodology is the real technology** | 舊 29 | 🔵 從第 3 節搬進來；兩個交叉引用已改 |
| 21 | **Five layers, five different questions** | 31 | 🔵 底下三則註記已刪 |
| 22 | **What the suite contains** | 32 | 🔵 新副標 |
| 23 | What was written down | 33 | Twenty-**four** documents |
| 24 | ▎SECTION 3 Measured results | 舊 34 | 標題由 `Results on real hardware` 改名 |
| 25 | The P4 path matches the OVS baseline | 35 | 加一行「PASS 量於 `dac192b`」 |
| 26 | **Failover, measured** | 36 | 🔵 四格表（含 P4/128）、無 291 s |
| 27 | 🖼 `page36_failover-boxplot.png` | — | 整頁圖 |
| 28 | 🖼 `page36_failover-raster.png` | — | 整頁圖 |
| 29 | 🖼 `page36_failover-decomposition.png` | — | 整頁圖 |
| 30 | What the data planes can actually carry | 37 | |
| 31 | 🖼 `page37_throughput-ab.png` | — | 整頁圖 |
| 32 | 210 Mbps sustained, then a link broken | 38 | |
| 33 | **How accurate the twin's link usage is** | 39 | 🔵 全頁補齊（誤差曲線表＋量子） |
| 34 | 🖼 `page39_quantisation-ladder.png` | — | 整頁圖 |
| 35 | **Synthesised telemetry against native** | 39b | 🆕 全新頁 |
| 36 | 🖼 `page39_sflow-accuracy-20M.png` | — | 整頁圖 |
| 37 | 🖼 `page39_sflow-accuracy-200M.png` | — | 整頁圖 |
| 38 | 🖼 `page39_per-hop-consistency.png` | — | 整頁圖 |
| 39 | An independent pass over the running system | 40 | |
| 40 | Demo | 41 | |
| 41 | Where it stands | 42 | 🔵 open 清單換成 9 條＋指向 `KNOWN-ISSUES.md` |
| 42 | **Future work** | 44 | 🆕 已定位但未排程的三個結構性問題 |
| 43 | **Planned for the next report** | 45 | 🟢 **v4.7 新增**——下一次要交數字的三件事 |
| 44 | **References** | 43 | 🆕 |

**已從投影片移除**（內容保留在下方）：`What changed, file by file`（舊 9）、
`Robustness: defects in my own code`（舊 19）、`Four smaller pieces`（舊 20）、
第 2 節全部（舊 21–26，含節封面）、第 3 節封面（舊 27）。

---

### C1. 逐頁大綱（舊編號 42 頁，內容出處索引）

> ✅ = 已做進 `NDTwin_deck.pptx`。🆕 = 本文件已改寫但**投影片還沒跟上**。產生器 `build_deck.js`。
> 每頁左上角有節次標記（10.5pt bold、`ACCENT`、y=0.28），例如 `1 · NEW CAPABILITIES`。

> ✅ **同步狀態（2026-08-18 晚）：本文件與 `NDTwin_deck.pptx` 已對齊，兩邊都是 42 頁。**
>
> 這一輪同步做掉的：第 2 節 10 頁 → 5 頁；Page 36 的 P4-vs-OVS 對照表換成 08-17 控制實驗；
> Page 24 ④ 換成「修復前後、同一張拓撲」並加上 ⑤ 混淆因子；數字重量到 `04b8933`；
> Page 42 新增兩條 08-18 的未完成（鎖無持有者、佇列端點無法查詢，含 OVS 連 log 都沒有的更正）。
>
> ⚠️ **`Scale of the work`（Page 8）與 `What changed, file by file`（Page 9）刻意沒更新**
> ——Adam 說後續還會再變。B 節的行數表也還是 08-16 量的，這兩頁動筆前要一起重跑 `count_lines.py`。

### 開場（Page 1–9，Page 3 是節封面）

**Page 1 — 標題頁** ✅

**Page 2 — Outline** ✅
- 五節 + 各節頁碼範圍：新增功能 pp. 8–17／baseline bug pp. 18–22／使用技術 pp. 23–24／測試工具與文件 pp. 25–27／量測結果與 demo pp. 28–34。
- ⚠️ **頁碼範圍寫死在這頁**，後面章節頁數一變就要回來改。

**Page 4 — Background: the system, and the task** ✅
- 左側四段編號條列：① C++ kernel 持有模型（拓撲圖、sFlow 遙測、flow 與 link usage）。② 七個元件依賴它，且**只透過 `/ndt/` HTTP API**——沒有共享記憶體、沒有共享檔案。③ 既有系統驅動 OVS（Mininet + Ryu，實驗室前人開發，一句話帶過）。④ 我的任務：讓同一個 twin 也能驅動 P4/bmv2，而七個元件不必改。
- 右側七個 consumer 清單（名稱 + 語言）＋一行：全部透過 `get_graph_data` 讀圖，那個 endpoint 壞掉七個一起壞。
- 素材：CHANGELOG L9-20；`doc/testing_workflow.md` 的元件依賴表。

**Page 5 — 原始架構圖**（新增，2026-08-18） ✅
- Adam 提供的 `NDTwin_Arch.pptx` 原圖，**照原座標以 pptxgenjs 重畫**，不是插圖片——這樣兩張架構圖是同一組 helper 畫的，風格必然一致，而且都還能編輯。
- 重畫用的 helper 在 `build_deck.js`：`aBox` / `aText` / `aArrow` / `aDash` / `aCloud` / `archTop`。`archTop()` 是兩頁共用的上半部（標題、Apps、Kernel 九宮格、Tools 欄、兩條虛線），**只有下半部不同**。
- 字體 Arial、黑框 1pt、白底，與原圖一致。座標直接取自原始 pptx 的 `<a:off>` / `<a:ext>`。
- 備註：這頁不加任何自己的註解，就是原圖。要讓聽眾先看到「我接手的系統長什麼樣」。

**Page 6 — 加上 P4 之後的架構圖**（新增，2026-08-18） ✅
- 上半部與 Page 5 **完全相同**（同一個 `archTop()`），差別只在虛線以下——這是刻意的，讓聽眾一眼看出「上面沒動」。
- 新增的東西一律用 `ACCENT`（`065A82`）標示：`P4 proxy agent` 框（粗框 1.75pt ＋ 右側小字 `new`）、三個 `bmv2 switch` 框、`P4Runtime` 標籤與箭頭、`Emulated Network (Mininet, bmv2)` 標籤、`sFlow (synthesised)` 標籤。既有的 OVS 那半維持全黑。
- **sFlow 方向與起點（Adam 特別交代，畫錯就毀了整頁）**：
  - OVS 側：箭頭從**雲**往上到 kernel（switch 自己發 sFlow），起點在虛線下方。
  - P4 側：箭頭從 **proxy 框上緣**往上到 kernel，**不是**從 bmv2 雲出來——因為 bmv2 不發 sFlow，是 proxy 合成的。標籤寫 `sFlow (synthesised)`。
  - 兩條都是**單向朝上**（`aArrow(..., "up")`，實作是 `flipV: true` + `endArrowType`）。
  - proxy 另有一條**雙向**箭頭到 kernel，標 `Ryu-compatible REST`。
- 右下角（Tools 欄下方空隙 y≈5.52）放整頁的結論句：`bmv2 emits no sFlow of its own. The proxy synthesises it, so the kernel's collector cannot tell the two fabrics apart.`
- ⚠️ 版面：控制器框放 y=5.32（不是 5.16），才有 0.36" 讓 `Ryu-compatible REST` / `sFlow (synthesised)` 兩個標籤放在 kernel 框**外面**。放 5.16 的話標籤會壓進 kernel 框裡。
- ⚠️ `Physical Network` 那一路**沒有畫**——這次工作沒動它，畫上去只會讓 Ryu 的線跨過 bmv2 雲。若教授問起，口頭說明即可。
- 白底黑字。大標 `P4 / bmv2 Data-Plane Support`；副標 `— and the baseline defects it exposed`；上方小字 `NDTwin Network Digital Twin`（強調色）。
- 下方只留 `Adam · 日期`。**不要**放 commit 數、branch 名、指導教授欄等小字。

**Page 7 — Architecture: how P4 attaches to the existing system** ✅
- 左側三段條列，右側示意圖。
- ① proxy 模仿 Ryu 北向 API。② proxy 合成 sFlow v5 打進 kernel 既有 UDP:6343 collector。③ 結果：kernel 上層、7 個外圍應用、Intent Translator 完全不改。
- **示意圖方向**——由上而下：`7 downstream apps` → `/ndt/* HTTP API` → `NDTwin Kernel (unchanged)`（強調色外框）→ `Ryu controller` | `P4 proxy agent` → `OVS switches` | `bmv2 switches`。箭頭朝上（狀態與遙測上行）。不要加「state & telemetry ↑」之類的說明文字，口述即可。
- 素材：CHANGELOG L11-15；`p4_proxy/proxy_agent/SPEC.md`。

**Page 8 — Scale of the work** ✅
- 四類橫條圖（Documentation／Tests & tooling／Kernel (C++)／P4 proxy），每類顯示 lines added（橫條＋數字）、files、removed，最後一列 Total。
- 副標：`336 commits, 2026-07-23 → 2026-08-16, on top of baseline 28b8b13`。
- 每類下方一行說明：doc＝Runbooks, design/status docs, investigation records；test＝gtest suites, P4-proxy Python tests, the L0–L4 harness；kernel＝39 existing files modified, 16 new；proxy＝All new — P4Runtime client, REST shim, sFlow emitter, P4 pipeline。
- 底部腳註（必留）：`Diffed against baseline 28b8b13. Comment lines, blank lines and build artefacts are excluded; intelligent_router.py is excluded as the lab's pre-existing Ryu controller.`
- **動筆時用 `count_lines.py` 重量**。

**Page 9 — What changed, file by file** ✅
- **只列 kernel 與 P4 proxy 的逐檔明細**（tests 與 doc 已在前一頁彙總，不重複）。格式參考 VS Code 檔案樹：目錄當小標（等寬字、強調色），底下縮排列檔名，右側依序 `NEW` 標籤、`+新增`、`−刪除`。
- 兩欄：左欄 Kernel (C++)，欄標小計 `53 files · +4,077 / −1,038`；右欄 P4 proxy，`24 files · all new · +4,134`。
- 左欄只列 ≥70 行者，其餘摺成一行 `N further files (headers, strategy interfaces, CMake)`。
- 右欄 24 檔，分 `proxy_agent/`、`p4_src/`、`mininet/`、`reference/` 四組。⚠️ 24 檔全列會超出版面，`reference/` 下的小工具摺成一行。
- ⚠️ `setting/` 的兩個 topology JSON（+963）**不列**——設定資料不是程式碼。腳註：`Source files only. Tests and documentation are on the previous slide; the two topology JSON files (+963) are configuration data, not code.`

### 第 1 節：新增功能（Page 10–20，Page 10 是節封面）

**Page 11 — The P4 pipeline** ✅
- 左側三段條列，右側**垂直流程圖**：Parser → `flow_5tuple`（強調色框）→ `ipv4_lpm` → `l2_forward` → Egress。方框高 0.60"、箭頭 0.28"，否則擠出版面。
- ① ternary `flow_5tuple` 帶真正 priority、置於 `ipv4_lpm` 之前，特定 flow rule 贏過預設路由而不靠 table 順序。② ARP/TCP/UDP/ICMP 解析 + L2 表，非 IPv4 frame 不再被默默丟棄。③ 遙測在 pipeline 裡產生：direct/per-port counters、TTL guard、1/256 clone-to-CPU。
- 腳註：`482 lines of P4_16 / v1model, compiled with p4c-bm2-ss.`
- 素材：CHANGELOG 條目 7；`p4_src/SPEC.md`。

**Page 12 — Inside the pipeline**（新增，2026-08-18） 🆕
- Adam 指定：在 P4 pipeline 那頁後面加一張**更詳細**的 pipeline 圖，**風格與 Page 5/5 的架構圖一致**，圖可以佔大一點，左側文字解釋不要多。
- 版面：左欄 3.05" 只放三段短標＋兩三行說明；右欄 8.5" 全給圖（`DX = 3.95`）。
- 圖的縱向結構（框寬皆 `DW = 8.5`，箭頭 0.22"）：
  ```
  Parser        Ethernet · ARP · IPv4 · TCP/UDP/ICMP      y=2.00  h=0.42
      ↓
  ┌ MyIngress ─────────────────────────────────┐          y=2.64  h=2.50
  │ packet_out?     → 照控制器指定的埠送出，return          │
  │ IPv4?           → flow_5tuple  (ternary, real priority)│
  │                     miss → ipv4_lpm  (LPM)             │
  │ LLDP?           → send_to_cpu   鏈路探索                │
  │ anything else?  → l2_forward   (exact)                 │
  │ ─────────────────────────────────────────              │
  │ TTL guard  在 ipv4_forward action 內                    │
  │ 1-in-256   → clone_preserving_field_list(I2E)          │
  └────────────────────────────────────────────┘
      ↓
  [ Traffic Manager ]  灰底，not programmable — 複製在這裡才真正發生   y=5.36  h=0.42
      ↓
  ┌ MyEgress ──────────────────────────────────┐          y=6.00  h=0.80
  │ is this a clone? → 貼 packet_in 標頭，不計數            │
  │ otherwise        → egress_port_counter                 │
  └────────────────────────────────────────────┘
  482 lines of P4_16 / v1model, compiled with p4c-bm2-ss.  （寬度只給 7.5"，避開頁碼）
  ```
- 框標題（`MyIngress` / `MyEgress`）用 `frameTitle()` 畫在框線上緣、白底蓋線，模仿原始 ASCII 圖的樣子。
- 用 `ACCENT` 標的只有這次新增的東西：`flow_5tuple`、`l2_forward`、`TTL guard`、`1-in-256`。其餘全黑。
- Traffic Manager 用灰底灰框（`F2F2F2` / `9A9A9A`），因為**那一段不是我們能寫的**——這是這頁想讓聽眾記住的事。
- 左欄三段：① Order is the design（flow_5tuple 在 ipv4_lpm 之前）② Two exits before routing（packet_out 與 LLDP 都不會走到轉發表）③ Cloning is not ours（ingress 只是標記，複製由 Traffic Manager 做）。
- ⚠️ **MyIngress 框高一定要 ≥ 2.50"**，第一版給 2.26" 時最後兩行（TTL guard、1-in-256）直接溢出去蓋住 Traffic Manager。
- 素材：`p4_proxy/p4_src/ndtwin_switch.p4`、`p4_src/SPEC.md`。

**Page 13 — The P4 proxy agent** ✅
- 左側三段條列（寬 5.55"），右側模組表（等寬檔名 + 職責 + 行數）。
- ① 重寫 Ryu 北向 API（`/v1.0/topology/*`、`/stats/flowentry/*`、`/stats/flow/<dpid>`、destination paths），含 Ryu 的 string-action flow 格式。② 南向 P4Runtime gRPC 到 `simple_switch_grpc`；啟動時並行連線，每個 unary call 都有 deadline。③ 只有 `/p4/` 是新詞彙——Ryu 沒有對應物可模仿的（switch liveness）才另立命名空間。
- ⚠️ 模組表的行數是**目前檔案大小**，不是 diff 行數（與 Page 9 口徑不同），表下必須註明 `Current file sizes, not diff counts.`
- 素材：`p4_proxy/proxy_agent/SPEC.md`。

**Page 14 — sFlow synthesis, and how it was proven** ✅
- 左側三段條列，右側 round-trip 三格流程圖 + 「Two independent checks」小表。
- ①「合法的 sFlow」不夠——kernel 的 decoder 是手寫的固定 word-offset parser，datagram 必須跟 OVS 同一個**形狀**（兩個 flow record：`extended_switch` 然後 `raw header`）。② agent 位址讀的是 kernel 讀的同一份拓撲 JSON——kernel 用 `AgentKey{agentIP, port}` 歸戶，位址不認識就變成「歸給了不存在的東西」而且不報錯。③ 跨語言 round-trip 證明。
- 小表：Round trip = `test_SFlowEmitterRoundtrip.cpp`；Byte compare = `test_sflow_emitter.py` vs OVS capture。
- 素材：CHANGELOG 條目 8。

**Page 15 — The telemetry sample path** ✅
- 左側三段條列，右側流程圖：bmv2 pipeline → PRE clone session 250 → `packet_in` →（分岔）Telemetry（強調色框）／LLDP。
- ① clone session 250 住在 pipeline 的 PRE，沒 pipeline 時 bmv2 會拒絕——所以 proxy 只在**自己推過 config 之後**才程式化它。② 樣本與真 packet-in 共用同一條 channel，靠 `reason` 欄位分流；這對**負載**跟正確性一樣重要，因為取樣是全部流量的 1/256，讓樣本流進 LLDP parser 會把 discovery 埋掉。③ 值得講的坑：第三個 controller header 編譯會過但被 P4Runtime 默默忽略（按名字匹配，只認得 `packet_in`/`packet_out`）。
- 圖下實測：`2,700 packets over ten hops produced 107 samples against a model prediction of 105.`
- 🔴 **素材更正（2026-08-19）**：原本標「CHANGELOG 條目 9」，**那個條目裡沒有這些數字**
  （它講的是 PRE clone session 與 `reason` 欄位分流）。
  **正確出處：`doc/2026-07-29_p4_status_and_test_guide.md:95`** ——
  「2700 封包 × 10 跳 ÷ 256 ≈ **105** 個期望 sample，實測 **107**（第一次查詢時）」。
  同表 `:94` 另有 `rx=126, addressed=126` 的整條鏈驗證。
  ⚠️ 依 A2b 還缺 commit tag，**動筆時要補上量測當時的 commit**。
  📌 這條是外部審查標成「EVIDENCE NOT FOUND」找出來的——**它的結論是錯的**（證據在 repo 裡，
  只是**寫成中文**而它搜的是英文片語），但它連帶抓到的引用錯誤是真的。
  🔑 教訓：grep 式的「找不到證據」在雙語 repo 上有系統性盲點，收到這種回報要自己再搜一次。

**Page 16 — Liveness reported from evidence** ✅ 🟢 **2026-08-20 全頁改為流程圖（Adam 裁定）**

> 🟢 **v4.8：這兩頁（16、17）條列敘述廢話太多，改成流程圖，風格比照架構圖。**
> **關鍵決定：畫的是程式裡真正的控制流，不是敘述的圖示化。** 兩張都是直接讀原始碼畫的——
> Page 16 讀 `DeviceConfigurationAndPowerManager.cpp` 的 `p4LivenessFor()`，
> Page 17 讀 `topology_manager.py` 的 `check_link_beacons()` / `run_watchdog_pass()`。
> 🔑 **這麼做的附加價值**：條列版當初把「三態」寫成一張並列的表，看起來像三個平等的選項；
> 實際上原始碼是**一條有順序的判斷鏈**，而「順序」正是它的設計——
> 先問有沒有探測結果、再問成不成功、再問夠不夠新、最後才問有沒有反證。
> **表格畫不出這件事，流程圖畫得出來。**
>
> **版面規格（兩頁共用，寫在 `build_deck.js` 的 fBox/fTxt/fArrow/fStep/fTest/fBranch）**：
> - 沿用架構圖的視覺：Arial、白底、1pt 黑框、`ACCENT` 只給新增／我方的東西。
> - **判斷框**用 `PANEL` 淡底 + 1.25pt 框，條件本身用 Courier New 粗體，下面一行 8pt 灰字解釋。
> - **終端框**（UP / UNKNOWN / DOWN / reported-not-rerouted）用細框 + 該色文字；`UP` 給 `ACCENT_BG`、
>   `DOWN` 與 `reported, not rerouted` 給 `WARNC`。
> - 標題用 Arial 15pt bold **畫在 y=0.50**（不是 deck 的 `pageTitle`），副標 9.5pt 在 y=0.84。
>   🔴 **y 一定要 ≥ 0.50**，因為 `sectionTab` 畫在 y=0.28，用 0.18 會直接撞上去（已踩過）。
> - 右欄 7.5pt 灰字註記，每個終端一則，講「為什麼是這個判定」。

**〔已作廢的條列版，保留供對照〕**
- 左側三段條列（**寬度上限 7.35"**，再寬會撞右欄），右側 Up / Down / Unknown 三態 + 強調色細條註記。
- ① 取代了什麼——`pingWorker` 每秒無條件對每台 bmv2 呼叫 `setVertexUp`，被砍掉的 switch 一秒內就回報健康；而 `is_up` 又 gate 住 power / CPU / temperature / link usage。② 探測是真的 round trip——`GetForwardingPipelineConfig` + `COOKIE_ONLY`；gRPC channel state 被否決當訊號，因為它在 IDLE 直到有東西強迫連線。③ LLDP 新鮮度改為無條件記錄——原本只在 edge 是新的時候才處理，收斂後每分鐘數千個存活證明被丟掉。
- 三態：**Up** = round-trip 成功的 RPC；**Down** = 問了而且沒有別的證據反駁；**Unknown** = proxy 不可達／未知 dpid／探測未完成／探測過期／新鮮 beacon 與失敗探測衝突。
- 註記：`Unknown` **不動 graph**。把它跟 Down 混為一談，正是當初一次掉線就把整組 OVS 標成死的原因（詳見 Page 23 ①）。
- 素材：commit `a8db425`。

**🟢 現行版（流程圖）的內容——每一格都對得回原始碼**

上半（虛線以上，`GATHERED BY THE PROXY`）：兩個**互相獨立**的證據來源匯進一個端點。
- `p4_client.probe()`，每 **2 s**（`LIVENESS_PROBE_INTERVAL_S = 2.0`）：
  `GetForwardingPipelineConfig` + `COOKIE_ONLY` → 寫 `probe_ok`、`probe_age_s`。
- LLDP beacon 抵達（`packet_in`，`reason = LLDP`，**無條件記錄**）→ 寫 `last_lldp_age_s`。
- 兩者匯入 `GET /p4/switch_state`，框上標 **“evidence, not a verdict”**。
  🔑 **這句是整頁的樞紐**：proxy 只交證據，判定在 kernel。所以虛線下方標 `DECIDED BY THE KERNEL`。

下半（判斷鏈，**順序照 `p4LivenessFor()` 的原文**，四個 yes 出口 + 一個終端）：

| # | 條件（Courier） | yes → | 右欄註記要講的 |
|---|---|---|---|
| 1 | `probe_ok` is absent or not a boolean | **UNKNOWN** | 第一次探測還沒回來。這裡回 Down 會讓**每一次開機的頭幾秒整張 fabric 都是死的** |
| 2 | `probe_ok == true` | **UP** | 唯一能證明 bmv2 行程在服務的訊號。gRPC channel state 被否決：它在 IDLE 直到有東西強迫連線 |
| 3 | `probe_age_s > 15 s`（`kProbeStaleSeconds`） | **UNKNOWN** | poller 卡住了。**那是關於 poller 的事實，不是關於交換機的** |
| 4 | `last_lldp_age_s ≤ 12 s`（`kLldpFreshSeconds`） | **UNKNOWN** | bmv2 可以照答控制面 RPC 而轉發很差，忙的交換機也可能漏掉一次 deadline。**新鮮 beacon 對上失敗探測是「分歧」不是「判決」** |
| — | 全部 no | **DOWN** | 問了，而且沒有任何別的證據反駁 |

底部橫條（一定要留）：`Up → setVertexUp` ／ `Down → setVertexDown` ／
**`Unknown → the graph is not touched`**（這格用黑色粗體，它是全頁的結論）。
🔑 **一句可講的總結**：**四條路通往「不知道」，只有一條路通往「死了」。**
⚠️ 常數 `kProbeStaleSeconds = 15.0`、`kLldpFreshSeconds = 12.0` 都在
`include/ndt_core/power_management/DeviceConfigurationAndPowerManager.hpp:259,268`，
**改了要回來改圖**。

**Page 17 — Failover: detect, reroute, recover** ✅ 🟢 **2026-08-20 全頁改為流程圖（Adam 裁定）**

**🟢 現行版（流程圖）——由上而下八格，兩個判斷點**
1. **Beacon out — 每 5 s**：`TopologyManager` 從每台交換機的每個 port 送一個 LLDP frame（packet_out）。
2. **Beacon in**：對面的 pipeline 把它送到 CPU port，回來變成 `packet_in`／`reason = LLDP`，
   **戳的是「那一個方向」的抵達時間**（不是那條 link）。
3. **Watchdog pass — 每 5 s**（`LINK_WATCHDOG_INTERVAL_S`）。
4. 🔶 **判斷：`now − last beacon > 15 s`？**（`LINK_BEACON_TIMEOUT_S = 3 × LLDP_BEACON_INTERVAL_S`）
   - **no → 迴圈退回第 3 格**（圖上左側有一條回頭線，這條要畫，否則看不出它是輪詢）。
   - 從沒講過話的 link 給 **30 s**（`LINK_STARTUP_GRACE_S = 6 ×`）。
   - 右欄註記講**為什麼是三次不是一次**：一個 interval 的容忍度會讓「掃描剛好落在 beacon 之前」
     就報故障，而**會抖動的鏈路報告比慢的更糟**——每一次都讓 kernel 拆邊、退出 BFS、重算全域路徑。
5. **belief 翻成 down，並告訴 kernel**：`POST /ndt/link_failure_detected`，
   **每一輪重試直到 kernel 接受**（`acked`）。理由要講：kernel 剛好在重啟就會永久掉掉這則通知，
   而症狀（壞掉的 link 一直顯示 up）**跟這個機制當初要修的 bug 長得一模一樣**。
6. 🔶 **判斷：這台交換機的 inbound link 全靜了，而 `probe_ok` 還是 true？**
   - **yes → `reported, not rerouted`**（獨立終端框，`WARNC`）：這是**交換機層級的症狀不是鏈路故障**，
     照報，但**把它的 link 留在路由圖裡**。
   - 右欄註記是**唯一一個實測出來的失效模式**：拔掉一個 bmv2 介面會讓那台的整條 packet-in 路徑卡住，
     於是**進入它的每條 link 同時靜音**——一次真實斷線產生**五個 down 方向，其中三個是健康的**，
     它們的 beacon 只是沒地方送。**回報可以安全地過度回報；重新編程不行。**
7. **`install_initial_routes()` — reprogram first**：在**移除 down 端點後的圖**上做 BFS，
   所以重裝不可能把同一條路徑再算回斷掉的 link。`insert_ipv4_route` 失敗會退回 MODIFY，**所以整輪是冪等的**。
8. **`push_destination_paths()` — announce second**：`POST /ndt/inform_all_destination_paths`。
   kernel 自己每 60 s 也會拉一次，**所以這一步買的只是延遲**。
   🔑 **順序本身就是重點**（右欄註記）：push 廣播的是**已經裝上去的**路由，
   先 announce 就會發出一份「誠實但已經過期」的快照，而更正要等到下一次 transition 才會到。

底部橫條：**偵測成本 = timeout 到 timeout + 一個掃描間隔**——
**照常數是 15–20 s，實測是 10.7–14 s**，兩者還沒對上，
**在對上之前調 timer 會不知道是什麼在動**（與 Page 45 ② 同一句，刻意呼應）。

⚠️ **這一頁不再放任何數據**。`ca72d22` 那張「Measured on the live stack」表已移除（Adam 裁定），
量測全部集中在 Page 26 與那三張圖。

**〔已作廢的條列版，保留供對照〕**
- 左側三段條列，右側「Measured on the live stack」數據表 + 強調色細條註記。
- ① bmv2 沒有 link-down 訊號，所以 proxy 自己發 LLDP beacon，watchdog 在 beacon 停止抵達時判定斷鏈。② `calculate_all_paths` 改成接收「要避開的端點」並在移除後的圖上搜尋——原本搜尋整張圖，所以失效後重裝會把同一條路徑再算回死掉的 link。③ 可以過度回報，但不可以過度反應：拿掉一個 bmv2 介面會讓進入該 switch 的每條 link 都靜默（一次真實斷線產生五個 down 方向、其中三個是健康的），所以**重新編程用的是比回報更窄的集合**。
- 數據表（`ca72d22`）：Outage ~15 s／Path `1-5-10-8-4 → 1-5-9-8-4`／Rule `s5 → 10.0.0.4` 由 `OUTPUT:4 → OUTPUT:3`／Verified = 經 P4Runtime 讀回／Paths held = 12 條全數維持／Loss 300 封包的 9.67% 後恢復／Restore 25 秒內回原路徑。
- 註記：**故障模型本身就是發現**。`tc netem` 只丟 egress queue，switch 在其他 port 照常轉發；`ifconfig down` 會破壞這一點。
- ⚠️ `tc netem` vs `ifconfig` 的對比與 Page 36 重複，**兩處擇一**。目前放這頁。
- 素材：commit `ca72d22`、`f773422`。

**Page 18 — Phase 7: switch power management**（新頁，v1/v2 大綱缺這一頁） ✅
- ① 為什麼需要——數位孿生要能回答「關掉這台會怎樣」，就必須真的能關、能開、能重新接管。
- ② 三段機制：`ndtwin-p4-power` helper（關閉整台 bmv2 並保留可重啟的狀態）、`POST /p4/readopt/{dpid}`（重開機後重建 mastership、pipeline、clone session、路由）、`/v1.0/topology/switches` 對死掉的 switch 直接讓它消失而不是留在清單裡假裝存在。
- ③ **live 驗收數字**：關機 135 秒後，power-on 到重新接管只花 **1.50 秒**（`949fcba` 修掉 gRPC 全域 subchannel pool 繼承舊 backoff 之後）；678 筆 10 Hz 取樣期間**零 up-blip**。
- ④ 誠實補一句：readopt 在鏈路還沒被 LLDP 重新發現時會回報「已接管、路由尚未安裝」，那 30 秒的空窗是已知且可觀測的。
- 素材：`doc/p4_bmv2_support_plan.md` Phase 7 節；`doc/phase7_power_mechanism_design.md`；commit `949fcba`、`32afeb9`、`3674ddd`；實測數字在 `A-live-runbook.md`、`W2-live-reverify.md`。
- 備註：這頁補的是原大綱的結構缺口——Phase 7 已完成卻完全沒有頁面。

**Page 19 — Robustness: two defects in my own code**（新頁） ✅
- 本頁刻意獨立，**講的是 Adam 自己寫的 proxy 碼裡的缺陷**——不放 bug 頁（那節只講 baseline），但也不藏。
- ① **readopt 對健康 switch 清表卻回報 success**（`a72a168`）：live 抓到、修好、補了拒絕與接受兩個方向的測試。真肇因是**我方 election id 重用**——`p4_client.py` 每個 client 都寫死同一組 `election_id (0,1)`，readopt 開的新 client 在協定層面與現任 primary 無法區分。已加防呆（沒取得仲裁就完全不碰 switch）；**election id 重用本身刻意不修、列為已知限制**（改 mastership 政策要重驗整條 readopt 流程，風險不對稱）。
- ② **單一 switch 的故障變成全 fabric 的狀態遺失**（`1a7d815` 的 proxy 半邊）：一台 bmv2 活著但不回應 gRPC 時，proxy 的 flow-table 端點是 `async def`，於是那個阻塞的 gRPC 讀跑在 asyncio 的 event loop 上，把**整個 proxy** 拖死——liveness 端點從 1.9 ms 變成完全無回應，kernel 讀不到任何 switch 的狀態，圖從 40/40 掉到 32/40。用 py-spy 對活著的 proxy 取 stack dump 直接指認出那一格；同一份 dump 還證明 liveness prober 全程健康、threadpool 全程閒置——**證據早就備好了，只是沒人能讀**。修法：把阻塞工作移出 event loop ＋ 給 streaming gRPC 讀加 deadline。修完實測：liveness 端點全程 1.2–1.9 ms、圖全程 40/40。
- ③ 🆕 **2026-08-19 新增第三條：修好一個繼承缺陷，曝光了它底下的第二個。**
  **這是 A2 裁定 `034da18` 要搬到這頁的那一條，2026-08-19 才真正執行。**
  - 繼承的路由器斷鏈時**從不重繞**——`on_link_delete` 只記 log ＋ 通知孿生，全檔 **0 個
    `remove_edge`**，而 `install_all_pair_paths` 被旗標擋著**一個 process 只跑一次**。
    實測 **180.75 s × 3，故障解除才恢復**（見 Page 24）。
  - 我的 `2c81b26` 修好它：加上刪邊與週期性重算。**但那正好讓繼承碼裡一個潛伏的假設
    變成構得到的**——BFS 查反向邊 `net[current][prev]["port"]`，而反向邊現在可能不見了。
    於是每次重算都在那行 `KeyError` 中止，流量仍然黑洞。
  - 我的 `034da18` 修好第二層：BFS 只走兩個方向都在的鏈路。
  🔑 **值得講的一般性結論**：**修復會改變可達性。** 那行有問題的碼是繼承的、一個字都沒動過，
  但在我的修復落地之前它是死碼。**「這個缺陷是誰的」這個問題，答案取決於誰讓它構得到。**
  ⚠️ **291 秒那個數字不要講**（Adam 裁定）——它量在這條鏈的中間狀態上。
  素材：`doc/audit/2026-08-19_failover-provenance/REPORT.md`。
- ⚠️ **② 與 Page 23 ④ 是同一事件的兩半**（那半在 baseline 的 kernel 碼、這半在自己的 proxy 碼），要明說是一體兩面，否則像重複計數。
- 🔴 **頁標題要改**：現在是三條，不是「two defects」。建議
  `Robustness: three defects in my own code`，或更準的
  `Robustness: what my own fixes broke, and how it was caught`。
- 素材：commit `a72a168`、`1a7d815`、`2c81b26`、`034da18`；`W2-live-reverify.md`。

**Page 20 — Four smaller pieces** ✅
- **2×2 格**（不是條列）。① 南向失敗可見化：`OpResult {ok, httpStatus, message}` 捕捉 curl 真正的 HTTP status；200 但 body 是 `{"status":"error"}` 也算失敗。② P4 明示自己的極限：group/meter 回 `501 unsupported`，不默默轉給 Ryu。③ 全 bmv2 拓撲的 identity ifIndex→port 對應，跳過不認識 bmv2 的 `ovs-vsctl`；惰性決定以免與拓撲載入 race。④ 操作員的 disable 現在存活：`adminDisabled` 折進 `is_enabled`，不再被下一次拓撲輪詢蓋掉。
- 素材：CHANGELOG 條目 4、10、12、19；commit `2e5e545`、`5a6fcdf`、`8c25dbc`。
- 備註：OpResult 放這頁（功能完善），不放 bug 頁——見 A2。

### 🔴【延後】第 2 節：建立一個可信的參照點（Page 21–26，Page 21 是節封面）

> **2026-08-18 改版（Adam 裁決）。**原本是 10 頁的「修復的 baseline bug」（舊 Page 22–31），
> **壓縮為 5 頁並更換主張**。兩個理由：
>
> 1. **學長姐會在場。**原結構在目錄上就寫著「四分之一的簡報在講前人哪裡做錯」，而既有系統
>    的功勞只有「一句話帶過」（舊 A1.1）。**一句話功勞對十頁缺陷**——這個不對稱措辭改不掉，
>    只有結構改得掉。
> 2. **逐條列缺陷不是這節最有價值的東西。**「同一個形狀重複出現」和「為什麼這些缺陷結構上
>    照不到」才是，而那兩件事講 5 頁比講 10 頁清楚。
>
> **完整的缺陷清單移到書面報告**，簡報不再逐條列。A2 的裁定表仍然有效且必須遵守——它現在
> 決定的是「哪一條可以被當作 baseline 缺陷引用」，不再是「放第幾頁」。
> 舊版 10 頁的完整內容在本檔 v3（git 歷史）。

**Page 22 — 我接手的是什麼，以及為什麼非動它不可** 🆕（合併「功勞」與舊版的「前提翻案」頁）

- **上半：baseline 是一套完整可運作的系統。**`28b8b13`（2026-04-20，實驗室前人上傳）：
  **76 個檔案**（不含 vendored 的 spdlog／nlohmann）、**45 個 C++ 原始檔、約 13,200 行**、
  **41 個 `/ndt/` endpoint**。七個外圍元件全部只透過這組 API 讀寫這個孿生。
  **我做的每一件事都站在它上面**——P4 支援之所以能做到「上層一行都不用改」，正是因為那組
  API 的邊界已經畫好了。
- **下半：開工前提被實測翻案。**假設是「模擬器功能正確、P4 是純新增、共用路徑不必動」。
  對真正的 baseline 樹逐條驗證之後：缺陷本來就在，而且**全部無聲**——不 crash、不留 log、
  每個 endpoint 回 200。**這正是前提看起來成立的原因。**
- **所以工作變成兩件事**：Track 1 = P4/bmv2 支援；Track 2 = 共用路徑的正確性（**先做**，
  因為它是驗證其他一切的參照點）。
- 強調句：`A baseline that lies cannot be used to verify a new data plane.`
- 🔴 **分寸句，必須放上投影片，不能只留在口頭**：
  > 這些缺陷**不是疏忽，是結構性的**。一個只回報自己的數位孿生沒有外部檢查點，
  > 它的錯誤按建構方式就是隱形的——正常使用它的人不可能發現它在說謊。
  > 要照見它們需要三樣東西：**第二個資料面**（差異測試）、**注入已知故障**（地面真相）、
  > 以及**獨立於孿生的量測**。這三樣在這次工作之前都不存在。
- 素材：baseline 規模數字用 `git ls-tree -r 28b8b13`（動筆時重數）；CHANGELOG L376-386、L388-410。
- 備註：這一頁決定整節的觀感。**先講清楚接手的東西有多完整，再講缺陷**，順序不能反。

**Page 23 — 同一個形狀重複出現：五種缺陷型態** 🆕（壓縮舊版六頁）

- 主張：**重點不是條數，是同一個形狀在不同子系統重複出現**——這代表它們是系統性的，
  可以被歸納、被寫成守則，而不是逐條打地鼠。
- 五種形狀（每種給 1–2 個代表例，**不逐條列完**）：
  1. **對非預期輸入直接 crash** — 一個 POST 打死整個 kernel（`/ndt/intent_translator/text`
     對 null translator 解參考，而 null deref 是 signal，下方 catch 接不到）。
     坑：`--no-ai` 是預設組態，所以這是常態不是邊角。
  2. **只會加、不會刪** — 每個資料攝取點都該問「舊資料什麼時候消失？」拓撲只在啟動抓一次
     （88 ms）就再也不讀；`setAllPaths` 從不清 map，斷鏈已刪的路徑還在回答查詢。
     **共同危害：孿生用已不存在的狀態計算——比空答案更糟，因為它看起來很有自信。**
  3. **失敗被回報成成功** — 一次 `ovs-vsctl` 掉線把十台交換機全標成死的（「失敗」與
     「回報零 bridge」不可區分），而且那個分支只會 `setVertexDown`，死是永久的。
  4. **默默給出錯的數字** — unsigned counter delta 下溢，**1.8×10¹⁹ bps 直達 API**；
     synthetic power 報 **1.9×10¹⁴ 瓦**。
  5. **沒有期限的等待** — kernel 讀每台交換機 flow table 的 `curl` 沒有 `--max-time`，
     而那個 sweep 是**逐台序列**的：一台不回應就卡住它後面每一台。
     **為什麼之前沒人發現**：Ryu/OVS 從來不會「活著但不回應」，要嘛答要嘛連線被拒；
     是 P4/bmv2 帶進這個新故障模式才引爆一個躺了很久的缺陷。
- ⚠️ **總數動筆時重數，並說清楚是哪一輪的盤點**（08-11 盤點 11 條、08-13 又裁定 8 條，見 A2）。
  舊版把 29 個條目分散在六頁，與「11+8」對不上——**這一頁不要給總數，給形狀**。
- ⚠️ 形狀 3 的 `3292653` 與舊 Page 26 ④ 對 graph 行為的描述互相矛盾（見 A2），
  **擇一，或直接不用那一例**（本頁只需要 1–2 個代表例，這是壓縮帶來的好處）。
- ⚠️ 形狀 5 與 Page 19 ② 是同一事件的兩半（那半在 baseline 的 kernel 碼、這半在自己的
  proxy 碼），要明說是一體兩面，否則像重複計數。
- 素材：CHANGELOG 條目 2、3、14、15、22–25、28、29、31；`fbd8140`、`f21d7a0`、`1a7d815`。
- 備註：**這頁是本節方法論價值最高的一頁**，建議講滿。逐條清單留給書面報告。

**Page 24 — 代表作：斷鏈之後從不重繞，而孿生說一切正常** 🔴 **2026-08-19 全頁改寫**

> 🔴 **這一頁的主張換了，因為舊主張的歸因被實測推翻。**
> 舊版寫「單向鏈路故障讓路由重算永久崩潰，實測 291 秒」，並把它當作**繼承缺陷**中最強的一條。
> **291 秒量在我們自己的中間版本上**（`2c81b26` 之後、`034da18` 之前），不是繼承版。
> 那個 `KeyError` 需要「圖會變不對稱」＋「會重算」兩個條件，**兩個都是 `2c81b26` 帶進來的**。
> 依 A1.5（bug 頁只講繼承缺陷），`034da18` 那段故事**移到 Page 19 穩健性頁**。
> **291 秒不進簡報**（Adam 2026-08-19）。證據鏈：`doc/audit/2026-08-19_failover-provenance/REPORT.md`。

- ① **繼承版的真實行為**：`on_link_delete` 的**全部內容**是記一行 log ＋ POST 通知孿生。
  沒有 `remove_edge`（全檔 **0** 次），而 `install_all_pair_paths` 被 `..._completed` 旗標擋著，
  **一個 process 只跑一次**。所以規則在啟動約 60 秒後裝好，**之後永遠不動**。
  🔑 **斷鏈不會觸發任何重繞——不是「重繞失敗」，是根本沒有重繞這件事。**
- ② **實測（2026-08-19，n=3，量於 `b6b75fa`）**：還原 `intelligent_router.py` 到 `2c81b26^`
  （純 Python，零編譯），同一支 `measure_failover.sh`、同一張 OVS 128-host cell、故障持續 **180 秒**：

  | | 中斷 | 故障還在時恢復？ |
  |---|---|---|
  | **繼承版路由器** | **180.75 / 180.75 / 180.75 s** | ❌ 三次都沒有 |
  | **現行** | 47.0 – 56.4 s（n=10） | ✅ 十次都有 |

  🔑 **三次到小數點第二位都一樣**，因為中斷長度是**故障持續多久**決定的，不是控制平面做了什麼。
  故障拉長，中斷就跟著拉長。**這是類別差異不是程度差異。**
  控制條件：注入前 `h1→10.0.0.33` 0% 遺失、bridge 是 `fail-mode=secure`（沒規則就丟包，
  不會是別的機制在撐）、netem 三輪全程驗證在位。
- ③ **同時孿生在說什麼**（這一段最有力，而且不受歸因更正影響）：該 flow 以 **9–15 Mbps 流動**、
  `edges_up 287/288`。更難堪的是它**收斂到一個看起來更健康的錯答案**：+50.2 s 時兩個方向
  都標 down（此時反而正確），+79.2 s 又「自我修正」回 287。**這是數位孿生最嚴重的失效模式**
  ——它不只是沒抓到，是主動給出令人安心的錯誤答案。
  ⚠️ 這段觀察量於 2026-08-13 的中間版本，**講的時候要說是哪一輪量的**（A2b 規則）。
- ④ **可講的一般性結論**：一個「看起來有在重算」的控制平面，和一個「真的會重繞」的控制平面，
  **從 API 上看不出差別**——兩邊的 `/ndt/` 端點都回 200，孿生兩邊都說健康。
  分辨它們需要的是**資料面的證據**（連續 ping），不是控制面的回報。
- 備註：**這頁是本節的高潮**，建議講滿。它證明四件事：baseline 真的會說謊；修復是有效的；
  差異測試這把刀是雙向的（拿 OVS 當 P4 的規格，反過來抓到 OVS 的 P0）；
  以及 **⑤ 本身——我在自己的頭條數字裡找到混淆因子並重做了實驗**。
  🔴 ⑤ 在教授場合比原本那個數字值錢：不放，Q&A 第一個問題就會是「你 P4 跑 4 台、
  OVS 跑 128 台，這樣能比嗎」，那時候就不是加分了。
- 素材：`034da18` 完整 commit message；`doc/audit/2026-08-12_overnight-review/C-live-ovs-runbook.md:660`
  （原始時間軸）；`doc/audit/2026-08-17_p4-vs-ovs-matched-topology/REPORT.md`（控制實驗，含 23 份 raw log）。

**Page 25 — 方法可重複，以及還沒修的** ✅（壓縮舊版「第二輪」＋ 誠實清單）

- **主張：同一套查證方法再跑一輪，又撈出六條。**重點不是條數，是**方法可重複**——
  查證方式是直接讀 baseline 樹（`git show 28b8b13:<path>`），不是看 CHANGELOG 的敘述。
- 代表例（不逐條列完，其餘進書面報告）：
  - **十台 switch 共用一個插座**（`59dc5d3`）：電源管理對每台交換機回同一個插座物件，
    關一台等於關全部。
  - **一個功能在五個層次同時是死的**（`ee7233b`）：historical link data 從 API 到儲存五層全部沒接通。
  - **丟棄 `boost::edge()` 的 found 旗標**（`cbb504a`）：回傳一個沒找到的 edge，後續當成有效的用。
  - ⚠️ **OpenAI API key 被寫進 log**（`57346f6`）：講的時候**必須帶一句**「這是產品自己的
    Intent Translator 在用 OpenAI」，否則會被誤判成 A1.3 禁止的「AI 協作開發流程」而整條砍掉。
- 🆕 **2026-08-17 又一條**：`setupNFSForApp` 在 app id 重用時提早 return
  （`fs::create_directories` 對已存在的目錄回 false → 當成失敗 → **跳過權限設定**，
  而呼叫端只記一行 warning 然後照樣回傳成功）。**已對 `28b8b13` 驗證為 baseline 缺陷。**
  屬 Page 23 形狀 3「失敗被回報成成功」。
- **誠實列出還沒修的**（動筆時重查）：`Answer::from_json`（「只會加不會刪」的第四例，
  **已發現、未修**）；VLAN 欄位名不符（issue #3 已立案，只講不修）；Ryu wedge 的 root cause
  未證明（危害已擋，見 Page 26）。
- 備註：「已發現、未修」在教授場合是**加分不是扣分**——它證明清單是查證出來的，不是挑好看的講。

**Page 26 — 調查故事：Ryu flow-stats wedge**（可略，但推薦講）

- ① 症狀：Mininet 活著時重啟 Ryu，`/stats/flow` 永遠回空表。
- ② 兩次重現、151 個樣本特徵化（`doc/audit/ryu-wedge-trace-2026-08-07.tsv`）；
  四個假說全數證偽，**root cause 至今未證明**——照實講。
- ③ 不碰 Ryu 修掉危害：wedged 回覆要 1.011 s（健康 0.027–0.083 s；1.0 s 正是
  `ryu/lib/ofctl_utils.py` 的 `DEFAULT_TIMEOUT`），所以 ≥0.5 s 的空表回覆一律拒收、沿用前值。
- ④ 操作守則：不要單獨重啟 Ryu。
- 素材：CHANGELOG L412-419；該 tsv 檔。
- 備註：展示「假說→證偽→只修危害」的研究方法，對教授場合是加分頁。
  **時間不夠時這頁優先刪**——它是本節唯一可略的一頁。

### 🔴【已拆解】第 3 節：使用技術 —— **這一節取消，兩頁各自搬家**（Adam 2026-08-19 裁定）

> **理由（三個，第三個是 Adam 沒提但成立的）**：
> ① **技術棧該在更前面**——它列的是聽眾在聽 pipeline 與 proxy **之前**需要的背景，
>    排在第 3 節等於技術細節都講完了才告訴他們用了什麼。
> ② **方法論屬於測試**——差異測試／mutation gate／allowlist 閘門／證據式設計就是測試方法論，
>    而第 4 節的 L0–L4 五層正是它的實作。**方法論解釋「為什麼要有這五層」，兩頁放一起才完整。**
> ③ **第 2 節延後之後，這一節會變成兩頁孤兒**，還要多耗一張節封面。拆掉正好收乾淨。
>
> **搬到哪**：
> - `技術棧總覽` → **開場，接在架構圖（Page 6/7）之後**，作為「用什麼做的」收尾。
> - `方法論` → **第 4 節開頭**，排在五層架構之前。
>
> ⚠️ **節次要重編**：原第 4 節→第 3 節、原第 5 節→第 4 節，節封面少一張，
> Outline（Page 2）與 E4c 的節封面清單都要同步。

**〔搬到開場〕技術棧總覽** ✅
- 建議三欄：**Kernel（C++23）**——CMake、Boost.Beast/Asio/URL、nlohmann::json、spdlog、libssh、GTest；ASan/TSan sanitizer 建置。**P4 資料面**——P4_16 / v1model、bmv2 `simple_switch_grpc`、`p4c-bm2-ss`、P4Runtime（gRPC/protobuf）、PRE clone session、Mininet。**Proxy 與控制面（Python）**——FastAPI/uvicorn、grpc、Ryu/OpenFlow 1.3、sFlow v5、LLDP、SNMP。
- 素材：`CMakeLists.txt`、`p4_proxy/requirements.txt`、各 SPEC.md。
- 備註：依 A1 規則，不出現 AI 協作相關字樣。

**〔搬到第 4 節開頭〕方法論（本次工作真正的重點技術）** ✅
- ① **差異測試**：OVS 路是已知良好的，直接拿它的行為當 P4 的規格（L4 differential）。
  🔴 **原本這裡寫「而 Page 24 證明這把刀是雙向的」——那個交叉引用要拿掉**，
  因為 Page 24 在延後的第 2 節裡。改講**同一輪 08-19 的實例**：同一把刀量出繼承版路由器
  斷鏈時從不重繞（180.75 s × 3），而現行碼會自癒——**差異測試對照的是「修好前 vs 修好後」，
  不必宣稱任何人的碼有 bug。**
- ② **Mutation testing 作為驗收關卡**：每個測試都要親眼看過它失敗（弄壞實作→看它紅→修回），證據入檔 `doc/audit/mutation-evidence-*.md`；抓到 11+ 個「通過但什麼都沒證明」的測試（動筆時重數）。
- ③ **allowlist 閘門**：沒列入白名單的 warning/差異一律 fail，新問題藏不進舊雜訊。
- ④ **證據式設計**：liveness 三態、南向 OpResult——「無法判斷」與「失敗」都不准偽裝成「成功」。
- 素材：`doc/testing_tools_overview.md`；CHANGELOG L433-441。

### 第 4 節：測試工具與文件（Page 30–33，Page 30 是節封面）

**Page 31 — 五層測試架構（L0–L4）** ✅
- 🔵 **headless 啟動收在這一頁的底部**（2026-08-18，Adam 提問後查證）。標題寫 `What made L2–L4 automatable at all`。
  ⚠️ **不要寫成「讓單元測試自動化」**——L1 是編譯成 `test_routing_strategy` 直接跑的 gtest，**本來就不需要 kernel process**。真正被 `--mode` / `--topology` / `--no-ai` 解鎖的是 **L2 / L3 / L4**，那三層都要 running stack，而 `stack.sh:642` 正是用這三個旗標把 kernel 拉起來的。
  可講的點：原本啟動是三個 `std::cin` prompt，測試編排只能 pipe `"1\n2\n2\n"` 進去，**prompt 順序一改就默默載入錯的拓撲**——測試工具本身的無聲失敗，正好呼應第 2 節的主軸。
  素材：`src/main.cpp` 的 `[Co-developed…]` 註解、`tools/test_workflow/stack.sh:642`。
- 分層表：L0 建置檢查／L1 單元測試（**ctest 與直接執行兩種方式都跑**——ctest 每 case 獨立 process，跨測試干擾永遠不會發生所以永遠報綠）／L2 API 契約／L3 元件契約（blast radius）／L4 OVS/P4 差異比對（allowlist 三分類：允許的 P4 限制／數值容忍／**其餘就是 bug**）；`stack.sh` 依模式用正確順序編排啟動。
- 素材：`doc/testing_tools_overview.md`（首選）、`tools/test_workflow/README.md`。

**Page 32 — 測試資產規模與品質保證** ✅
- ① 數字（**動筆時重量**）。2026-08-16 為 46 個 .cpp／579 gtest；**2026-08-18 已是 47 個 .cpp／603 gtest／82 suites（`2fc430c`）**，兩天內被四個 commit 追過。其餘：16 個 py 檔／438 個、`tests/python` 7 檔／236 個、`tests/shell` 7 支——**這三個也要重量**，它們和 gtest 那個數字同齡。
- ② 品質保證不是數字而是機制：mutation 證據檔；修掉 4 個測試工具自己的假 PASS（例：`unittest` 把 skipped 算進 `Ran N`，整檔 skip 也顯示綠燈；`fbd8140` 又修 3 個從未真正執行的測試）。
- ③ log 判定：`check_logs.py` 的 allowlist＋FORBID＋崩潰偵測（crash 訊息不吃 allowlist）。
- 素材：CHANGELOG L433-441；`doc/audit/mutation-evidence-*.md`。

**Page 33 — 文件資產** ✅
- 分類列出——**操作**：`full_test_runbook.md`、`ovs_manual_test_runbook.md`、`p4_manual_test_runbook.md`、`environment_gotchas.md`；**設計/狀態**：`p4_bmv2_support_plan.md`、`p4_status_and_test_guide.md`、`HANDOFF.md`、`ndt_api.md`；**測試**：`testing_tools_overview.md`、`testing_workflow.md`、`test_coverage_gaps.md`（誠實列出還沒測的）；**調查紀錄**：`doc/audit/`。
- 備註：可略；一頁帶過即可，重點是「接手的人有路可走」。

### 第 5 節：量測結果與 demo（Page 34–41，Page 34 是節封面）

**Page 35 — L4 差異比對：P4 對齊 OVS baseline** ✅
- 一句話結論：L4 differential **PASS（量於 `dac192b`）**——P4 與 OVS baseline 一致，被接受的差異全部有文字記錄；12 條因 P4 補齊而過時的 allowlist 逐條對活系統驗證後移除。
- 🔴 **兩件事動筆前必做**（2026-08-18 查核）：
  1. **「PASS」要標 `dac192b`，不可寫成現況。**`.test_run/baseline/` 現在是**空的**（08-15 之後沒有 capture），所以這個結論**今天重驗不了**——重跑要把 stack 換到 OVS capture 一次、再換回 P4 capture 一次。標 commit 是誠實的講法：它在 `dac192b` 驗過，之後沒再驗。
  2. **「14」這個數字要重數，並寫出口徑。**`baseline_diff_allowlist.txt` 的非註解**行數**是 `dac192b` 當時 **19**、現在 **18**——都不是 14。很可能 14 數的是「被接受的差異」這個*發現*數而不是*行*數（一行樣式可涵蓋多個差異），但**兩種口徑差 4–5**，講的時候要說清楚數的是哪一個。
- 素材：commit `dac192b`；CHANGELOG 條目 17；`tools/contract_test/baseline_diff_allowlist.txt`；查核紀錄 `doc/audit/2026-08-18_pre-report-claim-verification.md` §2a。
- 【Adam 後續提供】：比對輸出截圖、差異的分類表。

**Page 36 — Failover 端到端驗證** ✅（🔴 **2026-08-18 全面改寫，見下方作廢說明**）
- 一句話結論：注入只斷單一 link 的故障（`tc netem loss 100%`；不用 `ifconfig down`），流量改道、恢復後路由回原路，全程孿生狀態正確。**兩個資料面在控制條件下比較：P4 快 13%。**

- 🔴 **舊版對照表已作廢，整張不可再用。**它長這樣（保留於此，只為說明為什麼不能用）：

  | 量測 | bmv2（P4） | OVS（對照組） |
  |---|---|---|
  | ping 中斷後自癒 | 16.63 s | 52.42 s |
  | 單向故障 | 12.5 s 自癒 | 291 s 零自癒 |

  **作廢原因：P4 那欄跑 4 台 host 的拓撲，OVS 那欄跑 128 台**，而且 OVS 那側跑的是尚未被
  `034da18` 修復的碼。**資料面、拓撲大小、程式版本三個變因同時在動**，任何一列都不能歸因給
  資料面。舊版 caption「差異來自實作而非設定」正是那個不成立的歸因。

- ✅ **改用控制實驗的結果**（2026-08-17，`doc/audit/2026-08-17_p4-vs-ovs-matched-topology/`，
  **同一張拓撲、同一套量測腳本**；08-17 那輪 23 次，**補到四格之後共 40 次**）：

  | cell | n | 平均 | 標準差 | 範圍 |
  |---|---|---|---|---|
  | **P4 / 4 hosts** | 10 | **13.7 s** | 1.6 | 11.0 – 16.4 |
  | **OVS / 4 hosts** | 10 | **15.7 s** | 1.5 | 13.7 – 18.1 |
  | **OVS / 128 hosts** | **10** 🆕 | **51.8 s** | 3.3 | **47.0 – 56.4** |

  🆕 **2026-08-19：128-host 那格從 n=3 補到 n=10**（Adam 要求；原因是它要拿來跟 P4/128 對比，
  而且三格 n 不一致本身就會被問）。**新的 7 輪量於 `b6b75fa`**，原 3 輪量於 `9467ea0`。
  🔑 **n=3 的估計撐住了**：平均從 50.1 → 51.8，範圍只往上延伸到 56.4。
  這回頭佐證了當初「效果夠大所以 n=3 就夠」那個判斷是對的。
  raw log 在 `doc/audit/2026-08-19_failover-provenance/raw_ovs128_n10/`。

  **P4 比 OVS 快 2.0 秒（13%）**，Welch *t*=2.89、df 17.9、**p=0.0098**、95% CI **0.55–3.50 s**。
  **40 次全部只有一次中斷然後完全復原**，沒有任何一次失敗復原，也沒有任何一次是斷斷續續的。
  （這不是目測：`plot_figures.py` 的 raster 只收「恰好一個 >1 s 缺口」的 run，40 份全數入選。）
- **三個變因分離之後的量級順序**（這才是本頁的敘事）：
  🔴 **2026-08-19 全部重算，而且順序變了**（原文：`已修的 kernel 缺陷 ≫ 拓撲大小 3.2× ≫ 資料面 1.13×`）：
  繼承版路由器**從不重繞**（類別差異，不是倍數）≫ **拓撲大小 3.29×（OVS）／1.21×（P4）**
  ≫ 資料面 **4 台 1.15×、128 台 3.12×**。
  🔑 **「資料面是最小的一項」這句話在 128 台上不成立**——它從第三名跳到與拓撲效應同級。
- **方法上必須講的四件事**（它們是這 40 次能站得住的原因，也是舊表站不住的原因）：
  ① 連續 ping 5 packets/s 帶時間戳，中斷時間是**量出來的**不是推論的；
  ② **注入的鏈路在執行時解析**（OVS 讀 `ovs-ofctl dump-flows s1`、P4 讀 proxy 的
  `all_destination_paths`）——寫死介面會注進一條沒人在用的鏈路，那看起來跟「瞬間復原」一樣；
  ③ **netem 每 5 秒重讀一次**，任何一次不在就作廢該輪（40 次全數通過）；
  ④ 復原只在故障**仍然存在**時才採計，所以量到的是繞路不是故障解除。
- ⚠️ **引用時引區間，不要只引平均**：兩邊 run-to-run 範圍仍然重疊（P4 最慢 16.4 s、
  OVS 最快 13.7 s），**沒有任何單一一對 run 能證明它**，要靠樣本才看得見。
- 🆕 🔴 **2026-08-19：第四格量了，而且它推翻了「資料面是三項裡最小的」這個結論。**
  「P4 在 128 台上沒有測（第四格只驗交互作用，刻意不做）」**已作廢**。

  | cell | n | 平均 | sd | 範圍 |
  |---|---|---|---|---|
  | P4 / 4 hosts | 10 | 13.68 s | 1.6 | 11.0 – 16.4 |
  | OVS / 4 hosts | 10 | 15.71 s | 1.5 | 13.7 – 18.1 |
  | **P4 / 128 hosts** 🆕 | **10** | **16.59 s** | 2.0 | **14.3 – 20.8** |
  | OVS / 128 hosts | 10 | 51.75 s | 3.3 | 47.0 – 56.4 |

  🔑 **交互作用比兩個主效應都大**：4 → 128 台時，**OVS 慢 3.29×，P4 只慢 1.21×**。
  在 128 台上兩者相差 **3.12×，而且兩組範圍完全不重疊**（P4 最慢 20.8、OVS 最快 47.0）——
  對照 4 台時要靠 n=10 才看得出 2 秒的差距。
  ⚠️ **所以「資料面只差 1.13×，是三項裡最小的」這句話只在 4 台上成立**，不可以當通則講。
  ⚠️ **機制未查明**，不要猜。可講的是觀察本身：**規模放大時兩條控制路徑的退化方式不同**。
  - 條件對齊：同一支 `measure_failover.sh`、同一個目標 `10.0.0.33`、同樣 90 s 故障、
    P4 兩格都是 `-O3` build。P4/128 量於 `213d209`，OVS/128 的 7 輪同批，原 3 輪於 `9467ea0`。
  - **這一格能量得成，本身是個發現**：`p4_testbed_topo.py` 的註解寫著
    「128 hosts in BMv2 might be too heavy」——**實測是錯的**。bmv2 完全撐得住
    （10/10 switches up、16256 條路徑 11 秒收斂、每台 128 筆規則、記憶體充裕）。
    真正擋路的是**四份寫死 4 台的清單**散在三個檔案：拓撲接線、拓撲的 ARP 迴圈、
    proxy 的 `add_host` 表，以及**實際會跑的 `ntg_bmv2_topo.py` 的 ARP 迴圈**
    （`ndtwin-lab` 啟動的是它，而它 import 前者所以看起來一樣）。
    🔑 **可講的一般性結論：那句「可能太重」的註解擋了這個實驗好幾個月，而它從來沒被驗證過。**
- ⚠️ 這是**單一故障、單一 host pair、單一機器**的量測。它說的是「這個故障在這些拓撲上 P4 繞路比較早」，
  不是關於兩個資料面的通則。
- 素材：`doc/audit/2026-08-17_p4-vs-ovs-matched-topology/REPORT.md`（含 23 份 raw ping log 與
  `measure_failover.sh`）；舊數據出處 `A-live-runbook.md`、`C-live-ovs-runbook.md`、`W2-live-reverify.md`。
- ✅ 🆕 **2026-08-19 圖已備妥**：`figures/page36_failover-boxplot.png`（box plot ＋ 疊上 40 個原始點）、
  `figures/page36_failover-raster.png`（**四格，每格 n=10**）與
  `figures/page36_failover-decomposition.png`（一個類別項 ＋ **兩個乘數各兩根**，線性刻度）。
  **三張都是從 40 份 raw ping log 重新解析出來的**，不是抄報告的表——
  `plot_figures.py` 的 `outage_from_pings()` 每次重畫都重算一次，逐格與 REPORT.md §3 吻合。
  🔑 **box plot 上疊原始點是刻意的**：兩邊 run-to-run 範圍重疊（P4 最慢 16.4 s、OVS 最快 13.7 s），
  疊點讓「沒有任何單一一對 run 能證明它」這件事直接看得見，正好執行本頁「引區間不要只引平均」那條。
  ⚠️ 右側那格現在是 **P4/128 與 OVS/128 並排的兩個 box（各 n=10）**，不再是散點——08-19 兩格都補到 n=10。
- 🆕 **2026-08-19 新增實測：繼承版的路由器斷鏈時「從不重繞」，現在有數字了。**
  把 `intelligent_router.py` 還原到 `2c81b26^`（純 Python，零編譯），同一支 `measure_failover.sh`、
  同一張 OVS 128-host cell、故障持續 **180 秒**（現行恢復時間的 3.6 倍）：

  | | 中斷 | 故障還在時恢復？ |
  |---|---|---|
  | **繼承版路由器**（n=3） | **180.75 / 180.75 / 180.75 s** | ❌ **三次都沒有** |
  | **現行**（n=10） | 47.0 – 56.4 s（平均 51.8） | ✅ 十次都有 |

  🔑 **三次到小數點第二位都相同**，因為中斷長度是**故障持續時間決定的**，不是控制平面做了什麼。
  故障拉長，中斷就跟著拉長。**這是類別差異不是程度差異**，所以 n=3 就夠。
  控制條件：注入前 `h1→10.0.0.33` 0% 遺失、`fail-mode=secure`、netem 三輪全程驗證在位。
- 🔴 **291 秒那個數字不進簡報**（Adam 2026-08-19 裁定）。它量在**我們自己的中間版本**上，
  不是 baseline。完整證據鏈見 `doc/audit/2026-08-19_failover-provenance/REPORT.md`。
- 【Adam 後續提供】：斷鏈前後的路徑圖（數據已備齊，缺視覺化）。

**Page 37 — 兩個資料面的吞吐上限（2026-08-15 本機 A/B 飽和實測）** ✅
- 同一 fabric、同一 3-hop 路徑（h1→s1→s5→s2→h2）、同一 iperf3 腳本量兩顆 bmv2 build：
  - **現役 stock build**（`-O0` + 全 logging）：UDP delivered 天花板 **~40 Mbps**、TCP goodput **24.2 Mbps**（8 平行流仍 24.2，平行不救）、**~3.6k pps** 不分包長。
  - **重建 fast build**（`-O3 --disable-logging-macros`，`/usr/local/bmv2-fast`）：UDP delivered **~460–530 Mbps**、TCP **431 Mbps**、**~50.8k pps** —— **12–18× 增益**。
  - **OVS 對照 980 Mbps**（受 TCLink 1G 整形壓制）。
- ⚠️ **文獻值 ~170 Mbps（SIGSIM-PADS '23）不描述本機任一顆 build**（stock 低它 4×、fast 高它 ~3×），引用只能當量級提示並標注文獻。
- **原因**：bmv2 是解譯式參考實作，`-O0` + logging 巨集讓每包固定成本主導（天花板是 pps 不是 bps，64B 與 1400B 同 pps 實證）；丟包發生在第一台 on-path switch 的 input buffer，**介面計數器看不見**（h1 送 89,296、s1-eth3 RX 89,296、s1-eth1 TX 僅 33,456）。
- **連帶效應**：拓撲宣告 1 Gbps 時，P4 側單流利用率上限 stock **~4%**、fast **~43–53%**。TE 的 70% 壅塞門檻在 stock 上物理不可觸發（OVS 上 08-15 已實測成功觸發並改寫實表）；fast 上多流共享 uplink 時進入可設計範圍。對孿生量測而言，sFlow 1/256 取樣的誤差地板（196√(1/c)）比原始吞吐更早成為主導限制。
- 切換機制：topo 的 `bmv2_binary_override` 檔（`4b339f2` seam，`LD_LIBRARY_PATH` 自動攜帶、壞 override 大聲拒絕），預設仍跑 stock。
- 素材：`doc/2026-08-15_bmv2-performance-report.md`「本機飽和實測」節。
- 🆕 **2026-08-19 新增：控制平面啟動時間對照**（Adam 要求）。同一張 128-host fabric、
  同樣 **16256 條 all-pairs 路徑**：

  | | 拓撲建置 | 控制平面收斂到全部路徑就緒 |
  |---|---|---|
  | **P4 / 128**（proxy） | 22 s | **11 s** |
  | **OVS / 128**（Ryu） | 同一張 Mininet | **73 s** |

  🔴 **這個對照不可以照字面講。** OVS 那 73 秒裡**有 60 秒是寫死的等待**——
  `intelligent_router.py:473` 的 `if is_mininet: hub.sleep(60)`。扣掉之後是 **約 13 s vs 11 s**，
  兩邊同一個量級。
  🔑 **講「P4 開機快 6 倍」會被一句 `grep hub.sleep` 當場打死。** 誠實而且更有意思的講法是：
  **P4 這條路徑上沒有那個人為延遲**，而那 60 秒是繼承碼裡的常數，從來沒有人回頭問過它還需不需要。
  📌 順帶：那個 sleep 上面有一段註解記著一個「看起來像設定、行為像常數」的死旋鈕
  （`intelligent_router.py:43-47`），兩件事是同一個地方。
- ✅ 🆕 **2026-08-19 圖已備妥**：`figures/page37_throughput-ab.png`，**刻意畫成左右兩張**——
  左邊 bps、右邊 pps。**pps 那張才是論點**：stock 3.6k 對 fast 50.8k，而同一顆 build 在
  64 B 與 1400 B 下 pps 相同，這才證明「天花板是每包固定成本，不是頻寬」。
  只畫 bps 會讓人以為是頻寬問題。⚠️ 圖上**沒有**放文獻的 170 Mbps（兩顆 build 都不描述它），
  要提就放腳註並標明是文獻值。

**Page 38 — 200 Mbps 壓力測試＋負載下斷鏈** ✅
- 一句話結論：OVS stack 推到 200 Mbps 並在負載下斷鏈，記錄哪些量測撐住、哪些開始失真。
- 素材：commit `cc7437a` 完整 message。
- 【Adam 後續提供】：吞吐／量測誤差圖表。

**Page 39 — 孿生 flow-rate 精確度量測** ✅ 🆕 **2026-08-19 全頁補齊（原為空殼）**
- **一句話結論**：孿生的鏈路使用量估計是**無偏的**，而它的誤差**就是取樣理論的地板**——
  不是地板之上的某個實作誤差。所以精度不是一個數字，是一條曲線。
- **⚠️ 講法很重要**：**不要說「我們準確到 X%」。** 那個數字不存在——同一套儀器在 1 秒窗
  是 ±21%、在 430 秒窗是 ±1.2%。可以講的一句話是：
  > *unbiased, with precision set by sample count — ±21% at a 1 s window and 200 Mbit/s,
  > ±1.2% at 430 s, exactly as sampling theory predicts.*
  這比「我們很準」強得多，因為它展示的是**我們懂這把尺**，而不是「我們的尺很準」。
- **右側主圖**：誤差 vs 窗長，疊上 `誤差% ≈ 196 × √(1/c)` 的理論地板（c = 樣本數）。
  兩條實測線（200 Mbit/s 與 20 Mbit/s）應該**坐在曲線上**，這就是整頁的視覺論點。
- **誤差曲線（實測，量於 `04b8933`，OVS 128-host 拓撲、單一定速 UDP 流、無 NTG 無 apps）**：

  | 窗長 | 200 Mbit/s 觀測 ±% | 理論 ±% | 20 Mbit/s 觀測 ±% | 理論 ±% |
  |---|---|---|---|---|
  | 1 s | 20.7 | 23.9 | 70.9 | 75.6 |
  | 10 s | 8.1 | 7.6 | 25.7 | 23.9 |
  | 60 s | 3.1 | 3.1 | 6.8 | 9.8 |
  | 150 s | 1.9 | 2.0 | 4.9 | 6.2 |
  | 430 s | 1.2 | 1.2 | — | — |

  **無偏性**：中位數比值在每個窗長、兩種負載下都是 **0.97–1.02**。
  3599 個樣本的平均 **205.5 Mbit/s vs 真值 205.8**（差 **0.15%**）。
  跨 **430× 窗長 × 10× 負載** 驗證。
- **解析度地板**：量子 = `256 × frame bytes × 8`。本次實測 GCD **正好 3,059,712 = 256 × 1494 × 8**。
  ⚠️ **它是 per-flow 不是常數**——三輪量到三個不同值（1494 / 1506 / 1490），因為每次的流量組成不同。
  20 Mbit/s 那輪最能說明：十分鐘裡讀值**只取 15 個相異值**，全部是 3.06 Mbit/s 的倍數。
  1 Gbps 鏈路上 → 低於約 3 Mbit/s 的流看不見，`utilization_percent` 以 0.31% 為級距。
- **邊角情況表（誤差開始失效的邊界）**：

  | 邊界 | 後果 |
  |---|---|
  | 單次 1 秒讀值 | 200M 時擺盪 122–288 Mbit/s；20M 時比值 **0.149–2.382**（低 85%～高 138%） |
  | `±5% @ 1 秒窗` | **在 bmv2 上不可能**——不是生成器不夠力，是取樣數學。加大流量買不到 |
  | OVS **4-host cell** | **完全沒有配 sFlow**，讀值恆為 0 且 `status: success`。示範遙測**一律用 128-host** |
  | 10 Gbps 核心鏈路 | 分母寫死 1 Gbps（F-8），所以 `utilization_percent` 錯十倍。**改用 bps 講** |
- 🆕 **2026-08-19：P4/bmv2 已經量了，而且結論是「兩個平面上是同一把尺」。**
  詳見下方新增的 Page 39b。**原本寫在這裡的「本次只量 OVS」已不成立。**
- **這一頁仍然不支持的**：多條併發流下的精度；apps 在跑時的精度。

**Page 39b — 遙測精度：合成的（P4）對原生的（OVS）** ✅ 🆕 **2026-08-19 新量**
- **為什麼要有這一頁**：Page 39 證明的是「孿生的估計是無偏的、誤差是取樣理論地板」——
  但那是在 **OVS** 上量的，而**兩個平面產生遙測的方式根本不同**：

  | | 誰取樣 | 誰產生 sFlow 紀錄 |
  |---|---|---|
  | **OVS** | 交換機自己（`sampling=256`，`testbed_topo.py:136`） | **交換機自己**送出 |
  | **P4** | pipeline `random(0,255)==0` 複製到 CPU port（`ndtwin_switch.p4:52,384`） | **proxy 自己合成** sFlow v5 送進 kernel 既有的 :6343 |

  kernel 分不出來——這正是「上層一行都不用改」的實作方式。
  **所以這一頁測的是那個主張的數值面**：我們捏出來的遙測，和真的一樣準嗎？
- **兩邊取樣率相同（都是 1/256），所以理論地板共用，是同一把尺量兩個平面。** 這點先查證過才動手。
- **結果（P4 stock build、20 Mbit/s、600 s、2400 samples、0 掉樣，量於 `b6b75fa`）**：

  | 窗長 | P4 中位數比值 | OVS 中位數比值 | P4 觀測 ±% | OVS 觀測 ±% | 理論 ±% |
  |---|---|---|---|---|---|
  | 1 s | 0.965 | 0.966 | 54.6 | 70.9 | 75.5 |
  | 2 s | 1.001 | 0.967 | 47.5 | 51.3 | 53.4 |
  | 5 s | 1.008 | 0.989 | 29.6 | 35.0 | 33.8 |
  | 10 s | 1.016 | 1.022 | 20.1 | 25.7 | 23.9 |
  | 30 s | 1.008 | 0.990 | 8.8 | 11.8 | 13.8 |
  | 60 s | 1.003 | 1.007 | 6.3 | 6.8 | 9.7 |

  **兩邊真值都是 20.6 Mbit/s**（不是湊的，是各自量出來的），所以這張表可以逐列並排。
- **可以講的兩句話**：
  1. **合成的遙測和原生的一樣無偏**——中位數比值在每個窗長都是 0.97–1.02，兩個平面都是。
  2. **合成路徑沒有引入額外誤差**——P4 的散布在每個窗長都**等於或小於**取樣理論地板。
- ⚠️ **一個誠實的未解點，建議主動講而不是等人問**：P4 的散布**一致地低於理論地板**
  （1 秒窗 54.6% 對理論 75.5%），而 OVS 幾乎正好坐在線上。低於地板不是壞事，但
  **機制沒有查明**。候選解釋（都沒驗證）：bmv2 的 `random()` 每包不獨立，使取樣接近
  systematic 而非 Bernoulli（對定速流，systematic 取樣的變異數確實比 Bernoulli 低）；
  或連續兩次孿生讀值之間有相關性。**要主張它就得再設計一個實驗，目前只報告觀察。**
- **量子（解析度地板）也是各自量的**：P4 這輪 GCD = **3,051,520 = 256 × 1490 × 8**，
  OVS 那輪是 256 × **1494** × 8。**又一次證明量子是 per-flow 不是常數**——現在有四個值
  （1490 / 1490 / 1494 / 1506），不要在投影片上把它寫成一個固定數字。
- **拓撲對照的注意事項**：P4 這輪跑 4-host cell、OVS 那輪跑 128-host cell，但
  **兩張拓撲的交換機核心相同（都是 10 台、都是 32 條交換機間邊）**，差別只在 host 數。
  而取樣精度只由「該鏈路上的樣本數」決定，與 host 數無關——所以這個對照成立。
  ⚠️ 但要講就要把這句一起講，否則會被問「拓撲不一樣怎麼比」。
- ⚠️ 🆕 **`page39_per-hop-consistency.png` 上 OVS 有 4 個 box、P4 只有 2 個，會被問，先準備好答案。**
  **那是上面那件事的直接後果，不是缺陷**：128-host 佈局裡那條流走 4 跳，4-host 佈局裡走 2 跳，
  而只有**載著流量**的鏈路能入圖（其餘 28–30 條是 0）。
  🔑 **關鍵是這張圖問的是「同一條流在它自己路徑的各跳之間一致嗎」——那是每一格內部的比較,
  不是拿 P4 的跳去比 OVS 的跳。** 所以跳數不同不影響結論：**6 跳全部落在 1.0 的 ±4% 內。**
  （**Adam 2026-08-19 裁定：不為了對稱重跑。** 要對齊唯一的辦法是在 128-host P4 上重收
  600 秒 sFlow；判斷是那不會改變結論，只會讓圖好看。）
- **200 Mbit/s 的對照另外量**（P4 必須換 `-O3` fast build 才到得了 200 Mbps，
  stock 天花板約 40 Mbps）。⚠️ **換 build 是一個變因，引用時要標明。**
- **素材**：`doc/audit/2026-08-19_p4-sflow-accuracy/`（原始 `.jsonl.gz`、`analyse_q.py`、
  `plot_figures.py`）。**圖**：`figures/page39_sflow-accuracy-20M.png`、
  `figures/page39_sflow-accuracy-200M.png`、`figures/page39_per-hop-consistency.png`。
- **素材**：`doc/audit/2026-08-18_live-full-stack-round/sflow-accuracy-2026-08-18.md`
  （含兩輪原始資料 `.jsonl.gz` 與可重跑的 `run.py` / `analyse.py`）；
  理論來源 sflow.org packetSamplingBasics；commit `d7bf52f` 的 message 解釋了為什麼
  「<10 Mbps 單讀會錯數倍而中位數準」不是 bug。
- 🔑 **方法論亮點，值得留給 Q&A**：**先前一輪把這個量測做錯過，而錯法很有教育性。**
  舊的量測腳本用 `eth1..eth4` 這個埠號規則挑「交換機間介面」，但接取交換機上 host 是從
  eth3 開始的——所以 ground truth 混進了一條 host 鏈路。把那個方法套在**已知無偏**的資料上
  會回報 **0.813**；換成真正的交換機間介面集合回報 **1.017**。
  **一個看起來像 −19% 系統性偏差的東西，整個是量測工具自己造成的。**

**Page 40 — 獨立交叉檢查** ✅
- 一句話結論：由不了解實作的第三方視角對活的 OVS stack 做 51 次唯讀檢查，12 項發現全數裁定——1 項真 bug（已修），其餘為已記錄行為或誤報，逐條查證後結案。
- 素材：commit `2bec2a5`、`fbd8140`（其中 47 項 HIGH 裁定出 21 項真問題）。
- 備註：依 A1 規則，敘述用「第三方交叉檢查／獨立驗證流程」，不提以 AI 工具執行。
- 【Adam 後續提供】：是否深入展開由 Adam 決定，預設一頁帶過。

**Page 41 — Demo** ✅
- 【Adam 後續提供】：demo 影片。三段：① 斷鏈 failover 即時展示；② **Web-GUI** 看 P4 模式拓撲與流量；③ killed switch 的 liveness 三態變化。
- ✅ 🆕 **2026-08-19：錄製流程已寫好** → `2026-08-19_demo-recording-runbook.md`（本資料夾）。
  含每一段的畫面配置、逐字指令、以及**各自的「會當場發作」地雷**。
- ✅ **② 就是 Web-GUI，名字沒錯**：`~/Web-GUI`，**React + Vite，跑在 Docker 裡**，
  `http://localhost:3000`（容器 `ndt-frontend` / `ndt-node-positions-api` / `ndt-postgres`；
  部署腳本 `~/Web-GUI/web_gui_deploy.sh`）。面板有 Topology、FlowInformation、
  LinkFlowInformation、DeviceInformation、SwitchPortPanel 等。
  ⚠️ 它是**唯讀的視覺化介面**——**沒有電源或改路由的控制項**，那些要在 Mininet CLI 做。
  （另有 `~/Network-Traffic-Visualizer`，是**另一支** JavaFX 桌面程式，不是這個。）
- 🔑 **③ 的講法**：三態是 Up → **Unknown** → Down，而 **`Unknown` 不動 graph**。
  探測失敗但 LLDP beacon 還新鮮時判 Unknown，等 beacon 過期（15 s）才轉 Down——
  **不會因為一次探測失敗就改寫拓撲**。這正好回頭呼應 Page 23 的缺陷形狀。
- ⚠️ **不要現場 live demo**。這台機器沒有 ffmpeg／OBS，錄影用 GNOME 內建
  （`Ctrl+Alt+Shift+R`，存到 `~/Videos/Screencasts/*.webm`）；
  **`.webm` PowerPoint 不一定吃**，最穩的作法是簡報不嵌影片、切出去用瀏覽器播。

### 收尾（Page 42）

**Page 42 — 總結與未完成事項** ✅
- ① 成果一句話：P4/bmv2 資料面完整接入、上層零修改；baseline 共用路徑的無聲缺陷修復；五層測試架構讓兩個資料面都有可判定的健康標準。
- ② **誠實列出未完成**（08-13 重新核對）：**Phase 3 未開始**（Phase 7、8 都已完成）；`Answer::from_json` 第四例未修；Ryu wedge root cause 未證明；`hopsCounter` 分母膨脹已記錄未修；VLAN 欄位名不符已立案（issue #3）未修；已知風險——southbound 指令仍以 `popen("curl …")` 拼接、`json::dump()` 不跳脫單引號（刻意延後，22 處/3 檔）；**election id 重用刻意不修、列為已知限制**（見 Page 19）；**bmv2 stock build 吞吐上限 ~40 Mbps／台**（見 Page 37，解譯式參考實作的設計取捨，非缺陷）。
- 🆕 **2026-08-18 再新增一條未完成**：**鎖沒有持有者概念——任何呼叫端可以釋放任何呼叫端的鎖。**實測：A `acquire_lock {"type":"routing_lock"}` 拿到 200；B（另一個連線、無任何憑證）`release_lock` 同型別回 **200 released**，然後 B `acquire_lock` 直接拿到 200。`release_lock` 只檢查鎖存不存在（不存在回 412），**不看誰持有**。七個元件共用這組鎖，所以其中一個的清理流程可以在另一個操作到一半時無聲抽掉它的 routing lock。**報告前不修**：加 owner token 會改動七個元件的契約。由三個獨立模型中的兩個事先預測、實測證實（`doc/audit/2026-08-18_three-model-questioner-round/`）。
- 🆕 **2026-08-18 新增一條未完成**：**佇列式的 flow 端點沒有辦法查詢派送結果。**`install_flow_entry` 現在把「形狀」和「語意」分開——形狀不成立（例如缺 `actions`）在 HTTP 層同步回 **400**，形狀成立的進佇列回 **200 queued**。但 200 之後**規則到底有沒有裝上交換機，沒有任何 API 問得到**。補法是加一個查詢端點，或讓 200 回一個可查的 job id——**那是新功能不是修 bug**，所以列在這裡。
  🔴 **2026-08-18 更正（量於 `04b8933`）：本條原寫「派送結果只寫在 kernel log 裡」，那句話只對 P4 成立。**
  兩個資料面實測，同樣送一條交換機會拒絕的規則、同樣拿到 `200 queued`：**P4** 寫下
  `[error] dispatched install failed for dpid 1 (priority 901)`；**OVS 整份 log 16,324 行、0 個 error**，
  規則沒裝上而**任何地方都沒有紀錄**。所以在 OVS 上這個缺口不只是「查不到」，是**事後也追溯不到**。
  （成因：`Controller.cpp:55` 靠「200 回應的 body 裡有沒有 error」判失敗，P4 proxy 會放，
  Ryu 的 `/stats/flowentry/add` 在交換機裁決前就回 200，所以那個檢查在 OVS 上沒東西可找。）
  ⚠️ 講的時候要帶一句**為什麼這個缺口值得講**：契約套件 L2 曾經全綠而 kernel log 同時寫著 `dispatched install failed`——**綠燈與失敗可以同時存在**，正是因為佇列式端點只驗得到「誠實地說已排隊」。**那個例子是 P4 側的**；OVS 側連那行 log 都沒有。這條未完成本身就是 Page 22「無聲缺陷」主軸的現役實例。
- 🆕 **2026-08-19 新增三條未完成（round 4 實測，量於 `04b8933`）**。
  ⚠️ **完整清單現在有單一出處：`doc/KNOWN-ISSUES.md`（17 條，按「正常操作會不會踩到」排序）。**
  這頁只列該上台的，其餘指過去。
  1. 🔴 **電源開機可以回報成功而什麼都沒做。** P4 上，關機後**約 10 秒內**送
     `set_switches_power_state?action=on` 回 **200 `Success`、0.01 秒**，bmv2 行程數不動、
     交換機永久維持死亡，同時 `power=ON`、`is_up=True`、**100% 封包遺失**。
     成因完全是內部自造的：`powerOff` 標 vertex down，約 1 秒後 1 Hz liveness worker
     在死掉的交換機上把它翻回 up，於是 `P4PowerStrategy::powerOn` 第一行的
     `if (getVertexIsUp(node)) return success();` 就直接回成功。
     用有鑑別力的第二次呼叫證明：等 graph 沉澱到 `is_up=false` 後送**完全相同**的 POST，
     花 1.27 秒、行程 9→10、轉發全復原。
     **🔑 示範繞法（零成本）：關機後等 15 秒再開機。** 這條之所以排第一，是因為
     人手動示範「關掉再打開」就是幾秒內完成，**正好落在窗口裡**。
  2. 🔴 **P4 proxy 重啟會靜默摧毀 bring-up 以來安裝的每一條規則**（bmv2 沒重啟），
     而孿生回報**完整健康恢復**：40/40 邊、10/10 up、**零警告**。用 P4Runtime 直接讀真實
     交換機表驗證的。重啟 proxy 是**正常運維動作**，不需要注入任何故障。
  3. **上面那條「`json::dump()` 不跳脫單引號（刻意延後）」現在有實測後果了。**
     match 裡一個 `'` → `/bin/sh` 語法錯誤 → curl **從沒執行** → kernel 回報
     `no response from <component> within 5s`，**指控一個它根本沒連過的健康元件**。
     而同一輪測了「控制器真的掛掉」，得到**一模一樣的訊息**——所以那行 log
     無法區分「我的請求壞了」和「對方掛了」。
     **這條的傷害不是它會壞，是它會把除錯的人送去錯的地方。**
- 🆕 **2026-08-19：一條被推翻的「重大缺陷」，值得當方法論講。**
  兩個獨立模型（各自盲讀原始碼）都把「OVS 電源開機把交換機指向 `tcp:127.0.0.1:6633`，
  而 Ryu 在 6653」列為 **CRITICAL**。**實測是它們錯的**：電源循環後 `is_connected: true`，
  撐過兩分鐘。原因寫在 Ryu 自己的原始碼裡——沒指定埠時它為了向後相容**多開一個 6633 的
  server loop**。**這件事本專案的 repo 裡一個字都沒有。**
  但降級不等於沒事：`powerOn` **不檢查 `is_connected`** 就回 Success，所以防線是 Ryu 預設值的
  巧合。只要有人加上 `--ofp-tcp-listen-port`，每台電源循環過的交換機就被靜默孤立——**一個旗標之遙**。
  **可講的一般性結論：只讀原始碼會系統性高估缺陷，因為看不到 runtime 組態。**
- 🆕 **2026-08-19：「你有沒有把既有的東西弄慢？」——這題現在有實測答案，建議留給 Q&A。**
  讀取路徑是我們改最重的地方（`FlowLinkUsageCollector.cpp` +442/−168、
  `TopologyAndFlowMonitor.cpp` +454/−96、`HttpSession.cpp` +329/−234），而從來沒人量過。
  **同一個活的 fabric（Ryu 與 128-host 拓撲起一次不動，只抽換 kernel binary）、同一種 build type**：

  | endpoint | baseline `28b8b13` | 現行 `b6b75fa` |
  |---|---|---|
  | `get_graph_data` | p50 **13.02 ms** | p50 **11.99 ms** |
  | `get_switches_power_state` | p50 1.21 ms | p50 0.79 ms |
  | `get_cpu_utilization` | p50 0.33 ms | p50 0.32 ms |

  ⚠️ **可以講的是「沒有變慢」，不是「變快」**——兩邊每次呼叫的範圍重疊，n=200 的 p50 差 1 ms
  撐不起方向性宣稱。
  🔑 **這一輪最值得講的其實是方法**：第一次量出來是「現行慢 5.5×」，**那整個是
  Debug 對 Release 的混淆**（主樹是 `Debug`，我第一版 baseline 建成 `Release`）。
  改成一致的 build type 之後方向就反過來了。第二個坑：重建後新 kernel 因為舊的還佔著
  UDP 6343 而 abort，**舊 process 繼續服務 :8000**，量到的數字看起來很合理。
  **所以延遲量測必須確認自己量的是哪一個 process**（`/proc/<pid>/exe`），這已寫進程序。
  ⚠️ 順帶更正：sflow 報告裡的 **`get_graph_data` 57 ms 不是穩定值**——那是量測輪進行中
  （有流量、4 Hz 輪詢）測的；閒置時同一個端點同一張圖是 ~12 ms。**引用時條件要跟著數字走。**
  素材：`doc/audit/2026-08-19_api-latency-vs-baseline/REPORT.md`（含 `api_latency.py`，
  該腳本會先斷言拓撲再計時）。
- ③ 下一步。
- 素材：CHANGELOG L216-219、L421-431；`doc/HANDOFF.md`（注意過期）；
  **`doc/KNOWN-ISSUES.md`（2026-08-19 建立，17 條的單一彙總出處）**；
  round 4 實測在 `scratch/round4/FINDINGS-round4.md`。
- 備註：「誠實列出未完成」在教授場合是加分不是扣分；數字動筆時重查。
- 🔴 **可講的方法論亮點（強烈建議留給 Q&A 或口述）**：mastership 上游回報**在送出前被自己推翻**。原本結論是「**bmv2 本身**接受未取得 mastership 的 pipeline push」，規格條文都備好要回報 p4lang 上游了。送出前的最後一步——「用一個不是我們自己寫的 client 重現看看」，目的正是排除自家 client 的嫌疑——結果它排除的是 bmv2。第三方 raw gRPC client 三情境實測：① 真正的非 primary（election id 較低、bmv2 明確回 `"Is backup"`）推 pipeline **會**被 `PERMISSION_DENIED` 正確擋下；② 換成 election id **重複**時 push 才會過，**而且 Write 也一樣會過**，所以原本當殺手佐證的「Write 有檢查、push 沒有」這個不對稱根本不存在；③ 把在線 primary 的 stream 關掉，同一個 client、同一組 election id、同一種 RPC 就從 `OK` 翻成 `PERMISSION_DENIED`——這才是當初那四行 log 的真相。**上游回報在送出前取消。** 關鍵細節：我們自己的 log 從頭到尾寫著 `Election id already exists`（＝重複），是寫報告時被轉述成「election id 較低」，整個機制就建立在那個轉述上。**如果被問「你們怎麼確定自己沒搞錯」，這就是答案：一個會推翻自己的驗證流程。** 佐證：`doc/2026-08-13_p4runtime-mastership-spec-check.md`、可重跑的 `p4_proxy/reference/p4runtime_mastership_probe.py`。

**Page 43 — References** ✅ 🆕 **2026-08-19 新增（原本整份簡報只有 1 個引用）**
- **為什麼要有這一頁**：Page 39／39b 整頁的論證是「我們的誤差**就是**取樣理論的地板」，
  而那個「理論」在簡報上**沒有出處**。加一條引用，那一頁就從「我們量到這樣」
  變成「我們量到的與已發表的取樣理論一致」——這是最低成本、最高回報的一個改動。
- **✅ 已查證，可直接排版**（每條都讀過原文或官方頁面）：

  | # | 出處 | 撐哪一頁 |
  |---|---|---|
  | [1] | **Phaal, P. & Panchen, S.** *Packet Sampling Basics*, sFlow.org — 誤差 `≈ 196√(1/c)`，95% 信賴區間 | **Page 39、39b 的整個論證** |
  | [1a] | **Jedwab, J., Phaal, P. & Pinna, B.** *Traffic estimation for the largest sources on a network, using packet sampling with limited storage*, HP Labs Technical Report **HPL-92-35**, 1992-03 | [1] 引用它作為二項分布性質的依據 |
  | [2] | Chen, Hu, Jin. *Performance Evaluation of P4 Programmable Switches in Emulation*, ACM SIGSIM-PADS '23. DOI `10.1145/3573900.3591120` | Page 37 吞吐；bmv2 規模分析 |
  | [3] | p4lang/behavioral-model, `docs/performance.md` — 單台 `simple_switch` ~1047 Mbps / 80k pps | Page 37 的基準對照 |
  | [4] | Zhou, Yang, Duan, Lopez, Pastor, Wu, Boucadair, Jacquenet. *Network Digital Twin: Concepts and Reference Architecture*, IRTF NMRG, `draft-irtf-nmrg-network-digital-twin-arch-07`, 2024-09-26 | **Page 4 背景定位**、Page 42 |
  | [5] | faucetsdn/ryu README — *"The Ryu project needs new maintainers"*，並指向 OpenStack `os-ken` | Future work、技術選型 |

- 🔴 **`196√(1/c)` 的出處要講對，這條會被追問**（2026-08-19 查證）：
  **它不是一篇論文。** [1] 是 sFlow.org 的技術頁，**沒有出版日期，而且對式子本身沒有給引用**；
  它只在講二項分布性質時引了 [1a]。**底層數學就是二項分布的常態近似**——
  `196 = 1.96 × 100`，1.96 是 95% 信賴的 z 值。
  🔑 **所以被問「196 哪來的」，正確答案是「二項分布的 95% 常態近似」，不是「某篇論文的結果」。**
  答「這是 sFlow 規格寫的」會被追下去。
  📌 有個好用的細節：**Phaal 同時是 [1] 和 [1a] 的作者**——sflow.org 那頁是他把自己 1992 年的
  工作包裝成工程用形式。
  ⚠️ **[1a] 是查到的、沒開原文**；[1] 讀過。引用時照 A3 規則標清楚。
- 🔑 **[4] 特別有用**：它是 IRTF 的定義文件，讓「network digital twin」這個詞在簡報上有標準出處
  而不是自說自話。而且它**自己就寫**模擬／模擬器途徑「high resource consumption... poor scalability」
  ——正好是我們 bmv2 規模那段的文獻靠山，而不是我們自己在抱怨工具。
- 🔑 **[5] 是可以直接講的一句話**：我們南向依賴的 Ryu，**上游自己在 README 上求接手**。
  這不是我們的推測，是專案自己寫的。⚠️ 但**講法要準**：說「上游求接手並指向 os-ken」是事實；
  說「Ryu 已死」是過度延伸。
- ⚠️ **還沒查證、不要放上投影片的**（我只有知識，沒有現場核對）：P4_16 語言規格、
  P4Runtime 規格、sFlow v5 規格的正式書目資料；Statesman（SIGCOMM '14）；
  差異測試／mutation testing 的經典出處；ONOS／Stratum／PINS 的現況。
  依 A3 規則，這些要先開原文核對才可以引用。
- **版面**：一頁 5 條、兩欄或單欄清單、Calibri 11pt、`MUTED`。在對應頁的腳註用 `[n]` 回指。

**Page 44 — Future work** ✅ 🆕 **2026-08-19 新增**
- **為什麼要有這一頁**：Page 42 回答的是「你還欠什麼」（known limitations），
  **不回答「這件事接下來往哪走」**。教授場合這兩件事的作用不同，目前簡報只有前者。
- **三條，刻意分屬三個層次，而且都是我們自己的碼**（不是抱怨 baseline）：

  **① 併發控制——設計問題。** 兩條標準路徑各自被什麼擋住，已經定位：
  - **悲觀鎖沒有持有者概念**：`release_lock` 只檢查鎖存不存在（不存在回 412），**不看誰持有**。
    實測 A 拿鎖回 200 → B（另一連線、零憑證）release 回 **200 released** → B 直接拿到鎖。
    七個元件共用這組鎖。
  - 🆕 **而且加上 owner 也不夠**：`LockManager::renew`（`LockManager.hpp:123-137`）**只檢查
    `isLocked`，不檢查有沒有過期**，然後無條件把 `expiryTime` 往後推。所以一個**已經過期**
    的租約可以被無限期續下去——TTL 對「持有者掛掉」這個情境失去意義。
    `KNOWN-ISSUES.md:290` 有實測：非持有者把別人過期的 `routing_lock` 從 3s 續到 120s。
    🔑 **所以這條 future work 有兩半**：加 owner（誰能放）＋ 給 renew 加 `now < expiry`
    守衛（過期的租約不能復活）。**只做前者，崩潰的持有者仍然永遠不會被驅逐。**
  - **樂觀併發控制被 F-5 擋住**：commit 失敗偵測不到，所以重試沒有觸發條件。
  🔑 **這條最像研究題目**，因為它不是「我們沒做」而是「**兩條路各自的阻塞點已經找到，
  而且知道解鎖的前置是哪一個**」（修 F-5 是樂觀 CC 的唯一前置）。

  **② `topology_manager.py` 需要拆——結構問題。** 1,516 行，三個獨立責任
  （圖與路由／LLDP 與存活／規則翻譯）。
  🔑 **最強的證據是現成的**：這個類別內部有**兩把彼此獨立的鎖**
  （`_net_lock` 護圖、`_liveness_lock` 護存活簿記），而 `:288`／`:306` 的註解明寫兩者
  **"never held at once"**。一個類別需要兩把互不相干的鎖，通常就是兩個類別。
  **這是可驗證的觀察，不是主觀評論。**

  **③ 非同步回報 → completion handle——架構問題。** `processFlowBatch` enqueue 後立刻回
  `200 queued`，dispatcher 之後才真的送出，所以**交換機的拒絕傳不回 app**。
  🔑 **程式碼註解自己下的結論**：「needs either a synchronous path or a completion handle —
  **an architectural decision, not a wording one**」。
  加分細節：兩個會寫 flow 的 app **都把 response 丟掉**，所以就算今天改成 202 也沒人會看
  ——**這是七個元件的契約問題，不是 kernel 單邊的事**。
- **口述可補、不佔版面的其餘四條**：per-flow 5-tuple（P4 pipeline 有表、proxy 沒接、
  TE 自己也只送 `ipv4_dst`）；P4 在 128 台上從沒測過；LLDP 調參（實驗設計已在
  `KNOWN-ISSUES.md` §D-2，關鍵是**判準是誤判率不是偵測時間**）；多流／apps 在跑時的遙測精度。
- **版面**：三個編號條列，每條「一句問題＋一句證據＋一句下一步」。**不要列七條**，
  三條講得深比七條列得滿好。

**Page 45 — Planned for the next report** ✅ 🟢 **2026-08-20 新增（Adam 指定）**
- **為什麼要有這一頁，而且要跟 Page 44 分開**：Page 44 回答「這件事往哪走」，
  **不回答「下一次見面你會帶什麼來」**。教授場合這兩件事的作用不同：前者是研究方向，
  後者是**承諾**。🔑 **分工一句話**：Future work 是**已定位但沒排程**的結構性問題；
  這一頁是**下一次就要交出數字**的三件事。被問到差別時就這樣答。
- **版面**：三欄，每欄「編號＋標題＋現況段＋補充段＋強調色細條的判準句」。
  刻意跟 Page 44 的「左條列＋右註記」不同版型，讓人一眼知道這是另一種東西。
- **三條的共同結構（這是這頁的設計，不要破壞）**：每一條都寫出
  **① 現在的數字 ② 已經排除了什麼 ③ 怎麼算做完**。少了②就變成「我們打算查查看」。

  **① Find where the OVS 128-host recovery time goes**
  - 現況：**OVS 51.75 s vs P4 16.59 s，兩組範圍零重疊**。機制未查明。
  - 🔑 **已排除路徑計算**：同一張 fabric，16,256 條路徑在 Ryu 側實際只花約 **13 s**
    （量到 73 s，其中 **60 s 是 `intelligent_router.py:473` 寫死的 `hub.sleep(60)`**），
    P4 側 **11 s**。**這句一定要講**，否則整條聽起來像「不知道，打算亂查」。
  - 判準：**偵測＋重算＋裝規則三項要加得起來等於量到的 51.75 s。**（不是「找到原因」，
    是「帳要平」——後者可證偽。）

  **② Make failure detection faster without making it wrong**
  - 現況：偵測時間是**常數決定的不是網路決定的**。
    `topology_manager.py:137,155,158` → `LLDP_BEACON_INTERVAL_S = 5`，
    `LINK_BEACON_TIMEOUT_S = 3 ×` 它、`LINK_WATCHDOG_INTERVAL_S =` 它。
    **改一個常數三個一起動**，這是便宜的部分。
  - 實驗：beacon 掃 **5 / 3 / 2 / 1 秒**，每個值量偵測時間與誤判次數。
  - 判準：🔴 **看誤判率，不看偵測時間。** 偵測時間必然會降；而每一次誤判都讓 kernel
    拆邊、退出 BFS、重算全域路徑——`topology_manager.py:147-150` 的註解自己論證過
    「**會抖動的鏈路報告比慢的更糟**」。
  - ⚠️ **投影片上不要承諾降多少。**
  - 🔑 頁底那句「先解決一個疑點」是刻意的：註解寫偵測要 **15–20 s**，round 4 實測 **10.7–14 s**。
    **在模型對上之前調參，調完不知道是什麼在動。**
  - ⚠️ **沒放上投影片但要答得出來的隱藏成本**：`kLldpFreshSeconds = 12.0` 是 **C++ 常數**
    （`DeviceConfigurationAndPowerManager.hpp:259`）。beacon 從 5 降到 2.5，那個窗口就從容忍
    2.4 個 beacon 變成 4.8 個——**交換機存活判斷相對變得更不敏感**，維持比例要改 C++ 重編。
  - ⚠️ 另一個會被追問的：`handleLinkFailure` 對單向故障把**雙向**標 down，而修正它的是
    `kOnceConverged = 30 s` 的 topology poll。**所以「收斂」是兩個數字，調 LLDP 只改得動一個。**

  **③ Promote the fast bmv2 build to the default**
  - 現況：同一 fabric、同一腳本，stock（`-O0` ＋ logging）**~40 Mbps / 3.6k pps**；
    fast（`-O3 --disable-logging-macros`）**460–530 Mbps / 50.8k pps**。
  - 🔑 **切換的 seam 已經在了**（topo 的 `bmv2_binary_override`，`4b339f2`，`LD_LIBRARY_PATH`
    自動攜帶、壞 override 大聲拒絕），**預設仍是 stock**。所以這條不是「做不做得到」，
    是「敢不敢把預設換掉」。
  - **解鎖兩件現在量不了的事**：TE 的 **70% 壅塞門檻**（stock 上物理不可觸發）、
    **多流併發下的遙測精度**（Page 33／35 都明寫這是它們不支持的）。
  - 判準：**L0–L4 整套在 fast build 上通過。** 理由要講：**換交換機 binary 就是換掉
    每一層依賴的時序**，所以不能只跑吞吐。
- **素材**：`doc/KNOWN-ISSUES.md` §D-2（②的完整實驗設計與風險論證）；
  `doc/2026-08-15_bmv2-performance-report.md`（③）；
  `doc/audit/2026-08-17_p4-vs-ovs-matched-topology/`、`doc/audit/2026-08-19_failover-provenance/`（①）。

---

## F. 圖檔清單（2026-08-19 產出）

**位置**：`~/Desktop/NDTwin Slide material/figures/`
**產生器**：`NDTwin-Kernel/doc/audit/2026-08-19_p4-sflow-accuracy/plot_figures.py`
**重跑**：`"<slide material>/.plotvenv/bin/python" <repo>/doc/audit/2026-08-19_p4-sflow-accuracy/plot_figures.py "<slide material>/figures"`

> 🔑 **每張圖都是從已 commit 的原始資料重新算出來的，不是從報告的表格抄的。**
> failover 那三張每次重畫都重新解析 **40 份** raw ping log；sFlow 那些直接讀 `.jsonl.gz`。
> 所以「圖上的數字」與「報告裡的數字」不可能漂移——它們是同一次計算。
>
> ⚠️ **40 = 四格 × n=10**，散在三個目錄（08-17 那輪的 `raw/`、`raw_ovs128_n10/`、`raw_p4_128/`）。
> 三張 failover 圖共用同一個 `failover_key()` 分類器（2026-08-19 重構）——**在那之前 raster
> 自己留了一份分類邏輯，結果它安靜地少畫了 P4/128 那一格**。要再加格子只改那一個函式。

🔵 **v4.5 起：每張圖各佔一整頁**（Adam 2026-08-19 裁定）。檔名裡的 `pageNN` 只是它服務哪一段的
提示，**不是版位**。**圖頁不放頁標題**——八張圖都自帶標題與副標，再加一個標題就變兩層標題。
圖頁只有左上角節次標記與右下角頁碼，內容口述。實際順序見 C0 表。
產生器：`figurePage(file, ar)`，`ar` 直接寫成 `1840 / 860` 這種原始像素比，圖片依比例置中。
🟢 **v4.7：`ar > 2.5` 自動進寬圖模式**——左右邊界由 0.6" 縮到 0.4"（`maxW` 12.13 → 12.53），
且垂直剩餘空間**上 34% / 下 66%** 而不是各半。raster（2.82:1）就是為它加的。
⚠️ **`ar` 是寫死在呼叫端的**，圖重畫換了尺寸就要跟著改，否則圖會被拉變形而且**不會報錯**。
改圖之後先 `identify -format "%f %wx%h\n" figures/*.png` 對一次。

🔴 **v4.6 有兩張圖的尺寸變了,`ar` 必須跟著改,否則會變形**：

| 檔名 | 像素 | `ar` |
|---|---|---|
| `page36_failover-boxplot.png` | 1840 × 860 | `1840 / 860` |
| `page36_failover-decomposition.png` | **1920 × 980** 🔵 | `1920 / 980` |
| `page36_failover-raster.png` | **2480 × 880** 🔵 | `2480 / 880` |
| `page37_throughput-ab.png` | 1840 × 760 | `1840 / 760` |
| `page39_sflow-accuracy-20M.png` | 1840 × 920 | `1840 / 920` |
| `page39_sflow-accuracy-200M.png` | 1840 × 920 | `1840 / 920` |
| `page39_per-hop-consistency.png` | 1840 × 800 | `1840 / 800` |
| `page39_quantisation-ladder.png` | 1920 × 1000 | `1920 / 1000` |

⚠️ **raster 現在是 2.82:1（四格並排）**，在 16:9 版面上會頂到左右邊、垂直方向偏小。
它是三張 failover 圖裡**最不適合縮小的**（每個 tick 是一個 ping），
所以這一頁的圖要**盡量吃滿寬度**，上下留白不要平均分配。

| 檔名 | 用在 | 資料來源 |
|---|---|---|
| `page36_failover-boxplot.png` | Page 36 | 40 份 raw ping log（四格各 n=10） |
| `page36_failover-decomposition.png` | Page 36 | 同上；🔵 **兩個乘數各畫兩根**，見下 |
| `page36_failover-raster.png` | Page 36 | **40 次每一個 ping 都畫**，對齊故障時刻；🔵 四格 |
| `page37_throughput-ab.png` | Page 37 | `doc/2026-08-15_bmv2-performance-report.md` |
| `page39_sflow-accuracy-20M.png` | **Page 39b** | OVS run B ＋ P4 stock（20 Mbit/s 對照） |
| `page39_sflow-accuracy-200M.png` | **Page 39b** | OVS run A ＋ P4 fast（200 Mbit/s 對照） |
| `page39_per-hop-consistency.png` | **Page 39b** | 流經路徑上每一跳的比值（OVS 4 跳、P4 2 跳） |
| `page39_quantisation-ladder.png` | Page 39 副圖 | OVS 與 P4 並排的量子階梯，含平均／sd／極值 |

**兩張圖各自解決一個「box plot 看不到」的問題**：
- `failover-raster` — box plot 把每一輪壓成一個數字。raster 把 40 輪的**每一個 ping** 攤開，
  證明中斷是**乾淨的一段**而不是掉了又掉。⚠️ 這是被質疑「你怎麼知道它不是一直在閃」時的答案。
  四格並排時還多講一件事：**P4/128 那一格的中斷結束位置與 P4/4 幾乎重合，OVS/128 明顯外推**。
- `per-hop-consistency` — ⚠️ **這張原本要畫成「32 條鏈路」，做不出來**：實測只有
  **4 條（OVS）／2 條（P4）** 在載流量，其餘 28–30 條是 0。改成「同一條流經過的每一跳」，
  問的是「孿生在路徑每一跳上報的數字一致嗎」——6 跳全部落在 1.0 的 ±4% 內。
  ⚠️ **兩邊跳數不同不是缺陷而是拓撲**：OVS 那輪跑在 128-host 佈局（路徑 4 跳），
  P4 那輪跑在 4-host 佈局（路徑 2 跳），因為 P4 的 sFlow 資料是在 128-host 解鎖**之前**收的。
  **這張圖問的是「同一條流的各跳之間一致嗎」，那是每格內部的比較，不是跨格比較**，
  所以跳數不同不影響結論。若要跳數對齊，唯一辦法是在 128-host P4 上重收一次 sFlow（見下）。

🔵 **`failover-decomposition` 在 P4/128 量完之後已改版（2026-08-19）。**
舊版把兩個乘數各畫一根：拓撲 3.30×、資料面 1.15×，副標寫「注意它們有多小」。
**量完第四格之後那句話是錯的**——資料面在 128 台上是 **3.12×**，而拓撲在 P4 上只有 **1.21×**。
兩個乘數都沒有單一值,**各自取決於另一個因子的水準**。現在四根都畫，副標改寫。
⚠️ **不要回頭引用「資料面只有 1.15×」**，那個數字只在 4 台上成立。

**環境備忘（踩過的）**：這台機器**原本沒有 matplotlib**，也**沒有 Node**。
繪圖 venv 是 `<slide material>/.plotvenv`（`python3 -m venv` ＋ `pip install matplotlib`）。
⚠️ **不要裝進 `p4_proxy/venv`**——那支是 proxy 在用的。

⚠️ **`build_deck.js`／`NDTwin_deck.pptx`／`count_lines.py` 原本只存在於 Claude session 的沙箱目錄裡**
（`~/.config/Claude/local-agent-mode-sessions/…/outputs/`，綁 session id）。
2026-08-19 已複製到 `generator/` 與本資料夾。**`build_deck.js` 需要 Node，這台機器沒有**——
簡報由 Adam 的 cowork session 產生。

---

## D. 素材出處速查（agent 查證用）

| 主題 | 首選出處 |
|---|---|
| bug 的完整技術細節 | `git show <hash>` 的 commit message（品質極高，多數可直接改寫成投影片） |
| bug 清單與編號 | CHANGELOG `Unreleased` 節（L9-219）＋ themed 節（L371-441）——但分類以 A2 為準 |
| 測試工具敘述 | `doc/testing_tools_overview.md` |
| P4 計畫與 phase 狀態 | `doc/p4_bmv2_support_plan.md` ＋ B 節快照 |
| CHANGELOG 之後的 commits | `git log 850c2f2..HEAD` |
| 實測結果 | `ca72d22`、`cc7437a`、`d7bf52f`、`5639e65`、`dac192b`、`2bec2a5`、`fbd8140`、`034da18`、`949fcba` 的完整 message |
| **08-12/13 整夜測試輪的全部實測數據** | **`~/Documents/NDTwin documentation/Overnight review 2026-08-12/`**（repo 外）：`INDEX.md` 是入口；`A-live-runbook.md`（bmv2 輪）、`C-live-ovs-runbook.md`（OVS 輪）、`W2-live-reverify.md`（複驗輪）含 Page 34–38 要的全部數字 |
| 大規模測試與外部框架的評估 | `~/Documents/NDTwin documentation/Advanced testing research 2026-08-13/REPORT.md` |
| bmv2 吞吐 A/B | `doc/2026-08-15_bmv2-performance-report.md` |
| mastership 規格核對 | `doc/2026-08-13_p4runtime-mastership-spec-check.md`、`p4_proxy/reference/p4runtime_mastership_probe.py` |
| 增刪行數 | `count_lines.py`（見 E4） |

---

## E. 視覺與版面規格（Adam 已認可）

產生器：`build_deck.js`（pptxgenjs）。**新頁一律沿用裡面的 helper 與色票，不要另創風格。**

### E1. 設計原則

1. **極簡**。實驗室簡報風格，不是行銷簡報。白底、大量留白、細線分隔。
2. **顏色克制**。全篇只有一個強調色。不用色塊卡片、不用深色底頁（封面也不用）、不用彩色徽章。
3. **以編號條列為主軸**。`1 / 2 / 3` + 粗體小標 + 說明段。需要時才加示意圖，圖放右半或下半。
4. **不要淡灰字**。淡灰在投影機上幾乎看不見。判準：不重要的資訊**直接刪掉**（口述帶過即可），重要的用可辨識的深色或強調色。
5. **不要為了填版面加字**。寧可留白。

### E2. 色票與字體

| 用途 | 色碼 | 說明 |
|---|---|---|
| `INK` 標題 | `1A1A1A` | 頁標題、條列小標 |
| `BODY` 內文 | `2E2E2E` | 主要說明文字 |
| `MUTED` 次要 | `4F4F4F` | 副標、註記、腳註（**不得再淡**） |
| `FAINT` 說明 | `6E6E6E` | 欄位標籤、頁碼 |
| `RULE` 細線 | `D0D0D0` | 分隔線、方框外框 |
| `ACCENT` 強調 | `065A82` | 條列編號、關鍵數字、強調句、圖中的 kernel 框、節次標記 |
| `ACCENT_BG` | `EEF3F6` | 極淡強調底（架構圖的 kernel 框、After 對照框） |
| `PANEL` | `F7F8F9` | 中性淡底（Before 對照框、架構圖上層方框） |

| 元素 | 字體 | 字級 |
|---|---|---|
| 頁標題 | Cambria bold | 30–32pt（封面 44pt） |
| 副標 | Calibri | 14pt，`MUTED` |
| 節次標記 | Calibri bold | 10.5pt，`ACCENT`，y=0.28，`charSpacing: 1.0` |
| 條列小標 | Calibri bold | 15.5pt，`INK` |
| 條列編號 | Calibri bold | 13pt，`ACCENT` |
| 內文 | Calibri | 11.5–12.5pt，`BODY` |
| 腳註 | Calibri | 11pt，`MUTED` |
| 程式碼／識別碼 | Courier New | 隨上下文 |

**不要用 Aptos 或微軟正黑體**（前者無可靠替代、後者是中文版設定，已改英文）。

### E3. 版面

- 版面尺寸 13.333 × 7.5 吋（16:9）。左右邊界 `M = 0.85"`，內容寬 `CW = 11.63"`。
- 頁標題 y=0.62、副標 y=1.32、標題下細線 y=1.86；內容自 y≈2.16 起。
- 頁碼右下 `x=12.0, y=6.92`，10pt `FAINT`。封面不放頁碼。
- 條列間距至少 1.4"；每段內文寬度不超過 7.3"（超過就換兩欄或縮字數）。
- **產出後必做**：`validate.py` → 轉 PDF → `pdftoppm` 逐頁看圖，檢查文字溢出與撞行。這步不能省。

### E4. 增刪行數的計算口徑

**只有一支腳本：`count_lines.py`。** 它逐檔計算，再由同一份逐檔資料彙總出四大類，所以 Page 8 的彙總與 Page 9 的明細**不可能兜不攏**。輸出 `line_counts.json`。

> ⚠️ 曾經寫過兩支腳本各算各的，規則沒對齊，兩頁 kernel 數字差 24 行卻找不出原因。**不要再拆成兩支。**

規則：

- 基準：`28b8b13..HEAD`，`--unified=0`。
- **排除註解行與空行**。依副檔名：`.cpp/.hpp/.h/.p4` 去 `//`、`/* */`、`*` 開頭；`.py/.sh/.yml/.cmake` 去 `#` 開頭；`.md` 只去空行與 `<!-- -->`。
- 排除路徑：`build*`、`.test_run/`、`Testing/`、`test_env/`、`.vscode/`、`**/venv/**`、`*.pyc`。
- 排除檔案：`intelligent_router.py`（實驗室既有 Ryu 控制程式，隨 groundwork commit 帶入）、`.gitignore`。
- 分類：`kernel` = `src/`、`include/`、`setting/`、`cmake/`、`CMakeLists.txt`；`proxy` = `p4_proxy/`（但 `p4_proxy/tests/` 歸 test）；`test` = `tests/`、`tools/`、`.github/`、`p4_proxy/tests/`、根目錄測試/工具腳本；`doc` = `doc/`、任何 `.md`。
- 二進位檔（無文字 diff）不計入檔案數。
- `setting/*.json`（+963）計入 Page 8 的 kernel 彙總，但**不列入 Page 9 的原始碼明細**。兩頁 kernel 數字因此不同：**55 檔 / +5,040**（Page 8）vs **53 檔 / +4,077**（Page 9），差額正好是 963。這是刻意的，兩頁腳註都要說明。
- **簡報上必須註明口徑**，見 Page 8、3 腳註。
- 任何數字改動後，**兩頁一起重生**。

### E4a. 架構圖的畫法（Page 5、5）

兩張都用 `build_deck.js` 裡的 `aBox` / `aText` / `aArrow` / `aDash` / `aCloud` 畫，**上半部共用 `archTop()`**。字體 Arial、框線黑 1pt、白底，座標取自 Adam 的 `NDTwin_Arch.pptx`（`<a:off>` / `<a:ext>`，EMU ÷ 914400 = 吋）。

- 版面關鍵座標：上虛線 y=1.77、kernel 框 y=1.99 h=2.93（底 4.92）、下虛線 y=5.86、雲 y≈6.30 h=1.10、右側 Tools 分隔虛線 x=10.02。
- 新增元素一律 `ACCENT`，既有元素維持全黑——這個對比就是 Page 6 的全部訊息。
- `aArrow(s, x, y, w, h, dir)` 的 `dir`：`"up"`（`flipV` + 箭頭）／`"down"`／`"both"`（雙向）／`"right"`／`"left"`。
- 要再加第三條資料面（例如 physical）時，注意雲寬 4.05" × 2 已經吃滿 0.35→9.35，第三朵得把三朵都縮到 ~3.0"。

### E4c. 節封面頁（本文件編號 Page 3、10、21、27、30、34）

每一節前面一張，**沿用 Page 1 標題頁的版型**，只換文字：

| 元素 | 座標 | 樣式 |
|---|---|---|
| `SECTION n` | x=M, y=2.16 | Calibri 16pt，`ACCENT`，`charSpacing: 1.2` |
| 節名稱 | x=M, y=2.72 h=0.95 | **Cambria 44pt bold**，`INK` |
| 一句話說明 | x=M, y=3.72 h=0.62 | Calibri 20pt，`MUTED` |
| 短橫線 | x=M, y=4.66 w=1.1 | `ACCENT`，2pt |

- 🔵 **v4.5 實際是四張**（第 2 節延後 ＋ 第 3 節拆解，兩節同時消失）：
  `0 Background`（p.3）／`1 New capabilities`（p.10）／
  `2 Test tooling and documentation`（p.19）／`3 Measured results`（p.24）。
  節次標記字串在 `build_deck.js` 是 `"1 · NEW CAPABILITIES"` / `TAB2` / `TAB3`。
  原本的六張清單保留於此，兩節恢復時照舊：
  `0 Background`／`1 New capabilities`／`2 Baseline defects fixed`／`3 Technologies used`／
  `4 Test tooling and documentation`／`5 Measured results`。
- 說明句與 Outline 頁那一列的說明**刻意用同一句**，讓聽眾看到封面時知道「這就是目錄上那一節」。
- 封面頁**有頁碼**（Page 1 沒有）。
- ⚠️ 插入封面頁會讓每一節之後的頁碼全部位移，Outline 頁的 `pp. x–y` 與各頁交叉引用都要重算。
  🔵 **v4.5 起頁碼本身已自動計算**（`newSlide()` 遞增 `PAGE`），**但 Outline 的 `pp. x–y`
  仍然是寫死字串**，而且**各頁內文的「page N」交叉引用也是**。改結構後這兩處要人工對一次。
  目前對照：Background **pp. 4–9**／New capabilities **pp. 11–18**／
  Test tooling **pp. 20–23**／Measured results **pp. 25–40**；收尾 41–43 不列在 Outline 上。

### E4b. 第 3–5 節的版型（2026-08-16 實作，供改版參考）

| 頁 | 版型 | 要點 |
|---|---|---|
| 28 技術棧 | 三欄，每欄「名稱＋一行用途」 | 每項高 **0.52"**（0.66 會壓到底部註記）。底部 marginNote 寬度用 `CW − 0.75`，否則蓋到頁碼 |
| 29 方法論 | 2×2，每格「標題＋說明＋強調色細條的一句佐證」 | 佐證那句寫「它抓到了什麼」，不是重複說明 |
| 30 五層架構 | 4 欄表格 ＋ 底下兩塊並排註記 | 表格 `rowH` 0.46 |
| 31 測試資產 | 四個大數字橫排 ＋ 三段條列 ＋ 右欄兩註記 | 條列間距 1.12，**每段內文上限 2 行** |
| 32 文件資產 | 三欄分類清單（等寬檔名＋一行說明） | 檔名去掉日期前綴顯示比較好讀 |
| 33 L4 差異 | 四個大數字 ＋ 兩段條列 ＋ 右欄註記 ＋ `pending` 佔位 | |
| 34 Failover | 3 欄表格（量測／bmv2／OVS）＋ 兩塊並排註記 | **最後一列用顏色標**：P4 用 `ACCENT`、OVS 用 `WARNC`（`9C3B2E`），那是 Page 24 的 P0 |
| 35 吞吐 A/B | 5 欄表格 ＋ 兩段條列 ＋ 右欄兩註記 | fast build 那列用 `ACCENT` 標 |
| 36 壓力測試 | 四個大數字 ＋ 三段條列 ＋ 右欄註記 | 條列間距 1.10 |
| 37 精確度 | 5 欄表格（寬 7.35"）＋ 兩段條列 ＋ 右欄兩註記 | **標題要短**，長標題會換兩行撞到副標 |
| 38 交叉檢查 | 四個大數字 ＋ 兩段條列 ＋ 右欄註記 | |
| 39 Demo | 三欄，每欄「標題＋說明＋`pending` 佔位」 | |
| 40 收尾 | 左「Delivered」三項／右「Open」八列鍵值表 ＋ 左下註記 | mastership 那段只放一行指標，全文留給 Q&A |

**`pending()` 佔位框**：淡灰底細框 + `TO ADD  <說明>`。目前用在 Page 33（比對輸出）、34（路徑圖）、39（三張畫面）。Adam 補上素材後把這些換成圖。

### E5. 已知的呈現地雷（實際踩過）

1. 架構圖方向弄反（controller 在上）——apps 一定在最上面。
2. 封面用深色底、堆了一堆小字（commit 數、branch 名）——改白底，小字移除。
3. 淡灰字（`A6A6A6` 以下）在投影時看不見。
4. 條列間距抓太緊，兩行以上的說明會撞到下一段標題——留 1.4" 以上並實際渲染確認。
5. 直接用 `git diff --shortstat` 報行數——含註解與空行，會虛胖約 40%。
6. 逐檔清單一次列太多，左欄長度爆出版面撞到腳註——每欄上限約 20 列，其餘摺成一行摘要。
7. 表格右側多欄擠在同一個文字框裡會換行錯位——每個數字欄各自一個右對齊文字框。
8. **同一個數字用兩支腳本各算一次**——一定會兜不攏。跨頁共用的數字要有唯一計算來源（見 E4）。
9. 左欄條列寬度超過右欄起點——文字會蓋到右欄。左右分欄時，**左欄文字寬度 + 左邊界至少要比右欄起點小 0.3"**。
10. 垂直流程圖方框太高——五格 × 0.66" + 四個 0.34" 箭頭就會把圖下腳註推出版面。五格以上用 0.60" / 0.28"。
11. **在 repo 還在動的時候量數字**——08-16 那次前後兩分鐘量出 313 檔 / 314 檔兩個結果，同一天 `p4_proxy/tests` 也從 16 檔/438 變成 17 檔/453。產檔前最後再量一次。
12. **一頁塞四個 `defect()` 會爆版**。可用高度只夠三個（間距 1.5–1.62"）。第四個放右欄，用 `ACCENT` 細條 + 標題 + 一段整合的敘述——Page 23、23 都是這樣處理的。
13. **`listItem` 每段內文超過 2 行就會撞到下一段標題**（間距 1.10–1.12 時）。要嘛縮字數，要嘛把間距開到 1.42 以上並減少段數。
14. **頁標題超過約 45 字元會換兩行並壓到副標**。長話短說，細節放副標。
15. **架構圖的 sFlow 起點畫錯**——P4 那條必須從 proxy 出來，不是從 bmv2 雲。bmv2 不發 sFlow，畫成從雲出來就把整頁的主張講反了。
16. **架構圖的控制器框離 kernel 太近**——留 0.36" 才放得下箭頭旁的標籤，5.16 會讓標籤壓進 kernel 框內。
17. **doc/ 底下的檔名已全部加上日期前綴**（`2026-08-07_testing_tools_overview.md` 這種），且持續有新檔。引用前先 `ls doc/`，不要照抄本文件裡的舊路徑。
18. 🔵 **刪頁之後，別頁的「page N」交叉引用會指向不存在的頁。** v4.5 刪掉第 2 節與兩頁功能頁之後，
    方法論頁還寫著「page 24 是這個方法找到的 P0」（第 2 節的頁）與「pages 16 and 20 是它的實例」
    （page 20 已刪）。**刪頁的同一次就要 grep 一遍 `page \\d`。**
19. 🔵 **副標超過約 140 字元會換兩行、壓到標題底下那條細線。** 實測：141 字元一行、143 字元兩行。
    寫副標時抓 **≤ 130 字元**。
20. 🔵 **表格底部與其下第一個 `listItem` 至少要留 0.12"。** 表格高度 = `rowH` 陣列的總和 + 起始 y，
    算出來就知道下一段能從哪裡開始；憑感覺放一定會壓到編號。
21. 🔵 **頁底的 `Measured at <commit>` 腳註放 y=6.96、寬 `CW − 0.75`。** 放 6.84 會被上面兩行內文追上，
    寬度不減會蓋到頁碼。
22. 🔵 **左欄內文寬度要用「右欄起點 − 左邊界 − 0.3」倒推，不要沿用別頁的數字。**
    Future work 頁右欄在 x=8.42，左欄 x=1.21，所以內文最寬 6.91"——直接抄別頁的 7.6" 就會蓋過去。
    （這是 trap #9 的第三次重犯，所以寫成可計算的式子。）
23. 🔵 **整頁圖不要再加頁標題。** `figures/` 的八張圖都自帶標題與副標，投影片再加一個標題會出現兩層標題。
    圖頁只放左上角節次標記與右下角頁碼，圖片依原始長寬比置中（`figurePage(file, ar)`）。
24. 🟢 **圖重畫之後尺寸會變，而 `ar` 是寫死在呼叫端的——比例錯了不會報錯，只會變形。**
    v4.6 重畫了 raster（2040→2480 寬）與 decomposition（1840×800→1920×980），
    兩個 `ar` 都得跟著改。**換圖後先 `identify -format "%f %wx%h\n" figures/*.png` 對一次。**
25. 🟢 **右欄 `marginNote` 的第五個參數是色條高度，不是文字高度。** 文字短、條長會出現
    一截空的強調色條。加減文字之後**條高要跟著調**：約 `0.3 + 行數 × 0.19`。
26. 🟢 **在兩欄頁的左欄加句子，要先看它下面還有沒有東西。** Page 26 在主句加一句之後，
    就把 `What separating the variables shows` 那個小標壓掉了。**該句改放右欄的註記裡**——
    右欄註記本來就是放「為什麼這些數字站得住」的地方，語意也對。

### E6. 與 Adam 協作的既定慣例

- **對話用中文，投影片用英文**。
- **樣本先行**：大改動先做 3–5 頁樣本給 Adam 看風格，確認後才展開全部頁數。
- **要改投影片，先改這份 template**，再依 template 重生投影片。template 是唯一事實來源。
- **這份 template 的正本在 `~/Desktop/NDTwin Slide material/`**，不是 outputs。Adam 會直接編輯它。動工前先讀最新版。
- Adam 在對話中口頭給的偏好與逐頁修改，**要即時寫回這份文件**，不要只留在對話裡。
- 產出後一定要渲染成圖逐頁檢查；`validate.py` 通過不代表版面沒問題。
- 🔵 **副標的句型（Adam 2026-08-19 訂）**：副標**只介紹這一頁在做什麼**，不放結論、不放賣點。
  範本就是 sFlow 那頁：`bmv2 emits no sFlow of its own — so the proxy manufactures it,
  byte-compatible with what OVS sends`。**結構是「一個事實 → 所以這頁講/量什麼」。**
  ❌ 反例（都已改掉）：`A twin that cannot answer "what happens if I turn this one off" is not
  answering the question it exists for`（是主張不是介紹）、`The count is the least interesting
  number on this page`（機巧但沒說這頁有什麼）。
- 🔵 **不講自己造成的 bug**（Adam 2026-08-19 重申）。baseline 既有的 bug 另開一節，
  而那一節目前延後。所以**現階段整份簡報不出現任何 bug 歸因**。
  受此影響已刪／已改的：`Robustness: defects in my own code` 整頁、Phase 7 的 gRPC subchannel
  註記、Liveness 的「原本 pingWorker 無條件回報 up」、Failover 的「原本會算回死掉的 link」。
- 🔵 **精簡的判準**：一段內文如果口述時一定會講、而投影片上只是把口述寫下來，就只留粗體標題。
  投影片留給「聽的人自己看比較快」的東西：數字、表格、圖。
