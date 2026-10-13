# `fig_b02_loss_ladder` — 排名 2 · #53

**auditor 2026-09-16 起草。草稿（matplotlib），定稿由 Adam 交另一位 agent。**
產生器 `make_baseline_bug_figs.py`（同目錄，一支產八張）。

[Co-developed with claude code -- Adam]

## 這張圖說什麼

五個負載階梯的丟包率（0／0／0／0.34%／72.5%）與「每一階都回 success」；修後 API 帶 status／loss_fraction／分子分母

## 層級

✅ **第一層 baseline**——受影響的檔首次提交於 **2025-12-15**。
與 `../overnight-hunt/` 那五張要分開放：那裡有四張是我們自己的 `ndt` 工具（2026-08-21 起），
不是繼承來的系統。混在一起講會讓人以為我們修的全是 baseline。

## 可信度

🟢 **我讀過出處檔**：`doc/audit/2026-09-03_night-rounds/FINDINGS-ALL.md:87`（2k／20k／60k 每秒 0 掉；150,000/s 掉 0.34%；654,709/s 掉 72.5%）；API 欄位讀自 `src/ndt_core/collection/FlowLinkUsageCollector.cpp:1838-1857`
🔴 **我沒有親自重跑過任何一項量測**；數字來自當時的紀錄，登記者（我）未獨立複驗。

## 但書

🔴 五個階梯**不是等距的**（2k→654k），圖上是等寬排列＝示意。不要讀成線性關係。
