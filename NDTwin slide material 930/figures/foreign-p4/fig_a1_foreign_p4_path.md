# `fig_a1_foreign_p4_path` —— 一支外來 P4 程式怎麼在 NDTwin 上跑起來

[Co-developed with claude code -- Adam]

（本檔所有時間為 UTC。）

## 一句話

上排是一支 exercise 從資料夾到報告的七步（`drive_exercise.py` 對每一臂都這樣跑）；
下面是 `ndt up p4 --app` 起來之後同時在跑的東西：bmv2 每台跑 **exercise 自己編出來的程式**，
P4 proxy 經 P4Runtime 把 pipeline、表項、multicast group（以及 roles 綁定的那張路由表）寫進去——圖上 proxy 方塊裡只放這四個名字（四個小方塊），
root helper 在交換機間的 veth 上跑心跳；2 支 exercise 帶自己的控制器（external 模式），NDTwin 那時什麼都不寫。

## 資料來源（方塊都能在 live raw 裡找到名字）

K＝`/home/adam/Desktop/NDTwin-Kernel`，E＝`K/doc/audit/2026-09-04_p4-tutorial-exercise-prep`，
B＝T06 的 basic/solution arm report `E/runs/2026-09-27T074826Z_basic_solution_ndtwin.md`（code `5dc7fc9a`，`:446`）。

| 方塊 | 在 raw 裡的樣子 | 等級 |
|---|---|---|
| exercise → convert.py → package | B §4 步驟 1「N1 convert.py」`:67`起（`package 'basic' -> …`、`pipelines : s1=build/basic.json …`） | OBSERVED |
| pre-flight（圖上寫「package checks」；**21–25 項 PASS** 只在本檔） | 腳本數每份報告 pre-flight 區塊裡的 `  PASS` 行：T06 的 24 份 PASS 臂為 21–24 項（p4runtime／flowcache 21、多數 23、multicast 24），07 roles 的 `E/live-p1/runs/2026-09-26T202055Z_07_roles_basic/12_preflight_basic_roles.txt` 25 項 | OBSERVED |
| ndt claim | B 的 transcript `:877`「ok lab claimed by orch-0927 for 45m」 | OBSERVED |
| ndt up p4 --app | B `:191`「[1/3] bmv2 fabric」、`:202` heartbeat started、`:204`「[2/3] proxy + kernel」、`:210`「[3/3] verify」、`:214`「table entries: 5/5 applied on 4 switch(es), 0 failed」 | OBSERVED |
| multicast groups | T06 multicast/solution 的 pre-flight「1 multicast group(s)」（`E/runs/2026-09-27T075305Z_multicast_solution_ndtwin.md:162`）與 `switch_state` 的 `pre_entries`（同檔 `:326` 起；GAP-2b §1 記 applied 1、failed 0） | OBSERVED |
| roles.ipv4_route：NDTwin 寫程式自己的路由表 | 07 roles run：kernel batch 寫入 → dispatch `accepted_by_switch 1` → `/stats/flow/1` 讀回 10.0.9.9（見 `fig_d1`、`fig_d2`） | OBSERVED |
| heartbeat（root helper，0x88B5） | B `:202`；機制見 `fig_h0b` | OBSERVED（有跑）／READ（機制） |
| kernel：graph、link usage；samples | B pre-flight 的 INFO「telemetry.source not declared (auto: NDTwin's pipeline gets the cooperative path, anybody else's gets link telemetry)」（`:128`、`:173`）與 `:217`「telemetry: auto -- 0 cooperative, 4 」（報告在這一行被截斷）；link telemetry＝`tc` 取樣 → root emitter → sFlow → kernel（TICKET-P3 §2.5） | OBSERVED（有跑）／READ（路徑） |
| packet test（它自己的檢查） | B `:503` pingall、`:513-582` B2–B5（send.py → h2）、`:625` G1、`:1160`「>>> PASS (6/6)」 | OBSERVED |
| ndt down · release · report | B `:654` N9、`:750` N10、`:759`「ok lab released」 | OBSERVED |
| its controller（圖上寫「p4runtime · flowcache」；13 支中 2 支） | p4runtime、flowcache 的 control_plane_mode＝「跑時控制器」（GAP-1 §2b，`fig_t1b_requirements_matrix_0927.md` 的 control_plane_mode 表）；控制器經 `K/tools/p4_exercise/run_external_controller.py:70-97` 把寫死的 `127.0.0.1:5005N` 改寫到 fabric 的埠 | READ（行數）／OBSERVED（兩支 T06 解答臂 PASS） |
| bmv2（圖上不寫台數；每個 fabric 1–4 台） | T06 的拓樸：pod 4 台、三角 3 台、5h/3s 3 台、calc／multicast 1 台（GAP-2b §1 topology 那一列） | OBSERVED |

