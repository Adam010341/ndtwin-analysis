# 三段 demo 影片的錄製流程（**P4 / bmv2，128 hosts**）

**對應 Page 41（Demo）**。全部跑在 **P4 資料面**上，**128 台 host**。
用平常在用的介面：**Web-GUI 看、Mininet CLI 改、NTG 打流量**。

---

## 0. 開機流程（從乾淨環境開始，照順序貼）

### 步驟 0：清乾淨

**每次錄影前都做**，不管你覺得上一輪有沒有收乾淨。
bmv2 的孤兒 switch **活得過 `mn -c`**，殘留會讓下一輪出現對不上的症狀。

```bash
cd ~/Desktop/NDTwin-Kernel && ./tools/test_workflow/stack.sh down
```

```bash
sudo -n ndtwin-lab topo-stop; sudo -n ndtwin-lab cleanup
```

`cleanup` 做的事：殺掉 `ntg_bmv2_topo.py` / `p4_testbed_topo.py` / NTG 的 `testbed_topo.py`、
跑 `mn -c`、殺掉所有 `simple_switch_grpc`、刪掉 `/tmp/ndtwin_p4_switches.json`。

**確認真的乾淨**（三個都要是 0 / 不存在）：

```bash
pgrep -fc 'simple_switch_grp[c]'; pgrep -fc 'ntg_bmv2_top[o]'; ls /tmp/ndtwin_p4_switches.json 2>&1
```

> ⚠️ **`pgrep` 一定要加 `-f`**：它比對 process 名稱時只看前 15 個字元，
> 而 `simple_switch_grpc` 有 18 個 —— **`pgrep -c simple_switch_grpc` 永遠回 0**。
> 而 `[c]` 那個中括號是為了**不要匹配到這道指令自己**（這陷阱在這專案咬過三次）。
>
> ⚠️ **中括號只保護 pattern，不保護同一行的其他字。** 如果你把 `pgrep` 跟一條含有
> 完整 `simple_switch_grpc` 的指令（例如 `ls /usr/local/.../simple_switch_grpc`）
> 串在同一行，**那一行自己的 argv 就含有目標字串，還是會匹配到自己**。
> 要嘛分開跑，要嘛改用不吃 argv 的 `ps -eo comm | grep -c '^simple_switch'`。

---

### 步驟 1：設成 128 台 host

```bash
echo 128 > ~/Desktop/NDTwin-Kernel/p4_proxy/mininet/host_count_override
```

🔴 **這一步就是上次 `ping 10.0.0.33` 失敗的原因。** 這個檔不存在時 `HOST_NUM` 預設是 **4**，
只有 h1–h4（`10.0.0.1`–`10.0.0.4`），**`10.0.0.33` 那台根本沒被建出來** ——
h1 送 ARP 沒人回，於是 h1 自己的核心回一個 `Destination Host Unreachable`，
所以來源才是 `10.0.0.1`。**那不是網路壞了，是主機不存在。**

順便確認 bmv2 用的是**快的那顆 build**（demo 要打大流量，這是前提）：

```bash
grep -v '^#' ~/Desktop/NDTwin-Kernel/p4_proxy/mininet/bmv2_binary_override | grep .
```

應該印出 `/usr/local/bmv2-fast/bin/simple_switch_grpc`。**如果這裡是空的就會退回 stock build**，
而 stock 的天花板是 **~40 Mbps**（UDP delivered），大流量會整個被壓平。

> 🔑 **怎麼確認那顆真的是 fast build**（2026-08-19 驗過，**不要用檔案大小判斷**）：
> fast 是 92 MB、stock 只有 9.6 MB，但那個差距**全部來自 debug 符號**
> （`file` 說 fast 是 `with debug_info, not stripped`，stock 是 `stripped`）——
> **跟優化等級無關**。真正的判別是 `--disable-logging-macros` 會把逐封包的 log 格式字串編掉：
>
> ```bash
> for b in /usr/local/bin/simple_switch_grpc /usr/local/bmv2-fast/bin/simple_switch_grpc; do echo "$b"; strings -a "$b" | grep -cF "Processing packet received on port"; done
> ```
>
> ✅ **stock 回 1、fast 回 0** ＝ fast build 確認。（`Applying table`、`Pipeline '` 也同樣是 1 對 0。）

---

### 步驟 2：選 topo prompt 要給你哪一種介面

