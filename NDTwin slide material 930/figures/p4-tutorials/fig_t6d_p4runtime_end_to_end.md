# fig_t6d_p4runtime_end_to_end —— 一支 exercise 從頭到尾：p4runtime 在 NDTwin fabric 上

[Co-developed with claude code -- Adam]

圖上標題：`p4runtime, end to end on the NDTwin fabric`（42 字元）。版型、色票、畫圖 helper 沿用 T4 的 `fig_t6_multicast_end_to_end`（從 `make_exercise_path_figs.py` import，那支檔一個字沒改）。
和 T4 的差別：上排仍是八格，但這支的關鍵一步是 exercise 自己的控制器，所以 T4 的「arm report」格換成「controller」（接在 `ndt up` 之後、封包測試之前，正是它在 driver 裡的順序）；左下面板因此同時接 `ndt up` 與 `controller` 兩格。

## 一句話

09-27 那一輪（T06，code `5dc7fc9a +95`，髒 checkout）裡的 p4runtime：package 宣告 **external 控制面**——`ndt up` 起 3 台 bmv2、一個程式都不載，proxy 一條表項都不寫；
exercise 自己的 `solution/mycontroller.py` 經 **NDTwin 的 adapter**（`:50051 → :30051`、`:50052 → :30052`）用 P4Runtime 把 `build/advanced_tunnel.json` 裝到 s1、s2（s3 沒碰），再寫 6 條 tunnel 規則；
封包測試：h1 ping h2，解答臂 5/5（**PASS (5/5)**），骨架臂 transit 規則還是 TODO、0/5（**PASS (4/4)**，紅臂）。
twin 那一格：解答臂 h1→h2 的 UDP iperf 期間，s1-eth2 比 s2-eth1 多送 14,000 B、twin 在 s1-eth2 的積分 > 0、s1 的 tunnel counter 100 讀到 3,505 個封包；**14,000 B ＝ 3,500 datagram × 4 B tunnel 標頭，所以那些多出來的位元組是 0x1212 幀——這一步是推論（INFERRED，沒抓 pcap）**。

## 資料來源

K ＝ `/home/adam/Desktop/NDTwin-Kernel`；R ＝ `K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/runs`；
T06 ＝ `K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/2026-09-27T074635Z_06_thirteen/00_table.tsv`；
SOL ＝ `R/2026-09-27T081205Z_p4runtime_solution_ndtwin.md`（同名目錄 SOLD）；SK ＝ `R/2026-09-27T081131Z_p4runtime_skeleton_ndtwin.md`（同名目錄 SKD）；
CS ＝ `SOLD/driver-controller-p4runtime.log`；CK ＝ `SKD/driver-controller-p4runtime.log`；
TUT ＝ `/home/adam/tutorials`（c80d83e，這三支 exercise 目錄底下 0 個未提交修改）。

