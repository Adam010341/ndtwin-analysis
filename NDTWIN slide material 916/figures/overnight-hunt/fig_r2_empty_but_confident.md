# `fig_r2_empty_but_confident` — ROLE-2 重開循環壓力測：機器空了，而分身不知道

**auditor 2026-09-15 起草。草稿（matplotlib），定稿由 Adam 交另一位 agent。**
產生器 `make_role_diagrams.py`（同目錄，一支產五張）。逐頁文字在 `../../ROLES-PAGE-BY-PAGE.md`。

[Co-developed with claude code -- Adam]

## 可信度

🟢 **親自讀過**：下表每個數字都出自 `scratch/overnight-2026-09-05/hunt-0911/00-LEDGER.md`
該輪的收工紀錄（我這個 session 開檔讀過）。
🔴 **我沒有跑過這一輪**；數字是當夜角色自己記的，**登記者（我）未獨立複驗**——
`doc/KNOWN-ISSUES.md` 相關條目也是這樣標的（🟢 實測／🟠 轉述）。

## 圖上每個數字

| 圖上的字 | 出處（ledger「lab 第 2 輪收工」那一列，01:33） |
|---|---|
| bmv2 switches `0`、mininet processes `0`、topology session `none` | 「01:27:08 **0 bmv2／0 mininet／無 topo session**」 |
| `14` nodes, served on port 8000 | 「而 kernel 在 :8000 供 **14 節點圖**」 |
| `ndt status --check` → did not check | 「`--check` **rc 3「沒查」**」 |
| orphans verdict → CLEAN, no caveat | 「`orphans_verdict` **CLEAN 無但書**」 |

**同一輪還量到（沒畫進圖，在講者備註）**：cycle-07 時現場有 10 bmv2＋14 mininet＋活著的 proxy，
`orphans_verdict` **也是 CLEAN**——⇒ 這個判決在「什麼都沒有」與「什麼都有」時給同一個答案。

## 我的措辭選擇

「did not check」是 rc 3 的意思，不是工具的原字串；原字串在 ledger 裡寫作「沒查」。
## 這頁的講法

**規則 6**：投影片上只有標題與這張圖。下面這句進講者備註，不要印出來。

> 兩個儀器都沒有說謊——一個誠實地說「我沒查」，一個說「乾淨」。問題是沒有人分得出這兩句的差別，而機器上什麼都沒有了。
