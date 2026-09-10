# `fig_t1_requirements_matrix` —— 13 支 tutorial exercise 的需求 vs. NDTwin 今天的供給

[Co-developed with claude code -- Adam]

## 一句話

**13 支 p4lang/tutorials exercise 各自需要 16 個能力維度中的哪幾個（上半），對照 NDTwin 今天做得到哪幾個（底下隔開的那一列）。**

## 資料來源（圖上每一格都出自這裡，腳本裡沒有手抄的數字）

| 用途 | 檔 | 章節 |
|---|---|---|
| 需求矩陣 13×16 | `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/GAP-1-exercise-requirements.md` | §2a 資料面／§2b 控制面／§2c 拓樸與驗證 |
| `meters`／`digest` 兩欄（§2 沒有這兩欄） | `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/GAP-1-exercise-requirements.md` | §4b「只有少數支要的」的 `meters`／`digest` ＝ **0 支** |
| 對帳斷言（幾支要） | `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/GAP-1-exercise-requirements.md` | §4a、§4b |
| NDTwin today 那一列 1×16 | `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/GAP-2-ndtwin-p4-capabilities.md` | §1 能力矩陣＋文末「計數：做得到 1、部分 9、做不到 6」 |
| 列序（上→下） | `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/GAP-ANALYSIS.md` | §6 三階段（定序）、§4 逐支可行性表（同序，做交叉驗證） |
| 色票 | `/home/adam/Desktop/NDTwin slide material/NDTwin slide material 827/NDTwin-slide-template-827.md` | §E2 色票與字體 |

## 可信度

🟠 **【讀碼推導】** —— 兩份來源都明講本輪**沒有執行任何東西**：GAP-1 §0「本輪一個封包都沒送、一支 exercise 都沒跑，我只讀原始碼與設定檔」；GAP-2 §0「全部是【讀碼推導】：本輪沒起 fabric、沒跑 bmv2／Mininet／`ndt`、沒編譯」。
⇒ **這張圖是兩份讀碼盤點的視覺化，不是量測結果。**唯一夾帶【實測】標記的格子是 GAP-1 §2b 的 source_routing「灌幾筆」（三個檔都是空陣列，M7 §0），而那一欄不是 16 維之一、沒有進圖。

## 圖怎麼讀

- **上半 13 列**＝需求側，三色階（深藍`關鍵`／中藍`用到`／極淡`沒用到`）。
- **底下隔線之後那一列**＝NDTwin today，另一組三色階（綠`做得到`／琥珀`部分`／灰`做不到`）。
- **列序**由階段決定，階段之間留一道空白（沒有文字）：階段一＝['basic']（§6 解鎖欄「1 支真跑通」＋驗證欄點名）；階段二＝['qos', 'ecn', 'mri', 'firewall', 'basic_tunnel', 'source_routing', 'calc', 'link_monitor', 'load_balance']（§6 解鎖欄 +9 支的名單，逐字照抄順序）；階段三＝['multicast', 'p4runtime', 'flowcache']（餘數；§6 第三階段解鎖欄點名了 ['multicast', 'flowcache']，p4runtime 是餘數推得、§4 表也把它排在該位置）。
- **欄序**＝ GAP-1 §1 定義表的 16 個鍵順序（本腳本斷言解析到的集合與它相同）。

## 我做的歸類判斷（全部）

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

  其中 `idle_timeout` 是 GAP-1 §1 自己註明「維度清單外、但必須另立一條」的第 17 維（只有 flowcache 用），本圖照題目給的 16 鍵清單，**不畫它**。GAP-ANALYSIS §2 也把它列在判定表最後一列並標「（額外）」。

**兩個 §2 沒有欄位、由 §4b 補的維度**：`meters` 與 `digest`。§4b 明列兩者合計 **0 支**（「這批 exercise 完全不需要。做了不會有任何一支用到。」）⇒ 13 支全填 `沒用到`；腳本會斷言 §4b 的數字真的是 0，不是 0 就停。

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
- 需求矩陣形狀 = 13×16；NDTwin 列 = 1×16；兩者的 16 個鍵集合相同。
- 列序：§4 的 13 列順序 == §6 的（階段一 + 階段二名單 + 餘數），逐位比對。

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

## 逐格映射：NDTwin today 1×16

| 維度 | GAP-2 §1「今天」原文 | 色階 |
|---|---|---|
| `pipeline_load` | 部分 | **部分** |
| `tables` | 部分 | **部分** |
| `pre_multicast` | 做不到 | **做不到** |
| `pre_clone` | 部分 | **部分** |
| `counters` | 部分 | **部分** |
| `meters` | 做不到 | **做不到** |
| `registers` | 做不到 | **做不到** |
| `digest` | 做不到 | **做不到** |
| `packet_io` | 部分 | **部分** |
| `custom_headers` | 做不到 | **做不到** |
| `queue_metadata` | 做不到 | **做不到** |
| `checksum` | 部分 | **部分** |
| `ttl_or_hop` | 做得到 | **做得到** |
| `topology` | 部分 | **部分** |
| `control_plane_mode` | 部分 | **部分** |
| `verification` | 部分 | **部分** |

## 色票

| 色階 | 色碼 | 出處 |
|---|---|---|
| 關鍵 | `#065A82` | 827 模板 §E2 `ACCENT` |
| 用到 | `#8FB5C7` | `ACCENT` 混 55% 白 |
| 沒用到 | `#EEF3F6` | 827 模板 §E2 `ACCENT_BG` |
| 做得到 | `#2F7D4F` | 綠／琥珀／灰一組（題目給的選項），與藍色系分得開 |
| 部分 | `#E3A21A` | 同上 |
| 做不到 | `#C9CDD0` | 同上 |

字體：無襯線（Liberation Sans → DejaVu Sans → Arial 依序 fallback）。圖上文字只有標題、兩軸的刻度標籤、兩組圖例 —— **沒有任何句子**。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTWIN slide material 916/figures/p4-tutorials"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_tutorial_figs.py
```

產出：

- `fig_t1_requirements_matrix.pdf`
- `fig_t1_requirements_matrix.png`（300 dpi，2760×1980 px）
- `fig_t1_requirements_matrix.svg`
- `_hires/fig_t1_requirements_matrix.png`（500 dpi）
- `fig_t1_requirements_matrix.md`（本檔，同一支腳本產出，因此**不會與圖脫節**）

最後產出：2026-09-08 17:42；matplotlib 3.11.1；Python 3.13.13。
