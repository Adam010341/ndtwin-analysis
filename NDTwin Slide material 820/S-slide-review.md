# S — Slide template 補充審查（`fbd8140` → `5d53cf0`）

Base：worktree reset 到 `5d53cf0` ✅（開場是上游 `8b61cdc`，第五個中招的 agent）；`tests/` 存在 ✅。
輸入：`/home/adam/Desktop/NDTwin-slide-template.md`（2026-08-11 寫，HEAD `fbd8140`）。
**不改 template，只產報告。** 所有建議已對 template 自己的 A1／A2／A3 過濾。

## TL;DR

1. **⚠️ 差距不是「十幾個 commit」，是 69 個**（`fbd8140..5d53cf0`）。orchestrator 給的估計是 B1 的窄範圍（`b0a7bdc..5d53cf0` = 16）。素材量比預期大一個數量級，本報告據此擴大。
2. **B 節四個數字全部要換**：commit 202 → **271**；gtest 426 → **546**；Python 337+101 → **389+128 = 517**；`tests/python` 2 檔 → **4 檔**、`tests/` 33 .cpp → **43**。
3. **A3.1 的三條量測指令在 `5d53cf0` 仍然準確**，不用改——已驗 `TEST_P` = 0（無 runtime 展開偏差）、無 test 檔在兩個目錄外。grep 數與 B1/B3 實測 runtime 數（546 / 517）逐位吻合。
4. **Phase 狀態要改兩格**：Phase 7 **已完成**（機制＋測試＋live 驗收，`p4_bmv2_support_plan.md:480`）；**Phase 8 的表格格子（:25 寫「⬜ 未做」）與它自己的章節本體（:515-523，四條有三條劃掉標 ✅ 已解）矛盾**——這是 template 沒有的資訊。
5. **Page 33「未完成事項」因此過期**：現在只剩 shell injection 一條、Phase 3、Phase 5 counter-sample、`Answer::from_json`、Ryu wedge root cause。
6. **建議新增 2 頁**：① 第 1 節「Phase 7 電源管理」——**目前整個 Phase 7 在簡報裡沒有任何頁面**，這是最大的結構性缺口；② Page 31 旁的「第二輪獨立審查」——2026-08-12 那輪 **55 條、實質全中零誤判**，比 template Page 31 描述的第一輪大一個量級。
7. **A2 裁定表建議新增 9 條裁定**：**6 條列入 bug 頁**（`f21d7a0`／`57346f6`／`cbb504a`／`5054249`／`59dc5d3`／`ee7233b`，**每條都已 `git show 28b8b13:` 開檔驗證原文**）、**1 條必須拆一半**（`916d330`：power 半邊 baseline、OpResult 半邊照 `8c25dbc` 先例排除）、1 條併入既有 Page 18、1 條待 Adam 裁定（`44fa86e`）。**六條全部符合 Page 14「無聲」主題**，是加強敘事不是打亂它。
8. **⚠️ 兩個會讓簡報 agent 出錯的陷阱**：① `57346f6` 講的是**產品自己的** Intent Translator 用 OpenAI，**不是** A1.3 禁止的「AI 協作開發流程」——不寫明的話 agent 大概率整條砍掉；② `3292653` 的 commit message 與 template Page 18 ④ 對 graph 行為的敘述**互相矛盾**，動筆前必須擇一（見 §5.8）。
9. 第 5 節素材清單已備妥（§3），Page 28 現在填得起來（16.63s 自癒／hitless 復原）。**但素材全在 repo 外 `~/Documents/NDTwin documentation/`，而 template 的 D 節素材出處表只列 repo 內路徑**——agent 找不到就會編。
10. **⛔ readopt 相關的一切先不要上台**（`3a312e3`／`eace67c`）：今晚實測該端點會清空健康 switch 的表還回 success，而那句 502 訊息正是教人去打它。

---

## 1. B 節事實過期（逐條核對）

### 1.1 數字快照（全部在 `5d53cf0` 重量）

| template B 節（2026-08-11） | `5d53cf0` 實測 | 差 |
|---|---|---|
| `28b8b13..HEAD` **202** commit | **271** | +69 |
| `tests/` 33 個 .cpp、**426** gtest | **43** 個 .cpp、**546** gtest | +10 檔 / +120 |
| `p4_proxy/tests/` 12 檔、**337** | **14** 檔、**389** | +2 檔 / +52 |
| `tests/python/` **2** 檔、**101** | **4** 檔、**128** | +2 檔 / +27 |

Python 合計 **517**（389+128），與 B1／B3 各自獨立實跑的 `517 ran` 逐位吻合。
gtest **546 / 68 suites / 0 skip**（B1 實跑）與 grep 546 逐位吻合。

`tests/python/` 現有四檔：`test_contract_spec.py`、`test_p4_power_helper.py`、`test_route_install_gate.py`、`test_route_reinstall.py`。
**「未註冊進 ctest、獨立執行」這句仍成立**——已驗 `tests/CMakeLists.txt` 全檔無 `python` 字樣。

**+120 gtest 的成因**（回答 orchestrator 的「查哪些 commit 加的」）：見 §1.2，不是單一 commit，是三條主線。

### 1.2 +120 gtest / +10 .cpp 的成因（`git log --numstat -- tests/`）

