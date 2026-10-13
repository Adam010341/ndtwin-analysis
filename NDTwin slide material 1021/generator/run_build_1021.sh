#!/bin/bash
# Build NDTwin_deck_1021.pptx the way 930 was built (template 1b): conda env webgui-node's node, pptxgenjs 4.0.1
# from the cowork session's outputs/node_modules through NODE_PATH. No download, no install.
# [Co-developed with claude code -- Adam]
export NODE_PATH=/home/adam/.config/Claude/local-agent-mode-sessions/740b7c88-df32-4eb9-b383-248b5d7648c1/c7bf5182-caa3-411b-9b68-3914b9e29fe2/local_d9cbde44-6f6d-4599-be2d-61511d422ece/outputs/node_modules
cd "$(dirname "$0")/.." && conda run -n webgui-node node generator/build_deck_1021.js
