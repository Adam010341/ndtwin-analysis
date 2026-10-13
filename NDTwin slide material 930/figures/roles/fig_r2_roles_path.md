# fig_r2_roles_path —— roles.ipv4_route 從 package 走到程式自己的那張表

[Co-developed with claude code -- Adam]

本檔所有日期與時間皆為 **UTC**（run 目錄名的 `…Z`；commit 時間以 `TZ=UTC git log` 換算）。

## 一句話

上排是 09-26 那次 live 07 實際印出來的建包步驟：package 宣告 `roles.ipv4_route`（表 `MyIngress.ipv4_lpm`、比對 `hdr.ipv4.dstAddr`、動作 `MyIngress.ipv4_forward`）→ `convert.py` 把那張表原有的 16 條 entries 拿掉 → pre-flight 兩條檢查 PASS → `ndt up` 後 proxy 寫進 16 of 16 條初始路由。下排是 trunk `3d740be0` 的程式碼路徑：kernel 的寫入經 proxy 的 `route_flow`，用 `RouteBinding` 給的名字，以 P4Runtime Write 寫進**練習程式自己的** `MyIngress.ipv4_lpm`；沒有 roles 時同一條路回 501。上下兩排分開畫：上排是跑過的，下排是讀碼的。

## 資料來源

K＝`/home/adam/Desktop/NDTwin-Kernel`；R＝`K/doc/audit/2026-09-04_p4-tutorial-exercise-prep/live-p1/runs/2026-09-26T202055Z_07_roles_basic`。

| 用途 | 檔（path:line 或 JSON key） | commit／binary |
|---|---|---|
| package 宣告的三個名字 | `R/10_convert_roles.txt` 的 `roles :` 行 | run HEAD `b2eeb71d`（`R/01_binaries.txt`）；convert.py sha256 `fb30c4cd11575575` |
| 16 條拿掉（每台 4 條） | `R/10_convert_roles.txt` 的 `owned table :` 行（腳本核對 16＝4+4+4+4） | 同上 |
| pre-flight 兩條 PASS | `R/12_preflight_basic_roles.txt`：`PASS  roles.ipv4_route resolves`、`PASS  owned table has no package entries`；末行 `PASS -- every check passed` | preflight.py sha256 `c30e4e8b451c6dc6` |
| 16 of 16 條初始路由 | `R/21_proxy_roles_lines.txt`（`16 of 16 initial routes written into the package's route tables`） | main.py `54c9bd96c181b0dd`、topology_manager.py `dae3c3ca279bf78b` |
| kernel | `K/src/ndt_core/routing_management/HttpRoutingStrategyBase.cpp:326`（`installAnEntry`）、`:344`（`post("/stats/flowentry/add", …)`）；P4 策略繼承它：`K/include/ndt_core/routing_management/P4RoutingStrategy.hpp:24` | trunk `3d740be0`（READ） |
| proxy 入口 | `K/p4_proxy/proxy_agent/api_routes.py:500`（`@router.post("/stats/flowentry/add")`）→ `:529`（`topology.route_flow`） | 同上 |
| `route_flow` | `K/p4_proxy/proxy_agent/topology_manager.py:943`；呼叫 `insert_ipv4_route` 在 `:1057` | 同上 |
| `install_initial_routes` | `topology_manager.py:1279`；呼叫 `insert_ipv4_route` 在 `:1338` | 同上 |
| `RouteBinding` | `K/p4_proxy/proxy_agent/route_binding.py:79`（dataclass）、`:193`（`resolve`）；每台建 client 時決定：`K/p4_proxy/proxy_agent/main.py:230`（`build_p4_client`）、`:265`（`client.bind_routes(route_binding_for(...))`）、`:314`（`route_binding.resolve(...)`）；`K/p4_proxy/proxy_agent/p4_client.py:438`（`bind_routes`） | 同上 |
| 寫入 | `p4_client.py:1871`（`insert_ipv4_route`）、`:1880`（先過 `_writable_route_binding`）、之後 `self.stub.Write`（腳本斷言在函式 40 行內） | 同上 |
| 501 分支 | `p4_client.py:455`（`_writable_route_binding`）、`:463`（binding 為 None ⇒ `RouteWriteUnsupported`，reason `unbound`）；`api_routes.py:537`（轉成 501）、`:214`（`"outcome": "unsupported_on_p4"`）；`route_binding.py:73` | 同上 |
| 同一個 `resolve()` | `K/tools/p4_exercise/preflight.py:386`（`_check_roles`）、`:444`（`route_binding.resolve(...)`）、`:512`（owned table 那條 PASS）；`route_binding.py` 模組 docstring「ONE FUNCTION, TWO CALLERS」 | 同上 |
| convert 的旗標 | `K/tools/p4_exercise/convert.py:697`（`apply_route_role`） | 同上 |

