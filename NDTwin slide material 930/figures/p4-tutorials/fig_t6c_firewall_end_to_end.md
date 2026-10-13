# fig_t6c_firewall_end_to_end —— 一支 exercise 從頭到尾：firewall 在 NDTwin fabric 上

[Co-developed with claude code -- Adam]

圖上標題：`firewall, end to end on the NDTwin fabric`（41 字元）。版型、色票、畫圖 helper 沿用 T4 的 `fig_t6_multicast_end_to_end`（從 `make_exercise_path_figs.py` import，那支檔一個字沒改）。

## 一句話

09-27 那一輪（T06，code `5dc7fc9a +95`，髒 checkout）裡的 firewall：4 台 bmv2，**s1 跑 exercise 的 firewall 程式、s2–s4 跑 basic**（兩個 p4info）；convert 出 12 個檔、pre-flight 23 PASS／0 FAIL、claim 45 分鐘、proxy 經 P4Runtime 寫進 28/28 條表項（s1 13 條、其餘各 5 條，0 失敗）；
封包測試（各 3 秒的 TCP iperf＋每一對 ping）：解答臂 h1→h3 過了 262 MBytes、**h3→h1 連線逾時**、12 對 ping 全 0% loss（**PASS (4/4)**）；骨架臂兩個方向都過（254／248 MBytes）、ping 一樣全通（**PASS (3/3)**，紅臂該有的樣子：防火牆還沒寫）。
twin 那一格：解答臂的鏈路讀數只驗過一般 IPv4 的 UDP iperf（h1→h4），路徑上 3 個介面 > 0、其他 9 個 0——**IPv4 only**。

## 資料來源

K ＝ `/home/adam/Desktop/NDTwin-Kernel`；R ＝ `K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/runs`；
T06 ＝ `K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/2026-09-27T074635Z_06_thirteen/00_table.tsv`；
SOL ＝ `R/2026-09-27T080128Z_firewall_solution_ndtwin.md`（同名目錄 SOLD）；SK ＝ `R/2026-09-27T080011Z_firewall_skeleton_ndtwin.md`；
TUT ＝ `/home/adam/tutorials`（c80d83e，這三支 exercise 目錄底下 0 個未提交修改）。

