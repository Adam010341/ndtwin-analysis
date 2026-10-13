#!/usr/bin/env python3
"""
make_background_figs.py -- the two figures of the 930 deck's background section (B; Adam 2026-09-29):

  fig_b2_basic_walkthrough  (B2)  the p4lang/tutorials exercise `basic`: what the student writes, the
                                  path one packet takes through the program, the topology it runs on
                                  and where its table entries come from.
  fig_b3_basic_tunnel       (B3)  the exercise `basic_tunnel`: its own header (etherType read from the
                                  source), the parser branch, its exact-match table beside ipv4_lpm, and
                                  what a tunnelled packet does on the triangle.

Both are READ figures: nothing here was run.  Every table, action, key, constant, port, host address
and entry drawn on the canvas is read from the tutorials checkout at commit PIN with `git show` (so the
working tree's own edits -- the checkout has a comment-only change in exercises/basic/basic.p4 -- never
leak in) and checked; a missing or changed anchor stops the script with a named reason instead of
drawing a stale picture.  The only hand-written text is the layout, the friendly labels of the
four ipv4_forward statements (each tied to the source statement it labels, which is checked) and the
node positions (the node set is checked against the topology file).

[Co-developed with claude code -- Adam]

Regenerate:
    cd "/home/adam/Desktop/NDTwin slide material/NDTwin slide material 930/figures/background"
    "/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3" \
        make_background_figs.py
"""
import ipaddress
import json
import os
import re
import subprocess
import sys

import matplotlib

