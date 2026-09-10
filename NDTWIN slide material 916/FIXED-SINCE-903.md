# 903 → 909：修掉了什麼（Found, then fixed — delta）

**auditor 起草 2026-09-08 18:xx；Adam 定稿。** 這是 909 那一頁「Found, then fixed」的**資料正本**；
圖 `figures/fixed-since-903/fig_h1_fixed_since_903`（規格在模板 §C-909-H）只畫代號，數字與證據都在這裡。

[Co-developed with claude code -- Adam]

---

## 0. 口徑（先讀）

- **切點**：903 deck 的 p.8「Found, then fixed」只講了 M-1〜M-5、P-1、鎖端點三部曲（08-30）；
  903 模板全文**沒有一個字**提到 09-02 fix-design campaign、09-02 夜巡（findings #1–#91）、09-04／09-05 夜巡。
  ⇒ 本檔從 **09-02 晚的 fix-design campaign** 起算。🟡 那 20 支若 Adam 09-03 口頭講過，整組 §2.0 劃掉即可。
- **三種狀態，不可混寫**：
  - ✅ **trunk 已併**＝`git merge-base --is-ancestor <tip> trunk` 為真；附「進 trunk 線的 commit＋日期」。
    ⚠️ 09-03 晚起 trunk 的第一親鏈就是 `integrate/2026-09-03-auditor-merge` 那條線，所以有些「進線日期」早於 09-05 的最終合併 `cdc8dad9`。
  - 🔧 **分支上未併**＝tip 不是 trunk 祖先；附分支名＋tip。**一顆都沒推。**
  - 📝 **只登記未修**＝只進了 `doc/KNOWN-ISSUES.md`。
- **證據欄**：`閘門 N/0`＝變異閘 N 個變異 0 存活（沒看過紅不算交付）；`live`＝auditor 或 orchestrator 在 lab 上親自重跑；沒寫就是沒跑。
- 🔴 **trunk 修好 ≠ 使用者拿得到**：本機 tracking ref 顯示 `p4public/main` 停在 09-03 `9e6cc307`、落後 trunk **1689** 顆，
  `origin/main` 停在 08-26 `f5db629b`。**tracking ref 只證明「沒推」，不證明公開狀態**（那要打未認證 HTTPS）。
  ⇒ 上台的判詞是 **FIXED ≠ SHIPPED**：下面每一條對外都是「修在 trunk／分支上，尚未發布」。
- **來源**：`doc/audit/2026-09-03_night-rounds/MERGE-LOG.md`（42 列，trunk 有）、
  `doc/audit/2026-09-03_night-rounds/FINDINGS-COVERAGE.md`（68 條的覆蓋表）、
  `doc/audit/2026-09-02_fix-design-campaign/LEDGER.md`（讀 HEAD 版，工作樹那份有未提交修改）、
  `WAKEUP.md` §2.1–2.9（🔴 **repo 根目錄的未提交檔**——「這是未提交的觀測」）、`git for-each-ref`＋`git log` 09-08 18:0x。

## 1. 數字（拿去做 chip 的）

| 量 | 值 | 怎麼算的 |
|---|---|---|
| 進 trunk 的修法分支（09-03 → 09-05） | **47** | §2.1 30 支＋§2.2 9 支＋§2.3 8 支（含 4 顆 W 系列 commit、2 支閘門儀器）；不含純文件 |
| 09-02 fix-design campaign（🟡 切點前一天） | **20** | §2.0；`git log --merges 06bc60ac..36d832f5` ＝ 20 支（A-2 併兩次算一支）＝ 16 支修法＋4 支儀器／接線測試 |
| trunk 上的純文件登記／手冊修正 commit | **7** | §2.4 |
| 直接落 trunk、不走分支的修法 commit | **5**（＋1 補件） | §2.5；不計入 47（47 的定義是「分支」），圖上不畫磚 |
| 修好但**分支上未併**的分支 | **29**（工單 ≈33 張） | §3；`refs/heads/fix/*` 未併 28 支＋`chore/conventions-0906` |
| 推到公開 ref 的 | **0** | §0 第四點 |
| 只登記未修（KNOWN-ISSUES 新條目） | **8** | §4；trunk 的 `doc/KNOWN-ISSUES.md` 比 09-03 收工（`582241ef`）多出的 `###` 條目＝B-6／B-7／B-8／B-9／B-11／B-12／C-4b／G-12 |

## 2. ✅ trunk 已併

### 2.0 🟡 09-02 fix-design campaign（20 支，全部 09-02 併＝16 支修法＋4 支儀器／接線測試；一句話依各分支的 FIX 文件與 commit message，細節見 LEDGER）

