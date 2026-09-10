# NDTwin 簡報 — 待裁決的修改清單

> 這份檔案記錄的是「與 Adam 討論投影片內容時，回頭查證原始碼後發現的落差」。
> 每一條都附證據（`檔案:行號`），可以直接開檔覆核。
>
> **這份檔案不是決議，是待裁決清單。** 每條都有建議改法，但改不改由 Adam 決定 ——
> 有些落差是刻意的取捨，簡報上不一定要講。
>
> 對象是 `NDTwin-slide-template.md`（671 行版本，2026-08-18 改版後的 42 頁大綱）。
> 建立日期：2026-08-19。查證基準：branch `fix/flow-rate-divide-by-zero`，HEAD `04b8933`。

---

## 分級口徑

| 標記 | 意思 | 後果 |
|---|---|---|
| 🔴 | **事實錯誤** | 學長姐追問會當場站不住，必須改 |
| 🟡 | **過度宣稱** | 技術上成立，但端到端不成立；被追問要能立刻補上限制 |
| 🔵 | **精確度** | 不會錯，但可以更準或更好懂 |
| ➕ | **建議新增** | 目前沒寫，但值得放進去 |
| ✅ | **已查證正確** | 記在這裡是為了避免下一輪重查 |

---

## Page 4 — Background: the system, and the task

### 🔴 4-1 「沒有共享檔案」是錯的，而且與 Page 25 自相矛盾

**目前的寫法**（`NDTwin-slide-template.md:185`）：

> ② 七個元件依賴它，且**只透過 `/ndt/` HTTP API**——沒有共享記憶體、沒有共享檔案。

**問題：** 後半句不成立。kernel 自己就在 `/ndt/app_register` 的處理流程裡建立共享檔案：

- `ApplicationManager::registerApplication`（[`src/ndt_core/application_management/ApplicationManager.cpp:30-46`](../NDTwin-Kernel/src/ndt_core/application_management/ApplicationManager.cpp)）呼叫 `setupNFSForApp(appId)`
- `setupNFSForApp` 在 `:253` 執行 `std::system("exportfs -ra && systemctl reload nfs-server")`
- 模擬的輸入／輸出檔就走 `/srv/nfs/sim/<app_id>`，HTTP 只傳檔名

**而且這頁跟自己的第 2 節打架**：改版說明第 6 條（`:37`）寫「Page 25 新增 2026-08-17 找到的一條 baseline 缺陷（`setupNFSForApp` 提早 return）」。
Page 4 說「沒有共享檔案」，Page 25 講一個「建立共享檔案的函式」的缺陷 —— 同一份簡報裡的兩頁互相否定。

**建議改法：** 拿掉那個絕對否定，把重點放回真正要講的事（七個元件不必改）。

> ② 七個元件依賴它，**全部透過 `/ndt/` HTTP API**——沒有共享記憶體，沒有元件直接讀 kernel 的資料結構。

**查證過的部分（可以放心講）：** 七個 consumer 確實全部只用 `/ndt/`，沒有任何一個直接連 Ryu 或交換機讀狀態。零共享記憶體屬實。

**一個小保留（被問到再講，不必寫進投影片）：** NTG（Network-Traffic-Generator）的 `testbed_topo.py`
會 import Mininet 並執行 `ovs-vsctl`，所以「七個元件都碰不到 control plane」這種更強的說法**不能講**。
我們這邊有一個 172 行的 `p4_proxy/mininet/ntg_bmv2_topo.py` 當橋接。

---

## Page 11 — The P4 pipeline

這一頁的三段條列有兩段需要動。**核心問題是同一個：pipeline 的能力寫成了系統的能力。**

> **一句話總結，Adam 可以先記這個：**
> P4 pipeline 裡有三張表（`flow_5tuple` / `ipv4_lpm` / `l2_forward`），
> **但 proxy 只有寫 `ipv4_lpm` 的程式碼。** 另外兩張表永遠是空的。

證據 —— `p4_proxy/proxy_agent/p4_client.py` 裡所有 flow 寫入方法：

```
582:  def insert_ipv4_route(...)     → MyIngress.ipv4_lpm
662:  def delete_ipv4_route(...)     → MyIngress.ipv4_lpm
711:  def modify_ipv4_route(...)     → MyIngress.ipv4_lpm
```

沒有 `write_flow_5tuple_entry`，沒有 `write_l2_forward_entry`。
`grep flow_5tuple` 在整個 `p4_proxy/`（排除 tests）只命中一行**註解**。

---

### 🟡 11-1 ① ternary `flow_5tuple` — pipeline 做得到，系統做不到

**目前的寫法**（`:233`）：

> ① ternary `flow_5tuple` 帶真正 priority、置於 `ipv4_lpm` 之前，特定 flow rule 贏過預設路由而不靠 table 順序。

**這句話對 pipeline 是完全正確的：**

- 表在 [`p4_proxy/p4_src/ndtwin_switch.p4:307-325`](../NDTwin-Kernel/p4_proxy/p4_src/ndtwin_switch.p4)，六個 ternary key、`size = 1024`
- 「置於之前」是 `:368-372` 的控制流明寫的（P4 沒有 cross-table priority）：
  ```p4
  if (hdr.ipv4.isValid()) {
      if (!flow_5tuple.apply().hit) { ipv4_lpm.apply(); }
  }
  ```
