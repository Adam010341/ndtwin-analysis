# `fig_m1_hunt_pipeline` — 一夜夜巡的六個階段

**auditor 2026-09-15 起草。草稿（matplotlib），定稿由 Adam 交另一位 agent。**
產生器 `make_method_diagrams.py`（同目錄），重生指令寫在它的 docstring。

[Co-developed with claude code -- Adam]

## 這套方法有成文規格

🔑 **正本＝`.claude/skills/overnight-hunt/SKILL.md`（312 行）**。本圖畫的是 **09-11 那一夜的實際形狀**，
規格本身的階段切法略有不同（它多了兩個在夜巡開始前的步驟：印 `/goal` 那一行給 Adam 貼、
走之前用互動表單一次問完；結尾多一個 `WAKEUP.md` 四段交付）。上台若要講「我們的方法」而不是
「那一夜」，要補這三格。

## 可信度

🟢 **親自讀過**：本檔每一格的數字都出自我這個 session 打開讀過的檔案，逐項列在下表。
🔴 **沒有親自跑過任何一輪夜巡**——我讀的是 09-11 那一夜留下的帳本與角色報告。
本圖描述的是 **09-11 那一夜的實際形狀**，不是一套抽象方法論；別的夜巡階段數不一定相同。

## 每一格的出處

| 圖上的字 | 值 | 出處 |
|---|---|---|
| `ROUND 0` — 11 regression cells | 11 | `tests/fixtures/live_cells/` 底下 11 個 cell 目錄（`ls`，扣掉 `README.md`）；`tools/test_workflow/live_cells/` 有對應的 `.sh` |
| each one failed once | — | `tests/fixtures/live_cells/README.md`：`old/` 是修法前的 raw，`<cell>.sh judge old/` **必須 FAIL**，「a judge nobody has seen fail is a decoration」 |
| round 0 的時機 | — | `tools/test_workflow/live_cells/CELLS.md:12`「**When to run:** round 0 of a night round (while the reconnaissance agents are reading code)」 |
| `RECON` — 2 agents, read-only | 2 | `hunt-0911/00-LEDGER.md`「23:5x 第二步偵察派出（session 內 opus，唯讀，不動 lab）：recon-A…；recon-B…」 |
| 51 + 13 hypotheses | 51、13 | 同檔「00:49 recon-A 交件…317 行、**51 條假說**」；「00:41 recon-B 交件…831 行、11 種形狀 S1–S11、**13 條繞過建議 B0–B12**」 |
| `FALSIFY` — 27 held · 12 died · 8 unreachable | 27／12／8 | 同檔「01:17 …F-OFFLINE-1 完工訊息補的：**證實 27／推翻 12／構不到 8**／需 lab 或 build 17」 |
| `ROLES` — 11 roles | 11 | `hunt-0911/ROLE-*.md` 共 11 個角色（1–6、8–12；**沒有 ROLE-7**，R7 是另一回事，見下） |
| 45 min each, serialised | 45 | 帳本各輪派工句，例：「派 ROLE-1（opus，**45 分**預算，OVS4）」；序列化＝lab claim，「lab 序列化由本 session 持 claim」 |
| `FIX` — mutation gate / no red, no delivery | — | CLAUDE.md「測試沒看過紅就不算交付（mutation gate）」；帳本逐輪記 `閘門 N/0` |
| `CELL` — pre-fix raw = old/ · must FAIL forever | — | `tests/fixtures/live_cells/README.md` 的 `old/` 那一列與「🔴 Three rules about `old/`」第 1 條 |
| 回饋箭頭「tonight's finding becomes tomorrow's round 0」 | — | `CELLS.md:12` 同上；併入訊息 `fb2c281e`「nine live observations from the 09-11 hunt become repo scripts that run as **round 0 of every hunt**」 |
| `R7` — 每 10 分鐘一輪、唯讀、整夜 | 10 | 帳本「**R7 對帳審計員開跑**（唯讀、10 分鐘一輪到 06:30）」；在途表「R7 ｜ 跑中（10 分鐘一輪到 06:30）」 |
| EVERY ROLE：baseline → 45 min → restore → compare | — | 帳本每一輪都記這四步，例 01:06：「還原三件 `down` 0／`clean` 0／`status --check` 3＝基線（問題清單逐字相同）、orphans 兩輪 `VERDICT: CLEAN`、全機無 netem 殘留、13 個 M 不變 ⇒ **環境可信**」 |
| 「if they differ, the round is void」 | — | **這是我的措辭，不是原文**。原文是把「＝基線」當成宣告環境可信的前提。圖上這句是它的對偶說法；上台若要逐字，改引「環境可信」那句。 |

## 讀圖（全部進講者備註，不上投影片）

- **順序本身就是主張**：偵察與離線證偽在前、上機在後。帳本 23:5x 明寫「角色測試等偵察交件後再派（skill 第二步：**偵察在前**）」。理由是 lab 是序列資源，能離線殺掉的假說不該佔用它。
- **六個階段裡只有一個碰受測系統**（圖上唯一填色的那格）。這是這套方法能一夜跑 11 個角色的原因。
- **回饋邊才是這套方法的本體**：一條發現不是以「修好」收尾，是以「它的修法前證據被凍成一個永遠會紅的判決」收尾。
- **R7 是角色牌組裡的一員，但它並行不排隊**（`SKILL.md:181-192`）：唯讀、不持 claim、10 分鐘一輪、
  從頭開到尾。⚠️ **「ROLE-7 跳號是因為 7 被 R7 佔掉」是推論，規格沒有明說**；
  已查證的事實只有兩件：全機 `grep` 不到 ROLE-7，而 R7 用自己的檔名整夜並行。

## 已知限制（要講就要一起講）

- 圖上的數字全是 **09-11 那一夜**的。09-03 的 persona 輪與 09-12 的夜巡階段組成不同，不要拿這張圖代表全部。
- `27 held / 12 died / 8 unreachable` 三個數字**相加不等於 51+13**：另有「需 lab 或 build 17」一類，圖上沒畫。要精確就用表格，不要用這張圖對帳。
