# fig_s4_gui_plan —— ndt serve 的頁面往哪走：v1 已併、v2 已裁、與 Web-GUI 合一未排

[Co-developed with claude code -- Adam]

> **2026-09-27 17:05Z：投影片上這一頁改成表格頁（judge F-13，coordinator 裁定）**——圖上的狀態字樣（merged／ruled · on a branch／not scheduled／resolve first／red lines: open question）屬於判語式標籤。
> 表格內容由 integrator 放進模板；本圖留作存檔，不刪。
>
> 本檔所有日期時間都是 **UTC**（judge F-18）。

## 一句話

**v1**（09-27 12:35Z 併入 `f186ce98`）是 ndt serve 自己送出的三個靜態檔、手動更新；**v2**（Adam 09-27 約 13:1xZ 裁定）改用 Web-GUI 的技術棧
（React · Vite · Tailwind · TypeScript · i18next），**仍然由 ndt serve 送出、紅線不變**，每 10 秒自動更新、量測中暫停——
截至 09-27 17:03Z 分支上有三個 commit（範圍草案、ndt serve 伺服器端的準備、headless Chrome 測試驅動），**頁面本身還沒開始**、未併入；**長期**要和 Web-GUI 合成一個 app，**沒有排程**，而且得先解決
Web-GUI 對外開 `0.0.0.0:3000` 與 ndt serve 只聽 `127.0.0.1` 的衝突。整張圖都是**讀碼／讀裁定**，沒有量測。

## 資料來源

| 用途 | 檔（path:line 或 JSON key） | commit／binary |
|---|---|---|
| v1：三個靜態檔、由 ndt serve 送 | `tools/ndt_serve/serve.py:84-86` `STATIC`（`/`、`/app.js`、`/app.css`）、`:453-458`（Host 檢查之後、token 之前送出，不執行任何東西）；`git ls-tree f186ce98 tools/ndt_serve/static` ＝ `app.css`、`app.js`、`index.html`（124／638／50 行） | 合併 `f186ce98`（2026-09-27 12:35:38Z，兩個 parent）；HEAD `fed37cff` 的 `tools/ndt_serve` 與它相同 |
| v1：手動更新 | `scratch/overnight-2026-09-05/logs/orchestrator-0924/intake-0926/RULINGS-0927-ndtserve-gui-scope.md:16`（第 6 題「manual only in this cut」）；`tools/ndt_serve/static/app.js` 沒有 `setInterval`（腳本斷言）；只有打開中的 job log 每 2 s 重讀（`app.js:433`），關掉或頁面隱藏就停 | 同上 |
| v1 的依據 | `RULINGS-0927-ndtserve-gui-scope.md:4`（Adam 09-27 約 05:2xZ 的裁定 H：頁面由 ndt serve 自己送；token 走一次性 URL `#fragment`） | 裁定檔，scratch，未提交 |
| v2：技術棧、仍在 ndt serve 裡、紅線不變 | `…/intake-0926/RULINGS-0927-ndtserve-gui-v2.md:22-27`（R1） | 同上 |
| v2：10 s 自動更新、量測中暫停 | `RULINGS-0927-ndtserve-gui-v2.md:28-30`（R2，取代 scope 裁定的「只能手動」） | 同上 |
| v2 的裁定日期 | `RULINGS-0927-ndtserve-gui-v2.md:1`（檔內寫「2026-09-27 ~21:1x」＝+08，即約 13:1xZ；互動表單） | 同上 |
| v2 走到哪 | 分支 `feat/ndt-serve-gui-v2-0927`（worktree `scratch/overnight-2026-09-05/wt-ndt-serve-gui-v2-0927`）上不在 trunk 的 commit 共三個：`0d7f6ce8`（09-27 15:53:20Z）範圍草案 `doc/audit/2026-09-27_ndt-serve-gui/SCOPE-v2.md`（310 行，自述「For review before any code」）；`f3a20447`（16:20:54Z）「ndt serve: Web-GUI link setting, safer `url`, OWN_CLAIM pinned to ndt」改 `tools/ndt_serve/serve.py` 與三個測試檔；`6d5621ab`（16:36:32Z）`tests/browser/cdp_pipe.py`（DevTools-protocol 驅動）。**沒有任何頁面檔**（`tools/ndt_serve/static/`、`package.json`、vite／tailwind 設定、`.ts/.tsx`）——腳本一看到頁面檔就停 | 腳本用 `git for-each-ref`／`git log <branch> --not trunk`／`git show --name-only` 讀，唯讀 |
| 長期：與 Web-GUI 合一、未排程 | `RULINGS-0927-ndtserve-gui-v2.md:32-47`（R3；「not scheduled」在 :43） | 裁定檔 |
| 衝突：Web-GUI 對外 vs ndt serve 只聽本機 | `RULINGS-0927-ndtserve-gui-v2.md:44-46`；`~/Web-GUI/docker-compose.yml:52-53`（`ports: - '3000:3000'`，沒寫主機位址） | Web-GUI `f63a55c`（`~/Web-GUI` HEAD，唯讀） |
| Web-GUI 的技術棧真的是那五樣 | `~/Web-GUI/package.json:23`（`i18next ^25.3.2`）、`:26`（`react ^19.1.0`）、`:52`（`tailwindcss ^3.4.17`）、`:53`（`typescript ~5.8.3`）、`:55`（`vite ^6.3.5`） | 同上 |
| 紅線（下方藍帶） | `serve.py:72`（`BIND`）、`:484-499`（token 每次都查）、`:94`＋`:601-617`（一次性連結）、`:404-406`（無 CORS）；v2 裁定 :23 明寫紅線不變 | `f186ce98` |

