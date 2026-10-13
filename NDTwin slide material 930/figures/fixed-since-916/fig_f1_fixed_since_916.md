# fig_f1_fixed_since_916 —— 09-16 之後修掉了什麼：39 個已公開、2 個在審（09-28 重新釘住；13:2x 在審加一條）

[Co-developed with claude code -- Adam]

## 一句話

09-16 報告之後，trunk 上多了 **39 個修法 merge，全部已在兩個公開 P4 本體的 trunk 上**（未認證 HTTPS，2026-09-28 08:38:26–08:38:27 UTC），也都在兩個 `main` 的內容裡（`299c9e23`）；
另有 **2 條修法分支在審**。41 格裡 **28 格是量測儀器／測試本身**（1 格在審），kernel C++ 只有 **2** 格（都已併入）。清單截止於 trunk `3368412d`（圖右上 as-of）。
09-28 06:2x 的版本是 37／0／2、截止於 `85bec430`；之後兩條在審的併入並公開：`rulings KJL`（`fc25112e`，proxy 層，main：PR #15）與 `TERM trap`（`3368412d`，tests / instruments，main：PR #16）。
在審的兩條：`residue clock`（ndt tool：residue report 兩次讀鐘的跨秒競態）；13:2x 加的 `spawn helpers`（tests / instruments：六支 shell 套件的 fixture spawn helper 失敗只離開 subshell、沒被算到；`fix/spawn-helper-subshell-0928` @ `dfdb2121`）。

## 資料來源

| 用途 | 檔（path:line 或 JSON key） | commit／binary |
|---|---|---|
| 每一格的代號、日期、狀態與底色；§1 的每個數字 | `NDTwin slide material 930/FIXED-SINCE-916.md` §1（數字表）、§2–§4（每列＝一格），腳本 `make_fixed_since_916.py` 的 `parse_md()` 在執行時解析 | 清單截止於 trunk 快照 `3368412d`（2026-09-28 07:45:54 UTC） |
| 快照 sha | 同檔 §0「**快照**：本機 trunk `3368412d`」 | `3368412d` |
| 公開 trunk head（✅ 的判準）與圖右上 as-of 的時間 | 同檔 §9.1 兩列（HTTP 200，40 位 sha，時間）；回應原檔 `figures/fixed-since-916/public-check-20260928b/branches_*.json`；每次請求 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/net-repin-20260928T0831Z.log` | 我自己，未認證 |
| 對帳：本窗 merge 全集 | `TZ=UTC git -C NDTwin-Kernel log --first-parent --merges --since=2026-09-16 3368412d`（66 個）＝§2 的 39 ＋§6 的 21 ＋§7 的 6，逐顆比對 | `3368412d` |
| 對帳：狀態 | `git merge-base --is-ancestor <sha> 3368412d…`（✅ 須真；🕓 對快照須假）；`git cat-file -e <tip>`（🕓 tip 存在） | 各列的 sha |
| 對帳：日期（UTC） | `TZ=UTC git log -1 --format=%cd --date=format-local:%m-%d <sha>`，§2–§4 與 §6、§7 的每一列 | 各列的 sha |
| 層的底色 | 腳本 `LAYERS`（`make_fixed_since_916.py` 的常數段）：設計常數，不是量測 | — |

- 腳本**讀**的只有上面這些；圖上沒有任何手打的數字、代號或日期。**畫布與清單上的日期全部是 UTC**（畫布日期列右端標 `UTC`）。
- `FIXED-SINCE-916.md` 證據欄引用的 live run 與判決檔，哪些在公開 `audit-raw` `797c34ab`、哪些只在本機工作樹（未提交的觀測），逐項寫在該檔 §0；那些路徑只在清單裡，**不上圖**。

## 可信度

**OBSERVED（跑了、看到的）**
- 2026-09-28 08:31–08:38 UTC（未認證，不帶 token；每次請求逐行在 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/net-repin-20260928T0831Z.log`）：兩個 P4 本體 `"private": false`、預設分支 `main`；兩個 `trunk` 都是 `3368412d`；
  兩個 `main` 都是 `299c9e23`（#6–#16；ndtwin-lab 依 Adam 09-28 的規則跟著快轉）；P4-public `main` 仍是 `9e6cc307`（09-03）；§4 的分支不在任何公開 repo 的分支清單裡。
