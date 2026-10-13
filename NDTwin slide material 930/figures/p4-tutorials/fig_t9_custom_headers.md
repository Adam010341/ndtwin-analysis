# fig_t9_custom_headers —— 七支自訂標頭 exercise：都轉得動；twin 有沒有看過它們自己的幀，大多沒證據

[Co-developed with claude code -- Adam]

## 一句話

七支以自訂標頭為關鍵的 exercise，09-27 那輪（T06，`5dc7fc9a`）的解答臂全部 PASS——它們在 NDTwin fabric 上**轉得動**；
但 twin 的鏈路讀數有沒有涵蓋它們**自己的**自訂標頭幀：只有 p4runtime 的 0x1212 tunnel 有位元組層的證據，
basic_tunnel、flowcache、link_monitor、mri 只驗過同一個 fabric 上的一般 IPv4，calc 與 source_routing 沒有證據（G1 NOT RUN）。

## 資料來源

P ＝ `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep`；R ＝ `P/runs`；
T06 ＝ `P/live-p1/runs/2026-09-27T074635Z_06_thirteen/00_table.tsv`。

| 用途（圖上的值） | 檔（path:line 或 JSON key） | commit／binary |
|---|---|---|
| 哪七支（列） | `P/GAP-1-exercise-requirements.md:50-64` §2a 表，`custom_headers` 欄標 **關鍵** 的列：basic_tunnel `:53`、calc `:54`、flowcache `:57`、link_monitor `:58`、mri `:60`、p4runtime `:62`、source_routing `:64` | 已提交 `532b6c31` |
| 列下的標頭小字 | 同上各列的 `custom_headers` 格（腳本斷言 `0x1212`、`0x1234`、`packet_in/out`、`0x812`、`IPv4 option` 還在格子裡）；英文短標是我寫的 | 同上 |
| 左欄「PASS (n/n)」 | `T06:11` basic_tunnel `PASS (4/4)`、`T06:7` calc `PASS (3/3)`、`T06:27` flowcache `PASS (5/5)`、`T06:17` link_monitor `PASS (4/4)`、`T06:23` mri `PASS (5/5)`、`T06:25` p4runtime `PASS (5/5)`、`T06:5` source_routing `PASS (5/5)`；皆 rc 0 | T06 各 arm report code 行 `5dc7fc9a` |
| 「no evidence」 | calc：`R/2026-09-27T075113Z_calc_solution_ndtwin.md:457`；source_routing：`R/2026-09-27T075027Z_source_routing_solution_ndtwin.md:661`（兩者都是 `N8  G1 ... -- NOT RUN`） | 同上 |
| 「IPv4 only」 | G1 PASS 且用的是 `iperf -u -b 2M ... -l 1200`：basic_tunnel `R/2026-09-27T075455Z_basic_tunnel_solution_ndtwin.md:710,723`；flowcache `R/2026-09-27T081256Z_flowcache_solution_ndtwin.md:591,604`；link_monitor `R/2026-09-27T075920Z_link_monitor_solution_ndtwin.md:621,637`；mri `R/2026-09-27T080951Z_mri_solution_ndtwin.md:719,734` | 同上 |
| 「yes · 0x1212 bytes」 | p4runtime：`R/2026-09-27T081205Z_p4runtime_solution_ndtwin/link_usage/onpath.txt:1-2`（s1-eth2 4,361,273 B、s2-eth1 4,347,273 B）、`…/iperf_client.txt:9`（`Sent 3500 datagrams`）、`…/twin_integral.txt:2`（twin 在 s1-eth2 積分 29,338,582 bit）；`R/2026-09-27T081205Z_p4runtime_solution_ndtwin.md:610,623`（G1 PASS） | 同上；tutorials checkout `c80d83e` 的 `exercises/p4runtime/advanced_tunnel.p4:25-28`（`myTunnel_t` ＝ 兩個 `bit<16>` ＝ 4 B） |
| 6 對 7 | `P/GAP-ANALYSIS.md:44,75,206,211-212`（G6「6 支」）；`P/GAP-2b-ndtwin-p4-capabilities-2026-09-27.md:97`（「7 支自訂標頭 exercise」）、`:192-208`（§3 表與最後一欄） | GAP-ANALYSIS 已提交 `532b6c31`；**GAP-2b 未提交，待 Adam 審**（`git status` 為 `??`） |

## 可信度

**OBSERVED（跑過，T06 的 raw）**
- 七支解答臂的 verdict 與 rc 0。
- 各臂 G1 是 PASS 還是 NOT RUN，以及 G1 用的流量是一般 IPv4 UDP iperf。
- p4runtime：交換機之間的 s1-eth2 比主機端 s2-eth1 多 14,000 B，恰好 ＝ 3,500 個 datagram × 4 B；twin 在 s1-eth2 的積分 > 0。
- flowcache 的 G1 PASS，但 **T06 的流只到了 s1→s3 那一段，沒有送達 h3**（s1-eth3 就是 s1 往 s3 的那條線：tutorials `exercises/flowcache/topology.json:48-51` 的 `["s1-p3", "s3-p2"]`，Mininet 的 pN＝ethN；tutorials checkout `c80d83e`，乾淨）：twin 自己的讀數 `…/2026-09-27T081256Z_flowcache_solution_ndtwin/link_usage/twin_integral.txt:3`（s1-eth3 約 31.8 Mbit）、`:7-9`（s3 三個介面 0.000）；
  介面計數器 `netdev.before:7`→`netdev.after:7`（s1-eth3 3151 → 4596340 B）、`netdev.before:3`→`netdev.after:3`（s3-eth1 3531 → 3804 B，+273）——twin 的讀數與位元組實際的去向一致，s3 的 0 是正確讀數；
  沒有送達：`iperf_server.txt` 沒有報告列、`iperf_client.txt:10`「did not receive ack of last datagram」；`onpath.txt` 只有 s1-eth3。（2026-09-27 UTC 第二輪補，coordinator 核過同一批 raw。）