`~/Network-Traffic-Generator/setting/Mininet.yaml` 的 `mode:` 決定拓撲最後把 net 交給誰：

| `mode` | 你會拿到 | 用在 |
|---|---|---|
| `cli` | **Mininet 的 CLI**（`h1 ping h33`、`link ... down`、`pingall`） | **demo ①、③** |
| `custom_command` | **NTG 的 prompt**（`flow --config`、`dist --config`） | **demo ②** |

⚠️ **一次只能有一種**，所以 demo ①③ 和 demo ② 是**兩次不同的拓撲啟動**。

**demo ①③ 用這條：**
```bash
sed -i 's/mode: "custom_command"/mode: "cli"/' ~/Network-Traffic-Generator/setting/Mininet.yaml
```

**demo ② 用這條：**
```bash
sed -i 's/mode: "cli"/mode: "custom_command"/' ~/Network-Traffic-Generator/setting/Mininet.yaml
```

---

### 步驟 3：起 bmv2 拓撲（128 台）

```bash
sudo -n ndtwin-lab topo-start
```

**等它建完再往下**，128 台大約 **20–30 秒**。看進度：

```bash
sudo -n ndtwin-lab topo-out 40
```

✅ 要看到 **`All 10 BMv2 switches listening on gRPC 50051 ~ 50060.`**
❌ 如果印出 `WARNING: N of 10 BMv2 switches did NOT come up` —— **回步驟 0 重來**，
不要在殘缺的 fabric 上打流量，那量到的東西沒有意義。

---

### 步驟 4：起 proxy + kernel（**一定要帶 `TOPO_P4`**）

```bash
cd ~/Desktop/NDTwin-Kernel && TOPO_P4=$PWD/setting/StaticNetworkTopologyP4_10Switches_128Hosts.json ./tools/test_workflow/stack.sh up p4
```

⚠️ **它在 `[1/3]` 會停下來叫你「另開終端機跑 Mininet」——直接按 Enter 就好。**
拓撲步驟 3 已經起好了，這個提示是給沒有先起拓撲的人看的。
之後 `[2/3]` 起 proxy（:8081）、`[3/3]` 起 kernel（:8000）。

然後等收斂：

```bash
cd ~/Desktop/NDTwin-Kernel && ./tools/test_workflow/stack.sh wait
```

（`wait` 不必再帶 `TOPO_P4`：`up` 會把 mode 和拓撲路徑寫進 `.test_run/mode`，
`cmd_wait` 從那裡讀回來。⚠️ 但**如果 `up` 沒跑成功**，那個檔不存在，
`wait` 會退回 `$TOPO_OVS` —— 所以看到它報奇怪的數字時，先確認 `up` 有做完。）

> 🔴 **`up` 不帶 `TOPO_P4` 會永遠卡在這裡**：
> ```
> waiting for link discovery: want 12 destination paths
>   paths=16256
> ```
> `components.env:74` 的預設值是 **`StaticNetworkTopologyP4_10Switches_4Hosts.json`**，
> 而 `stack.sh` 的收斂閘門是從那份 JSON 算 `hosts × (hosts−1)` —— 4×3 = **12**。
> 你的 fabric 是 128 台，proxy 誠實回報 **16256**，兩邊**永遠對不上**。
>
> ⚠️ **這不只是卡住而已。** 那份 JSON 也是 **kernel 載入的靜態模型**，
> 所以就算硬等到 timeout 讓它帶著 warning 繼續跑，
> **kernel 會拿一份 4 台 host 的模型去描述一張 128 台的網路**，Web-GUI 上看到的是錯的。
>
> **這是第五份寫死 4 台的東西**（前四份：拓撲接線、拓撲 ARP、proxy 的 `add_host`、
> `ntg_bmv2_topo.py` 的 ARP）。128 台的模型是 2026-08-19 用
> `tools/test_workflow/derive_p4_topology_json.py` 從 OVS 那份導出來的
> （兩者只差 switch 的 `brand_name`），已經在 repo 裡，不用自己產。

---

### 步驟 5：確認三個介面都活著

```bash
curl -s localhost:8000/ndt/get_graph_data | python3 -c "
import json,sys; d=json.load(sys.stdin)
sw=[n for n in d['nodes'] if n.get('vertex_type')==0]
print('switches:', len(sw), 'up:', sum(1 for n in sw if n['is_up']))
print('nodes:', len(d['nodes']), 'edges:', len(d['edges']))"
```

