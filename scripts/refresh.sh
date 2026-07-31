#!/bin/bash
# Monthly dataset refresh: regenerate CSV from the prod screening cache, push if changed.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/generate.py
if ! git diff --quiet -- data/; then
  day=$(date -u +%F)
  sed -i "s/\*\*Snapshot generated:\*\* [0-9-]\+/**Snapshot generated:** ${day}/" README.md
  git add data/ README.md
  git commit -m "Monthly refresh: snapshot ${day}"
  git push
  echo "pushed snapshot ${day}"
else
  echo "no changes"
fi