- Phase 4 完成，commit `4577983`

**問題是端到端不成立：** 送一條 5-tuple 規則進來，proxy 會**回 400 拒絕**。

`topology_manager.py:96-106` 的白名單只有兩個欄位：

```python
HONOURED_MATCH_FIELDS = frozenset({"nw_dst", "ipv4_dst"})
ETH_TYPE_FIELDS = frozenset({"dl_type", "eth_type"})   # 只准 0x0800，而且不當 key
```

其餘一律 `raise UnsupportedMatchError` → HTTP 400。`ipv4_src` / `ip_proto` / `tcp_src` / `udp_dst` / `in_port` 全部被拒。

`topology_manager.py:28` 的註解自己說明了狀態：

> The pipeline does have a ternary `flow_5tuple` table with real priority (Phase 4);
> **wiring `route_flow` to it is the proper fix and remains Phase 3 work. Until then, refusing beats pretending.**

計畫書的 phase 表（`doc/2026-07-27_p4_bmv2_support_plan.md:20-27`）：Phase 4（pipeline）✅ 完成、**Phase 3（proxy 端點補完）⬜ 未做**。

**建議改法** —— 把「拒絕優於假裝成功」變成賣點，那本身就是好的設計原則，而且比「我們支援 5-tuple」更難被問倒：

> ① **A ternary 5-tuple table with real priority, ahead of LPM.**
> The pipeline can now express what an OpenFlow rule means. Until the proxy is wired to it,
> such rules are **rejected explicitly** rather than silently degraded to a destination-only
> route — which is what happened before.

**如果要講背後的事故（很有力，建議口述）** —— `topology_manager.py:14-25` 記錄的實測：

> 一筆 `{ipv4_src, ipv4_dst, ip_proto, udp_src, udp_dst}` priority 100 的 TE 規則，
> 被裝成 `10.0.0.4/32 -> port N`，proxy 回 200。
> **實測驗證過：規則生效了、流量也真的改道了，但它套用到所有前往 10.0.0.4 的流量**，
> 而不是 caller 指名的那一條；讀回來 priority 是 0。

一條瞄準單一 flow 的 TE 規則，悄悄變成整個目的位址的規則。**「不支援」你會知道，「靜靜降級」你不會。**

---

### 🔴 11-2 ② Non-IPv4 frames — 三個地方站不住

**目前的寫法**（`:233`）：

> ② ARP/TCP/UDP/ICMP 解析 + L2 表，非 IPv4 frame 不再被默默丟棄。

英文版（Adam 手上那份）：

> ARP, TCP, UDP and ICMP are parsed, and an L2 table forwards what the IPv4 path cannot.
> Before this, anything that was not IPv4 disappeared silently.

**問題一：ARP 沒有被 parse。**
`ndtwin_switch.p4` 裡**沒有 `arp_t` header**。parser 在 `:205-208` 對非 IPv4 走 `default: accept`，
ARP 只是被放行到 ingress，靠 Ethernet header 轉送。被 parse 的是 TCP / UDP / ICMP（`:223-244`）。

**問題二：L2 表沒有轉送任何東西。**
`l2_forward`（`:344-359`）**零 entry**（沒有寫入端，見上方），所以每個非 IPv4 幀都命中
`default_action = send_to_cpu()`。到了 proxy，`handle_packet_in`
（[`topology_manager.py:962`](../NDTwin-Kernel/p4_proxy/proxy_agent/topology_manager.py)）**只解析 LLDP** ——
ARP 進去被記一筆 liveness 證據，然後就沒了，不 flood 也不 learn。

**問題三：「disappeared silently」暗示現在不會了，但 ARP 現在仍然到不了目的地。**
只是死的地點從 pipeline 換成控制器。

**但這個改動不是白做的**（如果要講，講這兩點）：

1. 表和 punt 路徑都在了，所以要加 L2 learning 是**純控制平面**的改動，不用重編 pipeline、不用重推 `SetForwardingPipelineConfig`
2. 封包從「無聲消失」變成「控制器看得到」

**關鍵發現：OVS 端一模一樣。** 這條讓整段話可以改寫成一個更強的版本。

`intelligent_router.py`（1012 行）在 switch 上裝的規則**只有兩種**，加 Ryu 自己那條共三種：

| prio | match | action | 誰裝的 |
|---|---|---|---|
| 65535 | `dl_dst=01:80:c2:00:00:0e, dl_type=0x88CC` | CONTROLLER | Ryu `--observe-links`（`ryu/topology/switches.py:643`）|
| 10 | `eth_type=0x0800, ipv4_dst=<host>` | `OUTPUT:port` | `install_all_pair_paths`（`intelligent_router.py:629`）|
| 0 | `{}`（table-miss）| CONTROLLER | `switch_features_handler`（`intelligent_router.py:239-243`）|

**一條 `dl_dst` 的轉送規則都沒有。** live 佐證在
`doc/audit/2026-08-18_live-full-stack-round/live-findings-2026-08-18-ovs.md:44-50`：
s1 上 130 條規則，OUTPUT 直方圖 `[('2',96), ('CONTROLLER',2), ('3',1), ...]`。

