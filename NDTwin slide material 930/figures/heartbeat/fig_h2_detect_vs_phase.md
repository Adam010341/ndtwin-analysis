# `fig_h2_detect_vs_phase` —— 偵測時間取決於剪線落在心跳週期的哪裡

[Co-developed with claude code -- Adam]

（本檔所有時間為 UTC；run 目錄名的 `…Z` 就是 UTC。）

## 一句話

七次 live 剪線（H1 六次＋H3 一次），x＝剪線落在最後一幀之後幾秒（φ），y＝剪線到 kernel 圖 down 的秒數。
七個點全落在設計帶內：下緣 15 − φ（規則成立的那一刻），上緣 15 − φ + 5（再等一整個 watchdog 間隔）。
最慢 16.8 s、最快 12.2 s。

## 資料來源（腳本執行時讀取）

R＝`/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/2026-09-26T152605Z_08_heartbeat`

| 用途 | 檔 | commit／binary |
|---|---|---|
| H1 六點 (φ, detect) | `R/30_cycles.tsv` 欄 `phi_s`、`detect_s`：(0.024, 16.524)、(0.025, 16.598)、(0.028, 16.827)、(4.485, 12.204)、(4.535, 12.278)、(0.984, 15.906) | repo HEAD `cafd518a`、kernel `be70b5dd32356847`（`R/01_binaries.txt`） |
| H3 一點（沒綁定的 package，只偵測不改路） | `R/64_cycle.tsv` 第 2 行：`phi_s` 0.017、`detect_s` 16.607 | 同上 |
| 設計帶（兩條線） | 常數 15 s、5 s：`p4_proxy/proxy_agent/topology_manager.py:373`、`:419`、`:422`；run log `…/intake-0926/hbw-live/h14-20260926T152605Z.log:63-64` | trunk `3d740be0` |
| 「20 s」虛線 | 工單的驗收值 `doc/audit/2026-09-25_p4-heartbeat/TICKET-P4-heartbeat.md:8-9` | — |

腳本斷言：每一點都在 [15 − φ, 15 − φ + 5 + 0.5] 內、且 ≤ 20 s；不在就 `SystemExit`。

## 可信度

**OBSERVED**：七個點（上表）。raw 未進版控（未提交的觀測）。

**READ**：兩條線的常數（15 s timeout、5 s watchdog）與規則。

**INFERRED**：把兩條線畫成「帶」——這是由常數推的設計範圍，不是量出來的分布；帶的上緣也還沒加 pass／HTTP／kernel 的耗時（d + ε，本 run 量到 0.031–0.245 s，`pass_to_graph_s` 欄）。

## 判官修正（2026-09-27 UTC；F-9）

- 7 個點有 4 個擠在 φ≈0.02 s（16.52／16.60／16.83／16.61 s）：加一個放大的內嵌圖，四點各帶數值；H1（6 次，owned table、會改路）畫圓點，H3（1 次，unbound、只偵測）畫方點，圖例分開。
- 🔴 dirty checkout：H1–H4 那輪 `cafd518a +85 file(s) with uncommitted changes`，其中 2 個可能影響行為（`p4_proxy/mininet/host_count_override`、`tools/remote-lab/dorm_lab/`；`…/hbw-live/h14-20260926T152605Z.log:14-17`）。

## 圖怎麼讀

- 點越靠左（剪線剛好在一幀剛被聽到之後），要等越久：規則從**最後聽到的那一幀**起算 15 s。
- 點高於下緣的部分＝watchdog 相位 ψ（下一次 pass 何時跑）＋ d + ε。本 run 的 ψ 只取樣到 1.474–1.755 s（`watchdog_phase_s` 欄；H1 六次 1.493–1.755，H3 一次 1.474）。

## 已知但書（講者備註要講的教訓）

- 🔴 **相位鎖**：09-26 第一次 spike（run 1–2，report 層級）的迴圈總是在「剛聽到一幀之後約 0.7 s」剪線（P4-HB-SPIKE.md §2.3）。
  raw：`/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-25_p4-heartbeat/spike/runs/2026-09-26T023021Z_S_heartbeat/20_cycles.tsv` 與 `…/2026-09-26T052148Z_S_heartbeat/20_cycles.tsv` 的 `down_s` 欄：
  20 次裡 **18 次落在 14.197–14.382 s**（兩次 run 的 cycle 2–10），另外兩次是各 run 的 cycle 1（**13.275、13.298 s**，前面多一個 `sleep 1`）——同一個相位的重複，不是分布
  （判官 `…/intake-0926/judge-HBSPIKEDOC-4820862b.md` Blocking 1）。trunk `4bc1201b`／`580767a8`。
  之後補了去相位的 run 3–4：`…/2026-09-26T085020Z_S_heartbeat/20_cycles.tsv`（sweep，10 次，10.077–14.904 s）、`…/2026-09-26T085506Z_S_heartbeat/20_cycles.tsv`（random，20 次，10.668–14.791 s），trunk `094f417f`。
  四份 `20_cycles.tsv`（連同整個 `spike/runs/`，462 檔）都在 audit-raw `797c34ab`，逐檔 blob 與工作樹相同（2026-09-27 17:2xZ 本機比對）。spike 四輪的 checkout 也都髒：`4bc1201b +79`、`580767a8 +79`、`094f417f +84`（兩輪），各 run 的 `code` 行。H1 再刻意取最壞相位（φ≈0.02 s）剪三次。
  ⇒ 早先流傳的「偵測中位數約 14.3 s」**是相位鎖住的 report 層級數字**，不是 kernel 層級、也不是分布；這份簡報不用它。
- 一次 run 只取樣到一個 ψ ⇒ 七個點**沒有**涵蓋 ψ→5 s 的最壞情況（見 `fig_h3_upper_bound`）。
- H1 的偵測時間從 `cut_a_start`（開始下第一端 netem）起算；spike 的 report 層級是從 tc 返回起算。兩者差約 0.08 s，這張圖只畫 H1/H3，不混。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/heartbeat"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_heartbeat_figs.py
```

最後產出：2026-09-27T19:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_heartbeat_figs.py` sha256 `bfa5a5830e40158b…`（產圖之後腳本沒再改過）。
