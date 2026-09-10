# fig_t3a_silent_zero — 換一支 P4 程式，取樣就靜默歸零

投影片 **T3 左圖**（`WHAT ONLY A FOREIGN P4 PROGRAM REVEALS`）。一句話：**遙測鏈路依
`packet_in` 標頭的第 5 個 metadata id 讀 `sampling_rate`，那個 id 是位置相依的裸常數；
換一支欄位順序不同的 `.p4`，`sampling_rate` 讀成 0，而 `== 0` 的樣本被丟掉且不留任何 log。**

產出：`fig_t3a_silent_zero.{pdf,png,svg}` ＋ `_hires/fig_t3a_silent_zero.png`
（PNG 1680×1710 @300 dpi、hires 2800×2850 @500 dpi；畫布 5.60×5.70 in，直式，
與 `fig_t3b` 同高，設計成同一頁左右並排）。
畫法規約：827 §E4b（**畫程式裡真正的控制流**；判斷框 `PANEL` 底＋1.25pt 框、條件用等寬粗體；
失敗出口 `WARNC` 字＋`WARN_BG` 底；分支標籤 7.5pt）。

---

## 0. 可信度

🟠 **【讀碼推導】。圖右下角的 chip `READ-CODE` 就是這件事。**

`GAP-ANALYSIS` §5-發現①逐字寫：「三處行號本輪抽查逐字確認；**沒有實際換過程式驗證歸零**」。
⇒ **講機制，不要講「我們觀察到歸零」**。讀的樹＝**trunk `1a284f75`**；正本
`GAP-ANALYSIS.md` 當時仍是共用 worktree 的未提交檔（untracked）。

## 1. 每個框對應的原始碼

| 圖上的框 | 出處（本 session 自己 `sed` 讀過的行） |
|---|---|
| `bmv2 clone 1/256` | `p4_proxy/p4_src/ndtwin_switch.p4:411` `clone_preserving_field_list(CloneType.I2E, SAMPLE_SESSION, FL_SAMPLE)`；常數 `:48` `SAMPLE_SESSION = 250`、`:52` `SAMPLE_RATE = 256`（`:21-23` 註解自陳「cloned to the CPU port at 1/256 … matches OVS's sampling=256」） |
| `packet_in header` ／ `fields 1..5 by position` | `ndtwin_switch.p4:162-169` `@controller_header("packet_in") header packet_in_header_t`：`reason`／`ingress_port`／`egress_port`／`frame_length`／`sampling_rate`／`_pad` 六欄 |
| `emitter reads id 5` ／ `= sampling_rate` | `p4_proxy/proxy_agent/sflow_emitter.py:425-429`，`PKTIN_META_REASON = 1` … `PKTIN_META_SAMPLING_RATE = 5`；`:420-423` 註解自陳 **"They are positional, so reordering the header's fields renumbers them"** |
| 判斷框 `== 0 ?` | `sflow_emitter.py:468-469` `sampling_rate = meta.get(PKTIN_META_SAMPLING_RATE, 0)` / `if sampling_rate == 0:` |
| `sample dropped · no log`（WARNC 終端） | `sflow_emitter.py:470` `return None` —— **沒有 log、沒有 counter、沒有例外**。這是這張圖唯一的重點 |
| `sFlow → kernel`（正常出口） | `sflow_emitter.py:471-482` 回 `SampledPacket`；下游合成 sFlow → UDP 6343（`GAP-2` §3 觀察 1） |
| `foreign .p4` ／ `fields renumbered`（右側分支，虛線指回 `reads id 5`） | `GAP-ANALYSIS` §5-發現①：「13 支沒有一支的 controller header 長得跟我們一樣，flowcache 的 `@controller_header` 更是它自己的設計。**這條路以前沒人走過，因為十台一直載同一份 p4info**」 |

## 2. 圖上**沒有**畫、但屬於同一個機制的

- **packet-out 那一半**：`p4_client.py:217,222` 的 `metadata_id = 1 / 2` 也是裸字面。同一個病，
  方向相反；一張圖只講一個方向，講者備註帶過。
- **另外兩處靜默歸零**（`GAP-2` §3 觀察 1）：clone session 沒建 bmv2 直接丟 copy
  （`p4_client.py:342-344`）、agent IP 不在拓樸檔就歸屬於無（`sflow_emitter.py:311-320`）。
  畫進去會讓「一條鏈、一個 0」的故事變成三條，不畫。
- **修法**（G1 候選 A：開機由 p4info 的 `controller_packet_metadata` 按名字解析，~40 行【估】）：
  屬於 T2 的徽章，不重複畫。

## 3. Regenerate

```
cd "/home/adam/Desktop/NDTwin slide material/NDTWIN slide material 916/figures/p4-tutorials"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_gap_diagrams.py
```
修改函式：`fig_t3a()`。字型與 `_hires` 的口徑見 `fig_t2_gap_architecture.md` §5。

[Co-developed with claude code -- Adam]
