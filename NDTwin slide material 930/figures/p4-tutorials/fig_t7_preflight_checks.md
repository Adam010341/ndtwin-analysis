# fig_t7_preflight_checks —— pre-flight 在 ndt up 之前查什麼，以及它真的擋下的一次

[Co-developed with claude code -- Adam]

## 一句話

`ndt up p4 --app` 之前，pre-flight 對 package 做約 30 項檢查，分六組：package 與控制面、拓樸對得上、pipeline 與 p4info、
表項、roles、埠與編譯；26 份真實輸出裡，通過的 package 各有 21–25 個 PASS；
唯一一次 FAIL 是 basic_tunnel 骨架：9 個問題，第一個是表項指名的 `MyIngress.myTunnel_exact` 不在它自己的 p4info 裡 ⇒ rc 1，fabric 根本沒起。

## 資料來源

P ＝ `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep`；
T06 ＝ `P/live-p1/runs/2026-09-27T074635Z_06_thirteen/00_table.tsv`；BT ＝ `P/runs/2026-09-27T075454Z_basic_tunnel_skeleton_ndtwin.md`。

| 用途 | 檔（path:line 或 JSON key） | commit／binary |
|---|---|---|
| 25 份 arm 的 pre-flight 輸出 | T06 第 5 欄指的 26 份 arm report，每份第一個 `pre-flight: ` 區塊（N2 那一步）；腳本斷言同一份 report 裡的其他副本（`ndt up` 內、transcript 內）逐列一致 | T06 站在 `5dc7fc9a`（各 arm report 的 `ndt status` code 行） |
| 少一份的原因 | `T06:26` flowcache/skeleton `RED ARM (1/1): skeleton does not com…`：p4c 拒編，走不到 convert 與 pre-flight，report 裡沒有 pre-flight 區塊 | — |
| 第 26 份 | `P/live-p1/runs/2026-09-26T202055Z_07_roles_basic/12_preflight_basic_roles.txt:1-36`（25 PASS，含 roles 三列） | `01_binaries.txt:1` repo HEAD `b2eeb71d` |
| 每列右邊的數字 | 上面 26 份輸出裡，該 check 以 PASS／INFO／FAIL 出現的份數（同一份裡 `s1..s4 pipeline` 合成一列 `sN pipeline`；沒標名字的 FAIL 續行併入上一個 check） | — |
| 「21–25」PASS | 通過的 24 份 T06 輸出各 21–24 個 PASS（p4runtime、flowcache 各 21；multicast 24），07 那份 25 | — |
| 拒絕：FAIL 那一列 | `BT:113`（`FAIL  entries match p4info  9 problem(s); first: s1 entry 3: table 'MyIngress.myTunnel_exact' is not in the p4info (it has: MyIngress.ipv4_lpm)`），續行 `BT:114-119` | — |
| 拒絕：結論與 rc | `BT:127`（`FAIL -- 7 check(s) failed; do NOT bring this package up`）、`BT:239`（`pre-flight FAILED (rc 1)`）、`BT:244` 與 `T06:10`（`RED ARM (1/1): the skeleton does not get past the control plane, by design`，rc 1） | — |
| 每個 check 的名字還在碼裡 | `tools/p4_exercise/preflight.py`（腳本逐一斷言；例：`run()` 的檢查順序 `:292-326`，表項檢查 `:1081-1147`） | trunk `fed37cff`（這支檔與 `3d740be0` 相同；最後改動 `c21deca3`） |

## 可信度

**OBSERVED（跑過，真實 pre-flight 輸出）**
- 每列的 PASS／INFO／FAIL 份數、21–25、basic_tunnel 骨架的那一列 FAIL 與 rc 1、它沒有 `ndt up` 那一步（腳本斷言 BT 裡沒有 `== ndt up p4 --app`）。
- T06 的 25 份 arm report 與 07 的 `12_preflight_basic_roles.txt` 都在 **audit-raw `797c34ab`**（與工作樹比 blob hash 相同）。

**READ（讀碼，沒有執行）**
- 檢查的名字與順序來自 `preflight.py`（`run()` `:292-326`）。
- `FAIL -- 7 check(s) failed` 的「7」其實是 **FAIL 的列數**，不是 check 數：`_check_entries` 把一個 check 的問題拆成最多 7 列
  （第一列＋5 列細節＋「... and N more」，`preflight.py:1136-1142`），`main()` 用 `len(report.failures)` 數列（`:1239`）。
  所以這次是 **1 個 check、9 個問題、7 列 FAIL**。圖上寫的是「9 problems」，沒有用「7」。
- 9 個問題是不是都同一張表：raw 只印出前 6 個（s1、s2 的 entry 3-5），都是 `MyIngress.myTunnel_exact`。
  我讀了這一臂留下的 package 副本（`/home/adam/Desktop/NDTwin-Kernel/.test_run/packages/basic_tunnel-skeleton/s{1,2,3}-runtime.json`，mtime 2026-09-27T07:54Z）：
  每台 3 條 `MyIngress.myTunnel_exact`，共 9。`.test_run` 會被覆寫，不是存檔；所以圖上只寫「first:」。
