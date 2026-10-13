# `fig_c5_check` — `ndt check`

**auditor 2026-09-16 起草。草稿（matplotlib）。** 產生器 `make_ndt_command_figs.py`（一支產九張）。

[Co-developed with claude code -- Adam]

## 可信度

🟢 **逐字讀自工具自己的 `usage` 區塊**：`tools/test_workflow/ndt:8316` 起，2026-09-16 讀的。
🔴 **我沒有執行過這些指令**；rc 的意思是文件說的，不是我實測的。

## 層級（上台要講清楚）

`ndt` 是**我們自己寫的工具**（`tools/test_workflow/ndt`，首次提交 2026-08-21），
**不是繼承來的 baseline kernel**。這九頁屬於「我們建的工具長什麼樣」，
不屬於「我們修好了 baseline 的什麼」。

## 為什麼 rc 值得一頁

09-12 那一輪之前，`up`／`down`／`clean` 的退出碼互相重疊。那一輪讓每個碼只有一個意思，
而且三個指令用同一套：**0 做了、1 量過而讀數是髒的、3 什麼都沒量到、5 守衛拒絕什麼都沒做、2 呼叫錯誤**
（`check` 另有 4＝絆線響了）。**3 與 0 都「沒有抱怨」，但它們不是同一個答案**——這是整套的核心。