- 以上 raw（含 p4runtime、flowcache 的 `link_usage/` 各 7 檔）都在 **audit-raw `797c34ab`**（與工作樹比 blob hash 相同）。

**READ（讀文件或碼，沒有執行）**
- 哪七支、標頭長什麼樣：GAP-1 §2a（讀 tutorials 原始碼整理的表）。
- 4 B 是 `myTunnel_t` 的長度：tutorials `advanced_tunnel.p4:25-28`（不在 trunk 裡，是 tutorials 的 checkout）。
- GAP-2b §3 的判斷（別人讀 raw 寫的；09-28 Adam 裁定了其中四格，flowcache 的 twin 改為「只看過 IPv4」）：它把 p4runtime 判「看得到」，basic_tunnel／link_monitor／mri「只看過 IPv4」、source_routing／calc「無證據」——與本圖一致；flowcache 見下。

**INFERRED（判斷）**
- 「那多出來的 14,000 B 就是 0x1212 tunnel 標頭」：由位元組差＝datagram 數 × 標頭長推得；我沒有抓 pcap 看 ethertype。GAP-2b 還引了同一窗口 s1 `ingressTunnelCounter 100` 到 3505 packets（控制器 log），方向一致。
- flowcache 放「IPv4 only」是我的判斷：它的自訂標頭是 packet-in/out 的控制器標頭，只走 CPU port 到它自己的控制器，不走 twin 量的交換機鏈路；
  它的資料流量本來就是一般 IPv4。**GAP-2b §3 把 flowcache 判成「看得到 (judgement)」**；T1 頁（`fig_t1c`）依 coordinator 第二輪裁決改用本頁同一個字「IPv4 only」（虛線待審），兩頁一致。
- 「IPv4 only」只表示「只驗過一般 IPv4」，**不表示** twin 看不到自訂標頭幀；是沒量過，不是量過沒看到。

## 6 支還是 7 支（對帳）

- **GAP-1 §2a（`:53-64`）標 7 支**：basic_tunnel、calc、flowcache、link_monitor、mri、p4runtime、source_routing。GAP-2b 的「7 支」與此一致。
- **GAP-ANALYSIS G6（`:44,75,206`）寫 6 支**，名單在 `:211-212`：basic_tunnel、calc、source_routing、link_monitor、mri、flowcache。
- 腳本逐字比對兩份名單：**差的是 p4runtime**，不是 flowcache。
  p4runtime 用的是跟 basic_tunnel 同一個 0x1212 tunnel 標頭，G6 名單漏了它；GAP-ANALYSIS 沒寫原因（我沒有推測）。
- flowcache 兩份都算，但 G6 自己註明「controller header ＝ CPU 通道另計」。
  所以「走在交換機鏈路上的自訂標頭」其實也是 6 支，但是**另一組 6 支**：GAP-1 的 7 支扣掉 flowcache。
- 本圖用 GAP-1 的 7 支（與 GAP-2b 同一口徑）。

## 圖怎麼讀

- 每列一支 exercise，名字下面是它的自訂標頭（小字）。依右欄的類別排序：yes → IPv4 only → no evidence。
- 左框「RAN IT · 09-27」：解答臂的 verdict，七支全綠。
- 右框「twin saw its own frames」：這一輪的 raw 能不能證明 twin 的鏈路讀數涵蓋了這支 exercise 自己的自訂標頭幀。
  - 綠「yes · 0x1212 bytes」：只有 p4runtime。
  - 黃「IPv4 only」：G1 有跑、有 PASS，但用的是一般 IPv4 iperf，沒量那支的自訂標頭流量。
  - 灰「no evidence」：G1 NOT RUN。arm report 自己寫的理由：calc.p4:205-210 丟掉非 0x1234 的一切（`calc_solution…md:464`）、source_routing.p4:127-138 丟掉沒有 0x1234 堆疊的幀（`source_routing_solution…md:668`），一般 iperf 過不去。

## 已知但書

- **髒 checkout（F-16）**：七支解答臂的 code 行都是 `5dc7fc9a +95 file(s) with uncommitted changes`。圖上沒有印 sha。
- **措辭守則**：這幾支只能說「轉得動（forward）」；**不要說「NDTwin 觀測得到它們」**。
- G1 只斷言「鏈路使用率跟著 iperf 走」，不斷言封包送達（flowcache 就是送不到也 PASS 的例子）。
- 流身份層：非 IPv4 只進上限 1024 筆的側表、不進流表；raw 裡沒有任何一份證明 tutorials 的自訂標頭流量出現在側表（GAP-2b §3.1，READ，轉述）。本圖只講鏈路位元組層。
- 骨架臂不跑 G1，所以本圖只看解答臂。
- 這一頁全部依據 09-27 那一輪；其他輪（例如 09-26 的 flowcache）不同樣子，沒放。

- 紅測（mutation check）與產圖紀錄：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/o1-o2-t6-t9/`（`run_mutations.py`、`run_mutations.log` 14/14 照預期、`gen_overview.log`、`gen_p4tutorials.log`、各 mutant 輸入檔）。

## 重生指令

```
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/p4-tutorials"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_exercise_path_figs.py
```

最後產出：2026-09-27T17:05Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_exercise_path_figs.py` sha256 `6b2d5e08ced9bb91…`（產圖之後腳本沒再改過）。
