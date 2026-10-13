# fig_o1_since_0916 —— 09-16 之後落地了什麼，六條主線各一列

[Co-developed with claude code -- Adam]

## 一句話

09-16 報告之後到 09-27，六條主線各自落地：外來 P4 程式的 package 工具與 `ndt up p4 --app`（09-17）、
每台跑自己的程式（09-18）→ 13 支 exercise 兩臂第一次全部照預期（09-19）→ roles 第一刀（09-24）、
心跳段 W 與 H1–H5 live（09-26）、`ndt serve`（09-26／09-27）、protobuf 5 與 main 只經 PR（09-27）。
圖上每個日期都是腳本當場從 git 或 run 目錄名算出來的，時間一律 UTC。

## 資料來源

K ＝ `/home/adam/Desktop/NDTwin-Kernel`；L ＝ `K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs`。

| 用途（圖上的標籤） | 檔（path:line 或 JSON key） | commit／binary |
|---|---|---|
| 「convert · pre-flight · --app」◇（09-17 12:44Z）＋ 第二個 ◇（14:31Z） | `git show -s --format=%cI 386eb20c`（P1-B，tools/p4_exercise）、`54f69d15`（P1-C，`ndt up p4 --app`） | merge `386eb20c`、`54f69d15` |
| 「own program per switch」◇（09-18 07:57Z） | `git show -s --format=%cI b392f111`（P2-A） | merge `b392f111` |
| 「link-level telemetry」◇（09-18 19:56Z） | `git show -s --format=%cI f5ad6890`（P3-B） | merge `f5ad6890` |
| 「three-group campaign」●（09-19 11:57Z） | 目錄名 `K/doc/audit/2026-09-19_telemetry-three-groups/raw/2026-09-19T115737Z_full`；`FINDINGS.md:17` 同一個 run id | FINDINGS.md 已提交 `611a08d3`；raw 在 audit-raw `797c34ab` |
| 「first 13/13」●（09-19 14:43Z） | `L/2026-09-19T144328Z_06_thirteen/00_table.tsv`（26 列，腳本用 06_thirteen.sh 的規則重算 13/13，並斷言它是 09-16 之後第一個 13/13 的完整 run）；`REPORT-P3-2026-09-24.md:99-102` 寫同一件事 | 26 份 arm report 的 `ndt status` code 行 ＝ `f3b6d09c` |
| 「roles first cut」◇（09-24 16:00Z）＋ ●（16:02Z） | `git show -s --format=%cI 572d9462`；`L/2026-09-24T160256Z_07_roles_basic/01_binaries.txt:1`（repo HEAD 572d9462…） | merge `572d9462`；run 站在同一顆 |
| 「ecn probe fix, 13/13」◇（09-24 18:33Z）＋ ●（18:55Z） | `git show -s --format=%cI 0c96c1d0`；`L/2026-09-24T185505Z_06_thirteen/00_table.tsv`（26 列，13/13） | merge `0c96c1d0`；arm report code 行 ＝ `0c96c1d0` |
| 「local API merged」◇（09-26 00:05Z） | `git show -s --format=%cI 48209682` | merge `48209682` |
| 「segment W, live H1–H5」◇（09-26 15:24Z）＋ ●（15:26Z）＋ ●（17:29Z） | `git show -s --format=%cI cafd518a`；`L/2026-09-26T152605Z_08_heartbeat/01_binaries.txt:1`（repo HEAD cafd518a…），腳本斷言 H1 `30_cycles.tsv`、H3 `64_cycle.tsv`、H4 `82_flowentry_add.code` 存在；`L/2026-09-26T172912Z_08_heartbeat/51_06.txt:145`（`PASS 06_thirteen -- 26 arm(s)`） | merge `cafd518a`；H5 那輪站在 `3f8c2abf`（其 `01_binaries.txt:1`） |
| 「protobuf 5, 13/13」◇（09-27 07:43Z）＋ ●（07:46Z） | `git show -s --format=%cI 5dc7fc9a`；`L/2026-09-27T074635Z_06_thirteen/00_table.tsv`（26 列，13/13） | merge `5dc7fc9a`；arm report code 行 ＝ `5dc7fc9a` |
| 「own page (GUI v1)」◇（09-27 12:35Z） | `git show -s --format=%cI f186ce98` | merge `f186ce98` |
| 「main via PRs only」◇（09-27 13:43Z） | `git show -s --format=%cI 3d740be0`（一般 commit，改 CLAUDE.md） | commit `3d740be0` |
| 09-30 粗體刻度 | 腳本常數 `REPORT_DAY`（報告日，不是量測、上面沒有事件） | — |

- 每個 merge 腳本都斷言：兩個 parent、主旨還寫著那個分支名；`3d740be0` 斷言是一個 parent。
- `git -C K show -s --format=%cI <sha>` 給的是 +08:00，腳本換成 UTC 再畫。

## 可信度

**OBSERVED（跑過，從 live raw 讀出）**
- 7 個 live run 目錄的時間（目錄名的 UTC 戳）與內容：`144328Z` 與 `185505Z`、`074635Z` 三輪 06 的 13/13（由 `00_table.tsv` 重算）；
  `160256Z_07` 的 repo HEAD；`152605Z_08` 的 H1／H3／H4 檔存在；`172912Z_08` 的 H5 PASS 行；telemetry `115737Z_full` 目錄存在。
