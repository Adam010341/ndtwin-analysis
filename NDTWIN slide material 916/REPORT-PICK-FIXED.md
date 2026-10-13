# 從 903 到現在修掉的 bug——依嚴重度排序的候選清單（Adam 挑）

**v2，auditor 2026-09-15 重做**（v1 ＝ 09-08 起草，已過期，勘誤見 §0.1）。
**兩個篩選條件（Adam 09-08）**：① 修的是 **baseline 就已經存在的 bug**；② **足夠嚴重 或 容易觸發**。
🆕 **09-15 Adam 追加**：P4 tutorial 測試中發現「kernel 缺少的東西」也要列進來 ⇒ §3。

挑法：在「挑」欄打勾，或直接回代號（例：`1 3 4 7 12 T1 T2`）。

[Co-developed with claude code -- Adam]

---

## 0.1 🔴 勘誤：v1（09-08）有兩件事現在是錯的

| v1 怎麼寫 | 09-15 的事實 | 怎麼查出來的 |
|---|---|---|
| 「29 支修好**等併**」 | **0 支**。29 支在 09-10 那一夜全部併進 trunk（另 09-11 又併了 4 支新的） | 29 個 tip 逐顆 `git merge-base --is-ancestor <tip> trunk`，29/29 真 |
| 「**0 顆推到公開 repo**」「FIXED ≠ SHIPPED」 | **反過來了：本清單所有 baseline 修法都已公開發布**，在兩個公開 repo 的**預設分支** `main` 上 | 未認證 GitHub compare API：`f11868f6...main` 與 `6c4000eb...main` 兩個 repo 皆 `behind_by: 0` |

**公開狀態（09-15 未認證查證，逐項）**

| ref | Adam010341/NDTwin-Kernel-P4 | ndtwin-lab/NDTwin-Kernel-P4 |
|---|---|---|
| `main`（預設分支，`git clone` 拿到的） | `71e5d0cb`（09-13 README） | `776c20db`（本機沒有這顆） |
| `trunk` | `70615ec5` | `70615ec5` |
| 含全部 baseline 修法？ | ✅ 是 | ✅ 是 |

- 兩個 `main` **都不是 trunk 的祖先**（Adam 自己在上面加了 README commit），但**都含 `f11868f6`** ⇒ 修法齊全。
- trunk 比 main 多的那 10 顆 merge（09-12 那批）**全是 `ndt` 工具與文件**，沒有 baseline 修法 ⇒ 不影響上面的結論。
- ⚠️ **本次查證踩到一個坑要記著**：本 session 第一次 `git ls-remote` 回的 `main` 是**過期的 `f11868f6`**，
  API 與第二次 ls-remote 都回 `71e5d0cb`。**公開狀態要用兩種管道交叉驗，單打一次 ls-remote 會拿到舊答案。**

## 0.2 排序規則（嚴重度怎麼定的）

1. **「分身自信地給出錯答案」排在「東西壞掉」前面**——前者沒有錯誤訊息、會污染所有下游決策與量測；後者會被發現。
2. 同級看**觸發率**：每次操作 100% ＞ 容易 ＞ 少見。
3. 同級看**波及面**：整座 fabric／所有遙測 ＞ 單一端點／單一物件。

狀態一律 ✅＝已在 trunk **且已在公開 `main`**（§0.1 查證）。證據欄 `N/0`＝變異閘 N 個變異 0 存活；`live`＝在 lab 上親自重跑過。

## 0.3 🆕「在 916」欄怎麼讀（Adam 09-16 要求逐列標注）

| 記號 | 意思 |
|---|---|
| 🖼 | 916 素材裡**有專屬的一頁＋一張圖** |
| ✅ | **有專屬的一頁，但沒有專屬圖**（Q12／p.3——而且它不合新規則 6，要改成兩張表） |
| ☐ | **沒有自己的頁**。只在 p.2 那張看板上是一塊磚，上台不會被單獨講到 |

### 🔴 標完之後看到的偏斜，要先講

**一、目前有圖的 baseline 缺陷只有四個機制**：B-6（#5 列）、#54（#6 列）、#27（#12 列），
以及拓樸檔驗證那一族（#27／#28／#29 三列共用 `fig_r3_two_doors_one_field` 一張圖）。
**排名第一與第二的 #10 與 #53 都沒有頁、沒有圖。**

