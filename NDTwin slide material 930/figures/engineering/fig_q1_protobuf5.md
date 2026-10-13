# fig_q1_protobuf5 —— P4 proxy 的 protobuf 從 3.20.3 換到 5.29.6，每一步過了什麼檢查

[Co-developed with claude code -- Adam]

產出：`fig_q1_protobuf5.{pdf,png,svg}` ＋ `_hires/fig_q1_protobuf5.png`（畫布 13.33×5.5 in；PNG 300 dpi、hires 500 dpi）。
產生器：`make_engineering_figs.py` 的 `fig_q1()`。

## 一句話

09-25 先讓 `p4_proxy/requirements.txt` 描述實際在用的 venv（p4runtime 1.5.0、grpcio 1.82.1，protobuf 仍 3.20.3）；
09-26 在另建的候選 venv 上 live 試跑；09-27 併入 protobuf 5.29.6（多了 grpcio-tools 與 regen 工具），
同一天把開發機的 venv 遷過去、live 驗收、再對 CI——每一步的檢查結果都由腳本從 raw 讀出。**圖上沒有任何效能數字（刻意）。**

## 資料來源

縮寫：R＝`/home/adam/Desktop/NDTwin-Kernel`；I＝`R/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926`；
I25＝同層的 `intake-0925`；RUNS＝`R/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs`；
ARMS＝`R/doc/audit/2026-09-04_p4-tutorial-exercise-prep/runs`。
**I、I25、RUNS、ARMS 底下全部不在版控（未提交的觀測）**；requirements 與 commit 本身在 trunk（已提交）。

