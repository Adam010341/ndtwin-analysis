# `fig_t1b_requirements_matrix_0927` —— 13 支 tutorial exercise 的需求 vs. NDTwin 的供給（09-16 與 09-27 兩列）

[Co-developed with claude code -- Adam]

## 930 副本的來源（2026-09-27 複製）

- 本圖、本檔與產生器是從 `NDTWIN slide material 916/figures/p4-tutorials/` **複製**（不是移動）而來：`make_tutorial_figs_0927.py` 與 09-27 19:59 的產物。916 那份原封不動。
- 複製後只改了兩處：本節，以及下方「重生指令」的 `cd` 路徑改指 930。圖的資料、解析與斷言一字未改；OUT_DIR 本來就是腳本所在目錄，所以產物寫進 930。
- **四個判斷格已由 Adam 裁定（2026-09-28）**：NDTwin 09-27 列的 `registers`＝部分、`queue_metadata`＝做得到；twin sees it 欄的 multicast＝綠、flowcache＝只看過 IPv4。GAP-2b 在裁定前是**未提交的觀測**（`git status` 顯示 `??`，09-28 06:5x UTC 查），coordinator 讀過 diff 後提交。
- 🔴 flowcache／solution 的 G1 在 T06 判 PASS，但 iperf 0 個 datagram 到 h3（GAP-2b §4-1）——那一格**不能當送達的證據**（存檔圖；deck 的 T1 用 `fig_t1c`，兩張圖該格都是 IPv4 only）。

## 一句話

**13 支 p4lang/tutorials exercise 各自需要 16 個能力維度中的哪幾個（上半），對照 NDTwin 在 09-16 與 09-27 兩個時間點各做得到哪幾個（底下兩列）；右側兩欄說每一支今天是否在 NDTwin fabric 上兩臂照預期跑過、twin 的鏈路使用率有沒有跟上它的流量。**

## 🔴 底下兩列回答的是兩個不同的問題

- **NDTwin 09-16**（解析自 GAP-2 §1）：「今天、不改任何一行碼，**NDTwin 自己那支 P4 程式**（`ndtwin_switch.p4`）提供得了這一維嗎？」全部【讀碼】，trunk `1a284f75`。
- **NDTwin 09-27**（解析自 GAP-2b §1）：「需要這一維的每一支 exercise，今天都在 NDTwin fabric 上跑得起來；而且這一維裡歸 NDTwin 負責的那一半是 NDTwin 的碼做的。」判準與每維「歸 NDTwin 的那一半」寫在 GAP-2b §0；證據是 T06 的 live raw＋trunk `7746832e` 的讀碼，逐格標等級。
- ⇒ **09-16 → 09-27 的變化，一部分是 NDTwin 多做了事，一部分是題目本身把責任移給了 exercise 的程式**（路線 2：exercise 帶自己的 `.p4`）。GAP-2b §2 逐維說是哪一種。講圖時不要把兩列說成「同一把尺量了兩次」。

## 資料來源（圖上每一格都出自這裡，腳本裡沒有手抄的格值）

| 用途 | 檔 | 章節 |
|---|---|---|
| 需求矩陣 13×16 | `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/GAP-1-exercise-requirements.md` | §2a 資料面／§2b 控制面／§2c 拓樸與驗證 |
| `meters`／`digest` 兩欄（§2 沒有這兩欄） | `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/GAP-1-exercise-requirements.md` | §4b 的 `meters`／`digest` ＝ **0 支** |
| 對帳斷言（幾支要） | `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/GAP-1-exercise-requirements.md` | §4a、§4b |
| NDTwin 09-16 1×16 | `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/GAP-2-ndtwin-p4-capabilities.md` | §1 能力矩陣＋「計數」那一行 |
| NDTwin 09-27 1×16 | `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/GAP-2b-ndtwin-p4-capabilities-2026-09-27.md` | §1 能力矩陣＋「計數」那一行 |
| 右側兩欄 13×2 | `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/GAP-2b-ndtwin-p4-capabilities-2026-09-27.md` | §3 逐支表＋「彙總」那一行 |
| 右側兩欄的對帳對象（不取值，只比對） | `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/2026-09-27T074635Z_06_thirteen/00_table.tsv` | 26 臂的 rc／verdict／report |
| 列序（上→下） | `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/GAP-ANALYSIS.md` | §6 三階段（定序）、§4 逐支可行性表（同序，做交叉驗證） |
| 色票 | `/home/adam/Desktop/NDTwin slide material/NDTwin slide material 827/NDTwin-slide-template-827.md` | §E2 色票與字體 |

## 可信度

