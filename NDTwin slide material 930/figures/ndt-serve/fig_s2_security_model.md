# fig_s2_security_model —— ndt serve 擋誰、怎麼擋；哪幾條真的在 lab 上跑過

[Co-developed with claude code -- Adam]

> 本檔所有日期時間都是 **UTC**（judge F-18）。raw 檔名與檔內的 `+08:00` 時間戳照原樣引用，旁邊註明換算。

## 一句話

`ndt serve` 對八種威脅各有一道防線（**讀碼**，trunk 上的 `tools/ndt_serve` ＝ GUI v1 合併 `f186ce98`）；
其中五條在 **09-24（UTC）的真 lab** 上看過擋住（右欄綠）。別人的 claim 底下的 `up`：碼裡 P4 與 OVS 都由 ndt 自己的 guard 回 rc 5
（OVS 那一處由 `68ace017` 加入，trunk 上）；live 只有 P4（rc 5、什麼都沒建），**OVS 沒有在 lab 上跑過**（not run live）。
一次性連結、指令預覽、apps／cells 的「claim 必須是你的」三條是 09-24 之後才加的，**沒有在 lab 上跑過**。
v1.8（2026-09-29）：圖只畫最後狀態；09-24 那一筆修前的 OVS 紀錄只留在本檔（見「已知但書」），v1.7 被換掉的段落逐字在 `README-930.md` §13.7。

## 資料來源