**十個新測試檔**，全部來自三條主線：

| 主線 | 新檔 | commit |
|---|---|---|
| **Phase 7 電源管理** | `test_P4PowerStrategy.cpp`（266 行起） | `9afd647`、`99fd1f1`、`eace67c`、`2abf1e3`、`3a312e3` |
| **四主題 audit（AUDIT A/B/C/D）修復** | `test_HistoricalLogging.cpp`(325)、`test_ApiKeyNotLogged.cpp`(209)、`test_IntentTaskOutcomes.cpp`(390)、`test_HttpSessionStatusCodes.cpp`(240+45+16)、`test_ReverseEdgeLookup.cpp`(143+56)、`test_SmartPlugFields.cpp`(195)、`test_TopologyUrlAndPathJson.cpp`(223)、`test_CommandFailure.cpp`(97) | `ee7233b`、`57346f6`、`916d330`、`1145372`/`4c56ff7`/`d505b9d`、`cbb504a`/`6dd0485`、`59dc5d3`、`2609adc`、`ac07b0f` |
| **控制平面 ingest 加固** | `test_PathNodeParsing.cpp`(166)、`test_ParamParsing.cpp`(+52)、`test_TopologyAndFlowMonitor.cpp`(+202/+78/+61) | `f21d7a0`、`0d3bc9c`、`e7c308d`、`d505b9d` |

Python 側 +52/+27 同理：`test_p4_power_helper.py`（455+138+48 行，Phase 7）、`test_route_install_gate.py`（169 行，`801407f`）、`test_readopt.py`（`09a7a81`）。

→ **建議：Page 25 的數字換掉之外，加一句成因**——「一天內 +120 個 gtest，不是灌水：十個新測試檔對應 Phase 7 落地與一輪 55 條的獨立審查修復，每個修復都帶自己的測試」。非瑣碎理由：教授看到「426 → 546」會問怎麼來的；答不出成因，數字反而變扣分項。

### 1.3 A3.1 的三條量測指令：**仍然準確，建議不動**

逐條驗過，這是 A3 規則自己要求的「動筆重量」能不能信的問題：

- `TEST_P` 數 = **0**，`INSTANTIATE_TEST_SUITE_P` = 0 → 沒有 runtime 展開，grep 一條 = runtime 一條。（這是 grep-vs-runtime 最典型的偏差來源，這個 repo 剛好沒踩。）
- 拆解：`TEST(` 150 + `TEST_F(` 396 = 546，與總數自洽。
- 無 gtest 檔在 `tests/` 之外；無 `def test_` 的 .py 在 `p4_proxy/tests/`＋`tests/python/` 之外。
- 三條指令的輸出（546 / 389 / 128 / 271）與兩個 agent 的實跑數字一致。

→ **建議：A3.1 不改指令**，但值得加一句「已於 `5d53cf0` 驗過 `TEST_P`=0，若日後出現參數化測試，grep 數會低估 runtime 數」。這是非瑣碎的，因為 A3 的整個立論就是「數字動筆當下重新量」，而它沒說量法本身何時會失效。

### 1.4 Phase 狀態（對 `doc/p4_bmv2_support_plan.md` 現版核實）

| Phase | template B 節說 | 現版 plan 說 | 出處 |
|---|---|---|---|
| 7 | 部分（PID manifest 已建未用） | ✅ **完成** | `:24` 表格格子、`:480` 章節標題 |
| 8 | 未開始 | **表格 `:25` 說「⬜ 未做」，章節 `:515-523` 說四條有三條 ✅ 已解** | 見下 |
| 5 | 一半 | 一半（未變） | `:21` |
| 3 | 未開始 | 未做（未變） | `:23` |
| 0,1,2,4,6 | 完成 | 完成（未變） | `:17-22` |

**Phase 7 已完成的內容**（`:480-504`，逐條有 commit）：PID manifest（`22ada58`）＋ root helper `ndtwin-p4-power`（`624946d`）＋ `P4PowerStrategy` 真的呼叫它並在 `on` 之後要求 proxy readopt（`1978292`）＋ mutation 驗證過的測試（`9afd647`、`09a7a81`）＋ `on` 逾時的 orphan 修掉（`8eaa133`）＋ 失敗訊息改成講真正有效的復原路徑（`2abf1e3`）。Live 驗收：關掉一台、其餘九台 **9000/9000 封包零遺失**，關掉那台在 helper 回報 stopped 前 0.3 秒就停止轉送（`:495-497`）。

**Phase 8 的自相矛盾**（觀察，非推論——兩處都開檔讀過）：
`:25` 表格格子寫「⬜ 未做」，但 `:515-523` 的 Phase 8 章節本體：
- 散落腳本搬離根目錄 → ~~刪除線~~ **✅ 已解**（2026-08-12，五檔搬到 `p4_proxy/reference/`，port 8080→8081）
- `requirements.txt` protobuf 自相矛盾／缺 `requests` → ~~刪除線~~ **✅ 已解**
- CHANGELOG 沒有 P4 紀錄 → ~~刪除線~~ **✅ 已解**
- 「把暫緩的 shell injection 另外開一個 issue 追蹤」→ **唯一未劃掉的一條**

