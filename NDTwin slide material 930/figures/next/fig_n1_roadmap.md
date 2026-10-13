# `fig_n1_roadmap` —— 通往「帶自己的 .p4 來」的路

[Co-developed with claude code -- Adam]

（本檔所有時間為 UTC；run 目錄名的 `…Z` 就是 UTC。）

## 一句話

教授的目標是「帶自己的 .p4 來，NDTwin 把它模擬起來」。到 trunk `3368412d`（09-28 07:45 UTC，圖右上 as-of）：第一刀（NDTwin 寫外來程式的路由表）、
第二刀（心跳偵測＋改路）、**第三刀的 kernel 側（`get_graph_data` 的節點帶上 switch 的 capabilities，09-28 併入 `85bec430`）**已併入；
第三刀的 GUI 側（把 switch 做不到的操作變灰）在 Web-GUI repo 的分支上；「twin 看得見自訂標頭的流量」與多表 roles（load_balance）還沒開始。

**deck 版不畫 external 控制器的 detect-only 那一步**（coordinator 2026-09-27 UTC 第二輪：分支未併、不對外描述；Adam 2026-09-28：併入前不放回）。
含那一步的版本留作存檔：`fig_n1_roadmap_with_detect_only.{pdf,png,svg}`＋`_hires/`（09-28 用同一支腳本以 `--with-detect-only` 重生，狀態同 deck 版；detect-only 分支 `feat/external-detect-only-0927` @ `480e9f2e` 仍未併，照 coordinator 09-28 的確認，併入前不放回）。

## 資料來源（腳本執行時用 git 算狀態，唯讀）

K＝`/home/adam/Desktop/NDTwin-Kernel`；W＝`/home/adam/Web-GUI`。狀態一律對**釘住的 trunk commit `AT = 3368412d`**（09-28 08:3x 重新釘住時的公開 trunk head）算，不讀會動的 `trunk`

| 方塊 | 狀態怎麼算 | 依據 |
|---|---|---|
| cut 1 | `572d9462` 是 `3368412d` 的祖先 ⇒ done；日期＝該 commit 的 committer date，以 UTC 顯示（09-24 16:00Z；台灣時間是 09-25 00:00，與 `fig_o1` 一致用 UTC） | `K/doc/audit/2026-09-24_p4-driven-api-shape/REPORT-P4-2026-09-25.md`（第一刀）；ANALYSIS.md §8 裁決 4（`:401-408`） |
| cut 2 | `cafd518a` 是 `3368412d` 的祖先 ⇒ done（09-26 UTC） | 段 W merge；live H1–H5（`fig_h1`–`fig_h4`） |
| cut 3 | `85bec430`（Merge feat/kernel-capabilities-0927）是 `3368412d` 的祖先 ⇒ done（09-28 UTC）；方塊寫「capabilities on the graph API」 | 同上 ANALYSIS.md §8 裁決 3；CI：PR #14 兩個 run 四個 job 全綠、ctest 1385/1385（`K/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926/ci-compare-pr14.txt:1-2`） |
| cut 3 GUI | W 的分支 `draft/p4-capabilities-0924` 存在且不是 W `main` 的祖先 ⇒ on a branch（tip `65eecf6`，09-27 21:15Z；coordinator：未推、要不要推由 Adam 定） | Web-GUI 本機 git（唯讀） |
| next：twin 看得見自訂標頭 | git 裡沒有對應 ⇒ not started | GAP-2b §4-3（09-28 提交 `c8433963`）：「對外說 L3 達成目前沒有 raw 撐」；`fig_t9`（若有） |
| later：多表 roles | git 裡沒有對應 ⇒ not started | ANALYSIS.md §8 裁決 4：裁決把 load_balance 的多表範本、tunnel 的主機屬性、需要 ternary＋priority 的 app 都排在之後（`:406`，改寫、非原句） |
| 目標 | — | 教授的目標（本次工作指示；不是 repo 檔） |

腳本斷言：三個 done 的 sha 真的在 `3368412d`、兩條分支（存檔版多一條）真的存在而且**尚未**併入（一旦併入腳本會停，逼人更新圖）；讀不到 `3368412d` 的 sha 與日期也停。紅檢 5/5：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_roadmap-redcheck-20260928T0847Z.log`（git 的回答用模擬；09-27 版 3/3 在 `…-20260927T2002Z.log`）。
存檔版多一列（只在 `--with-detect-only` 時畫）：

| cut 2b（只在存檔版） | 分支 `feat/external-detect-only-0927` 存在且未併 ⇒ on a branch | Adam 09-27 裁決 B（external 也起心跳、只偵測不改路；orchestrator 記憶 `phase5-post-roles-state.md` 的「09-27 13:2x Adam 裁決 A–M」段（標題是 +08；＝05:2xZ）第 B 條，非 repo 檔） |

## 可信度

**OBSERVED（git，唯讀；kernel 與 Web-GUI 兩個 repo）**：done／on a branch 的判定。
**READ**：方塊內容與順序（裁決與分析文件）。
**INFERRED**：「next」「later」的先後是依裁決 4 的「之後」與 GAP-2b 的缺口排的，**不是**已排定的時程。

## 已知但書

- 「on a branch」不代表送審了：GUI 側的分支只在本機、沒有判官裁決檔（本檔查到的範圍內）。
- 09-28 08:4x 重新釘住：`AT` 由 `85bec430` 改成 `3368412d`（08:38 未認證查是兩個公開 trunk 的 head）；格子沒有變，只有右上的 as-of。
- 這張圖不寫日期承諾。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/next"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_roadmap.py
```

最後產出：2026-09-28T08:48:41Z（deck 版）、08:48:43Z（存檔版）（PNG 檔時間，UTC；重新釘住）；matplotlib 3.11.1；產生器 `make_roadmap.py` sha256 `0c746837d0ce38ba…`（只改 `AT` 為 `3368412d`）；重生紀錄 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/regen-repin-20260928T0848Z.log`（rc 0）；紅檢 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_roadmap-redcheck-20260928T0847Z.log`（5/5；`…T0846Z.log` 是改 harness 的模擬答案之前、3 個 SURVIVED，被取代）。上一版（`595aab61…`，as-of `85bec430`，PNG `db11947bf74e338f`）已被取代。