| 用途 | 檔（path:line 或 JSON key） | commit／binary |
|---|---|---|
| READ：只綁本機 | `tools/ndt_serve/serve.py:72`（`BIND = "127.0.0.1"`）、`:1214`（`Server((BIND, a.port))`）、`:1163`（`--port` 預設 8765） | `f186ce98`（HEAD `fed37cff`／`3d740be0` 的 `tools/ndt_serve` 與它逐位元組相同，腳本 `git diff --quiet` 驗） |
| READ：Host 必須是自己 | `serve.py:477-482` `_check_host`（只收 `127.0.0.1:<port>`／`localhost:<port>`，防 DNS rebinding） | 同上 |
| READ：token／Origin／無 CORS | `serve.py:73` `TOKEN_HEADER`；`:484-488` `_check_token`；`:463`＋`:496-499` 除 `/health` 外每個 GET 都查；`:501-511` 寫入查 token→Origin→JSON body；`:490-494` Origin 若有就必須是自己；`:453-458` 頁面三個靜態檔不查 token（它們不執行任何東西）；`:404-406` 從不回 `Access-Control-*`（全檔只有這一處註解提到該字串） | 同上 |
| READ：一次性連結 | `serve.py:94` `NONCE_TTL_S = 600`、`:95` `MAX_NONCES = 8`、`:187-188` URL 形如 `http://127.0.0.1:<port>/#k=<key>`、`:209-217` `take()`（先刪再回答＝只能用一次）、`:601-617` `POST /session` 以 key 換 token，且 **Origin 必填、必須是自己**（`:607-609`） | 同上；本機制在 `5281c2e1`（09-27 06:11Z）才加入 |
| READ：指令預覽 | `serve.py:359-370` `DryRun`（回傳 whitelist 建好的 argv，什麼都不跑）；`:703-709` `_spawn` 在取槽位之前就丟出；`:1118-1119` `DRY_RUN_OK` 只收會 spawn 的寫入；`:376-392` `confirm_policy` | 同上；`5281c2e1`（09-27）加入 |
| READ：一次一個 job | `serve.py:395` `SLOT`；`:710-713` 槽位被占 ⇒ 409 `busy` | 同上 |
| READ：apps／cells 要你自己的 claim | `serve.py:787-811` `_require_own_claim`（讀 `ndt status` 的 claim 行，`:1031` `OWN_CLAIM` **整行精確比對** `yours -- Nm left (until HH:MM:SS)`，格式出自 `tools/test_workflow/ndt:5799`）；apps 在 `:690-696`、lab cell 在 `:785` 套用 | 同上；cells 版 `8f2fbb5b`（09-24 15:22Z）、apps 版 `475b1036`（09-27 08:27Z） |
| READ：up／down 由 ndt 自己擋 | `tools/test_workflow/ndt:996` `guard_up_lab_free`（rc 5＝拒絕）；P4 在 `:3313` 呼叫、OVS 在 `:4362` 呼叫；誰擋什麼的說明 `serve.py:381-384` | ndt 同上 HEAD（09-29 讀 `3368412d`）；OVS 那一處由 `68ace017`（2026-09-25 12:23Z）併入——腳本斷言 `68ace017` 是 HEAD 的祖先，且它的 first-parent diff 加入了 `guard_up_lab_free "ovs $ovs_hosts"` 那一行 |
| READ：OVS「not run live」 | 腳本掃 `scratch/overnight-2026-09-05/logs/ndt-serve-0924/` 底下全部 `summary.json`（5 份）：「在別人的 claim 下跑 OVS `up`」的步驟只有 1 筆，job `20260924T144946Z-c3c7e1`＝09-24 14:49:46Z，早於 `68ace017`（job id 的時間是 UTC，`tools/ndt_serve/jobs.py:88` 用 `time.gmtime()`）；修法之後有這種步驟、或那一筆不在修法之前，腳本就停下。另一次性查（2026-09-29 08:14:15Z，讀、非腳本；`K/scratch/overnight-2026-09-05/logs/slides930/ovs-live-search-v18-20260929T0814Z.log`）：修法的 live 步驟清單（`scratch/overnight-2026-09-05/hunt-0911/fix/NDT-OVS-SUMMARY.md` §6）用的 owner 名 `ovs-claim-live-0925`／`ovs-claim-foreign-0925` 在 `K/scratch`、`K/doc`、`K/.test_run` 只命中該 SUMMARY、它在 `wt-audit-raw` 的鏡射，以及那份 log 自己 | 只證明「在這些地方找不到」 |
| OBSERVED：只有一個 listener | `scratch/overnight-2026-09-05/logs/ndt-serve-0924/live-fixes-20260924T2249/01-listen-and-token.txt` 第 2 行 `LISTEN 0 5 127.0.0.1:8765`（`ss -ltnpH 'sport = :8765'`，檔內 `22:49:21+08:00`＝09-24 14:49:21Z） | serve 碼 `c836cff0`（同目錄 `00-before.txt:2`）；ndt sha256 `cb134ccc…`（`00-before.txt:4`）＝ git blob `3273df8b`＝trunk `fd7382a3` 的 ndt |
| OBSERVED：外來 Host ⇒ 403 | `live-20260924T2201/api/04-probe-foreign-host.http`、`live-fixes-20260924T2249/b/04-probe-foreign-host.http`：`Host: rebind.attacker.test:8765` ⇒ `403 {"error": "host"}` | 14:01Z 那輪 serve 碼 `a139bceb`（`live-20260924T2201/00-before.txt:2`）；14:49Z 那輪 `c836cff0`；ndt 同上 |
| OBSERVED：沒帶 token ⇒ 403 | `live-20260924T2201/api/03-probe-no-token.http`（POST /down）、`live-fixes…/b/03-probe-no-token.http`（POST /down）、`b/14-probe-check-no-token.http`（GET /status?check=1，會打鎖探針的那個讀取） ⇒ `403 {"error": "token"}` | 同上 |
| OBSERVED：第二個寫入 ⇒ 409 | `live-20260924T2201/api/10-probe-busy-while-up.http`：`up` 跑的同時 POST /down ⇒ `409 {"error": "busy"}`，body 裡指名那個 `running` 的 up job | `a139bceb`；ndt 同上 |
| OBSERVED：別人的 claim 下 `up p4` | `live-fixes…/a2/summary.json` step `up-p4-under-a-foreign-claim`：argv `ndt up p4`、`rc 5`、`rc_class refused`、0.1 s；`a2/01-status-under-the-foreign-claim.http` 的 claim 行是 `ndt-serve-0924-foreign -- 5m left`；`a2/before-up.knob.diff`＝`after-up.knob.diff`（knob 沒動） | `c836cff0`；ndt 同上 |
| OBSERVED（修前，不上圖）：別人的 claim 下 `up`（OVS） | `live-fixes…/a/summary.json` step `up-under-a-foreign-claim`：argv `ndt up 4`、`rc 0`、meaning「the fabric came up and verified」、8.5 s；`a/18-…http` 的 claim 行是外人的；fabric 在無人 claim 下活了約 29 秒（`doc/audit/2026-09-24_ndt-serve/REPORT.md:56-63`） | 同上；跑的是 `68ace017` 之前的 ndt |