- 這個拒絕是 exercise 設計好的：tutorials 的 README:41-43 說骨架沒宣告那張表（BT §5 依據欄，【README 宣稱】＋【源碼推導】）。

**INFERRED（我的判斷）**
- **六組怎麼分是我的判斷**（腳本 `GROUPS`）：
  - package & control plane：`format`、`name`、`control_plane.*` 四項、`bmv2.cpu_port`、`switches keys`、`switches name`、`referenced files`
  - topology agrees：`topo_from_json.*` 四項、`switches agree`、`links agree`、`hosts named h<last octet>`、`hosts agree`
  - pipeline & p4info：`switches pipeline`、`sN pipeline`、`p4info parses`、`telemetry.source`（遙測走哪條路由 pipeline 決定，所以放這組）
  - entries：`entries`（外部控制面時的 INFO）、`entries match p4info`、`entries p4info is the pipeline's`、`PRE entries`（multicast／clone）
  - roles：`roles.ipv4_route resolves`、`owned table has no package entries`、`owned table default action`、`roles suggestion`
  - ports & compile：`gRPC port block`、`p4c-bm2-ss`
- 腳本斷言：26 份輸出裡出現的每一個 label 都落在某一組，否則停下。碼裡有、但 26 份都沒出現的 label（例如 `telemetry cooperative is possible`、`roles.ipv4_route owner`）不畫。

## 圖怎麼讀

- 每個框是一組；框裡每列是一個 check 的名字（照 pre-flight 印的原字）。
- 右邊的數字＝26 份真實輸出裡，這個 check 出現為 PASS（綠）、INFO（灰）、FAIL（紅）的份數。
  - 大多數是 26 綠：每一份都查、都過。
  - `entries` 3 灰：p4runtime 兩臂與 flowcache 解答臂是外部控制面，表項由它自己的控制器寫。
  - `PRE entries` 2 綠 24 灰：只有 multicast 兩臂宣告了 multicast group。
  - roles 那組只有 07 那一份（1）有宣告 roles；`roles suggestion` 16 灰是 pre-flight 對沒宣告 roles、但 p4info 有路由表形狀的 package 提示可以怎麼寫。
  - `entries match p4info` 22 綠、1 紅：紅的那一份就是右邊的拒絕。
- 右邊紅框：框標題是 basic_tunnel · skeleton，框裡是那一列 FAIL 的原文（`entries match p4info`、9 problems, first: `MyIngress.myTunnel_exact` not in its p4info）。
  「rc 1、`ndt up` 沒有執行」在 raw 裡（`BT:239`、`BT:244`、`T06:10`），依 rule 2 不寫在圖上（judge F-8），講者備註講。
- 圖例只有 PASS／INFO／FAIL 三個顏色；「數字＝26 份真實輸出裡的份數」這句也不上圖（F-8），只在這裡與講者備註。

## 已知但書

- **髒 checkout（F-16）**：T06 的 arm report code 行是 `5dc7fc9a +95 file(s)`（例 `…basic_solution_ndtwin.md:446`）；07 那輪是 `b2eeb71d +92 file(s)`（`…/2026-09-26T202055Z_07_roles_basic/00_status_before.txt` 的 code 行）；basic_tunnel 骨架沒走到 `ndt up`，report 裡沒有 code 行。圖上沒有印 sha。
- 26 ＝ 25 份 T06 arm ＋ 1 份 07 roles run；不是「26 臂」（fig_t5 的 26 是臂數，巧合同數）。
- `entries match p4info` 的 PASS 細節字面仍寫「recorded, NOT applied in stage one」（例 `…multicast_solution_ndtwin.md:118`），那是第一階段的舊字；
  T06 的表項實際有套用（fig_t6：4/4 applied）。字沒跟上，不影響判定。
- basic_tunnel 骨架的輸出裡，`entries p4info is the pipeline's` 仍是 PASS（表項與 pipeline 指同一份 p4info），失敗的只有 `entries match p4info`。
- pre-flight 通過不代表 exercise 會通過；它只保證 package 自洽、拓樸三方一致、編得過、埠可用。

- 紅測（mutation check）與產圖紀錄：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/o1-o2-t6-t9/`（`run_mutations.py`、`run_mutations.log` 14/14 照預期、`gen_overview.log`、`gen_p4tutorials.log`、各 mutant 輸入檔）。

## 重生指令

```
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/p4-tutorials"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_exercise_path_figs.py
```

最後產出：2026-09-27T17:05Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_exercise_path_figs.py` sha256 `6b2d5e08ced9bb91…`（產圖之後腳本沒再改過）。
