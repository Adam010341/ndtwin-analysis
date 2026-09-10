# 簡報素材核對（2026-08-17）—— 清單，未動 template、未動 deck

Adam 指定的收尾項。對象是 `NDTwin-slide-template.md`；**deck 仍凍結**。
每條都註明「要不要改」與「為什麼」，你決定。

[Co-developed with claude code -- Adam]

---

## A. 數字：全部往上，但這是 template 自己預期的

Page 31 ① 與 template L102–103 的重量標的是「**動筆時重量**（2026-08-16）」，
而且 L69–70 就附了計算指令。所以這不是錯，是**該重跑一次**。用它自己的指令量到的現值：

| 欄位 | template（08-16） | 現在（08-17，head `13e53df`） |
|---|---|---|
| `tests/` .cpp 檔 | 46 | **47** |
| gtest case | 579 | **585** |
| `p4_proxy/tests` 檔／函式 | 16／438 | **17／453** |
| `tests/python` 檔／函式 | 7／236 | 7／**238** |
| `tests/shell` | 7 | 7（不變） |

L103 的成長敘事「426→547→579」要收成 **→585**。
（+6 = 今天新增的 `test_FlowTableCacheOptionalFields.cpp`，見 D-1。）

**建議**：定稿前最後一次重跑 L69–70 的指令再填，不要現在填死。

## B. Page 32「文件資產」——三處過時，建議改

1. **檔名全部沒有日期前綴**：`full_test_runbook.md`、`ovs_manual_test_runbook.md`、
   `p4_manual_test_runbook.md`、`environment_gotchas.md`、`ndt_api.md`… 這些路徑自
   `9e3874c`（2026-08-13 全面改名）起**都已失效**，正確形式是
   `2026-07-30_full_test_runbook.md` 這種。投影片上就算不寫全路徑，備註引用時會踩到。
2. **少了今天新增的兩個入口**：
   - `doc/README.md`——doc/ 的分類索引（現役／參照／歷史／草稿），**新的第一站**
   - `doc/2026-08-17_testing-manual.md`——測試的**唯一入口**，其餘七份已加地位橫幅
3. **兩份已降級為「歷史」**：`full_test_runbook.md` 與 `p4_status_and_test_guide.md`。
   Page 32 目前把它們與現役 runbook 並列，會讓「接手的人有路可走」這個訴求打折。

**建議改法**（一句話換掉分類）：操作＝`2026-08-17_testing-manual.md`（入口）＋兩份手動
runbook＋`environment_gotchas`；索引＝`doc/README.md`；其餘照舊。

## C. Page 30「五層測試架構（L0–L4）」——實際上有 L5

`faults.sh` + `faults.txt` 是 **L5 故障注入層**（`run_layers.sh` 與新的測試說明書都這麼寫），
Page 30 只講到 L4。L5 是 08-13 才加的，而且它在 08-16 的故障矩陣輪真的跑出結果
（目錄三型＋五延伸型態、系統零缺陷、時間常數量測）。

**建議**：Page 30 的分層表補一列，或在 Page 30 備註加一句。這是白拿的一層深度。

## D. 今天新產出的素材（要不要用，你決定）

**D-1. 🔴 `install_flow_entry` 回 400 卻真的裝上規則（live 實證）**
報告＝`doc/audit/2026-08-17_install-rejected-but-applied.md`；修復＝`ad49347`＋`1b1f941`。
- 為什麼值得上台：deck 的敘事主線是「baseline 的缺陷**全部無聲**——不 crash、不留 log、
  每個 endpoint 回 200」（L85、Page 18 ①②③）。這一條是**同一族的反面**且更難察覺：
  它**回 400**，所以連「回 200」這個線索都沒有。沒有人會去查一個被拒絕的請求做了什麼。
- 證據強度：交換機表 5→6 條、獨立通道（proxy `/stats/flow/1`）讀回、機制讀過源碼
  （`.value()` 建 job → enqueue → `.at()` 才丟例外 → 覆蓋回應）、四個 mutant 全殺。
- 可達性也查證過：**Web-GUI `SwitchFlowTable.tsx:899` 只在 priority > 0 時才放進 body**，
  而它自己的 API 註解寫「priority optional」——不是理論上的洞。
- **落點建議**：baseline bug 那節不合適（缺陷在我方 kernel），照 A2 規則應與
  readopt 同頁族（穩健性／我方缺陷）。或者獨立一頁當「後期測試輪的最後一個發現」。

**D-2. 契約覆蓋率成了可講的數字**
`/ndt/*` 端點 **41 個**（dispatcher 實數），`doc/2026-01-02_ndt_api.md` 記載 **41/41**，
其中 **32 個有機器檢查**（今天 30→32）。Page 30 的 L2 目前只有定性描述，這是現成的量化。

**D-3. 「測試工具自己的假 PASS」從 4 個變 6 個**
Page 31 ② 現在寫「修掉 4 個測試工具自己的假 PASS」。今天又 +2：`modify_nickname` 送
`nickname`、`modify_device_name` 送 `device_name`（文件規定 `new_nickname`/`new_name`），
**兩條從寫下來就沒綠過**，因為 MUTATE 類要 `--allow-mutations` 才跑。
這正好強化 ② 的論點：數字不是保證，機制才是。

## E. 不需要改的（查過了，特此記錄）

- **p4lang clone 疊加**：template 全文沒有提到要投上游，所以 08-17「不投遞只歸檔」的
  裁決**不需要動 deck**。
- **TE priority/idle_timeout**：template 沒提，今天的更正不影響簡報。
- **Page 29／33 的 bmv2 效能與 SIGSIM 出處**：08-15/16 已補齊，今天沒有新變動。

## F. 定稿前的最後一步（提醒）

deck 的四項落筆裁定（`DRAFT-v1-NOTES.md`）**仍未裁**，且 v1 尚未做像素 QA
（機器無 LibreOffice）。上面 A 的數字重跑，最好與那四項一起做，
一次改 `generator/build_deck.py` 重出 v2，不要分兩次。