| 用途 | 檔（path:line 或欄位） | commit／binary |
|---|---|---|
| 上方版本條；p4runtime 1.4.1→1.5.0、grpcio `>=1.50.0`→`==1.82.1`、grpcio-tools 1.71.2 | `git show c0602510:p4_proxy/requirements.txt`:6,14,15；`git show a4c951a8:…`:30,46,47；`git show 5dc7fc9a:…`:81,97,98,111；`git show 3d740be0:…`:79,95,96,109（腳本斷言四個時點的值） | c0602510＝a4c951a8^1；a4c951a8、5dc7fc9a 為 trunk 上的 merge |
| 格內日期（UTC） | a4c951a8、5dc7fc9a 的 committer date；JOURNAL.txt:1、migrate.log:1、live-accept.log:1 的時戳；ci-36305829213-gcc.raw.log 的第一個時戳——腳本全部換成 UTC 再取月-日（09-25、09-26、09-27×4） | — |
| 「+ regen tool」 | `git cat-file -e 3d740be0:p4_proxy/regen_p4runtime_pb2.py` 成立；在 a4c951a8 不存在 | 已提交 |
| 09-25「1557 + 187 tests」 | I25/rerun-REQ-851cefd7.summary.log:1-2（`aligned2`＝依新檔建的 fresh venv、`mainvenv`＝主 venv；兩者皆 p4_proxy `Ran 1557 tests … OK (skipped=1)`、p4_exercise `Ran 187 tests … OK`） | 851cefd7＝a4c951a8^2 |
| 09-26「01: rc 0」 | I/pb5-trial/JOURNAL.txt:4-5（phase2：01 on venv-cand，`end rc=0`）；I/pb5-trial/01cand.out:77 `PASS 01_baseline`；RUNS/2026-09-26T055003Z_01_baseline/22_status.txt:9 `code 580767a8` | code 580767a8；候選 venv：I/pb5-trial/dists_cand.txt:17 `protobuf==5.29.6`（主 venv dists_main.txt:16 `protobuf==3.20.3`） |
| 09-26「06: 26/26 arms」 | JOURNAL.txt:6-7（phase3 `rc=0`）；I/pb5-trial/06cand.out:145；RUNS/2026-09-26T055148Z_06_thirteen/00_table.tsv（26 列＝24 列 rc 0 `PASS`＋2 列 rc 1 `RED ARM … by design`）；那 24 份臂報告（ARMS/2026-09-26T05…–06…Z_*_ndtwin.md）的 `code 580767a8` 行 | 同上 |
| 09-27 merge；「gates 5/6」 | `git log -1 --format=%P 5dc7fc9a`＝d9308f61 ab026ef0；I/judge-PB5PREP-6351be15.md:5 `READY AFTER FIXES`、:24 與 :40 `READY FOR ADAM'S DECISION`；I/pb5-merge/rerun-summary.ac0c3b64.txt:1-6（6 項中 5 項 `rc=0`；`test_ndt_serve # rc=1 … FAILED (failures=1)`） | test merge ac0c3b64（依 5dc7fc9a 訊息，樹＝b0cd6731＝這個 merge 的樹），在 3.20.3 venv 上跑 |
| 09-27「1658 + 187 tests」「same as old venv」「4 descriptors same」 | I/pb5-merge/migrate.log:1（trunk 5dc7fc9a；old venv protobuf 3.20.3）、:25-28（舊 venv 基準 `Ran 1658 tests`／`OK (skipped=1)`／`Ran 187 tests`／`OK (skipped=1)`）、:30（舊 venv 停放）、:135-139（新 venv 已安裝的套件：4 個 `descriptor identical`）、:146 `VERIFIED: … passes what the old venv passed`；I/pb5-merge/inner-migrate.txt:21（3c 步：新 venv 跑同兩套，與基準 `diff` 為空才印 VERIFIED）；停放檔 `/home/adam/p4_proxy-venv.protobuf3.20.3-20260927-154343.new`（在時腳本比對＝1658／187）；I/pb5-merge/venv-after.freeze:17 `protobuf==5.29.6` | trunk 5dc7fc9a |
| 09-27「01: PASS」「06: 26/26 arms」 | I/pb5-merge/live-accept.log:1（`trunk 5dc7fc9a…; venv 5.29.6 upb`）、:3、:4、:6、:7、:13；RUNS/2026-09-27T074558Z_01_baseline/22_status.txt:9 `code 5dc7fc9a`；RUNS/2026-09-27T074635Z_06_thirteen/00_table.tsv（26 列＝24 PASS＋2 設計紅）；24 份臂報告的 `code 5dc7fc9a` 行 | code 5dc7fc9a＋遷移後的 venv |
| CI「L1: 12 groups」「lines identical」 | I/ci-36303713298-gcc.raw.log（d9308f61，main）:6624 安裝 `protobuf-3.20.3`、:6871 `L1 FAILED (12 problem group(s))`；I/ci-36305829213-gcc.raw.log（7746832e，trunk）:6544 `protobuf==5.29.6`、:6632 安裝、:6634-6637 與 :6648-6651 `descriptor identical`（共 8 行）、:6900 `L1 FAILED (12 …)`；兩份 `FAILED`/`FAIL:` 行去時戳後逐行相同（29 行，腳本自己比）；I/ci-prediction-7746832e.txt:1-2（run 完成前寫下）；I/ci-compare-7746832e.txt:4 `IDENTICAL -- prediction met` | GitHub Actions run 36303713298、36305829213（ndtwin-lab/NDTwin-Kernel-P4 的 GCC job） |

## 可信度

**OBSERVED（跑過、看 raw）**
- 09-25：兩套測試 1557＋187 在 fresh venv 與主 venv 都 OK。
- 09-26：候選 venv 上 01 跑 1 次 rc 0；06 的 26 臂全部照設計結束（24 PASS、2 個設計上該紅的 skeleton 臂）。
- 09-27 test merge：6 項閘門 5 項 rc 0，`test_ndt_serve` 1 個 failure。
- 09-27 遷移：新 venv 跑同兩套，輸出與舊 venv 的基準一字不差；4 個 descriptor 與 p4runtime 附的相同。
- 09-27 live 驗收：01 PASS、06 26/26（照設計）。
- CI：換版前（d9308f61）裝的是 3.20.3、換版後（7746832e）裝的是 5.29.6；兩次 L1 都是 12 組、29 行 FAILED 相同。**CI 兩次都是紅的**（GCC、clang、TSan 失敗）。
- 我以未認證 curl 抓的公開 API（見 fig_q5 .md 的指令）：`runs?per_page=5` 快照中有 `Graph Update: pip in /p4_proxy`（id 36305831255，head 7746832e，branch main，completed success，updated 2026-09-27T08:20:07Z）。
- I/push-7746832e.log:25：7746832e 推上去時 GitHub 仍回「2 vulnerabilities … (2 high)」；之後 I/push-f186ce98.log 沒有這一行。

