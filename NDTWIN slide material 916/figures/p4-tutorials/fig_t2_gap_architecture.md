# fig_t2_gap_architecture — 五個 gap 各自坐在哪個元件上

投影片 **T2 `WHERE THE FIVE GAPS LIVE`** 的整頁圖。一句話：**十三支 exercise 帶進來的四樣東西
（`.p4`／`topology.json`／`sX-runtime.json`／`mycontroller.py`）各自撞到 proxy 或 kernel 的哪一個
元件，六個 `G` 徽章就釘在那些元件上，徽章邊框說它排在第幾階段。**

產出：`fig_t2_gap_architecture.{pdf,png,svg}` ＋ `_hires/fig_t2_gap_architecture.png`
（PNG 3732×2100 @300 dpi、hires 6220×3500 @500 dpi；畫布 12.44×7.0 in ＝ 16:9）。
畫法規約：827 §E2（色票＋Arial）、§E4a（apps 最上、雲最下、框線黑 1pt 白底、
**sFlow 從 proxy 的 emitter 出、不從 bmv2 雲出**）。

---

## 0. 可信度

🟠 **【讀碼推導】＋【估】。一行都還沒改，也沒有任何一支 exercise 在 NDTwin fabric 上跑過。**

- 六個徽章的**行數全部是量級粗估**（`GAP-ANALYSIS.md` §1 表格「工作量【估】」欄，
  §3 逐 gap 再拆一次候選 A/B/A' 的成本）。圖上寫 `~150`／`~180`／`~15`／`~85`／`~40`／`~30+250`，
  `~` 與 §6 的 `(est.)` 是同一個口徑，**不可讀成量出來的**。
- 元件與「今天寫死在哪」是**讀碼**的（行號見 §2），讀的樹＝**trunk `1a284f75`**。
- 🔴 **正本 `GAP-ANALYSIS.md`／`GAP-1`／`GAP-2`／`runs/` 在 2026-09-08 仍是共用 worktree 裡的
  未提交檔（`git status` ＝ untracked）**——引用時要講「這是未提交的觀測」。
- 圖上唯一 🟢 的元素是**沒有**的：這張圖不放任何實測數字。

## 1. 三層各是什麼

| 層 | 框 | 依據 |
|---|---|---|
| 上 `EXERCISE` | `topology.json`／`its .p4`／`sX-runtime.json`／`mycontroller.py` | `GAP-ANALYSIS` §1「方法①：逐支讀 `.p4`／`topology.json`／`sX-runtime.json`／`mycontroller.py`」 |
| 中左 `KERNEL` | `northbound API`／`topology model`／`sFlow parser + FlowKey` | `GAP-2` §3 觀察 5（分歧點在 kernel）；`FlowLinkUsageCollector.cpp:1266-1279`、`SFlowType.hpp:31-47`、`ryu_flow_stats.py:40-48` |
| 中右 `PROXY` | `packet-in decoder → sFlow emitter`／`pipeline loader`／`P4Runtime client`（內含 `table writer`＋`election_id`） | `GAP-2` §3 觀察 1、2、6；`sflow_emitter.py:446-482`、`main.py:185-186`、`p4_client.py:459-481,846`、`p4_client.py:234-235` |
| 下（雲） | `Mininet fabric · bmv2 × N`，副標 `one p4info today` | `GAP-ANALYSIS` §1-G4「十台同一份、跑時換不了」；§2b「firewall 的 `pod-topo/topology.json:39` 讓同一網路兩份 p4info 同時在線」＝今天做不到 |

**框的排序是為了讓四條箭頭都走直線**：kernel 把 `sFlow parser` 排在最右、proxy 把
`packet-in decoder → sFlow emitter` 排在最左，兩者隔著中線相鄰 ⇒ sFlow 那一箭只跨一個間隙。

## 2. 六個徽章：釘在哪、數字哪來、第幾階段

