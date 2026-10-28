# NDTwin report deck -- 2026-10-28 -- "P4 support since 10/14" -- content template

v1.0, written 2026-10-26 (UTC), for the meeting of Wednesday 2026-10-28. Single source of truth for page order,
page form, table cells, figure specs and speaker notes; generator/build_deck_1028.js reads §1 and §2 and types
nothing about a page itself. Format follows NDTwin-slide-template-1014.md (§0 rules, §1 page table, §2 per page,
§3 open items). Sources live in this file only: the pptx and the speaker script carry no commit, PR number, path
or run id.

Sources (all read for this draft; K = the NDTwin-Kernel repository, W = the PR tree checked out at
K/scratch/overnight-2026-09-05/wt-merge-head, L = K/scratch/overnight-2026-09-05/logs/nslab-a24-1026/live):
- Code and user docs: W at 5ab1c66a (git commit sha). Its tree (cd3bd43b) is identical to the PR head on
  GitHub, a9d8925f, which is the commit the lab VM ran (`git rev-parse a9d8925f^{tree} HEAD^{tree}` in W: both
  cd3bd43bdb4324727bf3ee6ce906dfbaa1d35416). Every W path:line below is at 5ab1c66a.
- The 10/14 deck's NDTwin pin: trunk 3a47bdb7 (NDTwin-slide-template-1014.md header). "New since 10/14" is
  checked against it: `git show 3a47bdb7:p4_proxy/proxy_agent/api_routes.py | grep '^@router'` has no
  /p4/register and no /p4/direct_counter; `git show 3a47bdb7:doc/2026-01-02_ndt_api.md` has no
  `ryu_rules_lost` and no "malformed flow entry"; `git diff --stat 3a47bdb7 HEAD -- tools/p4_exercise` adds
  thrift_cli.py (501 lines) and convert.py +376 lines. 3a47bdb7 is an ancestor of W HEAD.
- PR descriptions, read with `gh pr view 41|42 --repo Adam010341/NDTwin-Kernel-P4 --json title,body,...`
  on 2026-10-26: PR 41 "p4_proxy: read registers and direct counters, bind bmv2 to 127.0.0.1", MERGED
  2026-10-23T10:56:11Z, squash 12e5c080; PR 42 "p4_proxy: honest P4 write replies, CIDR destinations and
  Ryu-path loss notices", OPEN, head a9d8925f.
