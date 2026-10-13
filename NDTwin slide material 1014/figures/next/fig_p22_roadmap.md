# `fig_p22_roadmap` -- What we fix first, and what we disclose (page P22)

[Co-developed with claude code -- Adam]

Evidence class: **INFERRED (a plan)**. The ordering is derived from the ranked problems of P19-P21; the
costs are rough estimates (INFERRED in problems.tsv), the columns are horizons, not dates. Nothing here is
a commitment and nothing on it was run.

## Data source

- `figures_spec/problems.tsv` sha256 `ed186237a1a9b79b...` (19 ranked problems; evidence paths are @3a47bdb7 and
  are in the file, not on the canvas).
- `figures_spec/roadmap.txt` sha256 `aa4e42e647d8d03d...`: lanes, the rank -> lane/column placement with the
  fix text, DISCLOSE, and the arrows are all read from it at run time; box fill = persona hurt most = the
  first persona named in `hurts`; shape as second encoding: round corner = control-app developer, square =
  P4-program developer, diamond tab = network operator.
- Column rule, checked against each rank's cost in problems.tsv: NOW if every part is under about a week; NEXT if
  any part is about a week or more (up to 6 weeks); LATER if it needs a design decision first; DISCLOSE if
  fixable = no.
- Arrows (only these, from roadmap.txt): #2 -> #13; #1 -> #11; #8 -> #14; #3 -> #9.
- Box labels are the roadmap.txt fix texts with the cost parentheticals removed (costs live in the notes).
  Within a cell the boxes keep the spec order except that an arrow's source sits at the end of its row and its
  target at the start (so the route crosses no box); the generator searches the orderings.

## Placement actually drawn

| # | problem | hurts (first = fill) | column | lane | label on the figure | fixable | cost |
|---|---|---|---|---|---|---|---|
| 1 | Own .p4 only via a lab CLI tied to one machine | P4 dev | NEXT | Run it anywhere | User-level own-program command, install-time config, clean-VM CI | yes | about 1-2 weeks (INFERRED) |
| 2 | Writes report success that did not happen | app dev; P4 dev; operator (intent path) | NOW | Trust what the API says | Honest write results (non-2xx + wait mode) | yes | 3-5 days + one live gate (INFERRED) |
| 3 | Zero means idle or blind; slow flows vanish | app dev; operator (energy app reads usage) | NOW | See failures and load in time | Null when telemetry is silent; window parameter | yes | 2-3 days kernel + 1-2 days consumers (INFERRED) |
| 4 | P4 rule changes since bring-up are lost on proxy restart: routing writes journaled but not replayed, table_entry writes not journaled | P4 dev; app dev | NEXT | Trust what the API says | Journal + cookie-checked replay; routing replay; boot_id | yes | about 2-3 weeks in all: table_entry journal + cookie-gated replay 1-2 weeks; routing replay 2-3 days; kernel boot_id 2-3 days (INFERRED, estimated 2026-10-12 from trunk 3a47bdb7) |
| 5 | Power cycle cuts hosts while checks stay green | operator | NOW | Trust what the API says | Power cycle keeps port numbers (+ energy app lease) | yes | 1-2 days kernel + 1-2 days app (INFERRED) |
| 6 | Rule view lags and can show rejected rules | app dev | NOW | Trust what the API says | Fresh read-back, ghost filter on OVS | yes | 2-4 days (INFERRED) |
| 7 | Recording stops silently | operator | NOW | See failures and load in time | Recorder reconnects | yes | 1-2 days (INFERRED) |
| 8 | Topology must be declared; OVS copy is fixed | operator; app dev | NEXT | Model more of the network | OVS fabric from the model; undeclared switches; 64-switch run | yes | builder 2-3 days; discovery about 1 week; scale 1-2 lab nights; about 1.5-2 weeks in all (INFERRED) |
| 9 | What-if is narrow, no prediction-vs-measured run on record | operator; app dev | NEXT | Model more of the network | Link-removal what-if + one prediction-vs-measured run | yes | link input 2-3 days; validation 1-2 lab nights; NFS removal about 1 week (INFERRED) |
| 10 | P4 plane lacks ECMP and meters; five proxy routes missing | P4 dev; app dev | NEXT | Model more of the network | ECMP selector, table size, missing proxy routes | yes | about 2-3 weeks in all: selector 1-2 weeks; size 1 day; routes about 1 week after the scoping run (INFERRED, estimated 2026-10-12) |
| 11 | Built on an unmaintained controller | app dev; operator | NEXT | Run it anywhere | Ryu -> os-ken | yes | about 1 week + live gates (INFERRED) |
| 12 | Link and flow rates are 1/256 sampled estimates; exact counters are skipped or not exposed as rates | app dev; operator (energy app reads usage) | NOW | See failures and load in time | Counter-based link rates under Mininet | yes | 2-3 days OVS + 2-3 days P4 emitter (option A, INFERRED) |
| 13 | Failures reach apps only by polling | app dev | NEXT | See failures and load in time | Event stream (SSE) + LLDP interval sweep | yes | SSE about 1 week; sweep 1 lab night (INFERRED) |
| 14 | Mirroring a network means NDTwin must control it | operator | LATER | Model more of the network | Observer mode for an existing controller | yes | 3-6 weeks; needs a design decision (INFERRED) |
| 15 | API open to the network, no auth | operator | NOW | Trust what the API says | Local-only bind + token | yes | 1-2 days + client token updates (INFERRED) |
| 16 | Any app can release another app's lock | app dev | NOW | Trust what the API says | Lock owner check | yes | about 2 days (INFERRED) |
| 17 | Intent translator bound to one cloud LLM, no run on record | operator | NOW | Run it anywhere | Configurable LLM endpoint | yes | 1-2 days + an API key (INFERRED) |
| 18 | Physical switch path coded, no run on record | operator; app dev | DISCLOSE | no lane | Physical switches: coded, no run on record (no testbed) | no (hardware unavailable) | disclosure < 1 day; the run itself waits for hardware |
| 19 | No P4 hardware target; bmv2 packet-rate ceiling | P4 dev | DISCLOSE | no lane | No P4 hardware target; bmv2 ceiling in pps | no (target discontinued) | study months (INFERRED) |

## Checks the generator makes

Every rank 1-19 in problems.tsv exactly once and drawn exactly once; no fixable=no row in a fix lane; no
fixable=yes row in DISCLOSE; every rank's column equals the column rule on its cost; every arrow endpoint drawn
and a non-crossing route found.

## Regenerate

```bash
cd generator   # from the deck folder
"${NDTWIN_PLOTVENV:-../../NDTwin Slide material 820/.plotvenv/bin/python3}" make_p22_roadmap.py
```

Last produced: 2026-10-12T06:20:06Z (UTC); matplotlib 3.11.1; generator `make_p22_roadmap.py` sha256 `0287b0e0d89a615b...`, shared style `figstyle_1014.py` sha256 `be4a908ad5c4fbab...`.

[Co-developed with claude code -- Adam]