✅ 預期：**switches 10 / up 10、nodes 138、edges 288**。

**Web-GUI 打開**：瀏覽器 `http://localhost:3000`（已經在 Docker 裡跑著）。
要重啟的話：

```bash
cd ~/Web-GUI && ./web_gui_deploy.sh
```

---

## 0.5 錄影工具與畫面

這台機器**沒有 ffmpeg／OBS／kazam**，桌面是 **GNOME Shell 46 / Wayland**。用內建的：

- **`Ctrl` + `Alt` + `Shift` + `R`** 開始，**再按一次**停止 → `~/Videos/Screencasts/*.webm`

⚠️ **先錄 10 秒測試檔播來看**（有沒有被截斷、字夠不夠大、游標入不入鏡）。
**關掉通知**（快速設定 → 勿擾），一則通知就要重錄。

錄的時候在三個視窗之間切：

| 視窗 | 內容 | 怎麼開 |
|---|---|---|
| **A. Web-GUI** | `http://localhost:3000` | **主畫面** |
| **B. topo prompt** | Mininet CLI 或 NTG prompt | `sudo tmux -L ndtwinlab attach -t topo` |
| **C. kernel log** | 事件何時被偵測到 | `tail -f ~/Desktop/NDTwin-Kernel/.test_run/logs/kernel.log` |

---

## 1. Demo ①：斷鏈 → 自動繞路 → 復原（P4，128 hosts）

**前置**：步驟 0 → 1 → 2（選 `cli`）→ 3 → 4 → 5。

### 🔴 P4 上斷鏈只能用 `tc netem`，不能用 `link ... down`

Mininet CLI 的 `link s1 s5 down` 底層是對兩端 `ifconfig down`，
**在 bmv2 上不只斷那條線 —— 它讓整台 switch 的 packet-in 路徑停擺**。
實測：斷掉 s1 的一個埠之後，s1 的 `probe_ok` 還是 `true`、gRPC 沒斷、它還在對外送 beacon，
但 `last_packet_in_age_s` 從 3 秒跳到 **73 秒**，於是 **s6→s1 那條完全正常的線也被判失效**。
**畫面上會冒出你沒斷的 down edge，講解當場對不上。**

所以這一段的斷鏈指令是 `tc netem`（在視窗 B 旁邊另開一個終端機跑）。

### 錄影

**視窗 A（Web-GUI）**：打開拓撲頁，讓觀眾看到完整的 **10 switches / 128 hosts / 288 edges**。

**視窗 B（Mininet CLI）**：**先打一條 100 Mbit/s 的流**，這樣 GUI 上才看得到路徑。

> 🔴 **光靠 ping 是不夠的。** ping 每秒幾百 bytes，在 GUI 上等於 0，
> **你會看不出流量走哪一條路，也就沒辦法挑要斷哪一條**。
> ping 的用途只有一個：**把中斷長度量出來給觀眾看**。兩個都要跑。

```
mininet> h33 iperf3 -s -D
```

```
mininet> h1 iperf3 -c 10.0.0.33 -u -b 100M -l 1400 -t 300 &
```

⚠️ **結尾的 `&` 不能省** —— Mininet CLI 的前景指令會把 prompt 卡住 300 秒，
那樣就沒辦法再下 ping。
⚠️ **用 UDP（`-u`）不要用 TCP**：UDP 在圖上是乾淨的方波，斷掉直接掉到 0、通了直接回到 100。
TCP 會有 congestion control 的緩升，復原看起來拖泥帶水，**會模糊掉「16 秒就好了」這個重點**。
（100 Mbit/s 遠低於 fast build 的 300 Mbps 零損點，不會自己掉封包。）

**然後起持續 ping，這是前景、也是觀眾要看的主角**：

```
mininet> h1 ping -D h33
```

（用 **主機名 `h33`** 不要打 IP，Mininet 自己解析 —— 就不會再打錯。
`-D` 每行帶時間戳，觀眾可以直接讀出中斷長度。）

**讓它跑 10 秒正常回應**。這 10 秒不要剪掉，它是「斷之前是好的」的證據。

