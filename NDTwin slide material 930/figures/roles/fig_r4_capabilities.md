# fig_r4_capabilities —— 每台交換機在 switch_state 裡報的能力旗標

[Co-developed with claude code -- Adam]

本檔所有日期與時間皆為 **UTC**（run 目錄名的 `…Z`；commit 時間以 `TZ=UTC git log` 換算）。
v1.8（2026-09-29）：圖只畫最後狀態——最新一次 live 07（09-26，心跳在跑）裡兩個 package 各一列；v1.7 的全文（兩天四列、圖上印 sha）逐字在 `README-930.md` §13.7。

## 一句話

proxy 的 `GET /p4/switch_state` 每台交換機都帶一個 `capabilities` 物件（這是裁決 ③「GUI 讀一次能力旗標」的資料源）。同一支 tutorials basic，最新一次 live 07（09-26）裡：宣告 roles 的那包 `ipv4_route` 是 `ndtwin`（NDTwin 能寫路由）、`reroute` 是 `true`；不宣告的那包是 `unbound`、`reroute` `false`——只偵測、不改路。兩包的 `link_discovery` 都是 `heartbeat`，五元組都是 `false`。每一列都是 4 台交換機回報完全相同的值（4 of 4）。

## 資料來源

L＝`/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs`。

| 用途 | 檔（JSON key） | commit／binary |
|---|---|---|
| basic＋roles | `L/2026-09-26T202055Z_07_roles_basic/30_switch_state_roles.json` `switches.{1..4}.capabilities` | repo HEAD `b2eeb71d`（**+92 個檔未提交**，見已知但書）、kernel `be70b5dd32356847`（同 run `01_binaries.txt`） |
| basic 無 roles | 同 run `71_switch_state_plain.json` 同 key | 同上 |
| 「4 of 4」 | 同上兩檔：`switches` 有 4 台、`capabilities` 序列化後只有 1 種值（腳本斷言） | — |
| 同一個判定寫在 run log | `K/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926/live07/07.log:65`（roles，`L6 capabilities: all 4 switches report …`）、`:101`（unbound） | 同上 |
| 「最後狀態」 | L 底下 `*_07_roles_basic` 只有 09-24、09-26 兩個 run，09-26 是最新的（腳本斷言；出現更新的就停） | — |
| 欄位的語意 | `K/p4_proxy/proxy_agent/main.py:1151`（`capabilities_for`）、`:1205`（`capabilities_report`）；規格 `K/doc/audit/2026-09-24_p4-driven-api-shape/TICKET-P4-roles.md` §2.5-2、附錄 A | trunk `3d740be0`（READ；main.py 與 `b2eeb71d` 版 sha256 相同 `54c9bd96c181b0dd`） |

## 可信度

**OBSERVED（跑過，JSON）**
- 兩列的五個欄位值如圖；每列 4 台相同。
- 兩包的頂層 `reroute`：roles 那包 `available: true`、`reason: null`；無 roles 那包 `available: false`、`reason: "unbound"`（`30_…json`、`71_…json` 的 `reroute` key）。腳本斷言它與每台的 `capabilities.reroute` 一致。
- 兩包存檔當下 `links` 8 條（＝`declared_links.directions` 8），每條 `source: heartbeat`、`down: false`（腳本斷言）。
- 這些值同時也是 07 的 L6 判定（見上表 `07.log:65`、`:101`；見 `fig_r3`）。

**READ（讀碼，沒執行）**
- `reroute` 是整個 fabric 的事實、逐台回報；在宣告鏈路的 fabric 上，`reroute` 與 `link_discovery` 每次請求依 watchdog 最後讀到的心跳重算（`main.py:1205-1212` docstring：心跳一停，`reroute` 在一次讀取內變 false）。
- 附錄 A 規定：kernel `get_graph_data` 的節點將來原樣抄這個物件；**沒有 `capabilities` ⇒ 一切視為支援**（OVS、舊 kernel）。

**INFERRED**
- 顏色是依附錄 A 的語意分的：綠＝這台做得到（`ndtwin`、`true`、`heartbeat`）、灰＝做不到（`unbound`、`false`、`declared`）、白＝`binding_source` 只說綁定從哪來，不是能力。

## 圖怎麼讀

左上小標「RAN IT · live 07, 09-26」（日期由腳本從 run 目錄名取）。上列是宣告了 `roles.ipv4_route` 的 basic，下列是同一支程式不宣告 roles。欄位名照 JSON 原樣（等寬字）。兩列只差在 NDTwin 能不能寫那張路由表（`ipv4_route`）以及斷線時能不能改路（`reroute`）；偵測斷線（`link_discovery: heartbeat`）兩列都有。圖上不印 sha：sha 與髒 checkout 在本檔與模板 §2 R4 的講者備註。

