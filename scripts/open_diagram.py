"""Open or save a diagram in the right mode, inferred or explicit.

Modes
-----
edit            Write a redirect HTML → hosted Excalidraw editor  (default)
animate         Write a redirect HTML → hosted animation view
save-excalidraw Copy the .excalidraw source to the project directory
save-animation  Render and save an .animated.svg to the project directory
save-image      Render and save a .png to the project directory
open-image      Render a .png, save it, then open with the system viewer

The redirect HTML is a single-purpose relay file — it holds the long URL so the
agent can deliver a short, clickable file:// path.  The browser jumps straight to
the hosted page; no intermediate buttons.

Usage
-----
    cd {skill-root}/scripts
    uv run python open_diagram.py <path-to-file.excalidraw> [--mode MODE] [--dest DIR]

    # Edit (default)
    uv run python open_diagram.py /tmp/.../diagram.excalidraw

    # Open the animation view
    uv run python open_diagram.py /tmp/.../diagram.excalidraw --mode animate

    # Save the source file to the project
    uv run python open_diagram.py /tmp/.../diagram.excalidraw --mode save-excalidraw --dest /my/project

    # Render and save animated SVG
    uv run python open_diagram.py /tmp/.../diagram.excalidraw --mode save-animation --dest /my/project

    # Render and save PNG
    uv run python open_diagram.py /tmp/.../diagram.excalidraw --mode save-image --dest /my/project

    # Render PNG and open it
    uv run python open_diagram.py /tmp/.../diagram.excalidraw --mode open-image --dest /my/project

Output (printed to stdout, one line)
--------------------------------------
    edit / animate      →  Launcher: /absolute/path/to/open.html
    save-*              →  Saved: /absolute/path/to/<output-file>
    open-image          →  Opened: /absolute/path/to/<name>.png
"""

from __future__ import annotations

import argparse
import html as _html
import json
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

from hosted_scene_urls import build_animate_url, build_edit_url, discover_animationinfo

# ---------------------------------------------------------------------------
# Redirect HTML — instant relay, no buttons, no intermediate page
# ---------------------------------------------------------------------------

_REDIRECT_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Opening diagram\u2026</title>
  <script>window.location.replace("{url}")</script>
</head>
<body>Opening diagram\u2026</body>
</html>
"""


def _write_redirect(excalidraw_path: Path, target_url: str, suffix: str) -> Path:
    """Write a redirect HTML alongside the diagram and return its path."""
    out = excalidraw_path.with_name(f"open-{suffix}.html")
    escaped = _html.escape(target_url, quote=True)
    out.write_text(_REDIRECT_HTML.format(url=escaped), encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# Mode handlers
# ---------------------------------------------------------------------------

def _open_edit(path: Path, no_open: bool) -> None:
    url = build_edit_url(path)
    launcher = _write_redirect(path, url, "edit")
    print(f"Launcher: {launcher}")
    if not no_open:
        webbrowser.open(launcher.as_uri())


def _open_animate(path: Path, no_open: bool) -> None:
    url = build_animate_url(path)
    launcher = _write_redirect(path, url, "animate")
    print(f"Launcher: {launcher}")
    if not no_open:
        webbrowser.open(launcher.as_uri())


def _save_excalidraw(path: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / path.name
    shutil.copy2(path, out)
    anim = discover_animationinfo(path)
    if anim:
        shutil.copy2(anim, dest / anim.name)
    print(f"Saved: {out}")


def _save_animation(path: Path, dest: Path, scripts_dir: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / path.with_suffix(".animated.svg").name
    result = subprocess.run(
        ["uv", "run", "python", "render_animated_svg.py", str(path), "--output", str(out)],
        cwd=scripts_dir,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    print(f"Saved: {out}")


def _save_image(path: Path, dest: Path, scripts_dir: Path) -> Path:
    dest.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["uv", "run", "python", "render_excalidraw.py", str(path)],
        cwd=scripts_dir,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    # render_excalidraw.py writes a .png next to the source; move it to dest
    rendered = path.with_suffix(".png")
    if not rendered.exists():
        print(f"ERROR: Expected PNG not found at {rendered}", file=sys.stderr)
        sys.exit(1)
    out = dest / rendered.name
    shutil.move(str(rendered), out)
    return out


def _save_and_open_image(path: Path, dest: Path, scripts_dir: Path) -> None:
    out = _save_image(path, dest, scripts_dir)
    print(f"Opened: {out}")
    # Use the system viewer
    if sys.platform == "darwin":
        subprocess.run(["open", str(out)], check=False)
    elif sys.platform == "win32":
        subprocess.run(["start", str(out)], shell=True, check=False)
    else:
        subprocess.run(["xdg-open", str(out)], check=False)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

MODES = ("edit", "animate", "save-excalidraw", "save-animation", "save-image", "open-image")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Open or save a diagram in the right mode",
    )
    parser.add_argument("input", type=Path, help="Path to .excalidraw JSON file")
    parser.add_argument(
        "--mode",
        choices=MODES,
        default="edit",
        help=(
            "edit (default) | animate | save-excalidraw | "
            "save-animation | save-image | open-image"
        ),
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=None,
        help="Destination directory for save-* and open-image modes (default: same dir as input)",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="For edit/animate: write the HTML but do not open the browser",
    )
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

    dest = (args.dest or path.parent).expanduser().resolve()
    scripts_dir = Path(__file__).parent

    if args.mode == "edit":
        _open_edit(path, args.no_open)
    elif args.mode == "animate":
        _open_animate(path, args.no_open)
    elif args.mode == "save-excalidraw":
        _save_excalidraw(path, dest)
    elif args.mode == "save-animation":
        _save_animation(path, dest, scripts_dir)
    elif args.mode == "save-image":
        out = _save_image(path, dest, scripts_dir)
        print(f"Saved: {out}")
    elif args.mode == "open-image":
        _save_and_open_image(path, dest, scripts_dir)


if __name__ == "__main__":
    main()