**回到視窗 A**，在 Web-GUI 上**指出這條流走哪幾條鏈路**（Topology / LinkFlowInformation 面板）。
現在那條路徑上會是紮實的 **~100 Mbps**，其餘全是 0，**一眼就看得出來**。
🔑 **這一步是整段的關鍵**：接下來要斷的必須是**這條路徑上**的鏈路。
斷一條沒人在用的線，畫面看起來就跟 demo 失敗一模一樣。

> 💡 **h1 → h33 的路徑是可以預先知道的**：host 平均掛在 s1–s4 上（每台 32 台），
> **h1 在 s1、h33 在 s2**，所以流量走 `s1 → 核心 → s2`，**3 跳**。
> 而實測顯示路由總是挑 `eth1`（→ s5），**`eth2`（→ s6）完全閒置** ——
> 所以要斷的是 **`s1-eth1`**，繞路之後會走 `s1-eth2 → s6`。
> 🔑 **這對 demo 是加分**：s6 原本整台是全黑的，繞路後**一整條路徑會亮起來**，
> 畫面上非常明顯。（⚠️ 這是最短路徑沒有 ECMP 的預期行為，不是缺陷，但別在簡報上說成負載平衡。）

**新終端機**，斷掉剛剛指出來的那條（把 `s1-eth1` 換成你在 GUI 上看到的那條）：

```bash
sudo -n mnexec -a 1 tc qdisc add dev s1-eth1 root netem loss 100%
```

> ⚠️ 如果這條回報 `RTNETLINK answers: File exists`，代表那個介面上已經有 htb（TCLink 整形），
> 要掛在 htb 底下而不是 root。查 class 再掛：
> ```bash
> sudo -n mnexec -a 1 tc class show dev s1-eth1
> ```
> 然後把 `root` 換成 `parent <class-id>`。
> （`measure_failover.sh:40-49` 就是這樣分支的，量測腳本已經處理過這件事。）

**然後就是等。** 三件事依序發生，邊等邊講：

| 時間 | 畫面 | 講什麼 |
|---|---|---|
| 0 s | ping 沒有回應；**GUI 上 `s1-eth1` 從 100 Mbps 掉到 0** | 「鏈路斷了」 |
| ~15–20 s | 視窗 C 出現 `link failed` | 「**這 15 秒是 watchdog 的 beacon timeout，是設計值不是延遲**」 |
| **~17 s** | **GUI 上 `s1-eth2 → s6` 那條原本全黑的路徑跳到 100 Mbps**；ping 回來 | 「控制平面重算並下發，**故障還在的情況下自己好了**」 |

🔑 **P4/128 的中斷平均 16.6 秒（n=10，範圍 14.3–20.8）**，
對照 **OVS/128 是 51.8 秒（47.0–56.4）** —— 這句話可以在等的時候講。

⚠️ **GUI 的數字會逐秒跳動，那是取樣理論不是 bug。** 1-in-256 取樣在 1 秒窗誤差 ±75%，
30–60 秒窗才收斂到 <10%（實測中位數比值 0.97–1.02）。**長期準、短期吵。**

**復原**（可錄可剪）：

```bash
sudo -n mnexec -a 1 tc qdisc del dev s1-eth1 root
```

**錄完這段收拾**（否則 iperf3 會一直跑到 300 秒，影響下一段）：

```
mininet> h1 pkill iperf3
```

⚠️ **一條就夠，而且它會把 client 和 server 一起殺掉。**
Mininet 的 host 只有獨立的**網路** namespace，**PID namespace 是共用 root 的** ——
所以在任何一台 host 上跑 `pkill` 影響的是整台機器。
（同理：**不要用 `kill %iperf3`** 這種 job spec，`p4_testbed_topo.py:236` 已經記過它不可靠。）

---

## 2. Demo ②：Web-GUI 看 P4 拓撲與流量（**大流量**）

**前置**：步驟 0 → 1 → 2（選 `custom_command`）→ 3 → 4 → 5。

### 為什麼上一版流量太小

`flow_bmv2_low.json` 是為 **stock build** 寫的：TCP 4M / UDP 2M / fixed 8M ×3，
**加起來大約 20 Mbps**。那顆 build 的 UDP delivered 天花板只有 **~40 Mbps**，所以只能這樣。

**現在 `bmv2_binary_override` 指向 fast build**（`-O3 --disable-logging-macros`），實測：

| | stock | **fast** |
|---|---|---|
| UDP 零損點 | 25 Mbps | **300 Mbps** |
| UDP delivered 天花板 | ~40–42 Mbps | **~460–530 Mbps** |
| TCP 單流 goodput | 24.2 Mbps | **431 Mbps** |