**READ（讀過，未執行）**
- p4runtime 1.5.0 附的 generated modules 會被 protobuf ≥4.21 拒絕，所以安裝時要 regen（5dc7fc9a 的 commit 訊息；R/doc/audit/2026-09-25_p4proxy-requirements/TICKET-p4proxy-requirements.md:13）。
- 兩個 high alert 的編號：同 ticket :10-12（GHSA-8qvm-5x2c-j2w7／CVE-2025-4565；GHSA-7gcm-g887-7qv7／CVE-2026-0994）。
- test_ndt_serve 那一個紅：5dc7fc9a 訊息說是 TMPDIR 長度造成、這個分支沒碰那支測試；其後 fed37cff（`claim-note test independent of TMPDIR length`）修掉。

**轉述（協調者以 gh api、已認證查核，2026-09-27 UTC（原文寫 2026-09-28，+08）；我用未認證方式無法驗）**
- the two high protobuf alerts on the ndtwin-lab repo were closed as fixed on 09-27 08:20Z (checked by the coordinator with gh api, authenticated)。Adam010341 那份 repo 的 Dependabot alerts 是停用的。

**INFERRED（推論，未驗）**
- Graph Update 在 08:20:07Z 完成、alert 在 08:20Z 關閉，時間吻合：關閉是依賴圖更新後自動發生的。

## 圖怎麼讀

- 上方橫條＝repo 的 requirements 釘的版本：灰＝3.20.3，藍＝5.29.6。09-26 那格雖在灰條下，試跑用的是另建的候選 venv（格內寫明 5.29.6）。
- 六格＝時間順序的六步；藍框＝真正換版的那個 merge。
- 格下是**每一步一個結果格**（2026-09-27 UTC 第二輪，coordinator 第 13 項：原本一列列帶圓點的字讀起來像 bullet）；格頂的色條＝這一步的結果，格裡是那一步的檢查：綠＝過；黃＝部分（閘門 6 項 5 項過）；**紅＝CI 紅**——換版前後都是同樣的 12 組 L1 失敗、29 行相同（圖例寫「CI red (same 12 groups)」）。
- 格內日期是 UTC。
- 「26/26 arms」＝26 臂都照練習的設計結束，其中 2 臂（basic_tunnel、flowcache 的 skeleton）是設計上就該紅。

## 已知但書

- 09-26 試跑的候選 venv（5dc7fc9a 訊息稱 set A）與最後併入的集合（set C）不完全相同：候選 venv 是 starlette 1.7.0（I/pb5-trial/dists_diff.txt），併入的檔釘 starlette 1.3.1（`git show 5dc7fc9a:p4_proxy/requirements.txt`:118）。set C 只離線跑過，它的接受條件就是第 5 格（遷移後 live 01、06）。
- 5dc7fc9a 訊息寫試跑「01 x4」；JOURNAL 裡候選 venv 上的 01 只有 phase2 一次，另兩次在主 venv（phase1 控制組、phase6 還原檢查）。圖只寫候選 venv 那一次；「x4」的第四次指什麼我沒查到，不採用。
- 「1557 + 187」（09-25，較早的樹）與「1658 + 187」（09-27，5dc7fc9a）測試數不同是中間加了測試，不是退步；兩者不可相比。
- live-accept.log:12 記下 live 跑完後 venv 指紋變了（作者猜是 byte-code），未追查。
- 遷移步的「1658 + 187」其實是兩次：舊 venv 的基準（migrate.log:25-28）與新 venv 的結果（只以 diff 為空＋VERIFIED 表示；逐字輸出在 repo 外的停放檔 `.new`）。停放檔被刪後腳本只剩 VERIFIED 這條證據。
- 依 brief 規則 7：換版前後的效能數字不可放在同一張圖；這張圖一個效能數字也沒有。
- 對外不要說「CI 綠了」：換版前後 CI 都是紅的，這張圖只證明換版沒有改變它紅的方式。
- **兩次 live 都在 dirty checkout 上跑**（F-16）：09-26T055148Z 的 06 那 24 份臂報告都是 `code 580767a8  +83 file(s)`（01：RUNS/2026-09-26T055003Z_01_baseline/22_status.txt:9 `+81`）；09-27T074635Z 的 06 那 24 份都是 `code 5dc7fc9a  +95 file(s)`（01：RUNS/2026-09-27T074558Z_01_baseline/22_status.txt:9 `+93`）。圖上的 sha 是 HEAD，不是完整的樹。
- 09-27 的 raw（T06、01 baseline，連同 09-26 的 06）已提交到 audit-raw `797c34ab`（本地 `git ls-tree -r 797c34ab` 查得到那幾個 00_table.tsv／22_status.txt）；兩個 P4 repo 的 audit-raw 公開讀回見 I/push-audit-raw-797c34ab.log（orchestrator 以未認證 ls-remote 讀回 797c34ab），協調者也說兩邊都公開。我沒有另外打 URL 驗。

