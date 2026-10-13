# fig_q2_review_path —— 一個改動怎麼進 trunk：worker → 獨立判官 → test merge 重跑 → merge → push → CI 對預測

[Co-developed with claude code -- Adam]

產出：`fig_q2_review_path.{pdf,png,svg}` ＋ `_hires/fig_q2_review_path.png`（畫布 13.33×6.9 in）。
產生器：`make_engineering_figs.py` 的 `fig_q2()`。

## 一句話

每個改動都在自己的 worktree 裡先寫會紅的測試，交給一位沒參與的判官下判決；判官要求修的就退回 worker；
過了之後 orchestrator 在 test merge 上重跑閘門、`merge --no-ff` 進 trunk、推兩個 repo，再拿 CI 的結果對事先寫下的預測——CI 出了新的紅也一樣退回。
**同一個快照（trunk fed37cff）**：09-16 以來 `logs/**/judge-*.md` 判官檔裡**至少** 49 個判決（23 MERGE、23 AFTER FIXES、3 其他；圖上寫「≥ 49」），trunk 上 58 個 merge、其中 45 個在訊息全文裡點名判官（只看主旨是 23 個）。
圖上「READ · SINCE 09-16」那一帶是**讀** git 與判官檔的文字數出來的；「RAN IT · EXAMPLE」那一帶的數字是閘門與 CI 真的跑過的 log。
範例是 2026-09-26（UTC）的心跳段 W（merge cafd518a）。

## 快照（圖上與本檔的所有計數都用這一個）

- trunk：`fed37cff`（committer date 2026-09-27T15:47:29Z；push-fed37cff.log 記 15:47:38Z 推上）。腳本斷言：`fed37cff..trunk` 之間沒有在截止時間前的 commit（產圖時 trunk 仍是 fed37cff）。
- 判官檔：`L/**/judge-*.md` 中 mtime ≤ **2026-09-27T15:55:00Z** 的 38 份。截止之後出現的判官檔不算、由腳本逐一印出：第一次產圖（17:05Z）時是 2 份（`intake-0926/sudo2/judge-SUDOPROBE-d57f90f1.md`，mtime 16:40Z；`intake-0926/slides930/judge-SLIDES930.md`，16:57Z，投影片的稽核）；18:54Z 重生時 4 份；第三輪這一跑是 8 份（再加 `aeg/judge-AEG-f7e2a128.md`、`cicxx/judge-CICXX-a956fd78.md`、`cil1/judge-CIL1-e9c004f3.md`、`n7/judge-N7-7b4a48b9.md`、`slides930/judge-SLIDES930-r2.md`、`…-r3.md`）。都是截止之後才寫的，所以 49 不變；名單在執行 log。
  `intake-0926/aeg/judge-AEG-ebe17f7c.md`（15:50Z）與 15:53Z 的一份複審（不列路徑）在截止之前，算入。
- 起點：`--since=2026-09-16T00:00:00Z`；判官檔 mtime ≥ 2026-09-16T00:00Z（全部 38 份都符合）。

## 資料來源

縮寫：R＝`/home/adam/Desktop/NDTwin-Kernel`；L＝`R/scratch/overnight-2026-09-05/logs`；I＝`L/orchestrator-0924/intake-0926`；G＝`L/gates-0910`。
**L 底下全部不在版控（未提交的觀測）。**

