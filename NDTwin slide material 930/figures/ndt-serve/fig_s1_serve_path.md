# `fig_s1_serve_path` —— ndt serve：進實驗室的一扇本機門

[Co-developed with claude code -- Adam]

（本檔所有時間為 UTC。）

## 一句話

`ndt serve` 把 `ndt` 的實驗室動作包成一個只聽 127.0.0.1 的本機 HTTP 服務與網頁：瀏覽器拿一次性網址換 token，
每個請求都要帶 token 且同源；寫入前可以先預覽**將要執行的那一行 ndt 指令**；一次只跑一個工作，
app 起停與 lab cell 要你**自己持有 claim**（伺服器端檢查），`up`／`down` 交給 `ndt` 自己的守衛（別人持有 claim 時回 rc 5）。

## 資料來源（READ，trunk `3d740be0`；`tools/ndt_serve/` 在 `fed37cff` 相同——`git diff --stat 3d740be0 fed37cff` 只動 `tests/python/test_ndt_serve.py`；圖上兩個字面值由腳本從碼讀出）

K＝`/home/adam/Desktop/NDTwin-Kernel/tools/ndt_serve`

| 方塊 | 檔:行 |
|---|---|
| 只綁 127.0.0.1、預設 port 8765 | `K/serve.py:72`（`BIND = "127.0.0.1"`）、`:1163`（`--port` 預設 8765） |
| 一次性網址 `#k=<nonce>` | `K/serve.py:187-188`（`page_url`）、`:94`（`NONCE_TTL_S = 600`，一次、600 s）、`:601-617`（`POST /api/v1/session` 用 nonce 換 token） |
| 每個請求帶 token＋同源 | `K/serve.py:73`（`TOKEN_HEADER = "X-NDT-Token"`）、`:18-19`（說明：除 `/health` 與三個靜態檔） |
| 預覽確切指令 | `K/serve.py:359-392`（`{"dry_run": true}` 回 verbs.py 組出的 argv，不執行） |
| 一次一個工作、你的 claim？ | `K/serve.py:703-721`（工作槽，已有工作就 409 busy）、`:787-811`（`_require_own_claim`：`ndt status` 的 claim 行必須完全符合 `yours -- Nm left (until HH:MM:SS)`，`:1031`） |
| ndt 的動詞 | `K/verbs.py:65-86`（up 4／up ovs／up p4 [N]／up p4 --app）、`:125-128`（down）、`:131-144`（claim）、`:147-150`（release）、`:153-161`（apps／apps stop） |
| 工作紀錄回網頁 | `K/serve.py:33`（setsid、記在磁碟上）；頁面每 2 s 輪詢工作 log（GUI v1 的 `static/app.js`，merge `f186ce98` 的說明） |

## 可信度

**READ**：整張圖（架構圖）。

**OBSERVED（佐證，2026-09-24，不在圖上）**：只有一個 listener `LISTEN 127.0.0.1:8765`、token 檔 0600（`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/ndt-serve-0924/live-fixes-20260924T2249/01-listen-and-token.txt`，檔內 `22:49:21+08:00`＝14:49:21Z；目錄名是 +08 時間）；別人持有 claim 時 P4 平面 `up` 回 rc 5（同目錄 `a2/`）；11 步 API 跑法與直接跑 `ndt` 逐步一致（`…/live-20260924T2201/compare.md`，目錄名 22:01 +08＝14:01Z）。這些 live 跑在 09-24 的 `ndt` blob `3273df8b`。
**髒 checkout**：驅動的 ndt 在主 checkout `fd7382a3`，有 60 個檔未提交，其中 2 個可改變行為（`p4_proxy/mininet/host_count_override`、`tools/remote-lab/dorm_lab/`）；ndt 檔本身未改（sha256 `cb134ccc…`＝blob `3273df8b`）。解析與斷言見 `fig_s2_live_cells.md` 的髒 checkout 段（S 組 worker 的腳本）。

**INFERRED**：無。

## 已知但書

- 🔴 **GUI 這一刀（`f186ce98`，2026-09-27 12:35Z）沒有任何 live run**：沒有 claim、沒碰 lab，只在瀏覽器對著 stub server（127.0.0.1:18765）點過（`/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-27_ndt-serve-gui/REPORT.md:10`、`:225-245`）。
- merge：API＋cells＋walks `48209682`（2026-09-26 00:05Z）；GUI v1 `f186ce98`（2026-09-27 12:35Z）；claim-note 測試不再依賴 TMPDIR 長度 `fed37cff`（2026-09-27 15:47Z，只動測試）。
- GUI v2（React＋Vite，Web-GUI 的 stack）在分支 `feat/ndt-serve-gui-v2-0927` 上，**還沒有頁面檔、未併**；見 S4 表格頁。
- `up`／`down` 的 claim 檢查是 `ndt` 自己的（serve 不重複檢查）；serve 自己的 own-claim 檢查只管 app 起停與要 lab 的 cell。
- 沒有取消工作、沒有串流；`clean`／`check`／`ntg`／`--deep`／`--force` 沒有開放（`/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-24_ndt-serve/REPORT.md:194`）。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/ndt-serve"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_serve_diagram.py
```

## 判官修正（2026-09-27 UTC；F-11、F-16、F-18）

- F-11：原本寫 TMPDIR 修正「在分支、未併」已過時——它以 `fed37cff` 併入 trunk。圖面不變（圖上沒有這一項）。
- F-16：補髒 checkout 行。F-18：日期改 UTC。

最後產出：2026-09-27T15:42Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_serve_diagram.py` sha256 `c4034a2b8ed365f4…`（產圖之後腳本沒再改過）。