**而且 ARP 是被明確忽略的**（`intelligent_router.py:776-779`）：

```python
# Ignore ARP packets
arp_pkt = pkt.get_protocol(arp.arp)
if arp_pkt:
    return
```

ARP → 命中 table-miss → punt 到控制器 → handler 直接 `return`，不發 packet-out、不 FLOOD → **丟掉**。
**跟 P4 端的結局完全相同。** 兩邊都靠拓撲腳本預灌的 static ARP（`p4_testbed_topo.py:461-470`）讓 host 根本不需要 ARP。

**建議改法：**

> ② **The pipeline no longer discards non-IPv4 frames.**
> TCP/UDP/ICMP are parsed so the 5-tuple key can be built. ARP and other non-IPv4 frames now
> reach an L2 table instead of falling off the end of ingress; with no L2 entries installed
> they are punted to the controller — **the same place OVS sends them**, since the Ryu app
> ignores ARP too. Both fabrics rely on the static ARP the topology script pre-populates.

這個版本的優勢：它把「跟 OVS 對等」講出來，而那是**可以驗證的真話**。
比「我們把 ARP 修好了」強得多 —— 後者會被追問，然後得當場收回。

---

### 🟡 11-3 ③ per-port counters — `egress_port_counter` 沒有生產讀取端

**目前的寫法**（`:233`）：

> ③ 遙測在 pipeline 裡產生：direct/per-port counters、TTL guard、1/256 clone-to-CPU。

**「direct counters」完全成立** —— `flow_5tuple_counter` 和 `ipv4_lpm_counter`（`ndtwin_switch.p4:263-264`）
綁在 table entry 上，透過 `/stats/flow/<dpid>` 以 Ryu 的形狀回報給 kernel 的 Classifier。**這條路是活的。**

**「per-port counter」目前沒有接上任何東西：**

| 層 | 狀態 |
|---|---|
| P4 pipeline 累加 | ✅ 真的在跑 |
| proxy 讀它 | `read_egress_counter()` 在 `p4_client.py:555`，**沒有任何生產呼叫點**（只有測試叫它）|
| emitter 打包成 sFlow type 2 | ❌ `sflow_emitter.py` 只有 `SAMPLE_TYPE_FLOW = 1` |
| kernel 收 type 2 | 就算送過去也會被丟 —— `FlowLinkUsageCollector.cpp:1088` 的 `if (m_mode == MININET) continue` |

`doc/2026-07-27_p4_bmv2_support_plan.md:56` 已經記錄：「proxy 裡誰呼叫 `read_egress_counter`｜**沒有人**（只有測試呼叫它）」。

**這不算缺陷，而且模板 `:154` 已經把理由寫對了**（「counter-sample 半邊未做——但這與 OVS 行為對等，
MININET 模式本來就丟棄 counter sample」）。鏈路使用率實際上是從 flow sample 經 `m_counterReports` 算的。

**建議：條列文字不用改**，但如果被問到「per-port counter 拿來做什麼」，
**不要**答「算鏈路使用率」—— 正確答案是「它是 counter sample（Phase 5 未做的那一半）的預備輸入，
目前沒有生產讀取端；鏈路使用率走的是 flow sample」。

⚠️ **有個相關的坑，如果將來要接它，先讀這段：** `read_egress_counter` 在兩條失敗路徑上都靜默回 `(0, 0)`
（p4info 裡找不到 counter、`except Exception: pass`）。持續失敗的 gRPC 和「這條 link 閒置」在下游無法區分。
計畫書 `:72-79` 明寫**現在不修**，因為正確的失敗訊號長什麼樣取決於將來輪詢它的那個 caller。

⚠️ **順帶一條文件更正（不影響投影片，但別再被它誤導）：**
`doc/2026-07-29_HANDOFF.md:944` 把 `egress_port_counter[255]` 的 1 packet 讀成「clone 到 CPU port 的實證」。
**依現在的 egress 邏輯那是錯的** —— clone 在 `:422` 就 `return` 了，不會計數。
index 255 上的數字來自走 `send_to_cpu()` 的真 packet-in 和 LLDP beacon（`instance_type` 是 NORMAL，會被計數）。
`doc/2026-08-15_bmv2-performance-report.md:137` 已經標記那個結論「要重讀」，這裡把重讀的結果寫下來。

### 🔵 11-4 `default_action = send_to_cpu()` 是 catch-all，而 proxy 收到後直接丟掉

**Page 11 沒有講到這件事，但如果有人問「沒有路由的封包會怎樣」，現在的答案不好聽。**

P4 程式在 table-miss 這件事上**同時用了兩種哲學，而且不一致**：

| 機制 | 做法 | 屬於哪派 |
|---|---|---|
| LLDP | `else if (etherType == TYPE_LLDP) send_to_cpu();` — 編譯進去的**專屬分支** | ✅ selective punt，教科書等級 |
| `ipv4_lpm` | `:339` `default_action = send_to_cpu();` | ⚠️ **catch-all** |
| `l2_forward` | `:358` `default_action = send_to_cpu();` | ⚠️ **catch-all** |

而 proxy 的 `handle_packet_in`（`topology_manager.py:962`）**只解析 LLDP**，其餘的只留一個時間戳就丟掉。

