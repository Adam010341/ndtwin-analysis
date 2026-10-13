# fig_q3_review_catches —— 09-16 以來審查抓到的五件事：誰抓到、現在的狀態

[Co-developed with claude code -- Adam]

產出：`fig_q3_review_catches.{pdf,png,svg}` ＋ `_hires/fig_q3_review_catches.png`（畫布 13.33×5.4 in）。
產生器：`make_engineering_figs.py` 的 `fig_q3()`。

> **2026-09-27T17Z 起（協調者裁定，judge-SLIDES930.md F-13）：Q3 在投影片上改成表格頁，這張卡片圖移出 deck。**
> 圖檔保留作紀錄；投影片用下面「表格版」一節的內容。
> 2026-09-27 UTC 第二輪（coordinator 第 5 項）：第 3 列的「caught by」由 live run 改成 **raw review**——那一輪 live run 判 PASS（`00_table.tsv:27`），沒送達是讀 raw 才看到的（GAP-2b:239）；存檔的卡片圖同步改字。

## 表格版（Q3 頁用；日期皆 UTC）

| catch | caught by | when (UTC) | state | evidence path:line |
|---|---|---|---|---|
| cleanup 路徑的權限缺陷 / privilege bug in a cleanup path | judge | 2026-09-27 | fixed, merged fc25112e（main：#15 squash 299c9e23） | 判官紀錄（不公開，不列路徑）；merge fc25112e |
| 心跳量測被相位鎖住 / heartbeat test phase-locked | judge | 2026-09-26（≤06:42Z） | re-measured, merged 9c2e59e4 | I/judge-HBSPIKEDOC-4820862b.md:9；P4-HB-SPIKE.md:179 |
| G1 PASS 但沒送達 / G1 PASS, nothing delivered | raw review | 2026-09-27T08:12Z（run）；讀 raw 時發現 | open | ARMS/2026-09-27T081256Z_flowcache_solution_ndtwin/link_usage/iperf_client.txt:9-10、iperf_server.txt（無報告列）、netdev.before:3,7／netdev.after:3,7；live run 本身判 PASS（RUNS/2026-09-27T074635Z_06_thirteen/00_table.tsv:27）；GAP-2b:239 |
| H5 取樣器沒記到 / H5 sampler recorded nothing | live run | 2026-09-26T15:32Z | fixed, merged 0925d9fc | I/hbw-live/h5-20260926T153259Z.log:59 |
| ndt 改動讓 serve 錨點錯位 / ndt edit moved serve anchors | CI | 2026-09-26T15:25Z | fixed, merged 329dc555 | I/ci-36251857977-gcc.raw.log:6888；I/ci-compare-cafd518a.txt:11 |

「when」的依據：(a) 修正 commit 06b162f7 在 2026-09-27T11:50Z，判官的判決在它之前；(b) merge 318e6391（2026-09-26T06:42:56Z）的訊息已引用對 4820862b 的 MERGE AFTER FIXES；(c) 該臂的 run 目錄時戳；(d) run 目錄時戳；(e) CI run 36251857977 的 log 開始時間。
併入時間（UTC）：(a) 分支 fix/rulings-kjl-0927（tip 945d695d）以 fc25112e 併入 trunk，2026-09-28T06:36Z；PR #15 squash 進 main 為 299c9e23，08:28Z（兩個 main 同步）；9c2e59e4 2026-09-26T09:38Z；0925d9fc 與 329dc555 皆 2026-09-26T17:28Z。

## 一句話

五件事，四種抓法：判官兩件、讀 raw 一件、live run 一件、CI 一件；四件已修併入，一件還開著。

各件：cleanup 路徑的權限缺陷（判官；已修，#15）；心跳量測的相位鎖（判官）；G1 在沒送達的情況下 PASS（讀 raw——live run 自己判 PASS，是事後讀 raw 才看出沒送達）；H5 的取樣器什麼都沒記（live run）；ndt 的改動讓 ndt serve 的行號錨點錯位（CI）。

## 資料來源

縮寫：R＝`/home/adam/Desktop/NDTwin-Kernel`；I＝`R/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926`；
PREP＝`R/doc/audit/2026-09-04_p4-tutorial-exercise-prep`；RUNS＝`PREP/live-p1/runs`；ARMS＝`PREP/runs`。
**I、RUNS、ARMS 都不在版控（未提交的觀測）**；GAP-2b 09-28 提交為 `c8433963`（08:19Z 已在公開 trunk 上；本表讀的是提交前的同一段，§4 那幾行沒變）；P4-HB-SPIKE.md 與各 merge 已提交。

