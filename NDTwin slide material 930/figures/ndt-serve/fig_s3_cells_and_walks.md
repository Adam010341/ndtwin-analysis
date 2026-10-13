# fig_s3_cells_and_walks —— 09-24 兩條逐步引導（walk）：修前紅、修好綠、現在重跑

[Co-developed with claude code -- Adam]

> 本檔所有日期時間都是 **UTC**（judge F-18）。raw 檔名（例如 `live-cells-20260924T2224`）與檔內的 `+08:00` 時間戳照原樣引用，旁邊註明換算。

## 一句話

「一格 live cell 帶著修前的紅（old/）與修好當晚的綠（new/）」這個**概念 9/16 已經報告過**（916 deck 第 7 頁 CELL「Freeze the evidence：pre-fix raw = old/, must FAIL forever」、「11 regression cells」）。
**9/16 之後新的**是：ndt serve 把格子開成 API，加上 **walk**（old → new →（lab 格才有的 status → claim）→ run →（release）→ compare → 由人判定），
以及 **09-24 14:25Z 在真 lab 上走完的兩條 walk**：`help_drops_deleted_claims`（不用 lab）4 條紅轉綠；
`up_target_names_a_readable_model`（OVS 4 台）8 條紅轉綠，其中**真正帶著缺陷的是 4 條，另 4 條是 fixture gap**。兩格重跑都是 `CELL: PASS`、still_red 為空。

## 資料來源

| 用途 | 檔（path:line 或 JSON key） | commit／binary |
|---|---|---|
| READ：walk 的步驟 | `tools/ndt_serve/cells.py:305-309` `guided_steps`（lab 格才加 `status`、`claim`、`release`）；步驟標題 `cells.py:293-302` `STEP_TITLES` | trunk `fed37cff`／`3d740be0`，`tools/ndt_serve` ＝ `f186ce98` |
| READ：claim 的分鐘數（只在 .md） | `tools/ndt_serve/serve.py:956`（walk 的 claim 步驟 `{"minutes": 30, …}`） | 同上 |
| READ：lab 在 compare 之前就還 | `cells.py:285-287` 的註解；`940c1233`（09-24 14:24Z）改的順序 | 同上 |
| READ：old／new／run／walk 四個詞的意思 | `scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926/RULINGS-0927-ndtserve-gui-v2.md:15-18`（Adam 09-27 的回饋第 8 點） | 裁定檔，scratch，未提交 |
| READ：格子只能是 grid 自己列的 | `cells.py:12-16`；`tools/test_workflow/live_cells/run_cells.sh --list` 列出 11 格 | 同上 |
| 9/16 已報告過的概念 | `/home/adam/Desktop/NDTwin slide material/NDTWIN slide material 916/NDTwin_deck_916.pdf` 第 7 頁（CELL 框） | 916 deck |
| OBSERVED：兩條 walk 的每一步 | `scratch/overnight-2026-09-05/logs/ndt-serve-0924/live-cells-20260924T2224/walk-help_drops_deleted_claims/12-GET-api_v1_guided_g20260924T142509Z-dd4f41.json`、`walk-up_target_names_a_readable_model/46-GET-api_v1_guided_g20260924T142521Z-ad027d.json`（各自最後一次 GET；JSON key `walk.steps[].result`：old/new 的 `judge.asserts`、`compare.rows`、`run.cell_verdict`） | serve 碼 `940c1233`（`live-cells-20260924T2224/00-before.txt:2`）；ndt sha256 `cb134ccc…`（`:3`）＝ CELL 行的 `ndt=3273df8b…`（git blob，＝trunk `fd7382a3` 的 ndt）；kernel sha16 `be70b5dd32356847`（CELL 行） |
| OBSERVED：每列的日期 | 各 `CELL:` 行的 `at=`，腳本換成 UTC：old（help）`at=(replayed 2026-09-11)` 沒有時刻，取 PROVENANCE「run 2026-09-11 13:0x」(+08) ＝ 09-11 05:0xZ；old（up_target）`2026-09-11T02:55:10+08:00` ＝ **09-10 18:55:10Z**（所以圖上是 09-10）；new `2026-09-11T13:33:03+08:00`／`13:34:05+08:00` ＝ 09-11 05:33Z／05:34Z；run `2026-09-24T22:25:10+08:00`／`22:25:24+08:00` ＝ 09-24 14:25Z | 同上 |
| OBSERVED：fixture gap 是哪幾條 | 同一 JSON 的 `steps[old].result.judge.provenance`（＝`tests/fixtures/live_cells/up_target_names_a_readable_model/old/PROVENANCE.md` 的全文）：「Assertions that carry the finding」4 條、「Fixture gap」4 條 | 同上 |
| OBSERVED：判定（只在 .md，不上圖） | `scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926/walks/g20260924T142509Z-dd4f41.json`、`…/g20260924T142521Z-ad027d.json`：`verdict.verdict = green`，`verdict.at` ＝ 2026-09-26 00:01:39Z 與 00:03:08Z，note `4 red->green, 0 still red`／`8 red->green, 0 still red` | 走 walk 的伺服器（同一份 walk 檔） |
| OBSERVED：lab 格還原乾淨 | `live-cells-20260924T2224/raw-up_target_names_a_readable_model/2026-09-24/_restore-…/3-down.rc`＝0、`4-clean.rc`＝0、`6-verdict-postclean.txt` `VERDICT: CLEAN`（只查行程那一半；網路那一半在 down 前的 `2-verdict-predown.txt` 查過，當時 flow table 空、沒有鑑別力，見 `doc/audit/2026-09-24_ndt-serve/REPORT-cells.md:138-139`） | 同上 |