| 用途（圖上的值） | 檔（path:line） | commit／binary |
|---|---|---|
| 兩臂在 T06 的列 | `T06:24`（skeleton rc 0 `PASS (4/4)`）、`T06:25`（solution rc 0 `PASS (5/5)`） | — |
| run 站的 commit | `SOL:459`、`SK:459`（`code 5dc7fc9a +95 file(s) with uncommitted changes`） | trunk `5dc7fc9a`，工作樹 +95 未提交檔 |
| bmv2 執行檔 | `SOL:189`（`running binary: /usr/local/bmv2-fast/bin/simple_switch_grpc`）；sha256[:16] `3ff54b5c1901c9d3`（`SOL:24`） | bmv2-fast `3ff54b5c`；p4c `226f3f66df515c9e`（`SOL:25`） |
| convert.py「6 files」 | `SOL:79`（`files : 6`，列在 80-85）；`SOL:76`（`control plane : external`） | `tools/p4_exercise/convert.py` |
| pre-flight「21 PASS · 0 FAIL」 | `SOL:97-128` 的列數（腳本數：21 PASS、8 INFO、0 FAIL；`SOL:128`） | `tools/p4_exercise/preflight.py` |
| ndt claim「45-min lease」 | `SOL:966` | — |
| ndt up「bmv2 × 3」、一個程式都沒載 | `SOL:188`（`3 switches up after 6s`）；`SOL:201`（`proxy: 3/3 switches answered the liveness probe (no pipeline loaded on any of them, by design)`） | — |
| 「P4 proxy · writes nothing」 | `SOL:270`（switch_state：`its own controller owns every table and this proxy writes nothing`）；`SOL:58`（`control_plane.mode external`）；`SOL:61-63`（每台 `entries recorded=0 applied=0 failed=0`） | — |
| 「NDTwin's entries · 0」 | `SOL:61-63` 加總 | — |
| 「mycontroller.py · the exercise's own」 | `CS:3`（`[adapter] running /home/adam/tutorials/exercises/p4runtime/solution/mycontroller.py`）；骨架臂 `CK:3` 跑的是骨架的 `mycontroller.py` | tutorials c80d83e |
| 「adapter · :50051 → :30051」 | `CS:4`（`s1: 127.0.0.1:50051 device_id=0 -> localhost:30051 device_id=1`）、`CS:5`（s2 `50052 → 30052`）；adapter＝`K/tools/p4_exercise/run_external_controller.py`（`SOL:522` 的指令） | — |
| 圖例「build/advanced_tunnel.json」：s1、s2 藍框 | `CS:6-7`（`Installed P4 Program using SetForwardingPipelineConfig on s1`／`s2`）；`SOL:77`（package 的 pipeline 名） | — |
| 圖例「no program」：s3 虛線框 | `CS:4-7` 只有 s1、s2（adapter 沒對應 s3、程式只裝在 s1、s2）＋`SOL:201`（`ndt up` 什麼都不載）；判定表 `SOL:860`（`switches the controller programmed [1, 2]`） | — |
| 「tunnel rules · 6 installed」、上排「6 tunnel rules」 | `CS:8-13`（ingress／transit／egress 各在 s1、s2 上一條） | — |
| 拓樸連線（三角形） | 🟠 `TUT/exercises/p4runtime/topology.json`；對帳 🟢 `SOL:49-52`（3 hosts、3 switches、6 links）、`SOLD/link_usage/twin_integral.txt:1-9`（介面種類）。**external fabric 不跑心跳，arm report 裡沒有 `ndt up` 印出的鏈路清單可對**（basic_tunnel、firewall 有） | tutorials c80d83e |
| 解答臂「transit rule · on 2 switches」 | `CS:9`、`CS:12`（`Installed transit tunnel rule on s1`／`s2`）；判定表 `SOL:861` | — |
| 骨架臂「transit rule · TODO」 | `CK:9`、`CK:12`（`TODO Install transit tunnel rule`）；判定表 `SK:770` | — |
| 「h1 ping h2, 5 packets」「replies 5/5」 | `SOL:584`（`ping -c 5 -W 2 10.0.2.2`）、`SOL:596`（`5 packets transmitted, 5 received, 0% packet loss`）；判定表 `SOL:862` | — |
| 「replies 0/5」 | `SK:581`（`5 packets transmitted, 0 received, 100% packet loss`）；判定表 `SK:771` | — |
| 「PASS (5/5)」「PASS (4/4)」 | `SOL:18`、§5 `SOL:859-863`；`SK:18`、§5 `SK:768-771` | — |
| TWIN「UDP iperf h1 → h2」 | `SOL:610`（`h1 -> h2 (10.0.2.2), iperf -u -b 2M -t 16 -l 1200`）；`SOLD/link_usage/iperf_client.txt:9`（`Sent 3500 datagrams`） | — |
| TWIN「s1-eth2 − s2-eth1 · +14,000 B」 | `SOLD/link_usage/onpath.txt:1`（s1-eth2 4,361,273 B）、`:2`（s2-eth1 4,347,273 B）——iperf 期間每個介面的 **tx_bytes 差**（`/proc/net/dev`，🟠 `K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/_common.sh:679-681`、`:751`、`:858-886`） | — |
| TWIN「twin on s1-eth2 · > 0」 | `SOLD/link_usage/twin_integral.txt:2`（s1-eth2 29,338,582 bit）；其餘 7 個 off-path 介面 0.000；`:10`（`samples=64 span=16s`）；報告 `SOL:611-623`（`primary=s1-eth2 s2-eth1`、`LINK_USAGE … primary=2 minor=0 rc=0`） | — |
| TWIN「s1 tunnel counter 100 · 3,505 pkts」 | `CS:121-122`（最後一次讀：`s1 MyIngress.ingressTunnelCounter 100: 3505 packets (4347490 bytes)`）——exercise 自己的控制器讀它自己的 counter | — |
| TWIN INFERRED「= 3,500 × 4 B: the 0x1212 frames」 | 3,500 ＝ `iperf_client.txt:9`；4 B ＝ 🟠 `TUT/exercises/p4runtime/advanced_tunnel.p4:25-28`（`header myTunnel_t { bit<16> proto_id; bit<16> dst_id; }`）；0x1212 ＝ 🟠 同檔 `:7`（`TYPE_MYTUNNEL = 0x1212`） | tutorials c80d83e |
| ndt down「verified clean」 | `SOL:828-836`；`SOL:1197`（`ndt down rc=0`）；骨架 `SK:737-745`、`SK:1079` | — |
| ndt release「released」 | `SOL:852`；`SOL:1204`（`ndt release rc=0`）；骨架 `SK:761`、`SK:1086` | — |

