# `fig_d1_flow_api_matrix` —— 執行期改規則：各資料面做得到什麼

[Co-developed with claude code -- Adam]

（本檔所有時間為 UTC；run 目錄名的 `…Z` 就是 UTC。）

## 判官修正（2026-09-27 UTC；F-4，coordinator 裁）

- 兩列新證據（09-26 外來 P4＋roles／沒 roles）排在最上面；OVS（09-03）與 NDTwin 自己的 P4（08-24）兩列是 **09-16 之前的背景**，
  移進一個灰底、標「BEFORE 09-16 · BACKGROUND」的帶子裡，格子改灰、列名下方標日期。916 deck 第 32–33 頁已講過 OVS 的 flow 端點。
- 🔴 dirty checkout：09-26 那次 07 是 `b2eeb71d +92 file(s) with uncommitted changes`（`00_status_before.txt` 的 code 行）；
  08 H3 那次是 `cafd518a +85 file(s)`（其中 2 個可能影響行為：`p4_proxy/mininet/host_count_override`、`tools/remote-lab/dorm_lab/`，`…/hbw-live/h14-20260926T152605Z.log:14-17`）。
- **第二輪（2026-09-27 UTC，coordinator 第 12、16 項）**：灰底帶只蓋左表 RAN IT 的格子；那兩列的 READ THE CODE 格讀的是**今天的碼**（trunk `3d740be0`），不是背景，所以移出帶子、恢復一般底色，右表標題標「trunk 3d740be0」。
  08-24 那列的 checkout 狀態：raw 只記了 commit——`five_tuple_live.txt:2`「commit: e89fd4b」，由 `five_tuple_live.sh:43` 的 `git rev-parse --short HEAD` 寫入——**沒有記錄工作樹乾不乾淨**，所以 +N 不詳（不是 0）。09-03 那列同樣只記公開快照 `9e6cc30`，kernel binary sha 沒記。

## 一句話

左表「RAN IT」只放 live raw 看得到的：OVS 三個動作都跑過（經 kernel API）；NDTwin 自己的 P4 裝與刪跑過，但**只經 proxy**；
外來 P4 宣告了 `roles.ipv4_route` 時，kernel API 的裝與刪都跑過；外來 P4 沒宣告 roles 時，kernel API 的寫入被拒（501）。
沒有 live raw 的格子一律「not run」，不宣稱。右表「READ THE CODE」是讀碼得到的比對與動作範圍，不是跑出來的。

## 資料來源

K＝`/home/adam/Desktop/NDTwin-Kernel`；R07＝`K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/2026-09-26T202055Z_07_roles_basic`；R08＝`…/live-p1/runs/2026-09-26T152605Z_08_heartbeat`。

### RAN IT（OBSERVED，腳本逐檔斷言）

| 列 | 格 | raw | 那次 run 用的碼 | 日期 |
|---|---|---|---|---|
| OVS | install／modify／delete，經 kernel `/ndt/install_flow_entry`、`/ndt/modify_flow_entry`、`/ndt/delete_flow_entry` | `K/doc/audit/2026-09-02_manual-usertest/run-06-opus/logs/d9-d11-flow-mutation.log:5-16`（D9：`200` `"status":"queued"`，讀回 `priority=99,ip,nw_dst=10.99.99.99 actions=output:1`，規則數 130→131）、`:18-22`（D11：`actions=output:2`）、`:24-29`（D10：`gone from switch`，回到 130） | 公開快照 `9e6cc30`（`…/run-06-opus/STATE-AT-HARVEST.txt:22`）；kernel binary sha **沒有記錄** | 09-03（**09-16 之前，當背景**；該 log 在 trunk 已提交，`f6158e8a`） |
| NDTwin 自己的 P4 | install／delete，**直接打 proxy** `/stats/flowentry/add`、`/delete`（`five_tuple_live.sh:34`、`:127`、`:181`） | `K/doc/audit/2026-08-24_five-tuple-live/five_tuple_live.txt:19-25`（五元組規則 `prio=101 match={nw_dst 10.0.0.2, nw_proto 6, tp_dst 5001} -> OUTPUT:2`）、`:46-52`（刪除後回到 4 條） | commit `e89fd4b`（同檔 `:2`）；**checkout 乾淨與否沒有記錄**（腳本 `:43` 只寫 HEAD），+N 不詳 | 08-24（**09-16 之前，當背景**；已提交） |
| 外來 P4 ＋ roles | install／delete，經 kernel batch 端點（`07_roles_basic.sh:755`） | `R07/40_batch_install.{code,json}`：200、`"status":"queued"`、`request_id` 1；`R07/41_dispatch_install.json` `accepted_by_switch 1`；`R07/42_stats_flow_1_after_install.json` 讀回 `nw_dst 10.0.9.9 → OUTPUT:3`；刪除 `R07/43`、`44`（`accepted_by_switch 1`）、`45`（10.0.9.9 不見了） | repo HEAD `b2eeb71d`、kernel `be70b5dd32356847`（`R07/01_binaries.txt`） | 09-26（新） |
| 外來 P4，無 roles | install：kernel 先回 200 `queued`（`R07/74_batch_install_plain.json`），逐筆結果是被拒：`R07/75_dispatch_plain.json` `rejected_by_switch 1`、`R07/76d_dispatch_global.json` `recent_failures[].controller_status 501`、`unsupported_on_p4`、reason `unbound`；直接打 proxy 也是 501（`R07/73_proxy_add.code`、`R08/66_proxy_add.code`） | 同上；R08：HEAD `cafd518a` | 09-26（新） |