> **現況＝付了上送的成本，什麼都沒買到。** 一個找不到路由的 IPv4 封包會佔用一次 gRPC stream 傳輸
> 和一次 proxy 解析，然後被丟棄；而那條 `stream_recv_thread` 同時扛著遙測和 LLDP 解析。

⚠️ **這是讀程式碼的推論，沒有實測過負載下的影響。** 三個方向：

| 做法 | 得到 | 失去 |
|---|---|---|
| A. 改成 `drop()` | 最省，一行改動 | 失去「有流量但沒路由」的訊號 |
| **B. 保留上送但真的用它**（建議） | 一個「多少封包沒有路由」的計數器 | 要寫新程式碼 |
| C. 上送 + 限速 | 兩者兼顧 | v1model 的 meter 要另外接控制平面 |

**B 之所以值得，是因為它同時回答 OVS 側那個未修的診斷缺陷**
（`doc/audit/2026-08-18_live-full-stack-round/live-findings-2026-08-18-ovs.md:44-62`：
flow 命中 prio-0 table-miss 解析出 `OFPP_CONTROLLER` = 4294967293，
kernel 的錯誤訊息卻叫人去拓撲檔找一條不可能存在的鏈路）。
**兩邊是同一個問題的兩面：「這條流量沒有路由」現在沒有任何地方誠實地說出來。**

💡 一個省事的發現：三張表都**沒有**宣告 `const default_action`，
所以 default entry 在 P4Runtime 上是**執行時期可改的**——A/B/C 理論上不需要重編 P4 就能試。
（不過 proxy 目前沒有寫 default entry 的程式碼。）

---

### 🔵 11-5 右側垂直流程圖：三張表不是循序階段

**目前的寫法**（`:232`）：

> 右側**垂直流程圖**：Parser → `flow_5tuple`（強調色框）→ `ipv4_lpm` → `l2_forward` → Egress。

**問題：** 這個排法讀起來像五個依序經過的階段。實際上三張表是**同一個 control（`MyIngress`）裡互斥的分支**，
一個封包最多只會碰到其中兩張（`flow_5tuple` miss → `ipv4_lpm`）：

```p4
if (hdr.ipv4.isValid()) {
    if (!flow_5tuple.apply().hit) { ipv4_lpm.apply(); }
} else if (etherType == TYPE_LLDP) {
    send_to_cpu();
} else {
    l2_forward.apply();
}
```

**對到 v1model：** 圖上的四、五個方框其實只對應到 **2 個 programmable control**（`MyIngress` + `MyEgress`），
中間還隔著**不可程式化的 Traffic Manager**（複製真正發生的地方）。

**建議：** Page 12 已經把這件事畫對了（`:242-259` 的 ASCII 規格，三張表在同一個 `MyIngress` 框內，
Traffic Manager 灰底）。Page 11 的簡圖如果保留，至少要讓 `flow_5tuple` / `ipv4_lpm` / `l2_forward`
視覺上屬於同一個框，或加一行 `one control, three branches`。

⚠️ **另外要核對已產出的投影片：** 如果圖上把 `TTL guard` / `1-in-256 clone` 標在 **Egress** 之下，那是錯的 ——
TTL guard 在 `ipv4_forward` 這個 **ingress action** 裡（`ndtwin_switch.p4:276`），
clone 的判斷在 **ingress apply**（`:383-391`）。**Egress 裡只有 counter。**
（Page 12 的 ASCII 規格是對的，這條只針對 Page 11 的簡圖與已渲染的成品。）

---

## Page 12 — Inside the pipeline

### ✅ 12-1 ASCII 規格逐行查證正確

`:242-259` 的圖與 `ndtwin_switch.p4` 完全吻合：兩個出口（`packet_out` / LLDP）都在轉發表之前、
TTL guard 和 1-in-256 標在 `MyIngress` 內、Traffic Manager 灰底標 not programmable、
`MyEgress` 只有「是複本就貼標頭不計數 / 否則計 counter」。

左欄三段（`:265`）也正確，特別是 ③「Cloning is not ours（ingress 只是標記，複製由 Traffic Manager 做）」——
這是 v1model 最容易講錯的一點，寫對了。

### 🔵 12-2 可考慮加一行：哪些表有 control-plane writer

如果 Page 11 採用了上面的改法（明講 `flow_5tuple` 尚未接上），Page 12 的圖可以呼應：
把 `flow_5tuple` 和 `l2_forward` 用虛線框或加註 `(no control-plane writer yet)`。

**好處：** 這頁的目的是「讓聽眾看到 pipeline 的全貌」，把「哪些已接上／哪些是預留」畫進去，
比事後被問「那這張表有在用嗎」好。**壞處：** 會沖淡「新增功能」的視覺印象。**由 Adam 裁決。**

---

## Page 13 — The P4 proxy agent

### 🔵 13-1 ③ 「只有 `/p4/` 是新詞彙」— 目前有兩個端點，括號只涵蓋一個

**目前的寫法**（`:272`）：

> ③ 只有 `/p4/` 是新詞彙——Ryu 沒有對應物可模仿的（switch liveness）才另立命名空間。

**查證結果：** 目前 `/p4/` 命名空間下有**兩個**端點，都由 kernel 消費：