讀到的 raw 與 **audit-raw `797c34ab`** 逐檔 blob 相同：`K/scratch/overnight-2026-09-05/logs/slides930/e2e-figs-audit-raw-check-20260930T0525Z.log`（三張圖合計 22/22）。

## 可信度

**OBSERVED（跑過）**
- 上表每一個數字：6、21／0、45、3、0 條 NDTwin 表項、adapter 的兩組對應、程式裝在 s1 與 s2、6 條 tunnel 規則、transit 規則 2 條／TODO 2 行、5/5 與 0/5、兩個 verdict、14,000 B（兩個 tx 位元組差相減）、twin 在 s1-eth2 的積分 > 0（其餘 off-path 介面 0）、counter 3,505。
- **NDTwin 在這支 exercise 上做的事**：起 fabric（3 台空的 bmv2）、proxy 不寫任何東西、提供 adapter 讓 exercise 自己的控制器接上 NDTwin 的 gRPC 埠；程式與規則全是那支控制器寫的。
- 骨架臂：同一支 adapter、同樣裝了程式與 ingress／egress 規則（`CK:6-13`），只少了學生該寫的 transit 規則，所以 ping 全丟——紅臂照預期。它的 counter 顯示封包進了 s1 的 tunnel 卻沒從 s2 出來（`CK:58-59`：ingress 100＝5、egress 100＝0；圖上沒放）。
- 控制器讀回的表（`CS:15-23`，控制器自己讀交換機的輸出）：s1 的 `ipv4_lpm` 把 10.0.2.2/32 送進 `myTunnel_ingress(dst_id 100)`、`myTunnel_exact 100 → myTunnel_forward port 2`；s2 的 `myTunnel_exact 100 → myTunnel_egress(h2 的 MAC, port 1)`。

**READ（讀碼或讀檔，沒有執行）**
- 圖左連線畫自 tutorials 的 `topology.json`，只和 arm report 的數目與 `twin_integral.txt` 的介面種類對過（這支沒有 `ndt up` 的鏈路清單，見上表）。
- tunnel 標頭 4 B、etherType 0x1212：`advanced_tunnel.p4:7`、`:25-28`；s2 出口把標頭拿掉：`advanced_tunnel.p4:135-139`（`myTunnel_egress` 裡 `hdr.myTunnel.setInvalid()`）。
- `onpath.txt` 是 tx_bytes 差：`live-p1/_common.sh:679-681`、`:751`。

**INFERRED（圖上以灰底「INFERRED」標出的那一行）**
- 「s1-eth2 多出來的 14,000 B 就是 0x1212 幀的 tunnel 標頭」：14,000 ＝ 3,500 × 4 **恰好相等**（腳本斷言），加上控制器讀回的表說 10.0.2.2 的流量在 s1 進 tunnel、從 port 2（s1-eth2）出去、在 s2 拿掉標頭再送 h2（s2-eth1）——但**沒有抓 pcap**，所以是推論。
- 因此「twin 在 s1-eth2 的積分 > 0」讀的那條鏈路上，iperf 的幀帶著 0x1212 標頭——也是推論（twin > 0 本身是觀測）。❌ 不說「NDTwin 觀測得到 0x1212 標頭」：twin 讀的是介面上的取樣流量，這裡只證明它在那條鏈路上讀到了流量。
- counter 3,505 ＝ ping 的 5 個（iperf 前那次讀：`CS:68`，5 packets）＋iperf 的 3,500 個：數字吻合，對應關係是推論，圖上只印 3,505 這個觀測值。

## 圖怎麼讀