- **需求側 13×16**：🟠【讀碼推導】。GAP-1 §0「本輪一個封包都沒送、一支 exercise 都沒跑」。與 09-16 的舊圖逐格相同（同一支解析、同一份 GAP-1）。
- **NDTwin 09-16**：🟠【讀碼推導】。GAP-2 §0「全部是【讀碼推導】」。
- **NDTwin 09-27**：逐格混合，**每格的證據等級寫在 GAP-2b §1 那一格裡**，不在圖上。16 格中 14 格的依據含【跑過】；2 格只有【讀碼】：`meters`, `digest`。
- **右側 runs on NDTwin**：🟢【跑過】。來自 GAP-2b §3 的骨架臂／解答臂兩欄，本腳本再逐臂對 T06 的`00_table.tsv` 斷言 verdict、rc、report 時間戳一致（見下方對帳）。
- **右側 twin sees it**：🟢【跑過】的 G1 結果＋一層歸類判斷（見下一節）。
- 🔴 T06 的 raw（`runs/`、`live-p1/runs/`）在 NDTwin-Kernel 的 checkout 裡**未進版控**；是 audit-raw 的材料。

## 圖怎麼讀

- **上半 13 列**＝需求側，三色階（深藍`關鍵`／中藍`用到`／極淡`沒用到`）。
- **隔線之後兩列**＝`NDTwin 09-16`、`NDTwin 09-27`，同一組三色階（綠`做得到`／琥珀`部分`／灰`做不到`），但兩列的判準不同（見上）。
- **右側兩欄**只對 13 支 exercise 列有格，NDTwin 兩列那裡是空的。
- **列序**由階段決定，階段之間留一道空白（沒有文字）：階段一＝['basic']（§6 解鎖欄「1 支真跑通」＋驗證欄點名）；階段二＝['qos', 'ecn', 'mri', 'firewall', 'basic_tunnel', 'source_routing', 'calc', 'link_monitor', 'load_balance']（§6 解鎖欄 +9 支的名單，逐字照抄順序）；階段三＝['multicast', 'p4runtime', 'flowcache']（餘數；§6 第三階段解鎖欄點名了 ['multicast', 'flowcache']，p4runtime 是餘數推得、§4 表也把它排在該位置）。
- **欄序**＝ GAP-1 §1 定義表的 16 個鍵順序，最右兩欄是窄條。

## 右側兩欄是什麼

**runs on NDTwin**（綠＝是、灰＝否）：該支在 T06（`live-p1/runs/2026-09-27T074635Z_06_thirteen`）裡骨架臂紅如預期、解答臂綠。解析規則：GAP-2b §3 的骨架臂欄以「紅如預期」開頭**且**解答臂欄以「綠」開頭。「紅如預期」的定義照 `live-p1/06_thirteen.sh:107-115`：骨架臂 `PASS`／rc 0，或設計上的拒絕 `RED ARM`／rc 1（basic_tunnel、flowcache）。

**twin sees it**（GAP-2b §3 最後一欄開頭的粗體字）：

| 色 | GAP-2b 的字 | 意思 |
|---|---|---|
| 綠 `#2F7D4F` | 看得到 | 解答臂的 G1「link usage follows the iperf path」PASS，而 G1 跑的那條流屬於這支 exercise 自己的流量類別（IPv4 exercise；p4runtime 的 iperf 走了 0x1212 tunnel） |
| 琥珀 `#E3A21A` | 只看過 IPv4 | G1 PASS，但用的是一般 IPv4 iperf；這支 exercise 的自訂標頭流量（0x1212 tunnel、0x812 probe、MRI option）從沒被量過 |
| 白底斜線 `#9AA0A5` | 無證據 | G1 NOT RUN（該支的程式丟掉一般 iperf），也沒有別的 raw |

⚠️ 這一欄**只講鏈路使用率這一層**：G1 斷言「真的搬了位元組的介面，twin 的積分 > 0；沒搬的，積分在一個樣本的量之下」。它**不**斷言流量送達（GAP-2b §4-1 的 flowcache 就是 G1 PASS 而 iperf 沒到終點），**不**斷言流身份，**沒有**逐支的陽性對照（只有 live-p1/05 在 basic 上做過）。細節在 GAP-2b §3.1。

## 我做的歸類判斷

### 需求側（與 09-16 舊圖相同，原文照錄）

**機械規則**（先跑，三條）：

1. 格值是 `—` ⇒ `沒用到`。
2. 格值（去掉 `**` 與反引號後）以「關鍵」開頭 ⇒ `關鍵`。涵蓋 `**關鍵** …` 與 `**關鍵：…**` 兩種寫法。
3. 其餘非空敘述 ⇒ `用到`。**注意**：`**用到但不讀**（bloom filter）`（firewall／registers）與`**跑時控制器**`（flowcache／p4runtime 的 control_plane_mode）都是粗體但**沒有**「關鍵」標記，照規則 3 歸 `用到` —— 粗體本身不代表關鍵。

**攔截器**：任何格值以缺席詞（無／沒有／空／不需要／N-A）開頭、以「都沒有」結尾、帶問號、或以「部分」開頭，而又不在下面的例外表裡 ⇒ **腳本直接 `SystemExit`**，不猜。

**逐格審過的例外（共 3 格）**：