- **髒的 checkout（judge F-16）**：walk 驅動的 ndt 是主 checkout `fd7382a3`＋**60 個檔有未提交的修改**，其中 2 個可改變行為
  （`p4_proxy/mininet/host_count_override`＝未提交的 `4`、`tools/remote-lab/dorm_lab/`）。出處：`walk-up_target…/46-GET…json` 的 status 步驟 `stdout`（檔內第 236 行起）；
  腳本解析並印出。ndt 這個檔本身未改（sha256 等於 `fd7382a3` 的 blob）。ndt serve 的 worktree（`940c1233`）是否乾淨，`00-before.txt` 沒記。
- 腳本斷言：兩條 walk 的步驟清單等於 `cells.py` 的 `guided_steps`（不用 lab 那格 5 步、lab 格 8 步）；停在 verdict；
  old/new/compare 三處斷言的 id 一致；old 的失敗集合等於 `expected_fails`；compare 的 `red_to_green` 等於逐列比對、`still_red` 為空、
  run 是 `finished`／rc 0／`CELL: PASS`；fixture gap ＝ old 的紅減去 PROVENANCE 點名的「carry the finding」，且等於 PROVENANCE「Fixture gap」段列的那幾條；
  「red → green」印成「真正的條數 (+fixture gap 條數)」；兩條 walk 的 ndt blob 相同；判定檔的 id 與 walk 相同；日期一律換成 UTC。
- 紅燈檢查：拿掉判定、把 PROVENANCE 改成多點名一條、replay 日期沒有時刻，腳本都會停。log 與驅動：
  `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/ndt-serve-s2s4-red-checks.{log,py}`（09-27 17:04:54Z；scratch，未提交）。

## 可信度

**OBSERVED（09-24 14:25Z 真 lab，經 ndt serve API；未提交的 raw；ndt 所在 checkout 髒 +60 file(s)，見上）**
- `help_drops_deleted_claims`（requires none）：6 條斷言；old（09-11 replay）4 FAIL／2 ok，`CELL: FAIL`；new（09-11）6 ok，`CELL: PASS`；
  run（09-24）6 ok，`CELL: PASS`；紅轉綠 4、still_red 0。
- `up_target_names_a_readable_model`（requires ovs4）：9 條斷言；old（09-10 18:55Z，P4 arm 抓的 log）8 FAIL／1 ok，其中
  **4 條是 fixture gap**（那一輪沒留 `up.target`，斷言讀不到檔才紅，不是缺陷證據），4 條才是真正的缺陷；new（09-11）9 ok；
  run（09-24）9 ok，`CELL: PASS`；紅轉綠 4（+4 fixture gap）、still_red 0；status／claim／release 三步 rc 都是 0；還原 down 0、clean 0、`VERDICT: CLEAN`。