| 代號 | 一句話（缺陷 → 修法） | 進 trunk 線 | 證據 |
|---|---|---|---|
| A-2 | Ryu `get_link()` 無界 ⇒ 拓樸輪詢可永久阻塞而沒人發現 → vendor 一份有界的 `rest_topology`，`stack.sh` 改載自家副本 | `404b11a8` 09-02 | 閘門 9/0（批次）；vendored 檔另 6/0 |
| A-4c | P4 proxy 重啟無條件 `VERIFY_AND_COMMIT` 清空所有表，而 twin 不會說 → 重啟公布 `boot_id`／per-switch `table_generation`（尚無 kernel 讀者） | `0da64329` 09-02 | LEDGER |
| A-4d | install 與 delete 共用同一個 `dst/32` LPM 槽 ⇒ 刪一條就把目的地打成黑洞 → delete 把槽原地還給控制面路由（MODIFY、零空窗） | `8b87a9de` 09-02 | LEDGER 對帳 12:5x |
| A-4f | `del-br` 帶走 bridge 的 sFlow 紀錄、開機不重建 ⇒ 該鏈路遙測永久歸零且與 idle 不可分辨 → 關機存紀錄、開機回放並回讀，`get_graph_data` 加 `telemetry_status` | `36e3d78a` 09-02 | 閘門重跑後過（LEDGER 20:5x「20 支全殺」）；批次那次 rc=2「baseline 紅」是閘門 `BIN` 路徑錯、**根本沒跑過 binary**，33/33 ×3 含 shuffle 證偽 |
| A-7 | 排隊寫入的失敗對所有 API 不可見 → 接上 `droppedAfterStop()` 與 dispatcher 存活，並公布計數的口徑 | `a4a8eb2c` 09-02 | 閘門 8/0 |
| A-9 | 租約到期是「條件」不是「事件」、`isLocked` 從不清 ⇒ 死租約 `unlock()` 仍回 true、遲到的 release 清掉新持有者（polling livelock）→ 到期即結束、`leaseId` 可驗 | `49a3f084` 09-02 | 總閘 23/0 |
| B-2b／B-4 | kernel 自己拼 shell 字串：單引號讓它指控健康元件／模擬案例回 202 但從沒送出 → `utils::execArgv` 免 shell，全站點掃描分類＋守衛 | `4c49b050` 09-02 | Python 守衛紅→綠（auditor 重跑） |
| B-3 | MININET 早退 ⇒ historical logging 回 200「已啟用」卻一列都不寫 → 維持 200 但 `status: not_applicable`＋穩定 `reason` token | `bac267cb` 09-02 | 閘門 10/0 |
| B-x | `get_detected_flow_data` 含已結束的流（churn 下 ~92%，全是 idle）→ 流三態 `active`／`idle`／`ended`，端點預設只回 active | `cc9a9ea4` 09-02 | 閘門 7/0 |
| F-1 | MININET 下 CPU／記憶體／溫度是交換機 IP 的常數函數（四處捏造點）→ 一律改回既有哨兵 `-1`；F-1b 把溫度迴圈的 `ip.front()` 搬到型別過濾之後 | `b259c4d9` 09-02 | 閘門 9/0 |
| F-6 | 讀流表失敗的交換機被整份沖掉（`continue`＝這輪不產生），而四處註解承諾「保留前一份」→ 保留最後一份並標 `stale_since`／`stale_polls`／`last_error` | `fc2cd427` 09-02 | 閘門 7/0 |
| F-8 | 從未有流量的邊 `left_link_bandwidth_bps` **永久**寫死 1 Gbit/s（10 G 核心邊只宣告十分之一的餘裕）→ 改讀模型宣告容量＋新增 `left_link_bandwidth_source` | `dc969792` 09-02 | 閘門 4/0 |
| F-13 | 對不存在的 group／meter 做 modify／delete 回 200，install 打已存在的也回 200（12 格 6 格錯、回應完全相同）→ 先問交換機在不在再宣稱 | `9430bfbe` 09-02 | 閘門 5/0 |
| F-14／F-16／F-4 | host 永遠標不成 down、交換機死了它面向 host 的邊仍 up、死鏈路被 `updateHosts` 憑 IP 復活 → 改從交換機三態 liveness 推導，連兩輪讀不到才標 down 並帶 `down_reason` | `2bda7af1` 09-02 | 閘門 16/0 |
| F-15 | bmv2 gRPC 50051–60 落在本機 ephemeral 範圍內會被搶走，而部分 fabric 起不來仍 exit 0 → 改 30051–60、單一來源 `grpc_ports.py`、起不全即 fatal | `33338e15` 09-02 | LEDGER |
| A-8 | 命令關掉的交換機讓 L2／L3／`check_logs` 三個工具在系統正常時變紅 → 三態：down+OFF 記 `ACCOUNTED-FOR`、讀不到 `TOOL-PRECONDITION-FAILED` exit 3 | `aa44bdf1` 09-02 | 紅→綠（auditor 重跑：22＋113 綠；倒回三工具 rc 1、15 紅 4 錯） |
| B-1（接線測試） | 幽靈規則過濾器的接線沒有守衛（把呼叫註解掉測試照樣綠）→ 剝註解／字面量／`#if 0` 之後再比對 | `e88f1b71` 09-02 | auditor M4（註解掉 `:1975`）⇒ rc 1、16 顆 3 紅 |
| （儀器）G-2 殘餘 | harness 從不比較註冊窗與實跑窗、`port_holder` 無權限時空回傳被讀成「沒有」→ `assert_window_span`＋三態 `LISTENER-OWNER-HIDDEN` | `9f022901` 09-02 | 閘門 12/0；34/34，倒回 `lib.sh` ⇒ 12 紅 |
| （儀器）A-4e | 重構會讓別人的閘門 anchor 失效而 gtest 照樣綠 → `check_gate_anchors.py` 檢查器＋全 campaign 分支的漂移矩陣 | `99e9abd9` 09-02 | auditor 重跑檢查器：base 6/6 ok；真碰撞 1（bx 讓 topk `MISSING:3`） |
| （儀器） | 參考閘門把「沒量到的變異」記成通過（六種假綠）→ 一律計為存活者，加 summary 行與 0/1/2 exit | `aba03849` 09-02 | 閘門 5/0、5/0、6/0（rate_denominator／topk／log_suffix） |

