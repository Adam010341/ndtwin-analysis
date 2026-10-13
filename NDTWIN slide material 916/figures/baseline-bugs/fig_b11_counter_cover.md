# `fig_b11_counter_cover` — 排名 11 · A-7

**auditor 2026-09-16 起草。草稿（matplotlib），定稿由 Adam 交另一位 agent。**
產生器 `make_baseline_bug_figs.py`（同目錄，一支產八張）。

[Co-developed with claude code -- Adam]

## 這張圖說什麼

修法怎麼做的：不發明計數器，改成公布分母

## 層級

✅ **第一層 baseline**——受影響的檔首次提交於 **2025-12-15**。
與 `../overnight-hunt/` 那五張要分開放：那裡有四張是我們自己的 `ndt` 工具（2026-08-21 起），
不是繼承來的系統。混在一起講會讓人以為我們修的全是 baseline。

## 可信度

🟢 **我讀過出處檔**：`doc/audit/2026-09-02_fix-design-campaign/findings/A-7.md` §3.1（`dispatcher_running`）、§3.2（`counters_cover` 與兩個 `includes_*: false`）
🔴 **我沒有親自重跑過任何一項量測**；數字來自當時的紀錄，登記者（我）未獨立複驗。

## 但書

🔑 這張圖的重點是**被拒絕的那個選項**：boot-time 的計數器會結構性地永遠是 0，「一個永遠不會動的計數器比沒有計數器更糟」。
