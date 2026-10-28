# fig_p09_next -- What comes next

Page P09 of the 1028 deck. Evidence class: INFERRED (a plan; no dates). Spec: figures_spec/next.txt. Generator:
generator/make_p09_next.py with generator/figstyle_1028.py. It reads the template's P07 and P08 tables and
stops if a next step there has no box here.

## Boxes

| id | lane | column | label | from | stated in |
|---|---|---|---|---|---|
| B1 | Fresh machine | NOW | Traffic-generator path | P07 row 1 | P07 row 1 next step "fix, with tests" (Adam's brief: "(1) and (2) are being fixed with tests"). |
| B2 | Fresh machine | NOW | Log directory owner | P07 row 2 | P07 row 2 next step "fix, with tests" (Adam's brief). |
| B3 | API doc | NOW | Re-adopt needs a restarted switch | P07 row 3 | P07 row 3 next step "API doc: needs a restarted switch" (Adam's brief: "(3) is a doc fix"). |
| B4 | API doc | NOW | Register and counter routes, limits | P08 row 1 | P08 row 1 next step "add them, with limits, to the API doc" (proposal, template §3 item 3). |
| B5 | API doc | NOW | /24 against a host's /32 | P08 row 2 | P08 row 2 next step "say so in the API doc" (proposal, template §3 item 3). |
| B6 | Decide | NEXT | Kernel pre-check of prefix forms | P08 row 3 | P08 row 3 next step "decide: kernel pre-check refuses these forms" (proposal, template §3 item 3). |
| B7 | Decide | NEXT | Flag a stale 0 at proxy start | P08 row 4 | P08 row 4 next step "decide: flag it at proxy start" (proposal, template §3 item 3). |
| B8 | Apps | NEXT | An app that resends on the notice | P08 row 5 | P08 row 5 next step "an app that resends on it" (proposal, template §3 item 3). |

## Regenerate

```bash
cd generator   # from the deck folder
"${NDTWIN_PLOTVENV:-../../NDTwin Slide material 820/.plotvenv/bin/python3}" make_p09_next.py
```

Last produced: 2026-10-27T15:06:52Z (UTC); matplotlib 3.11.1; generator `make_p09_next.py` sha256 `979a55c67a742b46...`, shared style `figstyle_1028.py` sha256 `67385b0eb73c39b9...`.

[Co-developed with claude code -- Adam]
