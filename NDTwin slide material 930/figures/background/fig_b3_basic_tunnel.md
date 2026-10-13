# `fig_b3_basic_tunnel` —— basic_tunnel：自己的標頭、自己的表（B3）

[Co-developed with claude code -- Adam]

（本檔所有時間為 UTC。2026-09-29 新增；背景段 B 不受 delta only 限制，模板 §0 規則 1。）

## 一句話

p4lang/tutorials 的 `basic_tunnel`：在 ethernet 與 ipv4 之間插一個自訂標頭 `myTunnel_t`（proto_id、dst_id 各 16 bit，etherType 0x1212）；
parser 多一條分支，MyIngress 多一張以 `dst_id` 做 exact match 的表 `myTunnel_exact`，deparser 多送一個標頭。
下排：同一個目的 IP 10.0.3.3，不帶 tunnel 走到 h3，帶 `dst_id 2` 走到 h2——tunnel 標頭蓋過 IP 目的地。

## 資料來源（全部 READ：tutorials `/home/adam/tutorials` commit `c80d83e`，`git show c80d83e:<path>`；沒有執行任何東西）

T＝`exercises/basic_tunnel`。

| 圖上的東西 | 來源 | 產生器怎麼查 |
|---|---|---|
| etherType 0x1212、0x800 | `T/solution/basic_tunnel.p4:7`（`TYPE_MYTUNNEL = 0x1212`）、`:8`（`TYPE_IPV4 = 0x800`） | 讀常數值；主機端 `T/myTunnel_header.py` 的 `TYPE_MYTUNNEL` 必須同值、並 `bind_layers(Ether, MyTunnel, type=TYPE_MYTUNNEL)` |
| 標頭 `myTunnel_t`：proto_id 16 bit、dst_id 16 bit | `T/solution/basic_tunnel.p4:24-27` | 欄位名與位寬讀自原始碼，順序必須是 proto_id、dst_id |
| 主機怎麼送 tunnel 封包 | `T/send.py:40`：`Ether(...) / MyTunnel(dst_id=dst_id) / IP(dst=addr) / TCP(...)` | MyTunnel 必須夾在 Ether 與 IP 之間 |
| parser 分支 | `T/solution/basic_tunnel.p4:67-87`：etherType 0x1212 → `parse_myTunnel`、0x800 → `parse_ipv4`；`parse_myTunnel` extract 後 proto_id 0x800 → `parse_ipv4` | 三個 state、兩個 select 各自停 |
| `myTunnel_exact`（key `hdr.myTunnel.dst_id`、exact）→ `myTunnel_forward(port)` | `T/solution/basic_tunnel.p4:131-145`（動作只有 `standard_metadata.egress_spec = port`；default drop） | key、match kind、動作、default 各自停 |
| `ipv4_lpm` → `ipv4_forward(dstAddr, port)`「as in basic」 | `T/solution/basic_tunnel.p4:111-129` | key、參數、四條敘述都要和 basic 相同，否則「as in basic」這句就停 |
| apply：tunnel 有效 → myTunnel_exact；否則 IPv4 有效 → ipv4_lpm | `T/solution/basic_tunnel.p4:147-157` | 停止條件 |
| deparser：ethernet、myTunnel、ipv4 | `T/solution/basic_tunnel.p4:198-204` | emit 順序必須恰為這三個 |
| TODO（學生寫的）五塊 | 骨架 `T/basic_tunnel.p4`：parser `:61`、`myTunnel_forward` `:127`、`myTunnel_exact` `:130`、apply `:135`、deparser `:183` | 每塊都要有 TODO；骨架不得已宣告 `myTunnel_exact`／`myTunnel_forward`；標頭與常數必須已給好（`:8`、`:26`） |
| 拓樸（三角） | `T/topology.json`（`T/Makefile` 沒有 TOPO，用 `utils/Makefile:13-14` 的預設 `topology.json`） | 節點集合等於版面；連結端點、主機接線同 B2 的檢查 |
| 灰虛線：IPv4 到 10.0.3.3 | `T/s1-runtime.json`、`T/s3-runtime.json` 的 `ipv4_lpm` 條目：s1 port 3 → s3 port 1 → h3 | 沿 lpm 與拓樸的埠走；必須到 h3 |
| 藍線：dst_id 2 | `T/s1-runtime.json`、`T/s2-runtime.json` 的 `myTunnel_exact` 條目：s1 port 2 → s2 port 1 → h2 | 沿 exact 條目走；若和 IPv4 那條到同一台主機就停（這張圖的重點就沒了） |
| s1 的三條 exact 條目、「+ 3 ipv4_lpm entries」 | `T/s1-runtime.json`（3 條 ipv4_lpm＋3 條 myTunnel_exact；s2、s3 也各 3＋3） | 條目的表名、action、match 欄位、參數名都要是 solution 宣告過的；至少有一條 `myTunnel_exact` 條目 |

## 可信度

全部 **READ**。圖上沒有跑出來的數字；右上角標「READ · p4lang/tutorials c80d83e」。
🟢 另有跑過的證據（不在圖上、只在講稿）：T06 的 basic_tunnel 解答臂在 NDTwin fabric 上 PASS (4/4)，`--dst_id 2`／`3` 各落在對的主機（`E/runs/2026-09-27T075455Z_basic_tunnel_solution_ndtwin.md:833-835`，code `5dc7fc9a +95`）；
骨架臂被 pre-flight 拒絕，第一個理由是 `MyIngress.myTunnel_exact` 不在骨架的 p4info（T5）。twin 只看過這個 fabric 上的一般 IPv4（T7：IPv4 only）——❌ 不說「NDTwin 觀測得到 0x1212」。
`/home/adam/tutorials` 的 working tree 只在 `exercises/basic/basic.p4` 有註解改動，`basic_tunnel` 沒有；產生器一律用 `git show c80d83e:`。

## 已知但書

- 手寫的只有版面、`egress port ← port` 這個白話標籤（對應的敘述有檢查）、節點座標（集合有檢查），以及 `h1`、`h3`、`dst_id 2` 這組挑選（取自 README 第 6 步 `T/README.md:134-140`）。
- README 第 7 項要學生自己在 `sN-runtime.json` 加 tunnel 條目，但 `c80d83e` 的 runtime 檔已經帶了（所以骨架 `make run` 會因為找不到 `myTunnel_exact` 而失敗，`T/README.md:41-43`）。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/background"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_background_figs.py
```

## 紅檢

同 `fig_b2_basic_walkthrough.md`：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/make_background_figs-redcheck-20260929T0740Z.log`（81/81，對照組綠）。basic_tunnel 相關的停止點 33 個（solution 16、骨架 8、主機端 3、拓樸與條目 6），逐條在 log。

最後產出：2026-09-29T07:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_background_figs.py` sha256 `8497ac0b82412658…`；PNG sha256 前 16 碼：300 dpi `d51337ac1f045b78`、500 dpi `62f5b04a538cf0af`。