| exercise | 維度 | 原文 | 歸給 | 依據 |
|---|---|---|---|---|
| source_routing | `tables` | **一條 entry 都沒有** | **沒用到** | GAP-1 §4a「`tables` 12/13 —— 只有 source_routing 一條 entry 都沒有」＋GAP-ANALYSIS §4「G5 不需要：**0 筆 entry**」⇒ 歸「沒用到」。本腳本另以 §4a 的 12/13 做斷言，歸錯會當場爆。 |
| calc | `control_plane_mode` | **無**（entry 在 P4 裡） | **沒用到** | GAP-1 §1 把 control_plane_mode 定義成三選一，第③種就是「兩者皆無」；§3.3「`control_plane_mode`＝**無**」⇒ 歸「沒用到」。 |
| source_routing | `control_plane_mode` | 開機 runtime json（**空**） | **用到** | 模式仍是①「開機灌 runtime json」，只是 entry 陣列是空的（GAP-1 §3.13）⇒ 模式有用到，歸「用到」；「空」講的是筆數不是模式。 |

**兩個沒有進圖的欄位**（§2 有、16 維沒有）：

- GAP-1 §2b. 控制面 第 3 欄「灌幾筆／什麼」（未對到 16 維中的任何一個鍵）
- GAP-1 §2b. 控制面 第 9 欄「`idle_timeout`」（未對到 16 維中的任何一個鍵）

  其中 `idle_timeout` 是 GAP-1 §1 自己註明「維度清單外、但必須另立一條」的第 17 維（只有 flowcache 用），本圖照題目給的 16 鍵清單，**不畫它**。

### 供給側兩列與右側兩欄

本腳本**不做任何歸類判斷**：兩列的格值是 GAP-2／GAP-2b §1「今天」欄的三個字之一，右側兩欄是 GAP-2b §3 的開頭字。判斷都在 GAP-2b 裡；還標 `(judgement)`（待審）的是：

- **NDTwin 09-27 那一列**：（無）。
- **twin sees it 那一欄**：（無）。

Adam 2026-09-28 裁定、GAP-2b 標「（Adam 2026-09-28 裁定）」的是：

- **NDTwin 09-27 那一列**：`registers`, `queue_metadata`。
- **twin sees it 那一欄**：multicast, flowcache。

## 解析成功後跑的對帳斷言（任何一條不過就 `SystemExit`）

- §4a `pipeline_load` = 13/13 ✓
- §4a `topology` = 13/13 ✓
- §4a `verification` = 13/13 ✓
- §4a `tables` = 12/13 ✓
- §4a `checksum` = 10/13 ✓
- §4a `ttl_or_hop` = 11/13 ✓
- §4b `counters` = 2 支 ✓
- §4b `digest` = 0 支 ✓
- §4b `meters` = 0 支 ✓
- §4b `packet_io` = 1 支 ✓
- §4b `pre_clone` = 1 支 ✓
- §4b `pre_multicast` = 1 支 ✓
- §4b `queue_metadata` = 2 支 ✓
- §4b `registers` = 2 支 ✓
- GAP-2 計數 做得到1／部分9／做不到6 ✓
- GAP-2b 計數 做得到8／部分6／做不到2 ✓
- GAP-2b §3 彙總 跑得起來13／13、twin 看得到6／只看過 IPv4 4／無證據3 ✓
- GAP-2b §3 的 26 臂 verdict／rc／report 時間戳 == T06 00_table.tsv ✓
- GAP-2b §3 的「紅如預期」「綠」與 T06 的 rc／verdict 依 06_thirteen.sh 規則一致 ✓
- GAP-2b 的內文點名的 live 表就是 `2026-09-27T074635Z_06_thirteen/00_table.tsv` ✓
- 需求矩陣形狀 = 13×16；NDTwin 兩列各 1×16；右側 13×2；16 個鍵集合相同。
- 列序：§4 的 13 列順序 == §6 的（階段一 + 階段二名單 + 餘數），逐位比對。

## 逐格映射：NDTwin 09-16 → NDTwin 09-27

9 格變了：`pipeline_load`, `tables`, `pre_multicast`, `registers`, `custom_headers`, `queue_metadata`, `checksum`, `topology`, `control_plane_mode`。

| 維度 | GAP-2 §1「今天」 | 色階 | GAP-2b §1「今天」 | 色階 | 變了嗎 |
|---|---|---|---|---|---|
| `pipeline_load` | 部分 | **部分** | 做得到 | **做得到** | **變** |
| `tables` | 部分 | **部分** | 做得到 | **做得到** | **變** |
| `pre_multicast` | 做不到 | **做不到** | 做得到 | **做得到** | **變** |
| `pre_clone` | 部分 | **部分** | 部分 | **部分** | — |
| `counters` | 部分 | **部分** | 部分 | **部分** | — |
| `meters` | 做不到 | **做不到** | 做不到 | **做不到** | — |
| `registers` | 做不到 | **做不到** | 部分 | **部分** | **變** |
| `digest` | 做不到 | **做不到** | 做不到 | **做不到** | — |
| `packet_io` | 部分 | **部分** | 部分 | **部分** | — |
| `custom_headers` | 做不到 | **做不到** | 部分 | **部分** | **變** |
| `queue_metadata` | 做不到 | **做不到** | 做得到 | **做得到** | **變** |
| `checksum` | 部分 | **部分** | 做得到 | **做得到** | **變** |
| `ttl_or_hop` | 做得到 | **做得到** | 做得到 | **做得到** | — |
| `topology` | 部分 | **部分** | 做得到 | **做得到** | **變** |
| `control_plane_mode` | 部分 | **部分** | 做得到 | **做得到** | **變** |
| `verification` | 部分 | **部分** | 部分 | **部分** | — |

