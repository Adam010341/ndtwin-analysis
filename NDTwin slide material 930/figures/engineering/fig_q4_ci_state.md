# fig_q4_ci_state —— CI 每次 run 的 L1 失敗組數，與四個 job 的結果（09-28 重新釘住）

[Co-developed with claude code -- Adam]

產出：`fig_q4_ci_state.{pdf,png,svg}` ＋ `_hires/fig_q4_ci_state.png`（畫布 13.33×6.4 in）。
產生器：`make_engineering_figs.py` 的 `fig_q4()`。**as of 2026-09-28 08:53 UTC · trunk `3368412d`**（圖左下）。

## 一句話

09-25 到 09-28 的 56 次 CI run（46 次有 GCC 的 raw log，10 次是只有公開 API 結果的 ndtwin-lab trunk run）：
L1 的失敗組數從 14 起步，兩次被推到 15、當天修回；09-27 的 b005bf50 降到 12；09-28 PR #11（CI L1 lane）降到 1；PR #12 起是 0（`L1 passed`）。
clang、TSan 從 PR #9（`18c83aba` 的修法）起通過；**四個 job 第一次全綠是 ndtwin-lab trunk 上 `8d622ea4` 的 run（09-28 01:26Z 起跑）**，PR #12 的兩個 run（01:38Z）是**第一個全綠的 PR**。
PR #12–#14、#16、#17 與 ndtwin-lab trunk 從 `8d622ea4` 到 `3368412d` 的 run，四個 job 全綠（每個 run 的最後一次）；不是每一次都綠——一個不穩定的 shell 檢查（`test_apps_residue.sh`：ndt 的 residue report 兩次讀鐘的跨秒競態）讓 Adam010341 trunk `f253ed08` 的一次、PR #15 五次 GCC 裡的三次變紅（重跑後綠；圖上是那兩個 run 外面的紅圈）。

## 資料來源

縮寫：R＝`/home/adam/Desktop/NDTwin-Kernel`；I＝`R/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926`；I25＝同層 `intake-0925`；
S＝`R/scratch/overnight-2026-09-05/logs/slides930`；NET＝本資料夾的 `_net/`（我以未認證 HTTPS 抓的公開 API 快照）。**I、I25、S 不在版控（未提交的觀測）。**

每一點：L1 組數＝raw log 裡唯一一行 `L1 FAILED (N problem group(s))`，或 `L1 passed:`（＝0）；commit＝log 的 fetch 行 `+<40 hex>:refs/remotes/…`，
09-28 起 push run 抓全部歷史、fetch 行沒有 sha，改讀 checkout 那行的 ref 與 `git log -1 --format=%H` 的下一行；repo＝`Syncing repository:`；時間＝log 第一個時戳（UTC）。
四個 job＝jobs 檔、公開 API 的 jobs 快照（NET/jobs_<run>.json），或 orchestrator 的 compare 記錄。
09-28 的 18 份 GCC log（PR #9–#17）是 orchestrator 以 API 抓的（log 下載要認證），原樣複製到 `S/ci-raw/`（`S/ci-raw/MANIFEST.txt`：檔名、job、run、sha256、原始路徑）；
腳本斷言每份 log 的 job id 就是該 run 在公開 API 裡的 GCC job。一個 run 重跑過時，畫的是它最後一次 attempt（jobs 快照報的就是那一次）；較早的 attempt 的 GCC log 在 `S/ci-raw/earlier/ci-<run>-gcc.job<job>.attempt<k>.raw.log`（3 份，都是 PR #15），腳本讀它們的 L1 行、斷言 commit 與畫的那一點相同、attempt 早於 jobs 快照的 attempt；有紅的較早 attempt 就在那一點外畫紅圈。job 與 run、attempt 的對應：未認證的 `actions/jobs/<id>`，存在 `S/ci-raw/api-20260928/`。表中 PR #15 的分支名不寫。