### 2.1 09-03（30 支修法＋2 支純文件；MERGE-LOG 列 1–32）

| 代號 | 一句話（缺陷 → 修法） | 進 trunk 線 | 證據 |
|---|---|---|---|
| #58（REPORT-PICK 的 A-8） | 同一拓樸檔 8 次啟動產生 4 種路由表（BFS 平手由 gRPC 到達順序決定）→ 拓樸的純函數（`hashlib`） | `76d299d3` 09-03 | 閘門 5/0（auditor 重跑） |
| P4 priority | P4 上 `priority` 被靜默丟棄 → 501 取代假成功 | `323668ad` 09-03 | 閘門 7/0（auditor 重跑） |
| L-9 | `make_topology.py --stdout` 的報告污染 JSON → 報告走 stderr | `002e226c` 09-03 | 閘門 3/0 |
| G-7 | `ndtwin-lab` 寫死一個人的絕對路徑、換機器整個 fabric 起不來 → `/etc/ndtwin-lab.conf`＋`config` 子命令 | `2152d368` 09-03 | 59 checks＋閘門 14/0 |
| G-9 | lab 工具自己呼叫四次 `pkill -f`（會殺操作者的 shell）→ 具名 pid 清理；cleanup 失敗會 rc 1 | `5e5989c7` 09-03 | 閘門 6+4/0；併後重跑 29/29 |
| G-6 | `ndt apps sim` 印「started」而 app 已死 → 5 秒內判定、rc 1／2、`ORPHAN` 顯示 | `c42cc07d` 09-03 | 閘門 5/0 |
| #50（形狀） | `2>/dev/null <` 重導向順序（G-6 帶回的形狀）→ 修＋閘門 M2b 專守 | `49b91654` 09-03 | 26 checks、17/0 |
| #22／#23／#24／#41 | `ndt clean` 看不到會擋住下次啟動的 port（`:3005x`／`:6653`／`:6633`／`:9000`／UDP `:6343`）→ 逐 port 指名持有者 | `fbb83b03` 09-03 | 閘門 9/0（auditor 三次） |
| A-14 | `ndt` 兩個 `sudo -n` 不在手冊教的 sudoers 規則裡 ⇒ 守衛永不觸發 → sudo 表面列明 | `b5fe780f` 09-03 | 33 checks、14/0 |
| （行為） | `ndt up` 預設平面改 OVS（Adam 裁） | `50e8b78e` 09-03 | 23 checks、8/0 |
| B-5／#5 | kernel 每次正常關機都 abort（`stop()` 少 join 一條 thread）→ 補 join | `0e11c229` 09-03 | SIGINT 7/7 exit 0，raw 進 repo |
| #32／#45 | 根因：啟動競態讓 bmv2 liveness 路徑從不執行（`refreshDataPlaneKind` 早 1 ms 且只算一次；出貨檔 0/44）→ 載入搬進 `start()` 同步、判定不 latch | `0b34af5f` 09-03 | gtest（fixture 紅已解） |
| #10（#18 只修了高估那半） | 每條流的速率沒有分母（誤差＝迴圈週期，+4.4%～+24.9%）→ 除以量到的間隔 | `b76a2493` 09-03 | 閘門 5/0 |
| #53（遙測健康） | sFlow socket 丟 72.5% 時每個端點照回 success → 回應帶 `status: severe_loss`＋`loss_fraction`＋`offered_in_window`；`GET /ndt/get_sflow_stats` | `ea139d1c` 09-03 | 閘門（合併時解 2 檔） |
| #63（＋#69／#70 文字半） | logger CLI `--logfile` 接路徑 | `89857244` 09-03 | 閘門 9/0＋3 widening 0 誤捕（合併樹重跑） |
| #64／#65（輪次） | 端點回 500 的錯誤 body 被餵進 `updateLinks` → 分類 `reported_failure`／`wrong_shape`；`get_graph_data` 多 `topology_round` | `d00fa57c` 09-03 | 閘門 6/0（作者、共用工作樹的手連 binary）；🟠 乾淨樹只重跑了 19/19 套件，**auditor 沒重跑這支閘門** |
| #59（載入） | 拓樸檔壞 IP 在執行緒裡 throw ⇒ abort 且 port 已開；檔案不見照樣空圖開機 → 綁 port 前失敗、拒絕啟動；`--hosts 300` rc 1 | `70c324e1` 09-03 | 與 #32 同一排序問題的兩半 |
| #4／A-12 | `ovs4` 拓樸完全沒有配置 sFlow ⇒ 分身流量結構性為零 → 十座 bridge 配 sFlow | `5e355dda` 09-03 | 閘門 24/0；**live** 0→10 列、`avg_link_usage` 0→0.504 |
| #71 | 規則 journal 有寫沒接 → 接線 | `486d89fb` 09-03 | 閘門 14/0（auditor 重跑） |
| #17 | chaos harness 讀未註冊路由 ⇒ 每輪指控「path map 被清空」→ 拒絕 | `65d4a32f` 09-03 | 閘門 11/0 |
| #73／#74 | drift 與 shell-site 兩份盤點跟不上合併（trunk 上 1＋2 FAIL）→ 修 | `431d98a5` 09-03 | 紅親眼看、綠重跑 |
| #47 | 子行程繼承 listening socket（kernel 死了 port 還被 app 佔著）→ `SOCK_CLOEXEC`／`FD_CLOEXEC`／`close_range` | `08267dcb` 09-03 | 940/940、閘門 12/0 |
| #42／G-10 | `testbed_topo.py` 128 對 ping 全丟而 banner 印三個 OK → 橫幅只從 ping summary 推導、失敗 exit 1 | `014903fb` 09-03 | 45/45、閘門 25/0 |
| #6／#48／G-11 | `ndt apps stop` 只殺 bash wrapper（viz 的 JVM 活了 1h54m 三通道全說沒在跑）→ setsid 群組、三管道驗證、`apps orphans` rc 2 | `31b9ea8a` 09-03 | 71/0、閘門 13/0（**沒在真 app 上跑過**） |
| #78 | anchor 檢查器對根目錄檔給錯答案 → `is_repo_path` | `1ec39977` 09-03 | 閘門 13/0；紅 9 FAIL＋3 ERROR 親眼看 |
| #46／#36／#35 | 30 s 拓樸輪詢把命令關機的交換機寫回 up（9 次中 2 次，3.08 s 後復活）；電源 API 兩方向 `!isUp` 早退 → `adminPoweredOff` 旗標、`updateSwitches` 不抬 `isUp` | `34e2109d` 09-03 | 閘門 10/0＋3 widening、gtest 951/951；**live** 兩臂各 9 次：拒絕復活 6/9（t_off+2.56–2.60 s）、開機 API 真開 gRPC port 18/18，🔴 但 `is_up` 前後對照 0/9→0/9 **零鑑別力**（寫回 up 的是 liveness 快取，→ #80） |
| #69／#70 | 兩個 parser 靜默忽略未知旗標 → 對兩張表的聯集拒絕 | `ec0a0445` 09-03 | 閘門（首輪抓到自己兩個錯，已記） |
| #77 | `ndt up ovs` 跑的是 NTG 那份 `testbed_topo.py` 不是 repo 的 → 從 `KERNEL_DIR` 導出 | `06bc713d` 09-03 | 紅臂親眼看、丟棄式樹重跑 |
| #75 | INV-01 的 power-on latency 檢查修好了但 runner 沒接 → 接上；沒有該做事的 power-on 就 `NOT-MEASURED` | `078b2736` 09-03 | 閘門＋測試 |
| #8 | `ndt status --check` 在健康 `ovs4` 上假紅（比到 P4 的 `host_count_override`）→ `ndt up` 寫 `up.target` 基準、逐欄比對、新增 `dataplane` 欄 | `48c929fc` 09-03 | 61/0、閘門 12/0 |
| （純文件） | KNOWN-ISSUES 批次登記 | `9b85ee11` 09-03 | — |
| #52 文件半 | 流可見性的界線單位是 **pps 不是 bit/s**（~89／~22／~5／~3 pps 四個轉折）寫進 API 文件／KNOWN-ISSUES／runbook | `582241ef` 09-03 | 30 格逐格對 raw |