assert matplotlib.__version__.startswith("3.11"), matplotlib.__version__
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle  # noqa: E402

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["font.monospace"] = ["Courier New", "Liberation Mono", "DejaVu Sans Mono"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

TUT = os.environ.get("NDTWIN_TUTORIALS", "/home/adam/tutorials")
PIN = "c80d83e"                 # the tutorials commit every live run of the deck used

OUTDIR = os.path.dirname(os.path.abspath(__file__))
HIRES = os.path.join(OUTDIR, "_hires")

INK, BODY, MUTED, FAINT, RULE = "#1A1A1A", "#2E2E2E", "#4F4F4F", "#6E6E6E", "#D0D0D0"
ACCENT, ACCENT_BG, PANEL = "#065A82", "#EEF3F6", "#F7F8F9"
WHITE, GREY = "#FFFFFF", "#C9CDD0"
W, H = 13.33, 6.9

# the four statements of ipv4_forward, as the solution writes them (whitespace-normalised),
# and the label the figure prints for each.  The statements are checked against the source.
FWD = (
    ("standard_metadata.egress_spec = port", "egress port ← port"),
    ("hdr.ethernet.srcAddr = hdr.ethernet.dstAddr", "src MAC ← old dst MAC"),
    ("hdr.ethernet.dstAddr = dstAddr", "dst MAC ← dstAddr"),
    ("hdr.ipv4.ttl = hdr.ipv4.ttl - 1", "TTL − 1"),
)
TUN_FWD = (("standard_metadata.egress_spec = port", "egress port ← port"),)

# the packet each figure follows
B2_SRC, B2_DST = "h1", "h3"
B3_SRC, B3_IP_DST, B3_DST_ID = "h1", "h3", 2

# node positions (inches, y down); the node SET is checked against the topology file
B2_POS = {"s3": (1.95, 4.42), "s4": (4.95, 4.42), "s1": (1.95, 5.40), "s2": (4.95, 5.40),
          "h1": (1.25, 6.30), "h2": (2.65, 6.30), "h3": (4.25, 6.30), "h4": (5.65, 6.30)}
B3_POS = {"s1": (2.10, 6.05), "s2": (5.05, 6.05), "s3": (3.575, 5.10),
          "h1": (0.80, 6.05), "h2": (6.30, 6.05), "h3": (5.05, 5.10)}


def die(msg):
    raise SystemExit(f"make_background_figs: {msg}")


# ------------------------------------------------------------------ reading the source at PIN
def git(*args):
    return subprocess.run(["git", "-C", TUT, *args], capture_output=True, text=True)


def check_pin():
    r = git("rev-parse", "--verify", "--quiet", f"{PIN}^{{commit}}")
    if r.returncode != 0 or not r.stdout.strip():
        die(f"the tutorials checkout {TUT} has no commit {PIN}")
    return r.stdout.strip()


def read(rel):
    r = git("show", f"{PIN}:{rel}")
    if r.returncode != 0:
        die(f"cannot read {rel} at {PIN} in {TUT}")
    return r.stdout


def blank_comments(s):
    """Same length as s, comments replaced by spaces (newlines kept), so spans found here slice s."""
    out = list(s)
    for m in re.finditer(r"/\*.*?\*/|//[^\n]*", s, flags=re.S):
        for i in range(m.start(), m.end()):
            if out[i] != "\n":
                out[i] = " "
    return "".join(out)


def span(code, head, start=0, end=None):
    """(i, j): the inside of the first {...} after regex `head` in code[start:end], or None."""
    end = len(code) if end is None else end
    m = re.compile(head).search(code, start, end)
    if not m:
        return None
    i = code.find("{", m.start(), end)
    if i < 0:
        return None
    depth = 0
    for j in range(i, end):
        if code[j] == "{":
            depth += 1
        elif code[j] == "}":
            depth -= 1
            if depth == 0:
                return (i + 1, j)
    return None


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def norm(s):
    return " ".join(s.split())


def statements(code, sp):
    return [norm(x) for x in code[sp[0]:sp[1]].split(";") if norm(x)]


class P4:
    """One .p4 file at PIN: raw text, comment-blanked code, and the anchors the figures need."""

    def __init__(self, rel):
        self.rel = rel
        self.raw = read(rel)
        self.code = blank_comments(self.raw)
        self.anchors = []

    def at(self, what, idx):
        self.anchors.append((what, f"{self.rel}:{line_of(self.raw, idx)}"))

    def const(self, name):
        m = re.search(rf"\bconst\s+bit<16>\s+{name}\s*=\s*(0x[0-9A-Fa-f]+)\s*;", self.code)
        if not m:
            return None
        self.at(f"const {name}", m.start())
        return int(m.group(1), 16)

    def block(self, head, inside=None):
        sp = span(self.code, head, *(inside or (0, None)))
        if sp:
            self.at(head, sp[0])
        return sp

    def control(self, name):
        return self.block(rf"\bcontrol\s+{name}\s*\(")

    def control_apply(self, ctl):
        """The control's own apply block: the last `apply {` directly in it (not x.apply())."""
        last = None
        for m in re.finditer(r"(?<![\w.])apply\s*\{", self.code[ctl[0]:ctl[1]]):
            last = m
        if last is None:
            return None
        return span(self.code, r"(?<![\w.])apply\s*\{", ctl[0] + last.start(), ctl[1])

    def todo_in(self, sp):
        return sp is not None and "TODO" in self.raw[sp[0]:sp[1]]

    def todo_line_naming(self, word):
        return any("TODO" in ln and word in ln for ln in self.raw.splitlines())


def table_info(p4, ctl, name, where):
    sp = p4.block(rf"\btable\s+{name}\b", ctl)
    if sp is None:
        die(f"{where}: no table {name} in MyIngress")
    t = p4.code[sp[0]:sp[1]]
    k = span(t, r"\bkey\s*=")
    keys = re.findall(r"([\w.]+)\s*:\s*(\w+)\s*;", t[k[0]:k[1]]) if k else []
    a = span(t, r"\bactions\s*=")
    acts = [norm(x) for x in t[a[0]:a[1]].split(";") if norm(x)] if a else []
    m = re.search(r"\bdefault_action\s*=\s*(\w+)\s*\(\s*\)\s*;", t)
    return {"keys": keys, "actions": acts, "default": m.group(1) if m else None}


def action_info(p4, ctl, name, where):
    m = re.compile(rf"\baction\s+{name}\s*\(([^)]*)\)").search(p4.code, ctl[0], ctl[1])
    if not m:
        die(f"{where}: no action {name} in MyIngress")
    params = [norm(p).split()[-1] for p in m.group(1).split(",") if norm(p)]
    types = [norm(p).split()[0] for p in m.group(1).split(",") if norm(p)]
    sp = span(p4.code, rf"\baction\s+{name}\s*\(", ctl[0], ctl[1])
    p4.at(f"action {name}", m.start())
    return {"params": params, "types": types, "body": statements(p4.code, sp), "span": sp}


def parser_states(p4, where):
    ps = p4.block(r"\bparser\s+MyParser\s*\(")
    if ps is None:
        die(f"{where}: no parser MyParser")
    states = {}
    for m in re.finditer(r"\bstate\s+(\w+)\s*\{", p4.code[ps[0]:ps[1]]):
        sp = span(p4.code, r"\bstate\s+\w+\s*\{", ps[0] + m.start(), ps[1])
        states[m.group(1)] = p4.code[sp[0]:sp[1]]
        p4.at(f"state {m.group(1)}", sp[0])
    return ps, states


def select_cases(state_body, field):
    """{label: next_state} of `transition select(<field>) { label: next; ... }`, or None."""
    m = re.search(rf"transition\s+select\s*\(\s*{re.escape(field)}\s*\)", state_body)
    if not m:
        return None
    sp = span(state_body, r"transition\s+select\s*\(")
    return dict(re.findall(r"(\w+)\s*:\s*(\w+)\s*;", state_body[sp[0]:sp[1]]))


def emits(p4, where):
    dp = p4.control("MyDeparser")
    if dp is None:
        die(f"{where}: no control MyDeparser")
    return dp, re.findall(r"packet\.emit\(\s*([\w.]+)\s*\)", p4.code[dp[0]:dp[1]])


# ------------------------------------------------------------------ topology and entries
def topo_path(ex):
    mk = read(f"exercises/{ex}/Makefile")
    m = re.search(r"^TOPO\s*=\s*(\S+)\s*$", mk, flags=re.M)
    if m:
        return m.group(1)
    um = read("utils/Makefile")
    d = re.search(r"^ifndef TOPO\s*\nTOPO\s*=\s*(\S+)\s*$", um, flags=re.M)
    if not d:
        die(f"{ex}: its Makefile sets no TOPO and utils/Makefile has no default TOPO")
    return d.group(1)


def load_topology(ex, pos):
    rel = topo_path(ex)
    base = os.path.dirname(rel)
    try:
        topo = json.loads(read(f"exercises/{ex}/{rel}"))
        hosts, switches, links = topo["hosts"], topo["switches"], topo["links"]
    except (ValueError, KeyError) as e:
        die(f"{ex}: {rel} is not a hosts/switches/links topology ({e})")
    nodes = set(hosts) | set(switches)
    if nodes != set(pos):
        die(f"{ex}: the topology's nodes {sorted(nodes)} are not the drawn layout's {sorted(pos)}")
    ports = {}                              # (switch, port) -> neighbour node, or (switch, port)
    for a, b in links:
        ends = []
        for e in (a, b):
            m = re.fullmatch(r"(s\d+)-p(\d+)", e)
            if m and m.group(1) in switches:
                ends.append((m.group(1), int(m.group(2))))
            elif e in hosts:
                ends.append(e)
            else:
                die(f"{ex}: link end {e!r} in {rel} is neither a host nor sN-pK of a declared switch")
        for x, y in ((ends[0], ends[1]), (ends[1], ends[0])):
            if isinstance(x, tuple):
                ports[x] = y
    attach = {}
    for (sw, p), nb in ports.items():
        if isinstance(nb, str):
            attach[nb] = (sw, p)
    for h in hosts:
        if h not in attach:
            die(f"{ex}: host {h} is attached to no switch in {rel}")
    runtimes = {}
    for sw, cfg in switches.items():
        rj = cfg.get("runtime_json") if isinstance(cfg, dict) else None
        if not rj:
            die(f"{ex}: switch {sw} has no runtime_json in {rel}")
        try:
            runtimes[sw] = json.loads(read(f"exercises/{ex}/{rj}"))["table_entries"]
        except (ValueError, KeyError) as e:
            die(f"{ex}: {rj} has no table_entries ({e})")
    return {"rel": rel, "base": base, "hosts": hosts, "switches": switches, "links": links,
            "ports": ports, "attach": attach, "runtimes": runtimes}


def check_entries(ex, topo, tables, actions):
    """Every runtime entry names a table and an action the solution declares, with its key and
    parameter names.  tables: {'MyIngress.x': keys}; actions: {'MyIngress.y': params}."""
    for sw, entries in topo["runtimes"].items():
        for e in entries:
            t, a = e.get("table"), e.get("action_name")
            if t not in tables:
                die(f"{ex}: {sw}'s runtime names table {t!r}, which the solution does not declare")
            if a not in actions:
                die(f"{ex}: {sw}'s runtime names action {a!r}, which the solution does not declare")
            if not e.get("default_action"):
                want = [k for k, _ in tables[t]]
                if list(e.get("match", {})) != want:
                    die(f"{ex}: {sw}'s entry in {t} matches {list(e.get('match', {}))}, not the key {want}")
            if sorted(e.get("action_params", {})) != sorted(actions[a]):
                die(f"{ex}: {sw}'s {a} entry has params {sorted(e.get('action_params', {}))}, "
                    f"not {sorted(actions[a])}")


def lpm_port(entries, table, field, ip):
    best = None
    for e in entries:
        if e.get("table") != table or e.get("default_action"):
            continue
        addr, plen = e["match"][field]
        net = ipaddress.ip_network(f"{addr}/{plen}", strict=False)
        if ipaddress.ip_address(ip) in net and (best is None or plen > best[0]):
            best = (plen, e)
    return best[1] if best else None


def exact_port(entries, table, field, value):
    for e in entries:
        if e.get("table") == table and not e.get("default_action") and e["match"][field] == [value]:
            return e
    return None


def walk(ex, topo, src, lookup, what):
    """Follow one packet from host src switch by switch; lookup(switch) -> entry or None."""
    sw, _ = topo["attach"][src]
    hops, seen = [(src, None)], set()
    while True:
        if sw in seen:
            die(f"{ex}: {what} loops at {sw}")
        seen.add(sw)
        e = lookup(sw)
        if e is None:
            die(f"{ex}: {what}: {sw} has no entry for it (the default action would drop it)")
        port = int(e["action_params"]["port"])
        hops.append((sw, port))
        nb = topo["ports"].get((sw, port))
        if nb is None:
            die(f"{ex}: {what}: {sw} port {port} leads to no link in {topo['rel']}")
        if isinstance(nb, str):
            hops.append((nb, None))
            return hops
        sw = nb[0]


# ------------------------------------------------------------------ what each figure needs
def basic_facts():
    where = "basic solution"
    sol = P4("exercises/basic/solution/basic.p4")
    ipv4 = sol.const("TYPE_IPV4")
    if ipv4 is None:
        die(f"{where}: no const TYPE_IPV4")
    _, st = parser_states(sol, where)
    for s in ("parse_ethernet", "parse_ipv4"):
        if s not in st:
            die(f"{where}: the parser has no state {s}")
    if "packet.extract(hdr.ethernet)" not in norm(st["parse_ethernet"]).replace(" ", ""):
        die(f"{where}: parse_ethernet does not extract hdr.ethernet")
    cases = select_cases(st["parse_ethernet"], "hdr.ethernet.etherType")
    if not cases or cases.get("TYPE_IPV4") != "parse_ipv4":
        die(f"{where}: parse_ethernet does not go to parse_ipv4 on TYPE_IPV4")
    if "packet.extract(hdr.ipv4)" not in norm(st["parse_ipv4"]).replace(" ", ""):
        die(f"{where}: parse_ipv4 does not extract hdr.ipv4")
    ing = sol.control("MyIngress")
    if ing is None:
        die(f"{where}: no control MyIngress")
    fwd = action_info(sol, ing, "ipv4_forward", where)
    if fwd["params"] != ["dstAddr", "port"]:
        die(f"{where}: ipv4_forward takes {fwd['params']}, not (dstAddr, port)")
    for stmt, _ in FWD:
        if stmt not in fwd["body"]:
            die(f"{where}: ipv4_forward lacks the statement `{stmt}`")
    lpm = table_info(sol, ing, "ipv4_lpm", where)
    if lpm["keys"] != [("hdr.ipv4.dstAddr", "lpm")]:
        die(f"{where}: ipv4_lpm's key is {lpm['keys']}, not hdr.ipv4.dstAddr: lpm")
    for a in ("ipv4_forward", "drop"):
        if a not in lpm["actions"]:
            die(f"{where}: ipv4_lpm does not list the action {a}")
    if lpm["default"] != "drop":
        die(f"{where}: ipv4_lpm's default_action is {lpm['default']}, not drop")
    ap = sol.control_apply(ing)
    body = norm(sol.code[ap[0]:ap[1]]).replace(" ", "") if ap else ""
    if not re.search(r"if\(hdr\.ipv4\.isValid\(\)\)\{ipv4_lpm\.apply\(\);\}", body):
        die(f"{where}: MyIngress's apply does not apply ipv4_lpm under hdr.ipv4.isValid()")
    _, em = emits(sol, where)
    if em != ["hdr.ethernet", "hdr.ipv4"]:
        die(f"{where}: the deparser emits {em}, not hdr.ethernet then hdr.ipv4")
    ck = sol.control("MyComputeChecksum")
    if ck is None or "hdr.ipv4.hdrChecksum" not in sol.code[ck[0]:ck[1]] \
            or "update_checksum" not in sol.code[ck[0]:ck[1]]:
        die(f"{where}: MyComputeChecksum does not update hdr.ipv4.hdrChecksum")

    # the skeleton: what the student writes (TODO) and what is given
    where = "basic skeleton"
    sk = P4("exercises/basic/basic.p4")
    sk_ing = sk.control("MyIngress")
    if sk_ing is None:
        die(f"{where}: no control MyIngress")
    sk_lpm = table_info(sk, sk_ing, "ipv4_lpm", where)
    if sk_lpm["keys"] != [("hdr.ipv4.dstAddr", "lpm")]:
        die(f"{where}: ipv4_lpm is not given with key hdr.ipv4.dstAddr: lpm (the figure draws it as given)")
    sk_fwd = action_info(sk, sk_ing, "ipv4_forward", where)
    if sk_fwd["body"]:
        die(f"{where}: ipv4_forward already has statements (the figure marks its body as the student's)")
    todo = {
        "parser": sk.todo_in(sk.block(r"\bparser\s+MyParser\s*\(")),
        "ipv4_forward": sk.todo_in(sk_fwd["span"]),
        "apply": sk.todo_in(sk.control_apply(sk_ing)),
        "deparser": sk.todo_in(sk.control("MyDeparser")),
    }
    for k, v in todo.items():
        if not v:
            die(f"{where}: {k} has no TODO (the figure marks it as the student's part)")
    readme = read("exercises/basic/README.md")
    if "drops all packets" not in readme:
        die("basic README: it no longer says the skeleton drops all packets")

    topo = load_topology("basic", B2_POS)
    tables = {"MyIngress.ipv4_lpm": lpm["keys"]}
    actions = {"MyIngress.ipv4_forward": fwd["params"], "MyIngress.drop": []}
    check_entries("basic", topo, tables, actions)
    dst_ip = topo["hosts"][B2_DST]["ip"].split("/")[0]
    path = walk("basic", topo, B2_SRC,
                lambda sw: lpm_port(topo["runtimes"][sw], "MyIngress.ipv4_lpm", "hdr.ipv4.dstAddr",
                                    dst_ip), f"{B2_SRC} -> {dst_ip}")
    if path[-1][0] != B2_DST:
        die(f"basic: {B2_SRC} -> {dst_ip} ends at {path[-1][0]}, not {B2_DST}")
    s1 = topo["runtimes"]["s1"]
    default = [e for e in s1 if e.get("default_action")]
    if len(default) != 1 or default[0]["action_name"] != "MyIngress.drop":
        die("basic: s1's runtime does not set exactly one default, MyIngress.drop")
    return {"ipv4": ipv4, "fwd": fwd, "lpm": lpm, "todo": todo, "topo": topo, "path": path,
            "dst_ip": dst_ip, "anchors": sol.anchors + sk.anchors}


def tunnel_facts():
    where = "basic_tunnel solution"
    sol = P4("exercises/basic_tunnel/solution/basic_tunnel.p4")
    tun, ipv4 = sol.const("TYPE_MYTUNNEL"), sol.const("TYPE_IPV4")
    if tun is None:
        die(f"{where}: no const TYPE_MYTUNNEL")
    if ipv4 is None:
        die(f"{where}: no const TYPE_IPV4")
    hdr = sol.block(r"\bheader\s+myTunnel_t\b")
    fields = re.findall(r"bit<(\d+)>\s+(\w+)\s*;", sol.code[hdr[0]:hdr[1]]) if hdr else []
    if [f for _, f in fields] != ["proto_id", "dst_id"]:
        die(f"{where}: header myTunnel_t's fields are {fields}, not proto_id, dst_id")
    _, st = parser_states(sol, where)
    for s in ("parse_ethernet", "parse_myTunnel", "parse_ipv4"):
        if s not in st:
            die(f"{where}: the parser has no state {s}")
    c1 = select_cases(st["parse_ethernet"], "hdr.ethernet.etherType") or {}
    if c1.get("TYPE_MYTUNNEL") != "parse_myTunnel" or c1.get("TYPE_IPV4") != "parse_ipv4":
        die(f"{where}: parse_ethernet does not branch TYPE_MYTUNNEL -> parse_myTunnel and "
            f"TYPE_IPV4 -> parse_ipv4")
    if "packet.extract(hdr.myTunnel)" not in norm(st["parse_myTunnel"]).replace(" ", ""):
        die(f"{where}: parse_myTunnel does not extract hdr.myTunnel")
    c2 = select_cases(st["parse_myTunnel"], "hdr.myTunnel.proto_id") or {}
    if c2.get("TYPE_IPV4") != "parse_ipv4":
        die(f"{where}: parse_myTunnel does not go to parse_ipv4 when proto_id is TYPE_IPV4")
    ing = sol.control("MyIngress")
    if ing is None:
        die(f"{where}: no control MyIngress")
    tfwd = action_info(sol, ing, "myTunnel_forward", where)
    if tfwd["params"] != ["port"] or [s for s, _ in TUN_FWD if s not in tfwd["body"]]:
        die(f"{where}: myTunnel_forward is not (port) setting standard_metadata.egress_spec = port")
    ex = table_info(sol, ing, "myTunnel_exact", where)
    if ex["keys"] != [("hdr.myTunnel.dst_id", "exact")]:
        die(f"{where}: myTunnel_exact's key is {ex['keys']}, not hdr.myTunnel.dst_id: exact")
    if "myTunnel_forward" not in ex["actions"] or ex["default"] != "drop":
        die(f"{where}: myTunnel_exact does not list myTunnel_forward with default drop")
    fwd = action_info(sol, ing, "ipv4_forward", where)
    lpm = table_info(sol, ing, "ipv4_lpm", where)
    if lpm["keys"] != [("hdr.ipv4.dstAddr", "lpm")] or fwd["params"] != ["dstAddr", "port"] \
            or [s for s, _ in FWD if s not in fwd["body"]]:
        die(f"{where}: ipv4_lpm / ipv4_forward are not basic's (the figure says \"as in basic\")")
    ap = sol.control_apply(ing)
    body = norm(sol.code[ap[0]:ap[1]]).replace(" ", "") if ap else ""
    if "if(hdr.ipv4.isValid()&&!hdr.myTunnel.isValid()){ipv4_lpm.apply();}" not in body \
            or "if(hdr.myTunnel.isValid()){myTunnel_exact.apply();}" not in body:
        die(f"{where}: MyIngress's apply is not (IPv4 and no tunnel -> ipv4_lpm; tunnel -> myTunnel_exact)")
    _, em = emits(sol, where)
    if em != ["hdr.ethernet", "hdr.myTunnel", "hdr.ipv4"]:
        die(f"{where}: the deparser emits {em}, not ethernet, myTunnel, ipv4")

    where = "basic_tunnel skeleton"
    sk = P4("exercises/basic_tunnel/basic_tunnel.p4")
    if sk.const("TYPE_MYTUNNEL") != tun or sk.block(r"\bheader\s+myTunnel_t\b") is None:
        die(f"{where}: the header myTunnel_t / TYPE_MYTUNNEL is not given (the figure draws it as given)")
    sk_ing = sk.control("MyIngress")
    if sk_ing is None:
        die(f"{where}: no control MyIngress")
    for kind, name in (("table", "myTunnel_exact"), ("action", "myTunnel_forward")):
        if re.compile(rf"\b{kind}\s+{name}\b").search(sk.code, sk_ing[0], sk_ing[1]):
            die(f"{where}: it already declares {kind} {name} (the figure marks it as the student's)")
    todo = {
        "parser": sk.todo_line_naming("parser"),
        "myTunnel_forward": sk.todo_line_naming("myTunnel_forward"),
        "myTunnel_exact": sk.todo_line_naming("myTunnel_exact"),
        "apply": sk.todo_in(sk.control_apply(sk_ing)),
        "deparser": sk.todo_in(sk.control("MyDeparser")),
    }
    for k, v in todo.items():
        if not v:
            die(f"{where}: {k} has no TODO (the figure marks it as the student's part)")

    # the hosts: how a tunnelled packet is built
    hp = read("exercises/basic_tunnel/myTunnel_header.py")
    m = re.search(r"^TYPE_MYTUNNEL\s*=\s*(0x[0-9A-Fa-f]+)", hp, flags=re.M)
    if not m or int(m.group(1), 16) != tun:
        die("basic_tunnel: myTunnel_header.py's TYPE_MYTUNNEL is not the switch's")
    if not re.search(r"bind_layers\(\s*Ether\s*,\s*MyTunnel\s*,\s*type\s*=\s*TYPE_MYTUNNEL\s*\)", hp):
        die("basic_tunnel: myTunnel_header.py does not bind MyTunnel under Ether by TYPE_MYTUNNEL")
    sp_ = read("exercises/basic_tunnel/send.py")
    if not re.search(r"/\s*MyTunnel\(\s*dst_id\s*=\s*dst_id\s*\)\s*/\s*IP\(\s*dst\s*=\s*addr\s*\)", sp_):
        die("basic_tunnel: send.py does not put MyTunnel(dst_id) between Ether and IP")

    topo = load_topology("basic_tunnel", B3_POS)
    tables = {"MyIngress.ipv4_lpm": lpm["keys"], "MyIngress.myTunnel_exact": ex["keys"]}
    actions = {"MyIngress.ipv4_forward": fwd["params"], "MyIngress.myTunnel_forward": tfwd["params"],
               "MyIngress.drop": []}
    check_entries("basic_tunnel", topo, tables, actions)
    if not any(e["table"] == "MyIngress.myTunnel_exact" for es in topo["runtimes"].values() for e in es):
        die("basic_tunnel: no runtime entry names MyIngress.myTunnel_exact (the legend says the "
            "skeleton's entries name a table it lacks)")
    ip_dst = topo["hosts"][B3_IP_DST]["ip"].split("/")[0]
    ip_path = walk("basic_tunnel", topo, B3_SRC,
                   lambda sw: lpm_port(topo["runtimes"][sw], "MyIngress.ipv4_lpm", "hdr.ipv4.dstAddr",
                                       ip_dst), f"IPv4 {B3_SRC} -> {ip_dst}")
    tun_path = walk("basic_tunnel", topo, B3_SRC,
                    lambda sw: exact_port(topo["runtimes"][sw], "MyIngress.myTunnel_exact",
                                          "hdr.myTunnel.dst_id", B3_DST_ID), f"dst_id {B3_DST_ID}")
    if ip_path[-1][0] != B3_IP_DST:
        die(f"basic_tunnel: IPv4 {B3_SRC} -> {ip_dst} ends at {ip_path[-1][0]}, not {B3_IP_DST}")
    if tun_path[-1][0] == ip_path[-1][0]:
        die(f"basic_tunnel: dst_id {B3_DST_ID} ends at {ip_path[-1][0]} like the IPv4 path "
            f"(the figure's point is that the tunnel overrides the IP destination)")
    counts = {sw: (sum(e["table"] == "MyIngress.ipv4_lpm" for e in es),
                   sum(e["table"] == "MyIngress.myTunnel_exact" for e in es))
              for sw, es in topo["runtimes"].items()}
    hit = exact_port(topo["runtimes"]["s1"], "MyIngress.myTunnel_exact", "hdr.myTunnel.dst_id",
                     B3_DST_ID)
    if hit is None or int(hit["action_params"]["port"]) != tun_path[1][1]:
        die(f"basic_tunnel: s1's dst_id {B3_DST_ID} entry is not the one the drawn path takes")
    return {"tun": tun, "ipv4": ipv4, "fields": fields, "todo": todo, "topo": topo,
            "ip_path": ip_path, "tun_path": tun_path, "ip_dst": ip_dst, "counts": counts,
            "ex": ex, "lpm": lpm, "tfwd": tfwd, "fwd": fwd, "anchors": sol.anchors + sk.anchors}


# ------------------------------------------------------------------ drawing helpers
def box(ax, x, y, w, h, fill=WHITE, edge=INK, lw=1.2, ls="solid", r=0.06, z=2):
    ax.add_patch(FancyBboxPatch((x + r, y + r), w - 2 * r, h - 2 * r,
                                boxstyle=f"round,pad={r},rounding_size={r}", facecolor=fill,
                                edgecolor=edge, linewidth=lw, linestyle=ls, zorder=z))


def txt(ax, x, y, s, size=13, color=INK, weight="normal", ha="center", va="center",
        mono=False, z=6, bg=None):
    kw = {}
    if bg:
        kw["bbox"] = dict(boxstyle="square,pad=0.08", facecolor=bg, edgecolor="none")
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, zorder=z,
            family="monospace" if mono else None, linespacing=1.3, **kw)