**二、我 09-15 新做的五張缺陷圖裡，只有一張是 baseline。** 逐檔查過：

| 圖 | 缺陷動到的檔 | 首次提交 | 層 |
|---|---|---|---|
| `fig_r3_two_doors_one_field` | `src/ndt_core/collection/TopologyAndFlowMonitor.cpp` | **2025-12-15** | ✅ 第一層 baseline |
| `fig_r2_empty_but_confident` | `tools/test_workflow/ndt` | 2026-08-21 | ❌ 我們自己的工具 |
| `fig_r4_claim_race_window` | `tools/test_workflow/ndt` | 2026-08-21 | ❌ 我們自己的工具 |
| `fig_r12_stolen_marker` | `tools/test_workflow/ndt` | 2026-08-21 | ❌ 我們自己的工具 |
| `fig_r10_sampling_instant` | `tools/test_workflow/ndt` | 2026-08-21 | ❌ 我們自己的工具 |

🔑 **原因是我挑圖的判準錯了**：我挑的是「哪個機制畫成圖最清楚」，**不是「哪個是 baseline 缺陷」**。
夜巡第二夜本來就大量打在 `ndt` 工具上，所以照畫面挑就會挑到一整排自家工具。

**這不表示那四張不能用**——它們是角色扮演那一段最好的教材，因為角色扮演找到的正是這些。
但**擺放位置要對**：它們屬於「這套測試方法找得到什麼」，**不屬於「我們修好了 baseline 的什麼」**。
兩段混在一起講，教授會以為我們修的是別人的系統，其實有一半是自己的工具鏈。

**建議**：baseline 那一段要補圖的話，優先序就是清單的前兩名——`#10`（已有 903 那張，補 after 側）與 `#53`。

---

## 1. 第一層：baseline 的 bug（2025-12-15 第一批碼裡就有的）

