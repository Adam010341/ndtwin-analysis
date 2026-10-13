# 916 → 930：修掉了什麼（Found, then fixed — delta）

**figure worker 起草 2026-09-27 15:5x UTC；16:1x、17:0x UTC 依 integrator 轉來的更正與 judge-SLIDES930（F-3、F-16、F-18、F-20）改訂；Adam 定稿。**
**2026-09-28 13:2x UTC 審查中加一條（coordinator）：`spawn helpers`（`fix/spawn-helper-subshell-0928` @ `dfdb2121`，§4.3）；§0、§1、§4、§8、§10 跟著改；快照、merge 與公開狀態不變。**
**2026-09-28 08:4x UTC 重新釘住（coordinator：在審那一項的 PR #15 已 squash 進 main，中性磚規則解除；之後 PR #17 也併入，兩個 main 為 `eef173a9`）：快照由 `85bec430` 移到 `3368412d`；那一項成為 §2.2 的一般修法列；TERM trap 併入、移到 §2.4；新進審查一條（§4.2）；§0、§1、§6–§10 跟著改。**
**2026-09-28 08:2x UTC 判官修正輪：§0 的 audit-raw 清單逐檔重核、§1 表與 §4、§8、§10 的排版、在審那一項改用單一說法；內容數字不變。**
**2026-09-28 06:2x UTC 更新（coordinator 的 refresh 請求，待判官審）：快照由 `fed37cff` 移到 `85bec430`；§0、§1、§2、§4、§6–§10 跟著改，§9 多一輪未認證查核。**
這是 930 那一頁「Found, then fixed」的**資料正本**；圖 `figures/fixed-since-916/fig_f1_fixed_since_916` 由 `make_fixed_since_916.py`
**直接解析本檔 §1–§4、§6、§7、§9.1 的表**畫出（改這裡、重跑腳本，圖跟著變；腳本另外用 git 對帳每一顆 sha 與日期，對不上就拒畫）。

[Co-developed with claude code -- Adam]

---

## 0. 口徑（先讀）

- **本檔所有日期與時間都是 UTC**（git 日期以 `TZ=UTC git log --date=format-local:…` 取；腳本也這樣對帳）。
- **切點**：916 deck 的最後狀態＝trunk `70615ec5`（09-12 13:02）。之後 trunk 第一親鏈上到 09-17 09:52 之前**沒有任何 commit**，
  所以「09-16 之後」＝`TZ=UTC git log --first-parent --since=2026-09-16` 從 09-17 起的全部。
- **快照**：本機 trunk `3368412d`（2026-09-28 07:45:54）——**清單截止於 trunk `3368412d`**（09-27 的版本截止於 `fed37cff`，09-28 06:2x 的截止於 `85bec430`；2026-09-28 08:4x UTC 重新釘住）。
  trunk 之後若再動，**快照之後的 merge 不在本檔**；腳本用 `3368412d` 取 merge 清單，不用會動的 `trunk` 名字。
  - `TZ=UTC git log --first-parent --merges --since=2026-09-16 3368412d` ＝ **66** 個 merge（`85bec430` 時 64 個，之後 2 個：`fc25112e`、`3368412d`）。
  - `git log --first-parent --no-merges --since=2026-09-16 3368412d` ＝ **84** 顆直接 commit（`85bec430..3368412d` 多兩顆：`08f67b7a` CLAUDE.md、`c8433963` GAP-2b，都不是修法；修法仍只有 §5 的 4 顆）。
  - 未併分支：`git for-each-ref --no-merged=3368412d refs/heads refs/remotes`，tip 日期 ≥ 09-16 的 16 個 ref：3 個是 `audit-raw` 的本機／tracking ref、2 個是 `lab/main`、`p4/main`（`main` 的 tracking ref，squash commit 本來就不在 trunk 裡，見 §8），不算；
    其餘 11 條逐條分類在 §4、§6 末、§7 末；**分支 tip 取 2026-09-28 08:3x UTC 那一刻**（本機 git，唯讀）。
    13:2x 加列一條：`fix/spawn-helper-subshell-0928`（tip `dfdb2121` 10:57，§4.3）⇒ 分類的共 12 條；其他 ref 沒有重掃（13:2x 本機所見：residue 那條的 tip 已是 `571fa6fd`、另有 `backup/residue-live-pid-wait-0928-pre-fold`；§4.2 仍寫 08:3x 的 tip）。
- **單位＝一個 merge 或一條未併分支**，一列一格磚。一個 merge 修了好幾個缺陷（如 `7242e127` 的五個）仍是一列；
  層別取「缺陷所在的產線碼」佔多數的那層（`git diff --numstat <merge>^1 <merge>`，不算測試檔與 `doc/audit/**/*.md`）。
- **FIX 與 FEATURE 的分法**：merge 訊息寫出一個**已經在 trunk 上、跑過（live、CI 或產出過結果）而錯了**的東西，而 merge 修它 ⇒ FIX。
  新能力、或對**還沒跑過**的新儀器做的審查輪次 ⇒ FEATURE（§6），即使那些輪次也修了自己的錯。
  依任務單，protobuf 5（`5dc7fc9a`，修 CVE-2025-4565／CVE-2026-0994）歸 FEATURE。
- **三種狀態，不可混寫**（圖上也是三條分開的帶）：
  - ✅ **併入 trunk・公開**＝sha 是**公開** trunk head 的祖先。公開 head 只用未認證 HTTPS 取得（§9）：
    2026-09-28 08:38 UTC 兩個 P4 本體的 `trunk` 都是 `3368412d`（＝本檔快照），兩個 repo 都 `"private": false`（§9 第 32–36 列）。
    （之前的版本：09-27 16:04:56 與 17:02:39 兩個公開 `trunk` 都是 `fed37cff`，15:46 那一輪還是 `3d740be0`；09-28 06:20 是 `85bec430`。）
  - 🔧 **併入本機 trunk・未公開**＝是本機快照的祖先、不是公開 trunk head 的祖先（判定時 0 列）。
  - 🕓 **審查中**＝分支 tip 不是 `3368412d` 的祖先；附分支名＋tip。判定時 2 條，兩條的 branch 都**不在**任何公開 repo 的分支清單裡（residue clock：§9 第 32–33 列；spawn helpers：13:20 未認證 `git ls-remote`，`K/scratch/overnight-2026-09-05/logs/slides930/net-spawnhelpers-20260928T1320Z.log`）。


- **本機 tracking ref 一律不當公開證據**（本機 `lab/trunk` 停在 `fc25112e`、`p4/trunk` 停在 `18c83aba`，公開的其實是 `3368412d`——正好示範它會說謊）。
- **證據欄**：`變異 N/0`＝變異閘 N 個變異 0 存活；`紅先行`＝修法前親眼看過紅；判官＝merge 訊息寫的判決＋判決檔（有的話，附判決行號）。
  `live`＝有一次 live run 的 raw 路徑，且那次 run 的 code sha 包含這個 merge；**沒寫 live 就是沒有**。
  縮寫：`R/`＝`doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/`；`06 <時戳>`＝`R/<時戳>_06_thirteen/00_table.tsv`；
  `J25/`、`J26/`＝`scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0925/`、`…/intake-0926/`；
  `P3-*-JUDGE.md`、`P2-F-JUDGE.md`＝`scratch/overnight-2026-09-05/hunt-0911/fix/`。
