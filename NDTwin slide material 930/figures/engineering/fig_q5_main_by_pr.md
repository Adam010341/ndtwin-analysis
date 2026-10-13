# fig_q5_main_by_pr —— main 只經 PR＋squash merge 更新；審查留在 trunk（09-28 重新釘住）

[Co-developed with claude code -- Adam]

產出：`fig_q5_main_by_pr.{pdf,png,svg}` ＋ `_hires/fig_q5_main_by_pr.png`（畫布 13.33×6.1 in）。
產生器：`make_engineering_figs.py` 的 `fig_q5()`。**as of 2026-09-28 08:53 UTC · public API, unauthenticated**（圖右上）。

## 一句話

判官、收件、裁決都只在 trunk 上進行，trunk 照舊推兩個公開 repo；main 不再由 `trunk:main` 直推，
改成：從 trunk 切 PR 分支（去掉 `doc/audit/**/*.md` 與 `REPORT*.md`）→ 只在 Adam010341/NDTwin-Kernel-P4 開 PR、跑 CI → squash 成一個 commit 進 main。
**09-28 起 ndtwin-lab 的 main 跟著同步**（每次 squash 完把同一顆 main 快轉推過去；取代 09-27 的「停在 f186ce98」）。到 08:53Z，#6 到 #17 十二個 PR 照這條路進 main（`eef173a9`；#16 比 #15 先 squash；#17 把這條規則寫進 main 的 CLAUDE.md），兩個 repo 的 main 相同，沒有開著的 PR。

## 資料來源

縮寫：R＝`/home/adam/Desktop/NDTwin-Kernel`；I＝`R/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926`（未提交）；S＝`R/scratch/overnight-2026-09-05/logs/slides930`；NET＝本資料夾 `_net/`。

| 用途 | 檔（path:line 或 JSON key） | commit／來源 |
|---|---|---|
| 規則本身（圖的每一個箭頭） | `git show 08f67b7a:CLAUDE.md`:27（main 只經 PR＋squash）、:28-30（PR 只開在 Adam010341；ndtwin-lab 的 main 跟著同步，Adam 2026-09-28）、:31（審核只在 trunk 與功能分支）、:32（不再 `trunk:main`）、:33（PR 排除 `doc/audit/**/*.md` 與 `REPORT*.md`） | trunk `08f67b7a`（06:4xZ 查時只在本機 trunk；08:38Z 已是公開 trunk `3368412d` 的祖先；腳本逐句斷言） |
| 兩個 repo 的 trunk、main 的 head | NET/branch_{ndtwin-lab,Adam010341}_{main,trunk}.json 的 `commit.sha`；HTTP 碼在 NET/codes.txt | 我自己，未認證（08:53:29–08:53:31Z） |
| main 上的 squash 串 #6–#17 | 從 Adam010341 main 的 head 沿 first-parent 走回 f186ce98：ce6a9832 (#6)、f347a588 (#7)、f9be5842 (#8)、bad4cc7a (#9)、847acc7d (#10)、5d0f442c (#11)、4a3d7f39 (#12)、d0696776 (#13)、be01cc7a (#14)、9a74408b (#16)、299c9e23 (#15)、eef173a9 (#17)，每個都只有一個 parent；每個 commit 的 patch 與它 PR 分支（NET/pulls_Adam010341.json 的 `head.sha`）自 merge-base 起的 patch 完全相同；NET/pulls 裡九個 PR 的 `merged_at` 非空、`merge_commit_sha` 各為上述 commit | 本地 git＋未認證 API（pulls 06:16:40Z） |
| PR 沒帶審核文件 | `git diff --name-only <parent> <squash>` 十二次（28、1、1、4、18、15、12、8、16、5、18、1 個檔）裡沒有任何 `doc/audit/**/*.md`、`REPORT*.md` | 本地 git |
| main 與 trunk 的內容 | `git diff --name-status eef173a9 3368412d` 只有三個 `doc/audit/**/*.md`（`GAP-2b-…-2026-09-27.md`、`live-p1/README.md`、`TICKET-P4-heartbeat.md`，依規則不進 main） | 本地 git |
| PR 的 CI 對預測 | I/ci-compare-pr6-48e8005d.txt、ci-compare-pr7.txt … ci-compare-pr17.txt（`prediction met`；pr15 是在紅的 attempt 重跑綠之後才 met）；預測檔 I/ci-prediction-pr*.txt（寫在推之前） | orchestrator 的記錄；job 結果見 fig_q4 |