| 開始（UTC） | run | repo | ref | commit | L1 | L1 行 | jobs（GCC,clang,TSan,ASan） | jobs 來源 |
|---|---|---|---|---|---|---|---|---|
| 2026-09-25 09:49 | 36120567778 | ndtwin-lab | trunk | a4c951a8 | 14 | I25/ci-36120567778-gcc.log:6875 | no record | — |
| 2026-09-25 10:53 | 36126428688 | ndtwin-lab | trunk | 377a1271 | 15 | I25/ci-36126428688-gcc.log:6878 | f,f,f,s | I25/ci-36126428688.jobs.txt |
| 2026-09-25 11:59 | 36132382437 | ndtwin-lab | trunk | 680c5293 | 15 | I25/ci-36132382437-gcc.log:6878 | f,f,f,s | I25/ci-36132382437.jobs.txt |
| 2026-09-25 12:24 | 36134766761 | ndtwin-lab | trunk | 68ace017 | 15 | I25/ci-36134766761-gcc.log:6879 | f,f,f,s | I25/ci-36134766761.jobs.txt |
| 2026-09-25 21:04 | 36189445756 | ndtwin-lab | trunk | dd7e2fcf | 14 | I/ci-36189445756-gcc.raw.log:6877 | f,f,f,s | I/ci-36189445756.jobs.txt |
| 2026-09-26 00:06 | 36203510814 | ndtwin-lab | trunk | 14554090 | 14 | I/ci-36203510814-gcc.raw.log:6877 | f,f,f,s | I/ci-36203510814.jobs.txt |
| 2026-09-26 01:06 | 36207272058 | ndtwin-lab | trunk | dfbab30e | 14 | I/ci-36207272058-gcc.raw.log:6879 | f,f,f,s | I/ci-36207272058.jobs.txt |
| 2026-09-26 02:27 | 36211755454 | ndtwin-lab | trunk | 4bc1201b | 14 | I/ci-36211755454-gcc.raw.log:6879 | f,f,f,s | I/ci-36211755454.jobs.txt |
| 2026-09-26 05:21 | 36220555111 | ndtwin-lab | trunk | 580767a8 | 14 | I/ci-36220555111-gcc.raw.log:6879 | f,f,f,s | I/ci-36220555111.jobs.txt |
| 2026-09-26 06:43 | 36224592516 | ndtwin-lab | trunk | 318e6391 | 14 | I/ci-36224592516-gcc.raw.log:6878 | f,f,f,s | I/ci-36224592516.jobs.txt |
| 2026-09-26 08:49 | 36230955530 | ndtwin-lab | trunk | 094f417f | 14 | I/ci-36230955530-gcc.raw.log:6879 | f,f,f,s | I/ci-36230955530.jobs.txt |
| 2026-09-26 09:39 | 36233414349 | ndtwin-lab | trunk | 9c2e59e4 | 14 | I/ci-36233414349-gcc.raw.log:6879 | f,f,f,s | I/ci-36233414349.jobs.txt |
| 2026-09-26 15:25 | 36251857977 | ndtwin-lab | trunk | cafd518a | 15 | I/ci-36251857977-gcc.raw.log:6888 | f,f,f,s | I/ci-compare-cafd518a.txt |
| 2026-09-26 17:29 | 36259179041 | ndtwin-lab | trunk | 3f8c2abf | 14 | I/ci-36259179041-gcc.raw.log:6885 | no record | — |
| 2026-09-26 19:44 | 36267068730 | ndtwin-lab | trunk | b2eeb71d | 14 | I/ci-36267068730-gcc.raw.log:6885 | f,f,f,s | I/ci-36267068730.jobs.txt |
| 2026-09-26 21:39 | 36273687560 | ndtwin-lab | trunk | 3db3b9a8 | 14 | I/ci-36273687560-gcc.raw.log:6885 | f,f,f,s | I/ci-36273687560.jobs.txt |
| 2026-09-26 22:47 | 36277412804 | ndtwin-lab | trunk | 8746c1bc | 14 | I/ci-36277412804-gcc.raw.log:6885 | f,f,f,s | I/ci-36277412804.jobs.txt |
| 2026-09-26 23:25 | 36279411773 | ndtwin-lab | trunk | c34a643a | 14 | I/ci-36279411773-gcc.raw.log:6885 | f,f,f,s | I/ci-36279411773.jobs.txt |
| 2026-09-27 05:12 | 36296537822 | ndtwin-lab | trunk | b005bf50 | 12 | I/ci-36296537822-gcc.raw.log:6871 | f,f,f,s | I/ci-36296537822.jobs.txt |
| 2026-09-27 07:38 | 36303713298 | ndtwin-lab | main | d9308f61 | 12 | I/ci-36303713298-gcc.raw.log:6871 | f,f,f,s | I/ci-36303713298.jobs.txt |
| 2026-09-27 08:19 | 36305829213 | ndtwin-lab | trunk | 7746832e | 12 | I/ci-36305829213-gcc.raw.log:6900 | f,f,f,s | I/ci-36305829213.jobs.txt |
| 2026-09-27 12:36 | 36319541715 | ndtwin-lab | trunk | f186ce98 | 12 | I/ci-36319541715-gcc.raw.log:6901 | f,f,f,s | I/ci-36319541715-jobs.txt |
| 2026-09-27 15:24 | 36329444138 | ndtwin-lab | trunk | 3d740be0 | no log | — | f,f,f,s | _net/jobs_36329444138.json |
| 2026-09-27 15:25 | 36329482388 | Adam010341 | pr/shell-test-scoring | 48e8005d | 12 | I/ci-36329482388-gcc.raw.log:6884 | f,f,f,s | I/ci-compare-pr6-48e8005d.txt |
| 2026-09-27 15:25 | 36329490324 | Adam010341 | pull/6/merge | 03eff86a | 12 | I/ci-36329490324-gcc.raw.log:6900 | f,f,f,s | I/ci-compare-pr6-48e8005d.txt |
| 2026-09-27 15:45 | 36330744945 | Adam010341 | pr/claude-md-rules | a5bfd282 | 12 | I/ci-36330744945-gcc.raw.log:6884 | f,f,f,s | I/ci-compare-pr7.txt |
| 2026-09-27 15:45 | 36330754284 | Adam010341 | pull/7/merge | b9c27c4e | 12 | I/ci-36330754284-gcc.raw.log:6900 | f,f,f,s | I/ci-compare-pr7.txt |
| 2026-09-27 15:52 | 36331119197 | ndtwin-lab | trunk | fed37cff | no log | — | f,f,f,s | _net/jobs_36331119197.json |
| 2026-09-27 15:52 | 36331169426 | Adam010341 | pr/ndt-serve-claim-note | ef3aec3f | 12 | I/ci-36331169426-gcc.raw.log:6884 | f,f,f,s | I/ci-compare-pr8.txt |
| 2026-09-27 15:52 | 36331172122 | Adam010341 | pull/8/merge | fc63ab9d | 12 | I/ci-36331172122-gcc.raw.log:6900 | f,f,f,s | I/ci-compare-pr8.txt |
| 2026-09-27 19:04 | 36343017674 | Adam010341 | pr/ci-clang-tsan | d411e852 | 12 | S/ci-raw/ci-36343017674-gcc.job108686655193.raw.log:6895 | f,s,s,s | _net/jobs_36343017674.json |
| 2026-09-27 19:04 | 36343021331 | Adam010341 | pull/9/merge | c297ebb9 | 12 | S/ci-raw/ci-36343021331-gcc.job108686665505.raw.log:6911 | f,s,s,s | _net/jobs_36343021331.json |
| 2026-09-27 19:25 | 36344296725 | ndtwin-lab | trunk | 18c83aba | no log | — | f,s,s,s | _net/jobs_36344296725.json |
| 2026-09-27 22:34 | 36355763084 | ndtwin-lab | trunk | 149c8234 | no log | — | f,s,s,s | _net/jobs_36355763084.json |
| 2026-09-27 22:35 | 36355835109 | Adam010341 | pr/heartbeat-rulings | 0c08673e | 12 | S/ci-raw/ci-36355835109-gcc.job108723254765.raw.log:6895 | f,s,s,s | _net/jobs_36355835109.json |
| 2026-09-27 22:35 | 36355837441 | Adam010341 | pull/10/merge | 2b716974 | 12 | S/ci-raw/ci-36355837441-gcc.job108723262152.raw.log:6911 | f,s,s,s | _net/jobs_36355837441.json |
| 2026-09-28 00:05 | 36360889642 | ndtwin-lab | trunk | 9ef10250 | no log | — | f,s,s,s | _net/jobs_36360889642.json |
| 2026-09-28 00:16 | 36361624221 | Adam010341 | pr/ci-l1-lane | d4b96ea6 | 1 | S/ci-raw/ci-36361624221-gcc.job108739781529.raw.log:6982 | f,s,s,s | _net/jobs_36361624221.json |
| 2026-09-28 00:17 | 36361627323 | Adam010341 | pull/11/merge | ef6447dc | 1 | S/ci-raw/ci-36361627323-gcc.job108739789903.raw.log:6995 | f,s,s,s | _net/jobs_36361627323.json |
| 2026-09-28 01:26 | 36365963530 | ndtwin-lab | trunk | 8d622ea4 | no log | — | s,s,s,s | _net/jobs_36365963530.json |
| 2026-09-28 01:38 | 36366735218 | Adam010341 | pr/round-env-kernel-dir | fcb9664a | 0 | S/ci-raw/ci-36366735218-gcc.job108754530931.raw.log:6984 | s,s,s,s | _net/jobs_36366735218.json |
| 2026-09-28 01:38 | 36366738972 | Adam010341 | pull/12/merge | 0cbf7ea0 | 0 | S/ci-raw/ci-36366738972-gcc.job108754542107.raw.log:6997 | s,s,s,s | _net/jobs_36366738972.json |
| 2026-09-28 03:17 | 36373156511 | ndtwin-lab | trunk | f253ed08 | no log | — | s,s,s,s | _net/jobs_36373156511.json |
| 2026-09-28 03:18 | 36373185198 | Adam010341 | pr/sudo-probe | 27766535 | 0 | S/ci-raw/ci-36373185198-gcc.job108773555456.raw.log:6985 | s,s,s,s | _net/jobs_36373185198.json |
| 2026-09-28 03:18 | 36373189008 | Adam010341 | pull/13/merge | 421cfa20 | 0 | S/ci-raw/ci-36373189008-gcc.job108773566953.raw.log:6998 | s,s,s,s | _net/jobs_36373189008.json |
| 2026-09-28 03:41 | 36374700365 | ndtwin-lab | trunk | 85bec430 | no log | — | s,s,s,s | _net/jobs_36374700365.json |
| 2026-09-28 03:50 | 36375270576 | Adam010341 | pr/kernel-capabilities | ec8eb33a | 0 | S/ci-raw/ci-36375270576-gcc.job108779709337.raw.log:7066 | s,s,s,s | _net/jobs_36375270576.json |
| 2026-09-28 03:50 | 36375273810 | Adam010341 | pull/14/merge | 13ed700e | 0 | S/ci-raw/ci-36375273810-gcc.job108779718176.raw.log:7079 | s,s,s,s | _net/jobs_36375273810.json |
| 2026-09-28 06:57 | 36389041749 | ndtwin-lab | trunk | fc25112e | no log | — | s,s,s,s | _net/jobs_36389041749.json |
| 2026-09-28 07:21 | 36389126411 | Adam010341 | pull/15/merge | dbcf45a8 | 0（較早 #1: 1） | S/ci-raw/ci-36389126411-gcc.job108827321891.raw.log:7080 | s,s,s,s | _net/jobs_36389126411.json |
| 2026-09-28 07:55 | 36394350905 | ndtwin-lab | trunk | 3368412d | no log | — | s,s,s,s | _net/jobs_36394350905.json |
| 2026-09-28 07:56 | 36394430416 | Adam010341 | pr/suite-term-trap | 1e1c26ee | 0 | S/ci-raw/ci-36394430416-gcc.job108837361889.raw.log:7068 | s,s,s,s | _net/jobs_36394430416.json |
| 2026-09-28 07:56 | 36394435398 | Adam010341 | pull/16/merge | a7dd4e89 | 0 | S/ci-raw/ci-36394435398-gcc.job108837379659.raw.log:7081 | s,s,s,s | _net/jobs_36394435398.json |
| 2026-09-28 08:05 | 36389119721 | Adam010341 | （PR #15 的分支） | 47b8fb9c | 0（較早 #1: 1、#2: 1） | S/ci-raw/ci-36389119721-gcc.job108839888617.raw.log:7068 | s,s,s,s | _net/jobs_36389119721.json |
| 2026-09-28 08:29 | 36397644292 | Adam010341 | pr/claude-md-lab-sync | 2e1aef4c | 0 | S/ci-raw/ci-36397644292-gcc.job108847738971.raw.log:7069 | s,s,s,s | _net/jobs_36397644292.json |
| 2026-09-28 08:29 | 36397654628 | Adam010341 | pull/17/merge | a788b406 | 0 | S/ci-raw/ci-36397654628-gcc.job108847775441.raw.log:7082 | s,s,s,s | _net/jobs_36397654628.json |

