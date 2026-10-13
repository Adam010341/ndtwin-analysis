# fig_o2_thirteen —— 13 支 exercise 兩臂都照預期的支數，每一輪完整 live run

[Co-developed with claude code -- Adam]

## 一句話

09-16 報告時，13 支 exercise 還沒有一支在 NDTwin fabric 上跑過（圖上畫成刻度外的「not run」，不是 y＝0）；09-19 那天四輪完整 run 從 0 → 8 → 10 → 13，
之後六輪裡五輪是 13/13，唯一一次掉到 12（09-24 16:06Z，ecn 的探測儀器），同日 18:33Z 合併修正後、18:55Z 又回到 13。

## 資料來源

L ＝ `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs`。

| 用途 | 檔（path:line 或 JSON key） | commit／binary |
|---|---|---|
| 09-19 05:25Z 的 0 | `L/2026-09-19T052518Z_06_thirteen/00_table.tsv`（26 列：24 臂 verdict 是 ``ERROR -- LAB NOT RETURNED: `ndt down` exited 1``＝無判定，2 臂照預期） | arm report code 行 `dfb9d0d7` |
| 09-19 06:32Z 的 8 | `L/2026-09-19T063235Z_06_thirteen/00_table.tsv`（20 照預期、5 不照、1 無判定；缺 qos、mri、basic_tunnel、p4runtime、flowcache） | `cbc968d8` |
| 09-19 08:32Z 的 10 | `L/2026-09-19T083257Z_06_thirteen/00_table.tsv`（23 照預期、3 不照；缺 ecn、p4runtime、flowcache） | `1ea07e7b`＋`7242e127`（跑到一半 trunk 動了，兩顆都列） |
| 09-19 14:43Z 的 13 | `L/2026-09-19T144328Z_06_thirteen/00_table.tsv`（26 照預期） | `f3b6d09c` |
| 09-24 16:06Z 的 12 | `L/2026-09-24T160637Z_06_thirteen/00_table.tsv`（25 照預期；ecn 解答臂不照） | `67b64869` |
| 09-24 18:55Z 的 13 | `L/2026-09-24T185505Z_06_thirteen/00_table.tsv` | `0c96c1d0` |
| 09-26 05:51Z 的 13 | `L/2026-09-26T055148Z_06_thirteen/00_table.tsv` | `580767a8` |
| 09-26 15:33Z 的 13 | `L/2026-09-26T153300Z_06_thirteen/00_table.tsv` | `cafd518a` |
| 09-26 17:29Z 的 13 | `L/2026-09-26T172913Z_06_thirteen/00_table.tsv` | `3f8c2abf` |
| 09-27 07:46Z 的 13 | `L/2026-09-27T074635Z_06_thirteen/00_table.tsv` | `5dc7fc9a`（protobuf 5 之後） |
| 09-08「not run」（context，灰色空心方塊，畫在刻度下方） | `/home/adam/Desktop/NDTwin slide material/NDTWIN slide material 916/NDTwin-slide-template-916.md:257`「**0/13 在 NDTwin fabric 上跑過。**」（工作樹，mtime 2026-09-16T04:41Z；同一句在該 repo 已提交的 `da73ccf` 版第 92 行） | 09-08 跑的是 tutorials 自己的 harness，不是 NDTwin fabric |
| 「照預期」的規則 | `live-p1/06_thirteen.sh:107-150`（已提交 `bfe1f79a`）；腳本裡的 `classify()` 是從 `../p4-tutorials/make_arms_grid.py` 抄過來的（沒 import） | — |

- commit 欄＝每輪 arm report 裡 `ndt status` 的 `code` 行（腳本讀出、取聯集）。
- 只收 26 列的完整 run；09-24 的 14 輪 ecn 重跑（各 2 列）與 09-26T062049Z（basic、p4runtime，4 列）是部分 run，腳本印 `[skip]` 後略過。

## 可信度

