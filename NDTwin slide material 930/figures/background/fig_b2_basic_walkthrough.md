# `fig_b2_basic_walkthrough` —— basic：一個封包怎麼穿過這支程式（B2）

[Co-developed with claude code -- Adam]

（本檔所有時間為 UTC。2026-09-29 新增；背景段 B 不受 delta only 限制，模板 §0 規則 1。）

## 一句話

p4lang/tutorials 的 `basic`：學生要寫的是 parser、`ipv4_forward` 的內容、`apply` 與 deparser（藍框＋TODO）；
封包依序經過 parser（ethernet → ipv4）→ `MyIngress.ipv4_lpm`（以目的 IP 做 lpm）→ `ipv4_forward(dstAddr, port)`（設出埠、換兩個 MAC、TTL − 1）→ checksum → deparser。
下排是它跑的 pod 拓樸、h1 送往 10.0.3.3 的封包照 entry 走的路，以及 s1 開機裝進去的 5 條 entry。

## 資料來源（全部 READ：tutorials checkout `/home/adam/tutorials` 的 commit `c80d83e`，以 `git show c80d83e:<path>` 讀；沒有執行任何東西）

T＝`exercises/basic`。行號是 `c80d83e` 上的行號（產生器執行時印出的錨點見最後產出行的 log）。

| 圖上的東西 | 來源 | 產生器怎麼查 |
|---|---|---|
| etherType 0x800 | `T/solution/basic.p4:7` `const bit<16> TYPE_IPV4 = 0x800` | 讀常數值、印在 parser 裡 |
| parser：ethernet → ipv4 | `T/solution/basic.p4:60-71`（`parse_ethernet` extract ethernet、select etherType：`TYPE_IPV4: parse_ipv4`；`parse_ipv4` extract ipv4） | 三件事各一個停止條件 |
| `ipv4_lpm`：key `hdr.ipv4.dstAddr`、lpm、miss＝drop | `T/solution/basic.p4:102-113` | key、match kind、actions 含 `ipv4_forward` 與 `drop`、`default_action = drop()` 各自停 |
| `ipv4_forward(dstAddr, port)` 與四行標籤 | `T/solution/basic.p4:95-100`：`standard_metadata.egress_spec = port`、`hdr.ethernet.srcAddr = hdr.ethernet.dstAddr`、`hdr.ethernet.dstAddr = dstAddr`、`hdr.ipv4.ttl = hdr.ipv4.ttl - 1` | 參數名讀自原始碼；四條敘述逐條比對（去空白），少一條就停；圖上印的是這四條的白話標籤（egress port ← port／src MAC ← old dst MAC／dst MAC ← dstAddr／TTL − 1） |
| apply：if ipv4 is valid → ipv4_lpm | `T/solution/basic.p4:115-119` | 停止條件 |
| checksum | `T/solution/basic.p4:136-154`（`update_checksum` 寫 `hdr.ipv4.hdrChecksum`） | 停止條件 |
| deparser：emit ethernet, ipv4 | `T/solution/basic.p4:160-165` | emit 的順序必須恰為這兩個 |
| TODO（學生寫的）四塊 | 骨架 `T/basic.p4`：parser `:67-73`、`ipv4_forward` `:120-128`（去掉註解後沒有任何敘述）、apply `:151-156`、deparser `:204-209` | 每塊都要含 TODO；`ipv4_forward` 不得已有敘述；`ipv4_lpm` 在骨架裡必須已給好（key 同上） |
| 「skeleton: drops every packet」 | `T/README.md:47`（「`basic.p4`, which initially drops all packets」） | 字串不在就停 |
| 拓樸 `pod-topo/topology.json` | `T/Makefile:5` `TOPO = pod-topo/topology.json`；`T/pod-topo/topology.json`（4 主機、4 交換機、8 條連結） | 節點集合必須等於圖的版面；每個連結端點必須是主機或宣告過的 `sN-pK`；每台主機都要接到交換機 |
| h1 → 10.0.3.3 的藍線與「port N」 | `T/pod-topo/s1-runtime.json`、`s3-…`、`s2-…` 的 `MyIngress.ipv4_lpm` 條目；主機 IP 讀自拓樸 | 沿 lpm（最長前綴）與拓樸的埠一路走：s1 port 3 → s3 port 2 → s2 port 1 → h3；查不到、接到不存在的埠、繞圈、到錯的主機都各自停 |
| s1 的 5 條 entry | `T/pod-topo/s1-runtime.json`（1 條 default `MyIngress.drop`＋4 條 /32 `MyIngress.ipv4_forward`） | 所有 runtime 條目的表名、action、match 欄位、參數名都要是 solution 宣告過的；s1 必須恰有一條 default 且是 drop |

## 可信度

全部 **READ**（讀原始碼與設定檔）。圖上沒有任何跑出來的數字；右上角標「READ · p4lang/tutorials c80d83e」。
這支 exercise 在 NDTwin fabric 上跑過（T06 basic 兩臂照預期，code `5dc7fc9a +95`），但那是 T 段的證據，不在這張圖上。
**checkout 不乾淨**：`/home/adam/tutorials` 的 working tree 在 `exercises/basic/basic.p4` 有三行註解的本機修改（2026-07-14 的檔案時間，只動註解裡的 `*action data*` 與一個縮排）；產生器用 `git show c80d83e:` 讀，所以不受影響。

## 已知但書

- 手寫的只有版面、四條敘述的白話標籤、節點座標（節點集合有檢查）與 `h1 → h3` 這個挑選。
- `basic` 另有 `triangle-topo`；這張圖畫的是 `Makefile` 預設的 pod-topo（GAP-1 §3.1）。
- 它的 PTF 測試（`runptf.sh`）繞過 Mininet，不在圖上。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/background"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_background_figs.py
```

## 紅檢

`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_background_figs-redcheck-20260929T0740Z.log`：
harness 為每個案例建一個臨時 git repo（只放產生器會讀的檔，內容取自 `c80d83e`），改一處、commit，讓產生器的副本指向它；
81 個竄改 81/81 以產生器自己的具名理由停下，對照組（不改）畫得出兩張圖；2 個停止點任何輸入都到不了（理由在 log）。harness：同目錄 `make_background_figs-redcheck.py`。

最後產出：2026-09-29T07:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_background_figs.py` sha256 `8497ac0b82412658…`（與紅檢 log 檔頭同一版）；PNG sha256 前 16 碼：300 dpi `82beae2b5c451dbc`、500 dpi `5ae5bb8e657c5273`。
