#!/usr/bin/env bash
# Builds lab-verify.zip for upload as a Claude skill (claude.ai: Settings > Capabilities > Skills).
set -euo pipefail
cd "$(dirname "$0")/../.claude/skills"
rm -f ../../lab-verify.zip
zip -rq ../../lab-verify.zip lab-verify -x '*/__pycache__/*'
echo "wrote lab-verify.zip"
