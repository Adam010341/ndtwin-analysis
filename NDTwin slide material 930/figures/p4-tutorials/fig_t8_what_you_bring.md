# fig_t8_what_you_bring —— exercise 作者帶什麼來，convert.py 補什麼

[Co-developed with claude code -- Adam]

## 一句話

作者帶來的是 exercise 資料夾本來就有的東西：自己的 `.p4`、`make`／p4c 編出來的 bmv2 json 與 p4info、`topology.json`、
每台交換機的 `sN-runtime.json`，外加（可選）自己的控制器 `mycontroller.py`；
`convert.py` 把前四樣原路徑照抄進 package，再補兩個 NDTwin 自己的檔：`package.json`（合約）與 `ndtwin/topology.json`（NDTwin 的拓樸模型）。
以 09-27 那輪的 basic 解答臂為例，package 共 10 個檔＝8 個副本＋2 個新檔。

## 資料來源

R ＝ `/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep/runs`；
C ＝ `/home/adam/Desktop/NDTwin-Kernel/tools/p4_exercise/convert.py`（trunk `fed37cff`，與 `3d740be0` 相同；最後改動 `f5cd934b`）。

| 用途（圖上的值或框） | 檔（path:line 或 JSON key） | commit／binary |
|---|---|---|
| 「PACKAGE · 10 files」與 10 個檔名 | `R/2026-09-27T074826Z_basic_solution_ndtwin.md:78-88`（N1 convert.py 的輸出，`files : 10`） | T06 站在 `5dc7fc9a`（同檔 `:446` code 行） |
| 「8 copies, same paths」 | 同上 10 個檔名扣掉 `package.json`、`ndtwin/topology.json`；「原路徑照抄」＝`C:763-777` `write()` 的 `shutil.copyfile(abs_src, dest)`，dest 是 exercise 內的相對路徑（`C:18-29` docstring 說明為什麼保留原路徑） | — |
| 「new」兩個檔 | `C:786`（`written.append("ndtwin/topology.json")`）、`C:789`（`written.append("package.json")`） | — |
| 左邊四個框各是哪一類 | `C:465`（copies 先放 topology）、`C:480`（每台的 runtime json）、`C:508`（`.p4`）、`C:515`（`build/<stem>.json`、`build/<stem>.p4.p4info.txtpb`，只在已經 make 過時才有） | — |
| `pod-topo/s1…s4-runtime.json` 的「4」 | 同一份 convert 輸出裡 `pod-topo/sN-runtime.json` 的個數 | — |
| 「read back: ok」 | `…basic_solution_ndtwin.md:89`（`read back through p4_proxy/mininet/topo_from_json.py: ok`）；`C:806` `read_back(model)` | — |
| `mycontroller.py`「optional · 2 of 13」 | T06 13 支解答臂的 convert 輸出裡 `control plane : external` 的只有 p4runtime（`R/2026-09-27T081205Z_p4runtime_solution_ndtwin.md:76`）與 flowcache（`R/2026-09-27T081256Z_flowcache_solution_ndtwin.md:76`） | — |
| 「name recorded, not copied」 | `C:502`（`"controller": "mycontroller.py" if mode == "external" else None`，寫進 `package.json` 的 `source.controller`）；`C:461`（mode auto ＝ 有 `mycontroller.py` 就是 external）；p4runtime、flowcache 的 files 清單裡都沒有 `mycontroller.py`（上兩檔 `:79-86`） | — |

## 可信度

**OBSERVED（跑過，convert.py 在 T06 的真實輸出）**
- basic 解答臂的 package 是 10 個檔，檔名如圖；read back ok。
- 13 支裡 2 支（p4runtime、flowcache）的 control plane 是 external，而且它們的 package 檔案清單裡沒有 `mycontroller.py`。
- 13 支解答臂的 package 是 6–12 個檔（腳本印出，圖上沒放）。
- 以上 arm report 都在 **audit-raw `797c34ab`**（與工作樹比 blob hash 相同）。

**READ（讀碼，沒有執行）**
- 哪些是「照抄」、哪些是「新寫」，以及控制器「只記名字、不複製」：`convert.py` 的 `plan()`／`write()`（上表行號；腳本逐字斷言那幾行還在）。
- 「build/*.json 與 p4info 是 p4c 的輸出」：`C:31-35` docstring（沒 make 過的 exercise 會被拒，並給 make 指令）。
  T06 裡這兩個檔是 driver 在 convert 之前自己用 p4c 編的（arm report §2），不是 convert 編的。

**INFERRED**
- 「作者帶來的」這個說法是我的框法：exercise 資料夾原本就有、convert 不改內容的那些檔。不是碼裡的名詞。

## 圖怎麼讀

- 左框＝exercise 資料夾（以 basic 為例）：四類檔，最下面虛線框是可選的控制器。
- 中間＝`convert.py`，它最後把寫出的模型讀回來一次（read back: ok）。
- 右框＝package：上面一格是 8 個照抄的副本（路徑不變），下面兩格藍底是 NDTwin 新寫的兩個檔。
- 虛線箭頭：有控制器的 exercise，convert 只把 `mycontroller.py` 這個名字記進 `package.json`，不複製檔案；控制器在跑的時候由 driver 從 exercise 資料夾啟動。

## 已知但書

- **髒 checkout（F-16）**：`…basic_solution_ndtwin.md:446-450` 的 code 行是 `5dc7fc9a +95 file(s)`，其中 3 個會改行為。圖上沒有印 sha。
- 例子是 basic 解答臂；別的 exercise 的清單不同：firewall 有兩份程式（`build/firewall.json`＋`build/basic.json`，12 個檔），
  p4runtime／flowcache 沒有 runtime json（控制器自己寫表，6 個檔）。
- 「控制器由 driver 經 `tools/p4_exercise/run_external_controller.py` 啟動」：`drive_exercise.py:1601,1619`（READ）；那支 adapter 改寫 tutorials 寫死的 gRPC 位址（GAP-2b §1 `control_plane_mode` 列，轉述；GAP-2b 未提交，待 Adam 審，我沒有逐行讀 adapter）。
- 這一頁只講 package 長什麼樣；它能不能跑，看 fig_t7（pre-flight）與 fig_t6（一支從頭到尾）。
- 不要說成「NDTwin 可以操作任何外來 P4 程式」：external 模式的 detect-only 部分還沒做完。

- 紅測（mutation check）與產圖紀錄：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/o1-o2-t6-t9/`（`run_mutations.py`、`run_mutations.log` 14/14 照預期、`gen_overview.log`、`gen_p4tutorials.log`、各 mutant 輸入檔）。

## 重生指令

```
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/p4-tutorials"
nice -n 10 "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" make_exercise_path_figs.py
```

最後產出：2026-09-27T17:05Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_exercise_path_figs.py` sha256 `6b2d5e08ced9bb91…`（產圖之後腳本沒再改過）。
