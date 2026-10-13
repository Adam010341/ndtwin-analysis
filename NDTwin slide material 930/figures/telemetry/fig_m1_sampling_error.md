# `fig_m1_sampling_error` —— 兩條遙測路徑，同一個 fabric 的取樣誤差

[Co-developed with claude code -- Adam]

（本檔所有時間為 UTC。）

## 一句話

同一個 10 台 bmv2 fabric、同一條 h1→h4 路徑，只換遙測來源：
`cooperative`（P4 pipeline 在交換機內 1/256 clone 到 CPU port，proxy 合成 sFlow）與 `link`（交換機側 veth 上 `tc … sample rate 256`，root emitter 合成 sFlow）。
twin 讀到的鏈路使用率對介面計數器的誤差中位數：20 與 100 Mbit/s 兩條路都在 1.5–3.4%；**2 Mbit/s 時 cooperative 29.5%、link 7.5%**。
色帶＝只由 1/256 取樣本身就會產生的誤差範圍（shot-noise 預測 ×[0.5, 2]）。
空心點＝落在帶外（只有 cooperative 2 Mbit/s：29.5% 對帶頂 28.5%）；圖上把帶頂畫成短橫線並標值。

## 資料來源（腳本執行時讀取）

K＝`/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-19_telemetry-three-groups`

| 用途 | 檔（JSON key） | binary |
|---|---|---|
| 六個點與六條帶 | `K/raw/2026-09-19T115737Z_full/summary.json`：`sampling_error_by_group[group=cooperative|link]["H-B1"].rates[*].{offered_mbit, median_abs_error, band}` | kernel sha256 `be70b5dd3235684786dc…`、bmv2 `/usr/local/bmv2-fast/bin/simple_switch_grpc` sha256 `3ff54b5c1901c9d3…`——各取自該序列**自己那一代**的 arm.meta：cooperative＝`K/raw/2026-09-19T115737Z_full/G2/cooperative_f64_a/arm.meta:12-15`（起跑 12:16:08Z，`:5`）、link＝`K/raw/2026-09-19T115737Z_full/G3/link_f64_a/arm.meta:12-15`（起跑 12:26:50Z）；兩個 sampling-error 視窗與該 arm 同一次 bring-up（各代的 `10_up.txt`）。腳本讀這兩份並斷言兩代是同一組 binary（`binaries()`） |
| 對帳（不畫） | 同檔 `sampling_error_cross_group_registered.rates[*].ratio`：link/coop＝0.253、1.255、1.489；腳本斷言與圖上的點算出來的比值相同 | 同上 |
| 空心／實心 | 同檔 `…rates[*].position`（`above`／`inside`）；腳本自己用帶算一次，與檔內欄位不同就停 | 同上 |
| 三組的定義 | `K/PREREG.md:26-34` | — |
| 結論與判決 | `K/FINDINGS.md:120-126`（§3，組級判決）；trunk commit `611a08d3`（FINDINGS 最後一次改動，2026-09-24 12:13Z） | — |

值（腳本印出，與 summary.json 相同）：

| 速率 | cooperative | link | shot-noise 帶（cooperative；link 在 20／100 M 用 N＝5 條邊算，見但書） |
|---|---|---|---|
| 2 Mbit/s | 0.2953 | 0.0746 | [0.0713, 0.2853] |
| 20 Mbit/s | 0.0274 | 0.0344 | coop [0.0226, 0.0902]／link [0.0202, 0.0807] |
| 100 Mbit/s | 0.0154 | 0.0229 | coop [0.0101, 0.0404]／link [0.0090, 0.0361] |

## 可信度

**OBSERVED**：六個點（第五次 campaign，2026-09-19 11:57Z 起跑，`driver.log:1`；`invalid_arms` 空）。cooperative 的點來自 `G2/se_cooperative_*`、link 的點來自 `G3/se_link_*`。
raw 在 trunk 被 `.gitignore:84` 擋著（`doc/audit/**/raw*/*`），但在 **audit-raw `797c34ab`**（兩個 P4 repo 公開，coordinator 09-27 推）：本檔引用的 raw 檔（`summary.json`、G2／G3 兩份 arm.meta、下面 pps 那段的 `.log` 與它的 arm.meta）以 `git rev-parse 797c34ab:<path>` 對 `git hash-object` 逐檔比過，blob 相同（2026-09-27 17:0xZ 與 18:4xZ，本機唯讀）。

**髒 checkout**：這輪各世代的 `11_verify.txt:17` 都寫 `code 4d3f294f +60 file(s) with uncommitted changes`（G2、G3、G4、G5、G6；G1 是 `f4dd9f22 +60`，G1 不在本圖）。kernel 與 bmv2 以 sha256 指認（上表），不是以 commit 指認。