→ 也就是說 **Phase 8 四條剩一條**，而那一條是「開 issue 追蹤」不是寫程式。表格格子沒跟上。

**建議動作**：
- **B 節 Phase 快照改寫**為：Phase 0–2、4、6、**7** 完成；Phase 5 一半；Phase 3 未做；**Phase 8 四條已解三條，僅剩 shell injection 的追蹤條目（且 plan 的摘要表格自己還停在「未做」）**。
- **Page 33（總結與未完成事項）連動更新**：template 現在寫「Phase 3、8 未開始；Phase 7 部分」——三格全錯。改成「Phase 3 未做、Phase 5 counter-sample 半邊、Phase 8 剩追蹤條目；`Answer::from_json` 第四例未修；Ryu wedge root cause 未證明；shell injection 刻意延後」。
- 非瑣碎理由：Page 33 是**對教授誠實交代未完成**的那一頁，講錯方向（把已完成的說成未開始）比講漏更傷；而且 Phase 7 是整個電源管理主線。

---

## 2. 新 commit 裡的 slide 素材（`fbd8140..5d53cf0`，已按 A1／A2 過濾）

### 2.1 ⭐ 建議新增：Page 12.5 —「Phase 7：電源管理真的能用」（第 1 節）

**這是最大的結構性缺口。** template 寫在 Phase 7「部分完成」的時代，所以第 1 節（新增功能 Page 6–13）**整個沒有電源管理的頁面**——而 Phase 7 現在是完成的、有 live 驗收數據的、九個 commit 的主線。

- 要點：① **問題**：baseline 的 P4 關機是 `sudo mnexec -a s1 pkill -f simple_switch_grpc`——`mnexec -a` 要 PID 卻給了名字（根本不執行），就算能跑 `pkill -f` 會**把十台 switch 全殺光**（Mininet node 共用 PID namespace）；`powerOn` 是什麼都不做就回 `true` 的空殼。② **做法**：拓撲腳本啟動每台 bmv2 時寫 PID manifest（`22ada58`）→ root helper `ndtwin-p4-power` 只對 manifest 記載的那**一個** PID 送 SIGTERM，送之前再對 `/proc` 驗一次（`624946d`）→ `P4PowerStrategy` 真的呼叫它，並在 `on` 之後要求 proxy `POST /p4/readopt/{dpid}` 重掛 mastership／pipeline／clone session／routes，否則重啟後的 switch 一個封包都轉不動（`1978292`）→ 兩個操作都回誠實的 `OpResult`。③ `pkill` 是整條路徑的**禁字**，理由寫在 `P4PowerStrategy.cpp` 檔頭的匿名 namespace 註解裡。
- 素材：`doc/p4_bmv2_support_plan.md:480-511`（逐條規格 vs 結果對照表）、`doc/phase7_power_mechanism_design.md`；commit `624946d`、`1978292`。
- 非瑣碎：這是 Phase 7 整段，且「禁用 `pkill` 並在程式碼裡寫下理由」是很好的工程判斷展示。

### 2.2 ⭐ 建議新增 bullet：Page 12.5 或 Page 23（方法論）—— gRPC subchannel pool

**今晚 live 實測 135 秒關機 → 1.50 秒重連**（A-live-runbook），對照修復前的失敗。

- 要點：關機夠久之後 `powerOn` **必定失敗**，而且失敗訊息是 `UNAVAILABLE ... Connection refused`——打在一個**正在 listen 且正常 accept TCP 的 port** 上。根因：gRPC 的 **process-global subchannel pool** 按目標位址共用 subchannel；switch 關著的期間 liveness poller 每 2 秒探它一次（四分鐘約 120 次失敗連線），把該位址的 reconnect backoff 推到 gRPC 的 120 秒上限；`readopt_switch` 建的**全新** client 拿到的是同一個已經 backoff 的 subchannel。修法：`grpc.use_local_subchannel_pool`。
- **量化證據（極好的投影片素材）**：對 grpc 1.82.1 實測——對著關閉的 port 猛打 90 秒後在同一位址、同一 process、同一瞬間起真 server：**帶 option 的新 channel 0.00 秒 READY，不帶的要 32.56 秒**。
- **配套的方法論故事**：gRPC 會**安靜忽略**它不認識的 channel option，所以拼錯一個字在 runtime 零成本、直到下一次 power-cycle 才爆——因此測試**明寫出完整 option 字串**。兩個 mutant 都會死（移除 option、拼錯 option 各殺三條新測試中的兩條）。
- 素材：commit `e7d564b`（完整 message，幾乎可直接改寫）、merge `949fcba`；live 數據見 §3。
- 非瑣碎：這是「症狀完全誤導人」的教科書案例（連線被拒 vs port 開著），且有乾淨的對照實驗數字。

### 2.3 Page 11（證據式存活偵測）補一條：死 switch 從清單**消失**