| 卡 | 用途 | 檔（path:line） | commit／binary |
|---|---|---|---|
| (a) Privilege bug in a cleanup path | 判官判決 | 判官紀錄（不公開，不列路徑；腳本讀它的判決行） | 判在 fix/rulings-kjl-0927 的 4a96f894 與 15217241 |
| (a) | 「fixed · merged」 | `git rev-parse fix/rulings-kjl-0927`＝945d695d；`git merge-base --is-ancestor 06b162f7 15217241`、`… 945d695d 3368412d`、`… 06b162f7 3368412d` 皆成立（Q3 的檢查釘在 3368412d）；merge fc25112e；main：PR #15 squash 299c9e23（NET/pulls_Adam010341.json 的 `merge_commit_sha`） | trunk 3368412d |
| (b) Heartbeat test was phase-locked | 判官抓到 | I/judge-HBSPIKEDOC-4820862b.md:5（MERGE AFTER FIXES）、:9 `Blocking 1：相位鎖的後果沒推到底`、:10（cycles 2–10 的剪線都落在最後一次聽到之後 φ≈0.62–0.80 s） | 判在 spike 報告分支 @ 4820862b |
| (b) | 「re-measured · merged」 | R/doc/audit/2026-09-25_p4-heartbeat/P4-HB-SPIKE.md:153（§2.3 run 1–2 的相位鎖）、:179（§2.4 run 3–4 去相位鎖）；merge 094f417f（量測第 8 輪＝去相位）與 9c2e59e4（報告補節，subject 含 `de-phased`）皆在 3d740be0 內 | trunk |
| (c) G1 PASS, nothing delivered | live 的 raw | ARMS/2026-09-27T081256Z_flowcache_solution_ndtwin/link_usage/iperf_client.txt:9-10（`Sent 3500 datagrams`、`did not receive ack of last datagram`）；同目錄 iperf_server.txt 沒有任何報告列；ARMS/2026-09-27T081256Z_flowcache_solution_ndtwin.md:1076 `PASS G1 …`、:457 `code 5dc7fc9a`；RUNS/2026-09-27T074635Z_06_thirteen/00_table.tsv 的 flowcache/solution＝`PASS (5/5)` | code 5dc7fc9a（09-27 live 驗收那一輪 06） |
| (c) | 誰寫下的 | PREP/GAP-2b-ndtwin-p4-capabilities-2026-09-27.md:239（§4 第 1 條；09-28 提交 `c8433963`） | — |
| (c) | 「open」 | 本地每條分支 `git log trunk..<branch>` 的 subject 沒有一條提到 G1（排除 audit-raw、claude-memory 兩個存檔分支；腳本執行時查） | — |
| (d) H5 sampler recorded nothing | live run 自己 FAIL | RUNS/2026-09-26T153259Z_08_heartbeat/ 沒有 50_samples.tsv；I/hbw-live/h5-20260926T153259Z.log:59 `FAIL 08_heartbeat -- H5 …`；該 run 的 01_binaries.txt:1 `repo HEAD cafd518a…` | code cafd518a |
| (d) | 「fixed · merged」 | merge 0925d9fc（訊息：取樣器內嵌 Python 在 3.13 是 SyntaxError、stderr 被丟到 /dev/null）；重跑 RUNS/2026-09-26T172912Z_08_heartbeat/50_samples.tsv 存在、I/hbw-live/h5b-20260926T172912Z.log:59 `PASS 08_heartbeat`，該 run 00_status_before.txt:7 `code 3f8c2abf` | trunk 0925d9fc；重跑在 3f8c2abf |
| (e) ndt edit broke serve anchors | CI 抓到 | I/ci-36233414349-gcc.raw.log:6879（9c2e59e4：14 組）→ I/ci-36251857977-gcc.raw.log:6888（cafd518a：15 組）；I/ci-compare-cafd518a.txt:11 `NEW RED: tests/python/test_ndt_serve.py RcProvenance…`（段 W 在 tools/test_workflow/ndt 加的行讓 11 個 RC_SOURCE 行號錨點錯位） | GitHub Actions run 36233414349、36251857977 |
| (e) | 「fixed · merged」 | merge 329dc555（re-anchor 11 個錨點）；I/ci-36259179041-gcc.raw.log:6885（3f8c2abf：回到 14 組） | trunk 329dc555 |

「found」日期（UTC）：(a) 2026-09-27；(b) 2026-09-26；(c) 2026-09-27；(d) 2026-09-26T15:32Z；(e) 2026-09-26T15:25Z（依據見表格版）。

## 可信度

