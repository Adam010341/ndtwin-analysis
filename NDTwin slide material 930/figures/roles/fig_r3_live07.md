# fig_r3_live07 —— live 07 跑了兩次：L1–L6 全過，剪線時的掉包只記錄

[Co-developed with claude code -- Adam]

本檔所有日期與時間皆為 **UTC**（run 目錄名的 `…Z`；commit 時間以 `TZ=UTC git log` 換算）。

## 一句話

live 07（tutorials basic＋`roles.ipv4_route`，pod-topo 4 台 bmv2）跑了兩次：09-24（`572d9462`，心跳還沒進來）與 09-26（`b2eeb71d`，心跳在跑）。兩次 L1–L6 每一格都 PASS。右邊三組 pingall：開機 12/12、恢復後 12/12；**剪線期間**的掉包從 8/12 對降到 3/12 對——但這一項 07 **只記錄、不斷言**，L4 也**不斷言改路**。

## 資料來源

K＝`/home/adam/Desktop/NDTwin-Kernel`；L＝`K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs`；O＝`K/scratch/overnight-2026-09-05/logs/orchestrator-0924`。

| 用途 | 檔（path:line 或 JSON key） | commit／binary |
|---|---|---|
| 09-24 的 L 格判定 | `O/live-0925/07_roles_basic.log`（07 的 stdout；以 `   L1`～`   L6` 開頭的行＝`judge` 通過的行；無 `   !! ` 行；末行 `PASS 07_roles_basic`） | run `L/2026-09-24T160256Z_07_roles_basic`：repo HEAD `572d9462`、kernel `be70b5dd32356847`（`01_binaries.txt`） |
| 09-26 的 L 格判定 | `O/intake-0926/live07/07.log`（同上規則）；orchestrator 的摘要 `O/intake-0926/live07/RESULT.md` | run `L/2026-09-26T202055Z_07_roles_basic`：repo HEAD `b2eeb71d`、kernel `be70b5dd32356847`；07 腳本 sha256 `7010f3825e06c078`＝`b2eeb71d` 的已提交版 |
| 開機 pingall | 兩個 run 的 `32_pingall.txt` 末行 `PINGALL_LOSS pairs=12 zero_loss=12 lossy=0` | 同上 |
| 剪線期間 pingall | 09-24 `54_pingall_during_cut.txt`：`zero_loss=4 lossy=8`；09-26：`zero_loss=9 lossy=3`（lossy 的三對是 h1→h3、h1→h4、h2→h3） | 同上 |
| 恢復後 pingall | 兩個 run 的 `61_pingall_after_recovery.txt`：`zero_loss=12 lossy=0` | 同上 |
| 「只記錄不斷言」的出處 | 07 腳本：`note "traffic during the cut (recorded, NOT asserted …)"`（`b2eeb71d:852`＝trunk `3d740be0:901`）；檔頭 L4「REROUTING IS NOT ASSERTED here (08_heartbeat.sh H1 asserts it)」（`07_roles_basic.sh:32-39`）；兩份 log 都有這一行，腳本逐字核對它與 raw 末行相同 | 已提交 |
| ping 次數 | 開機 `ping -c 5`（`b2eeb71d:814`）；剪線中、恢復後 `ping -c 3 -W 2`（`:850`、`:865`；`_common.sh:576`） | 已提交 |

每格「n checks」＝該 log 以 `   L<n>` 開頭的行數：09-24 為 L1 2、L2 3、L3 1、L4 4、L5 6、L6 4；09-26 的 L1 多一行（unbound 那包在 switch_state 上的心跳鏈路檢查，段 W 之後才有）。

## 可信度

**OBSERVED（跑過，raw＋stdout log）**
- 兩次 run 的 L1–L6 全 PASS，stdout 無 fail 行，末行 `PASS 07_roles_basic`。
- 三組 pingall 的數字如上；09-26 剪線期間 lossy 的是 pingall 最先試的三個跨邊主機對，其後五個跨邊對都 0%。
- 剪線期間、pingall 之後抓的 proxy 鏈路表 `56_proxy_links_during_cut.json`：09-24 仍列 8 條（被剪的 s1:3↔s3:1 還在）；09-26 只剩 6 條（被剪那條兩個方向都不見了）。
- 兩次 run 的 L4 判定：`inject_link_failure` 後兩向 `is_up:false`、40 s 後仍 false、恢復後回 true、兩端無 netem。