- 要點：`render_switches` 的契約一直寫著「proxy 連不到的 switch 不會出現，所以 kernel 不會標它 enabled」，**壞的是呼叫端**——`topology_switches` 傳的是 `switches.keys()`，也就是「有史以來建過 client 的每一台」；殺掉一台的 process 不會移除它的 entry，所以死掉的 bmv2 持續被回報成 connected，**而同一個物件、同一時刻的 `/p4/switch_state` 卻說 `probe_ok=false`、`stream_alive=false`——同一個 process 的兩個端點互相矛盾**。kernel 信前者：`updateSwitches` 對列出的每個 dpid 無條件 `isUp = true`，所以孿生在每次拓撲輪詢都把已關機的 switch 宣告成活的，一秒後才被 1 Hz liveness worker 改回來。
- **量測方法本身值得講**：以 10 Hz 取樣 `is_up`，看到 up-blip **跟著輪詢自己的 5s→30s 節奏**出現（這正是「用 cadence 指認寫入者」的手法）。
- 只有**明確的 false** 才排除一台：從未完成的探測不是死亡證據，把它報成 disconnected 會讓 fabric 在每次啟動的頭幾秒全黑——與 `p4LivenessFor` 同一套三態規則，刻意保持一致，讓兩個 process 不會對「沒有讀數」的意義各說各話。
- 素材：commit `32afeb9`（完整 message）。live 驗證：dpid `0a` 從 `/v1.0/topology/switches` 消失、**678 筆 10 Hz 取樣零 up-blip**（A-live-runbook）。
- **⚠️ 誠實邊界**：修的是 **proxy 側**。kernel 側 `TopologyAndFlowMonitor.cpp:565` 仍然無條件 `isUp = true`（已開檔驗證）——也就是「不再餵它壞資料」而不是「它現在會自己判斷」。B2 已確認兩份文件一寫已修一寫未修**兩者都對**。這句要進備註，否則 Q&A 會被問破。

### 2.4 Page 13（其他功能）補：南向失敗可見化的**最後一哩**

template Page 13 已有 `OpResult` 一脈（含 `8c25dbc`）。新增兩條同脈：

- `eace67c`：`curl -sS -f` 把 readopt 的**失敗步驟**丟掉，兩邊 log 都查不到 → 改 `--fail-with-body`，proxy 對失敗 readopt 的說法才能到達 kernel log。
- `3a312e3`：`powerOn` 的 502 訊息改成講**實測有效**的復原路徑；先前寫的「off 再 on」**實跑證明也回 500**（`2abf1e3` 拿行不通的建議換了沒驗證過的建議——這句誠實得值得留）。
- **⛔ 但是**：今晚 A 實測 `POST /p4/readopt/{dpid}` 對**健康** switch 會清空整張表、裝回 0 條路由、還回 `"status":"success"`（s1、s6 兩台重現）。**502 訊息現在把操作者指向一個危險指令。** → **建議：這兩條先不要上投影片**，或只講「`--fail-with-body`：失敗的身體也要讀」這個一般性教訓，不要展示那句復原指引。等缺陷修掉再說。（此缺陷在 Adam 自己的 proxy 碼裡，按 A2 **不進 bug 頁**。）

### 2.5 不建議上頁面（已查證，記錄以免下一輪重查）

`3fc42ed`（搬腳本）、`f3759ae`（skipUnless）、`5d53cf0`／`78bdea0`（行號改 symbol）、`8090d60`（刪 scratch binary）、`b7d558b`、`9a954a7`、`f103764`、`d1ca197`、`7eddd68`、`0ffaad1`、`9894b90`、`6b40846`、`085d54c`、`cd3929a`、`4e58fd6`、`902d1ab`、`69a4b4d`——文件與整理類，單獨不成頁。
**但它們合起來有一個非瑣碎的故事**，見 §4.3。

---

## 3. 第 5 節（實機測試）素材清單 —— Page 28／32 可直接引用

template 說第 5 節骨架留白等 Adam 提供。**Page 28（Failover 端到端驗證）的 `【Adam 後續提供】` 現在可以填了。**

### 3.1 檔案位置（⚠️ 全部在 repo 外）

| 檔案 | 內容 |
|---|---|
| `/home/adam/Documents/NDTwin documentation/Overnight review 2026-08-12/A-live-runbook.md`（718 行） | bmv2 全輪 Phase 0–6，含逐段時間戳與觀察 |
| 同目錄 `C-live-ovs-runbook.md` | OVS 對照輪（S 收筆時仍在跑；**若完成即為 Page 27 L4 差異比對的活數據**） |
| 同目錄 `INDEX.md` | 五個 agent 的彙整 |
| `/home/adam/Documents/NDTwin documentation/Commit review/ADJUDICATION_AUDIT_ABCD_2026-08-12.md` | 55 條四主題審查裁決（Page 31 用） |

→ **建議：template 的 D 節「素材出處速查」加一列「實機測試與審查原始紀錄 → `~/Documents/NDTwin documentation/`（repo 外）」。** 非瑣碎理由：D 節現在**只列 repo 內路徑與 commit**，簡報 agent 會在 repo 裡找 Page 28 的數據並且找不到，然後很可能就編一個。

### 3.2 Page 28（Failover 端到端）可直接上投影片的數字

全部來自 A-live-runbook，bmv2 10 台、HEAD `5d53cf0`：

