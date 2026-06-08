#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PIP="${PIP:-python3 -m pip}"

cd "$ROOT"
$PIP install -e .
$PIP install -e packages/dsl2gillm
$PIP install -e packages/uri2gillm
$PIP install -e packages/nlp2gillm
$PIP install -e packages/cli2gillm
$PIP install -e packages/mcp2gillm
$PIP install -e packages/rest2gillm
echo "✓ gillm control layers installed"
