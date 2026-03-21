"""Open an Excalidraw file in the hosted Excalidraw editor.

Usage:
    cd {skill-root}/scripts
    uv run python edit_excalidraw.py <path-to-file.excalidraw>

The diagram is gzip-compressed, base64-encoded, and passed as a URL hash to
the hosted editor app.  Edit freely, then click "Download .excalidraw" to save.
"""

from __future__ import annotations

import argparse
import json
import sys
import webbrowser
from pathlib import Path

from hosted_scene_urls import EDIT_URL, encode_diagram

GITHUB_PAGES_URL: str | None = EDIT_URL

_SCRIPT_DIR = Path(__file__).parent
_EDIT_HTML  = _SCRIPT_DIR.parent.parent.parent / "hostedapp" / "edit.html"
def open_with_github_pages(hash_data: str) -> None:
    url = f"{GITHUB_PAGES_URL}#{hash_data}"
    print(f"Opening: {GITHUB_PAGES_URL}")
    webbrowser.open(url)


def open_with_local_server(hash_data: str) -> None:
    try:
        from local_excalidraw_server import LocalExcalidrawServer
    except ImportError:
        sys.path.insert(0, str(_SCRIPT_DIR))
        from local_excalidraw_server import LocalExcalidrawServer  # type: ignore[no-redef]

    html = _EDIT_HTML.read_text(encoding="utf-8")
    server = LocalExcalidrawServer(
        pages={"/edit.html": (html, "text/html; charset=utf-8")},
    )
    server.start()

    url = f"{server.url_for('/edit.html')}#{hash_data}"
    print(f"Serving locally: {server.url_for('/edit.html')}")
    print("Opening browser... Press Ctrl+C to stop the server when done.")
    webbrowser.open(url)

    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        print("Server stopped.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Open an Excalidraw file in the hosted editor")
    parser.add_argument("input", type=Path, help="Path to .excalidraw JSON file")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"ERROR: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    hash_data = encode_diagram(args.input)
    size_kb   = len(hash_data) / 1024
    print(f"Encoded size: {size_kb:.1f} KB")

    if size_kb > 2000:
        print("WARNING: Encoded data exceeds 2 MB — some browsers may truncate the URL.")

    if GITHUB_PAGES_URL:
        open_with_github_pages(hash_data)
    else:
        if not _EDIT_HTML.exists():
            print(f"ERROR: edit.html not found at {_EDIT_HTML}", file=sys.stderr)
            sys.exit(1)
        open_with_local_server(hash_data)


if __name__ == "__main__":
    main()
