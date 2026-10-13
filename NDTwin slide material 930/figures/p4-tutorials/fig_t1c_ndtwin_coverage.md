# `fig_t1c_ndtwin_coverage` —— NDTwin 涵蓋了什麼：09-16 對 09-27（T1 頁，2026-09-27 UTC 依判官 F-2 重切，第二輪再改）

[Co-developed with claude code -- Adam]

（本檔所有時間為 UTC；run 目錄名的 `…Z` 就是 UTC。）

## 一句話

只留 09-16 之後變了的部分，分三個有標題的面板：
**BACKGROUND · READ THE CODE**（NDTwin 自己那支 P4 的 16 維，全讀碼；就是 916 deck 那一列，灰底背景帶，標「as shown 09-16; read 09-08, trunk 1a284f75」）、
**RAN · JUDGED · 09-27**（每支 exercise 帶自己的 P4 跑在 NDTwin fabric 上時，歸 NDTwin 的那一半——GAP-2b 依跑過的證據下的判斷；兩格只有讀碼，以 × 斜線標，圖例「cannot · read only」）、
**T06 · 09-27**（13 支：runs on NDTwin 欄標 **RAN IT**、twin sees it 欄標 **JUDGED**，與 T7 同一用詞）。
四個判斷格已由 **Adam 2026-09-28 裁定**（`registers`＝部分、`queue_metadata`＝做得到、multicast 的 twin＝看得到、flowcache 的 twin＝IPv4 only），圖上不再有虛線框；圖右上標「as of GAP-2b with Adam's 2026-09-28 ruling」。

## 和 `fig_t1b_requirements_matrix_0927` 的關係（為什麼重切）

- 判官 F-2（`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926/slides930/judge-SLIDES930.md:99-108`）：
  t1b 上半的 13×16 需求矩陣與 916 deck 第 3 頁逐格相同，違反 delta only；而且讀碼列、混合列、跑過＋判斷的右欄擠在同一張沒標題的表。
- coordinator 2026-09-27 UTC 裁：拿掉 13×16，只留兩列 NDTwin 與右兩欄，分成有標題的面板，四個待審格加虛線（09-28 Adam 裁定後拿掉）。
- **第二輪（coordinator 更正自己第一輪的裁決）**：flowcache 的 twin 格**不是**「no evidence」，而是與 T7 同一個字「**IPv4 only**」（橘），當時保留虛線待審框；twin 計數因此是 **6／4／3**。09-28 Adam 裁定同一個值，GAP-2b 的那一格也改成「只看過 IPv4」，腳本不再覆寫。
  依據是 T06 那一臂的 raw：**T06 的流只到了 s1→s3 那一段，沒有送達 h3**（s1-eth3 就是 s1 往 s3 的那條線：tutorials `exercises/flowcache/topology.json:48-51` 的 `["s1-p3", "s3-p2"]`，Mininet 的 pN＝ethN；tutorials checkout `c80d83e`，乾淨）——twin 在 s1-eth3 讀到流量、在 s3 每個介面讀 0，而介面計數器說位元組正是這樣走的，所以 s3 的 0 是**正確的讀數**，不是 twin 的錯（見下表）。
  第一輪說「流沒離開 s1」「GAP-2b 的綠用的是 09-26 那輪」都是錯的：流是從 s1-eth3 離開 s1 的；GAP-2b 的 flowcache 列先引的是 T06 的 `flowcache/sol:588-604`，09-26 那輪是第二個引用。
- 09-16 那一列（第二輪，coordinator 第 4 項）：它就是 916 deck 的「NDTwin today」列，讀的是 GAP-2（trunk `1a284f75`，09-08 讀），所以放進灰底背景帶並標日期。
- `fig_t1b_*` 檔案保留在同目錄（由 916 複製），**不在 deck 裡**。

## 資料來源（腳本 import `make_tutorial_figs_0927.py` 的解析與斷言，沒有手抄格值）

E＝`/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep`；FC＝`E/runs/2026-09-27T081256Z_flowcache_solution_ndtwin`

| 用途 | 檔 | 狀態 |
|---|---|---|
| NDTwin 09-16 那列（1／9／6） | `E/GAP-2-ndtwin-p4-capabilities.md` §1 與「計數」行（`:39`）；讀的是 trunk `1a284f75`（`:10`），916 模板 `:254` 記這份盤點是 09-08 的 | 已提交（`532b6c31`）；背景 |
| NDTwin 09-27 那列（8／6／2）、read-only 兩格、兩個判斷格 | `E/GAP-2b-ndtwin-p4-capabilities-2026-09-27.md` §1 與「計數」行（`:105`）；read-only＝依據欄與位置欄都沒有【跑過】的格（`meters`、`digest`）；判斷格＝依據欄帶 `(judgement)`（`registers`、`queue_metadata`） | 🔴 **未提交，待 Adam 審** |
| 右兩欄 | GAP-2b §3 逐支表與彙總（`:192-208`）；逐臂對 T06 `E/live-p1/runs/2026-09-27T074635Z_06_thirteen/00_table.tsv` 斷言 verdict／rc／報告時間戳 | T06 在 audit-raw `797c34ab` |
| flowcache 的 twin 格＝IPv4 only | twin 自己的讀數 `FC/link_usage/twin_integral.txt:3`（`s1-eth3 31787577.500`，即約 31.8 Mbit）、`:7-9`（s3-eth1／2／3 都是 0.000）；介面計數器 `FC/link_usage/netdev.before:7`→`netdev.after:7`（s1-eth3 3151 → 4596340 B）、`netdev.before:3`→`netdev.after:3`（s3-eth1 3531 → 3804 B，+273）；`FC/link_usage/onpath.txt:1`（主路徑只有 `s1-eth3`）；沒有送達：`FC/link_usage/iperf_server.txt`（沒有報告列）、`iperf_client.txt:10`（沒收到 server 的 ack）。GAP-2b 的判斷（看得到 (judgement)）在 `:206`，先引 T06 的 `flowcache/sol:588-604` | T06；code `5dc7fc9a +95`（髒）；audit-raw `797c34ab` |