| 用途 | 檔（path:line） | commit／binary |
|---|---|---|
| 「≥ 49 verdicts」與 23／23／3 | 上述 38 份判官檔（**範圍只含** `R/scratch/overnight-2026-09-05/logs/**/judge-*.md`；`hunt-0911/fix/` 底下還有 6 份 `P2-F-JUDGE.md`、`P3-A…E-JUDGE.md`，`FIXED-SINCE-916.md` 引用它們，**不在**這個計數裡，所以寫「≥」）。判決的認法（`make_engineering_figs.py` 的 `V_LINE`）：`# 複審（…）：**<詞>**` 標題、FIX3 的表格列、REQ 的 `- **\`sha\`（…）：<詞>`、以及**行內任何位置**的 `合併裁決／判決／裁決／裁定／總判定／Verdict：<詞>`（關鍵字＋冒號必備，所以 merge 訊息裡的「judge MERGE on …」不算）；詞＝MERGE、MERGE AFTER FIXES、READY AFTER FIXES、READY FOR ADAM'S DECISION。腳本對 F-1 點名的六份逐一斷言結果（`JUDGE_EXPECT`），逐檔結果印在執行 log 的 `[judge]` 行 | 判官檔本身，無 binary |
| 「58 merges」「45 name a judge」 | `git -C R log --first-parent --merges --since=2026-09-16T00:00:00Z --format=%H fed37cff`＝58（以 +08 的 `--since=2026-09-16T00:00:00+08:00` 也是 58）；其中訊息全文含 `judge`（不分大小寫）的 45 個、只看主旨的 23 個。重算指令：<br>`for h in $(git log --first-parent --merges --since=2026-09-16T00:00:00Z --format=%H fed37cff); do git log -1 --format=%B $h \| grep -qi judge && echo $h; done \| wc -l`（主旨版把 `%B` 換成 `%s`）。coordinator 2026-09-27 UTC 另以同一方法核過 58／45／23 | trunk fed37cff（已提交） |
| 左下「at fed37cff」 | 同上的快照標記 | — |
| 範例：worker「103/103 seen red」「183/183 mutants killed」 | G/mutate_p4_heartbeat_w.p4hbw-ebdf365e.log:1（head ebdf365e）、:213 `every new proxy test seen red: 103 of 103`、:216 `mutation gate: 183 mutations, 0 survived` | 分支 feat/p4-heartbeat-w-0926 @ ebdf365e |
| 範例：judge「AFTER FIXES → MERGE」 | I/judge-HBW-1a3ebd7f.md:6 `總判定：**MERGE AFTER FIXES**`、:114 `R2 複審（ebdf365e …）：**MERGE**` | 判在 1a3ebd7f 與 ebdf365e |
| 範例：test merge「7b600ab0」「1658 tests OK」 | I/hbw/rerun3-summary.7b600ab0.txt:1-6（p4_proxy 1658 OK、其餘 4 項 rc 0、`tracked tree clean after the gates`） | test merge 7b600ab0 |
| 範例：merge「cafd518a」、標題列日期 09-26 | `git log -1 --format=%P cafd518a`＝9c2e59e4 ebdf365e（兩個 parent＝`--no-ff`）；committer date 2026-09-26T15:24:39Z | trunk cafd518a |
| 範例：push「2 repos」「public: 2×200」 | I/push-cafd518a.log:2-4、:9-11（兩個 repo 的 trunk 都 `9c2e59e4..cafd518a`），:20、:22（未認證 `curl …/tree/cafd518a` 兩個 repo 都 `200`） | — |
| 範例：CI「L1 14 → 15」「fix 329dc555」 | I/ci-36233414349-gcc.raw.log:6879（9c2e59e4：14 組）；I/ci-36251857977-gcc.raw.log:6888（cafd518a：15 組）；I/ci-compare-cafd518a.txt:11 `NEW RED: tests/python/test_ndt_serve.py …`；I/ci-36259179041-gcc.raw.log:6885（3f8c2abf：回到 14）；`git merge-base --is-ancestor 329dc555 3f8c2abf` 成立 | GitHub Actions run 36233414349、36251857977、36259179041 |

逐檔判決（腳本 `judge_tally()` 讀出，與執行 log 的 `[judge]` 行相同）：

