# `_hires/` — the same six figures, rasterised from their generated PDFs

`fig1`–`fig6` in `..` ship as PDF + PNG (300 dpi) + SVG, all three written by the
same `matplotlib` call in `../make_overnight_figs.py` — one vector source, so no
number can drift between formats.

These six are `pdftoppm -r 500` of the **PDF beside each PNG** in `..` — the same
vector source again, just rasterised higher for a projector or a print. No re-plot.

Regenerate all six:

    cd "../"  # NDTWIN slide material 916/figures/overnight-0904/
    for f in fig1_declared_vs_real_link_failure fig2_shutdown_southbound_writes \
             fig3_dispatch_counters_vs_switch_truth fig4_group_install_delete_readback \
             fig5_path_switch_count_static fig6_endpoint_latency_profile; do
      pdftoppm -r 500 -png -singlefile "${f}.pdf" "_hires/${f}"
    done

If `..`'s PDFs have changed since these were made (re-run `make_overnight_figs.py`
first if so), re-run the loop above — it always overwrites in place.

[Co-developed with claude code -- Adam]
