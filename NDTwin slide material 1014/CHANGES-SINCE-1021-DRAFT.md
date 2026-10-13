# 1014 deck：和 1021 草稿（v0.2）相比改了什麼

[Co-developed with claude code -- Adam]

2026-10-12（UTC）。報告從 10-21 提前到 10-14（三）。除了差異化分析，加了一段 9/30 之後的 P4 支援，只放新功能、不放修掉的 bug。

這個資料夾是 `NDTwin slide material 1021/` 的複本，1021 資料夾沒有動（逐檔 sha256 相同）。slide repo 沒有 stage、沒有 commit。1021 的三個紀錄檔沒有帶進來。

## 0. 釘住的版本

- NDTwin 那一欄釘在公開的 trunk `3a47bdb7`，它的程式等於公開 main `828cceb5`（兩者只差 19 個 `doc/audit/**/*.md`）。v0.2 讀的是 `2ece656c`。
- 兩者之間，`src/`、`include/`、KNOWN-ISSUES、README 逐位元組相同。變的只有：
  - P4 proxy：`api_routes.py`、`main.py`、`p4_client.py`、新的 `match_shape.py`；
  - `ndt`；
  - `preflight.py`；
  - CHANGELOG 的 12a。
- 逐格紀錄：`research/CHANGES_1014.tsv`，66 列，每列附 3a47bdb7 的 file:line。

## 1. 頁序（22 頁；form 1/6/15）

| 頁 | 標題 | 和 1021 比 |
|---|---|---|
| P01–P10 | （同 1021） | 只改備註：行號與 sha 改成 3a47bdb7；P05 的 A4、P06 的 P1、P3、P4 依新碼重寫；P08 寫出 128 主機那兩輪 run |
| P11 | What each side had to build | 表上只剩 READ（給的／自己寫的），行數移到備註和 P12 |
| P12–P16 | （同 1021） | 只改備註：P13、P14 縮短，推導移到頁面區塊裡、講者備註之外的 Detail；寫明量測用的是 committed 2ece656c 加約 105 個未提交檔；新增 ❌「輸的地方現在可能沒了」 |
| **P17** | P4 support since 9/30: new features | 新頁（READ）。四列：ternary／range／optional、交換機自己的拒絕原因、外部控制器下的斷線偵測（只偵測）、P4 健檢 |
| **P18** | P4 health check: 57 cells, offline only | 新頁（圖）。左：判哪些格（READ）；右：離線結果（RAN），包括 S0、T4–T7，以及「writer vs bmv2, 52 cases: 0 disagree」 |
| P19 | Real problems, ranked: 1-6 | 原 P17。第 4 名重估約 2–3 週，狀態在備註寫成一行 |
| P20 | Real problems, ranked: 7-12 | 原 P18。第 10 名改成「P4 plane lacks ECMP, meters, five routes」，約 2–3 週 |
| P21 | Real problems, ranked: 13-19 | 原 P19。第 15 名的推論句已刪，那一列保留 |
| P22 | What we fix first, and what we disclose | 原 P20。#4 在 NEXT；#10 的標籤改了 |

被拿掉的：
- 原本的「寫入器 vs bmv2」表格頁，併進 P18，成為一列。
- 「proxy 重啟後規則回來」那一頁。那是在修已知的缺陷（第 4 名），不算新功能。
- P17 的 409 那一列。那是修缺陷時加的防護；409 仍寫在 P06 的 P3 備註。

## 2. 新功能與修正的歸類（9/30 之後的 PR）

- **新功能，上 deck：**
  - #25：外部控制器下的斷線偵測（只偵測）；
  - #28、#37：P4 健檢；
  - #38：ternary／range／optional＋priority，以及 502 帶錯誤碼。
- **修正，不上：** #19、#30、#31、#32、#35，以及 #36（409 的防護）。
- **只動測試：** #22、#23、#26、#27、#29、#33、#34。
- **不是 P4：** #18、#21、#24。
- **沒有合併：** #20 已關閉、未合併。
- **進行中、不是功能：** 重啟後的規則重放，只寫在第 4 名的備註。

## 3. 改了的格子（矩陣沒有 glyph 變動）

