# fig_d2_queued_readback —— 「queued」不等於「已寫入」：要讀回來

[Co-developed with claude code -- Adam]

本檔所有日期與時間皆為 **UTC**（run 目錄名的 `…Z`；commit 時間以 `TZ=UTC git log` 換算）。

## 一句話

同一支 tutorials basic、同一個 kernel batch 寫入（`10.0.9.9 → port 3`，打在 s1），09-26 那次 live 07 做了兩遍：有宣告 `roles.ipv4_route` 的那包，kernel 回 `200 queued`，之後 dispatch 狀態是 `accepted_by_switch 1`，proxy 的 `/stats/flow/1` 讀得回 `10.0.9.9 → OUTPUT:3`；沒宣告 roles 的那包，kernel **一樣**回 `200 queued`，但 dispatch 狀態是 `rejected_by_switch 1`，kernel 的 `recent_failures` 記下 proxy 回的 `501 unsupported_on_p4`、reason `unbound`。兩邊的第一個回應一模一樣，結果相反——所以 `queued` 只代表「收下了」，要知道有沒有寫進去就得事後讀回。

## 資料來源

K＝`/home/adam/Desktop/NDTwin-Kernel`；O＝`K/scratch/overnight-2026-09-05/logs/orchestrator-0924`；R＝`K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/2026-09-26T202055Z_07_roles_basic`（repo HEAD `b2eeb71d`、kernel binary sha256 前 16 碼 `be70b5dd32356847`，見 `R/01_binaries.txt`）。

| 用途 | 檔（path:line 或 JSON key） | commit／binary |
|---|---|---|
| 送出的端點 | `07_roles_basic.sh` 的 `batch()`：`POST /ndt/install_flow_entries_modify_flow_entries_and_delete_flow_entries`（`b2eeb71d:706`＝trunk `3d740be0:755`） | 已提交；run 用的 07 sha256 `7010f3825e06c078`＝`b2eeb71d` 版 |
| 送出的 body | 同檔 `INSTALL=`（`b2eeb71d:824`＝`3d740be0:873`）：dpid 1、priority 10、`ipv4_dst $PROBE_DST`、`OUTPUT port 3`；`PROBE_DST="10.0.9.9"` | 同上 |
| roles：POST 回應 | `R/40_batch_install.code`＝`200`；`R/40_batch_install.json`：`status "queued"`、`accepted 1`、`request_id 1` | run `b2eeb71d` |
| roles：dispatch | `R/41_dispatch_install.json`：`complete true`、`counters.dispatched_ok 1`、`switch_outcome.accepted_by_switch 1`、`rejected_by_switch 0` | 同上 |
| roles：讀回 | `R/42_stats_flow_1_after_install.json` `"1"[]` 中 `match.nw_dst "10.0.9.9"` 的那筆：`actions ["OUTPUT:3"]` | 同上 |
| 無 roles：POST 回應 | `R/74_batch_install_plain.code`＝`200`；`R/74_batch_install_plain.json`：`status "queued"`、`accepted 1`、`request_id 1` | 同上（07 在兩包之間 `ndt down` 再 `ndt up`，kernel 是新的一個，request_id 從 1 起算） |
| 無 roles：dispatch | `R/75_dispatch_plain.json`：`counters.dispatched_ok 0`、`dispatch_failed 1`、`switch_outcome.rejected_by_switch 1` | 同上 |
| 無 roles：原因 | `R/76_dispatch_global.json` `recent_failures[0]`（`match.ipv4_dst "10.0.9.9"`）：`controller_status 501`、`message` 內 `"outcome":"unsupported_on_p4","reason":"unbound"`；稍後那份 `R/76d_dispatch_global.json` 仍有同一筆（`seq 1`） | 同上 |
| 手冊：queued 的意思 | `K/doc/2026-01-02_ndt_api.md:1754-1758`（「A `200` with `"status": "queued"` therefore means *accepted for programming*, not *programmed*」） | 2026-07-28 12:04Z 寫的（`git blame` `08746f4c9`），**09-16 之前，背景** |
| 手冊：只能讀回 | 同檔 `:1920-1928`（刪除沒有「什麼都沒刪」的回應；「The only way to tell is to read the rule back afterwards」在 `:1927-1928`） | 2026-09-05 21:02Z（`1536ff17e`），**09-16 之前，背景** |

## 可信度

