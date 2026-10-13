# `fig_h1_one_cut_cycle` —— 一次剪線、一次復原，量在 kernel 圖上

[Co-developed with claude code -- Adam]

（本檔所有時間為 UTC；run 目錄名的 `…Z` 就是 UTC。）

## 一句話

外來 P4 fabric（pod-topo、`--app basic`、roles 綁定）上剪一條 spine 線（`s1-eth3`↔`s3-eth1`），
從剪線開始到 kernel 圖兩向 `is_up:false` 是 **16.8 s**；拿掉 netem 到兩向回 `is_up:true` 是 **4.6 s**。
畫的是 H1 六個 cycle 裡**最慢**的那一個（cycle 3），保守的一端。

## 資料來源（腳本執行時讀取）

R＝`/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/2026-09-26T152605Z_08_heartbeat`

| 用途 | 檔 | commit／binary |
|---|---|---|
| 剪線、最後聽到、watchdog pass、graph down／up 的 CLOCK_MONOTONIC 時刻 | `R/30_cycles.tsv` 第 4 行（cycle 3）：`cut_a_start_mono` 72142.344、`last_heard_*_mono` 72142.316、`pass_prev_start_mono` 72153.926、`pass_start_mono` 72158.926、`graph_down_mono` 72159.171、`detect_s` 16.827；復原 `restore_a_start_mono` 72159.420、`first_heard_*` 72162.320、`restore_report_s` 3.401、`pass_up_start_mono` 72163.950、`graph_up_mono` 72164.042、`restore_s` 4.623 | `R/01_binaries.txt`：repo HEAD `cafd518a`、kernel `be70b5dd32356847`、helper `6a558fe452955de3` |
| 常數（5 s beacon、15 s timeout、5 s watchdog） | run log `…/intake-0926/hbw-live/h14-20260926T152605Z.log:63`；碼 `p4_proxy/proxy_agent/topology_manager.py:373`、`:419`、`:422` | trunk `3d740be0` 的檔 |

（`…/intake-0926/` ＝ `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926/`，未進版控。）

腳本斷言：`graph_down − cut_a_start == detect_s`、`graph_up − restore_a_start == restore_s`（差 ≤ 2 ms），六個 cycle 的 `strict_20s` 都是 `yes`。

## 可信度

**OBSERVED**：圖上每個時刻與兩個秒數（16.8、4.6）＝ `30_cycles.tsv` cycle 3 的值。六個 cycle 的範圍：剪線→down 12.204–16.827 s、復原→up 4.623–5.099 s（同檔 `detect_s`／`restore_s` 欄）。
**髒 checkout**：這個 run 是 `code cafd518a +85 file(s) with uncommitted changes`（`00_status_before.txt:7`），其中 2 個會改變行為：`p4_proxy/mininet/host_count_override`、`tools/remote-lab/dorm_lab/`（`…/intake-0926/hbw-live/h14-20260926T152605Z.log:14-17`）。
🔴 raw 在 trunk 未進版控（`.gitignore` 擋 `runs/`）；整個 run 目錄（194 個檔）在 audit-raw `797c34ab`，逐檔 blob 與工作樹相同（2026-09-27 17:2xZ 本機比對；最早收進的 commit 是 `543a3aa2`，`797c34ab` 的祖先）。`797c34ab` 依 coordinator 已公開在兩個 P4 repo。

**READ**：三個常數與規則「最後一幀之後沉默 > 15 s ⇒ 不通」（`topology_manager.py:419` 與 `link_heartbeat.py:1-30` 的說明）。

**INFERRED**（圖例寫「frame lost (inferred)」，2026-09-27 UTC 第二輪，coordinator 第 13 項）：圖上三個「frame lost」圓圈的位置＝最後聽到的那一幀 + 5 s × k（daemon 每 5 s 送一次，`tools/test_workflow/ndtwin-lab:734` `PERIOD_S = 5`；送出排程不漂移，P4-HB-SPIKE.md §2.5 引 `ndtwin-lab:1313`、`:1331`）。`30_cycles.tsv` 沒有逐幀的送出時刻，所以這三點是由週期推的，不是逐幀量到的。

## 圖怎麼讀

- 左：從剪線（時間 0）起算。心跳道：剪線前 0.028 s 最後一次聽到（綠點）；之後每 5 s 送的幀都被 netem 丟掉。
  「15 s timeout」從最後聽到的那一幀算起。watchdog 道：兩次 pass（+11.58 s 那次時間還不到，+16.58 s 那次判不通）。kernel 圖道：pass 之後 0.245 s 轉成 down。
- 右：從拿掉 netem（時間 0）起算。+2.9 s 第一次兩向都聽到、+4.53 s 的 pass 看見、+4.62 s kernel 圖轉回 up。
- 同一 run 的 pingall：剪線前 12/12 0% loss（`R/24_pingall_before.txt`）；cycle 1 判不通、改路後（線仍斷著）12/12 0% loss（`R/34_pingall_cut.txt`、run log `:72`「4 條 route 移開」、`:74`）；最後一次復原後 12/12（`R/37_pingall_after.txt`）。

## 已知但書

- **一次 run 只取樣到一個 watchdog 相位 ψ**（run log `:129`）：這一輪 ψ 在 1.49–1.76 s（`watchdog_phase_s` 欄），最壞 ψ≈5 s 沒被取樣到。見 `fig_h3_upper_bound`。
- 剪線是 out-of-band 的 `tc netem loss 100%` 同時下在兩端（不是 kernel 的 `inject_link_failure`）。
- 這是 **roles 綁定（owner ndtwin）** 的 package：會改路。沒綁定的 package（H3）只偵測不改路；external 控制面（H4）不起心跳（run log `:158`、`:168-172`）。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/heartbeat"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_heartbeat_figs.py
```

同時產出 `fig_h2_detect_vs_phase`。最後產出：2026-09-27T19:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_heartbeat_figs.py` sha256 `bfa5a5830e40158b…`（產圖之後腳本沒再改過）。