- 🔴 **`R/`、`scratch/` 在本機 checkout 不進版控**。本檔引用的檔，逐檔以 `git cat-file -e <commit>:<path>` 對公開 `audit-raw` **`797c34ab`**（17:02:39 兩個 P4 本體的 `audit-raw` 都是它，§9 第 19–20 列）與本機 audit-raw 最新的 `5cf0364c`（`797c34ab` 的後代）核對（2026-09-28 08:21 UTC，`K/scratch/overnight-2026-09-05/logs/slides930/audit-raw-check-20260928T0821Z.log`；重新釘住後加兩份 compare 記錄，最後一次的 log 名在 README §11）：
  **在 `797c34ab`（也在 `5cf0364c`）**——判決檔：`J25/judge-REQ-55cebe6c-7cc50b42.md`、`J25/judge-OVS-r3-98442add.md`；`J26/` 根目錄的 `judge-{HBNOVENV,HBR7,HBR7b,R2B,LP1C,R3,SGE,PSTUB,STALE,NOTES,NDTSERVE}-*.md`（11 份）；`J26/aeg/judge-AEG-ebe17f7c.md`、`J26/queued/judge-QUEUED-bbb9fd41.md`、`J26/sudo2/judge-SUDOPROBE-d57f90f1.md`、`J26/sudoprobe/`；`orchestrator-0919/judge-E-r10.md`。
  非判決檔：`gates-0910/mutate_ndt_ovs_claim.ndtovs-98442add.log`、`orchestrator-0918/rerun-E-071b2ada.log`、`orchestrator-0924/rerun-C-611a08d3.*.log`（4 份）、`rerun-D-bf349b64.*.log`（2 份）；live run `R/2026-09-18T*`、`2026-09-19T144328Z_06`、`2026-09-24T185505Z_06`、`2026-09-26T*`、第五次 campaign `raw/2026-09-19T115737Z_full`。
  **兩個都沒有（只在本機工作樹，未提交的觀測）**——判決檔：`J26/aeg/judge-AEG-f7e2a128.md`、`J26/cicxx/judge-CICXX-a956fd78.md`、`J26/cil1/judge-CIL1-e9c004f3.md`、`J26/n7/judge-N7-*.md`（2 份）、`J26/qn1/judge-QN1-85befc7d.md`（`J26/qn1/` 是一份判決檔加一份 `INTAKE.md`）、`J26/sudo2/judge-SUDOPROBE-995eeb69.md`、`hunt-0911/fix/` 的 `P3-*-JUDGE.md`（5 份）與 `P2-F-JUDGE.md`。
  非判決檔：`J26/ci-compare-pr15.txt`、`J26/ci-compare-pr16.txt`、`J26/aeg/rerun2-summary.d94b5547.txt`、`J26/cil1/rerun-cil1-summary.txt`、`J26/n7/rerun3-n7-summary.txt`、`J26/sudo2/rerun-sudo6583-summary.txt`、`J26/qn1/INTAKE.md`、`ci-cxx-0927/m1_formattime_red_green.log`、`ndt-serve-claim-note-0927/before-long.log`；live run `R/2026-09-19T052251Z_05…`。
  **2026-09-27 UTC 更新**：`06 2026-09-19T052518Z／063235Z／083257Z` 三輪與它們引用的 09-19 exercise 報告已進 audit-raw **`5cf0364c`**（08:21 的核對同：三個 run 目錄在 `5cf0364c`、不在 `797c34ab`）（`797c34ab` 的後代；
  coordinator 以未認證 `git ls-remote https://github.com/{ndtwin-lab,Adam010341}/NDTwin-Kernel-P4.git refs/heads/audit-raw` 核過兩邊公開；
  integrator 本機比對：三個 run 目錄各 27 檔、arm report 403 檔，blob 全同）。`052251Z_05` 仍不在。
- **live 的 code sha** 取自各 run 的 `ndt status`「code <sha>」行；那是 checkout 的 sha，**不是** kernel binary 的 sha。
  **每一次當證據的 live run 都跑在有未提交檔案的 checkout 上**，數目就在同一行（例：`code 365c60e1 +29 file(s) with uncommitted changes`；
  09-27 的 T06 是 +95，`doc/audit/2026-09-04_p4-tutorial-exercise-prep/runs/2026-09-27T074826Z_basic_solution_ndtwin.md` 的 code 5dc7fc9a 那一行，audit-raw `797c34ab`）；
  下面證據欄一律寫成「code <sha> +N」。

## 1. 數字（圖上的值標籤全部從這張表與 §2–§4 的列數來，腳本會互相對帳）

| 量 | 值 | 怎麼算的 |
|---|---|---|
| ✅ 併入 trunk・公開 | **39** | §2 的列數；每顆 sha 是公開 trunk `3368412d` 的祖先 |
| 🔧 併入本機 trunk・未公開 | **0** | §3 |
| 層：kernel C++ | **2** | §2.1（2） |
| 層：proxy | **6** | §2.2（6） |
| 層：ndt tool | **5** | §2.3（4）＋§4.2（1） |
| 層：tests-instruments | **28** | §2.4（27）＋§4.3（1） |
| 層：docs | **0** | 本窗沒有以文件為主體的修法 merge；文件修正都是直接 commit（§5 末） |
| FEATURE merge（不畫） | 21 | §6 |
| 其他 merge（README 同步、報告；不畫） | 6 | §7 |
| 直接落 trunk 的修法 commit（不畫） | 4 | §5 |
| 🕓 審查中（分支） | **2** | §4；tip 不在 `3368412d` 裡 |

對帳：39＋0（FIX merge）＋21＋6＝**66**＝快照的 merge 總數；腳本逐顆比對，不是只比總數。（`85bec430` 版：37／0／2，64＝37＋21＋6；09-27 版：32／0／4，58＝32＋20＋6。這次動的：在審的兩條併入並公開（`fc25112e` → §2.2、`3368412d` → §2.4）；新進審查一條（§4.2）。13:2x 再進審查一條（§4.3 `spawn helpers`）：審查中 1 → 2、層 tests-instruments 27 → 28；分支不是 merge，66 不變。）

## 2. ✅ 併入 trunk・公開（39）

### 2.1 kernel C++（2）

| 代號 | 一句話（缺陷 → 修法） | 進 trunk 線 | 證據 |
|---|---|---|---|
| P3-A link bytes | sFlow 樣本先看 ethertype／協定才記鏈路位元組 ⇒ ARP、LLDP、IPv6、其他 IP 協定不計入 link usage，非首片段還中止整個 datagram；egress-only 樣本記到反向邊 → 先記帳再辨識、egress-only 進 egress bank；非 IPv4 身分進 1024 筆有界側表（IPv4 數字不變） | `2a551df7` 09-19 | fable 判官 3 輪（`P3-A-JUDGE.md`）；變異 mutate_flowkey_families 8/0、gtest 1366/1366、seen-red R1–R6；live：`R/2026-09-19T052251Z_05_link_usage_generic`（code 2a551df7 +45；**raw 未記 kernel binary sha**） |
| clang/TSan | `DeviceConfigurationAndPowerManager` 的解構子不是 virtual（clang CI 在 `-Werror` 下失敗）；`utils::formatTime` 用整個 process 共用 buffer 的 `localtime()`（TSan 在 TopK locking 測試抓到 race）→ virtual 解構子、`localtime_r` | `18c83aba` 09-27 | 判官 MERGE（`J26/cicxx/judge-CICXX-a956fd78.md:3`）；紅先行 `scratch/…/logs/ci-cxx-0927/m1_formattime_red_green.log`、`m2_tsan_mechanism.log`；CI：PR #9 兩個 run 的 clang、TSan 第一次 success（公開 API `figures/engineering/_net/jobs_36343017674.json`、`jobs_36343021331.json`）；09-27 版列在 §4.1 |

### 2.2 proxy（6）

| 代號 | 一句話（缺陷 → 修法） | 進 trunk 線 | 證據 |
|---|---|---|---|
| P1-D bridge | lab 實際啟動的是 `ntg_bmv2_topo.py`，它不讀 app package（package 下 0/4 switches、tmux pane 一起消失）→ `p4_testbed_topo.bring_up()` 成為兩個入口共用的唯一 bring-up，topo log 落檔 | `d4187307` 09-18 | 變異 mutate_app_package 35/0、mutate_ndt_app_package 17/0；merge 訊息未記判官；live：`R/2026-09-18T095025Z_02_app_basic`（code 365c60e1 +29）pingall 12/12 零丟包 |
| P1-D eth0 | package host 的預設介面叫 `h1-eth0`，exercise 的 `dev eth0` 指令無聲失敗（`host.cmd()` 輸出被丟）⇒ 每個 ping 都 Network unreachable → 先改名 eth0、印出並計數每個指令的回應；verify_p4 用模型的 switch 數 | `8e62b423` 09-18 | 變異 38/0、18/0；merge 訊息未記判官；live：同上 run，12/12 |
| P3-B teardown | teardown 沒有跑完、留下過期紀錄 ⇒ `ndt down` exit 1 → teardown 一定跑到底 | `e8a8400e` 09-19 | 變異 28/0；`P3-B-JUDGE.md` 補記；live：06 `2026-09-19T052518Z`（code dfb9d0d7 +47）24/26 臂「LAB NOT RETURNED」→ 06 `2026-09-19T063235Z`（code cbc968d8 +54）0 臂 |
| P3-C exact[1] | proxy 拒收寫成單元素 list 的 EXACT 值（upstream tutorials 的 runtime JSON 就這樣寫）⇒ basic_tunnel solution 每台 6 條拒 3 條 → 單元素解包，二元素仍拒 | `7d6c88a2` 09-19 | 紅先行 10/14 格；變異 mutate_table_entry 41/0；`P3-C-JUDGE.md` 補記；live：basic_tunnel/solution 在 06 `063235Z` ERROR → 06 `2026-09-19T083257Z` PASS 4/4（該臂 code 7242e127 +60） |
| proxy reqs | `p4_proxy/requirements.txt` 寫的不是 proxy 與測試實際在跑的 venv → 對齊（p4runtime 1.5.0、grpcio 1.82.1、starlette 直接 pin；protobuf 仍 3.20.3） | `a4c951a8` 09-25 | opus 判官 MERGE AFTER FIXES（`J25/judge-REQ-55cebe6c-7cc50b42.md`）；兩個 venv 下 p4_proxy 1557 OK；**無變異閘**（依賴清單） |
| rulings KJL | cleanup 路徑的權限缺陷，審查抓到 → 已修（#15） | `fc25112e` 09-28 | 判官四輪，最後一輪 MERGE；main：PR #15 squash `299c9e23`（09-28 08:28Z）；層＝proxy（產線碼 534 行在 `p4_proxy/`、8 行在 `ndt`） |

### 2.3 ndt tool（4）

| 代號 | 一句話（缺陷 → 修法） | 進 trunk 線 | 證據 |
|---|---|---|---|
| P2-D no-LLDP | `ndt up p4 --app` 在跑 package 自己 pipeline 的 fabric 上，等 12 條 proxy 永遠不會發現的路徑（停在 4/12），先燒掉 stack.sh 的 300 s → verify_p4 讀 `control_plane.skipped`、改以每台的 table_entries 為 gate；proxy 說不送 LLDP 時 stack.sh 不等 | `fa83c170` 09-18 | fable 判官 2 輪；變異 mutate_ndt_app_package 37/0、mutate_stack_await_convergence 9/0；live：`R/2026-09-18T132506Z_02_app_basic`（code fa83c170 +34）verify_p4「up. ready」 |
| P2F N-up race | external control plane 下「N up」量到的是兩層競態（同一支 03 一次 3 up、一次 0 up）→ up／enabled 降為 reading，gate 改為每個宣告 dpid 的 probe 有回答 | `8eddb0e8` 09-18 | fable 判官（`P2-F-JUDGE.md`，on 49f368f6）；變異 49/0、mutate_live_p1_common 11/0；live：`R/2026-09-18T161610Z_03_app_p4runtime`（code 8eddb0e8 +40）controller 寫過的 s1/s2 up、s3 down |
| OVS claim | OVS 上的 `ndt up` 不看別人的 claim、也不看進行中的量測；過期的行程紀錄沒人標 → OVS 同 P4 回 rc 5，`--force` 每次留紀錄；過期紀錄先記下視窗才清掉 | `68ace017` 09-25 | opus 判官 3 輪、MERGE on 98442add（`J25/judge-OVS-r3-98442add.md`）；變異 mutate_ndt_ovs_claim 39/0（`scratch/…/logs/gates-0910/mutate_ndt_ovs_claim.ndtovs-98442add.log`） |
| sudo unknown | `ndt_sudo_probe` 把不認得的 `sudo:` stderr（requiretty、PAM、secure_path）讀成「已授權」⇒ `ndt status` 印出 live grant → 已知的拒絕＝拒絕、不認得的＝「無法判定」，`ndt status --check` 兩者都失敗 | `f253ed08` 09-28 | opus 判官 MAF on 103f94f0、d57f90f1、995eeb69（`J26/sudoprobe/`、`J26/sudo2/judge-SUDOPROBE-*.md:3`；最後一輪只剩文件修正）；orchestrator 重跑 6583c089：mutate_ndt_sudo_surface 31/0、suite 55/0（`J26/sudo2/rerun-sudo6583-summary.txt`）；CI：PR #13 兩個 run 四個 job 全 success（`_net/jobs_36373185198.json`、`jobs_36373189008.json`）；09-27 版列在 §4.2 |

### 2.4 tests-instruments（27）

