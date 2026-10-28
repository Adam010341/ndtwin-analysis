#!/bin/bash
# Build NDTwin_deck_1028.pptx the way 1014 was built: conda env webgui-node's node, pptxgenjs from an existing
# node_modules through NODE_PATH. No download, no install. NODE_PATH may be set by the caller; otherwise the
# first cowork-session outputs/node_modules that holds pptxgenjs is used (found by glob, not pinned).
# [Co-developed with claude code -- Adam]
if [ -z "$NODE_PATH" ]; then
  pkg=$(ls -d "$HOME"/.config/Claude/local-agent-mode-sessions/*/*/*/outputs/node_modules/pptxgenjs 2>/dev/null | head -1)
  [ -n "$pkg" ] || { echo "run_build_1028.sh: no node_modules with pptxgenjs found; set NODE_PATH" >&2; exit 2; }
  export NODE_PATH=$(dirname "$pkg")
fi
cd "$(dirname "$0")/.." && conda run -n webgui-node node generator/build_deck_1028.js