def arrow(ax, x0, y0, x1, y1, color=INK, lw=1.4, ls="solid", z=3, ms=13):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=ms,
                                 color=color, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0, zorder=z))


def todo_box(ax, x, y, w, h, fill=WHITE, z=2):
    """A part the skeleton leaves as TODO: thick accent outline and a TODO tag on the corner."""
    box(ax, x, y, w, h, fill=fill, edge=ACCENT, lw=2.4, z=z)
    tag(ax, x + w - 0.08, y - 0.02, z=z + 5)


def tag(ax, xr, y, z=8):
    tw, th = 0.56, 0.24
    ax.add_patch(FancyBboxPatch((xr - tw + 0.03, y - th / 2 + 0.03), tw - 0.06, th - 0.06,
                                boxstyle="round,pad=0.03,rounding_size=0.05", facecolor=ACCENT,
                                edgecolor=ACCENT, lw=1, zorder=z))
    txt(ax, xr - tw / 2, y, "TODO", size=9.5, color=WHITE, weight="bold", z=z + 1)


def canvas(title):
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    txt(ax, 0.45, 0.48, title, size=22, weight="bold", ha="left")
    txt(ax, 12.88, 0.50, f"READ · p4lang/tutorials {PIN}", size=11, weight="bold",
        color=FAINT, ha="right")
    return fig, ax


