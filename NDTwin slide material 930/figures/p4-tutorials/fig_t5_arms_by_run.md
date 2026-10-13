# `fig_t5_arms_by_run` —— 13 支 exercise × 兩臂，09-16 之後每一次完整 live 跑

[Co-developed with claude code -- Adam]

（本檔所有時間為 UTC；run 目錄名的 `…Z` 就是 UTC。）

## 一句話

09-16 之後在 NDTwin fabric 上的**每一次完整 06 跑（26 臂）**一欄，每支 exercise 兩格（骨架臂｜解答臂）：
綠＝照 exercise 說的表現、紅＝沒照預期、斜線＝沒有判定。每欄底下是「照預期」的臂數（/26）。

## 資料來源（腳本執行時讀取，圖上沒有手抄的值）

K＝`/home/adam/Desktop/NDTwin-Kernel`，E＝`K/doc/audit/2026-09-04_p4-tutorial-exercise-prep`。

| 用途 | 檔 | commit／binary |
|---|---|---|
| 每臂 rc 與判定（欄 3、4） | `E/live-p1/runs/<UTC>_06_thirteen/00_table.tsv`，十個 26 列的 run（下表） | 每個 run 的 arm report `ndt status` 段 `code` 行（下表） |
| 「照預期」的規則 | `E/live-p1/06_thirteen.sh:107-115`（`expected_rc`）、`:142-155`（rc 1 時判定必須以 `RED ARM` 開頭，`:143`） | trunk `3d740be0` 的檔 |
| 每臂是否跑在心跳上 | 00_table.tsv 欄 5 指的 arm report 內含 `heartbeat started (pid` 那一行 | 同上 |
| protobuf 5 的兩欄 | `K/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926/pb5-trial/JOURNAL.txt:6`（「phase3 start: 06 on venv-cand」，候選 venv 是 protobuf 5.29.6，同目錄 `dists_cand.txt`）、`…/pb5-merge/live-accept.log:7`（遷移後的 06 run dir） | — |
| bmv2 | 各 arm report §1：`/usr/local/bmv2-fast/bin/simple_switch_grpc` sha256[:16] `3ff54b5c1901c9d3`（十個 run 相同） | — |

| run（UTC，raw 目錄名） | 照預期 | code（arm report `ndt status` 的 `code` 行） | 心跳臂 | protobuf |
|---|---|---|---|---|
| 2026-09-19T052518Z | 2 | `dfb9d0d7`（`runs/2026-09-19T052720Z_basic_solution_ndtwin.md:457`） | 0 | 3.20.3 |
| 2026-09-19T063235Z | 20 | `cbc968d8`（`…063429Z_basic_solution…:456`） | 0 | 3.20.3 |
| 2026-09-19T083257Z | 23 | `7242e127`＋`1ea07e7b`（跑到一半 trunk 前進了，見但書） | 0 | 3.20.3 |
| 2026-09-19T144328Z | **26** | `f3b6d09c`（`…144521Z_basic_solution…:456`） | 0 | 3.20.3 |
| 2026-09-24T160637Z | 25 | `67b64869`（`…160820Z…:474`） | 0 | 3.20.3 |
| 2026-09-24T185505Z | **26** | `0c96c1d0`（`…185647Z…:474`） | 0 | 3.20.3 |
| 2026-09-26T055148Z | **26** | `580767a8`（`…055331Z…:474`） | 0 | **5.29.6（候選 venv）** |
| 2026-09-26T153300Z | **26** | `cafd518a`（`…153443Z…:446`） | 17 | 3.20.3 |
| 2026-09-26T172913Z | **26** | `3f8c2abf`（`…173056Z…:446`） | 17 | 3.20.3 |
| 2026-09-27T074635Z | **26** | `5dc7fc9a`（`…074826Z…:446`） | 17 | **5.29.6（遷移後）** |

沒進圖的：09-24 的 14 次 `ONLY=ecn` 單支重跑（`…T163427Z` 到 `…T185102Z`，每次 2 列）與 `2026-09-26T062049Z`（4 列，pb5 試跑的主 venv 對照）——不是完整 26 臂。

## 可信度

**OBSERVED（跑過）**：每一格都是 live 跑的 raw（`00_table.tsv`），腳本逐列讀；「照預期」的判法照 `06_thirteen.sh` 的規則在腳本裡重算，不是抄 run 的最後一行。
🔴 這些 raw 在 kernel checkout 的 trunk 上**未進版控**（`git ls-files` 0 筆）＝未提交的觀測。audit-raw `797c34ab` 收了哪幾個 run，見下方「已知但書」最後一條。