**OBSERVED（跑過、看 raw）**
- (c) 那一臂 G1 判 PASS，而 iperf 伺服端沒有任何報告列、客戶端收不到最後一個 datagram 的 ack。
- (d) 第一次 H5 run 沒有樣本檔、run 以 FAIL 結束；修正後重跑有樣本檔、PASS。
- (e) CI 的 L1 在 cafd518a 從 14 變 15，329dc555 之後回到 14。

**READ（讀判官檔／報告／commit 訊息，未執行）**
- (b) 相位鎖是判官讀 raw＋迴圈碼得出（判官檔 :10 認同報告把它標為 INFERRED）；去相位的 run 3–4 由 P4-HB-SPIKE.md §2.4 記錄。
- (d) 根因（f-string 內反斜線在 3.13 是 SyntaxError、stderr 丟到 /dev/null）只來自 0925d9fc 的訊息；當時 stderr 沒留，raw 裡看不到 SyntaxError 本身。

- (a) 判官判 MERGE AFTER FIXES，之後三份複審，最後一份 MERGE；分支 09-28 併入 trunk（fc25112e）、PR #15 squash 進 main。機制不在此轉述。

**INFERRED（推論，未驗）**
- (c)「一個 datagram 都沒到 h3」：伺服端沒報告列＋s3-eth1 幾乎沒動（GAP-2b:244）推得，不是伺服端親口說 0。GAP-2b 對原因的推論（練習自己的控制器在同一流第二次寫表時拿到 gRPC UNKNOWN 後停止處理 PacketIn）也未驗；那是練習控制器的競賽，不是 twin 的錯；但 G1 的 PASS 不含「流量送達」這件事本身是 OBSERVED。
- (c)「open」：只代表本地沒有提到 G1 的修正 commit，不代表沒人在做。

## 圖怎麼讀

- 五張卡，每張：上＝抓到什麼（≤6 個字）、中＝誰抓到（judge／raw review／live run／CI）與發現日期、下＝狀態色塊（綠＝已修併入、黃＝修正中（09-28 重新釘住後沒有）、紅＝還開著）。
- 卡依「誰抓到」排：判官、raw review、live run、CI。

## 已知但書

- (b) 「re-measured」指量測方法修了、重新量了；run 1–2 的偵測時間只代表一個相位，不能當偵測時間的分布。偵測時間的數字在 heartbeat 那兩張圖，不在這裡。
- (c) 發生在 09-27 live 驗收的那一輪（protobuf 5 之後）；GAP-2b 說 09-19（換版前）也出現過一次同樣形狀，所以推論不是換版造成的（INFERRED）。GAP-2b 09-28 才提交（`c8433963`）。
- (d) 這件事 run 自己就 FAIL 了（不是靜默）；卡上說的是「沒記到東西」。
- 「review caught」泛指判官、讀 raw、live run、CI 四種關卡，不是只有判官。

- (a) 描述照 coordinator 09-28 的裁定：一句「cleanup 路徑的權限缺陷，審查抓到，已修（#15）」，不寫機制或攻擊步驟。

## 重生指令

```
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/engineering"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_engineering_figs.py
```

最後一次執行的輸出：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-r3-20260927T1951Z.log`（第三輪最終重生；前兩次是 `regen-r2-20260927T1854Z.log` 與 worker 的 `engineering-figs-run-20260927T1705Z.log`）（未提交）。

最後產出：2026-09-28T08:48Z（PNG 檔時間，UTC；重新釘住）；matplotlib 3.11.1；產生器 `make_engineering_figs.py` sha256 `8959a132cc21b9d2…`（STATE＝trunk `3368412d`；(a) 卡改成 fixed · merged，綠）；重生紀錄 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-repin-20260928T0848Z.log`（rc 0）；紅檢 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_engineering_figs-redcheck-20260928T0846Z.log`（132 個停止點：129 個看過紅、3 個到不了；180 個竄改 180/180；對照組 4/4；harness 自檢 4/4）。上一版的卡片圖（(a) 黃色「fix in progress」，PNG `0a3edc21981718bc`）已被取代。 再釘到 main `eef173a9`（08:58Z）：產生器 `a0f7cc8a4d1cb252…`（改的是 q4 的 compare 記錄格式與 STATE_AT），同一次重生本圖 PNG 逐位元不變（`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-repin2-20260928T0858Z.log`）；紅檢 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_engineering_figs-redcheck-20260928T0857Z.log`（133 個停止點：130 個看過紅、3 個到不了；181 個竄改 181/181；對照組 4/4；harness 自檢 4/4）。