- 以上 7 個 run 目錄不在 kernel checkout 的版控裡，但都在 **audit-raw `797c34ab`**（與工作樹逐檔比 blob hash，全部相同）。
  協調者說 797c34ab 已在兩個 P4 repo 公開；這一點我沒有打公開 URL 驗。

**READ（讀紀錄，不是執行）**
- 11 顆 merge／commit 的日期、parent 數、主旨：`git show`（唯讀）。merge 的日期只說「什麼時候併進 trunk」，不說它「跑起來了」。
- `FINDINGS.md:17`、`REPORT-P3-2026-09-24.md:99-102` 與 raw 一致（兩份都已提交）。

**INFERRED（判斷，未驗證）**
- 挑哪些當里程碑、放哪一列，是我的判斷。例：protobuf 5 放「engineering」而不是「P4 exercises」；
  package 工具（P1-B/P1-C）與 P2-A 放「foreign-P4 API」。
- 09-17／09-18 三個 ◇ 與 telemetry 的 P3-B ◇ **不在 orchestrator 的候選清單裡**，是我加的：
  trunk first-parent 在 09-17 有 5 個 merge、09-18 有 11 個（`TZ=UTC git log --merges --first-parent trunk`），不畫會讓這兩天看起來是空的。
  不要的話刪 `milestones()` 裡 `386eb20c`、`54f69d15`、`b392f111`、`f5ad6890` 那幾行。

## 圖怎麼讀

- 每列一條主線；◇ ＝ merge／commit，● ＝ 跑過的 live run；x 軸是 UTC 日期，每格一天。
- ◇ 裡面有 ● ＝ 併進去之後幾分鐘內就在那顆 commit 上跑了 live：
  roles 2 分鐘、心跳 1.5 分鐘、protobuf 5 3 分鐘、ecn 修正 21 分鐘（都由上表的時間相減）。
- 心跳那列有兩個 ●：15:26Z 的 H1–H4、17:29Z 的 H5，同一個標籤。
- 09-20～09-23 沒有東西是真的：trunk first-parent 那四天 0 個 commit（同上 git log）。
- 09-30 只是一個刻度（報告日）。

## 已知但書

- **髒 checkout（F-16）**：每一輪都站在有未提交修改的工作樹上（`ndt status` code 行的 +N）：144328Z `f3b6d09c +61`、160256Z_07 `572d9462 +61`、185505Z `0c96c1d0 +79`、152605Z_08 `cafd518a +85`、172912Z_08 `3f8c2abf +89`、074635Z（T06）`5dc7fc9a +95`、telemetry 115737Z `+60`（G2–G6 的 `11_verify.txt:17` 都是 `4d3f294f +60`，G1 是 `f4dd9f22 +60`；M1 用的是 G2、G3）。圖上沒有印任何 sha，所以沒有要標 (dirty) 的地方。
- **時區（F-18）**：全部用 UTC。`0c96c1d0` 的 committer date 是 `2026-09-25T02:33:52+08:00`＝`2026-09-24T18:33:52Z`，所以落在 09-24；`f5ad6890` 是 `2026-09-19T03:56:52+08:00`＝`2026-09-18T19:56:52Z`。別頁若用 +08 日期，同一顆 commit 會差一天。
- **「live H1–H5」的 PASS 行在 orchestrator 的終端紀錄裡，不在 run 目錄**（integrator 2026-09-27 UTC 補查）：H1–H4 那輪 run 目錄沒有存 stdout（GAP-2b §4 第 6 點；GAP-2b 09-28 提交為 `c8433963`，已公開），但 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926/hbw-live/h14-20260926T152605Z.log:190` 是 `PASS 08_heartbeat`；H5 重跑那輪 `…/hbw-live/h5b-20260926T172912Z.log:59` 也是 `PASS 08_heartbeat`，另有 run 目錄裡的 `51_06.txt:145`。兩份 log 都未提交。
- **merge ≠ 跑過**：只有 ● 是跑過；ndt serve 兩個 ◇ 在圖上沒有 ●（它的 live walk 在 09-24 的 `3273df8b` 上，見 `48209682` 的 merge 訊息，READ）。
- **沒畫的**：09-18 的 live-p1 第一階段 run（01／02／02b／03）；09-24 的 14 輪 ecn 重跑（各 2 列）與 09-26T062049Z（basic、p4runtime，4 列）；
  09-26 的第二輪 07（`202055Z`）；09-26 的三輪 06（在 fig_o2）；`fed37cff`（09-27 之後只動測試的 merge）。
- **protobuf 5**：圖上沒有任何效能數字；前後的效能數字不可放同一張圖（brief 規則 7）。
- 「roles first cut」是 TICKET-P4-roles 第一刀；外來程式的 external 模式 detect-only 還沒做完——**不要說「NDTwin 可以操作外來 P4 程式」**。

## 重生指令

```
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/overview"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_overview_figs.py
```

同一支腳本也產 fig_o2_thirteen。

- 紅測（mutation check）與產圖紀錄：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/o1-o2-t6-t9/`（`run_mutations.py`、`run_mutations.log` 14/14 照預期、`gen_overview.log`、`gen_p4tutorials.log`、各 mutant 輸入檔）。

最後產出：2026-09-27T19:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_overview_figs.py` sha256 `08a4eb2183c6da85…`（產圖之後腳本沒再改過）。