**OBSERVED（跑過，從 live raw 讀出）**
- 10 輪 `00_table.tsv` 的 rc 與 verdict，以及每支 exercise 兩臂的分類；每輪的 code sha。
- 05:25Z 那輪 24 臂的 verdict 字面就是 ``ERROR -- LAB NOT RETURNED: `ndt down` exited 1``：是收尾沒把 lab 交回，不是 exercise 失敗。
- raw 狀態：144328Z 之後的 7 輪，`00_table.tsv` 與每輪 26 份 arm report 都在 **audit-raw `797c34ab`**（與工作樹比 blob hash，全部相同）；
  09-19 早上三輪（052518Z、063235Z、083257Z）不在 797c34ab；**2026-09-27 UTC 起在 audit-raw `5cf0364c`**（`797c34ab` 的後代；三個 run 目錄各 27 檔與它們的 arm report，blob 與工作樹相同，integrator 本機比對；公開性依 coordinator 的未認證 `git ls-remote`）。

**READ（讀文件，不是執行）**
- 09-08 的「not run」：模板那句說的是「0/13 在 NDTwin fabric 上**跑過**」——跑過的支數，和 y 軸的「兩臂都照預期」不是同一個量（judge F-7）；所以畫成刻度外的 not run 方塊，不是 y＝0。那句是 09-16 deck 讀 GAP-ANALYSIS 的結論，不是本圖腳本量的。
- 規則本身（`06_thirteen.sh:107-150`）。
- 05:25Z 那輪的處置（TICKET-P3 §9 裁決 19-20）與 06:32Z basic_tunnel 解答臂無判定的原因（裁決 23(2)：`ndt up` 在任何封包之前就停了）：出自 `make_arms_grid.py` docstring，我沒有重讀裁決；raw 裡那一臂的 verdict 只有 `ERROR` 五個字。
- 「16:06Z 掉的那一支是 ecn 的探測儀器，修在 driver」：出自 merge `0c96c1d0` 的訊息（mark 斷言沒改）。

**INFERRED**
- 無。圖上每個數字都是腳本從 `00_table.tsv` 算的。

## 圖怎麼讀

- y ＝ 13 支 exercise 裡，骨架臂與解答臂**兩臂都照 exercise 說的方式表現**的支數。
  「照預期」：解答臂 rc 0 且 PASS；骨架臂 rc 0 且 PASS——flowcache 與 basic_tunnel 的骨架例外，要 rc 1 且 verdict 以 `RED ARM` 開頭；
  verdict 以 `ERROR` 開頭＝無判定，不算。
- x ＝ 每一輪完整 run，上排是 UTC 開始時間、下排是日期；同一天的 run 靠在一起。
- 虛線左邊、刻度下方的灰色空心方塊＝09-08 的狀態：not run（沒有在 NDTwin fabric 上跑過）。它不在 y 軸刻度上。虛線右邊才是 09-16 之後。
- 05:25Z 那個空心藍點標「no verdict」：26 臂裡 24 臂沒有判定，0 不是「13 支都失敗」。
- 跟 fig_t5 是同一批 run、同一條規則：t5 畫逐臂，本圖只數兩臂都綠的支數。

## 已知但書

- **髒 checkout（F-16）**：十輪的 code 行都帶未提交修改：052518Z `+47`、063235Z `+54`、083257Z `+60`、144328Z `+61`、160637Z `+64`、185505Z `+79`、055148Z `+83`、153300Z `+88`、172913Z `+91`、074635Z（T06）`+95` file(s)。圖上沒有印 sha。
- 06:32Z 那輪也有 1 臂無判定（basic_tunnel 解答臂，verdict `ERROR`），所以 8 是下限。
- 08:32Z 那輪跨了兩顆 commit（trunk 在 25 分鐘的 run 中間動了）。
- 階梯線只連完整 run；兩輪之間的平線**不代表**那段時間有人量過。09-18 的 live-p1 第一階段 run（02_app_basic 等）不是 26 臂的 06，不在圖上。
- 09-27 那一點在 protobuf 5 之後；本圖沒有效能數字，所以可以同圖（brief 規則 7 只禁效能數字跨 protobuf 5 同圖）。
- 「13/13」＝exercise 自己的判定都照預期；**不等於** twin 看得到每一支的自訂標頭流量（見 fig_t9）。

- 紅測（mutation check）與產圖紀錄：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/o1-o2-t6-t9/`（`run_mutations.py`、`run_mutations.log` 14/14 照預期、`gen_overview.log`、`gen_p4tutorials.log`、各 mutant 輸入檔）。

## 重生指令

```
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/overview"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_overview_figs.py
```

最後產出：2026-09-27T19:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_overview_figs.py` sha256 `08a4eb2183c6da85…`（產圖之後腳本沒再改過）。
