# 給簡報產生器 session 的指令：重畫「How we measured」那頁

（Adam 2026-09-02 交辦；本檔是 prompt 正本，貼給 deck generator 用。）

---

現在 deck 裡「How we measured」的流程圖太醜、也沒把嚴謹度講清楚。請重做這一頁。

**先做的事**：讀 `NDTwin-slide-template-903.md` 的 §C''（How we measured 的內容正本）與 §C0-v2
（23 頁版現行頁序），確認這頁要插在哪、前後頁講什麼，不要跟 p.8 的 `PRE-REGISTERED` band 重複。
數字一律以 `~/Desktop/NDTwin slide material/paper/abstract/abstract.tex` 的 §"Three preregistered
measurements"（約 170–200 行）為準，**不要自己算、不要四捨五入**。

**這頁要讓觀眾一眼看懂的一件事**：我們的每一個數字都是**通過一連串關卡**才被允許印出來的，
而且**我們自己知道哪幾道關卡沒守住、也照講**。不是「我們很嚴謹」，是「嚴謹長什麼樣子、破在哪裡」。

## 建議畫法：一條由左到右的關卡帶（不要用傳統方框箭頭流程圖）

一條水平的量測管線，上面掛五道關卡；每道關卡用一個小圖示＋2–4 個字；
**關卡下方用一行極短的字寫「它擋掉了什麼」或「它沒守住什麼」**。
三個實驗（build／size／flow）用三條細線並行穿過這些關卡，
**哪個實驗沒過某一關，那條線就在那裡斷掉或轉成虛線**——這是整張圖的重點。

五道關卡（由左到右）：

1. **Preregistered** — 出手前寫死區間**與每個結果的意思**，含放棄判準。三條線都通過。
2. **Two mirrored arms** — 複製單位＝交錯的 arm，不是 rep。build 實驗每 arm 重啟 fabric（換 build）；
   size／flow 共用一個不重啟的 fabric。⇒ 三條線都通過，但 build 那條要標「restarts per arm」。
3. **Binary identity** — 每 arm 雙向 symbol signature 對負控。**只有 build 那條是實線**；
   size／flow 只從 process command line 記 binary ⇒ 畫成虛線，旁邊一行 `weaker, disclosed`。
   這關的產出寫在旁邊：兩個 build 印出**同一個版本字串** `1.15.3-f0b7d201`。
4. **CPU gate** — per-process 外來負載偵測，**且只在陽性對照發火之後才採信**。
   build／size 兩條實線；**flow 那條線在這裡斷掉**（那個實驗早於 gate），旁邊一行 `no detector`。
   再加一行極短的字：gate 是取樣器，第二台機器上它**漏掉一個 co-tenant**（我們是從對方的 ledger 發現的）。
5. **Dual readout** — endpoint counters ＋ 成對的 ingress-RX／egress-TX 介面計數。
   旁邊一行數字：kernel drop counter 讀 0，而 bmv2 內部丟掉 **79.66%**。

管線右端：**Two machines**——machine 1（筆電）與 machine 2（16-vCPU guest）＝預註冊的複製。
用兩個很小的機器圖示，下面一行 `registered replication`。**不要寫機器型號、不要寫 nslab。**

管線左端（入口）可放一行 ladder 的規格：`×1.5 rungs · clean = loss ≤0.5% (3-rep medians) · ±1 rung`。

## 硬性限制

- **圖上字要少**（Adam 的規矩）：標題、五個關卡名、每關一行短註、右端兩台機器、左端 ladder 一行。
  推導、但書、方法細節寫進講稿，不要塞進圖裡。
- **投影片文字用英文**，字級跟現行 deck 一致（Adam 09-01 已要求字級上調）。
- **不要把嚴謹度畫成一致的**。flow 實驗沒有 CPU gate、size／flow 的 binary identity 較弱、
  第二台機器的 gate 漏了一個 co-tenant——**這三件必須在圖上看得出來**。
  這頁的說服力來自「我們自己標出破口」，把它畫成五關全綠反而會被問倒。
- 顏色沿用 deck 現行的色票；斷線／虛線要在灰階列印下仍分得出來。
- 產出後把新頁序更新回模板 §C0-v2，並附一行說明這頁取代了哪一頁。