## 重生指令

```
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/engineering"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_engineering_figs.py
```

最後一次執行的輸出（含每份判官檔的判決、各圖的 `[q*]` 行）：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/engineering-figs-run-20260927T1705Z.log`（未提交）。

最後產出：2026-09-27T19:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；當時的產生器 `make_engineering_figs.py` sha256 `2c82ff1b8d151654…`。之後腳本改過兩輪、都只加停止條件、沒動畫法：紅檢修正輪（20:40Z：幾處沒有具名的解析失敗改成具名的停止條件、06／01 檢查逐項寫出原因、Q4 的 compare 記錄規則）與 API 欄位輪（20:52Z：API 快照在載入時就檢查圖要讀的每個欄位，`codes.txt` 每一行也檢查）；現在是 sha256 `3c44f472b1ac2292…`。用新腳本重跑，五張圖的 300 dpi 與 500 dpi PNG 都與現有檔**逐位元相同**，所以沒有重新產圖（`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-check-fixround-20260927T2054Z.log`）。紅檢：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_engineering_figs-redcheck-20260927T2053Z.log`（118 個停止點：115 個看過紅、3 個任何輸入都到不了；162 個竄改 162/162；對照組 3/3）。09-28 更新（Q4／Q5 的狀態刷新）：產生器又改一次，現在是 sha256 `468618f94882bff4…`；這張圖的 300 dpi 與 500 dpi PNG 重跑後與現有檔**逐位元相同**（`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-refresh-20260928T0658Z.log`、`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-check-all-*.log`），沒有重新產圖。紅檢 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_engineering_figs-redcheck-20260928T0649Z.log`（172/172）。 判官修正輪（2026-09-28 08:10Z）：產生器改為 `6f26e0ad2e3b6fbd…`（只改 fig_q4 的標籤），同一次重生本圖 PNG 逐位元不變（`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-judgefix-q4-20260928T0810Z.log`）；紅檢 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_engineering_figs-redcheck-20260928T0809Z.log`（128 個停止點：125 個看過紅、3 個到不了；174 個竄改 174/174；對照組 4/4；harness 自檢 4/4）。 重新釘住（2026-09-28 08:48Z）：產生器 `8959a132cc21b9d2…`（STATE `3368412d`；改的是 q3–q5），同一次重生本圖 PNG 逐位元不變（`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-repin-20260928T0848Z.log`）；紅檢 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_engineering_figs-redcheck-20260928T0846Z.log`（180/180）。 再釘到 main `eef173a9`（08:58Z）：產生器 `a0f7cc8a4d1cb252…`（改的是 q4 的 compare 記錄格式與 STATE_AT），同一次重生本圖 PNG 逐位元不變（`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-repin2-20260928T0858Z.log`）；紅檢 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_engineering_figs-redcheck-20260928T0857Z.log`（133 個停止點：130 個看過紅、3 個到不了；181 個竄改 181/181；對照組 4/4；harness 自檢 4/4）。
