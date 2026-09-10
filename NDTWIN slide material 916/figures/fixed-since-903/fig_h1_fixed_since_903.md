# fig_h1_fixed_since_903 — 903 → 909 的修法看板（**草稿**）

投影片 **H 頁**（`Found, then fixed — since 09-03`，整頁圖）。一句話：
**豎線左邊全是實線磚（已進 trunk）、右邊全是虛線磚（分支上修好、沒併、也沒推）。**

規格正本：`../../NDTwin-slide-template-916.md` §C-909-H。資料正本：`../../FIXED-SINCE-903.md` §1、§2.0–§2.4、§3。
視覺規約：`../../../NDTwin slide material 827/NDTwin-slide-template-827.md` §E2（色票＋Arial）、§E4a（黑框白底、只有一個強調色）。

產出：`fig_h1_fixed_since_903.{pdf,png,svg}` ＋ `_hires/fig_h1_fixed_since_903.png`
（PNG 3732×2100 @300 dpi、hires 6220×3500 @500 dpi；畫布 12.44×7.00 in，16:9）。

🔴 **這是草稿，不是定稿。** §C-909-H 寫「定稿由 Adam 交另一位 agent」；這一張的用途是
**把數字與結構攤開來對帳**——磚的集合、日期欄、豎線兩側的分佈、三類底色，都可以照下面的表逐塊核。

---

## 0. 可信度

| 圖上的東西 | 可信度 | 憑什麼 |
|---|---|---|
| 磚的集合與日期欄 | 🟢 **轉錄自正本** | 逐列抄 `FIXED-SINCE-903.md` §2.0–§2.3、§3；腳本裡是字面值，執行期不讀 repo |
| 分支存在／未併／tip | 🟢 **親自執行** | 09-08 21:0x 在 `/home/adam/Desktop/NDTwin-Kernel` 跑 `git rev-parse` ＋ `git merge-base --is-ancestor <branch> trunk`；29 支全部 unmerged，tip 與正本 §3 逐支相符 |
| 三類底色 | 🟢 **親自執行** | `git show --numstat --format= -m --first-parent <commit>`（§2）／`git diff --numstat <最近的祖先分支>...<branch>`（§3），規則見 §3 |
| 三個 chip 的數字 | 🟡 **一個照抄、一個照 git** | `47` 照正本；`27` 改成 `29`——查 git 得 29，**正本 §1 也已於 09-08 20:4x 自行更正為 29**（§3 標題仍寫 27），而 §C-909-H 的 chip 文字仍寫 27（見 §2、§6） |
| 「0 published」 | 🟠 **轉述，沒有自己驗** | 正本 §0 第四點；而正本自己就寫「tracking ref 只證明沒推、不證明公開狀態」。**這張圖沒有打過任何未認證 HTTPS。** |

## 1. 圖上有什麼（照 §C-909-H 逐項）

| §C-909-H 要求 | 這張圖 |
|---|---|
| 橫軸 `09-02 … 09-08` | ✅ 七欄；欄寬**不等**，按該日需要幾個子欄排（09-03 四個子欄、09-05／09-07 各一個） |
| 09-05 15:27 一條 `ACCENT` 豎虛線標 `last merge` | ✅ 畫在 09-05 欄的右界（`cdc8dad9`） |
| 上帶 `ON TRUNK` 實線磚 | ✅ 67 塊，全部在豎線左邊 |
| 下帶 `ON BRANCHES · NOT MERGED` 虛線磚 | ✅ 29 塊，全部在豎線右邊 |
| 每支修法一塊磚、只寫代號 | ✅ 沒代號的寫分支短名（`rate denom`／`conventions`／`intent-tmpdir`） |
| 底色三類＋圖例三格 | ✅ 見 §3、§4 |
| 09-02 欄 `?` 角標 | ✅ 20 塊全部有 |
| `+7 docs` 小字 | ✅ `ON TRUNK` 帶右端 |
| 三個 chip | ✅（第二個的數字改了，見 §2） |
| 判詞 `FIXED / NOT SHIPPED` | ✅ 右下，`ACCENT` 色條＋`ACCENT` 字 |

## 2. 磚數對帳

腳本每次執行都印這兩行（就是 assert 的內容）：

```
bricks ON TRUNK              : 63   (section 1 expects 63 = 47 + 16)
bricks ON BRANCHES, NOT MERGED: 29   (section 3 header says 27; its table has 29 rows, git agrees with 29)
```

| 帶 | 磚數 | 正本怎麼算 | 對不對 |
|---|---|---|---|
| `ON TRUNK` | **67** | §1：47（§2.1 30＋§2.2 9＋§2.3 8）＋ §2.0 的 **20** | ✅ 對。§2.0 09-08 核對後補到 20 列（16 修法＋4 儀器／接線測試）；§2.1 表裡有 32 列，其中 `9b85ee11`（KNOWN-ISSUES 批次登記）與 `582241ef`（#52 文件半）是純文件、不畫磚 ⇒ 30 塊 |
| `ON BRANCHES` | **29** | §1 現在寫 **29**（`refs/heads/fix/*` 未併 28 支＋`chore/conventions-0906`）；§3 的**標題**仍寫 27 | ✅ 對。§3 的表本身就是 **29 列**；`git for-each-ref refs/heads/` ＋ `merge-base --is-ancestor` 09-08 21:0x 查出未併的正好是 **`fix/*` 28 支＋`chore/conventions-0906` 1 支＝29**，29 支的 tip 與 §3 逐支相符 ⇒ **圖畫 29，chip 也寫 `29 BRANCHES WAITING`** |