| 在 916 | # | 代號 | 一句話（缺陷 → 修法） | 觸發 | 波及 | 修在哪 |
|---|---|---|---|---|---|---|
| ☐ | 1 | #10 | **每條流的速率沒有分母**——除的是迴圈週期不是量到的間隔，所有流速**單向高估**（安靜時 +4.4%、64 流 +24.9%）→ 除以量到的間隔 | 永遠 100% | 所有流速讀數 | ✅ `b76a2493` |
| ☐ | 2 | #53 | **遙測越忙越說謊**——sFlow socket 丟 72.5% 時每個端點照回 `success`，`avg_link_usage` 反而上升 → `status: severe_loss`＋`loss_fraction`＋`offered_in_window`。**修法已把丟包率做成 API，見 §1b** | 高負載 | 所有遙測 | ✅ `ea139d1c` |
| ✅ | 3 | Q12＋#33／#34 | **`is_up` 一個 bit 兩個意思**（命令 vs 觀測）：被命令關的報 OFF、自己死的報 ON；三態檢查兩邊讀同一個 bit ⇒ **結構上永遠不會響** → 拆 `admin_state`＋`reachable` | 任何故障 | 全部決策依據 | ✅ `cdc8dad9`（唯一 breaking change） |
| ☐ | 4 | #46／#36 | **30 s 拓樸輪詢把命令關機的交換機寫回 up**（9 次中 2 次，3.08 s 後復活）⇒ 一次 off 就能讓它死掉而 API 再也救不回 → `adminPoweredOff` 旗標 | 任一 API 關機 | 電源控制全失效 | ✅ `34e2109d` |
| 🖼 | 5 | B-6 | **API 宣告的 link failure 被輪詢靜默撤銷**——宣告的可見壽命上界就是 30 s，沒有任何訊息 → 宣告黏住＋`inject_link_failure/recovery` | 每次宣告 100% | 故障注入全失效 | ✅ `8b51caf4`（live 6/6） |
| 🖼 | 6 | #54 | **`succeeded` 數的是「POST 沒噴錯」不是「交換機變了」**——同一條 match 裝 20 次：`succeeded` +20、交換機 +1；刪 15 次不存在的：+15／+0 → 改名＋第二組「交換機收下」計數 | 永遠 100% | 寫入面全部讀數 | ✅ `31ae5d13`（live 8/8） |
| ☐ | 7 | F-14／F-16／F-4 | **host 永遠標不成 down**；交換機死了它面向 host 的邊仍 up；死鏈路被 `updateHosts` 憑 IP 復活 → 從交換機三態 liveness 推導、連兩輪才標 down | 任何故障 | 拓樸真實性 | ✅ `2bda7af1` |
| ☐ | 8 | #1／A-10 | **`delete_group_entry` 回 200 deleted 而 group 還在**、id 永久洩漏（根因：delete 帶 buckets 被 OVS 拒、Ryu 不回 error）→ 只有交換機確認才宣稱 deleted | 每次 OVS 刪 group 100% | 資源洩漏 | ✅ `d599c476` |
| ☐ | 9 | #2／C-4 | **幽靈規則**：install 後 0.257 s 流表就出現那一列（快取），真列 13.4 s 才到 → 只有裁決性的南向成功才確認條目 | 每次 install 100% | 流表可信度 | ✅ `c2b55184` |
| ☐ | 10 | F-8 | **從未有流量的邊頻寬永久寫死 1 Gbit/s**——10 G 核心邊只宣告十分之一的餘裕 → 讀模型宣告容量＋`_source` 欄 | 永遠（idle 邊） | 容量規劃 | ✅ `dc969792` |
| ☐ | 11 | A-7 | **排隊寫入的失敗對所有 API 不可見** → 接上 `droppedAfterStop()`／dispatcher 存活並公布計數口徑 | 任何寫入失敗 | 寫入面 | ✅ `a4a8eb2c` |
| 🖼 | 12 | #27／#76 | **印出「All subsystems stopped. Exiting.」之後又寫真交換機 10.7 s**，過程 0 行 log；停止請求要等整輪輪詢跑完 → `StopSignal`＋可取消子行程 | 每次關機 100% | 動到硬體 | ✅ `ac703196` |
| ☐ | 13 | A-9 | **租約到期是「條件」不是「事件」**、`isLocked` 從不清 ⇒ 死租約 `unlock()` 仍回 true、遲到的 release 清掉新持有者；Energy-App 每 300 s 放鎖又秒搶回 → 到期即結束、`leaseId` 可驗 | 任何跑 Energy app | 併發控制 | ✅ `49a3f084` |
| ☐ | 14 | B-5／#5 | **kernel 每一次正常關機都 abort**（`stop()` 少 join 一條 thread ⇒ `std::terminate`）——文件描述的乾淨關機路徑從來沒被執行過 → 補 join | 每次關機 100% | 收尾全失效 | ✅ `0e11c229`（SIGINT 7/7 exit 0） |
| ☐ | 15 | B-2b／B-4 | **kernel 自己拼 shell 字串**：一個單引號就讓它指控健康元件有問題；含引號的模擬案例回 202 但從沒送出 → `execArgv` 免 shell＋全站掃描 | 任何引號（容易） | 注入面 | ✅ `4c49b050` |
| ☐ | 16 | A-2 | **Ryu `get_link()` 無界** ⇒ 拓樸輪詢可永久阻塞而沒有人發現 → vendor 一份有界的 | Ryu 卡住（少見） | 拓樸全停 | ✅ `404b11a8` |
| ☐ | 17 | B-x | `get_detected_flow_data` **含已結束的流**（churn 下 ~92% 是 idle）→ 三態 `active`／`idle`／`ended`，預設只回 active | 流 churn | 流量視圖 | ✅ `cc9a9ea4` |
| ☐ | 18 | F-1 | MININET 下 **CPU／記憶體／溫度是交換機 IP 的常數函數**（四處捏造點）→ 一律回哨兵 `-1` | MININET 永遠 | 假數字 | ✅ `b259c4d9` |
| ☐ | 19 | F-6 | **讀流表失敗的交換機被整份沖掉**，而四處註解承諾「保留前一份」→ 保留最後一份＋`stale_since`／`stale_polls` | 暫時讀失敗 | 流表視圖 | ✅ `fc2cd427` |
| ☐ | 20 | F-13 | 對**不存在**的 group／meter 做 modify／delete 回 200，install 打已存在的也回 200（12 格 6 格錯、回應完全相同）→ 先問交換機在不在 | 容易 | API 誠實度 | ✅ `9430bfbe` |
| ☐ | 21 | B-3 | historical logging 回 200「已啟用」但**一列都不寫**（MININET 早退）→ 維持 200 但 `status: not_applicable`＋穩定 reason | MININET 永遠 | 記錄 | ✅ `bac267cb` |
| ☐ | 22 | #64／#65 | 端點回 **500 的錯誤 body 被當答案**餵進 `updateLinks` → 分類 `reported_failure`／`wrong_shape` | 任一端點出錯 | 拓樸 | ✅ `d00fa57c` |
| ☐ | 23 | #88／#85 | 未守衛的 `ip.front()`／`ip[0]` **全樹 24 處**；一台沒有位址的 switch 讓 status worker **SIGSEGV** → 逐處守衛 | 出貨檔不會、手寫檔會 | 崩潰 | ✅ `cff98191`＋`9ba1523a`＋`f4559c57` |
| ☐ | 24 | #47 | 子行程繼承 kernel 的 listening socket ⇒ **kernel 死了 port 還被 app 佔著**、擋下一次啟動 → CLOEXEC | kernel 掛時有子行程 | 重啟 | ✅ `08267dcb` |
| ☐ | 25 | #59 | 拓樸檔壞 IP 在執行緒裡 throw ⇒ **abort 且 port 已開**；檔案不見照樣空圖開機 → 綁 port 前失敗 | 容易 | 啟動 | ✅ `70c324e1` |
| ☐ | 26 | B-10 | 改一個 nickname，**kernel 就把使用者的模型檔改寫** ⇒ `--check` 一定紅 → overlay 檔、模型檔只讀 | 任何改名 | 使用者檔案 | ✅ `0584f1b5`（live 9/9） |
| 🖼 | 27 | 拓樸檔驗證一族 | 壞內容被**靜默收下**：edge 指到不存在節點、port 越界、無位址 host、未知 `brand_name` 映成 hardware、`vertex_type` 範圍外（檔案面全收但 API 面 400）→ 第一個 vertex 進圖前整檔拒絕 | 使用者寫錯檔（容易） | 帶著錯圖開機 | ✅ `e9d8a486`／`336d831e`／`8cdf299e`／`e80bd013`／`389d4d1d` |
| 🖼 | 28 | 🆕 B-15 | **寬鬆寫法的位址（`["10.1"]`）讓兩台 host 共用一個位址**，而查找只回第一個 → 拒絕 | 手寫檔 | 靜默錯路由 | ✅ `389d4d1d`（09-11） |
| 🖼 | 29 | 🆕 B-13 | **`link_bandwidth_bps: 0` 一扇門都不擋** ⇒ 被取樣到的邊利用率變 `null` → 檔案面加門 | 手寫檔 | 利用率 | ✅ `389d4d1d`（09-11） |
| ☐ | 30 | #38 | 連線被拒（6–9 ms）被印成「**30 秒逾時**」→ 讀 curl exit code、時間改成量到的 | sim app 沒起（容易） | 誤導除錯 | ✅ `27d48eda` |