### READ THE CODE（READ，trunk `3d740be0`；腳本斷言引用的字串還在）

| 列 | matches | actions | 檔:行 |
|---|---|---|---|
| OVS | OpenFlow match 原樣交給 Ryu | 原樣交給 Ryu | `K/src/ndt_core/routing_management/HttpRoutingStrategyBase.cpp` 的 `/stats/flowentry/add`、`/delete_strict`（`:322` delete_strict、`:344` add） |
| NDTwin 自己的 P4 | 只有目的 IP → `ipv4_lpm`；多於目的 IP → `flow_5tuple`（in_port、src、dst、proto、L4 ports） | 只讀 `OUTPUT`；其他 action 靜默忽略、沒有 OUTPUT 就失敗 | `K/p4_proxy/proxy_agent/topology_manager.py:196-212`（`FIVE_TUPLE_FIELD_MAP`）、`:1004-1012` |
| 外來 P4 ＋ roles | 只有目的 IP（第一刀只能綁目的路由）；五元組寫入回 501 `no_five_tuple_role` | 宣告的那個 action（例：`MyIngress.ipv4_forward(dstAddr, port)`） | `K/p4_proxy/proxy_agent/route_binding.py:159-161` |
| 外來 P4，無 roles | 只能改走 proxy 的 `/p4/table_entry`：exact、lpm（ternary／range／optional 回 501） | 它 p4info 裡的任一 action；**不記 journal**，proxy 重啟就消失 | `K/p4_proxy/proxy_agent/api_routes.py` `/p4/table_entry`（`@router.post` 在 `:836`，其 docstring 的狀態碼表在其後） |

## 可信度

- 左表每格 OBSERVED（raw 路徑如上）。07／08 的 raw 在 trunk 不進版控，但整個 run 目錄在 audit-raw `797c34ab`（逐檔 blob 與工作樹相同，2026-09-27 17:2xZ 本機比對）；09-03 的 `d9-d11-flow-mutation.log` 與 08-24 的 `five_tuple_live.txt` 本來就在 trunk 版控裡。
- 右表每格 READ（trunk `3d740be0`），沒有執行；四列都讀今天的碼，所以背景帶不蓋右表。
- 🔴 **沒有找到的**：P4 平面上 kernel 單數端點 `/ndt/*_flow_entry` 的 live 呼叫；任何 P4 平面的 modify live 呼叫；`/p4/table_entry` 成功寫入的 live raw（只有工單裡的範例 body，`TICKET-P2-exercise-dataplane.md:55`）。所以那幾格畫「not run」。
- NDTwin 自己的 P4 那一列**繞過了 kernel**（直接打 proxy）；「經 kernel 也一樣」是 INFERRED（同一個 `processFlowBatch` 路徑，`K/src/ndt_core/http/HttpSession.cpp:1946`、`:1961`、`:1976`），圖上用「proxy only」標明。

## 已知但書

- kernel API 永遠先回 `queued`：`"status": "queued"` 的意思是「**已接受、待寫入**」，不是「已寫入」（`K/doc/2026-01-02_ndt_api.md:1754-1758`）；要知道結果只能事後讀回（同檔 `:1924-1928`）。無 roles 那一列就是例子：HTTP 200，實際被拒。見 `fig_d2`。
- OVS 上 `switch_outcome` 永遠是 unknown：OpenFlow 不回應 FLOW_MOD（`R07/41_dispatch_install.json` 的 `why_unknown` 欄引 `doc/KNOWN-ISSUES.md` C-4）；P4 平面 proxy 先寫再回，所以分得出 accepted／rejected。
- external 控制面的 fabric 上，proxy 的 `/stats/flowentry/*` 回 409（`R08/82_flowentry_*.code`）；經 kernel 會怎樣沒有 live raw。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/flow-api"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_flow_api_matrix.py
```

最後產出：2026-09-27T18:54Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_flow_api_matrix.py` sha256 `73283f2b679de4b0…`（產圖之後腳本沒再改過）。
