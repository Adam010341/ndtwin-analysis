#!/bin/bash
# Regenerate the five figures with the matplotlib venv (3.11.1); the generators and figstyle_1021.py stop if
# matplotlib is not 3.11.x, and every companion .md records the version used.
# [Co-developed with claude code -- Adam]
PY="/home/adam/Desktop/NDTwin slide material/NDTwin Slide material 820/.plotvenv/bin/python3"
cd "$(dirname "$0")" || exit 1
"$PY" -c "import matplotlib; print('matplotlib', matplotlib.__version__)" || exit 1
rc=0
for g in make_p02_architecture make_p04_map make_p10_setup make_p13_relief make_p20_roadmap; do
  "$PY" $g.py; r=$?; echo "$g rc=$r"; [ $r -ne 0 ] && rc=$r
done
exit $rc