def draw_topology(ax, topo, pos, paths, port_marks):
    """Links from the topology file; each path in `paths` is (hops, colour, linestyle, width)."""
    on = {}
    for hops, col, ls, lw in paths:
        nodes = [n for n, _ in hops]
        for a, b in zip(nodes, nodes[1:]):
            on[frozenset((a, b))] = (col, ls, lw)
    for a, b in topo["links"]:
        na, nb = a.split("-p")[0], b.split("-p")[0]
        col, ls, lw = on.get(frozenset((na, nb)), (RULE, "solid", 1.6))
        (x0, y0), (x1, y1) = pos[na], pos[nb]
        ax.plot([x0, x1], [y0, y1], color=col, lw=lw, ls=ls, zorder=1, solid_capstyle="round")
    for n, (x, y) in pos.items():
        sw = n in topo["switches"]
        w, h = (0.72, 0.42) if sw else (0.60, 0.36)
        box(ax, x - w / 2, y - h / 2, w, h, fill=WHITE if sw else PANEL, edge=INK if sw else MUTED,
            lw=1.3 if sw else 1.0, r=0.05, z=4)
        txt(ax, x, y, n, size=12 if sw else 11, weight="bold" if sw else "normal",
            color=INK if sw else BODY, z=7)
    for sw, port, col in port_marks:            # the port each switch on a path sends to
        nb = topo["ports"][(sw, port)]
        nb_name = nb if isinstance(nb, str) else nb[0]
        (x0, y0), (x1, y1) = pos[sw], pos[nb_name]
        f = 0.5 if isinstance(nb, str) else 0.30
        dx, dy = x1 - x0, y1 - y0
        n = (dx * dx + dy * dy) ** 0.5
        px, py = -dy / n, dx / n                      # a unit normal ...
        if py > 0 or (abs(py) < 1e-9 and px < 0):     # ... pointing up (or right on a vertical)
            px, py = -px, -py
        ha = "left" if px > 0.5 else "right" if px < -0.5 else "center"
        txt(ax, x0 + dx * f + px * 0.14, y0 + dy * f + py * 0.14, f"port {port}", size=10,
            color=col, weight="bold", z=8, ha=ha)


