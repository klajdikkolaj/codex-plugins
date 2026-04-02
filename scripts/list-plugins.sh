#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

find "${ROOT_DIR}/plugins" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort
