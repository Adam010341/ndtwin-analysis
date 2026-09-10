# fig_t3b_election_wipe — 冒名者清空全表、然後回報成功

投影片 **T3 右圖**（`WHAT ONLY A FOREIGN P4 PROGRAM REVEALS`）。一句話：**proxy 的十個 client 與
tutorials 自帶的 `mycontroller.py` 投同一個寫死的 `election_id (0,1)`；bmv2 依規格把冒名者的
stream 當重複殺掉，但它的 `SetForwardingPipelineConfig` 照樣被接受、清空每一張表、回 `OK`。**

產出：`fig_t3b_election_wipe.{pdf,png,svg}` ＋ `_hires/fig_t3b_election_wipe.png`
（PNG 1680×1710 @300 dpi、hires 2800×2850 @500 dpi；畫布 5.60×5.70 in，與 `fig_t3a` 同高）。
型：序列圖，三條生命線。

---

## 0. 可信度

🟢 **【跑過】2026-08-13 三情境 live 實測。圖左下 chip `MEASURED 08-13` 就是這件事。**
**這是 T 頁組四張圖裡唯一一個實測的機制。**

- 正本：`doc/2026-08-13_p4runtime-mastership-spec-check.md` §2（三情境表）。
- 工具：`p4_proxy/reference/p4runtime_mastership_probe.py` —— **第三方 client，只用 raw grpc ＋
  stock protobuf，與 `p4_client.py` 零共用組包程式碼**（排除我方 client 的嫌疑本來就是那一步的目的），
  可重跑。
- 對象：本機 `simple_switch_grpc` **1.15.3-f0b7d201**，10 台 live bmv2，每情境各一台乾淨 device。
- 🟠 **只有一半是讀碼**：`mycontroller.py:167-176` 寫死 `127.0.0.1:50051/dev 0`、NDTwin 是
  `GRPC_PORT_BASE=30050`／`device_id=dpid`（`grpc_ports.py:39,48,66`、`main.py:182-186`）⇒
  **連位址都對不上**。**這一條沒畫進圖**（見 §2），講者備註帶。

## 1. 五個元素對應的來源

| 圖上 | 出處 |
|---|---|
| 生命線 `proxy client · election (0,1)` | `p4_proxy/proxy_agent/p4_client.py:232-235`（本 session 讀過）：`req.arbitration.election_id.high = 0` / `.low = 1`。`p4_client.py:60-72` 註解自陳「Every client built here bids the same hardcoded election_id (0, 1)」 |
| 生命線 `mycontroller · election (0,1)` | `GAP-ANALYSIS` §5-發現②：「tutorials **普遍自帶控制器**——`p4runtime` 與 `flowcache` 整支的教學重點就是跑 `mycontroller.py`」；`GAP-1` §3.6／§3.11 |
| `StreamChannel · primary`（proxy→bmv2，實線） | 08-13 文件 §2 情境 2 的 client `O`：`(0,1)` primary |
| `StreamChannel` **虛線**＋`killed: duplicate`（controller→bmv2） | 08-13 文件 §2 情境 2 的 client `D`：`(0,1)` 重複、**D 的 stream 被殺**；§3-2 逐字：bmv2 回 `INVALID_ARGUMENT: Election id already exists`（＝**重複**，不是「較低」） |
| `SetForwardingPipelineConfig` 實線＋`accepted` | 08-13 §2 情境 2 那一格：pipeline push **`OK`（清表 1→0）** |
| `tables wiped`（bmv2 內部，`WARN_BG` 底、`WARNC` 字） | 同上「清表 1→0」；`p4_client.py:60-72` 自陳「the impostor's SetForwardingPipelineConfig is accepted and **wipes every table**」；KNOWN-ISSUES **A-4c** |
| `OK`（bmv2→controller，`WARNC` 字） | 同上；`p4_client.py:60-72`「readopt against a healthy switch wiped its tables, installed nothing, and **reported success**」 |

## 2. 圖上**刻意沒畫**的（都在講者備註）

- **對照組（bmv2 沒有違規）**：08-13 §2 情境 1 —— 真正非 primary 的第三方 client，pipeline push
  被 `PERMISSION_DENIED: Not primary` **擋下**。這是 08-13 那份文件推翻自己原主張的那一格
  （原本要向上游回報 bmv2 違規，**已取消**）。畫進序列圖要第四條生命線，會蓋掉主線。
  ⚠️ **上台一定要講**：不然聽起來像在指控 bmv2。
- **情境 3（順序）**：`old.stop()` 之後所有 route write 才變 `Not primary`
  （08-13 §3-4，`topology_manager.py:831,836`）。那是 readopt 的 bug 形狀，不是本頁的題目。
- **位址對不上**（`50051/dev 0` vs `30050+dpid`）：🟠 讀碼，與圖上的 🟢 不可混寫 ⇒ 不上圖。
- **修法**（G3 候選 A：election_id 提成參數、NDTwin 用高值，~15 行【估】＋位址對齊 ~10 行）：
  屬於 T2 的 `G3 ~15` 徽章。

## 3. Regenerate

```
cd "/home/adam/Desktop/NDTwin slide material/NDTWIN slide material 916/figures/p4-tutorials"
"/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
    make_gap_diagrams.py
```
修改函式：`fig_t3b()`。字型與 `_hires` 的口徑見 `fig_t2_gap_architecture.md` §5。

[Co-developed with claude code -- Adam]