# ------------------------------------------------------------------ B2
def fig_b2(F):
    fig, ax = canvas("basic: one packet through the program")
    y0, h0 = 1.00, 2.35
    # parser
    todo_box(ax, 0.45, y0, 2.25, h0)
    txt(ax, 1.575, y0 + 0.32, "MyParser", size=14, weight="bold")
    box(ax, 0.70, y0 + 0.66, 1.30, 0.40, fill=PANEL, edge=MUTED, lw=1.0, r=0.05, z=4)
    txt(ax, 1.35, y0 + 0.86, "ethernet", size=12, mono=True, z=7)
    arrow(ax, 1.35, y0 + 1.08, 1.35, y0 + 1.62, color=INK)
    txt(ax, 1.46, y0 + 1.35, f"etherType\n{F['ipv4']:#05x}", size=10.5, color=MUTED, ha="left")
    box(ax, 0.70, y0 + 1.64, 1.30, 0.40, fill=PANEL, edge=MUTED, lw=1.0, r=0.05, z=4)
    txt(ax, 1.35, y0 + 1.84, "ipv4", size=12, mono=True, z=7)
    arrow(ax, 2.72, y0 + h0 / 2, 2.98, y0 + h0 / 2)
    # ingress
    box(ax, 3.00, y0, 6.35, h0, fill=PANEL, edge=RULE, lw=1.0, r=0.08, z=1)
    txt(ax, 3.18, y0 + 0.30, "MyIngress", size=14, weight="bold", ha="left")
    todo_box(ax, 4.95, y0 + 0.12, 4.15, 0.38, fill=WHITE, z=3)
    txt(ax, 5.10, y0 + 0.31, "apply: if ipv4 is valid → ipv4_lpm", size=11, ha="left",
        color=BODY)
    lpm = F["lpm"]
    kf, kk = lpm["keys"][0]
    box(ax, 3.20, y0 + 0.72, 2.55, 1.45, z=3)
    txt(ax, 4.475, y0 + 0.98, "ipv4_lpm", size=13.5, weight="bold", mono=True)
    txt(ax, 4.475, y0 + 1.36, f"key  {kf}", size=10.5, mono=True, color=BODY)
    txt(ax, 4.475, y0 + 1.64, f"match  {kk}", size=10.5, mono=True, color=BODY)
    txt(ax, 4.475, y0 + 1.92, f"miss  {lpm['default']}", size=10.5, mono=True, color=BODY)
    arrow(ax, 5.77, y0 + 1.45, 6.10, y0 + 1.45)
    txt(ax, 5.935, y0 + 1.30, "hit", size=10, color=MUTED)
    fwd = F["fwd"]
    todo_box(ax, 6.12, y0 + 0.72, 3.03, 1.45, z=3)
    txt(ax, 7.635, y0 + 0.96, f"ipv4_forward({', '.join(fwd['params'])})", size=11.5,
        weight="bold", mono=True)
    for i, (_, label) in enumerate(FWD):
        txt(ax, 6.35, y0 + 1.27 + i * 0.25, label, size=11, ha="left", color=BODY)
    arrow(ax, 9.37, y0 + h0 / 2, 9.63, y0 + h0 / 2)
    # checksum (given)
    box(ax, 9.65, y0, 1.45, h0)
    txt(ax, 10.375, y0 + 0.62, "MyCompute\nChecksum", size=12.5, weight="bold")
    txt(ax, 10.375, y0 + 1.45, "IPv4 header\nchecksum", size=11, color=MUTED)
    arrow(ax, 11.12, y0 + h0 / 2, 11.38, y0 + h0 / 2)
    # deparser
    todo_box(ax, 11.40, y0, 1.50, h0)
    txt(ax, 12.15, y0 + 0.40, "MyDeparser", size=12.5, weight="bold")
    txt(ax, 12.15, y0 + 0.86, "emit", size=11, color=MUTED)
    txt(ax, 12.15, y0 + 1.22, "ethernet", size=11.5, mono=True)
    txt(ax, 12.15, y0 + 1.52, "ipv4", size=11.5, mono=True)

    # topology, with the packet's path
    topo, path = F["topo"], F["path"]
    txt(ax, 0.45, 3.86, f"{topo['rel']}  ·  {B2_SRC} → {F['dst_ip']}", size=11,
        weight="bold", color=FAINT, ha="left")
    marks = [(n, p, ACCENT) for n, p in path if p is not None]
    draw_topology(ax, topo, B2_POS, [(path, ACCENT, "solid", 3.2)], marks)
    for hname in (B2_SRC, B2_DST):
        x, y = B2_POS[hname]
        txt(ax, x, y + 0.36, topo["hosts"][hname]["ip"].split("/")[0], size=10, mono=True,
            color=ACCENT)

    # s1's entries, as its runtime file writes them
    x0 = 6.85
    rj = topo["switches"]["s1"]["runtime_json"]
    txt(ax, x0, 3.86, f"{rj}  ·  installed at start", size=11, weight="bold", color=FAINT,
        ha="left")
    cols = [(x0 + 0.10, kf), (x0 + 1.95, "action"), (x0 + 3.55, fwd["params"][0]),
            (x0 + 5.55, fwd["params"][1])]
    for i, (cx, head) in enumerate(cols):
        txt(ax, cx, 4.28, head, size=10.5, weight="bold", color=MUTED, mono=True,
            ha="right" if i == 3 else "left")
    ax.plot([x0, 12.9], [4.46, 4.46], color=RULE, lw=1.0, zorder=2)
    hit_port = path[1][1]
    rows = []
    for e in topo["runtimes"]["s1"]:
        a = e["action_name"].split(".")[-1]
        if e.get("default_action"):
            rows.append(("default", a, "", "", False))
        else:
            addr, plen = e["match"][kf]
            p = e["action_params"]
            rows.append((f"{addr}/{plen}", a, p[fwd["params"][0]], str(p[fwd["params"][1]]),
                         int(p[fwd["params"][1]]) == hit_port and addr == F["dst_ip"]))
    rows.sort(key=lambda r: (r[0] == "default", r[0]))
    for i, (m, a, mac, port, hit) in enumerate(rows):
        yy = 4.72 + i * 0.36
        if hit:
            ax.add_patch(Rectangle((x0, yy - 0.17), 12.9 - x0, 0.34, facecolor=ACCENT_BG,
                                   edgecolor="none", zorder=1))
        c = ACCENT if hit else BODY
        txt(ax, cols[0][0], yy, m, size=11, mono=True, color=c, ha="left")
        txt(ax, cols[1][0], yy, a, size=11, mono=True, color=c, ha="left")
        txt(ax, cols[2][0], yy, mac, size=11, mono=True, color=c, ha="left")
        txt(ax, cols[3][0], yy, port, size=11, mono=True, color=c, ha="right")

    # legend
    ly = 6.62
    tag(ax, x0 + 0.56, ly)
    txt(ax, x0 + 0.68, ly, "you write it: the skeleton leaves a TODO", size=11, ha="left", color=BODY)
    txt(ax, 12.9, ly, "skeleton: drops every packet", size=11, ha="right", color=BODY)
    return fig


