# `fig_b04_poll_resurrects` — 排名 4 · #46/#36

**auditor 2026-09-16 起草。草稿（matplotlib），定稿由 Adam 交另一位 agent。**
產生器 `make_baseline_bug_figs.py`（同目錄，一支產八張）。

[Co-developed with claude code -- Adam]

## 這張圖說什麼

命令關機後 3.08 秒，30 秒輪詢把 is_up 寫回 true；9 次中 2 次

## 層級

✅ **第一層 baseline**——受影響的檔首次提交於 **2025-12-15**。
與 `../overnight-hunt/` 那五張要分開放：那裡有四張是我們自己的 `ndt` 工具（2026-08-21 起），
不是繼承來的系統。混在一起講會讓人以為我們修的全是 baseline。

## 可信度

🟢 **我讀過出處檔**：`REPORT-PICK-FIXED.md` §1 第 4 列；原始來源 `doc/audit/2026-09-03_fix-poll-resurrect/FIX-POLL-RESURRECT.md`
🔴 **我沒有親自重跑過任何一項量測**；數字來自當時的紀錄，登記者（我）未獨立複驗。

## 但書

🔴 時間軸是示意，只有 0 與 3.08 s 兩個點是量到的。