| 徽章 | 釘在 | 今天寫死在哪（`GAP-ANALYSIS` §1 表） | 行數【估】 | 階段（徽章邊框） |
|---|---|---|---|---|
| `G2  ~85` | `topology model` | `p4_testbed_topo.py:120-134`（選檔只看主機數）＋`main.py:113-120`（四等分公式）＋`main.py:154`（寫死十台）＋`p4_testbed_topo.py:662`（無 `link=TCLink`） | ~85 | **一**（細實線） |
| `G4  ~150` | `pipeline loader` | `main.py:185-186` | ~150 | **二**（粗實線） |
| `G5  ~180` | `P4Runtime client` 內的 `table writer` | `p4_client.py:846`（＋`:729,761-767,856-866,697-704`；`default_action` 只有讀 `:619`） | ~180 | **二**（粗實線） |
| `G3  ~15` | `P4Runtime client` 內的 `election_id` | `p4_client.py:234-235` | ~15 | **一**（細實線） |
| `G1  ~40` | `packet-in decoder → sFlow emitter` | `sflow_emitter.py:425-429` | ~40 | **一**（細實線） |
| `G6  ~30+250` | `sFlow parser + FlowKey` | `FlowLinkUsageCollector.cpp:1266` | ~30（候選 A'）＋~250（候選 B） | **三**（虛線） |

階段歸屬照 `GAP-ANALYSIS` §6 那張表：
**一**＝`G1`＋`G3`＋`G2-A/B`（~140 行）；**二**＝`G4`＋`G5`（~330 行）；
**三**＝`G2-C`＋`G6-A'`＋`G7`＋`G8`＋`G9a/b`（~205 行）。

⚠️ **`G2` 是唯一橫跨兩階段的**：A/B（三處改讀拓樸檔）在第一階段、C（`link=TCLink` 整形，~15 行）在
第三階段（§3-G2「C 走獨立進入點」）。徽章上的 `~85` 是 §1 表的整條 G2，邊框我畫成**一**，
因為 §6 第一階段的 ~140 行就是 40+15+85。**上台講到 ecn／mri 的整形時要補這一句**，圖上不寫。

⚠️ **`G6` 的 `~30+250` 是兩個候選不是兩個階段**：~30 ＝ A'（`ihl` 修正＋不可見樣本計數，不動口徑），
~250 ＝ B（擴 `FlowKey` 與 C++ 解析器，會動已發表的量測口徑）。§6 第三階段只含 A' 的 ~30。

**不在圖上的 G**：`G7`（counters，~50）／`G8`（PRE multicast，~80）／`G9a/b`（clone session＋cpu-port，~30）
——正本 §3 有，指派單只點名六個徽章，圖上不放。

## 3. 四條箭頭（＝模板 T2 圖規格那四條）

1. `its .p4` → `pipeline loader`
2. `sX-runtime.json`／`mycontroller.py` → `P4Runtime client`（＝ runtime json / controller → table writer）
3. `topology.json` → `topology model` → 雲
4. 雲（`bmv2 clone`）→ `packet-in decoder` →（`sFlow`）→ `sFlow parser + FlowKey`

第 4 條的鏈路依據：`clone_preserving_field_list(I2E, SAMPLE_SESSION=250, FL_SAMPLE)`
（`ndtwin_switch.p4:411`、常數在 `:48,52`，`SAMPLE_RATE=256`）→ egress 補 `packet_in` 標頭
（`:405-448`）→ PI 轉 typed metadata → `sample_from_packet_in` → 合成 sFlow → UDP 6343
（`sflow_emitter.py:446-482`）。**sFlow 從 proxy 出**，這是 §E4a 明寫的規矩，也是機制的實情。

## 4. 顏色與形狀口徑

- 有徽章的框：`ACCENT_BG` 淡底＋黑框；沒徽章的（`northbound API`、上層四框、雲）：純白＋黑框。
  827 §E1「全篇只有一個強調色」⇒ 階段不另外上色，只走**邊框粗細／虛實**（圖左下三格圖例）。
- `WARNC` 一格都沒用：這張圖沒有「量到的壞消息」，全部是讀碼推導。

## 5. Regenerate

```
cd "/home/adam/Desktop/NDTwin slide material/NDTWIN slide material 916/figures/p4-tutorials"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_gap_diagrams.py
```
（一支腳本產四張；matplotlib 3.11.1，腳本開頭有版本 assert。Arial 在這台機器上不存在，
`font.sans-serif` 退到 metric-compatible 的 Liberation Sans；SVG 用 `svg.fonttype="none"`
保留可編輯文字，換到有 Arial 的機器打開就是 Arial。`_hires/` 是同一支腳本 `dpi=500` 存的，
**不是** `pdftoppm`——與 `figures/overnight-0904/` 的作法不同，改了記得兩邊口徑要一致。）

修改函式：`fig_t2()`。所有數字是腳本裡的字面值，不從檔案算 ⇒ 輸出可重現。

[Co-developed with claude code -- Adam]
