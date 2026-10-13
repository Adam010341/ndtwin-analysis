# fig_r1_four_rulings —— Adam 09-24 的四條裁決，各做到哪裡

[Co-developed with claude code -- Adam]

> 🔁 **2026-09-27（UTC）起，這一頁在簡報裡改成「裁決 → 依範圍的狀態」表格（judge F-5：狀態色塊違反圖上規則、兩個 done 過度宣稱）。本圖與本檔只留作紀錄，不上 deck。** 表格內容由 figure worker 交給 integrator。

本檔所有日期與時間皆為 **UTC**（run 目錄名的 `…Z`；commit 時間以 `TZ=UTC git log` 換算）。

## 一句話

2026-09-24 Adam 對「P4 程式驅動的 API 形狀」按建議裁了四條（`ANALYSIS.md:401-408`）：①`owner: ndtwin` 時那張表歸 NDTwin；②不要求改 `.p4`，存活偵測走 root 的 veth 心跳；③GUI 讀一次能力旗標、把做不到的操作變灰；④第一刀只做 7 支同形程式、單表 `roles`。到 2026-09-27 16:0xZ 的狀態（依範圍說，不用「done」）：①live 只驗過 PASS 路徑（owned 表 0 條 package entries、proxy 寫進 16/16）；「拒絕 package entries」只有離線測試；後半句「繞路後的表可由宣告推算」未驗。②NDTwin 擁有路由表的 fabric 上 live 驗過偵測＋改路；unbound 只偵測；external 控制面不起心跳。③proxy 的 switch_state 有 capabilities（live）；kernel 與 GUI 未進 trunk。④`ipv4_route` 只有 basic 跑過 live，另 6 支同形只做離線 pre-flight；多表、tunnel、五元組在之後。

## 資料來源

K＝`/home/adam/Desktop/NDTwin-Kernel`；L＝`K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs`；O＝`K/scratch/overnight-2026-09-05/logs/orchestrator-0924`。

| 用途 | 檔（path:line 或 JSON key） | commit／binary |
|---|---|---|
| 四條裁決原文 | `K/doc/audit/2026-09-24_p4-driven-api-shape/ANALYSIS.md:401-408`（§8；裁決時間 2026-09-24 07:3x UTC，`:401`；腳本逐行斷言 403–406 的關鍵字） | 已提交 `46ef4813`（2026-09-24 07:30Z）；讀的是 trunk `3d740be0` |
| ①已合併 | `git merge-base --is-ancestor 572d9462 3d740be0` | roles 第一刀合併 `572d9462`（2026-09-24 16:00Z） |
| ①live | `L/2026-09-26T202055Z_07_roles_basic/10_convert_roles.txt`（owned table：16 條拿掉）、`12_preflight_basic_roles.txt`（`PASS owned table has no package entries`）、`21_proxy_roles_lines.txt`（16 of 16 initial routes）；07 log `O/intake-0926/live07/07.log` 末行 `PASS 07_roles_basic` | repo HEAD `b2eeb71d`、kernel `be70b5dd32356847`（同 run `01_binaries.txt`） |
| ②已合併 | `git merge-base --is-ancestor cafd518a 3d740be0` | 心跳段 W 合併 `cafd518a`（2026-09-26 15:24Z） |
| ②live H1–H4 | `O/intake-0926/hbw-live/h14-20260926T152605Z.log` 末行 `PASS 08_heartbeat`；raw `L/2026-09-26T152605Z_08_heartbeat/` | HEAD `cafd518a`（該 run `01_binaries.txt`） |
| ②live H5 | `O/intake-0926/hbw-live/h5b-20260926T172912Z.log` 末行 `PASS 08_heartbeat`、「a heartbeat ran on exactly the 17 expected arm(s)」 | HEAD `3f8c2abf` |
| ②external 未做 | h14 log `:168`「no heartbeat on the external fabric (rc 3), as designed」、`:173`「H4 reroute: reroute.available False, reason external_control_plane」；`git merge-base --is-ancestor feat/external-detect-only-0927 3d740be0` 為否（分支 head `17e40e29`，2026-09-27 16:14Z；原寫的 `ebe17f7c` 是 rulings AEG 的判官輪 commit，在這條分支的歷史裡但不是 tip——2026-09-27 UTC 第二輪更正） | — |
| ③proxy 端 | `L/2026-09-26T202055Z_07_roles_basic/30_switch_state_roles.json` `switches.*.capabilities`；碼 `K/p4_proxy/proxy_agent/main.py:1151`（`capabilities_for`）、`:1205`（`capabilities_report`） | run：`b2eeb71d`；碼：`3d740be0` |
| ③kernel 未進 trunk | `git grep '"capabilities"' 3d740be0 -- src include` 無結果；分支 `feat/kernel-capabilities-0927` head `91fa028d`（2026-09-27 15:37Z，「kernel: tests for P4 switch capabilities on get_graph_data」）不在 trunk；`O/intake-0926/RULINGS-0927-night.md:6`（Adam 2026-09-27 ~15:2xZ 裁：當晚做第三刀） | — |
| ③GUI 草稿 | `~/Web-GUI` 本機分支 `draft/p4-capabilities-0924` @ `1abd9dc`（2026-09-24 11:08Z），不在 `origin/main` | — |
| ④離線 6 支 | `O/merged-R-572d9462.offline_5-3.log`：basic_tunnel、ecn、qos、mri、link_monitor、firewall 各 `convert rc=0  preflight PASS (want PASS)`；末行 `OFFLINE-5-3: every exercise as expected` | 在合併樹 `572d9462` 上跑 |
| ④之後才做 | `ANALYSIS.md:406`（load_balance 多表範本、tunnel 主機屬性、ternary＋priority「都之後」）；`K/p4_proxy/proxy_agent/route_binding.py:75` `REASON_NO_FIVE_TUPLE_ROLE` | `3d740be0` |