| 判官檔（相對於 L） | 判決（行） |
|---|---|
| orchestrator-0919/judge-E-r10.md | MERGE AFTER FIXES（:5） |
| orchestrator-0924/judge-R-57aae1bf.md | MERGE AFTER FIXES（:3） |
| orchestrator-0924/judge-R-r2-3ff87a10.md | MERGE AFTER FIXES（:3） |
| orchestrator-0924/judge-ndt-serve-e4589399.md | READY AFTER FIXES（:5） |
| orchestrator-0924/judge-ndt-serve-r2-e28bcfe4.md | READY AFTER FIXES（:5） |
| intake-0925/judge-HB-9fbedc39.md | MERGE AFTER FIXES（:3） |
| intake-0925/judge-HB-r2-b22e88ed.md | MERGE（:5） |
| intake-0925/judge-HB-r3-01ff8368.md | **沒有單詞判決**（只逐條寫 CLOSED／NOT CLOSED；38 份中唯一一份） |
| intake-0925/judge-HB-r4-e1245b40.md | MERGE（:3，`**合併裁決：MERGE**`） |
| intake-0925/judge-OVS-6b7fce83.md／-r2-e1420df2.md／-r3-98442add.md | MERGE AFTER FIXES（:3）／MERGE AFTER FIXES（:1）／MERGE（:1） |
| intake-0925/judge-REQ-55cebe6c-7cc50b42.md | MERGE AFTER FIXES（:7，55cebe6c）＋其他（:12，7cc50b42：可進 live 試跑、不可併） |
| intake-0926/judge-FIX3-cafd518a.md | MERGE ×3（:9-11，三條分支） |
| intake-0926/judge-GUI-fcd4f69a.md | MERGE AFTER FIXES（:19）→ MERGE（:302） |
| intake-0926/judge-HBNOVENV-c4cb36b9.md | MERGE（:7） |
| intake-0926/judge-HBR4-79670365.md | MERGE（:5） |
| intake-0926/judge-HBR6-3d297c34.md | MERGE（:7） |
| intake-0926/judge-HBR7-a77b8fe2.md | MERGE AFTER FIXES（:5） |
| intake-0926/judge-HBR7b-96abb9b0.md | MERGE（:6） |
| intake-0926/judge-HBR8-3a724b87.md | MERGE（:6） |
| intake-0926/judge-HBSPIKEDOC-4820862b.md | MERGE AFTER FIXES（:5）→ MERGE（:33）→ MERGE AFTER FIXES（:44） |
| intake-0926/judge-HBW-1a3ebd7f.md | MERGE AFTER FIXES（:6）→ MERGE（:114） |
| intake-0926/judge-LP1C-c03130fe.md | MERGE AFTER FIXES（:3）→ MERGE（:332） |
| intake-0926/judge-NDTSERVE-48209682.md／-r2-f643b884.md | MERGE AFTER FIXES（:7）／MERGE（:5） |
| intake-0926/judge-NOTES-16069d1a.md | MERGE（:29） |
| intake-0926/judge-PB5PREP-6351be15.md | READY AFTER FIXES（:5）→ READY FOR ADAM'S DECISION（:24、:40） |
| intake-0926 底下另一個子目錄的 2 份（不公開，不列路徑） | MERGE AFTER FIXES、MERGE AFTER FIXES |
| intake-0926/judge-PSTUB-356d4e4e.md | MERGE AFTER FIXES（:3）→ MERGE（:270） |
| intake-0926/judge-R2B-4f661e31.md、judge-R3-c22d1300.md、judge-SGE-d271f5b8.md | MERGE（:21）、MERGE（:16）、MERGE（:3） |
| intake-0926/judge-STALE-d2a9d641.md | MERGE AFTER FIXES（:3）→ MERGE（:260） |
| intake-0926/aeg/judge-AEG-ebe17f7c.md | MERGE AFTER FIXES（:3） |
| intake-0926/queued/judge-QUEUED-bbb9fd41.md | MERGE（:3） |
| intake-0926/sudoprobe/judge-SUDOPROBE-103f94f0.md | MERGE AFTER FIXES（:1） |

合計：MERGE 23；MERGE AFTER FIXES 20＋READY AFTER FIXES 3＝圖上「AFTER FIXES 23」；READY FOR ADAM'S DECISION 2＋其他 1＝圖上「other 3」；共 49。

## 可信度

**READ（從 git 記錄與判官檔的文字數出來的，不是跑出來的）**
- `logs/**/judge-*.md` 的 38 份判官檔、49 個判決、1 份沒有單詞判決（上表）；範圍外還有 `hunt-0911/fix/` 的 6 份，所以全體是「≥ 49」。這是「數文件」，不代表判官判得對。
- 58 個 first-parent merge、45 個訊息全文含 judge、23 個主旨含 judge（`git log`，指令見上表）。
- 流程本身（worker 在 worktree、判官獨立、test merge 重跑、`--no-ff`、推兩個 repo、CI 對預測）：出自各 merge 訊息（例：cafd518a、5dc7fc9a）與 I/ci-prediction-*.txt、I/ci-compare-*.txt 的寫法；09-27 起 main 的更新方式另見 fig_q5。
- 「CI 出新紅 → 回到 worker」在範例裡的實際路徑：ci-compare-cafd518a.txt:11 寫 `fix dispatched (fix/ndt-serve-anchors-0926)`，該分支經 judge-FIX3 判 MERGE 後以 329dc555 併入。

**OBSERVED（範例的閘門與 CI 真的跑過；數字取自它們的 log）**
- 103/103 seen red、183 個變異 0 存活、test merge 上 1658 tests OK、兩個 repo 未認證讀回 200、CI 的 L1 14→15→14。

**INFERRED（推論，未驗）**
- 「45/58 點名判官」不代表另外 13 個沒審：其中 4 個是把 GitHub 上的 README 改動併回 trunk（6291db35、5f1d4611、7218ab82、dc0237c8），fed37cff 本身訊息只寫 `claim-note test independent of TMPDIR length`，其餘 8 個（09-17～09-19 UTC 的 P1/P3 系列與 0c96c1d0）訊息只寫工單或裁決編號；有沒有判官要去各自的收件紀錄查，我沒查。

## 圖怎麼讀

- 上排六格＝一個改動走的路；藍框＝判官。
- 黃色弧線（下方）＝判官判 AFTER FIXES 就退回 worker；紅色虛線弧（上方）＝CI 出現新的紅也退回 worker。
- 中段「SINCE 09-16 / at fed37cff」：左邊長條＝判官檔裡的判決數（綠 MERGE、黃 AFTER FIXES、灰 other）；右邊大數字＝trunk 的 merge 數；兩者是同一個快照。
- 下排＝範例（心跳段 W）在每一格實際留下的東西。所有日期都是 UTC。