**OBSERVED（09-26 live 07，HEAD `b2eeb71d`）**
- 圖上每一個值（`200`、`queued`、`request_id 1`、`ok`、`501`、`accepted_by_switch 1`、`rejected_by_switch 1`、`10.0.9.9 → OUTPUT:3`、`501 unsupported_on_p4`、`reason unbound`）都是腳本從上表的檔讀出並斷言的。
- 09-24 那次（`572d9462`）07 log 的 L2／L5 行是同樣的形狀（`O/live-0925/07_roles_basic.log`：「install: HTTP 200 request_id=1」「dispatched_ok 1」「reads back nw_dst 10.0.9.9 -> OUTPUT:3」；L5「recent_failures says why: … HTTP 501」），圖上只畫 09-26。

**READ（讀碼或讀手冊，沒執行）**
- `queued` 是 kernel 在任何請求到控制器之前就回的（手冊 `:1754-1758`；`K/src/ndt_core/http/HttpSession.cpp:2171` `processFlowBatch`，`:2386` 交給 dispatcher）。
- P4 平面上 proxy 先寫再回，所以 `switch_outcome` 分得出 accepted／rejected；OVS 平面永遠落在 `unknown`（`R/41_dispatch_install.json` 的 `why_unknown` 欄原文，引 `doc/KNOWN-ISSUES.md` C-4）。

**INFERRED**
- 圖中 kernel→proxy 的「dispatch」箭頭與其回覆「ok」「501」：raw 裡沒有這一段的 trace。「ok」取自 `counters.dispatched_ok 1`，「501」取自 `recent_failures[0].controller_status`（kernel 記下的 proxy 回應碼），箭頭本身是依碼畫的。

## 圖怎麼讀

兩個序列圖，左有 roles、右沒有；三條生命線是 07 腳本、kernel、P4 proxy，時間由上往下。實線是請求、虛線是回應。琥珀框圈起來的 `200 queued` 兩邊完全一樣；之後的綠色與紅色是兩邊唯一不同的地方。

## 已知但書

- 🔴 這裡的 `accepted_by_switch` 只有 P4 平面有意義；OVS 上同一欄永遠是 `unknown`，那邊只能讀回規則表。
- 手冊 `:1920-1928` 那段講的是**刪除**（刪了不存在的規則也回 200）；「只能讀回」的結論同樣適用於安裝，但原文的主語是刪除。
- 無 roles 的 501 是 roles 第一刀（`572d9462`，2026-09-24 16:00Z）才有的行為；在那之前同樣的寫入會以字面常數寫進作者的表，同一個 /32 已存在時改走 MODIFY 悄悄覆蓋（`K/doc/audit/2026-09-24_p4-driven-api-shape/TICKET-P4-roles.md` §1，當時標 INFERRED）。
- 範圍只有目的 IP 路由表；**不要說「NDTwin 能操作外來 P4 程式」**。
- raw 在 trunk 未提交（`runs/`），已鏡射到本機 `audit-raw` 分支 `36f8dd8d`，blob 逐檔相同（2026-09-27 17:2xZ integrator 再比：`36f8dd8d` 是 audit-raw `797c34ab` 的祖先，引用的 run 目錄在 `797c34ab` 逐檔 blob 與工作樹相同；`797c34ab` 依 coordinator 已公開在兩個 P4 repo）。
- **與 916 的重疊**：「queued 不等於已寫入、要讀回」這個主題 916 已經講過（第 26 頁：流表比交換機早 13 s 就有那條規則；第 28 頁：dispatch 計數改名；第 32 頁：09-04 量到 `succeeded` 數的是 POST 不是交換機狀態——都是 OVS 平面，我看過 916 deck PDF 這三頁的渲染）。**這一頁的新東西是 P4 平面的證據（09-26 live 07）**：同一個 `200 queued`，switch_outcome 分得出 accepted／rejected，而且無 roles 時的拒絕原因有名字（501 `unsupported_on_p4`、`unbound`）。上台時照這個講法，避免重講 916。
- 🔴 **本頁那次 07（09-26）跑在 dirty checkout 上**：`ndt status` 的 code 行是 `b2eeb71d  +92 file(s) with uncommitted changes`（`R/00_status_before.txt:7`），其中點名兩個可能改變行為的：`p4_proxy/mininet/host_count_override`（值 4）與 `tools/remote-lab/dorm_lab/`。sha 只說 HEAD，不代表 run 的整棵樹；本頁用到的六個 proxy／工具原始檔另有 sha256（`01_binaries.txt`）。
- 產生器斷言的紅燈檢查：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/roles-flowapi-redcheck.py`，紀錄 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/roles-flowapi-redcheck-20260927T1704Z.log`（12 個變異（D1–D4 是本圖的）全因指名的原因中止、2 個對照通過；第一版在 `…/roles-flowapi-redcheck.first-20260927T1606Z.log`）。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/flow-api"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_queued_readback.py
```

最後產出：2026-09-27T17:05Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_queued_readback.py` sha256 `71984358cdf00ebe…`（產圖之後腳本沒再改過）。