## 可信度

**OBSERVED（跑過，看 raw）**
- 07 在 09-24（`572d9462`）與 09-26（`b2eeb71d`）兩次 PASS；09-26 那次 convert 拿掉 16 條、pre-flight 兩條 PASS、proxy 寫進 16 of 16 條初始路由。
- 07 編的是 tutorials 原封不動的 `solution/basic.p4`（07 log「compiling …/exercises/basic/solution/basic.p4」）；09-26 的 `30_switch_state_roles.json` `heartbeat.side_effects.forwarded_to_hosts` 為 0。
- 08 H1–H4 PASS（`cafd518a`）；H5 重跑 PASS（`3f8c2abf`）；H4 在 external 控制面記錄 `reroute.reason external_control_plane`；H5 心跳只在預期的 17 臂上跑。
- 09-26 兩個 package 的 4 台交換機都回報 `capabilities`（見 `fig_r4`）。

**READ（讀碼或讀 git，沒執行）**
- 四條裁決原文在 `ANALYSIS.md:401-408`。
- trunk `3d740be0` 的 kernel 原始碼裡沒有 `"capabilities"`；第三刀分支與 external detect-only 分支都不在 trunk。
- `~/Web-GUI` 的草稿分支不在 `origin/main`。

**INFERRED（推論，沒驗）**
- 「external: open」＝Adam 2026-09-27 ~05:2xZ（記憶記的是台北時間 13:2x）裁了 external 也起 detect-only 心跳（只偵測、不改路），但尚未實作進 trunk、尚未 live。**裁決本身我只有轉述**：記憶 `phase5-post-roles-state.md:295`，以及 `K/scratch/overnight-2026-09-05/hunt-0911/fix/RULINGS-AEG-SUMMARY.md:56`「external 目前不啟動心跳……（B 會改這件事）」；沒有 Adam 原話的 raw 檔。
- 「multi-table: later」是依 `ANALYSIS.md:406` 的排序，不是有人排定的日期。

## 圖怎麼讀

四張卡＝四條裁決，由左到右照 `ANALYSIS.md` §8 的順序。卡上只有標題與兩三行關鍵詞；底部的色塊是狀態：綠＝已進 trunk 且有 live 證據；琥珀＝裁決已下、還沒進 trunk；灰＝裁決本身說「之後」。

## 已知但書

- ①的「done」只涵蓋「package 對 owned 表的 entries 在 pre-flight 被拒」與「無 roles 時寫入回 501」。裁決 ①還有後半句「繞路後的表必須能從宣告推算出來」，這張圖沒有單獨驗它。
- ②的「owned tables: done」包含 unbound fabric 的**只偵測**（08 H3：偵測到、`reroute false`、reason `unbound`）；琥珀的「external」指的是 external 控制面（p4runtime、flowcache）根本不起心跳。
- ②的 H5 第一次跑（`L/2026-09-26T153259Z_08_heartbeat`）是 FAIL：sampler 沒產生 `50_samples.tsv`，屬儀器錯；修好後在 `172912Z` 重跑才 PASS。兩次都要講。
- ③的狀態會變：第三刀 2026-09-27 ~15:2xZ 才開工。**更正（09-28）**：腳本的斷言釘在 trunk `3d740be0`，所以第三刀併入後重生**不會**失敗——這張存檔圖描述的是 `3d740be0` 的狀態。第三刀 kernel 側已在 09-28 03:41Z 併入（`85bec430`），GUI 側仍在 `~/Web-GUI` 的本機草稿分支；deck 的 R1 是表格頁，③那一列已照這個改。
- ④的「ipv4_route: done」只有 basic 跑過 live；其餘 6 支同形只做了離線 convert＋pre-flight，**沒有上 fabric**。
- 07、08 的 raw 與 log 在 trunk 都是未提交的觀測（`runs/`、`scratch/` 不進版控）；已鏡射到本機 `audit-raw` 分支 `36f8dd8d`，我逐檔比過 blob 相同（2026-09-27 17:2xZ integrator 再比：`36f8dd8d` 是 audit-raw `797c34ab` 的祖先，引用的 run 目錄在 `797c34ab` 逐檔 blob 與工作樹相同；`797c34ab` 依 coordinator 已公開在兩個 P4 repo）。`RULINGS-0927-night.md` 還沒進 audit-raw。
- 🔴 **兩次 07 都跑在 dirty checkout 上**：`ndt status` 的 code 行（各 run 的 `00_status_before.txt:7`）是 `572d9462  +61 file(s) with uncommitted changes`（09-24）與 `b2eeb71d  +92 file(s) with uncommitted changes`（09-26），其中點名兩個可能改變行為的：`p4_proxy/mininet/host_count_override`（值 4）與 `tools/remote-lab/dorm_lab/`。sha 只說 HEAD，不代表 run 的整棵樹；本頁用到的六個 proxy／工具原始檔另有 sha256（`01_binaries.txt`）。
- 產生器斷言的紅燈檢查：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/roles-flowapi-redcheck.py`，紀錄 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/roles-flowapi-redcheck-20260927T1704Z.log`（12 個變異全因指名的原因中止、2 個對照通過；第一版在 `…/roles-flowapi-redcheck.first-20260927T1606Z.log`）。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/roles"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_roles_figs.py
```

（一支腳本產 `fig_r1`～`fig_r4` 四張。）

最後產出：2026-09-27T17:05Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_roles_figs.py` sha256 `280b76fbbdf34135…`（產圖之後腳本沒再改過）。