- 斷鏈手法：`s6-eth3 ↔ s9-eth2`，`tc netem loss 100%` **雙端**（對端自 topo 推導，非照抄 runbook 範例）
- 偵測：**2 筆 down 通知、零假訊**；edge 由 40 → **38/40**
- 規則改變：`OUTPUT:3 → 4`；重繞路徑 **`1 6 10 7 4`**
- **中斷時長：ping 停 16.63 秒後自癒**
- **復原：hitless，0 封包遺失**
- 收尾：netem 零殘留
- 補充：power-cycle 過的 s10 **實測扛得住真流量**（不只是「起得來」）

### 3.3 Page 32（Demo）候選——現在有實測背書

template 列了三個候選，全部今晚驗過可行：① 斷鏈 failover（16.63s 自癒 + hitless 復原，數字漂亮）；③ killed switch 的 liveness 三態（dpid `0a` 從清單消失，10 Hz 678 筆零 up-blip）。
**⛔ 不要 demo readopt**（§2.4）。

### 3.4 誠實邊界（**必須進備註**，否則是在誇大）

- `3a312e3` / `eace67c` 今晚**未觸發**（全程沒遇到 502）→ **標為未驗證**，A 自己就是這樣記的。不要寫成「已驗證」。
- Phase 7 的 live 驗收（九台 **9000/9000 零遺失**、關掉那台在 helper 回報 stopped 前 **0.3 秒**停止轉送）出自 `doc/phase7_power_mechanism_design.md` 的「Live 驗收結果」，是**較早那一輪**，不是今晚這輪。兩輪不要混講。
- 今晚這輪同時**找到一個 P1 新缺陷**（readopt 清表）。**這件事本身是 Page 31／Page 23 的好素材**——「跑完整輪 live 驗證的價值不在於全綠，而在於它抓到了三個靜態 agent 都驗過『存在、接線正確、可貼上』的端點其實是壞的」。

---

## 4. 結構性缺口（整頁等級）

### 4.1 ⭐ 第 1 節缺 Phase 7 頁 —— 見 §2.1。（最大的一個）

### 4.2 ⭐ 建議新增：Page 31.5 或併入 Page 31 —— 第二輪獨立審查（55 條）

template Page 31 描述的是**較早那一輪**（51 次唯讀檢查／12 項發現；47 項 HIGH 裁定出 21 項真問題）。
**2026-08-12 又跑了一輪，規模與命中率都不同一個量級**：

| | 條數 | 實質成立 | 引用正確 |
|---|---|---|---|
| A 幻覺／假斷言 | 28 | 28 | 27 |
| B 測試完整性 | 6 | 6 | 6 |
| C 寫死假設 | 9 | 9 | 8 |
| D 吞掉的錯誤 | 12 | 12 | 12 |
| **合計** | **55** | **55** | **53** |

- **55 條實質全部成立、零誤判**，處置分 Tier 1–4，**Tier 1 四條全修完**。
- **最值得講的一句（方法論，非工具）**：命中率的差別**在 prompt 形狀，不在模型**——對照組是前一輪 47 個 HIGH 裡有相當比例是誤判。
- 兩處引用瑕疵**自己也記下來**（audit 引 `IntentTranslator.hpp:324-326`，那個檔只有 56 行；另一處 48 小時內測試檔數 13→14 就腐爛了——**恰好證明該條自己的論點**）。
- 素材：`ADJUDICATION_AUDIT_ABCD_2026-08-12.md`（repo 外，路徑見 §3.1）；Tier 1 四條的 commit `f21d7a0`／`3292653`／`5054249`／`cbb504a`。
- **依 A1.3 敘述用「第三方交叉檢查／獨立審查」，與 Page 31 現有措辭一致，不提工具。**
- 非瑣碎理由：這一輪產出了**至少五個新的 baseline 缺陷**（§5），直接餵養第 2 節；只講第一輪等於把最新、最有系統性的那一輪丟掉。

### 4.3 建議：Page 23（方法論）加第 ⑤ 點 —— 「引用會腐爛」作為一條工程紀律

§2.5 那批「瑣碎」commit 合起來是一個**有證據的方法論主張**，不是雜務：

- `5d53cf0`／`78bdea0`：把 runbook 與註解裡的**行號引用改成 symbol 名**——因為行號「在同一個小時內就腐爛了」（commit 標題自己這樣寫）。
- `7eddd68`：**把烘進三份測試文件的測試數字拿掉**，而不是再更新一次。
- `1d05e98`（28 條 AUDIT_A）：每一條腐爛引用**重新 grep 引文原文**去推導；**已經腐爛過兩次的數字（測試數、不可達的 status code）直接移除而不是再更新**。
- `0ffaad1`：整節撤回（`test_coverage_gaps.md` §1.2 三條全假）。
- 今晚的獨立佐證：B4 查 `p4_manual_test_runbook.md` 時，**全檔唯一存活的引用就是唯一用 symbol 不用行號的那一處**；五處行號引用全漂。
- 非瑣碎理由：這是可量化、可驗證的工程紀律（「引用要指向會跟著改的東西」），而且它跟 Page 23 現有的四點同構——都是「不讓錯誤偽裝成正確」。也剛好回答教授可能問的「你怎麼確保文件沒騙人」。

### 4.4 不建議另開頁的