# ------------------------------------------------------------------ B3
def fig_b3(F):
    fig, ax = canvas("basic_tunnel: its own header, its own table")
    tunx = f"{F['tun']:#06x}"
    ipx = f"{F['ipv4']:#05x}"
    # packet formats
    def seg(x, y, w, label, sub=None, fill=WHITE, edge=MUTED, bold=False):
        box(ax, x, y, w, 0.50, fill=fill, edge=edge, lw=1.1, r=0.03, z=3)
        if sub:
            txt(ax, x + w / 2, y + 0.17, label, size=11, mono=True, weight="bold" if bold else "normal")
            txt(ax, x + w / 2, y + 0.37, sub, size=9.5, color=MUTED)
        else:
            txt(ax, x + w / 2, y + 0.25, label, size=11, mono=True)
    ya, yb, xs = 1.00, 1.72, 1.55
    txt(ax, 0.45, ya + 0.25, "IPv4", size=11.5, weight="bold", color=MUTED, ha="left")
    seg(xs, ya, 1.55, "ethernet", f"etherType {ipx}")
    seg(xs + 1.55, ya, 0.95, "ipv4")
    seg(xs + 2.50, ya, 1.45, "tcp · msg")
    txt(ax, 0.45, yb + 0.25, "tunnelled", size=11.5, weight="bold", color=ACCENT, ha="left")
    seg(xs, yb, 1.55, "ethernet", f"etherType {tunx}")
    (b1, f1), (b2, f2) = F["fields"]
    seg(xs + 1.55, yb, 1.05, f1, f"{b1} bit", fill=ACCENT_BG, edge=ACCENT, bold=True)
    seg(xs + 2.60, yb, 1.05, f2, f"{b2} bit", fill=ACCENT_BG, edge=ACCENT, bold=True)
    seg(xs + 3.65, yb, 0.95, "ipv4")
    seg(xs + 4.60, yb, 1.45, "tcp · msg")
    txt(ax, xs + 2.10, yb + 0.66, "myTunnel_t", size=10.5, mono=True, color=ACCENT, weight="bold")

    # parser
    px, pw = 8.10, 4.80
    todo_box(ax, px, 0.92, pw, 1.55)
    txt(ax, px + 0.15, 1.13, "MyParser", size=12.5, weight="bold", ha="left")
    def st(x, y, name, w=1.25):
        box(ax, x, y, w, 0.38, fill=PANEL, edge=MUTED, lw=1.0, r=0.05, z=4)
        txt(ax, x + w / 2, y + 0.19, name, size=11, mono=True, z=7)
    sy = 1.48
    st(px + 0.20, sy, "ethernet", w=1.15)
    st(px + 1.90, sy, "myTunnel", w=1.20)
    st(px + 3.65, sy, "ipv4", w=0.95)
    arrow(ax, px + 1.37, sy + 0.19, px + 1.88, sy + 0.19, color=ACCENT)
    txt(ax, px + 1.625, sy - 0.14, tunx, size=10, color=ACCENT, weight="bold")
    arrow(ax, px + 3.12, sy + 0.19, px + 3.63, sy + 0.19)
    txt(ax, px + 3.375, sy - 0.14, f"proto_id {ipx}", size=10, color=MUTED)
    ax.add_patch(FancyArrowPatch((px + 0.78, sy + 0.40), (px + 4.12, sy + 0.40),
                                 connectionstyle="arc3,rad=0.22", arrowstyle="-|>", mutation_scale=13,
                                 color=INK, lw=1.4, shrinkA=0, shrinkB=0, zorder=3))
    txt(ax, px + 2.45, sy + 0.84, ipx, size=10, color=MUTED)

    # ingress
    y0 = 2.75
    box(ax, 0.45, y0, 10.55, 1.55, fill=PANEL, edge=RULE, lw=1.0, r=0.08, z=1)
    txt(ax, 0.62, y0 + 0.27, "MyIngress", size=13, weight="bold", ha="left")
    todo_box(ax, 2.35, y0 + 0.10, 1.95, 1.35, z=3)
    txt(ax, 3.325, y0 + 0.30, "apply", size=11.5, weight="bold")
    txt(ax, 3.325, y0 + 0.72, "myTunnel valid", size=10.5, color=ACCENT)
    txt(ax, 3.325, y0 + 1.17, "else: ipv4 valid", size=10.5, color=BODY)
    # tunnel lane
    todo_box(ax, 4.55, y0 + 0.14, 3.05, 0.60, z=3)
    (ekf, ekk), (lkf, lkk) = F["ex"]["keys"][0], F["lpm"]["keys"][0]
    txt(ax, 6.075, y0 + 0.34, "myTunnel_exact", size=12, weight="bold", mono=True)
    txt(ax, 6.075, y0 + 0.58, f"key {ekf} · {ekk}", size=9.5, mono=True, color=BODY)
    todo_box(ax, 7.85, y0 + 0.14, 2.95, 0.60, z=3)
    txt(ax, 9.325, y0 + 0.34, f"myTunnel_forward({', '.join(F['tfwd']['params'])})", size=11,
        weight="bold", mono=True)
    txt(ax, 9.325, y0 + 0.58, TUN_FWD[0][1], size=10.5, color=BODY)
    arrow(ax, 4.32, y0 + 0.44, 4.53, y0 + 0.44, color=ACCENT)
    arrow(ax, 7.62, y0 + 0.44, 7.83, y0 + 0.44)
    # ipv4 lane (given: basic's)
    box(ax, 4.55, y0 + 0.86, 3.05, 0.60, z=3)
    txt(ax, 6.075, y0 + 1.06, "ipv4_lpm", size=12, weight="bold", mono=True)
    txt(ax, 6.075, y0 + 1.30, f"key {lkf} · {lkk}", size=9.5, mono=True, color=BODY)
    box(ax, 7.85, y0 + 0.86, 2.95, 0.60, z=3)
    txt(ax, 9.325, y0 + 1.06, f"ipv4_forward({', '.join(F['fwd']['params'])})", size=10.5,
        weight="bold", mono=True)
    txt(ax, 9.325, y0 + 1.30, "as in basic", size=10.5, color=MUTED)
    arrow(ax, 4.32, y0 + 1.16, 4.53, y0 + 1.16)
    arrow(ax, 7.62, y0 + 1.16, 7.83, y0 + 1.16)
    arrow(ax, 11.02, y0 + 0.78, 11.28, y0 + 0.78)
    # deparser
    todo_box(ax, 11.30, y0, 1.60, 1.55)
    txt(ax, 12.10, y0 + 0.30, "MyDeparser", size=12, weight="bold")
    txt(ax, 12.10, y0 + 0.62, "emit", size=10.5, color=MUTED)
    txt(ax, 12.10, y0 + 0.92, "ethernet\nmyTunnel\nipv4", size=10.5, mono=True, va="top")

    # topology: one packet to h3's address, with and without the tunnel header
    topo = F["topo"]
    ipp, tnp = F["ip_path"], F["tun_path"]
    txt(ax, 0.45, 4.62, f"{topo['rel']}  ·  {B3_SRC} sends to {F['ip_dst']}", size=11,
        weight="bold", color=FAINT, ha="left")
    marks = [(n, p, ACCENT) for n, p in tnp if p is not None] + \
            [(n, p, MUTED) for n, p in ipp if p is not None and (n, p) not in tnp]
    draw_topology(ax, topo, B3_POS, [(ipp, MUTED, (0, (4, 3)), 2.4), (tnp, ACCENT, "solid", 3.2)],
                  marks)
    xa, ya_ = B3_POS[tnp[-1][0]]
    txt(ax, xa, ya_ + 0.40, f"dst_id {B3_DST_ID}", size=10.5, color=ACCENT, weight="bold")
    xb, yb_ = B3_POS[ipp[-1][0]]
    txt(ax, xb + 0.38, yb_, f"{F['ip_dst']}\nno tunnel", size=10.5, color=MUTED, ha="left")

    # s1's tunnel entries
    x0 = 7.10
    rj = topo["switches"]["s1"]["runtime_json"]
    txt(ax, x0, 4.62, f"{rj}  ·  installed at start", size=11, weight="bold", color=FAINT,
        ha="left")
    for cx, head, ha in ((x0 + 0.10, "myTunnel_exact: dst_id", "left"),
                         (x0 + 3.10, "action", "left"), (12.8, "port", "right")):
        txt(ax, cx, 5.00, head, size=10.5, weight="bold", color=MUTED, mono=True, ha=ha)
    ax.plot([x0, 12.9], [5.17, 5.17], color=RULE, lw=1.0, zorder=2)
    ents = [e for e in topo["runtimes"]["s1"] if e["table"] == "MyIngress.myTunnel_exact"]
    ents.sort(key=lambda e: e["match"]["hdr.myTunnel.dst_id"][0])
    for i, e in enumerate(ents):
        yy = 5.40 + i * 0.32
        dst = e["match"]["hdr.myTunnel.dst_id"][0]
        hit = dst == B3_DST_ID
        if hit:
            ax.add_patch(Rectangle((x0, yy - 0.15), 12.9 - x0, 0.30, facecolor=ACCENT_BG,
                                   edgecolor="none", zorder=1))
        c = ACCENT if hit else BODY
        txt(ax, x0 + 0.10, yy, str(dst), size=11, mono=True, color=c, ha="left")
        txt(ax, x0 + 3.10, yy, e["action_name"].split(".")[-1], size=11, mono=True, color=c, ha="left")
        txt(ax, 12.8, yy, str(e["action_params"]["port"]), size=11, mono=True, color=c, ha="right")
    lp, ex = F["counts"]["s1"]
    txt(ax, x0 + 0.10, 5.40 + len(ents) * 0.32, f"+ {lp} ipv4_lpm entries", size=10.5, color=MUTED,
        ha="left")
    ly = 6.66
    tag(ax, x0 + 0.56, ly)
    txt(ax, x0 + 0.68, ly, "you write it: the skeleton leaves a TODO", size=11, ha="left", color=BODY)
    return fig