- 以上 OBSERVED 的 raw 全在 `scratch/` 底下，**不在版本控制裡（未提交的觀測）**。
- **髒的 checkout（judge F-16）**：這幾輪驅動的 ndt 是主 checkout `fd7382a3`＋**60 個檔有未提交的修改**，其中 **2 個可改變行為**：
  `p4_proxy/mininet/host_count_override`（未提交的 `4`）與 `tools/remote-lab/dorm_lab/`。出處：`live-20260924T2201/99-after.txt:15-18`、
  `live-fixes-20260924T2249/a2/01-status-under-the-foreign-claim.http` 與 `a/18-…http` 的 `stdout` 第 9-12 行；腳本解析三處並斷言相同。
  ndt 檔本身的 sha256 `cb134ccc…` 等於 `fd7382a3` 的 blob `3273df8b`（`git cat-file -p 3273df8b | sha256sum`），也就是 ndt 這個檔沒有被改。
  ndt serve 的碼跑在各自的 worktree（`a139bceb`／`c836cff0`），`00-before.txt` 只記了 HEAD，**沒記 worktree 是否乾淨**。
- 腳本逐一 parse 並斷言：listener 恰一行且是 `127.0.0.1:<port>`；Host／token／busy 的 HTTP 碼與 `error` 欄；
  兩個 up 的 argv、rc、rc_class、當下 claim 行、knob diff。任一不符即 `SystemExit`。
  另把上表每個 `file:line` 寫成斷言（行號移動就失敗）。