| 端點 | 定義 | kernel 呼叫處 |
|---|---|---|
| `GET /p4/switch_state` | `api_routes.py:277` | `DeviceConfigurationAndPowerManager.cpp:836`（`pingWorker` 每秒一次）|
| `POST /p4/readopt/{dpid}` | `api_routes.py:241` | `P4PowerStrategy.cpp:55-129`（powerOn 第二步）|

括號裡的「switch liveness」只涵蓋第一個。readopt 是**電源循環後的重建**，是另一個 Ryu 沒有對應物的動作。

**建議改法：**

> ③ 只有 `/p4/` 是新詞彙——兩個端點，都是 Ryu 沒有對應物可模仿的：
> `switch_state`（liveness 證據）與 `readopt/{dpid}`（重開機後重建 mastership／pipeline／clone session／路由）。

⚠️ **給未來的自己（重要）：** 這兩個端點在 kernel 端是用 **base URL 字串拼接**呼叫的，
所以 `grep "/p4/" src/` **會回傳零筆**。不要因此判定它們是死碼 —— 改搜 `pingWorker` / `fetchP4SwitchState`。
同樣的陷阱：`grep "switch_state" src/` 也是零筆。

### 🔵 13-2 「重寫 Ryu 北向 API」的一個小保留

`:272` ① 列出的端點裡有 destination paths。
`/ryu_server/all_destination_paths` **不是 stock Ryu 的路由**，是實驗室前人加在
`intelligent_router.py` 裡的（`get_all_paths`，`:1003`）。

「重寫 Ryu 北向 API」講起來沒錯，但如果有人問「Ryu 原本就有這個嗎」，答案是**沒有，那是這個實驗室加的**。
不影響簡報文字，記在這裡避免被問倒。

### 🔴 13-3 模組表的行數過期了，8 個裡有 5 個要更新

模板 `:274` 註明這張表是「目前檔案大小，不是 diff 行數」，而 A2b（`:104`）要求**每個實測數字都要標它量在哪個 commit**。
這張表沒標，而且已經對不上了。

**2026-08-19 於 HEAD `04b8933` 實測（`wc -l p4_proxy/proxy_agent/*.py`）：**

| 模組 | 投影片 | 實測 | 差 |
|---|---|---|---|
| `topology_manager.py` | 1,392 | **1,516** | +124 |
| `p4_client.py` | 587 | **755** | **+168（+29%）** |
| `api_routes.py` | 256 | **366** | +110 |
| `kernel_notifier.py` | 144 | **184** | +40 |
| `main.py` | 305 | **321** | +16 |
| `sflow_emitter.py` | 448 | 448 | ✓ |
| `ryu_topology.py` | 338 | 338 | ✓ |
| `ryu_flow_stats.py` | 190 | 190 | ✓ |
| **總計** | **3,660** | **4,118** | **+458** |

**建議：** 重新量並在表下加註 `Current file sizes at 04b8933, not diff counts.`
—— 順手就把 A2b 的要求補上了。

### 🔵 13-4 `topology_manager.py` 的職責描述漏了兩塊

**目前：** `Graph state, BFS routing, LLDP beacons`

漏掉的是最近才加、而且在第 1 節有專頁的兩塊：**liveness polling**（Page 16 整頁在講）
與 **link watchdog / readopt**（Page 17、Page 18 在講）。
描述停在這三項，會讓聽眾以為 Page 16-18 的東西住在別的檔案裡。

**建議改成：** `Graph state, BFS routing, LLDP beacons, liveness & link watchdog`

（實際的六塊職責：① 圖狀態 ② 路由計算與安裝 ③ OpenFlow→P4 翻譯 ④ LLDP 全套
⑤ 存活與鏈路看門狗 ⑥ readopt。表格欄位塞不下六項，取四項即可。）

### ➕ 13-5 一組可以放進 Page 13 或 Page 27 的量級對照數字

**2026-08-19 實測（本機 `ryu-env` 裡的 Ryu 4.34）：**

| | 行數 |
|---|---|
| **Ryu 全部** | **172,708** |
| `ofproto_v1_3_parser.py` + `ofproto_v1_3.py`（OpenFlow 線路編碼） | 7,752 |
| `controller/` + `topology/` | 4,094 |
| `app/ofctl_rest.py` + `lib/ofctl_v1_3.py` + `lib/ofctl_utils.py` | 2,404 |
| **同功能子集小計** | **14,250** |
| **扣掉線路編碼後** | **≈ 6,500** |
| **我們的 proxy** | **4,118** |
| （實驗室自寫的 `intelligent_router.py`，另計） | 1,012 |

> 🎯 **可以直接講的一句話：扣掉 OpenFlow 的線路格式編碼（protobuf 免費給我們），
> 我們的 proxy 跟 Ryu 的對應子系統是同一個數量級。那 7,752 行的差距，全部來自
> 「自己編碼 vs protobuf 幫你編碼」。**

這比「我們寫了 4,118 行」有力得多，因為它說明了**P4Runtime 相對 OpenFlow 省掉了什麼**。

---

## ➕ 建議新增（一）：`topology_manager.py` 需要拆

**1,516 行，是 proxy 裡最大的檔案，也是最該拆的一個。** 裡面至少有三個彼此獨立的責任：