def save(fig, stem):
    os.makedirs(HIRES, exist_ok=True)
    for ext in ("pdf", "png", "svg"):
        kw = {"dpi": 300} if ext == "png" else {}
        fig.savefig(os.path.join(OUTDIR, f"{stem}.{ext}"), facecolor=WHITE, **kw)
    fig.savefig(os.path.join(HIRES, f"{stem}.png"), facecolor=WHITE, dpi=500)
    plt.close(fig)
    print(f"[out] {stem}")


def main():
    sha = check_pin()
    print(f"[tutorials] {TUT} @ {PIN} = {sha}")
    B = basic_facts()
    for what, where in B["anchors"]:
        print(f"[anchor] {where}  {what}")
    print(f"[basic] path {B['path']}; TODO {B['todo']}")
    T = tunnel_facts()
    for what, where in T["anchors"]:
        print(f"[anchor] {where}  {what}")
    print(f"[basic_tunnel] etherType {T['tun']:#06x}; fields {T['fields']}; IPv4 path {T['ip_path']}; "
          f"dst_id {B3_DST_ID} path {T['tun_path']}; entries per switch (lpm, exact) {T['counts']}; "
          f"TODO {T['todo']}")
    save(fig_b2(B), "fig_b2_basic_walkthrough")
    save(fig_b3(T), "fig_b3_basic_tunnel")
    return 0


if __name__ == "__main__":
    sys.exit(main())