> 🟡 **兩處還停在 27**：`FIXED-SINCE-903.md` §3 的標題「（27 支；09-06 → 09-08）」，以及 §C-909-H 規格裡的 chip 字串 `27 BRANCHES WAITING`。
> （本圖起稿時 §1 也寫 27；正本 09-08 20:4x 已自行更正成 29，與這張圖一致。）本 session 不動正本、不動模板。
>
> ✅ **09-02 欄已補到 20 塊。** 起稿時 §2.0 的表只有 16 列而 §1 寫 20；09-08 核對後 §2.0 補上了
> `A-8`／`B-1（接線測試）`／`（儀器）G-2 殘餘`／`（儀器）A-4e` 四列，圖與 assert 已跟上（trunk 磚 63 → **67**）。
> **chip 的 `47` 不動**——47 的定義是 09-03 → 09-05 的分支，09-02 那一欄（帶 `?` 的 20 塊）本來就不算在內。

`W4／#54` 沒有磚：§2.3 末尾自陳「只交選項、沒動碼——不算修」。

## 3. 三類底色的判法

§C-909-H：kernel C++＝`ACCENT_BG`、`ndt`／lab 工具＝`PANEL`、proxy／harness／docs＝白。判定規則寫死如下，**每一塊都可以照 §4 的表重跑**：

1. **量哪個 diff。** §2 的磚量它「進 trunk 線」那顆 commit（`git show --numstat --format= -m --first-parent`）。
   §3 的磚量 `git diff --numstat <最近的祖先分支>...<branch>`——**不是對 trunk**：那幾條鏈是疊起來的
   （W8→W8b→E-20、W3-3b→W15→W15b→BUG17→E-23/25、ndt-honesty→W16→ndt-round2／3-51、W14→W18、W8-8→E-4、intent-tmpdir→E-17），
   對 trunk 量會把前面幾支的檔案算到後面那支頭上。
2. **只算 production 檔。** 排除 `doc/**`、任何 `.md`、以及 `tests/` 底下的單元測試與 `mutate_*.sh`／`test_*.sh` 閘門腳本
   ——每一支修法都附一份 FIX 報告與一支變異閘門，行數比修法本身大一個量級，不排掉的話 91 塊裡有 70 塊會被判成「docs」。
   例外：`tests/shell/check_*.py` 是閘門**儀器**（不是某支修法的證據），算 production，歸白；
   `doc/audit/**/harness/**` 是 harness 本體（chaos harness、live-round harness），算 production，歸白
   ——這條原本只收 `2026-08-28_chaos-harness/harness/*.py`，補 `G-2 instr` 時放寬到所有 `doc/audit/**/harness/**`；
   **放寬後把原本 92 塊全部重跑，判定一塊都沒變。**
3. **分三類。** `src/`＋`include/` → kernel C++；`tools/test_workflow/`＋`tools/remote-lab/` → `ndt`／lab；其餘（`p4_proxy/`、`tools/contract_test/`、`tools/ryu_apps/`、chaos harness、`testbed_topo.py`、`cmake/`、閘門儀器）→ 白。
4. **贏家要拿到 ≥ 60% 的 production 增刪行**，否則標**混合**、畫白底。
5. production 檔一個都沒有的（純閘門／純測試／純文件的 commit 或分支）也畫白底，表裡標「（沒有 production 檔）」。

**兩塊的 commit 換過**（正本那顆不是碼）：
- `#46/#36/#35` 正本寫 `34e2109d`，那是把 raw 移出去的 merge（`-1025` 行 log）；碼在 **`7e8d91e0`**（§C-909 也是這樣寫的），照它判。
- `#27/#76` 正本寫 `ac703196`（閘門補件），並自陳「本體 `63792cc9`」；照 `63792cc9` 判。

### 結果

| 類別 | 底色 | trunk | 分支 | 合計 |
|---|---|---|---|---|
| kernel C++ | `ACCENT_BG` | 32 | 14 | **46** |
| `ndt`／lab 工具 | 深 `PANEL`（見 §6） | 14 | 4 | **18** |
| proxy／harness／docs | 白 | 21 | 10 | **31** |
| **混合**（判不出來，畫白） | 白 | 0 | 1（`E-2`） | **1** |
| | | 67 | 29 | **96** |

