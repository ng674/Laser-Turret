#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

python_bin="${PYTHON:-python3}"
if ! command -v "$python_bin" >/dev/null 2>&1; then
  echo "error: $python_bin is not available" >&2
  exit 1
fi

"$python_bin" -c 'import sys; assert sys.version_info >= (3, 11), "Python 3.11+ is required"'

if [[ ! -d .venv ]]; then
  "$python_bin" -m venv .venv
fi

.venv/bin/python -m pip install --upgrade pip setuptools wheel
.venv/bin/python -m pip install -e '.[sim,dev]'
.venv/bin/python scripts/check_simulation_environment.py

echo "Simulation environment is ready."
echo "Activate it with: source .venv/bin/activate"
