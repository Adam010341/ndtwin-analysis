#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fig_t1_requirements_matrix — 13 支 p4lang/tutorials exercise 的能力需求 vs. NDTwin 今天的供給。

資料**全部**解析自三份既有 .md，腳本裡沒有任何手抄的格值：
  GAP-1-exercise-requirements.md  §2a/§2b/§2c（需求矩陣）＋§4a/§4b（跨支彙整，當作對帳斷言）
  GAP-2-ndtwin-p4-capabilities.md §1（能力矩陣）＋「計數」那一行（當作對帳斷言）
  GAP-ANALYSIS.md                 §4（逐支可行性，決定列序）＋§6（三階段，交叉驗證列序）

解析失敗一律 raise SystemExit —— 不猜、不填預設值。

重跑：
  "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
      make_tutorial_figs.py

[Co-developed with claude code -- Adam]
"""

from __future__ import annotations

import datetime as _dt
import os
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ----------------------------------------------------------------------------
# 0. 路徑與常數
# ----------------------------------------------------------------------------

SRC_DIR = Path("/home/adam/Desktop/NDTwin-Kernel/doc/audit/2026-09-04_p4-tutorial-exercise-prep")
GAP1 = SRC_DIR / "GAP-1-exercise-requirements.md"
GAP2 = SRC_DIR / "GAP-2-ndtwin-p4-capabilities.md"
GAPA = SRC_DIR / "GAP-ANALYSIS.md"

OUT_DIR = Path(__file__).resolve().parent
HIRES_DIR = OUT_DIR / "_hires"
STEM = "fig_t1_requirements_matrix"

# 16 個維度鍵，順序＝ GAP-1 §1 的定義表順序（本腳本會斷言它與解析到的集合相同）。
DIMS = [
    "pipeline_load", "tables", "pre_multicast", "pre_clone",
    "counters", "meters", "registers", "digest",
    "packet_io", "custom_headers", "queue_metadata", "checksum",
    "ttl_or_hop", "topology", "control_plane_mode", "verification",
]

EXERCISES = [
    "basic", "basic_tunnel", "calc", "ecn", "firewall", "flowcache",
    "link_monitor", "load_balance", "mri", "multicast", "p4runtime",
    "qos", "source_routing",
]

# GAP-1 §2 的三個子表裡出現、但不屬於這 16 維的鍵（記錄下來，寫進 .md）。
KNOWN_EXTRA_KEYS = {"idle_timeout"}

# ---- 需求側三色階 / 供給側三色階 -------------------------------------------
REQ_CRITICAL, REQ_USED, REQ_NONE = "critical", "used", "none"
CAP_YES, CAP_PARTIAL, CAP_NO = "yes", "partial", "no"

CAP_ZH2KEY = {"做得到": CAP_YES, "部分": CAP_PARTIAL, "做不到": CAP_NO}

# 色票：藍色系取自 NDTwin-slide-template-827.md §E2（ACCENT / ACCENT_BG）。
INK, MUTED, FAINT, RULE = "#1A1A1A", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG = "#065A82", "#EEF3F6"

FILL = {
    REQ_CRITICAL: ACCENT,      # E2 ACCENT
    REQ_USED:     "#8FB5C7",   # ACCENT 混 55% 白
    REQ_NONE:     ACCENT_BG,   # E2 ACCENT_BG
    CAP_YES:      "#2F7D4F",
    CAP_PARTIAL:  "#E3A21A",
    CAP_NO:       "#C9CDD0",
}
EDGE = {
    REQ_CRITICAL: ACCENT,
    REQ_USED:     "#8FB5C7",
    REQ_NONE:     "#D3DFE7",
    CAP_YES:      "#2F7D4F",
    CAP_PARTIAL:  "#E3A21A",
    CAP_NO:       "#B4B9BD",
}
LEGEND_LABEL = {
    REQ_CRITICAL: "critical",
    REQ_USED:     "used",
    REQ_NONE:     "not used",
    CAP_YES:      "can do",
    CAP_PARTIAL:  "partial",
    CAP_NO:       "cannot",
}
ZH_LABEL = {
    REQ_CRITICAL: "關鍵", REQ_USED: "用到", REQ_NONE: "沒用到",
    CAP_YES: "做得到", CAP_PARTIAL: "部分", CAP_NO: "做不到",
}

TITLE = "What 13 P4 exercises need vs. NDTwin today"   # 42 chars

# ----------------------------------------------------------------------------
# 1. 小工具
# ----------------------------------------------------------------------------


def die(msg: str) -> "None":
    raise SystemExit("[make_tutorial_figs] PARSE FAILED: " + msg)


def read(p: Path) -> str:
    if not p.is_file():
        die(f"找不到來源檔 {p}")
    return p.read_text(encoding="utf-8")


_PIPE = re.compile(r"(?<!\\)\|")


def split_row(line: str) -> list[str]:
    """把一列 markdown 表格切成 cell；`\\|`（跳脫的管線）不切。"""
    parts = _PIPE.split(line.strip())
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return [c.strip() for c in parts]


_SEP = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?$")


def find_tables(text: str) -> list[dict]:
    """回傳 [{'heading':…, 'header':[…], 'rows':[[…],…]}]，heading＝最近的上一個標題行。"""
    lines = text.splitlines()
    tables, heading, i = [], "", 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("#"):
            heading = ln.strip()
        if ln.lstrip().startswith("|") and i + 1 < len(lines) and _SEP.match(lines[i + 1].strip()):
            header = split_row(ln)
            rows, j = [], i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append(split_row(lines[j]))
                j += 1
            tables.append({"heading": heading, "header": header, "rows": rows, "line": i + 1})
            i = j
            continue
        i += 1
    return tables


_TICK = re.compile(r"`([^`]+)`")


def ticked_keys(cell: str) -> list[str]:
    """cell 裡所有反引號 token 中屬於 DIMS 的那些（保持出現順序、去重）。"""
    out = []
    for t in _TICK.findall(cell):
        t = t.strip()
        if t in DIMS and t not in out:
            out.append(t)
    return out


def plain(cell: str) -> str:
    """去 markdown 強調與跳脫，只為了做「是不是缺席寫法」的判斷；輸出仍用原文。"""
    s = cell.replace("\\|", "|").replace("**", "").replace("`", "").strip()
    return s


def unescape(cell: str) -> str:
    return cell.replace("\\|", "|")


# ----------------------------------------------------------------------------
# 2. 格值 → 三色階
# ----------------------------------------------------------------------------

DASHES = {"—", "–", "-", "－", ""}

# 「不是那三種寫法」的偵測器。命中且不在 REVIEWED 裡 ⇒ fail loudly。
_SUSPECT = [
    re.compile(r"^(無|沒有|沒用到|不需要|空|N/A)"),      # 以缺席詞開頭
    re.compile(r"都沒有$"),                              # 以「…都沒有」結尾
    re.compile(r"（空）"),                                # 括號裡註明是空的
    re.compile(r"[?？]"),                                # 帶問號
    re.compile(r"^部分"),                                # 「部分」
]

# 逐格審過的例外：(exercise, dim) -> (原文, 判給哪一階, 為什麼)
# 依據一律引既有文件，不自行推測。
REVIEWED: dict[tuple[str, str], tuple[str, str, str]] = {
    ("source_routing", "tables"): (
        "**一條 entry 都沒有**", REQ_NONE,
        "GAP-1 §4a「`tables` 12/13 —— 只有 source_routing 一條 entry 都沒有」＋"
        "GAP-ANALYSIS §4「G5 不需要：**0 筆 entry**」⇒ 歸「沒用到」。"
        "本腳本另以 §4a 的 12/13 做斷言，歸錯會當場爆。"),
    ("calc", "control_plane_mode"): (
        "**無**（entry 在 P4 裡）", REQ_NONE,
        "GAP-1 §1 把 control_plane_mode 定義成三選一，第③種就是「兩者皆無」；"
        "§3.3「`control_plane_mode`＝**無**」⇒ 歸「沒用到」。"),
    ("source_routing", "control_plane_mode"): (
        "開機 runtime json（**空**）", REQ_USED,
        "模式仍是①「開機灌 runtime json」，只是 entry 陣列是空的（GAP-1 §3.13）"
        "⇒ 模式有用到，歸「用到」；「空」講的是筆數不是模式。"),
}


def classify_req(exercise: str, dim: str, cell: str) -> tuple[str, str]:
    """回傳 (色階, 判定理由)。"""
    raw = unescape(cell)
    key = (exercise, dim)
    if key in REVIEWED:
        expect, cls, why = REVIEWED[key]
        if raw.strip() != expect:
            die(f"§2 的 {exercise}/{dim} 原文變了：文件是 {raw!r}，例外表登記的是 {expect!r}。"
                f"請重新判斷後更新 REVIEWED。")
        return cls, "【逐格審過的例外】" + why
    s = plain(raw)
    if s in DASHES:
        return REQ_NONE, "格值是破折號 —— 直接歸「沒用到」。"
    if re.match(r"^關鍵", s):
        return REQ_CRITICAL, "格值以「關鍵」開頭（`**關鍵**` 標記）⇒ 歸「關鍵」。"
    for pat in _SUSPECT:
        if pat.search(s):
            die(f"§2 的 {exercise}/{dim} 格值 {raw!r} 不是「用到／沒用到／關鍵」三種寫法之一，"
                f"且不在 REVIEWED 例外表裡。請人工判定後登記，不要讓腳本猜。")
    return REQ_USED, "格值是非空的具體敘述、無「關鍵」標記 ⇒ 歸「用到」。"


# ----------------------------------------------------------------------------
# 3. 解析 GAP-1
# ----------------------------------------------------------------------------


def parse_gap1(text: str):
    tables = find_tables(text)
    req: dict[str, dict[str, str]] = {e: {} for e in EXERCISES}
    raws: dict[tuple[str, str], str] = {}
    why: dict[tuple[str, str], str] = {}
    seen_dims: list[str] = []
    skipped_cols: list[str] = []

    sub = [t for t in tables if t["heading"].startswith("### 2") and t["header"][:1] == ["exercise"]]
    if len(sub) != 3:
        die(f"GAP-1 §2 應該有 3 個以 `exercise` 開頭的子表，找到 {len(sub)} 個。")

    for t in sub:
        colmap: dict[int, str] = {}
        for idx, h in enumerate(t["header"][1:], start=1):
            keys = ticked_keys(h)
            if len(keys) == 1:
                colmap[idx] = keys[0]
            else:
                extra = [k.strip() for k in _TICK.findall(h)]
                head = t["heading"].lstrip("# ").strip()
                skipped_cols.append(f"GAP-1 §{head} 第 {idx+1} 欄「{h}」（未對到 16 維中的任何一個鍵）")
                if any(k in KNOWN_EXTRA_KEYS for k in extra):
                    pass
        if not colmap:
            die(f"{t['heading']} 一個維度欄都沒對到。")
        for d in colmap.values():
            if d in seen_dims:
                die(f"維度 {d} 在 §2 出現不只一次。")
            seen_dims.append(d)
        for row in t["rows"]:
            if len(row) != len(t["header"]):
                die(f"{t['heading']} 的一列欄數 {len(row)} != 表頭 {len(t['header'])}：{row[:2]}")
            ex = plain(row[0])
            if ex not in EXERCISES:
                die(f"{t['heading']} 出現未知 exercise 名稱 {ex!r}。")
            for idx, dim in colmap.items():
                cls, reason = classify_req(ex, dim, row[idx])
                req[ex][dim] = cls
                raws[(ex, dim)] = unescape(row[idx]).strip()
                why[(ex, dim)] = reason

    # --- §4b：meters／digest 兩維在 §2 沒有欄位，要從「幾支要」的彙整表補 ---
    t4b = [t for t in tables if t["heading"].startswith("### 4b")]
    if len(t4b) != 1:
        die(f"GAP-1 §4b 找到 {len(t4b)} 個表，預期 1 個。")
    counts_4b: dict[str, int] = {}
    for row in t4b[0]["rows"]:
        keys = ticked_keys(row[0])
        nums = re.findall(r"(\d+)\s*支", row[1])
        if not keys or len(nums) != 1:
            continue
        for k in keys:
            counts_4b[k] = int(nums[0])
    for d in ("meters", "digest"):
        if counts_4b.get(d) is None:
            die(f"GAP-1 §4b 沒解析到 `{d}` 的支數。")
        if counts_4b[d] != 0:
            die(f"GAP-1 §4b 說 `{d}` 有 {counts_4b[d]} 支要用，但 §2 沒有這一欄 —— 兩邊對不上，停。")
        for ex in EXERCISES:
            req[ex][d] = REQ_NONE
            raws[(ex, d)] = "（§2 無此欄）"
            why[(ex, d)] = ("§2 三個子表都沒有這一欄；GAP-1 §4b 明列 `meters`／`digest` ＝ **0 支**"
                            "（「這批 exercise 完全不需要」）⇒ 13 支全歸「沒用到」。"
                            "GAP-ANALYSIS §2 判定欄同樣寫「無需求，不是 gap」。")
        seen_dims.append(d)

    if sorted(seen_dims) != sorted(DIMS):
        die(f"解析到的維度集合與 16 維不符。多/少的是："
            f"{sorted(set(seen_dims) ^ set(DIMS))}")

    # --- §4a / §4b 對帳斷言 ---
    t4a = [t for t in tables if t["heading"].startswith("### 4a")]
    if len(t4a) != 1:
        die("GAP-1 §4a 表找不到（或不只一個）。")
    checks: list[str] = []
    for row in t4a[0]["rows"]:
        keys = ticked_keys(row[0])
        m = re.search(r"(\d+)\s*/\s*13", row[1])
        if len(keys) != 1 or not m:
            continue
        d, want = keys[0], int(m.group(1))
        got = sum(1 for e in EXERCISES if req[e][d] != REQ_NONE)
        if got != want:
            die(f"§4a 說 `{d}` 是 {want}/13，但 §2 解析出 {got} 支非「沒用到」。歸類有錯。")
        checks.append(f"§4a `{d}` = {want}/13 ✓")
    for d, want in sorted(counts_4b.items()):
        got = sum(1 for e in EXERCISES if req[e][d] != REQ_NONE)
        if got != want:
            die(f"§4b 說 `{d}` 有 {want} 支要，但 §2 解析出 {got} 支非「沒用到」。")
        checks.append(f"§4b `{d}` = {want} 支 ✓")
    if len(checks) < 10:
        die(f"對帳斷言只跑到 {len(checks)} 條，太少 —— §4a/§4b 的表可能沒解析到。")

    return req, raws, why, checks, skipped_cols


# ----------------------------------------------------------------------------
# 4. 解析 GAP-2
# ----------------------------------------------------------------------------


def parse_gap2(text: str):
    tables = [t for t in find_tables(text) if t["heading"].startswith("## 1.")]
    cand = [t for t in tables if t["header"][:2] == ["維度", "今天"]]
    if len(cand) != 1:
        die(f"GAP-2 §1 能力矩陣表找到 {len(cand)} 個，預期 1 個。")
    cap: dict[str, str] = {}
    raws: dict[str, str] = {}
    for row in cand[0]["rows"]:
        keys = ticked_keys(row[0])
        if len(keys) != 1:
            die(f"GAP-2 §1 的一列第一欄 {row[0]!r} 對不到唯一的維度鍵。")
        v = plain(row[1])
        if v not in CAP_ZH2KEY:
            die(f"GAP-2 §1 的 `{keys[0]}` 今天欄是 {v!r}，不是 做得到／部分／做不到。")
        cap[keys[0]] = CAP_ZH2KEY[v]
        raws[keys[0]] = v
    if sorted(cap) != sorted(DIMS):
        die(f"GAP-2 §1 的維度集合與 16 維不符：{sorted(set(cap) ^ set(DIMS))}")

    m = re.search(r"計數：做得到\s*(\d+)、部分\s*(\d+)、做不到\s*(\d+)", text)
    if not m:
        die("GAP-2 找不到「計數：做得到 N、部分 N、做不到 N」那一行，無法對帳。")
    want = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    got = tuple(sum(1 for d in DIMS if cap[d] == k) for k in (CAP_YES, CAP_PARTIAL, CAP_NO))
    if want != got:
        die(f"GAP-2 自報計數 {want}，解析結果 {got} —— 對不上。")
    return cap, raws, f"GAP-2 計數 做得到{want[0]}／部分{want[1]}／做不到{want[2]} ✓"


# ----------------------------------------------------------------------------
# 5. 解析列序（GAP-ANALYSIS §4 定序、§6 交叉驗證）
# ----------------------------------------------------------------------------


def parse_row_order(text: str):
    tables = find_tables(text)

    t4 = [t for t in tables if t["heading"].startswith("## 4.") and t["header"][:1] == ["exercise"]]
    if len(t4) != 1:
        die(f"GAP-ANALYSIS §4 逐支可行性表找到 {len(t4)} 個，預期 1 個。")
    order = [plain(r[0]) for r in t4[0]["rows"]]
    if sorted(order) != sorted(EXERCISES):
        die(f"§4 的 13 支名單與預期不符：{sorted(set(order) ^ set(EXERCISES))}")
    if len(order) != 13:
        die(f"§4 解析到 {len(order)} 列，預期 13。")

    t6 = [t for t in tables if t["heading"].startswith("## 6.") and t["header"][:1] == ["階段"]]
    if len(t6) != 1:
        die(f"GAP-ANALYSIS §6 三階段表找到 {len(t6)} 個，預期 1 個。")
    rows6 = t6[0]["rows"]
    if len(rows6) != 3:
        die(f"§6 有 {len(rows6)} 個階段，預期 3。")

    def names_in(cell: str) -> list[str]:
        found = []
        for tok in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", cell):
            if tok in EXERCISES and tok not in found:
                found.append(tok)
        return found

    # 階段一：解鎖「1 支真跑通」，該支＝驗證欄第一個 exercise 名。
    s1_unlock, s1_verify = rows6[0][3], rows6[0][4]
    if not re.search(r"1\s*支真跑通", s1_unlock):
        die(f"§6 第一階段的解鎖欄 {s1_unlock!r} 不是預期的「1 支真跑通」寫法。")
    s1 = names_in(s1_verify)[:1]
    if len(s1) != 1:
        die(f"§6 第一階段驗證欄 {s1_verify!r} 解不出唯一的 exercise。")

    # 階段二：解鎖欄自己寫了 +N 支與名單。
    s2_unlock = rows6[1][3]
    m = re.search(r"\+\s*(\d+)\s*支", s2_unlock)
    if not m:
        die(f"§6 第二階段解鎖欄 {s2_unlock!r} 沒有「+N 支」。")
    s2 = names_in(s2_unlock)
    if len(s2) != int(m.group(1)):
        die(f"§6 第二階段說 +{m.group(1)} 支，名單卻有 {len(s2)} 支：{s2}")

    # 階段三：其餘的（解鎖欄只點名 multicast/flowcache，p4runtime 是餘數）。
    s3 = [e for e in order if e not in s1 and e not in s2]
    s3_unlock = rows6[2][3]
    named3 = [e for e in names_in(s3_unlock) if e in s3]
    if not set(named3) <= set(s3):
        die("§6 第三階段點名的 exercise 不在餘數集合裡。")
    if sorted(s1 + s2 + s3) != sorted(EXERCISES):
        die("三階段拼起來不是 13 支。")

    # §4 的列序必須與「階段一 → 階段二名單順序 → 餘數」一致，不一致就停。
    expected = s1 + s2 + s3
    if order[:1] != s1:
        die(f"§4 第一列是 {order[0]}，§6 第一階段是 {s1[0]}。列序來源互相矛盾。")
    if order[1:1 + len(s2)] != s2:
        die(f"§4 第 2..{1+len(s2)} 列 {order[1:1+len(s2)]} 與 §6 第二階段名單 {s2} 不同序。")
    if order[1 + len(s2):] != s3:
        die(f"§4 尾段 {order[1+len(s2):]} 與餘數 {s3} 不同。")
    if expected != order:
        die("§4 與 §6 推出的列序不一致。")

    stage_of = {e: 1 for e in s1}
    stage_of.update({e: 2 for e in s2})
    stage_of.update({e: 3 for e in s3})
    note = (f"階段一＝{s1}（§6 解鎖欄「1 支真跑通」＋驗證欄點名）；"
            f"階段二＝{s2}（§6 解鎖欄 +{len(s2)} 支的名單，逐字照抄順序）；"
            f"階段三＝{s3}（餘數；§6 第三階段解鎖欄點名了 {named3}，"
            f"p4runtime 是餘數推得、§4 表也把它排在該位置）。")
    return order, stage_of, note


# ----------------------------------------------------------------------------
# 6. 畫圖
# ----------------------------------------------------------------------------

GAP_STAGE = 0.30      # 階段之間多留的列高
GAP_NDT = 0.75        # 13 支與 NDTwin today 之間的列高
CELL_W, CELL_H = 0.90, 0.84


def row_y(order, stage_of):
    """回傳 {exercise: y}（往下遞增）與 NDTwin 那一列的 y、隔線的 y。"""
    ys, y, prev = {}, 0.0, None
    for e in order:
        st = stage_of[e]
        if prev is not None and st != prev:
            y += GAP_STAGE
        ys[e] = y
        y += 1.0
        prev = st
    y_rule = y - 0.5 + GAP_NDT / 2.0
    y_ndt = y - 1.0 + GAP_NDT + 1.0
    return ys, y_ndt, y_rule


def draw(req, cap, order, stage_of):
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Liberation Sans", "DejaVu Sans", "Arial", "Helvetica"],
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "path",
        "axes.linewidth": 0.0,
    })

    ys, y_ndt, y_rule = row_y(order, stage_of)
    y_bottom = y_ndt + 0.5
    n_x = len(DIMS)

    fig_w, fig_h = 9.2, 6.6
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor("white")

    ax_l, ax_b, ax_w, ax_h = 0.158, 0.163, 0.835, 0.672
    ax = fig.add_axes([ax_l, ax_b, ax_w, ax_h])
    ax.set_xlim(-0.5, n_x - 0.5)
    ax.set_ylim(y_bottom, -0.5)
    ax.set_facecolor("white")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0, pad=4)

    def tile(cx, cy, cls):
        ax.add_patch(Rectangle(
            (cx - CELL_W / 2, cy - CELL_H / 2), CELL_W, CELL_H,
            facecolor=FILL[cls], edgecolor=EDGE[cls], linewidth=0.7, zorder=2))

    for e in order:
        for xi, d in enumerate(DIMS):
            tile(xi, ys[e], req[e][d])
    for xi, d in enumerate(DIMS):
        tile(xi, y_ndt, cap[d])

    # 13 支與 NDTwin today 之間的隔線
    ax.plot([-0.5, n_x - 0.5], [y_rule, y_rule], color=MUTED, lw=1.1,
            solid_capstyle="butt", zorder=3, clip_on=False)

    ax.set_xticks(range(n_x))
    ax.set_xticklabels(DIMS, rotation=45, ha="right", va="top",
                       fontsize=8.6, color=INK)
    ax.xaxis.set_ticks_position("bottom")

    yt = [ys[e] for e in order] + [y_ndt]
    ax.set_yticks(yt)
    ax.set_yticklabels(order + ["NDTwin today"], fontsize=8.8, color=INK)
    for lbl in ax.get_yticklabels()[-1:]:
        lbl.set_fontweight("bold")
        lbl.set_color(INK)

    # 標題
    fig.text(ax_l, 0.962, TITLE, fontsize=15.5, fontweight="bold",
             color=INK, ha="left", va="top")

    # 圖例：兩組各三格
    def handle(cls):
        return Rectangle((0, 0), 1, 1, facecolor=FILL[cls], edgecolor=EDGE[cls], linewidth=0.7)

    leg1 = ax.legend(
        [handle(c) for c in (REQ_CRITICAL, REQ_USED, REQ_NONE)],
        [LEGEND_LABEL[c] for c in (REQ_CRITICAL, REQ_USED, REQ_NONE)],
        title="EXERCISE NEEDS", loc="lower left", bbox_to_anchor=(0.0, 1.012),
        ncol=3, frameon=False, fontsize=8.8, handlelength=1.15, handleheight=1.05,
        handletextpad=0.5, columnspacing=1.25, borderpad=0.0, borderaxespad=0.0)
    leg1.get_title().set_fontsize(8.4)
    leg1.get_title().set_fontweight("bold")
    leg1.get_title().set_color(FAINT)
    leg1._legend_box.align = "left"
    for t in leg1.get_texts():
        t.set_color(INK)
    ax.add_artist(leg1)

    leg2 = ax.legend(
        [handle(c) for c in (CAP_YES, CAP_PARTIAL, CAP_NO)],
        [LEGEND_LABEL[c] for c in (CAP_YES, CAP_PARTIAL, CAP_NO)],
        title="NDTWIN TODAY", loc="lower left", bbox_to_anchor=(0.475, 1.012),
        ncol=3, frameon=False, fontsize=8.8, handlelength=1.15, handleheight=1.05,
        handletextpad=0.5, columnspacing=1.25, borderpad=0.0, borderaxespad=0.0)
    leg2.get_title().set_fontsize(8.4)
    leg2.get_title().set_fontweight("bold")
    leg2.get_title().set_color(FAINT)
    leg2._legend_box.align = "left"
    for t in leg2.get_texts():
        t.set_color(INK)

    return fig, (fig_w, fig_h)


# ----------------------------------------------------------------------------
# 7. 產 .md
# ----------------------------------------------------------------------------


def write_md(path: Path, req, raws, why, cap, cap_raw, order, stage_of,
             checks, cap_check, order_note, skipped_cols, png_size):
    def rel(p: Path) -> str:
        return str(p)

    L: list[str] = []
    a = L.append
    a(f"# `{STEM}` —— 13 支 tutorial exercise 的需求 vs. NDTwin 今天的供給")
    a("")
    a("[Co-developed with claude code -- Adam]")
    a("")
    a("## 一句話")
    a("")
    a("**13 支 p4lang/tutorials exercise 各自需要 16 個能力維度中的哪幾個（上半），"
      "對照 NDTwin 今天做得到哪幾個（底下隔開的那一列）。**")
    a("")
    a("## 資料來源（圖上每一格都出自這裡，腳本裡沒有手抄的數字）")
    a("")
    a(f"| 用途 | 檔 | 章節 |")
    a("|---|---|---|")
    a(f"| 需求矩陣 13×16 | `{rel(GAP1)}` | §2a 資料面／§2b 控制面／§2c 拓樸與驗證 |")
    a(f"| `meters`／`digest` 兩欄（§2 沒有這兩欄） | `{rel(GAP1)}` | §4b「只有少數支要的」的 `meters`／`digest` ＝ **0 支** |")
    a(f"| 對帳斷言（幾支要） | `{rel(GAP1)}` | §4a、§4b |")
    a(f"| NDTwin today 那一列 1×16 | `{rel(GAP2)}` | §1 能力矩陣＋文末「計數：做得到 1、部分 9、做不到 6」 |")
    a(f"| 列序（上→下） | `{rel(GAPA)}` | §6 三階段（定序）、§4 逐支可行性表（同序，做交叉驗證） |")
    a(f"| 色票 | `/home/adam/Desktop/NDTwin slide material/NDTwin slide material 827/NDTwin-slide-template-827.md` | §E2 色票與字體 |")
    a("")
    a("## 可信度")
    a("")
    a("🟠 **【讀碼推導】** —— 兩份來源都明講本輪**沒有執行任何東西**："
      "GAP-1 §0「本輪一個封包都沒送、一支 exercise 都沒跑，我只讀原始碼與設定檔」；"
      "GAP-2 §0「全部是【讀碼推導】：本輪沒起 fabric、沒跑 bmv2／Mininet／`ndt`、沒編譯」。")
    a("⇒ **這張圖是兩份讀碼盤點的視覺化，不是量測結果。**"
      "唯一夾帶【實測】標記的格子是 GAP-1 §2b 的 source_routing「灌幾筆」（三個檔都是空陣列，M7 §0），"
      "而那一欄不是 16 維之一、沒有進圖。")
    a("")
    a("## 圖怎麼讀")
    a("")
    a("- **上半 13 列**＝需求側，三色階（深藍`關鍵`／中藍`用到`／極淡`沒用到`）。")
    a("- **底下隔線之後那一列**＝NDTwin today，另一組三色階（綠`做得到`／琥珀`部分`／灰`做不到`）。")
    a("- **列序**由階段決定，階段之間留一道空白（沒有文字）：" + order_note)
    a("- **欄序**＝ GAP-1 §1 定義表的 16 個鍵順序（本腳本斷言解析到的集合與它相同）。")
    a("")
    a("## 我做的歸類判斷（全部）")
    a("")
    a("**機械規則**（先跑，三條）：")
    a("")
    a("1. 格值是 `—` ⇒ `沒用到`。")
    a("2. 格值（去掉 `**` 與反引號後）以「關鍵」開頭 ⇒ `關鍵`。"
      "涵蓋 `**關鍵** …` 與 `**關鍵：…**` 兩種寫法。")
    a("3. 其餘非空敘述 ⇒ `用到`。**注意**：`**用到但不讀**（bloom filter）`（firewall／registers）與"
      "`**跑時控制器**`（flowcache／p4runtime 的 control_plane_mode）都是粗體但**沒有**「關鍵」標記，"
      "照規則 3 歸 `用到` —— 粗體本身不代表關鍵。")
    a("")
    a("**攔截器**：任何格值以缺席詞（無／沒有／空／不需要／N-A）開頭、以「都沒有」結尾、"
      "帶問號、或以「部分」開頭，而又不在下面的例外表裡 ⇒ **腳本直接 `SystemExit`**，不猜。")
    a("")
    a("**逐格審過的例外（共 %d 格）**：" % len(REVIEWED))
    a("")
    a("| exercise | 維度 | 原文 | 歸給 | 依據 |")
    a("|---|---|---|---|---|")
    for (ex, d), (rawv, cls, reason) in REVIEWED.items():
        a(f"| {ex} | `{d}` | {rawv} | **{ZH_LABEL[cls]}** | {reason} |")
    a("")
    a("**兩個沒有進圖的欄位**（§2 有、16 維沒有）：")
    a("")
    for s in skipped_cols:
        a(f"- {s}")
    a("")
    a("  其中 `idle_timeout` 是 GAP-1 §1 自己註明「維度清單外、但必須另立一條」的第 17 維（只有 flowcache 用），"
      "本圖照題目給的 16 鍵清單，**不畫它**。GAP-ANALYSIS §2 也把它列在判定表最後一列並標「（額外）」。")
    a("")
    a("**兩個 §2 沒有欄位、由 §4b 補的維度**：`meters` 與 `digest`。§4b 明列兩者合計 **0 支**"
      "（「這批 exercise 完全不需要。做了不會有任何一支用到。」）⇒ 13 支全填 `沒用到`；"
      "腳本會斷言 §4b 的數字真的是 0，不是 0 就停。")
    a("")
    a("## 解析成功後跑的對帳斷言（任何一條不過就 `SystemExit`）")
    a("")
    for c in checks:
        a(f"- {c}")
    a(f"- {cap_check}")
    a("- 需求矩陣形狀 = 13×16；NDTwin 列 = 1×16；兩者的 16 個鍵集合相同。")
    a("- 列序：§4 的 13 列順序 == §6 的（階段一 + 階段二名單 + 餘數），逐位比對。")
    a("")
    a("## 逐格映射：需求側 13×16")
    a("")
    a("（原文照抄自 GAP-1 §2；`\\|` 已還原成 `|`。）")
    a("")
    for d in DIMS:
        a(f"### `{d}`")
        a("")
        a("| exercise | GAP-1 §2 原文 | 色階 | 為什麼 |")
        a("|---|---|---|---|")
        for e in order:
            cls = req[e][d]
            rv = raws[(e, d)].replace("|", "\\|")
            a(f"| {e} | {rv} | **{ZH_LABEL[cls]}** | {why[(e,d)]} |")
        a("")
    a("## 逐格映射：NDTwin today 1×16")
    a("")
    a("| 維度 | GAP-2 §1「今天」原文 | 色階 |")
    a("|---|---|---|")
    for d in DIMS:
        a(f"| `{d}` | {cap_raw[d]} | **{ZH_LABEL[cap[d]]}** |")
    a("")
    a("## 色票")
    a("")
    a("| 色階 | 色碼 | 出處 |")
    a("|---|---|---|")
    a(f"| 關鍵 | `{FILL[REQ_CRITICAL]}` | 827 模板 §E2 `ACCENT` |")
    a(f"| 用到 | `{FILL[REQ_USED]}` | `ACCENT` 混 55% 白 |")
    a(f"| 沒用到 | `{FILL[REQ_NONE]}` | 827 模板 §E2 `ACCENT_BG` |")
    a(f"| 做得到 | `{FILL[CAP_YES]}` | 綠／琥珀／灰一組（題目給的選項），與藍色系分得開 |")
    a(f"| 部分 | `{FILL[CAP_PARTIAL]}` | 同上 |")
    a(f"| 做不到 | `{FILL[CAP_NO]}` | 同上 |")
    a("")
    a("字體：無襯線（Liberation Sans → DejaVu Sans → Arial 依序 fallback）。"
      "圖上文字只有標題、兩軸的刻度標籤、兩組圖例 —— **沒有任何句子**。")
    a("")
    a("## 重生指令")
    a("")
    a("```bash")
    a('cd "/home/adam/Desktop/NDTwin slide material/NDTWIN slide material 916/figures/p4-tutorials"')
    a('"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \\')
    a("    make_tutorial_figs.py")
    a("```")
    a("")
    a("產出：")
    a("")
    a(f"- `{STEM}.pdf`")
    a(f"- `{STEM}.png`（300 dpi，{png_size[0]}×{png_size[1]} px）")
    a(f"- `{STEM}.svg`")
    a(f"- `_hires/{STEM}.png`（500 dpi）")
    a(f"- `{STEM}.md`（本檔，同一支腳本產出，因此**不會與圖脫節**）")
    a("")
    a(f"最後產出：{_dt.datetime.now().strftime('%Y-%m-%d %H:%M')}；"
      f"matplotlib {matplotlib.__version__}；Python {sys.version.split()[0]}。")
    a("")
    path.write_text("\n".join(L), encoding="utf-8")


# ----------------------------------------------------------------------------
# 8. main
# ----------------------------------------------------------------------------


def main() -> int:
    req, raws, why, checks, skipped = parse_gap1(read(GAP1))
    cap, cap_raw, cap_check = parse_gap2(read(GAP2))
    order, stage_of, order_note = parse_row_order(read(GAPA))

    # 形狀斷言
    if len(req) != 13 or any(len(req[e]) != 16 for e in req):
        die(f"需求矩陣形狀不是 13×16："
            f"{len(req)} 列，欄數 {sorted({len(v) for v in req.values()})}")
    if len(cap) != 16:
        die(f"NDTwin 列不是 1×16，是 1×{len(cap)}")
    print(f"[shape] 需求矩陣 {len(req)}×{len(next(iter(req.values())))}  "
          f"NDTwin 列 1×{len(cap)}")
    print(f"[order] {order}")
    for c in checks + [cap_check]:
        print("[check] " + c)

    HIRES_DIR.mkdir(parents=True, exist_ok=True)
    fig, (fw, fh) = draw(req, cap, order, stage_of)

    pdf = OUT_DIR / f"{STEM}.pdf"
    png = OUT_DIR / f"{STEM}.png"
    svg = OUT_DIR / f"{STEM}.svg"
    png5 = HIRES_DIR / f"{STEM}.png"
    fig.savefig(pdf, format="pdf", facecolor="white")
    fig.savefig(png, format="png", dpi=300, facecolor="white")
    fig.savefig(svg, format="svg", facecolor="white")
    fig.savefig(png5, format="png", dpi=500, facecolor="white")
    plt.close(fig)

    from PIL import Image
    with Image.open(png) as im:
        png_size = im.size
    with Image.open(png5) as im:
        png5_size = im.size

    write_md(OUT_DIR / f"{STEM}.md", req, raws, why, cap, cap_raw, order, stage_of,
             checks, cap_check, order_note, skipped, png_size)

    print(f"[figure] {fw}x{fh} in  (w:h = {fw/fh:.2f})")
    for p, s in ((png, png_size), (png5, png5_size)):
        print(f"[png] {p.name} {s[0]}x{s[1]}  ({p})")
    for p in (pdf, svg, OUT_DIR / f"{STEM}.md"):
        print(f"[out] {p}  {os.path.getsize(p)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
