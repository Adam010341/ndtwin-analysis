# `fig_b08_delete_reports_gone` — 排名 8 · #1/A-10

**auditor 2026-09-16 起草。草稿（matplotlib），定稿由 Adam 交另一位 agent。**
產生器 `make_baseline_bug_figs.py`（同目錄，一支產八張）。

[Co-developed with claude code -- Adam]

## 這張圖說什麼

刪除帶 buckets 被 OVS 拒、Ryu 不回錯、kernel 回 200 deleted，而 group 還在

## 層級

✅ **第一層 baseline**——受影響的檔首次提交於 **2025-12-15**。
與 `../overnight-hunt/` 那五張要分開放：那裡有四張是我們自己的 `ndt` 工具（2026-08-21 起），
不是繼承來的系統。混在一起講會讓人以為我們修的全是 baseline。

## 可信度

🟢 **我讀過出處檔**：`REPORT-PICK-FIXED.md` §1 第 8 列（根因鏈逐段）
🔴 **我沒有親自重跑過任何一項量測**；數字來自當時的紀錄，登記者（我）未獨立複驗。

## 但書

四格是**機制鏈**不是時間軸，沒有量到的秒數。