### 2.2 09-04（9 支；MERGE-LOG 列 33–42）

| 代號 | 一句話（缺陷 → 修法） | 進 trunk 線 | 證據 |
|---|---|---|---|
| #3／#21／#49／#83 碼半（A-11） | 失敗的 `ndt up ovs4` 不回滾、`up_p4` 在 orphan 上建 fabric 且錯誤偽裝成 P4 問題 → preflight 只對 `foreign` port 拒絕＋`rollback_up` 由新到舊收回 | `257e4eb0` 09-04 | 89 檢查套件＋閘門 |
| #61／#62 | 拓樸檔 edge 指到不存在節點／interface 超界被靜默收下 → 第一個 `add_vertex` 之前整檔驗證、綁 socket 前拒絕 | `e9d8a486` 09-04 | 14 gtest＋閘門 |
| #38 | 連線被拒（6–9 ms）被印成「30 秒逾時」→ 讀 curl exit code、時間改成量到的 | `27d48eda` 09-04 | 5 gtest＋閘門 |
| #82 | OVS `powerOff` 的 `!isUp` 早退 → 問 `ovs-vsctl br-exists` 三值判定（不在／在／問不到） | `3d2b38fe` 09-04 | 測試＋閘門 |
| #27／#76 | 關機 worker 只在輪與輪之間看 `m_running`（SIGINT 2.4–6.4 s；印完 Exiting 又寫真交換機 10.7 s）→ `StopSignal`＋`execCommandCancellable` | `ac703196`（本體 `63792cc9`）09-04 | 紅測試先行；閘門 8/0＋補件 |
| **Q12**＋#33／#34／#80／#81 | `is_up` 一欄兩義（命令 vs 觀測）→ `admin_state`＋`reachable`，`is_up` 留作棄用別名；**breaking**：`get_switches_power_state` body 形狀；API 文件 `2cd796ff` | `95a9f743` 09-04 06:51（integrate 線；trunk 最終合併 `cdc8dad9` 09-05 15:27） | 閘門 18/0＋3 widening；合併樹 `95a9f743` gtest／ctest 1022/1022。⚠️ `cdc8dad9` 併出來的那棵樹**沒有人重跑過 ctest**（09-05 那次 1069/1069 是併**之前**在 `0903b202` 上量的；缺口由 09-05 17:5x W2／W3 併後的 1083/1083 補上） |
| #1／A-10 | `delete_group_entry` 在 OVS 上無聲 no-op、id 永久洩漏（根因：delete 帶 buckets 被 OVS 拒、Ryu 不回 error）→ 只有交換機確認才宣稱 deleted | `d599c476` 09-04 | 閘門 5/0＋4 widening 0 went red（09-05 併前六項檢查重跑） |
| #85 | 一台沒有位址的 switch 讓 status worker SIGSEGV（可達性查證後降為潛伏）→ 守衛 | `93edd0fd`／`8103457b` 09-04 | death test：MININET 半 M1 抓到（exit 139 具名紅）；🔴 **TESTBED 半 M2 存活**，補件的第二支死測試只做過 `-fsyntax-only`、**沒看過紅**（合併樹的 M2 判決沒落檔） |
| #2／C-4 | B-1 的幽靈規則過濾器沒蓋 OVS 寫入路徑（0.257 s 就回快取列、真列 13.4 s 才到）→ 只有裁決性的南向成功才確認條目 | `c2b55184` 09-04 | 紅測試先行；7 commits |