| 代號 | 一句話（缺陷 → 修法） | 進 trunk 線 | 證據 |
|---|---|---|---|
| P2-E recv -u | driver 結束 receive.py 時，它寫檔的整塊緩衝不會沖出 ⇒ link_monitor 兩臂 0-byte log → 以 `-u` 啟動 | `8071cb3d` 09-18 | 紅先行 1 格；變異 mutate_drive_exercise 43/0（`scratch/…/logs/orchestrator-0918/rerun-E-071b2ada.log`）；無判官輪；live：06 `063235Z` link_monitor 兩臂 PASS 4/4（原缺陷在 tutorials harness 上看到，那一側的重跑 raw 沒找到） |
| P3-D live ×5 | 第一次 live 13/13 找到五個儀器缺陷（`ndt down` 把一筆遺留誤報成殘留、finish() 在 set -e 下半途結束、qos 通用格門檻、ICMP error 內嵌 header 誤讀、scapy 巢狀前綴）→ 逐一修 | `7242e127` 09-19 | 每項 fixture 紅→綠；變異 90/0、33/0、75/0；`P3-D-JUDGE.md` 補記；live：06 `063235Z` → 06 `083257Z`：qos skeleton 1/3→3/3、mri skeleton 2/4→4/4、mri solution 4/5→5/5（code 7242e127／1ea07e7b +60） |
| P3-E driver | 三組量測第一次真跑就死：`ndt verify_p4` 不是子指令、`set -u` 的 local hazard、teardown 被自己宣告的 measuring= 拒（rc 5）→ gate 改讀 `ndt up` 印的 [3/3]、down 之前先撤 measuring | `0389ef55` 09-19 | 紅先行 offline 26/25、40/11；mutate_analyse 25/0；`P3-E-JUDGE.md`；live：第五次 campaign `doc/audit/2026-09-19_telemetry-three-groups/raw/2026-09-19T115737Z_full` 跑完 |
| P3-E argv | bmv2 啟動紀錄裡的 argv 是一個字串，arm 逐字元迭代 ⇒ 每個 arm 都 INVALID → `shlex.split` | `7d0ef22a` 09-19 | M-E26 抓到、0 存活；`P3-E-JUDGE.md`；live：同上 campaign |
| P3-D r31/33 | controller 在 G1 量之前就停了 ⇒ 量到它的缺席卻算在 fabric 頭上；rc 4（視窗太長）被記成 twin 缺陷 → controller 活到 G1 量完、答案四值 | `f3b6d09c` 09-19 | 紅：pre-33 driver 6 格 5 紅；變異 mutate_drive_exercise 97/0、mutate_live_p1_common 40/0；live：06 `2026-09-19T144328Z`（code f3b6d09c +61）26/26 如預期 |
| P3-E labels | 分析把 PREREG 按組登記的假設逐格貼標 → 照 PREREG 登記的單位下判，沒有登記容差的判「未決」 | `305b9938` 09-24 | opus 判官 round 10 MERGE AFTER FIXES（`scratch/…/logs/orchestrator-0919/judge-E-r10.md`）；mutate_analyse 48/0、offline 78/0 |
| CPU window | 逐階 CPU 視窗吞進更高階的確認 rep ⇒ 11 個 bmv2 逐階判決翻 2 個 → climb-only 主讀數（Adam 裁，非 PREREG 登記）＋勘誤表保留舊值 | `d39959ba` 09-24 | opus 判官 HOLDS WITH CORRECTIONS；mutate_analyse 57/0、offline 78/0（`scratch/…/orchestrator-0924/rerun-C-611a08d3.*.log`） |
| tutorials ctrl | tutorials fabric 上 flowcache／p4runtime 的 solution 臂，controller 在 import 就死 → 只對該臂加 PYTHONPATH | `9d63af2e` 09-24 | opus 判官 MERGE AFTER FIXES → r2；mutate_drive_exercise 106/0（`scratch/…/orchestrator-0924/rerun-D-bf349b64.*.log`） |
| ecn probes | tutorials ecn solution 臂的標記檢查只有 2–4 個 probe（檢定力不足）→ 自送 60-probe train | `0c96c1d0` 09-24 | orchestrator 逐 hunk 讀，無判官輪；unit 178、變異 125/0；live：06 `2026-09-24T185505Z`（code 0c96c1d0 +79）26/26，ecn/solution PASS 4/4 |
| HB no-venv | heartbeat 測試的常數 pin 在沒有 proxy venv 的 GitHub CI 上紅（L1 14→15 組）→ 沒有 venv 時退回 PATH 上的 python3 | `dd7e2fcf` 09-25 | opus 判官 MERGE on c4cb36b9（`J26/judge-HBNOVENV-c4cb36b9.md`）；閘門新增 pin-no-path-fallback；當時真 CI 未觀測 |
| spike r7 | spike 第一次 live：`ndt down` 兩次被 ndt 自己的 measuring 守衛拒（rc 5），spike 仍 release ⇒ fabric 無人 claim 約 34 s → down 前先撤 measuring，down 失敗就保留 claim | `580767a8` 09-26 | fable 判官 MERGE AFTER FIXES a77b8fe2 → MERGE 96abb9b0（`J26/judge-HBR7-a77b8fe2.md`、`judge-HBR7b-96abb9b0.md`）；31 列 oldcode；live：`doc/audit/2026-09-25_p4-heartbeat/P4-HB-SPIKE.md` §0 run 2 PASS（log2:222；raw 在 audit-raw `1fafa3a0`） |
| serve anchors | segment W 讓 `ndt` 多 124 行 ⇒ ndt serve 釘住的 11 個行號 anchor 全部移位，公開 CI 的 L1 14→15 組 → 逐一重新 anchor | `329dc555` 09-26 | opus 判官 MERGE on 60194b09（判決檔沒找到）；變異 91/0 |
| 08 H5 sampler | live H5 什麼都沒記：sampler 內嵌 Python 的 f-string 有反斜線（SyntaxError）、stderr 丟進 /dev/null → quoted heredoc、stderr 落檔、起不來就 FAIL | `0925d9fc` 09-26 | 紅先行 c6c49215；變異 189/0；opus 判官 MERGE on f4f43a32；live：`R/2026-09-26T153259Z_08_heartbeat`（code cafd518a +86）沒有 50_samples.tsv → `R/2026-09-26T172912Z_08_heartbeat`（code 3f8c2abf +89）1646 行、stderr 0 byte |
| 07 HB links | heartbeat 跑著時，07 的 L1 仍照舊形狀判 links → links_heard 恰為模型的 8 個方向、來源是 heartbeat | `3f8c2abf` 09-26 | opus 判官 MERGE on e012a5a7；變異 167/0；07 在 b2eeb71d 上 live 跑過（`R/2026-09-26T202055Z_07_roles_basic`，code b2eeb71d +92），但 raw 沒有 links_heard 的捕獲 ⇒ **不記 live** |
| HB r2 | 判官 r2 的 notes：08 的 sampler 啟動後才死仍會 PASS、「HEARD」不是年齡、st_l6 沒跑到 live 呼叫 → FAIL／age／移到 dispatch 前 | `b2eeb71d` 09-26 | opus 判官 MERGE on 4f661e31（`J26/judge-R2B-4f661e31.md`）；變異 195/0、172/0、93/0 |
| 5e no-lab | 離線 suite `test_live_p1_common` 的 5e 格在 live 06 臂的 host 之間真的跑了 2 Mbit/s iperf（09-26 17:55）→ 假 fabric，sudo／mnexec／iperf 換成記錄並拒絕的 stub | `3db3b9a8` 09-26 | 紅先行（trunk 版做了 4 次 sudo mnexec iperf 還印 0 failed）；opus 判官 MAF c03130fe → MERGE be2ad2d2（`J26/judge-LP1C-c03130fe.md`）；變異 45/0 |
| HB r3 | 08 的 mutant tree 裡有 lab-state knob（mutant 寫得到 lab 狀態）；07 的 live L1 poll 讀呼叫者的 L1_POLL_S → ltree 只連 proxy_agent＋venv，poll 改為參數 | `8746c1bc` 09-26 | 紅先行 c0cef392、a435d24e；opus 判官 MERGE on c22d1300（`J26/judge-R3-c22d1300.md`）；變異 195/0、174/0 |
| guard env | `test_build_guard` 繼承外層 guard 的 JOBS=1 等變數 ⇒ 在閘門環境下 15 格紅（紅的是呼叫者的設定，不是碼）→ unset 九個變數 | `c34a643a` 09-26 | 紅 37/15；opus 判官 MERGE on d271f5b8（`J26/judge-SGE-d271f5b8.md`）；mutate_build_guard 14/0 |
| probe stubs | 六個 suite 經真的 `sudo -n` 送唯讀 lab probe（結果隨 live lab 變）→ 每個 suite 自帶 sudo stub：記錄、以 sudo 原話拒絕、收尾檢查 | `46a18285` 09-27 | 紅先行 sample_rate 4 格；opus 判官 MAF 356d4e4e → MERGE f9c59a44（`J26/judge-PSTUB-356d4e4e.md`）；mutate_probe_stubs 10/0 |
| stale suites | 三個 suite 在每個環境與 CI L1 都紅，其中 not_tee 是為錯的理由通過 → 重新定位、hermetic fixture、scorer 走 lane 自己的 summary | `b005bf50` 09-27 | trunk 紅 6/2/12；opus 判官 MAF d2a9d641 → MERGE 1d5180ce（`J26/judge-STALE-d2a9d641.md`）；閘 9/0、20/0 |
| NOTEs r3 | 07 self-test 的 poll 在結束後仍留 2 個行程；build_guard 的裸呼叫沒有自己的 lock、預設等 3600 s → 虛擬時鐘、獨立 lock | `d9308f61` 09-27 | opus 判官 MERGE on 16069d1a（`J26/judge-NOTES-16069d1a.md`）；mutate_build_guard 17/0、roles_binding 177/0、heartbeat_w 195/0 |
| NOTEs queued | `test_l1_shell_scoring` 的 group C 在刪掉 suite 的 summary 呼叫後仍綠（NOTE A）等 → 經「印 summary 的函式」讀 green path | `4ff4eee8` 09-27 | NOTE A 紅臂親見；opus 判官 MERGE on bbb9fd41（`J26/queued/judge-QUEUED-bbb9fd41.md`）；mutate_l1_shell_scoring 36/36、probe_stubs 14/0、sudo_surface 14/0 |
| claim-note tmp | `test_claim_note_reaches_ndt_as_one_argv_element` 用兩個絕對 temp 路徑組 note，TMPDIR 約 55 字元以上就超過 200 字上限、server 回 400 ⇒ 這格什麼都沒測就紅 → note 改用相對路徑、長度固定 | `fed37cff` 09-27 | 紅先行 105 字元紅／21 字元綠（`scratch/…/logs/ndt-serve-claim-note-0927/before-long.log` rc=1 → `after-long.log` OK，未進 audit-raw）；mutate_ndt_serve 150/0（同目錄 `gate.log`）；merge 訊息未記判官 |
| rulings AEG | A：H1 超過嚴格 20 s 由 FAIL 改為揭露 NOTE（Adam 裁，是判準改變不是修缺陷）；E：heartbeat 驅動 watchdog 時 switch_state 仍把 `link_watchdog` 列為 skipped；G：live-p1 預設 `NDT_OWNER=live-p1`，claim 看不出是誰 → 無預設 owner、拒跑 | `149c8234` 09-27 | opus 判官 MAF on ebe17f7c → MERGE on f7e2a128（`J26/aeg/judge-AEG-ebe17f7c.md:3`、`judge-AEG-f7e2a128.md:3`）；orchestrator 重跑 d94b5547：test_live_p1_common 191/0、thirteen 42/0、07／08 self-test PASS、anchors 122/122（`J26/aeg/rerun2-summary.d94b5547.txt`）；09-27 版列在 §4.3；**不記 live**（本窗沒有含它的 live run） |
| CI L1 lane | GitHub 的 hosted runner 上，Python L1 lane 把「這台機器沒有 lab 安裝」讀成 12 個問題組（CI 一直紅，紅的是環境不是碼）→ 檔案自己宣告的需求（`NDTWIN_L1_NEEDS`）只在 hosted runner 上、而且只在真的缺時才免；CI 抓完整歷史、建 `p4_proxy/venv` | `9ef10250` 09-28 | opus 判官 MERGE（`J26/cil1/judge-CIL1-e9c004f3.md:3`）；orchestrator 重跑：test_l1_shell_scoring 147/0 等（`J26/cil1/rerun-cil1-summary.txt`）；CI：PR #11 兩個 run 的 L1 由 12 組變 1 組（`I/ci-compare-pr11.txt:2`；raw `S/ci-raw/ci-36361624221-gcc.*.raw.log`） |
| round.env | 兩個量測輪的 `round.env` 把 `KERNEL_DIR` 寫死成主 checkout ⇒ 在 worktree 裡跑會讀到另一棵樹 → 由檔案自己的位置推 `KERNEL_DIR`，拒絕非 bash、無檔與相對路徑的 source；live 輪在 `KERNEL_DIR` 不是 lab helper 那棵樹時先拒絕、不寫任何東西 | `8d622ea4` 09-28 | opus 判官 MAF on 7b4a48b9、261b2d9d（`J26/n7/judge-N7-*.md:3`）；第 3 輪由 orchestrator 讀 diff 後接受，未再送判官；重跑 67e9963d：mutate_round_env_kernel_dir 24/0、mutate_live_round_lab_tree 19/0（`J26/n7/rerun3-n7-summary.txt`）；CI：這個 merge 的 trunk run 是第一次四個 job 全 success（`_net/jobs_36365963530.json`，09-28 01:26Z 起跑） |
| TERM trap | 三個把假的外部指令放在 PATH 上暫存目錄的 suite，收到 INT／TERM 時刪掉那個目錄後又返回、繼續跑，之後的呼叫會落到 PATH 上真的指令 → handler 改成只結束（rc 130／143） | `3368412d` 09-28 | opus 判官 MERGE on 85befc7d（`J26/qn1/judge-QN1-85befc7d.md:3`）；紅先行：base 在 stub 被刪後繼續跑、HEAD 停下（同檔）；main：PR #16 squash `9a74408b`（09-28 08:19Z），CI 四個 job 全綠（`J26/ci-compare-pr16.txt:1`） |

