#!/bin/sh
set -e

REPO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SKILL_NAME="hand-drawn-diagrams"

for BASE in "$HOME/.agents/skills" "$HOME/.claude/skills"; do
  mkdir -p "$BASE"
  LINK="$BASE/$SKILL_NAME"
  rm -rf "$LINK"
  ln -s "$REPO_DIR" "$LINK"
  echo "✓ linked $LINK -> $REPO_DIR"
done