所有 READ 行號都由腳本在 `git show 3d740be0:<path>` 上找出並印出（`make_roles_figs.py` 的 `[read 3d740be0]` 行；最後一次執行的輸出存在 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/roles-figs-run-20260927T1705Z.log`），找不到就中止。

## 可信度

**OBSERVED（09-26 live 07，HEAD `b2eeb71d`）**
- package 宣告的三個名字、16 條被拿掉、pre-flight 兩條 PASS、proxy 寫進 16 of 16 條初始路由（上排四格）。
- 同一次 run 的 L2：kernel batch 寫一條 `10.0.9.9 → port 3`，`/stats/flow/1` 讀回 `OUTPUT:3`；L5：沒有 roles 的同一支程式寫入得到 501 `unsupported_on_p4`、reason `unbound`（見 `fig_d2`、`fig_r3`）。

**READ（trunk `3d740be0`，沒執行）**
- 下排每一格的函式名與呼叫關係，行號如上表。
- pre-flight 與 proxy 呼叫的是同一個 `route_binding.resolve`。

- 下排讀的碼就是上排那次 run 跑的碼：`R/01_binaries.txt` 記的六個 proxy／工具檔 sha256（`route_binding.py`、`p4_client.py`、`main.py`、`topology_manager.py`、`convert.py`、`preflight.py`）與 `3d740be0` 的同名檔逐一相等；`api_routes.py`、`src/ndt_core/routing_management`、`include/ndt_core/routing_management`、`HttpSession.cpp` 的 `git diff b2eeb71d 3d740be0` 為空。兩項都由腳本斷言（`[read 3d740be0] = the 09-26 run's code on this path`）。kernel binary 本身（`be70b5dd32356847`）是從哪個 commit 建的，raw 沒記。

**INFERRED**
- 「L2 那條規則走的就是下排這條路」：碼是這樣接的，raw 只看得到兩端（kernel 回 queued、proxy 讀回），中間各函式沒有 trace。

## 圖怎麼讀

上排左到右是建包到開機；下排左到右是一次寫入。藍虛線「same resolve()」表示 pre-flight 與 proxy 用同一個函式驗 package 的宣告，不是資料流。紅框是沒有 roles 時的去向。

## 已知但書

- 🔴 只綁了**目的路由表**這一張。說法要照這個範圍講：「宣告了 `roles.ipv4_route` 的外來程式，NDTwin 能寫它那張目的 IP 路由表」。**不要說「NDTwin 能操作外來 P4 程式」**——五元組、多表、tunnel 都沒有 role，external 控制面也不歸這條路。
- `ndt up` 的收尾橫幅在這個 run 仍印「NDTwin discovered no links and installed no routes on this fabric」（`R/20_up_roles.txt` 末段），和 proxy log 的「16 of 16 initial routes written」（`R/21_proxy_roles_lines.txt`）互相矛盾。讀碼：`K/tools/test_workflow/ndt:4151-4157`（`3d740be0`；`b2eeb71d` 同一行號）只要是外來 pipeline 就印這段，不看 roles。這是橫幅過時，不是路由沒寫（L3 pingall 12/12 且 owned 表已無 package entries）。
- 下排的 kernel 格只寫 `installAnEntry`；batch 端點進來後經 `HttpSession::processFlowBatch` 與 dispatcher 才到這裡（`K/src/ndt_core/http/HttpSession.cpp:2171`、`:2386`），圖上省略。
- raw 在 trunk 未提交（`runs/`），已鏡射到本機 `audit-raw` 分支 `36f8dd8d`，blob 逐檔相同（2026-09-27 17:2xZ integrator 再比：`36f8dd8d` 是 audit-raw `797c34ab` 的祖先，引用的 run 目錄在 `797c34ab` 逐檔 blob 與工作樹相同；`797c34ab` 依 coordinator 已公開在兩個 P4 repo）。
- 🔴 **上排那次 07（09-26）跑在 dirty checkout 上**：`ndt status` 的 code 行是 `b2eeb71d  +92 file(s) with uncommitted changes`（`R/00_status_before.txt:7`），其中點名兩個可能改變行為的：`p4_proxy/mininet/host_count_override`（值 4）與 `tools/remote-lab/dorm_lab/`。sha 只說 HEAD，不代表 run 的整棵樹；本頁用到的六個 proxy／工具原始檔另有 sha256（`01_binaries.txt`）。
- 產生器斷言的紅燈檢查：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/roles-flowapi-redcheck.py`，紀錄 `/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/roles-flowapi-redcheck-20260927T1704Z.log`（12 個變異全因指名的原因中止、2 個對照通過；第一版在 `…/roles-flowapi-redcheck.first-20260927T1606Z.log`）。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/roles"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_roles_figs.py
```

最後產出：2026-09-27T17:05Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_roles_figs.py` sha256 `280b76fbbdf34135…`（產圖之後腳本沒再改過）。