（f＝failure、s＝success、no record＝沒有 job 紀錄；「較早 #k: n」＝第 k 次 attempt 的 L1 組數。所有時間 UTC。窗口：log 開始時間 < 2026-09-28T08:53:00Z；ndtwin-lab trunk 上 09-27 15:00Z 起沒有 log 的 CI run 由 API 補上、畫一條短豎線。）

公開 API 快照（我自己，未認證；每一次請求的時間、URL、HTTP 碼、位元組與 sha256 逐行在 `S/net-refresh-20260928T0616Z.log`；腳本 `S/net_get.py`，不帶任何 token）：
- 2026-09-28T06:16:27–06:16:55Z：四條 branches、`pulls?state=all&per_page=30`、兩個 repo 的 `actions/runs`；06:17:28–06:17:46Z：20 個 run 的 `actions/runs/<id>/jobs`。
- 2026-09-28T06:45:52–06:45:55Z：四條 branches 與 `ndtwin-lab/…/actions/runs?per_page=30` 再抓一次（ndtwin-lab main 已快轉到 `be01cc7a`，trunk 仍是 `85bec430`）；06:16Z 的那份留在 NET/prev-20260928T0616Z/。
- 2026-09-28T08:31:56–08:32:31Z（重新釘住，`S/net-repin-20260928T0831Z.log`）：四條 branches、pulls、兩個 repo 的 `actions/runs`（兩次 000 已重試）；08:32:48–08:32:51Z：6 個新 run 的 jobs；08:33Z：7 個 GCC job 的 `actions/jobs/<id>`。06:45Z 的那份留在 NET/prev-20260928T0645Z/。
- 2026-09-28T08:53:29–08:53:33Z（PR #17 併入之後，`S/net-repin2-20260928T0853Z.log`）：四條 branches、pulls、兩個 repo 的 `actions/runs`；08:55:59Z：PR #17 兩個 run 的 jobs；08:56Z：兩個 GCC job 的 `actions/jobs/<id>`。08:32Z 的那份留在 NET/prev-20260928T0832Z/。
- 09-27 的快照留在 NET/prev-20260927T1553Z／1608Z／1615Z／1702Z/。