- 「隔夜自動化驗證輪」**不建議另開一頁**：它的價值已經被 §3（第 5 節數據）與 §4.2（審查輪）吸收，單獨成頁會逼近 A1.3 的紅線（講執行方式而非成果）。**建議改為 Page 23 的一句話**：「同一份 runbook 由不熟悉實作的一方獨立跑完整輪，比全綠的測試套件更會抓到東西」——並用今晚的具體例子（readopt 端點三個靜態檢查全過、live 一跑就壞）當佐證。

---

## 5. A2 裁定表建議新增條目

方法一律照 template：`git show 28b8b13:<path>` 讀 baseline 原文，**不看 CHANGELOG 敘述**。以下每條都已開檔驗證，附 baseline 行號與原文特徵。

### 5.1 【列入 bug 頁】`f21d7a0` — 一個缺欄位的控制平面回應殺掉整個 kernel

- **baseline 驗證**：`28b8b13:src/ndt_core/collection/TopologyAndFlowMonitor.cpp:314` = `uint64_t switchDpidUint64 = stoull(switchDpidStr, nullptr, 16);`，其上 `:313` 是 `.value("dpid", "")`（缺欄位得到 `""`）。整個 `updateSwitches` **唯一的 catch 是 `catch (const json::parse_error& err)`**（`:340`）——`std::invalid_argument` 不是 `json::parse_error`，直接逃逸。三個 ingest 各有一個同款 catch（`:340`／`:421`／`:504`），**三個都只接 `json::parse_error`**。
- **逃逸路徑同樣是 baseline**：`28b8b13` 的 `updateGraph`（簽名在 `:512`）連續呼叫 `updateSwitches`／`updateHosts`／`updateLinks`，**三個都不在任何 try 裡**。
- **同族**：baseline `updateHosts`（`:367`）`macToUint64(host["mac"])` 無防護；`:382` `ipStringToUint32`；錯誤路徑裡還有 `host["mac"].dump()`——**在 mac 本身就是問題時才會走到**。
- **裁定：baseline crash bug，列入 Page 15（Crash 類）。**
- **⚠️ 誠實註記（照 Page 20 ② 的既有先例寫法）**：baseline 只在**啟動時抓一次**拓撲，所以曝險窗口是啟動那一次；Adam 加的週期性輪詢（`71d27c1`）把它變成**每次輪詢**。缺陷是既有的，曝光度是新的——這句要講，與 template 對 null-translator（`--no-ai` 讓它變預設組態）、`m_allPathMap` race（週期刷新讓啟動期 race 變永久）的處理方式完全一致。

### 5.2 【列入 bug 頁】`57346f6` — OpenAI API key 被寫進 kernel log

- **baseline 驗證**：`28b8b13:src/ndt_core/intent_translator/LLMAgent.cpp:27` 取 `getenv("OPENAI_API_KEY")`，`:29` 就是 `SPDLOG_LOGGER_INFO(Logger::instance(), "api_key={}",apiKey);`——**INFO 是預設開啟的等級**，所以每次啟用 AI 的啟動都把祕密寫進 log。
- **第二個缺陷同樣 baseline**：那行 log（`:29`）**跑在 null 檢查之前**（`if (apiKey == nullptr)` 在 `:30`），所以變數沒設時先把 null `char*` 餵進 fmt，而本來要解釋這個設定錯誤的 ERROR（`:32`）**到不了**。
- **裁定：baseline 安全性缺陷，列入 Page 19（API 錯誤處理與資源類）或單獨在 Page 15–19 開一條。**
- **⚠️ 給簡報 agent 的分辨規則（重要）**：A1.3「不提 AI 協作」指的是**開發流程**（不講用什麼工具寫程式）。**Intent Translator 是產品自己的功能**，template Page 8／22 本來就講它、Page 15 也講 null-translator crash。**這條可以講，不違反 A1.3。** 若不特別寫明，簡報 agent 很可能因為看到 `OPENAI_API_KEY` 就整條砍掉。
- 非瑣碎：洩漏路徑的敘述特別好——「不是 gitignore 掉的 `.test_run/`，是人手動貼進 git 的 handoff 文件與 log 摘錄」。

### 5.3 【列入 bug 頁】`cbb504a`（＋`6dd0485`）— 丟掉 `boost::edge()` 的 found 旗標

- **baseline 驗證**：`28b8b13:.../TopologyAndFlowMonitor.cpp:857` 與 `:879`（`findReverseEdgeByAgentIpAndPortNoLock` `:844` 與其加鎖孿生 `:865`）**兩處逐字相同**：`auto reverseEdge = boost::edge(targetNode, sourceNode, *m_graph).first;` 然後 `return reverseEdge;`——取 `.first`、丟掉 `.second`，把 miss 包進一個 **engaged** 的 `std::optional`（optional 對「找不到」回答「有」）。
- **危害**：`FlowLinkUsageCollector` 在 sFlow 攝取路徑上透過那個 descriptor 寫入（`touchEdgeFlow`，baseline `:1187` 就是呼叫點），所以只要圖上只有單向鏈路，**per-edge 流量記帳就跑在一個無效 descriptor 上**。
- **無聲**：「丟掉錯誤旗標不是 race，所以 sanitizer 看不到，也不會有 log」——**完美符合 Page 14 的「全部無聲」主題**。
- `getLinkBandwidthBetweenSwitches` 是同一形狀的**不對稱**版本：正向在四行前查了 `.second`，反向沒查。
- **裁定：baseline，列入 Page 16（資料正確性類）。**