## 1b. 🆕 #53 的修法：丟包率現在是 API 的一等公民（09-16 讀碼查證）

Adam 09-16 問「現在有 API 在回報丟包率嗎？沒有的話要不要做？」——**已經有了，而且不只一個入口，不用再做。**

| | 查到什麼 | 出處 |
|---|---|---|
| 專屬端點 | `GET /ndt/get_sflow_stats` | `src/ndt_core/http/HttpSession.cpp:504` |
| **掛進別的端點的回應** | 其他端點的 body 也帶 `telemetry_health` 區塊 | `HttpSession.cpp:3360`、`:3386` |
| 掛進每一列流量資料 | `j["telemetry_health"] = health` | `FlowLinkUsageCollector.cpp:2553` |

**回應帶的欄位**（`FlowLinkUsageCollector.cpp:1838-1857`，我逐行讀過）：

| 欄位 | 是什麼 |
|---|---|
| `status` | `ok`／`lossy`／`severe_loss`／`no_samples` |
| `loss_fraction` | 丟包率本身 |
| `samples_in_window`／`offered_in_window`／`dropped_in_window` | **分子與分母都給**，讀者可以自己重算、不同意我們的門檻也不必再打一次 API |
| `socket_drops_in_window`／`app_drops_in_window` | 丟在 socket 層還是應用層，分開算 |
| `window_seconds` | 這組數字涵蓋多久 |
| `rx_total`／`addressed_total`／`sock_ovfl_total`／`app_drop_total` | 自啟動以來的累計，給自己記基線的消費者 |

