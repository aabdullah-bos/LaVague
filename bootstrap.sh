#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

python -m venv "${VENV_DIR}"
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

python -m pip install -U pip

# Install local subprojects in editable mode so path dependencies resolve.
python -m pip install -e "${ROOT_DIR}/lavague-core"
python -m pip install -e "${ROOT_DIR}/lavague-integrations/contexts/lavague-contexts-openai"
python -m pip install -e "${ROOT_DIR}/lavague-integrations/drivers/lavague-drivers-selenium"
python -m pip install -e "${ROOT_DIR}/lavague-tests"
python -m pip install -e "${ROOT_DIR}/lavague-qa"

echo "Bootstrap complete. Activate with: source ${VENV_DIR}/bin/activate"
