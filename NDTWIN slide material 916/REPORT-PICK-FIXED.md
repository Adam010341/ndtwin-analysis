# 從 FIXED-SINCE-903 挑上台的修法——候選清單（Adam 挑）

auditor 09-08 晚起草。**兩個篩選條件（Adam 09-08）**：① 修的是 **baseline 就已經存在的 bug**；② **足夠嚴重 或 容易觸發**。

[Co-developed with claude code -- Adam]

## 0. 「baseline」怎麼判

- repo 的第一批碼＝**2025-12-15**（joemou／patty 的 kernel：`TopologyAndFlowMonitor`、`FlowLinkUsageCollector`、`DeviceConfigurationAndPowerManager`、`SimulationRequestManager`、`HttpSession`、`Controller`、`GraphTypes`…）——這些檔裡的 bug ＝ **baseline**。
- **2026-07-23 之後 Adam 加的**：`OVSPowerStrategy`／`P4PowerStrategy`（07-23）、`p4_proxy/`（07-23）、`testbed_topo.py`（07-23）、`tools/test_workflow`（`ndt`，07-27）、`HttpRoutingStrategyBase.cpp`（07-28，🟡 可能是 baseline 邏輯搬過來的）——這些的 bug 是產品 bug，但**不是 baseline**，另列第二層。
- 我們自己的儀器／harness／閘門／文件的 bug（L-x、G-3、G-5、#17、#75、#78、A-8 三工具、KIREF、E-17 …）**不列**。
- 嚴重度取 FINDINGS-ALL 的「嚴重／中等」與 REPORT-PICK-0908 的重現次數；「觸發」寫的是**使用者在什麼操作下會踩到**。修在哪：✅ trunk（附進線 commit）／🔧 分支（附 tip）。

## 1. 第一層：baseline 的 bug（★＝我建議上台，○＝可選）

