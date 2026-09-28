#!/usr/bin/env bash
# Runs every lab check. Usage: scripts/verify.sh [--offline]
# Set PYTHON to choose the interpreter (default: python3, needs >= 3.11).
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${PYTHON:-python3}"
exec "$PY" scripts/verify.py "$@"