找到缺陷的是誰（不上圖）：live run（P2-E、P3-B、P3-C、P3-D live ×5、P3-E driver／argv、spike r7、08 H5、5e no-lab）、CI（HB no-venv、serve anchors、stale suites、clang/TSan、CI L1 lane）、
判官或閘門（P3-E labels、CPU window、HB r2、HB r3、guard env、NOTEs r3、NOTEs queued 等）；**不是全部都由 live 或 CI 先抓到**。

### 2.5 docs（0）

（本窗沒有以文件為主體的修法 merge。）

## 3. 🔧 併入本機 trunk・未公開（0）

（判定時沒有。`fed37cff`（claim-note tmp）在 15:46 屬此類，16:04:56 已在兩個公開 trunk 上，移到 §2.4。）

## 4. 🕓 審查中（分支，未併；2）

### 4.1 kernel C++（0）

（09-27 版的 clang/TSan 已併入，見 §2.1。）

### 4.2 ndt tool（1）

| 代號 | 一句話（缺陷 → 修法） | 進 trunk 線 | 證據 |
|---|---|---|---|
| residue clock | ndt 的 residue report 讀一次鐘，`app_started_at` 對還在跑的 app 再讀一次 ⇒ 兩次之間跨秒時，app 剛裝的 rule 被算到它的時間窗外（`test_apps_residue.sh` 偶發紅）→ 同一份報表只讀一次鐘 | 未併：`fix/residue-live-pid-wait-0928` @ `74d1383f` 09-28 | 本機沒有判決檔（08:3x 查）；原因的量測在 `J26/ci-compare-pr15.txt:9-11`（coordinator 的紀錄）；commit 訊息寫了紅先行（5N 迫使兩次讀鐘之間跨秒）與變異閘——都沒執行、沒讀 log；未併（狀態截至 2026-09-28 08:3x UTC，本機 git 唯讀） |

### 4.3 tests-instruments（1）