## 可信度

**OBSERVED**
- 09-27 15:52Z 本機 `ss -ltnH 'sport = :3000'` 有兩個 listener：`0.0.0.0:3000` 與 `[::]:3000`（`_raw/ss-listen-3000-8765-20260927.txt`，我存的，未提交）。
  **沒帶 `-p`、也沒 sudo，所以沒認出是哪個行程**；說它是 Web-GUI 的 docker-proxy 是推論。圖上的 `0.0.0.0:3000` 取自裁定檔，不取自這筆。
- v2 分支在我作業期間長出來（git refs，唯讀）：15:53Z 只有範圍草案（當時標「scope draft only」），16:20Z／16:36Z 又多了伺服器端與測試驅動的 commit，
  17:03Z 重生時腳本依檔案種類判成「on a branch, no page yet」。**狀態還在變，09-30 前要重跑。**

**READ**
- v1 的結構（三個靜態檔、由 ndt serve 送、手動更新）——讀 `serve.py`、`app.js`、scope 裁定。
- v2 的技術棧、仍在 ndt serve 內、紅線不變、10 s 更新量測中暫停——讀 v2 裁定 R1／R2。
- 長期合一、未排程、要先解決的衝突與三個候選解法（Web-GUI 只聽本機、加登入、加一個有自己驗證的 proxy）——讀 v2 裁定 R3。
- Web-GUI 用的技術棧——讀 `~/Web-GUI/package.json`。

**INFERRED**
- 「`'3000:3000'` 沒寫主機位址 ⇒ Docker 會綁在所有介面」是 Docker 的預設行為，我沒有在這台機器上驗證是哪個行程在聽（見上）。
- v2 何時開工、何時完成：沒有任何排程資料，不推測。

## 圖怎麼讀

- 三個框由左到右：現在（v1）→ 已裁定的下一版（v2）→ 長期（與 Web-GUI 合一）。框上方的點與字是狀態：
  綠＝已併入（日期是合併 commit 的日期）、黃＝已裁定＋目前進度、灰＝沒有排程。
- 第三個框裡紅藍兩個小框是它必須先解決的衝突：Web-GUI 對外開 `:3000`，ndt serve 只聽 `127.0.0.1`。
- 下方藍帶橫跨 v1 與 v2：兩版共用同一組紅線（只聽本機、每次帶 token、一次性連結、不開 CORS）；
  第三個框下的紅色虛線框：合一之後紅線怎麼守，還沒有答案。

## 已知但書

- **GUI 第一刀（v1）沒有 live run**：`doc/audit/2026-09-27_ndt-serve-gui/REPORT.md:10`「這一刀沒有 claim、沒有動 lab」；§4.3（`REPORT.md:225-249`）的瀏覽器實測是對 stub 伺服器 `127.0.0.1:18765`、stub ndt、測試 token，
  點的是 `e4f7c036` 那版 app.js，之後 `9a6eb7f1`、`cf053502` 兩處改動沒有在瀏覽器裡重點過。
  09-27 12:59Z Adam 的 state 目錄（`~/.local/state/ndt-serve/guided/g20260927T125927Z-029ded.json`）有一條建立了但一步都沒走的 walk（全部 `pending`）——**沒有任何東西在 lab 上跑**。
- v1 的 UI 是英文標籤（scope 裁定第 2 題，`RULINGS-…-scope.md:12`）；v2 改成中文預設、字串表（v2 裁定第 5 點，`:11`）。
- v2 的「copy Web-GUI's components」：`SCOPE-v2.md` §0 更正說 Web-GUI 可直接抄的共用元件只有三個，實際是照樣式重寫（分支上的草案，未審）。
- 合一會動到公開的 Web-GUI repo，需要 PR 與別人的審查（v2 裁定 :47）。
- 這張圖的狀態標籤會過期：腳本在 v2 分支出現頁面檔時會停下，要改標籤才能重生。**09-30 報告前要重跑一次**（表格版同理）。
- 對帳舊結果：09-16 報告沒有這一頁（ndt serve 是 09-24 才開的單）；本圖不推翻任何舊圖。
- 避免說法：不要說「GUI 已經在 lab 上驗過」；不要說「v2 頁面已經在做」（分支上只有草案、伺服器端準備與測試驅動）；不要說「會和 Web-GUI 合併」而不加「沒有排程、要先解決對外開放的問題」。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/ndt-serve"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_serve_s2_s4.py
```

最後產出：2026-09-27T19:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_serve_s2_s4.py` sha256 `2f79ae137d352705…`（產圖之後腳本沒再改過）。

修訂：2026-09-27 17:05Z（judge F-13：改成表格頁、本圖退出 deck；F-18 全改 UTC；v2 狀態改為「on a branch, no page yet」）。