| 用途（圖上的值） | 檔（path:line） | commit／binary |
|---|---|---|
| 兩臂在 T06 的列 | `T06:18`（skeleton rc 0 `PASS (3/3)`）、`T06:19`（solution rc 0 `PASS (4/4)`） | — |
| run 站的 commit | `SOL:448`、`SK:459`（`code 5dc7fc9a +95 file(s) with uncommitted changes`） | trunk `5dc7fc9a`，工作樹 +95 未提交檔 |
| bmv2 執行檔 | `SOL:199`（`running binary: /usr/local/bmv2-fast/bin/simple_switch_grpc`）；sha256[:16] `3ff54b5c1901c9d3`（`SOL:24`） | bmv2-fast `3ff54b5c`；p4c `226f3f66df515c9e`（`SOL:25`） |
| convert.py「12 files」 | `SOL:80`（`files : 12`，列在 81-92） | `tools/p4_exercise/convert.py` |
| pre-flight「23 PASS · 0 FAIL」 | `SOL:104-137` 的列數（腳本數：23 PASS、8 INFO、0 FAIL；`SOL:137` `PASS -- every check passed`） | `tools/p4_exercise/preflight.py` |
| ndt claim「45-min lease」 | `SOL:822`（`ok  lab claimed by orch-0927 for 45m`） | — |
| ndt up「bmv2 × 4」 | `SOL:198`（`4 switches up after 6s`） | — |
| 圖例「build/firewall.json」（s1，藍框）／「build/basic.json」（s2–s4） | `SOL:78`（`pipelines : s1=build/firewall.json, s2=build/basic.json, s3=…, s4=build/basic.json`）；兩個 p4info：`SOL:61`（s1 `ef7561c073ee3b7f`）、`SOL:62-64`（s2–s4 `9213871cee36bd93`），與 pre-flight `SOL:124-127` 逐台相同；骨架臂同一組（`SK:72-75`、`SK:89`） | — |
| table entries「28/28 applied · 0 failed」 | `SOL:61-64`（`recorded=13/5/5/5`，applied 同數、failed 0，腳本加總）；對帳：`SOL:129`（pre-flight `28 entries across 4 switch(es)`）、`SOL:218`（`ndt up` 的 `28/28 applied across 4 switch(es) (they do not all carry the same count)`——各台不同數時 ndt 印總數，🟠 `K/tools/test_workflow/ndt:3975-3983` at `5dc7fc9a`） | — |
| 拓樸連線（s1、s2 為葉、s3、s4 為脊；h1/h2 掛 s1、h3/h4 掛 s2） | 🟠 `TUT/exercises/firewall/pod-topo/topology.json`；對帳 🟢 `SOL:49-52`（4 hosts、4 switches、8 links）、`SOL:201-204`（`ndt up` 列出的 4 條交換機間鏈路）、`SOLD/link_usage/twin_integral.txt:1-12`（介面種類） | tutorials c80d83e |
| 標題「TCP iperf 3 s each way」 | `SOL:518`、`SOL:544`（`iperf -c … -t 3`）；`SOL:524`、`SOL:550`（`TCP port 5001`） | — |
| 解答臂「TCP h1 → h3 · 262 MBytes」 | `SOL:529`（client `0.0000-3.0105 sec 262 MBytes 731 Mbits/sec`）、`SOL:538`（server 262 MBytes）；`SOLD/driver-iperf-h1-to-h3.log:7` | — |
| 解答臂「TCP h3 → h1 · timed out」 | `SOL:553`（`tcp connect failed: Connection timed out`）；server 沒有傳輸列（`SOL:556-562`，`(client killed after 25s)`） | — |
| 骨架臂「254 MBytes」「248 MBytes」 | `SK:540`／`SK:549`（h1→h3 client／server 254）；`SK:566`／`SK:575`（h3→h1 client／server 248） | — |
| 「ping, 12 pairs · 12/12 at 0% loss」 | `SOL:512`、`SK:523`（`0% (12/12 pairs at 0%, 0 lossy)`，`ping -c 5 -W 2` 每一個有序對） | — |
| 「PASS (4/4)」「PASS (3/3)」 | `SOL:18`、§5 `SOL:706-709`；`SK:18`、§5 `SK:700-702` | — |
| TWIN「UDP iperf h1 → h4」 | `SOL:575`（`h1 -> h4 (10.0.4.4), iperf -u -b 2M -t 16 -l 1200`） | — |
| TWIN「> 0 on s1-eth4, s2-eth2, s4-eth1 · 0 on the other 9 ports」 | `SOLD/link_usage/twin_integral.txt:4`（s1-eth4 23,520,598 bit）、`:6`（s2-eth2 40,048,419 bit）、`:11`（s4-eth1 35,598,645.75 bit），其餘 9 行 0.000；`:13`（`samples=64 span=16s`）；報告 `SOL:576-591`（`LINK_USAGE … primary=3 minor=0 rc=0`），腳本斷言兩處數字相同 | — |
| ndt down「verified clean」 | `SOL:677-685`；`SOL:1042`（`ndt down rc=0`）；骨架 `SK:671-679`、`SK:1032` | — |
| ndt release「released」 | `SOL:699`；`SOL:1049`（`ndt release rc=0`）；骨架 `SK:693`、`SK:1039` | — |

讀到的 raw 與 **audit-raw `797c34ab`** 逐檔 blob 相同：`K/scratch/overnight-2026-09-05/logs/slides930/e2e-figs-audit-raw-check-20260930T0525Z.log`（三張圖合計 22/22）。

## 可信度

**OBSERVED（跑過）**
- 上表每一個數字：12、23／0、45、4、28/28／0、262／254／248 MBytes、timed out、12/12、三個 verdict、twin 的 3 個 > 0 與 9 個 0。
- 防火牆只在解答臂擋、只擋一個方向：解答臂 h3→h1 的 TCP 連不上，h1→h3 過；同一臂的 ping 全通——擋的是 TCP 不是 fabric。骨架臂兩個方向都過，所以解答臂的「擋」是它的程式做的，不是 fabric 本來就不通。
- 兩臂 s1 都跑 firewall、s2–s4 都跑 basic，p4info 兩組一樣（腳本斷言兩臂相同）；差的只是 s1 的程式是解答還是骨架。