§2.0 09-08 補的那 4 塊（`A-8` `aa44bdf1`／`B-1 test` `e88f1b71`／`G-2 instr` `9f022901`／`A-4e instr` `99e9abd9`）
**四塊全部是白**：`B-1 test` 整顆只有一支 `test_t11_filter_is_wired.py`（沒有 production 檔）、
`A-8` 97% 落在 `tools/contract_test/`（契約測試）、`G-2 instr` 100% 落在 live-round harness、
`A-4e instr` 整顆只有閘門儀器 `check_gate_anchors.py`。**沒有一塊碰到 `src/`／`include/`。**
⇒ 09-02 欄由 10 藍／0 灰／6 白變成 **10 藍／0 灰／10 白**。

**判不出來的只有一塊：`E-2`**（`fix/e2-kernel-reports-loaded-model`）——production 增刪 416 行分成
kernel 178（`TopologyAndFlowMonitor` 回報載入的模型 sha）／`tools/test_workflow/run_layers.sh` 130／`tools/contract_test/spec.py` 108，
最高只有 43%，三層各佔一塊，所以標混合、畫白底。

## 4. 逐磚分類表

### §2.0 — 09-02 fix-design campaign（20 塊，全部帶 `?` 角標）

| 磚 | 正本寫的進 trunk 線 | 實際量的 commit | 主要改動路徑（production 檔；已去掉 doc／`.md`／閘門與單元測試） | 類別 |
|---|---|---|---|---|
| `A-2` | `404b11a8` | 同左 | `tools/ryu_apps/rest_topology_bounded.py`；`tools/ryu_apps/rest_topology_bounded.patch`；`tools/test_workflow/stack.sh` | proxy／harness／docs（95%） |
| `A-4c` | `0da64329` | 同左 | `p4_proxy/proxy_agent/rule_journal.py`；`p4_proxy/tests/test_rule_journal.py`；`p4_proxy/tests/test_table_generation.py` | proxy／harness／docs（100%） |
| `A-4d` | `8b87a9de` | 同左 | `p4_proxy/tests/test_delete_restores_route.py`；`p4_proxy/proxy_agent/topology_manager.py`；`p4_proxy/tests/test_five_tuple_match.py` | proxy／harness／docs（100%） |
| `A-4f` | `36e3d78a` | 同左 | `src/ndt_core/power_management/OVSPowerStrategy.cpp`；`tools/contract_test/spec.py`；`src/ndt_core/collection/FlowLinkUsageCollector.cpp` | kernel C++（88%） |
| `A-7` | `a4a8eb2c` | 同左 | `tools/contract_test/spec.py`；`tools/contract_test/selftest_fixtures.py`；`p4_proxy/tests/test_flowentry_endpoints.py` | proxy／harness／docs（86%） |
| `A-9` | `49a3f084` | 同左 | `include/ndt_core/lock_management/LockManager.hpp`；`src/ndt_core/http/HttpSession.cpp`；`tools/contract_test/warning_allowlist.txt` | kernel C++（100%） |
| `B-2b/B-4` | `4c49b050` | 同左 | `include/utils/Utils.hpp`；`src/ndt_core/application_management/SimulationRequestManager.cpp`；`src/ndt_core/routing_management/HttpRoutingStrategyBase.cpp` | kernel C++（100%） |
| `B-3` | `bac267cb` | 同左 | `src/ndt_core/http/HttpSession.cpp`；`include/ndt_core/data_management/HistoricalDataManager.hpp`；`src/ndt_core/data_management/HistoricalDataManager.cpp` | kernel C++（96%） |
| `B-x` | `cc9a9ea4` | 同左 | `include/common_types/SFlowType.hpp`；`include/ndt_core/collection/FlowLinkUsageCollector.hpp`；`src/ndt_core/collection/FlowLinkUsageCollector.cpp` | kernel C++（98%） |
| `F-1` | `b259c4d9` | 同左 | `src/ndt_core/power_management/DeviceConfigurationAndPowerManager.cpp`；`include/ndt_core/power_management/DeviceConfigurationAndPowerManager.hpp`；`tools/contract_test/selftest_fixtures.py` | kernel C++（79%） |
| `F-6` | `fc2cd427` | 同左 | `include/ndt_core/power_management/StaleTableCarryForward.hpp`；`src/ndt_core/power_management/DeviceConfigurationAndPowerManager.cpp`；`include/ndt_core/power_management/DeviceConfigurationAndPowerManager.hpp` | kernel C++（100%） |
| `F-8` | `dc969792` | 同左 | `include/common_types/GraphTypes.hpp`；`src/ndt_core/collection/TopologyAndFlowMonitor.cpp`；`src/ndt_core/http/HttpSession.cpp` | kernel C++（93%） |
| `F-13` | `9430bfbe` | 同左 | `src/ndt_core/routing_management/HttpRoutingStrategyBase.cpp`；`include/ndt_core/routing_management/HttpRoutingStrategyBase.hpp`；`include/ndt_core/routing_management/OpResult.hpp` | kernel C++（100%） |
| `F-14/16/4` | `2bda7af1` | 同左 | `src/ndt_core/collection/TopologyAndFlowMonitor.cpp`；`include/ndt_core/collection/TopologyAndFlowMonitor.hpp`；`include/common_types/GraphTypes.hpp` | kernel C++（100%） |
| `F-15` | `33338e15` | 同左 | `p4_proxy/mininet/grpc_ports.py`；`p4_proxy/mininet/p4_testbed_topo.py`；`p4_proxy/mininet/ntg_bmv2_topo.py` | proxy／harness／docs（98%） |
| `A-8` | `aa44bdf1` | 同左 | `tools/contract_test/spec.py`；`tools/contract_test/check_logs.py`；`tools/contract_test/run_contract_test.py` | proxy／harness／docs（97%） |
| `B-1 test` | `e88f1b71` | 同左 | （沒有 production 檔：整顆只有 `tests/python/test_t11_filter_is_wired.py` 468 行） | proxy／harness／docs（白） |
| `G-2 instr` | `9f022901` | 同左 | `doc/audit/2026-08-30_live-full-stack-round/harness/lib.sh`；`.../harness/25_apps_energy.sh` | proxy／harness／docs（100%） |
| `A-4e instr` | `99e9abd9` | 同左 | `tests/shell/check_gate_anchors.py`（閘門儀器；整顆只有這一個檔 680 行） | proxy／harness／docs（100%） |
| `rate denom` | `aba03849` | 同左 | （沒有 production 檔：只動閘門／測試／文件） | proxy／harness／docs（白） |

