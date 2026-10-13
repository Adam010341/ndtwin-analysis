# `fig_b09_ghost_rule` — 排名 9 · #2/C-4

**auditor 2026-09-16 起草。草稿（matplotlib），定稿由 Adam 交另一位 agent。**
產生器 `make_baseline_bug_figs.py`（同目錄，一支產八張）。

[Co-developed with claude code -- Adam]

## 這張圖說什麼

install 後 0.257 秒流表就有那一列（快取），交換機 13.4 秒才真的有

## 層級

✅ **第一層 baseline**——受影響的檔首次提交於 **2025-12-15**。
與 `../overnight-hunt/` 那五張要分開放：那裡有四張是我們自己的 `ndt` 工具（2026-08-21 起），
不是繼承來的系統。混在一起講會讓人以為我們修的全是 baseline。

## 可信度

🟢 **我讀過出處檔**：`REPORT-PICK-FIXED.md` §1 第 9 列
🔴 **我沒有親自重跑過任何一項量測**；數字來自當時的紀錄，登記者（我）未獨立複驗。

## 但書

🔴 時間軸**非等比例**：0.257 s 與 13.4 s 之間被壓縮成排版距離。
