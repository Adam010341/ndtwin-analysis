# NDTwin report deck -- 2026-10-21 -- "Why would a developer use NDTwin?" -- content template (DRAFT)

v0.2 draft, 2026-10-08 (UTC); matrix changes since v0.1 are logged in research/CHANGES_final.tsv. Single source of truth for page order, table contents, figure specs
and speaker notes. Format imitates NDTwin-slide-template-930.md (§0 rules, §1 page table, §2 per page).
Times in UTC.

Sources (all read for this draft):
- Matrix: research/matrix_final.json (sha256 0686db4d154b1eb7...), research/ROWS.json (d25c7b3994fcaf03...),
  research/CHANGES_final.tsv (75afe07aba7e5c68...), research/verify_ndtwin.tsv (47c566ab48811a0b...),
  research/verify_competitors.tsv (2b5b96d8d6ad30d8...). Competitor cells = READ of public material
  (commercial = vendor material, academic = paper/draft), accessed 2026-10-08. NDTwin cells = READ of code and
  docs at trunk 2ece656c (git commit sha, full 2ece656c4a280477209a09b6fb7a51304d38b8ff).
- NDTwin code/docs: K = /home/adam/Desktop/NDTwin-Kernel, read with `git show 2ece656c:<path>` (not the working
  tree). Sibling repos read at their HEAD commits: Energy-Saving-App 9facb78, Simulation-Platform-Manager
  b7efd93, Web-GUI f63a55c, Network-State-Recorder 850f61d, Traffic-Engineering-App f108c7c,
  Network-Traffic-Visualizer 9b56b30, Network-Traffic-Generator 6e3f388 (`git show HEAD:<path>`; their working
  trees have 1-4 uncommitted files each, not read).
- Defect tracker: K/doc/KNOWN-ISSUES.md@2ece656c (ids such as C-6 below). Its own header says entries can be
  stale; each id used here is cited with the code line or merge it rests on at 2ece656c (see §3).
- Hands-on (P10-P14, RAN unless marked): K/doc/audit/2026-10-08_why-ndtwin-handson/ = H: PHASE0_NOTES.txt,
  controls.tsv (kernel commit dcff37b6), congestion/ (TASK.txt, ARM_*.txt, PREREG.txt, results.tsv, SCORECARD.txt,
  results_supplementary.tsv, agents/; kernel commits 66e84f51 c3dd47c3 767a4b32 80a4e29f 98691518 9335b189
  65b14f46 90132fa1 ebc60595, local only), raw/ and congestion/raw/ (archived in the kernel repo's audit-raw
  branch, local commits ed24e5e5, 19daa00a, c6bf496e). Both runs and the supplementary rerun are complete:
  every run log ends with the fabric down and the results committed. Figures for P10 and P13 come from generator/make_p10_setup.py and make_p13_relief.py.
- Previous deck format: NDTwin slide material 930/NDTwin-slide-template-930.md.
- Figure specs: figures_spec/architecture.txt (P02), figures_spec/landscape.tsv (P04),
  figures_spec/problems.tsv (P17-P19, P20), figures_spec/roadmap.txt (P20).

[Co-developed with claude code -- Adam]

## 0. Rules (standing; carried over from 930 where they still apply, plus this deck's own)

1. ONE figure or ONE table per page (930 rule 2). No bullets, paragraphs, captions, kickers or verdict chips.
   The slide title is the only free text. Table cells are short "label -> value", never sentences.
   Every page has a `form:` in §1 (title / figure / table).
2. Figure pages: the figure fills the content area; its top-left title (<=45 chars) IS the slide title, not
   repeated by the generator (930 rule 3). Few words on figures: title, axes, value labels, box names, panel
   titles, a few key annotations. Derivations, caveats, methods and reconciliation go to the figure's .md and
   the §2 notes (CLAUDE.md; 930 rule 4).