## 可信度

每個方塊的**存在**都是 OBSERVED（2026-09-27 T06 或 2026-09-26 07 的 raw）；**箭頭的機制**（誰經什麼協定寫什麼）是 READ。
raw 狀態：本頁引用的 B、multicast 報告、07 的 `12_preflight_basic_roles.txt`、T06 `00_table.tsv` 都在 **audit-raw `797c34ab`**（`git rev-parse 797c34ab:<path>` 對 `git hash-object`，blob 相同，2026-09-27 17:1xZ 本機唯讀比對）；GAP-2b **未提交，待 Adam 審**（只在 T1c／此頁的 topology 那一列被引用）。
**髒 checkout**：T06 各臂 `code 5dc7fc9a +95 file(s) with uncommitted changes`（B `:446`）；07 roles `code b2eeb71d +92`（`E/live-p1/runs/2026-09-26T202055Z_07_roles_basic/00_status_before.txt:7`）。
**圖上沒有數字**（2026-09-27 UTC 第二輪，coordinator 第 13 項：這頁同時有跑過的方塊與讀碼的箭頭，所以跑出來的數字不上圖）。下表的「21–25 項」「1–4 台」「2 支」只在本檔與講稿；21–25 仍由腳本在執行時從那 25 份報告數出來並印出。

## 已知但書

- **不要**把這張圖講成「NDTwin 能操作任意外來 P4 程式」（Adam 2026-09-25 裁，orchestrator 記憶檔、非 repo：第二刀做完之前不對外這樣說；external 的 detect-only 在分支上、未併進 trunk `fed37cff`）。
- 表項寫入目前只支援 exact／lpm；`journaled: false`——proxy 重啟後表項會消失（GAP-2b §2 `tables`；`K/p4_proxy/proxy_agent/api_routes.py` `/p4/table_entry` 的說明）。
- external 模式（2 支）下 proxy 不開仲裁、不寫、不起心跳（`fig_h0b` 的但書）。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/foreign-p4"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_foreign_p4_diagram.py
```

## 判官修正（2026-09-27 UTC；F-21、F-16、F-18；第二輪：圖上的跑出數字拿掉）

- F-21：proxy 方塊裡的條列改成四個只有名字的小方塊（pipeline／table entries／multicast groups／roles.ipv4_route）；說明移到本檔。
- F-16：補髒 checkout 行；F-18：日期改 UTC；raw 狀態改引 audit-raw `797c34ab`。

最後產出：2026-09-27T19:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；當時的產生器 `make_foreign_p4_diagram.py` sha256 `efbccb4c6584d2a8…`。之後腳本改過一次（2026-09-27 20:04Z，只加了「07 那份沒有 pre-flight 區塊就停下」的停止條件），現在是 sha256 `8239f33506d018bd…`；用新腳本重跑，300 dpi 與 500 dpi 的 PNG 都與現有檔**逐位元相同**，所以沒有重新產圖。紅檢：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_foreign_p4_diagram-redcheck-20260927T2005Z.log`（2 個停止條件，2/2 以對應原因停下）。