| 責任 | 主要函式 | 大致範圍 |
|---|---|---|
| **圖狀態與路由** | `add_switch` `:379`、`calculate_all_paths` `:458`、`install_initial_routes` `:691` | networkx 圖、BFS、路由安裝 |
| **LLDP 與存活** | `create_lldp_packet` `:914`、`handle_packet_in` `:962`、`start_liveness_polling` `:1049`、`check_link_beacons` `:1263`、`run_watchdog_pass` `:1373` | beacon 收發、存活證據、鏈路看門狗 |
| **規則翻譯** | `unsupported_match_fields` `:106`、`route_flow` `:536`、`unroute_flow` `:625`、`modify_flow` `:654` | OpenFlow match/action → P4Runtime |

**為什麼這比很多技術項目更值得寫進 future work：**

1. **它是可驗證的觀察，不是主觀評論。** 三組函式之間幾乎沒有共用狀態，切面是清楚的。
2. **切面已經在程式碼裡浮現了，只差沒切。** 這個類別已經有**兩把彼此獨立的鎖**：
   `_net_lock`（RLock，護圖）與 `_liveness_lock`（Lock，護 beacon／存活簿記），
   而且 `:288` 與 `:306` 的註解明寫兩者**「never held at once」**。
   一個類別內部需要兩把互不相干的鎖，通常就是兩個類別的意思 —— 這條不是主觀感受，是現成的證據。
3. **跨責任的執行緒約束是這種巨型類別最容易搞錯的地方。** 例如
   「`handle_packet_in` 跑在 gRPC receive thread，所以不能在裡面發 HTTP」
   （`:982-986` 的註解：一個三秒逾時的 HTTP 呼叫會卡住這台後面每一台的 packet-in），
   所以鏈路失效是**記在這裡、由 watchdog 回報**。這種約束在拆開之後會變成型別／介面上看得見的東西。
4. **它是誠實的自我評估。** 一整節在講 baseline 的缺陷，自己的碼也交出一條結構性的待改項，
   比只講別人的問題好看得多 —— 這正是 `:61` 那條「功勞與缺陷的不對稱是本次改版要修掉的」的同一個精神。

**放哪裡：** Page 20（Four smaller pieces）或收尾頁的 future work。
與另一條 future work（下面的非同步回報）並列時，這條是**結構**、那條是**架構**，可以一起講：
「一個要拆檔案，一個要改回報模型。」

---

## ➕ 建議新增（二）：一個誠實而且有份量的 future work

**目前沒有任何一頁講到這件事，但它是整套系統最大的單一結構落差。**

`processFlowBatch`（[`src/ndt_core/http/HttpSession.cpp:1055-1076`](../NDTwin-Kernel/src/ndt_core/http/HttpSession.cpp)）
是**非同步**的：enqueue 之後立刻回 `200 {"status":"queued"}`，dispatcher 之後才在 per-DPID worker thread 上真的送出去。

**後果：proxy 回的 400 傳不回 app。** 上面 11-1 講的「拒絕優於假裝成功」，在 caller 那一端看到的仍然是 200。

程式碼裡的註解自己講得很清楚：

> FlowDispatcher is asynchronous by design (bursts of up to 2000, one worker per DPID), so the
> entries are still sitting in a queue at this point and no request has reached the controller yet.
> **A rejected rule or an unreachable controller was therefore reported as a completed installation.**

措辭已經從「Flows installed」改成「queued」（誠實了），但 HTTP status 刻意維持 200：

> Kept as HTTP 200 rather than 202 Accepted: 202 would be more accurate, but callers that check
> for exactly 200 would break, and this is the endpoint every writing app uses.

而且同一段註解記錄了：兩個會寫 flow 的 app **都把 response 丟掉**
（Energy-Saving-App `:225`/`:241` 不接回傳的 `std::optional<uint32_t>`、TE-App `:572` 不 assign `requests.post` 的結果）。

**為什麼值得放進簡報：** 註解自己下的結論是「Reporting per-entry status to the caller needs either a
synchronous path or a completion handle — **an architectural decision, not a wording one**」。
這是一個**已經分析清楚、有明確兩條路、但刻意沒做**的架構決策 —— 正是 future work 該長的樣子。

**放哪裡：** Page 19（Robustness）或 Page 20（Four smaller pieces）比較合適；也可以留給 Q&A。

---

## Page 17 — Failover

### 🔵 17-1 「11 秒偵測」要標明它是範圍裡的一個相位

實測數字（`doc/2026-07-27_p4_bmv2_support_plan.md:22, 465-467`，2026-08-10 於 10 台 bmv2）：

- 斷 `s1-eth1` → **11 秒**後三筆 `link_failure_detected` 抵達，圖 40/40 → **37/40**
- 推送的 9 條路徑**零條**從 s1 的 port 1 出去，h1 全改走 `1(p2) → 6`，push 0 次失敗
- 取樣 40 次／119 秒**只出現 `up=37/40` 一種狀態**；連同斷線起算共 **238 秒、約 7–8 個輪詢週期**
- `ifconfig up` 後 **14 秒**回到 40/40、12 條路徑

⚠️ **11 秒不是設計值，是相位的結果。** 超時是從**最後一張 beacon**算起，不是從斷線那一刻：

