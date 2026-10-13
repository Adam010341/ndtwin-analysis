# fig_t6_multicast_end_to_end —— 一支 exercise 從頭到尾：multicast 在 NDTwin fabric 上

[Co-developed with claude code -- Adam]

## 一句話

09-27 那一輪（T06，trunk `5dc7fc9a`）裡的 multicast：convert 出 7 個檔、pre-flight 24 個 PASS／0 FAIL、
claim 45 分鐘的租約、`ndt up` 起 1 台 bmv2 跑 exercise 自己的程式、proxy 經 P4Runtime 寫進 4/4 條表項與 1/1 個 multicast group（0 失敗）；
封包測試：解答臂 h1/h2/h3 互通、沒有人連得到 h4、h4 連得到別人（PASS 6/6）；骨架臂 12 對全不通，照預期（PASS 2/2）；
最後 `ndt down` 驗證乾淨、release、寫 arm report。

## 資料來源

R ＝ `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/runs`；
T06 ＝ `…/live-p1/runs/2026-09-27T074635Z_06_thirteen/00_table.tsv`；
SOL ＝ `R/2026-09-27T075305Z_multicast_solution_ndtwin.md`；SK ＝ `R/2026-09-27T075133Z_multicast_skeleton_ndtwin.md`。

| 用途（圖上的值） | 檔（path:line 或 JSON key） | commit／binary |
|---|---|---|
| 兩臂在 T06 的列 | `T06:8`（skeleton rc 0 `PASS (2/2)`）、`T06:9`（solution rc 0 `PASS (6/6)`） | — |
| run 站的 commit | `SOL:380`、`SK:383`（`ndt status` 的 `code 5dc7fc9a +95 file(s) with uncommitted changes`） | trunk `5dc7fc9a`，工作樹 +95 未提交檔 |
| bmv2 執行檔 | `SOL:183`（`running binary: /usr/local/bmv2-fast/bin/simple_switch_grpc`）；sha256[:16] `3ff54b5c1901c9d3`（`SOL:24`） | bmv2-fast `3ff54b5c`；p4c `226f3f66df515c9e`（`SOL:25`） |
| convert.py「7 files」 | `SOL:77`（`files : 7`，列在 78-84） | `tools/p4_exercise/convert.py` |
| pre-flight「24 PASS · 0 FAIL」 | `SOL:96-125` 的 PASS 列數（腳本數：24 PASS、3 INFO、0 FAIL；`SOL:125` `PASS -- every check passed`）；腳本斷言 N2 與 `ndt up` 內那兩份 pre-flight 一字不差 | `tools/p4_exercise/preflight.py` |
| ndt claim「45-min lease」 | `SOL:695`（`ok  lab claimed by orch-0927 for 45m`） | — |
| ndt up「bmv2 × 1」、s1 跑 `build/multicast.json` | `SOL:182`（`1 switches up after 6s`）、`SOL:75`（`pipelines : s1=build/multicast.json`）、`SOL:317`（`switches.1.pipeline.ndtwin: false`） | — |
| table entries「4/4 applied · 0 failed」 | `SOL:198`（`table entries: 4/4 applied on 1 switch(es), 0 failed`）；`SOL:345-351`（JSON `switches.1.table_entries`：applied 4、failed 0、recorded 4） | — |
| multicast group「1/1 applied · 0 failed」 | `SOL:332-336`（JSON `switches.1.pre_entries.multicast`：applied 1、failed 0、recorded 1） | — |
| h1–h4 | `SOL:50`（`hosts : h1, h2, h3, h4`） | — |
| 解答臂 4×4 矩陣 | `SOL:464-467`（`25% (9/12 pairs at 0%, 3 lossy)`；列出的 3 對是 h1/h2/h3 → h4，各 `100% loss, 0/5 received`；沒列的 9 對是 0%） | — |
| 解答臂「PASS (6/6)」 | `SOL:18`；§5 判定表 `SOL:589-594`（6 列全 PASS） | — |
| 骨架臂 4×4 矩陣 | `SK` 第 8 步（`SK:467` `100% (0/12 pairs at 0%, 12 lossy)`，12 對逐對列出） | — |
| 骨架臂「PASS (2/2)」 | `SK:18`；§5 `SK:581`（`RED ARM: nothing pings at all`） | — |
| 骨架臂也寫進了表項與 group | `SK:198`（4/4 applied, 0 failed）、`SK:335-339`（multicast applied 1、failed 0） | — |
| 「12 host pairs」 | `SOL:464`（`/12 pairs`）；§5 第一列 `0 untested of 12` | — |
| ndt down「verified clean」 | `SOL:558-566`（`verify clean` 段、`clean`）；`SOL:897`（`ndt down rc=0`） | — |
| ndt release「released」 | `SOL:582`（`ok  lab released`）；`SOL:904`（`ndt release rc=0`）；骨架 `SK:886` | — |

## 可信度

