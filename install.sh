#!/bin/sh

REPO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
INSTALLER="$REPO_DIR/installscripts/install.py"

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$INSTALLER" "$@"
fi

if command -v python >/dev/null 2>&1; then
  exec python "$INSTALLER" "$@"
fi

echo "Python is required to run the installer."
echo "Install Python and run this script again."
exit 1