```
LINK_BEACON_TIMEOUT_S = 15 s，beacon 每 5 s，watchdog 每 5 s
→ 最後一張 beacon 落在斷線前 0~5 s
→ 超時在 T+10 ~ T+15 觸發，watchdog 在下一次巡邏（≤5 s）才報
→ 偵測延遲的真實範圍是 10 ~ 20 秒
```

投影片如果只寫「11 秒偵測」，被問「為什麼不是 15 秒」會答不出來。
**建議寫成「10–20 秒（實測 11 秒）」**，並且準備好那個「從最後一張 beacon 算起」的解釋。

### ➕ 17-2 這一頁最值得講的一點，目前沒有寫

> **「回報失效」和「維持失效」是兩件不同的事，而第二件更容易被忘記。**

`kernel_notifier` 負責第一件，11 秒就送達。
但 kernel 的 `updateLinks()` **只會把邊設成 `true`，沒有任何路徑會把它設成 `false`**——
所以下一次拓撲輪詢就會把死掉的邊復活。

擋住這件事的是 `ryu_topology.render_links(net, down_endpoints=topology.down_link_endpoints())`
在**每一次輪詢回應裡**把那條線抽掉——**一個不同的模組，用完全不同的機制**。

這個 bug 曾經真實存在，`topology_manager.py:1447-1462` 的 docstring 記著：

> 失效報告是真的，它的效果活不過一次輪詢，而且沒有任何地方說。

（順帶：同一段 docstring 記錄 kernel 的輪詢間隔是**前 90 秒 5 s、之後 30 s**，
不是曾經誤植的 1 s；238 秒 ÷ 30 s ≈ 7–8 個週期就是這樣對上的。）

---

## ➕ 建議新增（三）：`p4runtime_lib` 可以取代手刻的南向層

`~/tutorials/utils/p4runtime_lib`（**967 行，已經 clone 在本機**）與我們手刻的部分對應：

| 檔案 | 行 | 對應我們的 |
|---|---|---|
| `helper.py` | 208 | `p4_client.py:414-467` 那六個 p4info ID 查找私有方法 |
| `switch.py` | 246 | 連線 + StreamChannel 管理 |
| `convert.py` | 150 | `socket.inet_aton` / `bytes.fromhex` 那些值編碼 |
| **`error_utils.py`** | **85** | **我們沒有這個** ← 最有價值的一塊 |

⚠️ `error_utils.py` 值得單獨看：它解析 P4Runtime 的 `google.rpc.Status` details，
裡面有 bmv2 塞進去的**每個 update 的個別錯誤**——比只看頂層 status code 精確得多。
而「bmv2 幾乎什麼都回 UNKNOWN」是這個 repo 已經記錄在案的痛點
（`insert_ipv4_route` 花了十行註解講「UNKNOWN 同時代表重複和真錯誤，所以改成 retry as MODIFY 消歧」）。

**這是「換掉 `p4_client.py` 裡手刻的一層」，不是「換掉 proxy」。** 可替換的切片是 755 / 4,118 ≈ **18%**。

**結構性論點（值得放進簡報或口述）：**
沒有任何現成的 P4 控制器會發 Ryu 形狀的 `/v1.0/topology/links`（dpid 十六進位）、
`/stats/flow/<dpid>`（action 字串形式），或與 OVS **位元組同形狀**的 sFlow v5。
因為沒有人在做「讓既有的 OVS 控制器以為自己還在跟 OVS 講話」這件事——
**而那正是這個專案的命題**。換掉北向 = 放棄「七個元件不必改」這個前提。

---

## ⚠️ 放進簡報前必須先查證的（我只有知識，沒有現場驗證）

模板 A3「事實查證規則」適用。以下三條**目前不要寫進投影片**：

| 待查證 | 我的認知 | 為什麼重要 |
|---|---|---|
| **Ryu 專案的維護狀態** | 4.34 是最後的 PyPI 發行（本機裝的就是 4.34），專案實質停止維護，開發轉移到 OpenStack 的 `os-ken` fork | 「我們依賴一個停止維護的框架」是很強的論點，但講錯會很難看 |
| **ONOS / Stratum / PINS / p4runtime-shell 的現況** | ONOS 有完整 P4Runtime 南向（Trellis/SD-Fabric）；Stratum 是**交換機 OS 不是控制器**；PINS 綁 SONiC；OpenDaylight 的 P4 plugin 長期停滯 | 若要在簡報上主張「沒有現成品可移植」，這張表要站得住 |
| **liveness prober 的循序探測邊界** | 10 台 × `LIVENESS_PROBE_TIMEOUT_S`(1.5 s) = 一輪最壞 15 s，而 kernel 的 `kProbeStaleSeconds = 15.0` → 全部逾時時第一台會在下一輪回來前就被判 `Unknown` | **只是把兩邊常數放在一起算的，沒有實測。** 結果其實是對的（全滅時答 Unknown 比 Down 保守正確），但它看起來像巧合而非設計；交換機數量或 timeout 一改，這個關係會無聲變化 |

---

## 🧹 順手可清的小東西（與投影片無關）

- `p4_proxy/proxy_agent/api_routes.py:1` — `BackgroundTasks` 被 import 但整個檔案沒用到，死 import。
  （註：若將來要修「proxy 的 400 傳不回 app」，`BackgroundTasks` 是**錯的**工具——正確方向是 completion handle。）