**OBSERVED（跑過，arm report 裡的 raw 輸出）**
- 上表每一個數字：7、24／0、45、1、4/4／0、1/1／0、12、9/12、3 對 100%、12/12 100%、兩個 verdict、rc 0。
- 誰收得到誰（逐條核過 raw，不信任何摘要）：
  - h1↔h2↔h3 六對都 0% loss、5/5（`SOL:590`）；
  - h1/h2/h3 → h4 三對都 100% loss、0/5（`SOL:465-467`、`SOL:591`）；
  - h4 → h1/h2/h3 三對都 0% loss、5/5（`SOL:592`）——h4 發出去的 ping 收得到回覆；
  - 兩邊 ARP 快取清空後重量 hX → h4，仍是三對 100%（`SOL:477`、`SOL:593`）。
  - ⇒ 先前某份摘要說「h2/h3/h4 收得到」**是錯的**；GAP-2b（09-28 Adam 裁定其中四格後提交為 `c8433963`，08:19Z 起在公開 trunk 上）說「h1/h2/h3 互通、h4 收不到」方向對，但要補一句：**h4 自己發起的連得到別人**。
- 骨架臂：12 對全部 100% loss（`SK:467` 起逐對）。表項與 group 同樣 applied、0 failed，所以骨架的「全不通」不是 NDTwin 沒寫表。
- 這兩份 arm report 與 T06 都在 **audit-raw `797c34ab`**（與工作樹比 blob hash 相同）。

**READ（讀碼或讀檔，沒有執行）**
- 為什麼 h4 收不到：driver 的判定表依據欄寫 `sig-topo/s1-runtime.json:47-65 replicates ports 1,2,3 only`（`SOL:591`，標【源碼推導，未執行】）。
  我另外讀了這一臂留下的 package 副本 `…/.test_run/packages/multicast-solution/sig-topo/s1-runtime.json:47-65`（mtime 2026-09-27T07:53Z，與本臂同時）：
  `multicast_group_id 1` 的 replicas 是 egress port 1、2、3。`.test_run` 會被下一輪覆寫，不是存檔。
- 為什麼骨架全不通：`SK:581` 依據欄 `multicast.p4:91 default_action = drop`（【源碼推導，未執行】）。
- `table_entries`／`pre_entries` 是 proxy 的 `GET /p4/switch_state` 自己回報的計數（proxy 的自述，不是從交換機讀回來的）。

**INFERRED**
- 無。圖上沒有推論出來的值。

## 圖怎麼讀

- 上排八格＝一臂從頭到尾的步驟（解答臂的數字；骨架臂的前幾步數字相同：`SK` 的 convert 7、pre-flight 24 PASS、表項 4/4、group 1/1）。
- 左下「NDT UP」：proxy 經 P4Runtime 把 package 的表項與 multicast group 寫進 s1；s1 跑的是 exercise 自己編出來的 `build/multicast.json`，不是 NDTwin 的程式。
- 右下兩個 4×4：列＝發送端、欄＝目的地；綠＝0% loss、紅＝100% loss、白＝自己。
  - 解答臂：最右一欄（→ h4）全紅，其餘全綠。
  - 骨架臂：全紅，這是這一臂該有的樣子（紅臂）。
- 格子底下是那一臂的 verdict，兩個都是 PASS：解答臂是「轉得動」、骨架臂是「照預期不通」。

## 已知但書

- **髒 checkout（F-16）**：`SOL:380-384`、`SK:383` 的 code 行是 `5dc7fc9a +95 file(s) with uncommitted changes`，其中 3 個會改行為（`p4_proxy/mininet/host_count_override`、`p4_proxy/mininet/app_package_override`、`tools/remote-lab/dorm_lab/`）。圖上沒有印 sha。
- multicast 是單交換機：沒有交換機之間的鏈路，所以心跳沒有東西可看（`SOL:184-187`，`heartbeat: nothing to watch ... (rc 3)`）。不要拿這一頁講心跳。
- 封包測試用的是 ping（ARP 經 multicast group 泛洪），不是 exercise README 裡的其他流量。
- `ndt up` 的 verify 印了「destination paths NOT CHECKED」（`SOL:195-197`）：外來程式上 NDTwin 不發 LLDP、不裝路由，轉發全靠 package 的 4 條表項。
- G1 鏈路使用率在解答臂 PASS（`SOL:487-498`，h1→h3 的 iperf，主路徑 s1-eth3 積分 38,784,142 bit，其餘三條 0.000）；圖上沒放，那是單播 iperf，沒走到 group 複製。
- arm report §1 自相矛盾：`SOL:24` 與 `SOL:183` 說跑的是 bmv2-fast（`3ff54b5c`），但同節 `SOL:27` 的附註寫「此處用的是 `/usr/local/bin` 那顆，不是 bmv2-fast」。
  那句是 driver 的舊樣板字（tutorials harness 時代），以 `ndt status` 與 `ndt up` 印的執行檔為準。
- `ndt down` 的 [1/3] 曾印「stack.sh down exited 1」（:30051、:9091 還在聽），[3/3] 清掉後 verify clean；最後 rc 0（`SOL:536-569`、`SOL:897`）。

## 重生指令

```
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/p4-tutorials"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_exercise_path_figs.py
```

同一支腳本也產 fig_t7、fig_t8、fig_t9。

- 紅測（mutation check）與產圖紀錄：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/o1-o2-t6-t9/`（`run_mutations.py`、`run_mutations.log` 14/14 照預期、`gen_overview.log`、`gen_p4tutorials.log`、各 mutant 輸入檔）。

最後產出：2026-09-27T17:05Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_exercise_path_figs.py` sha256 `6b2d5e08ced9bb91…`（產圖之後腳本沒再改過）。