- 兩條 walk 的判定都記為 green，時間 09-26 00:01Z／00:03Z（**依 judge F-12 不上圖**，只放在這裡）。
- 09-24 同一輪經 API 判 11 格的 old/ 與 new/：11 格 old 全 FAIL 且等於 EXPECTED-FAILS、11 格 new 全 PASS（`live-cells-20260924T2224/offline/`；REPORT-cells.md:56）——**那是重判存檔，不是重跑**，本圖沒畫。

**READ（讀碼，未執行）**
- walk 的步驟與順序、lab 格多出的三步、claim 30 分鐘、release 在 compare 之前（`cells.py:285-309`、`serve.py:956`）。
- old／new／run／walk 的定義（RULINGS v2:15-18）。
- 格子清單＝grid 自己的 `run_cells.sh --list`（11 格：3 格 none、6 格 ovs4、2 格 idle）。我在 09-27 15:4xZ 執行過一次 `--list`（它只列清單、不碰 lab，腳本頭註 `run_cells.sh:13`）。

**INFERRED（推論，未驗證）**
- 判定是 Adam 本人按的：walk 檔只記 `requested_by 127.0.0.1:…`，不記是誰；「Adam 09-26 判綠」出自合併訊息 `48209682`（「walks judged green by Adam 09-26」），不是 raw。

## 圖怎麼讀

- 上方一條細帶 **READ THE CODE**：一條 walk 的八個步驟名稱。實線框＝每一格都有；虛線框＝只有需要 lab 的格才有（status、claim、release）。
  （概念 9/16 講過，這裡只留步驟名，讓下方的 walk 對得上。）
- 下方主體 **RAN IT · dates UTC**：左右各一格。每一列是一份紀錄（old＝修前存檔、new＝修好當晚存檔、run＝09-24 重跑），
  **一個方塊＝一條斷言**，同一欄是同一條斷言。綠＝ok、紅＝FAIL、斜線紅框＝FAIL 但只是 fixture gap。
  列尾是該份紀錄 `CELL:` 行的判決原文（值，不是評語）；下方「red → green」是 compare 算出的條數，fixture gap 另外括號標出。
- 日期：old／new 是 09-10／09-11 的存檔（**早於 09-16，只當背景**）；09-24 的 run 是本期的新東西。

## 已知但書

- `up_target_names_a_readable_model` 的 old 是 **P4 arm** 的 log，而這一格驅動的是 **OVS**（PROVENANCE：OVS arm 當時沒有 rc 可用；
  缺陷是 `ndt:1948`（p4）與 `ndt:2287`（ovs）兩份一樣的三行，兩邊都離線證過）。所以「old 紅 → run 綠」是跨平面的對照。
- walk 的 GET 在 09-24 還不帶 token（REPORT-cells.md:164「cells 的 GET 要 token：沒有 live 證據」）；今天的碼每個 GET 都要 token。
- `requires idle` 的兩格（`up_refuses_*`）沒有用 walk 在 live 跑過（REPORT-cells.md:33）。
- 09-27 GUI 第一刀讓頁面可以點 walk，但**那一刀沒有動 lab**；瀏覽器實測是對 stub 伺服器與 `offline_cell` 這個 stub 格（`scratch/overnight-2026-09-05/logs/ndt-serve-gui-0927/browser-pane-walkthrough/WALKTHROUGH.md` B6）。
- 對帳舊結果：REPORT-cells.md:57（「no-lab 那格 4 條紅轉綠；ovs4 那格 8 條紅轉綠、still_red 為空、CELL: PASS、還原乾淨」）與本圖一致；
  本圖把 8 條拆成「4 條缺陷＋4 條 fixture gap」（依 PROVENANCE；judge F-12）。916 第 7 頁的「11 regression cells」與今天 `--list` 的 11 格一致。
- 避免說法：不要說「11 格都在 lab 上重跑過」——live 重跑的只有這兩格；第二格不要只講「8 條紅轉綠」。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/ndt-serve"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_serve_s2_s4.py
```

最後產出：2026-09-27T19:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_serve_s2_s4.py` sha256 `2f79ae137d352705…`（產圖之後腳本沒再改過）。

修訂：2026-09-27 17:05Z（judge F-12：red → green 改成「4 (+4 fixture gap)」、walk 步驟縮成細帶、判定移出圖面、標題改成 walks；F-18 全改 UTC；F-20 red-check 移出 scratchpad；F-16 補髒 checkout 註記）。