**READ（讀碼，沒執行）**
- L4 的「down」來自 `/ndt/inject_link_failure` 對 kernel 的宣告（`K/src/ndt_core/http/HttpSession.cpp:1097` `handleInjectLinkFailure`，`:1142`、`:1145` 兩向 `setEdgeDownByDeclaration`，另加兩端 netem；trunk `3d740be0`），不是心跳偵測。所以 L4 PASS 不證明偵測、更不證明改路。

**INFERRED（推論，沒驗）**
- 8→3 的原因：09-26 心跳在剪線後十幾秒內偵測到、proxy 在 NDTwin 擁有的路由表上改了路，所以 pingall 前段三對掉、後段不掉。07 沒有逐對時間戳，這只是**相符**，不是量測；改路本身由 08 H1 斷言（見心跳那頁）。
- 兩次 run 剪線期間 pingall 大約各跑了 42 s／31 s：這是從 `51_inject_failure.code` 與 `54_pingall_during_cut.txt` 的檔案 mtime 相減，不是 raw 內容。

## 圖怎麼讀

左：六列 L1–L6、兩欄兩次 run；綠格＝該格的每一條判定都 OK，格內是判定行數。右：每組兩根柱，09-24 在左、09-26 在右；柱高固定 12（ordered host pairs），綠＝0% 掉包的對數、紅＝有掉包的對數。只有中間那組（剪線期間）有紅，上方標「recorded, not asserted」。

## 已知但書

- 🔴 剪線期間的 8/12 與 3/12 **不是判定**：07 腳本把它寫成 note，不管多少都不會讓 07 FAIL。上台不要說「07 證明了會改路」。改路的斷言在 08 H1，不在 07。
- 🔴 07 的 log 在 09-26 那次仍印「(c) does not hold」——那是第一刀時寫的字句，段 W 之後已過時（心跳在擁有路由表的 fabric 上會改路）；raw 本身沒錯，字句沒跟上。
- 兩次之間 proxy 的 `main.py`、`topology_manager.py` 都改了（sha 不同，見兩個 `01_binaries.txt`；心跳段 W 與其後續），我沒有逐 hunk 分出哪些改動與掉包有關，所以「8→3 是心跳造成的」只算推論。07 腳本剪線那一段（`--- L4 ---` 到恢復後 pingall）與 `_common.sh` 的 `ping_loss`／`pingall_loss` 在 `572d9462` 與 `b2eeb71d` 逐字相同（READ，`git show` 比對），所以量法沒變。
- 兩次 run 各一次，沒有重複；「3」這個數字受剪線與 pingall 起跑的相位影響，下一次可能不同。
- 範圍只有目的 IP 路由表（`roles.ipv4_route`）這一張；不要延伸成「NDTwin 能操作外來 P4 程式」。
- raw 與 log 在 trunk 未提交（`runs/`、`scratch/`），已鏡射到本機 `audit-raw` 分支 `36f8dd8d`，逐檔 blob 相同（2026-09-27 17:2xZ integrator 再比：`36f8dd8d` 是 audit-raw `797c34ab` 的祖先，引用的 run 目錄在 `797c34ab` 逐檔 blob 與工作樹相同；`797c34ab` 依 coordinator 已公開在兩個 P4 repo）。兩次都在 protobuf 5 合併（`5dc7fc9a`，09-27）之前，同一個 kernel binary。
- 🔴 **兩次 07 都跑在 dirty checkout 上**：`ndt status` 的 code 行（各 run 的 `00_status_before.txt:7`）是 `572d9462  +61 file(s) with uncommitted changes`（09-24）與 `b2eeb71d  +92 file(s) with uncommitted changes`（09-26），其中點名兩個可能改變行為的：`p4_proxy/mininet/host_count_override`（值 4）與 `tools/remote-lab/dorm_lab/`。sha 只說 HEAD，不代表 run 的整棵樹；本頁用到的六個 proxy／工具原始檔另有 sha256（`01_binaries.txt`）。
- 產生器斷言的紅燈檢查：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/roles-flowapi-redcheck.py`，紀錄 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/roles-flowapi-redcheck-20260927T1704Z.log`（12 個變異全因指名的原因中止、2 個對照通過；第一版在 `…/roles-flowapi-redcheck.first-20260927T1606Z.log`）。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/roles"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_roles_figs.py
```

最後產出：2026-09-27T17:05Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_roles_figs.py` sha256 `280b76fbbdf34135…`（產圖之後腳本沒再改過）。
