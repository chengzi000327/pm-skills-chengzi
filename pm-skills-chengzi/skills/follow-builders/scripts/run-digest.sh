#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TMP_JSON="${TMPDIR:-/tmp}/follow-builders-prepared.json"
TMP_MD="${TMPDIR:-/tmp}/follow-builders-rendered.md"
NODE_BIN="${NODE_BIN:-node}"

: "${FOLLOW_BUILDERS_HOME:?FOLLOW_BUILDERS_HOME is required}"

"$NODE_BIN" "$SCRIPT_DIR/prepare-digest.js" > "$TMP_JSON"
"$NODE_BIN" "$SCRIPT_DIR/render-digest.js" "$TMP_JSON" > "$TMP_MD"
"$NODE_BIN" "$SCRIPT_DIR/deliver.js" --file "$TMP_MD"