計數：NDTwin 09-16 做得到 1／部分 9／做不到 6；NDTwin 09-27 做得到 8／部分 6／做不到 2。

### NDTwin 09-27 每格的依據（GAP-2b §1 原文照錄）

| 維度 | 色階 | 一句依據 |
|---|---|---|
| `pipeline_load` | **做得到** | 【跑過】13 支解答臂都在 NDTwin fabric 上跑自己的程式且綠。firewall 同一網路兩份程式（s1 p4info `ef7561c073ee3b7f`、s2–s4 `9213871cee36bd93`）。p4runtime／flowcache 由自己的控制器在跑時推，proxy 標 `pipeline_push` 跳過 |
| `tables` | **做得到** | 【跑過】9 支開機灌表的 exercise，entries 都由 NDTwin 依 p4info 名字寫入，0 failed：firewall 28/28、load_balance 14/14、link_monitor 每台 6（含只有 default 的 `MyEgress.swid`）。p4runtime／flowcache 的表由它們自己的控制器寫（控制面模式 ②） |
| `pre_multicast` | **做得到** | 【跑過】multicast 的 group 由 NDTwin 從 package 的 `multicast_group_entries` 寫入（applied 1、failed 0）。解答臂 h1/h2/h3 互通、h4 收不到 |
| `pre_clone` | **部分** | (b)(c) 【跑過】flowcache 綠，控制器收得到 PacketIn；NDTwin 寫的 clone session 是 0（`pre_entries.clone.applied 0`，`clone_session` 在 skipped），所以 session 是它自己的控制器寫的（推論）。NDTwin 從 package 套 `clone_session_entries` 的路沒有任何一支走過，只有讀碼 |
| `counters` | **部分** | (b)(c) 【跑過】counter 在 NDTwin fabric 上會動：p4runtime s1 `ingressTunnelCounter 100` 到 3505 packets，flowcache 也有讀數。但讀它們的都是 exercise 自己的控制器。NDTwin 的 `GET /p4/counter/{name}` 沒被任何 arm 或 live 腳本呼叫過，只有讀碼 |
| `meters` | **做不到** | 13 支都不需要（GAP-1 §4b）。NDTwin 仍沒有 MeterEntry，北向三個 meter 端點回 `unsupported_on_p4`。只有讀碼 |
| `registers` | **部分** | (a) firewall（bloom filter）與 link_monitor 的 register 在資料面跨封包保持狀態：firewall 擋下 h3→h1，link_monitor 回報非零埠【跑過】。但 NDTwin 沒有任何 RegisterEntry 讀寫路徑，twin 看不到 register 值（讀碼）。（Adam 2026-09-28 裁定）：GAP-1 §4b 說這兩支只需要資料面狀態，照那個讀法是「做得到」 |
| `digest` | **做不到** | 13 支都不需要（GAP-1 §4b）。stream receiver 只認 `packet`／`arbitration`，其餘印一行 unknown 就丟。只有讀碼 |
| `packet_io` | **部分** | (b) 【跑過】flowcache 綠。它要的 CPU port 510 由 NDTwin 從 package 帶進 bmv2 `--cpu-port`（pre-flight PASS 510）。但 packet-in／out 全走它自己的控制器；external 模式下 proxy 不開 stream，NDTwin 對外來程式沒有 packet-io 路徑 |
| `custom_headers` | **部分** | (a) 7 支自訂標頭 exercise 的解答臂全綠【跑過】。但 twin 端只有 p4runtime 的 0x1212 tunnel 流量有鏈路使用率的活證據（見 §3）；其餘自訂標頭流量都沒量過。讀碼上 kernel 先記鏈路位元組再看幀是什麼，而非 IPv4 的流身份只進上限 1024 筆的側表、不進流表 |
| `queue_metadata` | **做得到** | 【跑過】佇列靠 NDTwin 把 s1:3↔s2:3 整形成 0.5 Mbit/s 來形成：ecn 解答臂 h2 看到 tos `0x3`；mri 的 raw 裡有 `qdepth = 63`（未斷言）。（Adam 2026-09-28 裁定）：twin 不讀 qdepth，但那是逐包 metadata，不算 (a)；`--priority-queues` 沒有，13 支也都沒用 |
| `checksum` | **做得到** | 【跑過】10 支用 `update_checksum`、flowcache 另用 `verify_checksum`，解答臂全綠。firewall 的 TCP iperf h1→h3 3 s 傳了 262 MBytes，大流量沒有被 L4 checksum 擋掉。歸 NDTwin 的那一半（關主機 offload）只有讀碼 |
| `ttl_or_hop` | **做得到** | 【跑過】TTL／hop 由 exercise 的程式做、收端量得到：basic ttl 63、source_routing ttl {59, 62}、mri hop count 2 且 swid [1, 2]。這一維在路線 2 下沒有歸 NDTwin 的部分 |
| `topology` | **做得到** | 【跑過】四類拓樸都由 convert 出的 package 起，kernel 圖、拓樸檔、主機 namespace 三方一致：pod 4h/4s、三角 3h/3s、5h/3s、單交換機 calc 2h/1s 與 multicast 4h/1s。ecn／mri 的整形由 NDTwin 做；外來 fabric 的斷線由 veth 心跳判（H1 6/6 次都在 20 s 內） |
| `control_plane_mode` | **做得到** | 【跑過】三種模式都在 NDTwin fabric 上跑過。①開機 runtime json：9 支由 NDTwin 套、0 failed。②external：proxy 不仲裁、不寫，控制器經 NDTwin 的 adapter 連上 fabric 的埠（p4runtime、flowcache）。③無：calc 0 entry 仍答 1+1=2。另外 roles 讓 NDTwin 寫外來程式的 `ipv4_lpm`，pingall 12/12 |
| `verification` | **部分** | (a) 【跑過】twin 的鏈路使用率格（G1）只在 10/13 支解答臂 PASS；source_routing／calc／load_balance 是 NOT RUN（它們的程式丟掉一般 iperf）。06 沒有逐支的陽性對照（只有 live-p1/05 在 basic 上做）。自訂標頭的流身份只進側表（讀碼）。存活偵測有：心跳 H1–H5 PASS |

