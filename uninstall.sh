#!/bin/sh

REPO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
UNINSTALLER="$REPO_DIR/installscripts/uninstall.py"

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$UNINSTALLER" "$@"
fi

if command -v python >/dev/null 2>&1; then
  exec python "$UNINSTALLER" "$@"
fi

echo "Python is required to run the uninstaller."
echo "Install Python and run this script again."
exit 1