- 13:20 UTC 未認證 `git ls-remote`（`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/net-spawnhelpers-20260928T1320Z.log`）：兩個 `trunk` 仍是 `3368412d`、兩個 `main` 仍是 `eef173a9`；`fix/spawn-helper-subshell-0928` 不在兩個 P4 本體的分支清單裡。
- `git diff --name-status 299c9e23 3368412d` 只差三個 `doc/audit/**/*.md` 與 `CLAUDE.md`（規則那顆，PR #17 開著）⇒ 39 格的碼都在兩個 `main` 裡。
- 腳本在 `3368412d` 上跑過全部對帳：66 個 merge 逐顆對上、39 個 ✅ 都是公開 head 的祖先、2 個 🕓 tip 存在且不在快照裡、每列的 UTC 日期都等於 committer 日期（`make_fixed_since_916.py` 的 `[ok]` 兩行）。
- 腳本的拒畫看過紅：13 個變異全部停在對的理由、對照為綠（`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/mutation_check_fixed_since_916.spawnhelpers-20260928T1321Z.log`；檔頭記產生器、harness、清單的 sha256，檔尾 rc=0；13:2x 在審加一條後重跑，harness 只換 M6、M10b 的錨點；前一份 `…repin-20260928T0905Z.log`）。
  - 重新釘住時拿掉的：中性標題、它的斜線磚與它的位置停止條件（在審那一項已併入，coordinator 裁定 D）；跟著拿掉的變異是 M10（中性數 1→0）、M11.1–M11.5（那一列搬回各層標題）、M12（第二列放進中性標題）——不是留著讓它們空轉。
  - 改瞄準的兩個：M10b（§1 有一列帶粗體數字、卻不是狀態也不是層，例如殘留的「不標層」數）、M11b（§2–§4 的標題沒有層名）；兩個都停在新的具名理由。
  - 其餘 11 個沿用（錨點換到 `3368412d` 的清單）。之前的紀錄：`…judgefix-20260928T0826Z.log`（18 個，判官修正輪）、`…refresh-20260928T0634Z.log`、`…r3b-20260927T1952Z.log`、`…without-placement-stop-20260927T1934Z.log`。

**READ（讀了、沒執行）**
- 每個 merge 是 FIX 還是 FEATURE、缺陷一句話、層別：讀 66 個 merge 的訊息全文＋`git diff --numstat <merge>^1 <merge>`。
- 證據欄的判決：讀 merge 訊息寫的判決，以及判決檔的判決行（行號寫在清單裡，例：`J26/cicxx/judge-CICXX-a956fd78.md:3`、`J26/cil1/judge-CIL1-e9c004f3.md:3`、`J26/qn1/judge-QN1-85befc7d.md:3`）。
- PR #6–#16 的併入時間與 squash commit：讀 `figures/engineering/_net/pulls_Adam010341.json`（08:32:08 未認證）。
- `rulings KJL` 的層：`git diff --numstat fc25112e^1 fc25112e`，不算測試檔，產線碼 534 行在 `p4_proxy/`、8 行在 `ndt` ⇒ proxy；`residue clock` 的產線碼只有 `ndt`（33 行）⇒ ndt tool。
- 證據欄的 live：讀 `live-p1/runs/*` 的 `00_table.tsv`、`42_pingall_loss.txt`、`40_verify_p4.txt`、`46_kernel_up_after_solution.txt`、`50_samples.tsv` 與各 exercise 報告的「code <sha> +N」行（別人跑的 run；我讀 raw，沒有重跑）。

**INFERRED（推的、沒驗）**
- FIX／FEATURE 的邊界是判斷：規則寫在 FIXED-SINCE-916.md §0；邊界上的案例——`2a551df7`（P3-A，算 FIX）、`094f417f`（spike 去相位，算 FEATURE）、heartbeat spike 第 3–6 輪（未跑過的儀器，算 FEATURE）——換一個規則會移動 1–5 格。
- 一格修多個缺陷時取多數層：`7242e127`（5 個缺陷，1 個在 `ndt`）、`rulings AEG`（E 在 proxy，A／G 在 live-p1）都畫成 tests / instruments。
- 09-28 新列的分類：CI L1 lane（hosted runner 上的 L1 把「沒有 lab」讀成 12 組，CI 跑過而錯）與 round.env（寫死主 checkout）算 FIX、層＝tests / instruments（產線碼是 L1 腳本、CI 設定與量測輪的 round.env）；TERM trap（suite 在 INT／TERM 後繼續跑，紅先行看過）算 FIX、層＝tests / instruments，分支 `fix/suite-term-trap-0928`；第三刀 kernel 側 `85bec430` 算 FEATURE。 重新釘住加的：`rulings KJL`（proxy）；`TERM trap` 搬到 §2.4（tests / instruments）。另外新進審查的 `residue clock`（ndt tool，在審；tip 在快照前 14 分鐘，本機沒有判決檔——若只算有判決的在審分支，這格不會出現）。13:2x 加的 `spawn helpers` 層＝tests / instruments（`git show --stat dfdb2121`：只改 `tests/shell/` 的 7 個檔，沒有產線碼；本機也沒有判決檔）。