**門檻**：丟包率 > 1% ＝ `lossy`，≥ 10% ＝ `severe_loss`（`FlowLinkUsageCollector.hpp:416,418`）。

🔑 **兩個設計細節值得上台講**，它們正好回應「分身會不會說謊」這個主軸：

1. **沒有「四捨五入成 ok」**。碼裡的註解逐字寫著：低於 lossy 門檻的丟包**仍然是丟包**，
   第 4 輪那格 150000/s 丟了 0.34% 而且確實低報了，**誠實的答案是 `lossy`，不是「ok 加一個註腳」**。
2. **`status` 與 `telemetry_health` 是兩件事**，碼裡也註明了：
   前者說的是**這個請求**成不成功，後者說的是**這個答案**可不可信。#53 的病灶正是這兩件事以前只有一個欄位。

⇒ **不用做新的。要做的是把它放上台**：#53 目前**沒有頁也沒有圖**，而它在嚴重度上排第二。

## 2. 第二層：Adam 07-23 之後加的產品碼（不是 baseline，但嚴重／容易觸發）

| 在 916 | # | 代號 | 一句話 | 觸發 | 修在哪 |
|---|---|---|---|---|---|
| ☐ | 31 | A-4d | **P4 上「裝一條規則再刪掉」把目的地打成黑洞**（install／delete 共用 `dst/32` LPM 槽）→ delete 把槽原地還給控制面（MODIFY、零空窗） | 每次 P4 delete | ✅ `8b87a9de` |
| ☐ | 32 | #4／A-12 | **`ovs4` 十座 bridge 完全沒配 sFlow** ⇒ 分身看到的流量結構性為零 → 全配 | ovs4 100% | ✅ `5e355dda`（live 0→0.504） |
| ☐ | 33 | A-4f | OVS 電源循環的 `del-br` 帶走 sFlow 設定、開機不重建 ⇒ **該鏈路遙測永久歸零且與 idle 不可分辨** → 關機存、開機回放並回讀 | 每次 OVS power cycle | ✅ `36e3d78a` |
| ☐ | 34 | A-4c | P4 proxy 重啟**無條件清空所有表**而 twin 不會說 → 公布 `boot_id`／`table_generation` | 每次 proxy 重啟 | ✅ `0da64329` |
| ☐ | 35 | #32／#45 | 啟動競態（`refreshDataPlaneKind` 早 1 ms 且只算一次）⇒ **bmv2 liveness 路徑從不執行**（出貨檔 0/44） | 出貨檔 100% | ✅ `0b34af5f` |
| ☐ | 36 | 🆕 B-16 | **`POST /ndt/inject_link_recovery` 會拆掉不是它掛的 netem**，回 200 `ok:true`，一個字都不提來歷——會清掉別人實驗的狀態 | 每次 recovery | ✅ `6c4000eb`（09-11） |
| ☐ | 37 | 🆕 proxy pkill | `p4_proxy` 啟動重置跑 `sudo pkill -f simple_switch_grpc`——**用行程名殺**，會連別人 session 的交換機一起殺 → 改由 manifest 的 pid 收 | 每次 P4 啟動 | ✅ `526ad7c5`（09-11、8/0） |
| ☐ | 38 | 🆕 A8 | gRPC port 沒清掉時只印 warning，然後**起一座少一台的 fabric（9/10）照樣量** → FATAL＋`exit(1)` | 偶發 | ✅ `892fdbdc`（09-12、12/0） |
| ☐ | 39 | F-15 | bmv2 gRPC 50051–60 落在本機 ephemeral 範圍會被搶走，而**部分 fabric 起不來仍 exit 0** → 改 30051–60、起不全即 fatal | 偶發 | ✅ `33338e15` |
| ☐ | 40 | #82 | OVS `powerOff` 的 `!isUp` 早退（關一台已經 down 的就靜默不做事）→ 問 `br-exists` 三值判定 | 關已 down 的機 | ✅ `3d2b38fe` |
| ☐ | 41 | P4 priority | P4 上 `priority` 被**靜默丟棄** → 501 取代假成功（09-11 補上 `remedy` 欄說明為什麼不可能支援） | 任何帶 priority 的規則 | ✅ `323668ad`＋`526ad7c5` |
| 🖼 | 42 | `ndt`／lab 工具族 | 失敗的 `up` 不回滾、`apps stop` 只殺 wrapper（JVM 活了 1h54m 而三個通道都說沒在跑）、寫死路徑、四處 `pkill -f`、sudo 守衛永不觸發、擋啟動的 port 看不到、`--check` 假紅、跑錯 topo | 手冊路徑上都會踩 | ✅ 09-03～09-12 全在 trunk |