### 2.3 09-05（8 項：4 顆 W 系列 commit 經 `cdc8dad9`、2 支修法、2 支閘門儀器）

| 代號 | 一句話（缺陷 → 修法） | 進 trunk 線 | 證據 |
|---|---|---|---|
| W7 | te app launcher 缺 stdin ⇒ `EOFError` → 修 | `9de04f53` → `cdc8dad9` 09-05 | 閘門 9/0；**live** 25 s 內 log +53 行、`EOFError` 0 |
| W6／OV-2／OV-3（B-7／B-8） | 未知 IP 回 500、未知 dpid 回 200 與零 → 404＋`unknown_dpids` | `f8dbad66` → `cdc8dad9` 09-05 | **live** 404／對照 200；文件 `f0687b34` |
| W1／#87 | `install_group_entry` 對保留 id 回 200「installed」而 `groupdesc` 沒有 → 502 `absent` | `f2126cc5` → `cdc8dad9` 09-05 | **live** 三通道同答案 |
| W5／OV-1 | 模型檔整檔重排（841 行 diff）→ 2 行；⚠️ `--check` 仍 rc 1 ⇒ 開 W10（分支） | `0903b202` → `cdc8dad9` 09-05 | **live** 3998→2 行 |
| #89／W3 | 拓樸輸入驗證另外三扇門（空 ip 的 switch、`bridge_name` 缺席、`port_id` 越界）→ 在任何 vertex 進圖前拒絕 | `336d831e` 09-05 | 閘門 16/0；ctest 1083＝1069＋9＋5；**live R0b** e 由靜默收下變拒絕 |
| #88／W2 | 未守衛的 `ip.front()` 站點 → 守衛 | `cff98191` 09-05 | 閘門 7/0＋asan 10/10 |
| （儀器） | gate-anchor 檢查器修正＋L1 接線 | `11fd457e` 09-05 | anchor 57→65/72 |
| （儀器） | 最後一格 anchor（redirection）66/68 → 68/68 | `68c1dde4` 09-05 | anchor 68/68 |