所以我另外寫了一份 **`flow_bmv2_demo.json`**（在 `p4_proxy/mininet/`），
目標**約 220 Mbps 總量**，**是舊 template 的 11 倍**，但仍在 300 Mbps 零損點以下：

- **fixed**：3 條 TCP × **40 Mbit/s**、持續 280 秒 → **120 Mbps 穩定底流**（GUI 上是穩定的長條）
- **varied**：每秒 1 條，TCP 6 MB @ 20 Mbit/s ／ UDP 15 Mbit/s 持續 4 秒 → **約 100 Mbps 的變動量**
- 全部 `far`，所以流量都會**穿過核心鏈路** —— 這正是 GUI 上最好看的地方

### 錄影

**視窗 A（Web-GUI）**：
1. **拓撲**：10 台 switch、128 台 host。點一台，`DeviceInformation` 面板顯示它的資訊 ——
   **brand 是 BMv2**。
2. **視窗 B（NTG prompt）** 打流量：
   ```
   flow --config /home/adam/Desktop/NDTwin-Kernel/p4_proxy/mininet/flow_bmv2_demo.json
   ```
   ⚠️ **一定要用絕對路徑**：NTG 在進 prompt 之前會把 cwd 換到它自己的 repo。
   （`--config` 後面按 `Tab` 有路徑補全，錄影時用 Tab 比打字好看也不會 typo。）
3. **回到視窗 A**：核心鏈路的數字跳上去，`FlowInformation` / `PerLinkFlowGraph` 動起來。

### 🔑 這一段唯一要講的一句話

> **同一支 GUI、同一個 API、同一個 kernel。底下的資料面換成 P4，上層一行都沒有改。**

因為 proxy 模仿了 Ryu 的北向 API，**而且自己合成 sFlow v5** 餵進 kernel 既有的 :6343。
GUI 分不出來 —— **這正是這個專案的主張，而這一頁是它的畫面證據。**

### ⚠️ 地雷

- 🔴 **NTG 不支援中斷實驗。** 按 `Ctrl-C` 會把整個 NTG 關掉，不是停下這一輪。
  錄完你要的片段就直接停止錄影，讓它自己跑完再 `exit`。
- 🔴 **收尾預算是 `interval + fixed 的 duration`，不是 interval。**
  NTG **會重啟 fixed flow** 來維持 `fixed_flow_number`——第一批跑完它立刻補上第二批，
  而第二批又是完整的 duration。所以 interval 300 s ＋ duration 280 s 的組合
  **會在 prompt 上卡到第 580 秒**，畫面停在
  `Waiting for all connections to be restored, currently running host pairs: N`。
  **那不是當機**（`ps -eo pid,etimes,args | grep '[i]perf3'` 會看到它們的 `-t` 和已跑秒數）。
  ✅ **所以 fixed 的 `duration` 要設短**（現在是 **20 秒**）：靠重啟維持連續流量，
  尾巴最多 20 秒。`flow_bmv2_demo.json` 現在是 **interval 2 分鐘 ＋ duration 20 秒**，
  最壞情況 140 秒收完。
- **第一次跑 NTG 會先算 `link_relationship_init`**（host 之間的距離關係），
  128 台要算一下，**不是當機**。

---

## 3. Demo ③：關掉一台 switch → liveness 三態 → 再開回來

**前置**：跟 demo ① 同一套環境，可以接著錄，不用重起。

**用 Phase 7 的電源 API，不要用 `kill`。** 兩個理由：
1. **`kill` 掉的 switch 沒有對應的「開回來」** —— 你會被迫重建整個拓撲才能錄下一段。
2. **電源管理本身就是要 demo 的功能**（簡報 Page 18），用 `kill` 等於繞過它。

三個狀態是 **Up → Unknown → Down**，而 **`Unknown` 不會動 graph**。
這本身就是一個修過的缺陷：把 Unknown 當成 Down，**一次探測失敗就會把整組標成死的**。

**交換機的 IP**（`ip` 參數用這個，不是 host 的 10.0.0.x）：
`s1` = `192.168.123.11`、`s2` = `.12` …… 依序到 `s10` = `192.168.123.20`。

### 錄影

**視窗 A（Web-GUI）**：先讓觀眾看到 10 台 switch 全部正常。