## 3. 🆕 P4 tutorial 測出來的「kernel 缺少的東西」（不是 bug，是缺能力）

方法：拿 `p4lang/tutorials` 的 **13 支 exercise 當真實需求**，×16 個能力維度逐支讀碼對表。
正本 `doc/audit/2026-09-04_p4-tutorial-exercise-prep/GAP-ANALYSIS.md`。
🔴 **誠實聲明**：五個 gap **全部是【讀碼推導】**，一條都沒在 NDTwin 上驗證過；exercise 本身 09-08 在 **tutorials 自己的 Mininet** 上實跑 4/4 綠，**在 NDTwin fabric 上仍是 0/13**。
⚠️ 這裡的 `G` 是 GAP 編號，**與 KNOWN-ISSUES 的 `G-nn` 不同系**，上台請用左邊的 T 代號。

| 在 916 | 代號 | 原號 | 缺什麼 | 擋住幾支 | 今天寫死在哪 | 改法【估】 |
|---|---|---|---|---|---|---|
| 🖼 | T1 | G2 | 拓樸只認「主機數」選檔、proxy 用四等分公式推主機位置、交換機清單寫死十台；**逐連結頻寬完全沒被套用** | **13/13** | `p4_testbed_topo.py:120-134` | 三處改讀拓樸檔＋`TCLink`，~85 行 |
| 🖼 | T2 | G4 | 只推得動**一份寫死路徑的 pipeline**，十台同一份、跑時換不了 | **12/13** | `main.py:185-186` | per-dpid manifest，~150 行 |
| 🖼 | T3 | G5 | 表名／action 名／參數名／key 位寬**全寫死在三張自家表上**，且**沒有任何 `default_action` 寫入路徑** | **12/13** | `p4_client.py:846` | 旁路 `POST /p4/table_entry`，~180 行 |
| 🖼 | T4 | G1 | packet-in metadata id 是**位置相依的裸常數 1..5** ⇒ 換一支 P4 程式，遙測靜默歸零 | 12 支的遙測 | `sflow_emitter.py:425-429` | 由 p4info 按名字解析，~40 行 |
| 🖼 | T5 | G6 | 觀測面 **IPv4-only**：`etherType != 0x0800` 整包丟、`FlowKey` 只有 IPv4 五元組 | 6 支「轉得動、分身全盲」 | `FlowLinkUsageCollector.cpp:1266` | 分兩層，~30＋~250 行 |
| 🖼 | T6 | 發現① | **靜默歸零**：遙測鏈路依賴 NDTwin 自己那支 `.p4` 的欄位順序，換一支程式後每個速率／使用率都是 **0 且沒有任何錯誤訊息** | — | 同 T4 | 【讀碼推導】 |
| 🖼 | T7 | 發現② | **冒名者清空全表還回報成功**：tutorials 自帶的 `mycontroller.py` 與 proxy 的十個 client 投**同一個寫死的 election_id (0,1)**，它的 `SetForwardingPipelineConfig` 會被接受、清空每一張表、再回報成功 | — | `p4_client.py:60-72` | 🟢 **【跑過】**（08-13 mastership 實測） |

**T6／T7 的價值**：這兩條是「**測 tutorial 才會暴露**」的——自家 P4 程式永遠不會踩到。
**T7 是這一節唯一有實測的**，也是唯一一條「安全性」形狀的（無認證的控制面搶佔）。