（W4／#54「succeeded 不是規則數」**只交選項、沒動碼**——不算修，留在 §3 W11。）

### 2.5 直接落在 trunk 線、不走分支的修法 commit（5 顆＋1 顆補件；**不計入 §1 的 47**，圖上不畫磚）

| 代號 | 一句話（缺陷 → 修法） | commit | 證據 |
|---|---|---|---|
| G-3 | chaos `_c07` 的控制組零鑑別力（三條路由 404＋「rows==0 就算重現」），一條已發表的宣稱建立在它上面 → 給控制組鑑別力並撤回該宣稱 | `1411f163` 09-03 | `test_chaos_c07_control.py`＋`mutate_chaos_c07_control.sh` |
| L-1 | `run_layers.sh` 不管哪座 fabric 起著都用 4 主機模型（在 128 主機 fabric 上製造 `BROKEN`）→ 從跑著的 fabric 導出拓樸模型 | `09e72e7b` 09-03 | `mutate_run_layers_topology_from_fabric.sh` |
| L-5 | dispatch drift 掃描不認得 `utils::pathIs(...)` 註冊形式 ⇒ 兩條路由被讀成「已刪除」→ 教會它 | `70665602` 09-03 | `mutate_l3_dispatch_drift.sh` |
| L-10 | `00_preflight.sh` 自己失敗：`NDT_OWNER` 沒設就回 FOREIGN、`:8000` 持有者取錯 fd → 修 | `c916bd4c` 09-03 | `mutate_preflight_instrument_self_failures.sh` |
| G-5 | E 輪的還原檢查只斷言 JSON 裡存在 `"op":"truncate"`（任何取樣率都成立）→ 對編譯產物斷言、換 binary 前先 teardown | `e72ebdfa` 09-03 | `mutate_e_restore_asserts_compiled_artifact.sh` |
| （#22/#23/#24 補件） | ports agent 沒進 commit 的 `stack.sh` 那半：從 `ports.sh` 讀 port 表 | `5c64d432` 09-03 | MERGE-LOG「漏網之魚」 |

### 2.4 trunk 上的純文件（7 顆）

| commit | 內容 |
|---|---|
| `4088b237` 09-04 | API 文件三處補丁（N22 Q2、N22 Q4、T-2） |
| `deaf0502` 09-05 | 登 B-6（宣告的 link failure 被 30 s 輪詢撤銷）＋鎖是 advisory／ttl 邊界 |
| `f0687b34` 09-05 | B-7／B-8 的 W6 前後答案 |
| `2285c63c` 09-05 | 登 B-9（OVS power cycle 靜默重映射 ofport、底下 32 台主機永久斷而四種儀器全綠） |
| `1536ff17` 09-06 | 手冊九處與實作對不上（R6 找到）全修；登 C-4b（delete 後仍回報已刪規則 9.61 s）＋G-12 |
| `1a284f75` 09-07 | 登 B-11／B-12（無位址 host／未知 `brand_name` 被靜默收下） |
| `9483b160` 09-03 | run-06 三次 orchestrator 側中斷的紀錄 |

## 3. 🔧 修好但分支上未併（29 支＝未併的 `fix/*` 28 支＋`chore/conventions-0906`；09-06 → 09-08；一顆都沒推）