### §2.1 — 09-03（30 塊）

| 磚 | 正本寫的進 trunk 線 | 實際量的 commit | 主要改動路徑（production 檔；已去掉 doc／`.md`／閘門與單元測試） | 類別 |
|---|---|---|---|---|
| `#58` | `76d299d3` | 同左 | `p4_proxy/tests/test_path_determinism.py`；`p4_proxy/proxy_agent/ryu_topology.py`；`p4_proxy/proxy_agent/topology_manager.py` | proxy／harness／docs（100%） |
| `P4 priority` | `323668ad` | 同左 | `p4_proxy/tests/test_flowentry_endpoints.py`；`p4_proxy/proxy_agent/api_routes.py` | proxy／harness／docs（100%） |
| `L-9` | `002e226c` | 同左 | `tools/make_topology.py` | proxy／harness／docs（100%） |
| `G-7` | `2152d368` | 同左 | `tools/test_workflow/ndtwin-lab`；`tools/test_workflow/test_ndt_lab_session.sh` | ndt／lab（100%） |
| `G-9` | `5e5989c7` | 同左 | `tools/test_workflow/ndtwin-lab`；`tools/test_workflow/faults.sh` | ndt／lab（100%） |
| `G-6` | `c42cc07d` | 同左 | `tools/test_workflow/ndt` | ndt／lab（100%） |
| `redirection` | `49b91654` | 同左 | `tools/test_workflow/ndt`；`tools/remote-lab/ndtwin-vm.sh`；`tools/test_workflow/test_teardown_guards.sh` | ndt／lab（100%） |
| `#22/#23/#24` | `fbb83b03` | 同左 | `tools/test_workflow/ports.sh`；`tools/test_workflow/ndt`；`tools/test_workflow/ovs_4host_topo.py` | ndt／lab（100%） |
| `A-14` | `b5fe780f` | 同左 | `tools/test_workflow/sudo_surface.sh`；`tools/test_workflow/ndt` | ndt／lab（100%） |
| `ndt up ovs` | `50e8b78e` | 同左 | `tools/test_workflow/ndt` | ndt／lab（100%） |
| `B-5/#5` | `0e11c229` | 同左 | `tools/test_workflow/stack.sh`；`tools/test_workflow/supervise.sh`；`tools/contract_test/check_logs.py` | ndt／lab（76%） |
| `#32` | `0b34af5f` | 同左 | `include/ndt_core/collection/TopologyAndFlowMonitor.hpp`；`src/ndt_core/power_management/DeviceConfigurationAndPowerManager.cpp`；`src/ndt_core/collection/TopologyAndFlowMonitor.cpp` | kernel C++（100%） |
| `#10/#18` | `b76a2493` | 同左 | `src/ndt_core/collection/FlowLinkUsageCollector.cpp`；`include/common_types/SFlowType.hpp`；`include/ndt_core/collection/FlowLinkUsageCollector.hpp` | kernel C++（100%） |
| `sflow health` | `ea139d1c` | 同左 | `src/ndt_core/collection/FlowLinkUsageCollector.cpp`；`include/ndt_core/collection/FlowLinkUsageCollector.hpp`；`src/ndt_core/http/HttpSession.cpp` | kernel C++（100%） |
| `#69/#70 doc` | `89857244` | 同左 | `src/utils/Logger.cpp`；`include/utils/Logger.hpp`；`src/main.cpp` | kernel C++（100%） |
| `topo round` | `d00fa57c` | 同左 | `src/ndt_core/collection/TopologyAndFlowMonitor.cpp`；`include/ndt_core/collection/TopologyAndFlowMonitor.hpp`；`src/ndt_core/power_management/DeviceConfigurationAndPowerManager.cpp` | kernel C++（100%） |
| `topo load` | `70c324e1` | 同左 | `src/ndt_core/collection/TopologyAndFlowMonitor.cpp`；`tools/make_topology.py`；`include/ndt_core/collection/TopologyAndFlowMonitor.hpp` | kernel C++（86%） |
| `#4/A-12` | `5e355dda` | 同左 | `tools/test_workflow/ndt`；`tools/test_workflow/ovs_4host_topo.py` | ndt／lab（100%） |
| `#71` | `486d89fb` | 同左 | `p4_proxy/tests/test_journal_is_wired_in_main.py`；`p4_proxy/proxy_agent/main.py`；`p4_proxy/tests/test_journal_wiring.py` | proxy／harness／docs（100%） |
| `#17` | `65d4a32f` | 同左 | `doc/audit/2026-08-28_chaos-harness/harness/probes.py`；`doc/audit/2026-08-28_chaos-harness/harness/invariants.py`；`doc/audit/2026-08-28_chaos-harness/harness/actions.py` | proxy／harness／docs（100%） |
| `#73/#74` | `431d98a5` | 同左 | `tools/contract_test/components.py` | proxy／harness／docs（100%） |
| `#47` | `08267dcb` | 同左 | `src/utils/FdHygiene.cpp`；`include/utils/FdHygiene.hpp`；`src/ndt_core/event_handling/ControllerAndOtherEventHandler.cpp` | kernel C++（100%） |
| `#42/G-10` | `014903fb` | 同左 | `testbed_topo.py` | proxy／harness／docs（100%） |
| `#6/#48/G-11` | `31b9ea8a` | 同左 | `tools/test_workflow/ndt` | ndt／lab（100%） |
| `#78` | `1ec39977` | 同左 | `tests/shell/check_gate_anchors.py` | proxy／harness／docs（100%） |
| `#46/#36/#35` | `34e2109d` | **`7e8d91e0`** | `src/ndt_core/collection/TopologyAndFlowMonitor.cpp`；`src/ndt_core/power_management/P4PowerStrategy.cpp`；`include/ndt_core/collection/TopologyAndFlowMonitor.hpp` | kernel C++（100%） |
| `#69/#70` | `ec0a0445` | 同左 | `src/utils/Logger.cpp`；`include/utils/Logger.hpp`；`src/main.cpp` | kernel C++（100%） |
| `#77` | `06bc713d` | 同左 | `tools/test_workflow/ndtwin-lab`；`testbed_topo.py` | ndt／lab（80%） |
| `#75` | `078b2736` | 同左 | `doc/audit/2026-08-28_chaos-harness/harness/chaos.py`；`doc/audit/2026-08-28_chaos-harness/harness/invariants.py`；`doc/audit/2026-08-28_chaos-harness/harness/antioracle.py` | proxy／harness／docs（100%） |
| `#8` | `48c929fc` | 同左 | `tools/test_workflow/ndt` | ndt／lab（100%） |

