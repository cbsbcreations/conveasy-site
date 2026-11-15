#!/bin/sh
# Copies the conveasy.ai build (ai/, made by `python3 src/build.py`) into the docs/ folder of a checkout of
# cbsbcreations/conveasy-ai. Commit and push in that checkout afterwards.
# Usage (from this repo's root): sh tools/publish-ai.sh /path/to/conveasy-ai
set -e
DEST=${1:?give the path of the conveasy-ai checkout}
[ -f ai/CNAME ] || { echo "ai/ is missing: run python3 src/build.py first" >&2; exit 1; }
[ -d "$DEST/.git" ] || { echo "$DEST is not a git checkout" >&2; exit 1; }
rm -rf "$DEST/docs"
mkdir -p "$DEST/docs"
cp -a ai/. "$DEST/docs/"
echo "copied ai/ to $DEST/docs/"