## 逐支映射：右側兩欄

| exercise | 骨架臂（GAP-2b §3 ＝ T06） | 解答臂（GAP-2b §3 ＝ T06） | runs on NDTwin | twin sees it | GAP-2b §3 最後一欄原文 |
|---|---|---|---|---|---|
| basic | 紅如預期 `PASS (4/4)` rc 0（`074636Z`） | 綠 `PASS (6/6)` rc 0（`074826Z`） | **跑得起來** | **看得到** | **看得到**：G1 h1→h4，主路徑 3 條（2 條交換機間）積分 > 0，9 條非路徑 0.000 bit【跑過】`basic/sol:632-651` |
| qos | 紅如預期 `PASS (3/3)` rc 0（`075704Z`） | 綠 `PASS (4/4)` rc 0（`075747Z`） | **跑得起來** | **看得到** | **看得到**：G1 h1→h22 主路徑 2 條積分 > 0、9 條非路徑 0【跑過】`qos/sol:1221-1239` |
| ecn | 紅如預期 `PASS (3/3)` rc 0（`080513Z`） | 綠 `PASS (4/4)` rc 0（`080642Z`） | **跑得起來** | **看得到** | **看得到**：G1 h1→h22 走 0.5 Mbit/s 瓶頸，窗口 62 s，主路徑 2 條積分 > 0、9 條非路徑 0【跑過】`ecn/sol:993-1011` |
| mri | 紅如預期 `PASS (4/4)` rc 0（`080917Z`） | 綠 `PASS (5/5)` rc 0（`080951Z`） | **跑得起來** | **只看過 IPv4** | **只看過 IPv4**：G1 PASS 用的是一般 IPv4 iperf（ihl 5、不帶 MRI option）【跑過】`mri/sol:716-734`；帶 option 的包沒被量過。非路徑 s2-eth4 讀到 143,328 bit，在一個樣本的底限之下 |
| firewall | 紅如預期 `PASS (3/3)` rc 0（`080011Z`） | 綠 `PASS (4/4)` rc 0（`080128Z`） | **跑得起來** | **看得到** | **看得到**：G1 h1→h4 主路徑 3 條積分 > 0、9 條非路徑 0【跑過】`firewall/sol:572-591` |
| basic_tunnel | 紅如預期 `RED ARM (1/1)` rc 1（`075454Z`） | 綠 `PASS (4/4)` rc 0（`075455Z`） | **跑得起來** | **只看過 IPv4** | **只看過 IPv4**：G1 PASS 用的是一般 IPv4 iperf h1→h3【跑過】`basic_tunnel/sol:707-723`；`send.py --dst_id` 的 0x1212 tunnel 包沒被量過 |
| source_routing | 紅如預期 `PASS (2/2)` rc 0（`075000Z`） | 綠 `PASS (5/5)` rc 0（`075027Z`） | **跑得起來** | **無證據** | **無證據**：G1 NOT RUN，解答程式丟掉沒有 0x1234 堆疊的幀，一般 iperf 過不去【跑過】`source_routing/sol:668`；0x1234 幀本身沒被量過 |
| calc | 紅如預期 `PASS (2/2)` rc 0（`075053Z`） | 綠 `PASS (3/3)` rc 0（`075113Z`） | **跑得起來** | **無證據** | **無證據**：G1 NOT RUN（calc.p4 丟掉非 0x1234 的一切）【跑過】`calc/sol:464`；單交換機，只有 host 邊 |
| link_monitor | 紅如預期 `PASS (4/4)` rc 0（`075848Z`） | 綠 `PASS (4/4)` rc 0（`075920Z`） | **跑得起來** | **只看過 IPv4** | **只看過 IPv4**：G1 PASS 用的是一般 IPv4 iperf h1→h4【跑過】`link_monitor/sol:618-637`；0x812 probe 幀沒被量過 |
| load_balance | 紅如預期 `PASS (2/2)` rc 0（`075555Z`） | 綠 `PASS (2/2)` rc 0（`075630Z`） | **跑得起來** | **無證據** | **無證據**：G1 NOT RUN（s1 只轉 10.0.0.1/32，兩台真主機之間的 iperf 過不去）【跑過】`load_balance/sol:890` |
| multicast | 紅如預期 `PASS (2/2)` rc 0（`075133Z`） | 綠 `PASS (6/6)` rc 0（`075305Z`） | **跑得起來** | **看得到** | **看得到**（Adam 2026-09-28 裁定）：G1 h1→h3 主路徑 s1-eth3 積分 > 0、其餘 3 條 0【跑過】`multicast/sol:487-498`。單交換機只有 host 邊；G1 的單播 iperf 沒有走到 group 複製 |
| p4runtime | 紅如預期 `PASS (4/4)` rc 0（`081131Z`） | 綠 `PASS (5/5)` rc 0（`081205Z`） | **跑得起來** | **看得到** | **看得到**：G1 h1→h2，s1-eth2（交換機間）tx 4,361,273 B，比 s2-eth1（host）多 14,000 B＝3,500 datagram × 4 B（myTunnel 標頭）；同一窗口 s1 `ingressTunnelCounter 100` 到 3505 packets。所以 twin 在 s1-eth2 積分到的 29.3 Mbit 是 0x1212 幀【跑過】`p4runtime/sol:611-613`、`R/2026-09-27T081205Z_p4runtime_solution_ndtwin/driver-controller-p4runtime.log:122` |
| flowcache | 紅如預期 `RED ARM (1/1)` rc 1（`081255Z`） | 綠 `PASS (5/5)` rc 0（`081256Z`） | **跑得起來** | **只看過 IPv4** | **只看過 IPv4**（Adam 2026-09-28 裁定）：本輪 G1 PASS，但 iperf 在 s3 被丟、只有 s1→s3 那一段有流量（見 §4-1；09-19T151139Z 同一樣子）；twin 對那一段 > 0、其餘 0【跑過】`flowcache/sol:588-604`。同一臂 09-26 那輪 h1→h3 兩條主路徑都 > 0【跑過】`R/2026-09-26T175515Z_flowcache_solution_ndtwin.md:593-594,604`（trunk `3f8c2abf`；它與 `5dc7fc9a` 在 `src/`、`p4_proxy/proxy_agent/`、`p4_proxy/mininet/` 無 diff） |