## 圖怎麼讀

- 右上：as of 快照 sha 與公開查核的時間（清單 §0、§9.1）。
- 格上的字是 FIXED-SINCE-916.md 的「代號」欄；要看缺陷與證據，回那份清單找同名的列。
- 底色＝缺陷所在的層：深藍 kernel C++、橘 proxy、淺藍 ndt tool、淺灰 tests / instruments、白 docs（0）；圖例數字是三條帶合計（41 格）。
- 橫軸：merge 進 trunk 第一親鏈的日期（UTC；🕓 為分支 tip 的日期）；只列有修法的日子（09-17 只有功能與 README 的 merge、09-20〜09-23 沒有 merge，故不出現）。
- 三條帶＝三種狀態，互不混：上 **MERGED · PUBLIC**（實線框）、中 **MERGED · LOCAL ONLY**（虛線框，判定時 0）、下 **IN REVIEW**（點線框）；帶名旁的數字是格數。

## 已知但書

- **快照會過期**：清單截止於 trunk `3368412d`（08:38 公開）；分支 tip 取 08:3x UTC（`spawn helpers` 取 13:2x）。重跑前先更新清單。
- **公開預設分支 `main`**：兩個 `main` 在 08:38 都是 `299c9e23`（#6–#16 的 squash），tree 與 trunk `3368412d` 只差三個 `doc/audit/**/*.md` 與 `CLAUDE.md` ⇒ **39 格的碼都在裡面**（commit 本身不在 main 的歷史上）；在審的兩格不在。
- **公開 trunk ≠ 使用者照手冊拿到的**：手冊 P4 路徑 clone 的 `NDTwin-Kernel-P4-public` 停在 09-03（08:38 再查），41 格一格都不在那裡。
- **「live」是別人的 run，且都跑在有未提交檔案的 checkout 上**（每筆的「code <sha> +N」寫在清單證據欄，例 +29〜+92；09-27 的 T06 是 +95，audit-raw `797c34ab`）；我只讀了 raw，沒有重跑；`P3-A link bytes` 的 live run 沒記 kernel binary 的 sha；`fed37cff` 之後新併的 7 列都沒有 live run。
- **不是每一格都由 live 或 CI 先抓到**：不少是判官或閘門抓到的（清單 §2.4 末列出）。
- **有 4 顆直接落 trunk 的修法 commit 不畫**（清單 §5），與 916 那頁的做法一致。
- **`rulings KJL`**：cleanup 路徑的權限缺陷，審查抓到，已修（#15）；層＝proxy。判官檔四份（最後一份 MERGE）；分支以 `fc25112e` 併入 trunk、PR #15 squash 進 main。機制與攻擊步驟不上投影片、不寫進講稿。
- **不要把這頁講成性能結果**：這頁只數修法，不含任何量測數字；protobuf 5 切換（`5dc7fc9a`）前後的性能數字不在這頁。
- coordinator 以**已認證** `gh` 看到的狀態（Dependabot #1／#2 關閉等）是轉述，列在清單 §9.2，**不當公開證據**。
- 底色的色盲區分度（更正）：五個圖例底色在 protan／deutan／tritan 模擬下，**有磚的四色兩兩 OKLab 距離 ≥ 14.6**（最小的一對在 protan 模擬下）；
  **tests（`#E6E9EC`）對 docs（`#FFFFFF`）只有 6.6–6.8**（`…/logs/slides930/cvd_layer_fills.log:10`）——docs 本窗 0 格，只出現在圖例。先前寫的「兩兩 ≥ 14.6」是錯的。
  dataviz 指引附的 node 驗證器因這台沒有 node 而未跑。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/fixed-since-916"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_fixed_since_916.py
```

（需要 kernel checkout 在 `/home/adam/Desktop/NDTwin-Kernel`，或設 `NDTWIN_REPO`；只做唯讀的 git 查詢（TZ=UTC），不連網。）

最後產出：2026-09-28T13:21:28Z（PNG 檔時間，UTC；13:2x 在審加一條）；matplotlib 3.11.1；產生器 `make_fixed_since_916.py` sha256 `d93cead050551a98…`（沒改）；重生紀錄 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-spawnhelpers-20260928T1321Z.log`（rc 0）。上一版（39／0／1，PNG `97ea8e0255f1510d`，08:48:40Z 重新釘住）已被取代。