腳本對 flowcache 的停止條件（`flowcache_t06_reading()`）：twin 在 s1-eth3 的讀數必須 > 0、s3 三個介面必須都是 0；netdev 的 s1-eth3 增量 > 1 MB 且 s3-eth1 增量 < 1 kB；onpath 只有 s1-eth3；client 沒收到 ack；server 沒有報告列；GAP-2b 那一格仍是「看得到」——任一條變了就停。

## 可信度（面板即分級）

- **BACKGROUND · READ THE CODE**：09-16 那列 16 格全是讀碼（GAP-2 §0），是 916 已講過的一列，只當對照。
- **RAN · JUDGED · 09-27 列**（第三輪改標：格子是 GAP-2b 依跑過的證據下的判斷，與右邊 twin 欄同理）：14 格的依據含【跑過】；`meters`、`digest` 兩格只有讀碼（× 斜線），而且都是「做不到」——圖例寫「cannot · read only」，腳本斷言 read-only 格都是做不到（GAP-2b `:93`、`:95`、計數 `:105`）。`registers`（部分）、`queue_metadata`（做得到）是判斷格，Adam 09-28 裁定照原值（GAP-2b 標「（Adam 2026-09-28 裁定）」）。
- **T06**：runs on NDTwin 13/13 是 **RAN IT**。twin sees it 欄是 **JUDGED**（讀同一批 run 的 raw 判的）：看得到 6／只看過 IPv4 4／無證據 3。
  與 GAP-2b §3 的彙總相同（裁定後是 6／4／3；裁定前 GAP-2b 寫 7／3／3，本圖當時依 coordinator 第二輪裁決把 flowcache 改為 IPv4 only）。multicast 的「看得到」與 flowcache 的「IPv4 only」由 Adam 09-28 裁定。
- 🔴 兩列回答不同的問題：09-16 問「NDTwin **自己那支** P4 有沒有」，09-27 問「exercise 帶自己的 P4 跑在 NDTwin 上時，歸 NDTwin 的那一半是不是 NDTwin 做的」。
  變化一部分是 NDTwin 多做了事，一部分是題目換了（GAP-2b §2）。**不可講成「NDTwin 多了 7 個能力」。**
- 🔴 所有 arm report 的 `code` 行都是髒 checkout（T06 為 `5dc7fc9a +95 file(s) with uncommitted changes`，其中 3 個會改變行為）。

## 紅檢

`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/t1c-coverage-redcheck.sh`（git-ignored）：
- 09-28（Adam 裁定後）最終腳本：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/t1c-coverage-redcheck-ruling-20260928T0654Z.log`（`make_coverage_0930.py` sha256 `703bd7cbcd1c0033…`、模組 `2fb264715cd03b6f…`）：對照組 rc 0；**12 個停止條件各有一個竄改，12 個都 rc 1**、印出對應原因——前 9 個與第三輪相同（twin 讀數、netdev、onpath、client、server、T06 路徑、read-only 兩條）；新的 3 個：拿掉 `registers` 的裁定標記（四個裁定格移動）、`queue_metadata` 又標 `(judgement)`（還有未裁定的格）、GAP-2b 的 flowcache 格改回「看得到」（不是裁定的 IPv4 only）。
- 第三輪 `t1c-coverage-redcheck-r3-20260927T1943Z.log`（`2ac46740…`，11 個）、第二輪 `…-r2b-20260927T1854Z.log`（`54619b12…`，10 個）與 `…-r2-20260927T1838Z.log`、第一輪 `…-20260927T1735Z.log`（`30ef2f79…`，4 個）保留作紀錄。
- 腳本 import 的 `make_tutorial_figs_0927.py`（GAP-2／GAP-2b 解析與 T06 逐臂對帳）的紅檢：59 個停止點 69/69、7 個到不了（`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_tutorial_figs_0927-redcheck-20260928T0656Z.log`）。

## raw 狀態

T06 與 flowcache 那一臂的 raw 在 audit-raw `797c34ab`（T06 目錄 27 檔逐檔 blob 與工作樹相同，2026-09-27 17:2xZ 本機比對；依 coordinator 已公開在兩個 P4 repo）。GAP-2 已提交（trunk）；**GAP-2b 在 09-28 Adam 裁定後由 coordinator 讀 diff 提交**：`c8433963`（07:15Z；08:19Z 未認證查已在公開 trunk 上），內容 sha256 `77afc4d5…`＝本圖讀的那份（我改的只有四格、它們的六個標記與 §3 彙總行）。

## 圖怎麼讀

- 左兩列共用下方 16 個維度名；每列右邊是「做得到／部分／做不到」的格數。上面那列在灰底背景帶裡。
- 右欄：13 支依 GAP-ANALYSIS §6 的階段順序；底下是兩欄各自的計數（runs 13/13；twin 6／4／3）。
- 圖上只有標題、面板標題、軸標籤、數值與圖例。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/p4-tutorials"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_coverage_0930.py
```

最後產出：2026-09-28T06:59:08Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_coverage_0930.py` sha256 `703bd7cbcd1c0033…`、import 的 `make_tutorial_figs_0927.py` `2fb264715cd03b6f…`（09-28：讀 Adam 的裁定、拿掉虛線框與覆寫、加 as-of；重生紀錄 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-refresh-20260928T0658Z.log`，rc 0）。上一版（09-27 19:51Z，`2ac46740…`）已被取代。