**新終端機**，關掉 s3：

```bash
curl -s -X POST "http://localhost:8000/ndt/set_switches_power_state?ip=192.168.123.13&action=off"
```

✅ 預期回 `{"192.168.123.13": "Success"}`。
底層是 root helper `ndtwin-p4-power` 依 manifest 指名停掉**那一顆** `simple_switch_grpc`
（不是 `pkill`，那會殺掉全部十台）。
❌ 如果回 400，**那就是真的沒關成功** —— 這個端點**不會假裝成功**，
原因在 kernel log 不在回應裡（helper 沒裝／manifest 過期／gRPC port 被佔）。

**回到視窗 A**：**s3 不會馬上變 Down** —— 這就是要展示的中間態。
gRPC 探測已經失敗，但**它剛送出的 LLDP beacon 還沒過期**，所以判定是 **Unknown**，
**系統不會因為一次探測失敗就改寫拓撲**。等 beacon 過期（15 s）才轉 **Down**。

想在鏡頭前把中間態叫出來（另一個終端機）：

```bash
curl -s localhost:8081/p4/switch_state | python3 -c "
import json,sys; d=json.load(sys.stdin)
for k,v in d.items(): print(k, 'probe_ok=',v.get('probe_ok'), 'lldp_age=',v.get('last_lldp_age_s'))"
```

轉 Down 之後，`DeviceInformation` 的 CPU／記憶體／溫度全部顯示 unavailable ——
三個端點現在統一回 `-1`（commit `04b8933`），在那之前它們用三種不同方式講同一件事。

### 再開回來

🔴 **關機之後一定要等 15 秒再送 `on`。**
**關機後約 10 秒內送 `action=on` 會回 200 Success 但什麼都不做** ——
這是目前**最可能在示範現場當場發作**的缺陷，而且它「成功」的回應會讓你以為開了。

```bash
sleep 15; curl -s -X POST "http://localhost:8000/ndt/set_switches_power_state?ip=192.168.123.13&action=on"
```

（`sleep 15` 直接串在前面，就不必自己數秒數 —— 錄影時也剛好是一段可以講話的空檔。）

`on` 做的事比 `off` 多：helper 依 manifest 記下的 argv **用它自己的函式庫重新啟動**那顆
switch，然後 proxy 對它做 **re-adopt**（`POST /p4/readopt/{dpid}`：mastership、pipeline、
clone session、以及那台的路由全部重下）。

**視窗 A**：s3 回到 Up，而且**流量會重新經過它** —— 這一段是「twin 不只看得到，還控制得動」的證據。

**確認真的回來了**（比 GUI 更硬的證據）：

```bash
curl -s localhost:8081/p4/switch_state | python3 -c "
import json,sys; d=json.load(sys.stdin); print({k: v.get('probe_ok') for k,v in d.items()})"
```

### ⚠️ 地雷

1. 🔴 **關機後 10 秒內送 `on` 會回 Success 卻沒動作** —— **等 15 秒**。
2. 🔴 **`ip` 用的是交換機的管理 IP（`192.168.123.1x`），不是 host 的 `10.0.0.x`。**
   給錯 IP 會回 400。
3. **`os.kill` 回 `PermissionError` 代表那個 process 活著**，不是死了 ——
   自己寫檢查腳本時會踩到。
4. **不要用 `kill` 繞過 API。** 用 API 關掉的一定開得回來（這條路徑有 re-adopt）；
   **手動 `kill` 之後還能不能用 `action=on` 救回來，我沒有驗證過** ——
   demo 前不要拿沒驗過的路徑冒險。

---

## 4. 錄完之後

```bash
cd ~/Desktop/NDTwin-Kernel && ./tools/test_workflow/stack.sh down
sudo -n ndtwin-lab topo-stop; sudo -n ndtwin-lab cleanup
```

- 影片在 `~/Videos/Screencasts/`，改成看得懂的名字再放進簡報資料夾。
- **`.webm` PowerPoint 不一定吃**，而這台機器沒有 ffmpeg 可以轉檔。
  最穩：**簡報裡不嵌影片，切出去用瀏覽器播**。
- ⚠️ **報告當天不要現場 live demo。** 錄影的理由就是這個：
  上面每一段都有會當場發作的地雷，錄影可以重錄，現場不行。

---

*[Co-developed with claude code -- Adam]*