| # | 代號 | 一句話（缺陷 → 修法） | 觸發 | 嚴重 | 修在哪 | 建議 |
|---|---|---|---|---|---|---|
| 1 | B-5／#5 | kernel **每一次**正常關機都 abort（`stop()` 少 join 一條 thread ⇒ `std::terminate`），文件描述的乾淨關機路徑從來沒執行過 → 補 join；SIGINT 7/7 exit 0 | 每次關機，100% | 中高 | ✅ `0e11c229` 09-03 | ★ |
| 2 | #27／#76 | 印出「All subsystems stopped. Exiting.」之後又寫真交換機 10.7 s、0 行 log；停止請求要等整輪輪詢跑完 → `StopSignal`＋可取消的子行程 | 每次關機 | 高（動到硬體） | ✅ `ac703196`（本體 `63792cc9`）09-04 | ★ |
| 3 | #46／#36 | API 命令關機的交換機被 30 s 拓樸輪詢寫回 up（9 次 2 次，3.08 s 後）⇒ 一次 off 就能讓交換機死掉且 API 再也救不回 → `adminPoweredOff` 旗標、輪詢不抬 `isUp` | 任一 API 關機 | 高 | ✅ `34e2109d` 09-03 | ★ |
| 4 | Q12＋#33／#34 | `is_up` 一個 bit 兩個意思：被命令關的報 OFF、自己死的報 ON；三態檢查結構上永遠不會響 → `admin_state`＋`reachable` | 任何故障 | 高（決策依據） | ✅ `95a9f743`→`cdc8dad9` 09-05 | ★（已是 p.3） |
| 5 | #1／A-10 | `delete_group_entry` 在 OVS 上回 200 deleted 而 group 還在、id 永久洩漏（根因：delete 帶 buckets 被 OVS 拒、Ryu 不回 error）→ 只有交換機確認才宣稱 deleted | 每次 OVS 刪 group，100% | 高 | ✅ `d599c476` 09-04 | ★ |
| 6 | #2／C-4 | B-1 幽靈規則過濾器沒蓋 OVS：install 後 0.257 s 表就出現快取列、真列 13.4 s 才到 → 只有裁決性的南向成功才確認條目（🟡 缺陷是 baseline 的「排隊列當流表服務」，漏洞在 08 月我們的補丁沒蓋到 OVS） | 每次 install，100% | 中高 | ✅ `c2b55184` 09-04 | ★ |
| 7 | #10 | 每條流的速率沒有分母（誤差＝迴圈週期，安靜 +4.4%、64 流 +24.9%，單向高估）→ 除以量到的間隔 | 永遠 | 高（所有既存讀數偏高） | ✅ `b76a2493` 09-03 | ★ |
| 8 | #53 | sFlow socket 丟 72.5% 時每個端點照回 success、`avg_link_usage` 反向上升 → 回應帶 `status: severe_loss`＋`loss_fraction`＋`offered_in_window` | 高負載 | 高（量測說謊） | ✅ `ea139d1c` 09-03 | ★ |
| 9 | A-9 | `routing_lock` 租約到期是條件不是事件、`isLocked` 從不清 ⇒ Energy-App 每 300 s 放鎖又秒搶回（TR-5 三臂 0 台被關的原因）→ 到期即結束、`leaseId` 可驗 | 任何跑 Energy app | 高 | ✅ `49a3f084` 09-02 | ★ |
| 10 | B-2b／B-4 | kernel 自己拼 shell 字串：一個單引號讓它指控健康元件；模擬案例含引號回 202 但從沒送出 → `execArgv` 免 shell（🟡 檔是 07-28 的，邏輯疑為搬來的） | 容易（任何引號） | 高（注入面） | ✅ `4c49b050` 09-02 | ★ |
| 11 | F-14／F-16／F-4 | host 永遠標不成 down；交換機死了它面向 host 的邊仍 up；死鏈路被 `updateHosts` 憑 IP 復活 → 從交換機三態 liveness 推導、連兩輪、`down_reason` | 任何故障 | 高 | ✅ `2bda7af1` 09-02 | ★ |
| 12 | A-7 | 排隊寫入的失敗對所有 API 不可見 → 接上 `droppedAfterStop()`／dispatcher 存活、公布計數口徑 | 任何寫入失敗 | 高 | ✅ `a4a8eb2c` 09-02 | ★ |
| 13 | F-8 | 從未有流量的邊 `left_link_bandwidth_bps` 永久寫死 1 Gbit/s（10 G 核心邊只宣告十分之一餘裕）→ 讀模型宣告容量＋`_source` 欄 | 永遠（idle 邊） | 中高（capacity planning） | ✅ `dc969792` 09-02 | ★ |
| 14 | B-6 | API 宣告的 link failure 被 30 s 拓樸輪詢靜默撤銷（可見壽命上界 30 s）→ 宣告黏住＋`inject_link_failure/recovery` 端點 | 每次宣告，100% | 高 | 🔧 `fix/w8-declared-link-failure-sticky` `017c060f`（lw8 6/6）→ W8b `8a3f71d1` | ★（要講「分支上」） |
| 15 | B-x | `get_detected_flow_data` 含已結束的流（churn 下 ~92%）→ 三態 active／idle／ended，預設只回 active | 流 churn | 中高 | ✅ `cc9a9ea4` 09-02 | ○ |
| 16 | F-1 | MININET 下 CPU／記憶體／溫度是交換機 IP 的常數函數（四處捏造點）→ 一律回哨兵 `-1` | MININET 永遠 | 中（假數字） | ✅ `b259c4d9` 09-02 | ○ |
| 17 | A-2 | Ryu `get_link()` 無界 ⇒ 拓樸輪詢可永久阻塞而沒人發現 → vendor 有界版 | Ryu 卡住（少見） | 高 | ✅ `404b11a8` 09-02 | ○ |
| 18 | #61／#62＋#89＋B-11／B-12 | 拓樸檔壞內容被靜默收下：edge 指到不存在節點、port 越界、無位址 host、未知 `brand_name` 映成 hardware → 第一個 vertex 進圖前整檔拒絕 | 使用者寫錯檔（容易） | 中（帶著錯圖起來） | ✅ `e9d8a486`／`336d831e`；🔧 `72ffd4dd`／`8b3ebe49` | ○ |
| 19 | #88／#85 | 未守衛的 `ip.front()`／`ip[0]` 全樹 24 處，一台沒位址的 switch 讓 status worker SIGSEGV | 出貨檔不會；手寫檔會 | 高（崩潰）但難觸發 | ✅ `cff98191`（W2）；🔧 W14 `e62c8d6f`→W18 `67204ecc` | ○ |
| 20 | #47 | 子行程繼承 kernel 的 listening socket ⇒ kernel 死了 port 還被 app 佔著、擋下一次啟動 → CLOEXEC | kernel 掛時有子行程 | 中 | ✅ `08267dcb` 09-03 | ○ |
| 21 | #64／#65 | 端點回 500 的錯誤 body 被當答案餵進 `updateLinks` → 分類 `reported_failure`／`wrong_shape` | 任一端點出錯 | 中 | ✅ `d00fa57c` 09-03 | ○ |
| 22 | #59 | 拓樸檔壞 IP 在執行緒裡 throw ⇒ abort 且 port 已開；檔案不見照樣空圖開機 → 綁 port 前失敗、拒絕啟動 | 容易 | 中 | ✅ `70c324e1` 09-03 | ○ |
| 23 | F-13 | 對不存在的 group／meter 做 modify／delete 回 200（12 格 6 格錯）→ 先問交換機在不在 | 容易 | 中 | ✅ `9430bfbe` 09-02 | ○ |
| 24 | F-6 | 讀流表失敗的交換機被整份沖掉，四處註解承諾「保留前一份」→ 保留最後一份＋`stale_since` | 暫時讀失敗 | 中 | ✅ `fc2cd427` 09-02 | ○ |
| 25 | B-3 | historical logging 回 200「已啟用」但一列都不寫（MININET 早退）→ `status: not_applicable` | MININET 永遠 | 中 | ✅ `bac267cb` 09-02 | ○ |
| 26 | #54 | `succeeded` 數的是「POST 沒噴錯」：同 match 裝 500 次 succeeded +500、交換機 +1 → 改名＋「交換機收下」第二組計數＋request id | 永遠 | 中（誤導） | 🔧 `fix/w11-dispatch-status-accepted-counters` `8c8a0fe4`（lw11 8/8） | ○（fig3 已量） |
| 27 | B-10 | 改一個 nickname，kernel 就把模型檔改寫 ⇒ `--check` 一定紅 → overlay 檔、模型檔只讀 | 任何改名 | 中 | 🔧 `fix/w10-nickname-overlay` `52224425`（lw10b 9/9） | ○ |
| 28 | #38 | 連線被拒（6–9 ms）被印成「30 秒逾時」→ 讀 curl exit code | sim app 沒起（容易） | 低 | ✅ `27d48eda` 09-04 | ○ |

