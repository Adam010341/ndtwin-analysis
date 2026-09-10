# fig_t4_phases — 三階段解鎖幾支，以及已經跑過的那四次

投影片 **T4 `THREE PHASES TO A REGRESSION GATE`**。一句話：**左邊的階梯是「再寫幾行 ⇒ 幾支
exercise 跑得動」的三階段【估】，閘門在第二階之後；右邊的 2×2 是 09-08 已經實跑的四次，
skeleton 那一欄就是「紅也看過了」。**

產出：`fig_t4_phases.{pdf,png,svg}` ＋ `_hires/fig_t4_phases.png`
（PNG 3732×1680 @300 dpi、hires 6220×2800 @500 dpi；畫布 12.44×5.60 in）。

🔴 **這張圖左右兩半的證據等級不同，不可混讀**：左＝🟠【估】，右＝🟢【跑過】。
圖上用「`(est.)` 寫在 x 軸標籤裡」＋「右上一行 `4 runs · 09-08 · tutorials harness`」分開，
版面上再隔一條細線。**講的時候要把這條線唸出來。**

---

## 0. 可信度

### 左（階梯）— 🟠 【讀碼推導】＋【估】

`GAP-ANALYSIS` §6 那張表，三個階段的行數 **~140／~330／~205 全部標【估】**（§0 第二點：
「工作量是行數量級的粗估、標【估】」）。x 軸刻度是它們的累計：140 / 470 / 675。
y 軸「解鎖支數」1 / 10 / 13 也來自同一張表（一：「1 支真跑通」；二：「**+9 支**」；三：「**+3 支**」）。
**一支都還沒在 NDTwin fabric 上跑過。**

### 右（2×2）— 🟢 【跑過】2026-09-08

Adam 以 root 跑 `drive_exercise.py` 四次，報告在
`doc/audit/2026-09-04_p4-tutorial-exercise-prep/runs/`（四個檔的「判定」欄逐字）：

| 檔 | 判定 |
|---|---|
| `2026-09-08T092422Z_source_routing_solution.md` | **PASS (5/5)** (exit 0) |
| `2026-09-08T092437Z_source_routing_skeleton.md` | **PASS (2/2)** (exit 0) |
| `2026-09-08T092453Z_basic_solution.md` | **PASS (5/5)** (exit 0) |
| `2026-09-08T092522Z_basic_skeleton.md` | **PASS (4/4)** (exit 0) |

指認 binary（四份報告的 §1 一致）：`/usr/local/bin/simple_switch_grpc`
sha256[:16] **`327fa7d172217397`**（`1.15.3-f0b7d201`）、`p4c-bm2-ss` **`226f3f66df515c9e`**。
🔴 **那顆不是 `bmv2-fast`**（`README.md` §3：兩顆 `simple_switch_grpc` 版本字串相同、sha 不同，
ndt 用的是 `3ff54b5c`）。
🔴 **跑的是 tutorials 自己的 harness、tutorials 自己的 Mininet，不是 NDTwin fabric。**
那四次證明的是「exercise 對的樣子」與「driver 能用」，**不是** NDTwin 跑得動它們——
**在 NDTwin fabric 上仍是 0/13**（`GAP-ANALYSIS` §0 的 09-08 更新、§1 誠實聲明）。
🔴 正本 `runs/` 在 09-08 仍是共用 worktree 裡的**未提交**檔（untracked）。

## 1. 階梯怎麼讀（一個刻意的設計）

**每一階「爬幾格」就等於那階右下方鋪了幾塊名字磚。** 第一階爬 0→1 ⇒ 一塊（`basic`）；
第二階爬 1→10 ⇒ 九塊；第三階爬 10→13 ⇒ 三塊。名字磚填在「該階平台之下、前一階平台之上」
那個矩形裡，所以磚數＝豎直上升量，不必另外標數字。

| 階 | 累計行數【估】 | 解鎖到 | 名字磚（照 §6 逐字） |
|---|---|---|---|
| 一 | 140（＝G1 ~40 ＋ G3 ~15 ＋ G2-A/B ~85） | 1 | `basic` |
| 二 | 470（＋G4 ~150 ＋ G5 ~180 ＝ ~330） | 10 | `qos` `ecn` `mri` `firewall` `basic_tunnel` `source_routing` `calc` `link_monitor` `load_balance` |
| 三 | 675（＋G2-C ＋ G6-A' ＋ G7 ＋ G8 ＋ G9a/b ＝ ~205） | 13 | `multicast` `p4runtime` `flowcache` |