- Offline evidence (RAN, throwaway bmv2, stock and fast, not on an NDTwin fabric), private records on local
  trunk (not public): K/doc/audit/2026-10-17_p4-batch-1017/GATE.md:50 ("register read 41/41 and
  impostor/replace 27/27 checks; int-v1 17/17, ONTAS 12/12 verdicts", gate at merge 67146b0f);
  K/doc/audit/2026-10-16_p4-register-read/DESIGN.md:38-48, :59-60 (bmv2's P4Runtime answers every register read
  UNIMPLEMENTED; direct-counter reads work); DESIGN-thrift.md:208-212 (register reads 4737 read back; P4Runtime
  reads, GET /p4/direct_counter included, succeed before and after the Thrift reads). Binaries named there: stock
  /usr/local/bin/simple_switch_grpc sha256 327fa7d1..., fast /usr/local/bmv2-fast/bin/simple_switch_grpc sha256
  3ff54b5c... (DESIGN.md:20-23).
- Live evidence (RAN, lab VM, stock bmv2, functional only, no performance number): L. Identity
  (L/71_L3_rerun/00_identity.txt:2-7, L/72_L3_F3ab/00_identity.txt:2-7): kernel repo commit a9d8925f (git
  commit sha) plus 2 porcelain lines (p4_proxy/mininet/bmv2_binary_override modified to the stock binary; an
  untracked runs/ directory); bmv2 /usr/local/bin/simple_switch_grpc, `--version` 1.15.5-583e76e4, sha256
  1d7d356bbb0251a7...; f_checks.py sha256 df6f9ff59d76c37b...; f3ab.py sha256 f50e8227fa0c51ca....
  The VM ran with two workarounds, the /home/adam traffic-generator symlink and a chown of .test_run/logs
  (identity label line 1); those are the two problems on P07. Fabric: 10 switches, 4 hosts
  (L/72_L3_F3ab/f_checks.log:1-2). Sequence: L/progress.log.
- Live evidence, second run (RAN, a second fresh lab VM, stock bmv2, functional only, no performance or timing
  number): A = K/scratch/overnight-2026-09-05/logs/nslab-a25-1027/guest/logs. Identity (A/B1/00_identity.txt:1-8):
  kernel repo commit f8cda51c (git commit sha) plus the same 2 porcelain lines; bmv2 /usr/local/bin/simple_switch_grpc
  `--version` 1.15.5-583e76e4, sha256 1d7d356bbb0251a7... (same binary as the first run); b1.py sha256 2c0f42d9....
  At f8cda51c, p4_proxy/proxy_agent/ and tools/p4_exercise/ are byte-identical to W 5ab1c66a (`git diff --stat
  5ab1c66a f8cda51c -- p4_proxy/proxy_agent tools/p4_exercise` is empty); f8cda51c differs from W only in
  bring-up files (p4_proxy/mininet/ntg_bmv2_topo.py, topo_log.py, tools/test_workflow/ndt, ndtwin-lab,
  tools/ndt_serve/verbs.py and their tests), i.e. the files of P07 rows 1-2. Not said on any slide or note
  (§0 rule 5; Adam's instruction): P07 stays as observed in the first run. Sequence: A/progress.log.
- Reconciliation: the CIDR result updates KNOWN-ISSUES B-2c's 2026-08-31 live run (then CIDR => 400; now a
  well-formed destination prefix => 200 and a /24 entry; malformed forms still 400, W/doc/KNOWN-ISSUES.md:1270-1279).
  The rule-loss live run is the first live run of `ryu_rules_lost`: A-4c lists live verification as not yet
  done (W/doc/KNOWN-ISSUES.md:366-367); it does not overturn the offline trials (A-4c :363-365). The heartbeat
  re-run (L/62_L2_08_heartbeat_h1h4, PASS) repeats a check shown before 10/14 and is not a new result.
- Format model: NDTwin slide material 1014/ (template, generator, speaker script v2). Figure specs:
  figures_spec/rules_lost_flow.txt (P04), figures_spec/read_path.txt (P05), figures_spec/next.txt (P09).

[Co-developed with claude code -- Adam]

## 0. Rules (Adam's standing rules for these decks)

1. Every page is one figure or one table. The only free text on a slide is its title (and "Adam" on the title
   page, as on 930 and 1014). Table cells are label -> value, never sentences. Everything else goes into the
   speaker notes.
2. Figure pages: title plus one figure filling the content area; the figure's canvas title is the slide title.
   No caption, kicker, chip or verdict word.
3. Few words on figures: title, axes or box names, value labels, a few key annotations. No grey corner text:
   no commit, date, run id, source line or generator name (figstyle_1028.save_all refuses one).
4. No commit hashes anywhere in the pptx or the speaker script, speaker notes included. Sources live only in
   this file, above the "講者備註" line of each page block (the build copies from that line on).
5. New features only. Excluded as fixes or hardening: write replies that used to say 200 on failure (now 502);
   priority / dpid validation; Release-build warnings; in_port masking; binding bmv2/proxy to 127.0.0.1;
   table-entry journal replay after a proxy restart; the modify-priority landing fix.
6. Only the increment since 10/14. Not again: ternary/range/optional writes, 502 with P4Runtime error codes,
   detect-only link down, the P4 health check.
7. Technical decisions and final results only: no timeline, no debugging story, no review or CI process words,
   no PR numbers.
8. "Ran it" and "read it, not executed" never share a table. Every result row says how it was verified: live
   on the lab VM, or offline against throwaway bmv2.
9. No sugarcoat: real weaknesses are on a slide (P07, P08), each with a next step.
10. Page and word count low. English slide titles (<= 45 chars), Traditional Chinese speaker notes.
11. generator/redcheck_1028.py fails on any slide, note or script text with a 7+ hex-character commit-like
    token, a "PR #" / "#4x" reference, a rule-5 fix item or a rule-6 repeat, and on a date stamp on a figure.

## 1. Page order (9 pages)

| # | id | title (= on-slide title) | chars | form | evidence | status |
|---|---|---|---|---|---|---|
| 1 | P01 | P4 support since 10/14 | 22 | title | -- | ready |
| 2 | P02 | New P4 capabilities since 10/14 | 31 | table | RAN (live, lab VM) | ready |
| 3 | P03 | Rules wiped by a push: report, not replay | 41 | table | READ | ready |
| 4 | P04 | How the rule-loss notice reaches the app | 40 | figure `p4/fig_p04_rules_lost` | READ | ready (rules_lost_flow.txt) |
| 5 | P05 | Reading registers and direct counters | 37 | figure `p4/fig_p05_read_path` | READ | ready (read_path.txt) |
| 6 | P06 | Verified live on a fresh lab VM | 31 | table | RAN (live, lab VM) | ready |
| 7 | P07 | What a fresh machine exposed | 28 | table | RAN (live, lab VM) | ready |
| 8 | P08 | Limits of the new features | 26 | table | READ | ready (added page, §3 item 1) |
| 9 | P09 | What comes next | 15 | figure `next/fig_p09_next` | INFERRED (plan) | ready (next.txt) |

form count: title 1, figure 3 (P04, P05, P09), table 5.
Narrative: what is new (P02) -> the one design decision (P03) and how it works (P04) -> the new read path
(P05) -> what ran live (P06) -> what a fresh machine broke (P07) -> what the new features still cannot do
(P08) -> what we do next (P09).

## 2. Per page: content and speaker notes

Each block: the table (table pages) or the figure spec (figure pages), then "Sources" (this file only), then
the speaker notes from the line "講者備註" to the end of the block, which the build copies into the pptx.

### P01 `P4 support since 10/14`   form: title
Slide: the title and "Adam".
Sources: scope = everything in §0 rule 5/6 filters applied to PR 41 and PR 42 (header).
講者備註：
- 這份只講 10/14 之後 P4 這邊新增的功能，修 bug 的部分不放。
- 新功能有五個：讀 register、讀 direct counter、P4 上可以下 CIDR 目的地、pipeline 重推之後 app 可以看到哪些規則被清掉、把兩篇論文的 P4 app 轉成 NDTwin 的套件。
- 五項都在全新的實驗室 VM 上、用一般版 bmv2 實際跑過，只驗功能，沒有效能或時間數字。最後兩頁講還不夠的地方和下一步。

### P02 `New P4 capabilities since 10/14`   form: table
| capability | a developer can now | verified |
|---|---|---|
| register read | read a P4 program's registers: GET /p4/register/{name} | live, lab VM |
| direct counter read | read a table's direct counter: GET /p4/direct_counter/{name} | live, lab VM |
| CIDR destination | send a /24 through the Ryu-compatible flow API on P4 | live, lab VM |
| rule-loss notice | see per switch which Ryu-path rules a push wiped | live, lab VM |
| paper-app converter | bring 2018-19 tutorial and Thrift-CLI apps: int-v1, ONTAS | live, lab VM |

Sources:
- Row 1: W/p4_proxy/proxy_agent/api_routes.py:1604-1606 (route), :1611-1616 (bmv2 only, through bmv2's Thrift
  service, `source: "bmv2-thrift"`), :1627-1631 (two checks before every read), :1736-1743 (liveness probe, then
  the expected device id and Thrift port), W/p4_proxy/proxy_agent/bm_thrift.py:285-292 (bm_mgmt_get_info on the
  read's own connection must answer the expected device id and Thrift port). Route is on the P4 proxy (REST :8081,
  W/p4_proxy/proxy_agent/main.py:2767), not on the kernel's :8000: `grep -rn "p4/register" W/src W/include` is
  empty. PR 41 body: "registers are read through bmv2's Thrift service, checking on every read that the switch is
  alive and is the expected device". Verified offline: GATE.md:50 (41/41, impostor/replace 27/27, stock and fast).
  The 41 checks compare VALUES, not just status: audit-raw-1017
  scratch/overnight-2026-09-05/logs/gates-0910/merged-trunk-1017/chk_trial_reg.py:21-25 (r_mark[0] == [4737], the
  whole array == [4737] + 15 zeros, a range, the alias) and reg.trial.log (last line "TRIAL-REG CHECKS: 41 ok, 0
  failed"). Verified LIVE (second run): A/B1/b1_reg.log:5-19 -- the tutorials link_monitor package brought up
  with `ndt up p4 --app`, 4 switches; GET /p4/register for byte_cnt_reg and last_time_reg equals simple_switch_CLI
  register_read on each switch's Thrift port, all 4 switches (:5-12); one cell (:13); s1 byte_cnt_reg grew by 980
  after 10 pings (:14); controls: unknown name 404 (:15), index 8 of an 8-cell array 400 (:16), stopped switch 503
  with no values (:17-18); "ALL PASS b1 reg: 16 checks" (:19). Caveat (notes and Q&A only): last_time_reg was all
  zeros on every switch (:6, :8, :10, :12), so the comparison with real values rests on byte_cnt_reg.
- Row 2: api_routes.py:1491-1500 (route, one wildcard P4Runtime read of the whole table), :1508-1509 (null,
  never 0, for a unit not counted). Verified offline, counts compared: K/doc/audit/2026-10-16_p4-register-read/
  DESIGN.md:246 (the route's answers (100, 0 B, 0 pkt), (200, 201, 3), (0, 134, 2) equal thrift's counter_read by
  handle, both builds), :250 (hc_main: 0/0 -> 335/5, equal to thrift). The 1017 gate's register trial checks only
  that the route answers 200 next to the Thrift reads (chk_trial_reg.py:29-30; DESIGN-thrift.md:212); the counts
  rest on DESIGN.md:246-250 (10-16 branch code). Verified LIVE (second run): A/B1/b1_dc.log:1-20 -- baseline
  10-switch / 4-host fabric; after 10 pings h1 -> h2 every MyIngress.ipv4_lpm entry on the path grew by exactly
  10 packets / 980 B (s1, s2, s6 for 10.0.0.2; s1, s2, s5 for 10.0.0.1; :6-11, :13-15); controls: unknown name 404
  (:16), unknown dpid 404 (:17), stopped switch 503 with no entries (:19); "ALL PASS b1 dc: 9 checks" (:20).
- Row 3: W/doc/2026-01-02_ndt_api.md:1952-1954 (on P4 a CIDR destination-only match is installed as that
  prefix, longest prefix wins, host bits cleared); KNOWN-ISSUES B-2c :1276-1279. Verified live: P06 rows 1-2.
- Row 4: ndt_api.md:656-668, :690-698; W/p4_proxy/proxy_agent/topology_manager.py:1462-1469 (record, log line
  "NOT replayed"), :2349 (served in switch_state); W/src/ndt_core/power_management/P4RulesLost.cpp:99-101, :117
  (kernel ERROR line, copy onto the graph node). Verified live: P06 rows 3-5.
- Row 5: W/tools/p4_exercise/convert.py:262-296 (the 2018-06..2019-08 tutorials topology format; ONTAS is
  named as one), :915-930 (`--thrift-commands`: CLI table commands translated and appended to the switch's
  runtime file; int-v1 named), :440-445 (older p4info suffix, int-v1), :689-700 (multi-file programs, int-v1);
  W/tools/p4_exercise/thrift_cli.py:1-16 (table_add and table_set_default translated, everything else refused
  by name). PR 41 body: "can convert apps written for the 2018-19 tutorials topology format or driven by Thrift
  CLI scripts, which brings in the int-v1 and ONTAS paper apps". Verified offline: GATE.md:50 (int-v1 17/17, ONTAS
  12/12 verdicts). The verdicts compare frames byte for byte: K/doc/audit/2026-10-16_p4-paper-apps/
  offline_int_v1.py:37-50 (P1-P7: translated package vs the app's own CLI path, and vs int-v1's INT frame);
  audit-raw-1017 .../merged-trunk-1017/c1.offline_ontas_stock.log ("O3 g1..g7 leaves port 2 as the model computes
  it, byte for byte", "stock: 12 verdict(s), 0 failed"). The package was pushed through the proxy's own P4Runtime
  client on one throwaway switch (offline_int_v1.py:14-20), NOT brought up with `ndt up p4 --app` on an NDTwin
  fabric. Verified LIVE (second run) on the lab VM's NDTwin network with `ndt up p4 --app`:
  A/B2_09_paper_int_v1/10_stdout.txt:108 ("PASS 09_paper_int_v1"; on the way: every package entry applied, 10/10
  INT-tagged frames from h1 and 10/10 untagged control frames from h3, the ping matrix as the app predicts, link
  usage follows the iperf path, :60-93); A/B2_10_paper_ontas/10_stdout.txt:93 ("PASS 10_paper_ontas"; 16 entries
  applied, 67/67 frames arrive as the model computes them, 0/67 the other way, link usage follows the iperf path,
  :56-79).
講者備註：
- 五個新功能，最右邊一欄是怎麼驗的：五個都在全新的實驗室 VM 上、用一般版 bmv2 實際跑過，只驗功能，沒有效能或時間數字。
- 第一、二列：開發者可以直接讀自己 P4 程式裡的 register，和某張表的 direct counter。這兩個 API 在 P4 proxy 上，不在 kernel 的 REST API 上。register 走 bmv2 的 Thrift 服務，因為 bmv2 的 P4Runtime 根本不支援讀 register；每次讀之前都確認交換機還活著、而且 Thrift 那一端回報的裝置編號和 port 跟這台交換機一樣。direct counter 走 P4Runtime，一次讀回整張表每一筆的計數。實驗室上比對的是讀到的數值本身：register 讀到的值和交換機自己的命令列工具讀到的一樣；ping 10 次，路徑上每一筆 direct counter 剛好多 10 個封包。
- 第三列：以前 P4 上只能寫單一主機位址，現在透過和 Ryu 相容的 flow API 可以寫 /24 這種網段，交換機上就是一筆 /24 的 LPM。
- 第四列：proxy 重啟或交換機重新接管時，pipeline 會重推，表會被清空。現在 app 可以從拓樸圖上逐台交換機看到，哪些經由 Ryu 路徑下的規則被清掉，再自己重送。下一頁講為什麼這樣設計。
- 第五列：轉換工具現在吃得下 2018–19 年教學版拓樸格式的 app，以及用 Thrift CLI 腳本下表的 app，因此兩篇論文的 app（int-v1、ONTAS）現在可以轉成 NDTwin 的套件，並且已經在實驗室 VM 的 NDTwin 網路上起起來、跑過一輪功能檢查，兩個都通過。CLI 腳本只翻譯 table_add 和 table_set_default，其他指令會被拒絕並指名，不會偷偷略過。

### P03 `Rules wiped by a push: report, not replay`   form: table
| Ryu-path rules, at a push | replay automatically | report; the app resends |
|---|---|---|
| proxy puts back | every Ryu-path request it journaled | none of them |
| a detour whose reason is gone | can come back | stays gone |
| the app must | nothing | read the notice, resend |
| until the app acts | rules back | rules missing |
| chosen | no | yes |

Sources:
- Scope: only the rules installed through the Ryu-compatible routes (/stats/flowentry/*). ndt_api.md:661-664
  ("are not put back"). The control plane's own routes are installed again by the push itself (api_routes.py:
  903-905: mastership, pipeline, clone session and routes; live: L/72_L3_F3ab/f_checks.log:11 "routes_installed":
  4); that is not part of this decision and is not on the page.
- W/doc/KNOWN-ISSUES.md:336-337 (A-4c: "不重放、改成大聲報給 kernel：journal 只記請求、不記理由，重放可能裝回過期的 TE
  繞路"); W/doc/2026-01-02_ndt_api.md:660-666 (rules installed through the Ryu-compatible routes "are not put
  back (KNOWN-ISSUES A-4c: the proxy's journal records requests, not the reasons behind them, so a replay could
  reinstall a detour whose reason is gone)"); :698 (`replayed` always false); A-4c :372 ("重啟後規則仍然不見");
  W/p4_proxy/proxy_agent/rule_journal.py:520-522 (the routing-request journal's replay "is off and has no caller,
  because a routing request is stale the moment the reason for it passes").
- "the app must read the notice, resend": ndt_api.md:666-668, A-4c :350-352 (apps poll get_graph_data, act once
  per id, resend their own rules). No shipped app does it yet: P08 row 5.
- Reconciliation with 10/14: the 10/14 roadmap's rank 4 fix listed "routing replay"
  (NDTwin-slide-template-1014.md:562); this decision replaces that part of it with the report.
講者備註：
- 這是這一輪最主要的設計取捨：pipeline 重推之後，app 經由 Ryu 相容路徑下、被清掉的規則，要不要自動裝回去。（控制面自己的路由，重推時本來就會重新裝回，不在這個問題裡。）
- 自動重放看起來比較方便，但 proxy 的紀錄只記得「當時收到什麼請求」，不記得「為什麼要裝」。例如流量工程 app 為了避開壅塞裝了一條繞路，壅塞早就沒了，自動重放就會把這條已經沒有理由的繞路裝回來。
- 所以我們選擇回報：proxy 說清楚哪些規則不見了，由真正知道理由的 app 決定要不要重送。
- 代價也要講清楚：app 沒有重送之前，這些規則就是不在交換機上，每個 app 都要自己去看這個通知。10/14 的路線圖原本打算把這類路由請求重放回去，這個決定取代了那一部分。

### P04 `How the rule-loss notice reaches the app`   form: figure `p4/fig_p04_rules_lost`
Figure spec: figures_spec/rules_lost_flow.txt (generator generator/make_p04_rules_lost.py). Four lanes (App,
NDTwin kernel, P4 proxy, bmv2 switch), six numbered steps left to right. Steps 5 (app reads and resends) and 6
(rules back) are dashed: no shipped app does step 5 yet, and step 6 happens only when an app resends. Two
annotations: "polled at 1 Hz", "resend". The generator stops if a step or arrow of the spec is missing or names
an unknown lane, or if the canvas title differs.
Sources: the evidence line under each step in rules_lost_flow.txt.
講者備註：
- 這張圖是通知怎麼一路傳到 app。觸發點有兩種：P4 proxy 重啟，或某台交換機重啟之後被重新接管；兩種都會重推 pipeline，表就全空了。
- proxy 推完 pipeline 之後，用推之前那台交換機的 pipeline cookie 對自己的紀錄，把經由 Ryu 路徑裝、這次被清掉的規則逐筆整理出來，掛在 switch_state 的 ryu_rules_lost。
- kernel 本來就每秒讀一次 switch_state，順便把這份紀錄原封不動複製到那台交換機在拓樸圖上的節點，同時在 log 記一行錯誤。
- app 端的設計是：看到新的紀錄（每筆有自己的 id，同一筆只處理一次）就重送自己的規則。但目前還沒有任何 app 接上這個通知，所以第 5 步和第 6 步都是虛線；規則要等 app 重送才會回來，系統不會自己裝。

### P05 `Reading registers and direct counters`   form: figure `p4/fig_p05_read_path`
Figure spec: figures_spec/read_path.txt (generator generator/make_p05_read_path.py). App on top; the P4 proxy's
REST API with two routes; two channels down to one bmv2 switch: P4Runtime for the direct counter, Thrift for the
register with its two checks before every read (switch answers P4Runtime; same device id and port). Key
annotations: each check's refusal ("503" / "502", "nothing read"); "no register reads on bmv2" under the P4Runtime
channel label, "bmv2 only" beside the Thrift label (read_path.txt:20, :23). The generator stops if an element of
the spec is missing, an arrow differs, a label does not fit its box, or the canvas title differs.
Sources: the evidence line under each element in read_path.txt.
講者備註：
- 兩個讀取都在 P4 proxy 的 API 上，app 直接呼叫。
- direct counter 走 P4Runtime：一次讀整張表，每一筆帶自己的 match 和 bytes、packets。讀失敗回 503，明確說「這不是 0、也不是空表」。
- register 為什麼繞到 Thrift：bmv2 的 P4Runtime 對任何 register 讀取都回「尚未支援」，所以只能走 bmv2 自己的 Thrift 服務。風險是 Thrift 那個 port 上回答的可能不是我們以為的那台交換機，所以每一次讀之前做兩個檢查：先確認這台交換機回應 P4Runtime，再在同一條 Thrift 連線上確認回報的裝置編號和 port 跟這台交換機一樣；任何一個不過就回錯誤，不讀任何東西。
- 限制也講：只支援 bmv2，硬體目標沒有這個服務；register 最寬到 63 bit；一台裝置編號和 port 都一樣的冒牌交換機，在原交換機還活著時佔住那個 port，這兩個檢查擋不住。

### P06 `Verified live on a fresh lab VM`   form: table
| check | result | verified |
|---|---|---|
| /24 destination, Ryu route | read back as one /24 entry | live, lab VM |
| /25 via the kernel's flow API | 200, accepted by the switch, entries 5 -> 6 | live, lab VM |
| switch restart + re-adopt | 2 rules listed; same record on kernel graph; rules gone | live, lab VM |
| re-adopt: other 9 switches | records unchanged | live, lab VM |
| proxy restart | 2 rules listed; same record on kernel graph; rules gone | live, lab VM |

Sources (all RAN live on the lab VM; identity in the header):
- Row 1: L/71_L3_rerun/f_checks.log:16-18 (F2.1 10.0.0.0/24 through the proxy's /stats/flowentry/add, 200 on
  ipv4_lpm; F2.2 read back ['10.0.0.0/24']; F2.2c control: the bare host entry reads back as /32).
- Row 2: f_checks.log:22 (F2.6: 10.0.0.0/25 in both ipv4_dst and nw_dst through the kernel's install_flow_entry:
  200, accepted_by_switch 1, entries 5 -> 6). The "5" is the count after the F2.3/F2.4 checks (:19-21), which are
  not on the page (they read as hardening, review decision).
- Row 3: L/72_L3_F3ab/f_checks.log:4-15 (F3a: switch 2's process stopped and relaunched by p4_power_helper
  (:9-10), POST /p4/readopt/2 200 (:11), count 2 with both rules, cause readopt, replayed false (:12), id =
  table_generation and new (:13), the kernel's get_graph_data node carries the identical object (:14), rules no
  longer on the switch (:15)).
- Row 4: L/72_L3_F3ab/f_checks.log:16 (F3a.6: "no other switch's record moved", 9 other switches compared;
  L/72_L3_F3ab/f3ab.py:113, :136-138: the comparison is made around the re-adopt only).
- Row 5: L/72_L3_F3ab/f_checks.log:17-28 (F3b: proxy stopped the way stack.sh does and brought back (:23-24),
  count 2, cause proxy_restart, replayed false (:25), new id (:26), kernel node carries the identical object (:27),
  rules gone (:28)). The proxy-restart path has only the before-the-push control F3b.0 (:18).
- No timing on the page: f3ab.py:72-82 starts its clock after switch_state was already read and polls every
  0.5 s, so the "after N s" in the log is not a latency, and the run is labelled no-performance-numbers.
- Offline packet test mentioned in the notes (not on the page): KNOWN-ISSUES.md:1287-1294 (B-2c: /32 > /24 > /16
  forwarding on throwaway simple_switch_grpc, stock and fast, 11/11 each, through the proxy's own route_flow).
- Not on the page: F1 (write replies, a fix, §0 rule 5); F2.3-F2.5 (400s, review decision); the before-the-push
  controls F3a.0 / F3b.0 (count 0, :4, :18). L3 ran three times (L/progress.log): the first attempt's release
  failed, the second (run 71) stopped at F3.3 (L/71_L3_rerun/f_checks.log:32), which is P07 row 3, the third
  (run 72) passed.
講者備註：
- 這一頁全部是在一台全新的實驗室 VM 上、用一般版 bmv2 實際跑出來的，只驗功能，不是效能數字。網路是 10 台交換機、4 台主機。這些結果是在 VM 裡先繞過下一頁的兩個問題之後才跑得出來的。
- 前兩列是 CIDR：一筆 /24 寫進去，從交換機讀回來就是一筆 /24；對照組是控制面原本那筆單一主機的路由讀回來是 /32，所以讀得出兩者的差別。經由 kernel 的 flow API 下一筆 /25，交換機也接受了，條目多一筆。
- 後三列是規則遺失通知，兩種觸發都測了：交換機行程真的重啟再重新接管，和 proxy 重啟。兩種都正確列出剛剛裝的 2 條規則，kernel 拓樸圖上的那份和 proxy 的一模一樣，交換機上那 2 條也確實不見了。其他 9 台交換機的紀錄都沒有動（這是重新接管那一段的對照）。
- 要說明一句：這裡驗的是「規則寫得進去、讀得回來、通知是對的」，沒有送封包看 /24 實際怎麼轉；送封包的部分是在臨時 bmv2 上離線做過。

### P07 `What a fresh machine exposed`   form: table
| problem | effect (live, lab VM) | next step |
|---|---|---|
| traffic generator looked for in one fixed home directory | ndt up p4: 0/10 switches, no fabric | fix, with tests |
| first P4 bring-up creates the log directory as root | proxy cannot write its log; bring-up fails | fix, with tests |
| re-adopt of a switch that did not restart | 502 at mastership; reply: switch not touched | API doc: needs a restarted switch |

Sources (each problem observed on the lab VM; the code line that explains it is READ):
- The VM was set up with a custom recipe (L/40_build.log ... L/46_symlink.log, L/scripts), not by following the
  User Manual step by step.
- Row 1, observed: L/45_step4/02_up.txt (fabric did not come up: 0/10 switches, manifest missing; topo.log:
  "NTG repo not found at /home/adam/Network-Traffic-Generator (override with the NTG_DIR env var)"), L/45_step4/
  02_up.rc (ndt up rc=1). Seen for one user (ndt); "any other user" follows from the hard-coded path (INFERRED).
  READ: W/p4_proxy/mininet/ntg_bmv2_topo.py:60 (NTG_DIR defaults to /home/adam/Network-Traffic-Generator),
  :127-128; W/tools/test_workflow/ndtwin-lab:233-234 (config keys are KERNEL_DIR, NTG_PY, ENERGY_DIR, SIM_DIR
  only), :1665-1666 (topo-start runs the bridge as root with no NTG_DIR). Worked around on the VM with a
  /home/adam symlink (L/46_symlink.log). Reconciliation: first live sighting of the 10/14 rank-1 class "own .p4
  only via a lab CLI tied to one machine" (NDTwin-slide-template-1014.md:559), which then rested on READ only.
- Row 2, observed: L/51_disc/00_stat_before.txt (.test_run/logs owner root:root while .test_run is ndt:ndt),
  01_rm.txt and 03_stat_after_L1.txt (after removing it, the next bring-up recreated it root:root, born with
  topo.log), 04_permission_denied.txt (stack.sh line 588: .test_run/logs/p4_proxy.log: Permission denied);
  L/50_L1_01_baseline/10_stdout.txt (FAIL, 'ndt up p4 4' exited 1). READ: W/p4_proxy/mininet/topo_log.py:59,
  :173 (the bridge, run as root, makes .test_run/logs for topo.log); W/tools/test_workflow/stack.sh:588 (proxy
  log written as the user). Worked around with a chown (L/52_chown); L/progress.log shows 53_L1_rerun PASS after.
- Row 3, observed: L/71_L3_rerun/f_checks.log:32 and L/71_L3_rerun/32_f3_readopt.json (502, step mastership,
  "arbitration was not granted within the settle window ... The switch was not touched."), on a switch whose
  process had not been restarted; L/72_L3_F3ab/f_checks.log:9-11 (after a process restart the same readopt is
  200). "switch not touched" is the reply's own claim, not checked separately. READ: api_routes.py:897-900
  (readopt docstring: "one restarted bmv2 switch"); ndt_api.md:660-661 says readopt pushes the pipeline and does
  not state the precondition (no readopt section in ndt_api.md).
- "fix, with tests" and "API doc" are Adam's stated next steps (task brief, 2026-10-26).
講者備註：
- 在一台全新的機器上把 NDTwin 裝起來，碰到三個問題。這三個都還沒修，所以不算在新功能裡，照實列出來。
- 第一個：P4 拓樸啟動時，固定到某一個使用者的家目錄去找流量產生器；實驗室小幫手的設定檔也沒有可以改這個路徑的欄位。VM 上的使用者是另一個名字，ndt up p4 就起不了網路，10 台交換機一台都沒有；這是在一個使用者身上看到的，換成其他使用者也會一樣，是從寫死的路徑推出來的。VM 上是先用一個符號連結繞過去。10/14 列為第一名的「綁在一台機器上」那一類問題，這是第一次在實機上看到。
- 第二個：全新的 checkout 第一次啟動 P4 時，log 目錄由以 root 執行的拓樸程式建立，P4 proxy 以一般使用者寫不進自己的 log，整個啟動失敗；VM 上把目錄改回使用者擁有後才繼續。
- 這兩個都在修，會附測試。第三個是文件問題：重新接管一台交換機，前提是那台的行程真的重啟過；對一台還在跑的交換機下這個指令，會被拒絕，回覆說交換機沒有被動到。API 文件沒有寫這個前提，要補上。

### P08 `Limits of the new features`   form: table
| limit | effect | next step |
|---|---|---|
| register and counter routes | not in the API doc; limits (≤ 63 bit, same-id impostor) unstated | add them, with limits, to the API doc |
| /24 on P4: longest prefix wins | a host's own /32 on that switch still wins | say so in the API doc |
| prefix forms queued, then refused on P4 | failure shows only in dispatch status | decide: kernel pre-check refuses these forms |
| bmv2, then proxy restarted; kernel running | loss record says 0 | decide: flag it at proxy start |
| rule-loss notice | no app resends on it yet | an app that resends on it |

Sources (READ):
- Row 1: `grep -rn "p4/register\|p4/direct_counter" --include=*.md W` outside doc/audit is empty; the routes are
  documented only in their docstrings (api_routes.py:1494-1540, :1608-1680). Limits: api_routes.py:1621-1625
  (bit<W> with W at most 63), :1632-1638 (a bmv2 with the same device id and port number holding the port while
  the dpid's own switch answers P4Runtime is NOT caught). Next step proposed here (§3 item 3).
- Row 2: KNOWN-ISSUES B-2c :1297-1303 (on P4 only the prefix length decides; on an ordinary fabric every switch
  holds a /32 for every host, so a /24 does not take effect for those hosts; on a routes_to_attached_hosts_only
  fabric it does on transit switches); ndt_api.md:1953 says "the longest prefix wins" but not the /32 consequence.
  Next step proposed here (§3 item 3).
- Row 3: ndt_api.md:1952-1966 (/0, the dotted mask, an address as a number, a prefix on a source, a prefix with
  a source, protocol or port: 200 queued by the kernel, refused by the proxy afterwards, visible only in
  get_flow_dispatch_status); B-2c :1305-1311. Next step proposed here (§3 item 3).
- Row 4: ndt_api.md:703-706 (a switch whose bmv2 process was restarted before the proxy reports count 0 at proxy
  start; right only when the kernel and apps restarted too: if they keep running, their rules are gone and the
  record still says 0); KNOWN-ISSUES.md:370-371. This is not P06 row 5 (there bmv2 was not restarted). Also
  there, not on the page: the proxy holds the latest record per switch in memory only, so a second restart before
  the kernel reads it loses it (ndt_api.md:706-709, A-4c :368). Next step proposed here (§3 item 3).
- Row 5: `git grep -l ryu_rules_lost HEAD` is empty in Traffic-Engineering-App f108c7cf, Energy-Saving-App
  9facb780, Web-GUI f63a55ce, Network-State-Recorder 850f61da, Network-Traffic-Visualizer 9b56b30b,
  Simulation-Platform-Manager b7efd939 and Network-Traffic-Generator 6e3f3881 (read 2026-10-27, /home/adam/<repo>);
  A-4c :367 (live verification with a real TE app not done). Next step proposed here (§3 item 3).
講者備註：
- 這一頁是新功能本身的弱點，不是 bug 清單。
- 第一列：這兩個讀取 API 目前只寫在程式碼的說明裡，使用者文件還沒有；它的限制也還沒寫出來：register 最寬 63 bit，以及裝置編號和 port 都一樣的冒牌交換機擋不住。要連同限制一起補進文件。
- 第二列最容易誤會：P4 上比的是前綴長度，不是 OVS 那種 priority。一般的網路裡每台交換機對每台主機都有一筆 /32，所以下一筆 /24 想改某台主機的走法，在那台交換機上不會生效，只對沒有 /32 的位址有用。這點文件還沒講清楚，要補。
- 第三列：有幾種網段寫法 kernel 會先回 200 排進佇列，到 P4 proxy 才拒絕，失敗只看得到在派送狀態裡；要決定是不是讓 kernel 事先就擋掉。第四列：如果 bmv2 先重啟、接著 proxy 也重啟，而 kernel 和 app 一直在跑，那份遺失紀錄會說 0，但規則其實已經不見了；要決定是不是在 proxy 啟動時把這種情況標出來。另外，這份紀錄只存在 proxy 的記憶體裡，proxy 在 kernel 讀到之前又重啟一次，那份就看不到了。
- 第五列：通知已經做好，但目前還沒有任何 app 接上去、收到通知就重送；需要一個真的這樣做的 app。

### P09 `What comes next`   form: figure `next/fig_p09_next`
Figure spec: figures_spec/next.txt (generator generator/make_p09_next.py). Two columns, NOW and NEXT, five lanes
(fresh machine, API doc, decide, apps); one box per step, no dates. Column rule: NOW = being fixed now,
or a document change; NEXT = needs a design decision or app work. The generator stops if ANY P07 or P08
next step is not drawn, a box sits in a lane the spec does not list, or the canvas title differs.
Sources: next.txt (each box names the P07 / P08 row it comes from).
講者備註：
- 接下來先補的：新機器上那兩個問題，修好並附測試；文件補三件事：重新接管的前提、兩個讀取 API 和它們的限制、以及 P4 上 /24 和主機 /32 的關係。
- 再來：決定兩件事，kernel 要不要事先擋掉 P4 會拒絕的網段寫法、proxy 啟動時要不要標出那種「說 0 但其實不見」的情況；做一個真的會依遺失通知重送規則的 app。
- 圖上不寫日期，順序就是這兩欄。

## 3. Open items for the orchestrator (not slide content)

1. Page added: P08 "Limits of the new features" (kept, review decision). Adam's page order had no slot for the
   weaknesses of the new features themselves (rule 9); P07 is about the fresh machine only.
2. Wording that differs from the brief, following the sources:
   - Row (a)/(b) "through NDTwin's API": the two routes are on the P4 proxy's REST API (:8081), not on the
     kernel's (:8000). The slide says only the route; the notes say "P4 proxy".
   - The brief says ndt_api.md has sections on /p4/register and /p4/direct_counter: it has none (no user doc
     outside doc/audit mentions either route). Hence P08 row 1.
   - Row (c)'s "malformed or conflicting address fields get 400": removed from P06 and from the notes (review
     decision: it reads as hardening; it is the same "malformed flow entry" shape check that refuses bad
     priorities, ndt_api.md:1981). P06 shows the kernel path with the /25 row instead.
   - P06 "other switches' records unchanged": ran on the re-adopt path only (F3a.6); the row now says so.
   - P07 row 1 "any other user": observed for user ndt only; follows from the hard-coded path (INFERRED), said so
     in the notes and the script.
   - Register, direct counter and paper apps: first verified offline only; the second lab run (header, "Live
     evidence, second run") ran all three live, so P02 now says "live, lab VM" for every row, P08's old row 1
     ("not yet run on a live lab") and P09's two live-lab boxes are gone.
   - P03 is scoped to the Ryu-path rules; the control plane's own routes go back with the push (sources), and the
     separate table-entry mechanism is not shown (§0 rule 5).
3. Next steps that are proposals, not Adam's decisions: "add them, with limits, to the API doc" (P08 row 1),
   "say so in the API doc" (row 2), "decide: kernel pre-check refuses these forms" (row 3), "decide: flag it at
   proxy start" (row 4) and "an app that resends on it" (row 5). All five are drawn on P09.
4. Dropped by review decision: the P09 "optimised-build job" box (CI process, rule 6/7); P06's 400 rows; every
   timing on P06.
5. No render: there is no LibreOffice on the laptop, so the pptx was not rendered; layout is checked by
   generator/verify_deck_1028.py's geometry estimate only.