| 鏈／輪 | 分支 | tip | 修了什麼 | 證據 |
|---|---|---|---|---|
| 下半場 09-06 | `fix/w8-declared-link-failure-sticky` | `017c060f` | B-6：宣告的 link failure 贏過拓樸輪詢＋`inject_link_failure/recovery` 端點 | 閘門 8/0；ctest 1115；**live lw8 6/6**（90 s／9 樣本全 declared；trunk 對照 30 s 內復活） |
| 下半場 | `fix/w3-door3b-host-empty-ip` | `72ffd4dd` | B-11：`"ip": []` 的 host 被收下 → 拒絕（碼裡叫 door 3d） | 閘門 20/0；**live lw3 6/6 拒** |
| 下半場 | `fix/w15-unknown-brand-rejected` | `8b3ebe49` | B-12：未知 `brand_name` 靜默映射成 hardware → 拒絕；拿掉 `ALLOW_MIXED_DATAPLANE` 那句建議 | 閘門 24/0；**live lw3** |
| 下半場 | `fix/w10-nickname-overlay` | `52224425` | B-10：暱稱寫進 `setting/` 以外的 overlay、模型檔 kernel 只讀不寫；live 抓到 overlay 寫在 `build/` 底下（閘門 0 存活沒看見）再修 | 閘門 16/0；**live lw10 6/6 → lw10b 9/9** |
| 下半場 | `fix/w14-index-zero-guards` | `e62c8d6f` | #88 漏掉的七處 `ip[0]`（五處 HOST 級產線走得到） | 閘門 16/0；death test；ctest 1103 |
| 下半場 | `fix/w11-dispatch-status-accepted-counters` | `8c8a0fe4` | #54／A-7b：`succeeded` 改名＋「交換機收下」第二組計數＋per-request id | 閘門 16/0；**live lw11 8/8、P4 2/2** |
| 下半場 | `fix/ndt-honesty-0906` | `55a0bbe7` | W12 `ndt status` down 之後那句散文、W13 `ndt up` 自己寫 claim note、log 5 代、`ndt check` 看宣告並印 gap | 閘門 23＋7/0；anchor 75/75 |
| 下半場 | `fix/w16-apps-stop-lists-rules` | `19a05ddb` | G-12：`apps stop`／`orphans` 列出 app 留下的規則與鎖（不自動刪） | 閘門 13/0；**live lw16** |
| 下半場 | `chore/conventions-0906` | `fd7541ae` | 慣例三項＋cmake | — |
| round 2 09-07 | `fix/chaos-blackhole-attach-under-shaper` | `262e3ccd` | W8-8：chaos harness 的 netem 掛在 shaper 底下不是上面 | 閘門 8/0 |
| round 2 | `fix/contract-per-node-identity` | `8b85366e` | W3b-3：契約測試 per-node 身分（＋E-21 §7-2 env var 改名） | 閘門 9/0、164 OK |
| round 2 | `fix/intent-task-outcomes-per-test-tmpdir` | `c3d99d00` | `ctest -j2` 競態：每個 temp-dir fixture 自己的路徑 | 常數放回去 796／803 紅；三連 1084/1084 |
| round 2 | `fix/w15b-switch-kind-exemption` | `4bc93d00` | W15-2 豁免＋單一 brand 清單 | 閘門 27/0、28/0；**live lw17c** |
| round 2 | `fix/w18-eighth-index-zero` | `67204ecc` | #88 的第 24 處 `ip[0]`（舊文件寫 16／23 都低估） | death test 紅；閘門 9/0 |
| round 2 | `fix/w17-capacity-current-plane` | `fc140660` | 容量端點說明哪些數字是量的；登 C-6（bmv2 那把靜默的鍵）（＋E-14/15/16 文件） | 閘門 12/0；ctest 1106 |
| round 3 09-08 | `fix/ndt-round2-0907` | `3d1cddad` | W16-1/2/3＋I-3＋D-2＋E-9／E-11／E-10（`ndt` 誠實度系列） | 閘門 117/0、26/0；**live lw16r OVS 8/9＋F 5/5、lw16s P4 7/7** |
| round 3 | `fix/ndt-3-51-helper-apps-window` | `f8e9789d` | 3-51：helper 起的 sim 在主 checkout 算 2 個 orphan 的口徑與訊息 | 閘門 109/0、27/0；**live lw351b 8/8** |
| round 3 | `fix/w8b-withdrawal-needs-observed-failure` | `8a3f71d1` | W8b：撤回宣告要對得上一次觀測到的斷、dpid 0 → 400、Ryu 重啟不清宣告（＋E-22） | 閘門 18/0；**live lw8b2 8 PASS、lw8b3 10/10** |
| round 3 | `fix/e20-startup-sweep-all-interfaces` | `fa52d177` | E-20：啟動殘留掃描讀整個 fabric、說出每筆是誰的 | 閘門 25/0；**live lwe2021 6/7** |
| round 3 | `fix/e21-link-endpoints-in-contract` | `c5aeed56` | E-21：link 端點進契約（`declaration_retained` 上 wire） | 15/0；**live** 17 link 格 PASS |
| round 3 | `fix/bug17-mixed-dataplane-refused` | `c4d81eeb` | BUG-17：混平面拓樸被收下 → 拒絕；E-26 零交換機也拒；登 C-5 | 閘門 31/0＋8 widening；**live lw17b／lw17e 離線** |
| round 3 | `fix/e23-e25-exempt-switch-on-wire` | `6b3deae5` | E-23／25：豁免機在 wire 上說出來（`power_path=none`）；登 G-16 | 閘門 16/0；**live lwe2325 5/5**（⚠️ 豁免機 power off 仍回 Success，§7-7 待裁） |
| round 3 | `fix/e4-chaos-needs-opt-in-all-actions` | `cc725d04` | E-4：chaos 兩個會留狀態的控制改成 opt-in | 五閘門 0 存活 |
| round 3 | `fix/e17-test-tmpdir-carries-pid` | `942a9eb5` | E-17：temp 路徑帶 pid＋L1 跑掃描器 | 11/0；掃描器 220 檔 0 筆（trunk 樹紅 7 筆） |
| round 3 | `fix/g13-p4-rule-install-time` | `29002b82` | G-13：P4 規則安裝時間可查（`rules_timed`／`oldest_rule_installed_at`） | 閘門 26/0；**live lwg13 5/5** |
| round 3 | `fix/e2-kernel-reports-loaded-model` | `8bf26481` | E-2：kernel 回報載入的模型（sha 上 wire） | 閘門 8/0；**live lwe2 6/6** |
| round 3 | `fix/e29-update-hosts-race-evidence` | `16d04882` | E-29：`VertexProperties::ip` 無鎖讀的形狀修正＋TSAN 儀器；🔴 **不可寫成「修了一個 race」**（寫者是探針） | TSAN 4/4 |
| round 3 | `fix/known-issues-refs-by-entry-code` | `20c1636c` | KIREF：閘門在跑時讀 KNOWN-ISSUES、驗每一處引用（用條目代號不用行號） | 9/0；trunk 樹紅 58 |
| round 3 | `fix/docs-e1-e3-findings-coverage` | `5a0f4a00` | E-1／E-3 覆蓋表＋日期口徑（純文件） | 73/73 |