**READ（讀碼或讀檔，沒有執行）**
- 圖左連線畫自 tutorials 的 `pod-topo/topology.json`；腳本拿它對 `ndt up` 印出的 4 條鏈路、arm report 的數目、`twin_integral.txt` 的介面種類，全部一致才畫。
- 為什麼 ping 不受影響：driver 判定表依據欄 `ICMP has no TCP header, so check_ports never fires`（`SOL:708`，標【源碼推導，未執行】；`TUT/exercises/firewall/solution/firewall.p4:177`、`:195` 的 `check_ports`）。
- 為什麼 h3→h1 被擋：`SOL:707` 依據欄 `solution/firewall.p4:212-219 drop()s direction-1 packets whose bloom cells are unset`（【源碼推導，未執行】）。
- `ndt up` 那行 `28/28 … across` 是總數：`ndt:3975-3983`。`table_entries` 是 proxy 的自述計數。

**INFERRED**
- 無。

## 圖怎麼讀

- 上排八格＝解答臂的步驟（骨架臂同樣八步，前幾步數字相同：`SK:91` 12 files、`SK:229` 28/28）。
- 左下「NDT UP」：proxy 經 P4Runtime 把 28 條表項寫進 4 台；藍框的 s1 跑 `build/firewall.json`，黑框的 s2–s4 跑 `build/basic.json`，都是 exercise 自己編的程式。
- 右上：列＝測試、欄＝兩臂；綠＝過、紅＝沒過，格內是 raw 的值。骨架臂全綠是它該有的樣子（紅臂）。
- 右下「TWIN LINK READING」：twin 在解答臂 fabric 上的鏈路讀數，驗的是一般 IPv4 的 UDP iperf（h1→h4 會經過跑防火牆的 s1）。

## 已知但書

- ❌ 不說「NDTwin 能操作外來 P4 程式」或「NDTwin 觀測得到防火牆的判斷」。twin 那一格只驗過一般 IPv4 UDP iperf 的鏈路讀數；TCP 的擋與不擋是 iperf 在主機上看到的。firewall 本身沒有自訂標頭，「IPv4 only」在這裡就是它的全部流量種類，照 T7 的口徑標。
- twin 的積分是 1/256 取樣的估計：三個 on-path 介面的真實 tx 位元組差都是約 4.35 MB（`SOLD/link_usage/onpath.txt:1-3`，≈ 34.8 Mbit），twin 積分 23.5／40.0／35.6 Mbit——取樣的散佈，所以圖上只寫「> 0」與「0」。off-path 門檻 3,072,000 bit（`SOL:580`）。
- G1 的 iperf 是 UDP、方向 h1→h4（內往外），防火牆不擋；它量的是 fabric 的鏈路讀數，不是防火牆行為。骨架臂的 G1 沒跑（`SK:578`，NOT RUN）。
- **髒 checkout**：`SOL:448` 起的 code 行 `5dc7fc9a +95`，3 個會改行為的檔同 fig_t6。圖上沒有印 sha。
- arm report §1 的「此處用的是 `/usr/local/bin` 那顆」是舊樣板字（`SOL:27`），以 `SOL:199` 的執行檔為準。
- `ndt down` 的 [1/3] 曾印「stack.sh down exited 1」（`SOL:653`），[3/3] 後 verify clean、rc 0。
- 心跳在這一臂有跑（`SOL:206-207`），這頁不講它。

## 重生指令

```
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/p4-tutorials"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_exercise_e2e_figs.py
```

同一支腳本也產 fig_t6b（basic_tunnel）、fig_t6d（p4runtime）。

- **紅檢**：`K/scratch/overnight-2026-09-05/logs/slides930/make_exercise_e2e_figs-redcheck-20260930T0525Z.log`：133/133 以自己的 `[TAG]` 停下、對照組綠且 PNG 與資料夾逐位元相同；唯一到不了的是 `[TITLE]`（常數）。本圖專屬的停止點：FW_VT、FW_PINGALL（3）、FW_IPERF_STEPS、FW_IPERF（4）、FW_IPERF_TCP、FW_IPERF_SIDES、FW_PIPES（2）、FW_SHAS（2）、FW_SOL、FW_SK，另加共用的 T06_*、ARM_*、SS_*、ENTRIES_*、TOPO_*、G1_*、TWIN_*。
- **fig_t6 沒被動到**：`fig_t6-rerender-check-20260930T0523Z.log`（PNG 逐位元相同；SVG／PDF 只差日期與隨機 clip id）。
- 產圖紀錄：`make_exercise_e2e_figs-run-20260930T0525Z.log`。

最後產出：2026-09-30T05:25Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 sha256 `55bba40bc0a41c99…`；PNG sha256 `b7fa9fbbb3ad0d60…`（300 dpi）、`3215d86c86a2188b…`（`_hires`，500 dpi）。
