# `_hires/` — the same four figures, rasterised from their committed PDFs

`fig5`–`fig8` ship as both PNG (≈890 px wide) and PDF in
`doc/2026-08-29_bmv2-performance-study-figs/`. At slide width the PNG is about
80–100 dpi, which is visibly soft on a projector.

These four are `pdftoppm -r 500` of the **PDF beside that PNG** — the same
vector source, no re-plot, so no number can drift. Verified before rasterising:
each repo PNG's sha256 equals the copy in `../`, including `fig7`
(`f7aeeede…`, the 09-01 UDP-qualified re-render) — so the PDFs are the same
generation as the deployed PNGs, not a stale batch.

`fig1`–`fig4` have no PDF beside them and are used at their natural size.

Regenerate:

    cd doc/2026-08-29_bmv2-performance-study-figs
    pdftoppm -r 500 -png -singlefile fig5_reporting_matrix.pdf <outdir>/fig5_reporting_matrix

[Co-developed with claude code -- Adam]