## 可信度

**OBSERVED（CI 實際跑過；raw log、jobs 檔、公開 API）**
- 表中每一個 L1 組數、commit、repo、job 結果。
- 09-27 以前有記錄的 run：GCC、clang、TSan 失敗，ASan＋UBSan 通過；PR #9–#11 與 ndtwin-lab trunk `18c83aba`、`149c8234`、`9ef10250`：只剩 GCC 失敗（L1）；`8d622ea4` 之後：四個 job 全綠。
- 2 次（a4c951a8、3f8c2abf）沒有 job 記錄，畫成白格。
- orchestrator 的 compare 記錄（I/ci-compare-pr9.txt … pr17.txt）第一行寫的結果與公開 API 相同；pr12–pr14、pr16、pr17 寫「all four jobs SUCCESS」（pr17 的第一行寫 PR 的 head、不寫 run id：腳本改成由 PR 編號找它畫出的 run，並斷言其中一個在那個 head 上），腳本逐一核對 API；pr15 的第一行寫的是第一次 attempt（GCC 兩個都紅），畫的是最後一次 attempt（綠），紅的那幾次畫成紅圈。
- PR #15：兩個 run 的 GCC 五次 attempt 裡三次紅（L1 1 組：`test_apps_residue.sh`），重跑後綠（`S/ci-raw/earlier/` 的 3 份 log）。