## 4. 找到但**沒修**（想順口帶就挑，口徑＝「量到了、還沒修」）

| 在 916 | 代號 | 一句話 | 證據等級 |
|---|---|---|---|
| ☐ | N1 | 🆕 **C-9** 遙測停更時 `usage_bps` 回 **0** 而不是回「不知道」——只有另外兩個欄位分得出來（`telemetry_status=silent`、`last_sample_age_seconds` 一路長到 172.5 s） | 🟢 09-11 實測 |
| ☐ | N2 | **B-9** OVS 一次 power off→on 讓 **ofport 靜默重映射** ⇒ 底下 32 台主機永久斷，而四種儀器全綠 | 🟢 2/2 重現＋三個對照組 |
| ☐ | N3 | **C-4b** delete 之後 read-back 仍回報已刪的規則 **9.61 s** | 🟢 實測 |
| ☐ | N4 | 🆕 **C-8** `last_sample_age_seconds` 在一個「秒」欄位裡回 **−1.0 哨兵值** | 🟢 09-11 實測 |
| ☐ | N5 | 🆕 **B-17** sFlow counter sample 的 `ifSpeed = 0` 讓利用率變 `null`，而檔案面的門關不到它 | 🔵 讀碼、**未實測** |
| 🖼 | N6 | **`get_path_switch_count` 不讀活拓樸**——32/40 與 20/40 交換機間邊判 down 前後，12 條路徑的 `switch_count` 逐格相同（OVS 三個狀態都回 5） | 🟢 09-04 實測，**已有圖** `fig5` |

不要寫成 fixed：boot-ring deadlock（DEFECT-INVENTORY A-1）兩個修法都未驗證。

## 5. 上台怎麼講（三句，v2 已改口徑）

1. 「09-03 之後 trunk 多了 **104 支**修法，**全部已經公開發布**；其中**本清單 §1 的 30 條是 baseline 缺陷**，其餘多數是工具與測試面。」
   （**數字怎麼來的**：47＝09-03→09-05，沿用 v1 §1 的定義（不含純文件）；57＝`git log --merges cdc8dad9..trunk` 69 顆扣掉 12 顆純文件／KNOWN-ISSUES。兩段相加 104。）
2. 「絕大多數修法有**變異閘門看過紅**（沒看過紅不算交付）；例外逐格寫在正本的證據欄。標 live 的是在 lab 上親自重跑過的。」
3. 「P4 tutorial 當需求測出五個**缺的能力**——那不是 bug，是我們還沒做；其中兩條是**測別人的程式才會暴露**的。」

🔴 **v1 的第三句（「Q12 修在 trunk 但使用者拿不到」）不要再講**——09-12 之後不成立了。

## 6. auditor 建議的八條（Adam 09-15：「挑 5~10 個，挑適合拿來展示的」）

**挑選標準**（與 §0.2 的嚴重度不同，這裡加了「展示適性」）：① **已經有圖**（09-04 夜巡六張，零新工）；
② **有成對的數字**（宣稱 vs 真相），一進表格就說得完，符合 §0 規則 6；③ 一句話講得完，不必鋪陳背景。

主軸建議叫「**分身自信地說錯話的四種形狀**」——這是有結構的框架，不是 bug 流水帳。

| 序 | 代號 | 上台那句 | 成對數字 | 圖 |
|---|---|---|---|---|
| 1 | #10 | **數錯**——速率沒有分母。🔴 **見下方警告：這條 903 已經講過了** | 見下 | 903 已用過一張 |
| 2 | #53 | **越忙越錯**——丟包時反而報更高的使用率 | 丟 72.5% 仍每個端點 `success` | 要新圖 |
| 3 | #54 | **數的是自己不是世界**——成功計數數的是 POST 沒噴錯 | 裝同一條 20 次：計數 +20／交換機 +1；刪 15 次不存在的：+15／+0；對照組 1／1 | ✅ `fig3` |
| 4 | #2 | **快取搶在真相前面** | 流表 0.257 s 就有那一列，真列 13.4 s 才到 | 要新圖（時間軸） |
| 5 | B-6 | **狀態會自己漂回去**——宣告的斷鏈活不過一輪輪詢 | 自己翻回 25.4／24.4／23.4／22.5／21.5 s；真斷鏈 ≥60 s 不自癒 | ✅ `fig1` |
| 6 | #27 | **說停了之後還在動硬體** | Exiting 之後 10.743 s 還在寫真交換機、0 行 log；idle 對照 ≈2.4 s | ✅ `fig2` |
| 7 | Q12 | **一個 bit 兩個意思** | 命令關機後 0.3–1.5 s 被寫回 true、撐 8–13 s（兩臂 18/18） | 已是 p.3 |
| 8 | T7 | **測別人的 P4 程式才暴露的**：十個 client 共用寫死的 election_id，冒名者清空全表還回報成功 | 🟢 唯一有實測的 gap | 要新圖（序列圖） |

