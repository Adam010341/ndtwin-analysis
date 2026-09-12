# ndtwin-analysis

Measurement tooling, figure generators, and progress-report material for **NDTwin** — a network
digital-twin kernel with a P4/bmv2 data plane. The kernel itself lives in
[NDTwin-Kernel-P4](https://github.com/Adam010341/NDTwin-Kernel-P4); this repository holds the
things built *around* it to find out what it actually does, and to say so on a slide.

## About

Two halves, and the seam between them is the point of the repository.

| | |
|---|---|
| **`analysis/`** | The tools. Measurement drivers that ran the experiments, parsers and analysers that reduced the output, and the matplotlib scripts that rendered every figure in the decks. 10 measurement rounds, plus the literature-survey figure family and three kernel-side instruments. |
| **`NDTwin … slide material <MMDD>/`** | The reports. Four progress reports (820, 827, 903, 916): the slide template that is each one's single source of truth, the decks, the figures, and the deck generators. |

The organising rule is that **a number on a slide has to trace back to the run that produced
it.** So the plotting scripts do not transcribe values out of reports — they re-open the
archived measurement data and recompute what they draw. Several of them import their loaders
and palettes from a sibling round's script rather than restating them, so two figures standing
next to each other on a slide cannot drift apart. Where a parse is used instead of a
recomputation, the parse asserts its own yield, because a regex that silently matches nothing
renders a confident empty figure.

Three consequences worth knowing before reading anything here:

- **A figure can be right and still be unreadable.** Several scripts carry a long header
  explaining what the figure must *not* be allowed to say —
  [`plot_2x2.py`](analysis/rounds/2026-08-31_sampling-ceiling-after-merge/plot_2x2.py) refuses to
  draw its four arms on one axis because two of them ran 3.3 hours apart, and a tidy 2×2 grid
  would visually assert a comparability the data does not have.
- **Figures go stale silently.** A figure stamped "no arm has run yet" was true when rendered
  and false an hour later, and the PNG keeps rendering fine either way. That is why
  `plot_deck_903_round2.py` exists beside `plot_deck_903.py` instead of editing it.
- **Not every figure is a measurement.** The `fig4`–`fig8` family encodes a hand-coded census of
  34 published papers that measure bmv2; those are citations, not runs, and each row names its
  source. The measurement figures and the survey figures are never mixed on one axis.

## `analysis/rounds/` — the ten measurement rounds

Each directory holds that round's drivers (`*.sh`), analysers (`*.py`), figure script
(`plot_*.py`), the reduced aggregate outputs where the round produced them (`*.out`), and the
report and pre-registration documents
that state what the round was entitled to conclude.

| Round | The question | Figure script |
|---|---|---|
| `2026-08-19_p4-sflow-accuracy` | Is the ladder jitter abnormal, and does it shrink under load? | `plot_figures.py` |
| `2026-08-20_sampling-rate-and-cpu` | What does sampling cost, and where does the CPU actually go? | `plot_figures.py`, `plot_ladder_rates.py` |
| `2026-08-21_ovs-failover-after-fix` | After the fix, does the OVS scaling penalty survive? | `plot_after_fix.py` |
| `2026-08-21_ryu-topology-scaling` | Does Ryu's topology query explain the 128-host failover penalty? (No — it is link-failure detection) | `plot_budget.py` |
| `2026-08-25_sampling-rounds` | Three independent tickets: thread attribution, ladder extension, λ collapse | `plot_deck_827.py` |
| `2026-08-27_hardcoded-denominator` | Ticket Q: a hard-coded denominator, and what it did to the rates | `plot_deck_903.py`, `plot_q_by_flowcount.py` |
| `2026-08-28_QM-mirrored-block` | Six-arm mirrored block `base Q M M Q base`, so time cannot alias the treatment | `plot_deck_903_round2.py` |
| `2026-08-31_sampling-ceiling-after-merge` | Did the telemetry ceiling rise after batching and 1 kHz→1 Hz? (Not readable — 0 of 72 cells saturated) | `plot_2x2.py`, `plot_page_ceiling.py` |
| `2026-09-01_cpu-matrix-1hz` | The CPU matrix, reweighed once under the 1 Hz path | `plot_compare.py` |
| `2026-09-02_recompute-paired-ab` | Paired A/B: was that step caused by that one constant? | `plot_ab.py` |

## `analysis/study-figs/` — the bmv2 performance-study figures

`fig1`–`fig8` of the performance study, and the two scripts that build them:

- **`make_figs.py`** → `fig1` unit ambiguity · `fig2` per-flow monotonicity · `fig3` two build
  working points · `fig4` literature spread.
- **`make_survey_figs.py`** → `fig5`/`fig5b` reporting matrix (`fig5b` covers all 34 coded
  papers) · `fig6` twelve numbers on one axis · `fig7` aggregate across two planes ·
  `fig8` known-but-never-reported.

`README-generators.md` records why the two scripts are split and how `make_figs.py` came to be
version-controlled later than its own figures — the lock on the submission package was aimed at
submission *content*, never at reproducibility, and conflating the two nearly lost the
generators. `fig5b_reporting_matrix_34.md` is the coded census behind the matrix, one row per
paper with its citation.

## `analysis/kernel-tools/` — three kernel-side instruments

- **`twin_audit/`** — the twin lie detector. For every flow the twin reports as alive, go and
  check whether packets are actually moving. Built after a flow was reported "flowing at
  9–15 Mbps" with 287/288 edges up while it had carried zero packets for 291 seconds; every
  dashboard agreed, because they all descend from the same sFlow ingest. `criteria.py` answers
  "are packets moving between these two hosts?" as a **quorum over three channels that fail
  differently**, rather than one source that can be wrong in silence.
- **`make_topology.py`** — generate an OVS model with N hosts, so the all-pairs walk can be
  swept across scales. Two data points (4 hosts and 128) cannot separate a linear cost from a
  quadratic one.
- **`p4_power_helper.py`** — the privileged half of the P4 power strategy: start or stop exactly
  one named bmv2 switch from the manifest, and refuse everything else. It exists so that
  `kill` never has to go into `NOPASSWD`.

## Running the figure scripts

Most take an output directory: `python plot_figures.py <output-dir>`.

**The interpreter is part of the specification.** `make_figs.py`, `make_survey_figs.py` and
`plot_deck_903_round2.py` assert **matplotlib 3.11.x** and exit otherwise. This is not
fastidiousness: a layout defect that these scripts were fixed to avoid does not reproduce at all
on matplotlib 3.10 (it renders as 0 px instead of 11 px), so a "successful" run on the wrong
version proves nothing about the figure you are looking at. `plot_deck_903_round2.py` has an
escape hatch, `DECK_ALLOW_MPL_MISMATCH=1`, whose own error message tells you not to compare the
output against the archived figures afterwards.

The interpreter used for every archived figure is a dedicated venv (Python 3.13.13 +
matplotlib 3.11.1) that is **not in this repository** — `.plotvenv/` is ignored, since it is
rebuildable:

```bash
python3 -m venv .plotvenv && .plotvenv/bin/pip install 'matplotlib==3.11.1'
```

## What is deliberately not here

- **The raw measurement data.** Around 1.1 GB of `raw/` across these ten rounds, which stays in
  the kernel repository under `doc/audit/<round>/raw/` and its `audit-raw` ref. **47 of the 92
  scripts here name a path under `raw/`** — writing it during a run, or reading it back
  afterwards — so a clone of this repository alone will not take a round end-to-end; you need
  the matching round directory in the kernel repo. The `*.out` files that
  *are* here are the reduced aggregate outputs, so the numbers are legible without the archive.
- **Run logs** (`*.log`) — the transcripts of the runs themselves, which belong with the raw
  data rather than with the tools.
- **Session-internal notes** — handoffs, drafts, running notes, and cross-review memos. The
  pre-registrations, reports and findings are here; the scaffolding around them is not.
- **`ladder_ext.out`** — untracked in the kernel repo by commit `e6eec347`, "while it is still
  being written". An unfinished file is not a result.
- **`paper/` and `VENUES-*.md`** — the submission line, ignored here as in the kernel repo.

## Provenance

Everything under `analysis/` was taken verbatim from `NDTwin-Kernel-P4` at commit
**`d6cb0220`**, read out of the commit rather than off a working tree, and checked file by file
against that commit's blobs by sha256.

Exactly one file differs, deliberately: **`analysis/study-figs/make_figs.py` line 2**, a comment
that named a submission venue, is replaced with a neutral description of the script. The
original line is still in the kernel repository's history.

One claim inside the archive has aged: `analysis/rounds/2026-08-28_QM-mirrored-block/FINDINGS.md`
labels `Adam010341/NDTwin-Kernel-P4` as private. That was true on 2026-08-28 and is not true now
— that repository is public. The document is left as written, because an audit record that gets
quietly edited stops being one.

Code co-developed with Claude Code is marked in-file with
`[Co-developed with claude code -- Adam]`. The tools under `analysis/` come from
NDTwin-Kernel-P4, which is licensed Apache-2.0.
