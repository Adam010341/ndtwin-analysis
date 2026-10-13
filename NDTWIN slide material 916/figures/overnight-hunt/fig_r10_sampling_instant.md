# `fig_r10_sampling_instant` — ROLE-10 流量壓力狂 × 規模：取樣的那一秒決定了結論

**auditor 2026-09-15 起草。草稿（matplotlib），定稿由 Adam 交另一位 agent。**
產生器 `make_role_diagrams.py`（同目錄，一支產五張）。逐頁文字在 `../../ROLES-PAGE-BY-PAGE.md`。

[Co-developed with claude code -- Adam]

## 可信度

🟢 **親自讀過**：下表每個數字都出自 `scratch/overnight-2026-09-05/hunt-0911/00-LEDGER.md`
該輪的收工紀錄（我這個 session 開檔讀過）。
🔴 **我沒有跑過這一輪**；數字是當夜角色自己記的，**登記者（我）未獨立複驗**——
`doc/KNOWN-ISSUES.md` 相關條目也是這樣標的（🟢 實測／🟠 轉述）。

## 圖上每個數字

| 圖上的字 | 出處（ledger「05:55 ROLE-10 交件」） |
|---|---|
| 視窗前：nothing printed、rc 0 | 「**同一條連結同一種切法，切在 8 秒視窗的不同秒得三種答案**（視窗前不印 rc 0…」 |
| +3 s：`1.32 ok`、rc 0 | 「…**+3 s `1.32 ok` rc 0**…」 |
| +1 s later：`2.51 DOUBLE-COUNTING`、rc 4 | 「…**+1 s `2.51 DOUBLE-COUNTING` rc 4**）」 |
| 4 hosts ＝ 128 hosts ＝ 10 switches · 16 links | 「**規模軸在 `ndt check` 上不存在**（4 與 128 都是 10 switches／16 links，tripwire 兩輪**逐字相同**）」 |
| 248 extra edges are host-facing, every one excluded | 「128 多的 **248 條邊全 host-facing 被排除**」 |

## 那一輪的規模（沒畫進圖）

迴圈 **3599 秒**、**7106** 次 POST 全部 200 queued、delete **3549/3549** 被交換機拒絕（100%），
與 ROLE-5 在 4 台上看到的同一個形狀。

## 這張圖最該講的一句

**FIX-NDT-4 兩件都做到了**（不再說 replicas、rc 4 第一次 live 驗到），
**而判定仍然是取樣時刻的函數**。⇒ 🔑 **修法正確，結論仍不穩定——因為不穩定的不是修法，是量測窗口。**

## 座標軸的但書

🔴 三個取樣點的秒數是 ledger 記的相對位置（視窗前／+3 s／再 +1 s）。
**0–8 秒的刻度是示意**，不要讀成每一秒都取樣過。
## 這頁的講法

**規則 6**：投影片上只有標題與這張圖。下面這句進講者備註，不要印出來。

> 同一條連結、同一種切法，在八秒的視窗裡取樣三次得到三個不同的結論。修法是對的，不穩定的是量測窗口本身。