- 上排八格＝解答臂的步驟；「controller」取代 T4 的「arm report」格（理由見開頭）。
- 左下：上方 proxy「writes nothing」；下方 exercise 的 `mycontroller.py` → NDTwin 的 adapter（藍底，NDTwin 做的東西）→ P4Runtime → fabric。藍框＝裝了 `build/advanced_tunnel.json` 的交換機，虛線＝沒有程式。左下角兩個計數：控制器的 6 條規則、NDTwin 的 0 條表項。
- 右上：列＝transit 規則、ping 回覆；欄＝兩臂；綠＝有、紅＝沒有。
- 右下：twin 那一格——上三行是觀測，最下一行灰底 INFERRED 是推論。

## 已知但書

- ❌ **不說「NDTwin 能操作外來 P4 程式」**（模板 §0 規則 8）。這一頁能講的是：exercise 自己的控制器經 NDTwin 的 adapter 接上 NDTwin 起的 fabric、轉得動；NDTwin 的 proxy 在這支上不寫任何東西。
- ❌ 不說「NDTwin 觀測得到 0x1212」。只有 p4runtime 有 twin 讀到帶 tunnel 標頭的那條鏈路的**位元組證據**，而且那一步是 INFERRED（同 T7 的 p4runtime 那格）。
- twin 積分是 1/256 取樣的估計：s1-eth2 的 tx 差 4,361,273 B（≈ 34.89 Mbit），twin 積分 29.34 Mbit；s2-eth1 的 tx 差 ≈ 34.78 Mbit，twin 21.62 Mbit——所以圖上只寫「> 0」。off-path 門檻 3,072,000 bit（`SOL:614`）。
- 同一段時間 s2 的 ingress counter 200（反方向）從 5 變 7（`CS:118`→`CS:124`），推測是 iperf 的回報封包；圖上沒放。
- `ndt up` 時 kernel 的交換機存活讀數是 0/3 up（`SOL:203-207`，external fabric 在控制器載入程式之前本來就是這樣）；控制器跑完之後的存活讀數**這份 arm report 沒有抓**，所以圖上不談 kernel 的 up/down。
- external fabric 不跑心跳（switch_state `heartbeat: null`，`SOL:265`）；圖左的鏈路只來自 topology.json（READ）。
- **髒 checkout**：`SOL:459` 起的 code 行 `5dc7fc9a +95`，3 個會改行為的檔同 fig_t6。圖上沒有印 sha。
- arm report §1 的「此處用的是 `/usr/local/bin` 那顆」是舊樣板字（`SOL:27`），以 `SOL:189` 的執行檔為準。
- `ndt down` 的 [1/3] 曾印「stack.sh down exited 1」（`SOL:806`），[3/3] 後 verify clean、rc 0。

## 重生指令

```
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/p4-tutorials"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_exercise_e2e_figs.py
```

同一支腳本也產 fig_t6b（basic_tunnel）、fig_t6c（firewall）。

- **紅檢**：`K/scratch/overnight-2026-09-05/logs/slides930/make_exercise_e2e_figs-redcheck-20260930T0525Z.log`：133/133 以自己的 `[TAG]` 停下、對照組綠且 PNG 與資料夾逐位元相同；唯一到不了的是 `[TITLE]`（常數）。本圖專屬的停止點：P4R_VT、P4R_MODE、P4R_NDTWIN_ENTRIES、P4R_EMPTY、P4R_WRITES、P4R_LOG、P4R_ADAPTER（5）、P4R_SOL_TRANSIT、P4R_SK_TRANSIT、P4R_COUNTER（3）、P4R_PING（2）、P4R_PING_RESULT、P4R_PRIMARY、P4R_BYTES（5，含「位元組差 ≠ datagram × 標頭」）、P4R_HEADER（3），另加共用的 T06_*、ARM_*、SS_*、TOPO_*、G1_*、TWIN_*。
- **fig_t6 沒被動到**：`fig_t6-rerender-check-20260930T0523Z.log`（PNG 逐位元相同；SVG／PDF 只差日期與隨機 clip id）。
- 產圖紀錄：`make_exercise_e2e_figs-run-20260930T0525Z.log`。

最後產出：2026-09-30T05:25Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 sha256 `55bba40bc0a41c99…`；PNG sha256 `87fdeca1ac1965ef…`（300 dpi）、`7ee68dfe57511b09…`（`_hires`，500 dpi）。