| 代號 | 一句話（缺陷 → 修法） | 進 trunk 線 | 證據 |
|---|---|---|---|
| spawn helpers | 六支 shell 測試套件用 `X="$(spawn_fixture …)"` 叫 fixture 的 spawn helper ⇒ helper 失敗只離開 subshell、套件拿它的輸出當 pid 繼續跑，這個失敗從沒被算到 → 改在父 shell 呼叫、失敗算成一條具名的失敗檢查，等待上限 30 s（09-28 診斷 residue 偶發紅時發現） | 未併：`fix/spawn-helper-subshell-0928` @ `dfdb2121` 09-28 | 本機沒有判決檔（13:2x 查）；`3368412d` 上的一顆 commit，只改 `tests/shell/` 的 7 個檔，兩個 P4 本體的分支清單都沒有它（13:20 未認證 `git ls-remote`，`K/scratch/overnight-2026-09-05/logs/slides930/net-spawnhelpers-20260928T1320Z.log`）；commit 訊息寫了變異腳本 `mutate_fixture_spawn_helpers.sh`（讓每個 helper 都對不上、要求失敗被算到）——沒執行、沒讀 log；未併（狀態截至 2026-09-28 13:2x UTC，本機 git 唯讀） |

（09-28 06:1x 在審的 TERM trap 已併入，見 §2.4。）

## 5. 直接落在 trunk 線、不走分支的修法 commit（4；不計入 §1 的狀態數，圖上不畫磚）

| 代號 | 一句話（缺陷 → 修法） | commit | 證據 |
|---|---|---|---|
| live-p1 sudo | live-p1 的權限檢查要求整機 sudo（`sudo -n true`），操作者只有兩條 NOPASSWD ⇒ 整支只能用 sudo 跑 → 改用 `sudo -n -l <cmd>` 只問那兩條 | `41d7950f` 09-17 | — |
| live-p1 dict | 01／02／03 把 `switch_state.switches`（dict）當 list 迭代，`set -e` 在 verdict 前結束；03 的 controller 跑在沒有 `p4.tmp` 的 proxy venv → 修 | `3483203c` 09-18 | 第一次 live run 找到 |
| live-p1 03 arms | 03 把 exercise 的 skeleton controller 當綠臂（兩次 100% loss；transit rule 是學生的 TODO）→ skeleton 為紅對照、solution 為綠臂，加診斷腳本 | `62b77065` 09-18 | `04_diag_p4runtime.sh` 的記錄 |
| serve own-claim | ndt serve 的 precheck 把任何以 `yours` 開頭的 claim 當成自己的（外人 `yours-x` 也過）；兩種「讀不到」共用一句 → 全字比對、各報原因 | `6053f75f` 09-26 | intake 判官 findings 2／5／3（`J26/judge-NDTSERVE-48209682.md`） |

另有純文件更正：`ea18b6ca`、`f643b884`、`dfbab30e`（09-26，ndt serve 的註解／help／README）、`c0602510`（09-25，REPORT-P3／P4 更正）、
`7746832e`（09-27，開發機 venv 已遷移的紀錄）。

## 6. 新功能（FEATURE；不是修法，不畫）

| merge | 日期 | 內容 |
|---|---|---|
| `f282b895` | 09-17 | P1-A：P4 fabric 與 proxy 讀 app package（無 package 時每個被替換的常數原樣返回） |
| `386eb20c` | 09-17 | P1-B：`tools/p4_exercise`（tutorials exercise → app package、preflight、外部 controller） |
| `54f69d15` | 09-17 | P1-C：`ndt up p4 --app <dir>`＋live-p1 01–03 |
| `b392f111` | 09-18 | P2-A：每台 switch 跑 package 指定的 program |
| `78067633` | 09-18 | P2-B：通用 table-entry writer、`POST /p4/table_entry` |
| `365c60e1` | 09-18 | P2-C：同一套 exercise driver 跑 tutorials 與 NDTwin 兩個 fabric（附帶：`ndt status` 不再替沒編過的 pipeline 報速率） |
| `f5ad6890` | 09-18 | P3-B：鏈路層遙測（`tc … action sample` → psample → sFlow）（附帶：package 的 link shaping 真的套用） |
| `5ce3bf74` | 09-18 | P3-C：proxy 依名字讀 packet-in metadata、`ndtwin_telemetry.p4`、counter／multicast |
| `422fc014` | 09-19 | P3-D：13 個 exercise 兩個 fabric 全腳本化、`ndt up p4 --telemetry` |
| `9cec344e` | 09-18 | P3-E：三組遙測量測（PREREG、儀器、分析） |
| `572d9462` | 09-24 | phase-4 roles 第一刀：`roles.ipv4_route`、RouteBinding、宣告鏈路、capabilities、501 `unsupported_on_p4` |
| `377a1271` | 09-25 | heartbeat 段 H：`ndtwin-lab heartbeat start｜stop｜status` |
| `680c5293` | 09-25 | heartbeat spike 第 3–4 輪（未跑過的儀器的審查輪） |
| `14554090` | 09-26 | heartbeat spike 第 5 輪（同上） |
| `4bc1201b` | 09-26 | heartbeat spike 第 6 輪（同上） |
| `094f417f` | 09-26 | heartbeat spike 第 8 輪：去相位鎖的偵測量法 |
| `cafd518a` | 09-26 | heartbeat 段 W：proxy 讀 veth 心跳判鏈路、只在 NDTwin 擁有路由表時改路 |
| `48209682` | 09-26 | `ndt serve`：本機 HTTP API |
| `f186ce98` | 09-27 | `ndt serve` 自帶網頁 |
| `5dc7fc9a` | 09-27 | P4 proxy 升 protobuf 5.29.6（修 CVE-2025-4565／CVE-2026-0994；依任務單歸 FEATURE） |
| `85bec430` | 09-28 | 第三刀 kernel 側：每台 bmv2 switch 的 `get_graph_data` 節點帶上 proxy 回報的 capabilities（原樣複製，沒有就不帶）；ctest 1385/1385（多 17 個 P4Capabilities*，`I/ci-compare-pr14.txt:2`） |

未併的 FEATURE 分支（不入本檔的狀態數；tip 取 2026-09-28 08:3x UTC）：`feat/external-detect-only-0927` @ `480e9f2e` 與它的第四輪 `wip/external-detect-r4-0928` @ `89615935`（external control plane 的斷線偵測；**未完成，對外不可說**）、
`feat/ndt-serve-gui-v2-0927` @ `6d5621ab`（頁面 v2；仍沒有頁面檔）。第三刀的 GUI 側在另一個 repo（`~/Web-GUI` 的 `draft/p4-capabilities-0924` @ `65eecf6`），不在本 repo，也不在本檔的計數裡。
（09-27 版的 `feat/kernel-capabilities-0927` 已併為 `85bec430`。）

## 7. 其他 merge 與不算修法的未併分支（不畫）

| merge | 日期 | 內容 |
|---|---|---|
| `dc0237c8` | 09-17 | README：把 ndtwin-lab 上的 README 擴寫併回 trunk |
| `7218ab82` | 09-17 | README：`-s ours` 併入 Adam010341 的 README 分支，讓 `trunk:main` 能 fast-forward |
| `5f1d4611` | 09-24 | README：badge 列併回 |
| `6291db35` | 09-24 | README：架構圖與 P4 pipeline 圖併回 |
| `318e6391` | 09-26 | 報告：P4-HB-SPIKE run 1–2 |
| `9c2e59e4` | 09-26 | 報告：P4-HB-SPIKE run 3–4（去相位） |

未併、也不算修法的分支（2026-09-28 08:3x 仍是這 7 條）：`pr/shell-test-scoring` @ `48e8005d`（PR #6 的載具，內容＝`4ff4eee8`）、`pr/claude-md-rules` @ `a5bfd282`（CLAUDE.md 的 PR）、
`fix/p4proxy-protobuf5-0926` @ `5bb5f1fa`（tree 與 `5dc7fc9a^2` 相同，`6908659…`，已以改寫過主旨的版本併入）、
`cand/p4proxy-protobuf5-0925` @ `7cc50b42`（被上一條取代）、`docs/prereg-amendment-2-0924` @ `69e79a8f`（依 TICKET-P4 §7 裁決 2 不併）、
`chore/tools-out-of-audit-0927` @ `311c5053`（把 live 工具搬出 `doc/audit`，搬移不是修法）、
`pr/ndt-serve-claim-note` @ `ef3aec3f`（`fed37cff` 內容的 PR 載具，已以 PR #8 併進 Adam010341 `main`，見 §8）。

