# `fig_m2_persona_axis` — 角色扮演的格子：六個人格 × 四條軸，加一個常設角色

**auditor 2026-09-15 起草（09-15 晚修正一版，見文末「已更正」）。草稿（matplotlib），定稿由 Adam 交另一位 agent。**
產生器 `make_method_diagrams.py`（同目錄）。

[Co-developed with claude code -- Adam]

## 這套方法有成文規格

🔑 **正本＝`.claude/skills/overnight-hunt/SKILL.md`（312 行）**。`hunt-0911/` 底下那批 `ROLE-*.md`
是它的一次實例化，不是規格本身。本圖的結構（幾條軸、哪些人格、R7 的地位）全部照規格，
格子裡的角色編號照 09-11 那一夜的實例。

## 可信度

🟢 **親自讀過**：`SKILL.md:131-205`（視角、四條軸、角色牌組、R7）與 11 份 `ROLE-*.md` 的第一行。
🔴 **沒有親自跑過任何一個角色輪。**

## 四條軸（`SKILL.md:149-168`，逐條原文節錄）

| 軸 | 原文一句 |
|---|---|
| **時間** Time | 「作者假設事情照順序發生。」同時做、反過來做、做到一半斷掉 |
| **規模** Scale | 「作者在 4 host 上寫，在 128 host 上跑。」邊界值 0／1／max／max+1 |
| **狀態** State | 「作者假設從乾淨開始。」從上一個實驗的殘骸開始、pidfile 說沒有但 port 被佔 |
| **意圖** Intent | 「作者假設使用者想做『對的』事。」——「**這條軸最難自動生成，也最容易找到真 bug，因為它跳出了測試套件的想像力。**」 |

🔴 **只有四條。** 規格明寫「每個角色**綁一條軸＋一個具體動作面**」（`:170`）——
所以 ROLE-11 標題裡的「文件」是**動作面**，不是第五條軸。

## 格子怎麼來的（逐檔第一行）

| 檔 | 人格 | 軸 |
|---|---|---|
| `ROLE-1-A1.md` | 接班人 | State, Intent |
| `ROLE-2-CYCLES.md` | 重開循環 | Time, State |
| `ROLE-3-STUDENT.md` | 研究生 | Intent, Scale |
| `ROLE-4-CONCURRENT.md` | 第二個操作者 | Time |
| `ROLE-5-TRAFFIC.md` | 流量壓力狂 | Scale |
| `ROLE-6-SUCCESSOR2.md` | 接班人（二） | State, Time |
| `ROLE-8-A1-LIVE.md` | 接班人（三） | State, Intent |
| `ROLE-9-P4-128-CYCLES.md` | 重開循環 | Time, Scale |
| `ROLE-10-P4-128-TRAFFIC.md` | 流量壓力狂 | Scale |
| `ROLE-11-MANUAL-READER.md` | 照手冊的人 | Intent（動作面＝文件） |
| `ROLE-12-LIVE-TEARDOWN-OVERLAP.md` | 第二個操作者 | Time |
| `R7-reconciler.md` | 對帳審計員 | **跨軸、常設、並行** |

產生器內建 `assert n_roles == 11`（不含 R7），格子漏掉一個就 build 失敗。

## R7 那一列為什麼長得不一樣（`SKILL.md:183-192`）

- 其他角色**輪流上場**（只有一座 lab）；R7「**每次夜巡都要派，而且從頭開到尾**，跟當時在跑的角色同時存在」。
- 它能並行的原因寫得很清楚：「**唯讀，沒有例外**…它不持 claim，因此不佔第四步的隊伍」。
- 值得一個常設名額的理由（原文）：09-05 那晚 R7 交出的 4 條不一致裡有三條
  「是在**沒有任何角色在看的時段**露出來的」——
  🔑 **「空窗是唯一沒有主人的時段，而狀態不一致就住在那裡。」**

## 底部那句的出處

`SKILL.md:172` 逐字：「派出去的 prompt 要**寫死角色動機**，不要寫『請測試 X』——
**動機才會生出你想不到的動作序列**。」圖上英文是這句的翻譯。

## 我自己下的判斷（不是原文，要改就改這裡）

1. **人格的英文名是我取的**（`The successor`／`The restart cycler`／`The grad student`／
   `The second operator`／`The traffic pusher`／`The manual follower`／`The reconciler`）。
2. **ROLE-9 我放進 Time 與 Scale 兩格**：標題只寫「重開循環壓力測 × 規模軸」，
   而「重開循環」在規格的牌組表裡是「時間×狀態」。⇒ **這一格是推論**，要嚴格照字面就只留 Scale。
3. **ROLE-11 只放 Intent**：規格說軸只有四條，文件是動作面。**與該檔標題的字面（「意圖軸 × 文件」）
   不同**，我選了規格的分類法。

## 🔴 已更正（09-15 晚，第一版錯了兩處）

| 第一版畫成 | 錯在哪 | 現在 |
|---|---|---|
| 「five axes」，Docs 當第五欄 | 規格只有四條軸，文件是動作面 | 四欄，ROLE-11 收進 Intent |
| 底部「and never handed: **the defect list**, or where to look」 | **對夜巡角色是錯的**——brief 明訂一節「What is already known (**build on it, do not re-derive it**)」，刻意給已知事實避免重複發現 | 改成規格真正說的「a motive, never a test case」 |

🔑 **「不給已知缺陷」那條屬於另一條線**：手冊 usertest 的 tester 才是什麼都不給
（`doc/audit/2026-09-02_manual-usertest/README.md:29`：「**a hint would make it a guided walk**」）。
**同一套方法對兩個不同問句用兩種遮蔽策略**，混寫會把兩條線講成一條。