**READ（讀過）**：「照預期」的定義（`06_thirteen.sh:107-115`、`:142-155`）。

**INFERRED**：無。

## 圖怎麼讀

- 前三欄是 09-19 當天的開發輪，紅／斜線的原因各在 TICKET-P3 §9 有裁定（`E/TICKET-P3-observation.md`）：
  - `05:25` 的 24 格斜線＝`ndt down` 留下殘留、判定成 `ERROR -- LAB NOT RETURNED`（裁決 19①、20，`:172-173`）；exercise 本身的期望除了 qos 兩格都達成。
  - `06:32` 的 basic_tunnel/solution 斜線＝proxy 拒收上游 runtime json 的單元素 exact 值，`ndt up` 沒起來（裁決 23②，`:176`；修在 `7d6c88a2`）——**這一格是 NDTwin proxy 的缺陷**；mri 兩格是 driver 解析 bug（23①）；p4runtime／flowcache 解答臂當時歸因於機器負載（23③）；qos 骨架臂是儀器（20②）。
  - `08:32` 的三格紅＝通用格 G1 的參數設計（裁決 26，`:179`）。
- `09-24 16:06` 的 ecn/solution 紅＝ECN 標記檢查只看得到 2–4 個探測封包，是鑑別力不足的儀器；裁決 7 把探測改成 60 個（`0c96c1d0`），斷言一字未改，之後完整跑一次 26/26（`K/doc/audit/2026-09-24_p4-driven-api-shape/REPORT-P4-2026-09-25.md` §2 第 1 條、§5）。
- 格內白點＝該臂的 arm report 記錄了 `ndt up` 啟動心跳（09-26 起的三個 run，每個 17 臂）。
- 「protobuf 5」標在兩欄：09-26 05:51 是**試跑**（proxy 用候選 venv），09-27 07:46 是**遷移後**的驗收 run。

## 已知但書

- 09-19T083257Z 的 arm reports 指名兩個 code（11 份 `1ea07e7b`、13 份 `7242e127`）：共用 checkout，trunk 在這次 25 分鐘的 run 中前進。`1ea07e7b` 是 TICKET-P3 裁決 25 的文件 commit。
- **髒 checkout**：每個 run 的 arm report `code` 行都帶未提交檔數——052518Z `dfb9d0d7 +47`、063235Z `cbc968d8 +54`、083257Z `7242e127`／`1ea07e7b` 皆 `+60`、144328Z `f3b6d09c +61`、160637Z `67b64869 +64`、185505Z `0c96c1d0 +79`、055148Z `580767a8 +83`、153300Z `cafd518a +88`、172913Z `3f8c2abf +91`、074635Z `5dc7fc9a +95`（行號見上表；083257Z 見各 arm report）。其中會改變行為的 2 個：`p4_proxy/mininet/host_count_override`、`tools/remote-lab/dorm_lab/`（T06 另有 `app_package_override`）。圖上不印 sha，所以圖面沒有「dirty」字樣。
- 🔴 flowcache/solution 在 09-27 那欄是綠，但它的 G1（鏈路使用率格）當輪 iperf 0 個 datagram 到 h3（GAP-2b §4-1；09-28 提交 `c8433963`）；這張圖的綠只代表 **arm 的判定**照預期，不代表 G1 那一格是送達的證據。
- 這張圖**不是**「NDTwin 看得見這 13 支的流量」的證據；那一欄在 `fig_t1b` 的 twin sees it。
- audit-raw `797c34ab`（依 coordinator 已公開在兩個 P4 repo；本檔未自己打公開 URL）：`git ls-tree -r 797c34ab` 有 09-19T144328Z、09-24 兩個、09-26 三個與 **09-27T074635Z（T06）** 共七個完整 run，各 27 個檔、逐檔 blob 與工作樹相同（2026-09-27 17:2xZ 本機比對）；**沒有** 09-19 前三個開發輪（052518Z、063235Z、083257Z）；那三欄 2026-09-27 UTC 起在 audit-raw **`5cf0364c`**（`797c34ab` 的後代；各 27 檔與它們的 arm report 403 檔，blob 與工作樹相同，本機比對；公開性依 coordinator 的未認證 `git ls-remote`）。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/p4-tutorials"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_arms_grid.py
```

產出 `fig_t5_arms_by_run.{pdf,png,svg}`＋`_hires/fig_t5_arms_by_run.png`。最後產出：2026-09-27T16:20Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_arms_grid.py` sha256 `8c746a4a1464c40f…`（產圖之後腳本沒再改過）。