## 2. 第二層：Adam 07-23 之後加的產品碼（不是 baseline，但嚴重／容易觸發）

| # | 代號 | 一句話 | 觸發 | 嚴重 | 修在哪 |
|---|---|---|---|---|---|
| 29 | A-4d | P4 上「裝一條規則再刪掉」把目的地打成黑洞（install／delete 共用 `dst/32` 槽）→ delete 把槽還給控制面 | 每次 P4 delete | 高 | ✅ `8b87a9de` 09-02 |
| 30 | A-4c | P4 proxy 重啟無條件清空所有表而 twin 不說 → 公布 `boot_id`／`table_generation` | 每次 proxy 重啟 | 高 | ✅ `0da64329` 09-02 |
| 31 | A-4f | OVS 電源循環 `del-br` 帶走 sFlow 設定 ⇒ 該鏈路遙測永久歸零、與 idle 不可分辨 → 關機存、開機回放 | 每次 OVS power cycle | 高 | ✅ `36e3d78a` 09-02 |
| 32 | #32／D15 | 啟動競態：`refreshDataPlaneKind` 比拓樸早 1 ms 且只算一次 ⇒ bmv2 liveness 路徑從不執行（出貨檔 0/44）→ 載入同步、判定不 latch | 出貨檔 100% | 高 | ✅ `0b34af5f` 09-03 |
| 33 | #82 | OVS `powerOff` 的 `!isUp` 早退 → 問 `br-exists` 三值判定 | 關一台已 down 的交換機 | 中 | ✅ `3d2b38fe` 09-04 |
| 34 | #4／A-12 | `ovs4` 拓樸十座 bridge 全沒配 sFlow ⇒ 分身流量結構性為零 | ovs4 100% | 高 | ✅ `5e355dda` 09-03 |
| 35 | #42／G-10 | `testbed_topo.py` 128 對 ping 全丟而 banner 印三個 OK | 100% | 中 | ✅ `014903fb` 09-03 |
| 36 | P4 priority | P4 上 `priority` 被靜默丟棄 → 501 | 任何帶 priority 的規則 | 中 | ✅ `323668ad` 09-03 |
| 37 | F-15 | bmv2 gRPC 50051–60 落在 ephemeral 範圍會被搶、起不全仍 exit 0 → 30051–60、起不全即 fatal | 偶發 | 中 | ✅ `33338e15` 09-02 |
| 38 | A-11／#3、G-11／#6、G-7、G-9、A-14、#22–24、#8、#77 | `ndt` 與 lab 工具那一族（失敗的 up 不回滾、apps stop 只殺 wrapper、寫死路徑、`pkill -f`、sudo 守衛永不觸發、擋啟動的 port 看不到、`--check` 假紅、跑錯 topo） | 手冊路徑上都會踩 | 中 | ✅ 全在 trunk 09-03／09-04 |

## 3. 不在清單裡、但你可能想順口帶的（未修）

- **B-9**：OVS 一次 `set_switches_power_state` off→on 讓 ofport 重映射 ⇒ 底下 32 台主機永久斷而四種儀器全綠（2/2 重現＋三個對照組）——**只登記未修**（`2285c63c`；W9 只開單）。
- **C-4b**：delete 之後 read-back 仍回報已刪規則 9.61 s——只登記未修（`1536ff17`）。
- boot-ring deadlock（DEFECT-INVENTORY A-1）——兩個修法都未驗證，不要寫 fixed。
