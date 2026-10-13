# `fig_p18_health` -- P4 health check: 57 cells, offline only (page P18)

[Co-developed with claude code -- Adam]

Two panels, two evidence classes, never mixed.

- Left, **READ**: the cells the health check decides, one box per P4 feature dimension with its cell count, read
  from `tools/p4_health/cells/table.py@3a47bdb7` (CELLS: 57 cells, 22 dimensions). The generator re-reads that file with
  `git show 3a47bdb7:tools/p4_health/cells/table.py` on every run and stops if the spec differs. No box is highlighted.
- Right, **RAN, offline only**: the S0 static stage, cells T4-T7 and the table-writer comparison (52 shape cases), observed on throwaway bmv2 switches (stock
  and fast), not on the NDTwin fabric and not against a live lab. Commits and binary identity are in the P19
  speaker notes of the template (T4-T7 and the writer comparison: bmv2 binaries identified by install path only, no hash).
- No prediction is drawn (`doc/audit/2026-10-03_p4-health-check/expected_today.tsv` is not read).

## Data source

- `figures_spec/p4_health.tsv` sha256 `25dc2b8d4187ff67...`.

## Regenerate

```bash
cd generator   # from the deck folder
"${NDTWIN_PLOTVENV:-../../NDTwin Slide material 820/.plotvenv/bin/python3}" make_p18_health.py
```

Last produced: 2026-10-12T06:20:49Z (UTC); matplotlib 3.11.1; generator `make_p18_health.py` sha256 `ba6a72a99135c6a4...`, shared style `figstyle_1014.py` sha256 `be4a908ad5c4fbab...`.

[Co-developed with claude code -- Adam]
