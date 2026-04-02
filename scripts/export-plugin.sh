#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_NAME="${1:-}"

if [[ -z "${PLUGIN_NAME}" ]]; then
  echo "Usage: bash scripts/export-plugin.sh <plugin-name>" >&2
  exit 1
fi

PLUGIN_DIR="${ROOT_DIR}/plugins/${PLUGIN_NAME}"
EXPORT_SCRIPT="${PLUGIN_DIR}/scripts/export-github-repo.sh"
PACKAGE_SCRIPT="${PLUGIN_DIR}/scripts/package-release.sh"

if [[ ! -d "${PLUGIN_DIR}" ]]; then
  echo "Plugin not found: ${PLUGIN_NAME}" >&2
  exit 1
fi

if [[ -x "${EXPORT_SCRIPT}" ]]; then
  bash "${EXPORT_SCRIPT}" "${ROOT_DIR}/artifacts/github-repo"
else
  echo "Skipping standalone repo export: ${EXPORT_SCRIPT} not found or not executable"
fi

if [[ -x "${PACKAGE_SCRIPT}" ]]; then
  bash "${PACKAGE_SCRIPT}" "${ROOT_DIR}/artifacts/releases"
else
  echo "Skipping release archive: ${PACKAGE_SCRIPT} not found or not executable"
fi