### §2.2 — 09-04（9 塊）

| 磚 | 正本寫的進 trunk 線 | 實際量的 commit | 主要改動路徑（production 檔；已去掉 doc／`.md`／閘門與單元測試） | 類別 |
|---|---|---|---|---|
| `A-11` | `257e4eb0` | 同左 | `tools/test_workflow/ndt` | ndt／lab（100%） |
| `#61/#62` | `e9d8a486` | 同左 | `src/ndt_core/collection/TopologyAndFlowMonitor.cpp` | kernel C++（100%） |
| `#38` | `27d48eda` | 同左 | `src/ndt_core/application_management/SimulationRequestManager.cpp`；`include/ndt_core/application_management/SimulationRequestManager.hpp` | kernel C++（100%） |
| `#82` | `3d2b38fe` | 同左 | `src/ndt_core/power_management/OVSPowerStrategy.cpp`；`include/ndt_core/power_management/OVSPowerStrategy.hpp` | kernel C++（100%） |
| `#27/#76` | `ac703196` | **`63792cc9`** | `include/utils/StopSignal.hpp`；`src/ndt_core/power_management/DeviceConfigurationAndPowerManager.cpp`；`src/ndt_core/collection/TopologyAndFlowMonitor.cpp` | kernel C++（100%） |
| `Q12` | `95a9f743` | 同左 | `src/ndt_core/power_management/DeviceConfigurationAndPowerManager.cpp`；`tools/contract_test/spec.py`；`include/ndt_core/power_management/DeviceConfigurationAndPowerManager.hpp` | kernel C++（71%） |
| `#1/A-10` | `d599c476` | 同左 | `src/ndt_core/routing_management/HttpRoutingStrategyBase.cpp`；`include/ndt_core/routing_management/HttpRoutingStrategyBase.hpp` | kernel C++（100%） |
| `#85` | `93edd0fd` | 同左 | `src/ndt_core/power_management/DeviceConfigurationAndPowerManager.cpp`；`include/ndt_core/power_management/DeviceConfigurationAndPowerManager.hpp` | kernel C++（100%） |
| `#2/C-4` | `c2b55184` | 同左 | `src/ndt_core/power_management/DeviceConfigurationAndPowerManager.cpp`；`src/ndt_core/routing_management/Controller.cpp`；`include/ndt_core/routing_management/OpResult.hpp` | kernel C++（100%） |