**READ（讀 compare 記錄與 commit 訊息，未執行）**
- 14→15 的兩次：377a1271（心跳段 H）→ dd7e2fcf 修回；cafd518a（心跳段 W）→ 329dc555 修回（I/ci-compare-cafd518a.txt:11）。
- 14→12：b005bf50（probe stubs＋stale suites），I/ci-compare-b005bf50.txt:2。
- PR #15 的紅：原因是 ndt 的 residue report 兩次讀鐘之間跨秒（`I/ci-compare-pr15.txt:9-11`，coordinator 轉來的量測；與這個 PR 的改動無關）；修法在 `fix/residue-live-pid-wait-0928`（F1 的在審那一格）。
- 12→1：PR #11＝CI L1 lane（`9ef10250`）：宣告過的「需要 lab」在 hosted runner 上免除；剩下的 1 組是 test_cell_gate_suspect_wiring（I/ci-compare-pr11.txt:2-3）。1→0：PR #12＝round.env（`8d622ea4`）。

**INFERRED**
- 無。

## 圖怎麼讀

- 上：每個點＝一次 CI run 的 L1 失敗組數（0＝`L1 passed`）；圓＝ndtwin-lab trunk、空心方＝main、橘三角＝PR（Adam010341）。只在數字改變的地方標名字：trunk／main 的點標 commit，PR 的點標「PR #N」（N 從 PR 的分支對 pulls 快照查，查不到就停）。短豎線＝這次 run 只有 API 結果、沒有 GCC log，所以沒有 L1 數；圖例「no log」只寫一次。 紅圈＝這個 run 較早的 attempt 是紅的（重跑後綠），圖例「red on an earlier attempt」。
- 下：同一次 run 的四個 job；紅＝failure、綠＝success、白＝沒有記錄。
- 虛線分日（UTC）。