---

## 📌 已查證、可直接用的簡報材料（這輪新增）

**① LLDP：「規則 vs 編譯進去的分支」——OpenFlow/P4 分工哲學最乾淨的例子**

| | OVS / Ryu | P4 / bmv2 |
|---|---|---|
| 攔截 LLDP 的方式 | **執行時期的一條 OpenFlow 規則**（prio 65535，`eth_type` + `eth_dst`，可刪，`install_lldp_flow` 是個 CONF 開關）——`ryu/topology/switches.py:643-657` | **編譯進 binary 的一個分支**（`ndtwin_switch.p4:373-375`，只比 `eth_type`），要改必須重編＋重推 pipeline |
| 封包格式 | 真 LLDP TLV（Chassis ID / Port ID / TTL / End） | **Ethernet + ASCII 字串** `DPID:1,PORT:2`，27 bytes，零個 TLV |
| 那個 dst MAC `01:80:c2:00:00:0e` | **是規則的一半**（載重） | **純裝飾**（沒有任何地方讀它） |
| 用途 | 只做拓撲發現 | 拓撲發現 **＋ switch liveness 證據** |

第四列是 bmv2 特有的必要性：**bmv2 會回答 control-plane RPC 而不管 pipeline 有沒有在轉發**，
所以 LLDP 是唯一能證明資料面還活著的證據。這正好呼應 Page 16 ② 已經寫對的「探測是真的 round trip」。

**② probe 與 beacon 是兩個不同的問題，缺一不可**

> **probe 問「你還在嗎」（走控制面），beacon 問「你還在做事嗎」（走資料面）。**

| 症狀 | probe | beacon | 真相 |
|---|---|---|---|
| 行程被殺 | ❌ | ❌ | 整台死了 |
| 一條線被拔 | ✅ | ❌（其他線還有） | 只有那條線壞 |
| **pipeline 卡住** | **✅ 正常回答** | ❌ | **交換機聾了，線沒事** |
| 剛開機還沒推 pipeline | ✅ | ❌ | 正常，等就好 |

第二、三列的 probe 和 beacon 讀數**完全相同**，真相卻不同——這就是為什麼
`reroutable_down_endpoints` 必須交叉比對兩個訊號（`probe_ok` + 反向 beacon 是否還活著）。

kernel 端也用到組合（`DeviceConfigurationAndPowerManager.hpp:365`）：
`probe_ok` false **但** beacon 在 `kLldpFreshSeconds`(12 s) 內到過 → **不判 Down**。
**資料面的證據壓過控制面的證據。**

---

## ✅ 已查證正確、不用改（記錄以免下輪重查）

| 項目 | 位置 | 查證結果 |
|---|---|---|
| **v1model** | Page 27 技術欄 | 確認。`#include <v1model.p4>`（`:32`）、`V1Switch(...) main;`（`:475-482`）、`p4c-bm2-ss --arch v1model` |
| **482 行** | Page 11/12 腳註 | `wc -l` 確認 |
| **clone session 250** | Page 15 ① | 正確。`SAMPLE_SESSION = 250`（`:45`）是任意的 PRE session ID，P4 程式命名、控制平面填內容；「沒 pipeline 時 bmv2 會拒絕」屬實（`FAILED_PRECONDITION`）|
| **第三個 controller header 被默默忽略** | Page 15 ③ | 正確，`ndtwin_switch.p4:119-133` 有完整說明（PI 按名字匹配，只認 `packet_in`/`packet_out`）|
| **counter sample 未做 = 與 OVS 對等** | `:154` | 正確。`FlowLinkUsageCollector.cpp:1088` 的 `if (m_mode == MININET) continue` 證實 MININET 模式本來就丟棄 counter sample |
| **Unknown 不動 graph** | Page 16 / `:292` | 正確。`DeviceConfigurationAndPowerManager.cpp` 的 `pingWorker` 兩條分支都是 `case Unknown: break;` |
| **P4 liveness 是證據政策，OVS 是本機查詢** | Page 16 | 正確。`ovsLivenessFor` 3 行（`:349-359`）；`p4LivenessFor` 約 100 行、六個 Unknown 出口（`:367-471`）|
| **七個 consumer 只用 `/ndt/`** | Page 4 ② 前半 | 正確。零共享記憶體屬實（共享**檔案**的部分見 4-1）|
| **SPM「平行跑模擬案例」** | 第 1 節背景 | 正確（我先前判斷錯，已更正）。`run_simulator` 每個 case fork 自己的 `bp::child`，`bp::on_exit` 非同步，`active_processes` 是 map。`thread_count = 1` 只限制 SPM 自己的 HTTP event loop |

---

## 附錄：查證時踩到的 grep 陷阱（給下一輪）

1. **base URL 拼接** —— `grep "/p4/" src/` 回傳零筆，但 kernel 兩個端點都在呼叫。改搜函式名。
2. **`grep -rn "ryu|grpc|:8080"`** 會命中 `memo**ryU**tilization` / `maxMemo**ryU**sage`，
   差點誤判 Visualizer / Web-GUI 有碰 control plane。
3. **`| head -N` 之後不要拿它當總數。**

---

*[Co-developed with claude code -- Adam]*