### §2.3 — 09-05（8 塊）

| 磚 | 正本寫的進 trunk 線 | 實際量的 commit | 主要改動路徑（production 檔；已去掉 doc／`.md`／閘門與單元測試） | 類別 |
|---|---|---|---|---|
| `W7` | `9de04f53` | 同左 | `tools/test_workflow/ndt` | ndt／lab（100%） |
| `W6` | `f8dbad66` | 同左 | `src/ndt_core/http/HttpSession.cpp`；`src/ndt_core/power_management/DeviceConfigurationAndPowerManager.cpp`；`include/ndt_core/power_management/DeviceConfigurationAndPowerManager.hpp` | kernel C++（85%） |
| `W1/#87` | `f2126cc5` | 同左 | `src/ndt_core/routing_management/HttpRoutingStrategyBase.cpp` | kernel C++（100%） |
| `W5/OV-1` | `0903b202` | 同左 | `src/ndt_core/collection/TopologyAndFlowMonitor.cpp` | kernel C++（100%） |
| `#89/W3` | `336d831e` | 同左 | `src/ndt_core/collection/TopologyAndFlowMonitor.cpp` | kernel C++（100%） |
| `#88/W2` | `cff98191` | 同左 | `src/ndt_core/collection/TopologyAndFlowMonitor.cpp`；`include/utils/Utils.hpp`；`src/ndt_core/power_management/DeviceConfigurationAndPowerManager.cpp` | kernel C++（100%） |
| `anchor L1` | `11fd457e` | 同左 | `tests/shell/check_gate_anchors.py`；`tools/test_workflow/l1_unit_tests.sh` | proxy／harness／docs（90%） |
| `anchor 68` | `68c1dde4` | 同左 | `tests/shell/check_gate_anchors.py` | proxy／harness／docs（100%） |

### §3 — 分支上未併（29 塊；虛線磚）