## 8. 公開預設分支 `main` 上有哪些

- 兩個 P4 本體的預設分支都是 `main`（`"default_branch": "main"`，§9 第 5–6 列）。
- **兩個 P4 本體的 `main` 都是 `eef173a9`**（§9 第 37 列，2026-09-28 08:53，未認證；ndtwin-lab 那份依 Adam 09-28 的規則跟著快轉）＝PR #6 `ce6a9832`、#7 `f347a588`、#8 `f9be5842`、#9 `bad4cc7a`、#10 `847acc7d`、#11 `5d0f442c`、#12 `4a3d7f39`、#13 `d0696776`、#14 `be01cc7a`、#16 `9a74408b`、#15 `299c9e23`、#17 `eef173a9` 依序 squash
  （`figures/engineering/_net/pulls_Adam010341.json`，08:53:31 未認證；沒有開著的 PR）。`eef173a9` 與 trunk `3368412d` 的 tree 只差三個 `doc/audit/**/*.md`（依 PR 規則不進 main）；`git diff --name-status eef173a9 3368412d`，本機唯讀
  ⇒ **§2 的 39 列的碼全部在兩個 `main` 的內容裡**；但那些 merge commit 本身不在 `main` 的歷史上（squash 產生新 sha）。
- （09-28 06:20 以前 ndtwin-lab 的 `main` 停在 `f186ce98`，09-27 的規則是凍結；06:42 起跟著 Adam010341 的 `main`。）
- 🔴 **手冊 P4 路徑叫人 clone 的 `ndtwin-lab/NDTwin-Kernel-P4-public`**：`main` = `9e6cc307`（09-03），`compare/dc0237c8...main` 回 **404**
  （那個 repo 裡沒有本窗最早的 merge）；2026-09-28 06:20:07 與 08:38:41 再查仍是 `9e6cc307`（§9 第 28、35 列）⇒ **本檔 40 列一列都不在使用者照手冊拿到的那份 code 裡**。trunk 修好 ≠ 使用者拿得到。


- 🕓 的 2 條：兩個 `main` 都沒有（residue clock 08:53 查；spawn helpers 13:20 查，兩個 `main` 仍是 `eef173a9`，`dfdb2121` 不是它的祖先）。


## 9. 公開驗證紀錄（未認證 `curl -s`，無 token；時間皆 UTC；原始行存於 `figures/fixed-since-916/public-check-20260927.log`）

| # | 時間（UTC） | 指令（`curl -s -o <f> -w '%{http_code}' <URL>`） | HTTP | 結果 |
|---|---|---|---|---|
| 1 | 2026-09-27T15:46:39Z | `https://api.github.com/repos/ndtwin-lab/NDTwin-Kernel-P4/branches/trunk` | 200 | head `3d740be0964b36091c6f4299bd288fa52bcd258d` |
| 2 | 15:46:40Z | `…/ndtwin-lab/NDTwin-Kernel-P4/branches/main` | 200 | head `f186ce98c7643cf1e7a9e7e402e4193bd0d72805` |
| 3 | 15:46:40Z | `…/Adam010341/NDTwin-Kernel-P4/branches/trunk` | 200 | head `3d740be0964b36091c6f4299bd288fa52bcd258d` |
| 4 | 15:46:40Z | `…/Adam010341/NDTwin-Kernel-P4/branches/main` | 200 | head `ce6a983242d2339a2528f2af769661bba772f496` |
| 5 | 15:47:18Z | `…/repos/ndtwin-lab/NDTwin-Kernel-P4` | 200 | `default_branch=main`、`private=false` |
| 6 | 15:47:19Z | `…/repos/Adam010341/NDTwin-Kernel-P4` | 200 | `default_branch=main`、`private=false` |
| 7 | 15:47:21Z | `…/ndtwin-lab/NDTwin-Kernel-P4/compare/dc0237c8...trunk` | 200 | `ahead`，ahead_by 486、behind_by 0 |
| 8 | 15:47:23Z | `…/Adam010341/NDTwin-Kernel-P4/compare/dc0237c8...trunk` | 200 | `ahead`，ahead_by 486、behind_by 0 |
| 9 | 15:47:31Z | `…/Adam010341/NDTwin-Kernel-P4/branches?per_page=100` | 200 | 8 條；無 §4 的任何分支 |
| 10 | 15:47:31Z | `…/ndtwin-lab/NDTwin-Kernel-P4/branches?per_page=100` | 200 | 6 條；無 §4 的任何分支 |
| 11 | 15:47:28Z | `…/ndtwin-lab/NDTwin-Kernel-P4/compare/dc0237c8...main` | 200 | `ahead`，ahead_by 478 |
| 12 | 15:47:29Z | `…/ndtwin-lab/NDTwin-Kernel-P4/compare/4ff4eee8...main` | 200 | `behind`，behind_by 7，merge_base f186ce98 |
| 13 | 15:47:29Z | `…/Adam010341/NDTwin-Kernel-P4/compare/f186ce98...main` | 200 | `ahead`，ahead_by 1 |
| 14 | 15:47:30Z | `…/Adam010341/NDTwin-Kernel-P4/compare/4ff4eee8...main` | 200 | `diverged`，ahead_by 1、behind_by 7 |
| 15 | 15:59:39Z | `…/ndtwin-lab/NDTwin-Kernel-P4-public/branches/main` | 200 | head `9e6cc3071fd59a25f913f6d99a885033506d3983`（09-03） |
| 16 | 15:59:40Z | `…/ndtwin-lab/NDTwin-Kernel-P4-public/compare/dc0237c8...main` | 404 | 該 repo 沒有 `dc0237c8` |
| 17 | 16:04:56Z | `…/ndtwin-lab/NDTwin-Kernel-P4/branches?per_page=100` | 200 | 6 條；`trunk` `fed37cff…`、`main` `f186ce98…`；無 §4 的任何分支 |
| 18 | 16:04:56Z | `…/Adam010341/NDTwin-Kernel-P4/branches?per_page=100` | 200 | 9 條；`trunk` `fed37cff…`、`main` `ce6a9832…`；無 §4 的任何分支 |
| 19 | 17:02:39Z | `…/Adam010341/NDTwin-Kernel-P4/branches?per_page=100` | 200 | 9 條；`trunk` `fed37cff…`、`main` `f9be5842ed48c42ec3bba048179b39b0a254417e`、`audit-raw` `797c34ab8379a591dab91239a1292e05094dee7f`；無 §4 的任何分支 |
| 20 | 17:02:39Z | `…/ndtwin-lab/NDTwin-Kernel-P4/branches?per_page=100` | 200 | 6 條；`trunk` `fed37cff…`、`main` `f186ce98…`、`audit-raw` `797c34ab…`；無 §4 的任何分支 |
| 21 | 2026-09-28T06:16:55Z | `…/ndtwin-lab/NDTwin-Kernel-P4/branches/main`（06:16:12 那次 000，無回應，重試） | 200 | head `f186ce98…` |
| 22 | 06:16:28Z | `…/Adam010341/NDTwin-Kernel-P4/branches/main` | 200 | head `be01cc7a…` |
| 23 | 06:16:27Z | `…/ndtwin-lab/NDTwin-Kernel-P4/branches/trunk` | 200 | head `85bec430…` |
| 24 | 06:16:55Z | `…/Adam010341/NDTwin-Kernel-P4/branches/trunk`（06:16:28 那次 000，重試） | 200 | head `85bec430…` |
| 25 | 06:16:40Z | `…/Adam010341/NDTwin-Kernel-P4/pulls?state=all&per_page=30` | 200 | #6–#14 都 merged，#14 `merge_commit_sha` `be01cc7a…` |
| 26 | 06:20:06Z | `…/ndtwin-lab/NDTwin-Kernel-P4/branches?per_page=100` | 200 | 6 條；`trunk` `85bec430…`、`main` `f186ce98…`、`audit-raw` `5cf0364c…`；無 §4 的任何分支 |
| 27 | 06:20:07Z | `…/Adam010341/NDTwin-Kernel-P4/branches?per_page=100` | 200 | 15 條；`trunk` `85bec430…`、`main` `be01cc7a…`、`audit-raw` `5cf0364c…`、9 條 `pr/*`；無 §4 的任何分支 |
| 28 | 06:20:07Z | `…/ndtwin-lab/NDTwin-Kernel-P4-public/branches/main` | 200 | head `9e6cc307…`（09-03），沒有動 |
| 29 | 06:20:07Z／06:21:07Z | `…/repos/ndtwin-lab/NDTwin-Kernel-P4`、`…/repos/Adam010341/NDTwin-Kernel-P4`（後者 06:20:08、06:20:27 兩次 000，重試） | 200 | 兩個都 `default_branch=main`、`private=false` |
| 30 | 06:42Z | `git ls-remote https://github.com/{ndtwin-lab,Adam010341}/NDTwin-Kernel-P4.git refs/heads/main refs/heads/trunk`（不帶憑證） | — | 兩邊 `main` 都是 `be01cc7a…`、`trunk` 都是 `85bec430…`（未存檔，指令的輸出記在 `K/…/slides930/PROGRESS-0928.md`） |
| 31 | 06:45:52Z–06:45:54Z | 四條 `…/branches/{main,trunk}` 再抓一次 | 200 ×4 | ndtwin-lab `main` `be01cc7a…`、`trunk` `85bec430…`；Adam010341 同；存於 `figures/engineering/_net/branch_*.json`（06:16 那份在 `_net/prev-20260928T0616Z/`） |
| 32 | 08:38:26Z | `…/ndtwin-lab/NDTwin-Kernel-P4/branches?per_page=100` | 200 | 6 條；`trunk` `3368412d…`、`main` `299c9e23…`；無 §4 的分支 |
| 33 | 08:38:27Z | `…/Adam010341/NDTwin-Kernel-P4/branches?per_page=100` | 200 | 18 條；`trunk` `3368412d…`、`main` `299c9e23…`；無 §4 的分支 |
| 34 | 08:38:27Z／08:38:49Z | `…/repos/ndtwin-lab/NDTwin-Kernel-P4`、`…/repos/Adam010341/NDTwin-Kernel-P4`（後者 08:38:28 那次 000，重試） | 200 | 兩個都 `default_branch=main`、`private=false` |
| 35 | 08:38:41Z | `…/ndtwin-lab/NDTwin-Kernel-P4-public/branches/main` | 200 | head `9e6cc307…`（09-03），沒有動 |
| 36 | 08:31:56Z–08:32:31Z | 四條 `…/branches/{main,trunk}`、`pulls?state=all&per_page=30`（ndtwin-lab trunk 08:31:57 那次 000，重試） | 200 | 兩個 `main` `299c9e23…`、兩個 `trunk` `3368412d…`；PR #6–#16 都 merged、#17 開著；存於 `figures/engineering/_net/` |
| 37 | 08:53:29Z–08:53:33Z | 四條 `…/branches/{main,trunk}`、`pulls?state=all&per_page=30`（PR #17 併入之後） | 200 | 兩個 `main` `eef173a9…`、兩個 `trunk` `3368412d…`；PR #6–#17 都 merged、沒有開著的；存於 `figures/engineering/_net/`（前一份移到 `_net/prev-20260928T0832Z/`） |