- 紅燈檢查（腳本的斷言看過紅）：9 個人工破壞（外來 Host 改回 200、多一個 0.0.0.0 listener、P4 rc 改 0、兩輪的髒檔數不同、
  serve.py 行號位移、verdict 拿掉、PROVENANCE 改寫、replay 日期沒有時刻、compose 改綁 127.0.0.1）全部讓腳本停下，真 raw 對照組通過。
  log 與驅動：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/ndt-serve-s2s4-red-checks.{log,py}`（09-27 17:04:54Z，腳本 sha256 `4d033d29…`；scratch，未提交）。
  v1.8（2026-09-29）對目前的產生器（`22860412cca400bb…`）重跑：`ndt-serve-s2s4-red-checks-v18-20260929T0812Z.log`（9/9 停下、對照組通過）；S3 日期停止條件 `make_serve_s2_s4-s3date-redcheck-20260929T0812Z.log`（3/3、對照組通過）。
- v1.8 新增的停止條件（up/down 那一列只畫最後狀態）：`make_serve_s2_s4-redcheck.py` → `make_serve_s2_s4-redcheck-20260929T0811Z.log`：**8 個竄改 8/8 以產生器自己的具名理由停下、4 個對照組通過**——`68ace017` 不在 HEAD／git 不認得／換成沒加 OVS guard 那一行的 commit；OVS 那一筆的 job 時間晚於修法／job id 沒有時間；新的 live summary 在修法之後有 OVS `up`（`up 4` 與 `up ovs 4` 各一）；summary.json 不是步驟清單。對照組：修法之後的 P4 `up`、修法之前的 OVS `up`、修法之後不是「別人 claim」的 OVS `up` 都不會停。
  （同一分鐘跑了兩次：第一次之後產生器只多印掃描筆數、沒改任何判斷，第二次覆寫了同名 log；log 檔頭記的是第二次、也就是現在的產生器 sha256。）

## 可信度

**OBSERVED（09-24 14:01Z–14:53Z 真 lab、真 ndt，經 API；未提交的 raw；ndt 所在 checkout 髒 +60 file(s)，見上）**
- `ss` 看到 :8765 只有一個 listener：`127.0.0.1:8765`。
- 外來 Host（`rebind.attacker.test:8765`）兩輪都回 403 `host`。
- 沒帶 token 的寫入（POST /down）兩輪、沒帶 token 的 `status?check=1` 一次，都回 403 `token`。
- `up` 執行中再送 POST /down 回 409 `busy`。
- 外人 claim 下 `up p4` ⇒ rc 5 refused，0.1 s，knob 前後相同。
- （修前，不上圖）外人 claim 下 `up`（OVS 4）⇒ rc 0，fabric 建起來了——跑的是 `68ace017` 之前的 ndt，所以不是現在的碼的證據；是 ndt 的缺陷，不是 ndt serve 的。

**READ（讀 trunk 碼，未在 lab 上執行）**
- 八條防線的實作位置（上表）。
- Origin 檢查、無 CORS header：只有單元測試與讀碼（09-24 REPORT §4 表第 2 列明寫「沒用真的瀏覽器測過」），live 沒打過跨源請求。
- 一次性連結（600 s、用一次、最多 8 把）、dry_run 預覽：09-27 GUI 第一刀才加，**那一刀沒有 claim、沒有動 lab**
  （`doc/audit/2026-09-27_ndt-serve-gui/REPORT.md:10`；§4.3 的瀏覽器實測是對 stub 伺服器 `127.0.0.1:18765`、stub ndt、測試 token）。
- apps／cells 的 own-claim 檢查：cells 版 `8f2fbb5b` 在 09-24 live 之後（15:22Z）才進；apps 版 `475b1036` 是 09-27 08:27Z。兩者都只有單元測試＋變異。
- OVS 的 rc 5：`68ace017`（09-25 12:23Z）讓 `up_ovs` 呼叫 `guard_up_lab_free`（ndt:4362）。**沒有找到它在 lab 上跑過的 raw**
  （ticket `doc/audit/2026-09-25_ndt-ovs-claim/TICKET-ndt-ovs-claim.md:24` 把 live 交給 orchestrator；找過的地方與方法見上表「OVS『not run live』」那一列）。

**INFERRED（推論，未驗證）**
- 「別的機器連不到」是由「只有 127.0.0.1 listener」推得的；沒有從另一台機器實際連過。
- CSRF 的防護靠「自訂 header 讓瀏覽器必須先 preflight，而伺服器從不回 preflight」，這是依 Fetch 規格推的（serve.py:23-24 自己也這樣寫）。

## 圖怎麼讀

- 左欄是威脅（短語），中欄 **READ THE CODE** 是對應的防線，右欄 **RAN IT · live 09-24 (UTC)** 是那天在真 lab 上看到的回應（日期由腳本從 raw 第一行的時間戳換成 UTC）。
- 右欄綠＝防線擋住了（值是 raw 裡的 HTTP 碼／rc 與 `error` 欄）；白框「not run live」＝沒有 live 證據，**不代表壞**。圖例只有這兩種。
- 「someone else's claim: up/down」那列右欄分兩半：P4 rc 5（09-24 live，擋住）、OVS「not run live」。中欄是 HEAD 的碼：P4 與 OVS 都由 ndt 回 rc 5。
- 與 `fig_s1_serve_path` 的關係：s1 畫請求走的路，本圖把同一批閘門換成「擋誰」的角度，並分開「跑過」與「讀過」。

## 已知但書

- **時間差**：右欄是 09-24 的 serve 碼（`a139bceb`、`c836cff0`），中欄是 09-27 之後的碼（`f186ce98`）。
  Host／token／busy 三條在兩個版本之間的實作沒有改變語意（`_check_host`、`SLOT` 在 `fff032ea` 就有；`_check_origin` 在 `c836cff0` 成為函式），但**嚴格說 live 驗的是舊版**。
- **OVS 那半格為什麼是「not run live」**：09-24 唯一一筆 OVS 紀錄（上表「修前」列，rc 0、fabric 建起來）跑的是修法之前的 ndt；ndt serve 對 up/down 本來就交給 ndt 的 guard（serve.py:381-384）。
  09-24 的 ndt help 說 up 在 lab 被別人 claim 時回 5，當時只對 P4 成立（`doc/audit/2026-09-24_ndt-serve/REPORT.md:47`）；REPORT.md:6 的 09-26 補註說明自 `68ace017` 起兩個平面都成立。
  修法之後沒有 live 紀錄，所以圖上不畫那一筆，也不畫 rc 5——兩者都不是現在的碼跑出來的。
- **「沒有 claim」時**：ndt 讓 up/down 照跑，頁面比 ndt 嚴（要求 claim 是你的，serve.py:382-383）；這是頁面層的 UI guard，**伺服器端沒有替 up/down 加 own-claim 檢查**。
- 對帳舊結果：09-24 REPORT §4 的表（`REPORT.md:180-188`）列的 live 證據與本圖右欄的綠格一致；本圖沒有推翻它，OVS 那一筆修前的紀錄照舊成立、只是不上圖（v1.8），09-25 的 OVS 修正（讀碼）在中欄。
- 背景（非本圖證據）：09-27 15:52Z 我在這台筆電 `ss -ltnH 'sport = :8765'` 是空的（ndt serve 目前沒在跑），raw `_raw/ss-listen-3000-8765-20260927.txt`。
- 避免說法：不要說「ndt serve 已經安全了」或「做過滲透測試」；只能說「八條防線在碼裡，五條在 09-24 的真 lab 上看過擋住（up/down 那條只看過 P4）；OVS 的 up 在碼裡同樣被擋，沒有在 lab 上跑過」。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/ndt-serve"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_serve_s2_s4.py --only fig_s2_security_model
```
（不帶 `--only` 一支產三張：`fig_s2_security_model`、`fig_s3_cells_and_walks`、`fig_s4_gui_plan`；事實檢查不論如何都整份跑。09-27 那次三張一起產的輸出在 `_raw/last-run.log`。）

最後產出：2026-09-29T08:12Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_serve_s2_s4.py` sha256 `22860412cca400bb…`（產圖之後腳本沒再改過）；重生紀錄 `K/scratch/overnight-2026-09-05/logs/slides930/regen-v18-serve-20260929T0812Z.log`（只重畫本圖，`fig_s3`、`fig_s4` 沒動）。PNG sha256 300 dpi `01dcbd9fdc8b86a6…`、500 dpi `0d70f20812e96069…`（v1.7 是 `5d69797ba5f41d0c…`／`316a49083827119b…`）；畫布大小不變（13.33 × 7.0 in）。

修訂：2026-09-27 17:05Z（judge F-18 全改 UTC、F-20 red-check 移出 scratchpad、F-16 補髒 checkout 註記；圖面只改 RAN IT 標頭加 `(UTC)`）。
2026-09-29 v1.8：up/down 那一列只畫最後狀態——中欄「P4 and OVS」（拿掉「since 09-25」）、右欄 OVS 半格改成「not run live」（拿掉修前的 rc 0 紅格）、圖例拿掉「did not hold」；新增三組停止條件（見上）。
