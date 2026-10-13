# fig_t6b_basic_tunnel_end_to_end —— 一支 exercise 從頭到尾：basic_tunnel 在 NDTwin fabric 上

[Co-developed with claude code -- Adam]

圖上標題：`basic_tunnel, end to end on the NDTwin fabric`（45 字元，恰好到上限）。版型、色票、畫圖 helper 全部沿用 T4 的 `fig_t6_multicast_end_to_end`（從 `make_exercise_path_figs.py` import，那支檔一個字沒改）。

## 一句話

09-27 那一輪（T06，code `5dc7fc9a +95`，髒 checkout）裡的 basic_tunnel：解答臂 convert 出 9 個檔、pre-flight 23 PASS／0 FAIL、claim 45 分鐘、`ndt up` 起 3 台 bmv2 都跑 exercise 自己的 `build/basic_tunnel.json`、proxy 經 P4Runtime 寫進 18/18 條表項（每台 6 條，0 失敗）；
封包測試：h1 對 **h2 的 IP 10.0.2.2** 送兩個 0x1212 tunnel 幀，`--dst_id 2` 只有 h2 收到、`--dst_id 3` 只有 h3 收到（**PASS (4/4)**）；骨架臂在 pre-flight 就被擋下（第一個問題 `MyIngress.myTunnel_exact` 不在它的 p4info），沒有 `ndt up`（**RED ARM (1/1)**，照設計）。
twin 那一格：解答臂的鏈路讀數只驗過一般 IPv4 的 UDP iperf（h1→h3），路徑上 2 個介面 > 0、其他 7 個 0——**IPv4 only**。

## 資料來源

K ＝ `/home/adam/Desktop/NDTwin-Kernel`；R ＝ `K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/runs`；
T06 ＝ `K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/2026-09-27T074635Z_06_thirteen/00_table.tsv`；
SOL ＝ `R/2026-09-27T075455Z_basic_tunnel_solution_ndtwin.md`（同名目錄 SOLD）；SK ＝ `R/2026-09-27T075454Z_basic_tunnel_skeleton_ndtwin.md`；
TUT ＝ `/home/adam/tutorials`（c80d83e，這三支 exercise 目錄底下 0 個未提交修改）。