**`GATE` 的位置**：`ACCENT` 豎虛線畫在 **x = 470**，也就是**第二階段做完的那一刻**
（§6 🏁：「**第二階段之後**，tutorial 就可以當 NDTwin 的回歸測試」）。
⚠️ **不是 675**——675 是第三階段做完；線放 675 會被讀成「三階段全做完才有閘門」，
與判詞 `AFTER PHASE 2 / GATE` 相反。

⚠️ **第三階段之前 ecn／mri 會「綠得很可疑」**（沒有 `link=TCLink` 整形 ⇒ qdepth 恆 0，
`GAP-ANALYSIS` §2b①），**不可放進閘門**。圖上不寫，講者備註講。

## 2. 2×2 的四格與「expected fail」

| | `solution` | `skeleton` |
|---|---|---|
| `source_routing` | **5/5** | **2/2** |
| `basic` | **5/5** | **4/4** |

`skeleton` 欄底色 `PANEL`、欄下小字 `expected fail`：**骨架的斷言本來就是「要壞」**，
所以 2/2 與 4/4 是「壞得跟預期一樣」不是「少跑了幾條」。四份報告的判定表逐字：

| | want / got |
|---|---|
| `source_routing` solution（5 條） | 送出 2 幀 `2/2`、h2 收 **`2/2`**、ttl multiset **`[59, 62]`**、SourceRoute 層 **`0 blocks`**、ethertype IPv4 |
| `source_routing` skeleton（2 條） | 送出 2 幀 `2/2`、h2 收 **`0/0`** |
| `basic` solution（5 條） | 送 1 幀、`pingAll` loss **`0.0%`**、`ping -c3` 收 `3`、h2 收 `1`、ttl **`[63]`** |
| `basic` skeleton（4 條） | 送 1 幀、`pingAll` loss **`100.0%`**、`ping -c3` 收 `0`、h2 收 `0` |

⇒ **兩個方向都有預期輸出＝看得到紅**，符合 mutation gate「沒看過紅不算交付」（§6 🏁）。

⚠️ **口徑警告（我自己查到的）**：那四份報告的「來源等級」欄，多數斷言標的是
**【源碼推導，未執行】／【README 宣稱】**——那是指**期望值怎麼來的**，不是指沒跑；
`got` 欄與 exit 0 是真的跑出來的。**上台講「四次實跑」指的是 `got` 這一側。**
另外模板 §B-T 提到的「`s1.log` **91 行** `Dropping packet at the end of ingress`」
**不在 `runs/` 那四份報告裡**（報告只列 `s1.log` 的路徑與 159371 B），
來源是 Adam 在模板裡寫的那段 ⇒ 要用那個數字前先回頭查 log 本身。圖上沒放它。
✅ **auditor 09-08 18:0x 回頭查了**：`grep -c 'Dropping packet at the end of ingress' ~/tutorials/exercises/source_routing/logs/s1.log` ＝ **91**（檔 159467 B、mtime 17:24:36；driver 記的 159371 B 是關機前的大小，差 96 B 是尾行）。數字成立；來源改記為 log 本身（M7 §1.9），不是 `runs/`。

## 3. 圖上**沒有**放的

- 四格底下的細節（收幾包、ttl、91 行）：正本 §B-T 與 `runs/` 有，圖上只留 `5/5` 這種數字。
- `p4runtime` 在 §6 的**第一階段驗證欄**也被點名（「`mycontroller.py` 能與 proxy 共存而不清表」），
  但它**解鎖**是在第三階段 ⇒ 名字磚放第三階（照模板 T4 的逐字清單）。這一條是 §6 表裡
  「驗證方式」與「解鎖」兩欄的差別，不是矛盾；圖只畫解鎖。
- 各 gap 的行數拆解：那是 T2 的徽章。

## 4. Regenerate

```
cd "/home/adam/Desktop/NDTwin slide material/NDTWIN slide material 916/figures/p4-tutorials"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_gap_diagrams.py
```
修改函式：`fig_t4()`。階段與名字磚在 `PHASES` 那個 list、四格在 `CELLS`，都是字面值。
字型與 `_hires` 的口徑見 `fig_t2_gap_architecture.md` §5。

[Co-developed with claude code -- Adam]