併序與衝突（`WAKEUP.md` §2.9「併序」逐字）：ndt 鏈 W16 → ndt-round2 → 3-51；W8 鏈 W8 → W8b → E-20 → E-21；
W15 鏈 W3-3b → W15 → W15b → BUG17 → E-23/25；E-29 與 W18 改同一行、兩顆都要留。

## 4. 📝 只登記、未修（KNOWN-ISSUES 09-03 之後的新條目）

| 條目 | 登在 | 修法在哪 |
|---|---|---|
| B-6 宣告的 link failure 被 30 s 輪詢撤銷 | `deaf0502` | 🔧 W8 分支 |
| B-7／B-8 未知 IP／dpid 的回應 | `deaf0502`（`f0687b34` 只動 API 文件） | ✅ W6 已在 trunk |
| B-9 OVS power cycle 靜默重映射 ofport | `2285c63c` | ❌ 未修（W9 只開單） |
| B-11／B-12 無位址 host／未知 brand 被收下 | `1a284f75` | 🔧 W3-3b／W15 分支 |
| C-4b delete 後仍回報已刪規則 9.61 s | `1536ff17` | ❌ 未修 |
| G-12 死掉的 app 留下規則與鎖沒人說 | `1536ff17` | 🔧 W16 分支 |
| C-5 混平面、C-6 bmv2 靜默鍵、G-13 P4 規則安裝時間、G-14 helper 起的 app 窗、G-15 載入的模型、G-16 豁免機、A-7b、B-10 | 各分支 | 🔧 條目與修法都在分支上 |

## 5. 上台怎麼講（三句）

1. 「09-03 之後 trunk 多了 47 支修法、分支上還有 29 支修好等併；**沒有一顆推到公開 repo**。」
2. 「絕大多數修法有變異閘門看過紅，例外逐格寫在證據欄（#85 的 TESTBED 半、#64／#65 那支閘門）；標 live 的是在 lab 上親自重跑過的。」
3. 「Q12 的修法已在 trunk（09-05），但外面的使用者還拿不到——那是發布動作，不是修法動作。」