### 5.4 【列入 bug 頁】`5054249` — VLAN 欄位名不一致，一條規則永久毒化 flow-stats

- **baseline 驗證**：`28b8b13:src/ndt_core/collection/Classifier.cpp:771` = `if (match.contains("vlan_vid"))`，`:773` = `parseU64(match.at("vlan_id"))`。**guard 查 `vlan_vid`、實際讀 `vlan_id`**——而 `vlan_id` 這個欄位在 OpenFlow、在 Ryu 的輸出、在這個 repo 裡**都不存在**，所以任何真的帶 VLAN match 的 flow 都會讓 `.at()` 丟 `json::out_of_range`。
- **危害遠大於那個 throw**：那條規則**在之後每一次輪詢裡都還在**，所以同一台 switch 在同一條 flow 上死掉，永遠——它的 mark-and-sweep 再也不跑、**排在它後面的 switch 全部不再更新**、`get_switch_openflow_table_entries` 背後的 cache 再也不刷新。全部只呈現為 worker log 裡重複的一行。
- **裁定：baseline，列入 Page 16（資料正確性類）**，或作為 Page 17「只會加、不會刪」家族的近親（mark-and-sweep 停擺）。
- 非瑣碎：**這是一顆未引爆的地雷**——「今天沒有東西發出 `vlan_vid`，這正是它會以謎題而非回歸的形式出現的原因：**任何人安裝的第一條 VLAN 規則就會讓整個 fabric 的 flow-table 收集停止**」。對教授場合，「我修了一個還沒有人踩到的 bug，並說明為什麼它一定會被踩到」比修一個已知故障更有說服力。

### 5.5 【列入 bug 頁】`59dc5d3` — 十台 switch 共用同一個 smart plug

- **baseline 驗證**：`28b8b13:.../TopologyAndFlowMonitor.cpp:1958` 與 `:1972`（`get_static_topology_json` node 迴圈的**兩個分支**）都寫死 `{"smart_plug_ip", "172.25.166.135"}`。
- **危害**：依硬體拓撲那組值是 **s2** 的，而拓撲檔**一直都帶著逐台的真實指派**（十台分屬三個 PDU），載入器直接讀過去。**在真硬體上，信任這個端點的消費端會對所有十台去 power-cycle 同一個錯的插座。**
- **為什麼沒被發現**：kernel 自己的電源路徑從不用這些欄位（它讀 `switchSmartPlugTable`，從同一個檔另外建的），所以**沒有東西會去牴觸這個虛構**。
- **裁定：baseline，列入 Page 18（狀態破壞與誤報類）。**
- 非瑣碎：Page 18 現有四條裡有兩條是電源相關；這條把「**孿生對真硬體說謊**」的危害推到最高（會去動錯的實體插座）。

### 5.6 【列入 bug 頁】`ee7233b` — 歷史鏈路資料功能在**五個層次**同時是死的

- **baseline 驗證（兩層已逐字確認）**：
  - 層 1：`28b8b13:src/ndt_core/event_handling/ControllerAndOtherEventHandler.cpp:51` 收下 `std::shared_ptr<HistoricalDataManager> historicalDataManager` 參數，但初始化列 `:68` **結束在 `m_lockManager(std::move(lockManager))`**——成員從未被賦值；`:243` 再把那個 null 傳給每個 `HttpSession`。
  - 層 2：`28b8b13:src/main.cpp:142` `make_unique<HistoricalDataManager>` 與 `:172` `make_shared<HistoricalDataManager>`——**建了兩個不同的實例**；被 `start()`／`stop()` 的是前者，交給 event handler 的是後者。
- 另三層（`m_loggingEnabled` 寫了沒人讀；建構子用會丟例外的 `create_directories` 多載 → **一個建不出來的目錄會在啟動時殺掉 kernel**；寫入路徑每個 edge 開一個 ofstream 卻不檢查 `is_open()` → 在這台機器上輸出目錄是 root 所有、kernel 非特權執行，**每次 TESTBED 執行都往死掉的 stream 附加、什麼都沒寫、一行 log 都沒有**）出自 commit message；前兩層已足以定性。
- **裁定：baseline，列入 Page 15（層 4 是 crash）或 Page 18**。
- 非瑣碎：**「每一個破法單獨都足以讓功能失效，所以修好任何一個都不會有任何改善」**——這是「無聲」主題最極端的一個標本，也解釋了為什麼沒人發現：修一層的人會以為自己修錯了地方。**建議它進 Page 14（本節開場）當引例。**

### 5.7 【⚠️ 拆開裁定】`916d330` — 一半 baseline、一半 Adam 自己的

**這是最容易被簡報 agent 誤分類的一條**，所以要明確拆開：

