#!/bin/bash
# Regenerate the six figures with the matplotlib venv (3.11.1); the generators and figstyle_1014.py stop if
# matplotlib is not 3.11.x, and every companion .md records the version used.
# [Co-developed with claude code -- Adam]
HERE=$(cd "$(dirname "$0")" && pwd) || exit 1
PY="${NDTWIN_PLOTVENV:-$HERE/../../NDTwin Slide material 820/.plotvenv/bin/python3}"
cd "$HERE" || exit 1
"$PY" -c "import matplotlib; print('matplotlib', matplotlib.__version__)" || exit 1
rc=0
for g in make_p02_architecture make_p04_map make_p10_setup make_p13_relief make_p18_health make_p22_roadmap; do
  "$PY" $g.py; r=$?; echo "$g rc=$r"; [ $r -ne 0 ] && rc=$r
done
exit $rc