## 逐格映射：需求側 13×16

（原文照抄自 GAP-1 §2；`\|` 已還原成 `|`。）

### `pipeline_load`

| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |
|---|---|---|---|
| basic | 單一程式 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| qos | 單一程式 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| ecn | 單一程式 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| mri | 單一程式 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| firewall | **關鍵：s1 與 s2-s4 不同程式** | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |
| basic_tunnel | 單一程式 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| source_routing | 單一程式 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| calc | 單一程式 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| link_monitor | 單一程式 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| load_balance | 單一程式 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| multicast | 單一程式 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| p4runtime | **關鍵：跑時才推 pipeline** | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |
| flowcache | 單一程式（控制器推） | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |

### `tables`

| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |
|---|---|---|---|
| basic | **關鍵** `lpm ipv4_lpm` | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |
| qos | `lpm ipv4_lpm`（default＝`NoAction`） | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| ecn | `lpm ipv4_lpm`（/32 ＋ /24） | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| mri | `lpm ipv4_lpm` ＋ `MyEgress.swtrace`(僅 default) | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| firewall | `lpm ipv4_lpm` ＋ `exact check_ports`(2 欄 std_meta) | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| basic_tunnel | **關鍵** `lpm ipv4_lpm` ＋ `exact myTunnel_exact` | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |
| source_routing | **一條 entry 都沒有** | **沒用到** | 【逐格審過的例外】GAP-1 §4a「`tables` 12/13 —— 只有 source_routing 一條 entry 都沒有」＋GAP-ANALYSIS §4「G5 不需要：**0 筆 entry**」⇒ 歸「沒用到」。本腳本另以 §4a 的 12/13 做斷言，歸錯會當場爆。 |
| calc | `exact calculate`（**const entries，控制面改不了**） | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| link_monitor | `lpm ipv4_lpm` ＋ `MyEgress.swid`(僅 default) | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| load_balance | `lpm ecmp_group` ＋ `exact ecmp_nhop` ＋ `exact send_frame`(egress_port) | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| multicast | **關鍵** `exact mac_lookup`(MAC) ＋ default→multicast | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |
| p4runtime | `lpm ipv4_lpm` ＋ `exact myTunnel_exact` | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| flowcache | **關鍵** `exact flow_cache`(3 欄) ＋ `support_timeout` | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |

### `pre_multicast`

| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |
|---|---|---|---|
| basic | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| qos | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| ecn | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| mri | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| firewall | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| basic_tunnel | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| source_routing | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| calc | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| link_monitor | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| load_balance | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| multicast | **關鍵** grp 1 = {1,2,3} | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |
| p4runtime | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| flowcache | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |

### `pre_clone`

| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |
|---|---|---|---|
| basic | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| qos | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| ecn | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| mri | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| firewall | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| basic_tunnel | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| source_routing | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| calc | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| link_monitor | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| load_balance | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| multicast | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| p4runtime | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| flowcache | **關鍵** session 57→CPU_PORT | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |

### `counters`

| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |
|---|---|---|---|
| basic | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| qos | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| ecn | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| mri | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| firewall | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| basic_tunnel | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| source_routing | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| calc | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| link_monitor | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| load_balance | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| multicast | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| p4runtime | **關鍵** 兩個 tunnel counter | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |
| flowcache | **關鍵** 兩個 | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |

### `meters`

| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |
|---|---|---|---|
| basic | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| qos | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| ecn | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| mri | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| firewall | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| basic_tunnel | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| source_routing | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| calc | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| link_monitor | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| load_balance | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| multicast | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| p4runtime | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| flowcache | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |

### `registers`

| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |
|---|---|---|---|
| basic | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| qos | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| ecn | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| mri | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| firewall | **用到但不讀**（bloom filter） | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| basic_tunnel | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| source_routing | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| calc | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| link_monitor | **用到但不讀**（byte_cnt／last_time） | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| load_balance | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| multicast | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| p4runtime | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| flowcache | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |

### `digest`

| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |
|---|---|---|---|
| basic | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| qos | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| ecn | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| mri | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| firewall | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| basic_tunnel | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| source_routing | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| calc | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| link_monitor | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| load_balance | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| multicast | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| p4runtime | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |
| flowcache | （§2 無此欄） | **沒用到** | §2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。 |

### `packet_io`

| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |
|---|---|---|---|
| basic | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| qos | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| ecn | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| mri | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| firewall | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| basic_tunnel | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| source_routing | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| calc | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| link_monitor | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| load_balance | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| multicast | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| p4runtime | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| flowcache | **關鍵** | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |

### `custom_headers`

| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |
|---|---|---|---|
| basic | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| qos | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| ecn | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| mri | **關鍵** IPv4 option ＋ stack | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |
| firewall | tcp hdr | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| basic_tunnel | **關鍵** 0x1212 tunnel hdr | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |
| source_routing | **關鍵** 0x1234 ＋ stack `pop_front` | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |
| calc | **關鍵** 0x1234 ＋ `lookahead` | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |
| link_monitor | **關鍵** 0x812 ＋ 兩個 stack | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |
| load_balance | tcp hdr | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| multicast | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| p4runtime | **關鍵** 0x1212 tunnel hdr | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |
| flowcache | **關鍵** packet_in/out ＋ enum | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |

### `queue_metadata`

| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |
|---|---|---|---|
| basic | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| qos | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| ecn | **關鍵** `enq_qdepth` | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |
| mri | **關鍵** `deq_qdepth` | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |
| firewall | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| basic_tunnel | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| source_routing | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| calc | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| link_monitor | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| load_balance | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| multicast | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| p4runtime | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| flowcache | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |

### `checksum`

| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |
|---|---|---|---|
| basic | update | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| qos | update | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| ecn | update | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| mri | update | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| firewall | update | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| basic_tunnel | update | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| source_routing | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| calc | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| link_monitor | update | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| load_balance | update | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| multicast | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| p4runtime | update | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| flowcache | verify ＋ update | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |

### `ttl_or_hop`

| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |
|---|---|---|---|
| basic | 用到 `ttl-1` | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| qos | 用到 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| ecn | 用到 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| mri | 用到 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| firewall | 用到 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| basic_tunnel | 用到 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| source_routing | **關鍵** `ttl` 判路徑 | **關鍵** | 格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。 |
| calc | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| link_monitor | probe `hop_cnt` | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| load_balance | 用到 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| multicast | — | **沒用到** | 格值是破折號 —— 直接歸「沒用到」。 |
| p4runtime | 用到 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| flowcache | 飽和減 `\|-\|` | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |

### `topology`

| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |
|---|---|---|---|
| basic | 4h/4s pod-topo（另有 3h/3s triangle）；無 bw；gw＋靜態 ARP | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| qos | 5h/3s；**無任何 bw 參數**（與 ecn/mri 同形但不同設定） | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| ecn | 5h/3s；**s1-p3↔s2-p3 bw 0.5 Mbps** | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| mri | 5h/3s；**s1-p3↔s2-p3 bw 0.5 Mbps** | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| firewall | 4h/4s pod-topo；無 bw；gw＋ARP | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| basic_tunnel | 3h/3s 三角；無 bw；gw＋ARP | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| source_routing | 3h/3s 三角；無 bw；gw＋ARP | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| calc | **2h/1s**；無 bw；**無 gw、無 ARP** | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| link_monitor | 4h/4s pod-topo；無 bw；gw＋ARP | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| load_balance | 3h/3s 三角；無 bw；gw＋ARP | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| multicast | **4h/1s**；無 bw；**只有 `ip route add`，無 gw、無靜態 ARP** | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| p4runtime | 3h/3s 三角；無 bw；gw＋ARP | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| flowcache | 3h/3s 三角；無 bw；gw＋ARP；**三台都要 `cpu_port 510`** | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |

