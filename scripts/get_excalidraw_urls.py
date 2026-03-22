"""Build hosted edit and animation URLs for a local .excalidraw file.

Auto-discovers the companion .animationinfo.json if it exists alongside the
diagram, and bundles both into the URL hash.

Usage:
    cd {skill-root}/scripts
    uv run python get_excalidraw_urls.py <path-to-file.excalidraw>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from hosted_scene_urls import build_animate_url, build_edit_url, discover_animationinfo


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build hosted edit and animation URLs for an Excalidraw file",
    )
    parser.add_argument("input", type=Path, help="Path to .excalidraw JSON file")
    args = parser.parse_args()

    path = args.input.expanduser().resolve()
    if not path.exists():
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}", file=sys.stderr)
        sys.exit(1)

    anim = discover_animationinfo(path)
    if anim:
        print(f"Animation spec: {anim.name}", file=sys.stderr)
    else:
        print("No .animationinfo.json found — URLs will have no animation spec", file=sys.stderr)

    print("Edit URL:")
    print(build_edit_url(path))
    print()
    print("Animate URL:")
    print(build_animate_url(path))


if __name__ == "__main__":
    main()
