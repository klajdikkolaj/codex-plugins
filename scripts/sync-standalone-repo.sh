#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_NAME="${1:-}"
TARGET_REPO="${2:-}"

if [[ -z "${PLUGIN_NAME}" || -z "${TARGET_REPO}" ]]; then
  echo "Usage: bash scripts/sync-standalone-repo.sh <plugin-name> <absolute-target-repo-path>" >&2
  exit 1
fi

TARGET_REPO="$(cd "${TARGET_REPO}" && pwd)"
EXPORTED_REPO="${ROOT_DIR}/artifacts/github-repo/${PLUGIN_NAME}"

bash "${ROOT_DIR}/scripts/export-plugin.sh" "${PLUGIN_NAME}"

if [[ ! -d "${EXPORTED_REPO}" ]]; then
  echo "Expected exported repo at ${EXPORTED_REPO}" >&2
  exit 1
fi

if [[ ! -d "${TARGET_REPO}/.git" ]]; then
  echo "Target repo is not a git checkout: ${TARGET_REPO}" >&2
  exit 1
fi

rsync -a --delete \
  --exclude '.git' \
  "${EXPORTED_REPO}/" "${TARGET_REPO}/"

echo "Synced ${PLUGIN_NAME} into ${TARGET_REPO}"
echo "Next steps:"
echo "1. git -C ${TARGET_REPO} status"
echo "2. commit and push from the standalone repo if the diff looks correct"