**備援**（想換掉上面哪條時的同級替補）：#1（刪 group 回 200 但還在）、#46（輪詢寫回 up，與 Q12 同根、會重複）、
N2（B-9 ofport 重映射：32 台主機永久斷而四種儀器全綠——**未修**，當「還在追的」講很有力）。

### 🔴 一個要先決定的前提：09-04 那三張圖只有 before 側

`fig1`／`fig2`／`fig3` 是 **09-04 量的 current behaviour**，當時 binary 沒重建 ⇒ **沒有 after 側**。
而序 3／5／6 的修法**現在都在 trunk 且已公開**（#54→`31ae5d13`、B-6→`8b51caf4`、#27→`ac703196`）
⇒ **現在重跑就能做出真的 before/after**，那正是 Adam 09-04 明講要的形狀。

| 選項 | 代價 | 結果 |
|---|---|---|
| (a) 就用現有三張，標 `current behaviour @ 09-04` | 0 | 只能講「我們量到」，不能講「修好了長這樣」 |
| (b) 在修好的 binary 上重跑這三項，補 after 側 | 一輪 lab（lab 現在空、無 claim） | 三張真 before/after；professor 要的圖 |

**沒有 after 側就不要硬畫**——(a) 的圖上與講稿都必須寫 `current behaviour`，不可暗示是修後的樣子。

### 🔴 #10（分母）特別註記：903 已經講過 found 側

Adam 09-15 提供的 903 投影片截圖＝**這一條**（標題 `The denominator was assumed to be 1.000 s. It never was.`，
左圖 stem 1.0331／1.0396／1.0609／1.0486／1.0324 對紅線 1.000，右圖 +3.3／+4.0／+6.1／+4.9／+3.2%）。
確認同一個缺陷：`FlowLinkUsageCollector.cpp:1934-1936`／`:1952-1954`，分子是一個迴圈週期內的位元組，
掛「每秒」的名字送出（正本 `doc/audit/2026-09-02_live-round/FLOW-RATE-DENOMINATOR.md`）。

**⇒ 依 delta-only，found 側不可重講。可講的只有 delta ＝「修好了」。** 但是：

| | 狀態 |
|---|---|
| 修法 | ✅ `6088c0b5`「Divide the per-flow rates by the interval they accumulated over」→ trunk `b76a2493` 09-03，已公開 |
| **after 側量測** | ❌ **從來沒有量過**。碼裡已經有儀器（`:2184` 印 `rate divisor check: measured_interval_s=… divisor_used_s=…`），但沒有人跑過並存檔 |

🔴 **不要把 `+24.9%` 跟那張投影片並排**。它是**第一代 fabric（08-25）**的數字，而且出處是
`FlowLinkUsageCollector.hpp` 註解裡轉述的 `windowed mean 1248.7 ms`，不是那一輪量的。
投影片自己畫了一條 **4.2 點的雜訊底線**，五根棒子裡只有兩根超出去——把 24.9% 放上去會和它直接打架。
同理 `+4.4%` 是**安靜臂**、對 1 流而言是**上界**，正本明寫「不要把 +4.4% 當成 1 流的實測值」。

**建議**：序 1 改成**同一張圖加上 after 側**（「你 9/3 看過這張，現在右邊多一半」）——
delta-only 成立、圖已存在、而且是 professor 要的 before/after 形狀。
**前提是先跑一輪把 after 側量出來**（與上面 (b) 同一輪做掉）。不跑的話，**序 1 換成備援的 #1 或 N2**。