### `control_plane_mode`

| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |
|---|---|---|---|
| basic | 開機 runtime json | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| qos | 開機 runtime json | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| ecn | 開機 runtime json | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| mri | 開機 runtime json | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| firewall | 開機 runtime json | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| basic_tunnel | 開機 runtime json | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| source_routing | 開機 runtime json（**空**） | **用到** | 【逐格審過的例外】模式仍是①「開機灌 runtime json」，只是 entry 陣列是空的（GAP-1 §3.13）⇒ 模式有用到，歸「用到」；「空」講的是筆數不是模式。 |
| calc | **無**（entry 在 P4 裡） | **沒用到** | 【逐格審過的例外】GAP-1 §1 把 control_plane_mode 定義成三選一，第③種就是「兩者皆無」；§3.3「`control_plane_mode`＝**無**」⇒ 歸「沒用到」。 |
| link_monitor | 開機 runtime json | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| load_balance | 開機 runtime json | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| multicast | 開機 runtime json | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| p4runtime | **跑時控制器** | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| flowcache | **跑時控制器** | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |

### `verification`

| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |
|---|---|---|---|
| basic | `pingall`；另有 PTF（`ptf/basic_fwd.py`，veth，**不經 Mininet**） | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| qos | `send.py --p=UDP/--des/--m/--dur`；h2 看 `tos` 由 `0x1` 變 `0xb9`(UDP)／`0xb1`(TCP) | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| ecn | h1 `send.py` 1 pps ＋ h11 `iperf -u` 灌爆 → h2 看 `tos` 由 `0x1` 變 `0x3` | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| mri | h2 `receive.py` 要看到 swtrace 序列（swid ＋ qdepth）；iperf 製造佇列 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| firewall | `iperf h1 h2` 通、`iperf h1 h3` 通、**`iperf h3 h1` 要被擋** | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| basic_tunnel | `send.py --dst_id` → `receive.py` 讀 `show2()` 有無 tunnel 層；另有 PTF | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| source_routing | h2 收到、**`ttl == 59`**（`2 3 2 2 1`）vs `62`（`2 1`）；無 SourceRoute 層 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| calc | `h1 python3 calc.py` REPL：輸入 `1+1` 要回 `2`（`srp1` 請求／回應） | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| link_monitor | h1 跑 `send.py`(probe 迴圈)＋`receive.py`；印出的 Mbps 要與 `iperf h1 h4` 對得上 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| load_balance | h2/h3 各跑 `receive.py`；h1 反覆 `send.py 10.0.0.1`，**兩邊都要收到**（雜湊分流） | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| multicast | `pingall`：h1/h2/h3 互通、**h4 不通** | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| p4runtime | `h1 ping h2` 起初無回應、跑 `mycontroller.py` 後有；counter 每 2 s 遞增 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |
| flowcache | `h1 ping h2` 在控制器起來前無回應、起來後有；counter 要增加 | **用到** | 格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。 |

## 色票

| 色階 | 色碼 | 出處 |
|---|---|---|
| 關鍵 | `#065A82` | 827 模板 §E2 `ACCENT` |
| 用到 | `#8FB5C7` | `ACCENT` 混 55% 白 |
| 沒用到 | `#EEF3F6` | 827 模板 §E2 `ACCENT_BG` |
| 做得到／跑得起來／看得到 | `#2F7D4F` | 與 09-16 舊圖同一組綠 |
| 部分／只看過 IPv4 | `#E3A21A` | 同上琥珀 |
| 做不到／跑不起來 | `#C9CDD0` | 同上灰 |
| 無證據 | 白底、`#9AA0A5` 斜線 | 刻意與「做不到」的實心灰分開：沒量過 ≠ 量過不行 |

字體：無襯線（Liberation Sans → DejaVu Sans → Arial 依序 fallback）。圖上文字只有標題、兩軸的刻度標籤、三組圖例 —— **沒有任何句子**。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/p4-tutorials"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_tutorial_figs_0927.py
```

產出：

- `fig_t1b_requirements_matrix_0927.pdf`
- `fig_t1b_requirements_matrix_0927.png`（300 dpi，4380×2160 px）
- `fig_t1b_requirements_matrix_0927.svg`
- `_hires/fig_t1b_requirements_matrix_0927.png`（500 dpi）
- `fig_t1b_requirements_matrix_0927.md`（本檔，同一支腳本產出，因此**不會與圖脫節**）

09-16 的 `fig_t1_requirements_matrix.*` 與 `make_tutorial_figs.py` 本腳本不讀也不寫。

最後產出：2026-09-30T04:28Z（UTC）；matplotlib 3.11.1；Python 3.13.13。