- **baseline 的一半 → 進 bug 頁**：`28b8b13:.../IntentTranslator.cpp` 的 `POWEROFF_SWITCH`（`:231-241`）與 `POWERON_SWITCH`（`:242-251`）把 `setSwitchPowerState(...)` 當**裸述句**呼叫、丟掉回傳的 bool；而且 `if (deviceIpOpt.has_value())` **沒有 else**——拓撲解析不出來的裝置名**整個跳過呼叫**。兩者都掉進共用的 `return "ok"`（`:923`）。→ **baseline，列入 Page 18（誤報類）**。
- **Adam 自己的一半 → 不進 bug 頁**：同一個 commit 也修了 `INSTALL`／`MODIFY`／`DELETE_FLOW_ENTRY` 丟掉 **`OpResult`**。`OpResult` 是 Adam 在 Phase 2 自己加的機制 → **完全比照 A2 現有的 `8c25dbc` 排除條**（「補完自己的功能，放功能頁」）→ 放 Page 13。
- **一句很好的敘事**（可用於連接兩節）：這一層**就坐在 Phase 7 那條鏈的正上方，把那條鏈剛剛獲得的誠實整個丟掉**——helper 沒安裝的 P4 `powerOff` 對 LLM（因而對使用者）回答「ok」。

### 5.8 【建議：**不要**當成新 bug，併入既有頁】`3292653` — TESTBED 電源路徑回報 curl 的 exit code

- **baseline 驗證**：`28b8b13:.../DeviceConfigurationAndPowerManager.cpp:727` 建 `curl -s -X POST`（**無 `-f`**），`:739` `return rc == 0`。curl 對**任何**它成功收到的 HTTP 回應都 exit 0，所以 gateway 回 500／401／錯誤頁都被當成成功，`/ndt/set_switches_power_state` 對一台電源根本沒變的 switch 回 `{"<ip>": "Success"}`。→ 確為 baseline。
- **但 template Page 18 ④ 已經有一條 TESTBED 電源誤報**。建議**併為同一條的第二半**，不要當新 bug（否則 Page 18 會變成五條裡三條電源）。
- **⚠️ 動筆前要擇一的矛盾（觀察，未裁定）**：template Page 18 ④ 說它「一律把 graph 改成 caller *要求*的狀態」，而 `3292653` 的 message 說 `setPowerStateTestbed`「**從來沒碰過 graph**，所以 TESTBED 電源變更對孿生兩種情況都是隱形的」。兩句不能同時成立於同一個函式。可能是不同函式／不同路徑，**但簡報上只能出現一句**。→ **請 Adam 裁定**；在裁定前不要把兩句都放上去。
- 另有一個好註腳：誠實的實作**早就存在**，在一個三參數多載裡，**寫出來的那天零呼叫點、被刪掉的那天也是零呼叫點**——而且它的 URL 已經漂掉（不再送 `resource=outlet`），所以「直接把它接上去」會以只有真硬體才看得出來的方式出錯。

### 5.9 【不進 bug 頁，僅記錄】

- `44fa86e`（`m_ipStrToDpidMap` 用 `operator[]` 讀取造成插入）：**baseline 已驗證**——`28b8b13:.../IntentTranslator.cpp` 有九處 `m_ipStrToDpidMap[...]`（`:215/226/258/281/304/652/653/826/841`）。miss 會 default-construct 並插入 → **dpid 0**，把規則裝到一台不存在的 switch 上而不是回報錯誤名稱；kernel 以 `hardware_concurrency()` 條執行緒服務請求、這張 map 無鎖 → 兩個 miss 同時發生就是**並行 `std::map` 插入＝UB**。
  **→ 其實夠格進 Page 16（資料正確性）或 Page 20（併發）。** 之所以列在這裡，是因為 Page 20 只有兩條、加它會變三條，**由 Adam 決定要不要擴。** 若要用，正確的一句是：「正確寫法**五十行之上就有**（`DISABLE_SWITCH`／`ENABLE_SWITCH`，還附了解釋這件事的註解）——所以這不是不知道，是複製貼上第六次時沒帶上。」
- `42d86cd`／`7f738e6`／`900d60b`／`d505b9d`／`801407f`／`e7c308d`／`2609adc`／`ac07b0f`／`1145372`／`4c56ff7`／`6dd0485`：尚未逐條對 baseline 驗證。其中**打在 proxy／P4 側的一律排除**（Adam 自己的碼）；打在 kernel 既有檔案的需要 `git show 28b8b13:` 逐條驗。**若 Adam 要擴充第 2 節再驗**——本報告不猜。

---

## 6. 給 Adam 的三句話

1. **差距是 69 個 commit 不是十幾個**，所以 template 該補的比預期多：**兩頁新的**（Phase 7 電源管理、第二輪 55 條審查）＋ **B 節四個數字全換** ＋ **Page 33 的未完成清單三格全錯**。
2. **第 2 節（baseline bug）可以擴充**：`f21d7a0`／`57346f6`／`cbb504a`／`5054249`／`59dc5d3`／`ee7233b` 六條**已逐條對 `28b8b13` 原文驗證為 baseline**，`916d330` 要拆一半。它們**全部符合 Page 14「無聲」的主題**，所以是加強敘事而不是打亂它。要不要把 Page 14 的「11 個」改成新的數字，**請你裁定**（我沒有重新盤點舊的 11 條與新條目有無重疊）。
3. **Page 28 現在填得起來**（16.63s 自癒／hitless 復原／38-40／`1 6 10 7 4`），但 **repo 外的素材位置要寫進 D 節**，否則簡報 agent 找不到會編。**readopt 相關的一切先不要上台**。
