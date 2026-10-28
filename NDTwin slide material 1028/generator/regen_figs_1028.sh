#!/bin/bash
# Regenerate the three figures with the matplotlib venv (3.11.x); figstyle_1028.py stops if matplotlib is not
# 3.11.x, and every companion .md records the version used.
# [Co-developed with claude code -- Adam]
HERE=$(cd "$(dirname "$0")" && pwd) || exit 1
PY="${NDTWIN_PLOTVENV:-$HERE/../../NDTwin Slide material 820/.plotvenv/bin/python3}"
cd "$HERE" || exit 1
"$PY" -c "import matplotlib; print('matplotlib', matplotlib.__version__)" || exit 1
rc=0
for g in make_p04_rules_lost make_p05_read_path make_p09_next; do
  "$PY" $g.py; r=$?; echo "$g rc=$r"; [ $r -ne 0 ] && rc=$r
done
exit $rc