**READ**：色帶的定義（PREREG §5.2 註冊的 shot-noise 預測）。

**INFERRED**：無。

## 圖怎麼讀、要講的判決（組級，FINDINGS §3）

- `link`：三個速率都在帶內 ⇒ **H-B1 成立**（誤差就是取樣本身的雜訊）。
- `cooperative`：2 M 在帶**上方**、20／100 M 在帶內 ⇒ H-B1 不成立、H-B2 也不成立——這是 PREREG **沒有註冊的結局**，照規定**只報數字、不貼標籤**（FINDINGS `:126`）。
- 兩條路一樣準（H-B4）**不成立**：2 M 的 link/coop＝0.253，落在 [0.5, 2.0] 外。

## 已知但書（講者備註要講）

- 🔴 **pps 天花板這一題在這台機器上量不出來，所以不畫、不給倍數。** 依據（raw＋binary）：
  判別輪 `K/raw/2026-09-19T130352Z_G2/G2/cooperative_f64_a.log` 同一臂同一階 20 kpps——爬梯時 3 次中位數 0.2532%（`:8`，clean=yes），
  確認時 3 次中位數 0.5276%（`:15` 與 `:17` 的 `top_rung_confirmation=20:0.5276,0.8063,0.0000`，不過 0.5% 門檻）。
  binary：kernel sha256 `be70b5dd3235684786dc…`（`arm.meta` 的 `kernel_sha256_start` 與同 log `:18` 的 `kernel_sha256_end` 相同）、bmv2 `simple_switch_grpc` sha256 `3ff54b5c1901c9d3…`（`…/cooperative_f64_a/arm.meta`）；arm 起跑 2026-09-19T13:07:34Z；code `4d3f294f +60`（`K/raw/2026-09-19T130352Z_G2/G2/11_verify.txt:17`）。
  同一個門檻落在同一階的重複量測之間 ⇒ **不可以說「遙測把 pps 天花板壓低 N 倍」**。
- CPU 也不畫：FINDINGS §4 的 per-rung 時間窗有勘誤（`d39959ba`，2026-09-24 13:06Z），要引只能引勘誤後的值，而且那不是這頁的題目。
- 取樣誤差只在一個世代量、每格 3 個視窗（FINDINGS 威脅 1）。link 20／100 M 的帶用 N＝5 條邊算；改用註冊的 4 條邊，判決不變（FINDINGS `:127`）。
- 🔴 這些數字**全在 protobuf 5 切換（`5dc7fc9a`，2026-09-27）之前**量的；不能和切換之後的任何效能數字放在同一張圖。
- 這是 NDTwin 自己的 fabric（`ndt up p4 4 --telemetry <組>`），不是外來 P4 exercise 的 fabric。

## 重生指令

```bash
cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/telemetry"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_sampling_error_fig.py
```

紅檢（腳本的 **6 個**停止條件都看過紅——7 個竄改，`position` 兩個方向各一；對照組綠）：`/home/adam/Desktop/NDTwin-Kernel/scratch/overnight-2026-09-05/logs/slides930/m1-sampling-error-redcheck.sh`
與 `…/m1-sampling-error-redcheck-r2b-20260927T1854Z.log`（最終腳本 sha256 `a5c1dcb236d297a8…`；同腳本的前一跑 `…-r2-20260927T1843Z.log`；control rc=0；`position` 兩向竄改、ratio 竄改、`invalid_arms` 非空、速率不是 2／20／100、G2 的 kernel sha 換掉、G3 的 bmv2 sha 拿掉，各 rc=1，且印出對應原因）。
第一輪 `…/m1-sampling-error-redcheck-20260927T1710Z.log`（舊腳本 `b88a22e0…`，4 個）保留作紀錄。

## 判官修正（2026-09-27 UTC；F-14、F-16、F-18、F-20）

- F-14：拿掉 pps 天花板的前後對比數字；0.2532%／0.5276% 改引 raw＋binary（上面）；29.5% 改成空心點、帶頂 28.5% 畫出並標值，看得出在帶外。
- F-16：補髒 checkout 行。F-18：時間改 UTC（原本寫的是 +08 時間）。F-20：紅檢移到 kernel `scratch/…/slides930/`（git-ignored）。
- 第二輪（2026-09-27 UTC，coordinator 第 10、11 項）：binary 改引各序列自己那一代的 arm.meta（原本引的是 G4 的 link_f64_b），並由腳本斷言；補「速率不是 2／20／100」與兩個 binary 停止條件的紅。

最後產出：2026-09-27T19:51Z（PNG 檔時間，UTC）；matplotlib 3.11.1；產生器 `make_sampling_error_fig.py` sha256 `a5c1dcb236d297a8…`（產圖之後腳本沒再改過）。