公開查核（未認證，不帶 token）：08:53Z 那一輪逐行在 `S/net-repin2-20260928T0853Z.log`（兩個 main `eef173a9`、兩個 trunk `3368412d`；圖用這一份）；08:31–08:33Z 那一輪（兩個 main `299c9e23`，#17 開著）在 `S/net-repin-20260928T0831Z.log`，之前的在 `S/net-refresh-20260928T0616Z.log`。06:16Z：ndtwin-lab main 仍是 f186ce98、兩個 trunk `85bec430`、Adam010341 main `be01cc7a`；
06:42Z `git ls-remote https://github.com/{ndtwin-lab,Adam010341}/NDTwin-Kernel-P4.git`（不帶憑證）兩邊 main 都是 `be01cc7a`；06:45:52Z 的 branches 快照同（那一版的圖；留在 NET/prev-20260928T0645Z/）。
09-27 的查核紀錄（15:53Z～17:02:58Z，main 從 #6 走到 #8、ndtwin-lab main 停在 f186ce98）留在 NET/prev-20260927T*/。

## 可信度

**OBSERVED（我自己打公開 URL、讀本地 git）**
- 兩個 repo 都公開可讀（上面全部 HTTP 200 或 ls-remote 成功，未帶任何憑證）。
- 08:53Z：兩個 repo 的 main 都是 `eef173a9`、trunk 都是 `3368412d`。
- Adam010341 的 main 是 #6–#17 十二個單一 parent 的 squash commit，內容恰為各 PR 分支的 patch、不含 `doc/audit/**/*.md`／`REPORT*.md`。

**READ（讀規則，未執行）**
- 流程與排除規則：CLAUDE.md（`08f67b7a`）:27-35。PR 標題格式 `<模組>: <做了什麼> (#N)` 與十二個 squash commit 的 subject 相符。

**INFERRED**
- 無。

## 圖怎麼讀

- 左上藍框＝trunk：判官、收件、裁決都在這裡。
- 實線「push」＝trunk 推到兩個 repo 的 trunk。
- 灰虛線＋紅叉＝以前的 `trunk:main` 直推，09-27 起停止。
- 下排＝main 唯一的路：PR 分支（去掉審核文件）→ PR（跑 CI）→ squash 成一個 commit → Adam010341 的 main；綠字 #6–#17＝已照這條路進 main 的 PR（依編號，不是依併入的順序）；快照時沒有開著的 PR（有的話會寫在 PR 框下）。
- ndtwin-lab 的 main 標「follows」：它跟著 Adam010341 的 main 快轉，兩者是同一顆 commit。

## 已知但書

- 這張圖釘在 08:53Z 的快照（trunk `3368412d`、main `eef173a9`）。
- 新規則的 CLAUDE.md commit `08f67b7a` 已在公開 trunk 上（`3368412d` 的祖先），也已經 PR #17 進 main；圖上的「follows」是公開 API 看到的事實。
- 「公開」只用未認證 HTTPS 驗。2026-09-27T15:24Z 之前的 main 更新是 trunk:main 直推，不是 PR。所有時間 UTC。

## 重生指令

```
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/engineering"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_engineering_figs.py
```

最後產出：2026-09-28T08:58:28Z（PNG 檔時間，UTC；重新釘住到 main `eef173a9`）；matplotlib 3.11.1；產生器 `make_engineering_figs.py` sha256 `a0f7cc8a4d1cb252…`；重生紀錄 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-repin2-20260928T0858Z.log`（rc 0）。STATE＝trunk `3368412d`、公開 API 快照 2026-09-28T08:53Z（圖右上的 as-of）。紅檢：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_engineering_figs-redcheck-20260928T0857Z.log`（133 個停止點：130 個看過紅、3 個到不了；181 個竄改 181/181；對照組 4/4；harness 自檢 4/4）。之前：08:48:37Z（`299c9e23`、#17 open，PNG `1ee55fa6be46c241`）與 06:45Z 的快照（PNG `649f31a762f283e2`），都已被取代。