09-27 共 20 次請求。09-28 這一輪的每一次請求（含 CI 的 runs／jobs、三次 000 與一次沒記到 log 的診斷請求）逐行在 `K/scratch/overnight-2026-09-05/logs/slides930/net-refresh-20260928T0616Z.log`；
第 21–25 列的回應存在 `figures/engineering/_net/`，第 26–29 列的存在 `figures/fixed-since-916/public-check-20260928/`（腳本 `slides930/net_get.py`：不帶任何 token）。
08:3x 重新釘住那一輪（第 32–36 列）逐行在 `K/scratch/overnight-2026-09-05/logs/slides930/net-repin-20260928T0831Z.log`，第 37 列在 `…/net-repin2-20260928T0853Z.log`；第 32–35 列的回應在 `figures/fixed-since-916/public-check-20260928b/`，第 36 列的在 `figures/engineering/_net/`（前一份移到 `_net/prev-20260928T0645Z/`）。

### 9.1 本檔判定用的公開 trunk head（第 32、33 列；腳本讀這張表）

| repo | 時間（UTC） | HTTP | 公開 trunk head |
|---|---|---|---|
| ndtwin-lab/NDTwin-Kernel-P4 | 2026-09-28T08:38:26Z | 200 | `3368412d4fc452ce658f54adf458b4c6e275b81c` |
| Adam010341/NDTwin-Kernel-P4 | 2026-09-28T08:38:27Z | 200 | `3368412d4fc452ce658f54adf458b4c6e275b81c` |

- ✅ 的判定：上表的公開 head 是 40 位 sha；「§2 每一顆是它的祖先」由腳本以 `git merge-base --is-ancestor <sha> <head>` 在本機物件上算
  （sha 是內容定址，這是圖論事實，不是拿本機 ref 當公開證據）；第 7、8 列在 GitHub 上抽驗最早的一顆（`dc0237c8`）。
- 🔧 的判定：本機快照 `3368412d` 就是兩個公開 trunk head ⇒ 判定時 🔧＝0。（09-27 版：15:46 時 `fed37cff` 屬 🔧，16:04:56 起公開。）

### 9.2 coordinator 以**已認證** `gh` 查到的（2026-09-27 UTC，原文寫 09-28 +08；轉述，本檔沒有重做，**不當公開證據**，與上面的未認證紀錄分開）

- （當時）Adam010341 `main` = `ce6a9832`（PR #6，09-27 15:45 squash-merge）；PR #7、#8 開著（其後 #7、#8 都已併入，見 §8 與第 19 列）。
- trunk = `fed37cff`；ndtwin-lab `main` 凍結在 `f186ce98`（09-27 的規則；09-28 起跟著同步，見 §8）。
- Dependabot：ndtwin-lab 的 alert #1、#2（high，protobuf）09-27 08:20 以 fixed 關閉（對應 §6 的 `5dc7fc9a`）。

## 10. 上台怎麼講（三句，草稿）

1. 「09-16 之後，trunk 多了 39 個修法 merge，全部已在公開的 trunk 上，也都進了 main；另有 2 條在審。」
2. 「修的東西大多在量測儀器與測試本身（28/41）；kernel C++ 只有 2 個，都已併入。」
3. 「公開的 trunk 有，不等於使用者拿得到：手冊叫人 clone 的 P4-public 還停在 09-03。」

（本檔與圖停在 `3368412d`；之後 trunk 再動，下一次更新時重算。）