3. Evidence classes, never mixed in one table or one sentence: RAN (OBSERVED, executed, with raw path and
   binary identity), READ (code or documents read, not executed), INFERRED. Pages 2-9 and 15-19 are READ;
   pages 10-14 are RAN (P10's topology is READ from files); page 20 is a plan (INFERRED from 17-19). If one figure must show both, use two
   titled panels (930 rule 5).
4. RAN pages identify the binary: repo sha (+N uncommitted files), kernel binary sha256 prefix, bmv2 binary
   sha256 prefix, P4 pipeline json sha256 prefix -- in notes and the figure .md, not on the canvas
   (930 v1.8 practice). Every RAN number is reconciled with earlier results (which result it updates or can
   be compared with).
5. No conference or journal names, no private repos, no development or debugging history, no mention of how
   the material was checked (no review/verification process words, no work-item numbers). Defect-tracker
   ids (KNOWN-ISSUES C-6 etc.) and path:line@2ece656c are allowed as evidence.
6. Titles: English, sentence case, <=45 characters (each checked in §1).
7. 🔴 Non-code problems are EXCLUDED from slides AND notes (Adam's ruling): maintainer or commit concentration,
   contributor counts, GitHub stars or community size, the state of the lab's official public README, the
   website's documentation coverage, which repository holds what. Consequences in this draft: maturity rows
   M4 (stars) and M5 (contributors) are dropped for ALL tools; M3 for NDTwin says only the release status of
   what is compared; documentation gaps are not listed as problems; the problems list is code only.
8. No sugarcoat: ⚠ and ◌ stay visible on pages 5-7 with a legend row; pages 16-19 state real technical
   problems plainly, each with evidence and a concrete fix plus rough cost; "disclose" only where a fix is
   infeasible, with the reason.
9. Fairness (say it on 5-7): NDTwin's own defect tracker is visible to us and competitors' are not, so ⚠ exists
   only for NDTwin; commercial cells rest on vendor material, academic cells on the paper/draft; a cell is
   about the documented feature, not about how well it works.
10. Visual: 827 §E2 palette and the 916/930 figure style (matplotlib, Liberation Sans). Persona colours are the
    same on pages 3, 5-7, 17-20 (control-app dev / P4 dev / operator), with a shape as second encoding.
11. Generators stop with a named reason on bad input and are red-checked before delivery (930 rule 10): a
    table generator stops if a §2 table cell differs from matrix_final.json; the roadmap generator stops if a
    problems.tsv rank is missing or duplicated.
12. Guards for the speaker (❌ = do not say):
    - ❌ "NDTwin operates any foreign P4 program" (930 guard, still in force). Say "13 tutorial exercises run on
      the NDTwin fabric"; own programs enter through the lab CLI `ndt up p4 --app`.
    - ❌ "NDTwin stays in sync with your production network". It mirrors a Mininet fabric it controls through
      its own Ryu app or P4 proxy; physical mode is coded, with no run on record.
    - ❌ any bmv2 rate in Mbit/s. The ceiling is in packets per second (KNOWN-ISSUES F-bmv2: 16x ambiguity).
    - ❌ "the what-if predicts congestion". The shipped simulator models switch power-off only; no comparison
      with measured traffic is on record.
    - ❌ hands-on numbers before the run that produced them is complete and archived.
    - ❌ "NDTwin is the only tool that stays synced live". ONOS+Mininet also keeps a live view of the fabric it
      controls (A1, A3 ●); on P04 both sit in the same row ("none" = no link to a network they do not control).

## 1. Page order (20 pages)

| # | id | title (= on-slide title) | chars | form | evidence | status |
|---|---|---|---|---|---|---|
| 1 | P01 | Why would a developer use NDTwin? | 33 | title | -- | ready |
| 2 | P02 | What NDTwin is, as built today | 30 | figure `arch/fig_p02_architecture` | READ | ready (architecture.txt; redraw of the 827 layout); last rendered 10:57Z |
| 3 | P03 | Three developers, three jobs | 28 | table | READ | ready |
| 4 | P04 | Where 16 tools sit: fidelity vs live link | 41 | figure `landscape/fig_p04_map` | READ | ready (landscape.tsv: one placement rule, 8 positions unsure); last rendered 05:06Z |
| 5 | P05 | Control-app developer: who does what | 36 | table | READ | ready |
| 6 | P06 | P4-program developer: who does what | 35 | table | READ | ready |
| 7 | P07 | Network operator: who does what | 31 | table | READ | ready (contested cells ruled, §3) |
| 8 | P08 | Self-hosted tools: license, scale, interface | 44 | table | READ | ready |
| 9 | P09 | Commercial and academic: public material only | 45 | table | READ | ready |
| 10 | P10 | Hands-on: one task, two setups | 30 | figure `handson/fig_p10_setup` | READ (topology files) | ready (make_p10_setup.py; task = congestion relief, H/congestion/TASK.txt) |
| 11 | P11 | What each side had to build | 27 | table | RAN | ready (binary disclosure accepted, Adam 2026-10-08; both apps, cloc per line range) |
| 12 | P12 | Effort, measured | 16 | table | RAN | ready (binary disclosure accepted, Adam 2026-10-08; pre-registered metrics, SCORECARD.txt) |
| 13 | P13 | Time to relief after the trigger | 32 | figure `handson/fig_p13_relief` | RAN | ready (binary disclosure accepted, Adam 2026-10-08; make_p13_relief.py; both panels) |
| 14 | P14 | The same app, unchanged, on bmv2 | 32 | table | RAN | ready (binary disclosure accepted, Adam 2026-10-08; results.tsv, app logs) |
| 15 | P15 | When NDTwin is the right pick | 29 | table | READ | ready |
| 16 | P16 | When NDTwin is the wrong pick | 29 | table | READ | ready |
| 17 | P17 | Real problems, ranked: 1-6 | 26 | table | READ | ready |
| 18 | P18 | Real problems, ranked: 7-12 | 27 | table | READ | ready (rank 12 is new, 2026-10-08) |
| 19 | P19 | Real problems, ranked: 13-19 | 28 | table | READ | ready (rank 12 added 2026-10-08, Adam; old 12-18 are now 13-19) |
| 20 | P20 | What we fix first, and what we disclose | 39 | figure `next/fig_p20_roadmap` | INFERRED (plan) | ready (roadmap.txt; 19 ranks); last rendered 11:34Z |

form count: title 1, figure 5 (P02, P04, P10, P13, P20), table 14.
Narrative: the question (P01) -> what NDTwin is (P02) -> who asks it (P03) -> where everyone sits (P04) ->
task by task per developer (P05-P07) -> how mature and how big (P08-P09) -> one task built both ways, measured
(P10-P14) -> pick / do not pick (P15-P16) -> what is wrong with NDTwin, ranked by "would a developer give up"
(P17-P19) -> what we fix first (P20).

## 2. Per page: content and speaker notes

Marks: 🟢 RAN (OBSERVED), 🟠 READ, INFERRED. K = /home/adam/Desktop/NDTwin-Kernel; M = research/matrix_final.json;
H = K/doc/audit/2026-10-08_why-ndtwin-handson. Every NDTwin path:line is @2ece656c unless another sha is given.

### P01 `Why would a developer use NDTwin?`   form: title
Slide: the title only (signature "Adam" as in 930, Adam decides).
講者備註：
- 「老師上次問：開發者為什麼要用 NDTwin？今天整份報告就回答這一題，做法是拿 NDTwin 和 15 個現有工具逐項比。」
- 「三種開發者：寫網路控制 app 的、寫 P4 程式的、網管。每一種挑 8 件他們真的要做的事，每一格都附出處。」
- 「我們沒有修飾：NDTwin 自己的缺陷在表上用 ⚠ 標出來，後面三頁按『會不會讓開發者放棄』排序列出真正的問題和修法。」
- 證據分兩類：讀文件與程式碼（READ，第 2–9、15–19 頁）、實際跑過（RAN，第 10–14 頁，實作對照）。兩類不混在同一張表。

### P02 `What NDTwin is, as built today`   form: figure `arch/fig_p02_architecture`
Figure spec: figures_spec/architecture.txt (layers A apps / B kernel / C adapters / D data planes / E tools;
kernel blue, everything else grey; physical plane dashed "no run on record"; Local LLM and AI/ML-apps boxes
removed). Reuse: the 827 layout (NDTwin slide material 827/generator/build_arch_merged.js), redrawn with the
four changes listed in architecture.txt §0. Do not paste the old PNG.
講者備註：
- 🟠「NDTwin 的核心是一個 C++ kernel，對 app 開的是一個 REST API（port 8000），對下接三種資料平面之一：Mininet 裡的 OVS、Mininet 裡的 bmv2、實體交換機。一次只能接一種，混用會被拒絕。」
  出處：K/src/ndt_core/event_handling/ControllerAndOtherEventHandler.cpp:100（port 8000）；K/src/ndt_core/collection/TopologyAndFlowMonitor.cpp:3425-3427（混用平面拒絕）。
- OVS 與實體交換機經由 NDTwin 自己的 Ryu app 走 OpenFlow 1.3（K/intelligent_router.py:617-618）；bmv2 經由 P4 proxy 走 P4Runtime（K/p4_proxy/proxy_agent/main.py:2466 port 8081、p4_client.py:5,8）。kernel 對 proxy 講的是和 Ryu 同形的 REST，所以上層 app 不必知道底下是哪一種。
- 遙測一律進 kernel 的 sFlow 收集器（UDP 6343，K/include/ndt_core/collection/FlowLinkUsageCollector.hpp:33）：OVS 是交換機自己的 sFlow 1/256；bmv2 是 proxy 合成的 sFlow（K/p4_proxy/proxy_agent/sflow_emitter.py:1），外來程式走 tc 取樣（K/p4_proxy/mininet/psample_sflow_emitter.py:6）。
- 灰色方塊是 kernel 以外的元件（TE app、節能 app 與它的模擬器、模擬平台管理、Web GUI、狀態錄製、流量視覺化、流量產生器）。多數透過 REST 和 kernel 溝通；兩個例外：模擬案例經 NFS 交給模擬平台（Simulation-Platform-Manager@b7efd93 app.cpp:286），OVS fabric 由流量產生器的 testbed_topo.py 直接建（Network-Traffic-Generator@6e3f388 testbed_topo.py:39-48）。各自出處在 architecture.txt。
- 實體網路那一塊是虛線：程式寫了（HPE5520、Brocade ICX6610／ICX7250，K/include/common_types/GraphTypes.hpp:140-144），但沒有跑過的紀錄：kernel 樹裡沒有任何硬體執行 log；K/doc/2026-01-02_ndt_api.md:1598-1599 那句「has not been exercised」只講實體電源那個分支。
- 和 827 那張的差別：拿掉「Local LLM (fine-tuning)」與「AI/ML 推論 app」兩格，因為程式碼裡沒有（src/、include/ 沒有本機模型或 fine-tuning 的程式；唯一的 LLM 呼叫是 OpenAI，K/src/ndt_core/intent_translator/LLMAgent.cpp:138）；「Data cache manager」改名為實際模組名 Historical data manager。
- ❌ 不說「NDTwin 和你的正式網路即時同步」。

### P03 `Three developers, three jobs`   form: table
| developer | wants to get done | compared with | tasks |
|---|---|---|---|
| control-app developer | read state, write rules, test failures, reuse the app | Mininet+Ryu, ONOS+Mininet, Containerlab, ns-3, sFlow-RT | A1-A8 |
| P4-program developer | run own .p4, topology, entries, telemetry, tests | P4 tutorials VM, p4-utils, ONOS+Stratum | P1-P8 |
| network operator | mirror, check, predict, drill, save energy | Batfish, GNS3, Forward*, CML*, IP Fabric*, RouteNet-Fermi†, IRTF NDT draft† | O1-O8 |
| legend | * vendor material only · † paper or draft only | | |
講者備註：
- 🟠 三種開發者與 24 件事的定義在 research/ROWS.json（「personas」）。每一格的判定只有四種：● 內建（設定即可，不寫程式）、◐ 自己做（要寫程式或接別的工具）、○ 不支援或超出範圍、? 公開文件沒寫。
- 15 個對照工具的挑法：每一種開發者今天最可能拿來用的組合。商用的三個（Forward Networks、Cisco Modeling Labs、IP Fabric）只看得到廠商公開資料；學術的兩個（RouteNet-Fermi、IRTF 的 network digital twin 架構草案）只看得到論文或草案本身。
- 「Mininet+Ryu」那一欄是「自己組裝」的基準：一個開發者不用 NDTwin、自己拼起來會有什麼。

### P04 `Where 16 tools sit: fidelity vs live link`   form: figure `landscape/fig_p04_map`
Figure spec:
- Data: figures_spec/landscape.tsv (16 rows; columns tool, x_category, y_category, short_label, rationale,
  source, unsure; the `#` lines at the top carry the placement rule). The generator reads x/y/short_label
  only; rationale and source go to the figure .md.
- Placement rule (one rule for every tool, applied over M): x = the fidelity class in the tool's
  maturity.M6 note; y = link to a network the tool does not build or control, read from ops.O1 where the
  tool has an O1 cell, else from maturity.M6 plus app.A8 / p4.P8. stays synced live = a documented feature
  keeps ingesting state from such a network; imports snapshots = it ingests point-in-time config or state
  collected from one; none = it models only a network it builds, or controls as its controller.
  One point per tool, for the setup its matrix column names; other targets a tool can reach (hardware
  paths, coded or documented) are not drawn for any tool.
- x axis (left -> right, categorical, equal spacing): config model · ML model · flow-level model ·
  packet-level emulation · real devices. y axis (bottom -> top), axis title "link to a network the tool
  does not build or control": none · imports snapshots · stays synced live. Light grid: 5 x 3.
- Markers: filled circle per tool, label = short_label; tools sharing a cell are packed in the cell (the
  packet-level-emulation x none cell holds 10: Mininet+Ryu, ONOS+Mininet, Containerlab, ns-3,
  P4 tutorials VM, p4-utils, ONOS+Stratum, GNS3, CML*, NDTwin). NDTwin sits in the same band as the
  other nine (same vertical range, no row of its own), so the map shows no difference in y.
  ns-3: a distinct marker (open circle) at the left edge of that cell = packet-level SIMULATION.
  sFlow-RT: hollow diamond = monitor, not a model.
  IRTF NDT draft†: dashed horizontal band across the whole top row, label at the left end, no point;
  legend entry "framework (draft)".
  NDTwin: the only highlighted marker (accent colour); a dashed whisker left to flow-level model x none
  (shipped what-if). No marker for its physical path (coded, no run on record): P02 and P16 disclose it,
  and no other tool's hardware path is drawn either.
- Colours: persona of the tool's matrix group (app / P4 / operator); NDTwin in the accent colour.
- Words on canvas: title, axis title, axis category names, short labels, legend (marker kinds, IRTF as
  "framework (draft)").
講者備註：
- 🟠 位置規則只有一條，套用到全部 16 個工具，寫在 figures_spec/landscape.tsv 開頭：x＝M maturity.M6 說的 fidelity 類別；y＝和「工具自己沒有建、也沒有控制的網路」的連結——有文件化的功能持續吸收那種網路的狀態＝stays synced live；吸收從那種網路收來的某一時刻設定或狀態＝imports snapshots；只模擬自己建的、或自己當 controller 的網路＝none（NetBox 這類清冊匯入的拓樸算「自己建」）。有 O1 格的工具看 O1 的 note／scope；沒有 O1 格的八個（app 與 P4 兩頁的工具）看 M6 的 note 加 A8／P8。每個工具只畫一個點，就是矩陣那一欄所指的組合；硬體路徑（不管寫了還是有文件）一律不畫。逐列理由與出處在 landscape.tsv。
- 讀法：越右邊，模型越接近真實封包；越上面，和一個不歸它管的網路連得越緊。大多數開發工具都在「封包級模擬、none」那一格，NDTwin 也在；Batfish（開源）與商用的 Forward、IP Fabric 在左中——它們吸收從別人的網路收來的設定與狀態快照，不跑封包；sFlow-RT 在右上——它不建模型，只即時量測不歸它管的設備；RouteNet-Fermi 是 ML 模型、不接網路。
- NDTwin：twin 狀態是即時同步的，但同步的對象是它自己建、自己控制的 Mininet fabric（O1 要它自己的 Ryu app 當 controller，M ops.O1 NDTwin scope），所以照規則和 ONOS+Mininet 在同一列——ONOS+Mininet 也即時看它控制的 fabric（M app.A1、A3 ●）。「none」指的是和外部網路的連結，不是說沒有即時狀態。實體交換機路徑不畫（程式寫了、沒有跑過的紀錄，P02 與 P16 已揭露）；其他工具的硬體路徑也都不畫。附帶的 what-if 是 flow-level（max-min），所以有一條虛線往左拉到 flow-level。
- 不確定的位置（8 個，landscape.tsv 的 unsure 欄）：ns-3（x 軸沒有「封包級 simulation」這一格，畫在 emulation 格的左緣、換一種記號）、sFlow-RT（只量測、不建模型）、ONOS 兩組（x 取決於底下的資料平面；接實體交換機時 x 是 real devices，y 仍是 none，因為它就是 controller）、CML（NetBox 匯入只帶拓樸，算不上快照）、Forward 與 IP Fabric（規則沒有定快照的頻率；Forward 的連續快照、IP Fabric 的排程快照也可以讀成「持續吸收狀態」）、IRTF 草案（是框架草案，不是軟體，畫成一條帶子）。

### P05 `Control-app developer: who does what`   form: table
| task | Mininet+Ryu | ONOS+Mininet | Containerlab | ns-3 | sFlow-RT | NDTwin |
|---|---|---|---|---|---|---|
| A1 Read topology via API | ● | ● | ◐ | ◐ | ◐ | ●◌ |
| A2 Flows with path and rate | ◐ | ◐ | ◐ | ◐ | ◐ | ●⚠◌ |
| A3 Per-link utilization, live | ◐ | ● | ◐ | ◐ | ● | ●⚠◌ |
| A4 Install rules from an app | ● | ● | ◐ | ◐ | ◐ | ●⚠◌ |
| A5 Fail a link, watch the app | ● | ● | ◐ | ◐ | ◐ | ● |
| A6 What-if before a change | ◐ | ◐ | ◐ | ◐ | ○ | ◐ |
| A7 Same app: OpenFlow and P4 | ○ | ● | ○ | ○ | ◐ | ●⚠ |
| A8 Same app: emulated and real | ● | ● | ◐ | ◐ | ● | ●◌ |
| legend | ● built in · ◐ you build it · ○ no · ? docs silent | ⚠ open defect on that path (NDTwin only) · ◌ no run on that target | | | | |
(Generated from M personas.app; the generator stops if any cell differs from M.)
講者備註：
- 🟠 全表讀自 M（competitor 讀公開文件，NDTwin 讀 trunk 2ece656c 的程式碼與文件）。每格的一句說明、出處網址或 path:line 在 M 的 note／source。
- 數字：NDTwin 8 列裡 7 個 ●，最多；但其中 6 個帶 ⚠ 或 ◌——乾淨的 ● 只有 A5（故意弄斷一條 link）。ONOS+Mininet 6 個 ●、0 旗標；Mininet+Ryu 4 個。
- 旗標的意思：⚠＝那條路上有一個還開著的已知缺陷；◌＝在宣稱的那個目標上沒有任何跑過的紀錄（多半是實體交換機）。
  - A2 ⚠：每秒不到約 22 個封包的流，在預設 3 秒視窗裡有一半時間看不到（KNOWN-ISSUES「B-x 的反向」；K/include/ndt_core/collection/FlowLinkUsageCollector.hpp:91）。
  - A3 ⚠：遙測停了的時候利用率回 0，而不是「不知道」（KNOWN-ISSUES C-9、B-17）。
  - A4 ⚠：bmv2 表滿、或帶 priority 的刪除失敗，HTTP 仍回 200（C-6、C-7）；proxy 重啟後，bring-up 以來 app 新增或刪除的規則消失（bring-up 路由會重算回來；A-4c）。
  - A7 ●⚠：同一組 endpoint 兩個平面都在，但 P4（附帶的 ndtwin_switch.p4）上 group／meter 回 501（K/src/ndt_core/routing_management/P4RoutingStrategy.cpp:27-33），ECMP 的 TE app 只能跑 OpenFlow；⚠ 來自 C-6／C-7 這兩個只在 P4 發生的靜默失敗。
  - A7 的 ONOS+Mininet ● 和 NDTwin ● 用同一個基準一起判：各自附帶的 P4 pipeline 上，app 不改就跑（ONOS 附帶 bmv2 的 basic pipeconf，fwd、LLDP、host app 不改；M app.A7 ONOS note）。換別的 P4 程式，ONOS 要寫 pipeconf。若標準改成「每個附帶的 app 都能移植」，兩格一起降為 ◐，不只動一格。
  - ◌（A1–A4、A8）：實體交換機模式程式寫了，沒有跑過的紀錄（kernel 樹裡沒有硬體執行 log；K/doc/2026-01-02_ndt_api.md:1598 那句只講電源分支）。
- A5：NDTwin 在 Mininet 上用 tc netem 真的切斷一條 link（K/src/ndt_core/http/HttpSession.cpp:20,282），但**沒有事件推送**，app 要自己 poll。bmv2 上的偵測：鏈路在最後一個 LLDP beacon 之後 15 秒判斷為斷（每個 beacon 重設時間，K/p4_proxy/proxy_agent/topology_manager.py:1680；比較在 :2026；每 5 秒檢查一次，:422），也就是切斷後約 10–20 秒；KNOWN-ISSUES D-2 實測的 10.7–14 秒在這個範圍內。
- A6：大家都是 ◐。NDTwin 的 kernel 會把案例轉給外掛的模擬器，但唯一附帶的模擬器只模擬「關掉哪些交換機」；其他 what-if 要自己寫模擬器（M app.A6）。
- 公平性（規則 9）：⚠ 只出現在 NDTwin，因為我們看得到 NDTwin 自己的缺陷清單、看不到別人的；別人的格子講的是文件上有沒有這個功能，不是它做得好不好。

### P06 `P4-program developer: who does what`   form: table
| task | P4 tutorials VM | p4-utils | ONOS+Stratum | NDTwin |
|---|---|---|---|---|
| P1 Run my own .p4 on bmv2 | ● | ● | ● | ◐ |
| P2 Topology with hosts, built | ● | ● | ◐ | ● |
| P3 Table entries through an API | ● | ● | ● | ◐⚠◌ |
| P4 Link discovery, my program | ○ | ◐ | ◐ | ◐ |
| P5 Per-flow telemetry, no code | ◐ | ◐ | ◐ | ◐◌ |
| P6 Generated packet tests | ◐ | ◐ | ◐ | ◐ |
| P7 Network-wide view | ○ | ● | ● | ● |
| P8 Path to a hardware target | ○ | ◐ | ● | ○ |
| legend | ● built in · ◐ you build it · ○ no · ? docs silent | ⚠ open defect (NDTwin only) · ◌ no run on that target | | |
(Generated from M personas.p4.)
講者備註：
- 🟠 這一頁 NDTwin 是最弱的一欄：2 個 ●（P2、P7）、5 個 ◐、1 個 ○（P8）；三個對照組各有 3–4 個 ●。我們照實講。
- P1 ◐：自己的 .p4 經由 `tools/p4_exercise/convert.py` 打包（K/tools/p4_exercise/convert.py:1），再用實驗室的 `ndt up p4 --app` 起來：它寫入 proxy 讀的 knob 檔 app_package_override（K/tools/test_workflow/ndt:1602,1642；K/p4_proxy/mininet/app_package.py:56），kernel 樹裡沒有別的寫入者（problems 第 1 名）；13 支 P4 tutorial exercise 在 NDTwin fabric 上跑起來（M p4.P1 note）。只支援 exact／lpm 表項。
- P3 ◐⚠◌：`POST /p4/table_entry` 依表名寫 exact／lpm；ternary／range／optional 回 501（K/p4_proxy/proxy_agent/api_routes.py:880）；proxy 重啟表項就消失（api_routes.py:841、KNOWN-ISSUES A-4c）；執行期呼叫沒有跑過的紀錄（◌）。
- P4 ◐：LLDP 鏈路發現只對 NDTwin 自己的 ndtwin_switch.p4 有效；別的程式要嘛宣告鏈路（沒有斷線偵測），要嘛用 root 的心跳 helper（K/doc/2026-01-02_ndt_api.md:627；K/p4_proxy/proxy_agent/link_heartbeat.py:52-54）。
- P5 ◐◌：外來程式在 Mininet 上用 tc 取樣換算成 sFlow，不用改 .p4（K/p4_proxy/mininet/app_package.py:481）；每條鏈路的使用量在 13 支裡 10 支驗過，**每條流**的視圖在外來程式上沒驗過（◌）。
- P6 ◐：和三個對照組同一個基準——它們的 ◐ 是因為 P4Testgen 是常見的外掛；NDTwin 已經在跑 p4testgen，但只拿來檢查自己 pipeline 的覆蓋率（K/tools/test_workflow/p4_coverage_gate.sh:1），沒有替使用者的程式產生測試，要自己接。
- P8 ○：沒有硬體 P4 目標，只有 bmv2 v1model（K/README.md:5；K/p4_proxy/p4_src/SPEC.md:6-7；K/p4_proxy/p4_src/ndtwin_switch.p4:32）。
- ONOS+Stratum P8 ●：Stratum 支援 Tofino／Tomahawk，但 M 的 scope 註明 Tofino 已停產、Stratum 最後一次 release 是 2022-06-30。
- 公平性同 P05。

### P07 `Network operator: who does what`   form: table
| task | Batfish | GNS3 | Forward* | CML* | IP Fabric* | RouteNet-Fermi† | IRTF NDT draft† | NDTwin |
|---|---|---|---|---|---|---|---|---|
| O1 Mirror live state | ◐ | ◐ | ◐ | ◐ | ◐ | ○ | ◐ | ●⚠◌ |
| O2 Config correctness check | ● | ◐ | ● | ◐ | ● | ○ | ◐ | ○ |
| O3 Congestion what-if | ◐ | ◐ | ? | ◐ | ? | ◐ | ◐ | ◐ |
| O4 Run vendor NOS images | ○ | ● | ○ | ● | ○ | ○ | ○ | ○ |
| O5 Fault drills on a copy | ● | ● | ? | ● | ● | ◐ | ◐ | ●⚠ |
| O6 Energy-saving analysis | ○ | ○ | ? | ? | ? | ○ | ◐ | ●⚠◌ |
| O7 Natural-language intent | ○ | ● | ◐ | ● | ◐ | ○ | ◐ | ●⚠◌ |
| O8 Record and replay state | ◐ | ◐ | ● | ? | ● | ○ | ◐ | ●⚠◌ |
| legend | ● built in · ◐ you build it · ○ no · ? docs silent | ⚠ open defect (NDTwin only) · ◌ no run on that target | * vendor material · † paper or draft · GNS3 O7: 3.1 pre-release | | | | | |
(Generated from M personas.ops; the contested cells are ruled and applied in M, see §3.)
講者備註：
- 🟠 NDTwin 5 個 ●，5 個都帶旗標。O1 是這一列唯一的 ●（鏡像的是它自己控制的 fabric，見下）；O6 沒有其他 ●，但商用三家是 ?（公開資料沒寫，不等於沒有）。
- O1 ●⚠◌：kernel 輪詢 Ryu／proxy 與 sFlow 來鏡像；前提是 NDTwin 自己的 Ryu app 在控制那個網路、拓樸檔事先宣告（K/intelligent_router.py:617；K/src/ndt_core/collection/TopologyAndFlowMonitor.cpp:2373：拓樸檔沒有的交換機只印 WARN、被忽略）。⚠ 同 A2／A3；◌：沒有實體交換機的執行紀錄。
- O2 ○：NDTwin 沒有設定模型，沒有 ACL／可達性檢查——這是 Batfish、Forward、IP Fabric 的主場。
- O3 ◐：附帶的模擬器只吃「要關掉哪些交換機」，不吃「拿掉哪條鏈路」；它的預測和實測的比較沒有紀錄（kernel 與 Energy-Saving-App 的樹裡都找不到；Energy-Saving-App@9facb78 src/sim/energy_saving_simulator.cpp:467；M ops.O3 scope）。沒有一個工具在這格是 ●。
- O5 ●⚠：Mininet 上可以切 link、關交換機；但 OVS 上「關再開」會讓那台交換機底下所有主機永久斷線，而四種健康檢查全綠（KNOWN-ISSUES B-9）。「副本」是你用拓樸檔建的 Mininet fabric，不是自動複製的正式網路；OVS 的副本還是寫死的 10 台交換機（Network-Traffic-Generator@6e3f388 testbed_topo.py:39-48）。IP Fabric 的 ● 是廠商說法：MCP 示範頁說它在模型上模擬一次 gateway 故障；產品文件只看得到單點故障標示（M ops.O5 IP Fabric note）。
- O6 ●⚠◌：Energy-Saving-App 會在模擬檢查後關掉低負載交換機；Mininet 上的功率讀數是由 dpid 合成的；app 端的鎖 livelock 仍開著（KNOWN-ISSUES A-9）。
- O7 這一列只有一種讀法：一句自然語言的要求，改變這個工具所跑的網路（模擬的網路也算）。GNS3 ●（MCP 服務從自然語言建專案、節點、鏈路；3.1 是預發行版，表上腳註；NDTwin 的 P4 平面也還沒 release）、CML* ●（MCP 建 lab）；IP Fabric* ◐（MCP 只回答唯讀查詢，不動網路）、Forward* ◐（對模型問答與跑工作流程，GA 只是「預計」）。
- O7 ●⚠◌：`POST /ndt/intent_translator/text` 呼叫 OpenAI，預設關閉；開啟 AI 的執行沒有紀錄（測試 stack 一律以 --no-ai 啟動）；BLOCK_HOST 沒裝任何東西也回 success（KNOWN-ISSUES A-4g；K/src/ndt_core/intent_translator/IntentTranslator.cpp:809）。NDTwin 的 ● 也只在上面那個讀法下成立：它動的是自己控制的 Mininet fabric。
- O8 ●⚠◌：Network-State-Recorder 每 5 秒錄 graph 與 flow，Web-GUI／Visualizer 可以回放；但 recorder 遇到一次 connection refused 就永久停止、之後只產生空檔（K/doc/2026-08-14_cross-component-integration-matrix.md:147）；回放沒有跑過的紀錄（◌）。
- 公平性：商用三家（*）只根據廠商公開資料，它們的 ● 是廠商的說法；? 是「公開資料沒寫」，不等於沒有。學術兩個（†）只有論文或草案。

### P08 `Self-hosted tools: license, scale, interface`   form: table
| tool | license | cost | latest release | largest documented scale | install | interface |
|---|---|---|---|---|---|---|
| Mininet+Ryu | BSD-3 · Apache-2.0 | free | Mininet 2.3.0 (2021) · Ryu 4.34 (2019) | "hundreds of hosts", no figure | VM or source; root | Python API, CLI · Ryu REST |
| ONOS+Mininet | Apache-2.0 | free | 2.7.0 LTS (2022) | 100-400 switches (old test report) | Docker or Bazel build | REST, Java, CLI, GUI |
| Containerlab | BSD-3 | free | v0.79.0 (2026-08) | not stated | packages, Docker; sudo | CLI + YAML |
| ns-3 | GPL-2.0 | free | ns-3.49 (2026-10) | 10^9 nodes on HPC (study) | source build | C++ (Python bindings) |
| sFlow-RT | proprietary | free download; production by quote | 3.2 (date not stated) | not stated | tar, Docker, RPM, DEB; Java 17 | REST + JavaScript; no auth |
| P4 tutorials VM | Apache-2.0 | free | no versioned release | not stated (example 4/4) | VM or Ubuntu install | make, Mininet CLI, P4Runtime |
| p4-utils | GPL-2.0 | free | v0.0 (2018) | not stated | script or QEMU VM | Python API, JSON |
| ONOS+Stratum | Apache-2.0 | free | ONOS 2.7.0 (2022) · Stratum (2022-06) | not stated (example 4/6) | Docker + make, or VM | REST, Java · P4Runtime, gNMI |
| Batfish | Apache-2.0 | free | v2026.08.27 | 75-2735 nodes (11 real networks) | Docker or pip; 8 GB RAM min | Python (pybatfish) |
| GNS3 | GPL-3.0 | free; NOS images licensed apart | 2.2.61 (2026-07) | 600-800 routers, one server (third party) | installers, PPA, pip | REST + WebSocket |
| NDTwin | Apache-2.0 | free; LLM needs own OpenAI key | v1.0.0 (2026-02, OpenFlow only); P4 plane unreleased | 10 switches, 128 hosts (measured) | VM image or Ubuntu 24.04 build; sudo | REST :8000; no auth, no push |
(Rows M1, M2, M3, M7, M8, M9 of M; M6 fidelity is P04; M4 and M5 dropped for every tool, §0 rule 7.)
講者備註：
- 🟠 每格讀自 M 的 maturity 列；出處網址在 M 的 source／locator。日期是 2026-10-08 讀到的。
- NDTwin 的「latest release」：最後一個正式版 v1.0.0（2026-02）只有 OpenFlow（v1.0.0 沒有 p4_proxy/）；今天比較的 P4 平面是測試用快照、不是 release（K/README.md:8-10、:145-148）。
- NDTwin 的「scale」：10 台交換機、128 台主機、288 條有向邊，OVS 與 bmv2 兩個平面都量過（M maturity.M7）。
- 其他工具的「scale」：P4 tutorials VM 與 ONOS+Stratum 的格子是教學範例的拓樸（交換機數／主機數），不是上限，所以寫「not stated」。ONOS 的「100-400 switches」來自 ONOS 1.8 時代的測試報告，是搜尋摘要裡看到的，原頁沒有打開讀（M maturity.M7 ONOS note）。
- NDTwin 的「interface」：約 45 個 REST route、沒有認證、沒有 OpenAPI 規格、沒有推送（K/src/ndt_core/http/HttpSession.cpp:326-345）；P4 proxy 另有 REST :8081。sFlow-RT 同樣沒有內建的存取控制（M maturity.M9 sFlow-RT）。
- 標題用「self-hosted」不用「open-source」：這一頁有 sFlow-RT，它是 proprietary（免費下載）。
- 「install」欄的 NDTwin 前提：C++23、Boost 1.83+、Ryu 跑在 Python 3.8、需要 sudo（M maturity.M8）。

### P09 `Commercial and academic: public material only`   form: table
| tool | basis | what it models | cost | latest release | documented scale | interface |
|---|---|---|---|---|---|---|
| Forward Networks | vendor datasheet | config + state, from snapshots | quote, per device | 25.6.0 (2025-06) or newer | "thousands of devices" (vendor) | REST, query engine, MCP |
| Cisco Modeling Labs | vendor docs | VM / container NOS emulation | free 5 nodes · $199 (20) · $349 (40) | 2.10.0 (2026-03) | 520 running nodes | REST, Python client, MCP |
| IP Fabric | vendor docs | config + state, from discovery | quote, per device | 8.1.4 (2026-10) | sizing tier to 20,000 devices | REST, Python SDK, MCP |
| RouteNet-Fermi | paper | GNN: delay, jitter, loss | free code; data + GPU | paper 2023; no release | 300 nodes (trained on 5-10) | Python scripts |
| IRTF NDT draft | draft text | framework; model left open | free to read | draft -13 (2026-07) | n/a | names SNMP, NETCONF, REST |
講者備註：
- 🟠 讀自 M 的 maturity 列，五個都只用公開資料：商用三家看 datasheet、文件與定價頁，學術兩個看論文（arXiv 2212.12070）與 IETF 草案 draft-irtf-nmrg-network-digital-twin-arch-13。
- 為什麼放進來：它們是「network digital twin」這個詞今天在業界與學界的代表。Forward 與 IP Fabric 把自己叫 digital twin，但它們是設定與狀態的模型，不跑封包；公開資料沒有寫流量與負載（M ops.O1 note）；IRTF 草案要求即時資料與 what-if，但沒有實作；RouteNet-Fermi 是預測延遲的神經網路模型。
- 數字的性質：Forward 的「thousands of devices」是廠商說法；CML 的 520 是 2.9 版部落格的數字；IP Fabric 的 20,000 是 sizing 文件的級距；Forward 25.6.0 是找到的最新公開 release note，可能有更新的。

### P10 `Hands-on: one task, two setups`   form: figure `handson/fig_p10_setup`
Figure spec (generator generator/make_p10_setup.py; data paths, sha256 and matplotlib version in
figures/handson/fig_p10_setup.md):
- Data: H/topology.tsv (10 switches, 4 hosts, 16 switch-switch links; same wiring for all arms); the pair is
  H/congestion/variants_dev.tsv role A (h1 -> h3, the development workload handed to both agents); its largest
  flow's path before and after the move is the first move line of that pair in the NDTwin agent's development log
  H/congestion/raw/agent_ndtwin_dev/evidence/ctl7.log (s1-s5-s9-s8-s3 -> s1-s6-s9-s7-s3). The DIY app's base path
  for the same pair is read from H/congestion/raw/agent_diy_dev/ryu.log into the figure .md (not drawn).
- Canvas: core s9, s10; aggregation s5-s8; edge s1-s4; hosts h1-h4 on port 3. Before = solid accent, after =
  dashed accent; a load glyph (three red bars, "over the limit") on s1-s5.
- Two titled side panels: "NDTwin arm" = your app -> REST :8000 -> NDTwin kernel (topology, base forwarding,
  flow views) -> Ryu (OVS) or P4 proxy (bmv2), tag "OVS + bmv2"; "DIY arm" = your app is a Ryu app inside stock
  Ryu 4.34 (base forwarding, counters, moves) -> OpenFlow 1.3 -> OVS, tag "OVS only". Bottom: "same wiring for
  both arms".
- On canvas: box names, the two path keys, those tags. No numbers but box names.
- The generator stops if topology.tsv is not 10 switches / 16 links / 4 hosts on port 3, the dev pair or its move
  line is missing, a path hop is not a topology link on the logged port, before = after, or the DIY log has no
  base path for the pair.
講者備註：
- 🟠 拓樸（READ：讀檔，不是執行）：兩個臂用同一個 10 台交換機／4 台主機的接線（H/topology.tsv；兩個 JSON 模型與 ovs_4host_topo.py 的 16 條鏈路與埠一致，H/raw/helper_topo_vs_tsv.txt）。圖上的「搬移前／搬移後」是 NDTwin 那個 agent 開發時的一次執行紀錄（H/congestion/raw/agent_ndtwin_dev/evidence/ctl7.log 第 10 行），讀出來畫，不是這裡重跑的；DIY 的基本路由替同一對主機選的是另一條（s1-s6-s10-s7-s3，H/congestion/raw/agent_diy_dev/ryu.log 第 4 行）。
- 🟠 NDTwin 方塊寫的「base forwarding」：在 OVS 上是 NDTwin 自己的 Ryu app（K/intelligent_router.py）裝的，在 bmv2 上是 P4 proxy；NDTwin 臂的開發者一行都不用寫。
- 🟠 任務（H/congestion/TASK.txt，兩臂同一份）：任何一條交換機之間的鏈路、單一方向超過 40 Mbit/s 時，找出那條鏈路上最大的 TCP 流，搬到一條放得下的路徑，並且讓它留在那裡。只搬最大的那一條，不搬整對主機；任何主機對、任何方向、任何 port 都要能做。
- 🟠 判定（H/congestion/PREREG.txt §6、§7，兩個 app 都還不存在時寫定）：獨立的 checker 只讀 /sys 的 tx 計數器與接收端的 iperf3 JSON，不問 NDTwin、不問 Ryu。壅塞開始後 90 秒內解除、而且連續 120 秒保持，總送達 ≥95%、每條流 ≥90%，才算 PASS。每個臂×平面 5 次，變體 v1 v2 v3 v1 v2，每次都是全新的 fabric。判定用的變體沒有交給 agent（它們的 port／速率組合沒看過）；但兩個 agent 都自己測過 h2→h4，NDTwin 那個 agent 也測過 h3→h2（H/congestion/agents/*/NOTES.txt）。
- 🟠 兩臂差在哪（H/congestion/ARM_NDTWIN.txt、ARM_DIY.txt）：NDTwin 臂的 app 只能用 NDTwin 的 REST API（:8000），拓樸、基本轉送、流量視圖由 NDTwin 給；它在 OVS 上開發，同一個 app 目錄不改，再拿到 bmv2 上判定。DIY 臂的 app 本身就是原版 Ryu 4.34 的 OpenFlow 1.3 controller，連基本轉送都要自己寫，只有 OVS。
- INFERRED：為什麼是壅塞搬移、不是斷線後重新路由——NDTwin 自己就會繞過斷掉的鏈路（P13 左半），Ryu 附帶的 STP 範例也能讓 DIY 一行不寫就恢復（P13 左半）；failover 任務在兩側都不是「同一件工作」（H/PHASE0_NOTES.txt §4–5）。
- 🟠 DIY 臂也用實驗室的 helper 起 fabric（同一個 ovs_4host_topo.py），排除「DIY 的網路長得不一樣」。代價：helper 的 fabric 開著 sFlow（DIY 臂沒有人收）、DIY 臂另外把 bridge 釘在 OpenFlow 1.3，和 NDTwin 臂協商出同一版（H/PHASE0_NOTES.txt §6 第 1、2 點）。
- 公平性：DIY 臂沒有 P4 對應物，「同一個 app 不改就能跑 bmv2」只能問 NDTwin（P14）。

### P11 `What each side had to build`   form: table
| component | NDTwin arm | DIY arm |
|---|---|---|
| base forwarding | given by NDTwin | written: 123 lines |
| topology and ports | given by get_graph_data · parse: 40 lines | written: 96 lines, from topology.tsv |
| per-flow rate and path | given by get_detected_flow_data (sampled) · tracking: 76 lines | written: 57 lines, exact flow counters |
| path fallback, unused in the trials | written: 58 lines | n/a |
| per-link load | written: 12 lines, sum of flow estimates | written: 40 lines, exact port counters |
| congestion detection | written: 48 lines | written: 30 lines |
| path computation | written: 65 lines | written: 57 lines |
| rule install and check | given by batch write + dispatch status · calls: 122 lines | written: 52 lines, no check |
| keep it there | written: 37 lines | inside path choice, counted above |
| loop, settings, logging | written: 116 lines + run.sh 4 | written: 100 lines |
| same app on bmv2 | 0 lines changed (result: 4 of 5, P14) | n/a (no P4 plane) |
| total, cloc code lines | 578 | 555 |
(RAN: the cloc counts and the totals. READ: the split into rows, i.e. which line range belongs to which row; the ranges are in the notes.)
講者備註：
- 🟢 行數（RAN）：cloc 1.98（`cloc --quiet --csv`，只取 code 欄；空行、註解、Python docstring 不算）在兩個 app 的指定行範圍上跑出來的。檔案是判定時跑的那一份：controller.py sha256 8f861d3c、run.sh 4672a502、app.py 3a4f76c6（H/congestion/SCORECARD.txt 的身分行，這裡重算相同）。各列加總 574＋run.sh 4＝578、555，和整檔 cloc 相同，每一行只算一次。
- 🟠 列的切法（READ：我讀程式碼的歸類，不是執行的結果）；範圍列在這裡，任何人都可以重數。兩邊用同一個規則：埠名與埠號的對應算「topology and ports」，送出規則的 helper 算「rule install」。
  - NDTwin（H/congestion/agents/ndtwin_app/controller.py）：拓樸與埠 90–120、233–245（解析 GET /ndt/get_graph_data，含每條鏈路的埠）；每條流的速率與路徑 159–194、246–288、353–361（GET /ndt/get_detected_flow_data）；路徑備援 289–352（kernel 給的路徑不完整時，改從 GET /ndt/get_switch_openflow_table_entries 的基本規則推路徑）；鏈路負載 362–376；壅塞偵測 377–428；路徑計算 121–156、429–463；寫規則與確認 196–215、464–584（POST /ndt/install_flow_entries_modify_flow_entries_and_delete_flow_entries，再輪詢 GET /ndt/get_flow_dispatch_status?request_id=）；留在那裡 585–625；其餘 1–88、217–232、626–678。
  - DIY（H/congestion/agents/diy_app/app.py）：基本轉送 132–139、208–225、316–345、367–447（交換機上線、每對主機一條固定路徑、table-miss、ARP、packet-in）；拓樸與埠 33–44（從 topology.tsv 抄進程式）、64–90、226–291（從 OpenFlow port description 的埠名學埠號）、293–302；每條流速率 141–172、494–528；鏈路負載 470–493、529–552（OpenFlow port stats 的 tx_bytes）；壅塞偵測 585–615；路徑計算 92–130、553–584；寫規則 303–315（FlowMod helper _flow）、346–366（_exact_match、_install_exact：每條 TCP 連線一條精確的 5-tuple 規則，也是量速率用的計數器）、616–640（搬移）；其餘 1–32、45–63、174–207、448–469、641–664。DIY 的「留在那裡」是 _plan 不回到走過的路徑（app.py:565）加上搬過的流在 packet-in 時重裝（app.py:408–409），已算在路徑計算與基本轉送裡。
- 🟢 讀法（數字）：NDTwin 臂沒有寫基本轉送（DIY 123 行），拓樸與埠只要解析（40 對 96 行）；但整體 578 對 555，NDTwin 臂沒有比較小。
- INFERRED：NDTwin 臂多出來的，主要不是「每條流」那一列，而是另外兩處。一是路徑備援 289–352（58 行），10 次判定裡一次都沒有觸發（🟢 判定計入的 10 個 app log，epoch 1791442401–1791445864，裡沒有 "taken from the base rules"）。二是處理取樣雜訊的設定與偵測：controller.py:32–50 的常數（12 次平滑、均值減一個標準誤差、連續 5 次、42 Mbit/s 遲滯）與 377–428 的偵測。這些是那個 agent 選的做法；它在 NOTES 裡寫一條實際 33 Mbit/s 的流每秒讀到 22–46（H/congestion/agents/ndtwin_app/NOTES.txt）。NDTwin 北向的流量是 1/256 sFlow 取樣估計值；DIY 直接讀 OpenFlow 的精確計數器，鏈路負載只取 4 秒平均（app.py:46–51）。
- 🟠 寫入確認：NDTwin 臂每批寫入都查 dispatch status（controller.py:501–522）；DIY 臂不確認規則有沒有裝上（沒有 barrier，也沒有處理 OFPT_ERROR 的 handler，app.py:303–314），所以 DIY 那邊有沒有被拒，這次沒有測到。
- 公平性（PREREG §10，事先揭露）：DIY 要自己寫基本轉送，任務本來就比較大；DIY 可以抄 Ryu 附帶的範例，它沒有拉進任何其他 Ryu app（🟠 app.py 沒有 require_app，也沒有 ryu_args.txt）。
- n＝1：每臂一個 agent、一個 app；另一個 agent 可能寫出大小很不一樣的程式。

### P12 `Effort, measured`   form: table
| metric | NDTwin arm | DIY arm | pre-registered rule: result |
|---|---|---|---|
| lines of code in app/ (cloc) | 820 | 736 | NDTwin >= DIY: NDTwin loses |
| deliverable only (cloc) | 578 | 555 | informational, not registered |
| components the developer starts | 1 | 1 | equal: NDTwin loses |
| agent wall clock, first call to finish | 61 min | 35 min | NDTwin +73 %: NDTwin loses |
| agent tool calls | 101 | 46 | NDTwin +120 %: NDTwin loses |
講者備註：
- 🟢 全表是 RAN，出處 H/congestion/SCORECARD.txt（kernel commits 9335b189、65b14f46）。量法與「什麼算 NDTwin 輸」都是兩個 app 還不存在時就寫好的：H/congestion/PREREG.txt §9、§11。四個事先登記的努力指標，NDTwin 全部輸。
- 🟢 LOC：`cloc --quiet --csv`（cloc 1.98，/usr/bin/cloc），code 欄加總，app/ 底下除了 NOTES.txt 與 log 全部算。NDTwin 820＝Python 814（controller.py 574＋app/dev/ 的 8 支開發工具 240）＋run.sh 4＋dev/ 兩個一行的 API 回應 JSON 2；DIY 736＝app.py 555＋test_offline.py 161＋analyze.py 20。這裡用交付時 app/ 的副本（H/congestion/raw/agent_ndtwin_dev/、agent_diy_dev/）重跑 cloc，得到同樣的 820 與 736。
- 🟢 一個不對稱：NDTwin 那 2 行 JSON 算進去了，DIY 在 app/runs/ 底下留的 iperf3 JSON（工作負載的輸出，當成 log）沒有算。拿掉 JSON 是 818 對 736，判定不變。只算交付程式的 578 對 555 不是事先登記的指標，只供參考；它也沒有反過來。
- 🟢 components：(a) 開發者要自己啟動的行程兩邊都是 1 個（NDTwin：run.sh；DIY：ryu-manager app.py，沒有拉其他 Ryu app）；(b) 依賴的服務：NDTwin 臂是 NDTwin 的 REST API，DIY 臂是原版 Ryu 4.34。事先規則：一樣多就算 NDTwin 輸。
- 🟢 agent 時間與工具呼叫：從每個 agent 自己的對話紀錄算。起點是第一個工具呼叫（05:49:18Z、07:58:26Z）；終點用 agent 自己報的完成時間（06:50:29Z、08:33:45Z）＝3671 s 對 2119 s，+73%。若改用交回結果那一個呼叫的時間（06:50:48Z、08:34:02Z），差距仍是 +73%。工具呼叫 101 對 46（對話紀錄裡各是 102、47，各多的一次是交回結果的呼叫，不算）。事先規則：差距小於 25% 才算「沒有差別」。workload.sh 各跑 16、14 次（只供參考）。
- 🟠 誰寫、順序（READ：對話紀錄與 SCORECARD）：兩個都是全新的 Claude Sonnet 5.5 subagent，effort 都是 xhigh，同一份 prompt 範本（kits/AGENT_PROMPT_TEMPLATE.txt），只拿到自己那一臂的 kit，預算各 3 小時。NDTwin 臂先寫，DIY 臂後寫；後寫的 agent 沒有看過先寫那個 agent 的程式，也沒有看過它的對話紀錄。
- 🟠 揭露：Claude Code 對每個 subagent 都會附上專案的 CLAUDE.md 與最上層的 memory 索引，所以兩個 agent 的 context 裡都有它們；對話紀錄稽核顯示兩邊都沒有打開 memory 檔，各自只讀了自己的 ARM 檔允許的東西（DIY 那個 agent 讀了原版 Ryu 的原始碼，ARM_DIY 允許這麼做）。揭露，沒有修正（SCORECARD）。
- n＝1：每一臂只有一個 agent，這些努力數字各是一次觀察，不是分布；agent 的表現每次會不同（PREREG §1、§10）。
- 對帳：第一次在 NDTwin 上量「寫一個 app 要花多少」，沒有先前的結果可以更新或推翻。
- ❌ 不說「用 NDTwin 寫 app 比較省事」——在這個任務上，量出來是相反的。

### P13 `Time to relief after the trigger`   form: figure `handson/fig_p13_relief`
Figure spec (generator generator/make_p13_relief.py; data paths, sha256, every plotted value and the matplotlib
version in figures/handson/fig_p13_relief.md). Two titled panels, both RAN.
- Left panel "Built-in reroute, no app (link cut)": H/controls.tsv. Strips "NDTwin, OVS" (5), "NDTwin, bmv2" (5),
  "DIY, Ryu STP sample" (3). Dot = trial at gap_ms / 1000 s. Designed RED controls are checked, not drawn, and
  must all be NOT_RECOVERED: NDTwin's two red-bothpaths rows (both uplinks of s1 cut, no path exists) and the three
  DIY static-routes rows (static routes never recompute).
- Right panel "Congestion relief by the app": H/congestion/results.tsv rows ndtwin-app and diy-app. Strips
  "NDTwin app, OVS" (5), "NDTwin app, bmv2" (4 dots + 1 red cross in a grey "failed" zone), "DIY app, OVS" (5);
  x = time_to_relief_s. The scripted reference movers (*-ctl rows; 22 s is the harness's own schedule) are checked,
  not drawn.
- Median bar and label per strip; dots on one value are stacked vertically; each panel has its own x scale.
- Words on canvas: title, panel titles, strip names, axis "seconds after the trigger", tick numbers, "failed",
  medians, a three-entry key (trial, failed trial, median).
- The generator stops if a strip or a designed red control has a different number of trials than planned
  (run_controls.sh: 5 per NDTwin plane, 3 per DIY baseline; PREREG §7: 5 per arm x plane), a row is INVALID_* /
  SUDO_REFUSED / ANALYZER_FAILED / PRECUT_DEAD, a PASS row has no time, a scripted control differs from its
  pre-registered verdict, or a designed red control recovered.
講者備註：
- 🟢 左半（RAN，H/controls.tsv，kernel commit dcff37b6；ping 原始紀錄在 H/raw/，已封存在 audit-raw 分支 ed24e5e5）：用 tc netem 把 h1→h3 主路徑上 s1 的上行鏈路兩個方向都切成 100% loss，量「切斷之後送出、而且收到回覆的第一個 ping」距離切斷多久（H/analyze_ping.py：只算切斷之後送出的封包，還要連續 10 秒沒有 >0.5 s 的空檔才算恢復）。NDTwin 不需要任何 app 就自己繞路：OVS 中位數 20.3 s（15.9–20.8，5/5）、bmv2 15.2 s（14.4–19.2，5/5）。Ryu 附帶的 simple_switch_stp_13 一行不寫，3/3 在約 67.7 s（67.3–67.7）恢復。
- 🟢 沒畫的對照：DIY 靜態路由 3/3 沒有恢復，這是設計好的（對照：靜態路由本來就不重算）；NDTwin 兩個「s1 兩條上行都切」的負對照也都沒恢復，表示 checker 會變紅。這兩種都是設計好的紅色對照，generator 會檢查，不畫。
- 🟢 右半（RAN，H/congestion/results.tsv，kernel commits 80a4e29f、9335b189）：x＝壅塞開始到「解除、而且之後 120 秒都保持」的第一個 1 秒區間。NDTwin app 在 OVS 5/5、每次 10 s；在 bmv2 4/5，通過的 4 次都是 10 s，第 3 次（變體 v3）在 10 s 解除、114 s 被打破（RED_FLAPPED，紅叉，見 P14）。DIY app 在 OVS 5/5、每次 6 s。補充（不計入）：同一個 app 在 exclusive-CPU 的 lab claim 下（主機仍忙）於 bmv2 補跑 5 次，5/5 通過、解除 9–10 s（H/congestion/results_supplementary.tsv，kernel commit 90132fa1）；事先登記的 4/5 不變。補跑不畫在圖上。
- 🟢 依事先規則（PREREG §11）NDTwin 在反應時間上輸：中位數 10 s 對 6 s。兩邊都遠在 90 s 的期限內。
- 🟢 4 秒差距拆開（app log 的時間戳只到整秒；t0＝各次 events.log 的工作負載開始）：NDTwin app 在 t0+6.2–7.3 s 決定搬移（"moving"），t0+8.8–10.1 s 規則裝好（log 寫 "rules in place after 2.5 s"）；DIY app 在 t0+4.4–5.1 s 決定，t0+4.9–5.4 s 已經切換（MOVED）。所以大約 2 s 是偵測比較慢，大約 2 s 是 NDTwin app 自己的等待：它先裝下游、等 2 s 再切入口（controller.py:44 PHASE_GAP_S = 2.0，用在 :556），DIY 只等 0.25 s（app.py:62 BARRIER_WAIT_S = 0.25，用在 :623）。出處：判定計入的 10 個 app log（H/congestion/raw/app_ndtwin_{ovs,bmv2}_t1..t5.<epoch>.log，epoch 1791442401–1791445864）、各次的 events.log、H/raw/ryu_diy-app.*.log。
- INFERRED：只有偵測那約 2 s 可能來自 NDTwin 北向的流量與鏈路速率是 1/256 sFlow 估計值（app 要平滑幾秒才敢動），DIY 讀的是 OpenFlow 的精確計數器。另外那約 2 s 的等待是那個 agent 自己的設計選擇，不是平台的成本。
- 不要比：scripted 對照的 22 s 是 harness 自己排的時間（t0+20 s 再看 2 s 計數器），不是任何 controller 的性質，所以不畫；27 個 scripted 對照全部和事先登記的判定一致（🟢 results.tsv 的 *-ctl 列，generator 每次重新檢查）。左右兩半是不同的觸發、不同的量法，各有自己的 x 軸，秒數不能互相比。
- 🟢 身分：雜湊是在 app 判定之前取的（identity 檔寫於 02:47Z 與 03:43Z：H/raw/identity.20261008T104711.txt、H/congestion/raw/identity.20261008T114343.txt）。kernel binary build/bin/ndtwin_kernel sha256 6fc7e4187df49ee9（揭露，Adam 2026-10-08 接受：2026-10-03 建，沒有綁到 commit；雜湊在 app 判定之前取），bmv2-fast simple_switch_grpc sha256 3ff54b5c1901c9d3，P4 pipeline json sha256 0b19d789d74fc996，原版 Ryu 4.34、Mininet 2.3.0、OVS 3.3.9、iperf3 3.16。P4 proxy 與 NDTwin 的 Ryu app 是從共用工作樹直接跑的 Python。每次判定的工作樹狀態（HEAD 與未提交檔案集合，約 105 個別人的檔案）記在 H/congestion/raw/ndt_status_up_*.txt 第 9–12 行：對照 50ce5022（斷線）、66e84f51（壅塞）；app 判定 767a4b32 與 339bf2c4（後者是 07:13Z 的 trunk merge，只動測試，git diff 767a4b32 339bf2c4 沒有 src/ 或 p4_proxy/ 的檔案）。
- 🟠 binary 與 commit 的關係（READ，git log）：binary 建於 2026-10-03，之後到 trunk 2ece656c 的兩個 commit（c82b063b、46984527）只改 src/ndt_core/power_management/P4PowerStrategy.cpp；不在繞路或寫規則的路徑上（INFERRED）。
- 對帳：左半 NDTwin 可以和 K/doc/audit/2026-08-17_p4-vs-ovs-matched-topology/REPORT.md 比（同一個 10 台／4 主機 cell，各 n=10，全部恢復）。平均對平均：OVS 這次 19.2 s、當時 15.7 s；bmv2 這次 15.8 s、當時 13.7 s。那次切單一方向、h1→h2、每秒 5 個 ping、08-17 的 commit；這次切兩個方向、h1→h3、每秒 100 個 ping、2ece656c 的樹。同一個量級、又全部恢復：是更新，不是推翻；平均高了 2–3.5 s，原因沒有查，不推論。右半是第一次量，沒有可以對帳的舊結果。
- n＝1：右半每臂一個 agent、一個 app；10 s 與 6 s 是這兩個 app 的性質，不是所有 NDTwin app 與 Ryu app 的性質。

### P14 `The same app, unchanged, on bmv2`   form: table
| check | OVS | bmv2 |
|---|---|---|
| app code changed | -- | no (same directory; tree unchanged during the run) |
| PASS, of 5 trials | 5 | 4 |
| pre-registered: same app on P4 (PREREG s.11) | -- | fails: 4 of 5 < 5 of 5 |
| time to relief, median | 10 s | 10 s (4 PASS) |
| write refusals seen | 0 | 0 |
| failed trial | none | v3: relief broke at 114 s |
| DIY arm | 5 of 5, 6 s | n/a (no P4 plane) |
| supplementary rerun, not counted | -- | 5 of 5, median 10 s |
講者備註：
- 🟢 同一個目錄：H/congestion/agents/ndtwin_app（kernel commit 767a4b32 凍結）；判定之後重算 controller.py sha256 8f861d3c、run.sh 4672a502，和凍結的 commit 相同，判定期間這棵樹沒有改。寫它的 agent 從來沒在 bmv2 上試過（NOTES.txt：P4 itself could NOT be tested）。
- 🟢 標記偏離（SCORECARD）：PREREG §7 要兩個平面用同一個 app 標記；實際上 OVS 那幾列是 @767a4b32，bmv2 那幾列是 @339bf2c4，因為 run_congestion.sh 每一組平面取一次 repo HEAD，而 07:13Z 有一次 trunk merge（只動測試）；OVS 的 app-5（07:18Z）其實已經跑在 merge 之後的樹上，標的還是舊標記。app 的 bytes 沒變。
- 🟢 binary 身分（揭露，Adam 2026-10-08 接受）：kernel build/bin/ndtwin_kernel sha256 6fc7e4187df49ee9，mtime 2026-10-03 13:55，沒有綁到 commit；雜湊在 app 判定之前取（identity 檔 02:47Z：H/raw/identity.20261008T104711.txt；03:43Z：H/congestion/raw/identity.20261008T114343.txt）。
- 🟠 binary 與 commit（READ，git log）：從它建好到 2ece656c 之間只有 c82b063b、46984527 兩個 commit，只改 src/ndt_core/power_management/P4PowerStrategy.cpp。
- 🟢 PASS 與中位數：H/congestion/results.tsv 的 ndtwin-app 列，OVS 5/5、每次 10 s；bmv2 4/5，通過的 4 次都是 10 s。DIY 那一列是同一個檔案的 diy-app 列（OVS 5/5、每次 6 s）。
- 🟠 「write refusals seen」不能只看 HTTP 200（install 端點失敗也回 200，problems 第 2 名）。這個 app 每批寫入都檢查回覆的 rejected 與 accepted 數（controller.py:488–499），再輪詢 GET /ndt/get_flow_dispatch_status?request_id=，看到 dispatch_failed 或 switch_outcome.rejected_by_switch 就記一行 dispatch problem 並回滾（controller.py:501–522、553–568）。一次搬移在程式裡是兩批寫入：先下游、再入口（controller.py:553–557）。
- 🟢 10 次判定的 app log（判定計入的那 10 個：H/congestion/raw/app_ndtwin_{ovs,bmv2}_t1..t5.<epoch>.log，epoch 1791442401–1791445864；同目錄裡 epoch 1791454692 之後的 5 個是補跑，不在內）每次都是一行 moving 與一行 rules in place after 2.5 s，沒有任何 dispatch problem、install failed、重送或 loop error。獨立的 checker 也看到 10 次的流都真的換了路徑（results.tsv 的 p0 與 a_path_after；bmv2 第 3 次在 10 s 時也解除了），所以沒有「回 200 但沒裝」的靜默失敗。
- 🟠 OVS 那一格的 0 只代表控制面沒有拒絕，交換機端的拒絕在 OVS 上本來就看不到：OpenFlow 不回覆 FLOW_MOD，dispatch status 在 OVS 上一律記為 unknown；P4 上 proxy 先寫進交換機再回覆，才分得出 accepted／rejected（kit 的 docs/ndt_api.md §42 switch_outcome.why_unknown）。
- 🟢 失敗的那一次（bmv2 app-3，變體 v3，RED_FLAPPED）：10 s 解除後，被搬走的流 A 兩次掉到約 13 Mbit/s，一次 3 s（相對 110–112 s）、一次 5 s（219–223 s），iperf3 -b 隨後補送的突發把一條鏈路推過 40 Mbit/s（114 s 時 s9-s5 58.6 Mbit/s），「保持 120 s」不成立。app 只搬了一次，沒有重送（H/congestion/raw/app_ndtwin_bmv2_t3.1791445099.log；H/congestion/raw/bmv2stall_investigation/q1_iperf_dips.txt）。
- INFERRED：原因未明；唯一指向原因的線索是和另一個 session 的本機 build 時間重疊。那個 Claude session 在這台筆電上背景執行兩次 wolfSSL 建置（make -j4）：第 1 次 07:40:54Z 開始、07:41:22–07:41:34Z 之間結束，第 2 次 07:42:40Z 開始、07:43:47Z 以前結束；兩次停頓 07:41:17–20Z 與 07:43:06–11Z 都落在裡面（H/congestion/raw/bmv2stall_investigation/build_timing_other_session.txt）。同兩段時間 NDTwin kernel 自己 1 s 的迴圈也只在 app-3 慢了 80–210 ms（q3_kernel_loop_cadence.txt）。不指向原因的：RTT ≥5 ms 的事件在 14 次 bmv2 判定裡有 9 次都出現，包括同一條路徑上沒有掉速的 late-1 對照（q3_rtt_events.txt）。那時的 lab claim 沒有標 exclusive CPU（ndt status：exclusive cpu no）。
- 🟠 「NDTwin 沒有週期約 109 s 的動作」（兩次停頓相隔 109 s）：我讀過的週期性迴圈是 1 s（K/src/ndt_core/power_management/DeviceConfigurationAndPowerManager.cpp:891–901）、10 s（同檔 :2769、:2858）、收斂中 5 s／收斂後 30 s（K/src/ndt_core/collection/TopologyAndFlowMonitor.cpp:4850–4888）、60 s（K/src/ndt_core/collection/FlowLinkUsageCollector.cpp:538–563）、P4 proxy 的 2 s 與 5 s（K/p4_proxy/proxy_agent/topology_manager.py:513、:373），都 @2ece656c、工作樹相同；沒有約 109 s 的。這不是完整清單。
- 🟢 依事先規則它照樣算失敗：PREREG §7 只重跑 INVALID_* 列，RED_FLAPPED 不是。所以表上那一列：事先登記的「同一個 app 在 P4 上也能用」不成立（PREREG §11）。
- 🟢 補充，不計入（Adam 2026-10-08 裁定補跑 5 次、標為補充）：同一個 app 目錄（判定後重算 controller.py sha256 8f861d3c、run.sh 4672a502，沒變；標記 @65b14f46＝當時的 repo HEAD），bmv2，變體 v1 v2 v3 v1 v2，lab claim 標 exclusive_cpu=yes（只是 claim 的旗標，主機並不安靜，見下一行；H/congestion/raw/ndt_status_up_p4.1791454661.txt 到 1791456217.txt 共 5 個，工作樹狀態在第 10–13 行）。5/5 PASS，解除 10、10、9、10、10 s，保持期間最忙的鏈路 34.0–36.2 Mbit/s，max_dip 0.917–0.973，比計入的 PASS 列（0.964–0.983）掉得更深（H/congestion/results_supplementary.tsv，kernel commit 90132fa1；raw 在 audit-raw 19daa00a）。補跑當下沒有取雜湊；補跑後取的雜湊和 03:43Z 那份相同（kernel 6fc7e4187df49ee9、bmv2 3ff54b5c1901c9d3、pipeline json 0b19d789d74fc996），kernel mtime 仍是 2026-10-03，git diff 339bf2c4..65b14f46 在 runtime 路徑上是空的（H/congestion/raw/supp_20261008T181724/identity_after_rerun.txt）。表上那一列是它；事先登記的 4/5 與「不成立」都不改。
- 🟢 補跑時的主機（H/congestion/raw/supp_20261008T181724/vmstat.txt，每秒一筆；第 3 行是開機以來的平均，不算）：1,966 s，平均 idle 34.8%，有 241 s 在 swap-in；整段平均 swap-in 約 14 頁/s，不比失敗那次 sar 區間的 18.15 頁/s 高。保持期間主機也忙：app-1 保持期間 18:20:42–47 本地時間 idle 只剩 3%、可執行行程 17–29 個（vmstat.txt:219–224），18:19:57–58 swap-in 16,428 與 14,240 KB/s（vmstat.txt:170–171），解除照樣保持；最高的 59,572 KB/s 落在所有保持區間之外。瀏覽器與桌面 app 在保持區間裡有 281 個「行程×秒」各吃滿 1 核以上（pidstat.txt；SCORECARD.txt 的 ADDENDUM，kernel commit ebc60595）。失敗那次所在的 10 分鐘 sar 區間（15:40–15:50 本地時間）：idle 59.71%（H/congestion/raw/supp_20261008T181724/sar_sa08_1350-1900.txt:15）、swap-in 18.15 頁/s（同檔:48；NDTwin app 判定那一個小時裡最高，整個下午不是最高：14:00 是 63.29（:37）、17:00 是 88.51（:55））、磁碟 await 453.94 ms（:287）。失敗當時根檔案系統 99%（98G 用了 92G，剩 1.8G；另一個 session 15:41:00 自己跑的 df，H/congestion/raw/bmv2stall_investigation/build_timing_other_session.txt）；journal 12:00–19:00 沒有 ENOSPC（H/congestion/raw/supp_20261008T181724/journal_enospc_count.txt:2，數到 0）。
- INFERRED：補跑的保持期間主機一樣忙（idle 掉到 3%、swap-in 到 16 MB/s），解除仍然保持，所以單靠「CPU 負載高」或「swap-in」重現不了 app-3 的停頓。原因未明；唯一指向原因的線索是和另一個 session 的本機 build 時間重疊。
- 建議講法：「事先登記的『同一個 app 在 P4 上也能用』不成立：bmv2 5 次過 4 次、OVS 5 次全過；失敗那次的原因未明。」補跑可以接一句：「之後在 exclusive-CPU 的 lab claim 下補跑 5 次全過；主機其實仍忙（瀏覽器等在每次保持期間都吃滿 1 核以上，最低 idle 3%）。那是補充、不計入，也沒有證實原因。」
- 公平性：DIY 臂沒有 P4 平面，這一頁只能問 NDTwin。NDTwin 獨有的是：同一份程式不改，就在 bmv2 上跑起來，5 次過 4 次；DIY 在 bmv2 上根本沒有對應物。
- 對帳：P05 的 A7 ●⚠ 是讀碼判的（READ）；這是第一個 app 層級的 RAN 證據，比它弱。app 沒有用到 group／meter（P4 上 501）；PREREG §13 擔心的「5-tuple 寫入在 bmv2 上回 200 之後被拒」這次沒有發生。
- ❌ 不說「NDTwin 讓 app 在 P4 上完全可攜」，也不說「其實是 5/5」。

### P15 `When NDTwin is the right pick`   form: table
| you need | NDTwin | nearest alternative | tasks |
|---|---|---|---|
| one API: topology, flows, link load, rule writes | ● on all four (⚠ three, ◌ four) | ONOS+Mininet: ● on three | A1-A4 |
| one app on OVS and bmv2 | ●⚠ (no group/meter on P4) | ONOS+Mininet: ● | A7 |
| power-state and energy experiments | ●⚠◌ | no other ● on P07 (3 ?) | O6 |
| live view of flows and load, your fabric | A2 ●⚠◌ · A3 ●⚠◌ | ONOS+Mininet: A2 ◐ · A3 ● | A2, A3 |
| fault drills: cut links, power off switches | A5 ● · O5 ●⚠ (apps poll) | ONOS+Mininet: A5 ● (link events) | A5, O5 |
| recorded state, replayed in a GUI | ●⚠◌ (graph and flows) | Forward*, IP Fabric*: ● (snapshots) | O8 |
講者備註：
- 🟠 每一列都是 P05–P07 的格子，原樣帶過來，旗標不拿掉。
- 這一頁回答原題：一個 API 同時給拓樸、流、鏈路負載、還能寫規則，再加上節能實驗——這個組合在 P05–P07 只有 NDTwin 每格都是 ●（帶旗標）。ONOS+Mininet 最接近：A1、A3、A4、A5、A7、A8 都是 ●、沒有旗標；差在 A2（每條流的路徑與速率要自己拼）；它不在 P07 比，所以沒有節能那一列的判定。
- 第 2 列：兩邊都是 ●，同一個基準（各自附帶的 P4 pipeline 上，app 不改就跑）。NDTwin 的 ⚠ 是 P4 平面的靜默失敗（C-6、C-7），而且 P4 上 group／meter 回 501，ECMP 類 app 只能跑 OpenFlow。這一列兩邊打平，放在這裡是因為它和第 1、3 列合在一起才是 NDTwin 的組合。
- 🟢 第 2 列的 RAN 證據（P14）：一個壅塞搬移 app 一個 byte 不改，在 OVS 5/5、在 bmv2 4/5 通過（H/congestion/results.tsv；controller.py sha256 8f861d3c）；事先登記的「同一個 app 在 P4 上也能用」以 4/5 < 5/5 判為不成立（H/congestion/PREREG.txt §11、SCORECARD.txt）。失敗那次原因未明；唯一指向原因的線索是和另一個 session 的本機 build 時間重疊（INFERRED；H/congestion/raw/bmv2stall_investigation/build_timing_other_session.txt）。補充、不計入：exclusive-CPU claim 下（主機仍忙）補跑 5 次 5/5 通過（H/congestion/results_supplementary.tsv），沒有重現失敗、也沒有證實原因；事先登記的判定不變。這一格的 ● 是讀碼判的，跑出來的結果比它弱：講這一列時兩個一起講。
- 第 3 列：P07 的其他工具沒有 ●；Forward、CML、IP Fabric 是 ?（公開資料沒寫，不等於沒有）。
- 第 4 列：兩邊都是即時看自己控制的 Mininet fabric；差在每條流的路徑與速率（A2）：NDTwin 內建，ONOS+Mininet 要自己拼。
- 第 5 列：ONOS+Mininet 也能切 link，而且 app 收得到 link 事件；NDTwin 沒有推送、app 要 poll，但它還能在同一個 fabric 上關交換機做演練（O5）。
- 第 6 列：Forward、IP Fabric 在 O8 是乾淨的 ●（快照歷史，不是事件回放）；NDTwin 錄的是 graph 與 flow，內容不同，不是比它們強。

### P16 `When NDTwin is the wrong pick`   form: table
| you need | use instead | NDTwin today | tasks |
|---|---|---|---|
| config, ACL, reachability checks | Batfish, Forward*, IP Fabric* | ○ | O2 |
| vendor NOS behaviour | GNS3, CML*, Containerlab | ○ | O4 |
| a hardware P4 target | ONOS+Stratum | ○ | P8 |
| your own .p4, least friction | P4 tutorials VM, p4-utils | ◐ · ◐⚠◌ | P1, P3 |
| a twin of a network you do not control | Forward*, IP Fabric*, sFlow-RT | no (O1 needs its own Ryu app) | O1 |
| more than 10 switches, 128 hosts | ns-3, Batfish, IP Fabric* | largest measured: 10 / 128 | M7 |
| high packet rates on the P4 plane | OVS plane or hardware | ~16-20 kpps, one flow, fast build | F-bmv2 |
| traffic-aware what-if beyond power | ns-3, RouteNet-Fermi† | ◐ · ◐ switch power-off only | A6, O3 |
| physical switches today | ONOS, Mininet+Ryu | ●◌ coded, no run on record | A8 |
講者備註：
- 🟠 第 1–4 列與第 8、9 列來自 P05–P07 的格子；第 5 列的依據是 O1 的 scope（NDTwin 只鏡像它自己的 Ryu app 控制的網路）；第 6 列來自 M maturity.M7；第 7 列來自 KNOWN-ISSUES F-bmv2：一條流、三跳、fast build 量到的乾淨上限約 16–20 kpps，這個量測不支持任何其他 build、流數或 fabric 的推論。**天花板是 pps 不是 Mbit/s**（換 frame size，Mbit/s 差 16 倍）。❌ 不要把它講成「bmv2 大約幾 Mbps」。
- 第 3 列：產生封包測試（P6）四欄都是 ◐，所以不列；硬體目標（P8）只有 ONOS+Stratum 是 ●，但 Tofino 已停產、Stratum 最後一次 release 是 2022-06-30（M p4.P8 scope）。
- 第 4 列：自己的 .p4 在 NDTwin 上可以跑（13 支 tutorial exercise），但入口是實驗室的 `ndt up p4 --app`（problems 第 1 名）；表項 API 只有 exact／lpm，proxy 重啟會丟（P3 ◐⚠◌）。想快速試自己程式的人，p4-utils 或 P4 tutorials VM 比較省事。
- 第 5 列：要鏡像一個不是 NDTwin 在控制的網路，今天做不到（problems 第 14 名）。
- 第 9 列：實體交換機的程式寫了，kernel 樹裡沒有硬體執行 log（problems 第 18 名）。
- 這一頁的用意：讓老師知道我們清楚 NDTwin 不適合什麼。

### P17 `Real problems, ranked: 1-6`   form: table
| # | problem | hurts | evidence | fix | cost |
|---|---|---|---|---|---|
| 1 | own .p4 only via a lab CLI tied to one machine | P4 | ndt:1602,1642; ndtwin-lab:98; KI G-7 | user-level command; install-time config; clean-VM CI | 1-2 weeks |
| 2 | writes report success that did not happen | app · P4 · ops | api_routes.py:548; KI C-6, C-7, A-4g | non-2xx with reason; wait mode with per-entry result | 3-5 days |
| 3 | zero means idle or blind; slow flows vanish | app · ops | KI C-9, B-x reverse; FlowLinkUsageCollector.hpp:91 | null when silent; window parameter; contract test | 3-5 days |
| 4 | P4 rule changes lost on proxy restart | P4 · app | rule_journal.py:247; main.py:51; KI A-4c | wire the opt-in replay; journal table_entry; kernel reads boot_id | 2-4 days |
| 5 | power cycle cuts hosts, checks green | ops | OVSPowerStrategy.cpp:475; KI B-9 | keep ofport on re-add; ping before "success" | 2-4 days |
| 6 | rule view lags, can show rejected rules | app | KI C-4b, C-4 | fresh read-back from the switch; ghost filter on OVS | 2-4 days |
(Full rows, paths and costs: figures_spec/problems.tsv. All paths @2ece656c. Costs INFERRED.)
講者備註：
- 排序軸：「這件事會不會讓一個開發者放棄」。排序鍵依序比較：① 層級——A 擋住第一次使用 > B 讓人不再相信數字或結果 > C 少了能力但有繞法 > D 少見路徑上的（含只能揭露的）；② 同層內，修得了的排在只能揭露的前面；③ 受影響的開發者種類多的在前；④ 再相同時依嚴重度的判斷（INFERRED）。各名的層級：A＝第 1 名；B＝第 2–7 名（API 說成功其實沒做、0 分不出閒或瞎、規則悄悄消失、檢查全綠但主機斷線、規則視圖過期、錄製悄悄停止）；C＝第 8–15 名；D＝第 16–19 名（第 12 名是 2026-10-08 Adam 裁定新增的 C 層；原來的 12–18 名順延為 13–19）。成本是粗估（INFERRED），以人天計，不含排隊。
- 第 1 名：自己的 .p4 進 NDTwin 的入口是 proxy 讀的一個 knob 檔（K/p4_proxy/mininet/app_package.py:56），kernel 樹裡寫這個 knob 的只有實驗室 CLI `ndt up p4 --app`（K/tools/test_workflow/ndt:1602,1642）。`ndt` 透過 root helper 起 fabric，helper 的預設路徑指向一個使用者的家目錄（K/tools/test_workflow/ndtwin-lab:98；root 才能寫的 /etc/ndtwin-lab.conf 可以覆寫，:88，KNOWN-ISSUES G-7）。OVS 平面三個終端機的啟動方式不經過這支 helper（KNOWN-ISSUES G-7），所以只算 P4。修法：一個寫進文件的使用者層級指令，寫入 app package 並起 proxy 與 bmv2 fabric、不經過實驗室的 root helper；helper 的設定檔由安裝步驟寫入；再加一個在乾淨 VM 上從頭跑自己程式的 CI job。這一名只根據讀碼（READ）：在實驗室以外的機器上照這條路走一次的檢查還沒做。
- 第 2 名：bmv2 表滿時 proxy 回 200 `Failed to add route`（K/p4_proxy/proxy_agent/api_routes.py:548；C-6：每台第 897 筆起全部失敗）；P4 上帶 priority 的刪除全部失敗，呼叫端每次都拿到 200 queued（C-7：12 分鐘 4312 次 POST、100% 回 200）；kernel 的 install 只回 queued，結果要另外查（K/src/ndt_core/http/HttpSession.cpp:2443）；意圖翻譯的 BLOCK_HOST 不檢查安裝結果（A-4g；IntentTranslator.cpp:809）。修法：proxy 對被拒的寫入回非 2xx 並說明原因（bmv2 給的錯誤是空的 UNKNOWN 時，proxy 自己讀一次表列數、講出「表滿」）；kernel 把 proxy 的非 2xx 記為失敗，並提供等待模式回傳逐筆結果。
- 第 3 名：遙測停了時利用率回 0（C-9）、`last_sample_age_seconds` 回 −1.0（C-8，K/src/ndt_core/collection/FlowLinkUsageCollector.cpp:2042）、ifSpeed=0 讓利用率變 null（B-17）、每秒不到約 22 個封包的流在預設 3 秒視窗裡一半時間看不到（B-x 的反向；FlowLinkUsageCollector.hpp:91）。節能 app 正是靠「利用率低」決定關機，所以這是會關錯交換機的形狀（INFERRED）。修法：telemetry_status 不是 live 時 usage 與 age 給 null；視窗做成文件化的參數並回報每條流的取樣下限；加一條契約測試「silent 就不得有數值」。
- 第 4 名：proxy 重啟後 bring-up 的路由會重算回來，消失的是 bring-up 之後 app 的新增與刪除，以及所有 5-tuple 規則，而 twin 看起來完全健康（KNOWN-ISSUES A-4c）。已經有的：proxy 把它接受的路由寫入記在一個 rule journal 裡（K/p4_proxy/proxy_agent/main.py:97,111），journal 也有重放功能，回報四種狀態而不是成功／失敗（K/p4_proxy/proxy_agent/rule_journal.py:247），但重放預設關閉（環境變數 NDTWIN_RULE_JOURNAL_REPLAY，rule_journal.py:56），而且程式裡沒有任何地方呼叫它（main.py:51-53）。還沒有的：`/p4/table_entry` 寫的表項不進 journal（K/p4_proxy/proxy_agent/api_routes.py:841）；proxy 會發 boot_id／table_generation，kernel 沒有讀。修法：proxy 啟動時在 opt-in 底下呼叫既有的重放並回報狀態；table_entry 也記進 journal；kernel 讀 boot_id，在 dispatch status 裡標出「已遺失」。重放預設關閉是刻意的：journal 只記請求、不記原因，重放過期的繞路會裝回沒人要的路徑（rule_journal.py 檔頭），所以修法保留 opt-in。
- 第 5 名：OVS 關機後重新 add-port 沒有指定 ofport_request，埠號重排（K/src/ndt_core/power_management/OVSPowerStrategy.cpp:475）；結果是那台底下所有主機 100% 掉封包，而 reachable、is_up、路徑查詢、`ndt status --check` 四種都說健康（KNOWN-ISSUES B-9，128 主機 OVS 實測重現兩次）。Energy app 的鎖 livelock（A-9，kernel 端已修、app 端仍開）一起修。修法：關機前記下每個埠的 ofport、重新加入時用 ofport_request；回報成功前先 ping 一台主機；app 改用 kernel 的 leaseId 租約。
- 第 6 名：刪掉的規則在 `get_switch_openflow_table_entries` 裡還會被列 9.61 秒（KNOWN-ISSUES C-4b）；OVS 寫入路徑沒有套用「交換機拒絕的規則不要當成存在」的過濾（C-4；OVS 這一側是讀碼推論，沒有實跑）。

### P18 `Real problems, ranked: 7-12`   form: table
| # | problem | hurts | evidence | fix | cost |
|---|---|---|---|---|---|
| 7 | recording stops silently | ops | integration-matrix.md:147; KI B-3 | reconnect with backoff; refuse instead of 200 | 1-2 days |
| 8 | topology must be declared; OVS copy fixed | ops · app | TopologyAndFlowMonitor.cpp:2373 | OVS fabric from model; undeclared vertices; 64-switch run | 1.5-2 weeks |
| 9 | what-if narrow, no check on record | ops · app | energy_saving_simulator.cpp:467 | link-removal input; predicted vs measured run | 1-2 weeks |
| 10 | P4 plane narrower than OpenFlow | P4 · app | P4RoutingStrategy.cpp:27; api_routes.py:880 | ternary/range; ECMP selector; table size | 2-3 weeks |
| 11 | built on an unmaintained controller | app · ops | intelligent_router.py:618; Ryu 4.34 (2019) | port to os-ken, current Python | ~1 week |
| 12 | rates are sampled estimates; exact counters unused | app · ops | FlowLinkUsageCollector.cpp:1339; ovs_4host_topo.py:164 | counter samples under Mininet; P4 emitter too | 4-6 days |
講者備註：
- 第 7 名：Network-State-Recorder 一次 connection refused 就永久停止、之後只產生空檔（K/doc/2026-08-14_cross-component-integration-matrix.md:147）；kernel 的 /ndt/historical_logging 在 Mininet 下一列都不寫（KNOWN-ISSUES B-3）。修法：recorder 以 backoff 重連並記錄存活；historical_logging 在 Mininet 下要嘛寫、要嘛回 4xx。
- 第 8 名：拓樸檔沒有的交換機只印 WARN、被忽略（K/src/ndt_core/collection/TopologyAndFlowMonitor.cpp:2373）；OVS 副本是寫死的 10 台（Network-Traffic-Generator@6e3f388 testbed_topo.py:39-48），只有 bmv2 的 builder 讀拓樸模型；量過最大 10 台／128 主機。修法：OVS fabric 也從模型建（重用 K/p4_proxy/mininet/topo_from_json.py）；發現的交換機以「未宣告」頂點加入；兩個平面各做一次 64 台的規模量測。
- 第 9 名：模擬器的輸入只有「要關掉的交換機集合」（Energy-Saving-App@9facb78 src/sim/energy_saving_simulator.cpp:467），每個案例要掛 NFS、要 root（Simulation-Platform-Manager@b7efd93 app.cpp:286）；預測和實測的比較沒有紀錄（kernel 與 Energy-Saving-App 的樹裡都找不到）。修法：加「拿掉鏈路」的輸入（BFS 改路已經有）；在 10 台 fabric 上做一次「預測 vs 實測」；案例改用 HTTP 傳。分項：2–3 天、1–2 個實驗夜、約 1 週。
- 第 10 名：P4 上 group／meter 被拒（P4RoutingStrategy.cpp:27-33），ternary／range／optional 回 501（api_routes.py:880），每張表 1024 筆（K/p4_proxy/p4_src/ndtwin_switch.p4:344,360）。修法：table_entry 支援 ternary／range（bmv2 本身支援，2–3 天）；ndtwin_switch.p4 用 action selector 做 ECMP（1–2 週）；表大小做成建置參數（1 天）。
- 第 11 名：OVS 平面靠 Ryu 4.34（最後一個 tag 是 2019-10-01）跑在 Python 3.8（M maturity.M3、M8；K/intelligent_router.py:617-618）。修法：把 intelligent_router.py 移到 os-ken（OpenStack 維護的 Ryu 分支，API 同形），換到現行 Python，重跑 OVS 的 live 閘門。
- 第 12 名（2026-10-08 Adam 裁定新增，C 層）：🟠 Mininet 下 NDTwin 北向的流量與鏈路速率只來自 1/256 sFlow flow sample（kit 的 docs/ndt_api.md §3 left_link_bandwidth_source 的註記：Under Mininet only flow samples drive the update；§4）。精確的計數器其實有：kernel 會解析 sFlow 的 interface counter sample（ifIn／ifOutOctets，K/src/ndt_core/collection/FlowLinkUsageCollector.cpp:1295–1332），但在 Mininet 下直接跳過（:1339–1344）；OVS bridge 刻意設 polling=0，旁邊的註解寫「不要修」，理由正是 kernel 會跳過（K/tools/test_workflow/ovs_4host_topo.py:93、164–170），兩個設定綁在一起；P4 proxy 合成的 sFlow 只有 flow sample（K/p4_proxy/proxy_agent/sflow_emitter.py:78）。每條規則的 byte_count 在 GET /ndt/get_switch_openflow_table_entries 裡有，但那是 kernel 最近一次輪詢的值，「比交換機落後最多約十秒」（kit 的 docs/ndt_api.md:1307–1309），也沒有換算成速率；3.3 s／9.6 s 只是新增／刪除後在這個 endpoint 上看得到的延遲（ndt_api.md §5；OVS、kernel 4c9e0be1）。P4 proxy 自己的 REST（:8081）GET /p4/counter/{name} 已經能回 egress_port_counter 的精確 bytes（K/p4_proxy/proxy_agent/api_routes.py:967–994），但不在 kernel 的 API 上、也不是速率；kernel 沒有 port 統計的 route（K/src/ndt_core/http/HttpSession.cpp:348–527）。另外，kernel 的 counter sample 解析用的是標了廠商的位移（Brocade type 2、HPE type 4，K/src/ndt_core/collection/FlowLinkUsageCollector.cpp:1280–1286），它能不能正確讀 OVS 的 counter sample 沒有測過。以上都 @2ece656c。
- 🟢 第 12 名的實作證據（P11–P13）：同一個壅塞任務，NDTwin app 10 s、讀 OpenFlow 精確計數器的 DIY app 6 s（H/congestion/results.tsv）；4 s 裡約 2 s 是偵測、約 2 s 是 NDTwin app 自己的安裝等待。INFERRED：只有偵測那約 2 s 可能來自取樣估計值。
- 第 12 名的排序（INFERRED，依 P17 備註的排序鍵）：C 層、修得了；影響 app 與 ops 兩種（節能 app 靠利用率決定關機）→ 排在只影響一種的第 13–15 名之前；在同樣影響兩種的第 8–11 名之後：第 8–10 名是整個能力缺席（更大的拓樸、拿掉鏈路的 what-if、P4 表項種類），第 11 名是 OVS 平面綁在 2019 年後沒有維護的 Ryu 與 Python 3.8；這一個是慢約 2 s、要多寫平滑程式，而且有繞法（自己輪詢 §5 的 byte_count，像實作 agent 的 truth.py；這個繞法沒有在閉迴路裡測過）。
- 第 12 名的修法：A（較便宜）＝ Mininet 下 kernel 收 counter sample、OVS bridge 開 polling（兩個一起改、註解一起改），P4 proxy 從 egress_port_counter 發 counter sample；每個數字帶來源與取樣年齡；手冊寫明閉迴路 app 該用哪個。成本：OVS 2–3 天＋P4 2–3 天（INFERRED）；OVS 那 2–3 天的前提是既有的解析器讀得懂 OVS 的 counter sample（沒有測過，見上）。B 只在 A 不夠時：每條鏈路從 port 計數器、每條規則從 byte_count 差值算速率。

### P19 `Real problems, ranked: 13-19`   form: table
| # | problem | hurts | evidence | fix | cost |
|---|---|---|---|---|---|
| 13 | failures reach apps only by polling | app | no push in src/; topology_manager.py:415 | event stream (SSE); LLDP interval sweep | ~1 week |
| 14 | mirroring needs NDTwin as the controller | ops | intelligent_router.py:617; O1 | read-only observer mode | 3-6 weeks |
| 15 | API open to the network, no auth | ops | ControllerAndOtherEventHandler.cpp:100 | bind 127.0.0.1; token; narrow CORS | 1-2 days |
| 16 | any app can release another's lock | app | KI B-2 | owner check on release and renew | ~2 days |
| 17 | intent translator: one cloud LLM, no run on record | ops | LLMAgent.cpp:138 | configurable endpoint; one end-to-end run | 1-2 days |
| 18 | physical switch path: no run on record | ops · app | GraphTypes.hpp:140; no hardware log | disclose: no testbed; mark "unverified" | < 1 day |
| 19 | no P4 hardware target; bmv2 pps ceiling | P4 | ndtwin_switch.p4:32; KI F-bmv2 | disclose: target discontinued; state pps | -- |
講者備註：
- 第 13 名：src/、include/ 裡沒有 websocket 或 event-stream 之類的推送機制；P4 上 LLDP 每 5 秒一次（K/p4_proxy/proxy_agent/topology_manager.py:373），鏈路在最後一個 beacon 之後 15 秒判斷為斷（:1680、:2026；每 5 秒檢查一次，:422），也就是切斷後約 10–20 秒；KNOWN-ISSUES D-2 實測的 bmv2 偵測 10.7–14 秒在這個範圍內。修法：kernel 加 SSE 事件流（link、switch、規則結果）；跑 D-2 的 beacon 間隔掃描（knob `NDTWIN_P4_BEACON_S` 已在，掃描沒有跑過的紀錄）。
- 第 14 名：鏡像的前提是 NDTwin 自己的 Ryu app 安裝所有路由（K/intelligent_router.py:617-618）。修法：唯讀 observer 模式——拓樸從既有 controller 的 REST（ONOS、原版 Ryu）讀、遙測從交換機 sFlow，寫入關閉。需要先做設計決定（twin 對不是它控制的網路能做什麼）。
- 第 15 名：REST 伺服器綁在 0.0.0.0:8000（K/src/ndt_core/event_handling/ControllerAndOtherEventHandler.cpp:100），CORS 是 *（K/src/ndt_core/http/HttpSession.cpp:305），沒有認證——關交換機、切鏈路的 route 都在同一個 port。推論（INFERRED，未測）：同網段的任何主機都能呼叫它；瀏覽器裡的網頁也能送簡單 POST。繞法是防火牆，所以歸在 C 層。修法：預設只綁 127.0.0.1、要放寬得明確給旗標；會改變狀態的 route 要 bearer token；CORS 只開給 GUI 的 origin。
- 第 16 名：任何 app 都能釋放或續約別人的鎖（KNOWN-ISSUES B-2 第 2 部分；第 1 部分已修）。只有一個 app 時不會踩到；兩個 app 同時跑（例如 TE 與節能）就會，所以歸在少見路徑。
- 第 17 名：唯一的端點寫死 https://api.openai.com（K/src/ndt_core/intent_translator/LLMAgent.cpp:138），預設模型在 K/src/main.cpp:418；預設關閉，開啟 AI 的執行沒有紀錄（測試 stack 一律以 --no-ai 啟動）。修法：可設定的 OpenAI 相容 base URL（本機模型也能接）＋一次端到端測試。
- 第 18、19 名是「揭露」，不是修法，理由：
  - 18：程式寫了 HPE5520 與 Brocade 兩種（K/include/common_types/GraphTypes.hpp:140-144），但 kernel 樹裡沒有任何硬體執行 log，實體 testbed 停用（K/doc/2026-01-02_ndt_api.md:1598-1599 那句只講電源分支）。沒有硬體就沒辦法驗證；能做的是在 `--help` 與 get_graph_data 標出「testbed 模式未驗證」，拿到硬體的第一天就跑。
  - 19：程式只有 bmv2 v1model（K/README.md:5；K/p4_proxy/p4_src/SPEC.md:6-7；K/p4_proxy/p4_src/ndtwin_switch.p4:32）；主要的硬體 P4 目標（Tofino）已停產（M p4.P8 ONOS+Stratum scope）。bmv2 的天花板用 pps 講：約 16–20 kpps，一條流、fast build（KNOWN-ISSUES F-bmv2；這個量測不支持其他 build 的數字）。以後的選項是評估 P4-DPDK 或 eBPF 後端，以月計。

### P20 `What we fix first, and what we disclose`   form: figure `next/fig_p20_roadmap`
Figure spec: figures_spec/roadmap.txt (columns NOW / NEXT / LATER + grey DISCLOSE; lanes "Trust what the API
says", "See failures and load in time", "Run it anywhere", "Model more of the network"; one box per problem
rank, label = short fix + #N; fill = persona hurt most; four dependency arrows). Data: figures_spec/problems.tsv.
Column rule (roadmap.txt): NOW if every part of the fix is under ~1 week; NEXT if any part is ~1 week or more;
LATER if it needs a design decision first; DISCLOSE if not fixable with what exists.
講者備註：
- 這張圖是 P17–P19 的修法排程（INFERRED 的計畫，不是已完成的事）。不寫日期。
- NOW（每一部分都不到約一週）：#2 誠實的寫入結果、#3 遙測瞎了就給 null、#4 接上既有的重放與 boot_id、#5 OVS 電源循環保留埠號、#6 即時讀回、#7 recorder 重連、#12 Mininet 下用計數器算鏈路速率、#15 只綁本機加 token、#16 鎖的 owner 檢查、#17 可設定的 LLM 端點。讓人不再相信 twin 的六個（#2–#7）全部在這一欄。
- #12（2026-10-08 Adam 裁定新增）放 NOW 的理由：用較便宜的修法 A，兩部分各不到一週（kernel 收 counter sample 加 OVS 開 polling 2–3 天；P4 proxy 發 counter sample 2–3 天，INFERRED），依欄位規則是 NOW。不畫箭頭：它和 #3 改的是同一個收集器，但兩個修法誰都不需要誰先完成。
- NEXT（有一部分約一週以上）：第一個是 #1（排名第一但要 1–2 週，因為是打包加 CI），接著 #8 從模型建 OVS fabric、#9 what-if 加鏈路並對實測、#10 P4 表項種類與 ECMP、#11 換 os-ken、#13 事件流。
- LATER 只有 #14 observer 模式：需要先決定 twin 對它不控制的網路可以做什麼。
- DISCLOSE：#18 實體交換機（沒有 testbed）、#19 硬體 P4 目標（已停產）——修不了，理由在 P19。
- 箭頭讀作「被……需要」（圖例 needed by）：#2→#13（事件流要帶誠實的規則結果）、#1→#11（先有乾淨 VM 的 CI，再換 os-ken，CI 一起蓋到）、#8→#14（observer 需要未宣告頂點）、#3→#9（驗證 what-if 需要會說「我瞎了」的遙測）。

## 3. Open items for the orchestrator (not slide content)

Contested matrix cells, ruled and applied in M (CHANGES_final.tsv, source "judge-r1 finding N"):
1. ops O5 IP Fabric stays ●; note rewritten to the vendor MCP demo page claim (finding 2).
2. ops O7 read as "a plain-language request changes the network the tool runs, emulated networks included":
   GNS3 ● (3.1 pre-release, footnote on P07), CML ●, IP Fabric ◐, Forward ◐, NDTwin ●⚠◌ (finding 3).
3. app A7 ONOS+Mininet ● and NDTwin ●⚠ kept and ruled together; ONOS note/scope and NDTwin scope updated
   (finding 4). If the bar becomes "every shipped app ports", both go to ◐ together.
4. p4 P6 NDTwin ○ -> ◐, same basis as the three competitors (finding 5).
NDTwin scope texts in M that are stale or self-contradictory (cell glyphs unaffected):
5. ops O8 scope still cites B-3; B-3 is the kernel logger, off the NSR path; the real ⚠ is NSR stopping after
   one refused connection (integration matrix :147). Notes on P07 use the latter.
6. app A3 scope says "(A-4f, open)" and later "A-4f fix is merged in 2ece656c (36e3d78a)"; 36e3d78a is an
   ancestor of 2ece656c. P05 notes rest ⚠ on C-9/B-17 only.
7. maturity M3 NDTwin text includes material excluded by §0 rule 7; P08 uses only the release status.
Stale line numbers in KNOWN-ISSUES (ids still valid, lines moved): C-8 cites FlowLinkUsageCollector.cpp:1874
(now :2042); D-2 cites topology_manager.py:137 (now :373; timeout logic :1680, :2026, :422). This template
cites the current lines. A link goes down 15 s after its last beacon, about 10-20 s after a cut; D-2's
measured 10.7-14 s is within that window.
Other: README.md (trunk) says both planes support group and meter entries; P4RoutingStrategy.cpp:27-33 refuses
them on P4. Not a slide item, noted for the owner.
Problem rank 1: a read-only check of the own-program path off the lab machine (KNOWN-ISSUES G-7) has not been
done; the rank rests on READ evidence only.
Landscape positions marked unsure: 8 rows (figures_spec/landscape.tsv column `unsure`). The P04 bottom row is
named "none"; the axis title carries the meaning.
Generators: the five figure generators read their specs at run time. The generator to-dos listed in v0.2 (P04 "none" row, no NDTwin hollow marker, "framework (draft)", NDTwin in its cell, 8 unsure rows; P20 arrow legend from roadmap.txt, no two arrows on one line, #11 inside NEXT; P02 traffic-generator arrow to Mininet+OVS only, proxy sFlow arrow from the proxy box) are done; redcheck_1021.py has a case for each that a spec edit could undo.
Hands-on generators: make_p10_setup.py and make_p13_relief.py read their data at run time and are red-checked in
redcheck_1021.py (P10: 6 cases, P13: 10 cases, plus one control each).
8. Hands-on binary identity -- CLOSED, Adam 2026-10-08: accepted as a disclosure. The disclosure (P13 and P14
   notes): kernel build/bin/ndtwin_kernel sha256 6fc7e4187df49ee9..., built 2026-10-03, not bound to a commit;
   the hash was taken before the app trials (identity files 02:47Z and 03:43Z); the only commits between its
   build and 2ece656c (c82b063b, 46984527) touch src/ndt_core/power_management/P4PowerStrategy.cpp alone (READ,
   git log). The other half of the old release condition was already closed: release and teardown lines are in
   the run logs, the results are committed (dcff37b6, 80a4e29f, 9335b189, 65b14f46, 90132fa1, ebc60595) and the raw
   trees are archived in the audit-raw branch (ed24e5e5; supplementary rerun 19daa00a; host and build-timing
   evidence c6bf496e; local, not pushed).
9. Hands-on problem row -- APPLIED as rank 12, tier C (Adam 2026-10-08: "新增第 19 列，C 層", i.e. a 19th row).
   Placed by the P17 ranking key: tier C, fixable, two personas (app, ops) -> before the one-persona ranks
   13-15; after the two-persona ranks 8-11 on severity (INFERRED: about 2 s slower detection and extra app code,
   with a workaround, against three capabilities missing outright (ranks 8-10) and a controller pinned to an
   unmaintained Ryu on Python 3.8 (rank 11)). Old ranks 12-18 are now 13-19; tier
   C is 8-15 and tier D 16-19. Text, evidence and fix: P18 notes and figures_spec/problems.tsv rank 12; roadmap
   box NOW (two parts of 2-3 days each), no arrow. Rank cross-references renumbered: P16 notes (13 -> 14,
   17 -> 18), P17 tier line, P19 rows and notes, P20 notes (#12 -> #13, #13 -> #14, #14-#16 -> #15-#17,
   #17-#18 -> #18-#19, arrows #2->#13 and #8->#14), roadmap.txt, redcheck cases.
