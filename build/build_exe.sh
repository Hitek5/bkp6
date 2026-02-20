#!/usr/bin/env bash
set -euo pipefail

python -m pip install -r requirements.txt
pyinstaller --noconfirm --clean bkp6.spec

echo "Build complete: dist/bkp6-mvp"
