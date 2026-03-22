"""Open an Excalidraw file as an animation in the browser.

Usage:
    cd {skill-root}/scripts
    uv run python animate_excalidraw.py <path-to-file.excalidraw>

The diagram is gzip-compressed, base64-encoded, and passed as a URL hash to
the hosted animation app.  No extra dependencies beyond the existing venv.

Once GitHub Pages is live, set GITHUB_PAGES_URL below and the local server is
no longer needed — the script will just open the remote URL directly.
"""

from __future__ import annotations

import argparse
import json
import sys
import webbrowser
from pathlib import Path

from hosted_scene_urls import ANIMATE_URL, encode_diagram

# Set this to your GitHub Pages URL once deployed, e.g.:
# "https://youruser.github.io/hand-drawn-diagrams/docs/animate.html"
GITHUB_PAGES_URL: str | None = ANIMATE_URL

def open_with_github_pages(hash_data: str) -> None:
    url = f"{GITHUB_PAGES_URL}#{hash_data}"
    print(f"Opening: {GITHUB_PAGES_URL}")
    webbrowser.open(url)


def main() -> None:
    parser = argparse.ArgumentParser(description="Animate an Excalidraw file in browser")
    parser.add_argument("input", type=Path, help="Path to .excalidraw JSON file")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"ERROR: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Quick sanity check
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if not data.get("elements"):
        print("ERROR: No elements found in diagram.", file=sys.stderr)
        sys.exit(1)

    hash_data = encode_diagram(args.input)
    size_kb   = len(hash_data) / 1024
    print(f"Encoded size: {size_kb:.1f} KB")

    if size_kb > 2000:
        print("WARNING: Encoded data exceeds 2 MB — some browsers may truncate the URL.")

    if not GITHUB_PAGES_URL:
        print("ERROR: Hosted animate URL is not configured.", file=sys.stderr)
        sys.exit(1)

    open_with_github_pages(hash_data)


if __name__ == "__main__":
    main()