## 已知但書

- 判決數是「判決」不是「改動數」：一份檔可有多輪（例 HBSPIKEDOC 三輪），一輪也可判多條分支（FIX3 三條）。
- 前一版寫「43（18／22／3）」、「7 份沒有判決」是錯的（judge-SLIDES930.md F-1）：舊的規則只認行首的判決，漏掉六份心跳複審寫在「一句話：…**合併裁決：X**」裡的判決。修正前後的差別有紅燈記錄：`L/slides930/engineering-verdict-regex-redcheck-20260927T1706Z.log`（舊規則六行全漏、新規則六行全中，三個對照行兩者都中）。
- 截止用 mtime：之後若有人改動某份已算入的判官檔，它會被排除並印在 `[q2] … after cutoff` 那行，重生時要看。
- 前一版的 merge 數 57 是在 3d740be0 數的；本版統一用 fed37cff（多了 fed37cff 這個 merge＝58）。
- 範例的 CI 那一格是「和前一次比」（ci-compare-cafd518a.txt 對 9c2e59e4），那一次沒有事先寫的預測檔；事先寫預測的例子是 7746832e、f186ce98、PR #6～#8（I/ci-prediction-*.txt）。
- 「0 survived」是 worker 在自己的 worktree 跑的閘門；orchestrator 在 test merge 上另跑的是 roles_binding 的 162 個變異（rerun3-summary:5），圖上沒放。
- 2026-09-27T15:24Z 起 main 不再由 trunk 直推（fig_q5），圖上的「push both repos」指 trunk。

## 重生指令

```
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/engineering"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_engineering_figs.py
```

最後一次執行的輸出（含 `[judge]` 逐檔判決）：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-r3-20260927T1951Z.log`（第三輪最終重生；前兩次是 `regen-r2-20260927T1854Z.log` 與 worker 的 `engineering-figs-run-20260927T1705Z.log`）（未提交）。

最後產出：2026-09-27T19:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；當時的產生器 `make_engineering_figs.py` sha256 `2c82ff1b8d151654…`。之後腳本改過兩輪、都只加停止條件、沒動畫法：紅檢修正輪（20:40Z：幾處沒有具名的解析失敗改成具名的停止條件、06／01 檢查逐項寫出原因、Q4 的 compare 記錄規則）與 API 欄位輪（20:52Z：API 快照在載入時就檢查圖要讀的每個欄位，`codes.txt` 每一行也檢查）；現在是 sha256 `3c44f472b1ac2292…`。用新腳本重跑，五張圖的 300 dpi 與 500 dpi PNG 都與現有檔**逐位元相同**，所以沒有重新產圖（`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-check-fixround-20260927T2054Z.log`）。紅檢：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_engineering_figs-redcheck-20260927T2053Z.log`（118 個停止點：115 個看過紅、3 個任何輸入都到不了；162 個竄改 162/162；對照組 3/3）。09-28 更新（Q4／Q5 的狀態刷新）：產生器又改一次，現在是 sha256 `468618f94882bff4…`；這張圖的 300 dpi 與 500 dpi PNG 重跑後與現有檔**逐位元相同**（`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-refresh-20260928T0658Z.log`、`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-check-all-*.log`），沒有重新產圖。紅檢 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_engineering_figs-redcheck-20260928T0649Z.log`（172/172）。 判官修正輪（2026-09-28 08:10Z）：產生器改為 `6f26e0ad2e3b6fbd…`（只改 fig_q4 的標籤），同一次重生本圖 PNG 逐位元不變（`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-judgefix-q4-20260928T0810Z.log`）；紅檢 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_engineering_figs-redcheck-20260928T0809Z.log`（128 個停止點：125 個看過紅、3 個到不了；174 個竄改 174/174；對照組 4/4；harness 自檢 4/4）。 重新釘住（2026-09-28 08:48Z）：產生器 `8959a132cc21b9d2…`（STATE `3368412d`；改的是 q3–q5），同一次重生本圖 PNG 逐位元不變（`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-repin-20260928T0848Z.log`）；紅檢 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_engineering_figs-redcheck-20260928T0846Z.log`（180/180）。 再釘到 main `eef173a9`（08:58Z）：產生器 `a0f7cc8a4d1cb252…`（改的是 q4 的 compare 記錄格式與 STATE_AT），同一次重生本圖 PNG 逐位元不變（`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-repin2-20260928T0858Z.log`）；紅檢 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_engineering_figs-redcheck-20260928T0857Z.log`（133 個停止點：130 個看過紅、3 個到不了；181 個竄改 181/181；對照組 4/4；harness 自檢 4/4）。