- p4.P1、p4.P3：文字依新的寫入器改寫；◐⚠◌ 都留著。
  - ◐ 的理由用碼講：NDTwin 自己的 pipeline 上，這條 route 每張表都回 409；package 只能經實驗室 CLI 進來。
- p4.P4：外部控制器下的心跳只偵測（`ndt:2960-2962`、`main.py:1459`）。這是 v0.2 漏看的，glyph 不變。
- maturity.M3：commit 數改成 2987（2ece656c 時是 2772）。
- problems：
  - 第 4 名：fix 改寫，成本約 2–3 週（INFERRED，2026-10-12 照 trunk 估），移到 NEXT。
  - 第 10 名：ternary 那部分已經做好、移出；補上缺的五條 proxy route；成本約 2–3 週。
  - 其餘 14 名只換 sha，行號照舊。

## 4. 圖

- 六張圖都用 `generator/regen_figs_1014.sh` 重產。
- 畫面上不放任何出處字樣（commit、日期、run id、檔名、path:line）。`figstyle_1014.py` 的 `save_all` 看到這類字就會停下。
- 新圖：`p4/fig_p18_health`，左右兩個面板。左邊每次都用 `git show 3a47bdb7:tools/p4_health/cells/table.py` 重讀來比對；右邊只放離線的 RAN，沒有預測。
- 改名：roadmap 改成 `next/fig_p22_roadmap`。
- 圖上不再標「進行中」。

## 5. 決定與紀錄

- 第 15 名（API 對外開放、沒有認證）保留在問題清單。這是 dispatching session 2026-10-12 的決定，理由是「no auth」已經是 P08 上的介面事實，也寫在公開的缺陷清單裡。原本備註裡那句推論的曝露說法已經刪掉。
- 離線結果的 raw 留在原處、不封存，備註只引 commit。
- 對手欄不重讀，也不加讀取日期標籤。

## 6. 對抗式抽查（對 NDTwin 有利的改動）

- **P3 文字（五種 match）：**
  - 反面讀法：只有離線觀測，不在 NDTwin fabric 上；而且只對 package 的表有用。
  - 所以 ⚠、◌、◐ 都留著；P16 的備註也寫明 NDTwin 自己的表回 409。
- **P4 scope（只偵測的心跳）：**
  - 反面讀法：只有讀碼；而且心跳是 root 的實驗室工具。
  - 所以 glyph 留 ◐。P17 的備註寫明「只有讀碼」，並說明外部控制器本來就不寫表，新的只是偵測。
- **P18 的 0 disagree：**
  - 反面讀法：比對的是形狀規則，不經過 owner 檢查，也不在 fabric 上；bmv2 只以安裝路徑識別。
  - 這些都寫在備註，標題寫 offline only。
- **P18 的 COMPLETE 和 GREEN：**
  - 反面讀法：只有少數格有結果，而且都是離線的。
  - 所以面板寫「not yet run against a live lab」，備註寫其餘格子沒有結果，並加了一條 ❌。
- **第 10 名移出 ternary：**
  - 反面讀法：kernel 的 `/ndt` API 在 P4 上能裝的規則種類沒有變。
  - 所以這一名保留，備註也寫了這一句。

## 7. 閘門

- 結果總表：`generator/logs-1014/FINAL-1014-r3.txt`。
- 產 pptx 的 log：`build-1014-r3.log`。
- 比對腳本的 log：`verify-deck-*.log`。
- 紅燈檢查的 log：`redcheck-1014-*.log`，開頭第一行記了 template 的 sha。
- 新 case 在 mutant 上變紅：`redcheck-1014-mutant-p18-footer.log`。
- 私密字詞掃描：`private-scan-1014-r3.log`。log 裡只記字詞清單的 sha256 和字數，清單本身放在所有 repo 樹之外。

## 8. 公開性檢查

- 公開性檢查的時間是 2026-10-11T14:43Z、2026-10-11T16:25Z、2026-10-12T05:25Z。
- 2026-10-12T06:08Z 公開 trunk 移到 acb3c4b7：只改了一個 doc/audit 摘要的一行，沒有改程式碼，所以程式碼仍等於 3a47bdb7。
- 這幾點寫在 template 開頭（Sources 段），不進投影片、也不進講者備註。