## 已知但書

- 本地只有 09-25 以後的 CI log；09-16～09-24 的 run 不在圖上（不是沒跑）。
- 圖只畫 ndtwin-lab trunk 的 run 與 PR 的 run；Adam010341 自己的 trunk／main push run 不畫。其中 Adam010341 trunk `f253ed08` 那一次（run 36373153486）GCC 失敗，而同一個 commit 在 ndtwin-lab 通過；coordinator 查到的原因是不穩定的 `test_apps_residue.sh`（那份 log 要認證，我沒讀；同一個檢查也弄紅 PR #15 的三次 attempt，那三份 log 我讀了）。
- 狀態釘在 trunk `3368412d`、main `eef173a9`（08:53Z 的公開 API）；之後的 CI run 不在這張圖上。
- 36303713298 是 main 上的 run（當時 main 與 trunk 同步推，同一個 commit 各跑一次，只存了 main 那份）。
- PR run 的 commit 是 PR 分支或 GitHub 的 pull/N/merge，不是 trunk。
- 說「第一個全綠的 PR 是 #12」；要講最早的全綠 run，是 ndtwin-lab trunk `8d622ea4`（09-28 01:26Z）。不要說「09-28 起一直全綠」；有界的講法見一句話。

## 重生指令

```
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/engineering"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_engineering_figs.py
```
下一次更新：重抓 NET/（`S/net_get.py`，URL 同上）、把新的 GCC log 放進 `S/ci-raw/`、改 `make_engineering_figs.py` 的 `STATE`／`STATE_AT`。

最後產出：2026-09-28T08:58:27Z（PNG 檔時間，UTC；重新釘住到 main `eef173a9`）；matplotlib 3.11.1；產生器 `make_engineering_figs.py` sha256 `a0f7cc8a4d1cb252…`（STATE＝trunk `3368412d`、公開 API 快照 08:53Z；PR #15、#16、#17 的 run 與 fc25112e、3368412d 的 trunk run 進圖；較早 attempt 的紅圈；重生紀錄 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-repin2-20260928T0858Z.log`，rc 0）。紅檢：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_engineering_figs-redcheck-20260928T0857Z.log`（133 個停止點：130 個看過紅、3 個到不了；181 個竄改 181/181；對照組 4/4；harness 自檢 4/4）。之前：08:48:36Z（`8959a132…`，08:32Z 的快照，PNG `e776f09cf0e32b11`）與 08:10:40Z（`6f26e0ad…`，PNG `b83fffcb53bc27a8`），都已被取代。