## 已知但書

- 🔴 **這一 run 跑在 dirty checkout 上**：`ndt status` 的 code 行（`L/2026-09-26T202055Z_07_roles_basic/00_status_before.txt:7`）是 `b2eeb71d  +92 file(s) with uncommitted changes`，其中點名兩個可能改變行為的：`p4_proxy/mininet/host_count_override`（值 4）與 `tools/remote-lab/dorm_lab/`。sha 只說 HEAD，不代表 run 的整棵樹；本頁用到的六個 proxy／工具原始檔另有 sha256（`01_binaries.txt`）。腳本從 `00_status_before.txt` 讀出並斷言 +92；寫出時一律「`b2eeb71d +92`（dirty）」。
- 🔴 這是 **proxy** 報的。kernel 的 `get_graph_data` 節點也帶這個欄位（第三刀 kernel 側，merge `85bec430`，09-28 03:41Z；PR #14 的 CI 四個 job 全綠、ctest 1385/1385，`K/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926/ci-compare-pr14.txt:1-2`）——**kernel 這一側沒有 live run**；GUI 還沒讀它——「GUI 會變灰」目前只存在於 `~/Web-GUI` 的本機草稿分支（`draft/p4-capabilities-0924`）。
- `five_tuple` 在外來程式上一律 `false`：第一刀沒有五元組的 role，外來交換機上的五元組寫入一律 501（`route_binding.py:75` `REASON_NO_FIVE_TUPLE_ROLE`）。
- `ipv4_route: ndtwin` 只代表「目的 IP 路由表這一張」；不要說成「NDTwin 能操作外來 P4 程式」。
- 圖上的值要心跳在跑才成立。07 在 `ndt up` 後輪詢 switch_state：前兩次（約 4 s）`links` 仍全是 `source: declared`，第 3 次才全是 `heartbeat`（`30_switch_state_roles.json.polls`、`71_switch_state_plain.json.polls`）；圖上的值取自輪詢結束時存下的那一份。輪詢檢查的是 `links`，前兩次的 `capabilities` 長什麼樣沒有存。
- external 控制面的 fabric（p4runtime、flowcache）不在這張圖裡；那裡 `ndt up` 不起心跳（08 H4）。
- 同一支 basic 在 09-24 也跑過一次 07（`L/2026-09-24T160256Z_07_roles_basic`，`572d9462 +61`，心跳之前）；本圖只畫最後狀態，不畫那一次（產生器仍讀它，給 `fig_r3`）。
- raw 在 trunk 未提交（`runs/`），已鏡射到 audit-raw：`36f8dd8d` 是 audit-raw `797c34ab` 的祖先，引用的 run 目錄在 `797c34ab` 逐檔 blob 與工作樹相同（2026-09-27 17:2xZ integrator 比過；`797c34ab` 依 coordinator 已公開在兩個 P4 repo）。
- 紅檢（v1.8 新增與改過的停止條件）：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_roles_figs-redcheck.py` → `make_roles_figs-redcheck-20260929T0810Z.log`：**11 個竄改 11/11 以產生器自己的具名理由停下、2 個對照組通過**（有更新的 07 run、頂層 `reroute` 與每台不一致或缺、鏈路不是全由心跳餵／有一條 down／少一條、`link_discovery` 不是 heartbeat、09-26 的欄位多一個、值無法分類、run 目錄名沒有日期）。
  `evidence()` 的舊停止條件由舊 harness 重跑：`roles-flowapi-redcheck.py` → `roles-flowapi-redcheck-20260929T0812Z.log`（12/12、對照 2/2，與 09-27 的 `…-20260927T1704Z.log` 相同）。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/roles"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_roles_figs.py --only fig_r4_capabilities
```
（不帶 `--only` 會四張都重畫；`evidence()` 不論如何都整份檢查。）

最後產出：2026-09-29T08:12Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_roles_figs.py` sha256 `6d2d97925f1bc566…`（產圖之後腳本沒再改過）；重生紀錄 `K/scratch/overnight-2026-09-05/logs/slides930/regen-v18-roles-20260929T0812Z.log`（只重畫本圖，`fig_r1`–`fig_r3` 沒動）。PNG sha256 300 dpi `7edc2c395034dcdb…`、500 dpi `26345d320b2c9932…`（v1.7 是 `1cc2f62f3e7c6809…`／`edffdb328a290c1c…`）。
