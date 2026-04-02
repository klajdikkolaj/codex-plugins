#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 -m py_compile "${ROOT_DIR}/scripts/create-plugin.py"

for plugin_dir in "${ROOT_DIR}"/plugins/*; do
  [[ -d "${plugin_dir}" ]] || continue
  if [[ -x "${plugin_dir}/scripts/validate.sh" ]]; then
    echo "Validating $(basename "${plugin_dir}")"
    bash "${plugin_dir}/scripts/validate.sh"
  else
    echo "Skipping $(basename "${plugin_dir}"): no validate.sh"
  fi
done

echo "Workspace validation passed."