| 用途（圖上的值） | 檔（path:line） | commit／binary |
|---|---|---|
| 兩臂在 T06 的列 | `T06:10`（skeleton rc 1 `RED ARM (1/1): the skeleton does not get past the control plane, by design`）、`T06:11`（solution rc 0 `PASS (4/4)`） | — |
| run 站的 commit | `SOL:439`、`SOL:998`（`code 5dc7fc9a +95 file(s) with uncommitted changes`）；骨架臂沒走到 `ndt status`，沒有 code 行 | trunk `5dc7fc9a`，工作樹 +95 未提交檔 |
| bmv2 執行檔 | `SOL:192`（`running binary: /usr/local/bmv2-fast/bin/simple_switch_grpc`）；sha256[:16] `3ff54b5c1901c9d3`（`SOL:24`、`SOL:1037`） | bmv2-fast `3ff54b5c`；p4c `226f3f66df515c9e`（`SOL:25`） |
| convert.py「9 files」 | `SOL:77`（`files : 9`，列在 78-86） | `tools/p4_exercise/convert.py` |
| pre-flight「23 PASS · 0 FAIL」 | `SOL:98-130` 的列數（腳本數：23 PASS、7 INFO、0 FAIL；`SOL:130` `PASS -- every check passed`）；腳本斷言 N2 與 transcript 那份 pre-flight 的狀態／標籤一字不差 | `tools/p4_exercise/preflight.py` |
| ndt claim「45-min lease」 | `SOL:942`（`ok  lab claimed by orch-0927 for 45m`） | — |
| ndt up「bmv2 × 3」、三台都跑 `build/basic_tunnel.json` | `SOL:191`（`3 switches up after 6s`）、`SOL:75`（`pipelines : s1=…, s2=…, s3=build/basic_tunnel.json`）、`SOL:59-61`（`ndtwin=False`，p4info `e08bce0024fc7df2`） | — |
| table entries「18/18 applied · 0 failed」 | `SOL:59-61`（每台 `recorded=6 applied=6 failed=0`，腳本加總）；對帳：`SOL:122`（pre-flight `18 entries across 3 switch(es)`）、`SOL:210`（`ndt up` 的 `6/6 applied on 3 switch(es)`——每台都一樣時 ndt 印的是**每台**那一對，🟠 `K/tools/test_workflow/ndt:3975-3983` at `5dc7fc9a`） | — |
| 拓樸連線（三角形、h1/h2/h3 各掛一台） | 🟠 `TUT/exercises/basic_tunnel/topology.json`（hosts、6 條 links）；對帳 🟢 `SOL:47-50`（3 hosts、3 switches、6 links）、`SOL:194-196`（`ndt up` 列出的 3 條交換機間鏈路）、`SOLD/link_usage/twin_integral.txt:1-9`（每個介面是 host 還是 switch 端） | tutorials c80d83e |
| 封包測試的 IP「10.0.2.2, h2's IP」 | `SOL:501`、`SOL:602`（兩次都是 `send.py 10.0.2.2 … --dst_id N`）；`SOL:1040`（`hosts: h1=10.0.1.1, h2=10.0.2.2, h3=10.0.3.3`） | — |
| 「2 tunnel frames」 | `SOL:505`、`SOL:606`（`sending on interface eth0 to dst_id 2`／`3`）；兩幀都是 `type = 0x1212`、帶 `MyTunnel`（`SOL:509-512`、`SOL:610-613`） | — |
| 2×2 格：dst_id 2 → h2 收到、h3 沒有 | `SOL:551`、`:558`（h2 `got a packet`，`dst_id = 2`）；`SOL:596`（h3 只有 `sniffing on eth0`）；對帳 `SOLD/driver-h2-1-receive.log:2`、`driver-h3-1-receive.log:1` | — |
| 2×2 格：dst_id 3 → h3 收到、h2 沒有 | `SOL:662`、`:669`（h3 `got a packet`，`dst_id = 3`）；`SOL:651`（h2 只有 `sniffing on eth0`）；對帳 `SOLD/driver-h3-2-receive.log:2`、`driver-h2-2-receive.log:1` | — |
| 解答臂「PASS (4/4)」 | `SOL:18`；§5 判定表 `SOL:832-835`（4 列全 PASS） | — |
| 骨架臂「pre-flight FAIL · MyIngress.myTunnel_exact · not in its p4info」 | `SK:113`（`FAIL entries match p4info 9 problem(s); first: s1 entry 3: table 'MyIngress.myTunnel_exact' is not in the p4info (it has: MyIngress.ipv4_lpm)`）；`SK:127`（`FAIL -- 7 check(s) failed`＝1 個 check 的 7 行 FAIL，見 T5）；`SK:239`（`pre-flight FAILED (rc 1)`）；SK 裡沒有 `ndt up` | — |
| 骨架臂「RED ARM (1/1)」 | `SK:18`；§5 `SK:134` | — |
| TWIN「UDP iperf h1 → h3」 | `SOL:710`（`h1 -> h3 (10.0.3.3), iperf -u -b 2M -t 16 -l 1200`） | — |
| TWIN「> 0 on s1-eth3, s3-eth1 · 0 on the other 7 ports」 | `SOLD/link_usage/twin_integral.txt:3`（s1-eth3 35,604,357.75 bit）、`:7`（s3-eth1 35,603,586.75 bit）、其餘 7 行 0.000；`:10`（`samples=64 span=17s`）；報告 `SOL:711-723`（primary 列、off-path 列、`LINK_USAGE … primary=2 minor=0 rc=0`），腳本斷言兩處數字相同 | — |
| ndt down「verified clean」 | `SOL:801-809`（`verify clean` … `clean`）；`SOL:1279`（`ndt down rc=0`） | — |
| ndt release「released」 | `SOL:825`（`ok  lab released`）；`SOL:1286`（`ndt release rc=0`） | — |

讀到的 22 個 raw 檔（三張圖合計：T06、6 份 arm report、link_usage、driver log）與 **audit-raw `797c34ab`** 逐檔 blob 相同：`K/scratch/overnight-2026-09-05/logs/slides930/e2e-figs-audit-raw-check-20260930T0525Z.log`（22/22；本機 commit 物件，公開與否依模板 §0 規則 5，這次沒重驗）。

## 可信度

**OBSERVED（跑過，arm report 與同名目錄裡的 raw）**
- 上表每一個數字：9、23／0、45、3、18/18／0、2 個幀、2×2 的四格、兩個 verdict、骨架的 FAIL 列與 rc 1、twin 的 2 個 > 0 與 7 個 0。
- 同一個目的 IP（10.0.2.2，h2 的）：`--dst_id 2` 落在 h2、`--dst_id 3` 落在 h3——tunnel 標頭蓋過 IP 目的地（README 第 6 步說的事，這裡跑出來了）。每個收到的幀裡的 `dst_id` 與送出的一致（腳本逐幀核）。
- 骨架臂：pre-flight 擋下、rc 1，transcript 裡沒有 `ndt up`；這是 exercise 設計好的紅臂（骨架的 `sN-runtime.json` 寫了它自己沒有的表）。

**READ（讀碼或讀檔，沒有執行）**
- 圖左的連線（誰連誰、哪台掛哪個 host）畫自 tutorials 的 `topology.json`；腳本拿它對 `ndt up` 印出的 3 條交換機間鏈路、arm report 的 hosts／switches／links 數、`twin_integral.txt` 的介面種類，全部一致才畫。
- `ndt up` 那行 `6/6 applied on 3 switch(es)` 是每台的數字：`ndt:3975-3983`（每台同數用 "on"、否則印總數用 "across"）。
- `table_entries` 是 proxy 自己回報的計數（`GET /p4/switch_state`），不是從交換機讀回來的。