| 磚 | 分支（tip 見正本 §3） | diff 基準 | 主要改動路徑（production 檔；已去掉 doc／`.md`／閘門與單元測試） | 類別 |
|---|---|---|---|---|
| `W8` | `fix/w8-declared-link-failure-sticky` | `trunk` | `include/utils/NetemLinkFault.hpp`；`src/ndt_core/http/HttpSession.cpp`；`src/ndt_core/collection/TopologyAndFlowMonitor.cpp` | kernel C++（97%） |
| `W3-3b` | `fix/w3-door3b-host-empty-ip` | `trunk` | `src/ndt_core/collection/TopologyAndFlowMonitor.cpp` | kernel C++（100%） |
| `W15` | `fix/w15-unknown-brand-rejected` | `fix/w3-door3b-host-empty-ip` | `src/ndt_core/collection/TopologyAndFlowMonitor.cpp` | kernel C++（100%） |
| `W10` | `fix/w10-nickname-overlay` | `trunk` | `src/ndt_core/collection/TopologyAndFlowMonitor.cpp`；`tools/test_workflow/ndt`；`include/ndt_core/collection/TopologyAndFlowMonitor.hpp` | kernel C++（87%） |
| `W14` | `fix/w14-index-zero-guards` | `trunk` | `src/ndt_core/intent_translator/IntentTranslator.cpp`；`src/ndt_core/collection/FlowLinkUsageCollector.cpp`；`src/ndt_core/intent_translator/LLMAgent.cpp` | kernel C++（100%） |
| `W11` | `fix/w11-dispatch-status-accepted-counters` | `trunk` | `include/ndt_core/routing_management/DispatchOutcomeLog.hpp`；`src/ndt_core/http/HttpSession.cpp`；`tools/contract_test/spec.py` | kernel C++（73%） |
| `W12/W13` | `fix/ndt-honesty-0906` | `trunk` | `tools/test_workflow/ndt`；`tools/test_workflow/stack.sh` | ndt／lab（100%） |
| `W16` | `fix/w16-apps-stop-lists-rules` | `fix/ndt-honesty-0906` | `tools/test_workflow/ndt` | ndt／lab（100%） |
| `conventions` | `chore/conventions-0906` | `trunk` | `cmake/sanitizer-flags.cmake` | proxy／harness／docs（100%） |
| `W8-8` | `fix/chaos-blackhole-attach-under-shaper` | `trunk` | `doc/audit/2026-08-28_chaos-harness/harness/actions.py` | proxy／harness／docs（100%） |
| `W3b-3` | `fix/contract-per-node-identity` | `trunk` | `tools/contract_test/spec.py`；`tools/contract_test/selftest_fixtures.py`；`tools/contract_test/run_contract_test.py` | proxy／harness／docs（100%） |
| `intent-tmpdir` | `fix/intent-task-outcomes-per-test-tmpdir` | `trunk` | （沒有 production 檔：只動閘門／測試／文件） | proxy／harness／docs（白） |
| `W15-2` | `fix/w15b-switch-kind-exemption` | `fix/w15-unknown-brand-rejected` | `include/common_types/GraphTypes.hpp`；`src/ndt_core/collection/TopologyAndFlowMonitor.cpp`；`src/ndt_core/power_management/DeviceConfigurationAndPowerManager.cpp` | kernel C++（100%） |
| `W18` | `fix/w18-eighth-index-zero` | `fix/w14-index-zero-guards` | `src/ndt_core/collection/TopologyAndFlowMonitor.cpp` | kernel C++（100%） |
| `W17` | `fix/w17-capacity-current-plane` | `trunk` | `src/ndt_core/http/OpenflowCapacityReport.cpp`；`include/ndt_core/http/OpenflowCapacityReport.hpp`；`tools/contract_test/selftest_fixtures.py` | kernel C++（83%） |
| `W16-1/2/3` | `fix/ndt-round2-0907` | `fix/w16-apps-stop-lists-rules` | `tools/test_workflow/ndt` | ndt／lab（100%） |
| `3-51` | `fix/ndt-3-51-helper-apps-window` | `fix/w16-apps-stop-lists-rules` | `tools/test_workflow/ndt` | ndt／lab（100%） |
| `W8b` | `fix/w8b-withdrawal-needs-observed-failure` | `fix/w8-declared-link-failure-sticky` | `src/ndt_core/http/HttpSession.cpp`；`src/ndt_core/collection/TopologyAndFlowMonitor.cpp`；`include/ndt_core/collection/TopologyAndFlowMonitor.hpp` | kernel C++（99%） |
| `E-20` | `fix/e20-startup-sweep-all-interfaces` | `fix/w8b-withdrawal-needs-observed-failure` | `src/ndt_core/collection/TopologyAndFlowMonitor.cpp`；`include/utils/NetemLinkFault.hpp`；`include/ndt_core/collection/TopologyAndFlowMonitor.hpp` | kernel C++（100%） |
| `E-21` | `fix/e21-link-endpoints-in-contract` | `fix/w8b-withdrawal-needs-observed-failure` | `tools/contract_test/spec.py`；`tools/contract_test/selftest_fixtures.py` | proxy／harness／docs（100%） |
| `BUG-17` | `fix/bug17-mixed-dataplane-refused` | `fix/w15b-switch-kind-exemption` | `src/ndt_core/collection/TopologyAndFlowMonitor.cpp`；`include/ndt_core/collection/TopologyAndFlowMonitor.hpp`；`setting/AppConfig.hpp.example` | kernel C++（99%） |
| `E-23/25` | `fix/e23-e25-exempt-switch-on-wire` | `fix/bug17-mixed-dataplane-refused` | `src/ndt_core/power_management/DeviceConfigurationAndPowerManager.cpp`；`include/ndt_core/power_management/DeviceConfigurationAndPowerManager.hpp`；`include/common_types/GraphTypes.hpp` | kernel C++（95%） |
| `E-4` | `fix/e4-chaos-needs-opt-in-all-actions` | `fix/chaos-blackhole-attach-under-shaper` | `doc/audit/2026-08-28_chaos-harness/harness/chaos.py`；`doc/audit/2026-08-28_chaos-harness/harness/actions.py` | proxy／harness／docs（100%） |
| `E-17` | `fix/e17-test-tmpdir-carries-pid` | `fix/intent-task-outcomes-per-test-tmpdir` | `tests/shell/check_test_tmpdirs.py`；`tools/test_workflow/l1_unit_tests.sh` | proxy／harness／docs（93%） |
| `G-13` | `fix/g13-p4-rule-install-time` | `trunk` | `p4_proxy/tests/test_rule_install_times.py`；`p4_proxy/proxy_agent/rule_install_times.py`；`p4_proxy/tests/test_ryu_flow_stats.py` | proxy／harness／docs（100%） |
| `E-2` | `fix/e2-kernel-reports-loaded-model` | `trunk` | `tools/test_workflow/run_layers.sh`；`tools/contract_test/spec.py`；`src/ndt_core/collection/TopologyAndFlowMonitor.cpp` | **混合**（白） |
| `E-29` | `fix/e29-update-hosts-race-evidence` | `trunk` | `src/ndt_core/collection/TopologyAndFlowMonitor.cpp` | kernel C++（100%） |
| `KIREF` | `fix/known-issues-refs-by-entry-code` | `trunk` | （沒有 production 檔：只動閘門／測試／文件） | proxy／harness／docs（白） |
| `E-1/E-3` | `fix/docs-e1-e3-findings-coverage` | `trunk` | （沒有 production 檔：只動閘門／測試／文件） | proxy／harness／docs（白） |

## 5. 沒有畫進圖的東西

- **§2.4 的 7 顆純文件 commit**（`4088b237`／`deaf0502`／`f0687b34`／`2285c63c`／`1536ff17`／`1a284f75`／`9483b160`）
  ——§C-909-H 明講不畫磚，只在 `ON TRUNK` 帶右端寫 `+7 docs`。
  ⚠️ 其中 `1536ff17`（09-06）與 `1a284f75`（09-07）**在豎線右邊**，所以「豎線右邊沒有 trunk 的東西」這句話
  只對**修法**成立、對文件不成立。`+7 docs` 就放在那一側，講的時候不必迴避。