**INFERRED**
- 無。圖上沒有推論出來的值。

## 圖怎麼讀

- 上排八格＝解答臂從頭到尾的步驟（骨架臂只走到 pre-flight）。
- 左下「NDT UP」：proxy 經 P4Runtime 把 package 的 18 條表項寫進 s1–s3；三台都跑 exercise 自己編的 `build/basic_tunnel.json`，不是 NDTwin 的程式。
- 右上兩臂：解答臂的 2×2——列＝送出的 `dst_id`、欄＝哪台主機的 sniffer；綠＝收到、白＝沒收到。骨架臂沒有封包測試，紅框是它在 pre-flight 的那一列 FAIL。
- 右下「TWIN LINK READING」：twin 在解答臂 fabric 上的鏈路讀數，驗的是一般 IPv4 的 UDP iperf。琥珀色「IPv4 only」與 T7（`fig_t9_custom_headers`）的同一格一致。

## 已知但書

- ❌ **不說「NDTwin 觀測得到 0x1212」**。twin 那一格只驗過一般 IPv4 iperf（h1→h3 不帶 tunnel 標頭，走 `ipv4_lpm`）；兩個 tunnel 幀是 exercise 自己的 `send.py`／`receive.py` 在主機上送收的。只能說 basic_tunnel 在 NDTwin fabric 上**轉得動（forward）**。
- twin 的積分是 1/256 取樣的估計：s1-eth3 的真實 tx 位元組差是 4,345,998 B（`SOLD/link_usage/onpath.txt:1`，≈ 34.77 Mbit），twin 積分 35.60 Mbit；所以圖上只寫「> 0」與「0」，不印數值。off-path 門檻 3,072,000 bit（`SOL:714`），7 個 off-path 介面都是 0.000。
- **髒 checkout**：`SOL:439-443` 的 code 行是 `5dc7fc9a +95 file(s) with uncommitted changes`，其中 3 個會改行為（`p4_proxy/mininet/host_count_override`、`p4_proxy/mininet/app_package_override`、`tools/remote-lab/dorm_lab/`）。圖上沒有印 sha。
- arm report §1 自相矛盾：`SOL:24` 說跑的是 bmv2-fast（`3ff54b5c`），同節 `SOL:27` 的附註寫「此處用的是 `/usr/local/bin` 那顆」——那句是 driver 的舊樣板字，以 `ndt status` 與 `ndt up` 印的執行檔為準（與 fig_t6 同一個但書）。
- `ndt down` 的 [1/3] 曾印「stack.sh down exited 1」（6 個埠還在聽），[3/3] 清掉後 verify clean；最後 rc 0（`SOL:777-812`、`SOL:1279`）。
- 骨架臂在 T06 的 rc 是 1——那是它「被擋下」的正確結果，不是 driver 失敗。T5（`fig_t7_preflight_checks`）的紅框是同一列。
- 心跳在這一臂有跑（`SOL:193-199`），這頁不講它。

## 重生指令

```
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/p4-tutorials"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_exercise_e2e_figs.py
```

同一支腳本也產 fig_t6c（firewall）、fig_t6d（p4runtime）。

- **紅檢**：`K/scratch/overnight-2026-09-05/logs/slides930/make_exercise_e2e_figs-redcheck.py` → `make_exercise_e2e_figs-redcheck-20260930T0525Z.log`：133 個竄改 133/133 以它自己的 `[TAG]` 與該停止點的字樣停下；對照組綠，且對照組畫出的 6 張 PNG（300／500 dpi）與資料夾裡的逐位元相同。AST 列出的每個停止點都至少被一個竄改打到，唯一例外 `[TITLE]`（標題是程式裡的常數，任何輸入都到不了；理由在 log）。本圖的停止點：T06_*、ARM_*、SEC_*、CONVERT*、PF_*、CODE、CLAIM、UP_*、SS_*、DOWN_*、RELEASE*、ENTRIES_*、TOPO_*、LAYOUT、G1_*、TWIN_*、BT_*、BTSK_*。
- **fig_t6 沒被動到**：`fig_t6-rerender-check-20260930T0523Z.log`——用沒改過的 `make_exercise_path_figs.py`（sha256 `6b2d5e08ced9bb91…`，與 fig_t6 `.md` 記的同一顆）重畫 fig_t6 到暫存目錄：兩張 PNG 逐位元相同；SVG 只差 `dc:date` 與 matplotlib 隨機的 clip-path id，PDF 只差 CreationDate。資料夾裡的 fig_t6 沒有被覆寫。
- 產圖紀錄：`make_exercise_e2e_figs-run-20260930T0525Z.log`。

最後產出：2026-09-30T05:25Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_exercise_e2e_figs.py` sha256 `55bba40bc0a41c99…`（產圖之後腳本沒再改過）；PNG sha256 `30266777c8fa80a8…`（300 dpi）、`f12b871e51c77439…`（`_hires`，500 dpi）。