- **§2.1 的 2 顆純文件 commit**（`9b85ee11` KNOWN-ISSUES 批次登記、`582241ef` #52 的 pps 口徑）——不畫磚，
  也**不算在 `+7 docs` 的 7 裡面**（那個 7 只指 §2.4）。所以 trunk 上的純文件其實是 9 顆。
- **§2.5 的 5 顆（＋1 顆補件）直接落 trunk 線、不走分支的修法 commit**（`1411f163` G-3／`09e72e7b` L-1／`70665602` L-5／`c916bd4c` L-10／`e72ebdfa` G-5／`5c64d432` 補件）
  ——§1 把它們排除在 47 之外（47 的定義是「分支」），§C-909-H 的磚也只取 §2.0–§2.3 ⇒ **不畫磚**。
  ⚠️ 它們**是**修法、**在** trunk 上、日期是 09-03 ⇒ 「09-03 欄 30 塊」數的是**分支**，不是那天進 trunk 的修法總數。
- **§4 的「只登記未修」條目（正本 09-08 20:4x 由 9 改成 8：B-6／B-7／B-8／B-9／B-11／B-12／C-4b／G-12）**——它們不是修法。
- **W4／#54**——§2.3 自陳只交選項沒動碼。
- **每一支的一句話、閘門數、live 與否、合併順序**——全部留在正本，圖上不放句子（§C-909-H 與 CLAUDE.md 的生圖規則）。
- **`0 published` 的證據**——見 §0，這張圖沒有自己驗過公開狀態。

## 6. 與規格不同的地方（三處，都在這裡講明）

1. 🔴 **`ndt`／lab 那一類的底色改深。** §C-909-H 指定 `PANEL`＝`#F7F8F9`，離白只有 3/255；
   在 0.72" 寬的磚上與白底**完全分不出來**，三類底色會塌成兩類、底色就不承載資訊了（第一版渲染出來確認過）。
   改用 **`#DEE3E7`**——仍是中性灰、不是第二個色相，所以 827 §E4a「只有一個強調色」還是成立。
   **定稿那位 agent 如果用 pptx 的填色，可以自行決定要不要回到 `PANEL`**，但要先在投影機尺寸上看一次。
2. 🟡 **第二個 chip 的數字 27 → 29**（§C-909-H 的 chip 字串仍寫 27）。理由在 §2：git 查出來是 29，正本 §1 也已更正成 29；
   讓 chip 與圖上實際的磚數一致，比照抄規格裡那個數字重要。**規格的 chip 字串建議一併改成 `29 BRANCHES WAITING`。**
3. 🟡 **日期欄寬不等寬。** §C-909-H 只說橫軸是那七個日期，沒有規定等寬；09-03 有 30 塊、09-05 只有 8 塊，
   等寬會讓 09-03 疊到 15 列高、其他欄大量留白。改成「一欄需要幾個子欄就給幾格」（總共 14 格），
   `last merge` 的位置仍然落在 09-05 與 09-06 之間，論點不受影響。

另外兩件**照規格做、但值得知道**的事：

- 磚上寫的是**代號欄的縮寫**，不是全部代號：`#3／#21／#49／#83` 那一列用它自己括號裡的 **`A-11`**；
  `fix/ndt-honesty-0906` 用它修的 **`W12/W13`**；`F-14／F-16／F-4` 壓成 `F-14/16/4`。
  兩列都叫 `#69／#70` 的（`89857244` 文字半、`ec0a0445` parser 半）分別寫 `#69/#70 doc` 與 `#69/#70`；
  §2.0 補的四列照 auditor 指定寫 `A-8`／`B-1 test`／`G-2 instr`／`A-4e instr`。
  ⚠️ **圖上有兩塊都叫 `A-8`**：09-02 欄那塊是 `aa44bdf1`（命令關掉的交換機讓三個工具在系統正常時變紅），
  09-03 欄那塊是 `76d299d3`（BFS 平手 ⇒ 拓樸的純函數）。兩塊分屬不同日期欄、09-02 那塊帶 `?`，
  但**代號本身撞名**——正本兩處都寫 `A-8`，這裡照抄沒有改。
- 09-02 那 16 塊全部帶 `?`（🟡 切點前一天）。**Adam 確認 09-03 口頭講過的話，把 `TRUNK_0902` 整個清單清空即可**
  ——腳本會自己少一欄，assert 的期望值改成 `EXPECT_TRUNK = 47`。

## 7. Regenerate

```
cd "/home/adam/Desktop/NDTwin slide material/NDTWIN slide material 916/figures/fixed-since-903"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_fixed_since_903.py
```

matplotlib 3.11.1（腳本開頭 assert 版本）。資料全部是腳本裡的字面值，**執行期不讀 repo、不讀正本**，
所以輸出是 byte-stable；正本改了要手動同步 `TRUNK_09xx`／`BRANCH_09xx` 四＋三個清單與 `EXPECT_*` 三個常數。
字型 Arial → 本機退 Liberation Sans（827 §E2）；`_hires/` 是同一支腳本 500 dpi 直接存的，不是 `pdftoppm`。

[Co-developed with claude code -- Adam]
